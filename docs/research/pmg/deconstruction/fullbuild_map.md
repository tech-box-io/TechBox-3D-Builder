# PMG Full Build, step by step: a map for the deconstruction

Read from `PMG Build Instructions/guide.py` (1244 lines) and `PMG Build Instructions/steps.json` (model `model.glb?v=7e6f1622374f`,
99 views, 250 routes, 22 wires, 69 named parts), 21 Oct 2026. Nothing was regenerated. For the deconstruction script
(`deconstruction.py`, `g.take_apart()`), which reads this steps.json.

**Count:** the Full Build has **48 steps**, not 51 (51 is the published Cadasio guide's count). 99 views = Start + 2 Parts List
cards + Step 3 (single, no 3c) + 47 x (Step N, Step Nc) + Completed View. Step names below are the player's (steps.json).

Pose notation: `T[x,y,z]` a shift from the seat; `R[axis]@deg t[...]` a turn (about the part's middle, `at`) then a shift. Ids are
CAD instance ids. "by H1" = rides on H1 (`NAUO63`, the datum, never moves), so its riding pose is also its world pose.

---------------------------------------------------------------------------------------------------------------------------------

## 1. Every step

### 1a. Non-step views and the put_away / cut points

| View | guide.py | What |
|---|---|---|
| Start | 1240 (`g.start_view`) | every part seated; camera dir [-0.7723, 0.4726, 0.4246], target [522.7, 912.3, 1235.3], r 113.6, shift 0 (Lee's screenshot, 21 Oct) |
| Parts List, Parts List (Cont.) | 115 (`parts_list`, 69-96) | Electronics band (Nano I/O Module, Nano Board, Push Button x4, 4-Digit Display, Dot Matrix Display, Breadboard Wire (F-F) x21, USB Cable); Case band H1 - H14. Camera dir [-0.5997, 0.5299, 0.5997], target [574.4, 947.3, 1289.1], r 151.2 |
| put_away after Step 2 | 466 (in `peel`) | the 24 caps of the 12 button wires leave the screen; Step 3 has `cut: true` |
| put_away after Step 16 | 466 (peel, called 567) | the 18 caps of the 9 display / matrix wires leave; Step 17 `cut: true` (its CLK caps come straight back) |
| put_away after Step 26 | 618-619 `ELECTRONICS` | module, Nano, USB_B, USB_A, display, matrix, 4 buttons, 42 caps all leave; the case is built alone; Step 27 `cut: true` |
| carry re-declarations before Step 32 | 679-692 | buttons, module, display, matrix, USB_A ride **on H1** at their bench poses; NANO, USB_B on the module; each wire's device cap on its **device**, module cap on the module (`ON_THE_BENCH` routes) |
| Completed View | 1241 (`g.end_view`) | every part seated (all 45 offsets are zero), no `hide`/`poses`; camera dir [-0.8363, 0.459, 0.2999], target [546.0, 915.1, 1274.2], r 113.6 |

### 1b. The electronics on the bench (Steps 1 - 26): the case is not on screen

Everything here is done by **riding** (`ride=` / `g.carry`), not by `move=`: `moving` is empty in every one of these views, and
the module (`NAUO78`) lies still at `MODULE_BENCH` (`rest_at`, line 424). On the bench **every jumper cap, at both ends, rides on
the module** (`HUB` poses, line 205), not on its device; the devices are `rest_at` their bench places (lines 472, 569, 570).

| Step | guide.py | Caption (short) | Moves / appears | Riding (carry) and way | Camera dir / target / r | Wires (route ids, hover -> done; via) | Labels, eye, lines, inset, caution | Flags |
|---|---|---|---|---|---|---|---|---|
| 1 | 435 (rest_at 424, carry 426) | Press the Nano Board into the I/O module | appears NAUO78 module, NANO | NANO by module `T[35,0,0]` (module frame; world +y) -> `ZERO` | [-0.5792, 0.5736, -0.5792] / [673.6, 906.9, 1299.3] / 49.7 | none | labels Nano Board, Nano I/O Module (anchor `MODULE_SPOT`); 4 lead lines (`lines_at`, NANO_LINES 431) | |
| 2 | 469 (`peel` 457) | Peel twelve wires off the ribbon | appears 24 button caps | caps by module (ribbon poses) -> split poses | [-0.5792, 0.5736, -0.5792] / [619.0, 878.0, 1289.9] / 49.3 (`focus=caps`) | 12 button wires: 0-11 -> 12-23 | eye on the ribbon; no lines, no labels | put_away after |
| 3 | 485 | Find the four push buttons (VCC, OUT, GND) | appears NAUO76 black button (at `BUTTON_BENCH[0]`) | none | [-0.9685, 0.0581, 0.2421] / [641.5, 948.6, 1275.8] / 24.0 | none | inset on the printed pin names (target [645.35, 944.35, 1275.78], r 8.5, mark 6.9) | `single=True` (no Step 3c), `one_off_camera`, `cut` |
| 4 - 15 | loop 555-563 -> `wire_step` 509 -> `plug_on` 335 | Connect VCC / OUT / GND on the <colour> push button to V/S/G 4 - 7 | each step: the wire's 2 caps; Step 7 NAUO83 yellow, 10 NAUO84 white, 13 NAUO85 blue appear | both caps by module: loose pose -> 1 via (held 12 mm off the pins, `HELD_MM`) -> plugged (device cap `HUB(a, pa)`, module cap `ZERO`) | `BUTTON_RUN` (494): [-0.7228, 0.4352, 0.5368] / [645, 911, 1295] / 58 | loose -> held (via) -> bench: see section 3 (e.g. black VCC 24 -> via 25 -> 26) | labels: device pin (side right from yellow on), module pin (up-right), and the button's name on its cap (`name_on_cap`, first wire of each); eye on the loose wire at [618, 877.98, 1290] (`PARK_X`) | review note on Step 4 (`THREE_WIRES`, 551) |
| 16 | 567 | Peel nine more wires | appears 18 display / matrix caps | caps by module, ribbon -> split | [-0.4962, 0.8124, 0.3062] / [640, 884, 1292] / 62 | 9 wires: 59-67 -> 68-76 | eye | put_away after |
| 17 - 20 | loop 571-581 | Connect CLK / DIO / VCC / GND on the 4-digit display to S8 / S9 / V9 / G9 | Step 17: NAUO79 display appears (at `DISPLAY_BENCH`) + 2 caps; others 2 caps | caps by module: loose (x 712, z 1262) -> 3 vias (lifted, over, held 30 mm along the pin) -> plugged | 17-18 `DISPLAY_RUN` (496): [0.5068, 0.7658, -0.3959] / [672, 902, 1264] / 58; 19-20 `DISPLAY_PINS_RUN` (498): [0.4589, 0.5, 0.7344] / [672, 911, 1262] / 74 | e.g. CLK 77 -> via 78, 79, 80 -> 81 | pin labels; "4-Digit Display" label (17); eye near-below; inset on Step Nc (module pin from above; `side='left'` on 19c, 20c) | `ride_beats` (a beat per stage) |
| 21 - 25 | loop 595-604 | Connect VCC / GND / DIN / CS / CLK on the dot matrix display to V11 / G11 / S11 / S12 / S13 | Step 21: NAUO81 matrix appears (at `MATRIX_BENCH`) + 2 caps | caps by module: loose (x 680, z 1356, along x) -> 2 vias (gathered in the gap z 1338, held) -> plugged | `MATRIX_RUN` (505): [0.4741, 0.8292, 0.2961] / [672, 898, 1338] / 54 | e.g. VCC 97 -> via 98, 99 -> 100 | `MATRIX_LABELS` (586); "Dot Matrix Display" label (21); eye near-right; inset on Nc `side='right'`, dir [-0.4015, 0.9034, 0.1506] | `ride_beats` |
| 26 | 612 (carry 608, rest_at 609) | Connect the USB cable to the Nano Board | appears NAUO282 USB_B, NAUO283 USB_A | USB_B by module `T[0,25,0]` (`USB_HOVER`) -> `ZERO`; USB_A `rest_at USB_A_BENCH` | [0.922, 0.3871, 0.0054] / [668, 898, 1325] / 70 | usb cable 117 -> 118 | label USB Cable; 1 lead line (plug tip -> socket mouth); caution "Set the I/O module ... aside for now" | put_away after |

### 1c. The case (Steps 27 - 41), and the buttons into it (32 - 33)

| Step | guide.py | Caption (short) | Moves (id) | Way in (path / hover) | Camera dir / target / r | Wires | Labels, eye, lines | Flags |
|---|---|---|---|---|---|---|---|---|
| 27 | 624 | Begin with H1; push H2's front tabs into H1 | H2 `NAUO65`; H1 `NAUO63` shown (`show=`, never moves) | `direction=[1,0,0]`, hover 40: `T[40,0,0] -> 0` | [-0.5792, 0.5736, 0.5792] / [545.4, 912.7, 1290.5] / 117.2 | none (electronics put away) | H1 (near-above), H2; 1 lead line | `cut` |
| 28 | 627 | Push H3 onto the other end of H1 | H3 `NAUO66` | `T[43,0,0] -> 0` | [-0.5792, 0.5736, -0.5792] / [546.9, 912.7, 1290.5] / 118.4 | | H3; 1 line | |
| 29 | 628 | Push H4 onto the back tabs of H2 and H3 | H4 `NAUO73` | `T[65,0,0] -> 0` | [0.5792, 0.5736, 0.5792] / [556.2, 928.2, 1290.5] / 129.6 | | H4; 4 lines | |
| 30 | 670 | Turn the case over; H5 into H2's windows, swing into H3's notches | H5 `NAUO67` | `hinged` (634), 5 poses: `R[1,0,0]@-8` about [532.3, 903.39, 1357.17] with t [0,-60,-5], [0,-18,-5], [0,0,-5], 0; then seat | `FLOOR_CAMERA` (643): [-0.8, -0.5657, -0.2] / [529, 882, 1290] / 118 | | H5; 4 lines (Lee's points) | **flip** (pivot [529, 882, 1290], flip_axis [-0.9701, 0, -0.2425]); `one_off_camera` |
| 31 | 673 | Lay H6 on H5 the same way | H6 `NAUO60` | `hinged`, hinge [518.2, 900.39, 1357.17] | FLOOR_CAMERA | | H6; 4 lines | flip; one_off_camera |
| 32 | 793 | Bring the electronics back beside the case; blue button into the pocket farthest from H3 | blue button `NAUO85` moves; appear module, display, matrix, USB_A, 3 other buttons, 42 caps (NANO, USB_B by carry) | `button_way(3)` (779), 5 poses: `BUTTON_BENCH[3]` (R[0.7496,-0.6619,-0.0044]@179.94 t[135.39, 44.66, -21.64]) -> t[109.39, 44.66, -21.64] (26 mm clear) -> t[109.39, -65.34, -21.64] (lifted 110 mm; up on screen, the case is turned over) -> `T[0,-70,0]` (over its pocket) -> seat | `BUTTONS_IN` (792): [0.0175, -0.6364, -0.7712] / [582, 905, 1300] / 108 | Step 32 shows the bench routes (26-58, 81-116, usb 118); 32c: blue VCC/OUT/GND 52/55/58 -> 119/120/121 (`first_button_layout`, 767) | label "Blue Push Button"; no lines | flip; the view comes after a put_away, so nothing glides over |
| 33 | 801 | The other three buttons the same way: white, yellow, black nearest H3 | NAUO76 black, NAUO83 yellow, NAUO84 white | own `paths=` each (`button_way(k, clear=(-26, 0, -8))`), 5 poses, from `BUTTON_BENCH[k]` | BUTTONS_IN | 33c: all 12 button wires -> 122-133 (`case_bench_layout`, 751) | eye on NAUO76; `labels_done` on 33c: Blue, White, Yellow, Black (side left) | flip; `paths` |
| 34 | 805 | Lay H7 on H6, over the buttons | H7 `NAUO68` | `hinged`, hinge [518.1, 897.39, 1357.17] | FLOOR_CAMERA | | H7; 4 lines | flip; one_off_camera |
| 35 | 811 | Turn the case the right way up; H8 down into H5 | H8 `NAUO61` | `direction=[0,1,0]`, hover 94.5 | [-0.5792, 0.5736, -0.5792] / [529, 960, 1290.5] / 108 | | H8; 4 lines | upright again |
| 36 | 815 | Slide a piano key, H9, in through H8 into H4 | key `NAUO72` (over the black button) | `direction=[-1,0,0]`, hover 108: `T[-108,0,0]` | `KEY_CAMERA` (813): [-0.5792, 0.5736, -0.5792] / [484, 930, 1290.5] / 130 | | H9; 2 lines | |
| 37 | 817 | The other three keys | `NAUO71`, `NAUO70`, `NAUO69` (one path) | `T[-108,0,0]` | KEY_CAMERA | | "3x H9" on NAUO71; 3 lines (one per key) | 3 movers, one path |
| 38 | 827 | H10: rear tabs into H4, lower its front | H10 `NAUO64` | `h10` tilt `R[0,0,1]@-8` about [588.86, 931.08, 1290.5]: t[-124, 26, 0], via t[-14, 0, 0], t 0, then seat | KEY_CAMERA | | H10; 2 lines (`spots`) | `stops: [0, 2, 3]` |
| 39 | 831 | H11 down into H10, slide back into H4 | H11 `NAUO62` | `T[-6.7, 53.1, 0] -> T[-6.7, 0, 0] -> 0` | [-0.5792, 0.5736, 0.5792] / [556, 982, 1302] / 72 | | H11; 2 lines | |
| 40 | 834 | Fit H12 the same way | H12 `NAUO77` | `T[-7.6, 44.5, 0] -> T[-7.6, 0, 0] -> 0` | [-0.5792, 0.5736, -0.5792] / [556, 978, 1278] / 72 | | H12; 2 lines | |
| 41 | 837 | H13 down between H11 and H12 into H4 | H13 `NAUO75` | `direction=H13_UP` [-0.766, 0.643, 0], hover 80: `T[-61.3, 51.4, 0]` | [0.5792, 0.5736, -0.5792] / [555, 995, 1290] / 102 | | H13; 2 lines | |

### 1d. The electronics into the case (Steps 42 - 47) and H14 (48)

| Step | guide.py | Caption (short) | Moves | Way / riding | Camera dir / target / r | Wires (hover -> done; via) | Labels, eye, arrows, inset | Flags |
|---|---|---|---|---|---|---|---|---|
| 42 | 1162 (ways 1088-1161) | Pick up the I/O module, hold it over the back of H4, USB end up; lay the USB A end on the table behind the case | module (and all it carries) and USB_A, **by ride, `moving` empty** | module by H1: `MODULE_BENCH` (R[0.57735 x3]@120 t[72.85, -48.14, 8.78]) -> `MODULE_HELD` `T[0, 102.3, 0.2]` (straight over its seat); USB_A by H1: `USB_A_BENCH` (R[0.7071, 0, 0.7071]@180 t[-70.38, -10.69, 152.93]) -> `ZERO` (its seat, on the table behind the case) | [0.8387, 0.5446, 0.0] / [638, 1012, 1323] / 126 | hover: all 22 -> 134-155 (the 41c shapes re-issued with `tail_from` / `b_whole` / `b_from`); done: 156-177 (module held) | eye on the module; no labels | **`reappear: true`** (fade out on the bench, fade in held: `STEP42_REAPPEAR = True`, 1158; Lee: keep the fade on 42, this step only); **review note** (module USB end up vs the STEP's down) |
| 43 | 1175 | Lower the module onto the back of H4, edges into H10's notches | module `NAUO78` (moving) | `path=[MODULE_HELD, ZERO]`: `T[0, 102.3, 0.2] -> 0` | [0.6161, 0.4908, 0.6161] / [600, 985, 1290] / 100 | 43c: all 22 -> 178-199 (`mounted_layout` 894, `held_in_case=True`: button wires carry `b_from` ~82 mm; display / matrix wires to their bench places; usb 199 seated) | label Nano I/O Module (near-left); hand arrow tail [600.73, 1034.83, 1326.21] head [600.73, 934.83, 1326.21] normal [0.7071, 0, 0.7071] | |
| 44 | 1188 | Pick up the 4-digit display, under the dot matrix's wires, up behind the case, over the top; hold over the gap between H11 and H12 | display `NAUO79`, **by ride** | by H1: `DISPLAY_BENCH` (R z@40 t[97.47, -55.99, -73.17]) -> via `DISPLAY_UNDER` (R z@40 t[80.47, -61.99, 10.83]) -> via `DISPLAY_UP` (R z@40 t[80.47, 48.01, 10.83]) -> via `DISPLAY_OVER` (R z@23.32 t[-3.98, 47.06, 0]) -> `DISPLAY_HELD` (R z@23.32 t[-3.98, 13.06, 0]) | [0.7586, 0.6514, 0.0144] / [618, 962, 1278] / 102 | display 4: 190-193 -> via (200, 201, 202) CLK, (203-205) DIO, (206-208) VCC, (209-211) GND -> 212-215 | eye on the display | `ride_beats` |
| 45 | 1195 | Lower the display into the notches in H11 and H12, lean back on H13 | display (moving) | `path=[DISPLAY_HELD, DISPLAY_HALF (R z@23.32 t[-2.29, 2.07, 0]), ZERO]` | [-0.3466, 0.5631, 0.7502] / [560, 972, 1290] / 70 | 212-215 -> via 216-219 -> 220-223 | label 4-Digit Display; 2 lines | |
| 46 | 1203 | Pick up the dot matrix display, lift over the case, hold in front of H11 and H12 | matrix `NAUO81`, **by ride** | by H1: `MATRIX_BENCH` (R z@40 t[114.72, -32.09, 145.85]) -> via `MATRIX_UP` (R z@40 t[114.72, 92.91, 145.85]) -> via `MATRIX_OVER` (R z@20 t[-4.44, 92.64, 1.4]) -> `MATRIX_HELD` (R z@20 t[-4.44, 22.64, 1.4]) | [-0.7334, 0.6108, 0.2983] / [575, 970, 1320] / 115 | matrix 5: 194-198 -> via (224, 225) VCC, (226, 227) GND, (228, 229) DIN, (230, 231) CS, (232, 233) CLK -> 234-238; **and usb cable 199 -> 239** (`usb_outside`, 969: out over the matrix's wires) | eye on the matrix | `ride_beats` |
| 47 | 1210 | Hang the matrix on the hooks of H11 and H12, lean back | matrix (moving) | `path=[MATRIX_HELD, MATRIX_HALF (R z@20 t[-5.11, 2.22, 1.37]), ZERO]` | [-0.6217, 0.5014, -0.6017] / [540, 955, 1285] / 85 | 234-238 -> via 240-244 -> 245-249 | label Dot Matrix Display; 2 lines | |
| 48 | 1219 | Fit H14 over the display: tabs on the matrix's top edge, swing the top in | H14 `NAUO74` | `h14` tilt `R[0,0,1]@10` about [548, 968, 1290.5]: t[-31.9, 39.8, 0], t[1.8, 11.5, 0], t[6.4, 7.7, 0], 0; then seat (a beat each) | [-0.6519, 0.6018, -0.4614] / [552, 975, 1290] / 78 | none | label H14; 4 lines (2 Lee's, 2 `H14_TABS`); inset on 48c (tab on the matrix's top edge) | |

---------------------------------------------------------------------------------------------------------------------------------

## 2. The parts at the Completed View (69 on screen)

| Id | Student name (steps.json `names`) | What it is |
|---|---|---|
| NAUO63 | H1 | front plate, the datum (never moves; `show=` in Step 27) |
| NAUO65, NAUO66 | H2, H3 | side plates (H2 at z ~1358, H3 at z ~1222) |
| NAUO73 | H4 | back plate (x ~590); the module sits on its back |
| NAUO67, NAUO60, NAUO68 | H5, H6, H7 | floor plates (H6 holds the button pockets; H7 laid over the buttons) |
| NAUO61 | H8 | key-rest bar |
| NAUO72, NAUO71, NAUO70, NAUO69 | H9 (x4) | piano keys over the black, yellow, white, blue buttons (z 1249, 1282, 1316, 1349) |
| NAUO64 | H10 | upper deck |
| NAUO62, NAUO77 | H11, H12 | uprights (display supports) |
| NAUO75 | H13 | rear brace / display back-rest |
| NAUO74 | H14 | top cover over the display |
| NAUO78 | Nano I/O Module | on the back of H4, USB end up |
| NANO | Nano Board | in the module |
| NAUO76, NAUO83, NAUO84, NAUO85 | Push Button (hover: Black / Yellow / White / Blue Push Button) | D4, D5, D6, D7, in H6's pockets |
| NAUO79 | 4-Digit Display | TM1637, between H11 and H12, leaning on H13 |
| NAUO81 | Dot Matrix Display | MAX7219 32 x 8, on the hooks at the front of H11 / H12 |
| NAUO282 | USB Cable | right-angle Mini-B end, in the Nano (listed by this end) |
| NAUO283 | USB Cable | A end (unlisted, hover only), on the table behind the case |
| 42 caps (section 3) | Breadboard Wire (F-F) | 21 jumper wires, two caps each (unlisted, hover only) |

17 wood + 10 electronics + 42 caps = 69.

**Riding at the end** (Completed View `carry`, 45 entries, every pose `ZERO`): NANO and NAUO282 (USB_B) on the module; **NAUO283
(USB_A) on H1**; the 21 module-end caps on the module; each device-end cap on its device (3 per button, 4 on the display, 5 on the
matrix). **Offsets**: all 45 are zero; no part rests away from its seat (USB_A's seat is the CAD's own place, on the table behind
the case: box x 642-692, y 887.8-896.3, z 1238-1254). The end view has no `hide` or `poses`.

---------------------------------------------------------------------------------------------------------------------------------

## 3. The wires (22)

Wire ids are made at line 193: `f"{DEVICE_NAME[device].replace(' push button', '')} {pin}"`. Route `a` is always the device's cap,
`b` the module's (`as_routes`, 744; `W.route(..., a=DEV_CAP[w], b=MOD_CAP[w])`). The USB cable: `a` = USB_B (NAUO282), `b` = USB_A
(NAUO283). Caps come from `cad-geometry.json` `caps` (each with device, pin, centre, out, wire_end, pin_tip); `CAP_ON[(device,
pin)]` (178), `DEV_CAP[wire]` (196), `MOD_CAP[wire]` (197). Radius 0.625 (USB 1.75).

| Wire id | Colour | Device | Device cap (a), rides on at end | Module pin | Module cap (b), on NAUO78 | Plugged in | Final route |
|---|---|---|---|---|---|---|---|
| black VCC | #b70101 | NAUO76 | NAUO86 (VCC) | V4 | CAP_V4 | Step 4 | 178 |
| black OUT | #e4e4e4 | NAUO76 | NAUO87 (OUT) | S4 | NAUO96 | 5 | 179 |
| black GND | #343232 | NAUO76 | CAP_GND1 (GND) | G4 | NAUO97 | 6 | 180 |
| yellow VCC | #21f17a | NAUO83 | NAUO88 | V5 | CAP_V5 | 7 | 181 |
| yellow OUT | #7c5a30 | NAUO83 | NAUO89 | S5 | NAUO99 | 8 | 182 |
| yellow GND | #ffdc00 | NAUO83 | CAP_GND2 | G5 | NAUO95 | 9 | 183 |
| white VCC | #85144b | NAUO84 | NAUO90 | V6 | CAP_V6 | 10 | 184 |
| white OUT | #737980 | NAUO84 | NAUO91 | S6 | NAUO100 | 11 | 185 |
| white GND | #3876ac | NAUO84 | CAP_GND3 | G6 | NAUO98 | 12 | 186 |
| blue VCC | #a75294 | NAUO85 | NAUO93 | V7 | CAP_V7 | 13 | 187 |
| blue OUT | #ff4136 | NAUO85 | NAUO92 | S7 | NAUO101 | 14 | 188 |
| blue GND | #3d9970 | NAUO85 | CAP_GND4 | G7 | NAUO102 | 15 | 189 |
| 4-digit display CLK | #ac9400 | NAUO79 | NAUO259 | S8 | NAUO111 | 17 | 220 |
| 4-digit display DIO | #000000 | NAUO79 | NAUO260 | S9 | NAUO112 | 18 | 221 |
| 4-digit display VCC | #ab53ca | NAUO79 | NAUO261 | V9 | NAUO113 | 19 | 222 |
| 4-digit display GND | #bb3d3d | NAUO79 | NAUO262 | G9 | NAUO114 | 20 | 223 |
| dot matrix display VCC | #411900 | NAUO81 | NAUO134 | V11 | NAUO116 | 21 | 245 |
| dot matrix display GND | #339f3f | NAUO81 | NAUO135 | G11 | NAUO117 | 22 | 246 |
| dot matrix display DIN | #2a2f62 | NAUO81 | NAUO136 | S11 | NAUO115 | 23 | 247 |
| dot matrix display CS | #662639 | NAUO81 | NAUO137 | S12 | NAUO118 | 24 | 248 |
| dot matrix display CLK | #377e89 | NAUO81 | NAUO138 | S13 | NAUO119 | 25 | 249 |
| usb cable | #2d2926 (cable_black) | Nano | NAUO282 USB_B, on module | (Nano socket) | NAUO283 USB_A, **on H1** | 26 | 239 |

Final routes: all `stretch: true`; the 12 button wires also `b_from` 81.5 - 83.8 mm (the run in the case does not follow the
module). Lengths: buttons 132 - 207 mm, display 141 - 159, matrix 142 - 166, USB 133.

**Every route a wire has, view by view** (`view:route`; `-` = off screen; vias are a `done` view's `wire_via`):

    black VCC   2:0 2c:12 3:- 4:24 4c:26(via 25) 27:- 32:26 33c:122 42:134 42c:156 43c:178
    black OUT   2:1 2c:13 3:- 5:27 5c:29(via 28) 27:- 32:29 33c:123 42:135 42c:157 43c:179
    black GND   2:2 2c:14 3:- 6:30 6c:32(via 31) 27:- 32:32 33c:124 42:136 42c:158 43c:180
    yellow VCC  2:3 2c:15 3:- 7:33 7c:35(via 34) 27:- 32:35 33c:125 42:137 42c:159 43c:181
    yellow OUT  2:4 2c:16 3:- 8:4 8c:37(via 36) 27:- 32:37 33c:126 42:138 42c:160 43c:182
    yellow GND  2:5 2c:17 3:- 9:38 9c:40(via 39) 27:- 32:40 33c:127 42:139 42c:161 43c:183
    white VCC   2:6 2c:18 3:- 10:41 10c:43(via 42) 27:- 32:43 33c:128 42:140 42c:162 43c:184
    white OUT   2:7 2c:19 3:- 11:44 11c:46(via 45) 27:- 32:46 33c:129 42:141 42c:163 43c:185
    white GND   2:8 2c:20 3:- 12:47 12c:49(via 48) 27:- 32:49 33c:130 42:142 42c:164 43c:186
    blue VCC    2:9 2c:21 3:- 13:50 13c:52(via 51) 27:- 32:52 32c:119 33c:131 42:143 42c:165 43c:187
    blue OUT    2:10 2c:22 3:- 14:53 14c:55(via 54) 27:- 32:55 32c:120 33c:132 42:144 42c:166 43c:188
    blue GND    2:11 2c:23 3:- 15:56 15c:58(via 57) 27:- 32:58 32c:121 33c:133 42:145 42c:167 43c:189
    disp CLK    16:59 16c:68 17:77 17c:81(via 78,79,80) 27:- 32:81 42:146 42c:168 43c:190 44c:212(via 200,201,202) 45c:220(via 216)
    disp DIO    16:60 16c:69 17:- 18:82 18c:86(via 83,84,85) 27:- 32:86 42:147 42c:169 43c:191 44c:213(via 203,204,205) 45c:221(via 217)
    disp VCC    16:61 16c:70 17:- 19:87 19c:91(via 88,89,90) 27:- 32:91 42:148 42c:170 43c:192 44c:214(via 206,207,208) 45c:222(via 218)
    disp GND    16:62 16c:71 17:- 20:92 20c:96(via 93,94,95) 27:- 32:96 42:149 42c:171 43c:193 44c:215(via 209,210,211) 45c:223(via 219)
    mtx VCC     16:63 16c:72 17:- 21:97 21c:100(via 98,99) 27:- 32:100 42:150 42c:172 43c:194 46c:234(via 224,225) 47c:245(via 240)
    mtx GND     16:64 16c:73 17:- 22:101 22c:104(via 102,103) 27:- 32:104 42:151 42c:173 43c:195 46c:235(via 226,227) 47c:246(via 241)
    mtx DIN     16:65 16c:74 17:- 23:105 23c:108(via 106,107) 27:- 32:108 42:152 42c:174 43c:196 46c:236(via 228,229) 47c:247(via 242)
    mtx CS      16:66 16c:75 17:- 24:109 24c:112(via 110,111) 27:- 32:112 42:153 42c:175 43c:197 46c:237(via 230,231) 47c:248(via 243)
    mtx CLK     16:67 16c:76 17:- 25:113 25c:116(via 114,115) 27:- 32:116 42:154 42c:176 43c:198 46c:238(via 232,233) 47c:249(via 244)
    usb cable   26:117 26c:118 27:- 32:118 42:155 42c:177 43c:199 46c:239

What the route sets are:
- 26-58 / 81-116 / 118: the **bench** shapes (`bench_layout` 304, `plugged_on_bench` 316, `usb_cable(MODULE_BENCH, USB_A_BENCH)`):
  a_ref = the device's bench pose, b_ref = `MODULE_BENCH`. Shown again from Step 32 (electronics beside the case).
- 119-121: the blue button in the case, the others on the bench (`first_button_layout`).
- 122-133: all four buttons in the case, module on the bench (`case_bench_layout` 751; through H5's hole, under the keys, under H4,
  out behind it, across to the module).
- 134-155: the 41c shapes again, with bend data (`as_routes(..., held_in_case=True, tail=True)`: `b_from`, `tail_from`, `b_whole`;
  the matrix's via `head_first` 1136; USB `tail_from` 72.6, `a_whole` 40). 156-177: module held 102.3 mm over its seat
  (`module_held_layout` 872; USB 177 to the A end at its seat).
- 178-199: module seated (`mounted_layout` 894): buttons' up behind H4 (`button_lines_to` 859), display's to its bench place,
  matrix's over the display's way (`M_BRIDGE`), USB 199 (`SEATED_CABLE`).
- 200-223: the display's way up and in (`tunnel_way` 943, `display_way` 926 / `over_h4` 888); 224-249: the matrix's
  (`matrix_way` 959); 239: the USB cable outside the matrix's wires (`usb_outside` 969).
- Note: route ids are shared where two shapes are identical (yellow OUT's loose route at Step 8 is route 4, its ribbon route of
  Step 2: `PARK_X` 618 = `RIBBON_X0` 611 + 4 x 1.75).

**How caps move in the wire steps.** `wire_step` (509) puts both caps of the wire on the module (`g.carry([cap], by=MODULE,
pose=lying_on_bench[cap], appear=False)`, 523-524; `loose` 242 / `loose_poses` 219 lay them on the bench, `HUB` 205 turns world
poses into module-relative ones). `plug_on` (335) returns `ride = {a: [...vias, HUB(a, pa)], b: [...vias, ZERO]}` and the routes,
one per stage: buttons 1 via (`held`: 12 mm out along the pin, `along_out` 148); display 3 vias (`lifted`, `over`, `held` 30 mm
along its pin); matrix 2 vias (`gathered` in the gap at z 1338, `held` 5 mm off its pin). The vias' poses are in steps.json as
the Step Nc `carry[cap]['via']` (module-relative), the loose pose as the Step N `carry[cap]['pose']`. All layouts are settled by
`routing.py` (`R.ribbon` 59, `R.settle` 138, `R.Surfaces` 107) through `settled()` (282), cached by name in `LAYOUTS`.

---------------------------------------------------------------------------------------------------------------------------------

## 4. Bench and case transitions

**Bench phase (Steps 1 - 26).** The module lies flat, pins up, at `MODULE_BENCH` (world box x 646.9-700.2, y 877.1-891.6,
z 1269.8-1328.8; `bench_y` 877.104, the bench is the module's underside). The buttons stand in a row in front of it at
`BUTTON_BENCH[k]` (`button1..4_bench`: R[0.749595, -0.661883, -0.00437]@179.94 about each button's middle, t [135.22, 43.66, 34.08],
[135.15, 43.39, 15.38], [135.28, 43.26, -3.23], [135.39, 44.66, -21.64]); world middles x 641.5, y 948.6, z 1275.8 / 1289.6 /
1303.6 / 1317.7. **They hang in the air**: box y 933.6 - 963.7, about 56 mm above the bench (the CAD's / published pose copy).
Display at `DISPLAY_BENCH` (box x 647.8-675.2, y 911.1-938.6, z 1196.5-1244.0), matrix at `MATRIX_BENCH` (x 624.9-669.5,
y 901.3-946.2, z 1365.0-1500.9), USB A end at `USB_A_BENCH` (raised from the CAD copy so its lowest corner is on the bench, 408;
world middle [596.7, 881.4, 1398.9]). The case's own table is `table_y` 887.79, 10.7 mm above `bench_y`.

**Put away and back.** After Step 26 everything electronic is put away (618-619); Steps 27 - 31 build H1 - H6 alone. Before Step
32 (679-692) the electronics are re-declared to ride **on H1** at exactly their bench poses (so "beside the case" is the bench
place: behind the case at +x beyond H4 (x ~590), the display to the back-left (-z), the matrix and the USB A end to the back-right
(+z)), with each device's caps now on the device and the module's caps, the Nano and USB_B on the module. Step 32 makes them
`appear` with the bench routes (`ON_THE_BENCH`: 26-58, 81-116, 118); the view is turned over (flip) and starts afresh (cut after
the put_away), so nothing glides.

**Buttons into their pockets (Steps 32 - 33, flipped).** Blue first (`FIRST = 3`), then the other three together with their own
paths (`button_way`, 779: from the bench place, 26 mm clear (-x; the others also -8 z), lifted 110 mm (screen-up while turned
over), over the pocket 70 mm off (`BUTTON_DOWN`), pressed in; a beat each). Wires: 32c blue -> 119-121; 33c all 12 -> 122-133.
The module, display and matrix stay on the bench through Step 41 (their routes 81-116 / 118 unchanged until 42).

**Module, display, matrix into the case (Steps 42 - 47).**

| Stage | Module | Display | Matrix | USB A end | Routes (buttons / display / matrix / usb) |
|---|---|---|---|---|---|
| 41c | bench | bench | bench | bench | 122-133 / 81-96 / 100-116 / 118 |
| 42 (hover) | bench | bench | bench | bench | 134-145 / 146-149 / 150-154 / 155 (same shapes, bend data) |
| 42c (fade) | held `T[0, 102.3, 0.2]` | bench | bench | seat (`ZERO`, behind the case) | 156-167 / 168-171 / 172-176 / 177 |
| 43c | seat | bench | bench | seat | 178-189 / 190-193 / 194-198 / 199 |
| 44c | seat | held (via under, up, over) | bench | seat | - / 212-215 (via 200-211) / - / - |
| 45c | seat | seat (via half) | bench | seat | - / 220-223 (via 216-219) / - / - |
| 46c | seat | seat | held (via up, over) | seat | - / - / 234-238 (via 224-233) / **239** |
| 47c | seat | seat | seat (via half) | seat | - / - / 245-249 (via 240-244) / - |

(The round-4 five-beat way for Step 42, `WAY_42` 1116-1133 with the cable's shapes `_cables`, is still computed in guide.py but
overridden by `STEP42_REAPPEAR` (1159-1161); only the fade's end shapes are in steps.json.)

**Which way the published deconstruction goes.** Its Steps 2 - 4 (matrix, display, module lifted off still wired, laid beside the
housing) are exactly this build's Steps 47/46, 45/44 and 43/42 reversed, in that order; its D5 - D16 (H13, H12, H11, H10, keys,
H8, turned over: H7, the buttons, H6, H5, upright: H4, H1) are 41 back to 27 (with 36 + 37 and 32 + 33 merged), except that it
ends the case on H1 (H2 and H3 left standing, then hidden), where this build's reverse would end on H1 with H2, H3 off first.
Its bench phase (D17 - D23: matrix off its wires, matrix wires, USB, buttons off their wires, display off its wires, the 16 other
wires, the Nano) regroups this build's Steps 26 - 1 and leaves the electronics where Step 41c has them (= Step 26c's bench layout).

---------------------------------------------------------------------------------------------------------------------------------

## 5. What a reverse walk will trip on

1. **`take_apart()` learns a part's way in only from `moving`** (stepgen.py 847-858). Learnt: H2, H3, H4 (27-29), H5, H6, H7
   (30, 31, 34; flipped, `FLOOR_CAMERA`), blue button NAUO85 (32), black / yellow / white NAUO76 / 83 / 84 (33, own `paths`), H8
   (35), key NAUO72 (36), keys NAUO71 / 70 / 69 (37), H10 (38, stops [0, 2, 3] -> reversed [0, 1, 3]), H11, H12, H13 (39-41),
   **module (43 only: seat -> `T[0, 102.3, 0.2]`)**, **display (45 only: seat -> half -> held)**, **matrix (47 only)**, H14 (48).
   **Not learnt** (riding or shown, never in `moving`): **H1** (datum, `show=`), **NANO** (Step 1), **USB_B** (26), **USB_A**
   (`rest_at` / ride in 42), **all 42 caps** (Steps 4 - 25), and the bench legs of the module (42, a fade), display (44) and
   matrix (46). A default remove()/lift() of those is "pulled straight out the first free way" (and NANO, riding, gets the
   "not in its seat ... needs a check" review note). Give them `path=` (with `via()` for the beats) built from steps.json: the
   Step 44c / 46c `carry[...]['via']` + Step 44 / 46 `carry[...]['pose']` (world poses, as they ride on H1 at its seat), Step 42
   `carry` (module and USB_A bench poses), Step 1 `offsets['NANO']` (35 mm up, world) and Step 26 `offsets['NAUO282']` (25 mm up).
2. **Leads are not walked back automatically except by `unplug()`**, and only for parts in `came`. For lift()/remove() give
   `wires=` (last route) and `wire_via=` (one route per stage but the last) from the route ids in section 3, e.g. matrix seat -> bench
   in one lift: way seat, half, held, over, up, bench (5 stages): `wire_via` [240, 234, 225, 224] (VCC) ... and `wires` 194 - 198;
   display: seat, half, held, over, up, under, bench: `wire_via` [216, 212, 202, 201, 200] (CLK) ..., `wires` 190 - 193.
3. **Step 46 also moves the USB cable** (199 -> 239, out over the matrix's final wires). Taking the matrix back must put the cable
   back to 199 (`wires={'usb cable': ROUTES[199]}`), or the cable keeps a shape settled round wires that have gone.
4. **Step 42 is a fade (`reappear`), and `_takeoff()` (remove / unplug / lift) has no `reappear` option** (stepgen.py 949-952).
   Gliding the module from held (156-177) back to the bench (134-155) is the move Lee called "a mess" and replaced by the fade for
   that step only. Options for Lee: add `reappear=` to `_takeoff` (a generator change: every kit's check after), or a hand way (the
   round-4 `WAY_42` stops exist only in guide.py). A put_away and bring-back is not available: `place()`, `rest()` and `seat()`
   raise in a deconstruction (stepgen.py 1308, 1546, 1563).
   The published D4 cross-fades the module to "flat on the bench behind the housing", i.e. a fade too.
5. **Order constraints from the routes.** 122-133 (buttons in the case) are drawn with the module at `MODULE_BENCH`; 178-189 with it
   seated (`b_from` keeps the in-case run still while the module moves). So the buttons can come out only after the module is back
   on the bench, as in the build (and as published: D4 before D12). The display's way (200-202, "under the dot matrix display's
   wires") assumes the matrix is on the bench with routes 194-198 (`M_BRIDGE`): take the matrix off before the display (the reverse
   order, and the published one). Routes 156-176 assume display and matrix on the bench.
6. **USB_A rides on H1.** Removing or `put_away`-ing H1 takes USB_A with it while USB_B stays on the module: remove() refuses
   ("lead usb cable would be left on NAUO282 ..."), put_away drops the lead. Lift USB_A with the module in the reverse of Step 42
   (a lift's later parts ride on its first), or `ride_on=` the module, before the case goes.
7. **Caps: on their devices at the end, on the module on the bench.** In the Full Build the device-end caps ride on the module during
   Steps 4 - 26 and on their device from Step 32. In the deconstruction they ride on the device (Completed View). remove(device)
   takes its caps with it and then refuses the leads (their module ends stay) unless the module caps go too or `wires={w: None}`.
   Taking a device "off its wires" (published D17, D20, D21) needs the caps re-parented first: `unplug(caps, path=..., ride_on=
   MODULE, wires=...)`, since `unplug()` raises for parts the Full Build never had in `moving` unless `path=` is given, and it
   picks no `ride_on` or lead routes for them (stepgen.py 1000, 1022-1023, 1082-1096).
8. **Groups spanning two Full Build steps get two arrows by default** (units keyed by Full Build step, 1120-1133): the four keys
   (Step 36: NAUO72; Step 37: NAUO71, 70, 69) and the four buttons (32: NAUO85; 33: the other three). Lee wants them as one group:
   one `remove()` with `units=[[...]]` for a single arrow (published: one arrow on key 3 and an eye; the buttons with an eye only),
   camera from the later step (37's `KEY_CAMERA`, 33's flipped `BUTTONS_IN`). The breadboard wires (42 caps) need `units=` by
   bundle (published D22: two arrows, one per bundle).
9. **Turned over.** Steps 30 - 34 are `flip` (pivot [529, 882, 1290], flip_axis [-0.9701, 0, -0.2425]); 35 turns back. The
   electronics beside the case are turned over with the model in 32 - 33. Steps 30, 31, 34 have `one_off_camera` (`FLOOR_CAMERA`).
10. **Ways with turned poses** (no "passes through a part still there" check, 1049): H5 / H6 / H7 (`hinged`), H10, H14, display
    (45), matrix (47), buttons (32 / 33). Straight ways (checked): H2, H3, H4, H8, keys, H11, H12, H13, module (43).
11. **Sub-assemblies in the hand / isolated / own_frame:** none in the PMG Full Build. Only Step 3 is `single` (no 3c). The bench
    phase is the case-less "sub-assembly": its views are cut at Steps 3, 17 and 27.
12. **Completed View poses nothing differently** (no `hide`, no `poses`; all offsets zero), so `take_apart()` starts from the
    seated model with 45 riders and no resting parts; the USB A end is "in its seat" on the table behind the case.
13. **Review notes still open** (`review_notes` is not set False, so they show): Step 4 / 4c, three wires per button (published)
    vs the STEP's two; Step 42 / 42c, module USB end up (published) vs the STEP's down. README questions 1 - 7 (STEP version,
    wire count, module orientation, jumper length, cap colour grey vs black, Parts 1 - 3, an electronics check) are unanswered.
14. **Bench poses to reuse with care:** the buttons' bench places float about 56 mm above the bench (section 4, "Bench phase"); laying
    the buttons back there in a deconstruction shows them hanging as in the build. The display / matrix bench places and USB A
    place are on the bench.
15. **Step 42's hover routes (134-155) differ from 41c's (122-133, 81-116, 118) only in their bend data**, not their shape: either
    set ends the module's way back to the bench; 134-155 bend with the module by `b_whole` / `tail_from`.
