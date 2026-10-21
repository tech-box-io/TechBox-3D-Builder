# LSM deconstruction draft: visual-cue review (21 Oct 2026)

Angle: the visual cues, read from every picture: Start, each Step N and Step Nc, and the Completed View. The pictures are
`LSM Build Instructions/pages/steps-deconstruction/NNN.png`, drawn by pages.js. Each picture was checked against the views in
`steps-deconstruction.json` (arrows, eyes, insets, cameras, offsets) and against the part boxes in `assembly-report.json`. No
script, generator or browser was run. Wording points are left to `review_wording.md`; where a fix here depends on one there, it
says so. Findings are listed with the most severe first.

## 1. Step 4: the close-up's placement, ring and leader (medium)

- **Wrong:** in the picture (007.png), the close-up covers D11_C's arrow (the post at the D4 / D2 corner): only the arrow's tip
  shows at the frame's left edge. The ring sits on D3's outer face, over its engraved code, where nothing can be seen. The leader
  then runs from the right-hand frame across D4, the front post and D6 to reach the ring.
- **Evidence:** the close-up's target is D11_B's tab at `[674.83, 857.0, 1166.2]`, under D1 at the D5 / D3 corner
  (deconstruction.py:122). The inset has no `side=`. pages.js always uses the corner farthest from the spot
  (player/js/pages.js:33-34) and ignores the step's arrows, eyes and `side`. In the player, the room per side is computed at
  player.js:516-519; at this camera, right (about 640 px of 2000) and left (about 620) are nearly equal. So the player would
  probably also put the close-up on the right, with the same leader across the box. That breaks Lee's rule of 20 Oct 2026: a
  close-up sits on the side of the part its leader goes to (docs/cadasio-patterns.md:134).
- **Fix:** in deconstruction.py:122, `inset=dict(..., side='left')`. In pages.js, place the close-up where the player does
  (read `#inset`'s rectangle and scale it to the picture). Failing that, skip any corner that covers an arrow, eye, label or
  leader and prefer the spot's side. The PDF page for Step 4 hides a cue until then.

## 2. Step 11: D3's arrow floats off the part and shows only the second motion (medium)

- **Wrong:** the arrow sits in empty space about 60 px past D3's free end (021.png), and it is small at this camera (radius
  118). It shows only the slide out of D4's slots. The swing comes first in the caption ("Swing D3 open, away from D1"), and
  nothing shows it.
- **Evidence:** the arrow's tail is `[681.58, 881.63, 1137.67]` and its head `[710.89, 881.63, 1125.83]`. D3's outer face is
  at z 1153.7, so the tail is 16 mm off the face: it is drawn where the free end will be after the 22-degree swing.
  deconstruction.py:141 has no `arrow_style`.
- **Fix:** do it the way the PMG's take-apart did on the same day for its swung plates (PMG deconstruction.py:135, 182, 226,
  228; CLAUDE.md:361): `arrow_style={D3: dict(stage=0, then=[dict(stage=1)])}`. Step N then shows the swing on D3's free end,
  and the slide's arrow appears in turn. `then=` is in the working tree's stepgen.py, not yet committed. That is the same
  commit dependency as `let_go`.

## 3. Step 13: D4's slide off the tabs has no cue, and the arrow reads as being on the push button (medium)

- **Wrong:** the arrow shows only the 65 mm lift. The 8 mm slide off D1's and D2's tabs is the release the caption names first,
  and it has no cue. The arrow also rises from D4's top edge straight over the push button's nut and D2 behind it (025.png), so
  it reads as belonging to the button.
- **Evidence:** D4's way is `[[-8, 0, 0], [-8, 65, 0]]` (deconstruction.py:148). The arrow runs from `[595.9, 909.0, 1204.2]`
  to `[595.9, 949.0, 1204.2]`, the middle of D4's top edge. The button (box z 1233.7 - 1258.6) is behind that point along this
  camera's line of sight.
- **Fix:** `arrow_style={D4: dict(stage=0, at=[595.9, 909.0, 1172.0], then=[dict(stage=1, at=[587.9, 909.0, 1172.0])])}`.
  This moves both arrows along D4's top edge toward the D3 end, clear of the button. It has the same `then=` dependency as
  Step 11.

