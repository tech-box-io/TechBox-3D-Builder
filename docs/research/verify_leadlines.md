# Verification notes: red lead lines and 3D arrows

Skeptic pass over `reports/dim_leadlines.md`. Everything below was recomputed with my own code in
`reports/_work_verify_leadlines/` (no import of the analyst's scripts) from `cadasio_raw/*.json`, cross-checked
against `digest/*.json`, and against the saved renders in `thumbs/` and `thumbs_raw/`.

## Method

- `vcore.py`: own replay of every authored step (hidden ones folded in). Visibility is taken per solid (leaf flag).
  Parent flags are not reliable: e.g. LAC Full Build [109] the hovering F4 copy has parent `visible=false` and leaves
  `true`, and it is on screen in the render.
- Pose model checked independently (`v8_model.py`, `v9_links.py`): a part's `position` replaces the translation of its
  CAD transform and its quaternion replaces the CAD rotation. With that model the part-side `links` anchors reproduce the
  stored points within 0.6 mm on 520 line ends and within 3 mm on 680 of 694 linked ends (14 worse, 32 unlinked). The
  simpler "offset added in world space" model fits only 401. `object_local_positions` on the line itself does not
  reproduce the points (325 of 696 within 3 mm) and was not used.
- Travel T = change of the line vector between the frame that shows the line and the next viewer frame; for
  cross-faded sub-assemblies T = offset between the hover copy and the copy that replaces it (`v10_travel.py`).
- Step classification from leaf-level moves / appear / disappear between Step N and the next paused frame
  (`v4_steps.py`, `v6_hunt.py`).
- Pixel checks with PIL on the full-resolution renders (`v16_px.py`, `v22_width.py`, `v18_arrowpx.py`).
- Renders opened by eye: LAC Full Build [004] [006] [092] [098] [102] [109] [123] [128]; LSM Full Build [034] [046]
  [069] [078]; LSM Part 3 [010]; PMG Full Build [073] [077] [081] [097] [101]; PMG deconstruction [001];
  LAC deconstruction [061] [082].
- Limits: 5 line showings have no resolvable travel in my replay (2 free-ended lines in LSM Part 3+4 Step 4 [008],
  2 pose-swap lines in LSM Part 3+4 Step 10 [022] whose replacement copy I could not match, and I count the stray line
  [041] separately), so my denominators are 355 / 345 where the analyst has 360 / 350. No live viewer was used.

## Headline counts (all reproduced exactly)

| quantity | analyst | mine |
|---|---|---|
| lead-line showings / frames | 363 / 155 | 363 / 155 |
| frames by kind (Step N / Transition / Step Nc) | 149 / 6 / 0 | 149 / 6 / 0 |
| lines per frame, 20 guides | {1: 37, 2: 75, 4: 41, 6: 2} | same |
| lines per frame, 3 full builds | {1: 15, 2: 33, 4: 17} | same (149 lines, 65 frames) |
| line lifetime | 359 one frame, 4 two frames | same |
| arrow showings / frames | 106 / 97 | 106 / 97 (88 with one, 9 with two) |
| arrow showings by frame kind | 96 Step N, 9 Transition, 1 mis-named | same ("Step 45c", LAC deconstruction [120]) |
| defined objects | 958 lines, 176 arrows | same; all `#ff0000`; all arrows `straight` |

## Verdicts

### LL-1 qualified
- Reproduced: rigid part tweening to its seat with lines: 56 of 59 in the full builds, 132 of 140 in the 16
  construction guides. The eight without: LAC Step 42 x2 guides (two arrows), LAC Step 44 x2 (eye icons),
  LSM Step 38 / Part 3+4 Step 18 (63 stems fade in), LSM Part 1 and Part 1+2 Step 1 (paper peel, arrow).
- "Whenever a rigid part is about to travel onto mating features" is too wide. It holds when the part is animated with a
  tween. It does not hold when the seat is shown by cross-fade or fade-in: lines on only 6 of the 11 cross-faded
  seating steps in the full builds (no lines on LSM Step 21 [046] D2 panel onto the base, PMG Step 46 [101] shield onto
  H4, LAC Step 43 buzzer, PMG Steps 33-34 [073] button modules), none for the USB plug that fades in (LAC Step 40,
  LSM Step 20), none for repeat steps (LSM Step 38, PMG Step 39).
- "On the paused Step N frame": 6 of 155 line frames are auto Transitions (PMG [106] [111] [114] and Part 3 copies).
- "If nothing is being seated, draw none": one violation, the stray 8.8 mm line on LSM Part 1+2 Step 20 [041].
- Rotation-only step with no line and no arrow: LAC Step 29 [063] / Part 2 Step 15 [033] (turn the knob).

### LL-2 qualified
- Strictly true for wires and preparation: line or arrow on 0 of 49 wire-swap steps (full builds), 0 of 104 (all
  construction guides), 0 of 23 single-wire unplug steps (deconstruction: LAC 20, LSM 3), 0 of 10 ribbon / wire-slide
  steps (5 in the full builds), 0 of 8 leg-bend steps (3 in the full builds), 0 of 8 fade-in-only steps.
  No lead-line end is linked to a wire part anywhere (0 of 694 linked ends).
- Not strict for "picking up a pre-wired module / dropping in a small module": of the 14 cross-faded sub-assembly
  steps without lines in the full builds, 10 have neither and 4 carry an arrow (LAC Step 47, LSM Steps 21 and 23,
  PMG Step 46).
- Listed exceptions check out: PMG Step 25 [057] USB tween has 1 line; wire bundles in take-apart guides get arrows
  (LSM deconstruction Step 15 [040], PMG deconstruction Steps 18 [049] and 22 [057]).

### LL-3 confirmed
- Counts exact. By class: axial 24 of 24 frames with 1; two-lead 13 of 13 with 2; breadboard onto base 5 of 5 with 4;
  pin-header boards {2: 4, 4: 5}; plywood {1: 12, 2: 45, 4: 27, 6: 2}; cross-faded {1: 1 (stray), 2: 13, 4: 4}.
- 3 never occurs. More than 4 occurs on 2 frames (LSM Part 3 [010], Part 3+4 [012]; 6 lines, two nearly coincident in
  the render); the Full Build copy [057] has 4.

### LL-4 qualified
- Verified from anchor geometry: LAC Nano 2 lines 38.8 mm apart = diagonal corner pins (15.24 x 35.56 mm pin
  rectangle); LSM and PMG Nano 4 lines on a 15.2-15.6 x 35.0-35.6 mm rectangle = the 4 corner pins; LAC RTC Pin1 and
  Pin6, 12.3 mm apart; breadboard 4 lines on a 54.8 x 81.7 mm rectangle = its corners.
- Multi-line frames: 118; lines mutually parallel within 2 deg on 99, within 5 deg on 113 (exact match).
- The plywood clause ("every engaging pair up to 4; if more, 2 on each of two neighbours") rests on two authored steps
  (LAC F5 [123], F6 [128]) and is contradicted by the 6-line cut of LSM D5 and by PMG H8 [081], H11, H12 where fewer
  than the engaging pairs are drawn. I could not count engaging pairs without mesh data. Treat it as a design choice,
  not an observed convention. Pin-header evidence is 5 distinct authorings (2 lines in two of them, 4 in three).

### LL-5 confirmed
- 333 of 363 lines linked at both ends; 28 with one unlinked end; 2 with none. 25 ends reference an object id that
  is not in the CAD tree (LAC Full Build / Part 1 Steps 3, 5, 6, 7; LSM Full Build Steps 3, 6, 8, 31).
- 694 ends are linked, 688 to a single solid and 6 to a non-leaf node (analyst: 692).
- First point on the mover: 213 of 318 tweened lines (67 %); direction of authoring is not meaningful.
- 14 ends where anchors and stored points disagree by more than 3 mm: LAC pot line [055] / Part 2 [025] (560-590 mm),
  LSM D5 and D6 steps (61-95 mm).
- "Inside the female feature" quantified on plywood plates (280 plate-crossing ends): 242 lie within the plate
  thickness or on a face, 18 stop short of the entry face, 20 overshoot the exit face.

### LL-6 confirmed
- 345 two-point lines with travel: median 0.30 deg; <= 1 deg 266; <= 2 deg 299; <= 5 deg 334. Full builds: 143 lines,
  138 within 5 deg. Largest 10.7 deg (PMG Transition [111]).
- Above 5 deg: PMG Transition [111] / Part 3 [053] (8.8-10.7), PMG Step 41 [089] / Part 3 [031] (5.0-6.1),
  LSM Step 25 [055] / Part 3+4 [010] (6.0), LAC Step 52 [115] / Part 4 [026] (4.3-5.6 against the pose offset).
- Scope note: "travel" must be read as the first stage of motion. Against the net motion to the next paused frame,
  PMG Steps 42 and 43 are 7.2 and 9.7 deg off (the lock slide is not drawn), and the 10 polyline showings are not
  straight segments.
- Descriptive addition: 301 of 353 two-point lines lie within 10 deg of a world axis (212 vertical, 62 X, 27 Z).

### LL-7 qualified
- Reproduced: L/T median 1.000, quartiles 0.94-1.09; within 10 % on 222 of 355 (63 %); within 15 % on 276 (78 %);
  T - L within +-6 mm on 267; within +-0.5 mm on 72; +2.4..+5.5 on 82; -6..-0.5 on 88. All quoted examples match.
- "Exit face of a 3 mm through-slot" is not a convention: of 280 plate-crossing ends, exit face 92 (33 %), inside the
  thickness 96, entry face 54, short of the plate 18, beyond it 20.
- What the 3.4 mm cluster is: 39 of the 82 lines fall in the 3.3-3.5 mm bin. On those steps (PMG Steps 26, 27, 28,
  38, 42, 43; LAC Steps 49, 54) the line ends exactly on the exit face and the tab then protrudes 3.4 mm beyond the
  plate. Plates are 3.0 mm thick (31 of 33 panel solids; two LSM panels 3.18), so 3.4 is tab protrusion, not thickness.
- Breadboard holes: the board is 8.5 mm thick; line ends sit 7.0 mm below its top in LAC (8 of 8 frames) and LSM
  Part 1 / 1+2, 7.4 mm in the LSM Full Build, i.e. 1.1-1.5 mm above the underside (the hole floor). 17 of 20
  breadboard-insertion frames. Exceptions: LSM Full Build Step 5 [010] (0.2-0.3 mm) and, not listed by the analyst,
  LSM Part 1 [012] / Part 1+2 [011] Step 6 (2.2-2.3 mm).

### LL-8 qualified
- Polylines: 10 showings (8 with 3 points, 2 with 5), 4 distinct lines, 2 distinct steps (LSM Step 29 in 3 guides,
  LAC Step 45 in 2). End-to-end 44.0 vs net travel 43.7 mm; 108.5-111.9 vs 107.0-110.9 mm. Seen in render [098].
- Swing chords and second-stage lines on Transitions reproduced (6 Transition frames, all PMG).
- The choice of device is not consistent. Two-leg moves inside one step: polyline on 2 distinct steps (LSM 29,
  LAC 45), fresh lines on the Transition on 3 (PMG 48, 50, 51), nothing for the second leg on 2 (PMG 42, 43).
  Stages split over two numbered steps always get their own lines (6 of 6).

### LL-9 qualified
- Geometry reproduced: 40 pose-swap line showings, L/T 0.93-1.20, angle 0-5.6 deg, PMG matrix second stage 8.8-10.7.
- Frequency: lines on 6 of 20 cross-faded steps in the full builds, 6 of the 11 that actually seat something
  (my reading of which steps seat: LAC 43, 49, 52, 54; LSM 21, 30; PMG 33, 34, 46, 48, 50; the other nine are
  pick-up or carry steps). "Still draw lead lines" describes roughly half of the cases, not a rule.

### LL-10 confirmed
- Data: `#ff0000`, scale 5, `world_units: false`, sub-type `basic` on 363 of 363 shown and all 958 defined.
  Stored solid 327, dashed 36, dotted 0 shown (5 defined).
- Renders: on 123 frames the line is 5.1-5.3 px wide (area / length; saturated core 3.2-3.4 px) at image widths
  2559, 2560 and 3840 px alike. All 14 frames with dashed-stored lines show unbroken lines (0 gaps along every one).
- Occlusion seen in [004] (rear line hidden by the breadboard) and [055] (line vanishes behind the panel and a
  71-px piece reappears in the hole). No arrowheads or end markers in any render opened.
- Anomaly: `scale` is stored as the number 5 on 819 line objects and as the string "5" on 139.

### LL-11 confirmed
- 359 of 363 one frame; the 4 others are PMG Step 51 / Part 3 Step 26 second-stage lines (on at Transition [114] /
  [056], still flagged on Step 51c / 26c). Pixel check: the two pure-red segments present in [114] are absent in [115].
- 0 lines switched on by a Step Nc. Residual if left on: median 3.48 mm, <= 5 mm on 214 of 318.

### AR-1 qualified
- Reproduced: 12 arrows on 11 of 146 Step N frames (full builds); 29 showings on 27 frames (construction guides);
  removal steps 6 of 6 (12 of 12 over all construction guides) with an arrow and no line; 4 of 20 cross-faded steps.
- "Rather than seating it on features" is contradicted by two of those four: LSM Step 21 [046] (D2 panel pushed onto
  the base) and PMG Step 46 [101] (shield lowered onto H4) are seating steps drawn with an arrow.

### AR-2 qualified
- Reproduced: 77 arrows on 70 frames; 60 of 94 Step N frames (LAC 19 of 47, LSM 21 of 24, PMG 20 of 23) plus 9 PMG
  Transition frames; 3 lead lines, all on LAC deconstruction Steps 16-18.
- "Every part that is pulled off": of 67 Step N frames that take off or move something other than a single wire,
  60 carry an arrow. The 7 without: PMG Steps 2, 3 (arrow on the Transition only), PMG Step 12, and four the analyst
  did not list: LAC deconstruction Step 5 [013], Step 6 [015] (pose swaps), Step 23 [061] and Step 31 [082] (loose LCD
  and buzzer set aside: eye icon, then fade).

### AR-3 confirmed
- Direction: 88 arrows are followed by a tween; 83 within 12 deg of the first motion of the nearest moving part
  (median 1.7 deg). The 5 others: LAC deconstruction Step 24 (77 deg) and Step 28 (82, 87 deg), and 2 on a 1.2 mm
  residue. The analyst's 79 of 87 counts the second arrow of an opposed pair as a miss.
- Pose swaps: 17 arrows; 15 within 12 deg of the pose offset, 2 at 18-25 deg (analyst: 12 and 5).
- Length / travel for aligned arrows: 1.05 (quartiles 0.79-1.39) against the first stage, 0.92 (0.73-1.17) against
  the net travel; 45 of 83 within 0.75-1.35. The claimed 0.96 sits between; the figure depends on the definition.
- Carried sub-assemblies: 101.7 mm arrow for 519.9 mm (LAC Step 47), 102.9 for 184.4 mm (LSM Step 23).
- Tail: within 5 mm of the bounding box of the nearest moving or leaving solid on 98 of 106 (median 0.1 mm); my
  box distance is more lenient than the analyst's 78 of 104.
- LAC Step 23 [049] and Part 2 Step 9 [019]: stored points 177 deg from the anchors (confirmed).

### AR-4 confirmed
- 106 of 106 straight, `#ff0000`, opacity 1, two points. Proportions 5:20:17 on 74, 5:20:15 on 14, 11 other
  combinations on 18. Head at the end on 104.
- World size (params x scale x mm per unit): body median 4.27 mm (10th-90th percentile 2.58-7.58; min 1.28, max
  11.80), head width 16.67, head length 14.38; head length / arrow length 0.28.
- Pixel check on 9 renders: body width / length tracks the prediction (0.033 vs 0.030 [034]; 0.102 vs 0.085 LAC
  [046]; 0.128 vs 0.115 PMG deconstruction [025]); two are about half the prediction because the flat shape is seen
  obliquely.

### AR-5 qualified
- 88 frames with one, 9 with two, 0 with more.
- The wording "a group of identical parts shares one arrow; two arrows only for two different parts" does not match:
  on 7 of the 9 two-arrow frames the two arrows belong to two identical parts, one each (F7 posts: LAC Step 42,
  Part 4 Step 2, LAC deconstruction Steps 26, 28; lens supports: LSM deconstruction Steps 6, 7; matrix supports:
  Step 10). No step moves exactly two identical parts with a single shared arrow. Sharing happens for four or more
  identical parts (64 stems, 4 keys, 4 button modules) or a sub-assembly moved as one (for example LSM deconstruction
  Step 4 [010]: four lens supports and a side panel, one arrow).

### AR-6 confirmed
- One frame in 20 guides has both (LSM Part 1+2 Step 20 [041]). All 176 arrow objects are `straight`.

### AR-7 qualified
- 106 of 106 one frame; 96 / 9 / 1 by frame kind.
- "For a removal, follow with an auto-advancing keyframe": 44 of 44 tween-removal steps (12 construction,
  32 deconstruction) do. But of the 60 deconstruction Step N frames with an arrow, 20 go straight to the result frame
  (13 where the part only fades out, 4 tweens, 3 pose swaps).

## Missed or under-stated patterns

1. Two identical parts each get their own arrow (7 of 7); see AR-5.
2. Arrows are world-axis shapes, not camera-facing: direction within 10 deg of a world axis on 96 of 106; the flat
   plane's normal is a world axis on 92 and perpendicular to the arrow on 98; median angle between that normal and the
   view direction is 49 deg (within 45 deg on only 39).
3. T - L = 3.4 mm is tab protrusion past the plate with the line ending on the exit face (LL-7).
4. Breadboard-hole ends share one plane per guide, the hole floor 1.1-1.5 mm above the board's underside.
5. Arrows carry explicit `animation_show` / `animation_hide` = fade and `animation_attention` = none (106 of 106);
   lines have no show / hide setting and attention none (363 of 363). No pulsing or attention effect anywhere.
6. On 83 of 149 Step N line frames the moving part fades in at its hover pose on the same frame as the lines; on 62
   it was already on screen.
7. Line width is a fixed pixel count, not a share of the viewport (0.20 % at 2559 px, 0.13 % at 3840 px).
8. Lines routinely cross wiring and other parts (PMG [077] 139 mm lines over the wire loom; LAC [098]); a 7.3 mm
   marker line (LAC Step 46 [102]) is practically invisible in the render.
9. Frame-name anomalies around arrow steps that a name-keyed player would trip on: "Ttansition" (LAC Step 24, Part 2
   Step 10), "Transititon" and "Transiton" (deconstruction), "Step 20C", "Step 45c" used for a Step 45, and LAC
   deconstruction "Step 41" followed by "Step 40".

## Numeric defaults

Confirmed as stated: colour; solid style; 1 visible frame; lines per frame; axial 1; two-lead 2; pin-header 4 or 2;
flat body 4; parallel tolerance; L/T 1.00 (276 of 355 in 0.85-1.15); residual 3.5 mm; plywood 3 mm; all seven travel
medians (2-lead 32.9, pin-header 35.3, breadboard 46.9, axial 60.9, plywood 64.4, wired module 11.1, wired panel
57.2 mm); polyline; arrow colour / type; proportions; world size; arrows per frame; frames visible.

Corrected or narrowed: line width (drop the 0.2 % figure); through-slot offset (tab protrusion, 33 % of plate
crossings); blind-hole depth (17 of 20 frames, one more exception); arrow length percentile (the 90th percentile
falls in an empty gap between 86.5 and 101.7 mm; 95 of 106 arrows are 86.5 mm or shorter); arrow length / travel
(0.92-1.05 depending on definition); arrow direction (83 of 88); tail distance (method-dependent).
