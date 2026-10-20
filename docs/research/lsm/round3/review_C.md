# LSM Full Build, Lee's round 3: independent review, group C (Steps 26 - 32, 37 - 40)

Reviewer: a subagent, 19 Oct 2026. Read only. No guide.py, build_model.py or browser runs. Evidence: `LSM Build Instructions/steps.json`
against the round-2 file (`scratchpad/steps_r3_before.json`), the guide diff, `player/js/player.js`, the renders in
`LSM Build Instructions/thumbs/`, `assembly-report.json` (part boxes), and a JSON-only re-play of the player's wire blending
(`scratchpad/rc/finecheck.py`, `vis26.py`, `vis32.py`: player.js `mixPose`, `throughPoses`, `alongPath`, `paced`, `skinned`,
`sampled`, the new `tail_from` matching, 160 samples per wire as the player draws them; 400 to 800 moments per motion; wires
tested against part bounding boxes, the matrix as its board + LED slab). The re-play agrees with `tools/motioncheck.py` where
both look (Step 26c grey/white 0.26 mm at 0.400 here, 0.20 mm at 0.40 there).

## Verdicts

| Note | Verdict | In short |
|---|---|---|
| Step 26: no wires through the matrix in the move, or through D4 near its end | partial | Matrix and D4 now clear; the white and grey wires pass through **each other**, in view, for about 0.12 s |
| Step 27: zoom in slightly | done | radius 135.7 -> 118 |
| Step 28: D5's lead lines at Lee's two points | done | both lines end at the points; the D2 line's D5 end floats 3.4 mm off D5 (low) |
| Step 30: matrix turned earlier, Step 30 only lift and move; wires straight past D10 | done | no turn in Step 30; straight run to z 1254 - 1257, D10 spawns at z 1242.7 - 1245.7 |
| Step 31: slower, camera as image 5, arrow visible | partial | camera and speed done, arrow visible, but it starts inside D10 and covers its engraved code |
| Step 32: closer; close-up with the matrix faint and a camera showing the wires in D10's slot | partial | zoom and fade done; the close-up reads "D1" and is a third black sockets |
| Steps 37 - 40: closer, near Step 33's zoom | partial | 37/38 done (90 vs 33's 84); 39/40 only to 100, and zoom out again from 38c |

## The notes one by one

### Step 26: done for the parts Lee named; partial overall
- The matrix now turns half round during the carry (carry poses 180 deg -> 90 deg (P_MID) -> 0 -> 0), four beats (D4's way
  `[ZERO]*5`), wires paced stop by stop through routes 43 - 45 / 46 - 48 / 49 - 51 (`wire_via`).
- Matrix and D4: no clip found. motioncheck (meshes, 19 moments) found none. My re-play at 800 moments also found none:
  closest approach to the matrix slab is 0.66 mm clear (km 0.83 white, 0.32 grey), to D4 1.65 mm (grey, km 0.98), to D2 1.09 mm.
  The one hit, purple 0.13 mm into the slab at km 0.011, is the opening pose and comes from my box model of the board.
- **Not met: wires through each other.** At km 0.372 - 0.41 (beat 2, the matrix moving over the box) the grey wire goes through
  the white one: centre lines 0.30 mm apart at 0.375, then 0.21 mm (0.378), 0.13 mm (0.3925) and **0.05 mm** (0.395) near
  [627.0, 891.0, 1184.3], with radii of 0.62 mm each. A ray test from Step 26's camera (top view, radius 82) finds the spot
  covered by neither the matrix nor a wall. It is on screen at about (350 - 390, 150 - 168) of 768 x 428, over the ICSP end of
  the Nano. Purple/white (0.01 mm) and grey/purple (0.04 mm) also touch at km 0.38, but under the matrix. Lee is watching this
  step for clipping, so this pale pair merging and parting is likely to be noticed. motioncheck reported the same thing
  (`review_motion.txt`). Wire shapes are interpolated at only 19 moments there, so its "no wire into any part" is weaker
  evidence than it looks: in mid-beat, half a beat's motion happens between two of its samples.
- No look in the browser from a low angle, where a clip under the matrix would show.

