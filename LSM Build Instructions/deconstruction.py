"""Laser Stem Matrix (LSM), deconstruction: the finished kit taken apart, down to D1 with the breadboard stuck on it. A guide of its own
(steps-deconstruction.json), made from the Full Build as guide.py last wrote it (run that first, and this again after any change to
it). It opens on the Full Build's title page, ends on what is left, D1 and the breadboard (as TechBox's published take-apart ends:
the breadboard is stuck on for good), followed by the Full Build's parts list (as the MRA's and PMG's), and its card on the website
is the Full Build's.

First draft (Lee, 21 Oct 2026: "take this LSM Full Build guide and create a Deconstruction Guide based on it. Same principles as you
used for the MRA. Remembering some things can be removed in groups (like the 3 breadboard wires, etc.)"): the Full Build in reverse
(rulebook section 11), some parts in groups: the 64 stems, the four D11 posts, both D9, the push button's two wires, and the three
breadboard wires (the LED matrix pulled off their connectors, then the three wires out of the breadboard together, as the PMG's).
The reasons for the order are in docs/research/lsm/decon/plan_final.md:
  1. from the top: the stems, D8, D7, the D11 posts, D6;
  2. the LED matrix out of the box, still wired, the way the Full Build brought it in, reversed, its wires through the Full Build's own
     shapes: held over the box, D10 slid off it, then carried over D4 to lie outside;
  3. the D9s; the box turned over, D5 and D3 off; the right way up, the matrix carried back over D4 to beside the D5 end (its wires
     lie over D4's top edge until then), and D4 off;
  4. D2 slid out with the push button, still wired; the USB cable unplugged (the plug's way out runs into the button until D2 is
     out); the button's wires unplugged; the button taken apart on its own (the nut, then the button out of D2);
  5. the LED matrix pulled off its three wires' connectors, then the three wires out of i2, i3 and b19 together (b19 is under the USB
     plug's leg, so they come after it); the 330 ohm resistor, the capacitor, the 12 kOhm resistor and the Nano Board.
No counterpart for the Full Build's preparation (the backing, bending legs, splitting the ribbon, the nut off a new button) or its
cards. The USB cable cannot come out first, as the MRA's, RCC's and PMG's do (the box closes round its plug), so Step 1's caution
says to disconnect it from the computer first. The arrows take the sizes of TechBox's published LSM take-apart, an arrow per stage
where a part comes off in stages (as Lee had the PMG's: see PUBLISHED below). An independent review (docs/research/lsm/decon/review/)
put the wording into TechBox's take-apart style and moved several arrows; what it left for Lee is in the kit's README (questions
20 - 25)."""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
from stepgen import Guide, _shifted, apply_pose, compose, via  # noqa: E402

# ---------------------------------------------------------------- parts (as guide.py names them: assemble.py's ids)
D1, D2, D3, D4, D5, D6, D7, D8, D10 = 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D10'
D9_A, D9_B = 'D9_A', 'D9_B'
D11S = ['D11_A', 'D11_B', 'D11_C', 'D11_D']
BREADBOARD, BACKING, NANO, R12K, R330, CAP, MATRIX = 'BREADBOARD', 'BACKING', 'NANO', 'R12K', 'R330', 'CAP', 'MATRIX'
BUTTON, NUT, RED_PIN, BLACK_PIN = 'BUTTON', 'NUT', 'BTN_RED_PIN', 'BTN_BLACK_PIN'
USB_B, USB_A = 'USB_B', 'USB_A'
PINS = ['J_WHITE_M', 'J_GREY_M', 'J_PURPLE_M']                      # the three wires' pins, in i2, i3 and b19 (the 'white' one is drawn
SOCKETS = ['J_WHITE_F', 'J_GREY_F', 'J_PURPLE_F']                   # and named yellow), and their sockets, on the matrix's V+, V- and IN
STEMS = [f'STEM_{k:02d}' for k in range(1, 65)]

# ---------------------------------------------------------------- the Full Build, as guide.py last wrote it
FULL = json.loads((HERE / 'steps.json').read_text(encoding='utf-8'))
VIEW = {v['name']: v for v in FULL['views']}
ROUTES = FULL['routes']


