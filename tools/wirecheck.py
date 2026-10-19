"""Where a wire, as drawn in a view, passes into a part shown in that view (route points as written, parts at the view's poses).

    .venv.nosync/bin/python tools/wirecheck.py <kit folder> [steps file]

A wire's points (away from its own ends) within 0.7 of its radius of the surface of a part on screen in that view, the part at the
view's pose, the route as written (the player bends a route a little when its end parts are not where it was drawn). Run after
changing a guide's wires; each line names the view, the wire, the part and the nearest point (in that part's seated frame).
"""
import json, sys
import numpy as np
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from stepgen import Model, unapply_pose

kit = sys.argv[1]
steps = json.load(open(f'{kit}/{sys.argv[2] if len(sys.argv) > 2 else "steps.json"}'))
spec = json.load(open(f'{kit}/materials.json'))
M = Model(f'{kit}/{spec["source"]}')
radius = {w: d['radius'] for w, d in steps['wires'].items()}
seen = set()
for v in steps['views']:
    if v.get('kind') not in ('hover', 'done'):
        continue
    offs = v.get('offsets', {})
    for w, ri in (v.get('wires') or {}).items():
        key = (w, ri, json.dumps({i: offs.get(i) for i in v['visible']}, sort_keys=True))
        r = steps['routes'][ri]
        pts = np.asarray(r['pts'], float)
        L = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
        inner = pts[(L > 5.0) & (L < L[-1] - 5.0)]
        rad = radius[w]
        hits = []
        for i in v['visible']:
            if i in (r.get('a'), r.get('b')) or i.startswith('STEM_'):
                continue
            q = unapply_pose(offs.get(i), inner) if offs.get(i) is not None else inner
            lo, hi = M.inst[i].bounds
            sel = np.all((q > lo - rad) & (q < hi + rad), axis=1)
            if not sel.any():
                continue
            d = M.inst[i].nearest.on_surface(q[sel])[1]
            if (d < rad * 0.7).any():
                hits.append(f'{i} ({d.min():.2f} mm, {int((d < rad * 0.7).sum())} pts near {q[sel][d.argmin()].round(1).tolist()})')
        if hits:
            msg = f'{v["name"]:10s} {w:13s} route {ri}: ' + '; '.join(hits)
            if msg not in seen:
                seen.add(msg)
                print(msg)
print('checked', len(steps['views']), 'views')
