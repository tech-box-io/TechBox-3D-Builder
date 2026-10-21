"""The potentiometer's leads with F1 face down aside (Step 46 on): from its pins through the gap between F7B and F8, behind F8 and the
LCD, along the rails to their holes."""
import sys, time, json
from planner import *
ASIDE = json.loads(sys.argv[1]); LCDP = json.loads(sys.argv[2]); NEED, EVERY = float(sys.argv[3]), float(sys.argv[4])
EX = {'red': ('NAUO34', [718.72, 906.79, 1229.65]), 'tan': ('NAUO33', [718.72, 906.68, 1235.0]), 'black': ('NAUO14', [718.72, 906.57, 1240.35])}
VIEW = 'Step 50c'
poses = {i: ASIDE for i in ('NAUO10', 'NAUO11', 'NAUO12', 'NAUO13', 'NAUO146')}
poses.update({i: LCDP for i in ('NAUO94', 'NAUO97', 'NAUO98', 'NAUO99', 'NAUO100')})
# the volume F8 sweeps sliding in from 94 mm out (x 704 - 814, z 1264.5 - 1267.5, y 881 - 958), as points
g8 = np.array([[x, y, z] for x in np.arange(704.0, 815.0, 2.0) for y in np.arange(881.0, 959.0, 2.0) for z in (1264.5, 1266.0, 1267.5)])
others = [(g8, 0.8)]
for w, ri in VIEWS[VIEW]['wires'].items():
    if not w.startswith('pot'): others.append((np.asarray(S['routes'][ri]['pts']), RAD[w]))
ends = {}
for c, (cap, e) in EX.items():
    q = apply_pose(ASIDE, np.array([e, np.add(e, [0, -1, 0])])); ends[c] = (cap, q[0], unit(q[1] - q[0]))
BOX = ([678.0, 886.0, 1236.0], [862.0, 950.0, 1342.0])
done, ctl = {}, {}
for c in ('black', 'tan', 'red'):
    cap, e, d = ends[c]
    a, b = e + d * 6.0, wire_at(cap) + [0.0, 14.0, 0.0]
    drops = [(np.array([wire_at(ends[o][0]) + [0, 14.0, 0], wire_at(ends[o][0]) + [0, 2.0, 0]]), 0.625) for o in ends if o != c and o not in done]
    drops += [(np.array([ends[o][1], ends[o][1] + ends[o][2] * 9.0]), 0.625) for o in ends if o != c and o not in done]
    F = Field(VIEW, BOX, skip=(cap, 'NAUO11'), exclude=tuple(w for w in RAD if w.startswith('pot')), extra=others + drops + [(done[o], 0.625) for o in done],
              pitch=1.0, poses=poses)
    path = astar(F, a, b, need=NEED, free_near=(a, b))
    if path is None:
        print(c, 'NO PATH', flush=True); continue
    ctl[c] = controls_from(path, every=EVERY, trim=3.0)
    done[c] = into_hole(cap, e, d, ctl[c])
    print(c, 'controls', len(ctl[c]), flush=True)
print('mutual', mutual(done))
print('ASIDEWAY =', json.dumps({c: [[round(x, 1) for x in p] for p in w] for c, w in ctl.items()}))
