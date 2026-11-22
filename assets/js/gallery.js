/* Journals remain ordinary, readable links when JavaScript is unavailable. */
(() => {
  const source = document.querySelector('#gallery-data');
  if (!source) return;
  const journals = JSON.parse(source.textContent);
  const mapConfig = JSON.parse(document.querySelector('#gallery-map-config').textContent);
  const byId = new Map(journals.map(note => [note.id, note]));
  const $ = selector => document.querySelector(selector);
  const cards = [...document.querySelectorAll('[data-journal]')];
  const motion = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let scope = 'all';
  let visible = journals;
  let map, points, routes, tiles;
  const countryBounds = new Map(Object.entries(mapConfig.country_bounds));
  let currentRequest;
  let opener;
  let cleanupCarousel = () => {};
  const dialog = $('.journal-dialog');
  const dialogContent = $('.dialog-content');
  const status = $('#map-status');
  const statusMessage = $('#map-status-message');
  const retryMap = $('#retry-map');

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
          map.setView([note.place.lat, note.place.lng], Math.min(14, mapConfig.max_zoom), { animate: motion });
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
    // Countries without a stored bounding box still have their journal coordinates.
    // Use all notes in the country so an empty search does not change its geographic scope.
    if (!bounds) {
      const locations = journals.filter(note => note.place.country === scope)
        .map(note => [note.place.lat, note.place.lng]);
      bounds = locations.length ? L.latLngBounds(locations) : world;
    }
    map.fitBounds(bounds, { padding: [24, 24], maxZoom: 6, animate: motion });
  }

  function setMapStatus(message, retry = false) {
    statusMessage.textContent = message;
    status.hidden = !message;
    retryMap.hidden = !retry;
  }

  function addOnlineMap() {
    const attribution = document.createElement('a');
    attribution.href = mapConfig.attribution_url;
    attribution.textContent = mapConfig.attribution_text;
    tiles = L.tileLayer(mapConfig.tile_url, {
      maxZoom: mapConfig.max_zoom, noWrap: true,
      bounds: [[-85.05112878, -180], [85.05112878, 180]],
      attribution: attribution.outerHTML,
      referrerPolicy: 'strict-origin-when-cross-origin',
      updateWhenIdle: true, updateWhenZooming: false, keepBuffer: 0
    });
    const states = new Map();
    let timeout;
    let slow = false;
    const refreshStatus = () => {
      const values = [...states.values()];
      if (!navigator.onLine) setMapStatus('网络已断开，足迹和笔记仍可查看。', true);
      else if (values.includes('error')) setMapStatus('部分地图未能加载，足迹和笔记仍可查看。', true);
      else if (slow && values.includes('pending')) setMapStatus('地图加载较慢，可稍后重试。', true);
      else if (values.includes('pending')) setMapStatus('正在加载在线地图…');
      else setMapStatus('');
    };
    tiles.on('loading', () => {
      slow = false;
      clearTimeout(timeout);
      setMapStatus('正在加载在线地图…');
      timeout = setTimeout(() => { slow = true; refreshStatus(); }, 15000);
    });
    tiles.on('tileloadstart', event => { states.set(event.tile, 'pending'); });
    for (const [eventName, state] of [['tileload', 'loaded'], ['tileerror', 'error']]) {
      tiles.on(eventName, event => {
        // Ignore events from tiles discarded by a retry or a newer viewport.
        if (!states.has(event.tile)) return;
        states.set(event.tile, state);
        refreshStatus();
      });
    }
    tiles.on('tileunload tileabort', event => {
      states.delete(event.tile);
      queueMicrotask(refreshStatus);
    });
    tiles.on('load', () => { clearTimeout(timeout); refreshStatus(); });
    const retry = () => {
      clearTimeout(timeout);
      slow = false;
      states.clear();
      tiles.redraw();
    };
    retryMap.addEventListener('click', retry);
    window.addEventListener('offline', refreshStatus);
    window.addEventListener('online', retry);
    // Browser caching remains enabled; only the visible viewport is requested.
    tiles.addTo(map);
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
          const date = document.createElement('time');
          date.dateTime = note.date;
          date.lang = 'en';
          date.textContent = note.displayDate;
          link.append(date, ` · ${note.title}`);
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
    fitCountry();
  }));
  $('#gallery-search').addEventListener('input', filter);
  $('#gallery-year').addEventListener('change', filter);
  $('#gallery-reset').addEventListener('click', () => {
    scope = 'all';
    $('#gallery-search').value = $('#gallery-year').value = '';
    filter();
    fitCountry();
  });
  $('.gallery-filters').hidden = false;
  $('#gallery-reset').hidden = false;
  $('#show-route').addEventListener('change', updateMap);

  function initializeMap() {
    if (!window.L) { setMapStatus('地图组件未能加载，仍可通过卡片阅读笔记。'); return; }
    setMapStatus('正在准备在线地图…');
    map = L.map('footprint-map', { scrollWheelZoom: false, minZoom: 0, maxZoom: mapConfig.max_zoom,
      maxBounds: [[-85.05112878, -180], [85.05112878, 180]], maxBoundsViscosity: .8,
      zoomAnimation: motion, fadeAnimation: motion, markerZoomAnimation: motion, attributionControl: true });
    map.attributionControl.setPrefix('<a href="https://leafletjs.com/">Leaflet</a>');
    L.control.scale({ imperial: false, updateWhenIdle: true }).addTo(map);
    routes = L.layerGroup().addTo(map);
    points = L.featureGroup().addTo(map);
    fitCountry();
    updateMap();
    const requested = byId.get(new URLSearchParams(location.search).get('place'));
    if (requested) {
      scope = requested.place.country;
      filter();
      map.setView([requested.place.lat, requested.place.lng], Math.min(14, mapConfig.max_zoom), { animate: false });
    }
    addOnlineMap();
    $('.map-toolbar').hidden = false;
    $('#fit-footprints').addEventListener('click', () => {
      if (visible.length) map.fitBounds(points.getBounds(), { padding: [40, 40], maxZoom: Math.min(14, mapConfig.max_zoom), animate: motion });
    });
    new ResizeObserver(() => { map.invalidateSize(); }).observe($('#footprint-map'));
  }
  filter();
  initializeMap();
})();
