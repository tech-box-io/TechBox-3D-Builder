"""Which breadboard jumper can come off before which, by the wires alone (read-only, light: steps.json only).

    python3 -I docs/research/lac/decon/scripts/jumper_order.py

Each jumper leaves the way the Full Build put it in, reversed (both caps move alike, so its route moves rigidly with them): sampled at
40 moments along that way; it is blocked by another jumper still there if their centre lines come closer than 1.25 mm (two radii)
at any moment. Parts are not tested here (the generator's collision test does that); the RTC, resistors and Nano are still in."""
import json, itertools
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[5]
s = json.load(open(ROOT / 'LAC Build Instructions/steps.json'))
V = {v['name']: v for v in s['views']}
R = s['routes']
end = V['Completed View']
J = {w: np.array(R[n]['pts']) for w, n in end['wires'].items() if w.startswith('jumper ')}
step_of = {}
for v in s['views']:
    if v['kind'] == 'hover' and v.get('moving'):
        for w in J:
            r = R[end['wires'][w]]
            if r['a'] in v['moving'] and w not in step_of:
                own = v.get('paths') or {}
                step_of[w] = (v['name'], own.get(r['a']) or v['path'], own.get(r['b']) or v['path'])
ramp = lambda s: (lambda t: t * t * (3 - 2 * t))(min(1.0, max(0.0, (s - 0.1) / 0.8)))   # (player.js: the ends stay with their parts)
SH = {}
for w, P in J.items():
    seg = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
    SH[w] = np.array([ramp(x) for x in seg / seg[-1]])[:, None]   # share that goes with b
def way_points(path, k=40):
    """Positions of a translation-only way, reversed (from the seat out), sampled."""
    pts = [np.array(p if isinstance(p, list) else p['t'], float) for p in path[::-1]]
    out = []
    for a, b in zip(pts, pts[1:]):
        for t in np.linspace(0, 1, k // max(1, len(pts) - 1) + 1):
            out.append(a + (b - a) * t)
    return out
def blocked(w, other):
    best = 1e9
    for da, db in list(zip(way_points(step_of[w][1]), way_points(step_of[w][2])))[1:]:   # (not the seat itself: two seated wires may touch)
        P = J[w] + (1 - SH[w]) * da + SH[w] * db
        dist = np.min(np.linalg.norm(P[:, None, :] - J[other][None, :, :], axis=2))
        best = min(best, dist)
    return best
names = sorted(J, key=lambda w: int(step_of[w][0].split()[1]))
print('jumper, Full Build step, way in:')
for w in names:
    print(f'  {w:16s} {step_of[w][0]:8s} a {step_of[w][1]}  b {step_of[w][2]}')
print('\nclosest approach (mm, centre lines) of A leaving while B is still in; < 1.25 = passes through it:')
for a in names:
    row = []
    for b in names:
        if a == b: continue
        m = blocked(a, b)
        rest = float(np.min(np.linalg.norm(J[a][:, None, :] - J[b][None, :, :], axis=2)))
        if m < 3.0:
            row.append(f'{b.split()[1]} {m:.2f} (at rest {rest:.2f}){" BLOCKED" if m < 1.25 and m < rest - 0.05 else ""}')
    print(f'  {a:16s} ' + ('; '.join(row) or 'clear of all (> 3 mm)'))
