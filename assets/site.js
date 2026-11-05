/* Vika Pirnat — zagon strani. Uporablja window.VP iz bundle.js (kopija iz design sistema). */
(function () {
  var VP = window.VP;
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Analitika: PostHog brez piškotkov se naloži v glavi, samo na vikapirnat.com (tools/build.py, HEAD_ANALYTICS).
  // Drugje window.posthog ne obstaja in track() ne naredi nič. Zasebnost: /zasebnost/.
  function track(name, props) {
    try { if (window.posthog && window.posthog.capture) window.posthog.capture(name, props || {}); } catch (e) {}
  }
  function placeOf(el) {
    if (el.closest('.vp-footer')) return 'footer';
    if (el.closest('.vp-header')) return 'header';
    if (el.closest('.vp-band')) return 'contact_band';
    if (el.closest('.site-contact')) return 'contact_page';
    if (el.closest('.vp-hero')) return 'hero';
    var s = el.closest('section[id], section[aria-labelledby]');
    return s ? (s.id || s.getAttribute('aria-labelledby')) : 'page';
  }
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href');
    if (href.indexOf('mailto:') === 0) track('contact_clicked', { channel: 'email', place: placeOf(a) });
    else if (href.indexOf('linkedin.com') > -1) track('contact_clicked', { channel: 'linkedin', place: placeOf(a) });
    else if (href.indexOf('play.google.com') > -1) track('store_clicked', { store: 'google_play', place: placeOf(a) });
    else if (a.hasAttribute('hreflang') && a.closest('.vp-lang')) track('language_switched', { to: a.getAttribute('hreflang') });
  });
  document.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () { track('email_copied', { place: placeOf(b) }); });
  });
  document.querySelectorAll('.site-acc__item').forEach(function (d, i) {
    var sum = d.querySelector('summary');
    var name = d.querySelector('.site-acc__name');
    if (sum) sum.addEventListener('click', function () {
      if (!d.open) track('concept_opened', { concept: name ? name.textContent.trim() : '', concept_index: i + 1 });
    });
  });

  if (VP) {
    // Tema: sledi brskalniku, dokler obiskovalec ne izbere Svetla ali Temna.
    VP.theme(document.body, { follow: true });

    // Kopiraj e-pošto
    document.querySelectorAll('[data-copy]').forEach(function (b) {
      var target = document.getElementById(b.getAttribute('data-copy'));
      if (target) VP.copy(b, target);
    });
  }

  // Števec: od data-from (privzeto 0) do vrednosti v data-count
  function count(el) {
    var to = parseFloat(el.getAttribute('data-count'));
    var from = parseFloat(el.getAttribute('data-from') || '0');
    if (still || isNaN(to)) return;
    var start = null, dur = 1100;
    function step(t) {
      if (start === null) start = t;
      var k = Math.min(1, (t - start) / dur);
      var e = 1 - Math.pow(1 - k, 3);
      el.textContent = Math.round(from + (to - from) * e);
      if (k < 1) requestAnimationFrame(step);
    }
    el.textContent = from;
    requestAnimationFrame(step);
  }

  // Koncepti »Kako razmišljam«: na računalniku seznam levo, izbrani koncept desno (vedno je izbran en);
  // na telefonu se koncept odpre pod svojim imenom.
  var stage = document.querySelector('[data-stage]');
  if (stage) {
    var wide = window.matchMedia('(min-width: 900px)');
    var tabs = function () { return wide.matches && window.getComputedStyle(stage).display !== 'none'; };
    var items = Array.prototype.slice.call(document.querySelectorAll('.site-acc__item'));
    items.forEach(function (d) { d._panel = d.querySelector('.site-acc__panel'); });
    var place = function () {
      items.forEach(function (d) { if (d._panel.parentNode !== d) d.appendChild(d._panel); });
      if (!tabs()) return;
      var open = items.filter(function (d) { return d.open; })[0];
      if (!open) { items[0].open = true; return; } // »toggle« pokliče place znova
      stage.appendChild(open._panel);
    };
    items.forEach(function (d) {
      d.addEventListener('toggle', function () {
        if (tabs() && !items.some(function (x) { return x.open; })) { d.open = true; return; }
        place();
      });
    });
    if (wide.addEventListener) wide.addEventListener('change', place);
    place();
  }

  // Pojav ob drsenju, števci in diagram poteka (.site-flow) se sprožijo, ko pridejo v pogled
  var targets = document.querySelectorAll('[data-reveal], .site-flow');
  if (!('IntersectionObserver' in window)) {
    targets.forEach(function (el) { el.classList.add('is-in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      en.target.classList.add('is-in');
      en.target.querySelectorAll('[data-count]').forEach(count);
      io.unobserve(en.target);
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
  targets.forEach(function (el) { io.observe(el); });
})();
