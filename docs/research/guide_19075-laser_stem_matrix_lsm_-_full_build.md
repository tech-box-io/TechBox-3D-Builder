# Guide report: Laser Stem Matrix (LSM) - Full Build

Guide id: `19075-laser_stem_matrix_lsm_-_full_build` (kit LSM, role: full build)
Sources read: full digest (.md + .json), all 11 contact sheets, about 45 individual frames plus zoomed crops, targeted queries on the raw payload, and the digests of LSM Parts 1, 2, 3, 4 and the two combined guides (1+2, 3+4) for the comparison in section 8.

## 1. Summary

The full build takes the student from a bare breadboard to the finished Laser Stem Matrix in 88 viewer steps: 1 title page, 38 numbered steps each shown as a pair (`Step N` = annotated "how" view, `Step Nc` = clean "done" view; 76 steps), 4 named section cards that show a component on its own (`Capacitor`, `LED Matrix Diagram`, `Mini USB Cable`, `LED Stems`), 6 auto-advancing `Transition` steps and 1 `Completed View`. Electronics are built first on the flat base (breadboard, Nano, two resistors and a capacitor, a 3-wire ribbon to the 8x8 LED matrix, a panel-mounted push button, USB cable), then the laser-cut housing is closed around them (panels D2, D4, D3, D5), then the LED matrix is hung on supports D9/D10, three perforated shelves D6/D7/D8 are stacked on four D11 posts, and 64 light-guide stems are dropped in. The guide is entirely wordless: all 88 step descriptions are empty and there are no popups; everything is carried by red lead lines (57 shown), red arrows (4), cyan-underlined breadboard-hole labels (14 + one "64x"), a black eye icon (11 uses), disc badges (6) and cyan-framed inset pictures (5). The camera never moves inside a step pair, a new part normally fades in hovering on its insertion axis and tweens home in the `c` view (800 ms), and wires/flexible parts are instead swapped between pre-modelled poses. It is not a plain concatenation of the four part guides: step count and order are the same except for one swap, but the Part 1 and Part 2 region was re-shot (all 46 mapped steps have a different camera pose) while the Part 3 and Part 4 region is reused almost verbatim (25 of 39 mapped steps have an identical camera pose).

## 2. Notes on the data (read before trusting numbers)

- The digest's APPEAR/MOVE lines are incomplete for this guide. Components whose top-level node is flagged `hidden` in the CAD tree (side panels D3/D4/D5, shelves D6-D8, posts D11, LED-matrix pose variants, most stems, one D2 instance) never show up as "appeared" in the digest, e.g. digest steps [048]-[058] list no part changes at all although the thumbnails clearly show panels D4, D3 and D5 arriving. I re-resolved visibility and offsets from `cadasio_raw` at leaf level; the hover offsets quoted below for those parts come from that, cross-checked against the thumbnails.
- Huge offsets such as `[570.8, 911.0, 1127.2]mm` in the digest are components whose model origin is the assembly origin (paper sheet, bent resistor legs, loose wire caps, stems). They are placements, not hover offsets, and are ignored here.
- Stored 2D screen positions agree with the saved renders for the text labels, but not always for images: Step 6's eye icon is stored at x = -6 % yet is rendered at about 54 %, and Step 34/34c store the eye/inset on the right (92 %/71 % and 87 %/46 %) while the saved renders show them on the left. Thumbnails are treated as ground truth for layout.
- Five object ids referenced by annotations do not exist in the current CAD tree (old breadboard, button and stem bodies). Lead lines anchored to them still render in the thumbnails.

## 3. Outline

| viewer steps | numbered steps | section |
|---|---|---|
| 000 | - | Title page |
| 001-007 | 1-3 | Breadboard: peel backing, onto base D1, Nano on |
| 008-018 | 4-8 (+ Capacitor card) | Passives: 12 kOhm resistor, capacitor, 330 Ohm resistor |
| 019-026 | 9-12 | 3-wire ribbon: split, then one male end per step into i2, i3, b19 |
| 027-033 | 13-15 (+ LED Matrix Diagram card) | Same three wires, female ends onto the LED-matrix pads |
| 034-042 | 16-19 | Push button sub-assembly on panel D2, its two leads into row j |
| 043-047 | 20-21 (+ Mini USB Cable card) | USB cable into the Nano, D2 panel stood on the base |
| 048-058 | 22-26 | Housing walls: D4 rear, matrix passed outside, D3 right (hook + swing), D5 front |
| 059-068 | 27-30 | LED supports D9 x2, D10 hooked on the matrix, matrix lowered in |
| 069-081 | 31-36 | Shelf D6, four posts D11 (2 + 2), underside tab check, shelves D7 and D8 |
| 082-086 | 37-38 (+ LED Stems card) | One stem, then all 64 |
| 087 | - | Completed View |

## 4. Step table (every viewer step)

Legend. kind: `step` = `Step N`, `c` = `Step Nc`, `card` = named section card, `transition` = behaviour `play` (auto-advance, hidden from the step picker). Camera: "same" = identical pose to the previous step; otherwise rotation of the view direction, then resulting distance (mm) / elevation / azimuth. Lead-line lengths are the stored 3D lengths. All steps are 800 ms unless noted.

