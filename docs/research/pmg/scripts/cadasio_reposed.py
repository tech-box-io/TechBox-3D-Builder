"""Components whose placement TechBox's Cadasio project overrides (a 'position'/'rotation' set on a top-level component, not on a
solid), and where H14 ends up in the Completed View, compared with its CAD pose (NAUO74)."""
import json, sys, numpy as np
from scipy.spatial.transform import Rotation
RAW = '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/cadasio/raw/19075-piano_memory_game_pmg-full_build.json'
d = json.load(open(RAW)); a = d['assemblyStructure']; s = a['scaleFactor']
refs = {}; top = set()
def walk(n, parent, depth):
    r = n['rootReference']
    T = np.array([float(x) for x in r['transform'].split(',')]).reshape(4, 4).T if r.get('transform') else np.eye(4)
    refs[r['id']] = dict(name=r['name'], parent=parent, T=T)
    if depth == 1: top.add(r['id'])
    for c in n.get('children') or []: walk(c, r['id'], depth + 1)
walk(a, None, 0)
state = {}
for sid in d['orderedSteps']:
    st = d['steps'][sid]
    for k, p in (st.get('properties') or {}).items():
        if k in top and isinstance(p, dict) and (p.get('position') or p.get('rotation')):
            print('component override:', st['name'], st.get('behaviour'), refs[k]['name'], 'pos(mm)', {c: round(v / s, 1) for c, v in (p.get('position') or {}).items()}, 'rot', p.get('rotation'))
        if k in refs and isinstance(p, dict):
            e = state.setdefault(k, {})
            if p.get('position') is not None: e['pos'] = p['position']
            if p.get('rotation') is not None: e['rot'] = p['rotation']
    if st['name'] == 'Completed View':
        break
h14 = next(k for k in top if refs[k]['name'] == 'H14-1')
def M(pos, rot):
    m = np.eye(4)
    if rot: m[:3, :3] = Rotation.from_quat([rot['x'], rot['y'], rot['z'], rot['w']]).as_matrix()
    if pos: m[:3, 3] = [pos['x'], pos['y'], pos['z']]
    return m
Tc = refs[h14]['T'].copy()
e = state.get(h14, {})
Tn = Tc.copy()
if e:
    Tn = M(e.get('pos') or {'x': Tc[0, 3], 'y': Tc[1, 3], 'z': Tc[2, 3]}, e.get('rot'))
    if not e.get('rot'): Tn[:3, :3] = Tc[:3, :3]
sol = next(k for k in refs if refs[k]['name'] == 'H14-1/H14-Cut-Extrude1')
es = state.get(sol, {})
Ts = M(es.get('pos'), es.get('rot')) if es else np.eye(4)
Tw_cad = Tc; Tw_fin = Tn @ Ts
D = Tw_fin @ np.linalg.inv(Tw_cad)       # CAD world -> Cadasio final world (in units)
D[:3, 3] /= s
rv = Rotation.from_matrix(D[:3, :3]).as_rotvec()
print('H14 component CAD transform t(mm)', (Tc[:3, 3] / s).round(1), ' override', e, ' solid at Completed View', es)
print('H14: Cadasio final = CAD pose moved by: turn', np.degrees(np.linalg.norm(rv)).round(2), 'deg about', (rv / max(np.linalg.norm(rv), 1e-9)).round(3), 'then t', D[:3, 3].round(1))
json.dump(dict(D=D.tolist()), open(sys.argv[1], 'w'))
