# LSM deconstruction: the final plan (21 Oct 2026)

Made from the four studies (`study_build_map.md`, `study_generator.md`, `study_published.md`, `study_conventions.md`) and the
three plans (`plan_A_published.md`, `plan_B_reverse.md`, `plan_C_generator.md`) in this folder, with every point where they
disagree checked against `LSM Build Instructions/guide.py`, `steps.json`, `assembly-report.json`, `tools/stepgen.py` (working
tree), `player/js/player.js`, the MRA, RCC and PMG deconstruction scripts and the rulebook. Nothing was run except small Python
scripts reading JSON; this file is the only thing written. "FB N" is Full Build Step N; a bare step number is the
deconstruction's.

## 1. In short

- **24 steps** for the Full Build's 40 (0.60; the rulebook's range is 0.45 - 0.82, `docs/cadasio-patterns.md:242`), ending on D1
  with the breadboard stuck to it (as TechBox's published take-apart ends), then the Full Build's two Parts List pages
  (`take_apart(parts_list_at_end=True)`, as the MRA's and PMG's). Title page and website card: the Full Build's.
- **Order: the Full Build in reverse** (plans B and C), the house rule for a first draft (`cadasio-patterns.md:245-258`). Every
  state the guide passes through, and every wire shape, is one the Full Build already shows; no new wire shape is drawn. The
  only new moves are rigid ones (a part and every wire end on it moving by the same shift), so nothing can bend into a part.
- **Groups (Lee's "removed in groups")**: all 64 stems in one step; the four D11 posts in one step; both D9 in one step; both of
  the button's leads unplugged in one step; and the three breadboard wires in two group steps, as the PMG did its wires the same
  day: the LED matrix pulled off all three sockets at once, then all three wires out of i2, i3 and b19 at once, both ends, with
  the wires (`PMG Build Instructions/deconstruction.py:175-186`; rulebook `cadasio-patterns.md:256-257`, "or in phases").
- **Captions in TechBox's own wording for the MRA's deconstruction** ("Remove X from Y.", "Disconnect X from Y.", part names as the
  parts list has them: `MRA Build Instructions Prototype/step-text-deconstruction.json`), the yellow wire called yellow.
- **What must be given by hand** (the generator's defaults are wrong here; all verified in `stepgen.py`): BACKING (put away),
  D4, the push button, its nut, D10, the four D11 posts, the three sockets, the USB cable's A end, and every move of the matrix.
- **One dependency to settle before committing**: Step 19 uses `remove(..., let_go=...)`, which is in the working tree's
  `tools/stepgen.py` only (uncommitted, the PMG session's: `stepgen.py:927-928, 977-993, 1185-1188, 1731-1735`). The LSM script
  must not be committed before that change is, and its commit must not carry that change unless Lee says so. A fallback that
  needs no `let_go` is given (Step 19, fallback).

## 2. The facts that decided between the plans

1. **BACKING comes back unless it is put away.** `take_apart()` adds every part any Full Build view showed (`stepgen.py:874-880`).
   BACKING's last view is FB 1c, riding BREADBOARD at `[0, -40, 0]` (steps.json; `guide.py:276-286`), so it would sit 40 mm under
   the seated breadboard, through D1 and below the table, in every step. `g.put_away([BACKING])` straight after `take_apart()` hides
   it (`stepgen.py:1217-1227, 1698-1708`); the cost is that Step 1 opens without a glide from the title page (a cut). All plans agree.
2. **A jumper wire moves with its pin except its last 6 mm.** Every jumper route from route 33 on has `b_from` = length - 6
   (`guide.py:264-265`; route 33: `b_from` 150.2 of about 156 mm), and the player moves a point before `b_from` wholly with the
   wire's first end (`player.js:122-133`). So a pin pulled up alone drags its whole wire up with it. In the BESIDE shape the wire's
   last run lies under the matrix, so **plan A's Step 20 (pins up 30, sockets slid along their pins, the matrix still there) drags
   each wire up through the matrix board**, not "a little stretch". Only moves where both ends of a wire shift alike (rigid) are safe
   without new shapes. This is why the matrix comes off the sockets first (Step 19), then all six ends go up together (Step 20).
3. **The matrix can only lie where the Full Build drew its wires**: HELD over the box (routes 59-61), OUTSIDE D4 with the wires
   over D4's top edge (53-55), BESIDE the base (33-35). Checked against the part boxes: BESIDE's wires pass through D5's place
   (route 33, the yellow wire, crosses x 679.5 - 682.5 at y 875 - 877, inside D5's height, 856 - 907; the purple, route 35, at y 892 - 894)
   and through D9_B's (routes 33 and 34 cross x 655.8 - 658.8 at y 895 - 897, inside D9_B's 882 - 900.7), so BESIDE
   needs D5 and both D9 off; OUTSIDE blocks D4 (wires over its edge, `guide.py:659-676`); HELD blocks the D9 (the matrix's underside
   is at y 949.7 there, a D9 would rise to 965.7; both D9 are under the matrix in x). Hence the order: matrix to HELD, D10 off, matrix
   to OUTSIDE, D9 off, D5 and D3 off, matrix back to BESIDE, D4 off.
4. **The USB plug and the purple pin come late.** USB_B's way out (+Z 25, FB 23 reversed) meets the seated button after 9.2 mm
   (USB_B box top z 1224.46, BUTTON box bottom z 1233.65, overlapping in x and y: `assembly-report.json`), so D2 must be out first;
   D2's end tabs go through closed slots in D4 and D5, so D4 and D5 must be off first. The purple pin in b19 sits under the plug's
   leg (their boxes overlap 6.3 mm in height; README question 2, `guide.py:644`), so the three wires come after the USB cable.
5. **Generator defaults that are wrong, all confirmed in `_takeoff` (`stepgen.py:953-1205`)**:
   - D4: its latest record is FB 31's stand-still way (`paths={D4: [ZERO]*3}`, `guide.py:756-757`), which fits once D10 is gone
     (`stepgen.py:1011-1016`): no motion, and FB 31's camera. Hand path from FB 25.
   - BUTTON: its latest fitting record is FB 20's stand-still `TWO_BEATS` (`guide.py:553-554`), so it would not move. **A hand path
     is a pose relative to the seat, not an offset from where the part is** (`stepgen.py:911, 1003`), so the way out is
     `[0, 0, 157.1]` (D2 out by 57.1, plus FB 19's 100), not `[[0, 0, 100]]` as `study_build_map.md` item 3 says.
   - NUT alone does not fit its only record (group NUT + BUTTON, `stepgen.py:1012`), so it would be pulled straight up with a
     WARNING and a Review note (`stepgen.py:1038-1044`).
   - D10, the three sockets and the four D11 posts only ever rode (FB 15 - 17 and 34 - 36 move nothing, FB 31 only D4's still way), so
     they have no record: straight up, unchecked, with a Review note; `unplug()` of a socket raises (`stepgen.py:1034-1035`).
   - `lift()` never changes a lead's route by itself; without `wires=` the in-box wires would stay put while their sockets moved.
   - USB_A was only `show=`n (FB 23): no record; given a hand path.
6. **Riding parts are never obstacles in the order check** (`stepgen.py:995, 1060`), so plan A's worry that D5's order check would
   flag D10's tab is unfounded; D10's end also only pokes 0.4 mm past D5's outer face along X (D10 hi x 682.91, D5 hi x 682.51), so D5
   slides off it whatever the order.
7. **Lee's rules that settle the smaller disagreements** (`cadasio-patterns.md:226-243, 277-283`, `CLAUDE.md:351`): an arrow along
   the longest stage of the way unless Lee asks for another stage; two steps on one sub-assembly in the hand keep one camera; a
   sub-assembly taken apart on its own (`alone=`), the rest hidden, then the guide returns to the main model; a cable unplugged and
   removed has one arrow, on the plug, clear of the cable; a plug moved on its lead an eye; several ends at once an eye each; leads
   unplugged after the structure that the build put round them after plugging them in.

## 3. Script: `LSM Build Instructions/deconstruction.py`

Never `import guide`: `guide.py:826` calls `g.build()` on import and would rewrite `steps.json` and `parts.json`. Everything needed
is read from `steps.json`.

```python
"""Laser Stem Matrix (LSM), deconstruction: the finished kit taken apart, down to D1 with the breadboard on it. A guide of its own
(steps-deconstruction.json), made from the Full Build as guide.py last wrote it (run that first, and this again after any change
to it). First draft (21 Oct 2026): the Full Build in reverse (rulebook section 11), some parts in groups (Lee): the 64 stems, the
four D11 posts, both D9, the button's two leads, and the three breadboard wires (the LED matrix pulled off their sockets, then the
wires out of the breadboard together, as the PMG's). The LED matrix stays wired until the end, so it is carried back the way the
Full Build brought it: out of the box, over D4, and back beside the base so that D4 can come off."""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
from stepgen import Guide, _shifted, apply_pose, compose, via  # noqa: E402

D1, D2, D3, D4, D5, D6, D7, D8, D10 = 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D10'
D9_A, D9_B = 'D9_A', 'D9_B'
D11S = ['D11_A', 'D11_B', 'D11_C', 'D11_D']
BREADBOARD, BACKING, NANO, R12K, R330, CAP, MATRIX = 'BREADBOARD', 'BACKING', 'NANO', 'R12K', 'R330', 'CAP', 'MATRIX'
BUTTON, NUT, RED_PIN, BLACK_PIN = 'BUTTON', 'NUT', 'BTN_RED_PIN', 'BTN_BLACK_PIN'
USB_B, USB_A = 'USB_B', 'USB_A'
PINS = ['J_WHITE_M', 'J_GREY_M', 'J_PURPLE_M']                      # (in i2, i3, b19; the 'white' wire is drawn and named yellow)
SOCKETS = ['J_WHITE_F', 'J_GREY_F', 'J_PURPLE_F']                   # (on V+, V-, IN)
STEMS = [f'STEM_{k:02d}' for k in range(1, 65)]
DIAG = [-0.5792, 0.5736, -0.5792]                                   # (the Full Build's usual corner, guide.py:121)

FULL = json.loads((HERE / 'steps.json').read_text(encoding='utf-8'))
VIEW = {v['name']: v for v in FULL['views']}
ROUTES = FULL['routes']

# camera_of(step, moved=None), leads(step, prefix), full_way_back(step, part, then=()): copied from the MRA's script
# (MRA Build Instructions Prototype/deconstruction.py:55-60, 63-65, 92-99), unchanged.


def slid(pose, by):
    """A Full Build pose moved on by a pure shift (D2 slid out): only t changes, and a via() stays a via() (_shifted drops it)."""
    if isinstance(pose, dict):
        return type(pose)(dict(pose, t=[round(a + b, 3) for a, b in zip(pose.get('t', [0.0, 0.0, 0.0]), by)]))
    return [round(a + b, 3) for a, b in zip(pose, by)]


def carried_back(step, part, prefix):
    """A Full Build step that moved `part` only by riding on the breadboard (FB 26, 30: the LED matrix), walked back for lift():
    its stops reversed (each a beat), its wires back through the Full Build's own shapes, a stage a beat."""
    done = VIEW[step + 'c']
    c = done['carry'][part]
    assert c['by'] == BREADBOARD                  # (in its seat: the poses of the ride are where the matrix is)
    stops = [VIEW[step]['carry'][part]['pose'], *(c.get('via') or []), c['pose']]
    stages = {w: [ROUTES[n] for n in nos[::-1]] for w, nos in done['wire_via'].items() if w.startswith(prefix + ' ')}
    assert all(len(r) + 1 == len(stops) - 1 for r in stages.values()), (step, len(stops))
    return dict(path=stops[::-1][1:], wire_via=stages, wires=leads(step, prefix))


g = Guide(HERE, title='Laser Stem Matrix (LSM)', part='Deconstruction', names=dict(FULL['names']),
          steps_file='steps-deconstruction.json', source='lsm.glb', hero_azimuth=45,
          copyright_line='© TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')
g.take_apart(parts_list_at_end=True)                                # (the Full Build's parts list after the Completed View, as the MRA's)
g.put_away([BACKING])                                               # (peeled off in FB 1 and never back: take_apart() would show it under D1)

# where(i): copied from the MRA's script (deconstruction.py:108-113).
# ... the 24 steps of section 4 ...
g.build()
```

Notes on the set-up:
- `source='lsm.glb'` is required (the default is `mra.glb`, `stepgen.py:625`); `hero_azimuth=45` as the Full Build
  (`guide.py:92`). `FULL['names']` already holds the hover names ("Yellow Breadboard Wire", "Push Button", "D9", "D11"), so no
  `hover_names=` is needed.
- The decon shows no part the Full Build does not, so `_sync_model` (`stepgen.py:2365-2379`) does not rebuild `model.glb`, and the
  Full Build's card stays valid.

## 4. The steps

In the calls, `c` stands for the step's caption, given above each. "Default" = the generator's own choice: the Full Build's way
in, reversed, by that step's camera. Arrows are checked against the
camera rule (an arrow becomes an eye if |direction . camera dir| > 0.8, `stepgen.py:1424-1425`): none of the 24 does.

### A. From the top: stems, shelves, posts (undoes FB 40 - 33)

**1. "Remove all 64 LED Stems from D8, D7 and D6."**
`g.remove(c, STEMS, units=[STEMS], caution='Unplug the USB Cable from the computer or power supply before you begin.')`
- Undoes FB 40 + 39 ("one, then the rest" merged). Default way up 44, STEM_CAMERA (FB 40). `units=` gives one arrow (without it,
  two: one per FB step); with the stems spread out it starts on the stem nearest their middle (`stepgen.py:1414-1418`).
- The caution is a draft (question 3): the USB plug itself cannot come out until Step 15 (fact 4).

**2. "Remove D8 from the four D11 posts."** `g.remove(c, [D8])`. FB 38 reversed: up 55, SHELF_CAMERA.
- D8 passes the posts' top latches as in FB 38 (README question 17: the CAD's D8 slots are short of the latch heads).

**3. "Remove D7 from the four D11 posts."** `g.remove(c, [D7])`. FB 37 reversed: up 65, SHELF_CAMERA.

**4. "Push the tabs of the four D11 posts up out of the slots in D1, then remove the posts from D6."**
```python
g.remove(c, D11S, paths={i: [[0.0, 6.38, 0.0], [0.0, 85.0, 0.0]] for i in D11S}, keep_camera=True,
         inset=dict(target=[674.83, 857.0, 1166.2], dir=[0.4109, -0.8401, 0.3541], radius=6.0, mark=2.5,
                    caption='Push each tab up out of D1', alt='Close-up from below of a D11 tab through its slot in D1'))
```
- Undoes FB 36 + 35 + 34 (all four at once: Lee's groups; FB 36 already moved all four together). Two beats: the tab out of D1
  (FB 36 reversed, `D11_SHORT`), then up out of D6 (FB 34 / 35 reversed, `D11_UP`, `guide.py:802`).
- By hand because the posts only rode D1 (no record; default = straight up, unchecked, Review note). `paths=` per post gives an
  arrow on each, as the MRA's six base screws (Lee); the log notes "4 arrows" (expected).
- Camera kept from D7 (no jump; D6's step next uses nearly the same one). FB 36's own camera is from below (flipped) and would turn
  the upward arrows into eyes (0.84 > 0.8); FB 34 / 35 each frame one pair.
- The close-up is FB 36c's own (target, from-below direction and radius: `guide.py:811-814`), with a red box on the tab (D11_B's,
  at the D5 / D3 corner). The Full Build's see-through D1 and D5 cannot be repeated: takeoff steps have no `ghost`.

**5. "Remove D6 from the tabs at the top of the walls."** `g.remove(c, [D6])`. FB 33 reversed: up 64, FB 33's camera.

### B. The LED matrix out of the box, still wired (undoes FB 32 - 29)

**6. "Lift the LED Matrix, with D10 hooked under it, up out of the box and hold it over the box. Keep its three wires connected."**
```python
g.lift(c, [MATRIX], wire_via={w: [ROUTES[n] for n in nos[::-1]] for w, nos in VIEW['Step 32c']['wire_via'].items()},
       wires=leads('Step 32', 'wire'))
```
- Undoes FB 32. Default way (seat, through P_HALF without a pause, to P_HELD: one beat) and FB 32's camera; D10 and the sockets
  ride along. Wires: SEATED (65-67) through HALF (62-64) to HELD (59-61), the Full Build's blend played backwards (two legs, two
  wire stages, as FB 32). Default arrow up, from above the matrix (never under it: `lee_notes_2026-10-19b.md:41`).

**7. "Slide D10 toward D2 until its hooks release the edges of the LED Matrix, then remove it."**
```python
g.remove(c, [D10], path=[compose(where(MATRIX), VIEW['Step 31c']['carry'][D10]['via'][0], g._pivot(D10)),    # (+Z 40: unhooked)
                         compose(where(MATRIX), VIEW['Step 31']['carry'][D10]['pose'], g._pivot(D10))],     # (then down 22)
         arrow_style={D10: dict(at=[round(float(x), 2) for x in apply_pose(where(D10), [[599.5, 880.0, 1207.0]])[0]])},
         **camera_of('Step 31'))
```
- Undoes FB 31 (`guide.py:751-760`): two beats, along +Z 40 then down 22, relative to the matrix at P_HELD. D10 must go here:
  the OUTSIDE and BESIDE wire shapes were drawn without it, and it would lie across them.
- The arrow's tail (world about `[599.3, 936.6, 1206.7]`) is FB 31's arrow spot moved to D10's other face: D10's D4 end, outside
  the matrix (x < 606.7), 3 mm below D10's lower edge, just past its +Z face (D10 is a plate at z 1202.97 - 1205.97); it points +Z
  along the longest stage. Plan A's `[590.0, 892.0, 1204.5]` is beyond D10's end (x from 594.0); FB 31's own arrow, reversed
  tail-for-head, would point into D10 from behind.

**8. "Carry the LED Matrix over D4 and set it down outside the box, LEDs up, with its wires over the top edge of D4."**
`g.lift(c, [MATRIX], **carried_back('Step 30', MATRIX, 'wire'), **camera_of('Step 30'))`
- Undoes FB 30: path P_LIFT, P_OUTSIDE (two beats), wires HELD -> LIFT (56-58) -> OUTSIDE (53-55). HELD_CAMERA, which Step 9 also
  uses (no jump). The matrix now moves itself where in the Full Build it rode, paced by D4's still way; two stops against two wire
  stages keep pace the same way. Default arrow along the first stage (over D4), from the matrix's D4 side.

**9. "Remove both D9 pieces from the slots in D2 and D3."** `g.remove(c, [D9_A, D9_B])`.
- Undoes FB 29: up 65, HELD_CAMERA, an arrow on each (two of a kind, not touching: `stepgen.py:1141-1143`). They rise away from
  the wires under D9_A's end and from the capacitor under D9_B's edge.

### C. The walls, and the matrix moved round to the D5 end (undoes FB 28 - 25)

**10. "Turn the box over. Remove D5 from the tabs of D1, D2 and D3."** `g.remove(c, [D5])`.
- Undoes FB 28: +X 42 by FB 28's turned-over camera (the RCC's "Turn the car over. Slide L6 out." pattern). D5 is off before
  BESIDE (fact 3).

**11. "Swing the free end of D3 away from the box, then slide D3 out of the slots in D4."** `g.remove(c, [D3])`.
- Undoes FB 27: the two-stage way reversed (22 degrees about the hinge at D4, then 40 mm along the tilt, away from D4: a two-stage
  joint undone in one step, `cadasio-patterns.md:237`), still turned over, by FB 27's camera. The arrow follows the longest stage,
  the slide (Lee's rule); `arrow_style={D3: dict(stage=0)}` puts it on the swing if Lee prefers.

**12. "Turn the box right side up. Carry the LED Matrix back over D4, turning it around, and set it down beside the open end where
D5 was."**
```python
g.lift(c, [MATRIX], **carried_back('Step 26', MATRIX, 'wire'), eye=[MATRIX],
       arrows=[dict(tail=[585.0, 862.4, 1133.0], head=[690.0, 862.4, 1133.0], normal=[0, 1, 0], part=D1, width=5.0)],
       **camera_of('Step 26'))
```
- Undoes FB 26: four beats (P_UP_OUTSIDE, P_MID turned 90, P_UP_BESIDE turned 180, P_BESIDE), wires OUTSIDE -> UP_OUTSIDE ->
  MID -> UP_BESIDE -> BESIDE (routes 52/51/50, 49/48/47, 46/45/44 reversed, then 33-35). D4 cannot come off with the wires over
  its edge. The scene is FB 26's exactly (D2 and D4 on, no D3, D5, D9, D10, D6), so the Full Build's checked shapes hold.
- Cues: FB 26's own arrow on the table beside D3's place (Lee-approved, "as the published guide's Step 23"), tail and head swapped,
  and its eye on the matrix (`guide.py:700-704`), by FB 26's top-down camera.
- The highest motion risk: the only walk-back with turned poses, the matrix now the mover. motioncheck first, and look at Step 12c
  half way.

**13. "Slide D4 off the tabs of D1 and D2, then lift it off the USB Cable."**
`g.remove(c, [D4], path=full_way_back('Step 25', D4), **camera_of('Step 25'))` -> `[[-8, 0, 0], [-8, 65, 0]]`, BASE_CAMERA.
- Undoes FB 25. By hand because of fact 5 (D4's stand-still record). The notch in D4's foot is open below, so D4 slides along the
  cable and lifts off it (`guide.py:597, 630-636`). Default arrow along the lift (the longest stage).

### D. The push button and the USB cable (undoes FB 24 - 19)

**14. "Slide D2, with the Push Button, off the tabs of D1. Keep the Push Button's wires connected."**
`g.lift(c, [D2], wires=leads('Step 24', 'lead'), arrow_style={D2: dict(at=[638.2, 912.0, 1256.0])})`
- Undoes FB 24: default way +Z 57.1 to where FB 21 - 23 had D2, BASE_CAMERA; BUTTON and NUT ride along; the leads go back from
  routes 42/43 to 38/39. The USB plug and the leads' unplug poses need D2 there (fact 4; FB 21 - 22's pin poses are drawn for it).
- The arrow sits 5 mm above D2's top edge, just past its outer face: D2's outer face is turned away from the camera, so a default
  arrow would start behind D2.

**15. "Disconnect the USB Cable from the Nano Board."**
`g.remove(c, [USB_B, USB_A], units=[[USB_B]], paths={USB_A: [[0.0, 0.0, 25.0]]}, arrow_scale=2.0)`
- Undoes FB 23: the plug +Z 25 (default), BASE_CAMERA. The A end moves the same 25 mm, so the cable moves whole and cannot bend into
  anything (D4 is off, D2 is 57 mm out, the cable stays above D1 and the breadboard). One arrow, on the plug, clear of the cable
  (RCC rule); twice the size, as Lee had the MRA's USB arrow (`cadasio-patterns.md:234`; MRA script line 125).

**16. "Disconnect the Push Button's red wire from j5 and its black wire from j16."**
`g.unplug(c, [RED_PIN, BLACK_PIN], caution='Pull each wire out by its connector. Do not pull on the wires themselves.', **camera_of('Step 21'))`
- Undoes FB 22 + 21 (both at once: a group). Defaults are right only because D2 is where FB 21 - 22 had it: each pin back to its
  laid-out pose, leads 38 -> 36 and 39 -> 37, an eye on each pin, and each pin rides the button from then on (its `rode`, FB 20c).
  FB 21's camera (radius 40) holds both holes; FB 22's (the default) is closer on j16.
- Both leads change shape at once where the build changed one at a time: motioncheck.

**17. "Unscrew the nut from the back of the Push Button, on the inside of D2, and slide it off over the wires."**
```python
D2_AT = where(D2)                                                   # ([0, 0, 57.1]: D2 as Step 14 left it)
NUT_WAY = [slid(p, D2_AT) for p in full_way_back('Step 20', NUT)]  # (FB 20's quarter turns, reversed: two turns off, unscrewing)
NUT_WAY[3] = dict(NUT_WAY[3])                                       # (after one turn: a stop, so that the two turns take two beats)
g.remove(c, [NUT], path=NUT_WAY, alone=[D2, BUTTON, NUT, RED_PIN, BLACK_PIN],
         arrow_style={NUT: dict(at=[round(float(x), 2) for x in apply_pose(where(NUT), [[649.24, 882.63, 1250.3]])[0]])},
         **camera_of('Step 20', moved=D2_AT))
```
- Undoes FB 20, the sub-assembly on its own (`alone=`; RCC rule). FB 20's way reversed (`guide.py:552`): from tight against D2 to
  60 mm back, eight quarter turns the way that unscrews (clockwise from the head, as Lee asked for the build). `NUT_WAY[3]` is the
  pose after one whole turn (z -30); making it a stop gives two beats, as FB 20 had, so the hexagon does not seem to turn backwards.
- The arrow's tail is where Lee put the build's nut arrow (FB 18, `guide.py:547`: from the nut's rear face, 1 mm up, clear of the
  black lead), moved with D2 (world about `[649.24, 882.63, 1307.4]`); its length is the generator's (15 - 40 mm rule).
- FB 20's camera moved with D2 (from inside D2, where the nut is).

**18. "Push the Push Button out through the hole in D2, its wires following it."**
```python
g.remove(c, [BUTTON], path=[slid(p, D2_AT) for p in full_way_back('Step 19', BUTTON)],    # ([0, 0, 157.1])
         alone=[D2, BUTTON, RED_PIN, BLACK_PIN], keep_camera=True,
         arrow_style={BUTTON: dict(at=[round(float(x), 2) for x in apply_pose(where(BUTTON), [[649.23, 882.63, 1219.0]])[0]])})
g.put_away([D2])                                                    # (what is left of the sub-assembly taken apart in the hand)
```
- Undoes FB 19: +Z 100 from where it is. The pins ride the button, so they and both leads leave with it, rigidly, back through
  the hole the way FB 19 brought them.
- One camera with Step 17 (Lee's rule for two steps on one sub-assembly in the hand). From inside D2 a default arrow would start
  past the button's head, behind D2, so it is placed inside: tail beside the button body, 2.5 mm clear of it on the side away from
  the leads (world about `[649.23, 882.63, 1276.1]`), pointing out towards D2.

### E. The LED matrix off its wires, the wires, the breadboard parts (undoes FB 17 - 3)

**19. "Pull the LED Matrix off the connectors of the yellow, grey and purple wires, and remove it."**
```python
OFF = compose(where(MATRIX), [0.0, 0.0, -15.0], g._pivot(MATRIX))   # (15 mm back along its pins: off the sockets, as SOCKET_OFF)
AT = np.mean([apply_pose(where(s), [g._pivot(s)])[0] for s in SOCKETS], axis=0)   # (about [757.9, 872.7, 1232.1], under the matrix)
g.remove(c, [MATRIX], let_go=SOCKETS, path=[OFF, _shifted(OFF, [0.0, 30.0, 0.0])], arrow_style={MATRIX: dict(stage=0)},
         caution='Pull the LED Matrix away from the connectors. Do not pull on the wires themselves.',
         inset=dict(target=AT.round(2).tolist(), dir=[0.3, -0.8, 0.52], radius=10.0, mark=5.0,
                    caption='The three connectors on the V+, IN and V- pins', alt='Close-up from below of the three wires\' connectors on the pins at the corner of the LED Matrix'),
         **camera_of('Step 23'))
```
- Undoes FB 17 - 15 as one group (the three sockets come off together; in the PMG's way, the device off its wires' caps, which
  stay where they lie: `let_go`). Two beats: the matrix slides 15 mm back along its pins (`SOCKET_OFF` reversed, `guide.py:224`;
  world +Z, as the matrix lies turned half round), then lifts 30 and goes. The wires do not move (their ends do not), so nothing
  can pass through anything. The arrow is on the slide (`stage=0`): that is the action; the lift is only the way out of view.
- The sockets are under the matrix and hidden from above, so a close-up from below (rulebook: a part the camera cannot see gets a
  close-up from the other side), with one red box round the three. The target is computed, not typed (plan A's z 1228.0 is 4 mm off).
- Camera: FB 23's BASE_CAMERA, which showed this very scene (matrix beside the base) and sees b19 from the row-a side; the step
  opens afresh anyway after the `put_away([D2])`. Fallback if the pins look too small at radius 125: `view_dir=DIAG,
  frame=([680.0, 885.0, 1210.0], 95.0)` for both 19 and 20.
- **Fallback without `let_go`** (if the PMG session's stepgen change is not committed): Steps 19 and 20 as one step,
  `g.remove('Disconnect the yellow, grey and purple breadboard wires from i2, i3 and b19, and remove the LED Matrix with them.',
  [MATRIX] + PINS, paths={MATRIX: [_shifted(where(MATRIX), [0.0, 30.0, 0.0])]}, units=[[MATRIX]], eye=['J_GREY_M', 'J_PURPLE_M'],
  **camera_of('Step 23'))`: every wire end rises 30 together (rigid); the sockets are never shown coming off the matrix. 23 steps.

**20. "Disconnect the yellow, grey and purple breadboard wires from i2, i3 and b19."**
```python
g.remove(c, PINS + SOCKETS, paths={s: [_shifted(where(s), [0.0, 30.0, 0.0])] for s in SOCKETS}, arrows=[],
         eye=['J_GREY_M', 'J_PURPLE_M'], caution='Pull each wire out by its connector. Do not pull on the wires themselves.',
         keep_camera=True)
```
- Undoes FB 13 - 11 (Lee's example group). The pins go up 30 (their default, FB 11 - 13 reversed), the loose sockets up 30 by
  hand, so every wire rises whole in its BESIDE shape and goes with its ends. No arrows; an eye on the i2 / i3 pair and one on b19
  (the sockets are no longer plugged into anything). As the MRA's eight breadboard wires (`deconstruction.py:238`) and the PMG's 21.
- `unplug()` is not used: it would put the leads on FB 11 - 13's routes, drawn for the matrix held upright over the breadboard
  (`guide.py:436-443`). `keep_camera=True` is needed: the default would be FB 13's close-up of b19.

**21 - 24. The breadboard parts, each the default (FB's way reversed, up, by its camera); resistor legs go with their resistor
(a lead whose other end is None, `stepgen.py:1119`).**

| # | Caption | Call | Undoes |
|---|---|---|---|
| 21 | "Remove the 330 Ω Resistor from a11 and a19." | `g.remove(c, [R330])` | FB 9 |
| 22 | "Remove the Capacitor from j2 and j3." | `g.remove(c, [CAP])` | FB 7 |
| 23 | "Remove the 12 kΩ Resistor from h3 and h16." | `g.remove(c, [R12K])` | FB 5 (before the Nano: their boxes overlap) |
| 24 | "Remove the Nano Board from the breadboard." | `g.remove(c, [NANO])` | FB 3 |

No counterpart (preparation and check steps, `cadasio-patterns.md:242`): FB 1 (backing peeled), 2 (breadboard on D1: permanent),
4 and 8 (legs bent), 6 and 14 (looking at the capacitor and the matrix's pins), 10 (ribbon split), 18 (nut off a new button).

## 5. The end, the parts list, the website

- **Completed View**: D1 with the breadboard on it, from Step 24's direction (FB 3's corner), framed close by the generator
  (`stepgen.py:2040-2048`). BACKING is not in it (put away).
- **Parts list**: the Full Build's two pages after the Completed View (`parts_list_at_end=True`): decided by the curriculum
  director's rule for the MRA (`cadasio-patterns.md:264-265`), which the PMG follows; tell Lee rather than ask.
- **Title page**: the Full Build's (copied when no `start_view` is given, `stepgen.py:1982-1985, 2040-2042`), the USB cable left
  off as there.
- **guides.json**: after the `laser-stem-matrix-full-build` line add
  `"laser-stem-matrix-deconstruction": {"kit": "laser-stem-matrix", "steps": "steps-deconstruction.json", "label": "Deconstruction", "script": "deconstruction.py"},`
  then `python3 tools/site_pages.py` (render.yaml's framing rules; check_site.py refuses the guide without them). guides.json
  already carries the PMG session's uncommitted entry: stage only this line.
- **Card**: the Full Build's, copied by `await _dev.card()` on `player.html?steps=steps-deconstruction.json` (a take_apart guide's
  card is its Full Build's: `CLAUDE.md` "A deconstruction guide"). The model is unchanged, so `cards/steps.json`'s model stamp holds.
- **Publishing**: to the test site only, `python3 tools/publish.py laser-stem-matrix-deconstruction --to "share/Test guides preview"`,
  `check_site.py` on that folder, Lee views it on 8799. Never `site/` or `live` without Lee's word.

## 6. Risks and how to check them

Run one heavy job at a time (swap was 912 MB free during this study).

| Risk | Where | Check |
|---|---|---|
| BACKING back under D1 | every view | Step 1 shows no backing; log reads `take_apart(): ... (98 parts, 10 leads)` then the put-away |
| Matrix walk-back with turns | Step 12 | `motioncheck.py "LSM Build Instructions" --steps steps-deconstruction.json "Step 12c"`; `_dev.show('Step 12c', 0.5)` and at 0.25 / 0.75 |
| Matrix walk-backs, plain | Steps 6, 8 | motioncheck `"Step 6c" "Step 8c"`; look at both half way |
| Two leads unplugged at once | Step 16 | motioncheck `"Step 16c"`; the two leads must not cross |
| D2 out with its leads | Step 14 | motioncheck `"Step 14c"` (FB 24 reversed: low) |
| Wires moved rigidly | Steps 15, 18, 19, 20 | motioncheck `"Step 15c" "Step 18c" "Step 19c" "Step 20c"` (should be clean by construction; Step 18's pins pass through D2's hole) |
| Wires at rest | all | `wirecheck.py "LSM Build Instructions" steps-deconstruction.json`: every view at rest is a Full Build state, so any hit is new |
| Wrong defaults | 4, 7, 13, 15, 17, 18, 19, 20 | log: no `WARNING`, no Review note; the only `NOTE` should be "4 arrows" (Step 4). Any WARNING: stop and look |
| Hand-placed arrows | 7, 14, 17, 18 | look: on the part, visible, not inside D2 or under the matrix |
| Arrows sized by default | 1, 4, 9, 13, 17 | look; small parts may want `arrow_scale` as Lee had the MRA's (question-free: adjust on Lee's round) |
| Close-ups | 4, 19 | the tab and the three sockets inside their frames, the red box on them; FB 36c's for comparison |
| Nut turning | 17 | `_dev.show('Step 17c', 0.5)`: a pause after one turn, no backwards spin |
| Turned-over run | 10 - 11 | the box turns over once at 10, back at 12; the matrix outside turns with it, as FB 27 - 28 |
| Cameras | all | the deconstruction never writes `steps.json`; still, checksum `steps.json` before and after the run (memory rule: diff cameras) |
| Whole guide | all | `_runthrough()` on `player.html?steps=steps-deconstruction.json`, and on the Full Build (82 views) |
| `let_go` not committed | 19 | before committing: `git diff tools/stepgen.py` must not be in this guide's commit unless Lee says; otherwise use the fallback |

## 7. Questions for Lee

1. **The LED matrix's round trip.** It stays wired to the breadboard until Step 19 (the purple wire's pin is under the USB plug,
   which the button blocks until D2 is out), so the draft carries it out over D4 (Step 8) and back beside the base (Step 12), the
   Full Build's own moves, with D5 and D3 coming off with the box turned over, as they went on. TechBox's published take-apart takes
   D5 and D4 off early and lays the matrix aside once, upright; that needs new wire shapes. Keep the draft's?
2. **Close-ups.** The draft has two: a D11 tab through D1 (Step 4) and the three connectors under the matrix (Step 19). Add the
   published take-apart's catch close-ups (D8 under the posts' top latches, D3's spring latches), or keep to these two?
3. **Power.** Keep the caution on Step 1, "Unplug the USB Cable from the computer or power supply before you begin."?
4. **Pry Tool.** Does the LSM kit have one? If so, Step 24 gets the MRA's caution, "Use the Pry Tool to carefully remove the
   Nano Board."
5. **Hole labels.** The MRA's servo unplugging carries the Full Build's Row labels instead of an eye. Should Steps 16 and 20 carry
   the Full Build's hole labels (j5, j16; i2, i3, b19) instead of eyes?
6. **More groups.** D8 and D7 in one step? The 330 Ω resistor, the capacitor and the 12 kΩ resistor in one step? (The stems, the
   four D11 posts, both D9, the button's two leads and the three wires are already together.)

## 8. Where the plans disagreed, and the ruling

| # | Point | A (published) | B (reverse) | C (generator) | Ruling and why |
|---|---|---|---|---|---|
| 1 | Overall order | published, D5 at 4, D4 at 13, D3 after D4 | FB reversed | FB reversed | **Reverse** (B, C): the house rule for a first draft; only shapes Lee has seen; question 1 |
| 2 | D5 and D3 | upright, D3 a straight pull after D4 | turned over, D3 swings | same as B | **B / C**: FB 27 - 28 reversed by their cameras; D3 must swing while D4 is on |
| 3 | The three wires | one step: pins up, sockets slid along pins, matrix removed after | matrix lifted with the pins, then sockets off in the hand (turned over) | matrix off the sockets (`let_go`), then all six ends up | **C**: A drags each wire up through the matrix (fact 2); B pulls the pins out by lifting the matrix and needs a turned in-hand camera no FB view gives; C is rigid and is the PMG's pattern of the same day. C's own one-step fallback kept |
| 4 | USB vs button leads | leads, nut, button, then USB | USB, then leads | USB, then leads | **B / C**: FB 23 before 22, 21 reversed |
| 5 | USB A end | up 25 | +Z 25 | up 25 | **+Z 25** (B): the whole cable shifts as one, nothing to check |
| 6 | D11 posts | two pairs | four, one stage (`direction` up 85), FB 35's camera | four, two stages, camera kept | **C**: Lee's groups; the tab push (FB 36) kept as the first beat; no camera jump |
| 7 | Nut and button cameras | one camera | one camera | two (inside, then outside) | **One** (A, B): Lee's rule (`cadasio-patterns.md:229-230`); the button's arrow placed inside |
| 8 | Nut's way | fresh `nut_turns(0, -95)` | FB 20 reversed, two beats | same as B | **FB 20 reversed** (B, C): the build's way, reversed; -95 (FB 18's) only if the nut looks wrong fading on the wires |
| 9 | D3 / D4 arrow stage | D4 `stage=0` | `stage=0` on both, scale 1.5 | defaults | **Defaults** (C): Lee's longest-stage rule; `stage=0` noted as an option |
| 10 | Step 12 cue | FB 26 arrow reversed | FB 26 arrow reversed + eye | default arrow | **B**: FB 26's own cue, Lee-approved |
| 11 | D10 arrow | at `[590, 892, 1204.5]` (off the part) | at a world point | at FB 31's spot | **C's spot** on D10's +Z face, explained in Step 7 |
| 12 | D2 arrow | default | default, `at=` if needed | on D2's top edge | **C**: a default arrow starts behind D2 |
| 13 | Close-ups | eight (published) | D11 tab only | D11 tab only | **D11 tab + the sockets' close-up** (A's idea, since the sockets are hidden); the rest is question 2 |
| 14 | Steps 19 - 20 camera | BASE_CAMERA (fallback `look_from`) | FB 23's | `look_from=[1, 1, -1]` | **FB 23's**: the same scene, Lee-approved; from the D5 / D3 corner the Nano may partly hide b19 |
| 15 | Step count | 25 | 24 | 24 | **24** (23 with the fallback) |
| 16 | Captions | build-like | build-like | build-like | **TechBox's MRA deconstruction wording** ("Remove ... from ...", "Disconnect ...") |

Smaller corrections to the studies: `study_build_map.md` item 3 gives the button `path=[[0, 0, 100]]`; hand paths are poses from
the seat, so that would move it only 42.9 mm: it is `[0, 0, 157.1]`. Plan A's note that D5's order check may flag D10 is
unfounded (fact 6). Everything else the studies state that this plan relies on was confirmed in the files.

Considered and not taken: unplugging the matrix's sockets as soon as it is held over the box (Step 7), which would save Steps 8 and
12, leaves the sockets and wires hanging in the air in the held shape through eight steps; not shown anywhere in the Full Build and
wrong to a learner.

## 9. After the script exists

1. Run it (`.venv.nosync/bin/python "LSM Build Instructions/deconstruction.py"`), read the log (section 6).
2. motioncheck, then wirecheck, one at a time; then the browser check on 8805 (`player.html?steps=steps-deconstruction.json`):
   `_runthrough()`, and the views named in section 6.
3. guides.json line, `site_pages.py`, `_dev.card()`, publish to the test site, `check_site.py` on it.
4. Records: a deconstruction section in `LSM Build Instructions/README.txt` (with the questions), an LSM paragraph under "A
   deconstruction guide" in `CLAUDE.md` and the address in its list, a rulebook note for anything Lee rules.
5. Commit only this guide's files (`deconstruction.py`, `steps-deconstruction.json`, the card files, the guides.json line, the
   records); other sessions have uncommitted work in `tools/stepgen.py`, `tools/motioncheck.py`, `CLAUDE.md`, `guides.json`,
   `player/js/player.js` and the PMG and LAC folders. The `let_go` dependency: commit after the PMG session's stepgen change is in.
