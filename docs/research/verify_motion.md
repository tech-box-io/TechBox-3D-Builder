# Verification notes: part motion, hover offsets and seating

Skeptic pass over `reports/dim_motion.md` (MOT-1 to MOT-19 and the numeric defaults). Everything below was re-derived with code written for this check; none of the analyst's scripts or intermediate files were reused. Work files: `reports/_work_verify_motion/` (`vtrack.py` replay, `vlib.py`, then one script per check; `logs/<guide>.txt` holds a full per-frame motion log of all 20 guides).

Guide short names: LSM / LAC / PMG, `-F` Full Build, `-P1`.. part guides, `-Decon`. `[NNN]` = viewer index in that guide.

## 0. Method and why the digests could not be used

The task asked for a recompute from `digest/*.json`. For this dimension that is not possible, and the analyst was right to say so. I confirmed it independently before building anything:

- A step `position` REPLACES the node's local translation, it is not an offset from the assembled pose (LAC-F F1-1: CAD translation [436.4, 600.8, 730.6], first write [436.4, 600.8, 897.7]). `rotation` likewise replaces the CAD rotation (LAC Nut-4 returns to its CAD quaternion [0.9983, 0, -0.0578, 0] on Step 30). `scripts/digest.py` sums raw positions as offsets and never rotates them into world axes.
- Visibility is per leaf solid. PMG-F `USB Cable end-1` has `visible:false` on its parent from the first authored step to the last, yet its solids are shown at [056] (checked in `thumbs/.../056.jpg`). The digest ANDs the parent chain and so loses such parts.
- Scored against my replay for the 119 first-stage insertions: the digest MOVE line agrees in 39, has the wrong direction or distance in 46, and is missing altogether in 34.

So all numbers here come from a replay of `cadasio_raw/*.json`: world pose per leaf solid = product of local matrices down the tree, mm = scene units / scaleFactor, displacement measured on the bounding-box centre of the largest moving solid of each top-level component. Annotation state and step names were taken from the same replay. Spot values match the analyst's to 0.1 mm almost everywhere, so the two independent trackers agree on the raw facts; the disagreements below are about counting rules, class membership and how far the rules generalise.

Totals reproduced: 1037 viewer steps; 425 `Step N` frames, 424 `Step Nc` frames, 117 Transition-named frames (115 `play`, 2 `pause`).

## 1. Verdict summary

| ID | Verdict | One-line reason |
|---|---|---|
| MOT-1 | qualified | 119 / 86 / 6 / 7 / 13 / 4 / 3 reproduce, but "every rigid part" is too wide, and half of the "pre-staged while hidden" poses are written in the frame that fades the part OUT |
| MOT-2 | confirmed | 106 of 119 single leg, 103 without rotation, 424 of 424 c-steps with a fixed camera |
| MOT-3 | qualified | Transition legs hold 13 of 13; the "needs a different viewpoint" condition holds for 5 of 8 separately numbered second stages |
| MOT-4 | qualified | oblique share is 12 of 50 unique (24%), not 8; world axes are not screen axes |
| MOT-5 | qualified | overall statistics reproduce; the panel-mount class contains 3 nut rows; "one part-length" fits 10 of 22 |
| MOT-6 | qualified | exact for the PMG panels only; D3 and F2 do not slide in their own plane; F9 is a different mechanism; pivot is not always the edge |
| MOT-7 | confirmed | 11 spins, 115.1-179.6 deg, 1600 ms on 5; no rotation on ordinary insertions |
| MOT-8 | confirmed | 6 of 6 receivers fade in at rest, no counter-example |
| MOT-9 | confirmed | 0 wire tweens into a connection, 0 lead lines, 0 arrows |
| MOT-10 | confirmed | parking distances and repeatability reproduce; 30 of 30 parked on the camera side |
| MOT-11 | confirmed | 10 fan-outs, sideways only; fan-out default needs rewording |
| MOT-12 | qualified | true for parts whose wires are already routed; parts with free leads are tweened, one of them in full context |
| MOT-13 | confirmed | 11 pairs, 4 unique, no move |
| MOT-14 | qualified | "animate one, fade the rest" is used for 2 large sets only; 4 small identical sets are fully tweened |
| MOT-15 | confirmed | 14 removals, 12 on a Transition, arrow on all 14 |
| MOT-16 | qualified | direction reversed yes; distance reused for 17 parts; LSM does not undo two-stage joints |
| MOT-17 | qualified | cards isolate (14 of 14) but only 5 are followed by a tween of the carded part |
| MOT-18 | qualified | timing settings exact; "never move the camera with a part tween" fails on 34 non-c, non-Transition frames |
| MOT-19 | confirmed | 2 static views, 0 annotations |

