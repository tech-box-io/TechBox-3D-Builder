"""Which way each case part can come off (stepgen's own blocked() test, its default settings), in the Cadasio build order, with
only the parts placed before it present. Also the Cadasio guide's direction for that step (the side the part hovers on)."""
import sys, json, numpy as np, trimesh
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/tools')
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
import stepgen
from pmglib import Glb
SP = sys.argv[1]
cfg = dict(stepgen.DEFAULTS)
d = np.load(SP + '/wood.npz')
M = {}
for k in d.files:
    if k.endswith('__V'):
        i = k[:-3]; m = trimesh.Trimesh(d[i + '__V'], d[i + '__F'], process=True); m.merge_vertices(); M[i] = m
g = Glb('/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions/pmg.glb')
def load(i):
    V, F, _ = g.instance_geometry(i); m = trimesh.Trimesh(V, F, process=True); m.merge_vertices(); return m
for i in ['NAUO76', 'NAUO83', 'NAUO84', 'NAUO85', 'NAUO79', 'NAUO81', 'NAUO78']:
    M[i] = load(i)
N = {'NAUO63': 'H1', 'NAUO65': 'H2', 'NAUO66': 'H3', 'NAUO73': 'H4', 'NAUO67': 'H5', 'NAUO60': 'H6', 'NAUO68': 'H7', 'NAUO61': 'H8',
     'NAUO72': 'key (H9, -Z end)', 'NAUO71': 'key 2', 'NAUO70': 'key 3', 'NAUO69': 'key 4', 'NAUO64': 'H10', 'NAUO62': 'H11', 'NAUO77': 'H12',
     'NAUO75': 'H13', 'NAUO74': 'H14', 'NAUO76': 'button black', 'NAUO83': 'button yellow', 'NAUO84': 'button white', 'NAUO85': 'button blue',
     'NAUO79': 'display', 'NAUO81': 'matrix', 'NAUO78': 'I/O module'}
CAD = {'NAUO65': [1, 0, 0], 'NAUO66': [1, 0, 0], 'NAUO73': [1, 0, 0], 'NAUO67': [0.006, -0.73, -0.69], 'NAUO60': [0.007, -0.59, -0.81],
       'NAUO68': [0.015, -0.21, -0.98], 'NAUO61': [0, 1, 0], 'NAUO72': [-1, 0, 0], 'NAUO64': [-0.98, 0.205, 0], 'NAUO62': [-0.125, 0.99, 0],
       'NAUO77': [-0.17, 0.985, 0], 'NAUO75': [-0.766, 0.643, 0], 'NAUO74': [0.26, 0.96, 0.0]}
ORDER = [('NAUO65', ['NAUO63']), ('NAUO66', ['NAUO63', 'NAUO65']), ('NAUO73', ['NAUO63', 'NAUO65', 'NAUO66']),
         ('NAUO67', ['NAUO63', 'NAUO65', 'NAUO66', 'NAUO73']), ('NAUO60', ['NAUO63', 'NAUO65', 'NAUO66', 'NAUO73', 'NAUO67'])]
base = ['NAUO63', 'NAUO65', 'NAUO66', 'NAUO73', 'NAUO67', 'NAUO60']
ORDER += [(b, base) for b in ['NAUO76', 'NAUO83', 'NAUO84', 'NAUO85']]
base = base + ['NAUO76', 'NAUO83', 'NAUO84', 'NAUO85']
ORDER += [('NAUO68', base)]; base = base + ['NAUO68']
ORDER += [('NAUO61', base)]; base = base + ['NAUO61']
ORDER += [('NAUO72', base)]; base2 = base + ['NAUO72', 'NAUO71', 'NAUO70', 'NAUO69']
ORDER += [('NAUO71', base + ['NAUO72'])]
ORDER += [('NAUO64', base2)]; base2 = base2 + ['NAUO64']
ORDER += [('NAUO62', base2)]; base2 = base2 + ['NAUO62']
ORDER += [('NAUO77', base2)]; base2 = base2 + ['NAUO77']
ORDER += [('NAUO75', base2)]; base2 = base2 + ['NAUO75']
ORDER += [('NAUO78', base2)]; base2 = base2 + ['NAUO78']
ORDER += [('NAUO79', base2)]; base2 = base2 + ['NAUO79']
ORDER += [('NAUO81', base2)]; base2 = base2 + ['NAUO81']
ORDER += [('NAUO74', base2)]
ORDER += [('NAUO74', [b for b in base2 if b != 'NAUO81'] )]
NAMES = {(1, 0, 0): '+X', (-1, 0, 0): '-X', (0, 1, 0): '+Y', (0, -1, 0): '-Y', (0, 0, 1): '+Z', (0, 0, -1): '-Z'}
res = []
extra = {'NAUO75': [[-0.766, 0.643, 0], [0.643, 0.766, 0]], 'NAUO74': [[0.766, -0.643, 0], [-0.766, 0.643, 0], [0.643, 0.766, 0]],
         'NAUO79': [[0.643, 0.766, 0], [-0.766, 0.643, 0]], 'NAUO81': [[-0.643, -0.766, 0], [-0.766, 0.643, 0], [0.643, 0.766, 0]]}
for mov, sta in ORDER:
    m = M[mov]; s = trimesh.util.concatenate([M[x] for x in sta])
    reach = max(25.0, 0.8 * float(np.linalg.norm(m.extents))) + 5
    free = []
    dirs = [np.array(a, float) for a in stepgen.AXES] + [np.array(v, float) / np.linalg.norm(v) for v in extra.get(mov, [])]
    if mov in CAD:
        dirs.append(np.array(CAD[mov], float) / np.linalg.norm(CAD[mov]))
    out = {}
    for dvec in dirs:
        b = stepgen.blocked(m, s, dvec, reach, cfg)
        key = NAMES.get(tuple(np.round(dvec).astype(int)), None) if np.allclose(np.abs(dvec).max(), 1) else None
        key = key or str(np.round(dvec, 3).tolist())
        out[key] = 'blocked' if b else 'FREE'
    r = dict(moving=mov, name=N[mov], stationary=[N[x] for x in sta], reach_mm=round(reach, 1), tests=out,
             cadasio_dir=CAD.get(mov))
    res.append(r)
    print(f"{N[mov]:16s} free: {[k for k, v in out.items() if v == 'FREE']}   (cadasio pull-off {CAD.get(mov)})   with {len(sta)} parts")
json.dump(res, open(SP + '/wood_free.json', 'w'), indent=1)
