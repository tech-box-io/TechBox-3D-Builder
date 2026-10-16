# Guide report — `19075-piano_memory_game_pmg-full_build` (PMG, full build)

Sources: `digest/19075-piano_memory_game_pmg-full_build.md|json` (all 117 step blocks read), all 15 contact sheets, ~45 individual thumbs, targeted queries of `cadasio_raw/…full_build.json`, and the digests + raw payloads of PMG Parts 1, 2 and 3. Step indices `[NNN]` are the digest's viewer indices (0–116). Working scripts and crops are in `reports/_work_pmg_full/`.

## 1. Summary

The full build is a 117-step, text-free guide (135 authored steps, 18 hidden) that takes a student from a bare Nano I/O shield to the finished Piano Memory Game: plug the Arduino Nano into the shield, wire four push-button modules, a TM1637 4-digit display and a 32×8 LED dot matrix to it with 21 individual jumper wires, plug in the USB cable, build a 14-piece laser-cut wooden case (panels engraved H1–H14, four piano keys engraved H9), and finally clip the wired electronics into the case. It is one title page, 5 un-numbered section cards (electronics only), 51 numbered `Step N` / `Step Nc` pairs (hover view, then completed view), 8 auto-advancing `Transition` keyframes and one `Completed View`. Every step lasts 800 ms; no step has a description or popup, so all instruction is carried by the 3D model, pin-name labels, red lead lines, a black eye icon and a handful of photo/close-up insets. The guide is the master project from which Parts 1–3 were cloned: Parts 1+2+3 played back to back are the same 115 body steps, renumbered, with three of the six part bookends removed.

## 2. Step table (every viewer step)

Legend: *hover* = `Step N` (part shown away from its seat with guidance), *seated* = `Step Nc` (result). Camera column: `held` = camera identical to the previous step; otherwise the orbit angle, distance change and resulting elevation/azimuth. Screen positions are the stored top-left of the annotation in % of the viewport. Lengths are in mm.

