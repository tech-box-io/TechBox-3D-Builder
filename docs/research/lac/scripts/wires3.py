from lacload import *
import json
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra

def weld(V, F, tol=1e-3):
    q = np.round(V / tol).astype(np.int64)
    _, first, inv = np.unique(q, axis=0, return_index=True, return_inverse=True)
    return V[first], inv.reshape(-1)[F]

def centreline(V, F):
    V, F = weld(V, F)
    E = np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]])
    E = np.unique(np.sort(E, axis=1), axis=0)
    w = np.linalg.norm(V[E[:, 0]] - V[E[:, 1]], axis=1) + 1e-9
    G = coo_matrix((np.r_[w, w], (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(len(V), len(V))).tocsr()
    d0 = dijkstra(G, indices=0)
    a = int(np.argmax(np.where(np.isfinite(d0), d0, -1)))
    da = dijkstra(G, indices=a)
    ok = np.isfinite(da)
    P = V[ok]; s = da[ok]
    def binned(s, step=0.5):
        b = np.floor(s / step).astype(int)
        u, inv = np.unique(b, return_inverse=True)
        cnt = np.bincount(inv)
        line = np.vstack([np.bincount(inv, P[:, k]) / cnt for k in range(3)]).T
        return line
    line = binned(s, 2.5)
    def smooth(l, k=2):
        if len(l) < 2 * k + 3: return l
        out = l.copy()
        for i in range(k, len(l) - k):
            out[i] = l[i - k:i + k + 1].mean(0)
        return out
    for step in (2.0, 1.5, 1.0, 1.0, 1.0):
        line = smooth(line)
        seg = np.diff(line, axis=0); sl = np.linalg.norm(seg, axis=1); s0 = np.r_[0, np.cumsum(sl)]
        # project points onto polyline (nearest vertex then local segment)
        T = cKDTree(line)
        _, j = T.query(P)
        j = np.clip(j, 0, len(line) - 2)
        d = line[j + 1] - line[j]; L2 = np.maximum((d * d).sum(1), 1e-12)
        t = np.clip(((P - line[j]) * d).sum(1) / L2, 0, 1)
        sp = s0[j] + t * np.sqrt(L2)
        line = binned(sp, step)
    line = smooth(line, 1)
    # radius
    T = cKDTree(line); dist, _ = T.query(P)
    r = float(np.median(dist))
    L = float(np.linalg.norm(np.diff(line, axis=0), axis=1).sum())
    return dict(r=round(r, 3), length=round(L, 2), pts=line, comp=int(ok.sum()), total=len(V))

caps = {}
for n in TOP:
    ps = pieces(n)
    if ps and ps[0][0] in ('Wire Cap V2', 'Wire Cap'):
        V, F = mesh(n)
        lo, hi = V.min(0), V.max(0)
        caps[n] = dict(kind='male' if ps[0][0] == 'Wire Cap V2' else 'female', lo=lo.round(3).tolist(), hi=hi.round(3).tolist(), axis='xyz'[int(np.argmax(hi - lo))])
def nearest_cap(e):
    best = None
    for c, ci in caps.items():
        lo, hi = np.array(ci['lo']), np.array(ci['hi'])
        d = np.linalg.norm(np.maximum(0, np.maximum(lo - e, e - hi)))
        if best is None or d < best[1]: best = (c, round(float(d), 2))
    return best
out = {}
for n in TOP:
    ps = pieces(n)
    for (mn, V, F) in ps:
        if mn.startswith(('Part', 'Copy of Part')) and 'Resistor' not in mn and 'LCD' not in mn:
            w = centreline(V, F)
            key = n if len(ps) == 1 else f'{n}/{mn}'
            out[key] = dict(mesh=mn, r=w['r'], length=w['length'], a=w['pts'][0].round(2).tolist(), b=w['pts'][-1].round(2).tolist(),
                            cap_a=nearest_cap(w['pts'][0]), cap_b=nearest_cap(w['pts'][-1]), top=round(float(w['pts'][:, 1].max()), 2),
                            reached=f"{w['comp']}/{w['total']}", pts=w['pts'].round(3).tolist())
json.dump(dict(caps=caps, wires=out), open('lac_wires.json', 'w'))
for k, w in out.items():
    print(f"{k:22s} {w['mesh'][:22]:22s} r {w['r']:.2f} L {w['length']:6.1f} {w['reached']:>12s} top {w['top']:6.1f} a {w['a']} {w['cap_a']} b {w['b']} {w['cap_b']}")
