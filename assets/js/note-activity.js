(() => {
  const calendar = document.querySelector('.note-activity');
  if (!calendar) return;
  const days = [...calendar.querySelectorAll('.note-activity-day')];
  const detail = calendar.querySelector('.note-activity-tooltip');
  const scroll = calendar.querySelector('.note-activity-scroll');
  const show = day => {
    detail.textContent = day.getAttribute('aria-label');
    detail.hidden = false;
  };
  const select = day => {
    for (const item of days) item.tabIndex = item === day ? 0 : -1;
    show(day);
  };
  calendar.addEventListener('pointerover', event => {
    const day = event.target.closest('.note-activity-day');
    if (day) show(day);
  });
  calendar.addEventListener('pointerleave', () => {
    const focused = document.activeElement;
    if (focused.matches('.note-activity-day')) show(focused);
    else detail.hidden = true;
  });
  calendar.addEventListener('focusout', event => {
    if (!calendar.contains(event.relatedTarget)) detail.hidden = true;
  });
  calendar.addEventListener('focusin', event => {
    if (event.target.matches('.note-activity-day')) select(event.target);
  });
  calendar.addEventListener('click', event => {
    const day = event.target.closest('.note-activity-day');
    if (day) select(day);
  });
  calendar.addEventListener('keydown', event => {
    if (event.key === 'Escape') { detail.hidden = true; return; }
    const index = days.indexOf(event.target);
    if (index < 0) return;
    const steps = { ArrowLeft: -7, ArrowRight: 7, ArrowUp: -1, ArrowDown: 1 };
    let next;
    if (event.key in steps) next = index + steps[event.key];
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = days.length - 1;
    else return;
    event.preventDefault();
    const day = days[Math.max(0, Math.min(days.length - 1, next))];
    select(day);
    day.focus({ preventScroll: true });
    const bounds = day.getBoundingClientRect();
    const viewport = scroll.getBoundingClientRect();
    if (bounds.left < viewport.left) scroll.scrollLeft -= viewport.left - bounds.left + 8;
    if (bounds.right > viewport.right) scroll.scrollLeft += bounds.right - viewport.right + 8;
  });
  // On small screens, start at the most recent weeks.
  scroll.scrollLeft = scroll.scrollWidth;
})();
