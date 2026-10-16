"""The website's own pages, around the guides: the landing page (every kit), a page per kit (its guides), and the 404 page.

    python3 tools/site_pages.py            (tools/publish.py runs it after every publish, restore and take-down)

They are made from guides.json and from what is in site/ now, so a kit appears once one of its guides is published and a guide
once it is on the site; nothing else is listed. Header and footer copy TechBox's LMS (edu.tech-box.io). The pages link to the
guides (opened in the same tab, full window); nothing is offered for download. Links are from the site's root, because Render
serves /kits/x as well as /kits/x/.

Framing: these pages may not be shown inside any frame (render.yaml sends X-Frame-Options: DENY on every path, and a line of
script here is a second guard); a guide may be framed only by guides.json "embed_origins" (TechBox's LMS). This script writes
the guides' own second guard, assets/frame-guard.js (each published guide's index.html loads it), from embed_origins, so a new
LMS address reaches every guide without publishing them again; and, for the real site, render.yaml's per-guide
Content-Security-Policy rules, between its "BEGIN guide framing" and "END guide framing" lines: two rules per guide (/<guide>
and /<guide>/*), and never a Content-Security-Policy on /* (Render picks one value at random when two rules with the same
header name match a path). Only the standard library.
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / 'site'
SOURCE_ASSETS = Path(__file__).resolve().parent / 'site_assets'      # the TechBox wordmark, copied from the LMS
YEAR = 2026
NAME = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
ORIGIN = re.compile(r'^https://[a-z0-9-]+(\.[a-z0-9-]+)+(:[0-9]{1,5})?$')
RESERVED = ('kits', 'assets')


def validate(spec):
    """guides.json, checked (the tools that read it all call this): web-address names, each guide's kit, its label, and the LMS
    addresses (lower case, https, no path or slash: the guard compares them exactly)."""
    kits, guides, origins = spec.get('kits', {}), spec.get('guides', {}), spec.get('embed_origins')
    errors = [f'"{n}" is not a web-address name (lower-case words joined by hyphens)' for n in list(kits) + list(guides) if not NAME.match(n)]
    errors += [f'"{n}" would clash with a page of the website' for n in list(guides) + list(kits) if n in RESERVED]
    errors += [f'guide "{n}" is also the name of a kit' for n in guides if n in kits]
    errors += [f'guide "{n}" names kit "{g.get("kit")}", which is not under "kits"' for n, g in guides.items() if g.get('kit') not in kits]
    errors += [f'guide "{n}" has no "label" (how its card is named)' for n, g in guides.items() if not g.get('label')]
    errors += [f'kit "{n}" has no "name" or "folder"' for n, k in kits.items() if not k.get('name') or not k.get('folder')]
    if not isinstance(origins, list) or not origins:
        errors.append('"embed_origins" must list the LMS address(es), e.g. ["https://edu.tech-box.io"]')
    else:
        errors += [f'embed_origins: "{o}" is not an address like https://edu.tech-box.io (lower case, no path or slash)' for o in origins if not ORIGIN.match(str(o))]
    if errors:
        raise SystemExit('guides.json: ' + '; '.join(errors))
    return spec


def frame_guard_js(spec):
    """The guides' second guard against framing (the server's Content-Security-Policy is the real check): it refuses only a
    definite foreign origin ("null", no referrer or our own: the header decides), and lets this computer frame a guide."""
    return r"""// Only TechBox's LMS may show a guide inside a frame: the server's Content-Security-Policy frame-ancestors is the real check,
