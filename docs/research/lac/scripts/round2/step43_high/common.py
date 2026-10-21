"""guide.py's buzzer helpers, copied (LAC Build Instructions/guide.py as of 21 Oct 2026), without the Guide: for designing Step 43's
shapes in scratch. Nothing here loads the model."""
import json, sys, copy
from pathlib import Path
import numpy as np
ROOT = Path('/Users/lee-johnson/Desktop/Claude_Cadasio')
KIT = ROOT / 'LAC Build Instructions'
sys.path.insert(0, str(ROOT / 'tools'))
import wires as W  # noqa
from stepgen import apply_pose, compose, relative_pose, turned, unapply_pose, via, pose_out, _matrix  # noqa

paths = W.load(KIT / 'wire-paths.json')
HOLES, CAPS, LINES = paths['holes'], paths['caps'], paths['lines']
LCD_RAIL_SHIFT = {'NAUO82': 10.16, 'NAUO84': 15.23}
for _cap, _dz in LCD_RAIL_SHIFT.items():
    for _k in ('top', 'wire_at', 'tip'):
        if _k in CAPS[_cap]:
            CAPS[_cap][_k] = np.add(CAPS[_cap][_k], [0.0, 0.0, _dz]).tolist()
    CAPS[_cap]['box'] = np.add(CAPS[_cap]['box'], [0.0, 0.0, _dz]).tolist()
ZERO = [0.0, 0.0, 0.0]
BUZZER = 'NAUO62'
BUZZER_LEADS = [('red', 'NAUO58', 'j4', [674.5, 894.24, 1233.12], 'NAUO60', 'NAUO65'), ('black', 'NAUO59', '(-) blue', [676.02, 894.24, 1233.12], 'NAUO63', 'NAUO64')]
LEAD = {c: (cap, e) for c, cap, _, e, _, _ in BUZZER_LEADS}


def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def tidy(pose):
    if isinstance(pose, dict):
        return dict(pose, t=np.round(np.asarray(pose['t'], float), 2).tolist(), at=np.round(np.asarray(pose.get('at', [0, 0, 0]), float), 2).tolist(),
                    r=[*np.round(np.asarray(pose['r'][:3], float), 6).tolist(), round(float(pose['r'][3]), 6)])
    return np.round(np.asarray(pose, float), 1).tolist()


POSES = {k: tidy(v) for k, v in paths['poses'].items()}


def wire_at(cap):
    return np.asarray(CAPS[cap]['wire_at'], float)


def into_hole(cap, start, start_dir, controls, lift=6.0, above=10.0):
    top = wire_at(cap) + [0.0, 4.0 + above, 0.0]
    first = np.asarray(start, float) + unit(start_dir) * lift
    body = W.smooth([first, *[np.asarray(c, float) for c in controls], top], start_dir=unit(start_dir), end_dir=[0, -1, 0], spacing=0.5)
    return W.resample(W.join(W.straight(start, start_dir, lift), body, W.straight(top, [0, -1, 0], above + 4.0)), 1.0)


def posed_line(pose, pts):
    return apply_pose(pose, np.asarray(pts, float))


BUZZER_LYING = POSES['buzzer_lying']
BUZZER_WAY = {'red': [[647.2, 901.2, 1399.0], [647.8, 901.9, 1394.1], [647.8, 902.0, 1389.2], [647.8, 902.0, 1384.2], [647.8, 902.0, 1379.2], [647.9, 902.0, 1374.3], [648.1, 902.3, 1369.0], [648.5, 902.6, 1364.2], [648.8, 903.1, 1359.0], [648.8, 903.7, 1354.3], [649.1, 904.7, 1349.3], [650.1, 905.6, 1344.7], [652.5, 906.0, 1340.3], [655.8, 906.0, 1336.5]],
              'black': [[648.9, 897.0, 1393.1], [652.2, 897.0, 1389.5], [655.7, 897.0, 1386.0], [659.2, 897.1, 1382.5], [662.7, 897.4, 1379.0], [666.5, 897.8, 1375.2], [669.9, 898.0, 1371.8], [673.5, 898.0, 1368.3], [677.0, 898.0, 1364.9], [681.0, 898.3, 1361.5], [684.5, 899.2, 1358.7], [688.0, 901.4, 1355.6], [690.9, 904.1, 1352.7], [693.6, 907.0, 1349.8], [696.0, 910.3, 1346.4]]}
