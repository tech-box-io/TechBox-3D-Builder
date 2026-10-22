"""Laser Stem Matrix (LSM), deconstruction: the finished kit taken apart, down to D1 with the breadboard stuck on it, in the order and
the manner of TechBox's own published take-apart (Lee, 21 Oct 2026: "you need to base the deconstruction process off of this guide:
https://instructions.online/?id=19075-laser_stem_matrix_lsm_-_deconstruction"). A guide of its own (steps-deconstruction.json), made
from the Full Build as guide.py last wrote it (run that first, and this again after any change to it). It opens on the Full Build's
title page, ends on what is left (D1 and the breadboard, as the published take-apart ends), followed by the Full Build's parts list,
and its card on the website is the Full Build's.

The published take-apart, step by step (docs/research/guide_19075-laser_stem_matrix_lsm_-_deconstruction.md; its data replayed in our
part ids and mm: docs/research/lsm/decon/published/), outside in: the stems; D8; D7; D5 and D4 off the ends (which frees D10's ends);
the D11 posts two and two; D6; the LED matrix lifted out with D10 under it and set down beside the box, still wired; both D9; the three
breadboard wires out of the breadboard; the matrix on its own: D10 off, the wires' connectors off its pins; D3; D2 with the push button,
its two wires unplugged; the button on its own: the nut, the button out of D2; the USB cable; the 330 ohm resistor, the capacitor, the
12 kOhm resistor and the Nano Board. Each step has the published camera, arrows of the published size where the published tail is,
the published eyes, and a close-up where the published guide has one (each catch to release: D8's latches, D7's notches, the tabs at
D5's and D4's corners, the D11 posts' tabs under D1, D3's and D2's latches on D1), drawn from our model with a red box on the catch.
Where it differs, and why: the three wires come out in one step (Lee: "some things can be removed in groups (like the 3 breadboard
wires)"); the matrix's lift and its setting down are two steps (the published guide swaps two models in one); D2 comes off before its
wires are unplugged (one step each); D4, once off its tabs, is lifted off the USB cable (its notch held it); D10 is slid off its hooks
before it drops (they hold both edges of the matrix: a two-stage joint undone in one step, rulebook section 11; the published guide
drops it through them); the matrix on its own stays where it was laid (the published guide puts it back over the box), so that view's
camera and arrow are carried there; a few cameras and arrows are moved where ours would hide or lose what the published one showed (Step
16 from outside D2, whose latch and arrow the published camera saw through D2; Steps 10 and 11 framed to hold the laid matrix in a tall
window; Step 20 to hold the cable's A end; the arrows of Steps 14 and 18 at the connectors and the nut, not 40 mm away along the
wires). Two steps on one sub-assembly change camera where the published guide does (Steps 13 - 14, 18 - 19). Setting the matrix down
and unplugging the wires are fades, as the published guide's model swaps (and the rulebook's unplugging: "by swapping the routed model
for a loose one"); the wires' new shapes (laid aside, loose) are drawn and measured in wire_shapes.py. No counterpart for the Full
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
from stepgen import Guide, _shifted, apply_pose, compose, turn_dir, via  # noqa: E402

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
g.take_apart(parts_list_at_end=True,                                # (the Full Build's parts list, after the Completed View, as the MRA's)
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
assert PUB['Step 1']['camera']['fov'] == 45.0 and WS.LAID_POSE['r'] == [0.0, 1.0, 0.0, 180.0]   # (to_laid and laid_cam turn by it)


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


# The published guide shows the matrix on its own where it hovered over the box (a glitch: it had been laid aside); ours stays where it
# was laid, so that view's camera and arrows are carried there, turned with the matrix.
HOVER = np.array([0.0, 56.64, -0.52])                                # the published matrix's hover, from its seat
to_laid = lambda p: apply_pose(WS.LAID_POSE, [np.asarray(p, float) - HOVER])[0]


def laid_cam(step):
    c = PUB[step]['camera']
    return dict(view_dir=[round(float(x), 4) for x in turn_dir(WS.LAID_POSE, c['view_dir'])], frame=(r1(to_laid(c['target'])), round(c['radius'], 1)))


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
         inset=dict(target=r1(ring('Step 2')), dir=PUB['Step 2']['camera']['view_dir'], radius=7.0, mark=2.5,
                    caption='The latch on each D11 post', alt='Close-up of D8 under the latch at the top of a D11 post'),
         **cam('Step 2'))
g.remove('Remove D7 from the four D11 posts.', [D7], arrow_style={D7: arrow('Step 3')}, eye=[eye('Step 3')],
         inset=dict(target=r1(ring('Step 3')), dir=PUB['Step 3']['camera']['view_dir'], radius=7.0, mark=2.5,
                    caption='D7 in the notch of each D11 post', alt='Close-up of D7 in the notch of a D11 post'),
         keep_camera=True)                                          # (the published camera of Step 2, kept)

# ================================================================ THE ENDS: D5 AND D4 (D10's ends come free of their slots)
g.remove('Remove D5 from the tabs of D1, D2, and D3.', [D5], arrow_style={D5: arrow('Step 4')}, eye=[eye('Step 4')],
         inset=dict(target=r1(np.mean(tab_ends(D2, D5), axis=0)), dir=PUB['Step 4']['camera']['view_dir'], radius=26.0,
                    marks=[(p, 4.5) for p in tab_ends(D2, D5)], caption="D2's tabs through D5",
                    alt="Close-up of the corner of D5 and D2: red boxes around the ends of D2's two tabs, which pass through D5"),
         **cam('Step 4'))
g.remove('Slide D4 off the tabs of D1, D2, and D3, along the USB Cable. Then, lift it up off the cable.', [D4],
         path=[[-75.0, 0.0, 0.0], [-75.0, 40.0, 0.0]],              # (straight out, as published, the USB cable in the notch at its foot; then
         arrow_style={D4: arrow('Step 5', stage=0, then=[dict(dims=(40.0, 6.2), stage=1)])}, eye=[eye('Step 5')],   # up off it: an arrow each)
         inset=dict(target=r1(np.mean(tab_ends(D2, D4), axis=0)), dir=PUB['Step 5']['camera']['view_dir'], radius=26.0,
                    marks=[(p, 4.5) for p in tab_ends(D2, D4)], caption="D2's tabs through D4",
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
    g.remove(caption, pair, paths={i: [D11_SHORT, D11_UP] for i in pair},
             arrow_style={i: arrow(step, k) for k, i in enumerate(pair)}, eye=[eye(step)],
             inset=dict(target=[tip[0], 857.0, tip[2]], dir=[round(0.4109 * out_x, 4), -0.8401, round(0.3541 * out_z, 4)],
                        radius=TAB['radius'], mark=2.5, caption='The tab through D1', alt=TAB['alt']),
             caution='Squeeze the two prongs of each tab together to free its barb, under D1 and again under D6.',   # (each tab's barb
             **cam(step))                                           #  catches at both: feasibility, docs/research/lsm/decon/published/)
g.remove('Remove D6 from the tabs of D2 and D3.', [D6], arrow_style={D6: arrow('Step 8')}, **cam('Step 8'))

# ================================================================ THE LED MATRIX, OUT OF THE BOX AND SET DOWN, STILL WIRED
# Lifted with D10 under it (D4 and D5 are off, so D10's ends are free) the way the Full Build lowered it in (its Step 32, reversed: its
# wires through the Full Build's own half-way shape to the held one), then set down on the table beside the box by a fade, as the
# published guide swaps the model, its wires into the shapes wire_shapes.py draws (out through the open D4 end).
MATRIX_UP = arrow('Step 9', at=apply_pose(where(MATRIX), [[638.8, 899.0, 1204.0]])[0])   # (the published size; its tail was Step 8's, left
g.lift('Lift the LED Matrix, with D10 hooked under it, up off the two D9 pieces. Leave its wires connected.', [MATRIX],   # over: on the
       wire_via={w: [ROUTES[n] for n in nos[::-1]] for w, nos in VIEW['Step 32c']['wire_via'].items()},          # matrix's middle here)
       wires=leads('Step 32', 'wire'), arrow_style={MATRIX: MATRIX_UP}, **cam('Step 9'))
g.lift('Set the LED Matrix down on the table beside the box. Leave its wires connected.', [MATRIX], to=WS.LAID_POSE, reappear=True,
       wires=WS.laid(), arrows=[], eye=[MATRIX],                    # (a fade, as the published guide's swap: an eye on it, no arrow)
       view_dir=cam('Step 9')['view_dir'], frame=([605.0, 895.0, 1215.0], 110.0))   # (Step 9's direction, framed to hold the box, the held
g.remove('Remove both D9 pieces from the slots in D2 and D3.', [D9_A, D9_B],      #  matrix and where it is laid, in a window taller than wide)
         arrow_style={D9_B: arrow('Step 10', 0), D9_A: arrow('Step 10', 1)},
         view_dir=cam('Step 10')['view_dir'], frame=([605.0, 885.0, 1210.0], 106.0))   # (the published direction; the laid matrix in frame too)

# ================================================================ THE THREE WIRES OUT OF THE BREADBOARD (in one step: Lee)
# A fade, as the published guide swaps each wire for a loose one: the pins lie on the table by the matrix, riding on it from now on.
g.unplug('Disconnect the yellow, gray, and purple breadboard wires from i2, i3, and b19.', PINS, ride_on=MATRIX, reappear=True,
         paths={WS.MALE[w]: [WS.pin_pose(w)] for w in WS.JUMPERS}, wires=WS.loose(),
         eye=[eye('Step 13'), eye('Step 12')], caution=PULL, **cam('Step 11'))   # (an eye on i2 / i3 and one on b19)

# ================================================================ THE LED MATRIX ON ITS OWN
# D10's hooks hold both edges of the matrix (the Full Build slid it on, its Step 31): slid back along 40 mm, then down, an arrow for each
# (a two-stage joint undone in one step, rulebook section 11; the published guide drops it straight, through the hooks).
UNHOOKED, DOWN = VIEW['Step 31c']['carry'][D10]['via'][0], VIEW['Step 31']['carry'][D10]['pose']   # ([0, 0, 40], [0, -22, 40]: on the matrix)
DOWN = [DOWN[0], DOWN[1] - 18.0, DOWN[2]]                           # (40 mm down in all, as far as the published drop)
LAID_VIEW = lambda step, target: dict(laid_cam(step), frame=(target, laid_cam(step)['frame'][1]))   # (the published camera carried to the
g.remove('Slide D10 along the bottom of the LED Matrix, away from its pins, until its hooks come free of the edges. Then, remove it.',   # laid
         [D10], path=[compose(where(MATRIX), UNHOOKED, g._pivot(D10)), compose(where(MATRIX), DOWN, g._pivot(D10))],   # matrix, aimed at it:
         alone=[MATRIX, D10, *PINS, *SOCKETS], arrow_style={D10: dict(dims=(40.0, 4.4), stage=0,              # the published one aimed under
                                                                      then=[arrow('Step 14', at=False, stage=1)])},   # the matrix)
         eye=[D10], **LAID_VIEW('Step 14', [550.0, 862.0, 1226.0]))
LAID = where(MATRIX)
g.remove('Disconnect the three breadboard wires from the V+, IN, and V- pins on the LED Matrix.', PINS + SOCKETS, alone=[MATRIX, *PINS, *SOCKETS],
         paths={**{WS.FEMALE[w]: [WS.socket_pose(w, LAID, off=30.0)] for w in WS.JUMPERS},
                **{WS.MALE[w]: [WS.pin_pose(w, LAID, off=30.0)] for w in WS.JUMPERS}},
         units=[SOCKETS], arrow_style={SOCKETS[0]: arrow('Step 15', at=[576.0, 875.0, 1246.0])},   # (the published size, at the connectors'
         eye=[WS.FEMALE['purple']],                                 #  end, over the matrix's edge: the published tail was by the loose pins)
         caution="Hold the three black connectors on the LED Matrix's pins while you pull them off. Do not pull on the wires themselves.",
         **LAID_VIEW('Step 15', [556.0, 864.0, 1222.0]))            # (both ends of each wire go, so the wires go with them, whole)
g.put_away([MATRIX])                                                # (what is left of the sub-assembly taken apart on its own)

# ================================================================ D3, D2 WITH THE PUSH BUTTON
g.remove('Remove D3 from the latch on D1.', [D3], direction=[0.0, 0.0, -1.0], hover=40.0, arrow_style={D3: arrow('Step 16')},
         inset=dict(target=r1(ring('Step 16')), dir=[0.0, 0.34, -0.94], radius=20.0, mark=3.0,
                    caption='The latch on D1 at the foot of D3', alt='Close-up of the latch on D1 that holds the foot of D3'),
         **cam('Step 16'))
g.lift("Slide D2, with the Push Button, off the latch on D1 and out of its slots. Leave the Push Button's wires connected.", [D2],
       wires=leads('Step 24', 'lead'),                              # (the Full Build's Step 24 reversed: the leads as they lay before it)
       arrow_style={D2: arrow('Step 17')},
       inset=dict(target=r1(ring('Step 17')), dir=[0.0, 0.34, 0.94], radius=20.0, mark=3.0,
                  caption='The latch on D1 at the foot of D2', alt='Close-up of the latch on D1 that holds the foot of D2'),
       view_dir=[0.5997, 0.5299, 0.5997], frame=([640.0, 878.0, 1262.0], 95.0))   # (from outside D2, the title page's corner: its foot, the latch
                                                                    #  and the arrow show; the published camera, inside, saw them through D2)
g.unplug("Disconnect the Push Button's red wire from j5 and its black wire from j16.", [RED_PIN, BLACK_PIN], caution=PULL,
         **cam('Step 17'))                                          # (the Full Build's Steps 22 and 21, reversed: an eye on each pin; the
                                                                    #  published camera, inside, where the pins are)

# ================================================================ THE PUSH BUTTON ON ITS OWN
NUT_WAY = [slid(p, D2_OUT) for p in full_way_back('Step 20', NUT)]  # (the Full Build's eight quarter turns, reversed: unscrewing)
NUT_WAY[3] = dict(NUT_WAY[3])                                       # (a stop after the first whole turn: a beat a turn; then off over the
NUT_WAY.append(slid([0.0, 0.0, -95.0], D2_OUT))                     #  wires, past their pins' ends)
g.remove('Unscrew the nut from the Push Button, on the inside of D2. Then, slide it off over the wires.', [NUT], path=NUT_WAY,
         alone=[D2, BUTTON, NUT, RED_PIN, BLACK_PIN], arrow_style={NUT: arrow('Step 18', at=[650.0, 890.0, 1303.0])},   # (the published size,
                                                                    # beside the nut, above the button's axis: the published tail, 40 mm on
                                                                    # along the wires, read as the wires' and left a tall window)
         eye=[NUT], **cam('Step 18'))
g.remove('Remove the Push Button from D2, pulling its wires back through the hole.', [BUTTON],
         path=[slid(p, D2_OUT) for p in full_way_back('Step 19', BUTTON)], alone=[D2, BUTTON, RED_PIN, BLACK_PIN],
         arrow_style={BUTTON: arrow('Step 19', at=to_ours(PUB['Step 19']['arrows'][0]['tail']))},
         eye=[BUTTON], **cam('Step 19'))                            # (from D2's engraved face, as published, where the button comes out)
g.put_away([D2])

# ================================================================ THE USB CABLE AND THE BREADBOARD'S PARTS
g.remove('Disconnect the USB Cable from the Nano Board.', [USB_B, USB_A], units=[[USB_B]], arrow_style={USB_B: arrow('Step 20')},
         paths={USB_A: [[0.0, 0.0, 25.0]]}, eye=[USB_B],             # (one arrow, on the plug; the A end moves with it: the cable goes whole)
         view_dir=cam('Step 20')['view_dir'], frame=([575.0, 868.0, 1220.0], 105.0))   # (the published direction, aimed so that the cable's
                                                                    #  A end stays in the frame in a narrower window)
g.remove('Remove the 330 Ω Resistor from a11 and a19.', [R330], arrow_style={R330: arrow('Step 21')}, **cam('Step 21'))
g.remove('Remove the Capacitor from j2 and j3.', [CAP], arrow_style={CAP: arrow('Step 22')}, **cam('Step 22'))
g.remove('Remove the 12 kΩ Resistor from h3 and h16.', [R12K], arrow_style={R12K: arrow('Step 23')}, keep_camera=True)
g.remove('Remove the Nano Board from the Breadboard.', [NANO], arrow_style={NANO: arrow('Step 24')},
         caution='Use the Pry Tool to carefully remove the Nano Board.', keep_camera=True)   # (the kit has one, not modelled: Lee)

c = PUB['Completed View']['camera']
g.end_view = dict(dir=c['view_dir'], target=c['target'], radius=c['radius'])   # (the published take-apart's last view)
g.build()
