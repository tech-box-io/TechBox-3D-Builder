# Guide report: `19075-lac_full_build` ("LAC Full Build")

Kit: LCD Alarm Clock (LAC). Role: full build. 132 authored steps, 131 shown in the viewer (indices [000]-[130]).
Sources read: the whole digest (`digest/19075-lac_full_build.md` + `.json`), all 17 contact sheets, about 45 individual
frames at full size, the digest JSONs of LAC parts 1-4, and a handful of targeted queries on the raw payloads
(wood-panel visibility, annotation styles, project dates). Working scripts are in `reports/_work_lac_full/`.

## 1. Summary

The student builds the whole LCD Alarm Clock in 57 numbered steps: a breadboard on a plywood base (F3), an Arduino Nano,
two resistors and a real-time-clock module plugged into it, 12 loose jumper wires and 8 pre-attached component leads
connected one at a time, a rocker switch mounted in the top panel (F4), a potentiometer mounted in the front panel (F1),
a buzzer, a 20x4 I2C LCD and a USB lead, and finally the laser-cut box closed around it all (F7 x2, F9, F4, F8, LCD, F1,
F5, F2, F6). The guide is completely wordless: no step has a description or popup (0 of 131); meaning is carried only by
motion, red lead lines and arrows, short hole/pin labels, a black eye icon and five inset pictures. Every numbered step
is a pair, `Step N` (the "hover" view with annotations) followed by `Step Nc` (the seated result, normally clean), with
10 auto-advancing `Transition` keyframes inserted where a move needs more than one stage, 5 unnumbered section cards that
introduce a component on its own, one title page and one Completed View. The full build is the master project: LAC
parts 1-4 are later clones of it, and played back to back they reproduce it step for step once the three internal
Completed Views and three internal Start pages are removed and the steps renumbered (section 7).

## 2. Data caveat that affects reading the digest for this guide

The digest decides visibility as "the solid and all its ancestors are visible". In this project several plywood panels
have their top-level node flagged hidden while their child solids are switched on and off (verified in the raw
payload). The digest therefore never reports F2, F4, F5, F6 (or the F1-2 copy) appearing, although the thumbnails show
them clearly, and its "on screen now" part counts are 1-2 low on those steps. The true events, recovered from the raw
step properties, are:

| panel copy | becomes visible | hidden again | notes |
|---|---|---|---|
| F4-2 (top panel, flat pose) | [032] Step 15 | [107] Step 48c | also hidden on every isolated card/prep view in between |
| F4-3 (top panel, hovering above frame) | [107] Step 48c | [110] Step 49c | pose copy |
| F4-1 (top panel, seated) | [110] Step 49c | - | final |
| F1-2 (front panel, upright and hovering) | [120] Step 53c | [122] Step 54c | pose copy between F1-4 and F1-1 |
| F5-1 (end panel) | [123] Step 55, hovering 56.0 mm | - | slides in at [124] |
| F2-2 (back panel) | [125] Step 56, 79.7 mm away and tilted about 21 deg | - | slides at [126], rotates shut at [127] |
| F6-1 (end panel) | [128] Step 57, hovering 67.5 mm | - | slides in at [129] |
| F2-1 | never | - | unused copy |

The step table below uses the thumbnails plus these recovered events, not the digest part counts. The digest's
"parts still displaced" list is also not meaningful for this guide (several parts carry a large constant instance
offset), so "seated" in the table is judged from the thumbnails and the per-step moves.

## 3. Step table (every viewer step)

Kinds: `title`, `hover` (= `Step N`), `done` (= `Step Nc`), `transition (auto)` (behaviour `play`, auto-advances),
`card` (unnumbered section card), `completed`. Camera: `d` = distance in mm, `el` = elevation, `az` = azimuth, as given by
the digest. "Swap" means one model is hidden and a differently posed copy is shown in the same step, with no motion.
All steps have duration 800 ms. `->` in the annotations column reads "from ... to ...".

