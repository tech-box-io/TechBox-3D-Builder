"""PMG: which USB plug ends each USB cable body in pmg.glb touches (vertices within 1 mm of the end's box)."""
import json, mmap, struct, sys
import numpy as np
ROOT = '/Users/lee-johnson/Desktop/Claude_Cadasio'
sys.path.insert(0, ROOT + '/tools')
from glbio import node_matrix, COMPONENT, NCOMP
G = json.load(open(ROOT + '/docs/research/pmg/scripts/work/cadasio_map/glb_boxes.json'))
f = open(ROOT + '/PMG Build Instructions/pmg.glb', 'rb'); mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
clen, _ = struct.unpack_from('<II', mm, 12); doc = json.loads(bytes(mm[20:20 + clen])); bo = 20 + clen + 8
def acc(i):
    a = doc['accessors'][i]; v = doc['bufferViews'][a['bufferView']]; n = NCOMP[a['type']]; dt = np.dtype(COMPONENT[a['componentType']])
    return np.frombuffer(mm, dtype=dt, count=a['count'] * n, offset=bo + v.get('byteOffset', 0) + a.get('byteOffset', 0)).reshape(a['count'], n)
def pts(k):
    out = []
    def walk(i, M):
        W = M @ node_matrix(doc['nodes'][i])
        if 'mesh' in doc['nodes'][i]:
            for p in doc['meshes'][doc['nodes'][i]['mesh']]['primitives']:
                P = acc(p['attributes']['POSITION']).astype(float); out.append((P @ W[:3, :3].T + W[:3, 3]) * 1000)
        for c in doc['nodes'][i].get('children', []): walk(c, W)
    walk(G[k]['node'], np.eye(4)); return np.vstack(out)
for body in ('NAUO277', 'NAUO284', 'NAUO285'):
    P = pts(body)
    hits = []
    for end in ('NAUO278', 'NAUO279', 'NAUO280', 'NAUO281', 'NAUO282', 'NAUO283'):
        lo = np.array(G[end]['min']) - 1; hi = np.array(G[end]['max']) + 1
        n = int(np.count_nonzero(np.all((P >= lo) & (P <= hi), axis=1)))
        if n: hits.append((end, n))
    print(body, G[body]['meshes'][0]['name'][:20], 'touches', hits)
