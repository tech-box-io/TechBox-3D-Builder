# LSM deconstruction, round 3: the LED matrix section (Steps 9 - 14 today) and how to rewrite it

Lee asked (22 Oct 2026, second set of notes): Step 10 should take D10 off at this point. It must **slide** off the matrix. Then the
three wires come off the matrix's pins together while staying in the breadboard, and after that the wires themselves are removed.
Read-only study, no model loaded. Files read: `LSM Build Instructions/deconstruction.py` (HEAD f9e9da1 plus working tree, 335 lines),
`wire_shapes.py` (469 lines), `published-takeapart.json`, `steps.json`, `steps-deconstruction.json`, `guide.py`, git 40dc19b / 59594ae,
`docs/research/lsm/decon/published/{published_steps.txt, feasibility_verdicts.json, feasibility_log.txt, wire_shapes.json}`,
`assembly-report.json`.

## Summary

1. **The new Step 10 (D10) can be the Full Build's own Step 31, played in reverse, with the matrix held where Step 9 leaves it.**
   - The poses: `VIEW['Step 31c']['carry']['D10']['via'][0]` = `[0, 0, 40]`, then `VIEW['Step 31']['carry']['D10']['pose']` =
     `[0, -22, 40]`, both relative to the matrix.
   - At the end of Step 9 the wires are already in the Full Build's held shape. That is Full Build routes 59 - 61, which are
     deconstruction routes 10 - 12, identical point for point. This shape was drawn to lie dead straight through D10's notch for the
     whole slide.
   - The Full Build's motioncheck finds no touch in Step 31. Its only touches are Step 26c (twice) and 32c
     (`docs/research/lsm/round4/review_summary.md:150`). Feasibility also found that D10 passes the D9s ("P9 static: D10 riding the
     matrix at P_HELD against wire white/grey/purple (route 59-61): overlap 0.0 mm").
   - No new wire shape is needed.
   - The published Step 14 camera can be used as it is. The published guide shows the matrix at `(0.0, 56.6, -0.5)`, which is within
     0.2 mm of our `P_HELD` `[-0.2, 56.64, -0.32]`.
2. **The new Step 11 can be one `remove()` of the matrix with `let_go=SOCKETS`**, the PMG pattern Lee has approved (a device pulled
   off its wires' caps, the caps left where they were).
   - The matrix slides back along its pins (−Z, unturned at P_HELD) and comes off the three connectors. It is then gone.
   - The connectors stay where they came off, and the wires stay in the breadboard in the held shape.
   - Neither end of any wire moves, so no new wire shape is needed.
3. **The plan's order "wires out (Step 12), then the D9s" does not work with these wires. The D9s have to come out first** (as the
   published guide does: D9s Step 10, wires Steps 11 - 13).
   - All three held routes run under D9_A (x 617.13 - 620.13, lower edge y 882.18), at these points:
     - white: `[620.59, 885.41, 1170.26] .. [616.88, 885.48, 1169.77]`
     - grey: `[620.56, 885.41, 1172.78] .. [616.85, 885.44, 1172.3]`
     - purple: `[620.09, 880.85, 1213.23] .. [617.13, 880.89, 1212.87]`
   - Lifting the wires 30 mm whole would carry all three through D9_A.
   - With the D9s out, the lift is clear of D2: below D2's top the wires stay at z ≤ 1250.19, and D2's inner face is at z 1251.93.
   - **Proposed order:** 9 lift (as now), 10 D10 slid off, 11 the matrix off its connectors and away, 12 both D9s (the current call,
     unchanged), 13 the three wires out of i2, i3 and b19 together.
4. **The guide drops from 25 steps to 24.** D3, D2, ... become Steps 14 - 24. Lee's other notes of today name the current numbers:
   - his Step 15 (D3's close-up box) becomes Step 14;
   - his Step 16 (D2) becomes Step 15;
   - his Step 20 (the nut back on) becomes Step 19.

---

## (1) Steps 9 - 14 as written now

The parts are named at lines 44 - 52:
- `PINS = [WS.MALE[w] for w in WS.JUMPERS]` = `J_WHITE_M, J_GREY_M, J_PURPLE_M`, in i2, i3 and b19.
- `SOCKETS = [WS.FEMALE[w] ...]` = `J_WHITE_F, J_GREY_F, J_PURPLE_F`, on V+, V- and IN.
- In the guide's words, 'white' is shown and named yellow and 'grey' is named gray.

The helpers used here (lines 111 - 146):
- `PUB` is `published-takeapart.json['steps']`. Line 112 asserts the field of view is 45 and `WS.LAID_POSE['r'] == [0, 1, 0, 180]`.
- `cam(step)` gives `view_dir` and `frame=(target, radius)` from PUB.
- `arrow(step, k, at, **more)` gives `dims=(length, width)` from PUB, rounded to 0.1. `at=None` uses the published tail, `at=False`
  uses the generator's place.
- `eye(step, k)` gives `dict(id=part, anchor=ring)`.
- The published guide put the matrix back over the box on its own (a glitch). These helpers carry its points and cameras to our matrix
  laid on the table instead:
  - `HOVER = [0.0, 56.64, -0.52]` (line 140) is the published matrix's hover.
  - `to_laid(p) = apply_pose(WS.LAID_POSE, [p - HOVER])` (line 141) carries a published point onto the laid matrix.
  - `laid_cam(step)` (lines 144 - 146) turns the published camera's direction by LAID_POSE (a half turn about Y) and moves its target
    with `to_laid`.

Steps 9 - 14 as written now:

| Step | Lines | Call |
|---|---|---|
| **9** | 242 - 247 | `MATRIX_UP = arrow('Step 9', at=apply_pose(where(MATRIX), [[612.8, 899.0, 1178.0]])[0])` (published size 70.6 x 3.8; the tail on the matrix's corner nearest the camera). `g.lift('Lift the LED Matrix, with D10 hooked under it, up off the two D9 pieces. Leave its wires connected.', [MATRIX], wire_via={w: [ROUTES[n] for n in nos[::-1]] for w, nos in VIEW['Step 32c']['wire_via'].items()}, wires=leads('Step 32', 'wire'), arrow_style={MATRIX: MATRIX_UP}, **cam('Step 9'))`. No path, so the way is the Full Build's Step 32 reversed. Step 9c in steps-deconstruction.json: `paths MATRIX [[0,0,0],[-0.1,28.0,-0.2],[-0.2,56.6,-0.3]]`, `path_stops [0, 2]`. The wires go through route 13 - 15 (HALF) to routes 10 - 12, which are the Full Build's 59 - 61 (HELD), the same points. Those routes keep `b_from` 255.2 / 245.7 / 178.4, `tail_from` 154.2 / 146.9 / 78.4 and `b_ref` `[-0.2, 56.64, -0.32]`. D10 and the three sockets ride on the matrix at ZERO. Camera `[-0.4752, 0.5698, -0.6705]`, `([616.29, 882.21, 1206.55], 91.3)`. |
| **10** | 248 - 250 | `g.lift('Set the LED Matrix down on the table beside the box. Leave its wires connected.', [MATRIX], to=WS.LAID_POSE, reappear=True, wires=WS.laid(), arrows=[], eye=[MATRIX], view_dir=cam('Step 9')['view_dir'], frame=([605.0, 895.0, 1215.0], 110.0))`. A fade: the matrix, D10 and the sockets fade out at P_HELD and in at LAID_POSE `{t: [-90.95, -26.844, 27.78], r: [0,1,0,180], at: MC}`. The wires change to LAID (routes 16 - 18). |
| **11** | 251 - 253 | `g.remove('Remove both D9 pieces from the slots in D2 and D3.', [D9_A, D9_B], arrow_style={D9_B: arrow('Step 10', 0), D9_A: arrow('Step 10', 1)}, view_dir=cam('Step 10')['view_dir'], frame=([605.0, 885.0, 1210.0], 106.0))`. Each D9 goes up 65 (the Full Build's Step 29 reversed). Arrows: D9_B tail `(657.17, 891.55, 1204.83)`, 69.2 x 3.4; D9_A tail `(618.76, 892.06, 1204.69)`, 61.2 x 3.4. The comment says the frame was widened "the laid matrix in frame too". |
| **12** | 257 - 259 | `g.unplug('Disconnect the yellow, gray, and purple breadboard wires from i2, i3, and b19.', PINS, ride_on=MATRIX, reappear=True, paths={WS.MALE[w]: [WS.pin_pose(w)] for w in WS.JUMPERS}, wires=WS.loose(), eye=[eye('Step 13'), eye('Step 12')], caution=PULL, **cam('Step 11'))`. A fade: the pins go from their holes to lying on the table by the laid matrix, and ride on the matrix after that. The wires change to LOOSE (routes 19 - 21). Eyes: J_GREY_M at `[648.66, 879.66, 1172.97]`, J_PURPLE_M at `[627.91, 877.52, 1213.56]`. `PULL` = 'Pull each wire out by its connector. Do not pull on the wires themselves.' Camera `[0.5557, 0.7581, -0.3413]`, `([625.34, 873.23, 1206.5], 91.3)`. |
| **13** | 264 - 267 | `LAID_VIEW = lambda step, target: dict(laid_cam(step), frame=(target, laid_cam(step)['frame'][1]))`. `g.remove('Unclip D10 from the bottom of the LED Matrix.', [D10], path=[_shifted(where(D10), [0.0, -40.0, 0.0])], alone=[MATRIX, D10, *PINS, *SOCKETS], arrow_style={D10: arrow('Step 14', at=to_laid(PUB['Step 14']['arrows'][0]['tail']))}, eye=[D10], **LAID_VIEW('Step 14', [550.0, 862.0, 1226.0]))`. D10 drops 40 mm straight down from the laid matrix. The comment at lines 262 - 263 gives the reason: slid first, D10 passed through the wires lying in its notch. Arrow 50.8 x 4.4 from `[582.62, 862.17, 1230.66]` to `[582.62, 811.37, 1230.66]`. Eye anchor (generator's) `[607.7, 889.1, 1204.0]`. Camera `[0.5194, 0.5906, 0.6177]`, `([550, 862, 1226], 78.2)`. |
| **14** | 268 - 276 | `LAID = where(MATRIX)`. `g.remove('Disconnect the three breadboard wires from the V+, IN, and V- pins on the LED Matrix.', PINS + SOCKETS, alone=[MATRIX, *PINS, *SOCKETS], paths={**{WS.FEMALE[w]: [WS.socket_pose(w, LAID, off=30.0)] ...}, **{WS.MALE[w]: [WS.pin_pose(w, LAID, off=30.0)] ...}}, units=[SOCKETS], arrow_style={SOCKETS[0]: arrow('Step 15', at=[576.0, 875.0, 1246.0])}, eye=[WS.FEMALE['purple']], caution="Hold the three black connectors on the LED Matrix's pins while you pull them off. Do not pull on the wires themselves.", **LAID_VIEW('Step 15', [556.0, 864.0, 1222.0]))`. All six caps move 30 mm along PULL (−Z in world, since the matrix is turned), the LOOSE wires are carried whole, and all of it is gone. Arrow 31.6 x 3.5 from `[576, 875, 1246]` to `[576, 875, 1214.4]`. Then line 276: `g.put_away([MATRIX])`. |

### wire_shapes.py, item by item

Coordinates are assembly mm, Y up. Routes are `W.route` dicts with a = the pin (`J_*_M`), b = the socket (`J_*_F`), and `a_at` / `b_at`
set to the poses the ends were drawn at.

**Names and the seated geometry**
- `ZERO`; `JUMPERS = ['white', 'grey', 'purple']`; `MALE = J_{W}_M`, the pins in i2, i3, b19; `FEMALE = J_{W}_F`, the sockets;
  `WIRE = 'wire {w}'`; `JUMPER_R = 0.62`; `TABLE_Y = 856.23` (lines 59 - 65).
- Seated geometry (lines 68 - 76):
  - `ROW_X` for rows a - j; `COL1_Z = 1167.91`; `PITCH = 2.54`; `HOLE` = white i2, grey i3, purple b19.
  - `MC = [638.82, 895.58, 1203.99]`, the pivot of the matrix's poses.
  - `M_MID`, each pin's middle: `[ROW_X[row], 873.92, z of the column]`.
  - `M_EXIT`, where each pin's wire leaves: the same point at y 879.92, leaving along +Y.
  - `F_MID`, each socket's middle at y 894.334, z 1187.26: x white 608.24, purple 610.78, grey 613.32.
  - `F_EXIT`, where each socket's wire leaves: z 1191.26, leaving along +Z.
  - `PULL = [0, 0, 1]`, the way a socket comes off its pin in the matrix's own frame (guide.py's `SOCKET_OFF`).
- `LAID_T = [-90.95, TABLE_Y + 0.05 - 883.124, 25.28 + 2.5]` = `[-90.95, -26.844, 27.78]` and `LAID_POSE = turned([0,1,0], 180, MC, LAID_T)`
  (lines 82 - 83). This is the published Step 9c pose, lowered 32.7 mm so that D10's feet stand on the table (856.28), and moved 2.5 mm
  further toward D2 so that D10 clears the USB cable's A end.

**Small helpers**
- `_laid_world(p)` = `unapply_pose(LAID_POSE, p)`: points drawn in the world with the matrix laid, given in the matrix's seated frame.
- `smooth(start, start_dir, end, end_dir, mids, lead=3.0, lead_b, spacing=0.5)`: guide.py's smooth(). A straight lead out of each
  end, `W.smooth` between, resampled every 0.75 mm.
- `_clean`: strips rounding noise from a pose.

**Where the caps are**
- `socket_pose(w, pose=LAID_POSE, off=0)` = `compose(pose, PULL*off, F_MID[w])`: the socket's absolute pose.
- `socket_ride(off)` = `PULL*off`: its pose riding on the matrix.
- `_f_end(w, pose, off)`: the socket's wire end (F_EXIT under that pose) and its direction (+Z turned).
- `_m_end(w, pose)`: the pin's wire end (M_EXIT) and its direction (+Y turned).
- `_route(w, pts, m_pose, f_pose_)`: `W.route(..., a_at, b_at)`, with no stretch, b_from or tail_from.

**The run under the matrix (lines 139 - 150)**
- `NOTCH_X`, the seated x of each wire in D10's notch: white 608.40, purple 610.07, grey 611.74. The notch is seated x 605.18 - 612.79,
  from y 889.10 up.
- `RUN_Y = 893.35` seated: 1.6 mm under the matrix's back and 4.1 mm over the notch's bottom.
- `_socket_run(w, laid_zs)` builds the level run at (NOTCH_X, RUN_Y), in the seated frame:
  - from the given laid z values;
  - through D10, at seated z 1206.6 and 1202.4;
  - and an S into line with the socket, at z 1197.6.

**LAID (lines 165 - 193): the matrix laid beside the box, the pins still in the breadboard**
- `BOX_MIDS` are fixed points inside the box. Every wire stays under the D9s' lower edges, so that the D9s can be lifted out over them:
  - yellow and gray go over the Nano beyond its ICSP pins and under D9_A's end (lower edge 886.3);
  - purple goes under D9_A (lower edge 882.2) beside the USB plug;
  - all three leave over D1's edge at the open D4 end, at the D2 end of the box, beside the USB cable (z 1219, 5 mm away);
  - yellow crosses over the other two, once each.
- `OUT_MIDS` are drawn in laid world coordinates and ride with the matrix: down to the run's height and round the turn under the
  matrix's +X edge.
- `LAID_RUN = [1219.0, 1223.0, 1226.5]`, laid z.
- `PIN_LEAD`: white 3, grey 3, purple 2.
- `laid(pose)`: pin in its hole (`_m_end(w, ZERO)`), through `BOX_MIDS`, then the outside points and the run (both carried by
  `pose`), to the socket at `socket_pose(w, pose)`.

**LOOSE (lines 201 - 242): unplugged, the pins lying on the table by the matrix**
- `PIN_X` (laid world x): grey 573.9, purple 576.7, white 579.5. `PIN_END_Z = 1189.0`. `PIN_AXIS_Y = TABLE_Y + 0.875`.
- `LOOSE_MIDS`, laid world points from the pin to the run, rising from y 857.9 at z 1196 to 865.9 at z 1224.5.
- `LOOSE_RUN = [1227.6]`.
- `_pin_laid(w)`: the pin turned 90° about X at M_EXIT, its tip toward −Z.
- `pin_ride(w, off)` = `relative_pose(LAID_POSE, _pin_laid(w), M_MID)`, composed with `PULL*off`.
- `pin_pose(w, pose, off)` = `compose(pose, pin_ride(w, off), M_MID)`.
- `loose_one(w, pose, off)`: from the pin at pin_pose, through `LOOSE_MIDS` and the run (both shifted by `off` along PULL and carried
  by `pose`), to the socket.
- `loose(pose, off)`: all three.

**The check (lines 246 - 465)**
- Pieces:
  - `Parts`: the meshes (or a cache), with `clearance()` = distance to the mesh minus the radius, negative when inside;
  - `other_wires()`: the USB cable, the button's leads and the resistor legs, from the Full Build's last view;
  - `measure()`: the centre line sampled every 0.2 mm against every part present, the table and the other wires;
  - `BASE`: D1, D2, D3, BREADBOARD, NANO, R12K, R330, CAP, BUTTON, NUT, the button's pins, USB_B, USB_A;
  - `CAPS`: the six caps.
- `scenes()` checks these:
  - LAID with the D9s in, and the D9s swept up 0 - 54.4 mm;
  - every mix of LAID and LOOSE (the D9s out);
  - the matrix on its own, connectors pulled 0 - 30 mm, with D10 off and with D10 on;
  - D10 dropped 0 - 30 mm straight down.
- `main()` asserts the caps' positions and writes `docs/research/lsm/decon/published/wire_shapes.json`. The least clearance recorded
  is 0.25 mm (to the table, in LOOSE), and 0.373 mm between wires in LAID. With D10 still on and the connectors pulled 7.5 mm, the gray
  wire is −0.895 mm into D10.
- **Out of date:** the module docstring (lines 30 - 35) still describes D10 "slid off its hooks and down". The code drops it straight
  (deconstruction.py line 265), and `scenes()` measures a straight drop.

## (2) The earlier drafts, from git

`git log --oneline -- "LSM Build Instructions/deconstruction.py"`: f9e9da1 (Lee's notes of 22 Oct 2026), 59594ae (rebuilt on the
published take-apart, 21 Oct), 40dc19b (first draft, 21 Oct).

### 59594ae: D10 slid off the matrix laid on the table (the version Lee saw the wires pass into D10)

Docstring, lines 18 - 20:

> "D10 is slid off its hooks before it drops (they hold both edges of the matrix: a two-stage joint undone in one step, rulebook
> section 11; the published guide drops it through them)"

Lines 242 - 251:
```python
# D10's hooks hold both edges of the matrix (the Full Build slid it on, its Step 31): slid back along 40 mm, then down, an arrow for each
# (a two-stage joint undone in one step, rulebook section 11; the published guide drops it straight, through the hooks).
UNHOOKED, DOWN = VIEW['Step 31c']['carry'][D10]['via'][0], VIEW['Step 31']['carry'][D10]['pose']   # ([0, 0, 40], [0, -22, 40]: on the matrix)
DOWN = [DOWN[0], DOWN[1] - 18.0, DOWN[2]]                           # (40 mm down in all, as far as the published drop)
LAID_VIEW = lambda step, target: dict(laid_cam(step), frame=(target, laid_cam(step)['frame'][1]))
g.remove('Slide D10 along the bottom of the LED Matrix, away from its pins, until its hooks come free of the edges. Then, remove it.',
         [D10], path=[compose(where(MATRIX), UNHOOKED, g._pivot(D10)), compose(where(MATRIX), DOWN, g._pivot(D10))],
         alone=[MATRIX, D10, *PINS, *SOCKETS], arrow_style={D10: dict(dims=(40.0, 4.4), stage=0,
                                                                      then=[arrow('Step 14', at=False, stage=1)])},
         eye=[D10], **LAID_VIEW('Step 14', [550.0, 862.0, 1226.0]))
```

- Here `where(MATRIX)` was LAID_POSE (turned half round), so the slide went −Z 40 in the world and the drop −Y 40. Its Step 13c path:
  `t` z 26.81 → −13.19, then y −26.84 → −66.84.
- Arrows as generated (Step 13): the slide from `[548.23, 865.06, 1195.79]` to `[548.23, 865.06, 1155.79]`, 4.4 wide. The staged drop
  arrow (stage 2 after the beat added for `then=`) from `[548.23, 826.28, 1191.29]` to `[548.23, 775.48, 1191.29]`, which is under the
  table.
- Camera: the published one carried to the laid matrix, `[0.5194, 0.5906, 0.6177]`, `([550, 862, 1226], 78.2)`.
- Why it failed: in the LOOSE shape the wires dip from y 865.9 (laid z 1224.5) to 857.9 (z 1196), below the notch's bottom (laid about
  862). So D10, sliding along the laid matrix, passed through them. Lee's note of 22 Oct: "The breadboard wires are occluded into D10
  during the animation". The held shape does not have this problem (below).

### 40dc19b: the first draft, the Full Build walked back. D10 slid off the matrix held over the box (what is wanted now)

Lines 158 - 166:
```python
g.lift('Lift the LED Matrix, with D10 hooked under it, up out of the box and hold it over the box. Leave its wires connected.', [MATRIX],
       wire_via={w: [ROUTES[n] for n in nos[::-1]] for w, nos in VIEW['Step 32c']['wire_via'].items()},   # (the Full Build's Step 32 reversed:
       wires=leads('Step 32', 'wire'), arrow_style={MATRIX: size('matrix')})   # its wires through the half-way shape to the held one)
g.remove('Slide D10 toward D2 until its hooks come off the edges of the LED Matrix, then remove it from under the matrix.', [D10],
         path=[compose(where(MATRIX), VIEW['Step 31c']['carry'][D10]['via'][0], g._pivot(D10)),   # (along 40 mm: unhooked)
               compose(where(MATRIX), VIEW['Step 31']['carry'][D10]['pose'], g._pivot(D10))],     # (then down 22, from under the matrix)
         arrow_style={D10: size('d10_slide', stage=0, at=at_now(D10, [599.5, 886.0, 1207.0]),   # (at D10's D4 end, outside the matrix,
                          then=[size('d10_drop', stage=1, at=[620.0, 915.0, 1241.5])])},   # short of the wires; then the drop, in front of D10)
         **camera_of('Step 31'))
```

- Sizes: `d10_slide=(20.0, 2.5)` and `d10_drop=(30.0, 4.4)`. Line 128 - 130: "D10 drops 22 mm (the published D10 48) ... D10's slide,
  which the published guide has no arrow for, short and thin, so that it stops short of the wires hanging by it."
- `camera_of('Step 31')` = the Full Build's Step 31 camera, `[-0.6875, 0.4904, -0.5355]`, `([631.8, 932.6, 1218.0], 63.4)`. Lee framed
  it from his own screenshot (round 3).
- Generated (40dc19b Step 7 / 7c):
  - path D10 `[[-0.2, 56.6, -0.3], [-0.2, 56.6, 39.7], [-0.2, 56.6, 39.7] (the beat), [-0.2, 34.6, 39.7]]`;
  - the slide arrow from `[599.3, 942.6, 1206.7]` to `[599.3, 942.6, 1226.7]`, 2.5 wide;
  - the drop arrow from `[620.0, 915.0, 1241.5]` to `[620.0, 885.0, 1241.5]`, 4.4 wide;
  - no eye.
- **Do not reuse that drop tail:** at x 620 ± 2.2 and y 885 - 915 the arrow passes through D9_A (x 617.13 - 620.13, y up to 900.69),
  which is still in at that point.
- The Full Build's own wording of the joint, guide.py lines 751 and 757: "D10 hooks under the LED matrix: up under it, then slid along
  so that its hooks hold the matrix's edges (it rides on the matrix)", and the caption "Hook D10 under the LED matrix: hold it under
  the matrix, then slide it along until its hooks hold both edges."
- Feasibility (`feasibility_log.txt`): the hooks sit over the board's x edges at the D4 end (D10 x 594.01 - 607.34 at y 897.9 - 899)
  and at the D5 end (669.57 - 682.91). The matrix board spans x 606.92 - 670.71, so the hooks overlap it by 0.42 mm and 1.14 mm.
  - "P14 alt: the Full Build's Step 31 reversed (+Z 40 along the matrix, then down 22) / stage 1: LATCH (matrix material at the
    D5-end edge at 0.39 mm)"; "/ stage 2: FREE".
  - "−Z 40 ... BLOCKED (J_GREY_F ... first met after 11.7 mm)", so the slide has to go +Z, toward D2.

**How the first draft handled the three wires and their connectors** (after the USB cable, with the matrix lying beside the base at
P_BESIDE). Lines 213 - 231:
```python
# The matrix pulled back along its pins off the three connectors, which stay where they lie (let_go, as the PMG's displays), then
# lifted away; a close-up of the connectors, which are under the matrix, with the matrix drawn faintly (as the Full Build's Step 32c).
OFF = compose(where(MATRIX), [0.0, 0.0, -15.0], g._pivot(MATRIX))  # (15 mm back along its pins, as the Full Build held the sockets off them)
ENDS = np.mean([apply_pose(where(s), [g._pivot(s)])[0] for s in SOCKETS], axis=0)   # (the three connectors, under the matrix's corner)
g.remove('Disconnect the LED Matrix from the yellow, grey, and purple breadboard wires.', [MATRIX], let_go=SOCKETS,
         path=[OFF, _shifted(OFF, [0.0, 30.0, 0.0])],
         arrow_style={MATRIX: size('cable', stage=0, at=(ENDS + [0.0, 4.0, 15.0]).round(2).tolist(), then=[size('cable', stage=1)])},
         caution='Hold the three black connectors while you pull the LED Matrix off its pins. Do not pull on the wires themselves.',
         inset=dict(target=ENDS.round(2).tolist(), dir=[-0.3, 0.8, 0.52], radius=10.0, mark=5.0, ghost={MATRIX: 0.15},
                    caption='The three connectors', alt="Close-up of the three wires' connectors on the pins under the corner of the LED Matrix, the matrix drawn faintly"),
         **WIRES_CAMERA)
g.remove('Disconnect the yellow, grey, and purple breadboard wires from i2, i3, and b19.', PINS + SOCKETS,   # (together: Lee; both ends of each, so the
         paths={s: [_shifted(where(s), [0.0, 30.0, 0.0])] for s in SOCKETS}, arrows=[],   # wires go up whole, as their pins came down)
         eye=['J_GREY_M', 'J_PURPLE_M'], caution=PULL, keep_camera=True)   # (an eye on i2 / i3 and one on b19)
```

- `size('cable') = (31.6, 3.5)`. `WIRES_CAMERA = dict(view_dir=[-0.5792, 0.5736, 0.5792], frame=([684.0, 870.0, 1214.0], 82.0))`.
- The pins had no path: they took the Full Build's way reversed, up 30 (generated Step 20c: `J_*_M [[0,0,0],[0,30,0]]`).
- This is the mechanism to reuse now: matrix off with `let_go=SOCKETS`, then pins and sockets together.

## (3) published-takeapart.json, Steps 14 and 15

The arrow directions come from `published_steps.txt` (tip points).

- **Step 14 (D10)**
  - Camera: `view_dir [-0.5194, 0.5906, -0.6177]`, target `[645.61, 909.86, 1212.47]`, radius 78.24, fov 45.
  - Arrow: tail `[604.07, 945.65, 1204.58]`, length 50.76, width 4.431, straight down (tip `(603.3, 894.9, 1204.6)`). The tail lies
    inside D10, at its D4 end.
  - Eye: on 'D10 copy', ring `[600.49, 954.31, 1202.11]`, on the hook at the D4 end on the camera's side. No close-ups.
  - The scene: the matrix copy at `(0.0, 56.6, -0.5)`. D10 copy `turned((0,1,0), 180, at=(638.5, 891.9, 1204.5), t=(-0.2, 57.0, -0.9))`
    drops `(0, -48.4, 0)` and is gone in 14c. Everything else is hidden; only the matrix, D10, the six caps and the three loose wires
    are shown.
- **Step 15 (the connectors)**
  - Camera: `view_dir [-0.7915, 0.4034, 0.4592]`, target `[643.34, 915.65, 1202.28]`, radius 57.52.
  - Arrow: tail `[618.77, 931.36, 1230.72]`, length 31.55, width 3.453, along +Z (tip `(619.4, 929.5, 1262.2)`), 20 mm under the
    board.
  - Eye: on 'J_PURPLE_F copy', ring `[609.71, 948.77, 1182.01]`. No close-ups.
  - The transition moves the three wires, three pins and three sockets `(0, 0, 30.5)`. Step 15c shows the matrix only.
- **Both views were aimed at a matrix at our P_HELD** (`HOVER = [0, 56.64, -0.52]` against P_HELD `[-0.2, 56.64, -0.32]`). With the
  matrix kept held, `cam('Step 14')` and `cam('Step 15')` apply directly. `HOVER`, `to_laid`, `laid_cam` and `LAID_VIEW` are no longer
  needed. Our scene also shows the box, which the published scene had hidden.

## (4) Proposal

The new Steps 10 - 13 replace lines 248 - 276. Step 9 (lines 242 - 247) stays as it is; only its comment changes ("then set down on
the table beside the box by a fade" goes).

```python
# ================================================================ THE LED MATRIX OUT OF THE BOX, STILL WIRED, AND OFF ITS WIRES
# (Step 9 as now.) It stays held over the box until it is off its wires: the published guide shows it there for D10 and the
# connectors (its Steps 14 and 15, the matrix at [0, 56.6, -0.5]: our P_HELD within 0.2 mm), so those cameras are the published ones.

# D10's hooks hold both edges of the matrix (the Full Build hooked it on there, its Step 31: up under the matrix held over the box,
# then slid along until they held both edges). Lee, 22 Oct 2026: "D10 must slide off of the LED Matrix": the Full Build's Step 31
# reversed, slid 40 mm along the matrix toward D2, away from its pins, until the hooks come free (a catch at the D5-end hook, 0.39 mm:
# feasibility), then down 22 mm, where the Full Build brought it up from. The wires keep the Full Build's held shape, which lies dead
# straight through D10's notch all along the slide (rulebook: a wire a part slides along lies dead straight there); laid on the
# table (21 Oct) they dipped into D10.
D10_FREE, D10_DOWN = VIEW['Step 31c']['carry'][D10]['via'][0], VIEW['Step 31']['carry'][D10]['pose']   # ([0, 0, 40], [0, -22, 40]: on the matrix)
on_matrix = lambda rel: compose(where(MATRIX), rel, g._pivot(D10))
g.remove('Slide D10 along the bottom of the LED Matrix, away from its pins, until its hooks come free of the edges. Then, remove it.', [D10],
         path=[on_matrix(D10_FREE), on_matrix(D10_DOWN)],
         arrow_style={D10: dict(dims=(40.0, 4.4), stage=0,           # (the slide: from D10's face toward D2, at its D4 end, below its
                                at=r1(apply_pose(where(D10), [[599.5, 880.0, 1206.5]])[0]),   #  lower edge: [599.3, 936.6, 1206.2])
                                then=[arrow('Step 14', stage=1,      # (the drop, the published size: in front of D10, toward the camera,
                                            at=r1(apply_pose(on_matrix(D10_FREE), [[599.5, 880.0, 1202.4]])[0]))])},   # where the Full
         #                                                             Build's Step 31 arrow starts: [599.3, 936.6, 1242.1])
         eye=[dict(id=D10, anchor=[600.7, 897.7, 1203.0], side='up-left')],   # (the published eye: the hook at D10's D4 end)
         **cam('Step 14'))

# The matrix pulled back along its pins, off the three connectors, which stay where they came off (let_go, as the PMG's displays off
# their wires' caps); the wires stay in the breadboard as they are. Then it is gone.
g.remove('Disconnect the three breadboard wires from the V+, IN, and V- pins on the LED Matrix, and remove the LED Matrix. '
         'Leave the wires in the breadboard.', [MATRIX], let_go=SOCKETS,
         path=[_shifted(where(MATRIX), [0.0, 0.0, -30.0])],         # (as the PMG's: 30 mm back along its pins; the pins are 6.8 mm in)
         arrow_style={MATRIX: arrow('Step 15', at=[600.0, 952.0, 1231.0])},   # (the published size, at the published tail's z, beside the
         #                                                             matrix's edge on the camera's side: a plate moving along itself)
         eye=[dict(id=WS.FEMALE['purple'], side='up-left')],        # (the published eye)
         caution='Hold the three black connectors while you pull the LED Matrix off its pins. Do not pull on the wires themselves.',
         **cam('Step 15'))

g.remove('Remove both D9 pieces from the slots in D2 and D3.', [D9_A, D9_B],    # (before the wires, as published: they lie under D9_A)
         arrow_style={D9_B: arrow('Step 10', 0), D9_A: arrow('Step 10', 1)},
         view_dir=cam('Step 10')['view_dir'], frame=([605.0, 885.0, 1210.0], 106.0))   # (unchanged)

# The three wires out of i2, i3 and b19 together (Lee's group), their free ends with them, so that each goes up whole and is gone.
g.remove('Disconnect the yellow, gray, and purple breadboard wires from i2, i3, and b19.', PINS + SOCKETS,
         paths={**{p: [[0.0, 30.0, 0.0]] for p in PINS},              # (straight up out of their holes: the Full Build's PIN_HOVER)
                **{s: [_shifted(where(s), [0.0, 30.0, 0.0])] for s in SOCKETS}},
         arrows=[], eye=[eye('Step 13'), eye('Step 12')], caution=PULL, **cam('Step 11'))   # (as today's Step 12: an eye on i2 / i3, one on b19)
```

### Why each piece, and what was checked from the data

**Step 10 (D10)**
- The path is the Full Build's Step 31 reversed, so D10 comes to rest at `[0, -22, 40]` on the matrix, where the Full Build made it
  appear. That pose is known to be clear of the wires and the box: D10's feet are at y 917.7, above D2 and D3 (top 907.03) and well
  above the D9s (top 900.69).
- **Do not drop it further.** At 59594ae's −40 the feet would be at 899.7. At the published −48.4 D10 would pass into both D9s, which
  are still in (D9 y up to 900.69 near D2).
- The wires through D10's notch:
  - notch, world: x 604.98 - 612.59, bottom y 945.7;
  - held run: y 950.97, at x 608.4 (white), 610.2 (purple), 611.9 (grey);
  - the gray wire clears the notch wall by 0.07 mm, the same as in the Full Build;
  - D10's D4-end hook, world x ≤ 607.14, clears the white wire (x ≥ 607.78) by 0.64 mm as it drops.
- Both arrows are off the end-on threshold: |d · dir| is 0.62 for the slide and 0.59 for the drop (the threshold is 0.8).
- The slide arrow's tail is behind D10's +Z face at its D4 end. From the published camera (from −X, −Z, 36° up) its line of sight
  passes just under D10's lower edge (about y 937.1 against 939.7), and on the other side of the matrix's −X edge (606.7). The
  matrix's own box is x 606.92 - 670.71 and z 1173.79 - 1234.2.
- The drop arrow at 50.8 mm ends at y 885.8, 2.9 mm beside the white wire's rise (x 605) and 5 mm above the USB cable's box
  (y ≤ 880.4).
- `dims=(30.0, 4.4)` (40dc19b's `d10_drop`) would end it above the box's top. Our drop is 22 mm, against the published 48.4.

**Step 11 (the matrix off its connectors)**
- With `let_go=SOCKETS`, the sockets rest where they are (stepgen `held_here`).
- No wire end moves, so routes 10 - 12 stay as they are.
- The matrix's only remaining rider is gone with D10.
- The pins are seated, not riding, so no lead is left with one end gone.

**What the wires look like once the matrix is gone**
- The connectors stay where they came off: under where the matrix's corner was, about 44 mm above the box's top (y about 951).
- The wires keep the Full Build's held shape: up beside the open D4 end at the D2 end of the box, and back along at y 951.
- The other existing shapes that could serve:
  - `WS.laid()`: its sockets need the laid matrix under them, and changing to it would need the sockets to move, which is a fade
    step of its own.
  - `WS.loose()`: its pins are out of the breadboard.
  - guide.py's `loose(w, True)` / OFF_PIN (Steps 10 - 15, the matrix upright at P_UP): drawn with no box around it, never checked
    against D2, D3, the D9s or the button.
  - None of them fits better than the held shape.
- If Lee does not like connectors left in the air, the alternative is a new "dropped" shape in wire_shapes.py. It would start like
  the held one (IN_BOX + UP_SIDE to SIDE_TOP, so that `tail_from` matching keeps the run in the box still), then hang to the table.
  It needs its own fade step after Step 11, and new checks: outside D2 it meets the USB cable (box z ≤ 1258.9) and the button's head.

**The matrix's slide**
- The matrix slides 30 mm over the held run, 0.61 mm under its back face (back about 952.2, wire top 951.59), and over the three
  socket tops, 0.39 mm under it (socket tops 951.81).
- The run is evidence that the back face is flat over x 608 - 613.7. The gray socket's outer 0.25 mm (to x 613.99) is not covered by
  that evidence.
- A hand-given path is not order-checked by the generator. **Check MATRIX moving −Z 30 against the three sockets** (part against part:
  `blocked()` as feasibility.py does), then run motioncheck.
- The safer variant is the first draft's two stages: `path=[_shifted(where(MATRIX), [0, 0, -15.0]), _shifted(where(MATRIX), [0, 30.0, -15.0])]`
  with `then=[dict(dims=(31.6, 3.5), stage=1)]`.

**The arrow for Step 11 is reversed from the published one, on purpose**
- It points −Z on the matrix, where the published arrow points +Z on the connectors.
- Here the connectors cannot move: their wires run on from them along +Z.
- Moving the connectors instead (the published motion) would need three new, shortened routes and a second step to remove the
  matrix, because `let_go` parts cannot also move in the same call.

**Close-up and eye for Step 11**
- From `cam('Step 15')`, 24° up from the −X side, the connectors are mostly hidden under the board's edge.
- The published guide relies on the eye. The first draft's close-up could be added on Step 11:
  `inset=dict(target=r1(np.mean([apply_pose(where(s), [g._pivot(s)])[0] for s in SOCKETS], axis=0)), dir=[-0.3, 0.8, 0.52], radius=10.0, mark=5.0, ghost={MATRIX: 0.15}, caption='The three connectors', alt=...)`.
  The target is about `[610.58, 950.93, 1186.96]`.

**The order (D9s before the wires)**
- The figures are in the summary, point 3.
- The D9s lifting 65 mm with the connectors in the air: D9_A (x ≥ 617.13) passes the gray socket (x ≤ 613.99) by 3.1 mm and the run
  (x ≤ 613.74) by 3.4 mm.
- D9_A's published arrow (x 618.76 ± 1.7, up to y 953.3) also passes the run by about 3.4 mm.
- The wires under D9_A are below it, and it moves away from them.

**Step 13 (the wires out)**
- Both ends move by the same +30 Y. Points before `b_from` move wholly with `a`, and the rest blend between `a` and `b`
  (player.js `skinned`), so each route is carried up whole.
- The pins clear the USB plug: "the purple pin is 3.4 mm and its wire 4.5 mm clear of the plug in the current model" (feasibility
  P11-13: FREE).
- The caption is kept word for word from today's Step 12, so its `text_key` stays. There is no `step-text-deconstruction.json` in the
  kit folder.

### To clean up with it

- Lines 138 - 146 (`HOVER`, `to_laid`, `laid_cam`), `LAID_VIEW` and `LAID` (lines 264, 268), and `g.put_away([MATRIX])` (line 276)
  are no longer used. `put_away` of a part already removed would likely fail.
- The `WS.LAID_POSE` half of the assert at line 112 can go.
- `WS.laid / loose / pin_pose / socket_pose` are no longer called. Only `WS.MALE / FEMALE / JUMPERS` remain in use. wire_shapes.py's
  docstring and `scenes()` describe the old flow.
- Texts that describe the old flow and need rewording:
  - **deconstruction.py docstring** (lines 9 - 27): "set down beside the box", "the matrix on its own: D10 off", "D10 unclipped
    straight down"; the fades; and "Steps 10 and 11 framed to hold the laid matrix".
  - **CLAUDE.md, the LSM deconstruction paragraph**: "the LED matrix lifted out with D10 and set down beside the box still wired ...
    Setting the matrix down and unplugging the three wires are fades".
  - **README.txt.**
  - **docs/cadasio-patterns.md** lines 291 - 292 and 329 - 330: "D10 dropped straight off the matrix through its hooks, not slid
    along first". Lee's new note reverses this. Suggested rule: a part that hooked on by sliding comes off by sliding, in a pose where
    its wires lie straight along the slide; here, the matrix held over the box.
  - CLAUDE.md and the rulebook already have uncommitted changes from the LAC session. Edit them; do not overwrite them.

## Flags (unsure, or to verify in the browser)

1. **The arrows' tails** (`[599.3, 936.6, 1206.2]`, `[599.3, 936.6, 1242.1]`, `[600.0, 952.0, 1231.0]`) are worked out from part boxes
   and lines of sight, not seen. Check them on screen at 1280 x 800, 1024 x 768 and 768 x 1024. Also check that the eyes' leaders do
   not cross the arrows: `side='up-left'` is a guess.
2. **The eye on D10.** The published eye's ring was on a turned copy. `[600.7, 897.7, 1203.0]` is that ring moved into our D10's frame
   (the shift of P_HELD), with z set onto D10's −Z face. It falls inside our D4-end hook's span (x 594.01 - 607.34). Check that it
   sits on the hook.
3. **The matrix's −Z 30 slide over the gray socket's outer 0.25 mm** has not been checked part against part (see above). Run the part
   check and motioncheck (`tools/motioncheck.py "LSM Build Instructions" steps-deconstruction.json`) on the new Steps 10 - 13, and
   wirecheck.
4. **The connectors in the air** from Step 11c to Step 13 may look odd to Lee. The PMG precedent (Lee-approved, live) is the same
   thing on a bench. The alternative is above.
5. **The 0.04 mm rounding.** steps.json rounds the matrix's pose to `[-0.2, 56.6, -0.3]`; the held routes were drawn at
   `[-0.2, 56.64, -0.32]`. This already exists in today's Step 9c, and the gray wire's 0.07 mm to the notch wall is not changed by it
   (x is the same).
6. **Cameras.** `cam('Step 14')` and `cam('Step 15')` frame scenes the published guide had emptied. Here the box and breadboard show
   below, and nothing should be hidden; the published Step 14 target is low (y 909.86), framing the drop.
   - The alternative for Step 10 is the Full Build's Step 31 camera, which Lee framed himself
     (`[-0.6875, 0.4904, -0.5355]`, `([631.8, 932.6, 1218.0], 63.4)`).
   - The D9 step's camera is kept as it is (house rule: no unnamed step's camera changes), though its comment about "the laid matrix"
     no longer applies.
7. **Step numbers.** After this change, Lee's other notes of today point at Steps 14 (D3), 15 (D2) and 19 (the nut).
