"""Surface samples of the parts near the buzzer leads (seated meshes via parts_io), posed per view; and route checks."""
import json, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/tools')
from stepgen import apply_pose
import parts_io
import wires as W
KIT = parts_io.KIT
S = json.load(open(KIT + 'steps.json'))
VIEWS = {v['name']: v for v in S['views']}
ORDER = [v['name'] for v in S['views']]
RAD = {w: d['radius'] for w, d in S['wires'].items()}
BOX = (np.array([652.0, 884.0, 1226.0]), np.array([706.0, 948.0, 1346.0]))
B = json.load(open('bounds.json'))
_mesh = {}
def mesh(pid):
    if pid not in _mesh:
        _mesh.update(parts_io.seated([pid]))
    return _mesh[pid]
def samples(V, F, box, spacing=0.35, seed=1):
    T = V[F]
    lo, hi = T.min(1), T.max(1)
    keep = np.all((hi >= box[0]) & (lo <= box[1]), axis=1)
    T = T[keep]
    if not len(T): return np.zeros((0, 3)), np.zeros((0, 3))
    n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]); area = np.linalg.norm(n, axis=1) / 2
    nn = n / np.maximum(1e-12, 2 * area)[:, None]
    cnt = np.maximum(1, np.ceil(area / spacing ** 2)).astype(int)
    rng = np.random.default_rng(seed)
    idx = np.repeat(np.arange(len(T)), cnt)
    r1, r2 = rng.random(len(idx)), rng.random(len(idx))
    flip = r1 + r2 > 1; r1[flip], r2[flip] = 1 - r1[flip], 1 - r2[flip]
    P = T[idx, 0] + r1[:, None] * (T[idx, 1] - T[idx, 0]) + r2[:, None] * (T[idx, 2] - T[idx, 0])
    P = np.vstack([P, T.reshape(-1, 3)]); N = np.vstack([nn[idx], np.repeat(nn, 3, axis=0)])
    inb = np.all((P >= box[0] - 2) & (P <= box[1] + 2), axis=1)
    return P[inb], N[inb]
_samp = {}
def part_samples(pid):
    if pid not in _samp:
        V, F = mesh(pid)
        _samp[pid] = samples(V, F, BOX)
    return _samp[pid]
def near_parts(view, poses=None):
    v = VIEWS[view]; out = []
    for pid in v['visible']:
        if pid not in B: continue
        off = (poses or {}).get(pid, v.get('offsets', {}).get(pid))
        lo, hi = np.array(B[pid][0]), np.array(B[pid][1])
        c = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
        if off is not None: c = apply_pose(off, c)
        if np.all(c.max(0) >= BOX[0]) and np.all(c.min(0) <= BOX[1]):
            out.append((pid, off))
    return out
def dense(pts, step=0.25):
    p = np.asarray(pts, float); s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    t = np.arange(0, s[-1], step)
    return np.stack([np.interp(t, s, p[:, k]) for k in range(3)], 1), t, s[-1]
def check(view, pts, radius=0.625, skip=(), ends_mm=5.0, wires_skip=(), poses=None, extra_wires=None, report=6):
    """Smallest surface gaps of a route to each part / wire in a view (negative: into it)."""
    v = VIEWS[view]
    P, t, L = dense(pts)
    inner = (t > ends_mm) & (t < L - ends_mm)
    res = []
    for pid, off in near_parts(view, poses):
        if pid in skip: continue
        sp, sn = part_samples(pid)
        if not len(sp): continue
        if off is not None:
            sp2 = apply_pose(off, sp); sn2 = apply_pose(off, sn) - apply_pose(off, np.zeros((1, 3)))
        else:
            sp2, sn2 = sp, sn
        tree = cKDTree(sp2)
        dk, kk = tree.query(P, k=5, distance_upper_bound=8.0)
        d, k = dk[:, 0], kk[:, 0]
        ok = np.isfinite(d)
        if not ok.any(): continue
        g = np.full(len(P), 99.0)
        lo, hi = np.array(B[pid][0]), np.array(B[pid][1])
        c = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
        if off is not None: c = apply_pose(off, c)
        inbox = np.all((P > c.min(0)) & (P < c.max(0)), axis=1)
        inside = np.zeros(len(P), bool)
        votes = np.zeros(len(P))
        for m in range(5):
            okm = np.isfinite(dk[:, m])
            votes[okm] += np.where(np.einsum('ij,ij->i', P[okm] - sp2[kk[okm, m]], sn2[kk[okm, m]]) < 0, 1, -1)
        inside = ok & inbox & (votes >= 3)
        g[ok] = np.where(inside[ok], -d[ok], d[ok]) - radius
        g[~inner] = 99.0
        j = int(np.argmin(g))
        if g[j] < 3.0:
            res.append((round(float(g[j]), 2), pid, round(float(t[j]), 1), P[j].round(1).tolist()))
    W = dict((w, np.asarray(S['routes'][ri]['pts'], float)) for w, ri in v.get('wires', {}).items())
    if extra_wires: W.update(extra_wires)
    for w, q in W.items():
        if w in wires_skip: continue
        Q, _, _ = dense(q, 0.25)
        d, k = cKDTree(Q).query(P)
        g = d - radius - RAD.get(w, 0.625)
        g[~inner] = 99.0
        j = int(np.argmin(g))
        if g[j] < 3.0:
            res.append((round(float(g[j]), 2), 'wire ' + w, round(float(t[j]), 1), P[j].round(1).tolist()))
    return sorted(res)[:report]
