"""Write a steps copy with a Step 43 design in it, and check it (motioncheck's own blending, the model loaded once)."""
import copy, json
import numpy as np
from scipy.spatial import cKDTree
from common import *
import mc
from stepgen import apply_pose, unapply_pose

KITS = str(KIT)


def with_design(base, d):
    """d: dict(path=[...], stops=None|[...], red=[S1, ..., S_last], black=[...], seated={'red': route, 'black': route} (replace the old
    seated route everywhere), lying={'red': route, 'black': route} (replace the old lying route everywhere))"""
    S = copy.deepcopy(base)
    V = {v['name']: v for v in S['views']}
    v43, h43 = V['Step 43c'], V['Step 43']
    for v in (v43, h43):
        v['path'] = d['path']
        if d.get('stops'):
            v['stops'] = d['stops']
        else:
            v.pop('stops', None)
    old_seat = {c: v43['wires'][f'buzzer {c}'] for c in ('red', 'black')}
    old_lying = {c: V['Step 42c']['wires'][f'buzzer {c}'] for c in ('red', 'black')}
    for c in ('red', 'black'):
        shapes = d[c]
        nos = [put_route(S, r) for r in shapes]
        v43.setdefault('wire_via', {})[f'buzzer {c}'] = nos[:-1]
        if not nos[:-1]:
            v43['wire_via'].pop(f'buzzer {c}')
        new_seat = nos[-1]
        for v in S['views']:                      # the seated route from Step 43c on
            if (v.get('wires') or {}).get(f'buzzer {c}') == old_seat[c]:
                v['wires'][f'buzzer {c}'] = new_seat
        if d.get('lying', {}).get(c):
            ly = put_route(S, d['lying'][c])
            for v in S['views']:
                if (v.get('wires') or {}).get(f'buzzer {c}') == old_lying[c]:
                    v['wires'][f'buzzer {c}'] = ly
                if (v.get('wire_via') or {}).get(f'buzzer {c}'):
                    v['wire_via'][f'buzzer {c}'] = [ly if x == old_lying[c] else x for x in v['wire_via'][f'buzzer {c}']]
    return S


def motion(S, views=('Step 43c',), moments=39, margin=0.0, quiet=False):
    rep = {}
    n = mc.main([KITS, '--moments', str(moments), *views], steps=S, report=rep, margin=margin, quiet=quiet)
    return n, rep


def model():
    if 'm' not in mc._MODEL:
        motion(load_steps(), views=('Step 42c',), moments=1, quiet=True)
    return mc._MODEL['m']


def clearance(S, view, pts, radius=0.625, skip=(), poses=None, wire=None, end_mm=5.0, others=None):
    """Smallest surface gaps (mm) from a route (as drawn) to each part (posed as in `view`, or `poses`) and to each other wire of the view."""
    M = model()
    v = {x['name']: x for x in S['views']}[view]
    P = np.asarray(pts, float)
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
    at = np.arange(0, s[-1], 0.25)
    P = np.stack([np.interp(at, s, P[:, k]) for k in range(3)], 1)
    inner = P[(at > end_mm) & (at < s[-1] - end_mm)]
    out = []
    for i in v['visible']:
        if i in skip:
            continue
        off = (poses or {}).get(i, v.get('offsets', {}).get(i))
        q = unapply_pose(off, inner) if off is not None else inner
        m = M.inst[i]
        lo, hi = m.bounds
        sel = np.all((q > lo - 6) & (q < hi + 6), axis=1)
        if not sel.any():
            continue
        cp, dd, tri = m.nearest.on_surface(q[sel])
        within = np.all((q[sel] > lo) & (q[sel] < hi), axis=1)
        inside = within & (np.einsum('ij,ij->i', q[sel] - cp, m.face_normals[tri]) < -0.3 * dd)
        g = np.where(inside, -dd, dd) - radius
        k = int(np.argmin(g))
        out.append((round(float(g[k]), 2), i, inner[sel][k].round(1).tolist()))
    R = S['routes']
    for w, ri in (others if others is not None else (v.get('wires') or {})).items():
        if w == wire:
            continue
        q = np.asarray(R[ri]['pts'] if isinstance(ri, int) else ri, float)
        qs = np.r_[0, np.cumsum(np.linalg.norm(np.diff(q, axis=0), axis=1))]
        qa = np.arange(0, qs[-1], 0.25)
        q = np.stack([np.interp(qa, qs, q[:, k]) for k in range(3)], 1)
        dd, kk = cKDTree(q).query(inner)
        j = int(np.argmin(dd))
        out.append((round(float(dd[j]) - radius - S['wires'][w]['radius'], 2), 'wire ' + w, inner[j].round(1).tolist()))
    return sorted(out)
