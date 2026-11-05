#!/usr/bin/env python3
"""Zgradi spletno stran Vike Pirnat. Brez knjižnic, samo Python 3.

    py tools/build.py

1. tools/tokens.json   -> assets/tokens.css  (barve, pisave, razmiki iz design sistema)
   tools/bundle.css    -> assets/bundle.css  (komponente iz design sistema, brez pisav z Googla)
2. src/sl/*.html, src/en/*.html -> strani v korenu repozitorija (glava, noga, skripte)
3. sitemap.xml, robots.txt, 404.html

Pisave (assets/fonts.css, assets/fonts/) gostujejo na strani.

Vsebina strani je v src/. Glava, noga, pas s klicem k pogovoru in kontakt so tukaj,
da so na vseh straneh enaki. Ko je domena pripravljena, spremeni SITE_URL in ponovno zaženi.
"""
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent

SITE_URL = "https://vikapirnat.com/"  # lastna domena (datoteka CNAME); prej https://vika0615.github.io/vikapirnat-splet/
EMAIL = "vika.pirnat@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/vika-pirnat/"
GOBE_PLAY = "https://play.google.com/store/apps/details?id=io.github.vika0615.gobe"
# Uradni gumb Google Play (nespremenjen, iz play.google.com/intl/en_us/badges). Za jezik brez gumba ostane besedilni gumb.
PLAY_BADGE = {"sl": "assets/img/badges/google-play-sl.png", "en": "assets/img/badges/google-play-en.png"}
YEAR = "2026"
# Analitika: PostHog EU brez piškotkov (cookieless_mode "always"; v projektu vklopljeno »Enable cookieless tracking«).
# Projekt je isti kot za aplikacijo Gobe (brezplačen paket dovoli en projekt); dogodke strani loči lastnost $host.
# Pošilja samo na vikapirnat.com, ne lokalno. Vika svoje obiske izklopi z ?brez-analitike (vklopi z ?z-analitiko).
POSTHOG_KEY = "phc_qcTxKMxqicwLq6bWYLHHncrDpWL37qh4yPaEoa363g6V"
POSTHOG_HOST = "https://eu.i.posthog.com"
ANALYTICS_HOSTS = ("vikapirnat.com", "www.vikapirnat.com")

# id strani: (pot SL, pot EN). Nova stran = nova vrstica + src/sl/<id>.html + src/en/<id>.html
PAGES = {
    "home": ("", "en/"),
    "work": ("projekti/", "en/projects/"),
    "gobe": ("projekti/gobe/", "en/projects/gobe/"),
    "blog": ("blog/", "en/blog/"),
    "contact": ("kontakt/", "en/contact/"),
    "privacy": ("zasebnost/", "en/privacy/"),
}
NAV = ["home", "work", "blog"]
# Noga ima še kontakt (v meniju ga ni, ker je na vsaki strani pas s kontaktom)
FOOT_NAV = NAV + ["contact", "privacy"]
# Drobtinice in »Nazaj«: nadrejena stran. Zapisi na blogu (post:<ime>) imajo za starša blog.
PARENT = {"work": "home", "gobe": "work", "blog": "home", "contact": "home", "privacy": "home"}
# Zapisi na blogu: src/<jezik>/blog/<ime>.html (datoteke z _ na začetku so predloge). Napolni collect_posts().
POSTS = {"sl": {}, "en": {}}
LANGS = ("sl", "en")

