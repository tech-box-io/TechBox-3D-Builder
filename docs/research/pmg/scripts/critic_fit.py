"""Critic's spot checks on pmg.glb (memory-mapped, a few meshes only; the whole file is never loaded).

1. The built module's D4 pins from the MRA's measured pins, and the cap NAUO97 (G4) over them.
2. The published way up of the I/O module (NAUO78 turned 180 deg about the X-parallel line through y0, z0, as cadasio_map /
   cad_wire_paths found it): does it still fit the case? Counts module vertices inside the wood (trimesh on single plates),
   for the STEP's pose and for the turned one.
3. The published bench matrix (NAUO44 turned 180 deg about X through y 923.8, z 1420.3) written as a pose of the built NAUO81.
"""
import json, sys
import numpy as np
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from pmglib import Glb
import trimesh

ROOT = '/Users/lee-johnson/Desktop/Claude_Cadasio'
g = Glb(ROOT + '/PMG Build Instructions/pmg.glb')

def mesh_world(top, skip_under=None, names=None):
    """[(name, vertices mm (n,3), faces)] of the meshes under a top-level instance."""
    out = []
    skip_nodes = set()
    if skip_under:
        # node indices under the named inner node of this instance
        def mark(i):
            skip_nodes.add(i)
            for c in g.nodes[i].get('children', []):
                mark(c)
        def find(i):
            if g.nodes[i].get('name') == skip_under:
                mark(i); return True
            return any(find(c) for c in g.nodes[i].get('children', []))
        find(g.top[top])
    for i, name, m, W in g.mesh_nodes(top):
        mname = g.meshes[m].get('name') or name
        if i in skip_nodes or (names and not any(mname and mname.startswith(n) for n in names)):
            continue
        for pr in g.meshes[m]['primitives']:
            P = g.accessor(pr['attributes']['POSITION']).astype(float)
            F = g.accessor(pr['indices']).reshape(-1, 3) if 'indices' in pr else np.arange(len(P)).reshape(-1, 3)
            V = (P @ W[:3, :3].T + W[:3, 3]) * 1000.0
            mname = g.meshes[m].get('name') or name
            out.append((mname, V, np.asarray(F, dtype=np.int64)))
    return out

# ---- 1. pins and a cap
pins = json.load(open(ROOT + '/docs/research/mra/cad_pins.json'))['shield']
for row in ('D4', 'D7', 'D13'):
    for col in ('G', 'V', 'S'):
        x, y, z = pins['pins'][row][col]
        print(f'  {row} {col}: built ({y + 490.546:.2f}, {1077.982 - z:.2f}, {1360.501 - x:.2f})  bench ({x + 603.545:.2f}, {y + 774.168:.2f}, {z + 1153.856:.2f})')
cap = mesh_world('NAUO97')
V = np.vstack([v for _, v, _ in cap])
print('cap NAUO97 box', V.min(0).round(2), V.max(0).round(2), 'centre', ((V.min(0) + V.max(0)) / 2).round(2))

# ---- 2. the module turned the published way up
y0, z0 = 931.55, 1290.535          # from the box centres: NAUO78 (605.78, 932.5, 1290.47) and Cadasio's -2 (605.8, 930.6, 1290.6)
def flip(V):
    W = V.copy(); W[:, 1] = 2 * y0 - V[:, 1]; W[:, 2] = 2 * z0 - V[:, 2]; return W
mod = mesh_world('NAUO78', skip_under='NAUO301')
modV = np.vstack([v for _, v, _ in mod])
print('module (no plain Nano):', len(mod), 'meshes', len(modV), 'vertices; box', modV.min(0).round(2), modV.max(0).round(2))
board = [v for n, v, _ in mod if n and n.startswith('Shield_Arduino')]
B = np.vstack(board)
print('board STEP box', B.min(0).round(2), B.max(0).round(2), '| turned box', flip(B).min(0).round(2), flip(B).max(0).round(2))
jack = [v for n, v, _ in mod if n and 'PJ-002AH_Body' in n]
if jack:
    J = np.vstack(jack); print('jack STEP box', J.min(0).round(2), J.max(0).round(2), '| turned', flip(J).min(0).round(2), flip(J).max(0).round(2))
