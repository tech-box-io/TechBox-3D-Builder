"""F9's hook-and-swing (published Steps 45 - 46): where its feet are, and what it passes into on the way, at many moments.

usage: f9check.py [steps view whose scene to test against] -- poses from the published (docs/research/lac/round1/published_motions.md)
"""
import json, sys
from pathlib import Path
import numpy as np
import trimesh

ROOT = Path('/Users/lee-johnson/Desktop/Claude_Cadasio')
sys.path.insert(0, str(ROOT / 'tools'))
from stepgen import Model, apply_pose, turned, _matrix  # noqa: E402
from scipy.spatial.transform import Rotation, Slerp  # noqa: E402

kit = ROOT / 'LAC Build Instructions'
spec = json.load(open(kit / 'materials.json'))
model = Model(kit / spec['source'], adjust=spec.get('adjust_mm') or {}, own_parts=spec.get('own_parts', {}),
              extra_parts={i: (kit / e['glb'], e['pose']) for i, e in spec.get('extra_parts', {}).items()})
F9, F3 = 'NAUO45', 'NAUO2'
steps = json.load(open(kit / 'steps.json'))
views = {v['name']: v for v in steps['views']}
scene_view = sys.argv[1] if len(sys.argv) > 1 else 'Step 45'
V = views[scene_view]

P = [720.13, 887.54, 1355.78]
HOVER = [103.9, 35.3, 0.0]
BACK = [0.0, 35.3, 0.0]
TIPPED = turned([0, 0, -1], 25.79, P, t=[-0.45, 32.96, 0.0])
HOOKED = turned([0, 0, -1], 25.79, P)
ZERO = [0.0, 0.0, 0.0]

f9 = model.inst[F9]
print('F9 bounds', f9.bounds.round(2).tolist())
low = f9.vertices[f9.vertices[:, 1] < f9.bounds[0][1] + 6.0]
print('F9 feet region x range', low[:, 0].min().round(2), low[:, 0].max().round(2), 'z', low[:, 2].min().round(2), low[:, 2].max().round(2))
# F3's slots under F9: F3 vertices near F9's footprint
f3 = model.inst[F3]
near = f3.vertices[(abs(f3.vertices[:, 2] - 1355.8) < 3) & (f3.vertices[:, 0] > 690) & (f3.vertices[:, 0] < 725)]
print('F3 verts by F9 (x, y)', sorted(set((round(x, 2), round(y, 2)) for x, y, _ in near))[:40])


def mix(a, b, k):
    A, B = _matrix(a), _matrix(b)
    trn = lambda p: isinstance(p, dict) and p.get('r') and p['r'][3]
    c = np.asarray(((b if trn(b) else a).get('at') if (trn(a) or trn(b)) else None) or [0.0, 0.0, 0.0], float)
    R = Slerp([0, 1], Rotation.from_matrix([A[:3, :3], B[:3, :3]]))([k]).as_matrix()[0]
    M = np.eye(4)
    M[:3, :3] = R
    M[:3, 3] = (A[:3, :3] @ c + A[:3, 3]) * (1 - k) + (B[:3, :3] @ c + B[:3, 3]) * k - R @ c
    return M


samples, _ = trimesh.sample.sample_surface_even(f9, 30000, seed=1)
samples = np.vstack([samples, f9.vertices])
others = [i for i in V['visible'] if i != F9]
offs = V.get('offsets', {})
posed = {}
for i in others:
    m = model.inst.get(i)
    if m is None:
        continue
    o = offs.get(i)
    if o is not None:
        m = m.copy()
        m.apply_transform(_matrix(o))
    posed[i] = m


def check(M, label):
    pts = samples @ M[:3, :3].T + M[:3, 3]
    lo, hi = pts.min(0) - 0.5, pts.max(0) + 0.5
    worst = []
    for i, m in posed.items():
        b = m.bounds
        if np.any(b[1] < lo) or np.any(b[0] > hi):
            continue
        inbox = pts[np.all((pts >= b[0] - 0.01) & (pts <= b[1] + 0.01), axis=1)]
        if not len(inbox):
            continue
        if m.is_watertight:
            d = trimesh.proximity.signed_distance(m, inbox)
            dep = float(d.max())
        else:
            inside = m.contains(inbox)
            dep = float(trimesh.proximity.closest_point(m, inbox[inside])[1].max()) if inside.any() else 0.0
        if dep > 0.15:
            worst.append((i, round(dep, 2)))
    return worst


ways = {'Step 45': [HOVER, BACK, TIPPED, HOOKED], 'Step 46': [HOOKED, ZERO]}
for step, way in ways.items():
    for s in range(len(way) - 1):
        for k in np.linspace(0, 1, 11):
            M = mix(way[s], way[s + 1], k)
            w = check(M, f'{step} {s} {k:.1f}')
            if w:
                print(f'{step} stretch {s} at {k:.1f}: into', w)
    print(step, 'checked')
# where the feet are at the hooked pose
Mh = _matrix(HOOKED)
lowp = low @ Mh[:3, :3].T + Mh[:3, 3]
print('hooked: feet y range', lowp[:, 1].min().round(2), lowp[:, 1].max().round(2))
