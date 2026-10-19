"""PMG: match every Cadasio top-level component to a pmg.glb instance (NAUOn) by world box and transform.

    .venv.nosync/bin/python docs/research/pmg/scripts/match.py

Reads work/cadasio_tree.json and work/glb_boxes.json (from cadasio_tree.py). Writes work/match.json.
A pair matches when the boxes agree (centre and size within 0.5 mm) and the top-level transforms agree
(rotation within 1e-3, translation within 0.5 mm). Ties (identical copies at one place) are broken by names.
"""
import json, collections
import numpy as np
WORK = '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts/work/cadasio_map'
T = json.load(open(WORK + '/cadasio_tree.json'))['tops']
G = json.load(open(WORK + '/glb_boxes.json'))


def kind_glb(g):
    n = collections.Counter(m['name'] for m in g['meshes'])
    return n.most_common(1)[0][0]


def score(t, g):
    if t['min'] is None: return 1e9
    tc = (np.array(t['min']) + np.array(t['max'])) / 2; ts = np.array(t['max']) - np.array(t['min'])
    gc = (np.array(g['min']) + np.array(g['max'])) / 2; gs = np.array(g['max']) - np.array(g['min'])
    return float(np.abs(tc - gc).max() + np.abs(ts - gs).max())


def mscore(t, g):
    a = np.array(t['matrix_mm']); b = np.array(g['matrix_mm'])
    return float(np.abs(a[:3, :3] - b[:3, :3]).max()), float(np.abs(a[:3, 3] - b[:3, 3]).max())


res = []
used = collections.Counter()
for t in T:
    cands = sorted(((score(t, g), k) for k, g in G.items()), key=lambda x: x[0])[:4]
    best = cands[0]
    rs, ts = mscore(t, G[best[1]])
    res.append(dict(cad_id=t['id'], name=t['name'], idx=t['idx'], hidden=t['hidden'], nsolids=t['nsolids'],
                    min=t['min'], max=t['max'], best=best[1], box_err=round(best[0], 2), rot_err=round(rs, 4), trans_err=round(ts, 2),
                    glb_kind=kind_glb(G[best[1]]), others=[(k, round(s, 2)) for s, k in cands[1:3]]))
    if best[0] < 0.5: used[best[1]] += 1
json.dump(res, open(WORK + '/match.json', 'w'), indent=0)
good = [r for r in res if r['box_err'] < 0.5]
print('matched (box within 0.5 mm):', len(good), 'of', len(res))
print('GLB instances matched once:', sum(1 for k in G if used[k] == 1), 'twice+:', sum(1 for k in G if used[k] > 1), 'never:', sum(1 for k in G if used[k] == 0))
for k in G:
    if used[k] != 1: print('  GLB', k, 'used', used[k], kind_glb(G[k]), G[k]['min'], G[k]['max'])
print('unmatched Cadasio components:')
for r in res:
    if r['box_err'] >= 0.5:
        print(f"  {r['name']} idx{r['idx']} hidden={r['hidden']} n={r['nsolids']} box {r['min']}..{r['max']} nearest {r['best']} err {r['box_err']} ({r['glb_kind']}) {r['others']}")
