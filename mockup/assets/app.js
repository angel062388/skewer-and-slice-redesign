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
  var introOpen = false;                 // the hero sequence waits for this
  if (intro) {
    var SEEN = 'sns_intro_seen';
    var seen = false;
    try { seen = sessionStorage.getItem(SEEN) === '1'; } catch (e) { /* private mode */ }

    if (seen || reduced) {
      intro.remove();
      document.body.classList.remove('intro-lock');
    } else {
      introOpen = true;
      document.body.classList.add('intro-lock');
      var timer = setTimeout(closeIntro, 5500);   // ~5.5s, matches the progress bar
      var closed = false;

      function closeIntro() {
        if (closed) return;                        // timer, Skip and Esc can all call this
        closed = true;
        clearTimeout(timer);
        intro.classList.add('is-out');
        document.body.classList.remove('intro-lock');
        try { sessionStorage.setItem(SEEN, '1'); } catch (e) {}
        setTimeout(function () { if (intro && intro.parentNode) intro.remove(); }, 800);
        // let the hero start as the overlay is fading, not before
        setTimeout(function () {
          introOpen = false;
          document.dispatchEvent(new CustomEvent('sns:intro-done'));
        }, 450);
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
     3. Hero food sequence
        Each dish enters from the left, grows large at the centre of the
        hero for a beat, then travels to its resting spot on the right.
        Strictly one after the other: BBQ plate first, then the pizza.
        Distances are measured at runtime so "the centre" is the real
        centre on every screen. Waits for the intro to leave.
     ------------------------------------------------------------------ */
  var stage = document.querySelector('.hero__stage');
  var foods = stage ? [].slice.call(stage.querySelectorAll('.hero__food')) : [];

  // switches on the headline's underline and colour-warm animations
  var lightHero = function () {
    var h = stage && stage.closest('.hero');
    if (h) h.classList.add('is-on');
  };

  if (foods.length && 'animate' in Element.prototype && !reduced) {
    var DURATION = 2100;      // one dish, ms
    var GAP = 150;            // breath between dishes
    var FIRST_DELAY = 250;

    var flyIn = function (el, delay) {
      var hero = el.closest('.hero').getBoundingClientRect();
      var box = el.getBoundingClientRect();              // resting spot, no transform yet
      var vw = document.documentElement.clientWidth;      // excludes the scrollbar
      var toCenterX = vw / 2 - (box.left + box.width / 2);
      var toCenterY = (hero.top + hero.height / 2) - (box.top + box.height / 2);
      var startX = -(box.left + box.width + 80);          // fully off the left edge
      var maxZoom = (vw - 40) / box.width;                // never wider than the screen
      var zoom = Math.min(vw < 700 ? 1.3 : 1.5, maxZoom);

      var at = function (x, y, s, r) {
        return 'translate(' + x + 'px, ' + y + 'px) scale(' + s + ') rotate(' + r + 'deg)';
      };

      var anim = el.animate([
        { transform: at(startX, 30, 0.5, -110), opacity: 0, offset: 0,
          easing: 'cubic-bezier(.2,.75,.25,1)' },                      // swoop in, slow into centre
        { opacity: 1, offset: 0.1 },
        { transform: at(toCenterX, toCenterY, zoom, 0), offset: 0.4,
          easing: 'ease-in-out' },                                     // arrive big and upright
        { transform: at(toCenterX, toCenterY - 8, zoom + 0.04, 2), offset: 0.62,
          easing: 'cubic-bezier(.55,.05,.35,1)' },                     // hold, then travel right
        { transform: at(0, 0, 1, 0), opacity: 1, offset: 1 }
      ], { duration: DURATION, delay: delay, fill: 'forwards' });

      var settle = function () {
        try { anim.commitStyles(); anim.cancel(); }
        catch (e) { el.style.opacity = '1'; el.style.transform = 'none'; }
        el.classList.add('is-settled');                  // hand over to the CSS drift
      };
      // same promise the chaining uses, so "settled" and "next" always agree
      if (anim.finished && anim.finished.then) anim.finished.then(settle, function () {});
      else anim.onfinish = settle;
      return anim;
    };

    var showInPlace = function () {
      foods.forEach(function (el) { el.style.opacity = '1'; el.classList.add('is-settled'); });
    };

    var runSequence = function () {
      lightHero();
      var start = function (i, delay) {
        if (i >= foods.length) return;
        var a;
        try { a = flyIn(foods[i], delay); }
        catch (e) { showInPlace(); return; }          // never leave the hero empty
        var went = false;
        var next = function () { if (went) return; went = true; start(i + 1, GAP); };
        // "finished" waits until the tab is actually visible, which is what we
        // want: a page opened in a background tab still plays one-by-one.
        if (a.finished && a.finished.then) a.finished.then(next, function () {});
        else setTimeout(next, delay + DURATION);
      };
      start(0, FIRST_DELAY);
    };

    // measure only once layout is stable (web fonts can shift the hero).
    // A timer rather than requestAnimationFrame: rAF never fires in a hidden
    // tab, and getBoundingClientRect forces layout on its own anyway.
    var kick = function () {
      var fired = false;
      var go = function () {
        if (fired) return;
        fired = true;
        setTimeout(runSequence, 40);
      };
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(go);
      setTimeout(go, 900);
    };

    if (introOpen) document.addEventListener('sns:intro-done', kick, { once: true });
    else kick();
  } else {
    // no Web Animations support (or reduced motion): show the dishes in place
    lightHero();
    foods.forEach(function (el) { el.style.opacity = '1'; el.classList.add('is-settled'); });
  }

  /* ------------------------------------------------------------------
     3b. Sticky Order Online bar
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
     4d. Real fire behind the order band
         The restaurant's own YouTube clip (the same one the live site
         uses), loaded only when the band is near the viewport, muted and
         looping, sized to cover. The ember field stays underneath as the
         fallback for reduced motion, slow connections or blocked embeds.
     ------------------------------------------------------------------ */
  document.querySelectorAll('.firevideo[data-yt]').forEach(function (host) {
    if (reduced) return;
    var id = host.getAttribute('data-yt');
    var frame = null;

    var size = function () {
      if (!frame) return;
      var w = host.clientWidth, h = host.clientHeight;
      var cover = 1.18;                       // hides YouTube's letterbox and edge chrome
      var fw, fh;
      if (w / h > 16 / 9) { fw = w * cover; fh = fw * 9 / 16; }
      else { fh = h * cover; fw = fh * 16 / 9; }
      frame.style.width = Math.ceil(fw) + 'px';
      frame.style.height = Math.ceil(fh) + 'px';
    };

    var mount = function () {
      if (frame) return;
      frame = document.createElement('iframe');
      frame.title = 'Open flame';
      frame.setAttribute('aria-hidden', 'true');
      frame.setAttribute('tabindex', '-1');
      frame.setAttribute('allow', 'autoplay; encrypted-media');
      frame.src = 'https://www.youtube-nocookie.com/embed/' + id +
        '?autoplay=1&mute=1&loop=1&playlist=' + id +
        '&controls=0&rel=0&playsinline=1&disablekb=1&iv_load_policy=3&modestbranding=1';
      frame.addEventListener('load', function () {
        setTimeout(function () { host.classList.add('is-live'); }, 700);
      });
      host.appendChild(frame);
      size();
      window.addEventListener('resize', debounce(size, 150));
    };

    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting) { mount(); io.disconnect(); }
      }, { rootMargin: '500px 0px' });
      io.observe(host);
    } else {
      mount();
    }
  });

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
