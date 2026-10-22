# LAC deconstruction: the plan, ready to type into `LAC Build Instructions/deconstruction.py`

21 Oct 2026. Lee: "we need to make a deconstruction guide for this LAC as well. Here is the published version of the guide that we
need to convert / remake here: https://instructions.online/?id=19075-lac_deconstruction".

Read-only planning: nothing was run but light Python on JSON (`steps.json`, `published_geometry.json`, and the study scripts
`lead_order.py` / `jumper_order.py` in `scripts/`). No generator, no CAD, no browser. Built on the three studies in this folder
(`study_map.md`, `study_api.md`, `published_geometry.md` / `.json`), the published report `docs/research/guide_19075-lac_deconstruction.md`,
`tools/stepgen.py` (`take_apart`, `_takeoff` 969-1246, the take-off views 1771-1902, `_arrow_out` 1435-1513), the four other
`deconstruction.py` scripts and rulebook section 11. Every pose, route number and camera below was read from `steps.json` as it stands
at HEAD 61c6efc (Step 45: F9 brought in over its slots and tipped in, which is Lee's Step 45 request of today; the script reads F9's
poses from steps.json, so a later change to Step 45 is picked up, and an assert stops it if the shape of the change is new).

## 0. In short

- **32 steps** (Lee's groups, as the PMG's and LSM's drafts of the same day), or **47** with one wire per step as published (section 3
  gives the replacement code). Opens on the Full Build's title page, ends on F3 with the breadboard, then the Full Build's parts list.
- **Every step replays a state our Full Build already had, backwards.** That is the main departure from the published order, and the
  reason for it: in the published order our leads pass through each other (the Potentiometer's and the LCD's through the seated buzzer's
  black lead; purple, blue and green breadboard wires through the orange one; `scripts/lead_order.py`, `jumper_order.py`). Walking our
  Full Build back keeps every lead on a shape the Full Build drew (and Lee has seen) for exactly that state, so `wires=` / `wire_via=` can
  always be the Full Build's own routes and nothing needs drawing anew.
