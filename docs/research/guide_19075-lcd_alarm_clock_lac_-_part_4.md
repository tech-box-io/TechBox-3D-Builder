# Guide report: 19075-lcd_alarm_clock_lac_-_part_4  (LCD Alarm Clock, Part 4 — closing the enclosure)

Sources read: `digest/19075-lcd_alarm_clock_lac_-_part_4.md` (all 419 lines), all 6 contact sheets, 34 individual thumbs (plus enlarged crops), targeted queries of `cadasio_raw/…part_4.json` (script: `reports/_work_lac4/track.py`), and a step-by-step comparison against `digest/19075-lac_full_build.json`.

## 1. Summary

Part 4 is a purely mechanical guide: the student closes the laser-cut wooden enclosure around the electronics wired in Parts 1-3. No wire, screw or board is added. Seven loose wooden pieces are introduced (2x F7 clamp posts, F9 upright, F8 brace, F5 end, F2 back, F6 end) and four sub-assemblies that are already wired and tethered by their leads are picked up and fitted (piezo buzzer, F4 top panel with rocker switch, the LCD, F1 front panel with potentiometer and knob). The guide has 42 viewer steps: 1 title page, 17 `Step N` / `Step Nc` pairs, 6 auto-advancing `Transition` steps and a `Completed View`. It is wordless: 0 text labels, 0 step descriptions, 0 popups. Everything is communicated with red 3D lead lines (27), black "eye" icons (11), two zoomed inset images, three red arrows, and the part IDs engraved on the wood ("F1" ... "F9"). Rigid loose parts tween from a hover pose to their seat; anything tethered by wires cross-fades between pre-modelled poses. Steps [001]-[041] are identical to the last 41 steps of the LAC Full Build (its Step 41-57), renumbered from 1.

## 2. Step table (every viewer step)

Camera notation: `d` = distance mm, `el` = elevation, `az` = azimuth. "same" = camera unchanged from previous step. All steps are 800 ms.

