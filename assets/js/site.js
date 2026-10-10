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

  const intro = document.querySelector('.intro');
  const replay = document.querySelector('.replay-intro');
  if (!intro || typeof intro.showModal !== 'function') return;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const sessionKey = 'flowers-for-tuesday:intro-seen';
  let timer;
  let closeTimer;
  let manual = false;
  let preparing = false;
  const finish = () => {
    clearTimeout(timer);
    clearTimeout(closeTimer);
    if (intro.open) intro.close();
    intro.classList.remove('is-leaving');
    if (manual) replay?.focus({ preventScroll: true });
  };
  const dismiss = () => {
    if (!intro.open || intro.classList.contains('is-leaving')) return;
    clearTimeout(timer);
    intro.classList.add('is-leaving');
    closeTimer = setTimeout(finish, reducedMotion.matches ? 0 : 550);
  };
  const show = async (isManual = false) => {
    if (intro.open || preparing) return;
    preparing = true;
    manual = isManual;
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
  if (replay) {
    replay.hidden = false;
    replay.addEventListener('click', () => show(true));
  }
  let seen = false;
  try { seen = sessionStorage.getItem(sessionKey) === '1'; } catch { /* Still show a dismissible intro. */ }
  if (!seen && !reducedMotion.matches) show();
})();
