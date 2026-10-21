import sys, json
from pathlib import Path
import numpy as np
ROOT = Path('/Users/lee-johnson/Desktop/Claude_Cadasio'); sys.path.insert(0, str(ROOT / 'tools'))
from stepgen import Model
kit = ROOT / 'LAC Build Instructions'; spec = json.load(open(kit / 'materials.json'))
model = Model(kit / spec['source'], adjust=spec.get('adjust_mm') or {}, own_parts=spec.get('own_parts', {}),
              extra_parts={i: (kit / e['glb'], e['pose']) for i, e in spec.get('extra_parts', {}).items()})
f9, f3 = model.inst['NAUO45'], model.inst['NAUO2']
# outline of F9 in the xy plane (its face at z max): vertices on the face
V = f9.vertices; face = V[abs(V[:, 2] - V[:, 2].max()) < 0.01]
low = face[face[:, 1] < 892]
print('F9 face vertices below y 892 (x, y):')
for p in sorted(set((round(x, 2), round(y, 2)) for x, y, _ in low)): print('  ', p)
W = f3.vertices; s = W[(abs(W[:, 2] - 1355.8) < 5) & (W[:, 0] > 685) & (W[:, 0] < 725)]
print('F3 vertices near F9 (x, z):', sorted(set((round(x, 2), round(z, 2)) for x, _, z in s)))
