# How the LSM Full Build brings D10, the LED matrix and its three wires together, and whether D10 can slide off along the same wires

Read-only study, 22 Oct 2026, for Lee's note on the deconstruction's Step 10: "D10 should be removed at this point and the wires
disconnected from the LED Matrix in a group, but left attached to the breadboard, then the breadboard wires moved. Remember, D10 must
slide off of the LED Matrix".

Sources: `LSM Build Instructions/guide.py`, `steps.json` (Full Build, 82 views), `steps-deconstruction.json` (53 views, the working
copy as of this morning), `wire_shapes.py`, `assembly-report.json`, `docs/cadasio-patterns.md`. No model was loaded. Clearances were
worked out in pure Python from the route points in `steps.json`, sampled every 0.2 mm, against D10 drawn as boxes from its bounds and
its notch (see "D10's shape" below).

Conventions: assembly mm, Y up. "Matrix frame" means seated coordinates: a point minus the matrix's pose, which is a pure shift
wherever it matters here. D10 rides on the matrix, so its seat in the matrix frame is its own seat. Wire ids in code: `white` (drawn
and named yellow), `grey` (gray), `purple`. Caps: pins `J_WHITE_M`, `J_GREY_M`, `J_PURPLE_M` (in i2, i3, b19); sockets `J_WHITE_F`,
`J_GREY_F`, `J_PURPLE_F` (on V+, V-, IN).

## Answer first

**Yes. The wires are in exactly the same place relative to the matrix, so the difference is 0.00 mm.** The Full Build's `Step 31`,
`Step 31c` and `Step 32` all use routes **59 / 60 / 61** (`HELD`, guide.py:742) for white / grey / purple. All three show the matrix at
the same offset, `[-0.2, 56.6, -0.3]` (guide.py's `P_HELD = [-0.2, 56.64, -0.32]`, line 224, rounded in steps.json). The
deconstruction's `Step 9c` and `Step 10` use routes 10 / 11 / 12. These are point-for-point identical to 59 / 60 / 61 (350, 337 and 248
points, largest difference 0.0 mm, same `b_from`, `b_ref` and `tail_from`), with the matrix at the same `[-0.2, 56.6, -0.3]`, D10 at
`[0, 0, 0]` on it, and the sockets at `[0, 0, 0]` on it.

So sliding D10 off from the deconstruction's Step 9c state, by the Full Build's Step 31 motion reversed, plays the Full Build's own
Step 31 backwards. It uses the same wires, the same matrix pose and the same D10 relation. Lee has raised no wire-into-D10 problem in
the Full Build's Step 31.

The earlier failure (Lee, 22 Oct: "The breadboard wires are occluded into D10") happened because D10 was slid with the matrix laid on
the table. The wires then had the deconstruction's LAID or LOOSE shapes, which leave D10's notch 15 - 21 mm along the slide (see the
last section).

## D10's shape (from the files; no mesh read)

- D10's bounds, seated (`assembly-report.json`): x 594.01 - 682.91, y 883.12 - 900.68, z **1202.97 - 1205.97** (3 mm plate across Z).
- The notch the wires lie in (`wire_shapes.py:134 - 135`): x **605.18 - 612.79**, from y **889.10** up. guide.py:730 says "D10's
  slot ... x 605.2 - 612.8".
- The LED matrix, seated (`assembly-report.json`): x 606.92 - 670.71, y 893.06 - 898.10, z 1173.79 - 1234.20. Its back face is at
  y 895.60: the pins (y 894.333) lie "1.27 mm under the back face" (guide.py:465).
- For the clearance figures I drew D10 as three boxes, each taken at its worst case:
  - A: x 594.01 - 605.18, up to y 900.68 (D10's end and hook beside the matrix's -X edge).
  - B: the notch floor, x 605.18 - 612.79, y up to 889.10.
  - C: the body under the matrix, x > 612.79, up to the back face 895.60.

  The true outline can only give more room than this.

