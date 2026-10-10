(() => {
  const search = document.querySelector('#note-search');
  if (!search) return;
  const cards = [...document.querySelectorAll('[data-note]')];
  const groups = [...document.querySelectorAll('[data-note-group]')];
  const filters = [...document.querySelectorAll('[data-category-filter]')];
  const result = document.querySelector('#note-results');
  let category = '';
  const normalize = text => text.normalize('NFKC').toLocaleLowerCase();
  const searchable = new Map(cards.map(card => [card, normalize(card.dataset.search)]));
  const update = () => {
    const words = normalize(search.value).trim().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const card of cards) {
      const visible = (!category || card.dataset.category === category) && words.every(word => searchable.get(card).includes(word));
      card.hidden = !visible;
      if (visible) count++;
    }
    for (const group of groups) group.hidden = !group.querySelector('[data-note]:not([hidden])');
    for (const filter of filters) {
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
    event.preventDefault();
    category = filter.dataset.categoryFilter;
    update();
  });
})();
