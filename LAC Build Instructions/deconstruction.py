"""LCD Alarm Clock (LAC), deconstruction: the finished clock taken apart, down to F3 with the breadboard stuck on it. A guide of its
own (steps-deconstruction.json), made from the Full Build as guide.py last wrote it (run that first, and this again after any change
to it). It opens on the Full Build's title page, ends on what is left, F3 and the breadboard (as TechBox's published take-apart ends:
the breadboard is stuck on for good), followed by the Full Build's parts list (as the MRA's, PMG's and LSM's); its card on the website
is the Full Build's.

First draft (Lee, 21 Oct 2026: "we need to make a deconstruction guide for this LAC as well. Here is the published version of the
guide that we need to convert / remake here: https://instructions.online/?id=19075-lac_deconstruction"): TechBox's published LAC
take-apart (docs/research/guide_19075-lac_deconstruction.md, 47 steps) remade on our Full Build, within the in-house principles
(rulebook section 11): one wire per step, as published; every step a caption of its own; each arrow the size of the published one (an
arrow per stage, in turn, for F9; see the arrows below); nothing put back on (the published Steps 16 - 18 refit the washer, nut and knob
for storage: left out). The plan and its reasons: docs/research/lac/decon/plan.md; an independent review of the first draft (three
reviewers, each finding checked by a fourth): docs/research/lac/decon/review/.
  1. the case: F6, F2 (the USB cable walked back out of its slit), F5; then the USB cable, as soon as its plug can come out (Step 1's
     caution says to disconnect it from the computer first: the closed case holds the plug, as the LSM's box does);
  2. F1 pulled forward and laid aside, still wired; the LCD screen out of F9's notches, then out of the case to lie face down, still
     wired (two steps, as the Full Build brought it in); F8; F4 lifted off with the rocker switch and moved out behind the case, still
     wired;
  3. the Full Build's Steps 47 - 41 reversed: F1 moved in front of the breadboard's end, F9 tipped and lifted out, the F7s spread, the
     alarm buzzer lifted out to lie beside the base, still wired, the F7s out;
  4. each wired part, as the Full Build wired them, reversed: the LCD's four wires and the LCD; the buzzer's two leads and the buzzer;
     the potentiometer's three leads, F1 picked up and held upright, the potentiometer taken apart on its own (knob, nut, washer, out of
     F1); the yellow and orange jumper wires; the switch's three leads and the switch out of F4, on its own; the other six jumper wires;
  5. the real time clock module, each 12 kOhm resistor, the Nano Board.
Where it leaves the published order, our model made it: in the published order the potentiometer's and the LCD's leads pass through the
seated buzzer's black lead, and the purple, blue and green jumper wires through the orange one. Every lead keeps a shape the Full Build
drew: each route is one of the Full Build's. The steps walk the Full Build back, with two kinds of exception: the USB cable comes out at
Step 4 (power first), though the Full Build plugged it in at its Step 40, so Steps 4 - 15 take the case apart with the cable already
gone; and, one wire a step, the published order is kept where it clears rather than the Full Build's reversed (the LCD's wires GND
first, the buzzer's red lead first, white before dark red and purple before blue, the h27 resistor first)."""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
from stepgen import Guide, _shifted, apply_pose, compose, via  # noqa: E402

# ---------------------------------------------------------------- parts (as guide.py names them: the CAD's instance ids. Never import
# guide.py: it builds the Full Build as it is imported, rewriting steps.json and parts.json)
BREADBOARD, F3, RTC, COIN, RES1, RES2 = 'NAUO1', 'NAUO2', 'NAUO3', 'NAUO4', 'NAUO6', 'NAUO7'
F1, POT, NUT, KNOB, WASHER = 'NAUO10', 'NAUO11', 'NAUO12', 'NAUO13', 'NAUO146'
F7A, F7B, F8, F9 = 'NAUO42', 'NAUO43', 'NAUO44', 'NAUO45'           # F7A at the back (-x), F7B in front
F4, F5, F2, F6 = 'F4', 'F5', 'F2', 'F6'                             # (materials.json "extra_parts")
SWITCH, BUZZER, LCD, USB_B, PAPER = 'NAUO46', 'NAUO62', 'NAUO94', 'NAUO122', 'NAUO141'
NANO, USB_A = 'NANO', 'USB_A'
JUMPERS = {'black': ('NAUO16', 'NAUO17'), 'green': ('NAUO20', 'NAUO19'), 'purple': ('NAUO25', 'NAUO26'), 'blue': ('NAUO22', 'NAUO21'),
           'white': ('NAUO28', 'NAUO15'), 'dark_red': ('NAUO30', 'NAUO31'), 'orange': ('NAUO53', 'NAUO52'), 'yellow': ('NAUO56', 'NAUO55')}
