# Dimension report: Camera, framing and transitions

Scope: all 20 published TechBox Cadasio guides, 1037 viewer steps (hidden authoring steps excluded).
Step classes used below: Start 19, Step N ("hover") 425, Step Nc ("comp") 424, Transition 117, section card 31 (+2 overview views in `lac_electronics`), final view 19.

## 0. Method and caveats

- Camera data was re-read from the raw payloads (`default_camera.position`, `orbit_target`, `rotation` quaternion) by replaying every step in order; it agrees with the digest's rounded figures. A step counts as a camera move if the view direction turns more than 0.5 deg, the target shifts more than 0.5 mm, or the distance changes more than 0.5 mm (same test as the digest).
- **Effective elevation** = elevation measured against the scene's declared up-axis for that step, not against world +Y. This matters: 148 steps have an up-axis other than +y. On all 1037 steps the camera has no roll against the declared up-axis (|roll| < 2 deg) and looks straight at its orbit target, so effective elevation is what the student actually sees.
- **Framing** was measured two ways: (a) non-white bounding box of every saved step render (1037 thumbs); (b) a 3D re-projection of the oriented bounding boxes of all visible solids through the step camera (leaf-level visibility, as the per-guide readers recommended). On annotation-free Step Nc frames the two agree within 4 % of the frame on 300 of 398 frames; the remainder are mostly 4-8 % over-estimates. Framing percentages quoted below come from the renders; millimetre sizes and the "action volume" come from the 3D model.
- **Action volume** = the solids whose visibility or pose differs between a Step N and its Step Nc (the hovering/loose part at Step N plus where it ends up), 422 pairs.
- "Distance" is the orbit distance (camera to orbit target). It is within 15 % of the true camera-to-content depth on 143 of 203 checked views (median ratio 0.94) but is misleading on a few isolated close-ups whose orbit target sits far behind the part (e.g. LAC Full [046]-[054] reads 513 mm while the potentiometer and its arrow fill over half the frame height).
- Width percentages depend on the shape of the window the author saved the render in (ten window shapes from 1.82:1 to 2.78:1; 917 of 1037 renders, 88 %, are between 1.95:1 and 2.07:1). Height percentages do not (the 45 deg field of view is vertical).
- Working files: `reports/_work_dim_camera/` (`steps_table.csv` has one row per viewer step; `build.py`, `geom.py`, `geom2.py`, `delta.py`, `imgbbox.py`, `s1.py`-`s19.py` reproduce every number).

## 1. When the camera moves

### Table 1 - camera moves by step class (moves / steps of that class)

| Guide | Steps | Views | Step N | Step Nc | Transition | Card | Final | Longest hold |
|---|---|---|---|---|---|---|---|---|
| LAC deconstruction | 130 | 18 | 16/47 | 0/48 | 0/33 | - | 1/1 | [092]-[128] 37 steps |
| LAC electronics | 2 | 2 | - | - | - | 1/2 | - | - |
| LAC full build | 131 | 38 | 30/57 | 0/57 | 1/10 | 5/5 | 1/1 | [019]-[030] 12 steps |
| LSM deconstruction | 69 | 21 | 19/24 | 0/24 | 0/19 | - | 1/1 | [059]-[067] 9 steps |
| LSM full build | 88 | 38 | 29/38 | 0/38 | 3/6 | 4/4 | 1/1 | [052]-[056] 5 steps |
| LSM part 1 | 19 | 10 | 7/8 | 0/8 | - | 1/1 | 1/1 | [003]-[006] 4 steps |
| LSM part 2 | 31 | 14 | 11/13 | 0/13 | 0/1 | 1/2 | 1/1 | [003]-[009] 7 steps |
| LSM part 3 | 13 | 6 | 3/5 | 0/5 | 1/1 | - | 1/1 | [005]-[009] 5 steps |
| LSM part 3+4 | 43 | 18 | 12/18 | 0/18 | 3/4 | 1/1 | 1/1 | [007]-[011] 5 steps |
| LSM part 4 | 29 | 13 | 9/12 | 0/12 | 1/2 | 1/1 | 1/1 | [018]-[022] 5 steps |
| LSM part 1+2 | 47 | 21 | 18/21 | 0/21 | 0/1 | 1/2 | 1/1 | [019]-[025] 7 steps |
| LAC part 2 | 42 | 11 | 8/18 | 0/18 | 0/3 | 1/1 | 1/1 | [016]-[024] 9 steps |
| LAC part 3 | 21 | 9 | 4/8 | 0/8 | - | 3/3 | 1/1 | [009]-[016] 8 steps |
| LAC part 4 | 42 | 14 | 11/17 | 0/17 | 1/6 | - | 1/1 | [009]-[014] 6 steps |
| LAC part 1 | 32 | 10 | 7/14 | 0/14 | 0/1 | 1/1 | 1/1 | [019]-[030] 12 steps |
| PMG deconstruction | 61 | 23 | 20/23 | 0/22 | 2/14 | - | 0/1 | [051]-[058] 8 steps |
| PMG part 1 | 34 | 6 | 3/14 | 0/13 | 0/3 | 2/2 | 0/1 | [007]-[033] 27 steps |
| PMG part 2 | 27 | 9 | 4/11 | 0/11 | - | 3/3 | 1/1 | [013]-[022] 10 steps |
| PMG part 3 | 59 | 26 | 24/26 | 0/26 | 0/5 | - | 1/1 | [015]-[018] 4 steps |
| PMG full build | 117 | 38 | 31/51 | 0/51 | 0/8 | 5/5 | 1/1 | [007]-[033] 27 steps |
| **All 20** | **1037** | **345** | **266/425** | **0/424** | **12/117** | **30/33** | **17/19** | |

"Views" = number of distinct camera set-ups (325 moves + 20 opening views).

