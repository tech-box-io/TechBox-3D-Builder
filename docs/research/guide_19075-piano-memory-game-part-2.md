# Guide report: `19075-piano-memory-game-part-2` (Piano Memory Game, Part 2)

Kit: PMG. Role: part (2 of 3). Sources read: full digest (`digest/19075-piano-memory-game-part-2.md` + `.json`), all 4 contact sheets, 23 of the 27 individual frames (009, 016, 018, 020 on the sheets only) plus zoomed crops of the raw 2560/3840 px renders, and targeted queries of `cadasio_raw/19075-piano-memory-game-part-2.json` (helper scripts and crops are in `reports/_work_pmg_p2/`).

## 1. Summary

Part 2 is a pure wiring guide. Starting from the Part 1 result (Nano on its I/O shield with four big push-button modules already wired), the student separates a 9-wire female-female ribbon into single jumpers, wires the TM1637 4-digit display to the shield with 4 of them, wires the 32x8 MAX7219 dot-matrix display with the other 5, and finally plugs a right-angle Mini-USB cable into the Nano. The guide has 27 viewer steps: a title page, three unnumbered section cards (`4-Digit Display`, `Dot Matrix Display`, `USB Cable`), eleven numbered `Step N` / `Step Nc` pairs, and a `Completed View`. Every step is a `pause` step of 800 ms; there are no auto-advancing Transition steps, no step descriptions, and no popups. The only words the student sees are 18 pin-name labels (two per wire) and the title image. Wires are never animated into place: `Step N` shows a loose straight wire plus two pin labels and an eye icon, and `Step Nc` cross-fades to a pre-routed wire seated at both ends. The single red lead line in the guide is for the USB plug, the only part that tweens to its seat.

## 2. Step table (every viewer step)

Camera columns: d = camera distance in mm, el = elevation, az = azimuth. "same" = camera did not move on entering the step. Labels are listed module-side first, shield-side second.