def shift_of(pose):
    """A pose that only moves (a shift): its [x, y, z]."""
    assert pose is None or isinstance(pose, list) or not pose.get('r'), pose
    return list(pose) if isinstance(pose, list) else (pose or {}).get('t', [0.0, 0.0, 0.0])


def camera_of(step, moved=None):
    """The camera of a Full Build step, for a step of ours that undoes it by hand (the generator reuses it by itself otherwise);
    moved: where the sub-assembly it showed is now, if it has slid since (a shift)."""
    c = VIEW[step]['camera']
    by = shift_of(moved)
    return dict(view_dir=c['dir'], frame=([round(a + b, 1) for a, b in zip(c['target'], by)], c['radius']))


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


def slid(pose, by):
    """A Full Build pose moved on by a shift (D2 slid out with the button on it): only t changes, and a via() stays a via()."""
    by = shift_of(by)
    if isinstance(pose, dict):
        return type(pose)(dict(pose, t=[round(a + b, 3) for a, b in zip(pose.get('t', [0.0, 0.0, 0.0]), by)]))
    return [round(a + b, 3) for a, b in zip(pose, by)]


def carried_back(step, part, prefix):
    """A Full Build step that moved `part` only by riding on the breadboard (Steps 26 and 30: the LED matrix, paced by D4's still
    way), walked back for lift(): its stops reversed, a beat each, its wires back through the Full Build's own shapes, a stage a beat."""
    done = VIEW[step + 'c']
    c = done['carry'][part]
    assert c['by'] == BREADBOARD, step                 # (in its seat: the poses of the ride are where the matrix is)
    stops = [VIEW[step]['carry'][part]['pose'], *(c.get('via') or []), c['pose']]
    pivot = [g._pivot(part)]                      # (and the part is where that step left it)
    assert np.allclose(apply_pose(where(part), pivot), apply_pose(c['pose'], pivot), atol=0.05), (step, where(part), c['pose'])
    stages = {w: [ROUTES[n] for n in nos[::-1]] for w, nos in done['wire_via'].items() if w.startswith(prefix + ' ')}
    assert all(len(r) + 1 == len(stops) - 1 for r in stages.values()), (step, len(stops), {w: len(r) for w, r in stages.items()})
    return dict(path=stops[::-1][1:], wire_via=stages, wires=leads(step, prefix))


g = Guide(HERE, title='Laser Stem Matrix (LSM)', part='Deconstruction', names=dict(FULL['names']), steps_file='steps-deconstruction.json',
          source='lsm.glb', hero_azimuth=45, copyright_line='© TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')
g.take_apart(parts_list_at_end=True,                               # (the Full Build's parts list, after the Completed View, as the MRA's)
             leave_out=[BACKING])                                   # (peeled off in the Full Build's Step 1 and never back)


def where(i):
    """Where a part is now (on what it rides, if it rides)."""
    if i in g.riding:
        by, rel = g.riding[i]
        return compose(where(by), rel, g._pivot(i))
    return g.resting.get(i)


def at_now(part, seated):
    """A spot given on a part in its seat, where the part is now (an arrow's tail on a part that has moved)."""
    return [round(float(x), 2) for x in apply_pose(where(part), [seated])[0]]


# ---------------------------------------------------------------- the arrows, as TechBox's published LSM take-apart has them
# (as the PMG's, Lee, 21 Oct 2026: "the arrow sizes and sequencing need refinement. Examine the Cadasio"): (length, shaft width) in mm,
# measured from its data (docs/research/lsm/decon/arrows/: published_arrows.txt, report.md); a part that comes off in stages shows an
# arrow for each, in turn (arrow_style then=): D10, D3, D4, and the matrix pulled off its wires' connectors.
# A stage the published guide has no arrow for takes the same part's size; shorter where the stage is short here: D10 drops 22 mm (the
# published D10 48), D4 slides 8 mm off its tabs before it lifts (the published D4 was pulled 75 mm straight out); and D10's slide,
# which the published guide has no arrow for, short and thin, so that it stops short of the wires hanging by it.
PUBLISHED = dict(stems=(69.4, 4.6), d8=(65.6, 3.2), d7=(59.3, 4.2), d11_a=(45.0, 3.9), d11_b=(41.7, 3.6), d11_c=(47.0, 4.0),
                 d11_d=(45.6, 3.4), d6=(70.6, 3.8), matrix=(70.6, 3.8), d10=(50.8, 4.4), d10_slide=(20.0, 2.5), d10_drop=(30.0, 4.4), d4_slide=(30.0, 6.2), d9_a=(61.2, 3.4),
                 d9_b=(69.2, 3.4), d5=(62.8, 7.1), d3=(50.7, 3.5), d4=(80.1, 6.2), d2=(86.5, 3.9), usb=(63.3, 5.0), nut=(56.3, 5.0),
                 button=(38.4, 3.7), cable=(31.6, 3.5), r330=(32.0, 2.3), cap=(21.2, 2.1), r12k=(31.5, 1.3), nano=(40.5, 2.9))
