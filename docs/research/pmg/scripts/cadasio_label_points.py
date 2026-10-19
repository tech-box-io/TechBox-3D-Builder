"""Where TechBox's Cadasio guide anchors each pin label, in assembly mm: the label's link 'target' point is taken as local to
the solid it is anchored to; it is carried to the assembly by the transforms of that solid and its parents."""
import json, sys, numpy as np
RAW = '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/cadasio/raw/19075-piano_memory_game_pmg-full_build.json'
DIG = '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/cadasio/19075-piano_memory_game_pmg-full_build.json'
d = json.load(open(RAW)); a = d['assemblyStructure']; s = a['scaleFactor']
refs = {}
def walk(n, parent):
    r = n['rootReference']
    T = np.array([float(x) for x in r['transform'].split(',')]).reshape(4, 4).T if r.get('transform') else np.eye(4)
    refs[r['id']] = dict(name=r['name'], parent=parent, T=T)
    for c in n.get('children') or []:
        walk(c, r['id'])
walk(a, None)
def world(i):
    M = np.eye(4)
    while i is not None:
        M = refs[i]['T'] @ M; i = refs[i]['parent']
    return M
dig = json.load(open(DIG))
name_text = {}
for st in dig['steps']:
    for t in st['tb_on']:
        if t['kind'] == 'label':
            name_text.setdefault(t.get('name'), set()).add((t['text'], tuple(t['anchored_to'])))
tp = d['toolboxComponentsProperties']
out = []
for k, v in tp.items():
    nm = v.get('name')
    for L in v.get('links', []):
        tid = L.get('targetId'); dd = L.get('data') or {}
        if tid not in refs or not dd.get('target'):
            continue
        p = np.array([dd['target'][c] for c in 'xyz'] + [1.0])
        w = world(tid) @ p
        texts = sorted(name_text.get(nm, []))
        out.append(dict(label=nm, texts=[t[0] for t in texts], target_solid=refs[tid]['name'], point_mm=(w[:3] / s).round(2).tolist()))
for o in sorted(out, key=lambda o: (o['target_solid'], o['label'])):
    if o['texts']:
        print(o['texts'], o['target_solid'], o['point_mm'])
json.dump(out, open(sys.argv[1], 'w'), indent=1)
