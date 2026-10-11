"""Local setup, preview, and one-command publishing. Uses only the standard library."""
import argparse
from contextlib import contextmanager
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parents[1]
LOCAL = BASE / ".local"


def say(message):
    print(message, flush=True)


def run(args, *, capture=False, check=True, cwd=BASE):
    result = subprocess.run([str(arg) for arg in args], cwd=cwd, text=True,
                            encoding="utf-8", errors="replace", capture_output=capture)
    if check and result.returncode:
        detail = (result.stderr or result.stdout or "").strip() if capture else ""
        raise RuntimeError(f"命令执行失败（{result.returncode}）：{args[0]} {args[1]}\n{detail}")
    return result


@contextmanager
def build_lock(timeout=120):
    """An OS-managed lock: preview and publish cannot generate files concurrently."""
    LOCAL.mkdir(exist_ok=True)
    with (LOCAL / "build.lock").open("a+b") as handle:
        if handle.tell() == 0:
            handle.write(b"0")
            handle.flush()
        deadline = time.monotonic() + timeout
        while True:
            try:
                handle.seek(0)
                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if time.monotonic() >= deadline:
                    raise RuntimeError("另一个生成或发布任务仍在运行，请等待它完成后重试。")
                time.sleep(.25)
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)


def setup():
    if sys.version_info < (3, 10):
        raise RuntimeError("请先安装 Python 3.10 或更新版本。")
    if not shutil.which("node"):
        raise RuntimeError("请先安装 Node.js 18 或更新版本，公式排版需要使用它。")
    version = run(["node", "--version"], capture=True).stdout.strip()
    if int(version.lstrip("v").split(".")[0]) < 18:
        raise RuntimeError("Node.js 版本过低，请升级到 18 或更新版本。")
    python = BASE / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    stamp = BASE / ".venv/.requirements.sha256"
    digest = hashlib.sha256((BASE / "requirements.txt").read_bytes()).hexdigest()
    with build_lock(timeout=300):
        if not python.exists():
            say("首次运行：正在创建项目专用 Python 环境……")
            run([sys.executable, "-m", "venv", str(BASE / ".venv")])
        if not stamp.exists() or stamp.read_text().strip() != digest:
            say("正在安装项目依赖（仅首次运行或依赖更新时需要联网）……")
            run([python, "-m", "pip", "install", "--disable-pip-version-check", "-r", "requirements.txt"])
            stamp.write_text(digest + "\n", encoding="ascii")
    return python


def generate(python, *, capture=False):
    # The caller holds build_lock, including when used by the preview watcher.
    return run([python, "-u", "scripts/build.py"], capture=capture)


def git(*args, check=True):
    command = ["git", "-c", "core.quotepath=false"]
    # Use native OpenSSH on Windows, preserving any explicit user override.
    native_ssh = Path(os.environ.get("WINDIR", "C:/Windows")) / "System32/OpenSSH/ssh.exe"
    if os.name == "nt" and native_ssh.exists() and not os.environ.get("GIT_SSH_COMMAND"):
        command += ["-c", f'core.sshCommand="{native_ssh.as_posix()}" -o BatchMode=yes -o ConnectTimeout=15']
    return run([*command, *args], capture=True, check=check)


def github_repository(remote):
    match = re.fullmatch(r"(?:git@github\.com:|https://github\.com/|ssh://git@github\.com/)([\w.-]+/[\w.-]+?)(?:\.git)?/?", remote.strip())
    if not match:
        raise RuntimeError("origin 需要指向 GitHub 仓库的 SSH 或 HTTPS 地址。")
    return match.group(1)


