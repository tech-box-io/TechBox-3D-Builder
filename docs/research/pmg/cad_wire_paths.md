# PMG: wire paths from the CAD

Written 19 Oct 2026 by the wire-path study. Data: `docs/research/pmg/wire-paths-draft.json` (a draft for
`PMG Build Instructions/wire-paths.json`; same layout as the MRA's and RCC's files where it fits, one line of JSON, 1.1 MB).
Scripts, all in `docs/research/pmg/scripts/` and prefixed `wp_` because other studies share that folder:
`wp_glb.py` (reads single meshes of the 167 MB `pmg.glb` without loading the file), `wp_components.py` (splits bodies into solids),
`wp_extract.py` (centre lines), `wp_caps_pins.py` (caps and pins), `wp_links.py` (wire end -> cap -> pin), `wp_cadasio_replay.py` and
`wp_cadasio_match.py` (the published guide, replayed per solid and matched to the STEP), `wp_draft.py` (groups everything, writes the
JSON). They write their working files to the session scratchpad; run them in that order to rebuild the JSON (about 9 minutes, under
450 MB of memory).
All coordinates are mm in the assembly space of `PMG Build Instructions/pmg.glb` (Y up), as `stepgen.Model` uses them. Ids are the
CAD's top-level instances (`NAUOn`). "Measured" means computed from the CAD geometry. "Published" means TechBox's Cadasio guide
(`instructions.online/?id=19075-piano_memory_game_pmg-full_build`). Anything that is a guess says so.

STATUS: complete. Open points and questions are in section 10.

## Short answers

