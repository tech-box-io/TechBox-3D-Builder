# Guide report: LCD Alarm Clock (LAC) - Part 1

- Guide id: `19075-lcd_alarm_clock_lac_-part_1` (kit LAC, role: part)
- Sources read: `digest/19075-lcd_alarm_clock_lac_-part_1.md` (all 390 lines), all 4 contact sheets, 30 of 32 individual thumbs at full size, plus targeted queries on `digest/*.json` and `cadasio_raw/*.json` (camera targets, lead-line end points, label styling, step flags).
- Working crops and helper scripts: `reports/_work_lac_p1/`.
- Step indices below are the digest's `[NNN]` viewer indices (000-031).

## 1. Summary

Part 1 builds the electronic core of the clock on a breadboard: the student peels the adhesive backing off a half-size breadboard, sticks it onto laser-cut wood base panel F3, plugs in an Arduino Nano, bends and installs two resistors, plugs in a Real Time Clock (RTC) module with its coin cell, splits a 6-way jumper ribbon into single wires and then fits the six wires one at a time. The guide has 32 viewer steps: a title page, 14 numbered steps each authored as a "Step N" (hover/intro view, annotated) + "Step Nc" (completed view, clean) pair, one auto-advancing Transition, one named section card ("Real Time Clock") and a "Completed View". There is no instruction text anywhere (all 32 step descriptions are empty, no popups); everything is communicated by the 3D motion plus four annotation devices: red lead lines (12), cyan-underlined hole labels (20) and one "2x" quantity label, a black eye icon (10 uses), and one red arrow with one inset picture. One part is added per step without exception; rigid pin parts hover 34-47 mm straight above their seat and drop vertically, while wires never travel - a loose straight wire is shown parked beside the model and is swapped for a routed wire in the "c" step. The camera moves on only 10 of 32 steps and never on a "c" step.

## 2. Step table (every viewer step)

Screen positions are label/image top-left as % of viewport (x, y). "LL" = red lead line. Camera is `distance mm / elevation / azimuth`.