| idx | name | kind | what is added / done | annotations | camera |
|---|---|---|---|---|---|
| 000 | Start | title | Finished Part 2 assembly as hero model on the right half (74 top-level CAD parts: shield, Nano, 4 button modules, display, matrix, 21 routed wires + 42 housings, USB cable plugged in) | 2 unanchored images: TechBox logo SVG top-left (at 2.4 %, 8.1 %; width 39.5 % of viewport) and a title PNG lower-left (at 1.6 %, 64.6 %; width 46.5 %) carrying the kit name, "Part 2" and a copyright line | set: d 436, el 35, az -55 |
| 001 | 4-Digit Display | section card | Everything hidden except the TM1637 display, seen face-on | 1 photo inset (back of the real module, red rectangle round the CLK/DIO/VCC/GND header), 5 px cyan rounded frame, width 33.6 %, at (55.7 %, 31.1 %); cyan leader + dashed ring to the model's pin header | MOVES: zoom x4.79, d 91, el 3, az -91 |
| 002 | Step 1 | hover (prep) | Display hidden. A 9-wire ribbon (9 wires + 18 black housings) fades in alone, wires touching at 1.75 mm pitch | none | MOVES: d 103, el 49, az -53, centred on the ribbon |
| 003 | Step 1c | completed (prep) | The 9 wires tween sideways by -11.9 ... +9.3 mm so the pitch opens from 1.75 mm to about 4.4 mm: "separate the ribbon into single wires" | none | same |
| 004 | Step 2 | hover | Part 1 assembly + display fade in; 8 loose wires fade out; the gold wire stays as the staged loose wire (lower right) | labels `clk`, `s8`; eye icon -> loose gold wire | MOVES: zoom x0.6, d 173, el 25, az -72 |
| 005 | Step 2c | completed | Straight gold wire fades out, routed gold wire fades in seated on display CLK and shield S8 | all 3 removed | same |
| 006 | Step 3 | hover | Loose black wire fades in (lower left) | labels `dio`, `s9`; eye -> black wire | same |
| 007 | Step 3c | completed | Swap to routed black wire (DIO -> S9) | removed | same |
| 008 | Step 4 | hover | Loose purple wire | labels `VCC`, `V9`; eye | same |
| 009 | Step 4c | completed | Swap to routed purple wire (VCC -> V9) | removed | same |
| 010 | Step 5 | hover | Loose red wire | labels `GND`, `G9`; eye | same |
| 011 | Step 5c | completed | Swap to routed red wire (GND -> G9) | removed | same |
| 012 | Dot Matrix Display | section card | Everything hidden except the 32x8 LED matrix | 1 photo inset (back of the 4-module PCB, red rectangle round the input header VCC/GND/DIN/CS/CLK), cyan frame, width 36.7 %, at (7.1 %, 15.3 %); cyan leader from the red rectangle to a dashed ring on the model's header pins | MOVES: d 236, el 12, az -95 |
| 013 | Step 6 | hover | Assembly (now with 4 display wires) re-appears with the matrix in place; loose dark-brown wire below the shield | labels `VCC`, `V11`; eye | MOVES: d 202, el 30, az -81 |
| 014 | Step 6c | completed | Swap to routed dark-brown wire (VCC -> V11) | removed | same |
| 015 | Step 7 | hover | Loose green wire | labels `GND`, `G11`; eye | same |
| 016 | Step 7c | completed | Swap to routed green wire (GND -> G11) | removed | same |
| 017 | Step 8 | hover | Loose navy wire | labels `DIN`, `S11`; eye | same |
| 018 | Step 8c | completed | Swap to routed navy wire (DIN -> S11) | removed | same |
| 019 | Step 9 | hover | Loose maroon wire | labels `CS`, `S12`; eye | same |
| 020 | Step 9c | completed | Swap to routed maroon wire (CS -> S12) | removed | same |
| 021 | Step 10 | hover | Loose teal wire | labels `CLK`, `S13`; eye | same |
| 022 | Step 10c | completed | Swap to routed teal wire (CLK -> S13) | removed | same |
| 023 | USB Cable | section card | Everything hidden except the USB cable (cable body + USB-A plug + right-angle Mini-USB plug) | none | MOVES: rotate 96.6 deg, d 202, el 38, az +47 |
| 024 | Step 11 | hover | Whole assembly re-appears; cable hovers 22.9 mm out of the Nano's Mini-USB socket, on the socket axis | 1 red lead line, 28.5 mm, plug -> socket | MOVES: d 275, el 23, az +90 (rear view) |
| 025 | Step 11c | completed | Cable tweens 22.9 mm straight into the socket | lead line removed | same |
| 026 | Completed View | completed view | Nothing changes in the model | none | MOVES: 119.4 deg orbit back to the front, d 275, el 37, az -82 |

Totals: 27 steps = 1 title + 3 cards + 11 `Step N` + 11 `Step Nc` + 1 Completed View. Annotations actually shown: 18 labels, 9 eye icons, 2 photo insets, 2 title images, 1 lead line, 0 arrows.

## 3. Conventions found

### 3.1 Structure

- **Fixed skeleton** (always): `Start` -> for each new component: named section card -> numbered pairs -> `Completed View`. Evidence: [000]; cards [001] [012] [023]; pairs [002]-[011], [013]-[022], [024]-[025]; [026].
- **Every numbered step is a pair** (11 of 11): `Step N` tells the student what to pick up and where it goes (annotations on); `Step Nc` shows the result (annotations off). No `Step N` lacks its `c` twin in this guide.
- **Numbering is continuous across sections** (1 to 11); cards are unnumbered and named after the component they introduce.
- **Everything waits for the student**: 27 of 27 steps are `pause`, all 800 ms. No `play`/Transition steps, so each camera move shares the same 800 ms as the content change. This differs from the other PMG guides (see section 6).
- **No written instructions**: description is empty on 27 of 27 steps and there are no popups. Meaning is carried by pin labels, the eye icon, photo insets and the model.
- **Section card = isolation shot**: on all 3 cards every other part is hidden and the new component is shown alone. 2 of 3 cards add a photo inset; the `USB Cable` card [023] has no annotation at all.
- **Title page**: logo and title are images, not text labels; the hero model is this part's finished state, not the whole kit.
- **Completed View** repeats the last `Nc` state with a new camera only (one property change in the raw step: the camera).
- Hidden authoring steps: 4 (three before `Start`, one between `Step 10c` and `USB Cable`). They set base visibility/colours and are never seen.

