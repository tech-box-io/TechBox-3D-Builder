"""Critic's cross-checks of the four PMG research reports (JSON only; no mesh loading). Run with .venv.nosync/bin/python."""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
cm = json.load(open(HERE / 'cadasio_map.json'))
wp = json.load(open(HERE / 'wire-paths-draft.json'))
rp = json.load(open(HERE / 'reuse_poses.json'))
cs = json.load(open(HERE / 'cad_study.json'))
part = sys.argv[1] if len(sys.argv) > 1 else 'all'

if part in ('all', 'classify'):
    g = cm['glb_instances']
    ids = sorted(g, key=lambda s: int(s[4:]))
    print('instances', len(ids), 'first/last', ids[0], ids[-1])
    missing = [f'NAUO{i}' for i in range(1, 297) if f'NAUO{i}' not in g]
    print('not in cadasio_map.glb_instances:', missing)
    noroles = [i for i in ids if not g[i].get('role')]
    print('no role:', noroles)
    kinds = {}
    for i in ids:
        kinds.setdefault(g[i].get('kind'), []).append(i)
    for k, v in sorted(kinds.items(), key=lambda kv: -len(kv[1])):
        print(f'  {k!s:40} {len(v)}')

if part in ('all', 'wires'):
    print('wire-paths-draft keys (non NAUO):', [k for k in wp if not k.startswith('NAUO')])
    nauo = [k for k in wp if k.startswith('NAUO')]
    print('centre-line bodies:', len(nauo))
    # bodies in the cadasio_map routed/loose classes that have no centre line
    g = cm['glb_instances']
    roles = {i: (g[i].get('role') or '') for i in g}
    wireish = [i for i in g if re.search(r'wire|lead', roles[i], re.I) and not re.search(r'cap', roles[i], re.I)]
    print('cadasio_map wire/lead instances:', len(wireish))
    print('  without a centre line in the draft:', sorted(set(wireish) - set(nauo), key=lambda s: int(s[4:])))
    print('  centre lines not called wire/lead by cadasio_map:', sorted(set(nauo) - set(wireish), key=lambda s: int(s[4:])))
    # the wires list in the draft against cadasio_map's
    W = wp.get('wires')
    print('draft wires', len(W))
    for a, b in zip(cm['wires'], W):
        da = {p.get('pose'): [x.get('nauo') for x in (p.get('glb') if isinstance(p.get('glb'), list) else [])] for p in a['poses']}
        print(f"  step {a['step']:>2} {a['module']:<9} {a['module_pin']:<4} {a['shield_pin']:<4} {a['colour']}  | draft: {b.get('id')} {b.get('device_pin')} {b.get('module_pin')} {b.get('colour')}")
        print('      cm glb bodies:', {k: v for k, v in da.items() if v})
        print('      draft bodies :', {k: (v.get('body') if isinstance(v, dict) else v) for k, v in (b.get('poses') or {}).items()})

if part in ('all', 'poses'):
    print(json.dumps(rp['_about'])[:400])
    for grp in rp['groups']:
        print(json.dumps(grp)[:700])
        print()
