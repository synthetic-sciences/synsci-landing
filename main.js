import { inject } from '@vercel/analytics';
inject();

function safePlay(video) {
  const playPromise = video.play();
  if (playPromise && typeof playPromise.catch === 'function') {
    playPromise.catch(() => {});
  }
}

function initModeVideos() {
  const cards = document.querySelectorAll('.mode-card');
  if (!cards.length) return;

  const modal = document.getElementById('videoModal');
  const modalPlayer = document.getElementById('videoModalPlayer');
  const modalTitle = document.getElementById('videoModalTitle');
  const closeEls = modal ? modal.querySelectorAll('[data-close-video]') : [];
  const closeBtn = modal ? modal.querySelector('.video-modal-close') : null;
  let lastTrigger = null;

  function resetPreview(video) {
    video.pause();
    if (video.currentTime > 0) video.currentTime = 0;
  }

  function closeModal() {
    if (!modal || modal.hidden || !modalPlayer) return;
    modal.hidden = true;
    document.body.classList.remove('modal-open');
    modalPlayer.pause();
    modalPlayer.removeAttribute('src');
    modalPlayer.load();
    if (lastTrigger) lastTrigger.focus();
  }

  function openModal(source, title, trigger) {
    if (!modal || !modalPlayer || !modalTitle || !source) return;
    lastTrigger = trigger;
    modal.hidden = false;
    document.body.classList.add('modal-open');
    modalTitle.textContent = title;
    modalPlayer.setAttribute('src', source);
    modalPlayer.currentTime = 0;
    safePlay(modalPlayer);
    if (closeBtn) closeBtn.focus();
  }

  cards.forEach(card => {
    const preview = card.querySelector('.agent-preview-video');
    const trigger = card.querySelector('.agent-media-trigger');
    if (!preview || !trigger) return;

    preview.muted = true;
    preview.playsInline = true;
    preview.preload = 'auto';
    preview.load();

    const startPreview = () => {
      if (preview.readyState >= 2) {
        safePlay(preview);
        return;
      }
      const handleLoaded = () => safePlay(preview);
      preview.addEventListener('loadeddata', handleLoaded, { once: true });
      preview.load();
    };
    const stopPreview = () => resetPreview(preview);

    trigger.addEventListener('pointerenter', startPreview);
    trigger.addEventListener('pointerleave', stopPreview);
    card.addEventListener('focusin', startPreview);
    card.addEventListener('focusout', event => {
      if (!card.contains(event.relatedTarget)) stopPreview();
    });

    trigger.addEventListener('click', () => {
      const source = card.dataset.videoSrc;
      const title = card.dataset.videoTitle || 'Mode Demo';
      stopPreview();
      openModal(source, title, trigger);
    });
  });

  closeEls.forEach(el => el.addEventListener('click', closeModal));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') closeModal();
  });
}

// ── Scroll reveal ──
function initReveal() {
  const targets = [
    '.section-hdr', '.hero-top', '.hero-mockup-wrapper',
    '.mode-card', '.showcase-inner',
    '.runtime-card', '.sleep-monitor',
    '.isg-card',
    '.pricing-card',
    '.footer-brand'
  ];
  const els = document.querySelectorAll(targets.join(','));
  els.forEach(el => el.classList.add('reveal'));
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) e.target.classList.add('visible');
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });
  els.forEach(el => obs.observe(el));
}

// ── Smooth scroll ──
function initScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      e.preventDefault();
      const t = document.querySelector(a.getAttribute('href'));
      if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
}

// ── Dynamic section transitions ──
function initDynamicTransitions() {
  const transitionBars = document.querySelectorAll('.section-transition span');
  const showcaseArts = document.querySelectorAll('.showcase-art');
  if (!transitionBars.length && !showcaseArts.length) return;

  let rafId = 0;

  const update = () => {
    rafId = 0;
    const viewportHeight = window.innerHeight || 1;

    transitionBars.forEach(bar => {
      const rect = bar.getBoundingClientRect();
      const center = rect.top + rect.height / 2;
      const distance = Math.abs(center - viewportHeight / 2);
      const intensity = Math.max(0, 1 - distance / (viewportHeight * 0.65));
      const shift = -42 + intensity * 84;
      bar.style.setProperty('--transition-shift', `${shift.toFixed(2)}%`);
      bar.style.setProperty('--transition-alpha', (0.12 + intensity * 0.24).toFixed(2));
    });

    showcaseArts.forEach(art => {
      const section = art.closest('.showcase');
      if (!section) return;
      const rect = section.getBoundingClientRect();
      const sectionDelta = rect.top + rect.height / 2 - viewportHeight / 2;
      const shift = Math.max(-42, Math.min(42, sectionDelta * -0.08));
      art.style.setProperty('--art-shift', `${shift.toFixed(2)}px`);
    });
  };

  const requestUpdate = () => {
    if (!rafId) rafId = requestAnimationFrame(update);
  };

  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', requestUpdate);
  requestUpdate();
}

// ── Copy command ──
window.copyCmd = function(btn, text) {
  navigator.clipboard.writeText(text);
  const prev = btn.innerHTML;
  btn.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>';
  btn.style.color = 'var(--forest)';
  setTimeout(() => { btn.innerHTML = prev; btn.style.color = ''; }, 1200);
};

// ── Init ──
document.addEventListener('DOMContentLoaded', () => {
  initReveal();
  initScroll();
  initDynamicTransitions();
  initModeVideos();
});