SWITCH_CAPS = {'red': 'NAUO47', 'tan': 'NAUO49', 'black': 'NAUO48'}   # (leads 'switch <colour>': a = SWITCH, b = the cap)
POT_CAPS = {'red': 'NAUO34', 'tan': 'NAUO33', 'black': 'NAUO14'}      # (leads 'pot <colour>': a = the cap, b = POT)
BUZZER_CAPS = {'red': 'NAUO58', 'black': 'NAUO59'}                    # (leads 'buzzer <colour>': a = the cap, b = BUZZER)
LCD_WIRES = {'purple': ('NAUO82', 'NAUO97', 'Step 36'), 'yellow': ('NAUO84', 'NAUO98', 'Step 37'),   # (male cap in the breadboard,
             'teal': ('NAUO86', 'NAUO99', 'Step 38'), 'blue': ('NAUO93', 'NAUO100', 'Step 39')}       #  female cap on the LCD's pin,
ZERO = [0.0, 0.0, 0.0]                                                                               #  the Full Build step that plugged it)

# ---------------------------------------------------------------- the Full Build, as guide.py last wrote it
FULL = json.loads((HERE / 'steps.json').read_text(encoding='utf-8'))
VIEW = {v['name']: v for v in FULL['views']}
ROUTES = FULL['routes']


def camera_of(step, target=None, radius=None):
    """A Full Build step's camera, for a step of ours whose way is by hand (the generator reuses it by itself otherwise); target,
    radius: the same direction, framed afresh."""
    c = VIEW[step]['camera']
    return dict(view_dir=c['dir'], frame=(target or c['target'], radius or c['radius']))


def leads(step, prefix):
    """The routes of a set of leads in a Full Build view: {wire: route}."""
    return {w: ROUTES[n] for w, n in VIEW[step]['wires'].items() if w.startswith(prefix + ' ')}


def stages_back(step, prefix):
    """A Full Build step's in-between lead shapes (its done view's wire_via), walked back: {wire: [route, ...]}."""
    return {w: [ROUTES[n] for n in nos[::-1]] for w, nos in (VIEW[step + 'c'].get('wire_via') or {}).items() if w.startswith(prefix + ' ')}


def ride_back(step, part):
    """A Full Build ride of `part` on F3 (ride=; F3 is in its seat, so the poses are where the part is), walked back: its stops
    between, reversed, then where it rode as the step opened. A stop each."""
    c = VIEW[step + 'c']['carry'][part]
    assert c['by'] == F3, (step, part, c['by'])
    return [*(c.get('via') or [])[::-1], VIEW[step]['carry'][part]['pose']]


def shift_of(pose):
    """A pose that only moves (a shift): its [x, y, z]."""
    assert pose is None or isinstance(pose, list) or not pose.get('r'), pose
    return list(pose) if isinstance(pose, list) else (pose or {}).get('t', ZERO)


def slid(pose, by):
    """A ride pose moved on by a shift (where its carrier is now): only t changes, so that the Nut's turns past 360 degrees stay as
    written, and a via() stays a via() (compose() would make a matrix of them: the LSM's slid())."""
    if isinstance(pose, dict):
        return type(pose)(dict(pose, t=[round(a + b, 3) for a, b in zip(pose.get('t', ZERO), by)]))
    return [round(a + b, 3) for a, b in zip(pose, by)]


