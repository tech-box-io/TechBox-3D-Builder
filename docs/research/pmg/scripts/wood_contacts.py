"""Which wood parts touch / pass into which: for every pair, the share of A's surface samples inside B, the deepest, and the
share within 0.15 mm of B's surface. Also overall bounds (table height)."""
import sys, json, numpy as np, trimesh
SP = sys.argv[1]
d = np.load(SP + '/wood.npz')
B = json.load(open(SP + '/wood_basic.json'))
ids = list(B)
M = {}
for i in ids:
    m = trimesh.Trimesh(d[i + '__V'], d[i + '__F'], process=True)
    m.merge_vertices()
    M[i] = m
    print(i, B[i]['name'], 'watertight', m.is_watertight, 'volume', round(m.volume, 1) if m.is_watertight else None)
lo = np.min([m.bounds[0] for m in M.values()], 0); hi = np.max([m.bounds[1] for m in M.values()], 0)
print('all wood bounds', lo.round(2), hi.round(2))
for i in ids:
    print('  ', i, B[i]['name'], 'y from', round(M[i].bounds[0][1], 2), 'to', round(M[i].bounds[1][1], 2))
res = []
rng = np.random.default_rng(0)
for a in ids:
    pa, _ = trimesh.sample.sample_surface_even(M[a], 6000, seed=1)
    for b in ids:
        if a == b:
            continue
        bl, bh = M[b].bounds
        near = np.all((pa >= bl - 0.3) & (pa <= bh + 0.3), axis=1)
        if not near.any():
            continue
        q = pa[near]
        cp, dist, _ = trimesh.proximity.closest_point(M[b], q)
        inside = M[b].contains(q)
        sd = np.where(inside, dist, -dist)
        touch = (np.abs(sd) < 0.15).sum()
        deep = sd[inside].max() if inside.any() else 0.0
        if touch or inside.any():
            sel = q[(np.abs(sd) < 0.15) | inside]
            res.append(dict(a=a, an=B[a]['name'], b=b, bn=B[b]['name'], n_touch=int(touch), n_inside=int(inside.sum()), max_depth=round(float(deep), 3),
                            region_lo=sel.min(0).round(1).tolist(), region_hi=sel.max(0).round(1).tolist()))
            print(f"{B[a]['name']:>6} -> {B[b]['name']:<6} touch {touch:5d} inside {int(inside.sum()):5d} depth {deep:.3f} region {sel.min(0).round(1).tolist()} {sel.max(0).round(1).tolist()}")
json.dump(dict(bounds=[lo.tolist(), hi.tolist()], pairs=res), open(SP + '/wood_contacts.json', 'w'), indent=1)
