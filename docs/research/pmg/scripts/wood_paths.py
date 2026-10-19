"""Test ways in for the case parts: a path is a list of poses (stepgen's form, relative to the seat) from the seat outward; along it
(every 0.5 mm / 0.5 deg) the moving part's surface points are tested against the parts already built (and theirs against it), and the
deepest pass-through is reported per part, with where on the moving part it happens. A depth up to about 1.2 mm is a press fit or a
snap barb flexing past (stepgen's snug_fit); more is a real collision."""
import sys, json, numpy as np, trimesh
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/tools')
import stepgen
SP = sys.argv[1]
d = np.load(SP + '/wood.npz')
M = {}
for k in d.files:
    if k.endswith('__V'):
        i = k[:-3]; m = trimesh.Trimesh(d[i + '__V'], d[i + '__F'], process=True); m.merge_vertices(); M[i] = m
N = {'NAUO63': 'H1', 'NAUO65': 'H2', 'NAUO66': 'H3', 'NAUO73': 'H4', 'NAUO67': 'H5', 'NAUO60': 'H6', 'NAUO68': 'H7', 'NAUO61': 'H8',
     'NAUO72': 'key1', 'NAUO71': 'key2', 'NAUO70': 'key3', 'NAUO69': 'key4', 'NAUO64': 'H10', 'NAUO62': 'H11', 'NAUO77': 'H12',
     'NAUO75': 'H13', 'NAUO74': 'H14'}
def densify(path, step_mm=0.5, step_deg=0.5):
    """Poses between consecutive poses of the path, as the player plays them: the turn's angle about its own axis and point
    ('at') and the move 't' both change evenly."""
    def parts(p):
        if isinstance(p, dict) and p.get('r') and p['r'][3]:
            return np.array(p['r'][:3], float), float(p['r'][3]), np.array(p.get('at', [0, 0, 0]), float), np.array(p.get('t', [0, 0, 0]), float)
        return None, 0.0, None, np.array(p if not isinstance(p, dict) else p.get('t', [0, 0, 0]), float)
    out = []
    for a, b in zip(path[:-1], path[1:]):
        ax_a, ang_a, at_a, t_a = parts(a); ax_b, ang_b, at_b, t_b = parts(b)
        ax = ax_b if ax_b is not None else ax_a; at = at_b if at_b is not None else at_a
        n = max(2, int(max(np.linalg.norm(t_b - t_a) / step_mm, abs(ang_b - ang_a) / step_deg)) + 1)
        for s_ in np.linspace(0, 1, n):
            ang = (1 - s_) * ang_a + s_ * ang_b; t = (1 - s_) * t_a + s_ * t_b
            pose = dict(t=t.tolist(), r=list(ax) + [ang], at=list(at)) if ax is not None and abs(ang) > 1e-9 else t.tolist()
            out.append(stepgen._matrix(pose))
    return out
def run(label, mov, sta, path, n_pts=6000, report=True):
    m = M[mov]
    pts, _ = trimesh.sample.sample_surface_even(m, n_pts, seed=2)
    apt = m.area / n_pts
    poses = densify(path)
    worst = {}
    for k, T in enumerate(poses):
        q = pts @ T[:3, :3].T + T[:3, 3]
        for s in sta:
            S = M[s]; lo, hi = S.bounds
            near = np.all((q >= lo - 0.2) & (q <= hi + 0.2), axis=1)
            if not near.any(): continue
            inside = S.contains(q[near])
            if not inside.any(): continue
            qi = q[near][inside]
            dist = trimesh.proximity.closest_point(S, qi)[1]
            deep = dist > 0.3
            cnt = int(deep.sum())
            if cnt and cnt > worst.get(s, (0,))[0]:
                sp = pts[near][inside][deep]
                worst[s] = (cnt, k / (len(poses) - 1), sp.min(0).round(1).tolist(), sp.max(0).round(1).tolist(), float(dist.max()))
    if report:
        txt = ', '.join(f"{N[s]} {v[0]} pts ({v[0]*apt:.1f} mm2, max {v[4]:.2f} deep) at {v[1]:.2f} of the way, seated region {v[2]}..{v[3]}" for s, v in sorted(worst.items(), key=lambda x: -x[1][0]))
        print(f'{label}: deepest pass-through: {txt or "none"}')
    return {N[s]: dict(points_deeper_than_0_3=v[0], area_mm2=round(v[0] * apt, 1), max_depth_mm=round(v[4], 2), at_fraction=round(v[1], 3), seated_region=[v[2], v[3]]) for s, v in worst.items()}
