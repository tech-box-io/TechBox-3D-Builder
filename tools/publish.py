"""Publish a guide: freeze what it is now as a release, and make that the version the website serves.

    python3 tools/publish.py <guide> --note "what changed"    a new release of that guide (guides.json names them)
    python3 tools/publish.py <guide> --restore r3             put an earlier release back on the website (a roll-back)
    python3 tools/publish.py <guide> --take-down              take the guide off the website (its releases are kept)
    python3 tools/publish.py --list                           every guide: which release the website has, and the others
    (add --to <folder> for a practice run that writes there instead of releases/ and site/)

How it fits together:
- The kit folder is where a guide is written and checked (guide.py -> steps.json, model.glb, parts/, and cards/<steps>.webp, the
  picture for its card on the website, made in the player with _dev.card()). The player is the one copy in player/.
- A release is a frozen copy of exactly the files a learner's browser needs: the player (player.html becomes index.html), the
  guide's steps (as steps.json, with the Review notes and other authoring data taken out), the kit's model (with the CAD's own
  part, body and file names taken out), the logo and the part pictures its Parts List shows. Nothing else: no CAD, no guide.py,
  no colours file, no research. Releases are kept in releases/<guide>/r<N>/ with a record (release.json: when, why, the
  source's git commit, every file's checksum) and releases/<guide>/history.json. They never change and are never uploaded:
  tools/serve.py releases shows them on this computer only.
- site/<guide>/ is the one copy the website serves (Render publishes site/ only): always the release published or restored last.
  The address never changes, so an LMS embed of https://<domain>/<guide>/ always shows the current version, and earlier versions
  cannot be reached from the web. tools/check_site.py (Render's build command) compares it with its release record. After every
  change the website's own pages (the landing page, a page per kit) are made again from what is on the site (tools/site_pages.py).
- A guide may be shown inside a frame only by the sites in guides.json "embed_origins" (TechBox's LMS): render.yaml's headers say
  so (the real check), and each published index.html loads the site's assets/frame-guard.js (made from embed_origins by
  site_pages.py, so not frozen into the release) as a second guard. The website's own pages may not be framed at all.
- What the model gives away: a 3D guide has to send the part shapes to the browser; anyone with the address can save the model.
  The laser-cut wood is roughened in every model (materials.json "roughen_mm", build_model.py): a deterrent against tracing
  cutting files straight from it, not a guarantee (at 0.1 mm most joints would still fit). Only STEP and editable CAD stay private.
- The order: commit the checked sources, publish, look (python3 tools/serve.py site 8797 -> http://localhost:8797/<guide>/),
  commit site/ and releases/; going live is pushing to the branch Render deploys (render.yaml), only on Lee's word.

Only the standard library; light (it copies files). It locks against a second publish, not against a guide.py run: do not
publish while a guide is being regenerated (a steps file and model from different runs are refused).
"""
import argparse
import datetime
import fcntl
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_pages  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PLAYER = ROOT / 'player'
SITE = ROOT / 'site'
RELEASES = ROOT / 'releases'
NAME = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
RELEASE = re.compile(r'^r[1-9][0-9]*$')
PLAYER_FILES = ['js/core.js', 'js/player.js']                       # (not parts.html, parts.js or runthrough.js: authoring tools)
AUTHORING_KEYS = ('review', 'text_key')                              # per view: Review notes for TechBox; the step-text spreadsheet's key
FRESH_IMPORT = "import('./js/player.js?v=' + Date.now());   // (a fresh copy of the player's code on every load: no browser can keep an old one)"   # player.html's, for authoring
ICON = '<link rel="icon" href="data:,">'
GUARD = '<script src="/assets/frame-guard.js"></script>'            # the site's second guard against framing (tools/site_pages.py)
SLASH_FIX = """<script>
// On the website a guide is the folder /<guide>/ and this page is its index.html: opened without the closing slash, the browser
// would look for the guide's files one folder up, so add the slash before anything loads.
if (!/(\\/|\\.html?)$/i.test(location.pathname)) location.replace(location.pathname + '/' + location.search + location.hash);
</script>"""
TOP_PAGES = ('robots.txt',)                                          # (copied into a practice site; site_pages.py makes the others)
MODEL_GENERATOR = 'TechBox build_model.py'
MODEL_LIMIT = 15_000_000                                             # bytes: a published model is a few MB; the raw CAD is tens