### 3.2 Granularity

- **One wire per step, always** in the wiring steps: Steps 2-10 each add exactly one jumper (1 wire body + its 2 housings). 9 of 9.
- **Grouping happens only for a preparation action or a rigid unit**: Step 1 [002]-[003] handles all 9 wires at once because the action is "split the ribbon"; Step 11 [024]-[025] moves 3 CAD components (cable, two plug ends) as one cable.
- **Modules get no placement step**. The display and the matrix are introduced by their card and are simply present, already in their final position, when the next numbered step brings the assembly back ([004], [013]). 2 of 2.

### 3.3 Ordering

- Section order: display, then matrix, then the USB cable last.
- **Within a section, wires follow the module header's pin order from top pin to bottom pin**: display CLK, DIO, VCC, GND ([004] [006] [008] [010]; pin heights 929 -> 922 mm); matrix VCC, GND, DIN, CS, CLK ([013] [015] [017] [019] [021]; 929.5 -> 919.4 mm). The same order is also the ribbon's colour order and ascending shield pin number (8, 9, 9, 9, then 11, 11, 11, 12, 13).
- It is **not** "power before signal": the display's power wires come last, the matrix's come first. Pin order is the rule that holds in both sections.
- Preparation (ribbon separation) comes before any wire is used.

### 3.4 Motion

- **Jumper wires are swapped, not moved** (9 of 9). `Step N`: a straight loose wire model fades in at a staging spot. `Step Nc`: that model fades out and a different, pre-routed wire model fades in already seated. No travel path, no rotation.
- **Staging spot of the loose wire**: lying horizontally, parallel to the row of modules, about 40-55 mm on the camera side of the shield's near edge and roughly level with the top of the Nano, so it reads as "on the bench below the assembly". It is 50-100 mm from where it will be plugged; it is not placed near its pins. Steps 2 and 6-10 use the ribbon's own spot; Steps 3-5 use a spot 40 mm further toward the display.
- **Only two real tweens in the guide**: the ribbon fan-out [003] (27 parts, sideways, up to 11.9 mm) and the USB insertion [025] (22.9 mm, one straight move along the socket axis).
- **Rigid connector hovers on its mating axis**: the cable first appears 22.9 mm withdrawn straight out of the socket ([023], [024]), then slides in. One instance.
- No rotations (0 steps) and no multi-stage moves.
- Appear/disappear is always a fade; moves are tweens.

### 3.5 Red lead lines and arrows

