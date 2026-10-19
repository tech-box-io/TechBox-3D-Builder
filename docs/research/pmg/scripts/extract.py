"""Extract chosen top-level instances of pmg.glb into a small npz cache (vertices mm + faces, per instance and per mesh node).
Usage: extract.py OUT.npz NAUO60 NAUO61 ..."""
import sys, numpy as np
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from pmglib import Glb
g = Glb('/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions/pmg.glb')
out = {}
for t in sys.argv[2:]:
    V, F, parts = g.instance_geometry(t)
    out[f'{t}__V'] = V.astype(np.float64)
    out[f'{t}__F'] = F.astype(np.int32)
    out[f'{t}__parts'] = np.array([f'{a}|{b}|{c}|{d}' for a, b, c, d in parts])
np.savez_compressed(sys.argv[1], **out)
print('saved', sys.argv[1], len(sys.argv) - 2)