## 2. Per-pattern notes

### MOT-1 qualified

Reproduced: 119 first-stage insertion tweens (LSM-F 19, LAC-F 16, PMG-F 15 = 50 unique; they occur in 15 guides, LAC Part 3 has none). How the mover reached hover: fades in on the Step N 86; visible since the card before 6; bent resistor standing there since the prep step 7; already hovering 3; visible slide 13 (39.3-81.2 mm); nudge 0.5-1.7 mm 4. 116 of 116 distinct hover frames carry lead lines, all `#ff0000` (277 lines: 241 solid, 36 dashed), and none carries an arrow.

Narrowing needed:

1. "Every rigid part" is wrong. In the Full Builds 50 parts are tweened in, but 6 receivers, 63 stems, 3 keys, 3 button modules on Transitions, 6 carded modules and 2 plugged cables fade in already seated, and every wired sub-assembly is cross-faded. The rule applies to rigid parts that are placed by a tween.
2. Pre-staging, counted at viewer-frame level for the 99 fade-in cases: pose set while the part is hidden in both neighbouring frames 45; pose set in the frame in which the part goes from visible to hidden 50; pose reached in the frame that shows it 4 (LAC-F [031] switch 81.2 mm, PMG-F [059] H2 40.0 mm, and H8 0.9 mm at PMG-F [081] and PMG-P3 [023]). Ignoring the two sub-millimetre cases gives the analyst's 97 of 99.
3. The 50 are all the same event: the title page shows the finished model, and the first frame after it hides the model and writes the hover poses together (LAC-F [001] 6, LAC-P1 3, LAC-P4 3, LSM-F [001] 6, LSM-P1 2, LSM-P12 2, LSM-P3 1, LSM-P34 6, LSM-P4 3, all under step `transition: fade`; PMG-F [001] 6, PMG-P1 1, PMG-P2 1, PMG-P3 [001] 10, with no step fade). So "never move a part while it is fading in" stands, but parts are moved while fading out, 18 times with nothing masking it.

### MOT-2 confirmed

106 of 119 single leg on Step Nc (44 of 50 unique); 103 of the 106 with no rotation, the 3 exceptions being the LSM nut (LSM-F [040] 115.1 deg, LSM-P2 [022] and LSM-P12 [038] 179.3 deg). Camera unchanged on 424 of 424 c-steps. Small notes: two of the 106 run 1600 ms (the two 179.3 deg nut spins); 18 single legs stop short of the seat by design, as the analyst says. Pair mix by my strict name matching: 329 build pairs = 163 tween, 158 cross-fade, 8 fade-in only (analyst 331 = 163 / 157 / 11); the difference is LSM-P4 `Step 8` followed by `Step 9c`, PMG-P1 `Step 14` with no c frame, and how a 2 mm residue at LSM-F [085] is filed.

### MOT-3 qualified

Reproduced: 13 multi-leg seats (11 two-leg, 2 three-leg; 6 unique), every leg 800 ms, earlier legs on `play` Transitions, last leg on Step Nc. 68 Transition-named frames tween a part (67 `play` plus the `pause` Transition LAC-Decon [118]), 33 cross-fade or fade, 16 neither; none of the 68 moves the camera and the 12 that move the camera change no part.