| idx | name | kind | what is added / done | annotations | camera |
|---|---|---|---|---|---|
| [000] | Start | title | Hero render of the finished game (all 88 final parts) on the right half | TechBox logo SVG top-left (2,8)% w 39.5%; title PNG "Piano Memory Game (PMG) / Full Build / © 2026 TechBox…" bottom-left (2,65)% w 46.5%; both unanchored | hero: 320 mm; el 21, az -43 |
| [001] | Nano I/O Module | section card | Everything hidden; Nano I/O expansion shield alone, seen straight down | rectangle label "NANO I/O MODULE LABELS" = photo of the real shield + caption, at (54,17)%, cyan leader to the shield | orbit 69.2 deg, 320->133 mm; el 90, az 90 |
| [002] | Step 1 | step (hover) | Arduino Nano fades in 29.8 mm straight above the shield sockets | 4 red lead lines: Nano corner pins -> end holes of the two 15-pin sockets (25.7-28.7 mm) | orbit 56.4 deg, 133->142 mm; el 34, az -70 |
| [003] | Step 1c | step c (seated) | Nano tweens 29.8 mm down into the sockets (seated) | lines removed | held |
| [004] | Step 2 | step (hover) | Prep: shield + Nano hidden; 12-wire jumper ribbon alone (12 wires, 24 black housings) | eye icon -> ribbon | orbit 28.4 deg, 142->128 mm; el 49, az -37 |
| [005] | Step 2c | step c (seated) | Ribbon fans out into 12 separate wires (each slides 1-17 mm sideways) | none | held |
| [006] | Push Buttons | section card | Ribbon hidden; first push-button module (black cap) alone | photo of real module, red box round VCC/OUT/GND, at (59,19)% w 17%, leader to header pins | orbit 50.0 deg, 128->43 mm; el 17, az -85 |
| [007] | Step 3 | step (hover) | Shield + Nano return; button 1 stays, floating behind the shield. One loose straight red #b70101 wire appears at the parking spot beside/below the shield | labels "VCC" (button 1 (black) pin) + "V4" (shield pin); eye icon -> loose wire | orbit 21.8 deg, 43->173 mm; el 21, az -62 |
| [008] | Step 3c | step c (seated) | Straight wire cross-fades to the routed wire VCC -> V4 (no tween) | labels + eye removed | held |
| [009] | Step 4 | step (hover) | One loose straight white #e4e4e4 wire appears at the parking spot beside/below the shield | labels "OUT" (button 1 pin) + "S4" (shield pin); eye icon -> loose wire | held |
| [010] | Step 4c | step c (seated) | Straight wire cross-fades to the routed wire OUT -> S4 (no tween) | labels + eye removed | held |
| [011] | Step 5 | step (hover) | One loose straight dark-grey #343232 wire appears at the parking spot beside/below the shield | labels "GND" (button 1 pin) + "G4" (shield pin); eye icon -> loose wire | held |
| [012] | Step 5c | step c (seated) | Straight wire cross-fades to the routed wire GND -> G4 (no tween) | labels + eye removed | held |
| [013] | Transition | transition (auto) | Auto: button 2 (yellow cap) fades in beside button 1, already in place | none | held |
| [014] | Step 6 | step (hover) | One loose straight bright-green #21f17a wire appears at the parking spot beside/below the shield | labels "VCC" (button 2 (yellow) pin) + "V5" (shield pin); eye icon -> loose wire | held |
| [015] | Step 6c | step c (seated) | Straight wire cross-fades to the routed wire VCC -> V5 (no tween) | labels + eye removed | held |
| [016] | Step 7 | step (hover) | One loose straight brown #7c5a30 wire appears at the parking spot beside/below the shield | labels "OUT" (button 2 pin) + "S5" (shield pin); eye icon -> loose wire | held |
| [017] | Step 7c | step c (seated) | Straight wire cross-fades to the routed wire OUT -> S5 (no tween) | labels + eye removed | held |
| [018] | Step 8 | step (hover) | One loose straight yellow #ffdc00 wire appears at the parking spot beside/below the shield | labels "GND" (button 2 pin) + "G5" (shield pin); eye icon -> loose wire | held |
| [019] | Step 8c | step c (seated) | Straight wire cross-fades to the routed wire GND -> G5 (no tween) | labels + eye removed | held |
| [020] | Transition | transition (auto) | Auto: button 3 (white cap) fades in, already in place | none | held |
| [021] | Step 9 | step (hover) | One loose straight maroon #85144b wire appears at the parking spot beside/below the shield | labels "VCC" (button 3 (white) pin) + "V6" (shield pin); eye icon -> loose wire | held |
| [022] | Step 9c | step c (seated) | Straight wire cross-fades to the routed wire VCC -> V6 (no tween) | labels + eye removed | held |
| [023] | Step 10 | step (hover) | One loose straight grey #737980 wire appears at the parking spot beside/below the shield | labels "OUT" (button 3 pin) + "S5 (sic - pin is S6)" (shield pin); eye icon -> loose wire | held |
| [024] | Step 10c | step c (seated) | Straight wire cross-fades to the routed wire OUT -> S6 (labelled S5) (no tween) | labels + eye removed | held |
| [025] | Step 11 | step (hover) | One loose straight blue #3876ac wire appears at the parking spot beside/below the shield | labels "GND" (button 3 pin) + "G6" (shield pin); eye icon -> loose wire | held |
| [026] | Step 11c | step c (seated) | Straight wire cross-fades to the routed wire GND -> G6 (no tween) | labels + eye removed | held |
| [027] | Transition | transition (auto) | Auto: button 4 (blue cap) fades in, already in place | none | held |
| [028] | Step 12 | step (hover) | One loose straight orchid #a75294 wire appears at the parking spot beside/below the shield | labels "VCC" (button 4 (blue) pin) + "V7" (shield pin); eye icon -> loose wire | held |
| [029] | Step 12c | step c (seated) | Straight wire cross-fades to the routed wire VCC -> V7 (no tween) | labels + eye removed | held |
| [030] | Step 13 | step (hover) | One loose straight red-orange #ff4136 wire appears at the parking spot beside/below the shield | labels "OUT" (button 4 pin) + "S7" (shield pin); eye icon -> loose wire | held |
| [031] | Step 13c | step c (seated) | Straight wire cross-fades to the routed wire OUT -> S7 (no tween) | labels + eye removed | held |
| [032] | Step 14 | step (hover) | One loose straight teal-green #3d9970 wire appears at the parking spot beside/below the shield | labels "GND" (button 4 pin) + "G7" (shield pin); eye icon -> loose wire | held |
| [033] | Step 14c | step c (seated) | Straight wire cross-fades to the routed wire GND -> G7 (no tween) | labels + eye removed | held |
| [034] | 4-Digit Display | section card | Everything hidden; TM1637 4-digit display alone | photo of the back of the real module, red box round CLK/DIO/VCC/GND, at (52,30)% w 34%, leader to header pins | orbit 15.9 deg, 173->91 mm; el 12, az -75 |
| [035] | Step 15 | step (hover) | Prep: display hidden; 9-wire jumper ribbon alone | none (no eye icon - Step 2 has one) | orbit 41.6 deg, 91->103 mm; el 49, az -53 |
| [036] | Step 15c | step c (seated) | Ribbon fans out into 9 separate wires (each slides 1-12 mm) | none | held |
| [037] | Step 16 | step (hover) | Wired sub-assembly returns with the display floating upper-left. One loose straight gold #ac9400 wire appears at the parking spot beside/below the shield | labels "clk" (4-digit display pin) + "s8" (shield pin); eye icon -> loose wire | orbit 27.7 deg, 103->173 mm; el 25, az -72 |
| [038] | Step 16c | step c (seated) | Straight wire cross-fades to the routed wire clk -> s8 (no tween) | labels + eye removed | held |
| [039] | Step 17 | step (hover) | One loose straight black #000000 wire appears at the parking spot beside/below the shield | labels "dio" (4-digit display pin) + "s9" (shield pin); eye icon -> loose wire | held |
| [040] | Step 17c | step c (seated) | Straight wire cross-fades to the routed wire dio -> s9 (no tween) | labels + eye removed | held |
| [041] | Step 18 | step (hover) | One loose straight violet #ab53ca wire appears at the parking spot beside/below the shield | labels "VCC" (4-digit display pin) + "V9" (shield pin); eye icon -> loose wire | held |
| [042] | Step 18c | step c (seated) | Straight wire cross-fades to the routed wire VCC -> V9 (no tween) | labels + eye removed | held |
| [043] | Step 19 | step (hover) | One loose straight red #bb3d3d wire appears at the parking spot beside/below the shield | labels "GND" (4-digit display pin) + "G9" (shield pin); eye icon -> loose wire | held |
| [044] | Step 19c | step c (seated) | Straight wire cross-fades to the routed wire GND -> G9 (no tween) | labels + eye removed | held |
| [045] | Dot Matrix Display | section card | Everything hidden; 32x8 LED dot-matrix alone | photo of the back of the real matrix, red box round the input header, at (7,15)% w 37%, leader to header pins | orbit 25.4 deg, 173->236 mm; el 12, az -95 |
| [046] | Step 20 | step (hover) | Wired sub-assembly returns with the matrix floating at right. One loose straight dark-brown #411900 wire appears at the parking spot beside/below the shield | labels "VCC" (dot matrix pin) + "V11" (shield pin); eye icon -> loose wire | orbit 22.2 deg, 236->202 mm; el 30, az -81 |
| [047] | Step 20c | step c (seated) | Straight wire cross-fades to the routed wire VCC -> V11 (no tween) | labels + eye removed | held |
| [048] | Step 21 | step (hover) | One loose straight green #339f3f wire appears at the parking spot beside/below the shield | labels "GND" (dot matrix pin) + "G11" (shield pin); eye icon -> loose wire | held |
| [049] | Step 21c | step c (seated) | Straight wire cross-fades to the routed wire GND -> G11 (no tween) | labels + eye removed | held |
| [050] | Step 22 | step (hover) | One loose straight navy #2a2f62 wire appears at the parking spot beside/below the shield | labels "DIN" (dot matrix pin) + "S11" (shield pin); eye icon -> loose wire | held |
| [051] | Step 22c | step c (seated) | Straight wire cross-fades to the routed wire DIN -> S11 (no tween) | labels + eye removed | held |
| [052] | Step 23 | step (hover) | One loose straight maroon #662639 wire appears at the parking spot beside/below the shield | labels "CS" (dot matrix pin) + "S12" (shield pin); eye icon -> loose wire | held |
| [053] | Step 23c | step c (seated) | Straight wire cross-fades to the routed wire CS -> S12 (no tween) | labels + eye removed | held |
| [054] | Step 24 | step (hover) | One loose straight teal #377e89 wire appears at the parking spot beside/below the shield | labels "CLK" (dot matrix pin) + "S13" (shield pin); eye icon -> loose wire | held |
| [055] | Step 24c | step c (seated) | Straight wire cross-fades to the routed wire CLK -> S13 (no tween) | labels + eye removed | held |
| [056] | USB Cable | section card | Everything hidden; USB cable (USB-A to right-angle mini-USB) alone | none | orbit 96.6 deg, 202->202 mm; el 38, az 47 |
| [057] | Step 25 | step (hover) | Wired sub-assembly returns, seen from behind; cable plug 23 mm short of the Nano USB socket | 1 red lead line: plug tip -> Nano mini-USB socket (28.5 mm) | orbit 39.6 deg, 202->275 mm; el 23, az 90 |
| [058] | Step 25c | step c (seated) | Cable tweens 22.9 mm into the socket | line removed | held |
| [059] | Step 26 | step (hover) | All electronics hidden. Case starts: H1 (front rail) in place, H2 (side) 40 mm away | 1 lead line: H2 front tab -> H1 slot (36.6 mm) | orbit 109.7 deg, 275->275 mm; el 36, az -50 |
| [060] | Step 26c | step c (seated) | H2 tweens 40 mm onto H1 (seated) | line removed | held |
| [061] | Step 27 | step (hover) | H3 (other side) 43 mm away | 1 lead line: H3 front tab -> H1 slot (39.8 mm) | orbit 64.8 deg, 275->275 mm; el 40, az -136 |
| [062] | Step 27c | step c (seated) | H3 tweens 43 mm onto H1 | line removed | held |
| [063] | Step 28 | step (hover) | H4 (back panel) 65 mm behind the frame | 4 lead lines: 2 tabs on H2 + 2 tabs on H3 -> 4 slots in H4 (61.5 mm) | orbit 103.0 deg, 275->374 mm; el 36, az 34 |
| [064] | Step 28c | step c (seated) | H4 tweens 65 mm onto the four tabs | lines removed | held |
| [065] | Step 29 | step (hover) | Frame now shown upside-down (scene up-axis flips to -y). H5 (deck plate with 4 button apertures) 140 mm away | 2 lead lines: H5 edge tabs -> windows in H2 (118 mm) | orbit 100.2 deg, 374->374 mm; el -34, az -42 |
| [066] | Step 29c | step c (seated) | Leg 1: H5 tweens 117 mm to a tilted, half-inserted pose (not yet seated) | lines removed | held |
| [067] | Step 30 | step (hover) | No new part; same H5 seen from the other side | 2 lead lines: H5 free edge -> notches in H3 (57 mm) | orbit 67.7 deg, 374->275 mm; el -45, az -134 |
| [068] | Step 30c | step c (seated) | Leg 2: H5 drops 56 mm and rotates flat (seated) | lines removed | held |
| [069] | Step 31 | step (hover) | H6 (button carrier plate that sits under the deck) 136 mm away | 2 lead lines: H6 tabs -> slots in H5 (122.5 mm) | orbit 70.6 deg, 275->320 mm; el -28, az -44 |
| [070] | Step 31c | step c (seated) | Leg 1: H6 tweens 122 mm to a tilted pose | lines removed | held |
| [071] | Step 32 | step (hover) | No new part | 2 lead lines: H6 free edge -> H5 (44 mm) | orbit 67.1 deg, 320->236 mm; el -23, az -119 |
| [072] | Step 32c | step c (seated) | Leg 2: H6 drops 43 mm and rotates flat (seated) | lines removed | held |
| [073] | Step 33 | step (hover) | Wired electronics reappear, loose beside the upside-down case | 2 eye icons: one -> blue button (module to move), one -> its slot in H6 | orbit 54.6 deg, 236->275 mm; el -40, az 179 |
| [074] | Step 33c | step c (seated) | Blue button + its 3 wires cross-fade into the first slot (re-routed copies, no tween) | rendered close-up inset with red box showing the module clipped in, at (23,6)% w 17.5%, leader to the module; eyes removed | held |
| [075] | Step 34 | step (hover) | Nothing moves | eye icon -> next (yellow) button; inset removed | held |
| [076] | Step 34c | step c (seated) | Batch: remaining 3 buttons + 9 wires cross-fade into their slots | eye removed | held |
| [077] | Step 35 | step (hover) | H7 (bottom cover) 139 mm away | 2 lead lines: H7 tabs -> slots in H6 (139 mm) | orbit 102.1 deg, 275->320 mm; el -24, az -49 |
| [078] | Step 35c | step c (seated) | Leg 1: H7 tweens 139 mm to a tilted pose | lines removed | held |
| [079] | Step 36 | step (hover) | No new part | 2 lead lines: H7 free edge -> H6 (28.6 mm) | orbit 85.1 deg, 320->320 mm; el -35, az -151 |
| [080] | Step 36c | step c (seated) | Leg 2: H7 hinges down (about 1 mm + rotation) (seated) | lines removed | held |
| [081] | Step 37 | step (hover) | Case upright again (up-axis back to +y). H8 (cross divider, 4 slots) 94.5 mm above | 2 lead lines: H8 bottom tabs -> slots in the deck H5 (94.6 mm) | orbit 121.6 deg, 320->320 mm; el 30, az -41 |
| [082] | Step 37c | step c (seated) | H8 tweens 94.5 mm down | lines removed | held |
| [083] | Step 38 | step (hover) | First piano key (engraved H9) 108 mm in front | 1 lead line: key tip -> slot in back panel H4 (104 mm) | orbit 17.1 deg, 320->275 mm; el 36, az -22 |
| [084] | Step 38c | step c (seated) | Key tweens 108 mm through H8 into H4 | rendered close-up inset with red box showing the key tip hooked through H4 (stored at (60,30)% w 13%; saved render shows it upper-left), leader to key tip | held |
| [085] | Step 39 | step (hover) | Nothing moves | inset swapped for flat outline of H9 + "3x", stored at (53,27)% w 15.8%, leader to the next slot in H8 | held |
| [086] | Step 39c | step c (seated) | Batch: the other 3 keys fade in already seated (no tween) | inset removed | held |
| [087] | Step 40 | step (hover) | H10 (upper deck) 127 mm in front, 26 mm high | 2 lead lines: H10 rear tabs -> slots in H4 (116 mm) | orbit 50.7 deg, 275->275 mm; el 26, az 37 |
| [088] | Step 40c | step c (seated) | Leg 1: H10 tweens 126 mm, stopping 9 mm high | lines removed | held |
| [089] | Step 41 | step (hover) | No new part | 2 short lead lines: H10 -> H2 and H3 (8.7 mm) | orbit 62.5 deg, 275->275 mm; el 13, az -29 |
| [090] | Step 41c | step c (seated) | Leg 2: H10 drops 9 mm and rotates flat (seated) | lines removed | held |
| [091] | Step 42 | step (hover) | H11 (left display bracket) 54 mm above the deck | 1 lead line: H11 tab -> slot in H10 (50 mm) | orbit 31.1 deg, 275->275 mm; el 40, az -12 |
| [092] | Transition | transition (auto) | Auto: H11 tweens 53 mm down into the slot | line removed | held |
| [093] | Step 42c | step c (seated) | H11 tweens 6.7 mm sideways to lock (seated) | none | held |
| [094] | Step 43 | step (hover) | H12 (right display bracket) 45 mm above the deck | 1 lead line: H12 tab -> slot in H10 (41 mm) | orbit 98.9 deg, 275->236 mm; el 37, az -167 |
| [095] | Transition | transition (auto) | Auto: H12 tweens 44.5 mm down | line removed | held |
| [096] | Step 43c | step c (seated) | H12 tweens 7.6 mm sideways to lock (seated) | none | held |
| [097] | Step 44 | step (hover) | H13 (rear brace) 80 mm away | 4 lead lines: 2 between H13 and brackets H11/H12 (82 mm) + 2 H13 -> H4 (68 mm) | orbit 48.1 deg, 236->275 mm; el 40, az 130 |
| [098] | Step 44c | step c (seated) | H13 tweens 80 mm (seated) | lines removed | held |
| [099] | Step 45 | step (hover) | Nothing moves | eye icon -> Nano I/O shield lying loose beside the case | orbit 13.1 deg, 275->374 mm; el 28, az 135 |
| [100] | Step 45c | step c (seated) | Whole wired cluster (shield, Nano, 21 wires, USB cable) cross-fades to a pre-posed copy held above the back panel | none | held |
| [101] | Step 46 | step (hover) | Nothing moves | 1 red straight ARROW (80 mm) pointing down from the shield to back panel H4 - the only arrow in the guide | orbit 76.5 deg, 374->436 mm; el 29, az 45 |
| [102] | Step 46c | step c (seated) | Cluster cross-fades to the copy mounted on H4 | arrow removed | held |
| [103] | Step 47 | step (hover) | Nothing moves | eye icon -> loose 4-digit display | orbit 37.3 deg, 436->320 mm; el 41, az 89 |
| [104] | Step 47c | step c (seated) | Display + its 4 wires cross-fade to a copy held above the brackets | eye removed | held |
| [105] | Step 48 | step (hover) | Nothing moves | 2 lead lines: display PCB -> notches in H11 and H12 (12 mm) | orbit 83.4 deg, 320->236 mm; el 34, az -25 |
| [106] | Transition | transition (auto) | Auto: display cross-fades to an intermediate pose | first 2 lines replaced by 2 new ones for the second leg (9.5 mm) | held |
| [107] | Step 48c | step c (seated) | Display cross-fades to the seated copy | lines removed | held |
| [108] | Step 49 | step (hover) | Nothing moves | eye icon -> loose LED matrix | orbit 34.7 deg, 236->320 mm; el 38, az -68 |
| [109] | Step 49c | step c (seated) | Matrix + its 5 wires cross-fade to a copy held in front of the brackets | eye removed | held |
| [110] | Step 50 | step (hover) | Nothing moves | 2 lead lines: bracket hooks (H11, H12) -> matrix PCB (21 mm) | orbit 95.6 deg, 320->275 mm; el 14, az -177 |
| [111] | Transition | transition (auto) | Auto: matrix cross-fades to an intermediate pose | first 2 lines replaced by 2 new ones (10.8 mm) | held |
| [112] | Step 50c | step c (seated) | Matrix cross-fades to the seated copy | lines removed | held |
| [113] | Step 51 | step (hover) | H14 (face plate with display window) about 58 mm up/back from its seat | 2 lead lines: H14 -> top edge of the matrix PCB (58.5 mm); eye icon -> same edge | orbit 21.6 deg, 275->374 mm; el 36, az -172 |
| [114] | Transition | transition (auto) | Auto: H14 tweens 58 mm down | eye + first lines removed; 2 new short lines H14 <-> H11/H12 (8 mm) | held |
| [115] | Step 51c | step c (seated) | H14 nudges 2 mm and rotates onto the brackets | 2 lead lines still flagged visible (not noticeable in the render) | held |
| [116] | Completed View | completed | Final hero view of the finished game (H14 settles 2 mm) | all annotations removed | orbit 84.8 deg, 374->320 mm; el 35, az -61 |

