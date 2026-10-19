"""The PMG's printing, written to decals.json (materials.json "decals" names it).

    .venv.nosync/bin/python "PMG Build Instructions/silkscreen.py"      then   .venv.nosync/bin/python tools/build_model.py "PMG Build Instructions"

- NAUO78, the Nano I/O module on the back panel H4: the MRA's module print (its decals.json, written by its silkscreen.py), carried
  over unchanged, as the RCC's: the board is the same CAD model with every part in the same place, so the one rigid move that takes
  the MRA's module onto the PMG's (cad-geometry.json "mra_module_to_pmg", written by make_source.py: measured on the board mesh both
  files share, with the module turned the published way up) takes its print there too. Only each picture's corner and directions
  change; white on navy, as on the MRA and the RCC. (This assumes the PMG kit's module is the board in Lee's MRA photos, as the
  RCC's was confirmed to be, 16 Oct 2026.)
The button, display and matrix boards carry no print yet (their pins are named by the guide's labels; a question for Lee).
"""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
MRA_DECALS = HERE.parent / 'MRA Build Instructions Prototype' / 'decals.json'
M = np.array(json.load(open(HERE / 'cad-geometry.json'))['mra_module_to_pmg'], float)
R, T = M[:3, :3], M[:3, 3]
r3 = lambda a: round(float(a), 3)

module = []
for d in json.load(open(MRA_DECALS))['NAUO82']:
    d = dict(d)
    d['origin'] = [r3(c) for c in R @ np.array(d['origin'], float) + T]
    d['u'] = [int(round(c)) for c in R @ np.array(d['u'], float)]
    d['v'] = [int(round(c)) for c in R @ np.array(d['v'], float)]
    module.append(d)

out = {'_about': 'Printing on parts, drawn by the player (js/core.js); materials.json "decals" names this file. Written by silkscreen.py: edit that, not this.',
       'NAUO78': module}
with open(HERE / 'decals.json', 'w') as f:                # (one item a line, as the MRA's and RCC's)
    f.write('{\n "_about": ' + json.dumps(out['_about']) + ',\n "NAUO78": [\n')
    for k, d in enumerate(module):
        head = {kk: vv for kk, vv in d.items() if kk != 'items'}
        f.write('  ' + json.dumps(head)[:-1] + ', "items": [\n' + ',\n'.join('   ' + json.dumps(it) for it in d['items']) + ']}' + (',' if k < len(module) - 1 else '') + '\n')
    f.write(' ]\n}\n')
json.load(open(HERE / 'decals.json'))                     # (it must read back)
for d in module:
    print(f"{d['name']}: origin {d['origin']} u {d['u']} v {d['v']} size {d['size']} ({len(d['items'])} items)")