Counter-evidence to the second sentence: of the 8 second stages given their own numbered step, the camera moves on entering 5 (PMG H5 [067], H6 [071], H7 [079], H10 [089], LSM D11 [075]) and does not move on 3 (LAC F7 [092], LAC F9 [102], LSM D3 [055]). And the same joint is authored both ways: the swing of LAC F2 [127] and PMG H14 [115] is on the Step Nc straight after a Transition slide, the swing of D3, H5, H6, H7, H10 is its own step. A different viewpoint is therefore not what decides it.

Wording: "legs per press = 1" in the defaults is wrong. One press on Step N plays every leg back to back (1.6 s or 2.4 s); it is one leg per authored step.

### MOT-4 qualified

The rule itself survives: for single-leg seats the lead lines are parallel to the hover vector (median 0.0 deg, max 3.9 deg, 255 lines) and their length / hover distance has quartiles 0.94 / 1.00 / 1.07.

Direction counts depend on tolerance. With "single axis" meaning within 5 deg of a world axis: unique 50 = +Y 23, -Y 3, horizontal 12, oblique 12 (24%); all 119 = single-axis 91 (76%), oblique 28 (24%). The analyst's 25 / 14 / 3 / 8 and 101 / 18 need a tolerance of about 12 deg, which files H11 (7.2 deg) and H12 (9.7 deg) under +Y and H10 (7.8 deg) and H7 (11.7 deg) under horizontal, although MOT-6 says H7 and H10 slide in their tilted plane. Electronics into breadboard or socket: 27 of 27 from above, 25 exactly vertical, 2 (LSM capacitor, LSM-P1 [012] and LSM-P12 [011]) 5.9 deg off, as the analyst's anomaly note says.

World axes are not what the student sees. `up_axis` of the scene is rewritten per step (LAC-F -x for 23 frames and -y for 2, PMG-F -y for 16, LSM-F +x 7, -z 2, -y 2). Projected through the camera rotation at each hover frame, the hovering part sits above its seat on screen in 75 of 119, to the right in 23, to the left in 21, and below in 0. The three "-Y" cases (washer, nut, knob) read as sideways (sheet LAC-F [056]-[063]); the PMG underside panels H5 / H6 are added with the model turned over (sheet PMG-F [064]-[071]).

### MOT-5 qualified

Reproduced: all 119 min 22.9, quartiles 42.6 / 60.5 / 80.8, max 139.4; unique 50 quartiles 43.5 / 60.9 / 81.6; breadboard 46.9 / 48.0 / 49.2; boards 29.8 / 36.7 / 44.1; passives 29.1 / 32.4 / 40.0; USB 22.9; face-on wood 8 unique 42.0 / 64.7 / 69.4; other wood 22 unique 40.0 / 81.0 / 139.4, hover / extent quartiles 0.83 / 1.01 / 1.51; Pearson 0.46 (50) and 0.48 (119), Spearman 0.28 / 0.29.

Errors and narrowing:

- The class "panel-mount component with trailing leads" (4 unique, 10 copies, directions "+Y x4, +Z x3, -Z x3") contains the LSM nut going on. The mover at LSM-F [039], LSM-P2 [021], LSM-P12 [037] is the solid `Push button-Boss-Extrude6`, 21.0 x 18.0 x 1.5 mm, i.e. the hex nut (visible in sheet LSM-F [032]-[039]). Correct class: 3 unique (79.1, 81.2, 102.5), 7 copies (79.1 x2, 81.2 x2, 102.5, 103.2 x2), median 81.2.
- "Hardware on a shaft" then has 4 unique and 9 copies: 55.9-83.1 mm, median 61.3. The 60 mm figure is LAC only; the LSM nut hovers 80.4-83.1 mm because it starts beyond the lead tips.
- "About one part-length for anything that slides lengthwise" holds for 10 of the 22 unique rows (D11 x3, F7, H5, H6, H7, key, F2, H14: 0.83-1.05). The class is a catch-all: short-in-travel parts hover 3.1-5.7 extents (F8 94.2 mm for 16.5, D10 43.7 for 11.3, D9 64.6 for 18.5, H8 94.5 for 30.9), and long panels with a short tab engagement hover 0.29-0.62 (H2, H3, D3, H12, H11). The default "1.0 x extent, clamped to 40-140 mm" lands within 20% of the authored value for 11 of 22.
- Leads: measured along the travel, switch plus leads is 68.0 mm (hover 81.2, ratio 1.19) and button plus leads 82.5 mm (hover 102.5, ratio 1.24); the potentiometer's leads run sideways (28.0 mm along travel, hover 79.1).

