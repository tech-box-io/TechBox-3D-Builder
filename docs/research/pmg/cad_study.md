# PMG: what the CAD says (pmg.glb), the rigid parts and the case

Source: `PMG Build Instructions/pmg.glb` only (converted from `PMG Full 3D Cadasio Build.STEP`: 296 top-level instances NAUO1..NAUO296,
616 meshes, one grey material, no mesh shared between nodes). Coordinates are millimetres in assembly space (the GLB's metres x 1000), Y up,
parts as the CAD has them, read as `tools/stepgen.py`'s `Model` reads them (top-level instance = child of the root node `PMG Full 3D Cadasio
Build`; the root's transform is the identity). The GLB was read with `docs/research/pmg/scripts/pmglib.py` (the JSON header plus
memory-mapped accessors of the few nodes needed; the whole file was never loaded). Every number is also in `cad_study.json`. Scripts:
`docs/research/pmg/scripts/` (one per section, named below). Nothing in the kit folder was changed.

Status: complete (sections 0 - 8), 19 Oct 2026.

## 0. Summary

1. **Frame:** up +Y; the front (the student, the keys' ends, the display window) is **-X**; the student's right is **+Z**. The table is
   **y 887.79** (the four walls stand on it; the bottom cover H7 is 6.3 mm up). TechBox's Cadasio project uses the same frame (component
   placements equal to 0.001 mm), but its step offsets are in each component's own axes.
2. **Wood:** 17 parts, 3.0 mm plates. **Every engraved code equals its CAD name** (H1 ... H14, all four keys H9; the "v2" of H4, H11, H12,
   H13 is not engraved). `CODES` for guide.py are in 2.2. H5, H6, H7's codes are on their undersides (read with the case turned over).
3. **How the case goes together** (2.4): snap tabs, spring hooks and latches throughout; stepgen's own test finds a free axis only for H3 and
   H8, so nearly every step needs a hand-set direction or path. Tested ways: H2, H3, H4 from behind (+X); H5, H6, H7 a hinge (hooked into
   H2's closed windows, swung into H3's open notches, 8 deg); buttons straight into H6's pockets; H8 from above; keys from the front; H10 a
   hinge on its rear tabs in H4; H11 / H12 down into H10 then back to lock; H13 down its own slope; module down onto H4's back; display and
   matrix Cadasio's tilted two legs; H14 snaps over the brackets' spring hooks (no clean path in the CAD).
4. **Pose copies** (3): built = NAUO78 (module), NAUO76 / 83 / 84 / 85 (buttons black / yellow / white / blue = D4 - D7), NAUO79 (display),
   NAUO81 (matrix), NAUO282 + NAUO283 (USB plug and A end); every other copy is the same mesh moved, with exact (0.000 mm) poses in 3.1.
5. **The I/O module is the MRA's and the RCC's CAD model** (4): MRA -> PMG built is a 120 deg turn (pose in 4.2), MRA -> PMG bench a pure
   move (603.54, 774.17, 1153.85). The built Nano is node **NAUO301** inside NAUO78 (beware NAUO94's node of the same name). The MRA's
   single-mesh Nano and `usb-a-end.glb` are the same models as the PMG's.
6. **Pins** (5): module rows D4 - D9, D11 - D13 in both poses (pins +X built, +Y on the bench); buttons VCC / OUT / GND; display
   CLK / DIO / VCC / GND (pins +Z); matrix VCC / GND / DIN / CS / CLK (pins -Z built). Names checked against Cadasio's label points.
7. **Biggest CAD problems** (7): the built module is **upside down against the published guide** (USB down in the STEP, up in Cadasio);
   the bench has no seated Nano; duplicate node names in the module copies; H10 1.15 mm and H12 0.43 mm out of place; buttons wedged and
   tilted 7 deg; Cadasio's H14 ends somewhere other than the STEP's.

## 1. Frame: front, up, left and right, the table

- **Up is +Y.** Every wood part is right way up in the CAD (the keys on top, the bottom cover H7 underneath).
- **The front (where the student sits) is -X**: H1, the front rail, is the lowest-X part (x 460.4 - 463.4); the four piano keys run from just
  behind H1 (x 463.4) to the back panel H4 (x 587.4 - 590.4); the display window in H14 and the engraved codes of H1, H8, H9 and H10 all face
  or read the right way up from -X. **Back = +X.**
- **Student's right = +Z, left = -Z** (looking along +X with +Y up). H2 is the right side panel (z 1357.2 - 1360.2), H3 the left one
  (z 1220.6 - 1223.9). The case's centre plane is z = 1290.5 (H4, H5, H10 and the keys' pattern are symmetric about it).
- **The table is y = 887.8**: the lowest points of the case are the two side panels H2 / H3 (887.91), the back panel H4 (887.79) and the front
  rail H1 (888.30). The bottom cover H7 is 6.3 mm above the table (its underside y 894.06), so the case stands on its four walls.
- Overall the case is x 457.0 - 601.2 (144 mm deep, including the tabs of H2 / H3 sticking out in front of H1 and the tabs of H5 / H10 behind
  H4), y 887.8 - 1006.7 (119 mm high, to the top of H14), z 1217.6 - 1363.4 (146 mm wide).
- **The Cadasio project's frame is this frame.** Every rigid part of the STEP that also exists in TechBox's Cadasio project has the same
  placement there to 0.001 mm (script `cadasio_names.py`; 1 Cadasio unit = 23.608 mm). The Cadasio step offsets are stored in each component's
  own axes, not the assembly's, so they must be turned by the part's rotation before use (section 2.4 does this).
- **The bench**, where the electronics are wired before the case is built (Cadasio Steps 1 - 25), is at x 630 - 735, behind and to the right
  of the case, on the same table height: the bench I/O module NAUO1 is at x 647 - 700, y 877.1 - 901.7 (its solder tails reach 10.7 mm below
  the case's table; the bench is not the same surface as the case's table, see the end of section 6).

## 2. The wood: H1 - H14 (17 parts, script `wood_basic.py`, `wood_planes.py`, `wood_codes.py`, `wood_outlines.py`)

### 2.1 The parts

All are 3.0 mm plates (exact: the two faces are parallel planes 3.000 mm apart). Sizes are true mesh boxes.

| id | CAD name | engraved code | size x, y, z | lo - hi (mm) | how it sits | role |
|---|---|---|---|---|---|---|
| NAUO63 | H1 | **H1** | 3.1 x 20.8 x 145.8 | x 460.35 - 463.41, y 888.30 - 909.13, z 1217.59 - 1363.35 | upright across the front (normal X) | front rail; closed slots near each end for H2 / H3's front tabs |
| NAUO65 | H2 | **H2** | 136.9 x 49.5 x 3.0 | x 456.98 - 593.85, y 887.91 - 937.46, z 1357.17 - 1360.17 | upright, right side (normal Z) | right side panel: snap tabs to H1 (front), H4 (back), H10 (top); two closed windows for the floor plates' tabs |
| NAUO66 | H3 | **H3** | 136.9 x 49.6 x 3.3 | x 456.98 - 593.85, y 887.91 - 937.47, z 1220.59 - 1223.85 | upright, left side | left side panel, H2's mirror except: two slots **open at the bottom** for the floor plates' other edge |
| NAUO73 | H4v2 | **H4** | 3.0 x 80.9 x 145.7 | x 587.36 - 590.36, y 887.79 - 968.65, z 1217.64 - 1363.34 | upright across the back | back panel: 4 key slots, slots for H2 / H3 / H10 / H11 / H12 / H13, a bottom notch for H5; the I/O module stands 5 mm behind it (held by H10 and H5, section 6) |
| NAUO67 | H5 | **H5** | 137.8 x 3.4 x 139.4 | x 463.38 - 601.14, y 899.97 - 903.39, z 1220.82 - 1360.17 | flat | deck (top of the floor sandwich): four keyhole-shaped openings the buttons come up through; side tabs; rear tongue through H4 |
| NAUO60 | H6 | **H6** | 109.6 x 3.3 x 139.4 | x 463.37 - 572.96, y 897.06 - 900.39 | flat, under H5 | button carrier: four rectangular pockets the button boards sit in; side tabs |
| NAUO68 | H7 | **H7** | 109.6 x 3.3 x 139.4 | x 463.36 - 572.92, y 894.06 - 897.39 | flat, under H6 | bottom cover (plain plate with side tabs) |
| NAUO61 | H8 | **H8** | 3.1 x 30.9 x 139.4 | x 539.58 - 542.68, y 900.15 - 931.05 | upright across the case (normal X), on H5 | cross divider: four windows the keys pass through; tabs down into H5, notches for H11 / H12 at the top |
| NAUO69 - 72 | H9 (x4) | **H9** (all four) | 130.4 x 3.4 x 31.0 | x 463.42 - 593.81, y 913.16 - 916.56; z 1225.0 - 1256.0 / 1258.3 - 1289.3 / 1291.7 - 1322.6 / 1324.9 - 1355.9 (NAUO72, 71, 70, 69) | flat, side by side, 33.3 mm apart | piano keys; the back end is a split snap tab through H4 |
| NAUO64 | H10 | **H10** | 78.6 x 3.0 x 145.7 | x 521.45 - 600.03, y 931.08 - 934.08 | flat | upper deck over the back half; two rear tabs through H4; slots for H2 / H3's top tabs and H11 / H12's tabs |
| NAUO62 | H11v2 | **H11** | 71.2 x 78.0 x 3.0 | x 522.52 - 593.74, y 928.08 - 1006.09, z 1308.46 - 1311.46 | upright (normal Z), right of centre | display bracket (right) |
| NAUO77 | H12v2 | **H12** | 71.2 x 78.0 x 3.0 | x 522.52 - 593.74, y 927.65 - 1005.67, z 1269.52 - 1272.52 | upright, left of centre | display bracket (left); the same outline as H11 (not mirrored), sits 0.43 mm lower |
| NAUO75 | H13v2 | **H13** | 39.1 x 33.5 x 63.5 | x 562.10 - 601.16, y 950.29 - 983.74, z 1258.74 - 1322.24 | tilted 40.0 deg, its face normal (0.643, 0.766, 0) (up and back) | rear brace between the brackets and H4 |
| NAUO74 | H14 | **H14** | 38.5 x 45.1 x 73.7 | x 540.68 - 579.23, y 961.61 - 1006.73, z 1253.66 - 1327.32 | tilted 40.0 deg, outer face normal (-0.766, 0.643, 0) (up and toward the student) | face plate with the display window |

The Cadasio project names them `H1-1`, `H2-1`, `H3-1`, `H4v2-1`, `H5-1`, `H6-1`, `H7-1`, `H8-1`, `PMG_PianoKey_Aug25-1 .. -4` (NAUO69 .. 72),
`H10-1`, `H11v2-1`, `H12v2-2`, `H13v2-1`, `H14-1`.

**Six parts are tilted by a fraction of a degree in the CAD**: H1, H5, H6, H7, H8 and the four keys are all turned 0.177 deg about Z (their
normal is (0.0031, 1, 0) instead of (0, 1, 0)), and H3 is turned 0.293 deg about X. Over the 138 mm of H5 that is 0.43 mm. H2, H4, H10, H11,
H12 are exact; H13 and H14 are at exactly 40.000 deg. So H1 and the floor / key group were mated slightly crooked against the walls. Harmless
in pictures; it is part of why the press fits below look tighter than 0 mm.

### 2.2 Engraved codes: every code matches its CAD name (the "v2" is not engraved)

Found as the faces of a 0.254 mm deep pocket parallel to one face of the plate (as `build_model.py`'s `engraved_faces()` defines them), drawn
as seen from outside that face and read by eye (`codes_sheet.png` in the scratch folder; not kept). Letters 6.35 mm tall, none mirrored.
"Centre" is the middle of the code on the face itself (the pocket's floor middle moved 0.254 mm out to the face). For `guide.py`
(the RCC's form, `CODES = {id: ([nx, ny, nz], [x, y, z])}`):

    CODES = {'NAUO63': ([-1, 0, 0], [460.37, 895.43, 1348.46]),   # H1   front face, letters up +Y, reads toward +Z (upright from the front)
             'NAUO65': ([0, 0, 1], [579.17, 902.27, 1360.17]),    # H2   outer (right) face, letters up +Y, reads toward +X
             'NAUO66': ([0, 0, -1], [578.95, 902.17, 1220.77]),   # H3   outer (left) face, letters up +Y, reads toward -X
             'NAUO73': ([1, 0, 0], [590.36, 894.35, 1348.62]),    # H4   back face, letters up +Y, reads toward -Z
             'NAUO67': ([0, -1, 0], [565.01, 900.08, 1232.30]),   # H5   underside, letters up +X, reads toward -Z (upright with the case turned over)
             'NAUO60': ([0, -1, 0], [470.64, 897.37, 1232.01]),   # H6   underside, same way
             'NAUO68': ([0, -1, 0], [470.80, 894.37, 1231.97]),   # H7   underside, same way
             'NAUO61': ([-1, 0, 0], [539.66, 925.25, 1350.13]),   # H8   front face, letters up +Y, reads toward +Z
             'NAUO69': ([0, 1, 0], [534.35, 916.34, 1348.87]),    # H9   top face, letters up +X (away from the student), reads toward +Z
             'NAUO70': ([0, 1, 0], [534.35, 916.34, 1315.61]),    # H9
             'NAUO71': ([0, 1, 0], [534.35, 916.34, 1282.28]),    # H9
             'NAUO72': ([0, 1, 0], [534.35, 916.34, 1248.94]),    # H9
             'NAUO64': ([0, 1, 0], [580.56, 934.08, 1347.10]),    # H10  top face, letters up +X, reads toward +Z
             'NAUO62': ([0, 0, 1], [576.15, 956.09, 1311.46]),    # H11  +Z face (outward), letters up +Y, reads toward +X
             'NAUO77': ([0, 0, -1], [576.48, 955.66, 1269.52]),   # H12  -Z face (outward), letters up +Y, reads toward -X
             'NAUO75': ([0.643, 0.766, 0], [573.33, 975.94, 1290.22]),    # H13 upper face, letters up (0.766, -0.643, 0), reads toward +Z
             'NAUO74': ([-0.766, 0.643, 0], [547.55, 971.72, 1262.19])}   # H14 outer face, letters up (0.643, 0.766, 0) (up the slope), reads toward +Z

(The tilted parts' normals are the exact plate normals rounded to 3 places: H1 / H8 (-1, 0.003, 0), H5 / H6 / H7 (-0.003, -1, 0), keys
(0.003, 1, 0), H3 (0, -0.005, -1).) Codes are 6.4 x 8.9 - 15.0 mm.

What the codes mean for the cameras (the rule "each wood step is seen from the side its code faces"):

- **H1, H8, H9, H10, H14** face the student (front or top): readable from the front diagonals, the codes upright.
- **H2 / H3** are on the outer faces, near the back (x 579): readable from a side diagonal.
- **H4** is on the back face, low (y 894.4, z 1348.6, the student's right): readable from behind; once the I/O module is on H4's back
  (z 1263.8 - 1317.1) it stays visible (the code is at z 1345 - 1352, clear of the module).
- **H5, H6, H7** are on the undersides, upright only with the case turned over (Cadasio turns the case over for these three: the right
  steps for `flip=True`). In the finished game H6's and H7's codes are covered (H6's by H7) or underneath; H5's is covered by H6.
- **H11 / H12** face outward (+Z / -Z) on the brackets: readable from the side diagonals, partly hidden by H14 and H13 once those are on
  (not ray-tested).
- **H13** faces up and back, under the top of H14: readable from behind and above.

### 2.3 Outlines (what has what, read from the drawings in `wood_outlines.py`)

- **H1**: a plain bar with a closed vertical slot near each end (for the front snap tabs of H2 and H3).
- **H2 / H3**: the side panels. Front end: a split snap tab (two prongs with barbs) pointing -X into H1. Back end: the same pointing +X into
  H4. Top: a split snap tab pointing up into H10, and a sloping top edge (low at the front, y about 918, high at the back, 937.5). Lower
  middle: H2 has two closed windows (y about 900 - 910) for the +Z tabs of the floor plates H5 / H6 / H7; **H3 has two slots open at the bottom
  instead** for their -Z tabs (the two-leg fit: hook into H2's windows, then swing the other edge up into H3's notches).
- **H4**: back panel, wider at the bottom. Four rectangular key slots in a row (y 913 - 916.5); two long slots for H10's rear tabs; vertical
  slots at each side for H2 / H3's rear snap tabs; an opening at the bottom middle for H5's rear tongue; at the top an L-shaped notch at each side
  (for H11 / H12) and slots for H13.
- **H5**: deck. Four keyhole openings (narrow at the back, wide at the front) where the buttons come up; two side tabs on each side edge; two
  small slots for H8's bottom tabs; a narrower rear tongue (z 1260 - 1322) that passes under / through H4.
- **H6**: U-shaped carrier with three fingers: four rectangular pockets (x about 490 - 510) where the button boards lie; side tabs.
- **H7**: plain rectangle with side tabs.
- **H8**: a strip with four windows for the keys, two tabs down into H5, two notches at the top for H11 / H12.
- **H9**: key, 31 mm wide at the front, narrowing behind H8 to a split snap tab with barbs at the back end, through H4's slot.
- **H10**: plate with two rounded rear tabs through H4, two slots for H2 / H3's top tabs (front corners), two slots for the brackets' tabs.
- **H11 / H12**: the same outline (not mirrored): a tab at the bottom into H10, a sloping top edge at 40 deg with spring hooks (slits) where
  the matrix and H14 hang, a hook at the back into H4.
- **H13**: a rectangle with a hook at each end (into the brackets).
- **H14**: trapezoid with a rectangular window (the display shows through it), two slots near its top edge and notches at the bottom.

### 2.4 How each part goes on (scripts `wood_crossings.py`, `wood_sections.py`, `wood_free.py`, `wood_paths.py`)

Three tests: (a) stepgen's own `blocked()` on the six axis directions with its default settings (what the generator will conclude by
itself), with only the parts placed before (Cadasio order); (b) close-up sections of every joint (the plate cut at mid-thickness, the
other parts' material in it); (c) whole paths (from the seat outward, every 0.5 mm / 0.5 deg, turns played about their own point as
the player does): surface points of the moving part tested inside the parts already there, reporting the overlap and where on the moving
part it is. Depth up to about 1.2 mm over a small area = a snap barb or spring arm flexing past, or one of the CAD's press overlaps
(section 7); anything larger, or over a long stretch, is a real collision.

**stepgen's `blocked()` finds a free axis for only two steps: H3 (+X) and H8 (+Y).** Everything else is "no free direction", for
three reasons: the case is snap-fit throughout (split tabs with barbs, spring hooks, latches), several parts go in with a turn, and the CAD
has press overlaps of 0.4 - 1.2 mm (section 7). So **almost every PMG step needs `direction=` or a hand-set `path=` in guide.py.**

The joints (what goes in what; the sections are in the scratch folder, not kept):

- **H1 slots**: closed, 13.7 mm tall, at each end. H2's / H3's front end is a three-prong snap tab: the middle prong fills the slot, the
  upper and lower arms have barbs that pass through and spring out in front of H1, H1's slot bars sitting in the arms' notches.
- **H4 side slots** (y 891.1 - 899.0 and 919.6 - 927.45): two split snap tabs at the back of each side panel.
- **H10 front slots**: H2's / H3's top snap tab, up through H10 (x 530.6 - 538.5); the tab sits 1.15 mm too far back in both (7).
- **H2 windows** (closed, stepped: 16.7 wide at H5's level, 12.7 at H6's, 8.7 at H7's) take the +Z side tabs of H5, H6 and H7 stacked;
  **H3 notches** (12.75 wide, **open at the bottom**, with a spring latch finger each side) take their -Z side tabs. The floor plates are
  therefore hooked into H2 and swung up into H3.
- **H4 bottom notch** (open downward, z 1270.1 - 1320.4, exactly the width of the tongue): H5's rear tongue.
- **H4 key slots** (8.0 x 3.05): each key's split snap tab. **H8 windows** (20.1 wide): the keys pass through. H8 drops (+Y free) with
  two tabs into H5 and its ends into open notches at the top of H2 and H3.
- **H4 long slots** (22.7 wide, z 1243.0 - 1265.7 and 1315.2 - 1338.0, y about 930.8 - 934.3): H10's two rear tabs, which stick out
  9.7 mm behind H4 and have a notch on their inner edges at x 595 - 597 (the I/O module's board edges sit in these notches, section 6).
- **H10 bracket slots**: each bracket's bottom tab, an L-shaped hook that goes down through H10 and forward under it. **H4**: each bracket
  also has a spring snap tab through a closed slot of H4 (y 937.4 - 945.2) and rests in an open notch at the top of H4. So a bracket goes
  down into H10, then slides back (+X) to hook under H10 and snap into H4.
- **Brackets <-> H13**: H13 lies in a slot of each bracket; its two end hooks go into H4 (slots at y about 950 - 958).
- **Brackets <-> H14**: each bracket's top is a spring hook (long slit) through one of H14's two slots near its top edge; at the bottom
  H14 sits under an "ear" of each bracket (H14's bottom notches). The display lies between H14 (in front) and H13 (behind) in a window of
  each bracket; the matrix hangs on the brackets' front edges (section 6).

Ways in (each as stepgen poses relative to the seat, "pull-off" = the side the part hovers on; Cadasio's direction turned into assembly
axes):

| step | stepgen `blocked()` free | tested way in (path tests) | Cadasio's way (turned into assembly axes) |
|---|---|---|---|
| H1 | (datum) | | |
| H2 onto H1 | none | **+X hover, push -X**: only the front barbs flex (overlap 24 mm2, at the barb tips in front of H1); `direction=[1, 0, 0]` | +X 40, push -X (same) |
| H3 onto H1, H2 | **+X** | +X (barbs flex, 1.1 mm) | +X 43.2 (same) |
| H4 onto H1 - H3 | none | **+X**: only H2's / H3's rear barbs flex (0.8 mm). (-Y, coming up from below, cuts through the side panels' tabs) | +X 65 (the digest's "-Y" is in H4's own axes) |
| H5 (case turned over) | none | **two legs, a hinge**: from the seat, turn -8 deg about X through (532.3, 903.39, 1357.17) (the inner face of H2 at H5's top: the H3 side swings down out of the notches and the tongue out of H4's notch), then -Z 5 (tabs out of H2's windows), then -Y 60. Overlaps only 0.4 mm at H2's window edges and 0.6 mm at H3's latches. At -5 deg the H3 edge does not clear. Straight -Y is blocked by the windows. | hover (0.6, -101.5, -95.9); leg 1 to (-0.2, -54.5, 11.4); leg 2 drops in with a 3 deg turn (Cadasio's legs pass through H2) |
| H6 | none | the same hinge, through (518.2, 900.39, 1357.17): 0.4 - 0.9 mm (H2's windows, H5 above, H3's latches) | hover (1.0, -80.4, -109.5); leg 1 to (-0.1, -42.3, 6.8); leg 2 with 3 deg |
| buttons into H6 | none | **-Y** (with the case turned over: straight down into H6's pockets): only the seated overlaps (7) | cross-fade (no move) |
| H7 | none | the same hinge, through (518.1, 897.39, 1357.17): 0.4 mm, plus H3's latch 1.0 mm (not tested with the buttons in: their switches already overlap H7 by 0.3 - 1.4 mm in the CAD, 7) | hover (2.1, -28.9, -136.3), leg 1 to (0, -0.6, 0.1), leg 2 hinges down with 3 deg |
| H8 | **+Y** | +Y: no overlap at all | +Y 94.5 (same) |
| key (each) | none | **-X hover, push +X** through H8's window into H4: only the key's barbs in H4 (1.1 mm). | -X 107.7 (same); the other three appear seated |
| H10 | none | **two legs, a hinge**: from the seat, front up 8 deg about Z through (588.86, 931.08) (the rear tabs in H4's slots), then -X 14 (tabs out of H4), then away (-X 110, +Y 26): 0.9 mm at the rear tab notches. Straight +Y is blocked by H4, straight -X by H2 / H3's top tabs. | hover (-124.7, 26.1, 0); leg 1 to (0.2, 8.9, 0); leg 2 drops 8.9 with a 4 deg turn (same idea) |
| H11 | none | **two legs**: -X 6.7, then +Y 53.1 (Cadasio's): only H4's snap barb (1.3 mm) and the CAD's 1.0 mm overlap with H10 at the seat. Straight +Y is blocked. | hover (-6.7, 53.1, 0): drop 53.1, then +X 6.7 to lock (same) |
| H12 | none | -X 7.6, then +Y 44.5 (Cadasio's): the same, plus its 0.43 mm sink into H10 (7) | (-7.6, 44.5, 0), the same |
| H13 | none | **up its own slope**: pull-off (-0.766, 0.643, 0) x 80: only the 0.39 mm CAD overlap with H12. +Y or along its normal are blocked by H4 and the brackets. | 80.1 along its own X = (-61.4, 51.5, 0) (same) |
| I/O module | none | **+Y 105** (to the held-above copy NAUO94): no overlap at all. +X is blocked (board edges in H10's tab notches, H13) | arrow down from the held-above copy (same) |
| display | none | **Cadasio's two legs**: from the seat, turn 23.32 deg about Z through its middle (564.03, 980.84, 1293.47) with t (-2.29, 2.07, 0), then the same turn with t (-3.98, 13.06, 0): only the seated overlap with the bracket notches (0.9 - 1.1 mm). +Y and along H14's normal are blocked. | copies Display -6 (held) and -7 (intermediate), section 3.3 |
| matrix | none | **Cadasio's two legs**: turn 20 deg about Z through its middle (532.48, 955.89, 1289.1) with t (-5.11, 2.22, 1.37), then t (-4.44, 22.65, 1.4): only the seated overlap. Along its normal or +Y are blocked. | copies Matrix -9 and -8 |
| H14 | none | **no clean way found**: it snaps over the brackets' spring hooks (through its two top slots) with its bottom under the brackets' ears. The least overlap: top out 10 deg about Z through (548, 968) (its bottom), then up its slope 10, then out along its normal: about 1.1 mm at the spring hooks (12 mm2) and 0.7 mm at the matrix's top header. Every straight way overlaps the brackets by 1.1 - 1.5 mm over 20 - 70 mm2. A hand-set two-leg path like Cadasio's is needed. | hover up and back; leg 1 down 57.6; leg 2 a 2 mm nudge with a 7 deg turn. Cadasio's H14 is also re-posed in a hidden set-up step (7) |

The Cadasio guide turns the case over for H5 - H7 (Steps 29 - 36) and back for H8 (Step 37); with `flip=True` the player turns the model.
In assembly coordinates "from below" (-Y) is "from above" for the student while it is turned over.

## 3. The pose copies of the rigid electronics (script `copies.py`, `nano_check.py`)

Each copy is the same CAD part (the same meshes, vertex for vertex), so each transform was fitted on every vertex (Kabsch, same
vertex order): **every residual is 0.000 mm** (rms and max). Poses are in stepgen's form (`turned()` / `pose_out()`): a point p of the
built copy goes to (p - at) turned by r, + at + t; "at" is the built copy's middle (box centre). Plain [x, y, z] = a move only.

### 3.1 Which copy is built (in the finished case), and Cadasio's names

| part | BUILT copy (in the case) | other copies | pose from the built copy |
|---|---|---|---|
| I/O module (with Nano) | **NAUO78**, on the back of H4, board upright (normal X), components and pins facing back (+X), Nano USB end **down** (-Y), digital rows along its +Z edge, D0 at the top | NAUO1 (bench, flat, as the MRA's, Nano board and headers missing: section 4.3); NAUO94 (held 104.7 mm above the built one) | NAUO1: `{"t": [67.79, -43.1, 8.86], "r": [-0.57735, -0.57735, 0.57735, 120.0], "at": [605.78, 932.5, 1290.47]}`; NAUO94: `[0.0, 104.68, 0.1]` |
| button, black cap (D4) | **NAUO76** (Cadasio Big Button Module-5), z 1241.7, under key NAUO72 | NAUO7 (bench, Module-4) | `{"t": [135.22, 43.66, 34.07], "r": [0.749594, -0.661883, -0.00439, 179.94], "at": [506.26, 904.98, 1241.7]}` |
| button, yellow (D5) | **NAUO83** (Module-9), z 1274.3, under NAUO71 | NAUO6 (Module-3) | `{"t": [135.15, 43.39, 15.38], "r": [same], "at": [506.36, 905.25, 1274.25]}` |
| button, white (D6) | **NAUO84** (Module-10), z 1306.9, under NAUO70 | NAUO5 (Module-2) | `{"t": [135.27, 43.26, -3.23], "r": [same], "at": [506.23, 905.37, 1306.87]}` |
| button, blue (D7) | **NAUO85** (Module-11), z 1339.4, under NAUO69 | NAUO4 (Module-1) | `{"t": [135.39, 44.66, -21.64], "r": [same], "at": [506.09, 903.98, 1339.38]}` |
| 4-digit display | **NAUO79** (Display TM1637-2), between the brackets at 40 deg behind H14's window | NAUO80 (bench, Display -4, upright); NAUO129 (a copy 80 mm to the right of the seat, not in Cadasio's project) | NAUO80: `{"t": [97.47, -55.99, -73.17], "r": [0, 0, 1, 40.0], "at": [564.03, 980.84, 1293.47]}`; NAUO129: `[0.22, 0.3, 79.95]` |
| LED matrix | **NAUO81** (Matrix -4), on the brackets' front edges at 40 deg | NAUO44 (bench, upright; Cadasio's bench copy -1 is NAUO44 turned 180 deg about X and moved 29.3 mm in z); NAUO82 (Matrix -6, 143.3 mm to the left); NAUO267 (Matrix -7, 85.9 above) | NAUO44: `{"t": [114.72, -32.07, 116.48], "r": [-0.939693, 0.34202, 0, 180.0], "at": [532.48, 955.89, 1289.1]}`; NAUO82: `[0.0, 0.01, -143.33]`; NAUO267: `[0.0, 85.86, -0.99]` |
| USB right-angle (Mini-B) plug | **NAUO282**, in the built Nano from below | NAUO279 (bench, plugged in the bench Nano), NAUO281 (with NAUO94) | NAUO279: `{"t": [55.86, -5.28, 34.73], "r": [-0.57735, -0.57735, 0.57735, 120.0], "at": [611.18, 900.15, 1296.98]}`; NAUO281: `[0.23, 104.41, 0.1]` |
| USB A end | **NAUO283** (lying behind the case, the built set) | NAUO278 (bench), NAUO280 (hanging, the held-above set) | NAUO278: `{"t": [-59.17, -7.75, 83.24], "r": [-0.707107, 0, -0.707107, 180.0], "at": [655.84, 884.57, 1315.68]}`; NAUO280: `{"t": [-28.75, 59.71, 6.81], "r": [0, 0, -1, 90.0], "at": [655.84, 884.57, 1315.68]}` |
| Nano (loose, one mesh) | (none built: the built Nano is node NAUO301 inside NAUO78, 4.4) | NAUO3 (15.24 above the bench seat), NAUO2 (44.90 above it) | NAUO3 -> NAUO2: `[0.0, 29.66, 0.0]` |

The three USB sets (plug, cable body, A end) belong together: bench NAUO279 + NAUO277 + NAUO278; built NAUO282 + NAUO285 + NAUO283;
held-above NAUO281 + NAUO284 + NAUO280.

**Buttons, paired by cap colour** (the GLB has no colours; the cap colours are TechBox's Cadasio colours of the same components:
Module-1 blue `#0074d9`, -2 white `#ffffff`, -3 yellow `#ffdc00`, -4 black `#000000`; built -5 black, -9 yellow, -10 white, -11 blue), which
matches Cadasio's own cross-fades (Step 33c Module-1 -> -11; Step 34c -2, -3, -4 -> -10, -5, -9) and the wiring order (black D4, yellow D5,
white D6, blue D7). On the bench the buttons stand in a row behind the module (x 641, z 1275.8 / 1289.6 / 1303.7 / 1317.7: black, yellow,
white, blue), boards upright (normal X), caps toward -X, pins pointing down. In the case (left to right for the student: black, yellow,
white, blue under keys NAUO72, 71, 70, 69) the boards lie nearly flat, **tilted 7.1 deg** (board normal (0.124, -0.992, -0.007): the back
edge higher), caps up under the keys, pins pointing back (+X) and 7 deg up. Bench -> built is a half turn (179.94 deg) for all four. The
built buttons are not quite in a row: relative to the black one the others are moved (0.1, 0.27, 32.56), (-0.02, 0.4, 65.17),
(-0.17, -1.0, 97.68): the blue one sits 1.0 mm lower than the others.