## Every Full Build step that moves D10, the matrix, or the three wires' caps

Cameras are as written in steps.json: `dir`, `target`, `radius`.

| Step | Caption | What moves, and how | MATRIX offset, Step N -> Nc | Wire routes, N -> Nc (wire_via) | Camera |
|---|---|---|---|---|---|
| 10 | Pull apart both ends of the three-wire jumper ribbon ... | The ribbon on its own, far from the box. The pins and sockets ride on `J_WHITE_M`, which lies at `lying_pin`. `split_ride` spreads them: for example `J_GREY_M` on the carrier goes from `[0,0,-0.6]` to `[0,0,3.5]` and `J_PURPLE_M` from `[23,0,-39.4]` to `[23,0,-31.2]`. | not shown | 16/17/18 -> 16/19/20 | [-0.5792, 0.5736, -0.5792], [662, 925, 1106], 50.5 |
| 11, 12, 13 | Push the yellow / gray / purple wire's pin into i2 / i3 / b19 | Each pin, `path=[PIN_HOVER, ZERO]`: `[0,30,0]` -> 0, straight down 30 mm (-Y). The sockets wait at `f_pose(w, P_UP, SOCKET_OFF)`. | not shown | 11: 21/22/23 -> 24/25/23; 12: -> 24/26/23; 13: -> 24/26/27 | 11, 12: [-0.3282, 0.6298, -0.704], [644.3, 895.7, 1180.6], 38.3; 13: [-0.5792, 0.5736, 0.5792], [627.0, 892.0, 1213.6], 34.0 |
| 14 | Find the three pins on the back of the LED matrix ... | Nothing moves (`flip`, `single`, `staged`). | shown on its own | none | [-0.1802, -0.8011, 0.5708], [628, 895, 1199], 36 (flip) |
| 15, 16, 17 | Push the yellow / purple / gray wire's socket onto the V+ / IN / V- pin ... | The socket rides on the matrix: carry `SOCKET_OFF = [0,0,15]` -> `ZERO` (section 2). | `P_UP` = {t [28.12, 22.43, 13.29], r [0.954201, 0.211541, -0.211541, 92.6851], at [638.82, 895.58, 1203.99]}, same in N and Nc | 15: 24/26/27 -> 28/26/27; 16: -> 28/26/29; 17: -> 28/30/29 | [-0.3592, 0.449, -0.8182], [643, 906, 1203], 48 |
| 21 - 25 | (the button's leads, USB, D2, D4) | The matrix reappears at Step 21 (after `put_away` at Step 17) at `P_BESIDE`, riding on the breadboard. It does not move. | `P_BESIDE` = {t [91.01, -21.66, 11.37], r [0,1,0,180], at MC} | 33/34/35 throughout | (the steps' own) |
| 26 | Lift the LED matrix over D4, turning it round, and lay it down outside ... | Matrix ride `[P_UP_BESIDE, P_MID, P_UP_OUTSIDE, P_OUTSIDE]`, four beats (D4 is given `[ZERO]*5`) | `P_BESIDE` -> `[-90.8, 5.9, 25.1]` (`P_OUTSIDE` [-90.76, 5.89, 25.09]); vias {t [91.01,25,11.37], Y 180}, {t [-26,25,18], Y 90}, [-90.8, 25.0, 25.1] | 33/34/35 -> 53/54/55 (via 44-46, 47-49, 50-52) | [0.0, 0.9961, 0.088], [638.5, 880, 1205], 82 |
| 30 | Pick up the LED matrix and hold it over the box, LEDs up. | Matrix ride `[P_LIFT, P_HELD]`, two beats: up 50.75 mm (+Y), then +90.56 X, -25.41 Z | `[-90.8, 5.9, 25.1]` -> **`[-0.2, 56.6, -0.3]`**, via `[-90.8, 56.6, 25.1]` | 53/54/55 -> **59/60/61** (via 56/57/58) | [-0.5792, 0.5736, -0.5792], [601.0, 910.9, 1204.6], 114.8 |
| **31** | Hook D10 under the LED matrix: hold it under the matrix, then slide it along until its hooks hold both edges. | D10 only (section 1). `moving: ['D4']`, a way that stays put, `[ZERO]*3`, gives the step two beats. | `[-0.2, 56.6, -0.3]` in both | **59/60/61** in both, no wire_via | [-0.6875, 0.4904, -0.5355], [631.8, 932.6, 1218.0], 63.4 |
| **32** | Lower the LED matrix, with D10, into the box ... | Matrix `path=[P_HELD, via(P_HALF), ZERO]` = `[[-0.2,56.6,-0.3], [-0.1,28.0,-0.2], [0,0,0]]`, `stops [0, 2]`: one beat, 56.6 mm down. D10 and the sockets ride at `[0,0,0]`. | `[-0.2, 56.6, -0.3]` -> seat | **59/60/61** -> 65/66/67 (via 62/63/64, `HALF`) | [-0.5792, 0.5736, -0.5792], [636, 912, 1210], 66; inset on 32c: target [612, 892, 1203], dir [0.1504, 0.5013, -0.8521], r 15, ghost MATRIX 0.12, D4 0.25 |

