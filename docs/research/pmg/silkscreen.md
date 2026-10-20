# PMG printing: push buttons, 4-digit display, dot matrix (19 Oct 2026)

Lee's first round on the PMG draft asked for three things in the model:

1. the dot matrix's dots round, in proper 8 x 8 grids (screenshot `lee_images_2026-10-19/1_dot_matrix_dots_in_guide.webp`: rough
   polygons);
2. the push buttons' silkscreen (photo 2, TechBox's Cadasio card: VCC, OUT, GND by the header);
3. the 4-digit display's silkscreen, front and back (photos 3 - 5), and the dot matrix's (photos 6, 7).

All three are drawn by the player from decals (`PMG Build Instructions/silkscreen.py` -> `decals.json`, placed in the model by
`tools/build_model.py`), as the MRA's and RCC's boards are. The I/O module's print (NAUO78) is unchanged, byte for byte.

## How it is placed

Every decal is laid out in its part's own CAD frame and placed by that part's node in `pmg-guide.glb` (the kit's source;
`silkscreen.py` reads only its node matrices and checks each mesh's own box against the one measured here, so a changed CAD stops
it rather than misplacing the print). Decals ride with their parts, so they follow every pose.

Text is Arial in the player; the boards' silkscreen font is narrower, so each label has its photo's capital height and is squeezed
to its photo's length (`width`, which only ever narrows).

## 1. The LED blocks' dots (NAUO81, four "1088AS" meshes)

- Measured on the CAD: the block's face is 31.8 x 31.8 mm (own frame x 0 .. 31.8, z -31.8 .. 0, face at y 0, the black mask
  y -0.1 .. 0). 56 of the 64 dots are separate discs, 3.00 mm across (radius 1.500 on all), 0.1 mm thick, flush with the face;
  their centres fit x = 1.9875 + 3.98 i, z = -(1.9875 + 3.98 j) to 1e-7 mm. The eighth column (x 1.9875) is welded into the
  body in this export (no solid of its own): it follows the same grid.
- The old model coloured the dots white with 64 boxes in `materials.json`; after simplification (0.03 mm, 8000 triangles) the
  triangles inside each box made a rough polygon: Lee's screenshot.
- Now: `materials.json` `^1088AS$` keeps only its face box (the whole face black, dots and all) and each block carries a decal
  0.02 mm above its face: a black fill the size of the face and 64 white circles r 1.5 at the CAD's centres (24 px/mm). The
  decal is opaque over the whole face, so the face's own crease lines (round each disc) are covered.

## 2. The push buttons (NAUO76 black, NAUO83 yellow, NAUO84 white, NAUO85 blue)

- One CAD part placed four ways (each tilted about 7 degrees in the case). Board own frame: x -6.5 .. 6.5 (across), z -11 .. 11
  (along; the header at +z), face (cap side) y 0, board 1.2 thick. Header pins at x -2.5 (VCC, the highest assembly z),
  0 (OUT), +2.5 (GND); their black spacers z 7.5 .. 10; the switch body ends at z 4.0 (legs 4.7); the board's edge z 11.
  (The CAD's pitch is 2.5, the real 2.54.)
- Photo 2 (right half), 38 px/mm across the pins. Seen cap side up, header at the bottom: VCC left, GND right (matches the CAD's
  pin order). OUT: capitals 1.05 - 1.1 mm, 3.4 mm long, 0.3 mm above the spacer, over the middle pin. VCC and GND read up the
  board (tops to the left), capitals 1.3 mm, about 3.3 mm long, from about 1 mm above the spacer to its lower end, between the
  board's edge and the spacer. A thin outline round the header's footprint.
- Placed: OUT centred at (0, 6.65); VCC at (-5.15, 8.3) and GND at (5.15, 8.3), rot -90; outline 0.15 mm outside the spacers.
- Not matched: the real board is shorter than the CAD's (about 18 against 22 mm: the photo has 2.4 mm between the switch and the
  header, the CAD 3.5 mm), so the print keeps its distances from the header, as on the real board.

## 3. The TM1637 4-digit display (NAUO79)

