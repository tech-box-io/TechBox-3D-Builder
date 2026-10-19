"""Where the loose Nanos NAUO2 / NAUO3 (one mesh each, 'nano_Varsayilan') sit against the Nano inside the module assemblies:
the built module NAUO78's Nano (node NAUO301: nano-board, headers, chips) carried to the bench module NAUO1's pose, then nearest
distances to NAUO3's vertices, and an ICP refinement."""
import sys, json, numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from pmglib import Glb, kabsch, pose_from
SP = sys.argv[1]
g = Glb('/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions/pmg.glb')
C = json.load(open(SP + '/copies.json'))
def M(pose):
    from scipy.spatial.transform import Rotation
    if isinstance(pose, list):
        T = np.eye(4); T[:3, 3] = pose; return T
    ax = np.array(pose['r'][:3]); ang = np.radians(pose['r'][3])
    R = Rotation.from_rotvec(ax / np.linalg.norm(ax) * ang).as_matrix()
    at = np.array(pose['at']); T = np.eye(4); T[:3, :3] = R; T[:3, 3] = at - R @ at + np.array(pose['t']); return T
# Nano subtree of NAUO78
idx = [i for i, d, n, hm, mi in g.subtree('NAUO78') if n == 'NAUO301'][0]
print('NAUO301 node index in NAUO78:', idx, ' NAUO94 Nano index:', [i for i, d, n, hm, mi in g.subtree('NAUO94') if n == 'NAUO301'])
pts, names = [], []
def walk(i, W):
    from glbio import node_matrix
    W = W @ node_matrix(g.nodes[i])
    if 'mesh' in g.nodes[i]:
        v, _ = g.mesh_geometry(g.nodes[i]['mesh'], W, faces=False); pts.append(v); names.append(g.meshes[g.nodes[i]['mesh']].get('name'))
    for c in g.nodes[i].get('children', []):
        walk(c, W)
Wp = g.node_world(g.parent[idx])
walk(idx, Wp)
P = np.concatenate(pts)
lo, hi = P.min(0), P.max(0)
print('built Nano (NAUO301 in NAUO78) box', lo.round(2), hi.round(2), 'size', (hi - lo).round(2), 'meshes', len(names))
T = M(C['io_module']['NAUO1']['pose'])
Pb = P @ T[:3, :3].T + T[:3, 3]
N3, _, _ = g.instance_geometry('NAUO3', faces=False)
print('NAUO3 box', N3.min(0).round(2), N3.max(0).round(2))
print('built Nano carried to bench pose: box', Pb.min(0).round(2), Pb.max(0).round(2))
tree = cKDTree(N3)
sub = Pb[::7]
dist, _ = tree.query(sub)
print('nearest distance carried Nano -> NAUO3: median', np.median(dist).round(3), '90%', np.percentile(dist, 90).round(3), 'max', dist.max().round(3))
# ICP: carried Nano points onto NAUO3
Q = sub.copy(); Ttot = np.eye(4)
for it in range(30):
    d, j = tree.query(Q)
    keep = d < max(1.0, np.percentile(d, 80))
    R, t, rms, mx = kabsch(Q[keep], N3[j[keep]])
    Q = Q @ R.T + t
    S = np.eye(4); S[:3, :3] = R; S[:3, 3] = t; Ttot = S @ Ttot
d, _ = tree.query(Q)
print('after ICP: correction', pose_from(Ttot[:3, :3], Ttot[:3, 3], Pb.mean(0)), 'median', np.median(d).round(3), '90%', np.percentile(d, 90).round(3))
# the built Nano's pins: direction and USB end, by its header meshes
json.dump(dict(built_nano_node='NAUO301', built_nano_box=[lo.round(2).tolist(), hi.round(2).tolist()], meshes=names,
               carried_to_bench_vs_NAUO3=dict(median=float(np.median(dist)), p90=float(np.percentile(dist, 90)), max=float(dist.max())),
               icp_correction=pose_from(Ttot[:3, :3], Ttot[:3, 3], Pb.mean(0))), open(SP + '/nano_check.json', 'w'), indent=1)
# translation-only test (the boxes say NAUO3 = carried Nano + about 15.2 mm in Y)
shift = (N3.min(0) + N3.max(0)) / 2 - (Pb.min(0) + Pb.max(0)) / 2
d2, _ = tree.query(sub + shift)
print('pure shift', shift.round(2), 'nearest: median', np.median(d2).round(3), '90%', np.percentile(d2, 90).round(3), 'max', d2.max().round(3))
for ang in (180,):
    from scipy.spatial.transform import Rotation
    c = (Pb.min(0) + Pb.max(0)) / 2
    R = Rotation.from_rotvec([0, np.radians(ang), 0]).as_matrix()
    d3, _ = tree.query((sub - c) @ R.T + c + shift)
    print('  same but turned 180 about Y: median', np.median(d3).round(3))
