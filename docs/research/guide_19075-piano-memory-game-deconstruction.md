# Guide report — `19075-piano-memory-game-deconstruction`

Project name in Cadasio: "Piano Memory Game(PMG) Disassembly" · kit PMG · role: deconstruction (take-apart)
Sources: `digest/19075-piano-memory-game-deconstruction.md|json`, all 8 contact sheets, ~35 individual thumbs, targeted queries on `cadasio_raw/…deconstruction.json`, and the digest + raw of `19075-piano_memory_game_pmg-full_build` for the comparison. Helper scripts used are in `reports/_work_pmg_decon/`.

Step indices `[NNN]` are the digest/thumbnail indices (61 viewer steps, `[000]`–`[060]`). "D7" = deconstruction Step 7, "B43" = full-build Step 43.

---

## 1. Summary

The guide takes the finished Piano Memory Game apart in 23 numbered steps (61 viewer frames: Start, 23 × `Step N`, 22 × `Step Nc`, 14 auto-advancing `Transition`, `Completed View`). It has two phases. Steps 1–16 `[001]–[046]` strip the laser-cut housing: top cover off, the three wired modules (LED matrix, 4-digit display, Nano I/O shield) are lifted off the housing but stay wired together and lie beside it, then the wooden panels come off one at a time in exactly the reverse of the build order, with the four push buttons pulled out midway. Steps 17–23 `[047]–[060]` then unplug the loose electronics harness from one fixed camera: matrix board, its 5 wires, USB cable, 4 button modules, display, the remaining 16 wires, and finally the Nano, leaving the bare Nano I/O shield as the "Completed View". The authoring grammar is radically simpler than the build guides: there is no text at all (0 labels, 0 descriptions, 0 popups, 0 section cards), 0 red lead lines, and instead one fat red 3D arrow per action (31 arrow appearances) whose tail sits on the part to remove and whose head points along the pull direction; an eye icon is used only 4 times. Parts are not shown travelling to a hover position and resting there: on the `Step Nc` frame the part slides away along the arrow and fades out in the same 800 ms. The file is demonstrably a reversed clone of the full-build project: 16 of its camera poses are byte-identical to the camera of the build step being undone, and its arrows are the build's lead lines reversed (same axis, opposite sense, similar length).

---

## 2. Step table (every viewer step)

Camera column: `d` = distance mm, `el` = elevation, `az` = azimuth. "= B51" means the camera pose is byte-identical to full-build Step 51. "same" = camera did not move on entering this frame. All frames animate in 800 ms; `auto` = behaviour `play` (auto-advance), everything else waits for Next.

