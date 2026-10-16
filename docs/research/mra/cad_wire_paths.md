# MRA: wire paths from the CAD

Written 13 Oct 2026 by the wire-path study. Data: `cad_wires.json` (same folder).
Pictures: `cad_wire_paths_side.png`, `cad_wire_paths_top.png`, `cad_wire_paths_R4_slot.png`, `cad_wire_paths_hook_slot.png`.
All coordinates are mm in the assembly space of `mra.glb` (Y up, as assembled). Ids are the CAD's top-level instances (`NAUOn`).
"Measured" = computed from the CAD geometry. Anything that is a guess says so.
Pin names (G / V / S, row numbers, joystick pin names, real jumper colours) are taken from the pin study, `cad_pins.md` / `cad_pins.json`;
they were not re-derived here.

STATUS: complete (sections 1 to 5). Open points are listed in section 7.

## Short answers

- Every wire in the CAD is a round swept tube. Servo conductors are 1.00 mm across (radius 0.5) and lie 1.02 mm apart in a flat
  ribbon; joystick jumper wires are 1.25 mm across (radius 0.625). 14 instances hold 44 tubes; all 44 centre lines are in `cad_wires.json`.
- The four servo leads, servo to shield (pieces meet end to end: the largest gap is 0.03 mm):

  | Servo | Pieces in order | Length (middle wire) | Plug on the shield | Row (cad_pins) |
  |---|---|---|---|---|
  | NAUO45 base servo | stub 3.0 -> NAUO87 (Part1) 168.1 -> cable of NAUO83 40.0 -> plug NAUO83 | 211.1 | NAUO83 | 5 |
  | NAUO58 arm servo, low z (student's left) | stub 3.0 -> NAUO88 (Part2) 200.4 -> cable of NAUO84 40.0 -> plug NAUO84 | 243.4 | NAUO84 | 6 |
  | NAUO66 arm servo, high z (student's right) | stub 3.0 -> NAUO89 (Part3) 234.9 -> cable of NAUO86 40.0 -> plug NAUO86 | 277.9 | NAUO86 | 9 |
  | NAUO72 claw servo | stub 0.5 -> NAUO94 (Part5) 268.3 -> plug NAUO90 -> coupler NAUO91 -> plug NAUO92 (22.1 straight through, no tube modelled) -> NAUO93 (Part4, twisted) 149.2 -> plug NAUO85 | 440.1 | NAUO85 | 10 |

- The base servo's lead leaves the servo body at (163.64, 119.11, 146.77) heading +z (to the student's right), loops back and goes out
  through the L-shaped slot in R4 (NAUO13) 54 mm along, at (133.44, 130.25, 143.46). The slot is cut in from R4's TOP edge: a 2.1 mm wide stem
  comes straight down from the top edge (z 140.6 to 142.7) and ends in an 8.5 x 8.1 mm pocket (y 127.26 to 135.76, z 140.61 to 148.71) that
  sticks out to the right (+z) as seen from the controller. The lead sits in the pocket. So a guide shows the lead being lowered into the
  mouth on the top edge, slid down the stem and moved across into the pocket.
- The claw lead's extension piece (NAUO93) goes out through the same pocket in R4, 299 mm along the claw chain.
- The two arm servos' leads each go through a hook-shaped slot in the front lug of a side plate: NAUO58's through NAUO15
  (engraved R5) at (123.54, 163.40, 110.50); NAUO66's through NAUO14 (engraved R6) at (123.53, 163.42, 170.70). Each hook opens forwards (-x)
  through the lug's front edge and then drops 10 mm.
- The claw lead also goes through one hole in ARA_C3 (NAUO34) and two holes in ARA_A11 (NAUO29), and its plugs join inside the turret
  in the coupler NAUO91.
- The joystick wires touch no wood at all: they run from the joystick pins up over the controller and down onto the shield in free air.
- Colours: with brown = G, red = V, orange = S and the shield columns from `cad_pins.md` (G at x 50.09, V at 52.57, S at 55.06), the
  conductor that ends on the plug contact at x = 49.98 is brown and the one at x = 55.06 is orange, in all four chains.
  **Every `across` rule in `materials.json` paints them the other way round at present** (orange at x 49.98), including the base
  servo stubs in the model that is built now. Section 5 has the detail.
- On the base and the two arm servos, brown comes out as the conductor on the side of the servo AWAY from its white label. On the claw
  servo the CAD's tubes arrive the other way round (brown on the label side). A real servo cannot differ like that, so the CAD's claw chain
  has a half-turn too many somewhere (the extension piece NAUO93 is a twisted lead with 10.5 turns). Section 5 says what to do about it.

## 1. Centre lines

### What was done

For each cable instance the mesh was welded (0.001 mm) and split into connected solids. For each solid:

1. The two flat round end faces were found (faces grouped across edges gentler than 50 degrees; an end face is a flat group whose rim is a
   circle to within 0.02 mm). The end point is the centre of the circle fitted to the rim; the radius comes from the same fit.
2. Every side triangle gives one point on the axis: its centroid moved inwards by the radius along the triangle's normal (the normal
   of a round tube always points straight away from its centre line).
3. Those axis points were put in order with the distance over the mesh from end a, then refined four times: project each point on
   the current line, average the points in 0.4 mm bins of arc length (weighted by triangle area; points more than 0.15 mm off dropped).
4. The fine line was thinned to points no more than 2.0 mm apart while staying within 0.02 mm of the fine line, so points are closer
   in bends (down to 0.1 to 0.8 mm in the tightest ones). Straight pieces were filled in so that no gap is over 2.0 mm.
5. Check: the distance of every vertex of the solid from the saved polyline, which should equal the radius.

The suggested "rings of vertices at equal graph distance" idea is used only for the ordering (step 3). The points themselves come
from the face normals: that does not need the vertices to lie in rings, and it still works on the one tube that cuts through itself.

### Result

