"""Laser Stem Matrix (LSM), deconstruction: the finished kit taken apart, down to D1 with the breadboard stuck on it, in the order and
the manner of TechBox's own published take-apart (Lee, 21 Oct 2026: "you need to base the deconstruction process off of this guide:
https://instructions.online/?id=19075-laser_stem_matrix_lsm_-_deconstruction"). A guide of its own (steps-deconstruction.json), made
from the Full Build as guide.py last wrote it (run that first, and this again after any change to it). It opens on the Full Build's
title page, ends on what is left (D1 and the breadboard, as the published take-apart ends), followed straight by the Full Build's parts
list (no Completed View: Lee, 22 Oct 2026), and its card on the website is the Full Build's.

The published take-apart, step by step (docs/research/guide_19075-laser_stem_matrix_lsm_-_deconstruction.md; its data replayed in our
part ids and mm: docs/research/lsm/decon/published/), outside in: the stems; D8; D7; D5 and D4 off the ends (which frees D10's ends);
the D11 posts two and two; D6; the LED matrix lifted out with D10 under it and set down beside the box, still wired; both D9; the three
breadboard wires out of the breadboard; the matrix on its own: D10 off, the wires' connectors off its pins; D3; D2 with the push button,
its two wires unplugged; the button on its own: the nut, the button out of D2; the USB cable; the 330 ohm resistor, the capacitor, the
12 kOhm resistor and the Nano Board. Each step has the published camera, arrows of the published size where the published tail is,
the published eyes (the D11 posts' at the posts' feet, on their latches: Lee, 22 Oct 2026), and a close-up where the published guide has one (each catch to release: D8's latches, D7's notches, the tabs at
D5's and D4's corners, the D11 posts' tabs under D1, D3's and D2's latches on D1), drawn from our model with a red box on the catch.
Where it differs, and why: the three wires come out in one step (Lee: "some things can be removed in groups (like the 3 breadboard
wires)"); the matrix stays held over the box while D10 is slid off it and it is pulled off the three wires' connectors, the wires left
in the breadboard (Lee, 22 Oct 2026: "D10 must slide off of the LED Matrix"; the published guide set it down beside the box, still
wired, and took the wires out of the breadboard first); the wires, still in the breadboard, are then laid out of the way, out of the box
over its open end onto the table (Lee, the same day), and the D9s come out before the wires, which run under one of them; D2 comes
off before its wires are unplugged (one step each); D4, once off its tabs, is lifted off the USB cable (its notch held it); once the
button is out of D2, the nut is screwed back onto it, so that the two stay together (Lee, 22 Oct 2026: a step of its own). A few
cameras and arrows are moved where ours would hide or lose what the published one showed (Step 16 from outside D2, whose latch and
arrow the published camera saw through D2; Step 11 from under the held matrix, Lee's view; Step 21
to hold the cable's A end; Step 12, new, from the open end's corner by D2, so that the laid wires run across the picture; Step 14 framed
wider toward the open end, where the wires lie; the nut's arrow at the nut, not 40 mm away along the wires); arrows whose published tail
is inside a part, or that a part, the instruction boxes or a plug behind would hide or confuse, are moved (Steps 4 - 7, 9, 11, 13 and
25). Two steps on one sub-assembly
change camera where the published guide does (Steps 18 - 19). No counterpart for the Full
Build's preparation or its cards. The USB cable cannot come out first (the box closes round its plug), so Step 1's caution says to
disconnect it from the computer first. Its title page is the Full Build's, which leaves the USB cable off (it comes into view at Step
1). An independent review (docs/research/lsm/decon/review2/) went over it against the published guide."""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
sys.path.insert(0, str(HERE))
import wire_shapes as WS  # noqa: E402
from stepgen import ZERO, Guide, _shifted, apply_pose, compose, via  # noqa: E402

