"""Label placement search on a class picture of each view: every pixel is background, a large static part (board, wood), a small
static part, another wire, the moving part(s), the moving wire, a lead line, or a target spot; a label's cost is what it covers,
weighted, plus its leader's crossings, its distance, and its clashes with the other labels and eyes (at five window sizes)."""
import itertools
import json
import math
import sys

import numpy as np
from PIL import Image, ImageDraw

from render import read_model
from sim import NEAR, Cam, apply, layout, load, pose_matrix, skinned

SIZES = [(2000, 1017), (1440, 814), (1000, 634), (820, 528), (700, 634)]
SIDES = list(NEAR)
REACHES = [0.035, 0.05, 0.065, 0.08, 0.1]
BIG = {'NAUO1', 'NAUO2', 'NAUO10', 'NAUO42', 'NAUO43', 'NAUO44', 'NAUO45', 'F4', 'F5', 'F2', 'F6', 'NAUO141'}
W_CLASS = np.array([0.0, 0.03, 0.35, 0.45, 3.0, 2.0, 2.0, 6.0])   # bg, big, small, wire, moving part, moving wire, lead line, target
d, boxes, routes = load()
parts = read_model()
views = d['views']
import os
if os.environ.get('NEWCAMS'):
    from newcams import NEW
    for v in views:
        if v['name'] in NEW and v['kind'] == 'hover':
            v['camera'] = dict(NEW[v['name']])


def moving_of(i):
    v = views[i]
    nxt = views[i + 1] if i + 1 < len(views) else v
    mv = [p for p in v['visible'] if json.dumps(v['offsets'].get(p)) != json.dumps(nxt['offsets'].get(p))]
    mw = [w for w, no in (v.get('wires') or {}).items() if (nxt.get('wires') or {}).get(w) != no or routes[no].get('a') in mv or routes[no].get('b') in mv]
    return mv, mw


def class_map(i, cam):
    v = views[i]
    W, H = cam.W, cam.H
    img = Image.new('L', (W, H), 0)
    dr = ImageDraw.Draw(img)
    mv, mw = moving_of(i)
    items = []
    for pid in v['visible']:
        if pid not in parts:
            continue
        T, _ = parts[pid]
        P = apply(pose_matrix(v['offsets'].get(pid)), T.reshape(-1, 3)).reshape(-1, 3, 3)
        q = cam.project(P.reshape(-1, 3)).reshape(-1, 3, 2)
        z = np.linalg.norm(P.mean(1) - cam.pos, axis=1)
        cls = 4 if pid in mv else (1 if pid in BIG else 2)
        for k in range(len(z)):
            items.append((z[k], 0, q[k], cls))
    for wid, no in (v.get('wires') or {}).items():
        pts = skinned(routes[no], v['offsets'])
        q = cam.project(pts)
        z = np.linalg.norm((pts[1:] + pts[:-1]) / 2 - cam.pos, axis=1)
        wpx = max(2, int(2 * d['wires'][wid].get('radius', 0.6) / cam.mm_per_px))
        for k in range(len(q) - 1):
            items.append((z[k], wpx, (q[k], q[k + 1]), 5 if wid in mw else 3))
    items.sort(key=lambda t: -t[0])
    for z, wpx, q, cls in items:
        if wpx == 0:
            if np.abs(q).max() > 1e5:
                continue
            dr.polygon([tuple(p) for p in q], fill=cls)
        else:
            a, b = q
            if max(np.abs(a).max(), np.abs(b).max()) > 1e5:
                continue
            dr.line([tuple(a), tuple(b)], fill=cls, width=wpx)
    path_ = v.get('path') or []
    hops = [path_[0]] if any(isinstance(p, dict) for p in path_) else path_[:-1]
    for gd in v.get('guides') or []:
        poly = [apply(pose_matrix(w), gd['tip']) for w in hops] + [np.asarray(gd['mouth'], float)]
        q = cam.project(np.array(poly))
        dr.line([tuple(p) for p in q], fill=6, width=4)
    for it in (v.get('labels') or []) + (v.get('eye') or []):
        A = apply(pose_matrix(v['offsets'].get(it.get('id'))) if it.get('id') else np.eye(4), it['anchor'])
        x, y = cam.project(A)[0]
        dr.ellipse([x - 14, y - 14, x + 14, y + 14], fill=7)
    a = np.asarray(img)
    integ = []
    for c in range(len(W_CLASS)):
        m = (a == c).astype(np.int32)
        integ.append(np.pad(m.cumsum(0).cumsum(1), ((1, 0), (1, 0))))
    return a, integ, mv


