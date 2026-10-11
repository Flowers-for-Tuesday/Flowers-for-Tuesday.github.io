"""Local-only preview with source watching and browser reload; no runtime packages."""
import io
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
from urllib.parse import unquote, urlsplit
import webbrowser

from manage import BASE, build_lock, generate, say

PUBLIC_DIRECTORIES = {"about", "note", "music", "gallery", "publication", "assets", "files"}
PUBLIC_FILES = {"index.html", "404.html", "favicon.ico", "robots.txt", "sitemap.xml"}
IGNORED = {"__pycache__", "code.css"}
RELOAD_SCRIPT = r"""
<script data-local-preview>
(() => {
  let version = null;
  const badge = document.createElement('div');
  badge.id = 'local-preview-status';
  badge.setAttribute('role', 'status');
  badge.style.cssText = 'position:fixed;bottom:12px;right:12px;z-index:2147483647;max-width:min(720px,90vw);max-height:55vh;overflow:auto;padding:8px 12px;border-radius:8px;background:#25352d;color:white;font:13px/1.6 system-ui;white-space:pre-wrap;box-shadow:0 2px 12px #0003';
  document.body.append(badge);
  async function poll() {
    try {
      const response = await fetch('/__dev/status', {cache:'no-store'});
      if (!response.ok) throw new Error('Preview unavailable');
      const state = await response.json();
      if (version !== null && state.version !== version) {
        location.reload();
        return;
      }
      version = state.version;
      badge.textContent = state.error ? '生成失败，修正并保存后会自动重试\n' + state.error :
        state.building ? '本地预览 · 正在生成…' : '本地预览 · 保存后自动刷新';
      badge.style.background = state.error ? '#7c2e2e' : '#25352d';
    } catch (_) {
      badge.textContent = '本地预览已断开，请重新运行 preview.cmd';
    }
    setTimeout(poll, 900);
  }
  poll();
})();
</script>
"""


def source_snapshot(base=BASE):
    """Ignore generated HTML, manifests and highlighted CSS to avoid build loops."""
    paths = [base / "README.md", base / "favicon.ico", base / "requirements.txt"]
    for folder in ("templates", "scripts", "content", "assets", "files"):
        root = base / folder
        if root.exists():
            paths.extend(root.rglob("*"))
    result = {}
    for path in paths:
        relative = path.relative_to(base)
        if any(part.startswith(".") or part in IGNORED for part in relative.parts):
            continue
        try:
            if path.is_file():
                stat = path.stat()
                result[relative.as_posix()] = (stat.st_mtime_ns, stat.st_size)
        except FileNotFoundError:
            pass  # Editors may replace a file between listing and stat.
    return result


class PreviewState:
    def __init__(self):
        self.lock = threading.Lock()
        self.version = 0
        self.building = False
        self.error = ""

    def data(self):
        with self.lock:
            return {"version": self.version, "building": self.building, "error": self.error}

    def rebuild(self, python):
        with self.lock:
            self.building = True
        try:
            with build_lock():
                result = generate(python, capture=True)
            if result.stdout.strip():
                say(result.stdout.strip())
            with self.lock:
                self.version += 1
                self.error = ""
        except (RuntimeError, OSError) as error:
            say(f"生成失败，保存修改后自动重试：\n{error}")
            with self.lock:
                self.error = str(error)
        finally:
            with self.lock:
                self.building = False


def handler_for(state, base=BASE):
    class Handler(SimpleHTTPRequestHandler):
        extensions_map = {**SimpleHTTPRequestHandler.extensions_map,
                          ".svg": "image/svg+xml", ".woff2": "font/woff2",
                          ".md": "text/markdown; charset=utf-8"}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(base), **kwargs)

        def end_headers(self):
            self.send_header("Cache-Control", "no-store")
            super().end_headers()

        def bytes_response(self, body, content_type):
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            return io.BytesIO(body)

        def send_head(self):
            url_path = unquote(urlsplit(self.path).path)
            if url_path == "/__dev/status":
                return self.bytes_response(json.dumps(state.data()).encode(), "application/json; charset=utf-8")
            path = Path(self.translate_path(self.path)).resolve()
            try:
                relative = path.relative_to(base.resolve())
            except ValueError:
                self.send_error(403)
                return None
            parts = relative.parts
            if (any(part.startswith(".") for part in parts) or
                    (parts and parts[0] not in PUBLIC_DIRECTORIES and relative.as_posix() not in PUBLIC_FILES)):
                self.send_error(404)
                return None
            if path.is_dir() and url_path.endswith("/"):
                path = path / "index.html"
            if path.suffix.lower() == ".html":
                if path.is_file():
                    body = path.read_text(encoding="utf-8")
                elif state.data()["error"]:
                    body = '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>本地预览</title><body><p>页面尚未生成，请查看下方错误信息。</p></body></html>'
                else:
                    return super().send_head()
                body = body.replace("</body>", RELOAD_SCRIPT + "</body>") if "</body>" in body else body + RELOAD_SCRIPT
                return self.bytes_response(body.encode("utf-8"), "text/html; charset=utf-8")
            return super().send_head()

        def list_directory(self, path):
            self.send_error(404)
            return None

        def log_message(self, format, *args):
            # Polling should not flood the terminal; retain useful HTTP failures.
            if len(args) > 1 and str(args[1]).startswith(("4", "5")):
                super().log_message(format, *args)

    return Handler


def watch(python, state, stopped, previous):
    candidate = previous
    while not stopped.wait(.5):
        current = source_snapshot()
        if current != candidate:
            candidate = current
            continue  # Debounce until the next stable snapshot.
        if current != previous:
            previous = current
            say("检测到文件修改，重新生成…")
            state.rebuild(python)


def serve(python, port=8000, open_browser=False):
    say("Preparing local preview…")
    state = PreviewState()
    try:
        server = ThreadingHTTPServer(("127.0.0.1", port), handler_for(state))
    except OSError as error:
        raise RuntimeError(f"无法启动本地预览：端口 {port} 可能已被占用。可使用 --port 8001 指定其他端口。\n{error}") from error
    stopped = threading.Event()
    try:
        previous = source_snapshot()
        state.rebuild(python)
        watcher = threading.Thread(target=watch, args=(python, state, stopped, previous), daemon=True)
        watcher.start()
        address = f"http://127.0.0.1:{server.server_port}"
        say(f"Preview ready: {address}")
        say("保存 Markdown、JSON、模板或样式后，浏览器会自动刷新。按 Ctrl+C 停止。")
        if open_browser:
            webbrowser.open(address)
        server.serve_forever(poll_interval=.3)
    finally:
        stopped.set()
        server.server_close()
