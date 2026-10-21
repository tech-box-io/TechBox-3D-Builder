"""The buzzer's leads with the buzzer held 45 mm over its seat (Step 43's second stop): from the buzzer down to a point J on the CAD's
clamped lead, J_MM from the buzzer; from J to the hole the lead is the clamped lead itself, so that this run stays put while the
buzzer is lowered onto its seat (guide.py: b_from / tail_from). The review of Lee's first round (20 Oct 2026): with a shape of its own
all the way, the lead passed through the jumper and LCD wires as the buzzer came down.
Usage: python plan_buzz_up.py <clearance> <control point spacing> <grid mm>"""
import sys, json
from planner import *
LEADS = {'red': ('NAUO58', [674.5, 894.24, 1233.12], 'NAUO65'), 'black': ('NAUO59', [676.02, 894.24, 1233.12], 'NAUO64')}
UP = [0.0, 45.0, 0.0]
J_MM = 36.0
VIEW = 'Step 43c'
NEED, EVERY, PITCH = (float(x) for x in sys.argv[1:4])


def clamped(key, cap):
    """The CAD's clamped lead from the buzzer to the cap, every 1 mm."""
    line = cad_line(key)
    if np.linalg.norm(line[0] - wire_at(cap)) < np.linalg.norm(line[-1] - wire_at(cap)):
        line = line[::-1]
    return W.resample(line, 1.0)


def junction(line):
    s = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))]
    return int(np.searchsorted(s, J_MM))


others = [(np.asarray(S['routes'][ri]['pts']), RAD[w]) for w, ri in VIEWS[VIEW]['wires'].items() if not w.startswith('buzzer')]
done, ctl = {}, {}
for c in ('red', 'black'):
    cap, ex, key = LEADS[c]
    L = clamped(key, cap)
    j = junction(L)
    e = np.add(ex, UP)
    d = np.array([0.0, -1.0, 0.0])
    a, b = e + d * 3.0, L[j]
    o = [x for x in LEADS if x != c][0]
    ocap, oex, okey = LEADS[o]
    OL = clamped(okey, ocap)
    extra = others + [(L[j + 4:], 0.625)]
    extra += [(done[o], 0.625)] if o in done else [(OL[junction(OL):], 0.625), (np.array([np.add(oex, UP), np.add(oex, UP) + d * 9.0]), 0.625)]
    lo = np.minimum(a, b) - [25, 12, 25]
    hi = np.maximum(a, b) + [25, 20, 25]
    lo[1] = max(lo[1], 886.0)
    F = Field(VIEW, (lo, hi), skip=(cap, 'NAUO62'), exclude=tuple(w for w in RAD if w.startswith('buzzer')), extra=extra, pitch=PITCH,
              poses={'NAUO62': UP})
    path = astar(F, a, b, need=NEED, free_near=(a, b))
    if path is None:
        print(c, 'NO PATH', flush=True)
        continue
    ctl[c] = controls_from(path, every=EVERY, trim=3.0)
    body = W.smooth([a, *ctl[c], L[j]], start_dir=d, end_dir=unit(L[j + 2] - L[j]), spacing=0.5)
    done[c] = W.resample(W.join(W.straight(e, d, 3.0), body, L[j:]), 1.0)
    print(c, 'controls', len(ctl[c]), flush=True)
print('mutual', mutual(done) if len(done) > 1 else None)
print('UPWAY =', json.dumps({c: [[round(x, 1) for x in p] for p in w] for c, w in ctl.items()}))