### MOT-6 qualified

Per part, tilt at hover against the final pose / angle between the slide and the panel's own plane at hover / where the swing pivot sits:

| Part | Tilt at hover | Slide out of own plane | Swing | Pivot (fraction of half-size from centre) |
|---|---|---|---|---|
| PMG H5 [065]-[068] | 23.6 | 0.0 | 23.6, own step | 0.99, on the face: the edge |
| PMG H6 [069]-[072] | 18.1 | 0.0 | 18.1, own step | 0.99: the edge |
| PMG H7 [077]-[080] | 11.7 | 0.0 | 11.7, own step | 1.00: the edge |
| PMG H10 [087]-[090] | 7.9 | 0.0 | 7.9, own step | 0.75: 9.7 mm inside the edge |
| PMG H14 [113]-[115] | 10.1 | 0.0 | 12.6 on Step Nc, then 2.5 back on Completed View [116] | 0.48: half-way to the edge |
| LSM D3 [053]-[056] | 21.6 | 6.2 (slide inclined 27.9) | 21.6, own step | 0.95 |
| LAC F2 [125]-[127] | 21.4 | 11.8 (slide inclined 33.2) | 21.4 on Step Nc | 0.92 |
| LAC F9 [098]-[103] | 0 | - | leans 25.8 on a Transition, drops, straightens 25.8 in Step 46 | rotation is about the panel's thickness axis, near one corner |

So "already tilted by its swing angle" holds for 6 of 8, "slides in its own tilted plane" exactly for 5 (all PMG), "about the engaged edge" exactly for 3 and approximately for 2 more, "as a separate stage" as its own step for 6 and as the c-leg for 2. LAC F9 is not a hook-and-swing panel at all: it leans within its own plane to pass a hook, drops 33.0 mm and is stood upright (sheet LAC-F [096]-[103]).

The supporting statistic does not mean what is claimed. Using the analyst's own definition there are 576 rotation writes above 1 deg and 557 have an `origin` key on the node, but the stored origin is non-zero on only 373 (65%); 184 are {0, 0, 0}. The swing-to-seat write itself usually resets it (LAC F2 at Step 56c writes identity rotation, origin 0, `use_origin` false). The pivot has to be recovered from the two poses, as in the table.

### MOT-7 confirmed

65 visible rotation tweens above 1 deg in the 20 guides. Spins: 11 (LAC-F [050] 175.9, [053] 123.6; LAC-P2 [020], [023] the same; LSM-F [035] 179.6, [040] 115.1; LSM-P2 [017] 170.9, [022] 179.3; LSM-P12 [033], [038] the same; LSM-Decon [049] 176.0), all exactly about the travel axis; 1600 ms on 5. Flex 15.1 / 16.0 deg, knob 49.8 deg with 0 mm. The remaining rotations are all on frames that are neither c-steps nor Transitions and are residues, not uses: LAC nut re-angled 21.4 deg at LAC-F [065] and LAC-P2 [035]; LSM capacitor 6.0 deg at LSM-F [013] and 108 deg at LSM-P1 [012]; H14 2.5 deg at PMG-F [116], PMG-P3 [058], PMG-Decon [001]; a wire bundle turned 179.5 deg at LSM-Decon [037] under a step fade.

### MOT-8 confirmed

