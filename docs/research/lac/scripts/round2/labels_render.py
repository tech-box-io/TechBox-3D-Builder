"""A rough picture of a view as the player lays it out (flat-shaded triangles sorted by depth, wires as thick lines, lead lines, labels,
eyes and their leaders, the caption box), to look at a label placement without a browser."""
import json
import math
import struct
import sys

import meshoptimizer as mo
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from sim import KIT, Cam, apply, instructions_box, layout, load, pose_matrix, skinned

COMP = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}
NC = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4}


def read_model():
    f = open(KIT / 'model.glb', 'rb')
    f.read(12)
    n, _ = struct.unpack('<II', f.read(8))
    g = json.loads(f.read(n))
    m, _ = struct.unpack('<II', f.read(8))
    blob = f.read(m)
    views = []
    for bv in g['bufferViews']:
        ext = (bv.get('extensions') or {}).get('EXT_meshopt_compression')
        if ext:
            enc = blob[ext['byteOffset']:ext['byteOffset'] + ext['byteLength']]
            if ext['mode'] == 'ATTRIBUTES':
                raw = mo.decode_vertex_buffer(ext['count'], ext['byteStride'], enc).tobytes()     # (raw bytes: count x stride)
            else:
                fn = mo.decode_index_buffer if ext['mode'] == 'TRIANGLES' else mo.decode_index_sequence
                out = fn(ext['count'], ext['byteStride'], enc)                                    # (packed at byteStride bytes each)
                raw = out.view(np.uint8)[:ext['count'] * ext['byteStride']].tobytes()
            views.append((raw, ext['byteStride']))
        else:
            views.append((blob[bv.get('byteOffset', 0):bv.get('byteOffset', 0) + bv['byteLength']], bv.get('byteStride')))

    def acc(i):
        a = g['accessors'][i]
        raw, stride = views[a['bufferView']]
        dt = np.dtype(COMP[a['componentType']])
        nc = NC[a['type']]
        off = a.get('byteOffset', 0)
        if stride and stride != dt.itemsize * nc:
            arr = np.frombuffer(raw, np.uint8)[off:off + stride * a['count']].reshape(a['count'], stride)[:, :dt.itemsize * nc].copy().view(dt)
        else:
            arr = np.frombuffer(raw, dt, a['count'] * nc, off)
        arr = arr.reshape(a['count'], nc).astype(float)
        if a.get('normalized'):
            arr = arr / {np.int8: 127, np.uint8: 255, np.int16: 32767, np.uint16: 65535}[COMP[a['componentType']]]
        return arr

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

    parts = {}

    def walk(i, M, out):
        node = g['nodes'][i]
        M = M @ mat(node)
        if 'mesh' in node:
            for p in g['meshes'][node['mesh']]['primitives']:
                if p.get('mode', 4) != 4 or 'indices' not in p:
                    continue
                pos = acc(p['attributes']['POSITION'])
                pos = (M[:3, :3] @ pos.T).T + M[:3, 3]
                idx = acc(p['indices']).astype(np.int64).reshape(-1, 3)
                colour = None
                if 'COLOR_0' in p['attributes']:
                    c = acc(p['attributes']['COLOR_0'])[:, :3]
                    colour = np.clip(c[idx].mean(1), 0, 1) ** (1 / 2.2)
                mat_ = g['materials'][p['material']] if 'material' in p else {}
                base = (mat_.get('pbrMetallicRoughness') or {}).get('baseColorFactor', [0.8, 0.8, 0.8, 1])
                if colour is None:
                    colour = np.tile(np.clip(np.asarray(base[:3], float), 0, 1) ** (1 / 2.2), (len(idx), 1))
                out.append((pos[idx], colour))
        for c in node.get('children', []):
            walk(c, M, out)

    root = g['nodes'][g['scenes'][0]['nodes'][0]]
    for c in root.get('children', []):
        out = []
        walk(c, mat(root), out)
        if out:
            parts[g['nodes'][c]['name']] = (np.vstack([o[0] for o in out]), np.vstack([o[1] for o in out]))
    return parts


WIRE_RGB = {'jumper_black': (40, 40, 40), 'jumper_green': (40, 200, 80), 'jumper_purple': (130, 50, 170), 'jumper_blue': (30, 110, 220),
            'jumper_white': (235, 235, 235), 'jumper_dark_red': (150, 20, 20), 'jumper_orange': (245, 140, 20), 'jumper_yellow': (245, 210, 30),
            'jumper_teal': (20, 170, 170), 'lead_red': (230, 40, 50), 'lead_tan': (190, 140, 90), 'lead_black': (30, 30, 30), 'pin': (180, 180, 180),
            'cable_black': (30, 30, 30)}
ACCENT = (115, 207, 240)


