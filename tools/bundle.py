"""Pack a kit's guide into one HTML file that opens by double-click, with no server and no internet.

    python tools/bundle.py "<kit folder>" "<out.html>" [steps file]

Everything the player loads goes inside the file: the guide's steps (steps.json, or the steps file named, e.g. a chapter's),
model.glb and the logo (as data), the player's own code (from player/, the one copy) and three.js (as modules, each a data: URL
in the page's import map). For sending a guide to someone to look at on their own computer. It is a snapshot: re-run it after
regenerating the guide. The live kit folder keeps working as before. (Learners get the hosted guide: tools/publish.py.)
"""
import base64
import json
import posixpath
import re
import sys
from pathlib import Path

IMPORT = re.compile(r"""(\bfrom\s*|\bimport\s*\(?\s*)(['"])([^'"]+)\2""")


def data_url(raw, mime):
    return f'data:{mime};base64,' + base64.b64encode(raw).decode('ascii')


PLAYER = Path(__file__).resolve().parent.parent / 'player'      # the one copy of the player


def bundle(kit, out, steps_file='steps.json'):
    kit = Path(kit)
    vendor = PLAYER / 'vendor' / 'three'
    modules = {}                                     # bare specifier -> source text

    def addon_name(path):
        return 'three/addons/' + path.relative_to(vendor / 'addons').as_posix()

    def relink(source, here):
        """Every relative import in an addon becomes the bare name the import map gives it (a data: URL has no base to resolve against)."""
        def fix(m):
            spec = m.group(3)
            if spec.startswith('.'):
                spec = posixpath.normpath(posixpath.join(posixpath.dirname(here), spec))
            return f'{m.group(1)}{m.group(2)}{spec}{m.group(2)}'
        return IMPORT.sub(fix, source)

    modules['three'] = (vendor / 'three.module.min.js').read_text()
    for path in sorted((vendor / 'addons').rglob('*.js')):
        name = addon_name(path)
        modules[name] = relink(path.read_text(), name)
    core = (PLAYER / 'js' / 'core.js').read_text()
    player = (PLAYER / 'js' / 'player.js').read_text()
    fresh = "await import('./core.js' + new URL(import.meta.url).search)"
    fetch_steps = re.compile(r"const data = await fetch\(stepsFile[^\n]*\n")
    if fresh not in player or not fetch_steps.search(player):
        raise SystemExit('bundle.py: player.js has changed shape (the core import or the steps fetch); update bundle.py')
    player = player.replace(fresh, "await import('mra/core')")
    player = fetch_steps.sub("const data = JSON.parse(document.getElementById('mra-steps').textContent);   // (packed into this file by tools/bundle.py)\n", player, count=1)
    modules['mra/core'] = core
    modules['mra/player'] = player

    steps = json.load(open(kit / steps_file))
    steps['model'] = data_url((kit / steps['model'].split('?')[0]).read_bytes(), 'model/gltf-binary')
    for view in steps['views']:                      # the parts list's pictures (parts/*.png, from parts.html)
        for group in view.get('parts', []):
            for item in group['items']:
                picture = kit / item['picture']
                if not picture.exists():
                    raise SystemExit(f'bundle.py: {item["picture"]} is missing: open parts.html through tools/serve.py to make the part pictures')
                item['picture'] = data_url(picture.read_bytes(), 'image/png')
    logo = steps['meta'].get('logo')
    if logo:
        mime = {'.svg': 'image/svg+xml', '.png': 'image/png', '.webp': 'image/webp'}[Path(logo).suffix.lower()]
        steps['meta']['logo'] = data_url((kit / logo).read_bytes(), mime)

    page = (PLAYER / 'player.html').read_text()
    imports = {name: data_url(src.encode('utf-8'), 'text/javascript') for name, src in modules.items()}
    page, n1 = re.subn(r'<script type="importmap">.*?</script>', lambda m: '<script type="importmap">' + json.dumps({'imports': imports}) + '</script>', page, flags=re.S)
    page, n2 = re.subn(r'<link rel="modulepreload"[^\n]*\n', '', page)
    steps_json = json.dumps(steps, separators=(',', ':')).replace('</', '<\\/')
    page, n3 = re.subn(r'<script type="module">import\(\'\./js/player\.js[^<]*</script>',
                       lambda m: f'<script type="application/json" id="mra-steps">{steps_json}</script>\n<script type="module">import \'mra/player\';</script>', page)
    if (n1, n3) != (1, 1):
        raise SystemExit('bundle.py: player.html has changed shape (the import map or the player script); update bundle.py')
    page = page.replace('Check your connection and reload the page.', 'Try opening this file in Safari or Chrome.')
    Path(out).write_text(page)
    return Path(out).stat().st_size


if __name__ == '__main__':
    if len(sys.argv) not in (3, 4):
        raise SystemExit(__doc__)
    size = bundle(*sys.argv[1:])
    print(f'{sys.argv[2]}: {size / 1e6:.1f} MB')
