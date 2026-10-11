"""Local publishing control flow and preview regression checks; no network or Git writes."""
from contextlib import nullcontext
from pathlib import Path
from subprocess import CompletedProcess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import manage
import dev


def workflow(identifier=1, name="Build and publish website", **overrides):
    return {"id": identifier, "workflow_id": name, "name": name,
            "path": ".github/workflows/pages.yml", "status": "completed",
            "conclusion": "success", "html_url": "https://example.test/run", **overrides}


class DeploymentTests(unittest.TestCase):
    def test_github_remote_formats(self):
        for remote in ("git@github.com:Flowers-for-Tuesday/blog.git",
                       "https://github.com/Flowers-for-Tuesday/blog.git",
                       "ssh://git@github.com/Flowers-for-Tuesday/blog",
                       "https://github.com/Flowers-for-Tuesday/blog/"):
            self.assertEqual(manage.github_repository(remote), "Flowers-for-Tuesday/blog")
        with self.assertRaises(RuntimeError):
            manage.github_repository("https://example.com/user/blog")

    def test_skipped_deployment_is_not_success(self):
        state, _ = manage.deployment_state([workflow()], lambda _: [{"name": "deploy", "conclusion": "skipped"}])
        self.assertEqual(state, "not-deployed")

    def test_both_pages_modes_confirm_actual_deployment(self):
        legacy = workflow(name="pages build and deployment", path="dynamic/pages/pages-build-deployment")
        self.assertEqual(manage.deployment_state([legacy], lambda _: [])[0], "deployed")
        self.assertEqual(manage.deployment_state([workflow()], lambda _: [{"name": "deploy", "conclusion": "success"}])[0], "deployed")

    def test_pending_checks_and_failed_checks_are_not_success(self):
        legacy = workflow(2, name="pages build and deployment")
        for status, conclusion, expected in (("in_progress", None, "pending"), ("completed", "failure", "failed")):
            state, _ = manage.deployment_state([legacy, workflow(status=status, conclusion=conclusion)], lambda _: [])
            self.assertEqual(state, expected)
        self.assertEqual(manage.deployment_state([], lambda _: [])[0], "pending")

    def test_newest_run_supersedes_previous_failure(self):
        runs = [workflow(conclusion="failure"), workflow(2)]
        self.assertEqual(manage.deployment_state(runs, lambda _: [{"name": "deploy", "conclusion": "success"}])[0], "deployed")

    def test_status_filters_exact_commit(self):
        with patch.object(manage, "api", return_value={"workflow_runs": [workflow(head_sha="old")]}), \
                patch.object(manage, "say"):
            self.assertEqual(manage.wait_for_deployment("owner/repo", "new", timeout=0), 2)


class PublishTests(unittest.TestCase):
    def fake_git(self, *args, **kwargs):
        output = {("branch", "--show-current"): "main",
                  ("remote", "get-url", "origin"): "git@github.com:owner/repo.git",
                  ("rev-parse", "HEAD"): "abc123"}.get(args, "")
        return CompletedProcess(args, 0, output, "")

    def test_build_failure_prevents_staging_or_pushing(self):
        with patch.object(manage, "git", side_effect=self.fake_git) as git, \
                patch.object(manage, "build_lock", return_value=nullcontext()), \
                patch.object(manage, "generate", side_effect=RuntimeError("broken Markdown")), \
                patch.object(manage, "say"):
            with self.assertRaisesRegex(RuntimeError, "broken Markdown"):
                manage.publish("python", "test", wait=False)
            self.assertFalse(any(call.args[0] in ("add", "commit", "push") for call in git.call_args_list))

    def test_remote_ahead_prevents_build_or_git_mutations(self):
        def ahead(*args, **kwargs):
            if args[0] == "merge-base":
                return CompletedProcess(args, 1, "", "")
            return self.fake_git(*args, **kwargs)
        with patch.object(manage, "git", side_effect=ahead) as git, \
                patch.object(manage, "build_lock", return_value=nullcontext()), \
                patch.object(manage, "generate") as build, patch.object(manage, "say"):
            with self.assertRaises(RuntimeError):
                manage.publish("python", "test", wait=False)
            build.assert_not_called()
            self.assertFalse(any(call.args[0] in ("add", "commit", "push") for call in git.call_args_list))

    def test_retry_pushes_existing_commit_without_empty_commit(self):
        with patch.object(manage, "git", side_effect=self.fake_git) as git, \
                patch.object(manage, "build_lock", return_value=nullcontext()), \
                patch.object(manage, "generate"), patch.object(manage, "run"), \
                patch.object(manage, "say"):
            self.assertEqual(manage.publish("python", "test", wait=False), 0)
            self.assertTrue(any(call.args[0] == "push" for call in git.call_args_list))
            self.assertFalse(any(call.args[0] == "commit" for call in git.call_args_list))


class PreviewTests(unittest.TestCase):
    def test_snapshot_tracks_sources_and_ignores_generated_files(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            for name in ("note/example/main.md", "note/example/index.html", "note/.generated-pages.json",
                         "assets/css/site.css", "assets/css/code.css", "templates/base.html"):
                path = base / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("test", encoding="utf-8")
            snapshot = dev.source_snapshot(base)
            self.assertEqual(set(snapshot), {"note/example/main.md", "assets/css/site.css", "templates/base.html"})
            (base / "assets/css/site.css").write_text("changed", encoding="utf-8")
            self.assertNotEqual(snapshot, dev.source_snapshot(base))

    def test_preview_recovers_from_build_error(self):
        state = dev.PreviewState()
        with patch.object(dev, "build_lock", return_value=nullcontext()), patch.object(dev, "say"), \
                patch.object(dev, "generate", side_effect=[RuntimeError("invalid math"), CompletedProcess([], 0, "", "")]):
            state.rebuild("python")
            self.assertEqual(state.data(), {"version": 0, "building": False, "error": "invalid math"})
            state.rebuild("python")
            self.assertEqual(state.data(), {"version": 1, "building": False, "error": ""})


if __name__ == "__main__":
    unittest.main()
