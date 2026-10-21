import sys
SP = __import__('os').path.dirname(__import__('os').path.abspath(__file__))
sys.path.insert(0, SP)
exec(open(SP + '/way42c.py').read().split("c = {")[0])
I = np.eye(3)
seat_mid = np.asarray(D['mid_a'])
c = {
 'S1': ([bench, at(RB, [597, 1000, 1399]), at(RB, [680, 1000, 1399]), (np.array([667, 980, 1180]) - seat_mid).tolist(), (np.array([667.05, 892.06, 1180]) - seat_mid).tolist(), [0, 0, 0]],
        ['bench', 'lifted', 'back', 'over', 'down', 'seat']),
 'S2': ([bench, at(RB, [597, 1000, 1399]), at(RB, [680, 1000, 1399]), (np.array([667, 985, 1176]) - seat_mid).tolist(), (np.array([667.05, 892.06, 1176]) - seat_mid).tolist(), [0, 0, 0]],
        ['bench', 'lifted', 'back', 'over', 'down', 'seat']),
}
for k, (way, names) in c.items():
    print('==', k); evaluate(way, names); screen_extent(way, names)
print('#####')
from scipy.spatial.transform import Rotation as Ro, Slerp as Sl
RHALF = Sl([0, 1], Ro.from_matrix([RB, np.eye(3)]))([0.5]).as_matrix()[0]
c = {'S4': ([bench, at(RB, [597, 1000, 1399]), at(RB, [680, 1000, 1399]), at(RHALF, [680, 984, 1290]), (np.array([667, 980, 1180]) - seat_mid).tolist(),
             (np.array([667.05, 892.06, 1180]) - seat_mid).tolist(), [0, 0, 0]], ['bench', 'lifted', 'back', 'across', 'over', 'down', 'seat'])}
for k, (way, names) in c.items():
    print('==', k); evaluate(way, names); screen_extent(way, names)
    for s, nm in zip(way, names):
        M = _matrix(s); P = VA @ M[:3, :3].T + M[:3, 3]
        print('   ', nm, {kk: (project(P, CAM, w, h)[:, 0].min().round(0), project(P, CAM, w, h)[:, 0].max().round(0)) for kk, (w, h, b) in SIZES.items() if kk in ('760x634', '1000x548')})
print('&&&&&')
RY = lambda d: Ro.from_rotvec(np.radians(d) * np.array([0, 1.0, 0])).as_matrix()
c = {'S5': ([bench, at(RY(-90), [597, 1000, 1399]), at(RY(-90), [680, 1000, 1399]), at(RY(-45), [680, 984, 1290]), (np.array([667, 980, 1180]) - seat_mid).tolist(),
             (np.array([667.05, 892.06, 1180]) - seat_mid).tolist(), [0, 0, 0]], ['bench', 'lifted', 'back', 'across', 'over', 'down', 'seat'])}
for k, (way, names) in c.items():
    print('==', k); evaluate(way, names)
