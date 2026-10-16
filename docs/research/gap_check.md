# Completeness check of the verified pattern set

Scope: the 20 published TechBox guides, re-read from `cadasio_raw/*.json` (own replay in `reports/_work_gap/replay.py`), the digests, and the saved renders. Indices in square brackets are viewer indices, the same numbers as `thumbs/<guide>/NNN.jpg`. Contact sheets made for this check are in `reports/_work_gap/*.jpg`.

Three results matter most for the Mini Robot Arm:

1. The 20 guides contain no screw, servo, joystick, tool or moving joint. Everything the rulebook says about fasteners rests on one nut on a push button (LSM) and a knob, nut and washer on a potentiometer (LAC).
2. No guide ever moves a student-built sub-assembly as a rigid unit. Bench sub-assemblies are built at the pose where they will lie parked, and their only later move is a cross-fade because by then they are wired.
3. Several rules marked "confirmed" as absolutes have counted exceptions, and two verifier notes on part visibility disagree; the checks below say which is right.

## A. Gaps: what an author would still have to guess

### A1. Screws and threaded fasteners
- Checked: component names in all 20 inventories. No screw, bolt, standoff, servo, joystick, motor or tool exists.
- Nearest evidence is 8 fastener operations in the full builds: LSM nut off/on (Steps 16, 18; [034], [039]) and LAC knob, nut, washer off (Steps 22-24; [046], [052]) and on in reverse (Steps 26-28; [057], [059], [061]). Each is its own numbered step, shown in an isolated view, with one red arrow (off) or one axial red lead line (on).
- Thread spin is a token, not a number of turns, and is inconsistent: LAC nut spins 176 degrees while sliding off ([050]) and does not spin when refitted (Step 27c); LSM nut spins 180 degrees off ([035]) and 115 degrees on ([040]).
- No tool is ever drawn, no size is stated, no tightness cue exists. The only wording about tightness is in an abandoned LSM description ("until it is finger-tight").
- Fasteners have no tooltip name of their own: the LAC nut, washer and knob are not in the tooltip vocabulary (21 names, none for hardware).
- Rule conflict for the new kit: "every fastener gets its own step" (8 of 8) collides with "four or more identical drop-in parts: one exemplar, then do the rest" (3 of 4 groups). Four identical screws on one servo satisfy both. The data cannot settle it.

### A2. Servos, horns and other panel-mounted components with a captive lead
- Nearest evidence: push button (LSM), rocker switch, potentiometer, buzzer (LAC). They are mounted on a loose panel in an isolated view, the component moves and the panel fades in seated (5 of 5), leads ride rigidly with the body.
- Setting a rotary position has one precedent: LAC Step 29 ([063] to [064]). Face-on view of the knob, an eye icon on it, and the knob turns 50 degrees in place on Step 29c. This is the only model for "centre the servo horn".
- The order rule "finish all wiring on the open base before any wall goes on" would leave every servo panel tethered for the whole mechanical build. In LAC the switch panel stays tethered for 34 steps and the pot panel for 29; each needed up to four pre-posed copies (F1-1, -2, -3, -4). An articulated arm multiplies that cost. No guide wires after the mechanical build, so there is no evidence for the alternative.

### A3. A multi-pin plug on a lead, and polarity
- No lead in any guide ends in a multi-pin housing. Rocker switch, pot and buzzer leads end in single-pin housings and get one step each (8 of 8), eye on the housing, one label.
- Wire colour is identity only for jumpers. A servo lead's colours carry function, so the "never use colour for function" rule cannot be applied to it as written.
- Polarity has one precedent: the LSM capacitor. Card with a photo marking "GND Strip", minus and plus ([012]); then on Step 6 an eye on the stripe beside the two hole labels and two lead lines ([013]).
- A rigid plug has two treatments: LSM and LAC show an eye on the socket and fade the plugged cable in (LAC [088]); PMG hovers the plug with one red lead line and tweens it 22.9 mm ([057]).

