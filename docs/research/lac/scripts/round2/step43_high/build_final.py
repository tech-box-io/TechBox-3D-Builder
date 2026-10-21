"""Runs the paste-ready patch (guide_patch.txt) the way guide.py would, with guide.py's own helpers (common.py), and writes steps-final.json:
Step 43's path and its leads' routes replaced as the generator writes them."""
import json
import numpy as np
import common
from common import *
ns = {k: getattr(common, k) for k in ('W', 'np', 'unit', 'tidy', 'compose', 'wire_at', 'into_hole', 'posed_line', 'BUZZER', 'BUZZER_LYING',
                                      'BUZZER_LEADS', 'ZERO')}
exec(open('guide_patch.txt').read(), ns)
routes = {}
for c, cap, _, e, _, _ in BUZZER_LEADS:
    routes[f'buzzer {c}'] = [ns['buzzer_plugged'](c, cap, e, ns['BUZZER_LIFT'], ns['BUZZER_LIFT_WAY'][c], stretch=True, hold=ns['BUZZER_LIFT_HOLD'].get(c)),
                             ns['buzzer_high'](c, cap, e), ns['buzzer_clamped'](c, cap, e)]
    lying = ns['buzzer_plugged'](c, cap, e, ns['BUZZER_LYING'], ns['BUZZER_WAY'][c])
    assert same_route(lying, STEPS['routes'][VIEWS['Step 42c']['wires'][f'buzzer {c}']]), 'lying route changed!'
path = [ns['BUZZER_LYING'], ns['BUZZER_LIFT'], ns['BUZZER_HIGH'], ZERO]
write_steps(Path(__file__).resolve().parent / 'steps-final.json', path, routes)
ref = json.load(open('routes-cand13.json'))['routes']
for w, rs in routes.items():
    for a, b in zip(rs, ref[w]):
        pa, pb = np.asarray(a['pts']), np.asarray(b['pts'])
        d = float(np.abs(pa - pb).max()) if pa.shape == pb.shape else None
        print(w, len(pa), 'max diff vs cand11', d, {k: a[k] for k in a if k not in ('pts', 'b_ref')}, '| cand11', {k: b[k] for k in b if k not in ('pts', 'b_ref')})
print('lying routes unchanged; wrote steps-final.json')
