# Geometry review of the base and controller steps (Steps 1 - 24)

Review only: nothing in the project was changed, `guide.py` and `build_model.py` were not run, no browser was used.

**What was reviewed.** The guide was regenerated while this review was running (`guide.py` 22:31:28, `steps.json` 22:31:36,
`stepgen.py` 22:28, `player.js` / `core.js` 22:27, all 13 Oct 2026). Every number below is for that latest state:
`steps.json` md5 `aaaec44a354026e46c961483191e5a9b`, 48 views, 28 routes. It was checked from a frozen copy, and the
project copy still had the same md5 when this report was finished. (A first pass on the 21:49 version gave the same
answers wherever the guide did not change; the old horn path peaked at 0.60 mm, the new one at 0.48 mm.)

Model: the generator's own, `stepgen.Model(mra.glb, adjust=materials.json "adjust_mm")`, loaded once and kept as arrays.
Scripts and raw output: `scratchpad/review_bc/geometry/` (`s00` .. `s46`, `snap_2231/out/*.log|json`; first pass in `old_2149_outputs/`).

## How the numbers were made

- "Inside" is decided by the generalised winding number (> 0.5), not ray parity: the wood parts are not watertight in
  trimesh's sense (each engraved code is a patch of duplicated faces) and the motor carries loose label decals. Depth =
  distance from an inside point to the surface of the body it is inside. A 3 mm board gives at most 1.5 mm, so
  "1.5 mm deep" means "through the full thickness".
- Each part is sampled at every vertex plus surface points about 0.8 mm apart; both directions are tested.
- The plug NAUO83 is tested as the player draws it (housing + three contacts). Its CAD instance also carries 40 mm of
  straight cable, which `model.glb` leaves out (`Cable_JR: omit`).
- Poses, paths, riding parts and wires are ports of `js/player.js` (`mixPose`, `alongPath`, `composePose`, `throughPoses`,
  `skinned`, `sampled`, the route blending in `drawWires`). Transitions are sampled evenly along each beat's travel.
- Camera: eye = target + dir x radius / sin(22.5 deg) x 1.08, 45 degree vertical field of view, 16:10 frame.
  "ndc" = position in the frame, -1 .. 1 on each axis.

## Findings

In the guide: F1 - F9. In the CAD itself: the 0.56 mm motor / R2 fit, the hooked tabs, and the fact behind F1 that the
module has no rigid way in. Order: largest effect on screen first.

| | Step | What | Mark |
|---|---|---|---|
| F1 | 22c | module's board edge through both B6 arms, 1.50 mm, half the animation | ask Lee |
| F2 | 9 | both lead lines 0% visible, ends 6.2 mm from any part | must fix |
| F3 | 23c | lead inside R4 up to 1.50 mm for 44% of the animation | should fix |
| F4 | 8c | lead cuts the corner of the L-shaped slot, 1.42 mm, 14% of the animation | should fix |
| F5 | 20c | B6 right's arm passes through the left joystick's wires | ask Lee |
| F6 | 10 | the two lines to the horn 7% and 10% visible | ask Lee |
| F7 | 20 | one line floats in the B6 / B3 joint, 54 mm against 74 - 77 | should fix |
| F8 | 4, 5 | hand-set lines end 3.5 mm below R1 | ask Lee |
| F9 | 2 - 23c | lead and jumper wires change length between views | ask Lee |

### F1. Step 22c: the I/O module's path goes through both B6 arms. ask Lee

- Path `[[0, 6, 70], [0, 6, 0], [0, 0, 0]]`. The board's +x edge strip (x 94.9 - 96.7, the 1.65 mm board at y 110.8 - 112.4 while
  lifted) is inside the post at the end of B6 right (NAUO6) by up to **1.50 mm** in 42 of 79 frames (from 51% of the slide to
  88% of the drop), and inside B6 left (NAUO5) by up to **1.46 mm** in 20 of 79 frames (from 83% of the slide). Seated fit of the
  same pairs: 0.13 mm. Nothing else is touched. The riding caps touch nothing.