D10 is not in any view before Step 31, and only Step 31 moves it relative to the matrix.

### 1. Step 31: D10 slid onto the held matrix

- **The matrix.** It is held over the box at `P_HELD = [-0.2, 56.64, -0.32]`, a pure shift, written `[-0.2, 56.6, -0.3]` in Step 31
  and 31c. It stays there for the whole step.
- **D10's poses, riding on MATRIX** (guide.py:752 - 758):
  1. Start, where it appears: `carry(..., pose=D10_UNDER)` with `D10_UNDER = [0.0, -22.0, 40.0]`.
  2. A stop: `[0.0, 0.0, 40.0]`.
  3. End: `ZERO`.

  `ride={D10: [[0.0, 0.0, 40.0], ZERO]}`, without `via()`. Both are stops, a beat each ("Two beats ... up and then along", guide.py:755).
  steps.json Step 31c shows this as `carry D10 {pose [0,0,0], via [[0,0,40]]}`.
- **The same poses in the world:**
  1. `[-0.2, 34.64, 39.68]` (steps.json Step 31: `[-0.2, 34.6, 39.7]`)
  2. `[-0.2, 56.64, 39.68]`
  3. `[-0.2, 56.64, -0.32]`
- **The move before the slide:** **22.0 mm straight up (+Y)**, at z + 40. There D10's faces are at seated z 1242.97 - 1245.97,
  8.77 mm beyond the matrix's +Z end (1234.20).
- **The slide:** **40.0 mm along -Z** (toward D3) to its seat (faces z 1202.97 - 1205.97). The hooks run along the matrix's X edges.
- **The arrow.** Tail `[599.3, 914.64, 1242.08]`, head `[599.3, 914.64, 1215.68]`: 26.4 mm along -Z, on D10's start place, the slide
  only. Label `D10` at `[632.5, 893.3, 1203.0]`.