| # | name | kind | what is added or done | annotations | camera |
|---|---|---|---|---|---|
| 000 | Start | start | Title page. Finished LSM model on the right half; branding on the left. | 2 unanchored images: TechBox logo SVG (w 37.6 %, at 2 %/5 %) and title PNG "Laser Stem Matrix (LSM) / Full Build / (c) 2025 TechBox..." (w 42.9 %, at 2 %/61 %) | moves 18 deg -> d374 el29 az54 |
| 001 | Step 1 | step | Breadboard alone, floating (held 49 mm above its future seat). Action: peel the protective backing. | 1 red arrow (35 mm, straight down from the underside); 1 cyan-framed inset image "Protective Backing" (w 21.7 %) with cyan leader to a ring on the board edge | moves 83 deg -> d221 el26 az-43 |
| 002 | Transition | transition (auto) | Grey backing sheet tweens 39 mm straight down away from the breadboard. | none (arrow + inset removed) | same |
| 003 | Step 1c | c | Backing sheet hidden; bare breadboard. | none | same |
| 004 | Step 2 | step | Housing base D1 fades in at its seat; the breadboard is the hovering part (49 mm above). | 4 lead lines (50 mm): breadboard bottom corners -> corner marks on D1 | moves 11 deg -> d221 el34 az-52 |
| 005 | Step 2c | c | Breadboard tweens down 49 mm onto D1. | none | same |
| 006 | Step 3 | step | Arduino Nano fades in 44 mm above the breadboard. | 4 lead lines (49 mm): four corner header pins -> breadboard holes. No hole label | same |
| 007 | Step 3c | c | Nano tweens down 44 mm into the breadboard. | none | same |
| 008 | Step 4 | step | Resistor 1 (12 kOhm, blue body) alone, legs straight. Rest of model hidden. | eye icon -> colour bands | moves 96 deg -> d75 el35 az78 |
| 009 | Step 4c | c | Same resistor with both legs bent 90 deg (straight-leg solids swapped for bent-leg solids). | none | same |
| 010 | Step 5 | step | Assembly returns; resistor 1 hovers 32 mm above its holes. | 2 lead lines (30 mm): leg tips -> holes; 2 labels "h16" (left) and "h3" (right) | moves 14 deg -> d189 el41 az61 |
| 011 | Step 5c | c | Resistor 1 tweens down 32 mm. | none | same |
| 012 | Capacitor | card | Section card: capacitor alone, exactly side-on, grey stripe facing camera. | 1 cyan-framed inset photo (w 30.3 %) "GND Strip / GND - / VCC +" with leader to the stripe | moves 49 deg -> d42 el0 az90 |
| 013 | Step 6 | step | Assembly returns; capacitor hovers 29 mm above its holes (turned to mounting orientation). | 2 lead lines (28 mm): legs -> holes; 2 labels "j3", "j2"; eye icon -> grey stripe | moves 49 deg -> d189 el41 az61 |
| 014 | Step 6c | c | Capacitor tweens down 29 mm. | none | same |
| 015 | Step 7 | step | Resistor 2 (330 Ohm) alone, legs straight. | eye icon -> colour bands | moves 114 deg -> d64 el23 az-107 |
| 016 | Step 7c | c | Resistor 2 with legs bent (solid swap). | none | same |
| 017 | Step 8 | step | Assembly returns; resistor 2 hovers 30 mm above its holes. | 2 lead lines (35 mm); 2 labels "a11", "a19" | moves 28 deg -> d189 el32 az-137 |
| 018 | Step 8c | c | Resistor 2 tweens down 30 mm. | none | same |
| 019 | Step 9 | step | 3-wire jumper ribbon (white / grey / purple, male pins one end, female housings the other) alone, wires still joined. | eye icon -> ribbon | moves 67 deg -> d119 el55 az-41 |
| 020 | Step 9c | c | Ribbon swapped for a version with both ends split into three separate leads. | none | same |
| 021 | Step 10 | step | Assembly returns; split ribbon floats above the board. Wire 1 of 3 (white), male end. | 1 label "i2" -> white wire's male pin housing (label names the target hole, leader points at the wire end) | moves 70 deg -> d189 el30 az-139 |
| 022 | Step 10c | c | White wire swapped for its routed model, plugged into i2. | none | same |
| 023 | Step 11 | step | Wire 2 of 3 (grey), male end. | 1 label "i3" -> grey wire's male pin housing | same |
| 024 | Step 11c | c | Grey wire swapped for routed model in i3. | none | same |
| 025 | Step 12 | step | Wire 3 of 3 (purple), male end. | 1 label "b19" -> purple wire's male pin housing | moves 6 deg -> d189 el28 az-133 |
| 026 | Step 12c | c | Purple wire swapped for routed model in b19. | none | same |
| 027 | LED Matrix Diagram | card | Section card: no 3D parts. Full-frame 2D diagram of the back of the LED matrix. | 1 unanchored image (w 65 %): black square with two red-boxed pad groups, each with an eye icon + cyan leader baked into the picture | moves 87 deg -> d221 el22 az128 |
| 028 | Step 13 | step | Assembly returns with the 8x8 LED matrix floating above it (first appearance, no lead lines). White wire, female end -> matrix pad. | cyan disc badge "V+" -> matrix pad; white disc badge "V+" -> wire's female end; label "i2" -> breadboard hole (identifies which wire) | same |
| 029 | Step 13c | c | White wire swapped for model routed up to the matrix. | none | same |
| 030 | Step 14 | step | Purple wire, female end -> matrix pad. | cyan + white disc badges "V-In"; label "b19" -> breadboard hole | moves 125 deg -> d189 el23 az-19 |
| 031 | Step 14c | c | Purple wire swapped for routed model. | none | same |
| 032 | Step 15 | step | Grey wire, female end -> matrix pad. | cyan + white disc badges "V-"; label "i3" -> breadboard hole | moves 108 deg -> d258 el15 az-137 |
| 033 | Step 15c | c | Grey wire swapped for routed model. | none | same |
| 034 | Step 16 | step | Push button alone, with its red + black leads and the hex nut still on. Action: take the nut off. | 1 thick red arrow (69 mm) along the button axis, from the nut towards the lead ends | moves 78 deg -> d162 el38 az-51 |
| 035 | Transition | transition (auto, 1600 ms) | Nut tweens 101 mm along the leads while rotating (only 1600 ms step). | none (arrow removed) | same |
| 036 | Step 16c | c | Nut hidden; bare button + leads. | none | same |
| 037 | Step 17 | step | Left housing panel D2 fades in; button + leads float 102 mm from it on the hole axis. | 1 lead line (106 mm): hole centre <-> button barrel | moves 3 deg -> d189 el35 az-49 |
| 038 | Step 17c | c | Button + leads tween 102 mm through the hole. | none | same |
| 039 | Step 18 | step | View swings to the inside face; nut fades in 83 mm out along the leads. | 1 lead line (92 mm): nut <-> button thread | moves 114 deg -> d189 el30 az142 |
| 040 | Step 18c | c | Nut tweens 83 mm (with rotation) onto the thread. | none | same |
| 041 | Step 19 | step | Electronics assembly returns beside the floating D2 + button; LED matrix lies next to it. Both button leads in one step. | 2 labels "j5" (left) and "j16" (right) -> the two lead pin housings | moves 9 deg -> d258 el36 az149 |
| 042 | Step 19c | c | Both leads swapped for routed models plugged into row j. | none | same |
| 043 | Mini USB Cable | card | Section card: mini-USB cable alone (right-angle mini plug + USB-A). | eye icon -> cable | moves 74 deg -> d221 el51 az41 |
| 044 | Step 20 | step | Assembly returns (no cable). Where the cable goes. | eye icon -> Nano's USB socket | moves 43 deg -> d300 el48 az-28 |
| 045 | Step 20c | c | Cable fades in already plugged into the Nano (no travel). | none | same |
| 046 | Step 21 | step | Action: stand the D2 panel (with button) on the base. | 1 red arrow (45 mm) from the floating D2 panel towards the base edge | moves 62 deg -> d300 el51 az-133 |
| 047 | Step 21c | c | Floating D2 + button + leads swapped for the seated version: D2 standing in D1's edge slots, leads re-routed. | none | same |
| 048 | Step 22 | step | Rear panel D4 fades in 69 mm out from the rear edge. | 4 lead lines (65-69 mm): 2 from D2's end tabs, 2 from D1's edge tabs -> D4's slots | moves 57 deg -> d350 el43 az-45 |
| 049 | Step 22c | c | D4 tweens 69 mm in. | none | same |
| 050 | Step 23 | step | Top-down view. Action: carry the LED matrix across to the D4 side. | 1 red arrow (103 mm) pointing across the top; eye icon -> LED matrix | moves 43 deg -> d300 el85 az-18 |
| 051 | Step 23c | c | Matrix + its 3 wires swapped to a new pose outside D4, wires passing through D4's notch. | eye icon -> the notch (one of only 3 annotated c-views) | same |
| 052 | Transition | transition (auto) | Camera only: swings 130 deg to an underside/outside view (model turned over). | none (eye removed) | moves 130 deg -> d300 el-35 az141 |
| 053 | Step 24 | step | Right panel D3 fades in tilted about 22 deg and 64 mm away. | 2 lead lines (42 mm): D3 edge tabs -> D4 slots | same |
| 054 | Step 24c | c | D3 tweens 46 mm so its tabs sit in D4, still tilted. | none | same |
| 055 | Step 25 | step | Same view; second half of the same part. | 2 short lead lines (13-16 mm): D1 tabs -> D3 slots | same |
| 056 | Step 25c | c | D3 rotates about 22 deg shut (tween + rotation). | none | same |
| 057 | Step 26 | step | Front panel D5 fades in 42 mm off the open side. | 4 lead lines (39-43 mm): tab tips of D3 (x2) and D2 (x2) -> D5 slots | moves 76 deg -> d300 el41 az129 |
| 058 | Step 26c | c | D5 tweens 42 mm on. Housing walls complete. | none | same |
| 059 | Transition | transition (auto) | Camera only: 53 deg, back upright, looking into the open box. This is the Part 3 / Part 4 seam. | none | moves 53 deg -> d300 el31 az-165 |
| 060 | Step 27 | step | Two wide LED supports D9 fade in together 65 mm above the box. | 4 lead lines (65 mm): each D9 end tab -> wall slot | same |
| 061 | Step 27c | c | Both D9 tween down 65 mm. | none | same |
| 062 | Step 28 | step | Action: pick up the LED matrix (lying outside the box). | eye icon -> LED matrix | moves 32 deg -> d300 el23 az-129 |
| 063 | Step 28c | c | Matrix + wires swapped to a pose hovering above the box, LEDs up. | none | same |
| 064 | Step 29 | step | LED support D10 fades in below the floating matrix. | 2 L-shaped 3-point lead lines (44 mm): D10's two hooks, up, then across to the matrix edge | moves 14 deg -> d258 el18 az-116 |
| 065 | Transition | transition (auto) | D10 tweens 22 mm (first leg, up to matrix level). | none (lines removed) | same |
| 066 | Step 29c | c | D10 tweens 40 mm sideways onto the matrix edge (second leg). | none | same |
| 067 | Step 30 | step | Matrix + D10 about to be lowered into the box. | 2 lead lines (56-57 mm): D10 ends -> slots in the D4 / D5 walls | moves 77 deg -> d258 el23 az-32 |
| 068 | Step 30c | c | Floating matrix + D10 + wires swapped for the seated versions inside the box. | 1 cyan-framed inset image (w 16.8 %, eye icon baked in) of the wire routing, leader into the box | same |
| 069 | Step 31 | step | Bottom shelf D6 (64 square holes) fades in 64 mm above. | 4 lead lines (62-70 mm): D6's 4 slots -> wall tabs; 1 cyan-framed inset (w 22.2 %) top view of the matrix with 4 red corner boxes | moves 69 deg -> d258 el31 az47 |
| 070 | Step 31c | c | D6 tweens down 64 mm. | none | same |
| 071 | Step 32 | step | Two shelf supports D11 fade in 89 mm above. | 2 lead lines (44 mm): D11 lower tip -> corner slot in D6 | moves 14 deg -> d300 el21 az36 |
| 072 | Step 32c | c | Both tween down 82 mm (stop 7 mm short of fully seated). | none | same |
| 073 | Step 33 | step | The other two D11 fade in 84-90 mm above. | 2 lead lines (37-43 mm) | moves 82 deg -> d300 el23 az-55 |
| 074 | Step 33c | c | Both tween down 77-83 mm (7 mm short). | none | same |
| 075 | Step 34 | step | Underside view; base D1 and front D5 ghosted to 50 % opacity so the D11 tabs are visible. | eye icon -> one tab; 4 short lead lines (17 mm): D11 tabs -> D1 slots | moves 117 deg -> d258 el-57 az49 |
| 076 | Step 34c | c | All four D11 tween the last 7 mm so their tabs lock through D1; D1 opaque again. | 1 cyan-framed inset close-up (w 14.2 %, eye icon baked in) of a locked tab | same |
| 077 | Transition | transition (auto) | Camera only: 110 deg, back upright. D5 opacity restored. | none (inset removed) | moves 110 deg -> d300 el34 az123 |
| 078 | Step 35 | step | Middle shelf D7 fades in 68 mm above. | 4 lead lines (49 mm): D11 tops -> D7 slots | same |
| 079 | Step 35c | c | D7 tweens down 68 mm. | none | same |
| 080 | Step 36 | step | Top shelf D8 fades in 54 mm above. | 4 lead lines (59-63 mm): D11 tops -> D8 slots | same |
| 081 | Step 36c | c | D8 tweens down 54 mm. | none | same |
| 082 | LED Stems | card | Section card: one white LED stem alone. | 1 label "64x" (cyan bold 6em, no frame, no leader) to the right of the stem | moves 75 deg -> d173 el31 az32 |
| 083 | Step 37 | step | Assembly returns; one stem hovers 44 mm above a corner hole of D8. | 1 lead line (44 mm): stem <-> LED underneath (mostly hidden by the shelves) | moves 0 deg -> d374 el31 az32 |
| 084 | Step 37c | c | Stem tweens down 44 mm. | none | same |
| 085 | Step 38 | step | Repeat for the rest. | eye icon -> the inserted stem | same |
| 086 | Step 38c | c | Remaining 63 stems fade in, already seated. | none | same |
| 087 | Completed View | completed | Finished model, clean. | none | moves 13 deg -> d321 el39 az44 |

