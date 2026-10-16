# Geometry review of the arm, claw and final wiring (Steps 24 - 85)

Review only: nothing in the project was changed, `guide.py` and `build_model.py` were not run, no browser was used.

**What was reviewed.** A frozen copy taken at 23:41 on 13 Oct 2026: `steps.json` md5 `75fc3793f2fb66fe12d6fe2441b4d52d` (168 views,
115 routes), `guide.py`, `materials.json`, `wire-paths.json`, `stepgen.py`, `wires.py`, `js/`. The project's `steps.json` was regenerated at
23:43 with the same md5; the only later `guide.py` edit is to `PART_VIEWS` (part pictures), so every number below holds for the
current guide. Scripts and raw output: `scratchpad/review_ac/geometry/` (`s00` .. `s44`, `out/*.log|json`), adapted from
`scratchpad/review_bc/geometry/`. `s43_bfrom_test.py` / `s43b_test.py` test proposed fixes on in-memory copies only.

## How the numbers were made

- The CAD is loaded once (`s00_cache.py`) exactly as `stepgen.Model` does it (top-level instances, mm, merged vertices, `materials.json`
  `adjust_mm`). Every part is tested as `model.glb` draws it: the 40 mm of `Cable_JR` on plugs NAUO83 / 84 / 86 is left out (the `omit`
  rule); the other plugs have no cable in the CAD.
- "Inside" = generalised winding number > 0.5 (the wood meshes are not watertight). Depth = distance from an inside point to the surface
  of the body it is in. A 3 mm board gives at most 1.5 mm, so "1.5 mm deep" means "through the full thickness".
- Poses, paths, riders and wires are ports of `js/player.js` at 23:01: `mixPose`, `alongPath` with `stops`, `composePose`, `throughPoses`,
  `skinned()` with `a_ref` / `b_ref` and the new `b_from`, `sampled`, and the route blend in `drawWires` with `wire_via`. Transitions are
  sampled evenly along each beat's travel. "e" is the eased progress of a step's 0.8 s animation (the share the wire blend and a riding
  plug have done); the time it takes on screen is given where it matters.
- Camera: eye = target + dir x radius / sin(22.5 deg) x 1.08, 45 degree vertical field, 16:10 frame; "ndc" = place in the frame, -1 .. 1.
  Lead lines are drawn depth-tested (`core.js`), so a line behind a part is hidden; "seen" = share of 41 samples along a line that are in
  frame and not behind any part.
- The plug-on-pins test is live: seated, the four plugs touch nothing (their contacts are hollow); moved half a pitch sideways, plug
  NAUO84 takes the module's pins 0.76 mm deep. So "touches nothing" on the headers is real.

## Findings

Order: largest effect on screen first. "Guide" = fixable in `guide.py`; "generator" = `stepgen.py` places it; "CAD" = comes from the model.

| | Step | What | From | Mark |
|---|---|---|---|---|
| F1 | 82c, 83c | the plugged elbow / shoulder lead is dragged out of its hook slot through R5 / R6, 1.50 mm, for 0.5 s | guide | must fix |
| F2 | 78c, 79c, 81c, 61c | the claw lead is dragged through C3 beside the tongue hole and through A6 at its holes, up to 1.50 mm | guide | should fix |
| F3 | 61c, 78c, 79c | the claw plug goes 1.27 - 1.50 mm into C3 / A6 as it passes the holes | guide (kit fit) | should fix |
| F4 | 40c, 50c | the lead cuts the wood behind the hook slot's drop, 1.23 / 1.48 mm | guide | should fix |
| F5 | 81c, 82c, 83c | riding plugs glide through the joysticks' jumper wires and the base lead | guide | should fix |
| F6 | 81c | the extension cuts R4 beside the stem of the L-shaped slot, 1.50 mm | guide | should fix |
| F7 | 82, 84 | the "6" and "10" rings land on the plug of the row before, not on their row | guide | should fix |
| F8 | 37, 47 | the clamp plate's line runs from mid-window into the middle of the motor; 44% / 37% seen | generator | should fix |
| F9 | 60 | the claw motor's line starts 5.9 mm inside the motor; 54% seen | generator | should fix |
| F10 | 67, 68 | the screw line ends in mid-air 3.6 mm past C6 | generator | should fix |
| F11 | 32, 33 | two of the four lines float in notches, 4.1 and 6.3 mm from any wood | generator | should fix |
| F12 | 64 | the line stops 13 mm short of C3's slot (23.7 mm for 40 mm travel) | generator | should fix (small) |
| F13 | 78, 79 | the eye on A6's hole cannot be seen from any of the four views | generator gap | ask Lee |
| F14 | 62, 63 | one of the two lines is 37% seen from every view (the clip hides its own prong) | claw shown CAD way up | ask Lee |
| F15 | 25, 28 | travel 35.5 degrees off the view axis (rule: at least 40) | guide | ask Lee |
| F16 | 37c, 47c | R8 / R7 pass through the motor's rigid 3 mm lead stubs | CAD | ask Lee |
| F17 | 44c | the head of NAUO62 passes through R5's top edge | CAD pose | ask Lee (has a Review note) |
| F18 | 36 - 84 | wire lengths change from step to step (claw lead 55 -> 269 mm) | guide | ask Lee |

