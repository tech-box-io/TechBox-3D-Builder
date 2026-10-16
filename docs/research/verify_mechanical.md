# Verification notes: Mechanical (wood, fasteners, enclosure) assembly conventions

Skeptic pass over `reports/dim_mechanical.md` (MECH-1 .. MECH-12 and 28 numeric defaults).

## 0. Method

- **Independent re-derivation.** I did not reuse the analyst's `state_*.json` / `mech_rows.json`. I wrote my own state
  walk over the raw payloads (`reports/_work_verify_mechanical/vwalk.py` -> `v_<guide>.json`), my own step grouping and
  step classifier (`vsteps.py`), and one script per check (`s1.py` .. `s20.py`). Everything below comes from those.
- **Semantics I verified against the raw data and the renders before trusting any number**
  - Part `position` replaces the node's local translation (not an offset from the CAD pose): top-level leaves such as
    `LSM_Stem-1` and `Capacitor leg-1` carry absolute coordinates. mm = units / `scaleFactor`. Scale checked on a known
    part: the half-size breadboard measures 56.1 x 8.5 x 83.0 mm in all 20 payloads (SF 1, 0.478, 0.606, 0.042).
  - Visibility is per leaf solid, as the analyst says, **but a `visible` flag written on a non-leaf node is pushed down to
    its subtree at that step**. The analyst's walk ignores node-level flags. Proof: LAC Full raw step 121 (Step 53c)
    sets `LAC Knob-3` (node) invisible with no leaf writes, and render [120] shows that knob gone; the PMG displays have
    node `visible:false` from raw step 0 yet are on screen from [034], so the flag is not a persistent parent switch.
    Effect on the analyst's numbers: negligible (one stale knob in LAC from [120]); none of the claimed counts move.
  - For rotating parts I measure displacement at the bounding-box centre of the largest solid, not at the node origin.
    The analyst's origin-based figure gives artefacts on pure rotations (see MECH-5, LAC Step 29).
- **Mechanical step set.** My classifier (wood tween / fastener tween / panel-mount / breadboard-onto-base / pose swap of
  a wood panel or of a module once two or more wood parts are up / remaining identical parts) independently lands on the
  same totals: **75 mechanical steps in the 3 masters (LSM 22, LAC 27, PMG 26) and 173 in the 16 build guides**; 425
  numbered steps in 19 guides; 1037 visible frames.
- **Renders looked at.** LSM Full sheets 032-079 and thumbs 068, 076, 078; LAC Full sheets 032-039, 048-063, 088-103 and
  thumbs 119, 120, 128; PMG Part 3 sheets 000-007, 016-031.

## 1. Verdicts

| id | verdict | one-line reason |
|---|---|---|
| MECH-1 | qualified | every stat reproduces, but the rule as worded only describes 15 of 28 new wood kinds |
| MECH-2 | qualified | counts exact; "one per tab", "never more than 4" and "hover frame only" each have counter-examples |
| MECH-3 | qualified | 36 of 37, not 37 of 37: PMG Step 26 introduces two different panels |
| MECH-4 | qualified | counts exact; "each stage has its own lead lines" fails for 5 of the 6 Transition-type joints |
| MECH-5 | qualified | counts exact; the potentiometer goes in shaft-first, and removals are done with no panel on screen |
| MECH-6 | qualified | counts exact; "anything with wires attached" is too wide - free-lead components do tween |
| MECH-7 | confirmed | 39 / 12 / 43-167 deg / 73 of 75 all reproduce |
| MECH-8 | confirmed | 221 labels, 0 IDs, 0 labels on 173 mechanical steps, 34 of 34 tooltips |
| MECH-9 | confirmed | wiring count constant through LSM and LAC case steps; PMG hides 74 parts for 7 steps |
| MECH-10 | qualified | counts exact; red box is on 4 of 6 c-step insets, LSM uses a baked-in eye instead |
| MECH-11 | qualified | counts exact; "no mating feature" is not what separates arrows from lines |
| MECH-12 | confirmed | 47 of 61, median 65 deg; travel is 0.86 on-screen (median) |

