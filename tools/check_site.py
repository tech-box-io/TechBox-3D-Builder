"""Check site/ (what the website serves) before it goes out: Render runs this as its build command, so a failed check stops the
deploy and the previous one stays live. Run it yourself too before committing a publish:

    python3 tools/check_site.py            (or: python3 tools/check_site.py <a site folder>, e.g. a practice publish's)

Each guide in site/ must be exactly the release it says it is (steps.json meta.release): the same files, byte for byte, as
that release's record (releases/<guide>/r<N>/release.json, made by tools/publish.py). Nothing else may be in site/ but the
site's own pages (index.html, 404.html, robots.txt, kits/<kit>/index.html, assets/: made by tools/site_pages.py) and the guides
named in guides.json: no hidden files, no links, no CAD, no Review notes, no authoring tools. Every link and picture on the
site's own pages must lead to something on the site, and render.yaml must let only guides.json's embed_origins frame the guides.
Only the standard library; Python 3.8 or newer.
"""
import hashlib
import json
import os
import re
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_pages  # noqa: E402  (guides.json's own check, and the frame guard it writes)

SITE = ROOT / 'site'
TOP_FILES = ('index.html', '404.html', 'robots.txt')
TOP_DIRS = ('assets', 'kits')
ASSETS = ('site.css', 'techbox-wordmark-white.svg', 'frame-guard.js')
IGNORED = ('.DS_Store',)                     # (Finder's; never committed, so never deployed)
MODEL_GENERATOR = 'TechBox build_model.py'
MODEL_LIMIT = 15_000_000
IMPORT = re.compile(r"""(?:\bfrom\s*|\bimport\s*\(\s*|\bimport\s+)(['"])([^'"]+)\1""")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def walk(folder):
    """Every file under folder (relative paths), and the problems: links, hidden names."""
    files, problems = [], []
    for here, dirs, names in os.walk(folder, followlinks=False):
        for d in list(dirs):
            p = Path(here) / d
            if p.is_symlink():
                problems.append(f'{p.relative_to(folder)}/: a link')
                dirs.remove(d)
            elif d.startswith('.'):
                problems.append(f'{p.relative_to(folder)}/: a hidden folder')
                dirs.remove(d)
        for n in names:
            p = Path(here) / n
            if n in IGNORED:
                continue
            if p.is_symlink():
                problems.append(f'{p.relative_to(folder)}: a link')
            elif n.startswith('.'):
                problems.append(f'{p.relative_to(folder)}: a hidden file')
            else:
                files.append(p.relative_to(folder).as_posix())
    return sorted(files), problems


GUIDE_TYPES = ('.html', '.js', '.glb', '.png', '.webp', '.jpg', '.svg')   # (and steps.json, vendor/three/LICENSE)


def steps_stamp(steps):
    """A guide's content, in brief (its meta and the model's version left out): a deconstruction guide records the stamp of the
    Full Build it was taken apart from (stepgen take_apart(): meta.taken_from), and publish.py warns once the Full Build has
    changed since."""
    body = {k: v for k, v in steps.items() if k not in ('meta', 'model')}
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode('utf-8')).hexdigest()[:12]


def guide_parts(steps):
    """The parts (CAD instance ids) a guide shows in any of its views, or carries with one it shows: what its model must hold.
    (publish.py leaves every other part out of a guide's published model, so that a Part guide downloads only its own parts.)"""
    ids = set()
    for view in steps.get('views', []):
        ids.update(view.get('visible', []))
        ids.update(view.get('leaving', []))
        for i, c in (view.get('carry') or {}).items():
            ids.update((i, c.get('by')))
        ids.update(view.get('moving', []))
        ids.update(view.get('still', []))
        ids.update((view.get('paths') or {}).keys())
        ids.update((view.get('inset') or {}).get('hide', []))
        ids.update(item['id'] for item in view.get('labels', []) + view.get('eye', []) if item.get('id'))
    ids.discard(None)
    return ids


