#!/usr/bin/env python3
"""Zgradi spletno stran Vike Pirnat. Brez knjižnic, samo Python 3.

    py tools/build.py

1. tools/tokens.json   -> assets/tokens.css  (barve, pisave, razmiki iz design sistema)
   tools/bundle.css    -> assets/bundle.css  (komponente iz design sistema, brez pisav z Googla)
2. src/sl/*.html, src/en/*.html -> strani v korenu repozitorija (glava, noga, skripte)
3. sitemap.xml, robots.txt, 404.html

Pisave (assets/fonts.css, assets/fonts/) gostujejo na strani.

Vsebina strani je v src/. Glava, noga, pas s klicem k pogovoru in obrazec so tukaj,
da so na vseh straneh enaki. Ko je domena pripravljena, spremeni SITE_URL in ponovno zaženi.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SITE_URL = "https://vika0615.github.io/vikapirnat-splet/"  # z domeno: "https://vikapirnat.si/"
FORM_ENDPOINT = ""  # Formspree, npr. "https://formspree.io/f/abcdwxyz"; prazno = obrazec še ni povezan
EMAIL = "vika.pirnat@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/vika-pirnat/"
YEAR = "2026"

# id strani: (pot SL, pot EN). Nova stran = nova vrstica + src/sl/<id>.html + src/en/<id>.html
PAGES = {
    "home": ("", "en/"),
    "services": ("storitve/", "en/services/"),
    "work": ("delo/", "en/work/"),
    "gobe": ("delo/gobe/", "en/work/gobe/"),
    "contact": ("kontakt/", "en/contact/"),
}
NAV = ["home", "services", "work", "contact"]
LANGS = ("sl", "en")

T = {
    "sl": {
        "locale": "sl_SI",
        "nav": {"home": "Kako delam", "services": "Storitve", "work": "Delo", "contact": "Kontakt"},
        "nav_label": "Glavna navigacija",
        "lang_label": "Jezik",
        "theme_label": "Tema",
        "theme": {"system": "Sistem", "light": "Svetla", "dark": "Temna"},
        "skip": "Na vsebino",
        "site": "Vika Pirnat",
        "cta_eyebrow": "Kontakt",
        "cta_title": "Prvi 30-minutni pogovor je brezplačen.",
        "cta_lede": "Povejte mi, kaj gradite, za koga in kje se je zataknilo. Odgovorim osebno.",
        "cta_button": "Pišite mi →",
        "alt_eyebrow": "Raje po e-pošti ali LinkedInu?",
        "copy": "Kopiraj",
        "linkedin": "Pišite mi na LinkedInu ↗",
        "f_subject": "Povpraševanje s spletne strani",
        "f_name": "Ime in podjetje",
        "f_email": "E-pošta",
        "f_stage": "Kje ste zdaj?",
        "f_stages": [("ideja", "Ideja"), ("prototip", "Prototip"), ("produkt", "Produkt z uporabniki")],
        "f_msg": "Kaj gradite, za koga in kje se je zataknilo?",
        "f_send": "Pošlji",
        "f_sending": "Pošiljam …",
        "f_done": "Hvala, sporočilo je poslano. Odgovorim osebno na vaš e-naslov.",
        "f_error": "Sporočila ni bilo mogoče poslati. Pišite mi na " + EMAIL + ".",
        "f_off": "Obrazec še ni povezan. Pišite mi na " + EMAIL + ".",
        "f_privacy": "Podatke iz obrazca uporabim samo za odgovor na vaše sporočilo. Obrazec deluje prek storitve Formspree.",
        "f_hp": "Tega polja ne izpolnjujte",
    },
    "en": {
        "locale": "en_GB",
        "nav": {"home": "How I work", "services": "Services", "work": "Work", "contact": "Contact"},
        "nav_label": "Main navigation",
        "lang_label": "Language",
        "theme_label": "Theme",
        "theme": {"system": "System", "light": "Light", "dark": "Dark"},
        "skip": "Skip to content",
        "site": "Vika Pirnat",
        "cta_eyebrow": "Contact",
        "cta_title": "The first 30-minute call is free.",
        "cta_lede": "Tell me what you're building, who it's for and where you're stuck. I'll reply personally.",
        "cta_button": "Get in touch →",
        "alt_eyebrow": "Prefer email or LinkedIn?",
        "copy": "Copy",
        "linkedin": "Message me on LinkedIn ↗",
        "f_subject": "Enquiry from the website",
        "f_name": "Name and company",
        "f_email": "Email",
        "f_stage": "Where are you now?",
        "f_stages": [("ideja", "Idea"), ("prototip", "Prototype"), ("produkt", "Product with users")],
        "f_msg": "What are you building, for whom, and where are you stuck?",
        "f_send": "Send",
        "f_sending": "Sending …",
        "f_done": "Thank you, your message has been sent. I'll reply personally to your email.",
        "f_error": "The message couldn't be sent. Please email me at " + EMAIL + ".",
        "f_off": "The form isn't connected yet. Please email me at " + EMAIL + ".",
        "f_privacy": "I use the details from this form only to reply to your message. The form runs on Formspree.",
        "f_hp": "Leave this field empty",
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
    return PAGES[page_id][0 if lang == "sl" else 1]


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
    </div>
    <div class="vp-contact">
      <div><a class="vp-btn vp-btn--primary" href="{root}{url_of('contact', lang)}">{s['cta_button']}</a></div>
      {alt_contact(lang)}
    </div>
  </div>
</section>"""