size = lambda key, **more: dict(dims=PUBLISHED[key], **more)


# ================================================================ FROM THE TOP: THE STEMS, THE SHELVES AND THEIR POSTS
POWER = 'Disconnect the USB Cable from the computer or power supply before you begin.'
g.remove('Remove all 64 LED Stems from D8, D7, and D6.', STEMS, units=[STEMS], arrow_style={STEMS[0]: size('stems')},   # (in one step: Lee;
         caution=POWER,                                             #  one arrow, on the stem nearest their middle)
         view_dir=VIEW['Step 40']['camera']['dir'], frame=([638.5, 950.0, 1204.5], 100.0))   # (the Full Build's Step 40's, a little higher
                                                                    # and wider: the published arrow's length above the stems)
g.remove('Remove D8 from the latches of the four D11 posts.', [D8], arrow_style={D8: size('d8')})
g.remove('Remove D7 from the four D11 posts.', [D7], arrow_style={D7: size('d7')})
# All four posts at once (Lee's groups): their tabs pushed back up out of D1 (the Full Build's Step 36), then up out of D6's corner
# slots (34, 35); an arrow on each; the close-up of a tab through D1 from below, the Full Build's Step 36c's, with a red box on it.
D11_SHORT, D11_UP = VIEW['Step 34c']['carry'][D11S[0]]['pose'], VIEW['Step 34']['carry'][D11S[0]]['pose']   # (the tabs at D1's top; up)
TAB = VIEW['Step 36c']['inset']
g.remove('Lift the box and push the tabs of the four D11 posts up out of the slots in D1 from underneath. Then, remove the posts from '
         'D6.', D11S, paths={i: [D11_SHORT, D11_UP] for i in D11S}, keep_camera=True,   # (D7's camera: D6's, next, is nearly the same)
         arrow_style={i: size('d11_' + i[-1].lower()) for i in D11S},   # (each as the published post at its corner)
         inset=dict(target=TAB['target'], dir=TAB['dir'], radius=TAB['radius'], mark=2.5,
                    caption='Push each tab up out of D1', alt=TAB['alt']))
g.remove('Remove D6 from the tabs of D2, D3, D4, and D5.', [D6], arrow_style={D6: size('d6')})

# ================================================================ THE LED MATRIX OUT OF THE BOX, STILL WIRED
g.lift('Lift the LED Matrix, with D10 hooked under it, up out of the box and hold it over the box. Leave its wires connected.', [MATRIX],
       wire_via={w: [ROUTES[n] for n in nos[::-1]] for w, nos in VIEW['Step 32c']['wire_via'].items()},   # (the Full Build's Step 32 reversed:
       wires=leads('Step 32', 'wire'), arrow_style={MATRIX: size('matrix')})   # its wires through the half-way shape to the held one)
g.remove('Slide D10 toward D2 until its hooks come off the edges of the LED Matrix, then remove it from under the matrix.', [D10],
         path=[compose(where(MATRIX), VIEW['Step 31c']['carry'][D10]['via'][0], g._pivot(D10)),   # (along 40 mm: unhooked)
               compose(where(MATRIX), VIEW['Step 31']['carry'][D10]['pose'], g._pivot(D10))],     # (then down 22, from under the matrix)
         arrow_style={D10: size('d10_slide', stage=0, at=at_now(D10, [599.5, 886.0, 1207.0]),   # (at D10's D4 end, outside the matrix,
                          then=[size('d10_drop', stage=1, at=[620.0, 915.0, 1241.5])])},   # short of the wires; then the drop, in front of D10)
         **camera_of('Step 31'))
