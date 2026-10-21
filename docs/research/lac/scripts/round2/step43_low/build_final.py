"""The steps copy for the design as guide.py would write it (the paste-ready code run in a copy of guide.py's buzzer helpers)."""
import sys, copy, json
import numpy as np
import common
from guide_patch import PATCH, SEAT_RED
from evalkit import with_design

ns = vars(common)
ns['BUZZER_SEAT_WAY'] = copy.deepcopy(common.BUZZER_SEAT_WAY)
exec(SEAT_RED, ns)
exec(PATCH, ns)
PATH = [ns['BUZZER_LYING'], ns['BUZZER_LIFT'], ns['BUZZER_UP'], ns['BUZZER_UP'], ns['ZERO']]


def routes():
    out = {}
    for c, cap, _, e, _, _ in common.BUZZER_LEADS:
        out[c] = [ns['buzzer_lifted'](c, cap, e), ns['buzzer_held'](c, cap, e), ns['buzzer_over_seat'](c, cap, e), ns['buzzer_clamped'](c, cap, e)]
    return out


def steps_copy(name='steps_low.json'):
    base = common.load_steps()
    r = routes()
    for c in r:                                    # (round as stepgen writes routes: W.route already rounds the points to 0.01)
        pass
    S = with_design(base, dict(path=PATH, red=r['red'], black=r['black']))
    p = common.SCR / name
    json.dump(S, open(p, 'w'))
    return S, p


if __name__ == '__main__':
    S, p = steps_copy()
    print(p)
