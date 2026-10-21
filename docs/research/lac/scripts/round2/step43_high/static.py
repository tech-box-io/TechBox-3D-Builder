"""At-rest clearance of the buzzer's leads in every view from a start view on: smallest surface gap to each visible part (inside: negative)
and to each other wire (centre distance minus both radii), as tools/wirecheck.py samples it (0.2 mm, 5 mm free at each end). Parts are
queried one at a time (their search caches dropped after), to keep memory down.
    python static.py <steps file> [first view] [last view] [wires comma-separated] [--views]"""
import json, sys, gc
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/tools')
from stepgen import Model, unapply_pose
KIT = Path('/Users/lee-johnson/Desktop/Claude_Cadasio/LAC Build Instructions')
args = [a for a in sys.argv[1:] if not a.startswith('--')]
SHOW_VIEWS = '--views' in sys.argv
steps = json.load(open(args[0]))
first = args[1] if len(args) > 1 else 'Step 33'
last = args[2] if len(args) > 2 and args[2] != '-' else None
WIRES = (args[3] if len(args) > 3 else 'buzzer red,buzzer black').split(',')
spec = json.load(open(KIT / 'materials.json'))
M = Model(KIT / spec['source'], adjust=spec.get('adjust_mm') or {}, own_parts=spec.get('own_parts', {}),
          extra_parts={i: (KIT / e['glb'], e['pose']) for i, e in spec.get('extra_parts', {}).items()})
radius = {w: d['radius'] for w, d in steps['wires'].items()}


def dense(pts, step=0.2):
    pts = np.asarray(pts, float)
    L = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    s = np.arange(0.0, L[-1], step)
    return np.c_[[np.interp(s, L, pts[:, k]) for k in range(3)]].T, s, L[-1]


names = [v['name'] for v in steps['views']]
i0 = names.index(first)
i1 = names.index(last) + 1 if last else len(names)
views = [v for v in steps['views'][i0:i1] if v.get('wires')]
res = {}                                                    # (view, wire) -> [(gap, what, at)]
jobs = {}                                                   # part -> [(view, wire, points in the part's frame, points)]
for v in views:
    offs = v.get('offsets', {})
    for w in WIRES:
        if w not in v['wires']:
            continue
        r = steps['routes'][v['wires'][w]]
        pts, s, L = dense(r['pts'])
        inner = pts[(s > 5.0) & (s < L - 5.0)]
        rad = radius[w]
        out = res.setdefault((v['name'], w), [])
        for w2, ri in v['wires'].items():
            if w2 == w:
                continue
            q, _, _ = dense(steps['routes'][ri]['pts'])
            d, kk = cKDTree(q).query(inner)
            k = int(np.argmin(d))
            out.append((round(float(d[k] - rad - radius[w2]), 2), 'wire ' + w2, inner[k].round(1).tolist()))
        for i in v['visible']:
            if i in (r.get('a'), r.get('b')):
                continue
            q = unapply_pose(offs.get(i), inner) if offs.get(i) is not None else inner
            lo, hi = M.inst[i].bounds
            sel = np.all((q > lo - 4) & (q < hi + 4), axis=1)
            if sel.any():
                jobs.setdefault(i, []).append((v['name'], w, q[sel], inner[sel], rad))
for i, items in jobs.items():
    mesh = M.inst[i]
    for vn, w, q, world, rad in items:
        cp, d, tri = mesh.nearest.on_surface(q)
        inside = np.einsum('ij,ij->i', q - cp, mesh.face_normals[tri]) < -0.3 * d
        g = np.where(inside, -d, d) - rad
        k = int(np.argmin(g))
        res[(vn, w)].append((round(float(g[k]), 2), i, world[k].round(1).tolist()))
    mesh._cache.clear()
    gc.collect()
worst = {}
for v in views:
    out = []
    for w in WIRES:
        if (v['name'], w) not in res:
            continue
        best = sorted(res[(v['name'], w)])
        out.append(f"{w}: " + '; '.join(f'{g:+.2f} {what} {at}' for g, what, at in best[:3]))
        for g, what, at in best:
            key = (w, what)
            if g < worst.get(key, (99,))[0]:
                worst[key] = (g, v['name'], at)
    if SHOW_VIEWS:
        print(f"{v['name']:15s} " + ' | '.join(out))
print('smallest per (wire, thing), over', views[0]['name'], '-', views[-1]['name'], ':')
for (w, what), (g, vn, at) in sorted(worst.items(), key=lambda kv: kv[1][0])[:24]:
    print(f'  {g:+.2f}  {w:13s} {what:22s} {vn:15s} {at}')
