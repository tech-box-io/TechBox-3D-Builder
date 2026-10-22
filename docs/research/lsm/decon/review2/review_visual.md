# LSM deconstruction, second draft: review of the visual cues (21 Oct 2026)

Read from the pictures in `LSM Build Instructions/pages/steps-deconstruction/` (000 - 049; 2000 x 1163, drawn by pages.js),
`steps-deconstruction.json`, `deconstruction.py`, `wire_shapes.py` and the published replay in `docs/research/lsm/decon/published/`.
Nothing was run. Step names are the player's. Close-up placement and leaders in the pictures are pages.js's own and are not judged here.
Most severe first.

## 1. Step 14: the arrow is at the wrong end of the wires (HIGH)

- **What is wrong.** The step pulls the three black sockets off the matrix's header. The arrow lies beside the *other* three black
  housings (the male pins lying loose on the table), 400+ px from the header. The caution says "Hold the three black connectors while
  you pull them off the pins", and the only black connectors the arrow points at are the loose pins. The real sockets show as a thin
  black strip against the black board, under the matrix's edge, marked only by the eye's small ring.
- **Evidence.** `deconstruction.py:233` (`at=to_laid(PUB['Step 15'] ... tail)`). In steps-deconstruction.json Step 14 the arrow runs
  from (567.92, 847.88, 1204.52) to z 1172.92. The sockets J_*_F are at z 1248.5 (y 867.5, x 573.4 - 578.5) and the pins J_*_M at
  z 1183.0 (y 857.1). So the tail is 44 mm from the sockets and 21.5 mm short of the pins, and the arrow runs on past the pins. It also
  sits 8 mm below the table (856.2). In 027.png the arrow is under the pins at the far right and the header is at the far left. The
  published arrow (published_steps.txt:288) also sat 44 mm along the wires, but there the wires hung loose; ours end in pins right there.
  The arrow is also the published "very heavy" one: a 3.5 mm shaft at radius 57.5, the fattest on screen. The study (section 5,
  item 9, [040]) lists it as a published glitch, not to be copied.
