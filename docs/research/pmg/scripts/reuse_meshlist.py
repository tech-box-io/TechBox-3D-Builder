"""List the mesh nodes under named instances of a GLB (header only): node name, mesh name, own box size (mm), vertex count.

    .venv.nosync/bin/python docs/research/pmg/scripts/reuse_meshlist.py <glb> <instance> [<instance> ...]
"""
import collections
import sys

sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from reuse_hdr import Glb  # noqa: E402

H = Glb(sys.argv[1])
for name in sys.argv[2:]:
    for i in H.find(name):
        rows = H.mesh_nodes(i)
        print(f'== {name} (node {i}): {len(rows)} mesh nodes, {sum(r[4] for r in rows)} verts; parent {H.nodes[H.parent.get(i, i)].get("name")}')
        # the sub-assemblies directly under it
        for c in H.nodes[i].get('children', []):
            sub = H.mesh_nodes(c)
            print(f'   child {H.nodes[c].get("name")!r}: {len(sub)} mesh nodes, {sum(r[4] for r in sub)} verts')
        cnt = collections.Counter((r[1], tuple(round(float(x), 2) for x in (r[3] - r[2]))) for r in rows)
        for (m, size), c in sorted(cnt.items()):
            v = next(r[4] for r in rows if r[1] == m)
            print(f'     {m!r} x{c}  own size {list(size)}  {v} verts')
