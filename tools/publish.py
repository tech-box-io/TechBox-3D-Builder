"""Publish a guide: freeze what it is now as a release, and make that the version the website serves.

    python3 tools/publish.py <guide> --note "what changed"    a new release of that guide (guides.json names them)
    python3 tools/publish.py <guide> --restore r3             put an earlier release back on the website (a roll-back)
    python3 tools/publish.py <guide> --take-down              take the guide off the website (its releases are kept)
    python3 tools/publish.py --list                           every guide: which release the website has, and the others
    (add --to <folder> for a practice run that writes there instead of releases/ and site/)

How it fits together:
- The kit folder is where a guide is written and checked (guide.py -> steps.json, model.glb, parts/). The player is the one copy
  in player/.
- A release is a frozen copy of exactly the files a learner's browser needs: the player (player.html becomes index.html), the
  guide's steps (as steps.json, with the Review notes and other authoring data taken out), the kit's model, the logo and the part
  pictures its Parts List shows. Nothing else: no CAD, no guide.py, no colours file, no research. Releases are kept in
  releases/<guide>/r<N>/ with a record (release.json: when, why, the source's git commit, every file's checksum). They never change
  and are never uploaded: tools/serve.py releases shows them on this computer only.
- site/<guide>/ is the one copy the website serves (Render publishes site/ only): always the release published or restored last.
  The address never changes, so an LMS embed of https://<domain>/<guide>/ always shows the current version, and earlier versions
  cannot be reached from the web.
- Nothing goes live until site/ is committed and pushed (Render deploys on push). Before that, look at it exactly as it will be
  served: python3 tools/serve.py site 8797, then http://localhost:8797/<guide>/ .

Only the standard library; light (it copies files), but it takes the same lock as the other jobs so that two sessions cannot
publish at once.
"""
import argparse
import datetime
import fcntl
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAYER = ROOT / 'player'
SITE = ROOT / 'site'
RELEASES = ROOT / 'releases'
NAME = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
PLAYER_FILES = ['js/core.js', 'js/player.js']                       # (not parts.html, parts.js or runthrough.js: authoring tools)
AUTHORING_KEYS = ('review', 'text_key')                              # per view: Review notes for TechBox; the step-text spreadsheet's key
FRESH_IMPORT = "import('./js/player.js?v=' + Date.now());"          # player.html's "a fresh copy on every load", for authoring


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def registry():
    guides = json.load(open(ROOT / 'guides.json'))['guides']
    for name in guides:
        if not NAME.match(name):
            raise SystemExit(f'guides.json: "{name}" is not a web-address name (lower-case words joined by hyphens)')
    return guides


def releases_of(name):
    folder = RELEASES / name
    return sorted((int(p.name[1:]) for p in folder.glob('r*') if p.is_dir() and p.name[1:].isdigit())) if folder.exists() else []


def history():
    path = RELEASES / 'history.json'
    return json.load(open(path)) if path.exists() else {}


def save_history(h):
    RELEASES.mkdir(exist_ok=True)
    (RELEASES / 'history.json').write_text(json.dumps(h, indent=1) + '\n')


