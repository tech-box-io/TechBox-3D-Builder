# Verification notes: labels, eye icon, image callouts and section cards

Skeptic pass over `reports/dim_labels.md`. Everything below was re-derived with my own code in
`reports/_work_verify_labels/` (none of the analyst's `ann.json` / `*_rows.json` files were read).

## Method

- `replay.py`: fresh replay of the 20 raw payloads with a field-wise (deep) merge of step deltas, plus a shallow merge
  alongside it to test the "digest artefact" claim. Step classes reproduced exactly: Step N 425, Step Nc 424,
  Transition 117 (4 are typos: Transititon, Ttansition x2, Transiton), card 31 + 2 LAC Electronics views, Start 19,
  end 19 (one typo: Copmleted View). Total 1037.
- `pix_under.py`, `pix_match.py`, `pix_leader.py`: located every label rule in the saved pictures (`thumbs_raw`) by
  colour, matched 214 of 214, then tested that a cyan line really runs from a rule end to the stored leader tip
  (210 of 214; the 4 failures are one stale step, see below).
- `eye_pix.py`: FFT template match for the eye glyph, 226 of 226 found (median score 0.93).
- `img2.py`: located 35 of 45 inset frames in the pictures.
- `thick.py`, `centre.py`, `white.py`, `eye_white.py`, `misc.py`, `redend.py`: rule thickness, cap height, text
  centring, white-space tests, ring diameter, ring-to-lead-line distance.
- About 25 frames and 4 contact sheets viewed by eye.

## Verdicts in one table

| id | verdict | main reason |
|---|---|---|
| LBL-1 | confirmed | every style count reproduced exactly |
| LBL-2 | qualified | "2-3 characters" excludes the rail labels the same rule defines (26 of 214 are 7-8 characters) |
| LBL-3 | confirmed | 126 label steps, 38 with one, 88 with two, none with more; 214 of 214 on Step N |
| LBL-4 | confirmed | link-target counts exact; ring sits 0.3-0.6 % H from the red line end on rigid steps |
| LBL-5 | confirmed | all placement statistics reproduced within 1 % |
| LBL-6 | qualified | ordering and no-crossing hold 86 of 86; "same slots through a run" does not |
| LBL-7 | qualified | "two extreme holes" of a multi-pin part is 2 authored steps, LAC only; LSM does it differently twice |
| LBL-8 | confirmed | 7 showings, 3 texts, 6 em, no rule, no leader |
| EYE-1 | confirmed | all counts exact |
| EYE-2 | qualified | counts exact, but "whenever" is 79 % in builds and about half in deconstructions |
| EYE-3 | qualified | the 15-35 % band holds for 167 of 218 (77 %) |
| EYE-4 | confirmed | 23 of 424; 21 are real check cues |
| IMG-1 | qualified | "any picture" and "never in the bottom third" both need narrowing |
| IMG-2 | confirmed | class counts exact |
| IMG-3 | confirmed | 18 showings on 9 steps, LSM only |
| IMG-4 | confirmed | 19 of 19 |
| CARD-1 | qualified | 13 guides, not 12; cards cover about half of the bought-in components |
| TXT-1 | confirmed | popups 0, descriptions 55, tooltips 20 of 20 |
| NEV-1 | confirmed | no counter-example found |
| LIFE-1 | confirmed | 535 of 544 |
| POS-1 | qualified | mechanism real on PMG, but the reference frame is not 2:1 in general and the registered point is the callout centre |
| COL-1 | confirmed | all counts exact |

## Detail per pattern

### LBL-1 confirmed
214 underline labels of 223 label showings; border `#7fdbff` 214; thickness 5 on 212, 6 on 2 (LSM "c16"); leader type
line, solid, `#7fdbff`, no control point 214; ring "Life Saver Circle" 214, size 1.2 on 203 and 1.0 on 11; bold 214;
black 214; 3 em on 175 (LAC 84, PMG 84, LSM FB 7), 2.5 em on 39; Arial on 126, unset on 88; box 175x90 on 143 and
175x75 on 25; one link each. Shallow merge loses the leader colour on 24 labels and 10 eyes, deep merge on none, so
the "digest artefact" explanation is right. Render check: 208 of 208 unambiguous leaders leave the rule end nearest
the target. 122 distinct placements reproduced.

Small things the report does not say:
- 5 showings carry `margin-left: 25px` in the paragraph (LAC "g1" Step 3 x2, LSM "i2" Part 2 Step 5 / Part 1+2
  Step 13, LSM FB "i3" Step 15). The text renders 5-9 % of the rule length right of centre. So "centred" is 207 of 214
  in the picture, 212 of 214 by attribute.
- `leader_start_position.x` is exactly 0 or 1 on 210; 4 showings store 0.985.
- `shadow_enabled` is true on all 214 but nothing is visible with the underline container.

### LBL-2 qualified
Text classes reproduced exactly (hole 92, rail 24, capitals pin 50, shield 38, lower-case outliers 8, "Pin d12" 2;
distinct texts LSM 13, LAC 30, PMG 28). Length: 2 characters 76, 3 characters 112, 7 characters 12, 8 characters 14.
The rule text says "2-3 characters" and in the same sentence defines "(+) red" / "(-) blue". Corrected rule: hole and
pin identifiers are 2-3 characters (188 of 188 of those classes); rail labels are 7-8 characters and widen the rule
to 9.2-11.7 % of width. The PMG 4-digit display card photo prints CLK / DIO in capitals, which confirms that
"clk" / "dio" are slips.

### LBL-3 confirmed
Wire steps in the three full builds re-identified by hand from my per-step table: LAC Steps 9-14, 20-21, 36-39
(12 loose jumpers, 2 labels + eye), Steps 16-18, 30-34 (8 pre-attached leads, 1 label + eye); PMG Steps 3-14, 16-24
(21, 2 labels + eye); LSM Steps 10-12 (1 label), 13-15 (1 label + 2 discs), 19 (2 labels). 48 in all, 0 lead lines
on any of them.

### LBL-4 confirmed
Targets: breadboard 95 (LAC 72, LSM 23), wire connector housing 24 (LSM 21, LAC Deconstruction 3), module pin 51,
shield strip 42, Nano pin row 2. Note the link object is the whole breadboard body; the hole is only a 3D point in
the link data. Pixel check on the 34 non-stale labels of lead-line steps: 32 rings are within 0.02-0.63 % H of a red
line; the 2 that are not are "Pin d12" (on the Nano's pin row, as the analyst states).

### LBL-5 confirmed
My sample is 168 labels in ~2:1 frames (analyst 170). Target outside rule span 168 of 168; label further from the
centre line than its target 163; above target 148 (88 %); drop median 8.8 % H (quartiles 4.7, 11.5); horizontal gap
median 14.5; leader length median 19.2 (14.4, 23.4; range 2.8-44.4); angle median 35.2 deg (22.5, 42.8); centre x
21.0-74.0; rule y 12.9-66.4; 0 in the bottom third. The 20 below-target labels are the same list. White space: 211
of 214 text boxes under 2 % coloured pixels; the only real intrusion is LAC Step 6 "h29" (panel corner inside the
box, glyphs still clear). No leader passes through another label's text box (0 of 214).

### LBL-6 qualified
All 86 two-label steps with a valid render (65 at ~2:1 plus 21 at 2.79:1): leaders cross 0; flanking 42 with the
left label owning the left target 42 of 42; stacked 44 with the upper label owning the upper target 44 of 44.
Stacked rules 9.1-37.8 % H apart, median 14.8.
The slot clause does not hold as written. LAC six-jumper run (Steps 9-14): stacked right, stacked right, flanking,
flanking, stacked left, stacked left. PMG button block: module label left edge moves from 50.6 to 66.1 % W
(15.5 % of width, not "a few percent"), shield label 55.9 to 65.2. Only a label for a fixed connector stays put
(LAC LCD pin labels: left edge 18.8-20.4 %, rule y 55.9-59.3 %).

### LBL-7 qualified
Label + lead-line steps: LAC FB Steps 3, 5, 6, 7 and LSM FB Steps 5, 6, 8 (7 of 55 label steps) as claimed.
Five of those seven authored steps are two-lead parts, where "the two extreme holes" is simply both holes. For
multi-pin parts the evidence is two steps, both LAC (Nano c15 / g1, RTC j24 / j19). LSM handles the same case two
other ways: Part 1 Step 3 names one Nano pin and the hole it enters ("Pin d12" + "c16", 4 lead lines) and Full Build
Step 3 has 4 lead lines and no labels.

### LBL-8 confirmed
"2x" on LAC Step 4 and 4c (Part 1 and Full Build), "64X" in LSM Part 4 and Part 3+4, "64x" in LSM Full Build.
All 6 em, container none, leader none, colours `rgb(0,116,217)` and `rgb(127,219,255)`. Each still carries one 3D
link, which is unused.

### EYE-1 confirmed
226 showings (LAC 110, PMG 62, LSM 54); width 7.81 on 144, 8.2 on 62, 20 outliers (7.92 x10, 6.29, 7.58, 8.24, 8.7,
9.37 x2 each); no container 225; leader `#7fdbff` 226, 5 px on 224; ring `#7fdbff` 223, teal 3; fade 226; one eye on
208 steps, two on 9. Leader start points toward the target on 217 of 218; PMG at the left or right corner 58 of 58.
In LAC and LSM the start point lies inside the glyph (x 0.06-0.95, y 0.25-0.77 of the square), so the cyan line is
visible over the iris in some frames (seen in LAC Part 1 [019]).

### EYE-2 qualified
Full builds: eye on 71 of 146 Step N; 66 of 84 without lead lines (79 %); 5 of 62 with lead lines; with labels 42.
Deconstructions: eye on 48 of 94 Step N, arrow only on 41. So the eye is the usual cue, not the invariable one:
18 build steps and 41 take-apart steps without lead lines have none. The five eye + lead-line steps are LAC Steps 2
and 46, LSM Steps 6 and 34, PMG Step 51.

### EYE-3 qualified
218 icons (8 stale excluded): distance median 23.6 % H (19.4, 27.8; range 11.2-56.9); with labels 20.1, alone 27.2;
above 121, level 52, below 45; left 123, right 95; octants identical to the report. In the 15-35 % band: 167 (77 %);
30 closer, 21 further. Unlike labels the eye does use the bottom third: 32 of 218 centres. On white: 214 of 218.
Not in the report: on label + eye steps the eye sits lower than both label rules on 72 of 87, and the loose wire it
marks is staged at least 14 % H (median 28.5) from either destination.

### EYE-4 confirmed
Step Nc with a 2D annotation: 23 (14 insets from 6 pictures, 7 eyes, 2 "2x"). Eyes on Nc are LSM and LAC only;
insets on Nc are in all three kits.

### IMG-1 qualified
45 framed insets, 22 pictures; frame `#7fdbff` thickness 5 on 43; radius 0.1 on 45; leader 5 px on 44; ring
`#7fdbff` on 41; widths N median 15.8, Nc 16.8, card 31.2; alone 24, with arrow 14, with lead lines 4, with eye 10.
Two clauses need narrowing:
- "any explanatory picture": the LSM "LED Matrix Diagram" (3 showings) is unframed, full-frame, no leader, no link.
- "never in the bottom third": true of the frame centre (0 of 35 located frames) but 11 of 35 frames extend into it,
  bottom edge at 70-81 % H (LAC 45c, LAC Step 1, LSM Step 1, LSM 34c, LAC Deconstruction Step 24, PMG Push Buttons).
Red rectangles: a loose red-pixel test flags 16 of the analyst's 17 pictures and the 17th (Dot Matrix, a darker red
box) is visible by eye, so 17 of 22 is reproduced. A strict pure-red test finds only 11, so the boxes are not one
fixed red.
The report's "112 non-eye image showings" is a slip; its own parts sum to 104 and so do mine.

### IMG-2, IMG-3, IMG-4 confirmed
IMG-2: cards 10 + 2, build N 11, build Nc 14, deconstruction N 10 (LSM 8, LAC 2, PMG 0). The Nano I/O photo has no
red box; the other four card photos do.
IMG-3: six disc images x three guides, widths 5.82-7.81, all with `#7fdbff` leader and ring.
IMG-4: 19 Start steps with exactly 2 unlinked, unframed images, both gone on the next step. Logo x 1.8-2.5
(PMG Deconstruction 5.1), y 4.0-8.1, width 33.2-39.5; title x 1.6-2.5 (3.8), y 61.0-64.6 (LSM Part 1 24.1), width
42.1-48.4 (58.3). In PMG the two are not on one edge (2.4 against 1.6).

### CARD-1 qualified
31 showings, pause, 800 ms, camera moves on 29, next step is always a Step N. Content by showing: framed picture 12,
eye only 7, quantity 3, flat diagram 3, nothing 6. Corrections: cards occur in 13 guides (16 build guides minus LSM
Part 3, LAC Part 4, PMG Part 3), not 12. Coverage: 14 component types get a card; breadboard, Nano, resistors,
jumper wires (all kits), the LAC potentiometer and the LSM push button do not, so the rule describes modules and
cables with something to identify rather than every bought-in component.

### TXT-1, NEV-1, LIFE-1, COL-1 confirmed
TXT-1: `popupType` none on 1037; descriptions 55 (LSM Part 1 6, Part 2 18, Part 1+2 28, 3 placeholders); tooltip
names 8-27 per guide. PMG Parts 1-3 and Full Build leave 45 solids with an empty name.
NEV-1: end views 0 of 19 with any annotation; Transitions 0 of 117 with 2D (15 carry 3D lines or arrows, all PMG).
"NANO I/O MODULE LABELS" is a real text annotation, the only caption-like text on any canvas.
LIFE-1: 544 2D objects ever shown, 535 on one step, 9 on two; Step N with any annotation 423, with 2D 251.
COL-1: label rules and leaders 214, eye leaders 226, eye rings 223, inset frames 43, inset rings 41; all 473 3D
lines and arrows `#ff0000`.

### POS-1 qualified
What holds: for PMG the same stored positions exist as 1.952:1 and 2.786:1 pictures, and the callouts are
re-registered. Identical labels (42 pairs): predicting the 2.79 position from the 1.95 one by scaling the offset
from screen centre with the aspect ratio gives a median error of 0.02-0.06 % W; without it 3.9-6.0 %.
Eyes: remap error 0.03-0.07 % W, no-remap 0.45-5.2 %. Insets: Push Buttons frame centre 67.8 -> 62.5 % (predicted
62.5), same y.

What needs correcting:
1. The registered point is the centre of the callout, not its stored top-left corner. Corner model error 1.5 % W,
   centre model 0.02 %. Vertically the same: the rule sits at box-centre + half the rendered height.
2. The reference frame is not 2:1 in general. Implied reference aspect: PMG builds 1.99-2.01 (so even the Full
   Build pictures at 1.952 are stretched by 1.022, which is the unexplained 1.013-1.018 slope in the report);
   PMG Deconstruction 1.857 (its four eyes render exactly at their stored x; a 2.0 reference would move them
   1.1-2.6 % W); LAC 2.064-2.076; LSM Parts 1/2 2.00. LAC with a 2:1 reference would show slope 0.968; it shows
   0.997-1.002. No project field records the reference (`default_camera.aspect_ratio` is 2.001 for PMG and 2.066 for
   LAC but 2.089 / 1.044 for LSM and 2.001 for PMG Deconstruction, so it is not it).
3. "Sizes stay a fraction of width" is only shown between two captures that have nearly the same CSS width. The same
   175 px box is 6.25 % W in LSM Parts 1/2, 7.0-7.2 % in PMG and 8.0-8.1 % in LAC, so a label is not a fixed
   fraction of the viewport. Images (eye, insets) are stored in % of width and do hold it (eye matched at 8.2 % W in
   both PMG shapes).
4. LAC and LSM give no evidence either way on re-registration: each has labelled pictures at one shape only.

## Stale data found beyond the report's list
- Labels: LSM Step 6 "j2" / "j3" in Part 1 and Full Build (4 showings). The picture and the stored positions
  disagree by 2-6 % W and no leader runs to the stored tip. The report lists only the eye on this step.
- Eyes, moderate (2-5 %): LAC FB Step 40 / Part 3 Step 8; LAC FB Step 53 / Part 4 Step 13; LSM Part 3+4 Step 3c.
  With the 8 gross ones that is 13 of 226, so 213 match.

## Numeric defaults that need changing
See the structured return; the main ones are rule length (depends on box width and capture), rule thickness
(0.36-0.46 % H, = rule / 35), authoring aspect (per guide, 1.86-2.07), card guide count (13), check cues (21 real).
