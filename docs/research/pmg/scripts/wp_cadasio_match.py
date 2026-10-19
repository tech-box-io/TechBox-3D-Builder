"""Match the Cadasio project's wire bodies and caps to pmg.glb's instances (same name, box within 0.5 mm). Prints both ways."""
import json, sys, re
import numpy as np
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from wp_glb import Glb
from wp_components import GLB
SP = '/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/bc7f208e-dd24-481f-9696-6a220688eb27/scratchpad/'
cw = json.load(open(SP + 'cadasio_wires.json'))
G = Glb(GLB); d = G.doc; T = G.top()


def ours():
    out = {}
    for inst, node in T.items():
        lo, hi = np.full(3, 1e9), np.full(3, -1e9)
        names = []
        for name, W, prims, ni in G.meshes_of(node):
            names.append(name)
            for p in prims:
                a = d['accessors'][p['attributes']['POSITION']]
                l, h = np.array(a['min']), np.array(a['max'])
                c = np.array([[x, y, z, 1] for x in (l[0], h[0]) for y in (l[1], h[1]) for z in (l[2], h[2])]) @ W.T
                lo = np.minimum(lo, c[:, :3].min(0) * 1000); hi = np.maximum(hi, c[:, :3].max(0) * 1000)
        out[inst] = dict(name=names[0].split('^')[0] if len(names) == 1 else d['nodes'][node].get('name'), lo=lo, hi=hi, n=len(names))
    return out


O = ours()
want = re.compile(r'^(Part\d+|Copy|Wire Cap|G11|S1 |S12|S13|V11|USB)')
rows = []
matched_ours = {}
for c in cw['comps']:
    base = (c['base'] or '').replace(' [Default]', '').split('^')[0]
    if not want.match(base) or c['lo'] is None:
        continue
    lo, hi = np.array(c['lo']), np.array(c['hi'])
    best = None
    for inst, o in O.items():
        if o['n'] != 1 and not base.startswith('USB'):
            continue
        dd = max(np.abs(o['lo'] - lo).max(), np.abs(o['hi'] - hi).max())
        if best is None or dd < best[0]:
            best = (dd, inst)
    same_name = O[best[1]]['name'].startswith(base.split(' [')[0]) if best else False
    c['ours'] = best[1] if best and best[0] < 0.6 else None
    c['box_diff_mm'] = round(float(best[0]), 2) if best else None
    if c['ours']:
        matched_ours.setdefault(c['ours'], []).append(c['name'])
    rows.append(c)
for c in sorted(rows, key=lambda c: (c['ours'] is None, int(c['ours'][4:]) if c['ours'] else 0, c['name'])):
    st = c['steps']
    span = f"{st[0]}-{st[-1]} ({len(st)})" if st else 'never'
    col = list(c['colours'].items())[:2]
    print(f"{str(c['ours']):8s} diff {c['box_diff_mm']:7.2f}  {c['name'][:58]:58s} vis {span:14s} {col}")
json.dump(dict(rows=rows, viewer=cw['viewer']), open(SP + 'cadasio_match.json', 'w'), indent=0)
print('ours matched twice', {k: v for k, v in matched_ours.items() if len(v) > 1})
wire_like = [i for i, o in O.items() if o['n'] == 1 and re.match(r'^(Part\d+|Copy|Wire Cap)', o['name'])]
print('ours not in Cadasio', [i for i in wire_like if i not in matched_ours])
