LAC Build Instructions (LCD Alarm Clock, Full Build: the electronics on the breadboard, wired one wire at a time, then the box)

FIRST DRAFT 19 Oct 2026 (F2, F5 and F6 added the same day, from Lee's STEPs); LEE'S FIRST ROUND 20 Oct 2026 and SECOND ROUND 21 Oct 2026 (below). DECONSTRUCTION, first draft 21 Oct 2026 (THE DECONSTRUCTION below). Both published, r1, 22 Oct 2026 (questions 7 and 25). Build instructions generated from the engineer's STEP (LAC Full Build.STEP) and TechBox's published Cadasio
guide for the kit (instructions.online/?id=19075-lac_full_build), in the same format and with the same player as the MRA and RCC
guides (player/ was not changed). Not for distribution. Open questions are under QUESTIONS FOR LEE below.

HOW TO OPEN (Mac)
1. Double-click "Open Prototype.command". A Terminal window opens and the guide opens in your browser (port 8793, so it can run
   beside the MRA's 8791, the PMG's 8792 and the RCC's 8796). If macOS says it cannot be opened: System Settings > Privacy & Security >
   "Open Anyway".
2. When you are done, close the Terminal window. No internet connection is needed.
The controls are the MRA guide's: arrows step through, drag to rotate, scroll to zoom, Option-click a spot to copy where it is, the
grid button shows every step, ?review=0 hides the Review notes.
The deconstruction: player.html?steps=steps-deconstruction.json (the same server).

THE BUILD (57 steps, with the published numbers: Step 29 here lays F1 face down where the published Step 29 turns the knob (question
2). Until F9 was given its two published steps (Lee, 21 Oct 2026), a step from 46 on was numbered one lower here, as in Lee's notes of
20 and 21 Oct 2026 before then; every number in this file is as now.)
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
  the cable lying straight out behind the base to its A end, along the line on which F2's slit will come in (Step 56).
- Steps 41 - 54, the box: the two F7s into F3; their tops spread apart (arrows; they are not lifted), the buzzer lifted, carried over
  and lowered in between (its leads follow, a shape for each stop), let go; F9 hooked in by its front foot, tipped, and swung upright
  (Steps 45 and 46, as published); F1 moved, still face down, further out in front and
  along to the F7s' end (as published, Step 47: out of the LCD's way; its leads then run between the F7s and F8); F4 lifted over the
  frame (the switch's leads follow) and lowered onto the tabs of the F7s and F9 (four lead lines, from the tab tops Lee gave); F8 slid
  in from the front; the LCD lifted off the table and slid out in front, stood up face to the front 40 mm out, and moved in until the
  end of its board is in F8's notch, the other end angled 14 degrees out in front of F9 (the published pose, without its 2.14 mm lift,
  which put the LCD into F4); then straightened, pushed 14.9 mm on through F8's notch and slid back into F9's notches (a close-up of
  them); its wires stay behind F9 all the way (the run round F9's back edge held still); F1 stood up in front of the box and pushed onto
  the tabs of F4 and F3 (Lee's lead line at F4's front tab).
- Steps 55 - 57, the ends and the back, as published: F5 pushed onto the breadboard's end, the tabs of F1, F3 and F4 into its slots (six
  lead lines, two of them at F4's tabs as Lee gave them; seen low from the front as published, so that F5 does not hide them); F2, the case seen from behind: brought in swung out,
  the tabs at its slit end hooked into F5's slots, and swung shut onto the tabs of F3 and F4, its slit (open at the bottom) sliding along
  the USB cable, the cable following it (a Caution: the cable must sit in the slit; an eye on the cable in the slit, and a close-up of it
  on Step 56c); F6 onto the other end, which locks them all. The Completed View is the closed box. Unlike the published Step 56, the
  case stays upright (published: laid on its front, F2 lowered from above; the player can turn a model only upside down), and F2 comes
  in 40 mm straight from behind and then 14 mm along itself (published: about 80 mm, diagonally from behind and F6's end), so that its
  slit slides along the cable lying straight out behind the case.
- Checked (21 Oct 2026, after Lee's second round): the player's run-through check passes on every view (118 views, forwards,
  backwards and jumping, 0 problems); at rest each wire is clear of the parts and of the other wires (tools/wirecheck.py: one touch
  of 0.04 mm, the purple jumper's cap held over its hole beside the blue's, Step 12); during the moves (tools/motioncheck.py, every
  move at 39 moments: twice as many as Lee's first round was checked at) no wire passes into a panel, and 22 moments in 96 moves
  are left: the purple jumper brushing the blue jumper's cap and wire by 0.6 - 0.8 mm as it goes in (Step 12), the switch's black
  and tan leads 0.8 mm apart as Step 17 starts, the orange and yellow jumpers 0.94 mm apart (Step 21c), the buzzer's black lead
  through the LCD's four wires for about 50 ms (Step 43c: question 11), and 16 where the potentiometer's leads brush the wires of
  the bundle for a moment as their run in the case changes (Steps 47c and 53c, as after the first round). Lee's first round was
  left at 63 moments of 19 per move; before it, 132. Cameras: only those of Steps 16 - 18, 30 - 35, 50 and 51 changed in this round, and F9's two steps have the published one.

THE DECONSTRUCTION (50 numbered steps; first draft 21 Oct 2026, Lee's first round 22 Oct 2026. Lee: "we need to make a deconstruction
guide for this LAC as well. Here is the published version of the guide that we need to convert / remake here:
instructions.online/?id=19075-lac_deconstruction")
deconstruction.py -> steps-deconstruction.json; open it with player.html?steps=steps-deconstruction.json. TechBox's published take-apart
(47 steps) remade on our Full Build: one wire per step, as published (Lee, 22 Oct 2026: "For this kit only, given the excess number of
wires, let's keep it wire by wire"); its order where our model allows it; every step a caption of its own; each arrow the published
one's size, but alike parts alike (the two F7s, the two resistors) and shorter where the published length reached into the instruction
boxes (F4, the rocker switch); an arrow per stage, in turn, for F9 (the tip, then the lift); one arrow where a lead changes shape on the
way (F2, F4, the buzzer); the up arrows only for the F7s, as published. It opens on the Full Build's title page, ends on F3 with the
breadboard (stuck on for good, as published), and goes straight on to the Full Build's parts list (no Completed View: Lee, 22 Oct
2026); its website card would be the Full Build's. Every wire keeps a shape the Full Build drew (each route is one of the Full
Build's); the steps walk the Full Build back, except that the USB cable comes out at Step 4 (power first), the potentiometer and F9 come
where Lee put them (below), and one wire a step keeps the published order where it clears. The plan and its reasons:
docs/research/lac/decon/plan.md (the published guide mapped onto ours: study_map.md; its cameras, arrows and poses in our frame:
published_geometry.md); Lee's notes of 22 Oct: docs/research/lac/decon/lee_notes_2026-10-22.md.
- Steps 1 - 4: F6, F2 (the USB cable back out of its slit as F2 swings out and slides off), F5 (Step 1's caution: unplug the USB cable
  from the computer first; the closed case holds its plug); then the USB cable, as soon as its plug can come out (published: Step 25).
- Steps 5 - 10: F1 pulled forward (its arrow along its lower edge, level, as published) and laid face down aside, still wired; the LCD
  screen out of F9's notches (a close-up of them), then out of the case and laid face down, still wired (two steps, as the Full Build
  brought it in); F8; F4 lifted off with the switch and moved out behind the case, still wired (held up where the Full Build held it).
- Steps 11 - 14: F1 moved in front of the breadboard's end (ours lies face down where the published one lies face up, and the
  potentiometer's leads were plugged in with it there); the F7s spread, the buzzer lifted out to lie beside the base, still wired, and
  the F7s pulled out (before the potentiometer: the buzzer's black lead lies over the potentiometer's leads by the breadboard).
- Steps 15 - 25, the potentiometer first, as published (Lee, 22 Oct 2026): its black, tan and red leads (each left hanging from it, as
  before the Full Build plugged it in), seen from above the breadboard's end with F9 behind the leads (Lee's view, from his screenshot);
  F1 picked up and held upright; on its own: the knob, the nut (unscrewed in one smooth turn) and the washer slid off and faded, as
  everything taken off does, the potentiometer pushed out of F1's back; then the washer, the nut (screwed on) and the knob back onto the
  potentiometer (as published, and as Lee asked: "after the potentiometer is removed from F1, the washer, nut, and knob need to be
  reinstalled onto the potentiometer before moving on"), each appearing just off the shaft's end as its step opens, with a lead line to the shaft, as the Full
  Build puts them on F1 (its Steps 26 - 28), seen as close as the Full Build's Steps 22 - 24, which take them off the potentiometer
  there; then the potentiometer, whole, is put away (off the screen) with its leads.
- Steps 26 - 34: the LCD's four wires, one a step (GND, VCC, SDA, SCL labelled on its pins, as published), each female connector 7 mm
  off its pin, just clear of it (the LCD lies face down, its pins pointing at the case: pulled further, SDA's and SCL's leads passed
  into F9), each lead lifted with its breadboard end, so that it slides up out of the four leads' bundle (only its last 7 mm go with
  the connector off the pin: tied as it lies, it passed through its neighbours), the LCD; the buzzer's red and black leads, the buzzer; then F9, once the potentiometer, the LCD and the buzzer are out (Lee):
  tipped, then lifted, an eye on its lower rear latch (the back foot's barb under F3: Lee) and a close-up of its front foot's barb under F3.
- Steps 35 - 50: the yellow and orange jumper wires; the switch's black, tan and red leads; the rocker switch pushed up out of F4 (on its
  own), its two clips squeezed first (Lee: they must be; a close-up of them from below F4, a red box on each); the white, dark red,
  purple, blue, green and black jumper wires; the real time clock module; each 12 kΩ resistor; the Nano Board (the Pry Tool caution, as
  the MRA's and LSM's: the kit has one, though the model does not show it). Steps 41 - 50 share one camera, as the published's Steps
  36 - 47 do.
- Not taken from the published guide: its views turned on their side (F2, the potentiometer: our player keeps up as up); its fades
  between copies of a part in two places (here the parts move); its order where it would pass our wires through each other (the
  potentiometer's and the LCD's wires before the buzzer is out of the F7s; the orange jumper last, over purple, blue and green; the
  switch's leads before orange and yellow).
- Checked (22 Oct 2026, after Lee's second notes): the player's run-through check passes on every view (103 views, forwards,
  backwards and jumping, 0 problems; it now lets a part taken off come back where a view says so, `back`: Steps 23 - 25); at rest
  every wire is clear of the parts and of the other wires (tools/wirecheck.py, 0 problems: the buzzer's black lead, lying beside the
  base, is drawn 1.2 mm clear of F9's back edge from Step 13 until it is unplugged, as F9 now stays until Step 34: in the Full Build
  the two were never on screen together); during the moves (tools/motioncheck.py, 39 moments a move, which now also follows parts and
  leads as they leave) nothing passes into F9, and 21 brief contacts: 17 the Full Build's own, played backwards (Steps 6c and 11c are
  its Steps 53c and 47c; 13c its 43c); the potentiometer's black lead against its tan for a moment as it is unplugged (Step 15c, 0.65
  mm between centre lines); the switch's black and tan leads (Step 38c, as the Full Build's Step 17); and two the check has only now
  seen, as parts and leads leave: the yellow jumper's lead 0.3 mm into the orange's as it is lifted out (Step 35c), and the white
  jumper's connector 0.2 mm into the dark red lead (Step 41c). Looked at 1280 x 800 and 1024 x 768 (Step 15: the caption and caution
  boxes clear of the three leads); an independent review of the first draft (docs/research/lac/decon/review/: three reviewers, each
  finding checked by a fourth).

LEE'S FIRST ROUND (20 Oct 2026)
- The 12 kΩ resistor is named so everywhere (the parts list, labels, captions; "2x - 12 kΩ Resistor" on Step 4).
- Colours: the knob's silver ring and the resistor's bands, the breadboard's legends, the USB plug's and the switch's marks are TechBox's
  Cadasio face copies laid 0.02 mm over the body; the body under them now takes their colour, so the black no longer shows through
  (colour-atlas-lac.json: "skin"). The potentiometer is pictured from its knob side in the parts list.
- Cameras closer on what each step puts in (Steps 3 - 7, 9 - 18, 20 - 34, 36 - 41, 45, 51), labels moved off the parts and their
  leaders apart (Steps 1, 3 - 7, 15, 22, 33, 34); lead lines where Lee gave them (Steps 5, 6, 49, 54, 55). Steps Lee did not name whose
  camera changed: 26 and 28 share Steps 25 and 27's camera on F1 and the potentiometer (framed as before; the base behind them sits
  differently, as F1 is held where Step 29 now lays it down); Step 47 is a new move. Step 35's is as it was. Step 40's close camera
  leaves the USB cable's A end off the screen (it is back in Step 41).
- The moves: no part is turned about a far-off point any more (the buzzer's caps and the buzzer swung off the screen: Steps 33, 34,
  43); each lead has a shape for each stop of a move; the potentiometer's, the buzzer's and the LCD's wires are drawn from the
  breadboard, so that the run in the case is held still where both shapes share it: the LCD's round F9's back edge in every shape
  (Steps 36 - 52), the potentiometer's as F1 is pushed on (Step 54: it dipped into F8), the buzzer's through the jumpers as it is
  lowered onto its seat (Step 43, its last beat). The buzzer's leads turn out of the buzzer and into their holes over several mm (they
  had hairpins there). tools/motioncheck.py now turns a part between two poses as the player does (it turned every part about its
  middle, so it did not see those swings).
