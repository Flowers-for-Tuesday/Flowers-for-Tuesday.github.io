(() => {
  const root = document.documentElement;
  const key = 'flowers-for-tuesday:theme';
  const paletteKey = 'flowers-for-tuesday:palette';
  const palettes = Array.isArray(window.SITE_PALETTES) ? window.SITE_PALETTES : [];
  const validPalette = value => palettes.some(palette => palette.id === value);
  const defaultPalette = validPalette(window.SITE_DEFAULT_PALETTE) ? window.SITE_DEFAULT_PALETTE : (palettes[0]?.id || 'palette-0001');
  let palette = defaultPalette;
  let paletteToggle;
  let paletteStatus;
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  const valid = value => value === 'light' || value === 'dark';
  let preference = null;
  let toggle;
  try { preference = localStorage.getItem(key); } catch { /* Storage is optional. */ }
  try { palette = localStorage.getItem(paletteKey); } catch { /* Storage is optional. */ }
  if (!validPalette(palette)) palette = defaultPalette;
  if (!valid(preference)) preference = null;

  const apply = () => {
    const theme = preference || (system.matches ? 'dark' : 'light');
    const changed = root.dataset.theme !== theme;
    const paletteChanged = root.dataset.palette !== palette;
    root.dataset.theme = theme;
    root.dataset.palette = palette;
    const selected = palettes.find(item => item.id === palette);
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = selected ? selected.paper[theme] : (theme === 'dark' ? '#182326' : '#f8f9f6');
    if (toggle) {
      toggle.setAttribute('aria-pressed', String(theme === 'dark'));
      toggle.title = theme === 'dark' ? '切换到浅色模式' : '切换到深色模式';
    }
    if (paletteToggle && selected) {
      paletteToggle.setAttribute('aria-label', `下一组配色，当前第 ${selected.index} 组，共 ${palettes.length} 组`);
      if (paletteStatus) paletteStatus.textContent = `当前配色：${selected.index} / ${palettes.length}`;
    }
    if (changed) window.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
    if (paletteChanged) window.dispatchEvent(new CustomEvent('palettechange', { detail: { palette } }));
  };

  const selectPalette = value => {
    if (!validPalette(value)) return;
    palette = value;
    try { localStorage.setItem(paletteKey, palette); } catch { /* Keep the choice for this page. */ }
    apply();
  };
  window.SiteTheme = { selectPalette };

  // Run before styles and body are parsed to avoid a light flash on dark pages.
  apply();
  system.addEventListener('change', () => { if (!preference) apply(); });
  window.addEventListener('storage', event => {
    if (event.key !== key && event.key !== paletteKey && event.key !== null) return;
    if (event.key === key || event.key === null) preference = valid(event.newValue) ? event.newValue : null;
    if (event.key === paletteKey || event.key === null) palette = validPalette(event.newValue) ? event.newValue : defaultPalette;
    apply();
  });
  document.addEventListener('DOMContentLoaded', () => {
    paletteToggle = document.querySelector('.palette-toggle');
    paletteStatus = document.querySelector('.palette-status');
    if (paletteToggle && palettes.length) {
      paletteToggle.hidden = false;
      paletteToggle.addEventListener('click', () => {
        const current = palettes.findIndex(item => item.id === palette);
        selectPalette(palettes[(current + 1) % palettes.length].id);
      });
    }
    toggle = document.querySelector('.theme-toggle');
    apply();
    if (!toggle) return;
    toggle.hidden = false;
    toggle.addEventListener('click', () => {
      preference = root.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem(key, preference); } catch { /* Keep the choice for this page. */ }
      apply();
    });
  });
})();
