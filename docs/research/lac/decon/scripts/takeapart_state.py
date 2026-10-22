"""What take_apart() would start from for the LAC, read from its steps.json only (light JSON, no CAD): a mirror of tools/stepgen.py
Guide.take_apart()'s `came` records and its starting state (placed, riding, resting, wire_state), plus, per part, which record
remove() / lift() / unplug() would use by default (`fits[-1]`, the latest record whose group is wholly leaving: here, the part alone or
its whole group). Study aid for docs/research/lac/decon/study_api.md (21 Oct 2026).

    python3 docs/research/lac/decon/scripts/takeapart_state.py ["LAC Build Instructions"]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
KIT = ROOT / (sys.argv[1] if len(sys.argv) > 1 else 'LAC Build Instructions')
data = json.loads((KIT / 'steps.json').read_text(encoding='utf-8'))
views, routes, names = data['views'], data['routes'], data.get('names', {})


def moved(p):
    if p is None:
        return False
    if isinstance(p, dict):
        return bool(p.get('r') and p['r'][3]) or any(abs(x) > 1e-6 for x in p.get('t', [0, 0, 0]))
    return any(abs(x) > 1e-6 for x in p)


def zero_way(way):
    return all(not moved(p) for p in way)


came, before = {}, None
for k, v in enumerate(views):
    if v['kind'] == 'hover' and v.get('moving') and not v.get('wiggle'):
        nxt = views[k + 1] if k + 1 < len(views) and views[k + 1]['kind'] == 'done' else {}
        for i in v['moving']:
            own = (v.get('paths') or {}).get(i)
            way = own or v['path']
            came.setdefault(i, []).append(dict(
                index=k, name=v['name'], group=list(v['moving']), way=way, still=zero_way(way), isolated=bool(v.get('isolated')),
                flip=bool(v['camera'].get('flip')), wire_via={w: nos for w, nos in (nxt.get('wire_via') or {}).items()},
                wires=dict(v.get('wires') or {}), rode=((before or {}).get('carry') or {}).get(i)))
    if v['kind'] in ('hover', 'done'):
        before = v

end = views[-1]
states = [v for v in views if v['kind'] in ('hover', 'done')]
placed = list(end['visible'])
offsets, carry = dict(end.get('offsets') or {}), dict(end.get('carry') or {})
wires_now = {w: no for w, no in (end.get('wires') or {}).items()}
for v in reversed(states):
    for i in v['visible']:
        if i not in placed:
            placed.append(i)
            offsets[i] = (v.get('offsets') or {}).get(i)
            if i in (v.get('carry') or {}):
                carry[i] = v['carry'][i]
    for w, no in (v.get('wires') or {}).items():
        r = routes[no]
        if w not in wires_now and all(e is None or e in placed for e in (r.get('a'), r.get('b'))):
            wires_now[w] = no

print(f"{KIT.name}: {len(views)} views, {len(routes)} routes; Completed View shows {len(end['visible'])} parts; take_apart() "
      f"would start from {len(placed)} parts, {len(wires_now)} leads")
extra = [i for i in placed if i not in end['visible']]
if extra:
    print('  parts the Completed View does not show, taken from the last view that did (leave_out= candidates):',
          [(i, names.get(i)) for i in extra])
print('\nRiding at the end (carry):')
for i, c in carry.items():
    print(f"  {i:10s} {names.get(i, ''):26s} on {c['by']:8s} {names.get(c['by'], ''):14s} pose {'ZERO' if not moved(c['pose']) else c['pose']}")
print('\nResting off its seat at the end:', {i: p for i, p in offsets.items() if i not in carry and moved(p)} or 'none')
print('\nLeads at the end (route no, a end -> b end):')
for w, no in wires_now.items():
    r = routes[no]
    print(f"  {w:20s} #{no:<4d} a={r.get('a')} ({names.get(r.get('a'), '')})  b={r.get('b')} ({names.get(r.get('b'), '')})"
          + ''.join(f'  {k}={r[k]}' for k in ('stretch', 'tail_from', 'b_from', 'a_from', 'b_whole', 'a_whole') if k in r))
print('\nFull Build records (came) per part, oldest first; * = the record remove()/lift() uses for the part taken off alone (fits[-1]):')
for i in placed:
    recs = came.get(i, [])
    alone = [m for m in recs if set(m['group']) <= {i}]
    use = alone[-1] if alone else None
    tag = '' if recs else '  NO RECORD (came in by ride=, appear= or show= only)'
    print(f"  {i:10s} {names.get(i, ''):26s}{tag}")
    for m in recs:
        star = '*' if m is use else ' '
        print(f"     {star} {m['name']:9s} group={m['group']} stops={len(m['way'])} {'STILL WAY (all ZERO)' if m['still'] else ''}"
              f"{' flip' if m['flip'] else ''}{' isolated' if m['isolated'] else ''}"
              f"{' rode=' + m['rode']['by'] if m['rode'] else ''}{' wire_via=' + str(list(m['wire_via'])) if m['wire_via'] else ''}")
