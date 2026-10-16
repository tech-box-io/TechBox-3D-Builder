# MRA: the pins every wire plugs into (CAD + build videos)

Written 13 Oct 2026. Data: `cad_pins.json` (same folder). Stills and drawings: `stills/pins/` (index at the end).
All coordinates are mm in the assembly space of `mra.glb` (Y up, as assembled). Ids are the CAD's top-level instances (`NAUOn`).
"Measured" = read from the CAD geometry. "Seen" = read from a still of a build video (`MRA_Videos/Controller.mov`,
1080 x 1920, 266 s, unless another video is named). Anything that is a guess says so.

STATUS: complete (sections 1 to 5).

## Short answers

- **The CAD already has every wire on the pin Lee names. No wire has to move to another pin.**
  - left joystick NAUO80: GND -> A2 G, +5V -> A2 V, VRx -> A2 S, VRy -> A3 S;
  - right joystick NAUO81: GND -> A0 G, +5V -> A0 V, VRx -> A0 S, VRy -> A1 S;
  - base servo NAUO45 -> row 5 (plug NAUO83). The other three servo plugs sit on rows 6, 9 and 10.
- The videos show the same wiring on the real kit: the printed legends, the jumper colours, the flag "5" on the base
  servo's lead and the flag "6" on the left side servo's lead all fit.