T = stepgen.turned
res = {}
if __name__ == '__main__':
    which = sys.argv[2] if len(sys.argv) > 2 else 'all'
    walls = ['NAUO63']
    if which in ('all', 'walls'):
        res['H2 +X 40 (Cadasio)'] = run('H2 +X 40 (Cadasio)', 'NAUO65', ['NAUO63'], [[0, 0, 0], [40, 0, 0]])
        res['H2 +Z 40'] = run('H2 +Z 40', 'NAUO65', ['NAUO63'], [[0, 0, 0], [0, 0, 40]])
        res['H3 +X 43 (Cadasio)'] = run('H3 +X 43 (Cadasio)', 'NAUO66', ['NAUO63', 'NAUO65'], [[0, 0, 0], [43, 0, 0]])
        res['H4 +X 65 (Cadasio)'] = run('H4 +X 65 (Cadasio)', 'NAUO73', ['NAUO63', 'NAUO65', 'NAUO66'], [[0, 0, 0], [65, 0, 0]])
        res['H4 -Y 65'] = run('H4 -Y 65', 'NAUO73', ['NAUO63', 'NAUO65', 'NAUO66'], [[0, 0, 0], [0, -65, 0]])
    json.dump(res, open(SP + f'/wood_paths_{which}.json', 'w'), indent=1)
    if which == 'floor':
        S5 = ['NAUO63', 'NAUO65', 'NAUO66', 'NAUO73']
        for name, mov, sta, ytop in (('H5', 'NAUO67', S5, 903.39), ('H6', 'NAUO60', S5 + ['NAUO67'], 900.39),
                                      ('H7', 'NAUO68', S5 + ['NAUO67', 'NAUO60', 'NAUO76', 'NAUO83', 'NAUO84', 'NAUO85'], 897.39)):
            sta = [x for x in sta if x in M]
            res[f'{name} straight -Y 60'] = run(f'{name} straight -Y 60', mov, sta, [[0, 0, 0], [0, -60, 0]])
            for ang in (-5, -8):
                piv = [530, ytop, 1357.17]
                lab = f'{name} hinge: turn {ang} deg about X through (y {ytop}, z 1357.17), then -Z 5, then -Y 60'
                path = [[0, 0, 0], T([1, 0, 0], ang, piv), T([1, 0, 0], ang, piv, [0, 0, -5]), T([1, 0, 0], ang, piv, [0, -60, -5])]
                res[lab] = run(lab, mov, sta, path)
    json.dump(res, open(SP + f'/wood_paths_{which}.json', 'w'), indent=1)
    if which == 'upper':
        res = {}
        B8 = ['NAUO63', 'NAUO65', 'NAUO66', 'NAUO73', 'NAUO67', 'NAUO60', 'NAUO68']
        res['H8 +Y 95 (Cadasio)'] = run('H8 +Y 95 (Cadasio)', 'NAUO61', B8, [[0, 0, 0], [0, 95, 0]])
        B9 = B8 + ['NAUO61']
        res['key -X 108 (Cadasio)'] = run('key -X 108 (Cadasio)', 'NAUO72', B9, [[0, 0, 0], [-108, 0, 0]])
        res['key +Y 60'] = run('key +Y 60', 'NAUO72', B9, [[0, 0, 0], [0, 60, 0]])
        B10 = B9 + ['NAUO72', 'NAUO71', 'NAUO70', 'NAUO69']
        res['H10 +Y 30'] = run('H10 +Y 30', 'NAUO64', B10, [[0, 0, 0], [0, 30, 0]])
        res['H10 -X 30'] = run('H10 -X 30', 'NAUO64', B10, [[0, 0, 0], [-30, 0, 0]])
        for ang, py in ((-8, 931.08), (-10, 931.08), (-10, 934.08)):
            piv = [588.86, py, 1290.49]
            lab = f'H10 hinge: front up {-ang} deg about Z through (x 588.86, y {py}), then -X 14, then -X 110 +Y 26'
            res[lab] = run(lab, 'NAUO64', B10, [[0, 0, 0], T([0, 0, 1], ang, piv), T([0, 0, 1], ang, piv, [-14, 0, 0]), T([0, 0, 1], ang, piv, [-124, 26, 0])])
        B11 = B10 + ['NAUO64']
        res['H11 -X 6.7 then +Y 53 (Cadasio)'] = run('H11 -X 6.7 then +Y 53 (Cadasio)', 'NAUO62', B11, [[0, 0, 0], [-6.7, 0, 0], [-6.7, 53.1, 0]])
        res['H11 +Y 53 straight'] = run('H11 +Y 53 straight', 'NAUO62', B11, [[0, 0, 0], [0, 53.1, 0]])
        B12 = B11 + ['NAUO62']
        res['H12 -X 7.6 then +Y 44.5 (Cadasio)'] = run('H12 -X 7.6 then +Y 44.5 (Cadasio)', 'NAUO77', B12, [[0, 0, 0], [-7.6, 0, 0], [-7.6, 44.5, 0]])
        B13 = B12 + ['NAUO77']
        u = np.array([-0.766, 0.643, 0])
        res['H13 up the slope 80 (Cadasio)'] = run('H13 up the slope 80 (Cadasio)', 'NAUO75', B13, [[0, 0, 0], (80 * u).tolist()])
        res['H13 +Y 60'] = run('H13 +Y 60', 'NAUO75', B13, [[0, 0, 0], [0, 60, 0]])
        res['H13 along its normal 40'] = run('H13 along its normal 40', 'NAUO75', B13, [[0, 0, 0], (40 * np.array([0.643, 0.766, 0])).tolist()])
        B14 = B13 + ['NAUO75']
        for lab, v in (('H14 along its normal (out, toward the student) 40', [-0.766, 0.643, 0]), ('H14 up the slope 60', [0.643, 0.766, 0]),
                       ('H14 +Y 60', [0, 1, 0]), ('H14 Cadasio leg (0.26, 0.96, 0) 60', [0.26, 0.96, 0]), ('H14 down the slope 40', [-0.643, -0.766, 0])):
            res[lab] = run(lab, 'NAUO74', B14, [[0, 0, 0], (np.array(v) / np.linalg.norm(v) * float(lab.split()[-1])).tolist()])
        json.dump(res, open(SP + '/wood_paths_upper.json', 'w'), indent=1)
    if which == 'elec':
        sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
        from pmglib import Glb
        G = Glb('/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions/pmg.glb')
        def load(i):
            V, F, _ = G.instance_geometry(i); m = trimesh.Trimesh(V, F, process=False); M[i] = m
            N[i] = {'NAUO78': 'module', 'NAUO79': 'display', 'NAUO81': 'matrix', 'NAUO76': 'btn black', 'NAUO83': 'btn yellow',
                    'NAUO84': 'btn white', 'NAUO85': 'btn blue'}[i]
        res = {}
        CASE = ['NAUO63', 'NAUO65', 'NAUO66', 'NAUO73', 'NAUO67', 'NAUO60', 'NAUO68', 'NAUO61', 'NAUO72', 'NAUO71', 'NAUO70', 'NAUO69', 'NAUO64', 'NAUO62', 'NAUO77', 'NAUO75']
        for b in ['NAUO76', 'NAUO85']:
            load(b)
            sta = ['NAUO63', 'NAUO65', 'NAUO66', 'NAUO73', 'NAUO67', 'NAUO60']
            res[f'{N[b]} -Y 40 (case turned over: up)'] = run(f'{N[b]} -Y 40 (case turned over: up)', b, sta, [[0, 0, 0], [0, -40, 0]], n_pts=4000)
            res[f'{N[b]} -X 40'] = run(f'{N[b]} -X 40', b, sta, [[0, 0, 0], [-40, 0, 0]], n_pts=4000)
        load('NAUO78')
        res['module +Y 105 (to NAUO94, Cadasio)'] = run('module +Y 105 (to NAUO94, Cadasio)', 'NAUO78', CASE, [[0, 0, 0], [0, 105, 0]], n_pts=8000)
        res['module +X 40'] = run('module +X 40', 'NAUO78', CASE, [[0, 0, 0], [40, 0, 0]], n_pts=8000)
        del M['NAUO78']
        load('NAUO79')
        mid = [564.03, 980.84, 1293.47]
        res['display Cadasio (-7 then -6)'] = run('display Cadasio (-7 then -6)', 'NAUO79', CASE, [[0, 0, 0], T([0, 0, 1], 23.32, mid, [-2.29, 2.07, 0]), T([0, 0, 1], 23.32, mid, [-3.98, 13.06, 0]), T([0, 0, 1], 23.32, mid, [-3.98, 60, 0])], n_pts=4000)
        res['display +Y 50'] = run('display +Y 50', 'NAUO79', CASE, [[0, 0, 0], [0, 50, 0]], n_pts=4000)
        res['display out along H14 normal 40'] = run('display out along H14 normal 40', 'NAUO79', CASE, [[0, 0, 0], [-30.6, 25.7, 0]], n_pts=4000)
        load('NAUO81')
        mid = [532.48, 955.89, 1289.1]
        res['matrix Cadasio (-9 then -8)'] = run('matrix Cadasio (-9 then -8)', 'NAUO81', CASE + ['NAUO79'], [[0, 0, 0], T([0, 0, 1], 20, mid, [-5.11, 2.22, 1.37]), T([0, 0, 1], 20, mid, [-4.44, 22.65, 1.4]), T([0, 0, 1], 20, mid, [-40, 40, 1.4])], n_pts=6000)
        res['matrix out along its normal 40'] = run('matrix out along its normal 40', 'NAUO81', CASE + ['NAUO79'], [[0, 0, 0], [-25.7, -30.6, 0]], n_pts=6000)
        res['matrix +Y 40'] = run('matrix +Y 40', 'NAUO81', CASE + ['NAUO79'], [[0, 0, 0], [0, 40, 0]], n_pts=6000)
        H14S = CASE + ['NAUO79', 'NAUO81']
        for ang in (7, -7):
            for nm, piv in (('top hooks', [565.0, 1003.0, 1290.5]), ('bottom notches', [548.0, 968.0, 1290.5])):
                lab = f'H14 turn {ang} deg about Z through its {nm} {piv[:2]}, then out along its normal 30'
                res[lab] = run(lab, 'NAUO74', H14S, [[0, 0, 0], T([0, 0, 1], ang, piv), T([0, 0, 1], ang, piv, [-23, 19.3, 0])])
        json.dump(res, open(SP + '/wood_paths_elec.json', 'w'), indent=1)
    if which == 'h14':
        sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
        from pmglib import Glb
        G = Glb('/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions/pmg.glb')
        for i, nm in (('NAUO79', 'display'), ('NAUO81', 'matrix')):
            V, F, _ = G.instance_geometry(i); M[i] = trimesh.Trimesh(V, F, process=False); N[i] = nm
        res = {}
        CASE = ['NAUO63', 'NAUO65', 'NAUO66', 'NAUO73', 'NAUO67', 'NAUO60', 'NAUO68', 'NAUO61', 'NAUO72', 'NAUO71', 'NAUO70', 'NAUO69', 'NAUO64', 'NAUO62', 'NAUO77', 'NAUO75', 'NAUO79', 'NAUO81']
        S_ = np.array([0.643, 0.766, 0]); Nn = np.array([-0.766, 0.643, 0])
        for ang in (4, 7, 10):
            for piv in ([548.0, 968.0, 1290.5], [551.0, 971.0, 1290.5]):
                lab = f'H14 top out {ang} deg about Z through {piv[:2]}, then up the slope 10, then out 30'
                path = [[0, 0, 0], T([0, 0, 1], ang, piv), T([0, 0, 1], ang, piv, (10 * S_).tolist()), T([0, 0, 1], ang, piv, (10 * S_ + 30 * Nn).tolist())]
                res[lab] = run(lab, 'NAUO74', CASE, path)
        res['H14 up the slope 10 then out 30'] = run('H14 up the slope 10 then out 30', 'NAUO74', CASE, [[0, 0, 0], (10 * S_).tolist(), (10 * S_ + 30 * Nn).tolist()])
        res['H14 down the slope 6 then out 30'] = run('H14 down the slope 6 then out 30', 'NAUO74', CASE, [[0, 0, 0], (-6 * S_).tolist(), (-6 * S_ + 30 * Nn).tolist()])
        json.dump(res, open(SP + '/wood_paths_h14.json', 'w'), indent=1)