# ---------------------------------------------------------------- parts (as guide.py names them: assemble.py's ids)
D1, D2, D3, D4, D5, D6, D7, D8, D10 = 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D10'
D9_A, D9_B = 'D9_A', 'D9_B'
D11_A, D11_B, D11_C, D11_D = 'D11_A', 'D11_B', 'D11_C', 'D11_D'      # A, B at D5's end (D2's side, D3's side), C, D at D4's
BREADBOARD, BACKING, NANO, R12K, R330, CAP, MATRIX = 'BREADBOARD', 'BACKING', 'NANO', 'R12K', 'R330', 'CAP', 'MATRIX'
BUTTON, NUT, RED_PIN, BLACK_PIN = 'BUTTON', 'NUT', 'BTN_RED_PIN', 'BTN_BLACK_PIN'
USB_B, USB_A = 'USB_B', 'USB_A'
PINS = [WS.MALE[w] for w in WS.JUMPERS]                             # the three wires' pins, in i2, i3 and b19 ('white' is drawn and named
SOCKETS = [WS.FEMALE[w] for w in WS.JUMPERS]                        # yellow, 'grey' gray), and their sockets, on the matrix's pins
STEMS = [f'STEM_{k:02d}' for k in range(1, 65)]

# ---------------------------------------------------------------- the Full Build, as guide.py last wrote it
FULL = json.loads((HERE / 'steps.json').read_text(encoding='utf-8'))
VIEW = {v['name']: v for v in FULL['views']}
ROUTES = FULL['routes']


def leads(step, prefix):
    """The routes of a set of wires in a Full Build view: {wire: route}."""
    return {w: ROUTES[n] for w, n in VIEW[step]['wires'].items() if w.startswith(prefix + ' ')}


def full_way_back(step, part):
    """A Full Build step's way in for one part, reversed (its stops kept, the poses between passed through)."""
    v = VIEW[step]
    own = (v.get('paths') or {}).get(part)
    way, stops = (own, (v.get('path_stops') or {}).get(part)) if own else (v['path'], v.get('stops'))
    n = len(way) - 1
    keep = {n - k for k in stops} if stops else set(range(n + 1))
    return [p if k in keep else via(p) for k, p in enumerate(way[::-1])][1:]


def shift_of(pose):
    """A pose that only moves (a shift): its [x, y, z]."""
    assert pose is None or isinstance(pose, list) or not pose.get('r'), pose
    return list(pose) if isinstance(pose, list) else (pose or {}).get('t', [0.0, 0.0, 0.0])


def slid(pose, by):
    """A Full Build pose moved on by a shift (D2 slid out with the button on it): only t changes, and a via() stays a via()."""
    by = shift_of(by)
    if isinstance(pose, dict):
        return type(pose)(dict(pose, t=[round(a + b, 3) for a, b in zip(pose.get('t', [0.0, 0.0, 0.0]), by)]))
    return [round(a + b, 3) for a, b in zip(pose, by)]


g = Guide(HERE, title='Laser Stem Matrix (LSM)', part='Deconstruction', names=dict(FULL['names']), steps_file='steps-deconstruction.json',
          source='lsm.glb', hero_azimuth=45, copyright_line='© TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')
g.take_apart(parts_list_at_end=True,                                # (the Full Build's parts list at the end, as the MRA's ...
             completed_view=False,                                  #  straight after the last step: no Completed View, Lee 22 Oct 2026)
             leave_out=[BACKING])                                   # (peeled off in the Full Build's Step 1 and never back)


def where(i):
    """Where a part is now (on what it rides, if it rides)."""
    if i in g.riding:
        by, rel = g.riding[i]
        return compose(where(by), rel, g._pivot(i))
    return g.resting.get(i)


r1 = lambda v: [round(float(x), 2) for x in v]

# ---------------------------------------------------------------- the published take-apart: cameras, arrows, eyes, close-ups
# Its numbers, in our ids and mm (published-takeapart.json, extracted from its data replayed in docs/research/lsm/decon/published/; the
# published coordinates are ours). Each camera as the published one (its direction, target and radius: our player frames a radius as
# its own field of view does); each arrow the published one's length and shaft width, its tail where the published tail is (as Lee
# had the PMG's: "the arrow sizes ... Examine the Cadasio"), along the part's own way.
PUB = json.loads((HERE / 'published-takeapart.json').read_text(encoding='utf-8'))['steps']
assert PUB['Step 1']['camera']['fov'] == 45.0


def cam(step):
    """The published step's camera."""
    c = PUB[step]['camera']
    return dict(view_dir=[round(x, 4) for x in c['view_dir']], frame=(r1(c['target']), round(c['radius'], 1)))


def arrow(step, k=0, at=None, **more):
    """The published step's k-th arrow: its size (length, shaft width), its tail where the published one's is (at=, a tail given;
    at=False, the generator's place for it)."""
    a = PUB[step]['arrows'][k]
    return dict(dims=(round(a['length'], 1), round(a['width'], 1)), **({} if at is False else {'at': r1(a['tail'] if at is None else at)}), **more)


