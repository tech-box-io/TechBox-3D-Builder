# Dimension report: labels, eye icon, image callouts and section cards

Scope: every 2D annotation in the 20 published TechBox guides (text labels, the eye icon, image callouts, title-page images, section cards), plus the text channels that sit outside the canvas (step descriptions, popups, hover tooltips).

## 0. Method and data caveats

- Numbers come from a fresh replay of all 20 raw payloads (`reports/_work_dim_labels/extract.py` -> `ann.json`), not from the digests. The replay keeps every annotation property (box size, leader, anchor, container, link target, stored 2D position and stored 2D leader tip) for each of the 1037 viewer steps.
- Step classes used below: `N` = "Step n" (425), `Nc` = "Step nc" (424), `T` = Transition (117), `card` = named section card (31, plus the 2 overview views of LAC Electronics), `start` (19), `end` = Completed View / Completed Build (19).
- Render truth was measured from the saved step pictures (`thumbs_raw`): cyan underlines were located by pixel colour (`measure.py`, `match_underlines.py`, 200 of 214 labels matched), the eye icon by template matching (`eye_detect.py`, 226 of 226 searched), and white-space tests by counting coloured pixels under each callout (`whitespace.py`). About 45 frames were also looked at by eye across all three kits.
- Clone caveat. Part guides are slices of the full builds, so "showings" double-count the same authored callout. Where it matters both numbers are given: 214 standard-label showings = 122 distinct placements; 226 eye showings = 140 distinct; 45 inset showings = 22 distinct pictures.
- Digest caveat found on the way: the digest replaces an annotation's whole `leader` dict when a step changes one field of it, which is why several readers reported "leader colour missing" on some labels and eyes. With a field-wise merge all 214 labels and all 226 eye icons have leader colour `#7fdbff`. It is a digest artefact, not an authoring inconsistency.
- Stored 2D positions are percentages of the authoring viewport, which was about 2:1 in every kit (saved pictures are 1.95:1 to 2.07:1 for 17 guides). In those frames the stored label position equals the rendered top-left corner of the label box (fit: slope 0.999-1.013, residual 0.04-0.75 % of width) and 218 of 226 eye icons render where the data says (median error 0.05 % x, 0.26 % y). The 8 that do not are listed under anomalies.

## 1. Inventory

| guide | viewer steps | Step N | std labels (showings) | N steps with label | eye icons | N steps with eye | framed insets | other 2D | descriptions |
|---|---|---|---|---|---|---|---|---|---|
| LSM Part 1 | 19 | 8 | 8 | 4 | 3 | 3 | 2 | 2 title images | 6 |
| LSM Part 2 | 31 | 13 | 8 | 7 | 5 | 3 | 0 | 6 disc badges; 1 full-frame diagram; 2 title images | 18 |
| LSM Part 1+2 | 47 | 21 | 16 | 11 | 8 | 6 | 1 | 6 disc badges; 1 full-frame diagram; 2 title images | 28 |
| LSM Part 3 | 13 | 5 | 0 | 0 | 2 | 1 | 0 | 2 title images | 0 |
| LSM Part 4 | 29 | 12 | 0 | 0 | 3 | 3 | 2 | 1 quantity label; 2 title images | 1 (placeholder) |
| LSM Part 3+4 | 43 | 18 | 0 | 0 | 5 | 4 | 3 | 1 quantity label; 2 title images | 1 (placeholder) |
| LSM Full Build | 88 | 38 | 14 | 10 | 11 | 9 | 5 | 1 quantity label; 6 disc badges; 1 full-frame diagram; 2 title images | 0 |
| LSM Deconstruction | 69 | 24 | 0 | 0 | 17 | 16 | 8 | 2 title images | 0 |
| LAC Part 1 | 32 | 14 | 20 | 10 | 10 | 9 | 1 | 2 quantity-label showings; 2 title images | 0 |
| LAC Part 2 | 42 | 18 | 10 | 8 | 10 | 10 | 1 | 2 title images | 0 |
| LAC Part 3 | 21 | 8 | 10 | 6 | 10 | 8 | 1 | 2 title images | 0 |
| LAC Part 4 | 42 | 17 | 0 | 0 | 11 | 7 | 2 | 2 title images | 0 |
| LAC Full Build | 131 | 57 | 40 | 24 | 41 | 34 | 5 | 2 quantity-label showings; 2 title images | 0 |
| LAC Deconstruction | 130 | 47 | 4 | 4 | 28 | 28 | 2 | 2 title images | 0 |
| LAC Electronics | 2 | 0 | 0 | 0 | 0 | 0 | 0 | none | 1 (placeholder) |
| PMG Part 1 | 34 | 14 | 24 | 12 | 13 | 13 | 1 | 1 framed photo label; 2 title images | 0 |
| PMG Part 2 | 27 | 11 | 18 | 9 | 9 | 9 | 2 | 2 title images | 0 |
| PMG Part 3 | 59 | 26 | 0 | 0 | 7 | 6 | 3 | 2 title images | 0 |
| PMG Full Build | 117 | 51 | 42 | 21 | 29 | 28 | 6 | 1 framed photo label; 2 title images | 0 |
| PMG Deconstruction | 61 | 23 | 0 | 0 | 4 | 4 | 0 | 2 title images | 0 |
| **all 20** | **1037** | **425** | **214** | **126** | **226** | **201** | **45** | | **55** |

