"""Replay the Cadasio PMG Full Build (raw payload) per solid, as tools/cadasio/digest.py does, and record for every top-level
component: its bounding box in mm (Cadasio frame = pmg.glb's), the viewer steps where it is visible, its offset from its CAD
place at each of those steps, and its colour while visible. Writes scratchpad cadasio_wires.json."""
import json, re, collections
import numpy as np

SRC = '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/cadasio/raw/19075-piano_memory_game_pmg-full_build.json'
OUT = '/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/bc7f208e-dd24-481f-9696-6a220688eb27/scratchpad/cadasio_wires.json'
j = json.load(open(SRC))
steps, order, A = j['steps'], j['orderedSteps'], j['assemblyStructure']
SF = A['scaleFactor']; MM = 1.0 / SF
rv = A['rootVersions']
refs = {}


def walk(n, parent, M):
    r = n['rootReference']
    t = [float(x) for x in r['transform'].split(',')] if r.get('transform') else None
    T = np.array(t).reshape(4, 4) if t else np.eye(4)          # row-vector convention: p' = p @ T
    W = T @ M
    refs[r['id']] = dict(name=r['name'], parent=parent, ver=r['childVersionId'], hidden=bool(r.get('hidden')),
                         kids=[c['rootReference']['id'] for c in n.get('children') or []], home=tuple(t[12:15]) if t else (0, 0, 0), W=W)
    for c in n.get('children') or []:
        walk(c, r['id'], W)


walk(A, None, np.eye(4))
root = A['rootReference']['id']
tops = refs[root]['kids']
leaves = [k for k, v in refs.items() if not v['kids']]


def chain(k):
    out = []
    while k is not None:
        out.append(k); k = refs[k]['parent']
    return out


CH = {k: chain(k) for k in refs}
TOP = {k: (CH[k][-2] if len(CH[k]) >= 2 else k) for k in leaves}
top_leaves = collections.defaultdict(list)
for k in leaves:
    top_leaves[TOP[k]].append(k)


def kd_hex(mtl):
    m = re.search(r'Kd\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)', mtl or '')
    return '#%02x%02x%02x' % tuple(max(0, min(255, round(float(x) * 255))) for x in m.groups()) if m else None


def bbox_mm(k):
    """World box of a leaf (mm), from its version's own box through its transforms."""
    v = rv.get(refs[k]['ver']) or {}
    if 'versionMinX' not in v:
        return None
    lo = np.array([v['versionMinX'], v['versionMinY'], v['versionMinZ']]); hi = np.array([v['versionMaxX'], v['versionMaxY'], v['versionMaxZ']])
    c = np.array([[x, y, z, 1] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]) @ refs[k]['W']
    return (c[:, :3].min(0) * MM, c[:, :3].max(0) * MM)


base_col = {k: kd_hex((rv.get(refs[k]['ver']) or {}).get('versionMtlData')) for k in leaves}
vis = {k: not any(refs[a]['hidden'] for a in CH[k]) for k in refs}
pos, col = {}, {}


def eff_pos(k):
    x = y = z = 0.0
    for a in CH[k]:
        p = pos.get(a)
        if p:
            h = refs[a]['home']; x += p[0] - h[0]; y += p[1] - h[1]; z += p[2] - h[2]
    return (x * MM, y * MM, z * MM)


def eff_col(k):
    for a in CH[k]:
        if a in col:
            return col[a]
    return base_col.get(k)


rec = {t: dict(name=refs[t]['name'], base=(rv.get(refs[t]['ver']) or {}).get('versionComponentName'), steps=[], offsets={}, colours=collections.Counter(),
               n_solids=len(top_leaves[t])) for t in tops}
viewer = []
for sid in order:
    s = steps[sid]
    for k, p in (s.get('properties') or {}).items():
        if not isinstance(p, dict) or k not in refs:
            continue
        if p.get('visible') is not None:
            vis[k] = bool(p['visible'])
        if isinstance(p.get('position'), dict):
            pos[k] = (float(p['position'].get('x', 0)), float(p['position'].get('y', 0)), float(p['position'].get('z', 0)))
        if p.get('colour_main'):
            col[k] = p['colour_main']
    if s.get('behaviour') == 'hidden':
        continue
    vi = len(viewer); viewer.append(s['name'])
    for t in tops:
        ls = [k for k in top_leaves[t] if vis[k]]
        if not ls:
            continue
        r = rec[t]
        r['steps'].append(vi)
        off = np.mean([eff_pos(k) for k in ls], axis=0)
        if np.linalg.norm(off) > 0.05:
            r['offsets'][vi] = np.round(off, 2).tolist()
        for k in ls:
            r['colours'][eff_col(k)] += 1
out = []
for t in tops:
    r = rec[t]
    boxes = [bbox_mm(k) for k in top_leaves[t]]
    boxes = [b for b in boxes if b is not None]
    lo = np.min([b[0] for b in boxes], 0) if boxes else None
    hi = np.max([b[1] for b in boxes], 0) if boxes else None
    out.append(dict(id=t, name=r['name'], base=r['base'], n_solids=r['n_solids'], lo=None if lo is None else np.round(lo, 2).tolist(),
                    hi=None if hi is None else np.round(hi, 2).tolist(), steps=r['steps'], offsets=r['offsets'], colours=dict(r['colours'].most_common())))
json.dump(dict(viewer=viewer, comps=out), open(OUT, 'w'), indent=0)
print(len(viewer), 'viewer steps', len(out), 'components')
