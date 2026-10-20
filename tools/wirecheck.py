"""Where a wire, as drawn in a view, passes into a part shown in that view, or into another wire (route points as written, parts at
the view's poses).

    .venv.nosync/bin/python tools/wirecheck.py <kit folder> [steps file]

Each route is resampled every 0.2 mm (a 3 mm plate crossed between two of the route's own points would otherwise go unseen). A point
away from the wire's own ends counts when it is inside a part on screen in that view (the part at the view's pose), or within 0.7 of
the wire's radius of its surface; two wires count when their centre lines come closer than 0.9 of their radii added. The route is
taken as written (the player bends a route a little when its end parts are not where it was drawn). Run after changing a guide's
wires; each line names the view, the wire, the part (or the other wire) and the nearest point (in that part's seated frame).
"""
import json, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from stepgen import Model, unapply_pose

STEP, END = 0.2, 5.0                   # resampling step; how far from each end a wire may touch the parts it is tied to (mm)


def dense(pts, step=STEP):
    pts = np.asarray(pts, float)
    L = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    s = np.arange(0.0, L[-1], step)
    return np.c_[[np.interp(s, L, pts[:, k]) for k in range(3)]].T, s, L[-1]


kit = sys.argv[1]
steps = json.load(open(f'{kit}/{sys.argv[2] if len(sys.argv) > 2 else "steps.json"}'))
spec = json.load(open(f'{kit}/materials.json'))
M = Model(f'{kit}/{spec["source"]}')
radius = {w: d['radius'] for w, d in steps['wires'].items()}
seen, problems = set(), 0
for v in steps['views']:
    if v.get('kind') not in ('hover', 'done'):
        continue
    offs = v.get('offsets', {})
    lines = {}
    for w, ri in (v.get('wires') or {}).items():
        r = steps['routes'][ri]
        pts, s, length = dense(r['pts'])
        lines[w] = (pts, ri)
        inner = pts[(s > END) & (s < length - END)]
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
            p = q[sel]
            cp, d, tri = M.inst[i].nearest.on_surface(p)
            inside = np.einsum('ij,ij->i', p - cp, M.inst[i].face_normals[tri]) < 0
            bad = inside | (d < rad * 0.7)
            if bad.any():
                k = np.where(bad)[0][np.argmax(np.where(inside[bad], d[bad], -d[bad]))]
                hits.append(f"{i} ({'inside ' if inside[k] else ''}{d[k]:.2f} mm, {int(bad.sum())} pts, at {p[k].round(1).tolist()})")
        if hits:
            msg = f'{v["name"]:10s} {w:13s} route {ri}: ' + '; '.join(hits)
            if msg not in seen:
                seen.add(msg)
                problems += 1
                print(msg)
    names = sorted(lines)
    for a in range(len(names)):                                    # wires through each other
        for b in range(a + 1, len(names)):
            (pa, ra), (pb, rb) = lines[names[a]], lines[names[b]]
            d, k = cKDTree(pb).query(pa)
            near = 0.9 * (radius[names[a]] + radius[names[b]])
            if (d < near).any():
                j = int(np.argmin(d))
                msg = f'{v["name"]:10s} {names[a]:13s} route {ra}: wire {names[b]} (route {rb}) {d[j]:.2f} mm apart at {pa[j].round(1).tolist()}'
                if msg not in seen:
                    seen.add(msg)
                    problems += 1
                    print(msg)
print('checked', len(steps['views']), 'views;', problems, 'problems')
