# LSM deconstruction, plan B: the Full Build walked last to first (21 Oct 2026)

Angle: our own Full Build reversed, as the MRA's and RCC's first drafts were; steps merged and parts grouped by Lee's conventions
(rulebook section 11; "some things can be removed in groups (like the 3 breadboard wires, etc.)"); reordered only where physical
access or the wire shapes require it. Read-only planning: nothing was run except light Python reading `steps.json` and
`assembly-report.json`. Sources: the four study reports in this folder (`study_build_map.md`, `study_generator.md`,
`study_published.md`, `study_conventions.md`); `LSM Build Instructions/guide.py`; `steps.json`; `tools/stepgen.py` (take_apart
828-901, _takeoff 949-1188, put_away 1217-1232, _arrow_out 1377-1455, build's takeoff branch 1713-1823, title / end 1980-2025);
`player/js/player.js` 112-141 (how a wire follows its end parts); the MRA's, RCC's and (today's, uncommitted) PMG's `deconstruction.py`.

**Result: 24 steps (0.60 per build step; the rulebook's range for 40 build steps is 18 - 33), ending on D1 with the breadboard
stuck to it, then the Full Build's two Parts List pages.** Every wire shape used is one the Full Build already has (played
backwards), or a rigid move of a whole wire with both its ends; no new wire geometry is drawn.

## 1. Why the order is (nearly) forced

The reverse is not only the house default here: the LSM's wires leave little choice. Read from the part boxes
(`assembly-report.json`), `guide.py` and the README:

- **The purple pin cannot come out before the USB plug.** The plug's leg sits over b19 (README Q2: the purple wire is drawn 0.3 mm
  into it; USB_B x 619.29-643.29, y 873.62-881.12, z 1204.60-1224.46 overlaps J_PURPLE_M x 626.16-627.91, y 867.92-879.92,
  z 1212.76-1214.51). The build plugged the pin in first (Step 13) and the USB later (23).
- **The USB plug cannot come out before D2.** Its way out (+Z 25, Step 23 reversed) meets the back of the seated button after
  9.2 mm (USB_B z max 1224.46, BUTTON z min 1233.65); the build plugged it in with D2 standing 57.1 mm out. Its cable also lies in
  the notch in D4's foot, closed above: the whole cable can leave only once D4 is off.
- **D2 cannot come out before D4 and D5** (its end tabs go through their slots; D2 x 590.58-685.89) **nor before the D9s** (their
  ends go through D2 and D3).
- **D4 cannot come off while the matrix's wires lie over its top edge** (Full Build Steps 26-31: OUTSIDE / LIFT routes cross it at
  y 909.5, `guide.py:659`).
- **The wires cannot be taken off at the breadboard early** without new shapes: whichever way a pin moves, the whole wire moves with
  it except its last 6 mm (`b_from` = length - 6 on every jumper route from 33 on, `guide.py:264-265`; `player.js:131-132`: before
  `b_from` a point follows `a`, the pin, wholly). In every place the matrix lies (in the box, held, outside D4, beside the base) the
  wire runs on under the board to the header, so a pin lifted on its own drags the wire up through the matrix.
- **D10 must come off while the matrix is held over the box (P_HELD)**, as it went on: carried out to P_OUTSIDE or P_BESIDE with the
  matrix it would sit across the wires' run under the board (the OUTSIDE / BESIDE shapes were drawn without it).
- **The D9s cannot come up 65 mm while the matrix is held over the box** (matrix bottom at P_HELD 949.7; D9 top + 65 = 965.7): the
  matrix goes out over D4 first, as in the build (Steps 29-30).

