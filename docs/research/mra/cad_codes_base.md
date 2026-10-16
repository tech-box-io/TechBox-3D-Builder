# MRA: engraved codes and base-joint geometry, from the CAD

Source: `MRA Build Instructions Prototype/mra.glb` only (112 instances NAUO1..NAUO112). All coordinates are millimetres in assembly
space (the GLB's metres x 1000), Y up, parts as assembled. The same facts are in `cad_codes_base.json`. Pictures: `stills/codes/` (one
per wood part) and `stills/cad_base/` (plans, sections and the servo sequence).

Status: complete (all of sections 1, 2 and 3 (a) - (f)).

Main findings:

1. Engraved codes were read for all 44 wood parts. Only 18 CAD names match. Besides the mismatches already known (B3, B7, B8, R5/R6), **almost the
   whole arm is renumbered** (CAD A2_Supplement, A3 - A12 are engraved A3 - A13 in a different order) and **five claw parts** (CAD C4 - C8 are engraved
   C6, C4, C5, C8, C7).
2. NAUO41 - 44 are a separate snap-together block engraved T1 / T2, standing beside the base, touching nothing.
3. The base servo hangs in R1 by its ears, so it goes in from above with the horn leading. **The horn cannot pass R1 straight down at any rotation,
   and not at all while the servo is square to the hole with the horn across it as in the CAD.** It passes lengthwise along R1's hole and notch,
   end-first, with the servo tilted about the X axis. 3(a) gives tested, collision-free pose sequences: B (whole servo a quarter-turn away, laid over,
   swung upright, twisted back, pressed down: this is what the video report describes) and A (horn turned on the shaft instead).
4. **The CAD has the horn 1.68 mm too high for B2**: the horn's arms sit inside B2's wood. As modelled B2 cannot slide in and the horn does not
   reach into B1's pocket. With the horn drawn 1.7 - 2.0 mm lower (or servo and horn together 2.0 - 2.3 mm lower, which also puts the servo's boss in
   B2's round hole as the video report describes) everything in 3(c) and 3(d) works. B2's slot opens towards -Z: B2 moves -Z relative to the turret,
   47.5 mm from shaft-at-the-edge to seated.
5. R2, R3, R4 go on straight down, R5 in +Z, R6 in -Z; every one is a snap fit (barbs about 1 mm proud), so a rigid straight path overlaps by
   about 1 mm over the last 5.5 mm. R2's cut-out is 0.57 mm shorter than the servo it closes over.

## 1. Engraved codes on the wood parts (NAUO1 - NAUO44)

How this was read. Every wood part is a 3.0 mm plate with one pocket 0.25 mm deep cut into one face (found with the same test as
`tools/build_model.py engraved_faces()`: faces that neither lie in an outer plane nor span the full thickness). The pocket floors were
filled in black with PIL, looking straight at the engraved face from outside the part, at four rotations and in the mirrored state, and
the pictures were read by eye. In every case exactly one of the unmirrored rotations reads as normal text, so the engraving is modelled
the right way round on the face that carries it. 6 and 9 were told apart by the letter in front of them (the letter is only upright one
way). The pictures that were read are in `stills/codes/<id>.png` (whole part with the code in red on the left, the code enlarged on the
right, both seen from outside the engraved face with the code upright).

Result: the CAD name is the engraved code for only 18 of the 44 parts. The codes below are what a student sees on the wood.