def box_sum(integ, x0, y0, x1, y1, W, H):
    x0, y0, x1, y1 = int(max(0, x0)), int(max(0, y0)), int(min(W, x1)), int(min(H, y1))
    if x1 <= x0 or y1 <= y0:
        return np.zeros(len(integ))
    return np.array([I[y1, x1] - I[y0, x1] - I[y1, x0] + I[y0, x0] for I in integ], float)


def item_cost(it, a, integ, mv, W, H):
    why = []
    area = it['w'] * it['h']
    s = box_sum(integ, it['x'] - 2, it['y'], it['x'] + it['w'] + 2, it['y'] + it['h'], W, H)
    cover = s / max(1.0, area)
    c = 100 * float(cover @ W_CLASS)
    if cover[4] > 0.02: why.append(f'over moving part {cover[4]:.2f}')
    if cover[5] > 0.01: why.append(f'over moving wire {cover[5]:.2f}')
    if cover[7] > 0.0: why.append(f'over a target {cover[7]:.2f}')
    if cover[6] > 0.0: why.append(f'over a lead line {cover[6]:.3f}')
    x0, y0, ax, ay = it['leader']
    L = math.hypot(ax - x0, ay - y0)
    n = max(2, int(L / 4))
    hits = 0
    for k in range(n):
        t = k / n
        if (1 - t) * L < 16:                     # (its own end: the spot it names)
            continue
        x, y = int(x0 + (ax - x0) * t), int(y0 + (ay - y0) * t)
        if 0 <= x < W and 0 <= y < H:
            cl = a[y, x]
            if (cl == 4 and it.get('id') not in mv) or cl == 5:
                hits += 1
            elif cl == 7:
                hits += 2
    if hits:
        c += 6 * hits; why.append(f'leader across {hits}')
    if it.get('moved_down'):
        c += 800; why.append('under the caption')
    if it['clamped']:
        c += 150; why.append('clamped')
    f = L / W
    c += 300 * max(0.0, f - 0.09) + 300 * max(0.0, 0.045 - f) + 20 * f
    if it.get('asked') in ('near-above', 'near-below'):
        c += 2
    if it.get('reach') is not None and it.get('asked') in NEAR:
        c += 0.4 * abs(round((it['reach'] - 0.05) / 0.015))
    return c, why


def clash(a, b):
    ra = (a['x'] - 8, a['y'] - 8, a['x'] + a['w'] + 8, a['y'] + a['h'] + 8)
    rb = (b['x'], b['y'], b['x'] + b['w'], b['y'] + b['h'])
    c = 0.0
    if min(ra[2], rb[2]) > max(ra[0], rb[0]) and min(ra[3], rb[3]) > max(ra[1], rb[1]):
        c += 1500
    (x1, y1, x2, y2), (x3, y3, x4, y4) = a['leader'], b['leader']
    def o(ax, ay, bx, by, cx, cy):
        return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    if o(x3, y3, x4, y4, x1, y1) * o(x3, y3, x4, y4, x2, y2) < 0 and o(x1, y1, x2, y2, x3, y3) * o(x1, y1, x2, y2, x4, y4) < 0:
        c += 600
    for (p, q), r in (((a['leader'][:2], a['leader'][2:]), rb), ((b['leader'][:2], b['leader'][2:]), ra)):
        t = np.linspace(0.05, 0.95, 20)[:, None]
        pts = np.asarray(p) * (1 - t) + np.asarray(q) * t
        if ((pts[:, 0] > r[0]) & (pts[:, 0] < r[2]) & (pts[:, 1] > r[1]) & (pts[:, 1] < r[3])).sum() > 1:
            c += 400
    return c