def alt_contact(lang):
    s = T[lang]
    return f"""<div class="vp-contact__alt">
        <p class="vp-eyebrow">{s['alt_eyebrow']}</p>
        <div class="vp-contact__row">
          <span class="vp-contact__email" id="mail">{EMAIL}</span>
          <button class="vp-btn" type="button" data-copy="mail"><span lang="{lang}">{s['copy']}</span></button>
        </div>
        <div><a class="vp-btn vp-btn--quiet" href="{LINKEDIN}" target="_blank" rel="noopener">{s['linkedin']}</a></div>
      </div>"""


def contact_block(lang):
    s = T[lang]
    action = FORM_ENDPOINT or "#"
    off = "" if FORM_ENDPOINT else " data-off"
    options = "\n".join(f'          <option value="{v}">{label}</option>' for v, label in s["f_stages"])
    return f"""<div class="vp-contact">
      <form class="vp-form" data-form action="{action}" method="POST"{off}>
        <input type="hidden" name="_subject" value="{s['f_subject']}">
        <input type="hidden" name="jezik" value="{lang}">
        <div class="site-hp" aria-hidden="true"><label>{s['f_hp']} <input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label></div>
        <div class="vp-field"><label for="f-name">{s['f_name']}</label><input class="vp-input" id="f-name" name="ime" autocomplete="name"></div>
        <div class="vp-field"><label for="f-email">{s['f_email']}</label><input class="vp-input" id="f-email" name="email" type="email" autocomplete="email" required></div>
        <div class="vp-field"><label for="f-stage">{s['f_stage']}</label>
          <select class="vp-input" id="f-stage" name="faza">
{options}
          </select>
        </div>
        <div class="vp-field"><label for="f-msg">{s['f_msg']}</label><textarea class="vp-input" id="f-msg" name="sporocilo" required></textarea></div>
        <div><button class="vp-btn vp-btn--primary" type="submit" data-sending="{s['f_sending']}">{s['f_send']}</button></div>
        <p class="vp-form__done" data-form-done hidden role="status">{s['f_done']}</p>
        <p class="site-form__error" data-form-error hidden role="alert">{s['f_error']}</p>
        <p class="site-form__error" data-form-off hidden role="alert">{s['f_off']}</p>
        <p class="vp-small">{s['f_privacy']}</p>
      </form>
      {alt_contact(lang)}
    </div>"""


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
    <a class="vp-header__name" href="{root}{url_of('home', lang)}">{s['site']}</a>
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


def footer(lang, note):
    s = T[lang]
    note_html = f"\n    <span>{note}</span>" if note else ""
    themes = []
    for m in ("system", "light", "dark"):
        pressed = "true" if m == "system" else "false"
        themes.append(f'<button type="button" data-set-theme="{m}" aria-pressed="{pressed}">{s["theme"][m]}</button>')
    return f"""<div class="vp-wrap">
  <footer class="vp-footer">
    <span>© {YEAR} {s['site']}</span>{note_html}
    <span><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn ↗</a></span>
    <span class="site-theme"><span>{s['theme_label']}</span>
      <span class="vp-lang" role="group" aria-label="{s['theme_label']}">{''.join(themes)}</span>
    </span>
  </footer>
</div>"""


HEAD_THEME = "(function(){try{var t=localStorage.getItem('vp-theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}catch(e){}})();"


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
<link rel="preload" href="{root}assets/fonts/red-hat-text-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/red-hat-display-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/fonts.css">
<link rel="stylesheet" href="{root}assets/tokens.css">
<link rel="stylesheet" href="{root}assets/bundle.css">
<link rel="stylesheet" href="{root}assets/site.css">
</head>
<body data-lang="{lang}">
{header(lang, root, page_id, meta.get('nav', page_id))}
<main id="vsebina">
{body.strip()}
</main>
{footer(lang, meta.get('footnote', ''))}
<script src="{root}assets/bundle.js"></script>{scripts}
<script src="{root}assets/site.js"></script>
</body>
</html>
"""


def build_pages():
    for lang in LANGS:
        for page_id in PAGES:
            src = ROOT / "src" / lang / f"{page_id}.html"
            meta, body = parse_fragment(src.read_text(encoding="utf-8"))
            out = ROOT / url_of(page_id, lang) / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(page(lang, page_id, meta, body), encoding="utf-8", newline="\n")


def build_extras():
    urls = "\n".join(
        f"  <url><loc>{SITE_URL}{url_of(p, l)}</loc></url>" for p in PAGES for l in LANGS
    )
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
<link rel="stylesheet" href="{base}assets/fonts.css">
<link rel="stylesheet" href="{base}assets/tokens.css">
<link rel="stylesheet" href="{base}assets/bundle.css">
<link rel="stylesheet" href="{base}assets/site.css">
</head>
<body data-lang="sl">
<div class="vp-wrap">
  <header class="vp-header"><a class="vp-header__name" href="{base}">Vika Pirnat</a></header>
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