g.lift('Carry the LED Matrix over D4 and set it down outside the box, LEDs up. Leave its wires connected.', [MATRIX],
       **carried_back('Step 30', MATRIX, 'wire'), arrow_style={MATRIX: size('matrix', stage=0)},   # (the carry over D4: one arrow, as a
       **camera_of('Step 30'))                                      #  carry with its wires' stages cannot take arrows in turn)
g.remove('Remove both D9 pieces from the slots in D2 and D3.', [D9_A, D9_B],
         arrow_style={D9_A: size('d9_a', at=[618.6, 902.7, 1190.0]), D9_B: size('d9_b')})   # (D9_A's left of the USB plug, not rising from it)

# ================================================================ THE WALLS (the box turned over, as the Full Build put D3 and D5 on)
g.remove('Turn the box over with the LED Matrix, keeping its wires connected. Then, remove D5 from the tabs of D1, D2, and D3.', [D5],
         arrow_style={D5: size('d5')})
g.remove('Swing D3 open, away from D1, then unhook its tabs from the slots in D4.', [D3],
         arrow_style={D3: size('d3', stage=0, then=[size('d3', stage=1)])})   # (the swing, then the slide)
# The matrix's wires lie over D4's top edge: carried back over D4, turning round, to beside the box at the D5 end (the Full Build's Step
# 26 walked back, by its camera, with its own arrow, the other way, and its eye on the matrix).
g.lift('Turn the box the right way up. Carry the LED Matrix back over D4, turning it around, and set it down beside the box, at the '
       'end where D5 was. Leave its wires connected.', [MATRIX], **carried_back('Step 26', MATRIX, 'wire'), eye=[MATRIX],
       arrows=[dict(tail=[585.0, 862.4, 1133.0], head=[655.6, 862.4, 1133.0], normal=[0.0, 1.0, 0.0], part=D1, width=3.8)],   # (the matrix's size)
       **camera_of('Step 26'))
g.remove('Slide D4 off the tabs of D1 and D2, then lift it off the USB Cable.', [D4], path=full_way_back('Step 25', D4),
         arrow_style={D4: size('d4_slide', stage=0, then=[size('d4', stage=1, at=[587.9, 909.0, 1245.0])])},   # (the slide off the tabs;
                                                                    # then the lift, from D4's D2 end, clear of the button)
         **camera_of('Step 25'))                                    # (the Full Build's Step 25 reversed: its later records only stand still)

# ================================================================ D2, THE PUSH BUTTON AND THE USB CABLE
g.lift("Slide D2, with the Push Button, out of the slots in D1. Leave the Push Button's wires connected.", [D2],
       wires=leads('Step 24', 'lead'),                              # (the Full Build's Step 24 reversed: the leads as they lay before it)
       arrow_style={D2: size('d2', at=[638.2, 912.0, 1256.0])})     # (above D2's top edge, just past its outer face, turned from the camera)
g.remove('Disconnect the USB Cable from the Nano Board.', [USB_B, USB_A], units=[[USB_B]], arrow_style={USB_B: size('usb')},   # (one arrow,
         paths={USB_A: [[0.0, 0.0, 25.0]]})                         # on the plug; the A end moves with it: the cable goes whole)
PULL = 'Pull each wire out by its connector. Do not pull on the wires themselves.'
g.unplug("Disconnect the Push Button's red wire from j5 and its black wire from j16.", [RED_PIN, BLACK_PIN], caution=PULL,
         **camera_of('Step 21'))                                    # (both at once; the Full Build's Step 21 holds both holes)
