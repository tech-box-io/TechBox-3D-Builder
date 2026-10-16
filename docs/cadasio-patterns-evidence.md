# TechBox build-guide rulebook: evidence

Every rule extracted from the 20 published Cadasio guides, with the numbers behind it, its exceptions, and the verdict of an independent
re-check against the data. The short version is in [cadasio-patterns.md](cadasio-patterns.md). Step references like `[057]` are the
index of a step view within its guide; guide names are abbreviated (LSM, LAC, PMG; F = Full Build, P = Part, D = Deconstruction).

**Verdicts.** *confirmed*: held as stated. *qualified*: true once narrowed; the rule is shown as corrected, with the counter-examples.
*refuted*: not supported; listed so nobody re-derives it. *not re-checked*: the second pass did not report on it.

## Contents

- [Guide structure, step naming and numbering](#guide-structure-step-naming-and-numbering): 20 rules (16 confirmed, 4 qualified)
- [Step granularity and build ordering](#step-granularity-and-build-ordering): 22 rules (11 confirmed, 11 qualified)
- [Part motion, hover offsets and seating](#part-motion-hover-offsets-and-seating): 19 rules (9 confirmed, 10 qualified)
- [Red lead lines and 3D arrows](#red-lead-lines-and-3d-arrows): 18 rules (8 confirmed, 10 qualified)
- [Labels, eye icon, image callouts and section cards](#labels-eye-icon-image-callouts-and-section-cards): 22 rules (14 confirmed, 8 qualified)
- [Camera, framing and transitions](#camera-framing-and-transitions): 21 rules (8 confirmed, 13 qualified)
- [Visual style and the part colour library](#visual-style-and-the-part-colour-library): 15 rules (7 confirmed, 8 qualified)
- [Electronics and wiring conventions](#electronics-and-wiring-conventions): 19 rules (15 confirmed, 4 qualified)
- [Mechanical (wood, fasteners, enclosure) assembly conventions](#mechanical-wood-fasteners-enclosure-assembly-conventions): 12 rules (4 confirmed, 8 qualified)
- [Deconstruction (take-apart) guides](#deconstruction-take-apart-guides): 21 rules (11 confirmed, 10 qualified)

**Totals:** 189 rules; 103 confirmed, 86 qualified, 0 refuted.

## Guide structure, step naming and numbering

### STR-1 · confirmed

**Open every guide with one title step named 'Start', close it with one final view named 'Completed View', and put only three things in between: named section cards, numbered step pairs ('Step N' ... 'Step Nc') and auto-advancing 'Transition' steps.**

- Applies to: all: construction and deconstruction, all three kits (LSM, LAC, PMG); part guides, combined guides and full builds alike. Not the LAC Electronics parts overview.
- Evidence: 1037 viewer steps in 20 guides = 19 Start + 33 named cards + 425 Step N + 424 Step Nc + 117 Transition + 19 final. The kind sequence matches 'Start (card / Transition / Step N Transition* Step Nc)* Final' exactly in 16 of 20 guides. Final step is named 'Completed View' in 16 of 19. Part guides: 5-26 numbered steps (median 13), 13-59 viewer steps (median 31). Viewer steps per numbered step 2.24-2.62 (build), 2.65-2.88 (deconstruction).
- Exceptions: Grammar fails only through naming slips: LAC Deconstruction (duplicate 'Step 41' [104]; 'Step 45c' used for the Step 45 frame [120]); PMG Part 1 has no 'Step 14c' (Completed View [033] does its job); PMG Deconstruction has no 'Step 23c'. LAC Electronics has no Start or final. Final is named 'Completed Build' in LSM Part 2 [030] and LSM Part 1+2 [046], and misspelt 'Copmleted View' in LSM Part 3+4 [042].
- Why it helps students: Every guide in a classroom opens and closes the same way, so a student always knows where they are: a cover showing the goal, a run of numbered actions, then a clean view to compare their build against.
- For our player: Model a guide as an ordered list of typed steps: title, card, instruct, transition, result, completed. Validate the grammar at authoring time (exactly one title first, one completed last, every instruct followed by its result) so the naming slips seen in the corpus cannot be published.

### STR-2 · confirmed

**Author each student action as a pair of frames that both wait for the student: 'Step N' shows what is about to happen (new part at its hover pose, or a cue on the existing scene); 'Step Nc' (lower-case c = completed) shows the same scene after it has happened.**

- Applies to: all: construction, deconstruction, wiring, mechanical; all kits
- Evidence: 421 of 425 Step N are followed, after 0-3 Transitions, by the Step Nc of the same number (334 adjacent, 76 with one Transition, 9 with two, 2 with three). Build guides, Step N (331): new part fades in 173, scene/pose swap 34, part moves 40, fade-out only 2, model unchanged and only annotations appear 82 (25%). Build guides, Step Nc (330): model changes on 330 of 330 (154 tweened moves, 156 cross-fade swaps, 20 plain appear/disappear). Deconstruction: Step N leaves the model untouched on 67 of 94; Step Nc removes or swaps on 93 of 94.
- Exceptions: 4 broken pairs, all naming faults: LSM Part 4 [016] 'Step 8' completed by [017] 'Step 9c'; LAC Deconstruction [104] 'Step 41' is a dead duplicate of [105] 'Step 40'; PMG Part 1 [032] 'Step 14' and PMG Deconstruction [059] 'Step 23' run straight into Completed View. Capital suffix twice: 'Step 20C' (LSM Part 1+2 [042]), 'Step 14C' (LAC Part 1 [030]).
- Why it helps students: The student sees the instruction, does it, then presses Next and sees what it should now look like. Splitting 'do' from 'check' gives a natural self-check after every action without any text.
- For our player: Make the numbered step a first-class object holding an instruct state and a result state (plus optional in-between keyframes). Generate the 'Step N' / 'Step Nc' labels from that object; never let authors type them.

### STR-3 · confirmed

**Give every annotation a life of exactly one frame: on in one viewer step, off in the next. Put at least one annotation on every Step N. Leave Step Nc clean, except for an optional single 'check your work' callout (inset close-up or eye icon) that is new on that frame.**

- Applies to: all step kinds, all kits; the Nc check callout occurs in construction guides only
- Evidence: 1012 of 1019 annotation showings (99.3%) last exactly one viewer step. Step N annotated: 423 of 425. Step Nc with no annotation: 398 of 424 (94%); of the 26 others, 21 carry one new check callout (9 of 146 Step Nc in the three full builds). Start: exactly 2 annotations, 19 of 19. Final view: 0 annotations, 19 of 19. Transitions annotated: 15 of 117, all PMG.
- Exceptions: 7 showings last two steps, all faults: '2x' label on Step 4 and 4c (LAC Part 1 / LAC Full [008]-[009]); 4 lead lines left on at PMG Part 3 [057] / PMG Full [115]; one eye icon across the duplicated LAC Deconstruction frames [104]-[105]. Only Step N with no annotation: the 9-wire ribbon prep, PMG Part 2 [002] = PMG Full [035]. PMG Transitions carry second-leg lead lines ([106] [111] [114]) or a second-stage arrow (9 of 14 in PMG Deconstruction).
- Why it helps students: Whatever is drawn on screen is always about the current action; nothing stale lingers. A clean result frame lets the student compare their real model with an unobstructed picture.
- For our player: Scope annotations to a single step state and clear them automatically on leaving it; do not offer a 'persist' option. Warn the author when an instruct state has no annotation. Allow at most one check callout on a result state.

### STR-4 · confirmed

**Change the camera only on entering Start, a card, a Step N or the final view. Never move it on Step Nc, and do not move it on a Transition inside a pair, so the result is seen from exactly the view in which the instruction was given.**

- Applies to: all, all kits
- Evidence: Step Nc: camera moves on 0 of 424. Transitions inside a pair: 2 of 101. View constant from Step N to Step Nc in 423 of 425 numbered steps. Step N: camera moves on 266 of 425 (63%; build 211 of 331, deconstruction 55 of 94), median rotation 62.5 deg (build) / 55.7 deg (deconstruction). Cards 31 of 33, Start 19 of 19, final 17 of 19.
- Exceptions: PMG Deconstruction [007] and [012]: auto Transitions inside Steps 2 and 3 that swing the camera 96 and 83 degrees. Camera-only Transitions between pairs are covered in STR-8.
- Why it helps students: Before and after are directly comparable because the viewpoint does not jump; the only thing that changes between the two frames is the part the student just handled.
- For our player: Store a camera keyframe on the instruct state (optional) and on title/card/completed; the result state and in-step keyframes inherit it and expose no camera control in the editor.

### STR-5 · confirmed

**Number steps 1..N per published guide with no gaps. Give a number to every student action, including preparation and check actions; give none to Start, cards, Transitions or the final view. Restart at 1 in each part guide; run one continuous sequence through a full build.**

- Applies to: all, all kits
- Evidence: First numbered step is 'Step 1' in 19 of 19 guides; contiguous 1..N in 17 of 19. All 11 part guides and both combined guides restart at 1. Offsets in full builds equal the numbered-step count of the preceding parts: LAC +14 / +32 / +40; PMG +14 / +25; LSM +8 / +21 / +26. Project setting stepPrefix = 'Step' in 20 of 20.
- Exceptions: LSM Part 4 skips from 'Step 8' to 'Step 9c' and so shows 1..13 for 12 real steps. LAC Deconstruction has a duplicate 'Step 41' and no 'Step 45'. Step names are typed by hand on top of Cadasio's project-wide counter, so every numbering fault is a typing fault.
- Why it helps students: A teacher can say 'everyone stop at Step 9' and it means the same thing on every screen; cards and automatic animations do not shift the count.
- For our player: Compute step numbers at render time from position and a per-guide offset. A part guide is the master sequence sliced with offset reset to 0; a full build uses the same data with no reset.

### STR-6 · confirmed

**Make Start, cards, Step N, Step Nc and the final view wait for the student (pause). Make Transition auto-advance (play), so one press of Next carries the student from Step N through any Transitions to Step Nc.**

- Applies to: all, all kits
- Evidence: Non-Transition steps: pause on 920 of 920. Transitions: play on 115 of 117. Popups/checklists/buttons: 0 of 1037. Auto-advancing frames are 0-14% of a build guide and 23-28% of a deconstruction.
- Exceptions: Two Transitions wait for a click: LAC Deconstruction [033] (changes nothing) and [118] (RTC lift). Both look like faults.
- Why it helps students: The student sets the pace at every point where they must read or act, and is never asked to click through a frame that is only an animation waypoint.
- For our player: Next advances to the next pausing state, playing any in-step keyframes in sequence. Back should return to the previous pausing state. No dwell timers or auto-play of numbered steps.

### STR-7 · confirmed

**When one student action needs more than two keyframes, insert auto-advancing Transition frames between Step N and Step Nc instead of giving the intermediate state its own number. Use them for (1) a removal: arrow on Step N, part slides off in the Transition, part fades out on Step Nc; (2) the middle leg of a multi-leg seat; (3) an intermediate pose when a wired module is cross-faded through several poses.**

- Applies to: all; rare in construction (9% of numbered steps), standard in deconstruction (60%). All kits.
- Evidence: 101 of 117 Transitions sit inside a pair: 68 part moves, 27 model swaps, 4 that only clear cues, 2 camera moves. Build guides: 31 of 331 numbered steps contain one (27 with one, 4 with two); three full builds 15 of 146. Deconstructions: 56 of 94 (LSM 19 of 24, LAC 27 of 47, PMG 10 of 23). Maximum 3 Transitions in one numbered step.
- Exceptions: When the two stages need different viewpoints the kits use two numbered steps instead (e.g. LSM D3 Steps 24/25, PMG H5 Steps 29/30). Transitions that do nothing visible: LSM Deconstruction [011], LAC Part 4 [027] = LAC Full [116], LAC Deconstruction [033].
- Why it helps students: The student sees a slide-then-drop or pull-then-vanish as one continuous motion after one click, and the step count still matches the number of things they physically do.
- For our player: Allow a numbered step to hold an ordered list of 0-3 intermediate keyframes between instruct and result, each with its own part poses and visibility; play them back to back on one Next press.

### STR-8 · confirmed

**Use a Transition between a Step Nc and the next Step N only for something the student does not do and should not click for: a large camera re-orientation with a flip of the scene up-axis, or a not-yet-wired module fading in. Treat this as optional; most camera flips are done directly on Step N.**

- Applies to: construction; camera flips are an LSM habit, module fade-ins a PMG habit
- Evidence: 16 of 117 Transitions sit between pairs: 10 camera-only (8 LSM, each with an up-axis change, rotations 53-143 deg; 2 are one LAC step, 13 deg) and 6 part fade-ins (one PMG idiom seen twice). Of 39 up-axis changes in the corpus only 8 use a Transition; 28 happen directly on a Step N (LSM 6, LAC 16, PMG 6). Only 12 of 117 Transitions move the camera at all.
- Exceptions: Not a rule: LAC and PMG flip the up-axis on Step N with no Transition every time. The README's description of Transition as a camera step fits only 12 of 117.
- Why it helps students: A big turn of the model is shown as its own smooth move before the next instruction appears, so the student is not reading new lead lines while the view is still swinging.
- For our player: Support an optional auto-advancing bridge keyframe between two numbered steps, but do not require it for camera flips; default to moving the camera on the instruct state.

### STR-9 · confirmed

**Hide every Transition from the step picker and hide the navigation overlay while it plays, so the student neither sees it listed as a step nor can stop on it.**

- Applies to: all Transitions, all kits
- Evidence: hideInStepPicker true on 108 of 117 Transitions and 0 of 920 other steps. overlayVisible false on 110 of 117 Transitions and 0 of 920 other steps. Name spelt 'Transition' on 113 of 117.
- Exceptions: Visible in the picker: LSM Deconstruction [044] [052] [066]; LAC Part 4 [028] (its twin LAC Full [117] is hidden); LAC Deconstruction [033] [118]; PMG Part 3 [056] = PMG Full [114]; PMG Deconstruction [026]. Overlay left on: LSM Deconstruction [044] [066]; LAC Deconstruction [033] [118]; PMG Part 3 [056] = PMG Full [114]; PMG Deconstruction [026]. Misspelt names: 'Transiton' (LSM Deconstruction [038]), 'Ttansition' (LAC Part 2 [023], LAC Full [053]), 'Transititon' (LAC Deconstruction [002]).
- Why it helps students: The step list shows only places where the student does something, and they cannot get stranded on a half-finished motion.
- For our player: Intermediate keyframes have no name, no picker entry and no navigation controls; these are properties of the type, not per-step flags an author can forget.

### STR-10 · confirmed

**Animate every step change over 800 ms: fade parts and annotations in and out, tween part moves and camera moves, no camera orbit animation. Animate backward navigation too.**

- Applies to: all, all kits
- Evidence: 800 ms on 1030 of 1037 viewer steps. CAD options show=fade, hide=fade, move=tween on 1037 of 1037. Camera move=tween, animate_orbit=false, speed 2 on 1037 of 1037. 2D annotations fade/fade/tween on 1037 of 1037. Project flags identical in 20 of 20: autoStart, animateStepsViewer, animatePreviousStep all true; overlay horizontal_bottom; repeatCount 0; perspective camera, FOV 45.
- Exceptions: 7 steps at 1600 ms: nut unscrewing/screwing in LSM (LSM Part 2 [017] [022]; LSM Part 1+2 [033] [038]; LSM Full [035]) and two LCD pose swaps in LAC Deconstruction [016] [017]. LSM Full uses 800 ms for the same nut-on step ([040]), and LAC's nut steps use 800 ms, so the 'double time for threaded spin' exception is not applied consistently.
- Why it helps students: One steady rhythm across every guide; fast enough not to bore, slow enough to follow where a part came from and went to.
- For our player: One global timing constant (800 ms) and one easing scheme, not per-step settings. A click on a step with k in-between keyframes plays (k+1) x 800 ms. Optionally support a 2x duration flag for spin moves.

### STR-11 · qualified

**Leave the step-level page transition at 'none' and let per-part fades carry scene changes. A whole-frame 'fade' is an optional older LSM/LAC habit, used almost only for cuts between the assembly and an isolated part (or back); it appears in LSM and LAC build guides and 4 times in LSM Deconstruction, never in LAC Deconstruction or any PMG guide.**

- Applies to: construction; LSM and LAC only
- Evidence: 'fade' on 65 of 1037 steps (44 Step N, 17 cards, 4 Step Nc; never on Transition, Start or final). 48 of the 65 replace more than half the visible model, but 80 comparable whole-scene swaps use 'none'. By kit: LSM 36, LAC 29, PMG 0 of 298.
- Exceptions: Applied to 17 steps that are not scene swaps (e.g. LSM Full [046], LAC Part 1 [004], LAC Part 2 [025]). The newest kit (PMG) never uses it.
- Narrowed because: (1) Not construction-only: LSM Deconstruction [001] Step 1, [027] Step 9c, [037] Step 14, [047] Step 17c carry 'fade'. (2) The scene-swap link is stronger than reported: 55-57 of the 65 fades (not 48) replace more than half the visible model; 8-10 (not 17) do not: LSM Part 3 [001], LSM Full [046], LSM Deconstruction [001] [027] [047], LAC Part 1 [004], LAC Part 2 [025], LAC Part 4 [001], LAC Full [004] [055]. In LSM Full 12 of 13 and in LAC Full 11 of 13 fades are assembly/isolated-part cuts. (3) Still unsystematic: 85-110 comparable whole-scene swaps use 'none' (LAC Full: 11 with fade, 10 without). (4) The two steps with no value are the Start of LSM Part 4 and LSM Part 3+4, the same two that keep Cadasio's placeholder description.
- As first stated: Leave the step-level page transition at 'none' and let per-part fades carry scene changes. A whole-frame 'fade' is an optional older habit for cuts between the assembly and an isolated part.
- Why it helps students: Minor: a cut to an isolated part reads as a scene change rather than as parts flying about.
- For our player: Not needed as a feature. If scene cuts are wanted, apply one rule automatically (e.g. cross-fade when more than half the visible parts change) rather than a per-step switch.

### STR-12 · qualified

**Before the first numbered step that uses certain new components - mainly wired modules whose pins or orientation the student must identify - insert one un-numbered step named after the component in Title Case. Show the component alone, close up, with at most two annotations (typically a framed photo of the real part with its pins boxed, or an eye icon). The card waits for the student, has no 'c' twin and asks for no action. This is usual, not universal: the Arduino Nano and the breadboard never get a card, and coverage has grown by kit (LSM 2 part cards + 1 pin diagram for 7 bought-in component types, LAC 5 for 9, PMG 5 for 6).**

- Applies to: construction, electronics/wiring sections; all three kits. Not used for wooden panels or in deconstruction.
- Evidence: 31 card steps in 13 guides = 14 distinct cards. Followed by a Step N 31 of 31; preceded by a Step Nc 26 times and by Start 5 times. Pause / 800 ms / visible in picker 31 of 31. Camera moves on entry 29 of 31 and again on the next step 30 of 31. Content of the 14: photo or diagram inset 6, eye icon only 3, nothing 3, quantity label 1, full-frame 2D diagram 1. Annotations per card: 0 on 6, 1 on 23, 2 on 2. About 1 card per 10 numbered steps in full builds (14 per 146). 0 cards in LAC Steps 41-57, PMG Steps 26-51 and all 260 deconstruction steps.
- Exceptions: The card name is never drawn on the canvas; it exists only as the step name. Components whose first appearance is itself a numbered prep step get no card (resistors, jumper ribbons, potentiometer). 'LED Matrix Diagram' shows no 3D part. The 'Capacitor' card exists in LSM Part 1 and LSM Full (render dated 2026-09-22, the latest edit in the corpus) but not in LSM Part 1+2.
- Narrowed because: Bought-in components with no card and no prep step: Arduino Nano in all three kits (seated directly at LSM Full [006], LAC Full [006], PMG Full [002]); LSM push button (first at LSM Full [034] Step 16). Also without a card: breadboard (LSM, LAC), resistors (LSM, LAC), LAC potentiometer with knob/nut/washer ([046]); the LSM 8x8 LED matrix has only the 2D 'LED Matrix Diagram' ([027]). A card for a non-electronic part: 'LED Stems' (64 acrylic stems, LSM Full [082], in the enclosure section). Name on canvas: the 'Nano I/O Module' inset carries the caption 'NANO I/O MODULE LABELS' (PMG Part 1 [001]), so 'the card name is never drawn' is not quite true. 'Capacitor' card present in LSM Part 1 [011] and LSM Full [012], absent from LSM Part 1+2.
- As first stated: Before the first numbered step that uses a new bought-in component, insert one un-numbered step named after the component in Title Case. Show the component alone, close up, with at most two annotations (typically a framed photo of the real part with its pins boxed, or an eye icon). The card waits for the student, has no 'c' twin and asks for no action.
- Why it helps students: The student finds the right component in the kit and learns its pin names before being asked to connect anything to it.
- For our player: Provide a card step type with a required title that the player displays itself (the corpus relies on viewer chrome for it), an isolate-part mode, and slots for one photo inset and one pointer icon. Cards must not affect step numbering.

### STR-13 · confirmed

**Build the title page from two unanchored 2D images on the left and a 3D hero on the right: TechBox logo top-left; a three-line title block bottom-left (kit name with acronym in brackets / guide variant / copyright line); the finished model filling the right half. Nothing else on the page.**

- Applies to: all guides with a title page (19 of 20), all kits
- Evidence: Exactly 2 image annotations, no frame/leader/anchor, removed on the next step: 19 of 19. Same logo SVG in 19 of 19, stored x 1.8-2.5% (18 of 19), y 4.0-8.1%, width 33.2-39.5% of viewport width, height 0.27 x width. Title PNG stored x 1.6-2.5%, y 61.0-64.6%, width 42.1-48.4%, height 0.19-0.29 x width (17 of 19). On nine clean ~2:1 renders: logo spans x 2-41%, y 5-28%; title block x 2-46%, y 62-84%; model box x 48-54% to 88-95%, y 13-15% to 74-83%. Hero = most complete state: Start's visible solids overlap the final view by >=95% in 16 of 16 build guides; deconstructions show the fully built kit. The next step always moves the camera (19 of 19, 8-110 deg). Start elevation 21-47 deg, median 35.
- Exceptions: LSM Part 1's title image is a taller PNG stored at y 24%, width 58% (renders in the usual place). PMG Deconstruction's images are shifted right (x 5.1% / 3.8%) and the title overlaps the model in its saved 2.63:1 render. Cadasio placeholder description left on Start in LSM Part 4 and LSM Part 3+4. 'Stem' rather than 'STEM' on all 8 LSM title blocks; copyright year is baked into the image.
- Why it helps students: The cover tells the student which kit and which part they have opened and shows what they are about to build (or take apart) before any instruction appears.
- For our player: Make the title page a template with data slots (kit name, acronym, variant, year) rendered as live text over a fixed layout, plus an automatic hero of the guide's end state. Reserve the left ~45% of the frame for the two blocks and reflow for narrow viewports so text never overlaps the model.

### STR-14 · confirmed

**After the last Step Nc add one pausing step that changes only the camera: orbit to a clean three-quarter hero view of the result, close to the title-page direction, with no annotations.**

- Applies to: all, all kits
- Evidence: 0 annotations on 19 of 19. Camera moves on 17 of 19 (4.9-120 deg, median 66). Build guides: final view direction within 23 deg of Start in 14 of 16 (median 13 deg); final elevation 21-48 deg, median 38; distance vs Start x1.00 in 9, x0.86 in 3, x0.63 in 3, x1.17 in 1 (whole clicks of the 1.166 zoom ladder). Model unchanged from the last Step Nc in 10 of 16 build guides.
- Exceptions: PMG Part 1 [033] and PMG Deconstruction [060] have no camera move and perform the last step's result themselves (a Step Nc renamed). LAC Part 4 / LAC Full final view is 76 deg from the title direction. Small unannounced model changes on the final step in LSM Part 4 / Part 3+4 / Full and PMG Part 3 / Full. In deconstructions the step keeps the name 'Completed View' although it shows the leftover base.
- Why it helps students: A final unobstructed picture of the whole model from the familiar cover angle is the reference the student holds their finished build up against.
- For our player: Generate the completed step automatically: last result state, annotations cleared, camera tweened to the title-page hero pose (or one zoom click closer). Do not let it carry model changes.

### STR-15 · qualified

**For LAC and PMG (7 of the 11 part guides): author the kit once as a full build, then produce each part guide by cloning it and keeping a contiguous run of the sequence cut at a pair boundary, renumbered from 1, with a part-specific Start (hero = that part's finished state, subtitle 'Part n') and a part-specific final view. LSM was built the other way round (combined guides first, parts cut from them, full build assembled last on a different CAD model for the Part 1/2 region) and its Part 2 is not a contiguous run of the full build.**

- Applies to: construction part guides, all kits
- Evidence: LAC: 130 of 130 non-title steps of the full build have a twin in a part with identical camera (distance/elevation/azimuth), annotation counts, behaviour and duration. PMG: 114 of 115. Same CAD id and identical annotation inventory within each kit (LAC 150 objects, PMG 133). Parts: LAC 14/18/8/17 numbered steps, PMG 14/11/26, LSM 8/13/5/12; the last part of every kit is the enclosure. Cuts never fall inside a pair; 4 of 11 parts open with a section card directly after Start.
- Exceptions: LSM history differs: combined guides were made first (2025-07-17, 2025-08-04), parts cut from them (2025-08-22), then the full build re-shot (only 23 of 83 matched steps keep camera and annotation counts). PMG '4-Digit Display' card camera differs between Part 2 and Full. Cut leftovers stay in the files as hidden steps (68 across 17 guides).
- Narrowed because: LSM: only 23 full-build steps match a part on camera and annotation counts, all in the Part 3/4 region; nothing in LSM Full [001]-[047] matches Part 1, Part 2 or Part 1+2, and those three guides use a different CAD model (cadId 1baeed31 against 4114fb73). LSM Part 2 Steps 12 and 13 are the full build's Steps 21 and 20. PMG mismatch: '4-Digit Display' card, Full [034] elevation 11.5 / azimuth -75.3 against Part 2 [001] 2.8 / -91.2. Wording: 'cut leftovers stay as hidden steps (68 across 17 guides)' overstates - 15 of the 68 are the base-state keyframe, the four LAC parts have no other hidden step, and the largest count (18) is in PMG Full, the master. No step id is shared between any full build and its parts (0 in all three kits), so the lineage shows only in content, dates, cadId and inventory.
- As first stated: Author the kit once as a full build. Produce each part guide by cutting a contiguous run of that sequence at a pair boundary, renumbering from 1, and adding a part-specific Start (hero = that part's finished state, subtitle 'Part n') and a part-specific final view.
- Why it helps students: A class can do one phase per session and each session's guide has its own cover and its own finished picture, while the steps are exactly those of the full build.
- For our player: Keep one master sequence per kit with part-boundary markers; generate part guides (title, slice, completed, renumber) at publish time instead of cloning projects. This removes the drift and leftovers seen in the corpus.

### STR-16 · confirmed

**For a full or combined guide keep one Start (the last part's hero with the subtitle swapped) and one final view (the last part's). Drop every other Start and final view. Insert nothing at the seams - no divider, no 'Part n' card, no recap. Keep every section card and renumber continuously.**

- Applies to: full builds (all kits) and LSM combined guides
- Evidence: LAC Full 131 = 137 - 6 bookends. PMG Full 117 = 120 - 3. LSM Full 88 = 92 - 6 + 2 Transitions. LSM Part 1+2 47 = 50 - 3. LSM Part 3+4 43 = 42 - 2 + 3. Kept Start has the last part's camera in 4 of 5 (LSM Full pulls back one zoom click, 321 -> 374 mm); kept final view has the last part's camera in 5 of 5. 8 of 10 seams are a plain step change; 2 have an auto Transition (the LSM Part 3/4 seam in both guides containing it).
- Exceptions: LSM only: the full build does the USB cable (Step 20) before the D2 panel (Step 21), the reverse of Part 2 and Part 1+2; its Part 1/2 region is re-shot; LSM Part 3+4 repeats the panel step already in Part 1+2; LSM Part 1+2 lacks the 'Capacitor' card. PMG Full keeps Part 1's 'Completed View' frame under the name 'Step 14c'. Combined guides exist only for LSM, the oldest kit.
- Why it helps students: The full build reads as one uninterrupted job; students who do it in one sitting are not shown intermediate covers.
- For our player: The full build is the master sequence itself. No seam logic is needed beyond the normal camera tween between consecutive steps.

### STR-17 · qualified

**Structure a take-apart guide exactly like a build guide (Start, numbered pairs from 1, final view named 'Completed View'), with no section cards and no text. For each removal use either three beats - Step N (cue), auto Transition (part slides away, or the plugged wire is swapped for its loose model), Step Nc (part gone) - or two beats without the Transition (cue, then fade-out). Three beats is the LSM habit (19 of 24); LAC uses it for 27 of 47; PMG, the newest kit, uses two beats more often (Transition in only 10 of 23).**

- Applies to: deconstruction, all three kits
- Evidence: 3 of 3: 1 Start, 0 cards, 0 descriptions, 1 'Completed View'. Numbered steps 24 / 47 / 23 against 38 / 57 / 51 in the build. Transition inside the pair in 56 of 94 numbered steps (60%) vs 9% in build guides. Start reuses the full build's title camera exactly in LSM and LAC and its hero in PMG; only the subtitle changes to 'Deconstruction'.
- Exceptions: 38 of 94 steps have no Transition (wire or module swaps, or the part stays on screen). The deconstructions hold most naming and flag faults: three of the four broken pairs, the duplicated 'Step 45c', both pause Transitions and 6 of the 9 picker-visible Transitions.
- Narrowed because: Share of numbered steps with a Transition: LSM 79 %, LAC 57 %, PMG 43 % (60 % only as a pooled figure). What the Transition does: slide-off then fade-out in 36 of 94 (LSM 17, LAC 13, PMG 6); wire/module swap then fade-out in 12 (all LAC, Steps 19-22 and 36-43); the literal pattern 'Step N unchanged, one moving Transition, fade-out' in 18 of 94 (LSM 7, LAC 8, PMG 3). Two-beat removals with no Transition: PMG Deconstruction Steps 5, 9, 15-22 and 23 (11 of 23), LAC Steps 23 and 31, LSM Step 20. Step-level 'fade' is used 4 times in LSM Deconstruction ([001] [027] [037] [047]). Faults concentrated here as the report says: 3 of the 4 broken pairs, both pause Transitions, 6 of the 9 picker-visible Transitions.
- As first stated: Structure a take-apart guide exactly like a build guide (Start, numbered pairs from 1, final view), omit section cards and text, and give each removal three beats: Step N (cue, model unchanged), auto Transition (part slides away), Step Nc (part gone).
- Why it helps students: Students already know how to drive the guide from the build; the extra automatic beat shows which way a part comes off before it disappears.
- For our player: No separate player mode is needed. Offer a 'removal' step preset: instruct state = current model + direction cue; one intermediate keyframe = part displaced; result state = part hidden.

### STR-18 · confirmed

**Present kit contents as a separate short guide of static named views ('All Electronics', 'All Wood') with no title page, numbering, Transitions or final view.**

- Applies to: parts overview; LAC only (one guide)
- Evidence: 2 viewer steps, both pause / 800 ms, camera moves on both, 0 annotations; a hidden 'Start' sits last in the order.
- Exceptions: Single instance; 'All Wood' still carries Cadasio's placeholder description; the guide is titled 'Electronics' although its second view is wood.
- Why it helps students: A quick visual inventory to check the kit against before building.
- For our player: If wanted, treat as a guide made only of card-type steps; do not design structure around it.

### STR-19 · confirmed

**Do not rely on step description text or popups. Carry the instruction in the frame itself; the only text the viewer chrome supplies is the step name.**

- Applies to: all, all kits
- Evidence: Real description text on 52 of 1037 steps (LSM Part 1+2 28 of 47, Part 2 18 of 31, Part 1 6 of 19). The other 17 guides, including every project created after 2025-08-22, have none. Popups 0 of 1037.
- Exceptions: Where text exists it is stale: numbering lags the step names, two steps both say 15, typos ('srew', 'Buttoim', 'Ste[ 15', 'Step 12c 0 Connect'). Cadasio placeholder text on LSM Part 4 [000], LSM Part 3+4 [000], LAC Electronics [001].
- Why it helps students: Guides work for any reading level and language, and students keep their eyes on the model rather than on a caption.
- For our player: A caption field is optional. The player must show the step name itself (cards depend on it for their title).

### STR-20 · confirmed

**Apply the global look (white background, toon style and edges on every solid, default visibility) once, in a base-state keyframe before or at the first visible step, and build every later step as a delta on it.**

- Applies to: all, all kits (authoring pipeline)
- Evidence: In 20 of 20 guides the first authored step sets background #ffffff and a render style on 1148-5373 solids. That step is hidden in 15, is the visible Start in 4, and is the first view in LAC Electronics. 68 hidden steps in 17 guides; hidden steps' changes fold into the next visible step.
- Exceptions: Apart from the base state, hidden steps are abandoned drafts (duplicate 'Step 2', 'colors', 'Step 97', stale 'Step 23c'). startStepId points at the visible Start in only 1 of 20 projects.
- Why it helps students: Indirect: every frame of every guide has the same look because it is set in one place.
- For our player: Put house style in a kit-level theme, not in step data. Store step states as deltas on the previous state (or flatten at publish), and drop draft steps at publish.

### Added by the re-check

- Treat each annotation as a single-use object owned by one step. A cue that has to appear again (an eye icon, a lead line for the second leg of a seat) is a new object, not the earlier one switched back on. *Evidence:* 1010 distinct annotation objects account for all 1019 showings across the 20 guides; only 9 objects are shown in two separate steps (LSM Part 2 3, LSM Part 1+2 4, LSM Deconstruction 2). Second-leg lead lines at PMG Full [106] [111] [114] and the second arrows on 9 PMG Deconstruction Transitions are all new objects.
- A camera-only bridge Transition takes the whole camera move; the Step N that follows it keeps that view. And every up-axis flip is undone before the guide ends. *Evidence:* After each of the 10 camera-only Transitions between pairs (LSM Part 3 [005], LSM Part 4 [018], LSM Part 3+4 [007] [014] [032], LSM Full [052] [059] [077], LAC Part 4 [019], LAC Full [108]) the next Step N has no camera change: 10 of 10. Scene up-axis is +y on the Start and on the final step of 20 of 20 guides although it changes 39 times in between.
- In a take-apart guide a removal may be two beats instead of three: cue on Step N, part fades out on Step Nc, no Transition. The newest kit does this more often than not. *Evidence:* PMG Deconstruction: 11 of 23 numbered steps (Steps 5, 9, 15-22, 23) go cue -> fade-out with no Transition, against 6 slide-off removals with one. LAC Deconstruction Steps 23 and 31, LSM Deconstruction Step 20 do the same.
- Unplugging a wire in a take-apart guide is a fixed three-frame idiom: eye-icon cue on Step N, an auto Transition that swaps the plugged wire for its loose model, then fade-out on Step Nc. *Evidence:* 12 numbered steps in LAC Deconstruction (Steps 19-22 and 36-43, e.g. [101] -> [102] -> [103] and [105] -> [106] -> [107]); all 12 use the eye icon as the Step N cue, 4 add a text label.
- Section cards cover only some bought-in components, and coverage has grown with each kit. The Arduino Nano and the breadboard never get one. *Evidence:* Jumper wires aside: LSM 2 part cards + 1 pin diagram for 7 component types (no card for breadboard, Nano, resistors, push button), LAC 5 for 9 (none for breadboard, Nano, resistors, potentiometer), PMG 5 for 6 (none for the Nano, first seen at PMG Full [002] Step 1).
- A preparation action on a loose part is its own numbered pair shown with the part isolated; the assembly comes back on the next Step N. In the LSM and LAC full builds these cuts are where the step-level 'fade' transition sits. *Evidence:* 30 of 331 build Step N frames cut to a scene with under 25 % of the previous frame's solids (not counting steps after a card): LSM 14, LAC 12, PMG 4. Examples: LSM Full [008] Step 4 (254 -> 8 solids, resistor alone) then [010] Step 5 (8 -> 304); LAC Full [017] Step 8 (561 -> 30) then [019] Step 9. LSM Full: 12 of 13 fades are such cuts; LAC Full: 11 of 13.
- Compose layouts for a viewport of about 2:1. Annotation positions are stored in percent of the viewport, and the saved renders show the authoring window, not the embed size. *Evidence:* Every viewer step has a saved render (1037 of 1037). First-step render sizes: 2559 x 1239 (2.07:1) in 14 guides, 2:1 in 3 (LSM Part 1, PMG Part 1, PMG Part 2), 1.95:1 in 2 (PMG Part 3, PMG Full), 2.63:1 in PMG Deconstruction - the one title page where the title overlaps the model. Project embedSize is Cadasio's 560 x 315 (16:9) in 20 of 20.
- Clones keep the master's entire annotation inventory and get fresh step ids, so most stored annotation objects in a part guide are dead weight and a part can be tied to its master only by content. *Evidence:* 1524 of the 2534 annotation objects stored across the 20 projects are never visible in the viewer (LAC Part 3 shows 23 of 150; LAC Electronics 0 of 150; PMG Part 2 32 of 133). 0 step ids are shared between LAC Full, PMG Full or LSM Full and any of their parts or deconstructions. LSM runs on two CAD models: Parts 1, 2, 1+2 on cadId 1baeed31; Parts 3, 4, 3+4, Full, Deconstruction on 4114fb73.
- Read part visibility from leaf-level flags, starting each leaf hidden when it or any ancestor carries the CAD 'hidden' flag. Neither the digest's rule (every ancestor must be visible) nor the leaf's own flag alone matches the renders. *Evidence:* Checked on four renders. Digest rule drops the hovering D4 panel at LSM Part 3 [001] and the 4-digit display and USB cable on PMG Part 2 [000]. Leaf-own-flag rule (used in the analyst's report) shows 39 LCD solids on the LAC Part 2 [001] 'Rocker Switch' card and a 323-solid LED matrix through LSM Deconstruction [000]-[025]; neither is in the render. The third rule matches all four. At classification grade the analyst's counts survive (only 7 Step N frames change class), but the digest's APPEAR / MOVE lines under-report in LSM Parts 3, 4, 3+4, Full and Deconstruction (35 build Step Nc look static there and are not).

### Numbers (as corrected by the re-check)

| Setting | Value | Basis |
|---|---|---|
| Step animation duration | 800 ms (confirmed) | 1030 of 1037 viewer steps; the 7 others are 1600 ms |
| Duration for a threaded spin move (nut on/off) | No default - keep 800 ms. 1600 ms is an unsystematic exception, not a convention | Only 2 authored LSM steps (nut off, nut on) carry it, seen 5 times through clones (LSM Part 2 [017] [022], LSM Part 1+2 [033] [038], LSM Full [035]); LSM Full does nut-on at 800 ms [040]; LAC nut steps are 800 ms; the other two 1600 ms steps are LCD pose swaps in LAC Deconstruction [016] [017] |
| Part show / hide / move animation | fade / fade / tween (confirmed) | 1037 of 1037 steps |
| Camera animation | tween, no orbit animation, speed setting 2 (confirmed) | 1037 of 1037 steps |
| 2D annotation show / hide / move | fade / fade / tween (confirmed) | 1037 of 1037 steps |
| Behaviour of Start, card, Step N, Step Nc, final view | pause (confirmed) | 920 of 920 |
| Behaviour of Transition | play (confirmed) | 115 of 117; pause at LAC Deconstruction [033] [118] |
| Transition listed in step picker | no, hideInStepPicker = true (confirmed) | 108 of 117 Transitions (6 false, 3 unset); 0 of 920 other steps hidden |
| Navigation overlay during Transition | hidden, overlayVisible = false (confirmed) | 110 of 117 Transitions; visible on 920 of 920 other steps |
| Step-level page transition | none on 970, unset on 2, fade on 65 | The claim's 970 + 65 leaves 2 unaccounted: Start of LSM Part 4 and LSM Part 3+4 have no value. Fade: LSM 36 (including 4 in LSM Deconstruction), LAC 29, PMG 0 of 298 |
| Annotation lifetime | 1 viewer step (confirmed) | 1012 of 1019 showings; 1010 distinct objects, 9 shown in two separate steps |
| Annotations on title page | 2 images, no leaders (confirmed) | 19 of 19 |
| Annotations on final view | 0 (confirmed) | 19 of 19 |
| Annotations on a section card | 0 to 2, usually 1 (confirmed) | 31 cards: 6 with 0, 23 with 1, 2 with 2 |
| Camera moves on Step Nc | never (confirmed) | 0 of 424; no raw camera field changes on any Step Nc |
| Camera moves on Step N | 63 % over all guides, median rotation 62.5 deg (build) / 55.7 deg (deconstruction); on the six master projects 60 %, 58.0 deg (build) / 55.7 deg (deconstruction) | 266 of 425 over all 19 numbered guides, which counts cloned steps up to three times; 145 of 240 on the three full builds plus three deconstructions |
| Annotation-only Step N in build guides (statistic inside STR-2) | 89 of 331 (27 %), not 82 (25 %) | 7 frames counted as moves carry only a 0.005-0.042 mm stored position change on one part |
| Transitions inside one numbered step | 0 typical, 1 common, max 3 (confirmed) | 334 pairs with 0, 76 with 1, 9 with 2, 2 with 3 |
| Share of numbered steps containing a Transition | 9 % construction; deconstruction 60 % pooled but 79 % LSM, 57 % LAC, 43 % PMG | 31 of 331; 19 of 24, 27 of 47, 10 of 23 |
| Viewer steps per numbered step | 2.24-2.62 construction, 2.65-2.88 deconstruction | Per-guide ratios, 19 guides (claim rounded the low end up to 2.3) |
| Numbered steps per part guide | 5-26, median 13 (confirmed) | 11 part guides: 8, 13, 5, 12, 14, 18, 8, 17, 14, 11, 26 |
| Numbered steps per full build | 38 (LSM), 57 (LAC), 51 (PMG) (confirmed) | 3 full builds |
| Section cards per full build | 4 / 5 / 5, about 1 per 10 numbered steps (confirmed) | 14 cards for 146 numbered steps |
| Logo position (top-left corner) | x 2 %, y 4-8 % of viewport (confirmed) | 18 of 19 at x 1.81-2.50 %; PMG Deconstruction 5.13 % |
| Logo size | width 37.58 / 38.90 / 39.53 % of viewport width in 15 guides, 33.24 % in the three oldest, 36.38 % in PMG Deconstruction; height = 0.27 x width | Stored geometry, 19 title pages; the claimed 37.6-39.5 % range leaves out PMG Deconstruction |
| Title block position (top-left corner) | x 2 %, y 61-65 % of viewport (confirmed) | x 1.61-2.50 % in 18 of 19 (PMG Deconstruction 3.75 %); y 60.99-64.64 % in 18 of 19 (LSM Part 1 24.08 %) |
| Title block size | width 42-46.5 % of viewport width, height 0.19-0.29 x width (confirmed) | 17 of 19; LSM Part 2 48.36 %, LSM Part 1 58.28 % with h/w 0.56 |
| Hero model bounding box on title page | Target area x 48-54 % to 88-95 %, y 13-15 % to 74-83 % on the nine clean renders; across the 18 renders near 2:1 the model spans left 41-61 %, right 83-99 %, top 8-24 %, bottom 72-83 % | My pixel measurement of all 19 title renders; PMG Deconstruction (2.63:1, model runs off the bottom and under the title) excluded from the range |
| Logo fill colour | #00B0EF (confirmed) | Modal logo colour on 19 of 19 raw title renders |
| Title text colour | #585858 (confirmed) | Modal text colour on 18 of 19 raw title renders; #5B5B5B on PMG Deconstruction's smaller 1920 x 729 render |
| Background colour | #ffffff (confirmed) | Set in the first authored step of 20 of 20 and never changed; the project default underneath is #EEEEEE |
| Copyright line | (c) <year> TechBox. A division of TARIS Industries, LLC. All Rights Reserved. (confirmed) | Read on all 19 title blocks; 2025 on 14, 2026 on 5 |
| Title-page camera elevation | 21-47 deg, median 35 (confirmed) | 19 title pages |
| Final-view camera elevation | 21-48 deg, median 38 (confirmed) | 16 build guides (21.3-47.7, median 38.1) |
| Final-view direction vs title-page direction | within 23 deg, median 13 deg (confirmed) | 14 of 16 build guides at 2.5-21.6 deg; LAC Part 4 and LAC Full 75.8 deg |
| Final-view distance vs title-page distance | x1.00 (9 guides), x0.86 (3), x0.63 (3); one guide x1.17 (confirmed) | 16 build guides; 0.86 = 1/1.166, 0.63 = 1/1.166^3, 1.17 = PMG Part 1 |
| Camera type and field of view | perspective, 45 deg as project default; one step overrides to 50 deg | Default 45 in 20 of 20 projects; 1036 of 1037 viewer steps; LSM Part 1 [011] 'Capacitor' sets 50 and [012] returns to 45 |
| Navigation overlay | horizontal bar at bottom, visible at start (confirmed) | 20 of 20 |
| Auto-start / animate when stepping back | true / true (confirmed) | 20 of 20 |
| Final step name | Completed View (confirmed) | 16 of 19; 'Completed Build' x2, 'Copmleted View' x1 |
| Result-step suffix | lower-case 'c' with no space (confirmed) | 422 of 424; 'Step 20C' and 'Step 14C' are the two capitals |

### Open questions

- Which step does the live viewer open on? startStepId matches the visible 'Start' in only 1 of 20 projects (hidden step in 7, mid-guide step in 3, dangling id in 9). The data fit 'first non-hidden step in order' but this was not observed in a browser.
- After a 'play' Transition, does the viewer advance the instant the 800 ms animation ends, or is there a dwell? playStepTimeout is null in 20 of 20, which suggests no dwell.
- When the student presses Back from a Step Nc that follows a Transition, does the viewer stop on the Transition or run back through it to Step N? animatePreviousStep is true everywhere but backward behaviour over 'play' steps is not in the data.
- What does step-level transition 'fade' look like compared with 'none'? It is used 65 times in LSM/LAC and never in PMG, so it may not be worth reproducing.
- Is the 'c' suffix meant to be read by students (the step picker lists 'Step 3' and 'Step 3c' as two entries), or would TechBox prefer one step with two states in its own player?
- Should the last frame of a deconstruction keep the name 'Completed View'? It shows the leftover base, not a completed model.
- Are the LSM 'Part 1 + 2' and 'Part 3 + 4' combined guides still a wanted format? They exist only for the oldest kit and have drifted from the parts and the full build.
- Is an auto Transition wanted for large camera flips? LSM does it 8 times; LAC and PMG flip the view directly on Step N 22 times.
- Should the 1600 ms spin exception be kept? Its own kit applies it inconsistently and LAC's nut steps use 800 ms.
- Does TechBox want step description text supported at all? It survives only in three 2025 LSM projects and is stale there.
- Should the part guide's final view always be a separate camera-only step after a real last Step Nc? PMG Part 1 merges the two.
- The title block is a baked image with the copyright year inside it (2025 on LSM/LAC, 2026 on PMG) and 'Stem' rather than 'STEM' on LSM. Should the in-house player render it as live text so these can be corrected centrally?

## Step granularity and build ordering

### GRAN-1 · qualified

**A numbered step is a pair: 'Step N' (waits) then 'Step Nc' (waits), with 0-2 auto-advancing Transition frames between them in builds (up to 3 in take-aparts). The unit of a step is one kit item, not one hand action: one number may hold 2-3 chained motions of that item, and a loose jumper's two insertions share one number. Actions that add no part still get a number (34/146).**

- Applies to: all; construction guides of all three kits (LSM, LAC, PMG); the take-apart guides use the same pair but usually with a Transition
- Evidence: 331/331 build steps have both halves. Exactly one student-level item per step: 128/146 (88%) in the 3 full builds, 288/331 (87%) over all 17 build guides, 82/94 (87%) take-apart. Steps that add no part: 34/146 (23%; LSM 9, LAC 16, PMG 9). Frames per step: 2 in 131/146 (90%), 3 in 13, 4 in 2. Computed by grouping viewer frames into Step N..Step Nc units with a leaf-level visibility tracker and hand-labelling the 240 unique steps.
- Exceptions: 18 master steps handle more than one item: 7 preparation steps (ribbon splits of 2-12 wires, one '2x' lead bend), 7 identical-pair steps (4 placements, 2 flex, 1 push-home of four posts), 3 'do the rest' batches, and LSM Step 19 [041] (two leads). Naming slips only: LSM Part 4 'Step 8'/'Step 9c'; LAC Deconstruction 'Step 41' and 'Step 45c' used twice; PMG Part 1 and PMG Deconstruction close their last step with 'Completed View'.
- Narrowed because: 'Both halves 331/331' needs stand-ins: PMG Part 1 Step 14 [032] is closed by 'Completed View', LSM Part 4 'Step 8' [024] is closed by 'Step 9c'. 'One step per hand action' fails for 9 master steps that chain 2-3 motions under one number (LSM 29 [064]-[066]; LAC 45 [098]-[101], 52, 56; PMG 42, 43, 48, 50, 51) and for the 33 loose-jumper steps (two insertions each), while LSM gives each wire end its own number. 'Annotated' is 145/146: PMG Step 15 [035] has no annotation. In take-aparts 2 Transitions are set to pause (LAC Decon [033], [118]).
- As first stated: Make one numbered step per student hand action. A numbered step is always a pair: 'Step N' (annotated, waits) then 'Step Nc' (result, waits), with 0-2 auto-advancing Transition frames between them. Give a number to every action, including ones that add no part (peel, bend, split, strip hardware, swing shut, push home, spread, turn, pick up).
- Why it helps students: A class works at one pace: one click = one thing to do, then one frame to check it against. Small manipulations that are easy to skip (bending leads, pushing posts home) are not buried inside another step.
- For our player: The step model must be {intro frame, 0..n auto frames, result frame} with an explicit step type (place, second stage, wire, cable, prep, remove-for-prep, adjust, flex, pick up, seat wired, batch). The authoring pipeline should refuse a step that mixes two actions and must allow steps whose 'add' list is empty.

### GRAN-2 · confirmed

**Seat exactly one rigid part per placement step and never animate two different parts in one step. If the part being held needs a new stationary part to go into (base panel, mounting panel), let that receiver fade in already seated in the same step instead of giving it a step of its own.**

- Applies to: construction, mechanical and plug-in electronics; all three kits
- Evidence: PLACE steps seating one part: 44/48 master, 103/114 all build guides; the rest seat 2 identical parts. Steps moving two different kit items: 0/48. Steps with hole/pin labels that handle exactly one part: 54/55 master. Receiver-appears-seated: 6/48.
- Exceptions: 4 identical-pair steps (GRAN-3). LSM Step 19 has labels for two leads. In PMG Step 26 both H1 and H2 are new; only H2 moves.
- Why it helps students: Only one thing moves on screen, so there is no doubt which part to pick up; every label on screen belongs to that one part.
- For our player: A place step needs one moving part (or one rigid group) plus an optional list of parts that simply appear seated (the prototype's 'appear' field). The generator should pick the hand-held part as the mover even when the other part is the new one. A step that adds two different moving parts should be split.

### GRAN-3 · qualified

**On first placement, at most two identical wood parts share one step, with 0 text labels and one lead line (or two) per part; four identical posts are split 2+2 with a camera turn. A later joint second stage may move more than two at once.**

- Applies to: construction, mechanical (wood); LSM and LAC
- Evidence: 4 master steps (11 over all guides), all wood, all with 0 text labels, same travel within a pair (64.6/64.6, 81.6/81.6, 83.1/77.4, 80.3/80.3 mm); lead lines 2 or 4 per step.
- Exceptions: Not grouped although identical: the two LAC resistors (Steps 5, 6, each has its own hole labels), PMG button modules while being wired, all jumper wires. PMG has no pair step.
- Narrowed because: 'Never animate more than two parts together' is false: LSM Step 34 [075]-[076] tweens all four D11 posts 7.0 mm at once (also LSM Part 4 Step 8 [016], LSM Part 3+4 Step 14 [030]). 'Same travel within a pair' is false for LSM Step 33 [073]: 83.1 vs 77.4 mm (same direction). Pair travel also differs between copies of the same step (D9: 64.6 mm in Full, 68.0 in Part 4, 65.3 in Part 3+4). 'Both clearly visible from one view' is an interpretation resting on one case (the 82 degree turn at [073]).
- As first stated: Put two identical parts in one placement step only when they share the same motion and are both clearly visible from one camera view; otherwise split them into consecutive steps with a camera turn between. Never animate more than two parts together.
- Why it helps students: Halves the clicks for mirror-image parts without hiding either one; a pair is still easy to count.
- For our player: Allow a place step to carry at most two instances of the same part id with one shared path; the pipeline should check both are unoccluded from the step camera and otherwise emit two steps.

### GRAN-4 · qualified

**For a group of four or more identical drop-in parts that need no destination label, show one in full and then add one 'do the rest' step where the remainder appear seated (no lead lines, no labels, no per-part motion). Observed for groups of 4, 4 and 64; not used for the four D11 posts (2+2). A group of exactly three never occurs.**

- Applies to: construction, mechanical repeats; LSM (stems) and PMG (keys, button modules)
- Evidence: 3/3 cases of 3 or more identical drop-in parts (batch sizes 63, 3, 3). Batch step: 0 lead lines, 0 text labels, no per-part motion (fade-in or pose swap).
- Exceptions: Four D11 posts are done 2+2 with full animation instead. The quantity cue is not standardised: card '64x' + eye icon, inset '3x', or only an eye icon on the next part. '64x' vs '64X' between copies.
- Narrowed because: The stated threshold '3 or more' confuses the remainder (3, 3, 63) with the group (4, 4, 64). 3 of 4 groups of four or more are batched; the D11 posts (LSM Steps 32-33) are not. Identical items that need labels are never batched: the four PMG button modules take 12 single-wire steps (Steps 3-14).
- As first stated: For three or more identical drop-in parts, show one in full (hover, lead line, seat) and then add a single 'do the rest' step in which the remaining ones simply appear seated with a quantity cue.
- Why it helps students: Students learn the move once and are not made to click through 63 identical animations; the quantity cue tells them how many are left.
- For our player: Support a batch step type: a list of part instances that fade in at their seated pose, tied to the exemplar step, with a mandatory quantity badge ('Nx'). Pick one cue and use it every time.

### GRAN-5 · confirmed

**Connect one wire per step and never group wires. For a loose jumper show both ends in the same step with two destination labels; for a lead that is already attached to a component connect one free end per step with one label.**

- Applies to: construction, wiring; LAC and PMG as stated; LSM uses an older variant
- Evidence: One wire per WIRE step: 47/48 master, 100/103 all guides. Loose jumper = 2 labels + 1 eye icon: 33/33 master (66/66 all). Captive lead = 1 label + 1 eye: 8/8 (16/16). 0/48 wire steps have a lead line, a Transition, an isolated view or a moving part; the completed frame is a model swap in 48/48.
- Exceptions: LSM (oldest kit, 2025) connects one wire END per step: 3 wires take 6 steps (male ends 10-12, female ends 13-15, 1 label each, no eye icon). LSM Step 19 connects both push-button leads in one step with 2 labels (3 copies).
- Why it helps students: Wiring mistakes are the commonest classroom failure; one wire with its two named destinations per click makes each connection checkable before the next.
- For our player: A wire step takes one wire id, a loose model and a routed model, and one or two endpoint labels; the pipeline should generate one step per wire automatically and never merge them. Decide explicitly whether to follow the newer whole-wire convention (recommended) or LSM's end-by-end one.

### GRAN-6 · confirmed

**Treat anything that arrives pre-assembled as one part: a jumper with its two end housings, a switch or potentiometer with its leads, a module with its coin cell, a cable with its plugs. Move and show it as one rigid unit and never give the sub-pieces their own steps.**

- Applies to: all; all three kits and the LAC parts overview
- Evidence: CAD components per kit item: jumper 3, captive lead 2, switch 7, pot 7, push button 5, buzzer 5, RTC 3, USB 3. Loose-jumper completed frames add 1 wire + 2 housings in 66/66 LAC+PMG steps; captive leads 1 + 1 in 16/16. No step adds housings alone. LAC Electronics shows 31 CAD components as 9 kit items (my tracker: groups of 7, 5, 4, 3 share one displacement).
- Exceptions: The potentiometer's knob, nut and washer arrive attached but must be taken off and refitted, so they do get steps (GRAN-8). LSM data sometimes stores housings or the nut as sub-solids of the component, which is a modelling difference only.
- Why it helps students: The on-screen unit matches what comes out of the bag, so students are not asked to assemble something that is already assembled.
- For our player: The part list must be defined at kit-item level with a mapping to the CAD nodes that make it up; add/move/label operations address the item, and tooltips give every node of an item the same name.

### GRAN-7 · confirmed

**Give every preparation its own numbered step, shown with the part alone on a blank background, immediately before the part is first used. Split a jumper ribbon in one step into exactly the wires the next wiring run needs.**

- Applies to: construction; all three kits
- Evidence: 15/146 master steps are preparation (9 PREP + 6 REMOVE_PREP); all 15 shown in isolation. Ribbon split sized to the following run: 6/6 (3, 6, 2, 4, 12, 9 wires). All 6 removal-preps in the full builds are Step N (arrow) -> auto Transition -> Step Nc.
- Exceptions: LAC bends both resistors in one step with a '2x' label; LSM bends each in its own step. The LSM capacitor gets a card but no prep step. LSM Part 1 and Part 1+2 peel step has no Transition (2/14 over all guides). PMG Step 15 ribbon split has no annotation at all.
- Why it helps students: The student sees what the part should look like before installing it, with nothing else on screen to distract; having exactly the right number of loose wires on the desk prevents picking the wrong one.
- For our player: Add a prep step type that hides everything except the part, shows a before/after model swap or a small fan-out, and is auto-inserted before the first use of any part flagged 'needs preparation'. Ribbons need a 'split into N' prep derived from the next wiring run.

### GRAN-8 · confirmed

**Give every fastener or loose hardware part (nut, washer, knob) its own step, both when it comes off and when it goes on; take hardware off outside-in and refit it in exact reverse order.**

- Applies to: construction and deconstruction, mechanical; LAC (knob, nut, washer) and LSM (nut)
- Evidence: 8/8 master build hardware operations and 7/7 take-apart ones are single-part steps; 0/15 grouped. Off order knob, nut, washer; on order washer, nut, knob.
- Exceptions: No screws exist in any of the three kits, so batching of identical screws is untested. Nuts spin while travelling when removed but not when fitted in LAC.
- Why it helps students: Small hardware is what gets lost or fitted in the wrong order; one piece per click fixes the sequence.
- For our player: Hardware steps are ordinary single-part place/remove steps on a shared axis; the pipeline should generate the refit sequence as the reverse of the removal sequence. A policy for identical screws must be decided separately (see open questions).

### GRAN-9 · qualified

**Stage a compound fit: either give the second motion its own numbered step or chain it with an auto-advancing Transition inside the step. The camera never moves inside a build step. Which of the two is chosen is not settled by the data: a new viewpoint goes with 5 of 7 own-step cases, and 6 of 7 own-step cases are a swing of a part that is already hooked in.**

- Applies to: construction, mechanical (tab-and-slot wood, wired seats); all three kits
- Evidence: 7 master second-stage steps, 9 master steps with a staged Transition. Camera turns before the second numbered stage in 5/7 (PMG 62-85 degrees in 4/4, LSM Step 34 117 degrees); camera never moves inside a Transition (0/9).
- Exceptions: LSM Step 25 and LAC Step 46 are separate numbered steps with the camera unchanged. LAC F9 uses both (two Transitions in Step 45, then Step 46).
- Narrowed because: Viewpoint criterion fails for LSM Step 25 [055] and LAC Step 46 [102] (own step, camera unchanged). Swing criterion fails for LSM Step 34 [075] (own step, pure push) and for rotations that sit inside in-step chains (LAC 45 second Transition [100], LAC 56c [127], PMG 51c [115]). Counts 7 and 9 reproduce; camera moves inside 0 of 31 steps with a Transition over all build guides.
- As first stated: Split a compound fit into stages and never play it as one long animation: make the second stage its own numbered step when it needs a different viewpoint, otherwise chain it with an auto-advancing Transition inside the same step.
- Why it helps students: Hook-then-swing and drop-then-lock joints fail if done in one push; a separate frame for each stage shows the intermediate position and lets the camera show the second joint.
- For our player: Keep the prototype's 'stage_of' link between steps and add multi-leg paths with auto-advance waypoints. The pipeline rule: same camera works for both legs -> one step with a waypoint; otherwise -> two numbered steps.

### GRAN-10 · qualified

**Usually (6-7 of 10) handle an already-wired sub-assembly in two numbered steps: pick it up (eye icon, pose change, no lead line), then attach it (lead lines or arrow). Small tab-less modules and one panel are seated in a single step.**

- Applies to: construction, enclosure phase; all three kits
- Evidence: 7/10 master seat steps are preceded by a pick-up step for the same item. All 9 pick-up steps carry an eye icon and no lead line. All 19 pick-up/seat steps are pose swaps, none tweens.
- Exceptions: 3 single-step seats (buzzer, first button module, LSM panel D2). LSM Step 23 and LAC Step 47 only move a wired item out of the way.
- Narrowed because: 'Immediately preceded' holds for 6/10; in LSM the pick-up is Step 28 and the seat Step 30, with Step 29 (D10 clipped on) between. Three single-step seats: LAC 43 [094], PMG 33 [073], LSM 21 [046]. Two pick-ups never lead to a seat (LSM 23 [050], LAC 47 [104]). 9/9 pick-ups have an eye and no lead line; 19/19 are pose swaps.
- As first stated: Handle an already-wired sub-assembly in two numbered steps: first identify it and bring it over (eye icon, pose change), then attach it (lead lines or arrow, seated). Small modules without tabs may be seated in one step with two eye icons.
- Why it helps students: Wired parts dangle and are easy to confuse; the first step tells the student which one to pick up before the second shows where its tabs go.
- For our player: Wired modules need pre-posed variants (module + re-routed wires) and two step types, 'pick up' and 'seat', that cross-fade between variants; the pipeline should emit the pair automatically for any part that has wires attached and tabs to engage.

### GRAN-11 · confirmed

**Do not spend a numbered step on things the student does not attach: the base panel just appears under the first part, loose modules are introduced by an unnumbered section card and are simply present afterwards, and the next identical module may fade in during an auto Transition.**

- Applies to: construction; all three kits
- Evidence: 14/14 section cards in the three full builds come before the first step using the component and consume no number. Base panel never has its own step: 3/3 kits.
- Exceptions: PMG '4-Digit Display' card is followed by a ribbon-split step before the first display wire. Cards are uneven: Nano, resistors, potentiometer and all wood get none. The LSM matrix changes pose between Step 15 and Step 19 with no step.
- Why it helps students: Step numbers stay meaningful (every number is something to do) and new components still get a clean look-at-this moment.
- For our player: Cards are a separate unnumbered step kind; the numbering function must skip cards, auto frames, title and end pages. Parts need an 'introduced by card / present from step k' attribute so they can appear without a placement step.

### GRAN-12 · confirmed

**Cut a long build into Parts of roughly 5-26 numbered steps, each a self-contained block that ends when a wiring run or a mechanical block is complete; restart numbering at 1 in each Part and number continuously in the full build.**

- Applies to: all build guides; all three kits
- Evidence: Numbered steps per single-part guide: 5, 8, 8, 11, 12, 13, 14, 14, 17, 18, 26 (median 13, mean 13.3). Combined guides 18, 21. Full builds 38, 57, 51. Slice mapping verified by event signature: LAC 57/57, PMG 51/51, LSM 47/77 identical (rest data-level).
- Exceptions: LSM Part 3+4 Step 1 repeats the panel step of Part 2. LSM Part 2 swaps the last two steps relative to the Full Build.
- Why it helps students: A Part fits one lesson and ends at a state that can be put away and checked.
- For our player: Author once as a full build and derive Parts as index ranges with a numbering offset and their own title/end pages; the cut points should be stored as data and validated (never between a prep and its use or between two stages).

### ORD-1 · qualified

**Build the electronics on the open base first: carrier, then controller, then small plug-in parts, then all wiring. In the full builds the USB cable is the last electronics step and no panel is joined to the base before it.**

- Applies to: construction; all three full builds
- Evidence: All wiring before the first enclosure panel: 3/3 full builds. USB directly after the last wire and before the enclosure: 3/3, at 53%, 70% and 49% of the numbered steps. Controller is the first component placed: 3/3.
- Exceptions: LSM Part 2 and Part 1+2 put the button panel before the USB cable; the LSM Full Build reverses them.
- Narrowed because: USB-last holds in 5 of the 7 guides that contain the step; LSM Part 2 and Part 1+2 put the panel-on-base step before it. 'All wiring before the first enclosure panel' is true only for panels joined to the base: LSM D2 is on screen from Step 17 [037] and LAC F4 / F1 from Steps 15 / 25 as loose carriers. 'Controller is the first component placed' is 1/3: in LSM and LAC the breadboard is placed at Step 2 and the Nano at Step 3.
- As first stated: Build the electronics on the open base first: carrier and controller, then small plug-in parts, then all wiring; plug in the USB cable as the last electronics step; only then start the enclosure.
- Why it helps students: Everything is reachable while it is being wired, and the circuit can be powered and checked before it is boxed in.
- For our player: The authoring checklist/generator should order phases as base -> controller -> plug-ins -> wiring -> cable -> enclosure and flag any wire step that comes after an enclosure step.

### ORD-2 · qualified

**After the plug-in parts are on the board, finish one module completely before starting the next: mount it (if it mounts), then connect all its pins in one unbroken run.**

- Applies to: construction, wiring; LAC and PMG (LSM partly)
- Evidence: 11/11 component blocks in LAC + PMG are contiguous. Wire runs: LSM 6, 1; LAC 6, 3, 2, 5, 4; PMG 12, 9; every run starts right after that component's placement or a ribbon-split step.
- Exceptions: LSM connects all three near ends (Steps 10-12) before the module is shown, then all far ends (13-15). LAC's two Nano rail jumpers (13-14) follow the RTC wires.
- Narrowed because: 11/11 blocks are contiguous. But small plug-in parts are front-loaded regardless of module: LAC resistors at h27/h29 go in at Steps 5-6 and the switch they serve arrives at Step 15. 'Every run starts right after a placement or a split' fails twice: the pot leads start after the knob-turn step (LAC 29), the buzzer leads after a card. LSM does near ends of all three wires before the module is shown.
- As first stated: Finish one component completely before starting the next: prepare it, mount it, then connect all of its pins in one unbroken run of wire steps.
- Why it helps students: The student keeps one component and one area of the board in mind at a time, and the camera can stay still for the whole run.
- For our player: Group wire steps by target module in the source data so the generator can keep one camera per group and insert the card/prep at the head of each group.

### ORD-3 · qualified

**Within a module, connect wires in the physical order of its pins or leads, not by electrical function, and do not use wire colour to mean function. Taking modules in ascending controller pin order is a PMG-only convention.**

- Applies to: construction, wiring; PMG fully, LAC and LSM mostly
- Evidence: PMG: 6/6 modules in header order; shield pin number never decreases over 21 wires (20/20 adjacent pairs). LAC captive leads in the same colour order 3/3 components. Power pair first in only 4 of 13 module blocks. Wires taken in ribbon order: LSM 3/3, PMG 21/21.
- Exceptions: LAC RTC goes VCC, GND, SDA, SCL (one swap against pin order). LAC's 6-wire ribbon is used out of ribbon order ([018] vs Steps 9-14). Colours contradict convention (black to (+) in LAC Step 9, red is GND in PMG Step 19).
- Narrowed because: Ascending controller pin order fails in LAC: Nano-side rows run 8, 9, 14, 12, 1, 3, 5, 4, 8, 9. PMG is non-decreasing 20/20 only if the Step 10 [023] label 'S5' is read as S6; as printed it is 19/20. LAC RTC has one swap against pin order. Colour is not functional: black to (+) in LAC Step 9 [019], red to GND in PMG Step 19 [043].
- As first stated: Within a module, connect wires in the physical order of its pins or leads (along the header, or red-tan-black for a lead set), and take modules in ascending controller pin order. Do not reorder by electrical function, and do not use wire colour to mean function.
- Why it helps students: The next connection is always the neighbouring pin, so the student can track position by eye rather than by reading pin names; labels, not colours, carry the meaning.
- For our player: The wiring table should be sorted by (module, pin index) before steps are generated; wire colour should be assigned from ribbon position and treated only as an identifier.

### ORD-4 · qualified

**Mount a panel-mounted component on its loose panel first, in an isolated view, and wire its leads next. The panel joins the enclosure later: much later in LAC, as the first enclosure step in LSM.**

- Applies to: construction, mechanical + wiring; LSM and LAC
- Evidence: 3/3 panel-mounted components. All 7 mount/hardware steps hide the rest of the build; the build fades back on the first lead step.
- Exceptions: PMG has no panel-mounted component.
- Narrowed because: 'Much later' is LAC only (F4 attached at Step 49, F1 at Step 54). In LSM the panel is joined at Step 21, two steps after its leads (Step 19). The isolated block is 12 steps, not 7, when strip and adjust steps are included (LSM 16-18; LAC 15, 22-29).
- As first stated: Mount a panel-mounted component on its loose panel first, in an isolated view, wire its leads next, and join that panel to the enclosure much later.
- Why it helps students: Nuts and bodies are easy to reach on a loose panel, and the leads can be plugged in before the box closes around them.
- For our player: Support sub-assembly scopes: a run of steps that shows only a named subset of parts, after which the main assembly is restored and the sub-assembly continues as a wired module (GRAN-10).

### ORD-5 · qualified

**Order the enclosure by dependency: datum panel first, each support before what it carries, wired modules seated after their mount exists, the panel that covers the interior last.**

- Applies to: construction, mechanical; all three kits
- Evidence: Datum first 3/3; cover panel last 3/3 (D8 + stems, F6, H14); carriers before carried in every case checked (D9, D11, F7, F9, H11-H13). First-leg insertion direction of 48 placements: down 25, sideways 17, oblique 5, up 1; all 11 breadboard/shield plug-ins go straight down.
- Exceptions: Direction of growth differs: LSM walls first then interior then upward; LAC interior first then outer panels; PMG frame, underside, then top. 'Bottom-up' is not a general rule.
- Narrowed because: 'Right after its mount exists' fails for the LAC LCD: mount F9 is done at Steps 45-46, the LCD is hung at Step 52. 'High-count small parts at the very end' rests on the LSM stems alone; PMG's four keys go in at Steps 38-39 of 51. Direction counts reproduce within one borderline case (LSM Step 24 [053] is 28 degrees off the axis): mine are down 24, sideways 17, oblique 6, up 1.
- As first stated: Order the enclosure by dependency, not by height: datum panel first, each bracket or support before the thing it carries, each wired module seated as late as access allows and right after its mount exists, the panel that covers the interior last, and high-count small parts at the very end.
- Why it helps students: Every part has something to locate against when it arrives, and nothing has to be undone to reach a slot.
- For our player: The authoring pipeline should derive mechanical order from a mating-dependency graph (which tab enters which slot) plus an access check, not from Z height; it should also expose the scene up-axis per step so side or underside insertions can be shown as drops.

### ORD-6 · confirmed

**Group all work that needs the same orientation into one block so the model is turned over once and turned back once.**

- Applies to: construction, mechanical; PMG (target convention), weaker in LSM and LAC
- Evidence: PMG: 8 consecutive underside steps, 2 up-axis changes. LSM: 5 non-upright steps in 3 episodes (23; 24-26; 34). LAC: 10 in 3 episodes (22-29 isolated sub-assembly; 35; 56).
- Exceptions: LSM and LAC re-orient several times; only the newest kit is clean.
- Why it helps students: Fewer flips means fewer chances for loose wired parts to pull out and less re-orientation of the student's mental picture.
- For our player: Give steps an orientation attribute and let the sequencer cluster by it; flipping should be a scene-level up-axis change with a camera swing, not a part rotation.

### ORD-7 · confirmed

**Number the engraved part IDs in build order so the next part is always the next number.**

- Applies to: construction, mechanical; PMG only
- Evidence: PMG 14/14 in numeric order. LSM order D1, D2, D4, D3, D5, D9, D10, D6, D11, D7, D8 (7/10 adjacent pairs ascending). LAC order F3, F4, F1, F7, F9, F8, F5, F2, F6 (4/8).
- Exceptions: LSM and LAC do not follow it at all.
- Why it helps students: The part ID doubles as a progress cue and makes it obvious which panel to pick up without any text.
- For our player: If TechBox controls the engraving, generate part IDs from the step order; if not, the player must not assume ID order equals build order.

### GRAN-DEC-1 · qualified

**In a take-apart, remove one unit per step; lift wired modules off the housing while still wired and dismantle them later. Identical rigid multiples often come off together but not always.**

- Applies to: deconstruction; all three kits
- Evidence: RM steps removing one part 39/45; 6 remove identical sets (64, 4, 2, 2, 2, 2). DISMOUNT 11 steps, all pose swaps. One item per step overall 82/94 (87%). Frames per step: 3 in 50/94, 2 in 37/94.
- Exceptions: LSM Deconstruction Step 17 combines unplugging two leads with removing panel D2; Step 4 hides four posts for one frame by mistake. PMG never removes H2/H3 in a step.
- Narrowed because: 'Identical multiples together' fails for the two identical LAC resistors (Decon Steps 45, 46), the four LSM posts (2+2, Steps 6, 7) and every LAC wire (20 single steps). 82/94 becomes 81/94 if LSM Decon Step 17 [046] (two leads plus panel) is counted as multi-item. Frames per step by viewer frames are 37 / 49 / 6 / 2; the analyst's 50 / 5 counts Transitions (LAC Decon step 40 has a stray extra pause frame [104]).
- As first stated: In a take-apart guide remove one unit per step, take identical multiples off together, lift wired modules off the housing while still wired, and dismantle them later.
- Why it helps students: Take-apart is lower risk than building, so identical parts can go in one go; keeping modules wired until the wood is gone avoids strain on connectors.
- For our player: Take-apart can be generated from the build by reversing and merging (pairs of stages, exemplar + batch, pick up + seat become one step), with removal shown on an auto frame between intro and result.

### GRAN-DEC-2 · confirmed

**Decide one wire granularity for take-apart; the published guides disagree (one wire per step in LAC, bundles in PMG, mixed in LSM).**

- Applies to: deconstruction, wiring; all three kits
- Evidence: LAC 20 wires in 20 steps (12 whole jumpers with a Transition, 8 lead ends without). LSM 3 single ends + one 3-way connector step. PMG 5 wires in one step and 16 wires in one step.
- Exceptions: This is an inconsistency between kits, reported as such.
- Why it helps students: Bundles are faster and unplugging carries little risk; single wires are consistent with the build. Either works, but mixing them is confusing.
- For our player: Make wire grouping a setting of the take-apart generator (per wire / per module bundle); the newest guide suggests per-module bundles.

### GRAN-DEC-3 · confirmed

**Run the take-apart in near-reverse build order by physical access, with fewer steps than the build, and stop at the base carrier.**

- Applies to: deconstruction; all three kits
- Evidence: Step ratio take-apart/build: LSM 24/38 = 0.63, LAC 47/57 = 0.82, PMG 23/51 = 0.45. Spearman correlation of take-apart order with build order (component matched to the build step where it first appears): -0.93, -0.91, -0.99.
- Exceptions: Electronics are regrouped by component rather than strictly reversed (PMG Steps 17-23; LAC wire groups); LAC adds 3 steps refitting hardware for storage; preparation steps have no counterpart.
- Why it helps students: Reverse order is predictable and guarantees every part is reachable when its turn comes.
- For our player: Derive the take-apart sequence from the build graph (reverse topological order with merges) rather than authoring it separately; never emit a step that removes the carrier (breadboard on base, shield).

### Added by the re-check

- Use an unnumbered, auto-advancing Transition between two numbered steps for changes that are not a student action: turning the model back, reframing, or bringing the next module on screen. *Evidence:* 7 in the full builds and 16 over all build guides; none in take-aparts. LSM Full [052] (130 degrees), [059] (53), [077] (110), each with an up-axis change; LAC Full [108] (13 degrees, between Step 48c and Step 49); PMG Full [013], [020], [027] (next button module fades in). The analyst reports only the PMG three.
- PMG builds the housing frame as its own work-piece with the electronics hidden, then brings the wired cluster back; LSM and LAC build the enclosure around the electronics on the base. *Evidence:* PMG Full Steps 26-32 [059]-[072] show 2-6 wood parts only; the electronics return at Step 33 [073] (80 components on screen). In LSM Full [048] and LAC Full [090] the electronics stay on screen from the first enclosure step.
- Batching ('do the rest') is used only for placements that need no destination label; wiring of identical modules is never batched. *Evidence:* Four identical PMG button modules take 12 single-wire steps (Steps 3-14), each with 2 labels and 1 eye, while their drop-in seating is batched 1+3 (Steps 33-34).
- Parts placed in separate steps can share one joint second-stage step. *Evidence:* LSM Step 34 [075]-[076]: the four D11 posts placed in Steps 32 and 33 are pushed home together from underneath (4 lead lines, 1 eye, 117 degree camera turn, up-axis flipped). Same in LSM Part 4 Step 8 and Part 3+4 Step 14.
- Anomalies not in the analyst's list (typos and settings, not conventions). *Evidence:* 'Transititon' LAC Decon [002]; 'Ttansition' LAC Full [053] and LAC Part 2 [023]; 'Transiton' LSM Decon [038]; 'Step 20C' LSM Part 1+2 [042]; 'Step 14C' LAC Part 1 [030]; 'Copmleted View' LSM Part 3+4 [042]; 'Completed Build' instead of 'Completed View' in LSM Part 2 [030] and Part 1+2 [046]; two LAC Decon Transitions set to pause ([033], [118]); PMG labels 'clk / s8' [037] and 'dio / s9' [039] in lower case; PMG Step 51c [115] keeps two lead lines on the result frame; 11/146 result frames carry an annotation.
- The section card is placed inconsistently relative to the ribbon-split step. *Evidence:* Split then card: PMG Step 2 then 'Push Buttons' [006]; LAC Step 35 then 'LCD Screen' [078]. Card then split: PMG '4-Digit Display' [034] then Step 15 [035].

### Numbers (as corrected by the re-check)

| Setting | Value | Basis |
|---|---|---|
| Frames per numbered build step | 2 (Step N + Step Nc) in 90%; 3 in 9%; 4 in 1% | 131 / 13 / 2 of 146 full-build steps; 300 / 27 / 4 of 331 over all build guides. Reproduced. |
| Frames per numbered take-apart step | 3 in 52%, 2 in 39%, 4 in 6%, 5 in 2% | 49 / 37 / 6 / 2 of 94 by viewer frames. The analyst's 50 / 37 / 7 counts Transitions; LAC Decon step 40 has a stray extra pause frame [104]. |
| Viewer frames per numbered step, whole guide | 2.29-2.32 for full builds; 2.65-2.88 for take-aparts; 2.24-2.62 for part guides | 88/38, 131/57, 117/51; 61/23, 130/47, 69/24. Stated range 2.7-2.9 rounds 2.65 up. |
| Student-level parts per step | 1 in 88% (builds) and 87% (take-aparts) | 128/146, 288/331, 82/94 reproduced under the analyst's definitions; 81/94 if LSM Decon Step 17 counts as multi-item. |
| Maximum parts animated together in a build step | 2 identical parts on first placement; 4 in one joint push-home step | 4 master pair steps (11 over all guides); LSM Step 34 [075]-[076] moves four D11 posts 7.0 mm at once (3 copies). The stated maximum of 2 is wrong. |
| Batch threshold for identical drop-in parts | Groups of 4 or more (seen 4, 4, 64): one exemplar step then one 'rest' step | 3 of 4 groups of four or more; the four D11 posts are done 2+2. The stated 3, 3, 63 are remainders. A group of exactly 3 never occurs. |
| Wires per wiring step | 1 | 47/48 master, 100/103 all build guides. Reproduced. |
| Wire ends and labels per wiring step | Loose jumper: 2 ends, 2 labels, 1 eye. Captive lead: 1 end, 1 label, 1 eye. LSM: 1 end, 1 label, no eye | 33/33 (66/66), 8/8 (16/16), 6/6 master (18/18 with slices). Reproduced. |
| Fasteners per step | 1, off and on | 15/15 hardware steps (8 full-build, 7 take-apart). Reproduced. |
| Screws | None in any kit | No screw, bolt or standoff in any of the 20 inventories; only LAC knob / nut / washer and an LSM nut modelled as a sub-solid. |
| Ribbon split size | Exactly the wires needed until the next split: 2-12 | 6/6 (3, 6, 2, 4, 12, 9). Reproduced. The 9-wire split serves two modules. |
| Share of steps that add no part | 23% | 34/146 (LSM 9, LAC 16, PMG 9). Reproduced. |
| Share of wiring steps | 33% (LSM 18%, LAC 35%, PMG 41%) | 48/146 (7/38, 20/57, 21/51). Reproduced. |
| Numbered steps per Part | Median 13, mean 13.3, range 5-26 | 11 single-part guides. Reproduced. |
| Numbered steps per full build | 38, 57, 51 | Reproduced. |
| Position of the USB cable step | 49-70% of the build; last electronics step in the full builds | Step 20/38, 40/57, 25/51. Last electronics step in 5 of the 7 guides that contain it; LSM Part 2 and Part 1+2 put a panel step first. |
| CAD components per kit item | Jumper 3, captive lead 2, switch or pot with leads 7, push button 5, buzzer 5, RTC with cell 3, USB cable 3 | Reproduced with my own tracker. |
| Camera turn with a separate second-stage step | 62-117 degrees in 5 of 7; 0 in 2 of 7 | PMG 68, 67, 85, 62; LSM Step 34 117; LSM Step 25 and LAC Step 46 unchanged. Reproduced. |
| Underside block | One block of 8 consecutive steps, 2 up-axis changes | PMG Steps 29-36 only. Reproduced. |
| Take-apart to build step ratio | 0.45-0.82 | 24/38, 47/57, 23/51. Reproduced. |
| Take-apart vs build order | Spearman -0.90 to -0.99 | My own component mapping; the exact value moves by a few hundredths with the treatment of wires and pose copies. |
| First-leg insertion direction | Down 50-52%, sideways 35%, oblique 10-13%, up 2% | 48 placements. Mine: 24 / 17 / 6 / 1; analyst 25 / 17 / 5 / 1. One borderline case (LSM Step 24, 28 degrees off the axis). |

### Open questions

- Loose jumpers: follow the newer convention (one whole wire per step, two labels; LAC and PMG, 33/33) or LSM's one-end-per-step? The data favours the newer one but LSM was never re-authored.
- Screws: none of the three kits has any, so there is no evidence for how identical screws would be grouped. Apply the hardware rule (one per step, GRAN-8) or the identical-part rules (pair, or exemplar + 'Nx' batch, GRAN-3/4)?
- Exact threshold for batching identical parts: 2 are animated together, 4 posts were done 2+2, 3 keys and 3 button modules were batched after an exemplar. Is 3 the intended cut-off, and does visibility from one camera override it?
- The quantity cue for a batch is different in each of the three cases (card '64x' + eye, inset '3x', eye only). Which one should the TechBox player standardise on?
- Should engraved part IDs follow build order? Only PMG (the newest kit) does; LSM and LAC do not.
- Take-apart wire granularity is inconsistent (per wire in LAC, bundles in PMG). Which should the in-house generator use?
- Two identical resistors: LAC bends both in one '2x' prep step, LSM bends each separately. Which is intended when the parts really are identical?
- Second stage as its own numbered step vs an auto Transition: the camera-change explanation fits 5/7 cases; LSM Step 25 and LAC Step 46 do not. Is there another criterion (e.g. the student must pause to check the hook)?
- The TechBox prototype (steps_repro.json) has a place step that adds two different parts at once (R2 together with the base servo). Under GRAN-2 this would be two steps or one part appearing seated; which is wanted for the MRA kit?
- LSM Full Build puts the USB cable before the button panel, LSM Part 2 the other way round. Which order is correct for that kit?
- Tooltips and the live viewer were not checked (data only); whether batch steps and pose swaps look the same in the live player as in the saved renders is unverified.

## Part motion, hover offsets and seating

### MOT-1 · qualified

**Every rigid part that is PLACED BY A TWEEN gets two beats: it is on screen and stationary at a hover pose on Step N, then moves on the next press. Not every rigid part is tweened: receivers, the rest of large identical sets, carded modules and plugged cables fade in seated, and wired sub-assemblies are cross-faded. Never move a part while it fades IN (holds for 95 of 99 fade-ins; 97 if sub-millimetre nudges are ignored). The hover pose is staged before the frame that shows the part, but for half of them (50 of 99) it is written in the first frame after the title page, the same frame in which the finished model fades OUT, so pose changes on parts that are hidden or being hidden must be applied without animating them.**

- Applies to: construction, mechanical and plug-in electronics; all three kits (LSM, LAC, PMG), 16 build guides
- Evidence: 119 first-stage insertion tweens in 16 build guides (50 unique in the 3 Full Builds), recomputed from raw payloads. Hover pose reached by: fade-in on the Step N itself 86; fade-in on the section card before 6; swapped in at hover on the previous prep c-step 7 (bent resistors); already on screen and sliding to hover 13; nudged <=1.6 mm 4; already hovering 3. Of the 99 fade-in cases the hover pose was written while the part was hidden in 97 (98%). 116 of 116 distinct hover steps carry red lead lines.
- Exceptions: 13 visible slide-outs to hover, all state carry-over rather than intent: breadboard lifted for the peel on Step 1 (LSM Part 1, Part 1+2, Full; LAC Part 1, Full; 39.3-49.2 mm); first step after a title page that shows the finished state (LSM Part 3 [001] D4 69.4, LSM Part 4 [001] D9 68.0, LAC Part 4 [001] F7 80.3, PMG Part 3 [001] H2 40.0, LAC Part 2 [001] switch 81.2); LAC potentiometer backing off 79.1 mm (LAC-F [055]); LSM Part 1 capacitor returning 69.5 mm from its card [012]. 2 fade-ins write the pose in the same step (LAC switch card [031], PMG-F H2 [059]).
- Narrowed because: Pose reached in the frame that shows the part: LAC-F [031] switch 81.2 mm, PMG-F [059] H2 40.0 mm, PMG-F [081] and PMG-P3 [023] H8 0.9 mm. Visible slides to hover: breadboard LSM-P1 [001], LSM-P12 [001], LSM-F [001], LAC-P1 [001], LAC-F [001]; LSM-P3 [001] D4 69.4; LSM-P4 [001] D9 68.0; LAC-P4 [001] F7 80.3; PMG-P3 [001] H2 40.0; LAC-P2 [001] switch 81.2; LAC-F [055] and LAC-P2 [025] potentiometer 79.1; LSM-P1 [012] capacitor 70.2. Move plus fade-out in one frame: LAC-F [001] 6 parts, LSM-F [001] 6, LSM-P34 [001] 6 (all under step fade); PMG-F [001] 6 and PMG-P3 [001] 10 with no step fade. Rigid parts that never hover: LAC F3 [004], F4 [032], F1 [055]; LSM D1 [004], D2 [037]; PMG H1 [059]; 63 stems LSM-F [086]; 3 keys PMG-F [086].
- As first stated: Give every rigid part two beats: fade it in standing still at a hover pose (Step N), then move it home on the next press (Step Nc). Stage the hover pose while the part is still hidden; never move a part while it is fading in.
- Why it helps students: The student first sees which part to pick up and where it is aimed, with nothing moving; the motion on the next press then answers only one question: where does it go.
- For our player: Step data needs separate show and move phases. On entering a step, snap the pose of any part that is hidden at the start of the step, then fade it in; only tween parts that were already visible. Treat Start -> Step 1 as a cut so title-page end state does not produce fly-outs.

### MOT-2 · confirmed

**Make Step Nc a single straight translation of the hovering part to its seat, same duration as every other step, with no rotation and no camera move.**

- Applies to: construction, mechanical and plug-in electronics; all kits
- Evidence: First-stage insertions: one leg on Step Nc in 106 of 119 (89%) over all build guides, 44 of 50 unique. 103 of those 106 carry zero rotation. Camera unchanged on 424 of 424 c-steps across all 20 guides. Across 331 build step pairs: 163 tween something, 157 cross-fade between two models, 11 only fade something in.
- Exceptions: 13 multi-leg seats (6 unique, see MOT-3). 3 single-leg tweens rotate: the three copies of the LSM nut going on with a spin (LSM-F [040], Part 2 [022], Part 1+2 [038]). Some single legs deliberately stop short (LSM D11 posts 7.0 mm proud at [072], [074], pushed home at [076]).
- Why it helps students: One straight line is the easiest motion to copy with a hand, and because the camera is still the student can compare before and after in the same frame.
- For our player: Default move = linear position interpolation between two stored poses over one step; lock the camera for the whole N -> Nc pair.

### MOT-3 · qualified

**When a part cannot go straight in, give each leg its own authored step: earlier legs on auto-advancing 800 ms Transitions, the last leg on Step Nc, so one press plays all legs back to back (1.6 s or 2.4 s). A second stage that is a separate hand action may instead be its own numbered step whose Step N shows the part resting in the intermediate pose; this is the usual choice (6 of 8 swings) and it comes with a new camera in only 5 of 8, so a change of viewpoint is not the trigger.**

- Applies to: construction, mechanical (tab, hook and clip joints); all kits
- Evidence: Multi-leg via Transition: 13 step pairs in 16 build guides (11 two-leg, 2 three-leg), 6 unique. Split into two numbered steps: 8 unique. Every leg is 800 ms; a two-leg seat is 1.6 s, three legs 2.4 s, no dwell. Of 115 auto-advancing steps in all 20 guides, 67 carry a part tween, 33 a cross-fade or fade, 15 camera or annotation only; 0 of the 67 move the camera.
- Exceptions: The lock slide of H11 / H12 is tiny (6.7 / 7.6 mm). LAC-F Step 45 uses two Transitions and still leaves F9 tilted for Step 46.
- Narrowed because: Second stage in its own numbered step WITHOUT a camera change: LAC F7 [092], LAC F9 [102], LSM D3 [055]. With a change: PMG H5 [067], H6 [071], H7 [079], H10 [089], LSM D11 [075]. Same hook-then-swing joint authored the other way (swing on Step Nc right after a Transition): LAC F2 [126]->[127], PMG H14 [114]->[115].
- As first stated: When a part cannot go straight in, give each leg its own step: legs before the last go on auto-advancing Transition steps, the last leg on Step Nc. If the second stage needs a different viewpoint, make it its own numbered step whose Step N shows the part resting in the intermediate pose.
- Why it helps students: The student presses Next once and sees the legs in the right order (drop, then lock), or gets a new camera for the second stage so the locking feature is visible.
- For our player: Support chained auto-advance sub-steps inside one student step (keyframe list per part, 800 ms each), with annotations swappable per leg; support a step whose start state is an intermediate, not-yet-seated pose.

### MOT-4 · qualified

**Place the hover pose back along the path the part travels: lead lines lie on that path (parallel within 3.9 deg, length ratio median 1.00). Plug-in electronics come straight down their pin axis. Judge the direction on screen, not in world axes: the scene up-axis is switched per step so that the hovering part is above or beside its seat and never below it. About a quarter of hovers are oblique in world axes (12 of 50 unique), all along the part's own slide path.**

- Applies to: construction, mechanical and electronics; all kits
- Evidence: 50 unique hovers: +Y (from above) 25 = 50%; horizontal single axis 14 = 28%; -Y 3 = 6% (washer, nut, knob on the potentiometer shaft, LAC-F [057]-[062]); oblique 8 = 16%. All 119 copies: single-axis 101 (85%), oblique 18. Electronics into breadboard / socket: 27 of 27 straight down. Lead-line length / hover distance for single-leg seats: median 1.00, quartiles 0.94 / 1.08 (255 lines).
- Exceptions: All 8 unique oblique cases follow the physical path: tilted hook-in panels sliding in their own plane (LSM D3, LAC F2, PMG H5, H6, H14), L-shaped two-leg paths (LSM D10, LAC F9), slanted slots (PMG H13). For multi-leg seats the hover pose is the start of the path, not on the final insertion axis. Anomaly: the LSM capacitor is modelled about 6 deg off vertical and hovers at [3.4, 32.7, 0] mm in Part 1 [012] and Part 1+2 [011].
- Narrowed because: Counted as single-axis by the analyst but off-axis: PMG H7 [077] 11.7 deg, H10 [087] 7.8 deg (both slide in their tilted plane per MOT-6), H11 [091] 7.2 deg, H12 [094] 9.7 deg (L-paths). Not vertical: LSM capacitor 5.9 deg at LSM-P1 [012] and LSM-P12 [011]. World '-Y' hovers that read as sideways on screen: washer, nut, knob at LAC-F [057], [059], [061].
- As first stated: Place the hover pose back along the path the part physically takes: straight up for anything that plugs into a breadboard or socket, along the tab axis for panels (often sideways), and never from an arbitrary 'nice-looking' direction.
- Why it helps students: The gap between part and target shows the true direction to push, so the student orients hand and part correctly before touching the model.
- For our player: Each part needs an authored insertion vector (or path); the default hover offset is minus that vector. Do not default to 'up'.

### MOT-5 · qualified

**Choose hover distance by kind of fit, not by a constant: 30-44 mm for boards and passives, 39-49 mm for the breadboard, about 65 mm for a 3 mm panel moving face-on (42-69), about 80 mm for a panel-mount part with leads (roughly 1.2 x body-plus-leads when the leads trail along the travel), 56-61 mm for hardware onto a short shaft and 80-83 mm when it must first pass leads. 'About one part-length' applies only to parts that truly slide lengthwise (10 of 22 unique wood rows, ratio 0.83-1.05); the rest of that class ranges 0.29-5.71 and is better served by its median, 81 mm.**

- Applies to: construction, mechanical and electronics; all kits
- Evidence: All 119: min 22.9, quartiles 42.6 / 60.5 / 80.8, max 139.4 mm (unique 50: 43.5 / 60.9 / 81.5). By class (unique n; min / median / max): breadboard 2; 46.9 / 48.0 / 49.2. Nano and RTC boards 4; 29.8 / 36.7 / 44.1. Passives 5; 29.1 / 32.4 / 40.0. USB plug 1; 22.9. Panel-mount with leads 4; 79.1 / 82.2 / 102.5. Washer, nut, knob 3; 55.9 / 60.5 / 61.3. Stem 1; 43.5 (50.3, 55.1 in part guides). Wood face-on 8; 42.0 / 64.7 / 69.4. Wood edge-on or lengthwise 22; 40.0 / 80.9 / 139.4 with hover / extent-along-travel quartiles 0.8 / 1.0 / 1.6. Size correlation is weak: Pearson 0.46 (50 unique) and 0.49 (119) against extent along travel; Spearman 0.31 / 0.35.
- Exceptions: Values are hand-dragged: identical parts differ (LAC resistors 37.1 vs 40.0; LSM D11 posts 77.4 / 81.6 / 83.1) and the same part differs between guide copies (LSM breadboard 39.3 in Part 1 vs 49.2 in the Full Build; Nano 35.3 vs 44.1; stem 43.5 / 50.3 / 55.1). Short for their size: PMG H2 / H3 40.0 / 43.2 mm for 137 mm panels (ratio 0.29-0.32), H11 / H12 0.62 / 0.51, USB plug 0.46.
- Narrowed because: Class error: the 'panel-mount with leads' class (4 unique, 10 copies, '-Z x3') includes the LSM nut going on, LSM-F [039] 83.1, LSM-P2 [021] 80.4, LSM-P12 [037] 80.4; the mover is the 21.0 x 18.0 x 1.5 mm hex nut. Correct: 3 unique, 7 copies, median still 81.2. Hardware class becomes 9 copies, 55.9-83.1, median 61.3. Not one part-length: LAC F8 [111] 94.2 mm for 16.5 mm extent (5.71), LSM D10 [064] 3.86, LSM D9 [060] 3.49, PMG H8 [081] 3.06; PMG H2 [059] 0.29, H3 [061] 0.32, LSM D3 [053] 0.49, PMG H12 [094] 0.51, H11 [091] 0.62.
- As first stated: Choose the hover distance by the kind of fit, not by a constant: short for plug-in electronics, about one part-length for anything that slides lengthwise, about 60 mm for a flat panel moving face-on, and far enough for trailing leads to clear on panel-mount parts.
- Why it helps students: The gap is always large enough to see daylight between the mating features and to fit lead lines, but the part stays close enough to read as belonging to its target and to stay in frame.
- For our player: Store the hover distance per part, with authoring defaults by fit class (see numeric_defaults) that an author can override; do not hard-code one global offset.

### MOT-6 · qualified

**For a panel that hooks in on one edge and swings shut: show it at hover already tilted by its swing angle, slide it until the tabs engage, then rotate it flat about (or near) the engaged edge, normally as its own numbered step. Sliding exactly in the panel's own tilted plane and pivoting exactly on the edge is how the PMG panels are authored; LSM D3 and LAC F2 only approximate it. LAC F9 is a different joint (lean in its own plane, drop, stand upright) and should not be modelled as a swing.**

- Applies to: construction, mechanical (laser-cut hook-and-swing panels); LSM D3, LAC F2 and F9, PMG H5, H6, H7, H10, H14
- Evidence: 8 unique parts; angles 7.9 / 10.3 / 11.7 / 18.1 / 21.4 / 21.6 / 23.6 / 25.8 deg (median 19.8). Swing stage moves the centroid 4.1-28.4 mm; implied pivot radius 0.85-1.0 of half the panel across the hinge (H5 / H6 / H7 69-70 mm for 139 mm panels). In PMG the slide direction is inclined by exactly the tilt (H5 23.7 vs 23.6, H6 18.1, H7 11.7, H10 7.9 deg). 557 of 576 rotation writes above 1 deg in the raw payloads carry a stored custom pivot ('origin').
- Exceptions: LAC F9 arrives upright and is tilted on a Transition leg instead of at hover. LAC F2's slide direction (33 deg) does not equal its tilt (21.4 deg). The 7 mm push-home of the LSM D11 posts is a second stage with no rotation.
- Narrowed because: LSM-F [053]->[054] D3 slide inclined 27.9 deg against a 21.6 deg tilt (not reported as an exception). LAC-F [125]->[126] F2 33.2 against 21.4. PMG-F [113] H14 hovers at 10.1 deg, swings 12.6 at [115], corrected 2.5 at [116]. PMG H10 pivot 9.7 mm inside the edge; H14 pivot half-way between centre and edge. LAC-F [098]-[103] F9: upright at hover, rotation about the panel's thickness axis near a corner. Stored origin is zeroed at the swing write itself (LAC F2, Step 56c).
- As first stated: For a panel that hooks in on one edge and swings shut: show it at hover already tilted by its swing angle, slide it in its own tilted plane until the tabs engage, then rotate it flat about the engaged edge as a separate stage.
- Why it helps students: It reproduces the only way the part can physically go in; a straight push would jam, and the tilt at hover tells the student to angle the panel before starting.
- For our player: Poses need orientation as well as position, plus a per-move pivot point; interpolate the swing about that pivot so the hinge edge stays put.

### MOT-7 · confirmed

**Do not rotate parts during ordinary insertion. Use rotation only for: swing-to-seat about a hinge edge, flexing a part, a threaded part spinning about its travel axis, and turning a knob in place.**

- Applies to: construction and deconstruction, mechanical; all kits
- Evidence: 103 of 106 single-leg insertion tweens have no rotation. Spin tweens: 11 over all guides (5 unique), 115.1-179.6 deg; the end pose is a quaternion so one step cannot encode more than 180 deg. Duration 1600 ms on 5 of the 11 (all LSM), 800 ms on 6.
- Exceptions: Spin is inconsistent: the LAC nut does not spin going back on (LAC-F [060]), LAC washer and knob do not spin going on, the LSM nut-on spin is 179.3 deg in Part 2 [022] but 115.1 deg and 800 ms in the Full Build [040]; LSM Deconstruction nut-off [049] is 800 ms.
- Why it helps students: Because rotation is rare, when something does turn it reads as an instruction (unscrew this, swing this shut, turn this to its stop).
- For our player: Offer a 'threaded' flag on a move that adds a half-turn about the travel axis and optionally doubles the duration; otherwise keep orientation fixed.

### MOT-8 · confirmed

**Move the part the student is holding, even when the other part is the new one: a new receiving part fades in already in place and the hand-held part hovers and travels to it.**

- Applies to: construction, mechanical; all kits
- Evidence: 6 unique receiving parts fade in at rest on a Step N in the three Full Builds (LSM D1, D2; LAC F3, F4, F1; PMG H1); in each the mover is a different, hand-held part.
- Exceptions: None found; small sample.
- Why it helps students: Screen motion matches hand motion; the base stays put as it does on the desk.
- For our player: The authoring model must allow 'appears seated' for one part and 'hovers then moves' for another in the same step, independent of which part is new.

### MOT-9 · confirmed

**Never animate a wire into its connection. Show a loose, straight wire model in Step N and cross-fade it for a separately modelled routed wire in Step Nc: one wire per step, no lead line, no arrow.**

- Applies to: construction, wiring; all kits (10 build guides contain wiring)
- Evidence: 101 wire-connection steps in build guides (48 in the Full Builds: PMG 21, LAC 20, LSM 7): 101 of 101 are appear + disappear with no move; 100 add exactly one routed wire. 0 of these hover steps carry a lead line or arrow, against 116 of 116 rigid tween steps that carry lead lines. Loose model first appears in the same Step N in 64 of 101; already on screen in 37 (captive leads, hanging ribbon). 7 more steps fade a routed wire or cable in with no loose model (USB cable LAC-F [089], LSM-F [045]; LSM Part 2 button leads).
- Exceptions: LSM-F Step 19 [041]-[042] connects both push-button leads in one step. LSM connects one wire END per step (two steps and two routed models per wire); LAC and PMG connect a whole jumper per step. Deconstruction only: LSM Decon Step 15 tweens a 3-way connector 30.5 mm; PMG Decon Steps 18 and 22 slide wire bundles 36-90 mm while fading.
- Why it helps students: A flexible wire has no single correct path, so an animated path would mislead; the swap shows clearly which wire to pick up and what the finished connection looks like.
- For our player: Model each wire as (at least) two meshes, loose and routed, and implement a cross-fade swap step type; do not build wire path animation.

### MOT-10 · confirmed

**Present the loose wire lying flat and straight at one fixed parking spot beside the assembly on the camera side, and reuse that spot for every wire of the run.**

- Applies to: construction, wiring; LAC and PMG (LSM differs)
- Evidence: Distance from loose-wire centroid to routed-wire centroid: LAC fresh jumpers 80.3 / 106.2 / 127.2 mm (min / median / max, n=10; 76-118 mm sideways, 22-56 mm above); PMG 49.3 / 53.5 / 77.5 mm (n=20). Spot repeatability: LAC Steps 10-14 within 0.8 mm, Steps 36-39 within 2.2 mm; PMG drifts 1.7-1.8 mm per wire (19 mm over 12 wires) and jumps 40 mm between the display and matrix runs.
- Exceptions: LSM hovers the loose ribbon end at its destination instead (13.8-25.8 mm from the routed position, LSM-F [021], [023]). Captive leads are shown straight where their component is (LAC 37.9-119.3 mm away).
- Why it helps students: The eye learns where the 'next wire' appears, so only its colour changes from step to step; the work area stays uncovered for the hole labels.
- For our player: Provide a per-wiring-run 'staging anchor' in the scene; each wire step places its loose mesh there. Allow the alternative 'hover at target' placement.

### MOT-11 · confirmed

**Let a wire actually move in only two situations: fanning a ribbon or pair apart in an isolated prep step, and riding rigidly with the component it is soldered to.**

- Applies to: construction, wiring and mechanical; all kits
- Evidence: 10 fan-out step pairs over all guides (5 unique): sideways only, PMG 12 wires 1.1-17.3 mm (about 3.1 mm per position), PMG 9 wires 0.9-11.9, LAC 6-way 4.4-15.2 (about 5.6 mm per position), LAC 4-way 8.4 / 11.3 / 14.4, LAC pair 10.7 and 9.2. Riding: 7 build step pairs (4 unique).
- Exceptions: A loose wire kept on screen from the prep close-up is relocated to the parking spot as the assembly fades back (LAC-F [019] 177.3 mm, [042] 150.4 mm; PMG-F [037] 11.9 mm): a side effect, visible at [042]. LSM splits its ribbon by model swap, not by tween ([019]->[020]).
- Why it helps students: Both are rigid, unambiguous motions (pull the ribbon apart; the leads come along with the switch), so they can be shown truthfully.
- For our player: Allow wire meshes to be parented to a component for rigid moves, and allow simple per-wire translations in prep steps.

### MOT-12 · qualified

**Move a sub-assembly whose wires are already routed to the rest of the build by cross-fading complete pre-posed copies, never by tweening: a 'pick it up' swap to a copy near the mount (usually also re-oriented 90-180 deg), then an 'attach' swap to the seated copy, with one extra copy on an auto-advancing Transition for hook-on modules. A part whose leads are still free at the far end is tweened like any rigid part with its leads riding.**

- Applies to: construction and deconstruction, wired sub-assemblies; all kits
- Evidence: 45 such step pairs in the 16 build guides (20 in the Full Builds: LSM 4, LAC 8, PMG 8) and 11 in the deconstruction guides; none contains a tween. 7 of 10 wired sub-assemblies in the Full Builds use pick-up + attach; 3 go in one swap (LSM D2 [047], LAC buzzer [095] 170.2 mm, PMG button modules [074], [076] 142 mm). Final attach jump for tabbed panels 49.8 / 56.8 / 56.9 / 76.6 mm, i.e. a normal hover distance. Copies modelled: LSM matrix 5; LAC F1 4, F4 3, LCD 4, switch 3, potentiometer 4; PMG display 4, matrix 4, shield 3.
- Exceptions: Sub-assemblies are tweened while being built in an isolated view before any wire constrains them (LSM-F [034]-[040] button and nut on D2; LAC-F [031]-[033], [046]-[064]). In deconstruction the LAC switch and potentiometer are tweened out of their panels once isolated.
- Narrowed because: Wired part tweened in full-assembly context: PMG USB plug with its cable stub, 22.9 mm, PMG-F [057]->[058] with 74 parts on screen, and PMG-P2 [024]->[025] (not listed under this rule). Wired bundle re-posed by a pose write, not a copy swap: LSM-Decon [037], 60-106 mm and 179.5 deg, on a Step N under a step fade.
- As first stated: Move anything that has wires attached by cross-fading between complete pre-posed copies (part + its routed wires + housings), not by tweening. Use a 'pick it up' step that swaps to a copy near the mount, then an 'attach' step that swaps to the seated copy; add one extra copy on an auto-advancing Transition for hook-on modules.
- Why it helps students: Wires change shape when a module moves; honest before / after poses avoid showing wires stretching or passing through panels, and the hover copy with lead lines still shows the fit.
- For our player: The asset pipeline must support several pose variants of one sub-assembly, each with its own wire meshes, and a cross-fade step that swaps whole variant groups, including a 2-3 frame flipbook.

### MOT-13 · confirmed

**Show a change of shape (bending leads, splitting a ribbon) as a swap between two models of the part alone on screen, with the 'after' model already standing at the hover height of the step that installs it.**

- Applies to: construction, part preparation; LSM and LAC
- Evidence: 11 step pairs over all guides (4 unique), all appear + disappear with no move. Bent model appears 29-40 mm above its seat; 7 of the 119 insertion hovers are entered this way.
- Exceptions: LAC and PMG split ribbons with a small tween instead of a swap (MOT-11).
- Why it helps students: Before / after of the isolated part is unmistakable, and the next step only has to bring the board back under a part that is already where it should be.
- For our player: Reuse the cross-fade swap step type for shape changes; allow a part's mesh variant to be changed without changing its pose.

### MOT-14 · qualified

**Fade parts in already seated when there is nothing new to teach: the rest of a LARGE identical set after one exemplar was animated (64 stems, 4 keys), free-standing modules introduced on a card or Transition, and plugged cables. Small identical sets (2-4 parts) are tweened in full, in pairs.**

- Applies to: construction; all kits
- Evidence: Three Full Builds: 2 'animate one, fade the rest' cases (63 stems, 3 keys); 3 Transition fade-ins of the next peripheral; 6 modules introduced by card or simply present; 2 cables fading in plugged; plus the 48 routed wires.
- Exceptions: The PMG USB plug is tweened 22.9 mm ([057]->[058]) while the LAC and LSM cables just fade in. Wires are identical in kind but never batched.
- Narrowed because: Every member tweened: LSM D11 posts x4 (two at LSM-F [071], two at [073]); LSM D9 x2 together at [060]; LAC F7 x2 together at LAC-F [090]; LAC resistors x2 at [010] and [012]. Keys (4) are batched while posts (4) are not, so set size alone does not decide it.
- As first stated: Fade parts in already seated when there is nothing new to teach: the rest of an identical set after one exemplar was animated, free-standing modules that are introduced on a card or Transition, and plugged cables.
- Why it helps students: It avoids 63 identical animations and avoids implying a placement action for parts that simply lie on the desk.
- For our player: Provide a 'repeat' step that animates one exemplar and then fades the remaining instances in at rest; allow parts to appear with no hover.

### MOT-15 · confirmed

**Show a removal inside a build as hold, slide, fade: Step N shows the part still in place; an auto-advancing Transition slides it straight off along its axis and leaves it there; Step Nc fades it out. Put hardware back in the reverse order with the normal hover-then-seat pattern.**

- Applies to: construction (preparation removals): LSM nut, LAC knob / nut / washer, breadboard backing in LSM and LAC
- Evidence: 14 removals in build guides (6 unique): 12 tween on a Transition, 2 on the c-step (LSM Part 1 and Part 1+2 peel [002]). Travel: small hardware 37.6-37.9 mm; LSM nut 98.9-100.7 mm (it must pass the tips of 75 mm leads); backing sheet 39.3-53.2 mm. Refit hover is larger than removal travel (55.9-61.3 vs 37.6-37.9 mm).
- Exceptions: Only the LSM nut removal runs 1600 ms. The knob does not spin; nut and washer do.
- Why it helps students: The pause before the slide lets the student find the part and read the arrow; the pause after it shows the part clear of the shaft before it disappears.
- For our player: A removal step type = pause frame, auto tween out, auto or next-press fade; reuse it for deconstruction.

### MOT-16 · qualified

**In a take-apart guide move each part back out along its build direction and then hide it; unplug wires by cross-fade. Reusing the build's exact distance and undoing two-stage joints leg by leg is what the PMG guide does (9 of 12 matched parts, 7 of 7 two-stage joints); LAC does it for four wood panels, and LSM collapses two-stage joints into one straight pull.**

- Applies to: deconstruction; LSM, LAC, PMG deconstruction guides
- Evidence: LSM (24 steps): tween on Transition then hide 16, slide-while-fade 1, cross-fade 5, plain fade 2. LAC (47): tween on Transition then hide 14, tween on c-step and stay 6, cross-fade 25, plain fade 2. PMG (23): displacement and hide in the same frame 12, the same after a first-stage Transition tween 6, tween and stay 1, cross-fade 4. Tweened removal travel: min 2.5, quartiles 31.3 / 53.1 / 67.8, max 106.3 mm (n=41). Equal to the build travel within 1 mm for 19 of 53 matched removals (LAC F2, F5, F6, F8; LSM D7, D8, capacitor, resistor 2; PMG H4, H5, H6, H7, H8, H11, H12, H13). 23 wire unplug steps are cross-fades (LAC 20, LSM 3).
- Exceptions: The two authoring styles disagree on when the part fades (after the move in LSM / LAC, during it in PMG). Many distances were re-set by hand (LAC Nano 55.0 vs 39.8 in the build; LSM stems 62.5 vs 43.5; PMG keys 142.5 vs 107.7). LSM Decon Step 4 never shows D5 moving; LAC Decon Steps 16-18 are refits (insertions).
- Narrowed because: Two-stage joints not undone: LSM-Decon [043] D3 one straight 38.4 mm, no swing; [037]-[038] D10 one straight 48.4 mm, not the L-path; [016], [019] D11 posts 70.5-88.8 mm in one pull, no 7 mm stage. LAC-Decon [063] F9 undoes the straighten and the 33.0 mm drop but not the 103.9 mm approach. Equal-distance list omits PMG H10 (4.1 mm + 126.0 mm, identical to the build). Distances re-set: LAC Nano 55.0 vs 39.8, LSM stems 62.6 vs 43.5, PMG keys 142.5 vs 107.7.
- As first stated: In a take-apart guide, move each part along the build's hover vector reversed and then hide it; undo two-stage joints in reverse order with one Transition; unplug wires by cross-fade.
- Why it helps students: The part leaves the way it went in, so tabs and hooks are released in the right order, and removed parts do not pile up on screen.
- For our player: Generate deconstruction moves from the build data (negated hover path, reversed leg order) by default; choose one fade policy and apply it uniformly.

### MOT-17 · qualified

**For a prep step or a section card, hide everything else and show the subject alone; bring the context back by fading on the next Step N. When the next step tweens that same part in, show it on the card already at its hover pose. Most cards (9 of 14 in the Full Builds) introduce a module that is then wired and never hovers.**

- Applies to: construction; all kits
- Evidence: Three Full Builds: 22 context-hide events (12 on cards, 9 on a Step N, 1 on a c-step) and 23 restores (22 on a Step N). Step-level 'transition: fade' marks 13 of 17 hides in LSM-F and LAC-F and 65 of 1037 steps overall; PMG never uses it (0 of 5).
- Exceptions: LSM Part 1's capacitor card moves the part about 70 mm aside (and scales it) and slides it back on Step 6 [012].
- Narrowed because: Cards followed by a tween of their part: 5. At hover exactly: LAC-F [014] RTC, [031] switch, PMG-F [056] USB plug. Nudged: LSM-F [012]->[013] capacitor 0.5 mm and 6.0 deg, [082]->[083] stem 1.0 mm. Moved far: LSM-P1 [012] capacitor 70.2 mm with a scale change. No hover at all after the card: LAC buzzer [071], LCD [078], USB cable [087]; LSM matrix diagram [027], USB cable [043]; PMG shield [001], buttons [006], display [034], matrix [045].
- As first stated: For a prep step or a section card, hide everything else and show the part alone, already standing at the hover pose of the step that follows; bring the context back by fading on the next Step N.
- Why it helps students: The student studies the part without clutter, and when the board fades back the part is already aimed at its seat, so nothing jumps.
- For our player: Isolation = a visibility set per step with fade; keep the isolated part in its real hover pose rather than re-centring it.

### MOT-18 · qualified

**Use one duration and one set of animation options for everything: 800 ms per step, parts tween, show and hide fade, camera tween. Keep the camera still on the steps where motion is intended (every Step Nc and every part-moving Transition). On Step N entries camera moves and carry-over part moves do coincide, mostly masked by a step-level fade in LSM and LAC and unmasked in PMG.**

- Applies to: all guide types, all 20 guides
- Evidence: 800 ms on 1030 of 1037 viewer steps (99.3%); 1600 ms on 7. Part options tween / fade / fade on 1037 of 1037; camera tween, animate_orbit false, speed 2 on all; 2D annotations tween / fade / fade with 'separate_visibility' on all; animationChained false on all; animatePreviousStep true on all 20 guides. 922 pause steps, 115 play steps (all named Transition). Camera unchanged on 424 of 424 c-steps and on 67 of 67 part-motion Transitions; the 12 Transitions that move the camera change no part.
- Exceptions: 2 Transitions in LAC Deconstruction are 'pause' by mistake ([033], [118]). The easing curve itself is not in the data.
- Narrowed because: 35 frames that are neither c-steps nor Transitions move a visible part by more than 0.5 mm or 0.5 deg; the camera moves on 34 (28 Step N, 5 final views, 1 card). 20 exceed 10 mm; 6 of those have no step fade: LAC-F [042] and LAC-P2 [012] loose wire 150.5 mm, LSM-P1 [012] capacitor 70.2 mm, PMG-P3 [001] H2 40.0 mm, PMG-F [037] and PMG-P2 [004] wire 11.9 mm. Play steps are not all named 'Transition': 111 are, 4 are misspelled. One pause Transition carries a tween: LAC-Decon [118], 21.7 mm.
- As first stated: Use one duration and one set of easings for everything: 800 ms per step, parts tween, show / hide fade, camera tween, and never move the camera in the same step as a part tween.
- Why it helps students: A uniform rhythm makes every press of Next feel the same; with the camera still during a move the only thing changing on screen is the part.
- For our player: Global constants: step duration 800 ms, fade = step duration; expose a per-step duration override; enforce camera-or-part exclusivity for motion steps.

### MOT-19 · confirmed

**A 'parts laid out' overview is a static line-up with no hover or seating motion: one row per material class, pre-attached leads left attached, wood panels all turned to one orientation and ordered by part number.**

- Applies to: parts overview; LAC Electronics guide only
- Evidence: 2 views, 0 part tweens of interest, 0 annotations; build guides contain no laid-out view at all (the only staging in them is the parked loose wire and loose wired modules beside the base).
- Exceptions: Single guide, two views; electronics are not sorted or aligned while wood is.
- Why it helps students: It works as a picture checklist of the kit before building.
- For our player: Not a motion feature: a static scene preset is enough.

### Added by the re-check

- On screen the hovering part is always above or beside its seat, never below. When the physical insertion is from underneath or along a shaft, change the scene up-axis or turn the model over instead of animating upward from below. *Evidence:* Hover vectors of all 119 insertions projected through the camera rotation of their Step N: above 75, right 23, left 21, below 0. Scene up_axis is rewritten per step: LAC-F -x on 23 frames (potentiometer sub-assembly, Steps 22-29, sheet [056]-[063]) and -y on 2; PMG-F -y on 16 frames (underside panels H5-H7, sheet [064]-[071]); LSM-F +x on 7.
- Never hover a part along the line of sight: keep at least two thirds of the travel visible on screen. *Evidence:* Component of the hover vector along the view axis for the 119 insertions: median 52%, 90th percentile 64%, maximum 75%.
- Draw the lead line on the motion path. For an L-shaped seat make it a polyline that follows the corner; when the last leg is only a short lock or a swing, draw the first leg only. *Evidence:* 255 lead lines on single-leg seats are parallel to the hover vector (median 0.0 deg, max 3.9 deg) with length ratio 0.94/1.00/1.07. 3-point and 5-point polylines at LSM-F [064], LSM-P34 [019], LSM-P4 [005] (D10) and LAC-F [098], LAC-P4 [009] (F9). Two-point lines covering leg 1 only for PMG H11 [091], H12 [094], H14 [113], LAC F2 [125].
- Annotation type follows the direction of motion: red lead lines for a part going in, a red arrow for a part coming out or being pulled aside. *Evidence:* Insertion hover frames: lead lines on 116 of 116, arrows on 0. Removals inside builds: one arrow on 14 of 14 Step N frames, lead lines on 0. Deconstruction removal steps carry 1-2 arrows; the refits at LAC-Decon Steps 16-18 carry a lead line again; LAC F7 flex-out at LAC-F [092] carries 2 arrows.
- Animation is constant time, not constant speed: every leg takes 800 ms whatever the distance. *Evidence:* 134 insertion legs: 4 mm/s (3.0 mm swing leg of H14) to 174 mm/s (H7, 139.4 mm), quartiles 47/68/99 mm/s.
- Treat the first frame after the title page as a bulk re-pose: the finished model is hidden and the hover poses are written in the same frame, so pose changes on parts that are hidden or being hidden must not be animated (or the frame must cut). *Evidence:* 50 of the 99 fade-in insertions are staged in that frame: LAC-F [001] 6 parts, LAC-P1 3, LAC-P4 3, LSM-F [001] 6, LSM-P1 2, LSM-P12 2, LSM-P3 1, LSM-P34 6, LSM-P4 3 (all with step transition fade); PMG-F [001] 6, PMG-P1 1, PMG-P2 1, PMG-P3 [001] 10 (no step fade). In LSM and LAC 14 of 16 large carry-over moves sit under a step fade; PMG has none.
- Decide cross-fade versus tween by the far end of the wire: wires already routed to the build mean cross-fade between copies; free leads mean a normal rigid tween with the leads riding. Pick-up copies may be re-oriented freely; the attach copy is a straight offset along the insertion axis and is annotated like a normal hover. *Evidence:* 45 of 45 routed sub-assembly moves on build c-steps are copy swaps with no tween; 9 tween pairs carry free leads (switch, potentiometer, push button, and the PMG USB plug in full context at PMG-F [057]->[058]). Rotation between copies 90-180 deg in 8 of 12 pick-up or one-shot swaps; 0 deg and 49.8-107 mm on attach swaps at LAC-F [110], [122], LSM-F [047], [068], PMG-F [102], whose Step N frames carry 2-4 lead lines or an arrow.
- Identical parts in pairs go in together in one step with one shared vector; only sets too large to animate use 'one exemplar, fade the rest'. *Evidence:* LAC F7 x2 80.3 mm at LAC-F [090]->[091]; LSM D9 x2 64.6 mm at LSM-F [060]->[061]; first two D11 posts 81.7 mm at [071]->[072]. Second pair of D11 posts shares a step but not a distance (77.4 and 83.1 mm at [073]). Exemplar-then-fade only for 64 stems and 4 keys.
- ANOMALIES, not conventions: step-name typos and numbering slips that a name-based parser must tolerate. *Evidence:* 'Ttansition' LAC-F [053] and LAC-P2 [023]; 'Transititon' LAC-Decon [002]; 'Transiton' LSM-Decon [038]; 'Copmleted View' LSM-P34 [042]; 'Step 14C' LAC-P1; 'Step 20C' LSM-P12; 'Completed Build' in LSM-P2 and LSM-P12. LSM-P4 [016] 'Step 8' is followed by [017] 'Step 9c'. PMG-P1 'Step 14' [032] and PMG-Decon 'Step 23' [059] have no c frame (the PMG-P1 wire swap lands on the Completed View). LAC-Decon has a stray 'Step 41' at [104] before 'Step 40', and two frames named 'Step 45c' ([120], [122]) with no 'Step 45'. Two 'pause' Transitions in LAC-Decon ([033], [118]).
- METHOD CAUTION: the per-guide digests cannot be used for motion; use the raw payloads with position and rotation as absolute local values and visibility per leaf solid. *Evidence:* Against my raw replay of the 119 insertions the digest MOVE line agrees in 39, has the wrong direction or distance in 46 (part-local axes, e.g. LAC F7 reported +Z for a -Y drop) and is missing in 34 (solids under a CAD-hidden or step-hidden parent, e.g. LAC F5, F2, F6, all LSM lens parts). Verified on LAC F1-1 (position replaces CAD translation), LAC Nut-4 (quaternion returns to the CAD rotation) and PMG-F [056] (USB cable rendered although its parent is hidden).

### Numbers (as corrected by the re-check)

| Setting | Value | Basis |
|---|---|---|
| Step animation duration | 800 ms | Confirmed. 1030 of 1037 viewer steps; 1600 ms on 7 (five LSM nut steps, two LAC-Decon LCD Transitions). |
| Part move / show / hide | tween / fade / fade over the step duration | Confirmed. Identical on 1037 of 1037 steps (2 add animation_attention: none). |
| Camera during part motion | locked on Step Nc and on part-moving Transitions; no guarantee on Step N entries | Narrowed. Camera unchanged on 424 of 424 c-steps and 68 of 68 part-moving Transitions, but 34 other frames (28 Step N, 5 final views, 1 card) move the camera and a visible part together; 20 of them by more than 10 mm. |
| Legs per authored step (was 'legs per press') | 1 leg per step; one press on Step N plays all legs back to back: 2 legs = 1.6 s, 3 legs = 2.4 s | Reworded. 13 multi-leg seats, every leg 800 ms on its own 'play' step, playStepTimeout null on all 20 guides. A press therefore plays 2 or 3 legs, not 1. |
| Threaded spin | about 180 deg about the travel axis (median 175.9); 1600 ms optional | Confirmed. 11 spins: 8 at 170.9-179.6 deg, 3 at 115.1-123.6; axis exactly along travel in all; 1600 ms on 5 of 11, all LSM. |
| Hover: board or passive into breadboard / socket | 35 mm straight along the pin axis | Confirmed. 22 values 29.1-44.1 mm, median 34.5; 25 of 27 plug-in parts exactly vertical, 2 are 5.9 deg off (LSM capacitor). |
| Hover: breadboard onto base | 47 mm | Confirmed. 39.3, 39.3, 46.9, 46.9, 49.2 mm (5 copies, 2 unique), median 46.9. |
| Hover: USB plug | 23 mm along the socket axis | Confirmed. 22.9 mm at PMG-F [057] and PMG-P2 [024]; one part. |
| Hover: panel-mount part with trailing leads | 80 mm; about 1.2 x (body + leads) when the leads trail along the travel | Basis corrected. 7 copies, 3 unique: 79.1 x2, 81.2 x2, 102.5, 103.2 x2; median 81.2. The claimed 10 copies include 3 rows that are the LSM nut. Switch 68.0 mm long with leads, hover 81.2 (1.19); button 82.5 mm, hover 102.5 (1.24). |
| Hover: washer / nut / knob onto a shaft | 60 mm on a bare shaft; 80-83 mm when the nut starts beyond the leads | Widened. LAC 55.9, 60.5, 61.3 mm (6 copies); LSM nut 83.1, 80.4, 80.4 mm was filed in the wrong class. All 9: 55.9-83.1, median 61.3. |
| Hover: flat wood panel face-on | 65 mm along the tab axis | Adjusted from 60. 8 unique: 42.0, 54.1, 56.0, 64.3, 65.0, 67.5, 67.8, 69.4; median 64.7 (21 copies: median 64.3). |
| Hover: part sliding lengthwise or edge-on | 1.0 x extent along travel only for true lengthwise sliders; otherwise about 80 mm | Narrowed. Ratio 0.83-1.05 for 10 of 22 unique (D11 x3, F7, H5, H6, H7, key, F2, H14). Whole class: ratio 0.29-5.71, quartiles 0.83/1.01/1.51; distance median 81.0, quartiles 54.8/94.4. The clamped rule lands within 20% for 11 of 22. |
| Hover: fallback | 60 mm | Confirmed. Median 60.9 (50 unique) and 60.5 (119), quartiles 43.5/81.6, range 22.9-139.4. |
| Tilt of a hook-in panel at hover | its swing angle; 18-20 deg if unknown | Narrowed. 7 parts are tilted at hover: 7.9, 10.1, 11.7, 18.1, 21.4, 21.6, 23.6 deg, median 18.1. LAC F9 (25.8) is upright at hover. H14 hovers at 10.1 but is swung 12.6 and corrected 2.5 afterwards. |
| Swing-to-seat pivot | the engaged edge, on the panel face | Narrowed. Pivot at 0.99-1.00 of half-size for H5, H6, H7; 0.95 for D3; 0.92 for F2; 0.75 for H10; 0.48 for H14. The stored-origin statistic is overstated: origin is non-zero on 373 of 576 rotation writes, not 557, and is zeroed at the swing write. |
| Push-home stage | leave 7 mm proud, finish in a later step | Confirmed. 7.0 mm for all four LSM D11 posts at LSM-F [076], LSM-P34 [031], LSM-P4 [017]. One part type. |
| Flex angle | 15 deg | Confirmed. LAC F7 posts 15.1 and 16.0 deg out at LAC-F [093], back at [097]. |
| Removal travel inside a build | 38 mm for small hardware; about 100 mm past lead tips | Confirmed. Knob 37.6, nut 37.9, washer 37.9; LSM nut 98.8-100.6. |
| Deconstruction travel | build direction reversed; build distance only where the build file was reused | Narrowed. Equal within 1 mm for 17 of 42 distinct matched parts: PMG 9 of 12, LAC 4 of 14, LSM 4 of 16. Tweened removals n=40: quartiles 30.7/52.8/67.6 mm. |
| Loose wire parking distance | 50-60 mm on a compact board, 80-125 mm on a spread layout; same spot within about 2 mm per run; on the camera side | Confirmed. PMG 49.3/53.5/77.5 (n=20); LAC 80.3/106.1/127.2 (n=10); run spread 1.3 and 4.1 mm end to end; 30 of 30 nearer the camera and lower on screen. |
| Loose wire hover at target (LSM style) | about 15 mm from the routed position | Confirmed. 13.3-18.3 mm in 6 of 7 steps by my centroid; the two-lead step is larger. |
| Ribbon fan-out | resulting centre pitch 4.5-5 mm for 9-12 wires, 6-9 mm for 6, 8-13 mm for 4, about 22 mm for a pair (from 1.7 mm) | Reworded. The claimed 3 mm and 5.5 mm are spacing ADDED per position, and 5.5 fits only the 6-way. Measured pitch after: PMG 12-way 4.5-5.3, PMG 9-way 4.1-4.6, LAC 6-way 6.1-9.0, LAC 4-way 7.7-13.1, LAC pair 21.6. |
| Wire connection | cross-fade loose to routed in one 800 ms step, one wire per step, no lead line or arrow | Confirmed. 101 of 101; 0 lead lines, 0 arrows; two wires in one step only for the LSM push-button leads (3 copies). |
| Wired sub-assembly attach copy | 50-77 mm off the seat for tabbed panels, straight along the insertion axis; up to 3 cross-faded frames for hook-on modules | Confirmed. 49.8, 56.9, 57.1, 76.7 mm at 0 deg; 3 flipbooks in the Full Builds (LAC LCD, PMG display, PMG matrix). |

### Open questions

- Easing of the 'tween' is not stored in the payload (linear or eased?); needs one look at the live viewer.
- What does the viewer draw when a part changes pose and visibility in the same step? Build authoring avoids it for show (97 of 99 hover poses pre-staged while hidden); PMG Deconstruction relies on it for hide (18 removals slide while fading). Should the in-house player slide a part while it fades out?
- Does Cadasio interpolate a rotation about the stored pivot ('origin') or lerp position and slerp rotation separately? For a 20 deg swing the hinge edge drifts a few millimetres in the second case.
- Does a step-level 'transition: fade' suppress part tweens (cut) or play both? It decides whether the 177 mm loose-wire relocation at LAC Full Build [019] and the 47-49 mm breadboard lift on Step 1 are ever seen as motion.
- Is 1600 ms for a threaded spin intended? It exists only in LSM and was dropped from one of the two LSM spin steps in the Full Build ([040] is 800 ms).
- Is the change from hovering the loose wire end at its hole (LSM, the oldest project) to parking the wire beside the model (LAC, PMG) a deliberate house-style change?
- Should hover distances be standardised by fit class in the in-house tool, or stay free per part as they are now (identical parts currently differ by 3-6 mm, guide copies by up to 10 mm)?
- Which deconstruction fade policy should be the standard: move on a Transition then hide on Step Nc (LSM, LAC) or move and hide in the same frame (PMG)?
- Scale changes were not tracked in this analysis (the LSM capacitor is reported as shown x2 on its Part 1 card).
- Data caveat for other analysts: digest APPEAR / MOVE lines are wrong wherever a parent node is flagged hidden or a part is rotated; the figures here come from a leaf-level world-space tracker in reports/_work_dim_motion/ (track.py, events.py, analyze.py, master.py).

## Red lead lines and 3D arrows

### LL-1 · qualified

**When a rigid part is animated with a tween onto its mating features, show red lead lines on the frame before the motion (the paused Step N frame, or the auto Transition that starts a second stage). Holds on 56 of 59 such steps in the 3 full builds and 132 of 140 in the 16 construction guides. It is not a rule for seats shown by cross-fade or fade-in: only 6 of the 11 cross-faded seating steps in the full builds carry lines, and faded-in plugs and repeat steps carry none. If nothing is being seated, draw none.**

- Applies to: construction; plug-in electronics and mechanical/plywood steps; LAC, LSM, PMG
- Evidence: 3 full builds: 56 of 59 Step N frames where a rigid part tweens to its seat carry lines; 16 construction guides: 132 of 140. In total 363 line showings on 155 frames (149 Step N, 6 auto Transition, 0 Step Nc); 149 lines on 65 frames in the full builds. Computed by replaying raw payloads with per-solid visibility and classifying each Step N by what changes before its Step Nc.
- Exceptions: Rigid tween steps without lines: LAC Step 42 [092] (spread posts: 2 arrows), LAC Step 44 [096] (close posts: 2 eye icons), LSM Step 38 [085] (63 stems fade in as a repeat). Deconstruction guides show only 3 lines in total.
- Narrowed because: Tweened without lines (8 frames): LAC Step 42 [092] and Part 4 Step 2 [003] (two arrows), LAC Step 44 [096] and Part 4 Step 4 [007] (eye icons), LSM Step 38 [085] and Part 3+4 Step 18 [040] (63 stems fade in), LSM Part 1 and Part 1+2 Step 1 [001] (paper peel, arrow). Seats with no lines because nothing tweens: LSM Step 21 [046] (D2 panel onto base, arrow), PMG Step 46 [101] (shield onto H4, arrow), LAC Step 43 [094] (buzzer), PMG Steps 33-34 [073] [075] (button modules), LAC Step 40 [088] and LSM Step 20 [044] (USB plug fades in), PMG Step 39 [085] (3 keys fade in). Lines not on a paused frame: PMG Transitions [106] [111] [114] and Part 3 [048] [053] [056]. Line with nothing being seated: stray 8.8 mm line on LSM Part 1+2 Step 20 [041]. Rotation-only step with neither line nor arrow: LAC Step 29 [063].
- As first stated: Draw red lead lines on the paused 'Step N' frame whenever a rigid part is about to travel onto mating features (pins into holes, tabs into slots, shaft or body into a hole). If nothing is being seated, draw none.
- Why it helps students: The hovering part alone does not say where it lands; a line from each locating feature to its hole or slot shows the exact destination and the direction of push before anything moves.
- For our player: The step schema needs, per seating step, a list of mating pairs (part id + local point on each side). The player draws one segment per pair on the hover frame. The authoring pipeline must flag steps as 'seat' versus 'other' so lines are generated only for the former.

### LL-2 · qualified

**Never draw a lead line or arrow for a single jumper wire or captive lead being connected, for ribbon splitting, leg bending, or fade-in / repeat steps (0 exceptions in the construction guides). For pre-wired modules that are picked up, carried or dropped in by cross-fade the practice is mixed: of 14 such steps without lines in the full builds, 10 have only eye icons and 4 carry an arrow.**

- Applies to: construction; wiring and preparation steps; all kits
- Evidence: Wire-swap steps with a line or arrow: 0 of 49 in the 3 full builds, 0 of 104 in all 16 construction guides, 0 of 23 single-wire unplug steps in the deconstruction guides. Ribbon split 0 of 5, leg bending 0 of 3 (full builds). 10 of 20 cross-faded sub-assembly steps in the full builds carry only eye icons.
- Exceptions: A USB plug gets one axis line when it is animated as a rigid tween (PMG Step 25 [057]) but none when the cable simply fades in routed (LAC Step 40, LSM Step 20). Wire bundles slid away in take-apart guides do get an arrow (PMG deconstruction Steps 18, 22; LSM deconstruction Step 15).
- Narrowed because: Cross-faded module steps that do carry an arrow: LAC Step 47 [104], LSM Step 21 [046], LSM Step 23 [050], PMG Step 46 [101]. Wire bundles with an arrow in take-apart guides: LSM deconstruction Step 15 [040], PMG deconstruction Step 18 [049] and Step 22 [057] (two arrows). USB plug with one line when tweened: PMG Step 25 [057].
- As first stated: Do not draw lead lines (or arrows) for a jumper wire or captive lead being connected, for splitting a ribbon, bending resistor legs, picking up a pre-wired module, dropping in a small module, or 'repeat for the rest' steps. Use hole/pin labels and the eye icon there.
- Why it helps students: A wire has no fixed path, so a straight red line would suggest a motion that does not exist; keeping red lines for rigid insertions makes them a reliable signal for 'push this straight in here'.
- For our player: Wire steps must be a different step type in the player (model swap + labels + eye icon) with no line generation. The CAD-to-step pipeline must classify parts as rigid versus flexible/tethered.

### LL-3 · confirmed

**Use 1, 2 or 4 lines per frame, never 3 and never more than 4: 1 for an axial or single-tab part, 2 for a two-lead component or a part with two tabs, 4 for a flat body on a plate or a panel located on two neighbours.**

- Applies to: construction; all kits
- Evidence: Lines per frame over 20 guides: {1: 37 frames, 2: 75, 4: 41, 6: 2}; 3 full builds: {1: 15, 2: 33, 4: 17}. By class (all guides): axial part 1 line on 24 of 24 frames; two-lead component 2 on 13 of 13; breadboard onto base 4 on 5 of 5; pin-header boards {2: 4 frames, 4: 5 frames}; plywood {1: 12, 2: 45, 4: 27, 6: 2}.
- Exceptions: 6 lines on LSM Part 3 Step 5 [010] and Part 3+4 Step 6 [012] (one per tab of wall D5); the Full Build's copy of that step [057] has 4.
- Why it helps students: A few lines read at a glance and still fix position and orientation; one line per pin or per tab on a 30-pin board or an 8-slot panel would hide the part behind red.
- For our player: The line generator needs a cap of 4 and a selection step that reduces all mating pairs to 1, 2 or 4 representatives.

### LL-4 · qualified

**For pin headers and rectangular bodies draw lines only at the extremes: the 4 corner pins of a two-row header (or the 2 diagonal corners), both end pins of a single row, the 4 corners of a body. For plywood no consistent selection rule is observable: 1, 2 or 4 pairs are drawn, sometimes fewer than engage and once 6.**

- Applies to: construction; Nano, RTC module, breadboard, plywood panels; all kits
- Evidence: Nano line anchors span 80 % of the board's lateral diagonal in all three kits; RTC 47 % (end pins of its header). 118 multi-line frames: lines mutually parallel within 2 deg on 99 and within 5 deg on 113.
- Exceptions: Authoring differs between kits for the same Nano board (2 lines in LAC, 4 in LSM and PMG). Not every contact is drawn even below 4: PMG H8 [081] 2 lines for its bottom tabs only; H11/H12 1 line for the hook tab only.
- Narrowed because: Plywood clause rests on two authored steps (LAC F5 [123], F6 [128]) and I could not count engaging pairs without mesh data. Against it: 6 lines on LSM D5 in Part 3 [010] / Part 3+4 [012]; PMG H8 [081] 2 lines for bottom tabs only; PMG H11 [091] and H12 [094] 1 line each. Same Nano board: 2 lines in LAC [006], 4 in LSM [006] and PMG [002]. Pin-header evidence is only 5 distinct authorings.
- As first stated: When a part has many mating features, draw lines only at the extremes: the 4 corner pins of a two-row header (or 2 diagonal corners), both end pins of a single-row header, the 4 corners of a rectangular body, and for plywood every tab/slot pair that engages in this stage up to 4; if more engage, 2 on each of two neighbouring panels.
- Why it helps students: Widely spaced lines show alignment and orientation of the whole part; students line up the corners and the rest follows.
- For our player: Feature selection must rank mating pairs by spread (convex-hull corners of the pair set) and by neighbour panel, not just take the first N.

### LL-5 · confirmed

**Anchor each end of a line to a part at a mating point: one end at the tip of the male feature (pin tip, lead tip, tab tip, shaft end), the other inside the matching female feature (hole, slot, socket). Store it as part id + local point so the end follows the part; treat the line as undirected.**

- Applies to: construction; all kits
- Evidence: 333 of 363 lines are linked to a part solid at both ends; 692 of 726 ends are linked to one solid plus a local point. First point is on the moving part in 215 of 320 tweened lines (67 %), so point order is not meaningful.
- Exceptions: 25 lines have one end whose object id is not in the exported CAD tree (breadboard-hole ends in LAC and the LSM Full Build); 3 have a free end (LSM Part 3+4 Steps 7, 12). Mis-anchored lines: LSM D5 step ([057], Part 3 [010]) two lines anchored at the far end of a wall (133 mm for a 42 mm travel); LSM Part 4 Step 5 one line anchored to the base plate (102.8 mm).
- Why it helps students: The line starts and ends exactly on the two things that must meet, so it identifies both the feature on the part in hand and the feature on the model.
- For our player: Line ends must be defined in part-local coordinates and re-evaluated every frame from the part transforms. The CAD pipeline needs feature points (tab tip centres, slot centres, pin tips, hole axes), not just part bounding boxes.

### LL-6 · confirmed

**Make every lead line a straight segment parallel to the direction the part will travel in that stage.**

- Applies to: construction; all kits
- Evidence: 350 two-point lines with a measurable travel: median angle to travel 0.4 deg; <= 1 deg on 270 (77 %), <= 2 deg on 300 (86 %), <= 5 deg on 338 (97 %), maximum 10.7 deg. 3 full builds: 139 of 145 within 5 deg. Travel = relative movement of the two anchors to the next frame, from an exact transform replay.
- Exceptions: The 12 showings above 5 deg are rotation stages or second stages of cross-faded modules: LSM Step 25 [055] (6.0), PMG Step 41 [089] (5.1-6.1), LAC Step 52 [115] (5.6), PMG Transition [111] (8.9-10.7).
- Why it helps students: The line doubles as the motion path: students push along the line.
- For our player: If lines are generated from the same mating pair on both parts they are parallel by construction; add a validation that rejects a pair whose segment is more than about 2-5 deg off the stage's motion.

### LL-7 · qualified

**Size the line to the gap between the mating features at the hover pose, so length is about the travel (median L/T 1.00, 78 % within 15 %). Where the female end sits is not consistent: for breadboard holes it is the hole floor, 7.0-7.4 mm below the top of the 8.5 mm board (17 of 20 frames); for plywood slots it is the exit face on only a third of ends. When the line ends on the exit face of a slot, it is shorter than the travel by the tab's protrusion (3.4 mm in these kits).**

- Applies to: construction; all kits
- Evidence: 360 lines: L/T median 1.00, quartiles 0.94-1.09; within 10 % on 226 (63 %), within 15 % on 282 (78 %); T - L within +-6 mm on 273 (76 %), with clusters at 0 (72 lines within +-0.5 mm), +2.4..+5.5 mm (84) and -6..-0.5 mm (92). Breadboard-hole end depth 7.0 mm (LAC, LSM Part 1) to 7.4 mm (LSM Full Build); PMG sockets 1.9-4.9 mm. Slots crossed through their thickness (74 lines): entry face 29, exit face 30, inside 15.
- Exceptions: Axial parts are anchored on the body rather than the leading end, giving L/T 0.86-1.26 (LAC switch 69.5/81.2, pot 91.8/79.1, washer/nut/knob 1.19-1.26, PMG USB 28.5/22.9). Short marker lines where little travel remains: LSM Step 34 [075] 15.6-17.5 mm for 7.0 mm; LAC Step 46 [102] 7.3 mm for 10.7 mm. Where exactly the female end sits (mouth, far face, depth in hole) is not consistent between authors.
- Narrowed because: Slot ends (280): exit face 92, inside thickness 96, entry face 54, short of plate 18, beyond 20. Blind-hole depth exceptions: LSM Full Build Step 5 [010] (0.2-0.3 mm) and, not listed by the analyst, LSM Part 1 Step 6 [012] / Part 1+2 [011] (2.2-2.3 mm). Capacitor leads seat 8.1-8.3 mm deep, beyond the line end. Marker lines: LSM Step 34 [075] 15.6-17.5 mm for 7.0 mm; LAC Step 46 [102] 7.3 mm for 10.7 mm, practically invisible in the render.
- As first stated: Size the line to the gap between the two mating features at the hover pose: start at the male tip and end inside the female feature (exit face of a 3 mm through-slot; about 7 mm down a breadboard hole). If the male feature continues far past the receiving feature, still stop at the receiving feature. Result: length is about the travel, not a fixed copy of it.
- Why it helps students: The visible red span is exactly the distance left to close, and the line visibly enters the hole or slot; nothing red pokes out of the far side of the model.
- For our player: Generate end B as the point of the female feature on the tip's path, clamped so it never leaves the receiving part; do not hard-code 'length = hover offset'. Lines must be depth-tested so the part of the line inside material is hidden.

### LL-8 · qualified

**Three devices exist for paths that are not one straight move: a polyline through the tip's waypoints, short straight chords between closing tab/slot pairs for a swing, and fresh lines for the next stage. Stages split over two numbered steps always get their own lines (6 of 6). For two legs inside one step the choice is not consistent: polyline on 2 distinct steps, fresh lines on the auto Transition on 3 (all PMG), nothing for the second leg on 2.**

- Applies to: construction; mechanical/plywood; LSM, LAC, PMG
- Evidence: Polylines: 4 distinct lines in 2 distinct steps (10 showings in 5 guides); their end-to-end length equals total travel (44.0 vs 43.7 mm; 108.5-111.9 vs 107.0-110.9 mm). Lines on auto Transition frames: 6 frames (PMG Full Build and Part 3). No curved line exists in any guide.
- Exceptions: Lock slides of PMG H11/H12 (6.7 / 7.6 mm sideways, [093] [096]) get no line. One LAC polyline has 5 points with click artefacts at its start.
- Narrowed because: Second leg not drawn: PMG Step 42 [091]-[093] and Step 43 [094]-[096] (lock slide; residual 7.4 and 8.3 mm at the c frame). Polyline with click artefacts: LAC Step 45 [098] / Part 4 [009], 5 points with 0.1 and 4.7 mm first segments. Polyline evidence is 2 authored steps; Transition lines are 3 authored steps by one author.
- As first stated: For a path that is not one straight move: use a polyline through the tip's waypoints for a two-leg move; use short straight lines between the closing tab/slot pairs for a swing; and give each stage of a two-stage seat its own fresh lines (on the next numbered step or on the auto Transition).
- Why it helps students: Students see the actual route (up then across; hook this edge first, then close that edge) instead of a misleading straight shortcut.
- For our player: Line objects need to support more than 2 points and per-keyframe visibility (a line set per motion stage, including auto-advancing intermediate keyframes).

### LL-9 · qualified

**A wire-tethered panel or PCB that is seated by cross-fading pose copies may carry lead lines from the fixed tabs to the hovering copy, sized and aimed as if it tweened. This is done on about half of such seats (6 of 11 in the full builds; 6 of all 20 cross-faded steps); the others use an arrow or only eye icons.**

- Applies to: construction; wired sub-assemblies (LAC F4, F1, LCD; LSM matrix + D10; PMG display, dot matrix)
- Evidence: 6 of 20 cross-faded sub-assembly steps in the 3 full builds carry lines (4 carry an arrow, 10 only eye icons). For the 40 such line showings in all guides the line matches the offset to the next pose copy: L/T 0.93-1.20, angle 0-5.6 deg except PMG matrix second stage 8.9-10.7 deg.
- Exceptions: Comparable placements use an arrow instead (LSM Step 21 [046] D2 panel onto base, PMG Step 46 [101] shield onto H4) or only eye icons (buzzer LAC Step 43, button modules PMG Steps 33-34).
- Narrowed because: Cross-faded seats without lines: LSM Step 21 [046] and PMG Step 46 [101] (arrow), LAC Step 43 [094], PMG Step 33 [073] and Step 34 [075] (eye icons only).
- As first stated: When a wire-tethered panel or PCB sub-assembly is seated by cross-fading pose copies (no tween), still draw lead lines from the fixed tabs/notches to the hovering copy's slots/edges, exactly as if it were going to tween.
- Why it helps students: The student still performs a straight seating motion with their hands even though the animation cannot show it because of the wires.
- For our player: Line generation must not depend on an animated tween existing; it needs the hover pose and the seated pose of the unit, whichever way the player transitions between them.

### LL-10 · confirmed

**Style lead lines as thin solid pure-red (#ff0000) segments of constant on-screen width (5 px, not world units), with no arrowhead, end marker or dash, drawn in the 3D scene and occluded by parts in front of them.**

- Applies to: all line-carrying steps; all kits
- Evidence: Colour #ff0000 on 363 of 363 shown and all 958 defined line objects; scale 5 with world_units false on 363 of 363; measured width 2-3 px saturated core (4-5 px with anti-aliasing) on 144 renders at 2559 and 3840 px width and camera distances 173-436 mm; 353 of 363 are two-point segments.
- Exceptions: 36 showings (LSM only) are stored as 'dashed' (dash 10 / gap 5) but are drawn solid in every saved render checked; 5 'dotted' lines exist and are never shown. Red lines can sit next to red wires or the red breadboard rail (LAC [032], LSM [037]).
- Why it helps students: A hairline does not hide the small holes and slots it points at, stays legible at any zoom, and reads as 'path' rather than as another part; occlusion keeps depth cues honest.
- For our player: Render lines as screen-space-width segments (shader line or fat line with size attenuation off), depth test on. Do not implement dashes. Consider checking contrast against red parts.

### LL-11 · confirmed

**Show lead lines only on the frame that precedes the motion and switch them off as the part starts to move; 'Step Nc' never shows or introduces a lead line.**

- Applies to: all line-carrying steps; all kits
- Evidence: 359 of 363 line showings are visible for exactly one viewer frame; 0 are switched on by a Step Nc. If left on, lines would collapse to a 3.5 mm median residual because both ends follow their parts (<= 5 mm on 214 of 320).
- Exceptions: PMG Step 51 / Part 3 Step 26: two second-stage lines switched on at the auto Transition ([114] / [056]) are still flagged visible on Step 51c / 26c and are removed at Completed View; nothing red is visible in the saved render [115].
- Why it helps students: The result view stays clean so the student can compare their build with the picture.
- For our player: Line visibility is a property of the hover keyframe; the player should fade lines out in the same 800 ms as the seating tween and guarantee they are off in the completed state.

### AR-1 · qualified

**In a build, use a red arrow and no lead lines for a removal (always), for flexing parts apart (one step), and sometimes for moving a wired sub-assembly as a whole (4 of 20 cross-faded steps). Two of those four are seating steps, so arrow versus lines for a wired sub-assembly is not decided by seat versus carry.**

- Applies to: construction; removal, flexing and carry steps; LAC, LSM, PMG
- Evidence: 3 full builds: 12 arrows on 11 of 146 Step N frames; 6 of 6 removal steps have an arrow and no line; 4 of 20 cross-faded sub-assembly steps have an arrow. 16 construction guides: 29 arrow showings on 27 frames.
- Exceptions: Other hand moves use only eye icons (LAC Step 44 close posts; LSM Step 28 lift matrix); turning the knob (LAC Step 29 [063]) has an eye icon and no arrow.
- Narrowed because: Arrow used to seat: LSM Step 21 [046] (D2 panel pushed onto the base), PMG Step 46 [101] (shield lowered onto H4). Hand moves with no arrow: LAC Step 44 [096], LSM Step 28 [062], LAC Step 29 [063].
- As first stated: In a build, use a red 3D arrow instead of lead lines when the step removes, peels, spreads or carries something by hand rather than seating it on features.
- Why it helps students: An arrow says 'move it this way' when there is no specific hole or slot to aim at.
- For our player: Step schema needs an 'arrow' annotation type with tail point, direction and length, and a step kind for removal-inside-a-build (arrow frame, auto keyframe that slides the part off, result frame).

### AR-2 · qualified

**In a take-apart guide mark the part being pulled off with a red arrow on the still-assembled model and never use lead lines for removal. This covers 60 of the 67 Step N frames that take off or move something other than a single wire; single-wire unplug steps, loose parts being set aside and some pose-swap pick-ups have no arrow.**

- Applies to: deconstruction; LAC, LSM, PMG take-apart guides
- Evidence: 77 arrows on 70 frames; 60 of 94 Step N frames carry an arrow (LAC 19 of 47, LSM 21 of 24, PMG 20 of 23) plus 9 auto Transition frames in PMG. Lead lines: 3, all on LAC deconstruction Steps 16-18 [043] [045] [047] where washer, nut and knob are fitted back on. For comparison the 3 full builds show 149 lines and 12 arrows.
- Exceptions: Single-wire unplug steps have an eye icon and no arrow (LAC 20 steps, LSM Steps 11-13); PMG Steps 2, 3 have the arrow only on an auto Transition; PMG Step 12 has none.
- Narrowed because: No arrow on the paused frame: PMG Step 2 [004], Step 3 [009] (arrow on Transition only), PMG Step 12 [035]; and four the analyst did not list: LAC deconstruction Step 5 [013], Step 6 [015] (pose swaps), Step 23 [061] and Step 31 [082] (loose LCD and buzzer set aside with an eye icon). 23 single-wire unplug steps (LAC 20, LSM Steps 11-13).
- As first stated: In a deconstruction guide, mark every part that is pulled off with a red arrow on the still-assembled model; do not use lead lines for removal.
- Why it helps students: The part is still seated, so there is no gap to bridge; the arrow shows which way it comes out.
- For our player: A reversed build is not enough: the pipeline must replace each seating step's lines with one arrow along the reversed insertion axis and place it on the seated pose.

### AR-3 · confirmed

**Point the arrow along the first main motion of the part, put its tail on (or just beside) the part and its head in free space; make it roughly as long as the travel but do not rely on length to convey distance.**

- Applies to: construction and deconstruction; all kits
- Evidence: 87 arrows are followed by a motion of the part: 79 are within 12 deg of it (median about 2 deg). Length/travel for those 79: median 0.96, quartiles 0.76-1.31, 44 within 0.75-1.35. 17 arrows before a pose swap: 12 within 12 deg of the pose offset, 5 within 18-26 deg. Tail within 5 mm of the moving part on 78 of 104 (median 0.8 mm); head 42-59 mm clear (per-guide medians). Arrow length median 51 mm (10th-90th percentile 32-102).
- Exceptions: Two-stage removals: LAC deconstruction Steps 24 and 28 point along the main pull while the first stage is an unhook or straighten (65-82 deg off the first motion). Carried sub-assemblies: arrow far shorter than the move (102 mm for 184 mm and for 520 mm). LAC Step 23 [049] stored points are reversed relative to its anchors.
- Why it helps students: Tail-on-part identifies what to grab; the head in clear space is easy to see against the white background.
- For our player: Generate arrows from the removal vector: tail = a point on the part's surface facing the pull, direction = unit removal vector, length = clamp(travel, about 30, about 100 mm).

### AR-4 · confirmed

**Draw arrows as straight, flat, pure-red (#ff0000) shapes with proportions body : head width : head length = 5 : 20 : 17, sized in model space (body about 4 mm thick), not in screen pixels.**

- Applies to: construction and deconstruction; all kits
- Evidence: 106 of 106 shown arrows: sub-type straight, #ff0000, opacity 1 (all 176 defined arrow objects are straight). Proportions 5:20:17 on 74, 5:20:15 on 14 (LSM), 18 one-off variants. World size = params x per-arrow scale: body median 4.3 mm (10th-90th percentile 2.6-7.8), head width 16.7 mm, head length 14.4 mm; head length is 28 % of arrow length at the median. Head at the end on 104 of 106.
- Exceptions: Thickness is set by eye per arrow and ranges from 1.3 mm (LSM deconstruction Step 23) to 11.8 mm (PMG deconstruction Step 9); LSM Step 23 and its copies use 3:9:10; PMG deconstruction Step 4 uses 2:10:17.
- Why it helps students: A fat arrow is unmistakably different from the hairline lead lines, so 'pull/move' is never confused with 'insert here'.
- For our player: Arrow mesh defined in world units with fixed 5:20:17 proportions and one global thickness; unlit flat red material, no outline.

### AR-5 · qualified

**Never more than two arrows on a frame. One arrow per part or per sub-assembly moved as one; when exactly two separate parts are handled in a step, each gets its own arrow, including two identical parts; four or more identical parts share one arrow.**

- Applies to: construction and deconstruction; all kits
- Evidence: 97 frames with arrows: 88 with one, 9 with two, 0 with more.
- Exceptions: PMG deconstruction Step 1 [001] has two overlapping arrows for one part (duplicate).
- Narrowed because: The claimed wording "a group of identical parts shares one arrow; two arrows only for two different parts" fails on 7 of the 9 two-arrow frames, where two identical parts get one arrow each: LAC Step 42 [092], Part 4 Step 2 [003], LAC deconstruction Step 26 [070] (opposed) and Step 28 [074] (parallel), LSM deconstruction Step 6 [016], Step 7 [019], Step 10 [028]. No step moves exactly two identical parts with one shared arrow. Shared arrow: 64 stems (LSM deconstruction [001]), 4 keys (PMG deconstruction [028]), 4 button modules ([053]). Duplicate: PMG deconstruction Step 1 [001], two overlapping arrows (15.8 and 29.0 mm) on one part.
- As first stated: Use one arrow per moving unit; a group of identical parts shares one arrow; use two arrows only for two different parts or an opposed pair (spread apart). Never more than two.
- Why it helps students: One bold cue per action keeps the picture readable even when 4 keys or 64 stems come off together.
- For our player: Arrow generation works per moving unit (after grouping identical parts), not per part instance.

### AR-6 · confirmed

**Never put lead lines and an arrow on the same frame, and do not use curved or rotation arrows; rotations are shown by the animation or an eye icon only.**

- Applies to: all guides
- Evidence: Frames with both a line and an arrow: 0 in the 3 full builds and 3 deconstruction guides; 1 in all 20 guides (LSM Part 1+2 Step 20 [041], a stray 8.8 mm line left on). All 176 defined arrows are sub-type 'straight'.
- Exceptions: The single stray-line frame above.
- Why it helps students: Each frame carries one kind of motion cue, so the meaning of red stays unambiguous.
- For our player: The step schema can make 'lines' and 'arrow' mutually exclusive per keyframe; no rotation-arrow primitive is needed to match the published guides.

### AR-7 · qualified

**Show the arrow for one frame while the part is still in place and hide it as the motion starts. When the part is slid away by a tween, an auto-advancing keyframe always follows before the result frame (44 of 44); when the part simply fades out or is pose-swapped, the step goes straight to the result frame.**

- Applies to: removal steps in construction; all deconstruction steps
- Evidence: 106 of 106 arrow showings last one frame; 96 are on Step N frames, 9 on auto Transitions (PMG deconstruction second stages), 1 on a mis-named frame (LAC deconstruction [120] 'Step 45c').
- Exceptions: PMG deconstruction: the second-stage arrow is visible only during the 0.8 s auto Transition; Steps 2 and 3 have no arrow on the paused frame.
- Narrowed because: 20 of the 60 deconstruction Step N frames with an arrow have no auto Transition before the result frame (13 fade-outs, 4 tweens, 3 pose swaps). Arrow only during a 0.8 s auto Transition: 9 PMG deconstruction frames, including Steps 2 and 3 where the paused frame has none. Arrow on a frame named "Step 45c" (LAC deconstruction [120]).
- As first stated: Show the arrow on the paused frame while the part is still in place and hide it as the motion starts; for a removal, follow with an auto-advancing keyframe that slides the part away, then the result frame.
- Why it helps students: The student reads the cue at rest, presses Next, and then watches exactly the motion the arrow promised.
- For our player: Arrow visibility is tied to the hover keyframe; the player needs auto-advancing intermediate keyframes for removal motion.

### Added by the re-check

- When exactly two separate parts are handled in one step, give each its own arrow even if the parts are identical; share one arrow only for four or more identical parts or for a sub-assembly moved as one. *Evidence:* 7 of 9 two-arrow frames are two identical parts: LAC Step 42 [092], LAC Part 4 Step 2 [003], LAC deconstruction Steps 26 [070] and 28 [074], LSM deconstruction Steps 6 [016], 7 [019], 10 [028]. No frame moves exactly two identical parts with one arrow. Shared: 64 stems, 4 keys, 4 button modules, and LSM deconstruction Step 4 [010] (4 lens supports plus a side panel).
- Arrows are flat shapes laid in a world-axis plane and pointed along a world axis; they are not turned to face the camera. *Evidence:* Arrow direction within 10 deg of a world axis on 96 of 106; the stored plane normal is a world axis on 92 and perpendicular to the arrow on 98; median angle between that normal and the view direction is 49 deg (within 45 deg on only 39). Consistent with two renders where the arrow looks half as wide as predicted.
- Where a line ends on the exit face of a plywood slot, it is shorter than the travel by exactly the tab's protrusion (3.4 mm), not by the 3.0 mm plate thickness. *Evidence:* 39 lines with T - L of 3.3-3.5 mm; depth fraction 1.0 (exit face) on PMG Steps 26, 27, 28, 38, 42, 43 and LAC Steps 49, 54; 31 of 33 panel solids are 3.00 mm thick.
- All breadboard-insertion lines in a guide end on one plane, the floor of the hole, 1.1-1.5 mm above the board's underside. *Evidence:* LAC: Y = 890.1 mm on all 8 lines of Steps 3, 5, 6, 7 (board spans 888.6-897.1). LSM: Y = 864.5 mm on 8 of 10 lines in the Full Build and 8 of 10 in Part 1 (board 863.4-871.9 and 863.0-871.5).
- Lead lines and arrows carry no attention effect; arrows fade in and out explicitly. *Evidence:* animation_show and animation_hide = fade and animation_attention = none on 106 of 106 arrows; lines have no show / hide setting and animation_attention = none on 363 of 363.
- Lead lines are mostly world-axis lines, and mostly vertical. *Evidence:* 301 of 353 two-point lines lie within 10 deg of a world axis: 212 vertical, 62 along X, 27 along Z; the 52 oblique ones are hook-in and swing stages.
- The lines usually arrive with the part: the moving part fades in at its hover pose on the same frame that shows the lines. *Evidence:* 83 of 149 Step N line frames; on 62 the part was already on screen (preparation step before it, or second stage); 4 are cross-faded with no tween.
- Lead lines normally stand alone on the frame; text labels join them only for breadboard insertions, and arrows never share a frame with a text label. *Evidence:* 122 of 155 line frames carry no other annotation; 19 carry hole-name labels (all breadboard steps); 14 an eye icon or inset. 0 of 97 arrow frames carry a text label; 31 carry an eye icon or inset.
- Lines are drawn straight through whatever lies between the two features; nothing routes them around wiring, and very short ones are left in even when barely visible. *Evidence:* PMG Step 35 [077]: two 139 mm lines cross the wire loom; LAC Step 45 [098] polylines run through the wiring; LAC Step 46 [102] 7.3 mm line is a few pixels in the render.
- Anomaly, not a convention: frame names around arrow steps are unreliable, so a player must not key behaviour on the names. *Evidence:* "Ttansition" after LAC Step 24 [052] and Part 2 Step 10 [022]; "Transititon" and "Transiton" in deconstruction guides; "Step 20C" (LSM Part 1+2); an arrow on a frame named "Step 45c" (LAC deconstruction [120]); LAC deconstruction "Step 41" [104] followed by "Step 40" [105].
- Anomaly: the line width property changes type between projects. *Evidence:* scale is the number 5 on 819 line objects and the string "5" on 139 (the same split appears among dashed lines: 22 and 40).

### Numbers (as corrected by the re-check)

| Setting | Value | Basis |
|---|---|---|
| lead_line_colour | #ff0000 (confirmed) | 363 of 363 shown; all 958 defined line objects |
| lead_line_style | solid straight segment, no arrowhead or end marker (confirmed) | 327 stored solid, 36 stored dashed; all 14 frames holding dashed-stored lines show 0 gaps along every line at full resolution; 353 of 363 are two-point |
| lead_line_width | 5 px in render pixels, constant; not a share of the viewport | scale 5 and world_units false on 363 of 363; measured 5.1-5.3 px (area / length; saturated core 3.2-3.4 px) on 123 renders at 2559, 2560 and 3840 px width alike, which is 0.20 % of width at 2559 px but 0.13 % at 3840 px. Whether these are CSS or device pixels is not known |
| lead_line_depth_test | on (confirmed) | LAC [004] rear line hidden by the breadboard; LAC [055] line vanishes behind the panel and reappears in the hole |
| lead_line_frames_visible | 1 (confirmed) | 359 of 363 one viewer frame; 4 two frames (PMG Step 51 / Part 3 Step 26); 0 switched on by a Step Nc |
| lead_lines_per_frame | 1, 2 or 4 (confirmed) | 153 of 155 frames: {1: 37, 2: 75, 4: 41}; 6 on 2 frames |
| lines_axial_part / lines_two_lead_component / lines_flat_body_on_plate | 1 / 2 / 4 (confirmed) | 24 of 24, 13 of 13, 5 of 5 frames by my own classification |
| lines_pin_header_board | 4 corner pins, or 2 diagonal corners, or both end pins of a single row (confirmed) | 9 frames {4: 5, 2: 4}; anchor spans 38.8 mm (LAC Nano diagonal), 15.2-15.6 x 35.0-35.6 mm (LSM, PMG Nano), 12.3 mm (RTC); only 5 distinct authorings |
| lines_plywood_panel | 1, 2 or 4 per frame; no verifiable selection rule | 86 frames {1: 12, 2: 45, 4: 27, 6: 2}; the "2 on each of two neighbours" clause rests on LAC F5 and F6 only and is contradicted by LSM D5 (6) and PMG H8, H11, H12 |
| line_parallel_to_travel_tolerance | 2 deg target, 5 deg limit (confirmed) | 345 two-point lines: median 0.30 deg; <= 1 deg 266 (77 %), <= 2 deg 299 (87 %), <= 5 deg 334 (97 %), maximum 10.7 deg |
| line_length_over_travel | 1.00, accept 0.85-1.15 (confirmed) | 355 lines: median 1.000, quartiles 0.94-1.09; 222 within 10 % (63 %), 276 within 15 % (78 %) |
| line_stop_short_at_through_slot | end the line on the slot's exit face; it is then shorter than the travel by the tab's protrusion, 3.4 mm in these kits | 82 lines with T - L in 2.4-5.5 mm, 39 of them in the 3.3-3.5 bin; on PMG Steps 26, 27, 28, 38, 42, 43 and LAC Steps 49, 54 the end sits exactly on the exit face. Plates are 3.0 mm, so 3.4 is protrusion, not thickness. Only 92 of 280 plate-crossing ends are on the exit face (96 inside, 54 entry face) |
| line_end_depth_in_blind_hole | 7.0-7.4 mm below the top of the 8.5 mm breadboard (the hole floor, 1.1-1.5 mm above its underside) | 17 of 20 breadboard-insertion frames: LAC 8 of 8 at 7.0, LSM Part 1 and 1+2 at 6.7-7.0 on 3 of 4 steps each, LSM Full Build 7.4 on 3 of 4. Exceptions: LSM Full Build Step 5 (0.2-0.3 mm) and LSM Part 1 / 1+2 Step 6 (2.2-2.3 mm). PMG sockets differ (line ends spread over 3 mm) |
| line_residual_if_left_on_when_seated | 3.5 mm median (confirmed) | 318 tweened lines: median 3.48 mm; <= 5 mm on 214 |
| plywood_thickness | 3.0 mm (confirmed) | smallest bounding-box dimension of 33 panel solids in the 3 full builds: 3.00 on 31, 3.18 on LSM_Side1 and LSM_Lens_Top |
| travel_by_class | 2-lead 32.9 (29-40); pin-header 35.3 (30-44); breadboard onto base 46.9 (39-49); axial 60.9 (23-103); plywood 64.4 (7-139); wired module 11.1 (8-23); wired panel 57.2 (50-77) mm (all confirmed) | medians and ranges recomputed per class from my own travel replay; every value within 0.5 mm of the claim |
| polyline_for_two_leg_path | 3 points (confirmed), used on 2 of the 4 distinct in-step two-leg moves | 10 showings, 4 distinct lines, LSM Step 29 and LAC Step 45; 2 showings have 5 points from click artefacts; PMG Steps 42 and 43 draw the first leg only |
| arrow_colour_and_type | #ff0000, opacity 1, straight, flat (confirmed) | 106 of 106 shown; all 176 defined arrows are straight |
| arrow_proportions_body_headwidth_headlength | 5 : 20 : 17 (confirmed) | 74 of 106; 5 : 20 : 15 on 14; 11 other combinations on 18 |
| arrow_world_size_mm | body 4.3, head width 16.7, head length 14.4 (confirmed) | medians 4.27 / 16.67 / 14.38; body 10th-90th percentile 2.58-7.58 (claimed 7.8), range 1.28-11.80 |
| arrow_length | 51 mm median; 10th percentile 32 mm; 95 of 106 arrows are 86.5 mm or shorter, the other 11 are 102-116 mm | median 50.7, min 15.8, max 116.1. The 90th percentile falls in an empty gap between 86.5 and 101.7 mm, so the claimed 102 is one reading of it and 87 the other |
| arrow_length_over_travel | about 1.0 (0.92 to 1.05 depending on definition), quartiles about 0.75-1.35 | 83 aligned arrows: 1.05 (0.79-1.39) against the first stage of motion, 0.92 (0.73-1.17) against net travel to the next paused frame; 45 of 83 within 0.75-1.35; range 0.4-12.9 |
| arrow_direction_vs_motion | within 12 deg (median 1.7 deg) on 83 of 88 | each arrow matched to its nearest moving solid; the claimed 79 of 87 counts the second arrow of an opposed pair as a miss |
| arrows_per_frame | 1; 2 when two separate parts are handled, identical or not; never more | 88 frames with one, 9 with two; 7 of the 9 are two identical parts with one arrow each |
| arrow_tail_to_part_distance | on the part: median under 1 mm (method-dependent) | 0.1 mm median and 98 of 106 within 5 mm by bounding-box distance to the nearest moving or leaving solid; the analyst's 0.8 mm and 78 of 104 use a stricter measure. Head clearance medians per guide 36-52 mm by the same box measure (claimed 42-59) |
| arrow_frames_visible | 1 (confirmed) | 106 of 106 |

### Open questions

- Dashed flag: 36 line showings (LSM only) are stored as 'dashed' yet every saved render shows them solid. Does the live viewer draw them dashed? I could not open the viewer; treat solid as the convention unless TechBox confirms otherwise.
- Do lead lines shrink with the part during the 800 ms seating tween (both ends are linked to parts, so the data implies they follow) or do they simply fade? Not observable from saved frames.
- Line width: 'scale 5' measures about 4-5 px on renders saved at 2559 and 3840 px wide. Is that 5 CSS px or 5 device px? The device pixel ratio of the authoring machine is unknown, so the on-screen thickness at 1x could be 2.5 px or 5 px.
- Is 4 an intended maximum for lines per step? The same LSM wall step has 6 lines in Part 3 and Part 3+4 but 4 in the Full Build; no step anywhere has 3 or 5.
- Pin headers: is the intended rule 4 corner pins (LSM, PMG) or 2 diagonal corners (LAC)? Both exist for the same Nano board.
- For wire-tethered sub-assemblies that are cross-faded into place, what decides between lead lines (6 steps), an arrow (4 steps) and eye icons only (10 steps)? The split is not predictable from geometry (e.g. LSM D2 panel onto the base uses an arrow although it has tabs).
- Where should the receiving end of a line sit: at the mouth of the hole/slot, at the far face, or about 7 mm down a breadboard hole? All three occur; they look the same because the buried part is hidden, so this may simply be hand placement.
- When stored line points and part-link anchors disagree (LSM D6 step in three guides, LAC potentiometer line), which does the viewer draw? Lengths in the report use the anchors; the renders are consistent with either for the LSM case.
- Are arrows true 3D solids or camera-facing flat shapes? They render as flat unlit red in every frame inspected; the data only gives body/head sizes and segment counts.
- USB plugs: PMG shows the plug hovering with an axis line and a tween; LAC and LSM just fade the routed cable in with an eye icon on the socket. Which treatment should the TechBox player use?
- Per-arrow thickness varies about ninefold in model space (1.3 to 11.8 mm). Should the player use one fixed thickness (median 4.3 mm) or scale arrows with the part or the camera distance?

## Labels, eye icon, image callouts and section cards

### LBL-1 · confirmed

**Draw every text callout in one house style: bold black sans text centred over a light-blue #7fdbff rule (no box, no fill), a single straight #7fdbff leader of the same thickness leaving the end of the rule nearest the target, ending in a dashed #7fdbff ring ('life-saver' ring of four arc segments) centred on the exact feature. No arrowhead, no elbow.**

- Applies to: construction + the one deconstruction that uses labels; all three kits (LSM, LAC, PMG); wiring steps and rigid breadboard insertions
- Evidence: 214 of 223 label showings (122 distinct placements) use it. Underline container 214/214; colour #7fdbff 214/214; thickness 5 px on 212, 6 px on 2; text black bold 214/214; leader straight solid #7fdbff 214/214 (field-wise replay of raw data); ring 'Life Saver Circle' 214/214, size 1.2 on 203 and 1.0 on 11; box 175x90 px on 143, 175x75 px on 25, wider (195-258 px) for long texts. Font size 3em on 175 (LAC 84, PMG 84, LSM FB 7), 2.5em on 39 (LSM only). Font family Arial explicit on 126, unset (project default Public Sans Medium) on 88 (all PMG, LAC Deconstruction). Render-measured ratios: cap height / underline length 0.24-0.25 at 3em, 0.20 at 2.5em; text-to-rule gap 0.55 x cap height; text centre = rule centre within 0.2 % of width.
- Exceptions: Quantity labels (7 showings) and the PMG framed photo label (2) use other styles. LSM 'c16' has thickness 6. The 'leader colour missing' reported by several per-guide readers is a digest artefact (digest overwrites the whole leader dict); 0 labels actually lack it.
- Why it helps students: One unmistakable visual for 'this text names that exact hole or pin'; light blue never competes with red motion guidance or with part colours; the ring shows the precise hole without hiding it.
- For our player: Implement one label component: text + rule + leader + ring, all sized from one font-size token (rule length about 2.9 x font size, box height 1.5 x, stroke = font size / 12, ring diameter 0.6 x). Leader start must switch automatically between left and right rule end depending on which side the projected target is on. Pick one font and one size (3em equivalent) and do not reproduce the 2.5em / Arial-vs-default drift.

### LBL-2 · qualified

**Label text is only a destination identifier as printed on the hardware. Hole and pin identifiers are 2-3 characters (breadboard hole lower-case letter + number; module and shield pins in capitals). Power-rail labels are the exception in length: '(+) red' / '(-) blue', 7-8 characters, and they widen the rule to 9.2-11.7 % of width. Never a sentence, verb, part name, wire colour or step number.**

- Applies to: construction wiring and breadboard steps; LSM, LAC (breadboard vocabulary), PMG (shield vocabulary); LAC deconstruction pin labels
- Evidence: 214 labels: breadboard hole lower-case 92 (LSM 44, LAC 48); rail 24 (LAC; '(-) blue' 14, '(+) red' 10); module pin capitals 50 (LAC 12, PMG 38); shield pin capitals 38 (PMG); lower-case pin outliers 8 (PMG clk, dio, s8, s9); word + pin 2 (LSM 'Pin d12'). Length: 2-3 characters on 188/214; max 8.
- Exceptions: Anomalies, not conventions: PMG 'clk/dio/s8/s9' lower case (8 showings) against capitals everywhere else; 'Pin d12' is the only label with a word; PMG Step 10 says 'S5' where S6 is meant; LSM badge text 'V-In'. The colour word in a rail label names the rail stripe, not the wire.
- Narrowed because: The rule says '2-3 characters' but 26 of 214 showings (12 %) are 7-8 characters, 24 of them the rail labels the same rule defines. Anomalies confirmed as listed: 'clk','dio','s8','s9' (PMG Part 2 [004],[006]; FB [037],[039]); 'Pin d12'; 'S5' for S6 (PMG FB [023]).
- As first stated: Label text is only a destination identifier, 2-3 characters, written as it is printed on the hardware: breadboard hole = lower-case row letter + column number (c15, i23); power rail = polarity in brackets + stripe colour ('(+) red', '(-) blue'); module and shield pins = silk-screen name in capitals (GND, VCC, SDA, SCL, OUT, DIN, CS, CLK; V4, S4, G4). Never a sentence, verb, part name, wire colour or step number.
- Why it helps students: Students match the label to text they can physically read on the board, so there is nothing to translate; very short text stays legible at classroom distance and needs no reading skill.
- For our player: Authoring schema should store a destination id per wire end (hole, rail, pin) and generate the label text from it with fixed case rules, rather than free text. Validate against the board definition to catch errors like S5/S6 and mixed case.

### LBL-3 · confirmed

**Show one label per wire end the student places in this step and no more than two labels on screen; show labels only on the instruction view (Step N) and clear them on the result view.**

- Applies to: construction wiring; all kits
- Evidence: 126 label-carrying Step N views: 1 label on 38 (LAC 20, LSM 18), 2 labels on 88 (LAC 32, LSM 14, PMG 42), never 3+. Standard labels on Step Nc 0/424, Transition 0/117, cards 0, Start 0, end views 0. In the three full builds all 48 wire-connection steps have a destination callout for every end being placed: loose jumper both ends 33/33 (2 labels), pre-attached lead 8/8 (1 label), LSM single-end steps 6/6, LSM two-lead step 1/1.
- Exceptions: In LSM female-end steps the destination pin is named by a disc-badge pair and the single label re-identifies the wire by the hole it already occupies. LAC '2x' quantity label is the only label that persists into a c view.
- Why it helps students: The student never has to choose among callouts: each visible label is a thing to do now. Two is the most that can be read at a glance, and a clean result view makes checking the real build easy.
- For our player: Derive labels from the step's connection list: one per end placed, hard cap of two per step (split the step otherwise). Labels belong to the hover/instruction phase only and must be removed automatically when the step's result phase starts.

### LBL-4 · confirmed

**Anchor the label's ring to the exact feature, not to the part: the individual breadboard hole, the individual header pin, or the pin position on the shield strip. On rigid-part steps the ring sits on the hole where the red lead line ends.**

- Applies to: construction; all kits
- Evidence: Link targets of 214 labels: breadboard hole 95 (LAC 72, LSM 23); wire connector housing 24 (LSM 21, LAC decon 3); module header pin / socket 51 (LAC 9, PMG 42); shield header strip 42 (PMG); Nano pin row 2. Linked to a wooden panel, a wire body or a whole part: 0/214. One 3D link per label 214/214.
- Exceptions: LSM anchors hole labels to the wire's connector housing on wire-end steps (21 showings) instead of the hole; the LSM Full Build moved the far-end labels to the hole. PMG shield-side rings land within about one pin (per-guide reader: 6 of 9 on the exact strip).
- Why it helps students: The ring replaces counting holes: the student sees the one hole or pin, and on insertion steps the red line and the blue ring agree on the same hole.
- For our player: Board definitions need addressable sub-features (each hole, rail position and header pin with a 3D point). The label's leader tip is that point projected every frame; do not anchor to part centroids.

### LBL-5 · confirmed

**Place labels in white space outboard of the model: never over the model, never with the target underneath the label, normally above the target, never in the bottom third of the frame; the leader then runs diagonally inward and down to the feature.**

- Applies to: construction; all kits; measured on ~2:1 frames
- Evidence: Sample 170 label showings with the underline located in the render. Leader from nearest rule end 170/170; target horizontally outside the rule span 170/170; label further from the vertical centre line than its target 164/170; label above target 150/170 (88 %); underline-to-target drop median 8.8 % H (quartiles 4.7, 11.5); horizontal gap median 14.5 % H; leader length median 19 % H (quartiles 14, 23; range 3-44); leader angle median 35 deg (quartiles 23, 43). Label centre x 21-74 % W; underline y 13-66 % H, 0/170 in the bottom third. White-space test: 196/200 labels have <2 % coloured pixels under the text (max 4.7 %).
- Exceptions: 20 labels sit below their target: LAC h27/h29, j4, the four LCD pin labels (two guides each) and PMG V11/G11/S11/S12/S13 + one VCC. The white-space pixel test cannot detect overlap with white parts, though none was seen in about 45 frames viewed.
- Why it helps students: Text on clean white is readable from a distance; keeping labels outside and above leaves the work area unobscured and gives every leader a similar, predictable slant.
- For our player: Needs a label-placement solver: project the target, find free screen area outside the model's silhouette on the same side as the target relative to screen centre, prefer above, forbid the bottom third and any overlap with model pixels, keep leader 14-23 % of viewport height at 23-43 deg. Allow author override per label.

### LBL-6 · qualified

**With two labels, either flank the model or stack both on one side; the left label owns the left-most target, the upper label the upper target, and leaders never cross. A label does not keep a fixed slot through a run: it follows its target, and the arrangement switches between stacked and flanking as targets move. Only a label for a fixed connector repeats its slot.**

- Applies to: construction wiring and two-lead components; all kits
- Evidence: 66 two-label steps in the sample: flanking 37 (56 %), stacked 29 (18 right, 11 left). Leaders cross 0/66. Left label owns left-most target 37/37; upper label owns upper target 29/29. Stacked underlines 9-38 % H apart (median 15). Slot stability, e.g. PMG button block: module label x 51-67 %, y 25-34 %; shield label x 56-65 %, y 41-52 %; LAC LCD block pin label x 19-21 %, y 48-51 %.
- Exceptions: None found for crossing or ordering. Slot drifts a few percent as modules are added further right (PMG).
- Narrowed because: Slot clause fails. LAC FB six-jumper run: [019],[021] stacked right, [023],[025] flanking, [027],[029] stacked left. PMG button block [007]-[032]: module label left edge 50.6 to 66.1 % W (15.5 % of width, not 'a few percent'), rule y 32-41 %; shield label 55.9-65.2 %, y 50-59 %. Stable case: LAC LCD pin labels [079]-[085], left edge 18.8-20.4 %, rule y 55.9-59.3 %, while the board-side label moves 68.5 to 55.3 %.
- As first stated: With two labels, either put one on each side of the model or stack both on one side; the left label must own the left-most target, the upper label the upper target, and leaders must never cross. Keep the same label slots through a run of similar steps.
- Why it helps students: Label order mirrors target order, so the eye never has to untangle crossing lines; a stable slot lets students find the label instantly on the next wire.
- For our player: The placement solver must treat the two labels jointly (order constraint + non-crossing test) and should reuse the previous step's slots when the camera has not moved.

### LBL-7 · qualified

**When a two-lead part plugs into a breadboard, label the hole for each lead beside the two red lead lines (5 authored steps, LAC and LSM). For multi-pin parts the two-end-holes form is LAC practice only (Nano c15/g1, RTC j24/j19); LSM names one pin and its hole, or gives no label. Never label every pin.**

- Applies to: construction, breadboard kits (LSM, LAC)
- Evidence: Full builds: 7 Step N views carry '2 labels + lead lines' (LAC 4/4 breadboard insertions, LSM 3). Label + lead-line co-occurrence 7 of 55 label steps.
- Exceptions: LSM Full Build Step 3 (Nano) has lead lines but no labels (Part 1's version has two). PMG's Nano-onto-shield step has lead lines only (no hole names exist on a socket strip).
- Narrowed because: LSM Part 1 [005] / Part 1+2 [005] Step 3: 4 lead lines, labels 'Pin d12' + 'c16' (one pin name plus one hole, not two end holes). LSM FB [006] Step 3: 4 lead lines, no label. So for multi-pin parts the rule is 2 of 4 authored cases, both LAC.
- As first stated: When a rigid part plugs into a breadboard, add two hole labels naming the two extreme holes (the same two holes the red lead lines go to); do not label every pin.
- Why it helps students: Two reference holes fix the position and orientation of a many-pin part; labelling all pins would bury the picture.
- For our player: For breadboard-mounted parts the authoring data needs the two reference pins and their holes; the player renders lead lines and labels from the same pair.

### LBL-8 · confirmed

**State a repeat count with a bare quantity cue beside the isolated part ('2x', '64X'): very large bold coloured text, no rule, no leader.**

- Applies to: construction prep steps and cards; LAC, LSM (PMG uses a picture with '3x')
- Evidence: 7 text showings (3 distinct): Arial bold 6em (twice the label size), no container, no leader; position about (53-54 %, 12-22 %), upper right of the part. Colour #0074d9 (LAC) or #7fdbff (LSM).
- Exceptions: Inconsistent form: '2x' / '64X' / '64x' / '3x' inside an image; two different blues; '2x' persists into the c view. PMG buttons 2-4 get no quantity cue at all (eye only).
- Why it helps students: Says 'do this to all of them' without animating every copy.
- For our player: Provide a quantity badge primitive (count + 'x') with one fixed style; attach it to steps flagged as 'repeat n times'.

### EYE-1 · confirmed

**Use one text-free pointer, the black eye icon: about 8 % of viewport width, no frame, with a straight #7fdbff leader that leaves the glyph on the side facing the target and ends in the same dashed ring as labels. One per step, two at most.**

- Applies to: construction, deconstruction and section cards; all kits
- Evidence: 226 showings, 140 distinct placements, one PNG asset shared by all 20 projects. Width 7.81 % W on 144 (LAC, LSM), 8.2 % on 62 (PMG), 20 outliers 6.29-9.37 %. Square image, glyph fills the width and the middle 55 % of the height. No container 225/226; leader #7fdbff 226/226, 5 px on 224; ring #7fdbff 223/226; no text 226/226; leader start faces the target 217/217 (PMG: always the eye's left or right corner, 58/58). 1 eye on 208 steps, 2 eyes on 9, never 3. Fade in/out 226/226.
- Exceptions: One boxed eye (LSM Deconstruction Step 4); teal ring #39cccc on 3; eye baked into two LSM inset pictures and into the LED Matrix Diagram picture rather than placed as an annotation.
- Why it helps students: A wordless 'look at / pick up this' that is language-independent and visually distinct from red motion cues and from text labels.
- For our player: Ship the eye as a built-in pointer primitive sharing the label's leader and ring code; size it relative to the viewport like labels (eye width about equal to a label's rule length).

### EYE-2 · qualified

**The eye is the usual cue, not the invariable one, where no part hovers along lead lines: 79 % of such instruction views in the full builds and about half of deconstruction steps. The alternative is a bare red arrow for a hand move. Never on Transitions, title or end views; rarely (8 %) beside lead lines, and then as an orientation check.**

- Applies to: construction and deconstruction; all kits
- Evidence: 210 of 226 on Step N (build 161, deconstruction 49), 9 on cards, 7 on Step Nc, 0 on Start/Transition/end. Full builds (146 Step N): eye on 71; of 84 views without lead lines 66 have an eye (79 %); of 62 with lead lines 5 do (8 %). Eye co-occurs with labels on 42 (all 33 loose-jumper steps of LAC and PMG and all 8 pre-attached-lead steps). All 217 eye steps: alone 90, + 2 labels 66, + 1 label 22, + arrow 23, + lead lines 13, + inset only 3.
- Exceptions: LSM wire steps use labels (or discs) without an eye (7 steps in the Full Build); PMG ribbon-prep Step 15 has no eye though its twin Step 2 has; arrow-only steps (7 in full builds, 41 in deconstructions) have none. The two meanings 'pick this up' and 'check this' look identical.
- Narrowed because: No eye and no lead lines on 18 build steps: arrow only LAC FB [046],[049],[052],[092], LSM FB [034],[046], PMG FB [101]; LSM wire steps [021]-[032], [041]; inset steps LAC [001], LSM [001], PMG [085]; empty PMG [035]. 41 arrow-only deconstruction steps. Eye beside lead lines: LAC FB [004],[102], LSM FB [013],[075], PMG FB [113].
- As first stated: Put the eye on the instruction view whenever the thing to act on is not shown by a part hovering along red lead lines: on the loose wire or lead end to pick up (together with its destination labels), on an identifying feature of a part shown alone, on a pre-wired module to pick up, on a mating spot to check, or in take-apart steps on the plug or catch to release. Do not use it on insertion steps that already have lead lines, on Transitions, or on title/end views.
- Why it helps students: Wires and re-posed sub-assemblies are cross-faded, not animated, so nothing moves to show which item is meant; the eye fills that gap and tells the student what to find before acting.
- For our player: Step schema needs an optional 'attention target' (part or feature). Auto-suggest it for every step whose result is a model swap rather than a tween (wires, re-posed modules) and for prep/inspect steps; suppress it when lead lines are present unless the author asks for an orientation check.

### EYE-3 · qualified

**Place the eye in free white space typically 15-35 % of viewport height from its target (77 % of cases; full range 11-57 %), usually above or beside it, no fixed corner. Unlike labels it may sit in the bottom third. On wire steps it sits below the labels, next to the staged wire, and stays within about 3 % of width through a run.**

- Applies to: construction and deconstruction; all kits
- Evidence: 218 icons with render-verified position: eye-centre-to-target distance median 23 % H (quartiles 19, 28; range 11-57); with labels median 20 %, alone 26 %. Direction from target: above (any upper sector) 121 (56 %), level 50, below 47; left 125, right 93; PMG upper-left 32/58. Eye centre x 17-81 %, y 6-76 %. On white: 210/218 have <2 % coloured pixels under the glyph.
- Exceptions: Overlaps the shield on PMG display Step 2 / Step 16 (14-19 % coloured pixels). 8 of 226 stored positions disagree with the saved picture (stale data or stale picture).
- Narrowed because: Outside 15-35 %: 30 closer and 21 further (51 of 218). Bottom third: 32 centres, e.g. LAC FB [074],[079]-[085],[113], PMG FB [037],[046]-[054], LSM Deconstruction [010],[013],[019]. Slot drift: PMG display wires [037]-[054] x 28.1-45.4. On the model: PMG FB [037] / Part 2 [004] (13-14 %), LSM FB [051] (5.7 %).
- As first stated: Place the eye in the nearest free white space 15-35 % of the viewport height from its target, off the model, usually above or beside the target on the side away from the rest of the assembly; there is no fixed screen corner. Keep it in the same slot through a wiring run.
- Why it helps students: Close enough that the short leader is read instantly, far enough not to cover the part; a constant slot beside the wire staging spot makes the 'next wire' cue predictable.
- For our player: Reuse the label placement solver with a distance band of 15-35 % H and no side preference beyond 'free space, prefer above'; pin the slot while camera and staging spot are unchanged.

### EYE-4 · confirmed

**A result view (Step Nc) may carry one check cue, an eye or a framed close-up, only when the student must verify a seated detail that is easy to get wrong (wires through a notch, a tab locked in its slot); otherwise the result view stays clean.**

- Applies to: construction, mechanical / enclosure steps; all kits
- Evidence: Step Nc with any 2D annotation 23 of 424 (5.4 %): 14 inset showings (6 pictures), 7 eyes, 2 carried-over '2x'. 401 of 424 are clean.
- Exceptions: '2x' on LAC 4c is a carry-over, not a check. Stray 3D items on c views (PMG 26c / 51c lead lines, one misnamed LAC deconstruction frame) are authoring slips.
- Why it helps students: Turns the result picture into a self-check at exactly the joints where a silent mistake would block later steps.
- For our player: Result phase supports an optional single 'verify' callout (eye or inset) distinct from instruction callouts; default is none.

### IMG-1 · qualified

**Show a close-up or reference picture tied to a feature as a framed inset: white rounded rectangle, 5 px #7fdbff border, straight #7fdbff leader and dashed ring, usually (17 of 22 pictures) with a thin red rectangle on the detail. Keep its centre in the top or middle third; the frame itself may reach about 80 % of height. A picture that replaces the 3D view (LSM LED Matrix Diagram) is unframed and full-frame.**

- Applies to: construction, deconstruction, cards; all kits
- Evidence: 45 showings, 22 distinct pictures. Frame rectangle #7fdbff thickness 5, corner radius 0.1 on 43/45; leader thickness 5 on 44/45; ring #7fdbff 41/45; one 3D link 45/45. Width: step insets median 16 % W (7.8-24.8), card insets median 31 % W (17-37). Placement by centre: right-middle 21, left-top 11, left-middle 6, right-top 6, centre 1; 0 in the bottom third. Red highlight rectangles inside 17 of 22 pictures. Alone on the step 24/45; with arrow 14, with lead lines 4, with eye 10.
- Exceptions: PMG 8c/33c frame is #7fb9ff thickness 2; PMG Push Buttons ring is orange #ff5F0B; LSM Part 1 Capacitor leader is 2 px; some frames are clipped in 2.79:1 pictures; 4 stored inset positions are stale (LSM FB 34c, Part 3+4 14c, PMG FB 38c and Step 39).
- Narrowed because: Frame extends into the bottom third on 11 of 35 (bottom edge 70-81 % H): LAC FB [001],[101], LAC Part 1 [001], Part 4 [012], LAC Deconstruction [063], LSM FB [001],[076], Part 3+4 [031], Part 4 [017], PMG FB [006], Part 1 [006]. Unframed explanatory picture: LSM LED Matrix Diagram (FB [027], Part 2 [009], Part 1+2 [025]). Off-style as listed: PMG 8c/33c #7fb9ff/2, Push Buttons orange ring, LSM Part 1 Capacitor 2 px leader. The report's '112 non-eye image showings' should be 104.
- As first stated: Show any explanatory picture as a framed inset: white rounded rectangle with a 5 px #7fdbff border, a straight #7fdbff leader and dashed ring tying it to the feature on the 3D model, and thin red rectangles inside the picture marking the exact detail. Keep it in the side or top margin, never in the bottom third.
- Why it helps students: Shows what the main camera cannot (hidden face, tiny slot, real silk-screen text) without changing the main view, and the leader keeps the student oriented about where on the model the detail is.
- For our player: Inset primitive = image + frame + leader/ring to a 3D feature. Support authored highlight rectangles as overlay data instead of baking them into the bitmap, and a default width of about 16 % of viewport width for step insets and about 30 % for card photos.

### IMG-2 · confirmed

**Choose the inset content by purpose: a real product photo with the pin names boxed in red on a module's section card; a close-up render in the guide's own style on a step (hidden face or orientation aid on the instruction view, lock or routing check on the result view); in take-apart steps a close-up of the latch or tab to release.**

- Applies to: construction (cards and steps) and deconstruction; all kits, deconstruction mainly LSM
- Evidence: By step class: cards 10 (+2 framed photo labels), build Step N 11, build Step Nc 14, deconstruction Step N 10 (LSM 8 of 24 steps, LAC 2 of 47, PMG 0 of 23). Pin names on the LCD photo = the 4 labels of the next 4 steps; VCC/OUT/GND on the button photo = module-side labels of the next 12 PMG steps.
- Exceptions: LSM capacitor card uses a labelled diagram rather than a photo; 'Protective Backing' carries its own caption; PMG Step 39 uses an inset as a '3x' quantity cue.
- Why it helps students: The photo links the cartoon model to the physical board the student is holding and previews the pin names used by the next labels; the close-up proves what 'done' looks like.
- For our player: Asset pipeline needs a per-module pinout photo with a highlight region, plus a way to render close-up stills from the model for detail insets.

### IMG-3 · confirmed

**(LSM only) Name an off-board pin with a matched pair of round badges carrying the same text: a #7fdbff-filled disc with a leader to the pin and a white disc with a leader to the free wire end.**

- Applies to: construction wiring, LSM female-end steps only
- Evidence: 18 showings on 9 steps (3 authored steps x 3 guides). Diameter 5.8-7.8 % W; leader #7fdbff 5 px with ring; 12-27 % H from the target. LAC and PMG (authored later) name module pins with ordinary underline labels instead: 50 showings.
- Exceptions: Disc size inconsistent (7.81 % vs about 6 %); text 'V-In' is not a pin name. Not used in LAC or PMG.
- Why it helps students: Shows 'this end goes on that pin' as a visual match of two tokens.
- For our player: Do not build a separate badge primitive; use the standard label on the module pin (the later kits' convention) unless TechBox confirms it wants the disc pair.

### IMG-4 · confirmed

**Title page: logo image top-left, title block image (kit name, part, copyright) bottom-left, both left-aligned at about 2 % from the edge, unframed and without leaders, finished model in the right half; nothing else. Remove both on the first step.**

- Applies to: all guides with a Start step (19 of 20); all kits; construction and deconstruction
- Evidence: 19/19 Start steps carry exactly 2 images and no other annotation. Logo x 1.8-2.5 %, y 4.0-8.1 %, width 33.2-39.5 % W (bottom at 22-29 % H). Title x 1.6-2.5 %, y 61.0-64.6 %, width 42.1-48.4 % W (bottom at 80-89 % H). No container, no leader, no link 38/38.
- Exceptions: PMG Deconstruction offsets them to x 3.8-5.1 % and the title collides with the model; LSM Part 1 title image is a taller padded bitmap (y 24 %, width 58 %). Text is baked into PNGs. LAC Electronics has no title page.
- Why it helps students: A consistent cover that shows what the session builds and which part of the series it is.
- For our player: Title page is a fixed template with two slots (logo, title block rendered from metadata as live text) anchored to the left margin, and the model framed in the right half.

### CARD-1 · qualified

**Introduce a module or cable that has something to identify (pin names, polarity, connector, a count) with an unnumbered section card directly before its first use: the component alone on white, at most one eye and one framed picture (or a quantity label), pause, no motion, no title on canvas. Basic components (breadboard, Nano, resistors, jumper wires, potentiometer, LSM push button) and all wood get no card.**

- Applies to: construction, electronics sections; all kits; not used in wood-only parts or deconstructions
- Evidence: 31 card showings in 12 build guides, 14 distinct titles; 0 in the 3 deconstructions and in LSM Part 3, LAC Part 4, PMG Part 3. Content by showing: framed picture 12, eye only 7, quantity label 3, full-frame flat diagram 3, no annotation 6. By title: picture 6, eye only 3, quantity 1, diagram 1, nothing 3. Camera moves on 29/31; behaviour pause 31/31; card name drawn on canvas 0/31.
- Exceptions: Uneven coverage: Rocker Switch and both USB Cable cards are bare; potentiometer, Nano, breadboard, resistors and all wood get no card; LSM 'LED Matrix Diagram' shows no 3D part at all; when the isolated part needs preparing the isolated view is a numbered step instead.
- Narrowed because: Cards occur in 13 guides, not 12 (16 build guides minus LSM Part 3, LAC Part 4, PMG Part 3). No card for about half of the bought-in component types: breadboard and Nano and jumper wires in every kit, resistors (LSM, LAC), LAC potentiometer, LSM push button. Not 'alone': LSM LED Matrix Diagram shows no 3D; LAC Rocker Switch and Alarm Buzzer show the part with its leads (7 and 5 components).
- As first stated: Introduce a new bought-in component with an unnumbered section card directly before its first use: the component alone on white in a close view, with at most one eye icon and one framed reference picture (or a quantity label), no motion and no title drawn on the canvas.
- Why it helps students: Gives a 'find this in the kit' moment and shows where the pins are before any wire asks for them.
- For our player: Card is a step type: isolate one component, optional attention target, optional pinout photo, optional quantity. The player should show the card's name itself (step title UI), since Cadasio shows it only as the step name.

### TXT-1 · confirmed

**Carry no instruction text outside the canvas: no popups and no step descriptions; put student-facing part names in hover tooltips (one name per kit item, 'Role - Part ID' for wood) and rely on IDs engraved on wooden parts.**

- Applies to: all 20 guides
- Evidence: Popups 0/1037 steps. Descriptions 55/1037: 52 authored, all in the three oldest LSM guides (Part 1: 6, Part 2: 18, Part 1+2: 28), 3 Cadasio placeholders; 14 guides have none, including all full builds and all LAC and PMG guides. Tooltips enabled in 20/20 projects with title bound to the per-solid 'Description' value and no body text; 8-27 distinct names per guide (PMG 24-26, contrary to the PMG readers' 'placeholder' note).
- Exceptions: LSM descriptions exist but are stale (numbering offset, typos, bare 'Step nc'). Tooltip names contain typos and leftovers ('Laster Stem Matrix (LSM) - Part 1' on 58-80 solids, 'Housing Base - Part A1', 'Key Passthrough - Part H2'). Tooltip appearance was not observed live.
- Why it helps students: Wordless steps work for mixed reading levels and languages; a name is available on demand when a student points at a part.
- For our player: Parts list needs a display name per kit item and a mapping from every mesh to its kit item for hover/tap naming. Step description should be optional and off by default; no modal popups.

### NEV-1 · confirmed

**Never annotate: the finished/end view; Transitions (2D); wooden panels with text; wire colours; part names or component values; the route of a wire; step numbers, card titles, sentences, warnings, ticks, tools or hands on the canvas; lead lines or arrows with text.**

- Applies to: all guides
- Evidence: End views with any annotation 0/19; Transitions with a 2D annotation 0/117; labels linked to wood 0/214; labels containing a colour of a wire, a part name, a verb or a step number 0/214; lead lines on the 48 wire steps of the full builds 0; labels in LSM and PMG deconstruction 0 (LAC 4).
- Exceptions: Rail labels contain 'red'/'blue' (the rail stripe). 'Pin d12' has the word 'Pin'. Pictures may contain their own captions ('Protective Backing', 'NANO I/O MODULE LABELS', 'GND Strip').
- Why it helps students: Keeps the picture uncluttered and makes every annotation that does appear mean 'act on this now'.
- For our player: Do not auto-generate part-name labels, step captions on canvas or wire-path overlays; the end view and auto-advance frames must render with the annotation layer empty.

### LIFE-1 · confirmed

**Treat every 2D annotation as belonging to exactly one step view: it appears with that view and is gone on the next; give every instruction view at least one annotation.**

- Applies to: all guides
- Evidence: 535 of 544 label, eye and image objects are visible on exactly one viewer step (98 %). Step N with at least one annotation of any kind 423/425; with a 2D annotation 251/425.
- Exceptions: 9 reused objects ('2x' on 4 and 4c; LSM 'i3' label on two steps; four LSM disc images; one duplicated LAC deconstruction frame). The two empty Step N are the same PMG ribbon-prep step.
- Why it helps students: Nothing stale ever lingers on screen, and an instruction view never leaves the student guessing what to do.
- For our player: Annotations are properties of a step phase, not scene objects with their own timeline; entering a phase shows its set (fade), leaving hides all of it. Lint: warn on an instruction phase with no annotation.

### POS-1 · qualified

**Store each callout's position relative to the viewport shape it was authored in, and record that shape (it was 2.00:1 for PMG builds, 1.86:1 for PMG Deconstruction, 2.07:1 for LAC, 2.00-2.07:1 for LSM; no field in the data holds it). When the viewport shape changes, keep the CENTRE of the callout registered with the 3D model: y as a fraction of height, x offset from screen centre in units of height; the leader tip follows the projected feature. Observed on PMG only. Do not assume labels scale with viewport width.**

- Applies to: all guides (observed on PMG, the only kit saved at two viewport shapes)
- Evidence: ~2:1 frames: rendered x = 0.999-1.013 x stored x (LAC residual 0.04 % W), y slope 1.000. 2.79:1 frames: rendered x = 0.712-0.737 x stored + 11.6-13.3 (prediction for centre scaling by 1.99/2.79 = 0.713), y slope 1.001-1.002; eye stored at 31.8 % renders at 36.9 % (predicted 37.0). Sizes stay a fraction of width: label rule 7.19 % W and eye 8.2 % W at both shapes. Authoring pictures are 1.95:1-2.07:1 in 17 guides. 218/226 eye positions match the data (median error 0.05 % x, 0.26 % y).
- Exceptions: Only one pair of viewport shapes exists; portrait and narrow screens are untested. Width-relative sizing makes callouts large relative to the model on very wide viewports. 8 eye and 4 inset positions are stale in the data.
- Narrowed because: Reference is not 2:1 in general: LAC slope 0.997-1.002 at 2.065-2.07 (a 2:1 reference would give 0.968); PMG Deconstruction eyes [004],[009],[028],[035] at 1.857:1 render exactly at stored x (a 2.00 reference would shift them 1.1-2.6 % W). Even PMG Full Build pictures are stretched 1.022 (reference 2.00 against picture 1.952). 'Size is a fraction of width' is untested: the same 175 px box is 6.25 % W (LSM Parts 1/2), 7.0-7.2 % (PMG), 8.0-8.1 % (LAC). LAC and LSM have labelled pictures at one shape only, so they give no evidence on re-registration.
- As first stated: Store callout positions for a 2:1 frame and keep them registered with the 3D model when the viewport shape changes: y as a fraction of height, x measured from the screen centre in units of viewport height; the leader tip always follows the projected 3D feature.
- Why it helps students: Labels stay beside the part they belong to on any classroom screen instead of drifting away or onto the model.
- For our player: Layout engine: anchor = (0.5 W + dx * H, y * H) with dx authored at 2:1; recompute leader tips from 3D each frame; clamp to safe margins; consider sizing callouts by viewport height (not width) to avoid the wide-screen growth, and define behaviour for portrait.

### COL-1 · confirmed

**Reserve light blue #7fdbff for all 2D callout furniture (label rule, leaders, rings, inset frames, filled badge), black for label text and the eye glyph, and red inside 2D only as thin highlight rectangles in pictures; never colour-code labels by wire or function.**

- Applies to: all guides
- Evidence: #7fdbff on 214/214 label rules and leaders, 226/226 eye leaders, 223/226 eye rings, 43/45 inset frames, 41/45 inset rings. Label text black 214/214. Red rectangles inside 17/22 inset pictures.
- Exceptions: Quantity labels are coloured text (#0074d9 or #7fdbff); 3 teal rings, 2 orange rings, 2 #7fb9ff frames are slips.
- Why it helps students: Blue always means 'information / look here' and red always means 'motion or the critical detail', so the two channels are never confused.
- For our player: Define two theme tokens (callout blue, motion red) and use them everywhere; do not expose per-annotation colour pickers.

### Added by the re-check

- Every on-step callout is a pair: a 2D item plus exactly one 3D anchor. Only title images and the one full-frame diagram are free-floating. *Evidence:* Links per item: standard labels 214/214 one link, other labels 9/9, eyes 226/226, framed insets 45/45, disc badges 18/18 (512 of 512); title images 0/38 and LED Matrix Diagram 0/3. Even the leaderless quantity labels carry a link.
- The centre of a callout is what stays registered with the model when the viewport changes shape, and the shape it was authored in is not stored anywhere, so the in-house format must record it per guide (or per callout). *Evidence:* PMG identical stored labels at 1.952:1 and 2.786:1: centre model error 0.02-0.06 % W against 1.5 % for the corner. Implied reference aspect PMG builds 1.99-2.01, PMG Deconstruction 1.857, LAC 2.064-2.076. default_camera.aspect_ratio does not track it (PMG Deconstruction 2.001, LSM Full Build 1.044).
- On a wire step the layout is split in two: destination labels above the model, the wire to pick up staged well clear of both destinations with the eye beside it and below the labels. *Evidence:* 87 eye + label showings: eye centre lower than both label rules on 72 (LAC 38 of 44, PMG 34 of 42); eye target (the loose wire) at least 14.1 % H from the nearest label target, median 28.5 %. Eye link on these steps: wire body 64 (LAC 22, PMG 42), free connector housing 18 (LAC pre-attached leads) + 4 (LAC Deconstruction).
- The rule under a label is as long as the label box, so it grows with the text: 175 px for identifiers, 195-258 px for rail labels and 'Pin d12'. Budget up to 11.7 % of viewport width for a label. *Evidence:* 24 rail-label showings measured at 9.2-11.65 % W against 8.0-8.1 % for 175 px boxes in the same pictures (LAC FB [010],[019],[027],[074]).
- Leaders may run over the model but never through another label's text, and labels never share a step with a 3D arrow. *Evidence:* Cyan pixels inside any other label's text box: 0 of 214. Label + arrow co-occurrence 0 across the full builds and deconstructions; label + lead lines 7, label + eye 42 in the full builds.
- In LAC and LSM the eye's leader starts inside the glyph and is drawn over it; PMG moved the start to the eye's corner. Treat the PMG form as the convention. *Evidence:* leader_start_position for 160 LAC/LSM eyes spans x 0.06-0.95, y 0.25-0.77 of the square (all inside the glyph band); PMG 58/58 at x under 0.12 or over 0.88 and mid height. Visible in LAC Part 1 [019] close-up.
- Data caveat for anyone importing the projects: most 2D objects defined in a project are leftovers that no viewer step shows, and some saved pictures are older than the stored positions. *Evidence:* 856 text and image objects are defined but never visible on a viewer step (for example LAC Electronics 94, PMG Deconstruction 84, LAC Part 4 79) against 544 that are shown. Stale pictures: LSM Step 6 labels and eye (Part 1 [012], FB [013]), 13 eye showings and 4 inset showings in total.
- Label text has small markup slips that shift it off centre; a player should centre the text itself rather than trust the source markup. *Evidence:* 5 showings with 'margin-left: 25px' render 5-9 % of the rule length right of centre (LAC 'g1' [006] in Part 1 and FB, LSM 'i2' Part 2 [010] and Part 1+2 [026], LSM FB 'i3' [032]); 2 'Pin d12' showings have no centre attribute; 4 showings start the leader at 0.985 instead of the rule end.

### Numbers (as corrected by the re-check)

| Setting | Value | Basis |
|---|---|---|
| Label rule length on screen | Equals the label box width. Standard 175 px box: 8.0-8.1 % of width in LAC and LSM Full Build, 7.0-7.2 % in PMG, 6.25 % in LSM Parts 1, 2, 1+2. Rail labels and other long texts: 9.2-11.7 % of width. Overall range 5.0-11.7 %, not 6.3-8.3 %. | Rule located by colour for 214/214 labels; lengths per capture from reports/_work_verify_labels/thick.py and pix_resid.py (rail labels 201-258 px boxes measured at 9.2-11.65 % W). |
| Rule and leader thickness | Rule length / 35 (5 px on a 175 px box). On screen 0.46 % of height in LAC and LSM Full Build (5.7 px on a 1239 px frame), 0.38 % in PMG Full Build, 0.36 % in older LSM, 0.55 % at 2.79:1. The analyst's '5 px on 1239 px' undercounts the anti-aliased edge. | Integrated red-channel deficit across the rule on 181 standard-box labels; ratio rule/thickness 35-36 in every capture. |
| Label text alignment | Centred over the rule on 207 of 214 in the picture (212 by attribute). 5 showings carry a 25 px left margin and sit 5-9 % of the rule length right of centre; 2 ('Pin d12') are not centred. | Attribute scan of editor_contents plus measured text-centre offset per label (centre.py). |
| Text-to-rule gap | 0.42-0.48 x cap height (analyst 0.55). | Dark-pixel extent above the located rule, capitals/digits-only labels, per capture (thick.py). Method-dependent; treat as about half the cap height. |
| Anchor ring diameter | 35-36 px outer at 1.2 scale = 0.20 x a 175 px rule. On screen 42 px on a 2559 px wide LAC frame (3.4 % of height), 2.8 % in PMG Full Build, 2.3-2.5 % in older LSM, 4.0 % at 2.79:1. Analyst's '39 px, about 3 %' is slightly low for LAC. | Ring extent measured perpendicular to the leader on 172 labels (misc.py). |
| Authoring viewport aspect | Per guide, not one value: reference 2.00:1 for PMG builds (pictures saved at 1.952 and 2.786), 1.86:1 for PMG Deconstruction (49 of 61 pictures), 2.065-2.07:1 for LAC, 2.00:1 for LSM Parts 1, 2, 1+2 and 2.065:1 for the other LSM guides. | Saved picture sizes for all 1037 steps; per-guide fits of stored against rendered x for labels and eyes (pos1.py, pmgdecon.py). 17 guides do have pictures in 1.95-2.07 as claimed. |
| Callout registration point | Centre of the callout (label box, eye square, inset frame), not its stored top-left corner. | PMG 1.95:1 against 2.79:1: centre model error 0.02-0.06 % W, corner model 1.5 % W; vertical rule position consistent with box centre + half rendered height. |
| Eye distance from target | Median 23.6 % of viewport height (quartiles 19.4-27.8, range 11.2-56.9). The 15-35 % band covers 167 of 218 (77 %). | 218 template-located icons. |
| Eye allowed screen area | Centre x 17-81 %, y 6-76 %; 32 of 218 centres are in the bottom third. The label restriction (rule above 66.7 %) does not apply to the eye. | Same 218 icons; zones L-mid 38, C-top 46, C-mid 49, R-mid 28, C-bottom 26, L-top 20, L-bottom 6, R-top 5. |
| Eye positions that match the stored data | 213 of 226 (8 grossly stale, 5 more off by 2-5 %), not 218. | Template match against stored centre after the PMG re-registration; extra mismatches at LAC FB [088],[119], LAC Part 3 [018], LAC Part 4 [030], LSM Part 3+4 [006]. |
| Stale label positions | 4 label showings are stale too: LSM Step 6 'j2'/'j3' in Part 1 [012] and Full Build [013]. | No cyan line runs from the rule to the stored tip (coverage 0.02-0.36); rule 2-6 % W from the stored position. |
| Inset vertical extent | Centre never in the bottom third; frame height median 30 % of viewport height (14-72); frame bottom edge reaches 70-81 % of height on 11 of 35 located frames. | Frame outlines located in the pictures (img2.py). |
| Section cards | 31 showings in 13 guides (not 12); 4 / 5 / 5 per full build confirmed. | Guides with at least one card: LSM Part 1, 2, 1+2, 4, 3+4, FB; LAC Part 1, 2, 3, FB; PMG Part 1, 2, FB. |
| Result views with a 2D check cue | 21 real check cues of 424 (5.0 %); 23 with any 2D annotation once the two carried-over '2x' are counted. | 14 inset showings, 7 eyes, 2 '2x' on Step Nc. |
| Label slot drift in a run | Up to 15.5 % of width (PMG module label 50.6 to 66.1 %); about 1.6 % only for a label on a fixed connector. | Rendered rule positions over PMG FB [007]-[032] and LAC FB [079]-[085]. |
| Non-eye image showings | 104 (45 framed insets, 38 title images, 18 disc badges, 3 full-frame diagrams), not 112. | Class counts N 39, Nc 14, card 13, Start 38. |
| Defaults confirmed without change | Callout colour #7fdbff; text black bold; 3em of a 20 px base with 175x90 box (2.5em / 175x75 in older LSM); Arial 126 / unset 88; cap height 4.04-4.08 % H (LAC), 3.5 % (PMG), 2.5 % (LSM 2.5em), cap/rule 0.24-0.25 and 0.20; max 2 labels per step; 2-3 characters typical, 8 max; leader length median 19 % H (14-23, 3-44); angle median 35 deg (23-43); label above target 88 %, drop median 8.8 % H; label area centre x 21-74 %, rule y 13-66 %; stacked spacing min 9 %, median 15 %; eye width 7.81 / 8.2 % W, 1 per step, 2 at most; eye direction above 56 %, level 24 %, below 21 %; inset frame style 43/45; inset width 16 % and 31 %; disc 5.8-7.8 % W; quantity label 6em; title-page slots; lifetime 1 step (535/544); fade, 800 ms on every label and card step. | Each recomputed from my own replay or pixel measurement; baseFontSize is '20' in all 20 projects; the only 1600 ms steps are 5 Transitions and 2 Step Nc. |

### Open questions

- Could not open the live viewer: are step descriptions shown to students at all (they exist only in the three oldest LSM guides, with stale numbering), and how do the hover tooltips look and behave on touch screens?
- Sizing rule for 2D callouts is inferred from saved pictures only: labels and eyes keep a constant fraction of viewport WIDTH across 1.95:1 and 2.79:1 pictures, but the stored label box is in px and the px-to-screen factor differs per capture (0.92-1.58). What should the in-house player do on portrait, narrow or very wide screens?
- Horizontal positions are compressed about the screen centre at 2.79:1 (factor 0.71-0.74). Is this a true 3D-anchored callout (the link data holds 3D 'position' and 'target' vectors whose frame I could not resolve) or a 2D remap? Only one pair of viewport shapes is available to test.
- Where stored positions disagree with the saved picture (8 eye icons, 4 insets, mostly LSM Full Build / Part 1 / Part 1+2 and PMG Full Build), is the data or the picture stale? The live viewer would settle it.
- Which label size and font are the intended standard: 3em (LAC, PMG, part of LSM Full Build) or 2.5em (older LSM); Arial (LSM, LAC) or the project default Public Sans (PMG)?
- Case convention for pin names: PMG mixes 'clk/dio/s8/s9' with capitals elsewhere and LSM has 'Pin d12'. Should the player enforce lower case for breadboard holes and capitals for module and shield pins?
- Should off-board module pins use the LSM disc-badge pair or the ordinary underline label used by the later LAC and PMG guides?
- Should a wire-end label point at the destination hole (LAC, PMG, LSM rigid parts) or at the wire's own connector housing (LSM wire-end steps)? The LSM Full Build already moved far-end labels to the hole.
- The eye icon carries two meanings ('pick this up' and 'check this') with one glyph, and it appears on 7 result views. Does TechBox want separate icons or a rule that result views may carry one check cue?
- Quantity cue has four forms ('2x' blue, '64X', '64x', '3x' inside a picture). Which is the standard?
- Section-card coverage is uneven (Rocker Switch and both USB Cable cards are bare; the potentiometer has none; LSM's LED Matrix Diagram shows no 3D). Should every new bought-in component get a card with a pinout photo?
- Red highlight rectangles and two eye glyphs are baked into inset bitmaps. Should the player draw these as live overlays so they scale and theme with the rest?
- The white-space test for labels cannot detect overlap with white parts (breadboard). Visual inspection of about 45 frames found none, but it is not proven for all 214.

## Camera, framing and transitions

### CAM-1 · confirmed

**Never change the camera on a completed frame (Step Nc). Compute one camera per numbered step from the hover state and hold it through any part-motion keyframes to the completed frame.**

- Applies to: all step types, all three kits, construction and deconstruction
- Evidence: Camera moves on 0 of 424 Step Nc. 420 of 422 Step N / Step Nc pairs use one identical camera from hover to completed frame (computed from raw camera position/target per step; move threshold 0.5 deg / 0.5 mm).
- Exceptions: PMG Deconstruction Step 2 ([004] to [008]) and Step 3 ([009] to [013]): a camera-only auto Transition ([007], [012]) sits before Step Nc, so the result is seen from a different side. 3 Step N have no Nc at all (naming slips).
- Why it helps students: The before and after pictures are directly comparable: the only thing that changes between them is the part, so the student sees exactly what moved and where it ended up.
- For our player: Camera is a property of the numbered step, not of each frame. The player must not auto-refit or re-centre when the part seats; the completed frame inherits the hover camera unchanged.

### CAM-2 · qualified

**Set the camera only on entering a Step N, a section card, the title page or the final view (or in a dedicated camera-only auto step). Always re-set it on entering and on leaving a card that shows a 3D part (28 of 28 each way) and on leaving the title page (19 of 19). A 2D-only card may keep the surrounding camera. The final view usually re-sets it (17 of 19).**

- Applies to: all, all kits
- Evidence: 325 camera moves in 1037 viewer steps: 266 on Step N, 30 on cards, 17 on final views, 12 on camera-only Transitions, 0 on Step Nc. Cards: camera moves onto 29 of 31 and off on the next step on 30 of 31. First step after Start moves the camera 19 of 19 (rotation 8-110 deg).
- Exceptions: 2D-only card 'LED Matrix Diagram' keeps the previous camera (LSM Part 2 [009], Part 1+2 [025]); LSM Full [027] uses the card to pre-position the camera for Step 13. Final view does not move in PMG Part 1 and PMG Deconstruction.
- Narrowed because: The 'always' fails only on the 2D 'LED Matrix Diagram' card (0 parts on screen): LSM Part 2 [009] and LSM Part 1+2 [025] keep the previous camera on entry; LSM Full [027] moves on entry but the next Step 13 does not move. Final view does not move in PMG Part 1 [033] and PMG Deconstruction [060].
- As first stated: Set the camera only on entering a Step N, a section card, the title page or the final view (or in a dedicated camera-only auto step). Always re-set it when entering and leaving a card and when leaving the title page.
- Why it helps students: The view only changes at the moment the student is being told something new, so a camera move itself signals 'new place to look'.
- For our player: Authoring data needs a camera slot on step, card, title and final-view records only. Entering or leaving an isolated card must always trigger a camera change.

### CAM-3 · qualified

**Always set a new camera when the action (loose or hovering part plus destination) would not be fully inside the frame of the camera currently in effect. If it would fit: keep the camera for consecutive wiring steps (86 % kept) and consecutive eye-only steps (91 % kept); for rigid inserts and arrow steps expect a re-aim about two times in three, including after a step of the same kind; re-aim on a change of step kind (87 %).**

- Applies to: all; strongest contrast between wiring and mechanical steps; all kits
- Evidence: Step N moves the camera 266 of 425 (63 %): wiring 36/109 (33 %), rigid insert 112/149 (75 %), arrow 66/86 (77 %), eye-only 50/79 (63 %). Previous step same kind: wire to wire 12/85, eye to eye 2/23, lead to lead 66/94; kind changed 131/151 (87 %). Reuse test (action volume projected through the previous step's camera, 2 % margin): not inside 79, moved 77 (the other 2 had just been moved by a camera Transition); inside 324, moved 169 (52 %): wiring 19/91, rigid 64/99.
- Exceptions: Guide-level spread: PMG Part 1 moves on 3 of 14 Step N, PMG Part 3 on 24 of 26. Deconstructions 55/94 (59 %).
- Narrowed because: 'Reuse if same kind' fails for lead to lead (66 of 94 move) and arrow to arrow (36 of 53 move). Among lead to lead steps with the same travel direction and an action centre within 60 mm, 13 move and 16 hold, so no sharper rule emerges. 'Mechanical steps re-aim even if in frame' is 66/103 for rigid inserts, not always. Guide spread confirmed: PMG Part 1 3/14, PMG Part 3 24/26; deconstructions 55/94.
- As first stated: On a new Step N, reuse the previous camera if the step is the same kind of action in the same place; otherwise re-aim. Always re-aim if the action (loose/hovering part plus destination) would not be fully inside the previous frame; for mechanical steps re-aim to face the joint even if it would be.
- Why it helps students: Fewer camera moves during repetitive work keeps orientation; a fresh view for each new joint puts the tabs, slots and hover gap in plain sight.
- For our player: Auto-camera needs a reuse test before computing a new view: same step kind + action box inside previous frustum with margin. Wiring steps default to reuse; mechanical steps default to a new view.

### CAM-4 · qualified

**Hold one camera for a whole block of consecutive wiring steps in one work area (the block ends at a section card or a non-wiring step): set it on the first wire, framed for both ends of every wire in the block plus the staging spot of the loose wire, and do not move it per wire. A block can span several modules. LAC and PMG always; LSM for breadboard-side ends only.**

- Applies to: wiring; LAC and PMG always, LSM for breadboard-side ends; construction and LAC deconstruction
- Evidence: 30 label-only runs: 26 have no camera move after their first step; 72 of 79 later wire steps reuse the camera. First step of a run sets a new camera in 29 of 30.
- Exceptions: All 7 exceptions are LSM: the three matrix-pin steps swing 105-130 deg to face each pin (LSM Part 2 Steps 6, 7; Part 1+2 Steps 14, 15; Full Steps 14, 15) and LSM Full Step 12 nudges 5.8 deg.
- Narrowed because: 5 of the 30 runs are a single step, so the meaningful figure is 21 of 25 multi-wire runs. 'One module' is wrong for PMG Part 1 / Full [007]-[033]: 12 wires to four button modules and the shield under one camera (modules fade in at [013], [020], [027]). LSM exceptions as stated: Part 2 Steps 6, 7 (130, 105 deg), Part 1+2 Steps 14, 15, Full Steps 14, 15 (125, 109 deg) and Full Step 12 (5.8 deg). The cited LAC Decon [092]-[128] hold is 9 eye-only and 3 arrow steps, not a label run.
- As first stated: Hold one camera for a whole wiring run on one module: set it on the first wire, framed for both ends of every wire in the run plus the staging spot of the loose wire, and do not move it per wire.
- Why it helps students: Breadboard rows and header pins keep the same place on screen for every wire, so the student only has to read the new label.
- For our player: Group consecutive wire steps to the same module into a run and compute one camera from the union of all their endpoints, the module, and the wire staging position.

### CAM-5 · qualified

**Use a three-quarter view from above: effective elevation about 34 deg, between 20 and 50 deg on 87 % of steps. Views of 48-57 deg are used for anything lying flat that is read from above: LAC breadboard wiring, isolated prep close-ups, the ghosted underside check, some cards and deconstruction finals. Views of 13-19 deg are used to see a joint, pin or lead side-on, and for flat-module cards.**

- Applies to: all, all kits
- Evidence: Effective elevation (measured against the scene's declared up-axis): 903 of 1037 steps (87 %) in 20-50 deg, 983 (95 %) in 15-55; median 34; mean of 345 views 34.0. Step N views by kit: LSM 32, LAC 36, PMG 34. By kind: rigid insert 33 (IQR 27-36), arrow 35, eye-only 41, wiring 28.
- Exceptions: 15 steps outside 10-60 deg: plan views (PMG Nano I/O Module card 90; LSM carry-the-matrix step, world elevation 85), face-on cards (0-5), LAC knob check (8).
- Narrowed because: 'Higher only for a flat breadboard layout' fails: of 35 views at 48 deg or more only 8 are wiring views. The rest: 12 eye-only prep close-ups (LAC Full [017] Step 8, [040] Step 19; LSM Part 1 [007] Step 4), 5 arrow steps (LAC Full [104] Step 47; LSM Full [046] Step 21), 3 ghosted underside checks at 57, 3 cards, 2 deconstruction finals (49, 50), 2 PMG ribbon preps. Low band fits: 7 rigid inserts, 5 cards, 3 LSM matrix-pin wires, 2 PMG Decon steps.
- As first stated: Use a three-quarter view from above: effective elevation about 34 deg, kept between 20 and 50 deg. Go higher (48-57) only to look down onto a flat breadboard layout, lower (13-19) only to see a joint or lead side-on.
- Why it helps students: Top and two sides of the assembly are visible at once, so vertical hover gaps and horizontal positions both read without ambiguity.
- For our player: Default elevation 34 deg with a 20-50 clamp; allow a per-step override. Elevation must be measured against the step's up-axis, not world Y.

### CAM-6 · qualified

**LSM and LAC: point the camera at a corner of the model, azimuth within 15 deg of a diagonal (+-45 or +-135) on about 85 % of views, quadrant chosen per step. PMG: no preferred azimuth class (diagonal and cardinal views equally common); only its title pages are diagonal. All kits: title page on a diagonal (19 of 19); for a sideways insertion stand about 40-55 deg off the travel axis in plan and never look along it.**

- Applies to: all; quadrant choice matters most for mechanical steps; all kits
- Evidence: Views with +y up: 215 of 299 (72 %) within 15 deg of a diagonal, 41 (14 %) within 15 deg of a cardinal; median offset from a diagonal 9 deg. Title pages 19 of 19 within 15 deg of a diagonal. Horizontal inserts (48): camera 45-135 deg from the travel axis in plan on 34; on the approach side on 31.
- Exceptions: All four quadrants are used; there is no single house azimuth. Cardinal views: PMG Decon bench phase (az 90), PMG Part 2 Step 11 rear view (az 90), flat-module cards.
- Narrowed because: PMG as a whole: PMG Deconstruction 6 diagonal vs 9 cardinal of 19 views, PMG Full 12 vs 11 of 31, PMG Part 2 3 vs 5 of 9. Examples: PMG Full [091] Step 42 az -12, [094] Step 43 az -167, [110] Step 50 az -177, [057] Step 25 az 90; PMG Decon [047]-[059] az 90.
- As first stated: Point the camera at a corner of the model: azimuth near a diagonal (+-45 or +-135 deg), choosing whichever quadrant shows the mating features and the hover gap. For a sideways insertion stand roughly 45 deg off the travel axis, never looking along it.
- Why it helps students: A corner view shows two faces of every panel, so tabs, slots and engraved part IDs are readable and the incoming part is not hidden behind the assembly.
- For our player: Auto-camera should test the four diagonal quadrants and score each for visibility of the action volume and mating features, preferring the approach side; expose azimuth as a per-step override.

### CAM-7 · confirmed

**Use one lens and one camera motion everywhere: perspective, 45 deg vertical field of view, no roll, camera always looking at its target; animate camera changes as an 800 ms tween.**

- Applies to: all, all kits
- Evidence: FOV 45 on 1036 of 1037 steps. Roll against the declared up-axis under 2 deg on 1037 of 1037. Camera animation = tween, orbit animation off, speed 2 on 1037 of 1037. All 325 camera moves occur in 800 ms steps.
- Exceptions: LSM Part 1 'Capacitor' card [011] has FOV 50 (late insertion, anomaly). Animation options are stored as strings on 1035 steps.
- Why it helps students: A constant lens keeps apparent sizes comparable from step to step; a short tween (not a cut) lets the student follow where the view went.
- For our player: Fix FOV at 45 deg vertical and tween position/target over the step duration (800 ms). No per-step lens control is needed.

### CAM-8 · qualified

**Change view with a compound move that is mainly an orbit in azimuth (median 61 deg), with a moderate target shift (median 42 mm, 0.15 x distance) and usually a zoom change of 0-1 ladder level. Pure pan or zoom is rare (10 of 325). Elevation changes by a median 9 deg and stays within 15 deg on three moves in four. Within a guide every view is authored for its step; there are no home stations.**

- Applies to: all, all kits
- Evidence: Step N moves: median rotation 61 deg (IQR 22-83); 134 of 266 over 60 deg, 58 over 90 deg; median target shift 42 mm; median elevation change 8 deg. Pure pan/zoom (rotation under 2 deg) on 10 of 325 moves. 345 views use 341 distinct poses.
- Exceptions: Pure zoom-out after a card (LSM Step 37 / 17 / 12 after LED Stems; LAC Step 9). PMG Decon bench phase [047]-[060] holds one direction (e23 az90) with pans of 30 and 76 mm and one zoom.
- Narrowed because: 'Keep elevation within a few degrees': over 15 deg on 59 of 238 moves, 5 deg or less on only 75. 'Not by panning or zooming': 232 of 325 moves also change distance. Fifteen views share a view direction within 3 deg with an earlier non-adjacent view. Across sibling guides poses are copied: 108 of 196 distinct poses occur in more than one guide.
- As first stated: Change view by orbiting around the assembly, not by panning or zooming: turn mainly in azimuth, keep elevation within a few degrees, keep the target near the assembly. Author each view for its step rather than returning to fixed stations.
- Why it helps students: The assembly stays in the middle of the screen while the viewpoint walks round it, like turning the kit on the desk.
- For our player: Store camera as target + azimuth + elevation + distance; interpolate so large turns stay centred on the assembly. No library of preset stations is needed.

### CAM-9 · confirmed

**Take zoom from a small set of discrete levels spaced x1.166 apart, and change by at most one or two levels between consecutive in-context views.**

- Applies to: all, all kits
- Evidence: 992 of 1035 build/deconstruction steps (96 %) on a x1.166 ladder anchored at the kit's most-used distance; measured single-step ratio 1.165 (n 99). Zoom change on a move: none on 93 of 325, within +-1 level on 186 (57 %), within +-2 on 233 (72 %).
- Exceptions: Off-ladder: LSM 321, 374, 173, 42, 60; LAC 125; PMG 91, 103, 133, 142. LSM's ladder is half a level offset from LAC/PMG. Likely an editor zoom increment rather than a deliberate rule.
- Why it helps students: Scale stays stable between neighbouring steps; when it does jump, it marks a real change of context (close-up in or out).
- For our player: Snap computed distances to a geometric ladder (ratio about 1.17) and prefer the previous level when the fit is within one level, to avoid small zoom jitters.

### CAM-10 · qualified

**Set the distance from the working assembly on screen, not from the part being added: pull back as the assembly grows so the content fills about 60 % of the frame height (IQR 0.51-0.74; LSM 0.57, LAC 0.71, PMG 0.54). As a fit: depth to content centre is about 2.4 x the half-diagonal of the seated content, or about 2.2 x when the hovering part is included. Idle tethered sub-assemblies may be cropped.**

- Applies to: all, all kits
- Evidence: Model height / frame height on clean Step Nc frames is 0.54-0.63 in every distance band from under 130 mm to over 400 mm (259 views) while the content half-diagonal grows from 38 to 202 mm. Depth to content centre / half-diagonal of visible content: median 2.4, IQR 1.9-2.6 (203 validated views) = 0.91 x the bounding-sphere fit distance. In-context correlation of log distance with content size r 0.70, with action size r 0.54.
- Exceptions: LAC frames fuller (height median 0.71) and often cropped; 17 % of all frames touch an edge. Orbit distance is unreliable on a few isolated views whose target sits behind the part (LAC Full [046]-[054]).
- Narrowed because: The report's derived rule 5 pairs 2.4 with 'hover part included'; with the hover part the figure is 2.2. Applied to the hover-inclusive box, 2.4 lands within 20 % of the real depth on 133 of 213 views. Fill is not constant per kit and band (LAC 290-340 mm 0.87, LSM under 130 mm 0.47, PMG 130-215 mm 0.47). 65 of 398 clean Nc frames and 176 of 1037 frames touch an edge; PMG Part 3 [033], [038] and PMG Decon [017] crop the case itself.
- As first stated: Set the distance from everything that is on screen (assembly plus hovering part), not from the part being added: pull back as the assembly grows so that the content fills about 60 % of the frame height.
- Why it helps students: The student always sees the whole thing they are holding, so they can locate the new part relative to landmarks instead of a magnified hole.
- For our player: Fit distance = 2.4 x half-diagonal of the bounding box of all visible parts including the hover pose (about 0.9 x sphere fit at FOV 45), then snap to the ladder. Do not fit to the new part alone.

### CAM-11 · confirmed

**Do not zoom in on a small part while it is in context. Use a close-up only together with isolation (everything else hidden): cards, prep steps and sub-assembly work.**

- Applies to: all; cards and prep steps vs in-context steps; all kits
- Evidence: Isolated views (3 or fewer top-level parts, n 60) median 175 mm (IQR 110-224); in-context views (n 285) median 300 mm (258-323); ratio LSM 1.5, LAC 1.9, PMG 1.4. Only 9 of 285 in-context views are closer than 150 mm. In-context steps whose action is under 20 mm half-diagonal (n 12) are shot from a median 189 mm, the ordinary board view.
- Exceptions: LAC knob-position check (Full [063]-[064], Part 2 [033]-[034]) is a 125 mm face-on close-up with the panel still on screen (cropped on purpose).
- Why it helps students: In context, labels and lead lines identify the spot while the whole board stays visible; a close-up is reserved for inspecting a part on its own, where there is nothing else to get lost in.
- For our player: Close-up is a mode tied to an 'isolate' flag on the step, not something the auto-camera derives from part size.

### CAM-12 · qualified

**Keep the whole action in frame: the loose or hovering part and its destination. Idle parts may be cut by the frame edge. On a rigid insert the hovering part usually sits in the upper half (centre about 30 % down), its top edge about 13 % from the top and occasionally right at the edge.**

- Applies to: all; cropping tolerance mainly in LAC and PMG enclosure sections
- Evidence: Action volume fully inside the frame on 419 of 422 Step N / Nc pairs, and on 75 of 76 Step N frames where something else is cropped. Action centre median (0.49, 0.45); height 0.43 of the frame (IQR 0.33-0.56). Rigid inserts: hover part top edge at 13 % from the top (10th percentile 3 %). 176 of 1037 frames touch a frame edge (LAC 94, PMG 69, LSM 13).
- Exceptions: 3 pairs with the action partly outside the frame; hover posts and stems in LSM touch the top edge.
- Narrowed because: Real exception: LSM Full [071] Step 32, hover part touches the top edge. The other two 'outside' pairs (LSM Part 2 [001] Step 1, LSM Part 1+2 [017] Step 9) are reprojection artefacts; the renders show the wire fully in frame. Near-edge hover parts: LSM Part 4 [012] 0.008, LSM Full [073] 0.011, LSM Part 3+4 [028] 0.011, LAC Full [125] 0.020, PMG Part 3 [055] 0.018. 'Hover part in the upper part' fails on 30 of 149 rigid inserts.
- As first stated: Keep the whole action in frame: the loose or hovering part, its destination and the lead lines between them. Idle parts (wired panels lying around) may be cut by the frame edge. Put a hovering part in the upper part of the frame.
- Why it helps students: Everything the student must act on is visible; clutter that is not part of the step is allowed to fall away rather than shrinking the important area.
- For our player: Auto-camera constraint: action box (hover pose + seated pose + lead-line endpoints) inside a safe area (at least 3 % from the top, 2 % elsewhere). Parts not involved in the step are excluded from the hard constraint.

### CAM-13 · qualified

**Centre the composition on the visible content (bounding-box centre about (0.49, 0.47)); expect white margins on all sides in about five frames out of six, used for labels, eye icons and insets. LSM and LAC are centred on 85-88 % of clean frames, PMG on 62 %.**

- Applies to: all, all kits
- Evidence: Clean Step Nc frames (398): box centre median (0.49, 0.47); inside the central 0.40-0.60 box on both axes on 315 (79 %); height 0.61 (IQR 0.52-0.74), width 0.41 (0.34-0.56); margins top 0.18, bottom 0.21, left 0.28, right 0.30. Step N frames with annotations (425): height 0.67, width 0.46, top margin 0.12. Whole content is nearer the frame centre than the action alone on 141 of 238 new in-context views.
- Exceptions: Off-centre on purpose when a wire is staged to one side or a photo sits beside a part. Width figures depend on the saved window shape (88 % of renders are 1.95:1 to 2.07:1).
- Narrowed because: No margin on at least one side on 65 of 398 clean Nc frames and 176 of 1037 frames overall (bottom 102, top 72, right 60, left 43). PMG clean frames centred on 73 of 117. Content beats action for centring by only 59 % to 41 % (median offsets 0.12 vs 0.17 frame heights).
- As first stated: Centre the composition on the visible content and leave white margins on all sides for labels, eye icons and insets.
- Why it helps students: The subject is always in the middle of the screen and annotations sit on clean white, never over geometry.
- For our player: After fitting, shift the target so the projected content box centre is at about (0.49, 0.47) and reserve roughly a quarter of the width each side for 2D callouts; define layout in frame-height units so it survives other aspect ratios.

### CAM-14 · qualified

**Never animate a part towards or away from the viewer: keep the travel axis at least 40 deg off the view axis (45 deg or more on 96 %, about 60 typical) so the travel spans about a quarter of the frame height. For vertical travel this follows directly from the elevation rule (angle = 90 deg minus elevation).**

- Applies to: mechanical / rigid insertions and removals, all kits
- Evidence: 126 rigid translations of 10 mm or more: angle between travel and view axis median 59 deg (IQR 56-63), minimum 41; 119 at 45 deg or more, none under 30. On-screen travel median 0.27 frame heights (IQR 0.22-0.36). Build guides: 63 of 120 travels straight down, 48 horizontal, 0 upward.
- Exceptions: 7 cases at 41-45 deg (LSM Full Step 24, Step 6; LAC Step 45, 46; their part-guide copies).
- Narrowed because: Under 45 deg: LSM Full [053] Step 24 (41.2), LSM Part 1 [012] and Part 1+2 [011] Step 6 (42.2), LSM Decon [028] Step 10, LAC Decon [117] Step 44, [123] Step 46, [126] Step 47 (all 44.3). '0 upward' is wrong: LSM Full Step 29 ([064] to [065]), LSM Part 3+4 Step 9 and LSM Part 4 Step 3 lift the matrix support 19-22 mm up to the hovering matrix (the digest lists that move as down; the renders show up).
- As first stated: Never animate a part towards or away from the viewer: keep the travel axis at least 45 deg off the view axis (about 60 deg is typical) so the hover gap spans about a quarter of the frame height.
- Why it helps students: The gap between the part and its seat, and the red lead lines across it, are seen side-on at nearly full length, so the direction and distance of the push are obvious.
- For our player: Add a hard check to the auto-camera: reject candidate views where /travel . view/ exceeds cos(45 deg); among the rest prefer the one with the longest on-screen travel that still satisfies the house elevation.

### CAM-15 · confirmed

**Treat an auto-advancing Transition as a part-motion keyframe with the camera locked. If the view itself must change without anything else happening, use a separate camera-only auto step between two numbered steps.**

- Applies to: all; camera-only form used in LSM (turn-overs), once in LAC, twice in PMG deconstruction
- Evidence: 117 Transitions: 68 part tweens, 27 pose swaps, 6 fade-ins, 4 annotation-only, 12 camera-only. Camera fixed on 105 of 117. The 12 camera-only ones change nothing else, carry no annotation, are 800 ms, play, overlay hidden, hidden from the step picker; 10 sit between a Step Nc and the next Step N; 8 coincide with an up-axis change.
- Exceptions: Not required for big moves: 58 Step N rotate more than 90 deg directly and 28 of 39 up-axis changes happen on a plain Step N. README_DATA.md describes Transitions as camera steps; that fits only 12.
- Why it helps students: Motion keyframes read as one continuous action from one viewpoint; a camera-only step lets the student watch the kit being turned before any new part appears.
- For our player: Player needs two auto-advance frame types: motion keyframe (camera inherited) and camera keyframe (camera only). Whether to insert a camera keyframe for turn-overs is an authoring choice, not a rule.

### CAM-16 · qualified

**To work on the underside, turn the model over for the block of steps (one or more) by re-declaring which way is up, and keep viewing from above at a normal elevation. Do the same for side work only when a panel or box has to be stood up or laid down; ordinary sideways insertions are done on the upright model. Never put the camera below the horizon of an upright model.**

- Applies to: mechanical / enclosure and sub-assembly blocks; 12 of 20 guides, all kits; construction and deconstruction
- Evidence: All 110 steps with the camera below the world horizon have a non-default up-axis. 148 of 1037 steps use a re-declared up-axis; 39 changes (28 on a Step N, 8 on a camera Transition, 2 on a card, 1 on a final view); camera turn at the change 43-167 deg, median 102. Effective elevation inside these runs 22-47 deg.
- Exceptions: LSM underside check (effective 57 deg) and LSM plan view; LAC knob check at 8 deg. No dedicated 'turn it over' annotation was found; the camera move is the only cue.
- Narrowed because: Outside 22-47: LSM plan view (-5 effective, world 85; 6 steps), LSM ghosted underside check (57; 6 steps), LAC knob check (8; 4 steps). 'Or a side' is not general: 50 sideways-insert legs in build guides are done on an upright +y model (PMG Full 13, LAC Full 7, PMG Part 1 6). 10 of the 22 runs are a single numbered step or a single card, e.g. LAC Full [125]-[127], [076]-[077], [078].
- As first stated: To work on the underside or a side, turn the model over for the whole block of steps by re-declaring which way is up, and keep viewing from above at a normal elevation. Never put the camera below the horizon of an upright model.
- Why it helps students: The screen matches what the student does on the desk: they flip the kit and look down at it, rather than peering up from underneath.
- For our player: Each step needs an up-axis (or model orientation) field that persists until changed; orbit controls, elevation clamps and the auto-camera must all work relative to it. Consider adding an explicit flip cue, which the Cadasio guides lack.

### CAM-17 · confirmed

**Use a straight-down, face-on or see-through view only when one specific face has to be read: a plan view to match a product photo or show a free-hand move, a face-on view for a flat module or a dial position, ghosted covering parts to check something hidden.**

- Applies to: cards and check steps; LSM, LAC, PMG single cases
- Evidence: 15 of 1037 steps lie outside the 10-60 deg band. Flat-module cards are face-on or plan on 7 of 18 distinct cards. Ghosting appears on one step pair (three copies).
- Exceptions: None beyond the listed cases; the same card is shot slightly differently in sibling guides (4-Digit Display e3 vs e12; Capacitor 60 mm vs 42 mm).
- Why it helps students: Printed pin names, a dial pointer or a hidden tab are shown undistorted exactly when the student must read or check them.
- For our player: Provide per-step overrides for elevation/azimuth and a per-part opacity property; these are hand-authored, not auto-derived.

### CAM-18 · qualified

**Frame a section card as an isolated close-up: hide everything else, centre the part (or the part-plus-photo pair), fill about 63 % of the frame height, then usually pull back when the assembly returns (22 of 31). Show the part face-on or in plan when it sits beside a photo or diagram of that face (PMG module cards, LSM Capacitor); otherwise use a 3/4 view (all LAC cards, cables, stems).**

- Applies to: section cards in construction guides, all kits
- Evidence: 31 cards: camera moves onto 29 and off on the next step on 30; 27 show 3 or fewer top-level components; height fill median 0.63 (IQR 0.61-0.70); centred within 0.40-0.60 on both axes on 30; distance median 175 mm (42-277); zoom-out to the next step median x1.36 (22 of 31 pull back by a ladder level or more). Card and following step share a viewing side (azimuth within 23 deg) on 17 of 29.
- Exceptions: Height fill only 0.34-0.37 on PMG 4-Digit Display and USB Cable cards. LCD Screen card to next step turns 167 deg. Step-level cross-fade on all 10 LAC cards, 7 of 11 LSM cards, 0 of 10 PMG cards.
- Narrowed because: 'Face-on for flat boards' fails in LAC: Real Time Clock (LAC Full [014], 22 deg) and LCD Screen ([078], 35 deg) are flat modules in 3/4. The LSM Capacitor (0 / 5 deg) is face-on without being a board. Low fill: PMG 4-Digit Display 0.34-0.35, PMG USB Cable 0.37. No pull-back: LAC USB Cable (x1.00), Dot Matrix Display (x0.86). LCD Screen to next step turns 167 deg.
- As first stated: Frame a section card as an isolated close-up: hide everything else, centre the part (or the part-plus-photo pair), fill about 63 % of the frame height, choose face-on for flat boards and a 3/4 view for 3D-shaped parts, then pull back when the assembly returns.
- Why it helps students: The student gets a clear look at the new component, matched to its real-world photo, before having to find it in a crowded scene.
- For our player: Card template: isolate list + auto-fit at 0.6 height + optional 2D inset slot to the right, with the 3D part shifted left so the pair is centred; allow a 'flat face' orientation preset.

### CAM-19 · confirmed

**Title page: show the finished model of this guide as a 3/4 hero in the right half of the frame, leaving the left for the logo (top) and title block (bottom).**

- Applies to: title page of every construction and deconstruction guide (19 of 19)
- Evidence: Model centre x median 0.71 (0.67-0.75 on 18 of 19), centre y 0.48, height 0.67 of the frame (0.60-0.74 on 17), left edge median 0.49. Elevation median 35 (21-47); azimuth within 15 deg of a diagonal on 19 of 19. Whole composition spans 0.91 of the width; left margin 0.02, top 0.06. Next step moves the camera 19 of 19.
- Exceptions: PMG Deconstruction: model centre x 0.58, the title text overlaps the model. PMG Part 2 model only 0.50 high.
- Why it helps students: The student sees the goal before starting, in a consistent layout across every guide of every kit.
- For our player: Title template: fit model to 0.67 frame height, then offset the target so the model centre sits at x 0.71; logo and title are fixed 2D slots on the left.

### CAM-20 · qualified

**Final view: clear all annotations and orbit to a centred 3/4 hero, usually on the same side as the title page (15 of 19), at the title-page distance or one to three ladder levels closer, at elevation about 39 deg: either the title-page elevation (within 3 deg, 11 guides) or 10-20 deg higher when the title page was low (7 guides).**

- Applies to: final view of construction guides; deconstructions show what is left
- Evidence: Camera moves on 17 of 19; annotations 0 on 19 of 19. Box centre median (0.47, 0.47), height 0.67. Elevation median 39 (Start 35); on average 4 deg above Start. Distance vs Start: same 9, one level closer 3, x1.59 closer 4, x1.85-1.98 closer 2, one level farther 1. Azimuth within 27 deg of Start on 15 of 19 (median 14). Last move is a 5-21 deg settle in 7 guides, a 55-120 deg swing in 10.
- Exceptions: PMG Part 1 (renamed Step 14c, camera unchanged) and PMG Deconstruction (camera unchanged, bare shield low in frame). LAC Full / Part 4 / Decon end about 95 deg round from the Start view.
- Narrowed because: 'A few degrees higher' is an average of two groups: 11 guides within 3 deg, 7 guides 10-20 deg higher (LSM Full, Part 3+4, Part 4, LSM Decon, LAC Decon, PMG Part 3, PMG Full), PMG Decon 10 deg lower. Other side of the model: LAC Full [130] and LAC Part 4 [041] (98 deg), LAC Decon [129] (93), PMG Decon [060] (135). Not centred: LAC Full / Part 4 x 0.39, PMG Decon y 0.68. No move: PMG Part 1 [033], PMG Decon [060].
- As first stated: Final view: clear all annotations and orbit to a centred 3/4 hero on the same side as the title page, at the same distance or closer, a few degrees higher.
- Why it helps students: A clean, centred picture of the finished result to compare with the real kit, echoing the picture they were shown at the start.
- For our player: Final-view template: auto-fit the whole model centred at title-page azimuth and elevation about 39 deg; reuse the title-page distance unless the content is much smaller.

### CAM-21 · confirmed

**When the whole scene is swapped (assembly hidden for an isolated part, or brought back), a page cross-fade may replace the animated fly; it is optional and applied by author preference.**

- Applies to: scene swaps around cards and prep steps; LSM and LAC only
- Evidence: 142 steps replace more than half the visible solids; 55 carry the step-level fade: LSM 31 of 62, LAC 24 of 48, PMG 0 of 32. 65 fades in total, 61 on a step that also moves the camera, 10 on steps that are not scene swaps.
- Exceptions: Inconsistent within guides (LAC Part 1 [010] swaps without a fade); never used in PMG.
- Why it helps students: A cut avoids a confusing fly-through between two unrelated scenes.
- For our player: Offer a per-step 'cut/cross-fade' option; default can be a plain 800 ms tween with part fades, which is what PMG (the newest kit) does everywhere.

### Added by the re-check

- The diagonal 'look at a corner' azimuth is an LSM and LAC habit, not a house rule: PMG uses cardinal and in-between azimuths as often as diagonals. An auto-camera should not force a diagonal for PMG-style content. *Evidence:* +y views within 15 deg of a diagonal: LSM 108/129, LAC 75/86, PMG 32/84 (32 cardinal, 20 between; median offset 21.5 deg vs 9.0 and 6.7). Step-weighted PMG: 58/255 diagonal vs 89/255 cardinal. PMG Full [091] az -12, [094] az -167, [110] az -177, [057] az 90.
- A camera belongs to the step, not to the guide: part guides and full builds share the same camera for the same step, and deconstructions reuse build cameras for the mirrored step. *Evidence:* Part-guide views with an exact copy (position and target within 1 mm) in the kit's full build: LAC 38 of 44 (Step N 30 of 30), PMG 37 of 41 (Step N 31 of 31), LSM Part 3 / 3+4 / 4 22 of 37. Deconstruction views that are exact copies of a build view: PMG 16 of 23, LAC 8 of 18, LSM 6 of 21; same direction within 5 deg on 49 of 62. Overall 108 of 196 distinct poses occur in more than one guide.
- Where the same step was re-shot independently, the author made the same camera choice: same viewing side, at most one zoom level apart, same move-or-hold decision. *Evidence:* LSM Part 1 / 2 / 1+2 share 0 of 45 poses with LSM Full, yet over the 21 common steps the view directions differ by a median 6 deg (17 of 21 within 10 deg), the Full Build sits exactly one ladder level farther out on 14 steps, and the move / hold decision agrees on 19 of 21.
- On a rigid insert, centre the frame on the destination (where the part ends up) and let the hovering part ride above it; do not centre on the hovering part. *Evidence:* 149 rigid inserts: seated-part box centre median (0.49, 0.47), 0.11 frame heights from the frame centre; hover-part box centre (0.49, 0.30), 0.30 away. Hover part above its destination on screen on 99, below on 40, level on 10.
- An action that would fall outside the current frame is the one hard trigger for a new camera; everything else is a tendency. *Evidence:* Action volume projected through the camera in effect immediately before the step: outside on 83 Step N, new camera on 83 (78 of 78 at 0 % margin, 98 of 99 at 5 %). The report's 77 of 79 comes from testing against the previous numbered step's camera instead.
- A scene swap (isolated part in or out) almost always comes with a new camera, and the step-level fade is set on the way into an isolated view far more often than on the way out. *Evidence:* 127 of 140 swap steps move the camera. Fade set on entering a card on 17 of 31 but on the step after a card on 5 of 31; fades by class: Step N 44, card 17, Step Nc 4.
- Data caveat for anyone reusing the digests for motion or framing: digest MOVE directions are in the part's local frame and digest visible_parts uses chain visibility and counts every jumper as a part. *Evidence:* LSM Full [065] is listed as 22 mm down while renders [064]-[066] show the support rising to the matrix. The chain-visibility model matches the render box within 4 % on 161 of 333 clean frames against 256 of 333 for leaf-own visibility. Digest reports 0 parts on the PMG '4-Digit Display' card (PMG Part 2 [001], PMG Full [034]) although the display is on screen.

### Numbers (as corrected by the re-check)

| Setting | Value | Basis |
|---|---|---|
| Camera projection | perspective, 45 deg vertical FOV, no roll, look-at target (confirmed) | FOV 45 on 1036 of 1037 (LSM Part 1 [011] = 50); roll against declared up-axis 0.0 deg and look-at error 0.0 deg on 1037 of 1037 |
| Camera move duration and easing | 800 ms tween, no orbit animation (confirmed); 61 of 325 moves also carry a step-level fade | All 325 moves in 800 ms steps; animation options identical on 1037 steps (strings on 1035, typed on 2) |
| Default elevation | 34 deg (20-50 on 87 % of steps) (confirmed) | Median 34.1 of 1037 steps, mean 34.0 of 345 views; 903 in 20-50, 983 in 15-55 |
| Elevation by step kind | rigid insert 33; arrow 35; eye-only 41; wiring PMG 21-30, LSM 15-38 (median 27), LAC 48-57 on four of seven construction wiring views (others 24, 29, 35) | Medians over 149 / 86 / 79 / 109 Step N; LSM wiring views at 15, 19, 20, 23, 27, 28, 30, 36, 38; LAC at 24, 29, 35, 48, 51, 54, 57 plus 47 in the deconstruction |
| Azimuth | LSM and LAC: a diagonal (+-45 or +-135) within 15 deg on 84-87 % of views. PMG: no default class (38 % diagonal, 38 % cardinal). Title pages: diagonal in all kits | 215 of 299 +y views overall; LSM 108/129, LAC 75/86, PMG 32/84 (32 cardinal, median offset 21.5 deg); 19 of 19 title pages |
| Kit hero azimuth (title page) | LSM +50 to +57; LAC +141 to +143; PMG -43 to -60 (confirmed) | 7 of 8 LSM (Part 1 at -141), 5 of 6 LAC (Part 1 at +49), 5 of 5 PMG Start steps |
| Zoom ladder ratio | x1.166 per level (confirmed; exactly 1.1664 = 1.08 squared) | 992 of 1035 steps on the ladder; 93 of 99 near-single-level moves are 1.1664; other ratios fit at most 544 steps |
| Usual orbit distances | LSM 163-189 mm (breadboard), 258-300 (housing), 350-374 (stack and stems); LAC 277-323 (wiring), 377-440 (enclosure); PMG 173-202 (wiring), 275-320 (case) (confirmed) | Distance counts per kit; in-context Step N medians wiring 189 / 277 / 173 (n 21 / 44 / 41), rigid inserts 300 / 377 / 275 (n 58 / 39 / 36) |
| Fit distance | depth to content centre = 2.4 x half-diagonal of the seated content (hover part excluded); 2.2 x when the hover part is included | 214 validated completed frames: median 2.42, IQR 2.10-2.67 (0.92 x sphere fit); 213 view-entry frames with hover part: 2.22, IQR 1.94-2.54; by kit 2.44 / 2.36 / 2.19 |
| Content height in frame | 0.61 of frame height (IQR 0.51-0.74); LSM 0.57, LAC 0.71, PMG 0.54 (confirmed) | 398 annotation-free Step Nc renders; 0.54-0.63 across six distance bands (259 views) |
| Content width in frame | 0.41 of frame width at about 2:1 (IQR 0.34-0.56) (confirmed) | 398 Step Nc renders; 917 of 1037 renders between 1.95:1 and 2.07:1 |
| Content centre on screen | (0.49, 0.47) (confirmed); PMG less reliably centred | Median box centre of 398 clean Nc renders; 315 within 0.40-0.60 on both axes (LSM 114/130, LAC 128/151, PMG 73/117) |
| White margins (model only) | top 0.18, bottom 0.21, left 0.28, right 0.30 (confirmed as medians); no margin on at least one side in 16 % of frames | 398 clean Step Nc renders; 65 touch an edge |
| Top margin with hover part and labels | 0.12; hover part top edge median 0.13, at least 0.03 on 89 % of rigid inserts, minimum 0 (touching the edge) | 425 Step N renders; 149 rigid-insert action boxes: median 0.131, 10th percentile 0.026, 16 under 0.03, minimum -0.004 (LSM Full [071]) |
| Action volume placement | centre (0.49, 0.45), height 0.43 of frame, inside the frame on 419 of 422 (421 of 422 after removing two reprojection artefacts) | 422 Step N / Nc pairs by own 3D reprojection; rigid inserts: destination centre (0.49, 0.47), hover-part centre (0.49, 0.30) |
| Travel axis to view axis | at least 40 deg always, 45 deg or more on 96 %, typical 59 deg | 176 direction-merged rigid translations of 10 mm or more: median 59.2, IQR 56.1-63.5, minimum 41.2, 7 under 45, none under 30 |
| On-screen travel length | about 0.26 of frame height per leg (IQR 0.19-0.32) | 176 legs: median 0.25; rigid-insert legs (125): median 0.27, IQR 0.21-0.33 |
| Typical camera move | orbit 61 deg, target shift 42 mm (0.15 x distance), elevation change 9 deg (over 15 deg on a quarter), zoom unchanged or one ladder level on 57-60 % | 266 Step N moves; elevation change over 238 moves with unchanged up-axis: median 8.7, IQR 3.2-14.8; zoom none 93 + one level 93 of 325 (195 counting half levels) |
| Steps per camera view | median 2, mean 3.0 (parts 2.6, full builds 2.9-3.0, deconstructions 4.2) (confirmed) | 345 views over 1037 steps: 2.63 / 2.95 / 4.19 |
| Wiring run | 1 camera per wiring block in one work area (a block can span several modules) | 26 of 30 label runs, 21 of 25 multi-wire runs; 72 of 79 later wire steps reuse the camera; longest 12 wires / 27 viewer steps across four PMG button modules |
| Isolated close-up distance | median 175 mm (IQR about 130-224) | 56 isolated views by leaf visibility (3 or fewer top-level parts): median 175, IQR 127-224; true isolation is under-counted because ribbon cables count as many parts |
| Zoom-out when context returns after a card | x1.36 median, range x0.86-x4.48; 22 of 31 pull back at least one level (confirmed, wide spread) | 31 card-to-next-step transitions |
| Section card fill | height 0.63 of frame, centred (confirmed) | 31 cards: median 0.63, IQR 0.60-0.70; centred on 30; exceptions 0.34-0.37 on four PMG cards |
| Title page model placement | centre x 0.71, centre y 0.48, height 0.67 of frame, elevation 35 (confirmed) | 19 Start steps by own 3D reprojection: x 0.67-0.75 on 18; height 0.60-0.74 on 17; left edge 0.34-0.60 |
| Final view | centred (0.47, 0.47), height 0.67, elevation 39, title-page distance or one to three ladder levels closer, azimuth within about 15 deg of the title page on 15 of 19 | 19 final steps: same distance 9, x1.17 closer 3, x1.59 closer 4, x1.85-1.98 closer 2, farther 1; elevation within 3 deg of Start in 11, 10-20 deg higher in 7 |
| Underside / side work | re-declare the up-axis for the block; effective elevation 22-47; camera turn at the flip about 100 deg (confirmed) | 148 steps, 39 up-axis changes (43-167 deg, median 102); 110 of 110 below-horizon steps have a re-declared up-axis; 132 of 148 in 22-47 deg |
| See-through check view | covering parts at 50 % opacity, elevation 57 (confirmed, single authored case) | Raw opacity 0.5 on base and one side wall at LSM Full [075], Part 3+4 [030], Part 4 [016] only |
| Camera-only auto step | 800 ms, auto-advance, navigation overlay hidden, hidden from step picker, no annotations (confirmed) | 12 of 12 camera-only Transitions; 7 of them switch off one leftover annotation on entry |

### Open questions

- Is the x1.166 zoom ladder a deliberate convention or just the Cadasio editor's zoom increment? LSM's ladder is half a level offset from LAC/PMG, which suggests a tool artefact; the in-house player could use a continuous fit and still match the look.
- How does the live viewer adapt a saved camera to a different window shape (classroom tablets vs wide monitors)? Renders were saved at ten aspect ratios and the 45 deg FOV is vertical, so wide content may crop on narrow screens. Not testable from the data on disk.
- When should a turn-over get its own camera-only auto step? LSM does this for all 8 of its Transition-based re-orientations, but LAC and PMG flip the model directly on a Step N (28 of 39 up-axis changes). No threshold by angle is supported by the data.
- Should the in-house player add an explicit 'turn the kit over' cue? None of the 39 up-axis changes carries one; the camera swing is the only signal, and engraved part IDs simply render upside down.
- Why is the camera re-aimed on about two thirds of mechanical steps even when the action would already be in frame (64 of 99)? The likely reason is facing the mating features, but the choice of quadrant is hand-made; an auto-camera needs a visibility score that I could not derive from camera data alone.
- The orbit target is not the content centre (median offset tens of mm, and far behind the part on some isolated views). Is target placement deliberate (e.g. to leave room for a staged wire or labels) or incidental to how the author navigated? This affects how user orbiting feels in the player.
- Is the larger bottom margin (0.21 vs 0.18 top on completed frames) intentional room for the bottom navigation bar? The difference is small and hover frames reverse it at the top; evidence is weak.
- Step-level cross-fade on scene swaps is used on about half of LSM and LAC swaps and never in PMG (the newest kit). Which behaviour does TechBox want as the standard?
- My 3D re-projection matches the saved renders within 4 % on 300 of 398 clean frames; the rest over-estimate extents (hidden staging instances, scaled parts). Millimetre-based figures (fit ratio 2.4, action sizes) carry that uncertainty; render-based framing percentages do not.
- Deconstruction final views are inconsistent (LSM and LAC orbit to a centred hero of what is left; PMG leaves the last working view). Which should the player follow?

## Visual style and the part colour library

### STYLE-1 · qualified

**Render every part with flat two-tone toon shading and thin black outline edges on a pure white background; no shadows, ground plane, textures, gloss or silhouette pass. Edge crease angle is 40 degrees by default, but PMG raises it to 69 degrees per part on jumper-wire bodies.**

- Applies to: all step types (construction, deconstruction, wiring, mechanical, cards, title page); all three kits
- Evidence: toon style on 579,103 of 579,220 visible solid-steps (99.98%); edge style normal on 579,042 (99.97%); edge colour #000000, width 1, crease angle 40, silhouette none in 20/20; scene render style 'matt' at scene level but overridden per part. Computed by walking every step of all 20 raw payloads (styleop.py).
- Exceptions: 117 solid-steps with style unset/default (one wire solid on the LSM Full [087] and Part 4 [028] Completed View; D2 panel and USB plug solids in LSM Part 2, 1+2, 3+4) and 61 solid-steps with edge style unset in PMG Part 3/Full/Decon; none noticeable. scene_edge_style is 'normal' in the 7 LAC guides and 'none' in the other 13, with no visible difference because edges are set per part.
- Narrowed because: Per-part edge_angle 69 on 3,941 of 4,148 PMG wire solid-steps (95%) and 48 on 54; none in LSM/LAC. The default-style wire is in three guides, not two: LSM Full [087], Part 4 [028] and Part 3+4 [042]. scene_edge_style is 'normal' on one LSM Full step ([008]), so 'none in the other 13' has one exception. Other exceptions as the analyst listed (114 style-unset, 61 edge-unset).
- As first stated: Render every part with flat two-tone toon shading and thin black outline edges on a pure white background. No shadows, ground plane, textures, gloss or silhouette pass.
- Why it helps students: A line-drawing look like a printed manual: shapes read by outline, nothing competes with the red and cyan annotations, and it prints and projects cleanly in a classroom.
- For our player: Default material = unlit-looking toon with a 2-step ramp plus an edge pass (crease angle 40 deg, 1 px black, about 1-2 px on a 2,560 px wide view). White clear colour. No shadow maps, no environment, no floor.

### STYLE-2 · confirmed

**Compute the two tones as pixel = min(255, base x (0.2 x ambient + 0.8 x directional x tone)) per sRGB channel, with tone 1.0 on lit faces and 0.7 on shaded faces.**

- Applies to: all parts, all kits
- Evidence: 12 colour/frame pairs across the four lighting set-ups match within 2 levels per channel (toonval.py). Multipliers: LAC 1.150 lit / 0.910 shade (ambient 1.75, dir 1.0); LSM Part 1/2/1+2 1.175 / 0.935 (1.875, 1.0); LSM Part 3/4/3+4/Full/Decon 1.200 / 0.960 (2.0, 1.0); PMG 1.295 / 1.019 (1.875, 1.15). Light colours #333333 ambient and #cccccc directional in 20/20.
- Exceptions: The 0.7/1.0 tones and additive form are measured; the N.L > 0.4 switch point is the three.js default for this ramp and was not measured. Bright colours clip (white is #ffffff lit in every kit and also shaded in PMG).
- Why it helps students: Lit faces come out brighter than the stored colour and shaded faces only slightly darker, so parts stay light and legible and never go muddy; black parts keep visible outlines.
- For our player: Implement the ramp exactly (two tones 0.7 and 1.0, no gradient texture) in sRGB space and expose ambient/directional intensity as scene settings. Store base colours from the library; do not store screen colours. Choose one lighting preset (suggest ambient 1.875, directional 1.0).

### STYLE-3 · qualified

**Light with one directional light whose position is stored in step data (light_directional.position, aimed at the world origin); a face is lit when N.L > about 0.4. PMG stores it once: unit (-0.69, 0.61, 0.38), 38 degrees elevation, so top faces and the wall family facing the light are lit. LSM and LAC re-store it on 2-13 steps per guide, roughly from the viewer's side. On +y steps top faces are always lit; on a flip to -y with no new stored light the lighting flips with the up-axis; on LAC's -x steps the up-facing side can be shaded.**

- Applies to: all kits; underside/flipped views in LSM, LAC, PMG
- Evidence: 11/11 frames checked. In PMG (scene_light_follow_camera = false, 5/5 guides) every vertical face sampled is shaded (Part 3 [023]: H1, H2, H8, rear wall #e3bb8b; deck #ffeeb0).
- Exceptions: In LSM and LAC (flag unset, 15 guides) some vertical faces are lit and it depends on the camera: LSM panel D5 (normal +X) is lit in Full [000] at azimuth 54 and shaded in Part 3 [012] at azimuth 35; LAC F1 lit and F5 shaded in Part 4 [034]. No single world-fixed or camera-relative direction fitted the 16 faces tested in 6 frames.
- Narrowed because: LAC Decon [031] Step 12 (up-axis -x): the up-facing edge of F1 is the shaded tone #c9a77a while the +Y face is lit #ffd49c. 'In PMG every vertical face sampled is shaded' is wrong: H1 outer face is lit in PMG Part 3 [001] [002] [004] [008], rear wall lit in [030]; it holds on [023]. After a -y round trip the horizontal part of the light is not restored (PMG Part 3 [023], [030]); LSM Part 3 [012] matches the stored light rotated with the +x to +y change. Up-axis is not only for underside views: 148 of 1,037 steps are not +y (-x 68, -y 53, +x 21, -z 6). Live-viewer behaviour between stored positions is not settled from disk.
- As first stated: Light the scene from its up side: faces pointing along the scene up-axis get the lit tone; when the up-axis is flipped for an underside view, the lighting flips with it.
- Why it helps students: The surface a student would see as 'the top' is always the bright one, including when the model is shown turned over, so orientation reads consistently.
- For our player: Tie the directional light to the scene up-axis (rotate it when a step re-declares up). Use the PMG behaviour (light along up, vertical faces shaded) as the default until the LSM/LAC camera-follow behaviour is confirmed in the live viewer.

### STYLE-4 · qualified

**Give each material region one flat colour and keep it for that part across the guides of a kit. LSM and LAC are repainted from a house swatch set (about 77% and 84% of visible solids overridden); PMG mostly keeps CAD colours (17%). Wood is #deb887 in every guide that shows wood (18 of 20).**

- Applies to: all parts; LSM, LAC, PMG
- Evidence: Share of visible solids whose colour is a Cadasio override rather than the CAD colour: LAC 84% (6,293/7,512), LSM 76% (7,774/10,246), PMG 17% (2,014/12,113). #a6a9aa is the most used override (6,482 solid-in-guide instances in LSM + LAC). 92% of the 29,364 colour overrides are applied at or before the first viewer step.
- Exceptions: 15 between-guide differences, mostly between the two LSM projects: Nano header strips #1e1616 (Part 1/2/1+2) vs #181818 (Full) vs #000f41 (Part 3/4/3+4/Decon); Nano USB shell #a6a9aa vs #f5f5f6; capacitor can and 8x8 matrix board #000000 vs #1e1616; male Dupont pin #cccccc vs #a6a9aa vs #e4e4e4 (PMG); housings #1e1616 vs #000000 (PMG); LAC pot can #808080 and knob cap #e4e4e4 on later pose copies; PMG shield's built-in Nano copy teal #002e37.
- Narrowed because: 'Wood in 20/20' is wrong: PMG Part 1 and Part 2 show no wood solid. 'Small swatch set' is 28 (LSM), 45 (LAC) and 53 (PMG) distinct hexes on screen; 8, 12 and 11 of them cover 90% of solid-steps.
- As first stated: Give each material region one flat colour from a small swatch set and keep it identical for that part in every guide of the kit.
- Why it helps students: A part looks the same in Part 1, the full build and the take-apart guide, so students recognise it instantly and can match it to the real kit item.
- For our player: Ship one material table keyed by part and sub-feature (reports/_work_dim_style/colour_library.json) and reference it from every guide; do not allow per-guide colour edits. Lint for solids left at the CAD default #cad1ee.

### STYLE-5 · confirmed

**Model every printed or engraved marking as its own flat decal solid with its own colour, never as a texture.**

- Applies to: wood panels, breadboard, resistors, capacitor, switch, 7-segment display; all kits
- Evidence: 100% of markings in the three CAD models are zero-thickness surface solids offset about 0.1 mm from the body; 0 textures.
- Why it helps students: Markings stay crisp at any zoom and can be pointed at individually by an eye icon or leader (resistor band, polarity stripe, panel ID).
- For our player: The asset pipeline must keep decals as separate meshes (with a small depth offset to avoid z-fighting) and let annotations anchor to them.

### STYLE-6 · qualified

**Never recolour, tint, highlight or dim a part to draw attention. Colour changes on visible parts are corrections only (156 solid changes, 155 on leaving the Start page and 1 on a build step). Part size is changed on two info cards.**

- Applies to: construction and deconstruction, all kits
- Evidence: 156 visible-solid colour changes out of 579,220 solid-steps across 20 guides; 0 during build steps (colchange.py).
- Exceptions: None intentional.
- Narrowed because: '0 during build steps' is off by one: PMG Part 3 [045] is Step 22 (shield pose copy #000f41 to #224bbe), a correction. Per-part scale is used for emphasis on cards: LSM Part 1 [011] Capacitor card scales the capacitor x2 (with FOV 50), reset on [012]; the Mini USB Cable card (LSM Part 2 [027], Part 1+2 [043]) scales the plugs x0.95, reset next step.
- As first stated: Never recolour, tint, highlight or dim a part to draw attention; a part looks the same when new, hovering, seated or finished.
- Why it helps students: Colour always means 'what the real part looks like', so students are never confused by a highlight colour that does not exist on their desk; attention is carried by the red/cyan annotations instead.
- For our player: No 'highlight new part' feature by default. Per-step colour animation is not needed; colour is a static property of the part.

### STYLE-7 · qualified

**Use transparency only to look through covering panels, at 50% opacity, on the single hover step that needs it (LSM only, viewed from underneath). The panel bodies return to opaque on the following completed step.**

- Applies to: mechanical steps viewed from underneath; LSM only
- Evidence: 30 solid-steps at opacity 0.5 (5 solids x 2 steps x 3 guides); all other 579,190 solid-steps opacity 1.
- Narrowed because: The breakdown is not 5 solids x 2 steps. Hover step (Full [075], 3+4 [030], Part 4 [016]): 6 solids at 0.5, the base body + 2 ID decals and side wall LSM_Side4 body + 2 decals. Next step ([076], [031], [017]): both bodies back at 1.0, only the 4 decals still at 0.5 until the following Transition, which is a leftover. Under the digest visibility rule the side wall is not counted and the total is 15.
- As first stated: Use transparency only to look through a covering part, at 50% opacity, and only on the step that needs it.
- Why it helps students: Lets the student see the tabs coming through the base without removing the base from the picture.
- For our player: Support a per-part opacity value per step (default 1, ghost 0.5) with correct blending of edges; it is rare, so it can be a simple property rather than a mode.

### LIB-WOOD · qualified

**Colour all laser-cut wood #deb887 and engrave the part ID as near-black #1e1616 zero-thickness decals (2 per panel, 3 for two-digit IDs); leave the wood otherwise unmarked. Applies to the 18 guides that show wood.**

- Applies to: mechanical / enclosure parts; LSM (D1-D11, stems), LAC (F1-F9), PMG (H1-H14, H9 keys)
- Evidence: Panel body #deb887 on 100% of wood-body solid-steps in 20/20 guides; ID decals #1e1616 100% in LSM and LAC, 98% in PMG; 2 decals per panel, 3 for two-digit IDs. Rendered as #ffd49b/#caa77b (LAC), #ffd89f/#d0ac7e or #ffdda2/#d5b182 (LSM), #ffeeaf/#e2bb8a (PMG).
- Exceptions: LSM button panel D2 has a full-face overlay #855e42 on its outer face (7/7 LSM guides that show it); no other panel in any kit has a second face colour. LSM light-guide stems are #ffffff. One PMG H14 pose copy has a decal left wood-coloured. The LSM backing sheet reappears inside the housing recoloured #deb887 (stray).
- Narrowed because: Not 20/20: PMG Part 1 and Part 2 have no wood; LAC Electronics has panels on [001] only. The PMG exception is misdescribed: H14 carries 6 ID decals (two copies of the ID) and one whole copy, 3 decals, is left #deb887 on 5 steps (Part 3, Full) or 3 steps (Decon). The D2 overlay is two #855e42 solids (50.8 x 95.3 mm and 3.4 x 4.9 mm).
- As first stated: Colour all laser-cut wood #deb887 and engrave the part ID on each panel as near-black #1e1616 decals; leave the wood otherwise unmarked.
- Why it helps students: One warm flat colour makes every wooden piece read as 'wood' against electronics, and the engraved ID is the only way parts are named in the wordless guides.
- For our player: Material 'wood' = #deb887 flat, no grain, no burnt-edge colour (edges are just the shaded tone). Part IDs are geometry decals in #1e1616.

### LIB-BOARDS · confirmed

**Colour circuit boards by board type: Arduino Nano and PMG button modules navy #000f41; Nano I/O shield and TM1637 display #224bbe (matrix #234bbf); RTC module #0074d9; LCD #1a7e26; black boards #1e1616. Header plastic near-black, pins light grey, IC bodies #191919.**

- Applies to: electronics in all kits
- Evidence: Nano PCB #000f41 in 20/20 guides. Shield PCB #224bbe 5/5 PMG; all shield header blocks #ffff80 (3-pin #fffc9f) with pins #e3e3e3, socket strips #181818, DC jack #000000, capacitor #191919. RTC: PCB #0074d9, holder/ICs #191919, pins #f4e5a7, coin cell #a6a9aa. LCD: PCB #1a7e26, bezel #1e1616, glass #cccccc, pins #a6a9aa. PMG button module: PCB #000f41, switch #1e1e1e, caps #000000/#ffdc00/#ffffff/#0074d9. PMG matrix: blocks #ffffff, mask #1a1a1a, dots #e4e4e4.
- Exceptions: Nano header strips are navy like the board in LSM Part 3/4/3+4/Decon. Nano pins #a6a9aa in LSM/LAC but #e4e4e4 in PMG; ICSP pins gold #c8b273 only in LSM; USB shell #a6a9aa / #f5f5f6 / #cccccc / #e4e4e4 depending on project. Shield header rows are all one yellow (matches the product photo on the PMG Part 1 [001] card).
- Why it helps students: Each module has a distinct board colour, so students can tell the Nano from the shield or the clock module at a glance even at small size.
- For our player: Split each board asset into PCB, header plastic, pins, ICs, connectors and passives as separate material slots and fill them from the library; pick one Nano palette (suggest LSM Part 1 / LAC values).

### LIB-HARDWARE · confirmed

**Colour all metal #a6a9aa, all black plastic #1e1616 (cable jackets and black leads #2d2926), resistor bodies #0074d9 with real band colours, and the breadboard white with black legends and red/blue rail lines.**

- Applies to: breadboard, passives, USB cable, switches, potentiometer, buzzer, fasteners; LSM and LAC (USB cable also PMG)
- Evidence: Breadboard body #ffffff, decals #000000, rails #ff0e00 / #0074d9, backing #aaaaaa (same in all LSM and LAC guides). Resistor body #0074d9, leads #a6a9aa; 12k bands #a36315,#ff0e00,#000000,#ff0e00,#a36315; 330R bands #ff851b,#ff851b,#000000,#000000,#a36315. Capacitor stripe/legs #a6a9aa. USB plugs #1e1616, cable #2d2926, A-shell #a6a9aa, tongue #ffffff. Rocker body #1e1616, legend #ffffff. Pot can #a6a9aa, base #855e42, knob #1e1616, nut/washer #a6a9aa. Buzzer #1e1616. LSM button body #1e1616, flange #cccccc.
- Exceptions: Capacitor can #000000 in LSM Part 1/2/1+2 vs #1e1616 later. PMG USB cable #1e1616 and tongue #e4e4e4. Mini-B tip is four different greys/whites across projects. Unpainted CAD-default solids on screen: LSM button terminal tabs, one USB plug solid, straight resistor leads, LAC SMD 0805 bodies (0.4-1.4% of solid-steps in affected guides).
- Why it helps students: Value-carrying details (resistor bands, polarity stripe, rail colours) are the real colours students must check on the physical part.
- For our player: Use the library values directly; treat #cad1ee as an error colour in asset validation.

### LIB-WIRES · qualified

**Colour Dupont housings black with light-grey pins whatever the wire colour, and give each jumper wire its own colour; colour carries identity, not electrical function. Holds in the 19 guides that have wires.**

- Applies to: wiring steps; LSM, LAC, PMG
- Evidence: Housings #1e1616 (LSM, LAC) or #000000 (PMG) in every guide; male pins #a6a9aa / #cccccc / #e4e4e4. 40 distinct wire-body hexes (LSM 6, LAC 13, PMG 23). LSM ribbon: #ffffff, #b1b3b3, #4e008e. LAC 6-way: #2d2926, #10cc62, #611b6c, #0074d9, #cccccc, #800000; pair #ff851b, #eac80d; LCD ribbon #611b6c, #eac80d, #13a3a3, #0074d9; pre-wired leads #ef3340, #b28362, #2d2926. PMG 12-way: #b70101, #e4e4e4, #343232, #21f17a, #7c5a30, #ffdc00, #85144b, #737980, #3876ac, #a75294, #ff4136, #3d9970; 9-way: #ac9400, #000000, #ab53ca, #bb3d3d, #411900, #339f3f, #2a2f62, #662639, #377e89. Wire bodies about 58 mm long, 1.2 mm diameter.
- Exceptions: Same nominal colour is a different hex per kit (purple #4e008e / #611b6c / #ab53ca). LAC loose vs routed models differ: green #2ecc40 vs #10cc62, grey #aaaaaa vs #cccccc. PMG dark wires (#000000, #411900, #662639, #343232) are hard to tell apart; white wire is nearly invisible on the white background.
- Narrowed because: LSM Part 1 has no wires or housings, so 'every guide' is 19. 12 solid-steps of unpainted #cad1ee/#cad1ed housing on the first/last steps of LSM Full, Part 3+4 and Part 4. The analyst's report gives both 40 and 44 for the wire hex count.
- As first stated: Colour Dupont housings black with light-grey pins whatever the wire colour, and give each jumper wire its own saturated colour taken in ribbon order; colour carries identity, not electrical function.
- Why it helps students: The student picks 'the purple wire' from the ribbon; uniform black housings keep the wire colour the only distinguishing feature and match the real jumper wires.
- For our player: Wire colour is a per-wire property shared by the loose and routed models (enforce equality). Define one TechBox ribbon palette with enough contrast between neighbours and against white; housings and pins are fixed materials.

### STYLE-10 · qualified

**Use #ff0000 for motion annotations (lead lines, arrows) and light cyan #7fdbff for pointing annotations (underlines, leaders, anchor rings, inset frames); text and the eye icon are black. Cyan is exclusive to annotations; red is not, because parts carry a near-identical red.**

- Applies to: all annotated steps; 19 guides (LAC Electronics has no annotations)
- Evidence: 362/362 lead lines and 104/104 arrows #ff0000; 212/212 label underlines #7fdbff with black bold text; 491/498 anchor rings #7fdbff; 454 leaders #7fdbff plus 42 with no stored colour that render cyan; 44/46 inset frames #7fdbff; one black eye PNG used 224 times in 19 guides (annos.py over the 1,010 annotation objects ever shown).
- Exceptions: Anchor rings #39cccc x3 (LSM underside step), #ff5F0B x2 (PMG Push Buttons card), #7fb9ff x2 with matching frame and leader (one PMG inset). Quantity label is #7fdbff in LSM ('64X'/'64x') but #0074d9 in LAC ('2x'). Some wires and lead stubs are also red (#ef3340, #b70101) but never pure #ff0000.
- Narrowed because: Part colour #ff0e00 (breadboard (+) rail lines and resistor bands) is on 2,861 solid-steps in 15 guides and #f40000 on 45; on screen these read as the same red as a lead line. No solid is within 25 levels of #7fdbff. Small counts: 503 anchored objects (5 more are black 'Basic Circle' anchors on quantity labels, not drawn in LSM Part 4 [023]); the eye PNG is used 225 times, one inside a frame.
- As first stated: Reserve pure red #ff0000 for motion annotations (lead lines, arrows, highlight boxes inside pictures) and light cyan #7fdbff for pointing annotations (label underlines, leaders, anchor rings, inset frames); text and the eye icon are black.
- Why it helps students: Two colours with fixed meanings: red = 'this moves along here', cyan = 'look here / this is called'. Neither colour is used as a wood, board or housing colour, so annotations never blend into the model.
- For our player: Hard-code two annotation theme colours (motion #ff0000, callout #7fdbff) and black text; do not expose per-annotation colour pickers. Keep #ff0000 out of the part palette.

### STYLE-11 · confirmed

**Set callout labels in a bold sans at 3em of a 20 px base, black, centred on a 5 px cyan underline, with a 5 px straight cyan leader from the underline end nearest the target to a 30 px dashed ring.**

- Applies to: wiring and breadboard-insertion steps; LSM, LAC, PMG
- Evidence: 212 underline labels in 12 guides: bold 212/212, black 212/212, centred 210/212, 3em 175 / 2.5em 37 (older LSM), underline thickness 5 in 210, leader thickness 5 in 188/190, leader starts at an underline end in 208, box 175 px wide in 177 (175 x 90 default). Eye icon width 7.81% of viewport (142) or 8.2% (62, all PMG). Inset frames: 5 px border, corner radius 0.1, width median 17.6% (7.8-36.7).
- Exceptions: Font family: explicit Arial in LSM and LAC build guides (124 labels); none stored in PMG and LAC Deconstruction (88 labels), which therefore render in the project default Public Sans Medium (confirmed in LAC Decon [049]; the reader report calls these Arial). LSM Full mixes 3em and 2.5em. Quantity labels are Arial bold 6em with no underline or leader (5).
- Why it helps students: Short, large, high-contrast text (a hole or pin name) readable from the back of a classroom, with no box to hide the model.
- For our player: One label component: bold sans (pick Arial or Public Sans), 60 px on a 2,560 px wide view (about 2.3% of width), underline + leader + ring in #7fdbff at 5 px. Scale with viewport width so it stays the same relative size.

### STYLE-12 · confirmed

**Build the title page from two flat images on white: the TechBox logo top-left and a title / part / copyright block lower-left, with the finished model of that guide on the right in the normal render style.**

- Applies to: Start step of every guide except LAC Electronics; all kits
- Evidence: 19/19 guides with a title page use the same logo SVG (white wordmark on a rounded #00b0ef panel) at x 1.8-2.5%, y 4-8%, width 33.2% (LSM Part 1/2/1+2), 37.6% (other LSM), 38.9% (LAC), 39.5% (PMG); title PNG with #585858 text at x 1.6-3.8%, y 61-65%, width 42.1-48.4% in 18/19. No frame, leader or anchor on any of the 38 images.
- Exceptions: LSM Part 1 title block at y 24%, width 58.3%. PMG Decon logo at x 5.1%, width 36.4%. Title and copyright fonts are baked into the PNG (heavy condensed sans and a serif) and cannot be identified from data.
- Why it helps students: Shows what will be built before step 1, with consistent branding across kits.
- For our player: Title-page template with two image slots in viewport percentages (logo 2%/6%, ~38% wide; title 2%/63%, ~44% wide) and the hero model framed in the right half. Prefer live text over a PNG so titles stay consistent.

### STYLE-13 · confirmed

**Use a 45 degree perspective camera everywhere.**

- Applies to: all steps, all kits
- Evidence: 20/20 guides; 1 step with FOV 50 (LSM Part 1 [011] Capacitor card, back to 45 on [012]).
- Exceptions: The single FOV 50 card, a late insertion.
- Why it helps students: A constant lens keeps part proportions familiar from step to step.
- For our player: Fix FOV at 45 degrees (vertical) and do not expose it per step.

### Added by the re-check

- The light position is authored per step: step properties carry light_directional.position, and the lit faces follow unit(position) with a 0.4 threshold. PMG sets it once; LSM and LAC re-store it on 2-13 steps per guide. *Evidence:* 59 set events in 20 guides. 24 of 24 faces match in 9 frames, including the pair the analyst could not explain (LAC Part 4 [034], F1 lit and F5 shaded) and LAC Decon [031]. Median angle between stored light and camera: LAC 37, LSM 54, PMG 31 degrees.
- PMG softens outlines on jumper wires by raising the per-part edge crease angle to 69 degrees. *Evidence:* edge_angle 69 on 92-100% of wire solids in each PMG guide (3,941 of 4,148 wire solid-steps); absent in LSM and LAC.
- Info cards may change part size: per-part scale is set for one step and reset on the next. *Evidence:* LSM Part 1 [011] Capacitor card: capacitor scale 2 plus FOV 50, reset on [012]. Mini USB Cable card (LSM Part 2 [027], Part 1+2 [043]): plugs scale 0.95, reset next step.
- The scene up-axis is re-set often and to four different axes, not only flipped for underside views. *Evidence:* 148 of 1,037 viewer steps are not +y: -x on 68 (all LAC), -y on 53, +x on 21, -z on 6 (LSM plan views looking straight down).
- The digest's visibility rule undercounts what is on screen; a solid is shown when its nearest explicit visible flag is true, even under a CAD-hidden parent. *Evidence:* 501,702 vs 579,220 solid-steps. LSM Part 4 [016] shows side wall LSM_Side4 (CAD-hidden parent). The LCD PCB #1a7e26 has 0 visible solid-steps under the digest rule in all 5 LAC guides but is on screen.
- Annotation red is not unique on screen: parts use a near-identical red. *Evidence:* #ff0e00 on breadboard (+) rails and resistor bands, 2,861 solid-steps in 15 guides; #f40000 on 45. No solid is near #7fdbff.
- Some stored annotation properties do not render and should not be copied as conventions. *Evidence:* shadow_enabled true on all 212 label containers with no shadow in LAC Part 1 [019]; black Basic Circle anchors on the 5 quantity labels not drawn in LSM Part 4 [023]; 36 lead lines stored dashed render solid (LSM Part 4 [019]).
- Anomaly: the late LSM project scales two 8x8 matrix pose copies from step 0. *Evidence:* scale 0.95 on 323 solids of '8x8 LED-3' and 1.03 on 323 of '8x8 LED-4' in LSM Full, Decon, Part 3, Part 3+4, Part 4.

### Numbers (as corrected by the re-check)

| Setting | Value | Basis |
|---|---|---|
| Edge crease angle | 40 degrees scene default (20/20); 69 degrees per part on PMG jumper wires | edge_angle 69 on 3,941 of 4,148 PMG wire solid-steps, 48 on 54; none in LSM/LAC |
| Toon switch point | 0.38 < N.L threshold <= 0.46 (measured; consistent with 0.4) | N.L from stored light: 0.38 and 0.29 shaded, 0.46 and 0.63 lit, in 4 frames |
| Directional light direction | unit(light_directional.position), aimed at world origin; PMG fixed at (-0.69, 0.61, 0.38), 38 degrees elevation | 59 stored positions in 20 guides; 24/24 faces match in 9 frames; LSM has 21 and LAC 5 distinct directions, median elevation 41-44 degrees |
| Ghost opacity | 0.5 on panel bodies for 1 viewer step; ID decals linger 1 more step | 6 solids on the hover step and 4 decals on the next, in 3 LSM guides (30 solid-steps) |
| Wood | #deb887 in 18 of 18 guides that show wood | PMG Part 1 and Part 2 contain no wood solids |
| Lead line width | scale 5, screen-space; 4-5 px (mode 5) regardless of render width | Run lengths on LSM Part 4 [019] at 2,559 px and PMG Part 3 [023] at 3,840 px |
| Anchor ring | Life Saver Circle 30 x 30 px on 498; plus 5 black Basic Circle anchors on quantity labels (not drawn) | 503 anchored annotation objects |
| Eye icon width | 7.81% of viewport width (143) or 8.2% (62, all PMG) of 225 uses | One PNG asset, 225 objects in 19 guides, one of them framed |
| Title block position | Image box x 1.6-3.8%, y 61-65%, width 42-48% in 18/19; visible text at y 62-87% in 19/19 | LSM Part 1 PNG is padded; measured text extents on 6 Start frames |
| Title text colour | #585858 (18/19); #5b5b5b in PMG Deconstruction | Dominant grey in the title region of all 19 Start renders |
| TM1637 PCB | #224bbe in the 4 PMG guides that show it | PMG Part 1 does not show the display; shield PCB is 5/5 |
| Decal offset from body | 0.127 mm (LSM and PMG panels), 0.249 mm (LAC panels), under 0.06 mm (breadboard) | Bounding boxes of decal vs body solids in the three full builds |
| Visible solid-step base | 579,220 on the nearest-flag rule; 501,702 on the digest's all-ancestors rule | Both recomputed; renders support the nearest-flag rule |
| Render width behind pixel figures | 2,559-2,560 px for LSM/LAC; 1,920, 2,560 or 3,840 px for PMG | Sizes of thumbs_raw frames sampled across all guides |

### Open questions

- Light direction in LSM and LAC: up-facing faces are always lit, but some vertical faces are lit depending on the camera (LSM D5 lit at azimuth 54 in Full [000], shaded at azimuth 35 in Part 3 [012]). scene_light_follow_camera is unset there and explicitly false in PMG, where vertical faces are shaded. No single light vector fitted 16 faces in 6 frames; the live viewer needs to be orbited to settle whether the light follows the camera.
- Is the difference in light intensity between kits (ambient 1.75 / 1.875 / 2.0, directional 1.0 / 1.15) intended? It makes the same wood #deb887 render from #ffd49b to #ffeeaf. TechBox should pick one preset.
- Which Nano palette is canonical: black headers with silver pins and gold ICSP pins (LSM Part 1, LAC) or the PMG CAD defaults (#e4e4e4 pins)? Same for Dupont pins (#a6a9aa / #cccccc / #e4e4e4) and housings (#1e1616 / #000000).
- Is the dark #855e42 outer face on LSM panel D2 meaningful (an outside-face marker) or a one-off? No other panel in any kit has a second face colour.
- Label font: Arial (LSM, LAC builds) or Public Sans (PMG and LAC Deconstruction, the two newest projects)?
- Title-page fonts cannot be identified from the data because the title text is a raster image; the source artwork is needed.
- Wire palettes are per kit, with a different hex for the same nominal colour in each. A single TechBox ribbon palette has to be chosen; the guides do not provide one, and several PMG dark wires and the white wire are hard to distinguish.
- Should solids left at the CAD default colour #cad1ee (LSM button tabs, a USB plug solid, straight resistor leads, LAC SMD parts) be given real colours in TechBox's own assets? They look like authoring leftovers.

## Electronics and wiring conventions

### WIRE-1 · qualified

**Show a wire connection as a model swap between Step N and Step Nc: fade the pre-connection model out and fade a separately modelled routed model in, with no tween, no Transition and the same camera (103 of 103). In LAC and PMG (82 pairs) the Step N model is a straight unconnected wire and the Nc model is seated at both ends. In LSM the swap is per END: 3 of 7 pairs per guide end half-seated and 3 of 7 start from an already bent, half-seated wire. Loose and routed colour match on 98 of 103 pairs (45 of 48 in the full builds). A straight loose wire may still be tweened rigidly before it is connected: 12 step pairs in the full builds, not 9.**

- Applies to: wiring, construction; LSM, LAC, PMG (all 10 guides that connect wires)
- Evidence: 103 of 103 wire-connection step pairs (48 of 48 in the three full builds) are APPEAR + DISAPPEAR with 0 wire moves and 0 Transitions between N and Nc; both halves pause, 800 ms. Computed with a leaf-level state walker over the raw payloads (connections.json). In the full builds a wire model is swapped in 69 step pairs (48 connections + 20 re-poses + 1 ribbon split) and tweened in only 9, always while still straight and rigid (travelling with a pre-wired component, sliding apart in a ribbon-separation step, or the PMG USB plug).
- Exceptions: None for connections. LAC1 loose and routed models of the same wire differ slightly in colour (green #2ecc40 vs #10cc62; grey #aaaaaa vs #cccccc).
- Narrowed because: LSM pad-end steps start from a bent wire already plugged at one end: LSM2 [010] [012] [014], LSM12 [026] [028] [030], LSMF [028] [030] [032]; LSM breadboard-end steps end with the other end still free. Colour drift: LAC1 [021] and LACF [021] green #2ecc40 to #10cc62; LAC1 [027] and LACF [027] grey #aaaaaa to #cccccc; LSMF [023] #a6a9aa to #b1b3b3 (the analyst listed LAC1 only). Wire tweens the analyst missed: LACF [019] 177 mm, LACF [042] 150 mm, PMGF [037] 12 mm, where the first wire of a ribbon glides from the separated ribbon to the parking spot. Full list: LSMF Step 17; LACF Steps 8, 9, 15, 19, 20, 25, 35; PMGF Steps 2, 15, 16, 25.
- As first stated: Show a wire connection as a model swap: Step N shows the wire straight and unconnected, Step Nc fades it out and fades in a separately modelled, already-routed wire of the same colour seated at both ends. Never tween or morph a wire into place.
- Why it helps students: The student sees two unambiguous states, 'this wire, not yet connected' and 'this is what it looks like connected', without a distracting and physically meaningless flight path for a floppy part.
- For our player: The player needs a 'swap' step primitive (cross-fade model A out / model B in over 800 ms) and the asset pipeline must supply two models per wire: a straight loose one and a routed one per installed pose. No path animation or cable physics is required.

### WIRE-2 · confirmed

**Put no red lead lines and no arrows on a wire-connection step; destinations are named with text labels only.**

- Applies to: wiring, construction; LSM, LAC, PMG
- Evidence: 0 lead lines and 0 arrows on 103 of 103 connection pairs (the detection rule did not use line/arrow absence, so this is a finding).
- Exceptions: None. The PMG USB plug (PMGF [057]) is treated as a rigid insertion and does get 1 lead line.
- Why it helps students: Red is kept exclusively for rigid 'push this straight in' motions, so a wire step reads as 'find this hole/pin' rather than 'move along this line'.
- For our player: Authoring validation should reject lead lines/arrows on steps typed as 'wire'; the wire step template only exposes eye, labels and (optionally) pin badges.

### WIRE-3 · confirmed

**A wire step is a plain Step N / Step Nc pair: Nc carries no annotation at all and uses exactly the same camera as N.**

- Applies to: wiring, construction; LSM, LAC, PMG
- Evidence: 0 of 103 completed views carry any annotation; camera unchanged between N and Nc on 103 of 103; 0 Transitions inside a wire pair.
- Exceptions: Naming only: LAC1 [030] is 'Step 14C'; PMG1 [033] is named 'Completed View' but is the Step 14c swap.
- Why it helps students: The completed view is an uncluttered picture to compare against the real kit from the same viewpoint.
- For our player: On entering the completed half the player auto-hides every callout introduced by the hover half and locks the camera.

### WIRE-4 · confirmed

**One wire per numbered step: a free jumper gets one step pair covering both of its ends; a lead already attached to a component gets one step pair for its free end. Never group wires, even to adjacent pins.**

- Applies to: wiring, construction; LAC and PMG (current form); LSM differs
- Evidence: 33 of 36 ribbon jumpers are one-wire-one-step (LAC 12, PMG 21); 8 of 10 captive leads are one-lead-one-step.
- Exceptions: LSM: each of the 3 ribbon jumpers takes two steps, one END per step, all breadboard ends first, then the matrix card, then all pad ends (LSMF 10-12, [027], 13-15); the two push-button leads share one step with two labels (LSMF [041]).
- Why it helps students: Each press of Next is one physical action with one thing to check, which keeps a class in step and makes a mis-plugged wire easy to locate.
- For our player: Step data model: a wire step references exactly one wire id (or one lead id) and one or two endpoints; batch wire steps should not be offered in construction mode.

### WIRE-5 · confirmed

**Callout set for a wire step (current form): exactly one eye icon on the wire to pick up, plus exactly one text label per end to be plugged in: two labels for a free jumper, one for a captive lead. Nothing else.**

- Applies to: wiring, construction; LAC and PMG
- Evidence: Eye on 41 of 41 LAC/PMG pairs in the full builds (82 of 82 counting part guides); 2 labels on 33 of 33 free jumpers, 1 label on 8 of 8 captive leads. Eye anchored to the wire body on 32 of 33 free jumpers and to the lead's pin housing on 8 of 8 captive leads. Eye width 7.81% of viewport (LAC, 18 of 20) or 8.2% (PMG, 21 of 21), leader #7fdbff with dashed ring.
- Exceptions: LSM wire steps have no eye (0 of 7). LACF [083] has the eye on the end housing instead of the wire body. Eye is 7.92% wide on 2 LAC steps.
- Why it helps students: A fixed three-element picture (which wire, where end A goes, where end B goes) is learnt once and then read at a glance on every wiring step.
- For our player: Provide a wire-step template that auto-creates one eye anchored to the loose wire's midpoint (or lead tip housing) and one label slot per endpoint, each anchored to the exact pin/hole feature.

### WIRE-6 · qualified

**Label text is the terse destination name only: breadboard hole lower-case letter + number; rail '(+) red' / '(-) blue'; module pin as silkscreen capitals; I/O-module pin V/S/G + pin number in capitals. Style: bold black, 3em in LAC and PMG, 2.5em in LSM, 5 px #7fdbff underline, dashed ring on the exact pin or hole. Font: Arial is set explicitly only in LSM and LAC; PMG labels carry no font-family and render in the project default PublicSansMedium. Box 175 x 90 px for short 3em labels; rail labels auto-widen to 200-258 px; LSM 2.5em labels are 175 x 75.**

- Applies to: wiring, construction; LSM, LAC (breadboard vocabulary), PMG (I/O-module vocabulary), LAC LCD (module pins)
- Evidence: Full builds: 26 of 26 breadboard-hole labels lower case; 10 rail labels (5 '(+) red', 5 '(-) blue'); module-pin labels capital on 23 of 25; shield-pin labels capital on 19 of 21. Style: Arial bold black 3em in LAC/PMG (74 of 74), 2.5em in LSM (7 of 8); #7fdbff underline 5 px (82 of 82), dashed ring anchor on the exact pin/hole; default box 175 x 90 px (64 of 82).
- Exceptions: Anomalies: PMGF [037] 'clk'/'s8' and [039] 'dio'/'s9' are lower case; PMGF [023] says 'S5' where S6 is meant; LSMF [021] is 3em. The rail colour word can clash with the wire colour (black wire to '(+) red').
- Narrowed because: Font: 0 of 42 PMGF labels (0 of 84 over PMG1, PMG2, PMGF) have font-family Arial; 32 of 32 LACF and 8 of 8 LSMF do. So 'Arial 74 of 74 in LAC/PMG' is wrong for PMG. Box: 175 x 90 on 64 of 82; the 18 others are the 10 LAC rail labels (200-258 x 90), LACF [025] (175 x 91) and 7 LSM labels (175 x 75, LSMF [032] 152 x 76). Case anomalies confirmed: PMGF [037] 'clk'/'s8', [039] 'dio'/'s9' (the card photo silkscreen reads CLK / DIO); 'S5' appears twice and S6 never. Vocabulary counts reproduce: 26 of 26, 5 + 5, 23 of 25, 19 of 21.
- As first stated: Label text is the terse name of the destination only: breadboard hole = lower-case row letter + column number (i23); power rail = '(+) red' / '(-) blue' (the rail's stripe colour); module pin = silkscreen name in capitals (VCC, GND, OUT, SDA, SCL, DIN, CS, CLK); I/O-module pin = row letter V/S/G + controller pin number in capitals (V4, S4, G4). No verbs, part names or wire colours.
- Why it helps students: The label matches exactly what is printed on the board in front of the student, so matching is visual and needs no reading of sentences.
- For our player: Store pin/hole names on the board model (hole grid, rail ids, header pin silkscreen) and generate label text from the endpoint, with a case rule per endpoint class; add a validator for label text vs actual endpoint to prevent S5/S6-type errors.

### WIRE-7 · confirmed

**Show a free jumper as a straight model with both end housings, parked beside the assembly on the camera side, parallel to the board's long axis, at one staging spot that is re-used for every wire of the run; never hold it over its destination. Show a captive lead straight, as supplied, sticking out of its component.**

- Applies to: wiring, construction; LAC and PMG
- Evidence: 33 of 33 free jumpers lie along the board's long world axis. Staging spot spread within a run 2-7 mm in 5 of 6 runs (19 mm over the 12 PMG button wires = ribbon slots at 1.75 mm). Wire centre 66-118 mm horizontally from the board centre (36-89 mm clear of its edge); 3-10 mm above the board top in PMG, 42-68 mm in LAC. On screen the wire midpoint is in the lower half of the frame on 33 of 33 and left of centre on 30 of 33. Loose model: 58 mm body, 8 mm female housing, 12 mm male housing with pin.
- Exceptions: PMGF [037] is parked 40 mm from the spot used for the next three wires. LAC bridges are parked lower right, not lower left. LSM does not park wires (see WIRE-8).
- Why it helps students: The next wire always turns up in the same place on screen, isolated on white so its colour is easy to read, and it does not hide the pins it is about to go to.
- For our player: Each wiring run needs a 'staging anchor' (world position + orientation) authored once; the player places every loose wire of the run there. Reserve the lower-left of the wiring camera frame for it.

### WIRE-8 · confirmed

**LSM variant (earlier form, do not mix with WIRE-5/7 in one guide): connect one wire end per step with the wire held above the board; hang the hole label on the plug being connected; for a module pad, show a matched pair of discs with the same text, filled #7fdbff on the pad and white on the wire's free end, and re-identify the wire with a label naming the hole its other end already occupies.**

- Applies to: wiring, construction; LSM only (LSM2, LSM12, LSMF)
- Evidence: 7 of 7 LSM wire pairs have no eye icon; 3 of 3 pad connections use a badge pair (discs 5.8-7.8% of viewport wide); ribbon floats 27 mm and the LED matrix 40.5 mm above the breadboard top; plug hovers 24-25 mm above and 9-39 mm to the side of its hole. Camera re-aims on 5 of 7 LSM wire steps, by 109-125 degrees between pad steps.
- Exceptions: Far-end label is anchored to the seated plug in LSM2/LSM12 but to the breadboard hole in LSMF. Badge text 'V-In' conflicts with the card ('V- Out V+') and with the description ('IN pin').
- Why it helps students: When three near-identical wires come from one ribbon, pairing 'this end' with 'that pad' by identical badges removes any doubt about which wire and which pad.
- For our player: Support a 'pin badge pair' annotation (two linked discs sharing one text) as an optional alternative for unnamed pads, but default new content to the LAC/PMG recipe.

### WIRE-9 · qualified

**Wire one module completely before starting the next (3 of 3 kits; LSM does it in two passes with the matrix card between). Within a module go along its header or lead row in physical order: 10 of 11 groups with three or more pins; the exception is the LAC RTC. Do not reorder to put supply first (supply-first in 4 of 13 mixed groups). Taking modules in ascending controller-pin order is evidenced only in PMG; LAC's module order follows the mechanical build.**

- Applies to: wiring, construction; LSM, LAC, PMG
- Evidence: Physical pin order in 10 of 10 module groups with a row of 3 or more pins/leads (verified from monotonic leader-tip positions). Supply-before-signal holds in only 4 of 13 mixed groups.
- Exceptions: LAC RTC is wired VCC, GND, SDA, SCL = columns 23, 24, 22, 21 (LACF Steps 9-12), not in pin order. LSM breadboard pass is V+, V-, data. LSM leaves a module half-wired between its two passes.
- Narrowed because: LAC RTC wires land in columns 23, 24, 22, 21 (LACF [019]-[025]); it has four adjacent pins and belongs in the denominator, so 10 of 11, not 10 of 10. LAC module order is RTC (a8/a9), rail feeds (a14, a12), switch bridges (j1, j3), pot (a5), buzzer (j4), LCD (b8/b9): not ascending. PMG is ascending (4, 5, 6, 7, 8/9, 11-13). LSM breadboard pass is V+, V-, data.
- As first stated: Wire one module completely before starting the next; within a module connect in the physical order of its header pins; take modules in ascending controller-pin / left-to-right order. Do not reorder to put supply first.
- Why it helps students: The student works along a row of pins in the same direction every time and can count pins instead of reasoning about function.
- For our player: Authoring tool should propose wire-step order from header pin index; the pinout data for each module must include physical pin order.

### WIRE-10 · confirmed

**Treat wire colour as identity only: give each wire in a run its own colour, keep it identical between loose and routed models, model housings black, and never rely on colour to convey electrical function.**

- Applies to: wiring, construction and deconstruction; LSM, LAC, PMG
- Evidence: 46 wires in the full builds: supply on red/dark red 3 of 12; ground on black/charcoal 3 of 12; among the 36 ribbon jumpers 2 of 10 supply wires are red and 1 of 10 ground wires black. All 21 PMG jumpers are distinct colours; LAC re-uses 3 colours across ribbons. Wires are used in ribbon order in PMG (12 of 12, 9 of 9) and for the LAC LCD ribbon (4 of 4), not for the LAC 6-wire ribbon.
- Exceptions: Manufacturer-fitted polarised leads happen to match convention (pot red to (+), pot and buzzer black to (-)); the rocker switch leads do not.
- Why it helps students: Ribbon jumpers come in arbitrary colours; the student matches the colour on screen to the wire in hand, and the label (not the colour) says where it goes.
- For our player: Wire colour must be a per-wire asset property taken from the physical kit; the player must not auto-colour by net. Avoid white wires on the white background or outline them.

### WIRE-11 · confirmed

**Introduce each jumper ribbon in its own numbered preparation pair before the block that uses it: ribbon alone on white in close-up with an eye icon, then the same wires separated and straight. Size the ribbon to exactly the wires the next block(s) need.**

- Applies to: wiring, construction; LSM, LAC, PMG
- Evidence: 6 ribbon-prep pairs in the full builds, 6 of 6 with everything else hidden, eye on 5 of 6, camera distance 103-175 mm. Wire counts 3, 6, 2, 4, 12, 9 equal the wires used next. Ribbon pitch 1.75 mm; after separation 4.4-4.9 mm (PMG), 7.7-13.1 mm (LAC 4-wire), 21.6 mm (LAC pair).
- Exceptions: PMGF [035] has no eye. LSM swaps a joined model for a split model instead of sliding wires apart; LSM2 [001] has two eyes.
- Why it helps students: Students see how many wires to peel off and what they look like before any of them has to be plugged in.
- For our player: Provide a 'ribbon split' step type that isolates the ribbon and spreads the wires by a set pitch; ribbon assets need per-wire sub-models ordered across the ribbon.

### WIRE-12 · confirmed

**Give every module whose pin names will appear on wiring labels an un-numbered card named after the module, placed before its first use: module alone on white in close-up, plus a framed picture of the real board with the header to be used boxed in red and a leader to the same header on the 3D part.**

- Applies to: wiring, construction; LSM, LAC, PMG (full builds and wiring parts)
- Evidence: 13 electronics cards in the three full builds, all isolating the part; 12 of 13 directly before the first step using it. Pinout picture present for 6 of 6 modules whose pins are named on labels; framed photos 17-37% of viewport wide; red box on 5 of 6.
- Exceptions: Cards without a pinout: RTC and buzzer (eye only), rocker switch and the LAC/PMG USB cards (no annotation). Potentiometer, LSM push button, Nano and jumpers have no card. The LSM diagram replaces the 3D view with a flat picture; Push Buttons card uses an orange ring.
- Why it helps students: The pin names used on the following steps are shown once, large and on a photo of the real part, so students know where to read them on their own module.
- For our player: Module library entries need a pinout image with a marked header region; the player needs a card step type (no numbering, no completed twin, isolation, optional framed image with leader).

### WIRE-13 · confirmed

**Complete all wiring on the open base before any enclosure wall is fitted. Mount first, then wire, anything that plugs into the breadboard or mounts in a loose panel; wire loose, then mount later, any module that mounts to the enclosure. Do not spend a step placing a loose module: fade it in where it will be wired.**

- Applies to: construction, wiring, mechanical ordering; LSM, LAC, PMG
- Evidence: Wiring ends before the first wall in 3 of 3 full builds. Mounted before wiring: 4 of 4 (RTC, rocker switch, potentiometer, LSM button). Wired loose then mounted: 9 of 9 modules, with 0 placement steps (they appear on their card, on the first wire step, or on an auto Transition for PMG buttons 2-4).
- Exceptions: LSM LED matrix changes pose between steps without any step explaining it.
- Why it helps students: Pins stay reachable while wiring, and the student is not asked to balance a module in a half-built box.
- For our player: Step-order linting: flag wire steps scheduled after enclosure steps; allow parts to be 'present, unplaced' in the scene without a placement step.

### WIRE-14 · confirmed

**Use one camera per wiring run: frame both ends, the parked wire and label margins on the first wire of a module block and hold that view for every wire of the block; do not zoom to the pin.**

- Applies to: wiring, construction; LAC and PMG
- Evidence: 41 LAC/PMG wire steps in 9 runs: camera moves on the first step of 9 of 9 runs and on 0 of the other 32. Distance 173-202 mm (PMG), 277-439 mm (LAC); elevation 21-57 degrees.
- Exceptions: LSM re-aims on 5 of 7 wire steps to face each pad.
- Why it helps students: Nothing moves except the one wire and its labels, so the change from step to step is obvious.
- For our player: Camera keyframes belong to the run, not the step; the player should inherit the previous camera by default on wire steps.

### WIRE-15 · confirmed

**Make the USB cable the last electrical connection, give it its own card, and show it in a single step pair.**

- Applies to: wiring, construction; LSM, LAC, PMG
- Evidence: Card before the step in 3 of 3 kits; last connection before the enclosure in 3 of 3 full builds. Depiction: eye on the Nano socket then the routed cable fades in plugged (LSM, LAC: 2 kits); or plug hovers 22.9 mm with one 28.5 mm lead line and tweens in (PMG).
- Exceptions: LSM2/LSM12 fit the D2 panel before the cable. The two depictions are inconsistent between kits.
- Why it helps students: Nothing is live while wires are being moved, and the cable does not get in the way of earlier steps.
- For our player: Support both a fade-in cable step and a rigid plug insertion; pick one as house style (see open questions). Cable asset needs a loose model for the card and a routed plugged model.

### WIRE-16 · confirmed

**Plug a rigid component into the breadboard or I/O module with hover + lead lines + hole labels: hover it 29-44 mm straight above its seat, draw one thin red line from each end pin/lead tip to its hole, label those holes in lower case (maximum two), and tween straight down in the completed view. Bend leads in a separate isolated step first.**

- Applies to: construction, electronics; LSM and LAC (breadboard), PMG (Nano into I/O module)
- Evidence: 9 plug-ins in the full builds: 2 lead lines on 7, 4 on 2; two hole labels on 7 of 9; hover 29-44 mm, median 34 mm. Breadboards exist in LSM and LAC only; PMG has none. No servo or multi-pin sensor plugs in any kit.
- Exceptions: LSMF Nano and PMG Nano have 4 lines and no hole labels (LSM1's version labels 'Pin d12' and 'c16').
- Why it helps students: Naming just the two end holes fixes the position of a many-pin part without cluttering the view with a label per pin.
- For our player: The breadboard model must expose every hole as a named, addressable anchor (row letter + column, rails by polarity) for both lead-line ends and label rings.

### WIRE-17 · confirmed

**Model connector ends and their gender correctly: male pin ends go into breadboard holes, female housings go onto module or I/O-module header pins; every housing is black.**

- Applies to: wiring assets; LSM, LAC, PMG
- Evidence: 33 of 33 breadboard ends are male (LSM 5, LAC 28); 7 of 7 module-header ends in LSM/LAC are female; all 42 ends of the 21 PMG jumpers are female.
- Why it helps students: The picture matches which end of a male-female jumper to use where.
- For our player: Wire assets carry end types (M/F); authoring can validate end type against the target (hole vs header pin).

### WIRE-18 · confirmed

**Reposition an already-wired module only by cross-fading to a pre-posed copy that carries its own re-routed wires; never tween a wired part.**

- Applies to: construction, mechanical steps involving wired modules; LSM, LAC, PMG
- Evidence: 20 re-pose step pairs in the full builds (LSMF 4, LACF 8, PMGF 8), 0 wire moves; each wired module exists as 2-5 pose copies.
- Exceptions: Pre-wired components do tween once, rigidly with straight leads, when first mounted in a loose panel (LACF Steps 15, 25; LSMF Step 17).
- Why it helps students: Wires always look plausible in every pose instead of stretching or passing through parts.
- For our player: Asset pipeline must allow several pose variants per wired sub-assembly, and the swap primitive from WIRE-1 must handle groups (module + wires + housings).

### WIRE-19 · qualified

**Deconstruction has no shared wiring rule beyond 'no hole labels'. LACD: one wire per step, eye on the plug, cross-fade to the loose model (via an auto Transition for jumpers), pin-name labels only on the 4 adjacent LCD wires. LSMD: eye on every wire-removal step, an arrow added on 2 of 5, and the three pad-end wires are tweened 30.5 mm as rigid loose models before they fade. PMGD: arrows only, no eye, bundles of 5 and 16 wires that simply fade out.**

- Applies to: deconstruction, wiring; LACD, LSMD, PMGD
- Evidence: LACD: 20 wires in 20 steps, eye on 20 of 20, pin-name labels on 4, 0 arrows; 12 jumpers cross-fade to the straight model at the build's parking spot, 8 captive leads return to the hanging pose. LSMD: 3 breadboard ends one per step, then 3 pad plugs together, then 2 button plugs together. PMGD: bundles of 5 and 16 wires with 1-2 arrows, no eye.
- Exceptions: No shared granularity rule (1, 1-3, 5-16 wires per step); PMGD uses arrows where the others use eyes.
- Narrowed because: LSMD Step 15 [040]-[042]: eye + arrow, then 3 wires and 3 housings tween 30.5 mm on a Transition, then fade; LSMD Step 17 [046] has 2 eyes + arrow + picture. PMGD [049] [057]: arrows, no eye, plain disappear of 15 and 48 parts. LACD USB removal [067]-[069] is arrow + eye + 43 mm tween. LSMD [037] moves the three loose wires 2.7 m with a rotation across a camera cut.
- As first stated: Deconstruction: mark the plug to pull with an eye icon, use no hole labels, and remove wires by cross-fade; add pin-name labels only to tell adjacent identical wires apart. Granularity is not consistent across kits.
- Why it helps students: Unplugging needs no destination, so only the thing to grab is marked.
- For our player: Reuse the swap primitive in reverse; let the deconstruction author choose per-wire or bundle steps until a house rule is set.

### Added by the re-check

- Wire steps carry no text: leave the step description empty and use no popup on Step N or Step Nc. *Evidence:* Description empty and popup absent on 89 of 103 pairs: every LAC and PMG guide (82 of 82) and LSMF (7 of 7). Only LSM2 and LSM12 have descriptions, and they are stale (numbered +5, 'Ste[ 15').
- When a wire step directly follows ribbon preparation, keep the first wire on screen and tween it, straight and rigid, from its separated-ribbon position to the parking spot; when a module card sits in between, fade the wire in at the spot. *Evidence:* LACF [019] 177 mm, LACF [042] 150 mm, PMGF [037] 12 mm (same in LAC1 [019], LAC2 [012], PMG2 [004]). No tween after a card: PMGF [007] after [006], LACF [079] after [078]. This also explains why PMGF [037] is 40 mm from the other display wires.
- PMG wire labels use the project default font (PublicSansMedium), not Arial; only LSM and LAC set Arial explicitly. *Evidence:* 0 of 84 PMG wire labels contain font-family; 40 of 40 in LACF + LSMF do. Renders PMGF [007] and LACF [019] show different typefaces. The analyst reported Arial for 74 of 74.
- Do not conserve wire length between the loose and routed models: the loose model is a fixed-size token, the routed model is as long as the route needs. *Evidence:* Loose jumper body 58 mm against routed spans 23-113 mm; switch leads 30 mm to 94-136 mm; pot leads 50 mm to 229-240 mm; buzzer leads 39 mm to 65-69 mm (LACF [034]-[039], [065]-[075]).
- A re-pose step of an already-wired module keeps the normal mounting callouts on Step N (red lead lines or an arrow, or an eye) but completes by cross-fade, so a lead-line step can end in a swap rather than a tween. *Evidence:* Of the 20 re-pose pairs, 10 carry lead lines or an arrow (LACF Steps 47, 49, 52, 54; PMGF 46, 48, 50; LSMF 21, 23, 30) and 10 carry only an eye; none moves a part.
- Wire steps show the whole assembly built so far; isolation is reserved for module cards and ribbon preparation. *Evidence:* The first wire step of each run re-shows everything the card hid: LACF [034] +27 parts, [065] +40, [072] +50, [079] +58; PMGF [037] +42, [046] +57. Cards and ribbon steps show 1-7 components and 0 non-wire parts respectively.
- Anomalies to fix at source rather than copy: the eye icon overlaps the I/O module; two lead housings render pale in the first and last views; loose wires jump across a cut in deconstruction; duplicate or out-of-order step names. *Evidence:* PMGF [037] (render); LSMF [000] and [087] housings #cad1ee / #cad1ed; LSMD [037] three loose wires move 2.7 m with a rotation; LACD 'Step 41' [104] precedes 'Step 40' [105] and 'Step 45c' names both [120] and [122].

### Numbers (as corrected by the re-check)

| Setting | Value | Basis |
|---|---|---|
| Wire step timing | 800 ms, pause on both Step N and Step Nc, no Transition inside the pair (confirmed) | 103 of 103 pairs recomputed |
| Lead lines / arrows on a wire step | 0 / 0 (confirmed) | 103 of 103; no line or arrow object visible on N or Nc |
| Annotations on a wire Step Nc | 0 (confirmed) | 103 of 103 |
| Labels per wire step | 2 for a free jumper, 1 for a captive lead (confirmed) | 33 of 33 and 8 of 8 in LACF + PMGF; 82 of 82 with part guides |
| Eye icons per wire step and anchor | 1; on the wire body for a free jumper, at the mid-point (0.44-0.54 of body length) on 27 of 33; on the lead's pin housing for a captive lead | 41 of 41; body 32 of 33; mid-point 27 of 33 (off-centre LACF [085], PMGF [039] [041] [043]; housing LACF [083]); captive 8 of 8 |
| Eye icon width | 7.81% of viewport width (LSM, LAC); 8.2% (PMG) (confirmed) | LACF wire steps 18 of 20 (7.92 on 2); PMGF 21 of 21; all guides: 7.81 x143, 8.2 x62, 7.92 x10, other x8 |
| Wire label text style | bold black 3em (LAC, PMG), 2.5em (LSM); font Arial only in LSM and LAC; PMG has no font-family and inherits the project default PublicSansMedium | size/bold/colour 74 of 74 LAC+PMG and 7 of 8 LSM; font-family Arial on 32 of 32 LACF and 8 of 8 LSMF, 0 of 42 PMGF |
| Label underline, leader and anchor | #7fdbff underline 5 px; #7fdbff leader 5 px; dashed life-saver ring 30 px x 1.2 on the exact pin or hole (confirmed) | underline 82 of 82 (172 of 172 over all wiring guides); ring 1.2 on 80 of 82; leader explicit on 74 of 82, inherited from the base component on 8 |
| Label box | 175 x 90 px for short 3em labels; rail labels auto-widen to 200-258 x 90; LSM 2.5em labels 175 x 75 | 64 of 82 are 175 x 90; exceptions are the 10 LAC rail labels, LACF [025] (175 x 91) and 7 LSM labels |
| LSM pin badge pair | two discs with identical text, 5.8-7.8% of viewport wide; filled #7fdbff on the pad, white on the wire end (confirmed) | 3 of 3 pad steps in each of LSM2, LSM12, LSMF; widths 5.82-7.81 |
| Loose jumper model | 58.2 mm body, 1.2 mm thick; female housing 8.0 mm; male housing with pin 12.0 mm; overall M-M 74.2, M-F 69.4, F-F 65.4 mm | world bounding boxes; exceptions: LAC bridge jumpers 56.0/55.5 mm body and 70.5/71.2 mm overall; PMG display ribbon 58.8 mm body |
| Captive lead length (straight) | 30 mm (switch), 39 mm (buzzer), 50 mm (potentiometer, LSM button) (confirmed) | bodies 30.1-30.3, 38.9-39.0, 49.8-50.1, 49.6 mm |
| Ribbon pitch | 1.75 mm joined; after separation gaps 4.1-4.6 mm (9 wires), 4.5-5.4 mm (12 wires), 6.1-9.0 mm (LAC 6 wires), 7.7-13.1 mm (4 wires), 21.7 mm (pair) | PMGF [004]/[005], [035]/[036]; LACF [017]/[018], [040]/[041], [076]/[077]; the analyst's 4.4-4.9 are means (4.39, 4.85) |
| Parking spot of a loose jumper | 66-119 mm horizontally from the board centre (36-89 mm clear of its edge), parallel to the board's long axis, camera side; same spot for the run apart from the ribbon-slot offset | 33 of 33 free jumpers; spread 2-7 mm in 5 of 6 runs, 19.2 mm over the 12 button wires; PMGF [037] 40 mm off |
| Parked wire on screen | leader tip y 54-82% of viewport (lower half), left of centre | 33 of 33 lower half (53.6-81.7; the 83% figure is a buzzer lead); left of centre 30 of 33 (not LACF [042] [044], PMGF [037]) |
| Parked wire height | 3-10 mm above the board top (PMG); 42-68 mm above the breadboard top (LAC) (confirmed) | PMG 2.7-2.9 and 9.8-10.0 mm; LAC 42, 58.5, 68 mm |
| LSM hover heights | ribbon 27 mm and LED matrix 40.5 mm above the breadboard top; plug 24-25 mm above its seated height (confirmed) | LSMF: 26.8 mm; 912.4 - 871.9 = 40.5 mm; 24.0, 24.8, 24.4 mm |
| Plug-in component hover | 29-44 mm straight above the seat, median 34 mm; 2 lead lines, 4 on the LSM and PMG Nano (confirmed) | 9 plug-ins: 29.1, 29.8, 30.3, 32.4, 33.6, 37.1, 39.8, 40.0, 44.1 mm |
| USB plug hover (PMG) | 22.9 mm on the socket axis, 1 lead line 28.5 mm (confirmed) | PMGF [057]/[058] |
| Wiring camera | distance 173-202 mm (I/O-module kit), 277-439 mm (breadboard with panels); elevation 21-57 degrees; 0 moves inside a run (confirmed) | 9 constant-camera runs over 41 steps, including every Nc and auto Transition inside a run |
| Ribbon-prep camera | 103-175 mm, ribbon isolated (confirmed) | 6 of 6: 103, 110, 119, 128, 175, 175 mm; LACF [076] viewed from below |
| Pinout photo on a module card | 17-37% of viewport width, #7fdbff rectangle frame 5 px, red box round the header (confirmed) | 4 framed photos: 17.15, 29.02, 33.56, 36.72; red box seen on the LSM diagram, LCD, button and 4-digit display renders (dot matrix not opened); the I/O-module picture is a label object with no red box |
| Annotation count on a wire Step N | 3 (eye + 2 labels) or 2 (eye + 1 label) (confirmed) | 41 of 41 LAC/PMG; LSM is 1, 2 or 3 with no eye |
| Wire tweens in the full builds | 12 step pairs (analyst: 9) | LSMF 17; LACF 8, 9, 15, 19, 20, 25, 35; PMGF 2, 15, 16, 25; swaps remain 69 |

### Open questions

- Which wiring recipe should the player standardise on: the LAC/PMG whole-wire form (eye + destination labels + parked wire, 41 of 48 pairs, both later kits) or the LSM one-end-per-step form with badge pairs? Should the badge pair survive as an option for unnamed pads?
- Is the loose-wire parking spot meant to be a fixed screen position (lower left) or a fixed world offset per run? Data stores a world position; it lands lower left in 30 of 33 cases.
- Should the parked wire rest on a table plane? In LAC it floats 42-68 mm above the board and renders about 1.6 times oversize.
- USB cable: fade-in with an eye on the socket (LSM, LAC) or hover + lead line + tween (PMG, the newest kit)?
- Should rail labels keep the stripe colour word ('(+) red') when the wire going there is a different colour, e.g. a black wire to '(+) red'?
- Should I/O-module and module pin labels be upper case throughout (fixing 'clk', 'dio', 's8', 's9'), and should 'S5' for S6 (PMGF [023]) and the swapped j5/j16 labels (LSMF [041]) be corrected at source?
- Is the intended teaching order 'module pin order' (10 of 10 pin rows) or 'supply first'? The RTC is the only module wired supply-first against its pin order.
- Should every wired component get a card with a pinout (the potentiometer, RTC, rocker switch and LSM push button currently have none), and should the ribbon-prep step come before or after the module card (both orders occur)?
- For deconstruction, is one wire per step (LAC) or bundles with arrows (PMG) the intended granularity?
- Label size: is 3em the standard and LSM's 2.5em a legacy value?

## Mechanical (wood, fasteners, enclosure) assembly conventions

### MECH-1 · qualified

**For a single-motion rigid part (15 of the 28 new wood kinds in the masters: D4, D5, D6, D7, D8, D9; F5, F6, F8; H2, H3, H4, H8, H9, H13): fade it in on Step N already displaced back along its joint axis, in final orientation, and seat it with one straight 800 ms tween on Step Nc. The other 13 kinds are the two-motion parts of MECH-4: 7 arrive tilted 8-24 degrees and 6 take two or three tweens inside their own step. Always true in the build guides: the camera never moves after Step N within a numbered step, and the incoming part is never recoloured or restyled. Hover is hand-picked: median 68 mm (q1 54, q3 94, range 22-139); about 0.7 x the longest dimension.**

- Applies to: construction / mechanical; all wood panels, posts, brackets, keys, stems in LSM, LAC, PMG
- Evidence: Corrected state walk over raw payloads. 0 of 173 mechanical steps (16 build guides) move the camera on a Transition or Step Nc. 0 colour/style changes on any wood panel in a visible step of the 3 masters. Hover of 28 unique new wood parts (masters): min 22, q1 55, median 69, q3 94, max 139 mm; edge-first parts (tabs on the mover, travel in its own plane) n=16 median 82; face-on panels (slots on the mover, travel along its normal) n=9 median 64; oblique hinge arrivals 3. Hover / longest dimension median 0.7 (0.2-1.4). Direction vs declared up-axis for 36 part-moves: down 15, sideways 14, diagonal 4, up 3.
- Exceptions: Hover distance is hand-picked, not a constant; identical D11 posts use 82/82/83/77 mm. A part already visible on the title page slides out to hover instead of fading in (first step of LSM P3, LSM P4, LAC P4, PMG P3). Repeat instances fade in already seated. Wire-tethered parts never tween (MECH-6).
- Narrowed because: Holds: 0 of 173 mechanical steps (0 of all 331 numbered build steps) move the camera on a Transition or Nc; 0 appearance writes on wood except the one ghost step; all 44 wood translation stages 800 ms; slide-out exception exactly in LSM P3 [001], LSM P4 [001], LAC P4 [001], PMG P3 [001]. Against the wording: tilted arrivals H10 7.9, H14 10.3, H7 11.7, H6 18.1, F2 21.4, D3 21.6, H5 23.6 degrees; multi-tween steps D10 [064]-[066], F9 [098]-[101], F2 [125]-[127], H11 [091]-[093], H12 [094]-[096], H14 [113]-[115]. Numbers: median 67.7 not 69, q1 53.9 not 55; edge-first range starts at 40.0 (H2), not 43; PMG kit median is 80.1, not 87; the direction split '36 moves: 15 / 14 / 4 / 3' is not reproducible (first stage of 28 kinds: sideways 12, down 10, diagonal 5, up 1). The LED stem first appears on the 'LED Stems' card [082], not on a Step N. Outside scope: PMG Decon Steps 2 and 3 move the camera on an in-step Transition ([007], [012]).
- As first stated: Fade a new rigid part in on Step N already displaced back along its real joint axis, in final orientation, and seat it with one straight 800 ms tween on Step Nc. Do not move the camera after Step N and do not recolour or highlight the incoming part.
- Why it helps students: The gap between the part and its seat shows which way to push before anything moves, and the unchanged camera lets the student compare before and after.
- For our player: Each part needs an authored insertion axis and hover offset (vector, mm). Player: Step N = fade in at hover pose; Step Nc = linear tween to seat, 800 ms; camera locked across the pair. Auto default if none authored: about 0.7 x longest dimension, clamped 40-140 mm, along the joint axis.

### MECH-2 · qualified

**On the hover frame draw thin red (#ff0000, constant screen width) lead lines parallel to the travel and about as long as it (median 0.98-0.99 x), from tab to slot, for a representative subset of the joints: 1 for a single hook or tab, 2 for a two-tab part, 4 as 2 on each of two chosen neighbours (or one per post for a four-post plate). Not every tab gets a line. 4 is the usual maximum (147 of 149 line-bearing steps); two older LSM copies show 6. Lines are normally hidden as soon as the part moves; PMG shows fresh second-stage lines on the in-step Transition frame of three steps. Bind line ends to the parts, not to stored coordinates.**

- Applies to: construction / mechanical; all three kits
- Evidence: Lead lines on Step N over all 425 numbered steps in 19 guides: 0 lines 276, 1 line 37, 2 lines 69, 4 lines 41, 6 lines 2; never 3 or 5. Wood-tween steps in masters (38): 0 x2, 1 x6, 2 x19, 4 x11. Of 13 four-line panel steps in masters, 8 are 2+2 on two neighbours, 3 are four posts, H13 is 1+1+2, D6 has one unresolved anchor. Line length / stage travel (wood travelling 10 mm or more): masters n=81, q1 0.93, median 0.98, q3 1.01, 63 within 0.85-1.10. 363 line showings in all guides: all #ff0000, scale 5; 353 are 2-point, 10 are polylines.
- Exceptions: Two older LSM copies (Part 3 [010], Part 3+4 Step 6) show 6 lines for D5 where the Full Build shows 4. Not every tab gets a line: LAC F6 has 8 slots and 4 lines; PMG H8 has 2 lines for its bottom tabs only. Lines are shorter than travel when the part passes through (D11 posts 37-44 for 77-83 mm) and are marker-only on swings (7-29 mm). Two-leg paths use an L-shaped polyline (D10, F9). Anchor order is tab-first usually (30 of 42 face-on, 37 of 39 edge-first) but not always. 36 lines are stored dashed yet render solid.
- Narrowed because: Exact matches: 0:276, 1:37, 2:69, 4:41, 6:2, never 3 or 5; masters wood-tween 0:2, 1:6, 2:19, 4:11; 363 showings all #ff0000 scale 5, 353 two-point + 10 polylines, 36 stored dashed and rendering solid ([078]); 13 four-line panel steps; 77 of 79 lines within 5 degrees of the travel. Against the wording: (a) 'one per tab-and-slot pair' - LAC F6 [128] has slots on all four edges and gets 4 lines, F5 gets lines to 2 of its 3 present neighbours, PMG H8 gets 2; (b) 'never more than 4' - 6 lines on LSM P3 Step 5 [010] and LSM P3+4 Step 6 [012]; (c) 'hover frame only' - PMG Full Transition frames [106], [111], [114] each show 2 new lines and Step 51c [115] keeps 2 (same in PMG P3 [048], [053], [056], [057]); (d) LAC Step 49 is 2 + 1 + 1, not 2 + 2; (e) LSM Full Step 26 stores two 133 mm lines that show about 40 mm. Length ratio recomputed n=83, q1 0.93, median 0.99, q3 1.02, 60 inside 0.85-1.10 (claimed 81 / 0.98 / 63).
- As first stated: Draw one thin red lead line per tab-and-slot pair being engaged, from tab tip to slot mouth, parallel to the travel and about as long as the travel. Use 1, 2 or 4 lines per frame and never more than 4: 1 for a single hook or tab, 2 for a two-tab part, 4 as 2 per neighbour when a panel closes onto two neighbours. Show them on the hover frame only.
- Why it helps students: The lines pair each tab with its slot, so the student can see which features must line up and which way round the panel goes without any text.
- For our player: Lead lines are 3D segments anchored to a feature on the moving part and a feature on the fixed part, so they must follow both. Authoring needs tab/slot feature pairs per joint and a picker that caps at 4 (2 per neighbour, corner-most). Support multi-point polylines. Hide all lines the moment the tween starts. Treat lines as undirected.

### MECH-3 · qualified

**Introduce one kind of wooden part per numbered step (36 of 37 introducing steps in the masters). Two identical parts may share a step when they share one motion and one view (4 steps); four identical posts are split 2 + 2 with an 82 degree camera turn; for a larger set animate one and fade the rest in seated on the next step (2 cases: 3 keys, 63 stems). The base panel is the datum: it fades in seated and is never displaced in any frame. When a loose component meets a loose panel on the bench, the panel fades in seated and the component moves (5 of 5).**

- Applies to: construction / mechanical; all three kits
- Evidence: 37 master steps that introduce wood or stems: 31 one part (84 %), 4 identical pairs, 2 rest-of-set, 0 with two different kinds. Datum fades in seated in 3 of 3 kits. New stationary panel + moving existing component: 5 of 5.
- Exceptions: PMG Step 26 [059] shows datum H1 (seated) and H2 (hovering) together, the only frame with two different panels appearing. Quantity cue for the rest of a set is inconsistent: a '3x' inset for keys, a '64x' card for stems, only an eye icon for the three remaining button modules.
- Narrowed because: PMG Step 26 [059] introduces H1 (seated) and H2 (hovering, 40 mm) in one step, so 'two different kinds: 0 of 37' is 1 of 37 (30 single-kind + 1 two-kind + 4 pairs + 2 rest); the analyst's own exception line contradicts the stat line. The rest-of-set rule rests on two cases. The stem is a white (#ffffff) 3.17 x 3.17 x 66.7 mm square rod with no engraved ID, not plywood, and first appears on a card. Datum confirmed 3 of 3 and never displaced in 19 step-bearing guides. Quantity cue inconsistency confirmed ('3x' inset [085], '64x' / '64X' card label, eye only for buttons).
- As first stated: Introduce one kind of wooden part per numbered step. Allow two identical parts in one step only when they share one motion and one view; split four identical parts 2 + 2 with a camera turn; for larger sets animate one in full and let the rest fade in seated on the next step. The base panel is the datum: it fades in seated and never hovers. When a loose component meets a loose panel, the panel fades in seated and the hand-held component moves.
- Why it helps students: One thing to find and fit per press of Next keeps the step unambiguous, and moving the piece the student is actually holding matches what their hands do.
- For our player: Step schema: one moving part kind, optional instance count of 2. Needs a 'repeat' step type (exemplar highlighted by eye icon or Nx inset, remaining instances fade in seated). The authoring tool should flag a step that moves two different kinds, and should let the author mark which of two mating parts is hand-held.

### MECH-4 · qualified

**Show a joint that needs two motions (13 of 34 wood kinds) as two stages. Either give stage 2 its own numbered step (8 parts) with fresh short lead lines (7 of 9 such steps), or play stage 1 on an auto-advancing Transition between Step N and Step Nc with the camera held (6 parts, 7 frames). In the Transition form stage 2 usually has no cue of its own: only H14 gets new lines; D10 and F9 use one L-shaped polyline for the whole path; F2, H11 and H12 show nothing. A re-aimed camera goes with the two-step form in 5 of 8 cases, so the view does not fully decide which form is used.**

- Applies to: construction / mechanical; LSM D3, D10, D11; LAC F7, F9, F2; PMG H5, H6, H7, H10, H11, H12, H14
- Evidence: 13 of 34 wood kinds (38 %) need more than one motion. Split as two numbered steps for 8 parts (camera re-aimed for stage 2 in 5 of 8: PMG 62-85 degrees on all four, D11 117 degrees) and as a mid-step Transition for 6 parts (7 Transition frames, camera held in all). Arrival tilt 7.9-25.8 degrees. Lock slide 6.7/7.6 mm, push-home 7.0 mm, clamp splay 15-16 degrees. 7 of 9 second-stage numbered steps carry fresh lead lines.
- Exceptions: The choice is not fully explained by the camera: LSM D3 and LAC F9 use a second numbered step with the camera held. The H11/H12 lock slide has no line or arrow. D10's two legs share one L-shaped line. LAC F9 uses both mechanisms.
- Narrowed because: Confirmed: the 13 parts as listed; two-step D3, D11, F7, F9, H5, H6, H7, H10; Transition D10 [065], F9 [099]-[100], F2 [126], H11 [092], H12 [095], H14 [114]; stage-2 camera turn 62, 67, 68, 85 degrees (PMG) and 117 (D11), held for D3, F7, F9; lock slide 6.7 / 7.6 mm, push-home 7.0 mm, splay 15.1 / 16.0 degrees. Against 'each with its own lead lines': 5 of the 6 Transition-type parts have no separate stage-2 lines. Against the camera criterion: D3 (Step 25), F7 (Steps 42, 44) and F9 (Step 46) take a new numbered step with the camera held. 'Arrival tilt 7.9-25.8': the 25.8 is F9, which arrives upright and tilts on [100]; H14 arrives at 10.3 (12.6 is its seating rotation); tilt on arrival is 7.9-23.6 over 7 parts.
- As first stated: Show a joint that needs two motions (hook and swing, drop and slide, insert then push home) as two stages, each with its own lead lines. Use an auto-advancing Transition between Step N and Step Nc when both stages read from one view; use a second numbered step with a re-aimed camera when stage 2 needs a different view.
- Why it helps students: A tilted arrival followed by a separate swing shows the real hand sequence; a single long animation would hide which edge goes in first.
- For our player: A step must be able to hold more than one motion segment (translate, then rotate about an authored pivot at the tab edge), played back to back on one press of Next, with the nav overlay hidden during the intermediate segment. Lead-line sets are per segment. Rotation needs a custom pivot, not the part origin.

### MECH-5 · qualified

**Give every fastener its own numbered step, coming off and going on, with everything unrelated hidden (3-11 parts on screen). Removal: the bare component alone, one fat red arrow on the axis, an auto Transition slides the fastener off, Step Nc hides it. Then the panel fades in and the component is pushed through its hole with one lead line, from 79-103 mm away, entering from the side opposite its retaining hardware: leads-first for the push button and rocker switch, shaft-first for the potentiometer. Fitting: the fastener fades in on the axis with exactly one thin axial lead line and tweens home, in reverse order of removal. No size, name or tool is shown.**

- Applies to: construction and deconstruction / mechanical; LSM push-button nut, LAC potentiometer washer, nut and knob, LAC rocker switch (no screws exist in any kit)
- Evidence: 27 fastener steps in 7 guides: 13 removals (13/13 one arrow, 0 lead lines, all with a Transition), 12 fits (12/12 exactly one lead line, 0 arrows, no Transition), 2 knob-setting steps (eye icon only). One fastener per step 27/27. Text labels 0/27. Fit hover 56-61 mm (LAC), 80-83 mm (LSM); removal travel 38 mm (LAC), 99-101 mm (LSM). 7 panel-mount insertions, 79-103 mm, 1 line each. Axial line / hover median 1.16 (0.86-1.26). Parts on screen 3-11 against 20-51 when the build returns.
- Exceptions: Spin is not kit-wide: 8 of 13 removals and 3 of 12 fits rotate; the LSM nut spins about half a turn and its frame runs 1600 ms (5 of the 7 non-800 ms frames in the corpus), LAC's nut and washer spin on removal at 800 ms and nothing spins on refit. LSM Full re-authored the nut refit at 800 ms. The three LAC removal arrows are three different sizes.
- Narrowed because: All counts reproduce: 13 removals (13 one arrow, 0 lines, all with a Transition), 12 fits (12 one line, 0 arrows, 0 Transitions), 2 knob-setting steps; 27 of 27 one fastener; 0 labels; hover 55.9-61.3 / 80.4-83.1; removal 37.6-37.9 / 98.9-100.7; 7 insertions 79.1-103.2; ratio median 1.16 (0.86-1.26, n=19); spin 8 of 13 and 3 of 12. Against the wording: (a) the potentiometer goes in shaft-first from behind F1 at LAC Full Step 25 [055] and LAC P2 Step 11, so 'leads-first' is 5 of 7; (b) 'on the loose panel' fails for all 9 build-guide removal steps (LSM 16, LAC 22-24 and copies), which show no wood; (c) Appendix C 'LAC Step 29 Nc 57 mm' is an origin artefact, the knob only turns 49.8 degrees; (d) 1600 ms applies to 5 of the 11 spinning-fastener frames.
- As first stated: Give every fastener its own numbered step, both coming off and going on, and do the work on the loose panel with everything else hidden. Removal: one fat red arrow on the axis, an auto Transition slides the fastener off, Step Nc hides it. Fitting: the fastener fades in on the axis with exactly one thin axial lead line and tweens home. Push a panel-mount component through its hole leads-first from at least its own length away, with one lead line. Show no size, name or tool.
- Why it helps students: Small hardware is easy to drop or put on in the wrong order; one item per step in a bare view makes the order and the axis obvious.
- For our player: Fastener step types 'remove' (arrow, auto slide-off, hide) and 'fit' (hover on axis, one line, tween). Per-part axis and optional spin flag with doubled duration. An isolation mode that hides everything but a chosen set and restores it on a later step. No label field is needed for hardware; if TechBox wants sizes shown that is new design.

### MECH-6 · qualified

**Build panel-mount sub-assemblies on their loose panel first and join them to the box later (D2 + button 4 steps later, F4 + switch 34, F1 + pot 29). Never tween a part that is tethered, meaning its wires are already plugged in at the far end: cross-fade between pre-posed copies that carry their own re-routed wires. About half the cases (7 of 13) use two numbered steps, 'pick up' (eye icon, part re-posed at hover) then 'attach' (lead lines or an arrow, part seated); the rest do it in one. A component whose leads are still free is tweened together with its leads.**

- Applies to: construction / mechanical with wiring present; LSM D2+button and LED matrix; LAC F1+pot, F4+switch, LCD, buzzer; PMG button modules, Nano shield, display, dot matrix
- Evidence: 20 pose-swap steps in the masters, 45 in all build guides, 0 with a tween of the tethered part. 7 pick-up/attach pairs, 6 single-step cases. Cues over the 20: eye only 10, lead lines 6 (2 or 4), red arrow 4 (2 with an eye). Sub-assembly built 4, 34 and 29 steps before it is joined (LSM D2, LAC F4, LAC F1).
- Exceptions: Button modules go from eye icon to installed in one step. D2+button is joined with an arrow and no lead lines. Pot and switch are tweened again once isolated in the take-apart guide.
- Narrowed because: Counts reproduce: 20 pose-swap steps in the masters (LSM 21, 23, 28, 30; LAC 43, 47-49, 51-54; PMG 33, 34, 45-50), 45 in the build guides, 0 with a tween of the swapped part; 7 pairs + 6 singles; cues 10 eye-only, 6 lines (2 or 4), 4 arrows (2 with an eye). Against 'anything that has wires attached': the button with its 2 leads tweens 102 mm (LSM Step 17), the switch with 3 leads 81 mm (LAC Step 15), the pot with 3 leads 79 mm (LAC Step 25), and the USB plug with its cable 23 mm (PMG Step 25). No part with plugged-in wires tweens in any of the 16 build guides.
- As first stated: Build sub-assemblies on their loose panel first and join them to the box later. Never tween anything that has wires attached: cross-fade between pre-posed copies that carry their own re-routed wires, normally as two numbered steps, 'pick up' (eye icon, part re-posed at hover) then 'attach' (lead lines or an arrow, part seated).
- Why it helps students: Wires cannot be animated believably; showing a start pose and an end pose with the wires already draped tells the student where the cable should end up.
- For our player: The pipeline must support several posed instances of one sub-assembly, each with its own wire geometry, and a cross-fade swap action. This is the largest authoring cost in the corpus (LED matrix 5 poses, LAC F1 4 copies). Lead lines must be drawable to a part that will swap rather than move.

### MECH-7 · confirmed

**To work on another face, turn the kit over by re-declaring the scene up-axis and swinging the camera in the same step, so the work is still seen from above. Never rotate the model parts, never look up at the underside, and add no 'flip it' graphic. Group underside work so the kit is turned as few times as possible.**

- Applies to: construction and deconstruction / mechanical; LSM, LAC, PMG
- Evidence: 39 up-axis changes in 12 of 20 guides, each with a 43-167 degree camera move: 28 on a Step N, 8 on an auto Transition (all LSM), 2 on a card, 1 on a Completed View. 0 frames rotate the assembly. Masters: 6 mechanical episodes covering 22 of 75 mechanical steps; entered on Step N in 5 of 6. Camera elevation against the declared up-axis is 10-60 degrees on 73 of 75 master mechanical steps (median 34).
- Exceptions: LSM uses auto Transitions to enter once and to leave three times; LAC and PMG always cut on the step. LSM turns the kit three separate times, PMG once (8 numbered steps in one block). The two views outside 10-60 degrees are a plan view (LSM Step 23) and a straight-on knob close-up (LAC Step 29). No cue tells the student to turn the kit.
- Why it helps students: The picture matches what is on the desk after the student turns the kit over, and gravity-assisted insertions still read as coming down from above.
- For our player: The camera needs a per-step up vector, tweened together with position and target. Orbit controls must respect it. Do not implement flips as model rotations. Consider whether the in-house player should add an explicit turn-over cue, since the source has none.

### MECH-8 · confirmed

**Identify wooden parts by the ID engraved on the model and by a tooltip of the form '<Role> - Part <ID>'. Never put a part ID, part name or hardware size in an on-screen label; mechanical steps carry no text at all.**

- Applies to: all step kinds; all three kits
- Evidence: 221 label showings in 20 guides (holes 104, module pins 54, shield pins 30, rails 24, quantities 5, other 4): 0 contain an engraved ID, part name or fastener size. 0 text labels on 173 mechanical steps in 16 build guides. 34 of 34 wood kinds carry an engraved ID and a tooltip description.
- Exceptions: Engraved order equals build order only in PMG (H1-H14). IDs read upside-down in turned-over views; the camera is not chosen to keep them legible. PMG tooltips are inconsistent inside one part (H8 tagged 'Part H2' on some solids; H4 and H10 have three names each). Tooltip display was read from data, not seen in the live viewer.
- Why it helps students: The ID on screen is the same mark that is on the physical piece, so matching is by sight and works without reading.
- For our player: Engraved IDs must survive the model pipeline as visible dark geometry or texture. Per-part metadata field 'description' feeding a hover/tap tooltip. No label component is needed on mechanical steps.

### MECH-9 · confirmed

**Keep everything already built on screen, wires included, while the case goes on. Hide other parts only for bench work on a loose sub-assembly and for a harness that is not yet involved in the frame. Use ghosting only when a result must be seen through a panel.**

- Applies to: construction / mechanical; all three kits
- Evidence: Case steps with all prior wiring visible: LSM 18 of 18 (Steps 21-38), LAC 17 of 17 (Steps 41-57), PMG 19 of 26 (Steps 33-51). PMG hides all 74 electronics components for 7 steps (26-32). Opacity below 1 is used on one step in the corpus (0.5 on D1 and D5, LSM Step 34 and its copies in P4 and P3+4).
- Exceptions: PMG differs from LSM and LAC by hiding the harness for the bare-frame steps. Dangling electronics are often cropped by the frame edge in PMG case steps. No selective hiding of individual wires, cut-away or highlight colour was found in any build guide.
- Why it helps students: The picture stays a faithful copy of the desk, so the student can check cable routing against it while closing the box.
- For our player: Default visibility = everything installed so far. Provide an isolation set per step and a per-part opacity property. Do not auto-hide wires near the active joint.

### MECH-10 · qualified

**When a joint or cable ends up hidden or too small to read, confirm it on the completed step with an eye icon on the spot or a framed close-up (9 of 75 master mechanical c-steps; the other 66 are clean). The close-up marks the detail with a red box in LAC and PMG (4 of 6) and with an eye glyph drawn inside the picture in LSM (2 of 6). Close-ups also appear on the hover frame as orientation or quantity aids (3). A cable through a notch is shown by its result, not animated.**

- Applies to: construction / mechanical; all three kits
- Evidence: Master mechanical c-steps: 66 of 75 clean, 6 with an inset, 3 with an eye icon (all build guides: 152 clean, 14 inset, 7 eye). 9 insets on master mechanical steps, 13-22 % of viewport width, 6 on the c-step and 3 on the hover step.
- Exceptions: The USB lead through D4's U-notch (LSM Step 22) has no cue. Insets are pre-rendered images, some with the eye glyph baked in. A few stored inset positions disagree with the saved renders.
- Narrowed because: Counts reproduce: masters 66 clean (65 + PMG 51c with leftover lines), 6 inset, 3 eye; all build 152 / 14 / 7; 9 insets 13.2-22.2 % wide, 6 on c-steps, 3 on hover steps. Against 'red box on the detail': LSM 30c [068] and 34c [076] have no red box. Border: #7fdbff thickness 5 on 8 of 9; PMG 33c is #7fb9ff thickness 2. No cue for the USB lead through D4's notch at LSM Step 22.
- As first stated: When a joint or cable ends up hidden or too small to read, confirm it on the completed step with an eye icon on the spot or a framed close-up with a red box on the detail. Show a cable through a notch by its result, not by animating the cable.
- Why it helps students: It gives the student a concrete thing to check before moving on, at the moment a mistake is still easy to undo.
- For our player: Allow annotations on the completed frame (the c-step is not always clean). Inset = image in a rounded cyan-bordered box with a leader anchored to a 3D feature; needs an authoring path for close-up renders.

### MECH-11 · qualified

**Use a fat red arrow for a hand move that takes something off, flexes it or carries it: peeling the backing (2), pulling a fastener off (4), spreading two posts (2), carrying or sliding a tethered sub-assembly (4). Use lead lines when a part goes onto a target. Never put both on one step. Take-apart guides therefore use arrows for every removal.**

- Applies to: construction / mechanical; take-apart guides use arrows for every removal
- Evidence: 12 arrows on 11 steps in the masters; 0 of 75 master mechanical steps carry both an arrow and a lead line. 7 of 12 arrows share one style (#ff0000, body 5, head 20 x 15-17); length 25-103 mm. Take-apart guides: 24, 22 and 31 arrow showings against 0, 3 and 0 lead lines.
- Exceptions: One stray lead line shares a step with an arrow in LSM P1+2 Step 20 (a leftover, not visible). 5 of 12 arrows are hand-scaled variants. Some arrows are anchored to a neighbouring part rather than the part they describe (LAC Steps 42, 47).
- Narrowed because: Counts reproduce: 12 arrows on 11 master steps; 7 in body 5 / head 20 x 15-17; 24.7-102.9 mm; 0 of 75 mechanical steps with both; the only frame in the corpus with both is LSM P1+2 Step 20 [041]; take-apart 24 / 22 / 31 arrow showings against 0 / 3 / 0 lines. Against 'no mating feature to link': 4 of the 12 arrows pull a nut, washer or knob off a shaft (LSM 16; LAC 22-24) and every take-apart removal uses an arrow on a tab-and-slot joint, so absence of a mating feature is not the discriminator.
- As first stated: Use a fat red arrow only for a hand move that has no mating feature to link: peeling, pulling a fastener off, spreading two posts, carrying or sliding a tethered sub-assembly. Do not combine arrows and lead lines on one step.
- Why it helps students: It keeps two meanings apart: thin lines say 'this goes into that', the arrow says 'move it this way'.
- For our player: Arrow primitive: straight 3D arrow with fixed proportions (body 5, head 20 x 17), one per moving unit, removed before or as the motion starts. Validation rule in authoring: a step has lead lines or arrows, not both.

### MECH-12 · confirmed

**Re-aim the camera on entering most mechanical steps so the tabs and slots being joined face the viewer and the travel runs across the screen; hold it when the next step works at the same place.**

- Applies to: construction / mechanical; all three kits
- Evidence: Camera moves on entering 47 of 61 wood/tethered steps in the masters (108 of 141 in all build guides); median turn 65 degrees; 32 of 47 turn 45 degrees or more.
- Exceptions: Held on 'do the rest' steps, on second stages that read from the same view, and after a camera-only Transition (LAC [108]).
- Why it helps students: The hover gap and its lead lines are seen side-on, so distance and direction are readable.
- For our player: Per-step camera pose, tweened on step entry only. An auto-camera should place the travel vector roughly perpendicular to the view direction and keep 10-60 degrees elevation.

### Added by the re-check

- Every mechanical hover frame carries at least one cue and usually exactly one kind: lead lines, an eye icon, a red arrow or an inset. A bare hover frame never occurs. *Evidence:* 75 master mechanical Step N frames: lines 52 (4 of them with an eye, 2 with an inset), eye only 13, arrow 9 (2 with an eye), inset only 1 (PMG Step 39), none 0. All 173 build mechanical steps: none 0.
- The enclosure phase starts only after all wiring is finished, and plugging in the USB cable is the hand-over step in every kit. *Evidence:* Last step with a text label / USB step / first case step: LSM 19 / 20 / 21, LAC 39 / 40 / 41, PMG 24 / 25 / 26. No label-bearing step occurs after the first case step in any master.
- A panel-mount component enters from the side opposite its retaining hardware, so the leading end depends on the component: shaft-first when the hardware goes on the shaft, leads-first when it goes over the leads or the part snaps in. *Evidence:* LAC Full [055]: pot pushed shaft-first from behind F1, then washer [057], nut [059], knob [061] from the front. LSM Full [037]: button leads-first, nut over the leads [039]. LAC Full [032]: switch leads-first.
- Removal of pre-fitted hardware is shown on the bare component before its panel is on screen; the panel fades in only on the insertion step. *Evidence:* All 9 build-guide removal steps show no wood: LSM Full Step 16 [034], LSM P2 Step 8, LSM P1+2 Step 16, LAC Full Steps 22-24 [046]-[054], LAC P2 Steps 8-10. The panel first appears at LSM [037] and LAC [055].
- Lead-line ends are bound to part features and follow them; the stored point coordinates can be stale and should not be trusted for length. *Evidence:* Every line carries object_ids and object_local_positions. LSM Full Step 26 [057] stores two lines of 132.7 and 133.8 mm for a 42 mm move, and the render shows about 40 mm of red.
- A joint that is not finished stays visibly unfinished on the intervening completed frames until the step that finishes it. *Evidence:* D11 posts sit 7.0 mm proud from 32c [072] to 34c [076]; F7 posts stay splayed 15-16 degrees from 42c [093] across Step 43 to 44c [097]; D3, H5, H6, H7, H10 and F9 stay tilted between their two numbered steps.
- Wood uses two colour tokens everywhere: body #deb887 and engraving #1e1616. Two things break the pattern and should be decided on, not copied blindly. *Evidence:* All 34 kinds in the 3 CAD models carry those two colours. LSM D2 has extra face solids in #855e42, so its outer face renders dark brown in every view ([037], [048], [068]). LED stems are #ffffff.
- Loose tethered sub-assemblies are allowed to run off the frame during case steps; the camera frames the joint, not the whole kit. *Evidence:* LAC Full [088]-[103]: F1, F4 and the LCD are cut by the left and bottom frame edges. PMG P3 [023]-[031]: dot matrix and shield cropped. The analyst noted this for PMG only.

### Numbers (as corrected by the re-check)

| Setting | Value | Basis |
|---|---|---|
| Plywood thickness | 3.00 mm on 32 kinds; 3.18 mm on LSM D3 and D8. The LED stem is a 3.17 x 3.17 x 66.7 mm white square rod, not sheet | Bounding boxes of all 34 wood kinds plus the stem, from rootVersions |
| Hover distance, new wood part | median 68 mm; q1 54, q3 94; range 22-139 mm (claimed median 69, q1 55) | First-stage travel of the 28 new wood kinds in the 3 masters, recomputed |
| Hover, edge-first parts | median 81 mm, range 40-139 mm (claimed 82, 43-139; H2 at 40.0 mm is edge-first) | 16 parts with travel in the panel's own plane (/cos/ to normal under 0.35) |
| Hover, face-on panels | median 64 mm (22-69) - confirmed | 9 parts with travel along the panel normal |
| Hover as share of the part's longest dimension | median 0.7 (0.2-1.4) - confirmed | 28 parts, masters |
| Hover, breadboard onto base plate | 46.9 mm (LAC Full, LAC P1), 49.2 mm (LSM Full), 39.3 mm (LSM P1, LSM P1+2) - confirmed | 5 guides |
| Hover, panel-mount component through a panel | 79-103 mm - confirmed; leads-first for button and switch (5 of 7), shaft-first for the potentiometer (2 of 7) | 7 insertions, renders LSM [037], LAC [032], [055] |
| Hover, nut / washer / knob | 55.9-61.3 mm (LAC build), 80.4-83.1 mm (LSM) - confirmed | 12 fastener fits |
| Fastener removal travel | 37.6-37.9 mm (LAC build), 98.9-100.7 mm (LSM builds) - confirmed | 13 removals |
| Hover, LED stem | 43.5 / 50.3 / 55.1 mm - confirmed | LSM Full, P4, P3+4 |
| Lead lines per frame | 1, 2 or 4 on 147 of 149 line-bearing steps; 6 on 2 steps; never 3 or 5. Treat 4 as the usual maximum, not a hard one | 425 numbered steps: 37 / 69 / 41 / 2 |
| Lead-line length, wood joints | 0.98-0.99 x stage travel (IQR 0.93-1.02); PMG single-stage lines are travel minus 3.0-3.5 mm - confirmed | 83 lines in masters (claimed 81); 6 PMG lines |
| Lead-line length, axial parts | 1.16 x hover (0.86-1.26) - confirmed | 19 fastener fits and panel-mount insertions |
| Lead-line style | #ff0000, scale 5, world_units false, no arrowhead, rendered solid - confirmed; 36 stored dashed | 363 of 363 line showings; render [078] |
| Hinge tilt on arrival | 8-24 degrees on arrival (7.9, 10.3, 11.7, 18.1, 21.4, 21.6, 23.6); the claimed 25.8 is F9 tilting mid-move | 7 panels that appear tilted; F9 appears upright |
| Lock slide / push-home / clamp splay | 6.7 and 7.6 mm / 7.0 mm / 15.1 and 16.0 degrees - confirmed | PMG H11, H12 / LSM D11 / LAC F7 |
| Step duration | 800 ms on 1030 of 1037 frames - confirmed. 1600 ms is on 5 of the 11 spinning-fastener frames only (older LSM copies and LSM Full removal); the other 6 spin at 800 ms | All frames; spin frames LSM Full [035], [040], LSM P2 [017], [022], LSM P1+2 [033], [038], LSM Decon [049], LAC Full [050], [053], LAC P2 x2 |
| Nut spin while travelling | 170.9-179.6 degrees on 6 of 7 LSM nut moves; 115.1 degrees on the LSM Full refit | 7 LSM nut moves (claimed 6) |
| Ghost opacity | 0.5 - confirmed | LSM Full Step 34 and its 2 copies |
| Arrow | #ff0000, body 5, head 20 x 15-17, length 25-103 mm - confirmed (7 of 12 in that exact style) | 12 arrows in masters |
| Eye icon width | 7.81 % (17), 7.92 % (1), 8.2 % in PMG (7) - confirmed | 25 eye icons on master mechanical steps |
| Inset width and border | 13.2-22.2 % of viewport; border #7fdbff thickness 5 on 8 of 9, #7fb9ff thickness 2 on PMG 33c | 9 insets on master mechanical steps |
| Camera turn on entering a mechanical step | median 65 degrees; camera moves on 77 % of steps - confirmed (84 % if a preceding camera Transition counts) | 47 of 61 wood / tethered steps, masters |
| View height over the working orientation | 10-60 degrees, median 34 - confirmed | 73 of 75 master mechanical steps |
| Camera turn when the up-axis is re-declared | 43-167 degrees - confirmed | 39 up-axis changes in 12 guides |
| Wooden parts per numbered step | 1 kind on 36 of 37 introducing steps; 1 piece on 30 of 37 (81 %), an identical pair on 4, rest-of-set on 2, two different panels on 1 (PMG Step 26) | 37 wood-introducing steps, masters |
| Share of wood parts needing two motions | 38 % - confirmed | 13 of 34 wood kinds |
| Text labels on mechanical steps | 0 - confirmed | 173 mechanical steps in 16 build guides, plus 0 on take-apart mechanical steps |

### Open questions

- No screw, bolt, standoff, threaded insert or tool appears in any of the 20 guides (only one panel nut, and a washer + nut + push-on knob). How TechBox wants screws shown - one per step or 'first one, then Nx', spin, size text such as 'M3 x 6 mm', a screwdriver - cannot be derived and needs a decision.
- Lead-line cap: 41 steps use 4 lines and none use more, except two older LSM copies with 6 (one per tab). Is 'at most 4, 2 per neighbour' the intended rule, or 'every tab'?
- Two-stage joints: 8 parts use a second numbered step and 6 use a mid-step auto Transition. The camera explains PMG but not LSM D3 or LAC F9. What is the intended threshold?
- Turning the kit over: LSM uses auto Transitions, LAC and PMG cut directly on the step. Which should the player do?
- Should threaded parts spin and take 1600 ms everywhere? It is consistent only in the LSM part guides; LAC's nut does not spin on refit and LSM Full re-authored the refit at 800 ms.
- Hide the wired harness while the bare frame is built (PMG, 7 steps) or keep it visible throughout (LSM, LAC)?
- Ghosting at 50 % opacity is used on one step in the whole corpus. Convention or one-off?
- Hover distances are hand-picked (22-139 mm). Is '0.7 x longest dimension, clamped 40-140 mm, along the joint axis' acceptable as an automatic default?
- Are the '<Role> - Part <ID>' tooltips actually shown to students in the live viewer? This was read from the data only.
- No cue ever tells the student to turn the kit over. Should the in-house player add one, or stay faithful to the source?

## Deconstruction (take-apart) guides

### DEC-1 · confirmed

**Build a take-apart guide on the construction skeleton: `Start`, then numbered `Step N` / `Step Nc` pairs with auto `Transition` frames only between an N and its c, then `Completed View`. Leave out section cards and all text. Restart numbering at 1, independent of the build's numbers.**

- Applies to: deconstruction; all three kits (LSM, LAC, PMG)
- Evidence: 0 section cards in 3/3 take-apart guides (full builds have 4, 5, 5). 0/260 frames have a description or popup. 93/94 numbered steps have a `Step Nc`. 66/66 Transitions sit between an N and its c (full builds: 17/24). Start/N/c/end wait for the student 194/194; Transitions auto-advance 64/66. Counted with reports/_work_dim_decon/a1_frames.py over all 20 guides (corrected state walk, not the digests).
- Exceptions: PMG Step 23 has no `23c`; `Completed View` [060] performs the last removal. LAC [104] is named `Step 41` but is Step 40's instruct frame, [105] `Step 40` is an unchanged duplicate, [120] is named `Step 45c` but is Step 45's instruct frame. LAC shows 4 pin-name labels (DEC-11).
- Why it helps students: The student already knows the Step / Step-c rhythm from the build, so nothing new has to be learned; a take-apart needs no component introductions and no hole names.
- For our player: Same frame kinds as the construction player (pause-instruct, auto, pause-result, title, end); a take-apart document needs no card type and no text channel. Number steps from their order; do not trust authored step names.

### DEC-2 · confirmed

**On `Step N` change nothing in the model: show the part still seated and put every cue (arrow, eye icon, inset, label) on that frame only. `Step Nc` carries no cue at all.**

- Applies to: deconstruction; all three kits
- Evidence: Part to be removed is in its seated pose on `Step N` in 91/91 removal steps (the other 3 steps are re-fits). 95/95 N frames carry at least one cue. 0/93 c frames carry one (full builds: 11/146 c frames carry a check cue). Transitions carry none in LSM and LAC (0/52).
- Exceptions: PMG shows the second-stage arrow of a two-stage removal on the auto Transition (9 of its 14 T frames); on PMG Steps 2 and 3 that is the only arrow ([005], [010]), on screen about 0.8 s. 19 N frames change other geometry: 10 scene switches (DEC-13), 3 re-fit hover-ins (LAC 16-18) and visibility slips (LSM [001] [013] [046], LAC [001], PMG [001] [028]).
- Why it helps students: The paused picture still looks like the kit on the desk and answers 'which part, which way, what holds it' before anything moves; the result frame is a clean picture to compare against.
- For our player: Cues are scoped to the instruct frame with fade in/out and must be hidden when the removal animation starts. The model state on `Step N` equals the previous result state (plus an optional camera move).

### DEC-3 · qualified

**After Next on Step N the removal plays to the end and the next paused frame shows the part gone: true for 63 of the 65 steps that hide a part (LAC Steps 12 and 44 need an extra click). Usually, not never, avoid pausing on the pulled-out state: 5 paused frames show it. Removed free parts are never left on a paused frame, but LAC parks each loose jumper beside the model for one auto frame, and whatever is left in an isolated view stays until the scene switch. Two encodings exist and neither is settled as house style: A (auto frame tweens the part out, c fades it; LSM 17, LAC 14, and 6/6 removals inside the full builds) and B (displacement and hide written in the same frame; PMG 18, LSM 1).**

- Applies to: deconstruction, rigid parts and free wires; all three kits. Also every removal action inside the construction guides.
- Evidence: Removed part hidden at `Step Nc` in 65/94 steps (LSM 19/24, LAC 28/47, PMG 18/23). Encoding A = N -> auto Transition tweens the part out -> c fades it: LSM 17 steps, LAC 14, plus 6/6 removal steps in the full builds (LSM B1, B16; LAC B1, B22, B23, B24). Encoding B = N -> c with the displacement and visible=false written in the same frame (slide while fading): PMG 18/23, LSM 1 (Step 4). The other 29 steps: 22 cross-fades of wired things that stay on screen, 3 tweens where the part stays (LAC 15, 26, 35), 1 slip, 3 re-fits. 0 removed loose parts are ever parked beside the model. A = 1.6 s (800 + 800 ms), B = 0.8 s.
- Exceptions: PMG Step 8c [027] leaves plate H10 hovering in front of the housing until Step 9 [028]. LSM Step 20 and LAC Steps 23, 31 fade the part with no motion. LAC [118] Transition is `pause` (extra click). In LSM Part 1 and Part 1+2 the peel-backing removal has no Transition. 'Slides while fading' is inferred from the frame's animation settings (move tween, hide fade), not observed in the live viewer. Which encoding is house style is not settled: the newest guide (PMG, 2026-08) uses B, the two older ones and all build-internal removals use A.
- Narrowed because: Paused frames showing the pulled-out part: LAC [033] (pause Transition, knob held +55 mm - the analyst lists it only as doing nothing), LAC [118] (pause Transition, RTC +22 mm), LAC [042] 15c (potentiometer pulled out of F1 and left beside it), LAC [091] 35c (rocker switch pulled out of F4), PMG [027] 8c (H10 hovering). Timing is 1.6 s or 0.8 s only for single-stage removals: only 12 PMG steps are a pure 0.8 s; PMG two-stage steps take 1.6 s (6 steps), LAC two-stage steps 2.4 s (Steps 2, 24, 28), LSM Step 4 1.6 s with an empty first half.
- As first stated: After Next is pressed on `Step N`, play the removal to its end with no further click: the part travels out along the arrow and disappears, and the next paused frame shows it gone. Never pause on the pulled-out state and never leave removed loose parts on screen.
- Why it helps students: One physical action costs one click, and the screen always shows exactly what is still assembled; no pile of loose parts to misread.
- For our player: Provide a compound 'remove' action: tween to an offset then fade (sequential), plus a simultaneous tween+fade variant. When importing Cadasio-style data, fold auto frames between N and c into the step instead of exposing them.

### DEC-4 · confirmed

**Use auto-advancing `Transition` frames only as the motion stages inside a step (tween out, unhook stage, pose flipbook, routed-to-loose wire swap). Keep the camera still on them, hide them from the step picker and hide the navigation overlay while they play.**

- Applies to: deconstruction; all three kits (same attributes as Transitions in construction guides, different job)
- Evidence: 66 Transitions: 41 part motion (LSM 17, LAC 17, PMG 7), 21 cross-fades between pose or wire models (1, 15, 5), 2 camera-only, 2 empty. play 64/66; hidden from step picker 60/66; overlay hidden 61/66; 800 ms 64/66; camera unchanged 64/66. Auto frames are 64/260 = 24.6 % of take-apart frames against 24/336 = 7.1 % in the three full builds (51/775 = 6.6 % over all 16 construction guides); 0.70 Transitions per numbered step against 0.16. Steps containing at least one: 57/94 (LSM 19/24, LAC 28/47, PMG 10/23) against 15/146. Reason for the difference: in construction the hover-to-seat motion plays on the paused `Step Nc`; in take-apart the motion must finish and the part must vanish before the next pause.
- Exceptions: LAC [033] (does nothing) and [118] are `pause`. LAC [016] [017] run 1600 ms. Not hidden from the picker: LSM [044] [052] [066], LAC [033] [118], PMG [026]. LSM [011] moves nothing. Names misspelt: LSM [038] `Transiton`, LAC [002] `Transititon`.
- Why it helps students: The motion finishes by itself and the student lands on a stable frame; hidden auto frames cannot be navigated to by accident.
- For our player: Model a step as an ordered list of animation stages with a single wait-for-Next at the end; stages never appear in navigation. The study README's description of Transition as a camera step does not hold here (2/66).

### DEC-5 · qualified

**Pull a removed rigid part in a straight line along its insertion axis; the axis matches the build's hover offset in about 93 % of comparable part-moves. Copy the build's hover vector exactly only where the phase is authored as a mirror of the build: 17 of 42 comparable moves are bit-identical (LSM 5, LAC 4, PMG 8). Elsewhere the travel is chosen afresh, 0.31 to 1.52 times the build hover, and parts that faded in seated in the build have no hover to copy at all (PMG H1, LED matrix, display, buttons, all three wire bundles; LSM 3-way connector).**

- Applies to: deconstruction, mechanical and plug-in parts; all three kits
- Evidence: 42 rigid part-moves paired by part name with the hover offset at the part's first appearance in the full build: same direction (cos >= 0.95) 39/42; identical vector (within 1.5 mm) 17/42 (LSM 5, LAC 4, PMG 8); length ratio take-apart/build median 1.00, range 0.55-1.52. Travel used: plug-in electronic parts median 31 mm (22-55, n 9); laser-cut wood median 68 mm (29-143, quartiles 54-89, n 31). Arrow directions: 41 screen-up, 30 sideways, 5 diagonal, 1 down of 77.
- Exceptions: Direction differs where a tilt-in joint is flattened to one pull: LSM D3 (38 mm straight against a 64 mm oblique tilt-in), LSM D10, LAC F9. Distances not copied: LSM D6 45 vs 64, Nano 33 vs 46, stems 62.5 vs 41; LAC F7 44 vs 80, RTC 22 vs 34, resistors 51-52 vs 37-40, Nano 55 vs 40; PMG keys 142 vs 108, H14 69 vs 58. Nut rotation while travelling only in LSM [049] (176 deg); LAC nut [036] does not spin.
- Narrowed because: Direction differs: LAC F9 (cos 0.17), LSM side panel Side1 (38 mm straight against 64 mm oblique, cos 0.83), LSM small matrix support. Length differs: LSM Lens_Bottom 0.70, Nano 0.67, stems 1.52, Side4 1.29; LAC F7 0.55, RTC 0.65, resistors 1.27 and 1.39, Nano 1.38; PMG keys 1.32, H14 1.19, USB 1.29, Nano 0.87. The stated ratio range 0.55-1.52 leaves out F9 at 0.31. Plug-in travel is bimodal, not about 30 mm everywhere: LSM 29-31, PMG 26, LAC 22 (RTC) and 51-55. Arrow screen directions by my projection: 40 up (within 30 deg), 19 sideways, 17 oblique of which 10 point below the horizontal (mostly LAC), 1 straight down - the analyst's 41/30/5/1 hides the downward-oblique ones. Notation hazard: in the analyst's exception lists LSM D3, D6, D10 are engraved panel names (LSM panels are engraved D1-D11), not step numbers; panel D3 is removed in Step 16.
- As first stated: Move a removed rigid part in one straight line along its insertion axis, away from its seat, to the pose it hovered at in the build. Default travel = the part's hover offset in the construction guide.
- Why it helps students: The part leaves exactly the way it went in, so the motion itself teaches the pull direction and reuses a picture the student has already seen.
- For our player: No new motion data is needed: store seated pose + hover offset per part once and play the construction tween backwards for the take-apart.

### DEC-6 · qualified

**Where the build seated a panel with a hook-and-swing or slide-and-lock joint, PMG and LAC undo it inside one numbered step as two auto-chained stages, small unhook first and long pull second: 10 steps (PMG 7, LAC 3). First stage is a 6.7-8.9 mm slide (3 steps) or a 7-26 deg tilt about a pivot at the tab (7 steps); second stage 33-139 mm. LSM does not do this, and the reversal can be partial.**

- Applies to: deconstruction, mechanical (laser-cut panels); PMG and LAC
- Evidence: 10 steps. First stage is a 6.7-8.9 mm slide or an 8-26 deg tilt about the tab edge; second stage 44-139 mm. The build used two numbered steps for 6 of these joints (LAC F9, F7; PMG H5, H6, H7, H10) and a mid-step Transition for the other 4.
- Exceptions: LSM flattens both of its tilt-in joints (D3, D10) to one straight pull. The cue differs by kit: PMG shows arrow 1 on N and arrow 2 on the Transition (7/7); LAC shows a single arrow on N (3/3).
- Narrowed because: Second-stage minimum is 33.0 mm (LAC F9 [065]), not 44. LAC F9 reverses only the last two of the build's four motions (swing out, lift 33 mm, fade); the build's 104 mm sideways slide is not played back. LAC Step 2's single arrow points straight up while the lid tilts and then slides 57 deg away from the arrow (cos 0.55). LSM flattens its two tilt-in joints to one straight pull (side panel in Step 16, small matrix support in Step 14). For the player: tilts are stored as a rotation plus an explicit pivot (origin, use_origin) with the position already compensated.
- As first stated: Undo a hook-and-swing or slide-and-lock joint inside one numbered step: play the build's stages in reverse (small unhook or tilt first, then the long pull), chained by auto frames.
- Why it helps students: Shows that the panel must be released before it is pulled, without spending two clicks on one part.
- For our player: Support multi-stage part motion with rotation about a custom pivot and an optional cue per stage.

### DEC-7 · qualified

**Cue every tween or slide removal with a red (#ff0000) straight 3D arrow, head at the end, proportions body 5 : head width 20 : head length 17, on Step N (54/54 motion steps have one; PMG puts the second-stage arrow on the auto frame). One arrow per moving unit: two identical parts get an arrow each, four or more share one; never more than 2 per frame. The arrow points along the translation that follows, except where the first motion is a tilt. Length is hand-set, mostly 40-70 mm, and follows the travel only loosely. No lead lines on a removal.**

- Applies to: deconstruction, rigid parts and bundles; all three kits. The same meaning (pull / move by hand) holds for the few arrows in construction guides.
- Evidence: Every step that tweens or slides a rigid part has an arrow: 54/54. Arrows on 61/94 `Step N` frames (LSM 21, LAC 20, PMG 20) plus 2 PMG steps where it is only on the Transition. 77 arrows shown (24, 22, 31) against 12 in the three full builds; lead lines 3 against 149. One arrow on 54 frames, two on 7, never more; one arrow stands for a group of identical parts (64 stems, 4 keys, 4 buttons, 5 wires). Arrow direction equals the next frame's motion in 58/59 pairs. Length median 53 mm (quartiles 40-69, range 16-116). Length/travel median 0.96 over 55 pull-stage pairs (range 0.41-1.64; LSM 1.05, LAC 0.92, PMG 0.94). Style: #ff0000, straight, head at end 77/77; body width 5 / head width 20 in 71/77; head length 17 in 65, 15 in 6. Table: tbl_arrows.md.
- Exceptions: LAC F9 [063]: arrow points up while the first motion is a tilt. PMG unhook-stage arrows are 5-7 times longer than the 7-9 mm unhook. PMG [001] has two overlapping arrows; PMG [014] is thin (body 2, head 10); LSM has 5 off-style arrows. Per-arrow scale ranges 0.025-0.75, so on-screen thickness varies a lot (thin in PMG [040], very fat in PMG [053]). What the arrow is attached to in the data is inconsistent (the moving part in PMG 31/31, a static neighbour in LAC 22/22, mixed in LSM). LSM D20 has an arrow but the cable only fades; LSM D9 reuses D8's arrow unmoved. 8 of 34 cross-fade steps also carry an arrow.
- Narrowed because: Length is within 10 % of the travel in only 13 of 56 pairs and within 25 % in 31. Direction: LAC [063] F9 (listed) and also LAC [004] F2, whose arrow is 57 deg off the slide. 18 of 77 arrows are not followed by a translation at all: 8 precede a tilt, 8 a cross-fade, 2 nothing (LSM Step 4's empty Transition, LSM Step 20). 'One arrow stands for a group' holds only for groups of four or more (64 stems, 4 keys, 4 buttons, 5 wires); pairs get two arrows (LSM Steps 6, 7, 10; LAC Step 28). The raw per-arrow scale 0.025-0.75 is not comparable across kits because scene units differ (LSM 2.09, LAC 1.65, PMG 23.6 mm per unit); if scale multiplies the cross-section, shaft thickness is about 3.7 mm (LSM), 4.0 (LAC), 6.7 (PMG) median, range 1.3-11.8 mm.
- As first stated: Cue a rigid removal with one thick red straight 3D arrow per moving unit on `Step N`: tail on or right beside the part, head along the pull direction, length about the travel. Never use lead lines for a removal.
- Why it helps students: A removal has a direction but no target, so one bold arrow reads faster than several thin feature-to-feature lines; red already means motion in every guide.
- For our player: Generate the arrow from the removal vector: origin on the part, direction = removal direction, length = travel clamped to roughly 20-115 mm, constant on-screen thickness, one per moving unit or group, at most two per frame. Treat it as a free world-space object.

### DEC-8 · confirmed

**If something is fitted during a take-apart (for example hardware put back on a component for storage), use the construction grammar for that step: part hovering on its axis with one thin red lead line on `Step N`, seated on `Step Nc`, no Transition.**

- Applies to: deconstruction, mechanical; LAC only (Steps 16-18)
- Evidence: 3/3 re-fit steps: hover 54 / 38 / 43 mm on the shaft axis, lead line 61 / 39 / 49 mm (ratio 1.04-1.15), seat tween on c, 0 arrows, 0 Transitions. These are the only 3 lead lines shown in 260 take-apart frames.
- Exceptions: Single guide. LSM does not re-fit the button nut it removes in D18; the equivalent LSM build prep step B16 has no take-apart counterpart.
- Why it helps students: Arrow keeps meaning 'take off', lead line keeps meaning 'this goes there', even inside the same guide.
- For our player: Cue type follows the action (fit vs remove), not the guide type; the take-apart player must still render lead lines and hover-then-seat.

### DEC-9 · confirmed

**Use the eye icon to mark what has to be released, unplugged or picked up when the action has no single pull direction (it is shown by a cross-fade), and optionally next to an arrow to point at the catch or plug. On a wire, aim its leader at the connector housing at the end to pull.**

- Applies to: deconstruction, wiring and wired modules; all three kits (heavy in LSM and LAC, rare in PMG)
- Evidence: Cross-fade steps: eye on 30/34, 26 of them with no arrow. Fade-only steps: 3/3. Tween/slide steps: eye added to the arrow on 14/54 (LSM 11, LAC 2, PMG 1). Used on 47/94 steps (LSM 16, LAC 27, PMG 4), the same rate as in the full builds (71/146) where it means 'pick up / look at this loose part'. Leader ends on a plug housing for all 26 wire-step eyes (LSM 6, LAC 20). Width 7.81 % of the viewport 44/44 in LSM+LAC, 8.2 % 4/4 in PMG; leader #7fdbff with dashed ring; placed in free white space (x 13-68 %, y 7-63 %).
- Exceptions: Density differs threefold between kits, so how many eyes are wanted is an authoring choice, not a rule. LSM [010] eye has a box round it. LSM [010] and [013] eyes are anchored to a panel that is not rendered. PMG D12 (buttons out) has only an eye, no arrow anywhere.
- Why it helps students: Tells the student where to put their fingers when the picture cannot show a travel path.
- For our player: Screen-space icon with a leader that follows a 3D anchor on the plug; default it on for wire-unplug and pose-swap steps, optional elsewhere.

### DEC-10 · qualified

**Optionally add a framed close-up of the catch on Step N; this is an LSM habit, not a rule: 10 uses over roughly 33 panel removal or dismount steps (LSM 8, LAC 2, PMG 0). Style as stated: same toon render, one or two thin red rectangles on the tab, #7fdbff rounded frame of thickness 5, leader to a ring on the feature.**

- Applies to: deconstruction, mechanical; LSM (8) and LAC (2), none in PMG
- Evidence: 10 uses, all on N frames. Width 7.8-9.9 % of the viewport for a single latch (6 uses), 15-25 % for a whole panel face (4). Border #7fdbff thickness 5. Paired with an eye on 8/10; where two catches exist the eye marks one and the inset the other (LSM D4-D7).
- Exceptions: LSM [043] frame is clipped (no bottom edge). LSM D8 (lens bottom plate) has none. PMG uses none although its housing has the same kind of tabs.
- Narrowed because: No inset on LSM Steps 8, 10, 14, 19, on LAC Steps 1, 2, 3, 7, 28, or on any of PMG's 12 panel steps although those joints are the same kind.
- As first stated: When a laser-cut tab or latch must be released, add a framed close-up of the catch on `Step N`: same toon style, one or two thin red rectangles on the tab, light-blue rounded frame, leader to a ring on the real feature.
- Why it helps students: The catch is too small at whole-model zoom, and the camera stays wide in take-apart guides.
- For our player: Reuse the detail-inset asset of the construction step being undone when one exists; inset is an N-frame cue.

### DEC-11 · qualified

**Show no text in a take-apart. The only labels are four pin names (GND, VCC, SDA, SCL) on LAC Steps 19-22, marking the LCD-header end of the wire whose breadboard end carries the eye. Style: project default font (PublicSansMedium), bold, 3em, black, #7fdbff underline of thickness 5 with drop shadow, #7fdbff leader.**

- Applies to: deconstruction, wiring; all three kits
- Evidence: 4 labels in 260 frames (LAC Steps 19-22), held at (28-30 %, 37-39 %) of the viewport, Arial bold 3em on a #7fdbff underline. 0 breadboard-hole, rail or quantity labels; LSM 0, PMG 0. The full builds show 99 labels.
- Exceptions: None beyond the 4 LAC labels.
- Narrowed because: The font is not Arial: the four labels have no font-family and are registered as PublicSansMedium only, whereas the 41 inherited, never-shown build labels are Arial. The 'tells identical wires apart' rationale is thin: the other 16 LAC wire steps (three potentiometer leads, two buzzer leads, three switch leads, eight jumpers) and every LSM and PMG wire step have no label.
- As first stated: Show no text labels in a take-apart. The only justified label is a pin name that tells adjacent identical-looking wires apart.
- Why it helps students: Unplugging needs no destination; a hole coordinate would be noise. A pin name helps only when four identical plugs sit side by side.
- For our player: When deriving from a construction step, drop its hole labels; keep module pin-name labels only as an optional disambiguation.

### DEC-12 · confirmed

**Do not animate wires being re-routed. Unplug by cross-fading the routed wire model to a loose model (eye on the plug, no arrow) and then fading it, or slide a whole bundle off in its routed shape. Captive leads swap to a dangling pose and stay until their component leaves.**

- Applies to: deconstruction, wiring; all three kits (two different techniques)
- Evidence: LSM+LAC: 25 wire steps, 23 are eye-only cross-fades (LSM 3, LAC 20). Free jumpers pass through one auto frame as a straight loose wire at the build's staging spot (159-184 mm to the side) and then fade: LAC 12/12. Captive leads swap on c and stay: LAC 8/8, LSM 3/3. PMG: no loose-wire models; 5 wires slide 90 mm (D18) and 16 wires slide 36 / 75 mm (D22) with their housings and fade. Wires per step: LAC 20 wires in 20 steps; LSM 5 wires in 3 single steps + 2 grouped steps; PMG 21 wires in 2 steps. The builds were finer or equal (LSM 7 wire-end steps, LAC 20, PMG 21).
- Exceptions: LSM D15 tweens a 3-way connector 30.5 mm with an arrow; LSM D17 unplugs two button wires together with removing panel D2. Which end comes off first differs: LSM board end then module end; PMG module end then shield end; LAC both ends in one step. Order inside a wire group is not consistently reversed (LAC pot and switch leads reversed, LCD wires and buzzer leads forward; LSM white, purple, grey).
- Why it helps students: Keeps wire steps instant and unambiguous; the picture after the click matches a wire lying loose or hanging.
- For our player: Cross-fade between alternative wire models must be a first-class operation; keep the loose/staging model from the construction guide. Wire granularity (per wire vs per bundle) has to be an authoring setting.

### DEC-13 · qualified

**Dismount a wired module from the housing first by cross-fading it to a set-aside pose with its wires attached, and unplug it later. Take sub-assemblies apart in an isolated view with everything else hidden; switch scenes only on a Step N together with a camera move. Whatever is left in an isolated view is not removed by a step: it disappears at the next scene switch.**

- Applies to: deconstruction, wired modules and sub-assemblies; all three kits
- Evidence: 11 dismount steps (LSM 2, LAC 5, PMG 4); the on-screen part count does not drop on any of them. Pose chains played as flipbooks: LCD 4 poses, PMG matrix 4, display 4, shield 3. 10 scene switches; 10/10 happen on a `Step N` with a camera move (9-112 deg), 0 on a Transition or c. Hidden at a switch: 19 and 9 components (LSM), 64 and 32 (LAC), 74 (PMG).
- Exceptions: PMG never removes side panels H2 and H3 by a step; they vanish at the scene switch [047]. LSM renders the box with side D3 missing from [001] to [027] and the matrix missing until [026]. In PMG's flipped block the loose electronics hang upside-down in mid-air [032]-[036].
- Narrowed because: The analyst treats PMG H2/H3 as the exception, but it is the pattern at all 6 exits from an isolated view: LSM LED matrix module (vanishes at [043]), LSM button panel ([054]), LAC potentiometer assembly with its re-fitted hardware ([049]), LAC panel F4 and rocker switch ([092]), PMG H2 and H3 ([047]); LAC panel F1 also vanishes without a step, on Step 16's instruct frame [043]. 'Part count does not drop on any dismount' is off by one twice: LSM Step 17 (backing paper vanishes) and LAC Step 4 (the pose copy has no nut).
- As first stated: Dismount a wired module from the housing first, by cross-fading it to a 'set aside' pose with its wires still attached, and unplug it later. Take sub-assemblies apart in an isolated view with everything else hidden, and switch scenes only on a `Step N` together with a camera move.
- Why it helps students: Matches what the hands must do (nothing can be unplugged while trapped in the box) and removes clutter while a small sub-assembly is stripped.
- For our player: Needs several posed instances of a module (each with its own wire models) that can be cross-faded, per-step visibility sets for isolation, and scene switches bound to instruct frames.

### DEC-14 · qualified

**Housing: reverse of the build at part level in LAC and PMG; LSM departs from it. Electronics: component by component, bare jumpers pooled, plug-in parts then the controller last (3/3). Whether the wires or the component come off first is per kit: LAC unplugs a component's wires and then takes the component (4/4), PMG takes the module off its wires first and then removes the wires (3/3), LSM frees the board end, then the module end.**

- Applies to: deconstruction ordering; all three kits (strict reverse only in the mirror-authored phases)
- Evidence: Consecutive take-apart steps in reverse build order: LSM 18/23, LAC 32/44, PMG 18/22 (+2 ties); pooled 68/89 = 76 %. All step pairs in reverse order: 84 %, 83 %, 98 % (1305/1519 = 86 %). Strictly reverse run from Step 1: LSM 5 steps, LAC 18, PMG 17. The controller board is the final removal in 3/3.
- Exceptions: Not an exact reverse in any kit. LAC has 12 order breaks, LSM 5, PMG 2. PMG's bench phase appears to sweep left to right across a fixed view (single guide, inference).
- Narrowed because: PMG Steps 17, 20, 21 remove the module before its wires, the opposite of 'its wires, then the component'. LSM order breaks, in build step numbers: 22 then 33, 10 then 12, 11 then 29, 15 then 25, 17 then 20.
- As first stated: Order the take-apart as the reverse of the build at part level for the mechanical housing; for electronics work component by component (its wires, then the component), pool bare jumpers, and remove plug-in parts and the controller last.
- Why it helps students: Whatever went on last is on the outside and comes off first; finishing one component before touching the next keeps loose wires manageable.
- For our player: Auto-derivation can start from the reversed build order but needs a dependency check (a wired module must be dismounted before the panels trapping its wires, and unplugged only once out) and an authoring override for regrouping.

### DEC-15 · confirmed

**Make the take-apart coarser than the build: drop build steps that cannot or need not be undone (sticking the first part down, preparing a loose part, handling or check steps) and merge build steps that dealt with one part into one take-apart step.**

- Applies to: deconstruction; all three kits
- Evidence: 94 take-apart steps for 146 build steps = 0.64 (LSM 24/38, LAC 47/57, PMG 23/51). 18/146 build steps have no counterpart (4 adhesive-base, 10 preparation, 4 handling/check). 19 merges absorb 20 build steps (LSM 5, LAC 4, PMG 10); PMG's 23 remaining electronics steps become 7. Arithmetic: LSM 38-8-6 = 24; LAC 57-8-4+2 = 47; PMG housing 26 -> 16, bench 25 -> 7.
- Exceptions: LAC adds steps the build never had: 'take the freed component away' (D23 LCD, D31 buzzer) and three re-fits (DEC-8). LAC keeps one wire per step, so it shrinks least.
- Why it helps students: A take-apart is quicker and needs less explanation; the student only sees actions that actually separate something.
- For our player: Construction steps need a kind tag (seat, wire, module re-pose, preparation, handling/check, removal) and a part id so preparation steps can be skipped and same-part steps merged automatically.

### DEC-16 · qualified

**Usually one unit per numbered step; fasteners get their own steps (LSM nut; LAC knob, nut, washer). Identical parts: a pair is removed in one step with an arrow on each part, and four or more identical parts leave together under a single cue. PMG also removes wires as bundles of 5 and 16.**

- Applies to: deconstruction, mechanical; all three kits
- Evidence: Steps acting on exactly one component: LSM 19/24, PMG 15/23; every LAC step is one wire, one rigid part or one inseparable unit (RTC + cell, USB cable + adaptor, component + soldered leads). Grouped identical parts: 7 steps.
- Exceptions: LSM D17 combines a panel removal with unplugging two wires. PMG removes wires as bundles (DEC-12).
- Narrowed because: 'Cue on one of them' is false for pairs: two arrows on LSM Steps 6, 7, 10 and LAC Step 28. LSM does not let its four identical lens supports leave together; it splits them 2 + 2 over Steps 6 and 7 with a 131 deg camera swing between. Grouped identical-part steps are 9 (LSM 1, 6, 7, 10; LAC 26, 28; PMG 9, 12, 20), not 7 - the analyst's own evidence list has 9. PMG 15/23 could not be reproduced without the analyst's definition of a unit; the clearly multi-part PMG steps are 9, 12, 18, 20, 22.
- As first stated: Remove one unit per numbered step; identical parts that come off the same way leave together with the cue on one of them; fasteners get their own steps.
- Why it helps students: Keeps each click small, without making the student repeat an identical action four or sixty-four times.
- For our player: A removal action takes a list of parts sharing one motion; a single arrow may represent the group.

### DEC-17 · confirmed

**Start on the build's title page with the finished model (subtitle image 'Deconstruction'); end on a clean `Completed View` showing only what the guide leaves assembled.**

- Applies to: deconstruction; all three kits
- Evidence: Start camera identical to the build's Start in LSM and LAC (PMG elevation 33 vs 21). Title images removed on entering Step 1 in 3/3. Logo at x 1.8-5.1 %, y 5.0-7.8 %, width 36-39 %; title block at x 1.8-3.8 %, y 61-64 %, width 42-46 %. End-frame part set equals a build frame exactly (symmetric difference 0): build `Step 2` / `2c` for LSM and LAC, the first section card for PMG. End frame has 0 annotations in 3/3; camera re-frame is small (LSM 17.5 deg orbit, LAC 5 deg and one zoom notch in, PMG none).
- Exceptions: The name is inherited: nothing is completed. PMG's `Completed View` also performs the last removal (no Step 23c). PMG's saved Start frame has the title text running under the model.
- Why it helps students: The first picture matches the object in front of the student; the last one shows the state the kit should be in when it goes back in the box.
- For our player: Derive the end state as the set of parts whose build steps are not undone; do not fly back to the Start camera.

### DEC-18 · confirmed

**Move the camera only on entering a `Step N` and hold it through the auto frames and `Step Nc`; reuse the camera (and scene up-axis) of the construction step being undone; keep one view for a run of similar steps.**

- Applies to: deconstruction camera; all three kits
- Evidence: Camera moves on 55/95 N frames (LSM 19/24, LAC 16/48, PMG 20/23), 0/93 c frames, 2/66 Transitions. 26/55 Step-N camera poses are bit-identical to the build step being undone (LSM 5, LAC 7, PMG 14). Elevation 24-51 deg (LSM), 25-50 (LAC, one -24), 13-41 and a flipped block at -24 to -40 (PMG). Distances stay on the x1.166 zoom ladder; closest 162 mm (LSM), 237 (LAC), 173 (PMG) against 42-110 mm in the builds, because there are no cards or prep close-ups. Up-axis flips: LAC D2 and D12-D18, PMG D11-D14, none in LSM.
- Exceptions: PMG [007] and [012] are camera-only Transitions inside Steps 2 and 3. From LAC Step 9 and for most of LSM every camera is new. Framing inherited from the build cuts loose electronics at the frame edge in PMG [009]-[011], [017]-[018], [022]-[024], [032]-[034].
- Why it helps students: The removal is watched from the viewpoint in which the student saw the part go in, and the view never jumps during the motion.
- For our player: Camera is a per-step property of the instruct frame; the derivation copies it from the construction step, including the scene up-axis.

### DEC-19 · confirmed

**Keep the construction timing and naming: every frame 800 ms with fade for show/hide and tween for moves and camera; frames named `Start`, `Step N`, `Step Nc` (lower-case c), `Transition`, `Completed View`.**

- Applies to: all guides; checked here for the three take-apart guides
- Evidence: 800 ms on 258/260 frames. Numbering contiguous 1-24 (LSM), 1-23 (PMG), 1-47 (LAC, with two naming slips). Title-page subtitle reads 'Deconstruction' in 3/3.
- Exceptions: LAC [016] [017] are 1600 ms. Nut spin gets no double duration here (LSM [049] 800 ms) although the LSM build gives it 1600 ms. Project names are not uniform: 'Laser Stem Matrix (LSM) - Deconstruction', 'LAC Deconstruction', 'Piano Memory Game(PMG) Disassembly'.
- Why it helps students: Uniform pace and familiar step names across build and take-apart.
- For our player: One global default duration; a per-stage override exists but is rarely used.

### DEC-20 · qualified

**The recipe is sound as a starting point with these amendments: (3) copy the hover pose only where one exists, and treat arrow length = travel as a loose default; for two-stage joints choose between one generic arrow (LAC) and one arrow per stage (PMG); (4) the loose-wire stage is LAC only; (5) after an isolated view, drop what is left at the scene switch without a step, and choose wires-first or component-first per kit; (6) a paused pulled-out frame does occur 5 times and should be treated as a slip.**

- Applies to: auto-derivation of deconstruction from construction; synthesis of DEC-1 to DEC-18
- Evidence: See DEC-3 (65/94 fade-out; 54/54 arrows), DEC-5 (39/42 same direction, median ratio 1.00), DEC-15 (18 dropped, 19 merges), DEC-18 (26/55 cameras reused). What the recipe does not reproduce: LAC's regrouped order from Step 9, LSM's early side panels, PMG's bench phase (23 build steps -> 7).
- Exceptions: Open choices the data does not settle: three-beat vs compressed removal, wire granularity, which wire end first, how many eye icons, whether to re-fit stripped hardware.
- Narrowed because: See DEC-3 (5 paused pulled-out frames), DEC-5 (17/42 identical vectors; no build hover for PMG bench items), DEC-7 (length within 10 % of travel in 13/56), DEC-13 (residue vanishes at the switch), DEC-14 (PMG removes modules before wires).
- As first stated: Derive a take-apart from a construction guide like this: (1) frame 0 = the build's Start with the subtitle swapped; (2) walk the build steps last to first: skip preparation and handling/check steps, stop at the permanent first steps (their result is the `Completed View`), merge steps on the same part into one step with stages, merge 'one, then the rest' into one group; (3) rigid part: `Step N` = build step's camera, part seated, one red arrow along the hover-offset direction with length = hover distance (+ eye / the build's inset if there is a catch); then auto: hide cues, tween seated -> hover pose in 800 ms (stages reversed for two-stage joints); `Step Nc` = part faded out; (4) wire: eye on the plug, cross-fade routed -> loose at the build's staging pose, fade; captive leads dangle and stay; (5) wired module: cross-fade through the build's pose copies in reverse, leave it beside the model, unplug later; (6) never emit lead lines on a removal, hole labels, cards, a paused hover frame or a pile of removed parts; (7) end with the residue, no annotations.
- Why it helps students: Guarantees the take-apart shows each part leaving the way it arrived, with the same viewpoints and vocabulary as the build.
- For our player: Each construction step must carry: part ids, seated pose, hover offset(s) and stages, kind, camera + up-axis, optional detail inset, alternative wire/pose models. With that, a take-apart can be generated and then hand-tuned for order.

### DEC-ANOM · confirmed

**Do not copy the following authoring slips; they are anomalies, not conventions.**

- Applies to: deconstruction; per guide
- Evidence: 6/66 Transitions not hidden from the step picker; 2/66 not auto; 2/260 frames not 800 ms. Unused inherited annotations never shown: LSM 69 lead lines, 10 labels; LAC 41 labels, 43 lead lines; PMG 45 labels, 48 lead lines.
- Exceptions: Data caveat rather than guide fault: the digests' APPEAR / DISAPPEAR / MOVE lines are unreliable for these guides (parent `hidden` flags, absolute placements); all part-state numbers here come from reports/_work_dim_decon/walk.py.
- Why it helps students: Each one costs the student a dead click, a missing picture or a misleading cue.
- For our player: Validate authored guides: step names vs order, every auto frame flagged play + hidden, every removed part hidden by the result frame, every arrow followed by motion in its direction.

### Added by the re-check

- What is left in an isolated sub-assembly view is never removed by a step; it disappears at the next scene switch. A player deriving a take-apart must expect parts with no removal step. *Evidence:* 6 of 6 exits from an isolated view: LSM LED matrix module alone at [042], gone at [043]; LSM button panel alone at [053], gone at [054]; LAC potentiometer with re-fitted hardware at [048], gone at [049]; LAC panel F4 and rocker switch at [091], gone at [092]; PMG H2 and H3 at [046], gone at [047]. LAC panel F1 also vanishes without a step on Step 16's instruct frame [043]. The analyst recorded only PMG H2/H3, as an exception.
- Arrow count depends on group size: a pair of identical parts gets one arrow each; four or more identical parts share a single arrow. *Evidence:* Two arrows: LSM [016] [019] (lens supports 2 + 2), LSM [028] (two long matrix supports), LAC [074] (F7 pair). One arrow: LSM [001] 64 stems, PMG [028] 4 keys, PMG [053] 4 buttons, PMG [049] 5 wires. PMG [057] uses two arrows for two wire groups with different travel (36 and 75 mm).
- Whether a module or its wires come off first is decided per kit, not by a common rule. *Evidence:* LAC: wires then component in 4/4 (LCD Steps 19-22 then 23; buzzer 29-30 then 31; potentiometer leads 9-11 then 12-18; switch leads 32-34 then 35). PMG: module then wires in 3/3 (matrix Step 17 then its wires 18; buttons 20 and display 21 then all wires 22). LSM: board end of the matrix wires (11-13) then the connector at the module (15).
- A fully unplugged component leaves in one of two ways: eye plus plain fade with no motion (LSM, LAC) or an arrow and a short slide-while-fade (PMG). *Evidence:* Fade with eye, no motion: LSM Step 20 USB, LAC Step 23 LCD, LAC Step 31 buzzer. Slide with arrow: PMG Step 17 matrix 68 mm, Step 20 buttons 27 mm, Step 21 display 22 mm.
- Each take-apart guide is a copy of the full-build project with all steps re-authored: same CAD, same pose copies, the build's annotation library carried along unused, and almost every cue drawn new. *Evidence:* cadId identical decon vs full build in 3/3; annotation objects shared with the full build: LSM 94, LAC 144, PMG 133; shared step ids 0. Of the annotations actually shown, only 2 (LSM), 5 (LAC), 0 (PMG) come from the build (title, logo, LAC's two insets). This is why the build's hover vectors, staging poses and cameras can be bit-identical.
- Scene up-axis flips are inherited from the build step being undone so that the pull reads upward on screen; this holds in LAC and PMG, and LSM drops the build's flips. *Evidence:* LAC take-apart -x at Step 2 and Steps 12-18 matches build B56 and B22-29; PMG -y at Steps 11-14 matches build B29-36. LSM build flips at B23-26 and B34; the LSM take-apart is +y throughout.
- Tilt stages are stored as a rotation about an explicit pivot placed at the tab edge, with the position compensated; a player needs pivot rotation, not just translation, to replay them. *Evidence:* LAC F2 at [005]: rotation -21.4 deg about local z, origin (-0.4, 6.2, 61.3) mm, use_origin true, position shift 1.75 mm; PMG H10 at the step before [026]: 7.9 deg with origin (109.2, 3.3, -64.6). Neither the analyst's walk nor the digest reads origin/use_origin, so displacement figures for tilted parts (LAC F9 65 mm, PMG H6 43 mm, H5 56 mm first stage) are pivot compensation, not travel.
- The step-level 'fade' page transition is not part of the take-apart convention. *Evidence:* Used on 4 of 260 frames, all LSM ([001] [027] [037] [047]); only 1 of the 10 scene switches has it; LAC and PMG take-aparts never use it, although the LSM and LAC full builds use it 13 times each at scene switches and cards.
- Multi-stage steps chain several 0.8 s auto frames, so step duration scales with the number of stages; the 1.6 s / 0.8 s default describes single-stage removals only. *Evidence:* LAC Steps 2, 24, 28: two Transitions then c = 2.4 s. LAC Step 6 LCD flipbook 1.6 + 1.6 + 0.8 = 4.0 s. PMG Steps 2 and 3: three Transitions then c = 3.2 s, the last Transition being a camera-only move ([007] [012]).

### Numbers (as corrected by the re-check)

| Setting | Value | Basis |
|---|---|---|
| Frame / stage duration | 800 ms, fade for show/hide, tween for part and camera moves (confirmed) | 258 of 260 take-apart frames; LAC [016] [017] are 1600 ms pose swaps. Animation options identical on all shown frames. |
| Removal sequence length | Single-stage: 1.6 s three-beat (A) or 0.8 s compressed (B). Two-stage: 1.6 s in PMG, 2.4 s in LAC. Pose flipbooks 3.2-4.0 s. | A: LSM 17 + LAC 14 steps and 6/6 build removals. Pure 0.8 s B: 12 PMG steps only (5, 9, 10, 15-23). PMG two-stage Steps 1, 6, 7, 11, 13, 14 = 0.8 + 0.8; LAC Steps 2, 24, 28 = 3 x 0.8; LAC Step 6 = 1.6 + 1.6 + 0.8; PMG Steps 2, 3 = 4 x 0.8. |
| Removal travel (default) | Same axis as the build hover (about 93 %); equal to the build hover vector only in mirror-authored phases | 17 of 42 comparable part-moves bit-identical (LSM 5, LAC 4, PMG 8); others 0.31-1.52 x (median 1.00); no build hover exists for PMG H1, matrix, display, buttons, wire bundles and the LSM connector. |
| Removal travel, plug-in electronic part | Median 31 mm but bimodal: 26-31 mm in LSM and PMG, 51-55 mm in LAC (RTC 22) | n 9: LSM 29.1, 30.3, 31.0, 31.3; PMG 25.9; LAC 21.7, 50.7, 51.6, 55.0. |
| Removal travel, laser-cut wood part | About 68 mm (confirmed approximately), pull stage 33-143 mm | My list of 32 pull distances: median 67.7 mm; shortest LAC F9 33.0, longest PMG keys 142.5. |
| Unhook stage of a two-stage joint | 6.7-8.9 mm slide (3 steps) or 7-26 deg tilt (7 steps); second stage 33-139 mm (not 44-139) | 10 steps (PMG 7, LAC 3); LAC F9 second stage is 33.0 mm at [065]; PMG H14 tilt totals about 7 deg. |
| Arrow style | #ff0000, straight, head at end, body 5 / head width 20 / head length 17 (confirmed) | Colour and type 77/77; body 5 with head 20 in 71/77; head length 17 in 68/77, 15 in 6. Off-style: LSM [016] [028] x2 [056] [059], PMG [014]. |
| Arrow thickness on the model | Shaft about 4 mm in LSM and LAC, about 7 mm in PMG (range 1.3-11.8 mm); do not reuse the raw scale number across kits | body_width x scale x mm-per-unit, assuming scale multiplies the cross-section; mm per unit is LSM 2.09, LAC 1.65, PMG 23.6, which explains raw scale 0.12-0.75 against 0.025-0.10. |
| Arrow length | Median 53 mm (quartiles 40-69, range 16-116); length/travel median 0.95, quartiles 0.77-1.19, range 0.41-1.64 | 77 arrows; 56 arrow/travel pairs with travel of 20 mm or more; within 10 % in 13 pairs, within 25 % in 31; correlation 0.75. |
| Arrows per Step N | 1 per moving unit, 2 at most; a pair of identical parts gets 2, four or more identical parts get 1 | 1 arrow on 54 N frames, 2 on 7; pairs with two arrows LSM Steps 6, 7, 10 and LAC Step 28; single arrow for 64 stems, 4 keys, 4 buttons, 5 wires; 54/54 tween or slide removals have an arrow. |
| Arrow direction on screen | 40 up (within 30 deg), 19 sideways, 17 oblique (10 of them below horizontal), 1 down | Projection of 77 arrow vectors with each frame's camera and up-axis; analyst gave 41 / 30 / 5 / 1. World axis: 38 +Y, 28 horizontal, 5 -Y, 6 oblique. |
| Lead lines on a removal | 0 (confirmed) | 3 lines in 260 frames, all on LAC re-fit Steps 16-18; full builds 149. |
| Eye icon | Width 7.81 % of viewport (8.2 % in PMG), #7fdbff line leader ending in a dashed ring (confirmed) | 44/44 LSM+LAC, 4/4 PMG; 48 icons on 47 of 94 steps; 2 LSM eyes lack leader settings, 1 is boxed. |
| Detail inset | 7.8-9.9 % wide for one latch, 15-25 % for a panel face; #7fdbff rectangle frame, thickness 5, corner radius 0.1 (confirmed) | 10 insets (LSM 8, LAC 2), widths 7.81-9.92 and 15.02-24.84. |
| Text labels | 0; four LAC pin names in the project default font PublicSansMedium (not Arial), bold 3em black, #7fdbff underline thickness 5 with shadow | 4 labels in 260 frames (LAC Steps 19-22); label HTML has no font-family and the font table lists PublicSansMedium only; the 41 unused inherited labels are the Arial ones. |
| Transition attributes | play, hidden from step picker, navigation overlay hidden, camera unchanged (confirmed) | 64 / 60 / 61 / 64 of 66. |
| Share of auto-advancing frames | 24.6 % in take-apart guides against 7.1 % in the full builds (6.6 % over all 16 construction guides); 0.70 against 0.16 Transitions per numbered step (confirmed) | 64/260, 24/336, 51/775; 66/94, 24/146. |
| What Transitions do in a take-apart | 62 % part motion, 32 % cross-fade, 3 % camera-only, 3 % empty (confirmed) | 41 / 21 / 2 / 2 of 66 (LSM 17/1/0/1, LAC 17/15/0/1, PMG 7/5/2/0). |
| Take-apart steps per build step | 0.64 (LSM 0.63, LAC 0.82, PMG 0.45) (confirmed) | 94/146; 18 build steps dropped; mapping rebuilt independently. |
| Reverse-order fidelity | 76 % of consecutive steps, 86 % of all step pairs (confirmed) | 68/89 and 1305/1519; per kit 84 %, 83 %, 98 %. |
| Removed part hidden on the result frame | 69 % of steps (confirmed) | 65/94; rest = 22 re-posed, 3 kept in view, 3 re-fits, 1 slip. |
| Instruct frames that change geometry | 25 of 95 (19 if sub-part solid flickers are ignored) | 10 scene switches, 3 re-fit hover-ins, 6 visibility slips, plus LSM [004] [028] [051] [056] [065], LAC [015], and the PMG [001] nudge. |
| Camera moves | 55 of 95 instruct frames (58 %), 0 of 93 result frames, plus 2 of 66 Transitions and 2 of 3 Completed Views; 47 % of instruct-frame poses copied from the build | PMG [007] [012]; LSM and LAC end frames; 26/55 bit-identical. |
| Closest camera distance | 162 mm (LSM), 237 mm (LAC, at the Completed View; 277 inside steps), 173 mm (PMG); builds 42-110 mm (confirmed) | Minimum distance per guide: 162.3 / 237.5 / 173.1 against 42.2 / 110.0 / 43.3. |
| Loose-wire parking pose (LAC) | 159-184 mm to the side for one auto frame; equal to the build's staging pose in 10 of 12, not 12 | Steps 19-22 and 36-41 identical to 0.1 mm; Step 42 is 15 mm further out; Step 43 uses a borrowed model at a new pose. |
| Grouped identical-part steps | 9, not 7 | LSM 1, 6, 7, 10; LAC 26, 28; PMG 9, 12, 20. |
| Title page | Logo at about (2-5 %, 5-8 %) width 36-39 %; title block at about (2-4 %, 61-64 %) width 42-46 %; build's Start camera (confirmed) | 3 Start frames; camera identical to the build's Start in LSM and LAC, not PMG. |

### Open questions

- NOTE FOR THE ORCHESTRATOR: the narrative file reports/dim_deconstruction.md was NOT written. The Write tool rejected it ('Subagents should return findings as text, not write report files') and I did not work around that with another tool. All findings are in this structured result; the tables and scripts behind every number are in reports/_work_dim_decon/ (tbl_steps.md = every take-apart step with cue, removal mode, motion, build step undone and camera; tbl_hover.md; tbl_arrows.md; a1..a10 *.out logs; out_*.json; walk.py = corrected state walk for all 20 guides; img/pairs1.jpg and img/ends.jpg = build vs take-apart comparison sheets). If a report file is required, the harness rule needs lifting or the orchestrator should assemble it from this result.
- Three-beat or compressed removal? LSM and LAC (and every removal inside the construction guides) use Step N -> auto Transition (tween out) -> Step Nc (fade); the newest guide, PMG (2026-08), writes the displacement and the hide into Step Nc so the part slides while fading. Which does TechBox want as house style? I could not watch the live viewer, so the look of the compressed form is inferred from animation settings.
- Wire granularity when unplugging: one wire per step (LAC, 20/20), one plug or one shared connector per step (LSM), or whole bundles (PMG, 21 wires in 2 steps)? Is the PMG bundle form the intended simplification going forward or specific to that kit's shield?
- Which end of a wire comes off first? LSM: board end, then module end. PMG: module end, then shield end. LAC: both ends in one step. No rule can be extracted.
- How many eye icons and insets are wanted? LSM uses an eye on 16 of 24 steps and 8 latch insets; PMG uses 4 eyes on 23 steps and no insets although its housing has the same tab joints.
- Should a take-apart restore bought-in sub-assemblies to their as-supplied state? LAC re-fits washer, nut and knob on the potentiometer (Steps 16-18); LSM does not put the nut back on the push button.
- Where exactly should a take-apart stop? LSM and LAC stop at the breadboard stuck to the base (adhesive). PMG stops at the bare shield but never shows side panels H2 and H3 being removed - is that an omission or are the last two panels meant to be implied?
- Is the reordering in LSM (two side panels pulled off before the lens supports) and in LAC from Step 9 (component groups) deliberate pedagogy or just authoring convenience? An auto-derived guide in strict reverse order would differ from both.
- For two-stage joints, should the second-stage arrow be shown at all? PMG shows it only on an auto frame (about 0.8 s); LAC shows one arrow for the whole move; on PMG Steps 2 and 3 the only arrow is on an auto frame.
- Should threaded parts spin and take double time when removed? The LSM build gives the nut 1600 ms with rotation; in the take-apart guides the LSM nut spins in 800 ms and the LAC nut does not spin.
- Should the take-apart reuse the build camera for every step? It does in the mirror-authored phases (26 of 55 poses) but most LSM steps and all LAC steps from 9 on use fresh cameras.

## Gap check

A final pass looked for what an author would still have to guess at, and checked each gap against the data.

- **Screws, threaded fasteners and tools.** No screw, bolt, standoff or tool exists in any of the 20 inventories. All fastener evidence is 8 operations: LSM nut off/on (Steps 16, 18; [034], [039]) and LAC knob, nut, washer off (Steps 22-24; [046], [052]) and on in reverse (Steps 26-28; [057], [059], [061]); each is its own numbered step in an isolated view with one red arrow (off) or one axial lead line (on). Thread spin is a token and inconsistent: LAC nut 176 deg while sliding off [050] and none when refitted; LSM nut 180 deg off [035], 115 deg on [040]. No tool, size or tightness cue is ever shown; fasteners have no tooltip name (LAC vocabulary of 21 names has none for nut, washer, knob). *Why it matters:* The Mini Robot Arm is held together with screws; the rulebook's fastener rules would be applied to dozens of them.
- **Fastener rule versus batching rule.** Own-step holds 8 of 8 for hardware, batching holds for 3 of 4 identical sets of four or more (64 stems, 4 keys, 4 button modules; not the 4 posts). No guide has identical fasteners, so the data cannot choose. Needs a house decision before authoring. *Why it matters:* Four identical screws on one servo satisfy both 'every fastener gets its own step' and 'four or more identical parts: one exemplar, then do the rest'.
- **Servos and other panel-mounted parts with a captive lead; servo horn position.** Nearest evidence is the push button (LSM), rocker switch, potentiometer and buzzer (LAC): mounted on a loose panel in an isolated view, component moves, panel fades in seated (5 of 5), leads ride rigidly. Setting a rotary position has one precedent, LAC Step 29 ([063] to [064]): face-on view, eye icon on the knob, knob turns 50 deg in place on Step 29c. The 'all wiring before any wall' order would leave every servo panel tethered through the mechanical build; in LAC the switch panel stays tethered 34 steps and the pot panel 29, needing 3 and 4 pre-posed copies (F4-2/-3/-1, F1-3/-4/-2/-1). No guide wires after the mechanical build. *Why it matters:* Servos are the core of the kit and have no direct precedent.
- **Multi-pin plug on a lead, and polarity.** No lead in any guide ends in a multi-pin housing; captive leads end in single-pin housings and get one step each with an eye on the housing and one label (8 of 8). Polarity has one precedent, the LSM capacitor: card with a photo marking 'GND Strip', minus and plus [012], then an eye on the stripe beside two hole labels and two lead lines on Step 6 [013]. A rigid cable plug has two treatments: eye on the socket then the plugged cable fades in (LSM, LAC [088]) or the plug hovers with one red lead line and tweens 22.9 mm (PMG [057]). *Why it matters:* A servo plug is one 3-pin housing whose orientation is given only by wire colour; the rulebook says colour never carries function.
- **A finished sub-assembly moved as a unit.** Tween scan of the three full builds: the only different items that ever move together are a bought-in component with its own leads or battery, and identical pairs. No student-built sub-assembly is tweened. Bench sub-assemblies are staged where they will lie parked: positions are bit-identical from first bench frame to pick-up (LAC F1 [055] to [104], LAC F4 [032] to [065], LSM D2 [037] to [046]), so returning to the full scene needs no motion and no step. Once wired they are seated by cross-fade: 11 seat events, 7 in two numbered steps (re-pose with an eye, then attach), 4 in one (LSM D2 with an arrow [046], LAC buzzer with two eyes [094], PMG button modules [073], [075]); attach cue is lead lines 6, arrow 2, eyes only 3. An untethered multi-part sub-assembly has no precedent. *Why it matters:* Robot-arm sections are built on the bench and then joined; the author needs to know whether to tween, cross-fade or cut.
- **First-step conventions.** 5 of 19 guides open with a section card straight after Start (LAC Part 2, LAC Part 3, PMG Part 1, PMG Part 2, PMG Full Build). LSM and LAC Step 1 is a preparation step on the first part alone (peel the breadboard backing: red arrow plus an inset captioned 'Protective Backing', [001] in both); Step 2 hovers the breadboard over the base, which fades in seated. PMG Step 1 seats the Nano on the I/O module with 4 lead lines [002]. The base panel never gets a step. The cut from hero to first frame uses a step-level fade in 11 of 12 LSM/LAC build guides and 0 of 4 PMG build guides. Part guides start with earlier work already on screen: no recap, no parts list. *Why it matters:* The pattern set says what a guide contains but not how it opens.
- **Turning the work over.** 14 up-axis changes in the three full builds (LSM 5, LAC 7, PMG 2): 10 on a Step N, 1 on a card, 3 on an auto Transition (all LSM). None has a dedicated cue; the model simply appears the other way up with engraved IDs upside down (PMG [064] to [065]). Start and final view are always +y (19 of 19). *Why it matters:* A young student has to notice that the kit must be flipped.
- **Cues on frames that cannot be read.** 15 auto Transitions carry an annotation, all in PMG: 9 second-stage arrows in the take-apart and 3 lead-line pairs in the build, each published twice (Full Build [106], [111], [114] and Part 3). 423 of 425 Step N frames carry a cue; the 2 bare ones are the PMG 9-wire ribbon step (Full [035], Part 2 [002]). *Why it matters:* A cue shown only during an 0.8 s auto-advance is not an instruction.
- **Meaning of the eye icon.** Seen meaning: take this wire (PMG [007]), take this ribbon [004], look at this polarity mark (LSM [013]), turn this (LAC [063]), pick this up (PMG [099]), do the rest (LSM [085]), check this result (LSM [076]). Two eyes on one frame occur 4 times; twice they mean 'this goes there' for a wired module (LAC Step 43 [094], PMG Step 33 [073]), once 'release both' (LAC Step 44 [096]). The pair is not described in the pattern set. *Why it matters:* One glyph is the main wordless cue and the rulebook does not define what it tells the student to do.
- **Text and wording.** 52 step descriptions survive in the three oldest LSM guides in the form 'Step n - imperative sentence' with Title Case nouns, and 'Make Sure ...' on a result frame; they are stale and contain typos. Cadasio's placeholder description is still published on 3 visible steps (LSM Part 4 [000], LSM Part 3+4 [000], LAC Electronics [001]). Text-to-speech is off in 20 of 20. Pictures do contain words ('Protective Backing', 'GND Strip', 'GND', 'VCC', 'H9 3x', 'NANO I/O MODULE LABELS'). Label font is Arial on 133 showings and project default Public Sans on 88; size 3em on 175, 2.5em on 39. Part IDs use one letter per kit (D, F, H) with no stated scheme for the next. *Why it matters:* The rulebook says 'no text' but gives no wording template, no font and no part-ID scheme for when text is needed.
- **The last view.** Named 'Completed View' in 16 of 19, 'Completed Build' in 2, misspelt in 1. It changes only the camera in 14 of 19: PMG Part 1 [033] and PMG Deconstruction [060] have no last Step Nc, so the final view performs the last change (6 and 293 solids) with the camera unchanged, and three LSM guides switch on 4 extra solids. No annotation on any final view. Take-aparts end on what cannot be undone: breadboard stuck to the base (LSM [068], LAC [129]) or the bare I/O module (PMG [060]). *Why it matters:* The pattern set states it as one name and a camera-only step.
- **Title page details.** Logo 33-40 % of width at x 2 %, y 4-8 %; title block 42-58 % of width at x 2 %, y 61-65 % (19 of 19). Subtitles used: 'Part n', 'Part 1 + 2', 'Part 3 + 4', 'Full Build', 'Deconstruction'. Copyright year is baked into the image (2025 LSM and LAC, 2026 PMG). The hero is staged separately and differs from the final state: LAC Full Build hero shows the washer the final view lacks and omits bracket F9; PMG Full Build hero omits 6 solids of the USB cable. At 2.63:1 the title overlaps the model (PMG Deconstruction [000]). *Why it matters:* Layout is specified but not content, state of the hero or behaviour at other frame shapes.
- **Identical repeated parts and the quantity cue.** Sets found: pairs (4 steps), 4 posts (split 2 + 2), 4 keys (1 + 3), 4 button modules (1 + 3 by cross-fade), 64 stems (1 + 63); no set of 3. The quantity cue has three forms: '2x' in blue #0074d9 (LAC [008]), '64x' or '64X' in cyan on a card (LSM [082]), '3x' inside a picture (PMG [085]). Identical modules are wired in full every time (4 PMG button modules, 12 wire steps). *Why it matters:* Arm kits repeat brackets, servos and screws.
- **Showing what is hard to see.** Used: camera re-aim, up-axis flip, eye on the spot, framed close-up (21 result frames carry one new check cue), 50 % ghosting once (LSM Step 34 [075], 5 solids). Never used: section cut (21 stored settings, 0 enabled), exploded view, hiding a built part to expose what is behind it (wood parts leave the screen only at scene switches or pose swaps). *Why it matters:* The pattern set lists devices but not which to choose.
- **Accessibility for young students.** Contrast: cyan callout furniture on white 1.56:1, red on white 4.0:1, red on wood 2.15:1, cyan over wood 1.19:1, red on the blue shield 1.86:1. Sizing mixes three units (labels and line widths in fixed pixels, images in percent of width, arrows in model mm); at the projects' own 560 x 315 embed a 175 px label box is 31 % of the width. Which jumper to pick is conveyed by colour alone, and loose and routed models differ in colour on 5 of 103 pairs. Next presses: 81, 120, 108 for the full builds, 11-53 per part guide. Part names need a hover. No warning symbol, adult-help cue or test step anywhere. *Why it matters:* The in-house player is for classrooms and the pattern set has no rule on contrast, size, colour reliance or input.
- **Power and testing.** USB is plugged in at Step 20 of 38 (LSM), 40 of 57 (LAC), 25 of 51 (PMG) and stays attached for the rest of the build. No take-apart unplugs it first: it comes off at Step 20 of 24, 25 of 47 and 19 of 23. No guide has a power-on, upload or function-check step. *Why it matters:* A servo arm needs powering, centring and a safe take-apart order.
- **Continuity of pose copies.** LAC: the washer fitted in Step 26 disappears at Step 30 [065] and never returns; the nut is absent from the copies shown from Step 47c to Step 54 ([105] to [121]). No rule in the set requires copies to hold the same parts. *Why it matters:* Cross-fading copies is the house method for wired sub-assemblies, so a part missing from a copy vanishes on screen.
- **Player settings and data caveats.** Identical in 20 of 20: view cube shown, auto start, navigation overlay along the bottom, backward steps animated, interaction prompt off, tooltips on, embed 560 x 315. startStepId points at a mid-guide step in 3 guides (LSM Deconstruction 'Step 3', LSM Part 2 'Step 10', LSM Part 1+2 'Step 11') and is null in 9, so it cannot be trusted. Camera animation is stored as animate_orbit false on 1105 of 1105 steps; the path taken on a 90 degree re-aim is not determinable from the data. *Why it matters:* The player has to reproduce viewer behaviour that the rulebook does not list.

### Contradictions between topics, and which side is right

- Structure verifier (visibility from leaf-level flags, leaf starts hidden under a CAD-hidden ancestor) vs Style verifier (nearest explicit visible flag wins) **Resolution:** The two rules give the same picture in 16 guides and differ on 17 frames in 3 (LAC Part 2 [000], LAC Part 3 [000], PMG Deconstruction [000]-[014]). The LAC Part 2 title render shows panel F4 with the rocker switch, which only the leaf-flag rule shows. Leaf-level flags is right.
- GRAN-4 (sets of 4, 4 and 64 are batched; no set of 3) vs MECH-3 (3 keys, 63 stems) vs MOT-14 (sets of 2-4 are tweened in full, in pairs) **Resolution:** GRAN-4 is right on sizes: 64 stems, 4 keys, 4 button modules; MECH-3 quotes the remainders. MOT-14 is wrong for sets of 4: the 4 keys are batched (PMG [083]-[086]) and only the 4 posts go 2 + 2. A set of 4 goes either way; the divider is whether each part needs its own lead lines and viewpoint.
- STR-4, CAM-1, DEC-4, DEC-18 (camera never moves inside a pair) stated as absolutes **Resolution:** Step Nc holds 424 of 424. Transitions inside a pair hold 98 of 100: PMG Deconstruction [007] and [012] re-aim by 96 and 83 degrees before Step 2c and 3c. Keep the rule; treat the two as slips.
- STR-3 (every cue on a paused frame for one frame, result frame clean) vs LL-1, LL-8, DEC-2, DEC-7 (PMG puts second-stage lines and arrows on auto Transitions) **Resolution:** STR-3 is the rule by count: 15 Transition frames carry cues, all PMG, each visible 0.8 s. On result frames 26 of 424 carry something: 21 new check cues (allowed), 2 carried '2x' labels (LAC Step 4c), 2 carried lead-line pairs (PMG Step 51c [115], Part 3 Step 26c [057]), 1 misnamed frame. Do not adopt Transition cues; give a second stage its own numbered step.
- MOT-9 (never animate a wire into its connection) vs WIRE-15 (PMG USB plug hovers and tweens in with a lead line) **Resolution:** Both hold for different things: jumpers and captive leads are swapped on 103 of 103 pairs; a moulded plug was tweened once (PMG Step 25 [057]) and faded in seated in LSM and LAC. MOT-9 should say 'jumper wire or lead'; a rigid plug may be treated as a part.
- MECH-7 (do not rotate the model) vs Motion note and CAM-16 (turn the model over) **Resolution:** MECH-7 is right about mechanism: 39 up-axis changes and no part transform. On screen the model is the other way up, so the student must turn the kit; the wording 'turn the model over' describes the effect only.
- STYLE-7 (ghosting viewed from underneath) vs CAM-16 (never put the camera below the horizon) **Resolution:** CAM-16 is right: LSM Step 34 [075] has up-axis -y, so it is a flipped model seen from above.
- STYLE-11 (one label style, bold sans 3em) vs WIRE-6 and DEC-11 (Arial in LSM and LAC builds, project default in PMG and LAC Deconstruction; 2.5em in LSM) **Resolution:** WIRE-6 is right: Arial on 133 showings, default Public Sans on 88; 3em on 175, 2.5em on 39. There is no single house font; the newest kit uses the default at 3em.
- STR-1 and STR-14 (one final view named 'Completed View' that changes only the camera) vs the data **Resolution:** Name holds in 16 of 19, camera-only in 14 of 19 (PMG Part 1 and PMG Deconstruction lack the last Step Nc; three LSM guides add 4 solids). Keep the rule as the target.
- GRAN-8 and MECH-5 (every fastener its own step) vs GRAN-4 (batch four or more identical parts) **Resolution:** Undecided by the data: no guide has identical fasteners. Needs a house decision for screws.
- GRAN-10 (6-7 of 10) vs MECH-6 (7 of 13) vs LL-1 and LL-9 (11 cross-faded seats) **Resolution:** Recount gives 11 seat events, 7 in two numbered steps and 4 in one. The other denominators include carry steps (LAC Step 47, LSM Step 23) or drop one seat.
- MECH-1 (28 wood kinds) vs MECH-4 and MECH-8 (34 wood kinds) **Resolution:** 34 kinds exist; 6 never tween in because they fade in seated as datum or receiver (D1, D2, F1, F3, F4, H1). MECH-4 should read 13 of the 28 tweened kinds.
- WIRE-12 (every module whose pin names appear on labels gets a card) vs STR-12 (the Nano never gets a card) **Resolution:** STR-12 is right; LSM Step 3 carries the label 'Pin d12', a Nano pin name, so WIRE-12 has one exception and applies to wiring labels only.
- NEV-1 and LBL-2 (no words on the canvas) vs words inside pictures **Resolution:** True for labels only. Pictures carry 'Protective Backing' (LSM and LAC [001]), 'GND Strip', 'GND', 'VCC' (LSM [012]) and 'H9 3x' (PMG [085]).
- ORD-3, WIRE-10, LIB-WIRES (colour never means function) vs the LSM Capacitor card **Resolution:** True for jumpers only: the card uses red plus and black minus [012]. A servo lead would be a second case.
- Rule IDs DEC-1 to DEC-3 used twice (granularity section and deconstruction section) with different content **Resolution:** An ID collision, not a data conflict. Rename one family before the rulebook is cited.

### The rules the gap check ranked highest

1. Skeleton: Start, optional section cards, numbered pairs, Completed View. Step N shows the cue and waits; Step Nc shows the result from the same camera and waits. Number 1..N per guide with no gaps.
2. One kit item per numbered step. An identical pair may share a step. Batch only label-free drop-in parts in sets of four or more, after one worked example.
3. Every Step N carries at least one cue, on a paused frame, for one frame only. Step Nc is clean except one optional check picture or eye. No cues on auto Transitions.
4. Cue grammar: thin red lead lines for a part going on (1, 2 or 4, tab to slot, along the travel); one red arrow for a part coming off, flexed or carried; never both on a frame. Eye icon for wires, pick-ups and checks.
5. A rigid part fades in stationary at its hover pose, in final orientation, back along its insertion path and above or beside its seat on screen. It seats with one straight 800 ms move. No rotation except swing, lean, thread spin or a dial.
6. A second motion of the same part is its own numbered step with fresh lead lines, or an auto Transition with no new cue. The camera never moves inside a step.
7. Never tween anything whose wires are already plugged in. Cross-fade between pre-posed copies: re-pose with an eye, then attach with lead lines. Every copy must hold the same parts.
8. Build a bench sub-assembly in an isolated view at the pose where it will lie parked, so returning to the full scene needs no motion and no step.
9. One wire per step, shown as a model swap from a straight loose wire to the routed wire. Eye on the wire, one label per end, two labels at most, no lines or arrows. Park the loose wire at one spot per run.
10. Label text is only the identifier printed on the hardware. Part names live in tooltips ('Role - Part ID') and in IDs engraved on the wood, numbered in build order.
11. Preparation and fastener work get their own numbered steps in an isolated view, directly before first use. Do not zoom in on a small part while the assembly is on screen.
12. Put an un-numbered section card before the first use of any component with pins, polarity or a count to identify: the component alone, at most one eye and one framed photo with a red box.
13. Set the camera only on Start, cards, Step N and the final view. Use a three-quarter view from above (about 34 degrees), a 45 degree lens, the travel at least 40 degrees off the line of sight, and both the hovering part and its destination in frame.
14. Hold one camera through a wiring run; re-aim for most mechanical steps so the travel runs across the screen.
15. Order: electronics first on the open base, one module at a time, pins in physical order, USB last. Panel-mounted parts go on their loose panel first. Enclosure by dependency, cover last.
16. For underside or side work re-declare the up-axis and keep viewing from above. Group that work in one block and return to +y before the final view.
17. Look: white background, flat two-tone toon shading, thin black edges, no shadows. Wood #deb887 with engraved IDs #1e1616. Never tint or highlight a part; ghost at 50 % only to check something covered.
18. Annotation colours: red #ff0000 for motion, cyan #7fdbff for pointing furniture, black for text and the eye. Labels are bold sans text over a cyan rule with a straight leader to a dashed ring.
19. Animate every step change in 800 ms: fade for show and hide, tween for part moves and camera, backward navigation too. Hide auto Transitions from the step picker.
20. Title page: logo top-left, three-line title block bottom-left, finished model on the right, nothing else. Final view: clean three-quarter hero with no annotations.
21. Part guides are contiguous slices of the full build cut at pair boundaries, renumbered from 1, 5 to 26 steps each, each with its own Start and final view.
22. Take-apart: same skeleton without cards. Red arrow on the still-seated part on Step N, the removal plays through, the part is gone on Step Nc. Reverse order by access, coarser than the build, stop at what cannot be undone.
23. Confirm a hidden or tiny result with a framed close-up carrying a red box on Step Nc.
24. Decide before authoring, because the 20 guides are silent: screws and tools, servo order and plug orientation, a turn-over cue, a second cue for wire identity, minimum contrast and annotation size.
