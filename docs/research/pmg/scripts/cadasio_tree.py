"""PMG: the Cadasio project's CAD tree and the GLB's top-level instances, side by side (mm, assembly frame).

    .venv.nosync/bin/python docs/research/pmg/scripts/cadasio_tree.py

Writes docs/research/pmg/scripts/work/cadasio_map/cadasio_tree.json (every Cadasio top-level component: name, idx, hidden flag,
transform in mm, world box in mm, its solids) and work/cadasio_map/glb_boxes.json (every NAUO: world box in mm, matrix in mm,
mesh names). Reads the GLB header only (no mesh data).
"""
import json, struct, sys, os, collections
import numpy as np
ROOT = '/Users/lee-johnson/Desktop/Claude_Cadasio'
sys.path.insert(0, ROOT + '/tools')
from glbio import node_matrix
PAY = ROOT + '/docs/research/pmg/cadasio/raw/19075-piano_memory_game_pmg-full_build.json'
GLB = ROOT + '/PMG Build Instructions/pmg.glb'
WORK = ROOT + '/docs/research/pmg/scripts/work/cadasio_map'
os.makedirs(WORK, exist_ok=True)


def cad_matrix(s, mm):
    """Cadasio transform string (column-major 4x4, translation in scene units) -> 4x4 with translation in mm."""
    t = [float(x) for x in s.split(',')]
    M = np.array(t).reshape(4, 4).T
    M[:3, 3] *= mm
    return M


def box_corners(lo, hi):
    return np.array([[x, y, z, 1.0] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])


def cadasio_tree():
    j = json.load(open(PAY))
    A = j['assemblyStructure']; rv = A['rootVersions']; MM = 1.0 / A['scaleFactor']
    tops = []

    def walk(n, M, out, path):
        r = n['rootReference']
        W = M @ cad_matrix(r['transform'], MM) if r.get('transform') else M
        kids = n.get('children') or []
        if not kids:
            v = rv.get(r['childVersionId'])
            if v:
                lo = np.array([v['versionMin' + a] for a in 'XYZ']) * MM; hi = np.array([v['versionMax' + a] for a in 'XYZ']) * MM
                c = box_corners(lo, hi) @ W.T
                out.append(dict(id=r['id'], name=r['name'].split('/')[-1], path=path + [r['name'].split('/')[-1]], hidden=bool(r.get('hidden')),
                                min=c[:, :3].min(0).round(2).tolist(), max=c[:, :3].max(0).round(2).tolist(),
                                kd=(v.get('versionMtlData') or '')[:0]))
        for c in kids:
            walk(c, W, out, path + [r['name'].split('/')[-1]])

    for c in A['children']:
        r = c['rootReference']
        M = cad_matrix(r['transform'], MM)
        out = []
        walk(c, np.eye(4), out, [])
        lo = np.min([o['min'] for o in out], 0) if out else None; hi = np.max([o['max'] for o in out], 0) if out else None
        tops.append(dict(id=r['id'], name=r['name'], idx=r.get('idx'), hidden=bool(r.get('hidden')), matrix_mm=M.round(4).tolist(),
                         min=None if lo is None else lo.round(2).tolist(), max=None if hi is None else hi.round(2).tolist(),
                         nsolids=len(out), solids=[dict(id=o['id'], name=o['name'], sub=o['path'][1] if len(o['path']) > 2 else None, hidden=o['hidden'],
                                                        min=o['min'], max=o['max']) for o in out]))
    json.dump(dict(scale_mm_per_unit=MM, tops=tops), open(WORK + '/cadasio_tree.json', 'w'))
    return tops, MM


def glb_boxes():
    with open(GLB, 'rb') as f:
        f.read(12); clen, _ = struct.unpack('<II', f.read(8)); doc = json.loads(f.read(clen))
    nodes = doc['nodes']; meshes = doc['meshes']; acc = doc['accessors']
    root = [i for i, n in enumerate(nodes) if n.get('name') == 'PMG Full 3D Cadasio Build'][0]
    S = np.diag([1000.0, 1000.0, 1000.0, 1.0])
    rows = {}

    def walk(i, M, out):
        n = nodes[i]; W = M @ node_matrix(n)
        if 'mesh' in n:
            for p in meshes[n['mesh']]['primitives']:
                a = acc[p['attributes']['POSITION']]
                c = box_corners(a['min'], a['max']) @ (S @ W).T
                out.append((meshes[n['mesh']].get('name') or n.get('name'), c[:, :3].min(0), c[:, :3].max(0), a['count'], n.get('name')))
        for ch in n.get('children', []):
            walk(ch, W, out)
    for c in nodes[root]['children']:
        out = []; walk(c, np.eye(4), out)
        M = node_matrix(nodes[c]).copy(); M[:3, 3] *= 1000.0
        lo = np.min([o[1] for o in out], 0); hi = np.max([o[2] for o in out], 0)
        rows[nodes[c]['name']] = dict(node=c, min=lo.round(2).tolist(), max=hi.round(2).tolist(), matrix_mm=M.round(4).tolist(),
                                      meshes=[dict(name=o[0], node=o[4], min=o[1].round(2).tolist(), max=o[2].round(2).tolist(), verts=o[3]) for o in out])
    json.dump(rows, open(WORK + '/glb_boxes.json', 'w'))
    return rows


if __name__ == '__main__':
    tops, MM = cadasio_tree()
    g = glb_boxes()
    print('cadasio tops', len(tops), 'mm/unit', MM, 'glb tops', len(g))
    names = collections.Counter(t['name'].rsplit('-', 1)[0] for t in tops)
    print(names.most_common(80))
