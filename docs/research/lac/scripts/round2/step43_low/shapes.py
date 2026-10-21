"""Candidate shapes for Step 43 (design 'low, round the holes')."""
from common import *


def drawn_len(pts):
    return float(np.linalg.norm(np.diff(np.asarray(pts, float), axis=0), axis=1).sum())


def at_len(pts, s):
    p = np.asarray(pts, float)
    c = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    return np.stack([np.interp(s, c, p[:, k]) for k in range(3)])


def cut(pts, s):
    """The line from its first point up to s mm along it (ending exactly there)."""
    p = np.asarray(pts, float)
    c = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    keep = p[c < s - 1e-6]
    return np.vstack([keep, at_len(p, s)])


# ---- red seated, B': over the jumpers' row-i ends as now, then on over the orange and yellow jumpers into the back strip, and into j4
# from the back (as the lying lead goes in)
SEAT_KEEP = 14                                                      # BUZZER_SEAT_WAY red[:14]: up to [664.8, 925.4, 1287.8]


def seated_red(tail, keep=SEAT_KEEP, crest=None):
    colour, (cap, exit_) = 'red', LEAD['red']
    e, d = np.asarray(exit_, float), np.array([0.0, -1.0, 0.0])
    above = BUZZER_ABOVE[colour]
    top = wire_at(cap) + [0.0, 4.0 + above, 0.0]
    way = [np.asarray(p, float) for p in BUZZER_SEAT_WAY['red'][:keep]] + [np.asarray(p, float) for p in tail]
    h = top - way[-1]
    h[1] = 0.0
    way.append(top - unit(h) * 4.5 + [0.0, BUZZER_CREST[colour] if crest is None else crest, 0.0])
    line = into_hole(cap, e, d, way, lift=BUZZER_SEAT_OUT, above=above)
    return line, int(np.argmax(line[:, 2] >= BUZZER_J_Z))


def over_seat_from(colour, L, j):
    """buzzer_over_seat on a given seated line L (from the stub) with junction j: drawn from the hole."""
    cap, exit_ = LEAD[colour]
    e, d = np.add(exit_, BUZZER_UP), np.array([0.0, -1.0, 0.0])
    body = W.smooth([e + d * BUZZER_OUT, *[np.asarray(c, float) for c in BUZZER_UP_WAY[colour]], L[j]], start_dir=d,
                    end_dir=unit(L[j + 2] - L[j]), spacing=0.5)
    return W.resample(W.join(W.straight(e, d, BUZZER_OUT), body, L[j:]), 1.0)[::-1]


def free_run(head, ctrl, exit_pt, exit_dir, out=BUZZER_OUT):
    """A line drawn from the hole: `head` (from the hole, kept as it is), then smoothly through ctrl to the exit, leaving the exit
    straight along exit_dir for `out` mm (exit_dir: the stub's direction, out of the buzzer)."""
    head = np.asarray(head, float)
    hd = unit(head[-1] - head[-3])
    first = np.asarray(exit_pt, float) + unit(exit_dir) * out
    body = W.smooth([head[-1], *[np.asarray(c, float) for c in ctrl], first], start_dir=hd, end_dir=-unit(exit_dir), spacing=0.5)
    return W.resample(W.join(head, body, W.straight(first, -unit(exit_dir), out)), 1.0)


def exit_at(colour, pose):
    cap, exit_ = LEAD[colour]
    q = posed_line(pose, [exit_, np.add(exit_, [0.0, -1.0, 0.0])])
    return q[0], unit(q[1] - q[0])


def route(line, colour, pose, k=None, stretch=False, b_from=None):
    cap = LEAD[colour][0]
    kw = {}
    if stretch:
        kw['stretch'] = True
    elif k is not None:
        kw['tail_from'] = k
    return W.route(line, a=cap, b=BUZZER, **({'b_at': pose} if pose not in (None, ZERO) else {}),
                   b_from=b_from if b_from is not None else k, **kw)