def sha256(data):
    return hashlib.sha256(data if isinstance(data, bytes) else Path(data).read_bytes()).hexdigest()


def write_atomic(path, text):
    path = Path(path)
    tmp = path.with_name(f'.{path.name}.tmp')
    tmp.write_text(text)
    os.replace(tmp, path)


def spec():
    return json.load(open(ROOT / 'guides.json'))


def registry():
    """The guides in guides.json, each with its kit folder ("folder"), checked (site_pages.validate)."""
    s = site_pages.validate(spec())
    for g in s['guides'].values():
        g['folder'] = s['kits'][g['kit']]['folder']
    return s['guides']


def history(name):
    path = RELEASES / name / 'history.json'
    return json.load(open(path)) if path.exists() else {'guide': name, 'log': []}


def save_history(name, h):
    (RELEASES / name).mkdir(parents=True, exist_ok=True)
    write_atomic(RELEASES / name / 'history.json', json.dumps(h, indent=1) + '\n')


def releases_of(name):
    folder = RELEASES / name
    return sorted(int(p.name[1:]) for p in folder.glob('r*') if p.is_dir() and RELEASE.match(p.name)) if folder.exists() else []


def next_number(name):
    used = releases_of(name) + [int(e['release'][1:]) for e in history(name)['log'] if RELEASE.match(e.get('release') or '')]
    return max(used, default=0) + 1


def on_site(name):
    """The release site/<guide>/ holds, read from the site itself (not from the history)."""
    steps = SITE / name / 'steps.json'
    try:
        return json.load(open(steps))['meta'].get('release') if steps.exists() else None
    except (ValueError, KeyError):
        return '?'


def git_source(kit):
    """The commit the sources were at, and whether anything that makes this guide had uncommitted changes (None if unknown)."""
    try:
        run = lambda *a: subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        head = run('rev-parse', 'HEAD')
        dirty = run('status', '--porcelain', '--', str(kit.relative_to(ROOT)), 'player', 'guides.json', 'tools')
        return dict(commit=head, uncommitted_changes=bool(dirty))
    except (OSError, subprocess.CalledProcessError, ValueError):
        return dict(commit=None, uncommitted_changes=None)


def inside(kit, rel):
    """A file named in steps.json, as a path inside the kit folder (never outside it)."""
    p = Path(rel or '')
    if not rel or p.is_absolute() or '..' in p.parts:
        raise SystemExit(f'steps.json names "{rel}": not a plain path inside the kit folder')
    return kit / p


def read_glb(path):
    raw = Path(path).read_bytes()
    if raw[:4] != b'glTF' or len(raw) < 20:
        raise SystemExit(f'{path}: not a binary glTF file')
    n, kind = struct.unpack('<II', raw[12:20])
    if kind != 0x4E4F534A:
        raise SystemExit(f'{path}: its first chunk is not JSON')
    return raw, json.loads(raw[20:20 + n]), raw[20 + n:]


def model_problems(path):
    """Why a file is not a published guide model (a raw CAD export is tens of MB and was not made by build_model.py)."""
    _, doc, _ = read_glb(path)
    out = []
    if doc.get('asset', {}).get('generator') != MODEL_GENERATOR:
        out.append(f'not made by {MODEL_GENERATOR} (generator: {doc.get("asset", {}).get("generator")})')
    if 'EXT_meshopt_compression' not in doc.get('extensionsUsed', []):
        out.append('not meshopt-compressed')
    if Path(path).stat().st_size > MODEL_LIMIT:
        out.append(f'{Path(path).stat().st_size / 1e6:.1f} MB, over the {MODEL_LIMIT / 1e6:.0f} MB a guide model may be')
    return out