## 5. Conventions found

### 5.1 Structure and numbering

- **Always: every numbered step is a pair `Step N` / `Step Nc`.** 38 of 38. `Step N` shows the situation before the action with annotations; `Step Nc` shows the result. Numbering is continuous 1-38 with no gaps or repeats.
- **Always: `Step N` carries at least one annotation** (38/38). Combinations seen: lead lines only (16 steps), eye icon only (6), label only (3), 2 badges + label (3), labels + lead lines (2), arrow only (2), arrow + image (2), lead lines + inset image (2), labels + lead lines + eye (1), 2 labels (1).
- **Usually: `Step Nc` is clean.** 35 of 38 have no annotation. Exceptions: 23c [051] (eye icon on the notch the wires pass through), 30c [068] and 34c [076] (cyan-framed inset close-ups). All three are "check this result" hints, not instructions for a move.
- **Section cards** are named, paused steps that show something in isolation before its first use: `Capacitor` [012], `LED Matrix Diagram` [027], `Mini USB Cable` [043], `LED Stems` [082]. A card is used when the student only has to look (polarity, pad names, which cable, quantity). When the isolated part needs preparing, the isolated view is a numbered step instead and its `c` view shows the prepared part: resistors with legs bent (Steps 4, 7), ribbon split (Step 9), nut removed (Step 16). Cards are not numbered and do not have a `c` partner.
- **Transition steps** (6, behaviour `play`, `hideInStepPicker: true`, no annotations) come in two flavours:
  - mid-step motion, placed between `Step N` and `Step Nc` (3): [002] backing sheet drops away, [035] nut slides off (the only 1600 ms step), [065] first leg of D10's two-leg move;
  - camera-only, placed between two numbered steps (3): [052], [059], [077]. All three coincide with a change of the scene `up_axis`, i.e. they are used when the model is turned over to or from an underside view.
  - Exception: two "turn-over" views are entered directly without a Transition: Step 23 [050] (top-down, up-axis -z) and Step 34 [075] (underside, up-axis -y).