### F1. Steps 82c and 83c: the plugged lead is pulled out of its hook slot through the side plate. must fix

- 82c: the elbow lead's centre line is inside R5 beside the hook slot, **1.47 - 1.49 mm deep (the full board)**, over 3.2 mm of each wire, at
  [119.7, 164.5, 110.5] (113 mm along the lead), in 27 - 30 of 41 frames from e 0.025 to 0.95: from 18% to 77% of the time, **0.47 s of the
  0.8 s**. In frame (ndc -0.36, 0.48); the lead is the subject of the step. The lead goes into the lug and comes out again instead of
  leaving through the slot.
- 83c: the shoulder lead inside R6 the same way, **1.46 - 1.50 mm** at [119.4 - 119.9, 177.8 - 182.0, 170.7], e 0.025 - 0.975 (0.51 s), in sight
  at ndc (0.0, 0.82 - 0.87).
- Cause: the `lead['hooked']` and `lead['plugged']` routes have no `b_from`, so `skinned()` moves every point of the lead with the plug
  in proportion to how far along it is. The slot point, 46% along, follows 43% of the plug's 69 mm, 90-degree move. The base lead
  already uses `b_from=57` (routes 28 - 30); none of the arm and claw routes do.
- Fix (tested in `s43`): `b_from` on the side leads' hooked and plugged routes, e.g. in `side_lead()`
  `routes(ids, hooked, b_at=plug_hooked, b_from=through_slot_mm + 2.5, **ends)` and the same on `lead['plugged']` (116 mm elbow, 142 mm
  shoulder). With it nothing touches R5 or R6 in 82c / 83c.

### F2. Steps 78c, 79c, 81c, 61c: the claw lead is dragged through C3 and A6 while its plug is moved. should fix

| View | Part, where | Worst | Wire inside | When | On screen |
|---|---|---|---|---|---|
| 78c | C3 beside the tongue hole, [296.0, 195.1, 147.6] | 1.48 mm | 3.5 mm | e 0.03 - 0.78 (0.35 s) | in sight, ndc (-0.23, 0.19) |
| 78c | A6 at the top hole, [219.0, 211.4, 144.0] | 0.73 mm | 2.0 mm | e 0.60 - 0.78 | hidden by A5 |
| 79c | A6 at the lower hole, [184.8, 172.3, 151.2] | 1.47 mm | 10.2 mm | e 0.53 - 0.98 | hidden by A4 |
| 79c | C3 beside the tongue hole, [296.2, 194.9, 145.2] | 1.31 mm | 4.0 mm | e 0.85 - 0.95 | hidden by A5 |
| 81c | A6 at the lower hole, [191.2, 179.5, 145.4] | 1.50 mm | 13.8 mm | e 0.03 - 0.94 (0.45 s) | in frame (ndc 0.83), hidden by A4 |
| 61c | C3 at the tongue hole's edge, [297.0, 194.4, 148.0] | 0.61 mm | 2.2 mm | e 0.55 - 0.78 | in sight |

- Cause: as F1. Each in-between route (`by_way_of`) and each final route is tied to the plug's live pose, so the run of lead already
  held in the tongue hole and in A6's holes swings with the plug.
- Fix (tested in `s43`): give `claw_lead()` a held length passed on as `W.route(..., b_from=...)`: 62 mm once the lead has been fed past
  the tongue hole (routes of 64 mm or more), 149 past A6's top hole (150 or more), 210 past the lower hole (212 or more). Result: 78c
  0.05 mm, 79c 0.24 mm, 81c nothing in A6 or C3; 61c keeps 0.47 mm at the plug end, which is F3.