- An independent review (three reviewers, each finding checked by a fourth: docs/research/lac/round1/review.md) found the rest of the
  above: holes still hidden from their step's camera (14, 20, 21, 38, 39), the jumpers and Step 33's red cap gliding in from off the
  frame, the LCD ribbon's two ends crossing as each wire was connected, the LCD wires' run lifting through the jumpers in Step 51.
- Research for the round: docs/research/lac/round1/ (how the LSM does what Lee asked for, the published guide's moves and cameras, the
  model's colour faults, why the wires misbehaved mid-move).

LEE'S SECOND ROUND (21 Oct 2026; research and the evidence for each change: docs/research/lac/round2/)
- The breadboard's joining tabs as on the LSM's, where the real board has them: two on the a side (the front) and three on the column 30
  end (the buzzer's end). It is the LSM's revised breadboard (breadboard-lsm.glb, extra part NAUO1: the same CAD part vertex for vertex,
  holes unchanged); Step 1's camera and Step 2's corner lines kept where they were.
- Labels and eyes beside their targets, not at the window's edges, in every step of the kit (guide.py near(): 'near-left', 'up-right' ...
  with a reach; chosen per step clear of each other: round2/labels.md).
- Lee's cameras, solved from his screenshots to the pixel (round2/cameras.md): Steps 16 - 18, 30 - 32, 33 - 34, 50 (F8's label up and to
  its right). b9 (Step 39) shows from no direction in front (the cameras of Steps 14, 20, 21 and 38 already show their holes whole,
  from the first round), so Step 39c now has a close-up of it from above, the blue wire's pin in it; Step 38c the same close-up of b8,
  the teal wire's pin in it (Lee, later the same day).