## 3. Conventions found (with evidence and exceptions)

### 3.1 Structure

1. **Fixed skeleton.** `Start` → [`section card` →] `Step N` / `Step Nc` pairs → `Completed View`. Counts: 1 title, 5 cards, 51 `Step N`, 51 `Step Nc` (every N has its c: 51/51), 8 `Transition`, 1 `Completed View` = 117. Always true in this guide.
2. **One continuous number line.** Numbers run 1–51 without gaps across all three former parts. Cards, Transitions, Start and Completed View carry no number and do not consume one. The `c` suffix always means "completed state of the same number".
3. **No prose.** `description` is empty on 117/117 steps and `popupType` is `none` on 117/117. The only words on screen are pin names (42 labels), one photo caption ("NANO I/O MODULE LABELS"), "3x" inside one inset, the engraved part IDs on the wooden parts, and the title page.
4. **Section cards introduce a new electronic component before it is used** ([001] Nano I/O Module, [006] Push Buttons, [034] 4-Digit Display, [045] Dot Matrix Display, [056] USB Cable). On a card everything else is hidden and the component is shown alone (1 component on screen in 5/5); 4/5 pair it with a photo of the real board in a cyan-framed inset with a red rectangle round the pin names; the camera always moves to frame it (5/5). Exceptions: the USB Cable card has no annotation at all; there are no cards in the case section (Steps 26–51) — wooden parts are identified only by their engraved IDs.
5. **Uniform timing.** `animationDuration` = 800 ms on all 135 authored steps; show/hide = fade, move = tween, camera = tween (speed 2, no orbit animation); annotations fade separately from parts.
6. **Transition = auto-advancing keyframe.** All 8 are `play` (the other 109 are `pause`), never move the camera (0/8) and carry no step number. 7/8 are also hidden from the step picker with the overlay off ([114] is not — see anomalies). Two uses: (a) fade the next identical module into place between wire groups ([013], [020], [027]); (b) the middle keyframe of a two-leg seat ([092], [095], [106], [111], [114]).
7. **Hidden housekeeping steps.** A hidden first step sets the global look (toon style + normal edges on 5,367 solids, wood colour on the H parts); two hidden steps sit at the Part 2 → Part 3 seam; ten hidden legacy steps are parked after `Completed View`. The viewer never shows them.

