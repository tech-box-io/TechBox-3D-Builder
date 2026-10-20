# LSM Full Build, Lee's round 3 (19 Oct 2026): combined review summary

Sources: Lee's notes word for word (`docs/research/lsm/lee_notes_2026-10-19b.md`), reviews A, B and C in this folder, the
skeptics' checks, and my own completeness pass. I looked at the pictures myself and read `steps.json` against the round-2 file
(`scratchpad/steps_r3_before.json`). I ran nothing heavy, used no browser and changed nothing in the repository except this file.

**State of the evidence (read first)**
- `materials.json` and `tools/build_model.py` were edited at 22:55:38 to fix the corner LED (a round region). **That fix has not been
  built.** `model.glb`, `model.report.json`, `steps.json` (model stamp 53ca34eeb61f), `parts/LED-Matrix.png` (22:31) and
  `cards/steps.webp` (22:32) all come from the 22:18 model. Every check (runthrough, wirecheck, motioncheck) and every render came
  before the edit.
- `player.js` changed at 22:24:33. Only `p_Step6/14/16/32c.png` (22:25) show where the final player puts close-ups.
  `sheet_*`, `z_*` (22:15-22:16) and `f_*` (22:22) came before that change.
- Lee's own screenshots are 2000 px wide and look like Retina 2x captures, so his window is about 1000 CSS px wide. No render
  with the final player was made at that size, nor at 768.
- iCloud made " 2" copies at about 22:18 (in `scratchpad/quarantined.txt`). The LSM copies were identical and none is left in the
  kit folder.

## 1. Each note: final status

