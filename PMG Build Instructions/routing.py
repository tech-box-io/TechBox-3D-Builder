"""Jumper-wire routing for the PMG guide (Lee's first round, 19 Oct 2026: wires crossing one another and running into parts).

Two steps, for every set of wires the guide shows together:

1. ribbon(): each device's wires are laid side by side along one centre line, turned on the way (by the turn that best carries
   their order at the device's header into their order at the I/O module's), so that no wire of a bundle runs through another.
2. settle(): every wire is pushed off every other wire it comes within `gap` mm of, and out of every part on screen, the pushes
   spread smoothly along the wire (a displacement field, smoothed), the first and last few millimetres (straight out of the
   cap) kept where they are. A wire keeps its drawn shape where nothing is in its way.

The parts are taken as points sampled on their surfaces with their outward normals (measured once per part, in the part's own
seated frame; the wire is brought into that frame), which is quick and close enough here: check_wires.py measures the result
against the exact meshes.
"""
import numpy as np
import trimesh
from scipy.spatial import cKDTree

import wires as W
from stepgen import _matrix

RADIUS = 0.625                                                   # the jumper wires' radius (1.25 mm across)


def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def frames(P, n0=None):
    """Rotation-minimising frames (T, N, B) along a polyline (double reflection: Wang, Juttler, Zheng and Liu 2008)."""
    P = np.asarray(P, float)
    T = np.gradient(P, axis=0)
    T = unit(T)
    if n0 is None:
        n0 = np.cross(T[0], [0.0, 1.0, 0.0] if abs(T[0][1]) < 0.9 else [1.0, 0.0, 0.0])
    N = np.zeros_like(P)
    N[0] = unit(np.asarray(n0, float) - (np.asarray(n0, float) @ T[0]) * T[0])
    for i in range(len(P) - 1):
        v1 = P[i + 1] - P[i]
        c1 = v1 @ v1
        if c1 < 1e-12:
            N[i + 1] = N[i]
            continue
        rL = N[i] - (2 / c1) * (v1 @ N[i]) * v1
        tL = T[i] - (2 / c1) * (v1 @ T[i]) * v1
        v2 = T[i + 1] - tL
        c2 = v2 @ v2
        N[i + 1] = rL - (2 / c2) * (v2 @ rL) * v2 if c2 > 1e-12 else rL
        N[i + 1] = unit(N[i + 1] - (N[i + 1] @ T[i + 1]) * T[i + 1])
    return T, N, np.cross(T, N)


def _rot(phi):
    c, s = np.cos(phi), np.sin(phi)
    return np.array([[c, -s], [s, c]])


def ribbon(starts, ends, controls=(), lead=6.0, spacing=1.0, settle_mm=None, turn=None, twist=None, layer_mm=0.95):
    """The wires of one bundle, side by side: starts / ends are lists of (point, out) for each wire's two cap ends, out the way
    the wire leaves the cap. The bundle's centre line runs from the middle of the starts, straight out `lead` mm, through
    `controls`, to `lead` mm short of the middle of the ends. Each wire keeps its place in the bundle near each end and turns
    from the one to the other over the middle, or between the two points `twist` (the turn `turn` in radians, or the one that
    best carries the starts' layout into the ends'). Wires that change places in the bundle on the way (VCC to V, OUT to S, GND to
    G: the header's order is not the module's) pass over one another, `layer_mm` apart. Returns one centre line per wire, each
    starting at its start and ending at its end."""
    A = np.array([p for p, _ in starts], float)
    B = np.array([p for p, _ in ends], float)
    ad, bd = unit(np.mean([o for _, o in starts], axis=0)), unit(np.mean([o for _, o in ends], axis=0))
    a, b = A.mean(0), B.mean(0)
    la, lb = lead if isinstance(lead, (tuple, list)) else (lead, lead)              # (straight out of each end: one length, or two)
    pts = [a, a + ad * la, *[np.asarray(c, float) for c in controls], b + bd * lb, b]
    centre = W.resample(W.smooth(pts, start_dir=ad, end_dir=-bd, spacing=0.5), spacing)
    T, N, Bn = frames(centre)
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(centre, axis=0), axis=1))]
    L = s[-1]
    d = np.stack([(A - a) @ N[0], (A - a) @ Bn[0]], axis=1)                       # each wire's place at the start (in the frame)
    m = np.stack([(B - b) @ N[-1], (B - b) @ Bn[-1]], axis=1)                     # ... and at the end
    if turn is None:
        turn = float(np.arctan2(np.sum(d[:, 0] * m[:, 1] - d[:, 1] * m[:, 0]), np.sum(d[:, 0] * m[:, 0] + d[:, 1] * m[:, 1])))
    if twist is not None:
        s0, s1 = sorted(s[int(np.argmin(np.linalg.norm(centre - np.asarray(p, float), axis=1)))] for p in twist)
    else:
        edge = min(max(la, lb) + 2.0, L / 3) if settle_mm is None else settle_mm
        s0, s1 = edge, L - edge
    w = W.smootherstep(np.clip((s - s0) / max(s1 - s0, 1e-6), 0, 1))
    back = m @ _rot(-turn).T                                                       # the end layout turned back
    lay = np.zeros(len(A))
    if len(A) > 1:                                                                 # wires that change places pass over one another
        u = np.linalg.svd(d - d.mean(0), full_matrices=False)[2][0]
        lay = (np.argsort(np.argsort(back @ u)) - np.argsort(np.argsort(d @ u))).astype(float)
        across = np.array([-u[1], u[0]])
    out = []
    for k in range(len(A)):
        off = (1 - w)[:, None] * d[k] + w[:, None] * back[k]
        if lay[k]:
            off = off + np.sin(np.pi * w)[:, None] * across * lay[k] * layer_mm
        c, sn = np.cos(turn * w), np.sin(turn * w)
        off = np.stack([c * off[:, 0] - sn * off[:, 1], sn * off[:, 0] + c * off[:, 1]], axis=1)
        line = centre + off[:, :1] * N + off[:, 1:] * Bn
        u = (s / L)[:, None]
        line = line + (1 - u) * (A[k] - line[0]) + u * (B[k] - line[-1])        # (exactly on the ends: the frame's small errors)
        out.append(line)
    return out


