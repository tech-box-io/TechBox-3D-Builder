# Verification notes: Step granularity and build ordering

Skeptic pass over `reports/dim_granularity.md`. Everything below was recomputed with my own code in
`reports/_work_verify_gran/` (not the analyst's `_work_dim_granularity/`), then spot-checked against contact sheets.

## Method

- `common.py` groups viewer frames into numbered steps by order (`Step N` ... `Step Nc`), independent of the printed number.
- `mytrack.py` is my own leaf-level visibility/displacement tracker over `cadasio_raw/*.json`. I needed it because the
  digest's APPEAR/MOVE lines are blind to every part whose top node is flagged hidden in the CAD tree (all LSM and LAC wall
  panels). Checked against renders: LSM Full [048] shows D4 hovering with 4 lead lines, [053] D3 tilted, [073] two D11 posts
  hovering; the digest reports none of these, my tracker reports all three. The analyst's statement about this digest
  limitation is correct.
- `feat.py` builds one feature row per numbered step for all 19 stepped guides (frames, Transitions, annotations on the
  opener, parts appearing/moving/rotating, camera change, scene up-axis). `q1.py` ... `q12.py` are the individual checks.
- Indices `[NNN]` are the digest list position (the thumbnail number), not the JSON `order_index`.
- Sheets viewed: LSM Full 040-055, 072-087; LAC Full 008-023, 104-119; PMG Full 000-007, 032-039, 072-087; LSM Decon
  000-015, 040-047; LAC Electronics 000.

## Totals that reproduce exactly

| quantity | analyst | mine |
|---|---|---|
| numbered steps, full builds | 38 / 57 / 51 = 146 | same |
| numbered steps, all 16 build guides with steps | 331 | 331 |
| numbered steps, take-aparts | 24 / 47 / 23 = 94 | same |
| frames per build step (master) | 131 / 13 / 2 | 131 / 13 / 2 |
| frames per build step (all) | 300 / 27 / 4 | 300 / 27 / 4 |
| wire steps master / all | 48 / 103 | 48 / 103 |
| loose jumper = 2 labels + 1 eye + 1 wire + 2 housings | 33/33, 66/66 | 33/33, 66/66 |
| captive lead = 1 label + 1 eye + 1 wire + 1 housing | 8/8, 16/16 | 8/8, 16/16 |
| identical-pair placement steps | 4 master, 11 all | 4, 11 |
| steps moving two different kit items | 0/48 | 0 in all 331 build steps |
| section cards in full builds | 14 | 14 (4 + 5 + 5) |
| slices identical to full build | LAC 57/57, PMG 51/51 | LAC 57/57, PMG 51/51 on my annotation signature; LSM 64/77 |
| steps per single-part guide | 5, 8, 8, 11, 12, 13, 14, 14, 17, 18, 26 | same |

## Verdicts

**GRAN-1 qualified.** The pair structure holds: every one of 331 build steps has an opener and a closer, both `pause`,
with 0-2 in-step Transitions, all 35 of them `play`. Two wording problems. (a) "331/331 have both halves" needs the
stand-ins: 330 have a literal `Step Nc`; PMG Part 1 Step 14 [032] is closed by `Completed View`; LSM Part 4 `Step 8` is
closed by `Step 9c`. (b) "One step per hand action" is not what the data shows. The unit is one kit item, and one number
can hold several hand motions: 9 master steps chain 2-3 motions with Transitions (LSM 29; LAC 45, 52, 56; PMG 42, 43, 48,
50, 51) and each of the 33 loose-jumper steps contains two insertions, while LSM gives each wire end its own number.
Counts 128/146, 288/331, 34/146 (LSM 9, LAC 16, PMG 9) reproduce. 145/146 openers are annotated (PMG Step 15 [035] is
bare); 11/146 closers still carry an annotation.

**GRAN-2 confirmed.** 0 of 331 build steps tween two different kit items (the only multi-component moves are RTC + coin
cell and the USB plug parts). 6 receivers fade in seated: LSM [004], [037]; LAC [004], [032], [055]; PMG [059]. 56 master
steps carry text labels, 55 of them destination labels (LAC Step 4 [008] is "2x"), 54 handle one part.