| idx | name | kind | what is added or done | annotations | camera |
|---|---|---|---|---|---|
| 000 | Start | title | Title page. Finished clock (hero 3/4 view) on the right half of the frame. | 2 static images, no leader: TechBox logo SVG top-left (w 38.9 %, at 2 %,6 %); title PNG bottom-left (w 42.1 %, at 2 %,64 %) reading "LCD Alarm Clock (LAC) / Full Build / (c) 2025 TechBox..." | MOVES -> d377 el37 az143 (rot 70 deg, pan 139 mm, zoom x0.46) |
| 001 | Step 1 | hover | Breadboard alone (already raised 46.9 mm for Step 2). Instruction: peel the protective backing off the underside. | 1 red arrow, 24.7 mm, pointing straight down from the underside; 1 inset image (w 20.5 %, cyan rounded border) "Protective Backing" with cyan leader to the board corner | MOVES -> d237 el33 az-49 (rot 109 deg, pan 118 mm, zoom x1.59) |
| 002 | Transition | transition (auto) | Grey backing sheet drops 53 mm below the breadboard (annotations vanish first). | none | static |
| 003 | Step 1c | done | Backing sheet hidden. Bare breadboard. | none | static |
| 004 | Step 2 | hover | Base plate F3 fades in already seated; breadboard hovers 46.9 mm above it. | 4 lead lines, 47.9 mm, vertical, breadboard bottom corners -> F3; eye icon on a breadboard corner (orientation check) | MOVES -> d237 el31 az-54 (rot 5 deg, pan 19 mm, zoom x1.00) |
| 005 | Step 2c | done | Breadboard drops 46.9 mm onto F3. | none | static |
| 006 | Step 3 | hover | Arduino Nano appears 39.8 mm above the breadboard. | 2 lead lines, 41.2 mm, from two diagonally opposite corner pins to their holes; labels "c15", "g1" on those holes | static |
| 007 | Step 3c | done | Nano drops 39.8 mm into the breadboard. | none | static |
| 008 | Step 4 | hover | PREP, isolated: everything hidden; one resistor alone with straight legs, close-up. | label "2x" (blue, 6em, no leader); eye icon on the colour bands | MOVES -> d110 el29 az-141 (rot 73 deg, pan 42 mm, zoom x2.16) |
| 009 | Step 4c | done | Straight legs swapped for bent (staple-shaped) legs. No motion. | "2x" label stays | static |
| 010 | Step 5 | hover | Assembly returns; resistor 1 hovers 37.1 mm above. | 2 lead lines, 40.2/40.4 mm, one per leg tip -> hole; labels "(-) blue", "h27" | MOVES -> d277 el29 az-133 (rot 8 deg, pan 38 mm, zoom x0.40) |
| 011 | Step 5c | done | Resistor 1 drops 37.1 mm. | none | static |
| 012 | Step 6 | hover | Resistor 2 appears 40.0 mm above. | 2 lead lines, 43.2 mm, one per leg; labels "(-) blue", "h29" | static |
| 013 | Step 6c | done | Resistor 2 drops 40.0 mm. | none | static |
| 014 | Real Time Clock | card | SECTION CARD, isolated: RTC module (blue HW-84 board + CR2025 coin cell) alone, close-up, already in its hover pose. | eye icon on the coin cell | MOVES -> d175 el22 az-130 (rot 7 deg, pan 59 mm, zoom x1.59) |
| 015 | Step 7 | hover | Assembly returns underneath; RTC hovers 33.6 mm above the breadboard. | 2 lead lines, 37.2 mm, from first and last header pin (Pin1, Pin6) to holes; labels "j24", "j19" | MOVES -> d277 el29 az-133 (rot 7 deg, pan 59 mm, zoom x0.63) |
| 016 | Step 7c | done | RTC + coin cell drop 33.6 mm. | none | static |
| 017 | Step 8 | hover | PREP, isolated: 6-way male-male jumper ribbon alone (black, dark red, white, purple, blue, green). | eye icon on the ribbon | MOVES -> d175 el54 az130 (rot 71 deg, pan 138 mm, zoom x1.59) |
| 018 | Step 8c | done | Ribbon fans out into 6 separate wires (each slides 4-15 mm sideways). | none | static |
| 019 | Step 9 | hover | Assembly returns; one loose straight BLACK jumper lies ~164 mm to the side of the assembly. | eye icon on the wire; labels "i23", "(+) red" on the two destination holes | MOVES -> d277 el54 az128 (rot 2 deg, pan 104 mm, zoom x0.63) |
| 020 | Step 9c | done | Straight wire swapped for routed black wire i23 -> (+) rail. No motion. | none | static |
| 021 | Step 10 | hover | Loose GREEN jumper appears ~159 mm to the side. | eye on wire; labels "(-) blue", "i24" | static |
| 022 | Step 10c | done | Swap to routed green wire. | none | static |
| 023 | Step 11 | hover | Loose PURPLE jumper appears ~164 mm to the side. | eye on wire; labels "a8", "i22" | static |
| 024 | Step 11c | done | Swap to routed purple wire. | none | static |
| 025 | Step 12 | hover | Loose BLUE jumper appears ~161 mm to the side. | eye on wire; labels "a9", "i21" | static |
| 026 | Step 12c | done | Swap to routed blue wire. | none | static |
| 027 | Step 13 | hover | Loose WHITE jumper appears ~165 mm to the side. | eye on wire; labels "a14", "(-) blue" | static |
| 028 | Step 13c | done | Swap to routed white wire. | none | static |
| 029 | Step 14 | hover | Loose DARK-RED jumper appears ~167 mm to the side. | eye on wire; labels "a12", "(+) red" | static |
| 030 | Step 14c | done | Swap to routed dark-red wire. | none | static |
| 031 | Rocker Switch | card | SECTION CARD, isolated: rocker switch with its 3 pre-attached leads (black, tan, red) alone, in hover pose. | none | MOVES -> d175 el44 az137 (rot 12 deg, pan 208 mm, zoom x1.59) |
| 032 | Step 15 | hover | Top panel F4 appears flat, on its own; switch hovers 81.2 mm above its cut-out. | 1 lead line, 69.5 mm, switch body -> rectangular cut-out in F4 | MOVES -> d277 el17 az137 (rot 28 deg, pan 27 mm, zoom x0.63) |
| 033 | Step 15c | done | Switch drops 81.2 mm into F4; leads hang below the panel. | none | static |
| 034 | Step 16 | hover | Assembly returns; F4 (with switch) floats beside the base, leads dangling. RED switch lead is next. | eye on the red lead tip; label "j27" | MOVES -> d277 el24 az-158 (rot 61 deg, pan 105 mm, zoom x1.00) |
| 035 | Step 16c | done | Dangling red lead swapped for a routed lead to j27. | none | static |
| 036 | Step 17 | hover | TAN switch lead. | eye on lead tip; label "(+) red" | static |
| 037 | Step 17c | done | Swap to routed tan lead. | none | static |
| 038 | Step 18 | hover | BLACK switch lead. | eye on lead tip; label "j29" | static |
| 039 | Step 18c | done | Swap to routed black lead. | none | static |
| 040 | Step 19 | hover | PREP, isolated: 2-way jumper ribbon (orange + yellow) alone. | eye on the ribbon | MOVES -> d175 el57 az134 (rot 58 deg, pan 53 mm, zoom x1.59) |
| 041 | Step 19c | done | The two wires slide 9-11 mm apart. | none | static |
| 042 | Step 20 | hover | Assembly returns; loose ORANGE jumper lies ~160 mm to the side. | eye on wire; labels "j1", "i27" | MOVES -> d277 el57 az55 (rot 41 deg, pan 98 mm, zoom x0.63) |
| 043 | Step 20c | done | Swap to routed orange wire. | none | static |
| 044 | Step 21 | hover | Loose YELLOW jumper appears ~162 mm to the side. | eye on wire; labels "j3", "i29" | static |
| 045 | Step 21c | done | Swap to routed yellow wire. | none | static |
| 046 | Step 22 | hover | PREP (disassembly), isolated: potentiometer with knob, nut, washer and 3 leads alone. Scene up-axis flipped. | 1 red arrow, 41.8 mm, along the shaft: pull the knob off | MOVES -> d513 el-28 az-45 (rot 119 deg, pan 329 mm, zoom x0.54) |
| 047 | Transition | transition (auto) | Knob slides 37.6 mm off the shaft. | none | static |
| 048 | Step 22c | done | Knob hidden. | none | static |
| 049 | Step 23 | hover | Nut is next. | 1 red arrow, 41.3 mm, along the shaft | static |
| 050 | Transition | transition (auto) | Nut spins and slides 37.9 mm off. | none | static |
| 051 | Step 23c | done | Nut hidden. | none | static |
| 052 | Step 24 | hover | Washer is next. | 1 red arrow, 32.6 mm, along the shaft | static |
| 053 | Ttansition | transition (auto) | Washer slides 37.9 mm off. (Step name typo.) | none | static |
| 054 | Step 24c | done | Washer hidden. Bare potentiometer. | none | static |
| 055 | Step 25 | hover | Front panel F1 appears (alone, seated); potentiometer pulled back 79 mm behind it. | 1 lead line, 91.7 mm, shaft -> round hole in F1 | MOVES -> d439 el-32 az-40 (rot 6 deg, pan 178 mm, zoom x1.17) |
| 056 | Step 25c | done | Potentiometer pushes 79 mm through the hole. | 1 inset image (w 17.7 %): front close-up of the small rectangular locating slot beside the shaft hole, red box highlight, cyan leader to the hole | static |
| 057 | Step 26 | hover | Washer appears ~61 mm in front of the panel. | 1 lead line, 75.4 mm, washer -> shaft | static |
| 058 | Step 26c | done | Washer slides 61.3 mm onto the shaft. | none | static |
| 059 | Step 27 | hover | Nut appears ~56 mm in front. | 1 lead line, 66.7 mm, nut -> shaft | static |
| 060 | Step 27c | done | Nut slides 55.9 mm on. | none | static |
| 061 | Step 28 | hover | Knob appears ~60 mm in front. | 1 lead line, 76.5 mm, knob -> shaft | static |
| 062 | Step 28c | done | Knob slides 60.5 mm on. | none | static |
| 063 | Step 29 | hover | CHECK: nothing new; straight-on close-up of the knob on F1. | eye icon on the knob | MOVES -> d125 el-82 az-83 (rot 53 deg, pan 206 mm, zoom x3.51) |
| 064 | Step 29c | done | Knob rotates so its pointer mark sits at about 7 o'clock. | none | static |
| 065 | Step 30 | hover | Whole layout returns (up-axis back to +y): base, F4 with switch, F1 with pot lying flat. RED pot lead is next. | eye on lead tip; label "(+) red" | MOVES -> d439 el35 az120 (rot 132 deg, pan 179 mm, zoom x0.29) |
| 066 | Step 30c | done | Swap to routed red lead. | none | static |
| 067 | Step 31 | hover | TAN pot lead. | eye on lead tip; label "a5" | static |
| 068 | Step 31c | done | Swap to routed tan lead. | none | static |
| 069 | Step 32 | hover | BLACK pot lead. | eye on lead tip; label "(-) blue" | static |
| 070 | Step 32c | done | Swap to routed black lead. | none | static |
| 071 | Alarm Buzzer | card | SECTION CARD, isolated: piezo buzzer with red/black leads alone. | eye icon on the buzzer | MOVES -> d237 el56 az-47 (rot 88 deg, pan 110 mm, zoom x1.85) |
| 072 | Step 33 | hover | Layout returns; buzzer lies beside the base. RED buzzer lead is next. | eye on lead tip; label "j4" | MOVES -> d277 el48 az-38 (rot 10 deg, pan 51 mm, zoom x0.86) |
| 073 | Step 33c | done | Swap to routed red lead. | none | static |
| 074 | Step 34 | hover | BLACK buzzer lead. | eye on lead tip; label "(-) blue" | static |
| 075 | Step 34c | done | Swap to routed black lead. | none | static |
| 076 | Step 35 | hover | PREP, isolated: 4-way male-female ribbon (purple, yellow, teal, blue) alone. Up-axis -y. | eye on the ribbon | MOVES -> d110 el-47 az47 (rot 121 deg, pan 141 mm, zoom x2.52) |
| 077 | Step 35c | done | Three of the four wires slide 8-14 mm apart. | none | static |
| 078 | LCD Screen | card | SECTION CARD, isolated: 20x4 LCD module alone, close-up. Up-axis -x. | eye icon on the screen; inset image (w 29 %) of the I2C backpack with the GND/VCC/SDA/SCL pins boxed in red, cyan leader to the header | MOVES -> d150 el-39 az-47 (rot 65 deg, pan 14 mm, zoom x0.74) |
| 079 | Step 36 | hover | Layout returns with the LCD lying face-down beside the base; loose PURPLE M-F jumper ~180 mm to the side. | eye on wire; labels "GND" (LCD header) and "(-) blue" (breadboard) | MOVES -> d323 el51 az127 (rot 167 deg, pan 115 mm, zoom x0.46) |
| 080 | Step 36c | done | Swap to routed purple wire. | none | static |
| 081 | Step 37 | hover | Loose YELLOW M-F jumper. | eye on wire; labels "VCC", "(+) red" | static |
| 082 | Step 37c | done | Swap to routed yellow wire. | none | static |
| 083 | Step 38 | hover | Loose TEAL M-F jumper. | eye on wire end; labels "SDA", "b8" | static |
| 084 | Step 38c | done | Swap to routed teal wire. | none | static |
| 085 | Step 39 | hover | Loose BLUE M-F jumper. | eye on wire; labels "SCL", "b9" | static |
| 086 | Step 39c | done | Swap to routed blue wire. | none | static |
| 087 | USB Cable | card | SECTION CARD, isolated: USB cable (right-angle mini-USB to USB-A) alone. | none | MOVES -> d277 el47 az-45 (rot 82 deg, pan 85 mm, zoom x1.17) |
| 088 | Step 40 | hover | Layout returns; cable hidden again. | eye icon on the Nano's mini-USB socket | MOVES -> d277 el29 az-62 (rot 22 deg, pan 89 mm, zoom x1.00) |
| 089 | Step 40c | done | Cable fades in already plugged into the Nano. No motion. | none | static |
| 090 | Step 41 | hover | Two F7 uprights hover 80.3 mm above F3. | 2 lead lines, 75.4/76.9 mm, one per upright, bottom tab -> slot in F3 | MOVES -> d377 el22 az-144 (rot 73 deg, pan 50 mm, zoom x0.74) |
| 091 | Step 41c | done | Both uprights drop 80.3 mm. | none | static |
| 092 | Step 42 | hover | Spread the uprights. | 2 red arrows (38.5, 47.9 mm) pointing outward in opposite directions | static |
| 093 | Step 42c | done | Both F7s tilt apart (rotate ~15 deg, lift 2.6 mm). | none | static |
| 094 | Step 43 | hover | Buzzer goes between the uprights. | 2 eye icons: one on the buzzer (source), one on the F7 slot (destination) | MOVES -> d377 el50 az55 (rot 106 deg, pan 68 mm, zoom x1.00) |
| 095 | Step 43c | done | Buzzer + leads swapped to the clamped pose between the F7s. | none | static |
| 096 | Step 44 | hover | Release the uprights. | 2 eye icons, one on each F7 | static |
| 097 | Step 44c | done | F7s rotate back upright (seated). | none | static |
| 098 | Step 45 | hover | F9 bracket hovers 103.9 mm to the side. | 2 L-shaped polyline lead lines (108.5, 111.9 mm): from the two feet, across, then down into the F3 slots | MOVES -> d323 el42 az45 (rot 11 deg, pan 49 mm, zoom x1.17) |
| 099 | Transition | transition (auto) | F9 slides 103.9 mm in. | none | static |
| 100 | Transition | transition (auto) | F9 tilts and shifts 68 mm. | none | static |
| 101 | Step 45c | done | F9 shifts a further 33 mm; left leaning, foot hooked. | 1 inset image (w 20.3 %): close-up of the hooked foot, red box highlight | static |
| 102 | Step 46 | hover | Stand F9 up. | 1 lead line, 7.3 mm, at the foot; eye icon on the foot | static |
| 103 | Step 46c | done | F9 rotates upright (seated). | none | static |
| 104 | Step 47 | hover | Move the front-panel sub-assembly (F1 + pot) across to the other side. | 1 red arrow, 101.7 mm; eye icon on F1 | MOVES -> d377 el49 az101 (rot 39 deg, pan 57 mm, zoom x0.86) |
| 105 | Step 47c | done | F1 + pot + knob + leads swapped for a copy in the new place (leads re-routed). | none | static |
| 106 | Step 48 | hover | Top panel is next. | eye icon on F4 | MOVES -> d377 el47 az123 (rot 15 deg, pan 17 mm, zoom x1.00) |
| 107 | Step 48c | done | F4 + switch + leads swapped for a copy hovering above the frame. | eye icon on a pot lead at the breadboard (check the wiring before closing) | static |
| 108 | Transition | transition (auto) | CAMERA ONLY: tilt down and zoom in; eye cleared. | none | MOVES -> d323 el33 az123 (rot 13 deg, pan 20 mm, zoom x1.17) |
| 109 | Step 49 | hover | F4 hovering. | 4 lead lines, 46.4-49.5 mm, vertical: tab tops of F9 (x2) and F7 (x2) -> slots in F4 | static |
| 110 | Step 49c | done | F4 + switch swapped for the seated copy. | none | static |
| 111 | Step 50 | hover | F8 bracket hovers 94.2 mm to the side. | 2 lead lines, 94.2 mm, -> slot in F4 and slot in F3 | MOVES -> d323 el44 az134 (rot 14 deg, pan 42 mm, zoom x1.00) |
| 112 | Step 50c | done | F8 slides 94.2 mm in. | none | static |
| 113 | Step 51 | hover | LCD is next. | eye icon on the LCD (lying flat) | MOVES -> d439 el30 az53 (rot 64 deg, pan 24 mm, zoom x0.74) |
| 114 | Step 51c | done | LCD + 4 wires swapped for a copy standing in front of F9. | none | static |
| 115 | Step 52 | hover | Seat the LCD board in the F9 notches. | 2 lead lines, ~25 mm, F9 notch -> LCD board; inset image (w 15 %): close-up with two red boxes on the notches | static |
| 116 | Transition | transition (auto) | Annotations cleared; nothing moves. | none | static |
| 117 | Transition | transition (auto) | LCD swapped for an intermediate-pose copy. | none | static |
| 118 | Step 52c | done | LCD swapped for the seated copy. | none | static |
| 119 | Step 53 | hover | Front panel is next. | eye icon on F1 (lying flat) | MOVES -> d377 el42 az126 (rot 58 deg, pan 42 mm, zoom x1.17) |
| 120 | Step 53c | done | F1 sub-assembly swapped for a copy standing upright, hovering in front of the box. | none | static |
| 121 | Step 54 | hover | F1 hovering. | 4 lead lines, 73.3 mm: F4 (x2) and F3 (x2) -> F1 | static |
| 122 | Step 54c | done | F1 sub-assembly swapped for the seated copy. | none | static |
| 123 | Step 55 | hover | End panel F5 appears hovering 56.0 mm off the end. | 4 lead lines, 50.7-55.9 mm: F1 (x2) and F3 (x2) -> F5 | MOVES -> d377 el30 az43 (rot 66 deg, pan 50 mm, zoom x1.00) |
| 124 | Step 55c | done | F5 slides 56 mm in. | none | static |
| 125 | Step 56 | hover | Box rolled onto its end (up-axis -x); back panel F2 appears ~80 mm away, tilted ~21 deg. | 2 lead lines, 75.6/75.8 mm: F2 tabs -> F5 slots | MOVES -> d439 el41 az-40 (rot 66 deg, pan 28 mm, zoom x0.86) |
| 126 | Transition | transition (auto) | F2 slides in until its tabs engage (still tilted). | none | static |
| 127 | Step 56c | done | F2 rotates closed. | eye icon on the USB cable where it exits the notch (check) | static |
| 128 | Step 57 | hover | Box back upright (up-axis +y); end panel F6 appears hovering 67.5 mm off the end. | 4 lead lines, 63.4-64.1 mm: F1 (x2) and F2 (x2) -> F6 | MOVES -> d439 el36 az133 (rot 102 deg, pan 98 mm, zoom x1.00) |
| 129 | Step 57c | done | F6 slides 67.5 mm in. | none | static |
| 130 | Completed View | completed | Finished clock with USB lead, hero 3/4 view. | none | MOVES -> d377 el34 az45 (rot 70 deg, pan 80 mm, zoom x1.17) |