### A4. A finished sub-assembly moved as a unit
- Tween scan of the three full builds: the only groups of different items that ever move together are a bought-in component with its own leads or battery (RTC, rocker switch, pot, push button) and identical pairs. No student-built sub-assembly is tweened.
- Bench sub-assemblies are staged where they will be parked. Positions are bit-identical from the first bench frame to the pick-up: LAC F1 from [055] to [104], LAC F4 from [032] to [065], LSM D2 from [037] to [046]. Returning from the isolated view to the full scene needs no motion and no step. For F1 the bench view only re-declares the up-axis (-x) so the lying panel looks upright.
- Once wired, a sub-assembly is seated by cross-fade: 11 seat events. 7 use two numbered steps (re-pose with an eye, then attach); 4 use one step (LSM D2 with an arrow [046]; LAC buzzer with two eyes [094]; PMG button modules [073], [075]).
- Cue on the attach step: lead lines 6, arrow 2, eyes only 3.
- The pattern set does not say what to do with an untethered multi-part sub-assembly. The nearest rule is "anything pre-assembled moves as one rigid part".

### A5. First-step conventions
- After Start, 5 of 19 guides open with a section card, not a step: LAC Part 2 (Rocker Switch), LAC Part 3 (Alarm Buzzer), PMG Part 1 and Full Build (Nano I/O Module), PMG Part 2 (4-Digit Display).
- LSM and LAC Step 1 is a preparation step on the first part alone: peel the breadboard backing, red arrow plus an inset captioned "Protective Backing" ([001] in both). Step 2 hovers the breadboard over the base panel, which fades in seated.
- PMG Step 1 seats the Nano on the I/O module with 4 lead lines ([002]). The base panel never gets a step in any kit.
- The cut from the title hero to the first frame uses a step-level fade in 11 of 12 LSM and LAC build guides and in none of the 4 PMG build guides.
- A part guide starts with the earlier parts already on screen. There is no recap, no "you should have this" frame and no parts list.

### A6. Turning the work over
- 14 up-axis changes in the three full builds (LSM 5, LAC 7, PMG 2). 10 happen on a Step N, 1 on a card, 3 on an auto Transition (all LSM).
- None has a dedicated cue. The student sees the model the other way up (engraved IDs upside down, PMG [064] to [065]) and must infer that the kit has to be turned over.
- Every Start and every final view is at +y (19 of 19).

### A7. Cues that cannot be read
- 15 auto-advancing Transitions carry an annotation, all in PMG: 9 second-stage arrows in the take-apart and 3 lead-line pairs in the build (shown twice, Part 3 and Full Build; e.g. [106], [111], [114]). They are on screen for 0.8 s.
- 423 of 425 Step N frames carry at least one cue. The 2 bare ones are the PMG 9-wire ribbon step (Full [035], Part 2 [002]).

### A8. The eye icon carries several meanings
- Seen in renders: take this wire (PMG [007]); take this ribbon ([004]); look at this polarity mark (LSM [013]); turn this (LAC [063]); pick this up (PMG [099]); do the rest (LSM [085]); check this result (LSM [076], inside an inset).
- Two eyes on one frame occur 4 times. Twice they mean "this goes there" for a wired module (LAC Step 43 [094], PMG Step 33 [073]); once "release both" (LAC Step 44 [096]). The pattern set does not describe the pair.

### A9. Text and wording
- Step descriptions exist on 52 steps of the three oldest LSM guides, in the form "Step n - imperative sentence" with Title Case nouns ("Step 3 - Align Nano Board pin D12 with Breadboard Slot C16"), and "Make Sure ..." on a result frame. They are stale and contain typos. This is the only wording evidence.
- Cadasio's placeholder description is still published on 3 visible steps (LSM Part 4 [000], LSM Part 3+4 [000], LAC Electronics [001]).
- Text-to-speech of descriptions is switched off in 20 of 20 projects.
- Pictures do contain words: "Protective Backing" (LSM and LAC Step 1), "GND Strip", "GND", "VCC" (Capacitor card), "H9 3x" (PMG [085]), "NANO I/O MODULE LABELS". The wordless rule is true for labels only.
- Label fonts are split: Arial on 133 showings (LSM and LAC builds), project default Public Sans on 88 (PMG builds, LAC Deconstruction). Sizes: 3em on 175, 2.5em on 39 (LSM only), 6em on the 7 quantity-cue showings.
- Part IDs use one letter per kit: D (LSM), F (LAC), H (PMG). The rulebook does not say how the next letter is chosen.