T = {
    "sl": {
        "locale": "sl_SI",
        "nav": {"home": "O meni", "work": "Projekti", "blog": "Blog", "contact": "Kontakt", "privacy": "Zasebnost"},
        "crumb": {"gobe": "Gobe"},
        "crumbs_label": "Kje ste",
        "pager_label": "Naprej ali nazaj",
        "back": "Nazaj",
        "next": "Naprej",
        "footer_nav": "Strani",
        "posts_empty": "Prvi zapis je v pripravi.",
        "months": ["jan.", "feb.", "mar.", "apr.", "maj", "jun.", "jul.", "avg.", "sep.", "okt.", "nov.", "dec."],
        "nav_label": "Glavna navigacija",
        "lang_label": "Jezik",
        "theme_label": "Tema",
        "theme": {"system": "Sistem", "light": "Svetla", "dark": "Temna"},
        "skip": "Na vsebino",
        "site": "Vika Pirnat",
        "cta_eyebrow": "Kontakt",
        "cta_title": "Stopite z mano v stik.",
        "cta_lede": "Povejte mi, kaj gradite, za koga in kje se je zataknilo. Odgovorim osebno.",
        "cta_open": "Odprta sem za pogodbeno delo, skupen projekt ali zaposlitev.",
        "c_write": "Pišite mi →",
        "c_subject": "Povpraševanje s spletne strani",
        "c_mail": "E-pošta",
        "copy": "Kopiraj",
        "linkedin": "Pišite mi na LinkedInu ↗",
        "stores": "Prenos aplikacije Gobe",
        "play_k": "Prenesi za Android",
        "ios_k": "V pripravi",
        "ios_n": "Apple",
        "play_alt": "Na voljo v Googlu Play",
        "play_legal": "Google Play in logotip Google Play sta blagovni znamki družbe Google LLC.",
    },
    "en": {
        "locale": "en_GB",
        "nav": {"home": "About", "work": "Projects", "blog": "Blog", "contact": "Contact", "privacy": "Privacy"},
        "crumb": {"gobe": "Gobe"},
        "crumbs_label": "You are here",
        "pager_label": "Next or back",
        "back": "Back",
        "next": "Next",
        "footer_nav": "Pages",
        "posts_empty": "The first post is on its way.",
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "nav_label": "Main navigation",
        "lang_label": "Language",
        "theme_label": "Theme",
        "theme": {"system": "System", "light": "Light", "dark": "Dark"},
        "skip": "Skip to content",
        "site": "Vika Pirnat",
        "cta_eyebrow": "Contact",
        "cta_title": "Let's talk.",
        "cta_lede": "Tell me what you're building, who it's for and where you're stuck. I'll reply personally.",
        "cta_open": "I'm open to contract work, a joint project or employment.",
        "c_write": "Email me →",
        "c_subject": "Enquiry from the website",
        "c_mail": "Email",
        "copy": "Copy",
        "linkedin": "Message me on LinkedIn ↗",
        "stores": "Get the Gobe app",
        "play_k": "Download for Android",
        "ios_k": "Coming soon",
        "ios_n": "Apple",
        "play_alt": "Get it on Google Play",
        "play_legal": "Google Play and the Google Play logo are trademarks of Google LLC.",
    },
}


# ---------- 1. tokens.css ----------

def build_tokens():
    data = json.loads((ROOT / "tools" / "tokens.json").read_text(encoding="utf-8"))
    colors = data["color"]["tokens"]

    def val(v):
        m = re.fullmatch(r"\{([a-z0-9-]+)\}", v)
        return f"var(--{m.group(1)})" if m else v

    def theme_block(theme, indent="  "):
        lines = []
        for t in colors:
            v = t["value"]
            if isinstance(v, dict):
                lines.append(f"{indent}--{t['name']}: {v[theme]};")
        lines.append(f"{indent}color-scheme: {theme};")
        return "\n".join(lines)

    static = []
    for name, fam in data["type"]["families"].items():
        static.append(f"  --font-{name}: {fam};")
    for group in ("spacing", "radius", "layout"):
        for t in data[group]["tokens"]:
            static.append(f"  --{t['name']}: {t['value']};")
    for t in colors:
        if not isinstance(t["value"], dict):
            static.append(f"  --{t['name']}: {val(t['value'])};")

    css = f"""/* Ustvarjeno iz tools/tokens.json (design sistem Vika Pirnat, različica {data.get('version', '')}).
   Ne urejaj ročno: spremeni tokens.json in zaženi `py tools/build.py`.
   Privzeta je temna tema; svetla velja, kadar jo ima brskalnik ali jo izbere obiskovalec. */

:root {{
{chr(10).join(static)}
{theme_block('dark')}
}}

@media (prefers-color-scheme: light) {{
  :root:not([data-theme="dark"]) {{
{theme_block('light', '    ')}
  }}
}}

:root[data-theme="light"] {{
{theme_block('light')}
}}

:root[data-theme="dark"] {{
{theme_block('dark')}
}}
"""
    (ROOT / "assets" / "tokens.css").write_text(css, encoding="utf-8", newline="\n")


