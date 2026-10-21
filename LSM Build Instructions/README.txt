LSM Build Instructions (Laser Stem Matrix, Full Build: the electronics on the open base, the housing, the LED matrix, shelves and stems)

FIRST DRAFT 19 Oct 2026; LEE'S FIRST ROUND OF NOTES DONE THE SAME DAY (docs/research/lsm/lee_notes_2026-10-19.md), AND THE SECOND
ROUND THAT EVENING (docs/research/lsm/lee_notes_2026-10-19b.md, with what was done for each note); THE THIRD ROUND 20 Oct 2026
(docs/research/lsm/lee_notes_2026-10-20.md: a new D3, D8 seated higher, the V+ wire yellow, Steps 3, 6, 28 and 32). Build
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
    /usr/bin/python3 tools/serve.py "LSM Build Instructions" 8805     # then http://localhost:8805/player.html

THE BUILD (40 numbered steps; the published guide's 38 and its order, with the house rules applied)
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

QUESTIONS FOR LEE
1. The LED stem's CAD (you mentioned the acrylic stem is missing): until it comes, each stem is a plain square rod of Cadasio's size.
2. The USB cable: the LSM's right-angle Mini-B plug (as the published guide shows it). Its leg sits exactly where the purple wire's
   pin goes into b19 (the published model has the same clash), so the purple wire is drawn passing 0.3 mm into the plug. A straight
   plug (the MRA's) would clear b19 but run into the push button. Is the kit's cable right-angle, and is b19 the purple wire's hole?
3. (Answered: the label on the matrix's back reads V- IN V+, and the guide names the pins so.)
4. The button's leads: red into j5 and black into j16, as the published guide's result shows them (its Step 19 labels have them the
   other way round). Two steps, one wire each.
5. D2 is now plain wood like the other walls. If the real D2 is a different (brown) material, say so and it goes back.
6. Cards: the capacitor's polarity and the LED matrix's pins are now 3D steps with close-ups (Steps 6 and 14) in place of the
   published guide's picture cards. The Mini USB Cable and LED Stems cards are not reproduced ("63x" is on the last step).
7. Part guides: the published LSM has Parts 1 - 4 (and 1+2, 3+4). The draft is the Full Build only; Parts can be cut from it
   (g.chapter()) when you want them, and a deconstruction guide after that.
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
