(() => {
  if (!document.querySelector('.reference-item')) return;
  document.documentElement.classList.add('references-enhanced');
  let current;
  const highlight = () => {
    if (current) current.classList.remove('reference-highlight');
    current = null;
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); }
    catch { return; }
    const target = document.getElementById(id);
    if (!target?.classList.contains('reference-item')) return;
    current = target;
    // Restart the brief cue even when the same citation is clicked again.
    void target.offsetWidth;
    target.classList.add('reference-highlight');
  };
  document.addEventListener('animationend', event => {
    if (event.animationName === 'reference-highlight') {
      event.target.classList.remove('reference-highlight');
    }
  });
  window.addEventListener('hashchange', highlight);
  window.addEventListener('pageshow', highlight);
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || link.hasAttribute('download') || (link.target && link.target !== '_self')) return;
    const url = new URL(link.href, location.href);
    if (url.href === location.href && url.hash) highlight();
  });
  highlight();
})();
