PMG Build Instructions (Piano Memory Game, Full Build: the electronics wired on the bench, then the wooden case with the electronics
fitted into it)

FIRST DRAFT 19 Oct 2026; LEE'S FIRST ROUND done the same evening (below). Build instructions generated from Lee's STEP ("PMG Full 3D
Cadasio Build.STEP") and TechBox's published Cadasio guide for the kit (instructions.online/?id=19075-piano_memory_game_pmg-full_build),
in the same format as the MRA and RCC guides, with the same player. Not for distribution. Open questions are yellow Review notes on
their steps (in the kit's player; the website copy leaves Review notes out) and are listed at the end of this file.
Also on the local test website: http://localhost:8799/piano-memory-game-full-build/ (share/Test guides preview, a practice publish;
nothing is live).

HOW TO OPEN (Mac)
1. Double-click "Open Prototype.command". A Terminal window opens and the prototype opens in your browser (port 8792, so it can run
   beside the other kits). If macOS says it cannot be opened: System Settings > Privacy & Security > "Open Anyway".
2. When you are done, close the Terminal window. No internet connection is needed.
The controls are the MRA guide's: arrows step through, drag to rotate, scroll to zoom, Option-click a spot to copy where it is, the
grid button shows every step, ?review=0 hides the Review notes.

THE BUILD (49 steps, in the published guide's order)
- Step 1: the Nano Board into the Nano I/O module, lying on the bench (its USB socket at the power socket's end).
- Step 2: twelve breadboard wires peeled off the ribbon and separated.
- Step 3: the push buttons introduced, as the published guide's "Push Buttons" card: one button on its own, close up, and a close-up
  of its pins with their printed names (VCC, OUT, GND) boxed in red.
- Steps 4 - 15: the four push buttons, black, yellow, white and blue (rows 4, 5, 6, 7), each wired pin by pin: VCC to V, OUT to S,
  GND to G. One wire per step, as published: the wire lies loose in front of the module (an eye on it), then its two caps are lifted,
  held over their pins and pushed on; a label at the top of each pin (e.g. VCC and V4; Step 4's caution says what V4 means).
- Step 16: nine more wires off the ribbon (seen from higher up).
- Steps 17 - 20: the 4-digit display (CLK to S8, DIO to S9, VCC to V9, GND to G9); its wires run behind the push buttons' (over the
  Nano Board) into rows 8 and 9.
- Steps 21 - 25: the dot matrix display (VCC to V11, GND to G11, DIN to S11, CS to S12, CLK to S13), seen from behind it: its printed
  pin names beside its header and the module's pins; each wire lies behind the module, where this camera sees it.
- Step 26: the USB cable's right-angle plug into the Nano Board; its A end lies on the bench. A caution: set the module aside.
- Steps 27 - 31: the case on its own (as published): H1, then H2, H3 and H4 pushed on; the case turned over for H5 and H6, each hooked
  into H2's windows and swung into H3's notches (a beat for each, seen from the front, by H1).
- Steps 32 - 33: the electronics come back beside the case; the blue push button into its pocket in H6, then the other three. Their
  wires run under H5 (between H5 and H7), out under H4's raised bottom edge, and on to the module.
- Step 34: H7 over the buttons (still turned over, as H5 and H6).
- Steps 35 - 41: the case the right way up: H8; one piano key (H9) slid in from the front, then the other three; H10 hooked into H4 and
  lowered (the keys' camera for all three); H11 and H12 down into H10 and back into H4 (each from a front corner, close); H13 down its
  slope.
- Steps 42 - 48: the electronics into the case, each picked up first (an eye), then placed: the I/O module held over the back of H4
  (the USB cable's A end laid on the table behind the case) and lowered onto it; the 4-digit display passed under the dot matrix
  display's wires into the space behind the module (Step 44), lifted up behind the case, over the top and held over its place
  (Step 45), and lowered into the notches of H11 and H12 (Step 46); the dot matrix display lifted, carried over the case and held in
  front (Step 47), then hung on the hooks of H11 and H12 (Step 48).
- Step 49: H14 over the 4-digit display: its two bottom tabs set down onto the top edge of the dot matrix display (lead lines and a
  close-up on them), then its top swung in. The Completed View shows the game from the front, on the student's right, as the title
  page does.

LEE'S FIRST ROUND (19 Oct 2026; docs/research/pmg/round1_plan.md has the list and how each was done)
Step numbers in Lee's notes are the first draft's: from its Step 3 on, the new number is one higher, and its Step 43 (pick up the
display) is now two steps (44 and 45), so its Steps 44 - 47 are now 46 - 49.
- The dot matrix's LEDs are round, in 8 x 8 grids; the push buttons, the 4-digit display (front and back) and the dot matrix's back
  carry their printed labels, from Lee's photos (silkscreen.py, docs/research/pmg/silkscreen.md).
- The wires were all laid again (routing.py): each device's wires run side by side as a ribbon (turned on the way so that none of a
  bundle passes through another; where two change places, one passes over the other), then settled clear of every other wire and of
  every part in that view. Behind the module, from the bottom: the push buttons' rows, the display's rows (its wires run out beside
  the Nano Board and under the dot matrix's, then up beyond the module's end and over H4), the dot matrix's rows (outermost). Checked
  in every view: no wire inside a part, none through another (check_wires.py, check_overlaps.py, tools/wirecheck.py); during each
  step's motion (scripts/check_motion.py: round1/motion_check.txt); and by an independent review of every view (round1/, its findings
  fixed: the card shows the button alone, Step 16 the whole module, the dot matrix's loose wire lies where its camera sees it, each
  new wire is held clear of those already in). What is left, only while a step plays: where a whole bundle changes shape (the
  buttons into the case, Steps 32 - 33; the module up and down, 42 - 43; the display, 44 - 45; the dot matrix, 47) its own wires pass
  through one another for a moment (the player blends each wire on its own); in Steps 22 and 25 one matrix wire touches another as
  it settles in; in Step 33 the push buttons' wires touch H5's edge by up to 0.7 mm for a moment. And a riding part's in-between
  stops (the display over the top in Step 45, the dot matrix in Step 47) all play within one 0.8 s beat: see question 8.
- Parts list pictures: the I/O module and the Nano Board from their component side; the yellow push button; H5, H6, H7, H9, H10 and
  H13 the right way up; H14 face on.
- Cameras changed where Lee asked (and nowhere else, checked view by view against the first draft): Step 16; Steps 21 - 25; Steps
  30, 31 and 34; Steps 37 and 38 (Step 36's); Steps 39, 40, 41; the framing of Steps 44 - 45 and 47, whose motions changed.

HOW IT WAS MADE
- pmg.glb (167 MB, converted from the STEP) holds the engineer's pose copies of most parts (three I/O modules, eight buttons, three
  displays, four dot matrices, 139 wire caps, 114 wire bodies). make_source.py cuts it down to pmg-guide.glb (17 MB): one copy of each
  part, where it sits in the finished game; every other place is a pose of that copy (cad-geometry.json). pmg.glb stays on this Mac
  (over GitHub's file limit; its STEP's checksum is in cad-sources.sha256): run make_source.py again only if the STEP changes.
- Reused from the MRA and RCC (Lee, 19 Oct 2026): the Nano Board is the MRA's export of the Nano model (as both of the RCC's), placed
  in the module's sockets; the I/O module is the MRA's module model already (its colours, atlas and silkscreen carry over: silkscreen.py);
  the USB cable's A end and the jumper caps are the MRA's models already. The USB cable's Mini-B end stays the PMG's own right-angle plug
  (a part that differs stays the kit's own: rulebook section 13). The push buttons, display, dot matrix and wood are coloured as
  TechBox's Cadasio project has them (materials.json).
- The jumper wires are drawn by the player between their caps, as on the MRA, in the published guide's 21 colours. Since Lee's first
  round they are laid by routing.py (see LEE'S FIRST ROUND above): each device's wires as a ribbon, settled clear of every other wire
  and every part in the view; no wire passes through a part or another wire in any view (docs/research/pmg/scripts/check_wires.py,
  check_overlaps.py, tools/wirecheck.py; during the motions: check_motion.py).
- Checked: independent reviews of every view against the rulebook, the published guide's pictures and Lee's notes (their findings
  fixed: critic.md for the first draft, round1/ for the first round), the run-through check on all 101 views, in the kit and as
  published to the test website.
- Research: docs/research/pmg/ (cad_study.md, cadasio_map.md, cad_wire_paths.md, reuse_plan.md, critic.md, silkscreen.md,
  round1_plan.md, round1/).

WHERE THE STEP AND THE PUBLISHED GUIDE DIFFER
The STEP looks like an earlier save of the model than the one the published Cadasio guide was made from (CAD version 7, 4 Aug 2026;
docs/research/pmg/cadasio_map.md section 2). This draft follows the published guide, which is what students build from today:
- Each push button has three wires (VCC to V, OUT to S, GND to G). The STEP has two (OUT to S, and the VCC pin to G) and no cap on
  V4 - V7 or on a button's GND pin: make_source.py adds the eight caps.
- The I/O module goes on the back of H4 with the Nano's USB end at the top. The STEP has it the other way up (USB end at the bottom,
  its power socket resting on H5's tongue). Turned the published way up, it sits 1.9 mm higher than the published project has it, so
  that its board rests on H5's tongue instead of sinking into it.
- The dot matrix lies on the bench turned as published (the STEP's bench copy is turned end for end, its wires on the mirrored pins).

QUESTIONS FOR LEE (still open after the first round)
1. Is the STEP the latest version of the PMG model? It looks older than the published guide's; could the 3D engineer export the
   assembly the published Cadasio guide was made from? (Review note, Step 4.)
2. Three wires per push button (published) or the STEP's two? (Review note, Step 4.)
3. Which way up does the I/O module go on the back panel: USB end at the top (published) or at the bottom (STEP)? (Review note, Step 42.)
4. How long are the kit's jumper wires? The drawn lengths are representative (as the RCC's leads).
5. Jumper caps grey as the MRA's (this draft) or black as the published PMG guide?
6. Should the Full Build also be cut into the published Parts 1 - 3 (the buttons; the display, matrix and USB; the case)?
7. An electronics check before the case (as the MRA's and RCC's test card), or none (as published)?
8. Steps 45 and 47 carry the display and the dot matrix over the case through in-between stops, but the player plays a riding
   part's stops within one 0.8 s beat, so the crossing over the top is quick. A player change would give each stop a beat of its own
   (as a moving part's stops have); it would also slow the plugs walked back in the MRA's and RCC's deconstructions. Make it?
(The first draft's question 5, the boards' printed pin names, was answered by Lee's photos: done.)