def check_model(path, steps=None):
    raw = Path(path).read_bytes()
    if raw[:4] != b'glTF' or len(raw) < 20:
        return ['not a binary glTF file']
    n, _ = struct.unpack('<II', raw[12:20])
    doc = json.loads(raw[20:20 + n])
    out = []
    if doc.get('asset', {}).get('generator') != MODEL_GENERATOR:
        out.append(f'not a guide model made by {MODEL_GENERATOR}')
    if 'EXT_meshopt_compression' not in doc.get('extensionsUsed', []):
        out.append('not meshopt-compressed')
    if len(raw) > MODEL_LIMIT:
        out.append(f'{len(raw) / 1e6:.1f} MB, too big for a guide model')
    rest = raw[20 + n:]                          # (the binary chunk: publish.py packs it again when it leaves parts out)
    blen = struct.unpack('<II', rest[:8])[0] if len(rest) >= 8 else -1
    if blen != len(rest) - 8 or (doc.get('buffers') and doc['buffers'][0].get('byteLength') != blen):
        out.append('its binary chunk is not the length the model says')
    elif any(not (0 <= e.get('byteOffset', 0) and e.get('byteOffset', 0) + e.get('byteLength', 0) <= blen)
             for e in ((v.get('extensions') or {}).get('EXT_meshopt_compression') for v in doc.get('bufferViews', [])) if e):
        out.append('a compressed buffer view lies outside its binary chunk')
    if any('name' in m for m in doc.get('meshes', [])) and not doc.get('asset', {}).get('copyright'):
        out.append('still carries the CAD\'s names (not a published copy)')
    # (publish.py names only the assembly, "model", and the parts under it, and keeps a mesh's name only where the guide names a
    # part inside a part by it: any other name is the CAD's own, a body or file name)
    nodes, scenes = doc.get('nodes', []), doc.get('scenes', [])
    roots = scenes[doc.get('scene', 0)].get('nodes', []) if scenes else []
    if len(roots) == 1 and nodes[roots[0]].get('name') == 'model':
        parts = set(nodes[roots[0]].get('children', []))
        stray = [n['name'] for k, n in enumerate(nodes) if 'name' in n and k != roots[0] and k not in parts]
        if stray:
            out.append(f'{len(stray)} node(s) keep a CAD name (e.g. {stray[0]!r}): not a published copy')
        if steps is not None:                    # (a part the guide shows but its model lacks would silently not be there)
            missing = sorted(guide_parts(steps) - {nodes[k].get('name') for k in parts})
            if missing:
                out.append(f'{len(missing)} part(s) the guide shows are not in its model (e.g. {missing[0]!r})')
    else:
        out.append('its assembly is not named "model": not a published copy')
    prefixes = tuple(((steps or {}).get('mesh_names') or {}).keys())
    named = [m['name'] for m in doc.get('meshes', []) if 'name' in m and not (prefixes and m['name'].startswith(prefixes))]
    if named:
        out.append(f'{len(named)} mesh(es) keep a CAD name (e.g. {named[0]!r}): not a published copy')
    return out


def check_imports(folder, files):
    """Every module the player loads is in the folder (a new player module left out of a release would break it)."""
    out = []
    page = (folder / 'index.html').read_text()
    m = re.search(r'<script type="importmap">(.*?)</script>', page, re.S)
    imports = json.loads(m.group(1))['imports'] if m else {}
    for src, text in [('index.html', page)] + [(f, (folder / f).read_text()) for f in files if f.endswith('.js')]:
        for _, spec in IMPORT.findall(text):
            spec = spec.split('?')[0]
            if spec in imports:
                target = imports[spec]
            elif any(spec.startswith(k) for k in imports if k.endswith('/')):
                k = next(k for k in imports if k.endswith('/') and spec.startswith(k))
                target = imports[k] + spec[len(k):]
            elif spec.startswith('.'):
                target = os.path.normpath(os.path.join(os.path.dirname(src), spec))
            else:
                continue
            target = os.path.normpath(target[2:] if target.startswith('./') else target)
            if target not in files:
                out.append(f'{src} loads {spec}, which is not in the folder')
    return out