def eye(step, k=0, **more):
    """The published step's k-th eye: on our part, at the published ring (the part is in its seat there)."""
    e = PUB[step]['eyes'][k]
    return dict(id=e['part'], anchor=r1(e['ring']), **more)


def ring(step, k=0):
    return np.array(PUB[step]['insets'][k]['ring'])


# The published D2 on its own stood 0.6 mm off where ours stands (its 57.1 mm out): its points carried onto ours.
PUB_D2 = np.array([0.63, -0.58, 57.11])
D2_OUT = shift_of(VIEW['Step 24']['path'][0])                       # (57.1 mm out: where the Full Build had it, Steps 21 - 23)
to_ours = lambda p: np.asarray(p, float) - PUB_D2 + D2_OUT


def tab_ends(part, wall):
    """The ends of `part`'s tabs that pass through `wall` (out past its outer face), one point per tab: for a close-up's red boxes."""
    v, (lo, hi) = np.asarray(g.model.inst[part].vertices), g.model.inst[wall].bounds
    across = 0 if hi[0] - lo[0] < hi[2] - lo[2] else 2              # (the wall's thin axis)
    out = v[v[:, across] < lo[across]] if (lo[across] + hi[across]) / 2 < v[:, across].mean() else v[v[:, across] > hi[across]]
    y = out[:, 1].round(1)
    ys = np.unique(y)
    groups = np.split(ys, np.where(np.diff(ys) > 10.0)[0] + 1)       # (one group per tab, by height: the tabs are 6 mm tall, far apart)
    return [r1(out[(y >= gr[0]) & (y <= gr[-1])].mean(0)) for gr in groups]


def off_face(post, tail):
    """A D11 post's arrow tail moved out to 2.7 mm off the post's outer face: the published tails are on the face, so that half the
    shaft was inside the post (Lee, 22 Oct 2026, Step 7)."""
    lo, hi = g.model.inst[post].bounds
    x = hi[0] + 2.7 if tail[0] > (lo[0] + hi[0]) / 2 else lo[0] - 2.7
    return [round(float(x), 2), *tail[1:]]


def latch_foot(post):
    """Where a D11 post's tab goes down into D1, on the post's outer face, just above D1: the latch, its barb under D1 (Lee, 22 Oct
    2026, Steps 6 and 7: the eye "at the bottom where the actual latch element is", not half-way up the post as published)."""
    v, (lo, hi) = np.asarray(g.model.inst[post].vertices), g.model.inst[post].bounds
    (d_lo, d_hi) = g.model.inst[D1].bounds
    outer = lo[0] if (lo[0] + hi[0]) / 2 < (d_lo[0] + d_hi[0]) / 2 else hi[0]
    tab = v[v[:, 1] < d_hi[1]]                                       # (the tab, through D1)
    return r1([outer, d_hi[1] + 1.0, (tab[:, 2].min() + tab[:, 2].max()) / 2])


def latch_box(step):
    """The latch on D1 under a wall's foot, both its tabs (Lee, 22 Oct 2026, Steps 15 and 16: the red box "needs to include both tabs
    of the latch"; the published ring is on one of them): the close-up's target between them, and a box round both, 1.75 mm to spare."""
    p, v = ring(step), np.asarray(g.model.inst[D1].vertices)
    near = v[(np.abs(v[:, 0] - p[0]) < 15.0) & (np.abs(v[:, 2] - p[2]) < 6.0)]
    x0, x1 = float(near[:, 0].min()), float(near[:, 0].max())
    y0, y1 = float(near[:, 1].min()), float(near[:, 1].max())      # (in height too: D3's published ring was on D1's lower face)
    return dict(target=r1([(x0 + x1) / 2, (y0 + y1) / 2, p[2]]), mark=round((x1 - x0) / 2 + 1.75, 1))


def tab_under_d1(post):
    """The tip of a D11 post's tab under D1 (a close-up's target)."""
    v = np.asarray(g.model.inst[post].vertices)
    return r1(v[v[:, 1] < 859.0].mean(0))


PULL = 'Pull each wire out by its connector. Do not pull on the wires themselves.'
POWER = 'Disconnect the USB Cable from the computer or power supply before you begin.'

