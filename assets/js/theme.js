(() => {
  const root = document.documentElement;
  const key = 'flowers-for-tuesday:theme';
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  const valid = value => value === 'light' || value === 'dark';
  let preference = null;
  let toggle;
  try { preference = localStorage.getItem(key); } catch { /* Storage is optional. */ }
  if (!valid(preference)) preference = null;

  const apply = () => {
    const theme = preference || (system.matches ? 'dark' : 'light');
    const changed = root.dataset.theme !== theme;
    root.dataset.theme = theme;
    document.querySelector('meta[name="theme-color"]').content = theme === 'dark' ? '#182326' : '#f8f9f6';
    if (toggle) {
      toggle.setAttribute('aria-pressed', String(theme === 'dark'));
      toggle.title = theme === 'dark' ? '切换到浅色模式' : '切换到深色模式';
    }
    if (changed) window.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
  };

  // Run before styles and body are parsed to avoid a light flash on dark pages.
  apply();
  system.addEventListener('change', () => { if (!preference) apply(); });
  window.addEventListener('storage', event => {
    if (event.key !== key && event.key !== null) return;
    preference = valid(event.newValue) ? event.newValue : null;
    apply();
  });
  document.addEventListener('DOMContentLoaded', () => {
    toggle = document.querySelector('.theme-toggle');
    if (!toggle) return;
    apply();
    toggle.hidden = false;
    toggle.addEventListener('click', () => {
      preference = root.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem(key, preference); } catch { /* Keep the choice for this page. */ }
      apply();
    });
  });
})();