- NAUO80 (z about 119) is the LEFT joystick and NAUO81 (z about 164) the RIGHT one as the student sees the finished
  controller (joysticks nearest the student, arm furthest away; +z is the student's right). `guide.py` already has
  them that way round.
- Shield pins point straight up, direction [0, 1, 0]; every pin top is at y = 113.80.
  Joystick pins point towards the shield, direction [1, 0, 0]; every pin tip is at x = 25.46, y = 124.23.
- **One thing in the project is the wrong way round.** `materials.json` (`_notes.unconfirmed`) says the CAD header suffix
  `_B` was read as the G row and `_N` as the S row. The real board shows the opposite: `_N` is G, `_R` is V, `_B` is S
  (section 1). So on every servo plug the brown wire belongs on the conductor at x = 49.98 (the board-edge side) and the
  orange wire on the one at x = 55.06 (the Nano side). `cad_wire_paths.md` reaches the same conclusion from this pin map.
- **Joystick cable colours** (also listed as unconfirmed in `materials.json`): on the real kit the LEFT joystick's
  ribbon is yellow (GND), green (+5V), blue (VRx), purple (VRy); the RIGHT joystick's is black (GND), brown (+5V),
  red (VRx), orange (VRy). The model paints both ribbons yellow-green-blue-purple at present.
- In the CAD every wire arcs through open air above the controller. The only wood the leads pass through is in the
  turret: the L-shaped slot in R4 (base servo lead and the claw's extension lead) and the hook-shaped slots in the ears
  of R5 and R6 (the two side servos' leads). Coordinates in section 5.

## 1. The shield's pin map (NAUO82)

### What the board is

The real board (seen lying flat at 0:32, `shield_top_t00m32s_x4.jpg`) is the common blue "Nano I/O expansion shield"
with yellow pin headers, an Arduino Nano in two 15-way sockets, a barrel power jack, a reset button and a 47 uF can
capacitor. The CAD model NAUO82 is the same board, the same way up and not mirrored: header blocks, jack, capacitor,
reset button and Nano are in the same places as in the still.

Measured in the CAD:

| Feature | Where (mm) |
|---|---|
| Board (mesh `Shield_Arduino NANO`) | x 43.36 to 96.70, z 115.96 to 173.16, top face y = 106.43, underside y = 104.78 |
| Nano (mesh `nano_...`) | x 60.46 to 78.46, z 129.86 to 174.86. Its USB socket is at the +z end (x 64.0 to 74.9, y 119.0 to 122.8, z 165.5 to 174.9) and overhangs the board edge by 1.7 mm |
| Power jack (`PJ-002AH`) | x 81.1 to 90.1, y 106.4 to 117.4, z 160.6 to 175.0; opening faces +z |
| Reset button | x 92.2 to 95.2, z 157.0 to 162.2 |
| 47 uF capacitor | x 82.6 to 90.6, z 148.7 to 155.3, top y = 112.25 |
| Nano sockets (`Samtec-SSW-115`) | x = 61.78 and x = 77.08, z 132.2 to 170.8, top y = 114.94 |

The USB socket and the power jack are both at the +z end, the student's right. The digital rows are along the edge
nearest the joysticks (-x), the analogue rows along the edge nearest the turret (+x). The video shows the board fitted the
same way round (`final_controller_overview_t04m24s.jpg`; `Claw_mov_t07m05s_finished_wiring.jpg`).

### The pin headers

NAUO82 holds 37 meshes; 24 of them are `Samtec-TLW-...` pin headers. Each is a plastic strip (y 106.42 to 107.97) with
square pins through it. Measured: pitch 2.54; pin top y = 113.80 (5.83 mm of pin above the plastic); pins point
+Y = [0, 1, 0]; solder tails reach y = 103.80 under the board.

| Header meshes (child nodes of NAUO82) | CAD mesh name | Pins | x | z of the pins | What it is |
|---|---|---|---|---|---|
| NAUO143, 142, 141, 140 | TLW-104-01-F-S_N | 4 x 4 | 50.085 | 124.37 126.91 129.45 131.99, 136.92 139.46 142.00 144.54, 149.47 152.01 154.55 157.09, 162.02 164.56 167.10 169.64 | digital side, **G** column (at the board edge, nearest the joysticks) |
| NAUO147, 146, 145, 144 | TLW-104-01-F-S_R | 4 x 4 | 52.574 | same | digital side, **V** column |
| NAUO151, 150, 149, 148 | TLW-104-01-F-S_B | 4 x 4 | 55.064 | same | digital side, **S** column (nearest the Nano) |
| NAUO156 | TLW-108-01-F-S_N | 8 | 83.126 | 123.70 126.24 128.78 131.32 133.86 136.40 138.94 141.48 | analogue side, **G** column (nearest the Nano) |
| NAUO155 | TLW-108-01-F-S_R | 8 | 85.615 | same | analogue side, **V** column |
| NAUO154 | TLW-108-01-F-S_B | 8 | 88.105 | same | analogue side, **S** column (at the board edge, nearest the turret) |
| NAUO124, NAUO125 | TLW-103-01-F-S | 3 + 3 | 76.33, 73.83 | 121.63 124.17 126.71 | 2 x 3 block at the end away from USB. Not used by the kit. Names not read. |
| NAUO153 | TLW-104-01-F-S_W | 4 | 69.52 | 118.79 121.33 123.87 126.41 | 4-pin header. Not used. Names not read (guess: an I2C or serial breakout). |
| NAUO152 | TLW-104-01-F-S_W | 4 | 64.56 | 118.83 121.37 123.91 126.45 | 4-pin header. Not used. Names not read. |

The CAD modeller's suffixes mean the same on both sides of the board: `_N` = G, `_R` = V, `_B` = S, `_W` = the two
unused 4-pin headers. (Guess at where the letters come from: such shields are often sold with black, red and blue
headers for G, V and S; N = noir / negro.) The G V S order is NOT mirrored across the board: going from the joystick
edge (-x) to the turret edge (+x) the columns are G V S, then the Nano, then G V S again.

For whoever draws the board: the sixteen digital rows are four blocks of four with a gap between blocks (block pitch
12.55 mm, not 10.16). The real board has the same four blocks.

### The rows a student sees, with their printed names

Seen on the real board:

- Digital side, from the USB end to the far end: `AREF`, `GND`, `13`, `12` | `11`, `10`, `9`, `8` | `7`, `6`, `5`, `4` |
  `3`, `2`, `TX 1`, `RX 0`. Read at 0:32 (first three blocks) and at 4:24 (last block and "4", "5" of the next), stills
  `shield_top_t00m32s_x4.jpg`, `servo5_plug_rows_t04m24s_x12_ticks.jpg`, and again in Arm.mov at 5:56
  (`Arm_mov_t05m56s_shield_top_view_x4.jpg`).
- Beside each digital block three small letters name the columns: `S` nearest the Nano, then `V`, then `G` at the board
  edge. Seen between the first two blocks at 4:24, at the USB-end corner at 0:40, and at the USB end in Arm.mov 5:56.
- Analogue side: `A0 A1 A2 A3 A4 A5 A6 A7` printed along the outside of the header, A0 at the capacitor / power-jack
  end (the USB end), A7 at the far corner. Beside the capacitor the letters `G`, `V`, `S` run from the Nano outwards:
  G nearest the Nano, S at the board edge (0:40, `shield_A0-A7_GVS_legend_t00m40s_x6.jpg`).
- A real servo plug confirms the digital columns: at 4:24 the base servo's plug has its orange wire on the Nano side and
  its brown wire at the board edge, and the build notes say brown to G, orange to S.

Put onto the CAD. Pin tops; y = 113.80 for all; G, V, S differ only in x. Drawing: `cad_pin_map_student_view.png`.

Digital rows: G at x = 50.085, V at x = 52.574, S at x = 55.064.

| Row (printed) | JSON key | z | Used by |
|---|---|---|---|
| RX 0 | D0 | 124.37 | |
| TX 1 | D1 | 126.91 | |
| 2 | D2 | 129.45 | |
| 3 | D3 | 131.99 | |
| 4 | D4 | 136.92 | |
| **5** | D5 | **139.46** | base servo NAUO45 (plug NAUO83) |
| **6** | D6 | **142.00** | side servo NAUO58, student's left (plug NAUO84) |
| 7 | D7 | 144.54 | |
| 8 | D8 | 149.47 | |
| **9** | D9 | **152.01** | side servo NAUO66, student's right (plug NAUO86) |
| **10** | D10 | **154.55** | claw servo NAUO72 through the extension lead (plug NAUO85) |
| 11 | D11 | 157.09 | |
| 12 | D12 | 162.02 | |
| 13 | D13 | 164.56 | |
| GND | GND_row | 167.10 | |
| AREF | AREF_row | 169.64 | |

Analogue rows: G at x = 83.126, V at x = 85.615, S at x = 88.105.

| Row | z | Used by |
|---|---|---|
| **A0** | **141.48** | right joystick: G = GND, V = +5V, S = VRx |
| **A1** | **138.94** | right joystick: S = VRy |
| **A2** | **136.40** | left joystick: G = GND, V = +5V, S = VRx |
| **A3** | **133.86** | left joystick: S = VRy |
| A4 | 131.32 | |
| A5 | 128.78 | |
| A6 | 126.24 | |
| A7 | 123.70 | |

How sure:

- A0 to A7 and their G / V / S columns: high. The legend is readable in two videos, Lee's wiring lands exactly on the
  eight CAD end caps with this naming, and the jumper colours fit (section 2).
- Digital 0 to 13: high. Legends for 0 to 5 and 8 to 13 were read directly; "7 6" was read at 0:32. The four CAD servo plugs
  sit on rows 5, 6, 9 and 10, which only makes sense with this numbering.
- Digital G / V / S columns: high (legend read in two videos, plus the real plug's wire colours).
- The rows printed `GND` and `AREF`: medium-high for the legends. What their three pins carry was not traced; the kit
  does not use them.
- The 2 x 3 block and the two 4-pin headers: names not read; not used.

## 2. Which pins the CAD's wires sit on

### The eight joystick wires

Each bundle (NAUO111 = `Part6`, NAUO112 = `Part7`) is four separate tubes 1.25 mm across. Each tube was followed from end
to end in the CAD and its ends matched to the end caps (1.75 x 1.75 x 8.0 mm boxes). "Solid" is the tube's index in
`cad_wires.json`, which holds the centre lines.

| Joystick | Joystick pin | Cap on the joystick | Bundle / solid | Wire end at the joystick | Wire end at the shield | Cap on the shield | Shield pin (CAD) | Pin top | Lee says | Colour on the real kit |
|---|---|---|---|---|---|---|---|---|---|---|
| NAUO80 left | GND | NAUO104 | NAUO112 / 3 | 27.46, 124.23, 123.34 | 83.13, 115.97, 136.48 | NAUO99 | A2 G | 83.126, 113.80, 136.40 | A2 G: agrees | yellow |
| NAUO80 left | +5V | NAUO105 | NAUO112 / 2 | 27.46, 124.23, 120.84 | 85.61, 115.97, 136.48 | NAUO100 | A2 V | 85.615, 113.80, 136.40 | A2 V: agrees | green |
| NAUO80 left | VRx | NAUO106 | NAUO112 / 1 | 27.46, 124.23, 118.34 | 88.11, 115.97, 136.48 | NAUO101 | A2 S | 88.105, 113.80, 136.40 | A2 S: agrees | blue |
| NAUO80 left | VRy | NAUO107 | NAUO112 / 0 | 27.46, 124.23, 115.84 | 88.11, 115.97, 133.94 | NAUO102 | A3 S | 88.105, 113.80, 133.86 | A3 S: agrees | purple |
| NAUO81 right | GND | NAUO103 | NAUO111 / 3 | 27.46, 124.32, 168.34 | 83.13, 115.97, 141.48 | NAUO97 | A0 G | 83.126, 113.80, 141.48 | A0 G: agrees | black |
| NAUO81 right | +5V | NAUO108 | NAUO111 / 2 | 27.46, 124.26, 165.84 | 85.61, 115.97, 141.48 | NAUO96 | A0 V | 85.615, 113.80, 141.48 | A0 V: agrees | brown |
| NAUO81 right | VRx | NAUO109 | NAUO111 / 1 | 27.46, 124.23, 163.34 | 88.11, 115.97, 141.48 | NAUO95 | A0 S | 88.105, 113.80, 141.48 | A0 S: agrees | red |
| NAUO81 right | VRy | NAUO110 | NAUO111 / 0 | 27.46, 124.23, 160.84 | 88.11, 115.97, 138.94 | NAUO98 | A1 S | 88.105, 113.80, 138.94 | A1 S: agrees | orange |

**The CAD agrees with Lee on all eight wires**, so there are no "should go to" pins that differ from where the wires
already end. If the routes are redrawn for other reasons, the ends to keep are the "Pin top" column (shield) and the pin
tips in section 3 (joystick).

Small things in the CAD that do not change the answer:
- The caps on rows A2 and A3 (NAUO99 to 102) are drawn 0.08 mm off their pins in z (caps at 136.48 and 133.94, pins at
  136.40 and 133.86): they were placed 5.00 mm from the A0 / A1 caps instead of 5.08.
- The shield-end caps are boxes from y = 107.97 (sitting on the yellow plastic) to y = 115.97; the wire starts at the top
  face and leaves straight up. The joystick-end caps run x = 19.46 to 27.46; the wire starts at x = 27.46 and leaves
  along +x.
- The SW pin of each joystick has nothing on it, in the CAD and on the real kit.

What the videos show. The eight jumpers have single black housings and fill the capacitor end of the analogue header;
A4 to A7 are bare (`shield_A0-A7_GVS_legend_t00m40s_x6.jpg`, `shield_installed_jumpers_t03m48s_x3.jpg`,
`Arm_mov_t05m56s_shield_top_view_x4.jpg`). The outside (S) row carries four housings side by side whose wires are, from
A0 to A3: red, orange, blue, purple. Behind red, on A0, are brown and black; behind blue, on A2, are green and yellow.
With the colours at the joystick end (section 3) that is exactly Lee's wiring. One limit: the V and G pins behind the
front row are partly hidden in every still, so that black is on G and brown on V (and yellow on G, green on V) is taken
from the order of the wires in the ribbon, not seen pin by pin.

### Which joystick is "left"

NAUO80 (z 105 to 132) is the left joystick, NAUO81 (z 150 to 177) the right one. How this was decided:

1. The student uses the controller from the joystick end. The engraving on the top plate B8 reads the right way up from
   there, in the video (`final_controller_overview_t04m24s.jpg`) and in the CAD (`cad_B8_top_student_view.png`: "B8"
   is upright when +x is up the page and +z is to the right). From that seat the arm is ahead (+x) and up is +y, so
   the student's right is +z.
2. On the real B8 the left stick is engraved "Shoulder" (up / down) and "Base" (left / right), the right stick "Elbow"
   and "Claw". (The CAD's B8 carries only the code "B8", not these words.)
3. In the video the joystick with the yellow-green-blue-purple ribbon is fitted between B5 and B6 first and ends up under
   the Shoulder / Base side, the student's left; its ribbon goes to A2 / A3. The joystick with the
   black-brown-red-orange ribbon ends up under Elbow / Claw, the student's right; its ribbon goes to A0 / A1.
4. In the CAD the wires on A2 / A3 (NAUO112) go to NAUO80 and the wires on A0 / A1 (NAUO111) go to NAUO81.

All of this agrees with Lee's wording and with `guide.py` (`JOY_LEFT = NAUO80`; "the left joystick (the joystick connected
to A3)").

### The servo plugs

Each plug is a 3-way JR housing (`JR-3`, 7.9 x 2.75 x 14.0 mm, y 107.97 to 121.97) with three contacts at
x = 49.98, 52.52 and 55.06, lined up with the G, V and S columns. A plug sits across one row.

| Plug | Row (printed) | Plug box lo / hi | G pin top | V pin top | S pin top | Lead | Goes to |
|---|---|---|---|---|---|---|---|
| NAUO83 | **5** | 48.57, 107.97, 137.98 / 56.47, 121.97, 140.73 | 50.085, 113.80, 139.46 | 52.574, 113.80, 139.46 | 55.064, 113.80, 139.46 | NAUO87 (`Part1`), joined to the top of the plug's 40 mm cable stub at y = 160.96 | base servo NAUO45 in the turret |
| NAUO84 | **6** | 48.57, 107.97, 140.73 / 56.47, 121.97, 143.48 | 50.085, 113.80, 142.00 | 52.574, 113.80, 142.00 | 55.064, 113.80, 142.00 | NAUO88 (`Part2`) | side servo NAUO58, low z = student's left |
| NAUO86 | **9** | 48.57, 107.97, 150.53 / 56.47, 121.97, 153.28 | 50.085, 113.80, 152.01 | 52.574, 113.80, 152.01 | 55.064, 113.80, 152.01 | NAUO89 (`Part3`) | side servo NAUO66, high z = student's right |
| NAUO85 | **10** | 48.57, 107.97, 153.28 / 56.47, 121.97, 156.03 | 50.085, 113.80, 154.55 | 52.574, 113.80, 154.55 | 55.064, 113.80, 154.55 | NAUO93 (`Part4`), which starts inside the plug (this plug has no cable stub) | the extension joint just inside the turret (plug NAUO92, bridge NAUO91, plug NAUO90: x 139 to 168, y 132 to 135, z 141 to 149), then NAUO94 (`Part5`) to the claw servo NAUO72 |

The base servo is on row 5 in the CAD, as Lee says. The plugs are drawn 0.1 mm off the row centres in z (NAUO83 is
centred on z = 139.36, the row on 139.46); that is drawing tolerance, not a different row.

Which conductor is on G, V and S. The CAD has no colours, so this comes from position: the conductor that meets the
contact at x = 49.98 is on G and must be brown, the middle one is red, the one at x = 55.06 is on S and must be orange.
Ends below are from `cad_wires.json` (solid index in brackets); the shield end is where the lead meets the top of the
plug's cable stub, or for NAUO93 where it starts inside the plug.

| Lead | G = brown: shield end -> far end | V = red | S = orange |
|---|---|---|---|
| NAUO87 (row 5, base) | [0] 51.50, 160.96, 139.39 -> 162.62, 119.11, 149.76 | [1] 52.52, 160.96, 139.36 -> 163.64, 119.11, 149.76 | [2] 53.54, 160.96, 139.33 -> 164.66, 119.11, 149.76 |
| NAUO88 (row 6) | [0] 51.50, 160.96, 142.11 -> 184.58, 163.30, 92.85 | [1] 52.52, 160.96, 142.11 -> 184.58, 162.28, 92.85 | [2] 53.54, 160.96, 142.10 -> 184.58, 161.26, 92.85 |
| NAUO89 (row 9) | [0] 51.50, 160.96, 151.89 -> 184.58, 161.26, 188.35 | [1] 52.52, 160.96, 151.91 -> 184.58, 162.28, 188.35 | [2] 53.54, 160.96, 151.93 -> 184.58, 163.30, 188.35 |
| NAUO93 (row 10) | [0] 49.95, 116.29, 154.71 -> 142.02, 133.62, 142.12 | [2] 52.57, 115.89, 154.65 -> 141.99, 133.62, 144.66 | [1] 55.11, 115.54, 154.62 -> 141.56, 133.62, 147.20 |

Inside each cable stub (NAUO83, 84, 86) the three conductors fan in from the contacts (x = 49.98, 52.52, 55.06 at
y = 120.97) to a flat ribbon 3 mm wide (x = 51.0 to 54.0) at y = 160.96. `cad_wire_paths.md` follows each chain to its
servo and deals with the colour order at the servo end.

## 3. The joystick header

Mesh `5x_Ang_Conn_1` in each joystick: a 5-way right-angle header on the +x edge of the joystick board, 2.5 mm pitch
(the CAD part is drawn at 2.5, not 2.54). Each pin rises through a black plastic strip (x 16.91 to 19.41, y 120.53 to
123.03) and bends to run along +x at y = 124.23 (0.6 mm square). Past the strip the bare pin runs from x = 19.41 to its
tip at x = 25.46. Pins point [1, 0, 0], towards the shield.

The CAD board carries the legend as geometry (render: `cad_joystick_silk_NAUO80.png`) and the real module (marked
HW-504) has the same legend in the same order (`joystick_rainbow_legend_t00m32s_x5.jpg`,
`joystick_blackbrownredorange_legend_t00m32s_x5.jpg`): GND, +5V, VRx, VRy, SW. The video also shows the jumpers on the
first four pins and SW bare, on both joysticks.

| Pin (printed) | NAUO80 left: tip (x, y, z) | Cap, wire | Real colour | NAUO81 right: tip (x, y, z) | Cap, wire | Real colour |
|---|---|---|---|---|---|---|
| GND | 25.46, 124.23, 123.34 | NAUO104, NAUO112 / 3 | yellow | 25.46, 124.23, 168.34 | NAUO103, NAUO111 / 3 | black |
| +5V | 25.46, 124.23, 120.84 | NAUO105, NAUO112 / 2 | green | 25.46, 124.23, 165.84 | NAUO108, NAUO111 / 2 | brown |
| VRx | 25.46, 124.23, 118.34 | NAUO106, NAUO112 / 1 | blue | 25.46, 124.23, 163.34 | NAUO109, NAUO111 / 1 | red |
| VRy | 25.46, 124.23, 115.84 | NAUO107, NAUO112 / 0 | purple | 25.46, 124.23, 160.84 | NAUO110, NAUO111 / 0 | orange |
| SW | 25.46, 124.23, 113.34 | none | - | 25.46, 124.23, 158.34 | none | - |

On both joysticks GND is the pin at the highest z (the student's right-hand end of the header) and SW the lowest.
Each cap is a 1.75 x 1.75 x 8.0 mm box on its pin: x 19.46 to 27.46, y 123.36 to 125.11, centred on the pin's z. The
wire leaves the cap at x = 27.46 heading +x.

## 4. The servo rows

- CAD: four plugs, on rows 5, 6, 9 and 10 (coordinates in section 2 and in the JSON under `servo_leads`).
- Row 5, base servo. Its lead carries a white paper flag with a hand-written "5" (Controller.mov from 0:00). At 4:14 to
  4:24 it is pushed onto the second digital block from the far end ("4 5 6 7"). Which of the four rows was worked out
  twice, because a plug hides its own row:
  - Controller.mov 4:24 (`servo5_plug_rows_t04m24s_x12_ticks.jpg`): row 4 is bare with all three pins showing; the three
    wires enter the top of the plug one row further on; half of the row after that and all of row 7 show beyond it.
  - Arm.mov 5:56, nearly straight down (`Arm_mov_t05m56s_shield_top_view_x4.jpg`): scaled from the board's width, the
    foot of the plug spans about 33 to 35.5 mm from the USB-end edge of the board. A plug on row 5 would span 32.3 to
    35.1 mm, on row 4 34.9 to 37.6, on row 6 29.8 to 32.5. Rows 7 and 6 show their pins on one side of the plug, row 4's
    plastic on the other.
  Both give row 5. Confidence: high, short of certain, since no still shows the plug's foot directly.
- Row 6. In Arm.mov at 5:28 a servo is being fitted into the frame engraved "R8" on the side of the turret that has B5
  and R5 on it, which is the low-z side (the student's left); its lead carries a black flag with a white underlined "6"
  (`Arm_mov_t05m28s_flag6_servo_on_R8_frame.jpg`; the same flag at 5:56,
  `Arm_mov_t05m56s_overview_flag6_servo5.jpg`). In the CAD the low-z side servo is NAUO58, mounted on NAUO17 (CAD name
  `ARA_R8`), and its lead is on row 6. Agrees.
- Rows 9 and 10. In the finished kit (Claw.mov 7:00 and 7:05, `Claw_mov_t07m05s_finished_wiring.jpg`) four plugs stand
  in the middle two digital blocks, as rows 5, 6, 9 and 10 would. The flags for 9 and 10 were not read (a blue flag
  hangs on the twisted extension lead from the claw; its number is not legible in the frames looked at). By elimination
  and by the CAD: row 9 = the side servo on the student's right (NAUO66), row 10 = the claw (NAUO72).
- Not decided here: which of the two side servos is the "shoulder" and which the "elbow". B8's engraving says only
  which joystick drives which.

## 5. Routing features on the controller side

### What the CAD wires do

Checked by following every wire's centre line and testing it against the seventeen wood parts NAUO1 to NAUO17: no wire
passes through wood, and on the controller side no wire uses a slot or hole at all. They rise from their pins and arc
through open air above the shield:

- Joystick wires. They leave the caps at x = 27.46, y = 124.2 heading +x, run level to about x = 46, climb between
  x = 55 and x = 66, peak at y = 154 to 157 near x = 72 to 74, cross the lines of the B6 walls at about x = 73 to 79,
  y = 153 to 157 (the wall is only y = 102.1 high there, and the Nano's top is at y = 122.8), then drop straight down onto
  the analogue pins.
- Servo leads. From the top of each plug's stub (y = 160.96) they climb to y = 178 to 183 near x = 76 and slope down
  towards the turret. NAUO93 (row 10) peaks lower, at y = 168.

### The gaps the joystick wires leave through (B5, B6, B7, B8 = NAUO4, 5, 6, 7, 8)

Each joystick sits in a bay between two walls, under the top plate B8. Its header points out of the bay's open front.

| Opening | Bounded by | Plane and size | Where the CAD wires cross it |
|---|---|---|---|
| Left bay mouth | B5 (NAUO4, inner face z = 108.05), B6 left (NAUO5, inner face z = 128.63), B8 above (NAUO8, underside y = 134.23), base plate below (top of B2, y = 93.5) | at x = 32.5 (front edge of B8 and of the tall part of the walls): 20.6 mm wide, 40.7 mm tall | NAUO112: y = 124.2 to 124.3, z = 116.4, 118.6, 120.7, 122.8 |
| Right bay mouth | B6 right (NAUO6, inner face z = 153.00), B7 (NAUO7, inner face z = 173.63), B8 above, base plate below | at x = 32.5: 20.6 mm wide, 40.7 mm tall | NAUO111: y = 124.2 to 124.5, z = 161.5, 163.5, 165.5, 167.5 |

So the wires come out 10 mm below the underside of B8. In front of the mouths the walls are low: B5 drops to y = 109.4
(as far as x = 83.3), both B6 walls drop to y = 110.2 falling to 109.4 (as far as x = 45.2), and B7 stops at x = 32.5.
From x = 32.5 on, a wire at y = 124 is above all the wood.

Other features of these parts, none of which a wire passes through:

- Shield slots in the two B6 walls (NAUO5 at z 128.63 to 131.63, NAUO6 at z 150.00 to 153.00; outline
  `cad_outline_NAUO5.png`): a notch at x 43.04 to 45.20, y 104.78 to 106.31 on the joystick side and one at x 94.73 to
  97.02, y 104.78 to 106.31 on the turret side. The board's two long edges (x = 43.36 and x = 96.70) sit in them. Between
  the notches the wall's top is at y = 102.11, below the board; beyond the turret-side notch each wall has a tower from
  x = 94.86 to 107.6 rising to y = 118.5.
- B4 (NAUO3, x 68.53 to 71.53; `cad_outline_NAUO3.png`): top at y = 102.11 under the board, with a post at each end,
  z 108.05 to 115.67 up to y = 109.41 and z 173.45 to 179.80 up to y = 107.89. The board (z 115.96 to 173.16) lies
  between the posts.
- Gap beside the board on the student's left: between B5's inner face (z = 108.05) and the board's edge (z = 115.96),
  7.9 mm wide, x 43.4 to 96.7, crossed by B4's post at x 68.5 to 71.5. The CAD wires do not use it; the real ribbon does
  (below).
- B3 (NAUO9) and the joystick-board slots in the walls (y 118.9 to 120.6 at x -14.5 to -9.4 and x 14.7 to 19.8) are
  behind the headers and play no part in the wiring.

### The slots in the turret that the servo leads pass through

| Slot | Part | Shape and coordinates | Which lead, and where its centre line crosses the part's mid-plane (CAD) |
|---|---|---|---|
| L-shaped slot | R4 = NAUO13 (x 131.94 to 134.94), the turret wall facing the controller. Outline: `cad_outline_NAUO13.png` | Open at the top edge (y = 146.59). Entry leg 2.12 mm wide, z 140.60 to 142.72, running down to a pocket z 140.60 to 148.72, y 127.25 to 135.75 (8.1 x 8.5 mm). Corners (y, z): 146.59, 140.60 -> 127.25, 140.60 -> 127.25, 148.72 -> 135.75, 148.72 -> 135.75, 142.72 -> 146.59, 142.72; corner radius 0.5 | Base servo lead NAUO87 (row 5): three conductors at x = 133.44, y 129.0 to 131.5, z 143.2 to 143.7. Claw extension lead NAUO93 (row 10): at x = 133.44, y 133.0 to 133.7, z 142.2 to 146.6. Both sit in the pocket. |
| Hook slot | R5 = NAUO15 (z 109.00 to 112.00), in the ear that sticks out towards the controller. Outline: `cad_outline_NAUO15.png` | Open at the ear's -x edge (x = 117.58). Entry channel 2.25 mm wide, y 166.28 to 168.53, running +x to x = 125.12, then a pocket x 121.94 to 125.12 (3.18 mm wide) going down to y = 158.28. Corners (x, y): 117.58, 166.28 -> 121.94, 166.28 -> 121.94, 158.28 -> 125.12, 158.28 -> 125.12, 168.53 -> 117.58, 168.53 | Row 6 lead NAUO88, to side servo NAUO58: at z = 110.5, x 123.3 to 123.7, y 162.4 to 164.4, heading -z out of the turret. |
| Hook slot | R6 = NAUO14 (z 169.20 to 172.20). Outline: `cad_outline_NAUO14.png` | Same shape, same x and y as the one in R5 | Row 9 lead NAUO89, to side servo NAUO66: at z = 170.7, x 122.9 to 124.1, y 162.3 to 164.6, heading +z. |

Between the shield and these slots the CAD leads cross the turret end of the B6 walls (x = 107.6) at: NAUO87 y = 159,
z = 138; NAUO88 y = 169, z = 128; NAUO89 y = 160, z = 151; NAUO93 y = 140, z = 146. All well above the walls' towers
(y = 118.5).

A servo lead is three 1.0 mm conductors side by side, about 3.1 x 1.0 mm. It goes into the 2.1 mm entry of R4's slot and
the 2.25 mm entry of the hooks edge-on, then lies in the wider pocket.

### What the real leads do (seen; positions are descriptions, not measurements)

- Left joystick ribbon (yellow-green-blue-purple): out of the left bay mouth, up in front of B8, round the student's-left
  end of the board (over the gap between B5 and the board) and down onto A2 / A3 from the turret side. It stands in a
  loop well above the board (`final_servo5_plugged_t04m24s_x3.jpg`).
- Right joystick ribbon (black-brown-red-orange): out of the right bay mouth, up over digital rows 8 to 13 and
  diagonally over the Nano, down onto A0 / A1.
- Base servo lead: out of the turret through R4's L-shaped slot (the build notes' "move the servo wire into the L-shaped
  slot in R4"), down onto the base plate between turret and shield, round the USB end of the board, and onto row 5
  from the joystick side, flag next to the plug (`final_controller_overview_t04m24s.jpg`,
  `Arm_mov_t05m56s_overview_flag6_servo5.jpg`).
- Finished kit (`Claw_mov_t07m05s_finished_wiring.jpg`, `Claw_mov_t07m00s_leads_through_R4_R5_R6.jpg`): the left side
  servo's lead runs through the hook in R5's ear and the right side servo's through the hook in R6's ear, each then down
  to the digital rows; the extension joint (plug and socket) hangs just inside R4 and the twisted brown-red-yellow
  extension lead comes out through the L-shaped slot beside the base servo's lead.

The real ribbons are about twice as long as the CAD's tubes and flop where they like, so the CAD arcs are tidier than
the kit. The ends and the three turret slots are the fixed points.

## What this changes in the project

1. `materials.json`: the servo conductor order. Brown is on the G column, which is the column at x = 50.09 (`_N`), not
   x = 55.06. The `_notes.unconfirmed` line about `_B` = G can be replaced by: `_N` = G, `_R` = V, `_B` = S, confirmed
   from the legends on the real board and a real plug. See `cad_wire_paths.md` for which `across` rules to flip.
2. `materials.json`: the joystick ribbons. Left (NAUO112): GND yellow, +5V green, VRx blue, VRy purple. Right (NAUO111):
   GND black, +5V brown, VRx red, VRy orange. A black wire colour is not in the palette yet.
3. Nothing to change in `guide.py` for which joystick is left, which row the base servo uses, or which analogue rows the
   joysticks use.
4. Header strips: all yellow on the real board, as already decided.

## Stills and drawings (`stills/pins/`)

| File | Shows |
|---|---|
| `shield_top_t00m32s_x4.jpg` | Real board from above: AREF, GND, 13 ... 4 legends, the four digital blocks, USB and jack at one end |
| `shield_analog_side_t00m40s_x3.jpg`, `shield_A0-A7_GVS_legend_t00m40s_x6.jpg` | A0 ... A7 legend, the G V S letters beside the capacitor, the eight jumpers on A0 to A3 |
| `joystick_rainbow_legend_t00m32s_x5.jpg`, `joystick_blackbrownredorange_legend_t00m32s_x5.jpg` | Joystick legends GND +5V VRx VRy SW and which colour is on which pin |
| `shield_installed_jumpers_t03m48s_x3.jpg`, `shield_installed_t03m58s_x3.jpg` | Board fitted, jumpers in place, base servo lead not yet connected |
| `final_servo5_plugged_t04m24s_x3.jpg`, `final_controller_overview_t04m24s.jpg` | End of Controller.mov: base servo on row 5, both ribbons, B8's engraving |
| `digital_legends_servo_in_row5_t04m24s_x7.jpg`, `servo5_plug_rows_t04m24s_x12_ticks.jpg` | RX 0, TX 1, 2, 3, 4, 5 legends, the S V G letters, the plug on row 5 (ticks are frame pixels) |
| `Arm_mov_t05m28s_flag6_servo_on_R8_frame.jpg` | Arm.mov: the low-z side servo being fitted in the frame engraved R8, flag 6 on its lead |
| `Arm_mov_t05m56s_overview_flag6_servo5.jpg`, `Arm_mov_t05m56s_shield_top_view_x4.jpg` | Arm.mov: flag 6 on the left side servo's lead, flag 5, near-vertical view of the board with all legends |
| `Claw_mov_t07m05s_finished_wiring.jpg`, `Claw_mov_t07m00s_leads_through_R4_R5_R6.jpg` | Finished kit from the student's seat: leads through R4's slot and the R5 / R6 hooks, extension joint inside R4 |
| `cad_pin_map_student_view.png` | Drawing from the CAD data: every named pin, the pins in use in the real wire colours |
| `cad_joystick_silk_NAUO80.png` | The legend modelled on the CAD joystick board |
| `cad_B8_top_student_view.png` | CAD B8 engraving seen from the student's seat |
| `cad_outline_NAUO13.png`, `cad_outline_NAUO15.png`, `cad_outline_NAUO14.png` | R4, R5, R6 outlines with the slots and the points where leads cross |
| `cad_outline_NAUO5.png`, `cad_outline_NAUO3.png` | B6 and B4 outlines (shield notches, posts) |

## How it was measured, and limits

- Pin tops: the highest vertices of each header mesh, grouped along the header. Joystick pins: the separate solids
  inside `5x_Ang_Conn_1`. Wire ends: each tube followed along its surface from one end face to the other; exact end
  centres and tube numbers taken from `cad_wires.json`.
- Wood: each part's face outline and holes were extracted and each wire's centre line tested where it crosses the
  part's mid-plane.
- Names come from video stills, not from the CAD (the CAD shield has no printed legend; the CAD joystick does).
- Not checked: what the `GND` and `AREF` rows and the three small headers carry; the numbers on the flags for rows 9 and
  10; which side servo is shoulder and which elbow.