def git_source():
    """The commit the sources were at, and whether anything that makes a guide had uncommitted changes."""
    try:
        head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        dirty = subprocess.run(['git', 'status', '--porcelain', '--', '.', ':!site', ':!releases'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        return dict(commit=head, uncommitted_changes=bool(dirty))
    except (OSError, subprocess.CalledProcessError):
        return dict(commit=None, uncommitted_changes=None)


def published_steps(steps, release):
    """The learner's copy of the steps: no Review notes, no authoring keys; the model named so that a new release is fetched afresh."""
    out = dict(steps)
    out['meta'] = {k: v for k, v in steps['meta'].items() if k != 'review_notes'}
    out['meta'].update(review_notes=False, release=release)
    out['model'] = steps['model'].split('?')[0] + f'?v={release}'
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
                if item['picture'] not in files:
                    files.append(item['picture'])
    return files


def build_release(name, entry, note):
    kit = ROOT / entry['kit']
    steps_file = kit / entry['steps']
    steps = json.load(open(steps_file))
    files = needed_files(steps)
    missing = [f for f in files if not (kit / f).exists()]
    if missing:
        raise SystemExit(f'{name}: missing in {kit.name}: {", ".join(missing)} (part pictures: open parts.html through tools/serve.py)')
    model = kit / files[0]
    warnings = []
    stale = [f for f in files[1:] if f.startswith('parts/') and (kit / f).stat().st_mtime < model.stat().st_mtime]
    if stale:
        warnings.append(f'{len(stale)} part picture(s) are older than the model; re-render them with parts.html if the model changed: {", ".join(stale[:4])}{" ..." if len(stale) > 4 else ""}')
    if steps_file.stat().st_mtime < (kit / 'guide.py').stat().st_mtime:
        warnings.append(f'{entry["steps"]} is older than guide.py: has guide.py been run since its last edit?')
    reviews = sum(1 for v in steps['views'] if v.get('review'))
    if reviews:
        warnings.append(f'{reviews} view(s) carry Review notes; they are left out of the published copy (still in the kit)')
    page = (PLAYER / 'player.html').read_text()
    if page.count(FRESH_IMPORT) != 1:
        raise SystemExit('publish.py: player.html has changed shape (its player.js import); update FRESH_IMPORT')

    number = (releases_of(name) or [0])[-1] + 1
    release = f'r{number}'
    final = RELEASES / name / release
    tmp = RELEASES / name / f'.{release}.tmp'
    if final.exists():
        raise SystemExit(f'{final} exists already: a release is never overwritten')
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    (tmp / 'index.html').write_text(page.replace(FRESH_IMPORT, f"import('./js/player.js?v={release}');"))
    for f in PLAYER_FILES:
        (tmp / f).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PLAYER / f, tmp / f)
    shutil.copytree(PLAYER / 'vendor', tmp / 'vendor', ignore=shutil.ignore_patterns('.DS_Store'))
    (tmp / 'steps.json').write_text(json.dumps(published_steps(steps, release), separators=(',', ':'), ensure_ascii=False))
    for f in files:
        (tmp / f).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(kit / f, tmp / f)
    record = dict(guide=name, release=release, published=datetime.datetime.now().isoformat(timespec='seconds'), note=note,
                  kit=entry['kit'], steps=entry['steps'], title=steps['meta'].get('title'), part=steps['meta'].get('part'),
                  views=len(steps['views']), source=git_source(),
                  files={str(p.relative_to(tmp)): sha256(p) for p in sorted(tmp.rglob('*')) if p.is_file()})
    (tmp / 'release.json').write_text(json.dumps(record, indent=1) + '\n')
    tmp.rename(final)
    return final, record, warnings


def put_on_site(name, release_dir):
    """Make site/<guide>/ an exact copy of a release (less its record), replacing what was there."""
    SITE.mkdir(exist_ok=True)
    target, tmp, old = SITE / name, SITE / f'.{name}.tmp', SITE / f'.{name}.old'
    for p in (tmp, old):
        shutil.rmtree(p, ignore_errors=True)
    shutil.copytree(release_dir, tmp, ignore=shutil.ignore_patterns('release.json', '.DS_Store'))
    if target.exists():
        target.rename(old)
    tmp.rename(target)
    shutil.rmtree(old, ignore_errors=True)


def changes(name, new_dir):
    """What differs from the release that was on the website before."""
    h = history().get(name, {})
    before = h.get('on_site')
    if not before or not (RELEASES / name / before / 'release.json').exists():
        return ['(the first release of this guide)']
    old = json.load(open(RELEASES / name / before / 'release.json'))['files']
    new = json.load(open(new_dir / 'release.json'))['files']
    out = [f'changed: {f}' for f in sorted(new) if f in old and old[f] != new[f] and f != 'release.json']
    out += [f'added: {f}' for f in sorted(set(new) - set(old))]
    out += [f'removed: {f}' for f in sorted(set(old) - set(new))]
    return [f'compared with {before}:'] + (out or ['no file differs'])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('guide', nargs='?')
    ap.add_argument('--note', help='what changed (kept in the release record)')
    ap.add_argument('--restore', metavar='rN', help='put an earlier release back on the website')
    ap.add_argument('--take-down', action='store_true', help='take the guide off the website')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--to', metavar='FOLDER', help='a practice run: write the releases and the site under FOLDER instead')
    args = ap.parse_args()
    if args.to:
        global SITE, RELEASES
        SITE, RELEASES = Path(args.to).resolve() / 'site', Path(args.to).resolve() / 'releases'
    guides = registry()
    if args.list or not args.guide:
        h = history()
        for name, entry in guides.items():
            rs = releases_of(name)
            print(f'{name:40s} on the website: {h.get(name, {}).get("on_site") or "-":5s} releases: {", ".join(f"r{n}" for n in rs) or "none"}   ({entry["kit"]}/{entry["steps"]})')
        return
    name = args.guide
    if name not in guides:
        raise SystemExit(f'"{name}" is not in guides.json: {", ".join(guides)}')
    RELEASES.mkdir(exist_ok=True)
    with open(RELEASES / '.lock', 'w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit('another publish is running')
        h = history()
        entry = h.setdefault(name, {'on_site': None, 'log': []})
        when = datetime.datetime.now().isoformat(timespec='seconds')
        if args.take_down:
            shutil.rmtree(SITE / name, ignore_errors=True)
            entry['log'].append(dict(when=when, action='taken down', was=entry['on_site']))
            entry['on_site'] = None
            save_history(h)
            print(f'{name}: taken off the website (site/{name}/ removed; commit and push to make it so). Releases kept: {releases_of(name)}')
            return
        if args.restore:
            src = RELEASES / name / args.restore
            if not (src / 'release.json').exists():
                raise SystemExit(f'{name} has no release {args.restore}: {", ".join(f"r{n}" for n in releases_of(name))}')
            put_on_site(name, src)
            entry['log'].append(dict(when=when, action='restored', release=args.restore, was=entry['on_site']))
            entry['on_site'] = args.restore
            save_history(h)
            print(f'{name}: {args.restore} is back in site/{name}/. Look: python3 tools/serve.py site 8797 -> http://localhost:8797/{name}/ ; '
                  'then commit and push to put it live.')
            return
        if not args.note:
            raise SystemExit('say what changed: --note "..."')
        final, record, warnings = build_release(name, guides[name], args.note)
        report = changes(name, final)
        put_on_site(name, final)
        entry['log'].append(dict(when=when, action='published', release=record['release'], note=args.note, source=record['source']))
        entry['on_site'] = record['release']
        save_history(h)
    size = sum((final / f).stat().st_size for f in record['files'])
    print(f'{name}: {record["release"]} published to site/{name}/ ({len(record["files"])} files, {size / 1e6:.1f} MB; {record["views"]} views)')
    for line in report:
        print('  ' + line)
    for w in warnings:
        print('  WARNING: ' + w)
    if record['source']['uncommitted_changes']:
        print('  NOTE: the sources had uncommitted changes; commit them with the release so that it can be traced')
    print(f'  Look first: python3 tools/serve.py site 8797 -> http://localhost:8797/{name}/   (python3 tools/check_site.py checks the site)')
    print('  Then commit and push: Render deploys site/ and the address shows this release.')


if __name__ == '__main__':
    main()
