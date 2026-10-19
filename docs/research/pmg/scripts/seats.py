"""Where each built electronic part sits in the case: which wood parts it touches (vertices within 0.3 mm of a wood surface) or
passes into (vertices inside a wood part, with the depth), and where (box of those vertices), per mesh of the part. Also the
straight ways out (stepgen's blocked(), electronics against the wood only, the part's vertices against the wood)."""
import sys, json, numpy as np, trimesh
from scipy.spatial import cKDTree
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from pmglib import Glb
SP = sys.argv[1]
d = np.load(SP + '/wood.npz')
W = {}
for k in d.files:
    if k.endswith('__V'):
        i = k[:-3]; m = trimesh.Trimesh(d[i + '__V'], d[i + '__F'], process=True); m.merge_vertices(); W[i] = m
WN = {'NAUO63': 'H1', 'NAUO65': 'H2', 'NAUO66': 'H3', 'NAUO73': 'H4', 'NAUO67': 'H5', 'NAUO60': 'H6', 'NAUO68': 'H7', 'NAUO61': 'H8',
      'NAUO72': 'key1', 'NAUO71': 'key2', 'NAUO70': 'key3', 'NAUO69': 'key4', 'NAUO64': 'H10', 'NAUO62': 'H11', 'NAUO77': 'H12', 'NAUO75': 'H13', 'NAUO74': 'H14'}
g = Glb('/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions/pmg.glb')
out = {}
for inst in sys.argv[2:]:
    rows = []
    for i, name, mi, Wm in g.mesh_nodes(inst):
        v, _ = g.mesh_geometry(mi, Wm, faces=False)
        v = np.unique(np.round(v, 3), axis=0)
        mn = g.meshes[mi].get('name')
        for wi, wm in W.items():
            lo, hi = wm.bounds
            near = np.all((v >= lo - 0.35) & (v <= hi + 0.35), axis=1)
            if not near.any(): continue
            q = v[near]
            dist = trimesh.proximity.closest_point(wm, q)[1]
            ins = wm.contains(q)
            touch = (dist < 0.3) | ins
            if not touch.any(): continue
            deep = float(dist[ins].max()) if ins.any() else 0.0
            rows.append(dict(mesh=mn, node=name, wood=WN[wi], n_touch=int(touch.sum()), n_inside=int(ins.sum()), max_depth=round(deep, 2),
                             lo=q[touch].min(0).round(2).tolist(), hi=q[touch].max(0).round(2).tolist()))
    out[inst] = rows
    print('==', inst)
    for r in rows:
        print(f"   {r['mesh'][:40]:40s} {r['node']:8s} -> {r['wood']:5s} touch {r['n_touch']:5d} inside {r['n_inside']:5d} depth {r['max_depth']:.2f}  {r['lo']} .. {r['hi']}")
json.dump(out, open(SP + '/seats_' + '_'.join(sys.argv[2:]) + '.json', 'w'), indent=1)
