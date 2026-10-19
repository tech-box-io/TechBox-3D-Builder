"""Match each pmg.glb top-level instance to a top-level component of TechBox's Cadasio project (by its placement:
the CAD transform's translation and rotation, mm), to get the component names (H2-1, Big Button Module-3 ...)."""
import json, sys, numpy as np
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from pmglib import Glb
from glbio import node_matrix
R = '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/cadasio/raw/19075-piano_memory_game_pmg-full_build.json'
d = json.load(open(R)); a = d['assemblyStructure']; s = a['scaleFactor']
cad = []
for c in a['children']:
    r = c['rootReference']
    m = np.array([float(x) for x in r['transform'].split(',')]).reshape(4, 4).T   # column-major
    cad.append(dict(name=r['name'], hidden=r['hidden'], R=m[:3, :3], t=m[:3, 3] / s, nchild=len(c['children'] or [])))
g = Glb('/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions/pmg.glb')
out = {}
used = set()
for name, ni in g.top.items():
    M = g.root_M @ node_matrix(g.nodes[ni])
    t = M[:3, 3] * 1000; Rm = M[:3, :3]
    best = None
    for k, c in enumerate(cad):
        e = np.linalg.norm(c['t'] - t) + 50 * np.linalg.norm(c['R'] - Rm)
        if best is None or e < best[0]:
            best = (e, k)
    c = cad[best[1]]
    out[name] = dict(cadasio=c['name'], err=round(float(best[0]), 3), hidden=c['hidden'])
    used.add(best[1])
for n, v in out.items():
    print(n, v)
print('cadasio components not matched:', [cad[k]['name'] for k in range(len(cad)) if k not in used][:200])
json.dump(out, open(sys.argv[1], 'w'), indent=0)
