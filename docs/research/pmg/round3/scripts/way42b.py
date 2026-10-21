import sys
SP = __import__('os').path.dirname(__import__('os').path.abspath(__file__))
sys.path.insert(0, SP)
from way42 import *
from way42 import _matrix, D, evaluate, turned, np
from scipy.spatial.transform import Rotation as Rot
bench = D['USB_A_BENCH']; mid_a = np.asarray(D['mid_a'])
RB = _matrix(bench)[:3, :3]
RH = Rot.from_rotvec(np.radians(-90) * np.array([0, 0, 1.0])).as_matrix()


def at(R, mid):
    """A pose: turned by R (from the seat) about the A end's middle, the middle at `mid`."""
    rv = Rot.from_matrix(R).as_rotvec(); ang = float(np.linalg.norm(rv))
    if ang < 1e-9:
        return (np.asarray(mid, float) - mid_a).round(3).tolist()
    return turned((rv / ang).round(6).tolist(), round(float(np.degrees(ang)), 4), mid_a.round(3).tolist(), (np.asarray(mid, float) - mid_a).round(3).tolist())


cands = {
 'W1': ([bench, at(RB, [597, 1058, 1399]), at(RB, [644, 1058, 1260]), at(RH, [646, 1000, 1243]), at(RH, [646, 933, 1243]), [0, 0, 0]], ['bench', 'lifted', 'over', 'hang high', 'hang low', 'seat']),
 'W2': ([bench, at(RB, [597, 1058, 1399]), at(RB, [644, 1058, 1250]), at(RH, [646, 933, 1243]), [0, 0, 0]], ['bench', 'lifted', 'over', 'hang low', 'seat']),
 'W3': ([bench, at(RB, [597, 975, 1399]), at(RB, [680, 975, 1399]), at(RH, [680, 968, 1240]), at(RH, [646, 968, 1241]), at(RH, [646, 933, 1243]), [0, 0, 0]], ['bench', 'lifted', '+x', 'over dev', '-x', 'hang low', 'seat']),
}
for k, (way, names) in cands.items():
    print('==', k); evaluate(way, names)
print('########')
c2 = {
 'W4': ([bench, at(RB, [680, 975, 1399]), at(RH, [680, 968, 1240]), at(RH, [646, 968, 1241]), at(RH, [646, 933, 1243]), [0, 0, 0]], ['bench', 'up+x', 'over dev', '-x', 'hang low', 'seat']),
 'W6': ([bench, at(RB, [680, 975, 1399]), at(RH, [668, 968, 1240]), at(RH, [646, 933, 1243]), [0, 0, 0]], ['bench', 'up+x', 'over dev 668', 'hang low', 'seat']),
 'W7': ([bench, at(RB, [672, 972, 1399]), at(RH, [664, 970, 1238]), at(RH, [646, 940, 1242]), [0, 0, 0]], ['bench', 'up+x 672', 'over dev 664', 'hang low 940', 'seat']),
 'W8': ([bench, at(RB, [597, 975, 1399]), at(RB, [680, 975, 1399]), at(RH, [670, 968, 1240]), at(RH, [646, 933, 1243]), [0, 0, 0]], ['bench', 'lifted', '+x', 'over dev 670', 'hang low', 'seat']),
}
for k, (way, names) in c2.items():
    print('==', k); evaluate(way, names)
