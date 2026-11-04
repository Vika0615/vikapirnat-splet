/* Zemljevid problema: aplikacija Gobe. Vir: case study (zapisek »Case study — Gobe app«, stanje podatkov 2. 11. 2026).
   Uporaba: <figure class="vp-map" data-map="gobe"> … </figure>; izriše ga assets/site.js z VP.problemMap. */
window.VP_MAPS = window.VP_MAPS || {};
window.VP_MAPS.gobe = {
  days: 28, firstWeekScale: 2,
  axisNote: { sl: 'prvi teden v dvojnem merilu', en: 'first week at double scale' },
  lanes: [
    { id: 'U', sl: 'Uporabnik', en: 'User' }, { id: 'V', sl: 'Varnost', en: 'Safety' },
    { id: 'S', sl: 'Vsebina z viri', en: 'Sourced content' }, { id: 'K', sl: 'Kviz in atlas', en: 'Quiz and atlas' },
    { id: 'L', sl: 'Lansiranje', en: 'Launch' }
  ],
  tasks: [
    { id: 't1', lane: 'U', d: 0, sl: 'Začetnik, ki se želi naučiti', en: 'Beginners who want to learn' },
    { id: 't2', lane: 'V', d: 0, sl: 'Nikoli tiho ne izloči', en: 'Never silently dropped' },
    { id: 't3', lane: 'V', d: 4, below: 1, sl: 'Dvojnice, tudi neznane', en: 'Lookalikes, even unknown ones' },
    { id: 't4', lane: 'V', d: 19, below: 1, sl: 'Opozorilo samo enkrat', en: 'Warn only once' },
    { id: 't5', lane: 'S', d: 1, sl: 'Viri za 25 vrst', en: 'Sources for 25 species' },
    { id: 't6', lane: 'S', d: 4, below: 1, sl: 'Preverjeno proti virom', en: 'Checked against sources' },
    { id: 't7', lane: 'S', d: 19, sl: '64 vrst', en: '64 species' },
    { id: 't8', lane: 'K', d: 1, sl: 'Dizajn in makete', en: 'Design and mock-ups' },
    { id: 't9', lane: 'K', d: 2, below: 1, sl: 'Atlas in kviz', en: 'Atlas and quiz' },
    { id: 't10', lane: 'L', d: 3, sl: 'Analitika s soglasjem', en: 'Consented analytics' },
    { id: 't11', lane: 'L', d: 23, sl: 'Trgovina Play', en: 'Google Play' },
    { id: 't12', lane: 'L', d: 28, below: 1, end: 1, sl: 'Filter za robote', en: 'Robot filter' }
  ],
  bar: { lane: 'L', from: 7, to: 21, sl: 'Zaprti test: 12 testerjev × 14 dni', en: 'Closed test: 12 testers × 14 days', tagSl: 'OVIRA · ČAKANJE, KI GA NI MOGOČE SKRAJŠATI', tagEn: 'ROADBLOCK · A WAIT THAT CANNOT BE SHORTENED' },
  links: [
    { a: 't1', b: 't8' }, { a: 't2', b: 't9' },
    { a: 't5', b: 't9', crit: 1, sl: 'podatki pred zasloni', en: 'data before screens' },
    { a: 't9', b: 't10', crit: 1 },
    { a: 't10', b: 'barStart', crit: 1, sl: 'merjenje pred testom', en: 'measure before test' },
    { a: 't6', b: 'barStart' }, { a: 'barEnd', b: 't11', crit: 1 }, { a: 't7', b: 't11' }
  ],
  blind: [
    { d: 4, lane: 'L', to: 't9', sl: 'Napaka s travnika', en: 'The meadow bug' },
    { d: 12.5, lane: 'S', to: 't7', sl: '33 prijav manjkajoče gobe', en: '33 missing-mushroom reports' },
    { d: 19, lane: 'V', to: 't4', sl: 'Utrujenost od opozoril', en: 'Warning fatigue' },
    { d: 28, lane: 'L', to: 't12', end: 1, sl: 'Googlovi testni roboti', en: 'Google’s test robots' }
  ],
  launch: { d: 23, sl: 'OBJAVA · DAN 23', en: 'LAUNCH · DAY 23' }
};
