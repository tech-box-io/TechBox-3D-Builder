# LSM round 2: what the published Cadasio guide does in the steps Lee points to (19 Oct 2026)

This report reads TechBox's published LSM Full Build (`docs/research/lsm/cadasio/raw/19075-laser_stem_matrix_lsm_-_full_build.json`)
for the steps Lee's notes of 19 Oct 2026 point to, so the numbers can go into `LSM Build Instructions/guide.py`. Everything is in
assembly millimetres with Y up. Cadasio's assembly uses the same frame as our `lsm.glb` (see `../cad_study.md`). Viewer indices `[NNN]`
are the step pictures `docs/research/lsm/cadasio/thumbs/19075-laser_stem_matrix_lsm_-_full_build/NNN.jpg`. Step names are Cadasio's.
Lee's step numbers are our first draft's numbers, which differ from Cadasio's.

## 0. How the payload was read (and two traps in the existing digest)

- mm = scene units / `scaleFactor` (0.47846455), so 1 unit = 2.0900 mm. Step `properties` are deltas, applied in `orderedSteps` order,
  hidden steps included. Viewer index = orderedSteps index - 1, because the one hidden step ("Step 51") comes first.
- Part moves are set on **solids**, and a solid's `position` / `rotation` are in its **parent component's local frame**. The digest
  (`19075-...md`) and `replay.json` print them raw, as if they were world offsets. That is only right for parts whose CAD frame is
  not rotated. For D10's pose copy `LSM_MatrixSupportSmall_r2-2` (frame = diag(1,-1,-1)), the digest's "Transition: MOVE [0,-21.7,-2.1]
  (down)" is really **up** 21.7 mm and +2.1 mm along Z. All world positions below come from composing every override through the
  parent chain (world = W_component x T(position) x R(rotation)) and transforming each solid's own box.
- Image leaders are anchored at `links[].data.target`, in the target solid's local frame. `data.position` is something else. This was
  checked by projecting the anchors through the step camera (vertical fov 45, 1400 x 678 picture): they land exactly on the stored
  leader `target_position` for [050], [051], [068] and [069] (for example, 30c: projected (42.3 %, 44.9 %), stored (42.29, 44.87)).
- Lead lines and arrows: `points` are world positions (scene units). Their `object_local_positions` do not follow the same rule and
  were not used.
- Image `position` is the box's top-left corner in % of the viewport, `width` is in % of the viewport width, and `height` is height
  / width. This was checked against the pictures for [068] and [012]. The exception is [075] / [076], whose stored positions do not
  match what the viewer shows (see section 4).
- Part opacity is the `opacity` key on a solid. It appears only 12 times in the whole guide, all of them in Steps 34, 34c and the
  Transition after 34c.
- Scripts used (temporary, outside the repo): `/private/tmp/claude-501/lsm_r2/replay2.py` (replay with world placements),
  `proj.py` / `backproj.py` (projection and back-projection through a step camera), `profile.py` (2D outline of a plate in `lsm.glb`).

## Cameras (eye and orbit target in mm; the target is the screen centre; dir = unit vector target -> eye)