def check_guide(name, folder, releases):
    errors = []
    files, problems = walk(folder)
    errors += problems
    try:
        steps = json.load(open(folder / 'steps.json'))
    except (OSError, ValueError) as e:
        return errors + [f'steps.json does not read: {e}']
    meta = steps.get('meta', {})
    release = meta.get('release')
    if meta.get('guide') != name:
        errors.append(f'steps.json says it is "{meta.get("guide")}", not {name}')
    record_path = releases / name / str(release) / 'release.json'
    if not release or not record_path.is_file():
        return errors + [f'no release record for {release} ({record_path.relative_to(releases.parent)}): only tools/publish.py may write site/']
    record = json.load(open(record_path))
    expected = set(record['files'])
    for f in sorted(expected - set(files)):
        errors.append(f'{f} is missing (the release has it)')
    for f in sorted(set(files) - expected):
        errors.append(f'{f} is not part of {release}')
    for f in sorted(expected & set(files)):
        if sha256(folder / f) != record['files'][f]:
            errors.append(f'{f} differs from {release} as published')
    if meta.get('review_notes') is not False:
        errors.append('steps.json: meta.review_notes should be false (not a published copy)')
    for k, view in enumerate(steps.get('views', [])):
        bad = [key for key in ('review', 'text_key') if key in view]
        if bad:
            errors.append(f'steps.json view {k} ({view.get("name")}) still has {", ".join(bad)}')
            break
    named = [steps.get('model', '').split('?')[0], meta.get('logo')] + [item.get('picture') for v in steps.get('views', []) for g in v.get('parts', []) for item in g.get('items', [])]
    for f in sorted({n for n in named if n}):
        if Path(f).is_absolute() or '..' in Path(f).parts or f not in files:      # (exact names: a case slip passes on a Mac, not on Render)
            errors.append(f'steps.json names {f}, which is not in the folder')
    model = steps.get('model', '').split('?')[0]
    if model in files:
        errors += [f'{model}: {p}' for p in check_model(folder / model, steps)]
    for f in files:                                  # (only what a learner's browser needs: never a source, a note or a CAD file)
        if not (f == 'steps.json' or f == 'vendor/three/LICENSE' or Path(f).suffix.lower() in GUIDE_TYPES):
            errors.append(f'{f}: not a kind of file a guide holds (only {", ".join(GUIDE_TYPES)}, steps.json and the three.js licence)')
    if 'index.html' in files:
        page = (folder / 'index.html').read_text()
        if "import('./js/player.js?v=' + Date.now())" in page:
            errors.append('index.html is the authoring copy of the player, not a published one')
        if '<script src="/assets/frame-guard.js"></script>' not in page:
            errors.append('index.html does not load the site\'s frame guard')
        errors += check_imports(folder, files)
    return errors


def check_pages(site, spec):
    """The site's own pages: only the expected files, and every link and picture on them leads to something on the site."""
    errors = []
    assets = site / 'assets'
    if assets.is_dir():
        files, problems = walk(assets)
        errors += [f'assets/{p}' for p in problems] + [f'assets/{f}: not one of the site\'s own files' for f in files if f not in ASSETS]
    errors += [f'assets/{a} is missing' for a in ASSETS if not (assets / a).is_file()]
    guard = assets / 'frame-guard.js'
    if guard.is_file() and guard.read_text() != site_pages.frame_guard_js(spec):
        errors.append('assets/frame-guard.js does not match guides.json embed_origins (run python3 tools/site_pages.py)')
    pages = [site / 'index.html', site / '404.html']
    kits = site / 'kits'
    if kits.is_dir():
        for k in sorted(kits.iterdir()):
            if k.name in IGNORED:
                continue
            if k.is_symlink() or not k.is_dir() or k.name not in spec['kits']:
                errors.append(f'kits/{k.name}: not a kit in guides.json')
                continue
            files, problems = walk(k)
            errors += [f'kits/{k.name}/{p}' for p in problems] + [f'kits/{k.name}/{f}: not a kit page' for f in files if f != 'index.html']
            pages.append(k / 'index.html')
    for page in pages:
        if not page.is_file():
            continue
        text = page.read_text()
        for ref in re.findall(r'(?:href|src)="([^"]+)"', text):
            if re.match(r'^(https?:|mailto:|data:|#)', ref):
                continue
            target = (site / ref.lstrip('/')) if ref.startswith('/') else (page.parent / ref)
            target = Path(os.path.normpath(target))
            if not (target.is_file() or (target.is_dir() and (target / 'index.html').is_file())) or site.resolve() not in [target.resolve(), *target.resolve().parents]:
                errors.append(f'{page.relative_to(site)} links to {ref}, which is not on the site')
        if 'window.top !== window.self' not in text:
            errors.append(f'{page.relative_to(site)}: no frame guard (made by tools/site_pages.py?)')
    return errors


