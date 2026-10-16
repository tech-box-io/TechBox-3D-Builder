# Guide report: 19075-piano-memory-game-part-3  (kit PMG, role: part)

Sources: `digest/19075-piano-memory-game-part-3.md` + `.json` (all 59 viewer steps), all 8 contact sheets, 40+ individual
frames and crops from `thumbs/` and `thumbs_raw/`, targeted queries of `cadasio_raw/` (annotation property blocks, hidden
step list), and a signature comparison against the PMG full-build digest. Working crops are in `reports/_work_pmg_p3/`.

## 1. Summary

Part 3 is the **housing guide**: the student slots together the 14 laser-cut wooden panels (engraved H1...H14, plus four
identical piano keys H9) and, at the points where access demands it, drops in the electronics harness that was wired in
Parts 1 and 2 (4 push-button modules, Nano I/O module with Nano and USB lead, 4-digit TM1637 display, 32x8 LED matrix).
No wire is connected and no screw is used anywhere in this guide; every joint is tab-into-slot, hook-and-swing or
drop-and-slide. The guide is **59 viewer steps**: Start, 26 numbered steps each split into `Step N` (what is about to
happen) and `Step Nc` (the result), 5 auto-advancing `Transition` waypoints, and `Completed View`. It is completely
wordless: 0 text labels are shown, every step description and popup is empty; instruction is carried by motion, thin red
lead lines (43 of them), one red arrow, 7 black eye icons and 3 inset pictures. It is a renumbered slice of the PMG full
build (full-build Steps 26-51).

## 2. Step table (every viewer step)

Camera column: `moves A deg` = orbit on entering the step, then distance / elevation / azimuth. `same` = camera untouched.
Lead-line lengths in mm. "Swap" = the old model instance fades out and a duplicate at the new pose fades in (no tween).

