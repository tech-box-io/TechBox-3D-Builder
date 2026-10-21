LAC Build Instructions (LCD Alarm Clock, Full Build: the electronics on the breadboard, wired one wire at a time, then the box)

FIRST DRAFT 19 Oct 2026 (F2, F5 and F6 added the same day, from Lee's STEPs); LEE'S FIRST ROUND 20 Oct 2026 (below). Build instructions generated from the engineer's STEP (LAC Full Build.STEP) and TechBox's published Cadasio
guide for the kit (instructions.online/?id=19075-lac_full_build), in the same format and with the same player as the MRA and RCC
guides (player/ was not changed). Not for distribution. Open questions are yellow Review notes on their steps (Step 45) and
under QUESTIONS FOR LEE below.

HOW TO OPEN (Mac)
1. Double-click "Open Prototype.command". A Terminal window opens and the guide opens in your browser (port 8793, so it can run
   beside the MRA's 8791, the PMG's 8792 and the RCC's 8796). If macOS says it cannot be opened: System Settings > Privacy & Security >
   "Open Anyway".
2. When you are done, close the Terminal window. No internet connection is needed.
The controls are the MRA guide's: arrows step through, drag to rotate, scroll to zoom, Option-click a spot to copy where it is, the
grid button shows every step, ?review=0 hides the Review notes.

THE BUILD (56 steps, as numbered here. Steps 1 - 45 have the published numbers: Step 29 here lays F1 face down where the published
Step 29 turns the knob (question 2), and Step 45 here is the published Steps 45 and 46, F9 (question 4). From Step 46 on, Step N here
is the published Step N + 1.)
- Steps 1 - 7, the breadboard: its backing peeled off (it slides away below), stuck onto F3 (rails along F3's engraved edge); the Nano
  Board into rows c and g, columns 1 - 15 (c15, g1 labelled, as published); both 12 kΩ resistors shown with their legs straight, then
  bent (Step 4, 4c: the legs are drawn as wires, as the LSM's); each resistor from the (-) blue rail to h27, h29 (its lead lines from
  the leg tips Lee gave); the real time clock module into j19 - j24, its coin cell to the back. The camera close on the holes.
- Steps 8 - 14, the six-wire ribbon peeled apart in front of the board, then one wire per step, both ends at once, as published:
  black i23 - (+) red, green (-) blue - i24, purple a8 - i22, blue a9 - i21, white a14 - (-) blue, dark red a12 - (+) red. Once peeled
  apart the wires leave the table (as the LSM's), and each step opens on its wire held upright over its two holes, then pushes it in
  (one beat), the wire arching as the CAD has it; the camera close on the holes each wire goes into, and for a wire whose hole another
  hides from there (dark red's (+) red; orange's i27 and yellow's i29, Steps 20 - 21) from the nearest direction that shows both holes.
- Steps 15 - 21, the rocker switch pushed into F4 (F4 lying behind the base, raised, as the CAD has it; the camera close on it), its
  leads red j27, tan (+) red, black j29 (each cap held over its hole and pushed in, the camera on the holes with the switch in view);
  the two-wire ribbon, orange j1 - i27, yellow j3 - i29.
- Steps 22 - 32, the potentiometer: knob, nut and washer off (an arrow each along the shaft, the knob's from its face, the nut's and the
  washer's from the shaft's tip; the nut spun off counter-clockwise,
  two turns, as the LSM's), through F1's hole from the back, its little tab in the small slot beside the hole (a close-up on Step 25c,
  as published), washer, nut (spun on clockwise) and knob back on (a lead line each); F1 tipped forward, face down, in front of the
  breadboard's end (one smooth move; a step the published guide does without: F1 is first held upright in front of the board); its
  leads red (+) red, tan a5, black (-) blue.
- Steps 33 - 40, the buzzer laid beside the base, red j4 (brought in low, under the yellow jumper's arch), black (-) blue; the LCD screen
  laid face down beside the base and the four-wire male-female ribbon peeled apart, near the holes, female ends towards the LCD; GND
  (-) blue, VCC (+) red, SDA b8, SCL b9 (each wire's female end onto its pin, the wire running into the cap, and its male end into the
  breadboard in one step; each wire runs from the breadboard over the jumpers and round where F9 will stand, as it will once the LCD is
  in, then in a lane of its own to its pin; SDA's step seen from further round, where b8 shows; b9 shows from nowhere in front, so
  Step 39c has a close-up from above of the blue wire's pin in it); the USB cable's right-angle end into the Nano Board (it hovers and plugs, as decided for the MRA),
  the cable lying straight out behind the base to its A end, along the line on which F2's slit will come in (Step 55).
- Steps 41 - 53, the box: the two F7s into F3; their tops spread apart (arrows; they are not lifted), the buzzer lifted, carried over
  and lowered in between (its leads follow, a shape for each stop), let go; F9; F1 moved, still face down, further out in front and
  along to the F7s' end (as published, Step 47: out of the LCD's way; its leads then run between the F7s and F8); F4 lifted over the
  frame (the switch's leads follow) and lowered onto the tabs of the F7s and F9 (four lead lines, from the tab tops Lee gave); F8 slid
  in from the front; the LCD lifted off the table and slid out in front, stood up face to the front 40 mm out, and moved in until the
  end of its board is in F8's notch, the other end angled 14 degrees out in front of F9 (the published pose, without its 2.14 mm lift,
  which put the LCD into F4); then straightened, pushed 14.9 mm on through F8's notch and slid back into F9's notches (a close-up of
  them); its wires stay behind F9 all the way (the run round F9's back edge held still); F1 stood up in front of the box and pushed onto
  the tabs of F4 and F3 (Lee's lead line at F4's front tab).
- Steps 54 - 56, the ends and the back, as published: F5 pushed onto the breadboard's end, the tabs of F1, F3 and F4 into its slots (six
  lead lines, two of them at F4's tabs as Lee gave them; seen low from the front as published, so that F5 does not hide them); F2, the case seen from behind: brought in swung out,
  the tabs at its slit end hooked into F5's slots, and swung shut onto the tabs of F3 and F4, its slit (open at the bottom) sliding along
  the USB cable, the cable following it (a Caution: the cable must sit in the slit; an eye on the cable in the slit, and a close-up of it
  on Step 55c); F6 onto the other end, which locks them all. The Completed View is the closed box. Unlike the published Step 56, the
  case stays upright (published: laid on its front, F2 lowered from above; the player can turn a model only upside down), and F2 comes
  in 40 mm straight from behind and then 14 mm along itself (published: about 80 mm, diagonally from behind and F6's end), so that its
  slit slides along the cable lying straight out behind the case.
- Checked (20 Oct 2026): the player's run-through check passes on every view (116 views, forwards, backwards and jumping, 0 problems);
  at rest each wire is clear of the parts and of the other wires (tools/wirecheck.py: 3 touches of 0.03 - 0.05 mm, a jumper's cap held
  over its hole beside the wire before it, Steps 12 - 14); during the moves (tools/motioncheck.py, every move at 19
  moments) no wire passes into a panel any more: 13 moments where a plug going down brushes the wire beside it by 0.2 - 0.9 mm
  (Steps 12 - 14, 33, 36 - 39), one where the buzzer's red lead grazes the clock module's edge by 0.7 mm as the buzzer is carried
  over (Step 43, its second beat), and 49 where two wires brush for a moment inside the bundle (most as a lead's run in the case
  changes, Steps 46 and 52); before the round, 132 moments, some a lead through a 3 mm panel, and the check did not see the parts
  that swung off the screen.

LEE'S FIRST ROUND (20 Oct 2026)
- The 12 kΩ resistor is named so everywhere (the parts list, labels, captions; "2x - 12 kΩ Resistor" on Step 4).
- Colours: the knob's silver ring and the resistor's bands, the breadboard's legends, the USB plug's and the switch's marks are TechBox's
  Cadasio face copies laid 0.02 mm over the body; the body under them now takes their colour, so the black no longer shows through
  (colour-atlas-lac.json: "skin"). The potentiometer is pictured from its knob side in the parts list.
- Cameras closer on what each step puts in (Steps 3 - 7, 9 - 18, 20 - 34, 36 - 41, 45, 50), labels moved off the parts and their
  leaders apart (Steps 1, 3 - 7, 15, 22, 33, 34); lead lines where Lee gave them (Steps 5, 6, 48, 53, 54). Steps Lee did not name whose
  camera changed: 26 and 28 share Steps 25 and 27's camera on F1 and the potentiometer (framed as before; the base behind them sits
  differently, as F1 is held where Step 29 now lays it down); Step 46 is a new move. Step 35's is as it was. Step 40's close camera
  leaves the USB cable's A end off the screen (it is back in Step 41).
- The moves: no part is turned about a far-off point any more (the buzzer's caps and the buzzer swung off the screen: Steps 33, 34,
  43); each lead has a shape for each stop of a move; the potentiometer's, the buzzer's and the LCD's wires are drawn from the
  breadboard, so that the run in the case is held still where both shapes share it: the LCD's round F9's back edge in every shape
  (Steps 36 - 51), the potentiometer's as F1 is pushed on (Step 53: it dipped into F8), the buzzer's through the jumpers as it is
  lowered onto its seat (Step 43, its last beat). The buzzer's leads turn out of the buzzer and into their holes over several mm (they
  had hairpins there). tools/motioncheck.py now turns a part between two poses as the player does (it turned every part about its
  middle, so it did not see those swings).
- An independent review (three reviewers, each finding checked by a fourth: docs/research/lac/round1/review.md) found the rest of the
  above: holes still hidden from their step's camera (14, 20, 21, 38, 39), the jumpers and Step 33's red cap gliding in from off the
  frame, the LCD ribbon's two ends crossing as each wire was connected, the LCD wires' run lifting through the jumpers in Step 50.
- Research for the round: docs/research/lac/round1/ (how the LSM does what Lee asked for, the published guide's moves and cameras, the
  model's colour faults, why the wires misbehaved mid-move).

REUSED FROM THE MRA AND RCC (Lee, 19 Oct 2026: "replacing each item in the LAC file with the version you used on either the MRA or RCC")
- The Nano Board: the LAC's NAUO124 is the same Nano model as the MRA's; the guide shows the MRA's export of it (nano-mra.glb, cut by
  tools/cut_part.py to sit exactly where NAUO124 is), coloured by the MRA's atlas, as the RCC's two Nano Boards are.
- The USB cable's A end: the MRA's usb-a-end.glb (the LAC's NAUO121 is the same model, fitted vertex for vertex), with the MRA's colours.
- The female Dupont caps (the LCD wires' ends) are the MRA's breadboard-wire caps already.
- Not reused: the USB cable's Mini-B end, which on the LAC is a right-angle plug (the MRA's and RCC's are straight): the LAC's own.
- Everything else is coloured from TechBox's own published LAC Cadasio project, solid by solid (colour-atlas-lac.json).

WHAT WAS DONE WITH THE STEP
- The export carries most parts several times, once for each pose (four F1 / potentiometer sets, three switches, three LCDs, two buzzers,
  every wire in two or three poses). The guide shows each part once, seated, and moves it; the poses between the copies were measured
  (all fit to 0.0000 mm) and are used for where things lie on the way (F1 face down beside the base and face up at the far end, F4
  beside the base and over the frame, the buzzer and the LCD lying beside the base, the LCD short of F9's notches).
- trim_source.py cuts lac.glb (55 MB, 159 instances) down to the 52 the guide uses (lac-guide.glb, 7.4 MB). Run it again after
  replacing the STEP (python tools/step_to_glb.py "LAC Build Instructions/LAC Full Build.STEP" "LAC Build Instructions/lac.glb").
- F4 seated is not in the STEP (only F4 lying beside the base): it is that panel moved by the same move as the switch's two copies
  (extra part F4, f4.glb).
- F2, F5 and F6 come from Lee's STEP files of their own (F2.STEP, F5.STEP, F6.STEP, 19 Oct 2026), converted by tools/step_to_glb.py to
  f2.glb, f5.glb, f6.glb and placed where TechBox's published Cadasio project has them (its scene is this assembly scaled by 0.6055,
  fitted on six parts to 0.0006 mm; the part frames are the same): every tab meets its slot.
- Broken copies left out: the LCD lying face down (no display in it), a second coin cell beside the first, the dark red jumper wire
  ending in a14 beside the white one (the published guide has a12: the guide uses a12).
- The wires are drawn by the player along the CAD's centre lines (wire-paths.json; docs/research/lac/cad_study.md); where the STEP has
  no wire for a pose (the switch's leads with F4 beside the base, the potentiometer's with F1 beside the base, in front and seated) the
  guide draws a smooth one. Their lengths are representative, as the RCC's are. Where a wire touched a part or another wire, it was
  re-routed: the switch's leads (beside the base and seated), the potentiometer's (lying beside the base, over the buzzer and the LCD
  and past F9's end; stood up in front of the case; seated), the dark red jumper (a low arch) and the USB cable (through F2's slit). The
  seated leads, in the closed case, were found by a path search and are kept in guide.py as control points.

QUESTIONS FOR LEE
1. Section cards: the published guide has five unnumbered cards (Real Time Clock, Rocker Switch, Alarm Buzzer, LCD Screen with a photo of
   its pins, USB Cable). The MRA and RCC guides name each part with a label on its first step instead, which this draft does. Add the cards?
2. The published Step 29 turns the knob to point at about 7 o'clock (a check, with only an eye). I left it out: what is it for?
3. (Answered: the resistors' legs are now shown straight, then bent, as on the LSM.)
4. Step 45 (Review note): F9 goes straight down into its slots in the CAD; the published guide hooks it in tilted and then stands it up.
5. The right-angle USB plug is the LAC's own (the MRA's and RCC's are straight): is that the cable in the kit?
6. The jumper wires change length between lying loose and plugged in (the CAD routes them 50 - 90 mm); fine, as for the RCC's leads?
7. When it is ready for the website: its address would be lcd-alarm-clock-full-build (kit lcd-alarm-clock), added to guides.json then.
8. (Done in your first round: see above.)
9. The potentiometer's knob: TechBox's Cadasio project draws a silver ring round the end of the knob (and a silver pointer groove), so
   the guide keeps it and only stops the black showing through. If the real knob is all black, it is a one-line change to make it so.

FILES
  guide.py                      the build, in order (run it after any change: python "LAC Build Instructions/guide.py")
  materials.json                colours and detail; colour-atlas-lac.json its per-solid colours
  wire-paths.json               the breadboard's holes, the caps, every CAD wire's centre line, the poses between the CAD's copies
  trim_source.py                lac.glb -> lac-guide.glb (the parts the guide uses)
  lac.glb, lac-guide.glb        the CAD (converted from LAC Full Build.STEP), and cut down
  nano-mra.glb, usb-a-end.glb   the MRA's Nano Board and USB A end; f4.glb the top panel (extra parts)
  f2.glb, f5.glb, f6.glb        the back and end panels, from Lee's F2.STEP, F5.STEP, F6.STEP (extra parts; the STEPs stay out of git,
                                their checksums in cad-sources.sha256)
  steps.json, parts.json, model.glb, model.report.json, parts/   generated; do not edit by hand
  logo.webp                     the title page's logo (the RCC's)
  Research: docs/research/lac/ (cad_study.md; cadasio/ the published guide's data and step pictures; scripts/).