def header_rules(text):
    """render.yaml's header rules, as (path, name, value), comments left out."""
    rules, cur = [], {}
    for line in text.split('\n'):
        line = line.split(' #')[0].rstrip() if not line.lstrip().startswith('#') else ''
        m = re.match(r'^\s*-?\s*(path|name|value):\s*(.+)$', line)
        if not m:
            continue
        if m.group(1) == 'path' and cur:
            rules.append(cur)
            cur = {}
        cur[m.group(1)] = m.group(2).strip().strip('"\'')
    if cur:
        rules.append(cur)
    return [(r.get('path'), r.get('name'), r.get('value')) for r in rules if 'path' in r and 'name' in r]


def check_render(spec):
    """render.yaml: no page may be framed (X-Frame-Options: DENY on /*), except each guide, by guides.json's embed_origins only
    (two Content-Security-Policy rules per guide); never a Content-Security-Policy on /*, and no header name both on /* and on a
    narrower path (Render picks one of two same-named matching rules at random); no other site may load the files
    (Cross-Origin-Resource-Policy: same-site; never Access-Control-Allow-Origin)."""
    path = ROOT / 'render.yaml'
    if not path.is_file():
        return ['render.yaml is missing: it holds the site\'s headers (who may frame what)']
    rules = header_rules(path.read_text())
    errors = []
    xfo = [(p, v) for p, n, v in rules if n.lower() == 'x-frame-options']
    if xfo != [('/*', 'DENY')]:
        errors.append(f'render.yaml: X-Frame-Options must be one rule, "/*: DENY" (found {xfo or "none"})')
    if ('/*', 'Cross-Origin-Resource-Policy', 'same-site') not in rules:
        errors.append('render.yaml: no "Cross-Origin-Resource-Policy: same-site" on /*')
    if any(n.lower() == 'access-control-allow-origin' for _, n, _ in rules):
        errors.append('render.yaml: Access-Control-Allow-Origin would let any site load the guides\' files')
    csp = [(p, v) for p, n, v in rules if n.lower() == 'content-security-policy']
    if any(p == '/*' for p, _ in csp):
        errors.append('render.yaml: a Content-Security-Policy on /* (it would collide with the guides\' own)')
    value = 'frame-ancestors ' + ' '.join(spec.get('embed_origins', []))
    want = {(f'/{g}', value) for g in spec['guides']} | {(f'/{g}/*', value) for g in spec['guides']}
    for p, v in sorted(want - set(csp)):
        errors.append(f'render.yaml: no rule "{p}: {v}" (run python3 tools/site_pages.py)')
    for p, v in sorted(set(csp) - want):
        errors.append(f'render.yaml: unexpected Content-Security-Policy rule "{p}: {v}"')
    on_all = {n.lower() for p, n, _ in rules if p == '/*'}
    seen = set()
    for p, n, _ in rules:
        if (p, n.lower()) in seen:
            errors.append(f'render.yaml: two {n} rules on {p}')
        seen.add((p, n.lower()))
        if p != '/*' and n.lower() in on_all:
            errors.append(f'render.yaml: {n} on {p} and on /* (Render would pick one at random)')
    return errors