| idx | name | kind | what is added or done | annotations | camera |
|---|---|---|---|---|---|
| 000 | Start | title | Finished PMG shown at right (88 parts) | 2 screen-fixed images: TechBox logo (w 39.5 %, at 2 %,8 %) and title block "Piano Memory Game (PMG) / Part 3 / (c) 2026 TechBox..." (w 46.5 %, at 2 %,65 %) | 320 mm, el 21, az -43 |
| 001 | Step 1 | hover | Everything hidden except H1 (front strip, already in place, never introduced) and H2 (right side), H2 pulled back 40 mm | 1 lead line 36.6: H2 front tab tip -> end slot of H1 | moves 17, x1.17 -> 275, 36, -50 |
| 002 | Step 1c | seated | H2 tweens 40 mm into H1 | none | same |
| 003 | Step 2 | hover | H3 (left side) fades in 43.2 mm out | 1 lead line 39.8: H3 front tab -> other end slot of H1 | moves 65 -> 275, 40, -136 |
| 004 | Step 2c | seated | H3 tweens 43 mm | none | same |
| 005 | Step 3 | hover | H4 (back panel) fades in 65 mm behind the frame | 4 lead lines 61.5-61.6: 2 rear tabs of H2 + 2 of H3 -> 4 slots of H4 | moves 103, x0.74 -> 374, 36, 34 |
| 006 | Step 3c | seated | H4 tweens 65 mm | none | same |
| 007 | Step 4 | hover, stage 1 | Scene up-axis flips to -y (frame now shown underside-up). H5 (deck with 4 key-shaped cut-outs) fades in tilted, 140 mm away | 2 lead lines 118: two edge tabs of H5 -> two stepped holes in H2 | moves 100 -> 374, -34, -42 |
| 008 | Step 4c | part-seated | H5 tweens 117 mm; tabs hooked into H2, opposite edge still 56 mm up | none | same |
| 009 | Step 5 | hover, stage 2 | No new part | 2 lead lines 56.8: raised-edge tabs of H5 -> notches in top edge of H3 | moves 68, x1.36 -> 275, -45, -134 |
| 010 | Step 5c | seated | H5 swings down (56 mm + rotation) | none | same |
| 011 | Step 6 | hover, stage 1 | H6 (comb-shaped retainer deck) fades in tilted, 136 mm away | 2 lead lines 122.5: edge tabs of H6 -> tab holes on the H2 side (data anchor: H5) | moves 71, x0.86 -> 320, -28, -44 |
| 012 | Step 6c | part-seated | H6 tweens 122 mm; hooked, other edge 43 mm up | none | same |
| 013 | Step 7 | hover, stage 2 | No new part | 2 lead lines 44: raised tabs of H6 -> notches in H3 | moves 67, x1.36 -> 236, -23, -119 |
| 014 | Step 7c | seated | H6 swings down (43 mm + rotation) | none | same |
| 015 | Step 8 | identify | The whole Part 1-2 harness fades in beside the frame (71 components: I/O module + Nano, 4 button modules, LED matrix, display, USB lead, 22 wire bodies, 42 wire caps) | 2 eye icons: one -> blue push-button module, one -> first cut-out ledge in H6 | moves 55, x0.86 -> 275, -40, 179 |
| 016 | Step 8c | seated (swap) | Blue button module + its 3 wires + 3 caps swap from loose to installed in cut-out 1 | 1 inset picture (close-up render, red box round the board/header tucked under the ledge), cyan leader to the module; eyes removed | same |
| 017 | Step 9 | identify | Nothing moves | 1 eye icon -> yellow button module; inset removed | same as Step 8 (no move) |
| 018 | Step 9c | seated (swap) | Remaining 3 button modules (yellow, white, black) + 9 wires + 9 caps swap into cut-outs 2-4 | none | same |
| 019 | Step 10 | hover, stage 1 | H7 (solid bottom cover) fades in tilted, 139 mm away | 2 lead lines 139: edge tabs of H7 -> tab holes on the H2 side (data anchor: H6) | moves 102, x0.86 -> 320, -24, -49 |
| 020 | Step 10c | part-seated | H7 tweens 139 mm; hooked, other edge raised | none | same |
| 021 | Step 11 | hover, stage 2 | No new part | 2 lead lines 28.6: raised tabs of H7 -> notches in H3 | moves 85 -> 320, -35, -151 |
| 022 | Step 11c | seated | H7 swings shut (0.6 mm + rotation) | none | same |
| 023 | Step 12 | hover | Up-axis back to +y (frame upright again). H8 (key divider wall) fades in 94.5 mm above | 2 lead lines 94.6: two bottom tabs of H8 -> two slots in the deck | moves 122 -> 320, 30, -41 |
| 024 | Step 12c | seated | H8 drops 94.5 mm | none | same |
| 025 | Step 13 | hover | First piano key H9 fades in 108 mm in front, in line with its slot | 1 lead line 104.3: key tongue tip -> through H8 -> slot in H4 | moves 17, x1.17 -> 275, 36, -22 |
| 026 | Step 13c | seated | Key slides 108 mm home | 1 inset picture (rear of H4, key tongue poking through, red box), cyan leader to the tongue | same |
| 027 | Step 14 | identify | Nothing moves | 1 inset picture: flat outline of key "H9" with "3x"; cyan leader to the next slot in H8 | same as Step 13 (no move) |
| 028 | Step 14c | seated | 3 remaining keys fade in already seated | none | same |
| 029 | Step 15 | hover, stage 1 | H10 (top deck) fades in 127 mm in front/above | 2 lead lines 116: two rear tabs of H10 -> two slots of H4 | moves 51 -> 275, 26, 37 |
| 030 | Step 15c | part-seated | H10 tweens 126 mm; rear tabs in H4, front still 9 mm up | none | same |
| 031 | Step 16 | hover, stage 2 | No new part | 2 lead lines 8.7/8.8: underside of H10 -> top posts of H3 and H2 | moves 62 -> 275, 13, -29 |
| 032 | Step 16c | seated | H10 drops 9 mm + rotation | none | same |
| 033 | Step 17 | hover | H11 (display bracket) fades in 54 mm above H10 | 1 lead line 50.1: hook tab of H11 -> slot in H10 | moves 31 -> 275, 40, -12 |
| 034 | Transition | auto waypoint | H11 drops 53 mm into the slot | lead line removed, nothing added | same |
| 035 | Step 17c | seated | H11 slides 6.7 mm sideways to lock its hook | none | same |
| 036 | Step 18 | hover | H12 (second bracket) fades in 45 mm above H10 | 1 lead line 41.0: hook tab of H12 -> slot in H10 | moves 99, x1.17 -> 236, 37, -167 |
| 037 | Transition | auto waypoint | H12 drops 44.5 mm | lead line removed | same |
| 038 | Step 18c | seated | H12 slides 7.6 mm to lock | none | same |
| 039 | Step 19 | hover | H13 (U-shaped rear brace) fades in 80 mm up | 4 lead lines: 82 x2 (slit roots of H13 <-> slits of H11 and H12), 68 x2 (leg tips of H13 -> slots in H4) | moves 48, x0.86 -> 275, 40, 130 |
| 040 | Step 19c | seated | H13 slides 80 mm down | none | same |
| 041 | Step 20 | identify | Nothing moves | 1 eye icon -> Nano I/O module (lying loose) | moves 13, x0.74 -> 374, 28, 135 |
| 042 | Step 20c | re-pose (swap) | I/O module + Nano + USB lead + all wires swap to an upright pose about 80 mm above the back panel | none | same |
| 043 | Step 21 | hover | Nothing moves | 1 red 3D arrow 79.8 mm, pointing down from the module's bottom edge to H4 | moves 76, x0.86 -> 436, 29, 45 |
| 044 | Step 21c | seated (swap) | Module + harness swap to the pose seated on H4 | none | same |
| 045 | Step 22 | identify | Nothing moves | 1 eye icon -> 4-digit display (loose) | moves 37, x1.36 -> 320, 41, 89 |
| 046 | Step 22c | re-pose (swap) | Display + 4 wires + 4 caps swap to a hover pose above the H11/H12 brackets | none | same |
| 047 | Step 23 | hover, stage 1 | Nothing moves | 2 lead lines 12: bottom corners of display PCB -> lower notches of H11 and H12 | moves 83, x1.36 -> 236, 34, -25 |
| 048 | Transition | auto waypoint (swap) | Display swaps to stage-1 pose (bottom edge in the notches) | old 2 lines removed, 2 new lead lines 9.5: top of PCB -> upper notches | same |
| 049 | Step 23c | seated (swap) | Display swaps to seated pose | none | same |
| 050 | Step 24 | identify | Nothing moves | 1 eye icon -> LED matrix (loose) | moves 35, x0.74 -> 320, 38, -68 |
| 051 | Step 24c | re-pose (swap) | Matrix + 5-wire ribbon swap to a hover pose in front of the brackets | none | same |
| 052 | Step 25 | hover, stage 1 | Nothing moves | 2 lead lines 21.2/20.4: front notches of H12 and H11 <-> bottom edge of matrix PCB | moves 96, x1.17 -> 275, 14, -177 (side-on) |
| 053 | Transition | auto waypoint (swap) | Matrix swaps to stage-1 pose (bottom edge in notch, leaning out) | old 2 removed, 2 new lead lines 10.8: upper hooks of H12/H11 <-> PCB | same |
| 054 | Step 25c | seated (swap) | Matrix swaps to seated pose | none | same |
| 055 | Step 26 | hover, stage 1 | H14 (face plate with display window) fades in about 58 mm up-slope | 1 eye icon -> top edge of the matrix PCB where H14's feet tuck in; 2 lead lines 58.3/58.7: two feet of H14 -> that spot | moves 22, x0.74 -> 374, 36, -172 |
| 056 | Transition | auto waypoint | H14 slides 58 mm down | eye + 2 lines removed; 2 new lead lines 8.1/8.5: top slots of H14 <-> top hooks of H12/H11 | same |
| 057 | Step 26c | seated | H14 tips back onto the hooks (2 mm + rotation) | 2 lead lines still switched on (collapsed, not visible in the render) | same |
| 058 | Completed View | final | H14 settles a further 1.7 mm + rotation; finished product | none | moves 85, x1.17 -> 320, 35, -61 |

