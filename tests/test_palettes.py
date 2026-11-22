"""Reference palette integrity and readable light/dark website colors."""
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from palettes import contrast, load_palettes, theme_tokens

BASE = Path(__file__).resolve().parents[1]


class PaletteTests(unittest.TestCase):
    def test_imported_four_color_palettes_and_samples(self):
        palettes = load_palettes(BASE)
        source = json.loads((BASE / 'assets/color/color-palettes.json').read_text(encoding='utf-8-sig'))
        self.assertEqual(len(palettes), 377)
        self.assertEqual(len(palettes), len(source))
        self.assertEqual([p['number'] for p in palettes], list(range(1, 378)))
        for palette, original in zip(palettes, source):
            self.assertEqual(set(original), {'id', 'title', 'colors', 'image'})
            self.assertEqual(palette['title'], original['title'])
            self.assertEqual(palette['number'], original['id'])
            self.assertEqual([c['hex'] for c in palette['colors']], [c['hex'].upper() for c in original['colors']])
            self.assertEqual([c['name'] for c in palette['colors']], [c['name'] for c in original['colors']])
            self.assertEqual(palette['image'], original['image'])
            self.assertTrue((BASE / 'assets/color' / palette['image']).is_file())
            self.assertEqual(palette['id'], f'palette-{palette["number"]:04d}')
            self.assertTrue(palette['title'])
            self.assertEqual(len(palette['colors']), 4)

    def test_text_contrast_in_all_modes(self):
        for palette in load_palettes(BASE):
            for dark in (False, True):
                with self.subTest(palette=palette['id'], dark=dark):
                    tokens = theme_tokens(palette, dark)
                    for background in ('paper', 'surface', 'surface-active', 'surface-hover', 'code-surface'):
                        for foreground in ('ink', 'muted', 'accent'):
                            self.assertGreaterEqual(contrast(tokens[foreground], tokens[background]), 4.5,
                                                    f'{foreground} on {background}')
                    self.assertGreaterEqual(contrast(tokens['quote-ink'], tokens['quote-surface']), 4.5)
                    self.assertGreaterEqual(contrast(tokens['field-line'], tokens['surface']), 3)

    def test_catalog_and_styles_match_the_source(self):
        text = (BASE / 'assets/js/palettes.js').read_text(encoding='utf-8')
        catalog = json.loads(text.split('window.SITE_PALETTES = ', 1)[1].rstrip(';\n'))
        css = (BASE / 'assets/css/palettes.css').read_text(encoding='utf-8')
        self.assertNotIn('original', [p['id'] for p in catalog])
        self.assertEqual(len(catalog), 377)
        self.assertEqual([p['index'] for p in catalog], list(range(1, 378)))
        self.assertEqual(catalog[0]['id'], 'palette-0001')
        self.assertIn('window.SITE_DEFAULT_PALETTE = "palette-0001";', text)
        self.assertIn('@media screen {', css)
        for source, entry in zip(load_palettes(BASE), catalog):
            self.assertEqual(entry['id'], source['id'])
            self.assertEqual(entry['number'], source['number'])
            self.assertEqual(entry['title'], source['title'])
            self.assertEqual(entry['colors'], [c['hex'] for c in source['colors']])
            self.assertEqual(entry['color_names'], [c['name'] for c in source['colors']])
            self.assertEqual(entry['image'], source['image'])
            for mode in ('light', 'dark'):
                tokens = theme_tokens(source, mode == 'dark')
                self.assertEqual(entry['paper'][mode], tokens['paper'])
                self.assertIn(f'[data-palette="{source["id"]}"][data-theme="{mode}"]', css)
                self.assertIn(f'--accent: {tokens["accent"]};', css)


if __name__ == '__main__':
    unittest.main()
