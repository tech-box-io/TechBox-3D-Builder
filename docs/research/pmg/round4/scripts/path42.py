"""Step 42: candidate paths for the module from the bench to over H4, the wires bent with it as the player bends Step 42's opening routes
(b_whole / b_from weights), counted: wire-against-wire crossings and wires into the module, Nano Board and plug, sampled along the way;
and, at the end, how far the bent shapes are from the shapes over H4 (the re-dress still to come)."""
import sys, json
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation as Ro, Slerp
sys.path.insert(0, 'tools')
import stepgen
from stepgen import _matrix
KIT = 'PMG Build Instructions'
S = json.load(open(KIT + '/steps.json'))
V = {v['name']: v for v in S['views']}
v42, v42c = V['Step 42'], V['Step 42c']
spec = json.load(open(KIT + '/materials.json'))
model = stepgen.Model(KIT + '/' + spec['source'], adjust=spec.get('adjust_mm') or {}, own_parts=spec.get('own_parts', {}),
                      extra_parts={i: (KIT + '/' + e['glb'], e['pose']) for i, e in spec.get('extra_parts', {}).items()})
MOD, NANO, PLUG = 'NAUO78', 'NANO', 'NAUO282'
radius = {w: d['radius'] for w, d in S['wires'].items()}
BENCH = v42['carry'][MOD]['pose']
HELD = v42c['carry'][MOD]['pose']
centre = model.inst[MOD].bounds.mean(0)
Mb, Mh = _matrix(BENCH), _matrix(HELD)
cb, ch = Mb[:3, :3] @ centre + Mb[:3, 3], Mh[:3, :3] @ centre + Mh[:3, 3]
routes = {w: S['routes'][no] for w, no in v42['wires'].items() if w != 'usb cable'}
held_routes = {w: S['routes'][no] for w, no in v42c['wires'].items() if w != 'usb cable'}


def ramp(t):
    t = np.clip(t, 0, 1); return t * t * (3 - 2 * t)


def bend(r, M):
    """Route r (drawn with the module at its b_ref) bent with the module at world matrix M (the player's skinned, full)."""
    p = np.asarray(r['pts'], float); s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    if r.get('a_whole') is not None or r.get('b_whole') is not None:
        lo, hi = max(r.get('a_whole') or 0, r.get('b_from') or 0), r.get('b_whole', s[-1])
        wb = ramp((s - lo) / max(1e-6, hi - lo))
    else:
        u = (s - r['b_from']) / max(1e-6, s[-1] - r['b_from']) if r.get('b_from') else s / s[-1]
        wb = ramp((u - 0.1) / 0.8)
    B = M @ np.linalg.inv(_matrix(r['b_ref']))
    q = p @ B[:3, :3].T + B[:3, 3]
    return p + wb[:, None] * (q - p)


def rs(p, step=0.6):
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    t = np.arange(0, s[-1], step); return np.stack([np.interp(t, s, p[:, c]) for c in range(3)], 1)


VERTS = {k: np.asarray(model.inst[k].vertices)[::4] for k in (MOD, NANO, PLUG)}


def count(M):
    lines = {w: rs(bend(r, M)) for w, r in routes.items()}
    cross = 0
    names = sorted(lines)
    trees = {w: cKDTree(lines[w][6:-6]) for w in names}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            d = trees[a].query(lines[b][6:-6])[0]
            if d.min() < 0.9 * (radius[a] + radius[b]):
                cross += 1
    # wires into the module's parts: points within the parts' boxes in the module frame (cheap proxy), but their own last 8 mm
    Xi = np.linalg.inv(M)
    into = 0
    for w, p in lines.items():
        q = p[:-14] @ Xi[:3, :3].T + Xi[:3, 3]
        for k, vv in VERTS.items():
            lo, hi = vv.min(0) + 0.5, vv.max(0) - 0.5
            if np.all((q > lo) & (q < hi), axis=1).any():
                into += 1
    return cross, into


def pose_mat(R, c):
    M = np.eye(4); M[:3, :3] = R; M[:3, 3] = c - R @ centre; return M


Rb, Rh = Mb[:3, :3], Mh[:3, :3]
up = lambda f: np.array([0, 1, 0]) * f


