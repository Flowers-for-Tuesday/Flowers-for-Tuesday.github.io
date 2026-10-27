"""Gallery content contracts, static generation and safe lifecycle behavior."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from gallery import GalleryLibrary, MARKER, build_gallery


class GalleryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, slug="example", **overrides):
        meta = dict(title="A lake", date="2026-01-02", place=dict(name="Beijing", country="CN", lat=40, lng=116))
        meta.update(overrides)
        folder = self.base / "files/gallery" / slug
        (folder / "images").mkdir(parents=True, exist_ok=True)
        for name in ("one.svg", "two.svg"):
            (folder / "images" / name).write_text('<svg xmlns="http://www.w3.org/2000/svg"/>', encoding="utf-8")
        path = folder / "main.md"
        path.write_text("---\n" + yaml.safe_dump(meta, allow_unicode=True) + "---\n## Afternoon\n\nA **quiet** walk.\n\n<script>alert(1)</script>", encoding="utf-8")
        return path

    def render(self, page, main, description, title, *, output=None, extra_head=""):
        path = self.base / (output or "gallery/index.html")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(main, encoding="utf-8")

    def load(self):
        library = GalleryLibrary(self.base)
        library.discover()
        return library

    def test_dates_sort_and_hidden_folders_are_excluded(self):
        self.write("old", date="2025-01-01")
        self.write("new", date="2026-09-01")
        self.write(".draft", place=None)
        library = self.load()
        self.assertEqual([j.slug for j in library.journals], ["new", "old"])
        self.assertEqual(len(library.notes), 2)
        html = library.directory()
        self.assertLess(html.index('data-journal="new"'), html.index('data-journal="old"'))

    def test_invalid_metadata_fails_with_source(self):
        for values in (
            {"place": dict(name="x", country="CN", lat=91, lng=1)},
            {"place": dict(name="x", country="CN", lat=1, lng=float("nan"))},
            {"place": dict(name="x", country="CN", lat=True, lng=1)},
            {"date": "2026-02-30"}, {"date": "2026-1-1"}, {"images": []}, {"tags": "walk"}
        ):
            with self.subTest(values=values):
                self.write(**values)
                with self.assertRaisesRegex(ValueError, "files[/\\\\]gallery"):
                    self.load()

    def test_missing_asset_and_path_escape_are_rejected(self):
        for src in ("missing.jpg", "../../../../outside.jpg", "javascript:alert(1)"):
            with self.subTest(src=src):
                source = self.write()
                with source.open('a', encoding='utf-8') as stream:
                    stream.write(f'\n\n[Photo]({src})')
                if src.startswith('javascript:'):
                    # CommonMark renders executable link text literally instead of creating a link.
                    self.assertNotIn('href="javascript:', self.load().journals[0].note.html)
                    continue
                with self.assertRaises(ValueError):
                    self.load()

    def test_cover_and_photo_paths_work_at_both_page_depths(self):
        self.write()
        library = self.load()
        journal = library.journals[0]
        self.assertTrue(journal.images[0]["src"].endswith("one.svg"))
        self.assertIn('../files/gallery/example/images/one.svg', library.card(journal))
        entry = library.entry(journal)
        self.assertIn('../../files/gallery/example/images/two.svg', entry)
        self.assertIn('<strong>quiet</strong>', entry)
        self.assertNotIn('<script>alert(1)</script>', entry)

    def test_images_use_natural_filename_order_and_ignore_other_files(self):
        source = self.write()
        folder = source.parent / 'images'
        for name in ('10.PNG', '2.jpg', '1.webp', '.hidden.jpg', 'readme.txt'):
            (folder / name).write_text('fixture', encoding='utf-8')
        names = [photo['src'].split('/')[-1] for photo in self.load().journals[0].images]
        self.assertEqual(names, ['1.webp', '2.jpg', '10.PNG', 'one.svg', 'two.svg'])

    def test_adjacent_images_are_used_only_when_images_folder_is_absent(self):
        source = self.write()
        folder = source.parent / 'images'
        for image in folder.iterdir():
            image.rename(source.parent / image.name)
        with self.assertRaisesRegex(ValueError, 'at least one image'):
            self.load()
        folder.rmdir()
        self.assertEqual(len(self.load().journals[0].images), 2)

    def test_countries_are_derived_from_notes(self):
        self.write('china')
        self.write('japan', place=dict(name='Kyoto', country='JP', lat=35, lng=135))
        html = self.load().directory()
        self.assertIn('data-scope="all" aria-pressed="true">全部', html)
        self.assertEqual(html.count('data-scope="CN"'), 1)
        self.assertEqual(html.count('data-scope="JP"'), 1)
        self.assertNotIn('data-scope="overseas"', html)
        self.assertLess(html.index('id="footprints"'), html.index('class="gallery-filters"'))

    def test_uppercase_folder_preserves_page_and_image_paths(self):
        self.write('Orion', title='Orion')
        build_gallery(self.base, self.render)
        self.assertTrue((self.base / 'gallery/Orion/index.html').is_file())
        directory = (self.base / 'gallery/index.html').read_text(encoding='utf-8')
        article = (self.base / 'gallery/Orion/index.html').read_text(encoding='utf-8')
        self.assertIn('href="Orion/index.html"', directory)
        self.assertIn('../files/gallery/Orion/images/one.svg', directory)
        self.assertIn('../../files/gallery/Orion/images/one.svg', article)

    def test_metadata_is_escaped_in_html_and_embedded_json(self):
        title = '</script><script>alert(1)</script>'
        self.write(title=title)
        html = self.load().directory()
        self.assertNotIn(title, html)
        payload = html.split('id="gallery-data">')[1].split('</script>')[0]
        self.assertEqual(json.loads(payload)[0]["title"], title)

    def test_build_and_removal_only_clean_generated_reading_pages(self):
        source = self.write()
        build_gallery(self.base, self.render)
        generated = self.base / "gallery/example/index.html"
        self.assertIn(MARKER, generated.read_text(encoding="utf-8"))
        custom = self.base / "gallery/custom/index.html"
        custom.parent.mkdir()
        custom.write_text("handwritten", encoding="utf-8")
        source.unlink()
        build_gallery(self.base, self.render)
        self.assertFalse(generated.exists())
        self.assertEqual(custom.read_text(), "handwritten")
        self.assertIn('暂无符合条件的笔记', (self.base / 'gallery/index.html').read_text(encoding='utf-8'))

    def test_handwritten_page_collision_is_rejected(self):
        self.write()
        target = self.base / "gallery/example/index.html"
        target.parent.mkdir(parents=True)
        target.write_text("handwritten", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "handwritten"):
            build_gallery(self.base, self.render)
        self.assertEqual(target.read_text(), "handwritten")


if __name__ == "__main__":
    unittest.main()