- Wires going in through others: the white jumper (Step 13) is a low arch, and it and the dark red (Step 14) come in low from the front,
  5 mm up, under the purple and blue; the potentiometer's black lead (Step 32) runs under the tan's hump and is held 5 mm up; the LCD's
  GND and VCC wires go into other holes of the same rails (k = +2, +4: z 1290, 1295), clear of the green and black jumpers that lean over
  the CAD's holes (question 10); each LCD wire is pushed in by its cap only, the rest of it still; the lying LCD wires run in smooth lanes
  (Steps 36 - 39: "crazy and bent" was a hairpin and a straight drop).
- The buzzer's stubs coloured as its leads (red to j4, as published: our colours came from TechBox's other copy of the buzzer, which has
  them the other way round). Its leads start at the stubs (no gap), and seated they run over the jumpers, the eye above it. Step 43: the
  buzzer is lifted, carried high over the board (turning upright) and lowered straight in, its leads passing over every jumper and wire
  (round2/step43_judge.md: two designs, the better taken); seated, the red lead now leaves the buzzer forward, beside the black, up in
  front of the switch, and crosses back over the board past the clock module into j4 from behind (question 11).
- The LCD's ribbon (Step 35) laid clear of F1 and the potentiometer's leads, the view a little wider to take it in; its wires' ends are
  then put away, and each comes back on its own step (Steps 36 - 39), held over its hole, and is pushed in.