### A10. The last view
- Named "Completed View" in 16 of 19, "Completed Build" in 2, misspelt in 1.
- It changes only the camera in 14 of 19. PMG Part 1 [033] and PMG Deconstruction [060] have no last Step Nc, so the final view performs the last change (6 and 293 solids) with the camera unchanged. Three LSM guides switch on 4 extra solids in the final view.
- No annotation on any final view (19 of 19).
- Take-aparts end on what cannot be undone: breadboard stuck to the base (LSM [068], LAC [129]) or the bare I/O module (PMG [060]).

### A11. Title page
- Layout confirmed on 19 of 19. Logo 33-40 % of width at x 2 %, y 4-8 %; title block 42-58 % of width at x 2 %, y 61-65 %.
- Subtitles in use: "Part n", "Part 1 + 2", "Part 3 + 4", "Full Build", "Deconstruction". The copyright line is baked into the image and reads 2025 on LSM and LAC, 2026 on PMG.
- The hero is staged separately and is not always the final state: the LAC Full Build hero shows the potentiometer washer, which the final view lacks, and omits the F9 bracket; the PMG Full Build hero omits 6 solids of the USB cable that the final view shows.
- The layout breaks when the frame shape changes: in PMG Deconstruction [000] (2.63:1) the title overlaps the model.

### A12. Identical repeated parts
- Sets found: 2 (pairs, 4 steps), 4 posts (split 2 + 2), 4 keys (1 + 3), 4 button modules (1 + 3 by cross-fade), 64 stems (1 + 63). No set of 3.
- The quantity cue has three forms: "2x" in blue `#0074d9` (LAC [008]), "64x" or "64X" in cyan on a card (LSM [082]), "3x" inside a picture (PMG [085]).
- Identical modules are wired in full every time (4 PMG button modules, 12 wire steps); only the next module's arrival is automated.

### A13. Showing what is hard to see
- Used: camera re-aim, up-axis flip, eye on the spot, framed close-up (21 result frames carry one new check picture or eye), 50 % ghosting once (LSM Step 34 [075], 5 solids).
- Never used: section cut (21 stored settings, 0 enabled), exploded view, hiding a built part to expose what is behind it (wood parts leave the screen only at scene switches or pose swaps).
- No rule says which device to pick.

### A14. Accessibility for young students
- Contrast against white: cyan callout furniture `#7fdbff` 1.56:1; red `#ff0000` 4.0:1. Red on wood `#deb887` 2.15:1; cyan over wood 1.19:1; red on the blue shield 1.86:1.
- Sizing uses three units: text labels and line widths in fixed pixels (60 px type in a 175 x 90 px box, 5 px lines), images in percent of width, arrows in model millimetres. At the projects' own embed size of 560 x 315 a label box would be 31 % of the width.
- Which jumper to pick is conveyed by colour alone. Loose and routed models differ in colour on 5 of 103 pairs.
- Presses of Next: 81, 120 and 108 for the full builds; 11 to 53 for a part guide.
- Part names need a hover, which a touch screen does not have.
- No warning symbol, no adult-help cue, no test step anywhere.

### A15. Power and testing
- The USB cable is plugged into the Nano at Step 20 of 38 (LSM), 40 of 57 (LAC), 25 of 51 (PMG) and stays attached for the rest of the build.
- No take-apart starts by unplugging it: it comes off at Step 20 of 24, 25 of 47 and 19 of 23.
- No guide has a power-on, upload or function-check step.