## 4. Conventions found (evidence and exceptions)

Counts are over the 131 viewer steps: 1 title, 57 `Step N`, 57 `Step Nc`, 10 transitions, 5 cards, 1 Completed View.

### 4.1 Structure

- **S1. Every numbered step is a pair `Step N` then `Step Nc`.** 57 of 57. `Step N` shows what to do (part hovering or
  highlighted, annotations on). `Step Nc` shows the result. Numbering is continuous 1-57 with no gaps and does not
  restart at section cards.
- **S2. `Step Nc` is normally annotation-free.** 52 of 57 have no annotation at all. Exceptions (5): [009] 4c keeps the
  "2x" label; [056] 25c and [101] 45c add an inset close-up picture of the seated detail; [107] 48c and [127] 56c add
  an eye icon as a "check this before going on" marker.
- **S3. Every `Step N` carries at least one annotation.** 57 of 57. The combinations are few (section 4.5-4.9 give the
  recipes): eye + 2 labels (12), eye + 1 label (9, including "2x"), eye only (8), 1 lead line (5), 2 lead lines (4),
  4 lead lines (4), 2 lead lines + 2 labels (4), 1 arrow (3), arrow + picture or eye (2: Step 1 inset picture, Step 47 eye), 2 eyes (2), 2 arrows (1),
  4 lead lines + eye (1), 1 lead line + eye (1), 2 lead lines + inset image (1).