def api(path):
    request = Request("https://api.github.com/" + path, headers={
        "Accept": "application/vnd.github+json", "User-Agent": "Flowers-for-Tuesday-publisher",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urlopen(request, timeout=20) as response:
        return json.load(response)


def deployment_state(runs, jobs_for):
    """A successful build with a skipped deploy is NOT a published website."""
    relevant = [r for r in runs if r.get("name") == "pages build and deployment" or r.get("path", "").split("@")[0] == ".github/workflows/pages.yml"]
    # Reruns supersede earlier runs of the same workflow for this commit.
    newest = {}
    for run_info in sorted(relevant, key=lambda r: r["id"], reverse=True):
        newest.setdefault(run_info.get("workflow_id", run_info.get("name")), run_info)
    pending = not relevant
    deployed_link = None
    for info in newest.values():
        if info["status"] != "completed":
            pending = True
            continue
        if info["conclusion"] not in ("success", "skipped"):
            return "failed", info.get("html_url", "")
        if info.get("name") == "pages build and deployment" and info["conclusion"] == "success":
            deployed_link = info.get("html_url", "")
            continue
        for job in jobs_for(info["id"]):
            if job["name"] == "deploy" and job.get("conclusion") == "success":
                deployed_link = info.get("html_url", "")
    if pending:
        return "pending", ""
    if deployed_link is not None:
        return "deployed", deployed_link
    return "not-deployed", ""


def wait_for_deployment(repository, sha, timeout=300):
    say(f"等待 GitHub 部署提交 {sha[:7]}……")
    say(f"构建记录：https://github.com/{repository}/actions")
    deadline = time.monotonic() + timeout
    cache = {}
    def jobs_for(run_id):
        if run_id not in cache:
            cache[run_id] = api(f"repos/{repository}/actions/runs/{run_id}/jobs?per_page=100")["jobs"]
        return cache[run_id]
    last_state = None
    while True:
        try:
            runs = api(f"repos/{repository}/actions/runs?head_sha={sha}&per_page=30")["workflow_runs"]
            # Also verify the SHA locally rather than relying solely on the API filter.
            state, link = deployment_state([r for r in runs if r.get("head_sha") == sha], jobs_for)
        except (HTTPError, URLError, TimeoutError, OSError) as error:
            say(f"代码已保存在远程，但暂时无法查询部署状态：{error}")
            say("可稍后运行 python scripts/manage.py status 再检查。")
            return 2
        if state == "deployed":
            owner, repo = repository.split("/")
            suffix = "" if repo.casefold() == f"{owner}.github.io".casefold() else repo + "/"
            say(f"部署成功：https://{owner.lower()}.github.io/{suffix}")
            say(f"部署记录：{link}")
            return 0
        if state == "failed":
            say(f"代码已推送，但 GitHub 构建或部署失败：{link}")
            return 1
        if state != last_state:
            say("构建尚未完成，正在等待……" if state == "pending" else "构建已完成，等待发布任务……")
            last_state = state
        if time.monotonic() >= deadline:
            say("代码已推送，但尚未确认部署完成。")
            if state == "not-deployed":
                say(f"请检查 https://github.com/{repository}/settings/pages ，将 Source 设为 GitHub Actions。")
            say("可稍后运行 python scripts/manage.py status 再检查。")
            return 2
        time.sleep(min(12, max(0, deadline - time.monotonic())))


def publish(python, message, wait=True, timeout=300):
    branch = git("branch", "--show-current").stdout.strip()
    if branch != "main":
        raise RuntimeError(f"当前分支为 {branch or 'detached HEAD'}；请先切换到 main，再发布。")
    repository = github_repository(git("remote", "get-url", "origin").stdout)
    with build_lock():
        say("1/4 检查远程分支……")
        git("fetch", "origin", "main")
        ancestor = git("merge-base", "--is-ancestor", "origin/main", "HEAD", check=False)
        if ancestor.returncode == 1:
            raise RuntimeError("远程 main 有本地尚未包含的提交。请先处理本地修改并同步远程，再发布；本次未提交或推送。")
        if ancestor.returncode:
            raise RuntimeError("无法比较本地与远程分支。")
        say("2/4 生成页面并检查……")
        generate(python)
        run([python, "-m", "unittest", "discover", "-s", "tests", "-q"])
        for path in sorted((BASE / "assets/js").glob("*.js")):
            run(["node", "--check", path])
        say("3/4 提交项目修改……")
        changes = git("status", "--short").stdout.strip()
        if changes:
            say(changes)
        git("add", "--all")
        staged = git("diff", "--cached", "--quiet", check=False)
        if staged.returncode == 1:
            result = git("commit", "-m", message or f"Update website {datetime.now():%Y-%m-%d %H:%M}")
            say(result.stdout.strip())
        elif staged.returncode:
            raise RuntimeError("无法读取暂存区状态。")
        else:
            say("没有新的文件修改，将继续推送已有提交。")
        sha = git("rev-parse", "HEAD").stdout.strip()
        say("4/4 推送至 origin/main……")
        result = git("push", "--set-upstream", "origin", "main")
        say((result.stdout + result.stderr).strip())
    say(f"已推送：{sha[:7]}")
    return wait_for_deployment(repository, sha, timeout) if wait else 0


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Flowers for Tuesday：本地预览与快捷发布")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("setup", help="创建专用 Python 环境并安装依赖")
    commands.add_parser("build", help="重新生成网站")
    preview = commands.add_parser("preview", help="监听修改并自动刷新浏览器")
    preview.add_argument("--open", action="store_true", help="打开默认浏览器")
    preview.add_argument("--port", type=int, default=8000)
    publishing = commands.add_parser("publish", help="生成、检查、提交、推送并等待部署")
    publishing.add_argument("-m", "--message", default="", help="本次 Git 提交说明")
    publishing.add_argument("--no-wait", action="store_true", help="推送后立即结束，不等待部署")
    publishing.add_argument("--timeout", type=int, default=300, help="等待部署的最长秒数")
    status = commands.add_parser("status", help="检查当前提交的部署状态")
    status.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    try:
        if args.command == "status":
            repository = github_repository(git("remote", "get-url", "origin").stdout)
            return wait_for_deployment(repository, git("rev-parse", "HEAD").stdout.strip(), args.timeout)
        python = setup()
        if args.command == "setup":
            say("环境准备完成。可以双击 preview.cmd 或 publish.cmd。")
        elif args.command == "preview":
            from dev import serve
            serve(python, port=args.port, open_browser=args.open)
        elif args.command == "build":
            with build_lock():
                generate(python)
        elif args.command == "publish":
            return publish(python, args.message, not args.no_wait, args.timeout)
        return 0
    except KeyboardInterrupt:
        say("\n操作已停止。已完成的本地提交不会被撤销。")
        return 130
    except (RuntimeError, OSError, ValueError) as error:
        say(f"\n未完成：{error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