Columns. "Outward normal" is the direction the engraved face looks in, as assembled. "Reads along / up along" are the assembly-space
directions of the text's baseline (left to right) and of the top of the letters; a vector in brackets means the part sits at an angle in
the assembly. "Where the code sits" is the centre of the code as a fraction of the part's outline, seen from outside the engraved face
with the code upright. Part size is (width along the text baseline) x (height along the text's up) x thickness.

| id | CAD name | engraved code | name matches? | engraved face: outward normal | code reads left-to-right along / up along | code centre (mm) | where the code sits, with the code upright | part size (mm) |
|---|---|---|---|---|---|---|---|---|
| NAUO1 | ARA_B1 | **B1** | yes | +Y | -X / +Z | -7.9, 90.4, 100.0 | right end, bottom edge (92% across, 7% up) | 242.7 x 95.0 x 3.0 |
| NAUO2 | ARA_B2 | **B2** | yes | +Y | -X / +Z | -10.2, 93.4, 100.0 | right end, bottom edge (93% across, 7% up) | 242.7 x 95.0 x 3.0 |
| NAUO3 | ARA_B4 | **B4** | yes | -X | +Z / +Y | 68.7, 97.2, 122.1 | left of centre, lower half (23% across, 35% up) | 74.8 x 18.9 x 3.0 |
| NAUO4 | ARA_B5 | **B5** | yes | -Z | -X / +Y | -14.9, 106.9, 105.2 | right end, lower half (89% across, 33% up) | 110.5 x 49.7 x 3.0 |
| NAUO5 | ARA_B6 | **B6** | yes | -Z | -X / +Y | -14.9, 106.9, 128.8 | right end, lower half (91% across, 35% up) | 134.7 x 56.1 x 3.0 |
| NAUO6 | ARA_B6 | **B6** | yes | -Z | -X / +Y | -14.9, 106.9, 150.2 | right end, lower half (91% across, 35% up) | 134.7 x 56.1 x 3.0 |
| NAUO7 | ARA_B8 | **B7** | NO | -Z | -X / +Y | -14.9, 106.9, 173.8 | right of centre, lower half (79% across, 33% up) | 59.7 x 49.7 x 3.0 |
| NAUO8 | ARA_B9 | **B8** | NO | +Y | +Z / +X | 26.1, 137.1, 141.2 | centre, top edge (50% across, 89% up) | 95.0 x 59.7 x 3.0 |
| NAUO9 | ARA_B10 | **B3** | NO | -X | +Z / +Y | 1.3, 106.8, 140.7 | centre, lower half (50% across, 37% up) | 95.0 x 53.5 x 3.0 |
| NAUO10 | ARA_R1 | **R1** | yes | +Y | +Z / +X | 139.5, 102.8, 142.7 | centre, bottom edge (53% across, 16% up) | 70.0 x 72.7 x 3.0 |
| NAUO11 | ARA_R2 | **R2** | yes | -Z | -X / +Y | 145.9, 128.8, 129.7 | right of centre, middle (75% across, 45% up) | 72.7 x 71.3 x 3.0 |
| NAUO12 | ARA_R3v2 | **R3** | yes | +X | -Z / +Y | 195.5, 112.6, 147.7 | left of centre, lower half (40% across, 32% up) | 70.0 x 50.0 x 3.0 |
| NAUO13 | ARA_R4v2 | **R4** | yes | -X | +Z / +Y | 132.1, 112.6, 147.3 | right of centre, lower half (60% across, 32% up) | 70.0 x 50.0 x 3.0 |
| NAUO14 | ARA_R5 | **R6** | NO | +Z | +X / +Y | 140.7, 112.6, 172.1 | left of centre, lower half (28% across, 21% up) | 82.7 x 91.5 x 3.0 |
| NAUO15 | ARA_R6 | **R5** | NO | -Z | -X / +Y | 140.4, 112.6, 109.1 | right of centre, lower half (72% across, 23% up) | 82.7 x 81.8 x 3.0 |
| NAUO16 | ARA_R7 | **R7** | yes | +Z | +X / +Y | 181.1, 171.4, 177.6 | right of centre, top edge (80% across, 86% up) | 35.7 x 25.1 x 3.0 |
| NAUO17 | ARA_R8 | **R8** | yes | -Z | -X / +Y | 159.5, 171.4, 103.6 | right of centre, top edge (80% across, 86% up) | 35.7 x 25.1 x 3.0 |
| NAUO18 | ARA_A1 | **A1** | yes | -Z | [-0.91, 0.41, 0.00] / [0.41, 0.91, 0.00] | 150.1, 173.5, 123.7 | right of centre, middle (77% across, 55% up) | 60.0 x 12.7 x 3.0 |
| NAUO19 | ARA_A2 | **A2** | yes | -Z | [-0.91, 0.41, 0.00] / [0.41, 0.91, 0.00] | 150.1, 172.6, 120.7 | right of centre, middle (77% across, 51% up) | 60.0 x 12.7 x 3.0 |
| NAUO20 | ARA_A2_Supplement | **A3** | NO | -Z | [-0.91, 0.41, 0.00] / [0.41, 0.91, 0.00] | 151.0, 172.3, 117.7 | right of centre, middle (76% across, 50% up) | 60.0 x 12.7 x 3.0 |
| NAUO21 | ARA_A3 | **A4** | NO | -Z | [-0.67, -0.74, -0.00] / [-0.74, 0.67, 0.00] | 153.5, 186.7, 126.7 | right of centre, middle (78% across, 51% up) | 90.0 x 10.0 x 3.0 |
| NAUO22 | ARA_A4 | **A5** | NO | -Z | [-0.91, 0.41, 0.00] / [0.41, 0.91, 0.00] | 209.7, 229.4, 123.7 | right end, middle (84% across, 48% up) | 125.0 x 10.0 x 3.0 |
| NAUO23 | ARA_A5 | **A7** | NO | -Z | [-0.67, -0.74, -0.00] / [-0.74, 0.67, 0.00] | 206.2, 196.2, 126.7 | centre, middle (43% across, 51% up) | 92.0 x 12.0 x 3.0 |
| NAUO24 | ARA_A6 | **A8** | NO | +Z | [0.67, 0.74, 0.00] / [-0.74, 0.67, 0.00] | 203.9, 192.1, 162.3 | centre, middle (52% across, 47% up) | 92.0 x 12.0 x 3.0 |
| NAUO25 | ARA_A7 | **A11** | NO | +Z | [0.67, 0.74, 0.00] / [-0.74, 0.67, 0.00] | 185.4, 229.4, 169.1 | right of centre, middle (80% across, 48% up) | 90.0 x 10.0 x 3.0 |
| NAUO26 | ARA_A8 | **A10** | NO | +Z | +X / +Y | 221.5, 237.8, 166.1 | right of centre, upper half (60% across, 76% up) | 56.0 x 27.9 x 3.0 |
| NAUO27 | ARA_A9 | **A12** | NO | +Z | [0.91, -0.41, -0.00] / [0.41, 0.91, 0.00] | 256.3, 230.2, 169.1 | left of centre, middle (27% across, 49% up) | 90.0 x 10.0 x 3.0 |
| NAUO28 | ARA_A10 | **A13** | NO | +Z | [0.91, -0.41, -0.00] / [0.41, 0.91, 0.00] | 247.4, 212.5, 169.1 | left of centre, middle (29% across, 49% up) | 90.0 x 10.0 x 3.0 |
| NAUO29 | ARA_A11 | **A6** | NO | [-0.74, 0.67, 0.00] | +Z / [0.67, 0.74, 0.00] | 213.8, 206.5, 137.8 | left of centre, upper half (32% across, 73% up) | 36.2 x 66.8 x 3.0 |
| NAUO30 | ARA_A12 | **A9** | NO | +Z | [0.67, 0.74, 0.00] / [-0.74, 0.67, 0.00] | 197.3, 192.7, 139.4 | centre, upper half (49% across, 72% up) | 25.0 x 11.7 x 3.0 |
| NAUO31 | ARA_A12 | **A9** | NO | +Z | [0.67, 0.74, 0.00] / [-0.74, 0.67, 0.00] | 205.3, 201.5, 152.3 | centre, upper half (49% across, 72% up) | 25.0 x 11.7 x 3.0 |
| NAUO32 | ARA_C1 | **C1** | yes | +Z | +X / +Y | 335.9, 203.7, 166.1 | right of centre, top edge (78% across, 82% up) | 48.4 x 40.7 x 3.0 |
| NAUO33 | ARA_C2 | **C2** | yes | -Z | -X / +Y | 335.4, 203.6, 126.7 | left of centre, top edge (23% across, 82% up) | 48.4 x 40.7 x 3.0 |
| NAUO34 | ARA_C3 | **C3** | yes | -Y | +Z / -X | 314.0, 193.6, 147.3 | centre, upper half (52% across, 66% up) | 47.7 x 58.2 x 3.0 |
| NAUO35 | ARA_C4 | **C6** | NO | -Y | +Z / -X | 313.8, 180.1, 147.3 | centre, top edge (52% across, 83% up) | 47.7 x 46.5 x 3.0 |
| NAUO36 | ARA_C5 | **C4** | NO | -Z | -X / +Y | 335.1, 186.6, 129.7 | left of centre, middle (28% across, 42% up) | 40.4 x 16.5 x 3.0 |
| NAUO37 | ARA_C6 | **C5** | NO | +Z | +X / +Y | 327.2, 186.7, 158.6 | centre, middle (53% across, 42% up) | 40.4 x 16.5 x 3.0 |
| NAUO38 | ARA_C7 | **C8** | NO | -Y | -X / -Z | 362.4, 176.5, 157.8 | centre, lower half (46% across, 38% up) | 69.0 x 21.1 x 3.0 |
| NAUO39 | ARA_C8 | **C7** | NO | -Y | -X / -Z | 363.1, 176.5, 136.9 | centre, upper half (45% across, 62% up) | 69.2 x 21.5 x 3.0 |
| NAUO40 | ARA_C9 | **C9** | yes | -Y | +Z / -X | 314.1, 174.1, 147.6 | centre, upper half (53% across, 79% up) | 47.6 x 40.4 x 3.0 |
| NAUO41 | TB_TopBot | **T1** | NO | +Y | +X / -Z | 205.3, 93.8, 47.0 | right of centre, upper half (76% across, 80% up) | 38.1 x 38.1 x 3.0 |
| NAUO42 | TB_CenterLatches | **T2** | NO | +X | +Z / -Y | 196.6, 108.0, 58.6 | centre, upper half (50% across, 61% up) | 22.2 x 52.6 x 3.0 |
| NAUO43 | TB_CenterLatches | **T2** | NO | +Z | +X / +Y | 195.2, 119.7, 59.9 | centre, upper half (50% across, 61% up) | 22.2 x 52.6 x 3.0 |
| NAUO44 | TB_TopBot | **T1** | NO | +Y | +Z / +X | 206.7, 136.6, 68.6 | right of centre, upper half (76% across, 80% up) | 38.1 x 38.1 x 3.0 |

Mismatches between CAD name and engraving (26 parts, counting the four `TB_` parts):

- Base: CAD B8 = **B7** (NAUO7), CAD B9 = **B8** (NAUO8), CAD B10 = **B3** (NAUO9). (B1, B2, B4, B5, B6 x2 match.) There is no part engraved B9 or B10.
- Turret: CAD R5 = **R6** (NAUO14), CAD R6 = **R5** (NAUO15). R1-R4, R7, R8 match (R3 and R4 are named `R3v2`, `R4v2`).
- Arm: only A1 and A2 match. CAD A2_Supplement = **A3** (NAUO20), A3 = **A4** (NAUO21), A4 = **A5** (NAUO22), A5 = **A7** (NAUO23),
  A6 = **A8** (NAUO24), A7 = **A11** (NAUO25), A8 = **A10** (NAUO26), A9 = **A12** (NAUO27), A10 = **A13** (NAUO28), A11 = **A6** (NAUO29),
  A12 = **A9** (NAUO30 and NAUO31, two identical parts). So the engraved arm set is A1-A13 with A9 twice; the CAD names stop at A12.
- Claw: CAD C4 = **C6** (NAUO35), C5 = **C4** (NAUO36), C6 = **C5** (NAUO37), C7 = **C8** (NAUO38), C8 = **C7** (NAUO39). C1, C2, C3, C9 match.
- The four `TB_` parts are engraved **T1** (NAUO41, NAUO44) and **T2** (NAUO42, NAUO43): see section 2.

Cross-check: the codes read separately for `cadasio_mra_project.md` (its section 1.4) agree with this table on all 44 parts.

Notes on faces (useful for part pictures and for which way round a part goes; all read off the table):

- Horizontal plates are engraved on top (+Y): B1, B2, R1, B8, and the T1 pair. R1's code is therefore inside the turret box once R2-R6 are on.
- Turret walls are engraved on the face that looks away from the turret's middle (x = 164, z = 141): R3 (NAUO12) on +X, R4 (NAUO13) on -X,
  R6 (NAUO14) on +Z, R5 (NAUO15) on -Z, R7 (NAUO16) on +Z, R8 (NAUO17) on -Z. R2 (NAUO11), the wall in the middle, is engraved on -Z.
- Controller: B3 (NAUO9) and B4 (NAUO3) are engraved on -X; B5, both B6 and B7 (NAUO4, 5, 6, 7) are all engraved on -Z, so B5's code looks
  outwards and B7's looks inwards. The two B6 (NAUO5, NAUO6) are the same part in the same orientation, 21.4 mm apart in Z.
- Claw: the flat plates C3 (NAUO34), C6 (NAUO35), C9 (NAUO40) and the two gear fingers C8 (NAUO38), C7 (NAUO39) are all engraved on their
  underside (-Y) in the CAD pose.

## 2. NAUO41 - NAUO44 (`TB_TopBot`, `TB_CenterLatches`): a separate four-piece block

Measured:

- Two identical square plates, engraved **T1**: NAUO41 (y 90.91 - 93.91) and NAUO44 (y 133.74 - 136.74), each 38.10 x 38.10 x 3.0 mm, x 176.14 - 214.24,
  z 39.49 - 77.59, with a plus-shaped slot in the middle (arms 3.00 wide, 20.34 long, centred on x = 195.19, z = 58.54).
- Two identical strips, engraved **T2**, 22.23 wide x 52.59 long x 3.0: NAUO42 stands in the plane x = 193.69 - 196.69, NAUO43 in the plane
  z = 57.04 - 60.04; both run from y = 87.53 to y = 140.12. Each has one slot along its centre line, half its length. NAUO42's slot is open at
  the top (material on the centre line only from y 87.54 to 113.66); NAUO43 is the same part turned upside down, slot open at the bottom
  (material from y 113.98 to 140.10). The two cross each other in a half-lap and make a plus-shaped column.
- Each end of each strip is a snap latch: two 1.0 mm slits make springy outer fingers, the strip is 19.82 wide where a T1 plate sits
  (plate slot 20.34), and 21.98 - 22.20 wide just outside and just inside the plate. So each T1 is pushed over the end of the column and
  clicks into a 3 mm groove; the column ends stick out 3.38 mm beyond each T1.
- No part of the four touches or overlaps any other part of the model (deepest overlap between the four themselves: 0.000 mm).
- The block stands on the same plane as the underside of B1 (y = 87.53), 15.75 mm clear of B1's long -Z edge (block z max 77.59, B1 z min 93.34),
  about 88 mm from the turret's axis (x 163.64, z 140.84). Overall size 38.1 x 52.6 x 38.1 mm.

What it is. From the CAD alone: a free-standing spool-shaped block, not connected to the arm, base or controller. It carries codes in the same
style as the kit's other wood (T1, T2), so it is cut from the kit's sheets. GUESS: it is the object for the arm to pick up (the claw closes on
the 19 - 22 mm wide column between the two plates); "T" might stand for tower or target. Nothing in the CAD says so.

Is it part of the build? It is not part of base -> controller -> arm -> claw: it joins nothing. If the guide covers it, it is a short build of
its own with motions that follow from the geometry: (1) NAUO43 down (-Y) over NAUO42, slot into slot, 26.1 mm of travel; (2) NAUO41 pushed
up (+Y) onto the bottom end and NAUO44 pushed down (-Y) onto the top end until they click. Whether TechBox's instructions include it has to
come from the build notes, the video or the published Cadasio project (the published project's model does contain the `TB_` components; that
was seen in the scratch copy of the project JSON, not in the CAD).

## 3. The base, in detail

Parts and where they are (all as assembled in the CAD):

| part | id | lies in | notes |
|---|---|---|---|
| B1 | NAUO1 | y 87.53 - 90.53 | bottom plate, 242.7 x 95.0 |
| B2 | NAUO2 | y 90.53 - 93.53 | on top of B1, same outline |
| R1 | NAUO10 | y 99.96 - 102.96 | turret floor, body x 127.58 - 200.28, z 112.00 - 169.20, tabs out to z 105.62 and 175.58 |
| R2 | NAUO11 | z 129.55 - 132.55 | cross wall over the servo |
| R3 | NAUO12 | x 192.67 - 195.67 | +X wall |
| R4 | NAUO13 | x 131.94 - 134.94 | -X wall |
| R5 | NAUO15 (CAD name R6) | z 109.00 - 112.00 | -Z wall; bottom edge y 93.53 |
| R6 | NAUO14 (CAD name R5) | z 169.20 - 172.20 | +Z wall; bottom edge y 93.53 |
| base servo | NAUO45 | x 157.56 - 169.71, z 119.37 - 151.57, y 91.61 - 123.86 | MG90S, shaft down |
| horn | NAUO46 | x 145.46 - 181.81, z 137.52 - 144.17, y 89.86 - 94.41 | double-ended, 36.35 long |

The servo, measured (it hangs shaft-down):

- Shaft axis: x = 163.64, z = 140.84 (vertical). Splined shaft 4.87 dia from y 91.61 to 95.56.
- Gearbox (the stepped part round the shaft): y 95.56 - 101.31, x 157.74 - 169.54 (11.80 wide), z 132.00 - 146.73. Seen from below it is an
  11.8 mm circle on the shaft axis plus a smaller boss towards -Z; its farthest point from the axis is 8.84 mm away.
- Body: y 101.31 - 123.86, x 157.56 - 169.71 (12.15 wide), z 124.19 - 146.74 (22.55 long). The shaft is 5.90 from the body's +Z end and 16.65 from its -Z end.
- Mounting ears: y 102.96 - 105.46 (2.5 thick), reaching z 119.37 and z 151.57 (32.2 over the ears). **The underside of the ears (y 102.96) is exactly
  R1's top face (y 102.96): the servo hangs in R1 by its ears.** The ears cannot pass R1's hole, so the servo can only have gone in from above.
- Leads: three 1.0 mm stubs side by side, x 162.12 - 165.16, y 118.61 - 119.60, coming out of the +Z end face (z 146.77) to z 149.77.

The horn, measured: 36.35 long (18.18 each side of the shaft axis), lying along X in the CAD. Hub 6.65 dia, y 89.86 - 94.41 (4.55 tall). Arms
y 90.16 - 92.21 (2.05 thick), 5.9 wide next to the hub tapering to 3.2 at the rounded tips, with a row of small holes. Between the top of the
arms (y 92.21) and the underside of the gearbox (y 95.56) there is a neck 3.35 mm tall and at most 6.65 wide (hub, then shaft).

One thing in the CAD that is not physically possible, which matters for (c) and (d): **the horn's arms (y 90.16 - 92.21) lie inside B2's thickness
(y 90.53 - 93.53), and B2 has no cut-out for them** (see (c)). The only other overlap in the base larger than a press fit (0.15 mm) is the top of the servo in R2's cut-out, 0.58 mm (see (b)).

### (a) Base servo + horn into R1 (NAUO45 + NAUO46 into NAUO10)

The opening in R1 (plan view; picture `stills/cad_base/R1_plan.png`):

- Main hole: x 157.39 - 169.89 (12.50) by z 124.09 - 146.84 (22.75). The servo body (12.15 x 22.55) fills it with 0.17 mm each side in X and
  0.10 mm each end in Z.
- A notch off the +Z end of the hole: x 160.78 - 166.49 (5.71 wide), z 146.84 - 153.19 (6.35 deep). It is centred on the shaft axis in X (163.64).
  Hole plus notch are 29.10 long on that centre line.
- A 1.00 mm slit from the -Z end of the hole to R1's -Z edge (x 157.39 - 158.39, z 112.00 - 124.09). It is the relief cut of the snap latch beside it;
  nothing can pass through it.
- Outline of the opening, corner by corner (x, z): (158.39, 112.00) (158.39, 124.09) (169.89, 124.09) (169.89, 146.84) (166.49, 146.84) (166.49, 153.19)
  (160.78, 153.19) (160.78, 146.84) (157.39, 146.84) (157.39, 112.00).

Against the horn: the longest straight line that fits in hole + notch is 30.5 mm (corner (157.39, 124.09) to corner (166.49, 153.19)); the main hole's
diagonal is 25.96. The horn is 36.35 long.

**Straight down does not work at any rotation.** Tested: horn laid flat in the thickness of R1, turned about the shaft axis in 5-degree steps over
the full half-turn, shifted sideways in 1 mm steps over +/-14 mm in X and +/-22 mm in Z. At every one of those positions some of the horn is buried
1.47 - 1.50 mm (half the plate) in R1's wood.

**With the horn as in the CAD (across the servo, along X) and the servo square to the hole, no tilt works either.** Search over tilt about the Z axis, lift and sideways shift in X: from
the seated position the servo can only reach tilts of +/-6 degrees, lifts up to 7.5 mm and shifts of +/-2.5 mm; it never gets out. The hole is
only as wide (12.50) as the body (12.15), so the 36 mm horn cannot be threaded through across it.

**It goes through lengthwise, along the hole's long direction (Z), end-first, with the servo tilted about the X axis.** For that the horn has to
point along Z. There are two ways to get it there: turn the whole servo a quarter-turn about its shaft (sequence B), or turn the horn a quarter-turn
on the shaft (sequence A). Both were tested with the real meshes (198,000 surface points of servo + horn against R1 as an exact prism; every
in-between pose at 0.1 mm / 0.5 degree spacing) and both are collision-free.

Which one is real cannot be told from the CAD. Cross-check outside the CAD: `video_base_seg1.md` (0:18 - 0:22) describes **sequence B** (servo laid
over, one horn tip dipped into the cut-out, swung upright, then the whole servo twisted a quarter-turn and pressed down; horn never turned on its
shaft). So B is the one to animate; A is kept as the alternative that needs no squeeze.

How to read the poses: each is relative to the seated position: a turn about the stated axis through the pivot **P = (163.64, 91.19, 140.84)** (the
middle of the horn hub, on the shaft axis), then a move t = (x, y, z). This is the form `stepgen.turned(axis, degrees, at=P, t)` writes. A turn of
-60 degrees about +X leans the top of the servo towards -Z and puts the -Z end of the horn lowest. Between poses the tilt angle and t were interpolated
linearly with the pivot fixed (for the combined turns that is an even, shortest-way blend from one turn to the next), and that is the path that
was tested. The player's `mixPose` in `js/player.js` blends poses the same way (even turn, straight-line t about the pivot), so the poses can be
used as written.

**Sequence B (as in the video): whole servo a quarter-turn away, laid over 60 degrees.** Servo and horn move as one piece until B4.

| pose | turn through P (servo and horn together) | move t | what has happened | least gap to R1 on the way here |
|---|---|---|---|---|
| B0 | 104.48 deg about (-0.4472, 0.7746, -0.4472), which is a quarter-turn (+90 deg) about +Y followed by -60 deg about +X | (0, 40.0, -6.0) | held above R1: body lying across the hole, horn in line with the hole, laid over 60 deg, one horn tip lowest | - |
| B1 | same | (0, 14.5, -6.0) | straight down 25.5: the leading tip has gone through the hole 1.7 mm inside its -Z end and is 10.0 mm below R1 (tip at z 125.75, y 89.94). The hub is still 2.7 mm above R1 | 0.83 mm |
| B2 | 90 deg about +Y (level) | (0, 7.5, -6.0) | swung upright while coming down 7 mm: the hub, then the trailing tip, have followed through; the trailing tip passes down through the notch and ends at z 153.01 (notch ends at 153.19). Horn 0.25 mm under the floor, gearbox 0.10 mm above it | 0.10 mm |
| B3 | 90 deg about +Y | (0, 7.5, 0) | slid 6.0 mm towards +Z: shaft on its seated axis | 0.10 mm |
| B4 | none | (0, 7.5, 0) | whole servo twisted back a quarter-turn (-90 deg about +Y) about the shaft axis: body now over the hole, horn across it underneath | 0.10 mm |
| B5 | none | (0, 0, 0) | pressed straight down 7.5: body in the hole, ears on R1 | 0.00 (touching by design: ears rest on R1; the body is a 0.10 - 0.17 mm fit) |

- Which end first: by symmetry either horn tip can lead. In the tested sequence the leading tip goes in at the hole's -Z end (the end away from the
  notch) and the trailing tip comes down through the notch. With R1's code upright (it reads along +Z) the notch is at the reader's right.
