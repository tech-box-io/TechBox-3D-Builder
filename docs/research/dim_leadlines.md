# Dimension report: red lead lines and 3D arrows

Scope: all 20 published TechBox Cadasio guides (LSM x8, LAC x7, PMG x5). Step indices such as [012] are the digest's viewer indices; thumbnails are `thumbs/<guide>/NNN.jpg`.

## 0. Method and caveats

- **Own replay of the raw payloads** (`reports/_work_dim_leadlines/core2.py`, `extract2.py`): every authored step, hidden ones included, is replayed; visibility is taken per solid (the digest's parent-level visibility is unreliable for wood panels and pose copies, as several reader reports noted).
- **Where a line or arrow really is.** Each line/arrow end is tied to a part through a `links` entry on that part (`type: translation`, target `GL<line id>/AS` or `/AE`, with a point in the part's local frame). I rebuilt every end from that link and the part's transform at that step. The transform model was checked against stored points: a part's `position` replaces the translation of its CAD transform and its `rotation` quaternion replaces the CAD rotation. With that model, link-derived ends equal the stored `points` within 0.6 mm on 520 of 726 line ends and within 3 mm on 680; 14 ends differ by more than 3 mm (stored points and anchors disagree; listed in section 12; lengths in this report use the anchors); 32 ends have no usable link (ids missing from the CAD tree, or free ends).
- **Travel (T)** of a line is the movement of its two anchors relative to each other between the frame on which the line appears and the next frame. For wired sub-assemblies that are cross-faded instead of tweened, T is the offset between the hovering model copy and the copy that replaces it (`poseswap.py`). 360 of 363 line showings have a measurable T.
- **Duplication.** Part guides are cut from the full builds, so most content is counted two to four times in "all 20" figures. I give both "all 20 guides" and "3 full builds" (LAC, LSM, PMG full builds = the unique construction content; LSM Parts 1, 2 and 1+2 are an older authoring of the same steps and are called out where they differ).
- **Renders looked at:** 50 frames, listed in section 14, across all three kits, plus full-resolution crops from `thumbs_raw` for line thickness, dash style and where lines end.
- **Limits.** I could not open the live viewer. Whether a line shrinks with the part during the 800 ms tween, and whether "dashed" lines are drawn dashed live, are inferred from data and saved renders only. Feature-level statements (tab tip, slot, pin tip) come from anchor coordinates against solid bounding boxes plus the renders; there is no mesh-level check.

## 1. Headline numbers

- **363 lead-line showings** on 155 frames (149 "Step N" frames, 6 auto "Transition" frames, 0 "Step Nc" frames) and **106 arrow showings** on 97 frames, in the 20 guides.
- Unique construction content (3 full builds): **149 lines on 65 frames** (62 Step N + 3 Transition) and **12 arrows on 11 frames**.
- Deconstruction (3 guides): **77 arrows on 70 frames, 3 lead lines** (all three on the only steps of a take-apart guide where something is fitted back on).
- `lac_electronics` (parts overview) shows neither.

| guide | viewer frames | Step N frames | lead-line showings | frames with new lines (Step N / Transition / Step Nc) | lines per frame {n: frames} | arrow showings | frames with arrows (Step N / Transition / Step Nc) |
|---|---|---|---|---|---|---|---|
| LAC deconstruction | 130 | 47 | 3 | 3 (3 / 0 / 0) | {1: 3} | 22 | 20 (19 / 0 / 1) |
| LAC electronics | 2 | 0 | 0 | 0 (0 / 0 / 0) | - | 0 | 0 (0 / 0 / 0) |
| LAC full build | 131 | 57 | 44 | 20 (20 / 0 / 0) | {1: 6, 2: 9, 4: 5} | 7 | 6 (6 / 0 / 0) |
| LSM deconstruction | 69 | 24 | 0 | 0 (0 / 0 / 0) | - | 24 | 21 (21 / 0 / 0) |
| LSM full build | 88 | 38 | 57 | 21 (21 / 0 / 0) | {1: 3, 2: 9, 4: 9} | 4 | 4 (4 / 0 / 0) |
| LSM part 1 | 19 | 8 | 14 | 5 (5 / 0 / 0) | {2: 3, 4: 2} | 1 | 1 (1 / 0 / 0) |
| LSM part 2 | 31 | 13 | 2 | 2 (2 / 0 / 0) | {1: 2} | 2 | 2 (2 / 0 / 0) |
| LSM part 3 | 13 | 5 | 14 | 4 (4 / 0 / 0) | {2: 2, 4: 1, 6: 1} | 1 | 1 (1 / 0 / 0) |
| LSM part 3 4 | 43 | 18 | 43 | 14 (14 / 0 / 0) | {1: 1, 2: 6, 4: 6, 6: 1} | 2 | 2 (2 / 0 / 0) |
| LSM part 4 | 29 | 12 | 29 | 10 (10 / 0 / 0) | {1: 1, 2: 4, 4: 5} | 0 | 0 (0 / 0 / 0) |
| LSM part 1 2 | 47 | 21 | 17 | 8 (8 / 0 / 0) | {1: 3, 2: 3, 4: 2} | 3 | 3 (3 / 0 / 0) |
| LAC part 2 | 42 | 18 | 5 | 5 (5 / 0 / 0) | {1: 5} | 3 | 3 (3 / 0 / 0) |
| LAC part 3 | 21 | 8 | 0 | 0 (0 / 0 / 0) | - | 0 | 0 (0 / 0 / 0) |
| LAC part 4 | 42 | 17 | 27 | 10 (10 / 0 / 0) | {1: 1, 2: 5, 4: 4} | 3 | 2 (2 / 0 / 0) |
| LAC  part 1 | 32 | 14 | 12 | 5 (5 / 0 / 0) | {2: 4, 4: 1} | 1 | 1 (1 / 0 / 0) |
| PMG deconstruction | 61 | 23 | 0 | 0 (0 / 0 / 0) | - | 31 | 29 (20 / 9 / 0) |
| PMG part 1 | 34 | 14 | 4 | 1 (1 / 0 / 0) | {4: 1} | 0 | 0 (0 / 0 / 0) |
| PMG part 2 | 27 | 11 | 1 | 1 (1 / 0 / 0) | {1: 1} | 0 | 0 (0 / 0 / 0) |
| PMG part 3 | 59 | 26 | 43 | 22 (19 / 3 / 0) | {1: 5, 2: 15, 4: 2} | 1 | 1 (1 / 0 / 0) |
| PMG full build | 117 | 51 | 48 | 24 (21 / 3 / 0) | {1: 6, 2: 15, 4: 3} | 1 | 1 (1 / 0 / 0) |

Lines per frame over all 20 guides: {1: 37 frames, 2: 75, 4: 41, 6: 2}. In the three full builds: {1: 15, 2: 33, 4: 17}. Never 3 or 5; 6 occurs only in two re-cuts of one LSM step (section 3).

## 2. Which steps get lead lines, which get arrows, which get neither

Every "Step N" frame was classified by what happens between it and its "Step Nc" (leaf-level tracking of moves, appearances and disappearances).

**3 full builds (146 Step N frames):**

| what happens between Step N and Step Nc | steps | with lead lines | with arrow(s) | with eye icon | with text label | neither line nor arrow |
|---|---|---|---|---|---|---|
| rigid part tweens to its seat | 59 | 56 | 1 | 7 | 7 | 2 |
| part tweens away and is hidden (removal) | 6 | 0 | 6 | 0 | 0 | 0 |
| wired module / sub-assembly cross-fades to a new pose | 20 | 6 | 4 | 12 | 0 | 10 |
| wire: loose model swapped for routed model | 49 | 0 | 0 | 42 | 48 | 49 |
| ribbon wires slide apart (prep) | 5 | 0 | 0 | 4 | 0 | 5 |
| resistor legs: straight model swapped for bent | 3 | 0 | 0 | 3 | 1 | 3 |
| part only fades in | 3 | 0 | 0 | 2 | 0 | 3 |
| nothing changes | 1 | 0 | 0 | 1 | 0 | 1 |
| **total** | 146 | 62 | 11 | 71 | 56 | 73 |

**All 16 construction guides (331 Step N frames; parts repeat the full builds):**

| what happens between Step N and Step Nc | steps | with lead lines | with arrow(s) | with eye icon | with text label | neither line nor arrow |
|---|---|---|---|---|---|---|
| rigid part tweens to its seat | 140 | 132 | 4 | 16 | 19 | 4 |
| part tweens away and is hidden (removal) | 12 | 0 | 12 | 0 | 0 | 0 |
| wired module / sub-assembly cross-fades to a new pose | 47 | 14 | 11 | 28 | 2 | 23 |
| wire: loose model swapped for routed model | 104 | 0 | 0 | 85 | 101 | 104 |
| ribbon wires slide apart (prep) | 10 | 0 | 0 | 8 | 0 | 10 |
| resistor legs: straight model swapped for bent | 8 | 0 | 0 | 8 | 2 | 8 |
| part only fades in | 8 | 0 | 0 | 6 | 0 | 8 |
| nothing changes | 2 | 0 | 0 | 2 | 0 | 2 |
| **total** | 331 | 146 | 27 | 153 | 124 | 159 |

**3 deconstruction guides (94 Step N frames):**

| what happens between Step N and Step Nc | steps | with lead lines | with arrow(s) | with eye icon | with text label | neither line nor arrow |
|---|---|---|---|---|---|---|
| rigid part tweens to its seat | 7 | 3 | 4 | 0 | 0 | 0 |
| part tweens away and is hidden (removal) | 35 | 0 | 35 | 11 | 0 | 0 |
| tween plus a model swap | 1 | 0 | 1 | 1 | 0 | 0 |
| wired module / sub-assembly cross-fades to a new pose | 11 | 0 | 6 | 7 | 0 | 5 |
| wire: loose model swapped for routed model | 23 | 0 | 0 | 23 | 4 | 23 |
| part only fades out (may slide while fading) | 16 | 0 | 14 | 5 | 0 | 2 |
| nothing changes | 1 | 0 | 0 | 1 | 0 | 1 |
| **total** | 94 | 3 | 60 | 48 | 4 | 31 |

What this shows:

- **Rigid part that tweens onto its seat -> lead lines.** 56 of 59 such steps in the full builds (132 of 140 over all construction guides). The three without: LAC Step 42 [092] (spread the two F7 posts: two opposed arrows), LAC Step 44 [096] (close the posts on the buzzer: two eye icons), LSM Step 38 [085] (63 stems fade in seated as a "repeat"; the 2 mm move recorded there is data residue).
- **A wire being connected never gets a lead line or an arrow.** 0 of 49 wire-end steps in the full builds, 0 of 104 over all construction guides; likewise 0 of 23 single-wire unplug steps in the take-apart guides. Wires are shown by a model swap plus labels and/or an eye icon. Ribbon splitting (5 steps) and resistor-leg bending (3 steps) get neither either. (Wire bundles that are slid away in a take-apart guide do get an arrow: PMG deconstruction Steps 18 and 22, LSM deconstruction Step 15.)
- **Removal inside a build -> one arrow, no line.** 6 of 6 in the full builds (peel backing LAC Step 1 / LSM Step 1; knob, nut, washer off LAC Steps 22-24; nut off LSM Step 16).
- **Wired sub-assemblies that are cross-faded between poses** (20 steps in the full builds) split three ways: 6 get lead lines (a plywood panel or PCB being seated on tabs/notches: LAC Steps 49, 52, 54; LSM Step 30; PMG Steps 48, 50), 4 get an arrow (carried or stood in place without tab pairs being pointed out: LAC Step 47, LSM Steps 21 and 23, PMG Step 46), 10 get only eye icons (pick-up steps and small drop-in modules: buzzer, button modules).
- **Lines and arrows do not share a frame.** 0 of 146 full-build Step N frames carry both. The single case in all 20 guides is LSM Part 1+2 Step 20 [041], where a stray 8.8 mm line from an earlier step is left switched on inside the button.
- **Deconstruction uses arrows, not lines.** 60 of 94 Step N frames carry an arrow; the 3 lead lines are LAC deconstruction Steps 16-18 [043] [045] [047], where washer, nut and knob are refitted to the loose potentiometer.

Other annotations on the 155 frames that introduce lines: none on 122, text labels (breadboard hole names) on 16, eye icon on 9, both on 3, an inset picture on 4, the stray arrow frame 1.

## 3. How many lines

By joint class, 3 full builds:

| joint class | frames | lines | lines per frame {n: frames} | travel T mm (median) | L / T range (median) | median T − L mm |
|---|---|---|---|---|---|---|
| 2-lead component into breadboard | 5 | 10 | {2: 5} | 29–40 (32) | 0.92–1.15 (1.08) | -3.1 |
| axial part (shaft/body/plug/stem) | 9 | 9 | {1: 9} | 23–103 (61) | 0.86–1.26 (1.16) | -9.3 |
| breadboard onto base plate | 2 | 8 | {4: 2} | 47–49 (48) | 1.02–1.02 (1.02) | -1.0 |
| pin-header board into holes/sockets | 4 | 12 | {2: 2, 4: 2} | 30–44 (37) | 0.86–1.11 (1.07) | -2.5 |
| plywood tab/slot panel or post | 37 | 90 | {1: 6, 2: 20, 4: 11} | 7–139 (65) | 0.47–3.18 (0.99) | +0.3 |
| wired module onto brackets (pose swap) | 5 | 10 | {2: 5} | 8–23 (11) | 0.97–1.20 (1.08) | -0.9 |
| wired panel sub-assembly (pose swap) | 3 | 10 | {2: 1, 4: 2} | 50–77 (57) | 0.93–1.00 (0.96) | +3.4 |

All 20 guides:

| joint class | frames | lines | lines per frame {n: frames} | travel T mm (median) | L / T range (median) | median T − L mm |
|---|---|---|---|---|---|---|
| 2-lead component into breadboard | 13 | 26 | {2: 13} | 29–40 (33) | 0.83–1.15 (1.08) | -3.1 |
| axial part (shaft/body/plug/stem) | 24 | 24 | {1: 24} | 23–103 (61) | 0.86–1.26 (1.13) | -6.7 |
| breadboard onto base plate | 5 | 20 | {4: 5} | 39–49 (47) | 1.00–1.02 (1.02) | -1.0 |
| pin-header board into holes/sockets | 9 | 28 | {2: 4, 4: 5} | 30–44 (35) | 0.86–1.11 (1.10) | -3.5 |
| plywood tab/slot panel or post | 86 | 222 | {1: 12, 2: 45, 4: 27, 6: 2} | 7–139 (64) | 0.47–3.18 (1.00) | +0.3 |
| wired module onto brackets (pose swap) | 10 | 20 | {2: 10} | 8–23 (11) | 0.97–1.20 (1.08) | -0.9 |
| wired panel sub-assembly (pose swap) | 8 | 23 | {1: 1, 2: 3, 4: 4} | 50–77 (57) | 0.93–1.00 (0.96) | +3.4 |

Per part type (checked against renders):

| part being seated | lines | which features | evidence |
|---|---|---|---|
| Axial part: round shaft through a hole, washer / nut / knob onto a shaft, rocker-switch body into a rectangular cut-out, USB plug into socket, LED stem onto an LED | **1**, on the axis | centre of the body or shaft end to centre of the hole / shaft | LAC Steps 15, 25-28 ([032] [055] [057] [059] [061]); LSM Steps 17, 18, 37 ([037] [039] [083]); PMG Step 25 [057]. 9 of 9 steps in the full builds, 24 of 24 over all guides. Leads hanging from the part get no line. |
| Single-tab or single-tongue plywood part | **1** | the one tab tip to its slot | PMG H2, H3 (Steps 26, 27), H9 key (Step 38), H11, H12 hook tab (Steps 42, 43) |
| Two-lead component (resistor, capacitor) | **2**, one per lead | lead tip to its breadboard hole | LAC Steps 5, 6; LSM Steps 5, 6, 8 (5 of 5 full-build steps; 13 of 13 overall) |
| Pin-header board | **2 or 4, never one per pin** | LAC Nano (30 pins): the 2 diagonally opposite corner pins [006]; LAC RTC module (6-pin single row): both end pins [015]; LSM Nano and PMG Nano: the 4 corner pins ([006], [002]) | anchors sit at 80 % of the board diagonal in every Nano case |
| Flat body onto a plate (breadboard onto base) | **4** | the 4 bottom corners to the 4 corner cut-outs / marks in the plate | LAC Step 2 [004], LSM Step 2 [004]; LSM Part 1 [003] |
| Plywood panel with tabs/slots | **1, 2 or 4**: one line per tab/slot pair engaged in that stage, up to 4 | tab tip to slot | 37 frames in the full builds: {1: 6, 2: 20, 4: 11} |
| Two identical parts in one step | lines per part, total still 2 or 4 | 2 x F7 posts: 1 line each [090]; 2 x D11 posts: 1 each [071]; 2 x D9 supports: 2 each [060] | |

Details on plywood:

- **When 4 or fewer tab/slot pairs engage, each gets a line** (e.g. LSM D4 [048]: 2 tabs on D2 + 2 on D1 = 4 lines; LAC F1 [121]: 2 on F4 + 2 on F3; PMG H4 [063]: 2 on H2 + 2 on H3; LSM D7/D8 [078] [080]: 4 posts, 4 lines).
- **When more than 4 pairs engage, 4 lines are shown, two on each of two neighbouring panels.** LAC F5 [123]: the panel has 8 slots (2 per edge) and three neighbours are already in place (F3, F1, F4), so up to 6 pairs engage; lines are drawn only for the 2 tabs on F3 and the 2 on F1. LAC F6 [128]: 8 slots, all four neighbours in place (F1, F2, F3, F4); lines for the 2 tabs on F1 and the 2 on F2 only. LSM D5: 6 engaged pairs; the Full Build [057] shows 4, while Part 3 [010] and Part 3+4 [012] show all 6 (the only frames in the study with more than 4 lines).
- **Only the pairs that engage in the current stage are drawn.** Hook-and-swing panels get 2 lines for the edge that hooks in (LSM D3 Step 24 [053]; PMG H5/H6/H7/H10 Steps 29, 31, 35, 40; LAC F2 Step 56 [125]) and 2 fresh lines for the edge that closes in the next step or Transition (LSM Step 25 [055]; PMG Steps 30, 32, 36, 41 and Transition [114]).
- Not every contact is drawn even below 4: PMG H8 [081] shows 2 (bottom tabs only); H11/H12 show 1 (the hook tab).

Lines within one frame are parallel and of near-equal length: of 118 multi-line frames, the largest angle between any two lines is <= 2 deg in 99 and <= 5 deg in 113 (the others are the swing steps).

## 4. What each end is anchored to

- **Both ends are tied to parts.** 333 of 363 line showings have a part link at both ends; 25 have one end whose object id is not in the exported CAD tree (24 are breadboard-hole ends in LAC and the LSM Full Build, 1 is a wall end in LSM Step 31); 3 have a free end (LSM Part 3+4 Steps 7 and 12); 2 have object ids but no link (LSM Part 3+4 Step 4).
- **Granularity is one solid plus a local point.** 692 of 726 ends are linked to a single solid: an individual header pin (`nano-Surface-Offset3[117]`), a resistor leg (`Resistor stem 3-1`), a capacitor leg, a connector strip, or the one body solid of a plywood panel (`F3-Cut-Extrude1`, `H10-Cut-Extrude1`). The tab or slot is identified only by the local point, not by a separate object.
- **Direction of authoring is not a convention.** The first point is on the moving part in 215 of 320 tweened lines (67 %); PMG 33 of 40, LAC 23 of 34, LSM 27 of 55. Treat lines as undirected.
- **One end is on a male feature tip, the other in the matching female feature.** Seen in every render inspected: pin tip -> hole ([006] [002]), lead tip -> hole ([009] crop), tab tip -> slot ([090] [063] [123] [128]), slot -> post tip when the slotted plate is the mover ([078]), shaft end -> hole centre ([055] [037]). The male feature may be on either part: tabs on the seated walls and slots in the incoming panel (LSM D4 [048], LAC F6 [128], LAC F4 [109]) or tabs on the incoming part (LAC F7 [090], PMG H2/H3, LSM D11 posts [071]).
- **Where exactly the female end sits** varies by author and kit:
  - Breadboard holes: 7.0 mm below the board's top face in LAC (all four insertion steps end on one plane, Y = 890.1 mm) and in LSM Part 1 (6.7-7.0 mm); 7.4 mm in the LSM Full Build. That is 1.4-5 mm deeper than the seated pin tip, so the line is longer than the travel. One step (LSM Full Build Step 5 [010]) ends at the surface instead (0.2 mm).
  - PMG socket strips [002]: 1.9-4.9 mm below the socket top.
  - Slots in 3 mm plywood crossed through their thickness (74 lines): the line ends on the entry face in 29, on the exit face in 30, in between in 15. When the slotted plate is the moving part (114 lines) the line reaches its far face in 66, so a red dot shows inside the slot from the outside ([078] crop, [128] crop).
- **Depth-tested 3D lines.** Lines are hidden where geometry is in front: behind the panel in [055], inside wall thickness in [057], behind the breadboard in [004]. Whatever runs inside a part is invisible, which is why over-long anchors (below) do no visual harm.

## 5. Direction and length

Measured on the 360 line showings with a travel (350 two-point lines for the angle):

| measure | all 20 guides | 3 full builds |
|---|---|---|
| angle between line and travel, median | 0.4 deg | 0.3 deg |
| angle <= 1 deg | 270 / 350 (77 %) | 108 / 145 (74 %) |
| angle <= 2 deg | 300 / 350 (86 %) | 122 / 145 (84 %) |
| angle <= 5 deg | 338 / 350 (97 %) | 139 / 145 (96 %) |
| largest angle | 10.7 deg | 10.7 deg |
| L / T median (25th-75th percentile) | 1.00 (0.94-1.09) | 1.00 (0.94-1.07) |
| L within 5 % of T | 145 / 360 (40 %) | 65 / 149 (44 %) |
| L within 10 % of T | 226 / 360 (63 %) | 103 / 149 (69 %) |
| L within 15 % of T | 282 / 360 (78 %) | 122 / 149 (82 %) |
| T - L within +-6 mm | 273 / 360 (76 %) | 118 / 149 (79 %) |
| line length, median (10th-90th percentile) | 49 mm (17-104) | 50 mm (16-106) |
| travel, median (10th-90th percentile) | 53 mm (16-83) | 54 mm (11-94) |

- **Always parallel to the travel** within hand-placement error. The 12 showings above 5 deg are all rotation stages or pose swaps: LSM Step 25 (swing D3 shut, 6.0), PMG Step 41 (H10 swing, 5.1-6.1), LAC Step 52 (LCD onto hooks, 5.6), PMG Transition [111] (matrix second stage, 8.9-10.7).
- **Length is about the travel, but it is the gap between the two mating features, not a copy of the hover offset.** T - L has three clusters: about 0 (72 showings within +-0.5 mm: both anchors coincide when seated, e.g. LAC F8 [111] 94.2 / 94.2, LSM D9 [060] 64.6 / 64.6, PMG hinge stages), about +3.4 mm (84 showings between +2.4 and +5.5: the line stops one plywood thickness short because the tab travels on through the panel, e.g. PMG H2 36.6 / 40.0, H3 39.8 / 43.2, H4 61.5 / 65.0, key 104.2 / 107.7, H11 50.1 / 53.1, H12 41.0 / 44.5; LAC F7 75.4-76.9 / 80.3, F6 63.4-64.1 / 67.5), and -0.5 to -6 mm (92 showings: the line runs past the seated tip into a hole, e.g. LAC Nano 41.2 / 39.8, resistors 40.1-43.2 / 37.1-40.0, RTC 37.2 / 33.6).
- **Large departures have a mechanical reason or are mistakes:**
  - Part passes far through the receiving feature: the line still ends at that feature. LSM D11 posts through D6: 37-44 mm line for 77-83 mm travel (L/T 0.47-0.54) [071] [073]; LSM D7 onto the posts: 49-50 / 67.8 [078].
  - Axial parts anchored on their body rather than their leading end: LAC switch 69.5 / 81.2; pot 91.8 / 79.1; washer, nut, knob 75.4 / 61.3, 66.7 / 55.9, 76.5 / 60.5 (L/T 1.16-1.26); PMG USB 28.5 / 22.9.
  - Short "marker" lines where the remaining travel is tiny: LSM Step 34 [075] 15.6-17.5 mm for a 7.0 mm push; LAC Step 46 [102] 7.3 mm for 10.7 mm.
  - Mis-anchored lines (section 12).
- PMG, the newest kit, is the most exact: 38 of 48 lines have L/T between 0.90 and 1.05; 25 have T - L within +-1 mm and 11 are T minus 2.9-3.6 mm.

## 6. Paths that are not a single straight move

- **Two-leg path -> polyline that traces the path of the tab tip.** 4 distinct lines in 2 distinct steps (10 showings): LSM Step 29 [064] (D10 clip: 3 points, 21.8-22.0 mm up then 38.2 mm across, for a motion of 21.7 mm up in an auto Transition then 37.9 mm across; in Part 4's copy 19.6-20.6 + 41.4-41.9 mm for a 19.3 + 41.1 mm motion) and LAC Step 45 [098] (F9: 103.8-107.5 mm horizontal run then a 25.7-31.5 mm drop into the slots, for a 103.9 mm slide followed by a drop-and-tilt; 3 and 5 points, the 5-point one starts with a 0.1 mm and a 4.7 mm click artefact). End-to-end length equals the total travel (44.0 vs 43.7 mm; 108.5-111.9 vs 107.0-110.9 mm).
- **Rotation (swing) stage -> short straight lines between the tab/slot pairs that are about to close**, i.e. the chord of the arc: LSM Step 25 [055] 12.7-15.8 mm; PMG Step 30 [067] 56.8, Step 32 43.9, Step 36 28.5, Step 41 8.7 mm; LAC Step 46 [102] 7.3 mm. No curved line or rotation arrow exists anywhere.
- **Two-stage seats get fresh lines per stage.** The first stage's lines are removed and new ones for the second stage appear on the next numbered step (LSM Steps 24/25; PMG Steps 29/30, 31/32, 35/36, 40/41) or on the auto Transition between Step N and Step Nc (PMG [106], [111], [114]: 6 Transition frames with lines over PMG Full Build and Part 3).
- **Cross-faded wired sub-assemblies are treated as if they tweened.** For the 40 lines on such frames the line vector matches the offset to the next pose copy: L/T 0.93-1.20, angle 0-5.6 deg to the next pose except the PMG matrix second stage at 8.9-10.7 deg (LAC F4 46.4-49.5 / 49.8; LAC F1 73.3 / 76.7; LSM matrix + D10 56.1-57.2 / 57.1; PMG display 11.9-12.2 / 11.1 then 9.3-9.6 / 8.0; PMG matrix 20.4-21.2 / 20.4 then 10.8 / 10.8-11.1).

## 7. Style

- Colour `#ff0000`: 363 of 363 shown (and all 958 line objects defined in the 20 projects).
- `scale` 5 with `world_units: false` on 363 of 363: a constant on-screen width that does not change with zoom. Measured on 144 full-resolution saved renders: the saturated core is 2-3 px wide (about 4-5 px including anti-aliased edges) at both 2559 px and 3840 px image widths and at camera distances from 173 to 436 mm. On the 1400 px thumbnails that is about 2 px.
- No arrowhead, no end markers, no outline; straight two-point segments in 353 of 363 showings (the rest are the polylines above).
- Stored style is `solid` on 327 and `dashed` (dash 10 / gap 5) on 36 showings (LSM only: Part 1 [005] [009] [016], Part 2 [021], Part 1+2, and the D7/D8 steps of Part 4, Part 3+4 and the Full Build [078] [080]). **All 36 are drawn solid in the saved renders** (checked at full resolution on LSM Full Build [078], Part 1 [009], Part 2 [021]). 5 `dotted` lines exist and are never shown. Treat solid as the convention and the dashed flag as an anomaly.
- Lines sit in the scene and are occluded by parts (section 4).
- Risk seen in renders: the line colour is the same family as red wires and the red breadboard rail ([032] line next to a red lead; [037] next to the button's red lead).

## 8. Lifetime and what happens in "Step Nc"

- **One frame.** 359 of 363 line showings are visible on exactly one viewer frame and are switched off on the next. No line is ever switched on by a "Step Nc" frame.
- Exception: the two second-stage lines of PMG Step 51 (Part 3 Step 26) appear on the auto Transition [114] / [056] and are still flagged visible on Step 51c / 26c [115] / [057]; they are removed at Completed View. In the saved render [115] nothing red is visible.
- Because both ends follow their parts, a line would collapse to its residual length if it were left on after seating: median 3.5 mm, <= 5 mm for 214 of 320 tweened lines. The viewer hides it in the same 800 ms as the part moves (show/hide = fade).
- Arrows: 106 of 106 live one frame.

## 9. Arrows

### 9.1 When

| use | where | count |
|---|---|---|
| Remove a part during a build (arrow, then an auto Transition slides the part off, then Step Nc hides it) | LAC Step 1 [001], Steps 22-24 [046] [049] [052]; LSM Step 1 [001], Step 16 [034] | 6 of 6 removal steps in the full builds |
| Flex / spread by hand | LAC Step 42 [092]: two opposed arrows on the two F7 posts | 1 step (also LAC deconstruction Step 26 [070]) |
| Carry or place a wired sub-assembly (pose swap, nothing tweens) | LAC Step 47 [104] (front panel carried across, with eye icon); LSM Step 21 [046] (D2 panel onto base), Step 23 [050] (matrix carried outside, with eye icon); PMG Step 46 [101] (shield down onto H4) | 4 of 20 pose-swap steps in the full builds |
| Take-apart guides: every part that is pulled off | all three deconstruction guides | 60 of 94 Step N frames, plus 9 auto Transition frames in PMG (second stage of a two-stage removal) and 1 mis-named frame in LAC |

Arrows are not used for: seating a part (lines), connecting or unplugging a single wire (0 of 127 wire-swap steps in all guides), turning a knob (LAC Step 29 [063] has only an eye icon), spinning nuts. There is no rotation or curved arrow: all 176 arrow objects defined in the 20 projects, shown or not, are sub-type `straight`.

### 9.2 Geometry and style

- Straight, `#ff0000`, opacity 1: 106 of 106. Rendered as a flat unlit red shape with no outline ([001] LAC deconstruction, [025] [028] PMG deconstruction).
- Proportions: body width : head width : head length = **5 : 20 : 17** on 74 of 106 showings (69 of the 89 in the full builds + deconstruction guides); **5 : 20 : 15** on 14 (LSM); 11 other one-off combinations on the remaining 18 (3:9:10, 6:24:22, 5:15:10, 4:15:10, 4:15:14, 5:15:17, 7:21:21, 5:15:14, 4:12:10, 5:20:10, 2:10:17).
- These numbers are multiplied by a per-arrow `scale` set by eye (LAC median 0.48, LSM 0.37, PMG 0.057; the scene units differ per kit). Converted to millimetres the arrows are world-sized objects: **body 4.3 mm median (2.6-7.8 mm 10th-90th percentile), head width 16.7 mm, head length 14.4 mm**. Unlike lead lines they grow and shrink with zoom. Head length is 28 % of arrow length at the median.
- Length: median 51 mm (32-102 mm 10th-90th percentile; min 15.8, max 116.1).
- Head at the end point on 104 of 106; 2 are authored with the head at the start (LSM Step 21 and its Part 3+4 copy).
- **One arrow per moving unit.** 88 frames have one arrow, 9 have two, none has more. Two arrows mean two parts (LSM deconstruction Steps 6, 7, 10; LAC deconstruction Step 28; PMG deconstruction Step 22 for two wire bundles) or an opposed pair (LAC Step 42, LAC deconstruction Step 26); PMG deconstruction Step 1 has two overlapping arrows by mistake. One arrow stands for a whole group of identical parts (4 piano keys [028], 64 stems, 4 button modules, 5 wires).
- **Direction = direction the part is about to move.** 87 arrows are followed by a motion of the part (tween in the next frame, or a slide while fading out): 79 are within 12 deg of that motion (median 1.6-2.0 deg). The other 8: 3 show the main pull while the first stage is an unhook or straighten (LAC deconstruction Steps 24, 28), 3 are the second arrow of an opposed pair, 2 sit on a step whose only "motion" is a 1.2 mm data residue. 17 arrows precede a pose swap: 12 are within 12 deg of the offset between the two poses, 5 within 18-26 deg. 2 have no following motion (LSM deconstruction Steps 4 and 20: the part just fades).
- **Length is only loosely the travel.** Arrow length / travel for the 79 aligned arrows: median 0.96, 25th-75th percentile 0.76-1.31, 44 of 79 within 0.75-1.35, range 0.4-12.8 (the large values are short unhook stages). For carried sub-assemblies the arrow is much shorter than the move (102 mm for 184 mm; 102 mm for 520 mm).
- **Placement: tail on the part, head in free space along the pull.** The tail is within 5 mm of the part that moves in 78 of 104 measurable cases (median 0.8 mm); the head is 42-59 mm (median per guide) outside the part. Exceptions are deliberate "parked beside the model" arrows (LSM Step 23 [050], floating above the model in top view) and arrows drawn alongside a long part (LSM Step 16 [034], beside the button and its leads).
- What the arrow is linked to differs by guide and does not affect the picture: PMG deconstruction links the tail to the moving part and leaves the head free (31 of 31); LAC and LSM deconstruction mostly link both ends to a static neighbour.
- **Timing.** Shown on the paused Step N frame and gone on the next frame, before the part moves. For two-stage removals in PMG deconstruction the arrow for the second stage is shown on the auto Transition (9 frames), so it is on screen for only about 0.8 s.
- In the take-apart guides the arrow stands alone on 51 of 70 arrow frames; it is combined with an eye icon on 17 and with an inset close-up of the catch on 9 (7 have both). In construction guides: alone on 15 of 27 arrow frames, with an eye icon on 7, with an inset on 5. Never with a text label.

### 9.3 Construction versus deconstruction

| | 3 full builds | 3 deconstruction guides |
|---|---|---|
| lead lines shown | 149 | 3 |
| arrows shown | 12 | 77 |
| Step N frames with lines | 62 of 146 | 3 of 94 |
| Step N frames with an arrow | 11 of 146 | 60 of 94 |
| dominant arrow direction | down / toward the base (6 of 12 -Y) | up / away from the base (39 of 77 +Y) |
| part pose on the annotated frame | part hovering, lines bridge the gap | part still seated, arrow shows the way out |

## 10. Rules precise enough to generate lead lines and arrows

For each step, given the moving unit M, its hover pose, its seated pose, any intermediate waypoints, and the mating feature pairs (male feature point on one part, female feature point on the other) that engage during this stage:

1. **Emit lines only if** M is rigid (or a wired panel/PCB sub-assembly being seated on tabs/notches) and at least one mating pair engages in this stage. Emit nothing for wires, cable plugs that are not animated, ribbon/lead preparation, pick-up steps, drop-in modules and batch repeats.
2. **Choose pairs:**
   - axial fit (shaft, round or rectangular body, plug, stem): 1 line on the axis;
   - single tab: 1; two leads: 2;
   - pin header: the extreme pins only: both end pins of a single row, the 4 corner pins of a two-row board (2 diagonal corners is an accepted lighter variant);
   - rectangular body on a plate: its 4 corners;
   - plywood: every tab/slot pair that engages in this stage if there are 4 or fewer; otherwise 4, two on each of two neighbouring panels, the pairs furthest apart;
   - several identical parts in the step: apply the rule per part, total at most 4.
   Never 3, never more than 4.
3. **End points.** `A` = centre of the tip face of the male feature in the pose it has on the hover frame. `B` = a point of the female feature on the path of `A`: for a through-slot, the slot centre on the exit face of the plate (one material thickness, 3 mm, past the mouth); for a blind hole (breadboard, socket strip), a point on the hole axis between the seated tip position and 5 mm beyond it (the guides use about 7 mm below the surface); never beyond the far side of the receiving part. If the male feature keeps travelling far beyond the receiving feature (posts through a plate), stop at the receiving feature. Because `A` and `B` lie on one mating axis, the segment is parallel to the travel; verify angle <= 2 deg and length within 15 % of the stage travel, otherwise the pair is wrong.
4. **Multi-leg stage:** polyline `A`, waypoint(s) of `A`, `B`. **Rotation stage:** straight segment from tab tip to slot at the start of the stage. **Next stage:** new lines, old ones off.
5. **Attach** each end to its part (part id + local point) so the line follows the part; show it on the hover frame only; hide it (fade) as the motion starts.
6. **Draw** as a 3D segment: `#ff0000`, solid, constant 5 px screen width (about 0.2 % of viewport width), no arrowhead, depth-tested against the model.
7. **Arrow instead of lines** when the step removes, peels, spreads or carries something: one straight flat red arrow per moving unit (two only for two parts or an opposed pair), tail on the part (or just beside it), pointing along the first main motion, length about the travel clamped to roughly 30-100 mm, proportions 5 : 20 : 17 with a body about 4 mm thick in model space, visible on the paused frame only. Never on the same frame as lead lines; never for a single wire being connected.

## 11. Numeric defaults

| default | value | basis |
|---|---|---|
| lead_line_colour | #ff0000 | 363 of 363 shown lines; all 958 line objects defined in the 20 projects |
| lead_line_style | solid straight segment, no arrowhead or end marker | 327 stored solid; 36 stored dashed but drawn solid in saved renders; 353 of 363 are two-point segments |
| lead_line_width | 5 px, constant on screen (not world units); about 0.2 % of viewport width | scale 5 and world_units false on 363 of 363; measured 2-3 px saturated core (4-5 px with anti-aliasing) on 144 full-resolution renders at 2559 and 3840 px width |
| lead_line_depth_test | on (occluded by parts) | renders LAC [055], LSM [057], LAC [004] |
| lead_line_frames_visible | 1 (the Step N frame, or the auto Transition that starts a second stage) | 359 of 363 showings live exactly one viewer frame; 0 are switched on by a Step Nc |
| lead_lines_per_frame | 1, 2 or 4; maximum 4 | 153 of 155 frames ({1: 37, 2: 75, 4: 41}); 6 on 2 frames (re-cuts of one LSM step) |
| lines_axial_part | 1 on the axis | 24 of 24 frames (9 of 9 in the full builds) |
| lines_two_lead_component | 2, one per lead | 13 of 13 frames |
| lines_pin_header_board | 4 corner pins (two-row board) or 2 (diagonal corners, or both end pins of a single row); never one per pin | 9 frames: {4: 5, 2: 4}; anchors span 80 % of the board diagonal on all Nano steps |
| lines_flat_body_on_plate | 4, at the corners | 5 of 5 frames (breadboard onto base) |
| lines_plywood_panel | one per tab/slot pair engaged in the stage, up to 4; if more engage, 2 on each of two neighbouring panels | 86 frames: {1: 12, 2: 45, 4: 27, 6: 2}; LAC F5 4 of 6, F6 4 of 8 |
| line_parallel_to_travel_tolerance | 2 deg target, 5 deg limit | 350 two-point lines with travel: median 0.4 deg; <= 1 deg 77 %, <= 2 deg 86 %, <= 5 deg 97 %, max 10.7 deg |
| line_length_over_travel | 1.00 (accept 0.85-1.15) | 360 lines: median 1.00, quartiles 0.94-1.09; 63 % within 10 %, 78 % within 15 % |
| line_stop_short_at_through_slot | travel minus about 3.4 mm (line ends in the 3 mm panel while the tab goes on through) | 84 showings with T - L between 2.4 and 5.5 mm; PMG single-tab steps 3.0-3.5 mm |
| line_end_depth_in_blind_hole | about 7 mm below the surface (1.4-5 mm beyond the seated tip) | LAC 7.0 mm on all 4 breadboard steps; LSM Part 1 6.7-7.0 mm; LSM Full Build 7.4 mm; PMG sockets 1.9-4.9 mm; one step ends at the surface |
| line_residual_if_left_on_when_seated | 3.5 mm median | 320 tweened lines; <= 5 mm on 214 |
| plywood_thickness | 3 mm | panel solid bounding boxes (LAC F3 3.0 mm, LSM D2 3.13 mm) |
| travel_components_into_breadboard | 33 mm median (29-40) | 26 lines / 13 frames |
| travel_pin_header_boards | 35 mm median (30-44) | 28 lines / 9 frames |
| travel_breadboard_onto_base | 47 mm median (39-49) | 20 lines / 5 frames |
| travel_axial_parts | 61 mm median (23-103) | 24 lines / 24 frames |
| travel_plywood_parts | 64 mm median (7-139) | 222 lines / 86 frames |
| travel_wired_module_onto_brackets | 11 mm median (8-23) | 20 lines / 10 frames, offset between pose copies |
| travel_wired_panel_subassembly | 57 mm median (50-77) | 23 lines / 8 frames, offset between pose copies |
| polyline_for_two_leg_path | vertices at the tip's waypoints (3 points) | 4 distinct lines in 2 distinct steps (LSM Step 29, LAC Step 45), 10 showings |
| arrow_colour_and_type | #ff0000, opacity 1, straight, flat unlit | 106 of 106 shown; all 176 arrow objects defined are straight |
| arrow_proportions_body:head_width:head_length | 5 : 20 : 17 | 74 of 106 showings; 5 : 20 : 15 on 14 (LSM); 18 one-off variants |
| arrow_world_size_mm | body 4.3, head width 16.7, head length 14.4 (medians) | params x per-arrow scale x mm per unit; body 10th-90th percentile 2.6-7.8 mm |
| arrow_length | 51 mm median (32-102 10th-90th percentile) | 106 showings; min 15.8, max 116.1 |
| arrow_length_over_travel | 0.96 median (quartiles 0.76-1.31) | 79 arrows aligned with a following motion |
| arrow_direction_vs_motion | within 12 deg (median about 2 deg) | 79 of 87 arrows that are followed by a motion |
| arrows_per_frame | 1; 2 only for two parts or an opposed pair | 88 frames with one, 9 with two, none with more |
| arrow_tail_to_part_distance | 0.8 mm median (on the part) | within 5 mm of the moving part on 78 of 104 measurable arrows; head 42-59 mm clear of it |
| arrow_frames_visible | 1 (paused frame before the motion) | 106 of 106 |

## 12. Anomalies (not conventions)

- **Dashed flag:** 36 line showings are stored `dashed` but render solid (section 7).
- **Mis-anchored lines hidden by geometry:** LSM D5 step (Full Build Step 26 [057], Part 3 Step 5 [010], Part 3+4 Step 6 [012]): two lines are anchored at the far end of wall D3 and are 133-134 mm long for a 42 mm travel; only the 40 mm in the gap is visible because the rest runs inside the wall. Part 3 and Part 3+4 store 38-39 mm points for the same lines, disagreeing with their own anchors.
- **LSM D6 step** (Full Build Step 31 [069], Part 4 Step 5 [010], Part 3+4 Step 11 [024]): for two of the four lines the anchors and the stored points disagree: the anchors put the lower end 57-62 mm below the rear wall's top edge and 13-18 mm off the wall solid (121-126 mm long), the stored points end at the wall top (62-68 mm). The saved render [069] shows them ending at the wall top; anything lower would be hidden by the LED matrix, so the data cannot settle which is drawn. One end references an object id that is not in the CAD tree. Part 4's copy has a third line anchored to the base plate (102.8 mm).
- **LSM Part 3+4 Step 12 [026]:** the two lines for identical posts are 54 and 99 mm (44 mm in Part 4 and the Full Build).
- **LSM Part 1+2 Step 20 [041]:** stray 8.8 mm line switched on together with an arrow.
- **PMG Step 51c / Part 3 Step 26c:** two lines still flagged visible on a "c" frame.
- **LAC Step 23 arrow [049]** (and Part 2 Step 9): stored points say up, anchors say down; the anchors match the nut's motion and the neighbouring arrows.
- **LAC potentiometer line [055]** (and Part 2 [025]): stored points lie 560-590 mm from the anchors (same length, wrong place); the render follows the anchors.
- **LAC Step 45 [098]:** one of the two polylines has 5 points with three near-coincident at its start.
- **Arrow styling drift:** 18 of 106 arrow showings depart from 5 : 20 : 17 / 5 : 20 : 15; world thickness ranges from 1.3 mm (LSM deconstruction Step 23) to 11.8 mm (PMG deconstruction Step 9).
- **PMG deconstruction Step 1 [001]:** two overlapping arrows (15.8 and 29.0 mm) for one part.
- **LAC deconstruction [120]:** an arrow sits on a frame named "Step 45c" (a mis-named Step 45).
- **PMG deconstruction Steps 2, 3:** no arrow on the paused frame, only on the auto Transition.
- **Free or unresolved ends:** 28 line ends reference ids that are not in the CAD tree or have no link (LAC and LSM Full Build breadboard-hole ends; LSM Part 3+4 Steps 7 and 12).
- **Identical parts, different lines:** LSM posts hover 77-83 mm with lines of 36.6-43.8 mm; LAC F5's four lines are 50.7, 52.5, 55.2, 55.9 mm for one 56.0 mm travel.

## 13. Per-step tables

### 13.1 Lead lines, 3 full builds (65 frames, 149 lines)

T = relative travel of the anchors to the next frame; L = line length end to end (link-derived).

| guide | step | lines | moving part → receiving part | joint class | travel T (mm) | line length L (mm) | L / T | T − L (mm) | angle to travel (°) | notes |
|---|---|---|---|---|---|---|---|---|---|---|
| LAC full build | [004] Step 2 | 4 | breadboard → F3 | breadboard onto base plate | 46.9 | 47.9 | 1.02 | -1.0 | 0.0–1.2 |  |
| LAC full build | [006] Step 3 | 2 | Nano → breadboard hole (anchor id not in CAD tree) | pin-header board into holes/sockets | 39.8 | 41.2 | 1.04 | -1.4 | 0.0 |  |
| LAC full build | [010] Step 5 | 2 | resistor → breadboard hole (anchor id not in CAD tree) | 2-lead component into breadboard | 37.1 | 40.1–40.4 | 1.08 | -3.3–-3.0 | 0.2 |  |
| LAC full build | [012] Step 6 | 2 | resistor → breadboard hole (anchor id not in CAD tree) | 2-lead component into breadboard | 40.0 | 43.2 | 1.08 | -3.1 | 0.0–0.2 |  |
| LAC full build | [015] Step 7 | 2 | RTC module → breadboard hole (anchor id not in CAD tree) | pin-header board into holes/sockets | 33.6 | 37.2 | 1.11 | -3.6 | 0.0–0.5 |  |
| LAC full build | [032] Step 15 | 1 | rocker switch → F4 | axial part (shaft/body/plug/stem) | 81.2 | 69.5 | 0.86 | 11.7 | 0.0 |  |
| LAC full build | [055] Step 25 | 1 | potentiometer → F1 | axial part (shaft/body/plug/stem) | 79.1 | 91.8 | 1.16 | -12.7 | 0.0 | stored points disagree with anchors (stored 91.8 mm) |
| LAC full build | [057] Step 26 | 1 | washer → potentiometer | axial part (shaft/body/plug/stem) | 61.3 | 75.4 | 1.23 | -14.1 | 0.0 |  |
| LAC full build | [059] Step 27 | 1 | nut → potentiometer | axial part (shaft/body/plug/stem) | 55.9 | 66.7 | 1.19 | -10.8 | 0.0 |  |
| LAC full build | [061] Step 28 | 1 | knob → potentiometer | axial part (shaft/body/plug/stem) | 60.5 | 76.5 | 1.26 | -16.0 | 0.0 |  |
| LAC full build | [090] Step 41 | 2 | F7 → F3 | plywood tab/slot panel or post | 80.3 | 75.4–76.9 | 0.94–0.96 | 3.4–4.9 | 0.0 |  |
| LAC full build | [098] Step 45 | 2 | F9 → F3 | plywood tab/slot panel or post | 103.9 | 108.5–111.9 | 1.04–1.08 | -8.0–-4.5 | - | polyline (3/5 points), path length 135.3–138.1 mm; T shown is first leg, total 107.0–110.9 mm; part also rotates |
| LAC full build | [102] Step 46 | 1 | F9 → F3 | plywood tab/slot panel or post | 10.7 | 7.3 | 0.68 | 3.4 | 2.2 | part also rotates |
| LAC full build | [109] Step 49 | 4 | F9 + F7 → F4 | wired panel sub-assembly (pose swap) | 49.8 | 46.4–49.5 | 0.93–0.99 | 0.3–3.4 | 0.0 | wired sub-assembly cross-faded, nothing tweens; T = offset between hover copy and next copy |
| LAC full build | [111] Step 50 | 2 | F8 → F4 + F3 | plywood tab/slot panel or post | 94.2 | 94.2 | 1.00 | -0.0 | 0.0 |  |
| LAC full build | [115] Step 52 | 2 | F9 → LCD | wired module onto brackets (pose swap) | 22.8 | 24.8–25.1 | 1.09 | -2.2–-2.0 | 4.3–5.6 | wired sub-assembly cross-faded, nothing tweens; T = offset between hover copy and next copy |
| LAC full build | [121] Step 54 | 4 | F4 + F3 → F1 | wired panel sub-assembly (pose swap) | 76.7 | 73.3 | 0.96 | 3.4 | 0.8 | wired sub-assembly cross-faded, nothing tweens; T = offset between hover copy and next copy |
| LAC full build | [123] Step 55 | 4 | F5 → F1 + F3 | plywood tab/slot panel or post | 56.0 | 50.7–55.9 | 0.90–1.00 | 0.2–5.4 | 0.0 |  |
| LAC full build | [125] Step 56 | 2 | F2 → F5 | plywood tab/slot panel or post | 78.1 | 75.6 | 0.97 | 2.3 | 0.3–0.6 | part also rotates |
| LAC full build | [128] Step 57 | 4 | F6 → F1 + F2 | plywood tab/slot panel or post | 67.5 | 63.4–64.1 | 0.94 | 3.4–4.0 | 0.0 |  |
| LSM full build | [004] Step 2 | 4 | breadboard → D1 base | breadboard onto base plate | 49.2 | 50.2 | 1.02 | -1.0 | 0.0–1.1 |  |
| LSM full build | [006] Step 3 | 4 | Nano → breadboard hole (anchor id not in CAD tree) | pin-header board into holes/sockets | 44.1 | 49.0 | 1.11 | -5.0 | 0.0–0.4 |  |
| LSM full build | [010] Step 5 | 2 | resistor 1 → breadboard | 2-lead component into breadboard | 32.5 | 29.9 | 0.92 | 2.6 | 0.0 |  |
| LSM full build | [013] Step 6 | 2 | capacitor → breadboard hole (anchor id not in CAD tree) | 2-lead component into breadboard | 29.1 | 28.2 | 0.97 | 0.8 | 1.7–2.3 |  |
| LSM full build | [017] Step 8 | 2 | resistor 2 → breadboard hole (anchor id not in CAD tree) | 2-lead component into breadboard | 30.3 | 34.8 | 1.15 | -4.4 | 0.0 |  |
| LSM full build | [037] Step 17 | 1 | push button → D2 | axial part (shaft/body/plug/stem) | 102.5 | 106.1 | 1.03 | -3.6 | 0.0 |  |
| LSM full build | [039] Step 18 | 1 | hex nut → push button | axial part (shaft/body/plug/stem) | 83.1 | 92.4 | 1.11 | -9.3 | 0.0 | part also rotates |
| LSM full build | [048] Step 22 | 4 | D4 → D2 + D1 base | plywood tab/slot panel or post | 69.4 | 64.6–68.8 | 0.93–0.99 | 0.6–4.8 | 0.3 |  |
| LSM full build | [053] Step 24 | 2 | D3 → D4 | plywood tab/slot panel or post | 45.8 | 41.6–41.9 | 0.91 | 3.9–4.2 | 2.2–3.3 |  |
| LSM full build | [055] Step 25 | 2 | D3 → D1 base | plywood tab/slot panel or post | 15.6–18.3 | 12.7–15.8 | 0.81–0.86 | 2.5–2.9 | 3.4–6.0 | part also rotates |
| LSM full build | [057] Step 26 | 4 | D5 → D3 + D2 | plywood tab/slot panel or post | 42.0 | 39.2–133.8 | 0.93–3.18 | -91.7–2.8 | 0.2–1.8 |  |
| LSM full build | [060] Step 27 | 4 | D9 → D3 + D2 | plywood tab/slot panel or post | 64.6 | 64.6 | 1.00 | -0.0 | 0.0 |  |
| LSM full build | [064] Step 29 | 2 | D10 → LED matrix | plywood tab/slot panel or post | 21.8 | 44.0 | 2.02 | -22.2 | - | polyline (3/3 points), path length 60.0 mm; T shown is first leg, total 43.7 mm |
| LSM full build | [067] Step 30 | 2 | D10 → D4 + D5 | wired panel sub-assembly (pose swap) | 57.1 | 56.1–57.2 | 0.98–1.00 | -0.1–1.0 | 0.9 | wired sub-assembly cross-faded, nothing tweens; T = offset between hover copy and next copy |
| LSM full build | [069] Step 31 | 4 | D6 → D2 + D4 + (one anchor id not in CAD tree) | plywood tab/slot panel or post | 64.3 | 59.9–126.2 | 0.93–1.96 | -61.9–4.3 | 0.1–0.7 | stored points disagree with anchors (stored 62.3–67.8 mm) |
| LSM full build | [071] Step 32 | 2 | D11 → D6 | plywood tab/slot panel or post | 81.7 | 43.4–43.8 | 0.53 | 37.9–38.2 | 0.3–1.2 |  |
| LSM full build | [073] Step 33 | 2 | D11 → D6 | plywood tab/slot panel or post | 77.4–83.1 | 36.6–42.8 | 0.47–0.52 | 40.3–40.9 | 0.1 |  |
| LSM full build | [075] Step 34 | 4 | D11 → D1 base | plywood tab/slot panel or post | 7.0 | 15.6–17.5 | 2.23–2.51 | -10.5–-8.6 | 0.6 |  |
| LSM full build | [078] Step 35 | 4 | D7 → D11 | plywood tab/slot panel or post | 67.8 | 48.9–50.0 | 0.72–0.74 | 17.8–18.9 | 0.2–1.4 | 4 stored as dashed |
| LSM full build | [080] Step 36 | 4 | D8 → D11 | plywood tab/slot panel or post | 54.1 | 57.8–60.9 | 1.07–1.13 | -6.8–-3.7 | 0.4–2.1 | 4 stored as dashed |
| LSM full build | [083] Step 37 | 1 | stem → LED matrix | axial part (shaft/body/plug/stem) | 43.5 | 43.8 | 1.01 | -0.3 | 2.6 |  |
| PMG full build | [002] Step 1 | 4 | Nano → Nano I/O shield | pin-header board into holes/sockets | 29.8 | 25.7–28.7 | 0.86–0.96 | 1.1–4.1 | 0.0 |  |
| PMG full build | [057] Step 25 | 1 | USB plug → Nano | axial part (shaft/body/plug/stem) | 22.9 | 28.5 | 1.24 | -5.6 | 0.0 |  |
| PMG full build | [059] Step 26 | 1 | H2 → H1 | plywood tab/slot panel or post | 40.0 | 36.6 | 0.92 | 3.4 | 0.0 |  |
| PMG full build | [061] Step 27 | 1 | H3 → H1 | plywood tab/slot panel or post | 43.2 | 39.8 | 0.92 | 3.4 | 0.0 |  |
| PMG full build | [063] Step 28 | 4 | H4 → H2 + H3 | plywood tab/slot panel or post | 65.0 | 61.5 | 0.95 | 3.4 | 0.0 |  |
| PMG full build | [065] Step 29 | 2 | H5 → H2 | plywood tab/slot panel or post | 117.2 | 117.9 | 1.01 | -0.8 | 0.6 |  |
| PMG full build | [067] Step 30 | 2 | H5 → H3 | plywood tab/slot panel or post | 56.9 | 56.8 | 1.00 | 0.1 | 1.6 | part also rotates |
| PMG full build | [069] Step 31 | 2 | H6 → H5 | plywood tab/slot panel or post | 122.3 | 122.5 | 1.00 | -0.2 | 0.7 |  |
| PMG full build | [071] Step 32 | 2 | H6 → H5 | plywood tab/slot panel or post | 43.8 | 43.9 | 1.00 | -0.2 | 1.6–2.0 | part also rotates |
| PMG full build | [077] Step 35 | 2 | H7 → H6 | plywood tab/slot panel or post | 139.4 | 139.0–139.2 | 1.00 | 0.2–0.3 | 0.7 |  |
| PMG full build | [079] Step 36 | 2 | H7 → H6 | plywood tab/slot panel or post | 28.4 | 28.5 | 1.00 | -0.2 | 0.9 | part also rotates |
| PMG full build | [081] Step 37 | 2 | H8 → H5 | plywood tab/slot panel or post | 94.5 | 94.6 | 1.00 | -0.1 | 0.0 |  |
| PMG full build | [083] Step 38 | 1 | H9 key → H4 | plywood tab/slot panel or post | 107.7 | 104.2 | 0.97 | 3.5 | 0.0 |  |
| PMG full build | [087] Step 40 | 2 | H10 → H4 | plywood tab/slot panel or post | 126.0 | 116.2 | 0.92 | 9.8 | 1.0 |  |
| PMG full build | [089] Step 41 | 2 | H10 → H3 + H2 | plywood tab/slot panel or post | 8.7 | 8.7 | 1.00 | -0.1 | 5.1–6.1 | part also rotates |
| PMG full build | [091] Step 42 | 1 | H11 → H10 | plywood tab/slot panel or post | 53.1 | 50.1 | 0.94 | 3.0 | 0.0 |  |
| PMG full build | [094] Step 43 | 1 | H12 → H10 | plywood tab/slot panel or post | 44.5 | 41.0 | 0.92 | 3.4 | 0.0 |  |
| PMG full build | [097] Step 44 | 4 | H13 → H12 + H11 + H4 | plywood tab/slot panel or post | 80.1 | 68.2–82.1 | 0.85–1.03 | -2.1–11.9 | 0.3–2.5 |  |
| PMG full build | [105] Step 48 | 2 | 4-digit display → H11 + H12 | wired module onto brackets (pose swap) | 11.1 | 11.9–12.2 | 1.07–1.09 | -1.1–-0.8 | 2.2–3.2 | wired sub-assembly cross-faded, nothing tweens; T = offset between hover copy and next copy |
| PMG full build | [106] Transition | 2 | 4-digit display → H12 + H11 | wired module onto brackets (pose swap) | 8.0 | 9.3–9.6 | 1.17–1.20 | -1.6–-1.3 | 2.4–4.1 | wired sub-assembly cross-faded, nothing tweens; T = offset between hover copy and next copy; shown on auto transition |
| PMG full build | [110] Step 50 | 2 | H12 + H11 → dot matrix | wired module onto brackets (pose swap) | 20.4 | 20.4–21.2 | 1.00–1.04 | -0.8–-0.0 | 2.9–3.1 | wired sub-assembly cross-faded, nothing tweens; T = offset between hover copy and next copy |
| PMG full build | [111] Transition | 2 | H12 + H11 → dot matrix | wired module onto brackets (pose swap) | 10.8–11.1 | 10.8 | 0.97–1.00 | -0.0–0.3 | 8.9–10.7 | wired sub-assembly cross-faded, nothing tweens; T = offset between hover copy and next copy; shown on auto transition |
| PMG full build | [113] Step 51 | 2 | H14 → dot matrix | plywood tab/slot panel or post | 57.8 | 58.2–58.7 | 1.01 | -0.9–-0.5 | 0.7–1.3 | part also rotates |
| PMG full build | [114] Transition | 2 | H14 → H12 + H11 | plywood tab/slot panel or post | 8.8 | 8.1–8.6 | 0.92–0.97 | 0.3–0.7 | 1.6–2.6 | part also rotates; shown on auto transition |

### 13.2 Lead lines, the other 13 guides that show any (parts repeat the full builds; LSM Parts 1, 2, 1+2 are an older authoring)

| guide | step | lines | moving part → receiving part | joint class | travel T (mm) | line length L (mm) | L / T | T − L (mm) | angle to travel (°) | notes |
|---|---|---|---|---|---|---|---|---|---|---|
| LAC deconstruction | [043] Step 16 | 1 | washer → potentiometer | axial part (shaft/body/plug/stem) | 53.6 | 60.7 | 1.13 | -7.1 | 0.1 |  |
| LAC deconstruction | [045] Step 17 | 1 | nut → washer | axial part (shaft/body/plug/stem) | 37.8 | 39.2 | 1.04 | -1.4 | 0.6 |  |
| LAC deconstruction | [047] Step 18 | 1 | knob → washer | axial part (shaft/body/plug/stem) | 42.6 | 48.9 | 1.15 | -6.3 | 0.0 |  |
| LSM part 1 | [003] Step 2 | 4 | breadboard → D1 base | breadboard onto base plate | 39.3 | 39.3 | 1.00 | -0.0 | 0.6–1.0 |  |
| LSM part 1 | [005] Step 3 | 4 | Nano → breadboard | pin-header board into holes/sockets | 35.3 | 38.8–39.2 | 1.10 | -3.8–-3.5 | 0.5–0.7 | 1 stored as dashed |
| LSM part 1 | [009] Step 5 | 2 | resistor 1 → breadboard | 2-lead component into breadboard | 36.8 | 41.4 | 1.12 | -4.6 | 0.1 | 2 stored as dashed |
| LSM part 1 | [012] Step 6 | 2 | capacitor → breadboard | 2-lead component into breadboard | 32.9 | 27.2 | 0.83 | 5.7 | 0.1–0.4 |  |
| LSM part 1 | [016] Step 8 | 2 | resistor 2 → breadboard | 2-lead component into breadboard | 31.4 | 35.8 | 1.14 | -4.4 | 0.1 | 2 stored as dashed |
| LSM part 2 | [019] Step 9 | 1 | push button → D2 | axial part (shaft/body/plug/stem) | 103.2 | 106.7 | 1.03 | -3.5 | 0.2 |  |
| LSM part 2 | [021] Step 10 | 1 | hex nut → push button | axial part (shaft/body/plug/stem) | 80.4 | 90.0 | 1.12 | -9.5 | 0.0 | part also rotates; 1 stored as dashed |
| LSM part 3 | [001] Step 1 | 4 | D4 → D2 + D1 base | plywood tab/slot panel or post | 69.4 | 64.3–67.6 | 0.93–0.97 | 1.8–5.1 | 0.6 |  |
| LSM part 3 | [006] Step 3 | 2 | D3 → D4 | plywood tab/slot panel or post | 45.8 | 42.1–42.3 | 0.92 | 3.5–3.7 | 3.9–5.0 |  |
| LSM part 3 | [008] Step 4 | 2 | D3 → D1 base | plywood tab/slot panel or post | 15.7–18.6 | 12.7–16.1 | 0.81–0.87 | 2.5–3.0 | 2.2–4.3 | part also rotates |
| LSM part 3 | [010] Step 5 | 6 | D5 → D3 + D2 + D1 base | plywood tab/slot panel or post | 42.0 | 39.2–133.8 | 0.93–3.18 | -91.7–2.8 | 0.2–1.8 | stored points disagree with anchors (stored 38.3–39.4 mm) |
| LSM part 3 4 | [003] Step 2 | 4 | D4 → D1 base + D2 | plywood tab/slot panel or post | 69.4 | 64.4–67.9 | 0.93–0.98 | 1.5–5.0 | 0.0 |  |
| LSM part 3 4 | [008] Step 4 | 2 | D3 → D4 | plywood tab/slot panel or post | 45.8 | 40.5 | 0.89 | 5.2 | 3.9 |  |
| LSM part 3 4 | [010] Step 5 | 2 | D3 → D1 base | plywood tab/slot panel or post | 15.6–18.3 | 12.7–15.8 | 0.81–0.86 | 2.5–2.9 | 3.4–6.0 | part also rotates |
| LSM part 3 4 | [012] Step 6 | 6 | D5 → D3 + D2 + D1 base | plywood tab/slot panel or post | 42.0 | 39.2–133.8 | 0.93–3.18 | -91.7–2.8 | 0.2–1.8 | stored points disagree with anchors (stored 38.3–39.4 mm) |
| LSM part 3 4 | [015] Step 7 | 4 | D9 → D3 + ? | plywood tab/slot panel or post | 65.3 | 63.6–65.7 | 0.97–1.01 | -0.4–1.6 | 0.0 |  |
| LSM part 3 4 | [019] Step 9 | 2 | D10 → LED matrix | plywood tab/slot panel or post | 18.9 | 48.0–48.3 | 2.54 | -29.4–-29.1 | - | polyline (3/3 points), path length 63.5 mm; T shown is first leg, total 46.9 mm |
| LSM part 3 4 | [022] Step 10 | 2 | D4 + D5 → D10 | wired panel sub-assembly (pose swap) | - | 57.1 | - | - | - | wired sub-assembly cross-faded, nothing tweens; T = offset between hover copy and next copy |
| LSM part 3 4 | [024] Step 11 | 4 | D6 → D2 + D4 + D5 | plywood tab/slot panel or post | 64.3 | 58.6–126.2 | 0.91–1.96 | -61.9–5.7 | 0.0–0.4 | stored points disagree with anchors (stored 62.3–67.8 mm) |
| LSM part 3 4 | [026] Step 12 | 2 | D11 → D6 + ? | plywood tab/slot panel or post | 81.7 | 53.7–98.6 | 0.66–1.21 | -16.9–27.9 | 0.0 |  |
| LSM part 3 4 | [028] Step 13 | 2 | D11 → D6 | plywood tab/slot panel or post | 77.4–83.1 | 36.6–42.8 | 0.47–0.52 | 40.3–40.9 | 0.1 |  |
| LSM part 3 4 | [030] Step 14 | 4 | D11 → D1 base | plywood tab/slot panel or post | 7.0 | 15.6–17.5 | 2.23–2.51 | -10.5–-8.6 | 0.6 |  |
| LSM part 3 4 | [033] Step 15 | 4 | D7 → D11 | plywood tab/slot panel or post | 67.8 | 48.9–50.0 | 0.72–0.74 | 17.8–18.9 | 0.2–1.4 | 4 stored as dashed |
| LSM part 3 4 | [035] Step 16 | 4 | D8 → D11 | plywood tab/slot panel or post | 54.1 | 57.8–60.9 | 1.07–1.13 | -6.8–-3.7 | 0.4–2.1 | 4 stored as dashed |
| LSM part 3 4 | [038] Step 17 | 1 | stem → LED matrix | axial part (shaft/body/plug/stem) | 55.1 | 48.8 | 0.88 | 6.4 | 2.0 |  |
| LSM part 4 | [001] Step 1 | 4 | D9 → D3 + D2 | plywood tab/slot panel or post | 68.0 | 68.0 | 1.00 | -0.0 | 0.0 |  |
| LSM part 4 | [005] Step 3 | 2 | D10 → LED matrix | plywood tab/slot panel or post | 19.3 | 46.2 | 2.40 | -27.1 | - | polyline (3/3 points), path length 61.6–62.0 mm; T shown is first leg, total 45.4 mm |
| LSM part 4 | [008] Step 4 | 2 | D4 + D5 → D10 | wired panel sub-assembly (pose swap) | 57.2 | 56.9 | 0.99 | 0.2 | 0.9 | wired sub-assembly cross-faded, nothing tweens; T = offset between hover copy and next copy |
| LSM part 4 | [010] Step 5 | 4 | D6 → D2 + D4 + D1 base | plywood tab/slot panel or post | 64.3 | 59.9–126.2 | 0.93–1.96 | -61.9–4.3 | 0.0–0.4 | stored points disagree with anchors (stored 62.3–67.8 mm) |
| LSM part 4 | [012] Step 6 | 2 | D11 → D6 | plywood tab/slot panel or post | 81.7 | 43.4–43.8 | 0.53 | 37.9–38.2 | 0.3–1.2 |  |
| LSM part 4 | [014] Step 7 | 2 | D11 → D6 | plywood tab/slot panel or post | 77.4–83.1 | 36.6–42.8 | 0.47–0.52 | 40.3–40.9 | 0.1 |  |
| LSM part 4 | [016] Step 8 | 4 | D11 → D1 base | plywood tab/slot panel or post | 7.0 | 15.5–17.4 | 2.22–2.50 | -10.5–-8.5 | 0.6 |  |
| LSM part 4 | [019] Step 10 | 4 | D7 → D11 | plywood tab/slot panel or post | 67.8 | 48.9–50.0 | 0.72–0.74 | 17.8–18.9 | 0.2–1.4 | 4 stored as dashed |
| LSM part 4 | [021] Step 11 | 4 | D8 → D11 | plywood tab/slot panel or post | 54.1 | 57.8–60.9 | 1.07–1.13 | -6.8–-3.7 | 0.4–2.1 | 4 stored as dashed |
| LSM part 4 | [024] Step 12 | 1 | stem → LED matrix | axial part (shaft/body/plug/stem) | 50.2 | 48.2 | 0.96 | 2.0 | 2.5 |  |
| LSM part 1 2 | [003] Step 2 | 4 | breadboard → D1 base | breadboard onto base plate | 39.3 | 39.3 | 1.00 | -0.1 | 0.6–1.0 |  |
| LSM part 1 2 | [005] Step 3 | 4 | Nano → breadboard | pin-header board into holes/sockets | 35.3 | 38.8–39.2 | 1.10 | -3.8–-3.5 | 0.5–0.7 | 1 stored as dashed |
| LSM part 1 2 | [009] Step 5 | 2 | resistor 1 → breadboard | 2-lead component into breadboard | 36.8 | 41.4 | 1.12 | -4.6 | 0.1 | 2 stored as dashed |
| LSM part 1 2 | [011] Step 6 | 2 | capacitor → breadboard | 2-lead component into breadboard | 32.9 | 27.2 | 0.83 | 5.7 | 0.1–0.4 |  |
| LSM part 1 2 | [015] Step 8 | 2 | resistor 2 → breadboard | 2-lead component into breadboard | 31.4 | 35.8 | 1.14 | -4.4 | 0.1 | 2 stored as dashed |
| LSM part 1 2 | [035] Step 17 | 1 | push button → D2 | axial part (shaft/body/plug/stem) | 103.2 | 106.7 | 1.03 | -3.5 | 0.2 |  |
| LSM part 1 2 | [037] Step 18 | 1 | hex nut → push button | axial part (shaft/body/plug/stem) | 80.4 | 90.0 | 1.12 | -9.5 | 0.0 | part also rotates; 1 stored as dashed |
| LSM part 1 2 | [041] Step 20 | 1 | push button → D2 | wired panel sub-assembly (pose swap) | - | 8.8 | - | - | - | wired sub-assembly cross-faded, nothing tweens; T = offset between hover copy and next copy |
| LAC part 2 | [002] Step 1 | 1 | rocker switch → F4 | axial part (shaft/body/plug/stem) | 81.2 | 69.5 | 0.86 | 11.7 | 0.0 |  |
| LAC part 2 | [025] Step 11 | 1 | potentiometer → F1 | axial part (shaft/body/plug/stem) | 79.1 | 91.8 | 1.16 | -12.7 | 0.0 | stored points disagree with anchors (stored 91.8 mm) |
| LAC part 2 | [027] Step 12 | 1 | washer → potentiometer | axial part (shaft/body/plug/stem) | 61.3 | 75.4 | 1.23 | -14.1 | 0.0 |  |
| LAC part 2 | [029] Step 13 | 1 | nut → potentiometer | axial part (shaft/body/plug/stem) | 55.9 | 66.7 | 1.19 | -10.8 | 0.0 |  |
| LAC part 2 | [031] Step 14 | 1 | knob → potentiometer | axial part (shaft/body/plug/stem) | 60.5 | 76.5 | 1.26 | -16.0 | 0.0 |  |
| LAC part 4 | [001] Step 1 | 2 | F7 → F3 | plywood tab/slot panel or post | 80.3 | 75.4–76.9 | 0.94–0.96 | 3.4–4.9 | 0.0 |  |
| LAC part 4 | [009] Step 5 | 2 | F9 → F3 | plywood tab/slot panel or post | 103.9 | 108.5–111.9 | 1.04–1.08 | -8.0–-4.5 | - | polyline (3/5 points), path length 135.3–138.1 mm; T shown is first leg, total 107.0–110.9 mm; part also rotates |
| LAC part 4 | [013] Step 6 | 1 | F9 → F3 | plywood tab/slot panel or post | 10.7 | 7.3 | 0.68 | 3.4 | 2.2 | part also rotates |
| LAC part 4 | [020] Step 9 | 4 | F9 + F7 → F4 | wired panel sub-assembly (pose swap) | 49.8 | 46.4–49.5 | 0.93–0.99 | 0.3–3.4 | 0.0 | wired sub-assembly cross-faded, nothing tweens; T = offset between hover copy and next copy |
| LAC part 4 | [022] Step 10 | 2 | F8 → F4 + F3 | plywood tab/slot panel or post | 94.2 | 94.2 | 1.00 | -0.0 | 0.0 |  |
| LAC part 4 | [026] Step 12 | 2 | F9 → LCD | wired module onto brackets (pose swap) | 22.8 | 24.8–25.1 | 1.09 | -2.2–-2.0 | 4.3–5.6 | wired sub-assembly cross-faded, nothing tweens; T = offset between hover copy and next copy |
| LAC part 4 | [032] Step 14 | 4 | F4 + F3 → F1 | wired panel sub-assembly (pose swap) | 76.7 | 73.3 | 0.96 | 3.4 | 0.8 | wired sub-assembly cross-faded, nothing tweens; T = offset between hover copy and next copy |
| LAC part 4 | [034] Step 15 | 4 | F5 → F1 + F3 | plywood tab/slot panel or post | 56.0 | 50.7–55.9 | 0.90–1.00 | 0.2–5.4 | 0.0 |  |
| LAC part 4 | [036] Step 16 | 2 | F2 → F5 | plywood tab/slot panel or post | 78.1 | 75.6 | 0.97 | 2.3 | 0.3–0.6 | part also rotates |
| LAC part 4 | [039] Step 17 | 4 | F6 → F1 + F2 | plywood tab/slot panel or post | 67.5 | 63.4–64.1 | 0.94 | 3.4–4.0 | 0.0 |  |
| LAC  part 1 | [004] Step 2 | 4 | breadboard → F3 | breadboard onto base plate | 46.9 | 47.9 | 1.02 | -1.0 | 0.0–1.2 |  |
| LAC  part 1 | [006] Step 3 | 2 | Nano → breadboard hole (anchor id not in CAD tree) | pin-header board into holes/sockets | 39.8 | 41.2 | 1.04 | -1.4 | 0.0 |  |
| LAC  part 1 | [010] Step 5 | 2 | resistor → breadboard hole (anchor id not in CAD tree) | 2-lead component into breadboard | 37.1 | 40.1–40.4 | 1.08 | -3.3–-3.0 | 0.2 |  |
| LAC  part 1 | [012] Step 6 | 2 | resistor → breadboard hole (anchor id not in CAD tree) | 2-lead component into breadboard | 40.0 | 43.2 | 1.08 | -3.1 | 0.0–0.2 |  |
| LAC  part 1 | [015] Step 7 | 2 | RTC module → breadboard hole (anchor id not in CAD tree) | pin-header board into holes/sockets | 33.6 | 37.2 | 1.11 | -3.6 | 0.0–0.5 |  |
| PMG part 1 | [002] Step 1 | 4 | Nano → Nano I/O shield | pin-header board into holes/sockets | 29.8 | 25.7–28.7 | 0.86–0.96 | 1.1–4.1 | 0.0 |  |
| PMG part 2 | [024] Step 11 | 1 | USB plug → Nano | axial part (shaft/body/plug/stem) | 22.9 | 28.5 | 1.24 | -5.6 | 0.0 |  |
| PMG part 3 | [001] Step 1 | 1 | H2 → H1 | plywood tab/slot panel or post | 40.0 | 36.6 | 0.92 | 3.4 | 0.0 |  |
| PMG part 3 | [003] Step 2 | 1 | H3 → H1 | plywood tab/slot panel or post | 43.2 | 39.8 | 0.92 | 3.4 | 0.0 |  |
| PMG part 3 | [005] Step 3 | 4 | H4 → H2 + H3 | plywood tab/slot panel or post | 65.0 | 61.5 | 0.95 | 3.4 | 0.0 |  |
| PMG part 3 | [007] Step 4 | 2 | H5 → H2 | plywood tab/slot panel or post | 117.2 | 117.9 | 1.01 | -0.8 | 0.6 |  |
| PMG part 3 | [009] Step 5 | 2 | H5 → H3 | plywood tab/slot panel or post | 56.9 | 56.8 | 1.00 | 0.1 | 1.6 | part also rotates |
| PMG part 3 | [011] Step 6 | 2 | H6 → H5 | plywood tab/slot panel or post | 122.3 | 122.5 | 1.00 | -0.2 | 0.7 |  |
| PMG part 3 | [013] Step 7 | 2 | H6 → H5 | plywood tab/slot panel or post | 43.8 | 43.9 | 1.00 | -0.2 | 1.6–2.0 | part also rotates |
| PMG part 3 | [019] Step 10 | 2 | H7 → H6 | plywood tab/slot panel or post | 139.4 | 139.0–139.2 | 1.00 | 0.2–0.3 | 0.7 |  |
| PMG part 3 | [021] Step 11 | 2 | H7 → H6 | plywood tab/slot panel or post | 28.4 | 28.5 | 1.00 | -0.2 | 0.9 | part also rotates |
| PMG part 3 | [023] Step 12 | 2 | H8 → H5 | plywood tab/slot panel or post | 94.5 | 94.6 | 1.00 | -0.1 | 0.0 |  |
| PMG part 3 | [025] Step 13 | 1 | H9 key → H4 | plywood tab/slot panel or post | 107.7 | 104.2 | 0.97 | 3.5 | 0.0 |  |
| PMG part 3 | [029] Step 15 | 2 | H10 → H4 | plywood tab/slot panel or post | 126.0 | 116.2 | 0.92 | 9.8 | 1.0 |  |
| PMG part 3 | [031] Step 16 | 2 | H10 → H3 + H2 | plywood tab/slot panel or post | 8.7 | 8.7 | 1.00 | -0.1 | 5.1–6.1 | part also rotates |
| PMG part 3 | [033] Step 17 | 1 | H11 → H10 | plywood tab/slot panel or post | 53.1 | 50.1 | 0.94 | 3.0 | 0.0 |  |
| PMG part 3 | [036] Step 18 | 1 | H12 → H10 | plywood tab/slot panel or post | 44.5 | 41.0 | 0.92 | 3.4 | 0.0 |  |
| PMG part 3 | [039] Step 19 | 4 | H13 → H12 + H11 + H4 | plywood tab/slot panel or post | 80.1 | 68.2–82.1 | 0.85–1.03 | -2.1–11.9 | 0.3–2.5 |  |
| PMG part 3 | [047] Step 23 | 2 | 4-digit display → H11 + H12 | wired module onto brackets (pose swap) | 11.1 | 11.9–12.2 | 1.07–1.09 | -1.1–-0.8 | 2.2–3.2 | wired sub-assembly cross-faded, nothing tweens; T = offset between hover copy and next copy |
| PMG part 3 | [048] Transition | 2 | 4-digit display → H12 + H11 | wired module onto brackets (pose swap) | 8.0 | 9.3–9.6 | 1.17–1.20 | -1.6–-1.3 | 2.4–4.1 | wired sub-assembly cross-faded, nothing tweens; T = offset between hover copy and next copy; shown on auto transition |
| PMG part 3 | [052] Step 25 | 2 | H12 + H11 → dot matrix | wired module onto brackets (pose swap) | 20.4 | 20.4–21.2 | 1.00–1.04 | -0.8–-0.0 | 2.9–3.1 | wired sub-assembly cross-faded, nothing tweens; T = offset between hover copy and next copy |
| PMG part 3 | [053] Transition | 2 | H12 + H11 → dot matrix | wired module onto brackets (pose swap) | 10.8–11.1 | 10.8 | 0.97–1.00 | -0.0–0.3 | 8.9–10.7 | wired sub-assembly cross-faded, nothing tweens; T = offset between hover copy and next copy; shown on auto transition |
| PMG part 3 | [055] Step 26 | 2 | H14 → dot matrix | plywood tab/slot panel or post | 57.8 | 58.2–58.7 | 1.01 | -0.9–-0.5 | 0.7–1.3 | part also rotates |
| PMG part 3 | [056] Transition | 2 | H14 → H12 + H11 | plywood tab/slot panel or post | 8.8 | 8.1–8.6 | 0.92–0.97 | 0.3–0.7 | 1.6–2.6 | part also rotates; shown on auto transition |

### 13.3 Arrows in construction guides (29 showings)

| guide | step | frame | length (mm) | direction | body / head width / head length (params) | scale | ≈ world size mm (body / head w / head l) | next motion of the part | arrow vs motion (°) | L / travel | other cues on frame |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LAC full build | [001] Step 1 | hover | 24.7 | -Y(down) | 5/20/17 | 0.238 | 1.97/7.86/6.68 | backing sheet tweens 53.2 mm | 0.7 | 0.46 | image×1 |
| LAC full build | [046] Step 22 | hover | 41.8 | -Y(down) | 5/20/17 | 0.519 | 4.28/17.14/14.57 | knob tweens 37.6 mm | 4.1 | 1.11 | - |
| LAC full build | [049] Step 23 | hover | 41.3 | -Y(down) | 6/24/22 | 0.300 | 2.97/11.89/10.9 | nut tweens 37.9 mm | 1.6 | 1.09 | - |
| LAC full build | [052] Step 24 | hover | 32.6 | -Y(down) | 5/15/10 | 0.290 | 2.39/7.18/4.79 | washer tweens 37.9 mm | 1.6 | 0.86 | - |
| LAC full build | [092] Step 42 | hover | 38.5 | +X | 4/15/10 | 0.580 | 3.83/14.37/9.58 | F7 tweens 14.5 mm | 9.1 | 2.65 | - |
| LAC full build | [092] Step 42 | hover | 47.9 | -X | 4/15/14 | 0.580 | 3.83/14.37/13.41 | F7 tweens 14.5 mm | 172.3 | 3.31 | - |
| LAC full build | [104] Step 47 | hover | 101.7 | -Z | 5/20/17 | 1.244 | 10.27/41.09/34.92 | pose swap knob (519.9 mm between copies) | 6.4 | 0.2 | eye×1 |
| LSM full build | [001] Step 1 | hover | 35.1 | -Y(down) | 5/20/15 | 0.328 | 3.43/13.73/10.3 | backing sheet tweens 39.3 mm | 1.5 | 0.89 | image×1 |
| LSM full build | [034] Step 16 | hover | 68.7 | -Z | 5/20/15 | 0.216 | 2.26/9.02/6.77 | push button tweens 100.6 mm | 0.5 | 0.68 | - |
| LSM full build | [046] Step 21 | hover | 45.2 | -Z | 5/20/15 head at START | 0.475 | 4.97/19.86/14.9 | pose swap D2 (57.1 mm between copies) | 0.4 | 0.79 | - |
| LSM full build | [050] Step 23 | hover | 102.9 | -X | 3/9/10 | 0.848 | 5.32/15.96/17.73 | pose swap LED matrix (184.4 mm between copies) | 9.2 | 0.56 | eye×1 |
| LSM part 1 | [001] Step 1 | hover | 39.4 | -Y(down) | 5/20/15 | 0.827 | 4.14/16.55/12.41 | backing sheet tweens 48.3 mm | 1.6 | 0.82 | image×1 |
| LSM part 2 | [016] Step 8 | hover | 63.3 | -Z | 5/20/15 | 0.516 | 2.58/10.32/7.74 | push button tweens 98.8 mm | 2.7 | 0.64 | - |
| LSM part 2 | [025] Step 12 | hover | 50.1 | -Z | 5/20/10 | 1.328 | 6.64/26.55/13.28 | D2 slides 1.3 mm while fading out | 177.3 | 38.54 | eye×1 |
| LSM part 3 | [003] Step 2 | hover | 102.9 | -X | 3/9/10 | 0.848 | 5.32/15.96/17.73 | pose swap LED matrix (184.4 mm between copies) | 9.2 | 0.56 | eye×1 |
| LSM part 3 4 | [001] Step 1 | hover | 45.2 | -Z | 5/20/15 head at START | 0.475 | 4.97/19.86/14.9 | pose swap D2 (57.1 mm between copies) | 0.4 | 0.79 | - |
| LSM part 3 4 | [005] Step 3 | hover | 102.9 | -X | 3/9/10 | 0.848 | 5.32/15.96/17.73 | pose swap LED matrix (184.4 mm between copies) | 9.2 | 0.56 | eye×1 |
| LSM part 1 2 | [001] Step 1 | hover | 39.4 | -Y(down) | 5/20/15 | 0.827 | 4.14/16.55/12.41 | backing sheet tweens 48.3 mm | 1.6 | 0.82 | image×1 |
| LSM part 1 2 | [032] Step 16 | hover | 63.3 | -Z | 5/20/15 | 0.516 | 2.58/10.32/7.74 | push button tweens 98.8 mm | 2.7 | 0.64 | - |
| LSM part 1 2 | [041] Step 20 | hover | 55.3 | -Z | 5/20/17 | 1.331 | 6.65/26.61/22.62 | D2 slides 1.2 mm while fading out | 178.2 | 46.08 | line×1, eye×1 |
| LAC part 2 | [016] Step 8 | hover | 41.8 | -Y(down) | 5/20/17 | 0.519 | 4.28/17.14/14.57 | knob tweens 37.6 mm | 4.1 | 1.11 | - |
| LAC part 2 | [019] Step 9 | hover | 41.3 | -Y(down) | 6/24/22 | 0.300 | 2.97/11.89/10.9 | nut tweens 37.9 mm | 1.6 | 1.09 | - |
| LAC part 2 | [022] Step 10 | hover | 32.6 | -Y(down) | 5/15/10 | 0.290 | 2.39/7.18/4.79 | washer tweens 37.9 mm | 1.6 | 0.86 | - |
| LAC part 4 | [003] Step 2 | hover | 38.5 | +X | 4/15/10 | 0.580 | 3.83/14.37/9.58 | F7 tweens 14.5 mm | 9.1 | 2.65 | - |
| LAC part 4 | [003] Step 2 | hover | 47.9 | -X | 4/15/14 | 0.580 | 3.83/14.37/13.41 | F7 tweens 14.5 mm | 172.3 | 3.31 | - |
| LAC part 4 | [015] Step 7 | hover | 101.7 | -Z | 5/20/17 | 1.244 | 10.27/41.09/34.92 | pose swap knob (519.9 mm between copies) | 6.4 | 0.2 | eye×1 |
| LAC  part 1 | [001] Step 1 | hover | 24.7 | -Y(down) | 5/20/17 | 0.238 | 1.97/7.86/6.68 | backing sheet tweens 53.2 mm | 0.7 | 0.46 | image×1 |
| PMG part 3 | [043] Step 21 | hover | 79.8 | -Y(down) | 5/20/17 | 0.023 | 2.76/11.03/9.38 | pose swap USB cable (114.6 mm between copies) | 23.2 | 0.7 | - |
| PMG full build | [101] Step 46 | hover | 79.8 | -Y(down) | 5/20/17 | 0.023 | 2.76/11.03/9.38 | pose swap USB cable (114.6 mm between copies) | 23.2 | 0.7 | - |

### 13.4 Arrows in deconstruction guides (77 showings)

| guide | step | frame | length (mm) | direction | body / head width / head length (params) | scale | ≈ world size mm (body / head w / head l) | next motion of the part | arrow vs motion (°) | L / travel | other cues on frame |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LAC deconstruction | [001] Step 1 | hover | 56.1 | -Z | 5/20/17 | 0.590 | 4.87/19.49/16.57 | F6 tweens 67.5 mm | 2.3 | 0.83 | - |
| LAC deconstruction | [004] Step 2 | hover | 79.8 | -X | 5/20/17 | 0.667 | 5.51/22.02/18.72 | F2 tweens 28.2 mm | 8.2 | 2.83 | eye×1 |
| LAC deconstruction | [008] Step 3 | hover | 64.6 | +Z | 5/20/17 | 0.750 | 6.19/24.77/21.06 | F5 tweens 56.0 mm | 0.3 | 1.15 | - |
| LAC deconstruction | [011] Step 4 | hover | 79.0 | +X | 5/20/17 | 0.700 | 5.78/23.12/19.65 | pose swap F1 (76.7 mm between copies) | 3.1 | 1.03 | - |
| LAC deconstruction | [019] Step 7 | hover | 83.9 | +X | 5/20/17 | 0.546 | 4.51/18.03/15.32 | F8 tweens 94.2 mm | 1.7 | 0.89 | - |
| LAC deconstruction | [022] Step 8 | hover | 73.2 | +Y(up) | 5/20/17 | 0.406 | 3.35/13.4/11.39 | pose swap F4 (49.8 mm between copies) | 0.8 | 1.47 | - |
| LAC deconstruction | [031] Step 12 | hover | 41.2 | +Y(up) | 5/20/17 | 0.355 | 2.93/11.72/9.96 | knob tweens 52.7 mm | 2.0 | 0.78 | - |
| LAC deconstruction | [035] Step 13 | hover | 56.5 | +Y(up) | 5/20/17 | 0.450 | 3.72/14.86/12.63 | nut tweens 58.7 mm | 2.5 | 0.96 | - |
| LAC deconstruction | [038] Step 14 | hover | 70.6 | +Y(up) | 5/20/17 | 0.350 | 2.89/11.56/9.83 | washer tweens 55.0 mm | 0.6 | 1.28 | - |
| LAC deconstruction | [041] Step 15 | hover | 52.7 | -Y(down) | 5/20/17 | 0.510 | 4.21/16.85/14.32 | jumper wire(s) tweens 66.7 mm | 1.5 | 0.79 | - |
| LAC deconstruction | [063] Step 24 | hover | 33.8 | +Y(up) | 5/20/17 | 0.400 | 3.3/13.21/11.23 | F9 tweens 16.8 mm | 64.9 | 2.01 | image×1 |
| LAC deconstruction | [067] Step 25 | hover | 63.5 | +Z | 5/20/17 | 0.700 | 5.78/23.12/19.65 | USB cable tweens 43.3 mm | 0.8 | 1.47 | eye×1 |
| LAC deconstruction | [070] Step 26 | hover | 36.9 | -X | 5/20/17 | 0.454 | 3.75/14.98/12.74 | F7 tweens 14.5 mm | 172.6 | 2.55 | - |
| LAC deconstruction | [070] Step 26 | hover | 40.5 | +X | 5/20/17 | 0.460 | 3.8/15.18/12.91 | F7 tweens 14.5 mm | 9.3 | 2.8 | - |
| LAC deconstruction | [072] Step 27 | hover | 58.3 | +Z | 5/20/17 | 0.745 | 6.15/24.61/20.92 | pose swap buzzer (173.5 mm between copies) | 3.5 | 0.34 | eye×1 |
| LAC deconstruction | [074] Step 28 | hover | 37.3 | +Y(up) | 5/20/17 | 0.480 | 3.96/15.86/13.48 | F7 tweens 14.5 mm | 79.7 | 2.57 | - |
| LAC deconstruction | [074] Step 28 | hover | 34.2 | +Y(up) | 5/20/17 | 0.480 | 3.96/15.86/13.48 | F7 tweens 14.5 mm | 82.1 | 2.36 | - |
| LAC deconstruction | [090] Step 35 | hover | 63.6 | +Y(up) | 5/20/17 | 0.600 | 4.95/19.82/16.85 | rocker switch tweens 85.1 mm | 4.0 | 0.75 | - |
| LAC deconstruction | [117] Step 44 | hover | 29.8 | +Y(up) | 5/20/17 | 0.430 | 3.55/14.21/12.08 | RTC module + coin cell tweens 21.7 mm | 2.1 | 1.37 | - |
| LAC deconstruction | [120] Step 45c | c | 39.4 | +Y(up) | 5/20/17 | 0.420 | 3.47/13.87/11.79 | resistor tweens 51.6 mm | 1.6 | 0.76 | - |
| LAC deconstruction | [123] Step 46 | hover | 46.8 | +Y(up) | 5/20/17 | 0.480 | 3.96/15.86/13.48 | resistor tweens 50.7 mm | 1.0 | 0.92 | - |
| LAC deconstruction | [126] Step 47 | hover | 64.2 | +Y(up) | 5/20/17 | 0.450 | 3.72/14.86/12.63 | Nano tweens 55.0 mm | 2.9 | 1.17 | - |
| LSM deconstruction | [001] Step 1 | hover | 69.5 | +Y(up) | 5/20/15 | 0.437 | 4.57/18.28/13.71 | stem tweens 62.6 mm | 1.9 | 1.11 | eye×1 |
| LSM deconstruction | [004] Step 2 | hover | 65.6 | +Y(up) | 5/20/15 | 0.307 | 3.21/12.85/9.64 | D8 tweens 54.1 mm | 3.8 | 1.21 | eye×1, image×1 |
| LSM deconstruction | [007] Step 3 | hover | 59.3 | +Y(up) | 5/20/15 | 0.402 | 4.2/16.79/12.59 | D7 tweens 67.8 mm | 0.3 | 0.87 | eye×1, image×1 |
| LSM deconstruction | [010] Step 4 | hover | 62.8 | +X | 5/20/17 | 0.683 | 7.14/28.57/24.28 | none found | - | - | image×1, eye×1 |
| LSM deconstruction | [013] Step 5 | hover | 80.1 | -X | 5/20/17 | 0.597 | 6.24/24.97/21.22 | D4 tweens 75.2 mm | 1.1 | 1.07 | eye×1, image×1 |
| LSM deconstruction | [016] Step 6 | hover | 45.6 | +Y(up) | 5/20/17 | 0.328 | 3.43/13.73/11.67 | D11 tweens 88.8 mm | 1.8 | 0.51 | eye×1, image×1 |
| LSM deconstruction | [016] Step 6 | hover | 47.0 | +Y(up) | 7/21/21 | 0.270 | 3.95/11.85/11.85 | D11 tweens 88.8 mm | 2.0 | 0.53 | eye×1, image×1 |
| LSM deconstruction | [019] Step 7 | hover | 45.1 | +Y(up) | 5/20/15 | 0.371 | 3.88/15.52/11.64 | D11 tweens 84.5 mm | 1.2 | 0.53 | eye×1, image×1 |
| LSM deconstruction | [019] Step 7 | hover | 41.7 | +Y(up) | 5/20/15 | 0.346 | 3.62/14.47/10.86 | D11 tweens 84.5 mm | 1.0 | 0.49 | eye×1, image×1 |
| LSM deconstruction | [022] Step 8 | hover | 70.6 | +Y(up) | 5/20/17 | 0.367 | 3.83/15.32/13.03 | D6 tweens 44.7 mm | 0.7 | 1.58 | - |
| LSM deconstruction | [025] Step 9 | hover | 70.6 | +Y(up) | 5/20/17 | 0.367 | 3.83/15.32/13.03 | pose swap D10 (57.1 mm between copies) | 1.7 | 1.24 | - |
| LSM deconstruction | [028] Step 10 | hover | 66.0 | +Y(up) | 5/15/14 | 0.330 | 3.45/10.35/9.66 | D9 tweens 54.4 mm | 2.0 | 1.21 | - |
| LSM deconstruction | [028] Step 10 | hover | 61.2 | +Y(up) | 5/15/17 | 0.330 | 3.45/10.35/11.73 | D9 tweens 54.4 mm | 1.7 | 1.13 | - |
| LSM deconstruction | [037] Step 14 | hover | 50.8 | -Y(down) | 5/20/17 | 0.424 | 4.43/17.73/15.07 | D10 tweens 48.4 mm | 0.8 | 1.05 | eye×1 |
| LSM deconstruction | [040] Step 15 | hover | 31.6 | +Z | 5/20/17 | 0.330 | 3.45/13.81/11.74 | jumper wire(s) tweens 30.5 mm | 3.6 | 1.03 | eye×1 |
| LSM deconstruction | [043] Step 16 | hover | 50.7 | -Z | 5/20/17 | 0.338 | 3.53/14.13/12.01 | D3 tweens 38.4 mm | 1.2 | 1.32 | image×1 |
| LSM deconstruction | [046] Step 17 | hover | 86.5 | +Z | 5/20/15 | 0.372 | 3.89/15.54/11.66 | pose swap D2 (57.1 mm between copies) | 0.7 | 1.51 | eye×2, image×1 |
| LSM deconstruction | [048] Step 18 | hover | 56.3 | -Z | 5/20/17 | 0.479 | 5.0/20.0/17.0 | push button tweens 84.8 mm | 3.7 | 0.66 | eye×1 |
| LSM deconstruction | [051] Step 19 | hover | 38.4 | +Z | 5/20/17 | 0.350 | 3.66/14.63/12.44 | jumper wire(s) tweens 94.8 mm | 6.8 | 0.4 | eye×1 |
| LSM deconstruction | [054] Step 20 | hover | 63.3 | +Z | 5/20/17 | 0.480 | 5.02/20.07/17.06 | none found | - | - | eye×1 |
| LSM deconstruction | [056] Step 21 | hover | 31.5 | +Y(up) | 5/15/17 | 0.220 | 2.3/6.9/7.82 | resistor 2 tweens 30.3 mm | 3.7 | 1.04 | - |
| LSM deconstruction | [059] Step 22 | hover | 20.6 | +Y(up) | 4/12/10 | 0.250 | 2.09/6.27/5.23 | capacitor tweens 29.1 mm | 4.7 | 0.71 | - |
| LSM deconstruction | [062] Step 23 | hover | 30.9 | +Y(up) | 5/20/17 | 0.123 | 1.28/5.14/4.37 | resistor 1 tweens 31.3 mm | 1.0 | 0.99 | - |
| LSM deconstruction | [065] Step 24 | hover | 40.5 | +Y(up) | 5/20/17 | 0.273 | 2.85/11.4/9.69 | Nano tweens 30.9 mm | 2.4 | 1.31 | - |
| PMG deconstruction | [001] Step 1 | hover | 15.8 | -X&+Y(up) | 5/20/17 | 0.044 | 5.22/20.88/17.75 | H14 tweens 2.5 mm | 5.1 | 6.32 | - |
| PMG deconstruction | [001] Step 1 | hover | 29.0 | -X&+Y(up) | 5/20/17 | 0.044 | 5.24/20.95/17.81 | H14 tweens 2.5 mm | 8.8 | 11.6 | - |
| PMG deconstruction | [002] Transition | transition | 64.4 | +X&+Y(up) | 5/20/17 | 0.074 | 8.77/35.08/29.82 | H14 slides 69.0 mm while fading out | 3.1 | 0.93 | - |
| PMG deconstruction | [005] Transition | transition | 62.2 | +Y(up) | 5/20/17 | 0.072 | 8.54/34.16/29.03 | pose swap dot matrix (20.4 mm between copies) | 18.2 | 3.05 | - |
| PMG deconstruction | [010] Transition | transition | 29.1 | +Y(up) | 5/20/17 | 0.046 | 5.46/21.83/18.56 | pose swap 4-digit display (11.1 mm between copies) | 25.4 | 2.62 | - |
| PMG deconstruction | [014] Step 4 | hover | 83.6 | +Y(up) | 2/10/17 | 0.045 | 2.13/10.63/18.07 | pose swap USB cable (114.6 mm between copies) | 23.2 | 0.73 | - |
| PMG deconstruction | [017] Step 5 | hover | 74.4 | -X&+Y(up) | 5/20/17 | 0.052 | 6.14/24.56/20.88 | H13 slides 80.1 mm while fading out | 2.9 | 0.93 | - |
| PMG deconstruction | [019] Step 6 | hover | 37.6 | -X | 5/20/17 | 0.038 | 4.47/17.87/15.19 | H12 tweens 7.6 mm | 1.2 | 4.94 | - |
| PMG deconstruction | [020] Transition | transition | 43.1 | +Y(up) | 5/20/17 | 0.045 | 5.27/21.07/17.91 | H12 slides 44.5 mm while fading out | 1.1 | 0.97 | - |
| PMG deconstruction | [022] Step 7 | hover | 46.1 | -X | 5/20/17 | 0.052 | 6.15/24.6/20.91 | H11 tweens 6.7 mm | 0.4 | 6.89 | - |
| PMG deconstruction | [023] Transition | transition | 57.2 | +Y(up) | 5/20/17 | 0.052 | 6.14/24.54/20.86 | H11 slides 53.1 mm while fading out | 0.0 | 1.08 | - |
| PMG deconstruction | [025] Step 8 | hover | 52.4 | +Y(up) | 5/20/17 | 0.057 | 6.71/26.82/22.8 | H10 tweens 4.1 mm | 1.8 | 12.79 | - |
| PMG deconstruction | [026] Transition | transition | 116.1 | -X | 5/20/17 | 0.058 | 6.86/27.46/23.34 | H10 tweens 126.0 mm | 2.8 | 0.92 | - |
| PMG deconstruction | [028] Step 9 | hover | 109.5 | -X | 5/20/17 | 0.100 | 11.8/47.22/40.13 | H9 key slides 142.5 mm while fading out | 0.4 | 0.77 | eye×1 |
| PMG deconstruction | [030] Step 10 | hover | 71.7 | +Y(up) | 5/20/17 | 0.058 | 6.9/27.6/23.46 | H8 slides 94.5 mm while fading out | 1.1 | 0.76 | - |
| PMG deconstruction | [032] Step 11 | hover | 45.2 | -Y(down) | 5/20/17 | 0.068 | 8.0/32.0/27.2 | H7 tweens 26.7 mm | 4.9 | 1.69 | - |
| PMG deconstruction | [033] Transition | transition | 115.9 | -Z | 5/20/17 | 0.068 | 8.01/32.03/27.23 | H7 slides 139.4 mm while fading out | 4.6 | 0.83 | - |
| PMG deconstruction | [037] Step 13 | hover | 34.5 | -Y(down) | 5/20/17 | 0.040 | 4.76/19.02/16.17 | H6 tweens 41.2 mm | 8.8 | 0.84 | - |
| PMG deconstruction | [038] Transition | transition | 114.6 | -Z | 5/20/17 | 0.036 | 4.25/17.0/14.45 | H6 slides 122.3 mm while fading out | 1.3 | 0.94 | - |
| PMG deconstruction | [040] Step 14 | hover | 34.8 | -Y(down) | 5/20/17 | 0.052 | 6.19/24.75/21.03 | H5 tweens 53.4 mm | 11.5 | 0.65 | - |
| PMG deconstruction | [041] Transition | transition | 102.7 | -Y(down)&-Z | 5/20/17 | 0.069 | 8.18/32.71/27.81 | H5 slides 117.2 mm while fading out | 0.8 | 0.88 | - |
| PMG deconstruction | [043] Step 15 | hover | 105.0 | +X | 5/20/17 | 0.064 | 7.58/30.31/25.76 | H4 slides 65.0 mm while fading out | 0.0 | 1.62 | - |
| PMG deconstruction | [045] Step 16 | hover | 84.0 | -X | 5/20/17 | 0.066 | 7.82/31.27/26.58 | H1 slides 52.4 mm while fading out | 0.8 | 1.6 | - |
| PMG deconstruction | [047] Step 17 | hover | 45.1 | +Z | 5/20/17 | 0.057 | 6.7/26.8/22.78 | dot matrix slides 68.2 mm while fading out | 0.1 | 0.66 | - |
| PMG deconstruction | [049] Step 18 | hover | 65.9 | +Y(up) | 5/20/17 | 0.062 | 7.32/29.26/24.87 | jumper wire(s) slides 89.9 mm while fading out | 0.7 | 0.73 | - |
| PMG deconstruction | [051] Step 19 | hover | 42.2 | +Z | 5/20/17 | 0.070 | 8.23/32.94/28.0 | jumper wire(s) slides 29.6 mm while fading out | 2.3 | 1.43 | - |
| PMG deconstruction | [053] Step 20 | hover | 44.7 | +Y(up) | 5/20/17 | 0.082 | 9.73/38.9/33.07 | button module slides 27.2 mm while fading out | 0.1 | 1.64 | - |
| PMG deconstruction | [055] Step 21 | hover | 30.6 | -Z | 5/20/17 | 0.052 | 6.12/24.46/20.79 | 4-digit display slides 22.1 mm while fading out | 0.2 | 1.38 | - |
| PMG deconstruction | [057] Step 22 | hover | 50.9 | +Y(up) | 5/20/17 | 0.059 | 6.97/27.88/23.7 | jumper wire(s) slides 74.7 mm while fading out | 0.0 | 0.68 | - |
| PMG deconstruction | [057] Step 22 | hover | 43.3 | +Y(up) | 5/20/17 | 0.059 | 6.97/27.87/23.69 | jumper wire(s) slides 74.7 mm while fading out | 1.3 | 0.58 | - |
| PMG deconstruction | [059] Step 23 | hover | 28.5 | +Y(up) | 5/20/17 | 0.025 | 2.96/11.85/10.08 | Nano slides 25.9 mm while fading out | 0.0 | 1.1 | - |

## 14. Renders inspected (50 frames)

| guide | frames | what was checked |
|---|---|---|
| LAC Full Build | [001] [004] [006] [015] [032] [055] [059] [090] [092] [098] [104] [109] [111] [121] [123] [125] [128] (+ full-resolution crops of [123] [128]) | corner lines to base cut-outs; 2 diagonal Nano pins; RTC end pins; single axis line for switch, pot, nut; tab-tip to slot; L-shaped polylines; lines on a cross-faded panel; 4 of 6 / 4 of 8 tabs on end panels; peel, spread and carry arrows |
| LSM Full Build | [006] [013] [034] [037] [048] [050] [053] [055] [057] [064] [069] [071] [075] [078] (+ crop of [078]) | 4 corner pins; capacitor legs; button axis line; tilt-in and swing lines; elbow polylines; posts through plate; dashed-flag lines drawn solid; red dot inside slot; removal and carry arrows |
| LSM Part 1 / Part 2 | [009] crop, [021] crop | dashed-flag lines drawn solid; resistor lead tips to holes; nut axis line |
| PMG Full Build | [002] [057] [063] [065] [067] [083] [091] [097] [101] [105] [113] [115] | 4 corner pins into socket ends; USB axis line; one line per tab; hook then swing stages; key tongue; display on brackets; leftover lines on Step 51c not visible; shield arrow |
| Deconstruction | LAC [001] [070]; LSM [013]; PMG [025] [028] | arrow tail on part, head in free space; opposed pair; one arrow for four keys; arrow with eye icon and inset |

## 15. Working files

`reports/_work_dim_leadlines/`: `core2.py` (replay + transforms), `extract2.py` (all2.json: every line/arrow showing with anchors and travel), `stats2.py`, `consolidate.py`, `poseswap.py`, `steps_class.py`, `arrows.py`, `arrow_gone.py`, `arrow_swap.py`, `arrow_tail.py`, `arrow_stats.py`, `linewidth2.py`, `tables.py`, `crops/`.