2D annotation showings by step class:

| | Step N | Step Nc | Transition | card | Start | end view |
|---|---|---|---|---|---|---|
| standard label | 214 | 0 | 0 | 0 | 0 | 0 |
| quantity / photo label | 2 | 2 | 0 | 5 | 0 | 0 |
| eye icon | 210 | 7 | 0 | 9 | 0 | 0 |
| image (inset, disc, diagram, title) | 39 | 14 | 0 | 13 | 38 | 0 |
| steps with any 2D annotation | 251 of 425 | 23 of 424 | 0 of 117 | 25 of 33 | 19 of 19 | 0 of 19 |

Annotation recipes on Step N, the three full builds (146 steps; each kit counted once):

| recipe on the Step N view | LAC FB | LSM FB | PMG FB | all | share |
|---|---|---|---|---|---|
| lead lines only | 13 | 16 | 20 | 49 | 34 % |
| 2 labels + eye | 12 | 0 | 21 | 33 | 23 % |
| eye only (1 or 2) | 10 | 6 | 6 | 22 | 15 % |
| 1 label + eye | 8 | 0 | 0 | 8 | 5 % |
| arrow only | 4 | 2 | 1 | 7 | 5 % |
| 2 labels + lead lines (+ eye once) | 4 | 3 | 0 | 7 | 5 % |
| eye + lead lines | 2 | 1 | 1 | 4 | 3 % |
| label(s) only | 0 | 4 | 0 | 4 | 3 % |
| 1 label + 2 disc badges | 0 | 3 | 0 | 3 | 2 % |
| inset + arrow or lead lines | 2 | 2 | 0 | 4 | 3 % |
| eye + arrow | 1 | 1 | 0 | 2 | 1 % |
| other (quantity label + eye; inset alone; nothing) | 1 | 0 | 2 | 3 | 2 % |

Presence on those 146 steps: eye 71, lead lines 62, labels 55, arrow 11, inset 5. Co-occurrence: label+eye 42, label+lead 7, eye+lead 5, eye+arrow 2, lead+arrow 0, label+arrow 0.

The three deconstructions (94 Step N): arrow only 41, eye only 26, eye + arrow 10, eye + inset + arrow 7, 1 label + eye 4, lead line 3, inset + arrow 2, eye + inset 1. Labels on 4 of 94, lead lines on 3 of 94.

## 2. Text labels

### 2.1 Style (always true unless stated)

