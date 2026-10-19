"""Load LAC instances' meshes in assembly mm (world), from lac.glb, piece by piece (light: no trimesh scene)."""
import sys, numpy as np
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/tools')
from glbio import read_glb, node_matrix, accessor
GLB = '/Users/lee-johnson/Desktop/Claude_Cadasio/LAC Build Instructions/lac.glb'
doc, blob = read_glb(GLB)
nodes = doc['nodes']
parent = {c: i for i, n in enumerate(nodes) for c in n.get('children', [])}
idx = {n.get('name'): i for i, n in enumerate(nodes)}
root = doc['scenes'][0]['nodes'][0]
TOP = [nodes[c]['name'] for c in nodes[root]['children']]
def world(i):
    m = np.eye(4)
    while i is not None:
        m = node_matrix(nodes[i]) @ m; i = parent.get(i)
    return m
def pieces(name):
    """[(mesh name, V (n,3) mm, F (m,3))] for every mesh under the instance."""
    out = []
    def walk(j):
        n = nodes[j]
        if 'mesh' in n:
            M = world(j)
            m = doc['meshes'][n['mesh']]
            for p in m['primitives']:
                V = accessor(doc, blob, p['attributes']['POSITION']).astype(float)
                F = accessor(doc, blob, p['indices']).reshape(-1, 3).astype(np.int64)
                V = (V @ M[:3, :3].T + M[:3, 3]) * 1000.0
                out.append((m.get('name'), V, F))
        for c in n.get('children', []): walk(c)
    walk(idx[name])
    return out
def mesh(name):
    ps = pieces(name)
    Vs, Fs, off = [], [], 0
    for _, V, F in ps:
        Vs.append(V); Fs.append(F + off); off += len(V)
    return np.vstack(Vs), np.vstack(Fs)
def kabsch(A, B):
    """R, t with B ~ A @ R.T + t."""
    ca, cb = A.mean(0), B.mean(0)
    H = (A - ca).T @ (B - cb)
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1, 1, d])
    R = Vt.T @ D @ U.T
    return R, cb - ca @ R.T
