# Guide report: `19075-lcd_alarm_clock_lac_-_part_2` — LCD Alarm Clock (LAC) - Part 2

Kit: LAC. Role: part (2 of 4). 43 authored steps, 42 shown in the viewer (1 hidden set-up step folded into Start): 39 `pause`, 3 `play`.
Sources read: `digest/19075-lcd_alarm_clock_lac_-_part_2.md` + `.json` (all of it), all 6 contact sheets, all 42 thumbs (000-041), targeted queries on `cadasio_raw/19075-lcd_alarm_clock_lac_-_part_2.json`.
Working scripts and enlarged crops are in `reports/_work_lac_p2/` (`trackC.py` = my own visibility/motion tracker, `tb2.py` = annotation dump, `cam.py`, `bbox.py`, crops `c002/c006/c012/c026/c035/c037.png`).

Index convention: `[NNN]` = viewer step index as in the digest and thumbs.

## 1. Summary

Part 2 starts from the finished Part 1 board (bottom panel F3 with breadboard, Nano, real-time-clock module, two resistors and six jumpers) and adds the two front-of-house controls, each mounted in its own wood panel and then wired back to the breadboard. The student (a) drops the pre-wired 3-position rocker switch into the cut-out of top panel F4 and plugs its three leads into `j27`, the red (+) rail and `j29` (Steps 1-4); (b) peels an orange/yellow jumper pair apart and bridges `j1`-`i27` and `j3`-`i29` (Steps 5-7); (c) strips the knob, nut and washer off the pre-wired potentiometer (Steps 8-10), pushes it through front panel F1 from behind, refits washer, nut and knob and turns the knob to its stop (Steps 11-15); (d) plugs the pot's three leads into the red (+) rail, `a5` and the blue (-) rail (Steps 16-18). The guide is 18 numbered steps, each a strict "Step N" (annotated hover/intent view) + "Step Nc" (clean completed view) pair, wrapped in a title page, one section card and a Completed View; the three removal steps insert an auto-advancing "Transition" between N and Nc. There is no instructional text anywhere (0 of 42 steps have a description or popup): everything is said with one red lead line or arrow, one black eye icon, and cyan-underlined breadboard-hole labels. Steps [002]-[040] are content-identical to Full Build steps [032]-[070] ("Step 15"-"Step 32c"), renumbered 1-18.

Quantities at a glance

| item | count |
|---|---|
| viewer steps | 42 = 1 Start + 1 section card + 18 `Step N` + 18 `Step Nc` + 3 Transition + 1 Completed View |
| step duration | 800 ms on 42/42 (tween for moves, fade for show/hide, camera tween speed 2) |
| camera moves | 11 of 42 steps ([000] [001] [002] [004] [010] [012] [016] [025] [033] [035] [041]); 0 of 18 on `Nc`, 0 of 3 on Transition |
| red lead lines shown | 5 (Steps 1, 11, 12, 13, 14) - one each |
| red arrows shown | 3 (Steps 8, 9, 10) - one each |
| eye icons shown | 10 (Steps 2, 3, 4, 5, 6, 7, 15, 16, 17, 18) - one each |
| text labels shown | 10 over 8 wiring steps (`j27`, `(+) red`, `j29`, `j1`, `i27`, `j3`, `i29`, `(+) red`, `a5`, `(-) blue`) |
| other images | 2 on the title page (logo, title block), 1 detail inset (Step 11c) |
| steps with any text description / popup | 0 |

## 2. Step table (every viewer step)

Camera column = orbit distance mm / elevation / azimuth after entering the step; "same" = camera did not move. (For [016]-[024] the 513 mm figure is the distance to an orbit target that is not on the part, so it does not indicate zoom; judge framing from the thumbs.) Screen positions are the annotation's top-left corner in % of viewport (x, y). Part counts use leaf-level visibility (see section 6, data caveat 1).