# ================================================================ FROM THE TOP: THE STEMS, D8, D7
g.remove('Remove all 64 LED Stems from D8, D7, and D6.', STEMS, units=[STEMS], caution=POWER,   # (in one step, as published: one arrow)
         arrow_style={STEMS[0]: arrow('Step 1')}, eye=[eye('Step 1', side='up-left')], **cam('Step 1'))   # (the eye clear of the arrow)
g.remove('Remove D8 from the latches of the four D11 posts.', [D8], arrow_style={D8: arrow('Step 2')}, eye=[eye('Step 2')],
         inset=dict(target=r1(ring('Step 2')), dir=PUB['Step 2']['camera']['view_dir'], radius=7.0, mark=4.0,
                    caption='The latch on each D11 post', alt='Close-up of D8 under the latch at the top of a D11 post'),
         **cam('Step 2'))
g.remove('Remove D7 from the four D11 posts.', [D7], arrow_style={D7: arrow('Step 3')}, eye=[eye('Step 3')],
         inset=dict(target=r1(ring('Step 3')), dir=PUB['Step 3']['camera']['view_dir'], radius=7.0, mark=4.0, side='left',   # (on the
                    caption='D7 in the notch of each D11 post', alt='Close-up of D7 in the notch of a D11 post'),   # left, not across the model: Lee)
         keep_camera=True)                                          # (the published camera of Step 2, kept)

# ================================================================ THE ENDS: D5 AND D4 (D10's ends come free of their slots)
# (Lee, 22 Oct 2026: the arrows of D5 and D4 from their outer faces, the published ones started inside them; an eye on each of D3's two
# tabs through the wall, beside the model, level with its tab)
g.remove('Remove D5 from the tabs of D1, D2, and D3.', [D5], arrow_style={D5: arrow('Step 4', at=[684.0, 855.9, 1204.3])},
         eye=[dict(id=D3, anchor=p, side='right') for p in tab_ends(D3, D5)],
         inset=dict(target=r1(np.mean(tab_ends(D2, D5), axis=0)), dir=PUB['Step 4']['camera']['view_dir'], radius=26.0,
                    marks=[(p, 6.5) for p in tab_ends(D2, D5)], caption="D2's tabs through D5",
                    alt="Close-up of the corner of D5 and D2: red boxes around the ends of D2's two tabs, which pass through D5"),
         **cam('Step 4'))
g.remove('Slide D4 off the tabs of D1, D2, and D3, along the USB Cable. Then, lift it up off the cable.', [D4],
         path=[[-75.0, 0.0, 0.0], [-75.0, 40.0, 0.0]],              # (straight out, as published, the USB cable in the notch at its foot; then
         arrow_style={D4: arrow('Step 5', at=[593.0, 855.4, 1204.4], stage=0, then=[dict(dims=(40.0, 6.2), stage=1)])},   # up off it: an
         eye=[dict(id=D3, anchor=p, side='left') for p in tab_ends(D3, D4)],                                                 #  arrow each)
         inset=dict(target=r1(np.mean(tab_ends(D2, D4), axis=0)), dir=PUB['Step 5']['camera']['view_dir'], radius=26.0, side='right',
                    marks=[(p, 6.5) for p in tab_ends(D2, D4)], caption="D2's tabs through D4",
                    alt="Close-up of the corner of D4 and D2: red boxes around the ends of D2's two tabs, which pass through D4"),
         **cam('Step 5'))