def same_pose(a, b):
    """Two poses alike to 0.05 mm (a part where a Full Build view had it)."""
    pts = np.array([[0, 0, 0], [100, 0, 0], [0, 100, 0], [0, 0, 100]], float) + 600.0
    return np.allclose(apply_pose(a, pts), apply_pose(b, pts), atol=0.05)


g = Guide(HERE, title='LCD Alarm Clock (LAC)', part='Deconstruction', names=dict(FULL['names']), steps_file='steps-deconstruction.json',
          source='lac-guide.glb', hero_azimuth=135,                 # (the Full Build's: Guide's defaults are mra.glb and 225)
          copyright_line='© TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')
g.take_apart(parts_list_at_end=True,                                # (the Full Build's parts list, after the Completed View)
             leave_out=[PAPER])                                     # (the breadboard's backing, peeled off in the Full Build's Step 1)


def where(i):
    """Where a part is now (on what it rides, if it rides)."""
    if i in g.riding:
        by, rel = g.riding[i]
        return compose(where(by), rel, g._pivot(i))
    return g.resting.get(i)


def to_hanging(caps, prefix, plugged, hanging, part):
    """The Full Build's steps that plugged a part's leads in (each cap pushed in from held over its hole: `plugged`, by colour), walked
    back on to where each cap hung from `part` in the Full Build view before them (`hanging`): out of its hole (a beat), then down to
    hang (a beat), its lead through the plugged shape (carried up with its cap) to the hanging one. For unplug(): paths, wire_via,
    wires, ride_on. (The generator's own unplug() only lifts each cap over its hole, its lead in its plugged shape: the published and the
    Full Build have them hanging from their part.)"""
    paths, stages, last = {}, {}, {}
    for colour, cap in caps.items():
        w, step = f'{prefix} {colour}', plugged[colour]
        c = VIEW[hanging]['carry'][cap]
        assert c['by'] == part and VIEW[step]['moving'] == [cap], (cap, c, step)
        paths[cap] = [VIEW[step]['path'][0], compose(where(part), c['pose'], g._pivot(cap))]   # ([0, 18, 0] up; the black ones [0, 5, 0])
        stages[w] = [ROUTES[VIEW[step]['wires'][w]]]
        last[w] = ROUTES[VIEW[hanging]['wires'][w]]
    return dict(paths=paths, wire_via=stages, wires=last, ride_on=part)


# ---------------------------------------------------------------- the arrows, as TechBox's published LAC take-apart has them
# (as the PMG's and LSM's, Lee, 21 Oct 2026: "Examine the Cadasio"): (length, shaft width) in mm, measured from its data
# (docs/research/lac/decon/published_geometry.md section 3); an arrow per stage, in turn, for F9 (Step 12: the tip, then the lift). One
# arrow on one stage where a lead changes shape on the way (then= is refused with wire_via=): F2 on the pull away (Step 2), F4 on the
# lift (Step 10), the buzzer on the lift out (Step 14). The F7s: two arrows for the spread (Step 13), the up arrows only for the close
# and pull out (Step 15, as published). The F7s' up arrows: F7A's (at the back) 34.2 mm, F7B's 37.3 (by their tails: x 640 is F7A,
# x 711 F7B).
PUBLISHED = dict(f6=(56.1, 4.87), f2=(79.8, 5.51), f5=(64.6, 6.19), usb=(63.5, 5.78), f1=(79.0, 5.78), f8=(83.9, 4.51),
                 f4=(73.2, 3.35), f9=(33.8, 3.3), f7a_spread=(36.9, 3.75), f7b_spread=(40.5, 3.8), buzzer=(58.3, 6.15),
                 f7a_up=(34.2, 3.96), f7b_up=(37.3, 3.96), knob=(41.2, 2.93), nut=(56.5, 3.72), washer=(70.6, 2.89),
                 pot=(52.7, 4.21), switch=(63.6, 4.95), rtc=(29.8, 3.55), res1=(39.4, 3.47), res2=(46.8, 3.96), nano=(64.2, 3.72))