WOOD = {'H4': 'NAUO73', 'H5': 'NAUO67', 'H10': 'NAUO64', 'H13': 'NAUO75', 'H11': 'NAUO62', 'H12': 'NAUO77', 'H2': 'NAUO65', 'H3': 'NAUO66', 'H14': 'NAUO74'}
for code, nid in WOOD.items():
    parts = mesh_world(nid)
    tm = trimesh.Trimesh(np.vstack([v for _, v, _ in parts]), np.vstack([f + sum(len(p[1]) for p in parts[:k]) for k, (_, _, f) in enumerate(parts)]), process=True)
    lo, hi = tm.bounds[0] - 2, tm.bounds[1] + 2
    res = []
    for label, pts in (('STEP', modV), ('turned', flip(modV))):
        near = pts[np.all((pts > lo) & (pts < hi), axis=1)]
        inside = near[tm.contains(near)] if len(near) else near
        if len(inside):
            # how deep: distance to the plate surface
            d = np.abs(trimesh.proximity.signed_distance(tm, inside))
            res.append(f'{label}: {len(inside)} inside, deepest {d.max():.2f} mm, box {inside.min(0).round(1)}..{inside.max(0).round(1)}')
        else:
            res.append(f'{label}: 0 inside')
    print(code, nid, 'watertight' if tm.is_watertight else 'NOT watertight', '|', ' | '.join(res))
H5 = np.vstack([v for _, v, _ in mesh_world('NAUO67')])
sel = H5[(H5[:, 0] > 594) & (H5[:, 2] > 1255) & (H5[:, 2] < 1326)]
print('H5 tongue vertices x>594: y', sel[:, 1].min().round(2), '..', sel[:, 1].max().round(2), ' x', sel[:, 0].min().round(2), '..', sel[:, 0].max().round(2))

# ---- 3. the published bench matrix as a pose of the built NAUO81
def rot(axis, deg):
    a = np.asarray(axis, float); a /= np.linalg.norm(a); t = np.radians(deg)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * K @ K
def M(R, t):
    m = np.eye(4); m[:3, :3] = R; m[:3, 3] = t; return m
at = np.array([532.477, 955.89, 1289.103])
R1 = rot([-0.93969, 0.34202, 0], 180.0)
P1 = M(R1, at - R1 @ at + np.array([114.717, -32.075, 116.483]))          # built NAUO81 -> NAUO44 (reuse_poses.json)
c = np.array([0, 923.8, 1420.3]); R2 = np.diag([1.0, -1, -1])
P2 = M(R2, c - R2 @ c)                                                         # NAUO44 -> Cadasio's LED Matrix-1 (cad_wire_paths)
P = P2 @ P1
R = P[:3, :3]
ang = np.degrees(np.arccos(np.clip((np.trace(R) - 1) / 2, -1, 1)))
w, v = np.linalg.eig(R); ax = np.real(v[:, np.argmin(np.abs(w - 1))]); ax /= np.linalg.norm(ax)
# sign of the axis so that rot(ax, ang) == R
if np.abs(rot(ax, ang) - R).max() > 1e-6: ax = -ax
t = P[:3, 3] - (at - R @ at)
print('published bench matrix from built NAUO81: turned(%s, %.2f, at=%s, t=%s)' % (ax.round(5).tolist(), ang, at.tolist(), t.round(3).tolist()),
      ' check', np.abs(rot(ax, ang) - R).max().round(9))
mat = mesh_world('NAUO81', names=['PCB'])
Pv = np.vstack([v for _, v, _ in mat])
Q = Pv @ R.T + P[:3, 3]
print('built PCB centre', ((Pv.min(0) + Pv.max(0)) / 2).round(1), '-> published bench PCB centre', ((Q.min(0) + Q.max(0)) / 2).round(1), '(Cadasio LED Matrix-1 whole-part centre 649.4, 923.8, 1435.0)')

# whole matrix: the published bench pose against Cadasio's LED Matrix-1 box (centre 649.4, 923.8, 1435.0; size 17.7, 32.0, 131.9)
allm = np.vstack([v for _, v, _ in mesh_world('NAUO81')])
Q = allm @ R.T + P[:3, 3]
print('whole matrix, published bench pose: box centre', ((Q.min(0) + Q.max(0)) / 2).round(1), 'size', (Q.max(0) - Q.min(0)).round(1))
E = np.vstack([v for _, v, _ in mesh_world('NAUO44')])
print('NAUO44 as in the STEP: box centre', ((E.min(0) + E.max(0)) / 2).round(1), 'size', (E.max(0) - E.min(0)).round(1))
