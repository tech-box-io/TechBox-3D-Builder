"""Clearance of Step 43's in-between shapes at their stops (the buzzer at LIFT and at HIGH, every other part as in Step 43c, the other
wires at rest): smallest gaps to parts (the buzzer too) and to other wires, as static.py measures them."""
import json, sys, gc
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/tools')
from stepgen import Model, unapply_pose, _matrix
KIT = Path('/Users/lee-johnson/Desktop/Claude_Cadasio/LAC Build Instructions')
steps = json.load(open(sys.argv[1]))
spec = json.load(open(KIT / 'materials.json'))
M = Model(KIT / spec['source'], adjust=spec.get('adjust_mm') or {}, own_parts=spec.get('own_parts', {}),
          extra_parts={i: (KIT / e['glb'], e['pose']) for i, e in spec.get('extra_parts', {}).items()})
V = {v['name']: v for v in steps['views']}
v = V['Step 43c']
R = steps['routes']
radius = {w: d['radius'] for w, d in steps['wires'].items()}


def dense(pts, step=0.2):
    pts = np.asarray(pts, float)
    L = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    s = np.arange(0.0, L[-1], step)
    return np.c_[[np.interp(s, L, pts[:, k]) for k in range(3)]].T, s, L[-1]


stops = {'LIFT': 1, 'HIGH': 2}
for name, k in stops.items():
    pose = v['path'][k]
    print(f'== {name} (the buzzer at {pose})')
    lines = {}
    for w in ('buzzer red', 'buzzer black'):
        lines[w] = R[v['wire_via'][w][k - 1]]['pts']
    for w, pts0 in lines.items():
        pts, s, L = dense(pts0)
        inner = pts[(s > 5.0) & (s < L - 5.0)]
        rad = radius[w]
        best = []
        others = {**{w2: R[ri]['pts'] for w2, ri in v['wires'].items() if not w2.startswith('buzzer')}, **{w2: p for w2, p in lines.items() if w2 != w}}
        for w2, p2 in others.items():
            q, _, _ = dense(p2)
            d, _ = cKDTree(q).query(inner)
            j = int(np.argmin(d))
            best.append((round(float(d[j] - rad - radius.get(w2, 0.625)), 2), 'wire ' + w2, inner[j].round(1).tolist()))
        offs = dict(v.get('offsets') or {}, NAUO62=pose)
        cap = R[v['wires'][w]]['a']
        for i in v['visible']:
            if i in (cap,):
                continue
            off = offs.get(i)
            q = unapply_pose(off, inner) if off is not None else inner
            lo, hi = M.inst[i].bounds
            sel = np.all((q > lo - 4) & (q < hi + 4), axis=1)
            if not sel.any():
                continue
            cp, d, tri = M.inst[i].nearest.on_surface(q[sel])
            inside = np.einsum('ij,ij->i', q[sel] - cp, M.inst[i].face_normals[tri]) < -0.3 * d
            g = np.where(inside, -d, d) - rad
            j = int(np.argmin(g))
            best.append((round(float(g[j]), 2), i, inner[sel][j].round(1).tolist()))
        best.sort()
        print(f'  {w}: ' + '; '.join(f'{g:+.2f} {what} {at}' for g, what, at in best[:5]))
