"""Step 42, Lee's fourth round: the module spun through the gap (blue / matrix), then stood up onto H4, the USB A end moving in the same
beats. Screens a plan: the module against the case, the A end against the moving module, the wires (bent as the player bends them) and
the parts, and the caption box. Wires: beat 1 the opening routes bent with the module; later beats both the opening and the held routes
bent (the change between them is not modelled)."""
import sys, json
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation as Ro, Slerp
import os
SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SP, '../../round3/scripts'))   # proj.py
exec(open(SP + '/path42.py').read().split("Rx = lambda d")[0])   # model, routes, bend(), rs(), pose_mat(), Rb, Rh, cb, ch, centre
from proj import project, SIZES
G = json.load(open(KIT + '/cad-geometry.json'))
A = 'NAUO283'
VA = np.asarray(model.inst[A].vertices); VA = VA[::max(1, len(VA) // 500)]
CA = model.inst[A].bounds.mean(0)
CAM = dict(v42c['camera'])
CASE = [p for p in v42['visible'] if p.startswith('NAUO') and p in model.inst and p not in (MOD, NANO, PLUG, A) and not p.startswith('CAP')]
static = []
M42 = {}
def placed_static(v):
    carry, offs = v.get('carry') or {}, v.get('offsets') or {}
    out = {}
    def pl(pid, d=0):
        if pid in out: return out[pid]
        c = carry.get(pid)
        out[pid] = _matrix(offs.get(pid)) if c is None or d > 8 else pl(c['by'], d + 1) @ _matrix(c['pose'])
        return out[pid]
    for p in v['visible']: pl(p)
    return out
W42 = placed_static(v42)
riders = {p for p, c in (v42.get('carry') or {}).items() if c['by'] == MOD} | {MOD}
STATIC = [(p, W42[p]) for p in v42['visible'] if p in model.inst and p not in riders and p != A and not p.startswith('STEM_')]
MOVING = [p for p in riders if p in model.inst]
held_r = held_routes
RY = lambda d: Ro.from_rotvec(np.radians(d) * np.array([0, 1.0, 0])).as_matrix()


def mixM(Ma, Mb_, k, c):
    R = Slerp([0, 1], Ro.from_matrix([Ma[:3, :3], Mb_[:3, :3]]))([k]).as_matrix()[0]
    M = np.eye(4); M[:3, :3] = R
    M[:3, 3] = (Ma[:3, :3] @ c + Ma[:3, 3]) * (1 - k) + (Mb_[:3, :3] @ c + Mb_[:3, 3]) * k - R @ c
    return M


def a_pose(R, middle):
    M = np.eye(4); M[:3, :3] = R; M[:3, 3] = np.asarray(middle, float) - R @ CA; return M


def depth(P, parts):
    worst = (0, None)
    for part, X in parts:
        mesh = model.inst[part]; Xi = np.linalg.inv(X)
        q = P @ Xi[:3, :3].T + Xi[:3, 3]
        lo, hi = mesh.bounds
        near = np.all((q > lo) & (q < hi), axis=1)
        if not near.any(): continue
        cp, d, tri = mesh.nearest.on_surface(q[near])
        inside = np.einsum('ij,ij->i', q[near] - cp, mesh.face_normals[tri]) < -0.3 * d
        if inside.any() and d[inside].max() > worst[0]: worst = (round(float(d[inside].max()), 2), part)
    return worst


def run(mod_stops, a_stops, names, n=13, wires_from=('bench', 'held', 'held', 'held')):
    for b in range(len(mod_stops) - 1):
        res = dict(mod_case=(0, None), a_parts=(0, None), a_mod=(0, None), a_wire=(99, None), top={})
        for k in np.linspace(0, 1, n):
            M = mixM(mod_stops[b], mod_stops[b + 1], k, centre)
            Ma = mixM(a_stops[b], a_stops[b + 1], k, CA)
            # the module's parts against the case and the static parts
            for p in MOVING:
                Vp = np.asarray(model.inst[p].vertices)[::6]
                Wp = Vp @ (M @ np.linalg.inv(_matrix(BENCH)) @ W42[p])[:3, :3].T + (M @ np.linalg.inv(_matrix(BENCH)) @ W42[p])[:3, 3]
                d = depth(Wp, [(q, X) for q, X in STATIC if q != A])
                if d[0] > res['mod_case'][0]: res['mod_case'] = (d[0], f'{p} into {d[1]}', round(float(k), 2))
            PA = VA @ Ma[:3, :3].T + Ma[:3, 3]
            d = depth(PA, STATIC)
            if d[0] > res['a_parts'][0]: res['a_parts'] = (d[0], d[1], round(float(k), 2))
            mp = [(p, M @ np.linalg.inv(_matrix(BENCH)) @ W42[p]) for p in MOVING]
            d = depth(PA, mp)
            if d[0] > res['a_mod'][0]: res['a_mod'] = (d[0], d[1], round(float(k), 2))
            srcs = [routes] if wires_from[b] == 'bench' else ([routes, held_r] if b == 1 else [held_r])
            for src in srcs:
                for w, r in src.items():
                    p = rs(bend(r, M), 1.0)
                    dd = cKDTree(p).query(PA)[0].min() - radius[w]
                    if dd < res['a_wire'][0]: res['a_wire'] = (round(float(dd), 2), w, round(float(k), 2))
            for key, (w_, h_, box) in SIZES.items():
                q = project(PA, CAM, w_, h_)
                res['top'][key] = min(res['top'].get(key, 9e9), q[:, 1].min())
        print(f"{names[b]:>9s}->{names[b + 1]:<9s} module into {res['mod_case']}  A end into part {res['a_parts']}  into module {res['a_mod']}  "
              f"clear of wires {res['a_wire']}  top {' '.join(f'{k}:{v:.0f}' for k, v in res['top'].items())}")


R1 = RY(-90) @ Rb
c_half = cb + (ch - cb) * 0.5 + np.array([0, 40.0, 0])
SPUN = pose_mat(R1, c_half)
BENCHM, HELDM = _matrix(BENCH), _matrix(HELD)
benchA = _matrix(json.load(open(KIT + '/steps.json'))['views'][[v['name'] for v in S['views']].index('Step 42')]['carry'][A]['pose'])
print('module middle spun', c_half.round(1), 'box/caption screen sizes', {k: v[2] for k, v in SIZES.items()})
if __name__ == '__main__':
    I = np.eye(3)
    RYm = lambda d: Ro.from_rotvec(np.radians(d) * np.array([0, 1.0, 0])).as_matrix()
    plans = {
     'P9': ([BENCHM, SPUN, HELDM, HELDM, HELDM, HELDM], [benchA, a_pose(RYm(-90), [670, 1025, 1399]), a_pose(RYm(-90), [670, 1025, 1399]),
             a_pose(I, [684, 992, 1180]), a_pose(I, [667.05, 892.06, 1180]), np.eye(4)]),
     'P10': ([BENCHM, SPUN, HELDM, HELDM, HELDM, HELDM], [benchA, a_pose(RYm(-90), [670, 1025, 1399]), a_pose(RYm(-60), [686, 1025, 1380]),
             a_pose(I, [684, 992, 1180]), a_pose(I, [667.05, 892.06, 1180]), np.eye(4)]),
    }
    for k, (ms, as_) in plans.items():
        print('==', k); run(ms, as_, ['bench', 'spun', 'held', 'over', 'down', 'seat'], wires_from=('bench', 'held', 'held', 'held', 'held'))