### MECH-1 - hover then one straight tween (qualified)

Reproduced exactly: 0 of 173 mechanical steps move the camera on an in-step Transition or on Step Nc (0 of all 331
numbered build steps). No colour / style / edge-style / scale write on any wood solid in a visible step after the title
page in any of the 20 payloads, except the single ghost step. All 44 wood translation stages in the masters are 800 ms.
Title-page slide-out exception confirmed in exactly the four guides named (LSM P3 [001] 69 mm, LSM P4 [001] 68 mm,
LAC P4 [001] 80 mm, PMG P3 [001] 40 mm).

What needs narrowing:
- **"In final orientation" and "one straight tween on Step Nc" hold for 15 of the 28 new wood kinds** (D4, D5, D6, D7,
  D8, D9; F5, F6, F8; H2, H3, H4, H8, H9, H13). The other 13 are the MECH-4 parts. 7 kinds arrive tilted (H10 7.9,
  H14 10.3, H7 11.7, H6 18.1, F2 21.4, D3 21.6, H5 23.6 deg) and 6 take two or three tweens inside their own step.
  MECH-1 does not list these as exceptions.
- Hover of the 28 kinds (first-stage travel): min 21.9, q1 53.9, **median 67.7**, q3 94.3, max 139.4. Analyst: q1 55,
  median 69. Same thing to within 1-2 mm.
- Edge-first / face-on split by travel versus panel normal: face-on n=9, median 64.3, range 21.9-69.4 (matches).
  Edge-first with the analyst's 16 parts: median 81, **range 40.0-139.4, not 43-139** - H2 at 40.0 mm is edge-first in
  the analyst's own Appendix B.
- Per-kit medians: LSM 64.3, LAC 79.2, **PMG 80.1** (report text says 87).
- Direction split "36 moves: down 15, sideways 14, diagonal 4, up 3" could not be reproduced on any basis I tried.
  First stage of the 28 kinds: sideways 12, down 10, diagonal 5, up 1. All 44 translation stages: sideways 20, down 17,
  diagonal 5, up 2. The conclusion (the axis is the joint axis, not "down") stands.
- The LED stem first appears on the "LED Stems" card [082], not on a Step N.
- Outside the claim's scope: in the take-apart guides 2 of 94 numbered steps do move the camera on an in-step Transition
  (PMG Decon Steps 2 and 3, frames [007] and [012]).

### MECH-2 - lead lines (qualified)

Reproduced exactly: lines on Step N over 425 steps = 0:276, 1:37, 2:69, 4:41, 6:2; never 3 or 5. Wood-tween steps in
masters (38) = 0:2, 1:6, 2:19, 4:11; all build guides (88) = 0:4, 1:12, 2:43, 4:27, 6:2. 363 line showings, all
#ff0000, scale "5", `world_units` false; 353 two-point, 10 polylines (8 three-point, 2 five-point); 36 stored dashed and
they render solid (thumb 078). 13 four-line panel steps in the masters. Length / first-stage travel: n=83, q1 0.93,
median 0.99, q3 1.02, 60 inside 0.85-1.10 (analyst n=81, 0.98, 63). Lines are parallel to the travel: 77 of 79 within
5 degrees.

Counter-examples to the wording:
- **"One line per tab-and-slot pair" is not what is drawn.** LAC F6 [128] has slots on all four edges and gets 4 lines,
  to the two corner tabs of F1 and of F2 only (render checked). Its mirror F5 goes on with F1, F3 and F4 already in place
  and gets lines to F1 and F3 only. PMG H8 gets 2. The real rule is a representative subset, 2 per chosen neighbour, capped at 4.
