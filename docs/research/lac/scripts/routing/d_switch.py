from design_common import *
from scipy.spatial import cKDTree
FLAT = [-117.7, 17.3, -0.1]
EXITS = {'red': np.array([672.52, 929.76, 1258.37]), 'tan': np.array([679.52, 929.76, 1258.37]), 'black': np.array([686.52, 929.76, 1258.37])}
CAP = {'red': 'NAUO47', 'tan': 'NAUO49', 'black': 'NAUO48'}
def lead(c, ways):
    e = EXITS[c] + FLAT
    return into_hole(CAP[c], e, [0, -1, 0], ways)
def lanes(zr, zb, zt, yA=930.0, yB=922.0, yC=917.0):
    return {'red': [[566.0, yA + 2, zr], [620.0, yB + 1, zr + 2], [650.0, yC, 1268.0]],
            'black': [[575.0, yA, zb], [620.0, yB, zb + 2], [650.0, yC - 1, 1265.0]],
            'tan': [[570.0, yA + 1, zt], [620.0, yB + 2, zt + 2], [655.0, yC + 2, 1262.0], [688.0, yC, 1266.0]]}
def pair_gap(lines):
    out = 1e9
    ks = list(lines)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            a, _, _ = dense(lines[ks[i]], 0.3); b, _, _ = dense(lines[ks[j]], 0.3)
            d, _ = cKDTree(b).query(a[30:-30]); out = min(out, float(d.min()) - 1.25)
    return out
res = []
for zr in (1262.0, 1264.0):
    for zb in (1258.5, 1259.5):
        for zt in (1252.0, 1254.0):
            for yA, yB, yC in ((930.0, 922.0, 917.0), (934.0, 925.0, 919.0)):
                L = {c: lead(c, w) for c, w in lanes(zr, zb, zt, yA, yB, yC).items()}
                g = pair_gap(L)
                worst = min(clearance(v, L[c], 0.625, ends=('NAUO46', CAP[c]), wire=('switch red', 'switch tan', 'switch black'))[0] for c in L for v in ('Step 18c', 'Step 21c', 'Step 39c'))
                res.append((min(g, worst), round(g, 2), round(worst, 2), zr, zb, zt, yA, yB, yC))
res.sort(reverse=True)
for r in res[:5]: print(r)
best = res[0]
L = {c: lead(c, w) for c, w in lanes(*best[3:6], *best[6:]).items()}
for c in L:
    for v in ('Step 18c', 'Step 21c', 'Step 39c', 'Step 46c'):
        print(c, v, clearance(v, L[c], 0.625, ends=('NAUO46', CAP[c]), wire=('switch red', 'switch tan', 'switch black')))
