# Lee's second notes on the LSM deconstruction (22 Oct 2026), word for word

On the deconstruction as published to the test site after the first notes of the day (commit f9e9da1; laser-stem-matrix-deconstruction
r3, 25 steps). Step numbers as the player's step list showed them then.

> On the deconstruction guide only:
> Step 6 - the eyeball on the left D11 is too high, it should be at the bottom where the actual latch element is
> Step 7 - Same as Step 6
> Step 10 - D10 should be removed at this point and the wires disconnected from the LED Matrix in a group, but left attached to the breadboard, then the breadboard wires moved. Remember, D10 must slide off of the LED Matrix
> Step 15 - the bounding box is still too small in the breakout image. It needs to include both tabs of the latch
> Step 16 - Same as 15.
> Step 20 - The nut reinstallation can start at the mid point of the current step. The movement through empty space with the spread out view is not needed, start the nut just off the end of the push button's wires, then animate it back on.

## What was done (22 Oct 2026)

Step numbers in brackets are those of r4, the release these notes were done in: it had 24 steps (r3's Steps 10 - 14 became 10 - 13, so
r3's 15 is 14, 16 is 15 and 20 is 19). Since Lee's answer below added a step after 11, add one to r4's numbers from 12 on. The study behind the matrix steps: `decon/round3/` (fullbuild_d10_wires.md, takeapart_api.md, current_matrix_section.md).

| Note | Done |
|---|---|
| Step 6 [6], Step 7 [7]: the eye on the left D11 too high | Each eye now points at the foot of its post (D11_D, D11_A, the left post from each step's camera), on its outer face 1 mm above D1, at the middle of the tab that goes down through D1 and catches under it (`latch_foot()`). The published eyes were 17.6 and 21.1 mm up the post. A raycast confirms that the spot is the first thing the camera sees there. |
| Step 10 [10 - 13]: D10 off here, the wires off the matrix in a group but left in the breadboard, then the wires; D10 must slide off | The matrix is no longer set down beside the box (that fade is gone). It stays held over the box, where Step 9 lifts it. **[10]** D10 slides 40 mm along the matrix toward D2, away from its pins, until its hooks are free, then drops 22 mm. This is the Full Build's Step 31 (D10 hooked on there) reversed, with the wires exactly as they were then: dead straight through D10's notch for the whole slide (tightest, the gray wire, 0.04 mm off the notch wall, as in the Full Build). There is an arrow for each stage, in turn, and the published eye is on D10's hook. **[11]** The matrix is pulled 30 mm back along its pins, off the three connectors (as published, 30.5 mm), and is gone. The connectors stay where they came off and the wires stay in the breadboard. **[12]** Both D9 come out. **[13]** The three wires come out of i2, i3 and b19 together, each whole. The D9s go before the wires because the wires run under the D9 nearer D4 (guide.py; the rulebook). I read "then the breadboard wires moved" as the wires coming out of the breadboard; see the question below. No fades are left in the guide. |
| Step 15 [14], Step 16 [15]: the box too small, both tabs of the latch | Each close-up is now centred on the latch: across, between its two tabs (x 631.0 - 645.5), and in height, on D1's middle (D3's published ring sat on D1's lower face). The square box has a half-width of 8.9 mm, so it holds both tabs with about 1.75 mm to spare on each side (it was 6.0 mm, on one tab). |
| Step 20 [19]: start the nut just off the wires' end; no move through empty space or spread-out view | The nut is laid 5 mm off the pins' ends as the step opens (D2 has just been put away, so the view starts afresh; `rest_at()`, which now works in a take-apart). From there it goes on in one smooth move, as [17] took it off: eight quarter turns, the screwing way. The camera is closer: radius 58, was 105. The arrow is [17]'s size, 16.5 mm above the nut, clear of the wires it slides over. |

Found while checking (by an independent review, each finding challenged by a skeptic; four refuted), and fixed (step numbers of r4):

- **Step 11.** The arrow is over the matrix, toward the camera, where the matrix cannot hide it; its tail had been under the corner LEDs. The caption names the pins (V+, IN, V-), as r3's did. The caution was reworded ("pull the LED Matrix's pins out of them"). The eye is moved to the left, clear of the arrow and of the box's corner.
- **Step 10.** The slide arrow moved out from under D10's corner, which had clipped it.
- **Step 12.** The two D9 arrows are one size (like parts). They start just over D3's top edge, near the D9s' D3 ends, where the wires and connectors left in the air are not in front of them. The published tails were 8.6 mm down inside the D9s.
- **Step 13.** It is framed higher, so the wires' rise stays in view, under the caution box.
- **Step 6.** Its two arrows' tails sit 2.7 mm off the posts' outer faces, as Step 7's do: the published tails were half inside the posts.

Tools:
- `tools/motioncheck.py` now also checks the parts a take-apart step takes off, and their wires, along their ways until they fade. It had not seen D10 slide through the wires in r2; run on r2 now, it reports exactly that: the three wires about 2 mm into D10, at 0.20 of the motion. A part taken off in turn is not tested after its own way has ended.
- `tools/stepgen.py`: `rest_at()` after `take_apart()` moves a part lying aside between two steps, and the next view starts afresh (the nut).

Checks:
- The run-through: 51 views, 0 problems.
- wirecheck: 0 of 51.
- motioncheck, with the parts taken off and their wires included: only the Full Build's own Step 32 touch, played backwards in Step 9c.
- Every arrow is on screen, and no close-up covers an arrow, at 1280 x 800, 1024 x 768, 1000 x 680, 768 x 560 and 768 x 1024.
- No arrow is under the instruction boxes at 1280 x 800. At 1024 x 768 only Step 1's is (README question 29). At 768 x 560, Step 11's is under them too.
- Changed cameras: only the steps named and the new ones (11 and 13 framed on the matrix held over the box and on the wires; 19 closer).

Asked of Lee: once the matrix is off (Steps 11c - 13), the three connectors stayed where they came off, in the air over the box,
until the wires came out. Leave them so, or first lay the wires over the side of the box, still in the breadboard? Lee's answer, the
same day:

> Add a step that lays the three wires over the side of the box, still in the breadboard, before the D9s come out.

Done: a new **Step 12**, so the guide now has 25 steps (the D9s are Step 13, the wires out Step 14, D3 Step 15, ... the Nano Board
Step 25). The wires, still in the breadboard, are laid out of the box over its open end (where D4 was) and along the table, the
three connectors side by side on it, wire ends toward the box (`wire_shapes.py`: `draped()`, `draped_socket()`):

- Each wire keeps the Full Build's own run in the box (under the D9 nearer D4, which comes out next), so that run stays put as the
  wires move.
- Each turns out over D1's edge 19 - 21 mm above it, beside D2's end, and comes down onto the table. The USB cable leaves the box 20 mm
  nearer D3 and runs along the table parallel to them; the connectors lie 35 - 39 mm from it.
- Each is at least as long as it was held (yellow 261 mm, as held; gray and purple 4 and 7 mm longer, so that the three connectors lie
  side by side). A first try, about 90 mm shorter, made two wires run into each other as they changed
  shape.
- They turn out in the order in which their held shapes rise beside D2 (gray, purple, yellow), so none passes another as they move.
  Gray and purple cross over yellow's run in the box, 2.5 mm over it.

The move: the connectors go from where they came off down to the table along their leads, an eye on one, no arrow (a plug moved on its
lead). The camera is new, from D2's side, so the wires run across the picture to their connectors.

Knock-on changes:
- **Step 13 (the D9s):** the arrows stay near the D9s' D3 ends, from just over D3's top edge. At their published place along the D9s,
  the nearer D9's arrow starts in that D9's notch, right over the USB plug, as if it lifted the plug (an independent review of this step).
  The camera is r4's, unchanged. In a square or upright window the far ends of the laid wires reach the right edge.
- **Step 14 (the wires out):** it keeps the published direction, framed wider toward the open end, so the wires' far ends are in view
  as they come out. The frame was searched so that everything stays inside the picture at every shape of window.
- **Step 12's camera** looks from the open end's corner by D2. From D2's side, the wires turning out over D1's edge were hidden behind
  D2. It was framed by the same search: target [559, 915, 1241], radius 92.

Checks:
- The lay-out, the D9s past the laid wires, and the wires coming out: no contact at 39 moments each.
- The whole guide: motioncheck shows only the Full Build's own Step 32 touch in 9c; wirecheck 0 of 53; the run-through 53 views, 0
  problems.
- Arrows: all on screen, and none under a close-up, at 1280 x 800, 1024 x 768, 1000 x 680, 768 x 560 and 768 x 1024. None under the
  instruction boxes at 1280 x 800, and at 1024 x 768 only Step 1's (README question 29); in smaller windows the same few as before
  (Steps 1, 6, 7, 9, 11, 25), none of the new steps'.
- At rest, the drape against every part, the table and the USB cable: `decon/round3/drape_check.py` (its output beside it).

## Lee's third notes (22 Oct 2026), on release 5

With two pictures: Step 11 seen from under the matrix, and Step 12c with a green arrow on the laid wires (the first copy of that
picture came without its arrow; Lee sent it again). Kept on this Mac in `decon/round3/lee_pictures/`.

> Use this first image's view for Step 11 and adjust the arrow location as needed.
>
> For Step 12c - adjust the wire length to where they stop near where the green arrow is in the second image. Should be simple, just shortening them so they don't look as long next to the USB cable.

| Note | Done |
|---|---|
| Step 11: this view | **The camera.** Solved from the picture by the four corners of the board's underside: least squares with the player's own field of view and the canvas height fitted, every corner within about 1 px. The camera sits out past the open D4 end, 30 mm above the table, looking up 27° under the matrix: view_dir [-0.893, -0.450, -0.021], frame ([643.5, 942.9, 1196.6], 47.5). (The player's silhouette solver could not be used here: the picture crops the box, and it searches from above unless told otherwise.) **The arrow.** It is under the board now, toward the camera, along the board's middle. With the board between it and the camera, the matrix itself would have hidden it. It stays the published size. The eye's spot on the purple connector is the part of it that this camera sees. |
| Step 12c: shorter, stopping at the arrow | The arrow, projected with Step 12c's camera, points at the yellow wire 13 mm past where the wires reach the table. **The connectors.** They now lie there: gray's wire end at x 562, purple's 4 mm further on, yellow's 8 mm. The table run was about 96 mm. **The stagger.** Lying side by side, the shorter wires ran into each other as they moved: each wire's run over the box, longer than its new drape, is drawn in to its connector, and gray's and purple's runs over the box are 1.7 mm apart. Staggered in the order the wires run over the box, they stay apart all the way (no contact at 39 moments). **The matching.** The drape is shorter than the held shape, so it no longer matches by the connector's end: every bit keeps its distance from its pin, and the run in the box stays put. |

Checks:
- motioncheck: the lay-out, the D9s and the wires out, no contact at 39 moments each. The whole guide: only the Full Build's own Step 32 touch in 9c.
- wirecheck: 0 of 53.
- The drape at rest (`decon/round3/drape_check.py`): on the table, clear of it; the connectors 18 - 25 mm from the USB cable.
- The run-through: 53 views, 0 problems.
- Arrows: all clear at 1280 x 800, and at 1024 x 768 all but Step 1's. Step 11's is 2 px under the caution box at 768 x 560 (was 43).
- Changed views: Steps 11 (camera, arrow, eye) and 12c - 14 (the connectors' places); no other camera.

Then, on release 6 (Lee): "Yes, lower Step 11's view a little so the board and connectors clear the caution box in smaller windows,
keeping the same angle." Done: the same direction, aimed 10 mm higher and drawn back from radius 47.5 to 57 (frame ([643.5, 952.9,
1196.6], 57.0)). The board and the connectors now clear the caution box (the instruction box above it runs to three lines) by 42 px
at 1024 x 768, more at 1280 x 800, and about 10 px at 1000 x 680. The D9 stays in view at the bottom left, as in Lee's picture:
raising the aim alone, by 16 mm, pushed it out of the frame. A 768 x 560 window is too small to clear without changing the framing
(README question 29). Only Step 11's camera changed. The run-through: 53 views, 0 problems.
