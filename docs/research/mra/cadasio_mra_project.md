# TechBox's own Cadasio project for the MRA: colours, names and look

Status: complete (2026-10-13).

- Source: `scratchpad/mra_cadasio/19075-mini_robot_armmra.json`, the getProjectViewer payload of the private project
  "Mini Robot Arm(MRA)" (id `beab9584-dba1-46f5-a330-2e9daac36ec1`, company 19075, status "published", publish version 1,
  SolidWorks add-in 1.0.7.339, CAD upload version 7 of 12 Oct 2026). It holds ONE step, named "Step 10".
- Companion data: `cadasio_mra_colours.json` (same folder): the colour of every solid, as atlases keyed by our mesh names.
- Evidence pictures (same folder): `cadasio_mra_servo_label.png`, `cadasio_mra_engraved_codes_1.png`, `cadasio_mra_engraved_codes_2.png`.
- Working scripts and caches: `scratchpad/research_r2/cadasio_project/` (`scripts/`, `tree.json`, `ours.json`, `partmatch.json`,
  `solidmatch.json`, `ourcolours.json`, `skins.json`).
- Not done: the step's saved picture was not downloaded (no browser or network use in this task). Everything below is read from
  the payload's data and from our own CAD, not from a rendering. Where I say how something "shows", that is worked out from the data.

Coordinates are millimetres. "Assembly space" is the frame of `mra.glb` x 1000 (Y up); the Cadasio assembly uses the same frame
(checked: every part lands on ours). "Mesh coordinates" are a mesh's own coordinates in `mra.glb` x 1000, which is what
`tools/build_model.py` works in. "Solid N" of a mesh is the N-th connected solid as `build_model.py` numbers them
(`weld_positions` at 0.001 mm, then `split_components`).

## 0. Short answers

1. **The project matches our CAD exactly.** 112 top-level instances = NAUO1..NAUO112, one to one; 185 parts = our 185 mesh nodes;
   every relative rotation is a multiple of 90 degrees. Nothing is hidden and nothing is moved: the one step shows the whole kit assembled.
2. **Colours.** Cadasio shows 34 distinct colours. Wood (`#deb887`), engraving (`#1e1616`) and screws (`#a6a9aa`) are what we already
   use. Almost everything else differs from ours: see section 2.3. The colour file gives all of it per solid and reproduces 550 of 550
   solids when fed back through `colour_from_atlas`.
3. **Lee's five points**, exactly as Cadasio has them (details and solids in 2.2):
   - (a) regulator on the shield: body `#181818`, its two pin faces `#a6a9aa`, six small marks on top `#cccecc`;
   - (b) the 30 solder mounds and the 30 pin tops on the Nano: `#a6a9aa`;
   - (c) mini-USB: shell `#cccccc`, inner core `#a6a9aa`, five contacts `#d3d6d3`. **Cadasio does not make the shell the same silver as
     the pins**; making it so is a TechBox decision (it would be `#a6a9aa`);
   - (d) joystick header: ten pin solids `#a6a9aa`, plastic bar `#303030`;
   - (e) servo: label plate `#ff00ff`, white (`#ffffff`) lettering "Tower Pro / MG90S / Micro servo" inside a white frame, horns `#1a1a1a`.
4. **Most of these are "skins".** A Cadasio body named `...Surface-Offset...` is a zero-thickness copy of some faces of a solid, made so
   that those faces can carry their own colour. In our meshes each is an open shell within 0.05 mm of the solid under it. The solder
   cones are part of the Nano BOARD solid, the regulator's pins are part of its BODY solid, and so on. Colouring the skin alone is not
   enough; the faces under it must take the skin's colour too (the `"skin": true` treatment `build_model.py` already has).
5. **Servo leads are the other way round in our model.** In Cadasio, on all four servos and end to end, brown lands on the header row
   named `_N` (on the servo side of the board, the row nearest the edge), red on `_R`, orange on `_B`. Ours has brown and orange swapped everywhere.
6. **Names.** The project carries 12 tooltip texts and nothing else (no selection sets, no meta values, no renamed parts):
   Base / Shoulder / Elbow / Claw Motor, Joystick, Nano, Nano I/O Module, 6mm / 10mm / 16mm Hex Screw, Servo Extension Wire,
   Breadboard Wire (F-F). Wood parts have no tooltip. Proposed names for all 112 parts are in the table in 1.4.
7. **Engraved codes differ from CAD names on 26 of the 44 wood parts** (read from our CAD's engraving geometry; the same reading was
   made independently in `cad_codes_base.md`). The arm is engraved A1 to A13 (A9 twice), the claw has C4 to C8 shuffled, and the four
   `TB_` parts are engraved T1 and T2. Table in 1.4, pictures in the two `engraved_codes` files.
8. **Look.** Same recipe as the 20 published guides: every solid `toon` with `normal` edges, crease angle 40, black edges of width 1,
   white background, ambient light x 2, directional x 1, light not following the camera, 45 degree perspective lens. Numbers in section 4.

## 1. What the payload is and how it was read

### 1.1 Structure

| Thing | Value |
|---|---|
| Units | `assemblyStructure.scaleFactor` = 0.23716660223956862 scene units per mm (3 mm wood is 0.7115 units) |
| Tree | 1030 nodes: 1 root (`ARA_Pathways`), 112 top-level instances, 185 parts, 829 bodies. 15 sub-assembly nodes (joystick, shield, plugs) |
| Leaves (things with a colour) | 917: 829 bodies of multi-body parts + 88 single-body parts |
| Hidden nodes | none |
| Steps | 1 ("Step 10", behaviour `pause`, 800 ms, fade / tween); `stepNumber` "12" at project level (the editor's counter, I think) |
| Annotations (lead lines, labels, images) | none (`toolboxComponentsProperties` is empty) |
| Geometry | not in the payload (`versionData` is null; only boxes, areas and colours) |
| Colour of a leaf | the nearest `colour_main` set in the step on it or an ancestor, else the SolidWorks colour (`versionMtlData` Kd) |

Two things about the tree that are easy to get wrong (both checked on all 917 leaves):

- A **single-body part** (for example a screw, `M3x6mm-7`) is a leaf whose box is in its own coordinates and whose transform is its
  real placement.
- A **body of a multi-body part** (for example `ARA_B8-1/ARA_B8-Cut-Extrude1`) is a leaf whose box is in its PARENT part's coordinates,
  and whose "transform" is only a pivot: identity rotation, translation = the centre of its box (true for all 829 bodies). Applying
  that transform to the box puts everything in the wrong place.

The step's 116 `position` entries are not movements. Compared with each body's pivot they are nudges of 0.005 to 0.23 mm along the
face normal: the author pulled coincident surfaces apart so that they do not flicker. 104 are on `Surface-Offset` bodies (the wood
engravings by a median of 0.08 mm; on each servo three lettering bodies pushed in by 0.05 to 0.23 mm, see 2.2 e), 4 are the servo
label plates (pushed in by 0.02 to 0.04 mm), 4 are the potentiometer bodies (0.02 mm). The other four look like slips of the mouse:
`Shield_Arduino NANO-1` by (0.02, -0.01, -0.11) mm, `M3x10mm-6` by 0.07 mm, `TB_TopBot-Cut-Extrude1` by 0.01 mm and one lead stub
of the claw servo by 0.005 mm.

### 1.2 What a "Surface-Offset" body is

514 of the 829 bodies are named `<part>-Surface-Offset<n>[k]`. They are zero-thickness (or shell) copies of faces of a solid in the
same part, made in SolidWorks so that Cadasio, which colours whole bodies, can colour those faces separately: the engraved characters
on the wood, the lettering on the servo label, the yellow base of each pin header, and on the electronics every pin, lead, pad and
solder mound.

In our CAD export the same surfaces exist. I tested every solid of every multi-solid mesh: every solid that corresponds to a
`Surface-Offset` body is an open shell lying within 0.05 mm of another solid of the same mesh, and no other solid is. 238 of the
Nano's 273 solids are such skins.

### 1.3 Matching to our CAD

- Parts: Cadasio's component name plus configuration is our mesh name (`MG90S [Cut wires shorter]` = `MG90S_Cut wires shorter`,
  `nano [Varsayılan]` = `nano_Varsayılan`, `M3x6mm [91292A111]` = `M3x6mm_91292A111`). Parts of the same name were paired by world box
  (Hungarian assignment). Worst box mismatch: 3.95 mm on the joystick thumb cap (Cadasio's box for that one body is longer than the
  mesh in one axis), then 0.97 mm on a wire bundle, everything else under 0.25 mm.
