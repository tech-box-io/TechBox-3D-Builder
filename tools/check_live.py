"""Check the website as learners get it, after a push to live: each published guide is the release in site/, and every page
comes with the headers render.yaml gives it (above all, who may frame it). Render deploys a few minutes after the push, and it
applies render.yaml's headers only when the Blueprint is synced (21 Oct 2026: the Part guides and both deconstructions came
without their framing header, so the LMS could not show them, until Lee synced it), so run this once the deploy is done:

    python3 tools/check_live.py                  # https://models.tech-box.io, now
    python3 tools/check_live.py --wait 15        # every 30 s for up to 15 minutes, until two checks in a row pass (run it
                                                 # right after git push origin main:live; Render's CDN can answer both ways
                                                 # for a moment while a deploy spreads)
    python3 tools/check_live.py --base http://localhost:8797    # the same against serve.py site, which sends render.yaml's headers
                                                 # (Cache-Control apart: serve.py sends no-store, so that it is not compared)
    python3 tools/check_live.py --base http://localhost:8797 --site "share/Website preview/site"   # the Website Preview's copy

For each guide in site/ (or --site): /<guide>/steps.json and /<guide>/ (its index.html) byte for byte as there (the release it
holds; the part pictures are not compared, as Render's CDN recompresses PNGs, losslessly), /<guide> answers (or redirects to
/<guide>/), and its player comes as JavaScript. For a guide in guides.json that is not in site/ (never published, or taken down):
nothing there. The site's own pages (/, /kits/<kit>/ for each kit with a published guide, /404.html, the frame guard every page
loads) as in site/, and a missing page answers 404. On every one of those paths, each header render.yaml names: the value of the
rule that matches it (`/*`, `/<path>` or `/<path>/*`; a header sent twice is compared as both values, as browsers obey both), and
none where no rule matches (a header left in Render's dashboard after it went from render.yaml; never Access-Control-Allow-Origin).
Only the standard library; Python 3.8 or newer.
"""
import hashlib
import http.client
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_site import header_rules  # noqa: E402  (render.yaml read as check_site.py reads it)

AGENT = 'TechBox check_live.py'
MISSING = '/check-live-no-such-page/'
TIMEOUT = 20                                             # (seconds a request may take: a host that hangs costs one of these per check)
NEVER = ('access-control-allow-origin',)                 # (no other site may load the guides' files: check_site.py)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):     # (the first answer's own status and headers, as a browser first gets them)
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def joined(h):
    """Headers with lower-case names; one sent twice gives both values, joined, so that it differs from either alone."""
    return {k: ', '.join(h.get_all(k)) for k in {k.lower() for k in h.keys()}}


def fetch(url):
    """(status, headers, body) of one GET, or (None, {}, the error's text)."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': AGENT, 'Cache-Control': 'no-cache'})
        with OPENER.open(req, timeout=TIMEOUT) as r:
            return r.status, joined(r.headers), r.read()
    except urllib.error.HTTPError as e:                  # (a 404 or a redirect still has headers worth checking)
        return e.code, joined(e.headers), e.read()
    except (urllib.error.URLError, OSError, http.client.HTTPException, ValueError) as e:
        return None, {}, str(getattr(e, 'reason', None) or e).encode()


def matches(pattern, path):
    """Render's header paths: /* every path, /a/* everything under /a/ (and /a/ itself), /a that path only."""
    if pattern == '/*':
        return True
    if pattern.endswith('/*'):
        return path.startswith(pattern[:-1])
    return path == pattern


def expected(rules, path):
    """{header name: value} that render.yaml gives the path (a name with two matching rules is check_site.py's error)."""
    return {n.lower(): v for p, n, v in rules if matches(p, path)}


def live_base():
    m = re.search(r'^\s*domains:\s*\[\s*([^\],\s]+)', (ROOT / 'render.yaml').read_text(), re.M)
    return 'https://' + (m.group(1).strip('"\'') if m else 'models.tech-box.io')