def rough_problems(kit, model):
    """Why a kit's model would give away the exact shapes of its laser-cut parts: every mesh in the colour of a materials.json
    rule with "roughen_mm" must have been roughened (model.report.json, written by build_model.py with the model); a kit with no
    such rule must say that it has no laser-cut parts ("no_laser_cut_parts": true), so that a new kit cannot go out unroughened
    by being left out."""
    spec = json.load(open(kit / 'materials.json'))
    woods = {r['color'] for r in spec.get('rules', []) if r.get('roughen_mm') and r.get('color')}
    if not woods:
        return [] if spec.get('no_laser_cut_parts') is True else [
            'materials.json has no rule with "roughen_mm": the laser-cut parts would go out with their exact shapes; add it to the '
            'wood rule (as the MRA and RCC have), or set "no_laser_cut_parts": true if the kit has none']
    report = kit / 'model.report.json'
    if not report.is_file() or report.stat().st_mtime < model.stat().st_mtime - 60:
        return ['model.report.json is missing or older than the model: run tools/build_model.py on the kit']
    rows = json.load(open(report)).get('meshes', [])
    bare = [m['mesh'] for m in rows if woods & set(m.get('colours', [])) and 'edges roughened' not in m.get('note', '')]
    return [f'{len(bare)} laser-cut mesh(es) in {", ".join(sorted(woods))} not roughened: {", ".join(bare[:5])}{" ..." if len(bare) > 5 else ""}'] if bare else []