BUZZER_LIFT_WAY = {'red': [[645.7, 951.9, 1397.4], [645.9, 949.6, 1393.0], [646.6, 946.6, 1389.0], [648.0, 943.5, 1385.8], [650.5, 940.5, 1382.3], [653.0, 937.9, 1378.8], [655.0, 935.3, 1375.5], [656.4, 932.1, 1371.7], [656.8, 928.5, 1367.9], [656.8, 925.0, 1364.4], [656.8, 921.5, 1360.8], [656.8, 918.2, 1357.2], [656.8, 915.4, 1353.4], [656.8, 913.0, 1348.9], [656.8, 911.1, 1344.2], [657.1, 909.5, 1339.5], [658.5, 907.9, 1335.1]],
                   'black': [[648.2, 954.7, 1393.7], [651.0, 952.0, 1390.8], [653.8, 949.1, 1387.9], [656.7, 946.2, 1385.0], [659.6, 943.3, 1382.1], [662.5, 940.5, 1379.2], [665.4, 937.6, 1376.3], [668.3, 934.7, 1373.4], [671.1, 931.8, 1370.6], [674.0, 929.0, 1367.6], [677.3, 926.3, 1364.4], [680.4, 924.4, 1361.3], [683.9, 922.7, 1357.8], [687.1, 921.2, 1354.6], [690.6, 919.5, 1351.1], [693.7, 917.9, 1347.8], [696.7, 916.1, 1344.1]]}
BUZZER_UP_WAY = {'red': [[674.5, 931.0, 1236.6], [674.5, 921.5, 1240.0], [674.5, 912.0, 1244.0], [674.5, 905.0, 1249.0], [674.5, 902.8, 1254.0]],
                 'black': [[677.0, 931.0, 1236.6], [680.0, 923.5, 1240.0], [683.5, 915.5, 1244.0], [686.5, 910.0, 1248.0], [688.3, 909.8, 1251.8]]}
BUZZER_LIFT = tidy(compose([0.0, 60.0, 0.0], BUZZER_LYING, BUZZER_LYING['at']))
BUZZER_UP = [0.0, 45.0, 0.0]
BUZZER_ABOVE = {'red': 0.5, 'black': 5.0}
BUZZER_CREST = {'red': 0.3, 'black': 1.5}
BUZZER_OUT = 3.0
BUZZER_RISE = {'red': 2.2, 'black': 0.0}


def buzzer_line(colour, cap, exit_, pose, way):
    q = posed_line(pose, [exit_, np.add(exit_, [0.0, -1.0, 0.0])])
    e, d = q[0], unit(q[1] - q[0])
    above = BUZZER_ABOVE[colour]
    first, top = e + d * BUZZER_OUT, wire_at(cap) + [0.0, 4.0 + above, 0.0]
    across = lambda p: float(np.hypot(p[0] - top[0], p[2] - top[2]))
    keep = [np.asarray(p, float) for p in way if np.linalg.norm(np.asarray(p, float) - first) > 8.0 and across(p) > 7.0]
    rise = [first + d * 2.0 + [0.0, BUZZER_RISE[colour], 0.0]] if BUZZER_RISE[colour] else []
    h = top - (keep[-1] if keep else first)
    h[1] = 0.0
    return into_hole(cap, e, d, rise + keep + [top - unit(h) * 4.5 + [0.0, BUZZER_CREST[colour], 0.0]], lift=BUZZER_OUT, above=above)


def shared_to(line, point):
    s = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))]
    return round(float(s[int(np.argmin(np.linalg.norm(line - np.asarray(point, float), axis=1)))]), 1)


def buzzer_plugged(colour, cap, exit_, pose, way, stretch=False):
    line = buzzer_line(colour, cap, exit_, pose, way)[::-1]
    k = BUZZER_ABOVE[colour] + 4.0
    return W.route(line, a=cap, b=BUZZER, b_at=pose, b_from=k, **({'stretch': True} if stretch else {'tail_from': k}))


BUZZER_SEAT_WAY = {'red': [[674.5, 891.3, 1235.6], [674.5, 892.9, 1239.5], [674.5, 895.4, 1246.8], [674.5, 898.2, 1250.6], [674.5, 902.0, 1254.5], [674.5, 905.5, 1258.0], [674.5, 909.0, 1261.5], [674.1, 912.5, 1265.0], [672.9, 915.7, 1268.2], [670.4, 919.1, 1271.6], [667.9, 921.9, 1274.5], [665.7, 924.4, 1278.3], [664.8, 925.6, 1283.0], [664.8, 925.4, 1287.8], [664.9, 923.9, 1292.6], [665.4, 920.8, 1296.6], [666.0, 917.2, 1300.4], [666.2, 914.3, 1304.1], [666.2, 912.6, 1308.9], [666.2, 912.3, 1313.7], [666.2, 912.2, 1318.6], [665.5, 911.5, 1323.6]],
                   'black': [[676.2, 891.3, 1235.6], [677.6, 893.0, 1238.8], [680.6, 895.6, 1240.6], [686.8, 902.4, 1244.4], [687.8, 905.7, 1247.7], [688.1, 909.5, 1251.5], [688.8, 912.9, 1254.9], [690.4, 916.1, 1258.1], [692.4, 919.5, 1261.5], [693.2, 922.9, 1264.9], [694.1, 926.6, 1268.6], [695.8, 929.6, 1271.8], [697.7, 932.1, 1275.6], [698.4, 933.1, 1280.5], [698.5, 933.1, 1285.3], [698.5, 932.2, 1290.4], [698.5, 930.3, 1295.2], [698.5, 928.6, 1299.9], [698.5, 928.0, 1304.7], [698.5, 927.8, 1309.6], [698.5, 926.5, 1314.5], [698.5, 924.3, 1319.1], [698.5, 922.7, 1324.0], [698.5, 922.1, 1328.7], [698.5, 921.0, 1333.5]]}
