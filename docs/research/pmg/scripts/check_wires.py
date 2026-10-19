"""Where the PMG guide's drawn wires pass through a part: every view's wires, bent with their end parts as the player bends them
(player.js skinned()), against the wood (and the boards) where the view shows them.

    .venv.nosync/bin/python docs/research/pmg/scripts/check_wires.py [steps.json] [--parts all]

Reports, per view and wire, the deepest point of the wire's centre line inside a part (mm past the part's surface; the wire is
1.25 mm across, so anything over about 0.6 shows) and where it is. One process, about 400 MB.
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
KIT = ROOT / 'PMG Build Instructions'
sys.path.insert(0, str(ROOT / 'tools'))
from stepgen import Model, _matrix  # noqa: E402

steps = json.load(open(KIT / (sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else 'steps.json')))
WOOD = ['NAUO60', 'NAUO61', 'NAUO62', 'NAUO63', 'NAUO64', 'NAUO65', 'NAUO66', 'NAUO67', 'NAUO68', 'NAUO69', 'NAUO70', 'NAUO71', 'NAUO72',
        'NAUO73', 'NAUO74', 'NAUO75', 'NAUO77']
OTHER = ['NAUO78', 'NAUO79', 'NAUO81', 'NAUO76', 'NAUO83', 'NAUO84', 'NAUO85', 'NANO']
check = WOOD + (OTHER if '--parts' in sys.argv else [])
model = Model(KIT / 'pmg-guide.glb')
routes = steps['routes']
for r in routes:
    p = np.asarray(r['pts'], float)
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    r['_s'] = s / (s[-1] or 1)


def ramp(s):
    t = np.clip((s - 0.1) / 0.8, 0, 1)
    return t * t * (3 - 2 * t)


def end_move(part, ref, poses):
    if not part or (poses.get(part) is None and ref is None):
        return None
    M = _matrix(poses.get(part))
    return M @ np.linalg.inv(_matrix(ref)) if ref is not None else M


def skinned(r, poses):
    p = np.asarray(r['pts'], float)
    A, B = end_move(r.get('a'), r.get('a_ref'), poses), end_move(r.get('b'), r.get('b_ref'), poses)
    if A is None and B is None:
        return p
    wb = ramp(r['_s'])[:, None] if r.get('b') else np.zeros((len(p), 1))
    wa = 1 - wb if r.get('a') else np.zeros((len(p), 1))
    out = p.copy()
    if A is not None:
        out += wa * ((p @ A[:3, :3].T + A[:3, 3]) - p)
    if B is not None:
        out += wb * ((p @ B[:3, :3].T + B[:3, 3]) - p)
    return out


import trimesh  # noqa: E402
found = {}
for vi, v in enumerate(steps['views']):
    wires = v.get('wires') or {}
    if not wires:
        continue
    poses = v.get('offsets') or {}
    for wid, no in wires.items():
        pts = skinned(routes[no], poses)
        worst = (0.0, None, None)
        for part in check:
            if part not in v.get('visible', []):
                continue
            q = pts
            pose = poses.get(part)
            if pose is not None:
                M = np.linalg.inv(_matrix(pose))
                q = pts @ M[:3, :3].T + M[:3, 3]
            mesh = model.inst[part]
            lo, hi = mesh.bounds
            near = np.all((q > lo - 1) & (q < hi + 1), axis=1)
            if not near.any():
                continue
            d = trimesh.proximity.signed_distance(mesh, q[near])     # (positive inside)
            k = int(np.argmax(d))
            if d[k] > worst[0]:
                worst = (float(d[k]), part, pts[near][k].round(1).tolist())
        if worst[0] > 0.3:
            key = (wid, worst[1])
            found.setdefault(key, []).append((vi, v['name'], round(worst[0], 2), worst[2]))
for (wid, part), hits in sorted(found.items(), key=lambda t: -max(h[2] for h in t[1])):
    deepest = max(hits, key=lambda h: h[2])
    print(f'{wid:16s} through {part:7s} in {len(hits):2d} views, deepest {deepest[2]:5.2f} mm at {deepest[3]} ({deepest[1]}); views {hits[0][1]} .. {hits[-1][1]}')
print(f'{len(found)} wire / part pairs')
