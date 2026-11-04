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

  // Obrazec za povpraševanje (Formspree)
  document.querySelectorAll('form[data-form]').forEach(function (form) {
    var done = form.querySelector('[data-form-done]');
    var error = form.querySelector('[data-form-error]');
    var off = form.querySelector('[data-form-off]');
    var button = form.querySelector('button[type="submit"]');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      done.hidden = true; error.hidden = true; off.hidden = true;
      if (form.hasAttribute('data-off')) { off.hidden = false; return; }
      var label = button.textContent;
      button.disabled = true;
      button.textContent = button.getAttribute('data-sending') || label;
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw new Error('HTTP ' + r.status);
          form.reset();
          done.hidden = false;
          done.setAttribute('tabindex', '-1');
          done.focus();
        })
        .catch(function () { error.hidden = false; })
        .then(function () { button.disabled = false; button.textContent = label; });
    });
  });
})();