# ================================================================ THE D11 POSTS, TWO AND TWO, AND D6
# Each post's tab passes through a slot in D1, its barb caught underneath: pushed up out of D1 first (as the Full Build pushed it home,
# its Step 36), then up out of D6's corner slot (34, 35). A close-up from below of a tab through D1, as the Full Build's Step 36c's,
# on the post the published close-up shows, seen from outside its corner.
D11_SHORT, D11_UP = VIEW['Step 34c']['carry'][D11_A]['pose'], VIEW['Step 34']['carry'][D11_A]['pose']   # (the tabs at D1's top; up)
TAB = VIEW['Step 36c']['inset']
for step, pair, caption in (('Step 6', [D11_D, D11_C], 'Lift the box and push the tabs of the two D11 posts nearest the USB Cable up '
                                                       'out of the slots in D1 from underneath. Then, push each tab up through its corner '
                                                       'slot in D6, and remove the posts.'),
                            ('Step 7', [D11_A, D11_B], 'Push the tabs of the other two D11 posts up out of D1 and through D6 the same '
                                                       'way, and remove the posts.')):
    tip = tab_under_d1(PUB[step]['insets'][0]['part'])
    out_x, out_z = (1.0 if tip[0] > 640 else -1.0), (1.0 if tip[2] > 1204 else -1.0)
    tails = {i: off_face(i, PUB[step]['arrows'][k]['tail']) for k, i in enumerate(pair)}
    if step == 'Step 6':                                            # (6 mm lower, beside the posts: the left one's head was under the
        tails = {i: [x, round(y - 6.0, 2), z] for i, (x, y, z) in tails.items()}   #  caution box, three lines tall, at 1024 x 768)
    g.remove(caption, pair, paths={i: [D11_SHORT, D11_UP] for i in pair},
             arrow_style={i: arrow(step, k, at=tails[i]) for k, i in enumerate(pair)},
             eye=[dict(id=PUB[step]['eyes'][0]['part'], anchor=latch_foot(PUB[step]['eyes'][0]['part']))],   # (the published post, at its foot)
             inset=dict(target=[tip[0], 857.0, tip[2]], dir=[round(0.4109 * out_x, 4), -0.8401, round(0.3541 * out_z, 4)],
                        radius=TAB['radius'], mark=4.0, caption='The tab through D1', alt=TAB['alt'],
                        **({'side': 'right'} if step == 'Step 6' else {})),   # (Step 6's on the right, not across the model: Lee)
             caution='Squeeze the two prongs of each tab together to free its barb, under D1 and again under D6.',   # (each tab's barb
             **cam(step))                                           #  catches at both: feasibility, docs/research/lsm/decon/published/)
g.remove('Remove D6 from the tabs of D2 and D3.', [D6], arrow_style={D6: arrow('Step 8')}, **cam('Step 8'))

# ================================================================ THE LED MATRIX: OUT OF THE BOX, OFF D10, OFF ITS WIRES
# Lifted with D10 under it (D4 and D5 are off, so D10's ends are free) the way the Full Build lowered it in (its Step 32, reversed: its
# wires through the Full Build's own half-way shape to the held one), and held there, over the box, while D10 and then the wires come off
# it (Lee, 22 Oct 2026: "D10 should be removed at this point and the wires disconnected from the LED Matrix in a group, but left attached
# to the breadboard, then the breadboard wires moved. Remember, D10 must slide off of the LED Matrix"). The published guide has the
# matrix there too for D10 and the connectors (its Steps 14 and 15, at [0, 56.6, -0.5]; ours [-0.2, 56.6, -0.3]), so theirs are the
# cameras. The study behind this: docs/research/lsm/decon/round3/.
MATRIX_UP = arrow('Step 9', at=apply_pose(where(MATRIX), [[612.8, 899.0, 1178.0]])[0])   # (the published size; its tail was Step 8's, left
g.lift('Lift the LED Matrix, with D10 hooked under it, up off the two D9 pieces. Leave its wires connected.', [MATRIX],   # over: on the
       wire_via={w: [ROUTES[n] for n in nos[::-1]] for w, nos in VIEW['Step 32c']['wire_via'].items()},          # matrix's corner nearest
                                                                    # the camera here, so that its head is clear of the caption box in a
                                                                    # 1024 x 768 window)
       wires=leads('Step 32', 'wire'), arrow_style={MATRIX: MATRIX_UP}, **cam('Step 9'))