| viewer | step | eye | orbit target | dist | dir (target -> eye) | elev / azim | screen up | screen right |
|---|---|---|---|---|---|---|---|---|
| [000] | Start | (789.59, 1037.37, 1477.41) | (524.55, 857.71, 1284.11) | 374.0 | (0.7086, 0.4804, 0.5168) | 28.7 / 53.9 | (-0.39, 0.88, -0.28) | (0.59, 0.00, -0.81) |
| [012] | Capacitor card | (697.73, 902.44, 1163.32) | (655.49, 902.44, 1163.32) | 42.2 | (1, 0, 0) | 0.0 / 90.0 | (0, 1, 0) | (0, 0, -1) |
| [027] | LED Matrix Diagram | (782.53, 944.56, 1097.63) | (622.04, 861.97, 1224.84) | 220.8 | (0.7268, 0.3740, -0.5761) | 22.0 / 128.4 | (no parts shown) | |
| [034]-[036] | Step 16 / Transition / 16c (nut off) | (571.70, 944.65, 1442.88) | (670.69, 844.83, 1361.74) | 162.3 | (-0.6098, 0.6150, 0.4999) | 38.0 / -50.7 | (0.48, 0.79, -0.39) | (0.63, 0.00, 0.77) |
| [037]-[038] | Step 17 / 17c (button through D2) | (527.38, 968.27, 1413.40) | (645.01, 859.24, 1312.82) | 189.3 | (-0.6213, 0.5759, 0.5313) | 35.2 / -49.5 | (0.44, 0.82, -0.37) | (0.65, 0.00, 0.76) |
| [039]-[040] | Step 18 / 18c (nut on) | (731.30, 946.98, 1171.16) | (630.34, 853.69, 1301.34) | 189.3 | (0.5333, 0.4928, -0.6876) | 29.5 / 142.2 | (-0.30, 0.87, 0.39) | (-0.79, 0.00, -0.61) |
| [050]-[051] | Step 23 / 23c | (633.05, 1153.73, 1239.84) | (641.28, 854.52, 1214.53) | 300.4 | (-0.0274, 0.9961, 0.0842) | 84.9 / -18.0 | (0.00, 0.08, -1.00) | (1.00, 0.03, 0.00) |
| [062]-[063] | Step 28 / 28c | (427.71, 991.45, 1038.91) | (641.46, 871.75, 1212.75) | 300.4 | (-0.7116, 0.3985, -0.5787) | 23.5 / -129.1 | (0.31, 0.92, 0.25) | (-0.63, 0.00, 0.78) |
| [064]-[066] | Step 29 / Transition / 29c | (425.80, 971.02, 1105.12) | (646.11, 890.36, 1211.38) | 257.5 | (-0.8554, 0.3132, -0.4126) | 18.3 / -115.7 | (0.28, 0.95, 0.14) | (-0.43, 0.00, 0.90) |
| [067]-[068] | Step 30 / 30c | (516.85, 976.16, 1411.30) | (641.53, 873.54, 1210.67) | 257.5 | (-0.4841, 0.3985, 0.7790) | 23.5 / -31.9 | (0.21, 0.92, -0.34) | (0.85, 0.00, 0.53) |
| [069]-[070] | Step 31 / 31c | (809.16, 1031.98, 1361.14) | (649.60, 897.59, 1210.11) | 257.5 | (0.6195, 0.5218, 0.5864) | 31.5 / 46.6 | (-0.38, 0.85, -0.36) | (0.69, 0.00, -0.73) |
| [071]-[072] | Step 32 / 32c | (805.28, 1018.08, 1434.33) | (640.98, 910.24, 1207.15) | 300.4 | (0.5469, 0.3590, 0.7563) | 21.0 / 35.9 | (-0.21, 0.93, -0.29) | (0.81, 0.00, -0.59) |
| [073]-[074] | Step 33 / 33c | (417.75, 1030.03, 1363.44) | (642.32, 910.90, 1203.41) | 300.4 | (-0.7476, 0.3966, 0.5328) | 23.4 / -54.5 | (0.32, 0.92, -0.23) | (0.58, 0.00, 0.81) |
| [075]-[076] | Step 34 / 34c | (741.73, 691.73, 1293.67) | (635.91, 908.10, 1202.48) | 257.5 | (0.4109, -0.8401, 0.3541) | -57.2 / 49.2 | (-0.64, -0.54, -0.55) | (-0.65, 0.00, 0.76) |
| [077] | Transition after 34c | (851.36, 1066.92, 1056.59) | (643.23, 899.20, 1193.66) | 300.4 | (0.6929, 0.5583, -0.4563) | 33.9 / 123.4 | | |
| [087] | Completed View | (791.38, 1061.87, 1358.70) | (619.56, 859.31, 1179.04) | 320.7 | (0.5358, 0.6317, 0.5603) | 39.2 / 43.7 | (-0.44, 0.78, -0.46) | (0.72, 0.00, -0.69) |

Field of view is 45 degrees (perspective) throughout. The camera stays fixed inside each Step N / Nc pair. The scene's `up_axis` is
changed for some steps: `-z` for 23 / 23c; `+x` for Steps 24 - 26c (the box turned over), set at the Transition [052]; `+y` again
from the Transition [059]; `-y` for 34 / 34c; and `+y` from [077].
This is how the top-down view of Step 23 gets -Z at the top of the screen, and how Step 34's view from below is shown turned over.

Our player always keeps world +Y as screen up (`player/js/core.js:265`, `cameraPose`). Two consequences:
- **Step 23.** With Cadasio's exact dir, our screen up would be the projection of +Y, which is rotated 18 degrees from -Z toward +X. To get
  -Z exactly at the top (D3 at the top, D2 at the bottom, D4 at the left), use dir (0, 0.996, 0.088): elevation 85 degrees, azimuth 0.
- **Step 34.** `flip=True` with `view_dir=(0.4109, -0.8401, 0.3541)` reproduces Cadasio's picture. The player turns the model 180
  degrees about the horizontal part of dir (`core.js:250`, `worldFor`). The resulting screen up in the model's frame is
  (-0.642, -0.547, -0.553), which is Cadasio's (-0.64, -0.54, -0.55).

## 1. Step 23 / 23c: the LED matrix moved over D4 (top-down view and one arrow)

**Camera.** Top-down, see the table: elevation 84.9 degrees, distance 300.4, target (641.28, 854.52, 1214.53), on the box's middle at
table level. On screen, +X is right and -Z is up (`up_axis -z`). D4 (-X) stands on the left, D2 and the button are at the bottom, and
the matrix starts on the right (+X).