Totals: 54 pause steps, 5 play steps; every step 800 ms; 43 lead-line instances, 1 arrow, 7 eye icons, 3 inset pictures,
2 title images, 0 text labels.

## 3. Conventions found

### Structure
- **S1. Skeleton** (always): `Start` -> 26 x (`Step N`, `Step Nc`) -> `Completed View`. No named section cards in this
  guide (Parts 1 and 2 of the same kit do have them). 59 = 1 + 26 + 26 + 5 + 1.
- **S2. `Step N` / `Step Nc` pairing** (always, 26/26): `Step N` shows what is about to happen (hover part and/or
  annotation); `Step Nc` shows the result. Both wait for the student.
- **S3. `Transition` = motion waypoint, not a camera move** (always here, 5/5): [034] [037] [048] [053] [056] sit between
  `Step N` and `Step Nc`, auto-advance, and the camera is unchanged in all five. They chain two motion segments into one
  press of Next. This differs from the README's "camera Transition" description.
- **S4. Wordless** (always): description and popup are empty on 59/59 steps; none of the project's 45 text labels is
  ever switched on. The only text on screen is the engraved H-numbers on the wood, the title block, and "3x"/"H9" inside
  one inset picture [027].
- **S5. Title page** (same layout as Parts 1 and 2): logo top-left, title block lower-left, finished model on the right.
- **S6. Uniform timing** (always): 800 ms per step, parts fade in/out, moves tween, camera tweens (speed 2, no orbit
  animation), perspective FOV 45, view cube on.