| idx | name | kind | what is added or done | annotations | camera |
|---|---|---|---|---|---|
| 000 | Start | title, pause | Title page; finished closed clock shown on the right half | 2 unanchored images: TechBox logo SVG top-left (2%,6%, w 38.9%); title block PNG bottom-left (2%,64%, w 42.1%: "LCD Alarm Clock (LAC) / Part 4 / (c) 2025 TechBox ...") | MOVE -> d377 el37 az143 |
| 001 | Step 1 | hover, pause | Scene resets to end-of-Part-3 layout (24 parts fade in, 26 out). 2x F7 posts hover 80.3 mm straight above their slots in base F3 | 2 red lead lines, vertical, 75.4 / 76.9 mm, one per post: F7 bottom tab -> F3 slot | MOVE (rot 64 deg) -> d377 el22 az-144 |
| 002 | Step 1c | completed, pause | Both F7 tween 80.3 mm down, seated | none (lines removed) | same |
| 003 | Step 2 | action, pause | Nothing moves. Instruction: spread the two F7 posts apart | 2 thick red straight arrows (38.5 / 47.9 mm) pointing in opposite directions away from the posts | same |
| 004 | Step 2c | completed, pause | F7 posts tilt outward 15.1 / 16.0 deg about a pivot at their base | none | same |
| 005 | Step 3 | attention, pause | Nothing moves. Flags the loose buzzer and the slot in F7 it sits in | 2 eye icons: -> buzzer; -> F7-1 slot | MOVE (rot 106 deg) -> d377 el50 az55 |
| 006 | Step 3c | completed, pause | Buzzer cross-fades from loose pose to seated between the splayed posts (Piezo Buzzer-1 + 2 wires -> Piezo Buzzer-2 + red/black wires) | none | same |
| 007 | Step 4 | attention, pause | Nothing moves. Flags both posts (squeeze back) | 2 eye icons -> F7-1, F7-2 | same |
| 008 | Step 4c | completed, pause | F7 posts rotate back upright, clamping the buzzer | none | same |
| 009 | Step 5 | hover, pause | F9 upright fades in 103.9 mm to the side and 35.3 mm above its seat | 2 red L-shaped polyline lead lines (108.5 / 111.9 mm end to end; ~107 mm horizontal run then ~26 mm drop): F9 bottom tabs -> two slots in F3 | MOVE (rot 11 deg) -> d323 el42 az45, zoom x1.17 |
| 010 | Transition | auto (play) | F9 slides 103.9 mm sideways to above its slots | lines removed | same |
| 011 | Transition | auto (play) | F9 tilts 25.8 deg and drops toward the base (angled insertion) | none | same |
| 012 | Step 5c | completed (partial), pause | F9 moves a further 33 mm, still tilted, first tab hooked into F3 | 1 inset detail image (w 20.3%, at 66%,37%, right of model), blue rounded border, blue leader to F9 foot; red rectangle inside marks the slot | same |
| 013 | Step 6 | hover + attention, pause | Nothing moves | 1 very short red lead line (7.3 mm, vertical) F9 tab -> F3 slot, plus 1 eye icon on the same tab; inset removed | same |
| 014 | Step 6c | completed, pause | F9 rotates upright and moves 65 mm, seated | none | same |
| 015 | Step 7 | attention, pause | Nothing moves. Flags F1 front panel (lying face-down, tethered by pot wires) and the direction to move it | 1 eye icon -> F1; 1 thick red arrow (101.7 mm) pointing across the build | MOVE (rot 39 deg) -> d377 el49 az101, zoom x0.86 |
| 016 | Step 7c | completed, pause | F1 + pot + knob + 3 wires cross-fade to a new pose: face-up on the other side of the base (F1-3 -> F1-4) | none | same |
| 017 | Step 8 | attention, pause | Nothing moves. Flags F4 top panel (lying behind, tethered by rocker-switch wires) | 1 eye icon -> F4 | MOVE (rot 15 deg) -> d377 el47 az123 |
| 018 | Step 8c | completed (to hover), pause | F4 + rocker switch + 3 wires cross-fade to a hover pose ~46-50 mm above the uprights (F4-2 -> F4-3) | 1 eye icon -> a pot wire crossing the breadboard (check routing) | same |
| 019 | Transition | auto (play) | Camera only (lower and closer) | eye removed | MOVE (rot 13 deg) -> d323 el33 az123, zoom x1.17 |
| 020 | Step 9 | hover, pause | Nothing moves (F4 already hovering) | 4 red lead lines, vertical, 46.4-49.5 mm: top tabs of F9 (x2), F7-1, F7-2 -> slots in F4 | same |
| 021 | Step 9c | completed, pause | F4 + switch + wires cross-fade to seated (F4-3 -> F4-1) | none | same |
| 022 | Step 10 | hover, pause | F8 brace fades in 94.2 mm to the side | 2 red lead lines, horizontal, 94.2 mm each: F8 top hook -> F4 slot, F8 bottom hook -> F3 slot | MOVE (rot 14 deg) -> d323 el44 az134 |
| 023 | Step 10c | completed, pause | F8 tweens 94.2 mm, seated | none | same |
| 024 | Step 11 | attention, pause | Nothing moves. Flags the LCD (lying flat, tethered by 4 wires) | 1 eye icon -> LCD PCB | MOVE (rot 64 deg) -> d439 el30 az53, zoom x0.74 |
| 025 | Step 11c | completed (to hover), pause | LCD + 4 wires + 4 connector caps cross-fade to a standing pose ~25 mm in front of the F9 hooks (LCD V1-2 -> V1-3) | none | same |
| 026 | Step 12 | hover, pause | Nothing moves | 2 short red lead lines (25.1 / 24.8 mm) F9 hooks -> LCD PCB edge; 1 inset detail image (w 15.0%, top-left at 20%,4%) with 2 red rectangles marking the hooks | same |
| 027 | Transition | auto (play) | Nothing moves; annotations cleared | none | same |
| 028 | Transition | auto (play) | LCD cross-fades to an intermediate pose (V1-3 -> V1-5) | none | same |
| 029 | Step 12c | completed, pause | LCD cross-fades to seated (V1-5 -> V1-1) | none | same |
| 030 | Step 13 | attention, pause | Nothing moves. Flags F1 panel lying beside the build (one resistor-lead solid is silently hidden here) | 1 eye icon -> F1 | MOVE (rot 59 deg) -> d377 el42 az126, zoom x1.17 |
| 031 | Step 13c | completed (to hover), pause | F1 + pot + knob + 3 wires cross-fade to hover ~73 mm in front of the open front (F1-4 -> F1-2) | none | same |
| 032 | Step 14 | hover, pause | Nothing moves | 4 red lead lines, horizontal, 73.3 mm each: 2 tabs of F4 + 2 tabs of F3 -> slots in F1 | same |
| 033 | Step 14c | completed, pause | F1 assembly cross-fades to seated (F1-2 -> F1-1) | none | same |
| 034 | Step 15 | hover, pause | F5 end panel fades in 56.0 mm off the left end | 4 red lead lines, 50.7-55.9 mm: 2 tabs of F1 + 2 tabs of F3 -> slots in F5 | MOVE (rot 66 deg) -> d377 el30 az43 |
| 035 | Step 15c | completed, pause | F5 tweens 56 mm, seated | none | same |
| 036 | Step 16 | hover, pause | Scene up-axis flips to -X so the box is shown lying on its front; F2 back panel fades in tilted 21.4 deg, ~80 mm away | 2 red lead lines, diagonal, 75.6 / 75.8 mm: F2 edge tabs -> slots in F5 | MOVE (rot 66 deg) -> d439 el41 az-40, zoom x0.86 |
| 037 | Transition | auto (play) | F2 slides ~78 mm so its edge tabs enter F5, still tilted 21.4 deg like an open lid | lines removed | same |
| 038 | Step 16c | completed, pause | F2 rotates 21.4 deg down about its hinge edge, seated | 1 eye icon -> USB cable where it exits through the F2 notch | same |
| 039 | Step 17 | hover, pause | Up-axis back to +Y; F6 end panel fades in 67.5 mm off the right end | 4 red lead lines, 63.4-64.1 mm: 2 tabs of F1 + 2 tabs of F2 -> slots in F6; eye removed | MOVE (rot 102 deg) -> d439 el36 az133 |
| 040 | Step 17c | completed, pause | F6 tweens 67.5 mm, seated | none | same |
| 041 | Completed View | final, pause | Nothing changes | none | MOVE (rot 70 deg) -> d377 el34 az45, zoom x1.17 |

