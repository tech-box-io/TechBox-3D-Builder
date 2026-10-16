# RCC: the printing (silkscreen.py, decals.json) and the new decal shapes in js/core.js

Work of 15 Oct 2026. Files written: `RCC Build Instructions/silkscreen.py` (writes `RCC Build Instructions/decals.json`),
`js/core.js` in both kits (the same file, byte for byte), and this report. Nothing else in the kit folders was changed;
guide.py, build_model.py and bundle.py were not run. For the print to show in the RCC guide, the RCC's `materials.json` needs
`"decals": "decals.json"`, and `build_model.py` has to be run.

    .venv.nosync/bin/python "RCC Build Instructions/silkscreen.py"      # writes decals.json; needs numpy and Pillow (the venv has both)

Coordinates are RCC assembly mm (Y up). Every decal sits 0.02 mm above its face, as on the MRA.

## 1. What is printed

| part | decal | source | ink |
|---|---|---|---|
| NAUO1 L1 | `engraving FRONT`: "FRONT" at the front-left corner of the top face | Lee's drawing L1_etching.png | palette `ink` #1e1616 |
| NAUO23 I/O module | `silkscreen top`, `silkscreen underside`, `capacitor print`, `regulator print` | the MRA's decals.json, read at run time and turned onto the RCC board | as on the MRA (white on navy) |
| NAUO26 adapter | `silkscreen long arm`, `silkscreen short arm`, `capacitor print` | Lee's photo l_adapter_board.jpg | #000000 |
| NAUO30 controller | `silkscreen L-JS`, `silkscreen R-JS`, `silkscreen centre`, `logo`, `capacitor print` | the Cadasio project's TopSilkscreen~j5tP solids (positions) + Lee's photo (letter sizes) | #000000 |

The board print is black #000000, the house colour for breadboard legends (black print on a white body). The capacitor
band is #1e1616 and the solder pads are #a6a9aa (metal).

### 1.1 I/O module (NAUO23)

This is the same board model with every part in the same place, turned a quarter turn about Y (reuse_and_colours.md 1.3). `p_RCC = R p_MRA + t`, with
`R = [[0,0,-1],[0,1,0],[1,0,0]]` and `t = [864.282, 812.112, 1268.449]`. Only each decal's origin, u and v change; the items stay as they are.
silkscreen.py reads `MRA Build Instructions Prototype/decals.json`, so a later change to the MRA's module print carries over the next time this script runs.
Checks: the board's corners land on the RCC board to 0.002 mm, and the MRA's digital G column (x 50.085) lands on the RCC's G pins (z 1318.53).
The adapter covers part of the top print, as on the real car.

### 1.2 Adapter (NAUO26): from the photo

The decal frames read like the photo: right = −z, down = +x. Photo → assembly: x = 694.64 + (Y − 268)/16.45, z = 1320.97 + (1160 − X)/16.5.
This mapping matches the board edges to 0.5 mm and the header pins to 0.25 mm. Each mark was measured as a dark blob on the photo
(sizes below are capital heights):