**GRAN-3 qualified.** The four pair steps and the 2+2 split with an 82 degree turn are right. "Never animate more than
two parts together" is false as written: LSM Step 34 [075]-[076] tweens all four D11 posts 7.0 mm at once (also LSM Part 4
Step 8, Part 3+4 Step 14). "Same travel" is also loose: Step 33 is 83.1 vs 77.4 mm (same direction, different distance).

**GRAN-4 qualified.** Three batch cases confirmed in renders ([082] "64x", [085] eye, [086] 63 stems; PMG [085] inset
"H9 3x"; PMG [073] two eyes, [075] one eye). But the threshold is mis-stated: 3, 3, 63 are the sizes of the remainder. The
groups are 4, 4 and 64. No group of exactly 3 identical parts exists in any kit, and one of the four groups of 4 or more
(the D11 posts) is not batched. So it is 3 of 4 groups, smallest batched group 4.

**GRAN-5 confirmed.** All counts reproduce in master and slices. Label texts and wire colours checked per step.

**GRAN-6 confirmed.** Component counts per kit item reproduce (switch 7, pot 7, push button 5, buzzer 5, RTC 3, USB 3,
jumper 3, captive lead 2). LAC Electronics [000] has 31 components; they are 9 kinds of item but 10 pieces (two resistors).

**GRAN-7 confirmed.** 15/15 preparation steps show only the item being prepared (the rest of the build is hidden and
fades back on the next step). 6/6 removal-preps are arrow, auto Transition, gone. 6/6 ribbon splits match the following run (3, 6, 2, 4, 12, 9).
Extra anomaly: the section card sits after the split twice (PMG Step 2 then `Push Buttons`; LAC Step 35 then `LCD Screen`)
and before it once (PMG `4-Digit Display` then Step 15).

**GRAN-8 confirmed.** 8/8 and 7/7 single-part hardware steps. Order off knob, nut, washer; on washer, nut, knob, in both
LAC Full and LAC Decon. Evidence is one hardware stack (the pot) plus one nut; no screws in any inventory.

**GRAN-9 qualified.** The two mechanisms and the counts (7 own-step, 9 in-step) reproduce; camera never moves inside a
build step (0 of 31 steps with a Transition over all build guides). The decision rule "new viewpoint, new number" explains
5/7 and is not the only reading: 6 of the 7 own-step second stages are a swing (rotation) of a part already hooked in
(LSM 25; LAC 46; PMG 30, 32, 36, 41), the 7th is the four-post push-home. Rotations also occur inside in-step chains
(LAC 45 second Transition, LAC 56c, PMG 51c), so neither criterion separates the cases cleanly.

**GRAN-10 qualified.** 6/10 wired seats are immediately preceded by the pick-up step; the 7th (LSM 28 then 30) has
Step 29 between. 9/9 pick-ups have an eye and no lead line; 19/19 are pose swaps.

**GRAN-11 confirmed.** 14/14 cards, 3/3 base panels, PMG module fade-ins at [013], [020], [027].

**GRAN-12 confirmed.** Boundaries, restart at 1, LSM Part 2 swap of the last two steps, and the repeated panel step in LSM
Part 3+4 all reproduce.

**ORD-1 qualified.** True for the three full builds. Over the 7 guides that contain the USB step it is the last
electronics step in 5; LSM Part 2 and Part 1+2 put the panel first. "All wiring before the first enclosure panel" needs
"before a panel is joined to the base": LSM D2 is on screen from Step 17 and LAC F4 / F1 from Steps 15 / 25 as loose
carriers. In LSM and LAC the first part placed is the breadboard (Step 2), the controller is second (Step 3).

**ORD-2 qualified.** 11/11 blocks contiguous. Two things the wording hides: plug-in parts are front-loaded regardless of
the module they serve (LAC resistors at h27/h29 go in at Steps 5-6, the switch they serve arrives at Step 15), and the
pot's lead run starts after the knob-turn step, the buzzer's after a card.