| Instance | Solid | Radius | Length | End a | End b | Points | Tube vertices to centre line: min / mean / max |
|---|---|---|---|---|---|---|---|
| NAUO45 | 2 | 0.500 | 3.00 | (162.62, 119.11, 146.76) | (162.62, 119.11, 149.76) | 3 | 0.500 / 0.500 / 0.500 |
| NAUO45 | 3 | 0.500 | 3.00 | (163.64, 119.11, 146.76) | (163.64, 119.11, 149.76) | 3 | 0.500 / 0.500 / 0.500 |
| NAUO45 | 4 | 0.500 | 3.00 | (164.66, 119.11, 146.76) | (164.66, 119.11, 149.76) | 3 | 0.500 / 0.500 / 0.500 |
| NAUO58 | 3 | 0.500 | 3.00 | (181.58, 161.26, 92.85) | (184.58, 161.26, 92.85) | 3 | 0.500 / 0.500 / 0.500 |
| NAUO58 | 4 | 0.500 | 3.00 | (181.58, 162.28, 92.85) | (184.58, 162.28, 92.85) | 3 | 0.500 / 0.500 / 0.500 |
| NAUO58 | 5 | 0.500 | 3.00 | (181.58, 163.30, 92.85) | (184.58, 163.30, 92.85) | 3 | 0.500 / 0.500 / 0.500 |
| NAUO66 | 3 | 0.500 | 3.00 | (181.58, 161.26, 188.35) | (184.58, 161.26, 188.35) | 3 | 0.500 / 0.500 / 0.500 |
| NAUO66 | 4 | 0.500 | 3.00 | (181.58, 162.28, 188.35) | (184.58, 162.28, 188.35) | 3 | 0.500 / 0.500 / 0.500 |
| NAUO66 | 5 | 0.500 | 3.00 | (181.58, 163.30, 188.35) | (184.58, 163.30, 188.35) | 3 | 0.500 / 0.500 / 0.500 |
| NAUO72 | 3 | 0.500 | 0.50 | (334.38, 206.88, 132.84) | (334.38, 206.88, 132.34) | 2 | 0.500 / 0.500 / 0.500 |
| NAUO72 | 4 | 0.500 | 0.50 | (335.40, 206.87, 132.84) | (335.40, 206.87, 132.34) | 2 | 0.500 / 0.500 / 0.500 |
| NAUO72 | 5 | 0.500 | 0.50 | (336.42, 206.86, 132.84) | (336.42, 206.86, 132.34) | 2 | 0.500 / 0.500 / 0.500 |
| NAUO83 | 0 | 0.500 | 40.08 | (49.98, 120.97, 139.36) | (51.50, 160.96, 139.36) | 23 | 0.481 / 0.500 / 0.520 |
| NAUO83 | 1 | 0.500 | 39.99 | (52.52, 160.96, 139.36) | (52.52, 120.97, 139.36) | 22 | 0.500 / 0.500 / 0.500 |
| NAUO83 | 2 | 0.500 | 40.08 | (55.06, 120.97, 139.36) | (53.54, 160.96, 139.36) | 23 | 0.481 / 0.500 / 0.520 |
| NAUO84 | 0 | 0.500 | 40.08 | (49.98, 120.97, 142.11) | (51.50, 160.96, 142.11) | 23 | 0.481 / 0.500 / 0.520 |
| NAUO84 | 1 | 0.500 | 39.99 | (52.52, 160.96, 142.11) | (52.52, 120.97, 142.11) | 22 | 0.500 / 0.500 / 0.500 |
| NAUO84 | 2 | 0.500 | 40.08 | (55.06, 120.97, 142.11) | (53.54, 160.96, 142.11) | 23 | 0.481 / 0.500 / 0.520 |
| NAUO86 | 0 | 0.500 | 40.08 | (49.98, 120.97, 151.91) | (51.50, 160.96, 151.91) | 23 | 0.481 / 0.500 / 0.520 |
| NAUO86 | 1 | 0.500 | 39.99 | (52.52, 160.96, 151.91) | (52.52, 120.97, 151.91) | 22 | 0.500 / 0.500 / 0.500 |
| NAUO86 | 2 | 0.500 | 40.08 | (55.06, 120.97, 151.91) | (53.54, 160.96, 151.91) | 23 | 0.481 / 0.500 / 0.520 |
| NAUO87 | 0 | 0.500 | 168.22 | (51.50, 160.96, 139.39) | (162.62, 119.11, 149.76) | 111 | 0.477 / 0.500 / 0.522 |
| NAUO87 | 1 | 0.500 | 168.14 | (52.52, 160.96, 139.36) | (163.64, 119.11, 149.76) | 106 | 0.475 / 0.500 / 0.526 |
| NAUO87 | 2 | 0.500 | 168.25 | (53.54, 160.96, 139.33) | (164.66, 119.11, 149.76) | 105 | 0.474 / 0.500 / 0.525 |
| NAUO88 | 0 | 0.500 | 201.90 | (51.50, 160.96, 142.11) | (184.58, 163.30, 92.85) | 127 | 0.473 / 0.500 / 0.527 |
| NAUO88 | 1 | 0.500 | 200.39 | (52.52, 160.96, 142.11) | (184.58, 162.28, 92.85) | 125 | 0.458 / 0.500 / 0.538 |
| NAUO88 | 2 | 0.500 | 198.87 | (53.54, 160.96, 142.10) | (184.58, 161.26, 92.85) | 125 | 0.474 / 0.500 / 0.526 |
| NAUO89 | 0 | 0.500 | 240.33 | (51.50, 160.96, 151.89) | (184.58, 161.26, 188.35) | 151 | 0.467 / 0.500 / 0.533 |
| NAUO89 | 1 | 0.500 | 234.90 | (52.52, 160.96, 151.91) | (184.58, 162.28, 188.35) | 151 | 0.454 / 0.500 / 0.544 |
| NAUO89 | 2 | 0.500 | 229.54 | (53.54, 160.96, 151.93) | (184.58, 163.30, 188.35) | 142 | 0.467 / 0.500 / 0.532 |
| NAUO93 | 0 | 0.500 | 154.25 | (49.95, 116.29, 154.71) | (142.02, 133.62, 142.12) | 192 | 0.443 / 0.482 / 0.534 |
| NAUO93 | 1 | 0.500 | 155.77 | (55.11, 115.54, 154.62) | (141.56, 133.62, 147.20) | 209 | 0.385 / 0.482 / 0.540 |
| NAUO93 | 2 | 0.500 | 149.17 | (52.57, 115.89, 154.65) | (141.99, 133.62, 144.66) | 151 | 0.465 / 0.492 / 0.525 |
| NAUO94 | 0 | 0.500 | 271.59 | (336.42, 206.86, 132.34) | (163.58, 133.62, 147.20) | 178 | 0.475 / 0.500 / 0.525 |
| NAUO94 | 1 | 0.500 | 268.34 | (335.40, 206.87, 132.34) | (164.04, 133.62, 144.66) | 174 | 0.444 / 0.500 / 0.552 |
| NAUO94 | 2 | 0.500 (0.497 measured) | 265.05 | (334.38, 206.88, 132.34) | (164.85, 133.62, 142.12) | 209 | 0.397 / 0.494 / 0.583 |
| NAUO111 | 0 | 0.625 | 117.08 | (27.46, 124.23, 160.84) | (88.11, 115.97, 138.94) | 78 | 0.599 / 0.625 / 0.651 |
| NAUO111 | 1 | 0.625 | 115.10 | (27.46, 124.23, 163.34) | (88.11, 115.97, 141.48) | 78 | 0.586 / 0.625 / 0.658 |
| NAUO111 | 2 | 0.625 | 112.62 | (27.46, 124.26, 165.84) | (85.61, 115.97, 141.48) | 74 | 0.600 / 0.625 / 0.649 |
| NAUO111 | 3 | 0.625 | 110.95 | (27.46, 124.32, 168.34) | (83.13, 115.97, 141.48) | 80 | 0.598 / 0.625 / 0.650 |
| NAUO112 | 0 | 0.625 | 112.68 | (27.46, 124.23, 115.84) | (88.11, 115.97, 133.94) | 78 | 0.601 / 0.625 / 0.648 |
| NAUO112 | 1 | 0.625 | 110.59 | (27.46, 124.23, 118.34) | (88.11, 115.97, 136.48) | 78 | 0.553 / 0.625 / 0.661 |
| NAUO112 | 2 | 0.625 | 108.02 | (27.46, 124.23, 120.84) | (85.61, 115.97, 136.48) | 78 | 0.576 / 0.625 / 0.668 |
| NAUO112 | 3 | 0.625 | 106.03 | (27.46, 124.23, 123.34) | (83.13, 115.97, 136.48) | 74 | 0.601 / 0.625 / 0.649 |