| idx | name | kind | what is added or done | annotations on screen | camera |
|---|---|---|---|---|---|
| 000 | Start | title page | Finished Part 2 state at right: F3 + breadboard build in the middle, F4 with switch upper right, F1 with pot upper left, all six leads and both jumpers routed (51 scene parts) | 2 unanchored images: TechBox logo SVG top-left (w 38.9 %, at 2,6 %); title block PNG bottom-left (w 42.1 %, at 2,64 %): "LCD Alarm Clock (LAC) / Part 2 / (c) 2025 TechBox..." | moves: 439 / 35 / 141 |
| 001 | Rocker Switch | section card (3D part, no text) | Everything else fades out (50 parts). Rocker switch alone with its three pre-attached straight leads (black, tan, red), each ending in a black Dupont pin housing. Switch rises 81 mm from its title-page pose while the rest fades | none | moves: 175 / 44 / 137 (zoom x2.5) |
| 002 | Step 1 | hover (mechanical insert) | Top panel F4 fades in underneath, engraved side up, already in place. Switch + leads hover 81.2 mm straight above the rectangular cut-out | 1 red lead line, 69.5 mm, vertical: switch body (on its centre axis) -> centre of F4 cut-out | moves: 277 / 17 / 137 (pull back x0.63, tilt down 28 deg to a low side view) |
| 003 | Step 1c | completed | Switch + 3 leads + 3 pin housings tween 81.2 mm straight down as one rigid unit; rocker sits flush, leads hang straight below the panel | none | same |
| 004 | Step 2 | hover (wiring) | Part 1 assembly fades in beside F4 (27 parts: F3, breadboard, Nano, RTC module, 2 resistors, 6 jumpers). Nothing moves; the three leads still hang straight | eye icon (68,52 %) -> pin housing of the red lead; label `j27` (23,37 %) -> breadboard hole | moves: 277 / 24 / -158 (orbit 61 deg to the far side) |
| 005 | Step 2c | completed | Straight red lead + its pin fade out; routed red wire (switch terminal -> j27) + seated pin fade in. No tween | none | same |
| 006 | Step 3 | hover (wiring) | nothing changes in 3D | eye (66,53 %) -> pin of the tan lead; label `(+) red` (22,42 %) -> a hole on the red (+) rail | same |
| 007 | Step 3c | completed | Tan lead swapped for routed tan wire seated in the (+) rail | none | same |
| 008 | Step 4 | hover (wiring) | nothing changes in 3D | eye (64,52 %) -> pin of the black lead; label `j29` (24,39 %) -> hole | same |
| 009 | Step 4c | completed | Black lead swapped for routed black wire seated in j29 | none | same |
| 010 | Step 5 | hover (prep / look) | Everything hidden (35 parts). An orange + yellow male-male jumper pair fades in, joined side by side, two pins at each end | eye (57,17 %) -> the seam between the two wires at mid-length | moves: 175 / 57 / 134 (zoom x1.6) |
| 011 | Step 5c | completed | The two wires slide apart sideways (orange +10.7 mm, yellow -9.2 mm; about 20 mm gap) | none | same |
| 012 | Step 6 | hover (wiring) | Board assembly returns (35 parts; F4 is out of frame, its three routed leads enter from the top edge). Yellow wire hidden. Orange wire slides 150 mm from where the pair was shown to a parking spot on the table beside the base (about one breadboard length from the board, judged from the thumb), still straight | eye (72,39 %) -> middle of the orange wire; labels `j1` (27,32 %) and `i27` (36,17 %) -> the two holes | moves: 277 / 57 / 55 (high view onto the breadboard) |
| 013 | Step 6c | completed | Straight orange wire + 2 pins fade out; routed orange wire j1 <-> i27 + 2 seated pins fade in | none | same |
| 014 | Step 7 | hover (wiring) | Yellow straight wire fades in at the same parking spot beside the base | eye (70,44 %) -> middle of the yellow wire; labels `j3` (26,30 %) and `i29` (37,16 %) | same |
| 015 | Step 7c | completed | Yellow wire swapped for routed wire j3 <-> i29 | none | same |
| 016 | Step 8 | hover (removal; doubles as the part intro) | Everything hidden (41 parts). Potentiometer alone as supplied: brown body, 3 pre-attached leads (black, tan, red), washer, nut and black knob fitted. Scene up-axis switches to -x so the leads hang "down" on screen | 1 fat red arrow, 41.8 mm, from the pot body outward along the shaft, drawn over the knob | moves: 513 / -28 / -45 |
| 017 | Transition | auto-advance (play, 800 ms, nav overlay hidden) | Knob slides 37.6 mm off the shaft, no spin; arrow fades | none | same |
| 018 | Step 8c | completed | Knob fades out (set aside) | none | same |
| 019 | Step 9 | hover (removal) | nothing changes in 3D | 1 red arrow, 41.3 mm, same axis and direction, thinner (scale 0.30 vs 0.52) | same |
| 020 | Transition | auto-advance | Nut slides 37.9 mm off the shaft while spinning 176 deg | none | same |
| 021 | Step 9c | completed | Nut fades out | none | same |
| 022 | Step 10 | hover (removal) | nothing changes in 3D | 1 red arrow, 32.6 mm, smallest head (15 x 10) | same |
| 023 | Ttansition (sic) | auto-advance | Washer slides 37.9 mm off the shaft while turning 124 deg | none | same |
| 024 | Step 10c | completed | Washer fades out; bare pot with threaded bushing and 3 leads | none | same |
| 025 | Step 11 | hover (mechanical insert) | Front panel F1 fades in in place, engraved face to camera. Pot + leads back off 79 mm behind the panel on the shaft axis | 1 red lead line, 91.7 mm: pot (on the shaft axis) -> centre of the F1 hole; hidden where it passes behind the panel | moves: 439 / -32 / -40 (5.5 deg, target shift 178 mm) |
| 026 | Step 11c | completed + detail inset | Pot + 3 leads + 3 pins tween 79 mm; shaft now pokes through the front face | 1 inset picture (w 17.7 %, at 19,19 %; cyan rounded border) with cyan leader + ring to the small slot beside the hole: flat front view of the shaft with the pot's locating tab sitting in the slot, tab boxed in red | same |
| 027 | Step 12 | hover (mechanical insert) | Inset removed. Washer fades in 61.3 mm out in front of the panel on the shaft axis | 1 red lead line, 75.4 mm: washer centre -> pot | same |
| 028 | Step 12c | completed | Washer tweens 61.3 mm along the shaft to the panel face | none | same |
| 029 | Step 13 | hover (mechanical insert) | Nut fades in 55.9 mm out | 1 red lead line, 66.7 mm: nut centre -> pot | same |
| 030 | Step 13c | completed | Nut tweens 55.9 mm onto the thread (no spin); washer nudges 0.4 mm | none | same |
| 031 | Step 14 | hover (mechanical insert) | Knob fades in 60.5 mm out | 1 red lead line, 76.5 mm: knob centre -> pot | same |
| 032 | Step 14c | completed | Knob tweens 60.5 mm onto the shaft | none | same |
| 033 | Step 15 | hover (look / adjust) | nothing changes in 3D | eye (28,34 %) -> the knob's pointer mark (at 9 o'clock) | moves: 125 / -82 / -83 (face-on close-up, zoom x3.5) |
| 034 | Step 15c | completed | Knob rotates about 50 deg counter-clockwise in place (pointer to about 7:30) | none | same |
| 035 | Step 16 | hover (wiring) | Whole build returns (41 parts): F3 board, F4 with switch, and F1 now seen lying flat with the pot body up and its three straight leads pointing off to the left. Up-axis back to +y. Washer silently hidden | eye (13,13 %) -> pin of the red pot lead; label `(+) red` (38,42 %) -> hole on the red (+) rail | moves: 439 / 35 / 120 (orbit 132 deg, zoom x0.29) |
| 036 | Step 16c | completed | Red lead swapped for routed red wire seated in the (+) rail | none | same |
| 037 | Step 17 | hover (wiring) | nothing changes in 3D | eye (14,11 %) -> pin of the tan lead; label `a5` (36,42 %) | same |
| 038 | Step 17c | completed | Tan lead swapped for routed tan wire seated in a5 | none | same |
| 039 | Step 18 | hover (wiring) | nothing changes in 3D | eye (14,10 %) -> pin of the black lead; label `(-) blue` (36,44 %) -> hole on the blue (-) rail | same |
| 040 | Step 18c | completed | Black lead swapped for routed black wire seated in the (-) rail | none | same |
| 041 | Completed View | final view | nothing changes in 3D; no annotations | none | moves: 439 / 32 / 127 (7 deg orbit, 40 mm shift, same distance) |