size = lambda key, **more: dict(dims=PUBLISHED[key], **more)
POWER = 'Unplug the USB cable from the computer or power supply before you begin.'
PULL = 'Pull the wire out by its connector. Do not pull on the wire itself.'
PIN = 'Hold the black connectors to pull the wire off the pin and out of the breadboard. Do not pull on the wire itself.'


# ================================================================ THE CASE (the Full Build's Steps 57 - 55 reversed: the published 1 - 3)
g.remove('Pull F6 off the end of the case nearest the knob.', [F6], arrow_style={F6: size('f6')}, caution=POWER)
g.remove('Turn the case so its back faces you. Swing the end of F2 where F6 was out from the case, then slide F2 along to unhook it '
         'from F5 and pull it away, clear of the USB cable.', [F2],
         wire_via={'usb cable': [ROUTES[n] for n in VIEW['Step 56c']['wire_via']['usb cable'][::-1]]},   # (walked back out of the slit,
         wires={'usb cable': ROUTES[VIEW['Step 56']['wires']['usb cable']]},                              #  a stage a beat)
         arrow_style={F2: size('f2', stage=2, at=[645.22, 958.23, 1255.0])},   # (on the pull away: then= is refused with wire_via=;
                                                                    #  on F2's top edge, as published, its head short of the slit)
         eye=[dict(e) for e in VIEW['Step 56']['eye']])             # (the Full Build's eye on the slit, where the cable passes: as published)
g.remove('Pull F5 off the other end of the case.', [F5], arrow_style={F5: size('f5', at=[683.78, 881.40, 1371.07])})   # (at its lower
                                                                    # edge, as published: clear of its engraved code)

# ================================================================ POWER (as soon as the plug can come out: the published 25, moved up)
g.remove("Unplug the USB cable's small end from the Nano Board's USB socket.", [USB_B, USB_A], units=[[USB_B]], arrow_style={USB_B: size('usb')},
         paths={USB_A: [_shifted(where(USB_A), [0.0, 30.0, 0.0])]},   # (its far end lifted off the table with it: the cable goes whole)
         **camera_of('Step 40', target=[628.0, 900.0, 1365.0], radius=65.0))   # (the Full Build's Step 40, wider: plug, arrow, A end)

# ================================================================ F1, THE LCD SCREEN, F8, F4 (the Full Build's Steps 54 - 48 reversed: the published 4 - 8)
g.lift("Pull F1 forward off the tabs of F3 and F4. Leave the potentiometer's wires connected.", [F1, POT],
       wires=leads('Step 54', 'pot'), arrow_style={F1: size('f1')})   # (Step 54 reversed, by its camera; POT rides on F1 from now on)
g.lift('Lay F1 face down in front of the case, out of the way of the LCD screen.', [F1], path=[VIEW['Step 53']['carry'][F1]['pose']],
       wires=leads('Step 53', 'pot'), arrows=[], eye=[dict(id=F1, side='up-right', reach=0.035)],   # (an eye, as published Step 5)
       **camera_of('Step 47', target=[795.0, 945.0, 1316.0], radius=130.0))   # (the Full Build's view of F1 laid aside, closer: Step
                                                                    #  54's leaves it out)
NOTCHES = VIEW['Step 52c']['inset']
g.lift('Slide the LCD screen towards F8 until its board comes out of the notches in F9, then swing its free end out from the case. '
       'Leave its wires connected.', [LCD], wires=leads('Step 52', 'lcd'), wire_via=stages_back('Step 52', 'lcd'),
       arrows=[], eye=[dict(id=LCD, anchor=[713.76, 895.78, 1358.05], side='near-below', reach=0.05)],   # (published Step 6: an eye
                                                                    #  on its F9 end; below it, so that its leader and the close-up's do not cross)
       inset=dict(target=NOTCHES['target'], dir=NOTCHES['dir'], radius=NOTCHES['radius'], alt=NOTCHES['alt'],
                  marks=[(m['at'], m['half']) for m in NOTCHES['marks']]))   # (Step 52c's close-up; steps.json writes marks as dicts)
