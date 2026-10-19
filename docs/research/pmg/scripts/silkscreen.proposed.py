"""PROPOSAL for "PMG Build Instructions/silkscreen.py": the PMG's printing, written to decals.json (materials.json "decals" names it).

    .venv.nosync/bin/python "PMG Build Instructions/silkscreen.py"      then   .venv.nosync/bin/python tools/build_model.py "PMG Build Instructions"
    (here, for review, it writes nothing unless given an output path: .venv.nosync/bin/python docs/research/pmg/scripts/silkscreen.proposed.py [<out.json>])

- NAUO78, the Nano I/O module on H4: the MRA's module print (its decals.json, written by its silkscreen.py), carried over unchanged:
  the board is the same CAD model with every part in the same place (all 36 meshes, to 0.0001 mm), standing on edge against
  the back panel, so one rigid turn and move takes the MRA's print onto it (docs/research/pmg/reuse_plan.md 2.4). Only the four
  pictures' corners and directions change; white on navy, as on the MRA and the RCC. This is the RCC's silkscreen.py, shield
  part, with the PMG's R and T.
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
KIT = HERE if (HERE / 'pmg.glb').exists() else Path('/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions')
MRA_DECALS = KIT.parent / 'MRA Build Instructions Prototype' / 'decals.json'
r3 = lambda a: round(float(a), 3)

# p_PMG = R p_MRA + T: the MRA's I/O module (NAUO82) onto the PMG's NAUO78 (docs/research/pmg/scripts/reuse_compare.py: exact on all 36
# shared meshes). R is a third of a turn about (1, 1, -1): MRA up (+y) -> PMG +x (out of the back panel H4), MRA +x -> PMG -z, MRA +z -> PMG -y.
R = np.array([[0, 1, 0], [0, 0, -1], [-1, 0, 0]], float)
T = np.array([490.546, 1077.982, 1360.501])
module = []
for d in json.load(open(MRA_DECALS))['NAUO82']:
    d = dict(d)
    d['origin'] = [r3(c) for c in R @ np.array(d['origin'], float) + T]
    d['u'] = [int(round(c)) for c in R @ np.array(d['u'], float)]
    d['v'] = [int(round(c)) for c in R @ np.array(d['v'], float)]
    module.append(d)

out = {'_about': 'Printing on parts, drawn by the player (js/core.js); materials.json "decals" names this file. Written by silkscreen.py: edit that, not this.',
       'NAUO78': module}
for d in module:
    print(f"{d['name']}: origin {d['origin']} u {d['u']} v {d['v']} size {d['size']} ({len(d['items'])} items)")
if len(sys.argv) > 1 or (HERE / 'pmg.glb').exists():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / 'decals.json'
    with open(path, 'w') as f:                            # (one item a line, as the MRA's and RCC's)
        f.write('{\n "_about": ' + json.dumps(out['_about']) + ',\n "NAUO78": [\n')
        for k, d in enumerate(module):
            head = {kk: vv for kk, vv in d.items() if kk != 'items'}
            f.write('  ' + json.dumps(head)[:-1] + ', "items": [\n' + ',\n'.join('   ' + json.dumps(it) for it in d['items']) + ']}' + (',' if k < len(module) - 1 else '') + '\n')
        f.write(' ]\n}\n')
    json.load(open(path))
    print('written', path)
