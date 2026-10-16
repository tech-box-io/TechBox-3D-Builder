# Guide report: LCD Alarm Clock (LAC) - Part 3

- Guide id: `19075-lcd_alarm_clock_lac_-_part_3` (kit LAC, role: part)
- Sources read: `digest/19075-lcd_alarm_clock_lac_-_part_3.md` (all), all 3 contact sheets, all 21 thumbs, targeted queries on `cadasio_raw/…part_3.json`.
- Working files (scripts, crops): `reports/_work_lac_p3/`

## 1. Summary

Part 3 is a pure wiring guide: nothing is screwed, slotted or glued. Starting from the flat "electronics laid out on the table" state that Part 2 ends in (breadboard with Nano and RTC on wooden panel F3, switch and potentiometer panels lying around it), the student connects three bought-in components to the breadboard: the piezo **alarm buzzer** (2 captive leads), the **20x4 I2C LCD** (4 loose male-female jumper wires peeled from one ribbon), and the **USB cable** (plugged into the Nano). It has 21 viewer steps: a title page, 3 section cards, 8 numbered steps each with a "c" twin, and a Completed View. Every step is `pause`, 800 ms; there are no Transition steps, no red lead lines, no arrows, no part rotations and no written instructions at all. The whole instruction vocabulary is: an eye icon on the thing to pick up, one or two light-blue underlined labels naming where each wire end goes (`GND` -> `(-) blue`, `SDA` -> `b8` ...), and a cross-fade from a loose straight wire to the same wire routed in place.

## 2. Step table (every viewer step)

Screen positions are % of viewport (x from left, y from top). Camera = distance / elevation / azimuth.

