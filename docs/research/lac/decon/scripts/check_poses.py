"""Compare the published take-apart's posed copies with the CAD copies' poses in wire-paths.json (and the build's published poses):
each pose applied to the seated box's 8 corners; the largest gap in mm."""
import json, sys
from pathlib import Path
import numpy as np
from scipy.spatial.transform import Rotation
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lacpub import WIRES, HOME, BY_NAME, top_leaves, r2
d = json.load(open(Path(__file__).resolve().parents[1] / 'published_geometry.json'))
wp = json.load(open(WIRES))['poses']
def apply(pose, P):
    if isinstance(pose, list): return P + np.array(pose)
    ax = np.array(pose['r'][:3]); ax /= np.linalg.norm(ax)
    R = Rotation.from_rotvec(ax * np.radians(pose['r'][3])).as_matrix()
    at = np.array(pose['at']); return (P - at) @ R.T + at + np.array(pose['t'])
def corners(name):
    lo, hi = HOME.world_box(top_leaves[BY_NAME[name]], home=True)
    return np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
first = {}
for r in d['frames']:
    for a in r['appear'] + r['moved']:
        if a.get('pose') is not None and a['part'] not in first:
            first[a['part']] = (r['frame'], a['pose'])
pairs = [('F1-2', 'F1-1', 'F1_hover_front'), ('F1-4', 'F1-1', 'F1_flat_other_end'), ('LAC Potentiometer-4', 'LAC Potentiometer-1', 'pot_flat_other_end'),
         ('LAC Knob-4', 'LAC Knob-1', 'knob_flat_other_end'), ('LCD V1-2', 'LCD V1-1', 'lcd_lying'), ('LCD V1-5', 'LCD V1-1', 'lcd_standing_out'),
         ('Piezo Buzzer-1', 'Piezo Buzzer-2', 'buzzer_lying'), ('Rocker Switch-2', 'Rocker Switch-1', 'switch_flat_F4'),
         ('Rocker Switch-3', 'Rocker Switch-1', 'switch_hover')]
for copy, seat, key in pairs:
    f, pose = first[copy]
    P = corners(seat)
    gap = np.abs(apply(pose, P) - apply(wp[key], P)).max(axis=1)
    mean_d = (apply(pose, P) - apply(wp[key], P)).mean(0)
    print(f'{copy:22s} (frame {f:3d}) vs wire-paths {key:20s}: largest gap {gap.max():.2f} mm, mean offset {r2(mean_d)}')