### Step 27: done
- Camera [617.4, 881.6, 1189.6] r 135.7 -> [622.0, 881.6, 1195.0] r **118.0** (13 % closer), the same direction. v_Step27: nothing
  cut off at 768 x 428.
- The flipped run's pivot moved with it, so Step 28's `pivot` changed too. That does not move anything on screen: the player
  turns both the model and the camera target about the same pivot (core.js `cameraPose`).

### Step 28: done (one small defect)
- `guides` are now exactly Lee's two points, each as tip = mouth: [682.6, 861.3, 1176.1] (D1) and [685.9, 864.8, 1254.2] (D2).
  The player draws each from tip + D5's hover (+42 x) to the mouth. Before there were four lines (D1, two on D3, D2 at y 899.8).
- **D2 line (low):** D2's tab end is proud of D5. D2 reaches x 685.89 and D5's outer face is at 682.51 (assembly-report).
  So the line's D5 end is at x 727.9 while hovering, 3.4 mm off D5's face, not at D5's slot. In v_Step28 (zoomed:
  `scratchpad/rc/z28.png`) it shows as a short red stub over D5's top corner, starting on nothing. The D1 point is flush with D5's
  face (D1 to x 682.68), so that line starts in D5's slot, as it should. Fix: give the D2 line as a pair,
  `[[682.5, 864.8, 1254.2], [685.9, 864.8, 1254.2]]` (slot on D5, then the tab end on D2).

### Step 30: done
- From Step 26c on, the matrix is in its own orientation (`P_OUTSIDE = [-90.76, 5.89, 25.09]`, no turn). Step 30c's carry is
  via `[-90.8, 56.6, 25.1]` then `[-0.2, 56.6, -0.3]`: a 50.7 mm lift, then a move across at that height, two beats (1.6 s), no turn.
  The frames m_Step30c_0.25 / 0.5 / 0.75 show it.
- Wires held over the box (routes 58 - 60): level under the board (y 950.75 - 951.13) from the sockets (z 1190.94) to z 1256.7
  (white), 1254.5 (grey) and 1255.9 (purple), then the U-turn down into the box. D10 appears at z 1242.65 - 1245.65 and rises into
  that straight run. f_Step31 shows the straight run along the matrix's edge.
- Minor: the grey wire is not quite "dead" straight. It closes from the sockets' 2.54 mm pitch to 1.7 mm with an overshoot: x 613.12
  -> 611.39 (z 1212) -> 611.9 (z 1224 on). At z 1212 its surface is 0.08 mm from the purple wire's. That is 0.6 mm sideways,
  hardly visible at Step 31's zoom.

### Step 31: partial
- Camera: [-0.6875, 0.4904, -0.5355], target [631.8, 932.6, 1218.0], r 63.4. ov-5.png overlays it on image 5: matches.
- Slower: D4 is given a way of three poses, so the step is two beats (`moveDur` 1600 ms; before 800 ms, `moving: []`). D10 rides
  `[0,-22,40] -> [0,0,40] -> 0` one stretch per beat (`paced`), with a stop between the rise and the slide. That is twice as long.
- Arrow: visible now, beside the matrix (f_Step31). **But it runs through D10.** The arrow in steps.json goes from
  [599.3, 927.64, **1247.18**] to [599.3, 927.64, 1219.68]. Its body spans x 598.3 - 600.3, y 925.9 - 929.4 (width 4, normal
  [-0.86, 0.51, 0]). At its opening pose D10 is at x 593.8 - 682.7, y 917.8 - 935.3, **z 1242.65 - 1245.65**, so the tail starts
  1.5 mm behind D10's end block and comes out through its engraved face. In f_Step31 (zoomed: `scratchpad/rc/arrow31.png`) the
  arrow comes out of the block and covers the lower half of the "10" of the engraved D10. That is the same defect Lee asked to
  have fixed on Step 18's nut. Fix: start the tail at D10's near face (seated z about 1202.9, i.e. 1242.6 at the opening pose) and
  move the arrow down or sideways, off the code.

### Step 32: partial
- Main view: DIAG, target [636, 912, 1210], r **66** (was 114.8). The matrix and D10 fill the top of v_Step32 and the USB cable runs
  out at the bottom right. Done. Every key part is inside the fit sphere (the matrix's far corner is 66.0 mm from the target, D10's
  end 65 mm), so narrower windows keep them in frame.