### 3.2 Granularity

1. **One jumper wire per numbered step — never grouped.** 21 wires = 21 step pairs (Steps 3–14, 16–19, 20–24). Always true.
2. **One new part per numbered step.** 35 of 51 steps introduce exactly one new part (the 21 wires plus 14 rigid parts: Nano, USB cable, H3, H4, H5, H6, H7, H8, first key, H10, H11, H12, H13, H14). The other 16 are: Step 26 (two parts — the base H1 plus the first mover H2), Steps 2 and 15 (ribbon prep, 12 and 9 wires), Steps 30, 32, 36, 41 (second leg of the previous part), Steps 33, 34, 45–50 (repositioning already-wired modules), Step 39 (three keys at once).
3. **Batching only for exact repeats, and only after the first instance has been shown alone.** Button into its slot: one (Step 33/33c, with a close-up inset), then the other three in one step (Step 34/34c, cued by an eye icon). Piano key: one (Step 38/38c, with lead line and close-up), then three in one step (Step 39/39c, cued by a "3x" inset). Nothing else is batched.
4. **Ribbon-prep steps are sized to the next wiring block.** Step 2 shows a 12-wire ribbon (4 buttons × 3 pins), Step 15 a 9-wire ribbon (4 display + 5 matrix); the `c` step fans the ribbon into separate wires.
5. **A two-leg insertion costs either two numbered steps or one step plus a Transition.** Two numbered steps when the second leg needs a different viewpoint (H5: 29/30, H6: 31/32, H7: 35/36, H10: 40/41 — the camera orbits 62–85° between legs); one step with a Transition in the middle when the view can stay (H11: [091]–[093], H12: [094]–[096], display: [105]–[107], matrix: [110]–[112], H14: [113]–[115]).
6. **Moving an already-wired module is split into "look at it" and "place it".** Steps 45/46 (shield), 47/48 (display), 49/50 (matrix): the first pair picks the module up, the second seats it.