### A16. Continuity of pose copies
- LAC: the washer fitted in Step 26 disappears at Step 30 [065] and never returns; the nut is missing from the copies shown from Step 47c to Step 54 ([105] to [121]).
- The rulebook has no rule that every copy of a sub-assembly must contain the same parts.

### A17. Player settings not in the rulebook
- Identical in 20 of 20: view cube shown, auto start, navigation overlay along the bottom, backward steps animated, interaction prompt off, tooltips on, embed 560 x 315.
- `startStepId` is unreliable: it points at a mid-guide step in 3 guides (LSM Deconstruction "Step 3", LSM Part 2 "Step 10", LSM Part 1+2 "Step 11") and is null in 9.
- Camera animation is stored as `animate_orbit: false` on 1105 of 1105 steps; the data do not show what path a 90 degree re-aim takes.

## B. Contradictions between dimensions

| # | Between | Check | Right |
|---|---|---|---|
| 1 | Structure note (leaf-level visibility flags) vs Style note (nearest explicit flag wins) | The two rules agree on 16 guides and differ on 17 frames in 3 guides. LAC Part 2 [000] shows panel F4 with the switch; only the leaf-flag rule shows it. | Leaf-level flags |
| 2 | GRAN-4 (sets of 4, 4, 64) vs MECH-3 (3 keys, 63 stems) vs MOT-14 (sets of 2-4 are tweened in pairs) | Sets are 64 stems, 4 keys, 4 button modules; MECH-3 quotes the remainders. The 4 keys are batched, the 4 posts are not. | GRAN-4; a set of 4 goes either way |
| 3 | STR-4, CAM-1, DEC-4, DEC-18 ("never" move the camera inside a pair) | Step Nc 424 of 424 hold. Transitions inside a pair 98 of 100; PMG Deconstruction [007] and [012] re-aim by 96 and 83 degrees. | The rule; 2 exceptions |
| 4 | STR-3 (one-frame cues on paused frames, clean result) vs LL-1, LL-8, DEC-2, DEC-7 (PMG cues on Transitions) | 15 Transition frames carry cues, all PMG. 26 of 424 result frames carry something: 21 new check cues, 2 carried "2x" labels, 2 carried lead-line pairs, 1 misnamed frame. | STR-3 as the rule |
| 5 | MOT-9 (never animate a wire into its connection) vs WIRE-15 (PMG USB plug tweens in) | Jumpers and captive leads 103 of 103 by swap. PMG USB plug tweens with a lead line. | Both; a rigid plug is a part |
| 6 | MECH-7 (do not rotate the model) vs MOT note and CAM-16 (turn the model over) | 39 up-axis changes, no part transform. On screen the model is the other way up. | MECH-7 for mechanism |
| 7 | STYLE-7 (viewed from underneath) vs CAM-16 (never below the horizon) | LSM Step 34 [075] has up-axis -y. | CAM-16 |
| 8 | STYLE-11 (one label style) vs WIRE-6 and DEC-11 (two fonts, two sizes) | Arial 133, default 88; 3em 175, 2.5em 39. | WIRE-6 |
| 9 | STR-1, STR-14 (final view: one name, camera only) | See A10. | Holds in 14 of 19 |
| 10 | GRAN-8, MECH-5 (each fastener its own step) vs GRAN-4 (batch four or more) | No screws in the data. | Undecided |
| 11 | GRAN-10 (6-7 of 10) vs MECH-6 (7 of 13) vs LL-1 (11 seats) | 11 seat events; 7 in two steps, 4 in one. | 7 of 11 |
| 12 | MECH-1 (28 wood kinds) vs MECH-4, MECH-8 (34) | 34 kinds; 6 never tween in (D1, D2, F1, F3, F4, H1). | 13 of 28 tweened kinds are two-motion |
| 13 | WIRE-12 (every module named on a label has a card) vs STR-12 (Nano never has one) | LSM Step 3 label "Pin d12" names a Nano pin. | STR-12; one exception to WIRE-12 |
| 14 | NEV-1, LBL-2 (no words) vs pictures | See A9. | True for labels only |
| 15 | ORD-3, WIRE-10 (colour never means function) vs Capacitor card | Card uses red plus and black minus. | True for jumpers only |
| 16 | Rule IDs | DEC-1 to DEC-3 exist twice with different content (granularity and deconstruction). | Rename before use |