| idx | name | kind | what is added or done | annotations | camera |
|---|---|---|---|---|---|
| 000 | Start | title page | Shows the finished Part 3 state (70 parts / 800 solids, same as 019-020): LCD, buzzer and USB cable already wired. Model sits right of centre. | 2 unanchored images: TechBox logo SVG (w 38.9%, at 2%,6%); title PNG "LCD Alarm Clock (LAC) / Part 3 / (c) 2025 TechBox. A division of TARIS Industries, LLC. All Rights Reserved." (w 42.1%, at 2%,64%) | MOVES. 513 mm / 30 deg / 142 deg (widest view of the guide) |
| 001 | Alarm Buzzer | section card | Everything hidden except the buzzer with its two straight leads and Dupont pins (5 parts / 9 solids). Nothing moves. | Eye icon (32%,16%) -> centre of buzzer top face | MOVES. 237 mm / 56 deg / -47 deg (zoom x2.16) |
| 002 | Step 1 | hover | Assembly fades back (55 parts). Buzzer is simply present, resting ~30 mm off the end of the breadboard, leads straight and pointing away from the board. Task: red lead to hole j4. | Eye (35%,58%) -> red lead's Dupont housing; label `j4` (30%,37%) -> breadboard hole j4 | MOVES a little (9.5 deg). 277 mm / 48 deg / -38 deg |
| 003 | Step 1c | completed | Straight red lead (Part38 + cap V2-39) fades out; routed red lead (Part29 + cap V2-28) fades in plugged into j4. Black lead still straight. | none (both removed) | unchanged |
| 004 | Step 2 | hover | No 3D change. Task: black lead to the negative rail. | Eye (33%,65%) -> black lead's Dupont housing; label `(-) blue` (58%,14%) -> hole in the blue-striped rail | unchanged |
| 005 | Step 2c | completed | Straight black lead (Part37 + V2-37) swapped for routed black lead (Part30 + V2-29). | none | unchanged |
| 006 | Step 3 | hover, isolated prep | Everything hidden. A 4-way male-female ribbon jumper (purple, yellow, teal, blue; 4 wires + 4 male pin caps + 4 female housings = 12 parts) shown alone, wires still joined at 1.75 mm pitch. | Eye (53%,23%) -> middle of the ribbon (yellow wire). No text. | MOVES (121 deg). 110 mm (closest view of the guide); scene up-axis flipped to -y |
| 007 | Step 3c | completed | Ribbon peeled into 4 single wires: purple slides -14.4 mm, yellow -8.4 mm, blue +11.3 mm sideways in the ribbon plane, teal stays (gaps 7.8 / 10.1 / 13.1 mm). The only tweened part motion in the guide. | none | unchanged |
| 008 | LCD Screen | section card | Everything hidden; LCD module alone (124 solids), display side to camera. | Eye (36%,61%) -> centre of LCD glass; photo inset (w 29%, at 55%,6%, light-blue rounded frame) of the I2C backpack with a red rectangle round the GND/VCC/SDA/SCL pins, leader -> header on the 3D LCD | MOVES (65 deg). 150 mm; scene up-axis -x |
| 009 | Step 4 | hover | Assembly fades back (59 parts) with the LCD lying face-down beside the breadboard, backpack up (the LCD is never "placed" by a step). Loose purple wire staged in the foreground. | Eye (30%,64%) -> mid-point of purple wire; `GND` (21%,49%) -> GND pin of LCD header; `(-) blue` (69%,41%) -> hole in blue rail | MOVES (167 deg swing to the opposite side). 323 mm / 51 deg / 127 deg; up-axis back to +y |
| 010 | Step 4c | completed | Loose purple (Copy of Part15 + caps) fades out; routed purple (Part34 + V2-34 + Cap-8) fades in from LCD GND to the (-) rail. | none (3 removed) | unchanged |
| 011 | Step 5 | hover | Loose yellow wire appears at the same staging spot. | Eye (28%,63%) -> mid yellow wire; `VCC` (19%,48%) -> VCC pin; `(+) red` (69%,36%) -> hole in red rail | unchanged |
| 012 | Step 5c | completed | Swap to routed yellow (Part35 + V2-35 + Cap-7). | none | unchanged |
| 013 | Step 6 | hover | Loose teal wire at the staging spot. | Eye (25%,61%) -> female housing end of the teal wire; `SDA` (19%,48%) -> SDA pin; `b8` (55%,19%) -> hole b8 | unchanged |
| 014 | Step 6c | completed | Swap to routed teal (Part36 + V2-36 + Cap-6). | none | unchanged |
| 015 | Step 7 | hover | Loose blue wire at the staging spot. | Eye (26%,66%) -> blue wire near its female end; `SCL` (19%,51%) -> SCL pin; `b9` (56%,17%) -> hole b9 | unchanged |
| 016 | Step 7c | completed | Swap to routed blue (Part39 + V2-40 + Cap-5). All 4 LCD wires in. 68 parts. | none | unchanged |
| 017 | USB Cable | section card | Everything hidden; loose straight USB cable alone (right-angle mini-B plug one end, USB-A the other). | none | MOVES (82 deg). 277 mm / 47 deg / -45 deg |
| 018 | Step 8 | hover (target only) | Assembly fades back (67 parts) WITHOUT the cable. Only the destination is shown. | Eye (34%,52%, w 8.24%) -> the Nano's mini-USB socket | MOVES (21.5 deg, same distance). 277 mm / 29 deg / -62 deg (lowest elevation, looks into the socket) |
| 019 | Step 8c | completed | Routed cable fades in already plugged in (sheath Part67 + right-angle plug + USB-A end); USB-A end left free on the table. 70 parts / 800 solids. | none | unchanged |
| 020 | Completed View | final | No part change. | none | MOVES (120 deg). 439 mm / 30 deg / 128 deg (zoom x0.63), layout centred |

Totals: 21 steps, all `pause`, all 800 ms; camera moves on 9, is unchanged on 12; annotations ever shown: 13 images (10 eye icons, 1 photo inset, 2 title-page images) and 10 labels; 0 lead lines, 0 arrows.

## 3. Conventions (evidence and exceptions)

### Structure
1. **Skeleton**: Start (title) -> [section card -> Step N / Step Nc pairs] x3 -> Completed View. 21 = 1 + 3 + 8x2 + 1. *Always*: every numbered step has a "c" twin (8/8, all lowercase c). Numbering is continuous 1-8 across the section cards and restarts at 1 for this Part (the Full Build calls the same steps 33-40).
2. **Every step waits for the student**: 21/21 `pause`, 800 ms. No `play`/Transition steps (0/21), even for the 167 deg camera swing into [009] and the 121 deg swing into [006]. This is the only LAC part with zero Transitions.
3. **No written instructions**: step `description` empty and no popup on 21/21 steps. The picture plus at most 3 annotations is the whole instruction.
4. **Section card before each new bought-in component**: [001] Alarm Buzzer, [008] LCD Screen, [017] USB Cable. Named after the component, unnumbered, shows the component alone on white (5, 1 and 1 top-level parts visible; everything else hidden), camera zoomed onto it, no part motion. The card title exists only as the step name; there is no on-canvas title text. *Exceptions*: the ribbon jumper gets no card (Step 3 is its introduction); the USB card has no annotation while the other two have an eye icon.
5. **Title page shows the end state of this Part**, not the start state: same 70 parts / 800 solids as the Completed View, similar 3/4 angle (30 deg / 142 deg vs 30 deg / 128 deg) but pulled back (513 vs 439 mm) and shifted right to leave the left third for logo and title images.

