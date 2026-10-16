# Verification notes: Guide structure, step naming and numbering (STR-1 .. STR-20)

Skeptic pass over `reports/dim_structure.md`. Everything below was re-derived with my own code from
`digest/*.json` (names, order) and `cadasio_raw/*.json` (flags, camera, annotations, part state), and
checked against renders where the claim is visual. Scripts and intermediate files:
`reports/_work_verify_structure/` (`common.py`, `walker.py`, `walker3.py`, `a1.py` .. `a28.py`, `px.py`, `mont.py`).

Renders opened: contact sheets LSM Part 3 [000]-[007], LAC Full [000]-[007], LAC Part 2 [000]-[007],
PMG Deconstruction [000]-[007], LAC Deconstruction [008]-[015], LSM Deconstruction [016]-[023],
LSM Part 1 [008]-[015], LSM Part 2 [008]-[015], PMG Part 1 [000]-[007]; thumb PMG Part 2 [000];
my own montage of all 19 title blocks cut from `thumbs_raw` (`titles_0.png`, `titles_1.png`);
pixel measurements of all 19 title renders (`px.py`).

## 0. Result in one paragraph

16 of the 20 patterns reproduce as stated, most of them to the exact count. 4 need narrowing
(STR-11, STR-12, STR-15, STR-17) and one statistic inside STR-2 is off by 7. Nothing is refuted. The largest
single correction is to a numeric default: "1600 ms for a threaded spin" is not a default (two authored
steps, counted five times through clones, and contradicted inside its own kit).

| ID | Verdict | Short reason |
|---|---|---|
| STR-1 | confirmed | 1037 = 19 + 33 + 425 + 424 + 117 + 19; grammar 16 of 20; all listed exceptions found, no others |
| STR-2 | confirmed (one stat corrected) | 421 of 425 pairs; annotation-only Step N in builds is 89 (27 %), not 82 (25 %) |
| STR-3 | confirmed | 1012 of 1019 one-step showings; every listed exception reproduced |
| STR-4 | confirmed | Step Nc camera moves 0 of 424; inside-pair Transitions 2 of 101 |
| STR-5 | confirmed | Step 1 first in 19 of 19; contiguous in 17 of 19; offsets check |
| STR-6 | confirmed | pause 920 of 920; play 115 of 117 |
| STR-7 | confirmed | 101 inside / 16 between; 68 / 27 / 4 / 2 split reproduced |
| STR-8 | confirmed (two details added) | 10 camera + 6 fade-in; 39 up-axis changes = 8 T + 28 Step N + 2 card + 1 final |
| STR-9 | confirmed | 108 / 110 of 117; exception lists exact |
| STR-10 | confirmed | 1030 of 1037 at 800 ms; one step overrides FOV to 50 |
| STR-11 | qualified | also used in LSM Deconstruction (4); swap/non-swap split is 55-57 / 8-10, not 48 / 17 |
| STR-12 | qualified | cards cover only part of the bought-in components; Nano and breadboard never get one |
| STR-13 | confirmed | geometry, colours and title text verified on all 19; hero box figure is for 9 renders only |
| STR-14 | confirmed | pure camera step in 12 of 19; exceptions as listed |
| STR-15 | qualified | true for LAC and PMG (7 of 11 part guides); LSM ran the other way and its Part 2 is not a contiguous run of the full build; "68 cut leftovers" overstated |
| STR-16 | confirmed | step arithmetic and seam list reproduce |
| STR-17 | qualified | three-beat removal is the LSM habit; PMG (newest) omits the Transition in 13 of 23 |
| STR-18 | confirmed | single instance, as stated |
| STR-19 | confirmed | 52 real descriptions + 3 placeholders; popups 0 |
| STR-20 | confirmed | base state in first authored step 20 of 20; 68 hidden in 17 guides |

## 1. A method finding that affects every "what changed on this step" number

