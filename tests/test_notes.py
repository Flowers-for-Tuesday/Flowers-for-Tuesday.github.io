"""Regression coverage for Markdown discovery and rendering, without network access."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from notes import MARKER, NoteLibrary, date_value, split_frontmatter


class NoteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        (self.base / "note").mkdir()
        (self.base / "files/notes").mkdir(parents=True)
        self.library = NoteLibrary(self.base)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, content):
        path = self.base / "files/notes" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_discovery_metadata_sorting_and_drafts(self):
        self.write("计算物理/旧笔记/main.md", "---\ntitle: 较早的笔记\ndate: 2026-07-14 18:30\n---\n正文")
        self.write("计算物理/新笔记/main.md", "---\ntitle: 较新的笔记\ndate: 2026-08-03 8:40\n---\n正文")
        self.write("草稿.md", "---\ndraft: true\n---\n草稿")
        notes = self.library.discover()
        self.assertEqual([n.title for n in notes], ["较新的笔记", "较早的笔记"])
        self.assertEqual(notes[0].category, "计算物理")
        self.assertEqual(notes[0].output.name, "index.html")

    def test_markdown_blocks_links_and_math_are_not_mixed(self):
        self.write("Physics/A/main.md", '''---
title: A
---
# A
## 相同标题
## 相同标题

文字 $x_1$，以及 $$y^2$$。

```python
price = "$not_math$"
```

`$also_not_math$`

| A | B |
| - | - |
| 1 | 2 |

- [x] 已完成

脚注[^one]

[^one]: 一条脚注。

![图片说明](<图 1.png>)

[其他笔记](../B/main.md#章节)

<script>alert(1)</script>
''')
        self.write("Physics/A/图 1.png", "fixture")
        self.write("Physics/B/main.md", "## 章节\n正文")
        self.library.discover()
        note = next(n for n in self.library.notes if n.title == "A")
        self.library.parse(note)
        self.assertEqual([q["tex"] for q in self.library.equations], ["x_1", "y^2"])
        self.assertIn('id="相同标题-2"', note.html)
        self.assertNotIn("<h1", note.html)
        self.assertIn("<table", note.html)
        self.assertIn("footnote", note.html)
        self.assertIn('type="checkbox"', note.html)
        self.assertIn("%E5%9B%BE%201.png", note.html)
        self.assertIn("../B/index.html#", note.html)
        self.assertIn('alt="图片说明"', note.html)
        self.assertNotIn("<script>", note.html)
        self.assertIn("&lt;script&gt;", note.html)

    def test_unsafe_or_missing_local_assets_fail_clearly(self):
        self.write("one.md", "![missing](missing.png)")
        note = self.library.discover()[0]
        with self.assertRaisesRegex(ValueError, "Missing local asset"):
            self.library.parse(note)
        with self.assertRaisesRegex(ValueError, "outside the site"):
            self.library.resolve_link("../../../../secret.txt", note)

    def test_generated_output_collision_does_not_overwrite(self):
        self.write("topic/a/main.md", "A")
        self.write("topic/a/index.md", "B")
        with self.assertRaisesRegex(ValueError, "same page"):
            self.library.discover()

    def test_no_metadata_uses_heading_and_default_category(self):
        self.write("plain.md", "# My title\n\nA paragraph.")
        note = self.library.discover()[0]
        self.assertEqual(note.title, "My title")
        self.assertEqual(note.category, "未分类")
        self.assertEqual(note.published, "")

    def test_summary_skips_bibliography_and_uses_body(self):
        text = "这是一段介绍笔记主题的正文，用于让读者在进入文章之前了解笔记讨论的内容和研究方法。"
        self.write("summary.md", "[1] A long bibliography entry, Computational Physics, textbook edition.\n\n" + text)
        note = self.library.discover()[0]
        self.library.parse(note)
        self.assertEqual(note.summary, text)

    def test_cleanup_only_removes_previous_generated_pages(self):
        generated = self.base / "note/old.html"
        generated.write_text(MARKER + "old", encoding="utf-8")
        handwritten = self.base / "note/manual.html"
        handwritten.write_text("handwritten", encoding="utf-8")
        source_asset = self.write("old.html", "source attachment")
        manifest = self.base / "note/.generated-pages.json"
        manifest.write_text(json.dumps(["old.html", "manual.html"]), encoding="utf-8")
        self.library.remove_stale()
        self.assertFalse(generated.exists())
        self.assertTrue(handwritten.exists())
        self.assertTrue(source_asset.exists())

    def test_separate_source_assets_and_stable_reading_urls(self):
        source = self.write("Physics/A/main.md", "---\ntitle: A\ncover: cover.png\n---\n![Figure](figure.png)\n\n[Next](../B/main.md#section)")
        self.write("Physics/A/cover.png", "cover fixture")
        self.write("Physics/A/figure.png", "figure fixture")
        self.write("Physics/B/main.md", "# B\n\n## Section")
        self.library.discover()
        note = next(n for n in self.library.notes if n.title == "A")
        self.library.parse(note)
        self.assertEqual(note.source, source)
        self.assertEqual(note.output, self.base / "note/Physics/A/index.html")
        self.assertEqual(note.cover, "../../../files/notes/Physics/A/cover.png")
        self.assertIn('src="../../../files/notes/Physics/A/figure.png"', note.html)
        self.assertIn('href="../B/index.html#section"', note.html)
        self.assertIn('src="../files/notes/Physics/A/cover.png"', self.library.card(note))
        self.assertIn('href="../../../files/notes/Physics/A/main.md" download', self.library.article(note))

    def test_root_note_names_do_not_replace_directory(self):
        for name in ("index.md", "main.md", "plain.md"):
            self.write(name, name)
        outputs = {note.output.relative_to(self.base).as_posix() for note in self.library.discover()}
        self.assertEqual(outputs, {"note/index-note.html", "note/main.html", "note/plain.html"})

    def test_source_discovery_ignores_output_directory(self):
        self.write("new.md", "New source")
        (self.base / "note/old.md").write_text("Old location", encoding="utf-8")
        notes = self.library.discover()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].source.name, "new.md")

    def test_frontmatter_errors_and_dates(self):
        self.assertEqual(date_value("2026-08-03 8:40"), "2026-08-03")
        with self.assertRaises(ValueError):
            split_frontmatter("---\ntitle: Missing terminator")
        with self.assertRaises(ValueError):
            date_value("yesterday")


if __name__ == "__main__":
    unittest.main()