Findings:

- **Step Nc never moves the camera: 0 of 424, in every guide.** Of 422 Step N / Step Nc pairs, 420 use one identical camera from the hover frame to the completed frame, including every pair with part-motion Transitions in between.
  The 2 exceptions are PMG Deconstruction Step 2 and Step 3, where a camera-only auto Transition ([007], [012]) sits between the last pose-swap frame and Step Nc.
- 313 of 325 camera moves happen on entering a Step N (266), a card (30) or the final view (17). The other 12 are camera-only Transitions (section 5).
- A new Step N moves the camera 63 % of the time (266/425). By guide type: parts 121/185 (65 %), full builds 90/146 (62 %), deconstructions 55/94 (59 %).
- The 159 Step N that keep the camera: 141 simply continue from the previous Step Nc, 16 follow a Transition (10 of those a camera-only Transition that already moved it), 1 follows a card that had already moved it (LSM Full Step 13 after the 2D "LED Matrix Diagram" card), 1 is a duplicated frame (LAC Decon [105]).

### Table 2 - what kind of Step N re-aims the camera

Step N classified by the annotations it carries.

| Step N kind | Moved / total | Share |
|---|---|---|
| Rigid insert (red lead lines) | 112/149 | 75 % |
| Arrow step (removal, hand move) | 66/86 | 77 % |
| Eye icon or inset only | 50/79 | 63 % |
| Wiring (labels, no lead line) | 36/109 | 33 % |
| No annotation | 2/2 | - |

Sequence effect (previous numbered step -> this one, moved/total): wire -> wire 12/85 (14 %); eye -> eye 2/23 (9 %); lead -> lead 66/94 (70 %); arrow -> arrow 36/53 (68 %); any change of kind 131/151 (87 %).

Camera-reuse test: this step's action volume was projected through the previous numbered step's camera.

| Action volume under the previous camera | Step N | Camera moved |
|---|---|---|
| Not fully inside the frame (2 % safety margin) | 79 | 77 (97 %) |
| Fully inside the frame | 324 | 169 (52 %) |
| ... of which wiring | 91 | 19 (21 %) |
| ... of which rigid insert | 99 | 64 (65 %) |
| ... of which arrow | 67 | 47 (70 %) |

So "move only when the part would fall out of frame" explains wiring, but not mechanical steps: there the camera is re-aimed to face the joint even when the part would have been visible. The 2 "not inside, not moved" cases are LSM steps whose camera had just been moved by a camera-only Transition (LSM Full Step 24, LSM Part 3+4 Step 4), so in effect an out-of-frame action always gets a new camera.

### Table 3 - how long the camera is held

| Steps sharing one camera | 1 | 2 | 3 | 4 | 5-6 | 7-10 | 11-20 | 21-40 |
|---|---|---|---|---|---|---|---|---|
| Views (345) | 66 | 156 | 54 | 28 | 18 | 16 | 4 | 3 |

Median 2 steps per view (one Step N + its Step Nc), mean 3.0. By guide type: parts 2.6, full builds 2.9, deconstructions 4.2.
Numbered steps per view: 0 in 68 views (cards, Start, final, camera Transitions), 1 in 210, 2 in 38, 3-6 in 25, 9-12 in 4.

### Table 4 - wiring runs (consecutive label-carrying Step N without lead lines)

| Run (guides) | Wires | Viewer steps held | Dist / elev / azim | Later camera moves inside the run |
|---|---|---|---|---|
| PMG Part 1 Steps 3-14 = Full 3-14 | 12 | 27 ([007]-[033]) | 173 / 21 / -62 | 0 |
| PMG Part 2 Steps 2-5 = Full 16-19 | 4 | 8 | 173 / 25 / -72 | 0 |
| PMG Part 2 Steps 6-10 = Full 20-24 | 5 | 10 | 202 / 30 / -81 | 0 |
| LAC Part 1 Steps 9-14 = Full 9-14 | 6 | 12 ([019]-[030]) | 277 / 54 / 128 | 0 |
| LAC Part 2 Steps 2-4 = Full 16-18 | 3 | 6 | 277 / 24 / -158 | 0 |
| LAC Part 2 Steps 6-7 = Full 20-21 | 2 | 4 | 277 / 57 / 55 | 0 |
| LAC Part 2 Steps 16-18 = Full 30-32 | 3 | 6 | 440 / 36 / 120 | 0 |
| LAC Part 3 Steps 1-2 = Full 33-34 | 2 | 4 | 277 / 48 / -38 | 0 |
| LAC Part 3 Steps 4-7 = Full 36-39 | 4 | 8 | 323 / 51 / 127 | 0 |
| LAC Decon Steps 19-22 | 4 | 14 | 323 / 47 / 74 | 0 |
| LSM Part 2 Steps 2-4 = Part 1+2 10-12 (male ends) | 3 | 6 | 163 / 27 / -138 | 0 |
| LSM Full Steps 10-12 (male ends) | 3 | - | 189 / 30 / -139 | 1 (Step 12, a 5.8 deg nudge) |
| LSM Part 2 Steps 5-7 = Part 1+2 13-15 = Full 13-15 (female ends at the matrix) | 3 | - | 190-221 / 15-27 / varies | 2 per run (105-130 deg swings to face each pin) |

30 label runs in total (the table merges copies; 2 of the 30 are the single "2x" resistor-prep step of LAC Part 1 / Full): 26 have no camera move after their first step; 72 of 79 later steps in a run reuse the camera. All 7 exceptions are in LSM.

## 2. The house view

### Table 5 - effective elevation

