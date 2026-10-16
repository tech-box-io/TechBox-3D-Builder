"""Check site/ (what the website serves) before it goes out: Render runs this as its build command, so a failed check stops the
deploy and the previous one stays live. Run it yourself too before committing a publish:

    python3 tools/check_site.py            (or: python3 tools/check_site.py <a site folder>, e.g. a practice publish's)

It makes sure that site/ holds only the published guides named in guides.json, each a complete copy (the player, its steps, the
model, the logo and the part pictures its Parts List shows), and nothing that should stay in this folder: no CAD, no guide.py or
colours file, no Review notes, no authoring tools. Only the standard library.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / 'site'
TOP_FILES = {'index.html', 'robots.txt', '404.html'}
REQUIRED = ['index.html', 'js/player.js', 'js/core.js', 'vendor/three/three.module.min.js', 'steps.json']
ALLOWED = {'.html', '.js', '.json', '.glb', '.png', '.webp', '.svg', '.txt'}
FORBIDDEN_NAMES = {'guide.py', 'materials.json', 'wire-paths.json', 'decals.json', 'engraved-codes.json', 'model.report.json',
                   'parts.json', 'parts.csv', 'release.json', 'parts.html', 'parts.js', 'runthrough.js', 'player.html', 'history.json'}
FORBIDDEN_IN_NAME = ('colour-atlas', '.step', '.stp', '.command', 'silkscreen', '.py')


def check():
    errors, total = [], 0
    if not SITE.is_dir():
        return [f'{SITE} is missing'], 0
    guides = json.load(open(ROOT / 'guides.json'))['guides']
    for p in sorted(SITE.iterdir()):
        if p.name.startswith('.'):
            errors.append(f'site/{p.name}: hidden files and unfinished copies must not be published')
        elif p.is_file() and p.name not in TOP_FILES:
            errors.append(f'site/{p.name}: not a file the site needs at its top level')
        elif p.is_dir() and p.name not in guides:
            errors.append(f'site/{p.name}/: not a guide in guides.json')
    for name in guides:
        folder = SITE / name
        if not folder.exists():
            continue                                                     # (not published, or taken down)
        files = [p for p in folder.rglob('*') if p.is_file()]
        total += sum(p.stat().st_size for p in files)
        for f in REQUIRED:
            if not (folder / f).is_file():
                errors.append(f'{name}: {f} is missing')
        for p in files:
            rel = p.relative_to(folder).as_posix()
            lower = p.name.lower()
            if p.name.startswith('.'):
                errors.append(f'{name}: {rel}: hidden file')
            elif lower in FORBIDDEN_NAMES or any(s in lower for s in FORBIDDEN_IN_NAME):
                errors.append(f'{name}: {rel}: an authoring file, never published')
            elif p.suffix.lower() not in ALLOWED and p.name != 'LICENSE':
                errors.append(f'{name}: {rel}: not a file type the player uses')
            elif p.stat().st_size < 200 and p.read_bytes().startswith(b'version https://git-lfs'):
                errors.append(f'{name}: {rel}: a Git LFS pointer, not the file itself')
        steps_path = folder / 'steps.json'
        if not steps_path.is_file():
            continue
        try:
            steps = json.load(open(steps_path))
        except ValueError as e:
            errors.append(f'{name}: steps.json does not read: {e}')
            continue
        page = (folder / 'index.html').read_text() if (folder / 'index.html').is_file() else ''
        if 'Date.now()' in page or "js/player.js?v=" not in page:
            errors.append(f'{name}: index.html is not a published copy of the player (made by tools/publish.py)')
        if steps.get('meta', {}).get('review_notes') is not False:
            errors.append(f'{name}: steps.json is not a published copy (meta.review_notes should be false)')
        for k, view in enumerate(steps.get('views', [])):
            for key in ('review', 'text_key'):
                if key in view:
                    errors.append(f'{name}: steps.json view {k} ({view.get("name")}) still has "{key}"')
                    break
        model = folder / steps.get('model', '').split('?')[0]
        if not model.is_file():
            errors.append(f'{name}: the model {model.name} named in steps.json is missing')
        elif model.read_bytes()[:4] != b'glTF':
            errors.append(f'{name}: {model.name} is not a binary glTF file')
        glbs = [p.relative_to(folder).as_posix() for p in files if p.suffix.lower() == '.glb']
        if glbs != [model.relative_to(folder).as_posix()] and model.is_file():
            errors.append(f'{name}: .glb files other than the model: {", ".join(g for g in glbs if g != model.name)}')
        wanted = [steps.get('meta', {}).get('logo')] + [item['picture'] for view in steps.get('views', []) for group in view.get('parts', []) for item in group['items']]
        for f in {w for w in wanted if w}:
            if not (folder / f).is_file():
                errors.append(f'{name}: {f} (named in steps.json) is missing')
    return errors, total


if __name__ == '__main__':
    if len(sys.argv) > 1:
        SITE = Path(sys.argv[1]).resolve()
    errors, total = check()
    for e in errors:
        print('ERROR: ' + e)
    published = [p.name for p in SITE.iterdir() if p.is_dir() and not p.name.startswith('.')] if SITE.is_dir() else []
    print(f'site/: {len(published)} guide(s) ({", ".join(published) or "none"}), {total / 1e6:.1f} MB; '
          f'{"OK" if not errors else f"{len(errors)} problem(s)"}')
    sys.exit(1 if errors else 0)