Totals shown to the student: 27 lead lines (10 steps), 11 eye icons (9 steps), 2 inset images, 2 title-page images, 3 arrows (2 steps), 0 text labels.

## 3. Conventions found

### 3.1 Structure and numbering
- **Always**: `Start` title page first, `Completed View` last, both `pause`. Title page layout: logo top-left, title/part/copyright block bottom-left, finished model of *this part's end state* on the right, no anchors.
- **Always (17/17)**: every numbered step is a pair `Step N` then `Step Nc` (lowercase c). Numbering restarts at 1 for the part (Step 1-17).
- **No section cards** in this guide (Parts 1-3 have "Real Time Clock", "Rocker Switch", "Alarm Buzzer", "LCD Screen", "USB Cable").
- `Step N` shows *what to do* (annotated, part not yet seated). `Step Nc` shows *the result* with annotations cleared: 14/17 Nc steps are annotation-free. Exceptions [012], [018], [038] carry one "check this" callout on the result (inset or eye).
- Annotations live exactly one viewer step: every lead line, arrow, eye and inset is removed on the next step (20/20 annotated build steps, plus the title images).
- `Transition` = `play` (auto-advance), nav overlay hidden (`overlayVisible:false`), hidden from the step picker (5/6). In this guide 5/6 Transitions are intermediate keyframes *inside* a Step N -> Nc pair ([010],[011] F9 slide then tilt; [027],[028] clear annotations then LCD mid-pose; [037] F2 slide-in). Only [019] is a camera-only move between two numbered steps.
- All 42 steps use 800 ms, tween for moves, fade for show/hide; camera tween speed 2, no orbit animation.