| Effective elevation | -10 to 10 | 10 to 20 | 20 to 25 | 25 to 30 | 30 to 35 | 35 to 40 | 40 to 45 | 45 to 50 | 50 to 60 | 60 to 91 |
|---|---|---|---|---|---|---|---|---|---|---|
| Viewer steps (1037) | 13 | 34 | 170 | 171 | 167 | 179 | 103 | 113 | 85 | 2 |
| Distinct views (345) | 8 | 17 | 46 | 56 | 57 | 65 | 38 | 32 | 24 | 2 |

- 903 of 1037 steps (87 %) are between 20 and 50 deg; 983 (95 %) between 15 and 55. Median 34 deg; mean of the 345 views 34.0 deg.
- By view type (distinct views): Step N median 34 (10th-90th percentile 22-49), Start median 35 (range 21-47), final median 39 (21-50), cards median 35 but spread 0-90.
- By kit (Step N views): LSM median 32, LAC 36, PMG 34.
- By step kind (all Step N): rigid insert median 33 (IQR 27-36), arrow 35, eye-only 41, wiring 28 with a split: PMG wiring views are 21, 25 and 30 deg and LSM's 15-38 deg (mostly 20-30), while LAC's flat breadboard layout is viewed from 48-57 deg on 4 of its 6 wiring views (the switch-lead and potentiometer-lead views are 24 and 36).
- Low views (10-20 deg, 17 views): side-on looks at a joint or lead (LAC Step 15 switch drop 17 deg; PMG Steps 41/50 at 13-14 deg; LSM matrix-pin steps 15-19 deg) and flat-module cards.
- High views (50-57 deg, 24 views): LAC breadboard wiring and ribbon prep, LSM underside check, some cable cards.

### Table 6 - azimuth (views with up-axis +y, n = 299)

| Azimuth bin (deg) | Views | | Azimuth bin (deg) | Views |
|---|---|---|---|---|
| -180 to -150 | 14 | | 0 to 30 | 0 |
| -150 to -120 | 42 | | 30 to 60 | 63 |
| -120 to -90 | 8 | | 60 to 90 | 19 |
| -90 to -60 | 19 | | 90 to 120 | 8 |
| -60 to -30 | 54 | | 120 to 150 | 56 |
| -30 to 0 | 16 | | 150 to 180 | 0 |

- 215 of 299 views (72 %) are within 15 deg of a diagonal (+-45, +-135); 41 (14 %) are within 15 deg of a cardinal direction. Median offset from the nearest diagonal 9 deg.
- All four quadrants are used (LSM spreads evenly; LAC favours +90..+135; PMG favours -90..0). There is no single fixed azimuth, but there is a strong "look at a corner" habit.
- Hero azimuth per kit (Start pages): LSM about +50 to +57 (7 of 8; Part 1 uses -141), LAC about +141 to +143 (5 of 6; Part 1 uses +49), PMG -43 to -60 (5 of 5).

### Lens and motion

- Perspective camera, vertical field of view 45 deg on 1036 of 1037 steps. Exception: LSM Part 1 "Capacitor" card [011], 50 deg (anomaly; a late insertion).
- Camera animation is identical everywhere: tween, orbit animation off, speed 2 (stored as strings on 1035 steps, as proper types on 2). All 325 camera moves happen inside an 800 ms step.
- A camera move is mostly an orbit: median rotation 61 deg on Step N (IQR 22-83; 134 of 266 over 60 deg, 58 over 90 deg), with a median target shift of 42 mm. Elevation changes little (median 8 deg when the up-axis is unchanged). Only 10 of 325 moves are a pure pan or zoom (rotation under 2 deg): LAC Step 9, LSM Step 37/17/12 after the stems card, LSM P2 Step 11, LSM Decon Step 8, PMG Decon Steps 18, 19, 23.
- Camera poses are not recycled: the 345 views use 341 distinct poses (4 poses are used twice within a guide). There are no "home" stations the camera returns to.

## 3. Distance, zoom and subject size

### Table 7 - orbit distances in use (bold = on a x1.166 ladder anchored at the kit's most-used distance; * = off the ladder)

| Kit | Orbit distances, mm (viewer steps at each) | On ladder |
|---|---|---|
| LSM | 42 (1)*, 60 (1)*, **64** (6), **75** (6), **103** (4), **119** (2), **162** (46), 173 (3)*, **189** (58), **221** (26), **258** (52), **300** (96), 321 (5)*, **350** (16), 374 (17)* | 312/339 |
| LAC | **110** (8), 125 (4)*, **150** (2), **175** (12), **238** (17), **277** (133), **323** (85), **377** (48), **440** (70), **513** (19) | 394/398 |
| PMG | **43** (2), 91 (2)*, 103 (4)*, **128** (4), 133 (2)*, 142 (4)*, **148** (1), **173** (72), **202** (22), **236** (24), **275** (72), **320** (53), **374** (28), **436** (8) | 286/298 |

- 992 of 1035 build/deconstruction steps (96 %) sit on a geometric ladder with ratio 1.166 (measured 1.165 on 99 single-click moves). LAC and PMG share one ladder (110/128, 150/148, 175/173, 202, 237/236, 277/275, 323/320, 377/374, 440/436, 513); LSM's is offset by half a click (163, 189, 221, 258, 300, 350). This looks like the editor's zoom increment rather than a design decision, but the effect is a small fixed set of zoom levels.
- Zoom change on a camera move, in ladder clicks: 0 on 93 of 325 moves, within +-1 click on 186 (57 %), within +-2 on 233 (72 %). Large jumps (3-9 clicks) are entries to and exits from isolated close-ups.

### Table 8 - the zoom follows what is on screen, so the fill stays constant

One row per distance band; one representative annotation-free Step Nc frame per view (259 views).

