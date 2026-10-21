"""Evaluate candidate ways for the USB A end in Step 42 (module held): clearance to the held wires and the parts, and the caption box."""
import sys, json, pickle
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation, Slerp
SP = __import__('os').path.dirname(__import__('os').path.abspath(__file__))
sys.path.insert(0, SP); sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/tools')
import stepgen
from stepgen import _matrix, turned, compose
from proj import project, SIZES
D = pickle.load(open(__import__('tempfile').gettempdir() + '/held42.pkl', 'rb'))
S = json.load(open('/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions/steps.json'))
CAM = [v for v in S['views'] if v['name'] == 'Step 42c'][0]['camera']
KIT = '/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions'
spec = json.load(open(KIT + '/materials.json'))
model = stepgen.Model(KIT + '/' + spec['source'], adjust=spec.get('adjust_mm') or {}, own_parts=spec.get('own_parts', {}),
                      extra_parts={i: (KIT + '/' + e['glb'], e['pose']) for i, e in spec.get('extra_parts', {}).items()})
A = 'NAUO283'
VA = np.asarray(model.inst[A].vertices); VA = VA[::max(1, len(VA) // 600)]
C = model.inst[A].bounds.mean(0)
wires = D['held']; tree = {w: cKDTree(p) for w, p in wires.items()}
scene = [(p, pose) for p, pose in D['scene'] if p in model.inst]


def mix(a, b, k):
    Am, Bm = _matrix(a), _matrix(b)
    R = Slerp([0, 1], Rotation.from_matrix([Am[:3, :3], Bm[:3, :3]]))([k]).as_matrix()[0]
    M = np.eye(4); M[:3, :3] = R
    M[:3, 3] = (Am[:3, :3] @ C + Am[:3, 3]) * (1 - k) + (Bm[:3, :3] @ C + Bm[:3, 3]) * k - R @ C
    return M


def hanging(mid, deg=-90.0, axis=(0, 0, 1)):
    mid_a = np.asarray(D['mid_a'], float)
    return turned(list(axis), deg, mid_a.round(3).tolist(), (np.asarray(mid, float) - mid_a).round(3).tolist())


def evaluate(way, names, n=25, verbose=True):
    worst_all = []
    for s in range(len(way) - 1):
        wmin, pmax, box, off = (9e9, None), (0, None), {}, {}
        for k in np.linspace(0, 1, n):
            M = mix(way[s], way[s + 1], k)
            P = VA @ M[:3, :3].T + M[:3, 3]
            for w, t in tree.items():
                d = t.query(P)[0].min() - 0.625
                if d < wmin[0]:
                    wmin = (round(float(d), 2), w, round(float(k), 2))
            for part, pose in scene:
                mesh = model.inst[part]
                X = np.linalg.inv(_matrix(pose))
                q = P @ X[:3, :3].T + X[:3, 3]
                lo, hi = mesh.bounds
                near = np.all((q > lo) & (q < hi), axis=1)
                if not near.any():
                    continue
                cp, d, tri = mesh.nearest.on_surface(q[near])
                inside = np.einsum('ij,ij->i', q[near] - cp, mesh.face_normals[tri]) < -0.3 * d
                if inside.any() and d[inside].max() > pmax[0]:
                    pmax = (round(float(d[inside].max()), 2), part, round(float(k), 2))
            for key, (w, h, b) in SIZES.items():
                p = project(P, CAM, w, h)
                inb = ((p[:, 0] > b[0]) & (p[:, 0] < b[2]) & (p[:, 1] > b[1]) & (p[:, 1] < b[3])).mean()
                box[key] = max(box.get(key, 0), inb)
                off[key] = min(off.get(key, 9e9), p[:, 1].min())
        line = f'{names[s]:>22s} -> {names[s + 1]:<22s} wire clear {wmin}  part depth {pmax}  box {" ".join(f"{k}:{v:.0%}" for k, v in box.items())}  top {" ".join(f"{k}:{v:.0f}" for k, v in off.items())}'
        if verbose:
            print(line)
        worst_all.append((wmin, pmax, box))
    return worst_all


if __name__ == '__main__':
    bench = D['USB_A_BENCH']; mid_a = np.asarray(D['mid_a'])
    print('A end middle (model bounds)', C.round(2), 'geo', mid_a)
    benchM = _matrix(bench); bm = benchM[:3, :3] @ C + benchM[:3, 3]
    print('bench middle', bm.round(1))
    for lift, y2, y3, x2 in [(150, 1060, 933, 646), (170, 1060, 933, 646), (150, 1050, 933, 644)]:
        way = [bench, compose([0.0, lift, 0.0], bench, mid_a.tolist()), hanging([x2, y2, 1244.0]), hanging([x2, y3, 1244.0]), [0.0, 0.0, 0.0]]
        print('== lift', lift, 'y2', y2, 'y3', y3, 'x2', x2)
        evaluate(way, ['bench', 'lifted', 'hanging high', 'hanging low', 'seat'])
