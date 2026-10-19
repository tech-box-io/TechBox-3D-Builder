"""Joints between crossing plates: along the line where two plates cross (both at mid-thickness, and 1 mm either side within each
plate), the stretches of material of each plate and where they overlap. Tells tab-in-slot (one part's material in the other's gap),
open notch vs closed slot, and press fits (overlap)."""
import sys, json, numpy as np, trimesh
SP = sys.argv[1]
d = np.load(SP + '/wood.npz'); P = json.load(open(SP + '/wood_planes.json')); B = json.load(open(SP + '/wood_basic.json'))
M = {}
for k in d.files:
    if k.endswith('__V'):
        i = k[:-3]; m = trimesh.Trimesh(d[i + '__V'], d[i + '__F'], process=True); m.merge_vertices(); M[i] = m
NM = {i: P[i]['name'] for i in P}
NM.update({'NAUO69': 'H9 (z 1325-1356)', 'NAUO70': 'H9 (z 1292-1323)', 'NAUO71': 'H9 (z 1258-1289)', 'NAUO72': 'H9 (z 1225-1256)'})
def mid(i):
    n = np.array(P[i]['normal']); t = d[i + '__V'] @ n; return n, (t.min() + t.max()) / 2
def intervals(mask, t):
    out, on = [], None
    for k in range(len(t)):
        if mask[k] and on is None: on = t[k]
        if not mask[k] and on is not None: out.append([round(float(on), 2), round(float(t[k - 1]), 2)]); on = None
    if on is not None: out.append([round(float(on), 2), round(float(t[-1]), 2)])
    return out
PAIRS = [('NAUO63', 'NAUO65'), ('NAUO63', 'NAUO66'), ('NAUO73', 'NAUO65'), ('NAUO73', 'NAUO66'), ('NAUO73', 'NAUO67'), ('NAUO73', 'NAUO64'),
         ('NAUO73', 'NAUO62'), ('NAUO73', 'NAUO77'), ('NAUO73', 'NAUO69'), ('NAUO65', 'NAUO67'), ('NAUO65', 'NAUO60'), ('NAUO65', 'NAUO68'),
         ('NAUO66', 'NAUO67'), ('NAUO66', 'NAUO60'), ('NAUO66', 'NAUO68'), ('NAUO65', 'NAUO64'), ('NAUO66', 'NAUO64'), ('NAUO65', 'NAUO61'),
         ('NAUO66', 'NAUO61'), ('NAUO67', 'NAUO61'), ('NAUO61', 'NAUO69'), ('NAUO64', 'NAUO62'), ('NAUO64', 'NAUO77'), ('NAUO61', 'NAUO62'),
         ('NAUO61', 'NAUO77'), ('NAUO62', 'NAUO75'), ('NAUO77', 'NAUO75'), ('NAUO62', 'NAUO74'), ('NAUO77', 'NAUO74'), ('NAUO73', 'NAUO75'),
         ('NAUO63', 'NAUO67'), ('NAUO63', 'NAUO60'), ('NAUO63', 'NAUO68')]
res = []
for a, b in PAIRS:
    na, ca = mid(a); nb, cb = mid(b)
    u = np.cross(na, nb)
    if np.linalg.norm(u) < 0.5:
        continue
    u /= np.linalg.norm(u)
    # point on both mid-planes, nearest to the middle of the two boxes' overlap
    lo = np.maximum(np.array(B[a]['lo']), np.array(B[b]['lo'])); hi = np.minimum(np.array(B[a]['hi']), np.array(B[b]['hi']))
    c0 = (lo + hi) / 2
    A = np.array([na, nb, u]); rhs = np.array([ca, cb, u @ c0]); p0 = np.linalg.solve(A, rhs)
    allv = np.vstack([d[a + '__V'], d[b + '__V']]); tt = (allv - p0) @ u
    t = np.arange(tt.min() - 1, tt.max() + 1, 0.05)
    out = dict(a=NM[a], b=NM[b], a_id=a, b_id=b, line_dir=u.round(3).tolist(), line_point=p0.round(2).tolist(), lines={})
    for off_name, off in (('mid', np.zeros(3)), ('a+1', na * 1.0), ('a-1', -na * 1.0), ('b+1', nb * 1.0), ('b-1', -nb * 1.0)):
        pts = p0 + off + np.outer(t, u)
        ia = M[a].contains(pts); ib = M[b].contains(pts)
        coord = (pts @ u) if True else t
        # report in assembly coordinate along the dominant axis of u
        ax = int(np.argmax(np.abs(u))); cc = pts[:, ax]
        order = np.argsort(cc)
        out['lines'][off_name] = dict(axis='XYZ'[ax], a_material=intervals(ia[order], cc[order]), b_material=intervals(ib[order], cc[order]),
                                      overlap=intervals((ia & ib)[order], cc[order]))
    res.append(out)
    L = out['lines']['mid']
    print(f"{NM[a]} x {NM[b]} along {L['axis']} at {p0.round(1).tolist()}:\n   {NM[a]}: {L['a_material']}\n   {NM[b]}: {L['b_material']}\n   overlap: {L['overlap']}")
json.dump(res, open(SP + '/wood_crossings.json', 'w'), indent=1)