def uncommitted():
    """On this computer (not on Render): what the deploy needs that is not committed yet."""
    try:
        out = subprocess.run(['git', 'status', '--porcelain', '--', 'site', 'releases', 'render.yaml', 'guides.json'], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.rstrip()
    except (OSError, subprocess.CalledProcessError):
        return []
    return [l for l in out.split('\n') if l.strip()]


def check_git_case(site, name, files):
    """What git will deploy must have the same names, letter case included (macOS ignores case; Render does not)."""
    try:
        tracked = subprocess.run(['git', 'ls-files', '--', str(site / name)], cwd=site, capture_output=True, text=True, check=True).stdout.split('\n')
    except (OSError, subprocess.CalledProcessError):
        return []
    prefix = (site / name).resolve()
    names = set(files)
    lower = {f.lower(): f for f in files}
    out = []
    for t in filter(None, tracked):
        rel = (Path(site).resolve().parent / t).resolve()
        try:
            rel = rel.relative_to(prefix).as_posix()
        except ValueError:
            continue
        if rel not in names and rel.lower() in lower:
            out.append(f'git tracks {rel} but the file is {lower[rel.lower()]}: run git mv -f "{t}" with the new name')
    return out


def check(site=SITE):
    errors, total = [], 0
    if not site.is_dir():
        return [f'{site} is missing'], 0
    releases = site.parent / 'releases'
    try:
        spec = site_pages.validate(json.load(open(ROOT / 'guides.json')))
    except SystemExit as e:
        return [str(e)], 0
    guides = spec['guides']
    for f in TOP_FILES:
        if not (site / f).is_file():
            errors.append(f'site/{f} is missing')
    for p in sorted(site.iterdir()):
        if p.name in IGNORED:
            continue
        if p.is_symlink():
            errors.append(f'site/{p.name}: a link')
        elif p.name.startswith('.'):
            errors.append(f'site/{p.name}: hidden files and unfinished copies must not be published')
        elif p.is_file() and p.name not in TOP_FILES:
            errors.append(f'site/{p.name}: not a file the site needs at its top level')
        elif p.is_dir() and p.name not in guides and p.name not in TOP_DIRS:
            errors.append(f'site/{p.name}/: not a guide in guides.json')
    for name in guides:
        folder = site / name
        if not folder.is_dir() or folder.is_symlink():
            continue                                                     # (not published, or taken down; a link is reported above)
        try:
            found = check_guide(name, folder, releases)
            files, _ = walk(folder)
            found += check_git_case(site, name, files)
            total += sum((folder / f).stat().st_size for f in files)
        except Exception as e:                                           # (a damaged file is a failed check, with its reason)
            found = [f'could not be checked: {type(e).__name__}: {e}']
        errors += [f'{name}: {e}' for e in found]
    try:
        errors += check_pages(site, spec) + check_render(spec)
    except Exception as e:
        errors.append(f'the site\'s own pages could not be checked: {type(e).__name__}: {e}')
    return errors, total


if __name__ == '__main__':
    site = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else SITE
    errors, total = check(site)
    for e in errors:
        print('ERROR: ' + e)
    if site == SITE and not os.environ.get('RENDER'):                 # (Render sets RENDER; there the checkout is what deploys)
        pending = uncommitted()
        if pending:
            print(f'NOTE: not committed yet ({len(pending)}): {", ".join(l[3:] for l in pending[:6])}{" ..." if len(pending) > 6 else ""}'
                  ' (commit them before pushing to live)')
    published = sorted(p.name for p in site.iterdir() if p.is_dir() and not p.name.startswith('.') and p.name not in TOP_DIRS) if site.is_dir() else []
    print(f'{site.name}/: {len(published)} guide(s) ({", ".join(published) or "none"}), {total / 1e6:.1f} MB; '
          f'{"OK" if not errors else f"{len(errors)} problem(s)"}')
    sys.exit(1 if errors else 0)