"Solid" is the index of the connected solid inside the instance after welding, in this study's order. It is NOT the order
`build_model.py` or `cad_pins.json` use; match by end coordinates.

### How good the centre lines are (the check)

- Straight pieces (servo stubs, the middle wire of each plug cable): every vertex is exactly 0.500 from the line.
- Flat ribbon leads (NAUO87, 88, 89, the plug cables, NAUO94 solids 0 and 1) and the joystick wires: 98 % of vertices are within
  0.02 mm of the radius (that is the thinning tolerance). The worst single vertices are 0.056 under and 0.052 over on the servo leads
  (NAUO94 solid 1: 0.444 and 0.552) and 0.072 under, 0.043 over on the joystick wires (NAUO112 solid 1: 0.553; solid 2: 0.668).
  They are in the tightest bends.
- NAUO93 (Part4), the twisted lead: 0.385 to 0.540 (worst 0.115 under, on solid 1). Measured cause: the two outer wires wind
  10.45 times round the middle one (one turn every 14.3 mm, 1.0 to 2.7 mm from it), and each wire's end faces are tilted 20 to 30 degrees
  from its own centre line, so the tube's cross-section is not square to its centre line. The lines themselves are good to about 0.04.
- NAUO94 solid 2 (one outer wire of Part5): 0.397 to 0.583 (98 % within 0.473 to 0.516). This tube cuts through itself in the CAD: the
  mesh has 189 851 vertices (the other two have about 21 000), 11 370 edges shared by four or more triangles and 4 344 duplicate
  triangles. Its end ring at the servo is broken, so that end was taken from the 96 vertices lying in the end plane (circle fit: centre
  (334.384, 206.879, 132.335), radius 0.497). The centre line was fitted to the 78 % of the surface that is clean; it runs 1.02 mm
  beside the middle wire as it should.

**Worst case over all 44 tubes: 0.115 mm under the radius (NAUO93 solid 1) and 0.085 mm over (NAUO94 solid 2).**
Leaving out those two special pieces: 0.072 under, 0.052 over.

### Sizes worth knowing

- Servo ribbon: three wires, radius 0.5, centres 1.02 apart (3.04 wide by 1.0 thick overall).
- Plug cable (NAUO83, 84, 86, mesh `Cable_JR`): 40 mm long, straight up from the plug (y 120.97 to 160.96). The outer wires move
  sideways from 2.54 pitch at the plug (x 49.98, 52.52, 55.06) to 1.02 pitch (x 51.50, 52.52, 53.54) between y = 121.0 and about y = 134;
  above that the three are parallel.
- Plug body (mesh `JR-3`): 7.9 (across the three contacts) x 14.0 (long) x 2.75 (thick). Contacts (`JWT-CONTACT`): 2.0 x 10.0 x 2.2 boxes,
  inside the body from 1 mm short of the cable end to 3 mm short of the mating end.
- Joystick wire end caps (`Wire Cap`): 1.75 x 1.75 x 8.0.
- Coupler NAUO91 (`JR-3 Bridge`): box x 144.38 to 162.38, y 131.72 to 135.42, z 139.66 to 149.66; a sleeve with a 1 mm web in the middle
  (x 152.88 to 153.88) and an 8.5 mm deep socket each side.

## 2. Chains

Distances "s" are along the middle (V, red) conductor from the point where it leaves the servo body. G / V / S = the shield column
the conductor lands on (cad_pins: G x 50.09, V x 52.57, S x 55.06; the plug contacts are at x 49.98, 52.52, 55.06).
`across` = unit vector at the servo end from the G conductor to the S conductor.

### 2.1 Base servo NAUO45 -> plug NAUO83 (row 5)

| Piece | What | s from | s to | Gap before it |
|---|---|---|---|---|
| NAUO45 | lead stub on the servo body, 3.0 mm, straight along +z | 0.0 | 3.0 | - |
| NAUO87 (Part1) | routed lead | 3.0 | 171.14 | 0.000 (all three wires) |
| NAUO83 cable | 40 mm of cable moulded to the plug, straight down | 171.14 | 211.13 | 0.031 / 0.000 / 0.031 (G / V / S) |
| NAUO83 plug | contacts start where the cable ends (y 120.97) | 211.13 | - | 0 |

| Conductor | Solids (NAUO45 / NAUO87 / NAUO83) | At the servo | Side of the servo | At the plug (top of contact) | Length |
|---|---|---|---|---|---|
| G brown | 2 / 0 / 0 | (162.62, 119.11, 146.77) | away from the label | (49.98, 120.97, 139.36) | 211.30 |
| V red | 3 / 1 / 1 | (163.64, 119.11, 146.77) | middle | (52.52, 120.97, 139.36) | 211.13 |
| S orange | 4 / 2 / 2 | (164.66, 119.11, 146.77) | label side | (55.06, 120.97, 139.36) | 211.33 |

Leaves the servo at (163.64, 119.11, 146.77), direction (0, 0, 1). across = (1, 0, 0).
Plug NAUO83: body x 48.57 to 56.47, y 107.97 to 121.97, z 137.98 to 140.73. plug_position (centre of the face that goes onto the
pins) = (52.52, 107.97, 139.36); plug_direction (the way it moves to seat) = (0, -1, 0).

### 2.2 Arm servo NAUO58 (low z) -> plug NAUO84 (row 6)

| Piece | What | s from | s to | Gap before it |
|---|---|---|---|---|
| NAUO58 | stub, 3.0 mm, straight along +x | 0.0 | 3.0 | - |
| NAUO88 (Part2) | routed lead | 3.0 | 203.39 | 0.000 |
| NAUO84 cable | 40 mm of cable, straight down | 203.39 | 243.38 | 0.008 / 0.000 / 0.008 |
| NAUO84 plug | | 243.38 | - | 0 |

