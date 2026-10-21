"""The wires' centre lines as the player draws them while a step plays (the blend of docs/research/pmg/scripts/check_caps.py, without
the model), and how they look: per wire and beat, the sharpest bend (degrees over 3 mm: a fold or a spike), how much longer the line
is than the longer of the two shapes it blends between (stretched into a spike), and how high it reaches above both. Usage:
    shapes42.py <kit> [view] [--steps file] [--samples N] [--wires a,b] [--save file.npz]"""
import sys, json
from pathlib import Path
import numpy as np
from scipy.spatial.transform import Rotation, Slerp
sys.path.insert(0, 'tools')
from stepgen import _matrix

ease = lambda k: 4 * k ** 3 if k < 0.5 else 1 - (-2 * k + 2) ** 3 / 2   # (the player's)


def ramp(s):
    t = np.clip((s - 0.1) / 0.8, 0, 1)
    return t * t * (3 - 2 * t)


def resample(p, n, span=None, start=0.0, lo=0.0, hi=None, s=None):
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))] if s is None else s
    at = np.clip(start + np.linspace(0, s[-1] if span is None else span, n), lo, s[-1] if hi is None else hi)
    return np.stack([np.interp(at, s, p[:, k]) for k in range(3)], 1)


drawn = lambda r: np.r_[0, np.cumsum(np.linalg.norm(np.diff(np.asarray(r['pts'], float), axis=0), axis=1))]
length = lambda p: float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum())


def skinned(r, M, ends_only=False):
    p = np.asarray(r['pts'], float)
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    u = s / (s[-1] or 1)
    if r.get('b_from'):
        u = (s - r['b_from']) / max(1e-6, s[-1] - r['b_from'])
    mv = lambda part, ref: None if not part else (M.get(part, np.eye(4)) @ np.linalg.inv(_matrix(ref)) if ref is not None else M.get(part, np.eye(4)))
    A, B = mv(r.get('a'), r.get('a_ref')), mv(r.get('b'), r.get('b_ref'))
    wb = ramp(u)[:, None] if r.get('b') else np.zeros((len(p), 1))
    if r.get('a_whole') is not None or r.get('b_whole') is not None:
        lo, hi = max(r.get('a_whole') or 0, r.get('b_from') or 0), r['b_whole'] if r.get('b_whole') is not None else s[-1]
        t = np.clip((s - lo) / max(1e-6, hi - lo), 0, 1)
        wb = (t * t * (3 - 2 * t))[:, None] if r.get('b') else np.zeros((len(p), 1))
    wa = 1 - wb if r.get('a') else np.zeros((len(p), 1))
    out = p.copy()
    for X, w, end in ((A, wa, p[0]), (B, wb, p[-1])):
        if X is not None:
            out += w * (((X[:3, :3] @ end + X[:3, 3]) - end) if ends_only else ((p @ X[:3, :3].T + X[:3, 3]) - p))
    return out


