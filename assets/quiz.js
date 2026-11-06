/* Kviz »Kaj če ni služba?« (/kviz/, /en/quiz/). Besedilo v obeh jezikih je tukaj.
   Odgovori so samo v spominu strani: nič se ne shrani in nič se ne pošlje. */
(function () {
  var app = document.getElementById('quiz-app');
  if (!app) return;

  var LEVELS = ['A', 'B', 'C', 'D', 'E'];

  var T = {
    sl: {
      title: 'Kaj če ni služba?',
      eyebrow: 'Kviz za razmislek · 2 minuti',
      lead: 'Devet vprašanj za čas, ko ti služba ne sede. Ne povedo ti, kateri poklic je pravi zate. Pomagajo ti razmisliti, kje se težava zares skriva.',
      levelsLabel: 'Kviz preveri pet ravni, od najožje do najširše',
      levels: { A: 'Naloge', B: 'Ljudje', C: 'Podjetje', D: 'Poklic', E: 'Zunaj službe' },
      note: 'To je igra za razmislek, ne psihološki test. Odgovori ostanejo v tvojem brskalniku in se nikamor ne pošljejo.',
      start: 'Začni', back: 'Nazaj', again: 'Začni znova', share: 'Deli kviz na LinkedInu', about: 'Več o meni →',
      qOf: function (i, n) { return 'Vprašanje ' + i + ' od ' + n; },
      resultEyebrow: 'Tvoja domneva',
      stepLabel: 'En korak za ta teden',
      tallyLabel: 'Kako so se razporedili tvoji odgovori',
      also: 'Morda tudi',
      closing: 'To je domneva za preverjanje, ne diagnoza. Devet vprašanj ne pozna tvojega življenja.',
      questions: [
        { q: 'Nedelja zvečer. Kaj te ob misli na ponedeljek najbolj stisne?',
          a: { A: 'Naloge, ki me čakajo.', B: 'Določeni ljudje.', C: 'Način, kako se pri nas stvari delajo.', D: 'Občutek, da to sploh ni moje področje.', E: 'Brez energije sem že, preden se teden začne.' } },
        { q: 'Od jutri lahko iz službe odstraniš eno stvar, plača ostane enaka. Kaj gre ven?',
          a: { A: 'Del nalog.', B: 'Določeni ljudje.', C: 'Pravila in notranja politika.', D: 'Vse skupaj, raje začnem nekaj povsem drugega.', E: 'Nič posebej, rabim samo več časa zase.' } },
        { q: 'Pomisli na vse službe doslej, tudi študentske. Kaj se ponavlja?',
          a: { A: 'Podobne naloge me izčrpajo.', B: 'Naletim na podobnega vodjo ali ekipo.', C: 'Znajdem se v podobnem tipu podjetja.', D: 'Vedno ista stroka, ki me nikoli ne potegne.', E: 'Moja utrujenost, ne glede na službo.' } },
        { q: 'Kdaj pri delu izgubiš občutek za čas?',
          a: { A: 'Pri nalogah, ki jih dobim premalo.', B: 'Ko delam z ljudmi, ki mi ustrezajo.', C: 'Ko lahko stvar naredim po svoje, brez petih odobritev.', D: 'Pri delu nikoli, pri hobiju pogosto.', E: 'Zadnje čase nikjer.' } },
        { q: 'Isto delo, ista plača, a povsem druga ekipa in vodja. Kako se počutiš ob tej misli?',
          a: { A: 'Enako, naloge ostanejo iste.', B: 'Olajšano. To bi rešilo veliko.', C: 'Malo bolje, a hiša je ista.', D: 'Še vedno narobe. Ne gre za ljudi.', E: 'Težko rečem, za take misli nimam več energije.' } },
        { q: 'Nekdo te vpraša, kaj delaš. Kaj odgovoriš?',
          a: { A: 'Povem naziv, ne pa, kaj zares počnem.', B: 'Rečem: »Delo je v redu, ampak ...«', C: 'Raje povem, kaj delam, kot kje.', D: 'Hitro zamenjam temo.', E: 'Rečem: »Preveč.«' } },
        { q: 'Kaj drugim tiho zavidaš?',
          a: { A: 'Bolj zanimive naloge v isti stroki.', B: 'Dobrega vodjo ali ekipo.', C: 'Podjetje, na katerega so ponosni.', D: 'Povsem drug poklic.', E: 'Da imajo po službi še energijo.' } },
        { q: 'Vrneš se z dvotedenskega dopusta. Kdaj izpuhti dopustniški občutek?',
          a: { A: 'Ko odprem seznam nalog.', B: 'Na prvem sestanku.', C: 'Ob prvem internem obvestilu.', D: 'Ko se spomnim, da me to čaka še naslednjih 30 let.', E: 'Sploh ga ni bilo, dopust me ni spočil.' } },
        { q: 'Veš, da ti ne more spodleteti. Kaj spremeniš najprej?',
          a: { A: 'Vsebino svojega dela.', B: 'S kom delam.', C: 'Kje delam.', D: 'Kaj sem po poklicu.', E: 'Kako živim zunaj službe.' } }
      ],
      results: {
        A: { q: 'Kaj če ne potrebuješ nove službe, ampak drugačen ponedeljek?',
             t: 'Tvoji odgovori najpogosteje kažejo na vsebino dela, ne na ljudi ali podjetje. Naloge se pogosto dajo preoblikovati brez odpovedi. Preden zamenjaš službo, preveri, koliko prostora imaš v tej.',
             s: 'Zapiši tri naloge, ki ti dajo energijo, in tri, ki ti jo vzamejo. Eno zamenjavo predlagaj vodji.' },
        B: { q: 'Kaj če je delo pravo, soba pa napačna?',
             t: 'Največkrat se ti zatakne pri ljudeh: pri vodji, ekipi ali načinu sodelovanja. Delo samo ti morda še vedno ustreza. Menjava ekipe je manjši korak kot menjava poklica, zato jo je vredno preveriti prej.',
             s: 'Pojdi na kavo z nekom iz druge ekipe in vprašaj, kako delajo pri njih.' },
        C: { q: 'Kaj če je poklic pravi, streha pa napačna?',
             t: 'Tvoji odgovori kažejo na podjetje: na pravila, kulturo in način, kako se stvari delajo. Stroka in ljudje te motijo manj. Enako delo je pod drugo streho lahko povsem drugačna izkušnja.',
             s: 'Poišči tri podjetja, kjer tvoje delo poteka drugače, in piši nekomu, ki tam dela.' },
        D: { q: 'Kaj če ne potrebuješ boljše službe, ampak drugo zgodbo?',
             t: 'Odgovori kažejo, da te ne moti le ta služba, ampak področje samo. To je velika domneva, zato je ne preverjaj z odpovedjo. Preveri jo z majhnimi poskusi, ki te skoraj nič ne stanejo.',
             s: 'Poišči nekoga, ki dela nekaj, kar te vleče. Vprašaj, kakšen je tam običajen torek.' },
        E: { q: 'Kaj če ni kriva služba, ampak prazna baterija?',
             t: 'Tvoji odgovori govorijo bolj o energiji kot o delu. Ko je baterija prazna, je vsaka služba videti napačna. Najprej preveri to, šele potem odločaj o karieri.',
             s: 'En teden zapisuj, kdaj imaš energijo in kdaj ne, preden odločaš o službi. Če izčrpanost traja že dlje, se o njej pogovori z zdravnikom.' }
      }
    },
    en: {
      title: "What if it's not the job?",
      eyebrow: 'A 2-minute rethink',
      lead: "Nine questions for when work doesn't sit right. They won't tell you which job you're meant for. They help you work out where the problem actually lives.",
      levelsLabel: 'It looks at five levels, from narrowest to widest',
      levels: { A: 'Tasks', B: 'People', C: 'Company', D: 'Profession', E: 'Outside work' },
      note: 'This is a game for thinking, not a psychological test. Your answers stay in your browser and are not sent anywhere.',
      start: 'Start', back: 'Back', again: 'Start over', share: 'Share the quiz on LinkedIn', about: 'More about me →',
      qOf: function (i, n) { return 'Question ' + i + ' of ' + n; },
      resultEyebrow: 'Your working theory',
      stepLabel: 'One step for this week',
      tallyLabel: 'How your answers added up',
      also: 'Maybe also',
      closing: "This is a theory to test, not a diagnosis. Nine questions can't know your whole life.",
      questions: [
        { q: 'Sunday evening. What makes your chest tighten most when you think about Monday?',
          a: { A: 'The tasks waiting for me.', B: 'Certain people.', C: 'The way things get done around here.', D: "The feeling that this isn't my field at all.", E: "I'm out of energy before the week even starts." } },
        { q: 'From tomorrow you can delete one thing from your job and keep your pay. What goes?',
          a: { A: 'Some of my tasks.', B: 'Certain people.', C: 'The rules and office politics.', D: "All of it. I'd rather start something completely different.", E: 'Nothing in particular. I just need more time for myself.' } },
        { q: "Think of every job you've had, student jobs included. What keeps repeating?",
          a: { A: 'Similar tasks wear me out.', B: 'I end up with the same kind of boss or team.', C: 'I land in the same kind of company.', D: 'Always the same field, and it never pulls me in.', E: 'My tiredness, whatever the job.' } },
        { q: 'When do you lose track of time at work?',
          a: { A: 'On the tasks I rarely get to do.', B: 'When I work with people who suit me.', C: 'When I can do it my way, without five sign-offs.', D: 'Never at work. With my hobby, all the time.', E: 'Lately, nowhere.' } },
        { q: 'Same work, same pay, but a completely different team and manager. How does that feel?',
          a: { A: "The same. The tasks don't change.", B: 'Relieved. That would fix a lot.', C: "A bit better, but it's still the same company.", D: "Still not right. It's not about the people.", E: "Hard to say. I don't have the energy to think about it." } },
        { q: 'Someone asks what you do. What do you say?',
          a: { A: 'I give my job title, not what I actually do.', B: 'I say, “The work is fine, but…”', C: "I'd rather say what I do than where.", D: 'I change the subject fast.', E: 'I say, “Too much.”' } },
        { q: 'What do you secretly envy in other people?',
          a: { A: 'More interesting tasks in the same field.', B: 'A good manager or team.', C: "A company they're proud of.", D: 'A completely different profession.', E: 'That they still have energy after work.' } },
        { q: "You're back from two weeks off. When does the holiday glow wear off?",
          a: { A: 'When I open my to-do list.', B: 'At the first meeting.', C: 'At the first company-wide email.', D: 'When I remember this is the next thirty years.', E: "It never showed up. The holiday didn't recharge me at all." } },
        { q: "If you knew you couldn't fail, what would you change first?",
          a: { A: 'What I actually do all day.', B: 'Who I work with.', C: 'Where I work.', D: 'What I do for a living.', E: 'How I live outside work.' } }
      ],
      results: {
        A: { q: "What if you don't need a new job, just a different Monday?",
             t: 'Your answers keep pointing to the work itself, not the people or the company. Tasks can often be reshaped without quitting. Before you change jobs, check how much room you have in this one.',
             s: 'Write down three tasks that give you energy and three that drain it. Suggest one swap to your manager.' },
        B: { q: 'What if the work is right and the room is wrong?',
             t: "Most of the friction comes from people: your manager, your team or the way you work together. The work itself may still suit you. Changing teams is a smaller step than changing professions, so it's worth testing first.",
             s: 'Grab a coffee with someone from another team and ask how things work over there.' },
        C: { q: "What if it's the right job under the wrong roof?",
             t: 'Your answers point at the company: its rules, its culture and the way things get done. The field and the people bother you less. The same work can feel completely different under another roof.',
             s: 'Find three companies where your kind of work is done differently and write to someone who works there.' },
        D: { q: "What if you don't need a better job, but a different story?",
             t: "Your answers suggest it's not only this job that bothers you, but the field itself. That's a big theory, so don't test it by quitting. Test it with small experiments that cost you almost nothing.",
             s: 'Find someone doing something that pulls you in and ask what a normal Tuesday looks like for them.' },
        E: { q: "What if it's not the job, but an empty battery?",
             t: 'Your answers are more about energy than about work. When the battery is empty, every job looks like the wrong one. Check this first, then decide about your career.',
             s: "For one week, note when you have energy and when you don't, before deciding anything about the job. If the exhaustion has lasted a long time, talk to a doctor about it." }
      }
    }
  };

  var t = T[document.body.getAttribute('data-lang') === 'en' ? 'en' : 'sl'];
  var state = { screen: 'intro', idx: 0, answers: [], orders: [] };
  var mark = document.querySelector('.site-mark');
  var homeUrl = mark ? mark.href : '/';
  var canonical = document.querySelector('link[rel="canonical"]');
  var pageUrl = canonical ? canonical.href : location.href;
  var cta = document.getElementById('quiz-cta');

  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var x = a[i]; a[i] = a[j]; a[j] = x; }
    return a;
  }
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function button(cls, text, onClick) {
    var b = el('button', cls, text);
    b.type = 'button';
    b.addEventListener('click', onClick);
    return b;
  }
  function score(answers) {
    var rows = LEVELS.map(function (L) { return { level: L, count: 0, last: -1 }; });
    answers.forEach(function (L, i) {
      var r = rows[LEVELS.indexOf(L)];
      if (r) { r.count++; r.last = i; }
    });
    var sorted = rows.slice().sort(function (a, b) { return b.count - a.count || b.last - a.last; });
    var second = sorted[1].count > 0 && sorted[0].count - sorted[1].count <= 1 ? sorted[1].level : null;
    return { rows: rows, primary: sorted[0].level, secondary: second };
  }
  function levelsList(res) {
    var ul = el('ul', 'site-quiz__levels');
    LEVELS.forEach(function (L, i) {
      var li = el('li');
      li.appendChild(el('span', 'site-quiz__name', t.levels[L]));
      if (!res) {
        var band = el('span', 'site-quiz__band');
        band.style.setProperty('--w', (20 + i * 20) + '%');
        li.appendChild(band);
        li.appendChild(el('span'));
      } else {
        var c = res.rows[i].count;
        if (L === res.primary) li.className = 'site-quiz__top';
        var dots = el('span', 'site-quiz__dots');
        for (var k = 0; k < c; k++) dots.appendChild(el('span', 'site-quiz__dot'));
        li.appendChild(dots);
        li.appendChild(el('span', 'site-quiz__n', String(c)));
      }
      ul.appendChild(li);
    });
    return ul;
  }
  function block(label, child) {
    var b = el('div', 'site-quiz__block');
    b.appendChild(el('p', 'vp-eyebrow', label));
    b.appendChild(child);
    return b;
  }

  function intro() {
    var nodes = [];
    nodes.push(el('p', 'vp-eyebrow', t.eyebrow));
    var h = el('h1', 'vp-h1');
    h.appendChild(el('span', 'site-quiz__mark', t.title));
    nodes.push(h);
    nodes.push(el('p', 'vp-lede', t.lead));
    nodes.push(block(t.levelsLabel, levelsList()));
    var act = el('div', 'site-actions');
    act.appendChild(button('vp-btn vp-btn--primary', t.start, function () {
      state.screen = 'q'; state.idx = 0; state.answers = [];
      state.orders = t.questions.map(function () { return shuffle(LEVELS); });
      render(true);
    }));
    nodes.push(act);
    nodes.push(el('p', 'vp-small', t.note));
    return { nodes: nodes, heading: h };
  }

  function question() {
    var nodes = [], n = t.questions.length, item = t.questions[state.idx];
    var head = el('div', 'site-quiz__block');
    var prog = el('div', 'site-quiz__progress');
    prog.setAttribute('aria-hidden', 'true');
    for (var i = 0; i < n; i++) prog.appendChild(el('span', i <= state.idx ? 'is-done' : ''));
    head.appendChild(prog);
    head.appendChild(el('p', 'vp-eyebrow', t.qOf(state.idx + 1, n)));
    nodes.push(head);
    var h = el('h2', 'vp-h2', item.q);
    nodes.push(h);
    var opts = el('div', 'site-quiz__options');
    state.orders[state.idx].forEach(function (L) {
      var b = button('site-quiz__opt', item.a[L], function () {
        state.answers[state.idx] = L;
        if (state.idx < n - 1) state.idx++; else state.screen = 'result';
        render(true);
      });
      b.setAttribute('aria-pressed', String(state.answers[state.idx] === L));
      opts.appendChild(b);
    });
    nodes.push(opts);
    var nav = el('div', 'site-actions');
    nav.appendChild(button('vp-btn', t.back, function () {
      if (state.idx === 0) state.screen = 'intro'; else state.idx--;
      render(true);
    }));
    nodes.push(nav);
    return { nodes: nodes, heading: h };
  }

  function result() {
    var nodes = [], res = score(state.answers), r = t.results[res.primary];
    nodes.push(el('p', 'vp-eyebrow', t.resultEyebrow + ' · ' + t.levels[res.primary]));
    var h = el('h2', 'vp-h2');
    h.appendChild(el('span', 'site-quiz__mark', r.q));
    nodes.push(h);
    nodes.push(el('p', 'vp-lede', r.t));
    var step = el('div', 'site-quiz__step');
    step.appendChild(el('p', 'vp-eyebrow', t.stepLabel));
    step.appendChild(el('p', null, r.s));
    nodes.push(step);
    if (res.secondary) {
      var r2 = t.results[res.secondary];
      var also = el('div', 'site-quiz__also');
      also.appendChild(el('p', 'vp-eyebrow', t.also + ' · ' + t.levels[res.secondary]));
      also.appendChild(el('h3', 'vp-h3', r2.q));
      also.appendChild(el('p', null, r2.s));
      nodes.push(also);
    }
    nodes.push(block(t.tallyLabel, levelsList(res)));
    nodes.push(el('p', 'vp-small', t.closing));
    var acts = el('div', 'site-actions');
    var about = el('a', 'vp-btn vp-btn--primary', t.about);
    about.href = homeUrl;
    acts.appendChild(about);
    var share = el('a', 'vp-btn', t.share);
    share.href = 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(pageUrl);
    share.target = '_blank';
    share.rel = 'noopener';
    acts.appendChild(share);
    acts.appendChild(button('vp-btn vp-btn--quiet', t.again, function () {
      state.screen = 'intro'; state.answers = []; state.idx = 0;
      render(true);
    }));
    nodes.push(acts);
    return { nodes: nodes, heading: h };
  }

  function render(moved) {
    var view = state.screen === 'intro' ? intro() : state.screen === 'q' ? question() : result();
    while (app.firstChild) app.removeChild(app.firstChild);
    view.nodes.forEach(function (n) { app.appendChild(n); });
    if (cta) cta.hidden = state.screen !== 'result';
    if (moved) {
      view.heading.tabIndex = -1;
      view.heading.focus({ preventScroll: true });
      if (app.getBoundingClientRect().top < 0) app.scrollIntoView();
    }
  }

  render(false);
})();