- The swing B1 -> B2 is close to a plain 60-degree swing about the X-direction line through (163.6, 102.2, 128.8), a point in R1's top face 4.7 mm inside
  the -Z end of the hole. As an exact pure swing about that point it overlaps R1 by 0.23 mm, so use the linear path above (0.00 overlap).
- **The pinch.** The twist B3 -> B4 is only possible while the lift is between 7.40 mm (gearbox clear of the top of R1) and 7.75 mm (horn arms touch the
  underside of R1): the neck between horn and gearbox (3.35 mm) is just 0.35 mm taller than the plate (3.00 mm). Tested: at lift 7.35 the twist overlaps
  by 0.05 mm, at 7.80 by 0.05 mm, from 7.40 to 7.75 by nothing. In wood it would feel like a squeeze.
- The tilt can be as small as 20 degrees: (quarter-turn, then -20 deg about +X = 91.73 deg about (-0.1711, 0.9703, -0.1711)) with t = (0, 40, +2.0) ->
  (0, 14.5, +2.0) -> (0, 12.0, +2.0) -> (0, 9.5, -6.5), then level at (0, 7.5, -6.0) and on as B3 - B5. Tested the same way: least gaps 1.33, 0.45, 0.44,
  0.10 mm, no overlap. A coarser search found a grazing route at 15 degrees. The quarter-turn was tested in one sense only (+90 deg about +Y, which
  lays the long part of the body towards -X).

