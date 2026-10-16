# Dimension report: Guide structure, step naming and numbering

Scope: all 20 published TechBox Cadasio guides (LSM x8, LAC x7, PMG x5), 1037 viewer steps (1105 authored, 68 hidden).

## 0. Method and data caveats

- Step names, behaviour, duration, camera change, annotation counts and descriptions come from `digest/*.json`. `hideInStepPicker`, `overlayVisible`, step-level `transition`, animation option blocks, project flags, creation dates and title-image geometry come from `cadasio_raw/*.json` (the digest does not carry them).
- Part changes (appear / swap / move) were re-derived with a leaf-level walk of the raw payload because several per-guide readers showed the digest under-reports parts whose parent node is flagged hidden. Counts of "what changes on a step" (Table 8, Table 4) use that walk; they are classification-grade (did anything move / swap), not millimetre-grade.
- Every step was classified by name: `Start`; `Step <n>` (called **Step N** below); `Step <n>c` or `Step <n>C` (**Step Nc**); `Transition` including the four misspellings; `Completed View` / `Completed Build` / `Copmleted View` (**final**); anything else is a **named card**.
- Counting note: part guides are slices of the full builds, so "all 20 guides" counts the same authored step up to three times. Where it matters I also give the figure for the six independent master projects (the three full builds and the three deconstructions: 596 viewer steps).
- Renders inspected for this report (Read tool): title pages of LSM Part 1, LSM Full, LSM Part 1+2, LSM Part 3, LAC Part 2, LAC Deconstruction, PMG Part 1, PMG Deconstruction, plus a cropped montage of all 19 title blocks; contact sheets LAC Full [000]-[007] and [128]-[130], PMG Part 1 [000]-[007] and [032]-[033], LSM Part 4 [016]-[023], PMG Deconstruction [000]-[007], LSM Full [056]-[063], PMG Full [056]-[063], LAC Electronics [000]-[001].
- Scripts and intermediate outputs are in `reports/_work_dim_structure/`.

## 1. The patterns

Each pattern is stated as a rule, then what is always true, what is usually true, and the exceptions.

### STR-1. One fixed skeleton: Start, then cards / step pairs / transitions, then one final view

Rule: open every guide with a single title step named `Start`, close it with a single final view named `Completed View`, and put only three things in between: named cards, numbered step pairs (`Step N` ... `Step Nc`), and auto-advancing `Transition` steps.

- Always: 19 of 19 guides that have a title page begin with `Start` and end with a final-view step; there is exactly one of each per guide, including full builds and combined guides (Table 1).
- Grammar check: the kind sequence matches `Start (card | Transition | Step N Transition* Step Nc)* Final` exactly in 16 of 20 guides. The three build/deconstruction guides that fail do so because of naming slips or a missing last `Step Nc`, not because of a different structure: LAC Deconstruction (duplicate `Step 41` [104], `Step 45c` used for the Step 45 frame [120]), PMG Part 1 (no `Step 14c`, `Completed View` [033] does that job), PMG Deconstruction (no `Step 23c`, `Completed View` [060] does that job). The fourth is LAC Electronics, which is not a build guide (STR-18).
- Final step name: `Completed View` in 16 of 19; `Completed Build` in LSM Part 2 [030] and LSM Part 1+2 [046] (same lineage, the oldest project); `Copmleted View` in LSM Part 3+4 [042] (typo).
- Volume: a part guide has 5 to 26 numbered steps (median 13) and 13 to 59 viewer steps (median 31); a full build 38 / 57 / 51 numbered steps and 88 / 131 / 117 viewer steps; a deconstruction 24 / 47 / 23 numbered steps and 69 / 130 / 61 viewer steps. Viewer steps per numbered step: 2.24 to 2.62 in build guides, 2.65 to 2.88 in deconstructions (Table 3).

### STR-2. Every numbered step is a pair: `Step N` (instruction) then `Step Nc` (result)

Rule: author each student action as two frames that both wait for the student. `Step N` shows what is about to happen; `Step Nc` ("c" = completed, lower case, no space) shows the same scene after it has happened.

- 421 of 425 `Step N` frames are followed, after 0 to 3 Transitions, by the `Step Nc` with the same number. 334 pairs are adjacent, 76 have one Transition between, 9 have two, 2 have three.
- The 4 misses are all naming faults: LSM Part 4 [016] `Step 8` is completed by [017] `Step 9c`; LAC Deconstruction [104] `Step 41` is a dead duplicate of [105] `Step 40`; PMG Part 1 [032] `Step 14` and PMG Deconstruction [059] `Step 23` run straight into `Completed View`.
- What `Step N` shows, build guides (331 frames, Table 8): a new part fades in (173, usually at a hover pose), a scene swap or pose swap (34), a part moves, often together with a scene swap (40), parts only fade out (2), or nothing changes in the model at all and only annotations appear (82, 25 %). So a quarter of build `Step N` frames are pure cue frames ("pick this up", "push here").
- What `Step Nc` shows, build guides (330 frames): the model always changes, 0 of 330 are static. 154 are tweened moves to the seat, 156 are cross-fade swaps (wires, re-posed wired modules, bent leads), 20 are a plain appear or disappear.
- Deconstruction guides invert the content but keep the pair: `Step N` leaves the model untouched and adds the cue in 67 of 94 frames (71 %); `Step Nc` removes or swaps the part in 93 of 94 (63 fade-outs, 22 swaps, 8 moves).
- Suffix case: lower-case `c` in 422 of 424; capital `C` twice (LSM Part 1+2 [042] `Step 20C`, LAC Part 1 [030] `Step 14C`) - anomalies.

### STR-3. Annotations belong to one frame; `Step N` always has one, `Step Nc` is clean

Rule: switch every annotation on in exactly one viewer step and off on the next. Put at least one annotation on every `Step N`. Leave `Step Nc` clean, except for an optional single "check your work" callout that is itself new on that frame.

- Lifetime: across all guides there are 1019 annotation showings; 1012 (99.3 %) last exactly one viewer step. The 7 that last two are all faults: the `2x` label that survives into Step 4c (LAC Part 1 [009], LAC Full [009]), four lead lines left on at PMG Part 3 [057] / PMG Full [115] (`Step 26c` / `Step 51c`), and one eye icon across the duplicated LAC Deconstruction frames [104]-[105].
- `Step N` annotated: 423 of 425. The two without are one authored step seen twice: the 9-wire ribbon prep, PMG Part 2 [002] = PMG Full [035].
- `Step Nc` clean: 398 of 424 (94 %). Of the 26 that carry something, 21 carry one new check callout (an inset close-up or an eye icon that was not on `Step N`): LSM 9 showings, LAC 8, PMG 4; in the three full builds that is 9 of 146 `Step Nc` (LSM 23c, 30c, 34c; LAC 25c, 45c, 48c, 56c; PMG 33c, 38c). The other 5 are the faults listed above plus the misnamed LAC Deconstruction [120].
- Transitions carry annotations in 15 of 117 cases, all in PMG: the lead lines for the second leg of a two-leg seat (PMG Part 3 [048] [053] [056] = PMG Full [106] [111] [114]) and the second-stage arrow in PMG Deconstruction (9 of its 14 Transitions). In LSM and LAC, 0 of 87 Transitions carry an annotation.
- Start: exactly two annotations (logo image, title image), 19 of 19. Final view: zero annotations, 19 of 19.

### STR-4. The camera is set on entering a step group and then locked

Rule: change the camera only when entering `Start`, a card, a `Step N` or the final view. Never move it on `Step Nc`, and do not move it on a Transition that sits inside a pair, so the student sees the result from exactly the view in which the instruction was given.

