# Lee's notes on the LSM Full Build second draft (19 Oct 2026, evening), word for word

Step numbers are the second draft's (40 steps), as published to the test site that evening (r3). Pictures:
`lee_images_2026-10-19b/` (1: the Capacitor breakout picture for Step 6; 2: the camera wanted for Steps 11 and 12, a screenshot
of Step 12c; 3: Step 14, its overlapping leaders; 4: the camera wanted for Step 22; 5: the camera wanted for Step 31, with two
points Option-clicked on Step 28 in its corner).

> For Step 6, I have included the Capacitor Breakout image.
>
> Correct the lead lines here:
> Step 7 | Capacitor (CAP) | [652.5, 863.6, 1170.6]
> Step 7 | Capacitor (CAP) | [652.5, 863.6, 1173.1]
>
> In Step 10, you show the wires partially separated, but in Step 11, they are basically fully separated and somewhat confusing to look at. Also, update the camera view to be more like the second image attached for 11 & 12
>
> On Step 14, remove the BTE, Better than Expected, Only ONE Pin, and WS2812B-64 text. Adjust the remaining text location, leaving the white label where it is. The various lead lines on this step are overlapping and somewhat confusing - see the 3rd image.
>
> On Step 15, let's have the LED Matrix repositioned to be vertical so that the connection to the header and where the wires are located on the breadboard can be seen simultaneously. Add a lead line to the connection on the breadboard in addition to the eyeball and leadline already present on the LED Matrix pin. Do the same for Step 16 and 17.
>
> Step 18 - have the arrow start at the rear surface of the nut - currently it partially passes into the nut.
>
> For Step 22 - adjust the camera position to the fourth image attached.
>
> Step 23 - Is the USB A end the correct size? It looks a little oversized. Also, Step 23 is zoomed out a little far.
>
> Step 24 should use the same view as the slightly more zoomed in Step 23.
>
> Step 25 - Have D4 spawn in coming downward instead of in-toward D1. It also should use the same view as Step 23 after the slight zoom
>
> Step 26 - during the animation, the wires clip through the LED Matrix and toward the end of the animation, clip through D4 before settling in clear spaces.
>
> Step 27 - Zoom in slightly
>
> Step 28 - Step 28 | D1 (D1) | [682.6, 861.3, 1176.1]
> Step 28 | D2 (D2) | [685.9, 864.8, 1254.2]
>
> Also, in general for the LED Matrix, it looks like the LED immediately under the header is white, while the rest are all the same color. Can you adjust this outlier to match the rest?
>
> Step 30 - Looking at how the LED Matrix spins about the Z axis in this transition - I am wondering if we should already have it spun around in the correct orientation through the earlier movement on the earlier step? That way this transition is just a lift and move. Also, can you straighten the wires to where they are dead straight until at least beyond the point where D10 spawns in the next step?
>
> Slow the animation on Step 31 down and zoom in more - see the 5th image. Also, the arrow on this step is not visible at all - it's fully under the LED Matrix.
>
> Zoom in more for Step 32 as well - it's okay if the USB cable extends out of view. The focus here is on the LED Matrix and D10 moving into place. In the image breakout, can you have just a slight shade of the LED Matrix present - like 90% fade or something like that? And adjust the camera view in the breakout to better show how the wires fit in the slot of D10.
>
> Step 37 - Try to zoom in a little more, somewhere closer to Step 33's zoom
>
> Step 38 - Same as Step 37
>
> Step 39 - Same as 37
>
> Step 40 - Same as 37