- **S7. Hidden scratch steps** bracket the visible sequence: 2 before Start ("Step 143", "Step 144") and 10 after
  Completed View ("colors", "Step 7", "Step 6", "Step 97", "Step 5" ... "Start").

### Granularity
- **G1. One new wooden panel per numbered step** (13 of 13 panel-introducing steps: 1, 2, 3, 4, 6, 10, 12, 13, 15, 17,
  18, 19, 26). Never two different panels together.
- **G2. Repeated identical parts: first one alone, the rest together.** Buttons: Step 8 installs 1, Step 9 the other 3.
  Keys: Step 13 inserts 1 (with lead line and check picture), Step 14 the other 3 (with a "3x" picture). Only place
  where more than one part lands in a step.
- **G3. A two-stage joint gets either a second numbered step or a Transition.** Second numbered step, with a camera move
  of 62-85 degrees to the other side, for H5 (4/5), H6 (6/7), H7 (10/11), H10 (15/16). Transition, same viewpoint, for
  H11 (17), H12 (18), display (23), matrix (25), H14 (26). So 4 of the 26 numbered steps add no part at all.
- **G4. Pre-wired modules take two numbered steps each**: identify-and-bring-over (eye icon -> re-posed hover), then
  seat. Nano 20/21, display 22/23, matrix 24/25. Exception: button modules go straight from eye icon to installed (8, 9).

### Ordering
- **O1. Panels are engraved H1...H14 and are installed in exactly that numeric order.** The part number is the build
  order.
- **O2. H1 is the datum**: it is on screen from Step 1 and is never introduced with a hover.
- **O3. Electronics go in at the last moment access allows**: buttons after H6 and before the bottom cover H7 (Steps
  8-9); Nano module, display and matrix after the brace H13 (Steps 20-25); face plate H14 last.
- **O4. The harness is hidden for Steps 1-7 and fades in as a whole at Step 8** [015]; from then on it is always on
  screen, dangling beside the housing.
- **O5. Underside work is grouped**: Steps 4-11 ([007]-[022], 16 viewer steps) are all done with the frame shown
  upside-down, then it is turned upright once at Step 12 and stays upright.