def build_bundle():
    """tools/bundle.css je nespremenjena kopija iz design sistema. Na strani gre brez @import
    pisav z Googla: pisave so v assets/fonts.css in assets/fonts/, da obiskovalčev IP ne gre k Googlu."""
    css = (ROOT / "tools" / "bundle.css").read_text(encoding="utf-8")
    css = re.sub(r'@import url\("https://fonts\.googleapis\.com[^)]*\);\s*', "", css)
    head = "/* Ustvarjeno iz tools/bundle.css (kopija iz design sistema), brez @import pisav. Ne urejaj ročno. */\n"
    (ROOT / "assets" / "bundle.css").write_text(head + css, encoding="utf-8", newline="\n")


# ---------- 2. strani ----------

def url_of(page_id, lang):
    if page_id.startswith("post:"):
        slug = page_id[5:]
        if slug not in POSTS[lang]:
            return url_of("blog", lang)  # zapis v drugem jeziku še ne obstaja
        return ("blog/" if lang == "sl" else "en/blog/") + slug + "/"
    return PAGES[page_id][0 if lang == "sl" else 1]


def label_of(page_id, lang):
    s = T[lang]
    if page_id.startswith("post:"):
        return POSTS[lang][page_id[5:]]["title_short"]
    return s["crumb"].get(page_id) or s["nav"][page_id]


def parent_of(page_id):
    return "blog" if page_id.startswith("post:") else PARENT.get(page_id)


def fmt_date(iso, lang):
    y, m, d = (int(x) for x in iso.split("-"))
    mon = T[lang]["months"][m - 1]
    return f"{d}. {mon} {y}" if lang == "sl" else f"{d} {mon} {y}"


def depth(path):
    return path.count("/")


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def parse_fragment(text):
    m = re.match(r"\s*<!--(.*?)-->\s*", text, re.S)
    meta = {}
    if m:
        for line in m.group(1).strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    return meta, text


def cta_band(lang, root, page_id):
    s = T[lang]
    return f"""<section class="vp-band" aria-labelledby="cta-title">
  <div class="vp-wrap vp-band__inner">
    <div class="site-stack">
      <p class="vp-eyebrow">{s['cta_eyebrow']}</p>
      <h2 class="vp-h2" id="cta-title">{s['cta_title']}</h2>
      <p class="vp-lede">{s['cta_lede']}</p>
      <p class="vp-small">{s['cta_open']}</p>
    </div>
    {contact_block(lang)}
  </div>
</section>"""


def contact_block(lang):
    """Brez obrazca (GitHub Pages ga ne streže): e-pošta s kopiranjem in LinkedIn."""
    s = T[lang]
    mailto = f"mailto:{EMAIL}?subject={quote(s['c_subject'])}"
    return f"""<div class="vp-contact">
      <div><a class="vp-btn vp-btn--primary" href="{mailto}">{s['c_write']}</a></div>
      <div class="vp-contact__alt">
        <p class="vp-eyebrow">{s['c_mail']}</p>
        <div class="vp-contact__row">
          <span class="vp-contact__email" id="mail">{EMAIL}</span>
          <button class="vp-btn" type="button" data-copy="mail"><span lang="{lang}">{s['copy']}</span></button>
        </div>
        <div><a class="vp-btn vp-btn--quiet" href="{LINKEDIN}" target="_blank" rel="noopener">{s['linkedin']}</a></div>
      </div>
    </div>"""


def stores_block(lang, root):
    """Gumba za aplikacijo Gobe: Google Play (deluje) in iPhone (v pripravi, utripa).
    Applovega gumba »App Store« ne smemo uporabiti, dokler aplikacija ni v App Storu (Applova pravila)."""
    s = T[lang]
    if lang in PLAY_BADGE:
        play = f'<a class="site-store-badge site-store-badge--{lang}" href="{GOBE_PLAY}" target="_blank" rel="noopener"><img src="{root}{PLAY_BADGE[lang]}" width="646" height="250" alt="{s["play_alt"]}"></a>'
    else:
        play = f'<a class="site-store" href="{GOBE_PLAY}" target="_blank" rel="noopener"><span class="site-store__k">{s["play_k"]}</span><span class="site-store__n">Google Play ↗</span></a>'
    return f"""<div class="site-stores" role="group" aria-label="{s['stores']}">
          {play}
          <span class="site-store site-store--soon"><span class="site-store__k"><span class="site-dot site-dot--soon" aria-hidden="true"></span>{s['ios_k']}</span><span class="site-store__n">{s['ios_n']}</span></span>
        </div>"""


