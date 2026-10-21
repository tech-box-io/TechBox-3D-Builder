"""Steps 19 - 20: every view direction, which of the label spots (the display's pin and the module's) a camera there sees clear of the
parts and wires on screen, and how squarely it sees the display's printed back."""
import sys, json
import numpy as np
import trimesh
SP = __import__('os').path.dirname(__import__('os').path.abspath(__file__))
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/tools')
import stepgen
from stepgen import _matrix
KIT = '/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions'
S = json.load(open('/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions/steps.json'))
spec = json.load(open(KIT + '/materials.json'))
model = stepgen.Model(KIT + '/' + spec['source'], adjust=spec.get('adjust_mm') or {}, own_parts=spec.get('own_parts', {}),
                      extra_parts={i: (KIT + '/' + e['glb'], e['pose']) for i, e in spec.get('extra_parts', {}).items()})
routes = S['routes']; radius = {w: d['radius'] for w, d in S['wires'].items()}
V = {v['name']: v for v in S['views']}
DISPLAY = 'NAUO79'


def rest(v):
    M = {}
    carry, offs = v.get('carry') or {}, v.get('offsets') or {}
    def placed(pid, d=0):
        if pid in M: return M[pid]
        c = carry.get(pid)
        M[pid] = _matrix(offs.get(pid)) if c is None or d > 8 else placed(c['by'], d + 1) @ _matrix(c['pose'])
        return M[pid]
    for pid in v['visible']: placed(pid)
    return M


def ramp(s):
    t = np.clip((s - 0.1) / 0.8, 0, 1); return t * t * (3 - 2 * t)


def skinned(r, M):
    p = np.asarray(r['pts'], float); s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]; u = s / (s[-1] or 1)
    if r.get('b_from'): u = (s - r['b_from']) / max(1e-6, s[-1] - r['b_from'])
    def mv(part, ref):
        if not part: return None
        X = M.get(part, np.eye(4)); return X @ np.linalg.inv(_matrix(ref)) if ref is not None else X
    A, B = mv(r.get('a'), r.get('a_ref')), mv(r.get('b'), r.get('b_ref'))
    wb = ramp(u)[:, None] if r.get('b') else np.zeros((len(p), 1)); wa = 1 - wb if r.get('a') else np.zeros((len(p), 1))
    out = p.copy()
    for X, w in ((A, wa), (B, wb)):
        if X is not None: out += w * ((p @ X[:3, :3].T + X[:3, 3]) - p)
    return out


def scene(v):
    M = rest(v)
    meshes = []
    for pid in v['visible']:
        if pid not in model.inst or pid.startswith('STEM_'): continue
        m = model.inst[pid].copy(); m.apply_transform(M[pid]); meshes.append(m)
    big = trimesh.util.concatenate(meshes)
    wires = {w: skinned(routes[no], M) for w, no in v['wires'].items()}
    return big, wires, M


def seen(cam, target, big, wires, tol=1.5):
    d = target - cam; L = np.linalg.norm(d); d /= L
    locs, _, _ = big.ray.intersects_location([cam], [d])
    if len(locs):
        t = (locs - cam) @ d
        if (t < L - tol).any(): return False
    for w, p in wires.items():
        q = p - cam; t = np.clip(q @ d, 0, L - tol); dist = np.linalg.norm(q - t[:, None] * d, axis=1)
        if (dist < radius[w] + 0.2).any(): return False
    return True


NEED = float(sys.argv[1]) if len(sys.argv) > 1 else 0.8
GRID = np.array([[dx, -dy, dz] for dx in (-1.0, 0.0, 1.0) for dz in (-1.0, 0.0, 1.0) for dy in (0.0, 1.5, 3.0, 4.5)])


def frac(cam, t, big, wires):
    return float(np.mean([seen(cam, t + o, big, wires, tol=1.2) for o in GRID]))


steps = ['Step 19', 'Step 20']
data = {}
for name in steps:
    v = V[name]
    big, wires, M = scene(v)
    targets = [M[l['id']][:3, :3] @ np.asarray(l['anchor'], float) + M[l['id']][:3, 3] for l in v['labels'][:2]]
    data[name] = (big, wires, targets, [l['text'] for l in v['labels'][:2]])
    if name == 'Step 19':
        Vd = np.asarray(model.inst[DISPLAY].vertices) @ M[DISPLAY][:3, :3].T + M[DISPLAY][:3, 3]
        c = Vd - Vd.mean(0); w_, vec = np.linalg.eigh(c.T @ c); n = vec[:, 0]
        if n @ np.array([0.507, 0.766, -0.396]) < 0: n = -n
        print('display back normal', n.round(3), 'extents', np.sqrt(w_ / len(Vd)).round(1))
centre = np.array([672.0, 905.0, 1262.0]); dist = 74.0 / np.sin(np.radians(22.5)) * 1.08
ref = {'PINS': np.array([0.2198, 0.766, 0.604]), 'RUN': np.array([0.507, 0.766, -0.396])}
rows = []
for el in range(25, 86, 4):
    for az in range(0, 360, 6):
        e, a = np.radians(el), np.radians(az)
        d = np.array([np.cos(e) * np.cos(a), np.sin(e), np.cos(e) * np.sin(a)])
        cam = centre + d * dist
        ok = {}
        for name, (big, wires, targets, texts) in data.items():
            for t, tx in zip(targets, texts):
                ok[f'{name}:{tx}'] = frac(cam, t, big, wires)
        back = float(np.degrees(np.arccos(np.clip(d[0], -1, 1))))
        rows.append((el, az, d.round(4), ok, back))
import pickle
pickle.dump(rows, open(__import__('tempfile').gettempdir() + '/cam1920_rows.pkl', 'wb'))
for lim in (55, 60, 65, 70):
    cand = [r for r in rows if r[4] <= lim]
    best = sorted(cand, key=lambda r: -min(r[3]['Step 19:V9'], r[3]['Step 20:G9']))[:5]
    print('back <=', lim)
    for el, az, d, ok, back in best:
        print(f'   el {el} az {az} dir {d.tolist()} back {back:.0f}', {k: round(v, 2) for k, v in ok.items()})
