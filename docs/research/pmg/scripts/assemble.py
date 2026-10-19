"""Gather the scratch results into docs/research/pmg/cad_study.json, adding the Nano poses."""
import sys, json, glob, os, numpy as np
from scipy.spatial.transform import Rotation
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from pmglib import pose_from
SP = sys.argv[1]; OUT = '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/cad_study.json'
L = lambda n: json.load(open(f'{SP}/{n}'))
def T(pose):
    M = np.eye(4)
    if isinstance(pose, list): M[:3, 3] = pose; return M
    ax = np.array(pose['r'][:3]); R = Rotation.from_rotvec(ax / np.linalg.norm(ax) * np.radians(pose['r'][3])).as_matrix()
    at = np.array(pose['at']); M[:3, :3] = R; M[:3, 3] = at - R @ at + np.array(pose['t']); return M
C = L('copies.json'); MC = L('module_compare.json'); NC = L('nano_check.json')
nano_mid = (np.array(NC['built_nano_box'][0]) + np.array(NC['built_nano_box'][1])) / 2
M1 = T(C['io_module']['NAUO1']['pose']); M94 = T(C['io_module']['NAUO94']['pose'])
def P(M): return pose_from(M[:3, :3], M[:3, 3], nano_mid)
S = np.eye(4); S[:3, 3] = [0.01, 15.24, 0.01]; S2 = np.eye(4); S2[:3, 3] = [0.01, 44.90, 0.01]
nano = dict(node='NAUO301', note='the Nano inside the built module NAUO78 (34 meshes: nano-board, two 15-pin headers, chips, Mini-USB); NAUO94 has a node of the same name, which trimesh (stepgen.Model) loads as NAUO301_1 because NAUO78 comes first in the file',
            built_box=NC['built_nano_box'], built_middle=nano_mid.round(2).tolist(),
            usb_end_built=[0, -1, 0], pins_built=[-1, 0, 0],
            poses_from_built={'bench seat on NAUO1 (Cadasio nano-3; not in the STEP)': P(M1), 'NAUO3 (15.24 above the bench seat)': P(S @ M1),
                              'NAUO2 (44.90 above the bench seat)': P(S2 @ M1), 'in the held-above module NAUO94': P(M94)},
            loose_nanos='NAUO2 / NAUO3 are one mesh each (nano_Varsayilan, 296070 vertices), the same model as the MRA Nano NAUO126 (0.007 mm), hovering 44.90 / 15.24 mm straight above the bench module seat; neither is seated',
            check=NC)
res = dict(source='PMG Build Instructions/pmg.glb', units='mm, assembly space, Y up',
           frame=dict(up=[0, 1, 0], front=[-1, 0, 0], back=[1, 0, 0], student_right=[0, 0, 1], student_left=[0, 0, -1], table_y=887.79, case_centre_z=1290.49,
                      case_box=[[456.98, 887.79, 1217.59], [601.16, 1006.73, 1363.35]], cadasio_frame='same as the GLB (component placements equal to 0.001 mm); Cadasio offsets are in each component\'s own axes'),
           wood_basic=L('wood_basic.json'), wood_planes=L('wood_planes.json'), codes=L('codes.json'),
           codes_for_guide={i: (c['face_normal'], c['centre']) for i, c in L('codes.json').items()},
           wood_contacts=L('wood_contacts.json'), wood_crossings=L('wood_crossings.json'),
           free_directions_stepgen=L('wood_free.json'),
           paths={os.path.basename(f)[11:-5]: json.load(open(f)) for f in sorted(glob.glob(SP + '/wood_paths_*.json'))},
           copies=C, module_compare=MC, nano=nano, pins=L('pins.json'),
           seats={**L('seats_NAUO76_NAUO83_NAUO84_NAUO85_NAUO79.json'), **L('seats_NAUO78_NAUO81_NAUO282.json')},
           cadasio_names=L('cadasio_names.json'), cadasio_only_copies=L('cadasio_copies.json'), usb_a_end_from_mra_glb=L('usb_a_mra.json'),
           usb_sets={'bench (plugged into the bench Nano)': ['NAUO279 right-angle plug', 'NAUO277 cable', 'NAUO278 A end'],
                     'built (plugged into NAUO78 from below)': ['NAUO282 right-angle plug', 'NAUO285 cable', 'NAUO283 A end'],
                     'held above (with NAUO94)': ['NAUO281 right-angle plug', 'NAUO284 cable', 'NAUO280 A end']})
for k in ['wood_contacts']:
    res[k]['pairs'] = [p for p in res[k]['pairs'] if p['max_depth'] > 0.05 or p['n_touch'] > 20]
json.dump(res, open(OUT, 'w'), indent=1)
print('written', OUT, os.path.getsize(OUT))
print(json.dumps(nano['poses_from_built'], indent=0))