So: the matrix comes out with D10, D10 off, the matrix out over D4 (32, 31, 30 reversed); D9s, D5, D3 (29, 28, 27); the matrix
back over D4 to beside the base (26) so that D4 can come off (25); D2 out still wired (24); the USB cable (23); the button's
leads (22, 21); the button panel in the hand (20, 19); then the three wires, and the small parts. That is the Full Build in reverse
except that the three wires come off as one group, both ends, after the button (where the build's Steps 11-17 fall in reverse),
pins first and then the sockets in the hand (section 3, steps 19-20).

## 2. The script, outline

`LSM Build Instructions/deconstruction.py`, laid out as the MRA's (`MRA Build Instructions Prototype/deconstruction.py`) and the
RCC's. **Never `import guide`**: guide.py calls `g.build()` at module level (`guide.py:826`) and would rewrite steps.json and
parts.json. Every pose and route comes from steps.json.

```python
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
from stepgen import Guide, _rot, _shifted, apply_pose, compose, via

# parts (guide.py:27-40)
D1, D2, D3, D4, D5, D6, D7, D8, D10 = 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D10'
D9_A, D9_B = 'D9_A', 'D9_B'
D11S = ['D11_A', 'D11_B', 'D11_C', 'D11_D']
BREADBOARD, BACKING, NANO, R12K, R330, CAP, MATRIX = 'BREADBOARD', 'BACKING', 'NANO', 'R12K', 'R330', 'CAP', 'MATRIX'
BUTTON, NUT, RED_PIN, BLACK_PIN = 'BUTTON', 'NUT', 'BTN_RED_PIN', 'BTN_BLACK_PIN'
USB_B, USB_A = 'USB_B', 'USB_A'
PINS = ['J_WHITE_M', 'J_GREY_M', 'J_PURPLE_M']        # in i2, i3, b19 (the 'white' wire is shown and named yellow: Lee, 20 Oct)
SOCKETS = ['J_WHITE_F', 'J_GREY_F', 'J_PURPLE_F']     # on V+, V-, IN
WIRES = ['wire white', 'wire grey', 'wire purple']
STEMS = [f'STEM_{k:02d}' for k in range(1, 65)]
DIAG = [-0.5792, 0.5736, -0.5792]

FULL = json.loads((HERE / 'steps.json').read_text(encoding='utf-8'))
VIEW = {v['name']: v for v in FULL['views']}
ROUTES = FULL['routes']

def camera_of(step, moved=None):                      # as MRA deconstruction.py:55-60
def full_way_back(step, part, then=()):               # as MRA deconstruction.py:92-99
def where(i):                                         # as MRA deconstruction.py:108-113 (after g exists)
def turned_camera(step, pose):                        # as RCC deconstruction.py:42-46, with the pose given
    c = VIEW[step]['camera']
    return dict(view_dir=[round(float(x), 4) for x in _rot(pose) @ c['dir']],
                frame=([round(float(x), 1) for x in apply_pose(pose, c['target'])], c['radius']))
routes_at = lambda view: {w: ROUTES[VIEW[view]['wires'][w]] for w in WIRES}                       # a view's jumper shapes
stages_back = lambda view: {w: [ROUTES[n] for n in reversed(VIEW[view]['wire_via'][w])] for w in WIRES}   # its wire_via, reversed

# poses the Full Build used (read, not retyped; carry poses are rounded to 0.1 mm, turned ones to 0.01: harmless)
D2_OUT = VIEW['Step 24']['path'][0]                                     # [0, 0, 57.1]        (guide.py:559)
P_HELD = VIEW['Step 30c']['carry'][MATRIX]['pose']                      # [-0.2, 56.6, -0.3]  (guide.py:223)
P_LIFT = VIEW['Step 30c']['carry'][MATRIX]['via'][0]                    # [-90.8, 56.6, 25.1] (guide.py:744)
P_OUTSIDE = VIEW['Step 30']['carry'][MATRIX]['pose']                    # [-90.8, 5.9, 25.1]  (guide.py:222)
BACK_OVER_D4 = [*reversed(VIEW['Step 26c']['carry'][MATRIX]['via']), VIEW['Step 26']['carry'][MATRIX]['pose']]
                                                # P_UP_OUTSIDE, P_MID (90 deg), P_UP_BESIDE (180 deg), P_BESIDE (guide.py:221, 683-685)
D10_ALONG = VIEW['Step 31c']['carry'][D10]['via'][0]                    # [0, 0, 40] on the matrix
D10_UNDER = VIEW['Step 31']['carry'][D10]['pose']                       # [0, -22, 40] on the matrix

g = Guide(HERE, title='Laser Stem Matrix (LSM)', part='Deconstruction', names=dict(FULL['names']),
          steps_file='steps-deconstruction.json', source='lsm.glb', hero_azimuth=45,
          copyright_line='© TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')
g.take_apart(parts_list_at_end=True)       # (the Full Build's parts list after the Completed View, as the MRA's)
g.put_away([BACKING])                      # (see risk R1)
... the 24 steps below ...
g.build()
```

`source='lsm.glb'` (Guide's default is mra.glb), `hero_azimuth=45` (default 225; it matters only if the last step were turned over).
`names=dict(FULL['names'])` already holds the hover names ("Yellow Breadboard Wire", "Push Button" for the nut and pins, "USB Cable",
"D9", "D11"): no `hover_names=` needed.

## 3. The steps

Columns: (a) caption, (b) the call, (c) Full Build step(s) undone, (d) why here, (e) risk. "Default" = the generator's own way
(the Full Build's, reversed) and camera.

### 1. Stems
- (a) "Pull all 64 LED stems up out of D8, D7 and D6."
- (b) `g.remove(caption, STEMS, units=[STEMS])` (default ways: up 44; camera Step 40's STEM_CAMERA: DIAG, [638.5, 936, 1204.5], 90).
- (c) 40 + 39 ("one, then the rest" merges, rulebook l.242). (d) On top; they pass through D8, D7, D6. (e) Without `units=`
  STEM_01 (Step 39) and the other 63 (Step 40) are two units, two arrows. One arrow, starting on the stem nearest the block's middle
  (stepgen 1397-1402), about 24 mm (one stem's size). The published take-apart has one arrow too.

### 2. D8
- (a) "Lift D8 up off the four D11 posts, easing it past the latches at their tops."
- (b) `g.remove(caption, [D8])` (default: up 55, SHELF_CAMERA).
- (c) 38. (d) On the posts, under their top latches (Lee, 20 Oct: D8's top 0.02 mm under the latch heads). (e) D8 passes through
  the latch heads as it rises, as it did coming down in the build (README Q17: D8 sits 1.2 mm into each post; Lee's question on a
  newer D8 / D11 is open). The order check does not see the posts (they ride on D1, stepgen 983), so no warning. Optional close-up
  of a latch (published Step 2): question 6.

### 3. D7
- (a) "Lift D7 up off the D11 posts."
- (b) `g.remove(caption, [D7])` (default: up 65, SHELF_CAMERA).
- (c) 37. (d) Under D8, on the posts. (e) None.

### 4. The four D11 posts
- (a) "Pull the four D11 shelf posts up out of D6. Their tabs come up out of the slots in D1."
- (b) `g.remove(caption, D11S, direction=[0, 1, 0], hover=85.0, units=[[i] for i in D11S],`
  `view_dir=[-0.7476, 0.3966, 0.5328], frame=([638.5, 935.0, 1204.5], 100.0),`
  `inset=dict(target=[601.63, 857.0, 1242.4], dir=[-0.4109, -0.8401, 0.3541], radius=6.0, mark=3.0, caption='The tab through D1',`
  `alt="Close-up from below of a D11 post's tab through its slot in D1"))`
- (c) 36 + 35 + 34 merged (the lock and both pairs). (d) D7, D8 off; the posts go through D6's corner slots, so before D6.
  Camera: Step 35's own (the D4 / D2 corner, framed for posts 85 mm up), upright: Step 36's is turned over and from below, and
  from it an upward arrow points at the camera (|d . dir| = 0.84 > 0.8) and turns into an eye. The close-up is Step 36c's, moved
  to D11_C's tab (D1_SLOTS x 601.63, z 1242.4, `guide.py:793`), the corner nearest this camera, seen from below with a red box.
- (e) The D11s ride on D1 and have no Full Build record (they came in by `ride=`, `guide.py:803-814`): without `direction=` they
  are "lifted straight up, unchecked" with a WARNING and a yellow Review note (stepgen 1027-1032). With `direction=` there is no
  collision test, which is right (it was the build's own way). Four arrows: the log's NOTE "4 arrows" (stepgen 1134-1135), as the
  MRA's six base screws (Lee asked for an arrow on each). One straight pull instead of the build's two stages (6.38 then 85): both
  stages are straight up, so a pause between them shows nothing. The close-up is optional (question 6).

### 5. D6
- (a) "Lift D6 off the tops of the walls."
- (b) `g.remove(caption, [D6])` (default: up 64, Step 33's camera DIAG, [638.5, 913, 1204.5], 84).
- (c) 33. (d) Over the matrix, D10 and the D9s; on the walls' tabs. (e) None (Step 33's close-up of D1's slots is a build cue,
  not carried over; takeoff close-ups keep only one red box, stepgen 1777-1778).

### 6. The matrix lifted out with D10, still wired
- (a) "Lift the LED matrix, with D10 hooked under it, up out of the box, and hold it over the box. Its wires stay plugged in."
- (b) `g.lift(caption, [MATRIX], wires=routes_at('Step 32'), wire_via=stages_back('Step 32c'))` (default way: Step 32's reversed,
  seat -> through P_HALF -> P_HELD, one beat, stops [0, 2]; camera Step 32's: DIAG, [636, 912, 1210], 66).
  `wires` = HELD (routes 59 / 60 / 61), `wire_via` = HALF (62 / 63 / 64).
- (c) 32. (d) D6 is off; "wired modules are lifted off the housing first, still wired" (rulebook l.239). D10 and the three sockets
  ride on the matrix and go with it (Completed View carry).
- (e) `lift()` never re-routes a lead by itself (stepgen 1086-1099): without `wires=`, only the wires' last 6 mm would follow the
  sockets and the rest would stay in the box (a 56 mm stretch). With them it is Step 32 played backwards (the Full Build's Prev).
  One arrow up from the matrix, about 32 mm.

### 7. D10 off the matrix
- (a) "Slide D10 along under the LED matrix until its hooks let go of the edges, then lower it away."
- (b) `g.remove(caption, [D10], paths={D10: [compose(where(MATRIX), D10_ALONG, g._pivot(D10)),`
  `compose(where(MATRIX), D10_UNDER, g._pivot(D10))]}, arrow_style={D10: dict(at=[599.3, 936.6, 1207.7])}, **camera_of('Step 31'))`
  (= [[-0.2, 56.6, 39.7], [-0.2, 34.6, 39.7]]: +Z 40 along the matrix, then down 22; two beats; camera Lee's framing of Step 31:
  [-0.6875, 0.4904, -0.5355], [631.8, 932.6, 1218.0], 63.4).
- (c) 31. (d) It came on here, under the held matrix; carried further with the matrix it would cross the wires' run under the
  board (section 1).
- (e) D10 rides on the matrix with no record: without `paths=` it goes straight up through the matrix, WARNING + Review note
  (stepgen 1026-1032). The arrow by hand, as the build's Step 31 (`guide.py:759`, Lee: "on D10's end at D4, outside the matrix,
  where it shows"; no arrow hidden under the matrix, lee_notes_2026-10-19b.md:41): tail just off D10's +Z face at its D4 end
  (seated [599.5, 880.0, 1207.0] moved by P_HELD), pointing +Z along the slide, about 28 mm. By the box sight line it is clear of
  D10's lower edge from this camera; look at it. The wires (HELD) lie in D10's slot throughout, as in the build.

### 8. The matrix out over D4
- (a) "Carry the LED matrix over D4 and lay it down outside the box, LEDs up, its wires over the top edge of D4."
- (b) `g.lift(caption, [MATRIX], path=[P_LIFT, P_OUTSIDE], wires=routes_at('Step 30'), wire_via=stages_back('Step 30c'),`
  `**camera_of('Step 30'))` (two beats, both poses stops; `wires` = OUTSIDE 53 / 54 / 55, `wire_via` = LIFT 56 / 57 / 58; camera
  HELD_CAMERA: DIAG, [601, 910.9, 1204.6], 114.8).
- (c) 30. (d) The D9s cannot come up under the held matrix (section 1); this is where the build had it while they went in.
- (e) The matrix has no record of Step 30 (it rode; D4 was given a still way to pace it, `guide.py:748`), so the way is by hand.
  Two stops against one LIFT stage plus OUTSIDE: the wires keep pace stop by stop, as in the build. One arrow (about 40 mm) along the
  move across, from the matrix's D4 edge, over D4's top.

### 9. The two D9
- (a) "Pull both D9 LED supports up out of their slots in D2 and D3."
- (b) `g.remove(caption, [D9_A, D9_B])` (default: up 65; HELD_CAMERA).
- (c) 29. (d) The matrix is off them; their ends go through D2 and D3, so before D3 and D2. (e) Two arrows (two of a kind, not
  touching: stepgen 1129-1131). D9_A lifts off over the wires under its engraved end, as it came down over them.

### 10. D5 (turned over)
- (a) "Turn the box over. Slide D5 off the end, off the tabs of D1, D2 and D3."
- (b) `g.remove(caption, [D5])` (default: +X 42, Step 28's turned-over camera, kept with `flip` by stepgen 1146-1147).
- (c) 28. (d) D5 goes over the tabs of D1, D2, D3: first of the walls. (e) The decon's turned-over run (steps 10-11) takes its
  pivot and axis from D5's view (stepgen 2056-2067); the picture is the same as the build's. The matrix lying outside D4 turns over
  with the box, as in the build's Steps 27-28. Arrow about 34 mm. Upright instead: question 3.

### 11. D3 (turned over)
- (a) "Swing D3 open from the D5 end, then slide its tabs out of the slots in D4."
- (b) `g.remove(caption, [D3], arrow_style={D3: dict(stage=0, scale=1.5)})` (default way: swing 22 deg about the hinge, then 40 mm out
  along the tilt; Step 27's turned-over camera).
- (c) 27. (d) D5 off; D3's end tabs are hooked in D4's slots, so it unhooks by its hinge while D4 is on.
- (e) By default the arrow follows the longer stage, the slide along D3's length, which cannot be done first; `stage=0` puts it on
  the swing (outward, -Z), as the RCC's joysticks (Lee). About 25 mm by default (D3's middle swings ~16 mm), so x1.5. A way with a
  turn is not order-checked (stepgen 1049). Optional close-up of D3's latches (Lee's new D3 has spring cuts): question 6.

### 12. The matrix back over D4, beside the base
- (a) "Turn the box the right way up. Lift the LED matrix back over D4, turning it round, and lay it beside the base, where D5 was."
- (b) `g.lift(caption, [MATRIX], path=BACK_OVER_D4, wires=routes_at('Step 26'), wire_via=stages_back('Step 26c'),`
  `arrows=[dict(tail=[585.0, 862.4, 1133.0], head=[690.0, 862.4, 1133.0], normal=[0, 1, 0], part=D1, width=5.0)], eye=[MATRIX],`
  `**camera_of('Step 26'))` (four beats: P_UP_OUTSIDE, P_MID, P_UP_BESIDE, P_BESIDE, all stops; `wire_via` UP_OUTSIDE, MID,
  UP_BESIDE = routes 46, 45, 44 / 49, 48, 47 / 52, 51, 50; `wires` BESIDE 33 / 34 / 35; camera from above: [0, 0.9961, 0.088],
  [638.5, 880, 1205], 82).
- (c) 26. (d) D4 cannot come off with the wires over its edge (section 1); BESIDE runs past D9_B's and D5's places, now empty.
- (e) **The one turned walk-back**: the matrix is now the mover (in the build it rode, paced by D4's still way); its turned poses
  and the three-stage wires should blend as the build's did backwards, but the pacing of a mover's turned poses against
  `wire_via` is inferred, not seen: motioncheck.py on this step first. Cues: the build's own arrow on D1 reversed (beside the box,
  where D3 stood) and its eye on the matrix (`guide.py:701-703`). The default arrow instead would start at the matrix's D4 edge and
  run through D4 (it is below D4's top); if Lee prefers an arrow on the matrix, `arrow_style={MATRIX: dict(shift=[0, 9, 0])}` and no
  `arrows=`. Roundabout to a student (out at step 8, back here): question 1.

### 13. D4
- (a) "Pull D4 outward off the tabs of D1 and D2, then lift it up off the USB cable."
- (b) `g.remove(caption, [D4], path=[[-8.0, 0.0, 0.0], [-8.0, 65.0, 0.0]], arrow_style={D4: dict(stage=0, scale=1.5)},`
  `**camera_of('Step 25'))` (BASE_CAMERA: DIAG, [630, 880, 1228], 125).
- (c) 25. (d) D3 and D5 off, wires off its edge; D4 is over D2's tabs (closed slots), so before D2.
- (e) **By default D4 would not move**: its latest record is Step 31's still way (`paths={D4: [ZERO]*3}`, `guide.py:757`), which
  wins (`fits[-1]`, stepgen 1000), with no arrow (travel < 1 mm, stepgen 1404) and Step 31's D10 camera. The hand way is Step 25's
  reversed (`guide.py:633`). Arrow on the first stage (the 8 mm pull off the tabs, -X), x1.5 (about 39 mm). D4's notch is open
  below: it lifts off the cable.

### 14. D2 out, still wired
- (a) "Slide D2, with the push button, out of the slots along the edge of D1. Leave the button's wires plugged in."
- (b) `g.lift(caption, [D2], wires={'lead red': ROUTES[38], 'lead black': ROUTES[39]})` (default way: Step 24's reversed, +Z 57.1;
  BASE_CAMERA). Routes 38 / 39 are Step 24's hover shapes (`VIEW['Step 24']['wires']`).
- (c) 24. (d) D4, D5, D9s off; the USB plug's way out is blocked by the seated button (section 1); the leads' unplug poses assume
  D2 at D2_OUT. BUTTON and NUT ride on D2.
- (e) Without `wires=` the leads would stretch from the seated shapes 42 / 43. The default arrow (+Z) starts behind D2 from this
  camera and is moved on ~28 mm before it shows, and its first spot is inside the button's head: if it floats, `arrow_style={D2:
  dict(at=[660.0, 909.5, 1255.0])}` (just above D2's top edge, clear of the button). About 36 mm.

### 15. The USB cable
- (a) "Pull the USB cable's plug out of the Nano Board's USB socket, and take the cable away."
- (b) `g.remove(caption, [USB_B, USB_A], units=[[USB_B]], paths={USB_A: [[0.0, 0.0, 25.0]]}, arrow_scale=2.5)` (USB_B default:
  +Z 25; camera Step 23's BASE_CAMERA).
- (c) 23. (d) D2 is out of its way; D4 is off the cable. (e) USB_A has no record (`show=`): a hand way. Moving it +Z 25 with the
  plug moves the whole cable rigidly (both ends by the same vector): it stays over D1 and clear of the button's leads above it
  (y 893+); lifting the A end instead (as the MRA / RCC did) would bend the cable's middle over D1's edge, untested. One arrow, on
  the plug, 15 mm x2.5 (Step 23's camera radius is 125: the MRA doubled its USB arrow, the RCC quadrupled).

### 16. The button's two leads unplugged
- (a) "Unplug the push button's red and black wires from j5 and j16."
- (b) `g.unplug(caption, [RED_PIN, BLACK_PIN], **camera_of('Step 21'))` (defaults: Steps 21 / 22 reversed; leads to routes 36 / 37;
  each pin then rides on BUTTON, its `rode`; an eye on each; camera LEAD_CAMERA red: [0.5792, 0.5736, -0.5792], [645, 884, 1209],
  40, which framed the pin's whole way in Step 21 and has j16 in it).
- (c) 22 + 21 (two wires in, one per step; out together, rulebook l.256-257). (d) D2 is at D2_OUT, where the poses and shapes were
  drawn (route 36's a_ref [0, 0, 57.11]). (e) Both stretch leads blend at once (38 -> 36 and 39 -> 37); the build blended them
  one at a time: motioncheck. The default camera would be Step 22's close one on j16.

### 17. The nut (the button panel in the hand)
- (a) "Unscrew the nut from the push button, on the inside of D2, and slide it off over the wires."
- (b) `NUT_WAY = full_way_back('Step 20', NUT)` (8 poses: 7 via, the last a stop; the nut's Step 20 way reversed, unscrewing a
  quarter turn a pose, clockwise from the head: Lee, 19 Oct); then each pose shifted by D2_OUT (`_shifted(p, D2_OUT)`, re-wrapped in
  `via()` where it was one) and the fourth (z -30, 360 deg) unwrapped into a stop, so the two turns take two beats as in the build.
  `g.remove(caption, [NUT], path=NUT_WAY, alone=[D2, BUTTON, NUT, RED_PIN, BLACK_PIN],`
  `arrow_style={NUT: dict(at=[649.2, 882.6, 1307.4], scale=2.0)}, **camera_of('Step 20', moved=D2_OUT))`
  (camera [0.5792, 0.5736, -0.5792], [638.2, 881.6, 1272.2], 69.3: inside D2, as the build's Step 20, moved with D2).
- (c) 20. (d) "A sub-assembly is taken apart on its own" (RCC, Lee 18 Oct); the nut holds the button in D2.
- (e) **NUT has no usable record** (its Step 20 group was NUT + BUTTON, which stays): without `path=` it is pulled straight, no turn,
  WARNING + Review. Shifting the poses (`_shifted`) keeps the build's own turns and pivot; `compose()` would rewrite each as a turn of
  at most 180 deg (still a quarter turn per pose, so it would play the same, but less plainly). The arrow where Lee put the build's
  Step 18 arrow: from the nut's rear face, 1 mm up, clear of the black lead (`guide.py:546-547`), moved by D2_OUT; 15 mm by default,
  x2 (about 0.43 of the camera radius).

### 18. The button out of D2
- (a) "Push the button, with its wires following, back out through the round hole in D2."
- (b) `g.remove(caption, [BUTTON], path=[[0.0, 0.0, D2_OUT[2] + 100.0]], alone=[D2, BUTTON], keep_camera=True,`
  `arrow_style={BUTTON: dict(at=[649.2, 882.6, 1276.0])})`, then `g.put_away([D2])`.
- (c) 19. (d) The nut is off. The pins ride on BUTTON (step 16), so they and both leads go with it (stepgen 1100-1109).
- (e) **BUTTON's latest record is Step 20's still way** (`TWO_BEATS`, `guide.py:534, 553`): without `path=` it would not move.
  The way is Step 19's (+Z 100) from D2_OUT; the pins pass through D2's hole as they did in Step 19. One camera for the run in the
  hand (Lee's rule, rulebook l.230): from inside D2 the button's head is hidden, so the arrow is placed inside, beside the button
  body (x 649.2, clear of it by 2.5 mm), pointing at D2 along the push (about 32 mm, ending 1 mm short of D2's inner face). The
  build's own camera for Step 19 is outside D2 (question 5).

### 19. The three wires out of the breadboard, the matrix lifted with them
- (a) "Pull the yellow, grey and purple wires' pins out of i2, i3 and b19, and lift the LED matrix away with the wires still on it."
- (b) `g.lift(caption, [MATRIX] + PINS, paths={MATRIX: [_shifted(where(MATRIX), [0.0, 30.0, 0.0])], **{p: [[0.0, 30.0, 0.0]] for p
  in PINS}}, units=[[MATRIX]], eye=['J_GREY_M', 'J_PURPLE_M'], **camera_of('Step 23'))` (BASE_CAMERA: the build's camera for this
  very layout, the matrix beside the base, Steps 23-25, and the decon's steps 13-15). After it the pins ride on the matrix (lift:
  the movers after the first ride on the first, stepgen 1148-1152).
- (c) 13 + 12 + 11 (pins; Lee's group). (d) The USB plug is out (b19); the matrix lies beside the base with the BESIDE shapes;
  nothing above.
- (e) Everything at both ends of the three wires moves by the same +30 Y (pins up, as PIN_HOVER; the matrix with its sockets
  riding), so each wire moves rigidly (`player.js:131-139`: wa + wb = 1) and passes through nothing; no route change. A pin lifted
  on its own would drag its wire up through the matrix (section 1). Cues: one arrow on the matrix (about 25 mm); an eye on the
  i2 / i3 pair and one on b19 (the MRA's eight wires: an eye per group of ends). Camera: by the boxes, from DIAG (D3 now gone) the
  sight lines from i2 / i3 just clear the Nano's corner and from b19 clear R330; from either +X corner the capacitor (j2 / j3)
  hides i2 / i3. At radius 125 the pins are small (the eyes point at them): if they read too small, the same direction framed
  closer round the breadboard and the matrix, about `frame=([680.0, 885.0, 1210.0], 95.0)`; to be checked by eye.

### 20. The three wires off the matrix (in the hand)
- (a) "Turn the LED matrix over. Pull the three wires' sockets off its V+, IN and V- pins."
- (b) `OFF = (_rot(where(MATRIX)) @ [0.0, 0.0, 15.0]).round(3).tolist()` (= [0, 0, -15]: the build's SOCKET_OFF, `guide.py:224`, in
  the matrix's frame, turned 180 deg with it); `g.remove(caption, SOCKETS + PINS, alone=[MATRIX] + SOCKETS + PINS,`
  `paths={c: [_shifted(where(c), OFF)] for c in SOCKETS + PINS}, arrows=[], eye=['J_PURPLE_F'], flip=True,`
  `**turned_camera('Step 14', where(MATRIX)))`, then `g.put_away([MATRIX])`.
  (Step 14's turned-over view of the header, [-0.1802, -0.8011, 0.5708], [628, 895, 1199], 36, turned with the matrix: about
  [0.18, -0.80, -0.57], [740.6, 903.3, 1220.4].)
- (c) 17 + 16 + 15 (sockets; Lee's group). (d) In the hand, as the published take-apart's Step 15 and the RCC's modules. Pins first
  (step 19), then sockets: the build's sockets went on with the matrix upright over the breadboard (P_UP), a place the take-apart
  never passes through, so that order cannot be reversed with shapes that exist.
- (e) All six caps move by the same 15 mm, so the wires slide off rigidly under the board, parallel to it; both ends leave, so the
  leads go with them (stepgen 1107). The sockets have no record (they rode on in the build): `unplug()` of them is a ValueError
  (stepgen 1022), `remove()` without `paths=` lifts them straight up, Review note. An eye on the middle socket, no arrow (Lee's MRA
  round: eyes on wire ends). The turned-over view and its frame need a look; a one-step turned-over run gets its own pivot.

### 21. 330 ohm resistor
- (a) "Pull the 330 Ω resistor out of a11 and a19." (b) `g.remove(caption, [R330])` (default: up 30; Step 9's camera). (c) 9.
  (d) After the purple pin in b19 (next to a19) and the USB plug. (e) Its legs (`330 leg 1/2`, b = None) go with it. 15 mm arrow
  (the minimum) at radius 30.

### 22. Capacitor
- (a) "Pull the capacitor out of j2 and j3." (b) `g.remove(caption, [CAP])` (default: up 29; Step 7's camera). (c) 7. (d) Build
  reverse. (e) None (the polarity caution belongs to putting it in).

### 23. 12 kΩ resistor
- (a) "Pull the 12 kΩ resistor out of h3 and h16." (b) `g.remove(caption, [R12K])` (default: up 32; Step 5's camera). (c) 5.
  (d) It lies over the edge of the Nano (boxes overlap 1.2 mm in x): before the Nano. (e) Legs go with it.

### 24. Nano Board
- (a) "Lift the Nano Board out of the breadboard." (b) `g.remove(caption, [NANO])` (default: up 35; Step 3's camera).
  (c) 3. (d) Last of the electronics. (e) None. About 19 mm arrow at radius 50.

### Not undone
Build Steps 1 (backing), 2 (breadboard on D1: it stays, stuck), 4 and 8 (legs bent: the resistors leave bent), 6 and 14 (looking
at the capacitor and the matrix's pins), 10 (the ribbon split), 18 (the nut off a new button). Rulebook l.242.

## 4. The end, the parts list, guides.json

- **Completed View**: D1 with the breadboard stuck on it, nothing else (as TechBox's published LSM take-apart ends), framed on them
  from the last step's direction (DIAG, Step 3's), closer in (stepgen 2017-2025).
- **Parts list**: `take_apart(parts_list_at_end=True)`: the Full Build's "Parts List" and "Parts List (Cont.)" after the Completed
  View, as the MRA's (curriculum director, 19 Oct); CLAUDE.md says "No Parts List unless asked for", and Lee's "same principles as
  the MRA" reads as asking. Say so to Lee.
- **Title page and card**: the Full Build's (no `start_view`; `_dev.card()` copies `cards/steps.webp`, whose model 0a7267f2bc49 is
  the current one; the deconstruction adds no part, so the model is unchanged).
- **guides.json**, after `laser-stem-matrix-full-build` (line 17):
  `"laser-stem-matrix-deconstruction": {"kit": "laser-stem-matrix", "steps": "steps-deconstruction.json", "label": "Deconstruction", "script": "deconstruction.py"}`;
  then `python3 tools/site_pages.py` (render.yaml's framing rules for the new address).
- **Step text**: `step-text-deconstruction.json` (step_text.py with `steps-deconstruction.json`) if Lee's developer rewords it.

## 5. Risks, in one list, and what to check after the first run

- **R1. BACKING comes back.** `take_apart()` places every part any view showed (stepgen 874-880); BACKING was last seen in Step 1c
  riding the breadboard at [0, -40, 0] (checked in steps.json), so it would hang 40 mm under D1 in every step, in plain sight in the
  turned-over ones. `g.put_away([BACKING])` straight after `take_apart()` removes it; the cost is that Step 1 opens as a cut (no
  glide from the title page). The title page itself is the Full Build's (BACKING hidden in its seat). A cleaner fix is in
  take_apart(): skip a part that is not in a plain Completed View; that changes generator behaviour for every kit (check the MRA /
  RCC / PMG deconstructions are unchanged before adopting it).
- **R2. Parts whose default is wrong** (all given by hand above): D4 (still way), BUTTON (still way), NUT (no fitting record), D10,
  the D11s and the sockets (no record: Review notes otherwise), USB_A (no record), every matrix move (lift re-routes nothing).
- **R3. Motion never seen before**: step 12 (a mover's turned poses with three wire stages over four beats), step 16 (two stretch
  leads blending at once), step 15 (the cable moved rigidly with its A end along the table). Run `tools/motioncheck.py "LSM Build
  Instructions" --steps steps-deconstruction.json` (one heavy job at a time) and look at those steps half-way (`_dev.show('Step 12c',
  0.5)`); `tools/wirecheck.py ... steps-deconstruction.json` for the views at rest. Steps 6, 7, 8, 9, 10, 11, 14 replay Full Build
  blends backwards; 19 and 20 move whole wires rigidly.
- **R4. Cameras and arrows placed from boxes, not pictures**: steps 4 (close-up placement), 7 (D10's arrow), 14 (D2's arrow), 18 (the
  button's arrow inside D2), 19 (whether the pins read at BASE_CAMERA's radius), 20 (turned-over hand view, the only new camera).
  Look at each.
- **R5. Log lines to expect**: NOTE "4 arrows" on step 4; no WARNING (any WARNING means a way was missed); the "plug left behind"
  check (stepgen 1153-1158) should stay silent (no seated plug with a `rode` record touches a lifted part).
- **R6. Cameras of the Full Build must not change**: the deconstruction writes only its own steps file; still diff steps.json before
  and after (memory: keep step cameras).
- Then the usual: `_runthrough()` on `player.html?steps=steps-deconstruction.json` and on the Full Build (82 views), the card, the
  test-site copy on 8799 for Lee; nothing to `site/` or `live` without Lee's word.

## 6. Questions for Lee

1. **The matrix's round trip.** Taken apart in reverse, the LED matrix is carried out over D4 (step 8) so the D9s, D5 and D3 can come
   off, then carried back to beside the base (step 12) so D4 can come off, and only then are its wires unplugged (step 19). It is the
   only order whose wire shapes all exist already, but it moves the matrix twice. The alternative is TechBox's published order (D5
   and D4 off early, the matrix set on the table still wired), which needs new wire shapes drawn and checked. Keep the reverse?
2. **The three breadboard wires** come off together in two steps: pins out of i2, i3, b19 with the matrix lifted (19), then the
   sockets off the matrix's pins in the hand (20). Or one step: the wires go with the matrix and are never shown coming off its pins?
3. **D5 and D3 with the box turned over**, as the build put them on (and the RCC's "Turn the car over"), or the right way up, as the
   published take-apart does?
4. **The four D11 posts in one step** with an arrow each (as the MRA's six screws), or two steps in pairs (build and published)?
5. **The push button in the hand**: one camera for the nut and the button (from inside D2, the button's arrow beside it inside), as
   your rule for a run in the hand, or the build's two (inside for the nut, outside for the button)?
6. **Close-ups of catches**, as TechBox's published LSM take-apart has (8 of them): the draft keeps only the build's own close-up of a
   D11 tab through D1 (step 4). Add the D8 latches on the posts (step 2) and D3's latches (step 11), or none (as the MRA's and RCC's)?
7. **Other groups**: D8 and D7 in one step? The 330 Ω resistor, the capacitor and the 12 kΩ resistor in one step? (Draft: one per
   step, as the build and the published guide.)
8. **Cautions**: "Pull each wire by its plastic end, not by the wire" on steps 16, 19, 20 (as the developer's MRA wording)? A first
   step caution to unplug the USB cable from the computer, since the cable itself cannot come out before step 15? Does the LSM kit
   have a pry tool for the Nano Board?
9. The Full Build's parts list after the Completed View (as the MRA's): yes?