- **How the wires lie: dead straight along the slide** (rulebook line 204: "a wire that a part slides along lies dead straight there,
  past where the part comes in"). The wires lie in `HELD_TAIL` (guide.py:736 - 741). In the matrix frame (routes 59 - 61 minus
  `P_HELD`):

  | wire | x in D10's slide zone (seated z 1202.97 - 1245.97) | y | straight run (y 894.33 +- 0.02) | then |
  |---|---|---|---|---|
  | white | 608.58 - 608.61 | 894.24 - 894.46 | z 1195.75 - 1253.37 | hairpin up and over at z 1253 - 1259; its rising leg at z 1250.4 - 1250.7 (y 850 - 870) |
  | purple | 610.39 - 610.42 | 894.24 - 894.45 | z 1195.74 - 1253.25 | rising leg at z 1249.0 - 1249.3 |
  | grey | 612.05 - 612.19 | 894.25 - 894.45 | z 1195.01 - 1244.37, then within +-0.14 mm of 894.33 to z 1253.35 | rising leg at z 1247.6 - 1247.9 |

  Each run lies at least 0.52 mm under the matrix's back face (wire top at most 895.08, against the face at 895.60) and 4.5 mm over the
  notch's floor. From each socket's far end (seated z 1191.26) it runs straight along +Z, past where D10 comes up (z 1243 - 1246), then turns up
  in a hairpin behind it.
- **Clearance to D10 over the whole Step 31 motion** (box model, wire radius 0.62; the same backwards):

  | wire | rise (22 mm at z + 40) | slide (40 mm) | at the seat | nearest |
  |---|---|---|---|---|
  | white | 2.80 mm | 2.79 mm | 2.79 mm | the notch's -X wall (box A) |
  | purple | 1.77 mm | 1.76 mm | 1.76 mm | the notch's +X wall (box C) |
  | grey | **0.07 mm** | **0.04 mm** | 0.04 mm | the notch's +X wall, x 612.79 (box C), along the whole slide |
  | rising legs behind D10 during the rise | white 3.84, purple 2.45, **grey 1.05 mm** | | | D10's +Z face at the start of the rise (grey at seated [610.61, 861.04, 1247.64]) |

  The grey wire runs 0.04 - 0.07 mm off the notch's +X wall, so the fit is tight but clear. The figures come out the same with the
  matrix at the player's rounded `[-0.2, 56.6, -0.3]`: the fixed run is then 0.04 mm higher in the matrix frame. The research notes
  record that `tools/motioncheck.py` found no wire-into-part moment in the Full Build's Step 31. Its only reported touches are
  wire-to-wire, in Step 26c (twice) and Step 32c (`lee_notes_2026-10-19b.md`, `round4/review_summary.md:150`,
  `lee_notes_2026-10-22.md:50`). I did not run it.

### 2. Steps 15 - 17: the sockets onto the matrix's pins

- **The pin axis.** In the matrix's own (seated) frame the pins point **+Z**: from the header at the board edge (z 1173.785) toward the
  middle, tips at z 1190.06 (`PIN_TIP_Z`, guide.py:466). A socket's open end `F_TIP` is at z 1183.26 and its far end `F_EXIT`, where its
  wire leaves along +Z, is at z 1191.26. The sockets are at x 608.24 (V+, white), 610.78 (IN, purple), 613.32 (V-, grey), at y 894.333.
- **The travel.** Each socket rides on the matrix from `SOCKET_OFF = [0.0, 0.0, 15.0]` (guide.py:225) to `ZERO`: **15.0 mm along the
  matrix's -Z**. With the matrix at `P_UP` (upright), the matrix's +Z is assembly **[0, -1, 0]**, so the pins point straight down and
  each socket goes **15.0 mm straight up (+Y)**. steps.json shows `J_WHITE_F` t going from [30.46, 25.41, 41.81] to [30.46, 40.41,
  41.81] between Step 15 and 15c.
- **The labels.** V+ / IN / V- are at `F_TIP` ([608.24 / 610.78 / 613.32, 894.33, 1183.26]); i2 / b19 / i3 at y 877.0. There is an eye
  on the socket.
