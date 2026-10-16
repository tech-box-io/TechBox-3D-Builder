# Guide report: Laser Stem Matrix (LSM) - Part 1

- guide id: `19075-laser_stem_matrix_lsm_-_part_1` (kit LSM, role: part)
- sources read: `digest/19075-laser_stem_matrix_lsm_-_part_1.md` + `.json` (all 19 steps), all 3 contact sheets, all 19 thumbs (plus full-resolution crops of [001] [003] [005] [006] [009] [012] [013] [016] [017] from `thumbs_raw`), targeted queries on `cadasio_raw/…part_1.json`, and the digests of the sibling guides `…lsm_part_1_2`, `…lsm_-_part_2`, `…lsm_-_full_build` for comparison.
- crops and query scripts used are in `reports/_work_19075_lsm_p1/`.

## 1. Summary

Part 1 is the shortest LSM guide: 19 viewer steps, all `pause` (no auto-advancing Transition steps), every step 800 ms. The student prepares a half-size breadboard (peels its adhesive backing), sticks it onto the laser-cut wooden base plate "D1", plugs in an Arduino Nano, then adds three through-hole passives: a 12 kOhm resistor, an electrolytic capacitor and a 330 Ohm resistor. There are no jumper wires, screws or side panels in this part. The structure is: `Start` title page, eight numbered step pairs (`Step N` = annotated "before/hover" view, `Step Nc` = clean "after/completed" view), one unnumbered section card (`Capacitor`) placed immediately before the capacitor step, and a final `Completed View`. Exactly one physical part is placed per numbered step; preparation actions (peel backing, bend resistor leads) get their own numbered step pair in an isolated close-up. Every placement is shown the same way: part hovers 31-39 mm straight above its seat with thin red lead lines from its pin/lead tips to the destination holes and light-blue-underlined hole labels, then drops straight down in the `c` step, where all annotations are removed. The camera moves only when entering a `Step N` or a card, never on a `Step Nc`.

## 2. Step table (every viewer step)

Camera notation: d = distance mm, e = elevation deg, az = azimuth deg. "same" = camera unchanged from the previous step. Label positions are the stored `screen (x, y)%`.