214 of 223 label showings use one house style (PMG's preset is literally named "tech box label"):

| property | value | count |
|---|---|---|
| container | "underline": a horizontal rule under the text, no box, white fill | 214 / 214 |
| underline colour | `#7fdbff` | 214 / 214 |
| underline thickness | 5 px (6 px on LSM "c16", 2 showings) | 212 / 214 |
| text | bold, black `rgb(0,0,0)`, centred on the underline | 214 / 214 (2 LSM "Pin d12" showings lack the centre attribute) |
| font size | 3 em of a 20 px base | 175 / 214 (LAC 84, PMG 84, LSM Full Build 7) |
| | 2.5 em | 39 / 214 (all LSM: Parts 1, 2, 1+2 and 7 in the Full Build) |
| font family | Arial set explicitly | 126 / 214 (LAC build guides, LSM) |
| | not set, so the project default (Public Sans Medium) | 88 / 214 (all PMG, LAC Deconstruction) |
| box | 175 x 90 px at 3 em, 175 x 75 px at 2.5 em | 143 and 25; longer texts widen the box to 195-258 px (rail labels, "Pin d12") |
| leader | one straight segment, solid, `#7fdbff`, same thickness as the underline, no elbow control point | 214 / 214 |
| leader start | the end of the underline nearest the target (`leader_start_position` x = 0 or 1, y = 1) | 214 / 214 stored; 170 / 170 confirmed against renders |
| leader tip | "Life Saver Circle": a dashed ring (four arc segments), `#7fdbff`, 30 px x 1.2 = 36 px | size 1.2 on 203, 1.0 on 11 |
| link | exactly one 3D target per label | 214 / 214 |

Proportions that hold regardless of capture size (measured in renders): text cap height / underline length = 0.24-0.25 at 3 em and 0.20 at 2.5 em; gap between text bottom and underline = 0.55 x cap height; text centre = underline centre (offset 0.0-0.2 % of width); ring outer diameter about 0.19 x underline length; underline and leader the same thickness.

On-screen size in the saved ~2:1 pictures:

| capture | em | underline length | cap height | underline thickness |
|---|---|---|---|---|
| LAC all guides, LSM Full Build (2559 x 1239) | 3 | 8.1-8.3 % W = 16.7-17.1 % H | 4.0-4.1 % H | 0.40 % H (5 px) |
| LSM Full Build (2559 x 1239) | 2.5 | 8.1 % W | 3.4 % H | 0.40 % H |
| PMG Full Build (3840 x 1967) | 3 | 7.2 % W = 14.0 % H | 3.5 % H | 0.36 % H (7 px) |
| LSM Parts 1, 2, 1+2 (2560 x 1279) | 2.5 | 6.3 % W = 12.6 % H | 2.5 % H | 0.31 % H (4 px) |
| PMG Parts 1, 2 (2560 x 919, 2.79:1) | 3 | 7.1-7.2 % W = 20 % H | 5.0 % H | 0.54 % H |

The PMG rows show that a label keeps a constant fraction of the viewport width (7.2 % W at both 1.95:1 and 2.79:1), so on a wide, short viewport callouts grow relative to the model.

### 2.2 What the text says

| text class | LSM | LAC | PMG | total | examples |
|---|---|---|---|---|---|
| breadboard hole, lower-case row letter + column number | 44 | 48 | 0 | 92 | c15, h27, i23, a8, j4, i2, b19 |
| power rail, polarity + stripe colour | 0 | 24 | 0 | 24 | "(+) red" x10, "(-) blue" x14 |
| module pin, silk-screen name in capitals | 0 | 12 | 38 | 50 | GND, VCC, SDA, SCL, OUT, DIN, CS, CLK |
| shield pin, row letter (V / S / G) + pin number, capitals | 0 | 0 | 38 | 38 | V4, S4, G4 ... S13 |
| module / shield pin in lower case | 0 | 0 | 8 | 8 | clk, dio, s8, s9 |
| word + pin | 2 | 0 | 0 | 2 | "Pin d12" |

- Length: 188 of 214 labels are 2 or 3 characters; the longest are 7-8 characters ("(+) red", "(-) blue", "Pin d12"). No label contains a verb, a part name, a wire colour or a step number.
- The colour word in a rail label names the rail's printed stripe, not the wire (the tan lead goes to "(+) red" in LAC Step 17; a purple wire goes to "(-) blue" in LAC Step 36).
- Distinct texts: LSM 13, LAC 30, PMG 28.

### 2.3 What the leader points at

| kit | text class | target of the ring | showings |
|---|---|---|---|
| LAC | hole and rail labels | the exact hole on the breadboard top face | 72 |
| LAC | GND / VCC / SDA / SCL (build) | the individual pin of the LCD's 4-pin header | 8 |
| LAC | GND / VCC / SDA / SCL (deconstruction) | the plugged-in connector housing of that wire (3) or the pin (1) | 4 |
| LSM | hole labels on rigid-part steps and on Full Build far-end steps | the hole on the breadboard | 23 |
| LSM | hole labels on wire-end steps | the wire's own connector housing | 21 |
| LSM | "Pin d12" | the pin row of the hovering Nano | 2 |
| PMG | module pin names | the pin / socket of that module (button, display, matrix) | 42 |
| PMG | shield pin names | the header strip of the shield at that pin | 42 |

No label is ever linked to a wooden panel, a wire body or a whole part: 0 of 214.

### 2.4 How many, and are both ends labelled

- Label-carrying Step N views: 126. One label on 38 (LAC 20, LSM 18), two labels on 88 (LAC 32, LSM 14, PMG 42). Never three or more.
- Labels live on Step N only: 214 of 214; 0 on Nc, Transition, card, Start or end view.
- Wire steps in the three full builds (48 steps) follow "one destination callout per wire end the student places in this step":

| situation | steps | callouts |
|---|---|---|
| LAC loose jumper, both ends placed in one step | 12 | 2 labels (one per end) + eye on the loose wire: 12 / 12 |
| LAC pre-attached lead, one free end | 8 | 1 label (the hole or rail) + eye on the lead tip: 8 / 8 |
| PMG loose jumper, both ends placed in one step | 21 | 2 labels (module pin + shield pin) + eye on the loose wire: 21 / 21 |
| LSM ribbon wire, male end only | 3 | 1 label (the hole), no eye: 3 / 3 |
| LSM ribbon wire, female end only | 3 | 2 disc badges (pin + free wire end) + 1 label naming the hole the wire already sits in: 3 / 3 |
| LSM push-button pigtail, two leads in one step | 1 | 2 labels (one per lead) |

- Rigid plug-in parts on a breadboard get two labels naming the two extreme holes, alongside the red lead lines: LAC Nano, both resistors, RTC (4 / 4, "2 labels + lead lines"); LSM Full Build both resistors and the capacitor (3 / 3). Exceptions: the Nano has no label in the LSM Full Build (Part 1's version has "Pin d12" + "c16"), and PMG's Nano-onto-shield step has lead lines only.

### 2.5 Where labels sit on screen

Sample: 170 label showings in ~2:1 pictures whose underline was found in the render (PMG Parts 1 and 2 excluded because their pictures are 2.79:1; the same labels are in the Full Build).

| measure | result |
|---|---|
| leader leaves the underline end nearest the target | 170 / 170 |
| target lies horizontally outside the underline span (never under the text) | 170 / 170 |
| label is further from the vertical centre line than its target (pushed outward) | 164 / 170 |
| label above its target | 150 / 170 (88 %) |
| label left of target / right of target | 92 / 78 |
| vertical drop, underline to target | median 8.8 % H (quartiles 4.7 and 11.5; range -23.7 to +21.4) |
| horizontal gap, underline end to target | median 14.5 % H (quartiles 10.8 and 19.2; min 1.1) |
| leader length | median 19 % H (quartiles 14 and 23; range 3-44) |
| leader angle from horizontal | median 35 deg (quartiles 23 and 43; range 3-67) |
| label centre x | 21-74 % of width; none in the outer fifth on either side |
| underline y | 13-66 % of height; 0 / 170 in the bottom third |
| zone (left / centre / right x top / middle third) | L-top 36, L-mid 41, C-top 12, C-mid 15, R-top 24, R-mid 42 |
| targets | x 34-63 %, y 18-64 % (the model occupies the middle of the frame) |
| text box over white background | 196 / 200 labels have under 2 % coloured pixels under the text; maximum 4.7 % |

The 20 labels that sit below their target: LAC "h27" and "h29" (Steps 5, 6, in Part 1 and Full Build), LAC "j4" (Step 33), the four LCD pin labels GND / VCC / SDA / SCL (Steps 36-39; the header is in the upper-left and the white space is below it), PMG "V11 / G11 / S11 / S12 / S13" (Steps 20-24) and PMG "VCC" on Step 9.

Two-label steps (66 in the sample):

| arrangement | steps | ordering rule | holds |
|---|---|---|---|
| flanking: one label left of the model, one right | 37 | the left label owns the left-most target | 37 / 37 |
| stacked on one side (18 right, 11 left) | 29 | the upper label owns the upper target | 29 / 29 |
| leaders cross | 0 / 66 | | |

Stacked underlines are 9-38 % H apart (median 15 %). Within a wiring run the label slots repeat from step to step (for example PMG button block: module label x 51-67 %, y 25-34 %; shield label x 56-65 %, y 41-52 %; LAC LCD block: pin label x 19-21 %, y 48-51 %).

### 2.6 The other label kinds

| kind | style | where | showings |
|---|---|---|---|
| quantity label | Arial bold 6 em, no container, no leader; `#0074d9` ("2x") or `#7fdbff` ("64X" / "64x"); placed to the upper right of the isolated part at about (53-54 %, 12-22 %) | LAC Step 4 and 4c ("2x", persists into the c view); LSM "LED Stems" card | 4 + 3 |
| framed photo label | text annotation holding a photo plus a grey caption "NANO I/O MODULE LABELS" (Public Sans 20 px), rounded rectangle border `#7fdbff` 5 px, drop shadow, leader + ring | PMG "Nano I/O Module" card | 2 |

## 3. The eye icon

One PNG, the same asset in all 20 projects: a black almond-shaped eye with a white iris ring and a white highlight. 226 showings (140 distinct placements): LAC 110, PMG 62, LSM 54.

### 3.1 Style

| property | value | count |
|---|---|---|
| width | 7.81 % of viewport width (LAC, LSM) or 8.2 % (PMG) | 144 and 62; 20 outliers at 6.29-9.37 % (LSM Part 1 close-ups, a few LAC) |
| shape | square image; the glyph fills the full width and the middle 55 % of the height (about 2 : 1.1) | |
| container | none | 225 / 226 (one boxed eye, LSM Deconstruction Step 4) |
| leader | straight, solid, `#7fdbff`, 5 px | 224 / 226 (4 px on 2) |
| leader start | a point on the glyph on the side facing the target; in PMG always the left or right corner of the eye | direction check 217 / 217; PMG corner 58 / 58 |
| leader tip | same dashed ring as labels, `#7fdbff` | 223 / 226 (teal `#39cccc` on 3) |
| text | none, ever | 226 / 226 |
| per step | 1 on 208 steps, 2 on 9 steps, never 3 | |
| show / hide | fade | 226 / 226 |

The eye glyph is about as wide as a label underline (7.8-8.2 % W against 7.2-8.3 % W).

### 3.2 When it appears

| step class | showings | note |
|---|---|---|
| Step N, build guides | 161 | |
| Step N, deconstruction guides | 49 | |
| section card | 9 | Real Time Clock, Alarm Buzzer, LCD Screen, Mini USB Cable |
| Step Nc | 7 | "check the result": wires in a notch (LSM 23c), wire routing after a re-pose (LAC 48c, 56c) |
| Start, Transition, end view | 0 | |

Context of the 217 eye-carrying steps:

| what else is on the step | steps | meaning |
|---|---|---|
| nothing else | 90 | "this is the piece / look here" on a prep step, a card, a pick-up step or a check |
| 2 labels | 66 | loose jumper: eye on the wire, labels on the two destinations |
| 1 label | 22 | pre-attached lead (eye on the lead tip) or LAC deconstruction pin label |
| arrow (with or without inset) | 23 | hand move or removal: eye marks the part or the catch |
| lead lines (with or without labels) | 13 | orientation check next to an insertion (LSM capacitor stripe, LAC breadboard corner, LAC F9 slot, PMG H14 edge) |
| inset only | 3 | |

In the full builds the eye is the stand-in for motion guidance: of the 84 Step N views without lead lines 66 carry an eye (79 %); of the 62 views with lead lines only 5 do (8 %). The 18 without either are arrow-only (7), LSM label-only or label + disc wire steps (7), inset steps (3) and one empty prep step.

What it points at (from link targets, renders and reader reports): the body or free connector of the loose wire to pick up (wire steps); an identifying feature of a part shown alone (resistor colour band, capacitor stripe, RTC coin cell, LCD glass, ribbon connector); a pre-wired module about to be picked up (button, display, shield, buzzer, panel with switch); a mating feature or destination where nothing hovers (slot, notch, USB socket); in deconstruction the plug, clip or part to release.

### 3.3 Where it sits

Sample: the 218 icons whose stored position matches the render.

| measure | result |
|---|---|
| distance, eye centre to leader tip | median 23 % H (quartiles 19 and 28; range 11-57) |
| by context | with labels 20 % H (11-33); with arrow 23 %; with lead lines 27 %; alone 26 % |
| direction of the eye seen from its target | upper-left 66, upper-right 35, above 20, left 24, right 26, lower-left 28, lower-right 17, below 2 |
| summarised | above 121 (56 %), level 50 (23 %), below 47 (22 %); left 125 (57 %), right 93 |
| per kit | PMG 32 of 58 upper-left (38 of 58 above); LAC spread over all sectors; LSM 23 of 50 above |
| eye centre | x 17-81 %, y 6-76 %; zones: L-mid 47, C-top 46, C-mid 43, R-mid 30, C-bottom 26, L-top 17, L-bottom 6, R-top 3 |
| on white background | 210 / 218 have under 2 % coloured pixels under the glyph; 2 overlap the model by more than 10 % (PMG display Step 2 / 16) |

There is no fixed screen slot and no fixed side. The constant is: free white space, 15-35 % of the viewport height from the target, usually on the side away from the rest of the model. Within a wiring run the eye stays in one slot because the loose wire is staged in one place (LAC jumpers x 22-24 %, y 33-35 %; PMG button wires x 28-34 %, y 45-50 %).

## 4. Image callouts

112 non-eye image showings: 45 framed insets, 38 title-page images, 18 disc badges, 3 full-frame diagrams. Plus the 2 framed photo labels of 2.6.

### 4.1 Framed insets

| property | value | count |
|---|---|---|
| frame | rounded rectangle, border `#7fdbff`, thickness 5, corner radius 0.1, white fill | 43 / 45 (PMG Step 8c / 33c: `#7fb9ff`, thickness 2) |
| leader | straight, `#7fdbff`, 5 px, from the frame edge to the feature | colour 43 / 45 (`#7fb9ff` on PMG Step 8c / 33c); thickness 44 / 45 (2 px on LSM Part 1 Capacitor) |
| leader tip | dashed ring `#7fdbff` | 41 / 45 (orange `#ff5F0B` on PMG Push Buttons, 2 showings; `#7fb9ff` on PMG Step 8c / 33c, 2 showings) |
| link | one 3D target | 45 / 45 |
| width on Step N | median 15.8 % W (7.8-24.8) | 21 |
| width on Step Nc | median 16.8 % W (13.2-20.3) | 14 |
| width on cards | median 31.2 % W (17.2-36.7) | 10 |
| height | 13-70 % H, median 31 % H | |
| placement (by box centre) | right-middle 21, left-top 11, left-middle 6, right-top 6, centre 1; never in the bottom third | |
| relative to its target | above it on 34, below on 11; 16-68 % H away (median 43) | |
| alone on the step | 24 / 45; with arrow 14; with lead lines 4; with eye 10 | |

What the 22 distinct pictures are:

| type | pictures | where | on |
|---|---|---|---|
| real product photo with a red rectangle round the pin names | LCD I2C backpack (LAC); push-button module, 4-digit display back, dot-matrix back (PMG); plus the Nano I/O shield photo as a framed label | section cards | card |
| labelled diagram | capacitor polarity (GND strip, GND -, VCC +) | LSM "Capacitor" card | card |
| pre-rendered close-up in the guide's own toon style with 1-4 thin red rectangles on the exact feature | LAC pot locating tab (25c), LAC F9 foot slot (45c), LAC LCD on F9 hooks (Step 52), LSM top view with 4 corner slots (Step 31), PMG button on its ledge (33c), PMG key tab (38c), 7 LSM Deconstruction latch close-ups | steps | Nc 8 showings, N 14 |
| pre-rendered close-up with an eye glyph drawn inside the picture | LSM wire path inside the box (30c), LSM post tips through the base (34c) | steps | Nc |
| hidden-face view with its own caption and mini leader | "Protective Backing" under the breadboard (shared by LSM and LAC Step 1) | step | N |
| quantity cue | part outline "H9" with "3x" (PMG Step 39) | step | N |

17 of the 22 pictures contain red highlight rectangles (red pixels found inside the frame in the renders; the exceptions are the backing picture, the capacitor diagram, the two eye-in-picture close-ups and the "3x" cue).

When an inset is used:
- Build, Step Nc (14 showings, 6 pictures): to prove a locking or routing detail that the main view cannot show. This is the main reason an Nc view carries any 2D annotation (14 of 23).
- Build, Step N (11 showings): a hidden face, an orientation aid or a repeat cue.
- Deconstruction, Step N (10 showings): the latch or tab to release. LSM Deconstruction 8 of 24 steps, LAC 2 of 47, PMG 0 of 23.
- Cards (10 + 2 showings): the real board with its printed pin names.

### 4.2 Disc badges (LSM only)

18 showings on 9 steps (the three female-end wire steps in Part 2, Part 1+2 and the Full Build). Two round raster images carrying the same text: a `#7fdbff`-filled disc on the matrix pin and a white disc with a thin grey outline on the free wire end. Text "V+", "V-In", "V-" in bold black. Width 5.8-7.8 % W (11.6-15.6 % H), no container, straight `#7fdbff` 5 px leader with ring, 12-27 % H from the target (median 18). LAC and PMG, authored later, name module pins with ordinary underline labels instead (50 showings), so the disc pair is an LSM-only device.

### 4.3 Full-frame diagram (LSM only)

"LED Matrix Diagram" card, 3 showings: one flat picture 62.8-65.2 % W, no frame, no leader, no link, all 3D parts hidden. The picture (back of the matrix, two red-boxed pad groups) has two eye icons with leaders visible in the saved render that the step data never switches on.

### 4.4 Title-page images

Every Start step (19 of 19; LAC Electronics has no Start) shows exactly two unlinked, unframed images and nothing else, with the finished model in the right half:

| image | x | y | width | bottom / right edge |
|---|---|---|---|---|
| TechBox logo (one SVG for all guides: cyan rounded badge, white bulb and "TECHBOX") | 1.8-2.5 % (PMG Deconstruction 5.1) | 4.0-8.1 % | 33.2-39.5 % W | bottom at 22-29 % H, right at 36-42 % W |
| title block (PNG per guide: kit name, part or "Full Build" / "Deconstruction", copyright line) | 1.6-2.5 % (PMG Deconstruction 3.8) | 61.0-64.6 % (LSM Part 1: 24.1 % with a taller padded image) | 42.1-48.4 % W (LSM Part 1: 58.3) | bottom at 80-89 % H, right at 44-51 % W |

Both are removed on entering the next step.

## 5. Section cards

31 card showings in 12 build guides, 14 distinct titles. None in the deconstructions, none in the wood-only parts (LSM Part 3, LAC Part 4, PMG Part 3). A card is an unnumbered, named step with behaviour pause and 800 ms duration, placed directly before the first step that uses the component; the camera moves on 29 of 31 (the two exceptions show no 3D at all).

| card | guides | 3D shown | annotations |
|---|---|---|---|
| Capacitor (LSM) | Part 1, Full Build | capacitor alone, side-on | framed polarity diagram (30-32 % W) with leader to the stripe |
| LED Matrix Diagram (LSM) | Part 2, Part 1+2, Full Build | nothing | full-frame flat picture (63-65 % W) |
| Mini USB Cable (LSM) | Part 2, Part 1+2, Full Build | cable alone | eye |
| LED Stems (LSM) | Part 4, Part 3+4, Full Build | one stem alone | quantity label "64X" / "64x" |
| Real Time Clock (LAC) | Part 1, Full Build | module with coin cell, in hover pose | eye on the coin cell |
| Rocker Switch (LAC) | Part 2, Full Build | switch with its 3 leads | none |
| Alarm Buzzer (LAC) | Part 3, Full Build | buzzer with its 2 leads | eye |
| LCD Screen (LAC) | Part 3, Full Build | LCD alone | eye on the glass + framed photo of the I2C backpack (29 % W), red box round GND / VCC / SDA / SCL |
| USB Cable (LAC) | Part 3, Full Build | cable alone | none |
| Nano I/O Module (PMG) | Part 1, Full Build | shield alone, plan view | framed photo with caption, leader to the board |
| Push Buttons (PMG) | Part 1, Full Build | one button module, face-on | framed photo (17 % W), red box round VCC / OUT / GND |
| 4-Digit Display (PMG) | Part 2, Full Build | display alone | framed photo (34 % W), red box round the header |
| Dot Matrix Display (PMG) | Part 2, Full Build | matrix alone | framed photo (37 % W), red box round the input header |
| USB Cable (PMG) | Part 2, Full Build | cable alone | none |

By showings: framed picture 12, eye only 7, quantity label 3, full-frame diagram 3, nothing 6. By title: picture 6, eye only 3, quantity 1, diagram 1, nothing 3.

- The card's name is never drawn on the canvas (0 of 31); it exists only as the step name. The only words on any card are inside pictures (silk-screen text, "NANO I/O MODULE LABELS", "GND Strip") and the quantity label.
- The photo previews the vocabulary of the labels that follow: the four LCD pin names on the card are the four labels of the next four steps; VCC / OUT / GND on the button photo are the module-side labels of the next twelve PMG steps.
- All three PMG module cards and the LAC LCD card pose the 3D part to match the photo.
- LAC Electronics is not a card guide: two unannotated line-up views ("All Electronics", "All Wood") with no 2D annotation at all.

## 6. Text outside the canvas

| channel | finding |
|---|---|
| popups | 0 of 1037 steps (`popupType` is "none" everywhere) |
| step descriptions | 55 of 1037 steps. 52 are authored and all are in the three oldest LSM guides (Part 1: 6, Part 2: 18, Part 1+2: 28); 3 are Cadasio's placeholder "A Start point for your project..." (LSM Part 4, Part 3+4, LAC Electronics). The other 14 guides have none, including every full build and every LAC and PMG guide |
| description format, where present | "Step n - imperative sentence" on the hover view; a bare "Step nc" on the completed view. Numbering lags the step names, with typos (see anomalies) |
| hover tooltips | enabled in all 20 projects (`tooltips: true`); every part carries `tooltip_show: true`, `tooltip_title: "Description"`, `tooltip_text: "none"`, and the Description value is set per solid by the steps. Result: every solid of a kit item returns one student-facing name. 8-27 distinct names per guide (8 in LSM Part 1, 13-27 elsewhere) |
| tooltip vocabulary | electronics by plain name ("Nano Board", "LCD Screen", "Real Time Clock", "3-Position Rocker Switch", "Breadboard Wires (M-F)", "MAX7219 Display", "Small Blue Push Button"); wood as "Role - Part ID" ("Housing Rear Side - Part D4", "Top Side - Part F4", "Arch Bracket - Part H13") |
| engraved IDs | wooden parts carry their ID (D1-D11, F1-F9, H1-H14) as black geometry modelled on the part; this is the only on-canvas part naming |

The PMG readers reported tooltips as placeholders; the replay shows PMG has the same mechanism with 24-26 names. Tooltip appearance could not be observed (no live viewer), only the data.

## 7. What is never annotated

- Completed views: 0 of 19 carry any annotation. Transitions: 0 of 117 carry a 2D annotation.
- Step Nc: 0 of 424 carry a standard label; 401 of 424 carry no 2D annotation at all.
- Wooden panels: never labelled (0 of 214 labels link to wood); they are identified by the engraved ID.
- Wire colour: never written. The eye says which wire; colour words appear only in rail labels and name the rail.
- Part names: never written on the canvas. Value of a resistor: never written.
- The path of a wire: never drawn (0 lead lines on the 48 wire steps of the full builds).
- Step number, step title, card title, instruction sentence, warning, tick or cross, tool, hand, dimension, legend: none in any of the 1037 steps.
- Lead lines and arrows never carry text.
- Deconstruction: no hole or pin destinations (0 labels in LSM and PMG deconstruction; 4 in LAC to tell four adjacent identical-looking plugs apart).

## 8. Lifetime and layering

- 2D annotation objects are single-use: 535 of 544 label, eye and image objects are visible on exactly one viewer step. The 9 exceptions: "2x" on Step 4 and 4c (2 objects), the LSM "i3" label reused on Steps 3 and 7 (2), four LSM disc images reused with a swapped picture, one LAC Deconstruction eye on a duplicated step.
- Every Step N has at least one annotation of some kind: 423 of 425 (the two empty ones are the same PMG ribbon-prep step, Part 2 Step 1 = Full Build Step 15).
- Eye and image callouts fade in and out; labels use the step default (fade, 800 ms).

## 9. Screen-space behaviour seen in the saved pictures

The same PMG wiring steps exist as 1.95:1 pictures (Full Build) and 2.79:1 pictures (Parts 1 and 2). Comparing them:

| quantity | 1.95:1 | 2.79:1 | conclusion |
|---|---|---|---|
| label underline x against stored x | 1.013 x + (-0.9) | 0.712-0.737 x + 11.6-13.3 | x is compressed about the screen centre by authoring aspect / viewport aspect (1.99 / 2.79 = 0.71) |
| underline y against stored y | 1.001 y + 6.9 | 1.001-1.002 y + 8.3 | y is a plain percentage of height |
| eye centre x for stored 31.8 % | 31.4 % | 36.9 % | same compression (prediction 37.0 %) |
| underline length | 7.19 % W | 7.19 % W | size is a fraction of viewport width |
| eye width | 8.2 % W | 8.2 % W | same |

So a callout keeps its horizontal offset from the screen centre in units of viewport height (it stays registered with the 3D model, whose size is set by the vertical field of view), while its size follows the viewport width. Only this one pair of viewport shapes is available, so treat it as observed behaviour rather than a specification.

## 10. Anomalies (not conventions)

Text:
- PMG Step 10: shield-side label reads "S5", should be "S6" ("S5" twice, "S6" never). Present in Part 1 and the Full Build.
- PMG Steps 16-17 (Part 2 Steps 2-3): "clk", "s8", "dio", "s9" in lower case; every other PMG pin label is upper case, including "CLK" on the matrix.
- LSM badge "V-In" for the matrix input pad; the description says "IN pin", the diagram shows "Out".
- LSM Full Build Step 19: "j5" and "j16" point at the opposite leads to Part 2 Step 11.
- LSM labels are lower case ("c16") while the LSM descriptions use upper case ("Slot C16").
- Quantity cue written three ways: "2x" (LAC, blue `#0074d9`, with a trailing zero-width space), "64X" (LSM Part 4 and 3+4), "64x" (LSM Full Build), and "3x" baked into a picture (PMG).
- Descriptions: "srew", "Push Buttoim", "Ste[ 15", "Step 12c 0 Connect...", "Step 10C"; numbering offset from step names from LSM Step 5 on; three leftover Cadasio placeholder descriptions.
- Tooltip names: "Laster Stem Matrix (LSM) - Part 1" on 58-80 solids; "Mini-USB Cable" and "Mini USB Cable"; "12k Ohm Resistor" and "12 kOhm Resistor"; "Push Button" and "Black Push Button"; leftover letter-scheme names in LSM Parts 1, 2, 1+2 ("Housing Base - Part A1", "Nano Board - Part C", "LED Matrix - Part D", "Push Button - Part F", "Breadboard Wires - Part I"); PMG "Key Passthrough - Part H2" in Parts 1 and 2 against "Part H8" elsewhere; H4 named "Front Baseplate", "Rear Baseplate" and "Backplate"; "Push Button Plate -  Part H5" with a double space; "Adhesive Backing " with a trailing space.

Style drift:
- Label size: 2.5 em in LSM Parts 1, 2, 1+2 against 3 em in LAC and PMG; mixed inside the LSM Full Build (3 em on Steps 5, 6, 8, 10; 2.5 em on Steps 11-15, 19).
- Font family: Arial in LSM and LAC builds, unset (Public Sans) in PMG and LAC Deconstruction.
- Underline thickness 6 on LSM "c16"; ring size 1.0 on 11 labels and 8 eyes, 1.3 on 3 eyes.
- Eye width 6.29 / 8.7 / 9.37 % on the three LSM Part 1 eyes, 7.58 %, 7.92 % and 8.24 % on a few others; leader 4 px on 2.
- Ring colour teal `#39cccc` on 3 eyes (LSM Step 14 / Part 4 Step 8); orange `#ff5F0B` on the PMG Push Buttons inset; inset frame `#7fb9ff` thickness 2 on PMG Step 8c / 33c.
- One eye in a cyan box (LSM Deconstruction Step 4).
- The same eye PNG is named "Image", "new eye" and "Eye" in different projects.
- PMG Step 15 (9-wire ribbon prep) has no annotation while its twin Step 2 has an eye.
- Section cards uneven: Rocker Switch and both USB Cable cards have nothing; the potentiometer has no card.
- "2x" is the only label that survives into a c view.
- PMG Nano I/O card inset is a text label with an embedded image; every other inset is an image annotation.
- The eye overlaps the shield on PMG display Step 2 / 16.

Stale data (stored position disagrees with the saved picture):
- Eye icons, 8 of 226: LSM Part 1 Step 6 and LSM Full Build Step 6 (stored x = -5.8 %, rendered at 54-56 %, 6-12 %); LSM Full Build Step 34 (stored 92 %, 71 %; rendered 24 %, 33 %); LSM Part 1+2 Mini USB Cable card (stored 19 %, 16 %; rendered 38 %, 20 %); PMG Part 3 Steps 20 and 24 and their Full Build twins (off by 6-8 % of width).
- Insets: LSM Full Build 34c and LSM Part 3+4 14c stored at x = 87-93 % (partly off screen), rendered lower-left as in Part 4; PMG Full Build 38c and Step 39 stored over the model, rendered upper-left as in Part 3.
- LSM "LED Matrix Diagram": two eye icons visible in the saved picture that no step turns on.

## 11. Rules for the in-house player

1. One callout style for text: black bold sans text centred over a `#7fdbff` rule, a straight `#7fdbff` leader of the same thickness from the rule end nearest the target, a dashed `#7fdbff` ring on the exact feature. No box, no fill, no arrowhead.
2. Label text is a destination identifier of 2-3 characters as printed on the hardware: breadboard hole in lower case, rail as "(+) red" / "(-) blue", module and shield pins in capitals.
3. One label per wire end placed in the step, at most two labels per step, labels only on the instruction view, cleared on the result view.
4. Layout: text never over the model; target never under the label; label outboard of and normally above its target; nothing in the bottom third; two labels either flank the model in target order or stack on one side in target order; leaders never cross.
5. The eye icon is the only text-free pointer: black glyph about 8 % of viewport width, cyan leader and ring, one per step (two at most), on instruction views and cards, used where no part hovers along a lead line.
6. Framed insets for what the camera cannot show: rounded `#7fdbff` frame, leader and ring to the feature, thin red rectangles inside for the exact detail; photos on cards, close-ups on steps, and on result views only as a check.
7. Section card = component alone + at most one eye and one framed picture (or a quantity label); no title on canvas.
8. Title page = logo top-left, title block bottom-left, model on the right; no other annotation. End view = no annotation.
9. Part names live in hover tooltips and in engraved IDs, never in canvas labels. No popups; no reliance on step descriptions.
10. Positions are stored for a 2:1 frame and must be re-mapped about the screen centre when the viewport shape changes, so callouts stay registered with the model.

Working files: `reports/_work_dim_labels/` (`extract.py`, `ann.json`, `measure.py`, `match_underlines.py`, `underline_match.json`, `eye_detect.py`, `eye_detect.json`, `label_stats.py`, `label_rows.json`, `label_geo.json`, `eye_stats.py`, `eye_rows.json`, `image_rows.json`, `whitespace.py`, `tooltip_desc.json`).