- **"Never more than 4"**: 6 lines on LSM P3 Step 5 [010] and LSM P3+4 Step 6 [012] (2 + 2 + 2 onto D3, D2, D1).
- **"On the hover frame only"**: PMG Full shows 2 fresh lines on the in-step Transition frame of Steps 48 [106],
  50 [111] and 51 [114], and Step 51c [115] still has 2 lines on (same in PMG P3 [048], [053], [056], [057]). No line is
  ever visible on a card, title, Completed View or between-step Transition.
- The "2 per neighbour" reading of LAC Step 49 is really 2 + 1 + 1 (F9 twice, each F7 post once).
- Stored `points` can be stale: line ends are bound to parts (`object_ids` + `object_local_positions`). LSM Full Step 26
  stores two 133 mm lines that show about 40 mm of red.

### MECH-3 - one kind of wooden part per step (qualified)

37 introducing steps confirmed (LSM 14, LAC 9, PMG 14); 4 identical pairs (LSM 27, 32, 33; LAC 41); 2 rest-of-set steps
(PMG 39 three keys, LSM 38 sixty-three stems); 82 degree camera turn between the two D11 pairs. Datum: D1, F3 and H1
fade in seated, and none of them is ever displaced in any frame of the 19 step-bearing guides. Hand-held mover 5 of 5.

- **"0 with two different kinds" is 1 of 37**: PMG Step 26 [059] brings in H1 (seated) and H2 (hovering) together. The
  analyst's own exception line says so; the stat line should read 30 single-kind + 1 two-kind + 4 pairs + 2 rest.