| idx | name | kind | what is added / done | annotations | camera |
|---|---|---|---|---|---|
| [000] | Start | title page | Finished Part-1 assembly shown (6 parts: base plate, breadboard, Nano, 2 resistors, capacitor). Nothing to do. | 2 unanchored 2D images: TechBox logo SVG top-left (w 33.2, at 2,4%); title PNG lower-left (w 58.3, at 2,24%) reading "Laser Stem Matrix (LSM)" / "Part 1" / "(c) 2025 TechBox. A division of TARIS Industries, LLC. All Rights Reserved." Model sits in the right half. | MOVES (initial fly-in) to d190 e47 az-141 |
| [001] | Step 1 | prep, before | Everything hidden except the breadboard, which is already lifted 39.3 mm above its final seat, with the grey backing sheet ("Paper") on its underside. Action: peel the adhesive backing. | 1 thick red 3D straight arrow, 39.4 mm, pointing straight down from the breadboard's front edge. 1 framed inset image (light-blue rounded frame, w 18.7, at 67,14%) showing the underside with the words "Protective Backing"; light-blue leader + dashed ring on the breadboard's bottom layer. Description: "Step 1 - Peel off the adhesive backing from the breadboard". | MOVES: rotates 78 deg, d190 e26 az-40; step transition = fade |
| [002] | Step 1c | prep, after | Backing sheet slides straight down 48.3 mm away from the breadboard (breadboard does not move). | none (arrow + inset removed). Description: "Step 1c". | same |
| [003] | Step 2 | hover | Base plate `LSM_Bottom_r1` (engraved "D1") fades in at its seated pose under the still-floating breadboard; backing sheet disappears. | 4 red lead lines, 39.3 mm each, vertical, from the 4 bottom corners of the breadboard to the 4 small L-shaped corner cut-outs in the plate. No labels, no description. | MOVES slightly: rotates 12 deg, target +34 mm, d190 e27 az-53 |
| [004] | Step 2c | completed | Breadboard drops 39.3 mm straight down -> seated on plate. | none. Description: "Step 2c". | same |
| [005] | Step 3 | hover | Arduino Nano fades in 35.3 mm above its seat (USB end toward column 16+). | 4 red lead lines (38.8-39.2 mm) from the four corner header pins down to breadboard holes. 2 labels: "Pin d12" (at 55,7%; ring on the Nano PCB at the D12 corner next to the USB socket) and "c16" (at 56,29%; ring on breadboard hole c16, where the D12 line lands). Description: "Step 3 - Align Nano Board pin D12 with Breadboard Slot C16". | same as [004] (view reused) |
| [006] | Step 3c | completed | Nano drops 35.3 mm -> seated. | none. Description: "Step 3c - Make Sure the Nano Board Touches the Breadboard". | same |
| [007] | Step 4 | prep close-up, before | Everything else hidden. Resistor 1 (bands brown-red-black-red-brown = 12 kOhm) alone, straight leads, already at its hover location. | 1 black eye icon (w 8.7, at 56,10%) above the body, light-blue leader + ring on a colour band. No text. | MOVES: zoom x2.52 to d75 e51 az78; step transition = fade |
| [008] | Step 4c | prep close-up, after | Straight-lead solids swapped for bent (staple-shaped) lead solids: visibility swap, no motion. | none | same |
| [009] | Step 5 | hover | Base, breadboard and Nano fade back in; bent Resistor 1 hovers 36.8 mm above its seat. | 2 red lead lines (41.4 mm) from each lead tip to its hole. 2 labels: "h16" (left, at 33,21%) and "h3" (right, at 68,20%), rings on the holes. | MOVES: zoom out x0.46 to d163 e40 az74 |
| [010] | Step 5c | completed | Resistor 1 drops 36.8 mm -> seated in h3/h16 (in front of the Nano). | none | same |
| [011] | Capacitor | section card | Everything else hidden. Capacitor alone, scaled x2, moved about 70 mm off its seat, stripe turned toward camera. Nothing to do: read polarity. | 1 framed diagram image (light-blue frame, w 32.0, at 49,19%) to the right of the 3D part: photo-style capacitor with tag "GND Strip", legs marked "GND" (black minus) and "VCC" (red plus); leader + ring on the 3D capacitor's grey stripe. | MOVES: rotates 135 deg to d60 e5 az-100 (almost side-on), FOV 45 -> 50 |
| [012] | Step 6 | hover | Base, breadboard, Nano and Resistor 1 fade back in; capacitor returns to scale 1 and hovers 32.9 mm above its seat (along its own slightly leaning axis). | 2 red lead lines (27.2-27.3 mm) from the two leg tips to the holes. 2 labels: "j3" (left, at 43,17%) and "j2" (right, at 68,22%). 1 eye icon (w 6.3) upper-left of the capacitor with leader + ring on the grey stripe. | MOVES: zoom out x0.37 to d163 e43 az58, FOV back to 45 |
| [013] | Step 6c | completed | Capacitor moves 32.9 mm -> seated in j2/j3 (stripe leg in j3). | none | same |
| [014] | Step 7 | prep close-up, before | Everything else hidden. Resistor 2 (orange-orange-black-black-brown = 330 Ohm) alone, straight leads, at its hover location. | 1 eye icon (w 9.4, at 31,6%) upper-left, leader + ring on a colour band. | MOVES: zoom x2.52 to d65 e33 az-104; step transition = fade |
| [015] | Step 7c | prep close-up, after | Straight leads swapped for bent leads (visibility swap). | none | same |
| [016] | Step 8 | hover | Base, breadboard, Nano, Resistor 1, capacitor fade back in; bent Resistor 2 hovers 31.4 mm above its seat. | 2 red lead lines (35.8 mm). 2 labels: "a11" (left, at 36,27%) and "a19" (right, at 63,29%). Description: "Step 6 - Bend the leads of the 330 Ohm Resistor and insert in breadboard slots A11 and A19" (stale number, see anomalies). | MOVES: zoom out x0.4 to d163 e27 az-138 (opposite side of the board) |
| [017] | Step 8c | completed | Resistor 2 drops 31.4 mm -> seated in a11/a19. | none | same |
| [018] | Completed View | final view | Nothing added. | none | MOVES: pull back x0.86 to d190 e48 az-146 (within ~5 deg of the title-page view) |