## 4. Step 7: D10's arrow sits under D10 and points into the three wires (medium)

- **Wrong:** the arrow floats in the gap between D10 and the box's top edge, and its head lands on the white and purple wires
  (013.png). It can read as "pull the wires toward D2".
- **Evidence:** the tail `[599.3, 936.6, 1206.7]` is 3.1 mm below D10, whose box in this view is y 939.7 - 957.3. The arrow is
  28.1 mm long. The script puts the tail "3 mm below D10's lower edge" on purpose (`at_now(D10, [599.5, 880.0, 1207.0])`,
  deconstruction.py:133).
- **Fix:** put the tail on D10's own face, just above its lower edge and below its engraved code:
  `at=at_now(D10, [599.5, 886.0, 1207.0])`. Add `scale=0.7` (about 20 mm, above the 15 mm minimum) so that the head stops
  short of the wires.

## 5. Step 8: the matrix's arrow starts off the matrix and crosses its wires (low)

- **Wrong:** the arrow starts in the air beside the matrix's D4 edge and runs across the arch of the three wires (015.png).
- **Evidence:** the tail is `[600.33, 952.18, 1214.43]`. The matrix's box in this view is x 606.7 - 670.5, so the tail is 6.4 mm
  outside it, at the matrix's mid-height. The wires arch up from the sockets (x 607 - 614, z 1183 - 1191) on that same edge.
- **Fix:** `arrow_style={MATRIX: dict(shift=[0.0, 10.0, 0.0])}`. This raises the arrow clear of the wires, as Lee had the MRA's
  arrows raised clear of wires (CLAUDE.md:359). Or start it on the matrix's top face (y about 957). Check it in the player.

## 6. Steps 2, 3 and 4: on the exact diagonal camera, the arrows stack into the far D11 post (low)

- **Wrong:** D8's and D7's centre arrows run up into the far post's latch head (003.png, 005.png). In Step 4 (007.png, see also
  finding 1), the front post's arrow (D11_D) ends on the foot of the back post (D11_A), and the back post's own arrow sits
  directly above. The two read as one long arrow.
- **Evidence:** all three steps keep D7's camera, `dir [-0.579, 0.574, -0.579]` (deconstruction.py:116-121, `keep_camera=True`).
  The D4 / D3 and D5 / D2 corners (D11_D at x 601.6 z 1166.2, D11_A at x 674.8 z 1242.4) both lie on that diagonal. Each
  arrow is 36 - 40 mm long.
- **Fix:** for Step 4, `arrow_scale=0.6` (about 21 mm each), so the front arrow stops below the back post. Or give Step 4 a
  `view_dir` about 15 degrees off the diagonal. For Steps 2 and 3, move the tail off the camera's diagonal (screen-left here is
  +x / -z) with `arrow_style={D8: dict(at=[650.0, 934.4, 1180.0])}`, and the same for D7 at y 918.5. That puts each arrow about
  25 mm left of the far post.

## 7. Step 9: D9_A's arrow rises from exactly where the USB plug shows above D9_A (low)

- **Wrong:** the right-hand arrow starts on D9_A's top edge, right on top of the Mini-B plug's black body (017.png). Step 9c
  (018.png) shows the whole plug where the arrow's tail was, so the arrow can be taken for "pull the USB plug up".
- **Evidence:** D9_A's arrow tail is `[618.6, 902.7, 1204.3]`. USB_B is at x 619.3 - 643.3, z 1204.6 - 1224.5, just inside
  D9_A (x 617.1 - 620.1).
- **Fix:** `arrow_style={D9_A: dict(at=[618.6, 902.7, 1178.0])}` (deconstruction.py:137). This moves the arrow along D9_A
  toward the D3 end, clear of the plug.

## 8. Steps 21 and 23: the resistor arrows lie over the Nano Board (low)

- **Wrong:** in Step 23 (045.png), the 12 kΩ resistor's arrow starts at the resistor's top edge, but its whole shaft is drawn
  over the Nano's ATmega chip. In Step 21 (041.png), the 330 Ω resistor's arrow covers the Nano's USB socket. The next step,
  24, lifts the Nano, so the arrows can be read as the Nano's.
