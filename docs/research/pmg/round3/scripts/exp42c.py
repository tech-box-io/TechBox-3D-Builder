"""Step 42: the USB cable at each stop of the A end's new way (over the back), settled as usb_held does it."""
import sys, time, pickle
import numpy as np
SP = __import__('os').path.dirname(__import__('os').path.abspath(__file__))
sys.path.insert(0, SP)
import probe
from scipy.spatial.transform import Rotation as Rot
from scipy.spatial import cKDTree
ns = probe.load(marker='g.place("Pick up the I/O module')
g, W, R = ns['g'], ns['W'], ns['R']
from stepgen import _matrix, turned, apply_pose
MODULE, NANO, USB_B, USB_A = ns['MODULE'], ns['NANO'], ns['USB_B'], ns['USB_A']
held = ns['MODULE_HELD']
for p in (MODULE, NANO, USB_B):
    V = apply_pose(held, np.asarray(g.model.inst[p].vertices))
    print(p, 'held bounds', V.min(0).round(1), V.max(0).round(1))
bench = ns['USB_A_BENCH']; mid_a = np.asarray(ns['GEO']['parts'][USB_A]['middle'])
RB = _matrix(bench)[:3, :3]
RH = Rot.from_rotvec(np.radians(-90) * np.array([0, 0, 1.0])).as_matrix()


def at(R, mid):
    rv = Rot.from_matrix(R).as_rotvec(); ang = float(np.linalg.norm(rv))
    return turned((rv / ang).round(6).tolist(), round(float(np.degrees(ang)), 4), mid_a.round(3).tolist(), (np.asarray(mid, float) - mid_a).round(3).tolist())


stops = [('lifted', at(RB, [597, 975, 1399])), ('back', at(RB, [680, 975, 1399])), ('over', at(RH, [680, 968, 1240])),
         ('forward', at(RH, [646, 968, 1241])), ('lowered', at(RH, [646, 933, 1243]))]
LOOP = [[604.0, 1088.0, 1258.0], [606.0, 1092.0, 1284.0]]
vias = {'bench': LOOP + [[600.0, 1040.0, 1350.0]],
        'lifted': LOOP + [[604.0, 1080.0, 1325.0], [599.0, 1010.0, 1355.0]],
        'back': LOOP + [[614.0, 1080.0, 1322.0], [645.0, 1022.0, 1356.0]],
        'over': [[620.0, 1080.0, 1252.0], [644.0, 1040.0, 1241.0], [666.0, 1012.0, 1239.0]],
        'forward': [[620.0, 1078.0, 1254.0], [636.0, 1046.0, 1243.0]],
        'lowered': [[618.0, 1074.0, 1252.0], [638.0, 1040.0, 1244.0], [646.0, 1000.0, 1243.0]]}
held_lines = {w: np.asarray(p, float) for w, p in ns['_held_lines'].items()}
trees = {w: cKDTree(p) for w, p in held_lines.items()}
out = {}
for name, pose in [('bench', bench)] + stops:
    r = ns['usb_held'](f'exp cable {name}', pose, vias[name])
    p = np.asarray(r['pts'], float)
    L = float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum())
    clear = min(t.query(p[4:-4])[0].min() for t in trees.values()) - 1.75 - 0.625
    # the cable against the A end's own body (beyond its exit) and the module
    A = apply_pose(pose, np.asarray(g.model.inst[USB_A].vertices))
    dA = cKDTree(A).query(p[:-12])[0].min()
    print(f'{name:8s} length {L:6.1f}  clear of wires {clear:5.2f}  nearest A-end vertex (cable but its last 12 pts) {dA:5.2f}')
    out[name] = p
pickle.dump(dict(cables=out, stops=stops), open(__import__('tempfile').gettempdir() + '/cables42.pkl', 'wb'))

import json
sys.path.insert(0, SP)
from proj import project, SIZES
S = json.load(open('/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions/steps.json'))
cam = [x for x in S['views'] if x['name'] == 'Step 42c'][0]['camera']
def rs(p, n=200):
    s_ = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    t = np.linspace(0, s_[-1], n); return np.stack([np.interp(t, s_, p[:, k]) for k in range(3)], 1)
names = ['bench', 'lifted', 'back', 'over', 'forward', 'lowered']
sh = [rs(out[n]) for n in names]
for k in range(len(sh)):
    res = []
    for f in ([1.0] if k == 0 else [0.25, 0.5, 0.75, 1.0]):
        pp = sh[k] if k == 0 else sh[k - 1] * (1 - f) + sh[k] * f
        for key in ('760x634', '1000x548'):
            w, h, bx = SIZES[key]; q = project(pp, cam, w, h); inx = (q[:, 0] > bx[0]) & (q[:, 0] < bx[2])
            res.append(f"{key}@{f}:{(q[inx, 1].min() if inx.any() else 9999):.0f}/{bx[3]}")
    print(names[k], ' '.join(res))