- **At `P_HELD`** (a pure shift) the same axis is assembly **+Z**. A socket pulled off there moves +Z (toward D2), the direction its
  own wire leaves it and the direction of the straight run. The deconstruction's current Step 14 pulls them 30 mm the same way
  (`WS.PULL = [0, 0, 1]`, `socket_pose(..., off=30.0)`).
  - In routes 59 - 61 only the last 6.0 mm of each wire follows its socket (`b_from` = len - 6.0: 255.20 / 245.75 / 178.41). A 15 mm
    pull with these routes left as they are would carry that end 15 mm along a run that stays put, folding the wire back on itself.
    The new Step 11 needs wire shapes of its own for the pulled-off sockets.
  - With D10 still on, the grey socket (x 612.44 - 614.19, outside the notch's 612.79 wall) would reach D10's face (z 1202.97) after
    11.7 mm of pull. That is why D10 goes first, as wire_shapes.py:32 found for the laid matrix.

### 3. Step 32 and Step 32c

| | Step 32 (N: where it began) | Step 32c |
|---|---|---|
| MATRIX | `[-0.2, 56.6, -0.3]` (`P_HELD`) | seat (no offset) |
| D10 | `[-0.2, 56.6, -0.3]`, riding on MATRIX at `[0,0,0]` | `[0,0,0]` |
| sockets | ride on MATRIX at `[0,0,0]` | the same |
| wire routes | **59 / 60 / 61** (`HELD`, the same as Step 31 and 31c) | **65 / 66 / 67** (`SEATED`), wire_via **62 / 63 / 64** (`HALF`, matrix at `P_HALF = [-0.1, 28.0, -0.16]`) |
| route records | 59: len 261.21, b_from 255.20, tail_from 154.17, b_ref `P_HELD`; 60: 251.76 / 245.75 / 146.85; 61: 184.41 / 178.41 / 78.35 | 65: 112.83 / 106.82 / 91.92; 66: 109.34 / 103.34 / 88.39; 67: 47.91 / 41.91 / 25.77 |

The deconstruction's Step 9 (`g.lift(..., wires=leads('Step 32', 'wire'), wire_via=Step 32c's via reversed)`, deconstruction.py:243 -
247) plays Step 32 backwards. `Step 9c` ends with the matrix at `[-0.2, 56.6, -0.3]` (its `paths.MATRIX` is `[[0,0,0], [-0.1,28.0,-0.2],
[-0.2,56.6,-0.3]]`), D10 and the sockets at `[0,0,0]` on it, and routes 10 / 11 / 12, identical to 59 / 60 / 61. This is the Full
Build's Step 31c and Step 32 state exactly.

## For the new Step 10 (data only)

- **The way out**, Step 31 reversed, relative to the matrix:
  1. `[0, 0, 0]` -> `[0, 0, 40]`: slide 40 mm along +Z (toward D2).
  2. `[0, 0, 40]` -> `[0, -22, 40]`: drop 22 mm.

  In the world, with the matrix at `[-0.2, 56.6, -0.3]`, that is `[-0.2, 56.6, 39.7]` then `[-0.2, 34.6, 39.7]` (exact:
  `[-0.2, 56.64, 39.68]`, `[-0.2, 34.64, 39.68]`).
- **Room at the end of the drop.** D10's lower edge is at world y 917.76: 10.7 mm over D2's top (907.03) and 17.1 mm over the D9s'
  tops (900.69). The D9s are still in at that point, and their z range (1153.68 - 1254.93) covers D10's (world z 1242.65 - 1245.65),
  so D10 cannot go much lower there. Its +Z face is 6.3 mm from D2's inner face (1251.93).
- **Wires.** Keep 59 / 60 / 61 unchanged and the matrix unmoved through the whole slide and drop. The clearances above then hold
  exactly.
- **Camera.** Lee's own camera for this motion is the Full Build Step 31's, solved from his screenshot: dir [-0.6875, 0.4904, -0.5355],
  target [631.8, 932.6, 1218.0], radius 63.4. Step 9's published camera is [-0.4752, 0.5698, -0.6705], [616.3, 882.2, 1206.6], 91.3.

## Where the earlier slide went wrong: the laid and loose shapes, in the matrix frame

Each wire's (x, y) at given seated z, walking from the socket end. "-" means the wire has already left the run.

| z | white HELD | white LAID | white LOOSE | grey HELD | grey LAID | grey LOOSE | purple HELD | purple LAID | purple LOOSE |
|---|---|---|---|---|---|---|---|---|---|
| 1203 | 608.59, 894.33 | 608.40, 893.33 | 608.40, 893.33 | 612.13, 894.33 | 611.72, 893.33 | 611.72, 893.33 | 610.41, 894.33 | 610.06, 893.33 | 610.06, 893.33 |
| 1210 | 608.59, 894.33 | 608.40, 893.34 | 608.40, 893.05 | 612.12, 894.33 | 611.74, 893.35 | 611.74, 893.05 | 610.41, 894.33 | 610.07, 893.34 | 610.07, 893.05 |
| 1220 | 608.60, 894.32 | 607.19, 893.37 | 608.40, 890.67 | 612.09, 894.32 | 611.92, 893.34 | 611.75, 890.66 | 610.40, 894.32 | 609.95, 893.35 | 610.07, 890.67 |
| 1225 | 608.60, 894.34 | **582.57, 904.55** | 608.29, **889.26** | 612.10, 894.33 | 609.70, 893.34 | 611.82, **889.26** | 610.40, 894.33 | - (out at z 1222 - 1224) | 610.07, **889.25** |
| 1230 | 608.60, 894.40 | 581.33, 905.41 | 608.00, 887.60 | 612.10, 894.40 | **579.92, 898.86** | 612.00, 887.61 | 610.40, 894.40 | - | 610.05, 887.61 |
| 1240 | 608.60, 894.45 | 581.29, 906.14 | 607.38, 884.67 | 612.10, 894.44 | 574.67, 902.64 | 612.65, 884.67 | 610.40, 894.44 | - | 609.99, 884.67 |
| 1246 | 608.60, 894.26 | 581.33, 906.64 | 607.19, 883.94 | 612.10, 894.26 | 574.06, 903.93 | 612.79, 883.94 | 610.40, 894.26 | - | 609.99, 883.94 |

- **HELD** (Full Build Steps 30c - 32, deconstruction Steps 9c - 10) stays in the notch, at y 894.33, the whole 40 mm of the slide.
- **LAID** (deconstruction Steps 10c - 12, routes 16 - 18, matrix at {t [-90.95, -26.84, 27.78], Y 180}) leaves the notch sideways
  under the matrix's -X edge at seated z 1221 - 1227 (white at x 605.23, z 1221.26; purple 604.63, 1224.03; grey 604.31, 1226.55). With
  D10 slid +Z, the wires' centre lines are inside it, outside the notch, by 15.4 mm of slide (white), 18.0 mm (purple) and 20.6 mm
  (grey); the surfaces touch a little before that.
- **LOOSE** (deconstruction Steps 12c - 13, routes 19 - 21) drops below the notch floor (y 889.10) at seated z of about 1225 (white
  [608.26, 889.00, 1225.82], purple [610.07, 889.23, 1225.07], grey [611.82, 889.16, 1225.31]) and goes on down to y 883.94. With D10
  slid +Z, all three centre lines are inside the notch floor by 19.7 mm of slide.
- **The difference from HELD** at z 1225 - 1246: LAID is out to the side in x, 26 - 27 mm for white from z 1225 and 32 - 38 mm for
  grey from z 1230 (purple has turned out by z 1224); LOOSE is 5.1 - 10.3 mm lower in y. A straight drop
  clears both (white 2.60, grey 0.44, purple 2.10 mm), which is why the deconstruction now unclips D10 straight down. Only HELD lets
  D10 slide its full 40 mm.

## Files

- Report: `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/lsm/decon/round3/fullbuild_d10_wires.md`
- The scripts and their output are in this session's scratchpad (not kept). They read steps.json, steps-deconstruction.json and the
  numbers above, nothing else.