**Sequence A (alternative, not what the video shows): horn turned to lie along the servo body.** The horn is turned 90 degrees on the shaft first, so
servo and horn make one long shape, the body stays square to the hole and there is no pinch.

| pose | servo: turn about +X through P | move t | what has happened | least gap to R1 on the way here |
|---|---|---|---|---|
| A0 | -20 deg | (0, 40.0, +2.0) | held above R1, tilted, horn in line with the body | - |
| A1 | -20 deg | (0, 14.5, +2.0) | straight down 25.5: the -Z tip of the horn has entered the hole 1.7 mm inside its -Z end (tip at z 125.76, y 99.47) | 1.33 mm |
| A2 | -20 deg | (0, 12.0, +2.0) | 2.5 further down | 0.45 mm |
| A3 | -20 deg | (0, 10.0, -6.0) | slid 8 mm towards -Z and 2 mm down, i.e. along the horn: the -Z half of the horn is under the floor; the +Z tip is above the notch (z 151.9, y 107.4) | 0.45 mm |
| A4 | 0 deg | (0, 7.0, -6.5) | levelled: the +Z tip has swung down through the notch (tip at z 152.51). The whole horn is 0.75 mm under the floor | 0.31 mm |
| A5 | 0 deg | (0, 7.0, 0) | slid 6.5 mm towards +Z; the gearbox is in the hole | 0.31 mm |
| A6 | 0 deg | (0, 0, 0) | straight down 7.0: body in the hole, ears on R1 | 0.00 (by design) |
| A7 | - | - | horn turned back 90 degrees about the shaft axis, under R1, to the CAD pose (free: it sweeps a 36.4 mm circle 5.5 mm below the floor) | free |