Three ways of reading part visibility from the raw payload give different answers, and neither the
digest's nor the analyst's is right everywhere. Checked against renders:

| Reading | LSM Part 3 [001] D4 panel hovering | LAC Part 2 [001] card shows switch only | PMG Part 2 [000] display + USB on title | LSM Decon [023] no LED matrix under the lifted plate |
|---|---|---|---|---|
| Digest: leaf visible only if every ancestor is visible | wrong (panel missing) | right | wrong (display missing) | right |
| Analyst: the leaf's own flag only | right | wrong (39 LCD solids shown) | right | wrong (323 matrix solids shown) |
| Mine: leaf starts hidden if it or an ancestor carries the CAD `hidden` flag; after that only leaf-level step flags count | right | right | right | right |

I used the third reading (`walker3.py`). The good news for the report: at classification grade
(appear / swap / move / none per step) the analyst's reading and mine give the same table apart from a
2-step shift between "swap" and "move+swap". So Table 8 and Table 4 stand, with the one correction in
STR-2. The digest's own APPEAR / MOVE lines under-report in LSM Parts 3 and 4, 3+4, Full and
Deconstruction (35 build Step Nc frames look static in the digest and are not).

Unmatched property keys: step `properties` contain many ids that are in neither the assembly tree, the
annotation table, the camera nor the scene (e.g. 419 distinct ids in LAC Full). They are not found
anywhere in `assemblyStructure`; they are stale references to parts from earlier CAD versions and have
no visible effect.

## 2. Pattern by pattern

### STR-1 confirmed
- Kind counts per guide match Table 1 row for row. Total 1037 = 19 Start + 33 cards (31 section cards + the 2 LAC Electronics views) + 425 Step N + 424 Step Nc + 117 Transition + 19 final.
- Grammar `Start (card | Transition | Step N Transition* Step Nc)* Final` matches 16 of 20. Failures: LAC Deconstruction, PMG Part 1, PMG Deconstruction, LAC Electronics. LSM Part 4's 8 / 9c slip passes the kind grammar and fails only on numbers.
- Final name: `Completed View` 16, `Completed Build` 2 (LSM Part 2 [030], LSM Part 1+2 [046]), `Copmleted View` 1 (LSM Part 3+4 [042]).
- Part guides 5-26 numbered steps (median 13), 13-59 viewer steps (median 31). Ratios 2.24-2.62 build, 2.65-2.88 deconstruction.

### STR-2 confirmed, one statistic corrected
- 421 of 425 Step N reach the same-numbered Step Nc; 334 / 76 / 9 / 2 with 0 / 1 / 2 / 3 Transitions. The 4 broken pairs are exactly the four listed. Capital `C` twice (LSM Part 1+2 [042], LAC Part 1 [030]).
- Build Step Nc: model changes on 330 of 330 (154 moves, 156 swaps, 20 plain appear / disappear). Exact match.
- Build Step N (331): appear only 173, fade-out only 2: match. **Annotation-only frames are 89 (27 %), not 82 (25 %)**, and frames with a part move are 31-33, not 40. The 7 frames in dispute carry a stored position change of 0.005 to 0.042 mm on one part and nothing else: LSM Part 2 [014], LSM Part 1+2 [030] [041], LSM Part 3+4 [030], LSM Full [075], LAC Part 2 [019], LAC Full [049]. That is editor jitter, not a move.
- Deconstruction: Step N untouched 67 of 94; Step Nc changes 93 of 94 (63 fade-outs, 22 swaps, 8 moves). Match. The static one is LAC Deconstruction [120], the misnamed Step 45 frame.
- Label slip in the report: Table 8 says "14 build guides"; 331 Step N is the total of all 16 build guides.
- Render check: LAC Full [004] breadboard hovers over F3 with 4 red lead lines (and an eye icon), [005] seated, no annotations, same view.

