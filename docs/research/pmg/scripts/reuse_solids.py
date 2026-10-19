"""The solids (connected components after welding, as tools/build_model.py numbers them: largest first by vertex count is
NOT its order; build_model ranks by size, see colour_components) of each distinct mesh under the named PMG instances.

    .venv.nosync/bin/python docs/research/pmg/scripts/reuse_solids.py NAUO76 NAUO79 ...

Reads only those meshes' accessors (memory-mapped). Prints per mesh: vertex and triangle counts, then each solid's own-frame box
size (mm, sorted thin / mid / long), its box, and its share of the mesh's triangles.
"""
import sys

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from reuse_hdr import Glb  # noqa: E402

ROOT = '/Users/lee-johnson/Desktop/Claude_Cadasio/'
H = Glb(sys.argv[1] if sys.argv[1].endswith('.glb') else ROOT + 'PMG Build Instructions/pmg.glb')
names = sys.argv[2:] if sys.argv[1].endswith('.glb') else sys.argv[1:]
MAXSHOW = int(__import__("os").environ.get("MAXSHOW", 40))


def solids(V, F):
    q = np.round(V / 1e-6).astype(np.int64)                      # weld at 1 micrometre (file units: metres -> 0.001 mm)
    _, inv = np.unique(q, axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    Fw = inv[F]
    n = inv.max() + 1
    e = np.concatenate([Fw[:, [0, 1]], Fw[:, [1, 2]]])
    g = coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(n, n))
    k, lab = connected_components(g, directed=False)
    return k, lab, inv


seen = set()
for inst in names:
    for (node, mname, lo, hi, cnt, W) in H.mesh_nodes(H.find(inst)[0]):
        mi = H.nodes[node]['mesh']
        if (mname, cnt) in seen:
            continue
        seen.add((mname, cnt))
        (V, idx), = H.triangles(mi)
        F = idx.reshape(-1, 3).astype(np.int64)
        k, lab, inv = solids(V.astype(np.float64), F)
        Vmm = V.astype(np.float64) * 1000
        rows = []
        face_lab = lab[inv[F[:, 0]]]
        for c in range(k):
            sel = np.zeros(len(V), bool)
            sel[np.isin(lab[inv], [c])] = True
            P = Vmm[sel]
            ext = P.max(0) - P.min(0)
            rows.append((int(sel.sum()), np.sort(ext), P.min(0), P.max(0), float((face_lab == c).mean())))
        print(f'== {inst} mesh {mname!r}: {len(V)} verts, {len(F)} tris, {k} solids; own box {np.round(lo, 2).tolist()} .. {np.round(hi, 2).tolist()}')
        order = sorted(range(k), key=lambda c: -np.prod(np.maximum(rows[c][1], 1e-3)))
        for r, c in enumerate(order[:MAXSHOW]):
            n, ext, a, b, share = rows[c]
            print(f'   rank {r:3d}: {n:6d} v  thin/mid/long {np.round(ext, 2).tolist()}  box {np.round(a, 2).tolist()} .. {np.round(b, 2).tolist()}  {share * 100:.1f} % tris')
        if k > MAXSHOW:
            ext = np.array([rows[c][1] for c in order[MAXSHOW:]])
            print(f'   ... {k - MAXSHOW} more, thin/mid/long from {np.round(ext.min(0), 2).tolist()} to {np.round(ext.max(0), 2).tolist()}')