g.lift('Slide the LCD screen out of the slots in F8, bring it out through the front of the case, and lay it face down beside the '
       'case. Leave its wires connected.', [LCD], path=ride_back('Step 51', LCD), wire_via=stages_back('Step 51', 'lcd'),
       wires=leads('Step 51', 'lcd'), arrows=[], eye=[dict(id=LCD, side='up-left', reach=0.05)], **camera_of('Step 51'))
g.remove('Slide F8 out of the slots in F3 and F4, towards the front.', [F8], arrow_style={F8: size('f8', shift=[0.0, -18.0, 0.0])})   # (on
                                                                    # F8's lower half: higher, from Lee's camera, it lay on the potentiometer's leads)
g.lift("Lift F4, with the rocker switch, off the tabs of the F7s and F9, and move it out behind the case. Leave the switch's wires "
       'connected.', [F4], path=[VIEW['Step 49']['path'][0], VIEW['Step 48']['carry'][F4]['pose']],   # (up over the frame, then back
       wire_via={w: [r] for w, r in leads('Step 49', 'switch').items()},   # behind the case, at the Full Build's raised pose: Steps 49 and
                                                                           # 48, a beat each; the leads over
       wires=leads('Step 48', 'switch'),                                   # the frame, then as they lay before Step 48)
       arrow_style={F4: size('f4', stage=0)}, **camera_of('Step 49'))

# ================================================================ THE FULL BUILD'S STEPS 47 - 41 REVERSED (the published 24, 26 - 28)
g.lift('Move F1, still face down, nearer the case and along towards the end where F5 was, in front of the end of the breadboard.', [F1],
       path=[VIEW['Step 47']['carry'][F1]['pose']], wires=leads('Step 47', 'pot'), arrows=[], eye=[dict(id=F1, side='right')],
       **camera_of('Step 47'))
HOOKED = VIEW['Step 46']['carry'][F9]['pose']                      # (tipped forward about its front edge: its back foot up out of F3)
TIPPED = VIEW['Step 45c']['carry'][F9]['via']                     # (the same tilt, 33 mm higher: its front foot up out of its slot)
assert len(TIPPED) == 1, TIPPED                                    # (Step 45 as of 61c6efc: look again if its way changes)
FOOT = VIEW['Step 45c']['inset']
g.remove('Tip the top of F9 towards the front to lift its back foot out of F3. Keeping it tipped, lift F9 straight up to unhook its '
         'front foot from its slot in F3.', [F9], path=[HOOKED, *TIPPED],
         arrow_style={F9: size('f9', stage=0, at=[698.0, 956.0, 1359.5], then=[size('f9', stage=1)])},   # (the tip, over F9's top;
                                                                    #  then the lift)
         inset=dict(target=FOOT['target'], dir=FOOT['dir'], radius=FOOT['radius'], mark=FOOT['mark'], ghost=FOOT['ghost'],
                    alt=FOOT['alt']),                              # (Step 45c's close-up: the front foot's barb under F3, F3 faint)
         **camera_of('Step 46'))
g.lift('Gently pull the tops of the two F7s apart to free the alarm buzzer.', [F7A, F7B], ride_on=F3,   # (ride_on: else F7B rides on F7A)
       paths={i: [VIEW['Step 42c']['carry'][i]['pose']] for i in (F7A, F7B)},   # (15 degrees each way about its outer bottom edge)
       arrows=[dict(tail=[660.7, 920.0, 1219.5], head=[623.8, 920.0, 1219.5], normal=[0.0, 0.658, -0.753], part=F3, width=3.75),
               dict(tail=[691.8, 920.0, 1219.5], head=[732.3, 920.0, 1219.5], normal=[0.0, 0.658, -0.753], part=F3, width=3.8)],
       **camera_of('Step 44'))                                      # (outward at mid-height, as published, on the camera's side of the
                                                                    # planks, facing it: over the tops they lay under F4, held up behind)
g.lift("Lift the alarm buzzer out from between the two F7s, carry it over the breadboard, and lay it beside the base past the Nano "
       "Board's end. Leave its wires connected.", [BUZZER], wires=leads('Step 43', 'buzzer'), wire_via=stages_back('Step 43', 'buzzer'),   # (Step 43 reversed,
       arrow_style={BUZZER: size('buzzer', stage=0)},              # by its camera: up 75, over the board, down: a beat each; the arrow
       eye=[dict(id=BUZZER, anchor=[676.1, 934.26, 1226.81], side='near-right', reach=0.07)])   # on the lift out; an eye, as published,
                                                                    # beside the F7s, clear of the arrow)
