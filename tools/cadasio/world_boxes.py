"""World boxes of every top-level component of a Cadasio project (assembly mm), from the leaf versions' boxes.

    python tools/cadasio/world_boxes.py <payload.json> <out.json>

Used for the LSM (docs/research/lsm/cadasio/cadasio_world_boxes.json): where each published part sits, to rebuild a broken
assembly from loose parts (LSM Build Instructions/assemble.py). Each entry: id, CAD-hidden flag, component, tooltip, world box, the
4x4 placement (mm), solids.
"""
import json, sys, collections
import numpy as np

j = json.load(open(sys.argv[1]))
A = j['assemblyStructure']; rv = A['rootVersions']; MM = 1 / A['scaleFactor']
refs = {}


def walk(n, parent):
    r = n['rootReference']
    refs[r['id']] = dict(name=r['name'], parent=parent, ver=r['childVersionId'], t=r['transform'], hidden=bool(r.get('hidden')),
                         kids=[c['rootReference']['id'] for c in n.get('children') or []])
    for c in n.get('children') or []:
        walk(c, r['id'])


walk(A, None)
root = A['rootReference']['id']


def mat(k):
    t = [float(x) for x in refs[k]['t'].split(',')] if refs[k]['t'] else None
    if not t or len(t) != 16:
        return np.eye(4)
    m = np.array(t).reshape(4, 4).T     # column-major
    m[:3, 3] *= MM
    return m


def world(k):
    m = np.eye(4)
    while k is not None:
        m = mat(k) @ m
        k = refs[k]['parent']
    return m


desc = {}
for sid in j['orderedSteps']:
    for kk, vv in (j['steps'][sid].get('metaProperties') or {}).items():
        if isinstance(vv, dict) and isinstance(vv.get('Description'), str):
            desc.setdefault(kk, vv['Description'])


def leaves(k):
    if not refs[k]['kids']:
        yield k
    for c in refs[k]['kids']:
        yield from leaves(c)


out = {}
for k in refs[root]['kids']:
    los, his, nsol = [], [], 0
    for lf in leaves(k):
        v = rv.get(refs[lf]['ver']) or {}
        if v.get('versionMinX') is None:
            continue
        lo = np.array([v['versionMin' + a] for a in 'XYZ']) * MM; hi = np.array([v['versionMax' + a] for a in 'XYZ']) * MM
        c = np.array([[x, y, z, 1] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
        w = (world(lf) @ c.T).T[:, :3]
        los.append(w.min(0)); his.append(w.max(0)); nsol += 1
    if not los:
        continue
    lo, hi = np.min(los, 0), np.max(his, 0)
    W = world(k)
    out[refs[k]['name']] = dict(id=k, hidden=refs[k]['hidden'], comp=(rv.get(refs[k]['ver']) or {}).get('versionComponentName'),
                                desc=collections.Counter(desc.get(x) for x in [k] + list(leaves(k)) if desc.get(x)).most_common(1)[0][0] if any(desc.get(x) for x in [k] + list(leaves(k))) else None,
                                lo=lo.round(2).tolist(), hi=hi.round(2).tolist(), centre=((lo + hi) / 2).round(2).tolist(), size=(hi - lo).round(2).tolist(),
                                matrix=W.round(6).tolist(), solids=nsol)
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(len(out), 'components')
