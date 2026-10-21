"""Wires during a step's motion: the in-between frames that tools/wirecheck.py (views at rest) does not see.

    .venv.nosync/bin/python tools/motioncheck.py <kit folder> [--steps steps.json] "Step 26c" "Step 30c" ...   (no names: every view
                                                                                                               where a wire moves)

For each named view, at 19 moments of the motion that opens it: the moving parts along their ways, the riding parts through their
in-between places, each wire blended from its route in the view before to its route in this view (through any in-between routes),
as the player does (player.js: skinned, drawWires, throughPoses, paced); then every wire against every part on screen at that moment
(a point inside a part, or within 0.7 of the wire's radius of it, away from the wire's own ends) and against the other wires
(centre lines closer than 0.9 of their radii added). Adapted from the PMG session's docs/research/pmg/scripts/check_motion.py (19 Oct
2026), for any kit and every part. Approximate where the player is: poses are mixed linearly (turns by quaternion about the part's
middle), and a way's in-between poses are spaced by distance only.
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation, Slerp

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from stepgen import Model, _matrix  # noqa: E402

END = 5.0                                   # mm of a wire, at each end, allowed to touch the parts it is tied to


def ease(k):
    return 4 * k ** 3 if k < 0.5 else 1 - (-2 * k + 2) ** 3 / 2


def main(argv):
    args, steps_file, names = list(argv), 'steps.json', []
    kit = Path(args.pop(0))
    if args[:1] == ['--steps']:
        args.pop(0)
        steps_file = args.pop(0)
    trace = '--trace' in args
    names = [a for a in args if a != '--trace']
    steps = json.load(open(kit / steps_file))
    spec = json.load(open(kit / 'materials.json'))
    model = Model(kit / spec['source'], adjust=spec.get('adjust_mm') or {}, own_parts=spec.get('own_parts', {}),   # (the parts as the guide
                  extra_parts={i: (kit / e['glb'], e['pose']) for i, e in spec.get('extra_parts', {}).items()})  # has them: as wirecheck.py)
    routes, views = steps['routes'], steps['views']
    radius = {w: d['radius'] for w, d in steps['wires'].items()}

    def mix(a, b, k, part=None):
        """Part of the way from pose a to pose b as the player mixes them (player.js mixPose): the turn spread evenly about b's pivot (a's
        if b has none), that point moved in a straight line. A pose written as a turn about a far point (compose() without a pivot: the
        origin) then swings its part round it, as it does on screen (LAC round 1, 20 Oct 2026: caps 1.4 m off screen)."""
        A, B = _matrix(a), _matrix(b)
        turned = lambda p: isinstance(p, dict) and p.get('r') and p['r'][3]
        c = np.asarray(((b if turned(b) else a).get('at') if (turned(a) or turned(b)) else None) or [0.0, 0.0, 0.0], float)
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
            out += w * (((X[:3, :3] @ end + X[:3, 3]) - end) if ends_only else ((p @ X[:3, :3].T + X[:3, 3]) - p))
        return out

    def resample(p, n, span=None, start=0.0, lo=0.0, hi=None, s=None):
        s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))] if s is None else s
        at = np.clip(start + np.linspace(0, s[-1] if span is None else span, n), lo, s[-1] if hi is None else hi)
        return np.stack([np.interp(at, s, p[:, k]) for k in range(3)], 1)

    def drawn(r):                               # (distance along a route as drawn)
        return np.r_[0, np.cumsum(np.linalg.norm(np.diff(np.asarray(r['pts'], float), axis=0), axis=1))]

    def length(p):
        return float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum())

    def through(poses, k, part=None):
        n = len(poses) - 1
        s = min(n - 1, int(k * n))
        return mix(poses[s], poses[s + 1], k * n - s, part)

    all_names = [v['name'] for v in views]
    if not names:                               # every view whose wires change, or whose wired parts move
        names = [v['name'] for i, v in enumerate(views) if i and v.get('kind') in ('hover', 'done') and v.get('wires') and not v.get('cut')
                 and (v.get('wires') != views[i - 1].get('wires') or v.get('moving') or v.get('carry') != views[i - 1].get('carry'))]
    problems = 0
    for name in names:
        i = all_names.index(name)
        v, before = views[i], views[i - 1]
        if v.get('cut'):                        # (a view after a put-away opens without a glide: nothing moves into it)
            continue
        if v.get('reappear') and v.get('kind') == 'done':   # (`reappear`: fades out where it was and in where it ends; nothing moves)
            continue
        stops_of = lambda pid: ((v.get('path_stops') or {}).get(pid)) if v.get('paths') and pid in v['paths'] else v.get('stops')
        # (the moving parts move into the step's done view; in its opening view they stand where they hover)
        ways = {pid: (v.get('paths') or {}).get(pid) or v['path'] for pid in v.get('moving') or []} if v.get('kind') == 'done' else {}
        beats = max([len(stops_of(pid) or ways[pid]) - 1 for pid in ways] or [1])

        def paced(n, km):
            if beats > 1 and n == beats:
                b = min(beats - 1, int(km * beats))
                return (b + ease(km * beats - b)) / beats
            return ease(km)
        worst, touching, traced = {}, {}, {}
        for km in np.linspace(0.05, 0.95, 19):
            M = {pid: _matrix(pose) for pid, pose in (v.get('offsets') or {}).items()
                 if pid not in (v.get('carry') or {}) and pid not in ways}
            for pid, way in ways.items():
                M[pid] = along(way, stops_of(pid), km, pid)
            prior, carry = before.get('carry') or {}, v.get('carry') or {}

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
            for pid in carry:
                placed(pid)
            wire_via = v.get('wire_via') or {}
            we = paced(max([len(x) for x in wire_via.values()] or [0]) + 1, km)
            lines, src = {}, {}
            for w, no in (v.get('wires') or {}).items():
                was = (before.get('wires') or {}).get(w)
                if was is None or was == no:
                    p = skinned(routes[no], M)
                else:
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
                    elif ca is not None and cb is not None:      # (head by distance from the first end, tail from the last, as drawn)
                        sa, sb = drawn(ra), drawn(rb)
                        head, tail = max(ca, cb), max(sa[-1] - ca, sb[-1] - cb)
                        n1 = max(2, min(238, round(240 * head / max(1e-6, head + tail))))
                        two = lambda l, c, s: np.vstack([resample(l, n1, head, 0.0, 0.0, c, s), resample(l, 240 - n1, tail, s[-1] - tail, c, s[-1], s)])
                        pa, pb = two(a, ca, sa), two(b, cb, sb)
                    else:
                        span = max(length(a), length(b))
                        pa, pb = resample(a, 240, span), resample(b, 240, span)
                    p = pa + (pb - pa) * f
                    if trace:
                        src[w] = (pa, pb, leg, f)
                p = resample(p, max(60, int(length(p) / 0.4)))
                lines[w] = p
                s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
                inner = p[(s > END) & (s < s[-1] - END)]
                rad = radius[w]
                r = routes[no]
                for part in v.get('visible', []):
                    if part.startswith('STEM_') or part in (r.get('a'), r.get('b')):
                        continue
                    mesh = model.inst[part]
                    X = M.get(part)
                    q = inner if X is None else inner @ np.linalg.inv(X)[:3, :3].T + np.linalg.inv(X)[:3, 3]
                    lo, hi = mesh.bounds
                    near = np.all((q > lo - rad) & (q < hi + rad), axis=1)
                    if not near.any():
                        continue
                    cp, d, tri = mesh.nearest.on_surface(q[near])
                    inside = np.einsum('ij,ij->i', q[near] - cp, mesh.face_normals[tri]) < -0.3 * d   # (clearly behind the face: beside an edge the
                    # nearest face's normal can be square to the way out, and the sign is noise: the LAC session, 19 Oct 2026)
                    depth = np.where(inside, d + rad, rad - d)          # how far the tube's surface reaches into the part
                    bad = inside | (d < rad * 0.7)
                    if bad.any():
                        j = int(np.argmax(np.where(bad, depth, -9)))
                        key = (w, part)
                        if depth[j] > worst.get(key, (-9,))[0]:
                            worst[key] = (round(float(depth[j]), 2), round(float(km), 2), inner[near][j].round(1).tolist())
                            if trace and w in src:                  # (which bits of the two shapes were blended there)
                                pa, pb, leg, f = src[w]
                                pt = inner[near][j]
                                x = int(np.argmin(np.linalg.norm(pa + (pb - pa) * f - pt, axis=1)))
                                traced[key] = f'leg {leg} f {f:.2f}: sample {x}/{len(pa)} from {pa[x].round(1).tolist()} to {pb[x].round(1).tolist()}'
            ids = sorted(lines)
            for x, wa in enumerate(ids):
                tree = cKDTree(lines[wa][3:-3])
                for wb in ids[x + 1:]:
                    dd = tree.query(lines[wb][3:-3])[0]
                    lim = 0.9 * (radius[wa] + radius[wb])
                    if dd.min() < lim:
                        key = (wa, wb)
                        if dd.min() < touching.get(key, (9,))[0]:
                            touching[key] = (round(float(dd.min()), 2), round(float(km), 2), lines[wb][3:-3][int(np.argmin(dd))].round(1).tolist())
                            if trace:                       # (which bits of each wire's two shapes meet there)
                                pt, out = lines[wb][3:-3][int(np.argmin(dd))], []
                                for w in (wa, wb):
                                    if w in src:
                                        pa, pb, leg, f = src[w]
                                        x = int(np.argmin(np.linalg.norm(pa + (pb - pa) * f - pt, axis=1)))
                                        out.append(f'{w} leg {leg} f {f:.2f} sample {x}/{len(pa)}: {pa[x].round(1).tolist()} -> {pb[x].round(1).tolist()}')
                                traced[key] = '; '.join(out)
        for (w, part), (d, km, at) in sorted(worst.items(), key=lambda kv: -kv[1][0]):
            print(f'{name:9s} {w:13s} into {part:12s} {d:5.2f} mm at {km:.2f} of the motion, near {at}')
            if (w, part) in traced:
                print('          ', traced[(w, part)])
            problems += 1
        for (wa, wb), (d, km, at) in sorted(touching.items(), key=lambda kv: kv[1][0]):
            print(f'{name:9s} {wa:13s} and {wb:13s} centre lines {d:.2f} mm apart at {km:.2f}, near {at}')
            if (wa, wb) in traced:
                print('          ', traced[(wa, wb)])
            problems += 1
    print('checked', len(names), 'views in motion;', problems, 'problems')


if __name__ == '__main__':
    main(sys.argv[1:])
