"""PMG reuse study: (1) is the Cadasio project's frame the GLB's? (2) the colours Cadasio shows on chosen components, per solid,
with each component's world box, so that a colour can be tied to one of our instances by where it sits.

    python3 docs/research/pmg/scripts/reuse_cadasio_frame.py

Colours: the colour a solid has most often across the steps in which it is visible (tools/cadasio/atlas.py's rule).
"""
import collections
import json
import re
import sys

import numpy as np

sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from reuse_hdr import Glb  # noqa: E402

ROOT = '/Users/lee-johnson/Desktop/Claude_Cadasio/'
j = json.load(open(ROOT + 'docs/research/pmg/cadasio/raw/19075-piano_memory_game_pmg-full_build.json'))
A = j['assemblyStructure']
rv = A['rootVersions']
steps = j['steps']
MM = 1.0 / A['scaleFactor']
refs = {}


def mat(s):
    M = np.array([float(x) for x in s.split(',')]).reshape(4, 4).T
    M[:3, 3] *= MM
    return M


def walk(n, parent, W):
    r = n['rootReference']
    M = W @ mat(r['transform']) if r.get('transform') else W
    refs[r['id']] = dict(name=r['name'], parent=parent, ver=r['childVersionId'], hidden=bool(r.get('hidden')), W=M,
                         kids=[c['rootReference']['id'] for c in n.get('children') or []])
    for c in n.get('children') or []:
        walk(c, r['id'], M)


walk(A, None, np.eye(4))
root = A['rootReference']['id']


def kd(mtl):
    m = re.search(r'Kd\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)', mtl or '')
    return '#%02x%02x%02x' % tuple(max(0, min(255, round(float(x) * 255))) for x in m.groups()) if m else None


def leaves(k):
    if not refs[k]['kids']:
        yield k
    for c in refs[k]['kids']:
        yield from leaves(c)


def chain(k):
    while k is not None:
        yield k
        k = refs[k]['parent']


def box(k):
    pts = []
    for x in leaves(k):
        v = rv.get(refs[x]['ver'])
        if not v:
            continue
        lo = [v['versionMin' + a] * MM for a in 'XYZ']
        hi = [v['versionMax' + a] * MM for a in 'XYZ']
        c = np.array([[a, b, cc, 1] for a in (lo[0], hi[0]) for b in (lo[1], hi[1]) for cc in (lo[2], hi[2])]) @ refs[x]['W'].T
        pts.append(c[:, :3])
    P = np.vstack(pts)
    return P.min(0), P.max(0)


# colours seen while visible, every solid
vis = {k: not any(refs[a]['hidden'] for a in chain(k)) for k in refs}
col, seen = {}, collections.defaultdict(collections.Counter)
solids = [k for k in refs if not refs[k]['kids'] and rv.get(refs[k]['ver'])]
for sid in j['orderedSteps']:
    s = steps[sid]
    for k, p in (s.get('properties') or {}).items():
        if k in refs and isinstance(p, dict):
            if p.get('visible') is not None:
                vis[k] = bool(p['visible'])
            if p.get('colour_main'):
                col[k] = p['colour_main']
    if s.get('behaviour') == 'hidden':
        continue
    for k in solids:
        if vis[k]:
            c = next((col[a] for a in chain(k) if a in col), None) or kd(rv[refs[k]['ver']].get('versionMtlData'))
            seen[k][c] += 1

if __name__ == '__main__':
    PMG = Glb(ROOT + 'PMG Build Instructions/pmg.glb')
    top = PMG.top()
    gbox = {}
    for name, i in top.items():
        P = [np.array([[a, b, c, 1] for a in (lo[0], hi[0]) for b in (lo[1], hi[1]) for c in (lo[2], hi[2])]) @ W.T for (_, _, lo, hi, _, W) in PMG.mesh_nodes(i)]
        P = np.vstack(P)[:, :3]
        gbox[name] = (P.min(0), P.max(0))
    print('== frame check: Cadasio top-level components whose world box matches a GLB instance box (to 0.5 mm)')
    hits, misses = 0, []
    for k in refs[root]['kids']:
        lo, hi = box(k)
        best = min(gbox, key=lambda n: np.abs(np.r_[gbox[n][0] - lo, gbox[n][1] - hi]).max())
        err = np.abs(np.r_[gbox[best][0] - lo, gbox[best][1] - hi]).max()
        if err < 0.5:
            hits += 1
        else:
            misses.append((refs[k]['name'], round(float(err), 1)))
    print(f'  {hits} of {len(refs[root]["kids"])} Cadasio components land on a GLB instance; not: {len(misses)}')
    print('  ', misses[:12])
    want = sys.argv[1:] or ['Big Button Module', 'Display TM1637', 'LED Matrix', 'USB Right Angle', 'USB Cable end', 'Wire Cap-1', 'H4v2']
    for k in refs[root]['kids']:
        name = refs[k]['name']
        if not any(name.startswith(w) for w in want):
            continue
        lo, hi = box(k)
        best = min(gbox, key=lambda n: np.abs(np.r_[gbox[n][0] - lo, gbox[n][1] - hi]).max())
        err = np.abs(np.r_[gbox[best][0] - lo, gbox[best][1] - hi]).max()
        shown = sum(sum(seen[x].values()) for x in leaves(k) if x in seen)
        cols = collections.Counter()
        for x in leaves(k):
            if x in seen and seen[x]:
                cols[seen[x].most_common(1)[0][0]] += 1
        print(f'- {name}{" (hidden)" if refs[k]["hidden"] else ""}: box {np.round(lo, 1).tolist()} .. {np.round(hi, 1).tolist()}; '
              f'nearest GLB {best} ({err:.1f} mm); solid-steps shown {shown}; colours {dict(cols)}')