### Motion
- **M1. Hover then seat** (always for panels): the new panel fades in displaced straight back along its insertion axis,
  then tweens home on the `c` step. First-appearance offsets: 40, 43, 65, 140, 136, 139, 95, 108, 127, 54, 45, 80,
  ~58 mm (range 40-140, median 80). Not a fixed distance: big deck panels get ~130-140, small brackets ~45-55.
- **M2. Hook-and-swing** (5 parts: H5, H6, H7, H10, H14): the panel arrives tilted, first translates until the tabs on
  one edge are in their holes (no rotation), then rotates down onto the opposite support (digest ROTATE flag on [010]
  [014] [022] [032] [057]).
- **M3. Drop-and-slide lock** (H11, H12): drop 53 / 44.5 mm into the slot in the Transition, then a 6.7 / 7.6 mm
  sideways slide in the `c` step.
- **M4. Wired modules never tween; they cross-fade between duplicated snapshot instances**, each with its own re-routed
  wire bodies and caps. 10 swap steps: [016] [018] [042] [044] [046] [048] [049] [051] [053] [054], all APPEAR +
  DISAPPEAR with no MOVE. Snapshot chains: button loose -> installed (2 poses); I/O module -1 -> -3 -> -2 (3 poses);
  display -4 -> -6 -> -7 -> -2 (4 poses); LED matrix -1 -> -8 -> -9 -> -4 (4 poses).
- **M5. Repeat parts skip the hover**: the 3 extra keys [028] and 3 extra buttons [018] simply appear seated.

### Red lead lines
- **L1. One line per tab/slot pair being engaged in that stage** (usual): 43 lines over 22 viewer steps; 1 line on 5
  steps (1, 2, 13, 17, 18: single tab), 2 lines on 15 steps, 4 lines on 2 steps (3 and 19: four mating points).
- **L2. Tip-to-mouth, parallel to travel**: each line starts at the tip of the tab (or hook, or PCB corner) and ends at
  the mouth of the slot or notch it will enter. Length is 0.85-1.03 x the stage travel. In six cases it is exactly
  travel minus about 3.4 mm, i.e. it stops at the near face of the receiving panel and the tab then goes through the
  panel thickness: 36.6/40.0, 39.8/43.2, 61.5/65.0, 104.3/107.7, 50.1/53.1, 41.0/44.5.
- **L3. Second stage gets its own fresh lines** for the second set of features: Steps 5, 7, 11, 16 and Transitions
  [048] [053] [056]. Exception: the lock slides of H11/H12 ([034]->[035], [037]->[038]) get none.
- **L4. Shown on the hover frame only, removed on the next frame** (21 of 22 cases). Exception: [057].
- **L5. Style** (always): `#ff0000`, solid, thin (Cadasio line scale 5), 2 points, both ends bound to a part
  (`object_ids` + local positions) so they follow the parts.
- **L6. End order is not consistent**: usually moving part first, but fixed part first in [005] [052] [053] and mixed
  within [007] [039] [056]. Treat a lead line as undirected.

### Arrow
- **A1. One red 3D arrow in the whole guide** (Step 21 [043]): straight, `#ff0000`, body width 5, head 20 x 17, head at
  the end, 79.8 mm, from the bottom edge of the Nano I/O module down to back panel H4. Used where a wired module slides
  onto the housing and there is no single tab/slot pair to link.

### Labels
- **T1. No text callouts** (always, 0/59 steps). Parts are identified only by the engraved H-number on the model itself.

### Eye icon
- **E1. "Look at this" marker**: black eye, 8.2 % of viewport width, cyan `#7fdbff` leader ending in a dashed cyan ring
  on the feature. 7 icons on 6 steps. It marks (a) the pre-built module the student should pick up next: blue button
  [015], yellow button [017], Nano I/O module [041], display [045], LED matrix [050]; or (b) the spot to watch: the
  cut-out ledge in H6 [015], the matrix edge where H14's feet tuck in [055].