- Why: each B6 arm holds the board's two edges in a horizontal groove (y 104.8 - 106.3, at x 43.0 - 45.2 and x 94.7 - 97.0) that is
  closed above: 12.2 mm of wood over the +x groove (up to y 118.5), about 3 mm over the -x groove. A board can only enter
  those grooves by sliding along z at its seated height. But B4 has an end lip at z 173.5 - 179.8 that stands up to y 107.9, 3.1 mm
  above the board's underside (104.78).
- **In the CAD itself there is no rigid way in.** Measured by lift and distance out (worst depth of the module in each part):

  | Lift | B4 lip | B6 right | B6 left |
  |---|---|---|---|
  | 0 mm (level) | 1.32 - 1.48 mm for the whole slide after the first 6 mm | 0.13 (seated fit) | 0.13 |
  | 1.5 mm | 1.30 - 1.48 | 1.18 - 1.42 from 20 mm out | 1.09 - 1.38 from 10 mm out |
  | 3 mm | 1.07 at 50 mm out, then 0.11 | 1.37 - 1.50 | 1.31 - 1.46 |
  | 4 - 6 mm (as authored: 6) | 0.00 - 0.10 | 1.17 - 1.50 | 1.31 - 1.46 |

- So the guide chooses which wood the board passes through. As authored it is the two B6 posts, in full view, plus a 6 mm drop
  that cannot happen (the grooves are closed above). A level slide (`path=[[0, 0, 70], [0, 0, 0]]`) passes only through B4's lip:
  a 3 x 6.3 mm tab under the middle of the board. The video note in `guide.py` says the board "slides in level ... through the
  slot in each B6 arm, and is pressed down at the end", which matches the level slide with the board's trailing end riding over
  B4's lip. Fix if Lee agrees: the level slide, one leg; the four lead lines already end in the grooves and on B4.

### F2. Step 9: both lead lines are completely hidden, and their fixed ends are in mid-air. must fix

- `lines_at=[[157.3, 92.0, 118.0], [170.0, 92.0, 118.0]]`: the points are on B2's slot edges (0.01 mm), but at mid-thickness
  (y 92.0), and each line's seated end is 6.19 mm from the nearest part that is on screen (R5), under the turret.
- With the camera the generator chose (`dir [-0.5792, 0.5736, -0.5792]`, from the far side of the turret) **0 of 41 samples of
  either line can be seen** (behind R1, R4, R5, R6, R2 and B2 itself). With labels off the step has no visible cue at all.
- Tested fix: put the lines on B2's top face and end them where the slot edges pass under R6:
  `lines_at=[[[157.3, 93.55, 129.0], [157.3, 93.55, 172.3]], [[170.0, 93.55, 129.0], [170.0, 93.55, 172.3]]]`. Tips 0.02 mm from B2,
  seat ends 0.10 mm from R6, and from the side B2 comes from (`dir [-0.5792, 0.5736, 0.5792]`, the view Step 10 uses) both lines
  are 100% visible. From the present camera they are 32% and 2% visible, so the view has to change too (the generator's own
  score should then pick it, since it counts visible line samples).

### F3. Step 23c: the base lead is dragged through R4 while the plug travels. should fix

- For **44% of the 1.6 s** animation (12% to 65% of the time) the lead's centre line is inside R4's wood beside the L-shaped
  slot, up to **1.50 mm deep** (brown at [133.4, 144.4, 138.8]; red 1.49, orange 1.42), over about 4.8 mm of wire.
  Both end views are clean (see "Right as it is").
- Cause: `skinned()` moves every point of a route with the plug in proportion to how far along the wire it is. The slot is
  69% of the way along the loose route (54 of 77 - 80 mm), so that point follows about 83% of the plug's movement.
- The lead also grows from 78 mm to 211 mm while the plug moves 55 mm, and for 5 of 91 frames its top edge is 1% outside the frame.
- Fix: draw each conductor as two wires that meet in the slot's pocket (servo to pocket with `a=BASE_MOTOR` only; pocket to plug
  with `b=BASE_PLUG` only), or give `route()` a "stays put up to N mm" option that `skinned()` honours. Either removes F4 as well.

### F4. Step 8c: the lead cuts the inside corner of the L-shaped slot. should fix

