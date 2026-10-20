"""Fast clearance checks for candidate wire routes against the LAC's parts and other wires, view by view (as tools/wirecheck.py)."""
import json, sys, numpy as np
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/tools')
from pathlib import Path
from scipy.spatial import cKDTree
from stepgen import Model, unapply_pose
import wires as W
KIT = Path('/Users/lee-johnson/Desktop/Claude_Cadasio/LAC Build Instructions')
spec = json.load(open(KIT / 'materials.json'))
M = Model(KIT / spec['source'], adjust=spec.get('adjust_mm') or {}, own_parts=spec.get('own_parts', {}),
          extra_parts={i: (KIT / e['glb'], e['pose']) for i, e in spec.get('extra_parts', {}).items()})
S = json.load(open(KIT / 'steps.json'))
VIEWS = {v['name']: v for v in S['views']}
RAD = {w: d['radius'] for w, d in S['wires'].items()}
PATHS = json.load(open(KIT / 'wire-paths.json'))

def dense(pts, step=0.2):
    pts = np.asarray(pts, float)
    L = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    s = np.arange(0.0, L[-1], step)
    return np.c_[[np.interp(s, L, pts[:, k]) for k in range(3)]].T, s, L[-1]

def check(view, pts, radius, ends=(), wire=None, end_mm=5.0, extra_skip=()):
    """Problems for a candidate route `pts` (drawn as it looks in `view`): parts it passes into, wires it comes too close to."""
    v = VIEWS[view]
    P, s, L = dense(pts)
    inner = P[(s > end_mm) & (s < L - end_mm)]
    out = []
    for i in v['visible']:
        if i in ends or i in extra_skip:
            continue
        off = v.get('offsets', {}).get(i)
        q = unapply_pose(off, inner) if off is not None else inner
        lo, hi = M.inst[i].bounds
        sel = np.all((q > lo - radius) & (q < hi + radius), axis=1)
        if not sel.any():
            continue
        p = q[sel]
        cp, d, tri = M.inst[i].nearest.on_surface(p)
        inside = np.einsum('ij,ij->i', p - cp, M.inst[i].face_normals[tri]) < 0
        bad = inside | (d < radius * 0.7)
        if bad.any():
            k = np.where(bad)[0][np.argmax(np.where(inside[bad], d[bad], -d[bad]))]
            out.append(f"{i}{' inside' if inside[k] else ''} {d[k]:.2f} at {p[k].round(1).tolist()}")
    for w, ri in (v.get('wires') or {}).items():
        if w == wire or (isinstance(wire, (tuple, list)) and w in wire):
            continue
        q, _, _ = dense(S['routes'][ri]['pts'])
        d, k = cKDTree(q).query(inner)
        near = 0.9 * (radius + RAD[w])
        if (d < near).any():
            j = int(np.argmin(d))
            out.append(f"wire {w} {d[j]:.2f} at {inner[j].round(1).tolist()}")
    return out

def clearance(view, pts, radius, ends=(), wire=None, end_mm=5.0):
    """Smallest gap (mm, surface to surface) from the route to any part / other wire in the view, for tuning."""
    v = VIEWS[view]
    P, s, L = dense(pts, 0.5)
    inner = P[(s > end_mm) & (s < L - end_mm)]
    best = (1e9, None)
    for i in v['visible']:
        if i in ends:
            continue
        off = v.get('offsets', {}).get(i)
        q = unapply_pose(off, inner) if off is not None else inner
        lo, hi = M.inst[i].bounds
        sel = np.all((q > lo - 8) & (q < hi + 8), axis=1)
        if not sel.any():
            continue
        cp, d, tri = M.inst[i].nearest.on_surface(q[sel])
        within = np.all((q[sel] > lo) & (q[sel] < hi), axis=1)       # (the inside test only within the part's box: unreliable further out)
        inside = within & (np.einsum('ij,ij->i', q[sel] - cp, M.inst[i].face_normals[tri]) < 0)
        g = np.where(inside, -d, d) - radius
        if g.min() < best[0]:
            best = (float(g.min()), i)
    for w, ri in (v.get('wires') or {}).items():
        if w == wire or (isinstance(wire, (tuple, list)) and w in wire):
            continue
        q, _, _ = dense(S['routes'][ri]['pts'], 0.5)
        d, _ = cKDTree(q).query(inner)
        g = float(d.min()) - radius - RAD[w]
        if g < best[0]:
            best = (g, 'wire ' + w)
    return best
