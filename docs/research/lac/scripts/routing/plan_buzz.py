"""The buzzer's leads: lying beside the base (Steps 33 - 42) and at its stops on the way to its seat (Step 43)."""
import sys, time, json
from planner import *
LEADS = {'red': ('NAUO58', [674.5, 894.24, 1233.12]), 'black': ('NAUO59', [676.02, 894.24, 1233.12])}
STOPS = json.loads(sys.argv[1]); VIEW = sys.argv[2]; NEED, EVERY, PITCH = float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
views = sys.argv[6].split(',')
def union_wires(views):
    out, seen = [], set()
    for vn in views:
        for w, ri in (VIEWS[vn].get('wires') or {}).items():
            if w.startswith('buzzer') or ri in seen: continue
            seen.add(ri); out.append((np.asarray(S['routes'][ri]['pts']), RAD[w]))
    return out
others = union_wires(views)
out_all = {}
for stop, pose in STOPS.items():
    done, ctl = {}, {}
    for c in ('red', 'black'):
        cap, ex = LEADS[c]
        q = apply_pose(pose, np.array([ex, np.add(ex, [0, -1.0, 0])])); e, d = q[0], unit(q[1] - q[0])
        ABOVE = {'red': 1.0, 'black': 10.0}[c]                   # (red into j4 low: the yellow jumper arches 8 mm over j4)
        a, b = e + d * 6.0, wire_at(cap) + [0.0, 4.0 + ABOVE, 0.0]
        lo = np.minimum(a, b) - [30, 12, 30]; hi = np.maximum(a, b) + [30, 30, 30]; lo[1] = max(lo[1], 886.0)
        other = [o for o in LEADS if o != c][0]
        oc, oe = LEADS[other]
        qo = apply_pose(pose, np.array([oe, np.add(oe, [0, -1.0, 0])]))
        extra = others + ([(np.array([qo[0], qo[0] + unit(qo[1] - qo[0]) * 9.0]), 0.625), (np.array([wire_at(oc) + [0, 14.0 if other == 'black' else 5.0, 0], wire_at(oc) + [0, 2.0, 0]]), 0.625)] if other not in done else [(done[other], 0.625)])
        F = Field(VIEW, (lo, hi), skip=(cap, 'NAUO62'), exclude=tuple(w for w in RAD if w.startswith('buzzer')), extra=extra, pitch=PITCH, poses={'NAUO62': pose})
        path = astar(F, a, b, need=NEED, free_near=(a, b))
        if path is None:
            print(stop, c, 'NO PATH', flush=True); continue
        ctl[c] = controls_from(path, every=EVERY, trim=3.0)
        done[c] = into_hole(cap, e, d, ctl[c], above=ABOVE)
        print(stop, c, 'controls', len(ctl[c]), flush=True)
    print(stop, 'mutual', mutual(done) if len(done) > 1 else None)
    out_all[stop] = {c: [[round(x, 1) for x in p] for p in w] for c, w in ctl.items()}
print('BUZZWAYS =', json.dumps(out_all))
