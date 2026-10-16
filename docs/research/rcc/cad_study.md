# RCC: what the CAD says (rcc.glb)

Source: `RCC Build Instructions/rcc.glb` only (converted from `RCC_Assembly_v1.STEP`: 42 top-level instances NAUO1..NAUO42, 154 mesh
nodes). Coordinates are millimetres in assembly space (the GLB's metres x 1000), Y up, parts as assembled, loaded as `tools/stepgen.py`'s
`Model` loads them (top-level instance = child of the root node `RCC_Assembly_v1`; for connector work each mesh node was kept separately).
Every number below is in `cad_study.json`. Collision and free-direction tests use stepgen's own `blocked()`; the wood joints were measured
on 0.1 mm rasters of each 3 mm plate (each L part is an exact extrusion, so "inside the plate" is exact). Scripts ran from the scratchpad;
nothing in the kit folder was changed.

Status: complete (sections 0 - 5).

## 0. Summary

1. **The assembly holds the car and the hand controller side by side**, both right way up: the car centred on z = 1338.5, the controller on
   z = 1121. The car's ground is y = 876.9 (bottom of both wheels; L2 and L3 reach 877.0 - 877.1 and act as the rear skid).
2. **The car's front is +X**, the flat slotted end of L1 (x = 774.5), where the wheels are; the round end (x = 602.5) carries the battery and the
   skid. Lee's drawing ("FRONT" at the flat end) and the CAD's own names agree: the servo lead called "Left" belongs to the motor on -Z, the
   car's left when facing +X. **Car's left = -Z, right = +Z.**
3. **No mesh carries a colour** (every node has the converter's default `#97a3da`): all colours must come from a colour atlas of TechBox's
   Cadasio project and from `materials.json` rules.
4. **Duplicates for posing:** the two servo leads each come in two poses (loose straight lead with loose plug NAUO31-38 + NAUO21/22; routed
   lead plugged on the adapter NAUO39/40 + NAUO19/20); the battery lead in two (unplugged NAUO42 + plug NAUO28; plugged NAUO41 + plug NAUO29).
   Nothing else is duplicated: the second radio, joystick, servo and wheel are real second parts.
5. **NAUO9's 78.4 mm box is an artefact**: the wheel is 60 x 60 x 8 like NAUO8. It is the same part turned 180 degrees to face -Z and spun
   22.5 degrees about the axle; the box of a 60 mm square box spun 22.5 degrees is 60 x (cos 22.5 + sin 22.5) = 78.4. Wheels and servos are
   identical parts turned, not mirror images.
6. **All seven wood parts are engraved in the CAD, and every code matches its CAD name** (L1 - L7, 0.254 mm deep, 6.35 mm letters). L1's
   "L1" is already in the top-right corner of Lee's drawing (within 1 mm) but **upside down** relative to it; "FRONT" does not exist yet.
7. **The car's Nano is inside NAUO23**, as on the MRA: node `NAUO86` (`own_parts` in `materials.json`). The shield is the MRA's I/O
   module, turned 90 degrees about Y, so the MRA's row names and silkscreen positions carry over through a fixed mapping (section 3.1).
8. **Build order the geometry forces** (section 2.3): L1 datum; L2 (hook-and-swing) and L3 from underneath; L5 + both servos + L4 on the bench;
   that block down into L1; battery down into its cradle; **the shield slides in from the front** (-X) into grooves in L4 / L5 up to L2's fin;
   L7 and L6 slide in from the front and lock it; adapter, radio, servo plugs, battery snap and barrel plug on top.
9. **CAD problems** (section 4): the joystick PCB overlaps the controller board by 4.2 mm; the joystick's underside sits 2.8 mm into the guard; the
   controller guard is two pieces in the CAD but four in Lee's photo; the servo leads' two poses have different lengths (71 mm loose, 110 / 165 mm
   routed); the battery lead is only about 30 mm long; there is no USB A end and no car USB cable (a cable cannot reach the car's Nano while the
   battery is in); the shield's reset button clips L4 / L5 by 0.3 mm on the way in; the adapter's sockets sit up to 0.45 mm (one 0.9 mm) off the
   shield's pins; no screws anywhere.

## 1. The 42 instances

"Sits" gives the part's own axes in assembly space. Sizes are true mesh boxes (mm).

### 1.1 Car

| id | part | size (x, y, z) | how it sits | role |
|---|---|---|---|---|
| NAUO1 | **L1** | 172.0 x 3.0 x 130.0 | flat, top face +Y at y 909.23; round end -X, flat end +X | the deck, datum |
| NAUO2 | **L2** | 162.0 x 44.7 x 3.0 | upright in the centre plane z 1337.0-1340.0, mostly under L1 | keel and rear skid; battery seat; hooks over L1's front notch |
| NAUO3 | **L3** | 3.0 x 35.6 x 64.9 | upright across the car at x 640.2-643.2, under L1 | U-shaped battery cradle and second skid |
| NAUO4 | **L4** | 3.0 x 30.2 x 130.0 | upright across the car at x 713.1-716.1, through L1 | rear wall of the motor bay |
| NAUO5 | **L5** | 3.0 x 30.2 x 130.0 | upright across the car at x 739.5-742.5, through L1 | front wall of the motor bay |
| NAUO6 | **L6** | 64.7 x 28.6 x 3.0 | upright along the car at z 1352.5-1355.5 (right of centre), front | front clip, right |
| NAUO7 | **L7** | 64.7 x 28.6 x 3.0 | upright along the car at z 1321.5-1324.5 (left of centre), front | front clip, left |
| NAUO8 | wheel (rim + tyre) | 60 x 60 x 8 | axle along Z at (722.6, 906.9), z 1405.2-1413.2 | right wheel |
| NAUO9 | wheel | 60 x 60 x 8 | same axle, z 1263.6-1271.6 | left wheel (NAUO8 turned, see 0.5) |
| NAUO17 | FS90R servo | 32.3 x 12.2 x 29.7 | lying on its side, shaft +Z into NAUO8, ears in L4 / L5 | right motor |
| NAUO18 | FS90R servo | same | NAUO17 turned 180 degrees about X, shaft -Z | left motor |
| NAUO14 | 9 V battery | 17.1 x 47.9 x 26.0 | standing, through L1's 18.0 x 27.4 hole, in L3's U, bottom on L2 at y 892.2 | power |
| NAUO15 | 9 V snap ("DC_Adaptor") | 12.0 x 7.2 x 28.0 | on the battery top (overlaps its terminals 1.0 mm) | |
| NAUO23 | Nano I/O shield + car Nano (NAUO86 inside) | 59.0 x 24.6 x 53.3 | board flat at y 916.89-918.54, x 691.1-748.3, z 1311.8-1365.2; USB end -X | controller board of the car |
| NAUO26 | adapter board ("L") | 57.4 x 18.8 x 33.8 | board flat at y 928.58-930.18 on top of the shield | U1 / U2 servo headers, U3 radio socket |
| NAUO10 | nRF24L01 radio | 29.0 x 12.8 x 15.3 | flat, pins down in U3, board reaching forward to x 772.6 | car radio |
| NAUO19 / 20 | 3-way servo plug housings | 2.6 x 14.0 x 7.6 | upright on U2 / U1 | pose 2 (plugged) |
| NAUO21 / 22 | same housings | 14.0 x 7.6 x 2.6 | lying, mating face -X, beside the rear at x 638-652 | pose 1 (loose) |
| NAUO28 / 29 | barrel plug of the battery lead | 39.5 x 8.6 x 8.6 | axis along X at (y 925.04, z 1354.06) | unplugged / plugged |
| NAUO31-38 | servo leads, pose 1 | | straight back (-X) from each servo, 3-wire ribbon then separated ends | loose |
| NAUO39 / 40 | servo leads, pose 2 | | looping up to y 982 / 971 and down onto U2 / U1 | routed |
| NAUO41 / 42 | battery lead (2 conductors) | | snap top to plug back | plugged / unplugged |

### 1.2 Controller

| id | part | how it sits | role |
|---|---|---|---|
| NAUO30 | controller PCB | flat, top face y 918.54 (modelled 2.64 mm thick, 915.9-918.54), x 657.5-744.5, z 1046.2-1195.9 (long axis Z) | carries H1 / H2, L-JS / R-JS, radio socket, C1 |
| NAUO24 / 25 | guard, left / right half | 7 mm frames (y 913.36-920.34) round the board's outline, meeting at z 1120.3 / 1121.8 | handles / bumper |
| NAUO12 / 13 | KY-023 joysticks | PCB level with the board in its 31.6 x 29.0 cut-outs; header pins +X into the sockets | L-JS (z 1072-1099) / R-JS (z 1144-1172) |
| NAUO27 | Arduino Nano (one mesh) | pins down in H2 / H1, USB end -X | controller's Nano |
| NAUO11 | nRF24L01 | flat, pins in the 2x4 socket, board toward +X | controller radio |
| NAUO16 | Mini-B plug with 54 mm of cable | in the Nano's USB socket, tip 5.5 mm in | USB, controller only |

Lee's controller photo is a true top view (not mirrored): photo-up = +X, photo-right = +Z, so L-JS = NAUO49 socket (low z) and H2 = NAUO45 (z
1105.29), H1 = NAUO46 (z 1120.53), "USB" printed at the -X end. Lee's adapter photo is a top view too: photo-up = -X, photo-right = -Z.

### 1.3 Duplicates, poses and mirror images (rigid fits on matching vertices, error 0.000 mm)

| pair | relation |
|---|---|
| NAUO8 -> NAUO9 (wheels) | 180 degrees about (0.195, -0.981, 0): flipped about Y and spun 22.5 degrees about the axle. Proper rotation, **not a mirror** |
| NAUO17 -> NAUO18 (servos) | 180 degrees about X. Identical motors; their lead exits swap top / bottom accordingly |
| NAUO10 -> NAUO11 (radios), NAUO12 -> NAUO13 (joysticks) | pure translations |
| NAUO19 -> NAUO20 | translation -12.7 X (U2 to U1); NAUO21 / 22: 180 degrees about X of each other |
| NAUO28 -> NAUO29 | translation +8.95 X only: unplugged -> plugged |
| NAUO24 / 25 (guards) | different meshes, a mirror pair |
| L6 / L7 | nearly the same outline (2.6% of the area differs), mirror-placed |

Pose sets (show one at a time): right servo lead `NAUO31-34 + NAUO21` (loose) or `NAUO39 + NAUO19` (on U2); left `NAUO35-38 + NAUO22` or
`NAUO40 + NAUO20` (on U1); battery lead `NAUO42 + NAUO28` (unplugged) or `NAUO41 + NAUO29` (plugged). For our player the leads are routes, not CAD
parts (`"omit": true`, centre lines in `wire-paths.json`), and only one housing per lead is needed (`g.carry()` while loose).

## 2. The wood: L1 - L7

### 2.1 Outlines, slots, tabs (closed slots measured to the vertex)

- **L1** (deck): Lee's drawing to scale (4.586 px/mm both ways); every feature matches. Mirror-symmetric about the centre line z = 1338.48
  (to 20 mm2 of 16,900), so the outline alone cannot tell which face the drawing shows. Closed slots: L2 rear tab x 612.54-622.47 and L2 long tab
  x 660.88-690.47 (both 2.91 wide on the centre line: **0.09 mm narrower than the 3.0 mm wood**); L3 tabs z 1309.31-1317.12 and 1359.84-1367.65
  at x 640.17-643.17 (7.81 long); L4 slot x 713.12-716.12 and L5 slot x 739.47-742.47, both z 1308.73-1368.23 (59.5 long); battery hole x
  632.67-650.67, z 1324.77-1352.19 (18.0 x 27.4; battery 17.1 x 26.0). Open notches at the flat end: L2 (centre, to x 767.12), L6 / L7 (z
  1352.5-1355.5 / 1321.5-1324.5, to x 761.62). Side notches for the servos (x 713-742.5), with 3 mm notches for the servo ears (z 1277.2-1279.8 and
  1397.2-1399.7) and 10 mm notches for the leads (z 1288.8-1293.8 and 1383.2-1388.2, x 703.2-713.1).
- **L2** (keel): main body under L1 (top edge y 906.3 = L1's underside), rounded bottom reaching y 877.1 at x 641 (the skid). Up through L1: a
  3 mm tab x 612.5-622.5 (flush with L1's top), a fin x 661-690.5 rising to y 921.7 (it also stops the shield's back edge), and at the front a
  **barbed hook**: through L1's notch (x 767-774.5) up to y 914.3, overhanging back over L1 to x 762 with a ramped underside (y 909.3 at x 766.5,
  0.1 mm above L1; y 910.5 at x 762). Notches: battery seat x 633-651 (floor y 892.2, open up), L3 notch x 640.5-643.5 (open down, y 877-884.4),
  L4 / L5 notches x 713-716.4 and 739.5-742.5 (open up, floor y 898.9).
- **L3** (cradle): U shape, floor y 892.2 between z 1325 and 1352; two split snap tabs (a slit forms two prongs, barbs on top) up through L1 to y
  912.6; centre notch z 1337-1340 open up to y 884.6 (onto L2).
- **L4 / L5** (motor-bay walls): a 59.5 mm centre tab through L1's slot; notches open downward (z 1296.7-1308.7 and 1368.2-1380.2, top at y 909.2)
  that sit on L1's top face; the outer ends hang into L1's servo notches. Bottom notch z 1337.0-1340.0 (open down to y 898.7) onto L2. Holes:
  servo ears z 1277.23-1279.78 and 1397.18-1399.73 at y 900.81-912.91 (12.1 x 2.55), L6 / L7 slots (L4: 7.94 x 3.0 at y 897.1-905.04, the snap
  tab only; L5: 10.32 x 3.0 at y 895.91-906.23, the whole clip), and in L4 only the servo-lead holes z 1288.78-1293.78 and 1383.18-1388.18 at y
  902.36-911.36 (9.0 x 5.0). **Shield grooves:** at z 1311.6-1313.7 and 1363.3-1365.4 a horizontal slot y 916.9-918.4 (1.5 mm; the shield board
  is 1.65 mm) under a lip up to y 921.6.
- **L6 / L7** (front clips): a C shape. Body under L1 (y 893.1-906.2), head above L1 (y 909.2-921.7, x 750-774.5), joined through L1's front
  notch; split snap tab at the tip (x 709.7-716) through L4; a stop below the body (x 743-752, down to y 893.1) that bears on L5's front face.

### 2.2 Which tab goes where (crossing analysis, both parts' material along their common line)

| joint | what goes in what | fit |
|---|---|---|
| L2 -> L1 | L2's two tabs up through L1's closed slots; L2's hook through L1's front notch and back over L1's top | slots 2.91 vs 3.0 (press); hook 0.1 mm clear of L1; L2 overlaps the notch end by 0.3 mm |
| L3 -> L1, L2 | L3's two snap tabs up through L1's slots; L3's top notch onto L2's bottom notch (L3 below y 884.6, L2 above) | tabs 0.13 mm wider than the slots (snap) |
| servo -> L4, L5 | each servo's ears through the 12.1 x 2.55 holes in both walls; body 22.5 long between the walls' faces 23.35 apart; ear tips 1.5 mm proud into L1's ear notches | ears 0.1 mm snug |
| L4, L5 -> L1, L2 | centre tab down through L1's slot; downward notches onto L1's top; bottom notch onto L2's top notch (L4 / L5 above y 898.7) | exact |
| L6, L7 -> L5, L4, L1 | the clip slides -X: body through L5's slot, snap tab through L4's slot, L1's edge in the C, head through L1's front notch; stop against L5 | tabs about 0.1 mm snug |
| shield -> L4, L5 | board edges in the two grooves of each wall; back edge 0.65 mm short of L2's fin; front edge against the L6 / L7 heads | 0.12 mm press |
| battery -> L1, L2, L3 | through L1's hole, in L3's U, on L2's notch floor | 0.45 / 0.7 mm clear |
| wheels -> servos | pressed on the spline (right 0.2 mm overlap, left touching) | press |

### 2.3 How each part can go in (stepgen `blocked()`; "free" = the side the part hovers on)

| step (stationary = what is already built) | free directions | note |
|---|---|---|
| L2 into L1 | none | **hook-and-swing** (rulebook 4): tested path, from seated: turn rear-down 20-25 degrees about Z through (765.0, 911.5, 1338.5), then +X 6 mm (free from there). Build: arrive tilted, slide -X 6 mm to hook over L1's notch end, swing up |
| L3 into L1 + L2 | -Y | from underneath |
| each servo into L5 (bench) | -X | servo comes from -X |
| L4 onto L5 + servos (bench) | -X | lead must be through L4's lead hole first (the plug is 7.6 x 2.6 in section; the hole 9.0 x 5.0) |
| L4 / L5 / servos into L1 + L2 + L3 | +Y (and a false -Y) | from above, onto L2's notches. The -Y is an artefact: a 0.24 mm press overlap at L2's notch floors hides the collision |
| battery | +Y | from above |
| shield (with Nano) into L1-L5 | none, or +X before L2 | it can only slide along X in the grooves: -X is shut by L2's fin, +X by its own reset button (0.3 mm into L4's / L5's posts) and the 1.65 mm board in 1.5 mm grooves. As built it must come **from the front before L6 / L7** (published order too); stepgen needs `direction=` by hand |
| L7, then L6 | +X | from the front, sliding -X |
| adapter onto the shield | none (+Y with the shield's pin rows removed) | the CAD's female sockets are **solid blocks**, so male pins inside them look like a collision. Set `direction=` by hand: +Y |
| radio into U3 | none (+Y with U3 removed) | same reason; +Y |
| barrel plug | none (+Y / +Z with the jack removed) | the plug axis is X but it can back out only 6.5 mm before the battery; it plugs in with a short +X move (the CAD's two poses are 8.95 mm apart) |
| wheels | +Z (right), -Z (left) | along the axle |
| battery snap | +Y | |
| servo plug onto U1 / U2 | +Y physically (the test said -X because the housing is solid over the pins) | |
| controller: Nano | +Y | |
| controller: radio, joysticks, guards | none | solid sockets again; joysticks also clash with the board (section 4); guards overlap the over-thick board by 0.4-0.5 mm |
| controller: USB plug | -X | |

Because the sockets are solid, **every plug-in step on this kit needs a hand-set direction in `guide.py`**, and the lead-line anchors for those steps
should be the pin positions in section 3, not stepgen's contact patches.

### 2.4 Engraved codes (found with `build_model.py`'s `engraved_faces()` test, read from renders of the pocket floors)

All pockets are 0.254 mm deep, letters 6.35 mm tall, the right way round on the face that carries them.

| id | code | engraved face | reads upright with | code centre | where | seen in the finished car |
|---|---|---|---|---|---|---|
| NAUO1 | **L1** | +Y (top) | letters up = -X, baseline -Z (round end away): **upside down against Lee's drawing** | 766.26, 908.97, 1394.03 | front right corner | from all four upper diagonals |
| NAUO2 | **L2** | -Z (car's left) | up = +Y, baseline -X | 677.40, 899.44, 1336.98 | under the deck, rear half | only from below |
| NAUO3 | **L3** | +X (front) | up = +Y, baseline -Z | 643.17, 886.35, 1348.16 | bottom of the cradle, right of centre | only from below |
| NAUO4 | **L4** | +X (towards L5) | up = +Y, baseline -Z | 716.12, 896.98, 1361.41 | under the deck, right of centre | only from below |
| NAUO5 | **L5** | +X (front) | up = +Y, baseline -Z | 742.47, 896.94, 1361.42 | under the deck, right of centre | only from below |
| NAUO6 | **L6** | +Z (outer side) | up = +Y, baseline +X | 766.74, 902.04, 1355.48 | body, under the front of the deck | only from below |
| NAUO7 | **L7** | -Z (outer side) | up = +Y, baseline -X | 767.15, 902.08, 1321.48 | body, under the front of the deck | only from below |

Unlike the MRA, every CAD name equals the engraved code, so `guide.py` can use the CAD names directly.

### 2.5 L1: "FRONT" and "L1" as in Lee's drawing

The drawing measures (mm from the plate's edges, flat end at the top): **FRONT** 5.5-35.1 from the left edge, 5.5-12.0 from the flat edge (29.7 x 6.5
mm); **L1** 6.8-14.0 from the right edge, 5.9-12.0 from the flat edge (7.2 x 6.1 mm). Seen from above with the flat end away (from behind the car),
the left edge is -Z and the right edge +Z. So, keeping the CAD's face (top, +Y; the only code visible from above in the finished car), both read
with letters up = +X and baseline +Z:

- **L1** belongs at x 762.47-768.57, z 1389.48-1396.68: where the CAD's code already is (to 0.7 mm in x and 1.0 mm in z), but **turned 180 degrees**.
  `materials.json`: `"move_engraving": {"NAUO1": {"by": [-0.7, 0, -1.0], "turn": 180}}` (or `"by": [0, 0, 0]`).
- **FRONT** belongs at x 762.47-768.97, z 1278.98-1308.58 (front left corner). Nothing covers it (L7's notch starts at z 1321.5, the left wheel at
  x <= 752.6). The CAD has no pocket for it, so it needs new geometry: a decal (the I/O module's silkscreen route, `decals.json`, ink `#1e1616`), or
  a small extension of `build_model.py` to add text as an engraving.
- If Lee's drawing shows the underside instead (the outline cannot say), both words go on the bottom face with left / right swapped: worth one
  line to Lee.

### 2.6 Which side should carry each code

The rule (rulebook 13, "Seeing the engraved codes") is that each wood step is seen from the side the code faces. Against the build order in 2.3:

- **L1:** top face, as the CAD and Lee's drawing. The first steps (L2, L3) are done with the car upside down (`flip=True`), so the code is
  underneath then; it reads from the title page on.
- **L2 (-Z) and L3 (+X):** fine. Both go on with the car upside down, so a diagonal camera on the -Z side (L2) and the front side (L3) sees
  them. In the finished car they are visible only from below.
- **L4 (+X):** faces L5 while L4 slides +X onto the servos on the bench. By my estimate (not ray-tested) it can still be read from a front-right
  diagonal with L4 hovering 80 mm back, the line of sight passing beyond L5's end, but the -X face would face the student. Worth asking Lee
  which face the real L4 is engraved on.
- **L5 (+X):** fine; faces the camera in the bench step.
- **L6 (+Z), L7 (-Z):** the outer faces are right, but the codes sit on the bodies under the deck, so they can be read only from below.
  The published guide shows these steps from 17-18 degrees below the horizon. Our rulebook forbids that, so either show L7 / L6 with the car
  turned over, or move the codes onto the heads (above the deck, x 750-774.5).
- L4 and L5 are each nearly mirror-symmetric about the centre line, and L6 / L7 share an outline. A student can fit any of them either way
  round, and the code is the only cue to which way the CAD wants it.

## 3. Connector geometry (assembly mm; pin positions as x, z; the pins run along Y unless stated)

### 3.1 Car shield (NAUO23) and the MRA mapping

Board top y 918.54 (underside 916.89); male pin tips y 925.91; plastic spacers y 918.53-920.08. The shield is the MRA's I/O module turned 90
degrees about Y: **x_RCC = 864.28 - z_MRA, z_RCC = 1311.81 + (x_MRA - 43.36), y_RCC = y_MRA + 812.11** (checked on the digital rows, the analogue
rows A0-A7 and the 4-pin headers). So `MRA Build Instructions Prototype/silkscreen.py` positions carry over through this mapping.

- Digital G / V / S rows (the CAD names them N / R / B): G z 1318.53, V z 1321.02, S z 1323.51. Columns (x): AREF 694.64, GND 697.18, D13 699.72,
  D12 702.26 | D11 707.19, D10 709.73, D9 712.27, D8 714.81 | D7 719.74, D6 722.28, D5 724.82, D4 727.36 | D3 732.29, D2 734.83, D1/TX 737.37,
  D0/RX 739.91. The blocks are 12.55 apart, not 12.7.
- Analogue G / V / S: z 1351.58 / 1354.06 / 1356.55; A0 ... A7 at x 722.80 ... 740.58 (pitch 2.54).
- Serial 4-pin (z 1333.01): RX 737.83, TX 740.37, 5V 742.91, GND 745.45. I2C 4-pin (z 1337.96): SCL 737.88, SDA 740.42, 5V 742.96, GND 745.50.
  3V3 row z 1342.28 and GND row z 1344.78, x 737.57 / 740.11 / 742.65.
- Nano sockets (SSW-115) at z 1330.23 and 1345.53, x 693.5-732.1, top y 927.05.
- **Barrel jack** (PJ-002AH): body x 689.29-703.69, y 918.54-929.54, z 1349.56-1358.56, opening -X at x 689.29 (1.8 mm beyond the board edge),
  bore axis y 925.05, z 1354.06; inner contact ring at x 696.7-697.9.
- **Car Nano = node NAUO86** inside NAUO23 (nano-board, ATmega328, FT232, Mini-USB, two 15-pin headers, ICSP). `materials.json`
  `"own_parts": {"NAUO86": ...}` makes it a part, as NAUO126 on the MRA. Its pins: rows z 1330.29 and 1345.53, x 695.04-730.60, tips y 921.05
  (6 mm into the sockets). The USB shell is at x 689.42-698.82, y 931.15-934.90, z 1332.46-1343.36, opening -X. Seen from above with the USB end
  at -X, row z 1330.29 is D12, D11 ... D2, GND, RST, RX0, TX1 (D12 nearest the USB) and row z 1345.53 is D13, 3V3, AREF, A0-A7, 5V, RST, GND, VIN
  (standard Nano pin-out).

### 3.2 Adapter board (NAUO26): Lee's U1 / U2 / U3

Board y 928.58-930.18. The female headers hang **under** the board (bodies y 920.08-928.55, sitting on the shield's spacers), so the real board's
top shows only their solder pads, as in Lee's photo.

| header | position | onto the shield | CAD offset from the shield pins |
|---|---|---|---|
| **U1 (LWh)** = NAUO67, 3-pin male, on top | x 717.50; G z 1318.43, V 1320.97, S 1323.51; pins y 927.18-938.68, plastic 930.18-932.68 | (not on a shield pin) | |
| **U2 (RWh)** = NAUO66, 3-pin male | x 730.20; same z | | |
| **U3** = NAUO69, 2x4 socket, on top | x 745.06 / 747.60; z 1317.16, 1319.70, 1322.24, 1324.78; mouth y 938.88 | | |
| NAUO73 3-pin socket | x 694.64; z 1318.43 / 1320.97 / 1323.51 | AREF row G / V / S | 0.0 / 0.1 mm |
| NAUO71 2-pin socket | x 699.72, 702.26; z 1323.51 | D13 S, D12 S | 0 |
| NAUO68 4-pin socket | x 707.34-714.96; z 1323.51 | D11, D10, D9, D8 S | +0.15 mm in x |
| NAUO65 2x3 socket | x 722.58, 725.12; z 1318.43 / 1320.97 / 1323.51 | D6 and D5, G / V / S | +0.30 mm |
| NAUO72 3-pin socket | x 740.36; same z | D0 row G / V / S | +0.45 mm |
| NAUO70 2-pin socket | x 740.36; z 1343.20, 1345.74 | 3V3 row / GND row (middle column) | +0.25 x, **+0.94 z** |
| C1 | x 740.2-747.2, z 1327.7-1334.3 | | |

The photo's "S V G" under U1 and U2 runs from +Z to -Z, matching S at z 1323.51 and G at 1318.43. The offsets come from the shield model's 12.55 mm
block spacing against the adapter's exact 0.1" grid. Use the shield's pin positions for any label or lead line.

### 3.3 Servo leads and plugs

- Conductors 0.98 mm in diameter, 1.1 mm apart. At the servo the lead leaves the motor's -X face at x 715.7, y 905.7 / 906.8 / 907.9 (right motor
  z 1384.65: yellow, red, brown from the bottom up; left motor z 1292.35: brown, red, yellow, because it is the same motor turned over), then
  through L4's lead hole.
- Pose 1 (loose): ribbon straight to x 662.45 (56.5 mm), separated ends 14.4 mm to x 649.25, in the loose housing (NAUO21 right at z 1385.68; NAUO22
  left at z 1291.29), x 638.12-652.12, **mating face -X at x 638.12**, cavities at y 910.51 / 913.04 / 915.58. Right: yellow, red, brown upward;
  left: brown, red, yellow upward. Total wire about 71 mm.
- Pose 2 (routed): right lead about 165 mm, left about 110 mm, looping up to y 982 / 971. Housings NAUO19 (U2) and NAUO20 (U1), y 932.68-946.68,
  mating face down at y 932.68 on the header plastic; cavities exactly on the pins; wires end at y 943.8. **Colours are right on both plugs:
  yellow on S, red on V, brown on G.**

### 3.4 Battery lead and barrel plug

- Snap NAUO15 on the battery top (x 635.7-647.7, y 938.3-945.5, z 1325.7-1353.7). Both conductors (1.36 mm) leave its +Z end at (640.65, 943.7,
  1353.98) and (642.6, 943.7, 1353.96).
- Plugged pose: NAUO41 (34.2 / 32.0 mm) to the plug's back at x 659.5 (y 925.0, z 1354.75 / 1353.27). Plug NAUO29 body x 659.74-685.24 (8.6
  diameter), sleeve to 694.74, tip at x 696.29: 7.0 mm into the jack, on its axis.
- Unplugged pose: NAUO42 (28.4 / 26.9 mm) to x 650.6; plug NAUO28 everything 8.95 mm back, tip at 687.34 (1.95 mm short of the jack mouth), its
  back almost on the battery.

### 3.5 Car radio

NAUO10 pins at x 745.06 / 747.56, z 1317.28 ... 1324.78 (the model's pitch is 2.50, U3's 2.54: up to 0.12 mm apart), y 933.38-938.88 (5.5 mm into
U3). Board y 938.88 up, x 743.56-772.56: it reaches forward over the L6 / L7 heads to 1.9 mm short of L1's front edge.

### 3.6 Controller (NAUO30)

- Board top y 918.54. **H2** (NAUO45) z 1105.29 and **H1** (NAUO46) z 1120.53, 15 contacts each at x 695.04-730.60 (2.54), mouth y 927.04, 15.24
  apart. Controller Nano NAUO27: pin rows z 1105.3 / 1120.5, same x, tips y 921.04; ICSP 2x3 on top at x 730.47 / 733.01, z 1110.4 / 1112.9 /
  1115.5. H2 holds D12 ... TX1 and H1 holds D13 ... VIN (USB end -X).
- **L-JS** (NAUO49) and **R-JS** (NAUO48): 2x5 right-angle sockets lying on the board, bodies x 725.75-734.25 / 725.62-734.12, y 918.54-923.54, z
  1078.19-1091.50 / 1150.96-1164.27; tails go down into the board at x 735-738.6 behind them; **mouth faces -X** at x 725.75 / 725.62. Rows of 5 at
  z 1079.76, 1082.30, 1084.84, 1087.38, 1089.92 (L-JS) and 1152.53 ... 1162.69 (R-JS).
- Joystick header (5x_Ang_Conn): 5 pins at z 1079.92, 1082.42, 1084.92, 1087.42, 1089.92 (left joystick; right = +72.77), horizontal at y 921.12-922.60,
  from x 724.08 to tips at 731.75: **6 mm into the socket, plugged in moving +X**. Tails down to y 915.63 at x 723.8-724.6.
- Radio socket NAUO44 (2x4): x 709.43-714.43, z 1125.28-1135.85; radio NAUO11 pins at x 710.70 / 713.20, z 1126.75 ... 1134.25, y 921.74-927.24.
- Cut-outs in the board for the joysticks: x 695.9-727.5, z 1070.4-1099.4 and 1143.0-1172.2 (31.6 x 29.0).
- C1 (NAUO47): x 698.7-705.3, z 1126.7-1133.7.
- USB plug NAUO16: x 640.92-694.92, tip 5.5 mm into the Nano's socket at x 689.42.

## 4. What looks wrong or missing for the real kit

1. **Joystick vs controller board.** The KY-023 PCB is 34.0 long in X, the board's cut-out 31.6. In the CAD the joystick PCB lies in the board's
   plane and overlaps the board by 4.2 mm at the -X end (x 691.7-695.9). As placed, its header lines up with the L-JS / R-JS socket, so the
   socket height is consistent. Ask Lee how the joystick really sits: in the guard's pocket, or on a larger cut-out.
2. **Joystick underside vs guard.** The joystick's gimbal and legs go 2.8 mm into the guard's pocket floor (y 915.0-917.0).
3. **The controller PCB is modelled 2.64 mm thick** (a `BottomCopper` slab y 915.9-918.44 under a 0.1 mm top layer). The guards overlap it by
   0.4-0.5 mm, enough to make stepgen call them stuck.
4. **The guard is two pieces in the CAD (left / right) but four in Lee's photo** (two along the top edge meeting at the centre, plus a separate
   handle on each side). The photo's L-JS / R-JS sockets show five bent pins; the CAD has 2x5 sockets. Worth confirming.
5. **Servo leads:** two poses with different lead lengths: loose 71 mm, routed 110 mm (left) and 165 mm (right). The routed loops stand up to
   y 982, about 43 mm above the plugs. The real FS90R lead is one length (measure it); our routes in `wire-paths.json` should share it.
6. **Battery lead:** only 27-34 mm long in the CAD, and 6 mm longer in the plugged pose than the unplugged. Measure the real snap-to-barrel lead.
7. **USB:** the CAD has a Mini-B plug with 54 mm of cable for the controller, but no A end. The MRA's `usb-mini-b.glb` and `usb-a-end.glb`
   (`extra_parts`) can be reused. There is no USB cable on the car, and a Mini-B plug in the car's Nano would run into the battery (the plug model's
   last 9 mm passes through it): the car's Nano can be reached by USB only with the battery out.
8. **The shield's reset button** (x 702.1-707.3, z 1360.6-1363.6) reaches 0.3 mm into L4's / L5's corner posts (which start at z 1363.3), so sliding
   the shield in from the front clips it. The real board presumably flexes past; a hand-set path or a 0.3 mm `adjust_mm` would let stepgen pass it.
9. **Press fits modelled as overlaps:** L1's L2 slots 2.91 mm for 3.0 mm wood; L3's tabs 0.13 mm over; L2 overlaps L1's notch end by 0.3 mm; shield
   grooves 1.5 mm for a 1.65 mm board; L4 / L5 on L2 by 0.24 mm. Harmless for pictures, but they confuse `blocked()` (section 2.3).
10. **Adapter sockets off the shield pins** by 0.15-0.45 mm, and the 3V3 / GND 2-pin socket by 0.94 mm (section 3.2). Cosmetic.
11. **Female sockets are solid blocks** (adapter, controller, radio sockets, barrel jack, plug housings), which makes every plug-in look stuck
    to the generator.
12. **No screws anywhere.** Everything is tab, slot or snap; the servos hang by their ears, and the wheels press on. If the kit fixes the wheels
    with the servo's horn screw, it is missing.
13. **Nothing in the CAD is visibly out of place** apart from the above. The servo ears, shafts, wheels, battery, snap, Nano pins, radio pins and
    plugged leads all sit within 0.2 mm of their mates.
14. **Colours:** none in the GLB (section 0).

## 5. Notes for whoever writes `guide.py`

- Car parts: NAUO1-10, 14, 15, 17-23, 26, 28/29, 41/42 (and the leads as routes). Controller parts: NAUO11-13, 16, 24, 25, 27, 30. They can be one
  guide or two.
- `own_parts`: NAUO86 (car Nano). Leads `"omit": true`, centre lines from NAUO31-40 / 41-42 into `wire-paths.json` (`tools/wires.py`), each pair
  of poses giving a loose route and a plugged route of the same length.
- Hand-set `direction=` for the shield (from the front), adapter, radio, servo plugs, barrel plug, the controller's radio, joysticks (+X slide) and
  guards. Hand-set path for L2 (section 2.3). `flip=True` for L2 and L3 (and possibly L6 / L7, to read their codes).
- `"move_engraving"` for L1, plus a FRONT decal (section 2.5).
- Destination labels: `U1` / `U2` on the adapter (Lee's photo prints `LWh` / `RWh` beside them and `S V G` below), with the pin tops at y 938.68.
