# LAC deconstruction: the published take-apart's geometry, in our frame

Study for the LAC Deconstruction guide (21 Oct 2026; read-only: no kit file, guide or steps file changed; nothing that loads the CAD
was run). TechBox's published take-apart, `https://instructions.online/?id=19075-lac_deconstruction` (47 numbered steps, 130 viewer
frames), converted to our assembly frame: every camera as `view_dir=` + `frame=(target, radius)`, every arrow as tail / tip / `dims=`,
every eye, label, close-up and lead line as a point in our mm, and every part move as a pose relative to the part's seat, ready for
`deconstruction.py` (`path=`, `paths=`, `arrow_style=`, `view_dir=`, `frame=`, `inset=`).

- Data: `published_geometry.json` (this folder). `by_step` (Steps 1 - 47: camera, arrows, eyes, labels, close-ups, lead lines from the
  step's instruct frame, then every frame's motion: parts moved with their poses, posed copies faded in, wire bodies shown), `start`,
  `completed_view`, `frames` (all 130 viewer frames in full), `meta.mapping` (each Cadasio part -> our id).
- Scripts (`scripts/`, light: JSON only, about 3 s, under 100 MB): `lacpub.py` (the payload's tree, the replay, world placements),
  `published_geometry.py` (writes the JSON), `show.py` (prints frames), `make_tables.py` (the tables below), `check_projection.py`
  and `check_poses.py` (the checks below), `list_parts.py`, `dump_tb.py`. Run with `.venv.nosync/bin/python`.
- Frames are numbered as the viewer shows them (hidden steps skipped, Start = 0), as in `docs/research/guide_19075-lac_deconstruction.md`.

## 1. How the payload was read, and the checks

- Replay: every step's `properties` change the state left by the step before, in `orderedSteps` order, hidden steps included.
  Visibility per leaf solid (start: no node of its chain `hidden`; then only the leaf's own `visible`), as the report's "Data caveat"
  says. A node's `position` / `rotation` (quaternion) replace its local translation / turn; the tree's `transform` is a three.js
  column-major Matrix4 (the home placement); world = the chain multiplied out. mm = scene units / scaleFactor (0.6054634; 1 unit =
  1.65163 mm), no turn and no offset: the published scene is our assembly frame (cad_study.md section 7).
- A posed copy's pose (F1-2 of F1-1, the LCD's V1-2 of V1-1 ...) = its world matrix now x inverse(the seated copy's home matrix),
  written about the seated part's box centre (`pose`) and, for a turn, as a hinge (`pose_hinge` = `turned(axis, degrees, a point on
  the axis, t = slide along the axis)`, the point nearest the part's middle). A part that rides on another (knob, nut, washer on the
  potentiometer; the potentiometer on F1; the switch on F4) also gets `rel_to`: its pose relative to its carrier's move, i.e. a ride
  pose in the carrier's seated frame, as guide.py writes them.
- **Check 1, cameras and placements:** every eye, label and close-up ring (27 eyes, 4 labels, 2 close-ups), placed by this replay
  in our mm and projected with the published camera (vertical fov 45, the pictures' 1400 x 676), lands on Cadasio's own stored screen
  position for it (`target_position`) within 0.1 % of the frame. So the cameras, the world placements and the anchors are right.
- **Check 2, arrows:** the Step 1 arrow projected lands on the red arrow in `published/pictures/.../001.jpg` (tail 731, 372 px, tip
  868, 458); Steps 2, 25 and 26 checked by eye on the contact sheets. The arrows' `points` are what is drawn. Their
  `object_local_positions` (offsets from the solids under the cursor when placed) do not reproduce them (40 - 110 mm off): ignore them.
- **Check 3, sanity of the moves:** F6 comes off along our -z by 67.45 mm (our build Step 57 puts it on along +z by 67.5), F5 +z
  56.04, F8 +x 94.18. The posed copies match the CAD's copies in `wire-paths.json` "poses" to 0.01 mm: F1_hover_front, pot_flat_other_end,
  lcd_lying, lcd_standing_out, buzzer_lying, switch_flat_F4, switch_hover. Two differ: F1-4 (F1 laid flat beyond the -z end) is 0.92 mm
  lower than F1_flat_other_end (as the published build: published_motions.md), and the knob with it 2.14 mm higher than
  knob_flat_other_end.
- Units of the arrows: `body_width 5`, `head_width 20`, `head_length 17` are in the arrow's own units, multiplied by its `scale`
  (0.35 - 0.75 here) to scene units, then / scaleFactor to mm: shaft w = 5 x scale / 0.60546 = 8.26 x scale mm, head 4 w wide and
  3.4 w long (`docs/research/lsm/decon/arrows/measure_arrows.py`, calibrated on the PMG's 31 arrows). Our player draws the head 4 w wide
  and min(0.6 L, 3.4 w) long, so `dims=(L, w)` reproduces the published arrow.
- Cameras: `view_dir` = unit(eye - target); `radius` = distance x sin(22.5 deg) / 1.08 = distance / 2.822 (player/js/core.js
  cameraPose, frame_padding 1.08), which puts our eye exactly where Cadasio's was, same vertical framing, in a landscape window. Checked
  against the worked examples: published_motions.md (237.5 -> 84.2, 277 -> 98.2, 323.1 -> 114.5, 376.8 -> 133.5, 439.5 -> 155.7: the
  same here to 0.05) and the LSM study (radius x 2.82 = distance). Cadasio authored at 2.07:1: at 16:9 our sides are cut about 14 %.
  The title page and the Completed View are placed by `framedPose` in our player (direction kept, distance by the frame), not by
  this rule.

## 2. Cameras

Published distances come from the zoom ladder 237.5, 277, 323.1, 376.8, 439.5 mm. The camera changes on 18 frames (each the first
frame of the steps listed). Steps 1 - 8 reuse the published Full Build's cameras exactly (Step 3 = build 55: target (688.4, 888.4,
1297.7), dir (0.596, 0.499, 0.629), 376.8; Step 4 = build 53/54; Step 6 = build 51/52; Step 8 = build 49), Steps 9 - 47 have new ones.

| frame | published step(s) | `view_dir=` | target | distance | `frame=` radius | el / az | screen up |
|---|---|---|---|---|---|---|---|
| 000 | Start | (0.4769, 0.6039, -0.6386) | (739.0, 857.5, 1393.2) | 376.8 | 133.5 | 37.2 / 143.2 | world +y |
| 001 | 1 (F6) | (0.5882, 0.5876, -0.5556) | (633.2, 830.5, 1316.6) | 439.5 | 155.7 | 36.0 / 133.4 | world +y |
| 004 | 2 (F2) | (-0.4791, 0.6625, 0.5758) | (694.1, 892.3, 1270.6) | 439.5 | 155.7 | 41.5 / -39.8 | **world -x** (roll -119 deg) |
| 008 | 3 (F5) | (0.5964, 0.4991, 0.6287) | (688.4, 888.4, 1297.7) | 376.8 | 133.5 | 29.9 / 43.5 | world +y |
| 011 | 4, 5 (F1 forward, laid aside) | (0.6050, 0.6635, -0.4402) | (706.6, 874.2, 1253.3) | 376.8 | 133.5 | 41.6 / 126.0 | world +y |
| 015 | 6 (LCD unclipped) | (0.6975, 0.4947, 0.5185) | (670.6, 875.2, 1275.4) | 439.5 | 155.7 | 29.6 / 53.4 | world +y |
| 019 | 7 (F8) | (0.5117, 0.6969, -0.5024) | (689.6, 889.4, 1273.7) | 323.1 | 114.5 | 44.2 / 134.5 | world +y |
| 022 | 8 (F4) | (0.6965, 0.5509, -0.4598) | (678.6, 923.4, 1294.9) | 323.1 | 114.5 | 33.4 / 123.4 | world +y |
| 025 | 9 - 11 (pot wires) | (0.6840, 0.6972, -0.2145) | (644.9, 867.8, 1241.9) | 439.5 | 155.7 | 44.2 / 107.4 | world +y |
| 031 | 12 - 14 (knob, nut, washer) | (-0.5658, 0.6112, -0.5535) | (736.9, 889.0, 1101.5) | 277.0 | 98.2 | 37.7 / -134.4 | **world -x** (roll +122) |
| 041 | 15 (pot out of F1) | (-0.5616, -0.4017, -0.7234) | (734.8, 913.9, 1100.0) | 277.0 | 98.2 | -23.7 / -142.2 | **world -x** (roll +73) |
| 043 | 16 - 18 (washer, nut, knob back on) | (-0.6542, 0.4589, -0.6012) | (776.8, 801.9, 1099.3) | 277.0 | 98.2 | 27.3 / -132.6 | **world -x** (roll +117) |
| 049 | 19 - 23 (LCD wires, LCD away) | (0.6549, 0.7327, 0.1851) | (666.0, 854.6, 1330.6) | 323.1 | 114.5 | 47.1 / 74.2 | world +y |
| 063 | 24, 25 (F9, USB) | (0.5650, 0.5802, 0.5866) | (647.1, 893.0, 1296.5) | 323.1 | 114.5 | 35.5 / 43.9 | world +y |
| 070 | 26 - 34 (F7s, buzzer, buzzer and switch leads) | (0.7131, 0.5802, 0.3935) | (644.2, 892.6, 1291.2) | 323.1 | 114.5 | 35.5 / 61.1 | world +y |
| 090 | 35 (switch out of F4, alone) | (0.6657, 0.4223, -0.6152) | (561.0, 962.0, 1282.8) | 277.0 | 98.2 | 25.0 / 132.7 | world +y |
| 092 | 36 - 47 (jumpers, RTC, resistors, Nano) | (0.5663, 0.7152, 0.4096) | (672.5, 860.9, 1291.8) | 277.0 | 98.2 | 45.7 / 54.1 | world +y |
| 129 | Completed View | (0.4954, 0.7631, 0.4151) | (678.1, 853.2, 1292.7) | 237.5 | 84.2 | 49.7 / 50.0 | world +y |

Our player keeps world +y up on screen (a `flip=True` view turns the model 180 deg; nothing rolls the camera). So:

- **Steps 12 - 18** (the isolated F1 and potentiometer): Cadasio shows the copy F1-4, lying face up beyond the -z end (turned 90 deg about
  z), with the scene's up switched to -x, which is exactly the turn that copy has: seen in **F1's (and the potentiometer's) seated frame
  the roll is 0**. For a take-apart that shows F1 + the potentiometer alone and seated (or carried by a pure translation, as our build
  does with `BUILD` / `PULLED`), these are the published views exactly:

  | frame | steps | in the seated frame of | `view_dir=` | target | radius | el / az |
  |---|---|---|---|---|---|---|
  | 031 | 12 - 14 | F1 (NAUO10) | (0.6112, 0.5658, -0.5535) | (699.9, 872.0, 1289.3) | 98.2 | 34.5 / 132.2 |
  | 041 | 15 | F1 (NAUO10) | (-0.4017, 0.5616, -0.7234) | (724.8, 874.1, 1287.8) | 98.2 | 34.2 / -151.0 (from behind F1) |
  | 043 | 16 - 18 | the potentiometer (NAUO11), pushed 65.8 mm out of F1's back (F1 hidden) | (0.4589, 0.6542, -0.6012) | (678.6, 832.1, 1287.1) | 98.2 | 40.9 / 142.6 |

  (Add the translation of the pose the parts are shown at to the target. Cadasio's orbit targets here sit 50 - 95 mm off the parts:
  the parts are off-centre in the published pictures too.)
- **Step 2** (F2): the case is shown with -x up, as if lying on its front with F2 on top, the arrow pointing up the screen. Our player
  cannot roll the view: the same eye with world up is the published picture turned 119 deg. Our own Full Build Step 56 camera (from
  behind, dir (-0.7035, 0.5025, -0.5025), target (640, 915, 1290), radius 125) is 68 deg from it.
- **Step 35** (F4 alone, flat beside the base at the pure translation [-117.83, 17.26, -0.06]): in F4's seated frame, view_dir
  (0.6657, 0.4223, -0.6152), target (678.8, 944.8, 1282.8), radius 98.2.

Our Full Build's camera for the step each one undoes (stepgen's default for remove()), against the published: Step 1 vs our 57: 8.6
deg apart, published 1.42x wider; 2 vs 56: 68 deg (the roll above); 3 vs 55: 18.5 deg, 1.16x; 4 vs 54: 9.5 deg, 1.11x; 6 vs 52: 8.7
deg, 1.42x; 7 vs 50: 76 deg (ours from the +z end, published from the -z end), 1.18x; 8 vs 49: 13 deg, 1.04x; 9 vs 32: 76 deg, 3.7x;
12 vs 28 (seated frame): 22.5 deg, same radius; 15 vs 25: 45 deg, same; 16 vs 24: 18 deg, 2.3x; 19 vs 36: 18 deg, 1.67x; 24 vs 45: 6.2
deg, same; 26 vs 42: 62 deg, 1.04x; 35 vs 15: 24 deg, 1.58x; 36 vs 13: 41 deg, 3.8x; Completed View: 63 deg, 0.58x (published closer).
The published take-apart never comes closer than 277 mm (radius 98) while working; ours is often 2 - 4x closer.

## 3. Arrows

22 arrows on 20 steps. All `#ff0000`, straight, `body_width 5`, `head_width 20`, `head_length 17`, per-arrow `scale` 0.35 - 0.75.
"Placed on" is only the solid under the cursor when the arrow was put down (Cadasio does not tie it to it); "pulls" is the part the
step moves. Each arrow is axis-aligned within 3 deg and along the removal; its tail is where `arrow_style={id: dict(at=tail, dims=...)}`
would put ours.

| step (frame) | pulls | dir | tail (mm) | tip (mm) | L | shaft w | head w x l | `dims=` | travel that follows | L / travel |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 (001) | F6 | -z | (728.29, 918.30, 1212.36) | (730.56, 918.10, 1156.34) | 56.1 | 4.87 | 19.5 x 16.6 | (56.1, 4.87) | 67.5 | 0.83 |
| 2 (004) | F2 | -x | (645.22, 958.23, 1291.32) | (565.41, 958.15, 1291.56) | 79.8 | 5.51 | 22.0 x 18.7 | (79.8, 5.51) | 21.4 deg turn, then 78.1 | 1.02 |
| 3 (008) | F5 | +z | (683.78, 881.40, 1368.15) | (683.43, 881.38, 1432.72) | 64.6 | 6.19 | 24.8 x 21.1 | (64.6, 6.19) | 56.0 | 1.15 |
| 4 (011) | F1 (pulled forward) | +x | (721.38, 880.86, 1286.05) | (800.23, 876.89, 1285.84) | 79.0 | 5.78 | 23.1 x 19.6 | (79.0, 5.78) | cross-fade, 76.7 | 1.03 |
| 7 (019) | F8 | +x | (706.38, 925.49, 1267.42) | (790.28, 924.82, 1269.80) | 83.9 | 4.51 | 18.0 x 15.3 | (83.9, 4.51) | 94.2 | 0.89 |
| 8 (022) | F4 (lifted) | +y | (721.42, 951.24, 1286.01) | (721.97, 1024.41, 1286.76) | 73.2 | 3.35 | 13.4 x 11.4 | (73.2, 3.35) | cross-fade, 49.8 | 1.47 |
| 12 (031) | knob | along the shaft (world +y) | (690.49, 927.30, 1039.33) | (690.09, 968.47, 1037.94) | 41.2 | 2.93 | 11.7 x 10.0 | (41.2, 2.93) | 52.7 | 0.78 |
| 13 (035) | nut | along the shaft | (690.60, 915.36, 1041.52) | (691.04, 971.79, 1039.06) | 56.5 | 3.72 | 14.9 x 12.6 | (56.5, 3.72) | 58.7 | 0.96 |
| 14 (038) | washer | along the shaft | (689.81, 913.07, 1042.65) | (689.25, 983.65, 1043.18) | 70.6 | 2.89 | 11.6 x 9.8 | (70.6, 2.89) | 55.0 | 1.28 |
| 15 (041) | potentiometer (out of F1's back) | against the shaft (world -y) | (689.53, 906.80, 1037.73) | (689.58, 854.09, 1039.14) | 52.7 | 4.21 | 16.9 x 14.3 | (52.7, 4.21) | 66.7 | 0.79 |
| 24 (063) | F9 | +y | (697.90, 953.70, 1358.12) | (697.73, 987.46, 1358.06) | 33.8 | 3.30 | 13.2 x 11.2 | (33.8, 3.30) | 25.8 deg tilt, then 33.0 up | 1.02 |
| 25 (067) | USB cable (Mini-B plug) | +z | (676.50, 907.60, 1352.95) | (676.68, 906.71, 1416.41) | 63.5 | 5.78 | 23.1 x 19.6 | (63.5, 5.78) | 43.3 | 1.47 |
| 26 (070) | F7A spread | -x | (660.74, 918.41, 1243.69) | (623.84, 918.65, 1244.77) | 36.9 | 3.75 | 15.0 x 12.7 | (36.9, 3.75) | 15.1 deg tilt (top 18 mm out) | - |
| 26 (070) | F7B spread | +x | (691.77, 921.08, 1243.91) | (732.26, 922.14, 1245.34) | 40.5 | 3.80 | 15.2 x 12.9 | (40.5, 3.80) | 16.0 deg tilt (top 19 mm out) | - |
| 27 (072) | buzzer | +z | (676.42, 935.35, 1231.59) | (675.21, 934.84, 1289.86) | 58.3 | 6.15 | 24.6 x 20.9 | (58.3, 6.15) | cross-fade to lying | - |
| 28 (074) | F7B | +y | (711.37, 952.98, 1233.48) | (709.61, 990.20, 1231.61) | 37.3 | 3.96 | 15.9 x 13.5 | (37.3, 3.96) | straightened, then 44.4 up | 0.84 |
| 28 (074) | F7A | +y | (640.27, 955.52, 1234.15) | (640.05, 989.67, 1232.60) | 34.2 | 3.96 | 15.9 x 13.5 | (34.2, 3.96) | straightened, then 44.4 up | 0.77 |
| 35 (090) | switch (out of F4, alone) | +y | (561.18, 971.46, 1257.70) | (561.23, 1034.86, 1262.09) | 63.5 | 4.95 | 19.8 x 16.9 | (63.6, 4.95) | 85.1 | 0.75 |
| 44 (117) | RTC + coin cell | +y | (658.31, 937.99, 1289.93) | (659.35, 967.79, 1290.29) | 29.8 | 3.55 | 14.2 x 12.1 | (29.8, 3.55) | 21.7 | 1.37 |
| 45 (120) | resistor RES1 (NAUO6, h27) | +y | (682.29, 900.38, 1276.64) | (682.78, 939.79, 1277.61) | 39.4 | 3.47 | 13.9 x 11.8 | (39.4, 3.47) | 51.6 | 0.76 |
| 46 (123) | resistor RES2 (NAUO7, h29) | +y | (682.31, 902.20, 1271.49) | (681.82, 949.01, 1272.18) | 46.8 | 3.96 | 15.9 x 13.5 | (46.8, 3.96) | 50.7 | 0.92 |
| 47 (126) | Nano | +y | (676.84, 887.99, 1324.80) | (677.41, 952.12, 1321.58) | 64.2 | 3.72 | 14.9 x 12.6 | (64.2, 3.72) | 55.0 | 1.17 |

The isolated scenes' arrows in the seated frame (the frame of the cameras above): Step 12 (738.23, 918.44, 1227.14) -> (779.40, 918.84,
1225.75), +x along the shaft from the knob's face, 8 mm to the -z side of the axis; Step 13 (726.29, 918.33, 1229.33) -> (782.72,
917.89, 1226.87); Step 14 (724.00, 919.12, 1230.46) -> (794.58, 919.68, 1230.99); Step 15 (717.73, 919.40, 1225.54) -> (665.02, 919.35,
1226.95) (-x, out of F1's back); Step 35, F4 seated: (679.01, 954.20, 1257.76) -> (679.06, 1017.60, 1262.15). In the published pictures
Steps 12 - 14 start on the bushing / knob and run about one shaft length past the tip, as the build's did (published_motions.md).

Lengths 29.8 - 83.9 mm (median 56), widths 2.9 - 6.2 mm: bigger than our generator's own (15 - 40 mm, 1.6 - 3.2 mm), the same order as
the PMG's and LSM's published arrows that their deconstructions copy with `dims=`.

## 4. Eyes, labels, close-ups, lead lines

Eyes (the one eye picture, 7.81 % of the frame wide, a light-blue leader to a dashed ring): the ring is where the leader ends, our mm;
"icon at" is the eye picture's top-left in % of the 2.07:1 frame. On a wire, the eye is always on its male cap in the breadboard.

| step (frame) | ring (our mm) | on (our id) | what | icon at (x %, y %) |
|---|---|---|---|---|
| 2 (004) | (642.67, 897.68, 1339.72) | USB cable (NAUO123) | where it passes F2's slit | (43.5, 11.0) |
| 5 (013) | (800.49, 926.61, 1217.59) | F1 at FRONT_OUT (F1-2) | lay F1 aside | (51.6, 58.4) |
| 6 (015) | (713.76, 895.78, 1358.05) | LCD (NAUO94), seated | its F9 end, low | (30.8, 58.3) |
| 9 (025) | (700.08, 899.48, 1330.78) | cap NAUO14 | pot black, (-) blue | (17.1, 54.1) |
| 10 (027) | (690.14, 897.58, 1332.38) | cap NAUO33 | pot tan, a5 | (25.9, 54.2) |
| 11 (029) | (697.57, 897.93, 1331.16) | cap NAUO34 | pot red, (+) red | (24.8, 57.8) |
| 19 (049) | (700.05, 900.15, 1279.73) | cap NAUO82 | LCD purple (GND), (-) blue | (67.7, 54.1) |
| 20 (052) | (697.54, 899.43, 1279.93) | cap NAUO84 | LCD yellow (VCC), (+) red | (63.6, 52.1) |
| 21 (055) | (687.52, 901.87, 1325.05) | cap NAUO86 | LCD teal (SDA), b8 | (53.1, 58.0) |
| 22 (058) | (687.59, 901.05, 1320.93) | cap NAUO93 | LCD blue (SCL), b9 | (56.9, 59.7) |
| 23 (061) | (727.62, 904.67, 1431.16) | LCD lying (V1-2 = lcd_lying) | take the LCD away | (16.5, 25.5) |
| 25 (067) | (607.84, 880.08, 1414.30) | USB_A | the USB cable | (16.5, 42.1) |
| 27 (072) | (676.10, 934.26, 1226.81) | buzzer (NAUO62), seated | its top | (64.0, 11.7) |
| 29 (078) | (661.97, 902.07, 1334.67) | cap NAUO58 | buzzer red, j4 | (34.1, 31.1) |
| 30 (080) | (700.05, 900.99, 1341.18) | cap NAUO59 | buzzer black, (-) blue | (36.0, 33.3) |
| 31 (082) | (676.90, 910.19, 1400.87) | buzzer lying (buzzer_lying) | take the buzzer away | (18.5, 41.5) |
| 32 (084) | (661.32, 902.03, 1270.08) | cap NAUO48 | switch black, j29 | (59.0, 26.7) |
| 33 (086) | (697.53, 902.12, 1270.35) | cap NAUO49 | switch tan, (+) red | (64.2, 29.0) |
| 34 (088) | (661.05, 902.06, 1275.20) | cap NAUO47 | switch red, j27 | (57.9, 23.9) |
| 36 (092) | (700.07, 901.54, 1310.63) | cap NAUO15 | jumper white, (-) blue end | (60.4, 51.0) |
| 37 (095) | (697.53, 901.54, 1310.83) | cap NAUO31 | jumper dark_red, (+) red end | (62.2, 51.3) |
| 38 (098) | (690.11, 902.15, 1324.73) | cap NAUO25 | jumper purple, a8 end | (58.0, 60.1) |
| 39 (101) | (690.12, 901.89, 1322.42) | cap NAUO22 | jumper blue, a9 end | (58.6, 55.9) |
| 40 (104, 105) | (700.00, 902.10, 1285.71) | cap NAUO20 | jumper green, (-) blue end | (62.0, 53.8) |
| 41 (108) | (697.35, 902.11, 1285.77) | cap NAUO17 | jumper black, (+) red end | (60.3, 55.0) |
| 42 (111) | (662.01, 901.67, 1342.58) | cap NAUO53 | jumper orange, j1 end | (24.4, 24.1) |
| 43 (114) | (662.01, 901.42, 1337.33) | cap NAUO56 | jumper yellow, j3 end | (29.2, 15.2) |

Labels (Steps 19 - 22, Arial bold black, light-blue underline, leader to a dashed ring on the LCD's female cap, with the LCD lying face
down beside the +z end, `lcd_lying`): "GND" at (29.9, 37.2) %, ring (705.92, 913.99, 1385.30) on cap NAUO81; "VCC" (30.0, 37.2) %,
(707.55, 913.94, 1387.80) on NAUO80; "SDA" (28.4, 38.2) %, (710.14, 913.49, 1386.80) on NAUO79; "SCL" (28.3, 39.3) %, (713.02, 913.57,
1387.24) on the lying LCD's header (by NAUO78). In our terms: each wire's female end at the lying LCD's header, labelled with its pin.

Close-ups (pictures, not model views; the build's own pictures reused; the red boxes are drawn into the pictures, not in the data):
- Step 6 (015): `ASS5757488f-....png` (the build's Step 52 picture: F9's two notches holding the LCD, two red boxes), top left at
  (19.6, 2.9) %, 15.0 % wide, height / width 1.37, leader to **(714.29, 944.01, 1357.28)** on F9 (its upper notch). Our Full Build
  Step 52c already has this close-up as a model view: target (713.1, 919.5, 1356.5), dir (0.5963, 0.2981, 0.7454), radius 34, marks at
  (712.1, 947.3, 1356.5) and (712.1, 892.6, 1356.5), half 3.
- Step 24 (063): `ASSc25abb5a-....png` (the build's Step 45c picture: F9's front foot hooked in F3's slot, one red box) at (71.2, 34.7)
  %, 20.3 % wide, h / w 0.95, leader to **(717.97, 883.56, 1355.89)** (F9's front foot, under F3's top). Our Full Build Step 45c has it:
  target (716.0, 885.5, 1355.8), dir (0.1497, 0.1997, 0.9684), radius 10, mark 3, F3 ghosted 0.25.

Lead lines (only for the three parts put back on the bare potentiometer, Steps 16 - 18, along the shaft; in the potentiometer's seated
frame): 16 washer (774.96, 919.62, 1235.28) -> (714.25, 919.53, 1235.26), 60.7 mm; 17 nut (760.56, 919.25, 1235.11) -> (721.38,
919.62, 1235.28), 39.2 mm; 18 knob (721.38, 919.62, 1235.28) -> (770.32, 919.62, 1235.28), 48.9 mm. (World, F1-4 frame: 16 (689.31,
898.20, 1047.47) -> (689.40, 837.49, 1047.45); 17 (689.68, 883.80, 1047.30) -> (689.31, 844.62, 1047.47); 18 (689.31, 844.62,
1047.47) -> (689.31, 893.56, 1047.47).)

## 5. Every part move, as a pose from the part's seat (our axes)

Poses in stepgen's form (`[dx, dy, dz]`, or `turned(axis, degrees, at, t)`); "rides" = relative to its carrier's own pose (guide.py's
ride form). The `wire-paths.json` "poses" key is named where the published copy is the CAD's copy. "fade" = a cross-fade between
posed copies (no motion).

| step | part | published motion | pose(s) from the seat |
|---|---|---|---|
| 1 | F6 | tween out (Transition [002]) | `[0.0, 0.0, -67.45]` |
| 2 | F2 | tilt ([005]) then slide ([006]) | 1) `turned([0, 1, 0], 21.40, [639.96, 919.53, 1365.79])`: swung about the vertical through x 639.96, z 1365.79 (1.7 mm outside F2's outer face, at F5's inner face), its F6 end out to -x; 2) `turned([0, 1, 0], 21.40, [639.96, 919.53, 1365.79], [-42.72, 0.0, -65.41])` (slides 78.1 mm, 33 deg off -z towards -x: hooks out of F5, away from the case) |
| 3 | F5 | tween out ([009]) | `[0.0, 0.0, 56.04]` |
| 4 | F1 + potentiometer + knob | fade to pulled forward (4c) | F1 `[76.66, 0.0, 1.08]` (= `F1_hover_front`); pot rides `[0, 0, 0]`; knob rides on the pot `[-0.22, 0, 0]`. The nut and washer are not shown from 4c to 11c (a published slip) |
| 5 | F1 + pot + knob | fade to laid flat beyond the -z end, face up (5c) | F1 `turned([0, 0, 1], 90.0, [722.33, 919.53, 1289.87], [-32.93, -8.14, -187.81])` (= `F1_flat_other_end` 0.92 mm lower); pot rides on F1 `[0.91, 0, 0]` (= `pot_flat_other_end`); knob rides on the pot `turned([-1, 0, 0], 41.83, [732.56, 919.53, 1235.26], [-1.06, 0, 0])` (spun 41.8 deg about the shaft) |
| 6 | LCD + its 4 wires | three fades: [016] (1600 ms), [017] (1600 ms), 6c | 1) standing, pulled 14.88 mm through F8's notch, out of F9's notches: `[0.07, 0.38, -14.88]` (= `lcd_standing_out`; wires NAUO117 - 120, caps NAUO113 - 116); 2) angled: `turned([0, 1, 0], 14.0, [723.37, 919.52, 1265.11], [0.0, 2.14, 0.0])` (its F9 end swung 23 mm out in front of F9 about the vertical 3 mm in front of F8's notch, 2.14 up; wires NAUO109 - 112, caps NAUO105 - 108); 3) lying face down beside the +z end: `turned([0.70711, -0.70711, 0], 180.0, [713.01, 919.52, 1311.22], [14.96, -15.70, 119.04])` (= `lcd_lying`; wires NAUO83, 85, 87, 92, caps NAUO78 - 81). The build's 51 - 52 reversed |
| 7 | F8 | tween out ([020]) | `[94.18, 0.0, 0.0]` |
| 8 | F4 + switch + 3 leads | fades: [023], 8c | 1) over the frame `[0.0, 49.8, 0.0]` (switch `[0.0, 49.8, -0.2]` = `switch_hover`; leads NAUO147 - 149); 2) flat beside the base (-x side) `[-117.83, 17.26, -0.06]` (switch `[-117.68, 17.26, -0.06]` = `switch_flat_F4`, 0.14 mm off F4's copy; leads: Cadasio bodies Part23 - 25, not in our CAD). (Our Full Build's flat F4, `FLAT_F4`, is 35 mm nearer the base.) |
| 9 - 11 | pot leads, black / tan / red | fade, one per step | plugged routes NAUO159 / 158 / 157 (Part88 / 87 / 86, F1 laid flat beyond -z) fade out; the straight 50 mm leads NAUO152 / 151 / 150 with caps NAUO128 / 129 / 130 fade in, lying straight along +x under F1-4 at y 907 - 908.6 from x 702.5 to 760.4 (caps x 748.4 - 760.4, pins +x), z 1052.7 / 1047.4 / 1042.0 |
| 12 | knob | isolated (F1, pot, knob, nut, washer); tween [032], fade 12c | rides on the pot: `turned([-1, 0, 0], 41.83, [732.56, 919.53, 1235.26], [-1.06, 0, 0])` -> same turn, `[51.68, 0, 0]` (52.74 along the shaft, no spin) |
| 13 | nut | tween [036] | rides on the pot: `turned([-0.99975, -0.02205, -0.00206], 55.64, [725.11, 919.53, 1235.26], [-0.02, -0.28, -0.16])` -> `t [58.67, -0.28, -0.15]` (58.7 along the shaft, **not spun off**, unlike the build's [050]) |
| 14 | washer | tween [039] | rides on the pot: `turned([0.99995, 0, 0.01034], 180.0, [724.03, 919.53, 1235.26], [-0.60, 0.08, 0.02])` -> `t [54.40, 0.08, 0.02]` (55.0; the half turn is the copy's, invisible on a washer) |
| 15 | potentiometer (+ its 3 straight leads) | tween 15c (no Transition) | rides on F1: `[0.91, 0, 0]` -> `[-65.83, 0, 0]` (66.74 out of F1's back, along the shaft); stays on screen |
| 16 | washer back on (F1 hidden) | appears hovering, tween 16c | rides on the pot (now 65.8 mm behind F1's seat): `t [50.94, 0.08, 0.02]` -> `[-2.64, 0.08, 0.02]` (53.57) |
| 17 | nut back on | same | `t [35.44, -0.28, -0.15]` -> `[-2.38, -0.28, -0.15]` (37.82) |
| 18 | knob back on | same | `t [39.63, 0, 0]` -> `[-3.0, 0, 0]` (42.63). So the potentiometer as supplied: washer -2.64, nut -2.38, knob -3.0 along the shaft from their seats (ours: guide.py `DELIVERED` nut and washer -3.0, knob +4.611, the CAD's "assembled" knob) |
| 19 - 22 | LCD wires GND, VCC, SDA, SCL | Transition: routed -> loose straight, then fade | lying-LCD routes NAUO83 / 85 / 87 / 92 fade out; loose straight wires (the CAD's NAUO69 / 68 / 67 / 66 with caps NAUO70 + 74 / 71 + 75 / 72 + 76 / 73 + 77) moved `[184.45, 0, 0]` / `[181.51, 0, 0]` / `[183.39, 0, 0]` / `[182.15, 0, 0]`: along z 1250 - 1320 at x 786 - 792, y 955.7 (in front of the case, 70 mm above the table), then fade |
| 23 | LCD | fade out, no motion | (lying, as 6c) |
| 24 | F9 | unhook ([064]) then lift ([065]) | 1) `turned([0, 0, -1], 25.79, [720.13, 887.42, 1355.78])` (tipped forward about its front foot's edge on F3's top: the build's 45c / 46c reversed); 2) `turned([0, 0, -1], 25.79, [720.13, 887.42, 1355.78], [-0.50, 32.98, 0.0])` (33.0 straight up, still tipped). Not "33 mm sideways": the second stage is a lift |
| 25 | USB cable: plug NAUO122, A end USB_A, cable NAUO123 together | tween [068] | from `[0, 0, 1.0]` (1 mm proud all guide long) to `[0.0, 0.0, 44.28]` (43.28 along +z) |
| 26 | F7A, F7B | tween 26c, stay | F7A `turned([0, 0, 1], 15.07, [656.58, 887.61, 1233.18])`; F7B `turned([0, 0, -1], 16.05, [693.18, 888.19, 1233.19])` (each about its outer bottom edge on F3's top: tops 18 / 19 mm out; the build's 42c) |
| 27 | buzzer + 2 leads | fade 27c | buzzer `turned([0.57735, 0.57735, -0.57735], 120.0, [675.26, 914.34, 1227.79], [-4.32, -11.90, 173.01])` (= `buzzer_lying`, behind and past the +z end); leads NAUO60 / NAUO63 (plugged, lying) |
| 28 | F7A, F7B | straighten ([075]) then lift ([076]) | 1) both back to `[0, 0, 0]`; 2) both `[0.0, 44.42, 0.0]` |
| 29, 30 | buzzer red, black | fade | plugged NAUO60 / NAUO63 out; straight 39 mm leads NAUO91 + cap NAUO89 / NAUO90 + cap NAUO88 in, as the CAD has them (no move) |
| 31 | buzzer + leads | fade out, no motion | |
| 32 - 34 | switch black, tan, red | fade | plugged (Part24 / 25 / 23) out; hanging 30 mm leads NAUO134 / 135 / 136 + caps NAUO131 / 132 / 133 in, as the CAD has them (under the flat F4) |
| 35 | switch + 3 hanging leads | isolated (F4 flat, switch, leads); tween 35c, stays | rides on F4 (flat, `[-117.83, 17.26, -0.06]`): `[0.14, 0, 0]` -> `[0.14, 85.09, 0]` (85.09 up, out of F4's top); leads and caps `[0, 85.09, 0]` with it |
| 36 - 41 | jumpers white, dark_red, purple, blue, green, black | Transition: routed -> loose straight wire, then fade | loose = the CAD's six-way ribbon wire (`wire-paths.json` lines "Part15 - 20^LAC Wire Cables", with its caps) moved along +x: white Part18 +165.36, dark_red Part16 +167.44, purple Part17 +163.99, blue Part19 +161.16, green Part20 +159.13, black Part15 +164.51: straight along z 1257 - 1331 at x 764 - 772, y 938 - 940 (in front of the case, 53 mm above the table; the build's hover poses). Both ends' caps go; the eye is on one |
| 42 | jumper orange | same | loose = NAUO139 (two-way ribbon, orange) + caps NAUO138 / NAUO142 moved `[175.53, 0, 16.58]` (cap NAUO142 `[175.53, 0, 15.83]`) |
| 43 | jumper yellow | same | loose = the LCD's loose yellow wire NAUO68 + caps NAUO71 / NAUO75, moved `[171.45, -25.32, 12.73]` (a body reused) |
| 44 | RTC NAUO3 + both coin cells | tween ([118], a pause frame) | `[0.0, 21.72, 0.0]` |
| 45 | RES1 (NAUO6) | tween [121] | `[0.0, 51.60, -0.17]` (from `[0, 0, -0.17]`: its 8 shown solids sit 0.17 mm off the CAD seat) |
| 46 | RES2 (NAUO7) | tween [124] | `[0.0, 50.68, -0.11]` (from `[0, 0, -0.11]`) |
| 47 | Nano | tween [127] | `[0.0, 54.97, 2.61]` (from `[0, 0, 2.61]`: the published Nano sits 2.61 mm +z of the CAD's seat all guide long) |

Durations: every frame 800 ms except the LCD's [016] and [017], 1600 ms. Transitions auto-advance except [033] (a dead pause in
Step 12) and [118] (the RTC lift waits for a click).

## 6. What shows when (copies and wire bodies)

- Start: the closed clock with the USB cable (plug and A end 1 mm proud), no F9 and five inner wire bodies (they come on at Step 1,
  unseen); the seated washer is shown at Start only (hidden from Step 1, while the potentiometer is still in F1).
- Steps 1 - 11: F1 seated to 4, pulled forward (F1-2, the CAD's NAUO35) at 4c - 5, laid flat face up beyond the -z end (F1-4, NAUO154)
  from 5c; its plugged leads change from Cadasio's own bodies (Part14 / 16 / 74 seated, Part8 / 9 / 10 pulled forward: not in our CAD,
  boxes in the JSON) to NAUO157 - 159 (laid flat). The LCD as in section 5, Step 6.
- Steps 12 - 18: only F1-4, the potentiometer, knob, nut, washer and the three straight leads (64 parts hidden). F1 hidden from 16.
- Steps 19 - 34: the main model again (base, breadboard, electronics, F7s, F9 to 24, buzzer, F4 flat with the switch, the LCD lying to
  23). Steps 32 - 34 under the flat F4 (its leads hanging).
- Step 35: only F4 (flat), the switch and its three hanging leads (32 parts hidden).
- Steps 36 - 47: base, breadboard, jumpers, RTC, resistors, Nano. Ends on F3 with the breadboard (and its backing paper hidden).

## 7. What could not be determined, and cautions

1. **Rolled views.** Steps 2 and 12 - 18 have the scene's up switched to -x. Our player keeps world +y up. For 12 - 18 the seated-frame
   cameras above are exact (the roll undoes the copy's own turn); for Step 2 there is no exact equivalent (a 119 deg roll; our `flip`
   is a 180 deg turn of the model only).
2. **Arrow anchors.** `object_local_positions` do not give the drawn arrow (40 - 110 mm off); their meaning is unknown. The `points` are
   what is drawn (checked on the pictures).
3. **Close-up pictures.** The two close-ups are pictures; their red boxes are inside the PNGs (not in the data, and the PNGs are not in
   this folder). Their leader targets are given, and our Full Build's 45c and 52c close-ups show the same spots.
4. **Wire shapes.** The payload has no meshes: a wire body's own shape is only its box. Where the wire body is one of our CAD's
   (`wire-paths.json` lines: NAUO numbers above), its centre line moved by the `from_cad` pose in the JSON is the published shape. Nine
   bodies are Cadasio's own and not in our CAD: Part14 / 16 / 74 (pot leads seated), Part8 / 9 / 10 (pot leads, F1 pulled forward),
   Part20 / 21 / 22 (switch leads seated), Part23 / 24 / 25 (switch leads, F4 flat): only their boxes are known.
5. **Coin cells.** Which of `CR2025-50003LC-1 / -2` is our NAUO4 (in the holder) and which NAUO5 (half out) was not settled; both stay
   with the RTC and leave with it.
6. **Cross-fades have no in-between.** F1's pull forward and laying flat, F4's lift and laying flat, the LCD's three poses, the buzzer
   to its lying place, every wire: the published guide fades between copies. A motion path for ours (`lift(... path=)`, `reappear=True`)
   is a choice, not data.
7. **Published slips to leave out:** the nut and washer missing on the pulled-forward and laid-flat F1 (4c - 11c, they reappear as
   loose copies at 12); the seated washer hidden from Step 1; the knob copy spun 41.8 deg about the shaft; the misnamed frames ([104]
   "Step 41" = Step 40, [120] "Step 45c" = Step 45, [002] "Transititon"); the duplicate frame [105]; the pause Transitions [033] and
   [118]; the resistors' 0.11 / 0.17 mm and the Nano's 2.61 mm offsets from their seats; F1-4 0.92 mm low; the LCD wires' and jumpers'
   loose shapes floating 53 - 70 mm above the table.