- **S4. Section cards.** 5 unnumbered steps named after a component: `Real Time Clock` [014], `Rocker Switch` [031],
  `Alarm Buzzer` [071], `LCD Screen` [078], `USB Cable` [087]. Each hides everything else, shows the component alone in
  close-up, waits for Next, and has no `c` partner. The step name is the only place the component's name appears.
  3 of 5 carry an eye icon; `LCD Screen` also carries an inset picture; `Rocker Switch` and `USB Cable` carry nothing.
  Not every component gets a card: the Nano, resistors, potentiometer, breadboard and all plywood parts have none.
- **S5. Transitions.** 10 steps with behaviour `play` (auto-advance), all 800 ms, all without annotations, all hidden
  from the step overlay (`overlayVisible` false on exactly these 10). 9 sit between a `Step N` and its `Step Nc`
  (Steps 1, 22, 23, 24, 56 have one; Steps 45 and 52 have two). 1 sits between `Step 48c` and `Step 49` ([108]) and
  only moves the camera. Uses: (a) play a removal before the part is hidden ([002], [047], [050], [053]); (b) split an
  insertion into stages ([099]+[100], [116]+[117], [126]); (c) reframe ([108]).
- **S6. Bookends.** `Start` [000] is a title page (logo top-left, title block bottom-left, finished product on the
  right, no leaders). `Completed View` [130] is the finished product from a hero angle with no annotations.
