# Review: MRA guide Steps 24 to 85 (arm, claw, final wiring) against the videos and the CAD reports

Reviewer: video / CAD check, 13 Oct 2026. Review only: nothing in the project was changed apart from this file. The CAD was not
loaded, no generator was run and no browser was used. Read: `guide.py` (whole), `steps.json` (every view from Step 24 on; scripts and
dumps in the session scratchpad under `review_ac/video_cad/`), `authoring/brief.md`, `arm_log.md`, `claw_log.md`, `lee_notes_2026-10-13.md`,
`video_arm.md`, `video_claw.md` (and the `_seg` files where a detail mattered), `cad_arm_claw.md`, `cad_codes_base.md`, `cad_wire_paths.md`,
`cad_pins.md`, `cadasio_mra_project.md` section 3, and rulebook sections 1 to 10, 13 and 14.

Grades: **must fix** = wrong, or a student following the guide would get it wrong or get stuck. **should fix** = clearly better.
**ask Lee** = a choice that is Lee's. What I say about what the camera shows comes from the camera direction in `steps.json` against
each part's engraved-face normal (`cad_codes_base.md` table 1); I did not look at the pictures.

## Summary

Part identities, screw lengths, screw directions and the order are right throughout, and every lead goes through the right slots and
holes and lands brown-on-G on the right row. One must fix: Step 44. Its caption does not tell the student to swing A1 - A3 up before
putting in the lever-top screw. In the pose shown the screw cannot go in, and a student would get stuck there. The rest are caption
hints that the video supports (Steps 31, 46, 60, 71, 83), two camera problems (Steps 24 - 26 and 30; Step 78) and questions for Lee.

## Findings

### 1. Step 44 (NAUO62, lever-top screw): must fix

- **Problem.** The caption is "Screw A1 - A3 to A4 with a 10mm screw through the large hole in A3." In the CAD pose the guide shows,
  the screw cannot get in: its head hits the top edge of R5. On video the builder swings the lever upright first. A student following
  the caption and the picture gets stuck. The Review note says this to the reviewer, but the student is never told.
- **Evidence.** The hole's axis is at y 176.3 and R5's top edge at y 175.38 (`cad_arm_claw.md` 7.7 and 10). The head (5.5 mm across)
  spans y 173.55 - 179.05, so it overlaps the edge by 1.8 mm. It is partly hidden behind R5 even when seated: "5 of 12 rim rays" are
  blocked (`cad_arm_claw.md` section 3). `video_arm_seg2.md` item 14 has "Lever swung up by hand" at 5:50 - 5:59, and its point 7
  says "a driver from the R5 side fouls R5. The builder swings the lever upright first". In the video the screw is pushed through
  the raised lever (6:06 - 6:07), then A4 is hung on its tip (6:08 - 6:09) and the screw is driven (6:12 - 6:38). Only after that is
  A5 folded up onto A7 (6:39 - 6:49).
- **Fix.** Change the caption so that it carries the hand action. Step 43: "Swing A1 - A3 up until its free end stands clear above R5,
  and hold the coded end of A4 against the inner face of A1 there." Step 44: keep it as it is. Step 45: "Swing A5 up against the
  outside of A7 and screw them together with a 6mm screw through the second hole of A5." Keep the Review note on Step 44, because
  the picture still cannot show the raised lever (arm_log gap 3).

### 2. Step 31 (NAUO55, shoulder pivot): should fix

- **Problem.** "Screw A7 to R2 with a 6mm screw." This is the shoulder bearing. If a student drives it hard and clamps A7 to R2, they
  only find out at the Step 59 check. By then the screw cannot be reached: the elbow motor and its horn sit on the same axis. Freeing
  it means taking off R8's two screws, R8, the elbow motor and the lever.
- **Evidence.** `cad_arm_claw.md` section 3 lists it as a pivot. Its driver-access note says "NAUO55 is hidden behind horn NAUO59 and
  servo NAUO58", and 7.7 says the screw must go in before the lever and the motor. Video 2:37 - 2:39: hands off, and the frame, held
  only by this screw, swings forward. So "it still swings" is what the video shows. It is not invented tightening advice.
- **Fix.** "Screw A7 to R2 with a 6mm screw. Reach it through the opening in R5. A7 must still swing." The brief's rule against
  inventing tightening advice stays: the video shows only the check.

### 3. Step 46 (Shoulder Motor): should fix, and ask Lee about turning horns by hand

- **Problem.** "...push it in so the horn sits in the slot in A8." Until this step the upper arm hangs on the one -Z pivot. On the real
  kit the arm swings down onto the front end wall, so A8's slot is not where the horn is. On video the builder raises the arm and
  turns the horn by hand to match it. The guide shows the arm fixed at the CAD's 47.9 degrees, so a student is not told to do either.