### STR-3 confirmed
- 1019 showings, 1012 last one step, 7 last two: `2x` label LAC Part 1 / LAC Full [008]-[009]; eye icon LAC Deconstruction [104]-[105]; two lead lines each in PMG Part 3 [056]-[057] and PMG Full [114]-[115] (they appear on the Transition and survive into Step Nc).
- Step N annotated 423 of 425 (missing: PMG Part 2 [002], PMG Full [035]). Step Nc clean 398 of 424. Of the 26 others, 21 carry one image that is new on that frame (eye icon, stored width 7.81 %, or an inset 13-20 % wide); 9 of those are in the three full builds. The remaining 5 are the faults above plus LAC Deconstruction [120].
- Transitions annotated 15 of 117, all PMG (Part 3 3, Full 3, Deconstruction 9). Start 2 of 2 in 19 of 19; final 0 in 19 of 19; cards 6 / 23 / 2 with 0 / 1 / 2.
- Extra fact: annotation objects are single-use. 1010 distinct objects account for the 1019 showings; only 9 objects are shown in two separate steps (LSM Part 2 3, LSM Part 1+2 4, LSM Deconstruction 2).

### STR-4 confirmed
- Camera moves by kind: Start 19 of 19, cards 31 of 33, Step N 266 of 425 (build 211 of 331, deconstruction 55 of 94), Step Nc 0 of 424, Transition 12 of 117, final 17 of 19. I also compared the raw camera position, target, quaternion and FOV: no change of any kind on any Step Nc.
- Inside-pair Transitions with a camera move: PMG Deconstruction [007] (95.6 deg) and [012] (83.4 deg). View constant from Step N to Step Nc in 423 of 425.
- Median rotation when Step N moves: 62.5 deg build, 55.7 deg deconstruction over all guides. On the six master projects only (three full builds, three deconstructions) it is 145 of 240 = 60 % and 58.0 deg for builds.

### STR-5 confirmed
- First numbered step is `Step 1` in 19 of 19; contiguous 1..N in 17 of 19 (LSM Part 4 has N-sequence 1-8, 10-13 and Nc-sequence 1-7, 9-13; LAC Deconstruction has N-sequence ..39, 41, 40, 41, 42, 43, 44, 46, 47 and `Step 45c` twice).
- Full builds 1..38 / 1..57 / 1..51. Offsets equal the preceding parts' counts: LAC 14 / 32 / 40, PMG 14 / 25, LSM 8 / 21 / 26. `stepPrefix` = "Step" in 20 of 20.

### STR-6 confirmed
- pause on 920 of 920 non-Transition steps; play on 115 of 117 Transitions; pause Transitions LAC Deconstruction [033] (changes nothing) and [118] (113 solids move: RTC lift).
- Popups / checklists / buttons 0 of 1037; `nextStep` / `previousStep` default on 1037; `animationChained` false on 1037. Auto-advancing share 0-14.3 % in builds (LAC Part 4 6 of 42), 23.0-27.5 % in deconstructions.

### STR-7 confirmed
- 101 inside a pair (counting LAC Deconstruction [121], which sits between the two frames named `Step 45c`), 16 between. Inside: 68 part moves, 27 swaps, 4 that change nothing in the model, 2 camera-only. No-op Transitions: LSM Deconstruction [011], LAC Part 4 [027], LAC Full [116], LAC Deconstruction [033].
- Build guides 31 of 331 numbered steps contain one (27 with one, 4 with two); full builds 3 + 7 + 5 = 15 of 146. Deconstructions 19 of 24, 27 of 47, 10 of 23. Maximum 3 (PMG Deconstruction Steps 2 and 3).
- Render check: LAC Full [001] arrow + inset, [002] backing sheet below the breadboard, [003] sheet gone.

