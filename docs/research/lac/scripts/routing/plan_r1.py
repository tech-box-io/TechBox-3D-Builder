"""Lee's first round: the switch's leads lying (F4 35 mm nearer) and the potentiometer's leads with F1 face down in front, planned through
the parts and wires of every view they lie in."""
import sys, time, json
from planner import *
def union_wires(views, exclude):
    out, seen = [], set()
    for vn in views:
        v = VIEWS[vn]
        for w, ri in (v.get('wires') or {}).items():
            if any(w.startswith(x) for x in exclude) or ri in seen: continue
            seen.add(ri); out.append((np.asarray(S['routes'][ri]['pts']), RAD[w]))
    return out
which = sys.argv[1]
if which == 'switch':
    FLAT = np.array([-82.68, 17.26, -0.06])
    EX = {'red': ('NAUO47', [672.52, 929.76, 1258.37]), 'tan': ('NAUO49', [679.52, 929.76, 1258.37]), 'black': ('NAUO48', [686.52, 929.76, 1258.37])}
    VIEW, BOX = 'Step 45c', ([556.0, 886.0, 1238.0], [706.0, 968.0, 1300.0])
    views = ['Step 21c', 'Step 32c', 'Step 34c', 'Step 39c', 'Step 40c', 'Step 44c', 'Step 45c', 'Step 46c']
    order = ('tan', 'red', 'black'); skip0 = ('NAUO46',)
    ends = {c: (cap, np.asarray(e) + FLAT, np.array([0.0, -1.0, 0.0])) for c, (cap, e) in EX.items()}
    excl = ('switch', 'pot')
else:
    F1_DOWN = json.loads(sys.argv[2])
    EX = {'red': ('NAUO34', [718.72, 906.79, 1229.65]), 'tan': ('NAUO33', [718.72, 906.68, 1235.0]), 'black': ('NAUO14', [718.72, 906.57, 1240.35])}
    VIEW, BOX = 'Step 45c', ([676.0, 886.0, 1296.0], [800.0, 950.0, 1372.0])
    views = ['Step 32c', 'Step 34c', 'Step 39c', 'Step 40c', 'Step 44c', 'Step 45c']
    order = ('black', 'tan', 'red'); skip0 = ('NAUO11',)
    ends = {}
    for c, (cap, e) in EX.items():
        p = apply_pose(F1_DOWN, np.array([e, np.add(e, [0, -1, 0])]))
        ends[c] = (cap, p[0], unit(p[1] - p[0]))
    excl = ('pot',)
extra_all = union_wires(views, excl)
NEED, EVERY = float(sys.argv[-2]), float(sys.argv[-1])
done, ctl = {}, {}
t0 = time.time()
for c in order:
    cap, e, d = ends[c]
    a, b = e + d * 6.0, wire_at(cap) + [0.0, 14.0, 0.0]
    drops = [(np.array([wire_at(ends[o][0]) + [0, 14.0, 0], wire_at(ends[o][0]) + [0, 2.0, 0]]), 0.625) for o in ends if o != c and o not in done]
    drops += [(np.array([ends[o][1], ends[o][1] + ends[o][2] * 9.0]), 0.625) for o in ends if o != c and o not in done]   # (the others' first mm out of their pins)
    F = Field(VIEW, BOX, skip=(cap,) + skip0, exclude=tuple(w for w in RAD if w.startswith(excl)), extra=extra_all + drops + [(done[o], 0.625) for o in done])
    path = astar(F, a, b, need=NEED, free_near=(a, b))
    if path is None:
        print(c, 'NO PATH'); continue
    ctl[c] = controls_from(path, every=EVERY, trim=3.0)
    done[c] = into_hole(cap, e, d, ctl[c])
    worst = min(check_v for check_v in [0])
    print(c, 'controls', len(ctl[c]), round(time.time() - t0, 1), 's', flush=True)
for c in done:
    for v in views:
        r = check(v, done[c], 0.625, ends=(cap,) + skip0, wire=tuple(w for w in RAD if w.startswith(excl)))
        if r: print('  CHECK', c, v, r[:2])
print('mutual', mutual(done))
print('WAY =', json.dumps({c: [[round(x, 1) for x in p] for p in w] for c, w in ctl.items()}))