HELD = where(MATRIX)
# D10's hooks hold both edges of the matrix: the Full Build hooked it on here, its Step 31 (up under the held matrix, then slid along until
# they held both edges), with the wires as they are now, lying dead straight through D10's notch all along the slide. So it comes off by
# that step reversed: slid 40 mm along the matrix toward D2, away from its pins, until the hooks are free, then down 22 mm to where the
# Full Build brought it up from (still clear of D2 and the D9s). (Slid with the matrix laid on the table, the wires had other shapes and
# passed through it: Lee's note on Step 13, 22 Oct 2026.) An arrow for each stage, in turn: the slide's under D10's end nearest the
# camera, low and far enough out that D10 hides none of it, the drop's in front of D10 once it has slid (30 mm: it drops 22, the
# published one 48).
D10_FREE, D10_UNDER = VIEW['Step 31c']['carry'][D10]['via'][0], VIEW['Step 31']['carry'][D10]['pose']   # ([0, 0, 40], [0, -22, 40]: on it)
on_matrix = lambda rel: compose(HELD, rel, g._pivot(D10))
g.remove('Slide D10 along the bottom of the LED Matrix, away from its pins, until its hooks come free of the edges. Then, remove it.', [D10],
         path=[on_matrix(D10_FREE), on_matrix(D10_UNDER)],
         arrow_style={D10: dict(dims=(40.0, 4.4), stage=0, at=r1(apply_pose(on_matrix(ZERO), [[597.2, 876.9, 1206.5]])[0]),
                                then=[dict(dims=(30.0, 4.4), stage=1, at=r1(apply_pose(on_matrix(D10_FREE), [[597.2, 880.0, 1202.4]])[0]))])},
         eye=[dict(id=D10, anchor=[600.7, 897.7, 1203.0])],          # (the published eye: on the hook at D10's end nearest the camera)
         **cam('Step 14'))
# Then the matrix is pulled back along its pins off the three connectors, 30 mm as the published guide pulls them apart, and is gone; the
# connectors stay where they came off (let_go, as the PMG's displays off their wires' caps), the wires left in the breadboard as they are
# (Lee: "left attached to the breadboard"). Its pins are 6.8 mm into them; nothing else of it is below its back face there, 0.39 mm over
# the connectors, so it slides clear. Seen from under it (Lee's view, 22 Oct 2026, solved from his picture by the corners of the board's
# underside: the camera out past the open D4 end, below the matrix, the connectors and the board's printing in view). Its arrow is under
# it, toward the camera, so that the matrix (a plate moving along itself) covers none of it (as Lee had the PMG's), clear of the header.
g.remove('Disconnect the three breadboard wires from the V+, IN, and V- pins on the LED Matrix, and remove the LED Matrix. Leave the '
         'wires in the breadboard.', [MATRIX], let_go=SOCKETS, path=[_shifted(HELD, [0.0, 0.0, -30.0])],
         arrow_style={MATRIX: arrow('Step 15', at=[640.0, 941.0, 1204.0])},   # (the published size)
         eye=[dict(id=WS.FEMALE['purple'], side='near-left')],       # (the published eye)
         caution="Hold the three black connectors while you pull the LED Matrix's pins out of them. Do not pull on the wires themselves.",
         view_dir=[-0.893, -0.4496, -0.0207], frame=([643.5, 942.9, 1196.6], 47.5))   # (Lee's view)
# The three wires, still in the breadboard, laid out of the way, out over the box's open end where D4 was and onto the table (Lee, 22 Oct
# 2026: "Add a step that lays the three wires over the side of the box, still in the breadboard, before the D9s come out"): each keeps
# its run in the box, under D9_A, and turns out over D1's edge, its connector set down on the table (wire_shapes.py: DRAPED; the run in
# the box stays put as they move). An eye on a connector and no arrow, as a plug moved on its lead (rulebook section 11).
g.lift('Lay the three breadboard wires out of the box, over the open end where D4 was. Leave them in the breadboard.', SOCKETS,
       paths={WS.FEMALE[w]: [WS.draped_socket(w)] for w in WS.JUMPERS}, wires=WS.draped(), arrows=[],
       eye=[dict(id=WS.FEMALE['purple'])], view_dir=[-0.62, 0.58, 0.53], frame=([559.0, 915.0, 1241.0], 92.0))   # (from the open end's
                                                                    #  corner by D2: the wires turning out over D1's edge, along the
                                                                    #  table and their connectors in view at every shape of window)
# Both D9 (before the wires, as published: they run under D9_A). The published tails were 8.6 mm down inside the D9s, and at their place
# along the D9s D9_A's tail sits in its top edge's notch, over the USB plug, as if lifting it: these start near the D9s' D3 ends, just
# over D3's top edge (which hid them from the D9s' own tops); one size for the two (like parts, Lee 22 Oct 2026: the published sizes
# differed).
D9_TAIL_Y = float(g.model.inst[D3].bounds[1][1]) + 1.0
g.remove('Remove both D9 pieces from the slots in D2 and D3.', [D9_A, D9_B],
         arrow_style={D9_B: arrow('Step 10', 0, at=[657.17, D9_TAIL_Y, 1160.0]), D9_A: arrow('Step 10', 0, at=[618.76, D9_TAIL_Y, 1160.0])},
         view_dir=cam('Step 10')['view_dir'], frame=([605.0, 885.0, 1210.0], 106.0))   # (the published direction; framed as before)