# The button on its own (the rest hidden), one camera for the two steps: the Full Build's Step 20's, moved with D2.
D2_AT = where(D2)                                                   # (as the lift left it: 57.1 mm out)
NUT_WAY = [slid(p, D2_AT) for p in full_way_back('Step 20', NUT)]  # (the Full Build's eight quarter turns, reversed: unscrewing)
NUT_WAY[3] = dict(NUT_WAY[3])                                       # (a stop after the first whole turn: a beat a turn, where the Full Build
NUT_WAY.append(slid([0.0, 0.0, -95.0], D2_AT))                      #  played both in one; then off over the wires, past their pins' ends)
BUTTON_SET = [D2, BUTTON, NUT, RED_PIN, BLACK_PIN]
g.remove('Unscrew the nut from the Push Button, on the inside of D2. Then, slide it off over the wires.', [NUT], path=NUT_WAY,
         alone=BUTTON_SET, arrow_style={NUT: size('nut', at=at_now(NUT, [624.2, 895.8, 1250.3]))},   # (from the nut's rear face, 20 mm off
         **camera_of('Step 20', moved=D2_AT))                       #  its axis across the view: on the axis it lay over the button and wires)
g.remove('Push the Push Button out through the hole in D2, pulling its wires through after it.', [BUTTON],
         path=[slid(p, D2_AT) for p in full_way_back('Step 19', BUTTON)], alone=[D2, BUTTON, RED_PIN, BLACK_PIN], keep_camera=True,
         arrow_style={BUTTON: size('button', at=at_now(BUTTON, [649.23, 882.63, 1219.0]))})   # (beside the button's body, inside D2)
g.put_away([D2])                                                    # (what is left of the sub-assembly taken apart on its own)

# ================================================================ THE LED MATRIX OFF ITS WIRES, THE WIRES, THE BREADBOARD'S PARTS
# The matrix pulled back along its pins off the three connectors, which stay where they lie (let_go, as the PMG's displays), then
# lifted away; a close-up of the connectors, which are under the matrix, with the matrix drawn faintly (as the Full Build's Step 32c).
# Seen from the D4 / D2 corner, closer than the Full Build's camera for this scene (its Step 23's): the breadboard in front, the
# matrix to its right, the pull to the right.
OFF = compose(where(MATRIX), [0.0, 0.0, -15.0], g._pivot(MATRIX))  # (15 mm back along its pins, as the Full Build held the sockets off them)
ENDS = np.mean([apply_pose(where(s), [g._pivot(s)])[0] for s in SOCKETS], axis=0)   # (the three connectors, under the matrix's corner)
WIRES_CAMERA = dict(view_dir=[-0.5792, 0.5736, 0.5792], frame=([684.0, 870.0, 1214.0], 82.0))
g.remove('Disconnect the LED Matrix from the yellow, grey, and purple breadboard wires.', [MATRIX], let_go=SOCKETS,
         path=[OFF, _shifted(OFF, [0.0, 30.0, 0.0])],
         arrow_style={MATRIX: size('cable', stage=0, at=(ENDS + [0.0, 4.0, 15.0]).round(2).tolist(),   # (the pull off the pins, from the
                                   then=[size('cable', stage=1)])},   # board's edge by them, as the published cable's; then the lift)
         caution='Hold the three black connectors while you pull the LED Matrix off its pins. Do not pull on the wires themselves.',
         inset=dict(target=ENDS.round(2).tolist(), dir=[-0.3, 0.8, 0.52], radius=10.0, mark=5.0, ghost={MATRIX: 0.15},
                    caption='The three connectors',
                    alt="Close-up of the three wires' connectors on the pins under the corner of the LED Matrix, the matrix drawn faintly"),
         **WIRES_CAMERA)
g.remove('Disconnect the yellow, grey, and purple breadboard wires from i2, i3, and b19.', PINS + SOCKETS,   # (together: Lee; both ends of each, so the
         paths={s: [_shifted(where(s), [0.0, 30.0, 0.0])] for s in SOCKETS}, arrows=[],   # wires go up whole, as their pins came down)
         eye=['J_GREY_M', 'J_PURPLE_M'], caution=PULL, keep_camera=True)   # (an eye on i2 / i3 and one on b19)
g.remove('Remove the 330 Ω Resistor from a11 and a19.', [R330], arrow_style={R330: size('r330')})
g.remove('Remove the Capacitor from j2 and j3.', [CAP], arrow_style={CAP: size('cap')})
g.remove('Remove the 12 kΩ Resistor from h3 and h16.', [R12K], arrow_style={R12K: size('r12k')})
g.remove('Remove the Nano Board from the breadboard.', [NANO], arrow_style={NANO: size('nano')})

g.build()
