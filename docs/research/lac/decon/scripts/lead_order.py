"""Leads unplugged in the published take-apart's order: does a lead pass through another still plugged in? (read-only; steps.json only)

    python3 -I docs/research/lac/decon/scripts/lead_order.py

The moving lead is its route as it lies at that point (the routes our take-apart would have there), its plug moved straight out the way
the Full Build pushed it in (the first stage only: up out of its hole), blended along the lead as player.js does (ramp, b_from). Every
other lead still there is taken as drawn (its parts at the poses it was drawn for, as they are at that point). Centre lines closer than
1.25 mm (two radii; the USB cable 0.625 + 1.75) mean the tubes pass into each other: listed with how close they lie at rest."""
import json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[5]
s = json.load(open(ROOT / 'LAC Build Instructions/steps.json'))
R, W = s['routes'], s['wires']
ramp = lambda x: (lambda t: t * t * (3 - 2 * t))(min(1.0, max(0.0, (x - 0.1) / 0.8)))


def pts(n):
    return np.asarray(R[n]['pts'], float)


def shares(n):
    r, P = R[n], pts(n)
    seg = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
    L = seg[-1]
    out = []
    for x in seg:
        if r.get('b_from'):
            u = (x - r['b_from']) / max(1e-6, L - r['b_from'])
        else:
            u = x / L
        out.append(ramp(u) if r.get('b') else 0.0)
    return np.array(out)[:, None]          # how much each point goes with b


def sweep(n, end, way, k=24):
    """Positions of route n while its `end` ('a' or 'b') moves along `way` (list of translations from where it is)."""
    P, wb = pts(n), shares(n)
    w = 1.0 if end == 'both' else (wb if end == 'b' else 1 - wb)   # ('both': a loose wire lifted by both its caps)
    stops = [np.zeros(3)] + [np.asarray(d, float) for d in way]
    for a, b in zip(stops, stops[1:]):
        for t in np.linspace(0, 1, k)[1:]:
            yield P + w * (a + (b - a) * t)


def radius(name):
    return W[name]['radius']


def check(label, moving, statics):
    print(f'\n{label}')
    for name, n, end, way in moving:
        hits = []
        for oname, o in statics.items():
            if oname == name:
                continue
            Q = pts(o)
            rest = float(np.min(np.linalg.norm(pts(n)[:, None] - Q[None], axis=2)))
            close = min(float(np.min(np.linalg.norm(P[:, None] - Q[None], axis=2))) for P in sweep(n, end, way))
            touch = radius(name) + radius(oname)
            if close < touch and close < rest - 0.05:
                hits.append(f'{oname} {close:.2f} (rest {rest:.2f}, touch {touch:.2f})')
        print(f'  {name:14s} route {n:3d}: ' + ('; '.join(hits) if hits else 'clear'))


JUMPERS = {f'jumper {c}': n for c, n in (('black', 21), ('green', 22), ('purple', 23), ('blue', 24), ('white', 25), ('dark_red', 26),
                                         ('orange', 36), ('yellow', 37))}
SWITCH_FLAT = {'switch red': 30, 'switch tan': 31, 'switch black': 32}      # F4 lying flat behind the case (Step 48's start)
BUZZER_SEATED = {'buzzer red': 79, 'buzzer black': 80}
BUZZER_LYING = {'buzzer red': 52, 'buzzer black': 53}                       # lifted back out (Step 43 reversed)
LCD_LYING = {'lcd purple': 90, 'lcd yellow': 91, 'lcd teal': 92, 'lcd blue': 93}   # laid back face down (Steps 52, 51 reversed)
POT_ASIDE = {'pot red': 81, 'pot tan': 82, 'pot black': 83}                 # F1 face down in front (Step 53 reversed)
USB = {'usb cable': 125}

# Published order: pot (9 - 11, black, tan, red) with the LCD lying, the buzzer seated, F4 flat, every jumper in.
state = {**POT_ASIDE, **LCD_LYING, **BUZZER_SEATED, **SWITCH_FLAT, **JUMPERS}
for name, hold in (('pot black', 5.0), ('pot tan', 18.0), ('pot red', 18.0)):
    check(f'pub {9 + ["pot black", "pot tan", "pot red"].index(name)}: {name} up {hold} mm', [(name, state[name], 'a', [[0, hold, 0]])], state)
    state.pop(name)
# LCD wires (19 - 22, GND VCC SDA SCL), both ends: the male up 18, the female off its pin (the LCD face down: -15 z in the world)
for name in ('lcd purple', 'lcd yellow', 'lcd teal', 'lcd blue'):
    check(f'pub 19-22: {name}, male up 18 (b end -15 z)', [(name, state[name], 'a', [[0, 18, 0]])], state)
    state.pop(name)
