# Verification notes: Camera, framing and transitions (skeptic pass on dim_camera.md)

Scope: all 20 guides, 1037 viewer steps. Everything below was recomputed with my own code in
`reports/_work_verify_camera/` (nothing reused from `_work_dim_camera/` except two contact sheets I looked at).

## Method

- `base.py` / `lib.py`: my own replay of every raw payload (camera position, orbit target, quaternion, FOV, scene up-axis,
  step attributes). Move test: view direction > 0.5 deg, target > 0.5 mm or distance > 0.5 mm; a stricter quaternion + position
  test gives the identical 325 moves, and the smallest non-zero change in the whole corpus is far above threshold, so the
  threshold does not matter.
- `img.py`: my own non-background bounding box of all 1037 saved renders.
- `g3d.py` / `glib.py`: my own 3D replay (node transforms, `position` replaces the local translation, quaternion rotations,
  oriented bounding boxes projected through the step camera). Validated against the renders on 333 uncropped, annotation-free
  Step Nc frames: within 4 % of the frame on 256, within 8 % on 309 (leaf-own visibility model). The digest's
  chain-visibility model validates on only 161 of 333, so I did not use digest `visible_parts` for geometry.
- Scripts `v1.py`-`v30.py` hold each check. Class counts agree with the report: Start 19, Step N 425, Step Nc 424,
  Transition 117, card 31 (+2 overview), final 19.

## Verdicts