### 3.2 Granularity
- **One physical part per numbered step.** Only exception: Step 1 adds the two identical F7 posts together (same part, same action, adjacent slots).
- A single part can take several numbered steps when the hand action has stages: F7/buzzer = 4 steps (insert, spread, place buzzer, close); F9 = 2 steps (hook in tilted, then stand upright).
- Tethered sub-assemblies use a **pick-up step then an attach step** (3/3 for tab-and-slot parts): Step A eye icon on the loose part -> Ac part shown at hover; Step B lead lines -> Bc seated. F4 = Steps 8/9, LCD = 11/12, F1 = 13/14. The buzzer (no tabs) is one step: eye -> seated.
- Manipulation-only steps exist with no part added: Step 2 (spread), Step 4 (close), Step 7 (move the F1 panel out of the way).

### 3.3 Ordering
- Inside-out, bottom-up on the F3 base: internal uprights (F7, F9) -> clamped component (buzzer) -> top (F4) -> internal brace (F8) -> LCD -> front (F1) -> left end (F5) -> back (F2) -> right end (F6).
- Parts that later parts key into come first (F9 before F4 and before the LCD that hooks on it; F4 before F8, which spans F3-F4).
- The closing panels that hide the interior are last, and each needs the previous one (F5 lines start on F1/F3; F2 lines end on F5; F6 lines start on F1/F2).

### 3.4 Motion
- New rigid parts fade in on `Step N` already displaced along their real insertion axis, in final orientation, and tween straight to the seat on `Step Nc`: F7 80.3 mm (from above), F8 94.2 mm (from the side), F5 56.0 mm, F6 67.5 mm. Range of plain hover offsets: 56-94 mm.
- Parts that cannot go straight in get staged moves with a custom rotation pivot at the hinge/tab: F9 = side offset 103.9 mm + 35.3 mm high -> slide -> tilt 25.8 deg -> hook -> stand upright (4 keyframes over Step 5, 2 Transitions, 5c, 6c); F2 = tilted 21.4 deg and ~80 mm away -> slide to hinge edge (Transition) -> rotate flat (16c); F7 = splay 15-16 deg and back.
- **Wire-tethered things never tween.** Each pose is a separate pre-modelled set (panel + component + its wires + connector caps) and the sets cross-fade: 9 swaps for 4 sub-assemblies (buzzer 1; F1 3; F4 2; LCD 3). The LCD seat uses 3 consecutive swaps ([025] -> [028] -> [029]) to fake a motion path.
- No wire straight-to-routed swaps of individual jumpers occur in this guide (no jumpers are added).

### 3.5 Red lead lines
- Style: `#ff0000`, solid, thin (scale 5, a few px), 3D, anchored at both ends to part features so they follow the parts; depth-tested (hidden behind panels, visible again through the slot).
- **Anchor rule (9/10 steps): the line is authored from the tab (male feature) to the slot (female feature)**, regardless of which part is the moving one (F7 tab -> F3 slot; F4/F3 tab -> F1 slot; F1/F3 tab -> F5 slot). Exception: Step 12 runs from the fixed F9 hook notch to the LCD board edge. Lines have no arrowhead, so the student sees only "this feature meets that feature".
- Count per step is 1, 2 or 4, never more: 2 lines for a part with two tabs or one mating edge (Steps 1, 5, 10, 12, 16); 4 lines = 2 per mating edge for a panel that closes onto two neighbours (Steps 9, 14, 15, 17); 1 line in Step 6. Not every tab gets a line on the big panels (F1, F5, F6 have more slots than lines).
- Lines are parallel to the insertion axis and span the whole gap. Length vs hover offset where both are known: Step 1 75.4-76.9 / 80.3; Step 10 94.2 / 94.2; Step 15 50.7-55.9 / 56.0; Step 16 75.6-75.8 / 79.7; Step 17 63.4-64.1 / 67.5 -> ratio 0.91-1.00 (the shortfall is the tab depth).
- 25/27 lines are straight 2-point lines. Exception: the two Step 5 lines are L-shaped polylines (horizontal run, then drop into the slot) because the part comes from the side.
- Lead lines appear only on `Step N` (10/10) and are removed when the part starts to move.

