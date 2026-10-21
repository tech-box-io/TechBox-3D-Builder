"""A copy of the player's label layout (player/js/player.js layoutCallouts, screenRect, skinned; core.js cameraPose) in Python,
for the LAC's steps.json, so that every labelled view can be laid out at several window sizes without a browser."""
import json
import math
import struct
import sys
from pathlib import Path

import numpy as np
from PIL import ImageFont

ROOT = Path('/Users/lee-johnson/Desktop/Claude_Cadasio')
KIT = ROOT / 'LAC Build Instructions'
BOLD = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 28)
REG = '/System/Library/Fonts/Supplemental/Arial.ttf'
_fonts = {}


def font(path, size):
    key = (path, round(size * 4))
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def text_width(text, size, bold=True):
    return font('/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold else REG, size).getlength(text)


def load(steps='steps.json'):
    d = json.load(open(KIT / steps))
    f = open(KIT / 'model.glb', 'rb')
    f.read(12)
    n, _ = struct.unpack('<II', f.read(8))
    g = json.loads(f.read(n))
    boxes = {}

    def mat(node):
        if 'matrix' in node:
            return np.array(node['matrix'], float).reshape(4, 4).T
        M = np.eye(4)
        if 'scale' in node:
            M = np.diag([*node['scale'], 1.0]) @ M
        if 'rotation' in node:
            x, y, z, w = node['rotation']
            R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                          [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                          [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
            M4 = np.eye(4); M4[:3, :3] = R
            M = M4 @ M
        if 'translation' in node:
            T = np.eye(4); T[:3, 3] = node['translation']
            M = T @ M
        return M

    def walk(i, M, out):
        node = g['nodes'][i]
        M = M @ mat(node)
        if 'mesh' in node:
            for p in g['meshes'][node['mesh']]['primitives']:
                a = g['accessors'][p['attributes']['POSITION']]
                lo, hi = np.array(a['min'], float), np.array(a['max'], float)
                if a.get('normalized'):
                    s = {5120: 127, 5121: 255, 5122: 32767, 5123: 65535}.get(a['componentType'], 1)
                    lo, hi = lo / s, hi / s
                c = np.array([[x, y, z, 1.0] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
                w = (M @ c.T).T[:, :3]
                out.append(w)
        for c in node.get('children', []):
            walk(c, M, out)

    root = g['nodes'][g['scenes'][0]['nodes'][0]]
    for c in root.get('children', []):
        out = []
        walk(c, mat(root), out)
        if out:
            pts = np.vstack(out)
            boxes[g['nodes'][c]['name']] = (pts.min(0), pts.max(0))
    routes = []
    for r in d['routes']:
        pts = np.asarray(r['pts'], float)
        s = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
        L = s[-1] or 1.0
        routes.append(dict(r, P=pts, s=s / L, len=L))
    return d, boxes, routes


def pose_matrix(pose):
    M = np.eye(4)
    if not pose:
        return M
    if isinstance(pose, list):
        M[:3, 3] = pose
        return M
    t, r, at = np.asarray(pose.get('t', [0, 0, 0]), float), pose.get('r'), np.asarray(pose.get('at', [0, 0, 0]), float)
    if not r or not r[3]:
        M[:3, 3] = t
        return M
    ax = np.asarray(r[:3], float); ax /= np.linalg.norm(ax)
    a = math.radians(r[3])
    K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    R = np.eye(3) + math.sin(a) * K + (1 - math.cos(a)) * K @ K
    M[:3, :3] = R
    M[:3, 3] = t + at - R @ at
    return M


def apply(M, p):
    p = np.asarray(p, float)
    return (M[:3, :3] @ p.T).T + M[:3, 3] if p.ndim == 2 else M[:3, :3] @ p + M[:3, 3]


def ramp(s):
    t = np.clip((s - 0.1) / 0.8, 0, 1)
    return t * t * (3 - 2 * t)


def skinned(route, poses):
    def end_move(part, ref):
        if not part or not (poses.get(part) or ref):
            return None
        M = pose_matrix(poses.get(part))
        return M @ np.linalg.inv(pose_matrix(ref)) if ref else M
    A, B = end_move(route.get('a'), route.get('a_ref')), end_move(route.get('b'), route.get('b_ref'))
    P = route['P']
    if A is None and B is None:
        return P
    if route.get('b_from'):
        u = (route['s'] * route['len'] - route['b_from']) / max(1e-6, route['len'] - route['b_from'])
    else:
        u = route['s']
    wb = ramp(u) if route.get('b') else np.zeros(len(P))
    wa = 1 - wb if route.get('a') else np.zeros(len(P))
    out = P.copy()
    if A is not None:
        out += wa[:, None] * (apply(A, P) - P)
    if B is not None:
        out += wb[:, None] * (apply(B, P) - P)
    return out


class Cam:
    def __init__(self, camera, W, H, fov=45.0, pad=1.08):
        half = math.radians(fov / 2)
        aspect = W / H
        fitV = camera['radius'] / math.sin(half)
        fitH = camera['radius'] / math.sin(math.atan(math.tan(half) * aspect))
        dist = max(fitV, fitH) * pad
        d = np.asarray(camera['dir'], float); d /= np.linalg.norm(d)
        self.target = np.asarray(camera['target'], float)
        self.pos = self.target + d * dist
        z = d
        x = np.cross([0, 1, 0], z); x /= np.linalg.norm(x)
        y = np.cross(z, x)
        self.R = np.array([x, y, z])
        self.th, self.aspect, self.W, self.H = math.tan(half), aspect, W, H
        self.mm_per_px = 2 * dist * self.th / H          # (at the target's depth)

    def project(self, p):
        p = np.atleast_2d(np.asarray(p, float))
        c = (self.R @ (p - self.pos).T).T
        x = (c[:, 0] / -c[:, 2]) / (self.th * self.aspect)
        y = (c[:, 1] / -c[:, 2]) / self.th
        return np.c_[(x + 1) / 2 * self.W, (1 - y) / 2 * self.H]


def corners(lo, hi):
    return np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])


def part_rect(cam, boxes, view, pid):
    if pid not in boxes:
        return None
    lo, hi = boxes[pid]
    q = cam.project(apply(pose_matrix(view['offsets'].get(pid)), corners(lo, hi)))
    return [q[:, 0].min(), q[:, 1].min(), q[:, 0].max(), q[:, 1].max()]


def wire_points(cam, routes, view, ids=None):
    out = {}
    for wid, no in (view.get('wires') or {}).items():
        if ids is not None and wid not in ids:
            continue
        out[wid] = cam.project(skinned(routes[no], view['offsets']))
    return out


def screen_rect(cam, boxes, routes, view):
    x0 = y0 = math.inf
    x1 = y1 = -math.inf
    for pid in view['visible']:
        r = part_rect(cam, boxes, view, pid)
        if r is None:
            continue
        x0, y0, x1, y1 = min(x0, r[0]), min(y0, r[1]), max(x1, r[2]), max(y1, r[3])
    for wid, q in wire_points(cam, routes, view).items():
        q = q[::4]
        x0, y0, x1, y1 = min(x0, q[:, 0].min()), min(y0, q[:, 1].min()), max(x1, q[:, 0].max()), max(y1, q[:, 1].max())
    return dict(x0=x0, y0=y0, x1=x1, y1=y1)


NEAR = {'up-right': (1, -1), 'up-left': (-1, -1), 'down-right': (1, 1), 'down-left': (-1, 1),
        'near-left': (-1.25, 0), 'near-right': (1.25, 0), 'near-above': (0, -1.25), 'near-below': (0, 1.25)}


def instructions_box(view, W):
    """The caption box at the top left (player.html: #instructions left 16 top 14, #caption 18.4px, line-height 1.35, padding
    8 8 8 14, border 2, gap 10 before the speak button (about 34 px), max-width min(560px, 70vw); in a window of 700 px or less, top 46
    and right 16)."""
    text = view.get('caption') or ''
    if not text:
        return None
    narrow = W <= 700
    maxw = (W - 32) if narrow else min(560, 0.7 * W, W - 236)
    inner = maxw - (14 + 8 + 4 + 10 + 34)
    words, lines, cur = text.split(), 1, 0.0
    sp = text_width(' ', 18.4, bold=False)
    widest = 0.0
    for w in words:
        ww = text_width(w, 18.4, bold=False)
        if cur and cur + sp + ww > inner:
            widest = max(widest, cur); lines += 1; cur = ww
        else:
            cur = cur + sp + ww if cur else ww
    widest = max(widest, cur)
    width = min(maxw, widest + 14 + 8 + 4 + 10 + 34)
    height = lines * 18.4 * 1.35 + 16 + 4
    if view.get('caution'):
        height += 8 + 40
    left, top = 16, (46 if narrow else 14)
    return dict(left=left, top=top, right=left + width, bottom=top + height)


def layout(view, cam, boxes, routes, overrides=None, top=64, bottom=12):
    """layoutCallouts, with `overrides` = {index: dict(side=, reach=)} applied to the items (labels first, then eyes)."""
    W, H = cam.W, cam.H
    size = max(15, min(28, W * 0.027)); pad = 10; gap = max(14, W * 0.02)
    R = screen_rect(cam, boxes, routes, view)
    items = [dict(l, w=text_width(l['text'], size) + 2 * pad, h=size + 12) for l in (view.get('labels') or [])]
    items += [dict(e, eye=True, w=max(44, W * 0.07), h=max(44, W * 0.07) * 0.56) for e in (view.get('eye') or [])]
    for k, it in enumerate(items):
        if overrides and k in overrides:
            it.update(overrides[k])
    for it in items:
        pid = it.get('id')
        A = apply(pose_matrix(view['offsets'].get(pid)) if pid else np.eye(4), it['anchor'])
        ax, ay = cam.project(A)[0]
        it['ax'], it['ay'] = ax, ay
        room = dict(right=W - R['x1'] - gap - it['w'] - 8, left=R['x0'] - gap - it['w'] - 8, top=R['y0'] - gap - it['h'] - top,
                    bottom=H - R['y1'] - gap - it['h'] - bottom)
        reach = dict(right=R['x1'] - ax, left=ax - R['x0'], top=ay - R['y0'], bottom=R['y1'] - ay)
        sides = sorted([s for s in room if room[s] >= 0], key=lambda s: reach[s])
        near = NEAR.get(it.get('side'))
        it['asked'] = it.get('side')
        it['side'] = it['side'] if (near or it.get('side') in ('left', 'right', 'top', 'bottom')) else (sides[0] if sides else 'float')
        w, h = it['w'], it['h']
        if near:
            d = (it.get('reach') or 0.07) * W
            it['x'] = ax + near[0] * d - (w if near[0] < 0 else (w / 2 if near[0] == 0 else 0))
            it['y'] = ay + near[1] * d - (h if near[1] < 0 else (h / 2 if near[1] == 0 else 0))
        elif it['side'] == 'right':
            it['x'], it['y'] = R['x1'] + gap, ay - h - gap * 1.6
        elif it['side'] == 'left':
            it['x'], it['y'] = R['x0'] - gap - w, ay - h - gap * 1.6
        elif it['side'] == 'top':
            it['x'], it['y'] = ax + gap, R['y0'] - gap - h
        elif it['side'] == 'bottom':
            it['x'], it['y'] = ax + gap, R['y1'] + gap
        else:
            it['x'] = ax + (-1 if ax > W / 2 else 1) * 90 - (w if ax > W / 2 else 0)
            it['y'] = ay - 90
        it['clamped'] = False
        x = max(8, min(W - w - 8, it['x'])); y = max(top, min(H - h - bottom, it['y']))
        if abs(x - it['x']) > 0.5 or abs(y - it['y']) > 0.5:
            it['clamped'] = True
        it['x'], it['y'] = x, y
    box = instructions_box(view, W)
    for it in items:
        if box and it['x'] < box['right'] + 8 and it['x'] + it['w'] > box['left'] - 8 and it['y'] < box['bottom'] + 8:
            it['y'] = min(H - it['h'] - bottom, box['bottom'] + 12)
            it['moved_down'] = True
    for side in ['right', 'left', 'top', 'bottom', 'float']:
        group = [i for i in items if i['side'] == side]
        horizontal = side in ('top', 'bottom')
        group.sort(key=lambda i: (i['x'],) if horizontal else (i['ay'], i['y']))
        for a, b in zip(group, group[1:]):
            if horizontal:
                if b['x'] < a['x'] + a['w'] + 14:
                    b['x'] = a['x'] + a['w'] + 14
            elif b['y'] < a['y'] + a['h'] + 10:
                b['y'] = a['y'] + a['h'] + 10
    for it in items:
        y = it['y'] + it['h'] / 2 if it.get('eye') else it['y'] + it['h']
        x = it['x'] if abs(it['ax'] - it['x']) < abs(it['ax'] - (it['x'] + it['w'])) else it['x'] + it['w']
        it['leader'] = (x, y, it['ax'], it['ay'])
        it['leader_len'] = math.hypot(it['ax'] - x, it['ay'] - y)
    return items, R, box, size
