# LSM round 2: the LED matrix, its header, its label and the decal system

Read-only investigation, 19 Oct 2026, for Lee's Step 13 note (lee_notes_2026-10-19.md: "the current header looks like a
kindergartener drew it", "there's also a label on the back of the LED Matrix now") and pictures 3.jpg (front) and 4.jpg (back).
Nothing in the repository was changed. All numbers are assembly mm, Y up, "seated" = where `assemble.py` puts the part in
lsm.glb; "own" = the mesh's own frame in `lsm-electronics.glb` (mesh `8x8 LED`, positions x 1000).
Scratch scripts: /private/tmp/claude-501/lsm_matrix/ (a1 - a13.py).

## 0. Short answers

- The matrix's **back** (no LEDs) faces **down** when seated: back face at **y 896.703**, front (LED side) y 897.703, LED tops
  y 899.203. PCB 1.0 mm thick (own z 0 .. 1).
- The **IN corner** (header) is the seated **min-x, min-z corner, (606.92, 1173.785)**; the OUT pads are at the max-x, max-z corner.
  This matches the photo exactly (section 3): photo right = seated +x, photo up = seated +z, viewer below the board.
- The header's pins must point **+z** (from the board edge at z 1173.785 in towards the middle), lying flat under the back face,
  in a row along x: **V+ at x 608.24, IN at 610.78, V- at 613.32** (V+ nearest the edge x 606.92), which is the order the guide
  already uses (white = V+ lowest x, purple = IN, grey = V-).
- The photo shows a **surface-mounted** header: nothing comes through to the front (3.jpg, all four corners checked), and the short
  ends lie in long solder fillets on pads at the edge, like the CAD's OUT pads. So: tails on back-side pads, not legs through the
  board (section 2.2).
- Remove the CAD header by one rule: **drop every triangle of mesh `8x8 LED` with a vertex below own z = -0.05**, then close the
  three 1.5 x 5.0 mm openings it leaves in the back face. `make_atlas.py` must drop the header's atlas entries too, or the
  matrix loses all its colours (section 1.4).
- New sockets: same turn as now, translations **(607.682 | 610.222 | 612.762, 896.219, 1191.26)**; each pin 7.0 mm inside its
  socket (section 2.4).
- Decals attach **by part id** (`"MATRIX"`), via materials.json `"decals": "decals.json"`; text is drawn by the browser's canvas in
  Arial (not polygons), a filled rectangle is `{"fill": [x, y, w, h], "colour": ...}`. Ready-to-use entries in section 4.5.

## 1. The mesh `8x8 LED` and where it sits

### 1.1 Frames