# buzzer leads (29 red, 30 black) with the buzzer lying again
state.update(BUZZER_LYING)
check('pub 29: buzzer red up 5 (its Full Build hold)', [('buzzer red', state['buzzer red'], 'a', [[0, 5, 0]])], state)
check('ours, reversed: buzzer black up 18 first', [('buzzer black', state['buzzer black'], 'a', [[0, 18, 0]])], state)
state.pop('buzzer red'); state.pop('buzzer black')
# switch leads (32 black, 33 tan, 34 red): b = the cap
for name, hold in (('switch black', 5.0), ('switch tan', 18.0), ('switch red', 18.0)):
    check(f'pub 32-34: {name} up {hold}', [(name, state[name], 'b', [[0, hold, 0]])], state)
    state.pop(name)

# ------------------------------------------------------------------ the Full Build's own order, reversed (for comparison)
print('\n==== our Full Build reversed: the buzzer lifted back out first, then the LCD wires, the buzzer leads, the pot leads ====')
for pot_routes, where in ((POT_ASIDE, 'F1 face down in front (Step 47c pose: routes 81-83)'),
                          ({'pot red': 47, 'pot tan': 48, 'pot black': 49}, 'F1 moved back beside the breadboard end (Step 47 undone: routes 47-49)')):
    print(f'\n-- {where}')
    state = {**pot_routes, **LCD_LYING, **BUZZER_LYING, **SWITCH_FLAT, **JUMPERS}
    for name in ('lcd blue', 'lcd teal', 'lcd yellow', 'lcd purple'):
        check(f'{name}, male up 18', [(name, state[name], 'a', [[0, 18, 0]])], state)
        state.pop(name)
    check('buzzer black up 18', [('buzzer black', state['buzzer black'], 'a', [[0, 18, 0]])], state)
    state.pop('buzzer black')
    check('buzzer red up 5', [('buzzer red', state['buzzer red'], 'a', [[0, 5, 0]])], state)
    state.pop('buzzer red')
    for name, hold in (('pot black', 5.0), ('pot tan', 18.0), ('pot red', 18.0)):
        check(f'{name} up {hold}', [(name, state[name], 'a', [[0, hold, 0]])], state)
        state.pop(name)
    for name, hold in (('switch black', 5.0), ('switch tan', 18.0), ('switch red', 18.0)):
        check(f'{name} up {hold}', [(name, state[name], 'b', [[0, hold, 0]])], state)
        state.pop(name)

print('\n==== the published order, with F1 moved back beside the breadboard end first (Step 47 undone: routes 47-49) ====')
state = {'pot red': 47, 'pot tan': 48, 'pot black': 49, **LCD_LYING, **BUZZER_SEATED, **SWITCH_FLAT, **JUMPERS}
for name, hold in (('pot black', 5.0), ('pot tan', 18.0), ('pot red', 18.0)):
    check(f'{name} up {hold}', [(name, state[name], 'a', [[0, hold, 0]])], state)
    state.pop(name)

print('\n==== F1 back beside (routes 47-49), the buzzer lifted back out (lying, its leads plugged: 52, 53), the LCD lying ====')
state = {'pot red': 47, 'pot tan': 48, 'pot black': 49, **LCD_LYING, **BUZZER_LYING, **SWITCH_FLAT, **JUMPERS}
for name, hold in (('pot black', 5.0), ('pot tan', 18.0), ('pot red', 18.0)):
    check(f'{name} up {hold}', [(name, state[name], 'a', [[0, hold, 0]])], state)
    state.pop(name)
print('\n==== the LCD wires in the published order with the buzzer lying (52, 53) and F1 back beside (47-49) ====')
state = {'pot red': 47, 'pot tan': 48, 'pot black': 49, **LCD_LYING, **BUZZER_LYING, **SWITCH_FLAT, **JUMPERS}
for name in ('lcd purple', 'lcd yellow', 'lcd teal', 'lcd blue'):
    check(f'{name}, male up 18', [(name, state[name], 'a', [[0, 18, 0]])], state)
    state.pop(name)
print('\n==== the jumpers, both caps straight up 18 (white, dark red: their first 5 only) with every other jumper in (jumper_order.py has the full ways) ====')
state = dict(JUMPERS)
for name in JUMPERS:
    hold = 5.0 if name in ('jumper white', 'jumper dark_red') else 18.0
    check(f'{name} up {hold}', [(name, state[name], 'both', [[0, hold, 0]]), ], {k: v for k, v in state.items()})
