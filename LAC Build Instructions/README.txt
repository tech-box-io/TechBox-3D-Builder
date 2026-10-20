LAC Build Instructions (LCD Alarm Clock, Full Build: the electronics on the breadboard, wired one wire at a time, then the box)

FIRST DRAFT 19 Oct 2026 (F2, F5 and F6 added the same day, from Lee's STEPs). Build instructions generated from the engineer's STEP (LAC Full Build.STEP) and TechBox's published Cadasio
guide for the kit (instructions.online/?id=19075-lac_full_build), in the same format and with the same player as the MRA and RCC
guides (player/ was not changed). Not for distribution. Open questions are yellow Review notes on their steps (Steps 4 and 45) and
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
  Board into rows c and g, columns 1 - 15 (c15, g1 labelled, as published); both resistors' legs bent (one view, Review note); each
  resistor from the (-) blue rail to h27, h29; the real time clock module into j19 - j24, its coin cell to the back.
- Steps 8 - 14, the six-wire ribbon peeled apart in front of the board, then one wire per step, both ends at once, as published:
  black i23 - (+) red, green (-) blue - i24, purple a8 - i22, blue a9 - i21, white a14 - (-) blue, dark red a12 - (+) red. Each wire is
  picked up from where it lies, its caps turned upright over their holes and pushed in (two beats), the wire arching as the CAD has it.
- Steps 15 - 21, the rocker switch pushed into F4 (F4 lying behind the base, raised, as the CAD has it; the camera close on it), its
  leads red j27, tan (+) red, black j29; the two-wire ribbon, orange j1 - i27, yellow j3 - i29.
- Steps 22 - 32, the potentiometer: knob, nut and washer off (an arrow each, they slide off along the shaft), through F1's hole from
  the back, washer, nut and knob back on (a lead line each); F1 laid face down beside the base (a step the published guide does
  without: F1 is first held upright in front of the board); its leads red (+) red, tan a5, black (-) blue.
- Steps 33 - 40, the buzzer laid beside the base, red j4, black (-) blue; the LCD screen laid face down beside the base and the four-wire
  male-female ribbon peeled apart; GND (-) blue, VCC (+) red, SDA b8, SCL b9 (each wire's female end onto its pin and its male end
  into the breadboard in one step); the USB cable's right-angle end into the Nano Board (it hovers and plugs, as decided for the MRA),
  the cable lying straight out behind the base to its A end, along the line on which F2's slit will come in (Step 55).
- Steps 41 - 53, the box: the two F7s into F3; spread apart (arrows), the buzzer lowered in between (its leads follow), let go; F9;
  F1 carried round to the far end and laid face up; F4 lifted over the frame (the switch's leads follow) and lowered onto the tabs
  of the F7s and F9 (four lead lines, from F4's slots to the tab tops); F8 slid in from the front; the LCD stood up and brought in,
  then slid into F9's notches; F1 stood up in front of the box and pushed onto the tabs of F4 and F3.
- Steps 54 - 56, the ends and the back, as published: F5 pushed onto the breadboard's end, the tabs of F1, F3 and F4 into its slots (four
  lead lines, seen low from the front as published, so that F5 does not hide them); F2, the case seen from behind: brought in swung out,
  the tabs at its slit end hooked into F5's slots, and swung shut onto the tabs of F3 and F4, its slit (open at the bottom) sliding along
  the USB cable, the cable following it (a Caution: the cable must sit in the slit; an eye on the cable in the slit, and a close-up of it
  on Step 55c); F6 onto the other end, which locks them all. The Completed View is the closed box. Unlike the published Step 56, the
  case stays upright (published: laid on its front, F2 lowered from above; the player can turn a model only upside down), and F2 comes
  in 40 mm straight from behind and then 14 mm along itself (published: about 80 mm, diagonally from behind and F6's end), so that its
  slit slides along the cable lying straight out behind the case.
- Checked: the player's run-through check passes on every view (115 views, forwards, backwards and jumping, 0 problems); in every view
  each wire is clear of the parts and of the other wires (tools/wirecheck.py, 0 problems; 488 before this round's re-routing).

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
3. Step 4 (Review note): the player cannot swap the straight-legged resistor for the bent one, so the step shows the bent legs only.
4. Step 45 (Review note): F9 goes straight down into its slots in the CAD; the published guide hooks it in tilted and then stands it up.
5. The right-angle USB plug is the LAC's own (the MRA's and RCC's are straight): is that the cable in the kit?
6. The jumper wires change length between lying loose and plugged in (the CAD routes them 50 - 90 mm); fine, as for the RCC's leads?
7. When it is ready for the website: its address would be lcd-alarm-clock-full-build (kit lcd-alarm-clock), added to guides.json then.
8. Wires during the moves: at rest every wire is clear, but part-way through some moves a lead still passes briefly through a part or
   another wire (tools/motioncheck.py: 132 moments in 89 moves). The deepest, a lead through a 3 mm panel: F1 laid down (Step 29), the
   buzzer lifted through the potentiometer's leads (43), F1 carried round (46), the LCD stood up (50), F1 stood up and pushed on (52,
   53); the rest are jumpers and leads crossing for a moment as each is plugged in. A clean-up pass (a shape for each lead at each beat
   of those moves) is the next job, unless you would rather leave it.

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
