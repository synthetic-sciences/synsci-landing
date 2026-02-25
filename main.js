// ── Terminal animation ──
function initTerminal() {
  const term = document.getElementById('term');
  if (!term) return;

  let stopped = false;
  const cursor = () => '<span class="term-cursor"></span>';

  function clear() { term.innerHTML = ''; }

  function typeText(text, speed = 15) {
    return new Promise(resolve => {
      let i = 0;
      const el = document.createElement('span');
      term.appendChild(el);
      function tick() {
        if (stopped) return resolve();
        if (i < text.length) {
          el.innerHTML = text.slice(0, i + 1) + cursor();
          i++;
          setTimeout(tick, speed + Math.random() * 8);
        } else {
          el.innerHTML = text;
          resolve();
        }
      }
      tick();
    });
  }

  function addLine(html) {
    const div = document.createElement('div');
    div.innerHTML = html;
    term.appendChild(div);
  }

  function pause(ms) {
    return new Promise(r => setTimeout(r, ms));
  }

  async function play() {
    clear();

    // step 1: npm install
    await typeText('<span class="t-prompt">~ $</span> <span class="t-cmd">npm i -g @synsci/cli</span>', 18);
    await pause(250);
    addLine('');
    addLine('<span class="t-dim">added 1 package in 3s</span>');
    await pause(150);
    addLine('<span class="t-green">&#10003;</span> <span class="t-dim">installed</span> @synsci/cli@1.1.80');
    await pause(300);
    addLine('');

    // step 2: connect login
    await typeText('<span class="t-prompt">~ $</span> <span class="t-cmd">synsc connect login</span>', 18);
    await pause(250);
    addLine('');
    addLine('<span class="t-dim">opening browser...</span>');
    await pause(200);
    addLine('<span class="t-green">&#10003;</span> <span class="t-dim">authenticated via github as</span> <span class="t-cyan">researcher@lab</span>');
    await pause(150);
    addLine('<span class="t-green">&#10003;</span> <span class="t-dim">credentials synced:</span> <span class="t-cyan">tinker</span> <span class="t-dim">·</span> <span class="t-cyan">huggingface</span> <span class="t-dim">·</span> <span class="t-cyan">modal</span>');
    await pause(300);
    addLine('');

    // step 3: synsc
    await typeText('<span class="t-prompt">~ $</span> <span class="t-cmd">synsc</span>', 22);
    await pause(200);
    addLine('');
    addLine('<span class="t-dim">synthetic sciences cli v1.1.80</span>');
    await pause(100);
    addLine('<span class="t-green">&#10003;</span> <span class="t-dim">agent:</span> <span class="t-coral">research</span> <span class="t-dim">· model:</span> claude sonnet 4.5');
    await pause(100);
    addLine('<span class="t-green">&#10003;</span> <span class="t-dim">skills loaded:</span> 93');
    await pause(200);
    addLine('');
    addLine('<span class="t-prompt">&gt;</span> ' + cursor());
    // animation complete — stays as final state, no loop
  }

  // start when visible
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        stopped = false;
        play();
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.3 });

  obs.observe(term);
}

// ── Scroll reveal ──
function initReveal() {
  const targets = [
    '.section-hdr', '.hero-top', '.hero-mockup',
    '.agent-featured', '.agent-card', '.showcase-inner',
    '.cloud-card',
    '.ib-card',
    '.pricing-card',
    '.footer-hero'
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
  initTerminal();
});