| idx | name | kind | what is done / what changes on screen | annotations | camera |
|---|---|---|---|---|---|
| 000 | Start | title | Fully assembled PMG, nothing to do | 2 image callouts, no leader: TechBox logo SVG top-left at (5,8)% width 36%; title PNG bottom-left at (4,64)% width 46% reading "Piano Memory Game (PMG) / Deconstruction / © 2026 TechBox. A division of TARIS Industries, LLC. All Rights Reserved." | 3/4 front view from above, d320 el33 az-46 |
| 001 | Step 1 | step | Top cover H14 (plate with the display window). Cover is nudged 2 mm / ~3° on entry | 2 overlapping short arrows (16 and 29 mm, up-and-back) at H14's top edge; title images removed | moves 96° to rear-side view d374 el36 az-172 (= B51) |
| 002 | Transition | auto | H14 pivots ~10° the other way, its top edge lifting clear of the stand (the pose it had in the build's B51 Transition) | arrow swap: one 64 mm arrow up-and-out from the same edge | same |
| 003 | Step 1c | done | H14 slides off and fades. 4-digit display exposed | none | same |
| 004 | Step 2 | step | LED matrix still seated on the two uprights; nothing moves | eye icon at (60,7)%, light-blue leader to the matrix's top edge. No arrow | low side view d275 el14 az-177 (= B50) |
| 005 | Transition | auto | Matrix + its 5 wires cross-fade to a "lifted along the stand" pose model | 1 arrow, 62 mm, up from matrix top edge; eye removed | same |
| 006 | Transition | auto | Matrix cross-fades to a "pulled clear and tilted" pose; 5 wires replaced by one merged ribbon model | none | same |
| 007 | Transition | auto | nothing changes (camera-only frame) | none | swings 96° to front 3/4 view d320 el38 az-68 (= B49) |
| 008 | Step 2c | done | Matrix cross-fades to "lying on the bench to the right of the housing", still wired | none | same |
| 009 | Step 3 | step | 4-digit display still seated | eye icon at (62,12)% → display face. No arrow | d236 el34 az-25 (= B48) |
| 010 | Transition | auto | Display + 4 wires cross-fade to a lifted pose | 1 arrow, 29 mm, up from the display | same |
| 011 | Transition | auto | Display cross-fades to a pulled-out pose behind the stand | none | same |
| 012 | Transition | auto | nothing changes (camera-only frame) | none | swings 83° to rear view d320 el41 az89 (= B47) |
| 013 | Step 3c | done | Display cross-fades to a bench pose right of the shield, still wired | none | same |
| 014 | Step 4 | step | Nano I/O shield (with Nano, USB cable, all 21 jumpers) sitting in its slot at the back of the housing | 1 thin arrow, 84 mm, straight up from the shield | d436 el34 az59 (new; close to B46 d436 el29 az45) |
| 015 | Transition | auto | Shield + Nano + USB + all wires cross-fade to "held high above the housing" pose | none | same |
| 016 | Step 4c | done | Same group cross-fades to "flat on the bench behind the housing" pose | none | same |
| 017 | Step 5 | step | Rear brace H13 (bridges the two uprights) | 1 arrow, 74 mm, up-and-back along the slope, tail on H13 | d275 el40 az130 (= B44) |
| 018 | Step 5c | done | H13 slides 80 mm along the slope and fades | none | same |
| 019 | Step 6 | step | Upright H12 (left display support) | 1 arrow, 38 mm, horizontal toward the keys | d236 el37 az-167 (= B43) |
| 020 | Transition | auto | H12 slides 7.6 mm horizontally (unhooks) | arrow swap: 43 mm straight up | same |
| 021 | Step 6c | done | H12 lifts 44 mm and fades | none | same |
| 022 | Step 7 | step | Upright H11 (right display support) | 1 arrow, 46 mm, horizontal | d275 el40 az-12 (= B42) |
| 023 | Transition | auto | H11 slides 6.7 mm | arrow swap: 57 mm straight up | same |
| 024 | Step 7c | done | H11 lifts 53 mm and fades | none | same |
| 025 | Step 8 | step | Upper deck H10 | 1 arrow, 52 mm, up, at H10's front edge | low view d275 el13 az-29 (= B41) |
| 026 | Transition | auto | (hidden authoring step folded in) H10's front edge lifts 9 mm, plate tilts ~8° | arrow swap: 116 mm, horizontal, pulling the plate forward over the keys | same |
| 027 | Step 8c | done | H10 slides out 126 mm and stays visible, hovering in front of the housing | none | same |
| 028 | Step 9 | step | H10 hidden on entry. Four piano keys (plates engraved "H9") | 1 arrow, 110 mm, horizontal away from the housing, tail on key 3; plus eye icon at (21,19)% anchored to the same key | d275 el36 az-22 (= B38) |
| 029 | Step 9c | done | All 4 keys slide out 142 mm and fade. Four push buttons (black, yellow, white, blue caps) revealed | none | same |
| 030 | Step 10 | step | Key-rest bar H8 (strip behind the buttons) | 1 arrow, 72 mm, straight up | d320 el30 az-41 (= B37) |
| 031 | Step 10c | done | H8 lifts 94 mm and fades | none | same |
| 032 | Step 11 | step | Housing now seen upside-down (camera below, scene up-axis flipped to -Y). Base plate H7 | 1 arrow, 45 mm, pointing screen-up at H7's rear edge | d320 el-24 az-49 (= B35) |
| 033 | Transition | auto | H7's rear edge tilts ~12° | arrow swap: 116 mm along the plate, outward | same |
| 034 | Step 11c | done | H7 slides out 139 mm and fades. Underside of the 4 button modules and their 12 wires exposed | none | same |
| 035 | Step 12 | step | 4 push-button modules still in their pockets (seen from below) | eye icon at (13,15)% → PCB of the 2nd module. No arrow | d275 el-40 az179 (= B33) |
| 036 | Step 12c | done | 4 modules + their 12 wires cross-fade to "pulled out, bunched beside the shield" pose. Pockets empty | none | same |
| 037 | Step 13 | step | All 71 electronic components hidden; only 6 wood parts remain (H1–H6), still upside-down. Button tray H6 | 1 arrow, 35 mm, screen-up, on H6 | d320 el-28 az-44 (= B31) |
| 038 | Transition | auto | H6 lifts ~43 mm on one edge, tilting ~18° | arrow swap: 115 mm outward along the plate | same |
| 039 | Step 13c | done | H6 slides out and fades | none | same |
| 040 | Step 14 | step | Plate H5 | 1 arrow, 35 mm, screen-up, on H5 | d374 el-34 az-42 (= B29) |
| 041 | Transition | auto | (hidden authoring step folded in) H5 lifts ~56 mm on one edge, tilting ~24° | arrow swap: 103 mm outward | same |
| 042 | Step 14c | done | H5 slides out and fades. Open frame H1+H2+H3+H4 left | none | same |
| 043 | Step 15 | step | Upright again (up-axis back to +Y). Back panel H4 | 1 arrow, 105 mm, horizontal, straight out of the back | d374 el36 az34 (= B28) |
| 044 | Step 15c | done | H4 slides 65 mm and fades. U-frame H1+H2+H3 left | none | same |
| 045 | Step 16 | step | Front rail H1 | 1 arrow, 84 mm, horizontal, forward | d374 el25 az-40 (new) |
| 046 | Step 16c | done | H1 slides 52 mm and fades. Side panels H2 and H3 left standing apart | none | same |
| 047 | Step 17 | step | Scene switch: H2 and H3 vanish, the wired electronics reappear alone in a flat bench layout (matrix left, 4 buttons top, display right, shield + Nano bottom, USB cable). LED matrix board | 1 arrow, 45 mm, pointing left, away from the matrix's 5-pin connector | rear straight-on view d320 el23 az90 (new; same direction as B25, one zoom notch further out) |
| 048 | Step 17c | done | Matrix board slides 68 mm and fades; its 5 wires stay, ending in a black connector block | none | same |
| 049 | Step 18 | step | The 5 matrix wires (brown, green, navy, maroon, teal) | 1 arrow, 66 mm, up, tail on the bundle | pan 30 mm only, no rotation, no zoom |
| 050 | Step 18c | done | 5 wires + 10 Dupont housings rise 90 mm and fade | none | same |
| 051 | Step 19 | step | USB cable | 1 arrow, 42 mm, pointing left, tail on the USB-A plug | pan 76 mm only |
| 052 | Step 19c | done | Cable and both plugs slide away and fade | none | same |
| 053 | Step 20 | step | The 4 push-button modules | 1 arrow, 45 mm, up, tail on module 2 | same |
| 054 | Step 20c | done | 4 modules move 27 mm and fade; 12 wires stay with bare black housings | none | same |
| 055 | Step 21 | step | 4-digit display | 1 arrow, 31 mm, pointing right, tail on the display | same |
| 056 | Step 21c | done | Display moves 22 mm and fades; its 4 wires stay | none | same |
| 057 | Step 22 | step | All 16 remaining wires (12 button + 4 display) | 2 arrows up (51 and 43 mm), one on each bundle | same |
| 058 | Step 22c | done | 16 wires + 32 housings rise (button wires 36 mm, display wires 75 mm) and fade. Shield + Nano only | none | same |
| 059 | Step 23 | step | Arduino Nano on the shield | 1 arrow, 29 mm, up, tail on the Nano (anchored at its reset button) | zoom in x1.85 to d173, same direction |
| 060 | Completed View | end | Nano rises 26 mm and fades. Bare Nano I/O shield alone | none | same |

Authored-but-hidden steps (never shown, their properties are folded into the next frame): a `Transition` between `[015]` and `[016]`; a `Transition` before `[026]` (holds the H10 lift/tilt); a `Transition` before `[041]` (holds the H5 lift/tilt); `Step 23c` and `Step 59` between `[057]` and `[058]` (leftovers of an earlier two-part wire removal).

---

## 3. Is it the exact reverse of the build?

Full build (`19075-piano_memory_game_pmg-full_build`, 51 numbered steps, 117 frames) → deconstruction (23 numbered steps, 61 frames).

Macro order is an exact mirror. Build: wire up the electronics on the bench (B1–B25) → housing lower half (B26–B32) → buttons in (B33–34) → housing upper half (B35–B44) → mount shield, display, matrix (B45–B50) → cover (B51). Deconstruction: cover → dismount matrix, display, shield → upper housing → buttons out → lower housing → unplug electronics.

### Housing phase (D1–D16 vs B51→B26): strict reverse at part level, with build pairs merged

| decon | undoes | merge |
|---|---|---|
| D1 H14 | B51 | 1:1 |
| D2 LED matrix off stand | B50 + B49 | 2 → 1 |
| D3 display off stand | B48 + B47 | 2 → 1 |
| D4 shield out of slot | B46 + B45 | 2 → 1 |
| D5 H13 | B44 | 1:1 |
| D6 H12 | B43 | 1:1 |
| D7 H11 | B42 | 1:1 |
| D8 H10 | B41 + B40 | 2 → 1 |
| D9 4 piano keys | B39 + B38 (build: 1 key, then 3 more) | 2 → 1 |
| D10 H8 | B37 | 1:1 |
| D11 H7 | B36 + B35 | 2 → 1 |
| D12 4 buttons out | B34 + B33 (build: 1 button, then 3 more) | 2 → 1 |
| D13 H6 | B32 + B31 | 2 → 1 |
| D14 H5 | B30 + B29 | 2 → 1 |
| D15 H4 | B28 | 1:1 |
| D16 H1 | B27 (H3) + B26 (H1+H2) | 2 → 1; H2 and H3 are never explicitly removed |

26 build steps become 16. No part is taken out of order. Where the build spent two numbered steps on one part (slide in, then drop/lock: H5, H6, H7, H10), the deconstruction uses one numbered step with an auto-advancing `Transition` in the middle. Where the build did "one, then the other three" (keys, buttons) the deconstruction does all four at once.

### Electronics phase (D17–D23 vs B25→B1): regrouped and reordered, not a reverse

Build order: Nano onto shield (B1) → 12 button wires fanned out (B2) → button wires one at a time, VCC/OUT/GND for each of 4 buttons (B3–B14) → display wires (B15–B19) → matrix wires (B20–B24) → USB (B25).
Strict reverse would be: USB → matrix wires → display wires → button wires → Nano.
Actual: matrix board (D17) → matrix wires (D18) → USB (D19) → button modules (D20) → display (D21) → all 16 remaining wires (D22) → Nano (D23).

- Reorders: USB comes after the matrix instead of first; buttons come before the display. The actual order is a left-to-right sweep across the fixed bench view in `[047]` (matrix far left, USB left, buttons centre, display right), then everything left on the shield, then the Nano.
- Regrouping: each build wiring step attached one wire at both ends (module pin and shield pin). The deconstruction splits by end instead: first the module is pulled off all of its wires at once (D17, D20, D21), then the wires come off the shield as a bundle (D18: 5 wires; D22: 16 wires).
- 25 build steps become 7. The 21 single-wire build steps collapse into 2 bundle steps plus 3 module steps.

### How the frames differ from construction frames

| aspect | full build | deconstruction |
|---|---|---|
| Section cards with photo/diagram | 5 (Nano I/O Module, Push Buttons, 4-Digit Display, Dot Matrix Display, USB Cable) | 0 |
| Text labels shown | 43 (pin names at both wire ends) | 0 |
| Red lead lines shown | 48 | 0 |
| Red 3D arrows shown | 1 (B46) | 31 |
| Eye icon | on essentially every wiring step, ~30 | 4 (D2, D3, D9, D12) |
| `Step N` frame | new part appears hovering at an offset, lead lines to target | part still seated, arrow on it |
| `Step Nc` frame | part tweens to its seat | part tweens away and fades out |
| Auto `Transition` frames | 8 of 117 (7%) | 14 of 61 (23%) |
| Wires | one per step, straight model swapped for routed model | bundles; never straightened; no straight models used |
| Camera | new view for most part steps | the same views, reused exactly for 16 poses |

---

## 4. Conventions, with evidence and exceptions

### Structure
1. **Frame grammar per numbered step is `Step N` (pause, shows what to do) → optional `Transition`s (auto) → `Step Nc` (pause, shows the result).** 22 of 23 steps have an `Nc`. Exception: Step 23 has no `23c`; `Completed View` `[060]` plays that role.
2. **Frames per step: 2 (13 steps), 3 (8 steps: 1, 4, 6, 7, 8, 11, 13, 14), 5 (2 steps: 2, 3).** All 14 `Transition`s are in Steps 1–14; Steps 15–23 have none.
3. **No section cards, no step descriptions, no popups, no on-screen text** apart from the title card image `[000]`. Always true.
4. **Numbering restarts at 1 and is independent of the build** (23 steps vs 51). Step prefix "Step", completed suffix lowercase "c".
5. **Title card** `[000]`: assembled model + logo top-left + title block bottom-left; both images disappear on entering Step 1.
6. **Every frame is 800 ms; part moves tween, shows/hides fade; camera tweens, no orbit animation.** 66 of 66 authored steps.

### Granularity
7. **One physical thing per numbered step.** 15 of 23 steps act on exactly one component (H14, H13, H12, H11, H10, H8, H7, H6, H5, H4, H1, matrix board, USB cable, display, Nano).
8. **Identical multiples go together in one step with a single cue:** 4 piano keys (D9), 4 buttons out of the housing (D12), 4 buttons off their wires (D20).
9. **Wires are removed as bundles, never singly:** 5 (D18) and 16 (D22). Each wire's two black Dupont housings go with it.
10. **A wired module leaving the housing is its own step and removes nothing** (D2, D3, D4, D12): part count on screen is unchanged, only pose models swap.

### Ordering
11. **Top-down, outside-in for the housing, the strict reverse of the build** (table in section 3). Always true for D1–D16.
12. **Dismount wired modules from the housing before removing the panels that hold them, and keep them wired until the housing is gone.** Matrix, display and shield stay connected from `[008]` to `[047]`.
13. **Unplugging order on the bench: module end first, shield end second; Nano last; shield is never removed.** Matrix → its wires; buttons and display → their wires together.
14. **Bench unplugging follows screen position left to right**, not build order (section 3). One guide only, so low confidence as a rule.

### Motion
15. **The part never rests at a hover position. On `Step Nc` the part gets a displacement along the removal direction and `visible = false` in the same frame, so it slides away while fading.** 18 of 19 removals: H14 ~13 mm, H13 80, H12 44, H11 53, keys 142, H8 94, H7 139, H6 ~120, H5 ~115, H4 65, H1 52, matrix 68, matrix wires 90, USB cable ~150, buttons 27, display 22, remaining wires 36–75, Nano 26. For wood parts the displacement equals the build's hover offset for that part (H13 80.1 vs 80; H12 -44.5 vs -44; H11 -53.1 vs -53; H8 -94.5 vs -94; H7 (136,-29,2) identical; H6 (-110,-80,-1) identical; H5 (-96,-102,-1) identical; H4 -65 identical). Exception: H10 `[027]` stays visible at the build's hover offset (0, 26, 125) and is only hidden on entering Step 9 `[028]`.
16. **Two-stage removals use one `Transition`: `Step N` shows arrow 1 with the part at rest; the `Transition` plays motion 1 and swaps to arrow 2; `Step Nc` plays motion 2 with the fade.** 7 steps: H14 (tilt, then lift), H12 and H11 (slide ~7 mm, then lift), H10, H7, H6, H5 (lift one edge and tilt 8–24°, then pull out along the plate). The arrow always precedes the motion it describes by one frame.
17. **Flexible wired things are never tweened; they cross-fade between pre-modelled poses** (separate components for each pose, each with its own routed wire models). Matrix: 4 poses `[004]→[005]→[006]→[008]`; display: 4 poses `[009]→[010]→[011]→[013]`; shield harness: 3 poses `[014]→[015]→[016]`; buttons: 2 poses `[035]→[036]`. Auto `Transition`s play these as a flipbook.
18. **Flipping the model is done with the camera, not by rotating parts:** camera goes below (el -24° to -40°) and the scene up-axis is set to -Y for `[032]–[042]`, back to +Y at `[043]`. Same frames as the build's flipped block (B29–B36). Side effect: the loose electronics appear upside-down in mid-air in `[032]–[036]`.

### Lead lines
19. **No lead lines are shown at all.** 48 exist in the file (inherited from the build) and all stay hidden. The two `Transition`s `[026]` and `[041]` still carry explicit "hide" entries for build lead lines, evidence that these frames were cloned from build steps.

### Arrows
20. **One red straight 3D arrow per action.** 31 appearances: 20 of 23 `Step N` frames and 9 of 14 `Transition` frames carry an arrow; 0 of 22 `Step Nc`, 0 on Start/Completed. Exactly one arrow per frame except Step 1 (2, a duplicate) and Step 22 (2, one per wire bundle).
21. **Tail on the part to remove, head in free space along the pull direction.** In the data object 0 is always a feature of the moving part (panel body, PCB, a wire, the Nano's reset button); object 1 is the same non-assembly dummy for all 31 arrows. Nothing is drawn on a target because there is no mating target.
22. **Arrow direction is the build's lead-line direction reversed, with similar length.** Decon vs build pairs (mm): H13 74 vs 82; H10 pull 116 vs 116; H12 lift 43 vs 41; H11 lift 57 vs 50; H8 72 vs 95; H7 45 / 116 vs 29 / 139; H6 35 / 115 vs 44 / 122; H5 35 / 103 vs 57 / 118; H14 64 vs 58; keys 110 vs 104; Nano 29 vs 30 hover. Length range 16–116 mm, median 51 mm. Lengths track the travel only loosely (H4: arrow 105 mm, travel 65 mm).
23. **Arrows are mostly axis-aligned:** 12 along model +Y (up), 3 along model -Y (these are in the flipped block, so they also point up on screen), 5 along -X, 1 along +X, 5 along ±Z, 5 diagonal (parts on the sloped display stand, and the tilted plates). No arrow points along model "down into the assembly": every pull is drawn away from the model, upward or sideways (sideways arrows can slope slightly down on screen through perspective, `[028]`, `[043]`, `[045]`).
24. **One arrow stands for a whole group:** one arrow on key 3 for 4 keys `[028]`, one on button 2 for 4 buttons `[053]`, one on the bundle for 5 wires `[049]`.
25. **Arrow style:** colour #ff0000, flat, no outline, head at the end, body width 5 : head width 20 : head length 17, fade in/out. 30 of 31. Exception `[014]`: body 2, head 10. On-screen size is not constant: per-arrow scale ranges 0.025–0.10 (thin in `[014]` and `[037]`; very fat in `[005]`, `[028]`, `[053]`).

### Labels
26. **No labels.** 45 label objects exist (inherited: GND, VCC, OUT, S4, V5 …) and none is ever shown. Pin names are not needed to unplug.

### Eye icon
27. **The eye icon is rare (4 of 23 steps) and appears only on the `Step N` frame**, in the upper part of the viewport (y 7–19%), width 8.2% of the viewport, black glyph, light-blue (#7fdbff) leader ending in a dashed light-blue ring on the part.
28. **It marks a step whose action is shown by a pose swap or applies to several identical parts:** matrix `[004]` and display `[009]` (eye alone, the arrow only appears in the following auto `Transition`), 4 buttons `[035]` (eye alone, no arrow anywhere), 4 keys `[028]` (eye plus arrow). Three of the four mirror build steps that also carried an eye (B49, B47, B33/34). Exception to the pattern: the shield dismount D4 is also a pose swap but has an arrow and no eye, although its build twin B45 had an eye.

### Images
29. **Only the title card uses image callouts** (logo SVG, title PNG; no leader, positioned by top-left corner in viewport %). No photos, no pin diagrams.

### Camera
30. **The camera moves on entering a `Step N` and then stays put through its `Transition`s and `Nc`.** Moves on 20 of 23 `Step N` frames, 0 of 22 `Nc` frames. Exceptions: Steps 20, 21, 22 keep the previous camera; two camera-only `Transition`s `[007]` and `[012]` swing the view (96° and 83°) between pulling a module off the stand and showing it on the bench.
31. **Each housing step reuses the exact camera of the build step it undoes.** 16 poses are byte-identical (position and target): D1=B51, D2=B50, `[007]`=B49, D3=B48, `[012]`=B47, D5=B44, D6=B43, D7=B42, D8=B41, D9=B38, D10=B37, D11=B35, D12=B33, D13=B31, D14=B29, D15=B28. New cameras only for Start, D4, D16 and the bench phase.
32. **Bench phase uses one locked view direction** (el 23°, az 90°, straight-on from the back of the shield) for all of `[047]–[060]`; only two small pans (30 and 76 mm) and one zoom (x1.85 for the Nano) occur.
33. **Views are 3/4 from above:** elevation 23–41° on 44 frames, low side views 13–14° on 6 frames, from below -24° to -40° on 11 frames. View swings between consecutive numbered steps are large (median 41°, up to 112°).
34. **Camera distance sits on a zoom ladder with ratio ~1.166:** 173, (202), 236, 275, 320, 374, 436 mm. 320 mm is used on 25 frames, 275 on 15. FOV 45° perspective.
35. **Framing follows the build's framing of the part, not the whole scene**, so loose electronics lying beside the housing are often cut by the viewport edge (`[009]–[011]`, `[017]–[018]`, `[022]–[024]`, `[032]–[034]`).

### Context visibility
36. **Unrelated sub-assemblies are hidden once they are no longer attached.** After the buttons are out, all 71 electronic components are hidden for `[037]–[046]` (wood only); at `[047]` the wood disappears and the electronics return alone.

### Wiring
37. **Wires keep their routed shape and colour; black Dupont housings stay on the free wire ends after a module is pulled off** (`[048]`, `[054]`, `[056]`). No straight-wire models and no per-wire steps.

### Style
38. White background, no ground or shadow, toon shading with thin black outlines on every part (see section 5). Identical to the build.

---

## 5. Part looks (from the renders)

| part | look |
|---|---|
| Background | plain white #ffffff, no floor, no shadows, no gradient |
| Render style | cel/toon flat shading, 1 px black edges and silhouettes on all parts |
| Wooden housing panels H1–H14 | two flat tones only: lit faces pale cream ≈ #f8e8b0, shaded faces/edges tan ≈ #e0b888 (base material #deb887); black engraved part numbers "H1"…"H13" printed on the faces |
| Piano keys (4) | same wood look, each engraved "H9" |
| Nano I/O shield | bright blue PCB ≈ #2860f0; black female header strips and DC jack; pin headers with cream/yellow plastic (#ffff80) and silver pins; black electrolytic capacitor; small white/black button |
| Arduino Nano | dark navy PCB ≈ #001050, silver pads, black chip, white/silver mini-USB socket |
| LED matrix 32x8 | blue PCB ≈ #2048c0 on the back; four white module bodies printed "1088AS"; black face with white LED dots; black 5-pin header |
| 4-digit display | same blue PCB, black display window with white 7-segment digits |
| Push-button modules | navy PCB (#000f41), black switch body, round caps in black, yellow, white and blue (≈ #0090f8) |
| Jumper wires | thin round tubes in saturated distinct colours: matrix set brown, green, navy, maroon, teal; display set gold/yellow, black, purple, red; button set red, dark grey, white, bright green, yellow, maroon, blue, purple, green, brown, grey |
| Dupont housings | solid black blocks on every wire end |
| USB cable | very dark brown/black cable and overmoulds (#1e1616), silver USB-A shell with white tongue, right-angle mini-USB plug |
| Arrows | flat pure red #ff0000, no outline |
| Eye icon | black eye glyph; light-blue #7fdbff leader and dashed ring |
| Title images | TechBox logo: white wordmark and bulb on a sky-blue rounded rectangle; title: heavy grey condensed type, small serif copyright line |

---

## 6. Anomalies and inconsistencies

1. **Duplicate arrow at Step 1** `[001]`: two arrows (16 mm and 29 mm) with the same anchor and direction overlap. Every other single-part step has one.
2. **Arrow thickness is inconsistent.** `[014]` uses a thin arrow (body 2 / head 10) while the other 30 use 5 / 20; per-arrow scale varies fourfold.
3. **Step 8c `[027]` still shows the removed plate H10** hovering in front of the housing; it is only hidden on entering Step 9. All other `Nc` frames show the part gone.
4. **H2 and H3 are never removed by a step.** They are left standing in `[046]` and silently vanish at the scene switch `[047]`.
5. **Steps 2 and 3 have no arrow on the frame the student pauses on** (eye only); the arrow exists only on an auto-advancing `Transition` that is on screen for ~0.8 s. **Step 12 has no arrow at all.**
6. **Step 19 `[051]`: the arrow is on the USB-A (computer) end of the cable**, not at the Nano's mini-USB socket where the unplugging happens.
7. **Electronics order is not the reverse of the build** (USB after the matrix; buttons before the display).
8. **Stale hidden steps:** `Step 23c` and `Step 59` sit hidden between Step 22 and Step 22c; three hidden `Transition`s exist. Thumbnails for `[047]–[052]` carry later timestamps and a different viewport (3840x1967) than the rest, so Steps 17–19 were reworked after the first pass.
9. **No `Step 23c`;** the last result frame is called `Completed View` and shows the last remaining part rather than a completed model.
10. **Naming mismatch:** project name "Piano Memory Game(PMG) Disassembly" (no space before the bracket), title card "Piano Memory Game (PMG)" with subtitle "Deconstruction", guide id "…-deconstruction".
11. **Title text collides with the model** in the saved Start frame `[000]` (the end of "(PMG)" runs under the housing corner) because title images are placed in viewport % and the frame was saved at a wide 2.63:1 aspect.
12. **Saved frames have three different aspect ratios** (2.63:1 for 6 frames, 1.86:1 for 49, 1.95:1 for 6).
13. **Unused inherited annotations:** 45 labels, 48 lead lines, 2 arrows and 39 of the 45 image objects (only the 2 title images and 4 eye icons are ever shown) remain in the file, never shown.
14. **Sub-millimetre jitter:** Big Button Module-11 is nudged 0.1 mm back and forth in `[030]–[032]`; H14 moves +1.7 mm then -1.6 mm in `[001]–[002]`.
15. **`[006]` swaps the 5 matrix wires for a single merged ribbon component** (Part166) for one frame only, with slightly different colours.
16. **Loose electronics render upside-down in mid-air** during the flipped frames `[032]–[036]`.
17. **Data caveat (digest vs renders):** the digest's ancestor-based visibility under-reports three components. The 4-digit display (Display TM1637-4) is on screen from `[013]` to `[055]` and is what disappears at Step 21c `[056]` (the digest shows nothing disappearing there); the USB plug ends are on screen until `[052]`; part of the shield is missing from the digest's solid counts. Leaf-level visibility from the raw payload matches the thumbnails and was used for this report.

---

## 7. Relation to the other PMG guides

- `19075-piano_memory_game_pmg-full_build` (51 steps, 117 frames) is the parent. The deconstruction shares its CAD root ("PMG Full 3D Cadasio Build"), its annotation inventory and 16 exact camera poses, so it was made by cloning the build and reversing it. It adds 31 arrows and removes all text.
- `…-part-1` (Steps 1–14: Nano and button wiring), `…-part-2` (11 steps: display, matrix, USB wiring) and `…-part-3` (26 steps: housing and mounting) together equal the full build (14 + 11 + 26 = 51). The deconstruction's housing phase D1–D16 undoes Part 3; its bench phase D17–D23 undoes Parts 2 and 1 in 7 steps.
- The other two deconstruction guides in the study (`19075-lac_deconstruction`, `19075-laser_stem_matrix_lsm_-_deconstruction`) show the same headline pattern in their digests: arrows instead of lead lines (22 and 24 arrow appearances), a high share of auto-advancing frames (31 of 130 and 19 of 69), and few or no labels. They were not read in detail here.