| Orbit distance | Views | Model height / frame height (median, IQR) | Model width / frame width (median) | Median top-level parts on screen | Median half-diagonal of visible content |
|---|---|---|---|---|---|
| under 130 mm | 17 | 0.61 (0.47-0.62) | 0.43 | 3 | 38 mm |
| 130-215 mm | 47 | 0.54 (0.48-0.65) | 0.40 | 6 | 71 mm |
| 215-290 mm | 83 | 0.63 (0.53-0.78) | 0.50 | 29 | 106 mm |
| 290-340 mm | 64 | 0.62 (0.53-0.76) | 0.41 | 38 | 128 mm |
| 340-400 mm | 31 | 0.58 (0.47-0.66) | 0.39 | 40 | 145 mm |
| over 400 mm | 17 | 0.59 (0.54-0.67) | 0.38 | 74 | 202 mm |

- The subject is five times larger in the bottom row than the top row, yet it fills the same 54-63 % of the frame height. Distance is scaled to the visible content.
- Depth from camera to the centre of the visible content / half-diagonal of its bounding box (203 validated views): median 2.4, IQR 1.9-2.6 (LSM 2.5, LAC 2.3, PMG 2.1). That is 0.91 x the distance at which the content's bounding sphere would exactly fit the vertical field of view (IQR 0.74-1.00).
- In-context steps: log-log correlation of distance with the size of all visible content r = 0.70; with the size of the action volume only r = 0.54. Distance tracks the working assembly more than the part being added.

### Table 9 - close-ups are for isolated parts, not for small parts in context

| View type | Views | Orbit distance median (IQR) |
|---|---|---|
| Isolated (3 or fewer top-level parts on screen) | 60 | 175 mm (110-224) |
| In context (more than 3) | 285 | 300 mm (258-323) |

Ratio in-context / isolated: LSM 1.5, LAC 1.9, PMG 1.4. Isolated views are entered by a card (24), a prep or sub-assembly Step N (34) or a deconstruction final view (2).

In-context Step N that set a new camera, by size of the action volume:

| Action half-diagonal | Step N | Orbit distance median (IQR) | Action height / frame height (median) |
|---|---|---|---|
| under 20 mm | 12 | 189 (163-277) | 0.25 |
| 20-40 mm | 27 | 163 (163-189) | 0.38 |
| 40-70 mm | 70 | 289 (258-350) | 0.40 |
| 70-110 mm | 89 | 275 (258-300) | 0.55 |
| over 110 mm | 40 | 374 (320-436) | 0.53 |

A resistor or a jumper on the breadboard is shown from the same 163-189 mm (LSM) / 173 mm (PMG) / 277 mm (LAC) view as the whole board; the washer, nut and knob in LAC Steps 26-28 are fitted at 440 mm with the whole front panel in view ([057]-[062]). Only 9 of 285 in-context views are closer than 150 mm.

Per kit, in-context Step N distance: wiring LSM 189, LAC 277, PMG 173; rigid inserts LSM 300, LAC 377, PMG 275 (medians).

## 4. Framing, centring and margins (from the saved renders)

### Table 10 - bounding box of everything non-white, as a fraction of the frame

| Frame set | n | Height (median, IQR) | Width (median, IQR) | Centre x / y (median) | Margins top / bottom / left / right (median) | Touch a frame edge |
|---|---|---|---|---|---|---|
| Step Nc without annotations (model only) | 398 | 0.61 (0.52-0.74) | 0.41 (0.34-0.56) | 0.49 / 0.47 | 0.18 / 0.21 / 0.28 / 0.30 | 65 (16 %) |
| Step N (model + annotations) | 425 | 0.67 (0.59-0.78) | 0.46 (0.38-0.60) | 0.49 / 0.46 | 0.12 / 0.20 / 0.26 / 0.28 | 76 (18 %) |
| Section cards | 31 | 0.63 (0.61-0.70) | 0.50 (0.32-0.61) | 0.50 / 0.46 | 0.13 / 0.21 / 0.30 / 0.24 | 0 |
| Start (model + logo + title) | 19 | 0.78 (0.76-0.79) | 0.91 (0.88-0.94) | 0.48 / 0.45 | 0.06 / 0.17 / 0.02 / 0.07 | 1 |
| Final view | 19 | 0.67 (0.64-0.73) | 0.41 (0.39-0.56) | 0.47 / 0.47 | 0.13 / 0.18 / 0.23 / 0.32 | 0 |

- Centring: on clean Step Nc frames the bounding-box centre is within the middle fifth of the frame (0.40-0.60) on both axes in 315 of 398 (79 %); x alone 358 (90 %), y alone 349 (88 %). On uncropped frames the frame centre falls 55 % of the way down the model's box (IQR 46-59 %), i.e. the model sits very slightly high.
- Kit differences (clean Step Nc): height LSM 0.57, LAC 0.71, PMG 0.54; width LSM 0.38, LAC 0.45, PMG 0.47.
- Cropping: 176 of 1037 frames (17 %) have the model touching a frame edge - LAC 94, PMG 69, LSM 13 - almost all in enclosure sections where wired-but-idle panels and modules sprawl (LAC Full [104]-[111], PMG Part 3 [033]-[040]). The author does not zoom out to keep idle parts in.
- The camera is not re-framed when the part seats: Step Nc shows the hover framing minus the part, so its top margin is larger (0.18 vs 0.12).

### Table 11 - where the action sits (3D re-projection, 422 Step N / Step Nc pairs)