def render(d, boxes, routes, parts, i, W, H, overrides=None, path=None, scale=1.0):
    v = d['views'][i]
    cam = Cam(v['camera'], W, H)
    img = Image.new('RGB', (W, H), (255, 255, 255))
    dr = ImageDraw.Draw(img)
    light = np.array([0.3, 0.8, 0.5]); light /= np.linalg.norm(light)
    tris, cols, depth = [], [], []
    for pid in v['visible']:
        if pid not in parts:
            continue
        T, C = parts[pid]
        M = pose_matrix(v['offsets'].get(pid))
        P = apply(M, T.reshape(-1, 3)).reshape(-1, 3, 3)
        n = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0])
        n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
        shade = 0.55 + 0.45 * np.abs(n @ light)
        q = cam.project(P.reshape(-1, 3)).reshape(-1, 3, 2)
        z = np.linalg.norm(P.mean(1) - cam.pos, axis=1)
        tris.append(q); cols.append(np.clip(C * shade[:, None], 0, 1)); depth.append(z)
    segs = []
    for wid, no in (v.get('wires') or {}).items():
        pts = skinned(routes[no], v['offsets'])
        q = cam.project(pts)
        z = np.linalg.norm((pts[1:] + pts[:-1]) / 2 - cam.pos, axis=1)
        hx = d['wires'][wid]['colour']
        rgb = tuple(int(hx[k:k + 2], 16) for k in (1, 3, 5)) if hx.startswith('#') else WIRE_RGB.get(hx, (100, 100, 100))
        r = d['wires'][wid].get('radius', 0.6)
        wpx = max(2, int(2 * r / cam.mm_per_px))
        for k in range(len(q) - 1):
            segs.append((z[k], q[k], q[k + 1], rgb, wpx))
    T = np.concatenate(tris) if tris else np.zeros((0, 3, 2))
    C = np.concatenate(cols) if cols else np.zeros((0, 3))
    Z = np.concatenate(depth) if depth else np.zeros(0)
    allz = np.concatenate([Z, np.array([s[0] for s in segs])])
    order = np.argsort(-allz)
    nt = len(Z)
    for k in order:
        if k < nt:
            t = T[k]
            if np.abs(t).max() > 1e5:
                continue
            c = tuple(int(255 * x) for x in C[k])
            dr.polygon([tuple(p) for p in t], fill=c)
        else:
            z, a, b, rgb, wpx = segs[k - nt]
            if max(abs(a).max(), abs(b).max()) > 1e5:
                continue
            dr.line([tuple(a), tuple(b)], fill=rgb, width=wpx)
    # lead lines
    path_ = v.get('path') or []
    hops = [path_[0]] if any(isinstance(p, dict) for p in path_) else path_[:-1]
    for gd in v.get('guides') or []:
        poly = [apply(pose_matrix(w), gd['tip']) for w in hops] + [np.asarray(gd['mouth'], float)]
        q = cam.project(np.array(poly))
        dr.line([tuple(p) for p in q], fill=(255, 0, 0), width=2)
    items, R, box, size = layout(v, cam, boxes, routes, overrides=overrides)
    if box:
        dr.rectangle([box['left'], box['top'], box['right'], box['bottom']], outline=(26, 159, 217), width=2, fill=(255, 255, 255))
        dr.text((box['left'] + 14, box['top'] + 10), v.get('caption', '')[:90], fill=(0, 0, 0), font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 17))
    fnt = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', int(size))
    stroke = max(3, int(size * 0.16))
    for it in items:
        x0, y0, ax, ay = it['leader']
        dr.line([(x0, y0), (ax, ay)], fill=ACCENT, width=stroke)
        rr = size * 0.36
        dr.ellipse([ax - rr, ay - rr, ax + rr, ay + rr], outline=ACCENT, width=stroke)
        if it.get('eye'):
            dr.rectangle([it['x'] - 6, it['y'] - 6, it['x'] + it['w'] + 6, it['y'] + it['h'] + 6], fill=(255, 255, 255))
            dr.ellipse([it['x'], it['y'], it['x'] + it['w'], it['y'] + it['h']], fill=(17, 17, 17))
            cx, cy, r2 = it['x'] + it['w'] / 2, it['y'] + it['h'] / 2, it['h'] * 0.3
            dr.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=(255, 255, 255))
        else:
            dr.rectangle([it['x'] - 2, it['y'] + 2, it['x'] + it['w'] + 2, it['y'] + it['h']], fill=(255, 255, 255))
            dr.line([(it['x'], it['y'] + it['h']), (it['x'] + it['w'], it['y'] + it['h'])], fill=ACCENT, width=stroke)
            dr.text((it['x'] + 10, it['y'] + it['h'] - 9 - size), it['text'], fill=(17, 17, 17), font=fnt)
    dr.text((W - 160, H - 24), v['name'], fill=(120, 120, 120), font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 16))
    if scale != 1.0:
        img = img.resize((int(W * scale), int(H * scale)), Image.LANCZOS)
    if path:
        img.save(path)
    return img, items


if __name__ == '__main__':
    d, boxes, routes = load()
    parts = read_model()
    print(sum(len(t) for t, _ in parts.values()), 'triangles')