## 3. Conventions found (with evidence and exceptions)

### 3.1 Structure

- **S1. Fixed skeleton.** Start -> (section card) -> `Step N` / `Step Nc` pairs -> Completed View. All 18 numbered steps have both halves, in order, with lower-case `c` (18/18). Numbering restarts at 1 for the part; the Full Build shows the same content as Steps 15-32.
- **S2. Title page.** [000]: logo top-left, title block bottom-left, both unanchored 2D images at x = 2 %; the 3D model of this part's *finished* state fills the right-hand side. Same two image slots (w 38.9 % at 2,6 % and w 42.07 % at 2,64 %) are used by LAC Parts 1, 3 and 4.
- **S3. Two beats per action.** `Step N` = "here is what to pick up and where it goes" (annotated, nothing seated yet); `Step Nc` = result, annotations gone. 18/18 `Step N` carry at least one annotation; 17/18 `Step Nc` carry none. Exception: Step 11c [026] carries the detail inset.
- **S4. Section card = the new component alone.** [001] "Rocker Switch": 3D model in isolation, close camera, no annotations, no text; the step name is the only label. Exception / inconsistency: only 1 of the 3 new component kinds gets a card. The potentiometer's "alone on screen" view is merged into Step 8 [016] and the jumper pair's into Step 5 [010].
- **S5. No prose.** `description` is empty and `popup` is null on 42/42 steps. Part names exist only as hover tooltips (project `tooltips: true`, tooltip = the part's `Description`: "3-Position Rocker Switch", "Top Side - Part F4", "Front Side - Part F1", "Bottom Side - Part F3", "Potentiometer", "Breadboard Wires (M-M)", "Nano Board", "Real Time Clock"...) and as the engraved `F1`/`F3`/`F4` on the panels.
- **S6. Three-beat removal.** For "take this off": `Step N` (arrow, pause) -> `Transition` (play, 800 ms, part slides off, arrow fades, `overlayVisible: false`) -> `Step Nc` (pause, part fades out). 3/3 removals (Steps 8, 9, 10). In this guide a Transition is never a camera move (0/3) - it is the first half of a two-stage part animation.

### 3.2 Granularity

- **G1. One action per numbered step.** 18 steps = 8 wire connections (2, 3, 4, 6, 7, 16, 17, 18) + 2 component mounts (1, 11) + 3 removals (8, 9, 10) + 3 hardware fits (12, 13, 14) + 1 prep (5) + 1 adjust (15). Washer, nut and knob each get their own step both coming off and going on.
- **G2. Pre-wired components move as one rigid unit.** Switch + 3 leads + 3 pin housings (7 scene parts) in Step 1; pot + 3 leads + 3 pin housings (7 scene parts) in Step 11.
- **G3. Attached leads: one free end per step, one label.** Loose male-male jumper: the whole wire (both ends) in one step, two labels (Steps 6, 7). Never two different wires connected in one step. Only multi-part step: Step 5 shows two wires together because the action is separating them.

### 3.3 Ordering

- **O1. Per component: (strip) -> mount in its wood panel -> wire its leads.** Switch: Step 1 mount, Steps 2-4 leads. Pot: Steps 8-10 strip, 11-14 mount and hardware, 15 set, 16-18 leads. Wiring always comes after the mechanical mount.
- **O2. Lead order is red -> tan -> black on both 3-lead components (2/2).** It is not "power first": switch = `j27`, (+) rail, `j29`; pot = (+) rail, `a5`, (-) rail.
- **O3. Hardware comes off outside-in (knob, nut, washer) and goes back in exact reverse (washer, nut, knob).**
- **O4. Jumpers in ascending column order** (`j1`/`i27` then `j3`/`i29`), after the pair has been split.
- **O5. The whole part runs component by component, not panel by panel**: switch block ([001]-[009]), jumper block ([010]-[015]), pot block ([016]-[040]).

### 3.4 Motion

- **M1. Mechanical parts appear at a hover pose on the insertion axis and tween straight to the seat on `Nc`.** Hover distances: 81.2 (switch), 79.0 (pot), 61.3 (washer), 55.9 (nut), 60.5 mm (knob); range 56-81 mm, mean 68 mm. No rotation during insertion on 5/5 (the nut does not spin on the way in).
- **M2. Hover direction = the real insertion direction.** Switch from directly above the panel; pot from behind the panel; washer/nut/knob from in front along the shaft.
- **M3. New parts fade in at the hover pose; they do not fly in.** The author parks the still-hidden part at its hover pose one step early: washer positioned at [026], shown at [027]; nut [028] -> [029]; knob [030] -> [031]; knob/nut/washer [015] -> [016]. Exceptions: the switch tweens 81 mm up on entering [001] (it was visible on the title page), and the pot backs off 79 mm on entering [025] (it had been displayed at its seat in empty space during Steps 8-10).
- **M4. Wires never tween.** On every wiring `Nc` (8/8) the straight wire model and its pin housing(s) fade out and a separate routed model fades in at the seat. The straight wire is never held over its hole: attached leads stay hanging from the component; loose jumpers lie straight on the table beside the base, roughly one breadboard length away from the board (estimated from thumbs [012] and [014]). Nothing on screen joins the wire end to its hole: the student pairs the eye (source) with the label (destination), which sit 21-45 % of the frame width apart.
- **M5. Removal motion.** Part travels 37.6-37.9 mm off along the axis in the Transition; nut spins 176 deg and washer 124 deg, knob does not rotate; then fades out on `Nc`.
- **M6. In-place adjustment** uses the same pair: eye on `N`, rotation on `Nc` (Step 15: about 50 deg) or a small slide (Step 5: about 20 mm apart).
- **M7. Uniform timing.** 800 ms, tween, fade in/out on every step; backwards navigation is animated too (`animatePreviousStep: true`).

### 3.5 Red lead lines

- **L1. Exactly one per mechanical insertion (5/5), none on wiring steps (0/8) and none on removals (0/3).** Solid `#ff0000`, thin constant screen width (line `scale` 5, `world_units: false`), 2 points, collinear with the motion axis.
- **L2. Endpoints.** From a point on the moving part's own centre axis (a point on the switch body; a point on the pot body behind the bushing; the centre of washer / nut / knob) to the mating feature on the stationary part (centre of the F4 cut-out; centre of the F1 hole; a point on the pot's axis just behind the panel for the three hardware parts). Not pin-to-hole pairs, not one line per lead.
- **L3. Length is close to but not equal to the hover distance**: 69.5 vs 81.2 (0.86x), 91.7 vs 79.1 (1.16x), 75.4 vs 61.3 (1.23x), 66.7 vs 55.9 (1.19x), 76.5 vs 60.5 (1.26x). The difference (-12 to +16 mm) is the distance left between the two anchor points once seated.
- **L4. The line is attached at both ends**, so it shortens as the part travels and fades out over the same 800 ms (raw points for the washer line go from 75.4 mm at [027] to 13.5 mm at [028]).
- **L5. The line is a real 3D object and is depth-tested.** In [025] it disappears behind the panel between the panel edge and the hole and shows again inside the hole; in [002] its upper part is hidden behind the middle lead.