| ID | Verdict | Key recomputed figures | What needs changing |
|---|---|---|---|
| CAM-1 | confirmed | Camera moves on 0 of 424 Step Nc. 421 strictly number-matched pairs + 1 mis-numbered pair (LSM Part 4 [016] Step 8 / [017] Step 9c) = 422; 420 hold one camera. No up-axis or FOV change on any Nc. | "From the hover state" is not demonstrable: on 83 uncropped new-camera rigid inserts the hover frame is better centred on 29, the completed frame on 32, tie 22 (content centre y 0.45 hover, 0.51 completed). The one camera is a compromise that fits both. |
| CAM-2 | qualified | 325 moves = 266 Step N + 30 card (29 real + 1 overview) + 17 final + 12 Transition + 0 Nc. Cards 29/31 on, 30/31 off. After Start 19/19 (8-110 deg, 76-273 mm). | "Always" holds only for cards that show a 3D part: 28/28 on and 28/28 off. The 3 "LED Matrix Diagram" cards (0 parts) are the only exceptions. |
| CAM-3 | qualified | Step N moves 266/425; lead 112/149, arrow 66/86, eye 50/79, wire 36/109. wire->wire 12/85, eye->eye 2/23, lead->lead 66/94, arrow->arrow 36/53, kind change 131/151. | "Same kind = reuse" is true for wiring and eye-only steps only; rigid inserts and arrow steps re-aim about 70 % of the time even after the same kind. Out-of-frame rule is exact: against the camera actually in effect, 83 of 83 out-of-frame actions get a new camera (0 exceptions at 0 % and 2 % margin). In-frame: 182/339 move (wire 20/92, lead 66/103, arrow 56/76, eye 40/68), so "mechanical steps re-aim even if in frame" is a 2-in-3 tendency. |
| CAM-4 | qualified | 30 label-only runs, 26 without a later move, 72/79 later steps reuse, 29/30 first step sets a new camera; all 7 exceptions LSM. | 5 of the 30 runs are a single step; of 25 multi-wire runs 21 hold. "One module" is wrong: PMG Part 1 / Full [007]-[033] holds one camera across four button modules plus the shield. The unit is a wiring block in one work area bounded by cards or non-wiring steps. LAC deconstruction holds of 20 and 37 steps are eye-only un-wiring steps, not label runs. |
| CAM-5 | qualified | Effective elevation: 903/1037 in 20-50, 983 in 15-55, 15 outside 10-60, median 34.1, view mean 34.0. Kinds: lead 33.1, arrow 34.6, eye 40.6, wire 28.4. | "Higher only for a flat breadboard layout" is false: of 35 views at 48 deg or more only 8 are wiring views; 12 are eye-only prep close-ups, 5 arrow steps, 3 ghosted underside checks, 3 cards, 2 deconstruction finals, 2 other. Low band (10-20, 17 views) fits the stated purpose (7 rigid inserts, 5 cards, 3 LSM matrix-pin wires, 2 PMG decon). |
| CAM-6 | qualified | +y views: 215/299 within 15 deg of a diagonal, 41 cardinal, median offset 9.0. Title pages 19/19. | Kit-specific. LSM 108/129 (84 %), LAC 75/86 (87 %), PMG 32/84 (38 %) with 32 cardinal and median offset 21.5 deg; step-weighted PMG 58/255 diagonal vs 89/255 cardinal. PMG has no diagonal habit outside its title pages. Sideways inserts: plan angle 37-140 deg, never along the axis; 54 of 59 legs sit at 30-60 or 120-150 deg. |
| CAM-7 | confirmed | FOV 45 on 1036/1037 (LSM Part 1 [011] = 50). Roll vs declared up 0.0 deg on 1037; look-at error 0.0 deg on 1037. Animation options identical (1035 as strings, 2 typed: LSM Part 3+4 [000], Part 4 [000]). All 325 moves in 800 ms steps. | 61 of the 325 moves sit on a step with `transition: fade` (LSM and LAC only). |
| CAM-8 | qualified | Step N moves: rotation median 60.9 (IQR 21.6-83.0), 134 over 60, 58 over 90; target shift median 41.9 mm; pure pan/zoom 10/325; 341 distinct poses for 345 views. | Elevation change median 8.7 deg (IQR 3.2-14.8), over 15 deg on 59 of 238, so "within a few degrees" is too tight. 232 of 325 moves also change distance and the target shifts a median 0.15 x distance: moves are compound orbit + pan + zoom. Poses are unique within a guide but 108 of 196 distinct poses are shared between sibling guides. |
| CAM-9 | confirmed | 992/1035 on a x1.166 ladder (LSM 312/339, LAC 394/398, PMG 286/298); 93 of 99 single-level moves are exactly 1.1664 (= 1.08 squared). Alternative ratios 1.10-1.25 fit 305-544 steps. | Zoom change counts 186 / 233 are exact-ladder counts; including half-level moves gives 195 / 243 of 325. |
| CAM-10 | qualified | Fill by distance band (259 views): 0.61, 0.54, 0.63, 0.62, 0.58, 0.59; half-diagonal 36 to 206 mm. Correlations 0.69 (content) and 0.52 (action). | Depth / half-diagonal is 2.42 (IQR 2.10-2.67, n 214) for the completed frame without the hover part, but 2.22 (IQR 1.94-2.54) with the hover part included. The report's derived rule 5 pairs "2.4" with "hover part included"; that is inconsistent. Applied to the hover-inclusive box, 2.4 lands within 20 % of the real depth on 133 of 213 views, so it is a loose fit either way. |
| CAM-11 | confirmed | Isolated median 175 mm, in-context 300 (258-323); ratios 1.49 / 1.85 / 1.46. | Stronger than stated: of 12 many-part views under 150 mm, 9 are isolated ribbon or jumper close-ups (each wire counts as a part), 1 is the PMG Part 1 title page, 2 are the LAC knob check. |
| CAM-12 | qualified | Action inside frame 419/422; 75 of 76 cropped Step N frames keep it inside; centre (0.49, 0.45), height 0.43 (0.33-0.56). | 2 of the 3 exceptions are reprojection artefacts (LSM Part 2 [001], Part 1+2 [017]; the render shows the wire fully in frame). Real exception: LSM Full [071] Step 32 touches the top edge. Hover part centre y 0.30; above mid-frame on 119/149; above its destination on 99/149, below on 40. |
| CAM-13 | qualified | Clean Nc (398): centre (0.49, 0.47), central box 315 (79 %), height 0.61 (0.51-0.74), width 0.41 (0.34-0.56), margins 0.18 / 0.21 / 0.28 / 0.30. Step N: 0.67 / 0.46 / top 0.12. | "Margins on all sides" fails on 65/398 clean frames and 176/1037 of all frames (LAC 94, PMG 69, LSM 13). PMG centred on only 73/117 (62 %). Content beats action for centring on 139/236 (59 %), a weak majority. |
| CAM-14 | qualified | 176 direction-merged legs of 10 mm or more: angle median 59.2 (IQR 56.1-63.5), minimum 41.2, 7 under 45, none under 30. On-screen travel 0.25-0.27 frame heights. | "0 upward" is wrong: LSM Full Step 29 ([064] to [065]), Part 3+4 Step 9 and Part 4 Step 3 lift the matrix support 19-22 mm up to the hovering matrix. For vertical moves the angle is just 90 minus elevation, so this is partly a restatement of CAM-5. |
| CAM-15 | confirmed | 117 Transitions: 68 tweens, 27 swaps, 6 fade-ins, 4 nothing, 12 camera-only. Camera-only: 12/12 at 800 ms, play, overlay hidden, hidden from picker; 10 between Nc and N; 8 with an up-axis change. 58 Step N rotate over 90 deg. | 7 of the 12 also switch off one leftover annotation on entry. |
| CAM-16 | qualified | 148 steps with a re-declared up-axis in 12 guides; 110/110 below-horizon steps have one; upright model minimum world elevation 0.0; 39 changes (28 / 8 / 2 / 1), turn 43-167, median 102; 132/148 in 22-47 deg. | "Or a side" is not general: 50 sideways-insert legs are done on an upright model. 10 of the 22 runs are a single numbered step or one card. |
| CAM-17 | confirmed | 15 steps outside 10-60 deg, same list. Ghosting confirmed in raw: opacity 0.5 on base and one wall at LSM Full [075], Part 3+4 [030], Part 4 [016]. | None. |
| CAM-18 | qualified | 31 cards: 29 on, 30 off, 27 with 3 or fewer parts, height 0.63 (0.60-0.70), centred 30, distance median 175, zoom-out median x1.36, 22 pull back a level or more. | "Face-on for flat boards" is kit-specific: PMG module cards (90, 17, 3/12, 12 deg) and the LSM Capacitor (0/5 deg, not a board) are face-on beside a photo or diagram; LAC flat modules are 3/4 (Real Time Clock 22, LCD Screen 35). |
| CAM-19 | confirmed | Model centre x 0.71 (0.67-0.75 on 18), y 0.48, height 0.67 (0.60-0.74 on 17), left edge 0.49 (0.34-0.60), elevation 35 (21-47). Composition 0.91 wide, margins 0.02 left, 0.06 top. | Title-page content is the guide's end state: identical leaf set to the final view in 9 of 16 construction guides, at most 46 leaves different in the rest. Model left edge is left of 0.45 in 5 guides (LSM Part 2, Part 1+2, LAC Part 2, Part 3, PMG Deconstruction). |
| CAM-20 | qualified | Moves 17/19, 0 annotations 19/19, centre (0.47, 0.47), height 0.67, elevation 39 vs 35. Distance: same 9, x1.17 closer 3, x1.59 closer 4, x1.85-1.98 closer 2, farther 1. Azimuth within 27 deg on 15 (median 14). Settle 7, swing 10. | "A few degrees higher" hides a split: 11 guides within 3 deg of the title page, 7 are 10-20 deg higher, 1 is 10 deg lower. |
| CAM-21 | confirmed | 65 fades, 61 with a camera move; 55 on scene swaps (LSM 31/61, LAC 24/48, PMG 0/31); 10 not on swaps. | Fades by class: Step N 44, card 17, Step Nc 4. Set on entering a card 17/31, on the step after a card 5/31. That it replaces the fly is an interpretation; the payload only shows the property value. |

