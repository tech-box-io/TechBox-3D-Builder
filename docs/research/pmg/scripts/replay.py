"""PMG: replay the published Cadasio guide and record, for every top-level component, in which viewer steps it is
visible, where it is (offset from its CAD pose, mm) and whether it is turned; and every viewer step's camera.

    .venv.nosync/bin/python docs/research/pmg/scripts/replay.py

Rules (docs/cadasio-patterns.md, Appendix A; tools/cadasio/digest.py does the same): step properties are changes on
top of the previous step in orderedSteps, hidden steps included (a hidden step's changes show in the next shown step);
visibility is per solid (a solid starts hidden if it or an ancestor carries the CAD hidden flag, then is switched by its
own entries); a part's `position` replaces the translation of its CAD transform (offset = position - CAD translation);
mm = scene units / scaleFactor. Viewer index [000]-[116] = the shown (non-hidden) steps in order, as in the digest.
Writes work/replay.json.
"""
import json, math, collections
import numpy as np
ROOT = '/Users/lee-johnson/Desktop/Claude_Cadasio'
PAY = ROOT + '/docs/research/pmg/cadasio/raw/19075-piano_memory_game_pmg-full_build.json'
WORK = ROOT + '/docs/research/pmg/scripts/work/cadasio_map'
j = json.load(open(PAY))
A = j['assemblyStructure']; MM = 1.0 / A['scaleFactor']; steps = j['steps']; order = j['orderedSteps']
refs = {}


def walk(n, parent, top, Rpar=np.eye(3)):
    """Rpar: the world rotation of the parent's frame (CAD transforms only). A ref's `position` is in its parent's frame,
    so its world offset is Rpar @ (position - CAD translation): for a solid inside a part, the part's own rotation."""
    r = n['rootReference']
    t = [float(x) for x in r['transform'].split(',')] if r.get('transform') else []
    Rown = np.array(t).reshape(4, 4).T[:3, :3] if len(t) == 16 else np.eye(3)
    refs[r['id']] = dict(name=r['name'], parent=parent, top=top, hidden=bool(r.get('hidden')), kids=[c['rootReference']['id'] for c in n.get('children') or []],
                         home=tuple(t[12:15]) if len(t) == 16 else (0.0, 0.0, 0.0), Rpar=Rpar)
    for c in n.get('children') or []:
        walk(c, r['id'], top if top else (c['rootReference']['id'] if parent is None else None), Rpar @ Rown)


root = A['rootReference']['id']
refs[root] = dict(name=A['rootReference']['name'], parent=None, top=None, hidden=False, kids=[c['rootReference']['id'] for c in A['children']], home=(0, 0, 0))
for c in A['children']:
    walk(c, root, c['rootReference']['id'])
tops = [c['rootReference']['id'] for c in A['children']]


def chain(k):
    out = []
    while k is not None:
        out.append(k); k = refs[k]['parent']
    return out


CH = {k: chain(k) for k in refs}
leaves = [k for k, v in refs.items() if not v['kids'] and k != root]
top_leaves = collections.defaultdict(list)
for k in leaves: top_leaves[refs[k]['top']].append(k)
# the sub-assembly (depth-2) each leaf belongs to, for the shield's Nano
sub_of = {k: (CH[k][-3] if len(CH[k]) >= 4 else None) for k in leaves}

vis = {k: not any(refs[a]['hidden'] for a in CH[k]) for k in refs}
pos = {}; rot = {}; col = {}
cam = dict((j.get('cameraProperties') or {}).get('default_camera') or {})
scene = {}
for sc in (j.get('scenes') or {}).values(): scene.update(sc)
scene_ids = set((j.get('scenes') or {}).keys())


def v3(d): return (float(d.get('x', 0)), float(d.get('y', 0)), float(d.get('z', 0)))


def eff_off(k):
    """world offset (mm) of a solid from its CAD pose, from the `position` overrides on it and its ancestors."""
    o = np.zeros(3)
    for a in CH[k]:
        p = pos.get(a)
        if p:
            o += refs[a].get('Rpar', np.eye(3)) @ (np.array(p) - np.array(refs[a]['home']))
    o = o * MM
    return (round(float(o[0]), 1), round(float(o[1]), 1), round(float(o[2]), 1))


