"""Pass 1: split every wire-like body of pmg.glb into connected solids (vertices welded at 0.001 mm) and list them."""
import sys, json
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from wp_glb import Glb

GLB = '/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions/pmg.glb'


def wire_instances(G):
    out = []
    for name, node in G.top().items():
        ms = G.meshes_of(node)
        if len(ms) == 1 and (ms[0][0].startswith('Part') or ms[0][0].startswith('Copy')):
            out.append((name, ms[0][0].split('^')[0]))
    return sorted(out, key=lambda x: int(x[0][4:]))


def split(V, F):
    key = np.round(V, 3)
    _, inv = np.unique(key, axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    e = np.r_[F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]
    e = inv[e]
    n = inv.max() + 1
    A = coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(n, n))
    k, lab = connected_components(A, directed=False)
    return k, lab[inv], inv


if __name__ == '__main__':
    G = Glb(GLB)
    res = {}
    for inst, mesh in wire_instances(G):
        V, F, info = G.world_mesh(G.top()[inst])
        k, lab, _ = split(V, F)
        comps = []
        for c in range(k):
            P = V[lab == c]
            lo, hi = P.min(0), P.max(0)
            comps.append(dict(n=int(len(P)), lo=np.round(lo, 2).tolist(), hi=np.round(hi, 2).tolist()))
        comps.sort(key=lambda c: -c['n'])
        res[inst] = dict(mesh=mesh, solids=comps)
        print(inst, mesh, k, [c['n'] for c in comps][:12])
    json.dump(res, open('/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/bc7f208e-dd24-481f-9696-6a220688eb27/scratchpad/components.json', 'w'), indent=0)
