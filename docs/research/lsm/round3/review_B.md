# LSM Full Build, Lee's round 3: independent review, group B (Steps 15 - 25)

Reviewed 19 Oct 2026 from `LSM Build Instructions/steps.json` (now) against the round-2 file (`steps_r3_before.json`), the guide
diff, the renders in `LSM Build Instructions/thumbs/`, and Lee's picture 4. Numbers come from light Python: the player's own camera
formula (`player/js/core.js` `cameraPose`, fov 45, padding 1.08) projected onto a 1440 x 803 frame. It matches the renders to within
5 px (i2 tip computed (570, 727), drawn (572, 722); V+ tip computed (819, 131), drawn (818, 128)). Part geometry comes from `lsm.glb`
(numpy reader, no build). I ran nothing heavy, used no browser and changed nothing in the repository except this file.

## Verdicts

| # | Lee's note | Verdict |
|---|---|---|
| 1 | Steps 15 - 17: the LED matrix upright, so that the header connection and the breadboard holes show together | done |
| 2 | Steps 15 - 17: a lead line (hole label) to the breadboard connection on each step, besides the eye and the pin's leader | partial (Step 16) |
| 3 | Step 18: the arrow starts at the nut's rear surface and no longer runs into the nut | done |
| 4 | Step 22: camera as in image 4 | done |
| 5 | Step 23: is the USB A end the right size? | done (answered, no change) |
| 6 | Step 23: zoom in a little | done |
| 7 | Step 24: same view as Step 23 | done |
| 8 | Step 25: D4 comes in downward, not in towards D1 | done, with an 8 mm push at the end (explained below) |
| 9 | Step 25: same view as Step 23 | done |

### 1. Steps 15 - 17: the matrix upright (done)
- The MATRIX pose for Steps 15 - 17 turns the board's normal from +Y to (0.423, 0, 0.906), which is horizontal, so the board stands
  upright. Posed, it spans x 637 - 696, y 887.8 - 948.2 and z 1203.8 - 1232.5. That keeps it 3.3 mm above the Nano's highest point
  (y 884.52) and clear of everything on the breadboard.
- Views Step 15, 15c, 16, 16c, 17 and 17c share one camera: dir [-0.3592, 0.449, -0.8182], target [643, 906, 1203], radius 48 (the
  round-2 camera was [0.757, -0.154, -0.635], r 30). The camera sees the back of the board (dot product with its back normal 0.89).
- `z_Step15.png` and `f_Step15c.png` show the header and pins at the top right, with i2/i3 (bottom left) and b19 (right) in the same
  frame.
- The pins are as large on screen as before: V+ to V- spacing is 34.8 px now, 38.1 px in round 2 (1440 px frame).
- Ray tests from the camera: the white pin housing in i2 and the grey one in i3 are visible. Nothing stands in front of them but their
  own housings.

### 2. Steps 15 - 17: a hole label on each step (partial)
- Each step has its hole label: Step 15 `i2` [650.08, 871.92, 1170.45], Step 16 `b19` [627.04, 871.92, 1213.63], Step 17 `i3`
  [650.08, 871.92, 1172.99]. Each also keeps the pin label (V+, IN, V-) and the eye on the socket. These are the holes Steps 11 - 13
  used.
- **Step 16:** the `b19` leader ends on the 330 Ω resistor, not on the purple wire's pin.
  - From this shared camera, b19 is hidden behind R330. The ray from the camera to the anchor passes through R330 11.8 mm before it
    reaches the hole.
  - In `z_Step16.png` the dashed circle sits on the resistor's end cap at about (845, 580). The purple pin's housing is visible just
    above it, at about (840, 550).
  - Lee will most likely read "b19" as pointing at the resistor.
  - A possible fix: put the label's anchor on the visible side of the purple pin housing, e.g. [627.04, 875.5, 1213.63]. The ray to
    [627.04, 875.0, 1213.63] is clear and projects to (840, 568).