- With the new in-between route (over R4's top edge, then into the pocket) the lead is inside R4 for 14% of the 0.8 s animation
  (58% to 71% of the time): orange up to **1.42 mm deep** at [133.6, 138.2, 144.1], red 0.72 mm, brown 0.06 mm. That spot is the
  wood between the slot's stem (z 140.6 - 142.7) and its pocket (y 127.3 - 135.8): the blend goes diagonally from "over the edge" to
  "in the pocket" instead of down the stem and then across.
- Step 8 is now a close-up (frame radius 50), so it shows. Fix: one more in-between route with the lead at the foot of the stem
  (about y 136.5, z 141.7 at R4's plane) before the pocket, with a matching plug pose in `ride=`.
- The plug itself touches nothing on the way (0.00 mm, 121 frames) and stays in frame (worst ndc 0.78).

### F5. Step 20c: B6 right's long arm comes down through the left joystick's four wires. ask Lee

- At 44% to 59% of the 80 mm descent the four left wires (drawn stretched to the module parked at z + 100) are inside
  B6 right's arm: centre line 1.41 - 1.47 mm deep at about [64 - 66, 134 - 138, 151.5], 3 - 4 of 28 frames each. Afterwards they lie
  above the arm, and the done view is clean.
- The step's own review note already asks this ("park the module on the other side?"). With the module where it is, no straight
  path for the group avoids the wires: they span the arm's whole footprint. Parking the module on the other side was not tested.

### F6. Step 10: the two lead lines to the horn are hidden behind B2. ask Lee

- B1 comes up from 65 mm below with the camera above. Of the four lines, the two that carry the step's point (the ends of
  B1's horn-shaped cut-out to the horn) are **7% and 10% visible**; B2 hides 37 of 41 samples of each. The two corner lines are 100% visible.
- All four are well anchored (tips 0.35 - 1.38 mm from B1, the horn ends 0.24 mm inside the horn arms).
- This follows from Lee's point 13 (B1 starts below B2). The house alternative (rulebook section 7) is to show the kit turned
  over so the horn and cut-out face the camera.

### F7. Step 20: one of the four lead lines floats in the B6 / B3 halving joint. should fix (small)

- Line `[2.7, 93.8, 151.5] -> [2.7, 119.6, 151.5]`: the tip is 1.51 mm from B6 right (in the open notch, not on wood), the mouth
  1.60 mm from B3 (in B3's notch). It is 54.2 mm long against 74.1 - 77.1 mm for the other three, and 51% visible.
- Step 17 (the mirror-image step) has four tab-to-slot lines into B2. Fix: `lines_to=[B2]` on the Step 20 `seat()`, or four `lines_at` points.

### F8. Steps 4 and 5: the hand-set lines end 3.5 mm below R1. ask Lee (small)

- Lee's points are on the tab tips (0.03 mm from R3 / R4). Used as single points, each line's seated end is the tab tip where
  it finally sits: 3.48 mm (R3) and 3.61 mm (R4) below R1's underside, hidden under R1 (the lines are 88 - 90% visible).
- Harmless on screen. To end in the slot as the house rule says, give pairs, e.g. `[[193.6, 96.6, 121.5], [193.6, 102.96, 121.5]]`.

### F9. Wire lengths are not constant. ask Lee

- Base lead as drawn: 59 mm standing up (Steps 2 - 8), 87 - 90 mm on the in-between route, 77 - 80 mm in the slot (Steps 8c - 23),
  211 mm plugged in (Step 23c on; the CAD lead is 211.1 mm).
- Joystick wires, 106 - 117 mm as routed in the CAD: left set 192 - 197 mm in Step 17, 171 - 177 mm in Steps 17c - 21c, 145 - 151 mm in
  Step 22; right set 168 - 173 mm in Step 20, 142 - 149 mm in Steps 20c - 21c, 120 - 127 mm in Step 22. They stretch like elastic to
  reach the parked module.

## Right as it is

**1. Poses**
- Seated CAD, all 43 parts: the only overlap over 0.5 mm is Base Motor x R2, 0.56 mm (top edge of R2's notch in the top of the
  motor case, strip x 158.2 - 169.4, y 123.3 - 123.9). Others: screws in B1 0.35 mm (threads), motor shaft in horn 0.23 mm, screws under
  heads in B2 0.14 mm, tab fits 0.12 - 0.13 mm. The horn no longer overlaps B2 (`adjust_mm` on NAUO46). All of these are the CAD's.
- Every hover, riding and parked pose in every view: no overlap at all (0 posed pairs over 0.05 mm). Nearest approach under 4 mm:
  B2 hovering 1.14 mm from R6 in Step 9.
- **Step 2c, the horn through R1** (473 frames): the motor case never touches R1 (0.00 mm). The horn overlaps R1 only in beat 2,
  for 9 frames, worst **0.48 mm** where the trailing arm tip passes the end of the cable notch ([163.66, 102.47, 153.68]). No frame over 0.5 mm.
  - Hover: lifted 52 mm, quarter-turned, tilted 28 degrees, leading tip 30 mm above R1.
  - Stop 1: lifted 17.45, tilt 24: leading tip at [163.7, 99.5, 125.8], just through the cut-out (rim at z 124.09, underside y 99.96).
  - Through the vias: tilt 12, 9, 0 while sliding 6 mm along the cut-out; leading arm 7 mm under the far rim, trailing tip down through the notch.
  - Stop 2: level and centred, lifted 8.45: case bottom 1.05 mm above R1, arm tops 1.10 mm below it.
  - Beat 3: quarter turn about the shaft, 0.00 mm overlap in 170 frames. Beat 4: down 8.4 mm.
  - This is the move Lee describes in his second message: at an angle, rotated into the slot, spun 90 degrees about the vertical, set down.
- Step 23c, the plug's new path (slot, up and over, straight down onto row 5): 0.00 mm against everything, 166 frames, in frame (worst ndc 0.75).
- Straight paths: Steps 9c, 10c, 14c, 15c, 16c, 18c, 19c touch nothing. Steps 3c - 7c, 13c, 17c, 20c, 21c show 0.99 - 1.21 mm in the last
  3 - 8% of travel only: the CAD's hooked tabs snapping into their slots, inside the generator's 1.2 mm snug-fit allowance. Screws 0.20 mm.

**2. Lead lines**
- Every straight line is 0.0 degrees off its travel; Step 22's two-leg lines follow both legs. Step 2's single line (30.4 mm, from the
  leading arm tip to the far rim of the cut-out) is 5.2 degrees off the first leg; tip 0.22 mm inside the horn, mouth 0.21 mm from R1.
- All other tips and mouths are within 1.5 mm of the right part: 1.45 - 1.47 mm means "in the middle of a 3 mm tab or slot".
  Screws: tip 0.03 - 0.07 mm from the screw's point, mouth in the middle of the hole at B2's top face. Step 22: 0.02 - 0.20 mm.

**3. Wires**
- In all 46 views with wires, no wire's centre line is inside any part. The only contact with a part a wire does not join: the brown
  conductor grazes R4's face where the lead leaves the slot (tube 0.16 mm into it in Steps 8c - 23, 0.34 mm when plugged in).
- Ends, worst over all views: lead to servo stub 0.008 mm; lead to plug contact 0.099 mm, right contact every time (brown G, red V,
  orange S; row 5 at z 139.46); lead meets the plug within 4.6 degrees of its axis, riding or seated. Joystick wires to their caps
  0.089 mm and 0.007 mm; caps on A2 G / A2 V / A2 S / A3 S (left) and A0 G / A0 V / A0 S / A1 S (right), 0.084 mm off the pin axes (the CAD's own offset).
- In-hand views: cut ends and break marks are 32 - 47 mm from the nearest part.
- Steps 2c, 17c, 22c in motion: no wire touches anything.

**4. Labels and eyes**
- All 23 anchors are on a visible part and in frame (worst ndc 0.51). 22 are within 0.29 mm of their part. The Step 8 eye is 1.36 mm
  from R4 because it sits in the flared mouth of the slot, which is the intent.
- Nothing stands between any anchor and the camera. The "5" anchor is on the axis of row 5's V pin at its foot (0.29 mm inside the pin).

**5. Framing**
- Every hover view: moving parts, riders, seats and lead lines inside the frame (worst ndc 0.85, Step 16). Idle parts are cropped only
  in the three intended close-ups (Steps 8, 11, 23).
- Travel against the view axis: 50.1 - 55.0 degrees overall for every step, 69.5 for Step 23. Per leg the only one under 40 is
  a 2.9 mm via leg inside Step 2c (39.2); Step 23's first leg is 42.7.
