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

Today's step numbers in brackets: the guide has 24 steps now (r3's Steps 10 - 14 became 10 - 13, so r3's 15 is 14, 16 is 15 and 20 is
19). The study behind the matrix steps: `decon/round3/` (fullbuild_d10_wires.md, takeapart_api.md, current_matrix_section.md).

| Note | Done |
|---|---|
| Step 6 [6], Step 7 [7]: the eye on the left D11 too high | Each eye now points at the foot of its post (D11_D, D11_A, the left post from each step's camera), on its outer face 1 mm above D1, at the middle of the tab that goes down through D1 and catches under it (`latch_foot()`). The published eyes were 17.6 and 21.1 mm up the post. A raycast confirms that the spot is the first thing the camera sees there. |
| Step 10 [10 - 13]: D10 off here, the wires off the matrix in a group but left in the breadboard, then the wires; D10 must slide off | The matrix is no longer set down beside the box (that fade is gone). It stays held over the box, where Step 9 lifts it. **[10]** D10 slides 40 mm along the matrix toward D2, away from its pins, until its hooks are free, then drops 22 mm. This is the Full Build's Step 31 (D10 hooked on there) reversed, with the wires exactly as they were then: dead straight through D10's notch for the whole slide (tightest, the gray wire, 0.04 mm off the notch wall, as in the Full Build). There is an arrow for each stage, in turn, and the published eye is on D10's hook. **[11]** The matrix is pulled 30 mm back along its pins, off the three connectors (as published, 30.5 mm), and is gone. The connectors stay where they came off and the wires stay in the breadboard. **[12]** Both D9 come out. **[13]** The three wires come out of i2, i3 and b19 together, each whole. The D9s go before the wires because the wires run under the D9 nearer D4 (guide.py; the rulebook). I read "then the breadboard wires moved" as the wires coming out of the breadboard; see the question below. No fades are left in the guide. |
| Step 15 [14], Step 16 [15]: the box too small, both tabs of the latch | Each close-up is now centred on the latch: across, between its two tabs (x 631.0 - 645.5), and in height, on D1's middle (D3's published ring sat on D1's lower face). The square box has a half-width of 8.9 mm, so it holds both tabs with about 1.75 mm to spare on each side (it was 6.0 mm, on one tab). |
| Step 20 [19]: start the nut just off the wires' end; no move through empty space or spread-out view | The nut is laid 5 mm off the pins' ends as the step opens (D2 has just been put away, so the view starts afresh; `rest_at()`, which now works in a take-apart). From there it goes on in one smooth move, as Step 17 took it off: eight quarter turns, the screwing way. The camera is closer: radius 58, was 105. The arrow is Step 17's size, 16.5 mm above the nut, clear of the wires it slides over. |

Found while checking (by an independent review, each finding challenged by a skeptic; four refuted), and fixed:

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

Open, for Lee: once the matrix is off (Steps 11c - 13), the three connectors stay where they came off, in the air over the box, until the
wires come out. Leave them so, or first lay the wires over the side of the box, still in the breadboard? (That would be another
reading of "then the breadboard wires moved".)
