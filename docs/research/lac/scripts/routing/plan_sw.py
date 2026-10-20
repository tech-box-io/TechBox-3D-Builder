import time
from planner import *
from eval_in import IN, lines as in_lines
exec(open('plan_up.py').read().split("print('UP =")[0].split('done, ctl_up')[0])   # (imports only)
UP = {'black': [[781.2, 900.0, 1240.0], [771.3, 900.0, 1240.0], [761.5, 900.3, 1240.3], [753.2, 904.0, 1244.0], [746.5, 909.2, 1249.2], [736.8, 911.0, 1251.0], [726.9, 911.0, 1251.2], [717.3, 911.0, 1253.2], [708.0, 911.2, 1257.1]] + IN['black'][2:],
      'red': [[781.7, 900.0, 1233.0], [771.7, 900.0, 1233.0], [761.7, 900.0, 1233.0], [751.5, 900.2, 1233.6], [742.5, 902.1, 1236.7], [733.6, 903.0, 1241.0], [724.3, 903.0, 1245.2], [715.1, 903.0, 1249.4]] + IN['red'][2:],
      'tan': [[781.6, 903.1, 1237.0], [771.5, 904.0, 1237.0], [761.5, 904.0, 1237.0], [751.8, 904.6, 1237.1], [741.9, 906.5, 1237.7], [731.8, 907.0, 1238.2], [722.2, 907.0, 1240.3], [713.0, 907.0, 1244.4]] + IN['tan'][1:]}
SWL = {'red': ('NAUO47', [672.52, 929.76, 1258.37]), 'tan': ('NAUO49', [679.52, 929.76, 1258.37]), 'black': ('NAUO48', [686.52, 929.76, 1258.37])}
SWW = ('switch red', 'switch tan', 'switch black')
VIEWS_SW = [f'Step {k}c' for k in range(48, 57)] + [f'Step {k}' for k in range(49, 57)]
pot_in = in_lines(IN)
FO = PATHS['poses']['F1_hover_front']
pot_up = {c: into_hole(POTL[c][0], *start(c, FO)[1:], UP[c]) for c in UP}
def other_wires(view):
    """Every wire but the switch's in a view, the pot leads as they will be."""
    out = []
    v = VIEWS[view]; k = int(''.join(ch for ch in view.split()[1] if ch.isdigit()))
    for w, ri in v['wires'].items():
        if w in SWW: continue
        if w.startswith('pot') and k >= 52: continue
        out.append((np.asarray(S['routes'][ri]['pts']), RAD[w]))
    if k >= 53 or view == 'Step 53': out += [(L, 0.625) for L in pot_in.values()]
    if view in ('Step 52c', 'Step 53'): out += [(L, 0.625) for L in pot_up.values()]
    return out
import sys
NEED, EVERY = float(sys.argv[1]), float(sys.argv[2])
if __name__ == '__main__':
    BOX = ([652.0, 886.0, 1244.0], [702.0, 951.0, 1288.0])
    extra_all = [x for v in ('Step 48c', 'Step 50c', 'Step 51c', 'Step 52c', 'Step 56c') for x in other_wires(v)]
    done, ctl = {}, {}
    t0 = time.time()
    for c in ('tan', 'red', 'black'):
        cap, ex = SWL[c]; e = np.asarray(ex, float); d = np.array([0.0, -1.0, 0.0])
        a, b = e + d * 6.0, wire_at(cap) + [0.0, 14.0, 0.0]
        drops = [(np.array([wire_at(SWL[o][0]) + [0, 14.0, 0], wire_at(SWL[o][0]) + [0, 2.0, 0]]), 0.625) for o in SWL if o != c and o not in done]
        F = Field('Step 56c', BOX, skip=(cap, 'NAUO46'), exclude=POTW + SWW, extra=extra_all + drops + [(done[o], 0.625) for o in done])
        print(c, 'clear at start', round(float(F.clear[F.idx(a)]), 2), 'goal', round(float(F.clear[F.idx(b)]), 2), flush=True)
        path = astar(F, a, b, need=NEED, free_near=(a, b))
        if path is None:
            print(c, 'NO PATH'); continue
        ctl[c] = controls_from(path, every=EVERY, trim=3.0)
        done[c] = into_hole(cap, e, d, ctl[c])
        print(c, ctl[c], round(time.time() - t0, 1), 's', flush=True)
    print('mutual', mutual(done))
    print('SW =', ctl)
