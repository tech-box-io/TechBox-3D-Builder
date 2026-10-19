"""Split small connector meshes into connected pieces (each pin, each plastic block) and print each piece's box, main axis and
its two end points, so the pin tips and the way they point can be read. Usage: pin_parts.py INSTANCE MESHNAME [MESHNAME ...]"""
import sys, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from pmglib import Glb
g = Glb('/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions/pmg.glb')
inst, wanted = sys.argv[1], sys.argv[2:]
for i, name, mi, W in g.mesh_nodes(inst):
    mn = g.meshes[mi].get('name')
    if not any(w in mn for w in wanted):
        continue
    V, F = g.mesh_geometry(mi, W)
    # weld coincident vertices first
    key = np.round(V / 1e-3).astype(np.int64)
    _, inv = np.unique(key, axis=0, return_inverse=True); inv = inv.reshape(-1)
    Fw = inv[F]
    n = inv.max() + 1
    rows = np.concatenate([Fw[:, 0], Fw[:, 1], Fw[:, 2]]); cols = np.concatenate([Fw[:, 1], Fw[:, 2], Fw[:, 0]])
    ncomp, lab = connected_components(coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n)), directed=False)
    Vw = np.zeros((n, 3)); Vw[inv] = V
    print(f'== {inst} {name} {mn}: {len(V)} verts, {ncomp} pieces')
    for c in range(ncomp):
        P = Vw[lab == c]
        lo, hi = P.min(0), P.max(0)
        C = P - P.mean(0); u, s, vt = np.linalg.svd(C, full_matrices=False)
        ax = vt[0]; t = C @ ax
        print(f'   piece {c}: {len(P)} v box {lo.round(2).tolist()} {hi.round(2).tolist()} size {(hi-lo).round(2).tolist()} axis {ax.round(3).tolist()} ends {P[t.argmin()].round(2).tolist()} {P[t.argmax()].round(2).tolist()}')
