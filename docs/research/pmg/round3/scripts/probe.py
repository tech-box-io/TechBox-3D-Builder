"""Load guide.py's definitions (up to a marker) with a stub Guide that has the real model, for experiments."""
import sys
import numpy as np
ROOT = '/Users/lee-johnson/Desktop/Claude_Cadasio'
KIT = ROOT + '/PMG Build Instructions'
sys.path.insert(0, ROOT + '/tools')
sys.path.insert(0, KIT)
import stepgen

_model = None


class Stub:
    def __init__(self, *a, **k):
        global _model
        if _model is None:
            _model = stepgen.Model(KIT + '/pmg-guide.glb')
        self.model = _model

    def __getattr__(self, name):
        return lambda *a, **k: None


def load(marker="g.place('Begin the electronics", guide=KIT + '/guide.py'):
    src = open(guide).read()
    src = src[:src.index(marker)] if marker else src
    src = src.replace('from stepgen import Guide,', 'from stepgen import')
    ns = {'__file__': guide, '__name__': 'probe', 'Guide': Stub}
    exec(compile(src, guide, 'exec'), ns)
    return ns


def exact_check(lines, scene, model, skip=None, radius=0.625):
    """Worst depth of each line inside each part (exact signed distance; positive = the centre line is inside by that much)."""
    import trimesh
    out = {}
    for w, pts in lines.items():
        pts = np.asarray(pts, float)
        for part, pose in scene:
            if skip and part in skip.get(w, ()):
                continue
            M = np.linalg.inv(stepgen._matrix(pose))
            q = pts @ M[:3, :3].T + M[:3, 3]
            mesh = model.inst[part]
            lo, hi = mesh.bounds
            near = np.all((q > lo - 1) & (q < hi + 1), axis=1)
            if not near.any():
                continue
            d = trimesh.proximity.signed_distance(mesh, q[near]) + radius
            if d.max() > 0.05:
                out[(w, part)] = round(float(d.max()), 2)
    return out


def overlaps(lines, end_mm=6.0, need=1.25):
    from scipy.spatial import cKDTree
    out = {}
    names = list(lines)
    for i, a in enumerate(names):
        pa = np.asarray(lines[a], float)
        t = cKDTree(pa)
        for b in names[i + 1:]:
            pb = np.asarray(lines[b], float)
            L = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pb, axis=0), axis=1))]
            d, _ = t.query(pb)
            mid = (L > end_mm) & (L < L[-1] - end_mm)
            if mid.any() and d[mid].min() < need:
                out[(a, b)] = round(float(d[mid].min()), 2)
    return out
