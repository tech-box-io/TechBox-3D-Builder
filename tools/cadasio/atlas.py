"""Per-solid colours of a named assembly in a published Cadasio guide (a "colour atlas").

    python tools/cadasio/atlas.py <payload.json> <out.json> <component name> [<component name> ...]

For each solid of the named top-level component: its bounding box (mm) and the colour it is displayed
with (the colour it has most often across the steps in which it is visible). tools/build_model.py uses
an atlas to colour our own CAD model of the same part: see "atlas" in a kit's materials.json.
"""
import json, sys, re, collections
src, out = sys.argv[1], sys.argv[2]; wanted = sys.argv[3:]
j = json.load(open(src)); A = j['assemblyStructure']; rv = A['rootVersions']; steps = j['steps']; MM = 1.0 / A['scaleFactor']
refs = {}
def walk(n, parent):
    r = n['rootReference']; refs[r['id']] = dict(name=r['name'], parent=parent, ver=r['childVersionId'], hidden=bool(r.get('hidden')), kids=[c['rootReference']['id'] for c in n.get('children') or []])
    for c in n.get('children') or []: walk(c, r['id'])
walk(A, None)
def kd(mtl):
    m = re.search(r'Kd\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)', mtl or '')
    return '#%02x%02x%02x' % tuple(max(0, min(255, round(float(x) * 255))) for x in m.groups()) if m else None
def leaves(k):
    if not refs[k]['kids']: yield k
    for c in refs[k]['kids']: yield from leaves(c)
def chain(k):
    while k is not None:
        yield k; k = refs[k]['parent']
tops = {w: [k for k, v in refs.items() if v['name'] == w] for w in wanted}
watch = {k: list(chain(k)) for w in wanted for t in tops[w][:1] for k in leaves(t)}
vis = {k: not any(refs[a]['hidden'] for a in chain(k)) for k in refs}; col = {}     # hidden is inherited once; solids are switched individually after that
seen = {k: collections.Counter() for k in watch}
for sid in j['orderedSteps']:
    s = steps[sid]
    for k, p in (s.get('properties') or {}).items():
        if k in refs and isinstance(p, dict):
            if p.get('visible') is not None: vis[k] = bool(p['visible'])
            if p.get('colour_main'): col[k] = p['colour_main']
    if s.get('behaviour') == 'hidden': continue
    for k, ch in watch.items():
        if vis[k]:
            c = next((col[a] for a in ch if a in col), None) or kd((rv.get(refs[k]['ver']) or {}).get('versionMtlData'))
            seen[k][c] += 1
res = {}
for w in wanted:
    if not tops[w]: print('not found', w); continue
    sol = []
    for k in leaves(tops[w][0]):
        v = rv.get(refs[k]['ver'])
        if not v: continue
        c = seen[k].most_common(1)[0][0] if seen[k] else (next((col[a] for a in watch[k] if a in col), None) or kd(v.get('versionMtlData')))
        sol.append(dict(name=refs[k]['name'].split('/')[-1], min=[round(v['versionMin' + a] * MM, 3) for a in 'XYZ'], max=[round(v['versionMax' + a] * MM, 3) for a in 'XYZ'], colour=c, shown=sum(seen[k].values())))
    lo = [min(s['min'][i] for s in sol) for i in range(3)]; hi = [max(s['max'][i] for s in sol) for i in range(3)]
    res[w] = dict(bbox_min=lo, bbox_max=hi, solids=sol)
    print(w, 'solids', len(sol), 'bbox mm', [round(h - l, 1) for l, h in zip(lo, hi)], 'colours', collections.Counter(s['colour'] for s in sol).most_common(14))
json.dump(res, open(out, 'w'))
