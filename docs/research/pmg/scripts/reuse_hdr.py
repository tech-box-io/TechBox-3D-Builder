"""GLB header helpers for the PMG reuse study: the JSON chunk only (never the binary), node world matrices, and per mesh node
its name, own-frame box (accessor min/max) and vertex count. Geometry is read only where asked, through a memory map, so a
167 MB file costs no more than the pages actually touched.

    import hdr; H = hdr.Glb(path); H.top()  ->  {instance name: node index}
"""
import json
import mmap
import struct
import sys

import numpy as np

sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/tools')
from glbio import node_matrix, COMPONENT, NCOMP  # noqa: E402


class Glb:
    def __init__(self, path):
        self.path = path
        with open(path, 'rb') as f:
            magic, version, _ = struct.unpack('<III', f.read(12))
            clen, _ = struct.unpack('<II', f.read(8))
            self.doc = json.loads(f.read(clen))
            self.bin_offset = 12 + 8 + clen + 8
        self.nodes = self.doc['nodes']
        self.parent = {c: i for i, n in enumerate(self.nodes) for c in n.get('children', [])}
        self._world = {}

    def world(self, i):
        """World matrix (the export's units, metres for STEP exports) of node i."""
        if i not in self._world:
            p = self.parent.get(i)
            self._world[i] = (self.world(p) if p is not None else np.eye(4)) @ node_matrix(self.nodes[i])
        return self._world[i]

    def assembly(self):
        """The assembly node: the scene root followed down while it has a single child and no mesh (as tree.py)."""
        r = self.doc['scenes'][self.doc.get('scene', 0)]['nodes'][0]
        while len(self.nodes[r].get('children', [])) == 1 and 'mesh' not in self.nodes[r]:
            r = self.nodes[r]['children'][0]
        return r

    def top(self):
        a = self.assembly()
        return {self.nodes[c].get('name'): c for c in self.nodes[a].get('children', [])}

    def find(self, name):
        return [i for i, n in enumerate(self.nodes) if n.get('name') == name]

    def subtree(self, i):
        out, todo = [], [i]
        while todo:
            k = todo.pop(0)
            out.append(k)
            todo += self.nodes[k].get('children', [])
        return out

    def mesh_nodes(self, i):
        """[(node index, mesh name, own box lo (mm), own box hi (mm), vertex count, world matrix with t in mm)] under node i."""
        res = []
        for k in self.subtree(i):
            n = self.nodes[k]
            if 'mesh' not in n:
                continue
            m = self.doc['meshes'][n['mesh']]
            los, his, cnt = [], [], 0
            for p in m['primitives']:
                a = self.doc['accessors'][p['attributes']['POSITION']]
                los.append(a['min']); his.append(a['max']); cnt += a['count']
            W = self.world(k).copy()
            W[:3, 3] *= 1000.0
            res.append((k, m.get('name') or n.get('name'), np.min(los, 0) * 1000, np.max(his, 0) * 1000, cnt, W))
        return res

    def positions(self, mesh_index):
        """All POSITION arrays of a mesh (own frame, file units), read through a memory map (a copy, small)."""
        out = []
        with open(self.path, 'rb') as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            try:
                for p in self.doc['meshes'][mesh_index]['primitives']:
                    out.append(self._acc(mm, p['attributes']['POSITION']))
            finally:
                mm.close()
        return out

    def triangles(self, mesh_index):
        """[(positions, indices)] per primitive."""
        out = []
        with open(self.path, 'rb') as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            try:
                for p in self.doc['meshes'][mesh_index]['primitives']:
                    out.append((self._acc(mm, p['attributes']['POSITION']), self._acc(mm, p['indices']).reshape(-1)))
            finally:
                mm.close()
        return out

    def _acc(self, mm, index):
        a = self.doc['accessors'][index]
        view = self.doc['bufferViews'][a['bufferView']]
        off = self.bin_offset + view.get('byteOffset', 0) + a.get('byteOffset', 0)
        n = NCOMP[a['type']]
        dt = np.dtype(COMPONENT[a['componentType']])
        stride = view.get('byteStride') or dt.itemsize * n
        raw = np.frombuffer(mm, dtype=np.uint8, count=stride * (a['count'] - 1) + dt.itemsize * n, offset=off)
        if stride == dt.itemsize * n:
            return raw.view(dt).reshape(a['count'], n).copy()
        rows = np.lib.stride_tricks.as_strided(raw, shape=(a['count'], dt.itemsize * n), strides=(stride, 1))
        return rows.copy().view(dt).reshape(a['count'], n)


def rigid_fit(P, Q):
    """R, t with Q ~ R P + t (Kabsch), and the worst residual."""
    P, Q = np.asarray(P, float), np.asarray(Q, float)
    cp, cq = P.mean(0), Q.mean(0)
    U, _, Vt = np.linalg.svd((P - cp).T @ (Q - cq))
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1, 1, d]) @ U.T
    t = cq - R @ cp
    return R, t, float(np.max(np.linalg.norm((P @ R.T + t) - Q, axis=1)))