### F3. Steps 61c, 78c, 79c: the claw plug passes through the wood beside the holes. should fix

- 61c: plug NAUO90 **1.50 mm into C3** at [295.9, 195.1, 148.4] (17 samples over 0.5 mm), e 0.22 - 0.62 (0.13 s), in frame.
- 78c: **1.27 mm into A6** at the top hole, e 0.17 - 0.63 (0.16 s), behind A5. 79c: **1.42 mm into A6** at the lower hole, e 0.34 - 0.70 (0.11 s), behind A4.
- Cause: the plug is 7.9 x 2.75 mm; C3's tongue hole is 6.3 x 10 mm and A6's holes 8 x 8 mm. Turned as the lead's end turns it, the plug
  crosses each hole at an angle. On the video it goes through "narrow end first" and fills the A6 hole (video_claw.md 5:49 - 5:59).
- Fix: ride poses that take the plug through square to each hole, on edge through the tongue hole (7.9 mm along the 10 mm side), with
  the lead's last few mm twisted to match (`W.ribbon(..., end_across=...)`, then `W.plug_pose`). The claw author's log notes the limit.

### F4. Steps 40c and 50c: the lead cuts the wood behind the hook slot. should fix

- 40c: the elbow lead's centre line inside R5 **1.21 - 1.23 mm** over 7.5 mm at [126.3, 164.7, 110.3], e 0.875 - 0.975 (the last 0.10 s, while the
  motion slows down); in sight at ndc (0.21, 0.17). 50c: the shoulder lead inside R6 **1.19 - 1.48 mm** over up to 12.2 mm at [127.0, 158.0, 170.7], in sight.
- The point is 1.2 mm behind the back wall of the slot's drop (x 125.12, `cad_wire_paths.md` 3.3): the blend goes straight from the loose
  route to the hooked one, instead of in at the mouth, along the entry channel and down the drop. (In 40c the lead also brushes its own
  motor, 0.26 mm, e 0.52 - 0.60.)
