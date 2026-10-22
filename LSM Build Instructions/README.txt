LSM Build Instructions (Laser Stem Matrix, Full Build: the electronics on the open base, the housing, the LED matrix, shelves and stems)

FIRST DRAFT 19 Oct 2026; LEE'S FIRST ROUND OF NOTES DONE THE SAME DAY (docs/research/lsm/lee_notes_2026-10-19.md), AND THE SECOND
ROUND THAT EVENING (docs/research/lsm/lee_notes_2026-10-19b.md, with what was done for each note); THE THIRD ROUND 20 Oct 2026
(docs/research/lsm/lee_notes_2026-10-20.md: a new D3, D8 seated higher, the V+ wire yellow, Steps 3, 6, 28 and 32); THE TITLE
PAGE AS LEE'S PICTURE OF 21 Oct 2026 (docs/research/lsm/lee_notes_2026-10-21.md: the box closer and to the right of the middle); THE
DECONSTRUCTION 21 Oct 2026, REBUILT THE SAME DAY ON TECHBOX'S PUBLISHED TAKE-APART AT LEE'S WORD (deconstruction.py ->
steps-deconstruction.json; see THE DECONSTRUCTION below); "gray", not "grey", across the kit (Lee); LEE'S NOTES ON THE
DECONSTRUCTION OF 22 Oct 2026 DONE, BOTH SETS (docs/research/lsm/lee_notes_2026-10-22.md and lee_notes_2026-10-22b.md). Build
instructions generated from Lee's STEP files and TechBox's published Cadasio guide for the kit
(instructions.online/?id=19075-laser_stem_matrix_lsm_-_full_build), in the same format and with the same player as the MRA and RCC
guides. Not for distribution. The open questions are under QUESTIONS FOR LEE below.

HOW TO OPEN (Mac)
1. Double-click "Open Prototype.command". A Terminal window opens and the guide opens in your browser (port 8805, so it can run
   beside the other kits). If macOS says it cannot be opened: System Settings > Privacy & Security > "Open Anyway".
2. When you are done, close the Terminal window. The website version (as learners would see it): http://localhost:8799/laser-stem-matrix-full-build/
The controls are the MRA guide's: arrows step through, drag to rotate, scroll to zoom, Option-click a spot to copy where it is.

THE MODEL
Lee's STEP files do not hold a working assembly: the Full Build STEP lacks the Nano, D4 - D10 and the stems (and six of its
sub-assemblies point at missing files); the two newer files have each part once, laid out loose. The published Cadasio guide holds
the whole assembly in the same coordinates, and every part in Lee's files has the same own frame as Cadasio's copy, so assemble.py
takes each part from Lee's files and puts it where Cadasio has it: lsm.glb, which the guide is generated from. The details, and the
sub-millimetre corrections made to Cadasio's placements, are in docs/research/lsm/cad_study.md.
- From the MRA (Lee, 19 Oct 2026: use the MRA's or RCC's version where they have the part): the Nano Board, the USB cable's A end
  and the jumper wires' female caps (the same models), with the MRA's colours for the Nano.
- The LSM's own: the wood D1 - D11, the breadboard, the LED matrix, the resistors, the capacitor, the push button and its nut, the
  jumpers' male pins, and the right-angle Mini-B plug (the MRA's is straight, and a straight plug would run into the push button).