| Conductor | Solids (NAUO58 / NAUO88 / NAUO84) | At the servo | Side of the servo | At the plug | Length |
|---|---|---|---|---|---|
| G brown | 5 / 0 / 0 | (181.58, 163.30, 92.85) | away from the label | (49.98, 120.97, 142.11) | 244.97 |
| V red | 4 / 1 / 1 | (181.58, 162.28, 92.85) | middle | (52.52, 120.97, 142.11) | 243.38 |
| S orange | 3 / 2 / 2 | (181.58, 161.26, 92.85) | label side | (55.06, 120.97, 142.11) | 241.95 |

Leaves the servo at (181.58, 162.28, 92.85), direction (1, 0, 0). across = (0, -1, 0).
Plug NAUO84: body x 48.57 to 56.47, y 107.97 to 121.97, z 140.73 to 143.48. plug_position (52.52, 107.97, 142.11), plug_direction (0, -1, 0).

### 2.3 Arm servo NAUO66 (high z) -> plug NAUO86 (row 9)

| Piece | What | s from | s to | Gap before it |
|---|---|---|---|---|
| NAUO66 | stub, 3.0 mm, straight along +x | 0.0 | 3.0 | - |
| NAUO89 (Part3) | routed lead | 3.0 | 237.90 | 0.000 |
| NAUO86 cable | 40 mm of cable, straight down | 237.90 | 277.89 | 0.021 / 0.000 / 0.021 |
| NAUO86 plug | | 277.89 | - | 0 |

| Conductor | Solids (NAUO66 / NAUO89 / NAUO86) | At the servo | Side of the servo | At the plug | Length |
|---|---|---|---|---|---|
| G brown | 3 / 0 / 0 | (181.58, 161.26, 188.35) | away from the label | (49.98, 120.97, 151.91) | 283.41 |
| V red | 4 / 1 / 1 | (181.58, 162.28, 188.35) | middle | (52.52, 120.97, 151.91) | 277.89 |
| S orange | 5 / 2 / 2 | (181.58, 163.30, 188.35) | label side | (55.06, 120.97, 151.91) | 272.62 |

Leaves the servo at (181.58, 162.28, 188.35), direction (1, 0, 0). across = (0, 1, 0).
Plug NAUO86: body x 48.57 to 56.47, y 107.97 to 121.97, z 150.53 to 153.28. plug_position (52.52, 107.97, 151.91), plug_direction (0, -1, 0).

### 2.4 Claw servo NAUO72 -> coupler -> plug NAUO85 (row 10)

| Piece | What | s from | s to | Gap before it |
|---|---|---|---|---|
| NAUO72 | stub, 0.5 mm ("cut wires shorter"), along -z | 0.0 | 0.5 | - |
| NAUO94 (Part5) | routed lead, flat ribbon | 0.5 | 268.84 | 0.001 / 0.000 / 0.000 |
| NAUO90 plug | plain plug; the three wires end INSIDE it at x 164.85 / 164.04 / 163.58 (G / V / S), 3.0 to 4.3 mm in from its cable-end face x 167.88 | 268.84 | | wires overlap the plug, no gap |
| NAUO91 coupler | sleeve joining the two plugs (plug faces 1.0 mm apart: x 153.88 and 152.88) | | | - |
| NAUO92 plug | plain plug; the extension's wires start INSIDE it at x 142.02 / 141.99 / 141.56, 2.7 to 3.1 mm in from its cable-end face x 138.88 | | 290.89 | - |
| (no tube) | nothing is modelled between the wire ends in the two plugs: 22.83 / 22.05 / 22.03 mm straight along -x at y 133.62, z 142.12 / 144.66 / 147.20. The JSON chain bridges it with a straight line. | 268.84 | 290.89 | |
| NAUO93 (Part4) | extension lead, three wires twisted together (10.45 turns) | 290.89 | 440.06 | 0 (same y and z as the wire it continues, to 0.0001 mm) |
| NAUO85 plug | plain plug on the shield; the wires end INSIDE it at y 116.29 / 115.89 / 115.54, 5.7 to 6.4 mm below its cable-end face y 121.97 | 440.06 | - | wires overlap the plug |

| Conductor | Solids (NAUO72 / NAUO94 / NAUO93) | At the servo | Side of the servo | In the coupler (z) | At the plug | Length |
|---|---|---|---|---|---|---|
| G brown | 3 / 2 / 0 | (334.38, 206.88, 132.84) | LABEL side (see section 5) | 142.12 | (49.95, 116.29, 154.71) | 442.63 |
| V red | 4 / 1 / 2 | (335.40, 206.87, 132.84) | middle | 144.66 | (52.57, 115.89, 154.65) | 440.06 |
| S orange | 5 / 0 / 1 | (336.42, 206.86, 132.84) | away from the label | 147.20 | (55.11, 115.54, 154.62) | 449.90 |

Leaves the servo at (335.40, 206.87, 132.84), direction (0, 0, -1). across = (1.000, -0.011, 0).
Plug NAUO85: body x 48.57 to 56.47, y 107.97 to 121.97, z 153.28 to 156.03. plug_position (52.52, 107.97, 154.66), plug_direction (0, -1, 0).
Plug NAUO90: body x 153.88 to 167.88, y 132.25 to 135.00, z 140.71 to 148.61; mates towards -x. Plug NAUO92: body x 138.88 to 152.88,
same y and z; mates towards +x. Their contacts are in line (z 142.12, 144.66, 147.20), so the coupler joins them straight through.

## 3. Where each lead goes