Totals: 1 title + 8 `Step N` + 8 `Step Nc` + 1 section card + 1 final = 19. Camera moves on 10 of 19 steps ([000] [001] [003] [007] [009] [011] [012] [014] [016] [018]). Annotations shown: 14 lead lines, 1 arrow, 8 labels, 3 eye icons, 2 framed inset images, 2 title images.

## 3. Conventions found

### Structure
- **S1. Fixed skeleton** (always): `Start` -> numbered step pairs -> `Completed View`. Here 1 + 16 + 1 card + 1.
- **S2. Every numbered step is a pair** `Step N` / `Step Nc` (8/8). `Step N` = the annotated "before" (part hovering, or part before manipulation); `Step Nc` = the same scene after the action.
- **S3. `Nc` steps are always clean**: annotation count is 0 in all 8 `c` steps; every annotation introduced in `Step N` is removed in `Step Nc` (8/8). Annotations never persist across a pair boundary.
- **S4. Numbering is continuous and counts preparation actions**: 1 peel, 2 breadboard-on-base, 3 Nano, 4 bend R1, 5 insert R1, 6 capacitor, 7 bend R2, 8 insert R2.
- **S5. Section card**: one unnumbered step named after the part (`Capacitor`, [011]) sits immediately before the step that installs it. It isolates the part, enlarges it (scale x2) and pairs it with a framed reference diagram. Only 1 card in this guide; it is used for the only polarity-sensitive part.
- **S6. Title page** [000]: 2D logo top-left, 2D title/subtitle/copyright block lower-left, finished model of *this part* on the right, no leaders. `Completed View` [018] returns to nearly the same camera (d190, e47/48, az-141/-146) with no annotations.
- **S7. All steps wait for the student**: 19/19 `pause`, 19/19 duration 800 ms. No `Transition` (auto-advance) steps in this guide.

### Granularity
- **G1. One physical part per numbered step** (5/5 placement steps: breadboard, Nano, R1, capacitor, R2). Nothing is ever added in a group here.
- **G2. A manipulation of a part gets its own step pair before the placement** (3/3): peel backing [001]/[002], bend R1 leads [007]/[008], bend R2 leads [014]/[015].
- **G3. Multi-pin part is still one step**: the 30-pin Nano is one step with only its four corner pins annotated.

### Ordering
- **O1. Bottom-up and big-before-small**: breadboard prep -> base plate + breadboard -> Nano (establishes the column reference: D12 in c16) -> resistor 1 -> capacitor -> resistor 2.
- **O2. Prep immediately precedes use**: each bend close-up is directly followed by the insertion of that same resistor; the capacitor card is directly followed by the capacitor step.
- Not observable here: any power-before-signal wire ordering (no wires in Part 1).

### Motion
- **M1. Hover-then-drop** (5/5 placements): the part is shown displaced straight up from its seat (39.3, 35.3, 36.8, 32.9, 31.4 mm; mean 35 mm) and in `Nc` tweens in one straight move to the seat. Single stage, no rotation, no sideways approach.
- **M2. Which part appears vs which part moves** (exception to "new part hovers"): in Step 2 the *new* part (base plate) fades in at its seated pose, and the part the student is holding (breadboard, already on screen and pre-lifted in Step 1) is the one that hovers and then drops. So the rule is "the part in the student's hand moves", not "the new part moves".
- **M3. Shape change = model swap** (2/2): straight-lead resistor -> bent-lead resistor is an APPEAR + DISAPPEAR of lead solids between `Step N` and `Step Nc`, no MOVE, camera fixed. Same mechanism the README describes for straight -> routed wires.
- **M4. Isolation close-ups** (3/3: [007] [014] [011]): all other parts are hidden and the camera zooms x2.5-2.7 onto the single part. For the resistors the part is already at its hover location, so the following step only zooms out while the context fades back in. For the capacitor card the part is additionally moved about 70 mm aside and scaled x2, then returns to scale 1 / hover pose on Step 6.
- **M5. Peel shown as translation**: backing sheet moves 48.3 mm straight down [002]; the arrow in [001] previews this direction.
- **M6. Animation settings** (19/19): parts move by tween, show/hide by fade, 2D annotations fade; camera tween, `animate_orbit` false, speed 2.

