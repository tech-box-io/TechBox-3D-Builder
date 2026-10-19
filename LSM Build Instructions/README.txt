LSM Build Instructions (Laser Stem Matrix, Full Build: the electronics on the open base, the housing, the LED matrix, shelves and stems)

FIRST DRAFT 19 Oct 2026. Build instructions generated from Lee's STEP files and TechBox's published Cadasio guide for the kit
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
- Colours: the published guide's, solid by solid (colour-atlas-lsm.json, made by make_atlas.py), the MRA's for the Nano. D2's outer
  face is brown, as published. The wood is roughened as on every kit.
Commands (from the project folder), after a change to the CAD or the guide:
    .venv.nosync/bin/python "LSM Build Instructions/assemble.py"      # lsm.glb, after a new STEP (convert it first, see assemble.py)
    .venv.nosync/bin/python "LSM Build Instructions/make_atlas.py"    # colour-atlas-lsm.json
    .venv.nosync/bin/python "LSM Build Instructions/guide.py"         # steps.json, parts.json, model.glb
    /usr/bin/python3 tools/serve.py "LSM Build Instructions" 8805     # then http://localhost:8805/player.html

THE BUILD (39 numbered steps; the published guide's 38 and its order, with the house rules applied)
- Steps 1 - 8, the breadboard: backing peeled off; onto D1; the Nano Board in rows c and g, columns 2 - 16, USB socket at column 16
  (pin D12 in c16, as Part 1 of the published guide has it); the 12 kOhm resistor's legs bent, into h3 and h16; the capacitor into
  j2 and j3, grey stripe in j3; the 330 Ohm resistor's legs bent, into a11 and a19.
- Steps 9 - 16, the LED matrix's wires: the three-wire ribbon's ends pulled apart; the white, grey and purple pins into i2, i3 and
  b19, one per step; a note card naming the matrix's three pins; the LED matrix held over the breadboard and the white socket onto
  V+, the purple onto IN, the grey onto V-, one per step.
- Steps 17 - 23, the button and the USB cable: the button's nut off; the button through D2 from the brown side; the nut back on;
  the red lead into j5 and the black into j16, one per step (the published guide does both at once; one wire per step is the
  house rule); the USB cable's Mini-B plug into the Nano, its cable out to the A end on the table; D2 stood on D1.
- Steps 24 - 27, the housing: D4 (the USB cable in the notch at its foot); the LED matrix lifted over D4 and laid outside, its
  wires pressed into the slit in D4's top edge; with the box turned over, D3 hooked into D4 and swung shut (one step), then D5.
- Steps 28 - 39, inside and on top: the two D9; the LED matrix held over the box; D10 hooked under it; the matrix and D10 lowered
  in; D6; two D11 posts, then the other two; a check underneath that each D11's tab is through D1 (the published guide leaves the
  posts 7 mm short and pushes them home in this step); D7; D8; one stem; the other 63.

QUESTIONS FOR LEE
1. The LED stem's CAD (you mentioned the acrylic stem is missing): until it comes, each stem is a plain square rod of Cadasio's size.
2. The USB cable: the LSM's right-angle Mini-B plug (as the published guide shows it) rather than the MRA's straight one, because a
   straight plug would run into the push button. Is the kit's cable right-angle?
3. The LED matrix's pin names: the published guide's badges say V+, "V-In" and V-; the steps say V+, IN and V-. What is printed on
   the board (5V / DIN / GND?)?
4. The button's leads: red into j5 and black into j16, as the published guide's result shows them (its Step 19 labels have them the
   other way round). Two steps, one wire each.
5. D2's outer face brown, as published (the other panels plain wood on both faces): is D2 a different material, or should it match?
6. Cards: the published guide has un-numbered section cards (Capacitor, LED Matrix Diagram, Mini USB Cable, LED Stems "64x"). The
   in-house player has no picture cards yet: the capacitor's polarity is a caution on its step, the matrix's pins a numbered note
   card (Step 13), the cable and stems need none ("63x" on the last step).
7. Part guides: the published LSM has Parts 1 - 4 (and 1+2, 3+4). The draft is the Full Build only; Parts can be cut from it
   (g.chapter()) when you want them, and a deconstruction guide after that.
8. The Nano Board's place: Cadasio moves its Nano 2.3 mm sideways in the steps; here it is in rows c and g (from the published Part
   1's "Pin D12 - c16" label and the circuit), which puts every wire on the right Nano pin. Worth a check against the real kit.
