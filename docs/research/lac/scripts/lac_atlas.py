"""Per-solid colours of TechBox's published LAC Cadasio project, keyed by the mesh names of our CAD export (lac.glb)."""
import json, re, collections, sys
src, out = sys.argv[1], sys.argv[2]
want = set(sys.argv[3].split('|'))
j = json.load(open(src)); A = j['assemblyStructure']; rv = A['rootVersions']; steps = j['steps']; MM = 1.0 / A['scaleFactor']
refs = {}
def walk(n, parent):
    r = n['rootReference']; refs[r['id']] = dict(name=r['name'], parent=parent, ver=r['childVersionId'], hidden=bool(r.get('hidden')), kids=[c['rootReference']['id'] for c in n.get('children') or []])
    for c in n.get('children') or []: walk(c, r['id'])
walk(A, None)
def kd(mtl):
    m = re.search(r'Kd\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)', mtl or '')
    return '#%02x%02x%02x' % tuple(max(0, min(255, round(float(x) * 255))) for x in m.groups()) if m else None
def chain(k):
    while k is not None:
        yield k; k = refs[k]['parent']
def leaves(k):
    if not refs[k]['kids']: yield k
    for c in refs[k]['kids']: yield from leaves(c)
vis = {k: not any(refs[a]['hidden'] for a in chain(k)) for k in refs}; col = {}
seen = collections.defaultdict(collections.Counter)
leafset = [k for k in refs if not refs[k]['kids']]
for sid in j['orderedSteps']:
    s = steps[sid]
    for k, p in (s.get('properties') or {}).items():
        if k in refs and isinstance(p, dict):
            if p.get('visible') is not None: vis[k] = bool(p['visible'])
            if p.get('colour_main'): col[k] = p['colour_main']
    if s.get('behaviour') == 'hidden': continue
    for k in leafset:
        if vis[k]:
            c = next((col[a] for a in chain(k) if a in col), None) or kd((rv.get(refs[k]['ver']) or {}).get('versionMtlData'))
            seen[k][c] += 1
base = lambda name: re.sub(r'-\d+$', '', name.split('/')[-1])
res, single = {}, {}
# The Cadasio copy to read a part's colours from where its copies differ: the buzzer's lying copy, whose red stub is the one wired to j4
# (the clamped copy has the stubs the other way round: Lee, 21 Oct 2026, docs/research/lac/round2/buzzer_leads.md).
PREFER = {'Piezo Buzzer': 'Piezo Buzzer-1'}
for k, r in refs.items():
    b = base(r['name'])
    if b not in want or b in res or b in single: continue
    if b in PREFER and r['name'].split('/')[-1] != PREFER[b]: continue
    sol = []
    for L in leaves(k):
        v = rv.get(refs[L]['ver'])
        if not v or v.get('versionMinX') in (None, 'None'): continue
        c = seen[L].most_common(1)[0][0] if seen[L] else (next((col[a] for a in chain(L) if a in col), None) or kd(v.get('versionMtlData')))
        sol.append(dict(name=refs[L]['name'].split('/')[-1], min=[round(float(v['versionMin' + a]) * MM, 3) for a in 'XYZ'], max=[round(float(v['versionMax' + a]) * MM, 3) for a in 'XYZ'], colour=c, shown=sum(seen[L].values()),
                        **({'skin': True} if 'Surface-Offset' in refs[L]['name'] else {})))   # (a coloured face copy: the face under it takes its colour, as the LSM's make_atlas.py)
    if not sol: continue
    if not any(s['shown'] for s in sol):
        continue                                   # an instance never shown: try another
    cols = collections.Counter(s['colour'] for s in sol)
    if len(cols) == 1:
        single[b] = sol[0]['colour']
    else:
        lo = [min(s['min'][i] for s in sol) for i in range(3)]; hi = [max(s['max'][i] for s in sol) for i in range(3)]
        res[b] = dict(bbox_min=lo, bbox_max=hi, solids=sol, cadasio_instance=r['name'])
    print(b, len(sol), dict(cols.most_common(8)))
print('missing', sorted(want - set(res) - set(single)))
json.dump(dict(_single_colour=single, **res), open(out, 'w'))