UP = VIEW['Step 41']['carry'][F7A]['pose']                         # ([0, 80, 0]: where the Full Build held them over their slots)
g.remove('Let the two F7s close, then pull them up out of their slots in F3.', [F7A, F7B], paths={i: [ZERO, UP] for i in (F7A, F7B)},
         arrow_style={F7A: size('f7a_up', stage=1), F7B: size('f7b_up', stage=1, at=[709.9, 958.2, 1233.2])},   # (the up arrows only, as
         **camera_of('Step 41'))                                    # published: inward ones for the close were too short to read, 14 mm
                                                                    # in a 30 mm gap; F7B's on its spread top, as published; F7A's where
                                                                    # it will be once closed: over its spread top it would pass through F4)

# ================================================================ THE LCD SCREEN AND THE ALARM BUZZER OFF THEIR WIRES (the Full Build's 39 - 33 reversed: the published 19 - 23, 29 - 31)
# One wire per step, as published (GND first: in that order each clears the ones still in; SCL first passes through purple, yellow and
# teal). The Full Build's GND / VCC / SDA / SCL labels of Steps 36 - 39, on the LCD's pins (the published guide's only text); an eye on
# the breadboard end (published: the label on the LCD end, the eye on the breadboard end); each female cap 15 mm back off its pin
# ([0, 0, 15] on the LCD, where the Full Build held it before pushing it on), each male cap up its Full Build way.
PIN_LABELS = {colour: next(dict(l) for l in VIEW[step]['labels'] if l['id'] == LCD) for colour, (_, _, step) in LCD_WIRES.items()}
OFF_PIN = {fem: compose(where(LCD), VIEW[step]['carry'][fem]['pose'], g._pivot(fem)) for _, fem, step in LCD_WIRES.values()}
HOLE = {'purple': '(-) blue', 'yellow': '(+) red', 'teal': 'b8', 'blue': 'b9'}
for k, (colour, (male, fem, step)) in enumerate(LCD_WIRES.items()):
    g.remove(f"Disconnect the {colour} wire from {PIN_LABELS[colour]['text']} on the LCD screen and from {HOLE[colour]}.", [male, fem],
             paths={fem: [OFF_PIN[fem]]}, arrows=[], eye=[dict(id=male, side='up-right', reach=0.06)] if k < 2 else [male],
             labels=[PIN_LABELS[colour]],
             **(dict(caution=PIN) if k == 0 else dict(keep_camera=True)))   # (Step 36's camera, kept for the four: the published held one)
g.remove('Remove the LCD screen.', [LCD], path=[_shifted(where(LCD), [0.0, 30.0, 0.0])], arrows=[], eye=[LCD],   # (published: an eye,
         **camera_of('Step 35'))                                   # a fade where it lies; in-house a removal slides, then fades)
g.unplug("Disconnect the buzzer's red wire from j4.", [BUZZER_CAPS['red']], ride_on=BUZZER, caution=PULL,   # (the published 29, 30:
         **camera_of('Step 33', radius=54.0))                      # red, then black; the Full Build's camera, a little wider: the freed lead
g.unplug("Disconnect the buzzer's black wire from (-) blue.", [BUZZER_CAPS['black']], keep_camera=True)   # ran to the frame's edge;
                                                                    # ride_on: the red cap rode on nothing before the Full Build's Step 33)
g.remove('Remove the alarm buzzer.', [BUZZER], path=[_shifted(where(BUZZER), [0.0, 30.0, 0.0])], arrows=[], eye=[BUZZER], keep_camera=True)