def published_model(src, dst, steps):
    """The model with the CAD's own names taken out: the player finds parts by the names of the assembly's direct children (the
    ids in steps.json) and keeps those, and the assembly's own name becomes "model"; every other node name goes, and the mesh
    (body / file) names unless the guide names parts inside a part by them (steps.json mesh_names). Geometry is untouched."""
    _, doc, rest = read_glb(src)
    nodes = doc['nodes']
    roots = doc['scenes'][doc.get('scene', 0)]['nodes']
    assembly = roots[0] if len(roots) == 1 and 'mesh' not in nodes[roots[0]] else None
    keep = set(nodes[assembly].get('children', [])) if assembly is not None else set(roots)
    for k, node in enumerate(nodes):
        if k == assembly:
            node['name'] = 'model'
        elif k not in keep:
            node.pop('name', None)
    prefixes = tuple((steps.get('mesh_names') or {}).keys())
    for mesh in doc.get('meshes', []):
        if not (prefixes and mesh.get('name', '').startswith(prefixes)):
            mesh.pop('name', None)
    doc['asset']['copyright'] = steps['meta'].get('copyright') or 'TechBox'
    text = json.dumps(doc, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    text += b' ' * (-len(text) % 4)
    body = struct.pack('<II', len(text), 0x4E4F534A) + text + rest
    Path(dst).write_bytes(struct.pack('<III', 0x46546C67, 2, 12 + len(body)) + body)


def published_steps(steps, name, release, model_v):
    """The learner's copy of the steps: no Review notes, no authoring keys; the model named by its content, so a new model is
    fetched afresh and an unchanged one is not."""
    out = dict(steps)
    out['meta'] = {k: v for k, v in steps['meta'].items() if k != 'review_notes'}
    out['meta'].update(review_notes=False, guide=name, release=release)
    out['model'] = steps['model'].split('?')[0] + f'?v={model_v}'
    out['views'] = [{k: v for k, v in view.items() if k not in AUTHORING_KEYS} for view in steps['views']]
    return out


def needed_files(steps):
    """The guide's own files, relative to the kit folder: the model, the logo, and each picture its Parts List shows."""
    files = [steps['model'].split('?')[0]]
    if steps['meta'].get('logo'):
        files.append(steps['meta']['logo'])
    for view in steps['views']:
        for group in view.get('parts', []):
            for item in group['items']:
                if item.get('picture') and item['picture'] not in files:
                    files.append(item['picture'])
    return files


def verify_release(folder):
    """Errors if a release folder is not exactly what its record says."""
    record = json.load(open(folder / 'release.json'))
    have = {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file() and p.name not in ('release.json', '.DS_Store')}
    errors = [f'missing: {f}' for f in sorted(set(record['files']) - have)] + [f'not in the record: {f}' for f in sorted(have - set(record['files']))]
    errors += [f'changed since release: {f}' for f in sorted(have & set(record['files'])) if sha256(folder / f) != record['files'][f]]
    return errors


def build_release(name, entry, note):
    kit = ROOT / entry['folder']
    steps_file = inside(kit, entry['steps'])
    steps = json.load(open(steps_file))
    files = needed_files(steps)
    missing = [f for f in files if not inside(kit, f).exists()]
    if missing:
        raise SystemExit(f'{name}: missing in {kit.name}: {", ".join(missing)} (part pictures: open parts.html through tools/serve.py)')
    model = inside(kit, files[0])
    problems = model_problems(model)
    if problems:
        raise SystemExit(f'{name}: {files[0]} is not a guide model: {"; ".join(problems)}')
    problems = rough_problems(kit, model)
    if problems:
        raise SystemExit(f'{name}: not published: {"; ".join(problems)}')
    stamp = steps['model'].partition('?v=')[2]
    if stamp.isdigit() and int(stamp) != int(model.stat().st_mtime):
        raise SystemExit(f'{name}: {entry["steps"]} and {files[0]} are from different runs (the model changed after the steps were written): '
                         'run the kit\'s guide script again, then publish')
    warnings = []
    stale = [f for f in files[1:] if f.startswith('parts/') and inside(kit, f).stat().st_mtime < model.stat().st_mtime]
    if stale:
        warnings.append(f'{len(stale)} part picture(s) are older than the model; re-render them with parts.html if the model changed: {", ".join(stale[:4])}{" ..." if len(stale) > 4 else ""}')
    script = kit / entry.get('script', 'guide.py')
    if script.exists() and steps_file.stat().st_mtime < script.stat().st_mtime:
        warnings.append(f'{entry["steps"]} is older than {script.name}: has it been run since its last edit?')
    card = kit / 'cards' / (Path(entry['steps']).stem + '.webp')
    if not card.is_file():
        warnings.append(f'no card picture ({card.relative_to(ROOT)}): the website shows "No picture yet"; make one in the player with _dev.card()')
    elif card.stat().st_mtime < model.stat().st_mtime:
        warnings.append(f'the card picture is older than the model: make it again with _dev.card() if the model changed')
    reviews = sum(1 for v in steps['views'] if v.get('review'))
    if reviews:
        warnings.append(f'{reviews} view(s) carry Review notes; they are left out of the published copy (still in the kit)')
    page = (PLAYER / 'player.html').read_text()
    if page.count(FRESH_IMPORT) != 1 or page.count(ICON) != 1:
        raise SystemExit('publish.py: player.html has changed shape (its player.js import or its icon line); update FRESH_IMPORT / ICON')

    release = f'r{next_number(name)}'
    final, tmp = RELEASES / name / release, RELEASES / name / f'.{release}.tmp'
    if final.exists():
        raise SystemExit(f'{final} exists already: a release is never overwritten')
    tmp.mkdir(parents=True)
    player_v = sha256(b''.join((PLAYER / f).read_bytes() for f in PLAYER_FILES))[:12]
    (tmp / 'index.html').write_text(page.replace(FRESH_IMPORT, f"if (!window.techboxFrameRefused) import('./js/player.js?v={player_v}');   // (the player's code, named by its content)")
                                    .replace(ICON, ICON + '\n' + SLASH_FIX + '\n' + GUARD))
    for f in PLAYER_FILES:
        (tmp / f).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PLAYER / f, tmp / f)
    shutil.copytree(PLAYER / 'vendor', tmp / 'vendor', ignore=shutil.ignore_patterns('.*'))
    for f in files[1:]:
        (tmp / f).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(inside(kit, f), tmp / f)
    if card.is_file():
        shutil.copy2(card, tmp / 'card.webp')
    (tmp / files[0]).parent.mkdir(parents=True, exist_ok=True)
    published_model(model, tmp / files[0], steps)
    model_v = sha256(tmp / files[0])[:12]
    out = published_steps(steps, name, release, model_v)
    (tmp / 'steps.json').write_text(json.dumps(out, separators=(',', ':'), ensure_ascii=False))
    content = dict(out, meta={k: v for k, v in out['meta'].items() if k != 'release'})
    record = dict(guide=name, release=release, published=datetime.datetime.now().isoformat(timespec='seconds'), note=note,
                  kit=entry['folder'], steps=entry['steps'], title=steps['meta'].get('title'), part=steps['meta'].get('part'),
                  views=len(steps['views']), source=git_source(kit),
                  steps_content=sha256(json.dumps(content, sort_keys=True).encode('utf-8')),
                  files={p.relative_to(tmp).as_posix(): sha256(p) for p in sorted(tmp.rglob('*')) if p.is_file()})
    (tmp / 'release.json').write_text(json.dumps(record, indent=1) + '\n')
    tmp.rename(final)
    return final, record, warnings