- `Step Nc`: camera moves on 0 of 424. Always true.
- Transitions inside a pair: camera moves on 2 of 101 (PMG Deconstruction [007] and [012], which swing 96 and 83 degrees to show a dismounted module before `Step 2c` / `Step 3c`).
- So the view is constant from `Step N` to `Step Nc` in 423 of 425 numbered steps.
- `Step N`: camera moves on 266 of 425 (63 %; build guides 211 of 331, deconstructions 55 of 94). When it moves, the median rotation is 62.5 degrees in build guides and 55.7 in deconstructions. It stays put when work continues in the same place.
- Cards: 31 of 33 move the camera (the two that do not are the 2D-only `LED Matrix Diagram` card in LSM Part 2 [009] and Part 1+2 [025]). Start: 19 of 19. Final: 17 of 19.

### STR-5. Numbering starts at 1 in every guide, has no gaps, and counts only student actions

Rule: number steps 1..N per published guide. Give a number to every student action, including preparation and check actions; give no number to Start, cards, Transitions or the final view. In a full build keep one continuous run; in a part guide restart at 1.

- First numbered step is `Step 1` in 19 of 19 guides; the run is contiguous 1..N in 17 of 19. The two breaks are naming faults (LSM Part 4 skips from 8 to 9c, so it shows 1..13 for 12 real steps; LAC Deconstruction has the duplicate 41 and the missing 45).
- Restart per part: all 11 part guides and both LSM combined guides start at 1.
- Continuous in full builds: LSM 1..38, LAC 1..57, PMG 1..51; numbers run straight through cards and through the places where one part ends and the next begins.
- Offsets (verified by aligning step sequences): LAC Part 2 = +14, Part 3 = +32, Part 4 = +40. PMG Part 2 = +14, Part 3 = +25. LSM Part 2 = +8 (its Steps 12 and 13 swap places and become 21 and 20), Part 3 = +21, Part 4 = +26 (with the 8/9c slip repaired to 34/34c and +25 after it). The offset is always the number of numbered steps in the preceding parts.
- The project setting `stepPrefix` is "Step" in 20 of 20; step names are typed by hand on top of Cadasio's project-wide counter (which has reached 363 in LAC Deconstruction), which is why every numbering fault in the corpus is a typing fault.

### STR-6. Everything waits for the student except Transitions

Rule: give `Start`, cards, `Step N`, `Step Nc` and the final view behaviour `pause`. Give `Transition` behaviour `play` so that one press of Next carries the student from `Step N` through the Transition(s) to `Step Nc`.

- Non-Transition steps: pause on 920 of 920. Always true.
- Transitions: play on 115 of 117. The two pause Transitions are LAC Deconstruction [033] (changes nothing) and [118] (the RTC lift needs an extra click); both are faults.
- No step uses a popup, checklist or button (0 of 1037); `nextStep` / `previousStep` are the defaults on 1037 of 1037; `animationChained` is false on 1037 of 1037.
- Share of auto-advancing frames: 0 to 14 % in build guides (LAC Part 4 is the highest at 6 of 42), 23 to 28 % in deconstructions.

### STR-7. Transition use A (86 % of all Transitions): an extra keyframe inside one numbered step

Rule: when one student action needs more than two keyframes, insert auto-advancing `Transition` frames between `Step N` and `Step Nc`. Do not give the intermediate state its own number.

101 of 117 Transitions sit inside a pair (Table 4). They do three jobs:

1. Removal beat (arrow on `Step N`, part slides off in the Transition, part fades out on `Step Nc`). In build guides: peeling the breadboard backing (LSM Full [002], LAC Full [002]), unscrewing a nut (LSM Full [035]), stripping knob / nut / washer (LAC Full [047] [050] [053]). In deconstructions this is the standard beat: 56 of 94 numbered steps have at least one Transition (LSM 19 of 24, LAC 27 of 47, PMG 10 of 23).
2. Middle leg of a multi-leg seat: LSM D10 clip ([065]), LAC F9 ([099] [100]) and F2 ([126]), PMG H11 / H12 / H14 ([092] [095] [114]).
3. Flip-book frame for a wired module that is cross-faded through intermediate poses: LAC LCD ([116] [117]), PMG display and matrix ([106] [111]), and 15 wire or module swaps in LAC Deconstruction.

- By content: 68 part moves, 27 model swaps, 4 that only clear the cues, 2 camera moves.
- In build guides only 31 of 331 numbered steps (9 %) contain a Transition (27 with one, 4 with two); in the three full builds 15 of 146.
- A numbered step never contains more than 3 Transitions (PMG Deconstruction Steps 2 and 3).

### STR-8. Transition use B (14 %): a bridge between two numbered steps

Rule: use a Transition between `Step Nc` and the next `Step N` only for something the student does not do and should not have to click for.

16 of 117 Transitions sit between pairs:

- 10 are camera-only re-orientations. 8 of them are in the LSM kit and every one coincides with a scene up-axis flip (LSM Part 3 [005]; Part 4 [018]; Part 3+4 [007] [014] [032]; Full [052] [059] [077]); rotations 53 to 143 degrees. The other 2 are one authored LAC step (LAC Part 4 [019] = LAC Full [108], 13 degrees).
- 6 are one authored PMG idiom seen twice: the next push-button module, which the student does not install at that point, fades in already in place before its first wire step (PMG Part 1 [013] [020] [027] = PMG Full [013] [020] [027]).
- This is a kit habit rather than a rule: LAC and PMG flip the up-axis 22 times directly on a `Step N` with no Transition, and the LSM kit itself does so 6 times. Of 39 up-axis changes in the corpus, 8 use a Transition.
- A Transition never follows `Start`, never precedes the final view, and never touches a card (cards are preceded by a `Step Nc` 26 times and by `Start` 5 times, and are followed by a `Step N` 31 of 31 times).
- README correction: Transitions are described there as camera steps. Only 12 of 117 move the camera.

### STR-9. Transitions are invisible as steps

Rule: hide every Transition from the step picker and hide the navigation overlay while it plays, so the student neither sees it as a step nor can stop on it.

- `hideInStepPicker` true on 108 of 117 Transitions and on 0 of 920 other steps.
- `overlayVisible` false on 110 of 117 Transitions and on 0 of 920 other steps.
- Exceptions (all look like oversights): visible in the picker - LSM Deconstruction [044] [052] [066], LAC Part 4 [028] (its twin LAC Full [117] is hidden), LAC Deconstruction [033] [118], PMG Part 3 [056] = PMG Full [114], PMG Deconstruction [026]. Overlay left on - LSM Deconstruction [044] [066], LAC Deconstruction [033] [118], PMG Part 3 [056] = PMG Full [114], PMG Deconstruction [026].
- Step name: `Transition` on 113; misspelt on 4 (`Transiton` LSM Deconstruction [038]; `Ttansition` LAC Part 2 [023] = LAC Full [053]; `Transititon` LAC Deconstruction [002]). Since the name is never shown, the typos are harmless, which is presumably why they survived.

### STR-10. One animation timing for the whole library

Rule: animate every step change over 800 ms; fade parts and annotations in and out; tween part moves and camera moves; do not orbit the camera. Double the duration only for a part that spins on a thread.

- Duration 800 ms on 1030 of 1037 viewer steps. The 7 at 1600 ms: nut unscrewing and screwing in the LSM kit (LSM Part 2 [017] [022], Part 1+2 [033] [038], Full [035]) and two LCD pose swaps in LAC Deconstruction ([016] [017]). The LSM Full build keeps 1600 ms for unscrewing but uses 800 ms for screwing on ([040]), so even this exception is not applied consistently.
- CAD animation options: show = fade, hide = fade, move = tween on 1037 of 1037.
- Camera animation options: move = tween, animate_orbit = false, animation_speed = 2 on 1037 of 1037 (stored as strings on most steps and as typed values on a few; same values).
- 2D annotation options: show = fade, hide = fade, move = tween, visibility animated separately on 1037 of 1037.
- Project flags identical in 20 of 20: autoStart true, animateStepsViewer true, animatePreviousStep true (stepping back is animated too), navigation overlay `horizontal_bottom`, overlay visible at start, tooltips on, interaction prompt off, repeatCount 0, chain false, no play-step timeout, perspective camera with 45 degree field of view.
- Timing consequence: one click on a `Step N` that has k Transitions plays (k + 1) x 800 ms of animation before the next pause (1.6 s for the common one-Transition case).

