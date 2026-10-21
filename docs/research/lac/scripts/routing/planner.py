"""Plan a wire's way through a view's parts and wires: a clearance field on a 1 mm grid (signed distance to the parts' surfaces,
distance to other wires' tubes), then A* over the free voxels, preferring clearance; the path is smoothed and thinned into control
points for into_hole()."""
import heapq, itertools
import trimesh
from pot_common import *

def surface_samples(view, skip=(), spacing=0.35, box=None, poses=None):
    v = VIEWS[view]
    pts, nrm = [], []
    for i in list(v['visible']) + [i for i in (poses or {}) if i not in v['visible']]:
        if i in skip:
            continue
        m = M.inst[i]
        off = (poses or {}).get(i, v.get('offsets', {}).get(i))
        V = apply_pose(off, m.vertices) if off is not None else np.asarray(m.vertices)
        if box is not None:
            lo, hi = V.min(0), V.max(0)
            if np.any(hi < box[0] - 3) or np.any(lo > box[1] + 3):
                continue
        mm = trimesh.Trimesh(V, m.faces, process=False)
        n = int(mm.area / spacing ** 2) + 100
        p, f = trimesh.sample.sample_surface_even(mm, n, seed=1) if hasattr(trimesh.sample, 'sample_surface_even') else trimesh.sample.sample_surface(mm, n)
        if len(p) < n * 0.5:
            p, f = trimesh.sample.sample_surface(mm, n, seed=1)
        pts.append(p); nrm.append(mm.face_normals[f])
    return np.vstack(pts), np.vstack(nrm)

def wire_samples(view, exclude, extra=()):
    v = VIEWS[view]; P, R = [], []
    for w, ri in (v.get('wires') or {}).items():
        if w in exclude: continue
        q, _, _ = dense(S['routes'][ri]['pts'], 0.3); P.append(q); R.append(np.full(len(q), RAD[w]))
    for q, r in extra:
        q, _, _ = dense(q, 0.3); P.append(q); R.append(np.full(len(q), r))
    return np.vstack(P), np.concatenate(R)

class Field:
    def __init__(self, view, box, skip=(), exclude=POTW, extra=(), pitch=1.0, poses=None):
        self.lo, self.hi, self.h = np.asarray(box[0], float), np.asarray(box[1], float), pitch
        self.shape = tuple((np.ceil((self.hi - self.lo) / pitch)).astype(int) + 1)
        g = np.stack(np.meshgrid(*[self.lo[k] + np.arange(self.shape[k]) * pitch for k in range(3)], indexing='ij'), -1).reshape(-1, 3)
        sp, sn = surface_samples(view, skip, box=(self.lo, self.hi), poses=poses)
        t = cKDTree(sp); d, k = t.query(g, distance_upper_bound=12.0)
        d = np.where(np.isinf(d), 12.0, d)
        inside = np.zeros(len(g), bool); ok = k < len(sp)
        inside[ok] = np.einsum('ij,ij->i', g[ok] - sp[k[ok]], sn[k[ok]]) < 0
        self.dpart = np.where(inside, -d, d).reshape(self.shape)
        wp, wr = wire_samples(view, exclude, extra)
        t2 = cKDTree(wp); d2, k2 = t2.query(g, distance_upper_bound=12.0)
        d2 = np.where(np.isinf(d2), 12.0, d2 - np.where(k2 < len(wr), wr[np.minimum(k2, len(wr) - 1)], 0.0))
        self.dwire = d2.reshape(self.shape)
        self.clear = np.minimum(self.dpart, self.dwire) - 0.625
    def idx(self, p):
        return tuple(np.clip(np.round((np.asarray(p, float) - self.lo) / self.h).astype(int), 0, np.array(self.shape) - 1))
    def pos(self, ij):
        return self.lo + np.asarray(ij, float) * self.h

def astar(F, a, b, need=0.35, pref=3.0, K=4.0, free_near=()):
    """Least-cost path from point a to point b over voxels with clearance >= need (voxels within 2.5 mm of a point in free_near
    count as free: the ends)."""
    ok = F.clear >= need
    for p in free_near:
        ij = np.array(F.idx(p)); r = 3
        sl = tuple(slice(max(0, ij[k] - r), ij[k] + r + 1) for k in range(3))
        ok[sl] = True
    cost = 1.0 + K * np.clip(pref - F.clear, 0.0, None)
    s, t = F.idx(a), F.idx(b)
    nb = [d for d in itertools.product((-1, 0, 1), repeat=3) if d != (0, 0, 0)]
    nl = [np.sqrt(sum(x * x for x in d)) for d in nb]
    gs = {s: 0.0}; came = {}; tt = np.array(t)
    hq = [(0.0, s)]
    shape = F.shape
    while hq:
        f, u = heapq.heappop(hq)
        if u == t: break
        gu = gs[u]
        if f - np.linalg.norm(np.subtract(u, tt)) > gu + 1e-9: continue
        cu = cost[u]
        for d, L in zip(nb, nl):
            v = (u[0] + d[0], u[1] + d[1], u[2] + d[2])
            if not (0 <= v[0] < shape[0] and 0 <= v[1] < shape[1] and 0 <= v[2] < shape[2]) or not ok[v]: continue
            gv = gu + L * 0.5 * (cu + cost[v])
            if gv < gs.get(v, 1e18):
                gs[v] = gv; came[v] = u
                heapq.heappush(hq, (gv + np.sqrt((v[0] - t[0]) ** 2 + (v[1] - t[1]) ** 2 + (v[2] - t[2]) ** 2), v))
    if t not in came: return None
    path = [t]
    while path[-1] != s: path.append(came[path[-1]])
    return np.array([F.pos(p) for p in path[::-1]])

def controls_from(path, every=8.0, trim=4.0):
    sm = W.smoothed(path, window_mm=12.0, spacing=0.5)
    L = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(sm, axis=0), axis=1))])
    keep = np.arange(trim, L[-1] - trim, every)
    return [sm[np.argmin(abs(L - k))].round(1).tolist() for k in keep[1:]]