# Ime kot znak, povsod enako: Bricolage Grotesque, veliki začetnici, zeleni piki na i (brez utripanja).
WM = 'V<span class="site-wm__i">ı</span>ka P<span class="site-wm__i">ı</span>rnat'


def name_html(extra=""):
    """Ime za besedilo (naslov na domači strani, noga): bralniki zaslona preberejo »Vika Pirnat«."""
    return f'<span class="site-sr">Vika Pirnat</span><span class="site-wm{extra}" aria-hidden="true">{WM}</span>'


def wordmark(href):
    return f'<a class="site-mark" href="{href}" aria-label="Vika Pirnat"><span class="site-wm" aria-hidden="true">{WM}</span></a>'


def crumbs(lang, root, page_id):
    """Drobtinice: O meni › Projekti › Gobe. Na domači strani jih ni."""
    if page_id == "home":
        return ""
    chain, cur = [], page_id
    while cur:
        chain.append(cur)
        cur = parent_of(cur)
    chain.reverse()
    items = [f'<li><a href="{root}{url_of(pid, lang)}">{label_of(pid, lang)}</a></li>' for pid in chain[:-1]]
    items.append(f'<li aria-current="page">{label_of(chain[-1], lang)}</li>')
    return f"""<div class="vp-wrap">
  <nav class="site-crumbs" aria-label="{T[lang]['crumbs_label']}"><ol>{''.join(items)}</ol></nav>
</div>"""


def pager(lang, root, page_id, next_id):
    """Na dnu vsake podstrani: nazaj na nadrejeno stran in naprej na naslednjo, da obiskovalec ne obstane."""
    if page_id == "home":
        return ""
    s = T[lang]
    back = parent_of(page_id)
    left = f'<a class="site-pager__link" href="{root}{url_of(back, lang)}"><span class="site-pager__k">← {s["back"]}</span><span class="site-pager__t">{label_of(back, lang)}</span></a>'
    right = ""
    if next_id:
        right = f'<a class="site-pager__link site-pager__link--next" href="{root}{url_of(next_id, lang)}"><span class="site-pager__k">{s["next"]} →</span><span class="site-pager__t">{label_of(next_id, lang)}</span></a>'
    return f"""<div class="vp-wrap">
  <nav class="site-pager" aria-label="{s['pager_label']}">{left}{right}</nav>
</div>"""


def posts_list(lang, root):
    posts = sorted(POSTS[lang].items(), key=lambda kv: kv[1]["date"], reverse=True)
    if not posts:
        return f'<p class="site-posts-empty"><span class="site-dot site-dot--soon" aria-hidden="true"></span>{T[lang]["posts_empty"]}</p>'
    items = []
    for slug, m in posts:
        items.append(f"""<li><a href="{root}{url_of('post:' + slug, lang)}"><time datetime="{m['date']}">{fmt_date(m['date'], lang)}</time><h2>{m['title_short']}</h2><p>{m.get('description', '')}</p></a></li>""")
    return f'<ul class="site-posts">{"".join(items)}</ul>'


def header(lang, root, page_id, nav_key):
    s = T[lang]
    nav = []
    for key in NAV:
        cur = ' aria-current="page"' if key == nav_key else ""
        nav.append(f'<a href="{root}{url_of(key, lang)}"{cur}>{s["nav"][key]}</a>')
    langs = []
    for l, label in (("sl", "SLO"), ("en", "ENG")):
        cur = ' aria-current="true"' if l == lang else ""
        langs.append(f'<a href="{root}{url_of(page_id, l)}" hreflang="{l}"{cur}>{label}</a>')
    return f"""<a class="site-skip" href="#vsebina">{s['skip']}</a>
<div class="vp-wrap">
  <header class="vp-header">
    {wordmark(root + url_of('home', lang))}
    <div class="vp-header__end">
      <nav class="vp-header__nav" aria-label="{s['nav_label']}">
        {chr(10).join('        ' + n for n in nav).strip()}
      </nav>
      <div class="vp-lang" role="group" aria-label="{s['lang_label']}">
        {''.join(langs)}
      </div>
    </div>
  </header>
</div>"""


