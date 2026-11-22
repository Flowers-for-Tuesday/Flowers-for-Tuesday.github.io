(() => {
  const search = document.querySelector('#note-search');
  if (!search) return;
  const cards = [...document.querySelectorAll('[data-note]')];
  const groups = [...document.querySelectorAll('[data-note-group]')];
  const filters = [...document.querySelectorAll('[data-category-filter]')];
  const categoryLinks = [...document.querySelectorAll('.note-categories [data-category-filter]')];
  const layout = document.querySelector('#notes');
  const result = document.querySelector('#note-results');
  const libraryCount = document.querySelector('.note-library-count');
  const totalCount = categoryLinks.find(link => !link.dataset.categoryFilter)?.querySelector('span');
  let category = '';
  const normalize = text => text.normalize('NFKC').toLocaleLowerCase();
  const searchable = new Map(cards.map(card => [card, normalize(card.dataset.search)]));
  const availableInTheme = element => !element.dataset.noteTheme || element.dataset.noteTheme === document.documentElement.dataset.theme;
  const padded = count => String(count).padStart(2, '0');
  const update = () => {
    for (const link of categoryLinks) link.hidden = !availableInTheme(link);
    if (category && categoryLinks.some(link => link.dataset.categoryFilter === category && link.hidden)) {
      category = '';
      history.replaceState(null, '', '#notes');
    }
    const availableCards = cards.filter(availableInTheme);
    const availableCategories = categoryLinks.filter(link => link.dataset.categoryFilter && !link.hidden);
    if (totalCount) totalCount.textContent = padded(availableCards.length);
    if (libraryCount) libraryCount.textContent = `${padded(availableCategories.length)} 个主题 · ${padded(availableCards.length)} 篇笔记`;
    layout.classList.toggle('notes-overview', !category);
    const words = normalize(search.value).trim().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const card of cards) {
      const visible = availableInTheme(card) && (!category || card.dataset.category === category) && words.every(word => searchable.get(card).includes(word));
      card.hidden = !visible;
      if (visible) count++;
    }
    for (const group of groups) {
      const showEmptyCategory = group.dataset.emptyCategory && !words.length && (!category || category === group.dataset.emptyCategory);
      group.hidden = !showEmptyCategory && !group.querySelector('[data-note]:not([hidden])');
      group.querySelector('.note-grid').tabIndex = category ? -1 : 0;
    }
    for (const filter of categoryLinks) {
      if (filter.dataset.categoryFilter === category) filter.setAttribute('aria-current', 'true');
      else filter.removeAttribute('aria-current');
    }
    result.textContent = `找到 ${count} 篇笔记`;
    document.querySelector('.note-no-results').hidden = count !== 0 || groups.some(group => !group.hidden && group.dataset.emptyCategory);
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
  window.addEventListener('themechange', update);
  readHash();
})();