**Arrow.** One arrow on Step 23 only (`A09536b1a...`): a straight red #ff0000 3D arrow.
- From (684.18, 862.01, 1128.54) to (581.32, 862.01, 1130.10), head at the second end: 102.9 mm along -X.
- It lies flat at the height of D1's top face (y 862.0). It sits 21 mm beyond D1's -Z edge (z 1150), so it is drawn above the model
  on screen, at 58.4 % -> 38.3 % across and 15.5 % down. It is not on the matrix.
- `normal` (0, 1, 0), facing up. `body_width` 3, `head_width` 9, `head_length` 10, in scene units (about 6 / 19 / 21 mm). On the
  picture it measures about 5 / 15 / 16 mm.
- It is anchored to D1 (`object_ids` both `LSM_Bottom_r1-1`).
- The ratio is 3 : 9 : 10. Our player draws arrows at 5 : 20 : 17 (`core.js:299`).

**Eye icons.** The image `ASS3e405c2c...png` is Cadasio's standard eye; it is used 21 times in this guide.
- Step 23: box at (77.17 %, 31.78 %), width 7.81 %. Leader anchor on the matrix (730.17, 876.04, 1215.57), which is its centre.
- Step 23c: box at (31.95 %, 25.78 %). Leader anchor on D4 at x 595.45, z 1211.62. That is D4's top edge where the wires cross.
  The anchor's y (845.5) is meaningless from this camera.

**The matrix does not travel.** The two poses are separate pose copies of the matrix, cross-faded in 800 ms
(`animation_hide/show: fade`). The wire bodies are cross-faded the same way. So nothing passes through D4 in Cadasio. Lee's Step 25
collision is a consequence of our straight `ride` (guide.py:473).

| | matrix copy | matrix box lo -> hi | centre | turn |
|---|---|---|---|---|
| Step 23 (beside, +X) | `8x8 LED-1` | (697.94, 868.96, 1185.14) -> (761.73, 877.54, 1245.56) | (729.84, 873.25, 1215.35) | LEDs up, half turn about Y from seated |
| Step 23c (outside D4, -X) | `8x8 LED-6` | (516.16, 896.50, 1198.87) -> (579.95, 905.09, 1259.29) | (548.06, 900.80, 1229.08) | same |

Our `P_BESIDE` and `P_OUTSIDE` (guide.py:184-185) already give exactly these centres. The outside pose floats with its underside at
y 896.5, level with D4's top (907.04), 14.5 mm outside D4's outer face (x 594.41).

**Wire bodies** (boxes from `cadasio_world_boxes.json`; the wires are not moved between steps):

