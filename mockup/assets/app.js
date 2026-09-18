/* ==========================================================================
   Skewer & Slice — interactions
   1. Ember particle field (the "flame" motion layer)
   2. Intro sequence: logo in, buttons in, auto-exit at ~5.5s
   3. Sticky Order Online bar
   4. Mobile nav + scroll reveals
   ========================================================================== */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------------------------------------------
     1. Ember field
        Drifting sparks rising off an open flame. Runs on every
        <canvas class="embers__canvas">. Pauses when off-screen or when
        the tab is hidden so it never burns battery needlessly.
     ------------------------------------------------------------------ */
  function EmberField(canvas) {
    var ctx = canvas.getContext('2d');
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = 0, h = 0, parts = [], raf = null, visible = true;

    var density = canvas.dataset.density === 'high' ? 0.00016 : 0.00009;

    function resize() {
      var r = canvas.getBoundingClientRect();
      w = Math.max(r.width, 1);
      h = Math.max(r.height, 1);
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      build();
    }

    function spark(seed) {
      return {
        x: Math.random() * w,
        y: seed ? Math.random() * h : h + Math.random() * 40,
        r: 0.6 + Math.random() * 2.1,
        vy: 0.22 + Math.random() * 0.85,
        vx: (Math.random() - 0.5) * 0.36,
        life: 0,
        max: 150 + Math.random() * 260,
        hue: 18 + Math.random() * 26,
        sway: Math.random() * Math.PI * 2
      };
    }

    function build() {
      var n = Math.round(w * h * density);
      n = Math.max(24, Math.min(n, 190));
      parts = [];
      for (var i = 0; i < n; i++) parts.push(spark(true));
    }

    function frame() {
      ctx.clearRect(0, 0, w, h);
      ctx.globalCompositeOperation = 'lighter';

      for (var i = 0; i < parts.length; i++) {
        var p = parts[i];
        p.life++;
        p.sway += 0.014;
        p.y -= p.vy;
        p.x += p.vx + Math.sin(p.sway) * 0.34;

        if (p.life > p.max || p.y < -12) parts[i] = spark(false);

        var t = p.life / p.max;
        var a = t < 0.14 ? t / 0.14 : 1 - (t - 0.14) / 0.86;
        a = Math.max(0, Math.min(a, 1)) * 0.92;

        var g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 4.2);
        g.addColorStop(0, 'hsla(' + p.hue + ',100%,72%,' + a + ')');
        g.addColorStop(0.35, 'hsla(' + p.hue + ',100%,52%,' + (a * 0.55) + ')');
        g.addColorStop(1, 'hsla(' + p.hue + ',100%,44%,0)');
        ctx.fillStyle = g;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r * 4.2, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.globalCompositeOperation = 'source-over';
      raf = requestAnimationFrame(frame);
    }

    function start() { if (!raf && visible && !document.hidden) raf = requestAnimationFrame(frame); }
    function stop() { if (raf) { cancelAnimationFrame(raf); raf = null; } }

    resize();
    window.addEventListener('resize', debounce(resize, 180));
    document.addEventListener('visibilitychange', function () {
      document.hidden ? stop() : start();
    });

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        visible = entries[0].isIntersecting;
        visible ? start() : stop();
      }, { threshold: 0 }).observe(canvas);
    }

    if (reduced) {
      // Draw a single still frame instead of animating.
      for (var k = 0; k < 40; k++) { parts.forEach(function (p) { p.life++; }); }
      ctx.clearRect(0, 0, w, h);
      return;
    }
    start();
  }

  function debounce(fn, ms) {
    var t;
    return function () { clearTimeout(t); t = setTimeout(fn, ms); };
  }

  document.querySelectorAll('.embers__canvas').forEach(EmberField);

  /* ------------------------------------------------------------------
     2. Intro
        Shows once per browser session, so returning visitors and anyone
        clicking through from the menu are never made to sit through it.
     ------------------------------------------------------------------ */
  var intro = document.getElementById('intro');
  if (intro) {
    var SEEN = 'sns_intro_seen';
    var seen = false;
    try { seen = sessionStorage.getItem(SEEN) === '1'; } catch (e) { /* private mode */ }

    if (seen || reduced) {
      intro.remove();
      document.body.classList.remove('intro-lock');
    } else {
      document.body.classList.add('intro-lock');
      var timer = setTimeout(closeIntro, 5500);   // ~5.5s, matches the progress bar

      function closeIntro() {
        clearTimeout(timer);
        intro.classList.add('is-out');
        document.body.classList.remove('intro-lock');
        try { sessionStorage.setItem(SEEN, '1'); } catch (e) {}
        setTimeout(function () { if (intro && intro.parentNode) intro.remove(); }, 800);
      }

      var skip = intro.querySelector('.intro__skip');
      if (skip) skip.addEventListener('click', closeIntro);

      // Following either button should dismiss the intro, not fight it.
      intro.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', function () {
          try { sessionStorage.setItem(SEEN, '1'); } catch (e) {}
        });
      });

      document.addEventListener('keydown', function onEsc(e) {
        if (e.key === 'Escape') { closeIntro(); document.removeEventListener('keydown', onEsc); }
      });
    }
  }

  /* ------------------------------------------------------------------
     3. Sticky Order Online bar
        Appears after the hero scrolls away. It sits below the content,
        never over it, and there is no dismiss-me popup anywhere.
     ------------------------------------------------------------------ */
  var bar = document.getElementById('orderbar');
  if (bar) {
    var trigger = document.querySelector('.hero, .pagehead');
    var showAfter = function () {
      return trigger ? trigger.offsetHeight * 0.6 : 420;
    };
    var onScroll = function () {
      bar.classList.toggle('is-in', window.scrollY > showAfter());
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ------------------------------------------------------------------
     4. Mobile nav
     ------------------------------------------------------------------ */
  var burger = document.querySelector('.burger');
  var nav = document.getElementById('nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        nav.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ------------------------------------------------------------------
     4b. Ribbon "Pause motion"
     ------------------------------------------------------------------ */
  var ribbon = document.getElementById('ribbon');
  var ribbonBtn = document.querySelector('[data-ribbon-toggle]');
  if (ribbon && ribbonBtn) {
    var label = ribbonBtn.querySelector('[data-ribbon-label]');
    if (reduced) {
      ribbon.classList.add('is-paused');
      ribbonBtn.setAttribute('aria-pressed', 'true');
      if (label) label.textContent = 'Play motion';
    }
    ribbonBtn.addEventListener('click', function () {
      var paused = ribbon.classList.toggle('is-paused');
      ribbonBtn.setAttribute('aria-pressed', paused ? 'true' : 'false');
      if (label) label.textContent = paused ? 'Play motion' : 'Pause motion';
    });
  }

  /* ------------------------------------------------------------------
     4c. Menu category filter
         Replaces the live site's jump-anchor bar. Filtering happens in
         place, so nobody loses their scroll position.
     ------------------------------------------------------------------ */
  var chips = document.querySelectorAll('.chip[data-filter]');
  var grid = document.getElementById('dishGrid');
  if (chips.length && grid) {
    var dishes = grid.querySelectorAll('.dish');
    var empty = document.getElementById('dishEmpty');

    var apply = function (cat) {
      var shown = 0;
      dishes.forEach(function (d) {
        var match = cat === 'All' || d.getAttribute('data-cat') === cat;
        d.hidden = !match;
        if (match) { shown++; d.classList.add('is-in'); }
      });
      if (empty) empty.hidden = shown !== 0;
    };

    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        chips.forEach(function (c) { c.setAttribute('aria-pressed', 'false'); });
        chip.setAttribute('aria-pressed', 'true');
        apply(chip.getAttribute('data-filter'));
      });
    });
  }

  /* ------------------------------------------------------------------
     5. Scroll reveals
     ------------------------------------------------------------------ */
  var reveals = document.querySelectorAll('.reveal');
  if (reveals.length) {
    if (!('IntersectionObserver' in window) || reduced) {
      reveals.forEach(function (el) { el.classList.add('is-in'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
      reveals.forEach(function (el) { io.observe(el); });
    }
  }

  /* ------------------------------------------------------------------
     6. Year stamp
     ------------------------------------------------------------------ */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
