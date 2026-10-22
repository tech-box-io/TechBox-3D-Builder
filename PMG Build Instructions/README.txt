PMG Build Instructions (Piano Memory Game, Full Build: the electronics wired on the bench, then the wooden case with the electronics
fitted into it)

FIRST DRAFT 19 Oct 2026; LEE'S FIRST AND SECOND ROUNDS done the same evening, the THIRD on 20 - 21 Oct, the FOURTH, FIFTH and SIXTH on 21 Oct (below). Build instructions generated from Lee's STEP ("PMG Full 3D
Cadasio Build.STEP") and TechBox's published Cadasio guide for the kit (instructions.online/?id=19075-piano_memory_game_pmg-full_build),
in the same format as the MRA and RCC guides, with the same player. Not for distribution. Open questions are yellow Review notes on
their steps (in the kit's player; the website copy leaves Review notes out) and are listed at the end of this file.
Also on the local test website: http://localhost:8799/piano-memory-game-full-build/ and, the take-apart (first draft 21 Oct 2026,
below), http://localhost:8799/piano-memory-game-deconstruction/ (share/Test guides preview, a practice publish; nothing is live).
In the kit's player the take-apart is http://localhost:8792/player.html?steps=steps-deconstruction.json.

HOW TO OPEN (Mac)
1. Double-click "Open Prototype.command". A Terminal window opens and the prototype opens in your browser (port 8792, so it can run
   beside the other kits). If macOS says it cannot be opened: System Settings > Privacy & Security > "Open Anyway".
2. When you are done, close the Terminal window. No internet connection is needed.
The controls are the MRA guide's: arrows step through, drag to rotate, scroll to zoom, Option-click a spot to copy where it is, the
grid button shows every step, ?review=0 hides the Review notes.

THE BUILD (48 steps, in the published guide's order)
- Step 1: the Nano Board into the Nano I/O module, lying on the bench (its USB socket at the power socket's end).
- Step 2: twelve breadboard wires peeled off the ribbon and separated.
- Step 3: the push buttons introduced, as the published guide's "Push Buttons" card: one button on its own, close up, and a close-up
  of its pins with their printed names (VCC, OUT, GND) boxed in red.
- Steps 4 - 15: the four push buttons, black, yellow, white and blue (rows 4, 5, 6, 7), each wired pin by pin: VCC to V, OUT to S,
  GND to G. One wire per step, as published: the wire lies loose in front of the module (an eye on it), then its two caps are lifted,
  held over their pins and pushed on; a label at the top of each pin (e.g. VCC and V4, the module's up and to the right of its pin;
  the button's pins labelled on its right; Step 4's caption says what V4 is). Seen from a little higher (Lee's screenshot of Step 9).
- Step 16: nine more wires off the ribbon (seen from higher up).
- Steps 17 - 20: the 4-digit display (CLK to S8, DIO to S9, VCC to V9, GND to G9), seen from behind and above: its printed pin names
  and the module's pins; its wires run between the push buttons' and the camera (over the Nano Board) into rows 8 and 9; each wire
  lies between the display and the module before it goes in. A beat each: both caps lifted straight up off the bench; carried over,
  the display's to 30 mm out along its pin in its own lane above the wires already in, the module's over the Nano Board and the
  bundle to above its pin (low enough to stay clear of the caption box in the LMS's frame); the display's slid along its lane to
  12 mm off its pin while the module's is lowered over its pin; both pushed on. Steps 19 and 20 (VCC to V9, GND to G9) are seen from
  lower and further round towards rows 10 - 13 (Lee's third round: from Steps 17 - 18's side the display's own wires hid V9 and G9;
  the display's printed back still in view). On each Step Nc a close-up from above of the module's pin, its new cap boxed in red
  (Lee's fourth round).
- Steps 21 - 25: the dot matrix display (VCC to V11, GND to G11, DIN to S11, CS to S12, CLK to S13), seen from behind and above it
  (Lee's screenshot of Step 22): its printed pin names beside its header, the module's pins; the module's labels up and to its left,
  the matrix's to the right of its pin, under the wire before (Lee's fourth round), the eye to the right of the loose wire; each wire lies across the gap between the matrix and the module before it goes in. A beat each: the matrix's cap
  rises straight up to its place 5 mm off its pin (under the wires already in) while the module's comes through the gap, upright,
  above the pins' height; the module's slides along its column, 10.5 mm above the pins, to over its pin; both pushed on. On each
  Step Nc a close-up from above of the module's pin, its new cap boxed in red, as Steps 17 - 20's (Lee's fifth round).
- Step 26: the USB cable's right-angle plug into the Nano Board; its A end lies on the bench. A caution: set the module aside.
- Steps 27 - 31: the case on its own (as published): H1, then H2, H3 and H4 pushed on; the case turned over for H5 and H6, each hooked
  into H2's windows and swung into H3's notches (a beat for each, seen from the front, by H1).
- Steps 32 - 33: the electronics come back beside the case; the blue push button into its pocket in H6, then the other three, each
  moved 26 mm clear of the module (the others also 8 mm along the row), lifted above the case, carried over its pocket and pressed in (a beat each). Their wires run under H5
  (between H5 and H7), out under H4's raised bottom edge, and on to the module.
- Step 34: H7 over the buttons (still turned over, as H5 and H6).
- Steps 35 - 41: the case the right way up: H8; one piano key (H9) slid in from the front, then the other three; H10 hooked into H4 and
  lowered (the keys' camera for all three, close); H11 and H12 down into H10 and back into H4 (each from a front corner, close); H13
  down its slope.
- Steps 42 - 47: the electronics into the case, each picked up first (an eye), then placed: the I/O module held over the back of H4
  (Step 42, seen from straight behind: the module, all it carries, the USB cable's A end and every wire fade out on the bench and
  fade in where the step leaves them, a beat each: Lee's fifth round, this step only)
  and lowered onto it (its label to its left); the 4-digit display passed under the dot matrix display's wires into the space
  behind the module, lifted up behind the case, over the top and held over its place, a beat for each, in one step (Step 44), then
  lowered into the notches of H11 and H12 (Step 45); the dot matrix display lifted,
  carried over the case and held in front, a beat for each (Step 46: the USB cable moves out over its wires), then hung on the hooks
  of H11 and H12 (Step 47).
- Step 48: H14 over the 4-digit display: its two bottom tabs set down onto the top edge of the dot matrix display (lead lines and a
  close-up on them), then its top swung in. The Completed View shows the game from the front, on the student's right, seen from
  where the title page sees it, the model in the middle (Lee's sixth round).

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
  it settles in; in Step 33 the push buttons' wires touch H5's edge by up to 0.7 mm for a moment. (A riding part's in-between stops then played within one 0.8 s beat: a beat each since the second round.)
- Parts list pictures: the I/O module and the Nano Board from their component side; the yellow push button; H5, H6, H7, H9, H10 and
  H13 the right way up; H14 face on.
- Cameras changed where Lee asked (and nowhere else, checked view by view against the first draft): Step 16; Steps 21 - 25; Steps
  30, 31 and 34; Steps 37 and 38 (Step 36's); Steps 39, 40, 41; the framing of Steps 44 - 45 and 47, whose motions changed.

LEE'S SECOND ROUND (19 Oct 2026, late; docs/research/pmg/round2_plan.md). Lee's step numbers are the first round's; since this round
its Steps 44 and 45 are one step (44), so its Steps 46 - 49 are now 45 - 48.
- The push buttons' wires (Steps 4 - 15): the module pin's label up and to the right of its pin; the camera a little higher (solved
  from Lee's screenshot).
- The 4-digit display's wires (Steps 17 - 20): from behind and above (its printed pin names, the module's pins), its wires in front
  of the buttons' from there, each loose wire between the display and the module; the plug-in motions no longer cross other wires.
- The dot matrix's wires (Steps 21 - 25): higher (as Lee's screenshot of Step 22), the module's labels to its left, the matrix's
  below it (its name on its face, by the header), each loose wire between them, across the gap. Its input header as on the real board (Lee's photo 6): the five pins now reach 6.4 mm past
  the board's edge, and their tails behind it are 1.5 mm (make_source.py; the five caps moved out with them).
- Lee's own lead-line points: Steps 30, 31, 34 (H5, H6, H7 into H2 and H3), 37 (the keys into H4), 48 (H14 over H11 and H12).
- Steps 32 - 33: each button moved clear, lifted above the case, carried over, pressed in (it passed through H5).
- Steps 35 - 38 closer; Step 43's label to the left of the module.
- Steps 44 and 45 of the first round combined (the display under the matrix's wires, a pause, then up, over and held); Step 46 (the
  dot matrix) slower: a beat for each stage, as the player now allows a riding part (`ride_beats`, opt-in; checked on every kit).
  The USB cable moves out over the dot matrix's wires during Step 46 (it no longer runs between them and the case).
- Labels can now be told where to sit (`side`, opt-in in the player): used for the pin labels, the module's and the eyes above;
  the push buttons' names (Steps 4, 7, 10, 13) up and to the right, as the module's pins.
- Found while checking this round (not in Lee's notes): in Steps 17 - 25 the module's cap passed through the I/O board and the Nano
  Board on its way from the bench to its pin (and in Steps 22 and 25 a matrix wire touched another as it settled in). Both
  displays' wires now go in as described above (a beat for each stretch, so these steps play longer: 3.2 s and 2.4 s); no cap
  passes through a part or a wire (docs/research/pmg/scripts/check_caps.py, a check of every moving cap added this round).
- An independent review of the finished round (20 Oct 2026: the labels at four window sizes, from an iPad in portrait and the LMS's
  frame on a laptop to Lee's own, and the step-list pictures; and the new motions, replayed finely) found, and this was fixed:
  the push buttons' names further out (at the LMS's size the caption box pushed White Push Button down onto its VCC label) and the
  yellow, white and blue buttons' pin labels on their right (the yellow's ran across the black button's caps); Step 4's caution box
  folded into its caption (in the LMS's frame the box hid the black button); in Steps 21 - 25 the module's labels closer to the
  module (they sat on the dot matrix's header and its printed pin names, and the leaders crossed), the matrix's lower, its name
  further along it, the eye clear of the loose wire; in Steps 18 - 20 the display's cap no longer passes through the wires already in
  as it comes to its pin (it did for a fifth of a second), and in Steps 17 - 20 the carried cap stays clear of the caption box; in
  Steps 21 - 25 the module's cap slides higher over the pins; in Step 33 the buttons move further clear before rising (the white one
  rose through the blue one's wires). docs/research/pmg/scripts/check_caps.py now paces each beat as the player does and samples
  201 moments per motion (19 had missed the display's crossing). A second review of the fixes (pictures in round2/verify2 and
  verify3) tuned them: each button's name as far out as the LMS's size needs, no further (the leaders were long on Lee's screen);
  the dot matrix's VCC and GND labels lower still (on an iPad they sat on the board's corner); the display's module cap carried
  lower and its wire flatter (its loop still touched the caption box), the lifted wire sagging (straight, it read as lying on the
  board); the matrix's S-column caps higher (they read as among the pins); the buttons 26 mm clear and the other three 8 mm along
  the row (30 mm brought them within 2 mm of H5's tongue, and the white wires still grazed the blue ones).
- Not changed, for Lee: in the LMS's frame (narrower than Lee's window) the caption box covers the top of the push buttons in
  Steps 4 - 15 (the camera Lee asked for puts them near the top); only a camera change (the same angle, framed a little lower when the
  window is narrow) would clear it. In Steps 7 - 15 a button's pin labels (now to the right) have leaders that pass just over the
  bare OUT and GND pins; a dashed ring on the pin would mark which pin is meant, but pin labels have no ring (Lee, 14 Oct, the MRA).
  In Steps 11 and 14 the OUT wire passes the VCC wire for a moment as it is lifted to its pin (the white by half a millimetre, the
  blue through it), older than this round, found by the finer check: for the white and blue buttons the OUT pin lies beyond VCC's
  wire as seen from where the loose wire lies, so the way in has to be planned again (as the displays' were) to go round it.
- Checked: every view (no wire in a part or through another), the motions, wires and moving caps (round2/motion_check.txt, which
  lists what is left while steps play), labels at four window sizes (none overlapping, crossing or under the caption), the run-through
  on all 99 views in the kit and as published to the test website, and every other kit's run-through with the changed player.

LEE'S THIRD ROUND (20 Oct 2026; Lee's step numbers are the guide's as it was, and are unchanged)
- Steps 19 and 20: the module's pin (V9, G9) was hidden by the other wires: from Steps 17 - 18's side the display's own wires and
  caps, on S8 and S9, stand in front of it. A camera lower and further round towards rows 10 - 13, found by a ray test of every view
  direction against the new wire's two caps as they sit once plugged in, past every wire and part on screen (round3/scripts/
  cam1920c.py): about half of each cap in view, at the module and at the display (Steps 17 - 18's camera: 0 - 7 % at the module; round
  3's first try, reviewed: 55 % at the module but 17 % at the display, whose printed back it saw almost edge on). The run of four
  display wires so has two cameras (the rulebook's section 9 holds one camera for a run; Lee asked for this one). The display's back is
  seen at 63 degrees from the line of sight (Steps 17 - 18: 58), but from here the header's pin stubs lie over the printed names beside
  DIO, VCC and GND: only CLK can be read, and only at 1920 wide. The VCC and GND labels name the pins instead. No direction sees both
  pins and the printing squarely (the cost of seeing V9 and G9; a close-up of the printed header, as Step 3's card, could show it).
  Steps 17 and 18 keep their camera. The labels placed for it: V9 and G9 to the left of the module, VCC and GND just below and to the
  right of the display's pins (clear of the wires, the boards and the parked wire's cap at the four window sizes).
- Step 33c: the buttons named by colour once they are in the case upside down (Blue, White, Yellow, Black on the left, each to its own
  button's back, in the caption's order, blue to black; given to a screen reader with the step: the Read aloud button reads the caption
  only). Lee asked for each button named by colour; done as one label per button, all on one side. Labels on a Step Nc are new
  (`labels_done=`, opt-in; no other kit has any): an exception to the rulebook's "Step Nc is clean" and to its label rules (only on
  Step N, two at most, never a part name or a colour), recorded in its section 13.
- Step 37: its three lead lines as Step 36's, one per key (from the key's end to its slot in H4, just above the buttons' tops; Lee's
  points of the second round ran just below the tops, over the caps).
- Step 42: seen from the front of the case (which hides the buttons' wires behind H4), a beat each (10 x 0.8 s), framed 20 mm higher
  than round 3's first try so that the USB cable's end can be carried over the module in sight. The module is lifted straight up off
  the bench and turned in thirds to where it is held over H4. While it is lifted and turned two thirds of the way, every wire keeps
  the shape it had on the bench and is bent with the module (wholly from where it lies over the module, the Nano Board or the plug,
  less and less towards its far end: `b_whole`, a route setting new this round, opt-in), so that no bit of a wire jumps between the
  stops; in the last third the wires take their shapes over H4, the board then turned away from the camera. Then the USB cable's A
  end on its own: lifted off the bench and turned the right way up, carried back over the dot matrix display, across above the
  module, over to the left of the 4-digit display, set down on the table there and slid in under the display's end to its place, its
  cable end staying in front of the display's wires all the way. The cable comes out of the plug in a loop lying across the view (it
  was a flat 'paddle' seen edge on), its run by the plug turning with the plug; at the turn's stops it is drawn a third and two thirds
  of the way from its lifted shape to that loop, so that it changes shape gradually (from one stop to the next it folded into a
  hairpin). Everything stays below the caption box at the LMS's and an iPad's size (the iPad's narrow frame still cuts the dot matrix
  at the right edge).
  What is left (round3/verify3/motion_check_201.txt, 201 moments): nothing passes through anything in the lift or in the A end's six
  beats. In the turn, 102 contacts (the first try's 123; its 21 'module box' lines were false): 8 in its first third, 34 in the second,
  60 in the last. In the middle third (0.2 - 0.3 of the motion, about a fifth of a second), in the middle of the view, the dot matrix's
  five wires pass through the corner of the USB plug (up to 4.4 mm, more than a wire is thick) and under the board's edge (3 mm) and
  the Nano Board (0.9 mm): on the bench they run over the plug, close to the matrix's own pins, and as the board turns the plug's
  corner sweeps through that short run. The buttons' wires dip up to 1.4 mm into the board by their caps, and the USB cable touches the
  case's back corner once (1.3 mm). In the last third the bundles change from lying side by side (on the bench) to nesting one outside
  another (over H4) and pass one another (56 of the 79 wire-against-wire contacts), mostly behind the turned board or H4. The cable's
  drawn length grows from 76 to 340 mm over the module's four beats and is 121 - 249 mm on the A end's way; like every lead in the
  guide, its length is representative.
- Two independent reviews of the round (20 and 21 Oct 2026: round3/verify/, round3/verify2/; their findings checked by second
  reviewers before anything was changed) found, and this was fixed: Steps 19 - 20's first camera saw the display's back edge on, and
  the VCC / GND label then sat on the parked wire's cap at 1440 x 714; in Step 42 the USB cable passed through the 4-digit display's
  wires as its end was set down and went under the caption box at the LMS's size, the plug and the Nano Board rose into the
  display's and matrix's wires, the wires dipped into the board as it turned, the cable folded flat at the plug, the A end passed
  behind the module's top and then hung over the display's header as if plugged into it; Step 33c's labels were not recorded as an
  exception in the rulebook; in the generator, a labels_done mapping {id: text} lost its text, a single-view step dropped it silently,
  and a Part guide would have mixed the two views' labels; check_caps.py did not test the Nano Board, the plug or the caps against
  the case as the module moved, took the module's own box for wires passing through it, and dropped the A end from one test. The
  scripts behind this round's figures are in round3/scripts/.
- Not changed, for Lee: Step 33c's framing (its camera unchanged since round 2) puts the USB A end's tip (LMS frame) or the top of the
  dot matrix (iPad portrait) under the caption box; Steps 4 - 15 likewise (asked after round 2). The A end's place on the table (just
  under the 4-digit display's header end, pointing away from the camera, from Step 42 to the end, as Steps 43 - 51 have it): from
  Step 42's camera it reads at rest as if attached to the display's header (the display's caps lie across its neck), until the
  display is picked up in Step 44; moving it would change Steps 42 - 51. A third check (21 Oct) found the cable's hairpin, its curl
  beside the A end and the dot matrix's VCC wire lagging through the other four in the lift: fixed as above.
- Checked: every view at rest (tools/wirecheck.py: no wire in a part or through another, 99 views); every motion, wires and moving
  parts (check_caps.py, 201 moments: only Step 42c differs from the first try, and Step 43c, where two of the blue button's wires now
  touch H7 by 0.2 mm for a moment, inside the case); labels at four window sizes (48 labelled views: none
  overlapping, crossing or under the caption box) and the step-list pictures; Step 42c frame by frame at 760, 1000 and 1920 wide
  (round3/verify3/raw); cameras changed only on Steps 19, 20 and 42 (both views of each); the run-through on all 99 views in the kit and
  as published to the test website; and every other kit's run-through with the changed player (MRA 211 views and its deconstruction
  151, RCC 61 and 42, LAC 116, LSM 82).

LEE'S FOURTH ROUND (21 Oct 2026; Lee's step numbers, unchanged)
- Steps 17 - 20: on each Step Nc, a close-up from above of the I/O module's pin the wire has just gone onto (S8, S9, V9, G9), its cap
  boxed in red among those already in, the printed row numbers and S / V / G beside them (as the LAC's breadboard holes; recorded in
  the rulebook's section 6, as Lee asked it). Steps 19c - 20c turn it as their own camera is turned, and put it on the module's left,
  beside the pin, its leader not across the module (from 1000 px wide; at 760 px see the review below).
- Steps 21 - 25: each dot matrix pin's label (VCC, GND, DIN, CS, CLK) to the right of its pin, just under the wire put in the step
  before (VCC, the first, up and to the right); the module's labels up and a little to the right of where they were, still to the
  left of the wires (G11 a little nearer its pin than the others; S11 too, though not named: where it was it met DIN at the LMS's
  size); the eye to the right of the loose wire, a little down it, clear of the module's corner. Clear of one another at four window
  sizes.
- Step 27: H1's label above H1.
- Step 42, as Lee asked: the module through the gap between the dot matrix display's wires and the blue push button's, the USB cable
  up with it and settling between the black push button's wires and the 4-digit display's; in five beats (4 s; round 3's took ten).
  (1) The module lifted and spun flat a quarter turn, its USB end swinging through that gap towards the case, while the USB cable's A
  end is lifted straight up out of the corner; (2) the module stood up onto H4 while the A end goes up with it, over the module's top
  to the display's side; (3) the A end straight down there, clear of the display's wires; (4) set down beside the 4-digit display;
  (5) slid in under its end. While the module spins, the wires keep their bench shapes, bent with it; the dot matrix's turn to come
  straight up out of their pins (below).
- Step 42 seen from behind again, as Steps 41 and 43 are (Lee, the same round: "from behind the model instead of up and above it"):
  straight behind, between their two corners, the module's face square on, framed so that everything moving stays clear of the
  caption box at four window sizes (round4/scripts/fit42.py). From behind, the round's first try (made for the view from the front)
  showed what the front had hidden, and this was changed: the dot matrix's wires, which on the bench come in over the USB plug, stood
  up with the plug as the module stood up and folded into a tent above it (now, while the module spins flat, they turn to come straight
  up out of their pins, and so turn out of the module's face as it stands up, as they come out of it over H4); the A end, carried across
  below the module's top, passed between the wires and H4 and then down across the display's wires (now over the top and straight
  down the display's side); and the cable folded into a hook at the plug (now it rises out of the plug and runs straight to the A end).
  What is left (round4/verify/motion_Step42c_final.txt, 201 moments): 104 contacts, all in the first two beats (round 3: 102; this
  round's first try, from the front: 109); the A end's three beats touch nothing. In the first beat (0.07 - 0.12 of the step, about
  0.2 s), as the module spins: the dot matrix's wires pass into the module's corner, the Nano Board and the USB plug (12 contacts, the
  deepest 4.8 mm, CS into the Nano Board at 0.10; round 3's deepest anywhere in the step was 4.4 mm), and the USB cable into the top
  of the case at the back (H10 2.4 mm, H11 2.1 mm, H13 1.5 mm, H4 1.2 mm, at 0.09 - 0.10): the price of the shapes changing there
  without folding (the review, below). In the stand-up (0.23 - 0.34, about half a second) the buttons' four bundles, side by side on
  the bench and nested one outside another over H4, pass through one another (54 contacts), wires within a bundle pass into one
  another (28: 10 of them the dot matrix's, 6 the 4-digit display's, 12 the buttons'; of all 82 wire contacts, 69 have centre lines
  closer than a wire's radius), and the blue and white buttons' wires dip into the module by up to 1.4 mm (6, at 0.29): from behind
  this is in view (from the front, H4 hid it). As the A end crosses over the module's top, the cable folds for a moment (0.30 - 0.35,
  about 0.2 s; 138 degrees within 3 mm): the plug's cable comes out towards the display's side, so with the A end on the matrix's
  side it has to turn back, and it straightens as the A end crosses. The first beat's sharpest bends are now among the module's pins
  (round4/verify/shapes42.txt). At the start the A end lies behind the dot matrix display, out of sight from behind, until it is lifted.
- An independent review of the round (21 Oct 2026: round4/verify/review_raw.json, with the pictures it looked at in round4/verify/raw;
  four reviewers, each finding then checked by a second before anything was changed) found, and this was changed: in Step 42's first
  beat the dot matrix's wires zigzagged just past their header and the USB cable stood up in a hairpin above the plug, in the open
  (each changed into a shape more than twice as long, and the shorter one's points bunched where its two runs were matched; now matched
  from the first end along all but the last 3 mm, guide.py's head_first: the bunching falls among the module's pins and, for the cable,
  at the A end, behind the dot matrix display); G11 in Step 22 had moved more than "a bit" and sat over the brown wire (now up and to
  the left of its pin, nearer than before); the close-up's leader in Steps 19c - 20c ran across the module and the caps just put on,
  against the rulebook (now on the module's left, beside the pin; at 760 px, an iPad in the LMS, there is no room beside it, and the
  close-up sits at the top left, over the left half of the 4-digit display, its leader straight down to the pin); the rulebook's new
  entry claimed more than Lee asked (narrowed to what Lee asked); and this account left out the contacts into parts and the first
  beat's folds.
- The player, every kit: a close-up no longer covers the place it shows (on its side, with no room beside it in a narrow window, Steps
  19c - 20c covered their pin; it now goes higher or lower on that side, or smaller). Of the other kits' 13 close-ups at four window
  sizes, only the LSM's Step 36c at 760 px covered its own place (the D11 tab through D1, hidden): it now sits lower on the left with a
  short leader; every other close-up is where it was (each measured with the old rule and the new). Recorded in CLAUDE.md.
- Checked: every view at rest (tools/wirecheck.py: 0 problems in 99 views); every motion, wires and moving parts (check_caps.py, 201
  moments: only Step 42c differs from round 3); labels at four window sizes (48 labelled views: none overlapping, crossing or under
  the caption box); cameras changed only on Step 42 (both views), checked view by view against the guide as it was before the round;
  the close-ups at four window sizes; the run-through on all 99 views in the kit and as published to the test website (http://localhost:8799, release r8); and every other kit's run-through with
  the changed player (MRA 211 views and its deconstruction 151, RCC 61 and 42, LAC 116, LSM 82: no problems).

LEE'S FIFTH ROUND (21 Oct 2026, after the fourth)
- The title page: the model to the right of the middle, as the MRA's (it sat left of it). The player frames the title page itself (as
  big as the window allows, clear of the logo and the title); the guide now says which way it prefers among frames as big (shift 0.7
  of the view's radius): the model's middle 59 - 67% across in landscape windows (it was 44 - 50%), the same size. The player does
  this by moving the camera aside, which on its own showed the model 16.5 degrees round (H11 and the cable's loop went out of sight:
  the review, below); the camera's direction is turned back by as much, so the model is seen from exactly where it was in every
  landscape window (measured: 0.0 degrees at 1920 x 1000, 1440 x 900, 1000 x 634, 830 x 460 and 760 x 720). A phone held upright,
  where the model fills the width and is not moved aside, now sees it 12.5 degrees round.
- Steps 21 - 25: on each Step Nc a close-up of the module's pin the wire has just gone onto (V11, G11, S11, S12, S13), its cap boxed
  in red, as Steps 17 - 20's, seen from above and from the G side (straight from above, as 17 - 20's, the wire just put on V11 rose
  between the camera and G11: Step 22c's showed only that wire). On the module's right: on its left, the pin's side, the close-up covered the dot matrix
  display (in an iPad's frame, its header too, where the wire's other end is); on the right both devices stay in view at every
  window size, and its leader runs along the module's top edge to the pin (an exception to the rulebook's close-up placement,
  recorded there).
- Step 42, as Lee asked, for this step only: nothing moves. The module with all it carries (the Nano Board, the plug, the caps), the
  USB cable's A end and every wire fade out where they lie on the bench (one beat, 0.8 s) and fade in where the step leaves them, the
  module held over H4 and the A end on the table behind the case (a beat); going back, the same the other way. The published guides
  move wired things so too (rulebook section 4: complete copies cross-fade); this guide otherwise moves them, and its other steps
  still do. Recorded in the rulebook as Lee's exception. The camera is round 4's, from straight behind (framed for the way the module
  used to take; it could now be closer, unasked). Round 4's way is kept in guide.py behind STEP42_REAPPEAR = True: set it False and
  run guide.py to see it again.
- The player, every kit: a step may ask for this (`reappear`, guide.py's g.place(..., reappear=True)): what changes place, and its
  wires, fade out where they are and in where they end. Next or Prev pressed during it takes things on from where it ends (or, back,
  where it began), never through the wires. No other guide asks for it; tools/motioncheck.py, check_caps.py and check_motion.py
  skip such a step (nothing passes through anything).
- An independent review (21 Oct 2026: round5/verify/review_raw.json, its pictures in round5/verify/raw; three reviewers, each finding
  checked by a second) found, and this was changed: Step 22c's close-up showed only the VCC wire (now seen from the G side); the title
  page's model was seen 16.5 degrees round (now turned back); Next or Prev during Step 42's fade-out made the module glide through the
  wires into the next step (now it starts from where the fade would end).
- Checked: every view at rest (wirecheck.py: 0 problems in 99 views); views compared with the guide before this round, by content:
  only the title page (its camera), Steps 21c - 25c (the close-ups) and Steps 42 - 42c (the fade) differ; Step 42c's fade frame by
  frame forwards and back, and Next or Prev pressed half-way (where the module is, to the millimetre); the close-ups at four window
  sizes; the title page at 1920 x 1000, 1440 x 900, 1440 x 714, 1000 x 634, 830 x 460, 760 x 720 and 375 x 812; the run-through on all
  99 views in the kit and as published to the test website (http://localhost:8799, release r10); and every other kit's run-through with
  the changed player (MRA 211 views and its deconstruction 151, RCC 61 and 42, LAC 116, LSM 82: no problems).

LEE'S SIXTH ROUND (21 Oct 2026, after the fifth)
- The title page: the camera solved from Lee's screenshot of it ("On the starting view / completed view, let's go for this camera
  position / zoom"; asked for both views, then the Completed View centred, below): the game from the front, on the student's right,
  a little lower than before (dir [-0.7723, 0.4726, 0.4246], target [522.7, 912.3, 1235.3], radius 113.6, shift 0). In a window the
  shape of Lee's the model lands where the screenshot has it (across 40 - 79%, down 11 - 89% of the picture above the bar); 59 - 66%
  across in landscape windows, 78% of the height, seen from exactly that direction. In windows near square or upright the player
  moves the camera aside, as it does for every title page, where that lets the model be bigger: 1 degree round at 900 x 880, 8 on a
  phone held upright (where the model fills the width). The fifth round's shift and turned-back direction are gone.
- The Completed View, centred (Lee: "Centre the model on the Completed View; keep the title page as it is"): seen from the title
  page's eye (3.4 mm from it in windows 1.2 times as wide as the picture is tall or more: every landscape size measured; 6 mm at
  900 x 880, where the title page is moved aside 1 degree), turned to look at the model's middle (dir
  [-0.8363, 0.459, 0.2999], target [546.0, 915.1, 1274.2], radius 113.6, as the title page's). The model is in the middle across and
  down at every window size, 75 - 76% of the height in landscape windows (the title page's, off to the side, is stretched a little
  by the perspective to 78%); the same faces show as on the title page, the picture turned about 4 degrees more level (the camera
  turned to the model's middle). Moving the camera sideways instead (tried first) would have shown the model 8 degrees round. The
  player hardly moves the Completed View aside in any window (6 mm on a phone held upright, 0.6 degrees from Lee's view), while the
  title page, moved aside there, is 8 degrees from Lee's view: on a phone the two views are 7 degrees apart. The website's card picture is made again from it.
- Step 42: Lee keeps the fade ("Let's keep the fade on 42"). Round 4's way is still in guide.py behind STEP42_REAPPEAR (its shapes
  are the ones the fade ends on); the guide is unchanged there.
- Checked: views compared with the guide before this round: only the title page's and the Completed View's cameras differ; both
  views at 1920 x 1000, 1440 x 900, 1000 x 604 (Lee's window), 1000 x 634 in an LMS frame (?embed=1), 760 x 720 and 375 x 812 (the
  logo and title clear; the Completed View centred, and half-way through its glide from Step 48c); the run-through on all 99 views
  in the kit and as published to the test website (http://localhost:8799, release r12). An independent review (two reviewers,
  21 Oct 2026, the cameras re-projected from the model's own points) found no fault in the cameras and corrected this text: where the
  player moves the title page aside, and the 4-degree turn.

THE DECONSTRUCTION (first draft, 21 Oct 2026)
Lee: "take this PMG Full Build guide and create a Deconstruction Guide based on it. Same principles as you used for the MRA.
Remembering some things can be removed in groups (like the breadboard wires, four buttons, four H9 parts, etc.)". deconstruction.py
-> steps-deconstruction.json (26 steps), made from the Full Build as guide.py last wrote it: run it again after every Full Build
change. Its title page is the Full Build's, it ends on H1 followed by the Full Build's two parts list pages (as the MRA's), and its
card on the website is the Full Build's. The order is the Full Build in reverse, in the order of TechBox's own published PMG
take-apart where it has one (docs/research/guide_19075-piano-memory-game-deconstruction.md); the reasons for each choice are in
docs/research/pmg/deconstruction/ (the Full Build mapped step by step, the take-apart machinery, Lee's conventions).
- Step 1: the USB cable, both ends (power first, as the MRA's and the RCC's), from behind, one arrow on the plug pulled.
- Step 2: H14 (its way out points at the camera: an eye on its wood, above its window).
- Steps 3 - 8: the dot matrix display, the 4-digit display and the I/O module out of the case to the table behind it, still wired, each
  in the Full Build's two steps reversed, each by the camera of the step it undoes, the wires through the Full Build's own shapes
  stage by stage: tilted forward and lifted off its hooks (or out of its notches), then carried back over the case (the 4-digit
  display down behind it and out under the dot matrix display's wires); the I/O module lifted straight up off H4, then set on the
  table by a fade, as the Full Build's Step 42 brought it (Lee kept that fade).
- Steps 9 - 14: H13, H12, H11, H10, the four keys (H9) at once (an arrow on each), H8.
- Steps 15 - 16: the case turned over: H7, then the four push buttons out of their pockets at once, back to the table still wired.
- Steps 17 - 21: the electronics on their own, the case hidden (as the RCC's controller and I/O module): the dot matrix display, then the
  4-digit display, then the four push buttons at once, each pulled off the ends of its wires, which stay on the I/O module (as TechBox's
  published take-apart); then all 21 breadboard wires off the module at once (an eye on them); then the Nano Board out (the Full
  Build's Step 1 camera). One wide camera while the dot matrix display comes off, one closer for the rest.
- Steps 22 - 26: back to the case, still upside down: H6, H5; the right way up: H4, H3, H2. H1 is left.
- No counterpart for the Full Build's preparation (the wires peeled off the ribbon) or its Step 3 card.
- Choices Lee may want otherwise: it ends on H1, the base (as the MRA's and the RCC's; TechBox's published one ends on the bare I/O
  module, its case's last plates vanishing unexplained); the devices come off their wires before the wires come off the module (as
  published; the MRA's breadboard wires came off both ends at once); the I/O module goes back to the table by a fade. The wording
  names the parts as the Full Build does (the I/O module, the 4-digit display ...); the developer's sheet can change it
  (tools/step_text.py export ... steps-deconstruction.json).
- New in the generator and the player, for every kit (only this guide uses them): lift(..., reappear=True), a fade instead of a move,
  as place()'s; remove() / lift(..., let_go=[ids]), riders of what leaves that stay where they are (the wire ends a device is pulled
  off); the player turns a take-apart's fade round where it is when Prev or Next is pressed half-way, and a fade now leaves alone the
  parts that lie still (it compared poses as text, and a turned pose worked out again on the way could differ in the last digit: in
  this guide's Step 8 both displays faded with the module; in the Full Build's Step 42 the same 34 parts fade as before).
- An independent review (21 Oct 2026, three reviewers: pictures, order and wording, code) found, and this was changed: the wires of
  the devices pulled off vanished for two steps (their ends, let go of, were not on the electronics' own view); both displays faded
  with the module; the module's lift off H4 was faded too (now a step of its own, as the Full Build's); H11's arrow seemed to lift
  the 4-digit display behind it; H10's lay on the keys like theirs; H14's eye fell on the display's digits; the wording of Steps 3,
  5 and 22; the framing of the electronics' run.
- Checked: the run-through on all 56 views (and every other guide with the changed player: PMG Full Build 99, MRA 211, its
  deconstruction 151 and Parts 35, 50, 132, RCC 61 and 42, LAC 116, LSM 82: no problems); every step as it opens, half-way and at its
  end, at 1440 x 900 and the hand-framed ones at 760 x 720; the wires during each move (check_caps.py, 201 moments): no wire end
  passes into a part; wires of one device pass through each other in the matrix's and the display's carry, the module's lift off H4
  and the push buttons' way out, and two of the blue button's wires graze H7 by 0.22 mm half-way through the module's lift, exactly
  as in the Full Build's own Steps 46c, 44c, 43c, 32c and 33c (the same pairs and places, mirrored in time), not new here;
  the RCC's and MRA's deconstructions regenerate unchanged with the new generator; published to the test website (release r1).

THE DECONSTRUCTION, LEE'S FIRST ROUND (21 Oct 2026)
Lee: "H12 and H11's removal have the arrow going upward, which is right, but there's a motion toward H1 required first before the lift.
... The deconstruction guide is largely good, but the arrow sizes and sequencing need refinement. Examine the Cadasio linked here"
(TechBox's published take-apart, instructions.online/?id=19075-piano-memory-game-deconstruction). Its data and its 61 step pictures
were fetched (docs/research/pmg/cadasio/raw, decon_digest, decon_thumbs, decon_sheets) and every arrow measured
(docs/research/pmg/deconstruction/published_arrows.txt).
- Arrows in turn, as the published guide's auto-advancing frames swap them: a part that comes off in stages shows Step N's arrow for
  the first stage; as the step plays, the next stage's arrow appears while the first plays, and goes as its own plays. H12 and H11:
  toward H1 (from each plate's front edge), then up (from its face). H10: its front up (at its front edge), then out over the keys.
  H7, H6, H5: swung up, then out of H2's windows (the second as long as the first: ours comes 5 mm out of the windows, where the
  published plate slides 140 mm along itself). H14: its swing out comes towards the camera, so an eye on its wood as before, then its
  tabs' lift off the dot matrix display's edge as an arrow (ours leaves forward, the Full Build's way reversed; the published H14 leaves
  backward, over the stand). The still pictures (the step list, the 2D PDF) show every stage's arrow at once.
- Sizes: every arrow as long and thick as the matching published one (mostly 30 - 116 mm long, 4 - 12 mm thick), where the in-house
  rule of 18 Oct (for the MRA) was 15 - 40 mm and at most 3.2 mm. H14's lift arrow is the published first arrows' size (its 64 mm
  one ran out of this close view). Groups as published: one arrow for the four keys and for the four buttons pulled off their wires;
  an eye, no arrow, for the buttons out of their pockets (an arrow there hid a button); an arrow over each wire bundle's free ends.
  The dot matrix display's arrow off its hooks starts at its far end (from its middle it rose across the 4-digit display).
- Step order unchanged. Where it differs from the published guide: the USB cable first (power off before anything is handled, as the
  MRA's and the RCC's); each display and the I/O module in two steps (the Full Build's two, each by its own camera: our player keeps
  one camera per step); the electronics taken apart on their own between the buttons and H6, and the display before the buttons
  (the published guide finishes the case first, then the electronics on the bench left to right: buttons, then display); it ends on
  H1 (the published one ends on the bare I/O module, its H2 and H3 vanishing unexplained). Lee, asked whether the order should follow
  the published one too: "Keep the current step order; the arrows were what needed changing."
- New in the generator and the player (for every kit; only this guide uses it): arrow_style then= (arrows in turn, checked: stages
  after the first, in order, every moving part with as many) and dims=; core.js setArrowAlphas; the run-through checks such arrows (on
  before their turn, solid while due, gone after their stage, and after Prev half-way); stills draw them all. An independent review
  (two reviewers) found, and this was changed: H14's arrows ran against our motion; the buttons' arrow hid a button; Step 19's arrow
  touched the frame (the closer camera now has room above); the arrows of Steps 3, 10, 11 and 12 placed as published; the stills lost
  the later arrows; small code points (an arrow skipped for zero length shifted the others' fades; a clash of names).
- Checked: the run-through on all 56 views of the take-apart and on every other guide with the changed player (PMG Full Build 99, MRA
  211, its deconstruction 151 and Parts 35, 50, 132, RCC 61 and 42, LAC 116, LSM 82 and its deconstruction 52: no problems); every
  changed step as it opens, with each later arrow while it is due, and its still; the RCC's and MRA's deconstructions regenerate
  unchanged; published to the test website (release r2). Then H5's arrows corrected to the published 6.2 mm thick (the first measure
  took an unused arrow of the same length: the LSM session's check of every published arrow), release r3.

THE DECONSTRUCTION, LEE'S SECOND ROUND (21 Oct 2026)
Lee: "Step 7 needs a wider arrow / Step 10 - the second arrow appears too early and is partially occluded in H12 for part of the
animation. / Step 11 - Same as Step 10".
- Step 7 (the I/O module lifted off H4): its arrow 6.5 mm thick, as the published one (it was 2.1: the in-house thickness for its length).
- Steps 10 and 11: H12 and H11 now slide toward H1, rest for a beat while the up arrow fades in, then lift (the up arrow used to fade
  in while the plate was still sliding). The rest beat is the generator's (arrow_style then=), so every part that comes off in stages
  has it: H14 (Step 2), H10 (12), H7 (15), H6 (22), H5 (23), each step a beat longer. Both of H12's and H11's arrows are drawn 15 mm
  in front of the plate, towards the camera (in_front() in deconstruction.py), so the plate never covers them as it moves; the
  fading arrow no longer goes behind it.
- Checked: every changed step frame by frame through its move (the first arrow while the part slides, the second only once it rests,
  in front of the plate all through the lift); no camera changed; the run-through on all 56 views; the RCC's deconstruction
  regenerates unchanged (the MRA's has no then=). An independent review (three reviewers, each finding checked by another) found
  nothing wrong in what plays; two small points were changed: a stage= of another part in the same step is renumbered with the rest
  beats too (no guide has one yet), and stepgen.py's remove() docstring describes the new timing. The LSM's deconstruction, committed
  by its session, was made with this rest beat already (its D10, D3, D4 and cable steps). Published to the test website (release r4).
- Then Lee: "Step 17 - the arrow is partially occluded into the Dot Matrix display". Its arrow was 2.7 mm above the board's top and
  tilted towards the camera, so the lower half of its head (13 mm each side of the shaft) went into the display. Now it is 40 mm
  above the pins' ends (it was 18), its head about 14 mm clear of the top, still from the pin end along the pull. Checked at 1440 and
  760 wide; only Step 17 changed, no camera; the run-through on all 56 views. Published to the test website (release r5).

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
  fixed: critic.md for the first draft, round1/ for the first round), the run-through check on all 99 views, in the kit and as
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
(The first draft's question 5, the boards' printed pin names, was answered by Lee's photos: done. The first round's question 8, a beat
for each stage of a carried part, was answered in the second round: done, as an opt-in that changes no other kit.)