During A0 - A6 the horn carries the servo's pose plus its own quarter-turn: as one turn, 91.73 degrees about (-0.1711, 0.9703, -0.1711) through P for
A0 - A3 and 90 degrees about +Y through P for A4 - A6, with the same t as the servo. Here the horn end under the long (-Z) part of the body goes first
and the end that sticks out 12.3 mm past the shaft end of the body goes last, through the notch.

Pictures (section through the shaft axis, x = 163.64, +Z to the right; R1 black, servo blue, horn red): `stills/cad_base/servo_into_R1_servo_turned_60deg.png`
(B), `servo_into_R1_servo_turned.png` (B at 20 degrees), `servo_into_R1_horn_inline.png` (A).

### (b) R2 (NAUO11) over the base servo, tabs into R1

R2 is the wall in the plane z = 129.55 - 132.55 (picture `stills/cad_base/R2_elevation.png`).

- **Direction: straight down (-Y).** It cannot come from any other side: its two legs go down through R1 and its cut-out drops over the servo.
- **The cut-out** is a rectangle open at R2's bottom edge: x 157.39 - 169.89 (12.50 wide), from y 102.96 (bottom edge, which rests on R1's top face)
  up to y 123.29 (20.33 tall). It passes over the servo's **body** (the main case, 12.15 wide, x 157.56 - 169.71), 0.17 mm clear on each side,
  crossing it 5.4 - 8.4 mm from the body's -Z end, i.e. over the part of the body farthest from the shaft. The servo's label (0.3 mm proud on the +X
  side, to x 169.89) just touches the cut-out's edge.
