"""Music navigation, categorized notes, album covers and source lifecycle."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build
from music import build_music


class MusicTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.write("content/music-categories.json", '{"Classical": {}, "R&B": {}}')

    def write(self, path, content):
        target = self.base / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def generate(self):
        with patch.object(build, "BASE", self.base):
            build_music(self.base, build.render, "Test site")
        return (self.base / "music/index.html").read_text(encoding="utf-8")

    def test_empty_sections_categories_and_drafts(self):
        self.write("files/music/notes/secret.md", "---\ndraft: true\n---\nSecret")
        html = self.generate()
        for text in ('lang="ja">音楽', 'id="music-notes"', 'id="albums"', 'id="category-1"', 'id="category-2"', 'data-empty-category="Classical"', 'R&amp;B', '暂无原创专辑', 'href="../music/" aria-current="page">Music'):
            self.assertIn(text, html)
        self.assertNotIn('Secret', html)
        self.assertFalse((self.base / "culture").exists())

    def test_category_cards_album_links_assets_and_cleanup(self):
        self.write("files/music/notes/Classical/harmony.md", '---\ntitle: Harmony\ncategory: Classical\n---\n## Chords\n\n[Album](../../albums/first/main.md)')
        self.write("files/music/notes/R&B/rhythm.md", '---\ntitle: Rhythm\ncategory: R&B\n---\nGroove')
        album = self.write("files/music/albums/first/main.md", '---\ntitle: A & B\ncategory: 原创作品\ncover: cover.svg\ndate: 2026-11-06\nsummary: My album\n---\n## Tracks\n\n[Track](track.mp3)')
        self.write("files/music/albums/first/cover.svg", '<svg xmlns="http://www.w3.org/2000/svg"/>')
        self.write("files/music/albums/first/track.mp3", 'fixture')
        html = self.generate()
        for text in ('data-category="Classical"', 'data-category="R&amp;B"', 'href="notes/Classical/harmony.html"', 'href="albums/first/index.html"', 'src="../files/music/albums/first/cover.svg"', 'A &amp; B', 'My album'):
            self.assertIn(text, html)
        article = (self.base / "music/notes/Classical/harmony.html").read_text(encoding="utf-8")
        self.assertIn('href="../../index.html#category-1"', article)
        self.assertIn('href="../../albums/first/index.html"', article)
        release = (self.base / "music/albums/first/index.html").read_text(encoding="utf-8")
        self.assertIn('href="../../index.html#albums"', release)
        self.assertIn('href="../../../files/music/albums/first/track.mp3"', release)
        album.write_text('---\ndraft: true\n---\nHidden', encoding="utf-8")
        # Remove the public cross-link before unpublishing its target.
        self.write("files/music/notes/Classical/harmony.md", '---\ncategory: Classical\n---\nHarmony')
        self.generate()
        self.assertFalse((self.base / "music/albums/first/index.html").exists())
        self.assertTrue((self.base / "files/music/albums/first/cover.svg").exists())


if __name__ == "__main__":
    unittest.main()
