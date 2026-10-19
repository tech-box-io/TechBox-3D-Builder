"""The pose copies TechBox's Cadasio project uses that the STEP does not have (display -6 / -7, matrix -8 / -9, module -2 / -3,
nano-3 / -4, USB ends), as rigid moves from the copy that is the built part in the STEP. Component transforms only (mm)."""
import json, sys, numpy as np
from scipy.spatial.transform import Rotation
RAW = '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/cadasio/raw/19075-piano_memory_game_pmg-full_build.json'
d = json.load(open(RAW)); a = d['assemblyStructure']; s = a['scaleFactor']
T = {}
for c in a['children']:
    r = c['rootReference']; m = np.array([float(x) for x in r['transform'].split(',')]).reshape(4, 4).T; m[:3, 3] /= s; T[r['name']] = m
def rel(src, dst, at):
    D = T[dst] @ np.linalg.inv(T[src]); rv = Rotation.from_matrix(D[:3, :3]).as_rotvec(); ang = np.degrees(np.linalg.norm(rv))
    at = np.asarray(at, float); t = D[:3, :3] @ at + D[:3, 3] - at
    return dict(t=t.round(2).tolist(), r=((rv / np.linalg.norm(rv)).round(4).tolist() + [round(float(ang), 2)]) if ang > 1e-3 else None, at=at.round(2).tolist())
out = {}
for base, at, others in (('Display TM1637-2', [564.03, 980.84, 1293.47], ['Display TM1637-1', 'Display TM1637-4', 'Display TM1637-5', 'Display TM1637-6', 'Display TM1637-7']),
                         ('LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-4', [532.48, 955.89, 1289.1], ['LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-1', 'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-6', 'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-7', 'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-8', 'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-9']),
                         ('Ensamblaje_Shield_NANO-1', [673.62, 889.37, 1299.3], ['Ensamblaje_Shield_NANO-2', 'Ensamblaje_Shield_NANO-3']),
                         ('nano-1', [673.0, 937.3, 1306.2], ['nano-2', 'nano-3', 'nano-4', 'nano-5']),
                         ('USB Right Angle-1', [667.0, 894.9, 1331.7], ['USB Right Angle-2', 'USB Right Angle-3']),
                         ('USB Cable end-1', [596.7, 876.8, 1398.9], ['USB Cable end-2', 'USB Cable end-3'])):
    for o in others:
        if o in T:
            out[f'{base} -> {o}'] = rel(base, o, at)
            print(f'{base} -> {o}:', out[f'{base} -> {o}'])
json.dump(out, open(sys.argv[1], 'w'), indent=1)