- **No colours in the GLB.** `pmg.glb` has one material (`mat_0`, the converter's default). The 21 colours are the published guide's
  (section 6); the draft gives each wire its colour.
- **Every wire body is one wire.** The STEP has 109 jumper-wire bodies and 3 USB-cable bodies; each is ONE round tube (no ribbon or
  bundle is modelled as one body). Every jumper wire is 1.25 mm across (radius 0.625; NAUO163 0.635). The centre lines fit the CAD
  tubes to 0.01 mm. The USB cable is 4.6 mm across (radius 2.30).
- **Caps.** 139 Dupont caps: 131 `Wire Cap` (1.75 x 1.75 x 8.0 mm) and 8 `Wire Cap V2` (12.0 mm long, only on one end of the 12-wire
  ribbon's loose straight wires).
  A routed wire ends exactly on the outer end face of a cap (gap 0.00 mm, 5 bodies up to 1.6 mm off, section 7). A cap stays with
  the pin it is on: the same cap serves every pose that has the same device pose (NAUO8 on G4 of the bench module is used by the
  bench wire NAUO24 and by the in-case wire NAUO144).
- **The 21 wires** are all identified, pose by pose (section 3), but the STEP is an older state of the CAD than the one the published
  guide was made from, and for the wires that matters:
  1. **The four button VCC wires do not exist in the STEP** (no body, no cap on V4 - V7, no cap on the buttons' VCC pins) in any pose.
     The published guide has them (Steps 3, 6, 9, 12).
  2. **The STEP's button GND wires sit on the button's VCC pin.** The published guide labels a button's pins VCC, OUT, GND (pin 0,
     1, 2 below) and plugs its GND wire onto pin 2; the STEP plugs the G-row wire onto pin 0. The OUT wires agree.
  3. **The STEP's bench matrix NAUO44 is wired the reverse way round from the matrix in the case** (VCC and CLK swapped, GND and CS
     swapped, DIN right). The published guide turns the bench matrix half a turn about X (and so moves it 29.4 mm along +Z), which
     makes it agree with the case; the STEP's in-case matrix wiring agrees with the published guide.
  4. **The published guide mounts the I/O module on H4 the other way up**: its module on H4 (seated, and held above) is the STEP's
     NAUO78 / NAUO94 turned half a turn about X, USB end at the top (the STEP has the USB end at the bottom, by the floor). Every
     in-case wire of the published guide was re-drawn to match. So none of the STEP's in-case module-end routes matches the published
     guide.
  5. Two matrix wires are on the wrong module pin in the STEP (NAUO177 on G9, NAUO274 on S11), one wire is missing
     (CS of the "matrix held above" pose), and the loose straight wires for Steps 11 - 14 are missing (4 of the 12-wire ribbon).
- **Lengths differ wildly between poses of one wire** (the engineer drew each pose to fit): a button wire is 47 - 58 mm on the bench,
  133 - 184 mm with the module on H4, 245 - 288 mm with the module held above H4; matrix wires run from 187 to 329 mm. The real
  jumper length is unknown (question 1). The published guide's loose "token" wires are 58.2 / 58.8 mm.
- **Device pins** (all poses, published names): button pins 0 / 1 / 2 = VCC / OUT / GND; display (low y to high y on the bench)
  GND / VCC / DIO / CLK; matrix (low y to high y on the STEP's bench matrix) VCC / GND / DIN / CS / CLK. The I/O module is the MRA's
  board: G V S columns, rows D0 - D13 in four blocks (section 2).
- **USB cable**: three poses (bench NAUO277 99.8 mm, module held above NAUO284 58.4 mm, module on H4 NAUO285 66.4 mm), from the
  right-angle Mini-B plug to the A end. Only the bench pose matches the published guide (Steps 25 - 45). The CAD draws only a short
  stub of cable in each pose.

## 1. Centre lines (top-level `NAUOn` keys)

Method: as the RCC study (`docs/research/rcc/cad_wire_paths.md` section 1), adapted to bodies that are a single tube.

- Each wire instance was read alone (positions and normals of its one mesh) and welded at 0.001 mm; every body is one connected solid.
- Every side vertex moved in by the radius along its own normal lands on the centre line. Those points were put in order by the
  distance over the mesh from one end (a wire that doubles back near itself, such as the matrix wires hooking into their caps,
  is not confused), binned every 0.5 mm, averaged, re-projected onto the line within 6 mm of their previous place, and binned again
  (five rounds; the radius is re-measured each round).
- The two flat end faces give the end points (`end_a`, `end_b`, exact). The line is resampled every 1 mm.
- `check`: distance of every side vertex from the final line. For the jumper wires 1 % - 99 % lie within 0.601 - 0.643 mm of a
  0.625 mm radius (the facets of the CAD's tube); NAUO294 has a few vertices up to 1.27 mm (a local crease in the CAD body), NAUO191
  0.81. The loose straight wires are exact (0.625 everywhere).
- `dir_a`, `dir_b`: unit vectors pointing out of the wire at each end (into the cap).

| Group | Instances (CAD names) | Wires | Length (mm) |
|---|---|---|---|
| Bench: buttons (NAUO4 - 7) to module NAUO1 | NAUO24 - 31 (Part36 - 43) | 8 (GND, OUT) | 47.5 - 58.3 |
| Bench: display NAUO80 to NAUO1 | NAUO40 - 43 (Part44 - 47) | 4 | 76.1 - 81.0 |
| Bench: matrix NAUO44 to NAUO1 | NAUO55 - 59 (Part48 - 52) | 5 | 188.2 - 214.1 |
| Buttons in the case to NAUO1 on the bench | NAUO144, 145, 150, 151, 156, 157, 162, 163 | 8 | 143.3 - 167.8 |
| Buttons in the case to module held above H4 (NAUO94) | NAUO146, 147, 154, 155, 160, 161, 166, 167 | 8 | 245.0 - 287.7 |
| Buttons in the case to module on H4 (NAUO78) | NAUO148, 149, 152, 153, 158, 159, 164, 165 | 8 | 133.0 - 184.2 |
| Display on the bench to NAUO78 / to NAUO94 | NAUO168 - 171 / NAUO172 - 175 | 4 + 4 | 94.4 - 96.7 / 194.8 - 213.8 |
| Display held aside (NAUO129) / seated (NAUO79) to NAUO78 | NAUO195 - 198 / NAUO263 - 266 | 4 + 4 | 154.4 - 162.8 / 105.2 - 112.4 |
| Matrix on the bench to NAUO94 / to NAUO78 | NAUO286 - 289 + 292 / NAUO290, 291, 293 - 295 | 5 + 5 | 235.6 - 265.7 / 191.9 - 215.5 |
| Matrix held in front (NAUO82) to NAUO78 | NAUO176 - 179, 296 | 5 | 307.5 - 328.6 |
| Matrix seated (NAUO81) to NAUO1 / NAUO94 / NAUO78 | NAUO180 - 184 / 185 - 189 / 190 - 194 | 5 + 5 + 5 | 240.2 - 247.8 / 202.6 - 223.7 / 187.2 - 196.5 |
| Matrix held above (NAUO267) to NAUO1 | NAUO273 - 276 | 4 (CS missing) | 271.4 - 279.8 |
| Loose straight wires, 12-wire ribbon | NAUO207 - 210, 219 - 222 | 8 of 12 | 58.19 |
| Loose straight wires, 9-wire ribbon | NAUO247 - 258 | 12 (9 used) | 58.77 |
| USB cable | NAUO277, NAUO284, NAUO285 | 3 | 99.8, 58.4, 66.4 |

## 2. Caps and the pins they sit on (`caps`, `caps_on_pins`, `pins`)

Each cap: `kind`, `centre`, `axis` (unit, along its length), `length_mm`, `face_plus` / `face_minus` (centres of its two end faces),
`sits_on` (`device`, `pin`), and `wires` (the bodies that end in it, with which face). `caps_on_pins` turns that round:
`caps_on_pins[device instance][pin] = cap`. A pin's tip is inside its cap: on the module 2.2 mm short of the wire face, on the display
1.9 mm, on the bench matrix 5.0 mm; on the bench buttons the pin runs right through to the wire face (a CAD simplification).

**I/O module** (NAUO1 on the bench, NAUO94 held above H4, NAUO78 on H4). It is the MRA's board, same headers (CAD suffix `_N` = G,
`_R` = V, `_B` = S, as `docs/research/mra/cad_pins.md`). Pin tops measured on NAUO1 and carried to the other two by the CAD's own
transforms. NAUO1: pins point +Y, tops at y 887.97; columns G x 653.63, V 656.12, S 658.61 (G at the board edge); rows (z) D4 1290.78,
D5 1293.32, D6 1295.86, D7 1298.40 | D8 1303.33, D9 1305.87, D10 1308.41, D11 1310.95 | D12 1315.88, D13 1318.42 (USB end +Z).
NAUO78: pins point +X, tops at x 604.34; columns G z 1310.42, V 1307.93, S 1305.44; rows (y) D4 941.06 down to D13 913.42 (same
spacing). NAUO94: the same 104.7 mm higher (D4 y 1045.74; z +0.1). All 51 module caps sit within 0.04 mm of their pin's axis;
button, display and in-case matrix caps within 0.21 mm.

| Module pin | NAUO1 cap | NAUO94 cap | NAUO78 cap |
|---|---|---|---|
| G4 S4 / G5 S5 | NAUO8 NAUO9 / NAUO10 NAUO13 | NAUO106 NAUO107 / NAUO109 NAUO104 | NAUO97 NAUO96 / NAUO95 NAUO99 |
| G6 S6 / G7 S7 | NAUO15 NAUO12 / NAUO14 NAUO11 | NAUO105 NAUO110 / NAUO103 NAUO108 | NAUO98 NAUO100 / NAUO102 NAUO101 |
| S8 S9 V9 G9 | NAUO38 39 37 36 | NAUO120 121 122 123 | NAUO111 112 113 114 |
| V11 G11 S11 S12 S13 | NAUO51 50 54 53 52 | NAUO125 126 124 127 128 | NAUO116 117 115 118 119 |
| V4 - V7 | none | none | none |

**Buttons** (bench NAUO7, 6, 5, 4 = buttons 1 - 4, wired to rows 4 - 7; in the case NAUO76, 83, 84, 85 = buttons 1 - 4, in that
order along +Z). Three right-angle pins (the CAD's `Socket_Blok`; one of the four meshes is a duplicate). On the bench the pins point
down (-Y), tips at y 934.5, x 641.4, z (button 1) 1273.28 / 1275.78 / 1278.28 = pin 0 / 1 / 2; in the case they point (0.992, 0.124,
-0.005), tips at x 520.3, pin 0 at the +Z end. Published names: **pin 0 VCC, pin 1 OUT, pin 2 GND** (the published labels sit on
"Socket-2", "Socket-1", "Socket-3" of Big Button Module-4 = pins 0, 1, 2, and its re-drawn GND wire ends on a cap on pin 2). In the
STEP every button has caps on pins 0 and 1 only: pin 0 carries the G-row wire, pin 1 the S-row wire.

| Button | bench device | VCC (pin 0) cap | OUT (pin 1) cap | GND (pin 2) | case device | VCC cap | OUT cap | GND |
|---|---|---|---|---|---|---|---|---|
| 1 (row 4) | NAUO7 | NAUO16 | NAUO17 | none | NAUO76 | NAUO86 | NAUO87 | none |
| 2 (row 5) | NAUO6 | NAUO19 | NAUO18 | none | NAUO83 | NAUO88 | NAUO89 | none |
| 3 (row 6) | NAUO5 | NAUO20 | NAUO21 | none | NAUO84 | NAUO90 | NAUO91 | none |
| 4 (row 7) | NAUO4 | NAUO22 | NAUO23 | none | NAUO85 | NAUO93 | NAUO92 | none |

**Display** (bench NAUO80, held 80 mm to the side NAUO129, seated NAUO79). Four straight pins, pitch 2.40. Bench: pins point +Z,
tips at x 658.58, z 1244.05, y 921.58 / 923.98 / 926.38 / 928.78 = **GND / VCC / DIO / CLK** (the STEP's wiring and the published labels
agree). Caps: NAUO80 CLK NAUO32, DIO NAUO33, VCC NAUO34, GND NAUO35; NAUO129 NAUO130 / 132 / 131 / 133; NAUO79 NAUO259 / 260 / 261 / 262.

**Matrix** (bench NAUO44; held in front NAUO82; held above NAUO267; seated NAUO81). Five right-angle header pins, pitch 2.54.
Bench (STEP): pins point +Z, tips at x 648.21, z 1471.53, y 918.05 / 920.59 / 923.13 / 925.67 / 928.21 = pin 0 - 4. Seated: pins point
-Z, pin 0 at the top (536.96, 959.66, 1223.16) down to pin 4 (530.43, 951.87). Published names, by physical pin: **pin 0 VCC, 1 GND,
2 DIN, 3 CS, 4 CLK** (the published bench labels, carried through Cadasio's own transforms to the seated matrix, land on pins 0 - 4
in that order; the STEP's in-case wiring agrees; the STEP's bench wiring is the reverse, section 7). Caps: NAUO44 VCC NAUO49 ... CLK
NAUO45 (the bench caps are 0.53 - 0.56 mm off their pins' axes); NAUO82 NAUO139 - 143; NAUO81 NAUO134 - 138; NAUO267 NAUO268 - 272 (NAUO271,
on CS, has no wire).

## 3. The 21 wires and their poses (`wires`, `poses`, `jumper_wires`)

`wires` lists the 21 wires in the published order: `id`, `device`, `device_pin`, `module_pin`, `published_step`, `colour`, the
Cadasio names of its token and routed bench wire, `poses` (pose -> body, length, the two caps, the pins it is really on; `null` = the
pose exists but the STEP has no body for this wire; flags `WRONG_MODULE_PIN_in_STEP` / `WRONG_DEVICE_PIN_in_STEP`),
`length_spread_mm`, and the caps it would use in each device and module pose (`module_cap_by_module_pose`,
`device_cap_by_device_pose`, read off `caps_on_pins` by its pins; `null` where the STEP has no cap there).
`jumper_wires` has one entry per routed body, its points ordered **from the device to the module**, with `device_end`,
`device_end_direction`, `module_end`, `module_end_direction`, the caps and gaps, and `in_published_guide` (the Cadasio component
that is the same body, if the published guide shows it).

Lengths (mm) of each wire's body in each pose of the STEP. B = buttons, D = display, M = matrix; "M1" = module on the bench NAUO1,
"M94" = held above H4, "M78" = on H4. A dash: the STEP has no body. (Device pin in brackets where the STEP has it on the wrong pin.)

| Wire | module pin | colour | bench (M1) | devices in case, M1 | M94 | M78 |
|---|---|---|---|---|---|---|
| button1 VCC | V4 | #b70101 | - | - | - | - |
| button1 OUT | S4 | #e4e4e4 | NAUO25 52.5 | NAUO145 167.8 | NAUO147 287.7 | NAUO149 179.1 |
| button1 GND | G4 | #343232 | NAUO24 51.2 (VCC) | NAUO144 156.3 (VCC) | NAUO146 283.5 (VCC) | NAUO148 184.2 (VCC) |
| button2 VCC | V5 | #21f17a | - | - | - | - |
| button2 OUT | S5 | #7c5a30 | NAUO27 49.0 | NAUO151 150.5 | NAUO154 267.5 | NAUO153 161.1 |
| button2 GND | G5 | #ffdc00 | NAUO26 47.5 (VCC) | NAUO150 143.3 (VCC) | NAUO155 278.9 (VCC) | NAUO152 170.3 (VCC) |
| button3 VCC | V6 | #85144b | - | - | - | - |
| button3 OUT | S6 | #737980 | NAUO29 51.3 | NAUO157 150.2 | NAUO161 248.4 | NAUO159 139.9 |
| button3 GND | G6 | #3876ac | NAUO28 48.3 (VCC) | NAUO156 144.4 (VCC) | NAUO160 245.0 (VCC) | NAUO158 133.6 (VCC) |
| button4 VCC | V7 | #a75294 | - | - | - | - |
| button4 OUT | S7 | #ff4136 | NAUO31 58.3 | NAUO163 158.7 | NAUO167 247.8 | NAUO165 135.0 |
| button4 GND | G7 | #3d9970 | NAUO30 52.0 (VCC) | NAUO162 159.0 (VCC) | NAUO166 252.1 (VCC) | NAUO164 133.0 (VCC) |

| Wire | module pin | colour | D bench, M1 | D bench, M94 | D bench, M78 | D aside NAUO129, M78 | D seated NAUO79, M78 |
|---|---|---|---|---|---|---|---|
| display CLK | S8 | #ac9400 | NAUO40 81.0 | NAUO172 202.2 | NAUO168 96.6 | NAUO195 161.2 | NAUO263 105.2 |
| display DIO | S9 | #000000 | NAUO41 81.0 | NAUO173 194.8 | NAUO169 94.5 | NAUO196 162.8 | NAUO264 110.6 |
| display VCC | V9 | #ab53ca | NAUO42 76.1 | NAUO174 205.0 | NAUO170 96.7 | NAUO197 161.3 | NAUO265 112.4 |
| display GND | G9 | #bb3d3d | NAUO43 76.1 | NAUO175 213.8 | NAUO171 94.4 | NAUO198 154.4 | NAUO266 110.4 |

| Wire | module pin | colour | M bench NAUO44, M1 | NAUO44, M94 | NAUO44, M78 | in front NAUO82, M78 | seated NAUO81, M78 | (NAUO81, M1) | (NAUO81, M94) | (above NAUO267, M1) |
|---|---|---|---|---|---|---|---|---|---|---|
| matrix VCC | V11 | #411900 | NAUO55 214.1 (CLK) | NAUO286 235.6 (CLK) | NAUO291 191.9 (CLK) | NAUO176 307.5 | NAUO190 188.3 | NAUO180 241.2 | NAUO185 202.6 | NAUO273 272.0 |
| matrix GND | G11 | #339f3f | NAUO56 208.3 (CS) | NAUO287 249.7 (CS) | NAUO293 207.0 (CS) | NAUO177 320.9 on G9 | NAUO191 191.9 | NAUO181 240.2 | NAUO186 213.3 | NAUO274 278.2 on S11 |
| matrix DIN | S11 | #2a2f62 | NAUO57 205.2 | NAUO288 250.8 | NAUO294 214.1 | NAUO178 328.6 | NAUO192 187.2 | NAUO182 245.8 | NAUO187 206.3 | NAUO275 271.4 |
| matrix CS | S12 | #662639 | NAUO58 195.8 (GND) | NAUO289 265.7 (GND) | NAUO295 215.5 (GND) | NAUO179 316.4 | NAUO193 196.5 | NAUO183 245.4 | NAUO188 211.6 | - |
| matrix CLK | S13 | #377e89 | NAUO59 188.2 (VCC) | NAUO292 262.4 (VCC) | NAUO290 214.3 (VCC) | NAUO296 318.7 | NAUO194 194.7 | NAUO184 247.8 | NAUO189 223.7 | NAUO276 279.8 |

The poses in brackets (matrix seated or held above while the module is still on the bench or held above H4) are not states of the
published build order (module on H4 at Step 46, matrix on the brackets at Step 50); they look like an earlier order.

Where the published guide uses one of these bodies unchanged: NAUO25, 27, 29, 31 (the bench OUT wires, from their Step Nc to Step 34),
NAUO40 - 43 (the bench display wires, Steps 16c - 45), NAUO145 (button 1's OUT wire with the buttons in the case, Steps 34c - 45). Every other routed
wire of the published guide is a different body (re-drawn in the later CAD).

## 4. Lengths

A real wire has one length; the CAD draws each pose to fit (as on the RCC). Spread per wire, smallest to largest body:
button OUT and GND wires 47.5 - 287.7 mm (bench 47.5 - 58.3; module on H4 133.0 - 184.2; module held above 245.0 - 287.7), display wires
76.1 - 213.8 (seated 105.2 - 112.4), matrix wires 187.2 - 328.6 (seated 187.2 - 196.5). The finished game (module on H4, everything
seated) needs at most 184.2 mm; the module held 104.7 mm above H4 needs up to 287.7 mm, which a 20 cm jumper could not reach. The
published guide's loose straight wires are 58.2 mm (12-wire ribbon) and 58.8 mm (9-wire ribbon) between caps, a stand-in, not the real
length. Measure a kit jumper (question 1); then draw every pose at that length, with `stretch` where the shape changes a lot.

## 5. The loose straight wires (`loose_wires`)

The STEP has two groups of straight wires lying side by side, each with an 8 mm cap on one end (z 1329.4 - 1337.4) and a cap on the
other (z 1267.9 - 1279.9; the first group's are the 12 mm `Wire Cap V2`). They are the published guide's ribbons (Steps 2 and 15) and
its "tokens" (the one loose straight wire shown at each wire's Step N). The wires run 3.25 mm into the 8 mm caps and 3.5 - 4.0 mm into
the other caps.

- **`ribbon_12`** (Copy of Copy of Part15 - 18, Copy (2) of Copy of Part15 - 18): NAUO207, 208, 209, 210, 219, 220, 221, 222 at
  x 708.0 - 720.2 (pitch 1.74 - 1.75), y 894.4 - 894.5, from z 1334.1 to 1275.9 (58.19 mm). They are the tokens of Steps 3 - 10 in
  that order (colours below). **Four are missing**: the published guide has "Copy (2) of Copy of Part17-3 .. -6" (tokens of Steps 11 -
  14, #3876ac, #a75294, #ff4136, #3d9970), which are NAUO222 moved +1.74, +3.48, +5.22, +6.96 mm along X, each with copies of its caps
  NAUO211 and NAUO215 moved the same (`loose_wires.missing_from_STEP`).
- **`ribbon_9`** (Part125 - 137): NAUO247 - 258 at x 730.6 down to 711.4 (pitch 1.74 - 1.76), y 901.4 - 901.6, z 1334.2 to 1275.4
  (58.77 mm). The published guide uses nine: NAUO255, 253, 254, 252 (display tokens, Steps 16 - 19), NAUO251, 250, 249, 248, 247 (matrix
  tokens, Steps 20 - 24). NAUO256 - 258 are never shown.

Where the published guide shows them (Cadasio offset from the CAD place, mm, the same for the wire and its caps):

| | Step 2 (ribbon) | Step 2c (fanned) | each token's Step N |
|---|---|---|---|
| 12-wire ribbon | all (-116.0, 0, -26.5) | X -133.25, -129.99, -126.40, -122.98, -120.04, -117.09, -113.96, -110.95, then the four missing -107.89, -104.93, -101.81, -99.06 (Y 0, Z -26.5) | back to (-116.0, 0, -26.5) |

| | Step 15 (ribbon) | Step 15c (fanned) | each token's Step N |
|---|---|---|---|
| 9-wire ribbon | all (-124.78, 0, +49.6) | X Part125 -115.53, 126 -117.85, 127 -120.25, 128 -123.00, 129 -125.75, 130 -128.30, 134 -131.19, 132 -133.87, 133 -136.68 | (-124.78, 0, +49.6), except Steps 17 - 19: (-124.78, 0, +9.58) |

So on Step 2 the ribbon lies at x 592.0 - 611.2 (with the four missing wires), y 894.5, z 1249.4 - 1307.6, to the -X side of the bench
module (x 647 - 700); fanned out (2c) the wires spread to 4.5 - 5.4 mm apart (x 574.7 - 628.1). At its Step N a token lies where it
lay in the ribbon. The 9-wire ribbon lies at x 592.0 - 606.0, y 901.5, z 1325.0 - 1383.8, and fans out to 4.1 - 4.7 mm apart
(x 580.0 - 615.2); the tokens of Steps 17 - 19 lie 40 mm nearer (z 1285.0 - 1343.8).
Our player draws a wire as a tube: the tokens are routes with `a` = one cap, carried as one unit (or drawn without caps tied).

## 6. Colours

- In `pmg.glb`: none. The file has one material, the converter's default; every wire body, cap and cable is that grey-blue.
- Published (Cadasio colour of the routed wire of each Step Nc, the same as its token's), in `wires[].colour`:
  button 1 VCC #b70101, OUT #e4e4e4, GND #343232; button 2 VCC #21f17a, OUT #7c5a30, GND #ffdc00; button 3 VCC #85144b, OUT #737980,
  GND #3876ac; button 4 VCC #a75294, OUT #ff4136, GND #3d9970; display CLK #ac9400, DIO #000000, VCC #ab53ca, GND #bb3d3d; matrix VCC
  #411900, GND #339f3f, DIN #2a2f62, CS #662639, CLK #377e89. Colour follows the order of the ribbon, not the signal (as the earlier study
  says). Caps black #000000. USB cable #1e1616, its plugs #1e1616 with #e4e4e4 metal.
- `loose_wires[*].published_colour` gives each straight wire's colour (only the nine / eight used).

## 7. The STEP against the published guide, and CAD slips

The Cadasio project was made from version 7 of the CAD (uploaded 4 Aug 2026, 415 parts). The STEP Lee sent was exported on 19 Oct 2026
at 00:14 from SolidWorks 2026, but it holds an older state (296 parts). Measured part by part (Cadasio boxes and transforms against the
GLB):

- **The same** (0.00 - 0.13 mm): the bench module NAUO1, the bench buttons NAUO4 - 7, the bench display NAUO80, the buttons in the
  case NAUO76 / 83 / 84 / 85, the seated display NAUO79, the seated matrix NAUO81, the matrix held in front NAUO82, the matrix held above
  NAUO267 (1.9 mm), all the wood, all the loose straight wires and their caps, the bench USB cable (NAUO277, 278, 279), the caps of the
  bench and the in-case buttons, and the wire bodies listed at the end of section 3.
- **Turned half a turn about X**: the module on H4 (published "Ensamblaje_Shield_NANO-2" = NAUO78 turned 180 degrees about the
  X-parallel line through y 931.6, z 1290.5) and the module held above (NAUO94 about y 1035.1, z 1290.7), with their Nano and USB
  plug. So in the published guide the module's USB end is at the top (plug at y 962.9) where the STEP has it at the bottom (y 900.1),
  and rows D4 - D7 are at the bottom. Every published in-case wire and cap differs from the STEP's (by 30 - 60 mm).
- **Turned half a turn about X**: the bench matrix (published LED Matrix-1 = NAUO44 turned 180 degrees about the line through y 923.8,
  z 1420.3; centre moved from z 1405.6 to 1435.0, header now towards the module). This flip is what makes the published bench wiring
  and the case wiring land on the same physical pins. The published bench matrix wires are new bodies ("V11 to VCC", "G11 to GND",
  "S1 to DIN", "S12 to CS", "S13 to CLK").
- **Display approach poses**: the published guide brings the display in through two poses of its own (Display TM1637-6 / -7, 5.9 -
  13.0 mm from the seat); the STEP's NAUO129 (80 mm to the side) is not used. The matrix likewise (published LED Matrix-8 / -9, 7.6 -
  23.4 mm from the seat); the STEP's NAUO82 and NAUO267 exist in the project but are never shown.
- **Missing from the STEP**: the four button VCC wires in every pose and their caps (published bench: Part168, 170, 172, 174 with caps
  Wire Cap-160 - 163 on V4 - V7 and the button caps Wire Cap-10 / 13 / 14 / 16 = the STEP's NAUO16, 19, 20, 22, which the STEP uses for
  GND); the GND-pin caps of the buttons (published Wire Cap-164 - 167 on the bench, 168 - 171 in the case); four loose straight wires
  (section 5); the CS wire of the "matrix held above" pose (published Part150; its cap NAUO271 is there).
- **Different in the STEP**: the button GND wires (bench NAUO24, 26, 28, 30 are published Part169, 171, 173, 175, re-drawn onto pin 2);
  in the case with the module on the bench only NAUO145 is the published body (Part54); the published bench matrix (above).

CAD slips inside the STEP:

1. Button GND wires on the button's VCC pin, in every pose (16 bodies), if the published pin names are right (question 2).
2. The bench matrix's five wires (and the ten that run from NAUO44 to the module on H4 / held above) land on the reversed pins:
   V11 -> CLK pin, G11 -> CS pin, S12 -> GND pin, S13 -> VCC pin (DIN right). The in-case matrix wiring is the other way round.
3. NAUO177 (matrix held in front, GND wire) ends on G9 (cap NAUO114, shared with the display's GND wire) instead of G11.
4. NAUO274 (matrix held above, GND wire) ends on S11 (cap NAUO54, shared with NAUO275, the DIN wire) instead of G11.
5. Cap NAUO103 (G7 on the module held above) is pushed 2.26 mm further onto its pin than its neighbours (centre x 600.25 against
   602.51); NAUO166 ends on it.
6. Small gaps between a wire's end and its cap face: NAUO158 1.60 mm (cap NAUO90), NAUO294 0.89 / 0.67, NAUO191 0.58, NAUO171 0.17,
   NAUO291 0.14 mm. All others 0.00 - 0.06.

## 8. The USB cable (`usb`)

Three bodies, each a round cable 4.6 mm across (radius 2.30 on the bench, 2.25 measured in the other two), points ordered from the
right-angle Mini-B plug to the A end:

| Body | Pose | Mini-B plug | A end | Length | Fit |
|---|---|---|---|---|---|
| NAUO277 ("Copy of Part23") | bench: plug in the bench module's Nano NAUO1 | NAUO279, cable leaves its x 655.04 face heading -X | NAUO278, lying flat on the bench, cable enters its z 1374.07 end | 99.8 | exact (2.297 - 2.305) |
| NAUO284 (Part152) | module held above H4 | NAUO281 (611.4, 1004.6, 1297.1) | NAUO280, standing on end, enters at y 969.1 | 58.4 | a kink by the plug; the line there is within about 1.7 mm |
| NAUO285 (Part153) | module on H4 | NAUO282 (611.2, 900.1, 1297.0) | NAUO283, lying along X, enters at x 631.0 | 66.4 | a kink by the plug (bent tighter than its own radius); line within about 1.7 mm there, ends up to 2.3 mm short |

The bench pose is the published one (Steps 25 - 45; the published Step 25 shows the plug 22.9 mm out of its socket and the cable with
it). The published guide's other two cable poses are different (its module is turned, section 7). The CAD models only a short stub of
cable between plug and A end; a real cable is far longer, so the guide will draw it (as the MRA and RCC guides do with `W.curve`).

## 9. Using the draft

`paths = W.load('.../wire-paths-draft.json')`, then for example (mm, assembly space):

- a CAD route as it is: `W.route(paths['NAUO40'][0]['points'], a='NAUO80', b='NAUO1')` (display CLK, bench; points run display ->
  module for NAUO40, check `end_a`); or from `paths['jumper_wires']`, whose points always run device -> module:
  `j = next(j for j in paths['jumper_wires'] if j['body'] == 'NAUO263')`, `W.route(j['points'], a=j['device'], b=j['module'])`;
- the caps for a wire by its pins: `paths['caps_on_pins']['NAUO1']['S8']` (= NAUO38), `paths['caps_on_pins']['NAUO80']['CLK']` (= NAUO32);
  with ONE cap part per wire end in the guide, the caps of other poses are where that cap goes when its device moves (they agree with
  the device's pose to the CAD's precision, apart from NAUO103).
- a wire end drawn by hand: start at the cap's wire face (`caps[c]['face_plus']` or `face_minus`, the one listed in `caps[c].wires`),
  leaving along the cap's axis away from the pin.

What is NOT in the draft: routes for the four VCC wires, routes for the published in-case poses (module turned), the published bench
matrix pose. Those have to be drawn (`W.smooth`, `W.curve`) once Lee has answered the questions below.

## 10. Open points and questions for Lee

1. **Jumper length.** How long are the kit's jumper wires (10, 20 or 30 cm)? The CAD's poses need 47 - 329 mm; the finished game
   needs up to 184 mm; holding the module 105 mm above H4 (published Step 45c) needs up to 288 mm.
2. **Button pins.** The published guide names a button's pins VCC, OUT, GND (VCC at the end nearest row 4 on the bench), while the STEP
   plugs the GND wire on the pin the guide calls VCC. Which is right on the real board (a photo of the module's pin labels would settle
   it)? The draft follows the published guide.
3. **Module on H4.** Which way up does the I/O module go on H4: USB end at the top (published guide) or at the bottom (the STEP)? Every
   in-case wire route depends on it. If the published way, the guide author turns NAUO78 / NAUO94 half a turn about X and draws the
   in-case wires anew.
4. **Matrix.** Which way round does the matrix lie on the bench (published: header towards the module; STEP: header away)? With the
   published names (VCC on the pin that is at the top when the matrix is on its brackets) the STEP's bench wiring is reversed.
5. Should the guide keep the published ribbons (Steps 2 and 15: 12 and 9 straight wires fanning out) and the token-per-step style, or
   show each wire coming in already routed (house rules: one wire per step)?
6. The published display and matrix come in through approach poses that are not in the STEP; the STEP's own approach poses (display
   80 mm aside, matrix 143 mm in front or 86 mm above) are unused there. Which should the guide use?