- The USB cable centred on both plugs (its ends came from the rim of the CAD's end faces).
- Step 51: the LCD is stood on its header end, tips up and over it to stand upright out in front, comes in, and slides along its own length
  into F8's slots (it went in sideways, through F8's front); closer camera. Step 52 straightens it in the middle of F8's slots.
- Step 54: the fourth lead line from F1's back, as the other three. Step 49 (Lee, later the same day): its four lead lines run from the
  tops of the F7s' and F9's tabs to F4's underside (three ran on through F4's slots to 3.3 mm over its top, where the tabs' tops are
  once it is down).
- F9 (Lee, later the same day: "it does need to hook and rotate in as in the published guide"): two steps, as published. Step 45: held
  upright over its slots (Lee, then: not brought in from out in front, as published, where its lead lines ran through F1 lying there),
  tipped 25.8 degrees forwards about its front edge, and lowered until its front foot's
  barb hooks under F3 (a beat each; a close-up on Step 45c with F3 drawn faintly, as F3's edge hides the hook). Step 46: swung upright
  about that edge, its back foot down into its slot (an eye and a lead line on it). The published camera of both steps, its middle
  moved to the right, where the close-up goes. Each foot has a 1 mm barb under F3: the back one passes into F3's edge by up to 1.3 mm for a moment as F9 is
  swung upright (a snap fit; no turning point makes it less than 1.2), as in the published. Every step from 46 on is one higher.
- tools/motioncheck.py spaces a way's in-between poses as the player does (poseGap) and takes --moments (39 catches the quarters, where a
  step of two or four beats changes beat).

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
4. (Answered: F9 is hooked in and swung upright, as published: Steps 45 and 46.)
5. The right-angle USB plug is the LAC's own (the MRA's and RCC's are straight): is that the cable in the kit?
6. The jumper wires change length between lying loose and plugged in (the CAD routes them 50 - 90 mm); fine, as for the RCC's leads?
7. (Done, 22 Oct 2026: published on Lee's word as https://models.tech-box.io/lcd-alarm-clock-full-build/, r1, the kit's page
   /kits/lcd-alarm-clock/; it goes live when main is pushed to live.)