New non-wire parts that appear on a Step N of the Full Builds and do not move in that step while another part does: LAC F3 [004], F4 [032], F1 [055]; LSM D1 [004], D2 [037]; PMG H1 [059]. Six of six, no counter-example. The same holds for the cross-faded attach steps (the wired shield comes to the housing at PMG-F [102], the matrix to the box at LSM-F [068]).

### MOT-9 confirmed

100 wire-connection pairs plus PMG-P1 `Step 14`, whose swap lands on the Completed View [033] because there is no `Step 14c` (anomaly). All are appear plus disappear with no move; lines 0 and arrows 0 on every hover frame. One routed wire per step except the LSM push-button leads, which is three copies of one step (LSM-F [041], LSM-P2 [023], LSM-P12 [039]). Two additions: the hover frame is not unannotated, it normally has an eye-icon image on the loose wire and two text labels at the destination (65 of 102 have exactly that); and lead lines are not exclusive to tweens, 6 cross-fade attach steps in the Full Builds carry 2 or 4 (LAC-F [109], [115], [121]; LSM-F [067]; PMG-F [105], [110]).

### MOT-10 confirmed

LAC fresh jumpers 80.3 / 106.1 / 127.2 mm (n=10; 75.9-118.2 sideways, 22.1-55.9 above); PMG 49.3 / 53.5 / 77.5 (n=20); LAC parking spot x 768.7-770.0 over Steps 10-14 and 787.2-791.3 over Steps 36-39; PMG 1.75 mm per wire, 19.2 mm over 12, 40 mm between the display and matrix runs. All 30 fresh jumpers lie horizontal, nearer the camera than the routed position and lower on screen (21 lower-left, 9 lower-right). LSM: 13.3-18.3 mm for six of seven by my centroid choice.

### MOT-11 confirmed