| step | white | grey | purple | sockets (caps) |
|---|---|---|---|---|
| 23 | Part6: (646.48, 868.92, 1161.09) -> (760.66, 887.51, 1238.06) | Part5: (646.29, 866.33, 1162.26) -> (756.88, 887.00, 1238.06) | Part7: (626.34, 868.84, 1166.49) -> (758.78, 884.32, 1238.06) | Wire Cap-8/9/10: x 755.3-760.9, y 868.7-870.5, z 1233.19-1241.19 (under the matrix's corner) |
| 23c | Part31: (577.58, 876.33, 1166.93) -> (649.11, 908.96, 1251.78) | Part32: (573.67, 875.61, 1172.24) -> (649.52, 909.97, 1246.91) | Part33: (575.66, 876.31, 1210.42) -> (627.66, 908.57, 1246.91) | Wire Cap-17/18/19: x 573.5-579.1, y 896.2-898.0, z 1246.91-1254.91; wires leave them along -Z |

In 23c the white and grey wires sweep from i2 / i3 diagonally across the Nano toward D4, and the purple runs from b19 straight
along -X. All three cross D4's top edge together and then turn +Z to the sockets at the matrix's +X / +Z corner.
- From the picture, back-projected onto y 907, they cross at **z about 1211-1216** (±2 mm).
- The purple body's lowest z, 1210.42, bounds the crossing from below.
- They pass **over** D4's top (y 907.04), peaking at y 908.6-910.0.
- D4's slit is beside the crossing at z 1208.7-1209.9 (our mesh, `profile.py D4`; open from y about 892 to the top). Cadasio's wires
  do not sit down in it. Our `OVER_MIDS` (guide.py:468) press them into the slit at y 893-896.

## 2. Steps 28 - 30c: the matrix held over the box, D10 hooked on, the matrix lowered

**Poses.**
- Step 28c / 29 / 29c / 30: the matrix is held at `8x8 LED-5`, (606.72, 947.26, 1173.47) -> (670.51, 955.84, 1233.89). That is 56.86
  mm straight above its seated copy as shown at 30c (`8x8 LED-4`, (606.93, 890.40, 1173.99) -> (670.72, 898.98, 1234.40)). Our
  `P_HELD` (guide.py:186) matches.
- At 28c the stray backing sheet `Paper-1` reappears inside the box. This is a Cadasio slip; do not copy it.

**D10's L-shaped path.** D10 uses pose copy `-2`. Its 28c rotation (90 degrees about local X) gives the seated orientation. World
boxes:

| step | D10 box lo -> hi | offset from its final place on the held matrix |
|---|---|---|
| [064] Step 29 (appears, fades in) | (594.08, 918.45, 1239.95) -> (682.98, 936.00, 1242.95) | (0, -21.73, +37.87) |
| [065] Transition (auto, 800 ms) | (594.08, 940.18, 1242.01) -> (682.98, 957.74, 1245.01) | (0, 0, +39.93): up 21.73 and +2.06 along Z |
| [066] Step 29c | (594.08, 940.18, 1202.08) -> (682.98, 957.74, 1205.08) | 0: slid 39.93 along -Z |

D10 first appears below the matrix and beyond its +Z (D2) end. It rises at z 1242-1245, which is between the matrix's end (z 1233.9)
and the wires' turn (z about 1258). That is exactly where the wires run straight, so they go into D10's notch from below. D10 then
slides 39.9 mm along -Z to the middle, carrying the wires in the notch.
- Our `D10_UNDER = [0, -22, 40]` and `ride {D10: [[0, 0, 40], ZERO]}` (guide.py:496-500) already match this path.
- The Step 29 lead lines are two **3-point polylines** tracing the L:
  - (606.48, 932.83, 1241.82) -> (606.48, 954.62, 1241.82) -> (606.48, 954.62, 1203.61)
  - (670.60, 932.83, 1241.68) -> (670.60, 954.83, 1241.68) -> (670.60, 954.83, 1203.51)
  - Both run up 21.8 mm, then 38.2 mm along -Z, at the matrix's two X edges (606.7 / 670.5).
  - Our player's `setLeadLines` takes polylines (`core.js:293`).
- Steps 30 / 30c: matrix and D10 drop 56.9 / 57.1 mm straight down. At 30c the seated D10 copy `-1` is shown 0.66 mm +X of its CAD
  place (box 594.09-682.99), centring it between D4 and D5. It goes back to the CAD place by Step 38c. Ours (593.43-682.33) is the
  CAD place.

**Step 30 lead lines** (D10's end tabs to their slots):
- D4 end: (596.23, 948.21, 1203.47) -> (596.23, 890.96, 1203.47), 57.25 mm.
- D5 end: (681.15, 948.21, 1203.43) -> (681.15, 892.15, 1203.43), 56.06 mm.
- They **end at the bottoms of the slots**. In our mesh, D10's end tab spans y 891.2-900.7 (x 593.4-596.7). D4's slot for it is z
  1202.9-1205.4, open from the top down to y about 891.2.
- Our `D10_ENDS` (guide.py:509) puts the line end at y 885.1, 6 mm lower. This is Lee's Step 31 remark.

**D10's notch, where the wires pass** (our `lsm.glb`, outline looking along Z, `profile.py D10`):
- D4-end hook: x 593.4-604.7, rising to y 900.7.
- **Wire notch: x 604.7-612.2 (7.5 mm wide), bottom at y 889.2, open up to the matrix.** In Cadasio's held pose that is about
  x 605.3-612.9, y from 946.3.
- Middle bar: from x 612.2 on, top at y 895.0. Its slots for D9_A / D9_B (x 617.05-620.05 / 655.9-658.9) run up from D10's bottom
  edge (y 883.1) to y about 889.6.
- D10's engraving is on its -Z face (z 1203.23), on the D4-end hook (x 593.8-604.2, y 891.6-896.5).

**D9_A, the support nearest D4** (x 617.13-620.13; outline in the Z-Y plane):
- End tabs at y 891-900.7.
- Hooks at z 1153.5-1170.5 and 1237.5-1254.75 rise to y 900.7. The middle top is at y 895.2.
- Bottom edge: y 882.2 for z 1182-1228. It is **raised to y 886.2 at both ends** (z 1157-1182 and 1227-1250).
- Its engraving "D9" is on its **-X face (x 617.39), at its D3 end**: z 1158.7-1168.8, y 892.2-898.7.
- So "under the etched end of the D9 nearest the matrix" means under D9_A's raised D3 end. That is where the white and grey wires
  must cross to reach i2 / i3 (z 1170.45 / 1172.99, x 650.08).

**Wire bodies** (from `cadasio_world_boxes.json`):

| config | white | grey | purple | sockets |
|---|---|---|---|---|
| held (28c-30): Part28/29/30 | (600.71, 876.31, 1165.80) -> (649.14, 949.14, 1259.65) | (603.32, 875.61, 1172.22) -> (649.52, 949.27, 1259.96) | (604.75, 876.31, 1185.29) -> (627.66, 949.28, 1259.75) | Wire Cap-21/22/23: x 607.6-613.15, y 947.0-948.8, z 1177.84-1185.84; wires leave along +Z |
| seated (30c on): Part25/26/27 | (606.29, 876.35, 1166.89) -> (649.12, 892.47, 1211.44) | (610.09, 875.63, 1172.35) -> (649.52, 892.62, 1210.15) | (607.43, 876.31, 1186.36) -> (628.31, 892.29, 1219.94) | Wire Cap-14/15/16: x 606.41-611.96, y 890.13-891.88, z 1178.36-1186.36 |

**How the held wires run (28c - 30).** This was triangulated from the 28c and Step 30 pictures, two cameras 97 degrees apart, by
back-projecting points on the wires. Both views agree on the plane x about 609-610 for the turn, and the result fits the boxes above.
1. They leave the sockets at z 1185.8 along +Z and run straight under the matrix's -X edge, at x about 607-613, y about 946-950
   (the matrix's underside is at 947.3).
2. They continue **past the matrix's +Z end** (z 1233.9) for about 25 mm.
3. They turn down at **z about 1257-1260, y about 933-943, x about 609-610**. That is above D2's top edge (y 907; D2's inner face is
   at z 1251.9), and it sets the bodies' z max of 1259.65-1259.96.
4. They come back down toward -Z and enter the box **between D4's inner face (x 597.4) and D9_A (x 617.1)**, at x about 601-610.
   The grey and purple cross wall-top height (y about 904) at z about 1215-1225; the white, which separates from them, at z about
   1232-1240.
5. They go down to the floor (body y min 875.6-876.3) and on to i2 / i3. The purple stays on the D4 side (x <= 627.7) and goes to b19
   (627.04, 1213.63).

Reconstructed waypoints for white (grey and purple are 1.9 / 3.8 mm further +X at the sockets), ±3 mm:
(608.5, 947.9, 1185.8) start along +Z -> (608.5, 947.5, 1210) -> (608.5, 947, 1234) -> (609, 946, 1245) -> (609.5, 940, 1258)
-> (609.5, 932, 1259) -> (608, 922, 1250) -> (607, 914, 1240) -> (605, 906, 1232) -> into the box between D4 and D9_A -> floor
(y about 877-880) -> under D9_A's raised D3 end (y < 886) -> i2.

Our `HELD_MIDS` (guide.py:490) instead go straight up from the holes to the sockets.

**How the seated wires run (30c on).** The run is hidden in the main view and shown by the 30c inset.
1. From the sockets (z 1186.4) along +Z under the matrix's D4 edge (y about 890-892).
2. Through D10's notch (D10 at z 1202.97-1205.97).
3. Just past D10, z about 1207-1211 (body z max 1210.2-1211.4), down between D4 and D9_A (x about 606-612).
4. Then back under D10's lower edge (y 883.1) and under D9_A's raised D3 end to i2 / i3. Body y min is 875.6-876.4.
5. The purple drops just past D10 to b19, with z max 1219.9.

Our `SEATED_MIDS` (guide.py:505) currently climb to the socket from below at z 1192-1193, on the D3 side of D10.

**The 30c inset** (Image_5, `ASSf6e83899...png`, on Step 30c only; removed at Step 31):
- Box at (16.74 %, 28.21 %), width 16.78 % of the viewport, height 0.93 x width. Light-blue rectangle frame #7fdbff; Life Saver
  Circle anchor.
- Leader to **(606.94, 891.16, 1207.23)**, on the white wire 1.3 mm past D10's +Z face at the matrix's D4 edge. On screen that is
  (42.3 %, 44.9 %).
- It is a static rendered picture (Lee's picture 5, enlarged: `/private/tmp/claude-501/lsm_r2/i5.png`). It looks down past the
  matrix's D4 edge, with **the matrix drawn see-through** (ghosted inside the picture, not by opacity in the payload).
- It shows D4's inner face with D10's end tab in its slot, the three black sockets on the pins, and the white / purple / grey wires
  running from them under the matrix's edge and down through D10's notch, between the hook and the middle bar, beside the end of D9.
  The breadboard is below (resistor, column numbers).
- An eye icon inside the picture points at the wires in the notch.

## 3. Step 31: D6, and the inset with four red boxes

- D6 (`LSM_Lens_Bottom-3`) hovers 64.3 mm up: (596.96, 965.24, 1156.68) -> (679.51, 968.24, 1251.93).
- Four vertical lead lines are drawn at D6's corner slots:
  - (673.91, 969.51, 1242.26) -> (673.91, 906.45, 1242.26)
  - (604.06, 968.79, 1243.36) -> (604.06, 906.46, 1243.36)
  - (604.06, 968.73, 1166.79) -> (604.06, 900.95, 1166.79)
  - (673.91, 970.19, 1166.26) -> (673.91, 900.10, 1166.26)
- Camera: from the D5 / D2 corner, see the table.

**Inset** (Image_32, `ASS53e07d40...png`, on **Step 31**, not 31c; removed at 31c):
- Box at (65.92 %, 14.04 %), width 22.15 %, height 1.01 x width. Light-blue rectangle frame.
- Leader to the matrix's middle, **(643.98, 898.12, 1204.62)**; on screen (50.0 %, 47.9 %).
- It is a static picture (enlarged: `/private/tmp/claude-501/lsm_r2/i6.png`) of the box as Step 31 leaves it, **seen from straight
  above, in perspective** (all four walls' inner faces visible).
- D3 is at the top, D2 (the button's nut) at the bottom, D4 (the USB cable) on the left: screen up -Z, screen right +X, the same
  orientation as Step 23.
- Shown: the LED matrix, the two D9 bars along Z, D10 across the middle, the breadboard's ends (rows a-j, columns 1 and 29-30), the
  walls and D1. D6 is not in it, and no lead lines.
- **Four red boxes**, drawn in the picture, frame D1's four corner slots for the D11 tabs, which show white through D1. In our mesh
  (`profile.py D1`) these slots are about x 599.8-602.8 and 673.8-676.8, by z 1161-1171 and 1237-1248, each 3 x 10 mm.

## 4. Steps 32 - 34c: the four D11 posts, two short, then all home with D1 and D5 see-through

| step | what moves | box(es) | camera |
|---|---|---|---|
| [071] Step 32 | D11_A (`r2-2`) and D11_B (`r2-3`), the D5 side, appear 88.6 mm up | x 673.33-676.33, y 944.66-1024.39, z 1234.46-1250.34 and 1158.26-1174.14 | from D5 / D2 corner (dir (0.5469, 0.3590, 0.7563)) |
| [072] Step 32c | both down 81.65 mm, **to 7.0 mm above seated** | y 863.00-942.74. The bottom of each tab is 0.6 mm above D1's top face (862.4), at the top of its slot. | same |
| [073] Step 33 | D11_C (`r2-1`) and D11_D (`r2-4`), the D4 side, appear 90.1 / 84.4 mm up | x 600.13-603.13 | **from D4 / D2 corner** (dir (-0.7476, 0.3966, 0.5328)) |
| [074] Step 33c | both down to **+7.0 mm** | y 862.03-941.77 / 862.43-942.17 | same |
| [075] Step 34 | nothing moves; view from below; D1 and D5 at **opacity 0.5** | | dir (0.4109, -0.8401, 0.3541), up (-0.64, -0.54, -0.55) |
| [076] Step 34c | all four D11 down **7.0 mm** together to seated (y 856.02-935.76: the tab comes 3.4 mm out of D1's underside, 859.4); D1 and D5 back to **opacity 1** | | same |

- Each pair's two lead lines run from the post's bottom to D6. Step 32 lines: (675.07, 944.60, 1166.79) -> (675.46, 900.55, 1166.47)
  and (675.52, 945.15, 1242.99) -> (675.00, 901.50, 1242.99). Step 33: (602.24, 946.03, 1242.24) -> (602.19, 903.19, 1242.34) and
  (601.77, 940.25, 1166.01) -> (601.72, 903.69, 1166.10).
- **Engravings on D11** (our mesh): D11_A and D11_B on their +X faces (x 676.08), D11_C and D11_D on their -X faces (x 600.39), at
  y 905-910. That is why Cadasio turns the camera between Steps 32 and 33: from the D5 side for the first pair, the D4 side for the
  second.

**Opacity, exactly** (the only uses of `opacity` in the guide):
- Step 34: 0.5 on `LSM_Bottom_r1-1` (D1, set at the component and on its plate solid `Cut-Extrude1`) and on `LSM_Side4_r2-1` (D5:
  plate `Cut-Extrude1` and its two engraving inlays `Surface-Offset1[1]`, `[2]`).
- Step 34c: 1.0 on both plates (D1 `Cut-Extrude1`, D5 `Cut-Extrude1`), so both look opaque again.
- The Transition after 34c ([077]): D1's component-level value and D5's two inlays are reset to 1.0.
- Nothing else in the guide is ever see-through. (The see-through matrix in the 30c inset is inside the picture.)

**Step 34 annotations:**
- Four short vertical lead lines, 16.6-17.5 mm, from each post down through its D1 slot to just below D1:
  - (675.29, 874.75, 1166.41) -> (675.29, 857.98, 1166.46)
  - (675.38, 874.99, 1242.30) -> (675.38, 857.50, 1242.34)
  - (602.31, 874.95, 1167.11) -> (602.31, 858.36, 1167.11)
  - (601.94, 874.97, 1243.33) -> (601.94, 858.41, 1243.33)
- One eye (Image_2) with its leader to D11_B's tab tip, **(675.72, 863.39, 1166.50)** at the D5 / D3 corner; on screen
  (35.6 %, 39.6 %).
- The payload stores the eye at (92.22 %, 71.35 %), with leader target (75.14 %, 69.03 %). The viewer and the step picture show it on
  the **left**, at about (20-28 %, 29-37 %). The stored 2D positions for 34 / 34c are stale; the 3D anchors are right.

**Step 34c inset** (Image_11, `ASS3a1ae4d5...png`):
- Stored at (87.11 %, 45.82 %), width 14.22 %, height 1.01 x width. **Shown at the lower left**, about x 19-33 %, y 47-77 % of the
  step picture (Lee's picture 8).
- Leader to D11_B's tab, **(675.85, 856.41, 1167.30)**, through D1; on screen (35.3 %, 37.4 %).
- It is a very close, static picture from the same underside direction (enlarged: `/private/tmp/claude-501/lsm_r2/i8.png`). Two tab
  ends stick out of D1's underside: a wall's foot tab, and the D11 tab with its chamfered end. An eye inside the picture points at the
  D11 tab's tip. The USB cable is behind.

## 5. The Capacitor card [012], and the nut steps' motion

**Capacitor card** (a pause step before Step 6):
- Everything is hidden except the capacitor, which is raised **29.05 mm** (box (651.33, 892.67, 1169.11) -> (656.47, 912.72,
  1174.21); seated (650.29, 863.62, 1169.11) -> (656.42, 883.91, 1174.21)). Its 6 degree CAD lean is taken out: solid rotations
  (0.0523, 0, 0, 0.9986), and the stripe solid `Surface-Offset2` turned to face the camera.
- Camera: horizontal, from +X, 42.2 mm from the target (655.49, 902.44, 1163.32), screen right = -Z. The capacitor stands left of
  centre with its **grey stripe on its +Z (j3) side**, facing the camera.
- Photo inset (Image_37, `ASSc50c33f2...png`):
  - Top-left at **(49.89 %, 18.87 %)**, width **30.32 %**, height **1.09 x width**, so it reaches about 90 % down.
  - Light-blue rectangle #7fdbff frame; Life Saver Circle anchor; light-blue leader, thickness 5.
  - Leader to the stripe at **(656.33, 907.24, 1172.35)**; stored target (35.49 %, 36.03 %).
  - Content (Lee's picture 2): a photo of a real electrolytic capacitor, a dark "GND Strip" callout with an arrow to the stripe, and the
    legs marked GND (black minus disc) and VCC (red plus disc).

**Nut off: [034] Step 16, [035] Transition (play, 1600 ms, twice the usual 800), [036] Step 16c.**
- The button is the pose copy `Push button-2`, in the floating copy of D2 (`LSM_Side3_r2-2`, z 1309.04-1312.17, 57.11 mm out from
  the seated D2).
- Its axis is at (638.86, 881.05), along Z, head at +Z. The component's frame is the world frame to 0.004.
- [034]: the button is shown 102.54 mm out along +Z (body z 1393.38-1418.28). The nut is at its head end, z 1413.18-1414.68. The
  arrow (`body_width` 5, `head_width` 20, `head_length` 15) runs from **(627.91, 880.96, 1414.68) to (627.34, 881.09, 1345.95)**:
  68.7 mm along -Z, beside the button 11 mm off its axis, from the nut toward the pins. `normal` (-0.987, 0.159, 0) faces the camera.
- [035]: the nut slides **100.64 mm along -Z** (to z 1312.53-1314.03, past the pins' ends) and **turns 179.62 degrees** about the
  button axis. The quaternion is (0, 0, -0.99999, -0.00328) from identity, so the short way is +179.6 degrees about +Z. That is
  counter-clockwise seen from the head side, clockwise seen from the pin end.
- A half turn is the most one tween can show. With a right-hand thread this is, by 0.4 degrees, the screw-on sense, so its
  direction is effectively undefined. The arrow is removed at [035].
- [036]: the nut is hidden.

**Nut on: [039] Step 18, [040] Step 18c.**
- At [038] (17c, hidden) the nut's rotation is reset to identity.
- [039]: it appears 83.07 mm **behind** its seat on the -Z (inner) side, z 1223.35-1224.85, on the axis. The lead line runs
  **(638.86, 881.05, 1315.74) -> (638.84, 881.04, 1223.35)**, 92.4 mm along the axis, from the button body to the nut.
- [040]: the nut moves **+83.07 mm along +Z** to its seat (z 1306.42-1307.92, 1.1 mm off D2's inner face) while turning **115.06
  degrees**. The quaternion is (0, 0, -0.8437, -0.5368); the short way is +115.1 degrees about +Z, the screw-on sense for a
  right-hand thread.
- Camera from inside the box side (azimuth 142 degrees).

The rotation centre is the solid's local origin, which lies on the button axis (component origin (638.86, 881.05, 1315.74)), so the
nut spins in place. Cadasio cannot show more than half a turn per tween. Lee's "1-2 rotations" would need several stops (or a
spin parameter) in our player.

**LED Matrix Diagram [027]:**
- No parts are visible. One static picture (Image_19, `ASSe2452335...png`) at (14.44 %, 2.84 %), width 65.23 %, height 0.61 x width.
- It shows the back of the matrix as a black square with its mounting holes. The two 3-pin headers at opposite corners are framed by
  red boxes: top right, the input; bottom left, labelled "V- Out V+".
- Two eye icons point at them. The red boxes and eyes are in the picture.

## 6. Start [000] and Completed View [087], compared with our title page

| | dir (target -> eye) | elev / azim | eye -> target | target |
|---|---|---|---|---|
| Cadasio Start | (0.7086, 0.4804, 0.5168) | 28.7 / 53.9 | 374.0 | (524.55, 857.71, 1284.11), well off the model so that the model sits right of the title |
| Cadasio Completed View | (0.5358, 0.6317, 0.5603) | 39.2 / 43.7 | 320.7 | (619.56, 859.31, 1179.04) |
| ours, Start = Completed View (steps.json) | (0.5997, 0.5299, 0.5997) | 32.0 / 45.0 | 322.0 in a 2 : 1 window (114.1 / sin 22.5 x 1.08) | (602.9, 912.5, 1204.3), our model's box centre; pulled 35 mm toward -X by the USB A end lying at x 520-570 |

Where the model lands, projecting the same points of our model (box corners and stem tops) through each camera into a 1400 x 678
frame:

| | box + stems on screen | height of frame | vertical middle |
|---|---|---|---|
| Cadasio Start | x 60.7-88.2 %, y 13.5-74.1 % (the step picture: 49.6-88.6 % with the cable, 14.5-73.7 %) | 60.7 % | **43.8 %** |
| Cadasio Completed View | x 33.6-64.0 %, y 7.2-82.6 % (picture: stems top at 8 %, feet at 82 %) | 75.3 % | **44.9 %** |
| ours (title page's own shift ignored) | x 41.4-67.8 %, y 27.5-93.4 % | 65.9 % | **60.4 %** |

So ours sits about 15 % of the frame lower than Cadasio's ("a little low") and fills 66 % of the height against 75 % in Cadasio's
Completed View ("could be zoomed in"). The cause is our target: the box centre is dragged toward -X and downward by the USB A end
lying on the table. Seen from +X / +Z at 32 degrees, a target behind the model's middle puts the model low.

Cadasio's Completed View, re-expressed for our player: any point on its line of sight can serve as the target, for example
**(650.5, 895.8, 1211.4)** with dir **(0.5358, 0.6317, 0.5603)**, distance 262.9. That is radius about **93.2** under our formula
(dist = radius / sin 22.5 x 1.08, wide window).

## Reuse notes (what maps onto our tools)

- **Step 23 / 25 (ours).** Cadasio never animates the matrix across D4: it cross-fades the two poses under a top-down camera, with one
  flat arrow beside the model pointing -X. Its camera for us: dir (0, 0.996, 0.088), target (641.3, 854.5, 1214.5), distance 300.
  Arrow: tail (684.2, 862.0, 1128.5), head (581.3, 862.0, 1130.1), normal (0, 1, 0).
- **Steps 28-30 (ours).** The held wires should run along +Z under the matrix, about 25 mm past its +Z end (turn at z about 1258,
  y about 935-945), then down into the box between D4 and D9_A at z about 1215-1240. D10 then rises at z 1242-1245 and takes them
  into its notch (x 604.7-612.2, bottom y 889.2 seated, 946.3 held).
- **Step 31 lines (ours).** End them at the slot bottoms, y about 891 at D4 and 892 at D5, not at D10's bottom edge.
- **Step 30c-style inset (ours).** On Step Nc, a see-through-matrix close-up at the D4 edge. Anchor (606.94, 891.16, 1207.23), box
  about 17 % wide at the left.
- **Step 31 / 32 (ours).** The D1-slot picture is a top-down view (screen up -Z) with the four corner slots framed in red. Cadasio puts
  it on Step N, not Nc. Our `inset=` is documented as an Nc close-up (CLAUDE.md), so moving it to Step N needs the player to allow
  it, or it can go on Nc.
- **D11s.** Two posts per step, each pair going down to +7.0 mm (tab bottom at the top of D1's slot, y 863.0). Then a view from
  below (`flip=True`, view_dir (0.4109, -0.8401, 0.3541)) with D1 and D5 at 50 % and four 17 mm lead lines through the slots. On Nc,
  all four go down the last 7.0 mm together, D1 and D5 return to opaque, and a close-up of D11_B's tab, anchored at
  (675.85, 856.41, 1167.30), is shown. Cameras: D5-side pair from (0.5469, 0.3590, 0.7563), D4-side pair from
  (-0.7476, 0.3966, 0.5328).
- **Nut.** Off: 100.6 mm along -Z with a 179.6 degree turn in 1600 ms. On: 83.1 mm along +Z with a 115.1 degree turn. Both turn about
  the button axis (638.9, 881.1) along Z. Neither shows a full turn.
- **Capacitor card.** Capacitor alone, upright, raised 29 mm, seen side-on from +X at 42 mm, stripe toward the camera on the +Z side.
  Photo inset at (49.9 %, 18.9 %), 30.3 % wide, 1.09 tall, anchored on the stripe at (656.33, 907.24, 1172.35).