- **The servo is 0.57 mm taller than the cut-out**: servo top y 123.86, cut-out top y 123.29. As modelled R2 overlaps the top of the servo by 0.58 mm
  (strip x 157.59 - 169.69, z 129.61 - 132.50). GUESS: intended, so that R2 presses the servo down onto R1 (nothing else holds it; there are no
  servo screws in the base). For an animation it means R2 stops on the servo's top 0.57 mm before its drawn seat; it will not be noticed.
- **How far:** R2's bottom edge has to start above the servo's top, so at least 20.9 mm above its seat (123.86 - 102.96). The legs reach R1's top face
  when R2 is 6.39 mm above its seat and end 3.39 mm below R1's underside (leg tips at y 96.57, R1 is y 99.96 - 102.96).
- **Legs and slots** (each leg is a plain tab plus a springy latch finger with a barb, separated by a 1.0 mm slit):

| leg | tab at the tip (y 96.57) | latch finger at the tip | barb | slot in R1 (mouth on R1's top face, y 102.96) | lead line: leg tip -> slot mouth |
|---|---|---|---|---|---|
| -X | x 133.30 - 139.56 (widening to 132.93 - 140.61 at the top) | x 129.91 - 131.93 | out to x 128.53 between y 98.91 and 99.96, i.e. hooked under R1 | x 129.49 - 140.49, z 129.55 - 132.55 (11.00 x 3.00) | (134.74, 96.57, 131.05) -> (134.99, 102.96, 131.05) |
| +X | x 188.29 - 194.55 (widening to 187.24 - 194.92) | x 195.92 - 197.94 | out to x 199.32 between y 98.91 and 99.96 | x 187.24 - 198.24, z 129.55 - 132.55 (11.00 x 3.00) | (193.12, 96.57, 131.05) -> (192.74, 102.96, 131.05) |

- The barbs are 0.96 mm wider than the slots, so the last 5.5 mm of the push is a snap fit: moved as a rigid part R2 overlaps R1 by up to 1.0 mm
  from 5.5 mm above its seat down to the seat, and is fully clear from 6.5 mm up. That is how the part is meant to work (the fingers bend into
  their slits), not a modelling error. The same is true of every latch in (f).
- R2's bottom edge sits on R1's top face along x 127.58 - 129.61, 140.61 - 157.39, 169.89 - 187.24 and 198.24 - 200.28.
- Order this fixes: the servo must be in R1 before R2 (R2 closes over it), and R2 must be on before R3 and R4 (they straddle it, see (f)).

### (c) B2 (NAUO2): the open slot and round cut-out

Shape (picture `stills/cad_base/B2_B1_plan.png`): a keyhole cut into B2's long **-Z edge** (the edge at z = 93.34; it is the long edge the code "B2" sits
next to, 6.7 mm in from it).

- Slot: x 157.29 - 169.99 (**12.70 wide**), running from the -Z edge (z 93.34) to z 133.74, where it meets the round cut-out. 40.40 long.
- Round cut-out: centre (163.64, 140.84) = the shaft axis, **radius 9.525** (19.05 dia), far side at z 150.37.
- So the slot **opens towards -Z**. The shaft has to enter at B2's -Z edge and travel +Z along the slot to the middle of the round cut-out:
  **B2 moves in the -Z direction relative to the turret** (equally: the turret moves +Z relative to B2, its R6 side leading).
- **How far:** 47.50 mm from the shaft being level with B2's edge to seated; the horn hub (6.65 dia) is completely outside B2's edge when B2 is
  50.83 mm or more from its seat (140.84 + 3.33 - 93.34). Any start at 51 mm or more works; B2 is 95 mm wide in that direction.
- **Height:** B2 slides at its seated height, y 90.53 - 93.53. Its top face is then 0.00 mm below the bottom edges of R5 and R6 (both at y 93.53):
  the turret rides on B2 and nothing of the turret is tabbed into B2. Everything else on the turret is higher: R2/R3/R4 leg tips y 96.57 (3.04 above B2),
  gearbox underside y 95.56 (2.03 above), R1 y 99.96.
- What is in the slot while it slides: only the horn hub (6.65 dia) and, above y 94.41, the shaft (4.87). 3.0 mm of air each side.
- GUESS about the generous size: the keyhole matches the servo's gearbox, not the hub. The gearbox is 11.80 wide (slot 12.70), and its farthest point
  from the axis is 8.84 mm (cut-out radius 9.525), with its small boss pointing towards -Z, into the slot. In the CAD the gearbox stays 2.03 mm above
  B2, so this is clearance, not a fit.

**There is no collision-free path in the CAD, because the seated pose itself overlaps.** The horn's arms are at y 90.16 - 92.21; B2's wood is
y 90.53 - 93.53. Outside the round cut-out the arms are inside B2: -X arm from x 145.46 to 154.45 (9.0 mm of its length), +X arm from x 172.87 to 181.81
(8.9 mm), 1.68 mm deep. Put the other way: between the top of the horn arms (y 92.21) and the bottom edges of R5/R6 (y 93.53) there is 1.32 mm, and B2 is
3.00 mm thick. The CAD is 1.68 mm short of room. Nothing else is in the way: over a 60 mm slide the servo, R1 - R6 never touch B2.