### 3.6 Arrows
- 3 arrows in 2 steps, both for hand actions that are not "insert tab into slot": Step 2 (two opposed arrows = spread apart) and Step 7 (one arrow = carry this panel over there, paired with an eye).
- Style: red `#ff0000` straight 3D arrow, much thicker than a lead line (body 4-5, head width 15-20, head length 10-17), flat shaded.

### 3.7 Eye icon and insets (no text labels at all)
- Eye icon: black glyph PNG, 7.81% of viewport width (10/11; one is 7.92%), no container, straight light-blue leader `#7fdbff` thickness 5, ending in a dashed "life saver" ring of the same blue on the target.
- Two uses: (a) on `Step N`, "pick this up / act on this" for a part already on the table (buzzer [005], both F7 posts [007], F1 [015] and [030], F4 [017], LCD [024]) — 7 icons; (b) "check this detail" (F7 slot [005], F9 tab [013], wire routing [018], USB cable in notch [038]) — 4 icons. 1 or 2 per step. 9 of the 11 sit on a `Step N` (one of them, [013], alongside a lead line); 2 sit on a `Step Nc` ([018], [038]).
- Placement: free white space near the target, no fixed corner. Screen positions (x%,y%): (27,28) (57,13) (56,3) (69,40) (54,60) (24,10) (69,32) (34,56) (46,68) (72,28) (43,11).
- Inset detail image (2): a pre-rendered close-up of the same toon model in a white rounded rectangle with a `#7fdbff` border (thickness 5), same leader and ring anchor, with red outline rectangles inside marking the exact slot/hooks. Used where the mating feature is too small or hidden at the step's zoom (F9 foot [012]; LCD on F9 hooks [026]). Sizes 20.3% and 15.0% of viewport width.
- Part identification relies on the IDs engraved on the wood ("F1" ... "F9"), modelled as black solids on each panel.

### 3.8 Camera
- **Never moves between `Step N` and `Step Nc`, nor in Transitions inside a pair (0/17 Nc, 0/5 inner Transitions).** It moves on entering a `Step N` (11/17), on Start, on Completed View, and in one between-step Transition [019].
- A `Step N` keeps the previous camera when it continues work on the same part/area (Steps 2, 4, 6, 9, 12, 14).
- Perspective, fov 45 deg. Only three distances are used: 323 / 377 / 439 mm (steps of x1.17). Elevation always 22-50 deg (three-quarter view from above).
- Azimuth is chosen so the hover gap is seen roughly side-on and the lead lines are not foreshortened; the camera swings to whichever side the part approaches from (az 43 for the left end, 133 for the right end). Rotation per move 11-106 deg, median ~64 deg.
- Framing is loose and follows the active area: content covers 8-29% of viewport pixels; idle loose parts are allowed to run off-screen ([005]-[014], [017]-[023]); the hovering part and its full lead lines are always in frame.
- One-off: for Step 16 the scene up-axis is switched to -X ([036]) and back to +Y ([039]) so the box appears laid on its front for fitting the back panel.

### 3.9 Look
- White `#ffffff` background, no ground plane or shadows, toon (two-tone) shading on 1587 part overrides, black edges width 1, no silhouette, view cube on, bottom horizontal nav overlay.

## 4. Part looks (from the renders)