BUZZER_SEAT_OUT = 1.0
BUZZER_J_Z = 1262.0


def seated_from_buzzer(colour, cap, exit_):
    e, d = np.asarray(exit_, float), np.array([0.0, -1.0, 0.0])
    above = BUZZER_ABOVE[colour]
    top = wire_at(cap) + [0.0, 4.0 + above, 0.0]
    way = [np.asarray(p, float) for p in BUZZER_SEAT_WAY[colour]]
    if colour == 'red':
        h = top - way[-1]
        h[1] = 0.0
        way.append(top - unit(h) * 4.5 + [0.0, BUZZER_CREST[colour], 0.0])
    line = into_hole(cap, e, d, way, lift=BUZZER_SEAT_OUT, above=above)
    return line, int(np.argmax(line[:, 2] >= BUZZER_J_Z))


def buzzer_over_seat(colour, cap, exit_):
    L, j = seated_from_buzzer(colour, cap, exit_)
    e, d = np.add(exit_, BUZZER_UP), np.array([0.0, -1.0, 0.0])
    body = W.smooth([e + d * BUZZER_OUT, *[np.asarray(c, float) for c in BUZZER_UP_WAY[colour]], L[j]], start_dir=d,
                    end_dir=unit(L[j + 2] - L[j]), spacing=0.5)
    line = W.resample(W.join(W.straight(e, d, BUZZER_OUT), body, L[j:]), 1.0)[::-1]
    k = shared_to(line, L[j])
    return W.route(line, a=cap, b=BUZZER, b_at=BUZZER_UP, b_from=k, tail_from=k)


def buzzer_clamped(colour, cap, exit_):
    L, j = seated_from_buzzer(colour, cap, exit_)
    line = L[::-1]
    k = shared_to(line, L[j])
    return W.route(line, a=cap, b=BUZZER, b_from=k, tail_from=k)


# ---------------------------------------------------------------- steps.json access
STEPS = json.load(open(KIT / 'steps.json'))
VIEWS = {v['name']: v for v in STEPS['views']}


def same_route(a, b, tol=0.02):
    pa, pb = np.asarray(a['pts']), np.asarray(b['pts'])
    keys = lambda r: {k: v for k, v in r.items() if k != 'pts'}
    return pa.shape == pb.shape and float(np.abs(pa - pb).max()) <= tol and keys(a) == keys(b)


def write_steps(out_path, path43, routes43, extra_views=None):
    """A copy of steps.json with Step 43's buzzer path and its leads' routes replaced, as stepgen writes them: path = the stops,
    wire_via = every route but the last, wires = the last (and every later view that has the old final route gets the new one)."""
    S = copy.deepcopy(STEPS)
    routes = S['routes']

    def route_no(r):
        key = json.dumps(r, sort_keys=True)
        for i, x in enumerate(routes):
            if json.dumps(x, sort_keys=True) == key:
                return i
        routes.append(r)
        return len(routes) - 1
    V = {v['name']: v for v in S['views']}
    names = [v['name'] for v in S['views']]
    i43 = names.index('Step 43c')
    old_final = {w: V['Step 43c']['wires'][w] for w in routes43}
    new_final = {w: route_no(rs[-1]) for w, rs in routes43.items()}
    for n in ('Step 43', 'Step 43c'):
        V[n]['path'] = [pose_out(p) for p in path43]
        stops = [k for k, p in enumerate(path43) if not isinstance(p, via)]
        if len(stops) < len(path43):
            V[n]['stops'] = stops
        else:
            V[n].pop('stops', None)
    V['Step 43c']['wire_via'] = {w: [route_no(r) for r in rs[:-1]] for w, rs in routes43.items() if len(rs) > 1}
    for v in S['views'][i43:]:
        for w in routes43:
            if (v.get('wires') or {}).get(w) == old_final[w]:
                v['wires'][w] = new_final[w]
    for name, wires in (extra_views or {}).items():
        for w, r in wires.items():
            V[name]['wires'][w] = route_no(r)
    json.dump(S, open(out_path, 'w'))
    return S
