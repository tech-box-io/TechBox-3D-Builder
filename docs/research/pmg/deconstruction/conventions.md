# PMG deconstruction: Lee's conventions, and the published take-apart mapped onto the in-house Full Build

Study of 21 Oct 2026, read-only (nothing run, nothing changed but this file). For writing
`PMG Build Instructions/deconstruction.py` from the Full Build (`guide.py` -> `steps.json`).

Sources read: `docs/cadasio-patterns.md` sections 1, 4, 5, 6, 11, 13 (removal row, wire granularity row); `CLAUDE.md` "A kit's
guides" (the deconstruction bullets, lines 332 - 386); `MRA Build Instructions Prototype/README.txt`, `deconstruction.py`,
`steps-deconstruction.json`, `step-text-deconstruction.json`; `RCC Build Instructions/README.txt`, `deconstruction.py`,
`steps-deconstruction.json`; `docs/research/mra/lee_notes_2026-10-18.md`, `lee_notes_2026-10-19.md`; the git log of every
deconstruction commit (17 - 21 Oct); `releases/*-deconstruction/history.json`; `docs/research/guide_19075-piano-memory-game-deconstruction.md`
(TechBox's published PMG take-apart); `PMG Build Instructions/README.txt`, `guide.py`, `steps.json` (read with python);
`tools/stepgen.py` `take_apart()` / `remove()` / `unplug()` / `lift()` / `_takeoff()` / `carry()`.

**A correction to the brief:** the in-house PMG Full Build has **48 steps** (99 views: Start, 2 Parts List pages, Step 3 is a
one-view card, 47 pairs, Completed View). 51 is the *published* Cadasio build's count. The in-house case steps are the published
ones shifted: published B26 -> in-house 27 ... with the published two-step plates (B29+30, B31+32, B35+36, B40+41) each one
in-house step with beats (table in section 3).

---

## 1. Every convention Lee has stated for deconstruction guides

Dates are Lee's; "rulebook" = `docs/cadasio-patterns.md`.

### 1.1 Structure, title page, end, card, parts list

| Convention | Date, source |
|---|---|
| A deconstruction largely follows its construction guide **in reverse**. | Lee 17 Oct; rulebook l.247 |
| A part, once disconnected, **disappears**: it is removed, never reconnected; nothing is refitted for storage (as LAC does). Open: whether "disconnected" means each plug (a lead unplugged at one end dangles from its other end until that end's part goes, as the generator does) or fully free. | Lee 17 Oct; rulebook l.247-252 |
| Its **title page** shows the finished model, the Full Build's (same camera, subtitle "Deconstruction"), not an empty screen. `take_apart()` does this. | Lee 18 Oct (MRA); rulebook l.254; lee_notes_2026-10-18 |
| Its **Completed View** shows only what is left. The MRA's first draft ended on the bare I/O module (Nano last, as Lee first asked); after Lee's first round it ends on the **base, R1**; the RCC's ends on **L1**. "It ends on what is left (the base), closer in." | Lee 18 Oct; rulebook l.254, l.270-273; CLAUDE.md l.369 |
| Its **card** picture on the website is the Full Build's (`_dev.card()` copies it for a `take_apart()` guide). Replaced 17 Oct's "its own title page". | Lee 18 Oct (second round, MRA and RCC); CLAUDE.md l.369-370 |
| **Parts list**: "No Parts List unless asked for" (CLAUDE.md l.369). Lee (with the curriculum director) asked for the MRA's: the Full Build's parts list pages after the Completed View, `take_apart(parts_list_at_end=True)`. The RCC's (made the day before) has none. | Lee 19 Oct; rulebook l.261-265 |
| **No electronics test / no check steps** in a take-apart: a bench test the build makes has no counterpart; each motor is unplugged once and taken out once. Preparation steps (peeling wires off the ribbon) and cards have no counterpart either (rulebook l.240-245). | Lee 18 Oct (MRA draft); rulebook l.256-258 |
| **Every step has a description of its own** (not the build's captions reworded). Its wording is edited in its own sheet (`step-text-deconstruction.json`, via `tools/step_text.py ... steps-deconstruction.json`). | Lee 17 Oct; rulebook l.249; CLAUDE.md l.366 |
| It is a script of its own (`deconstruction.py`, named as `"script"` in `guides.json`), run after every Full Build change; it writes only its steps file and can add parts to the model, never take any away. | CLAUDE.md l.332-367 |
| 2D PDF: the Full Build and the deconstruction first, the Parts' later. | Lee 21 Oct; rulebook section 13 last row |

### 1.2 Order, groups, sub-assemblies

| Convention | Date, source |
|---|---|
| **Parts may be removed in unison**: several units in one step, each its own way (beyond the published guides' identical sets; the generator notes more than two arrows). | Lee 17 Oct; rulebook l.248 |
| **Wires that went on one at a time may come off together**: the MRA's eight breadboard wires off the joysticks and the module **at once** (done, Step 53); "or in phases, the joysticks pulled off the wires, then the wires off the module" (offered, not taken up). | Lee 18 Oct; rulebook l.256-257; lee_notes_2026-10-18 "Exception 1" |
| Lee merged identical pairs on the RCC (second round): **both wheel motors unplugged in one step**, **both pulled out of L5 in one step** (22 -> 20 steps). Latest ask (21 Oct, PMG): "some things can be removed in groups (like the breadboard wires, four buttons, four H9 parts, etc.)". | Lee 18 Oct (commit c9761ce); Lee 21 Oct (this task) |
| **A screw and the part it held, in one step, in sequence** (`in_turn=[[screw], [part]]`) where Lee named it (MRA's A12, A13, A11, A5, the lever); elsewhere a screw keeps its own step. Open whether every pair merges. (No screws in the PMG.) | Lee 18 Oct first round; rulebook l.267-270 |
| **Electronics come out where they are, before the housing around them** (MRA: with B8 off, the breadboard wires off both ends, the module out of its slots, the Nano out of it, then the joysticks with their walls), so the guide ends on the base. | Lee 18 Oct first round; rulebook l.270-273 |
| **Leads are unplugged before the structure around them comes out, as the build plugged them in last** (RCC: the wheel motors before L6, L7 and the I/O module). | Lee 18 Oct (RCC); rulebook l.280-281 |
| **Wired modules are lifted off the housing first, still wired, and unplugged later** (published practice, rulebook l.236; `lift()` exists for it). | rulebook section 11 |
| **A sub-assembly that comes off is taken apart on its own**, the rest hidden, close in (`alone=`), **then the guide returns to the main model** (RCC: the controller; the battery with its adapter; the I/O module). `g.put_away([...])` takes off what is left of it without a step (MRA: T1, C3, A10, A4, A1, A6, the module, B6, B5; RCC: the controller board, the battery, the module, L5). | Lee 18 Oct (RCC); rulebook l.277-280; both scripts |
| **Wood that holds a part comes off that part in the hand** (RCC: L4, L5 off the motors). | Lee 18 Oct (RCC); rulebook l.281-282 |
| A sub-assembly taken apart in the hand is **seen the way the build showed it** (from above where the build did); Lee asked for the claw's C3 from above. | Lee 18 Oct first round; rulebook l.273-275 |
| The **power cable first**: the MRA's USB cable is its Step 4 (after the T block), the RCC's its Step 1. (Both follow from reversal: it went in last in both builds. Lee has not stated "power first" as a rule.) | MRA/RCC scripts |

### 1.3 Arrows, eyes, close-ups, labels

| Convention | Date, source |
|---|---|
| One red arrow per moving unit, **never lead lines**. Parts the Full Build put on together are one unit; two of a kind get an arrow each (if they do not touch). | rulebook l.225; CLAUDE.md l.337-345 |
| **Arrows smaller than the published ones, sized to the part**: 15 - 40 mm long, 1.6 - 3.2 mm thick (a screw's about 17 mm). | Lee 18 Oct second round; rulebook l.226 |
| **Along the longest stage of the part's way** (the module's slide, not the nudge before it), **moved on along it until the camera can see it**; one that would point at the camera becomes an **eye** on the part. `arrow_style={id: dict(stage=k)}` puts it on a chosen stage instead (RCC joysticks: `stage=0`, the pull out of the socket). | Lee 18 Oct second round; RCC second round (c9761ce); CLAUDE.md l.345-347 |
| **On the part that matters**: the joystick, not the walls it carries (`units=[[JOY]]`). | Lee 18 Oct; rulebook l.228 |
| **Sizes by hand where Lee asked**: twice for the USB plug, the extension's join, the six base screws, the base motor; half again for claw parts; the RCC's arrows doubled, then doubled again (all but Steps 8, 12 - 15, 19). `arrow_scale=k`, `arrow_style={id: dict(scale=, like=, at=, shift=, face=, keep=)}`. | Lee 18 Oct third round; RCC (af9f05e) |
| **Placed where it reads**: on the top of R7 / R8 clear of the lead (`at=`), raised above wires (`shift=`), at the edge of B2's cut-out round the horn (where it comes away from); the RCC's adapter-board arrow on its long arm, clear of the Nano; the RCC's right motor's arrow from the same spot on its wheel as the left one's (mirrored). | Lee 18 Oct third round; RCC second round |
| **Kept though pointing towards the camera** where Lee said (the A9s: `keep=True`). | Lee 18 Oct third round |
| **Several screws: an arrow on each** (the six base screws), the hidden one's in a close-up. Two wheel motors: an arrow each. | Lee 18 Oct third round; RCC |
| **A plug moved on its lead gets an eye, no arrow** (as an unplug); `unplug()` puts an eye on each plug by default. | Lee 18 Oct second round |
| **Several wire ends at once: an eye each group** (the eight breadboard wires: one eye at the left joystick's ends, one at the right's, one at the module's; no arrows). | Lee 18 Oct second round (Step 53) |
| **A cable unplugged and removed: one arrow, on the plug that is pulled, clear of the cable; none on its far end** (`units=[[USB_B]]`, the A end given a `paths=` lift). | Lee 18 Oct (RCC); rulebook l.281 |
| **A part the camera cannot see: a close-up from the other side** (punched in, its frame and lead line), with that part's own arrow in it (`inset=dict(..., arrows=[ids])`, the arrow's `face=` towards the close-up), not an eye. | Lee 18 Oct second / third rounds |
| Eyes sit **on a white box** (contrast). | Lee 18 Oct first round (player, every guide) |
| **No text labels** in a take-apart (published), **except** where Lee asked: the MRA's unplugging of a servo carries the Full Build's labels for that row ("Row 6" and the servo) instead of an eye. | rulebook l.222, l.263-264; Lee 19 Oct |
| **Names** follow the Full Build (hover names too); the servos "X Servo (Y Dot)" in both guides. | Lee 19 Oct |

### 1.4 Cameras and motion

| Convention | Date, source |
|---|---|
| **Each step is seen by the camera of the Full Build step it undoes** (the generator's default); the MRA's module out of its slots "with the Full Build's own camera for that step, much closer". | rulebook l.243; Lee 18 Oct second round |
| **Two steps on one sub-assembly in the hand keep one camera** (`keep_camera=True`); **one camera for each run on a sub-assembly on its own** (RCC: the controller, the I/O module, L5 with the motors). | Lee 18 Oct second round; RCC review fixes (a389ef4) |
| Close-in steps follow the Full Build's zoom (the MRA claw steps as close as the Full Build's; `own_frame=True` for a step framed on its own). | Lee 19 Oct |
| A cable unplugged is seen **a little wider so that the whole cable shows** (RCC Step 1). | Lee 18 Oct (RCC) |
| The part leaves **along its build hover path, reversed**; a two-stage joint is undone inside one step (small unhook or tilt first, then the long pull). | rulebook l.233-234 |
| **Removal timing**: the part slides out (800 ms a stage), then fades over a beat of its own (800 ms, cosine, starting 150 ms before the slide rests), leads with it; Prev fades it in where its way ended and slides it back. | Lee 17 Oct (with a fade), changed 18 Oct ("smoother / less abrupt, and slower"); rulebook l.326 |
| Turning the kit over is said in the caption ("Turn the car over. Slide L6 out." / "Turn the car the right way up. ..."); the Full Build's turned-over cameras (`flip`) come with the step. | RCC script |
| Lee's PMG-only exception (21 Oct): the Full Build's **Step 42 fades out and reappears** (`reappear=True`; "Let's keep the fade on 42"), because the wired module's move was "such a mess". The published take-apart moves the same harness by cross-fades too (its D4, `[014]-[016]`). | PMG README fifth and sixth rounds; rulebook section 4 |

---

## 2. Caption style of the MRA's and RCC's deconstructions

Imperative, one action (or "X, then Y"), the part named first, its place after "from / off / out of". Two voices exist:

**The in-house draft voice** (Claude's, kept in the RCC's guide and in the MRA's `deconstruction.py` source):
- *Unplug*: "Unplug the USB cable from the controller's Nano Board." "Unplug the 9V adapter's barrel plug from the power socket on the I/O module." "Unplug both wheel motors from RWh and LWh."
- *Pull ... out of / off / back out of*: "Pull the right joystick back out of R-JS, then lift it out of its pocket." "Pull both wheel motors out of L5." "Turn L1 over. Pull L3 off L2 and out of the short slots in L1."
- *Lift ... out of / off*: "Lift the radio module out of its socket." "Lift the Nano Board out of H1 and H2." "Lift L4 and L5, with the wheel motors, off L1, bringing each motor's wire up out of its notch."
- *Slide ... out / back off*: "Turn the car over. Slide L6 out." "Slide L4 back off along the motors' wires, each plug passing back through its hole in L4."
- *Swing ... then unhook*: "Swing L2 up out of its slots in L1, then unhook it from the notch at the flat end of L1."
- *Unsnap / Unscrew / Take ... out of*: "Unsnap the 9V adapter from the top of the battery." "Unscrew the two 10mm screws that hold R7 to R6." "Take the shoulder motor out of R6, angling its servo horn back out through the opening."

**TechBox's developer's voice** (the MRA's live wording since 21 Oct, `step-text-deconstruction.json`, from "MRA deconstruction step text
LO (1).csv"; the latest word on how TechBox phrases a take-apart). Part names capitalised as the parts list has them (Nano I/O Module,
Nano Board, USB Cable, Servo Extension Wire, Right Joystick), and a small verb set:
- *Remove X from Y* (by far the commonest, 45 of 73): "Remove B8 from B5, B6, and B7." "Remove the Nano Board from the Nano I/O Module."
  "Remove B6, B7, and the Right Joystick together from B3 and B4." "Remove A9 from the cross-shaped slot next to A8."
- *Disconnect X from Y* (plugs, wires): "Disconnect the USB Cable from the Nano Board." "Disconnect all eight breadboard wires from the joysticks and the Nano I/O Module."
- *Remove the N screw(s) connecting A to B[, then separate the pieces.]*: "Remove the 6mm screw connecting A12 to A10, then separate the pieces."
- *Slide X out from / off / toward ..., then lift ...*: "Slide C4 and C5 toward the bottom of C3, then lift them out of the slots." "Slide B2 out from under the servo horn."
- *Lift X over ..., then slide it out of ...*: "Lift the Nano I/O Module over the notch in B4, then slide it out of the slots in both B6 pieces."
- *Thread X out of Y* (a lead through a hole): "Thread the Claw Servo's wires out of the top square hole in A6."
- *Tilt X to guide it out of Y*: "Tilt the Elbow Servo (Black Dot) to guide it out of R5."
- Cautions (orange box): "When disconnecting the wires, pull apart the two black connectors. Do not pull on the wires themselves."
  "Carefully thread the Shoulder Servo's wires all the way out of R7." "Use the Pry Tool to carefully remove the Nano Board."

**For the PMG**, recommended: write the draft in the developer's verbs (Remove / Disconnect / Slide / Lift / Swing ... then ...),
which TechBox chose for the MRA, so less is rewritten when the developer edits it. Part names: the PMG Full Build's captions write
them in lower case ("the I/O module", "the 4-digit display", "the dot matrix display", "the black push button", "the USB cable");
the developer capitalised the MRA's to the parts-list names. Either reads; I would follow the developer (Nano I/O Module, Nano
Board, 4-Digit Display, Dot Matrix Display, Push Buttons, USB Cable, breadboard wires) since the take-apart is the MRA's sibling
document, and note it for Lee. The PMG has no developer sheet yet (no `step-text.json` in the kit).

---

## 3. The published PMG take-apart mapped onto the in-house Full Build

In-house part ids (`guide.py` l.42-49): H1 `NAUO63`, H2 `NAUO65`, H3 `NAUO66`, H4 `NAUO73`, H5 `NAUO67`, H6 `NAUO60`, H7 `NAUO68`,
H8 `NAUO61`, keys H9 `NAUO72 NAUO71 NAUO70 NAUO69` (over the black, yellow, white, blue buttons), H10 `NAUO64`, H11 `NAUO62`,
H12 `NAUO77`, H13 `NAUO75`, H14 `NAUO74`; I/O module `NAUO78`, Nano Board `NANO`; push buttons black `NAUO76`, yellow `NAUO83`,
white `NAUO84`, blue `NAUO85`; 4-digit display `NAUO79`; dot matrix display `NAUO81`; USB cable Mini-B end `NAUO282` (rides on the
module), A end `NAUO283` (rides on H1, on the table behind the case under the display's end); 42 jumper caps (`CAP_*`, `NAUO86` ...):
at the Completed View 21 ride on the module, 5 on the matrix, 4 on the display, 3 on each button. 22 leads: `black VCC` ...
`blue GND`, `4-digit display CLK` ... `GND`, `dot matrix display VCC` ... `CLK`, `usb cable`.

| Published decon | Published build undone | In-house Full Build step undone (views) | Notes |
|---|---|---|---|
| D1 H14 (tilt, then lift) | B51 | **48** (H14: tabs set on the matrix's top edge, top swung in; 5 poses) | same |
| D2 matrix off the stand, to the bench, still wired (eye; cross-fades) | B50 + B49 | **47** (hung on the hooks of H11 / H12, `path` HELD -> HALF -> 0) + **46** (picked up, carried over the case, `ride` UP, OVER, HELD, `ride_beats`; the USB cable moved out over its wires) | 46 is a ride: not in `take_apart()`'s record of moves |
| D3 display off the stand, to the bench, still wired (eye; cross-fades) | B48 + B47 | **45** (lowered into the notches of H11 / H12) + **44** (under the matrix's wires, up behind the case, over, held: `ride` UNDER, UP, OVER, HELD, `ride_beats`) | 44 is a ride |
| D4 shield + everything on it out of its slot, to the bench (arrow; cross-fades) | B46 + B45 | **43** (lowered onto the back of H4, `path` HELD -> 0, 102.3 mm) + **42** (bench -> held over H4: **a fade and reappear**, Lee's exception; the A end laid behind the case) | 42 records no motion (`reappear`) |
| D5 H13 | B44 | **41** | |
| D6 H12 | B43 | **40** | each from its own front corner (Lee's first round) |
| D7 H11 | B42 | **39** | |
| D8 H10 (lift front, pull forward) | B41 + B40 | **38** (one step, 3 stops) | |
| D9 four keys at once (one arrow) | B39 + B38 | **37** (three) + **36** (one) | Lee's group ask |
| D10 H8 | B37 | **35** | |
| D11 (turned over) H7 | B36 + B35 | **34** (turned over, hook and swing) | |
| D12 four buttons out at once, to the bench, still wired (eye only) | B34 + B33 | **33** (three) + **32** (blue; "bring the electronics back beside the case") | Lee's group ask |
| D13 H6 | B32 + B31 | **31** (turned over) | |
| D14 H5 | B30 + B29 | **30** (turned over) | |
| D15 (upright) H4 | B28 | **29** | |
| D16 H1 (H2, H3 never removed; they vanish at D17) | B27 + B26 | **28** (H3), **27** (H2 onto H1, H1 the datum, never moved) | in-house: H3, H2 off, **H1 left** |
| D17 matrix board off its 5 wires | B20-24 (part) | 21 - 25 | bench, one fixed view |
| D18 the 5 matrix wires off the shield | B20-24 | 21 - 25 | |
| D19 USB cable | B25 | **26** (+ the A end's move in 42) | |
| D20 the 4 buttons off their 12 wires (one arrow) | B3-14 (part) | 4 - 15 | |
| D21 display off its 4 wires | B16-19 (part) | 17 - 20 | |
| D22 the 16 remaining wires (2 arrows) | B3-14, B16-19 | 4 - 15, 17 - 20 | |
| D23 Nano (zoomed) -> Completed View: bare shield | B1 | **1** | |
| (none) | B2, B15 (peel ribbons) | **2, 16** (peel), **3** (push-button card) | no counterpart (preparation, card) |

Where the in-house Full Build differs from the published one, and what it means for the take-apart:
- **Step 42 is a fade** (`reappear=True`, `STEP42_REAPPEAR = True` in `guide.py` l.1158): the steps file records no way from the bench
  to MODULE_HELD, only the two end states (Step 42's wires = the bench shapes, Step 42c's = held over H4). Round 4's five-beat way
  (`WAY_42`) exists only inside `guide.py`, with 104 contacts in its first two beats. **`_takeoff()` (remove / unplug / lift) has no
  `reappear` option** (stepgen.py l.947-951; `place()` has it, l.1223), so the module's way back to the bench needs either that
  option added to `lift()` (generator; the player already plays `reappear`), or a hand path with the contacts Lee rejected.
- **Steps 42, 44, 46 move by `ride`**, `moving` is `[]`: `take_apart()` records only steps with `moving` (stepgen.py l.849), so the
  default `lift()` of the module, display and matrix reverses only Steps 43, 45, 47 (to MODULE_HELD / DISPLAY_HELD / MATRIX_HELD).
  The rest of the way back must be given by hand from the Full Build's own record, as the MRA's `walked_back()` does
  (`MRA .../deconstruction.py` l.68-81): Step 44c `carry[NAUO79].via` (3 poses) and Step 46c `carry[NAUO81].via` (2), their
  `wire_via` (4 and 5 leads), Step 44's / 46's start `carry` pose (the bench) and `wires`. Step 45c / 47c `wire_via` hold the half-way
  shapes of the lowering.
- **The USB cable**: plugged at Step 26 on the bench; its A end carried behind the case in Step 42 (now under the 4-digit display's
  header end, `NAUO283` riding on H1); moved out over the matrix's wires in Step 46 (`usb_outside()`).
- **The I/O module goes on H4 USB end up** (published way; the STEP has it down): the take-apart follows the Full Build.
- **Wiring order** is the published one: buttons (4 - 15: black, yellow, white, blue, VCC / OUT / GND each), display (17 - 20), matrix
  (21 - 25), USB (26). The in-house extras (Step 3's one-view card, the close-ups on 17c - 25c, Step 33c's colour labels) have no
  counterpart.
- **The case**: in-house Step 27 moves only H2 (H1 is shown, never moved: the datum); the published B26 put both down. The published
  take-apart never removes H2 and H3 (a slip: they vanish at the scene switch). The in-house one can take H4, H3, H2 off and end on H1.
- **Turned over**: in-house Steps 30, 31, 34 use `FLOOR_CAMERA` (flip), 32 - 33 `BUTTONS_IN` (flip); the take-apart's steps undoing
  them inherit the turn from the Full Build's camera. The bench electronics beside the case are turned with it (as in the Full
  Build's 32 - 34 and the published `[032]-[036]`).

---

## 4. Proposed step list (21 steps; 21 / 48 = 0.44, at the bottom of the rulebook's 0.45 - 0.82; the published PMG's is 23 / 51 = 0.45)

Captions in the developer's voice (section 2). "Undoes" = in-house Full Build step(s). Cameras: the Full Build's for the step undone
unless said. Arrows sized to the part (15 - 40 mm), an arrow on each part of a group (Lee's precedent).

| # | Caption (draft) | Undoes | How (generator) |
|---|---|---|---|
| 1 | Disconnect the USB Cable from the Nano Board. | 26 (+ A end of 42) | `remove([NAUO282, NAUO283], units=[[NAUO282]])`: one arrow on the Mini-B plug, clear of the cable (RCC rule), none on the A end; the A end needs a `paths=` way **out from under the display's end, then up** (its first free way could run into the display). Camera: Step 43's corner (sees the plug at the module's top) framed a little wider so the cable and A end show (RCC rule), or Step 42's straight-behind view. |
| 2 | Swing the top of H14 out, then lift its two bottom tabs off the top edge of the Dot Matrix Display. | 48 | `remove([H14])`: the Full Build's 5 poses reversed. Step 48's camera. |
| 3 | Lift the Dot Matrix Display off the hooks of H11 and H12, then carry it back over the case and set it on the table behind it. Leave its wires connected. | 47 + 46 | `lift([NAUO81], path=..., wire_via=..., wires=...)`: Step 47's path reversed (0 -> HALF -> HELD) then Step 46's ride reversed (HELD -> OVER -> UP -> bench), its 5 leads stage by stage from Steps 47c / 46c `wire_via` and Step 46's start `wires`; the `usb cable` keys dropped (removed in step 1). Arrow on the matrix along stage 0 (off the hooks: `arrow_style={NAUO81: dict(stage=0)}`), as the RCC's joysticks. Step 47's camera; Step 46's frames the carry (check the end pose is in frame). |
| 4 | Lift the 4-Digit Display out of the notches in H11 and H12, then carry it back over the case, down behind the I/O Module and out under the Dot Matrix Display's wires to the table. Leave its wires connected. | 45 + 44 | as 3: Step 45's path reversed, then Step 44's ride (HELD -> OVER -> UP -> UNDER -> bench), 4 leads from 45c / 44c `wire_via`. Arrow along stage 0 (out of the notches). Step 45's camera is close (radius 70) and from the front: Step 44's (from behind, radius 102) shows the carry; choose by what stays in frame. |
| 5 | Lift the Nano I/O Module off the back of H4 and set it on the table behind the case, with everything still plugged into it. | 43 + 42 | `lift([NAUO78])`: Step 43 reversed (up 102 mm, an arrow along it), then **a fade and reappear** from MODULE_HELD to the bench pose (Step 42's start `carry`), wires to Step 42's start `wires` (the bench shapes, buttons still in the case). Needs `reappear=` on `lift()` (section 3). Step 43's camera. |
| 6 | Slide H13 up its slope and out from between H11 and H12. | 41 | `remove([H13])` |
| 7 | Slide H12 forward out of H4, then lift it out of the slot in H10. | 40 | `remove([H12])`: its own front corner, as Lee set in the build |
| 8 | Slide H11 forward out of H4, then lift it out of the slot in H10. | 39 | `remove([H11])` |
| 9 | Lift the front of H10 off H2 and H3, then pull its rear tabs out of the slots in H4. | 38 | `remove([H10])`: 3 stops reversed. KEY_CAMERA. |
| 10 | Slide all four piano keys (H9) out through H8 toward the front. | 37 + 36 | `remove(KEYS, units=[[k] for k in KEYS])`: an arrow on each (default would give 2: Step 36's one, Step 37's three); the generator notes 4 arrows. KEY_CAMERA (= step 9's: one camera). |
| 11 | Lift H8 out of the slots in H5. | 35 | `remove([H8])` |
| 12 | Turn the case over. Swing H7 up out of the notches in H3, then unhook its tabs from the windows in H2. | 34 | `remove([H7])`: hinge reversed (4 beats). FLOOR_CAMERA (flip). |
| 13 | Lift all four push buttons out of their pockets in H6 and set them on the table beside the Nano I/O Module. Leave their wires connected. | 33 + 32 | `lift(BUTTONS, units=[[b] for b in BUTTONS], wires={12 button leads: Step 32's start routes})`: each its own Full Build way reversed (blue from 32, the others from 33), all four at once; an arrow each along stage 0 (out of the pocket). BUTTONS_IN (flip). **Check with motioncheck.py**: in the build the blue went in on its own before the others. |
| 14 | Disconnect all 21 breadboard wires from the Push Buttons, the 4-Digit Display, the Dot Matrix Display and the Nano I/O Module. *Caution:* Pull each wire off by its black connector. Do not pull on the wires themselves. | 4 - 15, 17 - 25 | `remove(JUMPER_CAPS, arrows=[], eye=[...])`, `alone=` the harness (module, Nano, buttons, displays, caps): both ends at once, as the MRA's Step 53; an eye on the middle cap at the module, the matrix, the display and the middle button (4 eyes; the MRA's had 3). A new camera framing the whole bench layout, from the published bench side (the direction of in-house Step 26, `[0.922, 0.387, 0.005]`, wider), kept for 14 - 16. |
| 15 | Remove the Push Buttons, the 4-Digit Display and the Dot Matrix Display. | (3, 17, 21: the parts brought in) | `remove(BUTTONS + [NAUO79, NAUO81], alone=..., keep_camera=True)`: an arrow on each (6: the generator notes it), or one per kind (`units=[BUTTONS, [NAUO79], [NAUO81]]`, as the published one arrow for four buttons). |
| 16 | Remove the Nano Board from the Nano I/O Module. *Caution (the MRA developer's):* Use the Pry Tool to carefully remove the Nano Board (only if the PMG kit has the Pry Tool: ask). | 1 | `remove([NANO], alone=[NAUO78, NANO], keep_camera=True)` (or punched in, as the published D23 and the MRA's Step 55); then `g.put_away([NAUO78])`. |
| 17 | Swing H6 up out of the notches in H3, then unhook its tabs from the windows in H2. | 31 | `remove([H6])`: FLOOR_CAMERA (flip): the case is still upside down. The view starts afresh after the put-away. |
| 18 | Swing H5 up out of the notches in H3, then unhook its tabs from the windows in H2. | 30 | `remove([H5])`, FLOOR_CAMERA |
| 19 | Turn the case the right way up. Pull H4 off the back tabs of H2 and H3. | 29 | `remove([H4])` (65 mm along +x) |
| 20 | Pull H3 off the end of H1. | 28 | `remove([H3])` |
| 21 | Pull H2 off the other end of H1. | 27 | `remove([H2])` |
| - | Completed View: H1 alone, closer in; then the Full Build's two Parts List pages (`parts_list_at_end=True`). | | |

(21 numbered steps as listed; with the USB cable on the bench instead, as published, 21 too; with the wires in three bundles
(choice C, below), 23.)

Set-up, as the MRA's and RCC's: `Guide(HERE, title='Piano Memory Game (PMG)', part='Deconstruction', names=dict(FULL['names']),
steps_file='steps-deconstruction.json', source='pmg-guide.glb', hover_names=<guide.py's HOVER_NAMES: the buttons by colour>,
copyright_line=...)`, `g.take_apart(parts_list_at_end=True)`; a `guides.json` entry `"piano-memory-game-deconstruction": {"kit":
"piano-memory-game", "steps": "steps-deconstruction.json", "label": "Deconstruction", "script": "deconstruction.py"}` before any
publish (then `site_pages.py` writes its framing rule); its card is the Full Build's (`cards/steps.webp` exists).

---

## 5. Open choices, with a recommendation each

**A. Where the harness is taken apart, and where the guide ends.**
- (A1, recommended) **As soon as it is out of the case** (after the buttons, step 13), on its own (`alone=`), then back to the case,
  which comes apart down to **H1**. Reasons: both in-house take-aparts end on the first part of the build, the base (R1, L1), and
  Lee's MRA round moved the electronics before the housing to get there; Lee's RCC rule "taken apart on its own ... then the guide
  returns to the main model" fits exactly; and H6 / H5 are then seen as the Full Build saw them, wood only (the build put the
  electronics away for Steps 27 - 31), instead of beside the turned-over case upside down in mid-air (the published `[032]-[036]`).
- (A2) As published and as the strict reverse: the case first, the bench last, ending on the bare I/O module (what Lee first asked
  for the MRA's Completed View, before the first round). Then H1 must be removed too (or put away), which no in-house take-apart has done.

**B. Electronics lifted off still wired (published, reverse) or unplugged where they are (the MRA's "where they are").**
- (B1, recommended) **Lifted off still wired**, matrix, display, module, in that order (steps 3 - 5): the Full Build's own poses and
  wire shapes walked back (every shape on the way was routed and checked in Lee's rounds), the published order, and the rulebook's
  "wired modules are lifted off the housing first, still wired". Unplugging in the case is not practical: the matrix's header faces
  H11 / H12 as it hangs, the display sits between them, and the buttons' far ends are inside the case under H7, so their 12 wires
  could only come off the module end and dangle from inside the case (new routes for 12 leads).
- The module's way back (undoing Step 42): **a fade and reappear** (recommended: Lee's own choice for this move; the published
  take-apart cross-fades the same harness) needs `reappear` added to `lift()`. Without it, a hand path re-creates the motion Lee
  rejected (round 4: 104 contacts; fewer once the USB cable is gone, but the button bundles' 54 passings remain).

**C. The bench: how the wires come off.**
- (C1, recommended) **All 21 at once, both ends** (one step, an eye per group of ends), then the devices off in one step. Reasons:
  Lee's own example "the breadboard wires" names them as one group, as the MRA's eight at once (Step 53, published r1 / r2); the
  generator does it (`remove(caps)`: a lead whose both ends go goes too).
- (C2) **Per device bundle** (matrix 5, display 4, buttons 12): three steps, two eyes each (the rulebook's "two at most" and its
  section-13 default "per module bundle"). Choose this if four eyes crowd the bench view.
- (C3) **The published phasing, device off its wires, then the wires off the module** (Lee's second MRA option, "the joysticks pulled
  off the wires, then the wires off the module"). **Not possible as is**: a device's caps ride on it, so `remove(device)` takes them
  along and leaves its leads' module ends with nothing at the other end, which `_takeoff()` refuses (stepgen.py l.1110-1112). It
  would need the device's caps moved onto the module between steps (`g.carry(caps, by=NAUO78, pose=...)`: untried in a take-apart)
  or a generator option.

**D. The USB cable: first (recommended) or on the bench (published D19).** First: power off before anything is handled, as the MRA
(Step 4) and the RCC (Step 1) have it; and it takes the cable out of the two reversals where the Full Build had the most trouble with
it (Step 42's hairpins and folds; Step 46's cable moved out over the matrix's wires). Cost: one step from its own camera at the
module's top on H4, the A end slid out from under the display's end.

**E. Groups.** Four keys in one step (step 10) and four buttons out of the case in one step (step 13), each part with its own arrow
(Lee's precedent: the six base screws, the two wheel motors), as Lee asked. **H11 and H12** (a mirrored pair, different codes, each
seen from its own corner by Lee's first-round cameras): recommended **two steps**, as the build and the published take-apart; together
is possible (each its own way) with one new camera if Lee wants fewer steps. **H2 and H3** likewise two steps (recommended), each its
Full Build camera.

**F. Labels.** None (published; MRA except its Row labels). Step 33c's colour labels are not needed when all four buttons go at once.

**G. Parts list at the end.** Recommended `parts_list_at_end=True`: the latest instruction (Lee with the curriculum director, 19 Oct,
for the MRA) and "same principles as the MRA". The RCC's has none (made a day earlier): worth asking whether it should get one too.

**H. The arrows on the lifted displays and module.** Arrows (in-house lifts of wired parts use them: the RCC's battery and module, the
MRA's module), along the first stage (off the hooks, out of the notches, off H4), not the long carry; the published used eyes there.

**I. Captions' part names.** Developer's capitalised names (section 2), noted for Lee.

## 6. Points for the generator and checks

- `lift()` / `_takeoff()`: add `reappear=` (for step 5), passed through as `place()` does (`common['reappear']`, stepgen.py l.1895).
- A `walked_back()`-style helper for a whole module (stops = Step N `carry` pose, Step Nc `carry.via`, Step Nc `carry` pose; leads
  from Step Nc `wire_via` + `wires`), prefixed by the reversed `path` of the lowering step (45, 47), without `ride_on` (the part rests
  on the bench afterwards, as the Full Build's H1-riding did). The MRA's helper asserts each lead has 2 or len(stops) routes.
- `lift(BUTTONS)` without `ride_on=` makes the last three ride on the first afterwards ("go as one"): harmless here (all go in step 15).
- After step 1 the `usb cable` lead is gone: drop it from every `wires=` / `wire_via=` taken from Steps 42 - 47.
- Check with `tools/motioncheck.py <kit> steps-deconstruction.json` (step 5 is skipped if it is a reappear) and `_runthrough()` on
  `player.html?steps=steps-deconstruction.json`; the four buttons coming out together and the display's way under the matrix's wires
  are the motions to watch.
- Stale docs noticed: the RCC's take-apart has **20** steps (both wheel motors unplugged in one step, both out of L5 in one step,
  commit c9761ce); `CLAUDE.md` l.381 and the RCC README still say 22.
