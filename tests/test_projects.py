"""Project discovery, optional metadata and shared Markdown rendering regressions."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from projects import MARKER, ProjectLibrary


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, path, text):
        target = self.base / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def metadata(self, **values):
        return self.write("files/research/Example/project.json", json.dumps(values))

    def load(self):
        library = ProjectLibrary(self.base)
        library.discover()
        library.parse()
        return library, library.projects[0]

    def render(self, page, html, description, title, *, output=None, extra_head=""):
        self.write(output or f"{page}/index.html", html)

    def test_optional_links_and_sections_are_omitted(self):
        self.metadata(title="Example", links={"Preprint": "", "DOI": None, "GitHub": "   "})
        library, project = self.load()
        html = library.page(project)
        self.assertIn("Example", html)
        for absent in ('class="project-links"', 'id="research-log"', 'id="research-notes"', 'class="project-cover"'):
            self.assertNotIn(absent, html)

    def test_links_cover_and_assets_are_explicit(self):
        self.metadata(cover="assets/cover.jpg", links={"Poster": "assets/poster.pdf", "Preprint": "https://arxiv.org/abs/example", "DOI": "https://doi.org/example", "GitHub": "https://github.com/example/project", "讨论 & PPT": "assets/slides.pdf", "Empty": ""})
        for name in ("cover.jpg", "poster.pdf", "slides.pdf", "raw.csv", "unused.md"):
            self.write("files/research/Example/assets/" + name, "fixture")
        library, project = self.load()
        html = library.page(project)
        for label in ("Preprint", "DOI", "GitHub", "Poster"):
            self.assertIn(label, html)
        self.assertLess(html.index('>Poster '), html.index('>Preprint '))
        self.assertIn('>讨论 &amp; PPT ', html)
        self.assertIn('../../files/research/Example/assets/poster.pdf', html)
        self.assertIn('../files/research/Example/assets/cover.jpg', library.directory())
        for name in ("raw.csv", "unused.md", "Empty"):
            self.assertNotIn(name, html)
        self.assertEqual(len(project.library.notes), 0)

    def test_notes_sort_by_timestamp_with_drafts_and_undated_last(self):
        self.metadata()
        for name, date in (("early", "2026-10-18 8:40"), ("late", "2026-10-18 18:30"), ("old", "2026-10-17")):
            self.write(f"files/research/Example/notes/{name}/main.md", f"---\ntitle: {name}\ndate: {date}\n---\nBody")
        self.write("files/research/Example/notes/draft.md", "---\ndraft: true\n---\nDraft")
        self.write("files/research/Example/notes/undated.md", "Undated")
        library, project = self.load()
        self.assertEqual([n.title for n in project.library.notes], ["late", "early", "old", "undated"])
        html = library.page(project)
        self.assertIn('datetime="2026-10-18T18:30:00"', html)
        self.assertLess(html.index('>late</h3>'), html.index('>early</h3>'))
        self.assertIn("未标注日期", html)

    def test_note_covers_and_fixed_category_in_list_and_article(self):
        self.metadata(title="Project title", cover="assets/project.jpg")
        self.write("files/research/Example/assets/project.jpg", "project image")
        self.write("files/research/Example/notes/Own/main.md", "---\ntitle: Own\ncategory: Other\ncover: own cover.jpg\n---\nBody")
        self.write("files/research/Example/notes/Own/own cover.jpg", "note image")
        self.write("files/research/Example/notes/Fallback/main.md", "# Fallback")
        self.write("files/research/Example/notes/Remote/main.md", "---\ntitle: Remote\ncover: https://example.com/cover.jpg\n---\nBody")
        library, project = self.load()
        page = library.page(project)
        self.assertEqual(page.count('class="project-note-cover"'), 3)
        self.assertIn('src="../../files/research/Example/notes/Own/own%20cover.jpg"', page)
        self.assertIn('src="https://example.com/cover.jpg"', page)
        for note in project.library.notes:
            self.assertEqual(note.category, "Research Notes")
            self.assertEqual(note.meta["category"], "Research Notes")
            article = project.library.article(note, directory_path=project.output, category_anchor="research-notes")
            self.assertIn('<p class="eyebrow">Research Notes</p>', article)
            self.assertIn('class="article-cover"', article)
        fallback = next(n for n in project.library.notes if n.title == "Fallback")
        self.assertEqual(fallback.cover, "../../../../files/research/Example/assets/project.jpg")

    def test_log_and_notes_share_markdown_links_images_and_math(self):
        self.metadata()
        self.write("files/notes/Physics/shared.md", "Shared")
        self.write("files/research/Example/log.md", "# 研究日志\n\n[Read](notes/a/main.md)\n\n![Cover](assets/cover.jpg)")
        self.write("files/research/Example/assets/cover.jpg", "fixture")
        self.write("files/research/Example/notes/a/main.md", "---\nsummary: Preview only\n---\n# A\n\n## Section\n\n[Next](../b.md)\n\n[Shared](../../../../../notes/Physics/shared.md)\n\n$x^2$\n\n| A | B |\n| - | - |\n| 1 | 2 |")
        # Relative path from files/research/Example/notes/a to files/notes.
        path = self.base / "files/research/Example/notes/a/main.md"
        path.write_text(path.read_text(encoding="utf-8").replace("../../../../../notes/", "../../../../notes/"), encoding="utf-8")
        self.write("files/research/Example/notes/b.md", "# B")
        library = ProjectLibrary(self.base)
        library.discover()
        for note in library.renderer.notes:
            library.renderer.parse(note)
        project = library.projects[0]
        note = next(n for n in project.library.notes if n.title == "A")
        self.assertIn('href="notes/a/index.html"', project.log.html)
        self.assertIn('src="../../files/research/Example/assets/cover.jpg"', project.log.html)
        self.assertIn('href="../b.html"', note.html)
        self.assertIn('note/Physics/shared.html', note.html)
        self.assertIn('class="note-table"', note.html)
        self.assertEqual(library.renderer.equations[0]["tex"], "x^2")
        article = project.library.article(note, directory_path=project.output, collection_label="Project", return_label="课题主页", category_anchor="research-notes")
        self.assertIn('../../index.html#research-notes', article)
        self.assertIn("返回课题主页", article)
        self.assertNotIn("Preview only", article)

    def test_compatible_source_roots_and_duplicate_names(self):
        self.write("files/projects/One/log.md", "One")
        self.write("files/research/Two/log.md", "Two")
        library = ProjectLibrary(self.base)
        self.assertEqual(len(library.discover()), 2)
        self.write("files/research/one/log.md", "Duplicate")
        with self.assertRaisesRegex(ValueError, "Duplicate project"):
            ProjectLibrary(self.base).discover()

    def test_generated_pages_cleanup_and_handwritten_preservation(self):
        self.metadata()
        note = self.write("files/research/Example/notes/a.md", "A")
        ProjectLibrary(self.base).build(self.render)
        generated = self.base / "research/Example/notes/a.html"
        self.assertTrue(generated.exists())
        manual = self.write("research/Example/manual.html", "Handwritten")
        note.unlink()
        ProjectLibrary(self.base).build(self.render)
        self.assertFalse(generated.exists())
        self.assertTrue(manual.exists())
        self.metadata(draft=True)
        ProjectLibrary(self.base).build(self.render)
        self.assertFalse((self.base / "research/Example/index.html").exists())
        self.assertTrue(manual.exists())

    def test_unsafe_links_and_missing_assets_fail(self):
        for value in ("javascript:alert(1)", "../../../../secret.txt", "assets/missing.pdf"):
            with self.subTest(value=value):
                self.metadata(links={"DOI": value})
                library, project = self.load()
                with self.assertRaises(ValueError):
                    library.page(project)

    def test_handwritten_project_page_is_not_overwritten(self):
        self.metadata()
        target = self.write("research/Example/index.html", "Handwritten")
        with self.assertRaisesRegex(ValueError, "handwritten"):
            ProjectLibrary(self.base).build(self.render)
        self.assertEqual(target.read_text(encoding="utf-8"), "Handwritten")


if __name__ == "__main__":
    unittest.main()