- **The one new state** is the USB cable at Step 4 (as soon as its plug can come out: in-house "power first"); section 4 says how to check
  it and where it goes if the check fails (after Step 15: the Full Build's own Step 40 state).
- **Dropped:** the published storage refit (its Steps 16 - 18: Lee, nothing refitted), its rolled views (Steps 2, 12 - 18: our player
  keeps world up), its cross-fades between posed copies (real moves here), its wordless frames (every step a caption of its own).
- **Added:** F1 moved back in front of the breadboard (our Full Build's Step 47 undone) and F1 picked up and held upright to take the
  Potentiometer apart (Step 29 undone): our F1 lies face down where the published one lies face up.
- Arrows: the published sizes (`dims=`, `published_geometry.md` section 3), an arrow per stage in turn where a part comes off in
  stages and no lead changes shape on the way (F9, the F7s); one arrow where a lead does (F2, F4, the buzzer: `then=` is refused with
  `wire_via=`, question 20).

| ours | what | call | published | undoes (ours) | camera | cue |
|---|---|---|---|---|---|---|
| 1 | F6 | remove | 1 | 57 | default (57) | arrow f6, caution POWER |
| 2 | F2, the USB cable walked back out of its slit | remove | 2 | 56 | default (56) | arrow f2 on stage 2; eye on the slit |
| 3 | F5 | remove | 3 | 55 | default (55) | arrow f5 |
| 4 | USB cable | remove | 25 (moved up) | 40 | 40's direction, wider | arrow usb on the plug |
| 5 | F1 pulled forward, still wired | lift | 4 | 54 | default (54) | arrow f1 |
| 6 | F1 laid face down aside | lift | 5 | 53 | 47's | eye |
| 7 | LCD out of F9's notches, angled | lift | 6 (first half) | 52 | default (52) | eye; close-up of F9's notches |
| 8 | LCD out of the case, laid face down | lift | 6 (second half) | 51 | 51's | eye |
| 9 | F8 | remove | 7 | 50 | default (50) | arrow f8 |
| 10 | F4 with the switch, laid behind the case | lift | 8 | 49 + 48 | 49's | arrow f4 (the lift) |
| 11 | F1 moved back in front of the breadboard | lift | (new) | 47 | 47's | eye |
| 12 | F9: tipped, then lifted | remove | 24 | 46 + 45 | 46's | arrows f9 in turn; close-up of the foot |
| 13 | F7s spread | lift | 26 | 44 | 44's | two arrows over the tops |
| 14 | buzzer out, laid beside the case, still wired | lift | 27 | 43 | default (43) | arrow buzzer (the lift); eye |
| 15 | F7s: close, then up and out | remove | 28 | 42 + 41 | 41's | arrows in turn (in, then up) |
| 16 | the LCD's four wires, both ends | remove | 19 - 22 | 39 - 36 | default (39) | 4 pin labels; 2 eyes; caution PULL |
| 17 | LCD Screen | remove | 23 | (35) | 35's | eye |
| 18 | the buzzer's two leads | unplug | 29, 30 | 34, 33 | default (34) | eye on each |
| 19 | Alarm Buzzer | remove | 31 | (33) | kept | eye |
| 20 | the Potentiometer's three leads (to hang from it) | unplug | 9 - 11 | 32 - 30 | 30's direction, wider | eye on each |
| 21 | F1 picked up, held upright | lift | (12's isolation) | 29 | 29's | eye |
| 22 | Knob | remove, alone | 12 | 28 | 28's | arrow knob |
| 23 | Nut (unscrewed) | remove, alone | 13 | 27 | kept | arrow nut |
| 24 | Washer | remove, alone | 14 | 26 | kept | arrow washer |
| 25 | Potentiometer out of F1; then put_away F1 | remove, alone | 15 | 25 | kept | arrow pot |
| 26 | orange and yellow breadboard wires | remove | 42, 43 | 21, 20 | default (21) | 2 eyes |
| 27 | the switch's three leads (to hang from it) | unplug | 32 - 34 | 18 - 16 | 16's, wider | eye on each |
| 28 | Rocker Switch out of F4; then put_away F4 | remove, alone | 35 | 15 | 15's | arrow switch |
| 29 | the other six breadboard wires | remove | 36 - 41 | 14 - 9 | 9's direction, the set framed | 2 eyes |
| 30 | Real Time Clock (with its coin cell) | remove | 44 | 7 | default (7) | arrow rtc |
| 31 | both 12 kΩ resistors | remove | 45, 46 | 6, 5 | default (6) | arrow res1, arrow res2 |
| 32 | Nano Board | remove | 47 | 3 | default (3) | arrow nano |
| end | Completed View: F3 + breadboard; the Full Build's parts list | | end | (2, 1) | generator | |

## 1. Why this order (and where it leaves the published)

The published (report section 6.1): 1 - 8 the case reversed (F6, F2, F5, F1 forward, F1 aside, the LCD out, F8, F4); then the
Potentiometer (9 - 15, and the refit 16 - 18), the LCD's wires and the LCD (19 - 23), F9 (24), the USB cable (25), the F7s and the buzzer
(26 - 28), the buzzer's leads and the buzzer (29 - 31), the switch (32 - 35), the eight breadboard wires (36 - 43), RTC, resistors, Nano.

Ours keeps 1 - 8 (its Steps 1 - 3, 5 - 10) and the end (30 - 32), and in between walks our Full Build back, step for step:

| our steps | the Full Build state they replay | why not the published order there |
|---|---|---|
| 11 - 15 | 47 - 41 (F1 face down in front of the breadboard; F9 in; the buzzer seated, then lying wired; the LCD lying wired; F4 flat behind) | the buzzer must leave the F7s before any lead near it moves: in the published order (pot 9 - 11, LCD 19 - 22 with the buzzer seated) the pot's tan and red and the LCD's GND pass through the seated buzzer's black lead (0.52, 0.20, 0.15 mm apart; touching is 1.25). F1 must come back from where Step 6 laid it: unplugged there, the pot's tan lead passes through the red, the switch's tan and the purple jumper (those Step 47 shapes are long `stretch` leads never drawn for a plug to move). |
| 16 - 19 | 39 - 33 (the LCD's wires came on after the pot's and the buzzer's, so they come off first) | the published unplugs the pot before the LCD. Both orders are clear at the first stage in our model once the buzzer lies outside (lead_order.py), but our pot unplug has a second stage (each cap swung out 40 mm to hang from the Potentiometer, as before the Full Build plugged it in), through ground the LCD's wires occupy: no Full Build state ever had the pot's caps hanging with the LCD wired. |
| 20 - 25 | 32 - 25 | the published strips the pot on F1 lying face up, in a view rolled on its side; ours lies face down (knob down), so it is picked up and held upright as the Full Build held it (Step 29 undone) and stripped by the Full Build's own camera. |
| 26 | 21, 20 | the published takes orange and yellow last; purple, blue and green lifting out pass through orange (0.98 - 1.15 mm; jumper_order.py), which lies over them. |
| 27, 28 | 18 - 15 | the switch's leads in the published come off with orange and yellow still in (its caps' second stage swings past i27 / i29, orange's and yellow's ends): taken in the Full Build's order instead, orange and yellow are out first. |
| 29 | 14 - 9 | (published 36 - 41) |

USB cable: in-house rule (MRA, RCC, PMG; the LSM's as soon as reachable, with Step 1's caution): our Step 4, as soon as F6, F2 and F5
are off (F5 blocks its +z way, F2 holds the cable in its slit). If the check of section 4 fails, it goes after Step 15, where the state is
the Full Build's Step 40c exactly (the published has it after F9, our Step 12, which is the same idea).

## 2. The script

### 2.1 The header (paste as is)

```python
"""LCD Alarm Clock (LAC), deconstruction: the finished clock taken apart, down to F3 with the breadboard stuck on it. A guide of its
own (steps-deconstruction.json), made from the Full Build as guide.py last wrote it (run that first, and this again after any change
to it). It opens on the Full Build's title page, ends on what is left, F3 and the breadboard (as TechBox's published take-apart ends:
the breadboard is stuck on for good), followed by the Full Build's parts list (as the MRA's, PMG's and LSM's); its card on the website
is the Full Build's.

First draft (Lee, 21 Oct 2026: "we need to make a deconstruction guide for this LAC as well. Here is the published version of the
guide that we need to convert / remake here: https://instructions.online/?id=19075-lac_deconstruction"): TechBox's published LAC
take-apart (docs/research/guide_19075-lac_deconstruction.md, 47 steps) remade on our Full Build, within the in-house principles
(rulebook section 11): every step a caption of its own; parts that went on one at a time and go together come off together (Lee's PMG
and LSM groups: the LCD's four wires, each part's leads, the breadboard wires); each arrow the size of the published one, one per stage,
in turn; nothing put back on (the published Steps 16 - 18 refit the washer, nut and knob for storage: left out). The plan and its
reasons: docs/research/lac/decon/plan.md.
  1. the case: F6, F2 (the USB cable walked back out of its slit), F5; then the USB cable, as soon as its plug can come out (Step 1's
     caution says to disconnect it from the computer first: the closed case holds the plug, as the LSM's box does);
  2. F1 pulled forward and laid aside, still wired; the LCD Screen out of F9's notches, then out of the case to lie face down, still
     wired (two steps, as the Full Build brought it in); F8; F4 lifted off with the Rocker Switch and laid behind the case, still wired;
  3. the Full Build's Steps 47 - 41 reversed: F1 back in front of the breadboard's end, F9 tipped and lifted out, the F7s spread, the
     Alarm Buzzer lifted out to lie beside the case, still wired, the F7s out;
  4. each wired part, as the Full Build wired them, reversed: the LCD's four wires and the LCD; the buzzer's two leads and the buzzer;
     the Potentiometer's three leads, F1 picked up and held upright, the Potentiometer taken apart on its own (Knob, Nut, Washer, out of
     F1); the orange and yellow breadboard wires; the switch's three leads and the switch out of F4, on its own; the other six wires;
  5. the Real Time Clock, both 12 kOhm resistors, the Nano Board.
Where it leaves the published order, our model made it: in the published order the Potentiometer's and the LCD's leads pass through the
seated buzzer's black lead, and the purple, blue and green breadboard wires through the orange one. Here every step replays a state of
our Full Build, backwards, so that every lead keeps a shape the Full Build drew for that state."""
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
# (docs/research/lac/decon/published_geometry.md section 3); an arrow per stage, in turn, where a part comes off in stages and no lead
# changes shape on the way (F9, the F7s). The F7s' up arrows: F7A's (at the back) 34.2 mm, F7B's 37.3 (study_api.md's table has the two
# the other way round; published_geometry.json by tail: x 640 is F7A, x 711 F7B).
PUBLISHED = dict(f6=(56.1, 4.87), f2=(79.8, 5.51), f5=(64.6, 6.19), usb=(63.5, 5.78), f1=(79.0, 5.78), f8=(83.9, 4.51),
                 f4=(73.2, 3.35), f9=(33.8, 3.3), f7a_spread=(36.9, 3.75), f7b_spread=(40.5, 3.8), buzzer=(58.3, 6.15),
                 f7a_up=(34.2, 3.96), f7b_up=(37.3, 3.96), knob=(41.2, 2.93), nut=(56.5, 3.72), washer=(70.6, 2.89),
                 pot=(52.7, 4.21), switch=(63.6, 4.95), rtc=(29.8, 3.55), res1=(39.4, 3.47), res2=(46.8, 3.96), nano=(64.2, 3.72))
size = lambda key, **more: dict(dims=PUBLISHED[key], **more)
POWER = 'Disconnect the USB Cable from the computer or power supply before you begin.'
PULL = 'Pull each wire out by its connector. Do not pull on the wires themselves.'
```

### 2.2 The steps (paste in this order; `g.build()` last)

```python
# ================================================================ THE CASE (the Full Build's Steps 57 - 55 reversed: the published 1 - 3)
g.remove('Pull F6 off the end of the case nearest the Knob.', [F6], arrow_style={F6: size('f6')}, caution=POWER)
g.remove('Swing the free end of F2 out from the case. Then slide F2 along to unhook it from F5, and pull it away, clear of the USB '
         'Cable.', [F2],
         wire_via={'usb cable': [ROUTES[n] for n in VIEW['Step 56c']['wire_via']['usb cable'][::-1]]},   # (124, 74: walked back out of
         wires={'usb cable': ROUTES[VIEW['Step 56']['wires']['usb cable']]},                              #  the slit, a stage a beat)
         arrow_style={F2: size('f2', stage=2)},                     # (on the pull away: then= is refused with wire_via=)
         eye=[dict(e) for e in VIEW['Step 56']['eye']])             # (the Full Build's eye on the slit, where the cable passes: as published)
g.remove('Pull F5 off the other end of the case.', [F5], arrow_style={F5: size('f5')})

# ================================================================ POWER (as soon as the plug can come out: the published 25, moved up)
g.remove('Disconnect the USB Cable from the Nano Board.', [USB_B, USB_A], units=[[USB_B]], arrow_style={USB_B: size('usb')},
         paths={USB_A: [_shifted(where(USB_A), [0.0, 30.0, 0.0])]},   # (its far end lifted off the table with it: the cable goes whole)
         **camera_of('Step 40', target=[628.0, 900.0, 1365.0], radius=65.0))   # (the Full Build's Step 40, wider: plug, arrow, A end)

# ================================================================ F1, THE LCD SCREEN, F8, F4 (the Full Build's Steps 54 - 48 reversed: the published 4 - 8)
g.lift("Pull F1 forward off the tabs of F3 and F4. Leave the Potentiometer's wires connected.", [F1, POT],
       wires=leads('Step 54', 'pot'), arrow_style={F1: size('f1')})   # (Step 54 reversed, by its camera; POT rides on F1 from now on)
g.lift('Lay F1 face down in front of the case, toward the end where F6 was.', [F1], path=[VIEW['Step 53']['carry'][F1]['pose']],
       wires=leads('Step 53', 'pot'), arrows=[], eye=[dict(id=F1, side='up-right', reach=0.035)],   # (an eye, as published Step 5)
       **camera_of('Step 47'))                                      # (the Full Build's view of F1 laid aside: Step 54's leaves it out)
NOTCHES = VIEW['Step 52c']['inset']
g.lift('Slide the LCD Screen toward F8 until its board comes out of the notches in F9, then swing its free end out from the case. '
       'Leave its wires connected.', [LCD], wires=leads('Step 52', 'lcd'), wire_via=stages_back('Step 52', 'lcd'),
       arrows=[], eye=[dict(id=LCD, anchor=[713.76, 895.78, 1358.05])],   # (published Step 6: an eye on its F9 end)
       inset=dict(target=NOTCHES['target'], dir=NOTCHES['dir'], radius=NOTCHES['radius'], alt=NOTCHES['alt'],
                  marks=[(m['at'], m['half']) for m in NOTCHES['marks']]))   # (Step 52c's close-up; steps.json writes marks as dicts)
g.lift('Slide the LCD Screen out of the slots in F8, bring it out through the front of the case, and lay it face down beside the '
       'case. Leave its wires connected.', [LCD], path=ride_back('Step 51', LCD), wire_via=stages_back('Step 51', 'lcd'),
       wires=leads('Step 51', 'lcd'), arrows=[], eye=[dict(id=LCD, side='up-left', reach=0.05)], **camera_of('Step 51'))
g.remove('Slide F8 out of the slots in F3 and F4, toward the front.', [F8], arrow_style={F8: size('f8')})
g.lift("Lift F4, with the Rocker Switch, off the tabs of the F7s and F9, and lay it behind the case. Leave the Rocker Switch's wires "
       'connected.', [F4], path=[VIEW['Step 49']['path'][0], VIEW['Step 48']['carry'][F4]['pose']],   # (up over the frame, then down
       wire_via={w: [r] for w, r in leads('Step 49', 'switch').items()},   # behind the case: Steps 49 and 48, a beat each; the leads over
       wires=leads('Step 48', 'switch'),                                   # the frame, then as they lay before Step 48)
       arrow_style={F4: size('f4', stage=0)}, **camera_of('Step 49'))

# ================================================================ THE FULL BUILD'S STEPS 47 - 41 REVERSED (the published 24, 26 - 28)
g.lift('Move F1, still face down, back in front of the end of the breadboard.', [F1], path=[VIEW['Step 47']['carry'][F1]['pose']],
       wires=leads('Step 47', 'pot'), arrows=[], eye=[dict(id=F1, side='up-left', reach=0.05)], **camera_of('Step 47'))
HOOKED = VIEW['Step 46']['carry'][F9]['pose']                      # (tipped forward about its front edge: its back foot up out of F3)
TIPPED = VIEW['Step 45c']['carry'][F9]['via']                     # (the same tilt, 33 mm higher: its front foot up out of its slot)
assert len(TIPPED) == 1, TIPPED                                    # (Step 45 as of 61c6efc: look again if Lee changes its way)
FOOT = VIEW['Step 45c']['inset']
g.remove('Tip the top of F9 toward the front to lift its back foot out of F3. Then lift F9 up out of its front slot.', [F9],
         path=[HOOKED, *TIPPED], arrow_style={F9: size('f9', stage=0, then=[size('f9', stage=1)])},   # (the tip, then the lift)
         inset=dict(target=FOOT['target'], dir=FOOT['dir'], radius=FOOT['radius'], mark=FOOT['mark'], ghost=FOOT['ghost'],
                    alt=FOOT['alt']),                              # (Step 45c's close-up: the front foot's barb under F3, F3 faint)
         **camera_of('Step 46'))
g.lift('Gently pull the tops of the two F7s apart to free the Alarm Buzzer.', [F7A, F7B], ride_on=F3,   # (ride_on: else F7B rides on F7A)
       paths={i: [VIEW['Step 42c']['carry'][i]['pose']] for i in (F7A, F7B)},   # (15 degrees each way about its outer bottom edge)
       arrows=[dict(tail=[659.0, 968.0, 1233.2], head=[622.1, 968.0, 1233.2], normal=[0.0, 1.0, 0.0], part=F3, width=3.75),   # (10 mm
               dict(tail=[691.6, 968.0, 1233.2], head=[732.1, 968.0, 1233.2], normal=[0.0, 1.0, 0.0], part=F3, width=3.8)],   #  over the
       **camera_of('Step 44'))                                      # tops, outward, the published lengths; the Full Build's Step 42 ones
                                                                    # at y 945 lie behind F7A from the front)
g.lift('Lift the Alarm Buzzer out from between the two F7s and lay it beside the case, past the end of the breadboard. Leave its '
       'wires connected.', [BUZZER], wires=leads('Step 43', 'buzzer'), wire_via=stages_back('Step 43', 'buzzer'),   # (Step 43 reversed,
       arrow_style={BUZZER: size('buzzer', stage=0)},              # by its camera: up 75, over the board, down: a beat each; the arrow
       eye=[dict(id=BUZZER, anchor=[676.1, 934.26, 1226.81], side='near-above', reach=0.05)])   # on the lift out; an eye, as published)
UP = VIEW['Step 41']['carry'][F7A]['pose']                         # ([0, 80, 0]: where the Full Build held them over their slots)
g.remove('Let the two F7s close, then pull them up out of their slots in F3.', [F7A, F7B], paths={i: [ZERO, UP] for i in (F7A, F7B)},
         arrow_style={F7A: dict(dims=(14.0, 3.75), stage=0, at=[641.0, 965.0, 1233.2], then=[size('f7a_up', stage=1)]),   # (inward over
                      F7B: dict(dims=(14.0, 3.8), stage=0, at=[710.0, 965.0, 1233.2], then=[size('f7b_up', stage=1)])},   #  the tilted
         **camera_of('Step 41'))                                    # tops, short so that they do not meet; then each up, as published)

# ================================================================ THE LCD SCREEN AND THE ALARM BUZZER OFF THEIR WIRES (the Full Build's 39 - 33 reversed: the published 19 - 23, 29 - 31)
# (GND, VCC, SDA, SCL: the Full Build's labels of Steps 36 - 39, anchored on the LCD's pins; and each female cap 15 mm back off its
# pin, [0, 0, 15] on the LCD, where the Full Build held it before pushing it on)
PIN_LABELS = [next(dict(l) for l in VIEW[step]['labels'] if l['id'] == LCD) for _, _, step in LCD_WIRES.values()]
OFF_PIN = {fem: compose(where(LCD), VIEW[step]['carry'][fem]['pose'], g._pivot(fem)) for _, fem, step in LCD_WIRES.values()}
g.remove('Disconnect the four wires from the GND, VCC, SDA, and SCL pins of the LCD Screen and from the breadboard.',
         [c for male, fem, _ in LCD_WIRES.values() for c in (male, fem)], paths={f: [p] for f, p in OFF_PIN.items()},
         arrows=[], eye=[LCD_WIRES['yellow'][0], LCD_WIRES['teal'][0]],   # (an eye on the rail ends, one on b8 / b9; the males up 18:
         labels=PIN_LABELS, caution=PULL)                          # their Full Build ways, by Step 39's camera)
g.remove('Remove the LCD Screen.', [LCD], path=[_shifted(where(LCD), [0.0, 30.0, 0.0])], arrows=[], eye=[LCD],   # (published: an eye,
         **camera_of('Step 35'))                                   # a fade where it lies; in-house a removal slides, then fades)
g.unplug("Disconnect the Alarm Buzzer's red wire from j4 and its black wire from the (-) blue rail.", list(BUZZER_CAPS.values()),
         ride_on=BUZZER)                                           # (Steps 34 and 33 reversed, by Step 34's camera, back to where each
                                                                   # lay by the buzzer; ride_on: the red cap rode on nothing before Step 33)
g.remove('Remove the Alarm Buzzer.', [BUZZER], path=[_shifted(where(BUZZER), [0.0, 30.0, 0.0])], arrows=[], eye=[BUZZER], keep_camera=True)

# ================================================================ THE POTENTIOMETER (the Full Build's Steps 32 - 25 reversed: the published 9 - 15)
assert same_pose(where(F1), VIEW['Step 47']['carry'][F1]['pose'])  # (face down in front of the breadboard's end, as when it was wired)
g.unplug("Disconnect the Potentiometer's red wire from the (+) red rail, its tan wire from a5, and its black wire from the (-) blue "
         'rail.', list(POT_CAPS.values()),
         **to_hanging(POT_CAPS, 'pot', {'red': 'Step 30', 'tan': 'Step 31', 'black': 'Step 32'}, 'Step 29c', POT),
         **camera_of('Step 30', target=[744.0, 910.0, 1335.0], radius=60.0))   # (the Full Build's direction, wider: holes and Potentiometer)
BUILD = VIEW['Step 29']['carry'][F1]['pose']                       # ([100, 35, 100]: F1 held up, as the Full Build fitted the Potentiometer)
g.lift('Pick up F1 with the Potentiometer and hold it upright, the Knob facing out.', [F1], path=[BUILD], wires=leads('Step 29', 'pot'),
       arrows=[], eye=[dict(id=F1, side='down-right', reach=0.065)], **camera_of('Step 29'))   # (Step 29 reversed: the leads hang with it)
POT_AT = shift_of(where(POT))                                      # (= BUILD: the Potentiometer rides on F1, in its seat on it)
assert np.allclose(POT_AT, shift_of(BUILD), atol=0.05), POT_AT
F1_SET = [F1, POT, KNOB, NUT, WASHER]                              # (F1 on its own; the three leads' caps ride on the Potentiometer)
g.remove("Pull the Knob straight off the end of the Potentiometer's shaft.", [KNOB], alone=F1_SET,
         paths={KNOB: [slid(VIEW['Step 28']['carry'][KNOB]['pose'], POT_AT)]},   # (60 mm along the shaft: where the Full Build held it)
         arrow_style={KNOB: size('knob')}, **camera_of('Step 28'))  # (BUILD_LOOK, the Full Build's camera for Steps 25 - 28)
nut = VIEW['Step 27c']['carry'][NUT]
NUT_WAY = [slid(p, POT_AT) for p in [*nut['via'][::-1], VIEW['Step 27']['carry'][NUT]['pose']]]   # (the seven quarter turns back, then off)
NUT_WAY = [p if k in (3, len(NUT_WAY) - 1) else via(p) for k, p in enumerate(NUT_WAY)]          # (two beats: a stop after the first turn)
g.remove('Turn the Nut to unscrew it, then slide it off the shaft.', [NUT], alone=F1_SET, path=NUT_WAY, arrow_style={NUT: size('nut')},
         keep_camera=True)
g.remove('Slide the Washer off the shaft.', [WASHER], alone=F1_SET, paths={WASHER: [slid(VIEW['Step 26']['carry'][WASHER]['pose'], POT_AT)]},
         arrow_style={WASHER: size('washer')}, keep_camera=True)
assert same_pose(where(F1), BUILD)
g.remove('Push the Potentiometer out through the back of F1.', [POT], alone=F1_SET, path=[VIEW['Step 25']['carry'][POT]['pose']],
         arrow_style={POT: size('pot')}, keep_camera=True)         # ([21, 35, 100]: 79 mm behind F1, as the Full Build held it; its caps
g.put_away([F1])                                                   # ride on it, so its three leads go with it)

# ================================================================ THE BREADBOARD WIRES AND THE ROCKER SWITCH (the Full Build's Steps 21 - 9 reversed: the published 32 - 43)
g.remove('Disconnect the orange breadboard wire from j1 and i27, and the yellow breadboard wire from j3 and i29.',
         [*JUMPERS['orange'], *JUMPERS['yellow']], arrows=[],      # (both up 18 together, their Full Build ways: neither passes through
         eye=[JUMPERS['orange'][0], JUMPERS['yellow'][0]])         #  the other; an eye on each j end, as published; Step 21's camera)
g.unplug("Disconnect the Rocker Switch's red wire from j27, its tan wire from the (+) red rail, and its black wire from j29.",
         list(SWITCH_CAPS.values()),
         **to_hanging(SWITCH_CAPS, 'switch', {'red': 'Step 16', 'tan': 'Step 17', 'black': 'Step 18'}, 'Step 15c', SWITCH),
         **camera_of('Step 16', radius=55.0))                      # (Lee's camera for Steps 16 - 18, a little wider: the caps end under F4)
g.remove('Push the Rocker Switch up out of the square hole in F4.', [SWITCH], alone=[F4, SWITCH],
         path=[compose(where(F4), VIEW['Step 15']['carry'][SWITCH]['pose'], g._pivot(SWITCH))],   # (50 mm over F4, where the Full Build held it)
         arrow_style={SWITCH: size('switch')}, **camera_of('Step 15'))
g.put_away([F4])
SIX = [c for colour in ('black', 'green', 'purple', 'blue', 'white', 'dark_red') for c in JUMPERS[colour]]
g.remove('Disconnect the black, green, purple, blue, white, and dark red breadboard wires.', SIX,
         paths={c: [[0.0, 25.0, 0.0]] for c in SIX}, arrows=[],   # (all six straight up together: none moves against another)
         eye=[JUMPERS['purple'][0], JUMPERS['green'][1]],          # (an eye on the a8 end, one on the i24 end)
         **camera_of('Step 9', target=[682.0, 912.0, 1305.0], radius=48.0))   # (the Full Build's jumper camera, the whole set in frame)

# ================================================================ THE BREADBOARD'S PARTS (the Full Build's Steps 7 - 3 reversed: the published 44 - 47)
g.remove('Remove the Real Time Clock from j19 to j24.', [RTC, COIN], arrow_style={RTC: size('rtc')})   # (one arrow: they came in together)
g.remove('Remove both 12 kΩ Resistors from h27, h29, and the (-) blue rail.', [RES1, RES2],
         arrow_style={RES1: size('res1'), RES2: size('res2')})     # (an arrow each: two Full Build steps, two units)
g.remove('Remove the Nano Board from the breadboard.', [NANO], arrow_style={NANO: size('nano')})

g.build()
```

### 2.3 Per step: what the call relies on, where it leaves the published, what to look at first

1. **F6.** Default way (Step 57: -z 67.5) and camera. Published camera 8.6 deg away, 1.42x wider: ours is the Full Build's (rulebook:
   cameras reused). POWER caution as the LSM's (the plug is inside the closed case).
2. **F2.** Default way, 3 beats (swing open about the hinge at F5's inside, 14 mm along itself out of F5's slots, 40 mm out along -x); the
   cable's two in-between shapes keep pace (124, 74; 3 legs for 3 beats). One arrow, on stage 2, the pull (published: one 80 mm -X arrow
   in a view rolled 119 deg, which our player cannot copy; ours is seen from behind, Step 56's camera). Look: the arrow points 45 deg
   towards the camera (`d . dir` = 0.70; under 0.8 so it is drawn). If it reads badly: `stage=0` (the swing) or a camera turned towards
   the side. The eye is the Full Build's Step 56 eye on F2 at the slit (published: on the cable at the slit, the same spot).
3. **F5.** Default (Step 55: +z 56), END_CAMERA.
4. **USB cable.** USB_B by its record (Step 40: +z 18); USB_A has none (it rests off its seat, turned): lifted 30 with it. One arrow, on the
   plug (rulebook, RCC: "one arrow, on the plug that is pulled, clear of the cable, and none on its far end"). Camera: Step 40's direction
   (from behind at the breadboard's end; F2 is off, so the plug shows), framed on plug, arrow tip and A end. The +z arrow is 40 deg off the
   line of sight (foreshortened to about 0.64). **New state** (the only one): see section 4, check A.
5. **F1 forward.** Default way and camera (Step 54: F1 and the Potentiometer both listed: the record's group of two). `wires` = Step 54's
   hover routes (118 - 120). The Potentiometer rides on F1 from here on; the Knob, Nut and Washer on it.
6. **F1 aside.** Step 53's ride reversed (FRONT_OUT to F1_ASIDE, face down, a quarter turn about F1's middle); `wires` 81 - 83. Camera
   Step 47's (the Full Build's frame for F1 aside: Step 53's own leaves F1_ASIDE partly out, about 128 mm off its middle at radius 120).
   Published: an eye, no arrow; F1 laid face up beyond the -z end (ours face down along the front, toward the -z end).
7. **LCD unclipped.** Default way (Step 52 reversed: slid 14.9 mm toward F8 out of F9's notches, straightened back to angled; 2 beats) and
   camera; the leads' standing shape (110 - 113), then angled (106 - 109). The published eye anchor (its F9 end, low) and the Full Build's
   Step 52c close-up of F9's two notches (two red boxes, as the published close-up's picture).
8. **LCD laid down.** Step 51's ride reversed (IN, OUT, ON_END, LYING: 4 beats) with its three in-between lead shapes (96, 95, 94 ...)
   and the lying ones (90 - 93): 4 legs for 4 beats. Published: Steps 6's three cross-fades in one step (question 18).
9. **F8.** Default (Step 50: +x 94; Lee's screenshot camera). The generator may NOTE that this camera leaves out F1 and the LCD lying
   aside: expected.
10. **F4.** Steps 49 and 48 in one lift, as the published does (lifted, then laid flat): 2 beats, the switch's leads over the frame
    (84 - 86), then as they lay (30 - 32). One arrow, on the lift (stage 0).
11. **F1 back.** Step 47's ride reversed (F1_ASIDE to F1_DOWN: a slide, same turn); `wires` 47 - 49 (the routes the pot's leads were
    plugged with). Not in the published (its F1 never had to move for the LCD's wires: see section 1).
12. **F9.** Steps 46 and 45 reversed: back to HOOKED (its back foot up), then 33 mm up, still tipped (TIPPED); stops there, as the
    published (the Full Build held it upright 35.3 mm over its slots before it tipped in: a third stage, upright in the air, adds nothing
    for a student). Arrows in turn: stage 0 along the tip (mostly +x: `d . dir` about 0.67), then up (published one 33.8 mm +Y arrow; the
    tip had none: Lee's PMG ruling gives each stage one). Close-up: the Full Build's Step 45c (the front foot's barb under F3, F3 drawn
    faint) = the published Step 24's picture. Lee is changing Step 45 today: the poses come from steps.json; the assert stops the run if
    Step 45's ride gets more stops than one via.
13. **F7s spread.** Step 44 reversed (both to their Step 42c tilts), `ride_on=F3` (else F7B rides on F7A afterwards). Arrows by hand, 10 mm
    over the tops, outward, the published 36.9 / 40.5 mm and widths (the Full Build's Step 42 arrows, at y 945, lie behind F7A from this
    camera's side).
14. **Buzzer out.** Default way (Step 43 reversed: up 75 between the spread F7s, over the board, down to lie past the breadboard's end;
    3 beats) with the leads' two in-between shapes (76, 75 / 78, 77) and the lying ones (52 / 53). The arrow on the lift out (published:
    +Z 58.3 mm out between the F7s, which is not our way: ours goes up). Eye at the published spot (its top). It replays the Full Build's
    Step 43 backwards, including its known 50 ms brush of the black lead through the LCD's wires (README question 11): not new.
15. **F7s out.** Straightened (back to their seats), then up 80 (Step 41's hover): two stages each, an arrow each in turn: short
    inward ones over the tilted tops (14 mm, so that the two do not meet in the 30 mm gap), then the published up arrows. If Lee prefers
    the published (up arrows only): `arrow_style={F7A: size('f7a_up', stage=1), F7B: size('f7b_up', stage=1)}`.
16. **LCD wires.** All four, both ends (the MRA's eight breadboard wires at once; Lee's PMG / LSM groups): the males up 18 (their Full
    Build ways, Steps 36 - 39), the females 15 mm back off their pins (where the Full Build held them, on the LCD's own frame). Each lead
    goes with its two ends. The published pin labels, on the LCD's pins (the Full Build's Step 36 - 39 labels, anchors on the LCD,
    `near-right`); eyes on the breadboard ends (published: eye on the breadboard end, label on the LCD end). Camera: Step 39's. The
    published order within the four (GND first) is what clears one at a time; together they do not move against each other at the male
    ends, and their female ends all move the same way.
17. **LCD away.** Off its seat: a 30 mm lift, then the fade, with an eye (published: an eye, a fade where it lies). Step 35's camera (the
    Full Build's frame of the LCD lying: Step 39's cuts its far end).
18. **Buzzer's leads.** Default unplug of both (Steps 34 and 33 reversed, by Step 34's camera): each cap out of its hole and back to
    where it lay by the buzzer, its lead through the Full Build's shapes (52 -> 50, 53 -> 51; each 2 beats); `ride_on=BUZZER` (the red cap
    rode on nothing before Step 33: without it the buzzer's removal is refused).
19. **Buzzer away.** As 17, Step 34's camera kept.
20. **Pot leads.** By hand (`to_hanging`): each cap out of its hole (18 up; the black 5, under the tan's hump, as it went in), then on to
    hang from the Potentiometer where it hung before the Full Build plugged it in (Step 29c's carry poses; routes 47 -> 44, 48 -> 45,
    49 -> 46). The generator's own unplug would leave each cap held over its hole, riding on the Potentiometer in that odd place, to be
    swung up into the air with F1 at Step 21. Camera: POT_CAMERA's direction (from behind at the breadboard's end, high: F1 lies face down
    with the Potentiometer on top), framed on the holes and the Potentiometer (radius 60 from 41.7).
21. **F1 picked up.** Step 29 reversed (F1_DOWN to BUILD: a quarter turn up and 100 mm out, one beat), `wires` 41 - 43 (the leads hanging
    from the Potentiometer with F1 held up). In the whole model, by Step 29's camera; the next four are on their own. The LCD and the buzzer
    are gone by now, so F1's sweep meets nothing (it stays 13 mm clear of where the LCD lay anyway: x 769 and up, the LCD to x 756).
22. **Knob.** Step 28 reversed: 60 mm along the shaft (published 52.7). `alone=F1_SET` (the movers must be in it; the caps come as
    riders). BUILD_LOOK camera (published: in F1's seated frame, roll 0: view_dir (0.6112, 0.5658, -0.5535), 22.5 deg from ours).
23. **Nut.** Step 27 reversed: seven quarter turns back (unscrewing: the opposite way to the Full Build's), then off to 60 mm; a stop after
    the first whole turn, so two beats (the published slides it off 58.7 mm without turning). `slid()`, not `compose()`, so the turns past
    360 deg stay as written (the LSM's NUT_WAY).
24. **Washer.** Step 26 reversed: 60 mm along the shaft.
25. **Potentiometer out of F1.** Step 25 reversed: 79 mm out of F1's back, to [21, 35, 100] (F3 is in its seat, so the Full Build's carry
    pose is where it goes). Its three caps ride on it: its leads go with it. Then `put_away([F1])`.
26. **Orange and yellow.** Both by their records (Steps 21, 20: straight up 18), together: the same move, so they cannot pass through each
    other (one at a time they brush, 0.95 mm, as the Full Build's own Step 21 does). Step 21's camera.
27. **Switch leads.** As 20, from Steps 18 - 16 to Step 15c's hanging poses (routes 30 -> 27, 31 -> 28, 32 -> 29); Lee's Step 16 camera,
    radius 55 (from 45.2: the caps end at its edge, under F4).
28. **Switch out of F4.** Step 15 reversed: 50 mm up out of F4's top (published 85.1); its caps and leads with it; on its own; Step 15's
    camera (F4 lies where it lay then). Then `put_away([F4])`.
29. **Six breadboard wires.** All twelve caps straight up 25 together (not their Full Build ways: white and dark red came in sideways
    under purple and blue; moved as one, nothing moves against anything). JUMPER_DIR, framed on the whole set (radius 48; their own
    cameras were 26 - 34).
30. - 32. **RTC, resistors, Nano.** Defaults (records 7, 6 / 5, 3, their cameras). The two resistors in one step (alike, "two of a kind"),
    an arrow each (two units: two Full Build steps).
End: the generator frames F3 with the breadboard from Step 32's camera direction (Step 3's); the published Completed View is from
(0.4954, 0.7631, 0.4151), radius 84.2: `Guide(..., end_view=dict(view_dir=[0.4954, 0.7631, 0.4151], frame=([678.1, 887.0, 1305.0], 84.2)))`
if Lee wants it (target moved up onto the board: the published orbit target is 34 mm under it).

## 3. One wire per step, as published (47 steps): the replacements

Replace Steps 16, 18, 20, 26, 27, 29 and 31 with these (each step still has its own caption). Orders: the published where it clears in
our model, else the Full Build reversed (noted).

```python
# 16 -> four (the published 19 - 22, its order: GND first. SCL first passes through purple, yellow and teal: lead_order.py)
HOLE = {'purple': 'the (-) blue rail', 'yellow': 'the (+) red rail', 'teal': 'b8', 'blue': 'b9'}
for k, (colour, (male, fem, step)) in enumerate(LCD_WIRES.items()):
    g.remove(f"Disconnect the {colour} wire from {PIN_LABELS[k]['text']} on the LCD Screen and from {HOLE[colour]}.", [male, fem],
             paths={fem: [OFF_PIN[fem]]}, arrows=[], eye=[male], labels=[PIN_LABELS[k]],
             **(dict(caution=PULL) if k == 0 else dict(keep_camera=True)))   # (Step 36's camera, kept for the four: published held one)
# 18 -> two (the published 29, 30: red, then black; either order clears)
g.unplug("Disconnect the Alarm Buzzer's red wire from j4.", [BUZZER_CAPS['red']], ride_on=BUZZER)
g.unplug("Disconnect the Alarm Buzzer's black wire from the (-) blue rail.", [BUZZER_CAPS['black']], keep_camera=True)
# 20 -> three (the published 9 - 11 = the Full Build reversed: black, tan, red)
for k, (colour, hole, step) in enumerate((('black', 'the (-) blue rail', 'Step 32'), ('tan', 'a5', 'Step 31'), ('red', 'the (+) red rail', 'Step 30'))):
    g.unplug(f"Disconnect the Potentiometer's {colour} wire from {hole}.", [POT_CAPS[colour]],
             **to_hanging({colour: POT_CAPS[colour]}, 'pot', {colour: step}, 'Step 29c', POT),
             **(camera_of('Step 30', target=[744.0, 910.0, 1335.0], radius=60.0) if k == 0 else dict(keep_camera=True)))
# 26 -> two (the Full Build reversed: yellow, then orange; the published orange first; both brush 0.95 mm, as the Full Build's Step 21)
g.remove('Disconnect the yellow breadboard wire from j3 and i29.', list(JUMPERS['yellow']), arrows=[], eye=[JUMPERS['yellow'][0]])
g.remove('Disconnect the orange breadboard wire from j1 and i27.', list(JUMPERS['orange']), arrows=[], eye=[JUMPERS['orange'][0]], keep_camera=True)
# 27 -> three (the published 32 - 34 = the Full Build reversed: black, tan, red)
for k, (colour, hole, step) in enumerate((('black', 'j29', 'Step 18'), ('tan', 'the (+) red rail', 'Step 17'), ('red', 'j27', 'Step 16'))):
    g.unplug(f"Disconnect the Rocker Switch's {colour} wire from {hole}.", [SWITCH_CAPS[colour]],
             **to_hanging({colour: SWITCH_CAPS[colour]}, 'switch', {colour: step}, 'Step 15c', SWITCH),
             **(camera_of('Step 16', radius=55.0) if k == 0 else dict(keep_camera=True)))
# 29 -> six (the published 36 - 41: white, dark red, purple, blue, green, black; purple before blue clears, blue before purple brushes
# 0.78 mm). Each by its own Full Build way (up 18; white and dark red up 5, then out 14 sideways), the eye where the published has it.
for k, (colour, a, b, eye_cap) in enumerate((('white', 'a14', 'the (-) blue rail', 'NAUO15'), ('dark_red', 'a12', 'the (+) red rail', 'NAUO31'),
                                            ('purple', 'a8', 'i22', 'NAUO25'), ('blue', 'a9', 'i21', 'NAUO22'),
                                            ('green', 'the (-) blue rail', 'i24', 'NAUO20'), ('black', 'i23', 'the (+) red rail', 'NAUO17'))):
    g.remove(f"Disconnect the {colour.replace('_', ' ')} breadboard wire from {a} and {b}.", list(JUMPERS[colour]), arrows=[], eye=[eye_cap],
             **(camera_of('Step 9', target=[682.0, 912.0, 1305.0], radius=48.0) if k == 0 else dict(keep_camera=True)))
# 31 -> two (the published 45, 46: RES1 at h27 first)
g.remove('Remove a 12 kΩ Resistor from h27 and the (-) blue rail.', [RES1], arrow_style={RES1: size('res1')})
g.remove('Remove the other 12 kΩ Resistor from h29 and the (-) blue rail.', [RES2], arrow_style={RES2: size('res2')})
```

32 + 3 + 1 + 2 + 1 + 2 + 5 + 1 = 47 steps, as the published (its 47 less the refit's 3, plus our F1 moves back and up, and the LCD in
two steps).

## 4. Trying it: what first, what to check

One heavy job at a time (`df -h /System/Volumes/Data`, `sysctl vm.swapusage` first): the script loads lac-guide.glb (7 MB).

1. `.venv.nosync/bin/python "LAC Build Instructions/deconstruction.py"` (after `guide.py` whenever the Full Build changed). Expected:
   `take_apart(): from steps.json as it ends (57 parts, 25 leads)`, 32 step lines, `... -> 68 views` (Start, 64, Completed View, the two
   parts list pages), `wrote steps-deconstruction.json`.
2. The log. **Expected:** NOTE lines "the Full Build's camera leaves out ..., lying aside" on record-camera steps (9, 14, 26 and the
   like: F1, the LCD, F4 lying aside), and possibly a false "WARNING: ... looks plugged into a part that is lifted" on Step 7 (the LCD's
   GND / VCC male caps lie 1.7 mm from the seated LCD's box). **Not expected:** any "not in its seat: lifted straight up" (every such part
   has a way here: if one appears, a part id or a `where()` is wrong), any "no straight way out".
3. **Check A, the USB cable at Step 4** (the one state the Full Build never had: the plug moving out with the case's insides seated).
   (a) the log has no `WARNING: Disconnect the USB Cable ...: the way out of Step 40 passes through a part still there` (F9's box is
   at x 689 - 720, the plug's below about 685 by the boxes); (b) `tools/motioncheck.py "LAC Build Instructions" --steps
   steps-deconstruction.json "Step 4c"` shows no LCD wire, pot lead or switch lead hit (the LCD's wires turn round F9's back edge 4 - 6 mm
   beside the plug's way; the tan pot lead runs over the Nano Board). If either fails: move the Step 4 block to just after Step 15 (the
   Full Build's Step 40c state exactly: F1 face down in front, the buzzer and the LCD lying wired) and keep Step 1's caution.
4. Serve and look (`/usr/bin/python3 tools/serve.py "LAC Build Instructions" 8793` in the background, then
   `http://localhost:8793/player.html?steps=steps-deconstruction.json`), at 1440 x 900 and 760 x 720, each step as it opens, half-way
   (`_dev.show('Step 12c', 0.5)`) and at its end, in this order of risk:
   - Step 16: four pin labels on pins 2.5 mm apart, plus two eyes. If they overlap, give the four labels `side='right'` (a side of the
     model: the player ranges side labels), or drop the eyes to one.
   - Steps 20 and 27: the two-stage unplugs (each lead blending from plugged to hanging, three at once); the camera keeps holes and
     hanging caps in frame.
   - Step 12: the stage-0 arrow (along the tip, toward the front) drawn and readable; the close-up clear of both arrows; the second
     arrow appears only after the tip has finished (the rest beat).
   - Step 15: the short inward arrows over the tilted tops (at y 965) sit over the tops, not in them; adjust `at=` if the tops are
     elsewhere (they were computed from F7_TAB and the tilt: F7A's tilted top about x 639 - 642, F7B's 708 - 711, y 955 - 957).
   - Step 2: the arrow on the pull reads (see 2.3); the cable stays in the slit while F2 swings and slides.
   - Steps 4 and 6: the frames (cable and A end; F1 standing and laid aside).
   - Step 21: one beat for a quarter turn and 100 mm may be quick. For two: `path=[_shifted(VIEW['Step 47']['carry'][F1]['pose'],
     [0.0, 40.0, 0.0]), BUILD]` with `wire_via={w: [r] for w, r in leads('Step 29c', 'pot').items()}` (the hanging shapes, carried up
     whole with F1, then 41 - 43).
   - Step 23: the Nut turns the unscrewing way (opposite to the Full Build's Step 27), a quarter turn per pose.
   - Step 8: four beats (3.2 s); if too long for Lee, the Full Build's Step 51 had the same four.
5. The run-through on that page: `(0, eval)(await fetch('js/runthrough.js').then(r => r.text())); _dev.freeze(); _runthrough()`.
6. Wires: `.venv.nosync/bin/python tools/motioncheck.py "LAC Build Instructions" --steps steps-deconstruction.json --moments 39` (all
   moving views; heavy: alone), then `.venv.nosync/bin/python tools/wirecheck.py "LAC Build Instructions" steps-deconstruction.json`.
   A clash that the Full Build's own step has, mirrored in time, is not new (Step 14 = Step 43's 50 ms brush, README question 11). A new
   one in a grouped step (16, 20, 27, 29): split that group in the Full Build's reverse order (section 3's code) before anything else.
7. If Lee's Step 45 changes before this is run: run guide.py, then this; the F9 assert says if its way has changed shape (then
   `path=[HOOKED, *TIPPED]` and the `then=` list need its new stops).
8. Later rounds: keep a copy of steps-deconstruction.json and diff every view's camera after each edit (memory: keep step cameras).
9. For Lee's review: once guides.json has the entries (section 7, Lee's word on the names), `python3 tools/publish.py
   lcd-alarm-clock-deconstruction --to "share/Test guides preview"`, served on 8799; never live without Lee. The website card is the Full
   Build's (`_dev.card()` copies it): the LAC has no `cards/` folder yet, so the Full Build's card comes first.

## 5. The README section to add (LAC Build Instructions/README.txt)

At the top, after the FIRST DRAFT line:

    DECONSTRUCTION, FIRST DRAFT 21 Oct 2026 (deconstruction.py -> steps-deconstruction.json; see THE DECONSTRUCTION below).

A section after THE BUILD (and before WHAT WAS DONE WITH THE STEP):

    THE DECONSTRUCTION (32 numbered steps; first draft 21 Oct 2026, Lee: "we need to make a deconstruction guide for this LAC as well.
    Here is the published version of the guide that we need to convert / remake here: instructions.online/?id=19075-lac_deconstruction").
    TechBox's published take-apart (47 steps) remade on our Full Build: its order where our model allows it, every step its own caption,
    each arrow the published one's size, parts that went on one at a time and go together off together (as the PMG's and LSM's). It opens
    on the Full Build's title page, ends on F3 with the breadboard (stuck on for good, as published), followed by the Full Build's parts
    list; its website card is the Full Build's. Every step replays a state of the Full Build backwards, so each wire keeps a shape the Full
    Build drew for that state. The plan and its reasons: docs/research/lac/decon/plan.md.
    - Steps 1 - 4: F6, F2 (the USB cable back out of its slit as F2 swings out and slides off), F5 (Step 1's caution: disconnect the USB
      cable from the computer first; the closed case holds its plug); then the USB cable, as soon as its plug can come out.
    - Steps 5 - 10: F1 pulled forward and laid face down aside, still wired; the LCD Screen out of F9's notches (a close-up of them), then
      out of the case and laid face down, still wired (two steps, as the Full Build brought it in); F8; F4 lifted off with the switch and
      laid behind the case, still wired.
    - Steps 11 - 15 (the Full Build's Steps 47 - 41 backwards): F1 back in front of the breadboard; F9 tipped, then lifted (an arrow for
      each, in turn; a close-up of its front foot under F3); the F7s spread; the buzzer lifted out to lie beside the case, still wired; the
      F7s let close, then pulled out.
    - Steps 16 - 19: the LCD's four wires off both ends (labelled GND, VCC, SDA, SCL on its pins, as published), the LCD; the buzzer's two
      leads, the buzzer.
    - Steps 20 - 25: the Potentiometer's three leads (each hangs from it, as before the Full Build plugged it in); F1 picked up and held
      upright; on its own: the Knob, the Nut (unscrewed), the Washer, and the Potentiometer pushed out of F1's back.
    - Steps 26 - 32: the orange and yellow breadboard wires; the switch's three leads, the switch pushed out of F4 (on its own); the other
      six breadboard wires; the Real Time Clock; both resistors; the Nano Board.
    - Not taken from the published guide: putting the Washer, Nut and Knob back on the Potentiometer for storage (its Steps 16 - 18:
      nothing is refitted); its views turned on their side (F2, the Potentiometer: our player keeps up as up); its fades between copies of
      a part in two places (here the parts move); its order where it would pass our wires through each other (the Potentiometer's and the
      LCD's wires before the buzzer is out; the orange breadboard wire last).
    - Checked: (fill in after the run: the log, the run-through's view count, motioncheck / wirecheck, the widths looked at).

QUESTIONS FOR LEE, continued from 12 (section 8 below, in the README's words).

FILES, add:

    deconstruction.py             the take-apart (run it after guide.py: .venv.nosync/bin/python "LAC Build Instructions/deconstruction.py")
    steps-deconstruction.json     generated by it; do not edit by hand

## 6. The CLAUDE.md lines to add

1. Commands block, after the PMG's line (the LSM's is missing there too; add both):

        .venv.nosync/bin/python "LSM Build Instructions/deconstruction.py"            # (the LSM's, likewise, after its guide.py)
        .venv.nosync/bin/python "LAC Build Instructions/deconstruction.py"            # (the LAC's, likewise, after its guide.py)

2. "A kit's guides", the deconstruction bullet's first line: "(the MRA's and the RCC's, first drafts 18 Oct 2026; the PMG's and the
   LSM's, 21 Oct 2026)" becomes "(the MRA's and the RCC's, first drafts 18 Oct 2026; the PMG's, the LSM's and the LAC's, 21 Oct 2026)".
3. A paragraph after the LSM's ("... it ends on D1 with the breadboard, then the Full Build's parts list. Run it after every Full Build
   change."):

        The LAC's (`deconstruction.py`, 32 steps, first draft 21 Oct 2026: Lee's "convert / remake" of TechBox's published take-apart,
        19075-lac_deconstruction, 47 steps): its order where our model allows it, every step a state of our Full Build replayed backwards
        (so every lead keeps a shape the Full Build drew: no route drawn anew). F6, F2 (the USB cable walked back out of its slit), F5; the
        USB cable as soon as its plug can come out (Step 1's caution, as the LSM's); F1 pulled forward and laid aside, still wired; the LCD
        Screen out of F9's notches, then out of the case to lie face down, still wired (the Full Build's two steps); F8; F4 with the switch
        lifted off and laid behind the case, still wired; the Full Build's Steps 47 - 41 reversed (F1 back in front of the breadboard, F9
        tipped and lifted, the F7s spread, the buzzer out to lie beside the case, the F7s out: the buzzer must be out before any lead near
        it moves); then each wired part as the Full Build wired it, reversed, in groups (Lee's PMG and LSM rule): the LCD's four wires (the
        published GND / VCC / SDA / SCL labels) and the LCD, the buzzer's leads and the buzzer, the Potentiometer's leads (each cap on to
        hang from it, `to_hanging()`), F1 picked up and held upright and the Potentiometer taken apart on its own (Knob, Nut, Washer, out
        of F1), the orange and yellow wires (before the switch's leads; the published takes them last, where purple, blue and green lift
        through orange), the switch's leads and the switch out of F4 on its own, the other six breadboard wires; the Real Time Clock, both
        resistors, the Nano Board; it ends on F3 with the breadboard, then the Full Build's parts list. Not mirrored: the published storage
        refit (its Steps 16 - 18), its rolled views (2, 12 - 18), its cross-fades between posed copies. Arrows the published sizes
        (docs/research/lac/decon/published_geometry.md), in turn for F9 and the F7s. Run it after every Full Build change.

4. Layout, the `LAC Build Instructions/` entry, after "Research: docs/research/lac/.": "deconstruction.py -> steps-deconstruction.json
   (the take-apart, made from the Full Build: first draft 21 Oct 2026; docs/research/lac/decon/)."
5. Publishing, "the names in `guides.json` (Lee's: ...)": add `lcd-alarm-clock-full-build`, `lcd-alarm-clock-deconstruction` once Lee
   has named them (question 22).
6. Rulebook section 11: nothing until Lee rules on the questions (the in-house rules applied here are all already there).

## 7. guides.json (for Lee's word; the LAC has no entry yet, its Full Build neither)

    "kits":   "lcd-alarm-clock": {"name": "LCD Alarm Clock", "code": "LAC", "folder": "LAC Build Instructions"}
    "guides": "lcd-alarm-clock-full-build":     {"kit": "lcd-alarm-clock", "steps": "steps.json", "label": "Full Build"},
              "lcd-alarm-clock-deconstruction": {"kit": "lcd-alarm-clock", "steps": "steps-deconstruction.json", "label": "Deconstruction",
                                                 "script": "deconstruction.py"}

## 8. Questions for Lee (README numbering, after 12)

13. One wire per step, as the published (47 steps), or in groups as the PMG's and LSM's (32 steps: the LCD's four wires at once, each
    part's leads at once, orange and yellow together, the other six breadboard wires together, both resistors)? The draft groups.
14. The USB cable at Step 4 (power first, as soon as its plug can come out; Step 1 says to disconnect it from the computer), or where the
    published has it, after F9?
15. The order after F4: the published unplugs the Potentiometer, then the LCD, then takes F9, the USB cable, the F7s and the buzzer;
    ours takes F9, the F7s and the buzzer out first, then the LCD's wires, the buzzer's, the Potentiometer's, as our Full Build put
    them in, reversed. In the published order our Potentiometer's and LCD's wires would pass through the buzzer's black wire. Fine?
16. The Potentiometer: our F1 lies face down (knob down) where the published lies face up, so the draft moves F1 back in front of the
    breadboard, unplugs its three wires (each left hanging from the Potentiometer), then picks F1 up and holds it upright to take off the
    Knob, Nut and Washer, as the Full Build put them on. Two steps more than the published. Or take it apart where it lies, shown upside
    down?
17. The published puts the Washer, Nut and Knob back on the loose Potentiometer for storage (its Steps 16 - 18). Left out (your rule:
    nothing refitted). A note card at the end instead ("Put the Washer, Nut and Knob back on the Potentiometer to store it")?
18. The LCD Screen out in two steps (out of F9's notches; then out of the case and laid down, as the Full Build brought it in), or one
    (as published, a 6-beat step)?
19. The GND / VCC / SDA / SCL labels on the LCD's wire step (the published guide's only text): keep?
20. An arrow per stage, in turn, cannot be combined with a wire that changes shape stage by stage (F2 with the USB cable, F4 with the
    switch's wires, the buzzer, the LCD): those steps have one arrow. A small generator change would allow both (study_api.md 3.4); it
    touches every kit. Want it?
21. The LCD Screen and the Alarm Buzzer, once off their wires, lift 30 mm and fade with an eye on them (published: they fade where they
    lie). Fine?
22. The website address: lcd-alarm-clock-deconstruction (with the kit lcd-alarm-clock and lcd-alarm-clock-full-build, question 7)?