Read as: "lead line" on Steps 15 - 17 is the blue leader of a label (a hole label on the breadboard, as on Steps 11 - 13); the two
points on Step 28 are lead-line points for D5 (as Lee gave Step 7's).

## What was done (19 Oct 2026, evening)

| Note | Done |
|---|---|
| Step 6, the Capacitor breakout picture | The close-up is Lee's picture (`capacitor-card.webp`, `inset=dict(image=...)`, a new player option); it sits clear of the step's labels. |
| Step 7, lead lines | At Lee's two points (`lines_at`). |
| Steps 10 - 12, wires and camera | The white and grey wires stay side by side as a ribbon from their pins, leaving away from the row of holes so that neither crosses the other's hole (the grey pin had come down through the white wire), rising steeply enough to leave the 12 kΩ resistor in view. While the grey pin is still held up (Step 11c, Step 12), its wire runs beside the white one and leaves it only to climb to its pin. Steps 11 and 12 use the camera solved from Lee's screenshot (picture 2). |
| Step 14, print and leaders | The board's print keeps only "24 bit color" and "64 RGB LEDs" (silkscreen.py), the label where it was. Each pin named at a different place along it, so that the three leaders run side by side; the close-up's ring is on the label, not beside a pin's; the close-up box keeps clear of the labels (it had covered them), and in a narrow window the labels keep their order (player). Checked at 1280, 1000 and 768 px wide. |
| Steps 15 - 17, matrix upright | The matrix held upright over the breadboard, header at the top: the pin's label, the hole's label (i2, b19, i3, its ring on the pin in the hole, where it shows: b19 itself is behind the 330 Ω resistor from this camera) and an eye on the socket, one camera for the three. |
| Step 18, arrow | Starts at the nut's back face; 1 mm above the leads, so that its head does not cut into the black lead. |
| Step 22, camera | Solved from Lee's screenshot (picture 4). |
| Step 23, USB A end, zoom | The A end is true to the CAD: the same model and size as the MRA's and Cadasio's (16 x 8.5 x 50 mm). Closer camera, shared by Steps 23 - 25. |
| Step 24 | Step 23's camera. |
| Step 25, D4 downward | D4 comes down from above beside its place, then is pushed 8 mm on: D1's and D2's tabs go through closed slots in D4, so it cannot come straight down into its seat (the caption says so). Step 23's camera. |
| Step 26, wires through the matrix and D4 | The matrix and its wires now keep pace beat by beat (player), and the wire shapes are matched from both ends (`tail_from`: the run in the box stays put, the run under the matrix moves with it). tools/motioncheck.py: no wire into any part at any of 19 moments of the move (an independent re-play at 800 moments agrees). The white and grey wires no longer pass through each other over the Nano. The caption now says the matrix is turned round. |
| Step 27 | Closer. |
| Step 28 | D5's lead lines at Lee's points on D1 and D2 (the D2 one from D5's face, as D2's tab end stands proud of it); the generator's two lines to D3's tabs are gone, and the caption names D1, D2 and D3. Question for Lee: bring the D3 lines back? |
| LED colour | The corner LED under the header: its window is fused into its body in Lee's STEP; materials.json paints it grey like the others, a round patch (a new "round" region option), so that it looks exactly like its neighbours. |
| Step 30, turn earlier, straight wires | The matrix is turned on its way out in Step 26 and stays that way; Step 30 is a lift and a move (two beats). The wires run dead straight along under its edge to beyond where D10 comes up. |
| Step 31, slower, zoom, arrow | Two beats (up, then along); the camera solved from Lee's screenshot (picture 5); the arrow outside the matrix, from D10's front face and below its lower edge (not through D10 or over its code). |
| Step 32, zoom, close-up | Closer, on the matrix and D10. The close-up draws the matrix at 0.12 (`ghost`, a new close-up option), and the sockets (in front of the slot) and D4 (over the end of D10's code) faint too, and looks at D10's end from beside the slot: "D10" reads whole and the three wires drop through the slot beside it. Lowered in one smooth move (through a half-way shape, without stopping) so that the wires shorten with it. |
| Steps 37 - 40 | Closer, near Step 33's framing, all four the same. |

Left as they are: for a moment while they change shape, two wires brush against each other twice in Step 26, both under the matrix,
and once in Step 32 (the grey and purple wires low in the box by D4, just over D4's edge from the step's camera); tools/motioncheck.py
lists them. Steps 23 - 25: the USB cable's A end lies 60 mm further out than it needs to now that D4 comes from above (assemble.py);
bringing it in would let these steps frame closer and make it look less big, but moves the cable in every later step: Lee's call.
Step 28 opens about 15% wider than Step 27, which Lee had zoomed in (Step 28's camera is unchanged).

An independent review of this round (three reviewers, skeptics, a completeness check: docs/research/lsm/round3/) found the points
fixed above after the first pass: the held grey wire, Step 14's close-up ring, b19's label, the Step 18 and Step 31 arrows, Step 32's
close-up and stop, Steps 39 - 40, the LED's square patch, the Step 26 crossing, Step 28's lines and captions.
