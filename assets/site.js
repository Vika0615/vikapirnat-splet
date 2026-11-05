/* Vika Pirnat — zagon strani. Uporablja window.VP iz bundle.js (kopija iz design sistema). */
(function () {
  var VP = window.VP;
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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
