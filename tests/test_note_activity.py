"""Daily counts, calendar boundaries and isolation from other collections."""
from datetime import date, timedelta
from html.parser import HTMLParser
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from note_activity import activity_calendar
from notes import NoteLibrary


class CalendarParser(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.days = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "button" and "data-date" in attrs:
            self.days.append(attrs)


def note(published, **meta):
    return SimpleNamespace(published=published, meta=meta)


class NoteActivityTests(unittest.TestCase):
    def test_daily_counts_exclude_drafts_undated_and_outside_window(self):
        today = date(2026, 11, 6)
        start = today - timedelta(days=364)
        notes = [note(today.isoformat()) for _ in range(5)]
        notes += [note(start.isoformat()), note(""), note(today.isoformat(), draft=True),
                  note((start - timedelta(days=1)).isoformat()), note("2026-11-07")]
        html = activity_calendar(notes, today=today)
        cells = {day['data-date']: day for day in CalendarParser(html).days}
        self.assertEqual(cells[today.isoformat()]['data-count'], '5')
        self.assertEqual(cells[today.isoformat()]['data-level'], '4')
        self.assertEqual(cells[start.isoformat()]['data-count'], '1')
        self.assertEqual(cells['2026-11-05']['data-count'], '0')
        self.assertIn('最近一年共 6 篇', html)

    def test_calendar_includes_leap_day_and_exactly_365_distinct_days(self):
        today = date(2024, 3, 1)
        days = CalendarParser(activity_calendar([note('2024-02-29')], today=today)).days
        self.assertEqual(len(days), 365)
        self.assertEqual(len({day['data-date'] for day in days}), 365)
        self.assertEqual(days[0]['data-date'], (today - timedelta(days=364)).isoformat())
        self.assertEqual(days[-1]['data-date'], today.isoformat())
        leap_day = next(day for day in days if day['data-date'] == '2024-02-29')
        self.assertEqual(leap_day['data-count'], '1')
        self.assertIn('grid-row:5', leap_day['style'])  # Thursday, Sunday first.
        self.assertEqual(sum(day['tabindex'] == '0' for day in days), 1)
        self.assertEqual(days[-1]['aria-current'], 'date')

    def test_empty_calendar_and_sunday_boundary(self):
        days = CalendarParser(activity_calendar([], today=date(2026, 11, 8))).days
        self.assertTrue(all(day['data-count'] == '0' for day in days))
        self.assertIn('grid-row:1', days[-1]['style'])
        self.assertTrue(all('新增 0 篇笔记' in day['aria-label'] for day in days))

    def test_shared_directory_only_includes_calendar_when_requested(self):
        library = NoteLibrary(Path(__file__).resolve().parents[1])
        self.assertNotIn('class="note-activity"', library.directory())
        self.assertIn('class="note-activity"', library.directory(show_activity=True))


if __name__ == '__main__':
    unittest.main()