def check(base, site):
    rules = header_rules((ROOT / 'render.yaml').read_text())
    named = {n.lower() for _, n, _ in rules} | set(NEVER)
    if re.match(r'https?://(localhost|127\.0\.0\.1|\[::1\])(:|/|$)', base):
        named.discard('cache-control')                   # (serve.py sends no-store, so that an edit shows on reload)
    spec = json.load(open(ROOT / 'guides.json'))
    published = [g for g in spec['guides'] if (site / g).is_dir()]
    status, _, body = fetch(base + '/')
    if status is None:
        return [f'{base} does not answer ({body.decode(errors="replace")})'], published, 0
    problems, paths = [], 0

    def page(path, local=None, redirect_to=None, want=200):
        """One GET: its status, every header render.yaml names, and (local) its bytes against the file in site/."""
        nonlocal paths
        paths += 1
        status, got, body = fetch(base + path)
        if status is None:
            problems.append(f'{path}: no answer ({body.decode(errors="replace")})')
            return None
        if redirect_to and status in (301, 302, 307, 308):
            to = urllib.parse.urljoin(base + path, got.get('location', ''))
            if to != base + redirect_to:
                problems.append(f'{path}: redirects to {to!r}, not to {redirect_to}')
        elif status != want:
            problems.append(f'{path}: answered {status}, not {want}')
        rule = expected(rules, path)
        for name in sorted(named):
            if name in rule and got.get(name) != rule[name]:
                problems.append(f'{path}: {name} is {got.get(name)!r}, render.yaml says {rule[name]!r}'
                                + (' (is the Blueprint synced in Render?)' if name == 'content-security-policy' else ''))
            elif name not in rule and name in got:
                problems.append(f'{path}: {name}: {got[name]!r}, which render.yaml does not give this path '
                                '(delete it in Render\'s dashboard, Settings > Headers)')
        if status != want:
            return None
        if local is not None and hashlib.sha256(body).digest() != hashlib.sha256(local.read_bytes()).digest():
            problems.append(f'{path}: not the file in {site.name}/{local.relative_to(site)} (not deployed yet, or a different release)')
        return got

    for g in published:
        page(f'/{g}', redirect_to=f'/{g}/')
        page(f'/{g}/', site / g / 'index.html')
        page(f'/{g}/steps.json', site / g / 'steps.json')
        got = page(f'/{g}/js/player.js')
        if got is not None and 'javascript' not in got.get('content-type', ''):
            problems.append(f'/{g}/js/player.js: content-type {got.get("content-type")!r}, not JavaScript (browsers would refuse it)')
    for g in spec['guides']:
        if g not in published:
            status, _, body = fetch(base + f'/{g}/steps.json')
            if status != 404:
                problems.append(f'/{g}/: ' + ('online, but not in site/ (taken down or never published: deploy again)' if status == 200
                                               else f'could not tell whether it is online (answered {status or body.decode(errors="replace")})'))
    kits = sorted({spec['guides'][g]['kit'] for g in published})
    for path, local in [('/', site / 'index.html'), ('/404.html', site / '404.html'),
                        ('/assets/frame-guard.js', site / 'assets' / 'frame-guard.js')] + \
                       [(f'/kits/{k}/', site / 'kits' / k / 'index.html') for k in kits]:
        page(path, local)
    page(MISSING, want=404)
    return problems, published, paths


def main(argv):
    base, wait, site = live_base(), 0.0, ROOT / 'site'
    args = list(argv)
    while args:
        a = args.pop(0)
        if a in ('--base', '--wait', '--site') and args:
            v = args.pop(0)
            if a == '--base':
                base = v.rstrip('/')
            elif a == '--site':
                site = Path(v) if Path(v).is_absolute() else ROOT / v
            else:
                try:
                    wait = float(v)
                except ValueError:
                    raise SystemExit(__doc__)
        else:
            raise SystemExit(__doc__)
    if not re.match(r'https?://', base):
        raise SystemExit(f'--base needs http:// or https:// (e.g. http://localhost:8797), not {base!r}')
    if not (site / 'index.html').is_file():
        raise SystemExit(f'{site} is not a site folder (no index.html)')
    deadline, passes = time.time() + wait * 60, 0
    while True:
        problems, published, paths = check(base, site)
        stamp = time.strftime('%H:%M:%S')
        if not problems:
            passes += 1
            if not wait or passes == 2:
                print(f'{stamp} {base}: OK: {len(published)} guide(s) as released in {site.name}/ ({", ".join(published)}), '
                      f'headers as render.yaml says on {paths} paths')
                return 0
            print(f'{stamp} passed once; checking again in 30 s')
        else:
            passes = 0
            if not wait or time.time() + 30 > deadline:
                for p in problems:
                    print('PROBLEM: ' + p)
                print(f'{stamp} {base}: {len(problems)} problem(s)')
                return 1
            print(f'{stamp} {len(problems)} problem(s), e.g. {problems[0]}; checking again in 30 s')
        time.sleep(30)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
