"""Wires during a step's motion (the in-between frames the static checks do not see): the moving parts along their paths, each
wire blended from its route in the view before to its route in this view as the player blends it (player.js drawWires: both
routes bent with the parts where they are at that moment, each point keeping its share of the length for a `stretch` route, then
mixed; through any in-between routes the view names, `wire_via`; a part riding through in-between places, `carry.via`, as the
player's throughPoses), measured against the case's wood. Approximate: poses are mixed linearly (turns by quaternion); a wire with
in-between routes is assumed to keep pace with the whole motion's ease, not stop by stop.

    .venv.nosync/bin/python docs/research/pmg/scripts/check_motion.py "Step 32c" "Step 33c" ...
"""
import json
import sys
from pathlib import Path

import numpy as np
import trimesh
from scipy.spatial.transform import Rotation, Slerp

ROOT = Path(__file__).resolve().parents[4]
KIT = ROOT / 'PMG Build Instructions'
sys.path.insert(0, str(ROOT / 'tools'))
from stepgen import Model, _matrix  # noqa: E402

steps = json.load(open(KIT / 'steps.json'))
routes, views = steps['routes'], steps['views']
WOOD = ['NAUO60', 'NAUO61', 'NAUO62', 'NAUO63', 'NAUO64', 'NAUO65', 'NAUO66', 'NAUO67', 'NAUO68', 'NAUO69', 'NAUO70', 'NAUO71', 'NAUO72',
        'NAUO73', 'NAUO74', 'NAUO75', 'NAUO77']
model = Model(KIT / 'pmg-guide.glb')


def ease(k):
    return 4 * k ** 3 if k < 0.5 else 1 - (-2 * k + 2) ** 3 / 2


CENTRE = {}


def mix(a, b, k, part=None):
    """Two poses mixed as the player's mixPose does: the part's middle moves straight, the part turns about it."""
    A, B = _matrix(a), _matrix(b)
    c = CENTRE.setdefault(part, model.inst[part].bounds.mean(0)) if part else np.zeros(3)
    R = Slerp([0, 1], Rotation.from_matrix([A[:3, :3], B[:3, :3]]))([k]).as_matrix()[0]
    M = np.eye(4)
    M[:3, :3] = R
    M[:3, 3] = (A[:3, :3] @ c + A[:3, 3]) * (1 - k) + (B[:3, :3] @ c + B[:3, 3]) * k - R @ c
    return M


def along(path, stops, t, part=None):
    stops = stops or list(range(len(path)))
    beats = len(stops) - 1
    b = min(beats - 1, int(t * beats))
    k = ease(t * beats - b)
    seg = path[stops[b]:stops[b + 1] + 1]
    if len(seg) == 2:
        return mix(seg[0], seg[1], k, part)
    L = [np.linalg.norm(_matrix(seg[i + 1])[:3, 3] - _matrix(seg[i])[:3, 3]) + 1e-6 for i in range(len(seg) - 1)]
    d, i = k * sum(L), 0
    while i < len(L) - 1 and d > L[i]:
        d -= L[i]
        i += 1
    return mix(seg[i], seg[i + 1], min(1, d / L[i]), part)


def ramp(s):
    t = np.clip((s - 0.1) / 0.8, 0, 1)
    return t * t * (3 - 2 * t)


def skinned(r, M, ends_only=False):
    """A route bent with the parts at its ends where they are (M), as the player's skinned(): each point follows the end parts
    in proportion (none of `b` before b_from mm); a `stretch` route, while it changes shape, only by its two ends' shifts."""
    p = np.asarray(r['pts'], float)
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    u = s / (s[-1] or 1)
    if r.get('b_from'):
        u = (s - r['b_from']) / max(1e-6, s[-1] - r['b_from'])

    def mv(part, ref):
        if not part:
            return None
        X = M.get(part, np.eye(4))
        return X @ np.linalg.inv(_matrix(ref)) if ref is not None else X
    A, B = mv(r.get('a'), r.get('a_ref')), mv(r.get('b'), r.get('b_ref'))
    wb = ramp(u)[:, None] if r.get('b') else np.zeros((len(p), 1))
    if r.get('a_whole') is not None or r.get('b_whole') is not None:   # (wholly with a up to a_whole mm, with b from b_whole: player.js)
        lo, hi = max(r.get('a_whole') or 0, r.get('b_from') or 0), r['b_whole'] if r.get('b_whole') is not None else s[-1]
        t = np.clip((s - lo) / max(1e-6, hi - lo), 0, 1)
        wb = (t * t * (3 - 2 * t))[:, None] if r.get('b') else np.zeros((len(p), 1))
    wa = 1 - wb if r.get('a') else np.zeros((len(p), 1))
    out = p.copy()
    for X, w, end in ((A, wa, p[0]), (B, wb, p[-1])):
        if X is None:
            continue
        if ends_only:
            out += w * ((X[:3, :3] @ end + X[:3, 3]) - end)
        else:
            out += w * ((p @ X[:3, :3].T + X[:3, 3]) - p)
    return out


