# Dimension report: Electronics and wiring conventions

Scope: all 20 published TechBox guides (LSM = Laser STEM Matrix, LAC = LCD Alarm Clock, PMG = Piano Memory Game). Guide short names used below: LSM1, LSM2, LSM12 (Parts 1+2), LSM3, LSM4, LSM34, LSMF (full build), LSMD (deconstruction); LAC1-LAC4, LACF, LACD, LACE (electronics overview); PMG1-PMG3, PMGF, PMGD. Step indices in square brackets are the digest viewer indices of the named guide (for example LACF [019]).

## 1. How the numbers were produced

- A leaf-level state walker (`reports/_work_dim_wiring/walk.py`) replays every authored step of the raw payload and records, per viewer step, which top-level components are visible (solid-level visibility, hidden-parent flags honoured only where a solid was never switched explicitly), each component's effective hex colour, and its world bounding box in mm (CAD bounding box x CAD transform, with a step `position` replacing the transform translation). Annotation objects visible on each step are recorded with their text, size, screen position, leader tip position and anchor part.
- A wire-connection step is defined mechanically (`conn.py`): a `Step N` on which at least one pin/hole label is switched on and where, between `Step N` and its completed view, wire components are swapped (appear + disappear) while no rigid part moves. Lead lines and arrows were not part of the definition, so their absence is a finding, not an assumption.
- Result: **103 wire-connection step pairs in 10 guides** (LSM2 7, LSM12 7, LSMF 7, LAC1 6, LAC2 8, LAC3 6, LACF 20, PMG1 12, PMG2 9, PMGF 21). The other 6 construction guides (LSM1, LSM3, LSM4, LSM34, LAC4, PMG3) connect no wire. Because the part guides are slices of the full builds, the **48 pairs in the three full builds (LSMF 7, LACF 20, PMGF 21)** are the unique set; they cover **46 physical wires** (LSM 3 ribbon jumpers + 2 button leads; LAC 12 jumpers + 8 captive leads; PMG 21 jumpers). Percentages below are over the 48 unless stated.
- Part guides versus full builds: 55 part-guide wiring pairs were matched to their full-build twin. Of the 41 LAC and PMG pairs, 40 are identical in label text, label size, label position, wire colour, eye icon and camera, and the 41st differs only by one label nudged 2% (LAC1 Step 14). The 14 LSM pairs all differ (camera pulled back, label anchors changed, one label size, and the j5/j16 swap; see anomalies), because the LSM full build was re-shot.
- Renders inspected (contact sheets and single frames): LSM2 [000]-[030] (all), LSMF [027] [028] [041] [042], LSMD [032]-[039]; LAC1 [000]-[023], LAC2 [000]-[015] and [032]-[039], LAC3 [000]-[020] (all), LACD [048]-[055]; PMG1 [000]-[008], PMG2 [000]-[026] (all), PMGD [048]-[055].
- Kit chronology (from the per-guide reports): LSM projects were authored July-August 2025, LAC October-December 2025, PMG May 2026. Where the kits disagree, LAC and PMG agree with each other and LSM is the odd one out, so the LAC/PMG form is treated as the current house convention and the LSM form as an earlier variant.

## 2. Headline findings

1. A wire is never animated into place. On all 103 connection pairs the completed view fades the loose model out and fades a separately modelled, already-routed wire in (0 wire moves, 0 Transitions inside the pair).
2. Wire steps carry no red guidance at all: 0 lead lines and 0 arrows on 103 of 103. The destination is given by text labels (and, in LSM only, by a pair of pin badges).
3. The current callout recipe (LAC and PMG, 41 of 48 pairs): one black eye icon on the wire to pick up plus one label per end that has to be plugged in: two labels for a free jumper (33 of 33), one for a lead already attached to a component (8 of 8).
4. LSM uses a different, earlier recipe (7 of 48 pairs): one wire END per step, no eye icon, the label is hung on the plug in the student's hand, and module pads are marked with a filled/white badge pair.
5. Wire colour identifies which wire to pick up and nothing else. Of 12 supply wires only 3 are red or dark red; of 12 ground wires only 3 are black or charcoal; a black jumper goes to the (+) rail and a brick-red jumper to GND.
6. Connection order inside a module follows the physical order of the module's pins (10 of 10 testable module groups), not power-first (4 of 13 groups).
7. All wiring is finished before any enclosure wall is fitted (3 of 3 kits). Modules that mount in the enclosure are wired loose and mounted later (9 of 9); parts that mount in a loose panel or in the breadboard are mounted first and wired immediately after (4 of 4).

## 3. Every module wired: pins, colours, order

Columns: "Board-side label" is the breadboard hole / rail / I/O-module pin named on screen; "Module-side label" is the pin name on the peripheral. "Function" is read from the labels themselves (a wire labelled VCC, V+, (+) red or Vn is supply; GND, V-, (-) blue or Gn is ground; anything else is signal). M = male pin housing, F = female housing. The last column is the bounding-box length of the loose model and the largest bounding-box span of the routed model that replaces it; for LSM ribbon ends the "loose" figure is the previous state of the same wire.

**Laser STEM Matrix, full build (7 step pairs, 5 wires)**

