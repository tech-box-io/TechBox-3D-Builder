# LAC deconstruction: TechBox's published take-apart mapped onto our Full Build

Study, 21 Oct 2026 (read-only; nothing was run but light Python on JSON). For the planner of `LAC Build Instructions/deconstruction.py`.

Sources: `docs/research/guide_19075-lac_deconstruction.md` (the published take-apart, 47 steps, read whole; "pub [k]" = its viewer
index), its payload `docs/research/lac/decon/published/raw/19075-lac_deconstruction.json`, `LAC Build Instructions/guide.py` and
`steps.json` as last written (HEAD 61c6efc, F9 now brought in over its slots and tipped in), `tools/stepgen.py` `take_apart()` /
`_takeoff()` (lines 828-1246), the MRA / RCC / PMG / LSM `deconstruction.py`, `docs/cadasio-patterns.md` section 11,
`docs/research/lac/cad_study.md`, `docs/research/lac/round1/published_motions.md`.
Helper scripts (all read-only, in `docs/research/lac/decon/scripts/`): `views.py` (each Full Build view: moving, path, camera),
`changes.py` (what changes from view to view: visible, offsets, carry, wire routes), `published_cameras.py` (the published cameras in
our terms), `build_table.py` (section 2's table), `jumper_order.py` (which jumper's way out passes
through which), `lead_order.py` (which lead's unplugging passes through which, in the published order and others). The published arrows were measured with
`docs/research/lsm/decon/arrows/measure_arrows.py` (output kept in the tables below, not saved as a file).

Numbering: our Full Build has 57 steps, numbered as TechBox's published Full Build (19075-lac_full_build), so "Step N" below is both.
"View [k]" = index in our `steps.json` `views`; "route n" = index in `steps.json` `routes`. Published cameras are converted to ours as
`view_dir` = unit(eye - target), radius = distance x sin 22.5 / 1.08 = 0.3543 x distance (Cadasio's frame is our assembly frame, mm =
scene units / 0.6054634; the same conversion as published_motions.md). "rolled" = the published camera's up is not world up (the
report's "up-axis flipped to -X"): our player cannot roll the camera; `flip=True` (the model turned over) is the nearest we have.

## 0. In short

- The published take-apart (47 steps) maps onto our Full Build almost step for step: 1 - 8 are our Steps 57 - 48 reversed (F6, F2, F5,
  F1 forward and laid aside, the LCD out, F8, F4 with the switch), then each wired part: unplug, take apart, remove; jumpers; RTC,
  resistors, Nano; it ends on F3 with the breadboard. Every pose, camera and wire shape our take-apart needs is already in steps.json
  (the Full Build's own, reversed): section 3 names them step by step.
- **Dropped:** published 16 - 18 (the pot's washer, nut and knob put back on for storage: Lee's "nothing refitted").
- **Moved (in-house rules):** the USB cable to our Step 4, as soon as F6, F2 and F5 are off (power first; Step 1's caution as the LSM's).
- **Moved (our model):** the buzzer must come out of the F7s (published 26 - 28) before the pot's and the LCD's wires are unplugged
  (published 9 - 11, 19 - 22), or their leads pass through the buzzer's black lead; the pot's leads need F1 back where they were plugged
  in (our Step 47 undone: one extra step) or the tan lead passes through three others; orange and yellow jumpers must come off before
  purple, blue and green (published 42, 43 last), or those pass through orange; F9 before the buzzer (our Full Build's order).
- **Added:** F1 moved back beside the breadboard's end, and F1 picked up upright for its knob, nut and washer (our Full Build's Steps 47
  and 29 undone: ours lies face down, the published face up).
- **By hand** (the generator has no way for them): F7s, F9, switch, knob, nut, washer, the LCD's female caps, USB_A, the LCD's and F1's
  and F4's ride halves, the buzzer and LCD taken away; `ride_on=BUZZER` for the buzzer's red cap; `leave_out=['NAUO141']`.
- Result: 46 steps one wire each (section 7), or 31 with Lee's groups; questions for Lee in section 8.

## 1. Our Full Build as it ends (what `take_apart()` starts from)

`take_apart()` starts from the Completed View (view [117]): 57 parts visible. Its camera is the title page's (dir [0.5997, 0.5299,
-0.5997], target [666.5, 915.8, 1323.5], radius 144.8). One part was shown once and put away for good: **NAUO141, the breadboard's
backing paper** (Step 1, `g.put_away([PAPER])`): without `take_apart(leave_out=[PAPER])` it comes back where Step 1c left it, as the
LSM's BACKING did.

