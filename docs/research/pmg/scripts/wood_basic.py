"""Wood parts: size, plate normal (largest-area face direction), slab thickness, engraving pocket faces."""
import sys, json, numpy as np
SP = sys.argv[1]
d = np.load(SP + '/wood.npz')
NAMES = {'NAUO60': 'H6', 'NAUO61': 'H8', 'NAUO62': 'H11v2', 'NAUO63': 'H1', 'NAUO64': 'H10', 'NAUO65': 'H2', 'NAUO66': 'H3', 'NAUO67': 'H5',
         'NAUO68': 'H7', 'NAUO69': 'H9', 'NAUO70': 'H9', 'NAUO71': 'H9', 'NAUO72': 'H9', 'NAUO73': 'H4v2', 'NAUO74': 'H14', 'NAUO75': 'H13v2', 'NAUO77': 'H12v2'}
res = {}
for i, nm in NAMES.items():
    V, F = d[i + '__V'], d[i + '__F']
    tri = V[F]
    cr = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    area = np.linalg.norm(cr, axis=1) / 2
    n = cr / np.maximum(2 * area[:, None], 1e-12)
    # cluster normals: sign-agnostic
    key = np.round(np.where(n[:, [0]] < 0, -n, n) * 1, 2)
    best, bestA = None, 0
    for k in np.unique(key, axis=0):
        m = np.all(key == k, axis=1)
        if area[m].sum() > bestA:
            bestA, best = area[m].sum(), k
    nrm = best / np.linalg.norm(best)
    t = V @ nrm
    lo, hi = V.min(0), V.max(0)
    # levels along the normal (face planes): faces whose normal is +-nrm
    par = np.abs(n @ nrm) > 0.999
    lev = np.round((tri[par] @ nrm).mean(1), 3)
    levels, cnt = np.unique(lev, return_counts=True)
    la = {float(l): float(area[par][lev == l].sum()) for l in levels}
    res[i] = dict(name=nm, lo=lo.round(2).tolist(), hi=hi.round(2).tolist(), size=(hi - lo).round(2).tolist(), mid=((lo + hi) / 2).round(2).tolist(),
                  plate_normal=nrm.round(4).tolist(), along_normal=[float(t.min().round(3)), float(t.max().round(3))], thickness=float((t.max() - t.min()).round(3)),
                  face_levels_area=la, nverts=len(V), nfaces=len(F))
    print(i, nm, 'size', res[i]['size'], 'mid', res[i]['mid'], 'normal', res[i]['plate_normal'], 'thick', res[i]['thickness'])
    print('    levels(area):', {k: round(v, 1) for k, v in la.items()})
json.dump(res, open(SP + '/wood_basic.json', 'w'), indent=1)