| Step N kind | n | Action centre x (median, IQR) | Action centre y (median, IQR) | Action height / frame | Action top edge y (median) | Fully inside frame |
|---|---|---|---|---|---|---|
| All | 422 | 0.49 (0.45-0.54) | 0.45 (0.37-0.53) | 0.43 (0.33-0.56) | 0.23 | 419 |
| Rigid insert (lead lines) | 149 | 0.49 (0.46-0.54) | 0.41 (0.35-0.48) | 0.48 (0.39-0.61) | 0.13 | 148 |
| Wiring (labels) | 108 | 0.47 (0.44-0.50) | 0.50 (0.43-0.56) | 0.40 (0.35-0.55) | 0.28 | 108 |
| Arrow | 85 | 0.50 (0.48-0.55) | 0.46 (0.38-0.54) | 0.35 (0.23-0.45) | 0.30 | 85 |
| Eye / inset only | 78 | 0.50 (0.48-0.54) | 0.47 (0.39-0.53) | 0.44 (0.33-0.60) | 0.23 | 76 |

- The action volume (loose or hovering part plus its destination) is fully inside the frame on 419 of 422 steps, and on 75 of the 76 Step N frames where something else is cropped.
- On new-camera in-context steps the whole visible content is nearer the frame centre than the action in 141 of 238 cases (median offsets 0.12 vs 0.17 frame heights); the action sits about 7 % of the frame height above the content centre. The view is composed on "assembly plus hovering part", not on the hovering part alone.
- On rigid inserts the hovering part is at the top of the frame: top edge at 13 % down (10th percentile 3 %). LSM posts and stems touch or nearly touch the top edge (LSM Full [073], LSM P4 [012], [024]).

### Travel direction relative to the camera (126 rigid translations of 10 mm or more)

- Angle between the part's travel axis and the view axis: median 59 deg, IQR 56-63, minimum 41; 119 of 126 are 45 deg or more, none under 30 deg. No part is ever animated towards or away from the viewer.
- On screen the travel covers a median 0.27 of the frame height (IQR 0.22-0.36).
- Build guides: 63 of 120 travels are straight down relative to the scene up-axis, 48 horizontal, 9 oblique, 0 upward. On screen: 65 run downwards, 32 sideways, 23 diagonally.
- Horizontal inserts (48): the camera stands at about 45-55 deg or 125-135 deg from the travel axis in plan (34 of 48 between 45 and 135 deg); it is on the side the part comes from in 31 of 48. Never looking straight along the travel.

## 5. Transition steps (117)

| What the Transition does | Count | Camera moves? | Where it sits |
|---|---|---|---|
| Part tween (first leg, removal, slide) | 68 | no | 67 between Step N and Step Nc; 1 in a mis-named LAC Decon pair |
| Pose swap (cross-fade of a wired sub-assembly or wire) | 27 | no | between Step N and Step Nc |
| Fade-in of the next identical module | 6 | no | between Step Nc and the next Step N (PMG Part 1 / Full [013] [020] [027]) |
| Nothing changes except annotations switching off | 4 | no | between Step N and Step Nc (LAC Decon [033], LSM Decon [011], LAC Full [116] = Part 4 [027]) |
| **Camera only** | **12** | **yes** | 10 between Step Nc and the next Step N; 2 inside a pair (PMG Decon [007], [012]) |

- 105 of 117 Transitions leave the camera untouched. The README's description of Transition as a camera step fits only 12.
- The 12 camera-only Transitions move nothing else, show no annotation (98 Transitions switch annotations off on entry), last 800 ms, auto-advance, hide the navigation overlay and are hidden from the step picker.
  - 8 are LSM re-orientations that also change the scene up-axis: LSM Full [052] (130 deg), [059] (53), [077] (110); Part 3 [005] (143); Part 3+4 [007] (143), [014] (53), [032] (110); Part 4 [018] (110).
  - 2 are a small settle in LAC Full [108] = Part 4 [019]: 13 deg, one zoom click in, after the F4 top panel is re-posed.
  - 2 are PMG Decon [007] (96 deg) and [012] (83 deg): swing round to show the dismounted module before Step 2c / 3c.
- A camera Transition is not required for a big move: 58 Step N rotate more than 90 deg directly, and 28 of 39 up-axis changes happen on a plain Step N (all LAC and PMG turn-overs, LSM Step 23 and Step 34).
- General Transition facts (for context): 115 play, 2 pause (LAC Decon [033], [118], anomalies); 112 at 800 ms, 5 at 1600 ms (threaded nut moves); overlay hidden on 110; hidden from the step picker on 108.

## 6. Top-down, underside and re-oriented views

### Table 12 - runs with a re-declared up-axis (148 of 1037 steps, 12 of 20 guides)

| Guide | Steps | Up-axis | Entered on | Camera turn at entry | Effective elev (world elev) | What the student sees |
|---|---|---|---|---|---|---|
| LSM Full / P3 / P3+4 | [050]-[051] / [003]-[004] / [005]-[006] | -z | Step N | 43 deg | -5 (85) | true plan view of the open box for the "carry the matrix across" arrow |
| LSM Full / P3 / P3+4 | [052]-[058] / [005]-[011] / [007]-[013] | +x | camera Transition | 130-143 deg | 22-36 (-48 to 41) | box stood on rear wall D4 so D3 and D5 go on from above |
| LSM Full / P3+4 / P4 | [075]-[076] / [030]-[031] / [016]-[017] | -y | Step N | 117 deg | 57 (-57) | box upside down, base and one wall ghosted to 50 %, to push posts through |
| LAC Full / P2 | [046]-[064] / [016]-[034] | -x | Step N | 119 deg | 33-38, then 8 for the knob check (-82 to -28) | front panel F1 stood upright for the potentiometer block |
| LAC Full / P3 | [076]-[077] / [006]-[007] | -y | Step N | 121 deg | 47 (-47) | ribbon prep, isolated |
| LAC Full / P3 | [078] / [008] | -x | card | 65 deg | 35 (-39) | LCD Screen card |
| LAC Full / P4 / Decon | [125]-[127] / [036]-[038] / [004]-[007] | -x | Step N | 66-102 deg | 29 (42) | box lying on its front so rear panel F2 goes on like a lid |
| LAC Decon | [031]-[048] | -x | Step N | 81 deg | 34-41 (-24 to 38) | front panel + potentiometer block |
| PMG Part 3 / Full | [007]-[022] / [065]-[080] | -y | Step N | 100 deg | 23-45 (-45 to -23) | case upside down for all underside panels and the buttons (16 steps, 7 views) |
| PMG Decon | [032]-[042] | -y | Step N | 55 deg | 24-40 (-40 to -24) | same block, undone |

