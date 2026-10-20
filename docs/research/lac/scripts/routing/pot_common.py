from design_common import *
from stepgen import apply_pose
POTL = {'red': ('NAUO34', [718.72, 906.79, 1229.65]), 'tan': ('NAUO33', [718.72, 906.68, 1235.0]), 'black': ('NAUO14', [718.72, 906.57, 1240.35])}
FB = PATHS['poses']['F1_flat_beside']
def start(c, pose=FB):
    cap, ex = POTL[c]
    e = apply_pose(pose, np.asarray([ex], float))[0]
    d = unit(apply_pose(pose, np.asarray([np.add(ex, [0.0, -1.0, 0.0])], float))[0] - e)
    return cap, e, d
def plugged(c, way, pose=FB):
    cap, e, d = start(c, pose)
    return into_hole(cap, e, d, way)
POTW = ('pot red', 'pot tan', 'pot black')
def mutual(lines, skip=25):
    out = (1e9, None)
    ks = list(lines)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            a, _, _ = dense(lines[ks[i]], 0.3); b, _, _ = dense(lines[ks[j]], 0.3)
            d, _ = cKDTree(b).query(a[skip:-skip]); g = float(d.min()) - 1.25
            if g < out[0]: out = (g, ks[i] + '/' + ks[j])
    return out
from scipy.spatial import cKDTree
def worst(lines, views):
    res = []
    for c, L in lines.items():
        for v in views:
            if v not in VIEWS: continue
            g, what = clearance(v, L, 0.625, ends=('NAUO11', POTL[c][0]), wire=POTW, end_mm=5.0)
            res.append((round(g, 2), c, v, what))
    return min(res)
