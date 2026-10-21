"""Step 42 from behind: the A end over the module's top in beat 2 (instead of waiting), screened as eval42n.py screens a plan."""
import sys, runpy
sys.argv = ['x']
ns = runpy.run_path('docs/research/pmg/round4/scripts/eval42n.py', run_name='lib')
import numpy as np
run, a_pose, BENCHM, SPUN, HELDM, benchA = ns['run'], ns['a_pose'], ns['BENCHM'], ns['SPUN'], ns['HELDM'], ns['benchA']
from scipy.spatial.transform import Rotation as Ro
RY = lambda d: Ro.from_rotvec(np.radians(d) * np.array([0, 1.0, 0])).as_matrix()
I = np.eye(3)
UP = a_pose(RY(-90), [670, 1025, 1399])
plans = {}
for name, top, R in [('T1', [650, 1100, 1290], RY(-90)), ('T2', [645, 1105, 1305], RY(-90)), ('T3', [655, 1100, 1270], RY(-90)),
                     ('T4', [660, 1110, 1290], RY(-90)), ('T5', [650, 1100, 1290], RY(-60))]:
    plans[name] = ([BENCHM, SPUN, HELDM, HELDM, HELDM, HELDM],
                   [benchA, UP, a_pose(R, top), a_pose(I, [684, 992, 1180]), a_pose(I, [667.05, 892.06, 1180]), np.eye(4)])
for k, (ms, as_) in plans.items():
    print('==', k, flush=True); run(ms, as_, ['bench', 'spun', 'top', 'side', 'down', 'seat'], wires_from=('bench', 'held', 'held', 'held', 'held'))