- **S7. No words.** 0 of 131 steps have a description or popup. Tooltips are enabled in the project but every part's
  tooltip is the placeholder "Description / none". Text exists only as labels (41), as the step names, and inside
  images (logo, title block, "Protective Backing", the silkscreen in the LCD backpack picture).
- **S8. Uniform timing.** Every step is 800 ms; parts and annotations fade in/out; moves tween; the camera tweens
  (speed 2, no orbit animation). 121 steps pause, 10 play.

### 4.2 Granularity

- **G1. One thing per numbered step.** Always one part, one wire, one wire end, or one manual action.
- **G2. One loose jumper per step, both ends in that one step** (12 of 12 jumpers: Steps 9-14, 20-21, 36-39). The step
  shows two labels, one per end.
- **G3. One lead end per step for components that come with leads attached** (8 of 8: switch Steps 16-18, pot 30-32,
  buzzer 33-34). The step shows one label.
- **G4. When several things do share a step, they are physically one unit or identical twins:**
  RTC board with its coin cell (Step 7); switch with its 3 leads (Step 15); pot with its 3 leads (Step 25); the two
  identical F7 uprights together, with one lead line each (Step 41) and flexed together (Steps 42, 44); a jumper
  ribbon split into all its wires at once (Steps 8, 19, 35: 6, 2 and 4 wires); "2x" for bending both resistors'
  legs, shown once (Step 4).
- **G5. Preparation is its own numbered step, shown in isolation:** bend resistor legs (4), split ribbons (8, 19, 35),
  peel breadboard backing (1), strip knob/nut/washer off the pot (22, 23, 24: one fastener per step).
- **G6. Multi-stage fits are split across steps rather than crammed into one:** F9 is "hook it in leaning" (Step 45)
  then "stand it up" (Step 46); the top panel is "lift it over" (48) then "onto the tabs" (49); the LCD is "stand it
  up" (51) then "into the notches" (52); the front panel is "stand it up" (53) then "onto the tabs" (54); the buzzer
  clamp is "spread" (42), "insert" (43), "release" (44).

### 4.3 Ordering

- **O1. Base first, box last.** Base plate and breadboard (Steps 1-2), board-mounted electronics (3-7), wiring
  (8-14), panel-mounted controls with their wiring (15-32), loose peripherals with their wiring (33-40), then the
  enclosure (41-57). All electronics are finished and wired while the box is still open and flat.
- **O2. A component is placed, then wired straight away, before the next component.** RTC (7) then its wires (9-12);
  switch (15) then leads (16-18) then its two link jumpers (20-21); pot (25-29) then leads (30-32); buzzer then
  leads (33-34); LCD then wires (36-39). Ribbon-splitting prep steps (8, 19, 35) come right before the first wire
  that needs them. Exception: the Nano's two rail jumpers (Steps 13-14) come after the RTC's wires, not right after
  the Nano.
- **O3. Lead order on pre-wired components is always red, (tan), black** (switch 16-18, pot 30-32, buzzer 33-34).
- **O4. The LCD header is wired in pin order** GND, VCC, SDA, SCL (36-39). There is no global "power before signal"
  rule: RTC goes rail, rail, signal, signal (9-12); pot goes (+), signal, (-); switch goes signal, (+), signal;
  buzzer goes signal, (-).
- **O5. Box order:** inner uprights (F7 x2), buzzer clamped between them, LCD bracket F9, top F4, bracket F8, LCD,
  front F1, end F5, back F2, end F6. Inside-out, and each panel goes on only when the tabs it needs are present.
- **O6. Disassembly before assembly where the kit part arrives pre-assembled:** the pot's knob, nut and washer come
  off in Steps 22-24 (outermost first) and go back on in Steps 26-28 in reverse order (washer, nut, knob).

### 4.4 Motion

- **M1. Rigid parts hover along their insertion axis and travel in a straight line to the seat in `Step Nc`.**
  Hover offsets: breadboard 46.9 mm, Nano 39.8, resistors 37.1 and 40.0, RTC 33.6, switch 81.2, pot 79.0,
  washer 61.3, nut 55.9, knob 60.5, F7 80.3, F8 94.2, F9 103.9, F5 56.0, F6 67.5, F2 about 80. Range 34-104 mm; small
  board parts 34-47 mm, panel-mounted parts and plywood 56-104 mm. Direction is vertical for anything plugged into
  the breadboard or base, horizontal for end panels and brackets, along the shaft for the pot stack.
- **M2. The hand-held piece is the one that moves, even when the other piece is the new one.** In Step 2 the new base
  F3 fades in seated and the breadboard (on screen since Step 1) comes down onto it. In Step 25 the new panel F1
  fades in seated and the pot (on screen since Step 22) is pulled back 79 mm and pushed through. In Step 15 panel F4
  appears seated and the switch drops into it.
- **M3. Flexible things never animate; they swap.** A loose jumper is shown straight, lying about 160-180 mm to the
  side of the assembly at table level (159-167 mm in Steps 9-14, 160-162 in 20-21, about 180 in 36-39), and `Step Nc`
  hides it and shows a separately modelled routed wire in place (20 of 20 wire steps: appear + disappear, no move).
  The same swap is used for resistor legs straight to bent (4c), for the USB lead (card model, then plugged model
  fades in at 40c), and for every sub-assembly that drags leads with it: buzzer (43c), front panel with pot (47c,
  53c, 54c), top panel with switch (48c, 49c), LCD with its four wires (51c, [117], 52c). Those sub-assemblies exist
  as 2-4 posed copies (F1-1/-2/-3/-4, F4-1/-2/-3, LCD V1-1/-2/-3/-5, Rocker Switch-1/-2/-3, Piezo Buzzer-1/-2).
- **M4. Removals play as an auto transition, then the part is hidden.** Arrow on `Step N`; Transition slides the part
  38-53 mm away (the nut and washer also spin); `Step Nc` hides it (Steps 1, 22, 23, 24).