def lines_at(steps, name, km, centres):
    """{wire: (blended line, the two shapes, leg, f)} and the part placements at moment km (0..1) of the view's animation."""
    views, routes = steps['views'], steps['routes']
    names = [v['name'] for v in views]
    i = names.index(name)
    v, before = views[i], views[i - 1]

    def mix(a, b, k, part=None):
        A, B = _matrix(a), _matrix(b)
        c = centres.get(part, np.zeros(3))
        R = Slerp([0, 1], Rotation.from_matrix([A[:3, :3], B[:3, :3]]))([k]).as_matrix()[0]
        X = np.eye(4); X[:3, :3] = R
        X[:3, 3] = (A[:3, :3] @ c + A[:3, 3]) * (1 - k) + (B[:3, :3] @ c + B[:3, 3]) * k - R @ c
        return X

    def through(poses, k, part=None):
        n = len(poses) - 1
        s = min(n - 1, int(k * n))
        return mix(poses[s], poses[s + 1], k * n - s, part)
    beats = max([1] + [len(c.get('via', [])) + 1 for c in (v.get('carry') or {}).values()]) if v.get('ride_beats') else 1

    def paced(n, k):
        if beats > 1 and n == beats:
            b = min(beats - 1, int(k * beats))
            return (b + ease(k * beats - b)) / beats
        return ease(k)
    M, prior, carry = {}, before.get('carry') or {}, v.get('carry') or {}

    def placed(pid, depth=0):
        if pid in M:
            return M[pid]
        c = carry.get(pid)
        if c is None or depth > 8:
            return _matrix((v.get('offsets') or {}).get(pid))
        was = prior.get(pid, {}).get('pose') if prior.get(pid, {}).get('by') == c['by'] else None
        via = c.get('via', [])
        here = _matrix(c['pose']) if was is None or was == c['pose'] else through([was, *via, c['pose']], paced(len(via) + 1, km), pid)
        M[pid] = placed(c['by'], depth + 1) @ here
        return M[pid]
    for pid in v.get('visible', []):
        M[pid] = placed(pid)
    wire_via = v.get('wire_via') or {}
    we = paced(max([len(x) for x in wire_via.values()] or [0]) + 1, km)
    out = {}
    for w, no in (v.get('wires') or {}).items():
        was = (before.get('wires') or {}).get(w)
        if was is None or was == no:
            p = skinned(routes[no], M); out[w] = (p, p, p, 0, 0.0); continue
        way = [was, *(wire_via.get(w) or []), no]
        legs = len(way) - 1
        leg = min(legs - 1, int(we * legs))
        f = we * legs - leg
        ra, rb = routes[way[leg]], routes[way[leg + 1]]
        even = bool(ra.get('stretch') or rb.get('stretch'))
        a, b = skinned(ra, M, even), skinned(rb, M, even)
        ca, cb = ra.get('tail_from'), rb.get('tail_from')
        if even:
            pa, pb = resample(a, 240), resample(b, 240)
        elif ca is not None and cb is not None:
            sa, sb = drawn(ra), drawn(rb)
            head, tail = max(ca, cb), max(sa[-1] - ca, sb[-1] - cb)
            n1 = max(2, min(238, round(240 * head / max(1e-6, head + tail))))
            two = lambda l, c, s: np.vstack([resample(l, n1, head, 0.0, 0.0, c, s), resample(l, 240 - n1, tail, s[-1] - tail, c, s[-1], s)])
            pa, pb = two(a, ca, sa), two(b, cb, sb)
        else:
            span = max(length(a), length(b))
            pa, pb = resample(a, 240, span), resample(b, 240, span)
        out[w] = (pa + (pb - pa) * f, a, b, leg, f)
    return out, M, beats


def sharpest(p, step=3.0):
    p = resample(p, max(8, int(length(p) / step)))
    d = np.diff(p, axis=0); d /= np.linalg.norm(d, axis=1, keepdims=True) + 1e-9
    c = np.clip(np.einsum('ij,ij->i', d[:-1], d[1:]), -1, 1)
    j = int(np.argmax(np.degrees(np.arccos(c)))) if len(c) else 0
    return (float(np.degrees(np.arccos(c[j]))) if len(c) else 0.0), p[j + 1]


if __name__ == '__main__':
    args = sys.argv[1:]
    kit = Path(args.pop(0))
    name = args.pop(0) if args and not args[0].startswith('--') else 'Step 42c'
    n = int(args[args.index('--samples') + 1]) if '--samples' in args else 101
    only = args[args.index('--wires') + 1].split(',') if '--wires' in args else None
    save = args[args.index('--save') + 1] if '--save' in args else None
    steps = json.load(open(args[args.index('--steps') + 1] if '--steps' in args else kit / 'steps.json'))
    centres = {k: np.asarray(v['middle'], float) for k, v in json.load(open(kit / 'cad-geometry.json'))['parts'].items()}
    worst, keep = {}, {}
    for km in np.linspace(0, 1, n):
        L, M, beats = lines_at(steps, name, km, centres)
        b = min(beats - 1, int(km * beats))
        for w, (p, a, b_, leg, f) in L.items():
            if only and w not in only:
                continue
            ang, at = sharpest(p)
            stretch = length(p) / max(length(a), length(b_), 1e-6)
            high = p[:, 1].max() - max(a[:, 1].max(), b_[:, 1].max())
            r = worst.setdefault((w, b), dict(bend=(0, 0, None), stretch=(0, 0), high=(0, 0)))
            if ang > r['bend'][0]: r['bend'] = (round(ang), round(float(km), 3), at.round(1).tolist())
            if stretch > r['stretch'][0]: r['stretch'] = (round(stretch, 3), round(float(km), 3))
            if high > r['high'][0]: r['high'] = (round(float(high), 1), round(float(km), 3))
            if save: keep[f'{w}|{km:.3f}'] = p
    for (w, b), r in sorted(worst.items(), key=lambda x: (x[0][1], x[0][0])):
        if r['bend'][0] > 60 or r['stretch'][0] > 1.08 or r['high'][0] > 3:
            print(f'beat {b + 1}  {w:28s} sharpest {r["bend"][0]:3d} deg at {r["bend"][1]} {r["bend"][2]}   longer x{r["stretch"][0]} at {r["stretch"][1]}   '
                  f'above both shapes {r["high"][0]} mm at {r["high"][1]}')
    if save:
        np.savez_compressed(save, **keep)