- **Evidence.** `video_arm.md` timeline items 9 and 31 - 33. 2:37 - 2:39: the arm comes to rest on the front end wall. 7:10 - 7:18:
  "The upper arm is now raised (30 to 60 degrees)". 7:22 - 7:23: "the left fingers turn the horn". `video_arm_seg3.md` row 13: the
  horn is set "so that it points the way the raised upper arm points". 7:28: "Left hand steadies the turret and the raised upper arm".
  Section 5, item 13.
- **Fix.** Add "Hold the arm up so that the slot in A8 lines up with the opening in R6." For Lee: should students also turn the horn
  by hand to meet the slot? That back-drives an unpowered servo. The same question comes up at Step 44 (the lever, through the elbow
  motor's horn) and Step 73 (the jaws).

### 4. Steps 24 - 26 and 30: should fix

- **Problem.** These steps are seen from the +Z side (camera dir [-0.58, 0.57, +0.58]). A7 is engraved on its -Z face, so the student
  sees A7's blank face. Yet the Step 24 caption orients A7 by its code ("The code on A7 faces out, with its A at the same end as the
  A6 code"). Getting A7 end for end matters. Its shoulder hole is 2.8 mm (free, so the shoulder can pivot). Its elbow hole is 2.3 mm,
  which NAUO63 threads into. Reversed, the shoulder screw would bind in A7 and the elbow screw would have nothing to bite on. In Step
  26 the screw goes into A7's hole on the far, hidden face. Step 30's caption names "the engraved side of R2", which is also on -Z,
  away from the camera.
- **Evidence.** Engraved normals from `cad_codes_base.md`: NAUO23 (A7) -Z, NAUO11 (R2) -Z. Cameras from `steps.json`: Steps 24, 25, 26
  and 30 all use [-0.5792, 0.5736, 0.5792]. A6's engraved face would still be in view from -Z: its dot product with [-0.58, 0.57, -0.58]
  is 0.81. Hole sizes: `cad_arm_claw.md` section 9.
- **Fix.** Use the -Z view for Steps 24 - 26, for example by nudging the camera with `lines_at`, as was done for Step 31. Better, add
  a per-step camera to the generator (arm_log gap 2). Steps 27 - 29 stay on +Z. For Step 30 the caption could say "A7 goes against
  the R5 side of R2".

### 5. Step 78 (claw wire through the top hole of A6): should fix

- **Problem.** From this step's camera the top hole is hidden behind forearm strip A5. The eye icon's leader ends on A5, not on the
  hole the caption names.
- **Evidence.** Hole centre (222.76, 214.43, 144.49), from `cad_wire_paths.md` 3.5. Camera dir [-0.58, 0.57, -0.58]. The line of sight
  from the hole crosses A5's layer (z 123.55 - 126.55) at about (203.3, 233.7). A5's centre line runs Q (197.05, 235.70) to E
  (228.94, 221.29), and at x 203.3 it is at y 232.9: inside the 10 mm strip. `claw_log.md` gap 2 says the same thing. The bottom hole
  in Step 79 is clear from its camera (I checked the same way against A7, A4, the lever, R2 and R5).
- **Fix.** Use a camera from above the arm, or a framed close-up, for this one step. It needs the per-step camera the generator lacks.

### 6. Step 71 (jaw C8): should fix

- **Problem.** "Slide C8 in ... until its teeth mesh with C7." The caption does not say the jaws must be closed while C8 meshes. If C8
  goes in a tooth off, the jaws will not meet tip to tip.
- **Evidence.** `video_claw_seg2.md`. At 2:26 the trial fit has "both jaws closed so the two half-round bites make one round hole".
  At 2:52 - 2:54: "Both jaws end closed, tips together".
- **Fix.** "Slide C8 in between C6 and C9, code facing C9, with both jaws closed, until its teeth mesh with C7."

### 7. Step 60 (Claw Motor into C3): should fix

- **Problem.** The caption does not say which way round the motor goes. The case (22.6 x 12.15) fits C3's cut-out (23.2 x 12.3)
  either way. A motor turned round puts the shaft at the wrong end, and C6's keyhole will not then go over the horn (Step 66). By then
  the bars C4 and C5 already trap the motor's tabs, so the claw has to be taken apart.
- **Evidence.** Video 0:11 - 0:16: "The shaft is at the near (-Z) end of the cut-out, the end with the single big square slot beside
  it". The lead leaves at the shaft end (`cad_arm_claw.md` section 2), and C3's notch is at that end (section 9, NAUO34).
- **Fix.** "...from the engraved side, wire first, with the wire at the notched end of the cut-out (next to the square slot)."

### 8. Step 83 (row 9): should fix (minor)

- **Problem.** "Reconnect the shoulder motor to 9." It drops the colour reminder that Steps 23 and 82 carry, and a plug the wrong way
  round is the likeliest slip.
- **Fix.** Add "Remember brown to G, red to V, and orange to S." The drawn plug is right: brown at x 49.98 on G.

### 9. Steps 82 - 83 (plugging 6 and 9 at the very end): ask Lee

- **Problem.** The guide breaks Lee's servo rule but does not say it is breaking a rule. Rulebook 13 says a lead "is plugged in at
  the end of its section". On video, 6 and 9 were plugged in between Arm.mov and Claw.mov. The guide instead leaves both plugs
  hanging past their hooks through the 25 claw steps. When the Full Build is cut into Parts, the arm Part would end with two leads
  loose. The Step 82 Review note gives the reason ("one wiring run in the order of the rows"). `claw_log.md` adds a drawing reason:
  the plugged-in arcs cross where the join is drawn above R4.
- **Evidence.** Rulebook section 13, Servos row. Rulebook section 3: "Finish one module completely (mount, then every wire)".
  `video_claw.md` section 1: three plugs are already in at 0:00. Either order is safe for a student: the hanging plugs sit about 22 mm
  in front of the side plates' front lugs, clear of the claw work.
- **Fix (if Lee keeps his rule).** Move Steps 82 - 83 to just after Step 58, before the swing-check card. Move ABOVE_R4 and the loose
  extension clear of the side leads' plugged arcs. The Step 84 wiring run would then be row 10 only.

### 10. Steps 60 - 72 (claw built the CAD way up): ask Lee

- **Problem.** Nine parts arrive from underneath. C3, C6, C7, C8 and C9 are engraved on the faces that look down, and every claw
  camera looks from above (dir y +0.57). So none of those codes is ever seen. Yet the captions orient them by code: Step 60 "from the
  engraved side", 64 "from the engraved side of C3", 66 "code facing away from C3", 69 "code facing away from C6", 70 "code facing
  out", 71 "code facing C9". C2's and C4's codes (-Z) are also turned away from the +Z cameras in Steps 63 - 65. Lee's decision for
  B1 (rulebook 13, which names "parts of the claw under C3") allows this, but over 13 steps it removes the student's main check.
- **Evidence.** `cad_codes_base.md` table 1, against the cameras in `steps.json`. Video: the claw is built engraved faces up and
  turned over at 3:42.
- **Fix (for Lee to choose).** Either keep the CAD way up with the Step 60 Review note, or give the generator a way to show a staged
  sub-assembly turned over (rulebook sections 7 and 14), which matches the video.

### 11. Close-ups (focus) on whole parts and on every single screw: ask Lee

- **What the guide does.** Lee's decided exception (rulebook 13) covers punching in on the first fastener of a set and on a wire going
  into a slot or onto a pin. The new sections also zoom in on whole parts: the lever (Step 35), both motors (36, 46), both clamp plates
  (37, 47), A4 + A5 (43), the triangle (55), A13 (57) and the claw seat (74). They also zoom in on every single screw on the model.
  `arm_log.md` gives a reason: at whole-model scale these could not be made out. The rule break is not flagged to Lee anywhere.
- **Fix.** Ask Lee whether to widen the exception to "small parts and single screws on a large model".

### 12. T1 / T2 block (NAUO41 - 44): ask Lee

- **Problem.** The guide leaves this block out. It is in the CAD and in TechBox's Cadasio project (`cad_codes_base.md` section 2) but
  in no video. If it is the object for the claw to pick up, it needs three steps of its own.

### 13. Already flagged by Review notes; I agree with them

- Step 46: the 9 on the flag (rows agree with the CAD).
- Step 73: should students turn the unpowered jaws by hand?
- Step 80: the join is made level above R4.
- Step 84: the extension is drawn brown / red / yellow as on video, against orange in TechBox's Cadasio project.

## The authors' departures from the video, judged

| departure | safe for a student? |
|---|---|
| A4 + A5 joined after R8 (video: before the lever) | yes: bench work, nothing waits on it |
| triangle built after the Shoulder Motor (video: before) | yes: built off the kit |
| A4 placed before NAUO62 (video: screw first, A4 on its tip) | the order is fine; the missing "swing A1 - A3 up" is not (finding 1) |
| hook steps 40 and 50 straight after each clamp plate (not on video) | yes: the hook mouths are uncovered (`cad_wire_paths.md` 3.3), and later screws and drivers pass the hooked leads 11.8 mm (NAUO70) and 12.9 mm (NAUO62) away (measured on the routes in `steps.json`). The end of Claw.mov shows both leads in their hooks |
| no tightening advice, one swing check at the end | yes, except NAUO55 (finding 2) |
| claw clips early, C9 before C8 (= video, not the CAD's order) | yes: tested free; the CAD's "jaws before C9" is beaten by the sideways slide |
| claw shown the CAD way up | mechanically yes; codes hidden (finding 10) |
| claw slid into the fork (video: offered to A12 / A13, swung on the first screw, A5 swung down last) | yes: same end state, and the screws keep the video's order |
| join held level above R4 and laid level inside the turret (video: in the air, then upright behind R4) | yes; Review note on Step 80 |
| extension: slot before plug (video: plug, then slot) | yes; it follows the base motor and Lee's rule |
| rows 6 and 9 at the end (video: before Claw.mov) | yes, but it breaks Lee's rule (finding 9) |
| T1 / T2 left out | ask Lee (finding 12) |

## Checked and right

- **Part ids.** Every step moves the right part. The engraved codes follow `cad_codes_base.md`: A1 - A13 = NAUO18, 19, 20, 21, 22, 29,
  23, 24, 30/31, 26, 25, 27, 28; C1 - C9 = NAUO32, 33, 34, 36, 37, 35, 39, 38, 40; R5 = NAUO15, R6 = NAUO14, R7 = NAUO16, R8 = NAUO17.
  The motors are Elbow NAUO58 in R5 (-Z, flag 6) and Shoulder NAUO66 in R6 (+Z).
- **Screws.** All 23 match the CAD in length, in the joint they make and in the side their head is on (`cad_arm_claw.md` section 3):
  - 16mm: Steps 26, 29, 67, 68.
  - 6mm: Steps 31, 42, 45, 52, 54, 56, 75, 76, 77.
  - 10mm: Steps 34, 38, 39, 44, 48, 49, 58, 72.
  - Each `direction=` points from the hole to the head side. The R8 / R7 screws go upper first, then lower, as on video.
- **Order.** Steps 24 - 58 follow the video's real order (`video_arm.md` section 0), apart from the two bench groups moved as listed
  above. Steps 60 - 77 follow `video_claw.md` section 2 action for action. Every order the CAD forces is kept
  (`cad_arm_claw.md` 7.7): NAUO55 before the lever and the motor, NAUO56 before the lever goes in, motor before plate before screws,
  NAUO74 / 75 before C9.
- **Motion.** Hover sides and distances are sound:
  - A7 and A8 face-on; the A9 nuts along A6's normal from its engraved side.
  - The lever upright, down, 3.2 mm across, then swung; the motors horn first.
  - R8 / R7 45 mm along the motor axis; A4 + A5 and the triangle from above.
  - The claw clips along the claw normal, the bars and plates from below, C8 from +Z, the claw +X 99.6 mm.
- **Captions.** They use engraved codes and the house wording ("Begin the claw with C3.", "Add the second 10mm screw.", "Reconnect
  ... to 6. Remember brown to G ..."). The face-out and end-for-end cues for A7, A8, A11, A12 and A13 and for the lever stack match
  the video.
- **Names.** Hover names match the Cadasio tooltips: horns under their motor, plugs under their motor, coupler / NAUO92 / NAUO85 as
  "Servo Extension Wire", and 6 / 10 / 16mm Hex Screw on the right ids. The parts list is consistent.
- **Wiring.** Every lead goes through the right features:

  | lead | feature | gap to the CAD crossing point |
  |---|---|---|
  | elbow | R5 hook | 0.07 mm |
  | shoulder | R6 hook | 0.43 mm |
  | claw | C3 tongue hole | 0.28 mm |
  | claw | A6 top hole | 0.35 mm |
  | claw | A6 bottom hole | 0.10 mm |
  | extension | R4 pocket | 0.35 mm |
  | base | R4 pocket | 0.22 mm |

  - The state sequence follows Lee's rule (loose, then into the slot, then plugged), apart from finding 9.
  - Brown meets brown in the coupler (z 142.12 on both sides).
  - Brown lands on G (x 49.98 - 49.99) on rows 6, 9 and 10, at z 142.11, 151.91 and 154.75. The labels "6", "9" and "10" are anchored
    at z 142.0, 152.0 and 154.6, against `cad_pins.md`'s 142.00, 152.01 and 154.55.
- **Pairs and cameras.** Every step has its `c` view, and the camera stays fixed inside each pair.
