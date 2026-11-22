"""Load About entries from Markdown with YAML metadata."""
from pathlib import Path

from markdown_it import MarkdownIt

from notes import date_value, split_frontmatter
from dates import display_date


def load_about_entries(base):
    entries = []
    markdown = MarkdownIt("commonmark", {"html": False})
    for source in sorted((Path(base) / "files/about").glob("*.md")):
        try:
            meta, body = split_frontmatter(source.read_text(encoding="utf-8-sig"))
            subtitle = meta.get("subtitle")
            if not isinstance(subtitle, dict):
                raise ValueError("subtitle must contain date, period and location")
            for key in ("period", "location"):
                if not isinstance(subtitle.get(key), str):
                    raise ValueError(f"subtitle.{key} must be a quoted string")
            raw_date = subtitle.get("date")
            # Retain older slash-separated strings; ISO dates share Note's parser.
            if isinstance(raw_date, str) and "/" in raw_date:
                formatted_date = display_date(raw_date)
            else:
                published = date_value(raw_date)
                if not published:
                    raise ValueError("subtitle.date must contain a date")
                formatted_date = display_date(published)
            order = meta.get("order", 0)
            if isinstance(order, bool) or not isinstance(order, int):
                raise ValueError("order must be an integer")
            period = subtitle["period"].strip()
            entries.append({
                "source": source,
                "order": order,
                "subtitle": "，".join(part for part in (formatted_date, period, subtitle["location"].strip()) if part),
                "theme": {"晨": "light", "午": "light", "夜": "dark"}.get(period, "all"),
                "html": markdown.render(body),
            })
        except ValueError as error:
            raise ValueError(f"{source}: {error}") from error
    return sorted(entries, key=lambda entry: (entry["order"], entry["source"].name))
