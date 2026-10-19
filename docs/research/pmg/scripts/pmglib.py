"""Memory-light access to a big GLB: the JSON header plus memory-mapped accessors (no copy of the whole file).

Coordinates returned in mm (GLB metres x 1000), assembly space = the frame of the assembly root node's parent chain,
as tools/stepgen.Model uses it (top-level instance = child of the assembly node).
"""
import json, mmap, struct, sys
import numpy as np
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/tools')
from glbio import node_matrix, COMPONENT, NCOMP


class Glb:
    def __init__(self, path):
        self.f = open(path, 'rb')
        self.mm = mmap.mmap(self.f.fileno(), 0, access=mmap.ACCESS_READ)
        magic, version, _ = struct.unpack_from('<III', self.mm, 0)
        clen, _ = struct.unpack_from('<II', self.mm, 12)
        self.doc = json.loads(bytes(self.mm[20:20 + clen]))
        boff = 20 + clen
        blen, _ = struct.unpack_from('<II', self.mm, boff)
        self.bin_off = boff + 8
        self.nodes = self.doc['nodes']
        self.meshes = self.doc['meshes']
        self.parent = {}
        for i, n in enumerate(self.nodes):
            for c in n.get('children', []):
                self.parent[c] = i
        scene = self.doc['scenes'][self.doc.get('scene', 0)]
        r = scene['nodes'][0]
        M = np.eye(4)
        while len(self.nodes[r].get('children', [])) == 1 and 'mesh' not in self.nodes[r]:
            M = M @ node_matrix(self.nodes[r]); r = self.nodes[r]['children'][0]
        self.root = r
        self.root_M = M @ node_matrix(self.nodes[r])
        self.top = {self.nodes[c].get('name'): c for c in self.nodes[r]['children']}

    def accessor(self, index):
        a = self.doc['accessors'][index]
        view = self.doc['bufferViews'][a['bufferView']]
        offset = self.bin_off + view.get('byteOffset', 0) + a.get('byteOffset', 0)
        n = NCOMP[a['type']]
        dtype = np.dtype(COMPONENT[a['componentType']])
        stride = view.get('byteStride')
        if stride and stride != dtype.itemsize * n:
            raw = np.frombuffer(self.mm, dtype=np.uint8, count=stride * a['count'], offset=offset).reshape(a['count'], stride)
            return np.frombuffer(raw[:, :dtype.itemsize * n].tobytes(), dtype=dtype).reshape(a['count'], n)
        return np.frombuffer(self.mm, dtype=dtype, count=a['count'] * n, offset=offset).reshape(a['count'], n)

    def mesh_nodes(self, top_name):
        """[(node index, node name, mesh index, world 4x4 in metres)] under a top-level instance."""
        out = []
        def walk(i, M):
            W = M @ node_matrix(self.nodes[i])
            if 'mesh' in self.nodes[i]:
                out.append((i, self.nodes[i].get('name'), self.nodes[i]['mesh'], W))
            for c in self.nodes[i].get('children', []):
                walk(c, W)
        walk(self.top[top_name], self.root_M)
        return out

    def subtree(self, top_name):
        """[(node index, depth, name, has_mesh)] of a top-level instance."""
        out = []
        def walk(i, d):
            n = self.nodes[i]
            out.append((i, d, n.get('name'), 'mesh' in n, n.get('mesh')))
            for c in n.get('children', []):
                walk(c, d + 1)
        walk(self.top[top_name], 0)
        return out

    def node_world(self, i):
        chain = []
        while i is not None:
            chain.append(i); i = self.parent.get(i)
        M = np.eye(4)
        for j in reversed(chain):
            M = M @ node_matrix(self.nodes[j])
        return M

    def mesh_geometry(self, mesh_index, W, faces=True):
        """Vertices (mm, world) and faces of one mesh (all primitives)."""
        V, F, off = [], [], 0
        for p in self.meshes[mesh_index]['primitives']:
            v = self.accessor(p['attributes']['POSITION']).astype(np.float64)
            v = (v @ W[:3, :3].T + W[:3, 3]) * 1000.0
            V.append(v)
            if faces and 'indices' in p:
                F.append(self.accessor(p['indices']).reshape(-1, 3).astype(np.int64) + off)
            off += len(v)
        V = np.concatenate(V) if V else np.zeros((0, 3))
        F = np.concatenate(F) if F else np.zeros((0, 3), np.int64)
        return V, F

    def instance_geometry(self, top_name, faces=True, name_filter=None):
        Vs, Fs, off, parts = [], [], 0, []
        for i, name, mi, W in self.mesh_nodes(top_name):
            mname = self.meshes[mi].get('name') or name
            if name_filter and not name_filter(mname, name):
                continue
            v, f = self.mesh_geometry(mi, W, faces)
            parts.append((name, mname, off, off + len(v)))
            Vs.append(v); Fs.append(f + off); off += len(v)
        V = np.concatenate(Vs) if Vs else np.zeros((0, 3))
        F = np.concatenate(Fs) if Fs else np.zeros((0, 3), np.int64)
        return V, F, parts


def kabsch(A, B):
    """Rigid R, t with B ~ A @ R.T + t; returns R, t, rms, max error."""
    ca, cb = A.mean(0), B.mean(0)
    H = (A - ca).T @ (B - cb)
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1, 1, d])
    R = Vt.T @ D @ U.T
    t = cb - ca @ R.T
    err = np.linalg.norm(A @ R.T + t - B, axis=1)
    return R, t, float(np.sqrt((err ** 2).mean())), float(err.max())


def pose_from(R, t, at):
    """stepgen pose {t, r, at}: a point p of the built copy goes to (p - at) @ R.T + at + t."""
    from scipy.spatial.transform import Rotation
    at = np.asarray(at, float)
    tt = R @ at + t - at
    rv = Rotation.from_matrix(R).as_rotvec()
    ang = float(np.linalg.norm(rv))
    if ang < 1e-7:
        return [round(float(x), 2) for x in tt]
    ax = rv / ang
    return dict(t=[round(float(x), 2) for x in tt], r=[round(float(x), 6) for x in ax] + [round(float(np.degrees(ang)), 3)],
                at=[round(float(x), 2) for x in at])
