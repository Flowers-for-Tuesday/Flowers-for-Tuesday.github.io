/* Journals remain ordinary, readable links when JavaScript is unavailable. */
(() => {
  const source = document.querySelector('#gallery-data');
  if (!source) return;
  const journals = JSON.parse(source.textContent);
  const byId = new Map(journals.map(note => [note.id, note]));
  const $ = selector => document.querySelector(selector);
  const cards = [...document.querySelectorAll('[data-journal]')];
  const motion = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let scope = 'all';
  let visible = journals;
  let map, points, routes;
  const countryBounds = new Map();
  const overviewCountries = new Map();
  const detailRequests = new Map();
  let overview, overviewSettled = false;
  let activeDetail, hiddenOverview = [];
  let mapSelection = 0;
  let currentRequest;
  let opener;
  let cleanupCarousel = () => {};
  const dialog = $('.journal-dialog');
  const dialogContent = $('.dialog-content');
  const status = $('#map-status');

  async function openJournal(note, trigger) {
    if (!dialog.showModal) { location.href = note.url; return; }
    currentRequest?.abort();
    const request = new AbortController();
    currentRequest = request;
    opener = trigger || document.activeElement;
    cleanupCarousel();
    dialogContent.replaceChildren();
    const loading = document.createElement('p');
    loading.className = 'dialog-message';
    loading.setAttribute('role', 'status');
    loading.textContent = '正在加载笔记…';
    dialogContent.append(loading);
    dialog.setAttribute('aria-label', note.title);
    if (!dialog.open) dialog.showModal();
    dialog.scrollTop = 0;
    try {
      const response = await fetch(note.url, { signal: request.signal });
      if (!response.ok) throw new Error('Article unavailable');
      const articleUrl = new URL(note.url, location.href);
      const doc = new DOMParser().parseFromString(await response.text(), 'text/html');
      const entry = doc.querySelector('.gallery-entry');
      if (!entry) throw new Error('Article unavailable');
      // Detail pages use paths relative to their own folders.
      entry.querySelectorAll('[src], [href]').forEach(element => {
        for (const attribute of ['src', 'href']) {
          const value = element.getAttribute(attribute);
          if (value) element.setAttribute(attribute, new URL(value, articleUrl).href);
        }
      });
      if (request.signal.aborted || !dialog.open) return;
      dialogContent.replaceChildren(entry);
      cleanupCarousel = window.GalleryCarousel?.init(entry) || (() => {});
      entry.querySelector('.entry-links a')?.addEventListener('click', event => {
        event.preventDefault();
        dialog.close();
        // A selected entry is always a member of the current filtered collection.
        if (map) {
          map.setView([note.place.lat, note.place.lng], 5, { animate: motion });
          $('#footprints').scrollIntoView({ behavior: motion ? 'smooth' : 'auto', block: 'start' });
        } else location.href = event.currentTarget.href;
      });
    } catch (error) {
      if (request.signal.aborted) return;
      loading.textContent = '暂时无法加载预览，';
      const link = document.createElement('a');
      link.href = note.url;
      link.textContent = '打开完整笔记 ↗';
      loading.append(link);
    }
  }

  document.addEventListener('click', event => {
    const link = event.target.closest('[data-open-journal]');
    if (!link || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const note = byId.get(link.dataset.openJournal);
    if (!note) return;
    event.preventDefault();
    openJournal(note, link);
  });
  $('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    currentRequest?.abort();
    cleanupCarousel();
    opener?.focus({ preventScroll: true });
  });

  function fitCountry() {
    if (!map) return;
    const world = [[-56, -178], [78, 178]];
    let bounds = scope === 'all' ? world : countryBounds.get(scope);
    // Small countries absent from the overview dataset still have their journal coordinates.
    // Use all notes in the country so an empty search does not change its geographic scope.
    if (!bounds) {
      const locations = journals.filter(note => note.place.country === scope)
        .map(note => [note.place.lat, note.place.lng]);
      bounds = locations.length ? L.latLngBounds(locations) : world;
    }
    map.fitBounds(bounds, { padding: [24, 24], maxZoom: 6, animate: motion });
  }

  async function syncMapToCountry() {
    if (!map) return;
    const selection = ++mapSelection;
    const country = scope;
    if (activeDetail) map.removeLayer(activeDetail);
    activeDetail = null;
    hiddenOverview.forEach(layer => overview.addLayer(layer));
    hiddenOverview = [];
    fitCountry();
    if (!overviewSettled) return;
    if (country === 'all') {
      status.hidden = Boolean(overview);
      status.textContent = overview ? '' : '地图底图暂时无法加载；足迹点仍可使用。刷新页面可重试。';
      return;
    }
    status.hidden = false;
    status.textContent = '正在加载更精细的国家地图…';
    try {
      if (!detailRequests.has(country)) {
        const request = (async () => {
          const response = await fetch(`../assets/maps/countries/${country}.geojson`);
          if (!response.ok) throw new Error('Detailed map unavailable');
          const layer = L.geoJSON(await response.json(), {
            pane: 'land', interactive: false, smoothFactor: .2,
            style: feature => feature.properties.layer === 'admin1'
              ? { className: 'map-region', fill: false, weight: .8, opacity: .85 }
              : { className: 'map-land map-land-detail' }
          });
          if (!layer.getBounds().isValid()) throw new Error('Invalid detailed map');
          return layer;
        })();
        detailRequests.set(country, request);
        request.catch(() => detailRequests.delete(country));
      }
      const layer = await detailRequests.get(country);
      // A slow response must never replace a more recent country selection.
      if (selection !== mapSelection) return;
      hiddenOverview = overviewCountries.get(country) || [];
      hiddenOverview.forEach(item => overview.removeLayer(item));
      activeDetail = layer.addTo(map);
      countryBounds.set(country, layer.getBounds());
      fitCountry();
      status.hidden = Boolean(overview);
      status.textContent = overview ? '' : '国家地图已加载，周边世界底图暂不可用。';
    } catch {
      if (selection !== mapSelection) return;
      status.hidden = false;
      status.textContent = overview
        ? '精细地图暂不可用，已保留总览底图；重新选择该国家可重试。'
        : '地图底图暂不可用；足迹点仍可使用。重新选择该国家可重试。';
    }
  }

  function updateMap() {
    if (!map) return;
    points.clearLayers();
    routes.clearLayers();
    const chronological = [...visible].sort((a, b) => a.date.localeCompare(b.date) || a.id.localeCompare(b.id));
    // Group coincident locations so multiple journals at the same spot remain accessible.
    const locations = new Map();
    chronological.forEach((note, index) => {
      const key = `${note.place.lat},${note.place.lng}`;
      const group = locations.get(key) || [];
      group.push({ note, number: index + 1 });
      locations.set(key, group);
    });
    locations.forEach(group => {
      const first = group[0];
      const marker = L.marker([first.note.place.lat, first.note.place.lng], {
        icon: L.divIcon({ className: 'footprint-marker', html: `<span>${group.length > 1 ? group.length + '篇' : first.number}</span>`, iconSize: [30, 30], iconAnchor: [15, 15] }),
        title: `${first.note.place.name} · ${group.length} 篇笔记`, keyboard: true
      }).addTo(points);
      const label = document.createElement('span');
      label.textContent = first.note.place.name;
      marker.bindTooltip(label, { className: 'footprint-label', direction: 'top', offset: [0, -14] });
      if (group.length === 1) marker.on('click', () => openJournal(first.note, marker.getElement()));
      else {
        const list = document.createElement('div');
        group.forEach(({ note }) => {
          const link = document.createElement('a');
          link.href = note.url;
          link.dataset.openJournal = note.id;
          link.textContent = `${note.date} · ${note.title}`;
          list.append(link, document.createElement('br'));
        });
        marker.bindPopup(list);
      }
    });
    if ($('#show-route').checked) {
      for (let i = 1; i < chronological.length; i++) {
        const a = chronological[i - 1].place;
        const b = chronological[i].place;
        const line = [[a.lat, a.lng], [b.lat, b.lng]];
        if (Math.abs(b.lng - a.lng) > 180) {
          // Split at the dateline rather than drawing a long line across the world.
          const end = b.lng + (b.lng > a.lng ? -360 : 360);
          const edge = end > a.lng ? 180 : -180;
          const lat = a.lat + (b.lat - a.lat) * (edge - a.lng) / (end - a.lng);
          line.splice(0, 2, [[a.lat, a.lng], [lat, edge]], [[lat, -edge], [b.lat, b.lng]]);
        }
        L.polyline(line, { className: 'map-route', weight: 1.8, dashArray: '5 7', opacity: .8, interactive: false }).addTo(routes);
      }
    }
    $('#fit-footprints').disabled = !visible.length;
  }

  function filter() {
    const query = $('#gallery-search').value.trim().toLocaleLowerCase();
    const year = $('#gallery-year').value;
    visible = journals.filter(note => (!year || note.date.startsWith(year)) &&
      (scope === 'all' || note.place.country === scope) &&
      (!query || note.search.toLocaleLowerCase().includes(query)));
    const ids = new Set(visible.map(note => note.id));
    cards.forEach(card => { card.hidden = !ids.has(card.dataset.journal); });
    $('#gallery-result').textContent = `${visible.length} 篇笔记 · 按最新时间排列`;
    $('.gallery-empty').hidden = visible.length > 0;
    document.querySelectorAll('[data-scope]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.scope === scope)));
    updateMap();
  }
  document.querySelectorAll('[data-scope]').forEach(button => button.addEventListener('click', () => {
    scope = button.dataset.scope;
    filter();
    syncMapToCountry();
  }));
  $('#gallery-search').addEventListener('input', filter);
  $('#gallery-year').addEventListener('change', filter);
  $('#gallery-reset').addEventListener('click', () => {
    scope = 'all';
    $('#gallery-search').value = $('#gallery-year').value = '';
    filter();
    syncMapToCountry();
  });
  $('.gallery-filters').hidden = false;
  $('#gallery-reset').hidden = false;
  $('#show-route').addEventListener('change', updateMap);

  async function initializeMap() {
    if (!window.L) { status.textContent = '地图组件未能加载，仍可通过卡片阅读笔记。'; return; }
    status.textContent = '正在准备足迹地图…';
    map = L.map('footprint-map', { scrollWheelZoom: false, minZoom: 0, maxZoom: 10, zoomSnap: .25,
      maxBounds: [[-85, -200], [85, 200]], maxBoundsViscosity: .8, attributionControl: true });
    map.attributionControl.setPrefix('<a href="https://leafletjs.com/">Leaflet</a>');
    map.attributionControl.addAttribution('<a href="https://www.naturalearthdata.com/">Natural Earth</a>');
    map.createPane('land');
    map.getPane('land').style.zIndex = 200;
    map.createPane('grid');
    map.getPane('grid').style.zIndex = 210;
    for (let lat = -60; lat <= 60; lat += 30) L.polyline([[lat, -180], [lat, 180]], { pane: 'grid', className: 'map-grid', weight: 1, interactive: false }).addTo(map);
    for (let lng = -180; lng <= 180; lng += 30) L.polyline([[-80, lng], [80, lng]], { pane: 'grid', className: 'map-grid', weight: 1, interactive: false }).addTo(map);
    routes = L.layerGroup().addTo(map);
    points = L.featureGroup().addTo(map);
    syncMapToCountry();
    updateMap();
    const requested = byId.get(new URLSearchParams(location.search).get('place'));
    if (requested) {
      scope = requested.place.country;
      filter();
      syncMapToCountry();
    }
    $('.map-toolbar').hidden = false;
    $('#fit-footprints').addEventListener('click', () => {
      if (visible.length) map.fitBounds(points.getBounds(), { padding: [40, 40], maxZoom: 5, animate: motion });
    });
    new ResizeObserver(() => { map.invalidateSize(); }).observe($('#footprint-map'));
    try {
      const response = await fetch('../assets/maps/world.geojson');
      if (!response.ok) throw new Error('Map data unavailable');
      overview = L.geoJSON(await response.json(), {
        pane: 'land', interactive: false, style: { className: 'map-land' },
        onEachFeature(feature, layer) {
          const code = feature.properties.ISO_A2_EH || feature.properties.ISO_A2;
          if (!code || code.length !== 2) return;
          const bounds = countryBounds.get(code);
          if (bounds) bounds.extend(layer.getBounds());
          else countryBounds.set(code, layer.getBounds());
          const layers = overviewCountries.get(code) || [];
          layers.push(layer);
          overviewCountries.set(code, layers);
        }
      }).addTo(map);
    } catch {
      status.textContent = '地图底图暂时无法加载；足迹点仍可使用。刷新页面可重试。';
    }
    overviewSettled = true;
    // Apply the latest selection after loading, including clicks made while fetching.
    syncMapToCountry();
  }
  filter();
  initializeMap();
})();