class Surfaces:
    """Points on each part's surface with their outward normals, in its seated frame, measured once per part."""

    def __init__(self, model, spacing=0.45):
        self.model, self.spacing, self.cache = model, spacing, {}

    def of(self, part):
        if part not in self.cache:
            mesh = self.model.inst[part]
            n = int(min(400000, max(2000, 2.2 * mesh.area / self.spacing ** 2)))
            pts, faces = trimesh.sample.sample_surface(mesh, n, seed=7)
            self.cache[part] = (cKDTree(pts), pts, mesh.face_normals[faces], mesh.bounds)
        return self.cache[part]

    def placed(self, poses):
        """[(part, tree, pts, normals, seated bounds, the pose's matrix and its inverse)] for parts at their poses ({id: pose}, or
        a list of (id, pose) pairs, for a part in two places at once: a plug where it is held and where it goes in)."""
        out = []
        for part, pose in (poses.items() if isinstance(poses, dict) else poses):
            tree, pts, nrm, bounds = self.of(part)
            M = _matrix(pose)
            out.append((part, tree, pts, nrm, bounds, M, np.linalg.inv(M)))
        return out


def _ends_fixed(n, s, L, end_mm):
    """1 where a point may move, 0 within end_mm of either end (the wire straight out of its cap), ramped over 3 mm."""
    near = np.minimum(s, L - s)
    return np.clip((near - end_mm) / 3.0, 0, 1)