## C. Rules that matter most, in priority order

1. Skeleton: Start, optional section cards, numbered pairs, Completed View. Step N shows the cue and waits; Step Nc shows the result from the same camera and waits. Number 1..N per guide.
2. One kit item per numbered step. An identical pair may share a step. Batch only label-free drop-ins of four or more after one worked example.
3. Every Step N carries at least one cue, on a paused frame, for one frame only. Step Nc is clean except one optional check picture or eye.
4. Cue grammar: red lead lines for a part going on (1, 2 or 4, tab to slot, along the travel); one red arrow for a part coming off, flexed or carried; never both. Eye icon for wires, pick-ups and checks.
5. A rigid part fades in stationary at its hover pose, in final orientation, back along its insertion path and above or beside its seat on screen. It seats with one straight 800 ms move. No rotation except swing, lean, thread spin or a dial.
6. A second motion is its own numbered step with fresh lead lines, or an auto Transition with no new cue. The camera never moves inside a step.
7. Never tween anything whose wires are already plugged in. Cross-fade between pre-posed copies: re-pose with an eye, then attach with lead lines. Every copy holds the same parts.
8. Build a bench sub-assembly at the pose where it will lie parked, in an isolated view. Returning to the full scene needs no motion and no step.
9. One wire per step by model swap from a straight loose wire to the routed wire. Eye on the wire, one label per end, two labels at most, no lines or arrows. Park the loose wire at one spot per run.
10. Label text is only the identifier printed on the hardware. Part names live in tooltips ("Role - Part ID") and engraved IDs.
11. Preparation and fastener work get their own numbered steps in an isolated view, directly before first use. No close-up while the assembly is on screen.
12. A section card precedes any component with pins, polarity or a count to identify: the component alone, at most one eye and one framed photo with a red box.
13. Camera: set only on Start, cards, Step N and the final view. Three-quarter view from above (about 34 degrees), travel at least 40 degrees off the line of sight, 45 degree lens, hovering part and destination both in frame.
14. Hold one camera through a wiring run. Re-aim for most mechanical steps.
15. Electronics first on the open base, one module at a time, pins in physical order, USB last. Panel-mounted parts go on their loose panel first. Enclosure by dependency, cover last.
16. For underside work re-declare the up-axis and keep viewing from above. Group it in one block and return to +y before the final view.
17. Look: white background, flat two-tone toon shading, thin black edges, no shadows. Wood `#deb887` with engraved IDs `#1e1616`. Never tint or highlight a part. Ghost at 50 % only to check something covered.
18. Annotation colours: red `#ff0000` for motion, cyan `#7fdbff` for pointing, black for text and the eye. Bold sans label over a cyan rule with a straight leader and dashed ring.
19. Everything animates in 800 ms: fade for show and hide, tween for moves and camera, backward too. Auto Transitions are hidden from the step picker.
20. Title page: logo top-left, three-line title block bottom-left, finished model on the right, nothing else. Final view: clean three-quarter hero, no annotations.
21. Part guides are contiguous slices of the full build cut at pair boundaries, renumbered from 1, 5 to 26 steps each, with their own Start and final view.
22. Take-apart: same skeleton, no cards. Red arrow on the still-seated part, removal plays through, part gone on Step Nc. Reverse order by access, coarser than the build, stop at what cannot be undone.
23. Confirm a hidden or tiny result with a framed close-up carrying a red box on Step Nc.
24. Decide before authoring, because the data are silent: screws and tools, servo order and plug orientation, a turn-over cue, a second cue for wire identity, minimum contrast and size.
