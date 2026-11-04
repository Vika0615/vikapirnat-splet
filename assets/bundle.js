/* Vika Pirnat — vedenje komponent (brez knjižnic). window.VP:
   VP.problemMap(figure, data)  izriše zemljevid problema in ga pokaže v ~1 s, ko pride v pogled
   VP.lang(root)                preklop SLO / ENG za gumbe [data-set-lang] v root
   VP.theme(root, opts)         preklop Sistem / Svetla / Temna za gumbe [data-set-theme]; opts.follow = sledi brskalniku
   VP.copy(button, target)      kopira besedilo elementa target, ob zavrnitvi ga označi */
(function () {
  var VP = window.VP = window.VP || {};
  var NS = 'http://www.w3.org/2000/svg';

  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function bi(parent, attrs, sl, en) {
    el('text', Object.assign({ lang: 'sl' }, attrs), parent).textContent = sl;
    el('text', Object.assign({ lang: 'en' }, attrs), parent).textContent = en;
  }
  function seq(parent, t, cls) {
    var g = el('g', { 'class': 'seq' + (cls ? ' ' + cls : '') }, parent);
    g.style.setProperty('--t', t + 'ms');
    return g;
  }

  VP.problemMap = function (fig, data) {
    var svg = fig.querySelector('.vp-map__svg');
    if (!svg) return;
    var uid = fig.id || ('pm' + Math.floor(Math.random() * 1e6));
    var W = 1180, left = 210, right = 60;
    var days = data.days || 28, scale = data.firstWeekScale || 1;
    var unit = (W - left - right) / (days + 7 * (scale - 1));
    var X = function (d) { return d <= 7 ? left + d * unit * scale : left + 7 * unit * scale + (d - 7) * unit; };
    var LY = {};
    data.lanes.forEach(function (l, i) { LY[l.id] = 90 + i * 90; });
    var lastY = 90 + (data.lanes.length - 1) * 90, axisY = lastY + 56, H = axisY + 54;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    while (svg.firstChild) svg.removeChild(svg.firstChild);

    var defs = el('defs', {}, svg);
    var pat = el('pattern', { id: uid + '-hatch', width: 7, height: 7, patternUnits: 'userSpaceOnUse', patternTransform: 'rotate(45)' }, defs);
    el('line', { 'class': 'd-hatch', x1: 0, y1: 0, x2: 0, y2: 7 }, pat);
    var m1 = el('marker', { id: uid + '-ar', viewBox: '0 0 10 10', refX: 9, refY: 5, markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse' }, defs);
    el('path', { 'class': 'd-arrow', d: 'M0 0 L10 5 L0 10 Z' }, m1);
    var m2 = el('marker', { id: uid + '-arc', viewBox: '0 0 10 10', refX: 9, refY: 5, markerWidth: 6, markerHeight: 6, orient: 'auto-start-reverse' }, defs);
    el('path', { 'class': 'd-arrow--crit', d: 'M0 0 L10 5 L0 10 Z' }, m2);

    var gLanes = el('g', {}, svg), gAxis = el('g', { 'class': 'd-axis' }, svg), gLinks = el('g', {}, svg),
      gBar = el('g', {}, svg), gTasks = el('g', {}, svg), gBlind = el('g', {}, svg), gLaunch = el('g', {}, svg);

    // key building blocks: visible at rest
    data.lanes.forEach(function (l) {
      var y = LY[l.id];
      el('line', { x1: left - 14, y1: y, x2: X(days) + 14, y2: y, 'class': 'd-lane' }, gLanes);
      el('rect', { x: 24, y: y - 5, width: 10, height: 10, rx: 2, 'class': 'd-lanemark' }, gLanes);
      bi(gLanes, { x: 44, y: y + 5, 'class': 'd-lanelab' }, l.sl, l.en);
    });

    var ax = seq(gAxis, 0);
    for (var d = 0; d <= days; d++) el('line', { x1: X(d), y1: axisY, x2: X(d), y2: d % 7 === 0 ? axisY + 8 : axisY + 4 }, ax);
    el('line', { x1: X(0), y1: axisY, x2: X(days), y2: axisY }, ax);
    for (var t = 0; t <= days; t += 7) bi(ax, { x: X(t), y: axisY + 26 }, 'dan ' + t, 'day ' + t);
    if (data.axisNote) bi(ax, { x: X(3.5), y: axisY + 44 }, data.axisNote.sl, data.axisNote.en);

    var P = {};
    (data.tasks || []).forEach(function (k) {
      var x = X(k.d), y = LY[k.lane];
      P[k.id] = { x: x, y: y };
      var g = seq(gTasks, 120 + k.d * 11, 'd-task');
      el('circle', { cx: x, cy: y, r: 5.5 }, g);
      var a = { x: x + (k.end ? -10 : 10), y: y + (k.below ? 22 : -12) };
      if (k.end) a['text-anchor'] = 'end';
      bi(g, a, k.sl, k.en);
    });

    if (data.bar) {
      var b = data.bar, by = LY[b.lane], gb = seq(gBar, 380);
      P.barStart = { x: X(b.from), y: by }; P.barEnd = { x: X(b.to), y: by };
      el('rect', { x: X(b.from), y: by - 9, width: X(b.to) - X(b.from), height: 18, rx: 4, fill: 'url(#' + uid + '-hatch)', 'class': 'd-bar' }, gb);
      bi(gb, { x: X(b.from) + 2, y: by - 18, 'class': 'd-barlab' }, b.sl, b.en);
      if (b.tagSl) bi(gb, { x: X(b.from) + 2, y: by + 28, 'class': 'd-bartag' }, b.tagSl, b.tagEn);
    }

    (data.links || []).forEach(function (k, i) {
      var a = P[k.a], z = P[k.b];
      if (!a || !z) return;
      var sx = a.x + (k.a === 'barEnd' ? 0 : 6), ex = z.x - (k.b === 'barStart' ? 2 : 8), dx = Math.max(18, (ex - sx) * 0.5);
      var path = 'M' + sx + ' ' + a.y + ' C' + (sx + dx) + ' ' + a.y + ' ' + (ex - dx) + ' ' + z.y + ' ' + ex + ' ' + z.y;
      var tt = k.crit ? 600 + i * 30 : 470 + i * 20;
      var g = seq(gLinks, tt);
      var p = el('path', { d: path, pathLength: 1, 'class': 'd-link draw' + (k.crit ? ' d-link--crit' : ''), 'marker-end': 'url(#' + uid + (k.crit ? '-arc' : '-ar') + ')' }, g);
      p.style.setProperty('--t', tt + 'ms');
      if (k.sl) bi(g, { x: (sx + ex) / 2 + 6, y: a.y === z.y ? a.y + 18 : (a.y + z.y) / 2 - 8, 'class': 'd-linklab' }, k.sl, k.en);
    });

    (data.blind || []).forEach(function (k, i) {
      var x = X(k.d), y = LY[k.lane] - 46, to = P[k.to], g = seq(gBlind, 820 + i * 40, 'd-blind');
      if (to) el('path', { 'class': 'ln', d: 'M' + x + ' ' + y + ' L' + to.x + ' ' + to.y }, g);
      el('path', { 'class': 'dm', d: 'M' + x + ' ' + (y - 7) + ' L' + (x + 7) + ' ' + y + ' L' + x + ' ' + (y + 7) + ' L' + (x - 7) + ' ' + y + ' Z' }, g);
      var a = { x: x + (k.end ? -12 : 12), y: y + 4.5 };
      if (k.end) a['text-anchor'] = 'end';
      bi(g, a, k.sl, k.en);
    });

    if (data.launch) {
      var gl = seq(gLaunch, 760, 'd-launch');
      el('line', { x1: X(data.launch.d), y1: 40, x2: X(data.launch.d), y2: axisY - 6 }, gl);
      bi(gl, { x: X(data.launch.d), y: 30 }, data.launch.sl, data.launch.en);
    }

    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function draw() { fig.classList.add('is-drawn'); }
    var rb = fig.querySelector('[data-replay]');
    if (rb) {
      rb.hidden = !!reduce;
      rb.onclick = function () {
        fig.classList.add('no-anim'); fig.classList.remove('is-drawn');
        void fig.offsetWidth;
        fig.classList.remove('no-anim');
        requestAnimationFrame(function () { requestAnimationFrame(draw); });
      };
    }
    if (reduce || !('IntersectionObserver' in window)) { fig.classList.add('no-anim'); draw(); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { draw(); io.disconnect(); } });
    }, { threshold: 0.35 });
    io.observe(fig.querySelector('.vp-map__scroll') || fig);
  };

  VP.lang = function (root) {
    root.querySelectorAll('[data-set-lang]').forEach(function (b) {
      b.addEventListener('click', function () {
        var l = b.getAttribute('data-set-lang');
        root.setAttribute('data-lang', l);
        document.documentElement.lang = l;
        root.querySelectorAll('[data-set-lang]').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      });
    });
  };

  VP.theme = function (root, opts) {
    opts = opts || {};
    var html = document.documentElement, mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: light)') : null, mode = 'system';
    function systemTheme() { return mq && mq.matches ? 'light' : 'dark'; }
    function apply(m, remember) {
      mode = m;
      html.setAttribute('data-theme', m === 'system' ? systemTheme() : m);
      root.querySelectorAll('[data-set-theme]').forEach(function (x) { x.setAttribute('aria-pressed', x.getAttribute('data-set-theme') === m ? 'true' : 'false'); });
      if (remember) { try { localStorage.setItem('vp-theme', m); } catch (e) {} }
    }
    root.querySelectorAll('[data-set-theme]').forEach(function (b) {
      b.addEventListener('click', function () { apply(b.getAttribute('data-set-theme'), true); });
    });
    if (opts.follow) {
      var saved = null;
      try { saved = localStorage.getItem('vp-theme'); } catch (e) {}
      apply(saved === 'light' || saved === 'dark' ? saved : 'system', false);
      if (mq && mq.addEventListener) mq.addEventListener('change', function () { if (mode === 'system') apply('system', false); });
    }
  };

  VP.copy = function (button, target) {
    button.addEventListener('click', function () {
      var text = (target.textContent || '').trim();
      function done() {
        var sl = button.querySelector('[lang="sl"]'), en = button.querySelector('[lang="en"]');
        if (sl || en) { if (sl) sl.textContent = 'Kopirano'; if (en) en.textContent = 'Copied'; } else button.textContent = 'Kopirano';
      }
      function select() { var r = document.createRange(); r.selectNodeContents(target); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r); }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, select);
      else select();
    });
  };
})();
