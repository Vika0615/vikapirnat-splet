# vikapirnat-splet

Osebna spletna stran Vike Pirnat (produktno vodenje, svetovanje). Statični HTML, CSS in malo JS, brez ogrodja. Gostuje na GitHub Pages.

## Zgradba

| Mapa ali datoteka | Kaj je |
|---|---|
| `src/sl/*.html`, `src/en/*.html` | vsebina strani (SLO in ENG). **Tu urejaš besedilo.** |
| `tools/build.py` | zgradi strani: glava, noga (s preklopom teme), pas s klicem k pogovoru, kontakt (e-pošta in LinkedIn), `tokens.css`, `bundle.css`, `sitemap.xml`, `404.html` |
| `tools/tokens.json` | žetoni iz design sistema (barve, pisave, razmiki) |
| `tools/bundle.css` | **nespremenjena kopija** komponent iz design sistema; gradnja iz nje naredi `assets/bundle.css` brez pisav z Googla |
| `assets/bundle.js` | **kopija** skripte iz design sistema, ne urejaj ročno |
| `assets/fonts.css`, `assets/fonts/` | pisave Red Hat (latin, latin-ext), gostujejo na strani, da obiskovalčev IP ne gre k Googlu |
| `assets/site.css`, `assets/site.js` | dodatki samo za to stran (kartice projektov, O meni, preklop jezika) |
| `assets/maps/*.js` | podatki za zemljevid problema (en na case study) |
| `assets/img/` | posnetki zaslona in fotografija (`img/vika/`, brez metapodatkov) |
| `index.html`, `storitve/`, `projekti/`, `o-meni/`, `kontakt/`, `en/…` | zgrajene strani, ki jih streže GitHub Pages |

Design sistem: https://claude.ai/artifact/QMSTcyAZq2PXfPNSFTN81s

## Sprememba besedila

1. Uredi datoteko v `src/sl/` ali `src/en/` (vedno obe).
2. Zaženi `py tools/build.py`.
3. Preveri lokalno: `py -m http.server 8765` in odpri http://127.0.0.1:8765/
4. Commit in push. GitHub Pages objavi v 1–2 minutah.

## Nov projekt ali case study

1. V `tools/build.py` dodaj vrstico v `PAGES`, npr. `"primer": ("projekti/primer/", "en/projects/primer/")`.
2. Kopiraj `src/sl/gobe.html` in `src/en/gobe.html` v `src/sl/primer.html` in `src/en/primer.html` ter zamenjaj vsebino.
3. Za zemljevid problema dodaj `assets/maps/primer.js` in v glavi strani `scripts: maps/primer.js`; na sliki `data-map="primer"`.
4. Na strani Projekti (`src/sl/work.html`, `src/en/work.html`) kopiraj kartico `<li class="site-card">` in jo postavi na vrh seznama. Za kartico »V pripravi« uporabi `site-card site-card--soon` (navodilo je v komentarju na strani).
5. `py tools/build.py`, commit, push.

## Kontakt

Stran nima obrazca. Kontakt je gumb za e-pošto (`mailto:` z zadevo), naslov s kopiranjem in povezava na LinkedIn. Vse je v `contact_block()` v `tools/build.py`; naslov in povezava sta v `EMAIL` in `LINKEDIN`.

## Lastna domena (ko jo kupiš)

1. V `tools/build.py` nastavi `SITE_URL = "https://vikapirnat.si/"`, dodaj datoteko `CNAME` z vrstico `vikapirnat.si`, zaženi build, commit, push.
2. Pri registrarju v DNS dodaj (vrednosti preveri v GitHubovi dokumentaciji »Managing a custom domain for your GitHub Pages site«):
   - 4 zapise `A` za `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - (neobvezno) 4 zapise `AAAA` za `@`: `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
   - zapis `CNAME` za `www` → `vika0615.github.io`
3. Na GitHubu: Settings → Pages → Custom domain `vikapirnat.si` → Save. Ko je preverjanje DNS zeleno, vklopi **Enforce HTTPS**.
4. Priporočeno: domeno preveri tudi v Settings (profil) → Pages → Add a domain, da je nihče drug ne more uporabiti.