### 3.2 Stepgen poses for the guide (built part at its seat; the copy's place as a pose)

These are the "pose copies" the CAD has; the guide moves one part through them (`g.rest_at`, `g.carry`, `path=[...]`). For example the
bench module is the built module at `{"t": [67.79, -43.1, 8.86], "r": [-0.57735, -0.57735, 0.57735, 120.0], "at": [605.78, 932.5, 1290.47]}`
(a 120 deg turn about (-1, -1, 1)/sqrt3: the board goes from upright to flat), and the bench display is the built one turned 40 deg about
+Z (from 40 deg to upright) and moved (97.47, -55.99, -73.17).

### 3.3 Copies TechBox's Cadasio project has that the STEP does not (script `cadasio_copies.py`)

Cadasio's project (415 components) is a different version from this STEP (296). Its extra copies, as poses from the STEP's built copy:

- **Display** (from NAUO79, at its middle): Display -6 (held, Step 47c) `turned([0,0,1], 23.32, mid, t=[-3.98, 13.06, 0])`;
  Display -7 (intermediate, the Transition in Step 48) `turned([0,0,1], 23.32, mid, t=[-2.29, 2.07, 0])`; Display -5 / -1: 48.4 / 85.7
  straight above. So the display goes in tilted 23.3 deg more upright, drops about 11 mm into the bracket notches, then swings back 23.3 deg.