**Riding at the end** (Step 57c `carry`, every pose ZERO): the rocker switch NAUO46 on F4; the washer NAUO146, nut NAUO12 and knob
NAUO13 on the potentiometer NAUO11; the LCD's four female caps NAUO97 - 100 on the LCD NAUO94; **F7A NAUO42, F7B NAUO43 and F9 NAUO45
on F3**. **Resting off its seat:** only USB_A (the cable's A end, on the table behind the case: `{"t": [-24.97, 12.56, -62.58], "r":
[0, 1, 0, -90], "at": [599.97, 876.35, 1389.92]}`). Everything else is seated and rides on nothing: F1 and the potentiometer (pushed on
by a path in Step 54), the LCD (path, Step 52), the buzzer (path, Step 43), F4 (path, Step 49), F8, F5, F2, F6, every jumper and lead
cap, the LCD's male caps, the RTC and coin, both resistors, the Nano, the breadboard.

**What the generator knows of each part's way in** (`take_apart()`'s `came`: only parts listed in a Full Build step's `moving`):
Nano 3; RES1 5; RES2 6; RTC + coin 7; jumper caps 9 - 14, 20, 21 (both caps of a jumper in one step); switch caps 16 - 18; pot caps
30 - 32; buzzer caps 33, 34; LCD male caps 36 - 39; USB_B 40; buzzer 43; F4 49; F8 50; LCD 52; F1 + potentiometer 54; F5 55; F2 56;
F6 57 (and the breadboard 2, plus the dummy "stay" moves of Steps 23, 27, 29, 47). **Not known** (moved in only by `ride=`, or
appeared in place): F7A, F7B (Steps 41, 42, 44), F9 (45, 46), the switch (15), knob, nut and washer (22 - 28), the LCD's female caps
(36 - 39), USB_A, and the moves of F1 (25, 29, 47, 53), F4 (48) and the LCD (51) that were rides. For these `remove()` falls back to a
straight pull chosen by the collision test, and since they ride (or rest off their seat) it logs "not in its seat: lifted straight up,
unchecked" and adds a Review note: **give each of them a way by hand** (section 5 lists the Full Build poses to use).

### 1.1 Every lead, both ends (Completed View; `a` / `b` as in `steps.json` routes)

| wire id | a (end) | b (end) | route at end | plugged in | notes for the take-apart |
|---|---|---|---|---|---|
| jumper black | NAUO16 cap, i23 | NAUO17 cap, (+) red | 21 | Step 9 | loose M-M: both caps in one `remove()`, the lead goes with them |
| jumper green | NAUO20, (-) blue | NAUO19, i24 | 22 | 10 | as above |
| jumper purple | NAUO25, a8 | NAUO26, i22 | 23 | 11 | as above |
| jumper blue | NAUO22, a9 | NAUO21, i21 | 24 | 12 | as above |
| jumper white | NAUO28, a14 | NAUO15, (-) blue | 25 | 13 | way in [14, 5, 0] -> [0, 5, 0] -> 0 (under purple and blue) |
| jumper dark_red | NAUO30, a12 | NAUO31, (+) red | 26 | 14 | way in per cap: NAUO30 from +x, NAUO31 from +z (5 mm up) |
| jumper orange | NAUO53, j1 | NAUO52, i27 | 36 | 20 | lies over purple, blue and green (section 4.4) |
| jumper yellow | NAUO56, j3 | NAUO55, i29 | 37 | 21 | |
| switch red | NAUO46 switch | NAUO47 cap, j27 | 87 | 16 | cap rode on the switch before Step 16: `unplug()` re-hangs it there |
| switch tan | switch | NAUO49 cap, (+) red | 88 | 17 | as above |
| switch black | switch | NAUO48 cap, j29 | 89 | 18 | held 5 mm up (not 18) in Step 18 |
| pot red | NAUO34 cap, (+) red | NAUO11 potentiometer | 121 | 30 | cap rode on the pot before Step 30; route drawn with F1 seated |
| pot tan | NAUO33 cap, a5 | potentiometer | 122 | 31 | as above |
| pot black | NAUO14 cap, (-) blue | potentiometer | 123 | 32 | held 5 mm up in Step 32 (under the tan's hump) |
| buzzer red | NAUO58 cap, j4 | NAUO62 buzzer | 79 | 33 | **the cap rode on nothing before Step 33** (it appeared moving): `unplug(..., ride_on=BUZZER)` or the buzzer's `remove()` is refused |
| buzzer black | NAUO59 cap, (-) blue | buzzer | 80 | 34 | cap rode on the buzzer before Step 34 |
| lcd purple (GND) | NAUO82 male, (-) blue (hole moved +10.16 z, LCD_RAIL_SHIFT) | NAUO97 female, on GND, rides on the LCD | 114 | 36 | loose M-F: both caps in one `remove()`; the female has no known way (give one) |
| lcd yellow (VCC) | NAUO84 male, (+) red (+15.23 z) | NAUO98 female, VCC | 115 | 37 | as above |
| lcd teal (SDA) | NAUO86 male, b8 | NAUO99 female, SDA | 116 | 38 | as above |
| lcd blue (SCL) | NAUO93 male, b9 | NAUO100 female, SCL | 117 | 39 | as above |
| usb cable | NAUO122 USB_B, in the Nano | USB_A, on the table | 125 | 40 (route 74); 56 bent it into F2's slit (wire_via [74, 124] -> 125) | both ends in one `remove()`; USB_A rests off its seat: give it a way |
| res1 leg 1 / 2 | RES1 | (none) | 6 / 7 | 5 | go with RES1 |
| res2 leg 1 / 2 | RES2 | (none) | 8 / 9 | 6 | go with RES2 |

So the wired parts and what ties them: **the potentiometer** (3 leads to the board; carries knob, nut, washer; sits in F1), **the
switch** (3 leads; sits in F4), **the buzzer** (2 leads; held by the F7s), **the LCD** (4 M-F wires to the board; held by F8's slots and
F9's notches), **the Nano** (the USB plug in its socket). A part with a lead whose other end stays cannot be `remove()`d: unplug the
lead first, or take both ends together (loose wires), or `lift()` the part still wired.

## 2. Our Full Build, step by step, as the take-apart needs it

One row per step (made by `scripts/build_table.py`). "path" = moved in through `moving` (known to the generator); "ride" = moved by a
carry pose that changes (unknown to it); routes "a/b->c" = the route before Step N | on Step N -> on Step Nc, with `wire_via` stages.
Camera = Step N's `view_dir` / target / radius (Step Nc has the same in every pair).

| step | caption (cut) | path (generator knows it) | ride (by hand) | routes | camera dir / target / radius |
|---|---|---|---|---|---|
| Step 1 | Begin with the breadboard. Peel the protective backing off its undersi | - | NAUO141 (Breadboard) on NAUO1: appears -> [0.0, -50.0, 0.0] | - | [0.579, 0.574, -0.579] / [674.5, 914.3, 1305.8] / 58.4 |
| Step 2 | Stick the breadboard down onto F3, its red and blue rails along the sa | NAUO1 (Breadboard) from [0.0, 47.0, 0.0], 1 stage(s) | - | - | [0.579, 0.574, -0.579] / [684.3, 914.4, 1289.9] / 95.0 |
| Step 3 | Press the Nano Board into the breadboard: its pins go in rows c and g, | NANO (Nano Board) from [0.0, 40.0, 0.0], 1 stage(s) | - | - | [0.579, 0.574, -0.579] / [676.5, 916.0, 1324.3] / 50.0 |
| Step 4 | Bend the legs of both 12 kΩ resistors (brown, red, black, red, brown)  | - | - | res1 leg 1 None/0->6 via [2, 3]; res1 leg 2 None/1->7 via [4, 5] | [0.579, 0.574, -0.579] / [682.5, 938.2, 1276.8] / 24.0 |
| Step 5 | Press a 12 kΩ resistor into the breadboard, from the (-) blue rail to  | NAUO6 (12 kΩ Resistor) from [0.0, 37.0, 0.0], 1 stage(s) | - | - | [0.579, 0.574, -0.579] / [682.7, 918.0, 1276.7] / 32.0 |
| Step 6 | Press the other 12 kΩ resistor into the breadboard, from the (-) blue  | NAUO7 (12 kΩ Resistor) from [0.0, 37.0, 0.0], 1 stage(s) | - | res2 leg 1 None/8->8; res2 leg 2 None/9->9 | [0.579, 0.574, -0.579] / [682.7, 918.0, 1271.6] / 32.0 |
| Step 7 | Press the real time clock module into row j, its pins from j19 to j24, | NAUO3 (Real Time Clock) from [0.0, 34.0, 0.0], 1 stage(s); NAUO4 (Real Time Clock) from [0.0, 34.0, 0.0], 1 stage(s) | - | - | [0.579, 0.574, -0.579] / [660.0, 934.0, 1290.0] / 52.0 |
| Step 8 | Peel six wires off the ribbon of jumper wires, one of each colour, and | - | NAUO16 (Breadboard Wire (M-M)) on NAUO1: appears -> t[81.3, -15.6, 51.7] r90.0deg; NAUO17 (Breadboard Wire (M-M)) on NAUO1: appears -> t[48.3, -15.6, -12.9] r90.0deg; NAUO20 (Breadboard Wire (M-M)) on NAUO1: appears -> t[52.9, -15.6, 53.1] r90.0deg; NAUO19 (Breadboard Wire (M-M)) on NAUO1: appears -> t[88.4, -15.6, -11.6] r90.0deg; NAUO25 (Breadboard Wire (M-M)) on NAUO1: appears -> t[69.8, -15.6, ... | jumper black None/10->10; jumper green None/11->16; jumper purple None/12->17; jumper blue None/13->18; jumper white None/14->19; jumper dark_red None/15->20 | [0.449, 0.799, -0.4] / [757.4, 885.6, 1305.0] / 42.0 |
| Step 9 | Connect the black jumper wire from i23 to (+) red. | NAUO16 (Breadboard Wire (M-M)) from [0.0, 18.0, 0.0], 1 stage(s); NAUO17 (Breadboard Wire (M-M)) from [0.0, 18.0, 0.0], 1 stage(s) | - | jumper black 10/21->21 | [0.497, 0.819, -0.287] / [680.2, 912.1, 1285.6] / 30.3 |
| Step 10 | Connect the green jumper wire from (-) blue to i24. | NAUO20 (Breadboard Wire (M-M)) from [0.0, 18.0, 0.0], 1 stage(s); NAUO19 (Breadboard Wire (M-M)) from [0.0, 18.0, 0.0], 1 stage(s) | - | jumper green None/22->22 | [0.497, 0.819, -0.287] / [681.4, 912.1, 1284.3] / 31.2 |
| Step 11 | Connect the purple jumper wire from a8 to i22. | NAUO25 (Breadboard Wire (M-M)) from [0.0, 18.0, 0.0], 1 stage(s); NAUO26 (Breadboard Wire (M-M)) from [0.0, 18.0, 0.0], 1 stage(s) | - | jumper purple None/23->23 | [0.497, 0.819, -0.287] / [676.5, 912.1, 1306.5] / 34.5 |
| Step 12 | Connect the blue jumper wire from a9 to i21. | NAUO22 (Breadboard Wire (M-M)) from [0.0, 18.0, 0.0], 1 stage(s); NAUO21 (Breadboard Wire (M-M)) from [0.0, 18.0, 0.0], 1 stage(s) | - | jumper blue None/24->24 | [0.497, 0.819, -0.287] / [676.5, 912.1, 1306.5] / 32.9 |
| Step 13 | Connect the white jumper wire from a14 to (-) blue. | NAUO28 (Breadboard Wire (M-M)) from [14.0, 5.0, 0.0], 2 stage(s); NAUO15 (Breadboard Wire (M-M)) from [14.0, 5.0, 0.0], 2 stage(s) | - | jumper white None/25->25 | [0.497, 0.819, -0.287] / [694.2, 912.1, 1309.7] / 26.0 |
| Step 14 | Connect the dark red jumper wire from a12 to (+) red. | NAUO30 (Breadboard Wire (M-M)) from [14.0, 5.0, 0.0], 2 stage(s); NAUO31 (Breadboard Wire (M-M)) from [0.0, 5.0, 14.0], 2 stage(s) | - | jumper dark_red None/26->26 | [0.369, 0.819, -0.439] / [692.9, 912.1, 1312.3] / 26.0 |
| Step 15 | Push the rocker switch, wires first, down into the square hole in F4 u | - | F4 (F4) on NAUO2: appears -> [-82.7, 17.3, -0.1]; NAUO46 (Rocker Switch) on F4: appears -> [0.0, 0.0, 0.0]; NAUO47 (Rocker Switch) on NAUO46: appears -> [11.4, -5.3, -17.7]; NAUO49 (Rocker Switch) on NAUO46: appears -> [-17.1, -5.3, -11.3]; NAUO48 (Rocker Switch) on NAUO46: appears -> [25.4, -5.3, -12.6] | switch red None/27->27; switch tan None/28->28; switch black None/29->29 | [0.451, 0.752, -0.481] / [596.8, 977.3, 1258.3] / 62.0 |
| Step 16 | Connect the switch's red wire to j27. | NAUO47 (Rocker Switch) from [0.0, 18.0, 0.0], 1 stage(s) | - | switch red 27/30->30 | [0.401, 0.615, -0.679] / [643.7, 917.7, 1281.1] / 45.2 |
| Step 17 | Connect the switch's tan wire to (+) red. | NAUO49 (Rocker Switch) from [0.0, 18.0, 0.0], 1 stage(s) | - | switch tan 28/31->31 | [0.401, 0.615, -0.679] / [643.7, 917.7, 1281.1] / 45.2 |
| Step 18 | Connect the switch's black wire to j29. | NAUO48 (Rocker Switch) from [0.0, 5.0, 0.0], 1 stage(s) | - | switch black 29/32->32 | [0.401, 0.615, -0.679] / [643.7, 917.7, 1281.1] / 45.2 |
| Step 19 | Peel two wires off the ribbon of jumper wires, an orange and a yellow, | - | NAUO53 (Breadboard Wire (M-M)) on NAUO1: appears -> t[83.9, -15.6, -4.1] r90.0deg; NAUO52 (Breadboard Wire (M-M)) on NAUO1: appears -> t[81.4, -15.6, -4.1] r90.0deg; NAUO56 (Breadboard Wire (M-M)) on NAUO1: appears -> t[90.9, -15.6, 1.0] r90.0deg; NAUO55 (Breadboard Wire (M-M)) on NAUO1: appears -> t[88.3, -15.6, 1.0] r90.0deg | jumper orange None/33->33; jumper yellow None/34->35 | [0.449, 0.799, -0.4] / [753.9, 885.6, 1305.0] / 42.0 |
| Step 20 | Connect the orange jumper wire from j1 to i27. | NAUO53 (Breadboard Wire (M-M)) from [0.0, 18.0, 0.0], 1 stage(s); NAUO52 (Breadboard Wire (M-M)) from [0.0, 18.0, 0.0], 1 stage(s) | - | jumper orange 33/36->36 | [0.299, 0.906, -0.299] / [662.4, 912.1, 1309.1] / 44.3 |
| Step 21 | Connect the yellow jumper wire from j3 to i29. | NAUO56 (Breadboard Wire (M-M)) from [0.0, 18.0, 0.0], 1 stage(s); NAUO55 (Breadboard Wire (M-M)) from [0.0, 18.0, 0.0], 1 stage(s) | - | jumper yellow None/37->37 | [0.433, 0.866, -0.25] / [662.4, 912.1, 1304.0] / 44.3 |
| Step 22 | Begin the front panel with the potentiometer. Pull the knob off the po | - | NAUO11 (Potentiometer) on NAUO2: appears -> [21.0, 35.0, 100.0]; NAUO13 (Knob) on NAUO11: appears -> [42.6, 0.0, 0.0]; NAUO12 (Nut) on NAUO11: appears -> [-3.0, 0.0, 0.0]; NAUO146 (Washer) on NAUO11: appears -> [-3.0, 0.0, 0.0]; NAUO34 (Potentiometer) on NAUO11: appears -> [22.0, -44.3, -101.0]; NAUO33 (Potentiometer) on NAUO11: appears -> [29.5, -44.4, -97.0]; NAUO14 (Potentiometer) on NAUO11: ap ... | pot red None/38->38; pot tan None/39->39; pot black None/40->40 | [0.35, 0.451, -0.821] / [756.0, 951.0, 1335.0] / 42.0 |
| Step 23 | Unscrew the nut and take it off the potentiometer's shaft. | - | NAUO12 (Nut) on NAUO11: [-3.0, 0.0, 0.0] -> t[35.0, 0.0, 0.0] r720.0deg +7 via | - | [0.35, 0.451, -0.821] / [756.0, 951.0, 1335.0] / 42.0 |
| Step 24 | Take the washer off the potentiometer's shaft. | - | NAUO146 (Washer) on NAUO11: [-3.0, 0.0, 0.0] -> [35.0, 0.0, 0.0] | - | [0.35, 0.451, -0.821] / [756.0, 951.0, 1335.0] / 42.0 |
| Step 25 | Push the potentiometer's shaft through the round hole in F1 from the b | - | NAUO11 (Potentiometer) on NAUO2: [21.0, 35.0, 100.0] -> [100.0, 35.0, 100.0]; NAUO10 (F1) on NAUO2: appears -> [100.0, 35.0, 100.0] | pot red 38/38->41; pot tan 39/39->42; pot black 40/40->43 | [0.35, 0.451, -0.821] / [822.0, 960.0, 1375.0] / 98.0 |
| Step 26 | Put the washer back on the shaft against F1. | - | NAUO146 (Washer) on NAUO11: appears -> [0.0, 0.0, 0.0] | - | [0.35, 0.451, -0.821] / [822.0, 960.0, 1375.0] / 98.0 |
| Step 27 | Put the nut back on the shaft, and tighten it against F1. | - | NAUO12 (Nut) on NAUO11: appears -> [0.0, 0.0, 0.0] +7 via | - | [0.35, 0.451, -0.821] / [822.0, 960.0, 1375.0] / 98.0 |
| Step 28 | Put the knob back on the shaft, pushing it all the way on. | - | NAUO12 (Nut) on NAUO11: [0.0, 0.0, 0.0] -> [0.0, 0.0, 0.0]; NAUO13 (Knob) on NAUO11: appears -> [0.0, 0.0, 0.0] | - | [0.35, 0.451, -0.821] / [822.0, 960.0, 1375.0] / 98.0 |
| Step 29 | Lay F1 face down in front of the end of the breadboard, as shown, the  | - | NAUO11 (Potentiometer) on NAUO2: [100.0, 35.0, 100.0] -> t[79.0, -10.4, 99.6] r-90.0deg; NAUO10 (F1) on NAUO2: [100.0, 35.0, 100.0] -> t[79.0, -10.4, 99.6] r-90.0deg | pot red 41/41->44; pot tan 42/42->45; pot black 43/43->46 | [0.55, 0.62, 0.56] / [801.3, 950.1, 1389.7] / 104.5 |
| Step 30 | Connect the potentiometer's red wire to (+) red. | NAUO34 (Potentiometer) from [0.0, 18.0, 0.0], 1 stage(s) | - | pot red 44/47->47 | [-0.233, 0.758, 0.609] / [697.9, 915.6, 1338.8] / 41.7 |
| Step 31 | Connect the potentiometer's tan wire to a5. | NAUO33 (Potentiometer) from [0.0, 18.0, 0.0], 1 stage(s) | - | pot tan 45/48->48 | [-0.233, 0.758, 0.609] / [697.9, 915.6, 1338.8] / 41.7 |
| Step 32 | Connect the potentiometer's black wire to (-) blue. | NAUO14 (Potentiometer) from [0.0, 5.0, 0.0], 1 stage(s) | - | pot black 46/49->49 | [-0.233, 0.758, 0.609] / [697.9, 915.6, 1338.8] / 41.7 |
| Step 33 | Lay the alarm buzzer beside the base, past the end of the breadboard.  | NAUO58 (Alarm Buzzer) from t[-51.3, -2.0, 68.6] r120.0deg, 4 stage(s) | NAUO62 (Alarm Buzzer) on NAUO2: appears -> t[-0.4, -12.8, 176.1] r120.0deg; NAUO59 (Alarm Buzzer) on NAUO62: appears -> [-21.7, -45.9, -107.7] | buzzer red None/50->52 via [52]; buzzer black None/51->51 | [-0.396, 0.76, 0.516] / [656.1, 910.4, 1382.1] / 47.0 |
| Step 34 | Connect the buzzer's black wire to (-) blue. | NAUO59 (Alarm Buzzer) from t[-89.4, -2.0, 57.7] r120.0deg, 2 stage(s) | - | buzzer black 51/51->53 via [53] | [-0.396, 0.76, 0.516] / [656.1, 910.4, 1382.1] / 47.0 |
| Step 35 | Lay the LCD screen face down beside the base. Then peel four wires off | - | NAUO94 (LCD Screen) on NAUO2: appears -> t[-8.0, -38.6, 79.2] r180.0deg; NAUO82 (Breadboard Wire (M-F)) on NAUO1: appears -> t[33.8, -15.6, -78.0] r90.0deg; NAUO84 (Breadboard Wire (M-F)) on NAUO1: appears -> t[43.3, -15.6, -83.1] r90.0deg; NAUO86 (Breadboard Wire (M-F)) on NAUO1: appears -> t[60.4, -15.6, -112.3] r90.0deg; NAUO93 (Breadboard Wire (M-F)) on NAUO1: appears -> t[67.3, -15.6, -109.8] ... | lcd purple None/54->54; lcd yellow None/55->58; lcd teal None/56->59; lcd blue None/57->60 | [0.62, 0.62, 0.48] / [700.0, 905.0, 1330.0] / 125.0 |
| Step 36 | Connect the purple wire from GND on the LCD screen to (-) blue. | NAUO82 (Breadboard Wire (M-F)) from [0.0, 18.0, 0.0], 1 stage(s) | NAUO97 (Breadboard Wire (M-F)) on NAUO94: [27.8, -27.3, 109.7] -> [0.0, 0.0, 0.0] | lcd purple 54/61->62 | [0.62, 0.62, 0.48] / [716.1, 905.9, 1333.8] / 68.4 |
| Step 37 | Connect the yellow wire from VCC on the LCD screen to (+) red. | NAUO84 (Breadboard Wire (M-F)) from [0.0, 18.0, 0.0], 1 stage(s) | NAUO98 (Breadboard Wire (M-F)) on NAUO94: appears -> [0.0, 0.0, 0.0] | lcd purple 62/63->63; lcd yellow None/64->65 | [0.62, 0.62, 0.48] / [718.3, 905.9, 1333.8] / 69.9 |
| Step 38 | Connect the teal wire from SDA on the LCD screen to b8. | NAUO86 (Breadboard Wire (M-F)) from [0.0, 18.0, 0.0], 1 stage(s) | NAUO99 (Breadboard Wire (M-F)) on NAUO94: appears -> [0.0, 0.0, 0.0] | lcd yellow 65/66->66; lcd teal None/67->68 | [0.343, 0.766, 0.544] / [716.8, 905.9, 1337.3] / 70.1 |
| Step 39 | Connect the blue wire from SCL on the LCD screen to b9. | NAUO93 (Breadboard Wire (M-F)) from [0.0, 18.0, 0.0], 1 stage(s) | NAUO100 (Breadboard Wire (M-F)) on NAUO94: appears -> [0.0, 0.0, 0.0] | lcd teal 68/69->69; lcd blue None/70->71 | [0.62, 0.62, 0.48] / [720.4, 905.9, 1337.3] / 71.9 |
| Step 40 | Plug the USB cable's small end into the Nano Board's USB socket, the c | NAUO122 (USB Cable) from [0.0, 0.0, 18.0], 1 stage(s) | - | lcd blue 71/72->72; usb cable None/73->74 | [-0.451, 0.451, 0.771] / [672.0, 906.0, 1352.0] / 32.0 |
| Step 41 | Push the two F7s down into the slots in F3 by the end of the breadboar | - | NAUO42 (F7) on NAUO2: appears -> [0.0, 0.0, 0.0]; NAUO43 (F7) on NAUO2: appears -> [0.0, 0.0, 0.0] | - | [0.549, 0.549, -0.629] / [678.0, 948.0, 1262.0] / 110.0 |
| Step 42 | Spread the tops of the two F7s apart. | - | NAUO42 (F7) on NAUO2: [0.0, 0.0, 0.0] -> t[0.0, 0.0, 0.0] r15.0deg; NAUO43 (F7) on NAUO2: [0.0, 0.0, 0.0] -> t[0.0, 0.0, 0.0] r-15.0deg | - | [0.549, 0.549, -0.629] / [690.0, 915.0, 1270.0] / 110.0 |
| Step 43 | Lower the buzzer in between the two F7s, its ears into their slots. | NAUO62 (Alarm Buzzer) from t[-0.4, -12.8, 176.1] r120.0deg, 3 stage(s) | - | buzzer red 52/52->79 via [75, 76]; buzzer black 53/53->80 via [77, 78] | [0.549, 0.549, -0.629] / [690.0, 915.0, 1270.0] / 110.0 |
| Step 44 | Let go of the two F7s, so that they close on the buzzer. | - | NAUO42 (F7) on NAUO2: t[0.0, 0.0, 0.0] r15.0deg -> [0.0, 0.0, 0.0]; NAUO43 (F7) on NAUO2: t[0.0, 0.0, 0.0] r-15.0deg -> [0.0, 0.0, 0.0] | - | [0.549, 0.549, -0.629] / [690.0, 915.0, 1270.0] / 110.0 |
| Step 45 | Tip F9 towards the front and hook its front foot into its slot in F3 b | - | NAUO45 (F9) on NAUO2: appears -> t[0.0, 0.0, 0.0] r25.8deg +1 via | - | [0.529, 0.663, 0.53] / [735.0, 920.0, 1340.0] / 114.5 |
| Step 46 | Swing F9 upright, pressing its back foot down into its slot in F3. | - | NAUO45 (F9) on NAUO2: t[0.0, 0.0, 0.0] r25.8deg -> [0.0, 0.0, 0.0] | - | [0.529, 0.663, 0.53] / [735.0, 920.0, 1340.0] / 114.5 |
| Step 47 | Move F1, still face down, further out in front of the case and along t | - | NAUO11 (Potentiometer) on NAUO2: t[79.0, -10.4, 99.6] r-90.0deg -> t[136.0, -10.4, 14.6] r-90.0deg; NAUO10 (F1) on NAUO2: t[79.0, -10.4, 99.6] r-90.0deg -> t[136.0, -10.4, 14.6] r-90.0deg | pot red 47/47->81; pot tan 48/48->82; pot black 49/49->83 | [0.55, 0.62, 0.56] / [792.7, 919.5, 1347.0] / 166.9 |
| Step 48 | Lift F4, with the switch, over the frame. | - | F4 (F4) on NAUO2: [-82.7, 17.3, -0.1] -> [0.0, 49.8, -0.2] | switch red 30/30->84 via [84]; switch tan 31/31->85 via [85]; switch black 32/32->86 via [86] | [0.549, 0.549, -0.629] / [690.0, 915.0, 1270.0] / 110.0 |
| Step 49 | Lower F4 onto the tabs of the F7s and F9. | F4 (F4) from [0.0, 49.8, -0.2], 1 stage(s) | - | switch red 84/84->87; switch tan 85/85->88; switch black 86/86->89 | [0.549, 0.549, -0.629] / [690.0, 915.0, 1270.0] / 110.0 |
| Step 50 | Slide F8 into the slots in F4 and F3 from the front. | NAUO44 (F8) from [94.0, 0.0, 0.0], 1 stage(s) | - | - | [0.45, 0.539, 0.712] / [703.9, 927.3, 1307.0] / 97.1 |
| Step 51 | Stand the LCD screen up in front of the case, face to the front. Then  | - | NAUO94 (LCD Screen) on NAUO2: t[-8.0, -38.6, 79.2] r180.0deg -> t[0.0, 0.0, 0.0] r14.0deg +3 via | lcd purple 63/90->106 via [94, 95, 96]; lcd yellow 66/91->107 via [97, 98, 99]; lcd teal 69/92->108 via [100, 101, 102]; lcd blue 72/93->109 via [103, 104, 105] | [0.62, 0.62, 0.48] / [736.7, 938.8, 1396.5] / 100.0 |
| Step 52 | Straighten the LCD screen, pushing it on through the slots in F8, then | NAUO94 (LCD Screen) from t[0.0, 0.0, 0.0] r14.0deg, 5 stage(s) | - | lcd purple 106/106->114 via [110]; lcd yellow 107/107->115 via [111]; lcd teal 108/108->116 via [112]; lcd blue 109/109->117 via [113] | [0.62, 0.62, 0.48] / [705.0, 915.0, 1320.0] / 110.0 |
| Step 53 | Stand F1 up in front of the case, the knob on the outside. | - | NAUO11 (Potentiometer) on NAUO2: t[136.0, -10.4, 14.6] r-90.0deg -> [76.7, 0.0, 1.1]; NAUO10 (F1) on NAUO2: t[136.0, -10.4, 14.6] r-90.0deg -> [76.7, 0.0, 1.1] | pot red 81/81->118; pot tan 82/82->119; pot black 83/83->120 | [0.62, 0.55, -0.56] / [720.0, 915.0, 1270.0] / 120.0 |
| Step 54 | Push F1 onto the tabs of F4 and F3. | NAUO10 (F1) from [76.7, 0.0, 1.1], 1 stage(s); NAUO11 (Potentiometer) from [76.7, 0.0, 1.1], 1 stage(s) | - | pot red 118/118->121; pot tan 119/119->122; pot black 120/120->123 | [0.62, 0.55, -0.56] / [720.0, 915.0, 1270.0] / 120.0 |
| Step 55 | Push F5 onto the end of the case by the breadboard: the tabs of F1, F3 | F5 (F5) from [0.0, 0.0, 56.0], 1 stage(s) | - | - | [0.816, 0.398, 0.418] / [683.0, 919.0, 1320.0] / 115.0 |
| Step 56 | Turn the case so its back faces you. Hook the tabs at the slit end of  | F2 (F2) from t[-44.8, 0.0, -13.2] r20.0deg, 3 stage(s) | - | usb cable 74/74->125 via [74, 124] | [-0.704, 0.502, -0.502] / [640.0, 915.0, 1290.0] / 125.0 |
| Step 57 | Push F6 onto the other end of the case: the tabs of F1, F2, F3 and F4  | F6 (F6) from [0.0, 0.0, -67.5], 1 stage(s) | - | - | [0.5, 0.55, -0.669] / [683.0, 919.0, 1250.0] / 110.0 |

## 3. The published take-apart, step by step, on our model

Published: what comes off, its cue (arrow length x shaft width, mm, measured from the payload; eye; inset), and its camera in our terms
(dir / target / radius; "rolled" = scene up-axis turned, which we cannot copy). Ours: the ids and wire ids, the Full Build step(s) it
undoes with their camera, how the Full Build brought the part in, and what is true of our model at that point.

| pub | published: what, cue | published camera (ours) | our ids | our wires | undoes (ours) and its camera | how ours came in / notes |
|---|---|---|---|---|---|---|
| 1 | F6 out -Z 67.5 mm, fade; arrow 56.1 x 4.87 -Z | [0.588, 0.588, -0.556] / [633.2, 830.5, 1316.6] / 155.7 (= build 57's) | F6 | - | 57: [0.5, 0.55, -0.669] / [683, 919, 1250] / 110 | path [0, 0, -67.5] -> 0: `remove()` default (way, camera) |
| 2 | F2 tilts ~21 deg about an edge, slides 78 mm (-X, -Z), fade; arrow 79.8 x 5.51 -X; eye on the USB cable where it passes F2's slit | [-0.479, 0.663, 0.576] / [694.1, 892.3, 1270.6] / 155.7, rolled | F2 | usb cable 125 | 56: [-0.704, 0.502, -0.502] / [640, 915, 1290] / 125 (from the back) | path in 3 stages: swung 20 deg about the hinge at F5's inside (641.63, 919.5, 1366.07), 4.8 / 13.2 mm short of F5, 40 mm out: `remove()` default reverses it (swing open, unhook, pull -X). The cable: 56c `wire_via` [74, 124] -> 125, so `wire_via={'usb cable': [R124, R74]}`, `wires={'usb cable': R74}` puts it back as it lay before F2 (or leave 125: nothing is in its way once F2 is off). Our Step 56c has a close-up of the cable in the slit (inset, target [643.13, 899.6, 1339.4]) |
| 3 | F5 out +Z 56 mm, fade; arrow 64.6 x 6.19 +Z | [0.596, 0.499, 0.629] / [688.4, 888.4, 1297.7] / 133.5 | F5 | - | 55: [0.816, 0.398, 0.418] / [683, 919, 1320] / 115 | path [0, 0, 56] -> 0: default |
| 4 | F1 pulled forward +X (cross-fade to the "pulled forward" copy, pot, knob, nut and the 3 pot wires with it, stretched); arrow 79.0 x 5.78 +X at F1's lower edge | [0.605, 0.664, -0.440] / [706.6, 874.3, 1253.3] / 133.5 | F1 NAUO10, POT NAUO11 (knob, nut, washer ride on it) | pot red / tan / black 121-123 -> 118-120 | 54: [0.62, 0.55, -0.56] / [720, 915, 1270] / 120 | path [76.7, 0, 1.1] -> 0 (F1 and pot together): `lift([F1, POT])` default way and camera; the pot then rides on F1. Give `wires=` Step 54's routes 118-120 (lift() does not change routes by itself) |
| 5 | F1 laid aside (cross-fade to the copy at the far end, F1-4 = the published build 47's place); eye on F1 | same as 4 | F1 (pot riding) | pot 118-120 -> 81-83 | 53 (ride FRONT_OUT <- F1_ASIDE): [0.62, 0.55, -0.56] / [720, 915, 1270] / 120 | a ride: `lift([F1], to=VIEW['Step 53']['carry'][F1]['pose'])` (face down, `t [135.97, -10.43, 14.63]`, -90 deg about z at F1's middle), `wires=` Step 53's 81-83, camera by hand. Ours lies face down (knob down); the published F1-4 lies face up |
| 6 | LCD out of F9's notches, swung out, laid face down front-left, still wired (3 cross-fades of 1600 ms); eye on the LCD; inset of F9's notches, 2 red boxes | [0.698, 0.495, 0.519] / [670.6, 875.2, 1275.4] / 155.7 | LCD NAUO94 (female caps NAUO97-100 ride on it) | lcd purple / yellow / teal / blue 114-117 -> 90-93 | 52 (path, 2 stages: back 14.9 mm out of F9's notches toward F8, then turned 14 deg): [0.62, 0.62, 0.48] / [705, 915, 1320] / 110; 51 (ride, 4 stages: lying -> on end -> 20 mm out in front -> in, angled): [0.62, 0.62, 0.48] / [736.7, 938.8, 1396.5] / 100 | `lift([LCD])` default = 52 reversed only (it ends angled inside the case). For the whole way: path = 52 reversed + 51's ride stops reversed (`VIEW['Step 51c']['carry'][LCD]` via, then Step 51's pose = LCD_LYING), `wire_via` per wire = [110, 106, 96, 95, 94] (purple; yellow 111, 107, 99, 98, 97; teal 112, 108, 102, 101, 100; blue 113, 109, 105, 104, 103), `wires` = 90 / 91 / 92 / 93 (6 stages, 5 via + last). Or two steps (52, then 51), each by its own camera, as the PMG's displays. Inset: Step 52c's (F9's two notches, `marks`) |
| 7 | F8 out +X 94 mm, fade; arrow 83.9 x 4.51 +X | [0.512, 0.697, -0.502] / [689.6, 889.4, 1273.7] / 114.5 | F8 NAUO44 | - | 50: [0.45, 0.539, 0.712] / [703.9, 927.3, 1307] / 97.1 | path [94, 0, 0] -> 0: default |
| 8 | F4 with the switch and its 3 wires lifted, then set down flat (cross-fades to F4-3 then F4-2 = the build's flat copy); arrow 73.2 x 3.35 +Y | [0.697, 0.551, -0.460] / [678.6, 923.4, 1294.9] / 114.5 | F4 (switch NAUO46 rides on it) | switch red / tan / black 87-89 -> 84-86 -> 30-32 | 49 (path [0, 49.8, -0.2] -> 0) + 48 (ride FLAT_F4 [-82.7, 17.3, -0.1] -> over the frame): CASE_CAMERA [0.549, 0.549, -0.629] / [690, 915, 1270] / 110 (both) | `lift([F4], path=[[0, 49.8, -0.2], [-82.7, 17.3, -0.1]], wire_via={sw: [84 / 85 / 86]}, wires={sw: 30 / 31 / 32})`: the Full Build's two steps in one, 2 stages. The switch's caps stay plugged (they are seated, not riding) |
| 9-11 | unplug the pot's black, tan, red wires (eye on each plug); each then hangs straight down from the pot | [0.684, 0.697, -0.215] / [644.9, 867.8, 1241.9] / 155.7 | caps NAUO14 (black), NAUO33 (tan), NAUO34 (red) | pot black / tan / red | 32, 31, 30 (paths [0, 5, 0] / [0, 18, 0] / [0, 18, 0] -> 0; each cap rode on the pot): POT_CAMERA [-0.233, 0.758, 0.609] / [697.9, 915.6, 1338.8] / 41.7 | `unplug()` default takes Step 30-32's routes 47-49, **drawn with F1 face down beside the breadboard's end (F1_DOWN, Step 29c), not where our F1 lies now (Step 47 moved it 57 mm out and 85 mm along: routes 81-83)**; and in the published order the pot tan and red pass through the seated buzzer's black lead (section 4.2). See section 4.2 for the way that is clear |
| 12 | isolated: F1 + pot + knob + the 3 hanging wires (nut, washer shown); knob pulled off along the shaft; arrow 41.2 x 2.93 | [-0.566, 0.611, -0.554] / [736.9, 889.0, 1101.5] / 98.1, rolled | KNOB NAUO13 (rides on the pot) | - | 28 (ride, on the pot [60, 0, 0] -> 0): BUILD_LOOK [0.35, 0.451, -0.821] / [822, 960, 1375] / 98 (F1 upright at BUILD [100, 35, 100]) | not known to the generator: `remove([KNOB], path=[compose(where(POT), [60, 0, 0], g._pivot(KNOB))])`, `alone=`, camera by hand. Needs F1 upright first (ours lies face down, knob under it): section 4.3 |
| 13 | nut off; arrow 56.5 x 3.72 | same, rolled | NUT NAUO12 | - | 27 (ride: [60, 0, 0] -> 0 in two turns, 7 via poses): BUILD_LOOK | path by hand: `VIEW['Step 27c']['carry'][NUT]['via']` reversed, then `VIEW['Step 27']['carry'][NUT]['pose']`, each composed with where(POT); via() between stops (the LSM's NUT_WAY: a stop a turn) |
| 14 | washer off; arrow 70.6 x 2.89 | same, rolled | WASHER NAUO146 | - | 26 (ride [60, 0, 0] -> 0): BUILD_LOOK | path by hand, as the knob's |
| 15 | pot pushed out of the back of F1 (with its 3 wires), stays on screen; arrow 52.7 x 4.21 | [-0.562, -0.402, -0.723] / [734.8, 913.9, 1100.0] / 98.1, from below, rolled | POT (its 3 caps riding, once unplugged) | pot red / tan / black go with it | 25 (ride: pot [21, 35, 100] -> [100, 35, 100], i.e. 79 mm through F1 from behind): BUILD_LOOK; Step 25c inset (the pot's tab in F1's slot) | `remove([POT], path=[compose(where(F1), [-79, 0, 0], g._pivot(POT))])`: its caps ride on it, so both ends of each lead go and the leads go with it. Then `put_away([F1])` |
| 16-18 | washer, nut, knob put back on the loose pot for storage (lead lines) | [-0.654, 0.459, -0.601] / [776.8, 801.9, 1099.3] / 98.1, rolled | - | - | (22-24 redone) | **dropped**: Lee, 17 Oct 2026, a part once off is gone, never refitted |
| 19-22 | unplug the LCD wires GND (purple), VCC (yellow), SDA (teal), SCL (blue): label with the pin name at the LCD header, eye on the breadboard plug; the routed wire becomes a straight loose wire beside the base and fades | [0.655, 0.733, 0.185] / [666.0, 854.6, 1330.6] / 114.5 | males NAUO82 / 84 / 86 / 93, females NAUO97 / 98 / 99 / 100 | lcd purple / yellow / teal / blue (90-93) | 36-39 (male: path [0, 18, 0] -> 0, rode on the breadboard; female: ride on the LCD [0, 0, 15] -> 0): [0.62, 0.62, 0.48] / [716.1 - 720.4, 905.9, 1333.8 - 1337.3] / 68.4 - 71.9 (38: [0.343, 0.766, 0.544]) | one `remove([male, female])` per wire: the male's way is known (default, its step's camera); the female's is not: `paths={female: [compose(where(LCD), [0, 0, 15], g._pivot(female))]}` (off its pin, as the Full Build held it). The lead goes with both ends. In this (published, = build) order no male passes through another wire **once the buzzer lies outside again**; with the buzzer still seated, GND's passes through the buzzer's black lead (section 4.2). The reverse order (SCL first) does not clear (blue through purple 0.13 mm) |
| 23 | the free LCD taken away (eye; fade, no motion) | same | LCD (lying) | - | (35 laid it there; no move to undo) | `remove([LCD], path=[shifted up 30], arrows=[], eye=[LCD])`: it is off its seat, so the generator would lift it straight up with a Review note; in-house a part leaves by a move, then fades |
| 24 | F9 unhooked: tilts about its foot, then shifts 33 mm still tilted, fade; arrow 33.8 x 3.3 +Y; inset of F9's foot hooked in F3 (1 red box) | [0.565, 0.580, 0.587] / [647.2, 893.0, 1296.5] / 114.5 | F9 NAUO45 (rides on F3) | - | 46 (ride: swung upright from tilted 25.79 deg about its front foot (720.13, 887.54, 1355.78)) + 45 (ride: in over its slots at [0, 35.3, 0], tipped in through a via 33 mm up): [0.529, 0.663, 0.53] / [735, 920, 1340] / 114.5 (both) | not known to the generator: path by hand from steps.json, so it follows Step 45 as Lee changes it: `[VIEW['Step 46']['carry'][F9]['pose'], VIEW['Step 45c']['carry'][F9]['via'][0], VIEW['Step 45']['carry'][F9]['pose']]` (swing back to tilted, lift 33 mm tilted, upright at 35.3 mm; or stop tilted, as the published). Inset: Step 45c's (target [716.0, 885.5, 1355.8], F3 ghosted 0.25, mark 3). Arrows in turn (`then=`) for the swing and the lift |
| 25 | USB cable unplugged +Z with its right-angle plug, fade; arrow 63.5 x 5.78 +Z; eye on the cable | same as 24 | USB_B NAUO122, USB_A | usb cable | 40 (path [0, 0, 18] -> 0): [-0.451, 0.451, 0.771] / [672, 906, 1352] / 32 | `remove([USB_B, USB_A], units=[[USB_B]])`: USB_B default; USB_A rests off its seat (a turned pose): give it a way, shifted from where(USB_A) (**not** an absolute `[0, 30, 0]` as the PMG's, whose A end was in its seat). Step 40's camera is close (r 32): widen it so the cable shows (the RCC's, PMG's). In-house: earlier (section 4.6) |
| 26 | the two F7 tops spread apart (two opposed arrows 36.9 x 3.75 -X and 40.5 x 3.8 +X); they stay | [0.713, 0.580, 0.394] / [644.2, 892.6, 1291.2] / 114.5 (held to 34) | F7A NAUO42, F7B NAUO43 (ride on F3) | - | 44 (ride: TILT -> 0) and 42 (ride 0 -> TILT: +15 deg about z at (657.33, 887.61, 1233.2) for F7A, -15 deg at (693.18, 887.61, 1233.2) for F7B): CASE_CAMERA | `lift([F7A, F7B], paths={F7A: [TILT_A], F7B: [TILT_B]}, ride_on=F3)` (poses from `VIEW['Step 42c']['carry']`; ride_on so that F7B does not ride on F7A afterwards); two arrows; camera by hand |
| 27 | buzzer slid out +Z from between the F7s, then (cross-fade) lying front-left, still wired; arrow 58.3 x 6.15 +Z, eye on the buzzer | same | BUZZER NAUO62 | buzzer red / black 79 / 80 -> 52 / 53 | 43 (path: lying -> lifted 60 -> 75 mm over its seat -> 0; 43c wire_via red [75, 76], black [77, 78]): CASE_CAMERA | `lift([BUZZER], wire_via={'buzzer red': [R76, R75], 'buzzer black': [R78, R77]}, wires={'buzzer red': R52, 'buzzer black': R53})` (the PMG's lifted_back): the default way, up 75 mm and over the board to lie past the breadboard's end at the back. Ours goes up, not out along +Z |
| 28 | both F7s straightened, then lifted 44 mm, fade; two arrows 37.3 / 34.2 x 3.96 +Y | same | F7A, F7B | - | 42 + 41 (ride [0, 80, 0] -> 0) | `remove([F7A, F7B], paths={i: [ZERO, [0, 80, 0]] ...})` (straighten, then up: 2 stages; `then=` arrows for the lift); camera Step 41's by hand ([0.549, 0.549, -0.629] / [678, 948, 1262] / 110) |
| 29 | unplug the buzzer's red lead (eye); it is left sticking up from the buzzer | same | cap NAUO58 | buzzer red | 33 (path: from lying beside the buzzer, 4 stages): BUZZER_CAMERA [-0.396, 0.76, 0.516] / [656.1, 910.4, 1382.1] / 47 | `unplug([NAUO58], ride_on=BUZZER)`: default way (back to lying beside the buzzer, its route 50 as before Step 33) and camera; **ride_on is needed** (the cap rode on nothing before Step 33) |
| 30 | unplug the buzzer's black lead (eye) | same | cap NAUO59 | buzzer black | 34 (path from lying -> [0, 18, 0] -> 0; rode on the buzzer): BUZZER_CAMERA | `unplug([NAUO59])` default (route 51). Either order is clear (section 4.2); ours reversed would be black, then red. Or both in one step |
| 31 | buzzer taken away (eye; fade, no motion) | same | BUZZER (+ its 2 caps riding) | buzzer red / black go | (33 laid it there) | `remove([BUZZER], path=[shifted up 30], arrows=[], eye=[BUZZER])` |
| 32-34 | unplug the switch's black, tan, red wires (eye on each plug); each then hangs straight down below F4 | same | caps NAUO48 (black), NAUO49 (tan), NAUO47 (red) | switch black / tan / red (30-32) | 18, 17, 16 (paths [0, 5, 0] / [0, 18, 0] -> 0; rode on the switch): SWITCH_CAMERA [0.401, 0.615, -0.679] / [643.7, 917.7, 1281.1] / 45.2 | `unplug()` default works: routes 30-32 are drawn with F4 flat, where it lies again. To hang them as published and as before Step 16 (Step 15c), give paths ending at the hanging poses (`VIEW['Step 15c']['carry'][cap]`, on the switch), `wire_via` [30 / 31 / 32] and `wires` 27 / 28 / 29, `ride_on=SWITCH`, camera by hand. All three orders clear |
| 35 | isolated: F4 + switch + 3 hanging wires; switch pushed up out of F4, 85 mm, stays; arrow 63.6 x 4.95 +Y | [0.666, 0.422, -0.615] / [561.0, 962.0, 1282.8] / 98.1 | SWITCH (+ its 3 caps riding) | switch leads go with it | 15 (ride: on F4 [0, 50, 0] -> 0): [0.451, 0.752, -0.481] / [596.8, 977.3, 1258.3] / 62 | `remove([SWITCH], path=[compose(where(F4), [0, 50, 0], g._pivot(SWITCH))], alone=[F4, SWITCH])`, camera Step 15's by hand; then `put_away([F4])` |
| 36-43 | unplug one jumper each: white (36), maroon = our dark_red (37), purple (38), blue (39), green (40; frames misnamed "41" + a duplicate), black (41), orange (42), yellow (43); eye on one plug; routed -> loose beside the base -> fade | [0.566, 0.715, 0.410] / [672.4, 860.9, 1291.8] / 98.1 (held 36 - 47) | caps: white NAUO28 + NAUO15, dark_red NAUO30 + NAUO31, purple NAUO25 + NAUO26, blue NAUO22 + NAUO21, green NAUO20 + NAUO19, black NAUO16 + NAUO17, orange NAUO53 + NAUO52, yellow NAUO56 + NAUO55 | jumper white / dark_red / purple / blue / green / black / orange / yellow | 13, 14, 11, 12, 10, 9, 20, 21: cameras [0.497, 0.819, -0.287] (14: [0.369, 0.819, -0.439]; 20: [0.299, 0.906, -0.299]; 21: [0.433, 0.866, -0.25]), radius 26 - 44 | `remove([cap_a, cap_b], arrows=[], eye=[cap])` each: default ways (up 18; white and dark red up 5 then out 14 mm) and cameras. **In the published order purple, blue and green lift through orange** (section 4.4): take orange and yellow first |
| 44 | RTC + coin cell up +Y 22 mm, fade; arrow 29.8 x 3.55 | same | RTC NAUO3, COIN NAUO4 | - | 7 (path [0, 34, 0] -> 0): [0.579, 0.574, -0.579] / [660, 934, 1290] / 52 | default (one arrow: the two touch) |
| 45 | resistor 1 (h27) up 52 mm, fade; arrow 39.4 x 3.47 (frame misnamed "Step 45c") | same | RES1 NAUO6 | res1 leg 1 / 2 go with it | 5 (path [0, 37, 0] -> 0): [0.579, 0.574, -0.579] / [682.7, 918, 1276.7] / 32 | default |
| 46 | resistor 2 (h29) up 51 mm; arrow 46.8 x 3.96 | same | RES2 NAUO7 | res2 legs | 6: same dir / [682.7, 918, 1271.6] / 32 | default |
| 47 | Nano up 55 mm; arrow 64.2 x 3.72 | same | NANO | - | 3 (path [0, 40, 0] -> 0): [0.579, 0.574, -0.579] / [676.5, 916, 1324.3] / 50 | default (the USB plug must be out by then) |
| end | Completed View: F3 with the breadboard stuck on | [0.495, 0.763, 0.415] / [678.1, 853.2, 1292.7] / 84.1 | F3 NAUO2, BREADBOARD NAUO1 | - | (1, 2: never undone) | the generator frames what is left, closer in; then the Full Build's parts list (`take_apart(parts_list_at_end=True)`, as the MRA's, PMG's, LSM's) |

## 4. Where our Full Build differs from the published one, in ways the take-apart feels

### 4.1 F1 and where it lies
Published: F1 pulled forward (F1-2, the same 76.7 mm as our FRONT_OUT), then laid **face up beyond the -z end** (F1-4, its build 47's
place); the pot is stripped there, in an isolated scene with the camera rolled so the panel stands up. Ours: Step 29 laid F1 **face
down** in front of the breadboard's end (F1_DOWN, `t [78.97, -10.43, 99.63]`, -90 deg about z at F1's middle (722.33, 919.53,
1289.87)), the pot's leads were plugged in there (30 - 32, routes 47-49), Step 47 moved it, still face down, 57 mm further out and 85 mm
towards the -z end (F1_ASIDE, `t [135.97, -10.43, 14.63]`; routes 81-83) out of the LCD's way, Step 53 stood it up in front (FRONT_OUT
[76.7, 0, 1.1]; 118-120), Step 54 pushed it on (121-123). The knob, nut and washer came off and went back on with F1 **upright in the
air** at BUILD [100, 35, 100] (Steps 25 - 28, camera BUILD_LOOK); before that the pot was on its own at BUILD + [-79, 0, 0] (22 - 24,
POT_ALONE). Face down, our knob points at the table: the strip-down needs F1 turned up again.

### 4.2 Leads: what each unplug passes through (scripts/lead_order.py)
Each lead was moved as `unplug()` would move it (its plug straight out of its hole, the first stage of its Full Build way, reversed;
the lead blended along its length as player.js does), against every other lead still in at that point, each drawn as it lies there.
"Passes" = centre lines closer than 1.25 mm (two radii) and closer than they lie at rest.

- **Pot leads with F1 where our take-apart leaves it (face down aside, routes 81-83)**: black (up 5) touches red (1.09 mm), tan (up 18)
  passes through red (0.23), the LCD's yellow (0.19) and purple (1.17), the buzzer's black (0.92), the switch's tan (0.47) and the purple
  jumper (1.08); red passes through the buzzer's black (0.36). With the LCD wires and buzzer leads out first, tan still passes through
  red, the switch's tan and the purple jumper; holding every cap only 5 mm up does not clear it (black 1.09 to red). These are the
  Full Build's Step 47 shapes (long leads, `stretch`, no `b_from`), never drawn to have a plug moved.
- **Pot leads with F1 moved back beside the breadboard's end first (Step 47 undone: routes 47-49, Step 30 - 32's own)**: clear, once
  the buzzer lies outside the case again (its leads 52 / 53). With the buzzer still seated (published order) tan and red pass through
  its black lead (0.52, 0.20).
- **LCD wires (male up 18), the LCD lying**: in the published (= build) order GND, VCC, SDA, SCL all clear **once the buzzer lies
  outside again**; with the buzzer still seated, GND's passes through the buzzer's black lead (0.15). In the reverse order SCL passes
  through purple (0.13), yellow (0.23) and teal (0.30), SDA and VCC likewise: keep the published order (or take all four at once).
- **Buzzer leads** (buzzer lying, 52 / 53): red first (up 5, its Full Build hold) or black first (up 18): both clear.
- **Switch leads** (F4 flat, 30-32): black, tan, red (published = our Full Build reversed): clear, with every jumper still in.
So the published order works in our model only if the buzzer comes out of the F7s (published 26 - 28) **before** the pot and LCD
wires (published 9 - 11, 19 - 22), and F1 goes back beside the breadboard's end before its leads are unplugged.

### 4.3 The potentiometer's strip-down
The published strips it on F1 lying face up, isolated, then refits the washer, nut and knob for storage (16 - 18: dropped in-house).
Ours, to use the Full Build's own poses, routes and cameras: (1) unplug the three caps on a two-stage way, out of the hole (Step 30 - 32
reversed) and on to where each lay before Step 30, straight out from its pin (`VIEW['Step 29c']['carry'][cap]['pose']`, on the pot),
`wire_via` = Step 30 - 32's routes 47 / 48 / 49, `wires` = Step 29c's 44 / 45 / 46 (drawn for F1 at F1_DOWN), `ride_on=POT`; (2) `lift([F1],
to=[100, 35, 100])` (Step 29 reversed; the pot rides on F1, its caps on the pot), `wires` = Step 29's 41 / 42 / 43, `alone=[F1, POT, KNOB,
NUT, WASHER]` (the caps come as riders), camera Step 29's; (3) knob, nut, washer off (28, 27, 26 reversed, BUILD_LOOK); (4) the pot out of
the back of F1 (25 reversed), its leads with it; `put_away([F1])`. Without (1)'s second stage the caps would hang over their holes
relative to the pot and be swung up into the air with F1 in (2). Alternative: leave F1 face down and use `flip=True` with `alone=` (the
model turned over, so the knob points up as on the published isolated F1-4): fewer steps, no Full Build camera to reuse, and the
caps' and leads' shapes in that view are untested.

### 4.4 Breadboard jumpers (scripts/jumper_order.py)
Each jumper lifted the Full Build's way reversed (both caps; white and dark red up 5, then out 14 mm sideways), against the others
still in: orange (Step 20) lies over purple, blue and green (Steps 11, 12, 10), which went in before it. **In the published order
(orange and yellow last) purple passes through orange (0.98 mm, at rest 3.76), blue through orange (1.14) and green through orange
(1.15).** Orange and yellow pass within 0.95 of each other either way round (they lie 1.32 apart: the same contact the Full Build's
Step 21 makes coming down). Purple before blue (published) is cleaner than blue before purple (0.78, the contact the Full Build's
Step 12 already makes). White before dark red and dark red before white both clear. So: orange and yellow first, then the published
order (white, dark red, purple, blue, green, black); or all eight at once (Lee's "the breadboard wires" groups: MRA, PMG, LSM), when
nothing passes through anything.

### 4.5 The buzzer, the F7s and F9
- Published 27 slides the buzzer out along +Z between the spread F7s and cross-fades it to lying front-left. Ours (Step 43 reversed):
  up 75 mm, over the board to 60 mm above where it lies, down to lie past the breadboard's end at the back (x about 663 - 687, beside
  F9's x 689 - 720: clear by about 2 mm by the boxes; not tested by the generator, which skips ways that turn). Its leads go back
  through the Full Build's own stages (43c wire_via).
- The F7s ride on F3 (ride steps 41, 42, 44): spread, straighten and lift all need poses by hand (from `VIEW['Step 42c']['carry']` and
  Step 41's [0, 80, 0]). Published spread is 15 deg as ours.
- F9 rides on F3 (45, 46, as changed in 61c6efc: in over its slots, tipped in, swung upright). Its way out reversed is the published
  one: swing back to tilted about the front foot, then 33 mm up still tilted. Read the poses from steps.json, not copied, since Lee is
  still changing Step 45.

### 4.6 The USB cable and power
Published: unplugged at 25 (after F9). In-house the power cable comes first (MRA, RCC, PMG); where the box closes round the plug, Step
1's caution says to disconnect it from the computer (the LSM's). Ours: the plug (in the Nano's socket at column 1, centred near x 676.5, where the published
arrow starts; the cable leaves its right-angle body at x 659.3, z 1354.4: route 74's first point) leaves +Z 18 mm (Step 40 reversed), which F5 (z 1366 - 1369) blocks and F2 (the cable in its slit) holds: it can come
out as soon as F6, F2 and F5 are off, i.e. **our Step 4**, if its way clears F9 (box x 689.1 - 720.3, z 1354.3 - 1357.3, docs/research/lac/scripts/round2/f9/f9check_out.txt: the plug, x below
about 685, passes beside it by the boxes; `_takeoff()` tests this straight way against everything still seated and logs "passes through a part
still there" if not). Else after F9, as published. Step 1's caution in either case.

### 4.7 The LCD
Ours came in through two Full Build steps, both with their wires' shapes per stage (51: a ride in 4 stages with `wire_via`; 52: a path
in 2 stages with `wire_via`), so its way out is fully known except that the generator knows only Step 52's half (section 3, pub 6). The
male caps rode on the breadboard (lying beside it, Step 35); an unplugged male would ride there 18 mm over its hole. The LCD's GND and
VCC rail holes are moved +10.16 / +15.23 mm z from the CAD's (LCD_RAIL_SHIFT, to clear the black and green jumpers): materials.json
moves the caps too, so nothing to do here.

### 4.8 F4 and the switch
Published merges our 48 + 49 (lifted over the frame, then set flat) into one step: ours can too (one `lift()`, two stages, the
switch leads through 84-86 to 30-32). The switch then comes out of F4 isolated (published 35, ours Step 15 reversed) after its leads
are unplugged.

## 5. What the generator will do by default here, and where to override (tools/stepgen.py)

1. `take_apart(parts_list_at_end=True, leave_out=['NAUO141'])`: the backing paper (Step 1, put away for good) would otherwise come
   back. `Guide(..., part='Deconstruction', steps_file='steps-deconstruction.json', source='lac-guide.glb', names=dict(FULL['names']),
   hover_names=...)` as the LSM's; `hero_azimuth=135` and the copyright line as guide.py's.
2. `lift()` never changes a lead's route by itself (give `wires=`, and `wire_via=` for staged ways); `unplug()` gives each lead the
   route its Full Build step had on Step N, which for the pot leads was drawn for F1 at F1_DOWN (section 4.2).
3. Parts the generator has no way for (F7A, F7B, F9, the switch, knob, nut, washer, the LCD's female caps, USB_A, and anything off its
   seat: the LCD and buzzer lying, F1 aside) are pulled "straight out the first free way" with a WARNING and a Review note: give
   `path=` / `paths=`. Such a step also has no Full Build camera to reuse (the camera is reused only from parts whose way is known):
   give `view_dir=` / `frame=` (the LSM's `camera_of(step)`), or the generator picks a new one.
4. `unplug()` re-hangs a plug on what it rode on before its Full Build step (from that step's carry): the switch caps on the switch,
   the pot caps on the pot, the buzzer's black cap on the buzzer, the LCD males on the breadboard; **the buzzer's red cap rode on
   nothing** (it appeared moving in Step 33): `ride_on=BUZZER`, else the buzzer's `remove()` is refused (a lead with one end left).
   With `paths=` by hand the plug has no "rode" either: give `ride_on=` then too.
5. `lift([F1, POT])`: the pot rides on F1 from then on (good: they move as one); `lift([F7A, F7B], ...)` would make F7B ride on F7A:
   give `ride_on=F3`.
6. `arrow_style then=` (an arrow per stage, in turn: Lee's PMG ruling) cannot be combined with `wire_via=` (F2 with the cable's stages,
   F4 and the LCD with their wires' stages, the buzzer's lift): choose per step (one arrow, the leads through their stages; or arrows in
   turn, the leads blended once). `in_turn=` is refused where a lead changes route.
7. More than two arrows in a step logs a NOTE (published: two at most); jumpers and plugs take eyes (`arrows=[]`), so a group of eight
   jumpers has no arrow problem.
8. The removal way of a part the Full Build moved in is tested against what is still seated only for straight ways (the USB plug, F8,
   F5, F6, the Nano, RTC, resistors, jumpers): turned ways (F2, the LCD, the buzzer, F9) are not tested, and wires never are (run
   `tools/motioncheck.py` on the result, one heavy job at a time).

## 6. Published steps our conventions change or drop

| published | what in-house does | why |
|---|---|---|
| 16 - 18 (washer, nut, knob put back on the pot) | dropped | Lee, 17 Oct 2026: a part once off is gone, never refitted (rulebook section 11) |
| 25 (USB unplugged after F9) | moved to our Step 4 (as soon as F5 and F2 are off), Step 1 caution "Disconnect the USB Cable from the computer or power supply before you begin." | power first (MRA, RCC, PMG); the closed box hides the plug (the LSM's caution) |
| wordless steps | every step its own caption | Lee, 17 Oct 2026 |
| arrows as published, hand-set | the published sizes (length x width, section 3), one per stage in turn where a part comes off in stages | Lee's PMG and LSM rulings, 21 Oct 2026 |
| 2, 12 - 18 (camera rolled, scene up-axis -X) | our Full Build's cameras (Step 56's from the back; the pot upright at BUILD, BUILD_LOOK) | our player does not roll the camera |
| 4c, 5c, 6, 8, 27 (cross-fades between posed copies) | real moves: the Full Build's ways reversed, leads through its own stage shapes | the in-house player moves parts |
| 9 - 11, 19 - 22, 26 - 28 (order) | the buzzer out of the F7s before the pot and LCD wires; F1 moved back beside the board first; F9 before the buzzer | wires would pass through each other in our model (section 4.2); F9 then never meets the buzzer's way |
| 36 - 43 (jumper order) | orange and yellow first (or all eight at once) | purple, blue, green would pass through orange (section 4.4) |
| 12 - 15 isolated scene | `alone=` for the pot's steps, then `put_away([F1])`; the same for the switch (35) and `put_away([F4])` | the RCC's, PMG's, LSM's sub-assemblies taken apart on their own |
| 15c, 35c (pot, switch out but left on screen) | removed (slide, then fade) | rulebook 11: removed parts are not left on screen |
| 23, 31 (LCD, buzzer taken away by a fade, no motion) | a short move (up 30 mm), then the fade, with an eye | in-house removals slide then fade |
| 19 - 22 labels GND / VCC / SDA / SCL | keep (recommended) | the published has them; Lee made the same exception for the MRA's row labels; "no text labels" otherwise |
| one wire per step (20 steps of wires) | as published unless Lee asks for groups (section 8) | Lee asked to convert this published guide; his group rule came with the PMG and LSM requests |
| misnamed / duplicate frames ([104], [105], [120]), dead pause ([033]), RTC transition that waits ([118]) | not copied | slips (report section 7) |
| ends on F3 + breadboard | the same, then the Full Build's parts list | as the MRA's, PMG's, LSM's |

## 7. The take-apart this points to (46 steps; one wire per step, as published)

Ids as guide.py names them. "pub" = the published step it follows; "undoes" = our Full Build step(s); arrow = the published (length,
shaft width) in mm for `arrow_style={id: dict(dims=...)}`. Cameras: "default" = the generator reuses the undone step's; otherwise by
hand from that step (the LSM's `camera_of()`). Captions are ideas in TechBox's take-apart wording (the LSM review's), each its own.

| ours | caption idea | call | ids (and what goes with them) | pub | undoes | camera | cue |
|---|---|---|---|---|---|---|---|
| 1 | Remove F6 from the end of the case next to the Alarm Buzzer. (caution: disconnect the USB Cable from the computer or power supply before you begin) | remove | F6 | 1 | 57 | default (57) | arrow (56.1, 4.87) |
| 2 | Swing the end of F2 next to F6 away from the case, then slide F2 off the tabs of F5, clear of the USB Cable. | remove | F2; `wires` usb cable 74 (via 124) | 2 | 56 | default (56, from the back) | arrow (79.8, 5.51), in turn for the swing and the pull; eye on the cable at the slit (643.13, 899.6, 1339.4) |
| 3 | Remove F5 from the end of the case next to the breadboard. | remove | F5 | 3 | 55 | default (55) | arrow (64.6, 6.19) |
| 4 | Disconnect the USB Cable from the Nano Board. | remove | USB_B, USB_A (`units=[[USB_B]]`, USB_A a way shifted from where it lies) | 25 | 40 | 40's direction, wider (r about 70) | arrow (63.5, 5.78) on the plug |
| 5 | Pull F1 forward off the tabs of F3 and F4. Leave the Potentiometer's wires connected. | lift | F1, POT (knob, nut, washer ride); `wires` pot 118-120 | 4 | 54 | default (54) | arrow (79.0, 5.78) |
| 6 | Lay F1 face down in front of the case, toward the end where F6 was. | lift | F1 (`to` = Step 53's start pose); `wires` pot 81-83 | 5 | 53 | 53 | eye on F1 |
| 7 | Slide the LCD Screen out of the notches in F9 and back through the slots in F8, then lay it face down beside the case. Leave its wires connected. | lift | LCD (females ride); path 52 + 51 reversed; `wire_via` lcd [110/106/96/95/94 ...]; `wires` 90-93 | 6 | 52 + 51 | 52's or 51's, wider (or two steps, each its own) | eye on the LCD; inset Step 52c's (F9's notches) |
| 8 | Slide F8 out of the slots in F3 and F4, toward the front. | remove | F8 | 7 | 50 | default (50) | arrow (83.9, 4.51) |
| 9 | Lift F4, with the Rocker Switch, off the tabs of the F7s and F9, and set it down behind the case. Leave the switch's wires connected. | lift | F4 (switch rides); path [[0, 49.8, -0.2], [-82.7, 17.3, -0.1]]; `wire_via` switch 84-86; `wires` 30-32 | 8 | 49 + 48 | default (49) | arrow (73.2, 3.35) |
| 10 | Swing the top of F9 toward the front to unhook its foot from F3, then lift F9 out. | remove | F9; path from Steps 46, 45c, 45 (section 3, pub 24) | 24 | 46 + 45 | 46 | arrow (33.8, 3.3), in turn; inset Step 45c's |
| 11 | Spread the tops of the two F7s apart. | lift | F7A, F7B (paths = Step 42c's tilts, `ride_on=F3`) | 26 | 44 | 44 | arrows (36.9, 3.75) and (40.5, 3.8) |
| 12 | Lift the Alarm Buzzer out from between the F7s and lay it beside the case, past the end of the breadboard. Leave its wires connected. | lift | BUZZER; `wire_via` buzzer [76, 75] / [78, 77]; `wires` 52 / 53 | 27 | 43 | default (43) | arrow (58.3, 6.15); eye on the buzzer |
| 13 | Let the F7s straighten, then pull both out of the slots in F3. | remove | F7A, F7B (paths [ZERO, [0, 80, 0]]) | 28 | 42 + 41 | 41 | arrows (37.3, 3.96) and (34.2, 3.96) |
| 14 | Move F1, still face down, back in front of the end of the breadboard. | lift | F1 (`to` = Step 47's start, F1_DOWN); `wires` pot 47-49 | - (new) | 47 | 47 | eye on F1 |
| 15 | Disconnect the Potentiometer's black wire from the (-) blue rail. (caution: pull each wire out by its connector) | unplug | NAUO14 (path: [0, 5, 0], then lying out from its pin; `ride_on=POT`; `wire_via` 49; `wires` 46) | 9 | 32 | 32 (POT_CAMERA) | eye |
| 16 | Disconnect the Potentiometer's tan wire from a5. | unplug | NAUO33 (as 15: hold [0, 18, 0]; via 48; wires 45) | 10 | 31 | keep | eye |
| 17 | Disconnect the Potentiometer's red wire from the (+) red rail. | unplug | NAUO34 (via 47; wires 44) | 11 | 30 | keep | eye |
| 18 | Pick up F1 and hold it upright, the knob toward you. | lift | F1 (`to` [100, 35, 100]; `wires` pot 41-43; `alone=[F1, POT, KNOB, NUT, WASHER]`) | (12's isolation) | 29 | 29 | eye on F1 |
| 19 | Pull the knob off the Potentiometer's shaft. | remove | KNOB (on the pot [60, 0, 0]) | 12 | 28 | 28 (BUILD_LOOK) | arrow (41.2, 2.93) |
| 20 | Unscrew the nut and take it off the shaft. | remove | NUT (Step 27c's turns reversed) | 13 | 27 | keep | arrow (56.5, 3.72) |
| 21 | Take the washer off the shaft. | remove | WASHER (on the pot [60, 0, 0]) | 14 | 26 | keep | arrow (70.6, 2.89) |
| 22 | Push the Potentiometer out through the back of F1. | remove | POT (+ its 3 caps and leads); then `put_away([F1])` | 15 | 25 | keep | arrow (52.7, 4.21) |
| 23 | Disconnect the purple wire from GND on the LCD Screen and from the (-) blue rail. | remove | NAUO82, NAUO97 (female: off its pin, [0, 0, 15] in the LCD's frame) | 19 | 36 | default (36) | label "GND" on the pin; eye on NAUO82 |
| 24 | Disconnect the yellow wire from VCC on the LCD Screen and from the (+) red rail. | remove | NAUO84, NAUO98 | 20 | 37 | default (37) | label "VCC"; eye |
| 25 | Disconnect the teal wire from SDA on the LCD Screen and from b8. | remove | NAUO86, NAUO99 | 21 | 38 | default (38) | label "SDA"; eye |
| 26 | Disconnect the blue wire from SCL on the LCD Screen and from b9. | remove | NAUO93, NAUO100 | 22 | 39 | default (39) | label "SCL"; eye |
| 27 | Remove the LCD Screen. | remove | LCD (up 30) | 23 | (35) | keep | eye |
| 28 | Disconnect the Alarm Buzzer's red wire from j4. | unplug | NAUO58 (`ride_on=BUZZER`) | 29 | 33 | default (33) | eye |
| 29 | Disconnect the Alarm Buzzer's black wire from the (-) blue rail. | unplug | NAUO59 | 30 | 34 | default (34) | eye |
| 30 | Remove the Alarm Buzzer. | remove | BUZZER (+ its 2 caps, leads; up 30) | 31 | (33) | keep | eye |
| 31 | Disconnect the Rocker Switch's black wire from j29. | unplug | NAUO48 (default; or hung as before Step 16: section 3) | 32 | 18 | default (18) | eye |
| 32 | Disconnect the Rocker Switch's tan wire from the (+) red rail. | unplug | NAUO49 | 33 | 17 | default (17) | eye |
| 33 | Disconnect the Rocker Switch's red wire from j27. | unplug | NAUO47 | 34 | 16 | default (16) | eye |
| 34 | Push the Rocker Switch up out of the square hole in F4. | remove | SWITCH (+ its caps, leads; on F4 [0, 50, 0]; `alone=[F4, SWITCH]`); then `put_away([F4])` | 35 | 15 | 15 | arrow (63.6, 4.95) |
| 35 | Disconnect the orange Breadboard Wire from j1 and i27. | remove | NAUO53, NAUO52 | 42 | 20 | one camera for 35 - 42 (the published held one: dir [0.566, 0.715, 0.410], or the Full Build's JUMPER_DIR), `keep_camera` | eye |
| 36 | Disconnect the yellow Breadboard Wire from j3 and i29. | remove | NAUO56, NAUO55 | 43 | 21 | keep | eye |
| 37 | Disconnect the white Breadboard Wire from a14 and the (-) blue rail. | remove | NAUO28, NAUO15 | 36 | 13 | keep | eye |
| 38 | Disconnect the dark red Breadboard Wire from a12 and the (+) red rail. | remove | NAUO30, NAUO31 | 37 | 14 | keep | eye |
| 39 | Disconnect the purple Breadboard Wire from a8 and i22. | remove | NAUO25, NAUO26 | 38 | 11 | keep | eye |
| 40 | Disconnect the blue Breadboard Wire from a9 and i21. | remove | NAUO22, NAUO21 | 39 | 12 | keep | eye |
| 41 | Disconnect the green Breadboard Wire from the (-) blue rail and i24. | remove | NAUO20, NAUO19 | 40 | 10 | keep | eye |
| 42 | Disconnect the black Breadboard Wire from i23 and the (+) red rail. | remove | NAUO16, NAUO17 | 41 | 9 | keep | eye |
| 43 | Remove the Real Time Clock from j19 to j24. | remove | RTC, COIN | 44 | 7 | default (7) | arrow (29.8, 3.55) |
| 44 | Remove a 12 kΩ Resistor from h27 and the (-) blue rail. | remove | RES1 (+ legs) | 45 | 5 | default (5) | arrow (39.4, 3.47) |
| 45 | Remove the other 12 kΩ Resistor from h29 and the (-) blue rail. | remove | RES2 (+ legs) | 46 | 6 | default (6) | arrow (46.8, 3.96) |
| 46 | Remove the Nano Board from the breadboard. | remove | NANO | 47 | 3 | default (3) | arrow (64.2, 3.72) |
| end | (Completed View: F3 with the breadboard, then the Full Build's parts list) | | F3, BREADBOARD | end | (1, 2) | generator | |

Shorter, with Lee's groups (as the MRA's, PMG's, LSM's): 15 - 17 in one `unplug()` (the three pot wires, an eye each); 23 - 26 in one
`remove()` (eight caps; or the PMG's way: the LCD pulled off the female ends with `let_go=`, then the four wires out together), 28 - 29 in
one, 31 - 33 in one, 35 - 42 in one (all eight jumpers rise together: no order to get wrong): 46 - 2 - 3 - 1 - 2 - 7 = 31 steps.

## 8. Questions for Lee this raises

1. The USB cable at Step 4 (power first, once the case is open) or where the published guide has it (after F9)?
2. One wire per step, as published (46 steps), or the groups he asked for on the PMG and LSM (31 steps)?
3. The potentiometer: picked up and held upright to take its knob, nut and washer off (our Full Build's way, two extra steps: F1 moved
   back beside the breadboard's end, and lifted upright), or taken apart where it lies, the model shown turned over?
4. Keep the published GND / VCC / SDA / SCL labels on the LCD wire steps?
5. The LCD out in one step (as published) or two (as our Full Build brought it in, and as the PMG's displays went out)?
6. The order changes forced by our wires (the buzzer before the potentiometer and LCD wires; orange and yellow first): fine?
7. Before publishing: `guides.json` has no LAC kit or guide yet (the Full Build is not on the site either); the deconstruction needs a
   guide entry with `"script": "deconstruction.py"` and the kit an entry under `kits`.