def footer(lang, root, note):
    s = T[lang]
    note_html = f"\n    <span>{note}</span>" if note else ""
    themes = []
    for m in ("system", "light", "dark"):
        pressed = "true" if m == "system" else "false"
        themes.append(f'<button type="button" data-set-theme="{m}" aria-pressed="{pressed}">{s["theme"][m]}</button>')
    return f"""<div class="vp-wrap">
  <footer class="vp-footer">
    <span>© {YEAR} {name_html(' site-wm--sm')}</span>{note_html}
    <nav class="site-footnav" aria-label="{s['footer_nav']}">{' · '.join(f'<a href="{root}{url_of(k, lang)}">{s["nav"][k]}</a>' for k in FOOT_NAV)}</nav>
    <span><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn ↗</a></span>
    <span class="site-theme"><span>{s['theme_label']}</span>
      <span class="vp-lang" role="group" aria-label="{s['theme_label']}">{''.join(themes)}</span>
    </span>
  </footer>
</div>"""


# Uradni nalagalnik posthog-js (skrajšan seznam metod), init samo na lastni domeni.
HEAD_ANALYTICS = (
    "(function(){var h=location.hostname;if(" + "&&".join(f"h!=='{d}'" for d in ANALYTICS_HOSTS) + ")return;"
    "try{var q=location.search;if(q.indexOf('brez-analitike')>-1)localStorage.setItem('vp-notrack','1');"
    "if(q.indexOf('z-analitiko')>-1)localStorage.removeItem('vp-notrack');if(localStorage.getItem('vp-notrack')==='1')return}catch(e){}"
    "!function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split('.');"
    "2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}"
    "(p=t.createElement('script')).type='text/javascript',p.crossOrigin='anonymous',p.async=!0,"
    "p.src=s.api_host.replace('.i.posthog.com','-assets.i.posthog.com')+'/static/array.js',"
    "(r=t.getElementsByTagName('script')[0]).parentNode.insertBefore(p,r);var u=e;"
    "for(void 0!==a?u=e[a]=[]:a='posthog',u.people=u.people||[],u.toString=function(t){var e='posthog';"
    "return'posthog'!==a&&(e+='.'+a),t||(e+=' (stub)'),e},u.people.toString=function(){return u.toString(1)+'.people (stub)'},"
    "o='capture register register_once unregister get_distinct_id get_session_id reset set_config debug'.split(' '),n=0;n<o.length;n++)g(u,o[n]);"
    "e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);"
    f"posthog.init('{POSTHOG_KEY}',{{api_host:'{POSTHOG_HOST}',cookieless_mode:'always',person_profiles:'identified_only',"
    "capture_pageview:true,capture_pageleave:true,disable_session_recording:true,disable_surveys:true})})();"
)

HEAD_THEME = "document.documentElement.classList.add('js');(function(){try{var t=localStorage.getItem('vp-theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}catch(e){}})();"


