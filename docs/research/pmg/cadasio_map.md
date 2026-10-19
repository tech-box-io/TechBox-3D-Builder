# PMG: the published Cadasio guide mapped onto Lee's CAD, copy by copy

Written 19 Oct 2026. Data: `cadasio_map.json` (same folder): every viewer step's camera, every Cadasio component (visible steps,
moves, colour, its GLB copy), every GLB instance (its Cadasio name, the steps Cadasio shows it, its role), the 21 wires pose by
pose with their caps, every cap's pin. Colours: `colour-atlas-pmg-draft.json`.

Scripts (in `scripts/`, run in this order; each stays under 200 MB): `cadasio_tree.py` (both trees, world boxes), `match.py`
(box and transform match), `replay.py` (what each viewer step shows, and its camera), `wires.py` (pins, caps, wires; reads the
wire bodies' vertices from the GLB through a memory map), `pairs.py` (turn and shift between two copies), `usb_check.py`,
`build_map.py` (writes `cadasio_map.json`), `report_tables.py` (the tables below). Working files: `scripts/work/cadasio_map/`.

Sources: the Cadasio payload `cadasio/raw/19075-piano_memory_game_pmg-full_build.json`, its digest, the earlier study
`../guide_19075-piano_memory_game_pmg-full_build.md`, the step pictures, and `PMG Build Instructions/pmg.glb` (header,
transforms, and the vertices of the wire bodies only). Viewer steps are named as the guide's step list shows them, with the
digest's index: `[007] Step 3`. Millimetres, assembly frame, Y up (the GLB's metres x 1000). The case's front is -X (H1 and the
keys' free ends); the student's right is +Z (H2's side), checked on the Completed View picture.

## Short answers

- **Frame: identity.** Cadasio scene units x 23.6076 = GLB mm, same axes. 159 components coincide exactly (box within
  0.5 mm, same rotation, translation to 0.01 mm).
- **The STEP is not the CAD the published guide was made from.** It is an earlier state of the same SolidWorks assembly
  (Cadasio's copy is CAD version 7, made 4 Aug 2026: 415 top-level components; the STEP has 296). Every rigid part model is
  the same, and the wood, the eight push-button copies, the bench and seated display, the seated matrix, the bench I/O module
  and the bench USB cable are identical. What differs (section 2): each button has only two wires in the STEP (no GND wire, and
  its VCC-pin wire goes to G instead of V); the I/O module on the back panel is upside down (USB end down); the bench dot matrix
  is 29.4 mm nearer and turned end for end, so its five wires land on the mirrored pins; four of the twelve loose wires of the
  first ribbon are missing; the held and half-way poses of the display and the matrix that the guide shows are not there.
- **Built pose** (Completed View): I/O module NAUO78 (turned 180 deg from the published one), buttons NAUO76 / 83 / 84 / 85,
  display NAUO79, matrix NAUO81, USB NAUO282 + 285 + 283, wood NAUO60-75 and NAUO77. Section 3.
- **Buttons**: black, yellow, white, blue, wired to D4, D5, D6, D7, and in that order from the student's left to right in
  the case (z 1241.8, 1274.3, 1306.9, 1339.4). On the bench they stand behind the module in the same order along +Z.
- **The 21 wires**: section 5 (colour, pins, every pose, every cap). The published slips are confirmed by the geometry: Step 10's
  label "S5" is S6 (its cap sits on S6); Steps 16-17 say "clk" / "s8" and "dio" / "s9" in lower case.
- **Colours**: `colour-atlas-pmg-draft.json` (section 7). Button caps black `#000000`, yellow `#ffdc00`, white `#ffffff`,
  blue `#0074d9`; wood `#deb887` with engraving `#1e1616`.
- **Cameras**: all 117 in the JSON (`viewer_steps[*].camera`); one row per distinct camera in section 8.

## 1. Frame

- Cadasio `scaleFactor` 0.0423593: 1 scene unit = 23.6076 mm.
- Example: Cadasio "Big Button Module-1" translation (27.3378, 40.3366, 55.8188) units = (645.39, 952.27, 1317.77) mm; GLB
  NAUO4 (645.38, 952.25, 1317.74) mm; same rotation matrix. Over the 159 identical pairs the rotations agree to 1e-4.
- When reading Cadasio's moves: a `position` override is in the parent's frame. Most moves in this guide are set on a part's
  solids, so the offset must be turned by the part's own CAD rotation to give a world offset. The digest and the earlier study
  print the unturned numbers: their distances are right, but their directions are in the part's frame for parts that are
  turned in the CAD (H2's "(0, 0, 40)" is +40 X in the world, H4's "(0, -65, 0)" is +65 X, the first key's "(0, 0, 108)" is
  -108 X, the bench USB cable's three pieces all move +22.9 Z). The offsets in this report and in the JSON are world offsets.

## 2. The STEP is an earlier version of the published CAD

Evidence:
- SolidWorks numbers new virtual parts upwards. The published CAD has wire bodies Part113-124, Part142-146, Part150, Part166 and
  Part168-207, none of which is in the STEP; the STEP has Part36, 38, 40, 42 and 48-53, which the published CAD no longer has.
  Bodies with the same name in both are often routed differently (Part55: GLB centre (568.3, 972.1, 1277.0), Cadasio
  (572.2, 960.8, 1258.6)).
- The STEP's header is dated 2026-10-19T00:14 (the export); Cadasio's assembly is version 7, created 2026-08-04.
- Every difference below is something the published guide has right and the STEP has not, so the STEP is the earlier state.

What the STEP lacks that the guide shows:
- **The GND wire of each push button**, in all four poses (bench Part169 / 171 / 173 / 175; in the case Part176 / 178 / 180 / 181;
  held Part189 / 188 / 187 / 186; built Part182 / 183 / 184 / 185), the cap on each button's GND pin (bench Wire Cap-164..167,
  case Wire Cap-168..171), and the cap on V4-V7 of each I/O-module pose (bench Wire Cap-160..163, held 175..172, mounted
  179..176). In the STEP each button has two wires: OUT -> S (as published) and a wire from the button's VCC pin to G
  (Part36 / 38 / 40 / 42 on the bench, and their copies in the other poses). The published guide wires VCC -> V and GND -> G.
- **Loose wires 9-12 of the first ribbon** (Cadasio "Copy (2) of Copy of Part17-3..-6", Steps 11-14) and their 8 caps
  (Wire Cap-151..154, Wire Cap V2-9..12). The STEP's first ribbon has 8 wires (NAUO207-210, 219-222).
- **The Nano Board as a part of its own on the bench and on the mounted module** (Cadasio nano-3, nano-4). In the STEP the bench
  module NAUO1 has the Nano's chips in place but not its board or pin rows; NAUO2 and NAUO3 are whole Nanos 44.9 and 15.2 mm
  above that seat; NAUO78 and NAUO94 have their Nano built in. (The guide is to use the MRA's Nano Board anyway.)
- **The display held above the brackets and half-way** (Display TM1637-6, Steps 47c-48; -7, [106] Transition) with wires
  Part190-197 and caps Wire Cap-180..187; **the matrix held and half-way** (LED Matrix -8, Steps 49c-50; -9, [111]) with
  Part166 (one body holding all five wires) and Part203-207, caps Wire Cap-155..159 and 188..192.

What is different:
- **The I/O module on the back panel (NAUO78) and the held copy (NAUO94) are turned 180 deg about X** compared with the published
  ones (Ensamblaje_Shield_NANO-2 / -3): in the STEP the USB end and the power jack are at the bottom and the digital G / V / S
  rows on the +Z side; in the guide at the top and on the -Z side. The back panel H4 is the same in both. So every cap on these
  two copies, every wire into them, and the USB plug and lead in those poses are in other places.
- **The bench dot matrix (NAUO44)** is 29.4 mm nearer the module (centre z 1405.6, published 1435.0) and turned 180 deg about X,
  so its input header is at its far end. Its five wires (Part48-52) keep their order along the header and so land on the
  mirrored pins: V11 -> CLK, G11 -> CS, S11 -> DIN, S12 -> GND, S13 -> VCC (published: VCC, GND, DIN, CS, CLK). The same holds
  for its wires in the held and mounted poses (Part154-162, Part164).
- **USB in the held and built poses**: the plug at the bottom of the turned module, a shorter lead (Part152: 30.8 mm tall,
  published 63.5 mm), the A end elsewhere (built: 11.2 mm to -X and 69.7 mm to +Z of the published one).

Only in the STEP (never shown in the guide): the display held 80.0 mm to +Z of its seat (NAUO129) with wires Part105-108 and
caps NAUO130-133; the matrix 143.3 mm to -Z of its seat (NAUO82) and 85.9 mm above it (NAUO267), with their wires; the seated
matrix wired to the bench and the held module (Part90-99). Two slips in those unused poses: Part86 ends on G9 and Part148 on
S11 where G11 is meant. The published CAD also has spares never shown (H11v2-2, H12v2-1, H14-2, Display TM1637-1 / -5, nano-5,
Part113-124, 142-146, 198-202).

## 3. Which copy is the built pose

| Part | Built copy in the GLB | Against the published Completed View |
|---|---|---|
| Nano I/O Module | NAUO78 (on H4's inner face, x 593.5-618.1) | turned 180 deg about X (USB end down; published: up) |
| Nano Board | built into NAUO78 (board, pin rows, chips) | turned with it; the published guide shows a separate copy (nano-4) |
| Push buttons | NAUO76 black, NAUO83 yellow, NAUO84 white, NAUO85 blue | identical |
| 4-digit display | NAUO79 | identical (0.2 mm) |
| Dot matrix | NAUO81 | identical |
| USB cable | NAUO282 plug, NAUO285 lead, NAUO283 A end | other places (they follow the turned module) |
| Wood H1-H14, keys | NAUO60-75, NAUO77 (H12) | identical; H14 see below |
| Caps on the buttons | NAUO86-93 (VCC, OUT) | identical; the GND caps are missing |
| Wires, buttons | OUT: Part58 / 62 / 68 / 74 (NAUO149 / 153 / 159 / 165); old VCC-to-G: Part57 / 61 / 67 / 73 (NAUO148 / 152 / 158 / 164) | routed into the turned module; GND wires missing |
| Wires, display | Part138-141 (NAUO263-266); caps NAUO259-262 on the display | display end identical, module end differs |
| Wires, matrix | Part100-104 (NAUO190-194); caps NAUO134-138 on the matrix | matrix end identical, module end differs |
| Caps on the module | NAUO95-102, NAUO111-119 | other places (turned module); V4-V7 missing |

H14 (NAUO74): the published guide moves and turns H14 by hand in Steps 51-51c and keeps a small position and turn on it in the
Completed View (its solids turned about 14 deg about Z through an origin point). I could not reduce those overrides to one pose
with confidence; the earlier study took the end state to be the CAD seat, and the Completed View picture shows H14 seated.
Treat NAUO74 as the built pose and check it against the brackets when authoring (not verified).

## 4. Every GLB instance, by kind and pose

The JSON (`glb_instances`) has each NAUO on its own: Cadasio name, relation, role, the steps Cadasio shows it, its moves there.

| GLB instances | What they are |
|---|---|
| NAUO1 | Nano I/O Module, bench |
| NAUO2 / NAUO3 | Nano Board, 44.9 / 15.2 mm above its bench seat |
| NAUO4 / 5 / 6 / 7 | push button 4 blue / 3 white / 2 yellow / 1 black, bench |
| NAUO8-15, 36-39, 50-54 | caps on the I/O module (bench) |
| NAUO16-23 | caps on the push buttons (bench) |
| NAUO24-31 | routed wires: push buttons (bench) to the I/O module (bench) |
| NAUO32-35 | caps on the 4-digit display (bench) |
| NAUO40-43 | routed wires: display (bench) to the I/O module (bench) |
| NAUO44 | dot matrix, bench (turned end for end) |
| NAUO45-49 | caps on the dot matrix (bench) |
| NAUO55-59 | routed wires: matrix (bench) to the I/O module (bench) |
| NAUO60-75, 77 | wood: H6, H8, H11, H1, H10, H2, H3, H5, H7, H9 x4 (69-72), H4, H14, H13; H12 (77) |
| NAUO76, 83, 84, 85 | push buttons 1 black, 2 yellow, 3 white, 4 blue, in the case |
| NAUO78 | Nano I/O Module mounted on H4 (built; turned 180 deg) |
| NAUO79 / NAUO80 | 4-digit display, seated (built) / bench |
| NAUO81 / NAUO82 | dot matrix, seated (built) / aside (never shown) |
| NAUO86-93 | caps on the push buttons (in the case) |
| NAUO94 | Nano I/O Module held above H4 |
| NAUO95-102, 111-119 | caps on the I/O module (mounted on H4) |
| NAUO103-110, 120-128 | caps on the I/O module (held above H4) |
| NAUO129 | 4-digit display held beside its seat (STEP only) |
| NAUO130-133 | caps on the 4-digit display (held beside its seat) |
| NAUO134-138 | caps on the dot matrix (seated) |
| NAUO139-143 | caps on the dot matrix (aside) |
| NAUO144-167 | routed wires, push buttons in the case, two per button, to the I/O module on the bench (144-145, 150-151, 156-157, 162-163), held (146-147, 154-155, 160-161, 166-167) and mounted (148-149, 152-153, 158-159, 164-165) |
| NAUO168-171 / 172-175 | routed wires: display (bench) to the I/O module mounted / held |
| NAUO176-179, 296 | routed wires: matrix (aside) to the I/O module mounted |
| NAUO180-184 / 185-189 / 190-194 | routed wires: matrix (seated) to the I/O module on the bench / held / mounted (built: 190-194) |
| NAUO195-198 | routed wires: display (held beside) to the I/O module mounted |
| NAUO199-206, 211-218, 223-246 | caps of the loose straight wires |
| NAUO207-210, 219-222, 247-258 | loose straight wires (ribbon members and tokens) |
| NAUO259-262 | caps on the 4-digit display (seated) |
| NAUO263-266 | routed wires: display (seated) to the I/O module mounted (built) |
| NAUO267 | dot matrix, raised (never shown) |
| NAUO268-272 | caps on the dot matrix (raised) |
| NAUO273-276 | routed wires: matrix (raised) to the I/O module on the bench |
| NAUO277 / 278 / 279 | USB lead / A end / Mini-B plug, bench |
| NAUO280 / 281 / 284 | USB A end / plug / lead, held pose |
| NAUO282 / 283 / 285 | USB plug / A end / lead, built |
| NAUO286-289, 292 / 290-291, 293-295 | routed wires: matrix (bench) to the I/O module held / mounted |

Totals: 29 rigid electronics pieces, 17 wood, 91 routed wire bodies, 20 loose straight wires, 139 caps = 296.

### 4.1 Rigid parts (electronics)

| GLB | Cadasio component | Relation | Role | Cadasio shows it |
|---|---|---|---|---|
| NAUO1 | Ensamblaje_Shield_NANO-1 | identical | Nano I/O Module on the bench (flat, pins up, USB end +Z). In Cadasio its own Nano is hidden and nano-3 is shown on it; in the GLB this copy has the Nano's chips but not its board or pin rows | [001]-[003] Nano I/O Module to Step 1c, [007]-[033] Step 3 to Step 14c, [037]-[044] Step 16 to Step 19c, [046]-[055] Step 20 to Step 24c, [057]-[058] Step 25 to Step 25c, [073]-[099] Step 33 to Step 45 |
| NAUO94 | Ensamblaje_Shield_NANO-3 | same role, turned 180 deg about X | Nano I/O Module held 104.7 mm straight above NAUO78 (Cadasio: 102.3 mm above its mounted copy) | [100]-[101] Step 45c to Step 46 |
| NAUO78 | Ensamblaje_Shield_NANO-2 | same role, turned 180 deg about X | Nano I/O Module mounted on H4 (BUILT). USB end and jack at the bottom (Y-), digital rows on the +Z side; Cadasio's at the top and on the -Z side | [000] Start, [102]-[116] Step 46c to Completed View |
| NAUO2 | nano-1 | identical | Nano Board 44.9 mm straight above its bench seat | never shown |
| NAUO3 | nano-2 | identical | Nano Board 15.2 mm straight above its bench seat | never shown |
| - | nano-3 | not in the STEP | Nano Board seated on the bench module (Step 1: hovers +29.8 Y) | [002]-[003], [007]-[033], [037]-[044], [046]-[055], [057]-[058], [073]-[099] |
| - | nano-4 | not in the STEP (NAUO78 has its own) | Nano Board on the mounted module | [000], [102]-[116] |
| NAUO7 | Big Button Module-4 | identical | push button 1, BLACK, bench (D4) | [006]-[033] Push Buttons to Step 14c, [037]-[044], [046]-[055], [057]-[058], [073]-[075] Step 33 to Step 34 |
| NAUO6 | Big Button Module-3 | identical | push button 2, YELLOW, bench (D5) | [013]-[033] Transition to Step 14c, [037]-[044], [046]-[055], [057]-[058], [073]-[075] |
| NAUO5 | Big Button Module-2 | identical | push button 3, WHITE, bench (D6) | [020]-[033] Transition to Step 14c, [037]-[044], [046]-[055], [057]-[058], [073]-[075] |
| NAUO4 | Big Button Module-1 | identical | push button 4, BLUE, bench (D7) | [027]-[033] Transition to Step 14c, [037]-[044], [046]-[055], [057]-[058], [073] Step 33 |
| NAUO76 | Big Button Module-5 | identical | push button 1, BLACK, in its slot in H6 (BUILT) | [000] Start, [076]-[116] Step 34c to Completed View |
| NAUO83 | Big Button Module-9 | identical | push button 2, YELLOW, in the case (BUILT) | [000] Start, [076]-[116] |
| NAUO84 | Big Button Module-10 | identical | push button 3, WHITE, in the case (BUILT) | [000] Start, [076]-[116] |
| NAUO85 | Big Button Module-11 | identical | push button 4, BLUE, in the case (BUILT); the first one clipped in | [000] Start, [074]-[116] Step 33c to Completed View |
| NAUO80 | Display TM1637-4 | identical | 4-digit display on the bench | [034] 4-Digit Display, [037]-[044] Step 16 to Step 19c, [046]-[055], [057]-[058], [073]-[103] Step 33 to Step 47 |
| NAUO129 | - | no counterpart | 4-digit display held 80.0 mm to +Z of its seat, same turn as seated, wired to the mounted module (Part105-108) | n/a |
| - | Display TM1637-6 / -7 | not in the STEP | display held above its seat, turned 23.3 deg about -Z, box centre 12.8 mm higher and 4.3 mm to -X / half-way (1.8 higher, 2.7 to -X, same turn) | [104]-[105] Step 47c to Step 48 / [106] Transition |
| NAUO79 | Display TM1637-2 | identical (0.2 mm) | 4-digit display seated on the brackets H11 / H12 (BUILT) | [000] Start, [107]-[116] Step 48c to Completed View |
| NAUO44 | LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-1 | same role, turned 180 deg about X, 29.4 mm nearer | dot matrix on the bench; input header at its far end | [045]-[055] Dot Matrix Display to Step 24c, [057]-[058], [073]-[108] Step 33 to Step 49 |
| - | LED Matrix -8 / -9 | not in the STEP | matrix held in front of the brackets, turned 20.0 deg about -Z, box centre 22.6 mm higher and 3.9 mm to -X / half-way (2.2 higher, 4.6 to -X, same turn) | [109]-[110] Step 49c to Step 50 / [111] Transition |
| NAUO82 | LED Matrix -6 | identical | dot matrix 143.3 mm to -Z of its seat, wired to the mounted module (Part85-88, 163) | never shown |
| NAUO267 | LED Matrix -7 | same role, 1.9 mm along Z | dot matrix 85.9 mm above its seat, wired to the BENCH module (Part147-151) | never shown |
| NAUO81 | LED Matrix -4 | identical | dot matrix seated on the brackets (BUILT) | [000] Start, [112]-[116] Step 50c to Completed View |
| NAUO278 | USB Cable end-1 | identical | USB A end, bench | [056]-[058] USB Cable to Step 25c, [073]-[099] Step 33 to Step 45 |
| NAUO279 | USB Right Angle-1 | identical | right-angle Mini-B plug in the bench Nano (card and Step 25: +22.9 Z, out of the socket) | [056]-[058], [073]-[099] |
| NAUO277 | Copy of Part23-1 | same body (0.7 mm) | USB lead between NAUO278 and NAUO279, bench | [056]-[058], [073]-[099] |
| NAUO280 | USB Cable end-2 | same role, elsewhere | USB A end, held pose; 45.6 mm lower and 97.7 mm to +Z of Cadasio's | [100]-[101] Step 45c to Step 46 |
| NAUO281 | USB Right Angle-2 | same role, turned 180 deg about X | Mini-B plug in the held module's Nano (at its bottom here, its top in Cadasio) | [100]-[101] |
| NAUO284 | Part152-1 | same name, other shape | USB lead, held pose (joins NAUO280 and NAUO281) | [100]-[101] |
| NAUO282 | USB Right Angle-3 | same role, turned 180 deg about X | Mini-B plug in the mounted module's Nano (BUILT) | [000] Start, [102]-[116] |
| NAUO283 | USB Cable end-3 | same role, elsewhere | USB A end on the table behind the case (BUILT); 11.2 mm to -X and 69.7 mm to +Z of Cadasio's | [102]-[116] Step 46c to Completed View |
| NAUO285 | Part153-1 | same name, other shape | USB lead, BUILT (joins NAUO282 and NAUO283) | [102]-[116] |

(The USB pieces were paired by touch: each lead's vertices meet the boxes of exactly its two ends, `scripts/usb_check.py`.)

### 4.2 Wood

| GLB | Cadasio component | Role | Cadasio shows it (built pose; before that it hovers, section 9) |
|---|---|---|---|
| NAUO63 | H1-1 | H1, front rail | [000] Start, [059]-[116] Step 26 to Completed View |
| NAUO65 | H2-1 | H2, side (+Z, the student's right) | [000] Start, [059]-[116] Step 26 to Completed View |
| NAUO66 | H3-1 | H3, side (-Z) | [000] Start, [061]-[116] Step 27 to Completed View |
| NAUO73 | H4v2-1 | H4, back panel (the module mounts on it) | [000] Start, [063]-[116] Step 28 to Completed View |
| NAUO67 | H5-1 | H5, deck with the four button windows | [000] Start, [065]-[116] Step 29 to Completed View |
| NAUO60 | H6-1 | H6, button carrier under the deck | [000] Start, [069]-[116] Step 31 to Completed View |
| NAUO68 | H7-1 | H7, bottom cover | [000] Start, [077]-[116] Step 35 to Completed View |
| NAUO61 | H8-1 | H8, cross divider | [000] Start, [081]-[116] Step 37 to Completed View |
| NAUO72 | PMG_PianoKey_Aug25-4 | H9, key over button 1 (black); the first key (Step 38) | [000] Start, [083]-[116] Step 38 to Completed View |
| NAUO71 | PMG_PianoKey_Aug25-3 | H9, key over button 2 (yellow) | [000] Start, [086]-[116] Step 39c to Completed View |
| NAUO70 | PMG_PianoKey_Aug25-2 | H9, key over button 3 (white) | [000] Start, [086]-[116] Step 39c to Completed View |
| NAUO69 | PMG_PianoKey_Aug25-1 | H9, key over button 4 (blue) | [000] Start, [086]-[116] Step 39c to Completed View |
| NAUO64 | H10-1 | H10, upper deck | [000] Start, [087]-[116] Step 40 to Completed View |
| NAUO62 | H11v2-1 | H11, display bracket (+Z) | [000] Start, [091]-[116] Step 42 to Completed View |
| NAUO77 | H12v2-2 | H12, display bracket (-Z) | [000] Start, [094]-[116] Step 43 to Completed View |
| NAUO75 | H13v2-1 | H13, rear brace | [000] Start, [097]-[116] Step 44 to Completed View |
| NAUO74 | H14-1 | H14, face plate with the display window | [000] Start, [113]-[116] Step 51 to Completed View |

The keys are "PMG_PianoKey_Aug25" in Cadasio and "H9" as the GLB's mesh name; all four are engraved H9.

### 4.3 Routed wire bodies, by pose

Each cell: the GLB body, then its Cadasio twin. [=] identical, [~] same body within 2.5 mm, [name] same name but another route,
[old] the STEP's old wire from the button's VCC pin to G (not V), [mirr] module end on the mirrored matrix pin, [other] a
different body. "-" = the STEP has no body for that wire in that pose.

| Step | Wire | bench | in the case, module on the bench | held above H4 | module mounted, display / matrix on the bench | BUILT |
|---|---|---|---|---|---|---|
| 3 | button 1 VCC -> V4 | NAUO24 Part36 [old] (Part168) | NAUO144 Part53 [old] (Part177) | NAUO146 Part55 [old] (Part55) | | NAUO148 Part57 [old] (Part57) |
| 4 | button 1 OUT -> S4 | NAUO25 Part37 [=] | NAUO145 Part54 [=] | NAUO147 Part56 [name] | | NAUO149 Part58 [name] |
| 5 | button 1 GND -> G4 | - (Part169) | - (Part176) | - (Part189) | | - (Part182) |
| 6 | button 2 VCC -> V5 | NAUO26 Part38 [old] (Part170) | NAUO150 Part59 [old] (Part59) | NAUO155 Part65 [old] (Part65) | | NAUO152 Part61 [old] (Part61) |
| 7 | button 2 OUT -> S5 | NAUO27 Part39 [=] | NAUO151 Part60 [~] | NAUO154 Part66 [name] | | NAUO153 Part62 [name] |
| 8 | button 2 GND -> G5 | - (Part171) | - (Part178) | - (Part188) | | - (Part183) |
| 9 | button 3 VCC -> V6 | NAUO28 Part40 [old] (Part172) | NAUO156 Part63 [old] (Part179) | NAUO160 Part69 [old] (Part69) | | NAUO158 Part67 [old] (Part67) |
| 10 | button 3 OUT -> S6 | NAUO29 Part41 [=] | NAUO157 Part64 [~] | NAUO161 Part70 [name] | | NAUO159 Part68 [name] |
| 11 | button 3 GND -> G6 | - (Part173) | - (Part180) | - (Part187) | | - (Part184) |
| 12 | button 4 VCC -> V7 | NAUO30 Part42 [old] (Part174) | NAUO162 Part71 [old] (Part71) | NAUO166 Part75 [old] (Part75) | | NAUO164 Part73 [old] (Part73) |
| 13 | button 4 OUT -> S7 | NAUO31 Part43 [=] | NAUO163 Part72 [~] | NAUO167 Part76 [name] | | NAUO165 Part74 [name] |
| 14 | button 4 GND -> G7 | - (Part175) | - (Part181) | - (Part186) | | - (Part185) |
| 16 | display CLK -> S8 | NAUO40 Part44 [=] | | NAUO172 Part81 [name] | NAUO168 Part77 [name] | NAUO263 Part138 [name] |
| 17 | display DIO -> S9 | NAUO41 Part45 [=] | | NAUO173 Part82 [name] | NAUO169 Part78 [name] | NAUO264 Part139 [name] |
| 18 | display VCC -> V9 | NAUO42 Part46 [=] | | NAUO174 Part83 [name] | NAUO170 Part79 [name] | NAUO265 Part140 [name] |
| 19 | display GND -> G9 | NAUO43 Part47 [=] | | NAUO175 Part84 [name] | NAUO171 Part80 [name] | NAUO266 Part141 [name] |
| 20 | matrix VCC -> V11 | NAUO55 Part48 [mirr] (V11 to VCC-3) | | NAUO286 Part154 [name mirr] | NAUO291 Part159 [name mirr] | NAUO190 Part100 [name] |
| 21 | matrix GND -> G11 | NAUO56 Part49 [mirr] (G11 to GND-4) | | NAUO287 Part155 [name mirr] | NAUO293 Part160 [name mirr] | NAUO191 Part101 [name] |
| 22 | matrix DIN -> S11 | NAUO57 Part50 [other] (S1 to DIN-5) | | NAUO288 Part156 [name] | NAUO294 Part161 [name] | NAUO192 Part102 [name] |
| 23 | matrix CS -> S12 | NAUO58 Part51 [mirr] (S12 to CS-6) | | NAUO289 Part157 [name mirr] | NAUO295 Part162 [name mirr] | NAUO193 Part103 [name] |
| 24 | matrix CLK -> S13 | NAUO59 Part52 [mirr] (S13 to CLK-7) | | NAUO292 Part158 [name mirr] | NAUO290 Part164 [name mirr] | NAUO194 Part104 [name] |

Where the Cadasio twin has the same name it is not repeated. When each pose is shown: bench from Step Nc to [099] Step 45
(the buttons' only to [075] Step 34, the blue button's to [073] Step 33); buttons in the case with the module on the bench
[074] Step 33c (blue) / [076] Step 34c (the rest) to [099]; held above H4 [100]-[101] Steps 45c-46; module mounted with the
display / matrix on the bench [102]-[103] Steps 46c-47 (display), [102]-[108] Steps 46c-49 (matrix); built buttons from [102]
Step 46c, display from [107] Step 48c, matrix from [112] Step 50c, and on the title page [000].

Poses only Cadasio has: display held above the brackets [104]-[105] (Part190 CLK, 191 DIO, 192 VCC, 193 GND) and half-way [106]
(Part194-197, same order); matrix held [109]-[110] (Part166, one body of 5 sweeps) and half-way [111] (Part203 VCC, 204 GND,
205 DIN, 206 CS, 207 CLK).

Bodies only the STEP has (never shown): display held beside its seat to the mounted module NAUO195-198 (Part105-108: CLK, DIO,
VCC, GND); matrix aside to the mounted module NAUO176-179, 296 (Part85-88, 163: VCC, GND (to G9, a slip), DIN, CS, CLK); matrix
seated to the bench module NAUO180-184 (Part90-94) and to the held module NAUO185-189 (Part95-99); matrix raised to the bench
module NAUO273-276 (Part147 VCC, 148 GND (to S11, a slip), 149 DIN, 151 CLK; no CS body).

### 4.4 Wire caps (the black housings), by the part and pin they sit on

| Part (pose) | GLB caps: pin = NAUO | Cadasio caps the STEP lacks (shown in the guide) |
|---|---|---|
| I/O module, bench (NAUO1) | G4=8, S4=9, G5=10, S5=13, G6=15, S6=12, G7=14, S7=11, S8=38, G9=36, V9=37, S9=39, G11=50, V11=51, S11=54, S12=53, S13=52 | V4 = Wire Cap-160, V5 = 161, V6 = 162, V7 = 163 |
| I/O module, held (NAUO94) | G4=106, S4=107, G5=109, S5=104, G6=105, S6=110, G7=103, S7=108, S8=120, G9=123, V9=122, S9=121, G11=126, V11=125, S11=124, S12=127, S13=128 | V4 = Wire Cap-175, V5 = 174, V6 = 173, V7 = 172 |
| I/O module, mounted (NAUO78) | G4=97, S4=96, G5=95, S5=99, G6=98, S6=100, G7=102, S7=101, S8=111, G9=114, V9=113, S9=112, G11=117, V11=116, S11=115, S12=118, S13=119 | V4 = Wire Cap-179, V5 = 178, V6 = 177, V7 = 176 |
| button 1 black, bench (NAUO7) | VCC=16, OUT=17 | GND = Wire Cap-164 |
| button 2 yellow, bench (NAUO6) | VCC=19, OUT=18 | GND = Wire Cap-165 |
| button 3 white, bench (NAUO5) | VCC=20, OUT=21 | GND = Wire Cap-166 |
| button 4 blue, bench (NAUO4) | VCC=22, OUT=23 | GND = Wire Cap-167 |
| button 1 black, case (NAUO76) | VCC=86, OUT=87 | GND = Wire Cap-168 |
| button 2 yellow, case (NAUO83) | VCC=88, OUT=89 | GND = Wire Cap-169 |
| button 3 white, case (NAUO84) | VCC=90, OUT=91 | GND = Wire Cap-170 |
| button 4 blue, case (NAUO85) | VCC=93, OUT=92 | GND = Wire Cap-171 |
| display, bench (NAUO80) | CLK=32, DIO=33, VCC=34, GND=35 | |
| display, held beside (NAUO129, STEP only) | CLK=130, DIO=132, VCC=131, GND=133 | |
| display, seated (NAUO79) | CLK=259, DIO=260, VCC=261, GND=262 | |
| matrix, bench (NAUO44, turned) | VCC=49, GND=48, DIN=47, CS=46, CLK=45 (pins named by the part; its wires are mirrored) | Cadasio's bench caps Wire Cap-26..30 are elsewhere (other matrix pose) |
| matrix, aside (NAUO82) / raised (NAUO267) | VCC=139/268, GND=140/269, DIN=141/270, CS=142/271, CLK=143/272 | |
| matrix, seated (NAUO81) | VCC=134, GND=135, DIN=136, CS=137, CLK=138 | |
| Display TM1637-6 / -7 (Cadasio only) | - | CLK, DIO, VCC, GND = Wire Cap-180..183 / 184..187 |
| LED Matrix -8 / -9 (Cadasio only) | - | VCC, GND, DIN, CS, CLK = Wire Cap-155..159 / 188..192 |

A cap stays on its pin from pose to pose in the published guide: the bench module's caps are shown until the module is lifted
([099]), the module-end caps of a module until that module moves (e.g. the display's bench caps to [103]), so a wire's two caps
change at different steps. The JSON lists each wire's Cadasio caps per pose (`wires[*].poses[*].cadasio.caps`) and the GLB's.

### 4.5 Loose straight wires (tokens) and the two ribbons

| Step | Token: Cadasio = GLB | Its two caps: Cadasio = GLB | Centre at Step N (mm) | Ribbon |
|---|---|---|---|---|
| 3 | Copy of Copy of Part15-1 = NAUO207 | Wire Cap V2-4, Wire Cap-112 = NAUO206, NAUO202 | [592.0, 894.5, 1278.5] | 12-wire (Step 2) |
| 4 | Copy of Copy of Part16-1 = NAUO208 | Wire Cap V2-3, Wire Cap-111 = NAUO205, NAUO201 | [593.7, 894.5, 1278.5] | 12-wire |
| 5 | Copy of Copy of Part18-1 = NAUO209 | Wire Cap V2-2, Wire Cap-110 = NAUO204, NAUO200 | [595.5, 894.5, 1278.5] | 12-wire |
| 6 | Copy of Copy of Part17-1 = NAUO210 | Wire Cap V2-1, Wire Cap-109 = NAUO203, NAUO199 | [597.2, 894.5, 1278.5] | 12-wire |
| 7 | Copy (2) of Copy of Part15-2 = NAUO219 | Wire Cap V2-8, Wire Cap-116 = NAUO218, NAUO214 | [599.0, 894.4, 1278.5] | 12-wire |
| 8 | Copy (2) of Copy of Part16-2 = NAUO220 | Wire Cap V2-7, Wire Cap-115 = NAUO217, NAUO213 | [600.7, 894.4, 1278.5] | 12-wire |
| 9 | Copy (2) of Copy of Part18-2 = NAUO221 | Wire Cap V2-6, Wire Cap-114 = NAUO216, NAUO212 | [602.5, 894.4, 1278.5] | 12-wire |
| 10 | Copy (2) of Copy of Part17-2 = NAUO222 | Wire Cap V2-5, Wire Cap-113 = NAUO215, NAUO211 | [604.2, 894.4, 1278.5] | 12-wire |
| 11 | Copy (2) of Copy of Part17-3 = not in the STEP | Wire Cap V2-9, Wire Cap-151 = not in the STEP | [606.0, 894.4, 1278.5] | 12-wire |
| 12 | Copy (2) of Copy of Part17-4 = not in the STEP | Wire Cap V2-10, Wire Cap-152 = not in the STEP | [607.7, 894.4, 1278.5] | 12-wire |
| 13 | Copy (2) of Copy of Part17-5 = not in the STEP | Wire Cap V2-11, Wire Cap-153 = not in the STEP | [609.5, 894.3, 1278.5] | 12-wire |
| 14 | Copy (2) of Copy of Part17-6 = not in the STEP | Wire Cap V2-12, Wire Cap-154 = not in the STEP | [611.2, 894.3, 1278.5] | 12-wire |
| 16 | Part133-1 = NAUO255 | Wire Cap-120, Wire Cap-133 = NAUO226, NAUO238 | [591.8, 901.6, 1354.4] | 9-wire (Step 15) |
| 17 | Part132-1 = NAUO253 | Wire Cap-119, Wire Cap-132 = NAUO225, NAUO237 | [593.6, 901.6, 1314.4] | 9-wire |
| 18 | Part134-1 = NAUO254 | Wire Cap-117, Wire Cap-131 = NAUO223, NAUO236 | [595.3, 901.5, 1314.4] | 9-wire |
| 19 | Part130-1 = NAUO252 | Wire Cap-118, Wire Cap-124 = NAUO224, NAUO230 | [597.1, 901.5, 1314.4] | 9-wire |
| 20 | Part129-1 = NAUO251 | Wire Cap-125, Wire Cap-136 = NAUO231, NAUO241 | [598.8, 901.5, 1354.4] | 9-wire |
| 21 | Part128-1 = NAUO250 | Wire Cap-126, Wire Cap-137 = NAUO232, NAUO242 | [600.6, 901.5, 1354.4] | 9-wire |
| 22 | Part127-1 = NAUO249 | Wire Cap-128, Wire Cap-138 = NAUO233, NAUO243 | [602.3, 901.5, 1354.4] | 9-wire |
| 23 | Part126-1 = NAUO248 | Wire Cap-129, Wire Cap-139 = NAUO234, NAUO244 | [604.1, 901.5, 1354.4] | 9-wire |
| 24 | Part125-1 = NAUO247 | Wire Cap-130, Wire Cap-140 = NAUO235, NAUO245 | [605.8, 901.4, 1354.3] | 9-wire |

Parking spot: each loose wire appears at its Step N where it lay in its ribbon. Step 2's ribbon lies at x 592.0-611.2, y 894.4,
z 1278.5, in front of the bench module, the wires 1.75 mm apart, along Z (58.2 mm long); Step 15's at x 591.8-605.8, y 901.5,
z 1354.4 (Steps 16 and 20-24) or 1314.4 (Steps 17-19). In the CAD the ribbons lie further to +X (x 708-731); Cadasio moves them
(first ribbon -116.0 X, -26.5 Z; second -124.8 X, +49.6 Z; the 17-19 tokens -124.8 X, +9.6 Z). At Step 2c / 15c the wires fan out
(the JSON has each one's offset) and each comes back to its ribbon spot for its Step N. On the first ribbon each wire has an 8 mm cap
(Wire Cap) and a 12 mm one (Wire Cap V2, shown with one of its two solids); on the second, two 8 mm caps. The second ribbon has
three spares never shown (Part135-137 = NAUO256-258; caps NAUO227-229, 239, 240, 246).

## 5. The 21 jumper wires

Colour = the colour the wire is shown in most while visible (as `tools/cadasio/atlas.py` counts). The token and every routed
copy of a wire have the same colour, which is how the copies were matched (Part54 is the one exception, shown in the default grey
`#e3e3e3`). Pins were checked from the caps' positions: on the I/O module against its header rows (`_N` = G, `_R` = V, `_B` = S:
`docs/research/mra/cad_pins.md`; rows read from each copy's own headers, D12 / D13 / GND / AREF at the power-jack end), on the
modules against the caps of Steps 3c-24c.

| Step | Wire | Colour | Published labels | Token: Cadasio = GLB | Routed on the bench: Cadasio = GLB | Bench caps (Cadasio; GLB) module end, I/O end |
|---|---|---|---|---|---|---|
| 3 | button 1 (black) VCC -> V4 | `#b70101` dark red | VCC / V4 | Copy of Copy of Part15-1 = NAUO207 | Part168 = none (NAUO24 Part36 goes VCC -> G4) | Wire Cap-10, -160; NAUO16, none |
| 4 | button 1 OUT -> S4 | `#e4e4e4` white | OUT / S4 | Copy of Copy of Part16-1 = NAUO208 | Part37 = NAUO25 | Wire Cap-11, -2; NAUO17, NAUO9 |
| 5 | button 1 GND -> G4 | `#343232` dark grey | GND / G4 | Copy of Copy of Part18-1 = NAUO209 | Part169 = none | Wire Cap-164, -1; none, NAUO8 |
| 6 | button 2 (yellow) VCC -> V5 | `#21f17a` bright green | VCC / V5 | Copy of Copy of Part17-1 = NAUO210 | Part170 = none (NAUO26 Part38: VCC -> G5) | Wire Cap-13, -161; NAUO19, none |
| 7 | button 2 OUT -> S5 | `#7c5a30` brown | S5 / OUT | Copy (2) of Copy of Part15-2 = NAUO219 | Part39 = NAUO27 | Wire Cap-12, -6; NAUO18, NAUO13 |
| 8 | button 2 GND -> G5 | `#ffdc00` yellow | GND / G5 | Copy (2) of Copy of Part16-2 = NAUO220 | Part171 = none | Wire Cap-165, -3; none, NAUO10 |
| 9 | button 3 (white) VCC -> V6 | `#85144b` maroon | V6 / VCC | Copy (2) of Copy of Part18-2 = NAUO221 | Part172 = none (NAUO28 Part40: VCC -> G6) | Wire Cap-14, -162; NAUO20, none |
| 10 | button 3 OUT -> S6 | `#737980` grey | S5 / OUT (slip: the pin is S6) | Copy (2) of Copy of Part17-2 = NAUO222 | Part41 = NAUO29 | Wire Cap-15, -5; NAUO21, NAUO12 |
| 11 | button 3 GND -> G6 | `#3876ac` blue | GND / G6 | Copy (2) of Copy of Part17-3 = none | Part173 = none | Wire Cap-166, -8; none, NAUO15 |
| 12 | button 4 (blue) VCC -> V7 | `#a75294` orchid | VCC / V7 | Copy (2) of Copy of Part17-4 = none | Part174 = none (NAUO30 Part42: VCC -> G7) | Wire Cap-16, -163; NAUO22, none |
| 13 | button 4 OUT -> S7 | `#ff4136` red-orange | S7 / OUT | Copy (2) of Copy of Part17-5 = none | Part43 = NAUO31 | Wire Cap-17, -4; NAUO23, NAUO11 |
| 14 | button 4 GND -> G7 | `#3d9970` teal-green | GND / G7 | Copy (2) of Copy of Part17-6 = none | Part175 = none | Wire Cap-167, -7; none, NAUO14 |
| 16 | display CLK -> S8 | `#ac9400` gold | clk / s8 (lower case) | Part133 = NAUO255 | Part44 = NAUO40 | Wire Cap-18, -24; NAUO32, NAUO38 |
| 17 | display DIO -> S9 | `#000000` black | dio / s9 (lower case) | Part132 = NAUO253 | Part45 = NAUO41 | Wire Cap-19, -25; NAUO33, NAUO39 |
| 18 | display VCC -> V9 | `#ab53ca` violet | VCC / V9 | Part134 = NAUO254 | Part46 = NAUO42 | Wire Cap-20, -23; NAUO34, NAUO37 |
| 19 | display GND -> G9 | `#bb3d3d` red | GND / G9 | Part130 = NAUO252 | Part47 = NAUO43 | Wire Cap-21, -22; NAUO35, NAUO36 |
| 20 | matrix VCC -> V11 | `#411900` dark brown | V11 / VCC | Part129 = NAUO251 | V11 to VCC-3 = NAUO55 Part48 (mirrored: to CLK) | Wire Cap-30, -32; NAUO45 (CLK), NAUO51 |
| 21 | matrix GND -> G11 | `#339f3f` green | G11 / GND | Part128 = NAUO250 | G11 to GND-4 = NAUO56 Part49 (mirrored: to CS) | Wire Cap-29, -31; NAUO46 (CS), NAUO50 |
| 22 | matrix DIN -> S11 | `#2a2f62` navy | S11 / DIN | Part127 = NAUO249 | S1 to DIN-5 = NAUO57 Part50 (other route) | Wire Cap-28, -35; NAUO47, NAUO54 |
| 23 | matrix CS -> S12 | `#662639` wine | S12 / CS | Part126 = NAUO248 | S12 to CS-6 = NAUO58 Part51 (mirrored: to GND) | Wire Cap-27, -34; NAUO48 (GND), NAUO53 |
| 24 | matrix CLK -> S13 | `#377e89` teal | S13 / CLK | Part125 = NAUO247 | S13 to CLK-7 = NAUO59 Part52 (mirrored: to VCC) | Wire Cap-26, -33; NAUO49 (VCC), NAUO52 |

Every other pose of each wire, Cadasio and GLB, with its caps: table 4.3 and `cadasio_map.json` -> `wires[*].poses`.
The colour follows the ribbon position, not the signal (GND is red on the display, VCC dark brown on the matrix), as the
earlier study noted.

Module pins (the same in both projects, in the module's own frame): push button VCC, OUT, GND 2.5 mm apart (black bench button
NAUO7: caps at z 1273.3, 1275.8, 1278.3); display CLK, DIO, VCC, GND 2.4 mm apart (bench display NAUO80: caps at y 928.8,
926.4, 924.0, 921.6); matrix input header VCC, GND, DIN, CS, CLK 2.5 mm apart (the published bench matrix: y 929.6 down to
919.4). I/O module, bench (NAUO1): pin tops at y 887.97; G column x 653.64, V 656.12, S 658.60; D4 z 1290.77, then +2.54 per row
within a block of four, blocks 12.55 mm apart (D8 1303.32, D12 1315.87); all pin positions of all six module copies are in the
JSON (`shield_pins_world`).

## 6. Names

Cadasio has no tooltips (every part's tooltip is "Description" / "none"), so the only names are the CAD component names and the
five section cards: "Nano I/O Module", "Push Buttons", "4-Digit Display", "Dot Matrix Display", "USB Cable" (and the photo caption
"NANO I/O MODULE LABELS").

| CAD / Cadasio name | What it is | Proposed name (as the MRA / RCC NAMES) | Hover name |
|---|---|---|---|
| Ensamblaje_Shield_NANO | the I/O expansion board | Nano I/O Module | |
| nano (and the shield's own "arduino nano") | Arduino Nano | Nano Board | |
| Big Button Module (x4) | push-button module, pins VCC / OUT / GND | Push Button | Black / Yellow / White / Blue Push Button |
| Display TM1637 | TM1637 4-digit 7-segment display | 4-Digit Display | |
| LED Matrix 32x8 - 4 Modules 8x8 with MAX7219 | 32 x 8 LED dot matrix (four 8 x 8 on MAX7219) | Dot Matrix Display | |
| USB Right Angle + USB Cable end + lead (Copy of Part23, Part152, Part153) | USB cable, right-angle Mini-B to A | USB Cable | listed by its Mini-B end, as the MRA's |
| Wire Cap, Wire Cap V2 + the wire bodies | female-female jumper wire | Breadboard Wire (F-F), the MRA's name | e.g. "Breadboard Wire (F-F)" |
| H1 ... H14 (H4v2, H11v2, H12v2, H13v2) | laser-cut wood | H1 ... H14 (engraved codes) | |
| PMG_PianoKey_Aug25 (GLB mesh "H9") x4 | piano keys | H9 (x4) | |

## 7. Colours (`colour-atlas-pmg-draft.json`)

Written by `tools/cadasio/atlas.py` for: the eight push buttons (Big Button Module-1..5, -9..11), Display TM1637-4 and -2, LED
Matrix -1 and -4, USB Cable end-1, USB Right Angle-1, the bench USB lead (Copy of Part23-1), Wire Cap-1, -10, -112, Wire Cap V2-4,
every wood part (H1-1 ... H14-1, PMG_PianoKey_Aug25-4), and for reference Ensamblaje_Shield_NANO-1 and nano-3. Each entry lists the
solids with their box in the part's own frame and the colour shown.

- **Push button** (11 solids each): board `#000f41` navy, switch body `#1e1e1e`, socket pin holes `#1a1a1a` (x4), socket
  chamfers `#c6c1bc` (x4), cap `#000000` black (Big Button Module-4 bench / -5 case), `#ffdc00` yellow (-3 / -9), `#ffffff`
  white (-2 / -10), `#0074d9` blue (-1 / -11).
- **4-digit display** (41 solids): PCB `#224bbe`, display face `#000000` (2), segments `#ffffff` (30), pins `#e3e3e3` (4) and
  `#cccccc` (4).
- **Dot matrix** (500 solids): PCB `#234bbf`; the 8 x 8 modules ("1088AS") `#e4e4e4` (344) with `#a3aaad`, `#ffffff`, `#1a1a1a`
  (4 each); MAX7219 chips `#232323` (4); female headers `#e4e4e4` (128); 5-pin input header `#0a0a0a`, its pins `#e4e4e4` (10).
- **USB cable**: plug and A-end bodies `#1e1616`; metal shells `#e4e4e4` and `#a6a9aa`; lead `#1e1616`.
- **Wire caps**: housing `#000000`; the 12 mm cap's second solid (its pin) `#e4e4e4`.
- **Wood**: `#deb887`; engraved code `#1e1616` (2 or 3 solids laid on the face; H14 has 4 tan and 3 dark solids).
- I/O module and Nano: the MRA's colours are to be used; the atlas lists Cadasio's for reference (Cadasio's Nano PCB `#000f41`).
- Wires: the colour column of section 5. Some dark ones are hard to tell apart (`#000000`, `#411900`, `#662639`, `#343232`:
  rulebook Appendix B).

## 8. Cameras

Direction = unit vector from the target to the eye, GLB frame. Up = the camera's up vector, from Cadasio's camera rotation
(Y- on the turned-over run [065]-[080], where the scene's up axis is -y). Field of view 45 deg, perspective, throughout. The JSON
also gives the eye point.

| Viewer steps | Direction | Target (mm) | Distance (mm) | Elev / azim (deg) | Up |
|---|---|---|---|---|---|
| [000] Start | [-0.64, 0.357, 0.68] | [449.8, 919.1, 1210.4] | 320.4 | 20.9 / -43.3 | [0.25, 0.93, -0.26] (+y) |
| [001] Nano I/O Module | [0.003, 1.0, -0.0] | [679.1, 884.3, 1260.6] | 133.2 | 89.8 / 90.0 | [-1.0, 0.0, 0.0] (+y) |
| [002] Step 1 to [003] Step 1c | [-0.778, 0.556, 0.291] | [680.9, 883.6, 1302.3] | 142.5 | 33.8 / -69.5 | [0.52, 0.83, -0.19] (+y) |
| [004] Step 2 to [005] Step 2c | [-0.394, 0.76, 0.517] | [599.6, 890.6, 1284.1] | 128.2 | 49.5 / -37.3 | [0.46, 0.65, -0.6] (+y) |
| [006] Push Buttons | [-0.952, 0.295, 0.086] | [620.1, 954.3, 1282.8] | 43.3 | 17.1 / -84.8 | [0.29, 0.96, -0.03] (+y) |
| [007] Step 3 to [033] Step 14c | [-0.824, 0.363, 0.435] | [614.5, 929.2, 1306.6] | 173.1 | 21.3 / -62.1 | [0.32, 0.93, -0.17] (+y) |
| [034] 4-Digit Display | [-0.948, 0.2, 0.248] | [659.2, 922.2, 1246.9] | 91.1 | 11.5 / -75.3 | [0.19, 0.98, -0.05] (+y) |
| [035] Step 15 to [036] Step 15c | [-0.528, 0.753, 0.393] | [595.2, 895.2, 1359.2] | 103.4 | 48.9 / -53.3 | [0.6, 0.66, -0.45] (+y) |
| [037] Step 16 to [044] Step 19c | [-0.86, 0.426, 0.281] | [614.5, 929.2, 1306.6] | 173.1 | 25.2 / -71.9 | [0.4, 0.9, -0.13] (+y) |
| [045] Dot Matrix Display | [-0.976, 0.203, -0.079] | [659.2, 936.8, 1381.4] | 235.5 | 11.7 / -94.6 | [0.2, 0.98, 0.02] (+y) |
| [046] Step 20 to [055] Step 24c | [-0.856, 0.499, 0.137] | [614.3, 908.6, 1361.1] | 201.9 | 29.9 / -80.9 | [0.49, 0.87, -0.08] (+y) |
| [056] USB Cable | [0.577, 0.61, 0.543] | [611.1, 858.6, 1364.7] | 201.9 | 37.6 / 46.7 | [-0.44, 0.79, -0.42] (+y) |
| [057] Step 25 to [058] Step 25c | [0.922, 0.387, 0.005] | [628.9, 859.8, 1344.3] | 274.7 | 22.8 / 89.7 | [-0.39, 0.92, -0.0] (+y) |
| [059] Step 26 to [060] Step 26c | [-0.619, 0.595, 0.513] | [546.6, 870.7, 1304.0] | 274.7 | 36.5 / -50.3 | [0.46, 0.8, -0.38] (+y) |
| [061] Step 27 to [062] Step 27c | [-0.526, 0.646, -0.553] | [532.2, 866.6, 1291.3] | 274.7 | 40.2 / -136.5 | [0.45, 0.76, 0.47] (+y) |
| [063] Step 28 to [064] Step 28c | [0.454, 0.592, 0.666] | [538.0, 848.7, 1264.8] | 373.7 | 36.3 / 34.3 | [-0.33, 0.81, -0.49] (+y) |
| [065] Step 29 to [066] Step 29c | [-0.557, -0.56, 0.613] | [507.1, 893.7, 1250.6] | 373.7 | -34.1 / -42.3 | [0.38, -0.83, -0.41] (-y) |
| [067] Step 30 to [068] Step 30c | [-0.51, -0.707, -0.49] | [514.8, 896.4, 1260.0] | 274.7 | -45.0 / -133.8 | [0.51, -0.71, 0.49] (-y) |
| [069] Step 31 to [070] Step 31c | [-0.613, -0.468, 0.636] | [513.0, 901.5, 1254.5] | 320.4 | -27.9 / -43.9 | [0.32, -0.88, -0.34] (-y) |
| [071] Step 32 to [072] Step 32c | [-0.805, -0.388, -0.45] | [527.1, 914.0, 1277.2] | 235.5 | -22.8 / -119.2 | [0.34, -0.92, 0.19] (-y) |
| [073] Step 33 to [076] Step 34c | [0.018, -0.636, -0.771] | [575.8, 882.4, 1253.4] | 274.7 | -39.5 / 178.7 | [-0.01, -0.77, 0.64] (-y) |
| [077] Step 35 to [078] Step 35c | [-0.69, -0.411, 0.596] | [522.4, 906.0, 1232.6] | 320.4 | -24.3 / -49.2 | [0.31, -0.91, -0.27] (-y) |
| [079] Step 36 to [080] Step 36c | [-0.402, -0.571, -0.716] | [541.3, 925.8, 1284.5] | 320.4 | -34.8 / -150.7 | [0.28, -0.82, 0.5] (-y) |
| [081] Step 37 to [082] Step 37c | [-0.57, 0.499, 0.653] | [530.9, 915.4, 1283.4] | 320.4 | 30.0 / -41.1 | [0.33, 0.87, -0.38] (+y) |
| [083] Step 38 to [086] Step 39c | [-0.304, 0.585, 0.752] | [511.4, 888.4, 1296.6] | 274.7 | 35.8 / -22.0 | [0.22, 0.81, -0.54] (+y) |
| [087] Step 40 to [088] Step 40c | [0.538, 0.436, 0.721] | [551.7, 903.7, 1298.2] | 274.7 | 25.8 / 36.7 | [-0.26, 0.9, -0.35] (+y) |
| [089] Step 41 to [090] Step 41c | [-0.468, 0.226, 0.854] | [550.7, 912.7, 1293.5] | 274.7 | 13.1 / -28.7 | [0.11, 0.97, -0.2] (+y) |
| [091] Step 42 to [093] Step 42c | [-0.159, 0.649, 0.744] | [576.7, 944.8, 1284.1] | 274.7 | 40.5 / -12.0 | [0.14, 0.76, -0.63] (+y) |
| [094] Step 43 to [096] Step 43c | [-0.182, 0.606, -0.775] | [553.1, 959.8, 1293.9] | 235.5 | 37.3 / -166.8 | [0.14, 0.8, 0.59] (+y) |
| [097] Step 44 to [098] Step 44c | [0.581, 0.649, -0.491] | [541.2, 962.4, 1293.4] | 274.7 | 40.5 / 130.2 | [-0.5, 0.76, 0.42] (+y) |
| [099] Step 45 to [100] Step 45c | [0.628, 0.468, -0.622] | [600.0, 939.1, 1305.0] | 373.7 | 27.9 / 134.7 | [-0.33, 0.88, 0.33] (+y) |
| [101] Step 46 to [102] Step 46c | [0.616, 0.491, 0.616] | [584.5, 926.3, 1328.5] | 435.8 | 29.4 / 45.0 | [-0.35, 0.87, -0.35] (+y) |
| [103] Step 47 to [104] Step 47c | [0.759, 0.651, 0.014] | [601.1, 915.1, 1303.1] | 320.4 | 40.6 / 88.9 | [-0.65, 0.76, -0.01] (+y) |
| [105] Step 48 to [107] Step 48c | [-0.347, 0.563, 0.75] | [566.6, 952.3, 1284.8] | 235.5 | 34.3 / -24.8 | [0.24, 0.83, -0.51] (+y) |
| [108] Step 49 to [109] Step 49c | [-0.733, 0.611, 0.298] | [554.0, 909.7, 1331.1] | 320.4 | 37.6 / -67.9 | [0.57, 0.79, -0.23] (+y) |
| [110] Step 50 to [112] Step 50c | [-0.053, 0.248, -0.967] | [541.9, 914.1, 1298.9] | 274.7 | 14.4 / -176.9 | [0.01, 0.97, 0.25] (+y) |
| [113] Step 51 to [115] Step 51c | [-0.108, 0.582, -0.806] | [552.0, 927.2, 1302.4] | 373.7 | 35.6 / -172.4 | [0.08, 0.81, 0.58] (+y) |
| [116] Completed View | [-0.716, 0.574, 0.398] | [545.4, 912.0, 1312.5] | 320.4 | 35.0 / -60.9 | [0.5, 0.82, -0.28] (+y) |

(Elevation = angle of the direction above the XZ plane; azimuth = atan2(x, z) of the direction, as the digest gives them.)
Camera targets on the bench steps aim at the published poses; where the STEP's parts sit elsewhere (the bench matrix, the turned
module) a reused camera would need re-aiming.

## 9. How the rigid parts move in the guide (world offsets from the CAD pose, mm)

From the replay (`cadasio_components[*].moves`). "Then" = the next leg.

- Nano Board (nano-3): Step 1 +29.8 Y; seated at Step 1c.
- The bench USB cable (plug, A end and lead together): card [056] and Step 25 +22.9 Z (out of the Nano's socket along +Z);
  seated at Step 25c.
- H2 Step 26 +40.0 X; H3 Step 27 +43.2 X; H4 Step 28 +65.0 X; H8 Step 37 +94.5 Y; first key (NAUO72) Step 38 -107.7 X;
  H13 Step 44 (-61.3, 51.5, 0).
- Two-leg seats (their solids are turned as well; the turns were not resolved here): H5 Step 29 (0.6, -101.5, -95.9), then
  (-0.2, -54.5, 11.4); H6 Step 31 (1.0, -80.4, -109.5), then (-0.1, -42.3, 6.8); H7 Step 35 (2.1, -28.9, -136.3), then
  (0, -0.6, 0.1); H10 Step 40 (-124.7, 26.1, 0), then (0.2, 8.9, 0); H11 Step 42 (-6.7, 53.1, 0), then (-6.7, 0, 0) at the
  Transition, seated at 42c; H12 Step 43 (-7.6, 44.5, 0), then (-7.6, 0, 0); H14 Step 51 (29.8, 49.3, 0.7), then hand-set turns.
- Everything else changes pose by cross-fading to another copy (each wire at its Step Nc, the buttons at 33c / 34c, the module
  cluster at 45c / 46c, the display at 47c / [106] / 48c, the matrix at 49c / [111] / 50c), as the earlier study found.

## 10. What could not be verified

- That the STEP is the older state is inferred (part numbering, the fixes); only TechBox's engineer can confirm.
- Which way up the module really goes on the back panel (published: USB end up; STEP: down). H4 is the same in both; I did not
  look for a USB opening in H4.
- H14's final pose in the published guide (section 3), and the turns of the two-leg hover poses (section 9).
- Wire bodies were compared by bounding box only ("same name, other route" = boxes differ by more than 2.5 mm). Their centre
  lines are `cad_wire_paths.md`'s job.
- The Cadasio payload names a Draco mesh file for every solid (`versionDracoData`, e.g. "8d9022db-...drc"); the published shapes of
  the wires the STEP lacks could probably be fetched from Cadasio. Not tried (it means downloading files).
