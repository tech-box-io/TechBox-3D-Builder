"""Carry high, v4. Red's seated lead comes into j4 from behind (-x), as it lies before the step, rising behind the j-side caps and
crossing over the yellow and orange jumpers past the clock module's end, then on as before (over the jumpers' row-i ends, under the
switch's lying tan lead, down behind the buzzer). Stops: LYING -> LIFT -> A (high over the seat) -> UP (45 up, the seated leads
pre-skinned) -> ZERO."""
import sys, json
from common import *
import common
OUT = Path(__file__).resolve().parent
P = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
A = P.get('A', [0.0, 75.0, 0.0])
TOP = P.get('TOP', {'red': 945.0, 'black': 945.0})
SEAT_RED_TAIL = P.get('SEAT_RED_TAIL')                       # (the seated way's controls from where it leaves the old one, to the hole)
SEAT_RED_KEEP_Z = P.get('SEAT_RED_KEEP_Z', 1288.0)           # (the old controls kept up to here, from the stub)
BRANCH = {'red': P.get('BRANCH_RED'), 'black': None}         # (red: the point of the seated lead its carry riser leaves from)
RISER = {'red': P.get('RISER_RED'), 'black': P.get('RISER_BLACK', [699.2, 1340.9])}
RED_RISE = P.get('RED_RISE', [])
LIFT_WAY = {'red': P.get('LIFT_RED', BUZZER_LIFT_WAY['red']), 'black': P.get('LIFT_BLACK', BUZZER_LIFT_WAY['black'])}
LIFT_BFROM = P.get('LIFT_BFROM', {})
TAIL_A = {'red': P.get('TAIL_A_RED'), 'black': P.get('TAIL_A_BLACK')}
ZERO_BFROM = P.get('ZERO_BFROM', {'red': 'branch', 'black': 9.0})

if P.get('SEAT_RED'):
    common.BUZZER_SEAT_WAY['red'] = P['SEAT_RED']
elif SEAT_RED_TAIL:
    old = BUZZER_SEAT_WAY['red']
    common.BUZZER_SEAT_WAY['red'] = [p for p in old if p[2] <= SEAT_RED_KEEP_Z] + SEAT_RED_TAIL


def ramp(s):
    t = np.clip((s - 0.1) / 0.8, 0, 1)
    return t * t * (3 - 2 * t)


def seated_line(colour):
    cap, e = LEAD[colour]
    return seated_from_buzzer(colour, cap, e)[0]          # stub -> hole, every 1 mm


def branch_index(colour):
    L = seated_line(colour)
    if colour == 'red':
        return int(np.argmin(np.linalg.norm(L - np.asarray(BRANCH['red'], float), axis=1)))
    return None


def head_len(colour):
    if colour == 'red':
        L = seated_line('red')
        jb = branch_index('red')
        head = L[jb:][::-1]
        return round(float(np.linalg.norm(np.diff(head, axis=0), axis=1).sum()), 2)
    return BUZZER_ABOVE['black'] + 4.0


def carry_head(colour):
    cap, _ = LEAD[colour]
    rx, rz = RISER[colour]
    top = np.array([rx, TOP[colour], rz])
    if colour == 'red':
        L = seated_line('red')
        jb = branch_index('red')
        head = L[jb:][::-1]
        t = unit(L[jb - 1] - L[jb])
        rise = W.resample(W.smooth([head[-1], *[np.asarray(c, float) for c in RED_RISE], top], start_dir=t, end_dir=[0, 1, 0], spacing=0.5), 1.0)
        return np.vstack([head, rise[1:]])
    w = wire_at(cap)
    n = int(round(TOP[colour] - w[1]))
    return np.array([[w[0], w[1] + k * (TOP[colour] - w[1]) / n, w[2]] for k in range(n + 1)])


def tail_line(colour, pose_t, ctl):
    cap, ex = LEAD[colour]
    e, d = np.add(ex, pose_t), np.array([0.0, -1.0, 0.0])
    rx, rz = RISER[colour]
    top = np.array([rx, TOP[colour], rz])
    body = W.smooth([e + d * BUZZER_OUT, *[np.asarray(c, float) for c in ctl], top], start_dir=d, end_dir=[0, -1, 0], spacing=0.5)
    return W.resample(W.join(W.straight(e, d, BUZZER_OUT), body), 1.0)


def zero_bfrom(colour):
    v = ZERO_BFROM[colour]
    return head_len(colour) if v == 'branch' else float(v)


def carry_route(colour, pose_t, ctl):
    head = carry_head(colour)
    tl = tail_line(colour, pose_t, ctl)[::-1]
    line = np.vstack([head, tl[1:]])
    k = round(float(np.linalg.norm(np.diff(head, axis=0), axis=1).sum()), 2)
    return W.route(line, a=LEAD[colour][0], b=BUZZER, b_at=pose_t, b_from=k, tail_from=zero_bfrom(colour)), line


def zero_route(colour):
    cap, e = LEAD[colour]
    r = buzzer_clamped(colour, cap, e)
    k = zero_bfrom(colour)
    return dict(r, b_from=float(k), tail_from=float(k))


def preskinned(r0, pose_t):
    p = np.asarray(r0['pts'], float)
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    u = (s - r0['b_from']) / max(1e-6, s[-1] - r0['b_from'])
    q = p + ramp(u)[:, None] * np.asarray(pose_t, float)[None, :]
    return W.route(q, a=r0['a'], b=r0['b'], b_at=list(map(float, pose_t)), b_from=r0['b_from'], tail_from=r0['tail_from'])


def build(name):
    routes = {}
    for c, cap, _, e, _, _ in BUZZER_LEADS:
        lift = buzzer_plugged(c, cap, e, BUZZER_LIFT, LIFT_WAY[c], stretch=True)
        if LIFT_BFROM.get(c):
            lift = dict(lift, b_from=float(LIFT_BFROM[c]))
        ra, la = carry_route(c, A, TAIL_A[c])
        cl = zero_route(c)
        ru = preskinned(cl, BUZZER_UP)
        routes[f'buzzer {c}'] = [lift, ra, cl] if P.get('THREE_BEATS') else [lift, ra, ru, cl]
        for nm, r in (('lift', lift), ('A', ra), ('UP', ru), ('zero', cl)):
            p = np.asarray(r['pts']); s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
            print(f'  {c:5s} {nm:4s}: {s[-1]:6.1f} mm, tail_from {r.get("tail_from")}, b_from {r.get("b_from")}, stretch {r.get("stretch", False)}')
    path = [BUZZER_LYING, BUZZER_LIFT, A, ZERO] if P.get('THREE_BEATS') else [BUZZER_LYING, BUZZER_LIFT, A, BUZZER_UP, ZERO]
    out = OUT / f'steps-{name}.json'
    write_steps(out, path, routes)
    json.dump(dict(routes=routes, path=path, params=P), open(OUT / f'routes-{name}.json', 'w'))
    print('wrote', out)


if __name__ == '__main__':
    build(P.get('name', 'cand'))
