"""Read only parts of a big GLB: the JSON header, then single accessors by seeking (no whole-file load).

    G = Glb(path); G.top() -> {instance name: node index}; G.meshes_of(node) -> [(mesh name, world 4x4 (mm), prim dicts)]
    G.positions(prim) / G.indices(prim) -> numpy arrays (read from disk on demand)
"""
import json, struct, sys
import numpy as np
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/tools')
from glbio import node_matrix, COMPONENT, NCOMP


class Glb:
    def __init__(self, path):
        self.f = open(path, 'rb')
        magic, version, _ = struct.unpack('<III', self.f.read(12))
        clen, _ = struct.unpack('<II', self.f.read(8))
        self.doc = json.loads(self.f.read(clen))
        self.bin0 = 12 + 8 + clen + 8          # file offset of the binary chunk's data
        d = self.doc
        roots = d['scenes'][d.get('scene', 0)]['nodes']
        r, M = roots[0], np.eye(4)
        while len(d['nodes'][r].get('children', [])) == 1 and 'mesh' not in d['nodes'][r]:
            M = M @ node_matrix(d['nodes'][r]); r = d['nodes'][r]['children'][0]
        self.root, self.rootM = r, M @ node_matrix(d['nodes'][r])

    def top(self):
        return {self.doc['nodes'][c].get('name'): c for c in self.doc['nodes'][self.root]['children']}

    def meshes_of(self, node):
        out = []
        def walk(i, M):
            n = self.doc['nodes'][i]; W = M @ node_matrix(n)
            if 'mesh' in n:
                m = self.doc['meshes'][n['mesh']]
                out.append((m.get('name') or n.get('name'), W, m['primitives'], i))
            for c in n.get('children', []):
                walk(c, W)
        walk(node, self.rootM)
        return out

    def acc(self, index):
        a = self.doc['accessors'][index]
        view = self.doc['bufferViews'][a['bufferView']]
        off = self.bin0 + view.get('byteOffset', 0) + a.get('byteOffset', 0)
        n = NCOMP[a['type']]; dt = np.dtype(COMPONENT[a['componentType']])
        stride = view.get('byteStride') or dt.itemsize * n
        self.f.seek(off)
        raw = self.f.read(stride * (a['count'] - 1) + dt.itemsize * n)
        if stride == dt.itemsize * n:
            return np.frombuffer(raw, dtype=dt, count=a['count'] * n).reshape(a['count'], n).copy()
        buf = np.frombuffer(raw + b'\0' * (stride * a['count'] - len(raw)), dtype=np.uint8).reshape(a['count'], stride)
        return np.frombuffer(buf[:, :dt.itemsize * n].tobytes(), dtype=dt).reshape(a['count'], n).copy()

    def world_mesh(self, node):
        """All triangles of a top-level instance in assembly mm: (verts (n,3), faces (m,3), [(mesh name, material, vertex range)])."""
        V, F, info, base = [], [], [], 0
        for name, W, prims, ni in self.meshes_of(node):
            for p in prims:
                v = self.acc(p['attributes']['POSITION']).astype(np.float64)
                v = (np.c_[v, np.ones(len(v))] @ W.T)[:, :3] * 1000.0
                f = self.acc(p['indices']).reshape(-1, 3).astype(np.int64) if 'indices' in p else np.arange(len(v)).reshape(-1, 3)
                V.append(v); F.append(f + base)
                info.append((name, p.get('material'), base, base + len(v)))
                base += len(v)
        return np.vstack(V), np.vstack(F), info