def settle(free, fixed=None, parts=(), skip=None, radii=None, gap=0.4, part_gap=0.3, end_mm=4.0, iters=400, spacing=1.0, report=None):
    """Wires `free` ({id: points}) pushed apart from one another and from `fixed` ({id: points}, which do not move), and out of
    `parts` (Surfaces.placed()); `skip` {wire: part ids it may touch} (its own caps). Returns {id: points}."""
    fixed = fixed or {}
    skip = skip or {}
    radii = radii or {}
    names = list(free)
    P0, mob, tang = {}, {}, {}
    for w in names:
        p = W.resample(np.asarray(free[w], float), spacing)
        s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
        P0[w], mob[w] = p, _ends_fixed(len(p), s, s[-1], end_mm)
    D = {w: np.zeros_like(P0[w]) for w in names}
    fx = [np.asarray(v, float) for v in fixed.values()]
    fx_pts = np.concatenate(fx) if fx else np.zeros((0, 3))
    fx_r = np.concatenate([np.full(len(v), radii.get(k, RADIUS)) for k, v in fixed.items()]) if fx else np.zeros(0)
    fx_own = np.concatenate([np.full(len(v), -1 - i) for i, v in enumerate(fixed.values())]) if fx else np.zeros(0, int)
    sizes = [len(P0[w]) for w in names]
    own = np.concatenate([np.full(n, i) for i, n in enumerate(sizes)] + [fx_own]).astype(int)
    r = np.concatenate([np.full(n, radii.get(w, RADIUS)) for w, n in zip(names, sizes)] + [fx_r])
    n_free = sum(sizes)
    movable = np.concatenate([mob[w] for w in names])
    skips = [skip.get(w, set()) for w in names]
    rmax = float(r.max()) if len(r) else RADIUS
    worst = None
    for it in range(iters):
        Pf = np.concatenate([P0[w] + D[w] for w in names])
        T = np.concatenate([unit(np.gradient(P0[w] + D[w], axis=0)) for w in names])
        allp = np.concatenate([Pf, fx_pts])
        F = np.zeros_like(Pf)
        worst_w = 0.0
        pairs = cKDTree(allp).query_pairs(2 * rmax + gap, output_type='ndarray')
        if len(pairs):
            i, j = pairs[:, 0], pairs[:, 1]
            keep = own[i] != own[j]
            i, j = i[keep], j[keep]
            d = allp[i] - allp[j]
            dist = np.linalg.norm(d, axis=1)
            need = r[i] + r[j] + gap
            bad = dist < need
            i, j, d, dist, need = i[bad], j[bad], d[bad], dist[bad], need[bad]
            both_fixed = (i >= n_free) & (j >= n_free)                     # (two held wires: nothing to do)
            i, j, d, dist, need = i[~both_fixed], j[~both_fixed], d[~both_fixed], dist[~both_fixed], need[~both_fixed]
            if len(i):
                tj = np.where((j < n_free)[:, None], T[np.minimum(j, n_free - 1)], 0.0)
                side = np.cross(T[np.minimum(i, n_free - 1)], tj)
                side = np.where(np.linalg.norm(side, axis=1, keepdims=True) > 1e-6, side, np.array([[0.0, 1.0, 0.0]]))
                direc = np.where((dist > 1e-6)[:, None], d / np.maximum(dist, 1e-9)[:, None], unit(side))
                deficit = need - dist
                worst_w = float(deficit.max())
                both = (j < n_free)
                share_i = np.where(both, 0.5, 1.0)
                np.add.at(F, i[i < n_free], (direc * (deficit * share_i)[:, None])[i < n_free])
                jj = both
                np.add.at(F, j[jj], -(direc * (deficit * 0.5)[:, None])[jj])
        worst_p = 0.0
        for part, tree, pts, nrm, (lo, hi), M, Minv in parts:
            q = Pf @ Minv[:3, :3].T + Minv[:3, 3]
            near = np.all((q > lo - 3.0) & (q < hi + 3.0), axis=1)
            if not near.any():
                continue
            idx_pts = np.nonzero(near)[0]
            owner = own[idx_pts]
            ok = np.array([part not in skips[o] for o in owner])
            idx_pts = idx_pts[ok]
            if not len(idx_pts):
                continue
            dist, k = tree.query(q[idx_pts])
            sgn = np.einsum('ij,ij->i', q[idx_pts] - pts[k], nrm[k])
            need = r[idx_pts] + part_gap
            bad = (sgn < need) & ((sgn < 0) | (dist < need + 0.6))
            if bad.any():
                push = (need[bad] - sgn[bad])[:, None] * nrm[k[bad]]
                free_here = movable[idx_pts[bad]] > 0                          # (the ends, straight out of their caps, stay)
                if free_here.any():
                    worst_p = max(worst_p, float((need[bad] - sgn[bad])[free_here].max()))
                np.add.at(F, idx_pts[bad], push @ M[:3, :3].T)
        F *= movable[:, None]
        worst = (worst_w, worst_p)
        if worst_w < 0.02 and worst_p < 0.02:
            break
        at = 0
        for w, n in zip(names, sizes):
            D[w] += 0.6 * F[at:at + n]
            for _ in range(3):                                     # spread the push along the wire
                Dm = D[w].copy()
                Dm[1:-1] += 0.5 * (0.5 * (D[w][:-2] + D[w][2:]) - D[w][1:-1])
                D[w] = Dm * mob[w][:, None]
            at += n
    if report is not None:
        report.append(dict(iterations=it + 1, wire_overlap=round(worst[0], 3) if worst else 0.0, part_depth=round(worst[1], 3) if worst else 0.0))
    return {w: W.resample(P0[w] + D[w], spacing) for w in names}