# ================================================================ THE THREE WIRES OUT OF THE BREADBOARD (in one step: Lee)
# Each wire whole: its pin straight up out of its hole (the Full Build's way, reversed) and its connector with it.
g.remove('Disconnect the yellow, gray, and purple breadboard wires from i2, i3, and b19.', PINS + SOCKETS,
         paths={**{p: [[0.0, 30.0, 0.0]] for p in PINS}, **{c: [_shifted(where(c), [0.0, 30.0, 0.0])] for c in SOCKETS}},
         arrows=[], eye=[eye('Step 13'), eye('Step 12')], caution=PULL,   # (an eye on i2 / i3 and one on b19)
         view_dir=cam('Step 11')['view_dir'], frame=([583.0, 883.0, 1200.0], 112.0))   # (the published direction, framed wider toward
                                                                    #  the open end: the wires reach out to their connectors on the table)

# ================================================================ D3, D2 WITH THE PUSH BUTTON
g.remove('Remove D3 from the latch on D1.', [D3], direction=[0.0, 0.0, -1.0], hover=40.0, arrow_style={D3: arrow('Step 16')},
         inset=dict(**latch_box('Step 16'), dir=[0.0, 0.34, -0.94], radius=20.0,
                    caption='The latch on D1 at the foot of D3', alt='Close-up of the latch on D1 that holds the foot of D3'),
         **cam('Step 16'))
g.lift("Slide D2, with the Push Button, off the latch on D1 and out of its slots. Leave the Push Button's wires connected.", [D2],
       wires=leads('Step 24', 'lead'),                              # (the Full Build's Step 24 reversed: the leads as they lay before it)
       arrow_style={D2: arrow('Step 17')},
       inset=dict(**latch_box('Step 17'), dir=[0.0, 0.34, 0.94], radius=20.0,
                  caption='The latch on D1 at the foot of D2', alt='Close-up of the latch on D1 that holds the foot of D2'),
       view_dir=[0.5997, 0.5299, 0.5997], frame=([640.0, 878.0, 1262.0], 95.0))   # (from outside D2, the title page's corner: its foot, the latch
                                                                    #  and the arrow show; the published camera, inside, saw them through D2)
g.unplug("Disconnect the Push Button's red wire from j5 and its black wire from j16.", [RED_PIN, BLACK_PIN], caution=PULL,
         **cam('Step 17'))                                          # (the Full Build's Steps 22 and 21, reversed: an eye on each pin; the
                                                                    #  published camera, inside, where the pins are)

# ================================================================ THE PUSH BUTTON ON ITS OWN
# The nut comes off in one smooth go (Lee, 22 Oct 2026), turning the way that unscrews it all the way off over the wires and past their
# pins' ends, and is set aside (lift, not remove: it goes back on the button, below).
NUT_AT = VIEW['Step 20']['paths'][NUT][1]['at']                     # (the button's axis, as the Full Build turned the nut about it)
turn = lambda deg, z: dict(t=[0.0, 0.0, round(z, 3)], r=[0.0, 0.0, 1.0, float(deg)], at=NUT_AT)
OFF_D2 = [via(turn(720 - 90 * k, -95.0 * k / 8)) for k in range(1, 8)] + [[0.0, 0.0, -95.0]]   # (eight quarter turns over 95 mm, one beat)
g.lift('Unscrew the nut from the Push Button, on the inside of D2, and slide it off over the wires.', [NUT],
       path=[slid(p, D2_OUT) for p in OFF_D2], alone=[D2, BUTTON, NUT, RED_PIN, BLACK_PIN],
       arrow_style={NUT: arrow('Step 18', at=[650.0, 890.0, 1303.0])},   # (the published size, beside the nut, above the button's axis: the
       eye=[NUT], **cam('Step 18'))                                  #  published tail, 40 mm on along the wires, read as the wires')
