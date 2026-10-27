/* Shared by standalone journals and dynamically inserted reading dialogs. */
(() => {
  function initialize(carousel) {
    if (carousel.dataset.carouselReady) return () => {};
    const viewport = carousel.querySelector('.carousel-viewport');
    const slides = [...viewport.children];
    if (!slides.length) return () => {};
    const previous = carousel.querySelector('.carousel-prev');
    const next = carousel.querySelector('.carousel-next');
    const counter = carousel.querySelector('.carousel-counter');
    const dots = carousel.querySelector('.carousel-dots');
    const controller = new AbortController();
    const options = { signal: controller.signal };
    let active = 0;
    let frame;

    const update = index => {
      active = Math.max(0, Math.min(slides.length - 1, index));
      previous.disabled = active === 0;
      next.disabled = active === slides.length - 1;
      counter.textContent = `${active + 1} / ${slides.length}`;
      slides.forEach((slide, i) => {
        const selected = i === active;
        // Keep offscreen image links out of the keyboard and screen-reader order.
        if (!selected && slide.contains(document.activeElement)) viewport.focus({ preventScroll: true });
        slide.inert = !selected;
        slide.setAttribute('aria-hidden', String(!selected));
        if (selected) slide.querySelector('img').loading = 'eager';
      });
      [...dots.children].forEach((dot, i) => dot.setAttribute('aria-pressed', String(i === active)));
    };
    const go = index => {
      update(index);
      viewport.scrollTo({ left: active * viewport.clientWidth, behavior: 'instant' });
    };
    dots.replaceChildren();
    slides.forEach((slide, index) => {
      slide.setAttribute('role', 'group');
      slide.setAttribute('aria-label', `第 ${index + 1} 张，共 ${slides.length} 张`);
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.setAttribute('aria-label', `查看第 ${index + 1} 张图片`);
      dot.addEventListener('click', () => go(index), options);
      dots.append(dot);
    });
    previous.addEventListener('click', () => go(active - 1), options);
    next.addEventListener('click', () => go(active + 1), options);
    carousel.addEventListener('keydown', event => {
      if (event.altKey || event.ctrlKey || event.metaKey || !['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      go(event.key === 'Home' ? 0 : event.key === 'End' ? slides.length - 1 : active + (event.key === 'ArrowRight' ? 1 : -1));
    }, options);
    viewport.addEventListener('scroll', () => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        if (viewport.clientWidth) update(Math.round(viewport.scrollLeft / viewport.clientWidth));
      });
    }, { ...options, passive: true });
    // Retain the current image across viewport resize or phone rotation.
    const resize = new ResizeObserver(() => go(active));
    resize.observe(viewport);
    carousel.dataset.carouselReady = 'true';
    previous.hidden = next.hidden = dots.hidden = slides.length < 2;
    counter.hidden = false;
    go(0);
    return () => {
      controller.abort();
      resize.disconnect();
      cancelAnimationFrame(frame);
      delete carousel.dataset.carouselReady;
      slides.forEach(slide => { slide.inert = false; slide.removeAttribute('aria-hidden'); });
      previous.hidden = next.hidden = dots.hidden = counter.hidden = true;
    };
  }

  window.GalleryCarousel = {
    init(root) {
      const cleanups = [...root.querySelectorAll('[data-carousel]')].map(initialize);
      return () => cleanups.forEach(cleanup => cleanup());
    }
  };
  window.GalleryCarousel.init(document);
})();