### Red lead lines and arrows
- **L1. Colour and form**: all 14 lines are #ff0000, thin, straight, 2-point, parallel to the travel direction (vertical). Each is anchored at one end to the moving part and at the other to the target part, so it shortens as the part seats and is then hidden.
- **L2. One line per engaging feature, capped at four**: 2-lead parts get 2 lines, one per lead tip -> hole (R1 [009], capacitor [012], R2 [016]; 3/3). Large parts get exactly 4 lines at the corners: breadboard bottom corners -> the plate's 4 L-shaped corner cut-outs [003]; Nano's four corner header pins -> their 4 breadboard holes [005].
- **L3. Start and end features**: start = tip of the pin/lead (or bottom corner edge of the breadboard); end = the destination hole (lines end a few mm inside the hole) or the locating cut-out.
- **L4. Length is about the hover offset**: breadboard 39.3 vs 39.3 (ratio 1.00); Nano 39.2 vs 35.3 (1.11); R1 41.4 vs 36.8 (1.12); R2 35.8 vs 31.4 (1.14); capacitor 27.3 vs 32.9 (0.83). Range 0.83-1.14.
- **L5. No lead lines in prep steps or cards** (0 lines in [001] [002] [007] [008] [011] [014] [015]).
- **A1. Arrow**: a thick red 3D straight arrow is used once [001], for a removal/peel direction, not for an insertion. Insertions use lead lines only.

