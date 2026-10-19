"""PMG: one line per Cadasio top-level component: visibility (viewer index ranges and step names), moves, nearest GLB.

    .venv.nosync/bin/python docs/research/pmg/scripts/summarize.py [name filter]

Reads work/cadasio_map/{cadasio_tree,replay,match}.json.
"""
import json, sys
import numpy as np
WORK = '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts/work/cadasio_map'
T = {t['id']: t for t in json.load(open(WORK + '/cadasio_tree.json'))['tops']}
R = json.load(open(WORK + '/replay.json'))
M = {m['cad_id']: m for m in json.load(open(WORK + '/match.json'))}
V = R['viewer']
flt = sys.argv[1] if len(sys.argv) > 1 else ''


def ranges(vs):
    out = []; s = None
    for v in vs:
        if s is None: s = p = v
        elif v == p + 1: p = v
        else: out.append((s, p)); s = p = v
    if s is not None: out.append((s, p))
    return out


def rtxt(vs):
    return ', '.join(f'[{a:03d}] {V[a]["name"]}' if a == b else f'[{a:03d}]-[{b:03d}] {V[a]["name"]}..{V[b]["name"]}' for a, b in ranges(vs))


if __name__ == '__main__':
    for cid, t in sorted(T.items(), key=lambda x: x[1]['idx']):
        if flt and flt not in t['name']: continue
        r = R['tops'][cid]; m = M[cid]
        c = ((np.array(t['min']) + np.array(t['max'])) / 2).round(1).tolist()
        offs = sorted(set(tuple(o) for o in r['off'].values()))
        print(f"{t['name']} (idx{t['idx']}) c={c} -> {m['best']} err {m['box_err']} | vis: {rtxt(r['vis']) or 'never'}"
              + (f" | partial {r['partial']}" if r['partial'] else '') + (f" | offsets {offs[:4]}{'...' if len(offs) > 4 else ''}" if offs else '')
              + (f" | rot at {sorted(r['rot'])[:3]}..." if r['rot'] else ''))