8. (Done in your first round: see above.)
10. Steps 36 - 37: the LCD's GND and VCC wires now go into the (-) blue and (+) red rails two and four holes further along than the CAD
   has them (the same connection): where the CAD has them, the green and black jumpers lean right over the holes and the wires cannot go
   in without passing through them. Fine, or should they go back?
11. Step 43: the buzzer's leads now pass over every jumper, lying and as the buzzer is carried in, except for one moment (about 50 ms,
   mid-carry) when the black lead passes through the LCD's four wires: those were laid over the lying black lead (Steps 36 - 39), so one
   has to pass the other. Clean would take re-laying the LCD wires in front of the (-) blue rail (Steps 35 - 52), or playing Step 43 as
   a fade (the buzzer fading out and back in seated, as the PMG's Step 42), which no longer shows the carry. While the buzzer is held
   high, its leads look stiff for a moment (a long black line over the board, a red post behind the caps); softer shapes are possible.
12. Step 50's label (up and to the right of F8, as asked) lands on F8 in windows under about 880 px wide (an iPad in the LMS is 768):
   'up-left' is clear at every width.
13. (Answered, 22 Oct 2026: one wire per step, for this kit only, given its many wires.)
14. (Deconstruction) The USB cable at Step 4 (power first, as soon as its plug can come out; Step 1 says to unplug it from the computer),
   or where the published has it, after F9 (its Step 25)?
15. (Deconstruction) The buzzer comes out from between the F7s (Steps 12 - 14, still wired) before the potentiometer's wires: its black
   lead lies over them by the breadboard, so in our model they would pass through it. Its leads come off after the LCD's, then F9, as you
   asked. Fine?
16. (Deconstruction) The potentiometer: our F1 lies face down (knob down) where the published lies face up, so the draft moves F1 in
   front of the breadboard (Step 11), unplugs its three wires (each left hanging from it), then picks F1 up and holds it upright (Step
   18) to take off the knob, nut and washer, as the Full Build put them on. Two steps more than the published. Fine?
17. (Answered, 22 Oct 2026: the washer, nut and knob go back on the potentiometer once it is out of F1: Steps 23 - 25.)
18. (Deconstruction) The LCD screen out in two steps (Steps 7 and 8: out of F9's notches, then out of the case and laid down, as the
   Full Build brought it in), or one, as published?
19. (Deconstruction) The GND / VCC / SDA / SCL labels on the LCD's wire steps (Steps 26 - 29; the published guide's only text): keep?
20. (Deconstruction) Arrows: an arrow per stage, in turn (your PMG rule), cannot be combined with a wire that changes shape stage by
   stage, so F2, F4 and the buzzer (Steps 2, 10, 13) have one arrow; a small generator change would allow both (it touches every kit):
   want it? Step 14: the F7s close, then lift; the published draws only the up arrows, so does the draft (F7A's where it will be once
   closed, as F4 is held up over its spread top). Add an inward arrow first?