- Fix: an in-between route in `wires_done` (a list, as `by_way_of` builds it) with the lead lying level in the entry channel (mouth on the
  lug's front edge at x 117.66, y 166.25 - 168.54; channel back to x 121.9 / 124.0), and a matching plug pose in `ride`.

### F5. Steps 81c, 82c, 83c: the riding plugs glide through other wires. should fix

- 81c: the row-10 plug NAUO85 passes through the four right-joystick jumper wires, **0.48 - 0.74 mm**, e 0.24 - 0.67 (0.14 s), in sight at ndc
  (0.40, -0.26). 82c: the elbow plug through the four left jumper wires, **0.45 - 0.49 mm**, e 0.25 - 0.45, in sight, and through the base lead's
  riser over row 5, 0.76 mm, e 0.68 - 0.73. 83c: the shoulder plug through the four right jumper wires, **0.44 - 0.48 mm**, e 0.40 - 0.60, in sight.
- Cause: the plugs glide straight to `via([0, 30, 0])`, 30 mm above the row, and the jumper wires arc up to y 154 - 157 between the joysticks
  and the shield.
- Tested (`s43`, `s43b`): with `via([0, 55, 0])` no jumper wire is touched in 82c or 83c (closest: right Y, tube 0.58 mm into the plug,
  centre outside). In 81c one `via` pose 30 mm above the row-10 plug's slot pose in its `ride=` list clears the jumpers. The elbow plug still
  crosses the base lead, which stands in the plane z 139.5 up to y 176 between row 5 and R4: 0.51 mm with a 55 mm lift, 0.72 mm with 70 mm.
  It has to rise above y 180 before it crosses that plane (a second via, over the hook), or the brush (about 0.03 s) is accepted.

### F6. Step 81c: the extension cuts R4 beside the stem of the L-shaped slot. should fix

- As the join drops behind R4, the extension's wires next to the coupler are inside R4 **1.45 - 1.50 mm** (yellow, red; brown 0.83) over
  3.0 - 3.2 mm, at [133.4, 144.6, 146.4], e 0.79 - 0.94 (0.10 s), in the middle of the frame (ndc -0.01, 0.09).
- Same mechanism as base Step 8c (review_bc F4): the blend goes diagonally from "35 mm out over R4" to "in the pocket" through the wood
  beside the stem (z 140.6 - 142.7). Fix: an in-between extension route down the stem, with matching coupler and plug poses in `ride`.
  (`b_from` does not help here: the slot is at the coupler end of the extension.)

### F7. Steps 82 and 84: the row labels point at the plug on the row before. should fix

- The anchor of "6" (the foot of row 6's V pin, 0.30 mm inside it, as "5" in Step 23) is hidden by the row-5 plug, 2.06 mm in front of it
  on the sight line; "10" by the row-9 plug, 2.02 mm in front. On screen the ring lands on the side of the neighbouring plug, one row off.
  "9" (Step 83) is clear. Raising the anchor does not help from this side: the sight line climbs only about 1.3 mm before it meets the
  neighbouring plug, which stands 14 mm tall.
- From the house view on the +z side (`look_from=[-1, 1, 1]`, azimuth 315) "6" and "9" are clear (only their own pin); "10" is then behind
  another pin of the module 5.0 mm in front, so it also needs its anchor higher on the pin.
- Fix: `look_from=[-1, 1, 1]` for the whole run 82 - 84 (rulebook 7: one camera for a wiring run) and the "10" anchor raised; or Lee's choice of side.

### F8. Steps 37 and 47: the clamp plate's line goes from the middle of the window into the motor. should fix

- One automatic line: tip [170.3, 162.2, 106.4], 6.07 mm from R8 (the middle of its 12.3 mm window), mouth [170.3, 162.2, 103.5] **5.87 mm deep
  inside the Elbow Motor**; 42 mm, **44% seen**, seat end hidden. Step 47 the same on R7: 6.13 / 5.93 mm, **37% seen**. (Step 60 below has the
  same shape of line, from `axial=True` on a motor going through a cut-out.)
- Fix: two hole-to-hole lines, `lines_at=[[[170.28, 171.6, 106.46], [170.28, 171.6, 109.0]], [[170.28, 152.95, 106.46], [170.28, 152.95, 109.0]]]`
  (Step 47: z 174.74 -> 172.2). Tips 1.40 mm from the wall of R8's hole (its centre on the inner face), mouths 1.15 mm (centre of R5's 2.3 mm
  hole on its outer face); 47.5 mm long; 90% and 39% seen from the step's camera. The upper one alone is a valid single line.

### F9. Step 60: the claw motor's line starts inside the motor. should fix

- Axial line from [335.3, 196.3, 144.1], **5.94 mm deep inside the motor**, to the middle of C3's cut-out (6.11 mm from C3); 54% seen.
- Fix: two lines at opposite corners of the case, `lines_at=[[[329.14, 196.6, 132.86], [329.14, 193.0, 132.86]], [[341.29, 196.6, 155.41], [341.29, 193.0, 155.41]]]`:
  tips 0.29 / 0.17 mm from the case, mouths 0.29 / 0.19 mm from the cut-out's edge on C3's engraved face, 51 mm long, 44% and 88% seen.

### F10. Steps 67 and 68: the screw line ends in mid-air inside the claw. should fix

- Mouth [323.0, 186.6, 147.0], **3.98 mm from C6** (3.6 mm past its top face, in the gap between C6 and C3); Step 68 3.95 mm. 49% / 73% seen.
- Cause (generator): `axial=True` averages the screw's contacts with C6 (y 179.6 - 183.1) and with C3 (y 193.1 - 195.9) into one point between them.
- Fix: `lines_at=[[[322.95, 195.85, 147.08], [322.95, 179.53, 147.08]]]` (Step 68: x 347.25, tip y 195.59, z 147.06): from the screw's point to the
  middle of the hole in C6's outer face (1.42 / 1.38 mm from its wall), 43.7 mm, 66% / 85% seen. The same averaging hits any screw that
  passes through one part into another with `axial=True`; worth a fix in `stepgen` (mouth = the first contact along the approach).

### F11. Steps 32 and 33: two of the four lines float. should fix

- The lines at [139.9, 166.5] and [162.9, 181.4] (z 123.6 / 120.6) are **4.06 and 6.29 mm from any wood at both ends**: winding number 0 and no
  surface along z through A1, A2 or A3 there; the points lie in bays of the plates' outline (the notches). The other two lines are on the
  plates (0.05 / 1.38 mm). All four are 65 mm and 0.0 degrees off the travel.
- Cause (generator): the face-on contact gives anchors that fall outside the material. Fix: `lines_at` with the two good points
  ([171.7, 163.9, 123.6] and [191.3, 155.0, 123.6]; Step 33 at z 120.6), or move the other two onto the rims of the notches.

### F12. Step 64: the line stops short of C3. should fix (small)

- Mouth [317.1, 180.1, 131.1] at C2's lower end (1.55 mm), 13 mm short of C3's engraved face: 23.7 mm for 40 mm travel; 73% seen.
- Fix: `lines_to=[C3]`, or `lines_at=[[[317.1, 196.4, 131.1], [317.1, 193.03, 131.1]]]`: mouth in C3's square slot (1.50 mm), 36.6 mm, 54% seen.

### F13. Steps 78 and 79: the eye on A6's hole is hidden from every view. ask Lee

- The eye anchors (top hole [221.6, 215.4, 144.5], lower hole [185.6, 175.5, 144.5], each in the middle of its 8 mm hole) are behind A5
  (27 mm in front) and A4 (31 mm in front). **From all four three-quarter views they are hidden**: the holes sit between A7, A8 and the
  forearm strips, so `look_from` cannot help. The claw lead itself is 48 - 73% in sight in Step 78 and 25 - 47% in Step 79 (the current view is the best).
- Options: the eye on a visible stretch of the lead next to the hole; a view from higher than 35 degrees (not offered by `choose_view`);
  or a framed close-up (not in the player yet, rulebook 14).

### F14. Steps 62 and 63: one of the two clip lines is behind the clip. ask Lee

- The line from the near prong of C1 / C2 up into C3 is 37% seen (the clip itself hides 26 of 41 samples), and 37 - 39% from each of the
  four views; the other line is 95%. The clip arrives from below with the camera above, because the claw is shown the CAD way up.
- This follows from not turning the claw over (rulebook 13, "A part that goes on underneath"; section 14).

### F15. Steps 25 and 28: the A9 travels almost towards the camera. ask Lee

- Travel along A6's normal is **35.5 degrees** off the view axis (rulebook 7: at least 40). From azimuth 45 (`look_from=[1, 1, 1]`) it is 87.4
  degrees and the line 90% (Step 25) / 73% (Step 28) seen, but A6 is then seen from its plain side, nearly edge-on.
- The line, set by hand to follow the stem's tip, ends 2.3 mm beyond A6's plain face (3.1 mm from any wood), as `guide.py` intends. Now
  that `stepgen` has `look_from`, the hand-set line is no longer needed to steer the camera; the automatic one would end in the slot.

### F16. Steps 37c and 47c: the clamp plates pass through the motor's lead stubs. ask Lee (CAD)

- R8 overlaps the Elbow Motor's stubs **1.50 mm** at [182.4 - 184.6, 160.8 - 163.8, 92.4 - 93.3] (one frame, 72% of the travel; seated pair 0.09 mm),
  and the drawn lead's first 3 mm 1.39 mm deep (e 0.53 - 0.73, 0.07 s). R7 the same on the Shoulder Motor. Hidden behind the motor from the camera.
- Cause (CAD): the stubs are rigid and reach x 184.6, 2.7 mm past the end of the plate's window (x 181.9); R8's 1 x 8 mm notch is at the
  other end (`cad_arm_claw.md` 10). The real lead bends into the notch. Nothing shows on screen.

### F17. Step 44c: the lever-top screw passes through R5's top edge. ask Lee (already flagged)

- The head of NAUO62 is inside R5 **1.50 mm** (full thickness) at [141.3 - 145.7, 173.6 - 175.4, 109.0 - 111.3] from 67% to 88% of its travel. The CAD
  has the lever where this hole is 0.9 mm above R5, and the step's Review note says so; the guide cannot show the lever swung up.

### F18. Wire lengths change between steps. ask Lee

- Claw lead: 55 mm (Steps 60 - 61), 87 - 89 (61c - 78), 173 - 179 (78c - 79), 267 - 271 (79c - 81), 263 - 269 (81c on; CAD 269 to the join).
  Elbow 68 -> 137 -> 242 - 245 mm (CAD 243); shoulder 68 -> 160 - 165 -> 273 - 282 (CAD 278); extension 35 -> 30 -> 140 - 143 (CAD 149).
- Inside a step the wire grows out of its tip: 82c 137 -> 245 mm, 84c 30 -> 143 mm. Same question as review_bc F9.

## Right as it is

**1. Poses**
- CAD seated, all 101 parts: 84 pairs touch. Only R2 x Base Motor is over 0.5 mm (0.56, base). Arm and claw: screw threads 0.35 - 0.38 mm,
  screws under their heads 0.10 - 0.14, horn push fits 0.20 (A2 / A3 x elbow horn) and 0.35 (C7 x claw horn), shafts in horns 0.23, tab fits
  0.05 - 0.20, R7 / R8 x servo label 0.09. All the CAD's.
- Every hover, riding and seated pose of the 119 views from Step 24: **no posed pair over 0.05 mm**.
- Hand-set paths: 35c lever (upright, down, across, swung; 102 frames) touches nothing; 36c elbow motor worst 0.42 mm (horn x R5) and 0.37
  (case x R5); 46c shoulder motor worst 0.43 (horn x R6); 40c, 50c, 80c, 81c (join back over R4 and down) and the plugs in 82c - 84c touch no
  part, header pins included.
- Straight paths: 30c upper arm, 43c A4 + A5, 55c triangle, 74c claw slide (99.6 mm) touch nothing; every screw ends at 0.20 - 0.38 mm (threads);
  70c: C9 over the barbs of C1 / C2, 1.18 / 1.23 mm in the last 4% of travel only (the CAD's 1.1 mm snap barbs).

**2. Lead lines**
- Every straight line is 0.0 - 0.1 degrees off its leg; the turned paths (35, 36, 46) have one line from the hover pose, 3.1, 0.1 and 0.5 degrees
  off the first leg.
- Tips and mouths within 1.5 mm of the right part, and at least 71% seen, in Steps 24, 26, 27, 29, 30, 34, 36, 38, 39, 41 - 45, 48, 49, 51 - 54,
  56 - 58, 71, 72, 74 - 77. Also right, with an end in an opening: 65 (one mouth 1.59 mm under the motor's ear, which C5 props), 66 (tip 2.95 mm,
  the middle of C6's 6 mm square slot that takes C2 and C4 together), 69 (tip 2.30 mm in C7's horn pocket); 70 is anchored but one line is 61% seen.
  Step 31's mouth (2.4 mm into R5's opening) and Step 55's two (2.0 / 2.5 mm past R6 / A8) are hand-set ends at the seat, as intended.
  Step 35's line (59% seen) starts in A1's own hole, behind A2 and A3.

**3. Wires**
- In every view from Step 24, no wire's centre line is inside any part other than its own; the only contact is the base lead grazing R4
  (0.34 mm, known).
- Ends, worst over all views: lead to servo stub 0.106 mm; lead to plug contact 0.115 mm, the right contact every time (brown G, red V,
  orange / yellow S); every lead meets its plug within 7.7 degrees of its axis. Claw brown meets extension brown across the coupler (G at z 142.12 on both plugs).
- 84c (the extension onto row 10) and every animation not named in F1 - F6 are clean; 36c, 46c, 60c and 74c carry their leads rigidly.

**4. Labels and eyes**
- All 60 anchors (53 labels, 7 eyes) are on their own, visible part (part labels 0.00 - 0.07 mm; row labels 0.28 - 0.30 mm inside the foot of
  their pin, the Step 23 convention; eyes at the middle of their slot or hole, 1.12 - 3.99 mm) and in frame (worst ndc 0.60). Hidden: F7 and
  F13 only (four screw labels sit on the far side of their own screw; the ring still lands on the screw).

**5. Framing**
- Hover views: moving parts, riders and lead lines in frame (worst ndc 0.87, Step 51). In every animation the moving parts stay in frame (worst
  0.87), and so do moving wires except where the step frames a close-up: 81c (the claw lead 65 - 73% outside the frame on R4) and 83c (34 - 36% of
  the shoulder lead outside). The plug, the slot and the join are always inside.
- Travel against the view axis 54.5 - 59.2 degrees in every hover view except F15 (every leg of the hand-set paths 54.6 - 79.7); plug steps
  82 - 84: 74.5 - 83.7 degrees, every leg 55 - 89.

Not checked: the glide-in of a newly shown part from 1.8 x its hover offset (it comes along the same line, from further out).
