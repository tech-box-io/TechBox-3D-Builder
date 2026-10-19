"""Header-only tree of a GLB: top-level instances, their meshes and world bounds (mm), from accessor min/max."""
import json, struct, sys, collections
import numpy as np
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/tools')
from glbio import node_matrix
path = sys.argv[1]
with open(path, 'rb') as f:
    f.read(12); clen, _ = struct.unpack('<II', f.read(8)); doc = json.loads(f.read(clen))
nodes = doc['nodes']; meshes = doc['meshes']; acc = doc['accessors']
scene = doc['scenes'][doc.get('scene', 0)]
roots = scene['nodes']
print('roots', [nodes[r].get('name') for r in roots], 'nodes', len(nodes), 'meshes', len(meshes))
def walk(i, M, out):
    n = nodes[i]; W = M @ node_matrix(n)
    if 'mesh' in n:
        for p in meshes[n['mesh']]['primitives']:
            a = acc[p['attributes']['POSITION']]
            lo, hi = np.array(a['min']), np.array(a['max'])
            c = np.array([[x, y, z, 1] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]) @ W.T
            out.append((meshes[n['mesh']].get('name') or n.get('name'), c[:, :3].min(0), c[:, :3].max(0), a['count']))
    for c in n.get('children', []):
        walk(c, W, out)
# find the assembly root: descend while a single child
r = roots[0]; M = np.eye(4)
while len(nodes[r].get('children', [])) == 1 and 'mesh' not in nodes[r]:
    M = M @ node_matrix(nodes[r]); r = nodes[r]['children'][0]
M = M @ node_matrix(nodes[r])
print('assembly node', nodes[r].get('name'), 'top-level', len(nodes[r]['children']))
rows = []
for c in nodes[r]['children']:
    out = []; walk(c, M, out)
    if not out:
        rows.append((nodes[c].get('name'), None, None, 0, collections.Counter())); continue
    lo = np.min([o[1] for o in out], 0) * 1000; hi = np.max([o[2] for o in out], 0) * 1000
    names = collections.Counter(o[0] for o in out)
    rows.append((nodes[c].get('name'), lo, hi, sum(o[3] for o in out), names))
for name, lo, hi, nv, names in rows:
    if lo is None:
        print(f'- {name}: no meshes'); continue
    top = ', '.join(f'{k} x{v}' if v > 1 else k for k, v in names.most_common(6))
    print(f'- **{name}**: size {np.round(hi-lo,1).tolist()} at {np.round((hi+lo)/2,1).tolist()}; {sum(names.values())} meshes, {nv} verts: {top}{" ..." if len(names) > 6 else ""}')