### STR-8 confirmed, two details added
- Between pairs: 10 camera-only (LSM 8 with an up-axis change, 53.1 to 142.8 deg; LAC Part 4 [019] = LAC Full [108], 13.1 deg and a 377 to 323 mm push-in) and 6 fade-ins of a push-button module (PMG Part 1 / Full [013] [020] [027]).
- 39 up-axis changes = 8 on a Transition (all LSM) + 28 on Step N (LSM 6, LAC 16, PMG 6) + 2 on a card (LAC `LCD Screen`, Part 3 [008] = Full [078]) + 1 on a final view (LSM Part 3 [012]). So "LAC flips on Step N every time" should read "LAC never uses a Transition for it" (16 on Step N, 2 on a card).
- Added: after every one of the 10 camera-only bridge Transitions the following Step N does not move the camera (10 of 10). The Transition takes the whole move.
- Added: the up-axis is `+y` on every Start and every final step (20 of 20 guides); every flip is undone before the guide ends.

### STR-9 confirmed
- `hideInStepPicker` true on 108 of 117 Transitions (6 false, 3 absent) and on 0 of 920 others. `overlayVisible` false on 110 of 117 and on 0 of 920 others. Both exception lists are exact, including LAC Part 4 [028] visible while its twin LAC Full [117] is hidden.
- Name `Transition` 113; `Transiton` LSM Deconstruction [038]; `Ttansition` LAC Part 2 [023], LAC Full [053]; `Transititon` LAC Deconstruction [002].

### STR-10 confirmed
- 800 ms on 1030 of 1037. The 7 at 1600 ms are the seven listed. LSM Full [040] `Step 18c` is 800 ms.
- CAD options fade / fade / tween on 1037 (2 steps carry an extra `animation_attention: none`). Camera tween, orbit off, speed 2 on 1037. 2D fade / fade / tween on 1037. Project flags identical in 20 of 20.
- FOV: 45 in every project default, but one viewer step overrides it: LSM Part 1 [011] `Capacitor` sets FOV 50 and [012] sets it back to 45. So 1036 of 1037 steps, not "20 of 20" without exception. The same card in LSM Full does not do this.

