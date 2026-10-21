"""Step 42 from behind, the A end over the module's top to its display side in beat 2: collisions (as eval42n.py) and, from the camera
straight behind, how much of the A end is drawn over the wires (within 4 px on screen at the LMS's size), and its top on screen."""
import sys, runpy
sys.argv = ['x']
ns = runpy.run_path('docs/research/pmg/round4/scripts/eval42n.py', run_name='lib')
import numpy as np
from scipy.spatial import cKDTree
run, a_pose, BENCHM, SPUN, HELDM, benchA = ns['run'], ns['a_pose'], ns['BENCHM'], ns['SPUN'], ns['HELDM'], ns['benchA']
mixM, VA, CA, held_r, rs, bend, project, SIZES = ns['mixM'], ns['VA'], ns['CA'], ns['held_r'], ns['rs'], ns['bend'], ns['project'], ns['SIZES']
centre = ns['centre']
from scipy.spatial.transform import Rotation as Ro
RY = lambda d: Ro.from_rotvec(np.radians(d) * np.array([0, 1.0, 0])).as_matrix()
I = np.eye(3)
CAM = dict(dir=[0.8387, 0.5446, 0.0], target=[631, 1021, 1298], radius=132)
ns['CAM'].clear(); ns['CAM'].update(CAM)
w, h, box = SIZES['1000x548']
UP = a_pose(RY(-90), [670, 1025, 1399])


def screen_overlap(ms, as_):
    for b in range(1, len(ms) - 1):
        worst, top = 0.0, 9e9
        for k in np.linspace(0, 1, 13):
            M = mixM(ms[b], ms[b + 1], k, centre)
            Ma = mixM(as_[b], as_[b + 1], k, CA)
            PA = VA @ Ma[:3, :3].T + Ma[:3, 3]
            qa = project(PA, CAM, w, h)
            qw = np.vstack([project(rs(bend(r, M), 1.0), CAM, w, h) for r in held_r.values()])
            d = cKDTree(qw).query(qa)[0]
            worst = max(worst, (d < 4).mean()); top = min(top, qa[:, 1].min())
        print(f'   beat {b + 1}: A end over wires on screen, most {worst:.0%}; top on screen {top:.0f} (box bottom {box[3]})')


plans = {}
for name, top, R in [('U1', [650, 1110, 1215], I), ('U2', [650, 1115, 1200], I), ('U3', [655, 1105, 1225], I), ('U4', [645, 1120, 1210], I),
                     ('U5', [650, 1110, 1215], RY(-45))]:
    plans[name] = ([BENCHM, SPUN, HELDM, HELDM, HELDM, HELDM],
                   [benchA, UP, a_pose(R, top), a_pose(I, [684, 992, 1180]), a_pose(I, [667.05, 892.06, 1180]), np.eye(4)])
for k, (ms, as_) in plans.items():
    print('==', k, flush=True)
    run(ms, as_, ['bench', 'spun', 'top', 'side', 'down', 'seat'], wires_from=('bench', 'held', 'held', 'held', 'held'))
    screen_overlap(ms, as_)