- **E2. Shown only on `Step N`, gone on the very next frame** (6/6; five times that frame is `Step Nc`, once it is the
  Transition [056]). Placed in white space 12-25 % of the viewport away from the target; no fixed screen position.

### Inset pictures
- **I1. Three image callouts**, each a rounded rectangle with a light cyan border on white, in the upper-left of the
  viewport (at 23 %,4 %; 19 %,7 %; 16 %,11 %; widths 13-18 %), with a cyan leader and dashed ring on the feature.
- **I2. Two are "check your work" close-ups on a `c` step** ([016], [026]): a zoomed render with a red rectangle round
  the detail that must look right. They stay until the next `Step N`.
- **I3. One is a quantity cue on a `Step N`** ([027]): flat outline of the key with "3x".

### Camera
- **C1. The camera moves only on entering a `Step N`, Start or Completed View**: 24 of 26 `Step N`; 0 of 26 `Step Nc`;
  0 of 5 Transitions. Exceptions: Step 9 and Step 14 (the "do the rest" steps) reuse the previous view.
- **C2. Every new step re-orbits to face the joint**: 13-122 degrees per move, median 66; target shift only 8-64 mm
  (143 mm once, leaving the title page for Step 1). The camera circles the kit rather than panning.
- **C3. Distance is one of five zoom stops 1.166x apart**: 236 / 275 / 320 / 374 / 436 mm. Per view: 275 x10, 320 x8,
  374 x4, 236 x3, 436 x1. Closest for small second-stage details (Steps 7, 18, 23); farthest when the whole harness has
  to be in shot (Steps 20, 21).
- **C4. Elevation 13-41 degrees above the horizon when upright.** For underside work the scene up-axis is flipped to -y
  and elevation runs -23 to -45 (Steps 4-11). There is no "turn it over" step, icon or arrow; the cue is the camera
  swing (100 degrees at Step 4, 122 at Step 12) and the upside-down engraved labels.
- **C5. Framing follows the joint, not the whole kit**: hover part + target fill roughly 40-60 % of the frame width; the
  dangling electronics are often cut by the frame edge.

### Look
- **K1.** White `#ffffff` background, toon shading with exactly two flat tones per material, thin black outlines on every
  part, no shadows.
- **K2. No highlight colour for the new part**: an incoming part looks identical to the parts already placed.

### Wiring
- **W1. No wiring is taught in Part 3.** Wires are full-colour passengers of the pre-built harness and are re-routed
  only through the snapshot swaps of M4.

## 4. Part looks (from the renders)

| part | look |
|---|---|
| Wooden panels H1-H14 and keys H9 | Two flat toon tones: lit faces pale cream-yellow `#ffeeb0`, shaded faces tan `#e3bb8b`; thin black outline; black engraved part number on the face |
| Nano I/O expansion module | Royal-blue PCB `#2c61f5` with rows of pale holes, black female header strips, cream-yellow 3-pin header blocks with silver pins, black barrel jack |
| Arduino Nano | Very dark teal/navy board (about `#00303c`) with white chip and pad detail, silver mini-USB socket |
| Push-button modules | Navy board, black switch body, large round cap in blue `#0090fc`, yellow `#fcfc00`, white or black; black right-angle 3-pin header |
| 4-digit display | Blue PCB, black display block with white 7-segment "88:88" |
| LED matrix 32x8 | Blue PCB; four white blocks with near-black faces `#181818` and light-grey dots `#e8e8e8`; "1088AS" printed in black on the white sides |
| Jumper wires | Round tubes in flat saturated colours (red, yellow, bright green, teal-green, plum, purple, salmon, steel blue, brown, navy, white, black) with black rectangular connector housings |
| USB lead | Very dark brown-black `#271c1b` cable and moulded plugs, silver USB-A shell, right-angle mini-USB end |
| Lead lines / arrow | Pure red `#ff0000`; lines hair-thin, arrow a thicker shaft with a cone head |
| Eye icon | Solid black eye with a white ring pupil |
| Callout leaders and frames | Light cyan `#7fdbff` line ending in a dashed ring; inset frame is a rounded rectangle in the same cyan |
| Background | Plain white |