- **Exactly one lead line, used for the one part that physically slides in** [024]. Red `#ff0000`, solid, thin, straight, 2 points.
- Start: the root of the metal Mini-USB plug, where it meets the black right-angle housing (7.0 mm behind the plug tip, on the plug's centre line). End: the centre of the Nano's Mini-USB socket core, 4.8 mm inside the socket mouth. Both ends share the same X and Y, so the line lies exactly on the insertion axis.
- Length 28.5 mm against a hover of 22.9 mm (ratio 1.24). Only the 16.7 mm gap between plug tip and socket mouth is visible; the rest is inside the two parts.
- Shown on `Step 11` only and removed on `Step 11c`.
- **No lead lines for wires** (0 of 9 wiring steps) and **no arrows** anywhere.

### 3.6 Labels

- **Two labels on every wiring `Step N`** (9 of 9, 18 labels): the module-side pin name as silk-screened on the module, and the shield-side pin as row letter + number (S = signal, V = VCC, G = GND).
- **One house style** (18 of 18, preset named "tech box label"): bold black text at 3 em (base font 20 px), centred in a 175 x 90 px box with no box outline, a 5 px cyan `#7fdbff` underline, and a 5 px straight cyan leader ending in a dashed cyan ring.
- The leader leaves the end of the underline that faces the target: right end on 12 labels, left end on 6.
- **Leader tips**: on the module side the tip sits on the exact pin, near its free end (9 of 9). On the shield side the tip marks the pin position along the header to within about one pin; the ring is about 5 mm across on the model, roughly two pin pitches, so the label text is what identifies the row.
- **Placement**: labels are positioned in screen space in clear white area and stay in nearly the same place from step to step within a section. From the underline end to the target the leader spans about 4-10 % of the viewport width and 8-15 % of its height. The label box itself is about 6.8 % of the width and 9.8 % of the height of the 2560 x 919 renders.
  - Display section: module label at (20.7-24.4 %, 17.4-18.4 %), shield label at (58.1-60.8 %, 41.3-42.5 %).
  - Matrix section: shield label at (18.1-23.1 %, 47.8-51.8 %); module label at (43.5-44.2 %, 14.0-18.6 %) for VCC, GND, CS and at (60.9-63.5 %, 12.0-13.3 %) for DIN, CLK.
  - 13 of 18 labels sit above their target; the 5 matrix-section shield labels sit below-left with the leader rising.
- Labels exist only on `Step N` and are gone on `Step Nc` (9 of 9).

### 3.7 Eye icon

- A black eye icon (width 8.2 % of the viewport) with a cyan leader and dashed ring points at the loose wire on every wiring `Step N` (9 of 9). It never appears on `c` steps, cards, Step 1 or Step 11. It reads as "find this wire".
- The leader leaves the eye's right edge. The ring sits near the wire's midpoint on 6 steps and near its left end on 3 (Steps 3-5).
- The eye sits beside the wire in white space: up-left of it in the display section, below-left in the matrix section.

### 3.8 Photo insets

- Both module cards ([001], [012]) show a real photo of the module's back with a red rectangle round the header the student is about to use, inside a 5 px cyan rounded frame, joined by a cyan leader and dashed ring to the same header on the 3D model. Widths 33.6 % and 36.7 % of the viewport.
- On [012] the leader starts inside the red rectangle; on [001] it emerges from the photo's edge at mid-height.

### 3.9 Camera

- **The camera stays put while one module is being wired.** It never moves between `Step N` and `Step Nc` (0 of 11), and Steps 2-5 share one view, Steps 6-10 another.
- It moves on 9 of 27 steps only: [000], [001], [002], [004], [012], [013], [023], [024], [026]. That is on entering a card, on the first numbered step after a card (or after the ribbon prep), and at the Completed View.
- **Wiring view**: three-quarter from the front and above, elevation 25-30 deg, azimuth -72 to -81 deg. Distance steps back as the assembly grows: 173 mm, 202 mm, 275 mm.
- **Card view**: closer and flatter for flat modules (elevation 3 and 12 deg), with the component off-centre to leave room for the photo; elevation 38 deg for the cable.
- **The camera goes to the side that exposes the mating feature**: Step 11 is seen from the rear (azimuth +90 deg, about a half-turn from the wiring view). From there the Nano's USB socket is not behind the wire bundle, and the view direction is square to the insertion axis, so the 22.9 mm move and the lead line run horizontally across the screen. The reason is my reading of the renders; the data only records the camera. The Completed View then orbits back.
- Framing is loose. In the saved 2.79:1 renders the model fills about 24 % x 50 % of the frame in the display section, 59 % x 43 % in the matrix section and 61 % x 55 % for the USB step.
- Perspective camera, FOV 45.

### 3.10 Look

- White background `#ffffff`, toon shading with black outline edges on every part, no shadows, no ground plane.
- **Parts keep their real colours. There is no highlight colour on the new part and no ghosting of earlier parts**: no colour or opacity changes on any wiring step.
- **Two annotation colours with fixed jobs**: cyan `#7fdbff` for everything informational (label underlines, leaders, rings, photo frames) and red `#ff0000` for the motion lead line and the rectangles inside the photos.
- Modules hang in space at fixed positions (display left, buttons above, shield below, matrix right); no table or enclosure is drawn.

### 3.11 Wiring specifics

- **Wire identity is colour**: every jumper has its own saturated colour, the loose and routed versions match, and the Dupont housings are always black.
- Wires are consumed in ribbon order, edge to edge: gold, black, purple, red, then dark brown, green, navy, maroon, teal.
- Colours follow the ribbon, not electrical convention (see anomalies).
- Routed wires are smooth drooping curves from the module pins down to the shield header, with the housing drawn seated on the pins.

## 4. Part looks

CAD hex first; the renders are brighter because of the lighting (ambient 1.875, directional 1.15).

| part | look |
|---|---|
| Background | plain white |
| Nano I/O shield PCB | saturated royal blue slab (renders about `#2868f8`) with black outline and small edge holes |
| Shield 3-row pin headers | pale yellow plastic bases with light grey pins |
| Shield sockets for the Nano | black blocks |
| Arduino Nano | dark navy board with white component detail, silver Mini-USB socket |
| Big push-button modules | navy PCB `#000f41`, darker than the other boards; round caps in black, yellow, white and blue `#0074d9`; black 3-pin connectors |
| TM1637 4-digit display | blue PCB `#224bbe`, black display window, white 7-segment digits and colon, light grey pins |
| 32x8 LED matrix | black faces with white round LEDs, white module sides carrying "1088AS" text, blue PCB behind, 5 right-angle header pins |
| Jumper wires | flat-coloured tubes with black outline: gold `#ac9400`, black `#000000`, purple `#ab53ca`, red `#bb3d3d`, dark brown `#411900`, green `#339f3f`, navy `#2a2f62`, maroon `#662639`, teal `#377e89` |
| Dupont housings | pure black rectangular blocks on both ends of every wire |
| Ribbon (Step 1) | the 9 coloured wires side by side between two black housing blocks |
| USB cable | very dark brown-black `#1e1616` cable with moulded strain reliefs, silver `#a6a9aa` plug shells, white inserts |
| Labels | bold black text over a cyan underline, cyan leader, dashed cyan ring |
| Eye icon | solid black eye with white ring and highlight |
| Lead line | thin solid red line |
| Photo insets | colour photos in a cyan rounded frame with a red highlight rectangle |

## 5. Anomalies and inconsistencies

Authoring:

1. **Label case is inconsistent.** Steps 2-3 use lower case (`clk`, `dio`, `s8`, `s9` at [004], [006]); Steps 4-10 use upper case (`VCC`, `V9`, `GND`, `G9`, `V11` ... `CLK`, `S13`). The same signal is `clk` on the display and `CLK` on the matrix.
2. **Three shield-side leader tips are attached to a neighbouring part**: `s8` [004] to the Nano socket strip, `G9` [010] to the VCC-row strip about one pin over, `V11` [013] to the signal-row strip. The tips still land within about one pin of the right place.
3. **Eye icon overlaps the shield** in Step 2 [004]; on the other 8 steps it sits in clear space.
4. **Loose-wire staging spot is not constant**: Step 2 uses the ribbon spot (wire at lower right), Steps 3-5 a spot 40 mm away (lower left), Steps 6-10 the ribbon spot again.
5. **Eye ring position on the wire varies**: midpoint on 6 steps, near the left end on 3.
6. **Red wire on GND** [010], purple on VCC [008], dark brown on VCC [013], green on GND [015]. This follows ribbon order but contradicts the usual red = power convention.
7. **Near-identical dark wires**: black (Step 3) and dark brown (Step 6) are hard to tell apart; maroon (Step 9) is close to both.
8. **Step 11 framing crops the model**: the button modules run off the top edge in [024] and [025].
9. **Renders saved at two aspect ratios**: [000], [001], [026] at 2:1; the other 24 at 2.79:1. Label positions are stored as viewport percentages while leader tips follow the 3D part, so label-to-model spacing depends on viewport shape.
10. Three labels have no explicit leader style in the data (`V11` and `VCC` at [013], `DIN` at [017]). They render the same as the others.
11. Guide title in the data is "Piano Memory Game(PMG) Part 2" (no space before the bracket); the title image has the space.
12. CAD naming, not student-facing: the wire for S11 -> DIN is named "S1 to DIN"; the shield and display carry Spanish and Russian SolidWorks feature names.
13. The `4-Digit Display` card camera differs from the same card in the full build (elevation 3, azimuth -91 here; 12 and -75 there).

Digest caveats found while checking (they affect how this guide's digest reads, and probably others):

14. **The digest under-reports visibility.** `Display TM1637-4`, `USB Cable end-1` and `USB Right Angle-1` have a parent-level hidden flag but visible leaves, and they do render. So the digest shows "0 parts" on [001], "1 part" on [023], never lists the display as appearing, and counts 71 parts where 74 are on screen.
15. **"Still displaced" is a false alarm for the USB cable and the shield.** For components whose CAD reference has its own transform, the step `position` is an absolute translation that replaces the transform's translation; the true offset is position minus that translation. Recomputed: the cable is seated at [000], [025], [026] and hovers by exactly +22.9 mm at [023]-[024]. The odd wire-cap offsets (around 595, 902, 1387) are the same -124.8, 0, +49.6 mm as their wire. The nine shield "displacements" are the fixed mounting translations of nine of its own sub-components (PCB, two socket strips, diode, resistors, reset button and so on); all 97 visible shield solids have a true offset of 0.
16. The annotation inventory in the digest header (45 labels, 48 lead lines, 2 arrows, 38 images) is the whole PMG project, not this guide. This guide shows 18 labels, 1 lead line, 0 arrows, 13 images.

## 6. Relation to the other PMG guides

- **Part 2 is the full build's steps [034]-[058] with new numbers.** Full-build Steps 15-25 become Steps 1-11 here, with the same three cards, the same labels, the same eye icons, the same camera for every numbered step, the same 22.9 mm USB hover and 28.5 mm lead line. Only the `4-Digit Display` card camera differs, and Part 2 adds its own `Start` and `Completed View`.
- All PMG guides are cut from one Cadasio project: the component names carry "PMG Full 3D Cadasio Build", and the unused Part 1 and Part 3 annotations are still in this guide's inventory.
- **Part 1** (34 steps) builds what Part 2 starts from: shield, Nano, four button modules, 12 wires. It uses the same label and eye conventions (labels on 12 of its 14 `Step N` steps, eye on 13, a lead line on 1) and has two cards (`Nano I/O Module`, `Push Buttons`). It ends `Step 14` -> `Completed View` with no `Step 14c`, and it has 3 auto-advancing Transition steps; Part 2 has none.
- **Part 3** (59 steps) begins with the wooden housing parts. It has no cards and no labels, uses lead lines on 19 of its 26 `Step N` steps, the eye on 6, and has 5 Transition steps. Part 2 is the opposite profile: labels on 9 of 11 `Step N` steps and a lead line on 1, because it is nearly all wiring.
- The deconstruction guide (61 steps, 14 Transition steps) was not examined beyond its step list.