BUTTON_OUT = [slid(p, D2_OUT) for p in full_way_back('Step 19', BUTTON)]   # (the Full Build's way through D2, reversed: 100 mm out)
g.lift('Remove the Push Button from D2, pulling its wires back through the hole.', [BUTTON], path=BUTTON_OUT,   # (set aside: the nut goes
       alone=[D2, BUTTON, RED_PIN, BLACK_PIN], arrow_style={BUTTON: arrow('Step 19', at=to_ours(PUB['Step 19']['arrows'][0]['tail']))},   # back on)
       eye=[dict(id=BUTTON, side='near-above')], **cam('Step 19'))  # (from D2's engraved face, as published; the eye above the button,
g.put_away([D2])                                                    #  its leader clear of the arrow, Lee, and of the wires)
# After the button is out of D2, the nut goes back on it, over the wires (Lee, 22 Oct 2026: "we need a step that shows the nut being
# replaced onto the push button"), to where the button comes with it, screwed up to its head (the Full Build's g.carry([NUT], by=BUTTON,
# pose=[0, 0, 3.12])). It starts just off the end of the wires (Lee, the same day: "The movement through empty space with the spread out
# view is not needed, start the nut just off the end of the push button's wires, then animate it back on"): laid there once D2 is put
# away (the view after starts afresh), then on in one smooth go, as Step 18 took it off: eight quarter turns, the screwing way.
B = shift_of(BUTTON_OUT[-1])[2]                                     # (the button, 100 mm out of where D2 stood: z offset 157.1)
END = B + 3.12
PIN_TIP = min(float(apply_pose(where(p), np.asarray(g.model.inst[p].vertices))[:, 2].min()) for p in (RED_PIN, BLACK_PIN))
START = round(PIN_TIP - 5.0 - float(np.asarray(g.model.inst[NUT].vertices)[:, 2].max()), 2)   # (its face 5 mm off the pins' ends)
g.rest_at([NUT], [0.0, 0.0, START])
ON = [via(turn(90 * k, START + (END - START) * k / 8)) for k in range(1, 8)] + [[0.0, 0.0, round(END, 3)]]
ON_SET = [BUTTON, NUT, RED_PIN, BLACK_PIN]
g.lift('Slide the nut back over the Push Button\'s wires and screw it onto the Push Button, so that the two stay together.', [NUT],
       path=ON, ride_on=BUTTON, alone=ON_SET, eye=[NUT],
       arrow_style={NUT: arrow('Step 18', at=r1(np.asarray(g.model.inst[NUT].bounds).mean(0) + [0.0, 16.5, START]))},   # (Step 18's size, just
                                                                    #  above the nut, clear of the wires it slides over)
       view_dir=[-0.7741, 0.6193, 0.1316], frame=([638.2, 881.6, 1366.0], 58.0))   # (from the side, close: the nut, the wires, the button)
g.put_away(ON_SET)

# ================================================================ THE USB CABLE AND THE BREADBOARD'S PARTS
g.remove('Disconnect the USB Cable from the Nano Board.', [USB_B, USB_A], units=[[USB_B]], arrow_style={USB_B: arrow('Step 20')},
         paths={USB_A: [[0.0, 0.0, 25.0]]}, eye=[USB_B],             # (one arrow, on the plug; the A end moves with it: the cable goes whole)
         view_dir=cam('Step 20')['view_dir'], frame=([575.0, 868.0, 1220.0], 105.0))   # (the published direction, aimed so that the cable's
                                                                    #  A end stays in the frame in a narrower window)
g.remove('Remove the 330 Ω Resistor from a11 and a19.', [R330], arrow_style={R330: arrow('Step 21')}, **cam('Step 21'))
g.remove('Remove the Capacitor from j2 and j3.', [CAP], arrow_style={CAP: arrow('Step 22')}, **cam('Step 22'))
g.remove('Remove the 12 kΩ Resistor from h3 and h16.', [R12K], arrow_style={R12K: dict(arrow('Step 23'), dims=arrow('Step 21')['dims'])},
         keep_camera=True)                                          # (as big as the 330 ohm resistor's: Lee, 22 Oct 2026)
g.remove('Remove the Nano Board from the Breadboard.', [NANO], arrow_style={NANO: arrow('Step 24', at=[642.6, 879.0, 1182.8])},   # (above
                                                                    # the board: the published tail was inside it, Lee; moved 5 mm
                                                                    # across the board and 4.5 along, its head clear of the caution box)
         caution='Use the Pry Tool to carefully remove the Nano Board.', keep_camera=True)   # (the kit has one, not modelled: Lee)

g.build()