### 3.3 Ordering

1. **Electronics on the bench first, then the case, then electronics into the case.** Steps 1–25 wire everything loose; 26–32 build the frame and deck; 33–51 interleave installing electronics (33–34 buttons, 45–46 shield, 47–48 display, 49–50 matrix) with the remaining panels.
2. **Wires follow the module's header pin order, not "power first".** Buttons: VCC, OUT, GND (×4). Display: CLK, DIO, VCC, GND. Matrix: VCC, GND, DIN, CS, CLK. Each sequence matches the pin order printed on the photo of the card.
3. **Modules are wired in ascending shield pin number.** D4, D5, D6, D7 (buttons black, yellow, white, blue), D8/D9 (display), D11–D13 (matrix).
4. **Case goes outside-in and bottom-up.** Front rail + sides (26–27), back (28), flip, deck and button plates (29–32), buttons (33–34), bottom cover (35–36), flip back, divider (37), keys (38–39), upper deck (40–41), brackets (42–43), brace (44), shield (45–46), display (47–48), matrix (49–50), face plate (51).
5. Exception / inconsistency: ribbon prep comes *before* the card for the buttons (Step 2, then "Push Buttons") but *after* the card for the display ("4-Digit Display", then Step 15), so the display is shown, hidden for two steps, then shown again.

### 3.4 Motion

1. **Rigid parts: fade in at a hover pose, then tween straight to the seat.** `Step N` fades the part in displaced along its insertion axis; `Step Nc` tweens it home in 800 ms. Hover distances: Nano 29.8 mm straight up; USB plug 22.9 mm; case panels and keys 40–140 mm (H2 40, H3 43, H12 45, H11 54, H14 58, H4 65, H13 80, H8 94.5, key 108, H10 127, H6 136, H7 139, H5 140). Applies to the Nano, the USB plug, H2–H8, H10–H14 and the first key (15 parts).
2. **Wires are never tweened.** In `Step N` the wire appears loose and straight, lying flat at a parking spot in the lower part of the frame beside the shield (not hovering over its pins); in `Step Nc` it is replaced by a different, routed wire model by cross-fade (APPEAR + DISAPPEAR in the same step, no MOVE). 21/21 wire steps.
3. **Wired modules are never tweened either.** Buttons going into the case, the shield, the display and the matrix each exist as 2–3 pre-posed copies with re-routed wires; the guide cross-fades between copies ([074], [076], [100], [102], [104], [106], [107], [109], [111], [112]).
4. **Two-leg seats are translate-then-drop.** Leg 1 is a long straight slide (117–139 mm for H5/H6/H7, 126 mm for H10, 44–58 mm for H11/H12/H14); leg 2 is a short drop or lock (56, 43, ~1, 9, 6.7, 7.6, 2 mm), with a small rotation in 5 of 7 cases (H5, H6, H7, H10, H14).
5. **Modules being wired float at fixed positions around the shield** (buttons in a row behind it, display upper-left, matrix to the right); they fade in "already in place" and do not move until the case section.
6. **Repeat instances appear without motion.** The three extra keys ([086]) and the next button modules ([013], [020], [027]) simply fade in seated.

