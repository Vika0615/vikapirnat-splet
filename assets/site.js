/* Vika Pirnat — zagon strani. Uporablja window.VP iz bundle.js (kopija iz design sistema). */
(function () {
  var VP = window.VP;
  if (!VP) return;

  // Tema: sledi brskalniku, dokler obiskovalec ne izbere Svetla ali Temna.
  VP.theme(document.body, { follow: true });

  // Kopiraj e-pošto
  document.querySelectorAll('[data-copy]').forEach(function (b) {
    var target = document.getElementById(b.getAttribute('data-copy'));
    if (target) VP.copy(b, target);
  });

  // Zemljevid problema (en na stran); podatki so v assets/maps/*.js
  document.querySelectorAll('figure.vp-map[data-map]').forEach(function (fig) {
    var data = window.VP_MAPS && window.VP_MAPS[fig.getAttribute('data-map')];
    if (data) VP.problemMap(fig, data);
  });
})();
