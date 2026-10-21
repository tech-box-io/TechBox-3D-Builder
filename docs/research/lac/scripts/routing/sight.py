"""Sight lines from the player's eye (core.js cameraPose: target + dir * radius / sin(half fov) * padding, wider for narrow windows) to
the holes a step's moving caps go into, against the caps standing in the breadboard and the wires at rest. Usage:
  sight.py steps.json "Step 14,Step 20"            report
  sight.py steps.json "Step 20" search              directions round the current one that clear every hole at every window shape"""
import json, sys, math
import numpy as np
K = "/Users/lee-johnson/Desktop/Claude_Cadasio/LAC Build Instructions/"   # (the kit)
S = json.load(open(sys.argv[1])); W = json.load(open(K + "wire-paths.json")); caps = W['caps']
V = {v['name']: v for v in S['views']}; half = math.radians(S['fov'] / 2); BB_TOP = 897.11
ASPECTS = (16 / 9, 4 / 3, 1.0, 0.6)

def eye(cam, aspect):
    d = np.array(cam['dir'], float); d /= np.linalg.norm(d)
    fitV = cam['radius'] / math.sin(half); fitH = cam['radius'] / math.sin(math.atan(math.tan(half) * aspect))
    return np.array(cam['target']) + d * max(fitV, fitH) * S['frame_padding']

def ray_box(o, e, lo, hi):
    d = e - o; t0, t1 = 1e-6, 1.0
    for i in range(3):
        if abs(d[i]) < 1e-12:
            if o[i] < lo[i] or o[i] > hi[i]: return False
            continue
        a, b = (lo[i] - o[i]) / d[i], (hi[i] - o[i]) / d[i]
        if a > b: a, b = b, a
        t0, t1 = max(t0, a), min(t1, b)
        if t0 > t1: return False
    return True

def seg_seg(p, q, A, B):
    """distances from segment pq to many segments A[i]B[i]"""
    d1 = q - p; d2 = B - A; r = p - A
    a = d1 @ d1; e = np.einsum('ij,ij->i', d2, d2); f = np.einsum('ij,ij->i', d2, r)
    c = r @ d1; b = d2 @ d1
    den = a * e - b * b
    s = np.where(den > 1e-12, np.clip((b * f - c * e) / np.where(den > 1e-12, den, 1), 0, 1), 0.0)
    t = (b * s + f) / np.where(e > 1e-12, e, 1)
    s = np.where(t < 0, np.clip(-c / a, 0, 1), np.where(t > 1, np.clip((b - c) / a, 0, 1), s)); t = np.clip(t, 0, 1)
    P = p + np.outer(s, d1); Q = A + d2 * t[:, None]
    return np.linalg.norm(P - Q, axis=1)

def blockers(v):
    mov = set(v.get('moving', [])); vis = set(v['visible']); offs = v.get('offsets', {})
    boxes = [(cid, np.array(c['box'][0]), np.array(c['box'][1])) for cid, c in caps.items()
             if cid in vis and cid not in mov and not (cid in offs and offs[cid] != [0.0, 0.0, 0.0])]
    segs = []
    for wn, ri in (v.get('wires') or {}).items():
        r = S['routes'][ri]
        if r.get('a') in mov or r.get('b') in mov: continue
        P = np.array(r['pts'], float); segs.append((wn, P[:-1], P[1:], S['wires'][wn]['radius']))
    return boxes, segs

def clearance(v, cam, holes):
    """the least room (mm) between a sight line and a wire's surface, over holes x 9 points x window shapes; -1 if a cap is in the way"""
    boxes, segs = blockers(v); worst, who = 99.0, None
    for aspect in ASPECTS:
        e = eye(cam, aspect)
        for h in holes:
            for dx in (-0.5, 0, 0.5):
                for dz in (-0.5, 0, 0.5):
                    p = h + [dx, 0.0, dz]
                    for cid, lo, hi in boxes:
                        if ray_box(p, e, lo, hi): return -1.0, cid
                    for wn, A, B, rad in segs:
                        m = float(seg_seg(p, e, A, B).min()) - rad
                        if m < worst: worst, who = m, wn
    return worst, who

def holes_of(v):
    return [np.array([caps[c]['wire_at'][0], BB_TOP, caps[c]['wire_at'][2]]) for c in v.get('moving', []) if c in caps]

def azel(d):
    d = np.array(d, float) / np.linalg.norm(d); return math.degrees(math.atan2(d[2], d[0])), math.degrees(math.asin(d[1]))
def from_azel(az, el):
    az, el = math.radians(az), math.radians(el); return [round(math.cos(el) * math.cos(az), 3), round(math.sin(el), 3), round(math.cos(el) * math.sin(az), 3)]

for name in sys.argv[2].split(','):
    v = V[name.strip()]; hs = holes_of(v); cam = v['camera']
    c, who = clearance(v, cam, hs)
    az0, el0 = azel(cam['dir'])
    print(f"{v['name']:8s} az {az0:6.1f} el {el0:5.1f}  clearance {c:6.2f} ({who})", flush=True)
    if len(sys.argv) > 3 and sys.argv[3] == "search":
        found = []
        for daz in range(-45, 50, 5):
            for el in range(35, 81, 5):
                d = from_azel(az0 + daz, el); c2, w2 = clearance(v, dict(cam, dir=d), hs)
                if c2 >= 0.5: found.append((abs(daz) + abs(el - el0) * 0.7, daz, el, d, round(c2, 2)))
        for f in sorted(found)[:6]:
            print(f"    daz {f[1]:+4d} el {f[2]:3d}  dir {f[3]}  clearance {f[4]}", flush=True)

def visible_points(v, cam, holes, room=0.2):
    """the least number of the 9 points over each hole seen clear (no cap, `room` mm from every wire), over window shapes; and whether
    every hole's centre is clear at every shape"""
    boxes, segs = blockers(v); least, centres = 9, True
    for aspect in ASPECTS:
        e = eye(cam, aspect)
        for h in holes:
            n = 0
            for dx in (-0.5, 0, 0.5):
                for dz in (-0.5, 0, 0.5):
                    p = h + [dx, 0.0, dz]
                    ok = not any(ray_box(p, e, lo, hi) for _, lo, hi in boxes) and all(float(seg_seg(p, e, A, B).min()) - rad >= room for _, A, B, rad in segs)
                    n += ok
                    if dx == 0 and dz == 0 and not ok: centres = False
            least = min(least, n)
    return least, centres

if len(sys.argv) > 3 and sys.argv[3] == 'relaxed':
    for name in sys.argv[2].split(','):
        v = V[name.strip()]; hs = holes_of(v); cam = v['camera']; az0, el0 = azel(cam['dir'])
        print(v['name'], 'now', visible_points(v, cam, hs), flush=True)
        found = []
        for daz in range(-60, 65, 5):
            for el in range(35, 86, 5):
                d = from_azel(az0 + daz, el); n, c = visible_points(v, dict(cam, dir=d), hs)
                if c: found.append((-n, abs(daz) + abs(el - el0) * 0.7, daz, el, d))
        for f in sorted(found)[:5]:
            print(f"    {-f[0]}/9  daz {f[2]:+4d} el {f[3]:3d}  dir {f[4]}", flush=True)