The nearest thing, tested: **with the horn drawn 1.68 mm or more lower, the straight slide is collision-free** (horn lowered 1.75: least gap 0.08 mm;
lowered 2.0: 0.33 mm; lowered 2.6: 0.93 mm, over the whole 60 mm). Lowered by 1.7 the arms are at y 88.46 - 90.51, entirely inside B1's 3 mm pocket,
which is where they have to be for the model to work at all (see (d)); the hub still overlaps the shaft by 1.1 mm. Which of servo, horn or plates is really off cannot be told from the CAD.

Also tested: **servo and horn lowered together** by 1.70 - 2.33 mm. The slide is collision-free again (least gap 0.03 mm at 1.70, 0.36 at 2.03, 0.43
from 2.10 on), and from 2.03 mm down the gearbox is inside B2's keyhole: 11.80 wide in the 12.70 slot, then turning inside the 19.05 hole. 2.33 mm is
the limit, where the horn hub reaches the table plane (y 87.53). Cross-check outside the CAD: `video_base_seg1.md` (4:14 - 4:17) says the turret is slid
along the slot "until the servo's round boss is in the round hole". In the CAD the boss stops 2.03 mm above B2. GUESS: in the real kit the servo's
output end sits about 2.0 - 2.3 mm lower against the plates than in this CAD (for instance because the CAD's MG90S has its ears too near the shaft end);
that one error would explain the keyhole's size, the horn in B2's layer and the shallow pocket in (d) together.

For the guide there are three ways to show it, none of them exact: (1) draw the horn alone 1.7 - 2.0 mm lower from this step on (smallest visible change;
the ears stay on R1, the gearbox stays above B2); (2) draw servo and horn together about 2.1 mm lower (boss in the round hole as in the video, but the
ears then cut 2.1 mm into R1); (3) have the CAD corrected.

A second way in that the geometry allows (plan view only, same height problem): with the horn turned to lie along the slot (along Z) and the turret
held 8.7 mm or more towards -Z of its seat, the horn passes **straight down through the slot** (tested: overlap 0.00 from 8.7 mm, 2.97 mm of air each
side from 15 mm), and the turret then slides only that 8.7+ mm in +Z to bring the shaft to the centre. Then B2 need not come in from the side at all.
Whether TechBox does it this way is a question for the video.

### (d) B1 (NAUO1): the horn-shaped pocket

- A through-cut (the full 3.0 mm, y 87.53 - 90.53) in the shape of the horn: x 144.81 - 182.45 (37.64 long), z 136.86 - 144.82 (7.96 across the middle),
  centred on the shaft axis (163.63, 140.84). It is the horn's outline grown by about 0.65 mm: round middle 7.96 dia (hub 6.65), straight sides tapering to
  rounded ends 4.52 wide (horn tip 3.24). The smallest gap anywhere between horn and pocket is 0.24 mm.
- It runs along **X**, B1's long direction, which is how the horn lies in the CAD. No turn is needed relative to the CAD pose.
- **Direction: the horn enters from above (-Y)**: the turret on B2 is lowered onto B1 (or B1 is brought up under it). Nothing else of the turret
  reaches B1.
- **The horn has to be lined up first**, to within about **1 degree**: turned 0.5 degrees it still drops in (0.10 mm to spare), at 1.0 degree it touches
  (0.04 mm overlap), at 2 degrees it overlaps 0.3 mm. Either way round will do (turned 180 degrees it fits the same). So in the real build the student
  turns the turret (the servo body) on B2 until the horn underneath is parallel to B1's long edge, then drops it in.
- **Depth as modelled:** the horn barely enters the pocket: hub underside y 89.86 (0.67 mm into B1), arm underside y 90.16 (0.37 mm into B1). With the
  horn 1.7 mm lower (see (c)) the arms sit fully inside the pocket and B2 lies over them, 8.9 mm of each arm end under B2's wood. That is what stops
  the turret lifting off, and what holds the horn still so that the servo turns the turret instead. As modelled, with the arms in B2's layer, neither can happen.
- Cross-check outside the CAD: `video_base_seg2.md` (about 5:00 - 5:10) says nothing was turned to make the horn fit (it already lay along the plates) and
  that the horn ends up "about flush with B1's underside". In the CAD the hub's underside is 2.33 mm above B1's underside (y 89.86 against 87.53). So
  the real horn sits about 2.3 mm lower than modelled, which agrees with the 2.0 - 2.3 mm in (c).
- No collision on the way down in the CAD orientation (horn lifted 0 - 20 mm above its pose: 0.00 mm overlap with B1).

### (e) The six 6 mm screws (NAUO47 - NAUO52)

All six are the same: M3 socket-head screws (CAD name `M3x6mm_91292A111`), axis vertical, **head on top, entered from above (+Y side), driven down (-Y)**.
Head 5.5 dia, y 93.53 - 96.53 (3.0 tall), sitting on B2's top face. Thread 3.0 dia, y 87.53 - 93.53 (6.0 long): it passes **through B2**
(y 90.53 - 93.53, hole 2.80 dia) **and into B1** (y 87.53 - 90.53, hole 2.30 dia), ending flush with B1's underside. The thread is bigger than both holes
(about 0.10 mm per side in B2, 0.35 mm per side in B1; measured overlap 0.16 and 0.41 mm at the thread crests), so it cuts into the wood; that is why the collision test in `stepgen` cannot find a free direction for
them. They touch no other part.

| id | axis x | axis z | where on the base |
|---|---|---|---|
| NAUO47 | 209.16 | 99.69 | turret end, -Z side |
| NAUO52 | 209.16 | 181.99 | turret end, +Z side |
| NAUO48 | 104.07 | 99.69 | middle, -Z side |
| NAUO51 | 104.07 | 181.99 | middle, +Z side |
| NAUO49 | -20.84 | 99.69 | controller end, -Z side |
| NAUO50 | -20.84 | 181.99 | controller end, +Z side |

For lead lines (seated coordinates): screw tip (x, 87.53, z) -> hole mouth on B2's top face (x, 93.53, z); the screw travels along Y only.

### (f) R3 - R6: tabs, slots and directions

Pictures: `stills/cad_base/R3_elevation.png`, `R4_elevation.png`, `R5_elevation.png`, `R6_elevation.png`.

**R3 (NAUO12, plane x 192.67 - 195.67) and R4 (NAUO13, plane x 131.94 - 134.94): straight down (-Y).** The two have the same outline (R4 has one
extra cut, below). Each has three joints downwards and two sideways arms that R5 and R6 later slide onto. In the table x is the middle of the plate:
194.17 for R3, 133.44 for R4.

| joint | on R3 / R4 | receives it | tip (x, y, z) | mouth (x, y, z) |
|---|---|---|---|---|
| leg, -Z | latch finger z 114.34 - 116.35 (barb out to z 112.95 between y 98.91 and 99.96) + tab z 117.73 - 123.98 (widening to 117.35 - 125.03) | R1 slot z 114.03 - 125.03 (11.00 x 3.00) | (x, 96.57, 119.16) | (x, 102.96, 119.53) |
| leg, +Z | tab z 157.22 - 163.47 (widening to 156.17 - 163.85) + latch finger z 164.85 - 166.86 (barb out to z 168.25) | R1 slot z 156.17 - 167.17 (11.00 x 3.00) | (x, 96.57, 162.04) | (x, 102.96, 161.67) |
| half-lap | slot in the bottom edge, z 129.55 - 132.55, from y 102.96 up to y 127.66 | R2, whose top edge here is at y 127.66 (R2's low shoulders, x 127.58 - 135.18 and x 192.67 - 200.28) | slot mouth (x, 102.96, 131.05) | R2's shoulder (x, 127.66, 131.05) |

- Leg tips are at y 96.57, 3.39 mm below R1. The bottom edge between the legs rests on R1's top face (y 102.96).
- How far: clear of R1 from 6.5 mm above the seat; clear of R2 from 24.75 mm above the seat (the wall has to start above R2's shoulder). The last 5.5 mm
  into R1 is a snap fit (rigid overlap up to 1.02 mm at the barbs).
- R4's extra cut is the **L-shaped wire slot**: open at the top edge (y 146.59) at z 140.60 - 142.72 (2.12 wide), down to y 127.25, with a foot
  towards +Z out to z 148.72 between y 127.25 and 135.75.
- Sideways arms (the same on both walls, one towards each of R5 and R6), at y 133.56 - 144.56: a tab (y 133.56 - 141.24, chamfered to 134.61 - 140.87 at
  the tip) and above it a latch finger (y 142.24 - 144.56, barb up to y 145.64). Tips at **z 105.62** (-Z arm) and **z 175.58** (+Z arm). On the -Z arm
  the barb is at z 107.95 - 109.00, just outside R5's outer face; on the +Z arm at z 172.20 - 173.25, just outside R6's.

**R5 (NAUO15, CAD name R6; plane z 109.00 - 112.00): goes on in the +Z direction** (pushed from the -Z side towards the turret).
**R6 (NAUO14, CAD name R5; plane z 169.20 - 172.20): goes on in the -Z direction.** Neither has tabs of its own; each has four slots that take tabs
of R1, R3 and R4. Each wall's inner face ends up against the end of R1's body (z 112.00 and z 169.20).

| wall | slot in the wall (x, y) | takes | tab tip (x, y, z) | slot mouth on the wall's inner face |
|---|---|---|---|---|
| R5 | x 148.39 - 156.19, y 99.96 - 102.96 (7.81 x 3.00) | R1's latch pair: hooked finger x 148.34 - 152.62 (barb out to x 147.18 at z 107.95 - 109.00) and wedge finger x 153.62 - 156.19 | (152.27, 101.46, 105.62) | (152.29, 101.46, 112.00) |
| R5 | x 180.09 - 192.79, y 99.96 - 102.96 (12.70 x 3.00) | R1's plain tab, x 180.09 - 192.79, ends flush with R5's outer face | (186.44, 101.46, 109.00) | (186.44, 101.46, 112.00) |
| R5 | x 131.94 - 134.94, y 133.56 - 144.56 (3.00 x 11.00) | R4's -Z arm | (133.44, 139.44, 105.62) | (133.44, 139.06, 112.00) |
| R5 | x 192.67 - 195.67, y 133.56 - 144.56 (3.00 x 11.00) | R3's -Z arm | (194.17, 139.44, 105.62) | (194.17, 139.06, 112.00) |
| R6 | x 176.94 - 184.75, y 99.96 - 102.96 (7.81 x 3.00) | R1's latch pair: wedge finger x 176.94 - 179.51 and hooked finger x 180.51 - 184.88 (barb out to x 185.96 at z 172.20 - 173.25) | (180.91, 101.46, 175.58) | (180.85, 101.46, 169.20) |
| R6 | x 134.83 - 143.72, y 99.96 - 102.96 (8.89 x 3.00) | R1's plain tab, x 134.83 - 143.72, ends flush with R6's outer face | (139.28, 101.46, 172.20) | (139.28, 101.46, 169.20) |
| R6 | x 131.94 - 134.94, y 133.56 - 144.56 (3.00 x 11.00) | R4's +Z arm | (133.44, 139.44, 175.58) | (133.44, 139.06, 169.20) |
| R6 | x 192.67 - 195.67, y 133.56 - 144.56 (3.00 x 11.00) | R3's +Z arm | (194.17, 139.44, 175.58) | (194.17, 139.06, 169.20) |

- How far: the tips stand 6.38 mm out from each wall's inner face, so each wall is clear from 6.5 mm away. The last 5.75 mm is a snap fit (rigid
  overlap up to 1.2 mm at R1's barbs, 1.07 mm at R3's and R4's).
- Bottom edges: y 93.53 for both, which is B2's top face. R5 and R6 are the only turret parts that touch B2.
- R5 and R6 are not interchangeable: their R1 slots are in different places, and R6 is taller (top y 184.98 against 175.38).
- Other cut-outs in both, for the arm section: a servo window x 158.91 - 182.66, y 156.13 - 168.43 (23.75 x 12.30) and two 2.3 mm screw holes at
  (170.29, 152.95) and (170.29, 171.60); R6 also has a 2.8 mm hole at (139.41, 179.83).

**Order.** Forced by the geometry: R1 -> servo (with horn) -> R2 -> R3 and R4 (either first) -> R5 and R6 (either first); screws after B1 and B2. Not forced:
when B2 goes on (any time after the servo is in R1; the turret only touches it with the bottom edges of R5 and R6), and whether B1 goes under before
or after B2. The build notes' order (R1 - R6, then B2, then B1, then screws) is consistent with all of it. The present
`guide.py` follows this order except that it puts the servo into R2 first and brings the pair straight down onto R1, with the horn not shown until B2.
With the horn on the shaft a straight drop is impossible (see (a)); the servo has to go into R1 first by the tilting move, and R2 then comes down over it.
(Whether servo and R2 could make the tilting move together as a pair was not tested.)