**ORD-3 qualified.** Within-module pin order holds (PMG 6/6, LAC LCD, captive leads red, tan, black 3/3; the digest colour map calls the tan lead grey). "Ascending
controller pin order" is PMG only: LAC goes rows 8, 9, 14, 12, 1, 3, 5, 4, 8, 9. PMG is non-decreasing 20/20 only if the
Step 10 label "S5" is read as S6; as printed it is 19/20.

**ORD-4 qualified.** 3/3 sub-assembled in isolation. "Much later" is LAC only (panels attached at Steps 49 and 54); in
LSM the panel goes on at Step 21, two steps after its leads and as the first enclosure step. Isolated steps are 12, not 7
(LSM 16-18; LAC 15, 22-29).

**ORD-5 qualified.** Datum first and cover last 3/3. Direction counts reproduce within one borderline case (mine: down 24,
sideways 17, oblique 6, up 1; LSM Step 24 is 28 degrees off the axis). "Right after its mount exists" fails for the LAC
LCD (mount F9 at Steps 45-46, LCD hung at Step 52). "High-count parts last" rests on the LSM stems alone; PMG's four keys
go in at Steps 38-39 of 51.

**ORD-6 confirmed** as a PMG-only observation. LAC's count of 10 is mostly isolated views (pot sub-assembly, ribbon), not
the model being turned.

**ORD-7 confirmed.** PMG 14/14; LSM 7/10; LAC 4/8.

**DEC-1 qualified.** Counts reproduce. "Identical multiples together" is not general: LAC removes its two identical
resistors in separate steps (45, 46), the four LSM posts go 2+2, and LAC unplugs every wire singly.

**DEC-2 confirmed.**

**DEC-3 confirmed.** Ratios reproduce. Rank correlation with my own mapping: LSM -0.90 to -0.96, LAC -0.91 to -0.97,
PMG -0.98 to -0.99 depending on whether wires and pose copies are included.

## Numeric defaults

All reproduce except these:

- Frames per take-apart step: by viewer frames it is 37 / 49 / 6 / 2 for 2 / 3 / 4 / 5 frames. The analyst's 50 / 5 counts
  Transitions; LAC Decon step 40 has a stray extra pause frame ([104] `Step 41`).
- Maximum parts animated together: 2 on first placement, 4 in LSM Step 34.
- Batch threshold: groups of 4, 4, 64, not "3 or more".
- Take-apart viewer frames per step: 2.65-2.88 (stated as 2.7-2.9).
- Insertion direction: 24-25 / 17 / 5-6 / 1.
- Spearman: -0.90 to -0.99, mapping dependent.

## Missed

1. Unnumbered Transitions between steps: 7 in the full builds, 16 over all build guides, none in take-aparts. LSM uses
   them to turn the model back ([052] 130 degrees, [059] 53, [077] 110, each with an up-axis change); LAC [108] reframes;
   PMG [013], [020], [027] bring in the next module.
2. PMG builds the housing frame with the electronics hidden (Steps 26-32, 2-6 parts on screen) and brings the wired
   cluster back at Step 33 (80 components). LSM and LAC build the enclosure around the electronics.
3. Batching is never used where destination labels are needed: four identical PMG button modules take 12 single-wire
   steps.
4. The four-post push-home is one joint second stage for parts placed in two separate steps.
5. Anomalies not in the report: `Transititon` (LAC Decon [002]), `Ttansition` (LAC Full [053], LAC Part 2 [023]),
   `Transiton` (LSM Decon [038]), `Step 20C` (LSM 1+2 [042]), `Step 14C` (LAC Part 1 [030]), `Copmleted View` (LSM 3+4
   [042]), `Completed Build` in LSM Part 2 and 1+2; two LAC Decon Transitions set to pause ([033], [118]); PMG labels
   `clk | s8`, `dio | s9` in lower case; PMG Step 51c [115] keeps two lead lines.
