(() => {
  const cards = Array.from(document.querySelectorAll('[data-select-palette]'));
  const current = document.querySelector('.color-current');
  if (!current || !window.SiteTheme) return;
  const name = current.querySelector('.color-current-name');
  const swatches = current.querySelector('.color-current-swatches');
  const sample = current.querySelector('.color-current-image');
  const assetBase = new URL(current.dataset.paletteAssets, document.baseURI);
  const sync = () => {
    const id = document.documentElement.dataset.palette;
    const selected = window.SITE_PALETTES.find(palette => palette.id === id);
    if (!selected) return;
    cards.forEach(card => card.setAttribute('aria-pressed', String(card.dataset.selectPalette === id)));
    name.textContent = `${String(selected.number).padStart(4, '0')} · ${selected.title}`;
    sample.src = new URL(selected.image, assetBase).href;
    sample.alt = `${selected.title} · 配色样图`;
    swatches.replaceChildren(...selected.colors.map((color, index) => {
      const swatch = document.createElement('span');
      swatch.className = 'color-swatch';
      const chip = document.createElement('span');
      chip.className = 'color-chip';
      chip.style.backgroundColor = color;
      const hex = document.createElement('span');
      hex.className = 'color-hex';
      hex.textContent = color;
      const colorName = document.createElement('span');
      colorName.className = 'color-english-name';
      colorName.lang = 'en';
      colorName.textContent = selected.color_names[index];
      swatch.append(chip, colorName, hex);
      return swatch;
    }));
    current.hidden = false;
  };
  cards.forEach(card => {
    card.disabled = false;
    card.addEventListener('click', () => window.SiteTheme.selectPalette(card.dataset.selectPalette));
  });
  window.addEventListener('palettechange', sync);
  sync();
})();
