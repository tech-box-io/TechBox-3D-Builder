"""Writes guide_patch.txt: the paste-ready replacement for guide.py's buzzer section (from '# Each lead's way to its hole' to the end of
buzzer_clamped) and for the Step 43 call. BUZZER_WAY and black's BUZZER_LIFT_WAY are copied verbatim from guide.py."""
import json, re
from pathlib import Path
G = Path('/Users/lee-johnson/Desktop/Claude_Cadasio/LAC Build Instructions/guide.py').read_text().splitlines()
way_lines = [l for l in G if l.startswith('BUZZER_WAY = ') or l.startswith("              'black': [[648.9, 897.0, 1393.1]")]
assert len(way_lines) == 2, way_lines
lift_black = [l for l in G if l.startswith("                   'black': [[648.2, 954.7, 1393.7]")]
assert len(lift_black) == 1
P = json.load(open('cand13.json'))
fmt = lambda pts: '[' + ', '.join('[' + ', '.join(f'{x:.1f}' for x in p) + ']' for p in pts) + ']'
seat_black = [l for l in G if l.startswith("                   'black': [[676.2, 891.3, 1235.6]")]
assert len(seat_black) == 1
text = f'''# Each lead's way to its hole, the buzzer lying (Steps 33 - 42) and lifted 60 mm over where it lies (Step 43): short and smooth, clear
# of the parts and the other wires (a path search; Lee, 20 Oct 2026: the CAD's lying leads loop out sideways, and blending the straight
# leads into them threw them off the screen; the red one had a kink by the breadboard). Lifted, red's run behind the board's end stays
# low (under the yellow jumper's arch at j4) up to BUZZER_LIFT_HOLD and only then rises to the buzzer, so that as the buzzer is carried
# the run swings round behind the j-side caps without touching the yellow jumper (docs/research/lac/round2/step43_high.md).
{way_lines[0]}
{way_lines[1]}
BUZZER_LIFT_WAY = {{'red': {fmt(P['LIFT_RED'])},
{lift_black[0]}
BUZZER_LIFT_HOLD = {{'red': {P['LIFT_BFROM']['red']:.1f}}}                                  # (red, lifted: the run up to here, from the hole, does not follow the buzzer)
BUZZER_LIFT = tidy(compose([0.0, 60.0, 0.0], BUZZER_LYING, BUZZER_LYING['at']))   # (about the buzzer's own middle, as BUZZER_LYING is)
BUZZER_HIGH = [0.0, 75.0, 0.0]                                       # (Step 43: carried over the board to 75 mm over its seat, clear of the
                                                                    # spread F7s' tops, then lowered straight in)


BUZZER_ABOVE = {{'red': 0.5, 'black': 5.0}}                           # (how far each goes straight down into its hole, over the cap's top: red
                                                                    # into j4 under the yellow jumper, whose centre line is 913 over j4)
BUZZER_CREST = {{'red': 0.3, 'black': 1.5}}                           # (how far over the drop's top each comes in: red low, so that held 5 mm
                                                                    # over j4 (Step 33) it stays under the yellow jumper: review, 21 Oct 2026)
BUZZER_OUT = 3.0                                                    # (straight out of the buzzer before a lead turns)
BUZZER_RISE = {{'red': 2.2, 'black': 0.0}}                            # (red then rises over the black lead beside it, which it turns across)


def buzzer_line(colour, cap, exit_, pose, way):
    """A buzzer lead from its exit (the buzzer at `pose`): 3 mm straight out, through `way`, over a crest BUZZER_CREST mm above the top of its
    straight drop and 4.5 mm short of it, and down into its hole. The controls within 8 mm of the run out and 7 mm (across) of the drop
    are left out, so that the lead turns over several mm (the review of Lee's first round: the path search's controls there made
    hairpins, and the drop's top a crease)."""
    q = posed_line(pose, [exit_, np.add(exit_, [0.0, -1.0, 0.0])])
    e, d = q[0], unit(q[1] - q[0])
    above = BUZZER_ABOVE[colour]
    first, top = e + d * BUZZER_OUT, wire_at(cap) + [0.0, 4.0 + above, 0.0]
    across = lambda p: float(np.hypot(p[0] - top[0], p[2] - top[2]))
    keep = [np.asarray(p, float) for p in way if np.linalg.norm(np.asarray(p, float) - first) > 8.0 and across(p) > 7.0]
    rise = [first + d * 2.0 + [0.0, BUZZER_RISE[colour], 0.0]] if BUZZER_RISE[colour] else []
    h = top - (keep[-1] if keep else first)
    h[1] = 0.0
    return into_hole(cap, e, d, rise + keep + [top - unit(h) * 4.5 + [0.0, BUZZER_CREST[colour], 0.0]], lift=BUZZER_OUT, above=above)


def shared_to(line, point):
    """How far along `line` (from its first point) its point nearest `point` is."""
    s = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))]
    return round(float(s[int(np.argmin(np.linalg.norm(line - np.asarray(point, float), axis=1)))]), 1)


def buzzer_plugged(colour, cap, exit_, pose, way, stretch=False, hold=None):
    """A buzzer lead plugged in (buzzer_line), drawn from the hole: its straight drop held in the hole (b_from) and shared between
    shapes (tail_from); the rest carried whole with the buzzer (no stretch: it turns with it). With `stretch` (the buzzer lifted, Step
    43): matched to the next shape by share of length instead, so that its run over the seat grows along the lead rather than fanning out
    from the top of the drop (where it dipped into the resistors). `hold`: mm from the hole that do not follow the buzzer (b_from), if
    more than the drop."""
    line = buzzer_line(colour, cap, exit_, pose, way)[::-1]
    k = BUZZER_ABOVE[colour] + 4.0
    return W.route(line, a=cap, b=BUZZER, b_at=pose, b_from=hold or k, **({{'stretch': True}} if stretch else {{'tail_from': k}}))


# The seated leads (Lee, 21 Oct 2026: "pass the red and black wires over the black/green/purple/blue wires"; his second note on Step 43,
# the same day: and not through them as the buzzer is carried in). From the stub's end, straight on down 1 mm and round under it. Red comes
# into j4 from behind, as it lies before the step (under the yellow jumper's arch only at the hole): it climbs behind the j-side caps,
# crosses over the yellow and orange jumpers just past the clock module, over the row-i ends of the jumpers and over the black and green
# jumpers' arches, then over the switch's tan lead by the (+) red rail and down in front of the switch to the buzzer. Black runs along the
# front rails over the potentiometer's leads, the LCD's purple wire and the green jumper, over the switch's tan lead, to the buzzer. Both
# pass in front of the switch (on its +x side where it is seated), so that neither is under one of the switch's leads before F4 is lifted
# (Step 47): the buzzer is carried over the board, so its leads can only lie over what they cross, and the switch is then carried over
# them (docs/research/lac/round2/step43_high.md: which crossings each motion allows). Drawn from the stub's end: no gap where the lead
# meets it.
BUZZER_SEAT_WAY = {{'red': {fmt(P['SEAT_RED'])},
{seat_black[0]}
BUZZER_SEAT_OUT = 1.0                                               # (straight on out of the stub before the lead turns under it)
BUZZER_KEEP = {{'red': {P['BRANCH_RED']}, 'black': None}}         # (Step 43: the run from the hole to here is the same carried high and
                                                                    # seated, and stays put as the buzzer is lowered; black: its drop)
BUZZER_RISER = {{'red': [{P['RISER_RED'][0]:.1f}, 945.0, {P['RISER_RED'][1]:.1f}], 'black': [699.2, 945.0, 1340.9]}}   # (carried high: the top of each lead's
                                                                    # rise, red's from BUZZER_KEEP behind the j-side caps, black's straight up out of (-) blue)
BUZZER_RED_RISE = {fmt(P['RED_RISE'])}
BUZZER_HIGH_WAY = {{'red': {fmt(P['TAIL_A_RED'])},
                   'black': {fmt(P['TAIL_A_BLACK'])}}}


def seated_from_buzzer(colour, cap, exit_):
    """A buzzer lead seated, from the stub's end to the hole, every 1 mm (red in over a crest under the yellow jumper, as buzzer_line)."""
    e, d = np.asarray(exit_, float), np.array([0.0, -1.0, 0.0])
    above = BUZZER_ABOVE[colour]
    top = wire_at(cap) + [0.0, 4.0 + above, 0.0]
    way = [np.asarray(p, float) for p in BUZZER_SEAT_WAY[colour]]
    if colour == 'red':
        h = top - way[-1]
        h[1] = 0.0
        way.append(top - unit(h) * 4.5 + [0.0, BUZZER_CREST[colour], 0.0])
    return into_hole(cap, e, d, way, lift=BUZZER_SEAT_OUT, above=above)


def buzzer_kept(colour, cap, exit_):
    """The seated lead from the hole to BUZZER_KEEP (black: its drop), and its length."""
    line = seated_from_buzzer(colour, cap, exit_)[::-1]
    if BUZZER_KEEP[colour] is None:
        k = BUZZER_ABOVE[colour] + 4.0
    else:
        k = shared_to(line, BUZZER_KEEP[colour])
    s = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))]
    return line[:int(np.argmin(np.abs(s - k))) + 1], k


def buzzer_high(colour, cap, exit_):
    """A buzzer lead with the buzzer carried high over its seat (BUZZER_HIGH, Step 43): the seated lead from the hole to BUZZER_KEEP, up
    to the top of its rise (BUZZER_RISER) and high over the board to the buzzer (BUZZER_HIGH_WAY). Drawn from the hole; the run to the top
    of the rise does not follow the buzzer (b_from), and the run kept is matched by distance from the hole to the seated lead's as the
    buzzer is lowered (tail_from), the rest by distance from the buzzer: it settles straight down onto the seated lead."""
    kept, k = buzzer_kept(colour, cap, exit_)
    top = np.asarray(BUZZER_RISER[colour], float)
    if colour == 'red':
        line = seated_from_buzzer(colour, cap, exit_)
        j = len(line) - len(kept)                                   # (where the kept run ends, on the seated lead drawn from the stub)
        rise = W.resample(W.smooth([kept[-1], *[np.asarray(c, float) for c in BUZZER_RED_RISE], top], start_dir=unit(line[j - 1] - line[j]),
                                   end_dir=[0, 1, 0], spacing=0.5), 1.0)
    else:
        w = wire_at(cap)
        n = int(round(top[1] - w[1]))
        rise = np.array([[w[0], w[1] + i * (top[1] - w[1]) / n, w[2]] for i in range(n + 1)])
        kept = rise[:1]
    head = np.vstack([kept, rise[1:]])
    e, d = np.add(exit_, BUZZER_HIGH), np.array([0.0, -1.0, 0.0])
    body = W.smooth([e + d * BUZZER_OUT, *[np.asarray(c, float) for c in BUZZER_HIGH_WAY[colour]], top], start_dir=d, end_dir=[0, -1, 0],
                    spacing=0.5)
    tail = W.resample(W.join(W.straight(e, d, BUZZER_OUT), body), 1.0)[::-1]
    held = round(float(np.linalg.norm(np.diff(head, axis=0), axis=1).sum()), 1)
    return W.route(np.vstack([head, tail[1:]]), a=cap, b=BUZZER, b_at=BUZZER_HIGH, b_from=held, tail_from=k)


def buzzer_clamped(colour, cap, exit_):
    """A buzzer lead seated (seated_from_buzzer), drawn from the hole; the run from the hole to BUZZER_KEEP held still and kept (as the
    buzzer is lowered onto its seat, the rest follows it down)."""
    line = seated_from_buzzer(colour, cap, exit_)[::-1]
    _, k = buzzer_kept(colour, cap, exit_)
    return W.route(line, a=cap, b=BUZZER, b_from=k, tail_from=k)
'''
step43 = '''# (lifted, carried high over the board to 75 mm over its seat and lowered in: a stop each, its leads keeping pace stop by stop: carried,
# each lead rises behind what it will lie over and arches high to the buzzer; lowered, it settles straight down onto its seated way)
g.place('Lower the buzzer in between the two F7s, its ears into their slots.', move=[BUZZER], path=[BUZZER_LYING, BUZZER_LIFT, BUZZER_HIGH, ZERO],
        lines=False, eye=[dict(id=BUZZER, **near('near-above'))],         # (above the buzzer: Lee, 21 Oct 2026)
        wires_done={f'buzzer {c}': [buzzer_plugged(c, cap, e, BUZZER_LIFT, BUZZER_LIFT_WAY[c], stretch=True, hold=BUZZER_LIFT_HOLD.get(c)),
                                    buzzer_high(c, cap, e), buzzer_clamped(c, cap, e)] for c, cap, _, e, _, _ in BUZZER_LEADS}, **CASE_CAMERA)
'''
Path('guide_patch.txt').write_text(text)
Path('guide_patch_step43.txt').write_text(step43)
print(len(text.splitlines()), 'lines')
