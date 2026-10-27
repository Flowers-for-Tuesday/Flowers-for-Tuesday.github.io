"""About Markdown discovery, metadata and page integration."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from about import load_about_entries
import build
from dev import source_snapshot


class AboutTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        (self.base / "files/about").mkdir(parents=True)

    def write(self, name, period="晨", order=1, body="正文。"):
        path = self.base / "files/about" / name
        path.write_text(f'---\norder: {order}\nsubtitle:\n  date: "2026/10/24"\n  period: "{period}"\n  location: "于北京"\n---\n\n{body}\n', encoding="utf-8")
        return path

    def test_order_and_theme_mapping(self):
        self.write("b.md", "夜", 2)
        self.write("a.md", "午", 1)
        self.write("c.md", "晨", 2)
        self.write("d.md", "", 3)
        entries = load_about_entries(self.base)
        self.assertEqual([e["source"].name for e in entries], ["a.md", "b.md", "c.md", "d.md"])
        self.assertEqual([e["theme"] for e in entries], ["light", "dark", "light", "all"])
        self.assertEqual(entries[0]["subtitle"], "2026/10/24，午，于北京")

    def test_markdown_body(self):
        self.write("a.md", body="第一段。\n\n**强调**与[链接](https://example.com)。\n\n- 列表\n\n<script>bad()</script>")
        html = load_about_entries(self.base)[0]["html"]
        self.assertIn("<p>第一段。</p>", html)
        self.assertIn("<strong>强调</strong>", html)
        self.assertIn('<a href="https://example.com">链接</a>', html)
        self.assertIn("<li>列表</li>", html)
        self.assertNotIn("<script>", html)

    def test_invalid_metadata_reports_file(self):
        path = self.write("invalid.md", order="wrong")
        with self.assertRaisesRegex(ValueError, "invalid.md.*order"):
            load_about_entries(self.base)
        path.write_text("---\nsubtitle: text\n---\n正文", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "invalid.md.*subtitle"):
            load_about_entries(self.base)

    def test_page_reads_files_and_preview_watches_changes(self):
        path = self.write("entry.md", "夜", body="**来自 Markdown**")
        before = source_snapshot(self.base)
        self.assertIn("files/about/entry.md", before)
        with patch.object(build, "BASE", self.base), patch.object(build, "render") as render:
            build.about()
        main = render.call_args.args[1]
        self.assertIn('data-entry-theme="dark"', main)
        self.assertIn("2026/10/24，夜，于北京", main)
        self.assertIn("<strong>来自 Markdown</strong>", main)
        path.unlink()
        self.assertNotEqual(before, source_snapshot(self.base))
        self.assertEqual(load_about_entries(self.base), [])


if __name__ == "__main__":
    unittest.main()