- **One `Start` and one `Completed View`.** `Start` is the finished model plus two branding images; `Completed View` is the finished model with nothing else.
- **No text.** Step `description` is empty on 88/88 and there are no popups. Part names are only available as hover tooltips (project flag `tooltips: true`, tooltip title = the part's `Description` metadata, e.g. "Housing Base - Part D1", "12 kOhm Resistor", "Shelf Supports - Parts D11").
- One hidden authoring step exists before `Start` (named "Step 51"); it sets the white background, ambient light and initial visibility.

### 5.2 Granularity

- **Usually one new physical part per numbered step.** Exceptions, each with an evident reason:
  - Identical parts that share one motion go together: 2x D9 in Step 27 [060]; the four D11 posts as 2 + 2 in Steps 32 and 33 [071], [073] (the camera turns 82 deg between the two pairs so each pair's slots face the viewer).
  - Bulk repetition is "show one, then all": Step 37 inserts 1 stem with a lead line, Step 38 shows an eye icon on it and 38c fades in the other 63; the card before says "64x".
  - The two push-button leads are done in one step (Step 19 [041], two labels at once). This is the only wiring step with more than one wire end.
- **Wires: one end of one wire per step.** The 3-wire ribbon takes 6 steps (10-15): three male ends, then three female ends.
- **A part that needs two distinct motions gets two steps or a Transition.** D3 is hooked in (Step 24) and swung shut (Step 25) as two numbered steps with no new part in the second; D10 goes up then sideways within one step, split by an auto Transition [065].
- **Preparation is its own numbered step:** bend resistor legs (4, 7), split ribbon ends (9), remove nut (16).
- **Check-only steps exist** (no new part): Step 34 (look underneath, push posts home), Step 20 (where the cable goes), Steps 23 and 28 (relocate the LED matrix).

### 5.3 Ordering

- Electronics first, on the open base; enclosure afterwards; decorative top last. Within the breadboard: board, Nano, then low passives, then wires.
- Wire order on the breadboard side is white (i2), grey (i3), purple (b19), i.e. the two supply wires before the signal wire. On the matrix side the order is white (V+), purple (the pad the badge calls "V-In"), grey (V-), which follows the physical pad order rather than power-before-signal. So "power before signal" holds for 1 of the 2 passes.
- Each wire is fully identified before it is connected: for the second pass the label names the breadboard hole the wire already sits in.
- Housing order is D2 (carries the button), D4, D3, D5, i.e. the panel with a component first, then around the box; the box is turned on its side for D3 and D5.
- Inside the box and above it the order is strictly bottom-up: D9, matrix + D10, D6, D11, D7, D8, stems.
- Sub-assemblies are built in isolation and brought in afterwards: the push button is mounted on D2 with nothing else on screen (Steps 16-18), then the electronics reappear for wiring (Step 19).

### 5.4 Motion

- **Rigid parts: fade in hovering, tween home in the `c` view.** 19 of the 38 numbered steps do this (2, 3, 5, 6, 8, 17, 18, 22, 24, 25, 26, 27, 29, 31, 32, 33, 35, 36, 37). All moves are a single straight line along the insertion axis except D3 (straight move in 24c, then about 22 deg rotation in 25c) and D10 (two straight legs). Show/hide is `fade`, move is `tween`, 800 ms. The remaining 3 steps are Step 1 and Step 16 (a Transition animates the removal, then the removed piece is hidden) and Step 34 (a 7 mm push).
- **Hover distances** (travel in the `c` view):

| step | part | hover / travel (mm) | direction | lead lines | line length (mm) |
|---|---|---|---|---|---|
| 2 | breadboard onto D1 | 49 | above | 4 | 50 |
| 3 | Nano | 44 | above | 4 | 49 |
| 5 | resistor 1 | 32 | above | 2 | 30 |
| 6 | capacitor | 29 | above | 2 | 28 |
| 8 | resistor 2 | 30 | above | 2 | 35 |
| 17 | button through D2 | 102 | along hole axis | 1 | 106 |
| 18 | nut | 83 | along button axis | 1 | 92 |
| 22 | D4 | 69 | panel normal | 4 | 65-69 |
| 24 | D3 (tilted 22 deg) | 64 away, 46 travel | diagonal | 2 | 42 |
| 25 | D3 swing | rotation + 32 | hinge | 2 | 13-16 |
| 26 | D5 | 42 | panel normal | 4 | 39-43 |
| 27 | D9 x2 | 65 | above | 4 | 65 |
| 29 | D10 | 22 then 40 | up, then sideways | 2 (L-shaped) | 44 |
| 30 | matrix + D10 | (swap) | above | 2 | 56-57 |
| 31 | D6 | 64 | above | 4 | 62-70 |
| 32 | D11 x2 | 89 hover, 82 travel | above | 2 | 44 |
| 33 | D11 x2 | 84-90 hover, 77-83 travel | above | 2 | 37-43 |
| 34 | D11 x4 | last 7 | down | 4 | 17 |
| 35 | D7 | 68 | above | 4 | 49 |
| 36 | D8 | 54 | above | 4 | 59-63 |
| 37 | stem | 44 | above | 1 | 44 |

  Rule of thumb: about 30 mm for two-leg components, 44-49 mm for boards, 42-69 mm for housing panels and shelves, 83-102 mm for parts that travel along a long axis. Range 29-102 mm, median about 64 mm.
- **Exception to "the new part hovers": Step 2.** The new part (base D1) fades in at its seat and the part already on screen (breadboard, which has been floating since Step 1) is the one that hovers and moves.
- **Flexible or re-posed parts are swapped, not animated.** 16 numbered steps resolve by replacing one pre-modelled pose with another in the `c` view: bent legs (4, 7), split ribbon (9), each wire end straight to routed (10-15, 19), cable appearing plugged (20), D2 panel + button + leads seated (21), LED matrix relocated (23, 28, 30), 63 stems appearing (38). For these the `Step N` view has no lead line; it uses a label, badge, eye icon or arrow instead.
- **Arrows mean a free move or a removal, not an insertion.** 4 uses: peel backing (Step 1), take nut off (16), stand D2 on the base (21), carry the matrix across (23). Two are followed by an auto Transition that animates the move (1, 16), two by a pose swap (21, 23).
- The LED matrix has five pose variants and is never tweened between them: floating above the board (Steps 13-15), lying beside the base (19-23), outside panel D4 (23c-28), hovering above the box (28c-30), seated (30c onwards).
- A step can leave a part deliberately short of home: the D11 posts stop 7 mm high in 32c/33c and are pushed through in 34c.

### 5.5 Red lead lines

- **Style: always solid red `#ff0000`, thickness 5, no arrowhead, shown only in `Step N`, removed in `Step Nc`** (57 lines over 21 steps; none in any `c`, card or Transition).
- **Count = number of mating feature pairs that locate the part:** 2 for two-leg components (5, 6, 8), 4 for rectangular plates located at four corners/tabs (2, 3, 22, 26, 31, 35, 36), 1 on the axis for round or single-point parts (button 17, nut 18, stem 37), and per-tab for pairs of small parts (D9 pair: 4; D11 pair: 2; D10: 2). Distribution: 4 lines in 9 steps, 2 lines in 9 steps, 1 line in 3 steps.
- **Endpoints are feature to feature:** resistor/capacitor leg tip to breadboard hole; Nano corner header pin to hole; breadboard bottom corner to corner mark on D1; panel tab tip to the slot it enters (D4, D3, D5, D9, D6, D7, D8); button barrel to hole centre; nut to thread; D11 lower tip to its slot; stem to the LED beneath it.
- **Length is about the hover distance** (within about 20 % in 14 of the 19 tween steps that carry lines). The 5 exceptions: it is shorter when the part slides into or through something, because the line spans only the visible gap between the two features (D11 posts in Steps 32 and 33: about 44 mm line for 82 mm travel; D7 in Step 35: 49 mm for 68 mm); Step 29's L-shaped line is 44 mm for a 62 mm two-leg path; Step 34's lines are 17 mm for a 7 mm push.
- **Direction follows the travel**, a single straight segment. Exception: Step 29's two lines have 3 points each and are L-shaped, drawing the two-leg path (up, then across).
- Lead lines are not used for wire ends (0 of 8 wire-end steps).

### 5.6 Labels, badges, eye icon, insets

- **Breadboard-hole labels**: text is row letter + column number in lower case (`h16`, `h3`, `j3`, `j2`, `a11`, `a19`, `i2`, `i3`, `b19`, `j5`, `j16`); Arial bold black on white, sitting on a cyan `#7fdbff` underline; a cyan leader runs from the end of the underline to a dashed cyan ring on the target. 14 uses in 10 steps, never in a `c` view.
  - For rigid components the ring is on the hole and a red lead line arrives at the same hole (Steps 5, 6, 8).
  - For a wire's male end the label names the target hole but its ring sits on the wire's pin housing (Steps 10, 11, 12, 19).
  - For a wire's female end the label is an identifier: ring on the hole where the wire is already plugged (Steps 13, 14, 15).
  - Placement: two-label steps put one label left (x 26-40 %, y 16-23 %) and one right (x 60-71 %, y 17-33 %) of the model, underline extending outward; single labels sit upper-left (x 29-33 %, y 17-19 %) or opposite the badges.
  - Size: 3em in Steps 5, 6, 8, 10 (7 labels), 2.5em in Steps 11-15 and 19 (7 labels). See anomalies.
- **Disc badges** (Steps 13-15 only): a pair of round images with the same text, cyan-filled disc pointing at the LED-matrix pad and white disc pointing at the wire's free female end ("V+", "V-In", "V-"), each about 6 % of the frame width with a cyan leader and ring.
- **Eye icon**: one black eye glyph, always 7.81 % of the frame width, cyan leader to a dashed ring. 11 uses: identify an isolated part (Steps 4, 7, 9, Mini USB Cable card), orientation/polarity (Step 6, capacitor stripe), "act here" when nothing is hovering (Step 20 socket, Step 23 and 28 matrix, Step 38 stem), "check here" (23c notch, Step 34 tab). Never accompanied by text.
- **Cyan-framed insets** (rounded cyan border, cyan leader to a ring on the model): Step 1 "Protective Backing" (21.7 % wide), Capacitor card polarity photo (30.3 %), 30c wire routing (16.8 %), Step 31 matrix seating (22.2 %), 34c locked tab (14.2 %). The two in `c` views have the eye icon baked into the picture.
- **Quantity label**: "64x", cyan bold 6em, no frame, no leader, beside the single stem on the LED Stems card.
- **Full-frame 2D picture**: the LED Matrix Diagram card shows no 3D part at all, only one image 65 % wide.
- **Title page**: logo SVG top-left (37.6 % wide at 2 %/5 %), title PNG lower-left (42.9 % wide at 2 %/61 %: "Laser Stem Matrix (LSM)", "Full Build", copyright line); model pushed to the right half.

### 5.7 Camera

- **Always: the camera does not move between `Step N` and `Step Nc`** (38/38, including the 3 pairs with a Transition in between).
- **Usually the camera moves on entering a new numbered step** (29 of 38). It stays put when the next step works in the same place: Step 3 (same board), 11 (next hole), 25 (same panel), 36 (next shelf), 38 (same stem), and after a card or camera-only Transition that already moved it (13, 24, 27, 35).
- Every card moves the camera (4/4), as do `Start` and `Completed View`.
- Rotations between steps are large and free: 38 camera moves, median about 65 deg, 11 of them over 80 deg. The author turns the model to face the feature being worked on rather than keeping a home view.
- **Distance tracks the size of what is on screen**: isolated parts 42-221 mm (capacitor 42, resistors 64-75, ribbon 119, button 162, stem 173, cable 221); breadboard work 189-221 mm; board + matrix 189-258 mm; housing 258-350 mm; stems 374 mm. In the saved 2.07:1 frames the content is centred (median centre 49 %/49 %) and spans a median 38 % of the width and 59 % of the height in `c` views.
- **Elevation is a three-quarter view**, 15-55 deg in 78 of 88 steps (median 31). Exceptions: Capacitor card 0 deg (side-on), Step 23/23c 85 deg (top-down), Steps 24-25 with their Transition -35 deg and Step 34/34c -57 deg (from below).
- Framing favours the joint over the whole model: the trailing USB cable is cropped at the frame edge in Steps 30, 30c, 33, 33c and the hovering D11 posts touch the top edge in Steps 32 and 33.
- Camera animation is `tween`, speed 2, orbit animation off; perspective, FOV 45.
- Step-level `transition: fade` (a cut through a fade instead of animating) is set on 13 steps, 12 of which swap the whole scene between an isolated part and the assembly (Steps 1, 4, 5, 7, 8, 9, 10, 16, 20, and the cards LED Matrix Diagram, Mini USB Cable, LED Stems). Not consistent: 5 comparable scene swaps animate instead (Capacitor card, Steps 6, 13, 19, 37) and Step 21 fades without a scene swap.

### 5.8 Look

- White background `#ffffff`, no view-cube content in the renders, matt shading, every part in `toon` style with thin black `normal` edges (2924 of 2925 part overrides); ambient light 2, directional 1. The directional light is repositioned on the turn-over steps.
- Ghosting is used once: Step 34 sets D1 and D5 to 50 % opacity so the tabs behind them are visible, restored at 34c and the following Transition.
- Annotation colours: red `#ff0000` for lead lines and arrows, cyan `#7fdbff` for every 2D leader, underline, ring and frame, black for label text and the eye.

## 6. Part looks (from the renders)

| part | look |
|---|---|
| Laser-cut wood panels D1-D11 | Flat light tan (`#deb887`) with thin black outlines; part id ("D1" ... "D11") engraved in black on the face; slots and tabs drawn as outlines |
| Left panel D2 | Same shape language but its outer face is mid-brown (`#855e42`), inner face tan, so it reads as the "front" with the button |
| Breadboard | White/off-white block, dense grid of small black-outlined holes, red and blue rail stripes, tiny black row letters and column numbers |
| Protective backing | Plain light-grey sheet |
| Arduino Nano | Navy-blue PCB, silver header pins, gold-tan 2x3 header, white/silver mini-USB socket, black chip |
| Resistors | Bright blue body (`#0074d9`) with colour bands (12 kOhm: brown/red/black/red/brown; 330 Ohm: orange/orange/black/black/brown), silver legs; no black outline on the isolated views |
| Capacitor | Black can with a grey stripe, silver legs |
| Jumper ribbon | Three wires white, light grey, purple (`#4e008e`); black Dupont housings with silver pins; drawn as smooth tubes with outline |
| Push button | Black body and cap, light-grey/white hex nut, one red and one black lead ending in black Dupont pins |
| 8x8 LED matrix | Black PCB, 64 white/grey square LEDs, three header pins at one corner; back side shown only as a 2D diagram |
| Mini-USB cable | Black cable and plug housings, silver metal ends, white insert in the USB-A plug |
| LED stems | White square rods with a thin grey outline (colour override `#ffffff`) |
| Lead lines / arrows | Solid red; arrows are thick straight 3D arrows (body 5, head 20 x 15 in 3 of 4) |
| Labels | Black bold Arial on a cyan underline; cyan leader ending in a dashed cyan ring |
| Eye icon | Solid black eye glyph, cyan leader and ring |
| Insets | Picture inside a rounded cyan frame on white |

## 7. Anomalies and inconsistencies

1. **Step 19 [041] labels are swapped.** "j5" points at the black lead and "j16" at the red lead, but 19c [042] shows the black lead plugged at column 16 and the red at column 5. Part 2's equivalent step labels them the other way round (j16 on the black lead), matching its result. Electrically harmless for a push button, but the two views of the same step disagree.
2. **Badge text "V-In"** in Step 14 [030] for the matrix data-input pad. The other two badges are "V+" and "V-", and Part 2's step text calls this pad "the IN pin". Looks like a typo for "In".
3. **Step 3 [006] has no hole label.** Every other breadboard insertion names its holes. Part 1's version of this step carried two labels ("Pin d12", "c16"); they were dropped, leaving four lead lines as the only locator for the Nano.
4. **Mixed label sizes**: 3em (Steps 5, 6, 8, 10) versus 2.5em (Steps 11-15, 19); "i2" in Step 10 is visibly larger than "i3" in Step 11 at the same camera.
5. **Line-style data not reflected in renders**: the 8 lead lines of Steps 35 and 36 are stored as `dashed` but render solid in the saved frames; all other shown lines are `solid`.
6. **Stale lead-line data**: Step 26 [057] has two lines stored as 133 mm long (they render at about 40 mm like their neighbours) and only 4 lines where Part 3 had 6; Step 31 [069] has one line anchored to an object id that no longer exists.
7. **Unused leftovers in the project**: hidden step "Step 51"; a second quantity label "64X" (capital X) never shown; 20 lead lines (one `dotted`), 2 arrows and 12 images never shown.
8. **Stored image positions contradict the renders** for Step 6's eye icon and Step 34/34c (see section 2).
9. **Arrow inconsistency**: Step 23's arrow is thinner (body 3, head 9 x 10) than the other three (5, 20 x 15); Step 21's arrow is authored with `head_position: start`.
10. **Unannounced pose change**: the LED matrix floats above the board through 15c [033] and is lying beside the base when the assembly returns in Step 19 [041]; no step tells the student to put it down.
11. **Tooltip text problems**: "Laster Stem Matrix (LSM) - Part 1" (typo, and a guide title used as a part name) on 58 Nano solids and one USB-plug solid; "Mini-USB Cable" versus "Mini USB Cable"; "Push Button" versus "Black Push Button"; "Breadboard Wires" versus "Breadboard Wires (M-F)"; the backing sheet is described as "Breadboard"; three routed wires and two D2 solids have no description.
12. **Stray geometry** (not noticeable in the renders): the backing sheet becomes visible again at 28c and stays to the end inside the housing; two solids of the USB plug are visible from Step 13 to Step 19 before the cable is introduced; two loose-lead pin housings reappear at Completed View; Step 38 nudges the Nano 2.3 mm and leaves 58 of its solids displaced 44 mm inside the closed box.
13. **`transition: fade` applied inconsistently** (section 5.7).
14. Kit-level naming slips seen while comparing (not in this guide): Part 2 ends with "Completed Build" instead of "Completed View"; Part 4 numbers one pair "Step 8" / "Step 9c" and so ends at Step 13 with 12 steps; the 3+4 guide ends with "Copmleted View"; the 1+2 guide has "Step 20C".

## 8. Relation to LSM Parts 1-4 played back to back

**Counts.** Parts 1 + 2 + 3 + 4 = 19 + 31 + 13 + 29 = 92 viewer steps. Full build = 88 = 92 - 3 Start pages - 3 Completed views + 2 new Transitions.

| | Part 1 | Part 2 | Part 3 | Part 4 | sum | Full build |
|---|---|---|---|---|---|---|
| Start | 1 | 1 | 1 | 1 | 4 | 1 |
| numbered pairs | 8 | 13 | 5 | 12 | 38 | 38 |
| cards | 1 | 2 | 0 | 1 | 4 | 4 |
| Transition | 0 | 1 | 1 | 2 | 4 | 6 |
| Completed | 1 | 1 | 1 | 1 | 4 | 1 |

**Start and Completed views.** All four part Start pages are dropped and replaced by one new Start [000]: same logo, a new title image with the subtitle "Full Build", the finished model (as on Part 4's Start) with the camera pulled back from 321 to 374 mm. The Completed views of Parts 1, 2 ("Completed Build") and 3 are dropped. The final Completed View [087] is identical to Part 4's (same camera 321 mm / 39 / 44, same part state).

**Renumbering.**

| Part steps | Full build steps | viewer index |
|---|---|---|
| Part 1: 1-8 (+ Capacitor card) | 1-8 (unchanged numbers) | 001-018 |
| Part 2: 1-11 (+ LED Matrix Diagram card) | 9-19 (+8) | 019-042 |
| Part 2: Mini USB Cable card, Step 13 | card, Step 20 | 043-045 |
| Part 2: Step 12 | Step 21 | 046-047 |
| Part 3: 1-5 | 22-26 (+21) | 048-058 |
| Part 4: 1-7 | 27-33 (+26) | 060-074 |
| Part 4: "Step 8" / "Step 9c" | Step 34 / 34c | 075-076 |
| Part 4: 10-13 (+ LED Stems card) | 35-38 (+25) | 077-086 |

No numbered step was added or removed. Part 4's numbering slip (a pair named "Step 8" and "Step 9c") is repaired by the renumbering.

**The one reordering.** Part 2 ends: Step 12 (stand D2 panel on the base; arrow + eye icon), card Mini USB Cable, Step 13 (plug the cable in, D2 already standing). The full build does the cable first (card, Step 20) and the panel second (Step 21, arrow only, eye icon removed). This matches the combined guides: the 3+4 guide begins with the D2-panel step as its Step 1, and the full build's tail [046]-[087] is that guide's 42 content steps in one-to-one order.

**Seams.**
- Part 1 to Part 2: [018] Step 8c goes straight to [019] Step 9 (isolated ribbon) with a fade cut. No bridging step.
- Part 2 to Part 3: [047] Step 21c goes straight to [048] Step 22 with a 57 deg camera move. No bridging step, but this is where the reordering sits.
- Part 3 to Part 4: a new camera-only Transition [059] replaces Part 3's Completed View, Part 4's Start and the camera move Part 4's Step 1 used to make itself; it lands exactly on Part 4 Step 1's pose (300 mm / 31 / -165), so Step 27 [060] starts with the camera at rest. The 3+4 combined guide has the same Transition.
- The other new Transition is [002] inside Step 1 (backing sheet now tweens away and is hidden in 1c; in Part 1 it simply sat 48 mm below the board in 1c).

**Changed content, Part 1 region (re-shot).** 0 of 17 mapped steps keep their camera pose; 12 of 17 are pulled back by the same factor 1.16 (190 to 221 mm, 163 to 189 mm). Hover offsets changed (breadboard 39 to 49 mm, Nano 35 to 44 mm, resistor 1 37 to 32 mm, capacitor 33 to 29 mm). Step 3 lost its two labels. Dashed lead lines (resistor legs, one Nano line) became solid. Labels grew from 2.5em to 3em. Eye icons normalised to 7.81 % (were 6.3-9.4 %). Capacitor card re-shot closer and exactly side-on from the other side (60 mm / 5 / -100 to 42 mm / 0 / 90), without Part 1's temporary FOV 50. Nano and breadboard CAD models replaced.

**Changed content, Part 2 region (re-shot).** 0 of 29 mapped steps keep their camera pose; 17 of 29 use the same 1.16 pull-back. Step 9 shows one ribbon with one eye icon (Part 2: two eye icons, one per end). Male-end labels re-anchored from the ribbon to the individual pin housing; female-end labels re-anchored from the wire cap to the breadboard hole; the badges of Steps 13 and 14 shrunk from 7.8 % to about 6 % (Step 15's were already 6 %). The camera move for the matrix view moved from Step 13 onto the LED Matrix Diagram card. Button model replaced; Step 18's lead line dashed to solid; Step 18c shortened from 1600 to 800 ms. Step 19 label texts swapped (anomaly 1). Order of cable and panel swapped as above.

**Changed content, Part 3 region (reused).** 4 of 11 camera poses identical, the rest differ only in distance (350 to 300 mm at Step 23) or elevation (-48 to -35 for the underside block). Step 26 has 4 lead lines instead of 6. The 23c eye icon is re-anchored from a wire to the D4 panel.

**Changed content, Part 4 region (reused).** 21 of 28 camera poses identical, the others within 2 deg elevation and 12 deg azimuth. Hover offsets trimmed slightly (D9 68 to 65 mm, stem 50 to 44 mm). Step 31 gains the matrix-seating inset (already present in the 3+4 guide). Quantity label "64X" replaced by "64x".

**Text.** Parts 1 and 2 (and the 1+2 guide) carry step description text on many steps, with its own numbering and several typos ("Remove the srew attached to the Push Buttoim", "Ste[ 15"). The full build carries none.

**Implication for an in-house player.** A full build can be generated from part guides by: dropping every inner Start/Completed, keeping one title and one final view, renumbering continuously, and inserting an auto-advancing camera Transition at any seam where the next part starts from a different camera pose. Per-part camera distances cannot be assumed to carry over unchanged (the first half here was uniformly re-scaled by 1.16).