| part | look |
|---|---|
| Wooden panels F1-F9 | Flat light tan (material `#deb887`; lit faces render ~`#fed39c`, shaded faces ~`#c9a77a`), thin black edges, part ID engraved in black |
| LCD 20x4 module | Bright green PCB (~`#1c8e36`), black bezel, pale grey screen window (~`#ebebeb`), silver header pins; black I2C backpack with blue trim pot |
| Breadboard | White body, black holes, red and blue rail stripes |
| Arduino Nano | Dark navy PCB with silver pins |
| RTC module (HW-84) + coin cell | Bright blue PCB, black chips; silver cell with "CR2025" marking |
| Rocker switch | Black body, small white details |
| Piezo buzzer | Black cylinder; red and black leads |
| Potentiometer / knob / nut | Brown body `#855e42`, silver shaft; black knob with silver-white ring; silver nut |
| USB cable | Black cable and moulded plug, silver USB-A shell with white insert |
| Jumper / tether wires | Saturated flat colours: red `#ef3340`, black `#2d2926`, tan `#b28362`, yellow `#eac80d`, blue `#0074d9`, teal `#13a3a3`, purple `#611b6c`, orange `#ff851b`, green `#10cc62`; black Dupont housings with silver tips |
| Resistors | Blue bodies with colour bands, silver leads |
| Lead lines / arrows | Pure red `#ff0000` |
| Eye icon, leaders, inset borders | Black glyph; light blue `#7fdbff` |

## 5. Anomalies and inconsistencies

1. Transition [028] is not hidden from the step picker (`hideInStepPicker:false`); the other 5 Transitions are hidden.
2. One eye icon ([005], on the F7 slot) is 7.92% wide; the other 10 are 7.81%.
3. A single resistor-lead solid (`LAC Resistor 1 / Part6`) is silently hidden at Step 13 [030] and never restored.
4. Lead lines in Step 6 (7.3 mm) and Step 12 (~25 mm, mostly occluded) are almost invisible in the main view; the author compensates with an eye icon and an inset.
5. Step 2 arrows are anchored at both ends to F3 rather than to the F7 posts they describe; the Step 7 arrow is anchored to the USB plug and a jumper wire, so it starts beside, not on, the F1 panel flagged by the eye.
6. One of the two Step 5 polylines has 5 points with 3 nearly coincident at its start (click artefact); its sibling has 3 points.
7. Loose tethered panels do not rest on a common table plane (F4 floats ~40 mm up in [001]-[017]).
8. Per raw visibility flags the potentiometer nut is visible in [001]-[015], absent in the F1 pose variants [016]-[032], and back at [033].
9. The project carries unused annotations inherited from the full-build project: 41 text labels (breadboard coordinates, "(+) red", "(-) blue", GND/VCC/SDA/SCL), 49 lead lines, 53 images, 7 arrows in inventory versus 0 labels, 27 lines, 15 images, 3 arrows actually shown here.
10. Data caveat, not an authoring fault: the digest misses the appearance and seating of F5, F2 and F6 (Steps 15-17) because their visibility is set on child solids; I recovered them from the raw payload. The digest's ~1.7 m "still displaced" values for F1, knob, nano etc. are component placement offsets, not hover offsets.
11. Step names in this guide are clean (other LAC guides contain "Ttansition" and "Step 14C").

## 6. Relation to the other LAC guides

- **Full Build**: Part 4 [001]-[041] equals Full Build [090]-[130] ("Step 41" ... "Step 57", "Completed View"). I compared camera pose, behaviour and the annotation set step by step: 0 differences in 41 steps. Only the numbering (restarted at 1) and the Part-4 title page differ. Like Part 4, the Full Build has no section card in front of this enclosure section.
- **Part 3**: Part 4's Step 1 layout (F3 base with breadboard, F4 tethered by the switch, F1 face-down tethered by the pot, LCD lying flat, loose buzzer, USB cable) is Part 3's Completed View. Title pages share one template; each shows that part's end state.
- **Parts 1-3** are wiring guides with named section cards; Part 4 is the only LAC part with no section card and no wiring.
- **Deconstruction**: opens by undoing this guide, reusing the same pose-variant components in reverse order (F1-1 -> F1-2 -> F1-4, LCD V1-1 -> V1-5 -> V1-3 -> V1-2, Rocker Switch-1 -> 3 -> 2), and uses arrows where this guide uses lead lines (checked on its first ~45 steps only).