def page(lang, page_id, meta, body):
    path = url_of(page_id, lang)
    root = "../" * depth(path)
    s = T[lang]
    title = meta.get("title", s["site"])
    desc = meta.get("description", "")
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{SITE_URL}{url_of(page_id, l)}">' for l in LANGS
    )
    scripts = "".join(
        f'\n<script src="{root}assets/{src.strip()}"></script>' for src in meta.get("scripts", "").split(",") if src.strip()
    )
    body = body.replace("{{cta}}", cta_band(lang, root, page_id))
    body = body.replace("{{contact}}", contact_block(lang))
    note = meta.get("footnote", "")
    if "{{stores}}" in body and lang in PLAY_BADGE:
        note = (note + " · " if note else "") + s["play_legal"]
    body = body.replace("{{stores}}", stores_block(lang, root))
    body = body.replace("{{posts}}", posts_list(lang, root))
    body = body.replace("{{name}}", name_html())
    if page_id.startswith("post:"):
        m = POSTS[lang][page_id[5:]]
        body = body.replace("{{date}}", f'<time datetime="{m["date"]}">{fmt_date(m["date"], lang)}</time>')
    body = body.replace("{{email}}", EMAIL).replace("{{linkedin}}", LINKEDIN)
    body = re.sub(r"\{\{href:([a-z0-9-]+)\}\}", lambda m: root + url_of(m.group(1), lang), body)
    body = body.replace("{{root}}", root)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{SITE_URL}{path}">
{alternates}
<link rel="alternate" hreflang="x-default" href="{SITE_URL}{url_of(page_id, 'sl')}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{SITE_URL}{path}">
<meta property="og:locale" content="{s['locale']}">
<link rel="icon" href="data:,">
<script>{HEAD_THEME}</script>
<script>{HEAD_ANALYTICS}</script>
<link rel="preload" href="{root}assets/fonts/red-hat-text-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/red-hat-display-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/bricolage-grotesque-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/fonts.css">
<link rel="stylesheet" href="{root}assets/tokens.css">
<link rel="stylesheet" href="{root}assets/bundle.css">
<link rel="stylesheet" href="{root}assets/site.css">
</head>
<body data-lang="{lang}">
{header(lang, root, page_id, meta.get('nav', page_id))}
{crumbs(lang, root, page_id)}
<main id="vsebina">
{body.strip()}
</main>
{pager(lang, root, page_id, meta.get('next'))}
{footer(lang, root, note)}
<script src="{root}assets/bundle.js"></script>{scripts}
<script src="{root}assets/site.js"></script>
</body>
</html>
"""


def collect_posts():
    for lang in LANGS:
        folder = ROOT / "src" / lang / "blog"
        for f in (sorted(folder.glob("*.html")) if folder.exists() else []):
            if f.name.startswith("_"):
                continue
            meta, body = parse_fragment(f.read_text(encoding="utf-8"))
            if meta.get("status", "objavljeno") in ("osnutek", "draft"):
                continue
            meta.setdefault("title_short", meta.get("title", f.stem).split(" · ")[0])
            POSTS[lang][f.stem] = {**meta, "_body": body}


def build_pages():
    collect_posts()
    for lang in LANGS:
        for slug, m in POSTS[lang].items():
            pid = "post:" + slug
            out = ROOT / url_of(pid, lang) / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(page(lang, pid, {**m, "nav": "blog"}, m["_body"]), encoding="utf-8", newline="\n")
        for page_id in PAGES:
            src = ROOT / "src" / lang / f"{page_id}.html"
            meta, body = parse_fragment(src.read_text(encoding="utf-8"))
            out = ROOT / url_of(page_id, lang) / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(page(lang, page_id, meta, body), encoding="utf-8", newline="\n")


def build_extras():
    urls = "\n".join(
        f"  <url><loc>{SITE_URL}{url_of(p, l)}</loc></url>" for p in PAGES for l in LANGS
    ) + "".join(f"\n  <url><loc>{SITE_URL}{url_of('post:' + s, l)}</loc></url>" for l in LANGS for s in POSTS[l])
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8", newline="\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nDisallow: /src/\nDisallow: /tools/\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8", newline="\n")
    base = SITE_URL
    (ROOT / "404.html").write_text(f"""<!doctype html>
<html lang="sl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Te strani ni · Vika Pirnat</title>
<meta name="robots" content="noindex">
<link rel="icon" href="data:,">
<script>{HEAD_THEME}</script>
<script>{HEAD_ANALYTICS}</script>
<link rel="stylesheet" href="{base}assets/fonts.css">
<link rel="stylesheet" href="{base}assets/tokens.css">
<link rel="stylesheet" href="{base}assets/bundle.css">
<link rel="stylesheet" href="{base}assets/site.css">
</head>
<body data-lang="sl">
<div class="vp-wrap">
  <header class="vp-header">{wordmark(base)}</header>
  <section class="site-intro">
    <p class="vp-eyebrow">404</p>
    <h1 class="vp-h1">Te strani ni.</h1>
    <p class="vp-lede">Morda je naslov napačen ali pa je stran prestavljena.</p>
    <div class="site-actions"><a class="vp-btn vp-btn--primary" href="{base}">Na začetno stran →</a></div>
    <p class="vp-small"><span>This page doesn't exist.</span> <a href="{base}en/" hreflang="en">Go to the English home page →</a></p>
  </section>
</div>
</body>
</html>
""", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    build_tokens()
    build_bundle()
    build_pages()
    build_extras()
    print("Zgrajeno:", ", ".join(f"/{url_of(p, l)}" for l in LANGS for p in PAGES))
