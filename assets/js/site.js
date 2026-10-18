(() => {
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.site-nav');
  const mobile = window.matchMedia('(max-width: 680px)');
  const setMenu = (open) => {
    nav.classList.toggle('is-open', open);
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? '收起导航菜单' : '展开导航菜单');
  };
  if (menu && nav) {
    menu.hidden = false;
    document.documentElement.classList.add('menu-ready');
    setMenu(false);
    menu.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true'));
    nav.addEventListener('click', (event) => {
      if (event.target.closest('a')) setMenu(false);
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && mobile.matches && menu.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        menu.focus();
      }
    });
    mobile.addEventListener('change', () => setMenu(false));
  }

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const track = document.querySelector('.directory-track');
  const cards = [...document.querySelectorAll('.directory-card')];
  if (track && cards.length) {
    const hero = document.querySelector('.hero');
    let active = Math.max(0, cards.findIndex(card => card.classList.contains('is-expanded')));
    const ratios = cards.map(card => {
      const img = card.querySelector('img');
      return () => (img.naturalWidth || Number(img.width)) / (img.naturalHeight || Number(img.height));
    });
    const sizeCards = () => {
      const style = getComputedStyle(track);
      const gap = parseFloat(style.columnGap);
      const minimum = parseFloat(style.getPropertyValue('--thumb-min'));
      const ratio = Math.max(...ratios.map(read => read()));
      const height = Math.max(1, Math.min(hero.getBoundingClientRect().height,
        (track.clientWidth - (cards.length - 1) * (minimum + gap)) / ratio));
      track.style.setProperty('--card-height', `${height}px`);
      track.style.setProperty('--expanded-width', `${height * ratios[active]()}px`);
    };
    const activate = index => {
      active = index;
      cards.forEach((card, i) => card.classList.toggle('is-expanded', i === active));
      sizeCards();
    };
    cards.forEach((card, index) => {
      let expandOnClick = false;
      card.addEventListener('pointerenter', event => {
        if (event.pointerType === 'mouse') activate(index);
      });
      card.addEventListener('pointerdown', event => {
        expandOnClick = event.pointerType !== 'mouse' && active !== index;
      });
      card.addEventListener('pointercancel', () => { expandOnClick = false; });
      card.addEventListener('focus', () => activate(index));
      card.addEventListener('click', event => {
        if (expandOnClick) {
          event.preventDefault();
          activate(index);
        }
        expandOnClick = false;
      });
      card.querySelector('img').addEventListener('load', sizeCards);
    });
    track.addEventListener('keydown', event => {
      if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      const index = event.key === 'Home' ? 0 : event.key === 'End' ? cards.length - 1
        : Math.max(0, Math.min(cards.length - 1, active + (event.key === 'ArrowRight' ? 1 : -1)));
      cards[index].focus({ preventScroll: true });
    });
    const observer = new ResizeObserver(sizeCards);
    observer.observe(hero);
    observer.observe(track);
    document.fonts.ready.then(sizeCards);
    sizeCards();
  }

  const aboutCopy = document.querySelector('.about-copy');
  if (aboutCopy) {
    const currentTheme = () => document.documentElement.dataset.theme || 'light';
    const images = [...document.querySelectorAll('.theme-image')];
    images.forEach(figure => figure.style.setProperty('--image-night-opacity', currentTheme() === 'dark' ? '1' : '0'));
    const updateImages = () => {
      const theme = currentTheme();
      images.forEach(async figure => {
        const target = figure.querySelector(theme === 'dark' ? '.theme-image-night' : '.theme-image-day');
        try { await target.decode(); } catch { return; /* Retain the current image if loading fails. */ }
        if (currentTheme() === theme) figure.style.setProperty('--image-night-opacity', theme === 'dark' ? '1' : '0');
      });
    };
    window.addEventListener('themechange', updateImages);
    const entries = [...aboutCopy.querySelectorAll('.about-entry')];
    const pagination = aboutCopy.querySelector('.about-pagination');
    if (pagination) {
      const previous = pagination.querySelector('.about-previous');
      const next = pagination.querySelector('.about-next');
      const position = pagination.querySelector('.about-position');
      const empty = aboutCopy.querySelector('.about-empty');
      const remembered = new Map();
      let available = [];
      let active = 0;
      const showEntry = index => {
        active = available.length ? (index + available.length) % available.length : 0;
        const selected = available[active];
        entries.forEach(entry => { entry.hidden = entry !== selected; });
        previous.disabled = next.disabled = available.length < 2;
        pagination.hidden = available.length === 0;
        if (empty) empty.hidden = available.length !== 0;
        position.textContent = selected ? `${active + 1} / ${available.length}` : '';
        position.setAttribute('aria-label', selected ? `第 ${active + 1} 篇，共 ${available.length} 篇：${selected.querySelector('.page-subtitle').textContent}` : '暂无文章');
        remembered.set(currentTheme(), active);
      };
      const filterEntries = () => {
        available = entries.filter(entry => !entry.dataset.entryTheme || entry.dataset.entryTheme === 'all' || entry.dataset.entryTheme === currentTheme());
        showEntry(remembered.get(currentTheme()) || 0);
      };
      previous.addEventListener('click', () => showEntry(active - 1));
      next.addEventListener('click', () => showEntry(active + 1));
      pagination.addEventListener('keydown', event => {
        if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
        event.preventDefault();
        showEntry(active + (event.key === 'ArrowRight' ? 1 : -1));
      });
      filterEntries();
      window.addEventListener('themechange', filterEntries);
    }
  }

  const intro = document.querySelector('.intro');
  if (!intro || typeof intro.showModal !== 'function') return;
  const sessionKey = 'flowers-for-tuesday:intro-seen';
  let timer;
  let closeTimer;
  let preparing = false;
  const finish = () => {
    clearTimeout(timer);
    clearTimeout(closeTimer);
    if (intro.open) intro.close();
    intro.classList.remove('is-leaving');
  };
  const dismiss = () => {
    if (!intro.open || intro.classList.contains('is-leaving')) return;
    clearTimeout(timer);
    intro.classList.add('is-leaving');
    closeTimer = setTimeout(finish, reducedMotion.matches ? 0 : 550);
  };
  const show = async () => {
    if (intro.open || preparing) return;
    preparing = true;
    // Limit the wait: a slow font download must never prevent access to the site.
    try {
      await Promise.race([document.fonts.load('32px "Tokyo Romance"'), new Promise(resolve => setTimeout(resolve, 700))]);
    } catch { /* The system font remains readable if font loading fails. */ }
    preparing = false;
    intro.classList.remove('is-leaving');
    intro.showModal();
    try { sessionStorage.setItem(sessionKey, '1'); } catch { /* Private browsing may block storage. */ }
    timer = setTimeout(dismiss, reducedMotion.matches ? 1800 : 4200);
  };
  intro.querySelector('.intro-skip').addEventListener('click', dismiss);
  intro.addEventListener('cancel', (event) => { event.preventDefault(); dismiss(); });
  window.addEventListener('pagehide', finish);
  let seen = false;
  try { seen = sessionStorage.getItem(sessionKey) === '1'; } catch { /* Still show a dismissible intro. */ }
  if (!seen && !reducedMotion.matches) show();
})();
