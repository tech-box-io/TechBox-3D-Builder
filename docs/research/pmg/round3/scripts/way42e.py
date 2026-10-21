import sys
SP = __import__('os').path.dirname(__import__('os').path.abspath(__file__))
sys.path.insert(0, SP)
exec(open(SP + '/way42d.py').read().split("c = {\n 'S1'")[0])
from scipy.spatial.transform import Rotation as Ro
RY = lambda d: Ro.from_rotvec(np.radians(d) * np.array([0, 1.0, 0])).as_matrix()
import way42
for tgt in ([615.0, 992.0, 1290.0], [632.0, 1003.0, 1292.0]):
    CAM['target'] = tgt; way42.CAM['target'] = tgt
    plug = project(np.array([[611.0, 1077.0, 1284.0], [625.0, 1064.0, 1300.0]]), CAM, 1000, 548)
    for ya in (984, 1000, 1010, 1020):
        way = [bench, at(RY(-90), [597, 1000, 1399]), at(RY(-90), [680, 1000, 1399]), at(RY(-45), [680, ya, 1290]), (np.array([667, 980, 1180]) - seat_mid).tolist(),
               (np.array([667.05, 892.06, 1180]) - seat_mid).tolist(), [0, 0, 0]]
        M = _matrix(way[3]); P = VA @ M[:3, :3].T + M[:3, 3]
        q = project(P, CAM, 1000, 548)
        print('target', tgt, 'across y', ya, 'A end bottom on screen', round(q[:, 1].max()), 'module top', plug[:, 1].round(0).tolist())
        evaluate(way, ['bench', 'lifted', 'back', 'across', 'over', 'down', 'seat'])