- The 64 LED stems are drawn as plain 3.175 mm square rods 66.675 mm long (Cadasio's size): their CAD is not in the files yet.
- The breadboard's joining tabs on the sides the real one has them (Lee, 20 Oct 2026): two on the a side and three on the row 30 end
  (the CAD has them on the j side and the row 1 end); assemble.py moves them and closes the openings.
- D3 is Lee's updated part (LSM_D3.STEP, 20 Oct 2026, converted to lsm-d3.glb): 3.0 mm thick (the first was 3.175), longer end tabs,
  the latches' spring cuts and the slots reshaped; placed where the first D3 was (the same part frame).
- D8 sits with its top just under the D11 posts' top latches (Lee, 20 Oct 2026; Cadasio had it 2.1 mm lower). D8 is 3.17 mm thick in
  the CAD and the posts leave 3.0 mm for it, so it sits 0.19 mm into the ledge under it, out of sight.
- Colours: the published guide's, solid by solid (colour-atlas-lsm.json, made by make_atlas.py), the MRA's for the Nano; the LED
  matrix's V+ jumper wire yellow, not the published white, which was too like the light grey one beside it (Lee, 20 Oct 2026). D2 is
  plain wood like the other walls (Lee read the published guide's brown outer face as bad lighting). The capacitor is painted by
  region (black can, silver ends, silver stripe over the negative leg): the published guide's silver layers let black show through
  on its top. The wood is roughened as on every kit.
- The LED matrix (Lee's notes and photographs, 19 Oct 2026): its pin header made again as the real one is, a right-angle header
  lying flat on the back at one corner, its three pins (V+, IN, V-) pointing in along the board and their tails soldered to pads at
  the edge; the back printed as photographed, with the white label V- IN V+ beside the pins (silkscreen.py -> decals.json); of the
  board's own print only "24 bit color" and "64 RGB LEDs" are kept (Lee's second round). The LED at the corner under the header was
  white all over: in Lee's STEP its window is fused into its body, so materials.json paints that spot grey like the others. The
  matrix rests on the two D9 (the published assembly left it 1.1 mm above them), D10 is centred between D4 and D5, and the USB
  cable's A end lies 60 mm further out, so that D4 slides on over the cable rather than through the A end.
Commands (from the project folder), after a change to the CAD or the guide:
    .venv.nosync/bin/python tools/step_to_glb.py "LSM Build Instructions/LSM_D3.STEP" "LSM Build Instructions/lsm-d3.glb"   # a new D3
    .venv.nosync/bin/python "LSM Build Instructions/assemble.py"      # lsm.glb, after a new STEP (convert it first, see assemble.py)
    .venv.nosync/bin/python "LSM Build Instructions/make_atlas.py"    # colour-atlas-lsm.json
    .venv.nosync/bin/python "LSM Build Instructions/silkscreen.py"    # decals.json (the matrix's printing and label), then build_model
    .venv.nosync/bin/python "LSM Build Instructions/guide.py"         # steps.json, parts.json, model.glb
    .venv.nosync/bin/python "LSM Build Instructions/deconstruction.py"   # steps-deconstruction.json, from steps.json: after every guide.py
    /usr/bin/python3 tools/serve.py "LSM Build Instructions" 8805     # then http://localhost:8805/player.html

THE BUILD (40 numbered steps; the published guide's 38 and its order, with the house rules applied)
- The title page: the finished box from D5 and D2's corner, without the USB cable, large and to the right of the middle, as Lee's
  picture of 21 Oct 2026 (its camera solved from it); in a window taller than wide it is centred.
- Steps 1 - 9, the breadboard: backing peeled off; onto D1; the Nano Board in rows c and g, columns 2 - 16, USB socket at column 16
  (pin D12 in c16, as Part 1 of the published guide has it; c16's leader comes in from the side, across its red lead line, not along
  it); the 12 kOhm resistor's legs bent, into h3 and h16; the capacitor on its own, turned as Lee's capacitor picture shows it (stripe
  and GND leg on the left), its legs labelled GND (-) and VCC (+) underneath, with the picture as the close-up on its right, then into j2 and j3,
  stripe in j3, seen the same way round; the 330 Ohm resistor's
  legs bent, into a11 and a19.
- Steps 10 - 17, the LED matrix's wires: the three-wire ribbon's ends pulled apart; the yellow, grey and purple pins into i2, i3 and
  b19, one per step (i2 and i3 from Lee's framing; the yellow and grey wires stay side by side as a ribbon, leaving their pins away
  from the row, so that neither crosses the other's hole); the LED matrix turned over, its three pins labelled (each named at a
  different place along it, so that the leaders do not cross), with a close-up of the header and label; then the matrix held upright
  over the breadboard, header at the top, and the yellow socket onto V+, the purple onto IN, the grey onto V-: each step names the
  pin and the hole the wire's other end is in, with an eye on the socket.
- Steps 18 - 24, the button and the USB cable: the button's nut off (turning two turns as it comes off; the arrow from the nut's back
  face); the button through D2 from its engraved side; the nut back on (turning); the red lead into j5 and the black into j16, one per
  step (the black from Lee's framing); the USB cable's Mini-B plug into the Nano, its cable out to the A end on the table; D2 stood on
  D1 (Steps 23 - 25 share one camera, closer than the first draft's).
- Steps 25 - 28, the housing: D4 lowered from above beside its place (the USB cable in the notch at its foot), then pushed 8 mm on
  over the tabs of D1 and D2 (they go through closed slots in D4, so it cannot come straight down into place); the LED matrix lifted
  over D4 and laid outside, seen from above with an arrow, turned on the way so that it lies the right way round for Step 30 (four
  beats: up, over the D2 end turning, out turning, down), its wires over D4's top edge; with the box turned over, D3 hooked into D4
  and swung shut, then D5 (from the corner where its code is; lead lines at Lee's points on D1 and D2).
- Steps 29 - 40, inside and on top: the two D9 (the wires already under the engraved end of the one nearer D4); the LED matrix
  lifted straight up and moved over the box (no turn), its wires dead straight along under its edge past where D10 comes up, then
  back down between D4 and the D9; D10 hooked under it, over the wires (two beats, up then along, from Lee's framing, the arrow on
  D10's front face outside the matrix); the matrix and D10 lowered in, through a half-way shape without stopping (lead lines to the
  bottoms of D4's and D5's slots; a
  close-up of D10's end, the matrix, the sockets and D4 drawn faint, the wires dropping through its slot); D6 (a
  close-up from above of the four slots in D1 for the posts); two D11 posts, then the other two, each pair seen from the side its
  codes face, down only until their tabs reach D1; the box turned over, D1 and D5 see-through, all four pushed home (a close-up of a
  tab through D1); D7; D8; one stem; the other 63 coming in together (Steps 37 - 40 closer, near Step 33's framing).
- The wires are checked at rest in every view (tools/wirecheck.py) and at 19 moments of every move (tools/motioncheck.py): no wire
  passes into a part. For a moment while they change shape, two wires brush against each other twice in Step 26 (under the matrix)
  and once in Step 32 (low in the box by D4).

THE DECONSTRUCTION (24 numbered steps; www address laser-stem-matrix-deconstruction). Lee, 21 Oct 2026: "take this LSM Full Build
guide and create a Deconstruction Guide based on it. Same principles as you used for the MRA. Remembering some things can be removed in
groups (like the 3 breadboard wires, etc.)"; then, on the first draft (the Full Build in reverse): "you need to base the deconstruction
process off of this guide: https://instructions.online/?id=19075-laser_stem_matrix_lsm_-_deconstruction - so there are a lot of edits
needed", "The kit does have a pry tool, although it's not shown", "Let's use gray", "I think eyes instead of hole labels are okay for
this kit!"; and Lee's two sets of notes of 22 Oct 2026 on it (docs/research/lsm/lee_notes_2026-10-22.md and
lee_notes_2026-10-22b.md, with what was done for each).
So it follows TechBox's published LSM take-apart, step by step, in our model: its order, its groups, its camera for each
step, its arrows (their size, and their tail where it reads), its eyes, and a close-up wherever it has one (each catch to release),
drawn from our model with red boxes on the catch. The published guide's data, replayed in our part ids and mm, and the test of each of
its moves in our model: docs/research/lsm/decon/published/ (the numbers the guide uses: published-takeapart.json in this folder). It opens on
the Full Build's title page, ends on D1 with the breadboard (as the published one), followed straight by the Full Build's parts
list (no Completed View: Lee, 22 Oct 2026); its website card is the Full Build's.
- Steps 1 - 8, outside in: the stems (a caution: disconnect the USB cable from the computer first: the box closes round its plug); D8 off
  the posts' latches; D7; D5 and D4 off the ends (D2's tabs boxed in red at each corner, an eye on each of D3's two tabs; D4 slides out
  along the USB cable in the notch at its foot, then lifts off it; each arrow from the wall's outer face); the D11 posts two and two (their tabs pushed up out of D1 from underneath, then up through D6: a
  caution to squeeze each tab's prongs, as its barb catches under both; an eye on a post's foot, where its tab goes into D1); D6.
- Steps 9 - 13, the LED matrix and its wires (Lee's second note of 22 Oct 2026): lifted out with D10 hooked under it (D4 and D5 off, so
  D10's ends are free), its wires through the Full Build's own shapes, and held over the box; D10 slid off it, as the Full Build's Step
  31 hooked it on there, reversed (40 mm along, then down: its hooks hold both edges of the matrix, and the wires lie dead straight
  through its notch all along the slide); the matrix pulled 30 mm back along its pins off the three wires' connectors and gone, the
  connectors left where they came off and the wires in the breadboard; both D9 (the wires run under one of them); the three wires out of
  i2, i3 and b19 together, each whole (an eye on i2 / i3 and one on b19). No fades.
- Steps 14 - 19: D3 off D1's latch (the close-up's red box round both tabs of the latch); D2 with the button off D1's latch and out of its slots, still wired (seen from outside D2); the
  button's two wires unplugged from j5 and j16; the button on its own: the nut unscrewed and slid off over the wires in one smooth turn,
  the button out of D2, and the nut screwed back onto the button so that the two stay together (Lee, 22 Oct 2026): it starts just off
  the end of the wires, close up, and goes on in one smooth turning move.
- Steps 20 - 24: the USB cable; the 330 Ohm resistor, the capacitor, the 12 kOhm resistor, the Nano Board (a caution: use the Pry Tool,
  which the kit has, not modelled). The 12 kOhm resistor's arrow is the size of the 330 Ohm resistor's (Lee).
- Where it differs from the published guide, and why: in deconstruction.py's docstring (the three wires in one step; the matrix held
  over the box while D10 and the wires come off it, the D9s before the wires; D2 before its wires; D4 lifted off the cable; the nut put
  back on the button; Steps 11, 13, 15 and 20 framed to show what the published camera hid or lost; arrows moved where the published
  tail was inside a part (Steps 4 - 7, 12 and 24), where a part or the instruction boxes hid them (Steps 6, 9, 12 and 24), and to the
  nut (Step 17)).
- Checked: wires at rest in every view (0 problems) and in every move, the parts taken off and their wires included (one brief touch,
  the Full Build's own Step 32 touch played backwards in Step 9c); the run-through (51 views); every arrow on screen and no close-up over an arrow at
  1280 x 800, 1024 x 768, 1000 x 680, 768 x 560 and 768 x 1024 (22 Oct 2026, after the second notes); no arrow under the instruction
  boxes at 1280 x 800, nor at 1024 x 768 but Step 1's (question 29; Step 11's too at 768 x 560); an independent review (docs/research/lsm/decon/review2/).

QUESTIONS FOR LEE
1. The LED stem's CAD (you mentioned the acrylic stem is missing): until it comes, each stem is a plain square rod of Cadasio's size.
2. (Corrected 21 Oct 2026: in the current model the purple wire's pin in b19 is 3.4 mm from the USB plug and its wire 4.5 mm, measured
   for the deconstruction, docs/research/lsm/decon/published/feasibility.*; what follows was true of an earlier model.) The USB cable: the
   LSM's right-angle Mini-B plug (as the published guide shows it). Its leg sits exactly where the purple wire's
   pin goes into b19 (the published model has the same clash), so the purple wire is drawn passing 0.3 mm into the plug. A straight
   plug (the MRA's) would clear b19 but run into the push button. Is the kit's cable right-angle, and is b19 the purple wire's hole?
3. (Answered: the label on the matrix's back reads V- IN V+, and the guide names the pins so.)
4. The button's leads: red into j5 and black into j16, as the published guide's result shows them (its Step 19 labels have them the
   other way round). Two steps, one wire each.
5. D2 is now plain wood like the other walls. If the real D2 is a different (brown) material, say so and it goes back.
6. Cards: the capacitor's polarity and the LED matrix's pins are now 3D steps with close-ups (Steps 6 and 14) in place of the
   published guide's picture cards. The Mini USB Cable and LED Stems cards are not reproduced ("63x" is on the last step).
7. Part guides: the published LSM has Parts 1 - 4 (and 1+2, 3+4). Parts can be cut from the Full Build (g.chapter()) when you want
   them (the deconstruction, 21 Oct 2026, is a guide of its own).
8. The Nano Board's place: Cadasio moves its Nano 2.3 mm sideways in the steps; here it is in rows c and g (from the published Part
   1's "Pin D12 - c16" label and the circuit), which puts every wire on the right Nano pin. Worth a check against the real kit.
9. Step 28 (D5): D5 goes on with the box upside down (as D3 in Step 27), so its code, now in view, reads upside down. The published
   guide turns the box on its side for these two instead. Keep the box upside down, or stand it on its side?
10. Step 14: the label reads upright from this side; the board's own print (now only "24 bit color" and "64 RGB LEDs") runs the
    other way round, as in your photograph, so it reads upside down. The header's pins are drawn silver (the photograph's are gold
    at the tips). The CAD board is about 5 mm smaller than the real 65 mm board in one direction; the printing is placed by the
    mounting holes.
11. Steps 26 - 29: the LED matrix laid outside D4 is held in the air, as the published guide has it, not resting on the table.
12. (Answered, second round) The USB cable's A end in Step 23 is true to the CAD: the same model and size as the MRA's and the
    published guide's, 16 x 8.5 x 50 mm. It looks large next to the small parts on the breadboard.
13. (Second round) Step 25: D4 comes down from above, as asked, but stops beside its place and is then pushed 8 mm on: D1's and D2's
    tabs go through closed slots in D4, so it cannot be lowered straight in (the published guide pushes it on sideways too).
14. (Answered, third round) Step 28: your six lead lines, two each to D1, D2 and D3; the caption names D1, D2 and D3.
15. (Second round) Steps 23 - 25: the A end lies 60 mm further out than needed now that D4 comes from above. Bring it in (closer
    framing for these steps, the cable moved in every later step)?
16. (Second round) Step 28 now opens about 15% wider than Step 27, which you had zoomed in. Zoom Step 28 to match?
17. (Third round) D8 is 3.17 mm thick in the CAD, as the first D3 was, and its slots are 5.5 mm long, while the D11 posts leave 3.0 mm
    and their necks are 7.9 mm long: D8 sits 0.19 mm into the ledges and 1.2 mm into each post beside its slot (out of sight under the
    latch heads; Cadasio's model the same). Is there a newer D8 (or D11)?
18. (Answered) Step 6 turned to match the capacitor picture (and Step 7 with it).
19. (Answered) c16 keeps its ring on the hole, its leader across the red line; the other hole labels are as they were.
20. (Answered, Lee 21 Oct 2026) The deconstruction follows TechBox's published take-apart (b19 is free: question 2 corrected).
21. (Answered) Eyes on the unplugged wires' ends, no hole labels.
22. (Answered) The kit has a Pry Tool (not modelled): Step 24 has the MRA's caution.
23. (Deconstruction) The arrows take the published take-apart's sizes, as your PMG note asked of the PMG, with their tails where the
    published ones are, except where a tail was inside a part, or the arrow would be hidden or far from its part (Steps 4 - 7, 10 - 12,
    15, 17, 19 and 24), and like parts have one size (the D9s; the 12 kOhm resistor's as the 330 Ohm one's). The D11 posts go two and
    two, as published. The four D11 arrows keep their published sizes, a little different from each other (41.7 - 47.0 mm long,
    3.4 - 4.0 mm thick): make them one size too?
24. (Answered) D10 comes off the matrix while it is held over the box, wires still on it (Step 10; question 27).
25. (Answered) "gray" across the kit: the Full Build's captions, its caution and close-up caption, the hover names, the deconstruction.
26. (Answered by your second 22 Oct note) The matrix is no longer set down beside the box: D10 and the wires come off it held over
    the box, and nothing fades.
27. (Answered, Lee 22 Oct 2026) D10 slides off the matrix ("D10 must slide off of the LED Matrix"), held over the box, where the
    wires lie straight through its notch (laid on the table, they had passed into it).
28. (Deconstruction) The title page is the Full Build's, which leaves the USB cable off (your 21 Oct picture), so the cable comes into
    view at Step 1. Show it on the deconstruction's title page?
29. (Both guides, every kit) On a page of its own (not in the LMS frame, which shows pills instead), the instruction and caution boxes
    sit over the top of the picture, and a step's view does not move to keep clear of them. In a window 1024 x 768 or smaller, or a
    tall one (an iPad upright), the head of an arrow that points up to the top can go under them: here, Step 1's at 1024 x 768, and a
    few more at 1000 x 680 and smaller. The player could move such a step's view down just as far as the boxes need (as the title
    page already keeps clear of the logo and title), for every kit; or the arrows can be moved one by one. Which?