- **Every one of the 110 steps where the camera is below the world horizon has a re-declared up-axis.** The student never sees a worm's-eye view; they see a normal view from above of a model that has been turned over (engraved IDs render upside down, PMG Full [065]-[071]).
- Inside these runs the effective elevation stays in the normal band (22-47 deg) except the LSM plan view (straight down), the LSM underside check (57 deg) and the LAC knob check (8 deg).
- 39 up-axis changes in total: 28 on a Step N, 8 on a camera Transition (all LSM), 2 on a card, 1 on a final view. Camera turn at the change: 43-167 deg, median 102.
- No dedicated "turn it over" arrow, icon or text was found on these steps (the per-guide readers report the same); the camera move is the only cue.

### Views outside the 10-60 deg band (15 steps)

| View | Steps | Elev | Purpose |
|---|---|---|---|
| Plan view, straight down | PMG "Nano I/O Module" card (Part 1 [001], Full [001]) | 90 | match the product photo beside it |
| Plan view, straight down | LSM Step 23 / P3 Step 2 / P3+4 Step 3 (+ their Nc) | world 85 | free-hand move drawn as an arrow in plan |
| Face-on / side-on | LSM "Capacitor" card (0 and 5), PMG "4-Digit Display" card (3) | 0-5 | flat face matched to the photo or diagram |
| Face-on | LAC Step 29/29c = Part 2 Step 15/15c | 8 | knob pointer position; panel deliberately cropped left and bottom |

Other flat-module cards are nearly face-on too: PMG Push Buttons 17, Dot Matrix Display 12, 4-Digit Display 12 (Full).

Ghosting is used only on the LSM underside check (3 copies of one step pair).

## 7. Section cards (31, excluding the 2 overview views)

| Guide | Step | Card | Dist mm | Elev | Parts shown | Height fill | Zoom-out to next step | Rot to next | Annotations |
|---|---|---|---|---|---|---|---|---|---|
| LAC full build | [014] | Real Time Clock | 175 | 22 | 3 | 0.62 | x1.59 | 7.3 | eye |
| LAC full build | [031] | Rocker Switch | 175 | 44 | 7 | 0.62 | x1.59 | 27.6 | none |
| LAC full build | [071] | Alarm Buzzer | 238 | 56 | 5 | 0.63 | x1.17 | 9.5 | eye |
| LAC full build | [078] | LCD Screen | 150 | 35 | 1 | 0.75 | x2.16 | 167.3 | eye + photo |
| LAC full build | [087] | USB Cable | 277 | 47 | 1 | 0.70 | x1.00 | 21.5 | none |
| LSM full build | [012] | Capacitor | 42 | 0 | 1 | 0.60 | x4.49 | 49.0 | diagram |
| LSM full build | [027] | LED Matrix Diagram | 221 | 22 | 0 | 0.81 | x1.00 | 0 | 2D picture only |
| LSM full build | [043] | Mini USB Cable | 221 | 51 | 1 | 0.74 | x1.36 | 43.0 | eye |
| LSM full build | [082] | LED Stems | 173 | 31 | 1 | 0.61 | x2.16 | 0.0 | "64x" label |
| LSM part 1 | [011] | Capacitor | 60 | 5 | 2 | 0.63 | x2.71 | 128.4 | diagram |
| LSM part 2 | [009] | LED Matrix Diagram | 163 | 27 | 1 | 0.76 | x1.17 | 80.8 | 2D picture only |
| LSM part 2 | [027] | Mini USB Cable | 190 | 46 | 2 | 0.67 | x1.36 | 73.4 | eye |
| PMG part 1 | [001] | Nano I/O Module | 133 | 90 | 1 | 0.68 | x1.07 | 56.4 | photo |
| PMG part 1 | [006] | Push Buttons | 43 | 17 | 1 | 0.73 | x4.00 | 21.8 | photo |
| PMG part 2 | [001] | 4-Digit Display | 91 | 3 | 1 | 0.35 | x1.14 | 56.3 | photo |
| PMG part 2 | [012] | Dot Matrix Display | 236 | 12 | 1 | 0.56 | x0.86 | 22.2 | photo |
| PMG part 2 | [023] | USB Cable | 202 | 38 | 3 | 0.37 | x1.36 | 39.6 | none |
| PMG full build | [034] | 4-Digit Display | 91 | 12 | 1 | 0.34 | x1.14 | 41.6 | photo |

(18 distinct cards; the other 13 are identical copies in sibling guides.)