- **M5. Rotations happen in the `c` step or in a Transition, never in `Step N`:** F7 tilt out about 15 deg (42c) and
  back (44c); F9 tilt in ([100]) and upright (46c); knob turn (29c); F2 hinge shut from about 21 deg (56c); nut and
  washer spin off ([050], [053]).
- **M6. Ribbon splitting is shown as a small fan-out,** each wire sliding 4-15 mm sideways from its neighbour (8c,
  19c, 35c).
- **M7. Section cards show the part already in the pose it has in the next step,** so going from card to step only
  moves the camera and reveals the assembly (RTC already 33.6 mm up at [014]; switch already 81.2 mm up at [031];
  buzzer and LCD already lying where they will be wired).

### 4.5 Red lead lines

Style: 3D line, solid, #ff0000, thin, no arrowhead, no end markers. 44 are shown, in 20 of the 57 `Step N` views.

- **L1. A lead line joins the mating feature on the moving piece to the mating feature on the target, along the
  travel axis.** Length is close to the hover offset: ratio 0.86-1.26 over 16 measurable steps (for example 47.9 mm
  line for a 46.9 mm hover in Step 2; 94.2 for 94.2 in Step 50; 69.5 for 81.2 in Step 15; 76.5 for 60.5 in Step 28).
- **L2. Count is 1, 2 or 4, never more, and follows the geometry:**
  - 1 line for a single round or rectangular fit: switch body to cut-out (15), pot shaft to hole (25), washer, nut,
    knob to shaft (26-28), F9 foot (46). 6 steps.
  - 2 lines for a pin row or a two-tab part: Nano (3), each resistor (5, 6), RTC (7), F7 pair (41, one line per
    upright), F9 feet (45), F8 (50), LCD into notches (52), F2 tabs (56). 9 steps.
  - 4 lines for a panel: breadboard corners to base (2), top F4 (49), front F1 (54), ends F5 and F6 (55, 57). 5 steps.
- **L3. On a pin row the two lines go from the two extreme pins:** the Nano's two diagonally opposite corner pins to
  c15 and g1; the RTC's Pin1 and Pin6 to j19 and j24; each resistor's two leg tips. Only those two holes are
  labelled.
- **L4. On plywood the lines run tab to slot,** two per neighbouring panel (Step 54: 2 from F4 and 2 from F3 to F1;
  Step 55: 2 from F1 and 2 from F3 to F5; Step 57: 2 from F1 and 2 from F2 to F6; Step 49: 2 from F9 and 1 from each
  F7 to F4).
- **L5. Lead lines are removed before anything moves** (off at the Transition or at `Step Nc`, 20 of 20).
- **L6. Wires get no lead lines** (0 of 20 wire steps).
- Exceptions: Step 45 uses two bent (3- and 5-point) polylines that run sideways from the feet and then turn down
  into the slots, because the part first slides and then drops; Step 46's line is only 7.3 mm (a marker at the
  foot); Step 52's lines are about 25 mm and mark the notches, with no hover.

### 4.6 Red arrows

Style: solid 3D straight arrow, #ff0000, body width 5, head 15-24 wide. 7 are shown, in 6 `Step N` views.

- **A1. An arrow means "move this by hand in this direction" when nothing is being seated:** peel backing down (1),
  pull knob / nut / washer off along the shaft (22, 23, 24), spread the two uprights (42, two arrows in opposite
  directions), carry the front panel across (47).
- **A2. Arrows and lead lines never share a step** (0 of 26 steps that have either).
- **A3. Removal arrows are followed by an auto Transition** (4 of 4). The two non-removal arrows (42, 47) go straight
  to `Step Nc`.

### 4.7 Labels

Style (40 of 41): black Arial bold 3em, centred, sitting on a 5-px #7fdbff underline, with a #7fdbff leader from the
underline to a dashed-ring ("Life Saver Circle") anchor on the exact hole or pin. Boxes are positioned in screen
percentages; the anchor follows the 3D feature.

- **T1. Labels name destinations only, never parts.** 24 breadboard holes as lower-case row letter + column number
  with no space ("c15", "h27", "j4"); the two power rails as "(+) red" (5 uses) and "(-) blue" (7 uses), i.e.
  polarity sign plus stripe colour; the four LCD header pins as "GND", "VCC", "SDA", "SCL".
- **T2. Labels appear only on steps that connect something to the breadboard or LCD header** (24 steps: 4 plug-in
  parts and 20 wires), and are removed in `Step Nc` (24 of 24). Plywood steps have no labels; panels are identified by the "F1"..."F9" engraved in
  the model itself.
- **T3. One label per wire end:** 2 for a loose jumper or a 2-pin/row part, 1 for a pre-attached lead.
- **T4. Placement:** in white space beside the model, x 18-69 %, y 8-58 % of the frame, never over the model. Two
  labels sit on opposite sides when the holes are far apart (Steps 3, 5-7, 11, 12, 36-39) and stacked on one side
  when both holes are on that side (9, 10, 13, 14, 20, 21).
- Exception: "2x" (Step 4 and 4c) is a quantity mark, blue #0074d9, Arial bold 6em, no underline, no leader.

### 4.8 Eye icon

A black eye glyph image, 7.8 % of frame width, with a #7fdbff leader to a dashed-ring anchor. 41 are shown on 39
steps: 34 `Step N`, 3 cards, 2 `Step Nc`.

- **E1. "Pick this up / this is the piece for this step":** on the loose jumper (12 steps), on the tip of the lead to
  plug in (8 steps), on a ribbon to split (8, 19, 35), on a sub-assembly about to be repositioned (47, 48, 51, 53),
  on the socket to use (40).
- **E2. "Look here / check":** breadboard corner for orientation (2), resistor bands (4), knob pointer (29), F9 foot
  (46), wiring before closing the lid (48c), cable in its notch (56c), and on 3 section cards.
- **E3. Two eyes mark source and destination when there is no lead line:** buzzer and the F7 slot (43); the two
  uprights to release (44).
- **E4. The eye replaces the lead line for anything that swaps instead of moving** (wires, sub-assemblies). Eye and
  lead line share a step only twice (Steps 2 and 46).

### 4.9 Image callouts

- **I1. Five inset pictures,** each in a rounded rectangle with a 5-px #7fdbff border, 15-29 % of frame width, with
  a #7fdbff leader to a dashed-ring anchor on the feature: "Protective Backing" (Step 1), pot locating slot (25c),
  LCD backpack pins (LCD Screen card), F9 hooked foot (45c), LCD board in the F9 notches (Step 52).
- **I2. Four of the five highlight the detail with a thin red rectangle** inside the picture (not Step 1, which has
  its own text and leader inside the picture instead).
- **I3. They show what the main view cannot:** an underside, a tiny slot, or a real-part photo with pin names. Two sit
  on `Step Nc` (seated-state check), two on `Step N`, one on a card.