def put_on_site(name, release_dir):
    """Make site/<guide>/ an exact copy of a release (less its record), replacing what was there."""
    errors = verify_release(release_dir)
    if errors:
        raise SystemExit(f'{release_dir} does not match its record, so it is not put on the site: {"; ".join(errors[:5])}')
    SITE.mkdir(parents=True, exist_ok=True)
    target, tmp, old = SITE / name, SITE / f'.{name}.tmp', SITE / f'.{name}.old'
    shutil.copytree(release_dir, tmp, ignore=shutil.ignore_patterns('release.json', '.*'))
    if target.exists():
        target.rename(old)
    tmp.rename(target)
    shutil.rmtree(old, ignore_errors=True)


def changes(name, new_dir, before):
    """What differs from the release that was on the website before (or, if none is, the newest earlier release)."""
    earlier = [n for n in releases_of(name) if f'r{n}' != new_dir.name]
    if not before or before == '?' or not (RELEASES / name / before / 'release.json').exists():
        before = f'r{earlier[-1]}' if earlier else None
    if not before or before == new_dir.name:
        return ['(the first release of this guide)']
    old = json.load(open(RELEASES / name / before / 'release.json'))
    new = json.load(open(new_dir / 'release.json'))
    out = [f'changed: {f}' for f in sorted(new['files']) if f in old['files'] and old['files'][f] != new['files'][f] and f != 'steps.json']
    if old.get('steps_content') != new.get('steps_content'):
        out.insert(0, 'changed: steps.json (the steps themselves)')
    out += [f'added: {f}' for f in sorted(set(new['files']) - set(old['files']))]
    out += [f'removed: {f}' for f in sorted(set(old['files']) - set(new['files']))]
    return [f'compared with {before}:'] + (out or ['no file differs'])


def tidy(name):
    """Remove what an interrupted publish left behind."""
    for p in list((RELEASES / name).glob('.r*.tmp')) + [SITE / f'.{name}.tmp', SITE / f'.{name}.old']:
        shutil.rmtree(p, ignore_errors=True)


