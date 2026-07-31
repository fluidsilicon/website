/* ==========================================================================
   Fabriq — site behaviour
   No dependencies. Every block guards for its own markup, so the same file
   can be dropped on every page.
   ========================================================================== */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------------------------------------------------
     Header: mega menu + mobile drawer
     ------------------------------------------------------------------------ */
  function initNav() {
    var nav = document.querySelector('[data-nav]');
    var burger = document.querySelector('[data-burger]');
    if (!nav) return;

    var items = Array.prototype.slice.call(nav.querySelectorAll('[data-mega-item]'));
    var desktop = window.matchMedia('(min-width: 1024px)');
    var hoverTimer;

    function close(item) {
      item.classList.remove('is-open');
      var btn = item.querySelector('.nav__link');
      if (btn) btn.setAttribute('aria-expanded', 'false');
    }
    function closeAll(except) {
      items.forEach(function (i) { if (i !== except) close(i); });
    }
    function open(item) {
      closeAll(item);
      item.classList.add('is-open');
      var btn = item.querySelector('.nav__link');
      if (btn) btn.setAttribute('aria-expanded', 'true');
    }

    items.forEach(function (item) {
      var btn = item.querySelector('.nav__link');
      if (!btn) return;

      btn.addEventListener('click', function (e) {
        e.preventDefault();
        item.classList.contains('is-open') ? close(item) : open(item);
      });

      // Hover only where there is a real pointer and room for the panel.
      item.addEventListener('mouseenter', function () {
        if (!desktop.matches || !window.matchMedia('(hover: hover)').matches) return;
        clearTimeout(hoverTimer);
        open(item);
      });
      item.addEventListener('mouseleave', function () {
        if (!desktop.matches || !window.matchMedia('(hover: hover)').matches) return;
        hoverTimer = setTimeout(function () { close(item); }, 180);
      });
    });

    // Click-away and Escape.
    document.addEventListener('click', function (e) {
      if (!e.target.closest('[data-nav]') && !e.target.closest('[data-burger]')) closeAll();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      closeAll();
      if (nav.classList.contains('is-open') && burger) burger.click();
    });

    // Mobile drawer
    if (burger) {
      burger.addEventListener('click', function () {
        var open = nav.classList.toggle('is-open');
        burger.setAttribute('aria-expanded', String(open));
        burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
        document.body.style.overflow = open ? 'hidden' : '';
        if (!open) closeAll();
      });
    }

    // Reset state when crossing the breakpoint.
    desktop.addEventListener('change', function () {
      closeAll();
      nav.classList.remove('is-open');
      document.body.style.overflow = '';
      if (burger) burger.setAttribute('aria-expanded', 'false');
    });
  }

  /* ------------------------------------------------------------------------
     Tabs (industries)
     ------------------------------------------------------------------------ */
  function initTabs() {
    document.querySelectorAll('[data-tabs]').forEach(function (root) {
      var tabs = Array.prototype.slice.call(root.querySelectorAll('[role="tab"]'));
      if (!tabs.length) return;

      function select(tab) {
        tabs.forEach(function (t) {
          var on = t === tab;
          t.setAttribute('aria-selected', String(on));
          t.tabIndex = on ? 0 : -1;
          var panel = document.getElementById(t.getAttribute('aria-controls'));
          if (panel) panel.hidden = !on;
        });
      }

      tabs.forEach(function (tab, i) {
        tab.addEventListener('click', function () { select(tab); });
        tab.addEventListener('keydown', function (e) {
          var next = null;
          if (e.key === 'ArrowRight') next = tabs[(i + 1) % tabs.length];
          if (e.key === 'ArrowLeft') next = tabs[(i - 1 + tabs.length) % tabs.length];
          if (e.key === 'Home') next = tabs[0];
          if (e.key === 'End') next = tabs[tabs.length - 1];
          if (!next) return;
          e.preventDefault();
          select(next);
          next.focus();
        });
      });
    });
  }

  /* ------------------------------------------------------------------------
     Scroll reveals
     ------------------------------------------------------------------------ */
  function initReveals() {
    var els = document.querySelectorAll('[data-reveal]');
    if (!els.length) return;
    if (reduceMotion || !('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });

    els.forEach(function (el, i) {
      // Stagger siblings only — a long page shouldn't accumulate delay.
      var sibs = el.parentElement ? el.parentElement.querySelectorAll(':scope > [data-reveal]') : [];
      var idx = Array.prototype.indexOf.call(sibs, el);
      el.style.setProperty('--d', Math.min(idx < 0 ? 0 : idx, 5) * 70 + 'ms');
      io.observe(el);
    });
  }

  /* ------------------------------------------------------------------------
     The floorplan.
     Draws a device view: a column-typed fabric grid, a placed design shown as
     utilisation heat, and a telemetry sweep that reads it. The sweep is one
     masked gradient rather than 700 animated nodes, so it stays cheap.
     ------------------------------------------------------------------------ */
  function initFloorplan() {
    var svg = document.querySelector('[data-floorplan]');
    if (!svg) return;

    var W = 660, H = 420;
    var COLS = 46, ROWS = 26, GAP = 1.6;
    var cw = W / COLS, ch = H / ROWS;

    // Deterministic noise so the layout is identical on every load.
    function rnd(x, y) {
      var n = Math.sin(x * 127.1 + y * 311.7) * 43758.5453;
      return n - Math.floor(n);
    }

    function colType(c) {
      if (c === 0 || c === COLS - 1) return 'io';
      if (c % 11 === 5) return 'bram';
      if (c % 17 === 9) return 'dsp';
      return 'clb';
    }
    var BASE = { clb: '#212129', bram: '#2B2B37', dsp: '#343442', io: '#17171D' };

    // Two placed blocks: where the design actually lives.
    var regions = [
      { cx: 0.34, cy: 0.42, rx: 0.24, ry: 0.30 },
      { cx: 0.73, cy: 0.66, rx: 0.16, ry: 0.22 }
    ];
    function heat(c, r) {
      var x = c / COLS, y = r / ROWS, best = 0;
      regions.forEach(function (g) {
        var d = Math.hypot((x - g.cx) / g.rx, (y - g.cy) / g.ry);
        best = Math.max(best, 1 - d);
      });
      if (best <= 0) return 0;
      return Math.max(0, Math.min(1, best * 1.15 - rnd(c, r) * 0.5));
    }

    var base = [], mask = [];
    for (var r = 0; r < ROWS; r++) {
      for (var c = 0; c < COLS; c++) {
        var x = (c * cw + GAP / 2).toFixed(2);
        var y = (r * ch + GAP / 2).toFixed(2);
        var w = (cw - GAP).toFixed(2);
        var h = (ch - GAP).toFixed(2);
        var t = colType(c);
        var u = heat(c, r);
        var fill = BASE[t];
        var op = 1;
        if (u > 0.08) { fill = '#B8410E'; op = (0.2 + u * 0.7).toFixed(2); }
        base.push('<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h +
                  '" rx="0.5" fill="' + fill + '" opacity="' + op + '"/>');
        mask.push('<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h +
                  '" rx="0.5" fill="#fff"/>');
      }
    }

    // Interconnect: a few routed channels crossing the placed region.
    var routes = '';
    [6, 12, 19].forEach(function (row, i) {
      var y = (row * ch + ch / 2).toFixed(1);
      var x1 = (4 * cw).toFixed(1), x2 = ((26 + i * 5) * cw).toFixed(1);
      routes += '<path d="M' + x1 + ' ' + y + ' H' + x2 + '" stroke="#F0752A" stroke-opacity="0.5" stroke-width="0.9"/>';
    });

    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.innerHTML =
      '<defs>' +
        '<mask id="fpMask"><rect width="' + W + '" height="' + H + '" fill="#000"/>' + mask.join('') + '</mask>' +
        '<linearGradient id="fpSweep" x1="0" y1="0" x2="1" y2="0">' +
          '<stop offset="0"    stop-color="#F0752A" stop-opacity="0"/>' +
          '<stop offset="0.55" stop-color="#F0752A" stop-opacity="0.55"/>' +
          '<stop offset="0.92" stop-color="#FFD2AE" stop-opacity="0.95"/>' +
          '<stop offset="1"    stop-color="#FFFFFF" stop-opacity="0"/>' +
        '</linearGradient>' +
      '</defs>' +
      '<rect width="' + W + '" height="' + H + '" fill="#0B0B0E"/>' +
      '<g>' + base.join('') + '</g>' +
      '<g opacity="0.9">' + routes + '</g>' +
      '<g mask="url(#fpMask)" class="fp-sweep">' +
        '<rect class="fp-sweep__bar" x="' + (-W * 0.35) + '" y="0" width="' + (W * 0.35) + '" height="' + H + '" fill="url(#fpSweep)"/>' +
      '</g>';

    if (reduceMotion) {
      var bar = svg.querySelector('.fp-sweep__bar');
      if (bar) bar.setAttribute('x', String(W * 0.28));
      return;
    }

    // Sweep + readout, driven by one rAF loop.
    var barEl = svg.querySelector('.fp-sweep__bar');
    var outs = document.querySelectorAll('[data-readout]');
    var start = null, PERIOD = 5200;

    function frame(ts) {
      if (start === null) start = ts;
      var p = ((ts - start) % PERIOD) / PERIOD;
      barEl.setAttribute('x', (-W * 0.35 + p * (W * 1.35)).toFixed(1));

      outs.forEach(function (el) {
        var kind = el.getAttribute('data-readout');
        var phase = p * Math.PI * 2;
        if (kind === 'slack') el.textContent = (0.182 + Math.sin(phase) * 0.026).toFixed(3) + ' ns';
        if (kind === 'temp')  el.textContent = (61.4 + Math.sin(phase + 1.1) * 2.2).toFixed(1) + ' °C';
        if (kind === 'power') el.textContent = (14.7 + Math.sin(phase + 2.3) * 0.6).toFixed(1) + ' W';
        if (kind === 'tile')  el.textContent = 'X' + String(Math.floor(p * 46)).padStart(2, '0') +
                                               'Y' + String(Math.floor(8 + Math.abs(Math.sin(phase)) * 14)).padStart(2, '0');
      });
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  /* ------------------------------------------------------------------------
     Small utilities
     ------------------------------------------------------------------------ */
  function initYear() {
    document.querySelectorAll('[data-year]').forEach(function (el) {
      el.textContent = String(new Date().getFullYear());
    });
  }

  function initForm() {
    var form = document.querySelector('[data-demo-form]');
    if (!form) return;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var note = form.querySelector('[data-form-note]');
      if (note) {
        note.textContent = 'Not connected yet — point the form action at Formspree, HubSpot, or your own endpoint.';
        note.style.color = 'var(--burnt)';
      }
    });
  }

  function boot() {
    initNav();
    initTabs();
    initReveals();
    initFloorplan();
    initYear();
    initForm();
  }

  document.readyState === 'loading'
    ? document.addEventListener('DOMContentLoaded', boot)
    : boot();
})();