- Close-up: the matrix is drawn at 0.12 (`ghost`), an 88 % fade. Done.
- Close-up camera: dir [-0.30, 0.45, -0.84], r 10, looking along +z through D10's notch. Three problems Lee would see
  (inset32.png; as on the page: `scratchpad/rc/z32inset_page.png`):
  1. D10's engraved code is cut at the box's right edge and reads **"D1"**, the name of the base plate.
  2. The three black sockets ride on the matrix and are not faded. They sit between the close-up's camera (about
     [600.8, 904.3, 1180.0]) and the slot, so they fill the lower-left third and hide the slot's far wall (x 612.8).
  3. The wires look as if they curl up and over into the slot rather than lie in it. "How the wires fit in the slot" is only half
     shown.
  Fade the sockets with the matrix (`ghost={MATRIX: 0.12, J_*_F: 0.12}`) or aim past them, and move the target or widen the radius
  so that the whole "D10" is in the picture.
- Page (p_Step32c): with the model on the right, the box goes on the left and its leader runs about 300 px across the whole LED
  matrix to the spot at its far edge (low).

### Steps 37 - 40: partial
- Step 33: r 84, target y 913. Steps 37/38: 117.3 -> **90**, target [638.5, 922.0, 1204.5]. Close to 33: done.
- Steps 39/40: 126.4 -> **100**, target y 936. That is 19 % wider than Step 33 and 11 % wider than 37/38, so the view zooms out again
  between 38c and 39. On sheet_5 the box is about 270 px wide in 37 / 38c and 240 px in 39 / 40c (296 px in 33). r 90 would still
  hold the hovering stems: their tops reach y about 1013, against 936 + 90.

## Regressions and new problems next to these steps

1. **Step 32 lowers in two beats, with a full stop half-way** (medium-low, not asked for). The path is now
   `[[-0.2,56.6,-0.3],[-0.1,28.0,-0.2],[0,0,0]]` with no `stops`, and `alongPath` eases to a stop at every pose. So the matrix stops
   28 mm up, then goes on, and the step takes 1.6 s instead of 0.8 s. P_HALF was added so that the wires shorten without folding
   through D2. A `via()` pose would pass through it without stopping (the wire beats would then need to follow).
2. **Step 32c: grey and purple wires pass through each other** (low), at km 0.17 - 0.24. Centre lines go down to 0.18 mm
   (km 0.2125) beside D10's end, near [610.5, 929.9, 1238.2]. A ray test finds it in view from Step 32's camera, at about
   (482 - 507, 136 - 200) of 768 x 428. Brief (about 0.13 s).
3. **Step 26c: white and grey wires through each other** in view (see Step 26 above; low-medium).
4. **Step 31: the arrow pierces D10 and covers the "D10" code** (see Step 31; medium). Lee raised this kind of thing on Step 18.
5. **Step 28 opens 15 % wider than Step 27c** (low). Step 27 went to r 118 at a new target, while Step 28 (not named, so rightly
   left alone) stays at r 135.7, [617.4, 881.6, 1189.6]. Before, the two framings were identical. Worth asking Lee whether 28
   should follow 27.
6. **Step 28: the D2 lead line starts 3.4 mm off D5** (low; see above).
7. **Step 26's caption does not mention the half turn** (low). The matrix's half turn moved from Step 30 into Step 26, but the
   caption is unchanged ("Lift the LED matrix over D4 and lay it down outside, its wires over the top edge of D4."). A student
   following the words alone lays it down the wrong way round for Step 30.
8. **Steps 38c -> 39: zoom out of 11 %** (low; see Steps 37 - 40).

Checked and found harmless: D4 in `moving` with a still way on Steps 26, 30 and 31 is used by the player only for ways (beats).
Step 28's pivot change has no effect on screen. From Step 33 on, the wire routes are only renumbered (same points). No step
camera outside Lee's list changed. Not new in this round: the USB A end and cable are partly under the matrix laid outside D4
(Steps 26c - 30). The matrix's place there is the round-2 one (the same centre, only no longer turned).
