"""Measure the DRAPED wire shapes at rest (sockets on the table), the D9s in and swept up, against every part, the table and the other wires
(the LSM deconstruction's Step 12, 22 Oct 2026). Run from the project folder: .venv.nosync/bin/python -I docs/research/lsm/decon/round3/drape_check.py
It loads the model (about 1 GB): run it as the only heavy job. Its output of 22 Oct 2026: drape_check_at_rest.txt beside it."""
import sys
import numpy as np
from pathlib import Path
KIT = Path(__file__).resolve().parents[5] / 'LSM Build Instructions'
sys.path.insert(0, str(KIT))
import wire_shapes as WS
from stepgen import apply_pose, turn_dir
for w in WS.JUMPERS:
    pose = WS.draped_socket(w)
    print(w, 'socket pose', pose, 'wire leaves along', np.round(turn_dir(pose, [0, 0, 1]), 3))
routes = WS.draped()
for k, r in routes.items():
    p = np.asarray(r['pts']); print(k, 'pts', len(p), 'length', round(float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum()), 1), 'b_from', round(r['b_from'], 1), 'ends', p[0].round(2), p[-1].round(2), 'min y', p[:, 1].min().round(2))
parts = WS.Parts.load(cache=sys.argv[1] if len(sys.argv) > 1 else None, write_cache=None)
poses = {WS.FEMALE[w]: WS.draped_socket(w) for w in WS.JUMPERS}
present = WS.BASE + ['D9_A', 'D9_B'] + WS.CAPS
res = WS.measure(parts, routes, poses, present, others=WS.other_wires(), sweep=['D9_A', 'D9_B'])
for w, r in res.items():
    print(f"{w}: least {r['min'][0]:+.2f} ({r['min'][1]} at {r['min'][2]})")
    print('   ', ', '.join(f'{k} {v[0]:+.2f}' for v, k in sorted([(v, k) for k, v in {**r['parts'], **r['wires']}.items()])[:6]))
# the sockets lying on the table, against the parts and the USB cable
from scipy.spatial import cKDTree
cable = WS._dense(WS.other_wires()['usb cable']['pts'])[0]
for w in WS.JUMPERS:
    v = apply_pose(poses[WS.FEMALE[w]], parts.m[WS.FEMALE[w]].vertices)
    near = []
    for o in WS.BASE + ['D9_A', 'D9_B']:
        c = parts.clearance(o, WS.ZERO, v, 0.0, reach=5.0)
        if np.isfinite(c).any(): near.append((round(float(np.nanmin(c)), 2), o))
    near.append((round(float(cKDTree(cable).query(v)[0].min() - WS.other_wires()['usb cable']['radius']), 2), 'usb cable'))
    near.append((round(float(v[:, 1].min() - WS.TABLE_Y), 2), 'table'))
    print('socket', w, sorted(near)[:4])