- **Evidence:** R12K's tail is `[647.5, 881.5, 1189.3]`. The Nano (x 628.3 - 646.3, top y 884.5) is behind the resistor from
  this camera (Full Build Step 5's, `dir [0.579, 0.574, -0.579]`). Both arrows are already at the 15 mm minimum, so shortening
  them does not help.
- **Fix:** carry the Full Build's hole labels: `a11` / `a19` on Step 21 and `h3` / `h16` on Step 23, as Full Build Steps 9 and
  5 had them. This is the same ruling as review_wording.md item 6 for Steps 16 and 20, and it is Lee's MRA ruling. Or add an
  eye on the resistor.

## 9. Steps 16 and 20: the eyes sit on the busy breadboard (low)

- **Wrong:** in Step 16 (031.png), both eyes are drawn with their white boxes over the Nano, the 330 Ω resistor and the point
  where the red, yellow and white wires cross. The upper box hides that crossing. The top-right third of the frame is empty. In
  Step 20 (039.png), the two eyes stand side by side above the model and read as a face.
- **Evidence:** the Step 16 eye anchors are `[652.0, 875.2, 1177.6]` and `[652.0, 875.2, 1205.7]`, placed by default. The
  script gives no `side=` (deconstruction.py:158, 189-191).
- **Fix:** if the Full Build's hole labels replace the eyes (review_wording.md item 6), this goes too. Otherwise give the eyes
  places in the white space, for example `eye=[dict(id=BTN_BLACK_PIN, side='up-right'), dict(id=BTN_RED_PIN, side='right')]`
  on Step 16, and `side='top'` / `'right'` on Step 20.

## 10. Steps 19 to 20c: the new camera crops D1 at the bottom and leaves the top third empty; Step 19's leader crosses the model (low)

- **Wrong:** in all four views (037 - 040.png), D1's near corner and edge run off the bottom of the frame, while the top 35 -
  45% of the frame is empty. In Step 19 (037.png), the close-up fills the bottom-left corner, over the breadboard, the Nano and
  the i2 / i3 pins. Its leader runs across the breadboard and the matrix to the connectors. In the player the left side has the
  most room (player.js:516-519: left about 650 px against right about 580 at 2000), so the leader probably crosses there too.
- **Evidence:** `WIRES_CAMERA` (deconstruction.py:180) targets `[688.0, 878.0, 1210.0]`, beyond D1's +x edge (682.7) toward the
  matrix. The inset (deconstruction.py:185-187) has no `side=`.
- **Fix:**
  - Move the target about 10 mm down the screen (screen-up here is about `[0.41, 0.82, -0.41]`), to about `[684, 870, 1214]`.
    Then check that the matrix's arrow still fits in Step 19.
  - Add `inset=dict(..., side='right')`, the connectors' side (cadasio-patterns.md:134), and check it at 1000 and 760 px.
  - The pages.js fix in finding 1 covers the PDF page.

## 11. Step 16c: the unplugged pins hover over the breadboard's row-30 end (low)

- **Wrong:** after unplugging, the red and black pins hang 9 mm over the end of the breadboard, their tips over c30 and a30
  (032.png). They read as being about to go into row 30.
- **Evidence:** in Step 16c, BTN_RED_PIN and BTN_BLACK_PIN are at y 880.7 - 882.5 and z 1228.8 - 1240.8. The breadboard's top
  is y 871.92 and it ends at z 1246.9. These are Full Build Step 21's laid-out poses, which `unplug()` reuses.
- **Fix:** acceptable as the Full Build's own pose. If Lee finds it confusing, give the pins a pose lifted clear of the board.
  That needs new lead shapes, so put it to Lee rather than change it unasked.

## 12. Step 17: the double-size nut arrow covers the nut's rim and the black lead (low)

- **Wrong:** the arrow's tail starts on the nut's lower rim, and its head lies on the black lead next to the button (033.png).
  The nut is the part coming off, and it is partly hidden by its own cue.
- **Evidence:** the tail is `[649.24, 882.63, 1307.4]`; the nut is at z 1307.5 - 1309.0. The arrow runs 2.5 mm off the button's
  side, between the camera and the button. `scale=2.0` (deconstruction.py:166).
- **Fix:** `scale=1.5`, and `shift=[3.0, 0.0, -2.0]` so the arrow starts just past the nut, beside the leads rather than over
  them.