## 5. Anomalies and inconsistencies

1. **Step 26c is not the final pose.** [057] still has 2 lead lines switched on (the only `c` step with lead lines), and
   H14 moves a further 1.7 mm with a rotation on Completed View [058].
2. **H14 has no proper assembled CAD pose.** Its final position is a manual 1682 mm offset applied in Start; the
   component exists twice (H14-1, H14-2). The digest's "still displaced" for H14 is an artefact of this.
3. **Eye icon exists under two names**, "new eye" (27 defined) and "Eye" (3), same image. The "Eye" ones (Steps 22, 24)
   have no leader colour in the data although the render shows the usual cyan.
4. **One off-colour callout**: the Step 8c inset uses `#7fb9ff` for leader/ring; every other callout uses `#7fdbff`.
5. **Inconsistent "do the rest" cue**: keys get an explicit "3x" picture (Step 14); buttons get only one eye icon on the
   yellow button (Step 9) although three are installed.
6. **Lock slide unannotated**: the 6.7 / 7.6 mm sideways slide of H11/H12 has no line or arrow, unlike every other
   second stage.
7. **Lead-line end order varies** (see L6).
8. **Clipped and lopsided frames**: the kit is cut by the frame edge in [019]-[020], [029]-[030], [033]-[038],
   [039]-[040], [047]-[049]; many `c` frames are off-centre because the camera is not re-framed once the hover part
   seats (e.g. [040] sits in the lower half of an otherwise empty frame).
9. **Name spacing**: project name is "Piano Memory Game(PMG) Part 3" (no space) but the title image reads
   "Piano Memory Game (PMG)".
10. **Unused inventory**: 45 text labels and several images belong to the shared project but are never shown here. The
    label texts mix case (cs x2 vs CS x1, clk vs CLK, s8/s9 vs S4...S13).
11. **Hidden scratch steps** with stray names ("Step 143", "Step 144", "colors", "Step 97", duplicate "Step 1-7",
    second "Start").
12. **Data caveats, not guide faults**: digest offset directions are in part-local axes (e.g. [005] reports "-Y (down)"
    for a move the render shows as horizontal), so only magnitudes were used. At [046] the loose display instance is
    not listed as hidden although the render shows a single display. At [051] the matrix ribbon in the hover snapshot is
    one merged multi-colour body instead of 5 wires. Inventory colours are mostly grey because a hidden step recolours
    everything.
13. **CAD names** (not student-facing): "Ensamblaje_Shield_NANO", "Display TM1637-Вырез-Вытянуть2", "Tactal Switch".

## 6. Relation to the other PMG guides

- **Full build** (`19075-piano_memory_game_pmg-full_build`): Part 3 is full-build Steps 26-51 renumbered from 1. I
  compared camera (distance, elevation, azimuth), visible annotation counts, appear/disappear counts, move distances and
  behaviour for Part 3 [001]-[057] against full-build [059]-[115]: 56 of 57 are identical; the only difference is how
  the first step is entered (Part 3 hides the 86 parts of its title model; the full build hides 71 and shows 2). Start
  and Completed View cameras are identical too. The five Transitions line up with full-build Steps 42, 43, 48, 50, 51.
- **Parts 1 and 2**: they wire the harness that Part 3 installs. They use named section cards ("Nano I/O Module",
  "Push Buttons", "4-Digit Display", "Dot Matrix Display", "USB Cable") and text pin labels (GND, VCC, s8, ...); Part 3
  has neither. Title-page layout is the same (image positions and widths match Part 2 exactly).
- **Deconstruction**: its opening steps run Part 3 backwards (H14 off first, then the LED matrix), reuse the same
  camera stations (374/36/-172 and 275/14/-177) and the same snapshot instances (matrix -4 -> -9 -> -8), but use red
  arrows where Part 3 uses lead lines. I only read its first six steps.