## Numeric defaults that need correcting

- Hover part top edge "never under 0.03": false. Median 0.13 is right, but 16 of 149 rigid inserts are under 0.03 (10th percentile 0.026, minimum -0.004).
- Fit distance: 2.4 x half-diagonal applies to the seated content; 2.2 x with the hover part included.
- Wiring elevation: PMG 21 / 25 / 30 is right; LSM spans 15-38 (median 27); LAC is 48-57 on 4 of 7 construction wiring views, the others 24, 29, 35.
- Azimuth default: diagonal within 15 deg for LSM and LAC only; PMG has no preferred azimuth class.
- Isolated close-up: median 175 mm, lower quartile about 130 mm rather than 110.
- Final view distance: same as the title page or one to three ladder levels closer (not "one level").
- Elevation change per move: median 9 deg, a quarter exceed 15 deg.
- All other defaults reproduced within rounding (see table above and structured output).

## Patterns the report missed

1. Diagonal azimuth is an LSM / LAC habit, absent in PMG (see CAM-6).
2. Cameras are per-step assets copied between guide variants. Part-guide views with an exact copy in the kit's full build:
   LAC 38 of 44 (Step N 30 of 30), PMG 37 of 41 (Step N 31 of 31), LSM Part 3 / 3+4 / 4 22 of 37, LSM Part 1 / 2 / 1+2 0 of 45.
   Deconstruction views that are exact copies of a build view: PMG 16 of 23, LAC 8 of 18, LSM 6 of 21.
3. Where a step was re-shot (LSM Part 1+2 vs Full Build, 21 steps) the two cameras differ by a median 6 deg, the Full Build
   sits one ladder level farther out on 14 steps, and the move / hold decision agrees on 19 of 21. The camera choice is repeatable.
4. On rigid inserts the frame is centred on the destination, not the hover part: seated-part centre (0.49, 0.47), 0.11 frame
   heights from the frame centre; hover part at (0.49, 0.30), 0.30 away.
5. An out-of-frame action is the one hard trigger for a new camera: 83 of 83 against the camera actually in effect.
6. Scene swaps and camera moves go together: 127 of 140 swap steps move the camera.

## Data caveats found on the way

- Digest `MOVE` directions are in the part's local frame. LSM Full [065] is listed as 22 mm down but the render ([064]-[066])
  shows the support rising to the matrix.
- Digest `visible_parts` counts each jumper as a part and uses chain visibility; it reports 0 parts on the PMG "4-Digit
  Display" card although the display is on screen.
- README_DATA.md calls Transitions camera steps; 105 of 117 do not move the camera (the report already says this).