- **Matrix** (from NAUO81): Matrix -8 (held, Step 49c) `turned([0,0,1], 20, mid, t=[-4.44, 22.65, 1.4])`; Matrix -9 (intermediate)
  `turned([0,0,1], 20, mid, t=[-5.11, 2.22, 1.37])`: tilted 20 deg, drops 20.4 mm onto the hooks, swings back.
- **Bench Nano seated**: Cadasio's nano-3 = NAUO2 - 44.90 Y (the STEP has no seated bench Nano, section 4.3).
- **Mounted module**: Cadasio's Ensamblaje_Shield_NANO-2 (Step 46c) and -3 (held above, Step 45c) are **NAUO78 / NAUO94 turned 180 deg
  about X** (and 1.9 / 4.3 mm lower): in TechBox's published guide the Nano's USB end is at the **top**, the USB plug above the module
  (the Step 46c picture shows it so), while the STEP has it at the bottom. See section 7 and the questions.

## 4. The I/O module and the Nano (script `module_compare.py`)

### 4.1 The same CAD model as the MRA's and the RCC's

- **MRA** (`mra.glb` NAUO82, guide.py `MODULE`): 37 meshes; the Nano is one mesh (`nano_Varsayilan`, NAUO126, own_parts). The PMG module
  NAUO78 has 70 meshes: the same shield and headers, but the Nano as an assembly (nano-board, two 15-pin headers, chips, Mini-USB). 23 meshes
  are the same in both files to the vertex (board `Shield_Arduino NANO` 6240 vertices, the 3-, 4- and 8-pin headers, the Nano sockets, the
  jack pad); the others (capacitor, jack body, SMD parts) are tessellated differently but lie within 0.0 - 0.16 mm.