21. (Deconstruction) The LCD screen and the buzzer, once off their wires, lift 30 mm and fade, with an eye (published: they fade where
   they lie). Fine?
22. (Answered, 22 Oct 2026: the rocker switch has clips to squeeze, now in Step 40's caption and close-up; the kit has a Pry Tool, now
   Step 50's caution.)
23. (Deconstruction, and Full Build Steps 29c - 32) The potentiometer's unplugged leads stick straight out from it, as the Full Build
   draws them before they are plugged in. Droop them onto the table instead (a change in the Full Build, which the take-apart follows)?
24. (Deconstruction) Two small brushes for a moment: the potentiometer's black lead against its tan as it is unplugged (Step 15) and
   the switch's black and tan leads (Step 38). Fine, or unplug the tan first in each?
25. (Done, 22 Oct 2026: published with the Full Build as https://models.tech-box.io/lcd-alarm-clock-deconstruction/, r1. Its step
   text for editing, with the Full Build's: share/LAC step text 2026-10-22/.)
9. The potentiometer's knob: TechBox's Cadasio project draws a silver ring round the end of the knob (and a silver pointer groove), so
   the guide keeps it and only stops the black showing through. If the real knob is all black, it is a one-line change to make it so.

FILES
  guide.py                      the build, in order (run it after any change: python "LAC Build Instructions/guide.py")
  materials.json                colours and detail; colour-atlas-lac.json its per-solid colours
  wire-paths.json               the breadboard's holes, the caps, every CAD wire's centre line, the poses between the CAD's copies
  trim_source.py                lac.glb -> lac-guide.glb (the parts the guide uses)
  lac.glb, lac-guide.glb        the CAD (converted from LAC Full Build.STEP), and cut down
  nano-mra.glb, usb-a-end.glb   the MRA's Nano Board and USB A end; f4.glb the top panel (extra parts)
  breadboard-lsm.glb            the LSM's revised breadboard (its tabs on the a side and the column 30 end), in place of NAUO1
  f2.glb, f5.glb, f6.glb        the back and end panels, from Lee's F2.STEP, F5.STEP, F6.STEP (extra parts; the STEPs stay out of git,
                                their checksums in cad-sources.sha256)
  steps.json, parts.json, model.glb, model.report.json, parts/   generated; do not edit by hand
  deconstruction.py             the take-apart (run it after guide.py: .venv.nosync/bin/python "LAC Build Instructions/deconstruction.py")
  steps-deconstruction.json     generated by it; do not edit by hand
  logo.webp                     the title page's logo (the RCC's)
  Research: docs/research/lac/ (cad_study.md; cadasio/ the published guide's data and step pictures; scripts/; decon/ the take-apart:
  the published guide's data and pictures, the studies, the plan, the review).