- **Fix.** Put the tail just outside the matrix's edge in front of the header, as this camera sees it: `arrow_style={SOCKETS[0]:
  dict(dims=(31.6, 2.0), at=[585.0, 867.5, 1250.0])}`. That gives −Z along the edge, toward the middle of the near edge on screen.

## 2. Steps 14 / 14c (and 13 / 13c): framed on empty space under the matrix (MEDIUM)

- **What is wrong.** In 027.png and 028.png the matrix fills the top third and the lower two thirds are empty. In 14c the bare matrix
  sits along the top edge. Steps 13 and 13c (025.png, 026.png) are the same to a lesser degree.
- **Evidence.** Step 14's camera target is (543.4, 832.2, 1233.0). That is 36.5 mm below the laid matrix's middle (547.9, 868.7,
  1231.8) and 24 mm below the table. This copies the published offset (published target y 915.6 against its hovering matrix at about
  952), where the wires hung below the matrix. Ours lie at table level. Step 13's target is at y 826.4, 42 mm below the matrix.
- **Fix.** Raise both targets to the matrix: `frame=([548, 864, 1232], 57.5)` for Step 14, or centre it on the header with item 1.
  For Step 13, about y 860.

## 3. Step 18: a heavy arrow beside the wires, far from the nut (MEDIUM)

- **What is wrong.** In 035.png the thickest arrow in the guide runs from the middle of the wires, past the pins' ends, to the lower
  left. The nut, with its eye, is at the other end of the wires. The arrow reads as "pull the wires", not as "unscrew the nut and slide
  it off".
- **Evidence.** `deconstruction.py:257`. The arrow runs from (651.98, 878.88, 1265.59) to z 1209.29, 5.0 mm wide, at radius 67.1.
  The nut is at about (633.4, 875.8, 1308.5): its eye anchor plus D2's 57.1 mm. So the tail is 47 mm from the nut, and the head is
  25 mm past the pins (z 1234.8). The study (section 5, item 9, [048]) names this published arrow as "very heavy".
- **Fix.** Put the tail at the nut, beside the button's axis and clear of the wires, for example `at=[646, 880, 1302]` (−Z), with
  dims about (45, 3.0).

## 4. Steps 10c, 11, 11c, 12, 12c: the laid matrix lies on top of the USB cable (MEDIUM)

- **What is wrong.** In 020.png, 021.png and 022.png the cable vanishes under the matrix and comes out beside D10, with its A plug
  right against D10's end. Seen from the far side (023.png, 024.png), the black cable runs alongside the three jumper wires into the
  matrix's underside, and its A plug sticks out past the matrix's far corner. It looks like a fourth lead plugged into the matrix.
- **Evidence.** `wire_shapes.py:88-92` (LAID_POSE: "D10's end clears the USB cable's A end by 2.8 mm") and `:147`, `:206` ("over the
  USB cable (laid on the table under the matrix's middle)"). The published matrix floats 32.7 mm higher over the same spot.
- **Fix.** Lay the matrix clear of the cable, for example on the other side of the cable or past its A end, and redraw LAID and LOOSE
  in wire_shapes.py. Or put the published position to Lee as it is.

## 5. Step 16: the arrow is mostly behind D2, and the close-up's ring lands on the nut (MEDIUM)

- **What is wrong.** In 031.png the camera looks at D2's inner face. The arrow starts behind the panel and comes out from behind its
  right half, foreshortened, pointing away from the viewer. The close-up's dashed ring falls on the button's nut and the red lead's end,
  not on any latch you can see: the latch is on the far side of D2.
- **Evidence.** `deconstruction.py:243-248`, using `cam('Step 17')`, dir (−0.46, 0.77, −0.43). The arrow tail (637.93, 855.51, 1256.74)
  is at table level on D2's outer side (the nut, on the inside, is at z 1251.4 seated). The inset target (640.81, 860.56, 1255.23) is
  also outside D2.
- **Fix.** Lift the arrow over D2's top edge (`arrow_style={D2: dict(..., shift=[0, 45, 0])}` or a tail at y about 900). Then either
  move the close-up's ring onto D2's visible lower edge, or pick a camera from the D3 or D5 side, so the slide reads sideways and D2's
  foot shows.

## 6. Step 15: the close-up is too tight to read (MEDIUM)

- **What is wrong.** In 029.png the close-up shows a plain tan face, a slanting edge and a small latch. There is nothing to tell D1
  from D3, and no engraved code. Step 16's close-up has the same radius and reads a little better only because the button's edge is
  in one corner.
- **Evidence.** `deconstruction.py:240`: `radius=10.0`. Steps 4 and 5 use 26. The published close-up was the whole D3 face, 24.84 %
  wide (published_steps.txt:315).
- **Fix.** Use a radius of about 30, so that D3's lower half with "D3" and D1's edge are in the picture. Consider the same for Step 16.

## 7. Step 20 / 20c: the base sits high and small; the A plug touches the edge (LOW)

- **What is wrong.** In 039.png the board and the plug, which are the subject, sit in the upper middle (their centre at y 390 of 1163)
  and the A plug reaches the left edge (x 25). In 040.png the base fills the top-left quarter and about 60 % of the frame is empty.
- **Evidence.** The camera target (633.5, 832.0, 1239.2) is 24 mm below the table and about 34 mm toward D2 from the board's middle
  (the published target, used unchanged).
- **Fix.** Use `frame=([630, 866, 1215], 95)` or similar.

## 8. Step 1: the eye covers the arrowhead (LOW)

- **What is wrong.** In 001.png the eye icon overlaps the arrowhead's right wing, and its pale backing hides part of it. Its leader
  runs down the arrow's shaft to a ring at the arrow's tail, so the two cues sit on top of each other.
- **Evidence.** The eye anchor is on STEM_45 at (643.6, 966.3, 1218.3); the arrow tail is at (637.1, 944.4, 1202.8).
  `deconstruction.py:166`.
- **Fix.** `eye=[dict(eye('Step 1'), side='right')]` (or 'near-right' with a larger reach), or anchor the eye on a stem in the front row.

## 9. Start: the USB cable is missing, then appears at Step 1 (LOW, for Lee)

- **What is wrong.** Start (000.png) has no cable; Step 1 (001.png) has it, so it pops in. The published Start shows the cable
  (published_steps.txt, Start "+ usb cable"), and Step 1's caution is about that cable.
- **Evidence.** Start's `visible` has no USB_A or USB_B and its `wires` has no 'usb cable'. This is the Full Build's title page
  (`take_apart()`, `deconstruction.py:82`).
- **Fix.** Ask Lee whether the deconstruction may have its own start view with the cable shown. CLAUDE.md gives it the Full Build's.

## 10. Steps 6 and 7: the published 350 mm cameras leave the box small (LOW)

- **What is wrong.** In 011.png and 013.png the box is about 28 % of the frame's width, so the posts, their tabs and the arrows are
  small. Step 6's frame is mostly taken up by the cable.
- **Evidence.** Radius 124.2, against 106.4 (300 mm) in Steps 4, 5 and 8.
- **Fix.** Use radius 106.4 where the cable still fits, or put it to Lee.

## 11. Several steps: the USB cable's A end is cut off (LOW)

- **What is wrong.** At the PDF's 1.72 shape, the A plug runs off the bottom right in Steps 11 and 11c (021.png, 022.png), 15 and 15c
  (029.png, 030.png), and 16, 16c, 17 and 17c (031.png - 034.png).
- **Fix.** Check this in the player at 1280, 1000 and 768 px. For the PDF, use a slightly larger radius or move the target toward the
  plug.

## 12. Step 17c (and the views of D2 on its own): the unplugged pins hang in the air (LOW)

- **What is wrong.** In 034.png both pins stop in mid-air over the breadboard's far end, on ruler-straight leads.
- **Evidence.** In Step 17c the pin centres are at y about 881.6 and z 1234.8, about 7.7 mm above where they sat in their holes
  (873.9). That is the lead's route before the Full Build's Step 24.
- **Fix.** Optional: let the pins drop onto the board or the table.

## 13. PDF only: three close-up captions run past their frames (LOW)

- **What is wrong.**
  - Step 3, "D7 in the notch of each D11 post" (005.png): the text spans x 1255 - 1995, the frame 1295 - 1950.
  - Step 15, "The latch on D1 at the foot of D3" (029.png): the text runs past the frame.
  - Step 16, "The latch on D1 at the foot of D2" (031.png): the text spans x 8 - 745, the frame 50 - 705.
- **Evidence.** `player/js/pages.js:43-46` draws the caption with `fillText` at a fixed 24k px, without measuring or wrapping it.
- **Fix.** In pages.js, shrink the text to fit with `measureText`, or wrap it. Or shorten these captions.
