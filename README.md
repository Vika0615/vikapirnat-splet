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
| `assets/site.css`, `assets/site.js` | dodatki samo za to stran (domača stran O meni, kartice projektov, diagram poteka, pojav ob drsenju in števci) |
| `assets/img/` | posnetki zaslona in fotografija (`img/vika/`, brez metapodatkov) |
| `index.html` (O meni in Kako delam), `projekti/`, `blog/`, `kontakt/`, `en/…` | zgrajene strani, ki jih streže GitHub Pages |

Design sistem: https://claude.ai/artifact/QMSTcyAZq2PXfPNSFTN81s

## Sprememba besedila

1. Uredi datoteko v `src/sl/` ali `src/en/` (vedno obe).
2. Zaženi `py tools/build.py`.
3. Preveri lokalno: `py -m http.server 8765` in odpri http://127.0.0.1:8765/
4. Commit in push. GitHub Pages objavi v 1–2 minutah.

## Nov projekt ali case study

1. V `tools/build.py` dodaj vrstico v `PAGES`, npr. `"primer": ("projekti/primer/", "en/projects/primer/")`.
2. Kopiraj `src/sl/gobe.html` in `src/en/gobe.html` v `src/sl/primer.html` in `src/en/primer.html` ter zamenjaj vsebino.
3. Za diagram poteka kopiraj `<figure class="site-flow">` iz `src/sl/gobe.html` in zamenjaj korake (`--i` je zaporedna številka koraka, `--j` v krogu).
4. Na strani Projekti (`src/sl/work.html`, `src/en/work.html`) kopiraj kartico `<li class="site-card">` in jo postavi na vrh seznama. Za kartico »V pripravi« uporabi `site-card site-card--soon` (navodilo je v komentarju na strani).
5. `py tools/build.py`, commit, push.

## Blog

Zapis je datoteka `src/sl/blog/<ime>.html` (angleški prevod z istim imenom v `src/en/blog/`). Predloga: `src/sl/blog/_predloga.html`. Dokler je `status: osnutek`, se zapis ne objavi. Seznam zapisov na `/blog/` se naredi sam.

## Navigacija

Vsaka podstran ima drobtinice (O meni › Projekti › Gobe) in na dnu »Nazaj« na nadrejeno stran ter »Naprej« (`next:` v glavi datoteke). Nadrejene strani so v `PARENT` v `tools/build.py`.

## Kontakt

Stran nima obrazca. Kontakt je gumb za e-pošto (`mailto:` z zadevo), naslov s kopiranjem in povezava na LinkedIn. Vse je v `contact_block()` v `tools/build.py`; naslov in povezava sta v `EMAIL` in `LINKEDIN`.

## Lastna domena: vikapirnat.com

Domena je registrirana pri Webtasy (imenski strežniki `cdns1.controlpanel.si`, `cdns2.controlpanel.si`). Stran streže GitHub Pages.

- `tools/build.py`: `SITE_URL = "https://vikapirnat.com/"`; datoteka `CNAME` v korenu vsebuje `vikapirnat.com`.
- DNS pri Webtasy (vrednosti iz GitHubove dokumentacije »Managing a custom domain for your GitHub Pages site«):
  - 4 zapisi `A` za `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
  - 4 zapisi `AAAA` za `@`: `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
  - zapis `CNAME` za `www` → `vika0615.github.io`
- GitHub: Settings → Pages → Custom domain `vikapirnat.com`, **Enforce HTTPS** vklopljen, ko GitHub izda certifikat.
- Priporočeno: domeno preveri v Settings (profil) → Pages → Add a domain (zapis TXT), da je nihče drug ne more uporabiti za svojo stran.
