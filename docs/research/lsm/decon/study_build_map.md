# LSM Full Build, mapped for a deconstruction (study, 21 Oct 2026)

Source: `LSM Build Instructions/guide.py` (826 lines, read whole) and `steps.json` (82 views, 68 routes) as guide.py last wrote
them (21 Oct 2026 14:28), plus `assembly-report.json` (part boxes), `README.txt`, and `tools/stepgen.py` `take_apart()` /
`_takeoff()` (lines 828-1188) to say what the generator will do by default. Read-only study: nothing was run but light Python
reading JSON. Line numbers are guide.py's unless a file is named. "View [k]" is the index in `steps.json` `views`. Routes are
named by their index in `steps.json` `routes`; a deconstruction script reads them as the RCC's and MRA's do
(`ROUTES[VIEW['Step 32']['wires']['wire white']]`). The LSM guide has no `g.chapter()`: no Part files, so the deconstruction reads
`steps.json` only. No step carries a Review note (`review=` nowhere in guide.py; no `review` key in steps.json).

## 1. Ids, names, wires (guide.py:27-53, 165-205, 498-499, 598)

| id | student name (NAMES) | hover name | notes |
|---|---|---|---|
| D1 | D1 | | base plate (`LSM_Bottom_r1`), x 593.8-682.7, y 859.4-862.4, z 1150-1258.6 |
| D2, D3, D4, D5 | D2 .. D5 | | walls: D2 at +Z (button's, "left"), D3 at -Z ("right"), D4 at -X (USB end, "rear"), D5 at +X ("front") (guide.py:43-44). The box stands on the walls' feet: table at y 856.23 (guide.py:108) |
| D6, D7, D8 | D6, D7, D8 | | shelves ("lens" plates) bottom y 901-904, middle 913.5-916.5, top 929.2-932.4 |
| D9_A, D9_B | D9 (both) | | wide LED supports; D9_A nearer D4 (x 617-620), D9_B nearer D5 (x 656-659); z 1153.68-1254.93 (through D3 and D2) |
| D10 | D10 | | small matrix support, x 594.0-682.9 (its end tabs through D4 and D5), y 883.1-900.7, z 1203-1206 |
| D11_A..D11_D | D11 (all) | | shelf posts, y 856.0-935.8: A, B at D5's end (x 673-676; A at D2's end z 1234-1250, B at D3's end z 1158-1174); C, D at D4's end (x 600-603; C at D2's end, D at D3's end) |
| BREADBOARD | Breadboard | | y 862.4-871.92 (top), stuck on D1 |
| BACKING | (Breadboard) | | the backing paper, PART_OF breadboard (guide.py:50); put away after Step 1 and never brought back |
| NANO | Nano Board | | rows c and g, columns 2-16, USB socket at column 16 |
| R12K | 12 kΩ Resistor | | in h3, h16; legs are wires `12k leg 1/2` (a=R12K, b=None) |
| R330 | 330 Ω Resistor | | in a11, a19; legs `330 leg 1/2` (a=R330, b=None) |
| CAP | Capacitor | | in j2 (+), j3 (-, stripe); legs are in the mesh (no wire) |
| J_WHITE_M / J_WHITE_F | Breadboard Wire (M-F) | Yellow Breadboard Wire | wire `wire white`, drawn yellow #ffdc00 (guide.py:35-37: the code says white, it is shown and named yellow). Pin in i2, socket on V+ |
| J_GREY_M / J_GREY_F | Breadboard Wire (M-F) | Grey Breadboard Wire | `wire grey`, #cad1ee. Pin in i3, socket on V- |
| J_PURPLE_M / J_PURPLE_F | Breadboard Wire (M-F) | Purple Breadboard Wire | `wire purple`, #4e008e. Pin in b19, socket on IN |
| MATRIX | LED Matrix | | x 606.9-670.7, y 893.1-898.1, z 1173.8-1234.2; its three-pin header at the D4 / D3 corner of its back (pins x 608.24 V+, 610.78 IN, 613.32 V-) |
| BUTTON | Push Button | | through D2's round hole, head outside (+Z) |
| NUT | (Push Button) | | PART_OF button; inside D2 (z 1250.43-1251.93) |
| BTN_RED_PIN, BTN_BLACK_PIN | (Push Button) | | pins on the button's leads `lead red` (#ef3340) in j5, `lead black` (#2d2926) in j16; PART_OF button |
| USB_B | USB Cable | | right-angle Mini-B plug in the Nano's socket |
| USB_A | USB Cable | | the A end, UNLISTED (hover only), lying on the table outside D4 (x 460-509.7); wire `usb cable` (#2d2926, r 1.75) |
| STEM_01..STEM_64 | LED Stem | | square rods drawn from Cadasio's box (no CAD yet), y 902.3-969.0 |

UNLISTED (guide.py:51): USB_A and the six jumper caps (the ribbon is listed by hand as "Breadboard Wire (M-F)" x3,
`g.list_part`, guide.py:375). Wire radii: legs 0.31 (rings every 0.25 mm), jumpers 0.62, button leads 0.62, USB cable 1.75.
`steps.json` `names` already holds the hover names (J_WHITE_M -> 'Yellow Breadboard Wire', ...), so `names=dict(FULL['names'])`
as the MRA's deconstruction does carries them over.

## 2. The build, step by step

Cameras: Step Nc has Step N's camera in every pair (checked). `DIAG` = [-0.5792, 0.5736, -0.5792] (the D4 / D3 corner,
guide.py:121). "dummy way" = a part given a way that stays put only to make the step N beats long (the moving part listed in
`moving` does not move; what moves rides). "ride" = moved through `ride=` (a carried part's pose changes), never in `moving`.

| Step (views) | guide.py | caption (short) | what moves / appears, and its way | riding | wires (routes, N -> Nc) | camera dir / target / radius | annotations | notes |
|---|---|---|---|---|---|---|---|---|
| 1 ([3],[4]) | 276-286 | Peel the backing off the breadboard | appear BREADBOARD (rest_at BOARD_UP [0,49,0], l.276); BACKING rides it, [0,0,0] -> [0,-40,0] | BACKING on BREADBOARD | - | DIAG / [639.2,896.1,1204.2] / 56 | label Breadboard; arrow by hand on BACKING (tail [615.18,861.4,1166.57] -> head y 816.4, width 4) | lines=False; then put_away([BACKING]) l.286. No counterpart |
| 2 ([5],[6]) | 289-290 | Press the breadboard onto D1 | BREADBOARD path [0,49,0] -> 0 (by hand); D1 appears (show) | | | DIAG / [638.2,890.2,1204.3] / 76.6 (generator) | label D1; lines_at 4 corner marks (tip = mouth) | cut (after the put_away) |
| 3 ([7],[8]) | 294-300 | Nano into rows c, g, cols 2-16 | NANO direction +Y, hover 35 | | | DIAG / [638.6,888.0,1192.0] / 50 | labels c16 (side right), g2; 4 lead lines at the pin corners | |
| 4 ([9],[10]) | 302-303 | Bend the 12 kΩ legs | show R12K, staged (isolated), nothing moves | | 12k legs 0/1 -> 6/7 (via 2,3 / 4,5: 30°, 60°) | DIAG / [647.5,877.1,1189.3] / 24 | label; eye on R12K | No counterpart |
| 5 ([11],[12]) | 305-307 | 12 kΩ into h3, h16 | R12K +Y hover 32 (seat) | | | [0.5792,0.5736,-0.5792] / [647.5,886.0,1189.5] / 30 | labels h3, h16; lines at holes | |
| 6 ([13]) | 318-326 | Capacitor polarity card | show CAP, staged, single (no 6c), isolated | | | [0.554,0.2588,0.7912] / [653.6,874.0,1172.0] / 13 | labels GND (-) down-left, VCC (+) down-right; eye on stripe; inset image capacitor-card.webp, side right | No counterpart |
| 7 ([14],[15]) | 327-331 | Capacitor into j2, j3 | CAP +Y hover 29 (seat) | | | [0.4698,0.5736,0.671] / [652.6,885.0,1172.0] / 28 | labels j3, j2; lines at legs' tips; eye near-left on stripe; caution (stripe = j3, GND) | caution |
| 8 ([16],[17]) | 332-333 | Bend the 330 Ω legs | show R330, staged | | 330 legs 8/9 -> 14/15 (via 10,11 / 12,13) | DIAG / [624.5,876.9,1203.5] / 18 | label; eye | No counterpart |
| 9 ([18],[19]) | 334-336 | 330 Ω into a11, a19 | R330 +Y hover 30 (seat) | | | DIAG / [624.5,886.0,1203.5] / 30 | labels a11, a19 | |
| 10 ([20],[21]) | 375-390 | Pull the ribbon's ends apart | appear J_WHITE_M (rest_at RIBBON white, l.379), the other 5 caps ride on it (l.381-384); ride split_ride | 5 caps on J_WHITE_M | white 16 (stays), grey 17 -> 19, purple 18 -> 20 (all stretch) | DIAG / [662.0,925.0,1106.0] / 50.5 | eye on J_GREY_F | isolated; then put_away all six caps (l.390). No counterpart |
| 11 ([22],[23]) | 396-457 | Yellow pin into i2 | J_WHITE_M path PIN_HOVER [0,30,0] -> 0 (by hand); all six caps appear: pins rest at PIN_HOVER, sockets rest at f_pose(P_UP, SOCKET_OFF) (in the air where the upright matrix's pins will be) | | 21/22/23 -> 24/25/23 | [-0.3282,0.6298,-0.704] / [644.3,895.7,1180.6] / 38.3 | label i2; eye on pin | plug on its lead; cut |
| 12 ([24],[25]) | 450-457 | Grey pin into i3 | J_GREY_M [0,30,0] -> 0 | | grey 25 -> 26 | same as 11 | label i3; eye | plug on its lead |
| 13 ([26],[27]) | 450-457 | Purple pin into b19 | J_PURPLE_M [0,30,0] -> 0 | | purple 23 -> 27 | [-0.5792,0.5736,0.5792] / [627.0,892.0,1213.6] / 34 | label b19; eye | plug on its lead. Then put_away the 3 sockets (l.463) |
| 14 ([28]) | 464-473 | Find V+, IN, V- on the matrix | show MATRIX turned over, staged, single, flip | | none shown | flip: [-0.1802,-0.8011,0.5708] / [628,895,1199] / 36 (flip_axis [-0.3011,0,0.9536]) | labels V-, IN, V+ (along the pins); inset [613,895.6,1196] r 11 | isolated, cut; put_away MATRIX (l.473). No counterpart |
| 15 ([29],[30]) | 476-488 | Yellow socket onto V+ | nothing in `moving` (path [0,0]); MATRIX appears, rest_at P_UP (upright over the breadboard, l.476) with the three sockets riding it at SOCKET_OFF [0,0,15] (l.477-478); ride J_WHITE_F -> 0 | sockets on MATRIX | white 24 -> 28 | PIN_VIEW [-0.3592,0.449,-0.8182] / [643,906,1203] / 48 | labels V+ (on MATRIX), i2 (on J_WHITE_M); eye on socket | ride-only plug move; cut |
| 16 ([31],[32]) | 482-488 | Purple socket onto IN | ride J_PURPLE_F -> 0 | | purple 27 -> 29 | PIN_VIEW | labels IN, b19; eye | ride-only |
| 17 ([33],[34]) | 482-489 | Grey socket onto V- | ride J_GREY_F -> 0 | | grey 26 -> 30 | PIN_VIEW | labels V-, i3; eye | ride-only. Then put_away MATRIX and sockets (l.489) |
| 18 ([35],[36]) | 493-549 | Unscrew the nut off the (new) button | BUTTON dummy way TWO_BEATS (3 zero poses: 2 beats); NUT rides BUTTON from [0,0,3.12] through 7 quarter-turn poses to [0,0,-95] turned -720° (Step 18c carry `via`) | NUT, both pins on BUTTON (pins at hand_pin: leads laid straight back 50 mm, l.505-508, 526-527) | leads 31/32 (hand) | [0.6213,0.2806,0.7316] / [638.2,881.6,1207.0] / 53.4 | label Push Button; arrow by hand on NUT (z 1250.3 -> 1193.3) | isolated, cut; put_away NUT (l.549). No counterpart |
| 19 ([37],[38]) | 550-551 | Button through D2 from its engraved side | BUTTON direction +Z hover 100 (path [0,0,100] -> 0); D2 shown (appears, in its seat); against D2 | pins on BUTTON | 31/32 | [0.5792,0.5736,0.5792] / [638.2,881.6,1265.1] / 107.9 (generator) | label D2; one lead line | isolated, cut |
| 20 ([39],[40]) | 552-555 | Screw the nut back on, tight against D2 | NUT path NUT_ON: [0,0,-60], 7 via quarter turns, 0 (path_stops [0,8]); BUTTON dummy TWO_BEATS | pins on BUTTON | 31/32 | look_from [1,1,-1]: [0.5792,0.5736,-0.5792] / [638.2,881.6,1215.1] / 69.3 | one lead line | isolated. Then put_away D2, BUTTON, NUT, pins (l.555) |
| 21 ([41],[42]) | 557-590 | Red lead's pin into j5 | BTN_RED_PIN path [pin_pose('red', D2_OUT), 0]; D2, MATRIX, both pins appear; everything on the base back | D2 rest_at D2_OUT [0,0,57.11]; BUTTON, NUT on D2 (pose 0); pins on BUTTON (hand_pin); MATRIX on BREADBOARD at P_BESIDE (beside the base past D5, turned 180°); sockets on MATRIX | jumpers 33/34/35 (BESIDE); leads 36/37 -> red 38 | [0.5792,0.5736,-0.5792] / [645,884,1209] / 40 | label j5; eye on pin | plug on its lead; cut |
| 22 ([43],[44]) | 585-590 | Black lead's pin into j16 | BTN_BLACK_PIN path [pin_pose('black', D2_OUT), 0] | | black 37 -> 39 | [0.6491,0.6967,-0.3055] / [653.7,892.4,1204.6] / 35.5 (Lee's framing) | label j16; eye | plug on its lead |
| 23 ([45],[46]) | 592-618 | USB Mini-B into the Nano | USB_B path [0,0,25] -> 0; USB_A shown (appears in its seat on the table) | | usb cable 40 -> 41 | BASE_CAMERA DIAG / [630,880,1228] / 125 | label USB Cable; one lead line [637.29,877.37,1211.63] | plug |
| 24 ([47],[48]) | 620-626 | Stand D2 (with button) on D1 | D2 path [D2_OUT, 0]; BUTTON, NUT ride | | leads 38/39 -> 42/43 | BASE_CAMERA | one generator line | no label |
| 25 ([49],[50]) | 629-636 | Lower D4, then push onto D1, D2 tabs | D4 path [[-8,65,0], [-8,0,0], 0] (by hand) | | | BASE_CAMERA | label D4; 4 lead lines by hand | USB cable into D4's foot notch (NOTCH [595.9,859.1,1219.0]) |
| 26 ([51],[52]) | 679-704 | Lift the matrix over D4, lay it outside, LEDs up | D4 dummy way [0]*5 (4 beats); MATRIX rides BREADBOARD: P_BESIDE -> P_UP_BESIDE -> P_MID -> P_UP_OUTSIDE -> P_OUTSIDE (Step 26c carry `via`) | MATRIX on BREADBOARD | jumpers 33/34/35 -> 53/54/55, wire_via 44,45,46 / 47,48,49 / 50,51,52 | [0,0.9961,0.088] (from above) / [638.5,880,1205] / 82 | eye MATRIX; arrow by hand on D1 (tail [690,862.4,1133] -> head [585,862.4,1133], width 5) | ride-only; "turning the matrix". Wires over D4's top edge from here to Step 30 |
| 27 ([53],[54]) | 705-714 | Turn the box over; hook D3 into D4, swing shut | D3 path [turned(Y, 22°, HINGE, [37.09,0,-14.98]), turned(Y, 22°, HINGE), 0]; HINGE = [597.41, 881.63, 1156.68], TILT 22, 40 mm along the tilt | | | flip: [-0.5792,-0.5736,-0.5792] / [622,881.6,1195] / 118 (flip_axis [-0.7071,0,-0.7071]) | label D3; 2 lead lines (D3's end tabs into D4's slots, y 862 / 902) | flip run 27-28 |
| 28 ([55],[56]) | 715-720 | Push D5 onto the open end | D5 direction +X hover 42 | | | flip: [0.5792,-0.5736,-0.5792] / [617.4,881.6,1189.6] / 135.7 (pivot as 27) | label D5; 6 lead lines by hand (D1, D2, D3) | flip |
| 29 ([57],[58]) | 724-727 | Turn right way up; two D9 into D2, D3 slots | D9_A, D9_B +Y hover 65 | | | HELD_CAMERA DIAG / [601,910.9,1204.6] / 114.8 | label D9 on D9_A; 4 generator lines | |
| 30 ([59],[60]) | 728-749 | Pick up the matrix, hold it over the box | D4 dummy [0]*3 (2 beats); MATRIX rides BREADBOARD: P_OUTSIDE -> P_LIFT -> P_HELD | MATRIX on BREADBOARD | 53/54/55 -> 59/60/61, wire_via 56/57/58 | HELD_CAMERA | eye MATRIX | ride-only |
| 31 ([61],[62]) | 750-760 | Hook D10 under the matrix, slide it along | D4 dummy [0]*3; D10 appears riding MATRIX at D10_UNDER [0,-22,40] (l.752), ride -> [0,0,40] (via) -> 0 | D10 on MATRIX | | [-0.6875,0.4904,-0.5355] / [631.8,932.6,1218.0] / 63.4 (Lee's framing) | label D10; arrow by hand on D10 (tail [599.5,880,1202.4] -> head z 1176) | ride-only; "sliding across" |
| 32 ([63],[64]) | 761-790 | Lower the matrix with D10 into the box | MATRIX path [P_HELD, via(P_HALF), 0] (stops [0,2]); from here MATRIX rides nothing | D10, sockets on MATRIX | 59/60/61 -> 65/66/67, wire_via 62/63/64 (HALF) | DIAG / [636,912,1210] / 66 | lead lines to the bottoms of D4's, D5's slots (D10_TABS), lines_to walls + D10; inset on 32c: [612,892,1203], dir [0.15,0.5,-0.85], r 15, ghost MATRIX 0.12, D4 0.25 | |
| 33 ([65],[66]) | 791-797 | Lay D6 on the walls' tabs | D6 +Y hover 64 | | | DIAG / [638.5,913,1204.5] / 84 | label D6; inset on 33c: from above, D6 hidden, red boxes on the 4 D1 slots (D1_SLOTS) | |
| 34 ([67],[68]) | 798-807 | Two D11 (D5 end) down to D1 | nothing in `moving`; D11_A, D11_B appear riding D1 at D11_UP [0,85,0] (l.803), ride -> D11_SHORT [0,6.38,0] | D11s on D1 | | [0.5469,0.359,0.7563] / [638.5,935,1204.5] / 100 | label D11 on D11_A; 2 lead lines (foot up -> short) | ride-only |
| 35 ([69],[70]) | 808-810 | Other two D11 (D4 end) | D11_C, D11_D appear, ride [0,85,0] -> [0,6.38,0] | | | [-0.7476,0.3966,0.5328] / same / 100 | label "2x D11" on D11_C; 2 lead lines | ride-only |
| 36 ([71],[72]) | 811-814 | Turn over; push all four D11 home | ride all four [0,6.38,0] -> 0 | | | flip: [0.4109,-0.8401,0.3541] / [638.5,870,1204.5] / 72 (flip_axis [0.7575,0,0.6528]) | ghost D1 0.5, D5 0.5; eye on D11_B's foot; 4 lead lines y 874.75 -> 857.98; inset on 36c [674.83,857,1166.2] r 6 "The tab through D1" | ride-only; a lock |
| 37 ([73],[74]) | 815-817 | Turn right way up; D7 on the posts | D7 +Y hover 65 | | | SHELF_CAMERA DIAG / [638.5,922,1204.5] / 90 | label D7; lines_to the 4 D11 | |
| 38 ([75],[76]) | 818 | D8 on the posts | D8 +Y hover 55 | | | SHELF_CAMERA | label D8; lines_to D11s | |
| 39 ([77],[78]) | 819-820 | One stem through D8, D7, D6 | STEM_01 +Y hover 44 (axial) | | | STEM_CAMERA DIAG / [638.5,936,1204.5] / 90 | label LED Stem; 1 line | |
| 40 ([79],[80]) | 821-823 | The other 63 stems | STEM_02..64 +Y hover 44 | | | STEM_CAMERA | label "63x LED Stem" on STEM_02; eye on STEM_01; lines=False | |
| Completed View ([81]) | 104 | | everything, in its seat | see section 4 | final routes | HERO_DIR [0.5997,0.5299,0.5997] / [602.9,912.5,1204.3] / 114.1 | | |

Start ([0]): HERO_DIR / [598.9,896.5,1239.5] / 82.6, `hide=[USB_A, USB_B]` (guide.py:103); shows BACKING in its CAD seat between
the breadboard and D1 (out of sight). Parts List pages [1], [2] after it (Electronics; Housing, Supports and Shelves, Stems).
Hand-set motion (path=/paths=/ride=): Steps 1, 2, 10, 11-13, 15-17, 18, 20, 21-22, 23, 24, 25, 26, 27, 30, 31, 32, 34-36. Generator
ways (direction + hover): 3, 5, 7, 9, 19, 28, 29, 33, 37-40. Isolated (sub-assembly in the hand) views: 4, 6, 8, 10, 14, 18, 19, 20.
`cut` (no glide from the view before): Steps 2, 11, 14, 15, 18, 19, 21.

## 3. Wire states, view by view (route indices)

| view | white | grey | purple | red | black | usb | 12k 1/2 | 330 1/2 | wire_via (N -> Nc) |
|---|---|---|---|---|---|---|---|---|---|
| Start, Completed View | 65 | 66 | 67 | 42 | 43 | - (Start) / 41 (end) | 6/7 | 14/15 | |
| Step 4 / 4c | | | | | | | 0/1 -> 6/7 | | 12k: 2,3 / 4,5 |
| Step 8 / 8c | | | | | | | | 8/9 -> 14/15 | 330: 10,11 / 12,13 |
| Step 10 / 10c | 16 | 17 -> 19 | 18 -> 20 | | | | | | |
| Step 11 / 11c | 21 -> 24 | 22 -> 25 | 23 | | | | 6/7 | 14/15 | |
| Step 12c, 13c | 24 | 26 | 23 -> 27 (13c) | | | | | | |
| Step 15 -> 17c | 24 -> 28 (15c) | 26 -> 30 (17c) | 27 -> 29 (16c) | | | | | | |
| Steps 18-20 | | | | 31 | 32 | | | | |
| Step 21 / 21c | 33 | 34 | 35 | 36 -> 38 | 37 | | | | |
| Step 22c | 33 | 34 | 35 | 38 | 39 | | | | |
| Step 23 / 23c | 33 | 34 | 35 | 38 | 39 | 40 -> 41 | | | |
| Step 24c | 33 | 34 | 35 | 42 | 43 | 41 | | | |
| Step 26c (to 30) | 53 | 54 | 55 | 42 | 43 | 41 | | | white 44,45,46; grey 47,48,49; purple 50,51,52 |
| Step 30c (to 32) | 59 | 60 | 61 | | | | | | 56 / 57 / 58 |
| Step 32c (to end) | 65 | 66 | 67 | | | | | | 62 / 63 / 64 |

What each jumper shape is (guide.py): 16-20 the ribbon on its own (l.361-370); 21-23 pins held 30 mm up, sockets held off the
upright matrix's pins (HOVER_MIDS, l.423); 24-27 pins in, sockets off (LOOSE_MIDS; 25 = HELD_GREY, l.433); 28-30 sockets on the
upright matrix (ON_MIDS); 33-35 BESIDE (matrix beside the base past D5, l.567-571); 44-46 / 47-49 / 50-52 UP_BESIDE, MID,
UP_OUTSIDE (l.683-699); 53-55 OUTSIDE (over D4's top edge, matrix outside D4, l.662-676); 56-58 LIFT (l.744-747); 59-61 HELD
(l.735-742); 62-64 HALF (l.771-779); 65-67 SEATED (l.762-766). Button leads: 31/32 laid straight 50 mm back from the button
(hand_lead, l.516-520); 36/37 the same with D2 at D2_OUT; 38/39 plugged, D2 out; 42/43 seated (round the USB plug's far side, under
D10, SEATED_LEAD_MIDS l.622-623). USB: 40 plug 25 mm out; 41 seated, through D4's foot notch to the A end.

Route options. Jumpers 21-30 and 33-67: `stretch` False where `jumper(..., stretch=False)`; from 33 on each has `b_from` (only
the last 6 mm at the socket move with the matrix, `follow=6.0`) and `tail_from` (matched from the socket's end from that point:
the run in the box stays put while the matrix moves). Ribbon 16-20, purple 23/27-30, button leads, USB: `stretch` True. Legs:
a=resistor, b=None. Final lengths: white 112.8 mm, grey 109.3, purple 47.9, red lead 69.4, black lead 32.6, USB 116.0.

## 4. The finished model (Completed View, view [81])

Every part is in its CAD seat (the view has no offsets). 97 parts visible: all of section 1 except BACKING (put away at Step 1,
never back). `carry` at the end, which `take_apart()` turns into riding (stepgen.py:891):

| rides on | riders (pose 0 = in its seat) |
|---|---|
| D2 | BUTTON, NUT |
| MATRIX | J_WHITE_F, J_GREY_F, J_PURPLE_F (on the V+, V-, IN pins), D10 (its hooks on the matrix's edges) |
| D1 | D11_A, D11_B, D11_C, D11_D |

Not riding (free, seated): D1-D5, D6-D8, D9_A, D9_B, MATRIX (no longer on BREADBOARD after Step 32), BREADBOARD, NANO, R12K, R330, CAP,
the three jumper pins, both button pins (their carry by BUTTON ended at Steps 21 / 22), USB_B, USB_A, the 64 stems.
Nothing rests out of its seat (no `rest_at` survives), so there is no part "beside the model" at the end; USB_A's seat is itself on
the table outside D4 (README: 60 mm further out than needed).

Seats and what holds what (guide.py comments and boxes):
- BREADBOARD stuck on D1 between corner marks (Step 2). NANO, R12K (h3, h16), CAP (j2 +, j3 - stripe), R330 (a11, a19) in the
  breadboard. None of them rides on the breadboard.
- Jumper pins: J_WHITE_M in i2 (V+ to VIN), J_GREY_M in i3 (V- to GND), J_PURPLE_M in b19 (IN, from the Nano's pin D7 via the 330 Ω)
  (guide.py:202). b19 is under the USB plug's leg (the purple wire passes 0.3 mm into it, README Q2).
- Sockets on the matrix's header (riding MATRIX): white on V+, purple on IN, grey on V-.
- Final jumper routes 65/66/67 (guide.py:645-655, 762-766): from the pin, under the end of D9_A nearest D3 (white and grey over the
  Nano's ICSP pins, 1.8 mm under D9_A's engraved end; purple under its lower edge), along the floor beside D4 (x 605 / 607.4 /
  611), up into D10's slot (x 605.2-612.8) and back under the matrix to the socket. Ends: a = J_*_M (free, in the breadboard),
  b = J_*_F (riding MATRIX).
- Button: BUTTON through D2's hole from D2's engraved (outer) side, NUT tight inside; leads 42 (red, BUTTON -> BTN_RED_PIN in j5)
  and 43 (black -> BTN_BLACK_PIN in j16, j16 under D10). a = BUTTON (riding D2), b = pin (free).
- USB: USB_B in the Nano's socket (column 16), cable 41 leaves along -X down past the breadboard, over D1's edge, through the notch
  in D4's foot (z 1216-1222, y up to 862.7) and along the table to USB_A (x 460-509.7, y 856.23-864.78, z 1211-1227). a = USB_B,
  b = USB_A, both free.
- Walls: D2's tabs in slots along D1's edge; D4 over the tabs of D1 and D2 (closed slots: it went on from 8 mm out, -X); D3's end
  tabs hooked into D4's slots, D1's tabs into D3's; D5 over the tabs of D1, D2, D3. D9_A / D9_B in slots in D2 and D3 (their ends
  reach both walls' outer faces); the matrix rests on the D9s. D10's end tabs in slots in D4 and D5 (reaching through both),
  D10 hooked under the matrix, the three jumpers in its slot. D6 lies on the walls' tabs (0.3 mm above the D9s' tops), the
  D11 posts down through D6's corner slots with their tabs through slots in D1 (D1_SLOTS x 601.63 / 674.83, z 1166.2 / 1242.4);
  D7 and D8 on the posts (D8's top just under the posts' top latches); each stem down through D8, D7, D6 to stand over its LED.
- Title page (Start): the Full Build's title page hides USB_A and USB_B; the deconstruction's title page is this one
  (`take_apart()` keeps `views[0]`).

## 5. Sub-assemblies, and the order the build makes them

1. **The breadboard on D1** (Steps 1-9): backing off (1, in the air 49 mm up), onto D1 (2), Nano (3), 12 kΩ legs bent then in (4, 5),
   capacitor card then in (6, 7), 330 Ω legs bent then in (8, 9). Built in place; no part rides on the breadboard at the end.
2. **The jumper ribbon** (10): three wires lying on their own, ends pulled apart, put away. Then **pins into the breadboard** (11-13)
   with the sockets held in the air where the upright matrix's pins will be.
3. **The LED matrix with its three sockets** (14-17): the matrix turned over to find its pins (14, its own view), then held upright
   over the breadboard (rest_at P_UP) and each socket onto its pin (yellow V+, purple IN, grey V-), the sockets riding the matrix
   from there on. Put away; it comes back at Step 21 riding the BREADBOARD at P_BESIDE, beside the base past D5, turned 180°.
4. **D2 with the button, its nut and its two leads** (18-20, in the hand, isolated): nut off the new button (two turns), button
   through D2 from the engraved side, nut back on. Put away; back at Step 21 with D2 standing 57.11 mm out from its seat
   (D2_OUT, +Z), BUTTON and NUT riding D2, the pins riding the button at the end of straight 50 mm leads. Leads' pins into j5,
   j16 (21, 22: the pins stop riding), USB plug in (23), then D2 stood on D1 (24), the leads following (38/39 -> 42/43).
5. **D4 from above** (25): down 65 mm 8 mm out from its seat, then pushed 8 mm +X onto the tabs; the USB cable into its notch.
6. **The matrix out over D4** (26): from beside the base, up, over the D2 end turning a quarter, out turning the other quarter, down
   to lie outside D4 (P_OUTSIDE [-90.76,5.89,25.09]), the wires over D4's top edge; it rides the BREADBOARD.
7. **D3's two-stage tilt** (27, turned over): along its own tilted length 40 mm into D4's slots, 22° open about the hinge at D4's
   inner face / D3's inner face, then swung shut onto D1's tabs.
8. **D5** (28, turned over): +X 42 mm onto the open end.
9. **The two D9** (29): down 65 mm into slots in D2 and D3 (the jumpers already lie under D9_A's engraved end).
10. **The matrix held over the box** (30): lifted to P_LIFT [-90.76,56.64,25.09], moved over the box to P_HELD [-0.2,56.64,-0.32],
    no turn; wires dead straight along under its edge past where D10 comes up.
11. **D10 hooked under the matrix** (31): appears 22 mm under and 40 mm along (+Z), up, then slid -Z until its hooks hold both
    edges; rides the matrix from then on.
12. **The matrix and D10 lowered in** (32): through P_HALF [-0.1,28,-0.16] without stopping; D10's ends into D4's and D5's slots.
13. **D6** (33): down 64 mm onto the walls' tabs.
14. **The D11 posts** (34-36): A, B (D5 end), then C, D (D4 end), each pair from 85 mm up to 6.38 mm up (tabs at D1's top),
    then the box turned over and all four pushed home through D1. They ride D1 throughout.
15. **D7, D8** (37, 38): down 65 and 55 mm onto the posts.
16. **The stems** (39, 40): STEM_01 alone, then the other 63 together, each down 44 mm.

## 6. Build steps with no counterpart in a take-apart

- **Step 1** (backing peeled off): preparation. The published deconstruction never lifts the breadboard off D1 either.
- **Steps 4 and 8** (resistor legs bent): the resistors come out with their legs bent (the leg wires have b=None and go with them).
- **Step 6** (capacitor polarity card) and **Step 14** (finding the matrix's pins, turned over): information only.
- **Step 10** (the ribbon's ends pulled apart): preparation.
- **Step 18** (the nut off a new button): the reverse of Step 20 takes the nut off the button in D2 and the reverse of Step 19 the
  button out of D2; nothing puts the nut back on the loose button.
- **Step 26** (the matrix turned round over D4 to lie outside): exists only so that D3, D5 and the D9s could go on with the matrix out
  of the box. A strict reverse needs it twice over (matrix out over D4 while the D9s, D5 and D3 come off, then back over D4 to beside
  the base before D4 comes off: the wires lie over D4's top edge while the matrix is outside). The published deconstruction instead
  lays the matrix with D10 on the table beside the box once D6 is off.
- **Step 30** (lifted outside, moved over the box) and **Step 31** (D10 slid along under the matrix): "sliding across"; reversible,
  but only needed if the matrix goes back outside D4.
- **Step 25's** last 8 mm (+X onto the tabs) and **Step 27's** hook-and-swing: reversible in two stages (pull -X 8 mm then up;
  swing open 22° then slide out along the tilt).
- **Step 36** (box turned over, posts pushed home through D1): a lock. The reverse is pushing the tabs back up out of D1, then
  Steps 35 / 34 reversed (pulled up 85 mm); or the posts simply pulled up (the published deconstruction pulls them up in pairs).
- Turn-over captions: Steps 27 ("Turn the box over"), 29 and 37 ("Turn the box the right way up"), 36 ("Turn the box over").
- Steps 11-13 and 15-17 plug each jumper at each end in a step of its own (house rule: one wire per step); Lee asks for the three
  to come off together in the deconstruction.

## 7. Steps that moved only a plug on its lead (or a part only by riding)

| Step | plug / part | how it moved | in `take_apart()`'s record (`came`)? |
|---|---|---|---|
| 11, 12, 13 | J_WHITE_M, J_GREY_M, J_PURPLE_M | path [0,30,0] -> 0 (by hand); sockets parked in the air at P_UP + SOCKET_OFF | yes (moving) |
| 15, 16, 17 | J_WHITE_F, J_PURPLE_F, J_GREY_F | ride on MATRIX SOCKET_OFF [0,0,15] -> 0, nothing in `moving` | **no** |
| 21, 22 | BTN_RED_PIN, BTN_BLACK_PIN | path [pin_pose(c, D2_OUT), 0]; before, rode BUTTON | yes; `rode` = BUTTON (from Step 20c's carry) |
| 23 | USB_B (USB_A only shown) | path [0,0,25] -> 0 | yes (USB_B); USB_A never moved |
| 26, 30 | MATRIX (sockets riding) | ride on BREADBOARD with `via` stops (Step 26c / 30c carry) | **no** (D4 has the dummy way) |
| 31 | D10 | ride on MATRIX [0,-22,40] -> via [0,0,40] -> 0 (Step 31c carry `via`) | **no** |
| 34, 35, 36 | D11_A-D | ride on D1 [0,85,0] -> [0,6.38,0] -> 0 | **no** |
| 18, 20 | NUT | ride (18) / path (20, with BUTTON's dummy way) | yes, Step 20 only (group NUT + BUTTON) |

The done views carry the ride stops as `carry[id]['via']` (Step 18c NUT, 26c MATRIX, 30c MATRIX, 31c D10), the form the MRA's
`walked_back()` / `riding_back()` read (MRA deconstruction.py:66-91).

## 8. What `take_apart()` and remove() / unplug() / lift() will do by default (stepgen.py:828-1188), and where that goes wrong

`came` (stepgen.py:846-858) records, for each part, every hover view that lists it in `moving`; a default way out is the latest
one whose group is all leaving (`fits[-1]`, l.1000-1007), reversed, with that view's camera.

| part | build record used by default | default way out (reversed) | camera | fine? |
|---|---|---|---|---|
| STEM_01 / STEM_02-64 | Step 39 / Step 40 | up 44 | STEM_CAMERA | yes; but two units -> 2 arrows (one per build step); `units=[STEMS]` for one arrow as the published guide |
| D8, D7 | Steps 38, 37 | up 55, 65 | SHELF_CAMERA | yes |
| D11_A-D | none (ride only) | "computed": riding D1, so lifted straight up, unchecked, with a Review note and a WARNING (l.1027-1032) | none | **no**: give `path=` (e.g. [[0,6.38,0]] then [[0,85,0]], or straight [0,85,0]) and a camera |
| D6 | Step 33 | up 64 | Step 33's | yes |
| MATRIX (+D10, sockets ride) | Step 32 | 0 -> via P_HALF -> P_HELD (stops kept, [0,2]) | Step 32's | way yes; but `lift()` changes no wire by itself: pass `wires={w: ROUTES[59/60/61]}`, `wire_via={w: [ROUTES[62/63/64]]}` |
| D10 | none (rides MATRIX) | lifted straight up, unchecked, Review note | none | **no**: by hand, the reverse of Step 31 from where the matrix is (at P_HELD: [-0.2,56.64,39.68] then [-0.2,34.64,39.68], the Step 31 hover offset) |
| D9_A, D9_B | Step 29 (one group) | up 65 | HELD_CAMERA | yes; two of a kind, not touching -> one arrow each |
| D5 | Step 28 | +X 42 | flipped (Step 28's) | yes |
| D3 | Step 27 | swing open 22° about HINGE, then out 40 mm along the tilt | flipped (Step 27's) | yes |
| D4 | Steps 25, 26, 30, 31 (all group [D4]) | **Step 31's dummy way: does not move** | **Step 31's (the D10 close-up)** | **no**: give `path=[[-8,0,0],[-8,65,0]]` (Step 25 reversed) and BASE_CAMERA (DIAG, [630,880,1228], 125) |
| USB_B | Step 23 | unplug: +Z 25; lead -> route 40 (the Step 23 hover view's) | BASE_CAMERA | yes; USB_A has no record: give it a way (the RCC's `paths={USB_A: [...]}`) or take both ends with remove() |
| D2 (+BUTTON, NUT ride) | Step 24 | +Z 57.11 (to D2_OUT) | BASE_CAMERA | way yes; `remove(D2)` with the pins still in is refused (below); `lift(D2)` needs the leads given: `wires={'lead red': ROUTES[38], 'lead black': ROUTES[39]}` (Step 24's hover view), else they stretch from route 42/43 |
| BTN_RED_PIN / BLACK | Steps 21 / 22 | unplug: back to pin_pose(c, D2_OUT) (the pose assumes D2 at D2_OUT); lead -> route 36 / 37; then rides BUTTON (`rode`) | Step 21's / 22's | yes **only with D2 at D2_OUT first** (Step 24 reversed), as the build's order has it |
| NUT | Step 20 (group NUT + BUTTON) | only if BUTTON goes in the same call; alone: lifted straight up, Review note | | **no** alone: give the reverse of NUT_ON (view [39] `paths['NUT']`, 9 poses, turning) |
| BUTTON | Steps 18, 19, 20 | a group member already gone does not count (l.999-1000): with NUT removed first, Step 20 (NUT + BUTTON) fits and is the latest, so **BUTTON gets Step 20's dummy way and does not move**; with NUT still on and not listed, Step 19 is the last that fits (out +Z 100, the head side, through the nut) | Step 20's / 19's (isolated) | **no**: give `path=[[0,0,100]]` (Step 19 reversed) once the nut is off |
| J_*_M | Steps 11 / 12 / 13 | unplug: up 30; leads -> routes 21 / 25 / 23 (shapes drawn for sockets held off the upright matrix at P_UP) | Steps 11-13's | way yes, **leads no**: pass `wires=` drawn for where the matrix is then; no `rode` (they rested), so they rest 30 mm up unless `ride_on=` |
| J_*_F | none | `unplug()` raises "the Full Build never plugged ... in" (l.1022-1023) | | use `remove()`/`lift()` with a path (the reverse of SOCKET_OFF: [0,0,15] in the matrix's frame, composed with the matrix's pose) |
| R330, CAP, R12K, NANO | Steps 9, 7, 5, 3 | up 30, 29, 32, 35; the leg wires (b=None) go with their resistor | their cameras | yes |
| BREADBOARD | Step 2 | up 49 | Step 2's | yes (if it is to come off at all) |
| **BACKING** | Step 1 (visible in Steps 1, 1c) | - | | **pitfall**: `take_apart()` adds every part any step view showed (l.874-880), so BACKING is placed, riding BREADBOARD at [0,-40,0] (Step 1c), i.e. 40 mm under the breadboard, through D1 and the table. Remedy (untested): `g.put_away(['BACKING'])` straight after `take_apart()` (it makes the first step a cut), or a fix in take_apart() for a part put away and never brought back |

Leads and `remove()` (l.1100-1112): a lead with one end leaving and the other staying is refused. At the end: `wire *` have a = pin
in the breadboard (free) and b = socket riding MATRIX, so removing MATRIX (which takes D10 and the sockets as riders, l.961-971)
is refused until the pins are out (unplugged with `ride_on=MATRIX`, removed with it, or `wires={w: None}`). `lead red/black`:
a = BUTTON riding D2, b = pin in the breadboard: removing D2 (BUTTON, NUT go as riders) is refused until the pins are unplugged
(they then ride BUTTON and go with D2) or listed with it. `usb cable`: both ends free; remove both ends together. Leg wires go
with their resistor.

The two dummy-way parts in the build (D4 in Steps 26, 30, 31; BUTTON in Steps 18, 20) are the only `came` entries that do not move.

Cameras copied from the Full Build keep its keys (stepgen.py:1141-1147, 1722-1725): D3's and D5's are turned-over ones (Steps 27,
28: `flip` True with `pivot` and `flip_axis`); no other part's recorded build camera is turned over. A part moved while riding (D10, D11s, sockets) has no
Full Build camera to copy: give `view_dir=` / `frame=` (or `new_camera=True`). With `new_camera`, `choose_view` frames what is
shown (stepgen.py:1723-1725).

## 9. Constants a deconstruction script will want (guide.py)

- Poses relative to the seat: BOARD_UP [0,49,0] (l.275); PIN_HOVER [0,30,0] (l.237); SOCKET_OFF [0,0,15] (l.224); D2_OUT [0,0,57.11]
  (l.559); USB_OUT [0,0,25] (l.599); D4 way [[-8,65,0],[-8,0,0],0] (l.633); HINGE [597.41,881.63,1156.68], TILT 22, along-tilt
  [37.09,0,-14.98] (l.708-712); D5 +X 42; D9 +Y 65; D6 +Y 64; D11_UP [0,85,0], D11_SHORT [0,6.38,0] (l.802); D7 +Y 65; D8 +Y 55;
  stems +Y 44; NUT_AT [638.23,881.63,1251.0], NUT_OFF [0,0,-95], nut_turns() (l.532-540).
- Matrix poses (all relative to its seat, riding BREADBOARD in the build): P_UP (upright over the breadboard, l.216-220), P_BESIDE =
  turned([0,1,0], 180, MC, [91.01,-21.66,11.37]); P_UP_BESIDE (same, y +25); P_MID = turned([0,1,0], 90, MC, [-26,25,18]);
  P_UP_OUTSIDE [-90.76,25,25.09]; P_OUTSIDE [-90.76,5.89,25.09]; P_LIFT [-90.76,56.64,25.09]; P_HELD [-0.2,56.64,-0.32]; P_HALF
  [-0.1,28,-0.16]; MC = the matrix's box middle [638.82,895.58,1203.99]. D10_UNDER [0,-22,40] (on the matrix).
- Cameras: DIAG [-0.5792,0.5736,-0.5792]; BASE_CAMERA (DIAG, [630,880,1228], 125); HELD_CAMERA (DIAG, [601,910.9,1204.6], 114.8);
  SHELF_CAMERA (DIAG, [638.5,922,1204.5], 90); STEM_CAMERA (DIAG, [638.5,936,1204.5], 90); PIN_VIEW, PIN_CAMERA, LEAD_CAMERA as
  in the table; title / end: HERO_DIR [0.5997,0.5299,0.5997].
- Breadboard holes: `hole(name)` (l.107-112): ROW_X a..j, COL1_Z 1167.91, PITCH 2.54, BOARD_TOP 871.92.

## 10. What must come off before what (seats and part boxes, `assembly-report.json`)

Pairs of parts whose boxes overlap (light Python over `assembly-report.json`; walls' corner tabs and parts in their own holes left
out) and the guide's own comments give these orders. "Build order" means the reverse of the Full Build's order already respects it.

- Stems before D8, D7, D6 (each stem passes through all three: STEM_01 overlaps D6, D7, D8) and before the matrix (they stand over
  its LEDs). Build order.
- D8 before D7 (both on the D11 posts' ledges, D8 just under the posts' top latches), both before the posts. Build order.
- The D11 posts through D6's corner slots (each overlaps D6, D7, D8 by 3 x 3 x 15.9 mm) with their tabs through D1: in the build
  D6 went on before them. Their tabs come through D1 (Step 36).
- D6 before the matrix / D10 (D10's top y 900.68, D6's bottom 900.98), the D9s (top 900.69), and every wall (D6 lies on their
  tabs: D4 / D6 overlap 0.45 mm). Build order.
- Matrix with D10 before the D9s (it rests on them; its box lies within the D9s' height, y 893-898 against 882-901, so it sits down into their top edges) and before
  the Nano (D10's lower edge reaches 1.4 mm into the Nano's box). D10's end tabs run along X through slots in D4
  and D5 (D10 / D4 and D10 / D5 overlap 3 x 17.6 x 3 mm).
- D9_B before the capacitor: CAP's box reaches 1.7 mm into D9_B's (x 655.8-657.1, y 882.2-883.9): the capacitor stands under
  D9_B's lower edge. D9_A over the jumper wires' run (they pass under its engraved end, guide.py:638-644). D9s before D3 and D2
  (their ends pass through both walls' slots). Build order.
- D5 before D3 and D2 (D5 goes over the tabs of D1, D2 and D3); D3 before D4 (D3's end tabs hook into D4's slots); D4 before D2
  (D4 goes over D2's tabs through closed slots, so D4 comes off -X 8 mm before it can lift). Build order: D5, D3, D4, D2 reversed
  from 24, 25, 27, 28.
- USB_B before the purple pin and the 330 Ω resistor: USB_B's box overlaps J_PURPLE_M (b19 under the plug's leg) and R330
  (4.9 x 4.9 x 4.4 mm), and the Nano (its socket). The USB cable runs through D4's foot notch: D4 lifts off it (the notch is open
  below). Build order (R330 Step 9 and purple pin 13 before USB 23).
- The button's leads (42, 43) run round the USB plug's far side and under D10 (j16 under D10, guide.py:621-625).
- R12K before the Nano (their boxes overlap 1.2 mm in x: the resistor lies beside the Nano's row g pins). Build order.
- BUTTON and NUT: the nut inside D2 (z 1250.43-1251.93) on the button's thread; the button goes out of D2 towards +Z (its head
  side), wires first in the build (Step 19), so the nut off first.
- The breadboard on D1 is held by its sticky backing; the published deconstruction stops with it on D1.