### STR-11. Step-level page transition: default `none`; `fade` is an optional LSM/LAC habit for scene swaps

Rule: leave the step-level transition at `none` and let the per-part fades do the work. If a whole-scene cut is wanted (assembly out, isolated part in), `fade` is the only alternative ever used.

- `fade` on 65 of 1037 steps: 44 `Step N`, 17 cards, 4 `Step Nc`; never on a Transition, Start or final view.
- 48 of the 65 are on steps that replace more than half of the visible model; but 80 other steps that also replace more than half of the model use `none`. So the setting is not applied systematically.
- By kit: LSM 36, LAC 29 (all in the build guides; LAC Deconstruction 0 of 130), PMG 0 of 298. The newest kit does not use it at all.

### STR-12. Named section cards introduce a component before its first use

Rule: before the first numbered step that uses a new bought-in component, insert one un-numbered step named after the component in Title Case. Show the component alone, close up, with at most two annotations. A card waits for the student, has no `c` twin, and asks for no action.

- 31 card steps in 13 guides (Table 5), which are 14 distinct cards: LSM `Capacitor`, `LED Matrix Diagram`, `Mini USB Cable`, `LED Stems`; LAC `Real Time Clock`, `Rocker Switch`, `Alarm Buzzer`, `LCD Screen`, `USB Cable`; PMG `Nano I/O Module`, `Push Buttons`, `4-Digit Display`, `Dot Matrix Display`, `USB Cable`.
- Position: followed by a `Step N` 31 of 31; preceded by a `Step Nc` (26) or by `Start` (5). Never inside a pair, never next to a Transition.
- Behaviour pause, 800 ms, visible in the picker: 31 of 31. Camera moves on entry on 29 of 31, and the following `Step N` moves it again on 30 of 31 (pull-back to the assembly).
- Content of the 14 distinct cards: 6 pair the 3D part with a framed photo or diagram of the real part (`Capacitor`, `LCD Screen`, `Nano I/O Module`, `Push Buttons`, `4-Digit Display`, `Dot Matrix Display`); 3 show the part with only an eye icon (`Mini USB Cable`, `Real Time Clock`, `Alarm Buzzer`); 3 show the part with nothing (`Rocker Switch`, both `USB Cable`); 1 shows the part with a quantity label (`LED Stems`, "64X"); 1 is a full-frame 2D diagram with no 3D part (`LED Matrix Diagram`).
- The card's name appears nowhere on the canvas (checked on PMG Part 1 [001] [006], LSM Part 4 [023]); it exists only as the step name shown by the viewer chrome.
- Where cards are not used: wooden panels (0 cards in LAC Steps 41-57 and PMG Steps 26-51), the three deconstruction guides (0 of 260 steps), and components whose first appearance is itself a numbered preparation step (resistors, jumper ribbons, potentiometer).
- Density: 14 cards for 146 numbered steps in the three full builds, about one per ten steps, all in the electronics sections except `LED Stems`.
- Recency: the `Capacitor` card's saved render is dated 2026-09-22 in both LSM Part 1 and LSM Full, and both projects were last modified that day - the latest edit in the whole corpus. The card is absent from the older LSM Part 1+2. Cards are being back-fitted, which supports treating them as current house style.

### STR-13. Title page: logo top-left, three-line title block bottom-left, finished model on the right

Rule: build `Start` from two unanchored 2D images on the left edge and a 3D hero on the right. Nothing else.