- Camera moves onto the card on 29 of 31 and off it on the next step on 30 of 31. The exceptions are the 2D "LED Matrix Diagram" card (LSM Part 2 [009], Part 1+2 [025] keep the previous camera; LSM Full [027] pre-positions the camera for Step 13).
- Isolation: 27 of 31 show 3 or fewer top-level components (the rest are a pre-wired component with its leads).
- Fill: height median 0.63; the box centre is within 0.40-0.60 on both axes on 30 of 31. Where a photo or diagram sits beside the part, the 3D part is left of centre and the picture right of centre so that the pair is centred (PMG Full [001], [006]; LSM Full [012]).
- Distance: median 175 mm (range 42-277). Leaving the card the camera pulls back by a median x1.36 (range x0.86 to x4.49; 22 of 31 pull back by a ladder click or more, 4 by less than a click, 3 hold, 2 move in).
- Elevation is chosen for the part, not the house band: flat modules face-on or in plan (0-17 or 90 deg; 7 of the 18 distinct cards), 3D-shaped parts in a normal 3/4 view (22-56 deg).
- The card and the step after it tend to share a viewing side: azimuth difference 23 deg or less on 17 of 29; 0 deg for LED Stems (pure zoom). Counter-examples: LCD Screen (167 deg), LSM Part 1 Capacitor (128 deg).
- Step-level cross-fade ("transition: fade") is set on 17 of 31 cards: all 10 LAC cards, 7 of 11 LSM cards (cable, stems and the Full Build's diagram card; not the Capacitor cards), and 0 of 10 PMG cards.

Overview guide (`lac_electronics`): two static line-ups at 513 mm and 1505 mm, elevation 34 and 44, azimuth 130 and 138; the row fills 0.56-0.64 of the frame and is slightly left of centre. Not a card pattern.

## 8. Title page and final view

| Guide | Start dist / elev / azim | Model centre x, height | Final dist / elev / azim | Final vs Start: zoom, azimuth diff | Final bbox centre (x, y), height |
|---|---|---|---|---|---|
| LAC deconstruction | 377 / 37 / 143 | 0.75, 0.68 | 238 / 50 / 50 | x1.59, 93 deg | (0.50, 0.46), 0.68 |
| LAC full build | 377 / 37 / 143 | 0.75, 0.68 | 377 / 34 / 45 | x1.00, 98 deg | (0.39, 0.48), 0.64 |
| LSM deconstruction | 374 / 29 / 54 | 0.69, 0.61 | 189 / 49 / 38 | x1.98, 16 deg | (0.51, 0.46), 0.63 |
| LSM full build | 374 / 29 / 54 | 0.69, 0.60 | 321 / 39 / 44 | x1.17, 10 deg | (0.43, 0.45), 0.74 |
| LSM part 1 | 190 / 47 / -141 | 0.71, 0.67 | 190 / 48 / -146 | x1.00, 5 deg | (0.48, 0.47), 0.59 |
| LSM part 2 | 351 / 37 / 50 | 0.67, 0.64 | 221 / 39 / 40 | x1.59, 10 deg | (0.47, 0.50), 0.67 |
| LSM part 3 | 258 / 41 / 51 | 0.72, 0.65 | 221 / 42 / 36 | x1.17, 15 deg | (0.43, 0.49), 0.69 |
| LSM part 3+4 | 321 / 27 / 57 | 0.71, 0.65 | 321 / 39 / 44 | x1.00, 14 deg | (0.44, 0.47), 0.71 |
| LSM part 4 | 321 / 27 / 57 | 0.71, 0.68 | 321 / 39 / 44 | x1.00, 14 deg | (0.44, 0.46), 0.73 |
| LSM part 1+2 | 351 / 37 / 50 | 0.67, 0.65 | 221 / 39 / 40 | x1.59, 10 deg | (0.47, 0.50), 0.67 |
| LAC part 2 | 440 / 35 / 141 | 0.71, 0.66 | 440 / 32 / 127 | x1.00, 13 deg | (0.48, 0.48), 0.78 |
| LAC part 3 | 513 / 30 / 142 | 0.70, 0.67 | 440 / 30 / 128 | x1.17, 14 deg | (0.48, 0.48), 0.76 |
| LAC part 4 | 377 / 37 / 143 | 0.75, 0.68 | 377 / 34 / 45 | x1.00, 98 deg | (0.39, 0.48), 0.64 |
| LAC part 1 | 277 / 44 / 49 | 0.71, 0.74 | 277 / 44 / 38 | x1.00, 11 deg | (0.49, 0.44), 0.67 |
| PMG deconstruction | 320 / 33 / -46 | 0.58, 0.89 | 173 / 23 / 90 | x1.85, 135 deg | (0.51, 0.68), 0.33 |
| PMG part 1 | 148 / 22 / -60 | 0.71, 0.60 | 173 / 21 / -62 | x0.86, 3 deg | (0.54, 0.47), 0.52 |
| PMG part 2 | 436 / 35 / -55 | 0.74, 0.50 | 275 / 37 / -82 | x1.59, 27 deg | (0.55, 0.43), 0.62 |
| PMG part 3 | 320 / 21 / -43 | 0.73, 0.70 | 320 / 35 / -61 | x1.00, 18 deg | (0.44, 0.47), 0.78 |
| PMG full build | 320 / 21 / -43 | 0.73, 0.70 | 320 / 35 / -61 | x1.00, 18 deg | (0.44, 0.47), 0.78 |

Title page (19 of 19 guides that have one):
- The 3D model is the only 3D content and sits in the right half: model centre x median 0.71 (range 0.67-0.75 on 18; 0.58 on PMG Decon, where the title overlaps the model). Model left edge median 0.49 (0.34-0.60). Model height median 0.67 of the frame (0.60-0.74 on 17), vertical centre 0.48.
- 3/4 hero view: elevation median 35 (21-47), azimuth on a diagonal (within 15 deg on 19 of 19).
- Two unanchored images fill the left: together the whole composition spans 0.91 of the width with a 2 % left margin and 6 % top margin.
- The first step after Start always moves the camera (19 of 19; rotation 8-110 deg, target shift 76-274 mm, because the hero is offset to the right).

Final view (Completed View / Completed Build):
- Camera moves on 17 of 19. Exceptions: PMG Part 1 (the final view is a renamed Step 14c and keeps the wiring view) and PMG Deconstruction (bare shield left where the last step left it, low in the frame at y 0.68, height 0.33).
- No annotations on 19 of 19. Model centred: box centre x median 0.47, y 0.47; height median 0.67.
- Elevation median 39 (21-50): on average 4 deg higher than Start; 10 deg or more higher in 7 guides.
- Distance: same as Start in 9, one click closer in 3, x1.59 closer in 4, x1.85-1.98 closer in 2 deconstructions (little is left), one click farther in 1.
- Azimuth: within 27 deg of the Start azimuth in 15 of 19 (median difference 14 deg). Exceptions: LAC Full and Part 4 (98 deg, shows the other end with the USB lead), LAC Decon (93), PMG Decon (135).
- Size of the last move: 5-21 deg (a settle) in 7 guides, 55-120 deg (a swing back to the hero side) in 10.

## 9. Scene swaps and the step-level fade

- 142 steps replace more than half of the visible solids (isolated close-up in or out). 127 of them also move the camera.
- The step property "transition: fade" (a cross-fade of the whole page instead of an animated fly) is set on 65 steps: 61 with a camera move; 55 on whole-scene swaps. LSM uses it on 31 of 62 swaps, LAC on 24 of 48, **PMG on 0 of 32**. It is therefore an author habit, not a kit-wide rule; without it the swap is an 800 ms camera tween with parts fading.

## 10. Rules for an auto-camera (derived defaults)

1. Never change the camera on a completed (Nc) frame or on a part-motion keyframe. Compute one camera per numbered step, from the hover state.
2. Decide whether to reuse the previous camera: reuse if the step is the same kind as the previous one and its action volume (hover/loose part + destination + lead lines) is fully inside the previous frame with a 2 % margin; always reuse within a wiring run on one module; otherwise re-aim.
3. Re-aim by orbiting, not panning: keep the target near the centre of the visible content, choose the diagonal quadrant (azimuth +-45 / +-135, tolerance 15 deg) from which the mating features and the hover gap are visible, elevation 34 deg (allowed 20-50).
4. Check the travel axis: it must be at least 45 deg from the view axis (target about 60); the on-screen travel should be about a quarter of the frame height.
5. Set the distance from the visible content, not the part: depth to content centre = 2.4 x half-diagonal of the content's bounding box (hover part included), then snap to a x1.166 ladder. Expect the content to fill about 60 % of the frame height and 40-45 % of the width at a 2:1 viewport.
6. Shift the target so the content box centre lands at (0.49, 0.47) and the hover part's top edge is no higher than 3 % from the top. Idle tethered parts may be cropped; the action may not.
7. Isolated views (cards, prep steps): hide everything else, fit the same way (height fill 0.6), choose face-on for flat boards and 3/4 for 3D-shaped parts; pull back about one to two ladder clicks (x1.36 median) when context returns.
8. Underside or side work: re-declare the up-axis for the whole block and keep a normal elevation; do not put the camera below the horizon. Optionally (LSM style) put the turn-over in an 800 ms camera-only auto step.
9. Title page: hero 3/4 at elevation 35 with the model centre at x 0.71, height 0.67. Final view: clean, centred, elevation 39, same distance as the title page or one click closer, on the title page's side of the model.

## 11. Anomalies and inconsistencies (camera-related)

- README_DATA.md describes Transition as a camera step; only 12 of 117 Transitions move the camera.
- PMG Deconstruction [007] and [012]: camera-only Transitions inside a Step N / Step Nc pair, so Step 2c and Step 3c are seen from a different view than Step 2 and Step 3 (the only 2 of 422 pairs).
- LAC Deconstruction [033] and [118]: Transitions with behaviour "pause" (need an extra click); [033] changes nothing.
- LSM Part 1 [011] "Capacitor" card: field of view 50 instead of 45, the only such step.
- PMG Part 1 final view does not move the camera (renamed Step 14c); PMG Deconstruction final view is a leftover of the last step, off-centre and small; its Start page has the title text overlapping the model.
- Orbit target far from the subject on several isolated views, so the stored distance does not indicate zoom: LAC Full [046]-[054] / Part 2 [016]-[024] (513 mm, depth ratio 0.28), LSM Step 4c / 7c close-ups (ratio 0.45), LAC Step 8c, 19c, 33c (about 0.5).
- Distances off the zoom ladder: LSM 321 and 374 (Start / final / stems), 173 (LED Stems card), 42 and 60 (Capacitor cards); LAC 125 (knob check); PMG 91, 103, 133, 142 (cards and the first steps after them).
- The same card is shot differently in sibling guides: "4-Digit Display" elevation 3 / azimuth -91 in PMG Part 2 vs 12 / -75 in the Full Build; "Capacitor" 60 mm / 5 deg in LSM Part 1 vs 42 mm / 0 deg in the Full Build; LSM Step 3/2 (matrix carry) 350 mm in Part 3 vs 300 mm in Part 3+4 and Full.
- Step-level fade is applied inconsistently (about half of the LSM and LAC scene swaps, none in PMG; 10 fades are on steps that are not scene swaps, e.g. LAC Full Step 2 and Step 25, LSM Full Step 21).
- Frames with the working model cropped by the frame edge in 17 % of renders; a few crop more than idle parts (LSM Full [073] posts at the top edge; LAC Part 3 [019] / Full [089] Step 40c fills the full frame width).
- Saved renders come in ten window shapes (1.82:1 to 2.78:1, plus one 1.21:1 in `lac_electronics`), so any stored screen-percentage layout was authored against different window shapes.
- Camera animation options are stored as strings ("false", "2") on 1035 steps and as typed values on 2.
- Step-name typos met while classifying: "Ttansition" (LAC Full [053], LAC Part 2 [023]), "Transiton" (LSM Decon [038]), "Transititon" (LAC Decon [002]), "Copmleted View" (LSM Part 3+4 [042]), "Step 14C" (LAC Part 1 [030]), "Step 20C" (LSM Part 1+2 [042]); final view named "Completed Build" in LSM Part 2 and Part 1+2.