- **RCC** (`rcc.glb` NAUO23): 70 meshes with the same names as the PMG's (the Nano as an assembly too), tessellated differently; every mesh
  lies within 0.03 mm median (0.09 mm at the 95th percentile) of the PMG's after the fit.
- **The MRA's Nano NAUO126 is the same model as the PMG's loose Nanos NAUO2 / NAUO3** (one mesh each, 296070 vertices against the MRA's
  290945): carried with the module it lies within 0.007 mm of NAUO3 brought to the seat.

### 4.2 Transforms (fitted on the meshes common to both files, residual 0.000 mm)

| from | to | pose (stepgen form) |
|---|---|---|
| MRA NAUO82 (and its Nano NAUO126) | PMG **NAUO78, built** | `{"t": [535.75, 817.26, 1144.99], "r": [0.57735, 0.57735, -0.57735, 120.0], "at": [70.03, 115.24, 145.48]}` |
| MRA NAUO82 | PMG NAUO1, bench | `[603.54, 774.17, 1153.85]` (a move only: **the bench module is the MRA's module the same way round**) |
| MRA NAUO82 | PMG NAUO94, held above | `{"t": [535.75, 921.94, 1145.09], "r": [0.57735, 0.57735, -0.57735, 120.0], "at": [70.03, 115.24, 145.48]}` |
| RCC NAUO23 | PMG **NAUO78, built** | `{"t": [-113.02, 5.16, -48.01], "r": [0.707107, 0.707107, 0, 180.0], "at": [718.8, 927.35, 1338.48]}` |
| RCC NAUO23 | PMG NAUO1, bench | `{"t": [-45.23, -37.95, -39.16], "r": [0, 1, 0, 90.0], "at": [718.8, 927.35, 1338.48]}` |

("at" here is the MRA's / RCC's module middle in its own file.) A part cut from `mra.glb` with `tools/cut_part.py` (no `--like`) stays in
the MRA's assembly space, so the first row is exactly its `extra_parts` pose for the PMG's built seat.

### 4.3 The Nano

- **The built Nano is node `NAUO301` inside NAUO78** (the RCC's NAUO86 equivalent; `own_parts: {"NAUO301": ...}`): box x 599.49 - 618.09,
  y 903.12 - 948.12, z 1282.04 - 1300.04 (18.6 x 45.0 x 18.0), middle (608.79, 925.62, 1291.04); board upright, components facing +X,
  pins toward -X into the sockets, **USB end down (-Y)**. **Caution:** NAUO94 contains a node with the same name; trimesh (and so
  `stepgen.Model` / `build_model.py`) keeps the first, NAUO78's, as `NAUO301` and renames NAUO94's `NAUO301_1` (all 61 inner nodes of
  NAUO78 / NAUO94 share names; NAUO1's inner names are different). Worth a check in the generator log the first time.
- Poses of the built Nano (at its middle) for the other places:
  - bench seat (in NAUO1's sockets; Cadasio's nano-3): `{"t": [64.21, -33.21, 15.17], "r": [-0.57735, -0.57735, 0.57735, 120.0], "at": [608.79, 925.62, 1291.04]}`
  - NAUO3's place (15.24 above the bench seat): t `[64.22, -17.97, 15.18]`, same turn; NAUO2's (44.90 above): t `[64.22, 11.69, 15.18]`
  - in the held-above module NAUO94: `[0.0, 104.68, 0.1]`
- **The bench module NAUO1 has no Nano board**: its nano-board and two 15-pin header meshes are missing, but the Nano's chips, USB
  socket, resistors and LEDs are there, floating at the seated place (they match NAUO78's to 0.000 mm). Cadasio shows NAUO1 with 97 of 185
  solids and its own seated nano-3. **NAUO2 and NAUO3 are not seated**: both are one-mesh Nanos straight above the bench seat, 44.90 and
  15.24 mm up. NAUO2 -> NAUO3 is 29.66 mm, the drop of Cadasio's Step 1 (29.8 mm), so NAUO3 was probably meant as the seated Nano but
  sits 15.24 mm too high (its pins well clear of the sockets). For the guide: use one Nano part (NAUO301
  or the MRA's export, as the RCC does) and poses; leave NAUO2 / NAUO3 and the floating chips of NAUO1 out (`omit`, or `own_parts` the
  NAUO1 chips' parent `NAUO387` and never show it).
- On the bench the Nano's USB end points +Z (toward the student's right, as the MRA's); pins down (-Y).

### 4.4 The USB cable ends

- **A end**: the PMG's "USB Cable end" (NAUO278 / 280 / 283, 8678 vertices) is **the same model as the MRA's `usb-a-end.glb`** (fitted vertex
  for vertex, residual 0.000 mm). Its `extra_parts` pose (at [0, 0, 0], as the RCC's `USB_A`): built NAUO283
  `{"t": [814.99, 880.45, 1315.68], "r": [0, 0.707107, 0.707107, 180.0], "at": [0, 0, 0]}`; bench NAUO278
  `{"t": [596.67, 880.95, 1558.07], "r": [0.57735, 0.57735, -0.57735, 120.0], "at": [0, 0, 0]}`; held NAUO280
  `{"t": [622.96, 785.14, 1322.49], "r": [0.57735, 0.57735, 0.57735, 120.0], "at": [0, 0, 0]}`.
- **Mini-B end**: the PMG's plug is a **right-angle** Mini-B ("USB Right Angle", 24.0 x 7.5 x 19.9 mm, 3594 vertices); the MRA's
  `usb-mini-b.glb` is a straight plug with a cable stub (54 x 7.7 x 10.5 mm). Different parts: keep the PMG's.
- Plugged depth: the built plug NAUO282 (y 890.2 - 910.1) enters the built Nano's socket from below; the bench plug NAUO279 enters the bench
  Nano's socket along -Z (socket z 1319.4 - 1328.8, plug from z 1321.8). Cadasio's Step 25 plugs it with a 22.9 mm move.

## 5. The pins the wires go on (script `pins.py`)

### 5.1 I/O module, rows 4 - 9 and 11 - 13 (G / V / S = the CAD's `_N` / `_R` / `_B` header columns)

From the MRA's measured pin tops (`docs/research/mra/cad_pins.json`, top of each male pin), carried by the exact MRA -> PMG transforms.
Equivalently: **built** x = y_MRA + 490.54, y = 1077.98 - z_MRA, z = 1360.51 - x_MRA; **bench** = MRA + (603.54, 774.17, 1153.85); held
above (NAUO94) = built + (0, 104.68, 0.09). So the MRA's `silkscreen.py` positions carry over the same way. Pitch 2.54 within a block of 4,
blocks 4.93 apart (D7 -> D8, D11 -> D12), as on the MRA.

**Pins point +X (straight back, away from H4) when built; +Y (up) on the bench.** Built tips at x = 604.34; bench tips at y = 887.97.

| row | G built | V built | S built | G bench | V bench | S bench |
|---|---|---|---|---|---|---|
| D4 | 604.34, 941.06, 1310.42 | 604.34, 941.06, 1307.93 | 604.34, 941.06, 1305.44 | 653.62, 887.97, 1290.77 | 656.11, 887.97, 1290.77 | 658.60, 887.97, 1290.77 |
| D5 | y 938.52 | y 938.52 | y 938.52 | z 1293.31 | z 1293.31 | z 1293.31 |
| D6 | y 935.98 | | | z 1295.85 | | |
| D7 | y 933.44 | | | z 1298.39 | | |
| D8 | y 928.51 | | | z 1303.32 | | |
| D9 | y 925.97 | | | z 1305.86 | | |
| D11 | y 920.89 | | | z 1310.94 | | |
| D12 | y 915.96 | | | z 1315.87 | | |
| D13 | y 913.42 | | | z 1318.41 | | |

(In each column only the changing coordinate is repeated; built x 604.34 and z G 1310.42 / V 1307.93 / S 1305.44 throughout; bench y 887.97
and x G 653.62 / V 656.11 / S 658.60 throughout.) Built, the rows run down the module from D0 at the top to D13 at the bottom (-Y), with
S nearest the module's middle and G nearest its +Z edge; on the bench they run D0 -> D13 along +Z, G nearest the student's side (-X).

The STEP's own wire caps confirm the built rows: caps NAUO95 - 119 (8 mm along X, x 598.5 - 606.5) sit on D4 G / S, D5 G / S, D6 G / S,
D7 G / S, D8 S, D9 G / V / S, D11 G / V / S, D12 S, D13 S. Cadasio's labels on the bench module (Step 3 onward) anchor on the same blocks.

### 5.2 Button modules (VCC / OUT / GND)

Right-angle pins (Cadasio names the sockets Socket-2 = VCC, Socket-1 = OUT, Socket-3 = GND; their label points lie within 0.4 mm of
these tips on the bench copies). Pitch 2.5 mm. Each `Socket_Blok` mesh is one pin plus its black block; two of the four meshes coincide (the
CAD has the OUT pin twice).

| button | pin | built tip | bench tip |
|---|---|---|---|
| black NAUO76 / NAUO7 (D4) | VCC | 520.29, 906.82, 1244.12 | 641.37, 934.50, 1273.28 |
| | OUT | 520.28, 906.84, 1241.62 | 641.37, 934.50, 1275.78 |
| | GND | 520.26, 906.86, 1239.12 | 641.37, 934.50, 1278.28 |
| yellow NAUO83 / NAUO6 (D5) | VCC | 520.39, 907.09, 1276.67 | 641.40, 934.50, 1287.14 |
| | OUT | 520.38, 907.11, 1274.17 | 641.40, 934.50, 1289.64 |
| | GND | 520.36, 907.13, 1271.67 | 641.40, 934.50, 1292.14 |
| white NAUO84 / NAUO5 (D6) | VCC | 520.25, 907.20, 1309.29 | 641.40, 934.50, 1301.15 |
| | OUT | 520.24, 907.22, 1306.79 | 641.40, 934.50, 1303.65 |
| | GND | 520.22, 907.24, 1304.29 | 641.40, 934.50, 1306.15 |
| blue NAUO85 / NAUO4 (D7) | VCC | 520.12, 905.81, 1341.81 | 641.38, 934.50, 1315.24 |
| | OUT | 520.11, 905.83, 1339.31 | 641.38, 934.50, 1317.74 |
| | GND | 520.09, 905.85, 1336.81 | 641.38, 934.50, 1320.24 |

**Pins point down (-Y) on the bench, and back and slightly up, (0.992, 0.124, -0.005), when built.** On the bench VCC is on the low-z
side; built (the module turned over) VCC is on the high-z side.

### 5.3 Display (CLK / DIO / VCC / GND)

Four right-angle pins on the digit side, their free legs running to the board's end. Pitch 2.4 mm (not 2.54). Names from Cadasio's
labels (within 0.4 mm). **The pins point +Z (toward the student's right) in every copy** (the display turns about Z only).

| pin | built NAUO79 | bench NAUO80 | NAUO129 |
|---|---|---|---|
| CLK | 564.32, 985.73, 1317.22 | 658.58, 928.78, 1244.05 | 564.54, 986.03, 1397.17 |
| DIO | 562.78, 983.89, 1317.22 | 658.58, 926.38, 1244.05 | 563.00, 984.19, 1397.17 |
| VCC | 561.23, 982.05, 1317.22 | 658.58, 923.98, 1244.05 | 561.45, 982.35, 1397.17 |
| GND | 559.69, 980.21, 1317.22 | 658.58, 921.58, 1244.05 | 559.91, 980.51, 1397.17 |

Built, the four tips stand 1.8 mm beyond H11's outer face (z 1311.46 -> 1317.22): the leads leave through the bracket (the CAD's caps
NAUO259 - 262 sit there).

### 5.4 LED matrix input header (VCC / GND / DIN / CS / CLK)

The five-pin right-angle header ('90 5xHeader Pins') at one end of the PCB, legs on the LED side, tips 2.4 mm beyond the PCB's end. Pitch
2.54. Names from Cadasio's labels on its bench copy (Matrix -1 = NAUO44 turned 180 deg about X: its label points fall within 0.2 mm of
these tips once turned). **Pins point +Z on the bench copy NAUO44 and -Z (toward the student's left) when built.**

| pin | built NAUO81 | bench NAUO44 | NAUO82 | NAUO267 |
|---|---|---|---|---|
| VCC | 536.96, 959.66, 1223.15 | 648.21, 918.05, 1471.53 | 536.96, 959.67, 1079.82 | 536.96, 1045.52, 1222.16 |
| GND | 535.33, 957.72, 1223.15 | 648.21, 920.59, 1471.53 | 535.33, 957.73, 1079.82 | 535.33, 1043.58, 1222.16 |
| DIN | 533.70, 955.77, 1223.15 | 648.21, 923.13, 1471.53 | 533.70, 955.78, 1079.82 | 533.70, 1041.63, 1222.16 |
| CS | 532.06, 953.83, 1223.15 | 648.21, 925.67, 1471.53 | 532.06, 953.84, 1079.82 | 532.06, 1039.69, 1222.16 |
| CLK | 530.43, 951.88, 1223.15 | 648.21, 928.21, 1471.53 | 530.43, 951.89, 1079.82 | 530.43, 1037.74, 1222.16 |

Built, the header is at the matrix's left (-Z) end, beyond its last LED block: tips at z 1223.15, 2.4 mm past the PCB (z 1225.54),
46 mm to the left of H12 and above the top of the side panel H3 (y 952 - 960 against H3's top at 937.5); the CAD's caps NAUO134 - 138
sit there. On the bench (NAUO44, upright) VCC is lowest.

## 6. The case's datum and where each electronic part sits (script `seats.py`)

- **Datum:** H1 (Cadasio Step 26 shows H1 alone in place, then adds H2). The table is y 887.79; the case centre plane z 1290.49.
- **Buttons, in H6's pockets** (case turned over, from above): each board lies in a pocket of H6 (its front edge, x 492.2, on H6), its back
  edge (x 514.0 - 514.4) pressed up against H5's underside, the switch body down on H7, and the cap just under the key (black: touching; yellow
  and white: 0.2 / 0.3 mm into the key's underside). The cap comes up through H5's keyhole opening. Under keys: black NAUO72 (z 1225 -
  1256), yellow NAUO71, white NAUO70, blue NAUO69.
- **I/O module, on the back of H4**: the board stands 4.97 mm behind H4's back face (board back x 595.33, H4 x 590.36), its two side edges
  in the notches of H10's two rear tabs (x 595.3 - 597.0, y 931.1 - 934.2, at z 1265.9 and 1315.0), its barrel jack (at the bottom, the
  board's USB end) resting on the end of H5's rear tongue (y 902.99 = the tongue's top, x 597.0 - 601.2), and one corner touching H13 (y
  952). It comes down from above (+Y free all the way to the held-above copy NAUO94). With the module the other way up (Cadasio's), the jack
  would be at the top and the board would rest on something else: not checked.
- **Display, between the brackets** at 40 deg: the PCB's two lower corners in notches of H11 and H12 (x 557.0 - 558.7, y 970.8 - 973.6;
  overlaps 0.9 / 1.1 mm), the digits behind H14's window (H14 touches the display's face, 0.14 mm), H13 behind. Its ends cross the bracket
  planes (it is 47.5 mm long, the brackets 39 mm apart): it sits in the brackets' windows.
- **Matrix, on the brackets' front edges** at 40 deg (below and in front of H14, LEDs facing the student): the female headers of the LED
  modules at both long edges of the PCB (y 941.3 and 959.7 - 960.1 in the tilted plane) sit in the hooks of the brackets' front edges
  (z 1269.75 - 1272.8 and 1309.2 - 1310.8; overlaps 0.5 - 1.1 mm); the PCB touches H11 at one spot.
- **USB plug** NAUO282: in the built Nano from below; touches no wood. The built cable (NAUO285) runs back along the table to the A end
  NAUO283, which lies partly below the table (y 880.3 - 888.8).
- **The bench is not a surface**: the bench module NAUO1 sits 10.7 mm below the case's table (its solder tails at y 877.1), the bench
  buttons hang in the air behind it (pins down, tips at y 934.5), the bench display and matrix stand on edge at different heights (y 913.3
  - 937.3 and 907.8 - 939.8). Fine for the guide (each is placed by a pose), but the bench is not one plane to put on a table.

## 7. What looks wrong or missing in the CAD

1. **The built I/O module is upside down against the published guide.** In the STEP (NAUO78, and NAUO94 above it) the Nano's USB end
   points down and the right-angle USB plug is underneath the module (y 890 - 910, 2.4 mm above the table). In TechBox's Cadasio project
   the mounted module (Ensamblaje_Shield_NANO-2) and the held one (-3) are NAUO78 / NAUO94 turned 180 deg about X (and 1.9 / 4.3 mm lower):
   USB end up, the plug and cable at the top (the Step 46c picture shows the cable leaving the top of the module). The STEP is consistent
   with itself (its USB cable NAUO282 / 285 / 283 and its wire caps fit the USB-down module), so either the engineer changed it on purpose
   or one of the two is wrong. **Question for Lee.**
2. **No seated Nano on the bench.** The bench module NAUO1 has no Nano board or Nano headers (the Nano's chips, USB socket and LEDs float
   in place); the two loose Nanos NAUO3 / NAUO2 hover 15.24 / 44.90 mm above the seat (NAUO3 was probably meant to be seated: NAUO2 ->
   NAUO3 is Cadasio's 29.8 mm drop). Use one Nano part with poses (section 4.3).
3. **Duplicate node names:** NAUO78 and NAUO94 share all 61 inner node names (NAUO297 - 357), including the Nano's `NAUO301`. stepgen
   keeps NAUO78's as `NAUO301` (the first in the file) and NAUO94's becomes `NAUO301_1`; `own_parts` must name `NAUO301`, and NAUO94 should
   be left out of the model anyway. NAUO1 also repeats `NAUO441` / `NAUO442` inside itself (two reset buttons), harmless. The button
   instances share their inner names too (NAUO376 - 382 in every button).
4. **Small turns in the wood:** H1, H5, H6, H7, H8 and the four keys are turned 0.177 deg about Z; H3 0.293 deg about X; H1 also about
   0.29 deg about X (its two slots are 0.69 mm apart in height), so **H2's front snap tab sits 0.65 mm low in H1's slot** (its lower barb
   overlaps H1 by 0.65 mm), while H3's fits.
5. **H10 sits 1.15 mm too far forward** against the top snap tabs of H2 and H3 (both overlap H10's slot edge by 1.15 mm); H10's rear tabs and
   other slots fit.
6. **H12 sits 0.43 mm lower than H11** (y 927.65 against 928.08; the same outline): it sinks 0.43 mm into H10 along its whole bottom edge,
   0.39 mm into H13, 0.46 mm into H14 and 0.38 mm into H8. Both brackets' bottom hooks also overlap the front edge of H10's slot by 1.0 mm.
7. **Buttons wedged and tilted.** The built buttons lie tilted 7.1 deg; each board's back edge goes 1.0 - 1.25 mm into H5's underside, the
   switch bodies 0.3 - 0.7 mm into H7 (the blue one 1.36 mm, and its pins 0.5 mm), the yellow and white caps 0.2 / 0.3 mm into the keys. The
   blue button sits 1.0 mm lower than the other three. Their spacing (32.5 - 32.6 mm) is not the keys' (33.3).
8. **Press overlaps elsewhere:** display PCB corners 0.9 / 1.1 mm into the bracket notches; matrix headers 0.5 - 1.1 mm into the bracket
   hooks; H11 / H12 to H14 0.13 / 0.46 mm; H4 to the keys' and brackets' snap tabs 0.43 mm; H2 / H3 to H4 0.25 mm. Harmless in pictures,
   but they and the snap barbs are why stepgen finds no free direction for most steps (section 2.4).
9. **H14's final place in Cadasio is not the CAD's.** A hidden set-up step (Step 143) moves and turns the whole H14 component (about 7 deg)
   and its solids carry further offsets to the end, so the published Completed View shows H14 away from the STEP's pose (by my reading of
   Cadasio's transforms about 26 mm and 1 deg, **not verified**; the digest called it a "CAD-pose quirk"). The STEP's own H14 interlocks with
   the brackets (hooks through its slots, bottom under the ears) and its window lies over the display's digits, so I take the STEP's pose as
   the seat. Worth a look against Cadasio's Completed View picture.
10. **No colours**: one grey material for everything (the colours must come from a colour atlas of TechBox's Cadasio project, as for the RCC).
11. **Cadasio's project is a different CAD version** (415 top-level components against the STEP's 296): it has copies the STEP lacks
    (display -6 / -7, matrix -8 / -9, nano-3 / -4 / -5, module -2 / -3 as in item 1), and the STEP has copies Cadasio lacks (NAUO129,
    NAUO44's place). Cadasio's bench matrix (-1) is NAUO44 turned 180 deg about X (its input header at the other end).
12. **The bench is not on one surface** (section 6), and the built USB A end lies 7.5 mm below the case's table.
13. **Not checked here:** whether the module's Nano sockets and the female headers are solid blocks (they were on the RCC, the same module
    model, which made every plug-in look stuck to the generator); the wires and wire caps (another report); the colours.

## 8. Notes for whoever writes `guide.py`

- **Ids**: wood as in 2.1 (the CAD name = the engraved code; only H4, H11, H12, H13 carry "v2" in the CAD name). Built electronics:
  `MODULE = 'NAUO78'`, Nano `own_parts: {"NAUO301": ...}` (or the MRA's Nano export, below), buttons NAUO76 / 83 / 84 / 85 (black / yellow /
  white / blue = D4 / D5 / D6 / D7), display NAUO79, matrix NAUO81, USB plug NAUO282, USB A end NAUO283 (or the MRA's `usb-a-end.glb`).
  Leave out (`omit`) every other copy: NAUO1, NAUO2, NAUO3, NAUO4 - 7, NAUO44, NAUO80, NAUO82, NAUO94, NAUO129, NAUO267, NAUO278 - 281,
  and the CAD's cable bodies; use the poses of section 3 instead (`rest_at`, `carry`, `path=`).
- **Reusing the MRA / RCC parts** (Lee's request): the module is the same CAD model in all three kits. Cut from `mra.glb` with
  `tools/cut_part.py` without `--like` (it stays in the MRA's assembly space), the MRA module NAUO82 and its Nano NAUO126 go to the PMG's built
  seat with `extra_parts` pose `{"t": [535.75, 817.26, 1144.99], "r": [0.57735, 0.57735, -0.57735, 120.0], "at": [70.03, 115.24, 145.48]}`
  and to the bench with `[603.54, 774.17, 1153.85]`. The RCC's `nano-mra.glb` is the same Nano export (cut `--like` the RCC's NAUO27); for the
  PMG cut it again (`--like "PMG Build Instructions/pmg.glb" NAUO3` puts it 15.24 mm above the bench seat, so its pose to the bench seat is
  `[0, -15.24, 0]`, and to the built seat the inverse of section 4.3's NAUO3 pose). The A end: `usb-a-end.glb` with the poses of 4.4. Nothing
  else in the PMG (buttons, display, matrix, right-angle Mini-B plug, wood) exists in the MRA or RCC.
- **CODES**: section 2.2 (copy as it is).
- **Hand-set directions / paths** (section 2.4): H2, H3, H4 `direction=[1, 0, 0]`; H5, H6, H7 the hinge path (turn -8 deg about X at H2's
  inner face, then -Z 5, then -Y), with `flip=True` for H5 - H7 and the buttons (Cadasio turns the case over for exactly these); buttons
  `direction=[0, -1, 0]`; H8 `[0, 1, 0]`; keys `[-1, 0, 0]`; H10 the hinge (front up 8 deg about Z at H4, then -X); H11
  `path=[[-6.7, 53.1, 0], [-6.7, 0, 0], [0, 0, 0]]` and H12 `path=[[-7.6, 44.5, 0], [-7.6, 0, 0], [0, 0, 0]]` (down into H10, then back to
  lock, as Cadasio); H13 up its own slope (-0.766, 0.643, 0); module `[0, 1, 0]` (from the held-above copy, 104.7 mm); display and matrix
  Cadasio's two legs (3.3); H14 a hand-set two-leg path (no clean one exists in the CAD).
- **Lead lines**: the joints in 2.4 are the anchors (tab -> slot); for the floor plates Cadasio draws them to H2's windows and H3's notches.
- **Pins** for labels and wire ends: section 5 (`cad_study.json` `pins`).