def path_slerp(n=24, lift=60.0):
    out = []
    for f in np.linspace(0, 1, n):
        R = Slerp([0, 1], Ro.from_matrix([Rb, Rh]))([f]).as_matrix()[0]
        c = cb + (ch - cb) * f + up(lift * np.sin(np.pi * f))
        out.append(pose_mat(R, c))
    return out


def path_two(first, n=24, lift=40.0):
    """Two turns one after the other: `first` (a rotation applied in world frame first), then the rest to the held turn."""
    R1 = first @ Rb
    out = []
    for f in np.linspace(0, 1, n):
        if f <= 0.5:
            g = f / 0.5; R = Slerp([0, 1], Ro.from_matrix([Rb, R1]))([g]).as_matrix()[0]
        else:
            g = (f - 0.5) / 0.5; R = Slerp([0, 1], Ro.from_matrix([R1, Rh]))([g]).as_matrix()[0]
        c = cb + (ch - cb) * f + up(lift * np.sin(np.pi * f))
        out.append(pose_mat(R, c))
    return out


Rx = lambda d: Ro.from_rotvec(np.radians(d) * np.array([1.0, 0, 0])).as_matrix()
Ry = lambda d: Ro.from_rotvec(np.radians(d) * np.array([0, 1.0, 0])).as_matrix()
Rz = lambda d: Ro.from_rotvec(np.radians(d) * np.array([0, 0, 1.0])).as_matrix()
print('check: Ry(-90)Rx(-90) Rb == Rh ?', np.allclose(Ry(-90) @ Rx(-90) @ Rb, Rh, atol=1e-3), ' Rz(-90)Ry(-90) Rb == Rh ?', np.allclose(Rz(-90) @ Ry(-90) @ Rb, Rh, atol=1e-3))
cands = {'slerp (now)': path_slerp(), 'tip USB end up, then face the back (Rx, Ry)': path_two(Rx(-90)),
         'spin USB end to the case, then stand up (Ry, Rz)': path_two(Ry(-90))}
for name, path in cands.items():
    res = [count(M) for M in path]
    print(f'{name:52s} crossings over the way {sum(r[0] for r in res):4d} (max at one moment {max(r[0] for r in res)}), into module parts {sum(r[1] for r in res)}')
print('---- between bundles only, and the re-dress at the end')
dev = lambda w: w.split()[0] if w.split()[0] in ('black', 'yellow', 'white', 'blue') else ('display' if '4-digit' in w else 'matrix')


def count2(M):
    lines = {w: rs(bend(r, M)) for w, r in routes.items()}
    names = sorted(lines); trees = {w: cKDTree(lines[w][6:-6]) for w in names}
    pairs = set()
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if dev(a) == dev(b):
                continue
            if trees[a].query(lines[b][6:-6])[0].min() < 0.9 * (radius[a] + radius[b]):
                pairs.add((dev(a), dev(b)))
    return pairs


def redress(M):
    tot = []
    for w, r in held_routes.items():
        a = rs(bend(routes[w], M), 1.0); b = rs(np.asarray(r['pts'], float), 1.0)
        n = 60
        sa = np.linspace(0, len(a) - 1, n).astype(int); sb = np.linspace(0, len(b) - 1, n).astype(int)
        tot.append(np.linalg.norm(a[sa] - b[sb], axis=1).mean())
    return np.mean(tot)


for name, path in cands.items():
    allp = {}
    for k, M in enumerate(path):
        for p in count2(M):
            allp.setdefault(p, []).append(k)
    print(f'{name:52s} bundle pairs touching: {len(allp)}', {f'{a}/{b}': len(ks) for (a, b), ks in sorted(allp.items())}, f' re-dress at the end: {redress(path[-1]):.1f} mm')
print('---- the plug along the spin-then-stand path')
G = json.load(open(KIT + '/cad-geometry.json'))
pe = np.asarray(G['usb']['plug_exit']); po = np.asarray(G['usb']['plug_out'])
path = path_two(Ry(-90), n=9)
for k, M in enumerate(path):
    print(k / 8, 'plug exit', (M[:3, :3] @ pe + M[:3, 3]).round(1).tolist(), 'out', (M[:3, :3] @ po).round(2).tolist(), 'module middle', (M[:3, :3] @ centre + M[:3, 3]).round(1).tolist())
print('A end bench middle', G['parts']['NAUO283']['middle'], 'A exit seat', G['usb']['a_exit'])