- `assemble.py:239`: `add('MATRIX', from_mesh(EL, '8x8 LED'), at('8x8 LED-4', (0.2, 0.0, -0.2)), ...)`.
- lsm.glb node `MATRIX`: R = [[1,0,0],[0,0,1],[0,-1,0]], t = (639.673, 896.703, 1202.553). So
  seated = (t.x + own x, t.y + own z, t.z - own y), and own = (X - 639.673, 1202.553 - Z, Y - 896.703).
  Own z (the board's normal, towards the LEDs) points up (+y); own y points along -z.
- Mesh: 107 516 vertices, 95 417 triangles, one primitive; own box x -32.75..31.04 (63.79), y -31.65..28.768 (60.42),
  z -6.083..2.5. Seated box x 606.92..670.71, y 890.62..899.20, z 1173.785..1234.203 (assembly-report.json `MATRIX`).
- Welded at 1 micron (as `assemble.py` `split()`), it has **321 solids**. The colour atlas (`colour-atlas-lsm.json` "8x8 LED")
  lists 323 Cadasio solids, matched 100 % (model.report.json: "atlas match 100%; 7234 faces under a skin recoloured").

### 1.2 Solids by kind (own frame; seated in brackets)

| kind | count | size (own x * y * z) | own z | seated | atlas colour |
|---|---|---|---|---|---|
| board body (Cadasio `Boss-Extrude5`), solid 0 | 1 | 63.79 * 60.42 * 8.32 | -6.075 .. 2.25 | back face y 896.703, front y 897.703 | #1e1616 |
| LED bodies (5050) | 63 + 1 | 6.3 * 5.0 * 1.5 (the corner one 5.3 * 5.0) | 1.0 .. 2.5 | y 897.703 .. 899.203 | #fbfbfb |
| LED windows | 63 | 3.6 * 3.6 * 0.1 | 2.4 .. 2.5 | | #a6a9aa |
| capacitors (front) | 56 | 2.01 * 1.01 * 1.0 | 1.0 .. 2.005 | | #b1b3b3 |
| capacitor pads (front) | 112 | 1.5 * 2.0 * 0.1 | 1.0 .. 1.105 | | #b1b3b3 |
| **header blocks** (`Surface-Offset4[1,2,4]`), solids 9, 34, 43 | 3 | 1.516 * 5.016 * 4.05 | -4.05 .. 0 | x 607.915-609.431, 609.815-611.331, 611.715-613.231; y 892.653..896.703; z 1174.777..1179.793 | #b1b3b3 (skin) |
| **header "pins"** (`Surface-Offset4[3,5,8]`), solids 11, 35, 44 | 3 | 1.262 * 4.641 * 1.883 (1044 tris each) | -6.083 .. -4.2 | x 608.04-609.30, 609.94-611.20, 611.84-613.10; y 890.62..892.503; z 1176.652..1181.293 | #b1b3b3 (skin) |
| stray quads (`Surface-Offset4[6,7]`), solids 8, 33 | 2 | 1.55 * 0 * 1.6 (2 triangles, flat) | -4.05 .. -2.45 | z 1176.518, y 892.653..894.253 | #b1b3b3 |
| **OUT pads** (`Surface-Offset5[2,3,4]`), solids 267, 297, 316 | 3 | 2.006 * 5.503 * 0.023 | -0.023 .. 0 | x 663.35-665.36, 665.85-667.86, 668.35-670.36; z 1228.453..1233.956 (0.25 - 5.75 mm from the edge) | #b1b3b3 |
| **"V- Out V+" glyphs** (`Boss-Extrude7[1-7]` + `Surface-Offset5` copies) | 7 * 2 | about 1.0 high | -0.013 .. 0 | x 663.5..670.3, z 1227.20..1228.26 | #b1b3b3 |
| mounting holes (in solid 0) | 6 | round, 2.0 dia, through | | x 614.42 / 663.02; z 1181.60 / 1204.20 / 1226.70 | |

Notes:
- LED grid: columns seated x 610.57 + 8.08 k, rows z 1176.78 + 7.78 k. Caps sit between rows, one per LED pair along z.
- The header in the CAD is Cadasio's: its real body is part of the board's own extrusion (`Boss-Extrude5` reaches down to own
  z -6.075 under the header), with the silver `Surface-Offset4` shells laid over it. Three blocks hang 4.05 mm under the back face
  at 1.9 mm pitch (not 2.54), and under each a 1.26 mm "pin" lies along +z from z 1176.65 to 1181.29, centred y 891.56,
  5.14 mm under the board. That is the "kindergartener" header.
- The OUT corner already matches the photo: three 2.0 * 5.5 mm SMD pads at 2.5 mm pitch, with "V- Out V+" printed inboard of
  them, reading along -x (V- at x 670, V+ at x 664), letter tops towards -z (towards the middle). They are grey #b1b3b3 in the model
  (Cadasio's colour); in the photo the print is white. Leave them, or cover them with a white decal if Lee wants them white.
- The photo has six mounting holes too (not four): two are hidden, one under the label and one partly under the header's plastic.
  Pad and glyph solids are the only things on the back face (none of them more than 0.023 mm proud) apart from the header.

### 1.3 What to remove, by a rule

**Drop every triangle of the `8x8 LED` mesh that has a vertex below own z = -0.05 mm.** Checked (a11.py): this removes
7 462 of 95 417 triangles and touches nothing else:
- the eight `Surface-Offset4` shells entirely (solids 8, 9, 11, 33, 34, 35, 43, 44);
- 3 904 triangles of the board body (solid 0), in three pieces, one under each block (1 300 - 1 302 triangles each);
- everything removed lies in own x -31.875..-26.325, y 21.26..27.776, z -6.083..0 (seated x 607.8..613.3, z 1174.8..1181.3,
  y 890.6..896.7).

After removal the mesh's own box is x -32.75..31.04, y -31.65..28.768, **z -0.023..2.5**, 87 955 triangles.

The board body's back face then has **three rectangular openings** (where the blocks joined it), 4-vertex loops in the plane
own z = 0: own x [-31.75, -30.25], [-29.85, -28.35], [-27.95, -26.45], all at own y [22.768, 27.768] (seated x 607.92-609.42,
609.82-611.32, 611.72-613.22; z 1174.785..1179.785). Close each with two triangles facing own -z, e.g. corners
(x0, y0, 0), (x0, y1, 0), (x1, y1, 0) and (x0, y0, 0), (x1, y1, 0), (x1, y0, 0), normals (0, 0, -1). (`build_model.py`'s
`fill_holes` cannot do it: it only fills round holes straight through a plate, with two rims, build_model.py:333-366.) New pads
at 2.5 mm pitch would not cover these 1.9 mm-pitch openings, so they must be closed in the mesh.

Do it in `assemble.py` (it already splits and rebuilds meshes: `split()`, `sub_mesh()`, assemble.py:143-160), so that lsm.glb, and
with it the generator's collision tests, has the new header too.

### 1.4 The colour atlas must follow (otherwise the matrix goes grey)

`colour_from_atlas()` (tools/build_model.py:492-525) first requires the mesh's overall box to match the atlas entry's box within
0.02 * 63.79 + 0.3 = 1.58 mm on every axis (line 509). The trimmed mesh is 2.52 mm deep in own z; the atlas box is 8.58 mm
(-6.083..2.5), so no axis mapping passes and the whole matrix would get no atlas colours. Fix in `make_atlas.py` (MESHES, line 25):
for `8x8 LED`, drop the solids whose name starts `8x8 LED-Surface-Offset4` and clip the board solid's (`8x8 LED-Boss-Extrude5`) min
z from -6.075 to -0.02, so that the written bbox becomes z -0.023..2.5. (The board body would still be matched to Boss-Extrude5 as
its nearest box even unclipped, but the bbox check comes first.) Then run make_atlas.py before guide.py.

The new header pieces should be **meshes of their own** inside the MATRIX part (e.g. `LED Matrix header`, `LED Matrix header pin`),
not merged into `8x8 LED`, so the atlas box stays the board's; give them materials.json rules (`header_black`, `pin`).

## 2. The header, proposed

### 2.1 Orientation (seated)

- Back face: y 896.703, facing -y. Everything on the back hangs below it.
- IN corner: (x 606.92, z 1173.785). Edge along x at z 1173.785 (where the legs are soldered); edge along z at x 606.92.
- Pins: in a row along x, pointing +z, lying 1.27 mm under the back face.
- Room: D4 (the wall) is at x 594.41..597.41, D9_A (support) at x 617.13..620.13, D10 at z 1202.97..1205.97: all clear of
  what follows. The breadboard and Nano are 12 mm and more below.

### 2.2 What the photo shows (4.jpg, measured on enlargements: hdr.png)

Scale from the pin pitch and the hole columns: 12.0 - 12.2 px/mm. Distances from the board's bottom (IN) edge, px y 1063.7:
- three pins at px x 630.0, 660.75, 690.75 (pitch 30.4 px = 2.54 mm);
- plastic px x 613.7..702.5, px y 961.2..992.5: 7.3 * 2.6 mm, **5.9 to 8.5 mm from the edge**, about 0.4 mm in from the side edge;
- pins from the plastic to the tips at px y 862.5: **8.1 - 8.2 mm past the plastic** (gold for the outer 6.2 mm, silver for the
  2 mm next to the plastic). This is longer than the 6 mm of a standard header; the photo is the reference;
- tails from the plastic to about 0.7 mm from the edge, in solder fillets **0.7 to 4.9 mm from the edge** that lie flat along the
  pin, on pads (like the CAD's OUT pads, which are 0.25 - 5.75 mm from their edge in the CAD and about 0.9 - 4.9 mm in the photo);
- nothing on the front (3.jpg corners): surface mount, no through-holes.
- The bottom-left mounting hole shows just past the plastic's end, about a quarter of it covered.

### 2.3 Proposed geometry (seated assembly mm; own frame in brackets for `assemble.py`)

Middle pin at x 610.78: the mirror of the CAD's middle OUT pad (666.85) about the board's centre x 638.815. The photo, mapped on
the mounting holes (section 3.1), puts the pins at 608.30, 610.83, 613.30: within 0.06 mm.

| piece | seated | own (MATRIX frame) |
|---|---|---|
| pin centre lines (0.64 mm square) | x 608.24 (V+), 610.78 (IN), 613.32 (V-); y 895.433 (1.27 under the face) | x -31.433, -28.893, -26.353; z -1.27 |
| pins, mating part | z 1182.26 -> tip z 1190.26 (8.0 mm past the plastic, as photographed; 6.0 mm standard would end at 1188.26) | y 20.293 -> 12.293 |
| plastic body 7.62 * 2.54 * 2.54 | x 606.97..614.59, y 894.163..896.703 (flat on the face), z 1179.72..1182.26 | x -32.703..-25.083, y 20.293..22.833, z -2.54..0 |
| tails | from the plastic at z 1179.72 to z 1174.60 (0.8 mm from the edge); joggled up to the face: y 895.433 to z 1179.2, rising to y 896.383 (pin touching the face) by z 1178.6, flat on the pad to 1174.60 | y 22.833 -> 27.953; z -1.27 -> -0.32 |
| pads (decal or 0.023 mm solids, silver) | mirror of the OUT pads: 2.0 wide at x centres 608.28, 610.78, 613.28; z 1174.03..1179.54 | x -31.391, -28.891, -26.391; y 23.018..28.521 |
| solder fillets (optional) | 1.3 wide, z 1174.6..1178.6, y 895.95..896.703 round each tail | y 23.95..27.95, z -0.75..0 |

Notes:
- The plastic ends at x 614.59 and covers the left half of the hole at (614.42, 1181.60) (the photo shows a quarter). The CAD board's
  margin from edge to hole column is 7.5 mm against about 8.3 mm on the real board, so both cannot be matched; the pins are kept
  true to the edge.
- `assemble.py` already has `box_mesh(size)` (assemble.py:163-185), flat-shaded boxes from the origin; each piece is
  `(name, V, N, F, m)` with `m` a 4x4 inside the part (translation in mm), and same-named identical meshes are shared
  (assemble.py:329-335), so three pins cost one mesh.
- Colours: plastic `header_black` #181818 (palette already has it), pins `pin` #a6a9aa (the photo's mating ends are gold; the
  palette has no gold).

### 2.4 The sockets (J_WHITE_F, J_PURPLE_F, J_GREY_F)

The `Wire Cap` mesh (own x -1.433..0.317, y -1.66..0.09, z 0..8) is a **tube open at both ends**: identical end faces at z 0 and
z 8, a 1.25 * 1.25 mm bore centred at own (x -0.558, y -0.786) running the full length, and a latch window through its +y wall at
own z 3.25 - 4.5 (a3.py, a4.py). Either end takes a pin; `guide.py` treats the seated min-z end as the open end (`F_TIP`,
guide.py:177) and the max-z end as where the wire leaves (`F_EXIT`, guide.py:176). Keep that.

**Now** (assemble.py:308-309, Cadasio's placement + (1.385, 0.555, 0)): R = diag(-1, 1, -1), t = (608.114 | 610.014 | 611.914,
892.345, 1186.36). Boxes x 607.80-609.55, 609.70-611.45, 611.60-613.35 (1.9 mm pitch, 0.15 mm apart); y 890.68..892.43;
z 1178.36..1186.36; bore y 891.559, on the CAD pins (2.93 mm in).

**Proposed**, one per pin, the same turn R = diag(-1, 1, -1) (window towards the board), bore on the pin axis, open end 1.0 mm off the
plastic, pin 7.0 mm in (tip 1.0 mm short of the wire end):

| socket | pin | t (translation) | box x | box y | box z |
|---|---|---|---|---|---|
| J_WHITE_F | V+ x 608.24 | (607.682, 896.219, 1191.26) | 607.365..609.115 | 894.559..896.309 | 1183.26..1191.26 |
| J_PURPLE_F | IN x 610.78 | (610.222, 896.219, 1191.26) | 609.905..611.655 | same | same |
| J_GREY_F | V- x 613.32 | (612.762, 896.219, 1191.26) | 612.445..614.195 | same | same |

t = (pin x + (-0.558), 895.433 + 0.786, open end z + 8). Socket top 0.39 mm under the back face; 0.79 mm between sockets; the grey
one 2.94 mm from D9_A. Change against now: white (-0.432, +3.874, +4.90), purple (+0.208, +3.874, +4.90), grey (+0.848, +3.874, +4.90).
The pin enters 7.0 mm (any open end from 1182.36 to 1187.36 keeps it 2.9 mm or more).

Sketch for assemble.py (in place of lines 307-309; not applied):

    SOCKET_TURN = np.diag([-1.0, 1.0, -1.0])
    BORE = np.array([-0.558, -0.786])                       # the cap's bore, its own (x, y)
    PIN_Y, OPEN_Z = 896.703 - 1.27, 1183.26                 # pin axis 1.27 under the back face; socket mouth 1 mm off the plastic
    for part_id, x in [('J_WHITE_F', 608.24), ('J_PURPLE_F', 610.78), ('J_GREY_F', 613.32)]:
        add(part_id, from_mesh(EL, 'Wire Cap'), placement(SOCKET_TURN, [x + BORE[0], PIN_Y - BORE[1], OPEN_Z + 8.0]), ...)

(better: compute the pin points from `parts['MATRIX']['place']` and the own-frame numbers of 2.3, so a later nudge of the matrix
carries the sockets.)

Side effects to check in guide.py (other topics): the hand-set wire mid points near the sockets (`LOOSE_MIDS`, guide.py:312-313,
the routes at :408 and :491) were set for sockets 3.9 mm lower, 4.9 mm nearer the edge and at 1.9 mm pitch. `F_EXIT`/`F_TIP`,
the Steps 13 - 15 labels and `f_pose()` follow the model by themselves. `mid(MATRIX)` changes only in y (box min y 890.62 ->
894.163), and the matrix's turns in guide.py are about vertical axes through it, so `P_OVER`, `P_BESIDE`, `P_OUTSIDE` are unaffected.
`SOCKET_OFF = [0, 0, 15]` (guide.py:187) still holds a socket in line with its pin, since the pins point +z. The wires leave the
sockets heading +z (towards the middle of the matrix), at y about 895.4, x 608 - 613, between D4 and D9_A.

## 3. The photo against the model

### 3.1 Which corner, and the mapping

The photo of the back is not mirrored (its print reads normally). Matching features:
- CAD OUT pads at (max x, max z), with "V- Out V+" reading along -x, letter tops towards -z (glyph baselines at own y -25.709 =
  seated z 1228.26, tops at z 1227.20). Photo: pads top-right, the text below them, upside down, "V-" at the right.
- CAD header at (min x, min z). Photo: header bottom-left.
- So **photo right = seated +x, photo up = seated +z**, and the viewer is at -y (right x up = x x z = -y, towards the viewer).

Fitted on the mounting holes (photo px (704.4, 357), (1295.5, 663.6), (1296, 971) against CAD (614.42, 1226.70), (663.02, 1204.20),
(663.02, 1181.60)):

    seated x = 614.42 + (px - 704.4) * 0.08222        (12.16 px/mm)
    seated z = 1226.70 - (py - 357.0) * 0.07345       (13.61 px/mm)

Check: the middle hole comes out at z 1204.18 (CAD 1204.20).

**The CAD board is about 5 mm short in z.** The real board is square (787 * 796 px, about 64.7 * 65.4 mm at 12.16 px/mm; such
boards are sold as 65 * 65 mm), the CAD is 63.79 * 60.42; its hole rows are 22.55 mm apart against about 25.2 on the real board,
its LED rows 7.78 apart against 8.08 across. Positions below are therefore mapped through the hole fit (which squeezes z) and sizes are
given at the true scale (12.16 px/mm). Not something to change now (D9 and D10 are fitted to the CAD board), but worth telling Lee.

### 3.2 The label

- A white square sticker, 155 * 152.5 px = **12.7 * 12.5 mm** (a half-inch square). Black, thin, sans-serif "V- IN V+", capitals
  1.54 mm high, the line 11.1 mm long with wide gaps (V- / IN / V+ centres 3.8 - 4.2 mm apart).
- **Where:** against the IN edge's side (x) edge, about 0.7 mm in; its near edge 21.8 mm from the IN edge, i.e. about 5.2 mm past
  the pin tips, 13.3 mm past the plastic. It covers the middle-left mounting hole, whose centre is 1.4 mm inside its far edge.
- **Mapped:** centre (613.61, 1199.85); at 12.7 * 12.7: **x 607.26..619.96, z 1193.50..1206.20** (covers the hole at
  (614.42, 1204.20), 1.0 mm inside its far edge; 2.2 mm past the proposed sockets' ends, 1.4 mm clear of the "Only ONE Pin" line).
  D9_A (x 617.13..620.13) will hide its last 2.8 mm when seen from below in the box.
- **Reading direction:** rotated 180 degrees against the board's own print: it reads along **-x** with its letter tops towards **-z**
  (towards the header). Read upright, "V+" is at the low-x end, over the V+ pin's side, "V-" at the high-x end:
  V- centre x 618.27, IN 614.45, V+ 610.26 (z 1199.99). The words do not line up with the pins (a loose sticker), but the order does.

### 3.3 The board's print (white, Arial-like, upright: reads along +x, tops towards +z)

| text | seated centre (x, z) | length mm | capital height mm | font size (cap / 0.716) | notes |
|---|---|---|---|---|---|
| WS2812B-64 | (638.52, 1214.25) | 20.9 | 2.57 | 3.59 | regular |
| Better Than Expected | (637.54, 1206.31) | 25.6 | 1.71 | 2.39 (2.5 to come nearer the length) | regular |
| BTE box (white fill) | (636.62, 1199.15) | 10.8 wide | 5.1 high | | box x 631.22..642.02, z 1196.60..1201.70 |
| BTE (black on the box) | (636.45, 1199.18) | 9.3 | 4.11 | 5.74 | bold italic |
| Only ONE Pin | (621.00, 1191.30) | 13.9 | 1.81 | 2.53 | starts at x 614.06, beside the third pin's tip |
| 24 bit color | (636.61, 1191.30) | 11.2 | 1.81 | 2.53 | |
| 64 RGB LEDs | (653.01, 1191.30) | 15.4 | 1.81 | 2.53 | |

Arial at these sizes comes out a little longer than the photo for all but "Better Than Expected" (23 - 24 mm): `width` squeezes
those, but cannot stretch.

## 4. The decal system

### 4.1 Pipeline

1. A kit's `silkscreen.py` (MRA: 110 lines, RCC: 435) writes `decals.json`: `{"_about": ..., "<part id>": [decal, ...], ...}`.
2. `materials.json` names it: `"decals": "decals.json"` (MRA materials.json:383, RCC :608). The LSM's materials.json has no
   `decals` key yet. An inline dict `{part id: [decals]}` also works (build_model.py:1164-1168).
3. `tools/build_model.py:1176-1177` copies `decals[node name]` into that node's glTF `extras.decals` in model.glb, for any kept
   node with that name (not starting `_`). No picture goes into the model; `publish.py`'s `only_parts` copies nodes whole
   (`node = dict(nodes[k])`), so the extras travel to the website.
4. The player (`player/js/core.js:162-215`, `addDecal`): GLTFLoader puts node extras in `userData`; for every **part** (the assembly's
   direct children, core.js:149-150) it draws each decal on a canvas and lays it as a textured quad, made a child of the part, so
   it moves, turns and fades with the part (setFade swaps its `opacity` uniform). It is not pickable (`raycast` off), drawn
   transparent, no depth writes, with `polygonOffset` (-1, -4) so it wins over the face it lies on.

So decals **attach by part id**: the key is the part's node name in lsm.glb, `"MATRIX"` (assemble.py:345 names part nodes by id).
Coordinates are **seated assembly mm**; the player converts them into the part's frame at load (`part.matrixWorld` inverse, before
any pose).

### 4.2 Format

    {"name": "...", "origin": [x, y, z], "u": [..], "v": [..], "size": [w, h], "px_per_mm": 24, "colour": "#f2f2f2", "items": [...]}

- `origin`: the picture's top-left corner; `u`: the way its "right" runs; `v`: the way its "down" runs; `size`: picture mm. The quad's
  corners are origin, +u*w, +u*w+v*h, +v*h; it is seen from the side **v x u** faces. Put `origin` 0.02 mm off the face (MRA:
  `TOP + 0.02`, `UNDER - 0.02`).
- `px_per_mm`: canvas resolution (default 20; MRA 20 - 40). `colour`: the default ink, a CSS colour (hex), not a palette name.
- Items, in picture mm (y down), each with an optional `colour`:
  - text: `{"text": s, "at": [x, y], "size": font size, "rot": degrees, "align": "center"|"left"|"right", "weight": 400, "width": max length}`.
    Drawn with canvas `fillText` in `${weight || 700} ${size}px Arial, Helvetica, sans-serif` (core.js:181), `textBaseline =
    'middle'`, so `at` is about the middle of the capitals. **Fonts, not polygons**: the browser's Arial. `size` is the font size;
    Arial's capitals are 0.716 of it (RCC silkscreen.py:39 `CAP`). Default weight is **700 (bold)**: write `"weight": 400` for
    regular. `width` only squeezes. There is no italic field, but `weight` goes into the font string as written, so
    `"weight": "italic 700"` gives bold italic with no player change.
  - `{"rect": [x, y, w, h], "line": 0.15}`: an outline.
  - `{"fill": [x, y, w, h], "colour": "#..."}`: **a filled rectangle** (the label, the BTE box, the RCC adapter's square pads).
  - `{"circle": [x, y, r]}` filled, or with `"line"` an outline. `{"poly": [[x, y], ...] or [ring, ...]}`: filled even-odd (a ring
    inside another is a hole), or with `"line"` an outline (`"open": true` for a polyline). `{"arc": [x, y, r, from, to]}`.
  - Items are drawn in order: a fill, then text on it.
  - Polygons are only needed for shapes no font gives (the RCC's traced TechBox logo and its FRONT, RCC silkscreen.py:152-221, 355).

### 4.3 Facing for the matrix's back (faces -y)

- The board's own print (upright, reads along +x, tops to +z): `u = [1, 0, 0]`, `v = [0, 0, -1]`; v x u = -y. Top-left = (min x,
  max z): origin `[606.92, 896.683, 1234.203]`, size `[63.79, 60.42]`; picture (px, py) = (X - 606.92, 1234.203 - Z).
- The label (reads along -x, tops to -z): `u = [-1, 0, 0]`, `v = [0, 0, 1]`; v x u = -y. Top-left = (max x, min z).

### 4.4 The asked-for example: a white label with black "V- IN V+"

    {"name": "label V- IN V+", "origin": [619.96, 896.663, 1193.5], "u": [-1, 0, 0], "v": [0, 0, 1], "size": [12.7, 12.7],
     "px_per_mm": 40, "colour": "#1e1616", "items": [
       {"fill": [0, 0, 12.7, 12.7], "colour": "#f4f4f2"},
       {"text": "V-", "at": [1.69, 6.49], "size": 2.2, "weight": 400},
       {"text": "IN", "at": [5.51, 6.49], "size": 2.2, "weight": 400},
       {"text": "V+", "at": [9.70, 6.49], "size": 2.2, "weight": 400}]}

(0.04 mm off the face rather than 0.02, so that it is always drawn over the board's print decal if they ever overlap. One text item
`{"text": "V- IN V+", "at": [5.9, 6.4], "size": 2.2, "weight": 400}` also works, about 8.4 mm long against the photo's 11.1;
three items keep the photo's spacing.)

### 4.5 The rest of the matrix's back, as one decal (draft for an LSM silkscreen.py)

    {"name": "silkscreen back", "origin": [606.92, 896.683, 1234.203], "u": [1, 0, 0], "v": [0, 0, -1], "size": [63.79, 60.42],
     "px_per_mm": 24, "colour": "#f2f2f2", "items": [
       {"text": "WS2812B-64", "at": [31.60, 19.95], "size": 3.59, "weight": 400, "width": 20.9},
       {"text": "Better Than Expected", "at": [30.62, 27.89], "size": 2.5, "weight": 400, "width": 25.6},
       {"fill": [24.30, 32.50, 10.8, 5.1]},
       {"text": "BTE", "at": [29.53, 35.03], "size": 5.74, "weight": "italic 700", "width": 9.3, "colour": "#111111"},
       {"text": "Only ONE Pin", "at": [14.08, 42.91], "size": 2.53, "weight": 400, "width": 13.9},
       {"text": "24 bit color", "at": [29.69, 42.91], "size": 2.53, "weight": 400, "width": 11.2},
       {"text": "64 RGB LEDs", "at": [46.09, 42.91], "size": 2.53, "weight": 400, "width": 15.4},
       {"fill": [0.36, 54.66, 2.0, 5.5], "colour": "#a6a9aa"},
       {"fill": [2.86, 54.66, 2.0, 5.5], "colour": "#a6a9aa"},
       {"fill": [5.36, 54.66, 2.0, 5.5], "colour": "#a6a9aa"}]}

(the last three: the IN pads, mirror of the CAD's OUT pads, x 607.28-609.28 / 609.78-611.78 / 612.28-614.28, z 1174.03..1179.54;
leave them out if the pads are made as solids.) decals.json then is `{"_about": ..., "MATRIX": [<silkscreen back>, <label>]}`, and
materials.json gets `"decals": "decals.json"`; build_model.py (or guide.py, which rebuilds the model when the parts change) puts it
in model.glb. The parts-list picture of the matrix shows the back only if its picture is posed back up.

## 5. Order of work this implies (for whoever makes the change)

1. assemble.py: trim `8x8 LED` (rule 1.3), close the three openings, add the header meshes (2.3), move the three sockets (2.4);
   run it (lsm.glb, assembly-report.json).
2. make_atlas.py: the `8x8 LED` entry without the header (1.4); run it.
3. materials.json: rules for the new header meshes; `"decals": "decals.json"`; an LSM `silkscreen.py` writing decals.json (4.4, 4.5).
4. guide.py: re-check the hand-set wire points near the sockets (2.4), then regenerate and check Steps 13 - 15 and 24 - 31 in the player.