### Labels and callouts
- **T1. Label style** (8/8 labels): Arial bold 2.5em, black, centred, sitting on a light-blue (#7fdbff) underline; a light-blue leader leaves the end of the underline nearest the target, and ends in a dashed light-blue ring ("Life Saver Circle") exactly on the feature.
- **T2. Label content** = breadboard hole coordinate in lower case, one label per destination hole (7 of 8 labels: c16, h3, h16, j2, j3, a11, a19). The 8th is "Pin d12" on the Nano. No label names a part.
- **T3. Reference-pin pattern for multi-pin boards** [005]: label one reference pin on the part ("Pin d12") and its matching hole ("c16"), both stacked on the same side (right), instead of labelling every pin.
- **T4. Two-hole parts**: the two labels go left and right of the hovering part in the same left/right order as the holes on screen, in the upper third of the frame (y 17-29%, x 33-68%); leaders do not cross (3/3: [009] [012] [016]).
- **T5. Labels only on hover steps** that plug into the breadboard (4/5 placements). Exception: Step 2 (breadboard onto plate) has lead lines but no labels.
- **T6. Step description text** follows "Step N - imperative sentence" when present, but is only filled on 6/19 steps ([001] [002] [004] [005] [006] [016]); the on-screen graphics carry the instruction alone on the others.
- **E1. Eye icon** (3 uses): black eye image with light-blue leader + ring on the feature to inspect. On resistor close-ups it points at the colour bands ([007] [014], 2/2: identify the value before bending); on the capacitor hover step it points at the polarity stripe ([012]). Meaning: "check this before you act". Placed above/upper-left of the part, width 6-9% of the viewport.
- **I1. Framed inset image** (2 uses): light-blue rounded rectangular frame with leader + ring to the 3D feature, used where the 3D model cannot convey it: "Protective Backing" underside view [001]; capacitor polarity diagram with GND Strip / GND / VCC [011].
- **I2. Title images** are unanchored, no frame.

### Camera
- **C1. Camera never moves on `Nc`** (0/8). The before/after pair is always seen from the identical viewpoint.
- **C2. Camera moves when entering a `Step N` or a card** (7 of 8 `Step N`, the card, start, end). Exception: Step 3 [005] reuses the Step 2 view because the Nano lands on the same area.
- **C3. Two zoom levels**: assembly views at d190 (steps 1-3, Start, Completed View) or d163 (steps 5, 6, 8); isolated-part close-ups at d60-75 (x2.5-2.7).
- **C4. Orbit, do not chase**: across the assembly views [003] [009] [012] [016] the orbit target stays within 7 mm of the same point (board centre); only azimuth (-53, 74, 58, -138) and elevation (27-43 deg) change, so that the destination holes are on the near side and not hidden behind the Nano. The camera does not zoom in on the individual hole.
- **C5. Three-quarter views only**: elevation 26-51 deg for all build steps; never top-down. Exception: the Capacitor card at e5 (side-on) with FOV 50; everything else is perspective FOV 45.
- **C6. Composition**: frame is about 2:1. In assembly views the model occupies roughly the middle 45% of the width (x 26-72%) and y 22-87%; the hovering part rises into the top 2-16% of the frame; the white side margins hold the labels.

### Look
- **K1.** Pure white background (#ffffff, set on the first step; project default is #EEEEEE), no ground plane, no shadows.
- **K2.** All 1058 solids use the "toon" style with "normal" edges: flat cel-shaded fills with thin black outlines.
- **K3. Annotation colour code**: red (#ff0000) = motion (lead lines, arrow); light blue (#7fdbff) = information (label underline, leaders, ring anchors, inset frames); black = label text and eye icon.

## 4. Part looks (from the renders)

| part | look |
|---|---|
| Base plate `LSM_Bottom_r1` | Laser-cut wood: flat light tan top (renders ~#ffd89f, material #deb887), darker tan edge faces (~#d0a878), black outlines, black engraved "D1" on the top face; tabs, slots and 4 small L-shaped breadboard-corner cut-outs. |
| Breadboard | White top (~#fdfdfd), very light grey side walls (~#efefef); each tie-point drawn as a small black-outlined square; black printed column numbers and row letters a-j; thin red and blue power-rail stripes with + / - marks; small white clip nubs on the sides. |
| Backing sheet ("Paper") | Flat light grey rectangle (~#c8c8c8, material #aaaaaa) with black outline. |
| Arduino Nano | Navy PCB (~#001048), black pin-header strips, silver-grey pins, gold/tan 2x3 ICSP pins (#c8b273), silver mini-USB shell, black IC, white/silver small components. |
| Resistors | Bright blue dog-bone body (#0074d9, lit ~#0189ff); saturated colour bands: R1 brown-red-black-red-brown, R2 orange-orange-black-black-brown (brown #a36315, red #ff0e00, orange #ff851b, black); silver-grey leads (#a6a9aa), straight then bent into a staple. |
| Capacitor | Black cylinder with a grey/silver polarity stripe and grey top (#a6a9aa), two silver legs; modelled leaning slightly. |
| Lead lines / arrow | Thin pure-red lines; one thick pure-red 3D arrow with a large head. |
| Labels | Black Arial bold on a light-blue underline, light-blue elbow leader, dashed light-blue ring at the target. |
| Eye icon | Solid black eye glyph with white iris ring, light-blue leader + ring. |
| Inset images | White panel with light-blue rounded frame; "Protective Backing" is a grey-on-white render with small text; the capacitor diagram is photo-style with a dark "GND Strip" tag, black minus "GND" and red plus "VCC". |
| Title art | Cyan TECHBOX logo plate (bulb + gear icon, white text); dark-grey condensed bold title, small serif copyright line. |

## 5. Anomalies and inconsistencies

1. **Stale step number in description**: viewer step "Step 8" [016] carries the description "Step 6 - Bend the leads of the 330 Ohm Resistor and insert in breadboard slots A11 and A19". The text predates the bend steps being numbered (it also describes bend + insert as one action, while the bend is shown separately in Step 7/7c).
2. **Descriptions are sparse and uneven**: only 6/19 steps have any; two are bare placeholders ("Step 1c", "Step 2c"); Steps 2, 4, 5, 6, 7 have none here although the combined Part 1+2 guide has text for the same steps (e.g. "Step 2 - Place Breadboard on the Housing Base, centered in the L-Shaped cutouts").
3. **Case mismatch between labels and text**: labels use lower case ("Pin d12", "c16", "a11"), descriptions use upper case ("pin D12", "Slot C16", "A11 and A19"). Description capitalisation is itself inconsistent (sentence case in Step 1, Title Case in Step 3c).
4. **Resistor value is never shown on screen**: Steps 4 and 7 identify the resistor only by the eye icon on the colour bands; "12k" appears nowhere in this guide and "330 Ohm" only in the misnumbered description.
5. **Lead-line style flag inconsistent**: of the 14 lines shown, 5 are stored as "dashed" ([005] 1 of 4, [009] 2, [016] 2) and 9 as "solid" ([003] 4, [005] 3, [012] 2). In the saved renders all 14 look solid, so the flag is not a visible convention here. In [005] one of the four lines is also anchored in the reverse order (breadboard -> Nano, 38.8 mm) to the other three (39.2 mm).
6. **Label leader property inconsistent**: "Pin d12", "h3", "h16" have no stored leader colour while the other five have #7fdbff; "c16" has thickness 6 instead of 5. All eight render the same.
7. **Capacitor card differs from the other close-ups**: FOV 50 instead of 45, step transition "none" where the other isolating close-ups ([001] [007] [014]) use "fade". Its thumbnail and diagram asset are dated 2026-09-22 while the rest of the guide's assets are dated 2025-07 to 2025-10, so the card is a late insertion; internal step `index` 13 is duplicated on Step 6c and Step 7 as a result.
8. **Capacitor leans**: its assembly transform is tilted about 6 deg from vertical, so the seated capacitor and its two lead lines visibly lean in [012] [013] [016]-[018]. The digest reports its hover as "[0, -32.9, 0] ... MOVE +Y (up)" because the offset is in the part's flipped local frame; in the render it hovers above and moves down like every other part.
9. **Stored position of the eye icon in [012]** is (-6, 16)% but it renders at about (56, 6)%; stored image positions are not reliable for layout.
10. **Arrow anchoring**: the peel arrow [001] is anchored to the breadboard body, not to the backing sheet, and its length (39.4 mm) matches the breadboard's hover offset rather than the sheet's 48.3 mm travel.
11. **Residual data offsets** (not visible): 7 Nano sub-solids remain 1.6-2.8 mm off their CAD pose when "seated"; bent resistor leads and capacitor legs carry ~1.7 m offsets because their CAD home is elsewhere. The digest therefore lists Nano/Resistor/Capacitor as "still displaced" to the end.
12. **Leftover content**: only 7 of the project's 46 top-level components are ever shown (base plate, breadboard, backing sheet, Nano, 2 resistors, capacitor). The other 39 are hidden Part-2 content (8x8 LED matrix x2, jumper wires and their 13 connector caps, 2 push-button models, 3 USB cable parts, side panel), and there are unused annotations (labels i2, i3, I3, b19, j5, j16, In, V+, "/ / V-"; 6 more eye icons; 6 unused lead lines; 1 unused arrow). Part tooltips are enabled but hold only placeholder text ("Description" / "none").
13. **Naming**: title reads "Laser Stem Matrix" ("Stem", not "STEM").

## 6. Relation to the other LSM guides (checked against their digests)

- **Part 1+2 combined (`…lsm_part_1_2`)**: its steps [001]-[016] are the same authored steps as Part 1 [001]-[017] with identical cameras (d190/e26/az-40, d190/e27/az-53, d75/e51/az78, d163/e40/az74, d163/e43/az58, d65/e33/az-104, d163/e27/az-138), identical lead-line lengths (39.3 x4, 38.8/39.2 x3, 41.4 x2, 27.3/27.2, 35.8 x2), identical labels and eye-icon widths. Differences: the combined guide has **no `Capacitor` card** (goes Step 5c -> Step 6) and has **more descriptions filled in** ("Step 4 - Bend the leads of the 12k Ohm Resistor and insert in breadboard slots H3 and H16", "Step 5 - Install the Capacitor into breadboard slots J2 and J3 (with the grey-striped side in slot J3)"), which confirms the description numbering runs behind the viewer step names. It then continues numbering with Step 9 (first wires) instead of ending.
- **Part 2 (`…lsm_-_part_2`)**: same project lineage (identical annotation inventory: 19 labels, 19 images, 20 lead lines). It restarts numbering at Step 1 but its descriptions still say "Step 7 …", "Step 9 …", i.e. they continue from Part 1's old numbering. Its title page shows the whole Part 1+2 result; its first step hides the Part 1 assembly to show wires alone.
- **Full build (`…lsm_-_full_build`)**: same sequence and structure for these parts (Step 1 peel ... Step 8 R2, including the `Capacitor` card between 5c and 6) but re-authored: different Nano model, longer hover/lead lines (about 50 mm for breadboard and Nano), camera further out (d221/d189), all lead lines in these steps solid, no "Pin d12"/"c16" labels on Step 3, no descriptions on these steps, and an auto-advancing `Transition` inserted between Step 1 and Step 1c.
- Net: Part 1 is the first third of one shared authoring, trimmed after Step 8c, with a `Completed View` appended and the `Capacitor` card added later (also present in the full build).