10 fan-out pairs (5 unique), single axis, 0.00 mm off-axis, 0 deg, part alone on screen. Captive leads riding a rigid tween: 9 build pairs by my count (the analyst's 7 leave out LSM-P2 [019]-[020] and LSM-P12 [035]-[036]). The third situation the analyst lists as a side effect occurs 8 times (LAC-F [019] 177.3, [042] 150.5; LAC-P1 [019]; LAC-P2 [012]; PMG-F [037] and PMG-P2 [004] 11.9; LSM-P2 [003] and LSM-P12 [019] 3.4).

Fan-out figures: "3 mm per position" is spacing ADDED. Ribbon pitch goes from 1.7 mm to 4.5-5.3 mm (PMG 12-way), 4.1-4.6 (PMG 9-way), 6.1-9.0 (LAC 6-way), 7.7-13.1 (LAC 4-way), 21.6 (LAC pair). "5.5 mm for 6 or fewer" fits only the 6-way.

### MOT-12 qualified

Reproduced: 45 pose-copy swaps on c-steps in build guides (20 in the Full Builds: LSM 4, LAC 8, PMG 8), 6 more on Transitions (3 in the Full Builds), 11 on c-steps in deconstruction, none with a tween in the same frame. Attach jumps 49.8 / 56.9 / 57.1 / 76.7 mm. Copies: LSM matrix 5; LAC F1 4, F4 3, LCD 4, switch 3, potentiometer 4; PMG display 4, matrix 4, shield 3.

What actually separates cross-fade from tween is whether the wires are already routed to the assembly. Parts whose leads are still free are tweened with the leads riding: switch, potentiometer, push button in isolated views, and the PMG USB plug with its cable stub in full context (PMG-F [057]->[058], 74 parts on screen; PMG-P2 [024]->[025]). The analyst lists the isolated cases as exceptions but not the USB plug. Also: pick-up and one-shot swaps re-orient the sub-assembly by 90-180 deg in 8 of 12 in the Full Builds (buzzer 120 at LAC-F [095], F1 180 at [105] and 90 at [120], LCD 170 at [114], LSM matrix 180 at LSM-F [063], PMG button modules 180 at PMG-F [074] and [076], shield 120 at [100]), which a tween could not show sensibly; attach swaps onto tabs are pure translations with 0 deg (LAC-F [110], [122]; LSM-F [047], [068]; PMG-F [102]), and the last frame of a hook-on flipbook turns 20-23 deg (PMG-F [107], [112]). And once, in deconstruction, a wired bundle is re-posed by a pose write, not a copy swap: LSM-Decon [037], 60-106 mm and 179.5 deg, on a Step N under a step fade.

### MOT-13 confirmed

8 resistor swaps (LSM-F 2, LSM-P1 2, LSM-P12 2, LAC-F 1, LAC-P1 1) plus 3 ribbon splits = 11, 4 unique, no move. The after-model stands at the next step's hover pose: resistors exactly in 7 and within 1.7 mm in 1 (LSM-F [010]); the split ribbon within 3.4 mm of the model used in the next step.

### MOT-14 qualified

The listed cases reproduce (63 stems at LSM-F [086], 3 keys at PMG-F [086], button modules at PMG-F [013], [020], [027], cables at LAC-F [089] and LSM-F [045]). But "the rest of an identical set" is not a general rule: it is used for the two large sets only. Four smaller identical sets are tweened in full: LSM D11 posts x4 (two at [071], two at [073]), LSM D9 x2 together [060], LAC F7 x2 together [090], LAC resistors x2 in consecutive steps [010], [012]. Keys (4) are batched and posts (4) are not, so set size alone does not decide it either.

### MOT-15 confirmed

14 removals (6 unique): 12 tween on a Transition, 2 on the c-step (LSM-P1 and LSM-P12 [002]). Knob 37.6, nut 37.9, washer 37.9; LSM nut 98.8-100.6 at 1600 ms; backing sheet 39.3 / 48.3 / 53.2. All 14 Step N frames carry exactly one arrow and no lead line. For the backing sheet Step 1 is not "part still in place": the sheet fades in under the breadboard while the breadboard is lifted 39-49 mm.

### MOT-16 qualified

My pair classification: LAC-Decon 13 tween-then-hide, 6 tween-and-stay, 25 cross-fade, 2 plain fade; LSM-Decon 17 / 1 displaced-and-hidden / 5 / 1; PMG-Decon 11 displaced and hidden in one frame, 6 more after a Transition leg, 1 tween-and-stay, 4 cross-fade. Within one of the analyst's counts everywhere. Tweened removal travel n=40: min 2.5, quartiles 30.7 / 52.8 / 67.6.

- Direction is the build direction reversed for every matched part that has the same orientation in both guides, except LSM D10 and D3 and LAC F9. (For the potentiometer hardware and the LSM nut the comparison in world axes means nothing: the build fits them in an isolated view with a different orientation.)
- Distance equals the build within 1 mm for 17 distinct parts: PMG H4, H5, H6, H7, H8, H10, H11, H12, H13 (H10 is missing from the analyst's list); LAC F2, F5, F6, F8; LSM D7, D8, capacitor, resistor 2. That is 9 of 12 matched parts in PMG, 4 of 14 in LAC, 4 of 16 in LSM. "Same as the build" describes PMG, not the corpus.
- "Undo two-stage joints in reverse order" is true for PMG (7 of 7) and LAC F2. LSM does not: D3 leaves in one straight 38.4 mm move with no swing, D10 in one straight 48.4 mm move in place of the L-path, the D11 posts in one pull of 70.5-88.8 mm with no 7 mm stage. LAC F9 undoes the straighten and the 33.0 mm drop but not the 103.9 mm approach.

### MOT-17 qualified

65 of 1037 steps carry `transition: fade`, none in PMG: confirmed. The three Full Builds have 14 section cards (LAC 5, LSM 4, PMG 5) and all 14 isolate their subject; context comes back on a Step N in 22 of 23 restores. "Already standing at the hover pose of the step that follows" only has meaning for the 5 cards followed by a tween of the carded part: exact for LAC RTC [014], LAC switch [031], PMG USB [056]; nudged for the LSM capacitor (0.5 mm and 6.0 deg at LSM-F [013]) and stem (1.0 mm at [083]). The other 9 cards introduce a module that is then wired and never hovers.

### MOT-18 qualified

Exact: 800 ms on 1030, 1600 ms on 7 (LSM-F [035]; LSM-P2 [017], [022]; LSM-P12 [033], [038]; LAC-Decon [016], [017]); 922 pause, 115 play; part options tween / fade / fade on 1037 (2 add `animation_attention: none`); camera options and 2D options identical on all; `animationChained` false on all; project flags identical on all 20.

Not true as a "never": 35 frames that are neither c-steps nor Transitions move a visible part by more than 0.5 mm or 0.5 deg, and the camera moves on 34 of them (28 Step N, 5 final views, 1 card). 20 are larger than 10 mm. 14 of those sit under a step fade; 6 do not: LAC-F [042] and LAC-P2 [012] (loose wire 150.5 mm), LSM-P1 [012] (capacitor 70.2 mm), PMG-P3 [001] (H2 40.0 mm), PMG-F [037] and PMG-P2 [004] (wire 11.9 mm). The rule holds where motion is intended: c-steps and Transitions.

Also: the 115 play steps are not all named "Transition"; 111 are, 4 are misspelled (section 4).

### MOT-19 confirmed

LAC Electronics: 2 pause frames, 0 annotations. [000] electronics in one line along world Z. [001] nine panels in one line along Z in the order F9 ... F1, all at Y 920 (F4 928), standing parallel. One instance per part number: F7 appears once although the kit has two.

## 3. Patterns the report missed

1. On screen the hover is never below the seat (0 of 119; above 75, right 23, left 21). Where the physical insertion is from underneath or along a shaft, the author changes the scene `up_axis` or turns the model over.
2. The hover vector is never close to the line of sight: its component along the view axis is at most 75% (median 52%), so at least two thirds of the travel is visible on screen.
3. Lead lines are the motion path: parallel to the hover vector within 3.9 deg and the same length (median ratio 1.00). For L-shaped seats they are 3- and 5-point polylines that trace the corner (LSM D10 at LSM-F [064], LSM-P34 [019], LSM-P4 [005]; LAC F9 at LAC-F [098], LAC-P4 [009]); when the last leg is a 3-8 mm lock or a swing the line covers only the first leg (H11, H12, H14, F2).
4. Annotation type follows the direction of motion: insertions have lead lines and no arrow (116 of 116), removals inside builds have one arrow and no lead line (14 of 14), deconstruction removals have 1-2 arrows, refits in LAC-Decon Steps 16-18 have a lead line again.
5. Constant time, not constant speed: every leg is 800 ms whatever the distance, so speed runs from 4 mm/s (a 3 mm swing leg) to 174 mm/s (H7, 139.4 mm), median 68 mm/s.
6. The first frame after the title page is a bulk re-pose: the finished model is hidden and hover poses are written in the same frame (50 of the 99 fade-in insertions are staged there). A player has to apply pose changes of parts that are hidden or being hidden without animating them, or cut.
7. Cross-fade or tween is decided by the far end of the wire (see MOT-12), and pick-up swaps include a 90-180 deg re-orientation (8 of 12) while attach swaps onto tabs are a straight 50-107 mm translation shown like a normal hover, with 2-4 lead lines or an arrow on the Step N.
8. Identical pairs go in as one group with one vector (F7 x2 80.3 mm, D9 x2 64.6 mm, first two D11 posts 81.7 mm); the second pair of D11 posts shares a step but not a distance (77.4 and 83.1 mm at LSM-F [073]).

## 4. Anomalies (not conventions)

- Step names: `Ttansition` (LAC-F [053], LAC-P2 [023]), `Transititon` (LAC-Decon [002]), `Transiton` (LSM-Decon [038]), `Copmleted View` (LSM-P34 [042]), `Step 14C` (LAC-P1), `Step 20C` (LSM-P12), `Completed Build` in LSM-P2 and LSM-P12 against `Completed View` elsewhere.
- Numbering: LSM-P4 [016] `Step 8` is followed by [017] `Step 9c` and there is no `Step 8c` or `Step 9`; PMG-P1 `Step 14` [032] has no c frame; PMG-Decon `Step 23` [059] has no c frame; LAC-Decon has a stray `Step 41` at [104] before `Step 40` [105], and two frames named `Step 45c` ([120], [122]) with no `Step 45`.
- Two `pause` Transitions in LAC-Decon ([033], [118]); [118] carries a 21.7 mm part tween.
- PMG H14 is swung 12.6 deg from a 10.1 deg hover tilt and corrected by 2.5 deg on the final view.
- LSM capacitor leans 5.9 deg in Part 1 and Part 1+2 and is straightened by a visible 6.0 deg turn in the Full Build [013].
- LSM-P34 stems rise 9.7 mm on Step 18c [041] and drop again on the final view [042].

## 5. Numeric defaults

| Default | Checked value | Status |
|---|---|---|
| Step duration | 800 ms (1030 of 1037) | confirmed |
| Part move / show / hide | tween / fade / fade (1037 of 1037) | confirmed |
| Camera during part motion | locked on c-steps (424 of 424) and Transitions (68 of 68); not on Step N entries (34 frames with both) | narrowed |
| Legs | one per authored step; one press plays all legs, 1.6 s or 2.4 s | reworded |
| Threaded spin | median 175.9 deg, 8 of 11 at 170 deg or more, 3 at 115-124; 1600 ms on 5 of 11 | confirmed |
| Hover, board or passive | 35 mm (22 values 29.1-44.1, median 34.5) | confirmed |
| Hover, breadboard | 47 mm (39.3-49.2, median 46.9) | confirmed |
| Hover, USB plug | 23 mm (22.9, one part, two copies) | confirmed |
| Hover, panel-mount with leads | 80 mm; 7 copies, 3 unique (79.1, 81.2, 102.5-103.2); about 1.2 x body-plus-leads when the leads trail along the travel | basis corrected |
| Hover, washer / nut / knob | 60 mm for LAC (55.9-61.3); 80-83 mm for the LSM nut; all 9: median 61.3 | widened |
| Hover, face-on panel | 65 mm (42.0-69.4, median 64.7 unique, 64.3 all copies) | 60 understates |
| Hover, lengthwise | 1.0 x extent only for true lengthwise sliders (10 of 22, 0.83-1.05); otherwise 81 mm median, quartiles 55 / 94 | narrowed |
| Hover, fallback | 60 mm (median 60.9 unique, 60.5 all) | confirmed |
| Tilt at hover | swing angle; 7 parts tilted at hover, 7.9-23.6 deg, median 18.1 | F9 excluded |
| Swing pivot | the engaged edge for H5, H6, H7 (0.99-1.00), D3 0.95, F2 0.92; H10 0.75, H14 0.48 | narrowed |
| Stored pivot | non-zero origin on 373 of 576 rotation writes | 557 overstated |
| Push-home stage | 7.0 mm (4 posts, 3 copies) | confirmed |
| Flex | 15 deg (15.1, 16.0) | confirmed |
| Removal travel in a build | 38 mm (37.6-37.9); 99-101 mm for the LSM nut | confirmed |
| Deconstruction travel | build direction reversed; build distance reused for 17 of 42 distinct parts, 9 of them PMG | narrowed |
| Loose wire parking | PMG 49.3 / 53.5 / 77.5; LAC 80.3 / 106.1 / 127.2; run spread within 2.2 mm | confirmed |
| Loose wire at target, LSM | 13-18 mm for 6 of 7 | confirmed |
| Ribbon fan-out | resulting pitch 4.1-5.3 mm for 9-12 wires, 6.1-9.0 for 6, 7.7-13.1 for 4, 21.6 for a pair (from 1.7 mm) | reworded |
| Wire connection | cross-fade in one 800 ms step, no lead line or arrow | confirmed |
| Wired sub-assembly attach copy | 49.8 / 56.9 / 57.1 / 76.7 mm; 3 flipbooks | confirmed |