| # | Lee's note (part) | Status | Evidence / what is left |
|---|---|---|---|
| 1 | Step 6: his Capacitor Breakout picture | Done | inset.image `capacitor-card.webp`, byte-identical to his 1.webp. In p_Step6 the box sits clear of the eye and the labels. Low: the photo is a mirror of the 3D view (its strip and GND leg on the left; in the model on the right). The close-up caption says "strip" (his picture's word), the step and Step 7 caution say "stripe". |
| 2 | Step 7: lead lines at his two points | Done | guides are exactly [652.5, 863.6, 1170.6] and [652.5, 863.6, 1173.1]. Camera, labels and eye unchanged. |
| 3 | Steps 10-11: wires "basically fully separated" in 11 | **Partial** (confirmed) | Step 11 opening: 63 of 72 mm within 3.5 mm. **Step 11c and the Step 12 opening:** 13 of 72 mm within 3.5 mm, 23-27 mm apart over the grey's first half (v_Step11c, sheet_0). Step 10 is unchanged, as it should be. |
| 4 | Steps 11 and 12: camera like image 2 | Done | 11/11c/12/12c share dir [-0.3282, 0.6298, -0.704], target [644.3, 895.7, 1180.6], r 38.3 (cmp-2). **New side effect, found on comparing f_Step12c with image 2:** in 12c (and 13/13c) the ribbon now lies low across columns g/h and hides most of the 12 kOhm resistor, which is clear in Lee's own screenshot. Held sockets about 2.5% from the top edge (image 2: about 6%). |
| 5 | Step 14: remove BTE, Better than Expected, Only ONE Pin, WS2812B-64 | Done | decals.json keeps only "24 bit color" and "64 RGB LEDs". The BTE fill is gone too. |
| 6 | Step 14: adjust the remaining text, white label where it is | Done | The two lines are centred at [31.9, 26.0/30.5]. The label entry is unchanged (git diff touches only the back print). |
| 7 | Step 14: leaders overlapping and confusing (image 3) | Done at 1152 x 720 only | Eye removed. Labels sit at three places along the pins. In p_Step14 (4x crop) no leaders cross. **Not checked** at Lee's size (about 1000 CSS px) or at 768. The f_/v_ renders from before the player change show the close-up leader through the V+ ring. Still there: four rings on three pins, with the close-up's ring on the V- pin's tip next to the V+ ring (target [612.5, 894.5, 1191]). |
| 8 | Step 15 (and 16, 17): matrix vertical, header and breadboard seen together | Done | One upright MATRIX pose and one camera for 15-17c (r 48). z_Step15, p_Step16 and sheet_1 show the header with i2/b19/i3 in one frame. |
| 9 | Steps 15-17: a lead line to the breadboard connection besides the eye and the pin's leader | **Partial** (confirmed) | 15 has i2 and 17 has i3. **Step 16's b19 ring sits on the 330 Ohm resistor** (the ray to the hole hits R330 11.8 mm short; z_Step16 and p_Step16 at about (670, 465)). Step 17's hover view was never rendered. The pin labels and eyes are kept on all three. |
| 10 | Step 18: arrow from the nut's rear surface | Done | Tail at z 1253.42, 0.11 mm behind the nut's back face. Pre-existing and confirmed by me (f_Step18, 4x): the arrowhead's upper barb runs into the black lead, the same "passes into" kind of fault. |
| 11 | Step 22: camera as image 4 | Done | 22/22c dir [0.6491, 0.6967, -0.3055], r 35.5. ov-4 nearly coincides. Step 21 unchanged. |
| 12 | Step 23: "Is the USB A end the correct size?" | **Question: needs an answer in the reply** | True to the CAD: 49.7 x 15.9 x 8.55 mm in lsm.glb, no scale, the MRA's model. It looks big because it is nearer the camera (x1.17), and the new camera made it grow more than the base (+24% vs +17%, B's numbers). |
| 13 | Step 23: zoomed out too far | Done | r 148.7 -> 125, same direction. Still framed by the A end lying about 130 mm out (see problem 22). |
| 14 | Step 24: same view as the new Step 23 | Done | Identical camera. |
| 15 | Step 25: D4 comes in downward | Done, with an 8 mm push at the end | path [-8, 65, 0] -> [-8, 0, 0] -> 0. The push is needed (closed slots) and **must be explained in the reply**. Caption "Lower D4 down" says it twice. |
| 16 | Step 25: Step 23's view | Done | Identical camera (camdiff shows it as NEW only because the caption changed). |
| 17 | Step 26: wires through the matrix, and through D4 near the end | **Partial** | Parts: motioncheck (meshes, 19 moments) and C's re-play (800 moments) find no wire in the matrix or D4 (D4 1.65 mm clear). **But the white and grey wires pass through each other in view**: 0.20 mm apart at 0.40 (motioncheck) and 0.05 mm at 0.395 (C), near [627, 891, 1184], over the Nano's top end, not hidden by the matrix. It was not caught in a frame: renders exist at 0.4 and 0.45 only, and m_Step26c_0.4 shows the pair touching side by side there. |
| 18 | Step 27: zoom in slightly | Done | r 135.7 -> 118, same direction. Side effect: Step 28 (not named) now opens 15% wider than 27c. Before, they matched. |
| 19 | Step 28: his points on D1 and D2 | Done as lead lines, but see the new item | guides = exactly his two points. **Not reported by anyone:** round 2's two lines to D3's tabs (z 1155.1) were dropped, while the caption still reads "Push D5 onto the open end, over the tabs of D3 and D2". Now no line goes to D3, and one goes to a D1 tab the caption does not name (D1, D2 and D3 all pass through D5: D1 to x 682.68, D3 to 685.18, D2 to 685.89). The D2 line starts 3.4 mm beyond D5's face as a red stub over its corner (z28.png). |
| 20 | LED under the header to match the others | **Partial; fix written, not built** | The 22:18 model colours a 3.7 mm square, which leaves a square frame with diagonal corner ticks (parts/LED-Matrix.png against HEAD, ledcorner.png). `"round": "xy"` was added at 22:55 but not built. |
| 21 | Step 30: turn the matrix earlier (a question), so that Step 30 is a lift and move | Done; **answer the question in the reply** | The half turn is in Step 26c (carry 180 -> 90 -> 0). Step 30c goes via [-90.8, 56.6, 25.1] to [-0.2, 56.6, -0.3]: a 50.7 mm lift, then a move, no turn. |
| 22 | Step 30: wires dead straight until beyond where D10 spawns | Done | Routes 58-60 are level (y 950.75-951.13) to z 1254.5-1256.7. D10 spawns at z 1242.65-1245.65. The grey wire overshoots 0.6 mm sideways (hardly visible). |
| 23 | Step 31: slower | Done | Two beats (1600 ms, was 800): rise, then slide. |
| 24 | Step 31: zoom like image 5 | Done | dir [-0.6875, 0.4904, -0.5355], r 63.4. ov-5 matches. |
| 25 | Step 31: arrow not visible | **Partial** (confirmed by me) | The arrow is visible now, but its tail starts inside D10's end block (tail z 1247.18, D10 at z 1242.65-1245.65) and the arrow covers the lower half of the engraved "10" (f_Step31; arrow31.png). |
| 26 | Step 32: zoom in, USB may leave the view, focus on the matrix and D10 | Done | r 114.8 -> 66, target [636, 912, 1210]. |
| 27 | Step 32 close-up: matrix about 90% faded | Done | ghost {MATRIX: 0.12}, an 88% fade. |
| 28 | Step 32 close-up: camera showing how the wires fit in D10's slot | **Partial** (confirmed by me, inset32.png) | D10's code is cut at the edge and **reads "D1"**. The three sockets ride on the matrix but are not faded: they fill the lower-left third as a solid black block and hide the slot's far wall. The wires look as if they curl over into the slot. On the page (p_Step32c) the leader crosses the whole matrix. |
| 29 | Steps 37 and 38: closer, near Step 33 | Done | r 117.3 -> 90, target [638.5, 922, 1204.5] (Step 33: r 84, the same x and z). |
| 30 | Steps 39 and 40: "Same as 37" | **Partial** (confirmed by me, sheet_5) | r 126.4 -> 100, so the view zooms out 11% from 38c to 39. In 39 and 40c the box is visibly smaller than in 37/38c, with room left above the stems. |

