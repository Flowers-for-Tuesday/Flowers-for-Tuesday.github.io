"""Build the Note directory's daily publication calendar from declared dates."""
from collections import Counter
from datetime import date, datetime, timedelta, timezone


def activity_calendar(notes, *, today=None):
    today = today or datetime.now(timezone(timedelta(hours=8))).date()
    start = today - timedelta(days=364)
    grid_start = start - timedelta(days=(start.weekday() + 1) % 7)
    weeks = ((today - grid_start).days // 7) + 1
    counts = Counter(
        note.published for note in notes
        if note.published and not note.meta.get("draft")
        and start <= date.fromisoformat(note.published) <= today
    )
    cells, months = [], []
    last_month_column = -3
    for offset in range(weeks * 7):
        day = grid_start + timedelta(days=offset)
        column, row = offset // 7 + 1, offset % 7 + 1
        position = f'grid-column:{column};grid-row:{row}'
        if day < start or day > today:
            cells.append(f'<span class="note-activity-pad" style="{position}" aria-hidden="true"></span>')
            continue
        if (day == start or day.day == 1) and column - last_month_column >= 3 and column <= weeks - 2:
            months.append(f'<span style="grid-column:{column}">{day.month}月</span>')
            last_month_column = column
        count = counts[day.isoformat()]
        label = f'{day.isoformat()}：新增 {count} 篇笔记'
        current = ' aria-current="date"' if day == today else ''
        cells.append(f'<button type="button" class="note-activity-day" data-date="{day.isoformat()}" data-count="{count}" data-level="{min(count, 4)}" style="{position}" tabindex="{0 if day == today else -1}" aria-label="{label}" title="{label}"{current}></button>')
    return f'''<section class="note-activity" aria-label="每日新增笔记，最近一年共 {sum(counts.values())} 篇" style="--activity-weeks:{weeks}">
      <div class="note-activity-scroll"><div class="note-activity-calendar">
        <div class="note-activity-months" aria-hidden="true">{''.join(months)}</div>
        <div class="note-activity-weekdays" aria-hidden="true"><span>一</span><span>三</span><span>五</span></div>
        <div class="note-activity-days" role="group" aria-label="每日新增数量，可用方向键切换日期">{''.join(cells)}</div>
      </div></div>
      <p class="note-activity-tooltip" role="status" aria-live="polite" hidden></p>
    </section>'''