| idx | name | kind | what is added or done | annotations | camera |
|---|---|---|---|---|---|
| 000 | Start | title page, pause | Finished Part-1 result shown as hero at right of frame (27 parts visible: F3, breadboard, Nano, 2 resistors, RTC, 6 routed wires) | 2 unanchored images: TechBox logo SVG at (2, 6) w 38.9 %; title PNG "LCD Alarm Clock (LAC) / Part 1 / (c) 2025 TechBox..." at (2, 64) w 42.1 % | set: 277 / 44 / 49; model pushed right to clear the text |
| 001 | Step 1 | hover (a removal action) | Everything hidden except the breadboard (already lifted 46.9 mm to its hover height) and its grey backing sheet. Action: peel off the adhesive protective backing | 1 red 3D arrow, 24.7 mm, pointing straight down from the breadboard's bottom front edge; 1 inset image callout (cyan rounded rectangle, w 20.5 %, at (64, 46)) = render of the underside captioned "Protective Backing", cyan leader + ring on the breadboard's bottom corner | MOVES (fade cut): 72.7 deg, 277 -> 237; 237 / 33 / -49 |
| 002 | Transition | auto-play 800 ms, hidden from step picker | Backing sheet translates 53.2 mm straight down away from the breadboard | arrow + inset fade out; none left | unchanged |
| 003 | Step 1c | completed | Backing sheet fades out; bare breadboard remains (still at hover height) | none | unchanged |
| 004 | Step 2 | hover | Wood base panel F3 fades in already in its seated pose under the hovering breadboard (the breadboard is the mover) | 4 LL, 47.9 mm each, vertical, one per breadboard corner ending in the matching corner slot of F3; eye icon at (65, 8) with cyan leader to the breadboard's top corner by the row/column lettering | small MOVE (fade): 4.9 deg, target 19 mm; 237 / 31 / -54 |
| 005 | Step 2c | completed | Breadboard tweens 46.9 mm straight down onto F3 (seated) | none | unchanged |
| 006 | Step 3 | hover | Arduino Nano fades in 39.8 mm straight above its seat | 2 LL, 41.2 mm, from the two diagonally opposite corner pins into their holes; labels "c15" (35, 20) and "g1" (62, 33) whose rings sit on those same two holes | unchanged |
| 007 | Step 3c | completed | Nano tweens 39.8 mm down (straddles the centre channel, rows c-g, columns 1-15) | none | unchanged |
| 008 | Step 4 | hover, isolated part-prep | All context hidden; one resistor with straight leads alone in close-up | "2x" (blue #0074d9, Arial bold 6em, no box, no leader) at (54, 12); eye icon at (30, 45) pointing at the resistor's black centre band | MOVES (fade cut): 73.4 deg, 237 -> 110 (x2.16); 110 / 29 / -141 |
| 009 | Step 4c | completed (prep) | Straight leads swapped for bent, staple-shaped leads (fade swap of sub-solids, no motion) | "2x" stays (only annotation in the guide that survives into a "c" step); eye removed | unchanged |
| 010 | Step 5 | hover | F3 + breadboard + Nano fade back in; resistor #1 is seen hovering 37.1 mm above its holes | 2 LL (40.4 / 40.2 mm) from each lead tip into its hole; labels "(-) blue" (32, 30) and "h27" (57, 58); "2x" removed | MOVES (tweened pull-back, no fade): 110 -> 277 (x0.4), 7.6 deg; 277 / 29 / -133 |
| 011 | Step 5c | completed | Resistor #1 tweens 37.1 mm down | none | unchanged |
| 012 | Step 6 | hover | Resistor #2 (already bent) fades in 40.0 mm above its holes | 2 LL, 43.2 mm; labels "(-) blue" (33, 31) and "h29" (58, 55) | unchanged |
| 013 | Step 6c | completed | Resistor #2 tweens 40.0 mm down | none | unchanged |
| 014 | Real Time Clock | section card, pause, isolated | Context hidden; RTC module (blue PCB, black cell holder, CR2025 coin cell) alone, already in its hover pose | eye icon at (62, 23) pointing at the coin-cell face; no text on screen | MOVES (fade): 277 -> 175 (x1.59), 7.3 deg; 175 / 22 / -130 |
| 015 | Step 7 | hover | Context fades back; RTC stands upright 33.6 mm above its seat | 2 LL, 37.2 mm, from the two END pins (Pin1, Pin6) of the 6-pin header into their holes; labels "j24" (39, 27) and "j19" (64, 26) | MOVES (fade) back to 277 / 29 / -133 |
| 016 | Step 7c | completed | RTC + cell tween 33.6 mm down (seated) | none | unchanged |
| 017 | Step 8 | hover, isolated part-prep | Context hidden; 6-way jumper ribbon alone (black, dark red, grey, purple, blue, green) | eye icon at (49, 16) pointing at the middle (grey) wire | MOVES (fade cut): 70.7 deg, target 138 mm; 175 / 54 / 130 |
| 018 | Step 8c | completed (prep) | The wires slide apart sideways (tweened, by 4.4 to 15.2 mm each) so the ribbon becomes six single wires = "separate the ribbon" | none | unchanged |
| 019 | Step 9 | hover (wire) | Context fades back, now seen from the opposite side; only the black wire remains, lying straight on the "table" at lower-left | eye icon at (24, 34) on the wire's mid-point; labels "i23" (64, 15) and "(+) red" (63, 26); no lead lines | MOVES (fade): 175 -> 277, target 104 mm; 277 / 54 / 128 |
| 020 | Step 9c | completed | Loose black wire fades out; routed black wire + its 2 Dupont housings fade in in place (i23 to + rail) | none | unchanged |
| 021 | Step 10 | hover (wire) | Loose green wire appears in the same parking spot | eye (23, 35); labels "i24" (61, 13) and "(-) blue" (62, 23) | unchanged |
| 022 | Step 10c | completed | Green wire swapped to routed (i24 to - rail) | none | unchanged |
| 023 | Step 11 | hover (wire) | Loose purple wire, same spot | eye (22, 34); labels "a8" (27, 14, left) and "i22" (60, 16, right) | unchanged |
| 024 | Step 11c | completed | Purple wire routed over the Nano (i22 to a8) | none | unchanged |
| 025 | Step 12 | hover (wire) | Loose blue wire, same spot | eye (22, 33); labels "a9" (25, 15) and "i21" (59, 17) | unchanged |
| 026 | Step 12c | completed | Blue wire routed (i21 to a9) | none | unchanged |
| 027 | Step 13 | hover (wire) | Loose light-grey wire, same spot | eye (23, 33); labels "a14" (27, 8) and "(-) blue" (18, 19), both left | unchanged |
| 028 | Step 13c | completed | Grey wire routed (a14 to - rail) | none | unchanged |
| 029 | Step 14 | hover (wire) | Loose dark-red wire, same spot | eye (22, 35); labels "a12" (28, 10) and "(+) red" (19, 19), both left | unchanged |
| 030 | Step 14C | completed | Red wire routed (a12 to + rail) | none | unchanged |
| 031 | Completed View | final, pause | Nothing added; finished Part-1 assembly | none | MOVES (tweened orbit): 55.5 deg, same distance; 277 / 44 / 38 |

Totals actually shown: 12 lead lines (4+2+2+2+2), 21 labels (20 hole/rail labels + "2x"), 13 images (2 title, 1 inset, 10 eye icons), 1 arrow.

## 3. Conventions found (evidence and exceptions)

### 3.1 Structure

1. **Skeleton = Start -> numbered pairs -> Completed View.** [000] title page, [001]-[030] fourteen numbered steps, [031] "Completed View". Always true here.
2. **Every numbered step is a pair: "Step N" then "Step Nc".** 14 of 14. "Step N" is the annotated intro/hover view; "Step Nc" is the same camera with the part seated and all annotations removed. Exception in naming only: [030] is "Step 14C" (capital C).
3. **No words outside callouts.** 32 of 32 step descriptions are empty, 0 popups. The only student-facing text is the title image, 20 hole/rail labels, "2x", and the caption baked into the inset picture ("Protective Backing").
4. **Transition steps are auto-playing in-betweens, not numbered.** One instance [002]: behaviour `play`, 800 ms, flagged hidden from the step picker, sits between Step 1 and Step 1c, carries an intermediate motion (backing sheet drops 53.2 mm) and clears the annotations. No camera move.
5. **A named section card introduces a new electronic module right before the step that installs it.** One instance [014] "Real Time Clock": context hidden, module alone in close-up, eye icon only, no on-screen title (the name lives only in the step list). The Nano, breadboard, resistors and wires do not get a card.
6. **Part-preparation is a numbered step of its own, shown isolated.** Step 4 [008]/[009] (bend resistor leads) and Step 8 [017]/[018] (split the ribbon). In both, all other parts are hidden and the camera cuts to a close-up; the context returns in the next numbered step.
7. **Numbering restarts at Step 1 in each Part** (Part 1 = Steps 1-14; in the Full Build the same content is Steps 1-14 of 57).
8. **Title page layout**: logo top-left (2, 6) w 38.9 %, title/part/copyright image lower-left (2, 64) w 42.1 %, hero render of this Part's end state at right. Same positions and widths in LAC Parts 2-4.
9. **Uniform timing**: every step 800 ms; parts show/hide by fade, move by tween; camera tween speed 2, no orbit animation.

### 3.2 Granularity

10. **Exactly one physical part is installed per numbered step** - 14 of 14. The two identical resistors get two separate install steps (5 and 6); the six wires get six steps (9-14). Never two wires in one step.
11. **Multiples are only grouped for preparation, with a quantity label.** Step 4 shows one resistor with "2x" (do this to both); Step 8 shows the whole ribbon separating into all six wires at once.
12. **"Parts on screen" grows by one student-level part per pair** (wire steps add 1 wire + 2 connector housings = 3 components, visible solids +5).

### 3.3 Ordering

13. **Bottom-up / base-first**: backing off -> breadboard onto wood panel F3 -> microcontroller (Nano) -> small passives (2 resistors) -> tall module (RTC) -> wires last.
14. **Prep immediately before first use**: resistor bend (Step 4) directly before resistor install (5, 6); ribbon split (Step 8) directly before the first wire (9).
15. **Wiring order** (6 wires): module power first (Step 9 RTC i23 -> + rail, Step 10 RTC i24 -> - rail), then module signals (Step 11 i22 -> a8, Step 12 i21 -> a9), then the controller's rail feeds (Step 13 a14 -> - rail, Step 14 a12 -> + rail). So "power before signal" holds for the module, but the Nano's own rail connections come last, and +/- order is not fixed (+ then - for the RTC, - then + for the Nano).

### 3.4 Motion

16. **Rigid plug-in parts first appear hovering straight above their seat (+Y) and drop vertically in the "c" step.** 5 of 5 seatings: breadboard 46.9 mm [005], Nano 39.8 mm [007], resistor #1 37.1 mm [011], resistor #2 40.0 mm [013], RTC 33.6 mm [016]. Hover offsets range 33.6-46.9 mm (not a single standard value); always pure vertical, single stage, no rotation.
17. **The mover is the part the student handles, not necessarily the new part.** In Step 2 [004] the new part (F3) fades in already seated and the existing breadboard is the one hovering and travelling down.
18. **Wires do not travel.** 6 of 6: "Step N" shows a loose straight wire model parked flat beside the assembly; "Step Nc" fades that out and fades in a different, pre-routed wire model (plus its two Dupont housings) in the installed position. Same swap technique for the resistor leads straight -> bent [009].
19. **Parking spot is constant**: all six loose wires appear at the same place, orientation and size (lower-left of frame, diagonal, eye-icon target at x 25-28 %, y 54-57 %), each moved 159-177 mm from where it lay in the ribbon view of Step 8. The wire is beside the model on the table plane, not above its holes.
20. **No rotations, no multi-stage moves** in this guide. The only extra motion is the single Transition [002].

### 3.5 Red lead lines

21. **Lead lines are used only for rigid vertical insertions.** 12 lines over 5 steps ([004] x4, [006] x2, [010] x2, [012] x2, [015] x2). 0 of 6 wire steps, 0 on prep steps or the section card.
22. **Style**: #ff0000, solid, constant on-screen thickness (line scale 5, same weight as the cyan leaders), 2 points, vertical.
23. **End points = mating feature -> its target**: the four bottom corners of the breadboard (a 54.8 x 82.6 mm rectangle) -> the points on F3 directly below, each landing at a small corner slot of the panel [004]; Nano pin tips -> breadboard holes [006]; resistor lead tips -> holes [010], [012]; RTC header pin tips -> holes [015].
24. **Count rule**: for a multi-pin part only two pins are drawn - the two extremes (Nano: diagonally opposite corner pins c15 and g1, 14 columns x 4 rows apart; RTC: Pin1 and Pin6 of the 6-pin header; resistor: its two leads). The 4-cornered mechanical placement gets 4.
25. **Length is approximately the hover offset**, slightly longer because the lower end is anchored a little inside the target: 47.9 vs 46.9 mm (x1.02), 41.2 vs 39.8 (x1.04), 40.4/40.2 vs 37.1 (x1.09), 43.2 vs 40.0 (x1.08), 37.2 vs 33.6 (x1.11). For the four breadboard-hole steps the lower end is at one common height (Y = 890.1 mm), a few mm below the breadboard's top face, so the line visibly enters the hole.
26. **Lead lines live only in "Step N"** and are removed on "Step Nc" (5 of 5).

### 3.6 Arrows

27. **One red 3D straight arrow** in the guide ([001], 24.7 mm, body width 5, head 20 x 17), pointing straight down from the breadboard's lower edge to show the peel-off direction. Arrows are for a removal/direction-of-pull, not for ordinary insertion (insertions use lead lines).

### 3.7 Labels and callouts

28. **Hole labels**: lowercase row letter + column number, no space ("c15", "g1", "h27", "h29", "j24", "j19", "i23", "i24", "i22", "i21", "a8", "a9", "a14", "a12" - 14 labels).
29. **Rail labels**: "(+) red" and "(-) blue" = polarity sign in parentheses + stripe colour, used instead of a coordinate because any hole in the rail will do (6 labels: 2 x "(+) red", 4 x "(-) blue").
30. **Exactly two labels on every step that plugs something into the breadboard** - 10 of 10 (Steps 3, 5, 6, 7, 9-14): the two end holes. Steps with no breadboard hole involved (1, 2, 8) have none; Step 4 has only "2x".
31. **Label style (20 of 20)**: Arial bold, black, 3em (project base font 20); container type "underline" in cyan #7fdbff, thickness 5; straight cyan leader (thickness 5) leaving from the end of the underline nearest the target (left end when the label is right of its target, right end when left of it; 19 exact, 1 at 0.987); target marked with a cyan dashed "Life Saver Circle" ring on the hole.
32. **Label ring = lead-line end.** Where a step has both, each label's ring sits on the hole where a red line terminates ([006], [010], [012], [015]).
33. **Placement**: labels sit in the white margin beside the model, on the side of their target. Wiring view: breadboard/RTC-side labels at right (x 59-64 %, y 13-26 %), Nano-side labels at left (x 18-28 %, y 8-19 %). When both labels are on the same side the hole coordinate is on top and the rail label below ([019], [021], [027], [029]). Labels are above their targets in 18 of 20 cases (exceptions: "h27", "h29" sit below-right at y 55-58 %).
34. **Quantity label "2x"**: digit then "x", blue #0074d9, Arial bold 6em, no container, no leader, upper right of the part [008]-[009].
35. **Inset picture callout** (1 use, [001]): a cyan rounded-rectangle frame (border 5, w 20.5 % of viewport) holding a small render of a view the main camera cannot show (underside of the breadboard) with its own caption, joined by a cyan leader and ring to the feature.
36. **All annotations are cleared for the completed view**: 13 of 14 "c" steps have zero annotations (exception: "2x" in [009]). [031] has none.

### 3.8 Eye icon

37. **Black eye icon + cyan leader and ring = "find/inspect this loose part".** 10 uses, always on a "Step N" or section card, never on a "c" step: breadboard orientation corner [004], resistor colour bands [008], RTC coin cell [014], ribbon [017], and each of the six loose wires [019], [021], [023], [025], [027], [029]. Size 7.81 % of viewport width (7.92 % twice), no container. It sits just above its target in 9 of 10 cases (below-left in [008]).
38. **Where the eye is absent**: steps where the part was already presented by a preceding isolated view (Step 5, 6 after Step 4; Step 7 after the RTC card) and Step 3 (Nano), Step 1 (inset instead).

### 3.9 Camera

39. **The camera never moves on a "c" step or on the Transition** (0 of 15). It moves on 10 of 32 steps: [000], [001], [004], [008], [010], [014], [015], [017], [019], [031].
40. **Long fixed runs.** One camera serves Steps 2-3 ([004]-[007]), one serves Steps 5-7 ([010]-[016], apart from the card), and one serves all six wires ([019]-[030], 12 consecutive steps).
41. **Three work stations plus close-ups, distances from a small set (110 / 175 / 237 / 277 mm, FOV 45 deg perspective)**:
    - A, base + Nano: 237 / 31-33 / -49 to -54.
    - B, resistors + RTC (opposite end of the board): 277 / 29 / -133.
    - C, wiring: 277 / 54 / 128 (higher, looking down so both wire ends and hole lettering are visible).
    - Isolated close-ups: resistor 110 / 29 / -141; RTC card 175 / 22 / -130; ribbon 175 / 54 / 130. Each keeps roughly the azimuth of the station that follows it.
    - Hero views: Start 277 / 44 / 49, Completed View 277 / 44 / 38.
42. **The view is not zoomed onto the hole.** In assembly views the whole F3 + breadboard stays in frame and fills only about 40-45 % of the frame width; labels and lead lines do the pointing. Isolated parts likewise fill about 40-45 % of the width (RTC about 60 % of the height).
43. **Off-centre framing to make room**: in the wiring station the orbit target is about 60 mm below the board so the assembly sits upper-centre/right and the lower-left is free for the parked wire and eye icon; on the title page the model is pushed right.
44. **Context swaps are cuts with a fade transition** (step `transition: fade` on [001], [004], [008], [014], [015], [017], [019]); the pull-back at [010] and the final orbit at [031] are plain tweens.
45. **Completed View** = same model, no annotations, camera orbits to a 3/4 hero angle close to the Start view.

### 3.10 Look

46. White background (#ffffff), toon shading on every part, black 1 px edges (edge angle 40), no silhouette, matt, perspective camera. Annotation palette is only three colours: red #ff0000 (lead lines, arrow), cyan #7fdbff (label underline, leaders, rings, inset frame), black (label text, eye icon), plus blue #0074d9 for "2x".

### 3.11 Wiring specifics

47. **Wire colour identifies which wire to pick up; it is not an electrical colour code.** Black -> (+) rail, green -> (-) rail, purple and blue -> signals, light grey -> (-) rail, dark red -> (+) rail. The colours are simply the six colours of the ribbon separated in Step 8.
48. **Wires go in a free hole of the same column strip as the pin they connect to**: RTC pins sit in row j (j19-j24), wires go in the adjacent row i (i21-i24); Nano pins sit in rows c/g, wires go in row a of the same column (a8, a9, a12, a14).
49. **Ribbon consumption order** is black, green, purple, blue, grey, red (ribbon order is black, red, grey, purple, blue, green), i.e. not sequential across the ribbon.

## 4. Part looks

| part | look in the renders |
|---|---|
| Background / edges | pure white; black 1 px outlines on every part; flat toon colour |
| Wood base panel F3 | flat tan/wood #deb887, slightly darker cut edges, near-black engraved "F3" (#1e1616); rectangular slots and tab notches |
| Breadboard | white #ffffff body with light-grey side faces, black #000000 hole insets and lettering, blue #0074d9 and red #ff0e00 rail stripes, small white side clips |
| Protective backing ("Paper") | flat mid-grey #aaaaaa sheet |
| Arduino Nano | dark navy PCB #000f41, black pin-header strips (#1e1616), silver pins and components #a6a9aa, light-grey mini-USB shell #cccccc, black ICs, 2x3 ICSP header standing up |
| Resistor | bright blue body #0074d9 with bands brown #a36315 / red #ff0e00 / black #000000 / red / brown; silver leads #a6a9aa (straight, then bent to a staple shape) |
| RTC module (HW-84) | bright blue PCB #0074d9, black cell holder #191919, silver coin cell #a6a9aa embossed "CR2025 3 VOLTS +", cream/gold header pins #f4e5a7, grey/silver SMD parts and black ICs on the back |
| Jumper wires, loose | straight round wire; black #2d2926, dark red #800000, grey #aaaaaa, purple #611b6c, blue #0074d9, green #2ecc40 |
| Jumper wires, routed | smooth arcs from hole to hole; black #2d2926, green #10cc62, purple #611b6c, blue #0074d9, light grey #cccccc, dark red #800000 |
| Dupont housings ("Wire Cap V2") | black #1e1616 rectangular housing with a small wire-coloured window and a silver pin #a6a9aa |
| Lead lines / arrow | red #ff0000, thin solid; arrow is a 3D shaft with a cone head |
| Labels | black bold Arial on a cyan #7fdbff underline, cyan leader, cyan dashed ring at the target |
| Eye icon | solid black eye glyph, cyan leader and ring |
| Inset picture | white box, cyan rounded border, small render with its own caption |

## 5. Anomalies and inconsistencies

1. **Step name typo**: [030] is "Step 14C" (capital C); the other 13 completed steps use lowercase "c", and the Full Build names the same step "Step 14c".
2. **Hidden leftover part**: the backing sheet "Paper-1", which the student removed in Step 1, is switched visible again at [019] and stays visible through [031] (it is also flagged visible on the Start page [000]). Its stored position at [019] (Y 887.6 mm) is 46.9 mm below its Step-1 height, i.e. back in its CAD place sandwiched between the seated breadboard and panel F3, so it is occluded in every saved view; it is still logically "present" in the finished model.
3. **Wire colour against polarity**: the black wire goes to the (+) red rail [019] and the green wire to the (-) blue rail [021], while later the grey wire goes to (-) and the red one to (+). Colour is not used as a polarity code and the black-to-plus choice could mislead.
4. **Loose and routed wire models differ slightly in colour**: green #2ecc40 loose vs #10cc62 routed; grey #aaaaaa loose vs #cccccc routed (the routed one reads as white).
5. **Lead lines are hand-placed**: the extra length over the hover offset varies (1.0, 1.4, 3.1-3.3, 3.2, 3.6 mm); the two lines of [010] differ (40.4 vs 40.2 mm); several lean 0.3-0.9 mm off vertical; authored directions are mixed (some bottom-to-top, some top-to-bottom).
6. **Hover offsets are not standardised**: 33.6, 37.1, 39.8, 40.0, 46.9 mm; the two identical resistors use 37.1 and 40.0 mm.
7. **Eye icon size varies**: 7.92 % wide in [017] and [019], 7.81 % in the other eight.
8. **"2x" label**: persists into the completed step [009] (the only annotation that does) and its text carries a trailing zero-width space.
9. **Transition style inconsistency**: the context swap at [010] (close-up back to assembly) is a tween with no fade, whereas the six other context swaps use a fade transition.
10. **Section card has no visible title**: "Real Time Clock" exists only as the step name; nothing on screen names the module.
11. **Dormant annotations**: the project holds 150 annotations but this guide ever shows only 47 (21 of 41 labels, 12 of 49 lead lines, 1 of 7 arrows, 13 of 53 images). The rest (e.g. labels j27, j29, j1, a5, b8, b9, GND, VCC, SDA, SCL) belong to later Parts of the same shared project.
12. **Authoring leftovers in the data**: a hidden default "Start" step still carrying Cadasio's boilerplate description precedes the real title step; "Step 1" and "Transition" share authoring index 3; label "a12" sits at (28, 10) here but (26, 9) in the Full Build.
13. **CAD pose quirks (not student-visible)**: the Nano carries a permanent 2.6 mm (one hole pitch) offset from its CAD pose. The digest lists the resistors and the backing sheet as "displaced" by about 1.7 m at all times; for these components the stored step position is effectively an absolute coordinate (the sheet's CAD transform translation is (743, 888, 1228) mm, matching its stored positions), so only their step-to-step MOVE deltas (37.1, 40.0, 53.2 mm) are meaningful. The RTC's hover is stored along the module's local axes ([0, 0, 33.6] / [33.6, 0, 0]); the render and the vertical lead lines show it is 33.6 mm straight up in the world. Two CR2025 coin-cell instances move with the RTC although one cell is seen.
14. **Digest naming quirk to keep in mind**: the digest's automatic colour names call the purple wire (#611b6c) "dark grey" and the dark-red wire (#800000) "brown".

## 6. Relation to the other LAC guides

- **Part 1 is the first 14 steps of `19075-lac_full_build`, verbatim.** Viewer steps [002]-[028] are identical in the two digests (same moves, cameras, annotations and screen positions); [029] differs only by the "a12" label position, [030] only by the "14C" capitalisation. Part 1 adds its own Start page (hero shows only the Part-1 result; own title PNG) and its own Completed View; in the Full Build step 31 is the next section card ("Rocker Switch").
- All LAC build guides come from one shared project: identical annotation inventory (53 images / 41 labels / 7 arrows / 49 lead lines) in Parts 1-4, Full Build and Electronics, with each Part showing only its slice.
- Numbering restarts per Part: Part 1 Steps 1-14, Part 2 Steps 1-18, Part 3 Steps 1-8, Part 4 Steps 1-17 = Full Build Steps 1-57.
- Section cards recur with the same role in later Parts ("Rocker Switch" in Part 2; "Alarm Buzzer", "LCD Screen", "USB Cable" in Part 3); Part 4 (wood enclosure) has none. Title page image positions and widths are the same in Parts 2-4.
- Pin-name labels (GND, VCC, SDA, SCL) that are dormant here are used in Part 3 for the LCD wiring, so Part 1's hole-coordinate-only labelling is specific to breadboard-to-breadboard wires.