### STR-11 qualified
- Counts by kind and kit reproduce: 65 = 44 Step N + 17 cards + 4 Step Nc; LSM 36, LAC 29, PMG 0 of 298. The other steps are 970 `none` plus 2 with no value at all (the Start of LSM Part 4 and LSM Part 3+4, the two that still carry Cadasio's placeholder text).
- **Not construction-only.** LSM Deconstruction has 4: [001] Step 1, [027] Step 9c, [037] Step 14, [047] Step 17c. LAC Deconstruction and PMG have none.
- **The link to scene swaps is stronger than reported.** With render-consistent visibility, 55 to 57 of the 65 fades (depending on how "more than half" is measured) replace more than half the visible model, and 8 to 10 do not: LSM Part 3 [001], LSM Full [046], LSM Deconstruction [001] [027] [047], LAC Part 1 [004], LAC Part 2 [025], LAC Part 4 [001], LAC Full [004] [055]. In the two full builds that use it, 12 of 13 (LSM) and 11 of 13 (LAC) fades are cuts between the assembly and an isolated part or back.
- It is still not systematic: 85 to 110 comparable whole-scene swaps use `none` (LAC Full alone: 11 with fade, 10 without).

### STR-12 qualified
- Reproduced: 31 card steps in 13 guides; followed by a Step N 31 of 31; preceded by a Step Nc 26 and by Start 5; pause / 800 ms / not hidden from the picker 31 of 31; camera moves on entry 29 of 31 and on the next step 30 of 31; annotations 0 on 6, 1 on 23, 2 on 2. 14 authored cards (13 distinct names: `USB Cable` is used by both LAC and PMG).
- Every card changes the model (25 swaps, 5 fade-outs, 1 move+swap); none is a pure overlay.
- **"Before the first numbered step that uses a new bought-in component" is too strong.** Component families with no card of their own, by full build:
  - LSM: breadboard, Arduino Nano, resistors, 8x8 LED matrix (it has a 2D pin diagram, not a part card), push button. Cards: Capacitor, Mini USB Cable.
  - LAC: breadboard, Arduino Nano, resistors, potentiometer with knob / nut / washer. Cards: Real Time Clock, Rocker Switch, Alarm Buzzer, LCD Screen, USB Cable.
  - PMG: Arduino Nano (first seen at Step 1 [002]). Cards: Nano I/O Module, Push Buttons, 4-Digit Display, Dot Matrix Display, USB Cable.
  The analyst's explanation ("first appearance is itself a numbered prep step") covers resistors, ribbons and the potentiometer but not the Arduino Nano (seated directly at LSM Full [006], LAC Full [006], PMG Full [002]) or the LSM push button.
- **Not only bought-in electronics.** `LED Stems` (64 acrylic stems, LSM Full [082]) is a mechanical part in the enclosure section and gets a card.
- **Name on canvas.** The `Nano I/O Module` inset carries its own small caption "NANO I/O MODULE LABELS" (PMG Part 1 [001] render). No other card shows text naming the component.
- Render checks: LSM Part 1 [011] capacitor alone + framed photo with GND / VCC marked; PMG Part 1 [006] button alone + framed photo with VCC / OUT / GND boxed in red; LSM Part 2 [009] full-frame 2D diagram, no 3D part; LAC Part 2 [001] switch alone, no annotation.

### STR-13 confirmed
- 19 of 19: exactly two image annotations, leader type `none`, no links, no anchor, both gone on the next step. Same logo file in 19.
- Stored geometry matches Table 6 to two decimals. Logo widths: 33.24 (3), 37.58 (5), 38.90 (6), 39.53 (4), 36.38 (PMG Deconstruction). Title widths: 42.07 (6), 42.93 (5), 45.66, 45.80, 46.51 (4), 48.36, 58.28.
- Pixels: logo fill modal colour #00B0EF on 19 of 19 renders; title text modal colour #585858 on 18 of 19 (#5B5B5B on PMG Deconstruction's smaller 1920 x 729 render).
- Title text read on all 19 (montage): three lines, "Laser Stem Matrix (LSM)" on 8, "LCD Alarm Clock (LAC)" on 6, "Piano Memory Game (PMG)" on 5; variants Part 1-4, Part 1 + 2, Part 3 + 4, Full Build, Deconstruction; copyright 2025 on 14, 2026 on 5.
- Hero: every solid visible on Start is also visible on the final view in 16 of 16 build guides (at least 99.9 %). In the other direction the final view has more: LAC Full Start shows 817 solids against 862 on its final view (LAC Part 4 Start shows 863); LSM Part 2 and Part 1+2 651 against 679.
- Start elevation 21-47 deg, median 35. Next step moves the camera 19 of 19 (8.0-109.5 deg).
- Caveat on the hero box: "x 48-54 % to 88-95 %, y 13-15 % to 74-83 %" holds for the nine clean renders named (my figures for those nine: left 48.4-53.9 %, right 88.4-95.0 %, top 12.6-15.3 %, bottom 73.8-83.2 %). On the other ten the model runs wider (`px2.py`): right edge 95.8-98.7 % (LSM Part 2, Part 1+2, Part 3, LAC Part 2, LAC Part 3, PMG Part 2); top edge 7.9 % (LAC Part 1) to 24.2 % (PMG Part 2); left edge 40.6-41.3 % in LSM Part 2, LSM Part 1+2 and LAC Part 3 and 44.9 % in LAC Part 2, i.e. the model reaches into the gap between logo and title block. PMG Deconstruction's model runs off the bottom edge (99.9 %) and under the title. Treat the box as a target area, not an invariant.

### STR-14 confirmed
- 0 annotations 19 of 19; camera moves 17 of 19 (4.9-120.3 deg, median 66.4). Build guides: Start-to-final direction 2.5-21.6 deg in 14, 75.8 deg in LAC Part 4 and LAC Full; median 12.9. Final elevation 21.3-47.7, median 38.1. Distance ratio 1.00 x 9, 0.86 x 3, 0.63 x 3, 1.17 x 1.
- Model unchanged in 10 of 16 build guides and 2 of 3 deconstructions, so the step is a pure camera move in 12 of 19. Others: 4 wire-cap solids reappear (LSM Part 4, Part 3+4, Full); 67 solids drop up to 9.8 mm (LSM Part 3+4); 7 solids settle 1.7 mm (PMG Part 3, Full); PMG Part 1 [033] swaps 3 solids and PMG Deconstruction [060] removes 293 (both do the last step's result and have no camera move).

### STR-15 qualified
- The rule is stated for "construction part guides, all kits". It holds for LAC and PMG (7 of 11 part guides). In LSM the four parts were cut from the two combined guides and the full build came last; LSM Part 2 is not a contiguous run of the full build (its Steps 12 and 13 are the full build's 21 and 20), and nothing in the full build's Part 1 / Part 2 region shares a camera with the parts.
- LAC: 130 of 130 non-title steps of the full build equal their part twin on camera distance / elevation / azimuth, annotation counts by type, behaviour and duration. PMG: one mismatch, the `4-Digit Display` card (Full [034] elevation 11.5 / azimuth -75.3; Part 2 [001] 2.8 / -91.2). PMG Full [033] `Step 14c` has the same camera and content as PMG Part 1 [033] `Completed View`.
- LSM: the 23 matching steps are all in the Part 3 / Part 4 region (Full Steps 22, 22c, 26c, 27, 27c, 31c, 32-38c, the [077] Transition, the `LED Stems` card, the final view). Nothing in Full [001]-[047] matches Part 1, Part 2 or Part 1+2. Those three guides also sit on a different CAD model (cadId 1baeed31) from the other five LSM guides (4114fb73).
- No step id is shared between any full build and its parts (0 shared ids in all three kits), so the twin relation can only be shown by content, as the analyst did.
- Wording: "cut leftovers stay as hidden steps (68 across 17 guides)" overstates. 15 of the 68 are the base-state keyframe; the four LAC parts have no hidden step other than that one; the largest count is in PMG Full (18), which is the master, not a cut.

### STR-16 confirmed
- 137 - 6 = 131; 120 - 3 = 117; 92 - 6 + 2 = 88; 50 - 3 = 47; 42 - 2 + 3 = 43. Kept Start has the last part's camera in 4 of 5 (LSM Full 374 mm against Part 4's 321 mm); kept final view in 5 of 5. 10 seams, 2 with a Transition (LSM Part 3+4 [014], LSM Full [059]).
- LSM order swap confirmed: Part 2 has panel (Step 12) then cable (Step 13); Full has cable (Step 20) then panel (Step 21). LSM Part 3+4 Step 1 is the same panel step as LSM Part 1+2 Step 20.

### STR-17 qualified
- Skeleton confirmed: 3 of 3 with 1 Start, 0 cards, 0 descriptions, 1 `Completed View`; 24 / 47 / 23 numbered steps. Title camera identical to the full build in LSM (374 / 29 / 54) and LAC (377 / 37 / 143); PMG same distance, elevation 33 against 21.
- **The three-beat removal is not uniform across kits.** Numbered steps with at least one Transition: LSM 19 of 24 (79 %), LAC 27 of 47 (57 %), PMG 10 of 23 (43 %). What the Transition does:
  - part slides away, then fades out on Step Nc: LSM 17, LAC 13, PMG 6 (36 of 94);
  - plugged wire or module is swapped for its loose model, then fades out: LAC 12;
  - literally "Step N unchanged, one moving Transition, fade-out": LSM 7, LAC 8, PMG 3 (18 of 94).
- **PMG, the newest kit, mostly uses two beats**: cue on Step N, fade-out on Step Nc, no Transition, in 11 of 23 (Steps 5, 9, 15-22 and 23 into Completed View), against 6 slide-off removals.
- Step-level `fade` appears 4 times in LSM Deconstruction (see STR-11).
- Render checks: LAC Deconstruction [008] arrow, [009] panel F5 slid off, [010] gone; [011] arrow, [012] front panel moved aside still wired (no Transition). PMG Deconstruction [001]-[003] with a second arrow on the Transition.

### STR-18 confirmed
- 2 viewer steps, pause / 800 ms, 0 annotations shown (the project stores 150 annotation objects, none visible), hidden `Start` last in order, placeholder description on `All Wood`.

### STR-19 confirmed
- Real descriptions 6 + 18 + 28 = 52 (LSM Part 1, Part 2, Part 1+2); placeholders on LSM Part 4 [000], LSM Part 3+4 [000], LAC Electronics [001]; popups 0 of 1037. Stale numbering and the four typos are as quoted.

### STR-20 confirmed
- First authored step sets scene colour #ffffff (project default is #EEEEEE / matt) and style `toon` with edges `normal` in 20 of 20; it is hidden in 15, the visible Start in 4, the first view in LAC Electronics. The background is never set again in any guide.
- "1148-5373 solids" counts every property entry, including stale ids. Entries that resolve to a node in the current tree: 1058-5367.
- 68 hidden steps in 17 guides. `startStepId` hits the visible Start only in LSM Part 1; 7 point at the hidden first step, 3 at a mid-guide step, 9 at an id that no longer exists.

## 3. Numeric defaults

Confirmed as stated: 800 ms; fade / fade / tween (parts and 2D); camera tween, no orbit, speed 2;
pause 920 of 920; play 115 of 117; picker hidden 108 of 117; overlay hidden 110 of 117; annotation
lifetime 1 step (1012 of 1019); 2 annotations on Start; 0 on final; 0-2 on a card (6 / 23 / 2);
Step Nc camera never (0 of 424); Transitions per step 334 / 76 / 9 / 2; 9 % / 60 % with a Transition;
5-26 numbered steps per part (median 13); 38 / 57 / 51 per full build; 4 / 5 / 5 cards; logo position;
logo height 0.27 x width; title position; title width 42-46.5 % in 17 of 19; title h/w 0.19-0.29;
#00B0EF; #ffffff; copyright line (2025 x 14, 2026 x 5); Start elevation 21-47 (median 35); final
elevation 21-48 (median 38); final within 23 deg of Start in 14 of 16 (median 13); distance ratios
1.00 x 9, 0.86 x 3, 0.63 x 3; overlay bar bottom, visible at start; auto-start and animate-back true;
final name 16 of 19; lower-case c 422 of 424.

Corrected:

| Default | Claimed | Corrected | Basis |
|---|---|---|---|
| Duration for a threaded spin | 1600 ms (optional) | no default; keep 800 ms | 2 authored LSM steps (nut off, nut on) seen 5 times through clones; LSM Full uses 800 ms for nut-on [040]; LAC nut steps 800 ms; the other 2 are LCD swaps in LAC Deconstruction [016] [017] |
| Step-level page transition | none, 970 of 1037 | none on 970, unset on 2, fade on 65 | the 2 unset are Start of LSM Part 4 and Part 3+4 |
| Camera moves on Step N | 63 %, median 62.5 / 55.7 deg | 63 % and 62.5 / 55.7 over all guides; 60 % and 58.0 / 55.7 on the six masters | 266 of 425; masters 145 of 240 |
| Field of view | 45 deg, 20 of 20 | 45 deg project default in 20 of 20; 1036 of 1037 steps | LSM Part 1 [011] sets 50 |
| Logo width | 37.6-39.5 % (33.2 % in three oldest) | 37.58 / 38.90 / 39.53 % in 15; 33.24 % in 3; 36.38 % in PMG Deconstruction | stored widths, 19 title pages |
| Viewer steps per numbered step | 2.3-2.6 / 2.7-2.9 | 2.24-2.62 / 2.65-2.88 | per-guide ratios |
| Share of numbered steps with a Transition, deconstruction | 60 % | 60 % overall; 79 % LSM, 57 % LAC, 43 % PMG | 19 of 24, 27 of 47, 10 of 23 |
| Hero model box on title | x 48-54 to 88-95 %, y 13-15 to 74-83 % | holds on the 9 clean renders; across the 18 renders near 2:1 the model spans left 41-61 %, right 83-99 %, top 8-24 %, bottom 72-83 % | pixel measurement of 19 title renders (PMG Deconstruction, 2.63:1, excluded from the range) |
| Title text colour | #585858 | #585858 on 18 of 19 renders | PMG Deconstruction reads #5B5B5B on its smaller render |
| Annotation-only Step N, build guides (STR-2 stat) | 82 of 331 (25 %) | 89 of 331 (27 %) | 7 frames carry only a sub-0.05 mm stored position change |

## 4. Patterns the report did not state

1. **Annotation objects are single-use.** 1010 distinct annotation objects produce the 1019 showings; 9 objects are shown in two separate steps (LSM Part 2 3, LSM Part 1+2 4, LSM Deconstruction 2). A repeated cue (the eye icon, a lead line for a second leg) is a new object each time.
2. **Clones keep the master's whole annotation inventory.** 1524 of the 2534 annotation objects stored across the 20 projects are never visible in the viewer. LAC Part 3 shows 23 of its 150; LAC Electronics shows 0 of 150.
3. **A camera-only bridge Transition takes the whole move**: the Step N after it never moves the camera (10 of 10).
4. **Every up-axis flip is undone before the guide ends**: up-axis is `+y` on Start and on the final step in 20 of 20.
5. **Two-beat removal in the newest deconstruction**: PMG Deconstruction removes a part with cue then fade-out and no Transition in 11 of 23 numbered steps.
6. **Wire-unplug idiom in LAC Deconstruction**: eye-icon cue on Step N (12 of 12, 4 with a label as well), Transition swaps the plugged wire for the loose wire, Step Nc fades it out. 12 numbered steps: Steps 19-22 and 36-43, e.g. [101]-[103], [105]-[107].
7. **Card coverage is partial and has grown by kit** (jumper wires left out of the count): LSM 2 part cards + 1 pin diagram for 7 bought-in component types, LAC 5 for 9, PMG 5 for 6. The Arduino Nano never has one.
8. **Isolated-part pairs**: 30 of 331 build Step N cut from the assembly to a single loose part (visible solids under 25 % of the previous frame, not counting steps after a card): LSM 14, LAC 12, PMG 4. The assembly returns on the next Step N. In LSM Full and LAC Full these cuts are where the step-level `fade` sits.
9. **Authoring aspect ratio is about 2:1, not the embed size.** Every viewer step has a saved render (1037 of 1037): 2559 x 1239 (2.07:1) in 14 guides, 2:1 in 3, 1.95:1 in 2, 2.63:1 in PMG Deconstruction. The project `embedSize` is 560 x 315 (16:9) in 20 of 20. Annotation positions are stored in % of viewport, so the title-page layout was composed for roughly 2:1.
10. **Step ids are not preserved by cloning** (0 shared ids between any full build and its parts), and LSM runs on two CAD models (Parts 1, 2, 1+2 on one; Parts 3, 4, 3+4, Full, Deconstruction on another).

## 5. Not checked

- Player behaviour that the payload cannot show (which step opens first, dwell after a play step, Back through a Transition). The analyst lists these as open questions and I have nothing to add.
- Whether "new part appears at a hover pose" on Step N is millimetre-accurate; I only checked appear / move / swap classification.
- The three visibility readings differ by 3 to 19 solids on a few LAC and PMG Deconstruction steps even between my two variants (leaf flags only, or parent flags pushed down). Thumbnails are too small to settle those; no count in this note depends on them.