### Granularity
6. **One connection per numbered step.** 6 of 8 steps add exactly one wire (Steps 1, 2, 4, 5, 6, 7), Step 8 adds one cable. Never two wires in one step, even when the four LCD wires go to four adjacent header pins and two adjacent holes (b8, b9).
7. **The one grouped step is a preparation step**: Step 3 handles 4 wires at once because they are physically one item (a ribbon) that has to be split before use; it is shown in isolation with nothing else on screen.
8. **Loose components are never "placed" by a step.** Buzzer and LCD are introduced by their card and are then simply present beside the breadboard when the assembly fades back ([002], [009]). Steps are spent only on connections. (Nothing is mechanically mounted in this Part.)

### Ordering
9. Section order: buzzer -> LCD -> USB cable (the power/programming cable is last).
10. LCD wires go in header pin order GND, VCC, SDA, SCL, which is also the ribbon order purple, yellow, teal, blue and happens to be power pair before signal pair. *Exception to "power first"*: the buzzer is wired signal first (red -> j4, Step 1) and ground second (black -> (-) rail, Step 2).

### Motion and wiring
11. **Straight-to-routed swap, no travel** (6/6 wire steps): `Step N` shows a loose straight wire model; `Step Nc` fades it out and fades in a separately modelled routed wire at its installed position (APPEAR + DISAPPEAR, zero MOVE). The wire never flies to its seat.
12. **Staging spot for free jumper wires** (Steps 4-7, 4/4): each loose wire appears at the same place, repeatable within ~4 mm: straight, horizontal, parallel to the breadboard's long axis, about 60 mm above the breadboard top and beyond the panel edge on the camera side, i.e. floating between camera and model in the lower-left of the frame (x 33-53%, y 58-89%). It is 110-140 mm from its two destinations (the wire is ~80 mm long) and, being ~1.6x nearer the camera than the board, renders ~1.6x larger than true scale. True displacement from its CAD parking pose is +181.5 to +184.5 mm along X only.
13. **Captive leads use their own straight form as the "hover"** (Steps 1-2): the buzzer's leads stick straight out of the buzzer, away from the breadboard; one lead per step is swapped for its routed form.
14. **Male end to the breadboard, female end to the module header** for all 4 LCD jumpers (routed models show the black female housing on the LCD's right-angle header and the pin in the breadboard).
15. Only real part travel: Step 3c, a sideways slide of 3 of 4 wires by 8.4-14.4 mm (tween). No rotations on any step (0/21).
16. USB cable (Step 8/8c) follows a third pattern: loose part seen only on the card, `Step 8` shows just the destination, `Step 8c` fades the installed cable in.

### Red lead lines and arrows
17. **None.** 0 lead lines and 0 arrows are visible on any of the 21 steps. (The 49 lead lines and 7 arrows in the digest's annotation inventory belong to other sections of the shared LAC Full Build project; only 23 of 150 toolbox items are used here.) In this guide wiring is explained with labels, not with lead lines.

### Labels
18. **One style for all 10 labels**: bold black Arial 3em, sitting on a light-blue `#7fdbff` underline (thickness 5); the leader continues from the end of the underline as one elbowed line of the same colour and thickness, ending in a dashed "life-saver" ring (size 1.2) on the exact feature. Default box 175x90 px, wider for long text.
19. **Vocabulary**: breadboard hole = lowercase column letter + row number (`j4`, `b8`, `b9`); power rails = polarity in brackets + stripe colour (`(-) blue`, `(+) red`); module pin = its silkscreen name in capitals (`GND`, `VCC`, `SDA`, `SCL`). No verbs, no part names, no wire colours.
20. **One label per wire end the student has to find**: 2 labels for a free jumper (module pin + breadboard hole; Steps 4-7, 4/4), 1 label when the other end is captive (Steps 1-2, 2/2), 0 for the prep step and the USB step.
21. **Anchoring is exact**: each pin label is linked to a different pin solid of the 4-pin header (targets ~2.5 mm apart); each breadboard label is linked to the breadboard top face with a 3D target on the specific hole.
22. **Labels live only in `Step N`** and are all removed in `Step Nc` (8/8). Fade in/out.
23. **Placement**: in screen space on white, outside the model. In the four LCD steps the pin label sits in the same slot left of the LCD (19-21%, 48-51%) and the breadboard label upper-right of the board (55-69%, 17-41%); leaders are roughly 15-30% of the frame long and cross the model to reach the feature.

### Eye icon
24. **Exactly one eye icon on every `Step N`** (8/8) and on 2 of 3 cards; never on `Step Nc`, the title page or the Completed View. Black eye glyph PNG, 7.81% of viewport width, light-blue leader and life-saver ring like the labels.
25. It marks the thing to pick up: the loose wire or its connector in 7 of 8 steps (Dupont housing in Steps 1-2, ribbon in Step 3, mid-wire in Steps 4-5, female end in Steps 6-7). *Exception*: Step 8, where it marks the destination socket because the cable is not on screen.
26. It sits beside the loose part on the side away from the model (lower-left, x 25-35%, y 58-66% in wiring steps), never over the model.

### Images
27. **Photo inset on a section card** (1 of 3 cards): the LCD card carries a real photo of the I2C backpack with a red rectangle round the 4 pins about to be wired, top-right, 29% of viewport width, light-blue rounded frame and leader to the 3D part. It previews the four pin names used as labels in Steps 4-7.
28. Title page is built from two images (logo SVG top-left, title/copyright PNG lower-left), not text labels.

### Camera
29. **Never moves between `Step N` and `Step Nc`** (0/8).
30. **Held fixed for a whole run of steps in one work area**: 4 buzzer steps [002]-[005], 8 LCD steps [009]-[016], 2 USB steps [018]-[019].
31. **Moves on**: every card (3/3), the first step after every card (3/3), the isolated prep step [006], Start and Completed View. 9 moves / 21 steps.
32. **Wiring framing is the whole connection, not a close-up of the hole**: both endpoints and the staged loose wire are in frame together; breadboard spans ~20-24% of frame width; elevated 3/4 view (48-51 deg, 277-323 mm). The side is chosen so the module's connector faces the camera (azimuth -38 deg for the buzzer side, 127 deg for the LCD header side). The USB step drops to 29 deg to look into the Nano's socket.
33. Cards zoom onto the single part (110-277 mm); scene up-axis is switched for isolated views (-y at [006], -x at [008], back to +y at [009]) to pose the part instead of rotating it.
34. Camera animation: tween, speed 2, orbit off; perspective, fov 45.

### Look
35. White `#ffffff` background; all parts "toon" (flat, unshaded) with 1 px black edges (edge angle 40 deg), no silhouette; ambient light 1.75. Show/hide = fade, move = tween.

## 4. Part looks (from the renders)

| part | look |
|---|---|
| Background | plain white |
| Wooden panels (F3, F4, frame panel) | flat light tan (renders ~`#fcd49c`, material `#deb887`), black outline, panel id ("F3", "F4") engraved in black on the face |
| Breadboard | white body, grid of small black square holes, thin red and blue rail stripes, tiny black row numbers and a-j column letters |
| Arduino Nano | dark navy PCB (~`#001048`), black chip, silver pins and mini-USB socket |
| RTC module | bright blue PCB standing upright, large silver coin cell lettered "CR2025 3 VOLTS" |
| LCD 20x4 | bright green PCB (`#1c902c`), near-black bezel (`#201818`), flat light-grey glass (`#e8e8e8`), row of silver header pins; black I2C backpack with blue trimmer and 4 silver right-angle pins |
| Piezo buzzer | all near-black disc with mounting ears, moulded ring pattern; twin lead red + black |
| Jumper wires | saturated flat colours, thin black outline: purple (`#611b6c`), yellow (`#eac80d`), teal (`#13a3a3`), blue (`#0074d9`), red (`#ef3340`), black (`#2d2926`), plus orange, green, tan-brown, white and maroon from earlier parts |
| Dupont ends | black rectangular housing; male end has a short silver pin, female end is a longer plain black housing |
| USB cable | near-black sheath and plugs with strain-relief ribs, silver metal shells, white insert with two square holes in the USB-A end |
| Resistors, switch, potentiometer (earlier parts) | blue resistor bodies with coloured bands and silver legs; black rocker switch; brown potentiometer knob |
| Labels | black bold text on light-blue underline, light-blue leader and dashed ring |
| Eye icon | solid black eye with white iris ring, light-blue leader and dashed ring |
| Title page | cyan (`#00b0ec`) rounded TechBox logo block with white lettering; title in dark grey (`#585858`) condensed bold; small black serif copyright line |

## 5. Anomalies and inconsistencies

Authoring:
- **Step 3/3c sits in the wrong section**: splitting the ribbon prepares the LCD wires but comes before the "LCD Screen" card, so it falls under "Alarm Buzzer".
- **USB Cable card has no eye icon**; the other two cards do.
- **Step 8 breaks the hover pattern**: no loose part on screen, eye icon on the destination instead of on the part.
- **Eye icon anchor point is inconsistent on like-for-like steps**: mid-wire in Steps 4-5, female-end housing in Steps 6-7. Eye width is 8.24% in [018] vs 7.81% elsewhere; ring size 1 in [011] vs 1.2 elsewhere.
- **Colour words can mislead**: `(-) blue` and `(+) red` name the rail stripe, not the wire. Step 4 sends a purple wire to "(-) blue", Step 5 a yellow wire to "(+) red", and Step 7 uses a blue wire for SCL. GND/VCC are not on black/red wires because the colours come from the ribbon.
- **Order rule differs between sections**: buzzer is signal then ground; LCD is ground, power, then signals.
- Hidden authoring step 0 still carries Cadasio's default text "A Start point for your project - feel free to rename, reorder or delete".
- The "LCD Screen" card keeps internal index 79 (its position in the Full Build) while every other step's index equals its position here.
- The four loose wires are recoloured light grey `#cad1ed` at [008] while hidden, then recoloured correctly when shown; invisible leftover.
- 1 mm nudges on the installed USB pieces (plug +1 mm X, USB-A end -1 mm X, sheath +1 mm Z) set at Start; invisible to the student.
- The saved render for [017] is a later re-capture (3840x1919, timestamp 11 May 2026, the guide's last-modified date) than the others (2559x1239, timestamps 23 Nov 2025 and 3 Jan 2026).

Data-reading caveats (digest, not authoring):
- **Cadasio `position` is an absolute instance translation, not an offset from the seated pose.** For parts whose base transform has a non-zero translation, the digest's "displaced by" value includes that translation. Checked by projecting anchors to the screen: the stored 2D target of the eye on the purple wire is (42.7%, 72.3%); "position replaces translation" predicts (43.3%, 71.0%), "position adds to translation" predicts (61.9%, 4.3%). Consequences here: the loose LCD wires' real displacement is +181.5..184.5 mm in X only (not the mixed vectors listed), and the "parts still displaced" lists (LAC Resistor, F3, Breadboard, nano, LAC Knob, LAC Nut, USB parts) are artefacts; e.g. LAC Nut-4's position equals its base translation exactly.
- [017] digest says the USB cable shows 1 of 9 solids; the raw data turns all 9 on and the render shows the whole cable (the sub-assembly references are flagged hidden in the structure and the digest does not see the leaf overrides).
- Digest colour name "dark grey" for `#611b6c` is purple on screen.
- Digest camera elevations of -47 deg / -39 deg at [006]-[008] are relative to world +Y; with the up-axis flipped the student sees a normal from-above view.

## 6. Relation to the other LAC guides

- **Exact slice of the Full Build**: Part 3 [001]-[019] equals `19075-lac_full_build` [071]-[089] (Alarm Buzzer, Steps 33-35, LCD Screen, Steps 36-39, USB Cable, Step 40) step for step: same camera, same part counts, same annotations and screen positions on 19/19 steps. Only the step numbers (33-40 -> 1-8), the Start page (own title PNG, own camera) and the Completed View are specific to the Part.
- Built from the same Cadasio project: assembly is named "LAC Full Build", parts are `PartNN^LAC Full Build`, and 127 of 150 toolbox items are unused leftovers.
- **Continuity**: Part 1 has 14 steps and Part 2 has 18, so Part 3 starts at Full Build step 33. Part 3 Step 1 shows Part 2's finished state plus the buzzer (50 parts / 642 solids + 5 / 9 = 55 / 651). Part 3's Completed View camera (439 mm / 30 deg / 128 deg) is practically Part 2's (439 / 32 / 127). Part 4 Step 1 is Full Build step 41.
- **Differences in kind**: Part 3 is the only LAC part with no Transition steps (Part 1 has 1, Part 2 has 3, Part 4 has 6) and no lead lines or arrows (annotation turn-on events elsewhere: Part 1 12 lead lines + 1 arrow; Part 2 5 + 3; Part 4 27 + 3). It has the most section cards: 3, against 1 in Part 1 ("Real Time Clock"), 1 in Part 2 ("Rocker Switch") and none in Part 4.
- I did not open the other LAC guides' renders; the comparison above is from their digests only.