| Step [index] | Module | Wire colour (hex) | Kind, ends | Board-side label | Module-side label | Function | Eye icon on | Loose length → routed span (mm) |
|---|---|---|---|---|---|---|---|---|
| 10 [021] | 8x8 LED matrix (breadboard end) | white (#ffffff) | ribbon jumper, M end | i2 | - | power (+) | none | - → 72 |
| 11 [023] | 8x8 LED matrix (breadboard end) | grey (#b1b3b3) | ribbon jumper, M end | i3 | - | ground | none | - → 62 |
| 12 [025] | 8x8 LED matrix (breadboard end) | purple (#4e008e) | ribbon jumper, M end | b19 | - | signal | none | 58 → 23 |
| 13 [028] | 8x8 LED matrix (pad end) | white (#ffffff) | ribbon jumper, F end | i2 | badge pair "V+" | power (+) | none | 72 → 74 |
| 14 [030] | 8x8 LED matrix (pad end) | purple (#4e008e) | ribbon jumper, F end | b19 | badge pair "V-In" | signal | none | 23 → 42 |
| 15 [032] | 8x8 LED matrix (pad end) | grey (#b1b3b3) | ribbon jumper, F end | i3 | badge pair "V-" | ground | none | 62 → 69 |
| 19 [041] | Push button (2 captive leads) | red (#ef3340), black (#2d2926) | 2 captive leads, M | j5 / j16 | - | switch pair | none | 49, 50 → 113, 86 |

**LCD Alarm Clock, full build (20 step pairs, 20 wires)**

| Step [index] | Module | Wire colour (hex) | Kind, ends | Board-side label | Module-side label | Function | Eye icon on | Loose length → routed span (mm) |
|---|---|---|---|---|---|---|---|---|
| 9 [019] | RTC module | black (#2d2926) | free jumper, M-M | i23 / (+) red | - | power (+) | wire body | 74 → 35 |
| 10 [021] | RTC module | green (#10cc62) | free jumper, M-M | (-) blue / i24 | - | ground | wire body | 74 → 38 |
| 11 [023] | RTC module | purple (#611b6c) | free jumper, M-M | a8 / i22 | - | signal | wire body | 74 → 37 |
| 12 [025] | RTC module | blue (#0074d9) | free jumper, M-M | a9 / i21 | - | signal | wire body | 74 → 32 |
| 13 [027] | Nano rail feed | light grey (#cccccc) | free jumper, M-M | a14 / (-) blue | - | ground | wire body | 74 → 24 |
| 14 [029] | Nano rail feed | dark red (#800000) | free jumper, M-M | a12 / (+) red | - | power (+) | wire body | 74 → 23 |
| 16 [034] | Rocker switch (captive lead) | red (#ef3340) | captive lead, M | j27 | - | signal | pin housing of the lead | 30 → 108 |
| 17 [036] | Rocker switch (captive lead) | tan (#b28362) | captive lead, M | (+) red | - | power (+) | pin housing of the lead | 30 → 136 |
| 18 [038] | Rocker switch (captive lead) | black (#2d2926) | captive lead, M | j29 | - | signal | pin housing of the lead | 30 → 94 |
| 20 [042] | Switch bridge to Nano | orange (#ff851b) | free jumper, M-M | j1 / i27 | - | signal | wire body | 56 → 67 |
| 21 [044] | Switch bridge to Nano | yellow (#eac80d) | free jumper, M-M | j3 / i29 | - | signal | wire body | 56 → 67 |
| 30 [065] | Potentiometer (captive lead) | red (#ef3340) | captive lead, M | (+) red | - | power (+) | pin housing of the lead | 50 → 240 |
| 31 [067] | Potentiometer (captive lead) | tan (#b28362) | captive lead, M | a5 | - | signal | pin housing of the lead | 50 → 233 |
| 32 [069] | Potentiometer (captive lead) | black (#2d2926) | captive lead, M | (-) blue | - | ground | pin housing of the lead | 50 → 229 |
| 33 [072] | Buzzer (captive lead) | red (#ef3340) | captive lead, M | j4 | - | signal | pin housing of the lead | 39 → 68 |
| 34 [074] | Buzzer (captive lead) | black (#2d2926) | captive lead, M | (-) blue | - | ground | pin housing of the lead | 39 → 65 |
| 36 [079] | LCD (I2C header) | purple (#611b6c) | free jumper, M-F | (-) blue | GND | ground | wire body | 58 → 109 |
| 37 [081] | LCD (I2C header) | yellow (#eac80d) | free jumper, M-F | (+) red | VCC | power (+) | wire body | 58 → 110 |
| 38 [083] | LCD (I2C header) | teal (#13a3a3) | free jumper, M-F | b8 | SDA | signal | end housing | 58 → 63 |
| 39 [085] | LCD (I2C header) | blue (#0074d9) | free jumper, M-F | b9 | SCL | signal | wire body | 58 → 66 |

**Piano Memory Game, full build (21 step pairs, 21 wires)**

| Step [index] | Module | Wire colour (hex) | Kind, ends | Board-side label | Module-side label | Function | Eye icon on | Loose length → routed span (mm) |
|---|---|---|---|---|---|---|---|---|
| 3 [007] | Push button 1 | dark red (#b70101) | free jumper, F-F | V4 | VCC | power (+) | wire body | 58 → 44 |
| 4 [009] | Push button 1 | white (#e4e4e4) | free jumper, F-F | S4 | OUT | signal | wire body | 58 → 44 |
| 5 [011] | Push button 1 | charcoal (#343232) | free jumper, F-F | G4 | GND | ground | wire body | 58 → 44 |
| 6 [014] | Push button 2 | bright green (#21f17a) | free jumper, F-F | V5 | VCC | power (+) | wire body | 58 → 44 |
| 7 [016] | Push button 2 | brown (#7c5a30) | free jumper, F-F | S5 | OUT | signal | wire body | 58 → 44 |
| 8 [018] | Push button 2 | yellow (#ffdc00) | free jumper, F-F | G5 | GND | ground | wire body | 58 → 44 |
| 9 [021] | Push button 3 | maroon (#85144b) | free jumper, F-F | V6 | VCC | power (+) | wire body | 58 → 44 |
| 10 [023] | Push button 3 | grey (#737980) | free jumper, F-F | S5 | OUT | signal | wire body | 58 → 44 |
| 11 [025] | Push button 3 | steel blue (#3876ac) | free jumper, F-F | G6 | GND | ground | wire body | 58 → 44 |
| 12 [028] | Push button 4 | pink-purple (#a75294) | free jumper, F-F | V7 | VCC | power (+) | wire body | 58 → 44 |
| 13 [030] | Push button 4 | red-orange (#ff4136) | free jumper, F-F | S7 | OUT | signal | wire body | 58 → 44 |
| 14 [032] | Push button 4 | teal green (#3d9970) | free jumper, F-F | G7 | GND | ground | wire body | 58 → 44 |
| 16 [037] | 4-digit display | gold (#ac9400) | free jumper, F-F | s8 | clk | signal | wire body | 59 → 58 |
| 17 [039] | 4-digit display | black (#000000) | free jumper, F-F | s9 | dio | signal | wire body | 59 → 61 |
| 18 [041] | 4-digit display | purple (#ab53ca) | free jumper, F-F | V9 | VCC | power (+) | wire body | 59 → 61 |
| 19 [043] | 4-digit display | brick red (#bb3d3d) | free jumper, F-F | G9 | GND | ground | wire body | 59 → 61 |
| 20 [046] | Dot matrix display | dark brown (#411900) | free jumper, F-F | V11 | VCC | power (+) | wire body | 59 → 54 |
| 21 [048] | Dot matrix display | green (#339f3f) | free jumper, F-F | G11 | GND | ground | wire body | 59 → 54 |
| 22 [050] | Dot matrix display | navy (#2a2f62) | free jumper, F-F | S11 | DIN | signal | wire body | 59 → 54 |
| 23 [052] | Dot matrix display | wine (#662639) | free jumper, F-F | S12 | CS | signal | wire body | 59 → 49 |
| 24 [054] | Dot matrix display | teal (#377e89) | free jumper, F-F | S13 | CLK | signal | wire body | 59 → 47 |

Notes to the table:
- LSMF Step 19: by seated geometry the red lead ends in column 5 and the black lead in column 16 (11 hole pitches apart, 27.9 mm). LSM2 [023] labels them that way; LSMF [041] has the two labels pointing at the opposite leads (anomaly A2).
- PMGF Step 10 [023]: the board-side label reads "S5" but the wire sits between V6 and G6, so "S6" is meant (anomaly A1).
- LAC hole labels are always a free hole in the same 5-hole strip as the component pin (RTC pins in row j, its wires in row i; Nano pins in rows c and g, its wires in rows a, b, i and j). The guides never show a Nano pin name.

### 3.1 Order of connections per module group (full builds)

| Group | Steps | Order used | Follows physical pin order of the module? | Supply before signal? |
|---|---|---|---|---|
| LSM matrix, breadboard ends | LSMF 10-12 | i2 (V+), i3 (V-), b19 (data) | n/a (holes are not in one row) | yes |
| LSM matrix, pad ends | LSMF 13-15 | V+, V-In, V- | yes (pad anchor x = -15.1, -13.8, -12.9) | no |
| LAC RTC | LACF 9-12 | i23 (+), i24 (-), i22, i21 | **no** (columns 23, 24, 22, 21) | yes |
| LAC Nano rail feeds | LACF 13-14 | a14 (-), a12 (+) | descending column | n/a |
| LAC rocker switch leads | LACF 16-18 | red, tan, black | yes (lead tips at x 64.6, 62.6, 60.7% of screen) | no (signal, +, signal) |
| LAC switch bridges | LACF 20-21 | j1-i27, j3-i29 | ascending column | n/a |
| LAC potentiometer leads | LACF 30-32 | red, tan, black | yes (21.2, 21.8, 22.4%) | no (+, signal, -) |
| LAC buzzer leads | LACF 33-34 | red, black | 2 leads | no (signal, -) |
| LAC LCD | LACF 36-39 | GND, VCC, SDA, SCL | yes (header top to bottom, as on the card photo) | yes |
| PMG push buttons 1-4 | PMGF 3-14 | VCC, OUT, GND (x4) | yes, 4 of 4 (left to right) | no |
| PMG 4-digit display | PMGF 16-19 | CLK, DIO, VCC, GND | yes (top to bottom) | no (supply last) |
| PMG dot matrix | PMGF 20-24 | VCC, GND, DIN, CS, CLK | yes (top to bottom) | yes |

Physical pin order holds in 10 of 10 groups where the module has a row of 3 or more pins/leads (LSM pads, switch, pot, LCD, 4 buttons, display, matrix); the one multi-pin exception is the RTC, whose wires land in breadboard holes next to its pins rather than on the module. Supply-first holds in 4 of the 13 groups that mix supply and signal wires (counting the four buttons separately). Modules are taken in ascending controller pin number in PMG (D4, D5, D6, D7, D8/D9, D11-D13).

### 3.2 Wire colour against function (46 wires, full builds)

| Function | Wires | Colours used |
|---|---|---|
| Supply (+) | 12 | white; black; dark red x2; tan; red; yellow; bright green; maroon; pink-purple; purple; dark brown |
| Ground | 12 | grey; green x2; light grey; black x2 (both captive leads); purple; charcoal; yellow; steel blue; teal green; brick red |
| Signal | 20 | purple x2; blue x2; orange; yellow; teal x2; red x2 (captive); tan; black x2; white; brown; grey; red-orange; gold; navy; wine |
| Switch pair (LSM button) | 2 | red, black |

- Supply on a red or dark-red wire: 3 of 12 (LAC Nano feed, PMG button 1, LAC potentiometer lead). Ground on a black or charcoal wire: 3 of 12 (PMG button 1 jumper, LAC potentiometer and buzzer leads).
- Among the 36 ribbon jumpers the match rate is 2 of 10 supply wires red and 1 of 10 ground wires black. Counter-examples: black jumper to "(+) red" (LACF [019]), brick-red jumper is GND (PMGF [043]), yellow is VCC (LACF [081]) and also GND (PMGF [018]).
- The only wires that do follow the usual code are manufacturer-fitted leads with a polarity: potentiometer red to (+) and black to (-), buzzer black to (-) (3 of 3). The rocker switch's red/tan/black leads go to signal, (+), signal, so even fitted leads are not a code.
- Colours are unique within a ribbon (3, 6, 2, 4, 12 and 9 wires), and all 21 PMG jumpers are different colours. LAC re-uses three colours on different wires in different ribbons (purple #611b6c, blue #0074d9, yellow #eac80d), so colour identifies a wire only within the current ribbon/run.
- Ribbon position: wires are used in ribbon order in PMG (12 of 12 and 9 of 9, ribbon pitch 1.75 mm) and for the LAC LCD ribbon (4 of 4); the LSM ribbon is used in ribbon order only at the pad end; the LAC 6-wire ribbon is not used in ribbon order (ribbon: green, blue, purple, white, dark red, black; used: black, green, purple, blue, white, dark red).

## 4. Patterns (rules), with counts and exceptions

### WIRE-1  Show a connection as a model swap, never as a moving or bending wire
- Rule: in `Step N` show the wire as a straight, unconnected model; in `Step Nc` fade it out and fade in a separate pre-routed model that is already seated at both ends (same colour, with its end housings).
- Stats: 103 of 103 connection pairs are appear + disappear with no wire move; 0 of 103 have a Transition between N and c; both halves are `pause`, 800 ms. Routed spans range from 23 mm (short breadboard jumper) to 290 mm (potentiometer lead).
- Related: a wire only ever tweens while it is still straight and rigid: travelling with a pre-wired component into its panel (LACF Steps 15, 25; LSMF Step 17), sliding apart in a ribbon-separation step (LACF 8, 19, 35; PMGF 2, 15), or as the PMG USB plug (PMGF 25). That is 9 step pairs in the full builds against 69 swaps (48 connections + 20 re-poses + the LSM ribbon split).
- Exceptions: none for connections. Colour drift between the two models in LAC1: loose green #2ecc40 vs routed #10cc62, loose grey #aaaaaa vs routed #cccccc.

### WIRE-2  No red lead lines and no arrows on a wire step
- Stats: 0 lead lines and 0 arrows on 103 of 103 connection pairs. Red is reserved for rigid insertions (board into breadboard, component into panel, USB plug in PMG).
- Exceptions: none.

### WIRE-3  Keep `Step Nc` of a wire step completely clean and hold the camera
- Stats: 0 of 103 completed views carry any annotation; camera unchanged between N and c on 103 of 103.
- Exceptions: naming only (LAC1 "Step 14C"; PMG1 ends on "Completed View" instead of "Step 14c").

### WIRE-4  Granularity: one wire per numbered step
- Rule: a free jumper gets one step pair covering both of its ends; a lead that is already attached to a component gets one step pair for its free end. Never group wires, even when several go to adjacent pins.
- Stats: 33 of 36 jumpers are one-wire-one-step (LAC 12, PMG 21); 8 of 10 captive leads are one-lead-one-step (LAC switch 3, pot 3, buzzer 2).
- Exceptions (all LSM): the 3 ribbon jumpers take two steps each, one END per step, all breadboard ends first and then all matrix ends with the module's diagram card in between (LSMF Steps 10-12, card [027], 13-15); the two push-button leads share one step with two labels (LSMF [041]).

### WIRE-5  Callouts on a wire step: one eye, plus one label per end to plug in
- Rule (LAC, PMG): exactly one eye icon marks the wire to pick up; exactly one text label marks each destination. Free jumper = 2 labels; captive lead = 1 label. Nothing else.
- Stats: eye icon on 41 of 41 LAC/PMG pairs (82 of 82 counting part guides); labels 2 on 33 of 33 free jumpers and 1 on 8 of 8 captive leads; total annotations per step is 3 or 2. Eye width 7.81% of viewport in LAC (7.92% on 2 of 20), 8.2% in PMG; leader #7fdbff ending in a dashed ring.
- Eye anchor: mid-point of the wire body for free jumpers (32 of 33; LACF [083] is on the end housing); the pin housing at the tip of the lead for captive leads (8 of 8).
- Exceptions: LSM has no eye on any wiring step (0 of 7), see WIRE-8.

### WIRE-6  Label vocabulary and letter case
- Breadboard hole: lower-case row letter + column number ("i23", "a8", "b19"): 26 of 26 in the full builds (LAC 18, LSM 8).
- Breadboard power rail: polarity in brackets + the rail's stripe colour, lower case: "(+) red" x5, "(-) blue" x5 on wire steps (plus "(-) blue" x2 on the resistor steps). The colour word names the rail, not the wire.
- Module pin: the silkscreen name in capitals: VCC, GND, OUT, SDA, SCL, DIN, CS, CLK (23 of 25).
- I/O-module (shield) pin: row letter V / S / G + controller pin number, capitals: V4, S4, G4 ... S13 (19 of 21).
- Exceptions: PMGF [037] "clk" / "s8" and [039] "dio" / "s9" are lower case (4 of 42 PMG labels; the same signal is "CLK" at [054]). No label contains a verb, a part name or a wire colour.
- Style: bold black Arial, 3em in LAC and PMG (74 of 74), 2.5em in LSM (7 of 8; LSMF [021] is 3em); 5 px #7fdbff underline, 5 px #7fdbff leader, dashed "life-saver" ring (30 px x 1.2) on the exact pin or hole; default box 175 x 90 px (64 of 82).
- Anchors: LAC labels are tied to the breadboard (28) or to the LCD header pin (4). PMG module labels are tied to the module's own pin (21 of 21); shield labels to the correct header row block on 17 of 21 (4 are tied to a neighbouring part but still land within about one pin).

### WIRE-7  How the loose wire is shown (LAC, PMG)
- Free jumper: a straight model with both end housings, parked beside the assembly on the camera side, parallel to the long axis of the breadboard / row of modules (33 of 33 lie along the same world axis as the board's long side). It is not held over its destination.
- The parking spot is authored once per run and re-used: within a run the wire centre varies only by its ribbon slot (spread 2-7 mm in 5 of 6 free-jumper runs, ignoring one misplaced wire; 19 mm over the 12 button wires, i.e. 11 x 1.75 mm).
- Distances: 66-118 mm horizontally from the board centre (36-89 mm clear of the board edge). Height is not on a table plane: 3-10 mm above the top of the PMG I/O module, 42-68 mm above the LAC breadboard top (the wire floats nearer the camera and therefore renders larger).
- On screen the eye's leader tip (the wire mid-point) is in the lower half of the frame on 33 of 33 and left of centre on 30 of 33; the eye icon sits above its wire on 35 of 41 and to its left on 38 of 41, 8-31% of the viewport away.
- Captive lead: the lead is shown in its as-supplied straight form, sticking out of / hanging from the component (30-50 mm long), with the eye ring on its pin housing; the completed view replaces it with the routed lead while the other leads stay straight.
- Loose model size: 58 mm wire body, 1.2 mm thick; female housing 8 mm; male housing with pin 12 mm; a male-male jumper is 74 mm tip to tip.
- The parts-overview guide LACE [000] follows the same modelling: pre-attached leads are shown straight on their component with black pin housings; loose jumpers are not shown there at all.
- Exceptions: PMGF [037] (first display wire) is parked 40 mm from the spot used at [039]-[043]; LSM uses WIRE-8.

### WIRE-8  LSM variant (earlier form): hold the wire above the board, label the plug, badge the pad
- Near (breadboard) ends, LSMF [021] [023] [025]: the split ribbon floats horizontally 27 mm above the breadboard top, directly over the board; the plug hovers 24-25 mm above and 9-39 mm to the side of its hole (not vertically above it). One lower-case hole label is anchored to the plug itself. No eye, no line.
- Far (module) ends, LSMF [028] [030] [032]: the LED matrix floats 40.5 mm above the breadboard top; a matched pair of discs carrying the same text marks the connection: a filled #7fdbff disc on the module pad and a white disc on the wire's free female end (5.8-7.8% of viewport wide; "V+", "V-In", "V-"). One hole label names the hole the wire's other end already occupies, so the student knows which wire is meant. The camera swings 109-125 degrees between these steps to face each pad.
- Stats: 7 of 7 LSM pairs have no eye; 3 of 3 pad connections use the badge pair; camera moves on 5 of 7 LSM wire steps versus 9 of 41 in LAC/PMG.
- Differences between LSM copies: the far-end label is anchored to the seated plug in LSM2/LSM12 and to the breadboard hole in LSMF.

### WIRE-9  Order of connections
- Rule: finish one module before starting the next; within a module go along its header in physical pin order; take modules in ascending controller pin / left-to-right order. Do not reorder to put supply first.
- Stats: see table 3.1 (10 of 10 pin rows in physical order; supply-first only 4 of 13).
- Exceptions: RTC (VCC, GND, then SDA, SCL); LSM breadboard pass (V+, V-, data).

### WIRE-10  Colour is identity, not function
- Rule: give every wire in a run its own saturated colour, keep loose and routed models the same colour, model every end housing black; never rely on colour to tell the student what a wire does. Use the label for that.
- Stats: section 3.2.
- Exceptions: none (the three conventional matches are coincidences of fitted leads).

### WIRE-11  Introduce and separate a jumper ribbon in its own numbered step, in isolation
- Rule: before the first wire of a block, show the ribbon alone on white (everything else hidden, close camera) with an eye icon on it; the completed view shows the same wires separated and straight. Size the ribbon to exactly the wires the following block(s) use.
- Stats: 6 ribbon-prep pairs in the full builds (LSMF 9; LACF 8, 19, 35; PMGF 2, 15); 6 of 6 isolated; eye on 5 of 6; camera distance 103-175 mm; wire counts 3, 6, 2, 4, 12, 9 = exactly the wires used next (PMG's 9 = 4 display + 5 matrix).
- Separation: wires slide sideways in the ribbon plane; pitch goes from 1.75 mm to 4.4-4.9 mm (PMG 9- and 12-wire), 7.7-13.1 mm (LAC 4-wire), 21.6 mm (LAC pair); the LAC 6-wire ribbon widens from 12.3 to 40.3 mm. LSM instead swaps a joined-ribbon model for a split one with the ends fanned.
- Exceptions: PMGF [035] has no eye (the only `Step N` in that guide with no annotation); LSM2 [001] has two eyes (one on the male block, one on the female block) where LSMF [019] has one.

### WIRE-12  Module cards and pinout pictures
- Rule: every module whose pin names appear on wiring labels gets an un-numbered card, named after the module, immediately before its first use: module alone on white, close camera, plus a picture of the real board with the header to be used boxed in red, in a #7fdbff rounded frame with a leader to the same header on the 3D part.
- Stats: 13 electronics cards in the full builds (LSMF: Capacitor, LED Matrix Diagram, Mini USB Cable; LACF: Real Time Clock, Rocker Switch, Alarm Buzzer, LCD Screen, USB Cable; PMGF: Nano I/O Module, Push Buttons, 4-Digit Display, Dot Matrix Display, USB Cable). All 13 hide everything else; 12 of 13 come directly before the first step that uses the part (the 4-Digit Display card is followed by the ribbon-preparation step first). A pinout picture is present for 6 of 6 modules whose pins are named on labels (LSM matrix pads, LCD header, I/O module, push button, 4-digit display, dot matrix); picture width 17-37% of the viewport (65% for the LSM diagram, which replaces the 3D view).
- Cards without a pinout: RTC and buzzer (eye icon only), rocker switch and both later USB cards (no annotation), LSM USB card (eye), capacitor (polarity picture).
- Exceptions: the potentiometer, the LSM push button, the Nano and the jumpers have no card (their isolated view is a numbered preparation step). The LSM diagram shows "V- Out V+" while the badges say "V+", "V-In", "V-" (anomaly A3). The I/O-module picture has a caption and no red box; the Push Buttons picture has an orange ring.

### WIRE-13  When modules are mounted relative to wiring
- Rule: complete all wiring on the open base before any enclosure wall goes on. A component that mounts in a loose panel or plugs into the breadboard is mounted first and wired straight after; a module that mounts to the enclosure is wired while loose and mounted during enclosure assembly. A loose module is never "placed" by a step: it simply fades in at the position where it will be wired.
- Stats: wiring ends before the first wall in 3 of 3 full builds (LSMF wiring 10-19, walls 21-26; LACF wiring 9-39, enclosure 41-57; PMGF wiring 3-24, case 26-51). Mounted before wiring: 4 of 4 (RTC into breadboard, rocker switch into F4, potentiometer into F1, LSM button into D2). Wired loose then mounted: 9 of 9 (LSM matrix; LAC buzzer and LCD; PMG 4 buttons, display, dot matrix), with 0 placement steps; they appear on their card, on the first wire step, or (PMG buttons 2-4) on an auto-advancing Transition.
- After wiring, a wired module is repositioned only by cross-fading between pre-posed copies that each carry their own re-routed wires: 20 such step pairs in the full builds (LSMF 4, LACF 8, PMGF 8), 0 wire moves.

### WIRE-14  One camera per wiring run
- Rule: set the view on the first wire of a module block so that both ends, the parked wire and the label margins fit, then hold it for every wire of that block. Do not zoom to the pin.
- Stats (LAC, PMG): 41 wire steps in 9 runs; the camera moves on the first step of 9 of 9 runs and on 0 of the other 32 steps. Distances 173-202 mm (PMG), 277-439 mm (LAC); elevation 21-57 degrees. Longest hold: 12 button wires (PMGF [007]-[033]).
- Exceptions: LSM re-aims for nearly every wire end (5 of 7).

### WIRE-15  USB cable
- Rule: give the cable its own card, make it the last electrical connection, and show it with a single step pair.
- Stats: card before the step in 3 of 3 kits (cable alone; eye on it only in LSM). Last connection before the enclosure in 3 of 3 full builds (LSMF Step 20, LACF Step 40, PMGF Step 25).
- Two depictions: (a) LSM and LAC: `Step N` shows only an eye icon on the Nano's USB socket, no loose cable in the scene; `Step Nc` fades the plugged, routed cable in (no motion, no line). (b) PMG: the plug appears withdrawn 22.9 mm on the socket axis with one red lead line (28.5 mm) and tweens in, seen from the rear so the travel runs across the screen.
- Exceptions: LSM2 / LSM12 fit the D2 panel before the cable; LSMF reverses that.

### WIRE-16  Components that plug into the breadboard or the I/O module
- Rule: hover the part straight above its seat, draw one thin red line from each end pin / lead tip to its hole, and name those holes with lower-case labels (maximum two); tween straight down in the completed view. Bend leads in a separate isolated step first (model swap), and flag polarity with an eye icon.
- Stats: 9 plug-ins in the full builds (LSMF Nano, 2 resistors, capacitor; LACF Nano, 2 resistors, RTC; PMGF Nano into the I/O module). Lines: 2 on 7, 4 on 2 (the LSMF and PMG Nano, at the four corner pins). Two hole labels on 7 of 9. Hover 29-44 mm (median 34).
- Breadboards are used in LSM and LAC; PMG has none (everything goes through the Nano I/O module with 3-row V/S/G headers). There are no servo or multi-pin sensor plugs in any kit: every connection is a single-pin Dupont end.
- Exceptions: LSMF Nano and PMG Nano have no hole labels (LSM1's version labels "Pin d12" and "c16").

### WIRE-17  Connector ends are modelled and gendered correctly
- Rule: a pin end (male) goes into a breadboard hole; a socket end (female) goes onto a module or I/O-module header pin. Model each end as a black housing (male ones with a silver pin).
- Stats: 33 of 33 ends that go into a breadboard are male pins (LSM 5, LAC 28); 7 of 7 ends that go onto a module header in LSM and LAC are female (3 matrix pads, 4 LCD pins); all 42 ends of the 21 PMG jumpers are female (header pins at both ends). Housing colours #000000 / #1e1616, pins #a6a9aa / #cccccc.
- Exceptions: none.

### WIRE-18  Deconstruction: unplugging
- LACD: one wire per step, both ends in the same step (20 wires, 20 steps); an eye icon on one plugged-in housing on 20 of 20 (the only cue on 16; the four LCD wires add a pin-name label GND, VCC, SDA, SCL to tell adjacent wires apart); no hole labels, no arrows, no lead lines. (LACD [105] is a duplicate frame that inherits its eye from [104].) Free jumpers cross-fade to the straight loose model at the build's parking spot in an auto Transition and then fade (12); captive leads swap back to the hanging straight pose and stay (8).
- LSMD: breadboard ends one per step with an eye on the plug and no arrow (Steps 11-13); the three matrix-end plugs together with an arrow (Step 15); two button plugs together (Step 17).
- PMGD: wires leave in bundles (5 matrix wires at Step 18, 16 wires at Step 22) with one red arrow per bundle, no eye and no label.
- No common rule beyond "eye on the plug, never a hole label, wires cross-fade"; granularity differs by kit (1, 1-3, 5-16 wires per step).

## 5. Supporting tables

### 5.1 Wiring runs and where the loose wire is parked (LAC, PMG full builds)

| Run | Steps | Camera (dist mm / elev / azim) | Loose model | Spot spread in run (mm) | Horizontal distance to board centre (mm) | Height above board top (mm) | Eye tip on screen (x%, y%) |
|---|---|---|---|---|---|---|---|
| LAC RTC + Nano jumpers | 9-14 | 277 / 54 / 128 | 74 mm M-M jumper | 4.7 | 92-96 | 42 | 25-28, 54-57 |
| LAC switch leads | 16-18 | 277 / 24 / -158 | 30 mm captive lead, vertical | lead pitch 7 | 116-129 | 35 | 61-65, 60 |
| LAC switch bridges | 20-21 | 277 / 57 / 55 | 56 mm M-M jumper | 2.0 | 95-96 | 68 | 74, 66-67 |
| LAC pot leads | 30-32 | 439 / 35 / 120 | 50 mm captive lead | lead pitch 5.4 | 252-263 | 16 | 21-22, 28-29 |
| LAC buzzer leads | 33-34 | 277 / 48 / -38 | 39 mm captive lead | 1.6 | 104-105 | 0 | 44-45, 82-83 |
| LAC LCD | 36-39 | 323 / 51 / 127 | 58 mm M-F jumper | 4.2 | 114-118 | 58 | 35-43, 63-72 |
| PMG buttons | 3-14 | 173 / 21 / -62 | 58 mm F-F jumper | 19.2 (ribbon slots) | 66-84 | 3 | 38-42, 67-73 |
| PMG display | 16-19 | 173 / 25 / -72 | 59 mm F-F jumper | 5.2 (+40 for [037]) | 78-98 | 10 | 44-65, 71-82 |
| PMG dot matrix | 20-24 | 202 / 30 / -81 | 59 mm F-F jumper | 6.9 | 87-93 | 10 | 47, 56-58 |

### 5.2 Ribbon preparation steps

| Guide step | Wires | Ends | Annotation | Camera dist (mm) | Completed view |
|---|---|---|---|---|---|
| LSMF 9 [019] (LSM2 1 [001]) | 3 | M-F | 1 eye (2 in LSM2) | 119 (103) | joined model swapped for split model |
| LACF 8 [017] | 6 | M-M | eye | 175 | wires slide apart, ribbon width 12.3 to 40.3 mm |
| LACF 19 [040] | 2 | M-M | eye | 175 | slide 9.1 and 10.7 mm apart |
| LACF 35 [076] | 4 | M-F | eye | 110 | slide 0 / 8.5 / 11.3 / 14.4 mm |
| PMGF 2 [004] | 12 | F-F | eye | 128 | fan out, pitch 1.75 to 4.85 mm |
| PMGF 15 [035] | 9 | F-F | none | 103 | fan out, pitch 1.74 to 4.39 mm |

### 5.3 Electronics cards (full builds)

| Card | Index | Content | Next step |
|---|---|---|---|
| Capacitor | LSMF [012] | part x2 in close-up + framed polarity picture (30% wide) | Step 6 (insert) |
| LED Matrix Diagram | LSMF [027] | flat picture only (65% wide), two red-boxed pad groups with eye icons baked in | Step 13 (first pad) |
| Mini USB Cable | LSMF [043] | cable alone + eye | Step 20 |
| Real Time Clock | LACF [014] | module alone + eye on coin cell | Step 7 (plug in) |
| Rocker Switch | LACF [031] | switch with its 3 leads, no annotation | Step 15 (mount) |
| Alarm Buzzer | LACF [071] | buzzer with 2 leads + eye | Step 33 (first lead) |
| LCD Screen | LACF [078] | LCD alone + eye + photo of the I2C header (29% wide), GND/VCC/SDA/SCL boxed in red | Step 36 |
| USB Cable | LACF [087] | cable alone, no annotation | Step 40 |
| Nano I/O Module | PMGF [001] | board in plan view + captioned photo of the real board | Step 1 (Nano in) |
| Push Buttons | PMGF [006] | one button + photo (17% wide), VCC/OUT/GND boxed in red | Step 3 |
| 4-Digit Display | PMGF [034] | display + photo of its back (34% wide), header boxed in red | Step 15 (ribbon), 16 |
| Dot Matrix Display | PMGF [045] | matrix + photo of its back (37% wide), header boxed in red | Step 20 |
| USB Cable | PMGF [056] | cable alone, no annotation | Step 25 |

### 5.4 Mounting versus wiring

| Component | Mounted | Wired | Sequence |
|---|---|---|---|
| LSM 8x8 LED matrix | LSMF Step 30 (after walls) | Steps 10-15 | wired floating, mounted later |
| LSM push button | Steps 16-18 into loose panel D2 | Step 19 | mount in panel, wire, then panel onto base (Step 21) |
| LAC RTC | Step 7 into breadboard | Steps 9-12 | mount, wire |
| LAC rocker switch | Step 15 into loose panel F4 | Steps 16-18 (+ bridges 20-21) | mount in panel, wire |
| LAC potentiometer | Steps 25-28 into loose panel F1 | Steps 30-32 | mount in panel, wire |
| LAC buzzer | Step 43 (clamped in F7) | Steps 33-34 | wired loose, mounted later |
| LAC LCD | Steps 51-52 | Steps 36-39 | wired loose, mounted later |
| PMG push buttons x4 | Steps 33-34 | Steps 3-14 | wired loose, mounted later |
| PMG 4-digit display | Steps 47-48 | Steps 16-19 | wired loose, mounted later |
| PMG dot matrix | Steps 49-50 | Steps 20-24 | wired loose, mounted later |

### 5.5 Label counts by class (wire steps, full builds)

| Kit | Breadboard hole | Rail | Module pin | I/O-module pin | Total | Size |
|---|---|---|---|---|---|---|
| LSM | 8 | 0 | 0 (3 badge pairs instead) | 0 | 8 | 2.5em (1 at 3em) |
| LAC | 18 | 10 | 4 | 0 | 32 | 3em |
| PMG | 0 | 0 | 21 | 21 | 42 | 3em |

Label placement: the label box sits above its target on 73 of 82 and the leader leaves the end of the underline nearest the target. In PMG the module-side label is the upper of the two on 21 of 21. Two labels on one step are 10-56% of the viewport apart (median 22%).

## 6. Anomalies (errors and inconsistencies, not conventions)

- A1. PMGF [023] / PMG1 [023]: shield label "S5" where S6 is meant; "S5" appears twice and "S6" never.
- A2. LSMF [041]: labels "j5" and "j16" are attached to the wrong leads (j5 to the black lead's plug, j16 to the red); the seated wires at [042] have red in column 5 and black in column 16, as LSM2 [023] labels them.
- A3. LSM pad naming: badge "V-In" (LSMF [030]) is not a pin name; the diagram card reads "V- Out V+" and the LSM2 description says "IN pin".
- A4. Mixed case in PMG: "clk", "s8", "dio", "s9" (PMGF [037] [039]) against capitals elsewhere.
- A5. Label size: LSM wire labels are 2.5em except LSMF [021] at 3em; LAC and PMG are 3em.
- A6. PMGF [035] (9-wire ribbon) has no eye icon; the equivalent PMGF [004] has one.
- A7. PMGF [037]: first display wire parked 40 mm away from the spot used for the next three.
- A8. LACF [083]: eye anchored to the end housing; the other three LCD wires have it on the wire body. Eye width 7.92% on 2 of 20 LAC wire steps (7.81% elsewhere), 8.24% on the USB step.
- A9. Four PMG shield labels are anchored to a neighbouring part (V4 and s8 to the Nano socket strip, G9 to the V row, V11 to the S row).
- A10. Colour clashes a student may notice: black wire to "(+) red" (LACF [019]), yellow wire to "(+) red" and purple to "(-) blue" (LACF [079] [081]), brick-red wire = GND (PMGF [043]); the white PMG wire is nearly invisible on the white background.
- A11. LAC1 loose and routed models of the same wire differ in colour (green, grey).
- A12. LSM wiring steps carry stale descriptions in LSM2 / LSM12 (numbered +5, slot names in capitals, "Ste[ 15"); LSMF has none. The description says upper-case "I2" where the label says "i2".
- A13. Card / preparation order differs: ribbon prep before the Push Buttons card (PMGF Step 2, card [006]) but after the 4-Digit Display card (card [034], Step 15); in LAC the LCD ribbon prep (Step 35) comes before the LCD Screen card.
- A14. USB depiction differs between kits (fade-in with eye versus hover + lead line + tween) and LSM2 fits the panel before the cable while LSMF does the reverse.

## 7. Numeric defaults

| Item | Value | Basis |
|---|---|---|
| Wire-step duration / behaviour | 800 ms, pause on both N and Nc | 103 of 103 |
| Lead lines / arrows on a wire step | 0 / 0 | 103 of 103 |
| Annotations on Nc | 0 | 103 of 103 |
| Labels per free jumper / per captive lead | 2 / 1 | 33 of 33 / 8 of 8 |
| Eye icons per wire step | 1 | 41 of 41 LAC+PMG |
| Eye icon width | 7.81% of viewport width (LAC, LSM); 8.2% (PMG) | 18 of 20; 21 of 21 |
| Label text | Arial bold black, 3em (2.5em in LSM) | 74 of 74 LAC+PMG |
| Underline / leader | #7fdbff, 5 px / 5 px, dashed ring anchor 30 px x 1.2 | 82 of 82 underline; 80 of 82 ring size |
| Label box | 175 x 90 px | 64 of 82 |
| LSM pad badge | disc pair, 5.8-7.8% of viewport wide, filled #7fdbff on pad / white on wire end | 3 of 3 |
| Loose jumper model | 58 mm body, 1.2 mm thick; F housing 8 mm, M housing + pin 12 mm; M-M overall 74 mm | bounding boxes |
| Ribbon pitch | 1.75 mm joined; 4.4-4.9 mm after separation (9-12 wires) | PMGF, LACF |
| Parking spot of loose jumper | 66-118 mm from board centre, parallel to board long axis, on the camera side | 33 of 33 |
| Parked wire on screen | leader tip y 54-83% (lower half), x left of centre | 33 of 33; 30 of 33 |
| LSM hover heights | ribbon 27 mm, matrix 40.5 mm above breadboard top | LSMF |
| Plug-in component hover | 29-44 mm, median 34 mm | 9 plug-ins |
| USB plug hover (PMG) | 22.9 mm, 1 lead line 28.5 mm | PMGF [057] |
| Wiring camera | distance 173-202 mm (I/O-module kits), 277-439 mm (breadboard + panels); elevation 21-57 degrees | 41 steps |
| Camera moves inside a wiring run | 0 | 32 of 32 |
| Cards with pinout picture | framed photo 17-37% of viewport wide (#7fdbff rounded frame); red box round the header to use | 4 framed photos measured; red box on 5 of 6 pictures |

## 8. Rules an author must follow for a new wiring sequence

1. Finish mechanical mounting that does not depend on the enclosure (breadboard plug-ins, components in loose panels) before wiring that component; leave enclosure-mounted modules loose.
2. Before a module's first wire, insert an un-numbered card named after the module: module alone on white, with a framed picture of the real board and the header boxed in red if any of its pin names will be used on labels.
3. Before the first wire from a new ribbon, insert a numbered preparation pair: ribbon alone with an eye icon, then the same wires separated. Size the ribbon to the wires needed.
4. Fade the module in at the place where it will be wired; do not spend a step placing it.
5. Set one camera for the whole module block: both ends in frame, room at lower left for the parked wire and white margins for labels. Do not move it until the block is done.
6. For each wire, in the module's physical pin order, author one pair:
   - `Step N`: straight loose wire parked at the block's staging spot (or the straight captive lead on its component); one eye icon on it; one label per end to plug in, using the vocabulary in WIRE-6; no lead lines, no arrows.
   - `Step Nc`: same camera; loose wire and all three callouts off; pre-routed wire in the same colour on; nothing else.
7. Give every wire in the block its own colour and keep it between loose and routed models. Do not use colour to signal function.
8. Model male ends for breadboard holes and female ends for header pins, with black housings.
9. Do all wiring before the first enclosure wall. Plug the USB cable last, with its own card.
10. To move an already-wired module later, cross-fade to a pre-posed copy with its own re-routed wires; never tween it.

## 9. Open questions

- Which wiring recipe should the player standardise on for a kit with a breadboard and an off-board module: the LSM one-end-per-step form with badge pairs, or the LAC/PMG whole-wire form with an eye icon? The two later kits use the latter exclusively.
- Is the parking spot meant to be a fixed screen position (lower left) or a fixed world offset? The data stores a world position per ribbon; on screen it lands lower left in 30 of 33 cases but lower right for the LAC bridges.
- Should the loose wire rest on a table plane? In LAC it floats 42-68 mm above the board, which makes it render about 1.6 times larger than scale.
- USB: fade-in with an eye on the socket (LSM, LAC) or hover + lead line + tween (PMG, the newest kit)?
- Should rail labels keep the colour word ("(+) red") when the wire going there is a different colour?
- Should shield labels be upper case throughout ("S8", "CLK") and should the "S5" for S6 be corrected at source?
- Is "module pin order" or "supply first" the intended teaching order? The RTC is the only module wired supply-first against its pin order.
- For deconstruction, is one wire per step (LAC) or bundles (PMG) the intended granularity?

## 10. Working files

All under `reports/_work_dim_wiring/`: `walk.py` (state walker), `state_<guide>.json` (per-step state for all 20 guides), `wiresteps.py`, `conn.py` and `connections.json` (the 103 connection records), `stats1.py`, `table.py`, `mdtable.py`, `master_table.md`.