- Instances: every Cadasio top-level instance maps to exactly one NAUO id and the other way round (table in 1.4).
- Solids: Cadasio's body boxes were carried into our mesh coordinates through the relative transform (always a 90 degree rotation, so
  boxes stay exact) and paired with our connected solids by box. Of our 660 solids (all 185 mesh nodes), 641 pair within 0.6 mm (sum of the six face
  offsets) and 583 within 0.02 mm. The other 19 are 10 wire tubes (the box of a swept tube differs by up to 1.2 mm between our
  tessellated tube and Cadasio's exact one; each bundle still pairs one to one), the two thumb caps, and seven solids of ours that
  are several Cadasio bodies welded together or have no Cadasio body of their own (2.3, "merged").
- Bodies Cadasio has that are not separate solids in our meshes (they are in the JSON with `"solid": null`): the wood engraving
  surfaces (in ours the engraving is a pocket in the one wood solid), the 28 lettering surfaces of each servo label (welded into the
  label solid), 16 resistor-pack terminals, the mini-USB core, the reset shell and two programming-header strips on the Nano, the four
  legs of the joystick's switch, four flat marks on each potentiometer, and the four 3.5 mm corner pads on each joystick board.

### 1.4 The 112 instances

"Engraved" is the code cut into the wood, read from our CAD (how: section 3.2). "Proposed name" is discussed in section 3.3.

| id | Cadasio instance | our mesh(es) | centre (mm) | Cadasio tooltip | engraved | proposed name |
|---|---|---|---|---|---|---|
| NAUO1 | `ARA_B1-1` | `ARA_B1` | 94, 89, 141 | - | B1 | B1 |
| NAUO2 | `ARA_B2-1` | `ARA_B2` | 94, 92, 141 | - | B2 | B2 |
| NAUO3 | `ARA_B4-1` | `ARA_B4` | 70, 100, 142 | - | B4 | B4 |
| NAUO4 | `ARA_B5-1` | `ARA_B5` | 28, 115, 107 | - | B5 | B5 |
| NAUO5 | `ARA_B6-1` | `ARA_B6` | 40, 115, 130 | - | B6 | B6 |
| NAUO6 | `ARA_B6-2` | `ARA_B6` | 40, 115, 152 | - | B6 | B6 |
| NAUO7 | `ARA_B8-1` | `ARA_B8` | 3, 115, 175 | - | B7 | B7 |
| NAUO8 | `ARA_B9-1` | `ARA_B9` | 3, 136, 141 | - | B8 | B8 |
| NAUO9 | `ARA_B10-1` | `ARA_B10` | 3, 114, 141 | - | B3 | B3 |
| NAUO10 | `ARA_R1-1` | `ARA_R1` | 164, 102, 141 | - | R1 | R1 |
| NAUO11 | `ARA_R2-1` | `ARA_R2` | 164, 132, 131 | - | R2 | R2 |
| NAUO12 | `ARA_R3v2-1` | `ARA_R3v2` | 194, 122, 141 | - | R3 | R3 |
| NAUO13 | `ARA_R4v2-1` | `ARA_R4v2` | 133, 122, 141 | - | R4 | R4 |
| NAUO14 | `ARA_R5-1` | `ARA_R5` | 159, 139, 171 | - | R6 | R6 |
| NAUO15 | `ARA_R6-1` | `ARA_R6` | 159, 134, 110 | - | R5 | R5 |
| NAUO16 | `ARA_R7-2` | `ARA_R7` | 170, 162, 176 | - | R7 | R7 |
| NAUO17 | `ARA_R8-1` | `ARA_R8` | 170, 162, 105 | - | R8 | R8 |
| NAUO18 | `ARA_A1-1` | `ARA_A1` | 166, 166, 125 | - | A1 | A1 |
| NAUO19 | `ARA_A2-1` | `ARA_A2` | 166, 166, 122 | - | A2 | A2 |
| NAUO20 | `ARA_A2_Supplement-1` | `ARA_A2_Supplement` | 166, 166, 119 | - | A3 | A3 |
| NAUO21 | `ARA_A3-1` | `ARA_A3` | 170, 206, 128 | - | A4 | A4 |
| NAUO22 | `ARA_A4-1` | `ARA_A4` | 250, 212, 125 | - | A5 | A5 |
| NAUO23 | `ARA_A5-1` | `ARA_A5` | 202, 192, 128 | - | A7 | A7 |
| NAUO24 | `ARA_A6-1` | `ARA_A6` | 202, 192, 161 | - | A8 | A8 |
| NAUO25 | `ARA_A7-1` | `ARA_A7` | 166, 210, 168 | - | A11 | A11 |
| NAUO26 | `ARA_A8-1` | `ARA_A8` | 216, 239, 165 | - | A10 | A10 |
| NAUO27 | `ARA_A9-1` | `ARA_A9` | 276, 222, 168 | - | A12 | A12 |
| NAUO28 | `ARA_A10-1` | `ARA_A10` | 265, 205, 168 | - | A13 | A13 |
| NAUO29 | `ARA_A11-1` | `ARA_A11` | 205, 194, 144 | - | A6 | A6 |
| NAUO30 | `ARA_A12-1` | `ARA_A12` | 199, 191, 138 | - | A9 | A9 |
| NAUO31 | `ARA_A12-2` | `ARA_A12` | 207, 200, 151 | - | A9 | A9 |
| NAUO32 | `ARA_C1-1` | `ARA_C1` | 322, 191, 165 | - | C1 | C1 |
| NAUO33 | `ARA_C2-1` | `ARA_C2` | 322, 191, 128 | - | C2 | C2 |
| NAUO34 | `ARA_C3-1` | `ARA_C3` | 323, 195, 146 | - | C3 | C3 |
| NAUO35 | `ARA_C4-1` | `ARA_C4` | 329, 181, 146 | - | C6 | C6 |
| NAUO36 | `ARA_C5-1` | `ARA_C5` | 326, 188, 131 | - | C4 | C4 |
| NAUO37 | `ARA_C6-1` | `ARA_C6` | 326, 188, 157 | - | C5 | C5 |
| NAUO38 | `ARA_C7-1` | `ARA_C7` | 359, 178, 155 | - | C8 | C8 |
| NAUO39 | `ARA_C8-1` | `ARA_C8` | 359, 178, 139 | - | C7 | C7 |
| NAUO40 | `ARA_C9-1` | `ARA_C9` | 326, 175, 146 | - | C9 | C9 |
| NAUO41 | `TB_TopBot-1` | `TB_TopBot` | 195, 92, 58 | - | T1 | T1 |
| NAUO42 | `TB_CenterLatches-1` | `TB_CenterLatches` | 195, 114, 58 | - | T2 | T2 |
| NAUO43 | `TB_CenterLatches-2` | `TB_CenterLatches` | 195, 114, 58 | - | T2 | T2 |
| NAUO44 | `TB_TopBot-2` | `TB_TopBot` | 195, 135, 58 | - | T1 | T1 |
| NAUO45 | `MG90S-1` | `MG90S` | 164, 108, 136 | Base Motor | - | Base Motor |
| NAUO46 | `2PartShoulder-1` | `2PartShoulder_Mirrored` | 164, 92, 141 | Base Motor | - | Double Servo Horn |
| NAUO47 | `M3x6mm-1` | `M3x6mm_91292A111` | 209, 92, 100 | 6mm Hex Screw | - | 6mm Screw |
| NAUO48 | `M3x6mm-2` | `M3x6mm_91292A111` | 104, 92, 100 | 6mm Hex Screw | - | 6mm Screw |
| NAUO49 | `M3x6mm-3` | `M3x6mm_91292A111` | -21, 92, 100 | 6mm Hex Screw | - | 6mm Screw |
| NAUO50 | `M3x6mm-4` | `M3x6mm_91292A111` | -21, 92, 182 | 6mm Hex Screw | - | 6mm Screw |
| NAUO51 | `M3x6mm-5` | `M3x6mm_91292A111` | 104, 92, 182 | 6mm Hex Screw | - | 6mm Screw |
| NAUO52 | `M3x6mm-6` | `M3x6mm_91292A111` | 209, 92, 182 | 6mm Hex Screw | - | 6mm Screw |
| NAUO53 | `M3x16mm-1` | `M3x16mm_91292A115` | 201, 190, 133 | 16mm Hex Screw | - | 16mm Screw |
| NAUO54 | `M3x16mm-2` | `M3x16mm_91292A115` | 209, 199, 156 | 16mm Hex Screw | - | 16mm Screw |
| NAUO55 | `M3x6mm-7` | `M3x6mm_91292A111` | 175, 162, 128 | 6mm Hex Screw | - | 6mm Screw |
| NAUO56 | `M3x10mm-1` | `M3x10mm_91292A113` | 159, 170, 121 | 10mm Hex Screw | - | 10mm Screw |
| NAUO57 | `M3x6mm-8` | `M3x6mm_91292A111` | 197, 236, 125 | 6mm Hex Screw | - | 6mm Screw |
| NAUO58 | `MG90S-2` | `MG90S` | 170, 162, 104 | Elbow Motor | - | Elbow Motor |
| NAUO59 | `1PartShoulder-2` | `1PartShoulder` | 182, 159, 120 | Elbow Motor | - | Single Servo Horn |
| NAUO60 | `M3x10mm-2` | `M3x10mm_91292A113` | 170, 172, 107 | 10mm Hex Screw | - | 10mm Screw |
| NAUO61 | `M3x10mm-3` | `M3x10mm_91292A113` | 170, 153, 107 | 10mm Hex Screw | - | 10mm Screw |
| NAUO62 | `M3x10mm-4` | `M3x10mm_91292A113` | 143, 176, 124 | 10mm Hex Screw | - | 10mm Screw |
| NAUO63 | `M3x6mm-9` | `M3x6mm_91292A111` | 229, 221, 125 | 6mm Hex Screw | - | 6mm Screw |
| NAUO64 | `M3x6mm-10` | `M3x6mm_91292A111` | 193, 239, 168 | 6mm Hex Screw | - | 6mm Screw |
| NAUO65 | `M3x6mm-11` | `M3x6mm_91292A111` | 239, 239, 168 | 6mm Hex Screw | - | 6mm Screw |
| NAUO66 | `MG90S-3` | `MG90S` | 170, 162, 177 | Shoulder Motor | - | Shoulder Motor |
| NAUO67 | `1PartShoulder-3` | `1PartShoulder` | 181, 168, 161 | Shoulder Motor | - | Single Servo Horn |
| NAUO68 | `M3x10mm-5` | `M3x10mm_91292A113` | 170, 172, 174 | 10mm Hex Screw | - | 10mm Screw |
| NAUO69 | `M3x10mm-6` | `M3x10mm_91292A113` | 170, 153, 174 | 10mm Hex Screw | - | 10mm Screw |
| NAUO70 | `M3x6mm-12` | `M3x6mm_91292A111` | 139, 180, 171 | 6mm Hex Screw | - | 6mm Screw |
| NAUO71 | `M3x10mm-7` | `M3x10mm_91292A113` | 229, 221, 166 | 10mm Hex Screw | - | 10mm Screw |
| NAUO72 | `MG90S-4` | `MG90S_Cut wires shorter` | 335, 196, 144 | Claw Motor | - | Claw Motor |
| NAUO73 | `1PartShoulder-4` | `1PartShoulder` | 342, 180, 138 | Claw Motor | - | Single Servo Horn |
| NAUO74 | `M3x16mm-3` | `M3x16mm_91292A115` | 323, 186, 147 | 16mm Hex Screw | - | 16mm Screw |
| NAUO75 | `M3x16mm-4` | `M3x16mm_91292A115` | 347, 186, 147 | 16mm Hex Screw | - | 16mm Screw |
| NAUO76 | `M3x10mm-8` | `M3x10mm_91292A113` | 335, 177, 156 | 10mm Hex Screw | - | 10mm Screw |
| NAUO77 | `M3x6mm-13` | `M3x6mm_91292A111` | 312, 206, 168 | 6mm Hex Screw | - | 6mm Screw |
| NAUO78 | `M3x6mm-14` | `M3x6mm_91292A111` | 302, 188, 168 | 6mm Hex Screw | - | 6mm Screw |
| NAUO79 | `M3x6mm-15` | `M3x6mm_91292A111` | 302, 188, 125 | 6mm Hex Screw | - | 6mm Screw |
| NAUO80 | `KY-023_Joystick-Module-1` | `PCB_1`, `5x_Ang_Conn_1`, `Baseplate_1` and 6 more | 6, 133, 119 | Joystick | - | Left Joystick |
| NAUO81 | `KY-023_Joystick-Module-2` | `PCB_1`, `5x_Ang_Conn_1`, `Baseplate_1` and 6 more | 6, 133, 164 | Joystick | - | Right Joystick |
| NAUO82 | `Ensamblaje_Shield_NANO-1` | `Shield_Arduino NANO`, `User Library-PJ-002AH_Body`, `User Library-PJ-002AH_Pad` and 19 more | 70, 115, 146 | Nano / Nano I/O Module | - | Nano I/O Module (with the Nano plugged in) |
| NAUO83 | `JR-3_with_cable-3` | `Copy of JR-3^JR-3_with_cable`, `Copy of JWT-CONTACT^JR-3_with_cable`, `Copy of Cable_JR^JR-3_with_cable` | 52, 134, 139 | Base Motor | - | Base Motor wire |
| NAUO84 | `JR-3_with_cable-4` | `Copy of JR-3^JR-3_with_cable`, `Copy of JWT-CONTACT^JR-3_with_cable`, `Copy of Cable_JR^JR-3_with_cable` | 52, 134, 142 | Elbow Motor | - | Elbow Motor wire |
| NAUO85 | `JR-3-7` | `Copy of JR-3_2^JR-3`, `Copy of JWT-CONTACT_1^JR-3` | 52, 115, 155 | Servo Extension Wire | - | Servo Extension Wire |
| NAUO86 | `JR-3_with_cable-6` | `Copy of JR-3^JR-3_with_cable`, `Copy of JWT-CONTACT^JR-3_with_cable`, `Copy of Cable_JR^JR-3_with_cable` | 52, 134, 152 | Shoulder Motor | - | Shoulder Motor wire |
| NAUO87 | `Part1^ARA_Pathways-1` | `Part1^ARA_Pathways` | 108, 151, 150 | Base Motor | - | Base Motor wire |
| NAUO88 | `Part2^ARA_Pathways-1` | `Part2^ARA_Pathways` | 123, 170, 107 | Elbow Motor | - | Elbow Motor wire |
| NAUO89 | `Part3^ARA_Pathways-1` | `Part3^ARA_Pathways` | 123, 175, 179 | Shoulder Motor | - | Shoulder Motor wire |
| NAUO90 | `JR-3-8` | `Copy of JR-3_2^JR-3`, `Copy of JWT-CONTACT_1^JR-3` | 161, 134, 145 | Claw Motor | - | Claw Motor wire |
| NAUO91 | `JR-3 Bridge-1` | `JR-3 Bridge` | 153, 134, 145 | Servo Extension Wire | - | Servo Extension Wire |
| NAUO92 | `JR-3-2` | `Copy of JR-3_2^JR-3`, `Copy of JWT-CONTACT_1^JR-3` | 146, 134, 145 | Servo Extension Wire | - | Servo Extension Wire |
| NAUO93 | `Part4^ARA_Pathways-1` | `Part4^ARA_Pathways` | 96, 142, 149 | Servo Extension Wire | - | Servo Extension Wire |
| NAUO94 | `Part5^ARA_Pathways-1` | `Part5^ARA_Pathways` | 250, 176, 139 | Claw Motor | - | Claw Motor wire |
| NAUO95 | `Wire Cap-1` | `Wire Cap` | 88, 112, 142 | Breadboard Wire (F-F) | - | Breadboard Wire |
| NAUO96 | `Wire Cap-2` | `Wire Cap` | 86, 112, 142 | Breadboard Wire (F-F) | - | Breadboard Wire |
| NAUO97 | `Wire Cap-3` | `Wire Cap` | 83, 112, 142 | Breadboard Wire (F-F) | - | Breadboard Wire |
| NAUO98 | `Wire Cap-4` | `Wire Cap` | 88, 112, 139 | Breadboard Wire (F-F) | - | Breadboard Wire |
| NAUO99 | `Wire Cap-5` | `Wire Cap` | 83, 112, 136 | Breadboard Wire (F-F) | - | Breadboard Wire |
| NAUO100 | `Wire Cap-6` | `Wire Cap` | 86, 112, 136 | Breadboard Wire (F-F) | - | Breadboard Wire |
| NAUO101 | `Wire Cap-7` | `Wire Cap` | 88, 112, 136 | Breadboard Wire (F-F) | - | Breadboard Wire |
| NAUO102 | `Wire Cap-8` | `Wire Cap` | 88, 112, 134 | Breadboard Wire (F-F) | - | Breadboard Wire |
| NAUO103 | `Wire Cap-9` | `Wire Cap` | 24, 124, 168 | Breadboard Wire (F-F) | - | Breadboard Wire |
| NAUO104 | `Wire Cap-10` | `Wire Cap` | 24, 124, 123 | Breadboard Wire (F-F) | - | Breadboard Wire |
| NAUO105 | `Wire Cap-11` | `Wire Cap` | 24, 124, 121 | Breadboard Wire (F-F) | - | Breadboard Wire |
| NAUO106 | `Wire Cap-12` | `Wire Cap` | 24, 124, 118 | Breadboard Wire (F-F) | - | Breadboard Wire |
| NAUO107 | `Wire Cap-13` | `Wire Cap` | 24, 124, 116 | Breadboard Wire (F-F) | - | Breadboard Wire |
| NAUO108 | `Wire Cap-14` | `Wire Cap` | 24, 124, 166 | Breadboard Wire (F-F) | - | Breadboard Wire |
| NAUO109 | `Wire Cap-15` | `Wire Cap` | 24, 124, 163 | Breadboard Wire (F-F) | - | Breadboard Wire |
| NAUO110 | `Wire Cap-16` | `Wire Cap` | 24, 124, 161 | Breadboard Wire (F-F) | - | Breadboard Wire |
| NAUO111 | `Part6^ARA_Pathways-1` | `Part6^ARA_Pathways` | 58, 137, 154 | Breadboard Wire (F-F) | - | Breadboard Wire |
| NAUO112 | `Part7^ARA_Pathways-1` | `Part7^ARA_Pathways` | 58, 136, 126 | Breadboard Wire (F-F) | - | Breadboard Wire |

## 2. Colours

### 2.1 Every colour the project shows

"Set in the step" means the author chose it in Cadasio. The others are whatever the SolidWorks model carried, which for `#e4e4e4`
(SolidWorks' default grey: 205 solids) most likely means nobody has coloured that solid yet. "Solids" counts Cadasio's leaf solids
over all 112 instances (917 in total), so the three identical servos count three times.

| Colour | Solids | Set in the step? | Where |
|---|---|---|---|
| `#a6a9aa` | 246 | yes | nano_Varsayılan (125), 5x_Ang_Conn_1 (20), Tactile-Switch_1 (16), M3x6mm_91292A111 (14), Copy of JWT-CONTACT^JR-3_with_cable (9), M3x10mm_91292A113 (8), Potentiometer_02_1 (6) ... |
| `#e4e4e4` | 205 | no (SolidWorks colour) | nano_Varsayılan (125), PCB_1 (60), Potentiometer_02_1 (10), Potentiometer_01_1 (10) |
| `#ffffff` | 112 | no (SolidWorks colour) | MG90S (84), MG90S_Cut wires shorter (28) |
| `#1e1616` | 92 | yes | wood parts (92) |
| `#deb887` | 44 | yes | wood parts (44) |
| `#404040` | 26 | 16 of 26 | Wire Cap (16), Copy of JR-3^JR-3_with_cable (3), Copy of JR-3_2^JR-3 (3), Tactile-Switch_1 (2), JR-3 Bridge (1), Part6^ARA_Pathways (1) |
| `#181818` | 26 | yes | nano_Varsayılan (20), Tactile-Switch_1 (2), Samtec-SSW-115-01-F-S (2), User Library-PJ-002AH_Body (1), nano - reg (1) |
| `#191919` | 25 | no (SolidWorks colour) | 47uf CAP Dcase (15), nano_Varsayılan (9), reset core (1) |
| `#cccecc` | 18 | no (SolidWorks colour) | cap106C (12), nano - reg (6) |
| `#ffff80` | 17 | no (SolidWorks colour) | Samtec-TLW-104-01-F-S_R (4), Samtec-TLW-104-01-F-S_B (4), Samtec-TLW-104-01-F-S_N (4), Samtec-TLW-104-01-F-S_W (2), Samtec-TLW-108-01-F-S_R (1), Samtec-TLW-108-01-F-S_B (1), Samtec-TLW-108-01-F-S_N (1) |
| `#bd291f` | 13 | no (SolidWorks colour) | MG90S (3), Copy of Cable_JR^JR-3_with_cable (3), MG90S_Cut wires shorter (1), Part1^ARA_Pathways (1), Part5^ARA_Pathways (1), Part4^ARA_Pathways (1), Part2^ARA_Pathways (1) ... |
| `#ff9d07` | 13 | 2 of 13 | MG90S (3), Copy of Cable_JR^JR-3_with_cable (3), MG90S_Cut wires shorter (1), Part1^ARA_Pathways (1), Part5^ARA_Pathways (1), Part4^ARA_Pathways (1), Part2^ARA_Pathways (1) ... |
| `#303030` | 12 | no (SolidWorks colour) | 5x_Ang_Conn_1 (2), PCB_1 (2), Thumb-Button (2), Baseplate_1 (2), Potentiometer_02_1 (2), Potentiometer_01_1 (2) |
| `#975100` | 11 | no (SolidWorks colour) | MG90S (3), Copy of Cable_JR^JR-3_with_cable (3), Part1^ARA_Pathways (1), Part4^ARA_Pathways (1), Part2^ARA_Pathways (1), Part3^ARA_Pathways (1), Part6^ARA_Pathways (1) |
| `#1a1a1a` | 7 | no (SolidWorks colour) | 1PartShoulder (6), 2PartShoulder_Mirrored (1) |
| `#d3d6d3` | 6 | no (SolidWorks colour) | nano_Varsayılan (6) |
| `#fffbf0` | 6 | no (SolidWorks colour) | Copy of JWT-CONTACT_1^JR-3 (6) |
| `#262626` | 4 | no (SolidWorks colour) | MG90S (3), MG90S_Cut wires shorter (1) |
| `#c7c2bd` | 4 | no (SolidWorks colour) | MG90S (3), MG90S_Cut wires shorter (1) |
| `#ff00ff` | 4 | no (SolidWorks colour) | MG90S (3), MG90S_Cut wires shorter (1) |
| `#efefef` | 4 | no (SolidWorks colour) | nano_Varsayılan (4) |
| `#a5936d` | 4 | no (SolidWorks colour) | nano_Varsayılan (2), cap106C (2) |
| `#c0c0c0` | 3 | no (SolidWorks colour) | User Library-PJ-002AH_Pad (2), M3x6mm_91292A111 (1) |
| `#975000` | 2 | yes | MG90S_Cut wires shorter (1), Part5^ARA_Pathways (1) |
| `#808080` | 2 | yes | Rotator-Unit_1 (2) |
| `#000f41` | 2 | yes | nano_Varsayılan (1), Shield_Arduino NANO (1) |
| `#ffff7f` | 2 | yes | Samtec-TLW-103-01-F-S (2) |
| `#cccccc` | 1 | yes | nano_Varsayılan (1) |
| `#a5926d` | 1 | yes | m7 diode (1) |
| `#d8d8d8` | 1 | no (SolidWorks colour) | led (1) |
| `#15ff93` | 1 | no (SolidWorks colour) | Part7^ARA_Pathways (1) |
| `#ffff00` | 1 | no (SolidWorks colour) | Part7^ARA_Pathways (1) |
| `#c5bdff` | 1 | no (SolidWorks colour) | Part7^ARA_Pathways (1) |
| `#003fd8` | 1 | no (SolidWorks colour) | Part7^ARA_Pathways (1) |

Against the colour library in the rulebook (section 8): wood, engraving, metal `#a6a9aa`, Nano board `#000f41`, header blocks
`#ffff80`, socket strips `#181818` and IC bodies `#191919` are the house colours. Not the house colours: the I/O module board
(`#000f41` here, `#224bbe` in the published guides), header pins (`#a6a9aa` here, `#e3e3e3` there), Dupont housings (`#404040` here,
`#1e1616` there), and the servo leads (brown `#975100`, red `#bd291f`, orange `#ff9d07` here; the published pre-wired leads are red
`#ef3340`, tan `#b28362`, black `#2d2926`).

### 2.2 Lee's five points

For each: what Cadasio has, which solids of ours are involved (mesh coordinates, then assembly space), and what a rule has to do.

**(a) The voltage regulator under the Nano, on the shield.** Mesh `nano - reg`, in NAUO82. Mesh box (-3.25, -0.095, -4.155)..(3.25, 1.6, 4.155);
in mesh coordinates Y is up through the chip.

| Solid | What | Size | Mesh box min .. max | Assembly box min .. max | Cadasio | Ours now |
|---|---|---|---|---|---|---|
| 1 | body, pins included (closed solid) | 6.50 x 1.69 x 8.30 | (-3.25, -0.09, -4.15) .. (3.25, 1.60, 4.15) | (65.7, 106.3, 148.1) .. (74.0, 108.0, 154.6) | `#181818` (set) | `#1e1616` |
| 0 | pin skin, the wide end | 6.50 x 0.79 x 2.43 | (-3.25, -0.095, -4.155) .. (3.25, 0.695, -1.727) | (71.5, 106.3, 148.1) .. (74.0, 107.1, 154.6) | `#a6a9aa` (set) | `#1e1616` |
| 2 | pin skin, the narrow end | 3.81 x 0.79 x 2.43 | (-1.905, -0.095, 1.727) .. (1.905, 0.695, 4.155) | (65.7, 106.3, 149.5) .. (68.1, 107.1, 153.3) | `#a6a9aa` (set) | `#1e1616` |
| 3, 4, 5, 6, 7, 8 | flat marks on top (print), y = 1.595 | 0.31-0.71 x 0 x 1.00-1.03 | within (-1.25, 1.595, -1.26) .. (1.41, 1.595, 1.26) | within (68.6, 108.0, 150.1) .. (71.1, 108.0, 152.8) | `#cccecc` (SolidWorks colour, not set) | `#1e1616` |

Rule: in `nano - reg`, the two solids whose thinnest side is 0.79 mm (`thin` 0.7 to 0.9) are skins coloured `#a6a9aa`, with
`"skin": true` so the pin faces of the body under them take the silver; the solids of zero thickness (`thin` 0 to 0.05) are the
print, `#cccecc`; the body (thinnest side 1.69) is `#181818`.
(There is a second regulator on the underside of the Nano itself: `nano_Varsayılan` solid 20, 8.30 x 1.69 x 6.50 at mesh
(1.95, -1.60, -13.41)..(10.25, 0.09, -6.91), assembly (68.8, 115.8, 135.6)..(75.3, 117.5, 143.9). Cadasio `#181818`, ours `#d3d6d3`.
It has no pin skins and cannot be seen once the Nano is in its sockets.)

**(b) The solder mounds round the Nano's pins.** Mesh `nano_Varsayılan`, in NAUO82. Mesh box (-3.82, -8.52, -16.62)..(41.18, 10.11, 1.38);
in mesh coordinates X runs along the board (USB end at +X), Y is up through the board (board 0..1.6, parts on top above 1.6), Z across.

| Solids | What | Size each | Mesh span | Assembly span | Cadasio | Ours now |
|---|---|---|---|---|---|---|
| 30: 7, 8, 18, 19, 27, 28, 36, 37, 48, 49, 61, 62, 71, 72, 82, 83, 103, 104, 129, 130, 165, 166, 204, 205, 237, 238, 254, 255, 262, 263 | solder mound skins (cones, open underneath) | 1.83 x 1.52 x 1.83 | y 1.60 .. 3.12; two rows at z about -15.2 and 0.0; x -0.9 .. 36.5 | (60.9, 119.0, 132.8) .. (78.0, 120.6, 170.2) | `#a6a9aa` (set) | `#e4e4e4` |
| 30: 13, 14, 25, 26, 32, 33, 42, 43, 58, 59, 66, 67, 77, 78, 87, 88, 109, 110, 141, 142, 180, 181, 217, 218, 246, 247, 260, 261, 270, 271 | pin skins, upper part | 0.78 x 3.27 x 0.78 | y 0.00 .. 3.27 | (61.4, 117.4, 133.3) .. (77.5, 120.7, 169.6) | `#a6a9aa` (set) | `#e4e4e4` |
| 30 (11, 12, 23, 24, ...) | pin skins, lower part | 0.78 x 6.02 x 0.79 | y -8.52 .. -2.50 | (61.4, 108.9, 133.3) .. (77.5, 114.9, 169.6) | `#e4e4e4` (not set; hidden in the socket strips) | `#e4e4e4` |
| 0 | the board, WITH the 30 cones (and 6 more underneath) as part of it | 43.20 x 4.60 x 18.00 | y -1.50 .. 3.10 | (60.5, 115.9, 129.9) .. (78.5, 120.5, 173.1) | `#000f41` (set) | `#000f41` |
| 5, 6 | the two 15-pin header strips, each one solid WITH its pins | 38.10 x 11.75 x 2.54 | y -8.50 .. 3.25 | x 75.8 .. 78.4 and x 60.6 .. 63.1 | `#191919` | `#191919` |

Why ours look like the board (worked out from the geometry, not from a rendering): the cone is part of the navy board solid (678 of
its vertices sit inside each mound's box) and the silver skin is a separate shell 0.02 mm outside it. Our build gives the skins
`#e4e4e4` from the old atlas, but simplifies that colour group from 125,814 to 6,720 triangles (tolerance relaxed to 0.48 mm by the
6,000 triangle budget), which leaves 10 to 16 triangles per mound; the board's own cone then pokes through. One mound (solid 7) also
has its faces wound inwards. Rule: mark the mound and pin skins as skins, so the board and header faces under them take `#a6a9aa`.
The same goes for the 32 ATmega lead skins (1.28 x 0.68 x 1.28, `#a6a9aa`) and the 6 programming-header pin skins (0.76 x 6.01 x 0.76, `#a6a9aa`).

**(c) The mini-USB socket.** Mesh `nano_Varsayılan`.

| Solid | What | Size | Mesh box | Assembly box | Cadasio | Ours now |
|---|---|---|---|---|---|---|
| 253 | shell AND inner core (they touch, so they are one solid in our mesh) | 9.40 x 4.80 x 10.90 | (31.78, 0.55, -13.07) .. (41.18, 5.35, -2.17) | (64.0, 118.0, 165.5) .. (74.9, 122.8, 174.9) | shell (9.40 x 3.75 x 10.90, y 1.6 .. 5.35) `#cccccc` (set; SolidWorks colour `#e4e4e4`); core (8.20 x 4.50 x 7.70) `#a6a9aa` (set) | `#e4e4e4` |
| 248, 249, 250, 251, 252 | the five contacts | 9.40 x 2.55 x 0.50 | x 30.78 .. 40.18, y 1.60 .. 4.15, z -9.47 .. -5.77 | (67.6, 119.0, 164.5) .. (71.3, 121.6, 173.9) | `#d3d6d3` (not set) | `#d3d6d3` |

So in Cadasio the shell is lighter (`#cccccc`) than the pins (`#a6a9aa`); only the core inside the opening is pin silver. If Lee wants
"the same silver as the pins", that is `#a6a9aa` on solid 253 (one colour is all that solid can take), which is darker than
Cadasio's shell. Ours is whiter than both because the old atlas gave it `#e4e4e4`.

**(d) The joystick's header pins.** Mesh `5x_Ang_Conn_1`, in NAUO80 and NAUO81. Mesh box (-7.3, -6.25, -3.0)..(1.25, 6.25, 4.0).

| Solids | What | Size each | Mesh boxes | Assembly (NAUO80; add 45.0 to z for NAUO81) | Cadasio | Ours now |
|---|---|---|---|---|---|---|
| 0, 1, 2, 3, 4 | the pins a wire plugs onto | 7.60 x 0.60 x 1.50 | x -7.3 .. 0.3, z 2.5 .. 4.0, y centres -5.0, -2.5, 0, 2.5, 5.0 | (17.9, 123.0, 113.0) .. (25.5, 124.5, 123.6) | `#a6a9aa` (set) | `#1e1616` |
| 6, 7, 8, 9, 10 | the legs through the board | 0.60 x 0.60 x 3.00 | x -0.3 .. 0.3, z -3.0 .. 0.0, same y centres | (17.9, 117.5, 113.0) .. (18.5, 120.5, 123.6) | `#a6a9aa` (set) | `#1e1616` |
| 5 | plastic bar | 2.50 x 12.50 x 2.50 | (-1.25, -6.25, 0.0) .. (1.25, 6.25, 2.5) | (16.9, 120.5, 112.1) .. (19.4, 123.0, 124.6) | `#303030` (SolidWorks colour) | `#1e1616` |

All eleven are closed solids, so a plain component rule works: `thin` 0.5-0.7 gives the ten pins.

**(e) The servo label and horns.** Meshes `MG90S` (NAUO45, NAUO58, NAUO66) and `MG90S_Cut wires shorter` (NAUO72). Mesh box
(-16.1, -11.275, -6.075)..(16.1, 20.975, 6.25). The label is on the +Z face of the mesh.

| Solid | What | Size | Mesh box | Cadasio | Ours now |
|---|---|---|---|---|---|
| 0 | body | 32.20 x 28.30 x 12.15 | (-16.1, -11.275, -6.075) .. (16.1, 17.025, 6.075) | `#262626` | `#2d2926` |
| 1 | label plate; in our mesh the lettering faces are welded into it | 20.15 x 10.05 x 0.30 | (-10.075, -5.875, 5.95) .. (10.075, 4.175, 6.25) | plate `#ff00ff`; lettering `#ffffff` | `#f5f5f6` |
| 2 | output shaft | 4.87 x 3.95 x 4.87 | (2.94, 17.02, -2.44) .. (7.81, 20.98, 2.44) | `#c7c2bd` | `#f5f5f6` |
| 3 / 4 / 5 | lead stubs (3.0 long; 0.5 long on NAUO72) | 1.0 x 1.0 across | x 11.3 .., y -7.02 .. -6.03, z -1.52 .. -0.52 / -0.5 .. 0.5 / 0.52 .. 1.52 | brown `#975100` / red `#bd291f` / orange `#ff9d07` (on NAUO72: orange / red / brown `#975000`) | orange / red / brown (NAUO72: all `#2d2926`) |

Label plates in assembly space: NAUO45 (169.6, 108.4, 125.4)..(169.9, 118.5, 145.5), facing +X; NAUO58 (160.2, 156.0, 93.5)..(180.4, 156.3, 103.6),
facing -Y; NAUO66 (160.2, 168.2, 177.7)..(180.4, 168.5, 187.7), facing +Y; NAUO72 (329.0, 196.2, 134.1)..(329.4, 206.3, 154.2), facing -X.

The lettering in Cadasio is 28 flat bodies at z = 6.25, all `#ffffff` (SolidWorks colour), none of them a solid of its own in our mesh:

- 25 named `MG90S-Surface-Offset2[1..25]`: a frame 19.0 x 9.0 mm with two dividers 0.2 mm wide, at (-9.5, -5.35)..(9.5, 3.65); eight
  letters "TowerPro" in the top row (y 0.72 .. 3.06); five "MG90S" in the middle row (y -2.48 .. -0.11); eleven for "Micro servo" in the
  bottom row (y -4.97 .. -3.08: ten letters and the dot of the i). These show.
- 3 named `MG90S-Surface-Offset1[1..3]`: a band 18.6 x 2.8 mm behind the middle row and the insides of the 9 and the 0. On every servo
  the author pushed these 0.05 to 0.23 mm into the body, further than the plate (0.02 to 0.04 mm), so they sit under the plate and do
  not show (worked out from the offsets, not seen). The middle row is therefore pink with white letters like the other two.

In our mesh every one of the 28 has exactly two face islands in solid 1 on the plane z = 6.25 (the plate's own split face and the
copy), with the same x/y box to 0.03 mm. `cadasio_mra_servo_label.png` is that rule drawn from OUR mesh: faces of solid 1 whose island
box equals one of the 25 visible boxes in white, everything else `#ff00ff`. It reads "Tower Pro / MG90S / Micro servo" inside a frame,
seen from +Z with +X to the right and +Y up. So the lettering can be had from our CAD, but it needs a face-level rule (like the wood
`engraving` rule), not a per-solid colour: `build_model.py` splits by connected solid and the letters are welded to the plate. The 25
boxes are in the JSON under `MG90S` (entries with `"shown": true`) together with the rule in words.
"Outlined" text: with toon edges on, Cadasio draws a black line round every one of these flat bodies, so each white letter has a
black outline; our build would get the same from the island borders.

Horns: `2PartShoulder_Mirrored` (NAUO46, the two-arm horn under the base motor, 36.35 x 4.55 x 6.65, assembly (145.5, 89.9, 137.5)..(181.8, 94.4, 144.2))
and `1PartShoulder` (NAUO59, NAUO67, NAUO73, one arm 17.9 x 2.29 x 6.63 plus hub 6.63 x 4.55 x 6.65): all `#1a1a1a`, the SolidWorks
colour. Ours are `#f5f5f6` (rule `Shoulder` -> `white_plastic`).

### 2.3 Every difference, part by part

**Wood, NAUO1 to NAUO44** (40 mesh names): wood `#deb887` and engraving `#1e1616`, both set in the step. Same as ours (`wood`, `ink`). No difference.
In Cadasio the two `TB_CenterLatches` instances also carry `colour_secondary` `#000000`, which has no visible effect that I can find.

**Screws, NAUO47-57 and others**: `#a6a9aa`, same as ours. One screw, NAUO55 (`M3x6mm-7`, at (175.3, 161.9, 128.1)), was missed by the
author and shows the SolidWorks colour `#c0c0c0`.

**Everything else** (one row per group of solids that share a colour; "close" means within 10 levels per channel):

| Mesh (instances) | Solid(s) of ours | What | Size (mm) | Cadasio | Ours now | Verdict |
|---|---|---|---|---|---|---|
| `M3x6mm_91292A111` (NAUO47-52, NAUO55, NAUO57, NAUO63-65, NAUO70, NAUO77-79) | 0 | whole part | 5.50 x 5.48 x 9.00 | `#a6a9aa` | `#a6a9aa` steel | same |
| `M3x10mm_91292A113` (NAUO56, NAUO60-62, NAUO68-69, NAUO71, NAUO76) | 0 | whole part | 5.50 x 5.48 x 13.00 | `#a6a9aa` | `#a6a9aa` steel | same |
| `M3x16mm_91292A115` (NAUO53-54, NAUO74-75) | 0 | whole part | 5.50 x 5.48 x 19.00 | `#a6a9aa` | `#a6a9aa` steel | same |
| `MG90S` (NAUO45, NAUO58, NAUO66) | 0 | body | 32.20 x 28.30 x 12.15 | `#262626` | `#2d2926` servo_body | close (within 7 levels) |
|  | 1 | label plate (with the lettering faces welded in) | 20.15 x 10.05 x 0.30 | `#ff00ff` | `#f5f5f6` servo_label | DIFFERENT |
|  | 2 | output shaft | 4.87 x 3.95 x 4.87 | `#c7c2bd` | `#f5f5f6` white_plastic | DIFFERENT |
|  | 3 | lead stub | 3.00 x 1.00 x 1.00 | `#975100` | `#ff851b` wire_orange | DIFFERENT |
|  | 4 | lead stub | 3.00 x 1.00 x 1.00 | `#bd291f` | `#ef3340` wire_red | DIFFERENT |
|  | 5 | lead stub | 3.00 x 1.00 x 1.00 | `#ff9d07` | `#7c5a30` wire_brown | DIFFERENT |
| `MG90S_Cut wires shorter` (NAUO72) | 0 | body | 32.20 x 28.30 x 12.15 | `#262626` | `#2d2926` servo_body | close (within 7 levels) |
|  | 1 | label plate (with the lettering faces welded in) | 20.15 x 10.05 x 0.30 | `#ff00ff` | `#f5f5f6` servo_label | DIFFERENT |
|  | 2 | output shaft | 4.87 x 3.95 x 4.87 | `#c7c2bd` | `#f5f5f6` white_plastic | DIFFERENT |
|  | 3 | lead stub | 0.50 x 1.00 x 1.00 | `#ff9d07` | `#2d2926` servo_body | DIFFERENT |
|  | 4 | lead stub | 0.50 x 1.00 x 1.00 | `#bd291f` | `#2d2926` servo_body | DIFFERENT |
|  | 5 | lead stub | 0.50 x 1.00 x 1.00 | `#975000` | `#2d2926` servo_body | DIFFERENT |
| `2PartShoulder_Mirrored` (NAUO46) | 0 | whole horn | 36.35 x 4.55 x 6.65 | `#1a1a1a` | `#f5f5f6` white_plastic | DIFFERENT |
| `1PartShoulder` (NAUO59, NAUO67, NAUO73) | 0 | arm | 17.90 x 2.29 x 6.63 | `#1a1a1a` | `#f5f5f6` white_plastic | DIFFERENT |
|  | 1 | hub | 6.63 x 4.55 x 6.65 | `#1a1a1a` | `#f5f5f6` white_plastic | DIFFERENT |
| `PCB_1` (NAUO80-81) | 0 | board | 34.00 x 26.00 x 1.61 | `#303030` | `#1e1616` pcb_black | DIFFERENT |
|  | 26 solids (1..26) | pad or print on top (0.01 mm thick) | 0.25-11.60 x 0.25-12.80 x 0.01 | `#e4e4e4` | `#e3e3e3` pin_silver | close (within 1 levels) |
| `5x_Ang_Conn_1` (NAUO80-81) | 0, 1, 2, 3, 4 | pin (bent part) | 7.60 x 0.60 x 1.50 | `#a6a9aa` | `#1e1616` black_plastic | DIFFERENT |
|  | 5 | plastic bar | 2.50 x 12.50 x 2.50 | `#303030` | `#1e1616` black_plastic | DIFFERENT |
|  | 6, 7, 8, 9, 10 | pin leg | 0.60 x 0.60 x 3.00 | `#a6a9aa` | `#1e1616` black_plastic | DIFFERENT |
| `Baseplate_1` (NAUO80-81) | 0 | whole part | 18.00 x 23.30 x 3.50 | `#303030` | `#1e1616` black_plastic | DIFFERENT |
| `Case` (NAUO80-81) | 0 | whole part | 16.00 x 16.00 x 16.10 | `#a6a9aa` | `#a6a9aa` metal_can | same |
| `Rotator-Unit_1` (NAUO80-81) | 0 | whole part | 16.20 x 21.50 x 16.20 | `#808080` | `#f5f5f6` white_plastic | DIFFERENT |
| `Potentiometer_01_1` (NAUO80-81) | 0 | body | 9.50 x 3.50 x 11.00 | `#303030` | `#0074d9` pot_blue | DIFFERENT |
|  | 1, 3, 4 | leg | 0.75 x 0.30 x 3.00 | `#a6a9aa` | `#0074d9` pot_blue | DIFFERENT |
|  | 2 | disc on the side | 3.90 x 0.50 x 3.89 | `#e4e4e4` | `#0074d9` pot_blue | DIFFERENT |
| `Potentiometer_02_1` (NAUO80-81) | 0 | body | 9.50 x 3.50 x 11.00 | `#303030` | `#0074d9` pot_blue | DIFFERENT |
|  | 1, 3, 4 | leg | 0.75 x 0.30 x 3.00 | `#a6a9aa` | `#0074d9` pot_blue | DIFFERENT |
|  | 2 | disc on the side | 3.90 x 0.50 x 3.89 | `#e4e4e4` | `#0074d9` pot_blue | DIFFERENT |
| `Tactile-Switch_1` (NAUO80-81) | 0 | body (with its four legs) | 6.89 x 7.06 x 6.01 | `#181818` | `#1e1616` black_plastic | close (within 6 levels) |
|  | 1, 2, 4, 5 | corner stud | 1.09 x 0.20 x 1.09 | `#a6a9aa` | `#e3e3e3` pin_silver | DIFFERENT |
|  | 3 | button | 3.42 x 1.27 x 3.43 | `#404040` | `#1e1616` black_plastic | DIFFERENT |
| `Thumb-Button` (NAUO80-81) | 0 | whole part | 25.92 x 25.92 x 18.00 | `#303030` | `#1e1616` black_plastic | DIFFERENT |
| `Shield_Arduino NANO` (NAUO82) | 0 | whole part | 53.34 x 1.65 x 57.20 | `#000f41` | `#224bbe` pcb_blue | DIFFERENT |
| `Samtec-SSW-115-01-F-S` (NAUO82) | 0 | whole part | 2.41 x 11.15 x 38.61 | `#181818` | `#1e1616` black_plastic | close (within 6 levels) |
| `Samtec-TLW-103-01-F-S` (NAUO82) | 0 | base skin | 7.64 x 1.54 x 2.51 | `#ffff7f` | `#ffff80` header_yellow | close (within 1 levels) |
|  | 1 | pins (and the base under the skin) | 7.62 x 10.00 x 2.49 | `#a6a9aa` | `#e3e3e3` pin | DIFFERENT |
| `Samtec-TLW-104-01-F-S_N` (NAUO82) | 0 | base skin | 10.18 x 1.54 x 2.51 | `#ffff80` | `#ffff80` header_yellow | same |
|  | 1 | pins (and the base under the skin) | 10.16 x 10.00 x 2.49 | `#a6a9aa` | `#e3e3e3` pin | DIFFERENT |
| `Samtec-TLW-104-01-F-S_R` (NAUO82) | 0 | base skin | 10.18 x 1.54 x 2.51 | `#ffff80` | `#ffff80` header_yellow | same |
|  | 1 | pins (and the base under the skin) | 10.16 x 10.00 x 2.49 | `#a6a9aa` | `#e3e3e3` pin | DIFFERENT |
| `Samtec-TLW-104-01-F-S_B` (NAUO82) | 0 | base skin | 10.18 x 1.54 x 2.51 | `#ffff80` | `#ffff80` header_yellow | same |
|  | 1 | pins (and the base under the skin) | 10.16 x 10.00 x 2.49 | `#a6a9aa` | `#e3e3e3` pin | DIFFERENT |
| `Samtec-TLW-104-01-F-S_W` (NAUO82) | 0 | base skin | 10.18 x 1.54 x 2.51 | `#ffff80` | `#ffff80` header_yellow | same |
|  | 1 | pins (and the base under the skin) | 10.16 x 10.00 x 2.49 | `#a6a9aa` | `#e3e3e3` pin | DIFFERENT |
| `Samtec-TLW-108-01-F-S_N` (NAUO82) | 0 | base skin | 20.34 x 4.18 x 2.51 | `#ffff80` | `#ffff80` header_yellow | same |
|  | 1 | pins (and the base under the skin) | 20.32 x 10.00 x 2.49 | `#a6a9aa` | `#e3e3e3` pin | DIFFERENT |
| `Samtec-TLW-108-01-F-S_R` (NAUO82) | 0 | base skin | 20.34 x 1.54 x 2.51 | `#ffff80` | `#ffff80` header_yellow | same |
|  | 1 | pins (and the base under the skin) | 20.32 x 10.00 x 2.49 | `#a6a9aa` | `#e3e3e3` pin | DIFFERENT |
| `Samtec-TLW-108-01-F-S_B` (NAUO82) | 0 | base skin | 20.34 x 1.54 x 2.51 | `#ffff80` | `#ffff80` header_yellow | same |
|  | 1 | pins (and the base under the skin) | 20.32 x 10.00 x 2.49 | `#a6a9aa` | `#e3e3e3` pin | DIFFERENT |
| `User Library-PJ-002AH_Body` (NAUO82) | 0 | body | 14.40 x 11.00 x 9.00 | `#181818` | `#1e1616` black_plastic | close (within 6 levels) |
|  | 1 | inside of the barrel | 1.17 x 6.49 x 6.50 | `#181818` | `#1e1616` black_plastic | close (within 6 levels) |
| `User Library-PJ-002AH_Pad` (NAUO82) | 0 | back contact | 0.36 x 12.10 x 3.00 | `#a6a9aa` | `#e3e3e3` pin_silver | DIFFERENT |
|  | 1 | side contact | 2.50 x 6.50 x 0.40 | `#a6a9aa` | `#e3e3e3` pin_silver | DIFFERENT |
|  | 2 | spring contact | 0.25 x 3.50 x 2.50 | `#c0c0c0` | `#e3e3e3` pin_silver | DIFFERENT |
|  | 3 | centre pin | 6.00 x 1.99 x 2.00 | `#c0c0c0` | `#e3e3e3` pin_silver | DIFFERENT |
| `47uf CAP Dcase` (NAUO82) | 0 | base | 6.60 x 1.50 x 8.00 | `#191919` | `#a6a9aa` metal_can | DIFFERENT |
|  | 1 | can | 6.28 x 5.06 x 6.30 | `#191919` | `#a6a9aa` metal_can | DIFFERENT |
|  | 11 solids (2..14) | mark on top | 0.45-5.44 x 0.00 x 0.35-1.89 | `#191919` | `#1e1616` black_plastic | close (within 5 levels) |
|  | 9, 10 | terminal skin | 1.51 x 0.41 x 3.11 | `#191919` | `#a6a9aa` metal_can | DIFFERENT |
| `nano - reg` (NAUO82) | 0, 2 | pin skin | 3.81-6.50 x 0.79 x 2.43 | `#a6a9aa` | `#1e1616` black_plastic | DIFFERENT |
|  | 1 | body (its pins are part of this solid) | 6.50 x 1.69 x 8.30 | `#181818` | `#1e1616` black_plastic | close (within 6 levels) |
|  | 3, 4, 5, 6, 7, 8 | mark on top | 0.31-0.71 x 0.00 x 1.00-1.03 | `#cccecc` | `#1e1616` black_plastic | DIFFERENT |
| `m7 diode` (NAUO82) | 0 | whole part | 6.66 x 2.35 x 2.50 | `#a5926d` | `#1e1616` black_plastic | DIFFERENT |
| `blm21` (NAUO82) | 0 | whole part | 2.76 x 0.95 x 1.30 | `#a6a9aa` | `#1e1616` black_plastic | DIFFERENT |
| `smt_resistor222_a` (NAUO82) | 0 | whole part | 1.70 x 0.60 x 3.80 | `#a6a9aa` | `#1e1616` black_plastic | DIFFERENT |
| `cap106C` (NAUO82) | 0, 1 | terminal skin | 1.71 x 0.59 x 1.21 | `#a6a9aa` | `#a5936d` cap_tan | DIFFERENT |
|  | 2 | body | 1.70 x 1.81 x 4.00 | `#a5936d` | `#a5936d` cap_tan | same |
|  | 3, 4, 5, 6, 7 | mark on top | 0.71-1.70 x 0.00 x 0.19-0.60 | `#cccecc` | `#a5936d` cap_tan | DIFFERENT |
| `led` (NAUO82) | 0 | base with terminals | 4.00 x 0.50 x 1.30 | `#a6a9aa` | `#f5f5f6` white_plastic | DIFFERENT |
|  | 1 | lens | 1.40 x 0.50 x 1.20 | `#d8d8d8` | `#f5f5f6` white_plastic | DIFFERENT |
| `reset core` (NAUO82) | 0 | whole part | 5.20 x 2.15 x 2.80 | `#191919` | `#1e1616` black_plastic | close (within 5 levels) |
| `reset shell` (NAUO82) | 0 | whole part | 3.00 x 1.65 x 4.00 | `#a6a9aa` | `#e3e3e3` pin_silver | DIFFERENT |
| `Copy of JR-3^JR-3_with_cable` (NAUO83-84, NAUO86) | 0 | whole part | 14.00 x 2.75 x 7.90 | `#404040` | `#1e1616` black_plastic | DIFFERENT |
| `Copy of JWT-CONTACT^JR-3_with_cable` (NAUO83-84, NAUO86) | 0 | whole part | 10.00 x 2.20 x 2.00 | `#a6a9aa` | `#e3e3e3` pin | DIFFERENT |
| `Copy of Cable_JR^JR-3_with_cable` (NAUO83-84, NAUO86) | 0 | wire | 40.00 x 1.00 x 2.52 | `#ff9d07` | `#7c5a30` wire_brown | DIFFERENT |
|  | 1 | wire | 39.99 x 1.00 x 1.00 | `#bd291f` | `#ef3340` wire_red | DIFFERENT |
|  | 2 | wire | 40.00 x 1.00 x 2.52 | `#975100` | `#ff851b` wire_orange | DIFFERENT |
| `Copy of JR-3_2^JR-3` (NAUO85, NAUO90, NAUO92) | 0 | whole part | 14.00 x 2.75 x 7.90 | `#404040` | `#1e1616` black_plastic | DIFFERENT |
| `Copy of JWT-CONTACT_1^JR-3` (NAUO85, NAUO90, NAUO92) | 0 | whole part | 10.00 x 2.20 x 2.00 | `#a6a9aa` | `#e3e3e3` pin | DIFFERENT |
| `JR-3 Bridge` (NAUO91) | 0 | whole part | 18.00 x 3.70 x 10.00 | `#404040` | `#1e1616` black_plastic | DIFFERENT |
| `Part1^ARA_Pathways` (NAUO87) | 0 | wire | 112.12 x 65.36 x 25.73 | `#975100` | `#ff851b` wire_orange | DIFFERENT |
|  | 1 | wire | 112.11 x 64.59 x 27.44 | `#bd291f` | `#ef3340` wire_red | DIFFERENT |
|  | 2 | wire | 112.11 x 63.97 x 29.33 | `#ff9d07` | `#7c5a30` wire_brown | DIFFERENT |
| `Part2^ARA_Pathways` (NAUO88) | 0 | wire | 143.75 x 18.65 x 70.93 | `#975100` | `#ff851b` wire_orange | DIFFERENT |
|  | 1 | wire | 142.73 x 17.63 x 70.99 | `#bd291f` | `#ef3340` wire_red | DIFFERENT |
|  | 2 | wire | 141.72 x 16.84 x 71.05 | `#ff9d07` | `#7c5a30` wire_brown | DIFFERENT |
| `Part3^ARA_Pathways` (NAUO89) | 0 | wire | 144.10 x 42.50 x 59.49 | `#975100` | `#ff851b` wire_orange | DIFFERENT |
|  | 1 | wire | 142.50 x 42.32 x 57.54 | `#bd291f` | `#ef3340` wire_red | DIFFERENT |
|  | 2 | wire | 140.91 x 42.14 x 55.61 | `#ff9d07` | `#7c5a30` wire_brown | DIFFERENT |
| `Part4^ARA_Pathways` (NAUO93) | 0 | wire | 92.72 x 52.39 x 14.29 | `#975100` | `#ff851b` wire_orange | DIFFERENT |
|  | 1 | wire | 90.90 x 53.53 x 12.26 | `#ff9d07` | `#7c5a30` wire_brown | DIFFERENT |
|  | 2 | wire | 90.45 x 52.71 x 11.80 | `#bd291f` | `#ef3340` wire_red | DIFFERENT |
| `Part5^ARA_Pathways` (NAUO94) | 0 | wire | 173.37 x 85.62 x 18.55 | `#ff9d07` | `#7c5a30` wire_brown | DIFFERENT |
|  | 1 | wire | 171.87 x 84.59 x 18.01 | `#bd291f` | `#ef3340` wire_red | DIFFERENT |
|  | 2 | wire | 170.04 x 83.57 x 17.57 | `#975000` | `#ff851b` wire_orange | DIFFERENT |
| `Part6^ARA_Pathways` (NAUO111) | 0 | wire | 61.30 x 41.86 x 25.04 | `#ff9d07` | `#ffdc00` wire_yellow | DIFFERENT |
|  | 1 | wire | 61.27 x 40.73 x 25.43 | `#bd291f` | `#3d9970` wire_green | DIFFERENT |
|  | 2 | wire | 58.78 x 39.62 x 26.46 | `#975100` | `#0074d9` wire_blue | DIFFERENT |
|  | 3 | wire | 57.41 x 38.53 x 28.37 | `#404040` | `#a75294` wire_purple | DIFFERENT |
| `Part7^ARA_Pathways` (NAUO112) | 0 | wire | 61.27 x 41.14 x 19.72 | `#c5bdff` | `#ffdc00` wire_yellow | DIFFERENT |
|  | 1 | wire | 61.27 x 40.36 x 19.39 | `#003fd8` | `#3d9970` wire_green | DIFFERENT |
|  | 2 | wire | 58.78 x 39.57 x 17.51 | `#15ff93` | `#0074d9` wire_blue | DIFFERENT |
|  | 3 | wire | 57.12 x 38.79 x 16.24 | `#ffff00` | `#a75294` wire_purple | DIFFERENT |
| `Wire Cap` (NAUO95-110) | 0 | whole part | 1.75 x 1.75 x 8.00 | `#404040` | `#1e1616` black_plastic | DIFFERENT |

**The Nano, mesh `nano_Varsayılan` in NAUO82** (273 solids of ours; 127 differ, all because this project uses `#a6a9aa` for metal
and near-black for a few bodies where the old atlas, taken from the PMG guide, has `#e4e4e4` and light greys). The "What" names are mine, from the SolidWorks body names
(`atmega328`, `ftdi FT232rl`, `MINIUSBSHELL` and so on), sizes and positions; "underside" means below the board (mesh y under 0):

| What | Solids of ours | Size (mm) | Skin? | Cadasio | Ours now | Verdict |
|---|---|---|---|---|---|---|
| ATmega lead skin | 32 | 1.28 x 0.68 x 1.28 | yes | `#a6a9aa` | `#e4e4e4` | DIFFERENT |
| SOLDER MOUND skin, on top of the board | 30 | 1.83 x 1.52 x 1.83 | yes | `#a6a9aa` | `#e4e4e4` | DIFFERENT |
| pin skin, upper part (through the board and above it) | 30 | 0.78 x 3.27 x 0.78 | yes | `#a6a9aa` | `#e4e4e4` | DIFFERENT |
| USB-serial chip lead skin or mark (underside) | 15 | 0.14-1.01 x 0.05-0.98 x 1.01-5.30 | yes | `#181818` | `#e4e4e4` | DIFFERENT |
| programming-header pin skin | 2, 3, 4, 15, 16, 17 | 0.76 x 6.01 x 0.76 | yes | `#a6a9aa` | `#cccccc` | DIFFERENT |
| resistor (underside) | 35, 117, 118, 264, 265 | 3.80 x 0.60 x 1.70 | no | `#a6a9aa` | `#e5eaed` | DIFFERENT |
| LED base | 44, 45, 46, 47 | 4.00 x 0.50 x 1.30 | no | `#a6a9aa` | `#d3d6d3` | DIFFERENT |
| resistor pack: top face | 79, 80 | 1.30 x 0.30 x 3.20 | no | `#181818` | `#ffffff` | DIFFERENT |
| MINI-USB SOCKET (shell and core are one solid in our mesh) | 253 | 9.40 x 4.80 x 10.90 | no | `#cccccc` | `#e4e4e4` | DIFFERENT |
| regulator (underside of the Nano) | 20 | 8.30 x 1.69 x 6.50 | no | `#181818` | `#d3d6d3` | DIFFERENT |
| reset button (core and shell are one solid in our mesh) | 68 | 3.00 x 2.15 x 5.20 | no | `#181818` | `#d3d6d3` | DIFFERENT |
| USB-serial chip lead skin or mark (underside) | 37 | 0.11-1.41 x 0.01-0.52 x 0.04-2.06 | yes | `#e4e4e4` | `#e4e4e4` | same |
| pin skin, lower part (inside the socket strips) | 30 | 0.78 x 6.02 x 0.79 | yes | `#e4e4e4` | `#e4e4e4` | same |
| pad / hole skin in the board | 27 | 0.43-0.90 x 0.00-1.60 x 0.86-0.90 | yes | `#e4e4e4` | `#e4e4e4` | same |
| print on top of the ATmega | 24 | 0.10-1.66 x 0.00-0.40 x 0.10-1.92 | yes | `#e4e4e4` | `#e4e4e4` | same |
| small skin (pad, crystal or resistor end) | 7 | 0.16-0.99 x 0.05-0.50 x 0.16-0.99 | yes | `#e4e4e4` | `#e4e4e4` | same |
| mini-USB contact | 248, 249, 250, 251, 252 | 9.40 x 2.55 x 0.50 | no | `#d3d6d3` | `#d3d6d3` | same |
| LED lens | 50, 51, 52, 53 | 1.40 x 0.50 x 1.20 | no | `#efefef` | `#efefef` | same |
| capacitor (underside) | 34, 272 | 4.00 x 1.81 x 1.70 | no | `#a5936d` | `#a5936d` | same |
| header strip with its 15 pins (one solid) | 5, 6 | 38.10 x 11.75 x 2.54 | no | `#191919` | `#191919` | same |
| resistor pack: body with its 8 terminals (underside) | 69, 70 | 3.00 x 0.46 x 3.20 | no | `#191919` | `#191919` | same |
| ATmega328 body | 91 | 11.22 x 1.10 x 11.22 | no | `#191919` | `#191919` | same |
| USB-serial chip body (underside) | 158 | 10.20 x 1.90 x 9.25 | no | `#191919` | `#191919` | same |
| board (the 30 solder cones on top are part of this solid) | 0 | 43.20 x 4.60 x 18.00 | no | `#000f41` | `#000f41` | same |
| crystal | 81 | 3.39 x 0.80 x 3.39 | no | `#d3d6d3` | `#d3d6d3` | same |
| diode (underside) | 60 | 1.70 x 1.35 x 4.90 | no | `#191919` | `#191919` | same |
| programming header: three 2-pin strips with their pins (one solid in our mesh) | 1 | 5.00 x 11.75 x 7.62 | no | `#181818` | `#181818` | same |

"Merged" solids, where one solid of ours is several Cadasio bodies of different colours (the colour in the tables and in the JSON is
that of the body whose box is nearest; the JSON lists the others under `also_covers`):

| Mesh, solid | Ours is | Cadasio has |
|---|---|---|
| `nano_Varsayılan` 253 | USB shell + core | shell `#cccccc`, core `#a6a9aa` |
| `nano_Varsayılan` 68 | reset button | core `#181818`, shell (3.0 x 1.65 x 4.0) `#a6a9aa` |
| `nano_Varsayılan` 69, 70 | resistor pack body + 8 terminals each | body `#191919`, terminals `#a6a9aa` |
| `nano_Varsayılan` 1 | three 2-pin header strips | `#181818` (one, set) and `#191919` (two, not set) |
| `Tactile-Switch_1` 0 | switch body + four legs | body `#181818`, legs (0.44 x 4.68 x 0.71) `#a6a9aa` |

Per-instance exceptions (the mesh is the same, the colour is not): NAUO55 screw `#c0c0c0` (above); the three contacts in each of the
plugs NAUO90 and NAUO92 (`Copy of JWT-CONTACT_1^JR-3`) show the SolidWorks colour `#fffbf0`, while the same contacts in NAUO85 and in
NAUO83 / 84 / 86 are set to `#a6a9aa`. Both look like omissions; NAUO90 and NAUO92 sit inside the bridge NAUO91.

### 2.4 Which solids are skins

A colour rule for any of these must also recolour the faces under the skin (`"skin": true`), or the body shows through after
simplification, as it does now on the Nano.

| Mesh | Skins (solids of ours) | Cadasio colour | Lies on |
|---|---|---|---|
| `nano_Varsayılan` | 30 solder mounds, 30 upper pin skins, 32 ATmega leads, 6 programming-header pins | `#a6a9aa` | board, header strips, ATmega, header |
| `nano_Varsayılan` | 15 lead skins and marks of the USB-serial chip (underside) | `#181818` (set; probably a slip: the neighbouring ones are unset) | chip |
| `nano_Varsayılan` | 125 others: 30 lower pin skins, pads, print, remaining leads | `#e4e4e4` (not set) | various |
| `nano - reg` | 0, 2 (pins); 3-8 (print) | `#a6a9aa`; `#cccecc` | body |
| `cap106C` (two instances) | 0, 1 (terminals); 3-7 (marks) | `#a6a9aa`; `#cccecc` | body `#a5936d` |
| `47uf CAP Dcase` | 9, 10 (terminals); 2-8, 11-14 (marks) | all `#191919` (not set) | can and base, also `#191919` |
| `Samtec-TLW-*` (17 headers) | 0 (the base) | `#ffff80` (`#ffff7f` on the two 3-pin ones) | the pin solid, `#a6a9aa` |
| `MG90S`, `MG90S_Cut wires shorter` | 25 visible lettering faces inside solid 1 | `#ffffff` | label plate `#ff00ff` |
| wood (44 parts) | engraving (a pocket in our mesh, not a skin) | `#1e1616` | wood |

The headers are already handled this way in `materials.json` (`"rank": 1, "skin": true`), except that the pin colour there is
`#e3e3e3` and Cadasio's is `#a6a9aa`.

### 2.5 Wires: colours, and which way round

Every conductor was followed through our CAD from end to end (pieces that share an end ring), and Cadasio's colour read off each piece.

Servo leads (stub on the servo, cable, 40 mm pigtail in the plug, contact, header pin):

| Servo | Brown `#975100` | Red `#bd291f` | Orange `#ff9d07` |
|---|---|---|---|
| NAUO45 Base Motor | `MG90S` solid 3 > NAUO87 solid 0 > NAUO83 `Cable_JR` solid 2 > contact at (50.0, 112.9, 140.3) on `Samtec-TLW-104-01-F-S_N-7` | solid 4 > NAUO87 solid 1 > NAUO83 solid 1 > (52.5, 112.9, 140.3) on `_R-7` | solid 5 > NAUO87 solid 2 > NAUO83 solid 0 > (55.1, 112.9, 140.3) on `_B-7` |
| NAUO58 Elbow Motor | solid 3 > NAUO88 solid 0 > NAUO84 solid 2 > (50.0, 112.9, 143.0) on `_N-7` | solid 4 > NAUO88 solid 1 > NAUO84 solid 1 > (52.5, 112.9, 143.0) on `_R-7` | solid 5 > NAUO88 solid 2 > NAUO84 solid 0 > (55.1, 112.9, 143.0) on `_B-7` |
| NAUO66 Shoulder Motor | solid 3 > NAUO89 solid 0 > NAUO86 solid 2 > (50.0, 112.9, 152.8) on `_N-6` | solid 4 > NAUO89 solid 1 > NAUO86 solid 1 > (52.5, 112.9, 152.8) on `_R-6` | solid 5 > NAUO89 solid 2 > NAUO86 solid 0 > (55.1, 112.9, 152.8) on `_B-6` |
| NAUO72 Claw Motor | `MG90S_Cut wires shorter` solid 5 > NAUO94 solid 2 > plug NAUO90 at (158.8, 132.7, 142.1) > bridge NAUO91 > plug NAUO92 at (148.0, 132.7, 142.1) > NAUO93 solid 0 > plug NAUO85 at (50.0, 112.9, 155.6) on `_N-6` | solid 4 > NAUO94 solid 1 > NAUO93 solid 2 > (52.5, 112.9, 155.6) on `_R-6` | solid 3 > NAUO94 solid 0 > NAUO93 solid 1 > (55.1, 112.9, 155.6) on `_B-6` |

- Cadasio is consistent: brown always ends on an `_N` header, red on `_R`, orange on `_B`. On this (servo) side of the board the `_N` row
  is at x 48.8 to 51.3 mm, nearest the board edge, and `_B` at x 53.8 to 56.3 mm, nearest the Nano. `cad_pins.md` (another report of this round) reads the board legends
  as `_N` = G, `_R` = V, `_B` = S. Together: brown to G, red to V, orange to S, as the build notes say.
- **Our model has brown and orange the other way round on every lead** (ours orange where Cadasio has brown). `materials.json` lists
  this as unconfirmed, and its note reads `_B` as the G row; that reading is the wrong way round.
- On the claw servo the SolidWorks colours would have put brown on S. The author fixed it in Cadasio by swapping brown and orange on
  the claw servo's stubs and on its cable NAUO94 (typing `#975000` for the brown). So on NAUO72 the stub at mesh z -1.52..-0.52 is
  orange, where the other three servos have brown.
- The claw servo's stubs (0.5 mm long) are not coloured at all in ours: the `MG90S` rule asks for `long` 2 to 4 mm.
- The atlases in the JSON give the right colour per wire solid for every one of these meshes; using them instead of the `across`
  lists removes the question of which end counts as first.

Joystick wires (four separate tubes per bundle, a cap at each end; pin names from `cad_pins.md`):

| Bundle | Solid | Cadasio | Joystick end (cap; z of the pin) | Module end (cap; header) | Pin | Ours now |
|---|---|---|---|---|---|---|
| `Part6^ARA_Pathways` NAUO111, right joystick NAUO81 | 0 | orange `#ff9d07` | NAUO110; 160.8 | NAUO98; `Samtec-TLW-108-01-F-S_B-1` | VRy to A1 S | `#ffdc00` |
| | 1 | red `#bd291f` | NAUO109; 163.3 | NAUO95; `_B-1` | VRx to A0 S | `#3d9970` |
| | 2 | brown `#975100` | NAUO108; 165.8 | NAUO96; `_R-1` | +5V to A0 V | `#0074d9` |
| | 3 | dark grey `#404040` | NAUO103; 168.3 | NAUO97; `_N-1` | GND to A0 G | `#a75294` |
| `Part7^ARA_Pathways` NAUO112, left joystick NAUO80 | 0 | lilac `#c5bdff` | NAUO107; 115.8 | NAUO102; `_B-1` | VRy to A3 S | `#ffdc00` |
| | 1 | blue `#003fd8` | NAUO106; 118.3 | NAUO101; `_B-1` | VRx to A2 S | `#3d9970` |
| | 2 | green `#15ff93` | NAUO105; 120.8 | NAUO100; `_R-1` | +5V to A2 V | `#0074d9` |
| | 3 | yellow `#ffff00` | NAUO104; 123.3 | NAUO99; `_N-1` | GND to A2 G | `#a75294` |

These eight colours are the SolidWorks colours (not set in the step) and they agree with the colours `cad_pins.md` reports for the
real kit (black, brown, red, orange; yellow, green, blue, purple). All 16 caps (NAUO95 to NAUO110) are `#404040`, set in the step.

### 2.6 Things in the Cadasio project that look unfinished or accidental

Worth knowing before copying a colour:

- 205 solids still carry SolidWorks' default grey `#e4e4e4`: the lower halves of the Nano's pins, pads and print on the Nano, the 30
  pads and print on each joystick board, the disc on each potentiometer.
- The 47 uF capacitor on the shield is entirely `#191919` (can, base, terminals, marks): nobody has coloured it.
- 15 lead skins and marks of the USB-serial chip on the Nano's underside are `#181818` while the 37 next to them are unset.
- `m7 diode` is `#a5926d`, one digit off the capacitor tan `#a5936d` used elsewhere; `Samtec-TLW-103` bases are `#ffff7f`, one off `#ffff80`;
  the claw lead's brown is `#975000`, one off `#975100`. Typed by hand.
- NAUO55 and the contacts of NAUO90 / NAUO92 were missed (2.3).
- `MG90S` label magenta `#ff00ff` and the white lettering are SolidWorks colours, not set in Cadasio. Lee describes the label as pink
  with white lettering, so they are as intended.
- The project is not set to start by itself (`autoStart` false) and has no navigation overlay; all 20 published guides have both.

### 2.7 The colour file

`cadasio_mra_colours.json`, 68 atlases and 24 single colours, covering all 92 mesh names of `mra.glb`.

- An atlas is a top-level key with the mesh's name: `bbox_min`, `bbox_max`, `solids: [{name, min, max, colour, ...}]`, in mesh
  coordinates in mm: the form `colour-atlas.json` has, so `"atlas": "<file>#<mesh name>"` works in `materials.json`. For solids that
  exist in our mesh, `min` / `max` are OUR solid's box (so the match is exact with the identity axis map) and `solid` is its index.
  Extra keys: `skin`, `set_in_step`, `cad_colour`, `box_error_mm`, `also_covers`, and for Cadasio bodies with no solid of their own
  `"solid": null` with `inside_solid`, `flat`, `shown`.
- `_single_colour`: one colour for each mesh that is one colour throughout. `_instance_exceptions`: the two cases in 2.3.
- `_instances`: NAUO id -> Cadasio instance, item number, tooltip, meshes, engraved code, proposed name.
- `_conductors`: the tables of 2.5 as data. `_palette_seen`, `_wood`, `_source`, `_how_to_read`.
- Check made: every atlas was passed to `tools/build_model.py` `colour_from_atlas` with the boxes of our solids, for every instance
  of every multi-colour mesh: 550 solids, 0 wrong colours, match score 100% each time.
- One atlas per mesh name serves every instance of that mesh; `MG90S_Cut wires shorter` is its own mesh, so the claw servo's swapped
  stubs need no special case.
- Limits: solid numbers depend on `build_model.py`'s welding (0.001 mm); if that changes, use the boxes. Atlases colour whole solids,
  so the servo lettering, the wood engraving and the "merged" solids in 2.3 are beyond what an atlas alone can do.


## 3. Names

### 3.1 What naming the project carries

Everything, exhaustively (the whole payload was scanned for tooltip, label, title, caption, alias, description, comment and note fields):

| Kind | What is there |
|---|---|
| Custom tooltips | 12 texts, on 781 of the 917 solids (`tooltip_title: custom`, `tooltip_show: true`, `tooltip_text: none`). Table below |
| Wood parts | no tooltip at all (136 solids). The engraved code is the only name |
| Instance names | the SolidWorks names with their instance suffix (`ARA_B8-1`, `MG90S-2`, `Part5^ARA_Pathways-1`). None renamed |
| Item numbers | 1 to 60, nested (`19.1` .. `19.20` inside the shield assembly), numbered automatically: one number per distinct part, so the 15 M3x6 screws are all item 2. `itemNumber` in the CAD tree itself is empty everywhere |
| Meta properties | the six default columns exist (name, item_number, description, quantity, surface_area, volume) but `metaPropertyValues` is empty |
| Selection sets | none (`selectionSets` is empty) |
| Step description, popup text | empty |
| CAD upload comment | "ASDF" |
| Project name / tag | "Mini Robot Arm(MRA)" / "mini robot armmra" |

| Tooltip | Solids | Instances |
|---|---|---|
| Base Motor | 45 | NAUO45 (servo), NAUO46 (its two-arm horn), NAUO83 (its plug and pigtail), NAUO87 (its cable) |
| Elbow Motor | 46 | NAUO58 (servo, at z 104), NAUO59 (horn), NAUO84 (plug), NAUO88 (cable) |
| Shoulder Motor | 46 | NAUO66 (servo, at z 177), NAUO67 (horn), NAUO86 (plug), NAUO89 (cable) |
| Claw Motor | 43 | NAUO72 (servo), NAUO73 (horn), NAUO94 (cable), NAUO90 (the plug on its end) |
| Servo Extension Wire | 12 | NAUO93 (cable), NAUO92 and NAUO85 (the plugs on its ends), NAUO91 (the coupler that takes the claw motor's plug) |
| Joystick | 148 | NAUO80 and NAUO81, the same text on both |
| Nano | 293 | inside NAUO82: the part `nano` (our mesh `nano_Varsayılan`) |
| Nano I/O Module | 97 | inside NAUO82: everything else (board, headers, sockets, jack, capacitor, regulator and so on) |
| 6mm Hex Screw | 15 | NAUO47-52, 55, 57, 63-65, 70, 77-79 |
| 10mm Hex Screw | 8 | NAUO56, 60, 61, 62, 68, 69, 71, 76 |
| 16mm Hex Screw | 4 | NAUO53, 54, 74, 75 |
| Breadboard Wire (F-F) | 24 | NAUO111 and NAUO112 (four wires each) and the 16 end caps NAUO95-110 |

Two things the tooltips settle: which servo TechBox calls which (NAUO58 on the R8 side is the Elbow Motor, NAUO66 on the R7 side the
Shoulder Motor), and that a servo's horn and lead are named as part of that motor.

### 3.2 Engraved codes

The payload cannot give the codes (it has no geometry), only how many characters each part has: every wood part has one flat
engraving body per character. Three characters on CAD `ARA_A7`, `ARA_A8`, `ARA_A9`, `ARA_A10`; two on every other part, including CAD
`ARA_A11` and `ARA_A12`. That already says the CAD names A7 to A12 cannot be the engraved codes.

So I read them from our CAD: the pocket faces `tools/build_model.py engraved_faces()` finds, drawn looking at the engraved face from
outside (unmirrored), each code shown as it comes and turned 180 degrees so that 6 and 9 cannot be confused
(`cadasio_mra_engraved_codes_1.png`, `_2.png`). The reading reproduces the four mismatches already known (CAD B10 = B3, B8 = B7,
B9 = B8, R5 / R6 swapped), agrees with the character counts above, and is the same, part for part, as the independent reading in
`cad_codes_base.md`. The codes are in the "engraved" column of the table in 1.4. The mismatches:

| CAD name | Engraved | | CAD name | Engraved |
|---|---|---|---|---|
| `ARA_B8` (NAUO7) | B7 | | `ARA_A9` (NAUO27) | A12 |
| `ARA_B9` (NAUO8) | B8 | | `ARA_A10` (NAUO28) | A13 |
| `ARA_B10` (NAUO9) | B3 | | `ARA_A11` (NAUO29) | A6 |
| `ARA_R5` (NAUO14) | R6 | | `ARA_A12` (NAUO30, NAUO31) | A9 (two parts) |
| `ARA_R6` (NAUO15) | R5 | | `ARA_C4` (NAUO35) | C6 |
| `ARA_A2_Supplement` (NAUO20) | A3 | | `ARA_C5` (NAUO36) | C4 |
| `ARA_A3` (NAUO21) | A4 | | `ARA_C6` (NAUO37) | C5 |
| `ARA_A4` (NAUO22) | A5 | | `ARA_C7` (NAUO38) | C8 |
| `ARA_A5` (NAUO23) | A7 | | `ARA_C8` (NAUO39) | C7 |
| `ARA_A6` (NAUO24) | A8 | | `TB_TopBot` (NAUO41, NAUO44) | T1 (two parts) |
| `ARA_A7` (NAUO25) | A11 | | `TB_CenterLatches` (NAUO42, NAUO43) | T2 (two parts) |
| `ARA_A8` (NAUO26) | A10 | | | |

Matching: B1, B2, B4, B5, B6 (two parts), R1, R2, R3 (`R3v2`), R4 (`R4v2`), R7, R8, A1, A2, C1, C2, C3, C9.

### 3.3 Proposed student-facing names

Listed per part in the last column of the table in 1.4 and in the JSON (`_instances[*].proposed_name`). The choices, and where the
sources disagree:

| Part | Cadasio tooltip | `guide.py` now | Lee's words | Proposed |
|---|---|---|---|---|
| Wood | none | the engraved code | | the engraved code: B1-B8, R1-R8, A1-A13, C1-C9, T1, T2 (never the CAD name) |
| Servos NAUO45 / 66 / 58 / 72 | Base / Shoulder / Elbow / Claw Motor | "Base Servo"; caption "the base servo" | "Base Motor" | **Base Motor, Shoulder Motor, Elbow Motor, Claw Motor** |
| Horn NAUO46 (two arms) | Base Motor | not named | "double servo horn" | **Double Servo Horn** |
| Horns NAUO59, 67, 73 (one arm) | Elbow / Shoulder / Claw Motor | not named | | **Single Servo Horn** |
| Screws | 6mm / 10mm / 16mm Hex Screw | "6mm Screw"; caption "six 6mm screws" | | **6mm Screw, 10mm Screw, 16mm Screw** (the build-notes wording; "Hex" is Cadasio's addition) |
| Joysticks NAUO80 / NAUO81 | Joystick | "Left Joystick", "Right Joystick" (labels); "Joystick" (parts list) | | **Left Joystick** (NAUO80, the one wired to A2 and A3), **Right Joystick** (NAUO81, wired to A0 and A1) |
| NAUO82 as a whole | Nano I/O Module (and Nano) | "I/O Extension Module"; caption "the extension module" | "I/O Module", "carrier module" | **Nano I/O Module**, "I/O module" for short in captions. It arrives with the Nano plugged in |
| The Nano inside NAUO82 | Nano | caption "the nano" | | **Nano** (hover text for mesh `nano_Varsayılan`; the other meshes of NAUO82 answer "Nano I/O Module") |
| Servo's own lead: plug NAUO83 / 84 / 86 / 90 and cable NAUO87 / 88 / 89 / 94 | the motor's name | captions "the servo", "the servo wire" | | **Base Motor wire** and so on; hover text can simply be the motor's name, as in Cadasio |
| Extension: NAUO93, 92, 85, 91 | Servo Extension Wire | not named | | **Servo Extension Wire** |
| Jumper bundles NAUO111 / 112 and caps NAUO95-110 | Breadboard Wire (F-F) | not named | "breadboard wires" | **Breadboard Wire**; when one wire is meant, by colour: "the yellow breadboard wire" |

Guesses and open points in this table: "Single Servo Horn" is my wording by analogy with Lee's "double servo horn". "wire" for a
servo's lead follows `guide.py` ("Move the servo wire into the L-shaped slot in R4"). Whether the module is called "Nano I/O Module"
(Cadasio), "I/O Extension Module" (`guide.py`, from the build notes) or "I/O Module" (Lee) is Lee's call; one of them should be
used everywhere. The purpose of T1 / T2 (two 38 mm square plates and two crossing 52.6 mm latches standing apart from the arm at
(195, 92..135, 58)) is not stated anywhere in the payload; it looks like a block for the claw to pick up, which is a guess.


## 4. Look settings

Everything the payload says about how the model is drawn. "Scene" values are the project's scene object; "step" values are set by the
one step and override the scene.

| Setting | Value | Where it is stored |
|---|---|---|
| Render style of every solid | `toon` (917 of 917 leaves, set on the solid or its parent) | step, per part: `style` |
| Edges of every solid | `normal` (917 of 917) | step, per part: `style_edges` |
| Edge opacity | 1 (set on 679 leaves, unset on 238: the default) | step, per part: `opacity_edges` |
| Scene render style | `matt` (overridden by the per-part `toon`) | scene: `scene_render_style` |
| **Edge crease angle** | **40** degrees | scene: `scene_edge_angle`. This is the "40" on Cadasio's Toon setting. No part overrides it |
| Edge colour | `#000000` | scene: `scene_edge_colour` |
| Edge width | 1 | scene: `scene_edge_width` |
| Scene edge opacity | 1 | scene: `scene_edge_opacity` |
| Scene edge style | `none` (no effect: edges are switched on per part) | scene: `scene_edge_style` |
| Silhouette | `none` | scene: `scene_silhouette_style` |
| Tangent edges in the CAD upload | not included | `assemblyStructure.includesTangentEdges` false |
| Background | `#ffffff`, single colour | step (scene default `#EEEEEE`, `colour_type` Single, secondary `#EEEEEE`, influence 45, angle 45: unused) |
| Ambient light | colour `#333333`, intensity **2** | colour: scene; intensity: step (scene default 1.2) |
| Directional light | colour `#cccccc`, intensity **1** | scene |
| Light follows the camera | **false** | step: `scene_light_follow_camera` |
| Directional light position | (123.18, 97.90, -41.69) scene units = (519.4, 412.8, -175.8) mm | step: `light_directional.position` |
| Shadows, floor, gloss, textures | no such settings exist | |
| Transparency | none; `transparentBackground` false | |
| Camera | perspective, field of view **45** degrees | `cameraProperties.default_camera`, `scene_camera_fov` |
| Up axis | +y; view cube shown | scene |
| Animation | 800 ms; show and hide fade, moves tween; camera tween, speed 2, no orbit | step |
| Fonts | `PublicSansMedium`, `#637381`, base size 20 | project |
| Project flags | `tooltips` true, `animateStepsViewer` true, `animatePreviousStep` true, `edgesVisibleOnAnimate` true, `stepPrefix` "Step", `autoStart` **false**, `viewerNavigationOverlay` **none**, `interactionPrompt` false, embed 560 x 315 | project |

The camera of the one step:

| | Scene units | mm, assembly space |
|---|---|---|
| Position | (121.351, 90.186, -33.880) | (511.7, 380.3, -142.9) |
| Orbit target | (48.514, 35.938, 23.828) | (204.6, 151.5, 100.5) |
| Distance | 107.602 | 453.7 |
| Rotation (quaternion x, y, z, w) | (-0.11368, 0.86904, 0.23509, 0.42021) | no roll: the camera's right axis is level (y component 0.000) |
| Looks along | | (-0.677, -0.504, 0.536) |
| Elevation above the horizon | | 30.3 degrees |
| Azimuth (atan2 of x over z, target to camera, as `tools/cadasio/digest.py` reports it) | | 128.4 degrees |
| Near / far | 0.0124 / 19913 | |
| Aspect ratio of the authoring window | 2.786 | |

In words: the camera is beyond the claw end (+X), above, on the -Z side, looking back down the arm towards the controller. The model's
box is (-27.2, 87.1, 39.5)..(394.5, 266.0, 208.6) mm, centre (183.6, 176.6, 124.0); the target is 40 mm from that centre. The project's
default camera (before the step) looks at exactly the model centre from 300.3 mm at elevation 45, azimuth 45.

The light: its stored position is 47 mm from this camera position ((7.7, 32.5, -32.9) mm away), so in the saved view it is close to a
headlamp, a little above and to the side of the eye; with `scene_light_follow_camera` false it stays there when the student orbits.
Seen from the origin it is in the direction (0.757, 0.601, -0.256): elevation 37 degrees, azimuth 109 degrees. Whether Cadasio aims
it at the origin or at the orbit target is not in the payload (from the target the direction is (0.638, 0.529, -0.560)).

How this compares with the 20 published guides (`docs/research/dim_style.md`): identical recipe. `toon` + `normal` edges on every solid,
angle 40, `#000000`, width 1, silhouette none, white background set in the first step, ambient `#333333`, directional `#cccccc`, 45 degree
lens are 20 of 20 there. Ambient 2 with directional 1 is the LSM Part 3 / Part 4 / Full Build / Deconstruction setting (LAC 1.75,
PMG 1.875 with directional 1.15). `scene_light_follow_camera: false` is otherwise only set in the five PMG guides. With the shading
formula fitted in that research (pixel = base x (0.2 x ambient + 0.8 x directional x tone), tone 1.0 lit / 0.7 shaded), these numbers
give lit faces 1.20 x the base colour and shaded faces 0.96 x: the rulebook's "about 1.2 x / 0.95 x". That formula was not re-measured here.

Nothing in the payload gives a toon threshold other than the 40 degree edge angle, a toon ramp, or an outline width other than 1.


## 5. Decisions and open questions

1. **USB socket.** Cadasio: shell `#cccccc`, core `#a6a9aa`. Lee asked for the pin silver. In our mesh shell and core are one solid, so
   it is one colour either way: `#cccccc` (Cadasio's shell) or `#a6a9aa` (same as the pins).
2. **Pin silver.** This project uses `#a6a9aa` for every pin, lead, contact and solder mound that has been coloured. Our `pin` /
   `pin_silver` are `#e3e3e3` (the published header-pin colour) and the old Nano atlas uses `#e4e4e4`. Lee's points (a) to (d) all
   imply `#a6a9aa`.
3. **I/O module board.** `#000f41` here (the Nano's navy), `#224bbe` in the published guides and in ours.
4. **Brown and orange on the servo leads** are swapped in ours (2.5). Cadasio and `cad_pins.md` agree on brown = G.
5. **Joystick wire colours.** Ours are placeholders; Cadasio's eight colours match the real kit.
6. **Servo lettering** needs a face-level rule in `build_model.py` (2.2 e); a colour entry cannot do it.
7. **Skins on the Nano and the regulator** (2.4): the atlas gives the colours, but the skin treatment is what makes them show.
8. **Unfinished colours in Cadasio** (2.6): the 47 uF capacitor (all near-black; ours is a silver can), the joystick board's pads
   (`#e4e4e4`), the potentiometer discs, the lower pin halves. Copy, or keep ours?
9. **Dupont housings and wire caps** `#404040` here; the colour library says `#1e1616`.
10. **Names** (3.3): "Nano I/O Module" against "I/O Extension Module"; "Hex Screw" against "Screw"; what T1 / T2 are for.
11. **Not checked**: how the step actually renders (the saved picture was not fetched). Worth one look at the live project for the
    label, the light direction and the USB shell before the colours are frozen.

## 6. How it was done

- `scripts/tree.py`: flattens the payload (world matrix, box, SolidWorks colour and step properties of all 1030 nodes).
- `scripts/ours.py`: splits every mesh of `mra.glb` into connected solids the way `build_model.py` does and stores their boxes.
- `scripts/match_parts.py`, `match_solids.py`: the pairing of 1.3. `skins.py`: the open-shell test of 1.2. `wires3.py`: the conductor
  traces of 2.5. `ourcols.py`: replays `materials.json` through `build_model.py`'s own functions (imported, not run) to get the colour
  our build gives each solid today. `label2.py`, `render_label.py`, `engrave2.py`: the label and engraving pictures.
- `scripts/gen_json.py` writes the colour file; `validate.py` feeds it back through `colour_from_atlas`.
- Nothing in the project was edited; `guide.py` and `tools/build_model.py` were not run.