- 19 of 19 title pages have exactly two annotations, both images with no frame, no leader and no anchor; both are removed on the next step. Table 6 has the stored geometry.
- Logo: the same SVG file in all 19 (white "TECHBOX" wordmark and light-bulb/gear mark on a rounded rectangle, fill sampled as #00B0EF). Stored at x 1.8 to 2.5 % in 18 of 19, y 4.0 to 8.1 %, width 33.2 to 39.5 % of viewport width, height = 0.27 x width. By kit: LSM older projects 33.24 % at (2.5, 4.0); LSM later projects 37.58 % at (1.8, 5.0); LAC 38.90 % at (2.1, 5.9); PMG 39.53 % at (2.4, 8.1).
- Title block: one PNG per guide, stored at x 1.6 to 2.5 %, y 61.0 to 64.6 %, width 42.1 to 48.4 %, height = 0.19 to 0.29 x width in 17 of 19 (the two outliers are listed under Exceptions). By kit: LSM Part 2 48.36 % and Part 1+2 45.66 % at (2.5, 62-63); LSM later projects 42.93 % at (1.8, 61-62); LAC 42.07 % at (2.1, 64.1); PMG 46.51 % at (1.6, 64.6).
- Title block content, identical layout in 19 of 19 (montage checked): line 1 kit name with its acronym in brackets, heavy condensed sans, dark grey (sampled #585858): "Laser Stem Matrix (LSM)", "LCD Alarm Clock (LAC)", "Piano Memory Game (PMG)". Line 2 the guide variant in the same face at roughly 45 % of the size (eyeballed): "Part 1" ... "Part 4", "Part 1 + 2", "Part 3 + 4", "Full Build", "Deconstruction". Line 3 the copyright line in a small serif face: "(c) 2025 TechBox. A division of TARIS Industries, LLC. All Rights Reserved." (LSM and LAC, 14 guides) or the same with 2026 (PMG, 5 guides). All three lines are left-aligned to the logo's left edge.
- Measured on nine clean renders at about 2:1 (LSM Part 4, Part 3+4, Full, Deconstruction; LAC Part 4, Full, Deconstruction; PMG Part 3, Full): logo spans x 2 to 39-42 %, y 5-8 to 26-29 %; title block spans x 2 to 44-47 %, y 62-66 to 80-84 %; the model's bounding box starts at x 48-54 % and ends at 88-95 %, y 13-15 to 74-83 %. The left 45 % of the frame is reserved for the two images.
- The hero is the most complete state the guide deals with. In all 16 build guides the set of visible solids on `Start` overlaps the final view's set by at least 95 % (identical in 9; leaf-level walk). In the 3 deconstructions it is the fully built kit, i.e. the state the guide starts from. The first content step then rewinds: it always moves the camera (19 of 19, 8 to 110 degrees) and replaces most of the scene.
- Camera on `Start`: elevation 21 to 47 degrees (median 35). Full builds reuse the last part's title camera (STR-16).
- Exceptions: LSM Part 1's title image is stored at y 24 %, width 58 %, h/w 0.56 (a taller PNG with transparent padding; it renders in the usual place). PMG Deconstruction's two images are shifted right (x 5.1 and 3.8 %) and in its saved render (2.63:1) the title text overlaps the model. `Start` carries Cadasio's placeholder description in LSM Part 4 and Part 3+4.

### STR-14. The final view is a clean hero shot near the title-page direction

Rule: after the last `Step Nc`, add one pause step that changes only the camera: orbit to a three-quarter hero view of the result, with no annotations.

- 0 annotations on 19 of 19. Camera moves on 17 of 19 (4.9 to 120 degrees, median 66).
- In build guides the final view direction is within 23 degrees of the `Start` direction in 14 of 16 (median 13 degrees; LAC Part 4 and LAC Full are 76 degrees off: the title looks at the clock from its front-right, the final view from its front-left, where the USB lead comes out). Final elevation 21 to 48 degrees (median 38).
- Distance relative to `Start` is a whole number of zoom-ladder clicks (x1.166): the same distance in 9 build guides, one click closer (x0.86) in 3, three clicks closer (x0.63) in 3, one click farther in 1.
- Model content: unchanged from the last `Step Nc` in 10 of 16 build guides. Small unannounced changes in the others (two wire caps reappear in LSM Part 4 / Part 3+4 / Full; panel H14 settles 1.7 mm in PMG Part 3 / Full; the 64 stems drop 9.7 mm in LSM Part 3+4).
- Exceptions: PMG Part 1 [033] and PMG Deconstruction [060] have no camera move and perform the last step's result themselves (they are a `Step Nc` renamed). In deconstructions the step is still called `Completed View` although it shows what is left (bare breadboard on its base, or the bare shield).

### STR-15. Part guides are slices of one master project, each with its own bookends

Rule: author the kit once as a full build. Produce each part guide by cutting a contiguous run of that sequence at a pair boundary, renumbering from 1, and adding a part-specific `Start` (hero = that part's finished state, subtitle "Part n") and a part-specific final view.

- LAC: Full created 2025-10-06, Parts 1-4 cloned 2025-12-10/11; all share one CAD id and the identical inventory of 150 annotation objects. Aligning the sequences, every one of the 130 non-title steps of the full build has a twin in a part with identical camera (distance / elevation / azimuth), annotation counts, behaviour and duration.
- PMG: Full created 2026-05-20, Parts 1-3 cloned 2026-08-07; same CAD id and the same 133 annotation objects. 114 of 115 matched non-title steps are identical on the same test (the `4-Digit Display` card camera differs).
- LSM is the exception in history, not in outcome: the combined guides came first (Part 1+2 2025-07-17, Part 3+4 2025-08-04), the four parts were cut from them on 2025-08-22, and the full build was made on 2025-08-28 with the Part 1/2 region re-shot (only 23 of 83 matched steps keep the same camera and annotation counts).
- Cuts fall between a `Step Nc` and the next card or `Step N`, never inside a pair. Where the next section opens with a card, the part opens with that card directly after `Start` (LAC Part 2, LAC Part 3, PMG Part 1, PMG Part 2).
- Each part is one phase of work: LAC 14 / 18 / 8 / 17 numbered steps, PMG 14 / 11 / 26, LSM 8 / 13 / 5 / 12. The last part of every kit is the enclosure.
- Leftovers of the cut stay in the file as hidden steps (68 across 17 guides) and unused annotation objects; they are not student-visible.

### STR-16. A full build is the parts concatenated with the inner bookends removed and nothing put in their place

Rule: for a full or combined guide keep one `Start` (the last part's hero, with the subtitle image swapped) and one final view (the last part's). Drop every other `Start` and final view. Do not insert a divider, a "Part n" card or a recap at the seams; keep every section card; renumber continuously.

| Guide | Sum of its parts | Dropped | Added | Result |
|---|---|---|---|---|
| LAC Full | 32 + 42 + 21 + 42 = 137 | 3 final views + 3 Starts | nothing | 131 |
| PMG Full | 34 + 27 + 59 = 120 | Part 2 Start, Part 2 final view, one Start | nothing (Part 1's `Completed View` is kept under the name `Step 14c`) | 117 |
| LSM Full | 19 + 31 + 13 + 29 = 92 | 3 final views + 3 Starts | 2 Transitions ([002] inside Step 1, [059] at the Part 3 / Part 4 seam) | 88 |
| LSM Part 1+2 | 19 + 31 = 50 | Part 1 final view, Part 2 Start, Part 1's `Capacitor` card (added to Part 1 later) | nothing | 47 |
| LSM Part 3+4 | 13 + 29 = 42 | Part 3 final view, Part 4 Start | `Step 1` / `Step 1c` (the D2 panel step that the split series keeps in Part 2) and 1 Transition [014] at the seam | 43 |

- Kept `Start`: same camera as the last part's `Start` in LAC Full, PMG Full, LSM Part 1+2 and LSM Part 3+4; LSM Full pulls back one zoom click (321 to 374 mm) and nudges the view by a few degrees. Kept final view: identical camera to the last part's in 5 of 5.
- Seams, as the student sees them: LAC Full [030] `Step 14c` to [031] `Rocker Switch` card; [070] `Step 32c` to [071] `Alarm Buzzer` card; [089] `Step 40c` to [090] `Step 41` (camera 73 degrees, 277 to 377 mm). PMG Full [033] `Step 14c` to [034] `4-Digit Display` card; [058] `Step 25c` to [059] `Step 26` (camera 110 degrees, all electronics fade out, H1 and H2 fade in). LSM Full [018] `Step 8c` to [019] `Step 9`; [047] `Step 21c` to [048] `Step 22`; [058] `Step 26c` to auto Transition [059] to [060] `Step 27`. In 8 of 10 seams the next step simply follows; the 2 with a Transition are the LSM Part 3 / Part 4 seam in both guides that contain it.
- Not a pure concatenation in LSM only: the full build plugs in the USB cable (Step 20) before standing the D2 panel on the base (Step 21), the reverse of Part 2 and Part 1+2; the Part 1/2 region is re-shot; LSM Part 3+4 repeats the panel step that Part 1+2 already contains.
- Combined guides ("Part 1 + 2", "Part 3 + 4") exist only for LSM, the oldest kit. LAC and PMG publish parts, a full build and a deconstruction only.

### STR-17. Deconstruction guides use the same skeleton with the Transition as the norm

Rule: structure a take-apart guide exactly like a build guide (Start, numbered pairs from 1, final view), omit cards, and give each removal the three-beat `Step N` (cue, model unchanged) / `Transition` (part slides away) / `Step Nc` (part gone).

- 3 of 3 deconstruction guides: 1 Start, 0 cards, 0 text, 1 `Completed View`; 24 / 47 / 23 numbered steps against 38 / 57 / 51 in the matching build.
- Transition inside the pair in 56 of 94 numbered steps (60 %) against 9 % in build guides. Where there is none, the step is a wire or module swap or the part stays on screen.
- `Start` reuses the full build's title page: identical camera in LSM and LAC (374 / 29 / 54 and 377 / 37 / 143), same hero in PMG; only the subtitle image changes to "Deconstruction".
- All three were cloned from the full-build project (same CAD id; created after the build) and are the least tidy guides in the corpus: three of the four broken pairs in STR-2, the duplicated `Step 45c`, both pause Transitions and 6 of the 9 picker-visible Transitions are in deconstructions.

### STR-18. A kit-contents overview is a separate, stepless guide (one instance)

Rule (low confidence, one guide): present kit contents as a short guide of static named views ("All Electronics", "All Wood"), with no title page, numbering, Transitions or final view.

- LAC Electronics: 2 viewer steps, both named cards, both pause / 800 ms, camera moves on both, 0 annotations. A hidden `Start` step sits last in the order. `All Wood` still carries Cadasio's placeholder description.

### STR-19. Guides are wordless: no step descriptions, no popups

Rule: do not rely on step description text. Carry the instruction with the frame itself; the only viewer-chrome text is the step name.

- Real description text exists only in the three oldest LSM projects: Part 1+2 (28 of 47 steps), Part 2 (18 of 31), Part 1 (6 of 19). That is 52 of 1037 steps. Three more descriptions are Cadasio's default placeholder (LSM Part 4 Start, LSM Part 3+4 Start, LAC Electronics `All Wood`).
- The other 17 guides, which include every project created after 2025-08-22, have no instruction text; popups are unused in 20 of 20 (Table 7).
- Where text exists it follows "Step N - imperative sentence" on `Step N` and a bare "Step Nc" on the result, but it is stale: its numbering lags the step names (name `Step 5` / text "Step 4 - ..."), two steps both say 15, and it contains typos ("srew", "Buttoim", "Ste[ 15", "Step 12c 0 Connect ..."). Treat it as an abandoned feature, not a convention.

### STR-20. A base-state keyframe before the first frame sets the house style

Rule: apply global look (white background, toon style and edges on every solid, default visibility) once, in a keyframe that precedes or coincides with the first visible step; build every later step as a delta on it.

- In 20 of 20 guides the first authored step sets the scene background to #ffffff and a render style on 1148 to 5373 solids. In 15 guides that step is hidden (named `Start`, `Step 50`, `Step 51`, `Step 60`, `Step 143`); in 4 it is the visible `Start` (LSM Part 1, Part 2, Part 1+2, PMG Deconstruction); in LAC Electronics it is the first view.
- Hidden steps are folded into the next visible step by the viewer. 68 hidden steps in 17 guides; apart from the base state they are abandoned drafts (duplicate `Step 2`, `colors`, `Step 97`, a stale `Step 23c`).

## 2. Anomalies (typos and inconsistencies, not conventions)

Step names
- `Copmleted View` - LSM Part 3+4 [042].
- `Completed Build` instead of `Completed View` - LSM Part 2 [030], LSM Part 1+2 [046].
- `Transiton` - LSM Deconstruction [038]. `Ttansition` - LAC Part 2 [023], LAC Full [053]. `Transititon` - LAC Deconstruction [002].
- Capital suffix: `Step 20C` - LSM Part 1+2 [042]; `Step 14C` - LAC Part 1 [030] (the full build has `Step 14c`).
- `Step 8` completed by `Step 9c` - LSM Part 4 [016] / [017]; numbers then run to 13 for 12 steps. Correct in Part 3+4 (14 / 14c) and Full (34 / 34c).
- LAC Deconstruction: `Step 41` twice ([104] and [108]; [104] is an unchanged duplicate of [105] `Step 40`); `Step 45c` twice ([120] and [122]; [120] is the Step 45 instruction frame and carries the arrow); no `Step 45`.
- Missing last result frame: PMG Part 1 has no `Step 14c`; PMG Deconstruction has no `Step 23c` (a hidden stale `Step 23c` exists).

Behaviour and player flags
- Transitions that wait for a click: LAC Deconstruction [033] (also a no-op) and [118].
- Transitions left visible in the step picker and/or with the overlay on: LSM Deconstruction [044] [052] [066]; LAC Part 4 [028]; LAC Deconstruction [033] [118]; PMG Part 3 [056] = PMG Full [114]; PMG Deconstruction [026].
- Transitions that change nothing but annotations: LSM Deconstruction [011] (the D5 panel removal is never shown), LAC Part 4 [027] = LAC Full [116].
- 1600 ms used for screwing the nut on in LSM Part 2 [022] / Part 1+2 [038] but 800 ms for the same step in LSM Full [040]; 1600 ms on two LCD swaps in LAC Deconstruction [016] [017] and on no other swap.
- Step-level `fade` transition applied to 48 of 128 whole-scene swaps and to 17 steps that are not scene swaps (e.g. LSM Full [046], LAC Part 1 [004], LAC Part 2 [025]).
- `startStepId` does not point at the visible `Start` in 19 of 20 projects: it points at a hidden first step in 7, at a mid-guide step in 3 (LSM Part 2 `Step 10`, LSM Part 1+2 `Step 11`, LSM Deconstruction `Step 3`) and at a step id that no longer exists in 9.

Annotations outliving their frame
- `2x` label on Step 4 and Step 4c - LAC Part 1 / LAC Full [008]-[009].
- Two lead lines still on at `Step 26c` / `Step 51c` - PMG Part 3 [057], PMG Full [115].
- Only `Step N` with no annotation: PMG Part 2 [002] = PMG Full [035].

Title pages and names
- "Stem" rather than "STEM" on all 8 LSM title blocks.
- Project names do not match the title blocks: `LAC Full Build`, `LAC Deconstruction`, `LAC Electronics`; `Piano Memory Game(PMG) Updated ` (no space before the bracket, trailing space) for the full build; `Piano Memory Game(PMG) Disassembly` for the guide whose title block says "Deconstruction"; `Laser Stem Matrix (LSM) - Part 3.` (stray full stop); double space in `(LSM) -  Part 2` and `(LSM) -  Part 1 + 2`.
- Guide ids use three different separator styles (`..._lsm_-_part_1`, `..._lsm_part_1_2`, `..._lac_-part_1`, `...-memory-game-part-1`, `..._pmg-full_build`).
- LSM Part 1 title image stored at y 24 % / width 58 % (others y 61-65 % / width 42-48 %); PMG Deconstruction images shifted right and overlapping the model in the saved render.
- Copyright year is baked into the image: 2025 on LSM and LAC, 2026 on PMG.
- Cadasio placeholder description ("A Start point for your project - feel free to rename, reorder or delete") left on LSM Part 4 [000], LSM Part 3+4 [000], LAC Electronics [001], and on the hidden first step of the six other LAC projects.

Relations between guides
- LSM Full reverses the order of the USB-cable and D2-panel steps relative to LSM Part 2 and Part 1+2.
- LSM Part 3+4 `Step 1` repeats LSM Part 1+2 `Step 20`; a class doing the two combined guides sees it twice.
- The `Capacitor` card is in LSM Part 1 and LSM Full but not in LSM Part 1+2.
- Stale descriptions in LSM Part 1 / Part 2 / Part 1+2 (numbering offset, duplicate "15", typos; see STR-19).
- Section cards are uneven: 6 of 31 carry no annotation; the potentiometer, resistors and jumper ribbons get a numbered prep step instead of a card; in PMG Full the ribbon prep comes before the `Push Buttons` card but after the `4-Digit Display` card.

## 3. Numeric defaults

| Name | Value | Basis |
|---|---|---|
| Step animation duration | 800 ms | 1030 of 1037 viewer steps |
| Duration for a threaded spin move | 1600 ms | 5 of the 7 exceptions (LSM nut on / off); not applied in LSM Full Step 18c |
| Part show / hide / move | fade / fade / tween | 1037 of 1037 |
| Camera move | tween, no orbit animation, speed 2 | 1037 of 1037 |
| 2D annotation show / hide / move | fade / fade / tween | 1037 of 1037 |
| Behaviour of Start, card, Step N, Step Nc, final | pause | 920 of 920 |
| Behaviour of Transition | play (auto-advance) | 115 of 117 |
| Transition hidden from step picker | true | 108 of 117 |
| Navigation overlay during Transition | hidden | 110 of 117 |
| Step-level page transition | none | 970 of 1037; fade on 65, all LSM / LAC; PMG 0 of 298 |
| Annotation lifetime | 1 viewer step | 1012 of 1019 showings |
| Annotations on Start | 2 (logo, title block) | 19 of 19 |
| Annotations on final view | 0 | 19 of 19 |
| Annotations on a card | 0 to 2 | 31 cards: 6 with 0, 23 with 1, 2 with 2 |
| Camera moves on Step Nc | never | 0 of 424 |
| Camera moves on Step N | 63 % of the time, median rotation 62.5 degrees (build) | 266 of 425 |
| Max Transitions inside one numbered step | 3 (typical 0 or 1) | 334 pairs with 0, 76 with 1, 9 with 2, 2 with 3 |
| Share of numbered steps with a Transition | 9 % build, 60 % deconstruction | 31 of 331; 56 of 94 |
| Viewer steps per numbered step | 2.3 to 2.6 build, 2.7 to 2.9 deconstruction | Table 3 |
| Numbered steps per part guide | 5 to 26, median 13 | 11 part guides |
| Section cards per full build | 4 / 5 / 5 (about 1 per 10 numbered steps) | LSM / LAC / PMG full builds |
| Logo position (top-left corner) | x 2 %, y 4 to 8 % of viewport | 18 of 19 at x 1.8-2.5 %; PMG Deconstruction 5.1 % |
| Logo width | 37.6 to 39.5 % of viewport width (33.2 % in the 3 oldest); height = 0.27 x width | Table 6 |
| Title block position | x 2 %, y 61 to 65 % | 18 of 19 |
| Title block width | 42 to 46.5 % of viewport width; height = 0.19 to 0.29 x width | Table 6 |
| Hero model bounding box on Start | x from 48-54 % to 88-95 %; y from 13-15 % to 74-83 % (2:1 viewport) | 9 clean title renders |
| Logo fill colour | #00B0EF | sampled from 3 raw title renders |
| Title text colour | #585858 | sampled from 3 raw title renders |
| Background | #ffffff | scene colour in 20 of 20 |
| Start camera elevation | 21 to 47 degrees, median 35 | 19 title pages |
| Final view camera elevation | 21 to 48 degrees, median 38 | 16 build guides |
| Final view direction vs Start | within 23 degrees (median 13) | 14 of 16 build guides |
| Final view distance vs Start | x1.00, x0.86 or x0.63 (0, 1 or 3 zoom clicks of 1.166) | 15 of 16 build guides |
| Camera | perspective, field of view 45 degrees | 20 of 20 |
| Navigation overlay | bar along the bottom, visible at start | 20 of 20 |
| Auto-start, animate when stepping back | true, true | 20 of 20 |

## 4. Open questions

1. Which step does the live viewer open on? `startStepId` is unusable (it matches the visible `Start` in 1 of 20 projects). The data are consistent with "first non-hidden step in order", but this was not observed in a browser.
2. After a `play` step, does the viewer advance as soon as the 800 ms animation ends, or is there a dwell? `playStepTimeout` is null in 20 of 20, which suggests no dwell.
3. When the student presses Back from a `Step Nc` that follows a Transition, does the viewer stop on the Transition or run back through it to `Step N`? `animatePreviousStep` is true everywhere, but the behaviour on `play` steps going backwards is not in the data.
4. What does the step-level `transition: fade` look like compared with the default (cross-dissolve of the whole frame, or parts fading while the camera cuts)? It is used 65 times in LSM / LAC and never in PMG.
5. Is the "c" suffix meant to be read by students (the step picker lists `Step 3` and `Step 3c` as two entries), or is it an authoring label TechBox would rather present as one step with two states?
6. Should the final frame of a deconstruction keep the name `Completed View`? It shows the leftover base, not a completed model.
7. Are the LSM "Part 1 + 2" / "Part 3 + 4" combined guides still a wanted format? They exist only for the oldest kit and have drifted from the parts.
8. Is a Transition for a camera flip wanted? LSM does it 8 times; LAC and PMG flip the up-axis on `Step N` directly.
9. Should the 1600 ms spin exception be kept? Its own kit applies it inconsistently and LAC's nut steps use 800 ms.
10. Does TechBox want step description text supported at all? It survives only in three 2025 LSM projects and is stale there.

## 5. Tables behind the numbers

### Table 1. Composition of all 20 guides (viewer steps = what the student sees)

| Guide | Created | Viewer steps | Hidden authoring steps | Start | Cards | Step N | Step Nc | Transition | Final | pause | play | Numbered steps (first..last) | Final step name |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LSM-P1 | 2025-08-22 | 19 | 0 | 1 | 1 | 8 | 8 | 0 | 1 | 19 | 0 | 8 (1..8) | Completed View |
| LSM-P2 | 2025-08-22 | 31 | 0 | 1 | 2 | 13 | 13 | 1 | 1 | 30 | 1 | 13 (1..13) | Completed Build |
| LSM-P1+2 | 2025-07-17 | 47 | 0 | 1 | 2 | 21 | 21 | 1 | 1 | 46 | 1 | 21 (1..21) | Completed Build |
| LSM-P3 | 2025-08-22 | 13 | 1 | 1 | 0 | 5 | 5 | 1 | 1 | 12 | 1 | 5 (1..5) | Completed View |
| LSM-P4 | 2025-08-22 | 29 | 8 | 1 | 1 | 12 | 12 | 2 | 1 | 27 | 2 | 12 (1..13) | Completed View |
| LSM-P3+4 | 2025-08-04 | 43 | 5 | 1 | 1 | 18 | 18 | 4 | 1 | 39 | 4 | 18 (1..18) | Copmleted View |
| LSM-Full | 2025-08-28 | 88 | 1 | 1 | 4 | 38 | 38 | 6 | 1 | 82 | 6 | 38 (1..38) | Completed View |
| LSM-Decon | 2025-08-30 | 69 | 1 | 1 | 0 | 24 | 24 | 19 | 1 | 50 | 19 | 24 (1..24) | Completed View |
| LAC-P1 | 2025-12-10 | 32 | 1 | 1 | 1 | 14 | 14 | 1 | 1 | 31 | 1 | 14 (1..14) | Completed View |
| LAC-P2 | 2025-12-11 | 42 | 1 | 1 | 1 | 18 | 18 | 3 | 1 | 39 | 3 | 18 (1..18) | Completed View |
| LAC-P3 | 2025-12-11 | 21 | 1 | 1 | 3 | 8 | 8 | 0 | 1 | 21 | 0 | 8 (1..8) | Completed View |
| LAC-P4 | 2025-12-11 | 42 | 1 | 1 | 0 | 17 | 17 | 6 | 1 | 36 | 6 | 17 (1..17) | Completed View |
| LAC-Full | 2025-10-06 | 131 | 1 | 1 | 5 | 57 | 57 | 10 | 1 | 121 | 10 | 57 (1..57) | Completed View |
| LAC-Decon | 2025-11-26 | 130 | 1 | 1 | 0 | 47 | 48 | 33 | 1 | 99 | 31 | 47 (1..47) | Completed View |
| LAC-Elec | 2026-02-16 | 2 | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (-..-) | (none) |
| PMG-P1 | 2026-08-07 | 34 | 6 | 1 | 2 | 14 | 13 | 3 | 1 | 31 | 3 | 14 (1..14) | Completed View |
| PMG-P2 | 2026-08-07 | 27 | 4 | 1 | 3 | 11 | 11 | 0 | 1 | 27 | 0 | 11 (1..11) | Completed View |
| PMG-P3 | 2026-08-07 | 59 | 12 | 1 | 0 | 26 | 26 | 5 | 1 | 54 | 5 | 26 (1..26) | Completed View |
| PMG-Full | 2026-05-20 | 117 | 18 | 1 | 5 | 51 | 51 | 8 | 1 | 109 | 8 | 51 (1..51) | Completed View |
| PMG-Decon | 2026-08-24 | 61 | 5 | 1 | 0 | 23 | 22 | 14 | 1 | 47 | 14 | 23 (1..23) | Completed View |
| **Total** | | **1037** | **68** | 19 | 33 | 425 | 424 | 117 | 19 | 922 | 115 | 425 | |

### Table 2. Step properties by step kind, all 20 guides (n = 1037)

| Kind | n | behaviour pause | behaviour play | 800 ms | 1600 ms | camera moves on entry | has >=1 annotation | hideInStepPicker = true | overlayVisible = false | step-level transition = fade |
|---|---|---|---|---|---|---|---|---|---|---|
| Start | 19 | 19 | 0 | 19 | 0 | 19 | 19 | 0 | 0 | 0 |
| Named card | 33 | 33 | 0 | 33 | 0 | 31 | 25 | 0 | 0 | 17 |
| Step N | 425 | 425 | 0 | 425 | 0 | 266 | 423 | 0 | 0 | 44 |
| Transition | 117 | 2 | 115 | 112 | 5 | 12 | 15 | 108 | 110 | 0 |
| Step Nc | 424 | 424 | 0 | 422 | 2 | 0 | 26 | 0 | 0 | 4 |
| Completed View/Build | 19 | 19 | 0 | 19 | 0 | 17 | 0 | 0 | 0 | 0 |

### Table 3. Per guide: where the camera moves and where annotations sit

| Guide | Step N with camera move | Step Nc with camera move | Transition with camera move | Step N with annotation | Step Nc with annotation | Transition with annotation | Numbered steps containing >=1 Transition | Viewer steps per numbered step |
|---|---|---|---|---|---|---|---|---|
| LSM-P1 | 7/8 | 0/8 | 0/0 | 8/8 | 0/8 | 0/0 | 0/8 | 2.38 |
| LSM-P2 | 11/13 | 0/13 | 0/1 | 13/13 | 0/13 | 0/1 | 1/13 | 2.38 |
| LSM-P1+2 | 18/21 | 0/21 | 0/1 | 21/21 | 0/21 | 0/1 | 1/21 | 2.24 |
| LSM-P3 | 3/5 | 0/5 | 1/1 | 5/5 | 1/5 | 0/1 | 0/5 | 2.60 |
| LSM-P4 | 9/12 | 0/12 | 1/2 | 12/12 | 2/12 | 0/2 | 1/12 | 2.42 |
| LSM-P3+4 | 12/18 | 0/18 | 3/4 | 18/18 | 3/18 | 0/4 | 1/18 | 2.39 |
| LSM-Full | 29/38 | 0/38 | 3/6 | 38/38 | 3/38 | 0/6 | 3/38 | 2.32 |
| LSM-Decon | 19/24 | 0/24 | 0/19 | 24/24 | 0/24 | 0/19 | 19/24 | 2.88 |
| LAC-P1 | 7/14 | 0/14 | 0/1 | 14/14 | 1/14 | 0/1 | 1/14 | 2.29 |
| LAC-P2 | 8/18 | 0/18 | 0/3 | 18/18 | 1/18 | 0/3 | 3/18 | 2.33 |
| LAC-P3 | 4/8 | 0/8 | 0/0 | 8/8 | 0/8 | 0/0 | 0/8 | 2.62 |
| LAC-P4 | 11/17 | 0/17 | 1/6 | 17/17 | 3/17 | 0/6 | 3/17 | 2.47 |
| LAC-Full | 30/57 | 0/57 | 1/10 | 57/57 | 5/57 | 0/10 | 7/57 | 2.30 |
| LAC-Decon | 16/47 | 0/48 | 0/33 | 47/47 | 1/48 | 0/33 | 27/47 | 2.77 |
| LAC-Elec | - | - | - | - | - | - | - | - |
| PMG-P1 | 3/14 | 0/13 | 0/3 | 14/14 | 0/13 | 0/3 | 0/14 | 2.43 |
| PMG-P2 | 4/11 | 0/11 | 0/0 | 10/11 | 0/11 | 0/0 | 0/11 | 2.45 |
| PMG-P3 | 24/26 | 0/26 | 0/5 | 26/26 | 3/26 | 3/5 | 5/26 | 2.27 |
| PMG-Full | 31/51 | 0/51 | 0/8 | 50/51 | 3/51 | 3/8 | 5/51 | 2.29 |
| PMG-Decon | 20/23 | 0/22 | 2/14 | 23/23 | 0/22 | 9/14 | 10/23 | 2.65 |

### Table 4. Every Transition step (117) classified

Position: *inside* = between a Step N and its Step Nc; *between* = after a Step Nc and before the next Step N. Content is from a leaf-level walk of the raw payload (camera = camera pose changes; move = a visible part translates/rotates; swap = one model fades out while another fades in; appear = parts only fade in; none = only annotations are cleared).

| Guide | Inside: part move | Inside: model swap | Inside: nothing but clearing cues | Inside: camera only | Between: camera only (+ up-axis flip) | Between: part fades in | Total | play | hidden from picker | nav overlay hidden | 1600 ms |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LSM-P2 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| LSM-P1+2 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| LSM-P3 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 0 |
| LSM-P4 | 1 | 0 | 0 | 0 | 1 | 0 | 2 | 2 | 2 | 2 | 0 |
| LSM-P3+4 | 1 | 0 | 0 | 0 | 3 | 0 | 4 | 4 | 4 | 4 | 0 |
| LSM-Full | 3 | 0 | 0 | 0 | 3 | 0 | 6 | 6 | 6 | 6 | 1 |
| LSM-Decon | 17 | 1 | 1 | 0 | 0 | 0 | 19 | 19 | 16 | 17 | 0 |
| LAC-P1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0 |
| LAC-P2 | 3 | 0 | 0 | 0 | 0 | 0 | 3 | 3 | 3 | 3 | 0 |
| LAC-P4 | 3 | 1 | 1 | 0 | 1 | 0 | 6 | 6 | 5 | 6 | 0 |
| LAC-Full | 7 | 1 | 1 | 0 | 1 | 0 | 10 | 10 | 10 | 10 | 0 |
| LAC-Decon | 17 | 15 | 1 | 0 | 0 | 0 | 33 | 31 | 31 | 31 | 2 |
| PMG-P1 | 0 | 0 | 0 | 0 | 0 | 3 | 3 | 3 | 3 | 3 | 0 |
| PMG-P3 | 3 | 2 | 0 | 0 | 0 | 0 | 5 | 5 | 4 | 4 | 0 |
| PMG-Full | 3 | 2 | 0 | 0 | 0 | 3 | 8 | 8 | 7 | 7 | 0 |
| PMG-Decon | 7 | 5 | 0 | 2 | 0 | 0 | 14 | 14 | 13 | 13 | 0 |
| **All** | 68 | 27 | 4 | 2 | 10 | 6 | 117 | 115 | 108 | 110 | 5 |

### Table 5. Every named section card (31, plus the 2 views of LAC Electronics)

| Guide | Index | Card name | Preceded by | Followed by | Camera moves on entry | Camera distance (mm) | Annotations on the card |
|---|---|---|---|---|---|---|---|
| LSM-P1 | [011] | Capacitor | Step 5c | Step 6 | yes | 60 | image w=31.99% (leader to part) |
| LSM-P2 | [009] | LED Matrix Diagram | Step 4c | Step 5 | no | 163 | image w=62.81% (no leader) |
| LSM-P2 | [027] | Mini USB Cable | Step 12c | Step 13 | yes | 190 | image w=7.81% (leader to part) |
| LSM-P1+2 | [025] | LED Matrix Diagram | Step 12c | Step 13 | no | 163 | image w=62.81% (no leader) |
| LSM-P1+2 | [043] | Mini USB Cable | Step 20C | Step 21 | yes | 190 | image w=7.81% (leader to part) |
| LSM-P4 | [023] | LED Stems | Step 11c | Step 12 | yes | 173 | label "64X" |
| LSM-P3+4 | [037] | LED Stems | Step 16c | Step 17 | yes | 173 | label "64X" |
| LSM-Full | [012] | Capacitor | Step 5c | Step 6 | yes | 42 | image w=30.32% (leader to part) |
| LSM-Full | [027] | LED Matrix Diagram | Step 12c | Step 13 | yes | 221 | image w=65.23% (no leader) |
| LSM-Full | [043] | Mini USB Cable | Step 19c | Step 20 | yes | 221 | image w=7.81% (leader to part) |
| LSM-Full | [082] | LED Stems | Step 36c | Step 37 | yes | 173 | label "64x" |
| LAC-P1 | [014] | Real Time Clock | Step 6c | Step 7 | yes | 175 | image w=7.81% (leader to part) |
| LAC-P2 | [001] | Rocker Switch | Start | Step 1 | yes | 175 | none |
| LAC-P3 | [001] | Alarm Buzzer | Start | Step 1 | yes | 237 | image w=7.81% (leader to part) |
| LAC-P3 | [008] | LCD Screen | Step 3c | Step 4 | yes | 150 | image w=7.81% (leader to part); image w=29.02% (leader to part) |
| LAC-P3 | [017] | USB Cable | Step 7c | Step 8 | yes | 277 | none |
| LAC-Full | [014] | Real Time Clock | Step 6c | Step 7 | yes | 175 | image w=7.81% (leader to part) |
| LAC-Full | [031] | Rocker Switch | Step 14c | Step 15 | yes | 175 | none |
| LAC-Full | [071] | Alarm Buzzer | Step 32c | Step 33 | yes | 237 | image w=7.81% (leader to part) |
| LAC-Full | [078] | LCD Screen | Step 35c | Step 36 | yes | 150 | image w=7.81% (leader to part); image w=29.02% (leader to part) |
| LAC-Full | [087] | USB Cable | Step 39c | Step 40 | yes | 277 | none |
| LAC-Elec | [000] | All Electronics | (first step) | All Wood | yes | 513 | none |
| LAC-Elec | [001] | All Wood | All Electronics | (last step) | yes | 1505 | none |
| PMG-P1 | [001] | Nano I/O Module | Start | Step 1 | yes | 133 | label "NANO I/O MODULE LABELS" |
| PMG-P1 | [006] | Push Buttons | Step 2c | Step 3 | yes | 43 | image w=17.15% (leader to part) |
| PMG-P2 | [001] | 4-Digit Display | Start | Step 1 | yes | 91 | image w=33.56% (leader to part) |
| PMG-P2 | [012] | Dot Matrix Display | Step 5c | Step 6 | yes | 236 | image w=36.72% (leader to part) |
| PMG-P2 | [023] | USB Cable | Step 10c | Step 11 | yes | 202 | none |
| PMG-Full | [001] | Nano I/O Module | Start | Step 1 | yes | 133 | label "NANO I/O MODULE LABELS" |
| PMG-Full | [006] | Push Buttons | Step 2c | Step 3 | yes | 43 | image w=17.15% (leader to part) |
| PMG-Full | [034] | 4-Digit Display | Step 14c | Step 15 | yes | 91 | image w=33.56% (leader to part) |
| PMG-Full | [045] | Dot Matrix Display | Step 19c | Step 20 | yes | 236 | image w=36.72% (leader to part) |
| PMG-Full | [056] | USB Cable | Step 24c | Step 25 | yes | 202 | none |

### Table 6. Title page (Start) and final view, per guide

Positions are the stored top-left corner of each image in % of viewport width / height; width in % of viewport width; h/w is the stored aspect ratio.

| Guide | Logo x,y | Logo width | Title block x,y | Title width | Title h/w | Start camera dist / elev / azim | Final camera dist / elev / azim | Angle Start vs Final view | Final dist / Start dist | Camera move into final |
|---|---|---|---|---|---|---|---|---|---|---|
| LSM-P1 | 2.5, 4.0 | 33.24 | 2.5, 24.1 | 58.28 | 0.56 | 190 / 47 / -141 | 190 / 48 / -146 | 4 deg | 1.00 | 21.2 deg |
| LSM-P2 | 2.5, 4.0 | 33.24 | 2.5, 62.0 | 48.36 | 0.27 | 351 / 37 / 50 | 221 / 39 / 40 | 8 deg | 0.63 | 70.4 deg |
| LSM-P1+2 | 2.5, 4.0 | 33.24 | 2.5, 62.9 | 45.66 | 0.22 | 351 / 37 / 50 | 221 / 39 / 40 | 8 deg | 0.63 | 70.4 deg |
| LSM-P3 | 1.8, 5.0 | 37.58 | 1.8, 61.7 | 42.93 | 0.23 | 258 / 41 / 51 | 221 / 42 / 35 | 12 deg | 0.86 | 66.4 deg |
| LSM-P4 | 1.8, 5.0 | 37.58 | 1.8, 61.5 | 42.93 | 0.22 | 321 / 27 / 57 | 321 / 39 / 44 | 16 deg | 1.00 | 12.9 deg |
| LSM-P3+4 | 1.9, 4.7 | 37.58 | 1.9, 61.0 | 42.93 | 0.23 | 321 / 27 / 57 | 321 / 39 / 44 | 16 deg | 1.00 | 12.9 deg |
| LSM-Full | 1.8, 5.0 | 37.58 | 1.8, 61.2 | 42.93 | 0.22 | 374 / 29 / 54 | 321 / 39 / 44 | 13 deg | 0.86 | 12.9 deg |
| LSM-Decon | 1.8, 5.0 | 37.58 | 1.8, 61.2 | 42.93 | 0.23 | 374 / 29 / 54 | 189 / 49 / 38 | 23 deg | 0.51 | 17.5 deg |
| LAC-P1 | 2.1, 5.9 | 38.90 | 2.1, 64.1 | 42.07 | 0.24 | 277 / 44 / 49 | 277 / 44 / 38 | 8 deg | 1.00 | 55.5 deg |
| LAC-P2 | 2.1, 5.9 | 38.90 | 2.1, 64.1 | 42.07 | 0.24 | 439 / 35 / 141 | 439 / 32 / 127 | 12 deg | 1.00 | 7.0 deg |
| LAC-P3 | 2.1, 5.9 | 38.90 | 2.1, 64.1 | 42.07 | 0.23 | 513 / 30 / 142 | 439 / 30 / 128 | 12 deg | 0.86 | 120.3 deg |
| LAC-P4 | 2.1, 5.9 | 38.90 | 2.1, 64.1 | 42.07 | 0.23 | 377 / 37 / 143 | 377 / 34 / 45 | 76 deg | 1.00 | 69.5 deg |
| LAC-Full | 2.1, 5.9 | 38.90 | 2.1, 64.1 | 42.07 | 0.29 | 377 / 37 / 143 | 377 / 34 / 45 | 76 deg | 1.00 | 69.5 deg |
| LAC-Decon | 2.1, 5.9 | 38.90 | 2.1, 64.1 | 42.07 | 0.25 | 377 / 37 / 143 | 237 / 50 / 50 | 64 deg | 0.63 | 4.9 deg |
| PMG-P1 | 2.4, 8.1 | 39.53 | 1.6, 64.6 | 46.51 | 0.19 | 148 / 22 / -60 | 173 / 21 / -62 | 2 deg | 1.17 | none |
| PMG-P2 | 2.4, 8.1 | 39.53 | 1.6, 64.6 | 46.51 | 0.20 | 436 / 35 / -55 | 275 / 37 / -82 | 22 deg | 0.63 | 119.4 deg |
| PMG-P3 | 2.4, 8.1 | 39.53 | 1.6, 64.6 | 46.51 | 0.20 | 320 / 21 / -43 | 320 / 35 / -61 | 21 deg | 1.00 | 84.8 deg |
| PMG-Full | 2.4, 8.1 | 39.53 | 1.6, 64.6 | 46.51 | 0.20 | 320 / 21 / -43 | 320 / 35 / -61 | 21 deg | 1.00 | 84.8 deg |
| PMG-Decon | 5.1, 7.8 | 36.38 | 3.8, 63.8 | 45.80 | 0.25 | 320 / 33 / -46 | 173 / 23 / 90 | 110 deg | 0.54 | none |

Build guides (16): angle between Start and final view directions min 2, median 13, max 76 deg; 14/16 within 23 deg. Start elevation (19 guides) 21..47 deg, median 35. Final elevation (16 build guides) 21..48 deg, median 38.0.

### Table 7. Step description text and popups

| Guide | Steps with a description | of which Cadasio placeholder text | Popups |
|---|---|---|---|
| LSM-P1 | 6/19 | 0 | 0 |
| LSM-P2 | 18/31 | 0 | 0 |
| LSM-P1+2 | 28/47 | 0 | 0 |
| LSM-P3 | 0/13 | 0 | 0 |
| LSM-P4 | 1/29 | 1 | 0 |
| LSM-P3+4 | 1/43 | 1 | 0 |
| LSM-Full | 0/88 | 0 | 0 |
| LSM-Decon | 0/69 | 0 | 0 |
| LAC-P1 | 0/32 | 0 | 0 |
| LAC-P2 | 0/42 | 0 | 0 |
| LAC-P3 | 0/21 | 0 | 0 |
| LAC-P4 | 0/42 | 0 | 0 |
| LAC-Full | 0/131 | 0 | 0 |
| LAC-Decon | 0/130 | 0 | 0 |
| LAC-Elec | 1/2 | 1 | 0 |
| PMG-P1 | 0/34 | 0 | 0 |
| PMG-P2 | 0/27 | 0 | 0 |
| PMG-P3 | 0/59 | 0 | 0 |
| PMG-Full | 0/117 | 0 | 0 |
| PMG-Decon | 0/61 | 0 | 0 |

### Table 8. What changes on Step N and on Step Nc (leaf-level walk of the raw payload)

appear = parts only fade in; swap = some parts fade out while others fade in; move = a visible part translates or rotates; none = geometry unchanged (annotation-only frame).

| Guide set | Kind | n | appear only | swap | move (any) | disappear only | none |
|---|---|---|---|---|---|---|---|
| 14 build guides | Step N | 331 | 173 | 34 | 40 | 2 | 82 |
| 14 build guides | Step Nc | 330 | 8 | 156 | 154 | 12 | 0 |
| 3 deconstruction guides | Step N | 94 | 7 | 8 | 5 | 7 | 67 |
| 3 deconstruction guides | Step Nc | 94 | 0 | 22 | 8 | 63 | 1 |

