"""At-rest clearances (surface to surface, mm) of the new shapes in every view they appear in (parts posed as there; the buzzer and the
lead's own cap skipped, as wirecheck does; 5 mm at each end skipped)."""
import json
import numpy as np
from evalkit import clearance, model
import common
import build_final

S = json.load(open(common.SCR / 'steps_low.json'))
B = common.load_steps()
V = {v['name']: v for v in S['views']}
r = build_final.routes()
caps = {'red': 'NAUO58', 'black': 'NAUO59'}


def worst(view, pts, colour, poses=None, n=4):
    out = clearance(S, view, pts, skip=('NAUO62', caps[colour]), poses=poses, wire=f'buzzer {colour}')
    parts = [x for x in out if not x[1].startswith('wire')]
    wires = [x for x in out if x[1].startswith('wire')]
    return parts[:2], wires[:n]


if __name__ == '__main__':
    model()
    stops = {'lifted (stop 1, buzzer upright 70 mm over where it lay)': (0, build_final.ns['BUZZER_LIFT']),
             'held over the seat (stop 2)': (1, build_final.ns['BUZZER_UP']), 'over the seat, laid (stop 3)': (2, build_final.ns['BUZZER_UP'])}
    for label, (i, pose) in stops.items():
        for c in ('red', 'black'):
            p, w = worst('Step 43c', r[c][i]['pts'], c, poses={'NAUO62': pose})
            print(f'{label:55s} {c:5s} parts {p}  wires {w}')
    # the seated red (B') in every view it is in, against the old seated red
    new_no = V['Step 43c']['wires']['buzzer red']
    old_no = {v['name']: v for v in B['views']}['Step 43c']['wires']['buzzer red']
    rows = []
    for v in S['views']:
        if (v.get('wires') or {}).get('buzzer red') == new_no:
            pn, wn = worst(v['name'], S['routes'][new_no]['pts'], 'red', n=2)
            po, wo = worst(v['name'], B['routes'][old_no]['pts'], 'red', n=2)
            rows.append((v['name'], pn[:1], wn[:2], po[:1], wo[:1]))
            print(f"{v['name']:16s} new: parts {pn[:1]} wires {wn[:2]} | old: parts {po[:1]} wires {wo[:1]}", flush=True)
