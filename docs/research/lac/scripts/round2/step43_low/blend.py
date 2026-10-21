"""The player's blending of the two buzzer leads through Step 43 (as tools/motioncheck.py does it), checked against a precomputed
clearance field (field43.npz: the parts and the other wires, static in Step 43). Fast: for searching shapes."""
import numpy as np
from scipy.spatial.transform import Rotation, Slerp
from scipy.ndimage import map_coordinates
from common import *
from stepgen import _matrix

F = np.load(SCR / 'field43.npz')
DP, DW, WH, FLO, FP, WN = F['dpart'], F['dwire'], F['which'], F['lo'], float(F['pitch']), list(F['wnames'])
END = 5.0


def ease(k):
    return 4 * k ** 3 if k < 0.5 else 1 - (-2 * k + 2) ** 3 / 2


def mix(a, b, k):
    A, B = _matrix(a), _matrix(b)
    turned = lambda p: isinstance(p, dict) and p.get('r') and p['r'][3]
    c = np.asarray(((b if turned(b) else a).get('at') if (turned(a) or turned(b)) else None) or [0.0, 0.0, 0.0], float)
    R = Slerp([0, 1], Rotation.from_matrix([A[:3, :3], B[:3, :3]]))([k]).as_matrix()[0]
    M = np.eye(4)
    M[:3, :3] = R
    M[:3, 3] = (A[:3, :3] @ c + A[:3, 3]) * (1 - k) + (B[:3, :3] @ c + B[:3, 3]) * k - R @ c
    return M


def shift(p):
    return np.asarray(p if isinstance(p, (list, tuple)) else (p or {}).get('t', [0.0, 0.0, 0.0]), float)


def gap(a, b):
    turn = (Rotation.from_matrix(_matrix(a)[:3, :3]).inv() * Rotation.from_matrix(_matrix(b)[:3, :3])).magnitude()
    return float(np.linalg.norm(shift(b) - shift(a)) + np.degrees(turn) * 0.5)


def along(path, stops, t):
    stops = stops or list(range(len(path)))
    beats = len(stops) - 1
    b = min(beats - 1, int(t * beats))
    k = ease(t * beats - b)
    seg = path[stops[b]:stops[b + 1] + 1]
    if len(seg) == 2:
        return mix(seg[0], seg[1], k)
    L = [gap(seg[i], seg[i + 1]) + 1e-6 for i in range(len(seg) - 1)]
    d, i = k * sum(L), 0
    while i < len(L) - 1 and d > L[i]:
        d -= L[i]
        i += 1
    return mix(seg[i], seg[i + 1], min(1, d / L[i]))


def ramp(s):
    t = np.clip((s - 0.1) / 0.8, 0, 1)
    return t * t * (3 - 2 * t)


def skinned(r, M, ends_only=False):
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
    if r.get('a_whole') is not None or r.get('b_whole') is not None:
        lo, hi = max(r.get('a_whole') or 0, r.get('b_from') or 0), r['b_whole'] if r.get('b_whole') is not None else s[-1]
        t = np.clip((s - lo) / max(1e-6, hi - lo), 0, 1)
        wb = (t * t * (3 - 2 * t))[:, None] if r.get('b') else np.zeros((len(p), 1))
    wa = 1 - wb if r.get('a') else np.zeros((len(p), 1))
    out = p.copy()
    for X, w, end in ((A, wa, p[0]), (B, wb, p[-1])):
        if X is None:
            continue
        out += w * (((X[:3, :3] @ end + X[:3, 3]) - end) if ends_only else ((p @ X[:3, :3].T + X[:3, 3]) - p))
    return out


def resample(p, n, span=None, start=0.0, lo=0.0, hi=None, s=None):
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))] if s is None else s
    at = np.clip(start + np.linspace(0, s[-1] if span is None else span, n), lo, s[-1] if hi is None else hi)
    return np.stack([np.interp(at, s, p[:, k]) for k in range(3)], 1)


def drawn(r):
    return np.r_[0, np.cumsum(np.linalg.norm(np.diff(np.asarray(r['pts'], float), axis=0), axis=1))]


def length(p):
    return float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum())