def resample(p, n, span=None):
    """n points along p: by share of its length, or (span given) every span/(n-1) mm from its start, held at its end beyond it."""
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    at = np.linspace(0, s[-1] if span is None else span, n)
    return np.stack([np.interp(at, s, p[:, k]) for k in range(3)], 1)


def length(p):
    return float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum())


def through(poses, k, part=None):
    n = len(poses) - 1
    s = min(n - 1, int(k * n))
    return mix(poses[s], poses[s + 1], k * n - s, part)


names = [v['name'] for v in views]
for name in sys.argv[1:]:
    i = names.index(name)
    v, before = views[i], views[i - 1]
    if v.get('reappear') and v.get('kind') == 'done':   # (`reappear`: fades out where it was and in where it ends; nothing moves)
        print(f'{name}: fades out and in where it ends (reappear): nothing moves')
        continue
    worst, touching = {}, {}
    for t in np.linspace(0.05, 0.95, 19):
        lines = {}
        M = {pid: _matrix(pose) for pid, pose in (v.get('offsets') or {}).items()
             if pid not in (v.get('carry') or {}) and pid not in (v.get('moving') or [])}   # (riders and movers: placed below)
        for pid in v.get('moving') or []:
            path = (v.get('paths') or {}).get(pid) or v['path']
            stops = ((v.get('path_stops') or {}).get(pid)) if v.get('paths') and pid in v['paths'] else v.get('stops')
            M[pid] = along(path, stops, t, pid)
        k = ease(t)
        prior, carry = before.get('carry') or {}, v.get('carry') or {}

        def placed(pid, depth=0):                      # (a rider after what it rides on: caps on the module, on its carrier)
            if pid in M:
                return M[pid]
            c = carry.get(pid)
            if c is None or depth > 8:
                return _matrix((v.get('offsets') or {}).get(pid))
            was = prior.get(pid, {}).get('pose') if prior.get(pid, {}).get('by') == c['by'] else None
            here = _matrix(c['pose']) if was is None or was == c['pose'] else through([was, *c.get('via', []), c['pose']], k, pid)
            M[pid] = placed(c['by'], depth + 1) @ here
            return M[pid]
        for pid in carry:
            placed(pid)
        for w, no in (v.get('wires') or {}).items():
            was = (before.get('wires') or {}).get(w)
            if was is None or was == no:
                p = skinned(routes[no], M)
            else:
                way = [was, *((v.get('wire_via') or {}).get(w) or []), no]
                legs = len(way) - 1
                leg = min(legs - 1, int(k * legs))
                f = k * legs - leg
                ra, rb = routes[way[leg]], routes[way[leg + 1]]
                even = bool(ra.get('stretch') or rb.get('stretch'))
                a, b = skinned(ra, M, even), skinned(rb, M, even)
                if even:
                    pa, pb = resample(a, 200), resample(b, 200)
                else:
                    span = max(length(a), length(b))
                    pa, pb = resample(a, 200, span), resample(b, 200, span)
                p = pa + (pb - pa) * f
            lines[w] = p
            for part in WOOD:
                if part not in v.get('visible', []):
                    continue
                mesh = model.inst[part]
                X = M.get(part)
                q = p if X is None else p @ np.linalg.inv(X)[:3, :3].T + np.linalg.inv(X)[:3, 3]
                lo, hi = mesh.bounds
                near = np.all((q > lo - 1) & (q < hi + 1), axis=1)
                if not near.any():
                    continue
                d = trimesh.proximity.signed_distance(mesh, q[near]) + 0.625
                if d.max() > 0.2:
                    key = (w, part)
                    j = int(np.argmax(d))
                    if d[j] > worst.get(key, (0,))[0]:
                        worst[key] = (round(float(d[j]), 2), round(float(t), 2), p[near][j].round(1).tolist())
        from scipy.spatial import cKDTree
        ids = [w for w in lines if w != 'usb cable']
        for x, wa in enumerate(ids):
            pa = resample(lines[wa], 160)
            tree = cKDTree(pa[8:-8])
            for wb in ids[x + 1:]:
                pb = resample(lines[wb], 160)[8:-8]
                dd = tree.query(pb)[0]
                d = float(dd.min())
                if d < 1.15:
                    key = (wa, wb)
                    if d < touching.get(key, (9,))[0]:
                        touching[key] = (round(d, 2), round(float(t), 2), pb[int(np.argmin(dd))].round(1).tolist())
    print(name, 'deepest wire in wood during the motion (mm, at t):', dict(sorted(worst.items(), key=lambda kv: -kv[1][0])[:12]) or 'none')
    print(name, 'wires through one another (centre lines closer than 1.15 mm, at t):', dict(sorted(touching.items(), key=lambda kv: kv[1][0])[:12]) or 'none')