## 2. Confirmed problems, most severe first, with fix hints

1. **Steps 11c and 12 (opening): the wires still come apart** (medium; it is Lee's note). The held grey uses HOVER_MIDS (`_hi`,
   guide.py:401), which meets `_lo` only at its last two points.
   - Fix: a "grey held, white plugged" route on Step 11's wires_done that follows `_rib(_lo, 1)` from the sockets back and climbs to
     PIN_HOVER only over the last 30-35 mm.
   - Or lift the plugged white wire to the hover ribbon in 11c.
   - Then wirecheck/motioncheck Steps 11-12 and diff the cameras.
2. **Step 16: the b19 label points at the 330 Ohm resistor** (medium; Lee's note).
   - Anchor it on the visible purple pin housing, e.g. [627.04, 877.0, 1213.63] (y 876.5-878.5; not 875.5, whose ring still touches
     R330).
   - Or give Step 16 its own camera, which breaks Lee's one camera for the three steps: ask him first.
3. **Step 31: the arrow comes out of D10's end block and covers "10"** (medium; the same fault Lee had fixed on Step 18). Start the
   tail at D10's near face (about z 1242.6 at the opening pose) and move the arrow off the code, down or sideways.
4. **Step 32c close-up: reads "D1", sockets in the way** (medium; Lee's note). Fade the sockets with the matrix
   (`ghost={MATRIX: 0.12, J_WHITE_F: 0.12, J_GREY_F: 0.12, J_PURPLE_F: 0.12}`) or aim past them. Move the target or widen the radius so
   that the whole "D10" shows.
5. **Step 26c: the white and grey wires pass through each other, in view, for about 0.12 s** (medium; Lee is watching this step for
   clipping).
   - Separate their beat-2 shapes (routes 43-48) near [627, 891, 1184].
   - Fix it, or at least do not tell Lee these contacts are "mostly under the matrix": the What-was-done note says so, but this one
     and the Step 32c one are both in view.
6. **The corner LED: the fix is not in the model** (medium until built).
   - Run build_model.py, then guide.py (model stamp), parts.html (parts/LED-Matrix.png) and `_dev.card()` (the card is now drawn from
     another model, so publish will warn).
   - Check the corner LED close up against its neighbours.
7. **Step 28: the caption and lead lines disagree** (low-medium; new). The caption names D3's and D2's tabs; the lines go to D1 and
   D2. Round 2's two D3 lines were dropped on the reading that Lee's two points replace all four. Either bring the D3 lines back,
   or change the caption to name D1, D2 and D3, and tell Lee which.
8. **Steps 39 and 40 are not "same as 37"** (low-medium). r 90 (as 37/38) at target y 936. sheet_5 shows room above the stems. Check
   that the hovering stem stays in frame.
9. **Step 32: the lowering stops half-way** (low-medium; not asked for, but disclosed in the What-was-done note). path [P_HELD, P_HALF,
   ZERO] with no `stops`, and player.js `alongPath` eases to a stop at every pose. Use `via(P_HALF)` if the wires can keep pace;
   otherwise tell Lee why.
10. **Steps 12c-13c: the ribbon hides the 12 kOhm resistor** (low-medium; new against Lee's own image 2). Keep the ribbon but lift it
    clear of h3-h16, e.g. rising more steeply from the pins as in image 2. A also measured a bend of about 1.4 mm radius at each pin
    housing.
11. **Step 18: the arrowhead's barb runs into the black lead** (low; pre-existing, visible in f_Step18). Move the arrow 1.5-2 mm
    towards +x.
12. **Step 28: the D2 line is a stub beyond D5** (low). Give it as a pair [[682.5, 864.8, 1254.2], [685.9, 864.8, 1254.2]].
13. **Step 32c: grey and purple touch in view** (low). motioncheck 0.45 mm at 0.20; C 0.18 mm near [610.5, 929.9, 1238.2].
14. **Step 32c: the close-up's leader crosses the whole matrix** (low; p_Step32c).
15. **Step 28 opens 15% wider than Step 27c** (low). Ask Lee whether 28 should follow 27.
16. **Step 26's caption does not say the matrix is turned round** (low). The half turn is now in this step.
17. **Step 25's caption: "Lower D4 down"** (low).
18. **Step 6: the photo is a mirror of the model; "strip" vs "stripe"** (low).
19. **player.js:456** (low, every kit): the extra tries `[12, sy]` and `[W - boxW - 12, sy]` for the top and bottom sides are not checked
    against `onScreenInstructions()`, and `covered()` counts only labels. A top-side close-up could land on the caption.
20. **Steps 15-17: the caption box covers the matrix's top-left strip at 1152 x 720** (low; p_Step16). The header stays clear.
21. **Steps 23-25: the A end lies 60 mm further out than it needs to** (suggestion). The assemble.py reason (D4 came in from 65 mm
    out) no longer applies. Bringing it in would let Steps 23-25 frame closer and make it look less big. Lee's call: it moves the cable
    in later steps.
22. **Steps 11-12: the held sockets are about 2.5% from the top edge** (low). Look at narrow windows.

## 3. Not verified by anyone

- Step 14 at Lee's window size (about 1000 CSS px wide) and at 768 with the final player. Do the close-up box and its leader stay
  clear of the V+ ring and the caption?
- Step 17's hover view (the i3 label). It was only projected, never rendered.
- The Step 26c and 32c wire contacts in an actual frame (crossings at 0.395 and 0.21; frames exist at 0.4/0.45 and 0.2).
- Close-up placement for Steps 6, 14 and 32c at sizes other than 1152 x 720.
- The bend radius of about 1.4 mm at the pins (A's numbers only) and how it reads on screen.
- Step 23's on-screen growth figures (B only). Whether r 90 holds Steps 39/40's hovering stem (C's estimate; sheet_5 agrees there
  is room).
- Every check after the 22:55 edit. After the rebuild, run runthrough on the LSM again (and on every kit if build_model.py changes
  their output), then wirecheck and motioncheck. Also check that `check_site`/publish accept the new card and parts picture.

## 4. Easy to miss in the reply to Lee

- **Step 23 asks a question.** Answer it: true to the CAD (16 x 8.5 x 50 mm, the MRA's and Cadasio's model). It looks large from
  perspective and its place on the table; offer to bring it 60 mm closer.
- **Step 30 asks a question** ("I am wondering if we should..."). Say yes: it is now turned in Step 26, and Step 30 is a lift and a
  move.
- **Step 25:** explain the 8 mm push at the end (D1's and D2's tabs go through closed slots in D4; the published guide pushes it on
  too). Otherwise it looks like the "in toward D1" he asked to remove.
- **Step 28:** say that only his two lines remain, the D3 lines are gone, and the caption still names D3. Ask which he wants.
- **Step 32:** mention the new stop half-way down (or remove it).
- **Steps 26 and 32:** do not describe the wire contacts as hidden. The white/grey one in Step 26c is in view.
- **Steps 15-17:** if b19 stays where it is, say so (a hole hidden by the resistor). Better, fix it first.
- **Step 6:** the close-up is his photo as supplied, mirrored relative to the model.
- **Process:** after the fixes, publish the round to the test preview (`--to "share/Test guides preview"`, Lee reviews on
  http://localhost:8799). Never push live without Lee's word.