def blended(way, f, M, n=240):
    """A lead part of the way (f, in its leg) between two routes of `way` (as the player's drawWires)."""
    ra, rb = way
    even = bool(ra.get('stretch') or rb.get('stretch'))
    a, b = skinned(ra, M, even), skinned(rb, M, even)
    ca, cb = ra.get('tail_from'), rb.get('tail_from')
    if even:
        pa, pb = resample(a, n), resample(b, n)
    elif ca is not None and cb is not None:
        sa, sb = drawn(ra), drawn(rb)
        head, tail = max(ca, cb), max(sa[-1] - ca, sb[-1] - cb)
        n1 = max(2, min(n - 2, round(n * head / max(1e-6, head + tail))))
        two = lambda l, c, s: np.vstack([resample(l, n1, head, 0.0, 0.0, c, s), resample(l, n - n1, tail, s[-1] - tail, c, s[-1], s)])
        pa, pb = two(a, ca, sa), two(b, cb, sb)
    else:
        span = max(length(a), length(b))
        pa, pb = resample(a, n, span), resample(b, n, span)
    return pa + (pb - pa) * f


def lookup(P):
    idx = ((np.asarray(P) - FLO) / FP).T
    dp = map_coordinates(DP, idx, order=1, mode='nearest')
    dw = map_coordinates(DW, idx, order=1, mode='nearest')
    wi = map_coordinates(WH, idx, order=0, mode='nearest')
    return dp, dw, wi


def frames(path, stops, routes, moments=99, lying=None):
    """routes: {colour: [S0, S1, ..., S_last]} (S0 the route before the step). Yields (km, {colour: line})."""
    beats = len(stops or path) - 1
    for km in np.linspace(0.0, 1.0, moments + 2)[1:-1]:
        M = {BUZZER: along(path, stops, km)}
        if beats > 1:
            b = min(beats - 1, int(km * beats))
            we = (b + ease(km * beats - b)) / beats
        else:
            we = ease(km)
        out = {}
        for c, way in routes.items():
            legs = len(way) - 1
            leg = min(legs - 1, int(we * legs))
            f = we * legs - leg
            p = blended((way[leg], way[leg + 1]), f, M)
            out[c] = resample(p, max(60, int(length(p) / 0.4)))
        yield km, out, M


def check(path, stops, routes, moments=99, verbose=False, forced=()):
    """The worst gaps (mm, surface to surface) of each lead to the parts, to the other wires (by name), and to each other."""
    worst = {}
    for km, lines, M in frames(path, stops, routes, moments):
        for c, p in lines.items():
            s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
            inner = p[(s > END) & (s < s[-1] - END)]
            dp, dw, wi = lookup(inner)
            gp = dp - 0.625
            k = int(np.argmin(gp))
            key = (c, 'parts')
            if gp[k] < worst.get(key, (9e9,))[0]:
                worst[key] = (round(float(gp[k]), 2), round(float(km), 3), inner[k].round(1).tolist())
            gw = dw - 0.625
            for w in np.unique(wi[gw < 2.0]):
                sel = (wi == w)
                j = np.where(sel)[0][int(np.argmin(gw[sel]))]
                key = (c, WN[int(w)])
                if gw[j] < worst.get(key, (9e9,))[0]:
                    worst[key] = (round(float(gw[j]), 2), round(float(km), 3), inner[j].round(1).tolist())
        from scipy.spatial import cKDTree
        for c, p in lines.items():                          # a lead folded on itself (bits far apart along it, close in space)
            s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
            t = cKDTree(p)
            best = 9e9
            for i, j in t.query_pairs(1.25):
                if abs(s[i] - s[j]) > 4.0:
                    best = min(best, float(np.linalg.norm(p[i] - p[j])))
            key = (c, 'fold')
            if best < 9e9 and best - 1.25 < worst.get(key, (9e9,))[0]:
                worst[key] = (round(best - 1.25, 2), round(float(km), 3), [])
        if len(lines) == 2:
            a, b = lines['red'][3:-3], lines['black'][3:-3]
            d = cKDTree(a).query(b)[0]
            j = int(np.argmin(d))
            key = ('red', 'black')
            if d[j] - 1.25 < worst.get(key, (9e9,))[0]:
                worst[key] = (round(float(d[j]) - 1.25, 2), round(float(km), 3), b[j].round(1).tolist())
    return worst


def score(worst, forced=()):
    """The smallest gap over everything not forced."""
    return min([v[0] for k, v in worst.items() if (k[0], k[1]) not in forced and k[1] not in forced] or [9.0])