CACHE = {}


def prepared(i):
    if i not in CACHE:
        CACHE[i] = []
        for W, H in SIZES:
            cam = Cam(views[i]['camera'], W, H)
            a, integ, mv = class_map(i, cam)
            CACHE[i].append((W, H, cam, a, integ, mv))
    return CACHE[i]


def evaluate(i, sel, verbose=False):
    v = views[i]
    total, notes = 0.0, []
    for W, H, cam, a, integ, mv in prepared(i):
        items, R, box, size = layout(v, cam, boxes, routes, overrides=sel)
        for it in items:
            c, why = item_cost(it, a, integ, mv, W, H)
            total += c
            if why:
                notes.append(f"{W}: {it.get('text', 'eye')} {', '.join(why)} ({c:.0f})")
        for p, q in itertools.combinations(items, 2):
            c = clash(p, q)
            total += c
            if c:
                notes.append(f"{W}: {p.get('text', 'eye')} / {q.get('text', 'eye')} clash {c:.0f}")
    return total, notes


def best(i, options=None):
    v = views[i]
    n = len(v.get('labels') or []) + len(v.get('eye') or [])
    opts = options or [[dict(side=s, reach=r) for s in SIDES for r in REACHES] for _ in range(n)]
    P = prepared(i)
    placed = {}
    unary = {}
    for k in range(n):
        for j, o in enumerate(opts[k]):
            tot = 0.0
            for si, (W, H, cam, a, integ, mv) in enumerate(P):
                items, R, box, size = layout(v, cam, boxes, routes, overrides={k: o})
                placed[(k, j, si)] = items[k]
                tot += item_cost(items[k], a, integ, mv, W, H)[0]
            unary[(k, j)] = tot
    pair = {}
    for p, q in itertools.combinations(range(n), 2):
        for jp in range(len(opts[p])):
            for jq in range(len(opts[q])):
                pair[(p, jp, q, jq)] = sum(clash(placed[(p, jp, si)], placed[(q, jq, si)]) for si in range(len(P)))
    bestc, bestj = math.inf, None
    for combo in itertools.product(*[range(len(o)) for o in opts]):
        c = sum(unary[(k, combo[k])] for k in range(n))
        if c >= bestc:
            continue
        for p, q in itertools.combinations(range(n), 2):
            c += pair[(p, combo[p], q, combo[q])]
            if c >= bestc:
                break
        if c < bestc:
            bestc, bestj = c, combo
    return bestc, {k: opts[k][j] for k, j in enumerate(bestj)}


def labelled():
    return [i for i, v in enumerate(views) if v['kind'] == 'hover' and (v.get('labels') or v.get('eye'))]


if __name__ == '__main__':
    want = sys.argv[1:] or None
    out = {}
    for i in labelled():
        v = views[i]
        if want and v['name'] not in want:
            continue
        now, _ = evaluate(i, None)
        c, sel = best(i)
        _, notes = evaluate(i, sel)
        names = [l['text'] for l in v.get('labels') or []] + ['eye'] * len(v.get('eye') or [])
        print(f"{v['name']}: now {now:.0f}, best {c:.0f}: " + '; '.join(f"{names[k]} {o['side']} {o['reach']}" for k, o in sel.items()), flush=True)
        for n_ in notes[:6]:
            print('      ', n_)
        out[v['name']] = dict(now=now, best=c, sel=[[names[k], o['side'], o['reach']] for k, o in sel.items()], notes=notes)
        CACHE.clear()
    json.dump(out, open('best2.json', 'w'), indent=1)
