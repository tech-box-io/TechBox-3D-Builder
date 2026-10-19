PMG Build Instructions (Piano Memory Game, Full Build: the electronics wired on the bench, then the wooden case with the electronics
fitted into it)

FIRST DRAFT 19 Oct 2026. Build instructions generated from Lee's STEP ("PMG Full 3D Cadasio Build.STEP") and TechBox's published
Cadasio guide for the kit (instructions.online/?id=19075-piano_memory_game_pmg-full_build), in the same format as the MRA and RCC
guides, with the same player (player/ is unchanged). Not for distribution. Open questions are yellow Review notes on their steps (in
the kit's player; the website copy leaves Review notes out) and are listed under QUESTIONS FOR LEE below.
Also on the local test website: http://localhost:8799/piano-memory-game-full-build/ (share/Test guides preview, a practice publish;
nothing is live).

HOW TO OPEN (Mac)
1. Double-click "Open Prototype.command". A Terminal window opens and the prototype opens in your browser (port 8792, so it can run
   beside the other kits). If macOS says it cannot be opened: System Settings > Privacy & Security > "Open Anyway".
2. When you are done, close the Terminal window. No internet connection is needed.
The controls are the MRA guide's: arrows step through, drag to rotate, scroll to zoom, Option-click a spot to copy where it is, the
grid button shows every step, ?review=0 hides the Review notes.

THE BUILD (47 steps, in the published guide's order)
- Step 1: the Nano Board into the Nano I/O module, lying on the bench (its USB socket at the power socket's end).
- Step 2: twelve breadboard wires peeled off the ribbon and separated.
- Steps 3 - 14: the four push buttons, black, yellow, white and blue (rows 4, 5, 6, 7), each wired pin by pin: VCC to V, OUT to S,
  GND to G. Each button appears with its first wire, held in front of the module, pins down (as published). One wire per step, as
  published: the wire lies loose in front of the module (an eye on it), then its two caps are lifted, held over their pins and
  pushed on; a label names each pin (e.g. VCC and V4; Step 3's caution says what V4 means).
- Step 15: nine more wires off the ribbon.
- Steps 16 - 19: the 4-digit display (CLK to S8, DIO to S9, VCC to V9, GND to G9).
- Steps 20 - 24: the dot matrix display (VCC to V11, GND to G11, DIN to S11, CS to S12, CLK to S13).
- Step 25: the USB cable's right-angle plug into the Nano Board; its A end lies on the bench. A caution: set the module aside.
- Steps 26 - 30: the case on its own (as published): H1, then H2, H3 and H4 pushed on; the case turned over for H5 and H6, each
  hooked into H2's windows and swung into H3's notches.
- Steps 31 - 32: the electronics come back beside the case; the blue push button into its pocket in H6, then the other three.
- Step 33: H7 over the buttons (still turned over).
- Steps 34 - 40: the case the right way up: H8; one piano key (H9) slid in from the front, then the other three; H10 hooked into H4 and
  lowered; H11 and H12 down into H10 and back into H4; H13 down its slope.
- Steps 41 - 46: the electronics into the case, each picked up first (an eye), then placed (as published): the I/O module held over
  the back of H4 (the USB cable's A end laid on the table behind the case) and lowered onto it (an arrow; USB end at the top); the
  4-digit display into the notches of H11 and H12; the dot matrix display onto their hooks.
- Step 47: H14 over the 4-digit display, its bottom on the dot matrix display's top edge, then swung in. The Completed View shows the
  game from the front, on the student's right, as the title page does.

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
- The jumper wires are drawn by the player between their caps, as on the MRA, in the published guide's 21 colours. Their shapes come
  from the CAD where it has them (the OUT and display wires on the bench, the way through the case under the keys), otherwise drawn
  smooth, each module's wires layered so that where they cross they pass over one another; no wire passes through a part in any
  step (docs/research/pmg/scripts/check_wires.py; wires touching one another: check_overlaps.py).
- Checked: an independent review of every view against the rulebook and the published guide's pictures (its findings fixed), the
  run-through check on all 98 views, in the kit and as published to the test website.
- Research: docs/research/pmg/ (cad_study.md, cadasio_map.md, cad_wire_paths.md, reuse_plan.md, critic.md).

WHERE THE STEP AND THE PUBLISHED GUIDE DIFFER
The STEP looks like an earlier save of the model than the one the published Cadasio guide was made from (CAD version 7, 4 Aug 2026;
docs/research/pmg/cadasio_map.md section 2). This draft follows the published guide, which is what students build from today:
- Each push button has three wires (VCC to V, OUT to S, GND to G). The STEP has two (OUT to S, and the VCC pin to G) and no cap on
  V4 - V7 or on a button's GND pin: make_source.py adds the eight caps.
- The I/O module goes on the back of H4 with the Nano's USB end at the top. The STEP has it the other way up (USB end at the bottom,
  its power socket resting on H5's tongue). Turned the published way up, it sits 1.9 mm higher than the published project has it, so
  that its board rests on H5's tongue instead of sinking into it.
- The dot matrix lies on the bench turned as published (the STEP's bench copy is turned end for end, its wires on the mirrored pins).

QUESTIONS FOR LEE
1. Is the STEP the latest version of the PMG model? It looks older than the published guide's; could the 3D engineer export the
   assembly the published Cadasio guide was made from? (Review note, Step 3.)
2. Three wires per push button (published) or the STEP's two? (Review note, Step 3.)
3. Which way up does the I/O module go on the back panel: USB end at the top (published) or at the bottom (STEP)? (Review note, Step 41.)
4. How long are the kit's jumper wires? The drawn lengths are representative (as the RCC's leads).
5. The published guide names each module's pins on section cards with a photo of the real board; the player has no photo cards yet.
   Should the button, display and dot matrix boards carry their printed pin names, as the I/O module does? If so, a photo of each.
6. Jumper caps grey as the MRA's (this draft) or black as the published PMG guide?
7. Should the Full Build also be cut into the published Parts 1 - 3 (the buttons; the display, matrix and USB; the case)?
8. An electronics check before the case (as the MRA's and RCC's test card), or none (as published)?