# ================================================================ THE POTENTIOMETER (the Full Build's Steps 32 - 25 reversed: the published 9 - 15)
assert same_pose(where(F1), VIEW['Step 47']['carry'][F1]['pose'])  # (face down in front of the breadboard's end, as when it was wired)
for k, (colour, hole, step) in enumerate((('black', '(-) blue', 'Step 32'), ('tan', 'a5', 'Step 31'), ('red', '(+) red', 'Step 30'))):
    g.unplug(f"Disconnect the potentiometer's {colour} wire from {hole}.", [POT_CAPS[colour]],   # (the published 9 - 11: black, tan, red)
             **to_hanging({colour: POT_CAPS[colour]}, 'pot', {colour: step}, 'Step 29c', POT),
             **(dict(camera_of('Step 30', target=[744.0, 910.0, 1335.0], radius=60.0), caution=PULL) if k == 0 else dict(keep_camera=True)))
BUILD = VIEW['Step 29']['carry'][F1]['pose']                       # ([100, 35, 100]: F1 held up, as the Full Build fitted the Potentiometer)
g.lift('Pick up F1 with the potentiometer and hold it upright, the knob facing out.', [F1], path=[BUILD], wires=leads('Step 29', 'pot'),
       arrows=[], eye=[dict(id=F1, side='down-right', reach=0.065)], **camera_of('Step 29'))   # (Step 29 reversed: the leads hang with it)
POT_AT = shift_of(where(POT))                                      # (= BUILD: the Potentiometer rides on F1, in its seat on it)
assert np.allclose(POT_AT, shift_of(BUILD), atol=0.05), POT_AT
F1_SET = [F1, POT, KNOB, NUT, WASHER]                              # (F1 on its own; the three leads' caps ride on the Potentiometer)
g.remove("Pull the knob straight off the end of the potentiometer's shaft.", [KNOB], alone=F1_SET,
         paths={KNOB: [slid(VIEW['Step 28']['carry'][KNOB]['pose'], POT_AT)]},   # (60 mm along the shaft: where the Full Build held it)
         arrow_style={KNOB: size('knob')},                          # (the published view of its knob, nut and washer (frame 031), in F1's
         view_dir=[0.6112, 0.5658, -0.5535], frame=([799.9, 907.0, 1389.3], 98.2))   # seated frame, moved with F1: the nut and washer face on)
nut = VIEW['Step 27c']['carry'][NUT]
NUT_WAY = [slid(p, POT_AT) for p in [*nut['via'][::-1], VIEW['Step 27']['carry'][NUT]['pose']]]   # (the seven quarter turns back, then off)
NUT_WAY = [p if k in (3, len(NUT_WAY) - 1) else via(p) for k, p in enumerate(NUT_WAY)]          # (two beats: a stop after the first turn)
g.remove('Unscrew the nut and slide it off the shaft.', [NUT], alone=F1_SET, path=NUT_WAY, arrow_style={NUT: size('nut')},
         keep_camera=True)
g.remove('Slide the washer off the shaft.', [WASHER], alone=F1_SET, paths={WASHER: [slid(VIEW['Step 26']['carry'][WASHER]['pose'], POT_AT)]},
         arrow_style={WASHER: size('washer')}, keep_camera=True)
assert same_pose(where(F1), BUILD)
g.remove('Push the potentiometer out through the back of F1.', [POT], alone=F1_SET, path=[VIEW['Step 25']['carry'][POT]['pose']],
         arrow_style={POT: size('pot')}, **camera_of('Step 25'))   # ([21, 35, 100]: 79 mm behind F1, as the Full Build held it, by its
                                                                    # camera: from the published one the body starts hidden behind F1; its caps
g.put_away([F1])                                                   # ride on it, so its three leads go with it)

# ================================================================ THE BREADBOARD WIRES AND THE ROCKER SWITCH (the Full Build's Steps 21 - 9 reversed: the published 32 - 43)
# Yellow and orange first (the Full Build's 21 and 20 reversed): the published takes them last, where purple, blue and green lift through
# orange, which lies over them; and before the switch's leads, whose caps swing past i27 / i29 on their way to hang from the switch.
g.remove('Disconnect the yellow jumper wire from j3 and i29.', list(JUMPERS['yellow']), arrows=[], eye=[JUMPERS['yellow'][0]],
         caution=PULL)