def main():
    global SITE, RELEASES
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('guide', nargs='?')
    what = ap.add_mutually_exclusive_group()
    what.add_argument('--restore', metavar='rN', help='put an earlier release back on the website')
    what.add_argument('--take-down', action='store_true', help='take the guide off the website')
    what.add_argument('--list', action='store_true')
    ap.add_argument('--note', help='what changed, or why (kept in the record)')
    ap.add_argument('--to', metavar='FOLDER', help='a practice run: write the releases and the site under FOLDER instead')
    args = ap.parse_args()
    if args.to:
        SITE, RELEASES = Path(args.to).resolve() / 'site', Path(args.to).resolve() / 'releases'
        SITE.mkdir(parents=True, exist_ok=True)
        for page in TOP_PAGES:                                       # (so that check_site can check the practice site too)
            if not (SITE / page).exists() and (ROOT / 'site' / page).exists():
                shutil.copy2(ROOT / 'site' / page, SITE / page)
    site_cmd = f'python3 tools/serve.py "{SITE}" 8797' if args.to else 'python3 tools/serve.py site 8797'
    check_cmd = f'python3 tools/check_site.py "{SITE}"' if args.to else 'python3 tools/check_site.py'
    guides = registry()
    if args.list or not args.guide:
        for name, entry in guides.items():
            log = history(name)['log']
            last = next((e for e in reversed(log) if e['action'] in ('published', 'restored', 'taken down')), None)
            logged = None if not last or last['action'] == 'taken down' else last.get('release')
            now = on_site(name)
            odd = '' if now == logged else f'   (the history says {logged or "not on the website"})'
            print(f'{name:40s} on the website: {now or "-":5s} releases: {", ".join(f"r{n}" for n in releases_of(name)) or "none"}   '
                  f'({entry["folder"]}/{entry["steps"]}){odd}')
        return
    name = args.guide
    if name not in guides:
        raise SystemExit(f'"{name}" is not in guides.json: {", ".join(guides)}')
    if args.restore and not RELEASE.match(args.restore):
        raise SystemExit(f'--restore takes a release name such as r3, not "{args.restore}"')
    RELEASES.mkdir(parents=True, exist_ok=True)
    with open(RELEASES / '.lock', 'w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit('another publish is running')
        tidy(name)
        h = history(name)
        when = datetime.datetime.now().isoformat(timespec='seconds')
        was = on_site(name)
        if args.take_down:
            shutil.rmtree(SITE / name, ignore_errors=True)
            h['log'].append(dict(when=when, action='taken down', was=was, note=args.note))
            save_history(name, h)
            site_pages.build(SITE, write_yaml=not args.to)
            print(f'{name}: taken off the website (site/{name}/ removed; commit and push to make it so). Releases kept: '
                  f'{", ".join(f"r{n}" for n in releases_of(name)) or "none"}')
            return
        if args.restore:
            src = RELEASES / name / args.restore
            if not (src / 'release.json').exists():
                raise SystemExit(f'{name} has no release {args.restore}: {", ".join(f"r{n}" for n in releases_of(name)) or "none"}')
            put_on_site(name, src)
            h['log'].append(dict(when=when, action='restored', release=args.restore, was=was, note=args.note))
            save_history(name, h)
            site_pages.build(SITE, write_yaml=not args.to)
            print(f'{name}: {args.restore} is back in site/{name}/. Look: {site_cmd} -> http://localhost:8797/{name}/ ; then commit and push.')
            return
        if not args.note:
            raise SystemExit('say what changed: --note "..."')
        final, record, warnings = build_release(name, guides[name], args.note)
        report = changes(name, final, was)
        try:
            put_on_site(name, final)
        except BaseException:
            h['log'].append(dict(when=when, action='made, not on the site', release=record['release'], note=args.note))
            save_history(name, h)
            raise
        h['log'].append(dict(when=when, action='published', release=record['release'], note=args.note, source=record['source']))
        save_history(name, h)
        site_pages.build(SITE, write_yaml=not args.to)
    size = sum((final / f).stat().st_size for f in record['files'])
    print(f'{name}: {record["release"]} published to site/{name}/ ({len(record["files"])} files, {size / 1e6:.1f} MB; {record["views"]} views)')
    for line in report:
        print('  ' + line)
    for w in warnings:
        print('  WARNING: ' + w)
    if record['source']['uncommitted_changes']:
        print('  NOTE: the guide\'s sources had uncommitted changes: commit the sources first, so that the release names their commit')
    print(f'  Look first: {site_cmd} -> http://localhost:8797/{name}/   then: {check_cmd}')
    print('  Then commit site/, releases/, render.yaml and guides.json; it goes live when pushed to the branch Render deploys (only on Lee\'s word).')


if __name__ == '__main__':
    main()
