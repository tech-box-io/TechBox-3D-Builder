"""Our LAC Full Build, one row per step, for docs/research/lac/decon/study_map.md (read-only; steps.json only).

    python3 -I docs/research/lac/decon/scripts/build_table.py

Columns: step, caption (cut), moved in by a path (`moving`, the way's first pose and stage count), moved by a ride (carry poses that change
from the view before Step N to Step Nc, by what), routes that change (N's route -> Nc's), Step N's camera."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
s = json.load(open(ROOT / 'LAC Build Instructions/steps.json'))
V, names = s['views'], s['names']
nm = lambda i: names.get(i, i)


def short(p):
    if isinstance(p, dict):
        r = p.get('r') or [0, 0, 0, 0]
        return f"t{[round(x, 1) for x in p['t']]} r{round(r[3], 1)}deg"
    return str([round(x, 1) for x in p])


def cam(c):
    return f"{[round(x, 3) for x in c['dir']]} / {[round(x, 1) for x in c['target']]} / {c['radius']}"


prev = None
for k, v in enumerate(V):
    if v['kind'] not in ('hover', 'done'):
        continue
    if v['kind'] == 'done':
        prev = v
        continue
    done = V[k + 1]
    moved = []
    for i in v.get('moving') or []:
        own = (v.get('paths') or {}).get(i) or v['path']
        if all(p == [0.0, 0.0, 0.0] for p in own):
            continue                                  # (a dummy 'stay' way)
        moved.append(f"{i} ({nm(i)}) from {short(own[0])}, {len(own) - 1} stage(s)")
    rides = []
    before = (prev or {}).get('carry') or {}
    for i, c in (done.get('carry') or {}).items():
        b = before.get(i)
        if b != c and c.get('pose') is not None:
            frm = short(b['pose']) if b else 'appears'
            rides.append(f"{i} ({nm(i)}) on {c['by']}: {frm} -> {short(c['pose'])}{' +' + str(len(c['via'])) + ' via' if c.get('via') else ''}")
    wires = []
    pw = (prev or {}).get('wires') or {}
    for w, n in (done.get('wires') or {}).items():
        a = v.get('wires', {}).get(w)
        if pw.get(w) != n or a != n:
            wires.append(f"{w} {pw.get(w)}|{a}->{n}{' via ' + str(done['wire_via'][w]) if (done.get('wire_via') or {}).get(w) else ''}")
    print(f"| {v['name']} | {v.get('caption', '')[:70]} | {'; '.join(moved) or '-'} | {'; '.join(rides) or '-'} | {'; '.join(wires) or '-'} | {cam(v['camera'])} |")
    prev = done