g.remove('Disconnect the orange jumper wire from j1 and i27.', list(JUMPERS['orange']), arrows=[], eye=[JUMPERS['orange'][0]],
         keep_camera=True)
for k, (colour, hole, step) in enumerate((('black', 'j29', 'Step 18'), ('tan', '(+) red', 'Step 17'), ('red', 'j27', 'Step 16'))):
    g.unplug(f"Disconnect the switch's {colour} wire from {hole}.", [SWITCH_CAPS[colour]],   # (the published 32 - 34: black,
             **to_hanging({colour: SWITCH_CAPS[colour]}, 'switch', {colour: step}, 'Step 15c', SWITCH),   # tan, red)
             eye=[dict(id=SWITCH_CAPS[colour], side='near-right', reach=0.05)],
             **(dict(camera_of('Step 16', radius=55.0), caution=PULL) if k == 0 else dict(keep_camera=True)))   # (Lee's camera for Steps 16 - 18, a little
                                                                    # wider: the caps end under F4)
g.remove('Push the rocker switch up out of the square hole in F4.', [SWITCH], alone=[F4, SWITCH],
         review='The rocker switch clicks into F4 (the Full Build\'s Step 15). Does it have clips to squeeze before it can be pushed out? '
                'If so: "Squeeze the clips on the sides of the rocker switch, under F4, and push it up out of the square hole."',
         path=[compose(where(F4), VIEW['Step 15']['carry'][SWITCH]['pose'], g._pivot(SWITCH))],   # (50 mm over F4, where the Full Build held it)
         arrow_style={SWITCH: size('switch')}, **camera_of('Step 15'))
g.put_away([F4])
# The other six, as published (36 - 41): white, dark red, purple, blue, green, black (purple before blue clears; blue before purple brushes
# 0.78 mm). Each by its own Full Build way, reversed; the eye where the published has it.
for k, (colour, a, b, eye_cap) in enumerate((('white', 'a14', '(-) blue', 'NAUO15'), ('dark_red', 'a12', '(+) red', 'NAUO31'),
                                            ('purple', 'a8', 'i22', 'NAUO25'), ('blue', 'a9', 'i21', 'NAUO22'),
                                            ('green', '(-) blue', 'i24', 'NAUO20'), ('black', 'i23', '(+) red', 'NAUO17'))):
    g.remove(f"Disconnect the {colour.replace('_', ' ')} jumper wire from {a} and {b}.", list(JUMPERS[colour]), arrows=[],
             eye=[dict(id=eye_cap, side='down-right', reach=0.07)],   # (below and to the right, over F3, as published)
             **(dict(view_dir=[0.5663, 0.7152, 0.4096], frame=([680.0, 915.0, 1300.0], 75.0)) if k == 0 else dict(keep_camera=True)))
# (the published's one view of its Steps 36 - 47, from the breadboard's end, 46 degrees up (published_geometry.md, frame 092), framed on
# the board, kept to the end: from the Full Build's close cameras of the parts below, the published arrows filled the frame, the Nano
# Board's ran off its top; from the Full Build's jumper camera, 55 degrees up, the up arrows faced the camera and became eyes)

# ================================================================ THE BREADBOARD'S PARTS (the Full Build's Steps 7 - 3 reversed: the published 44 - 47)
g.remove('Pull the real time clock module out of j19 to j24.', [RTC, COIN], arrow_style={RTC: size('rtc')}, keep_camera=True)   # (one arrow: they came in together)
g.remove('Pull a 12 kΩ resistor out of (-) blue and h27.', [RES1], arrow_style={RES1: size('res1')}, keep_camera=True)   # (the published 45, 46)
g.remove('Pull the other 12 kΩ resistor out of (-) blue and h29.', [RES2], arrow_style={RES2: size('res2')}, keep_camera=True)
g.remove('Remove the Nano Board from the breadboard.', [NANO], arrow_style={NANO: size('nano')}, keep_camera=True,
         review='Does the LAC kit have a Pry Tool? If so, this step gets the caution "Use the Pry Tool to carefully remove the Nano Board.", '
                'as the MRA and LSM take-aparts have.')

g.build()