- CAD own frame: board x -21 .. 21, y -12 .. 12, back z 0, front z 1.3; digit block on the front x -14 .. 16, y -7 .. 7; chip on
  the back x -16.7 .. -8.7, y -6.5 .. 6.5; corner holes r 1.1 at (+-19, +-10); pins at x 18.8: CLK y 3.5, DIO 1.1, VCC -1.3,
  GND -3.7 (the caps' pin tips in cad-geometry.json).
- Photos 4 (front) and 5 (back) calibrated on the four corner holes: 16.15 / 16.1 px/mm (front), 16.32 / 16.3 (back), the holes
  38 x 20 mm apart as in the CAD. Front seen with the pins on the right (right = +x, down = -y); back with the pins on the left
  (right = -x, down = -y): CLK at the top on both photo and CAD.
- Front: U1 (capitals 1.18) centred at (1.42, 8.56), above the block; J1 (1.06) at (18.55, 6.45) above the header; the outline
  round the header's footprint (x 17.45 .. 20.15, y -5.05 .. 4.85); "4-Digit Display  V1.2" (regular weight, capitals 1.55,
  17.1 mm long) centred at (2.2, -9.67).
- Back: HW-069 (1.2) from x 16.59 at y 10.25; CLK DIO VCC GND (1.24) from 1.67 mm beside each pin, on its line; C1, C2 (1.13)
  with their outlines and parts, lifted 0.3 mm (the CAD's chip is 0.3 mm longer than the real one and would cover C2's outline);
  R2, C4, R1, C3 (1.25, reading up the board) with their outlines and parts; U2 (1.07) under the chip and its pin-1 circle; the
  display's twelve solder joints (not in the CAD: 2.54 pitch, rows 10.16 apart, about the block's middle; pin 1 square) with "12"
  and "1". The parts between the two rows of joints are placed from the joints: on the real board they sit 0.28 mm off the
  corner holes' middle (photo 5).
- Added for the look of the photos, not silkscreen: the plated rims of the corner holes (r 1.1 .. 1.6, both sides) and of the
  header's pins (back, GND square), the solder joints, and the small parts drawn flat (resistors black with "103", capacitors
  tan, tinned ends). Left out: the copper traces under the mask, the marking on the TM1637 chip, the vias.

## 4. The dot matrix's rear (NAUO81, the PCB)

- CAD own frame: x -16.1875 .. 113.3125 (the input header at the low end), y -16 .. 16, back face z 1.5 (the LED blocks in front,
  z < 0). Four modules 32.375 long, centres x 32.375 k; on each, 1.0 mm holes: LED pins x -9.188 + 2.54 i, y +-12; input pins
  x -14.2875, y -5.76 -3.22 -0.68 1.86 4.40 (VCC GND DIN CS CLK, from the caps); output pins x 14.6875, y -5.56 .. 4.60.
- Photo 7: 8.2 px/mm, input header on the right, VCC at the top: right = -x, down = +y (the pin order fixes it).
- Placed per module: VCC GND DIN CS CLK right-aligned 1.5 mm left of the input pins (picture), VCC GND DOUT CS CLK left-aligned
  1.5 mm right of the output pins, capitals 1.06, each on its pin's line; OUT (1.52, centred 8.7 mm from the module's middle
  towards its output end) with its arrow, IN (centred -7.55) with its arrow, on y 14.42; MH (1.52) on the input module at
  (-0.44, -14.5); plated rims round all 104 holes (pin 1 of each LED block square, as photographed); the links between one
  module's output pins and the next one's input pins.
- Not matched: on the photo the header pins sit 0.6 mm lower relative to the LED rows than the CAD's holes; labels follow the
  CAD's holes. The MH is in a serif face on the board (the player has only Arial).
- Not added: the print on the board's front (photo 6: "IN" and "OUT" arrows along the edge under the LED blocks): in the CAD the
  blocks cover the board's front almost to its edges (0.1 mm), 1.2 mm above it, so it could not be seen.

## Checks

(The Mac went down before this section was written; checked afterwards, in the player, 19 Oct 2026.) Seen in the player and in the
round's review (docs/research/pmg/round1/): the push buttons' VCC / OUT / GND read upright beside the header (the Step 3 card's
close-up, round1/step3_card_live.jpg); the dot matrix's 4 x 64 round dots on a black face (round1/matrix_dots.png); its back's VCC GND
DIN CS CLK, DOUT, IN / OUT and MH where photo 7 has them (round1/matrix_rear.png; legible from the wiring camera, Steps 21 - 25); the
display's U1, J1 and "4-Digit Display V1.2" on the front (parts/4-Digit-Display.png) and its back's print (Steps 21 - 23). The I/O
module's print is unchanged.