- **I4. Title page:** two static images without leaders, logo (38.9 % wide, at 2 %, 6 %) and title block (42.1 % wide,
  at 2 %, 64 %).

### 4.10 Camera

Perspective, FOV 45 deg. The view cube is on.

- **C1. The camera never moves between `Step N` and `Step Nc`** (0 of 57), nor during any Transition that lies inside
  a step (0 of 9).
- **C2. The camera moves only on entering a `Step N` (30 of 57), a card (5 of 5), Start or Completed View,** plus the
  single camera-only Transition [108]. 38 moves in 131 steps.
- **C3. It stays put for a run of similar steps in the same place** (27 `Step N` views do not move): consecutive wires
  to the same component (10-14, 17-18, 21, 31-32, 34, 37-39), the washer/nut/knob stack (23-24, 26-28), the next
  action on the same parts (3, 6, 42, 44, 46, 49, 52, 54). Longest static run: [019]-[030], six wires, 12 views.
- **C4. Isolate, then return.** For every card and every prep step the rest of the model is hidden and the camera
  goes close (distance 110-237 mm in 8 of 10 cases; the pot strip-down is framed at 513 mm and the USB card at
  277 mm); the next step pulls back to the assembly (277-439 mm) and brings everything back.
  The two panel sub-assemblies are built in isolation as well (switch into F4, [031]-[033]; pot into F1, [046]-[064]).
  34 of 131 views are isolated.
- **C5. Distances come from a fixed ladder:** 110, 125, 150, 175, 237, 277, 323, 377, 439, 513 mm, i.e. 175 mm times
  powers of about 1.167 (mouse-wheel zoom clicks). Most used: 277 (37 views, electronics on the base), 439 (25),
  377 (20), 323 (19).
- **C6. Views are three-quarter views from above:** elevation 17-57 deg whenever the scene is upright, azimuth
  clustered near the four diagonals (-158...-130, -62...-38, 43...55, 101...143), chosen so the target holes or slots
  face the viewer. The one straight-on view is the knob check ([063]-[064]).
- **C7. The workpiece is re-oriented by switching the scene's up axis rather than by moving parts:** 7 switches
  ([046] to -x for the pot and front panel, [065] back to +y, [076] -y, [078] -x, [079] +y, [125] -x to stand the box
  on end so the back panel goes on like a lid, [128] +y).

### 4.11 Look

- White background (#ffffff), toon-shaded parts (1587 per-part style settings are `toon`, 2 are `default`) with black 1-px feature edges
  (edge angle 40 deg), no silhouette outline, no shadows, no ground plane. Two-tone shading: a lit tone and one
  darker tone per material.
- Annotation palette is three colours only: red #ff0000 (lead lines, arrows, highlight boxes), cyan #7fdbff (label
  underline, leaders, anchor rings, picture borders), black (label text, eye icon). Blue #0074d9 appears once ("2x").

### 4.12 Wiring recipe (20 steps)

`Step N`: the wire (or lead tip) gets an eye icon; each destination gets a label; no lead line; camera static if the
previous step wired the same component. `Step Nc`: the straight/dangling model is swapped for the routed model, and
labels and eye are removed. Routed wires are modelled as smooth arcs standing up off the board, each ending in a black
Dupont housing. Loose jumpers: two labels. Pre-attached leads: one label, taken in the order red, tan, black. LCD
jumpers: one label on the LCD header pin and one on the breadboard.

### 4.13 Mechanical recipe (16 steps)

`Step N`: part hovering 34-104 mm off its seat along the insertion axis, 1/2/4 red lead lines feature to feature,
no labels, normally no eye (exceptions: Steps 2 and 46). `Step Nc`: part seated, clean; add an inset picture if a small locating feature must be checked
(25c, 45c). Sub-assemblies with leads are swapped between posed copies instead of moved, and are introduced one step
earlier with an eye icon ("this next") and a `c` view that shows them repositioned and ready (47/47c, 48/48c, 51/51c,
53/53c).

## 5. Part looks (from the renders)

