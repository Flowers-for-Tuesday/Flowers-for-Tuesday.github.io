"""Publication date sorting, readable citations and safe DOI navigation."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from references import read_references
from projects import ProjectLibrary
from notes import Note, NoteLibrary


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.path = self.base / "files/research/Test/assets/references.bib"
        self.path.parent.mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, text):
        self.path.write_text(text, encoding="utf-8")
        return read_references(self.path)

    def test_newest_year_first(self):
        refs = self.write('''
        @article{first, title={First}, author={Zulu, A}, year=1990}
        @article{second, title={Second}, author={Alpha, B}, year=2026}
        @article{third, title={Third}, year=2004}
        ''')
        self.assertEqual([ref.key for ref in refs], ["second", "third", "first"])
        self.assertIn('[1]', refs[0].html(1))

    def test_month_day_precision_stable_ties_and_undated_last(self):
        refs = self.write('''
        @article{unknown,title={Unknown},urldate={2099-12-31}}
        @article{yearonly,title={Year},year=2026}
        @article{feb,title={February},year=2026,month=feb}
        @article{march,title={March},year=2026,month={March}}
        @article{firsttie,title={First},date={2026-03-10}}
        @article{secondtie,title={Second},year=2026,month=3,day=10}
        @article{latest,title={Latest},date={2026-03-11},year=2025}
        ''')
        self.assertEqual([ref.key for ref in refs], ['latest', 'firsttie', 'secondtie', 'march', 'feb', 'yearonly', 'unknown'])
        self.assertIn('(2026)', refs[0].citation)

    def test_nested_braces_accents_names_macros_and_page_ranges(self):
        refs = self.write(r'''
        @string{prb = "Physical Review B"}
        @article{paper,
          title = {A {Hubbard} model: \$ {\textbackslash}mathrm\{{SU}\}(n)\$},
          author = {Sch{\"o}nhammer, K. and de la Cruz, Jr., Juan and {Research and Development Team}},
          journal = prb, volume = {52}, number = {4}, pages = {2504--2510},
          month = jul, year = {1995}, doi = {https://doi.org/10.1103/PhysRevB.52.2504},
          file = {Local PDF:C:\\Users\\private.pdf:application/pdf}
        }
        ''')
        ref = refs[0]
        self.assertIn("Schönhammer", ref.citation)
        self.assertIn("Juan de la Cruz, Jr.", ref.citation)
        self.assertIn("Research and Development Team", ref.citation)
        self.assertIn("SU(n)", ref.citation)
        self.assertNotIn("\\mathrm", ref.citation)
        self.assertIn("2504–2510", ref.citation)
        self.assertIn("<cite>Physical Review B</cite>", ref.citation)
        self.assertEqual(ref.url, "https://doi.org/10.1103/PhysRevB.52.2504")
        self.assertNotIn("private.pdf", ref.html(1))

    def test_doi_preferred_over_url_and_encoded(self):
        refs = self.write('@article{x,title={X},doi={doi:10.1234/a?b#c},url={https://example.com/other}}')
        self.assertEqual(refs[0].url, 'https://doi.org/10.1234/a%3Fb%23c')
        self.assertIn('DOI: 10.1234/', refs[0].html(1))

    def test_missing_fields_url_fallback_and_html_escaping(self):
        refs = self.write('''
        @misc{x,title={<script>alert(1)</script>},url={https://example.com/paper?a=1&b=2}}
        @book{y,title={Book},publisher={Publisher},date={2025-01-01}}
        ''')
        refs = {ref.key: ref for ref in refs}
        html = refs['x'].html(2)
        self.assertNotIn('<script>', html)
        self.assertIn('&lt;script&gt;', html)
        self.assertIn('&amp;b=2', html)
        self.assertIn('n.d.', html)
        self.assertIn('Publisher (2025)', refs['y'].citation)
        self.assertEqual(refs['y'].url, '')

    def test_missing_and_empty_bibliography(self):
        self.assertEqual(read_references(self.path), [])
        self.assertEqual(self.write('% No references yet\n'), [])

    def test_invalid_input_has_source_path(self):
        for text in ('@article{broken,title={Unclosed}',
                     '@article{x,title={X},doi={javascript:bad}}',
                     '@article{x,title={X},url={file:///secret.pdf}}'):
            with self.subTest(text=text):
                with self.assertRaisesRegex(ValueError, 'references.bib'):
                    self.write(text)

    def test_section_and_index_are_last_and_ignore_pdf_files(self):
        self.write('@article{first,title={Paper},year=2025,doi={10.1234/paper}}')
        source = self.path.parent.parent
        (source / 'log.md').write_text('Research log', encoding='utf-8')
        (source / 'notes').mkdir()
        (source / 'notes/one.md').write_text('# One', encoding='utf-8')
        (source / 'assets/unrelated.pdf').write_bytes(b'Not a PDF')
        library = ProjectLibrary(self.base)
        project = library.discover()[0]
        library.parse()
        html = library.page(project)
        self.assertLess(html.index('href="#research-log"'), html.index('href="#research-notes"'))
        self.assertLess(html.index('href="#research-notes"'), html.index('href="#research-references"'))
        self.assertLess(html.index('id="research-notes"'), html.index('id="research-references"'))
        self.assertIn('href="https://doi.org/10.1234/paper"', html)
        self.assertNotIn('unrelated.pdf', html)

    def citation_project(self, body):
        self.write('''@article{older,title={Older},year=2020}
                      @article{newer,title={Newer},year=2026}''')
        source = self.path.parent.parent
        (source / 'log.md').write_text(body, encoding='utf-8')
        folder = source / 'notes/Nested Note'
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'main.md').write_text(body, encoding='utf-8')
        library = ProjectLibrary(self.base)
        project = library.discover()[0]
        library.parse()
        return library, project

    def test_citations_link_to_sorted_entries_from_logs_and_nested_notes(self):
        library, project = self.citation_project('See [@older] and [@newer; @older].')
        html = project.log.html
        self.assertIn('href="#reference-older"', html)
        self.assertIn('>[2]</a>', html)
        self.assertIn('>[1]</a>', html)
        self.assertEqual(html.count('class="research-citation"'), 3)
        note = project.library.notes[0]
        self.assertIn('href="#reference-older"', note.html)
        article = project.library.article(note)
        self.assertIn('id="reference-older" tabindex="-1"', article)
        self.assertIn('href="#note-references">参考文献', article)
        self.assertLess(article.index('</article>'), article.index('class="note-references"'))
        self.assertIn('id="reference-older" tabindex="-1"', library.page(project))
        # The identity survives a change in publication order.
        self.path.write_text('@article{older,title={Older},year=2027}\n'
                             '@article{newer,title={Newer},year=2026}', encoding='utf-8')
        updated = ProjectLibrary(self.base)
        changed = updated.discover()[0]
        updated.parse()
        self.assertIn('href="#reference-older"', changed.log.html)
        self.assertIn('>[1]</a>', changed.log.html)

    def test_citations_preserve_code_math_escapes_links_and_plain_numbers(self):
        body = r'''`[@missing]`

```text
[@missing]
```

$[@missing]$

\[@missing] [1] [label [@missing]](https://example.com) [@missing](https://example.com)

**See [@older]**

| Citation |
| --- |
| [@newer] |
'''
        # Avoid invoking KaTeX; inline parsing is sufficient for these assertions.
        from unittest.mock import patch
        with patch.object(NoteLibrary, 'render_math'):
            _, project = self.citation_project(body)
        self.assertEqual(project.log.html.count('class="research-citation"'), 2)
        self.assertIn('<code>[@missing]</code>', project.log.html)
        self.assertIn('[@missing] [1]', project.log.html)
        self.assertIn('href="https://example.com"', project.log.html)

    def test_unknown_citation_reports_key_and_source(self):
        with self.assertRaisesRegex(ValueError, r"missing.*log\.md"):
            self.citation_project('See [@missing].')

    def test_regular_notes_do_not_interpret_citations(self):
        note = Note(self.base / 'regular.md', self.base / 'index.html', {},
                    'See [@missing].', 'Test', 'Test', '')
        NoteLibrary(self.base).parse(note)
        self.assertIn('[@missing]', note.html)

    def test_regular_note_local_bibliography_and_bottom_section(self):
        folder = self.base / 'files/notes/Physics/One'
        folder.mkdir(parents=True)
        (folder / 'main.md').write_text('## note-references\nSee [@older; @newer].', encoding='utf-8')
        (folder / 'references.bib').write_text(
            '@article{older,title={Older},year=2000}\n'
            '@article{newer,title={Newer},year=2026,doi={10.1234/newer}}', encoding='utf-8')
        (folder.parent / 'two.md').write_text('Another note', encoding='utf-8')
        library = NoteLibrary(self.base)
        library.discover()
        note = next(n for n in library.notes if n.source.parent == folder)
        library.parse(note)
        self.assertEqual([ref.key for ref in note.references], ['newer', 'older'])
        self.assertIn('<sup class="research-citations">', note.html)
        self.assertIn('href="#reference-older"', note.html)
        self.assertIn('>[2]</a>', note.html)
        html = library.article(note)
        self.assertIn('href="#note-references-bibliography">参考文献', html)
        self.assertIn('id="note-references-bibliography"', html)
        self.assertIn('href="https://doi.org/10.1234/newer"', html)
        self.assertLess(html.index('</article>'), html.index('class="note-references"'))
        self.assertLess(html.index('class="note-references"'), html.index('class="related-notes"'))
        other = next(n for n in library.notes if n is not note)
        library.parse(other)
        self.assertEqual(other.references, [])
        self.assertNotIn('class="note-references"', library.article(other))

    def test_regular_note_missing_key_reports_local_source(self):
        folder = self.base / 'files/notes/One'
        folder.mkdir(parents=True)
        (folder / 'main.md').write_text('See [@missing].', encoding='utf-8')
        (folder / 'references.bib').write_text('% Empty library', encoding='utf-8')
        library = NoteLibrary(self.base)
        note = library.discover()[0]
        with self.assertRaisesRegex(ValueError, r"missing.*main\.md"):
            library.parse(note)

    def test_project_notes_keep_project_bibliography(self):
        _, project = self.citation_project('See [@older].')
        source = project.library.notes[0].source
        source.with_name('references.bib').write_text('@article{local,title={Local}}', encoding='utf-8')
        source.with_name('second.md').write_text('See [@newer].', encoding='utf-8')
        library = ProjectLibrary(self.base)
        project = library.discover()[0]
        library.parse()
        self.assertEqual(len(project.library.notes), 2)
        for note in project.library.notes:
            self.assertIs(note.references, project.references)
            article = project.library.article(note)
            self.assertIn('id="reference-older"', article)
            self.assertIn('id="reference-newer"', article)
            self.assertNotIn('id="reference-local"', article)
            self.assertNotIn('index.html#reference-', note.html)
        note = next(n for n in project.library.notes if n.source == source)
        self.assertIn('href="#reference-older"', note.html)

    def test_citation_anchor_escapes_special_characters(self):
        from references import Reference, citation_plugin
        from markdown_it import MarkdownIt
        ref = Reference('paper:中文&"', 'Title')
        html = MarkdownIt().use(citation_plugin, [ref], '', 'log.md').render('[@paper:中文&"]')
        self.assertIn('href="#reference-paper%3A%E4%B8%AD%E6%96%87%26%22"', html)
        self.assertIn('id="reference-paper:中文&amp;&quot;"', ref.html(1))


if __name__ == '__main__':
    unittest.main()