- Step 15's `i2` tip sits at the foot of the white pin housing, beside the capacitor, and is clearly visible (crop of `z_Step15.png`).
- **Evidence gap:** there is no render of Step 17 (hover) with its `i3` label; only 17c is rendered. By projection the i3 tip lands at
  (580, 714), on the grey pin housing, which is not hidden. Placement and crossings are not checked visually.

### 3. Step 18: the arrow from the nut's rear surface (done)
- The nut in `lsm.glb`, seated, spans z 1250.43 - 1251.93 and reaches x 648.74 at the axis height. In Step 18 it rides +3.1 mm on the
  button, so it spans z 1253.53 - 1255.03.
- Round 2's arrow tail was at z 1255.12. Its body (x 647.23 - 651.23, width 4) therefore ran through the nut's whole thickness at its
  corner.
- The arrow now runs from z 1253.42 to 1196.42. Its tail is 0.11 mm behind the rear face (the face away from the camera, which is on
  the +z side), so it no longer overlaps the nut anywhere.
- It clears the button body (x max 646.66) by 0.57 mm.
- `f_Step18.png` (zoomed): the tail comes out from behind the nut's lower right corner, flush with its back edge.

### 4. Step 22: camera as in image 4 (done)
- Step 22 and 22c share dir [0.6491, 0.6967, -0.3055], target [653.7, 892.4, 1204.6], radius 35.5.
- `ov-4.png` (render over Lee's screenshot): the edges almost coincide.
- On screen, measured from the centre in frame heights, the button sits 0.685 in Lee's picture and 0.69 in `f_Step22.png`. The
  vertical scale also matches (the breadboard takes 69 % of the height vs 66 %).
- Step 21's camera is unchanged.

### 5. Step 23: USB A end size (done: answered, no change)
- The A end is the MRA's `usb-a-end.glb`, placed with a rotation and a translation only (`assemble.py` line 330, no scale). In the
  model it measures 49.7 x 15.9 x 8.55 mm, which matches the stated answer (16 x 8.5 x 50 mm, true to the CAD).
- The impression Lee had will not go away, and the new camera makes it slightly stronger:
  - The A end is nearer the camera than the base. Perspective enlarges it by 1.17 relative to the base (1.15 before).
  - The new target moved towards it, so it grew on screen more than the base did: 157 -> 195 px wide (+24 %), against 236 -> 276 px
    (+17 %) for the breadboard (1440 x 803).

### 6. Step 23: zoom in a little (done)
- Radius 148.7 -> 125.0 (x 0.84). Target [640.9, 881.6, 1232.8] -> [630.0, 880.0, 1228.0]. Direction unchanged.
- The base is about 17 % larger on screen, a "little" closer as asked.
- The framing is still set by the A end lying on the table about 130 mm from the base, so the step's subject (the Mini-B plug) stays
  small. See the regressions section: the reason that A end was moved 60 mm further out no longer exists.

### 7. Step 24: same view as Step 23 (done)
Step 24 and 24c have exactly Step 23's camera (dir, target, radius).

### 8. Step 25: D4 comes down (done, with an 8 mm push at the end)
- The path is [-8, 65, 0] -> [-8, 0, 0] -> 0: D4 appears 65 mm up (and 8 mm out) and comes straight down, then goes 8 mm on towards D1.
- I checked the geometry:
  - At x -8, D4 spans x 586.41 - 589.41. That clears D1's tab tips (x 593.78) by 4.4 mm and D2's tabs (x 590.58) by 1.2 mm.
  - D4's notch is open from its foot up to y ~868, at z 1216.5 - 1221.25 (measured in `lsm.glb`). Where D4 comes down, the USB cable
    (radius 1.75) lies at y 862.6 - 863.4 and z 1219.5 (route 40), so it passes up the notch with no contact, as `motioncheck` also
    found.
  - The push itself is needed: D1's and D2's tabs go into closed slots.
- Lee will see that second beat towards D1, which is what the note said "instead of". The explanation (closed slots; the published
  guide pushes it on too) has to reach Lee with this round.
- Nothing on screen draws the 8 mm push except the four lead lines, which now slant about 7 degrees from upright.
- Caption: "Lower D4 down beside ..." says the same thing twice ("Lower ... down").

### 9. Step 25: same view as Step 23 (done)
Step 25 and 25c have Step 23's camera exactly (`review_camdiff.txt` lists Step 25 as NEW only because its caption changed).

## Regressions and other findings, in and next to these steps

1. **Step 16, b19 leader on the 330 Ω resistor (new this round, medium).** See item 2. The label was added this round, and the shared
   Step 15 - 17 camera hides b19 behind R330.
2. **Step 18, the arrowhead cuts into the black lead (pre-existing, low-medium).** The arrow lies flat in the plane y 881.63. The black
   lead runs straight along z at x 641.93, y 881.65, radius 0.62. The head (16 mm wide, 13.6 mm long, base at z 1210.02) has its inner
   barb inside the lead for about 2.2 mm (z 1207.8 - 1210.0, x 641.23 - 642.55). You can see it in `f_Step18.png` at about (735-760,
   405-415). It is the same kind of "passes into" that Lee just flagged on the nut. This round did not cause it: round 2's head was the
   same, 1.7 mm further along. Moving the arrow 1.5 - 2 mm towards +x (x 650.8 - 651.3) would clear it.
3. **Step 23, the A end is more prominent (low).** It grew 24 % on screen against 17 % for the base (item 5), in the step where Lee
   said it looks oversized.
4. **Steps 23 - 25, the A end is still 60 mm further out than the first draft (low, a suggestion).** `assemble.py` (comment above line
   330) says it was moved 60 mm "so that D4, held 65 mm out before it goes on, has the cable in its notch rather than the A end". D4 now
   comes from above, so that reason is gone. The A end's distance is what keeps Steps 23 - 25 zoomed out. Bringing it back would let
   all three frame closer on the base (Lee's call: it moves the cable in every later step).
5. **Steps 15 - 17, the caption box over the matrix's top edge (low).** In the whole-page composite at 1152 x 720 (`p_Step16.png`), the
   instructions box (to x 518, y 78) covers the top-left strip of the matrix, whose top edge is at y ~50. The header (x 620 - 660) is
   clear. In Lee's 2000 px wide window the box's right edge just reaches the matrix's top-left corner.
6. **Step 25 caption: "Lower D4 down" (low).** It says the same thing twice.
7. **No unnamed camera changed in this group.** Steps 18 - 21, 26 and the Step 14 card are as in round 2.
8. **The wires in Steps 18 - 25 have the same shape at rest.** Only the blend data changed (`stretch`, `b_from`, `tail_from`), and that
   matters only where the route changes (Step 26, another group).
9. **Wires at rest and in motion.** `wirecheck` found nothing in any of these views. `motioncheck` found nothing here either; its only
   findings are in 26c and 32c.

## Files
- Renders looked at: `thumbs/z_Step15.png`, `z_Step16.png`, `f_Step15c.png`, `sheet_1.png`, `sheet_2.png`, `f_Step18.png`,
  `f_Step22.png`, `ov-4.png`, `f_Step23.png`, `v_Step25.png`, `v_Step25c.png`, `p_Step16.png`; Lee's
  `docs/research/lsm/lee_images_2026-10-19b/4.webp`.
- Guide lines: `LSM Build Instructions/guide.py` 211 - 216 (P_UP), 448 - 454 (PIN_VIEW, the hole labels), 513 (the Step 18 arrow),
  549 - 556 (LEAD_CAMERA), 581 - 599 (BASE_CAMERA, the D4 path and caption); `assemble.py` 325 - 331 (the A end).
