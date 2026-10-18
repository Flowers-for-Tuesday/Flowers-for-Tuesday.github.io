(() => {
  const search = document.querySelector('#note-search');
  if (!search) return;
  const cards = [...document.querySelectorAll('[data-note]')];
  const groups = [...document.querySelectorAll('[data-note-group]')];
  const filters = [...document.querySelectorAll('[data-category-filter]')];
  const categoryLinks = [...document.querySelectorAll('.note-categories [data-category-filter]')];
  const layout = document.querySelector('#notes');
  const result = document.querySelector('#note-results');
  let category = '';
  const normalize = text => text.normalize('NFKC').toLocaleLowerCase();
  const searchable = new Map(cards.map(card => [card, normalize(card.dataset.search)]));
  const update = () => {
    layout.classList.toggle('notes-overview', !category);
    const words = normalize(search.value).trim().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const card of cards) {
      const visible = (!category || card.dataset.category === category) && words.every(word => searchable.get(card).includes(word));
      card.hidden = !visible;
      if (visible) count++;
    }
    for (const group of groups) {
      group.hidden = !group.querySelector('[data-note]:not([hidden])');
      group.querySelector('.note-grid').tabIndex = category ? -1 : 0;
    }
    for (const filter of categoryLinks) {
      if (filter.dataset.categoryFilter === category) filter.setAttribute('aria-current', 'true');
      else filter.removeAttribute('aria-current');
    }
    result.textContent = `找到 ${count} 篇笔记`;
    document.querySelector('.note-no-results').hidden = count !== 0;
  };
  document.querySelector('.note-search').hidden = false;
  search.addEventListener('input', update);
  document.querySelector('#clear-note-search').addEventListener('click', () => {
    search.value = '';
    update();
    search.focus();
  });
  for (const filter of filters) filter.addEventListener('click', event => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    if (location.hash !== filter.hash) history.pushState(null, '', filter.hash);
    category = filter.dataset.categoryFilter;
    update();
    if (filter.classList.contains('note-more')) {
      const heading = filter.closest('[data-note-group]').querySelector('h2');
      heading.focus({ preventScroll: true });
      heading.closest('[data-note-group]').scrollIntoView({ block: 'start' });
    }
  });
  const readHash = () => {
    category = categoryLinks.find(link => link.hash === location.hash)?.dataset.categoryFilter || '';
    update();
  };
  window.addEventListener('hashchange', readHash);
  readHash();
})();