def qrot(q, v):
    x, y, z, w = q['x'], q['y'], q['z'], q['w']
    R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                  [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                  [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
    return R @ np.array(v)


viewer = []
tvis = {t: [] for t in tops}           # viewer idxs where any leaf of the top is visible
tfull = {t: [] for t in tops}          # ... where all are
toff = {t: {} for t in tops}           # viewer idx -> offset mm (mode over visible leaves), only if non-zero
trot = {t: {} for t in tops}           # viewer idx -> rotation quaternion set on the top ref (if any)
tpart = {t: {} for t in tops}          # viewer idx -> count of visible leaves when partial
tcol = {t: collections.Counter() for t in tops}   # colour shown (leaf-steps), as tools/cadasio/atlas.py counts it
rv = A['rootVersions']
ver = {}
def _walkver(n):
    r = n['rootReference']; ver[r['id']] = r['childVersionId']
    for c in n.get('children') or []: _walkver(c)
for c in A['children']: _walkver(c)
import re as _re
def kd(mtl):
    m = _re.search(r'Kd\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)', mtl or '')
    return '#%02x%02x%02x' % tuple(max(0, min(255, round(float(x) * 255))) for x in m.groups()) if m else None
base = {k: kd((rv.get(ver.get(k)) or {}).get('versionMtlData')) for k in leaves}
subvis = collections.defaultdict(list)  # (top, sub name) -> viewer idxs where that sub-assembly is visible
v = -1
for oi, sid in enumerate(order):
    s = steps[sid]; P = s.get('properties') or {}
    for k, p in P.items():
        if not isinstance(p, dict): continue
        if k in refs:
            if p.get('visible') is not None: vis[k] = bool(p['visible'])
            if isinstance(p.get('position'), dict): pos[k] = v3(p['position'])
            if isinstance(p.get('rotation'), dict): rot[k] = p['rotation']
            if p.get('colour_main'): col[k] = p['colour_main']
        elif k == 'default_camera': cam.update(p)
        elif k in scene_ids: scene.update(p)
    if s.get('behaviour') == 'hidden': continue
    v += 1
    c = None
    if cam.get('position') and cam.get('orbit_target'):
        pp, tt = np.array(v3(cam['position'])), np.array(v3(cam['orbit_target']))
        d = pp - tt; n = float(np.linalg.norm(d))
        up = qrot(cam['rotation'], (0, 1, 0)) if cam.get('rotation') else None
        c = dict(dir=(d / n).round(4).tolist(), target_mm=(tt * MM).round(1).tolist(), eye_mm=(pp * MM).round(1).tolist(), dist_mm=round(n * MM, 1),
                 up=None if up is None else np.round(up, 4).tolist(), fov=cam.get('fov'),
                 elev_deg=round(math.degrees(math.asin(max(-1, min(1, d[1] / n)))), 1), azim_deg=round(math.degrees(math.atan2(d[0], d[2])), 1))
    viewer.append(dict(v=v, name=s['name'], behaviour=s['behaviour'], order_index=oi, camera=c, up_axis=scene.get('up_axis')))
    for t in tops:
        ls = top_leaves[t]
        vv = [k for k in ls if vis[k]]
        if not vv: continue
        tvis[t].append(v)
        if len(vv) == len(ls): tfull[t].append(v)
        else: tpart[t][v] = len(vv)
        offs = collections.Counter(eff_off(k) for k in vv)
        o = offs.most_common(1)[0][0]
        if any(abs(x) > 0.05 for x in o): toff[t][v] = list(o)
        if t in rot: trot[t][v] = rot[t]
        for k in vv:
            tcol[t][next((col[a] for a in CH[k] if a in col), None) or base[k]] += 1
        for k in vv:
            if sub_of[k]: subvis[(t, refs[sub_of[k]]['name'].split('/')[-1])].append(v)

out = dict(viewer=viewer, tops={t: dict(name=refs[t]['name'], nleaves=len(top_leaves[t]), vis=tvis[t], full=tfull[t], partial=tpart[t], off=toff[t], rot=trot[t], colours=tcol[t].most_common(6)) for t in tops},
           subs={f'{refs[t]["name"]}|{n}': sorted(set(vs)) for (t, n), vs in subvis.items() if 'nano' in n.lower()})
json.dump(out, open(WORK + '/replay.json', 'w'))
print('viewer steps', len(viewer))
print('tops ever visible', sum(1 for t in tops if tvis[t]), 'never', sum(1 for t in tops if not tvis[t]))
