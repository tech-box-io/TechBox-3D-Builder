"""The buzzer (a moving part) against every other part on screen during Step 43c's motion, mixed as the player mixes poses (as
tools/motioncheck.py: mixPose, poseGap pacing): how far its surface reaches into each part (negative gap) or how close it comes.
    python partpath.py <steps file> [moments]"""
import json, sys, gc
from pathlib import Path
import numpy as np
from scipy.spatial.transform import Rotation, Slerp
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/tools')
from stepgen import Model, _matrix
KIT = Path('/Users/lee-johnson/Desktop/Claude_Cadasio/LAC Build Instructions')
steps = json.load(open(sys.argv[1]))
N = int(sys.argv[2]) if len(sys.argv) > 2 else 99
spec = json.load(open(KIT / 'materials.json'))
M = Model(KIT / spec['source'], adjust=spec.get('adjust_mm') or {}, own_parts=spec.get('own_parts', {}),
          extra_parts={i: (KIT / e['glb'], e['pose']) for i, e in spec.get('extra_parts', {}).items()})
V = {v['name']: v for v in steps['views']}
v = V['Step 43c']
path = v['path']
MOV = 'NAUO62'


def ease(k):
    return 4 * k ** 3 if k < 0.5 else 1 - (-2 * k + 2) ** 3 / 2


def mix(a, b, k):
    A, B = _matrix(a), _matrix(b)
    turned = lambda p: isinstance(p, dict) and p.get('r') and p['r'][3]
    c = np.asarray(((b if turned(b) else a).get('at') if (turned(a) or turned(b)) else None) or [0.0, 0.0, 0.0], float)
    R = Slerp([0, 1], Rotation.from_matrix([A[:3, :3], B[:3, :3]]))([k]).as_matrix()[0]
    X = np.eye(4); X[:3, :3] = R
    X[:3, 3] = (A[:3, :3] @ c + A[:3, 3]) * (1 - k) + (B[:3, :3] @ c + B[:3, 3]) * k - R @ c
    return X


def along(t):
    stops = v.get('stops') or list(range(len(path)))
    beats = len(stops) - 1
    b = min(beats - 1, int(t * beats))
    k = ease(t * beats - b)
    seg = path[stops[b]:stops[b + 1] + 1]
    if len(seg) == 2:
        return mix(seg[0], seg[1], k)
    raise SystemExit('via poses not handled')


verts = np.asarray(M.inst[MOV].vertices)
sub = verts[np.random.default_rng(1).choice(len(verts), min(len(verts), 4000), replace=False)]
moments = np.linspace(0, 1, N + 2)[1:-1]
posed = [(t, sub @ along(t)[:3, :3].T + along(t)[:3, 3]) for t in moments]
offs = v.get('offsets') or {}
res = []
for part in v['visible']:
    if part == MOV or part not in M.inst:
        continue
    mesh = M.inst[part]
    X = _matrix(offs.get(part)) if offs.get(part) is not None else np.eye(4)
    Xi = np.linalg.inv(X)
    lo, hi = mesh.bounds
    best = (99.0, None, None)
    for t, P in posed:
        q = P @ Xi[:3, :3].T + Xi[:3, 3]
        sel = np.all((q > lo - 3) & (q < hi + 3), axis=1)
        if not sel.any():
            continue
        cp, d, tri = mesh.nearest.on_surface(q[sel])
        inside = np.einsum('ij,ij->i', q[sel] - cp, mesh.face_normals[tri]) < -0.3 * d
        g = np.where(inside, -d, d)
        k = int(np.argmin(g))
        if g[k] < best[0]:
            best = (round(float(g[k]), 2), round(float(t), 3), P[sel][k].round(1).tolist())
    mesh._cache.clear(); gc.collect()
    if best[1] is not None:
        res.append((best[0], part, best[1], best[2]))
for g, part, t, at in sorted(res)[:12]:
    print(f'  buzzer vs {part:8s} {g:+7.2f} mm at {t:.3f} of the motion, near {at}')