Each lead was tested against every non-cable instance other than its own servo and plug (surface distance) and against every one
of the 44 wood plates (is the tube inside the plate's 3 mm thickness, and if so is it in a hole, in an open slot, or in the wood).
No lead is inside wood anywhere. No part comes within 2 mm of a lead except those listed below and, at the shield, the plugs next door
(the four plugs stand side by side).

Lead against lead (centre lines; the tubes are 1 mm thick, so 1.0 means touching): the base lead and the claw extension touch just in
front of R4, 1.04 apart at (132.0, 133.7, 142.4); the base lead and NAUO58's lead cross 1.78 apart above the shield at (61.8, 176.4, 140.4);
everything else is 7 mm or more apart until the plugs.

The long arcs between the turret and the shield are free air in the CAD (the modeller's sketch of a hanging lead); only the servo
exit, the slot or hole, and the plug are fixed places.

### 3.1 Base servo lead (NAUO45)

**Where it leaves the servo.** At (163.64, 119.11, 146.77), heading +z = (0, 0, 1). In the servo's own terms: out of the end face
nearest the output shaft, 4.7 mm from the face opposite the shaft, with the three wires side by side across the servo's width.
In the assembly the servo is shaft-down (the horn NAUO46 is below it), so the lead comes out near the TOP of the servo body (its top
face is y 123.85), from the face that looks towards +z (the student's right, towards side plate NAUO14, engraved R6). The exit is
inside the turret, 28.7 mm behind R4's inner face (x 134.94).

**The route (middle wire).**

| s | Point | What happens |
|---|---|---|
| 0 to 3 | (163.64, 119.11, 146.77) to (163.64, 119.11, 149.77) | stub, straight along +z |
| 3 to 20 | to (156.7, 120.5, 163.6) | carries on +z to z 163.7 (its furthest), turning towards -x |
| 20 to 50 | to (135.7, 128.7, 146.0) | runs back towards R4: forwards (-x), back to the left (-z), rising 8 mm |
| 48.7 to 59.6 | | within 1 mm of R4; closest at s 50.4, where the brown wire at (135.32, 127.78, 145.66) is 0.15 mm from the lower inside edge of the pocket (134.94, 127.25, 145.66) |
| 50.9 to 57.1 | | inside R4's thickness (x 131.94 to 134.94), in the pocket of the L-shaped slot |
| **54.0** | **(133.44, 130.25, 143.46)** | crosses the middle of R4, heading (-0.63, 0.50, -0.60) |
| 57 to 110 | (129.4, 133.9, 140.3) to (98.0, 172.1, 137.3) | climbs forwards at about 50 degrees, z steady at 137.4 |
| 110 to 171 | highest point (76.4, 182.7, 138.6) at s 135 | arcs over and comes down above the shield |
| 171.14 to 211.13 | (52.52, 160.96, 139.36) to (52.52, 120.97, 139.36) | the plug's cable, straight down into plug NAUO83 |

**In the slot.** Where the three wires cross the middle of R4 (x 133.44):

| Wire | Point | Gap from tube to nearest cut edge |
|---|---|---|
| G brown | (133.44, 129.03, 143.68) | 1.27 (the pocket floor, y 127.26) |
| V red | (133.44, 130.25, 143.46) | 2.36 |
| S orange | (133.44, 131.51, 143.21) | 2.11 |

The ribbon stands on edge there (its width is up and down, brown lowest), which is also how it has to go down the 2.1 mm stem.
From the middle wire the pocket has 3.0 mm of room below, 5.6 above, 2.9 to the left (-z) and 5.3 to the right (+z).

### 3.2 The L-shaped slot in R4 (NAUO13, CAD name `ARA_R4v2`)

R4 is the turret wall that faces the controller: a 3 mm plate, x 131.94 to 134.94, y 96.57 to 146.59, z 105.62 to 175.58.
The slot is cut right through the 3 mm and is part of the plate's outer outline, not a closed hole. Seen from the controller (looking
along +x; +z is to the right, y is up):

- **Mouth:** on the TOP edge of R4 (y 146.59). The stem is z 140.59 to 142.73 (2.13 wide); at the edge its corners are rounded off
  (radius about 1.1), so the opening on the edge itself is z 139.42 to 143.99. The plate's middle is z 140.60, so the mouth is just right of centre.
- **Stem:** straight down from the top edge. Its left wall (z 140.6) runs from the top edge down to the pocket floor; its right wall
  (z 142.73) runs from the top edge down to y 136.84, where it turns into the pocket's top edge. Stem length above the pocket: 10.8 mm.
- **Pocket (the foot of the L):** y 127.26 to 135.76 (8.50 high), z 140.61 to 148.71 (8.10 wide), corners rounded (radius about 1.1).
  It extends to the RIGHT (+z) of the stem. Its floor is 19.3 mm below the top edge.
- **It opens upwards** (+y), through the top edge. There is no opening to either side or downwards.
- **The mouth is not covered** in the finished model: no part comes within 3 mm of the line straight up from the mouth
  (x 133.44, z 141.66) for 38 mm above the top edge, and nothing stands within 12 mm in front of the pocket or 15 mm behind it (on the line through its centre). So the lead can
  be dropped in after the turret is complete.
- Overall box: y 127.26 to 146.59, z 139.42 to 148.71. Area 92 mm2. The back wall R3 (NAUO12) has the same outline box and no such slot (its
  area is 92 mm2 more than R4's).

Outline at mid-thickness, as (y, z), starting and ending on the top edge (26 points; the same list is in `cad_wires.json` under
`features.R4_L_slot.outline` with x = 133.44):

    (146.59, 143.99) (146.48, 143.46) (146.15, 143.03) (145.68, 142.77) (145.32, 142.72) (136.84, 142.73) (136.33, 142.92)
    (135.95, 143.31) (135.76, 143.81) (135.71, 147.72) (135.54, 148.14) (135.16, 148.52) (134.66, 148.71) (128.34, 148.71)
    (127.83, 148.52) (127.45, 148.14) (127.26, 147.63) (127.26, 141.69) (127.45, 141.18) (127.83, 140.80) (128.34, 140.61)
    (145.50, 140.59) (146.01, 140.40) (146.39, 140.02) (146.58, 139.51) (146.59, 139.42)

Picture: `cad_wire_paths_R4_slot.png`.

Two leads use the pocket in the CAD: the base servo lead (above) and the claw lead's extension NAUO93 (section 3.5), which crosses
at (133.44, 133.54, 144.91), above the base lead's wires. At the middle of R4 the nearest two wires are 2.36 apart centre to centre
(base orange and extension brown: 1.36 between the tubes); just in front of R4, at (132.0, 133.7, 142.4), the climbing base lead
brushes the extension (centres 1.04 apart, tubes 0.04 apart).

### 3.3 Arm servo NAUO58 (low z, student's left)

The servo sticks out through side plate NAUO15 (z 109 to 112); its lead end is outside the turret, so the lead has to come back in.

| s | Point | What happens |
|---|---|---|
| 0 to 3 | (181.58, 162.28, 92.85) to (184.58, 162.28, 92.85) | stub, straight along +x (towards the back) |
| 3 to 40 | furthest out (177.0, 162.3, 72.5) | a level U-turn (y stays 162.3) out to z 72.1, 20 mm outboard of the stub, coming round to head -x |
| 40 to 105 | (128.7, 162.9, 100.9) at s 100 | runs forwards and inwards, still level, outside the turret: 21 mm clear of R4's outline and 25 mm clear of R8's (NAUO17) |
| 107.7 to 114.3 | | within 1 mm of NAUO15. It touches the slot walls where it goes in and comes out: the brown wire at (124.63, 164.31, 108.78) is 0.03 mm from the back wall's corner (125.12, 164.31, 109.00) and the orange wire at (122.41, 162.51, 112.28) is 0.05 mm from the front wall's corner (121.94, 162.51, 112.00) |
| 108.9 to 113.0 | | inside the plate's thickness, in the drop of the hook-shaped slot |
| **110.9** | **(123.54, 163.40, 110.50)** | crosses the middle of NAUO15, heading (-0.45, 0.05, 0.89) |
| 113 to 203 | highest point (76.2, 178.1, 137.6) at s 170 | free air, up and over to the shield |
| 203.39 to 243.38 | (52.52, 160.96, 142.11) to (52.52, 120.97, 142.11) | the plug's cable, straight down into plug NAUO84 |

Wires at the middle of the plate (z 110.50): G (123.76, 164.40), V (123.54, 163.40), S (123.31, 162.41); stacked up and down, 0.85 to
1.07 mm clear of the slot walls each side.

**The hook-shaped slot** (NAUO15, CAD name `ARA_R6`, engraved R5 per `guide.py`; cut through z 109.0 to 112.0). It is in the lug that
sticks out of the front of the side plate above R4 (the lug's front edge is x 117.6; the lug spans y 150.8 to 175.4). Looking along -z (x to the right, y up):

- **Mouth:** on the lug's FRONT edge (x 117.66), between y 166.25 and 168.54 (2.29 wide; rounded corners make it y 165.45 to 169.36 on the edge itself).
- **Entry:** a level channel from the front edge back to x 121.9 (lower wall) / x 124.0 (upper wall).
- **Drop:** x 121.94 to 125.12 (3.18 wide), from y 168.52 down to a square-cornered floor at y 158.28 (10.24 long).
- **It opens forwards** (-x, towards the controller). The lead is in the drop, 5.1 mm above its floor.
- **The mouth is not covered** in the finished model: nothing comes within 3 mm of the line straight forward from the mouth for 22 mm
  (checked for both side plates).

Outline at mid-thickness as (x, y), from the lower corner of the mouth round to the upper corner (18 points; in the JSON as
`features.R5_hook_slot.outline` with z = 110.5):

    (117.66, 165.45) (117.89, 165.84) (118.32, 166.16) (118.85, 166.28) (120.94, 166.25) (121.36, 166.08) (121.74, 165.70)
    (121.93, 165.19) (121.94, 158.28) (125.12, 158.28) (125.11, 167.44) (124.92, 167.95) (124.54, 168.33) (124.03, 168.52)
    (118.58, 168.56) (118.16, 168.73) (117.78, 169.11) (117.66, 169.36)

Picture: `cad_wire_paths_hook_slot.png`.

### 3.4 Arm servo NAUO66 (high z, student's right)

The mirror image: the servo sticks out through side plate NAUO14 (z 169.2 to 172.2).

| s | Point | What happens |
|---|---|---|
| 0 to 3 | (181.58, 162.28, 188.35) to (184.58, 162.28, 188.35) | stub, straight along +x |
| 3 to 100 | highest point (154.8, 195.9, 205.1) at s 72; furthest out z 206.9 | unlike NAUO58's, this loop climbs: up and outboard (to y 196, z 207), then forwards |
| 100 to 133 | (123.8, 175.4, 181.2) at s 120 | comes down and inwards towards the front lug of NAUO14 |
| 132.9 to 140.3 | | within 1 mm of NAUO14; closest at s 137.4: the orange wire at (122.89, 163.23, 169.38) is 0.45 mm from the slot's front wall (x 121.94) |
| 133.5 to 139.0 | | inside the plate's thickness, in the drop of the hook-shaped slot |
| **136.3** | **(123.53, 163.42, 170.70)** | crosses the middle of NAUO14, heading (0.00, -0.71, -0.71) |
| 139 to 238 | lowest (122.0, 155.3, 159.7) at s 150; then up to (71.0, 177.3, 151.2) at s 210 | dips to y 155 inside, then up and over to the shield |
| 237.90 to 277.89 | (52.52, 160.96, 151.91) to (52.52, 120.97, 151.91) | the plug's cable, straight down into plug NAUO86 |

Wires at the middle of the plate (z 170.70): G (124.16, 162.29), V (123.53, 163.41), S (122.91, 164.58); 0.46 to 1.08 mm clear.
The hook-shaped slot in NAUO14 (CAD name `ARA_R5`, engraved R6 per `guide.py`; cut through z 169.2 to 172.2) has exactly the same
outline as the one in NAUO15, at the same x and y (`features.R6_hook_slot`).

### 3.5 Claw servo lead (NAUO72)

| s | Point | What happens |
|---|---|---|
| 0 to 0.5 | (335.40, 206.87, 132.84) to (335.40, 206.87, 132.34) | stub, along -z, towards claw side plate ARA_C2 (NAUO33) |
| 1.6 to 6.9 | closest at s 3.6: (334.60, 209.40, 130.57) | turns up within 1 mm of C2's inner face (z 129.55); tube 0.52 mm from it |
| 0.5 to 50 | highest point (317.9, 217.2, 135.8) at s 23 | up and back over the claw servo, then down |
| 55.4 to 59.3; **57.2** | **(300.77, 195.09, 147.06)**, heading (-0.35, -0.94, 0.03) | down through a hole in ARA_C3 (NAUO34) |
| 60 to 140 | (291.2, 187.7, 147.9) at s 70; (236.0, 209.8, 144.6) at s 130 | under C3, then back along the forearm, climbing with it, z about 144.5 (the middle between the arm sides) |
| 142.2 to 146.3; **144.2** | **(222.76, 214.43, 144.50)**, heading (-0.95, 0.32, 0.01) | through the first hole in ARA_A11 (NAUO29), near the elbow |
| 150 to 200 | (200.9, 204.2, 144.5) at s 170 | down along the upper arm |
| 202.5 to 207.2; **204.9** | **(186.71, 174.50, 144.49)**, heading (0.22, -0.98, 0.00) | back through the second hole in ARA_A11 |
| 207 to 245 | (190.1, 159.5, 144.5) at s 220 | straight down inside the turret, just in front of the back wall R3 (NAUO12, inner face x 192.67); closest at s 233.3, where the brown wire at (191.20, 146.54, 143.63) is 0.98 mm from it |
| 245 to 265 | (182.6, 133.7, 144.7) at s 250 | turns forwards (-x) at y 133.6 |
| 268.84 to 290.89 | (164.04, 133.62, 144.66) to (141.99, 133.62, 144.66) | plug NAUO90, coupler NAUO91, plug NAUO92, in a straight line along -x (plug bodies span x 167.88 down to 138.88) |
| 297.5 to 301.3; **299.4** | **(133.44, 133.54, 144.91)**, heading (-1.00, 0.00, 0.07) | out through the pocket of R4's L-shaped slot (the twisted extension NAUO93) |
| 301 to 400 | highest (72 to 78, 167.0, 151) at s 370 to 380 | free air, up and over to the shield |
| 400 to 440.06 | to (52.57, 115.89, 154.65) | down into plug NAUO85 |

The holes:

| Part | Hole | Centre | Size | Wires at mid-thickness, gap to the hole edge |
|---|---|---|---|---|
| ARA_C3 (NAUO34), plate about y 193.6 to 196.6 at this x (its normal is (0.011, 1.000, 0)) | rectangular, closed | (300.78, 195.09, 147.06) | 6.34 along x by 10.00 along z | G (301.63, 195.08, 146.45) 1.82; V 2.66; S (299.90, 195.10, 147.67) 1.79 |
| ARA_A11 (NAUO29), the cross plate between the arm sides, normal (0.74, -0.67, 0) | square, closed, nearer the claw | (222.76, 214.43, 144.49) | 8.00 x 8.00, rounded corners | G (222.25, 213.87, 143.76) 2.74; V 3.50; S (223.27, 215.00, 145.23) 2.74 |
| ARA_A11 (NAUO29) | square, closed, nearer the turret | (186.70, 174.50, 144.49) | 8.00 x 8.00 | G (187.05, 174.88, 143.56) 2.57; V 3.50; S (186.37, 174.13, 145.43) 2.57 |
| R4 (NAUO13) | the L-shaped slot's pocket (section 3.2) | | | G (133.44, 133.67, 142.27) 1.16; V (133.44, 133.54, 144.91) 1.71; S (133.44, 133.08, 146.58) 1.63 |

The lead goes through the exact centre of each closed hole (the modeller aimed the path at the hole centres).
C2, C3 and A11 are CAD file names; their engraved codes were not checked here.

## 4. Joystick bundles NAUO111 and NAUO112

Each bundle is four separate wires, radius 0.625. Every wire end sits exactly on the end face of a cap (gap 0.000 mm, on the cap's
axis to within 0.09 mm). Joystick-side caps lie along x (x 19.46 to 27.46; the wire leaves the +x end heading +x). Shield-side caps
stand along y (y 107.97 to 115.97; the wire enters the top heading -y). Centre lines are in `cad_wires.json` under `joystick_wires`
(ordered joystick end first) and under `NAUO111` / `NAUO112`.

| Bundle | Solid | Length | Joystick end | Cap there | Joystick pin (cad_pins) | Shield end | Cap there | Shield pin (cad_pins) | Real wire colour (cad_pins) |
|---|---|---|---|---|---|---|---|---|---|
| NAUO111 | 0 | 117.09 | (27.46, 124.23, 160.84) | NAUO110 | NAUO81 VRy | (88.11, 115.97, 138.94) | NAUO98 | A1 S | orange |
| NAUO111 | 1 | 115.10 | (27.46, 124.23, 163.34) | NAUO109 | NAUO81 VRx | (88.11, 115.97, 141.48) | NAUO95 | A0 S | red |
| NAUO111 | 2 | 112.62 | (27.46, 124.26, 165.84) | NAUO108 | NAUO81 +5V | (85.61, 115.97, 141.48) | NAUO96 | A0 V | brown |
| NAUO111 | 3 | 110.96 | (27.46, 124.32, 168.34) | NAUO103 | NAUO81 GND | (83.13, 115.97, 141.48) | NAUO97 | A0 G | black |
| NAUO112 | 0 | 112.68 | (27.46, 124.23, 115.84) | NAUO107 | NAUO80 VRy | (88.11, 115.97, 133.94) | NAUO102 | A3 S | purple |
| NAUO112 | 1 | 110.59 | (27.46, 124.23, 118.34) | NAUO106 | NAUO80 VRx | (88.11, 115.97, 136.48) | NAUO101 | A2 S | blue |
| NAUO112 | 2 | 108.03 | (27.46, 124.23, 120.84) | NAUO105 | NAUO80 +5V | (85.61, 115.97, 136.48) | NAUO100 | A2 V | green |
| NAUO112 | 3 | 106.03 | (27.46, 124.23, 123.34) | NAUO104 | NAUO80 GND | (83.13, 115.97, 136.48) | NAUO99 | A2 G | yellow |

The cap-to-cap pairing was measured here and agrees with `cad_pins.json` wire for wire; the pin names and real colours are from there.

Route (all eight are alike): out of the joystick cap heading +x at y 124.2 for about 20 mm, up and forwards (x 55 to 67, y 129 to 155),
over the top at y 153.9 to 157.2 near x 71 to 73, then down onto the shield header. They touch nothing: no wood plate and no other
part comes within 2 mm, except their own caps. Bundle NAUO112 (left joystick) passes over the left B6 wall (NAUO5, z 128.6 to 131.6) at
about (73.5, 153.7, 130.3), some 40 mm clear of the wall's outline there; bundle NAUO111 (right joystick) passes over the right B6 wall
(NAUO6, z 150.0 to 153.0) near (75.7, 156.6, 150.7).

## 5. Colours

### Which conductor is which

A servo lead is brown = ground (G), red = power (V), orange = signal (S). Red is the middle wire. The shield's digital-side columns
(from `cad_pins.md`, read off the real board in the video) are G at x = 50.09 (board edge, joystick side), V at 52.57, S at 55.06
(nearest the Nano). So, following each tube from the plug back to the servo:

| Chain | Brown (G) at the plug | Brown at the servo | Orange (S) at the plug | Orange at the servo |
|---|---|---|---|---|
| NAUO45 base | x 49.98 | x 162.62, the -x wire (the one nearer R4); servo side away from the label | x 55.06 | x 164.66, the +x wire; label side |
| NAUO58 low z | x 49.98 | y 163.30, the upper wire; away from the label | x 55.06 | y 161.26, the lower wire; label side |
| NAUO66 high z | x 49.98 | y 161.26, the lower wire; away from the label | x 55.06 | y 163.30, the upper wire; label side |
| NAUO72 claw | x 49.95 | x 334.38, the -x wire; LABEL side | x 55.11 | x 336.42, the +x wire; away from the label |

"Label side" is measured in the servo mesh's own frame: the white label plate is on the mesh's +z face; the three stubs are at
mesh z = -1.02, 0, +1.02.

`cad_pins.json` (`servo_leads`) reached the same G / V / S assignment for the far ends of Part1, Part2, Part3 and Part4 independently.

### The claw chain does not agree with the other three

The base and both arm servos have brown on the side away from the label. The claw servo comes out with brown on the label side.
All four are the same servo, so the CAD's claw chain swaps the outer wires once too often between servo and shield. The CAD cannot
say where: in the flat lead NAUO94, or in the twisted extension NAUO93, whose outer wires make 10.45 turns (about half a turn more
than a whole number). What a guide should do (a recommendation, not a measurement):

- Colour the extension NAUO93 from the shield end (brown on G). That is the end the student is told about.
- Colour the servo's own lead NAUO94 so that it matches the extension where the two plugs meet in the coupler (brown to brown): that
  joint is what the student looks at. In CAD-tube terms that is NAUO94 solid 2 = brown, solid 1 = red, solid 0 = orange.
- The price is the 0.5 mm stub on the claw servo, which then has brown on the label side, unlike the other servos. It is too short
  to see. (If the three stubs on NAUO72 are painted by the same rule as the other servos, `build_model.py` will report a colour break
  between NAUO72 and Part5; give `MG90S_Cut wires shorter` its own rule with the order reversed, or leave its stubs unpainted.)

### The present rules in `materials.json` are all the other way round

`materials.json` (as of 13 Oct 20:53) says in its notes that the outer colours were worked out with "_B read as the G row, _N as the
S row". `cad_pins.md` found the opposite from the legends on the real board (_N = G at x 50.09, _B = S at x 55.06). Reproducing
`build_model.py`'s `order_leads()` for every lead mesh and following the tubes gives:

| Mesh (instances) | `across` now | Paints (in `order_leads` order) | Should be |
|---|---|---|---|
| `MG90S` (NAUO45, 58, 66) | orange, red, brown | orange on the wire away from the label | brown, red, orange |
| `MG90S_Cut wires shorter` (NAUO72) | same rule | nothing: the size filter `long: [2, 4]` misses the 0.5 mm stubs, so they take the servo body colour | see the note above |
| `Part1^ARA_Pathways` (NAUO87) | orange, red, brown | orange on the wire that lands on G | brown, red, orange |
| `Part2^ARA_Pathways` (NAUO88) | orange, red, brown | orange on G | brown, red, orange |
| `Part3^ARA_Pathways` (NAUO89) | brown, red, orange | orange on G | orange, red, brown |
| `Part4^ARA_Pathways` (NAUO93) | orange, red, brown | orange on G | brown, red, orange |
| `Part5^ARA_Pathways` (NAUO94) | orange, red, brown | orange on the wire that continues into Part4's G wire | brown, red, orange |
| `Cable_JR` (NAUO83, 84, 86) | brown, red, orange | orange on the contact at x 49.98 | orange, red, brown |

So the rules are consistent with each other (no colour changes along a chain, including through the coupler), but every one has
brown and orange exchanged against "brown to G". Swapping brown and orange in each `across` list fixes all of them at once.
The model that is built now (`model.report.json`: 44 parts kept, `MG90S` lead_order orange, red, brown) shows the base servo's stubs
with orange at x 162.62 and brown at x 164.66; by the chain they should be brown at x 162.62 and orange at x 164.66.
This rests on the pin study's reading of the board (G at the board edge). If Lee confirms that reading, the swap is right.

Not from the CAD: which side of a real MG90S the brown wire is on was not checked. The CAD puts it away from the label on three
servos out of four; confirm on a real servo before relying on the servo end.

### Joystick wires (for completeness)

The present rule paints Part6 and Part7 yellow, green, blue, purple in order of rising z at the joystick. Against the real colours
recorded in `cad_pins.json`: the left joystick's bundle NAUO112 is reversed (painted yellow on VRy, real yellow is GND; real order from
low z is purple, blue, green, yellow), and the right joystick's bundle NAUO111 is really orange, red, brown, black from low z
(VRy, VRx, +5V, GND), not the yellow-to-purple set at all.

## 6. What is in `cad_wires.json`

| Key | Contents |
|---|---|
| `_about` | units and definitions |
| `NAUO45`, `58`, `66`, `72`, `83`, `84`, `86`, `87`, `88`, `89`, `93`, `94`, `111`, `112` | list of conductors: `solid`, `mesh`, `radius_mm`, `length_mm`, `end_a`, `end_b`, `n_points`, `points`, `check` (min / p01 / mean / p99 / max distance of the tube's vertices from the line). This is the shape `tools/wires.py load_centrelines()` expects. |
| `chains` | per servo id: `pieces`, `piece_roles`, `piece_ranges_mm`, `middle` (the middle wire from servo body to plug, one polyline), `length_mm`, `across`, `leaves_servo_at`, `leaves_servo_direction`, `plug`, `plug_position`, `plug_direction`, `plug_centre`, `plug_box`, `plug_cable_end`, `conductors` (G, V, S in that order: colour, both ends, the solids it is made of with the gap before each, its own full polyline `points`, which side of the servo), `passes` (slots and holes, in order, with distances, points, heading, the three wires' positions and the cut outline), `comes_near` (parts within 2 mm) |
| `plugs` | NAUO83, 84, 85, 86, 90, 92: box, centre, mating face centre and direction, cable-end face centre, the three contact boxes |
| `coupler` | NAUO91 box |
| `joystick_wires` | the eight wires, joystick end first, with the cap at each end and the caps' boxes |
| `caps` | NAUO95 to NAUO110: box, centre, axis |
| `features` | `R4_L_slot`, `R5_hook_slot`, `R6_hook_slot`: outline points, mouth, stem / drop, pocket, which way it opens |
| `colour_rule_check` | the table in section 5 as data |

`across` is chosen so that `tools/wires.py ribbon(middle, across, pitch=1.02)` returns the wires in the order G, V, S (brown, red, orange).
Give it `pitch=1.02`: that is the CAD's spacing; the function's default of 1.27 is wider than the CAD ribbon (checked: with the
base chain it returns the three wires at x 162.37 / 163.64 / 164.91 at the default pitch, against 162.62 / 163.64 / 164.66 in the CAD).
`ribbon()` carries the ribbon along without twisting, which is not what the CAD tubes do everywhere; the true wire lines are in
`chains[...].conductors[...].points`.

## 7. Limits and open points

1. G / V / S and the row numbers come from `cad_pins.md`. If that reading of the board changes, the colours here flip with it; the
   geometry does not.
2. Which side of a real MG90S carries the brown wire was not established. The CAD is not consistent about it (three servos one way,
   the claw servo the other).
3. Engraved codes of the arm and claw parts on the claw lead's route (CAD names ARA_C2, ARA_C3, ARA_A11) were not checked. R4, R5, R6
   follow `guide.py` (NAUO13 = R4, NAUO15 = engraved R5, NAUO14 = engraved R6).
4. The free-air arcs between turret and shield are the CAD modeller's drawing, not a measurement of a real kit. In the CAD they rise
   to y 167 (claw extension), 177 and 178 (arm servos) and 183 (base servo), 45 to 60 mm above the tops of the shield plugs.
5. The CAD routes the arm servo leads with a 20 mm loop outboard of each servo before they come back to the hook slots, and the base
   lead with a loop out to z 163.7 before R4. Whether a real lead is long enough to be dressed like that was not checked (CAD chain
   lengths: 211, 243, 278 mm; claw 269 mm to the coupler plus a 149 mm extension).
6. The claw lead's plug-to-plug joint is modelled as two socket plugs in a sleeve with no pins between them; the real part is
   presumably a servo extension lead (a guess).
7. No lead was found inside wood, but three places are tight: NAUO58's lead touches the walls of its hook slot (0.03 and 0.05 mm), the
   base lead's brown wire clears the lower inside edge of R4's pocket by 0.15 mm, and NAUO66's orange wire clears its hook slot by 0.45 mm.
   (These gaps were sampled every 0.5 mm along the wire, so they are good to a few hundredths.) The base lead and the claw extension
   also touch each other just in front of R4 (section 3.2).

Scratch scripts and intermediate files for this study are in the session scratchpad under `research_r2/cad_wires/`
(`centre.py` = the centre-line method, `plates.py` = plate outlines, `s12_json.py` = writes the JSON).
