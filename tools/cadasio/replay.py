"""Per shown step of a Cadasio guide: which top-level components are visible, how far each is displaced from its CAD pose
(mm), whether it is rotated, and the camera (position, target in assembly mm).

    python tools/cadasio/replay.py <payload.json> <out.json>

Used for the LSM (docs/research/lsm/cadasio/replay.json): which pose copy of a part each published step shows, and where.
"""
import json, sys, math, collections
import numpy as np

j = json.load(open(sys.argv[1]))
steps, order, A = j['steps'], j['orderedSteps'], j['assemblyStructure']
MM = 1.0 / A['scaleFactor']
refs = {}


def walk(n, parent):
    r = n['rootReference']
    t = [float(x) for x in (r.get('transform') or '').split(',')] if r.get('transform') else []
    refs[r['id']] = dict(name=r['name'], parent=parent, hidden=bool(r.get('hidden')), kids=[c['rootReference']['id'] for c in n.get('children') or []],
                         home=tuple(t[12:15]) if len(t) == 16 else (0.0, 0.0, 0.0))
    for c in n.get('children') or []:
        walk(c, r['id'])


walk(A, None)
root = A['rootReference']['id']


def chain(k):
    out = []
    while k is not None:
        out.append(k); k = refs[k]['parent']
    return out


leaves = [k for k, v in refs.items() if not v['kids']]
CH = {k: chain(k) for k in leaves}
TOP = {k: (CH[k][-2] if len(CH[k]) >= 2 else k) for k in leaves}
nleaf = collections.Counter(TOP.values())
vis = {k: not any(refs[a]['hidden'] for a in chain(k)) for k in refs}
pos, rot = {}, {}
cam = dict((j.get('cameraProperties') or {}).get('default_camera') or {})


def v3(d):
    return (float(d.get('x', 0)), float(d.get('y', 0)), float(d.get('z', 0)))


out = []
n_shown = 0
for idx, sid in enumerate(order):
    s = steps[sid]
    for k, p in (s.get('properties') or {}).items():
        if not isinstance(p, dict) or k not in refs:
            if isinstance(p, dict) and p.get('cadasio_property_type') == 'camera' or k == 'default_camera':
                pass
            continue
        if p.get('visible') is not None:
            vis[k] = bool(p['visible'])
        if isinstance(p.get('position'), dict):
            pos[k] = v3(p['position'])
        if p.get('rotation') is not None:
            rot[k] = p['rotation']
    for k, p in (s.get('properties') or {}).items():
        if isinstance(p, dict) and (p.get('position') is not None and p.get('orbit_target') is not None):
            cam.update(p)
    if s.get('behaviour') == 'hidden':
        continue
    shown = collections.Counter()
    for k in leaves:
        if vis[k]:
            shown[TOP[k]] += 1
    comps = {}
    for t, n in shown.items():
        # displacement of the top component (its own position override) and of the deepest overridden ancestor of its leaves
        off = [0.0, 0.0, 0.0]
        p = pos.get(t)
        if p:
            h = refs[t]['home']; off = [(p[i] - h[i]) * MM for i in range(3)]
        sub = collections.Counter()
        for k in leaves:
            if TOP[k] == t and vis[k]:
                for a in CH[k][:-2]:
                    if a in pos:
                        h = refs[a]['home']; sub[tuple(round((pos[a][i] - h[i]) * MM, 1) for i in range(3))] += 1
        comps[refs[t]['name']] = dict(n=n, of=nleaf[t], off=[round(x, 1) for x in off], rot=t in rot, sub_offsets={str(k): v for k, v in sub.most_common(3)})
    c = None
    if cam.get('position') and cam.get('orbit_target'):
        c = dict(pos=[round(x * MM, 1) for x in v3(cam['position'])], target=[round(x * MM, 1) for x in v3(cam['orbit_target'])])
    out.append(dict(index=n_shown, name=s.get('name'), behaviour=s.get('behaviour'), camera=c, visible=comps))
    n_shown += 1
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(n_shown, 'shown steps')
