"""Steps 19c - 20c: for every view direction, how much of each plugged-in cap (the new wire's two: on the module's V9 / G9 and on the
display's VCC / GND) a camera there sees past the parts and wires on screen, and how squarely it sees the display's printed back (+x)."""
import sys, json, pickle
import numpy as np
SP = __import__('os').path.dirname(__import__('os').path.abspath(__file__))
sys.path.insert(0, SP)
exec(open(SP + '/cam1920.py').read().split("steps = ['Step 19', 'Step 20']")[0].replace("S = json.load(open('/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions/steps.json'))", "S = json.load(open('/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions/steps.json'))"))
data = {}
for name in ('Step 19c', 'Step 20c'):
    v = V[name]
    before = V[name[:-1]]
    moving = [w for w, no in v['wires'].items() if before['wires'].get(w) != no][0]
    r = routes[v['wires'][moving]]
    big, wires, M = scene(v)
    wires = {w: p for w, p in wires.items() if w != moving}
    caps = {}
    for cap, side in ((r['b'], 'module'), (r['a'], 'display')):
        Vc = np.asarray(model.inst[cap].vertices)
        lo, hi = Vc.min(0), Vc.max(0)
        Wc = Vc @ M[cap][:3, :3].T + M[cap][:3, 3]
        idx = np.random.default_rng(0).choice(len(Wc), min(40, len(Wc)), replace=False)
        caps[side] = Wc[idx]
    # the scene without the two caps themselves (their own faces must not hide them)
    meshes = []
    for pid in v['visible']:
        if pid not in model.inst or pid.startswith('STEM_') or pid in (r['a'], r['b']): continue
        m = model.inst[pid].copy(); m.apply_transform(M[pid]); meshes.append(m)
    big = trimesh.util.concatenate(meshes)
    data[name] = (big, wires, caps)
centre = np.array([672.0, 905.0, 1262.0]); dist = 74.0 / np.sin(np.radians(22.5)) * 1.08
rows = []
for el in range(30, 86, 4):
    for az in range(0, 360, 6):
        e, a = np.radians(el), np.radians(az)
        d = np.array([np.cos(e) * np.cos(a), np.sin(e), np.cos(e) * np.sin(a)])
        cam = centre + d * dist
        ok = {f'{n}:{side}': float(np.mean([seen(cam, p, big, wires, tol=0.3) for p in pts]))
              for n, (big, wires, caps) in data.items() for side, pts in caps.items()}
        rows.append((el, az, d.round(4), ok, float(np.degrees(np.arccos(np.clip(d[0], -1, 1))))))
pickle.dump(rows, open(__import__('tempfile').gettempdir() + '/cam1920c_rows.pkl', 'wb'))
for lim in (55, 60, 65, 75, 90):
    cand = [r for r in rows if r[4] <= lim]
    best = sorted(cand, key=lambda r: -min(r[3]['Step 19c:module'], r[3]['Step 20c:module']))[:5]
    print('back <=', lim)
    for el, az, d, ok, back in best:
        print(f'   el {el} az {az} dir {d.tolist()} back {back:.0f}', {k: round(v, 2) for k, v in ok.items()})
for k, d in (('PINS', [0.2198, 0.766, 0.604]), ('RUN', [0.507, 0.766, -0.396]), ('NEW', [0.6113, 0.766, 0.1986])):
    d = np.array(d) / np.linalg.norm(d); cam = centre + d * dist
    print(k, {f'{n}:{side}': round(float(np.mean([seen(cam, p, big, wires, tol=0.3) for p in pts])), 2) for n, (big, wires, caps) in data.items() for side, pts in caps.items()})