### 3.5 Red lead lines and the arrow

1. **Style.** Solid red `#ff0000`, straight, no arrowhead, anchored in 3D at both ends. 48 lines in total: 42 switched on in 21 `Step N` steps and 6 in 3 Transitions.
2. **Count = number of visible mating-feature pairs: 1, 2 or 4.** One line in 6 steps (USB plug, H2, H3, first key, H11, H12); two lines in 12 steps and all 3 Transitions; four lines in 3 steps (Nano's four corner pins, H4's four tabs, H13's four joints). Never 3, never more than 4.
3. **Endpoints are the mating features themselves.** Pin tip → socket hole (Nano), plug tip → USB socket, tab → slot (all panels), key tip → slot in the back panel, PCB edge → bracket notch (display, matrix). Which end is stored first is not consistent (11 of the 48 lines are stored target-first, e.g. all four at [063] and both at [110]), which does not matter because there is no arrowhead.
4. **Length = travel of that leg.** Line length / tween distance is 0.85–1.02 for every tweened leg (e.g. 36.6 vs 40.0, 61.5 vs 65.0, 94.6 vs 94.5, 104.3 vs 107.7, 139.1 vs 139.4): the line spans exactly the gap between the two features and is parallel to the motion. Exceptions: USB plug, 28.5 mm line for a 22.9 mm move (1.24); H7 leg 2, 28.6 mm line for a hinge-down that translates only ~1 mm.
5. **Lifetime = one step.** Every set of lines is removed at the following `c` step or replaced by a new set at the following Transition (21/21 hover sets, 2/3 Transition sets). Exception: the set created at [114] is still flagged visible at [115] Step 51c.
6. **Never used for wires** (0 of 21 wire steps) — a wire's two ends are identified by labels instead.
7. **One arrow in the whole guide** ([101] Step 46): red, straight, 80 mm, pointing down from the lifted shield to the back panel. It stands in for lead lines when the thing being moved is a cross-faded wired module rather than a tweened part.

### 3.6 Labels and callouts

1. **Every wire step has exactly two text labels and one eye icon** (21/21). One label names the pin on the module (VCC/OUT/GND, CLK/DIO, DIN/CS), the other the pin on the shield (V4/S4/G4 … S13). The text is the board silkscreen, nothing else.
2. **Label style.** Bold black text at 3em (37 of the 42 pin labels are identical in every stored style attribute; the other 5 differ only by a missing leader-colour value and render the same), sitting on a light-cyan `#7fdbff` underline that continues as a leader to a small dashed ring on the pin. No box, no fill.
3. **Labels sit in white space beside the model, never on it,** and stay in roughly the same place through a block: button block — module-pin label x 51–67 %, y 25–34 %; shield-pin label x 56–65 %, y 41–52 %; eye x 24–30 %, y 43–50 %. Display block — module label top-left (21–24 %, 17–18 %), shield label right (58–61 %, 41–42 %), eye below (28–45 %, 52–61 %). Matrix block — shield label lower-left (18–23 %, 48–52 %), module label top (43–64 %, 12–19 %), eye bottom (32–38 %, 59–63 %).
4. **Labels live for the hover step only** (removed on every `c` step, 42/42).
5. **No part-name labels.** Wooden parts are identified by IDs engraved in the model (H1…H14; the keys read H9) and electronic modules by their section card.
6. **Eye icon = "this is the thing to pick up / look at".** Black eye PNG, 8.2 % of viewport width, cyan leader. 29 icons on 28 steps: the loose wire in all 21 wire steps, the ribbon in Step 2, the button and its destination slot in Step 33 (two eyes), the next button in Step 34, the shield in Step 45, the display in Step 47, the matrix in Step 49, the mating edge in Step 51. It is used exactly where there is no hover-to-seat tween to show what moves, always on `Step N`, never on `Nc`.
7. **Image insets.** (a) Photos of the real board on cards, red rectangle round the pin names (3 images + 1 photo-in-label). (b) Rendered close-ups shown on the *completed* step to prove the locking detail — button clipped into its slot [074], key tip hooked through the back panel [084] — again with a red rectangle. (c) A flat part outline with "3x" for "repeat three more times" [085]. All insets have a thin rounded cyan frame and a cyan leader to the feature; widths 13–37 % of the viewport.
8. **Title page.** Logo top-left at (2, 8) %, 39.5 % wide; title/subtitle/copyright block bottom-left at (2, 65) %, 46.5 % wide; product hero on the right half. Both overlays are unanchored images.

### 3.7 Camera

1. **The camera only moves on Start, cards, `Step N` and Completed View — never on `Step Nc` (0/51) and never on a Transition (0/8).** The hover → seat animation therefore always plays from a fixed viewpoint.
2. **During wiring the camera is set once per module block and then held.** [007]–[033]: one view (173 mm, elevation 21°, azimuth −62°) for all 12 button wires, 27 consecutive steps. [037]–[044]: one view (173 mm, 25°, −72°) for the 4 display wires. [046]–[055]: one view (202 mm, 30°, −81°) for the 5 matrix wires. Only the first wire of each block (Steps 3, 16, 20) moves the camera.
3. **In the case section the camera is re-aimed for almost every step.** 24 of the 26 `Step N` from 26 to 51 move it (all but Steps 34 and 39, which only add a cue), with a median orbit of 67° and a maximum of 122°, so that the tabs and slots being joined face the viewer.
4. **Framing is the whole sub-assembly, centred, with white margins left for labels.** There is no close zoom on a single pin or tab; detail is given by labels and insets instead. Distances: cards 43–236 mm, wiring 173–202 mm, case 236–436 mm, hero 320 mm. Zoom changes between consecutive build steps are small (×0.74–×1.36); bigger jumps happen only when entering or leaving a card or ribbon close-up (e.g. ×0.25 at Step 3, ×0.6 at Step 16).
5. **Perspective, FOV 45°, three-quarter views from above.** In the upright sections the elevation is 12–49° above the horizon (median 28.5°); straight-down 90° is used once, for the shield card [001]. The guide uses 38 distinct viewpoints over 117 steps.
6. **Working on the underside flips the scene's up-axis rather than rotating the model.** Steps 29–36 ([065]–[080]) set `up_axis` to −y (camera elevations −23° to −45°, engraved IDs read upside-down); Step 37 [081] sets it back to +y.

### 3.8 Look

White background (`#ffffff`), every solid drawn with toon (flat cel) shading and thin black edges, no silhouette outline, perspective camera, view cube on, navigation bar along the bottom. The look is set per part by overrides in a hidden first step, not by the scene (scene render style stays `matt`, scene edges `none`).

| Part | Look in the renders |
|---|---|
| Nano I/O shield | royal-blue PCB `#224bbe`; pale-yellow pin-header blocks `#ffff80` with light-grey pins; two black 15-pin sockets and black DC jack `#191919`; small grey/white SMD parts |
| Arduino Nano | navy PCB `#000f41`, light-grey pins and components `#e4e4e4`, black chip and headers, white/grey mini-USB socket |
| Push-button modules | navy board `#000f41`, black switch body, three light-grey right-angle pins, large round caps: black, yellow `#ffdc00`, white, blue `#0074d9` (one colour per button) |
| 4-digit display | royal-blue PCB, black display face, white segments, four light-grey pins |
| LED dot matrix | royal-blue PCB `#234bbf`, four white module bodies `#e4e4e4` with black faces and white dots, light-grey header pins |
| Jumper wires | 21 different saturated colours (red, white, dark grey, bright green, brown, yellow, maroon, grey, blue, orchid, red-orange, teal-green, gold, black, violet, red, dark brown, green, navy, maroon, teal); colour follows ribbon position, not signal (GND is red on the display, VCC is dark brown on the matrix) |
| Wire end housings | black `#000000` Dupont housings on both ends of every wire; ribbon ends drawn as one black block |
| USB cable | very dark brown-black cable and plug bodies `#1e1616`, light-grey metal shells |
| Wooden case panels and keys | tan `#deb887` with lighter cream lit faces (two-tone under toon shading), black edges, part IDs engraved in dark brown-black `#1e1616` |
| Annotations | red `#ff0000` lead lines and arrow; light-cyan `#7fdbff` leaders, underlines and inset frames; black bold label text; black eye icon; red rectangles inside insets |

## 4. Anomalies (typos and inconsistencies — not conventions)

1. **Wrong pin label.** Step 10 [023] labels the shield pin "S5"; the wire is the third button's OUT and its neighbours are V6 [021] and G6 [025], so it should read "S6". "S5" is therefore used twice ([016] and [023]) and "S6" never.
2. **Mixed letter case.** "clk" / "s8" [037] and "dio" / "s9" [039] are lower-case; every other pin label is upper-case, including "VCC" / "V9" and "GND" / "G9" in the same block and "CLK" / "CS" / "DIN" in the matrix block.
3. **Missing eye icon.** Step 15 [035] (9-wire ribbon) has no annotation, whereas the equivalent Step 2 [004] has an eye icon. It is the only `Step N` in the guide with nothing on it; the toolbox holds 30 eye icons and only 29 are ever shown.
4. **Unused toolbox items.** Two labels reading "cs" (lower-case), one arrow and one eye icon are never made visible.
5. **Inconsistent Transition flags.** [114] is the only Transition with `hideInStepPicker = false` and `overlayVisible = true`; the other seven are hidden from the picker.
6. **Lead lines left on in a completed step.** [115] Step 51c keeps 2 lead lines flagged visible (they are not noticeable in the render); they are only removed at Completed View. It is the only `c` step with lines.
7. **Colour slip on a pre-posed copy.** In [100] and [101] the Nano's PCB renders teal-green instead of navy; it is navy again from [102].
8. **Inset positions that disagree with the saved render.** The stored positions of the insets on [084] (60, 30) % and [085] (53, 27) % would put them over the model; the saved renders of both steps show them upper-left (about (18, 3) % and (16, 10) %), close to where Part 3 stores them ((19, 7) % and (16, 11) %). The position is a property of the annotation, not of the step, so it was probably dragged later without the thumbnail being re-saved; which one the live viewer shows could not be confirmed from the data.
9. **Card / prep order differs between blocks** (see 3.3.5).
10. **USB lead line longer than the move** (28.5 mm vs 22.9 mm) — the only line that overshoots its travel by more than 2 %.
11. **Inconsistent leader data.** Five labels store no leader colour ("V5" [014], "G7" [032], "V11" and "VCC" [046], "DIN" [050]) although they render with the same cyan leader as the rest; label anchors also land on different sub-parts for equivalent pins (e.g. "G9" [043] sits on the V-row strip), i.e. they were placed by eye.
12. **Two names for the same icon.** 27 annotations are called "new eye" and 3 "Eye" ([103], [108], plus the unused one); same PNG, same size.
13. **Project title.** The project is named "Piano Memory Game(PMG) Updated " (no space before the bracket, trailing space, leftover "Updated"), while its own title page reads "Piano Memory Game (PMG) / Full Build". The guide id uses underscores (`piano_memory_game_pmg-full_build`) where the three parts use hyphens.
14. **Not student-facing, but visible in the data.** A wire component is named "S1 to DIN" although it goes to S11; tooltips are enabled project-wide but every part's tooltip is the default "Description / none".
15. **Digest caveats for this guide.** The digest never reports the 4-digit display (`Display TM1637-4`), the two USB plug bodies or 65 of the shield's solids as visible, because a parent node carries a hidden flag while the leaf solids are shown; the renders show them (the display is on screen at [034], [037]–[044], [046]–[055], [057]–[058] and [073]–[103]). "Still displaced" for the shield (10 solids) and for H14 at the end is a CAD-pose quirk, not a part left unseated.

## 5. Relation to Parts 1, 2 and 3

**Lineage.** The full build is the original project (created 2026-05-20). Parts 1, 2 and 3 were cloned from it within 40 minutes on 2026-08-07 (08:20, 08:39, 08:59 UTC) and trimmed. All four share the same CAD model and version, the same annotation IDs and an identical toolbox inventory (38 images, 45 labels, 2 arrows, 48 lead lines), so each part still carries the other parts' unused annotations.

**Arithmetic.** Parts: 34 + 27 + 59 = 120 viewer steps. Full build: 117 = 1 Start + 33 (Part 1 body) + 25 (Part 2 body) + 57 (Part 3 body) + 1 Completed View. The three steps that disappear are Part 1's Start, Part 2's Start and Part 2's Completed View.

| Full build | Comes from | Renumbering | Notes |
|---|---|---|---|
| [000] Start | Part 3 [000] Start | — | Same camera (320 mm, 21°, −43°) and same finished-product hero; only the subtitle image differs ("Full Build" instead of "Part 3"). Part 1's and Part 2's title pages (their own end-state heroes at 148 mm and 436 mm) are dropped. |
| [001]–[032] Nano I/O Module … Step 14 | Part 1 [001]–[032] | none (Steps 1–14) | Identical except the position of the "NANO I/O MODULE LABELS" photo label: (54, 17) % vs (50, 13) %. |
| [033] Step 14c | Part 1 [033] **Completed View** | renamed | Identical content and camera. Part 1 has no Step 14c: its last completed step is simply named "Completed View" (no extra hero orbit). The full build gives it back its ordinary name. |
| [034]–[058] 4-Digit Display … Step 25c | Part 2 [001]–[025] | Step n → Step n + 14 (1–11 → 15–25) | Identical except the first card: camera (91 mm, 12°, −75°) vs (91 mm, 3°, −91°), photo inset at (52, 30) % vs (56, 31) %. Card names are unchanged. |
| — | Part 2 [026] Completed View | dropped | A pure camera orbit (119°, to 275 mm / 37° / −82°) with no part change. |
| — | Part 3 [000] Start | reused as [000] | See first row. |
| [059]–[115] Step 26 … Step 51c | Part 3 [001]–[057] | Step n → Step n + 25 (1–26 → 26–51) | Identical except three inset positions: [074] (23, 6) % vs (23, 4) %; [084] (60, 30) % vs (19, 7) %; [085] (53, 27) % vs (16, 11) %. The five Transitions keep their places. |
| [116] Completed View | Part 3 [058] Completed View | — | Identical (orbit 84.8°, 374 → 320 mm, 35°, −61°). |

**Step-for-step identity.** Comparing every aligned pair of digest records (parts appearing/disappearing, moves, rotations, annotations with their text, anchors and positions, camera, visible-part counts): 84 of 117 are identical in every field. Of the other 33, only 7 are real differences (the rows above: [000], [001], [034], [059], [074], [084], [085]); 4 are knock-ons of those (the next step removes the repositioned annotation or starts from the changed camera: [002], [035], [075], [086]); the remaining 22 (within [073]–[099]) differ only in the digest's bookkeeping of the USB cable's offset, explained below. The saved renders agree: of the 59 full-build frames that map to Part 3 ([000] and [059]–[116]), 55 are pixel-near-identical to Part 3's (under 0.4 % of pixels differ) and the 4 that differ are exactly [000], [074], [084], [085].

**Seams.**
- *Part 1 → Part 2* ([033] → [034]): no bookend in between. The 42 wired button parts fade out and the display card fades in alone; the camera rotates 15.9° and zooms ×1.9 (173 → 91 mm). Because Part 2 opens with a section card, the join reads naturally.
- *Part 2 → Part 3* ([058] → [059]): no bookend and no card. From the rear view of the wired electronics (275 mm, 23°, 90°) the camera orbits 109.7° at unchanged distance, all electronics fade out and H1 + H2 fade in with H2 already in its hover pose. Two hidden authoring steps ("Step 68", "Step 61") sit here in the full build to reset state; Part 3 does not have them. In Part 3 the same step is entered from the hero (H2 tweens out of the finished model instead of fading in).
- The hidden step before "USB Cable" ("Step 73") exists in both the full build and Part 2; a hidden "Step 107" before Step 51 and a hidden duplicate "Step 51c" before Completed View exist only in the full build.

**State carried across the seam.** In the full build the USB cable's plugged-in offset is set at Step 25c [058] and simply persists when the electronics return at Step 33 [073]. Part 3 has no step that sets it (the steps that did were deleted with Part 2), so its digest shows the cable at the CAD pose from its Step 8 to Step 20, although Part 3's saved renders look the same as the full build's. The full build is the self-consistent version; the parts depend on state being re-keyed on their Start page (Part 2's Start does set it; Part 3's does not).

**Other differences between the projects.** Parts 1 and 2 dropped the ten hidden legacy steps parked after Completed View; Part 3 and the full build keep them. Most Part 1 and Part 2 thumbnails were saved at a wider aspect (1400 × 503) than the full build's and Part 3's (1400 × 717), so those frames cannot be compared pixel for pixel; for them the comparison rests on the step data.

**What this means for the in-house player.** A "full build" is not a separate authoring job: it is the concatenation of the part bodies with (a) one Start, taken from the last part's hero and re-subtitled, (b) one Completed View, taken from the last part, (c) intermediate Completed Views either dropped (when they are a pure camera orbit) or demoted to an ordinary `Step Nc` (when they also complete the last step), (d) continuous renumbering by a fixed offset per part, and (e) section cards and Transitions left untouched.