- "For larger sets animate one and fade the rest in" rests on two cases (n=3 and n=63).
- The stems are not plywood: one white (#ffffff) square rod, 3.17 x 3.17 x 66.7 mm, with no engraved ID.

### MECH-4 - two-motion joints (qualified)

Reproduced: 13 of 34 kinds; 8 split over two numbered steps (D3, D11, F7, F9, H5, H6, H7, H10) and 6 over an in-step
Transition (D10, F9, F2, H11, H12, H14; 7 Transition frames, camera held on all). Stage-2 camera re-aim on 5 of 8
(PMG 62, 67, 68, 85 deg; D11 117 deg). 7 of 9 second-stage numbered steps carry lines. Lock slide 6.7 / 7.6 mm,
push-home 7.0 mm, splay 15.1 / 16.0 deg.

- **"Each stage has its own lead lines" holds for the numbered-step variant (7 of 9) but for only 1 of the 6
  Transition-type parts** (H14, lines on [114]). F2 [126]-[127], H11 [092]-[093] and H12 [095]-[096] show nothing for
  stage 2; D10 and F9 use one L-shaped polyline for both legs.
- The "same view -> Transition, new view -> new step" criterion explains 5 of the 8 two-step parts; D3, F7 and F9 use a
  second numbered step with the camera held. The analyst says this (confidence medium); the rule text should not
  present it as the deciding rule.
- "Arrival tilt 7.9-25.8": 25.8 is F9, which arrives upright and tilts on its second Transition [100]; H14 arrives at
  10.3 and the 12.6 is its seating rotation. Tilt on arrival proper is 7.9-23.6 deg over 7 parts.

### MECH-5 - fasteners and panel-mount components (qualified)

Reproduced exactly: 27 fastener steps in 7 guides; 13 removals (13 with one arrow, 0 lines, all with an in-step
Transition); 12 fits (12 with one line, 0 arrows, 0 Transitions); 2 knob-setting steps (eye only); one fastener per step
27 of 27; 0 labels; fit hover 55.9-61.3 (LAC) and 80.4-83.1 (LSM); removal travel 37.6-37.9 (LAC) and 98.9-100.7 (LSM);
7 insertions 79.1-103.2 mm with one line each; axial line / hover n=19, median 1.16, 0.86-1.26; spin on 8 of 13 removals
and 3 of 12 fits; 3-11 parts on screen.

- **"Leads-first" is wrong for the potentiometer.** LAC Full Step 25 [055] (and LAC P2 Step 11) pushes the pot through
  F1 **shaft-first from behind**; washer, nut and knob then go on from the front ([057], [059], [061]). Leads-first is
  true for the push button (3 guides) and the rocker switch (2 guides): 5 of 7.
- **"Do the work on the loose panel"** is true for fits only. In the build guides all 9 removal steps (LSM 16; LAC
  22-24; and their copies) show the bare component with no wood on screen; the panel first fades in on the insertion step.
- "LAC Step 29 knob Nc 57 mm / rot 50" in Appendix C is an origin artefact: the knob only turns 49.8 deg in place.
- "1600 ms for a spinning nut" is 5 of the 11 spinning-fastener frames; the other 6 run at 800 ms (LSM Full refit [040],
  LSM Decon [049], LAC nut and washer in LAC Full and LAC P2).

### MECH-6 - tethered sub-assemblies (qualified)

Reproduced: 20 pose-swap steps in the masters (LSM 4, LAC 8, PMG 8), 45 in the build guides, none with a tween of the
swapped part; 7 pick-up / attach pairs + 6 single steps; cues 10 eye-only, 6 lines, 4 arrows (2 with an eye); gaps 4,
34, 29 steps.

- **"Never tween anything that has wires attached" is too wide.** Pre-wired components whose leads are still free are
  tweened together with their wires: button + 2 leads 102 mm (LSM Step 17), switch + 3 leads 81 mm (LAC Step 15), pot +
  3 leads 79 mm (LAC Step 25), and the USB plug with its cable 23 mm (PMG Step 25). The true rule is about parts whose
  wires are already plugged in at the far end; for those the count is 0 in all 16 build guides.
- "Normally two numbered steps" is 7 of 13 cases.

### MECH-7 - turning the kit over (confirmed)

39 up-axis changes in 12 guides; every one has a camera move in the same frame, 42.9-167.3 deg; 28 on a Step N, 8 on an
auto Transition (all LSM), 2 on a card, 1 on a Completed View. 22 of 75 master mechanical steps run under a non-default
up-axis in 6 runs. Effective elevation 10-60 deg on 73 of 75, median 33.9; the two outside are LSM Step 23 (-4.8) and
LAC Step 29 (7.6). No build-guide frame rotates more than hinge panels, fasteners, the knob and one capacitor.

Notes, none of which change the verdict: LSM Step 23 is a plan view (up-axis used to set screen-up, not to turn the
kit); "group underside work" is shown by PMG only; LSM Decon Step 14 [037] re-poses the matrix wire harness by 180 deg
during a scene cut.

### MECH-8 - engraved IDs and tooltips (confirmed)

221 label showings; none matches a part ID, part name or hardware size; 0 labels on any frame of the 173 mechanical
steps (also 0 on the take-apart mechanical steps). All 34 kinds have dark engraving solids (#1e1616) on a #deb887 body
and a `Description` tooltip. Wording variants beyond those listed: LSM D11 reads "Parts D11", four PMG H10 solids read
"Nano Board Bracket - H10" with no "Part", and one LSM D6 pose copy has no tooltip.

### MECH-9 - what stays on screen (confirmed)

Non-wood parts on screen: LSM Steps 21-38 constant at 23-24; LAC Steps 41-57 constant at 67-68; PMG 0 for Steps 26-32
(all 74 hidden at [059], back at [073]), then 74 to the end. Opacity below 1 only on LSM Full Step 34 [075] and its two
copies. Addition: frame-edge cropping of loose sub-assemblies is just as visible in LAC ([088]-[103]) as in PMG.

### MECH-10 - result checks (qualified)

Master mechanical c-steps: 65 clean + 1 with leftover lines (PMG 51c), 6 inset, 3 eye; all build 150 + 2, 14, 7.
9 insets, 13.2-22.2 % wide, 6 on the c-step and 3 on the hover step.

- **Red box on 4 of the 6 c-step insets** (LAC 25c, LAC 45c, PMG 33c, PMG 38c). The two LSM ones (30c [068], 34c [076])
  have an eye glyph and cyan leader drawn inside the picture and no red box.
- Border is #7fdbff / 5 on 8 of 9; PMG 33c is #7fb9ff / 2.
- The rule fires on 9 of 75 completed steps; it is an exception device, not a default.

### MECH-11 - arrows (qualified)

12 arrows on 11 master steps (10 on mechanical steps + 2 peel steps); 7 in the body 5 / head 20 x 15-17 style; lengths
24.7-102.9 mm; 0 of 75 mechanical steps with both an arrow and a line; the only frame in 20 guides with both visible is
LSM P1+2 Step 20 [041]. Take-apart showings 24 / 22 / 31 arrows against 0 / 3 / 0 lines.

- **"No mating feature to link" does not separate the two cues.** 4 of the 12 arrows pull a fastener off a shaft, and
  every take-apart removal uses an arrow on a tab-and-slot joint. What the data supports: arrow = something comes off, is
  flexed or is carried by hand; lead line = something goes onto a target.

### MECH-12 - camera re-aim (confirmed)

47 of 61 (77 %), median 64.8 deg, 32 at 45 deg or more; 108 of 141 in all build guides; PMG 24 of 26. Of the 14 held
steps, 4 follow a between-step Transition that already moved the camera (LSM 24, 27, 35; LAC 49), so the view is fresh
on 51 of 61. New measurement for "travel runs across the screen": on-screen share of the first-stage travel vector is
median 0.86, minimum 0.66, at least 0.8 on 29 of 37.

## 2. Numeric defaults

| default | claimed | recomputed | status |
|---|---|---|---|
| plywood thickness | 3.0 (3.2 on D3, D8, stems) | 3.00 on 32 kinds; 3.18 on D3 and D8; stem is a 3.17 mm square rod | ok, stem is not sheet |
| hover, new wood part | median 69, q1 55, q3 94, 22-139 | median 67.7, q1 53.9, q3 94.3, 21.9-139.4 | ok (use 68) |
| hover, edge-first | median 82 (43-139) | median 81 (40.0-139.4), n=16 | lower bound is 40 |
| hover, face-on | median 64 (22-69) | 64.3 (21.9-69.4), n=9 | ok |
| hover / longest dimension | 0.7 (0.2-1.4) | 0.7 (0.2-1.4) | ok |
| breadboard onto base | 47 / 49 / 39 | 46.9 (LAC Full, P1), 49.2 (LSM Full), 39.3 (LSM P1, P1+2) | ok |
| panel-mount hover | 79-103, at least body + leads | 79.1-103.2 | ok; pot is shaft-first |
| nut / washer / knob hover | 56-61 LAC, 80-83 LSM | 55.9-61.3, 80.4-83.1 | ok |
| fastener removal travel | 38 LAC, 99-101 LSM | 37.6-37.9, 98.9-100.7 | ok |
| LED stem hover | 44 / 50 / 55 | 43.5 / 50.3 / 55.1 | ok |
| lead lines per frame | 1, 2, 4; max 4 | 37 / 69 / 41 steps; 6 on 2 steps | ok as "usual max" |
| line length, wood | 0.98 x travel (0.93-1.01); PMG travel - 3.4 | 0.99 (0.93-1.02), n=83; PMG -3.0 to -3.5 on 6 lines | ok |
| line length, axial | 1.16 x hover (0.86-1.26) | same, n=19 | ok |
| line style | #ff0000, scale 5, solid | 363 of 363; 36 stored dashed | ok |
| hinge tilt on arrival | 8-26, about 20 | 7.9-23.6 on arrival (7 parts); 25.8 is F9 mid-move | narrow to 8-24 |
| lock slide / push-home / splay | 6.7-7.6 / 7.0 / 15-16 | 6.7, 7.6 / 7.0 / 15.1, 16.0 | ok |
| step duration | 800; 1600 for a spinning nut | 1030 of 1037 at 800; 5 nut frames at 1600 | 800 ok; 1600 is 5 of 11 spin frames |
| nut spin | about half a turn (171-180) | 170.9-179.6 on 6 of 7 LSM nut moves; 115.1 on LSM Full refit | add the 115 |
| ghost opacity | 0.5 | 0.5, one authored use + 2 copies | ok |
| arrow | #ff0000, body 5, head 20 x 15-17, 25-103 mm | 7 of 12 in that style; 24.7-102.9 | ok |
| eye icon width | 7.8 % (8.2 % PMG) | 7.81 x17, 7.92 x1, 8.2 x7 | ok |
| inset | 13-22 %, #7fdbff | 13.2-22.2; #7fdbff on 8 of 9 | ok, one #7fb9ff |
| camera turn on entry | median 65, 77 % | 64.8, 47 of 61 | ok |
| view height | 10-60, median 34 | 73 of 75, median 33.9 | ok |
| camera turn at up-axis change | 43-167 | 42.9-167.3, 39 changes | ok |
| wooden parts per step | 1 (84 %) | 31 of 37 counting PMG Step 26 as one; 30 strictly | ok |
| two-motion share | 38 % | 13 of 34 | ok |
| text labels on mechanical steps | 0 | 0 of 173 | ok |

## 3. Patterns the analyst missed

1. **Every mechanical hover frame carries a cue; none is bare.** 75 master mechanical Step N frames: lines 52 (4 with an
   eye, 2 with an inset), eye only 13, arrow 9 (2 with an eye), inset only 1, nothing 0. Same in all 173 (0 bare).
2. **The enclosure phase starts only after all wiring, and the USB-cable step is the hand-over in all three kits.**
   Last step with a text label / USB step / first case step: LSM 19 / 20 / 21, LAC 39 / 40 / 41, PMG 24 / 25 / 26.
   No label-bearing step occurs after the first case step.
3. **Insertion side follows the hardware, not the leads.** The pot goes shaft-first from the inside and its washer, nut
   and knob go on from the outside; the button and switch go leads-first from the outside.
4. **Lead-line ends are bound to parts, not stored as fixed coordinates** (LSM Step 26: 133 mm stored, about 40 mm seen).
5. **Wood has two colour tokens and two exceptions.** Body #deb887 and engraving #1e1616 on all 34 kinds. LSM D2 has an
   extra face skin in #855e42, so its outer face renders dark brown in every view ([037], [048], [068]). Stems are white.
6. **An unfinished joint stays visibly unfinished between steps.** D11 posts sit 7.0 mm proud from 32c to 34c; F7 posts
   stay splayed across Step 43; D3, H5, H6, H7, H10 and F9 stay tilted between their two numbered steps.
7. **Removals in the build guides happen before the panel exists on screen** (9 of 9 removal steps show no wood).

## 4. Extra anomalies seen (not conventions)

- LSM P3+4 Step 18 [040]: the exemplar stem moves a further 9.7 mm on the "rest of the stems" step.
- LSM Full Step 34c [076]: the D1 node is still stored at opacity 0.5 while its body solid is back at 1; it renders opaque.
- LAC Full: `LAC Knob-3` is hidden at Step 53c through a node-level flag only, which a leaf-only reader misses.
- PMG Decon Steps 2 and 3 have three in-step Transitions each, the third one a camera move.
- Two Transition frames are set to `pause` instead of `play`: LAC Decon [033] and [118].
- The report's PMG median hover (87 mm) does not match its own Appendix B rows (80 mm).

## 5. Files

`reports/_work_verify_mechanical/`: `vwalk.py` (state walk), `v_<guide>.json`, `vc.py`, `vsteps.py` (grouping, features,
classifier), `vshow.py` (frame dump), `s1.py`-`s20.py` (one check each), `hover_rows.json`.