### 3.6 Arrows

- **A1. Red solid 3D arrows are used only for removal (3/3)** and never for insertion. One arrow, tail at the pot body, pointing outward along the shaft, drawn over the part to be removed. Length 32.6-41.8 mm against a 38 mm removal travel.
- Exception / inconsistency: the three arrows are styled differently (scale 0.52 / 0.30 / 0.29, body 5 / 6 / 5, head 20x17 / 24x22 / 15x10), so they look fat, medium and small for the same action.

### 3.7 Labels

- **T1. One label per breadboard hole to be used.** Text is the hole coordinate, lower-case row letter + column number (`j27`, `i29`, `a5`), or `(+) red` / `(-) blue` for a power rail (the colour word names the rail stripe, not the wire).
- **T2. One style on 10/10.** Bold black Arial at 3 em, no box, cyan `#7fdbff` underline (thickness 5) that continues as a cyan leader to a cyan ring ("Life Saver Circle", 30 px) sitting on the hole. Box 175 px wide for coordinates, 200-217 px for rail labels.
- **T3. Placement.** Label always up-left of its hole (target is 10.8-18.7 % of viewport to the right and 12.6-19.1 % below the label's top-left corner; mean 15 % / 15 %). Labels sit in clear space at x 21-38 %, y 16-44 %. With two labels they are stacked diagonally and their leaders do not cross.
- **T4. Labels point at the destination only.** The source end is marked by the eye icon, not by text.

### 3.8 Eye icon

- **E1. A black eye pictogram marks "this is the thing to pick up / look at".** Exactly one on each wiring step (8/8) and on the two look/adjust steps (5, 15); 0 on the 5 insertions and 3 removals; never on `Nc`.
- **E2. Anchor.** The free pin housing of the lead to plug next (6: Steps 2, 3, 4, 16, 17, 18), the middle of the loose jumper (2: Steps 6, 7), the seam of the wire pair (Step 5), the knob's pointer mark (Step 15).
- **E3. Style.** Width 7.8-7.9 % of the viewport, cyan leader + cyan ring exactly like the labels, placed 8-27 % away from its target in empty space on the side away from the labels (right of the leads in Steps 2-7, upper left in Steps 15-18).

### 3.9 Images

- **I1. Detail inset for an alignment that the 3D view cannot show.** Step 11c [026]: a flat rendered close-up on a wood-coloured field, cyan rounded-rectangle border (thickness 5), cyan leader + ring to the feature; the critical feature (locating tab in its slot) is boxed in red inside the picture. Only instance; it is the only annotation on any `Nc` step and it is cleared on the next step.

### 3.10 Camera

- **C1. One camera per work area; it stays frozen while the student works there.** 11 moves in 42 steps. Runs without a move: [004]-[009] (6 steps), [012]-[015] (4), [016]-[024] (9), [025]-[032] (8), [035]-[040] (6).
- **C2. The camera only moves on entering a hover step, a card, the title or the Completed View.** Never on `Nc` (0/18) and never on a Transition (0/3), so every seat/swap/removal animation is watched from a still camera.
- **C3. Angle is chosen for the action.** Low side view (elevation 17 deg) for the vertical drop of the switch; 24 deg from the far side so the hanging leads and row j are both visible; 57 deg looking down for breadboard jumpers; face-on (82 deg off the panel plane) close-up for the knob setting; 35 deg overview for the long pot leads.
- **C4. Framing.** Content is horizontally centred (bounding-box centre x 40-56 % on 40/42 thumbs) and sits slightly high; the bottom 12-37 % of the frame is left empty on 40/42 (navigation bar is `horizontal_bottom`). Isolated parts and single-panel views take 14-43 % of frame width, multi-panel assembly views 43-73 %. Exceptions: [012]-[015] crop the switch leads at the top edge (F4 is out of frame); [033]-[034] deliberately crop the panel at the left and bottom edges.
- **C5. View-up trick.** For the whole pot block [016]-[034] the scene `up_axis` is switched from `+y` to `-x` (and the camera goes to negative elevation) so that the front panel, which lies face-down in the flat layout, reads as an upright panel with the leads hanging down. Restored to `+y` at Step 16 [035].
- **C6. Completed View is a small settle, not a fly-around**: 7 deg orbit and 40 mm target shift at unchanged distance from the last step's view.

### 3.11 Look and colour language

- **K1.** White `#ffffff` background, no ground or shadow; flat toon shading (`toon` on 1590 solids); thin black edge lines (width 1, 40 deg edge angle), no silhouette outline; perspective camera, 45 deg FOV.
- **K2. Three annotation colours with fixed meanings.** Red `#ff0000` = motion and "critical" (lead lines, arrows, the red box in the inset). Cyan `#7fdbff` = pointing (label underline, all leaders, rings, inset border). Black = text and the eye.

### 3.12 Other

- **X1. Context isolation.** While a component is introduced, stripped or mounted in its panel, everything unrelated is hidden (50 parts hidden at [001], 35 at [010], 41 at [016]); the whole build fades back in on the first wiring step of that component (27 parts at [004], 35 at [012], 41 at [035]), together with the camera move.
- **X2. Unfolded layout.** The panels are never assembled to each other in this part: F3 lies flat with the breadboard, F4 floats in mid-air to one side with the switch leads hanging beneath it, F1 lies flat to the other side. Only wires join them.

## 4. Part looks (from the renders)

| part | look |
|---|---|
| Background / scene | pure white, no floor, no shadows |
| Edges | thin black lines on every part |
| Wood panels F1, F3, F4 | flat light tan (`#deb887`, renders as pale peach), slightly darker cut edges, black engraved part number (`F1`, `F3`, `F4`); slots and cut-outs show the white background |
| Breadboard | white body, black square holes, black printed row letters and column numbers, thin red and blue rail stripes |
| Arduino Nano | dark navy PCB, silver pins and pads, black IC, silver mini-USB socket, 2x3 silver header |
| RTC module (HW-84) | bright mid-blue PCB standing upright, black ICs, grey/black coin-cell holder with a silver CR2025 cell |
| Resistors | blue ribbed body, bare silver legs |
| Jumper / lead wires | saturated flat colours with black outline: red `#ef3340`, black `#2d2926`, tan `#b28362`, orange `#ff851b`, yellow `#eac80d`, green `#10cc62`, blue `#0074d9`, purple `#611b6c`, white/light grey `#cad1ed`, dark red `#800000` |
| Dupont pin housings (Wire Cap V2) | black `#1e1616` rectangular sleeve with a silver `#a6a9aa` pin; a tiny square in the wire's colour shows on the sleeve in close-up |
| Rocker switch | all-black body and rocker, white `I O II` markings, three black sleeved terminals underneath, leads black / tan / red |
| Potentiometer | brown `#855e42` round body, silver threaded bushing and splined slotted shaft, small brown lug plate, leads black / tan / red |
| Knob | black ribbed cylinder with a silver ring at the face edge and a short white pointer line |
| Nut / washer | flat silver-grey `#a6a9aa` |
| Lead lines / arrows | pure red `#ff0000`; lines hair-thin, arrows fat and flat |
| Labels | bold black Arial on nothing, cyan underline + leader + ring |
| Eye icon | solid black almond eye with white iris ring and highlight |
| Inset | wood-coloured field, grey part, red square, cyan rounded border |

## 5. Anomalies and inconsistencies

1. **Typo:** [023] is named `Ttansition` (the same typo is in Full Build [053]).
2. **Section cards are uneven:** the rocker switch has a card ([001]); the potentiometer and the jumper pair do not.
3. **Arrow styling differs across the three removal steps** (see A1).
4. **Tiny style drift:** eye icon width 7.92 on [004] and [010] vs 7.81 elsewhere; eye leader thickness 4 on [008] vs 5 elsewhere.
5. **`(+) red` is ambiguous as a label:** on Step 3 it is the *tan* lead that goes to "(+) red", on Step 16 it is the *red* lead. The word names the rail stripe. The ring marks one specific rail hole although any hole on the rail would do.
6. **Lead order is by wire colour, not by function** (O2) - a possible surprise if the in-house player assumes power-before-signal.
7. **Washer disappears from the model after it is fitted:** hidden again at Step 16 [035] and on the title page (it would be under the panel in those views anyway). At the same step the nut gets an unannounced 0.9 mm / 21 deg adjustment. At Step 13c the washer shifts 0.4 mm.
8. **Two unintended fly moves** caused by state carry-over: switch rises 81 mm entering [001]; pot backs off 79 mm entering [025].
9. **The pot is shown "seated" in empty space for 9 steps** ([016]-[024]) before its panel exists on screen.
10. **Frame crop:** in [012]-[015] the switch's routed leads run off the top of the frame.

Data caveats (not authoring issues, but they affect how the digest reads for this guide)

1. The digest undercounts by one part on every step where F4 is on screen ([000], [002]-[009], [012]-[015], [035]-[041]): the top-level `F4-2` node carries a stale `visible: false` from the title step while its solids are switched on individually. The thumbs show F4; a leaf-level tracker (`reports/_work_lac_p2/trackC.py`) agrees with the thumbs. The digest therefore does not list "F4 appears" at Step 1 [002].
2. The README describes Transition steps as camera steps; here all 3 are part motions with the camera still.
3. The digest prints Step 9's arrow as pointing `+Y`, opposite to Steps 8 and 10. That is stale stored geometry; the arrow is object-anchored and the render shows all three pointing off the shaft.
4. Offsets printed as "still displaced" for knob, nut, resistors, F3, breadboard and the Nano (2.6 mm) are permanent placement offsets of re-used CAD instances, not hover states.
5. The toolbox inventory (53 images, 41 labels, 7 arrows, 49 lead lines) is the Full Build's; this guide shows 13 images, 10 labels, 3 arrows and 5 lead lines. Labels such as `2x`, `GND`, `c15` belong to other parts.
6. 18 of the 42 saved thumbnails are dated 2025-11-23, before this project was created (2025-12-11): they were inherited from the source project. 18 were re-saved 2026-01-03 (every step that shows the breadboard) and 6 on 2026-05-11 ([019]-[024], 1400x700 instead of 1400x676).

## 6. Relation to the other LAC guides

- **Full Build:** steps [002]-[040] here are identical (same parts appearing/disappearing, same moves, same annotations and screen positions, same cameras) to `19075-lac_full_build` [032]-[070], i.e. "Step 15" ... "Step 32c", including the `Ttansition` typo. Only the numbering (1-18), the Start page and the Completed View are specific to this part. The section card [001] differs only in what it has to hide.
- **Part 1 -> Part 2:** the 27 parts that fade in at Step 2 [004] are exactly Part 1's Completed View (27 parts).
- **Part 2 -> Part 3:** Part 3's Step 1 brings back 50 parts, matching this guide's end state.
- **Shared template:** all four parts use the same title-page slots and the same logo; each has its own title PNG. Part 3 also has 10 eye icons and 10 labels and names every new component with a card (Alarm Buzzer, LCD Screen, USB Cable); Part 1 has one card (Real Time Clock); Part 4 has no labels at all and 27 lead lines (pure mechanical assembly). Part 2 is the only LAC part that mixes all four step kinds (mount, wire, remove, adjust).
- I did not open the sibling guides' thumbnails; the comparison above is from their digests only.