// this is a second guard (made by tools/site_pages.py from guides.json embed_origins; every published guide loads it).
(function () {
  if (window.top === window.self) return;
  var allowed = ORIGINS, bad = false, ao = location.ancestorOrigins;
  var local = function (o) { return /^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(o); };
  if (ao && ao.length) {
    for (var i = 0; i < ao.length; i++) if (ao[i] !== 'null' && allowed.indexOf(ao[i]) < 0 && !local(ao[i])) bad = true;
  } else if (document.referrer) {
    try { var o = new URL(document.referrer).origin; if (o !== location.origin && allowed.indexOf(o) < 0 && !local(o)) bad = true; } catch (e) {}
  }
  if (!bad) return;
  window.techboxFrameRefused = true;
  document.documentElement.style.visibility = 'hidden';
  document.addEventListener('DOMContentLoaded', function () {
    var p = document.createElement('p'), a = document.createElement('a');
    a.href = location.href; a.target = '_blank'; a.rel = 'noopener'; a.textContent = 'Open this build guide in a new tab';
    p.style.cssText = 'font:16px system-ui,sans-serif;padding:16px'; p.appendChild(a);
    document.body.replaceChildren(p); document.documentElement.style.visibility = '';
  });
})();
""".replace('ORIGINS', json.dumps(spec['embed_origins']))

FRAME_GUARD = """<script>
// This page is not to be shown inside a frame (only a guide may be, and only by TechBox's LMS); the server's X-Frame-Options:
// DENY is the real check, this is a second guard.
if (window.top !== window.self) {
  document.documentElement.style.visibility = 'hidden';
  document.addEventListener('DOMContentLoaded', function () {
    var p = document.createElement('p'), a = document.createElement('a');
    a.href = location.href; a.target = '_blank'; a.rel = 'noopener'; a.textContent = 'Open the TechBox build guides in a new tab';
    p.style.cssText = 'font:16px system-ui,sans-serif;padding:16px'; p.appendChild(a);
    document.body.replaceChildren(p); document.documentElement.style.visibility = '';
  });
}
</script>"""
BEGIN, END = '# BEGIN guide framing', '# END guide framing'


ICONS = {
    'LinkedIn': ('https://www.linkedin.com/', '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect width="4" height="12" x="2" y="9"></rect><circle cx="4" cy="4" r="2"></circle>'),
    'Facebook': ('https://www.facebook.com/TechBoxIO', '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path>'),
    'Instagram': ('https://www.instagram.com/techbox.io/', '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"></line>'),
}

CSS = """:root{--blue:#00b0f0;--blue-dark:#0090c8;--ink:#1f2937;--muted:#5b6472;--page:#f5f7fa;--card:#fff;--line:#e3e8ef}
*{box-sizing:border-box}
html,body{margin:0}
body{background:var(--page);color:var(--ink);font-family:Inter,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.5;display:flex;flex-direction:column;min-height:100vh}
a{color:inherit}
.top{position:sticky;top:0;z-index:5;background:var(--blue);box-shadow:0 2px 6px rgba(0,0,0,.12)}
.top .in{padding:8px 32px;display:flex;align-items:center;justify-content:space-between}
.top img{display:block;width:300px;height:70px;object-fit:contain}
main{flex:1;width:100%;max-width:1200px;margin:0 auto;padding:40px 32px 64px}
h1{font-size:34px;line-height:1.2;margin:0 0 6px}
.lead{color:var(--muted);margin:0 0 32px;font-size:17px}
.crumbs{font-size:14px;color:var(--muted);margin:0 0 14px}
.crumbs a{color:var(--blue-dark);text-decoration:none}.crumbs a:hover{text-decoration:underline}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:24px;list-style:none;margin:0;padding:0}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;transition:box-shadow .15s,transform .15s}
.card:hover,.card:focus-within{box-shadow:0 10px 28px rgba(15,35,60,.12);transform:translateY(-2px)}
.card a.main{text-decoration:none;display:flex;flex-direction:column;flex:1;outline:none}
.card a.main:focus-visible{box-shadow:inset 0 0 0 3px var(--blue)}
.card .pic{aspect-ratio:16/10;background:#fff;display:flex;align-items:center;justify-content:center;border-bottom:1px solid var(--line)}
.card .pic img{width:100%;height:100%;object-fit:contain}
.card .pic .none{color:#9aa3ae;font-size:14px}
.card .body{padding:16px 18px 18px;display:flex;flex-direction:column;gap:4px;flex:1}
.card h2{font-size:19px;margin:0}
.card .sub{color:var(--muted);font-size:14px;margin:0}
.card .go{margin-top:auto;padding-top:12px;color:var(--blue-dark);font-weight:600;font-size:15px}
.empty{color:var(--muted)}
footer{background:var(--blue);color:#fff;padding:48px 0}
footer .in{max-width:1200px;margin:0 auto;padding:0 32px}
footer .cols{display:grid;grid-template-columns:repeat(4,1fr);gap:32px}
footer h4{margin:0 0 16px;font-size:16px;font-weight:600}
footer p,footer li{color:rgba(255,255,255,.8);margin:0 0 8px}
footer ul{list-style:none;margin:0;padding:0}
footer a{text-decoration:none}footer a:hover{color:#fff}
footer .mail{text-decoration:underline}
footer .logo{display:block;width:200px;height:47px;margin:0 0 16px}
footer .social{display:flex;gap:16px}
footer .social a{width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,.1);display:flex;align-items:center;justify-content:center;color:#fff}
footer .social a:hover{background:rgba(255,255,255,.2)}
footer .social svg{width:20px;height:20px}
footer .base{border-top:1px solid rgba(255,255,255,.2);margin-top:32px;padding-top:32px;display:flex;justify-content:space-between;align-items:center;color:rgba(255,255,255,.8);gap:16px}
footer .base p{margin:0}
footer .base nav{display:flex;gap:24px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
@media (max-width:760px){.top .in{padding:8px 16px}.top img{width:200px;height:47px}main{padding:28px 16px 48px}h1{font-size:27px}
  footer .cols{grid-template-columns:1fr;text-align:center}footer .logo{margin:0 auto 16px}footer .social{justify-content:center}
  footer .base{flex-direction:column;text-align:center}}
"""


def esc(s):
    return html.escape(str(s), quote=True)


def page(title, body):
    social = ''.join(f'<a href="{url}" target="_blank" rel="noopener" aria-label="{name}"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{svg}</svg></a>'
                     for name, (url, svg) in ICONS.items())
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><meta name="robots" content="noindex"><link rel="icon" href="data:,">
{FRAME_GUARD}
<link rel="stylesheet" href="/assets/site.css">
</head><body>
<header class="top"><div class="in"><a href="/" aria-label="TechBox build guides: home"><img src="/assets/techbox-wordmark-white.svg" alt="TechBox" width="300" height="70"></a></div></header>
<main>
{body}
</main>
<footer><div class="in">
<div class="cols">
<div><img class="logo" src="/assets/techbox-wordmark-white.svg" alt="TechBox" width="200" height="47"><p>Empowering educators and students through innovative STEM education.</p></div>
<div><h4>Log-In</h4><ul><li><a href="https://edu.tech-box.io/educator/auth">Educator</a></li><li><a href="https://edu.tech-box.io/student/auth">Student</a></li></ul></div>
<div><h4>Support for Educators</h4><p><a class="mail" href="mailto:support@tech-box.io">support@tech-box.io</a></p><p>Mon–Fri, 8–6 ET</p></div>
<div><h4>Connect</h4><div class="social">{social}</div></div>
</div>
<div class="base"><p>© {YEAR} TechBox. All rights reserved.</p><nav aria-label="Policies"><a href="https://tech-box.io/policies/privacy-policy" target="_blank" rel="noopener">Privacy Policy</a><a href="https://tech-box.io/policies/terms-of-service" target="_blank" rel="noopener">Terms of Service</a></nav></div>
</div></footer>
</body></html>
"""


def card(href, picture, title, sub, go):
    pic = f'<img src="{esc(picture)}" alt="" loading="lazy" width="960" height="600">' if picture else '<span class="none">No picture yet</span>'
    return (f'<li class="card"><a class="main" href="{esc(href)}"><div class="pic">{pic}</div><div class="body">'
            f'<h2>{esc(title)}</h2>{f"<p class=sub>{esc(sub)}</p>" if sub else ""}<span class="go">{esc(go)} <span aria-hidden="true">→</span></span></div></a></li>')


def published(site, guides):
    """The guides on the site now: name -> (meta from its steps.json, whether it has a card picture)."""
    out = {}
    for name in guides:
        steps = site / name / 'steps.json'
        if steps.is_file():
            out[name] = (json.load(open(steps))['meta'], (site / name / 'card.webp').is_file())
    return out


def build(site=SITE, write_yaml=None):
    """write_yaml: also write render.yaml's framing rules (by default only when this is the real site, not a practice one)."""
    spec = validate(json.load(open(ROOT / 'guides.json')))
    kits, guides = spec['kits'], spec['guides']
    live = published(site, guides)
    (site / 'assets').mkdir(parents=True, exist_ok=True)
    (site / 'assets' / 'site.css').write_text(CSS)
    (site / 'assets' / 'frame-guard.js').write_text(frame_guard_js(spec))
    for f in SOURCE_ASSETS.iterdir():
        if f.is_file() and not f.name.startswith('.'):
            shutil.copy2(f, site / 'assets' / f.name)
    kit_cards, written = [], set()
    for slug, kit in kits.items():
        names = [n for n, g in guides.items() if g['kit'] == slug and n in live]
        if not names:
            continue
        cards = []
        for n in names:
            meta, has_pic = live[n]
            cards.append(card(f'/{n}/', f'/{n}/card.webp' if has_pic else None, guides[n].get('label') or meta.get('part') or n,
                              meta.get('title'), 'Open the 3D guide'))
        title = f'{kit["name"]} ({kit["code"]})' if kit.get('code') else kit['name']
        body = (f'<p class="crumbs"><a href="/">Build Guides</a> <span aria-hidden="true">›</span> {esc(kit["name"])}</p>\n'
                f'<h1>{esc(title)}</h1>\n<p class="lead">Choose a guide to open it.</p>\n<ul class="grid">\n' + '\n'.join(cards) + '\n</ul>')
        (site / 'kits' / slug).mkdir(parents=True, exist_ok=True)
        (site / 'kits' / slug / 'index.html').write_text(page(f'{title} – TechBox Build Guides', body))
        written.add(slug)
        cover = next((n for n in names if live[n][1]), None)                  # (the kit's card shows its first guide with a picture: the Full Build)
        count = f'{len(names)} guide{"s" if len(names) > 1 else ""}'
        kit_cards.append(card(f'/kits/{slug}/', f'/{cover}/card.webp' if cover else None, kit['name'], kit.get('code') and f'{kit["code"]} · {count}' or count,
                              'See the guides'))
    body = ('<h1>Build Guides</h1>\n<p class="lead">Step-by-step 3D build instructions for TechBox kits.</p>\n'
            + (f'<ul class="grid">\n' + '\n'.join(kit_cards) + '\n</ul>' if kit_cards else '<p class="empty">No guides are published yet.</p>'))
    (site / 'index.html').write_text(page('TechBox Build Guides', body))
    (site / '404.html').write_text(page('Not found – TechBox Build Guides', '<h1>This page isn’t here</h1>\n'
                                       '<p class="lead">The guide may have moved. <a href="/">See all the build guides</a>, or open it again from your course.</p>'))
    for old in (site / 'kits').glob('*') if (site / 'kits').exists() else []:   # (a kit with no guide left on the site has no page)
        if old.is_dir() and not old.is_symlink() and old.name not in written and (site / 'kits').resolve() in old.resolve().parents:
            shutil.rmtree(old)
    if write_yaml if write_yaml is not None else site.resolve() == SITE.resolve():
        if write_render_yaml(spec):
            print('render.yaml: the guides\' framing rules changed: commit render.yaml (and guides.json) with site/ and releases/')
    return sorted(written)


def framing_rules(spec):
    """render.yaml's per-guide framing rules: only the LMS may frame a guide (CSP overrides the site-wide X-Frame-Options: DENY)."""
    value = 'frame-ancestors ' + ' '.join(spec['embed_origins'])
    lines = []
    for name in spec['guides']:
        for path in (f'/{name}', f'/{name}/*'):
            lines += [f'      - path: {path}', '        name: Content-Security-Policy', f'        value: "{value}"']
    return lines


def write_render_yaml(spec, path=ROOT / 'render.yaml'):
    """Write the framing rules into render.yaml; True if the file changed."""
    if not path.is_file():
        raise SystemExit(f'{path} is missing: the site\'s headers (who may frame what) are in it')
    text = path.read_text().split('\n')
    begins = [k for k, l in enumerate(text) if l.strip() == BEGIN]
    ends = [k for k, l in enumerate(text) if l.strip() == END]
    if len(begins) != 1 or len(ends) != 1 or begins[0] > ends[0]:
        raise SystemExit(f'render.yaml needs one "{BEGIN}" line and, after it, one "{END}" line, to write the guides\' framing rules between')
    new = text[:begins[0] + 1] + framing_rules(spec) + text[ends[0]:]
    if new == text:
        return False
    path.write_text('\n'.join(new))
    return True


if __name__ == '__main__':
    site = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else SITE
    kits = build(site)
    print(f'{site.name}/: landing page, 404 page and kit pages for {", ".join(kits) or "no kit yet"}')
