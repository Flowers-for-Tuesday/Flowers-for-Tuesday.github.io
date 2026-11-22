"""Music notes by genre and original releases presented as albums."""
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

from dates import display_date
from notes import ARTICLE_HEAD, NOTE_HEAD, NoteLibrary, esc, relative_url

MUSIC_HEAD = '<link rel="stylesheet" href="{root}/assets/css/music.css">'


class MusicLibrary(NoteLibrary):
    def __init__(self, base, section):
        super().__init__(base)
        self.section = section
        self.root = self.base / "music" / section
        self.source_root = self.base / "files/music" / section
        config = self.base / "content/music-categories.json"
        self.categories = json.loads(config.read_text(encoding="utf-8")) if section == "notes" and config.exists() else {}

    def ordered_categories(self):
        return list(dict.fromkeys([*self.categories, *super().ordered_categories()]))

    def cover_url(self, note):
        parts = urlsplit(note.cover)
        return note.cover if parts.scheme else relative_url((note.output.parent / unquote(parts.path)).resolve(), self.root.parent)

    def card(self, note):
        card = super().card(note)
        card = card.replace(f'href="{relative_url(note.output, self.root)}"', f'href="{relative_url(note.output, self.root.parent)}"', 1)
        if note.cover:
            parts = urlsplit(note.cover)
            old = note.cover if parts.scheme else relative_url((note.output.parent / unquote(parts.path)).resolve(), self.root)
            card = card.replace(f'src="{esc(old)}"', f'src="{esc(self.cover_url(note))}"', 1)
        return card

    def album_card(self, note):
        cover = f'<img src="{esc(self.cover_url(note))}" alt="" loading="lazy" decoding="async">' if note.cover else '<span class="music-cover-placeholder" aria-hidden="true">♪</span>'
        date = f'<time datetime="{note.published}" lang="en">{display_date(note.published)}</time>' if note.published else '原创专辑'
        summary = f'<p class="music-album-summary">{esc(note.preview_summary)}</p>' if note.preview_summary else ''
        return f'''<article class="music-album"><a href="{relative_url(note.output, self.root.parent)}"><div class="music-album-cover">{cover}</div><div class="music-album-meta">{date}<span aria-hidden="true">↗</span></div><h3>{esc(note.title)}</h3>{summary}</a></article>'''


def build_music(base, render, site_name):
    base = Path(base)
    notes, albums = (MusicLibrary(base, section) for section in ("notes", "albums"))
    for library in (notes, albums):
        library.discover()
    paths = {**notes.paths, **albums.paths}
    for library in (notes, albums):
        library.paths.update(paths)
        for note in library.notes:
            library.parse(note)
        library.render_math()
        for note in library.notes:
            is_album = library.section == "albums"
            anchor = "albums" if is_album else f"category-{library.ordered_categories().index(note.category) + 1}"
            article = library.article(note, directory_path=base / "music/index.html", collection_label="Music",
                                      return_label="音乐目录", category_anchor=anchor,
                                      breadcrumb_label="原创作品" if is_album else None,
                                      labels={"body": "专辑介绍"} if is_album else None)
            if is_album:
                article = f'<div class="music-album-detail">{article}</div>'
            render("music", article, note.summary or note.title, note.title + " | " + site_name,
                   output=note.output.relative_to(base).as_posix(), extra_head=ARTICLE_HEAD + MUSIC_HEAD)
        library.root.mkdir(parents=True, exist_ok=True)
        library.remove_stale()
    # Reuse Note's directory, filters, search, cards and reading pages.
    directory = notes.directory().split('</header>', 1)[1]
    directory = directory.replace('<p class="eyebrow">按主题阅读</p>', '', 1)
    for index, category in enumerate(notes.ordered_categories(), 1):
        if not any(note.category == category for note in notes.notes):
            directory = directory.replace(f'id="category-{index}" data-note-group',
                                          f'id="category-{index}" data-note-group data-empty-category="{esc(category)}"', 1)
    directory = re.sub(r'(<div class="note-grid"[^>]*>)</div>', r'\1<p class="music-category-empty">该类别暂无笔记。</p></div>', directory)
    album_cards = ''.join(albums.album_card(note) for note in albums.notes)
    if not album_cards:
        album_cards = '<div class="music-albums-empty"><p>暂无原创专辑</p></div>'
    render("music", f'''<header class="page-heading"><p class="eyebrow" lang="ja">音楽</p><h1 lang="en">Music<span class="title-period">.</span></h1></header>
      <section id="music-notes" class="music-section" aria-labelledby="music-notes-heading"><header class="music-section-heading"><h2 id="music-notes-heading">笔记</h2><p>{len(notes.notes):02d} 篇</p></header>{directory}</section>
      <section id="albums" class="music-section" aria-labelledby="albums-heading"><header class="music-section-heading"><h2 id="albums-heading">原创作品</h2><p>{len(albums.notes):02d} 张专辑</p></header><div class="music-album-grid">{album_cards}</div></section>''',
      "音乐笔记与原创专辑。按 Classical、R&B 等类别阅读音乐笔记，聆听原创作品。", "Music | " + site_name,
      extra_head=NOTE_HEAD + MUSIC_HEAD + '\n<script src="{root}/assets/js/notes.js" defer></script>')
    return notes, albums
