"""Render local BibTeX references newest first, without PDF or network access."""
from dataclasses import dataclass
from datetime import date
from html import escape
from pathlib import Path
import re
from urllib.parse import quote, unquote, urlsplit

from pybtex.database import parse_file
from pybtex.richtext import Text


def plain(value):
    """Decode BibTeX braces/accents and common text-only math in paper titles."""
    value = str(value or "")
    # Zotero can export literal math as escaped dollars, braces and backslashes.
    value = re.sub(r"\{?\\textbackslash\}?", lambda _: "\\", value)
    value = value.replace(r"\{", "{").replace(r"\}", "}")
    value = re.sub(r"\\(?:mathrm|mathbf|mathit|textrm|text)\s*\{([^{}]*)\}", r"\1", value)
    value = value.replace(r"\$", "$")
    value = re.sub(r"\$([^$]+)\$", r"\1", value)
    text = Text.from_latex(value).render_as("text")
    text = re.sub(r"\\(?:mathrm|mathbf|mathit|textrm|text)\b\s*", "", text)
    return " ".join(text.split())


def author_name(person):
    names = person.first_names + person.middle_names + person.prelast_names + person.last_names
    name = plain(" ".join(names))
    if person.lineage_names:
        name += ", " + plain(" ".join(person.lineage_names))
    return name


def doi_link(value):
    value = plain(value).strip()
    value = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", value, flags=re.I)
    value = unquote(value)
    if not re.fullmatch(r"10\.\d{4,9}/[^\s<>]+", value):
        raise ValueError(f"Invalid DOI: {value!r}")
    return value, "https://doi.org/" + quote(value, safe="/().;:-_")


def publication_date(fields):
    """Prefer ISO publication dates, then BibTeX year/month/day; never urldate."""
    match = re.fullmatch(r"(\d{4})(?:-(\d{1,2})(?:-(\d{1,2}))?)?", plain(fields.get("date")))
    if match:
        year, month, day = (int(part or 0) for part in match.groups())
        date(year, month or 1, day or 1)
        return year, month, day
    year_text = plain(fields.get("year"))
    if not re.fullmatch(r"\d{4}", year_text):
        return 0, 0, 0
    year = int(year_text)
    month_text = plain(fields.get("month")).lower().strip(".")
    months = {name: index for index, name in enumerate(
        ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"), 1)}
    month = int(month_text) if month_text.isdigit() else months.get(month_text[:3], 0)
    day_text = plain(fields.get("day"))
    day = int(day_text) if month and day_text.isdigit() else 0
    date(year, month or 1, day or 1)
    return year, month, day


@dataclass
class Reference:
    key: str
    citation: str
    link_label: str = ""
    url: str = ""

    @property
    def anchor(self):
        return "reference-" + self.key

    def html(self, index):
        link = f'<a class="reference-link" href="{escape(self.url, quote=True)}">{escape(self.link_label)} <span aria-hidden="true">↗</span></a>' if self.url else ""
        return f'<li class="reference-item" id="{escape(self.anchor, quote=True)}" tabindex="-1" data-reference-key="{escape(self.key, quote=True)}"><span class="reference-number" aria-hidden="true">[{index}]</span><div class="reference-copy"><p>{self.citation}</p>{link}</div></li>'


def citation_plugin(md, references, target, source):
    """Resolve [@key; @another] against a note or project's bibliography."""
    entries = {ref.key: (index, ref) for index, ref in enumerate(references, 1)}
    pattern = re.compile(r"\[@([^\s\[\];]+)(?:\s*;\s*@[^\s\[\];]+)*\]")

    def citation(state, silent):
        # Label lookahead must see ordinary brackets, otherwise Markdown treats
        # the citation as a nested link and rejects the enclosing real link.
        if silent or state.linkLevel or not state.src.startswith("[@", state.pos):
            return False
        match = pattern.match(state.src, state.pos, state.posMax)
        if not match:
            return False
        if not silent:
            keys = [part.strip()[1:] for part in match.group()[1:-1].split(";")]
            state.push("citation_group_open", "sup", 1).attrSet("class", "research-citations")
            for position, key in enumerate(keys):
                if key not in entries:
                    raise ValueError(f"Unknown citation key {key!r} in {source}; check the associated references.bib")
                index, ref = entries[key]
                if position:
                    state.push("text", "", 0).content = ", "
                # Dedicated token names bypass resolution of source Markdown paths.
                token = state.push("citation_open", "a", 1)
                token.attrs = {"href": target + "#" + quote(ref.anchor, safe=""),
                               "class": "research-citation", "role": "doc-biblioref",
                               "title": key, "aria-label": f"参考文献 [{index}]：{key}"}
                state.push("text", "", 0).content = f"[{index}]"
                state.push("citation_close", "a", -1)
            state.push("citation_group_close", "sup", -1)
        state.pos = match.end()
        return True

    # Ordinary Markdown links take priority; code and math use their own rules.
    md.inline.ruler.after("link", "research_citation", citation)


def read_references(path):
    path = Path(path)
    if not path.exists():
        return []
    try:
        bibliography = parse_file(str(path), bib_format="bibtex", encoding="utf-8-sig")
        references = []
        # Stable sorting retains BibTeX order for entries with identical dates.
        entries = sorted(bibliography.entries.items(), key=lambda item: publication_date(item[1].fields), reverse=True)
        for key, entry in entries:
            fields = entry.fields
            authors = [author_name(person) for person in entry.persons.get("author", [])]
            if not authors:
                authors = [author_name(person) for person in entry.persons.get("editor", [])]
                if authors:
                    authors[-1] += " (ed.)"
            names = (", ".join(authors[:-1]) + ", and " + authors[-1]) if len(authors) > 2 else " and ".join(authors)
            parts = []
            if names:
                parts.append(escape(names.rstrip(".")) + ".")
            title = plain(fields.get("title", "未注明题名"))
            parts.append(f'<span class="reference-title">{escape(title.rstrip("."))}.</span>')
            journal = plain(fields.get("journal") or fields.get("journaltitle") or fields.get("booktitle"))
            publication = f'<cite>{escape(journal)}</cite>' if journal else ""
            volume = plain(fields.get("volume"))
            number = plain(fields.get("number") or fields.get("issue"))
            pages = plain(fields.get("pages") or fields.get("eid")).replace("--", "–")
            if volume:
                publication += (" " if publication else "") + f'<strong>{escape(volume)}</strong>'
            if number:
                publication += f'({escape(number)})'
            if pages:
                publication += (", " if publication else "") + escape(pages)
            if not journal:
                publisher = plain(fields.get("publisher") or fields.get("institution") or fields.get("school"))
                if publisher:
                    publication += (", " if publication else "") + escape(publisher)
            published_year = publication_date(fields)[0]
            year = str(published_year) if published_year else plain(fields.get("year"))
            publication += f' ({escape(year or "n.d.")}).'
            parts.append(publication.strip())
            reference = Reference(key, " ".join(parts))
            if fields.get("doi"):
                doi, reference.url = doi_link(fields["doi"])
                reference.link_label = "DOI: " + doi
            elif fields.get("url"):
                url = plain(fields["url"])
                parsed = urlsplit(url)
                if parsed.scheme not in ("http", "https") or not parsed.netloc or any(ord(c) < 32 for c in url) or "\\" in url:
                    raise ValueError(f"Invalid reference URL for {key}: {url!r}")
                reference.url, reference.link_label = url, "原文链接"
            references.append(reference)
        return references
    except Exception as error:
        raise ValueError(f"Cannot read references in {path}: {error}") from error