| part | look |
|---|---|
| Background | pure white |
| Plywood panels F1-F9 | flat light tan (material #deb887; renders about #fed29e lit, #caa67a on shaded faces and edges), black outlines, part id "F1"..."F9" as black engraved lettering that is part of the model |
| Breadboard | very light grey/white body (about #eaeaea), black-outlined square holes, red and blue rail stripes, tiny black row letters and column numbers; backing paper mid grey #aaaaaa |
| Arduino Nano | dark navy PCB, silver pins and parts, silver mini-USB socket, black 2x3 header |
| Resistor | bright blue body (about #026ac6) with brown, red, black, red, brown bands; grey legs (straight, then bent) |
| RTC module | bright blue PCB, black coin-cell holder, grey cell engraved "CR2025 3 VOLTS +", black ICs, pale gold header pins |
| Loose jumpers | one saturated flat colour each: black #2d2926, green #10cc62, purple #611b6c, blue #0074d9, white/light grey #cccccc, dark red #800000, orange #ff851b, yellow #eac80d, teal #13a3a3; black Dupont housing (#1e1616) with a silver pin and a small pale square on the housing |
| Pre-attached leads | black #2d2926, tan #b28362, red #ef3340, each ending in a black Dupont housing |
| Rocker switch | all black with white "O / I" marks |
| Potentiometer | brown body (about #9a6e4a), silver-grey bush and shaft; black knob with a silver ring and pointer line; silver-grey nut and washer |
| Buzzer | black disc with mounting ears, red and black leads into one black 2-pin housing |
| LCD module | green PCB (about #1e922e), black bezel, light grey screen (about #eaeaea), black I2C backpack with a blue trimmer, silver header pins |
| USB lead | black cable and plugs, silver USB-A shell with white insert, right-angle mini-USB plug |
| Lead lines / arrows | red #ff0000; lines thin with no head, arrows chunky 3D |
| Labels | black Arial bold on a cyan #7fdbff underline, cyan leader, dashed cyan ring at the target |
| Eye icon | solid black eye glyph, cyan leader and ring |
| Inset pictures | rounded rectangle, cyan #7fdbff border, red rectangle highlight inside |

## 6. Anomalies and inconsistencies (not conventions)

1. Step name typo: [053] is named `Ttansition` (the other 9 are `Transition`). The same typo is in Part 2 [023].
2. Wire colour does not encode function. A black jumper goes to "(+) red" (Step 9), green and white go to
   "(-) blue" (10, 13), purple is LCD GND and yellow is LCD VCC (36, 37); the switch's red lead goes to a signal row
   (j27) and its tan lead to "(+) red" (16, 17). Only the labels are reliable.
3. Jumpers are not used in ribbon order: the ribbon in Step 8 reads green, blue, purple, white, dark red, black,
   but they are used black, green, purple, blue, white, dark red.
4. Eye icon size is not quite uniform: width 7.81 % (35 uses), 7.92 % (5), 8.24 % (1, Step 40). Label anchor size is
   1.2 on 38 labels and 1.0 on 2.
5. Step 38's eye is anchored to the jumper's end housing; Steps 36, 37, 39 anchor it to the wire body.
6. Step 47's arrow is anchored to the USB-lead parts although it shows the front panel's move.
7. Step 2's four lead lines are authored in mixed directions (3 breadboard-to-base, 1 base-to-breadboard). No
   visible effect, since lines have no heads.
8. 10 toolbox annotations are never shown in the viewer (5 lead lines, 5 images): leftovers.
9. The washer is hidden from [065] Step 30 onward and never shown again. The nut is also missing on the intermediate
   front-panel copies ([105]-[121]) and returns with the final copy at [122]. Neither is noticeable under the knob.
10. A stray straight resistor-leg solid is switched on at [088] and off at [119]; I could not find it in the renders.
11. Saved step thumbnails come in three aspect ratios (1400x678 on 77 steps, 1400x676 on 47, 1400x503 on 7), so the
    views were saved in differently sized editor windows.
12. Step 29/29c turns the knob with only an eye icon; there is no arrow or picture saying which way or how far.
13. [108] is the only Transition that moves the camera, and the only one outside a `Step N`/`Step Nc` pair.
14. Digest limitations for this guide (section 2): panels F2/F4/F5/F6 missing from appear events; some lead-line
    anchors on the breadboard show as an unresolved id (`?a691dc20`).

## 7. How the full build relates to LAC parts 1-4

**Provenance.** The full build is the master. All five projects use the same CAD upload (same `cadId`, version 58),
the SolidWorks component names in the parts still read `...^LAC Full Build`, and all five carry the identical set of
150 annotation ids. Created: full build 2025-10-06; Part 1 2025-12-10 23:54, Part 2 2025-12-11 00:12, Part 3 00:53,
Part 4 00:53 (UTC). Last modified: all on 2026-01-03, except Part 3 on 2026-05-11. So the parts are clones of the
full build cut down to a slice of its steps, not the other way round.

**Mapping (verified field by field against the four part digests).**

| full build | corresponds to | renumbering | section cards carried over |
|---|---|---|---|
| [000] Start | its own title page; camera and model identical to Part 4's Start (d377, el37, az143), title image says "Full Build" instead of "Part 4" | - | - |
| [001]-[030] Step 1 ... Step 14c | Part 1 [001]-[030] | Step n = Step n | Real Time Clock |
| [031]-[070] Rocker Switch ... Step 32c | Part 2 [001]-[040] | Part 2 Step n = full Step n + 14 | Rocker Switch |
| [071]-[089] Alarm Buzzer ... Step 40c | Part 3 [001]-[019] | Part 3 Step n = full Step n + 32 | Alarm Buzzer, LCD Screen, USB Cable |
| [090]-[129] Step 41 ... Step 57c | Part 4 [001]-[040] | Part 4 Step n = full Step n + 40 | none |
| [130] Completed View | Part 4 [041] Completed View, identical (d377, el34, az45) | - | - |

32 + 42 + 21 + 42 = 137 part steps; the full build has 131. The six missing views are exactly the internal bookends.

**Dropped.** Part 1's Completed View; Part 2's Start and Completed View; Part 3's Start and Completed View; Part 4's
Start (replaced by the full build's own). **Kept.** One Start, one Completed View (Part 4's), all 5 section cards, all
10 Transitions, all 57 step pairs.

**Seams.** There are three, and nothing is inserted at them: [030] Step 14c runs straight into [031] Rocker Switch;
[070] Step 32c into [071] Alarm Buzzer; [089] Step 40c into [090] Step 41. The step after each seam ends in exactly
the same state as in the part (same camera pose, same visible parts, same annotations). Only the way in differs,
because the previous view is a wiring view instead of a title page:

| seam step | full build arrives from | camera travel in full build | camera travel in the part |
|---|---|---|---|
| [001] Step 1 | own Start | rot 109 deg, pan 118 mm, 377 to 237 mm | rot 73 deg, pan 123 mm, 277 to 237 mm |
| [031] Rocker Switch | Step 14c | rot 12 deg, pan 208 mm, 277 to 175 mm | rot 10 deg, pan 273 mm, 439 to 175 mm |
| [071] Alarm Buzzer | Step 32c | rot 88 deg, pan 110 mm, 439 to 237 mm | rot 94 deg, pan 120 mm, 513 to 237 mm |
| [090] Step 41 | Step 40c | rot 73 deg, pan 50 mm, 277 to 377 mm | rot 64 deg, pan 101 mm, 377 to 377 mm |

At [090] the part has to swap 24 parts in and 26 out (Part 4's Start shows the finished clock); the full build only
adds the two F7 uprights. At [031] and [071] the part hides 48 and 69 parts, the full build 27 and 50.

**Changed content.** Apart from the seams, the 130 mapped steps are the same in behaviour, duration, annotation
kinds, texts, anchors, lead-line lengths, camera pose and visible parts. The only differences found:

- Step name: Part 1 has `Step 14C` (capital C); the full build has `Step 14c`.
- Label position: in Step 14 the "a12" label sits at (26 %, 9 %) in the full build and (28 %, 10 %) in Part 1.
- Step 35's eye icon has a leader colour attribute set in the full build and unset in Part 3; no visible difference.
- Saved thumbnails: 109 of 130 pairs are pixel-identical within JPEG noise. Step 14 differs by the label nudge. Ten
  pairs were saved at a different aspect ratio (full [040], [041], [046]: 678 vs 676 px high; [049]-[054] and [087]:
  503 vs 700 px high). Ten pairs in Part 3 (full [079]-[086], [088], [089]) differ on about 1-3 % of pixels, all on
  shaded faces, consistent with Part 3 having been re-saved four months later.
- The `Ttansition` typo is in both, so it predates the cloning.

**What the parts add.** Each part gets its own Start (same logo and title layout, subtitle "Part n", model shown in
that part's finished state from its own hero camera: Part 1 d277 el44 az49, Part 2 d439 el35 az141, Part 3 d513 el30
az142, Part 4 d377 el37 az143) and its own Completed View (same state, no annotations, hero angle). Parts 2 and 3 open
directly on a section card after Start; Parts 1 and 4 open on Step 1.

**Other LAC guides (metadata only, not analysed here).** `19075-lac_electronics` carries the same 150 annotation ids
(3 steps: All Electronics, All Wood, Start). `19075-lac_deconstruction` shares 144 of its 199 annotation ids with the
full build and was created 2025-11-26, between the full build and the parts.