- **U1 / U2**: labels at (x 716.32 / 729.10, z 1325.5), 0.73 mm bold. Each has a rectangle round the header body, 0.15 mm out, line 0.2.
- **LWh / RWh**: at (717.20 / 729.99, z 1316.08), 1.3 mm, squeezed to 3.55 / 3.7 mm long. They read up the board (`rot: -90`), with the letter tops toward +z.
- **S V G**: under each header at x 719.84 (U1) and 732.63 (U2), each letter centred on its pin. **S is on z 1323.51 (+z)**, V on 1320.97, G on 1318.43. 1.67 mm, regular weight, squeezed to the photo's narrower letters.
- **U3**: label at (743.09, 1316.19), 0.72 mm bold, with a rectangle round the 2x4 socket.
- **C1**: label at (747.98, 1329.43), 0.79 mm bold.
- **TechBox icon** (no wordmark): fitted to the photo box x 739.20–748.32, z 1335.88–1341.76 (9.12 mm high). It comes out 6.00 mm wide against the photo's 5.88.
- **Solder pads** (extra, not in the brief, easy to drop): the underside sockets' joints. Round pads 1.64 mm across and one square pad per socket, at the CAD's pin positions (reuse_and_colours.md 3.2 #14). The CAD's pin tips stand up through them, as in the photo.
- **Capacitor top** (can r 2.95 flat, top y 937.88): a dark band on the −x side, cut off 1.45 mm from the can's centre.
  "470 / 10V / RVT" read toward +x (`rot: 90`), with 470 the −z line. The letters are 1.15 mm high at a 1.5 mm line pitch. The
  block sits 0.5 mm along its lines away from the band and 0.2 mm toward the letter tops, as measured.

### 1.3 Controller (NAUO30): Cadasio positions, photo sizes

The frames read like the photo: right = +z, down = −x. The Cadasio payload gives each TopSilkscreen solid's box
(own x → z + 1048.013, own y → x + 603.216, × 1/scaleFactor). That gives exact positions for the outlines (L-JS, R-JS, H1, H2, NRF, C1),
drawn with their outer edge on the solid's box, line 0.2.

The real board's letters are about 1.36–1.47 x the CAD's. Measured on the photo
(board plane: z = 983.23 + X/6.975, x = 727.5 − (Y − 549)/6.99, matching TECHBOX to 0.1 mm):

| text | anchor (x, z) | cap height | notes |
|---|---|---|---|
| L–JS | 733.755, from 1092.1 | 1.1 | left-aligned where the CAD's starts |
| R–JS | 733.63, from 1146.2 | 1.15 | ends 0.5 mm short of its outline |
| H2 / H1 | 733.4, on 1105.29 / 1120.53 | 1.1 | mostly hidden by the sockets in a view from above, as in the photo |
| NANO BOARD / CONTROLLER | from 722.2 (reading −x), centred z 1114.15 / 1110.85 | 2.0 | `rot: 90` (tops toward +z); letter tops on the CAD's line |
| NRF24L01 | 707.55, on 1130.57 | 1.2 | 7.9 long |
| C1 | 705.55, from 1133.2 | 1.0 | |
| USB | 692.0, on 1112.9 | 2.0 | half under the guard's rim, as on the real board |

- **C1's outline**: two open brackets round the can's base, with the + corners (+z) cut off. Only a sliver shows outside the base.
- **Not drawn**: the "+" and "−" polarity marks, which sit under the can.
- **Capacitor top** (top y 926.237): the band on the −z side, with the same text block as on the adapter (`rot: 0`).
- **Logo**: icon fitted to solids 144–148 (x 681.45–688.66, z 1155.04–1159.83); it comes out 4.75 wide against the Cadasio's 4.79.
  The wordmark is laid on the seven letter solids 149–155 with one scale and offset, to **0.02 mm**: the board's wordmark is the same artwork as logo.webp.
  On the board the icon is 1.10 x larger relative to the wordmark than in logo.webp. The photo agrees with the board: icon 52 px high against letters 42 px, ratio 1.24 (CAD 1.215, logo.webp 1.33).

Not printed: the faint lines on both boards are copper traces under the mask. No underside print (no photo, nothing in the Cadasio).

### 1.4 The TechBox logo shapes

The Cadasio payload does not hold the silkscreen's outlines. It gives only each solid's box; the meshes are external Draco files
(`*.drc`) that are not in the payload, and their `.edges` data is empty. So silkscreen.py traces the kit's `logo.webp` itself each
time it runs:
- Marching squares on the white artwork, to a fraction of a pixel, simplified to 0.8 px. That is about 0.01 mm on the controller.
- The shapes are split into icon and wordmark at the widest gap. The script stops with an error unless it finds 7 letters.
- The traced outline differs from the picture by 1.6 % of the artwork's pixels, all of them along the edges.

Each shape is a `poly` item whose holes (the gear's inside, the counters of B and O) are further rings.

### 1.5 L1: FRONT, and the CAD's "L1"

- **FRONT** is a decal: the CAD has no pocket for it.
  - Placement: Lee's drawing (4.58 px/mm) puts it 5.1 mm in from the −z edge. It sits on the line of the "L1" code, top at x 768.69 (5.8 mm from the front edge), letters up toward +x, reading +z, spanning z 1278.58–1307.25.
  - Letter shapes: built as filled strokes in the weight and height of the CAD's own engraved code. Capitals are 6.32 high, upright strokes 0.85, cross strokes 0.75, all measured on the CAD's pocket floor. Shapes and spacing follow the drawing, scaled to that height.
  - Clearances: nothing covers it. L7's notch starts at z 1321.5, and the left wheel ends at x 752.6.
- **The CAD's "L1"** reads upside down against the drawing; the code's pocket is at x 763.08–769.43, z 1390.33–1397.74. To make it match, add to `materials.json`:

      "move_engraving": {"NAUO1": {"by": [-0.74, 0, -0.95], "turn": 180}}

  This turns the code about its own middle and moves it onto the drawing's spot (x 762.34–768.69, z 1389.38–1396.79), on the same line as FRONT.
  L1's node has no rotation, so the move is the same in assembly and mesh frames. The wood rule must carry `"engraving": "ink"` (`^L[1-7]$`, reuse report 1.1).
  If `"by": [0, 0, 0]` is preferred, FRONT has to move 0.74 mm toward +x to stay on the line: in silkscreen.py, `code_top = 769.434`.
- The two then match in size and stroke weight. The font cannot match exactly: the CAD's "1" has a curved flag, and its font is not available here.
- Side by side with Lee's drawing at the same scale, FRONT and L1 land where the drawing has them (within about 0.3 mm). As cad_study.md 2.5
  notes, the drawing's outline cannot show whether it is the top or the underside.

## 2. js/core.js: what addDecal can draw now

Added to `addDecal`, in both kits' `js/core.js` (identical):
- `{poly: [[x, y], ...] or [[[x, y], ...], ...]}`: a filled outline, or several rings filled even-odd, so a ring inside another is a hole.
  With `line` it draws the rings as outlines, and `open: true` leaves them unclosed (a bracket).
- `{arc: [x, y, r, from, to]}`: degrees, clockwise from the picture's right, as canvas measures them. With `line` it draws the arc;
  without `line` it fills the piece of the circle that the chord cuts off (the capacitor band).
- `text` takes an optional `width`: the text is squeezed to at most that length (canvas `fillText`'s maxWidth). Without `width` the old call runs unchanged.

Existing items run through the same code as before. The MRA's decals.json uses none of the new keys (checked), so the MRA renders as
it did. Checked in the browser: the MRA player, already being served on port 8791, loads with the new core.js, shows the module's print
at Step 1, and logs no console errors. The MRA's `_runthrough()` was not re-run: the change touches only how decals are drawn when the page loads.

## 3. Checks

- `silkscreen.py` runs and decals.json reads back. All four keys are top-level instances of rcc.glb. Every item lies inside its
  picture, and every decal faces away from its face (+Y, or −Y for the module's underside) at face + 0.02 mm.
- **Photo overlays**: each decal was warped onto Lee's photo with the mappings above and drawn in red. On the adapter every
  label, outline, pad, the icon and the capacitor print land on the photo's marks. On the controller the logo, NANO BOARD /
  CONTROLLER, L–JS, NRF24L01, C1 and USB land on theirs. The capacitor's top looks shifted on the controller photo only because
  of perspective: the can is 7.7 mm tall.
- **3D**: a scratch page in the scratchpad loaded the real `js/core.js` with a small GLB of the boards, headers, capacitors and L1
  cut from rcc.glb, each part carrying its decals (13 decals). From above, the adapter and the controller read exactly as in the
  photos, and L1 reads as in Lee's drawing. In an oblique view the print follows the faces and hides under the parts standing on them.

## 4. Points for Lee or the next step

1. The RCC's `materials.json` needs `"decals": "decals.json"`, the `move_engraving` above, and the boards coloured white (reuse report 2.1 and 2.4 #10).
2. Is the RCC kit's I/O module the board in the MRA photos? Its print is carried over on that assumption (reuse report 2.4 #9).
3. The adapter's solder pads are an extra. They make the board look like the photo, but they are metal, not print. Drop them if unwanted: one line in silkscreen.py (`long_items += pads(...)` and the short-arm `pads`).
4. Board print colour: #000000 (breadboard legends) is used; #1e1616 (ink) would match the engraving. This is a one-line change (`PRINT`).
5. FRONT's letters copy the CAD code's height and stroke but not its exact font.
6. Texture memory: the RCC's decals come to about 6.6 MP of canvas, half of it the module's, against the MRA's 3.1. They are drawn once at load and add no per-frame work.
