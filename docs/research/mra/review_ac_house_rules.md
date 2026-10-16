# Review: Steps 24 to 85 (arm, claw, final wiring) against the house rules and Lee's notes

Review only; nothing in the project was changed. Read from `steps.json` (snapshot of 23:41:57, 168 views; the copy rewritten at 23:43
has the same content) and `guide.py` (the only change since the snapshot is `PART_VIEWS`, which does not touch the steps). Rules:
`docs/cadasio-patterns.md` sections 1 to 7, 9, 10 and 13. Lee's points: `lee_notes_2026-10-13.md` 4, 5, 7, 11, 12, 14, 16, 20.
Evidence from the two authoring logs and the merged video reports. No browser was used and the CAD was not loaded, so anything
about what can be seen on screen is quoted from the authors' logs, not checked. Per-step numbers came from a script over
`steps.json` (scratch: `.../scratchpad/review_ac/house_rules/dump.py`).

Severity: **must fix** = wrong, or would mislead a student; **should fix** = clearly better; **ask Lee** = a choice that is Lee's.

## Findings

### 1. Step 44: the caption leaves out the move that makes the screw possible (must fix)
- **Problem.** The guide shows A1 - A3 down (CAD pose) and the 10mm screw going in from outside R5. In that pose the hole is 0.9 mm
  above R5's top edge and the screw head passes 1.8 mm through that edge on its way in. On the video the lever is first swung
  upright by hand so that the hole stands clear of R5. Then the screw is pushed through the lever and A4 is hung on its tip
  (`video_arm.md` actions 21 and 22, 5:50-6:11). A student who copies the picture cannot get the screw or the driver past R5.
- **Evidence.** The step's own Review note; `video_arm.md` section 4 row 20 and section 5 item 14.
- **Fix.** Put the move in the caption, for example "Swing A1 - A3 up until the large hole in A3 is clear of R5, then screw A1 - A3
  to A4 with a 10mm screw through that hole." (121 characters). The model still cannot show the second pose (arm log, gap 3).
  Reword the Review note as a question (see finding 4).

### 2. Step 78: the eye points at a hole that the camera cannot see (should fix)
- **Problem.** The camera is the house view from -X -Z (dir [-0.579, 0.574, -0.579], r 68). The claw log, gap 2, says "the top
  hole of A6 is behind A5 from there", and that the lead's run between the forearm strips is mostly hidden. So the eye's ring
  falls on A5, not on the hole.
- **Evidence.** `claw_log.md`, gaps 2 and 3. Both authors also wrote that there is no per-step camera, but `stepgen.place()` and
  `seat()` now take `look_from=` (`tools/stepgen.py` lines 485-488, edited 23:02).
- **Fix.** Add `look_from=` to Step 78 (try the +Z side, `[-1, 1, 1]`) and check in the player that the hole and the lead
  entering it can be seen. If neither diagonal view shows the hole, put the eye on the lead just before the hole. Also look at
  Step 79 from the same side.

### 3. Steps 35 and 36: captions too long for a small embed (should fix)
- **Problem.** Step 35 is 176 characters and Step 36 is 161. Step 46 (157) and Step 24 (122) are next. Steps 1 to 23 have a median
  of 35 characters and a maximum of 123; Steps 24 to 85 have a median of 67. Most of the extra length is orientation information
  ("code facing out") that the student needs, so it is the three long motion captions that should be cut.
- **Fix.**
  - 35: "Slide A1 - A3 down between R5 and A7, slotted end first and A3 facing R5, onto the screw head in A7. Swing it towards the controller."
  - 36: "The elbow motor has 6 on its wire. Angle its servo horn through the opening in R5, then push the motor in so the horn sits in the slot in A2 and A3." (148)
  - 46: the same pattern (144).

### 4. The Review notes are statements, not questions (should fix)
- **Problem.** All eight notes in Steps 24 to 85 end with a full stop: Steps 44, 46, 60, 73, 80, 82, 84 and 85. Four of them run
  to 228-306 characters. Most of the Steps 1 to 23 notes end with a question Lee can answer (2, 10, 17, 20). The notes are on the
  right steps. Step 73's "Confirm that students should do this." can already be answered yes or no and can stay. Suggested
  rewordings:
  - **44:** "The guide cannot show A1 - A3 swung up (video 5:50-6:11). Is the caption enough?"
  - **46:** "Is the shoulder motor's flag 9 on the real kit? (Arm video 7:50: fairly sure. Claw video: not readable. CAD: row 9.)"
  - **60:** see finding 6.
  - **80:** "On video the join is made in the air and ends upright just behind R4 (6:30-6:57); here it ends lying level inside the
    turret, where the CAD has it. Is the CAD place right?"
  - **82:** see finding 5.
  - **84:** "Draw the servo extension wire brown / red / yellow (the real one, video 5:44) or brown / red / orange (TechBox's Cadasio project)?"
  - **85:** delete it. Lee already answered in point 19 (the USB cable comes in a later revision). Write "Nano" with a capital N in
    the card.
- **Missing note, Step 74.** On video the claw is offered to A12 and A13 alone, turned on the first screw, and A5 is swung down to
  it afterwards (`video_claw.md` actions 21-26, 3:42-5:09). Here it slides straight in between the strips (+X, 99.6 mm). Add: "On
  video the claw goes onto A12 and A13 first and A5 is swung down to it; here it slides in between them. Is sliding in right for
  students?"

### 5. Steps 82 and 83: elbow and shoulder plugged in after the claw, not at the end of the arm (ask Lee)
- **Problem.** The Servos decision in section 13 says a servo "is plugged in at the end of its section". Section 3 says to finish
  one module completely before starting the next. On video, 6 and 9 are already plugged in when the claw starts (`video_arm.md`
  "Leads"; `video_claw.md` section 1). The arm research proposed both plug steps at the end of the arm. The claw author moved them
  to the end of the claw, because the plugged-in leads "arc over the shield right where the join is made" and because the authoring
  task asked for one final wiring run.
- **Recommendation.** Follow the decision: plug 6 and 9 after Step 58 and before the arm's check card. If the plugged-in leads then
  get in the way of the join in Step 80, park the join elsewhere rather than moving the plugs. If Lee prefers one run at the end,
  add that as a new convention in section 13.

### 6. Steps 60, 64-70, 72: the claw is built from below, and its codes are face down (ask Lee)
- **Problem.** The guide builds the claw the way up the CAD has it. Nine hover poses are below the seat: Steps 60 (-55 mm in y), 64
  (-40), 65 (-40), 66 (-65), 67 (-60), 68 (-60), 69 (-65), 70 (-65) and 72 (-60). Section 4 says a hovering part is never below its
  seat; section 7 says underside work is shown with the kit turned over. The engraved faces of C3, C6, C7, C8 and C9 point down, and
  every camera is 35 degrees above the horizon, so none of those codes is seen. Captions such as "code facing away from C3" describe
  faces the picture does not show. On video the claw is built engraved faces up and turned over at 3:42 (`video_claw.md` section 0,
  item 1).
- **Justified?** It is a known player gap (rulebook section 14: "Turning the kit over: not yet"; claw log, gap 1). The captions avoid
  "up" and "down", which helps. The claw research left the choice to Lee (`video_claw.md` section 5, item 1).
- **Fix.** Reword the Step 60 note as a question: "Keep the claw the CAD way up (nine parts from below, codes face down), or add a
  turned-over view for sub-assemblies first so that it is built engraved faces up as on video?" I recommend the turned-over view:
  it is what the rulebook asks for, and it is the only way to show the codes.

### 7. Close-ups on parts that are not a first fastener or a wire (ask Lee)
- **Problem.** Section 7 and the section 13 decision allow a close-up in context only for the first fastener of a set and for a
  wire going into a slot or onto a pin. The arm and claw also punch in on motors, plates and sub-assemblies. The whole scene frames
  at r 175 (Step 30) to r 231 (Completed View). The close-ups are:
  - Step 35, lever: r 96.5
  - Step 36, elbow motor: r 83.6
  - Step 37, R8: r 72.5
  - Step 43, A4 + A5: r 121
  - Step 46, shoulder motor: r 86.2
  - Step 47, R7: r 86.2
  - Step 57, A13: r 93.8
  - Steps 55 (r 152.6) and 74 (r 156.9) are only slightly closer than the whole scene.
- **Justified?** Probably. These parts go deep inside the turret, the arm log says "at whole-model scale none of these could be
  made out", and each frame still holds the whole action (hover pose and seat). But it is a break of a rule Lee has ruled on.
- **Fix.** Ask Lee. If he accepts, add it to section 13 as a third exception, for example "a part fitted inside the turret or the
  arm is framed on the action".

### 8. Steps 39 and 49: the second clamp screw is also a close-up, with no pull-back (ask Lee)
- **Problem.** Lee's rule in point 4, point 12 and section 13 is first screw close up, then pull back for the rest. For the clamp
  plates' two-screw joints, Step 38 and Step 39 are both at r 73.4 (only the target moves to the second hole), and likewise Steps 48
  and 49. The authoring brief allowed this ("One or two screws: each its own ordinary step, a close-up is fine"), but Lee's
  decision does not cover pairs.
- **Fix.** Ask Lee whether a pair follows his rule (Step 39 / 49 pulls back to the turret, as Step 12 does for the base) or stays
  close. Steps 67 and 68 (C6) are in the isolated claw view, so the question does not arise there.

### 9. Smaller caption points (should fix)
- **Mixed wording for screws.** Steps 42, 52 and 54 say "Join them with a 6mm screw through A5 / A11 / A12". Every other screw
  step, and Step 11, uses "Screw X to Y". Use "Screw A5 to A4 with a 6mm screw." and the same for A11 and A12 on A10.
- **Step 56.** Reword as "Screw R6 to A11 with a 6mm screw, through the hole in the lobe from outside R6."
- **Step 58.** Reword as "Screw A13 and A10 to A8 with a 10mm screw."
- **Step 84.** It drops the word "Remember" that Steps 23 and 82 use. Reword as "Connect the servo extension wire to 10. Remember
  brown to G, red to V, and yellow to S."

### 10. Labels in close-ups can land on the model (should fix, player)
- **Problem.** In a close-up there is no white space, so the player puts labels and eyes 90 px from the target. The claw log, gap
  3, reports "10" sitting over the R4 code in Step 84, and labels under the caption. Section 6 says a label is never placed over the
  model and never in the bottom third of the view.
- **Evidence.** From the log; not checked here.
- **Fix.** In `layoutCallouts` (`js/player.js`), when no side has room, keep the label out of the caption band and off the target
  part's bounding box. Check Steps 82-84 and 40 / 50 afterwards.

### 11. Rule breaks that are justified (no change)
- **Steps 25 and 28: camera 35 degrees from the travel** (rule: at least 40). The A9 goes in along A6's normal. The other diagonal
  view is 87 degrees off the travel but sees A6 exactly edge-on (dot 0.045), so the slot would be invisible. The arm log steered to
  this view on purpose.
- **Steps 75-77: three identical 6mm screws, one by one.** Three different holes in two clips, from two sides; Step 77 needs the
  camera on the other side, and the video drives them one at a time with the robot turned round (`video_claw.md` 4.2). "Per joint"
  in section 13 is met.
- **Steps 41-43 and 51-55: built later than on video.** On video A4 + A5 and the triangle are built earlier. Here each is built
  immediately before it is fitted, which is section 3's rule for preparation.
- **Step 35: a three-stage path in one step.** This is allowed by the section 13 decision on motions that are not a straight push.
- **Steps 37 and 47: R8 and R7 hover 45 mm, not 65.** The plate has to pass over the loose lead and its plug.
- **Step 60: claw motor hovers 55 mm, not 80.** The 55 mm lead stands up ahead of it.
- **Steps 79 and 81: two verbs in each caption.** Each is one hand motion on video (6:05-6:21; 6:51-6:57). A possible wording for
  81: "Push the join down behind R4 so that the servo extension wire drops into the L-shaped slot in R4."
- **No tightening advice in the pivot captions.** The video shows every pivot driven home and then swinging; the brief forbids
  invented advice, and note card 59 stands in for the checks.

## Lee's notes in the arm and claw

- **4 and 12 (one screw close up, zoom out, the rest together).** No joint in Steps 24-85 has three or more identical screws (both
  video reports agree), so the "rest together" step never comes up. Every single screw on the model is shown close up with one
  axial lead line. Not settled: the pull-back after the first screw of a pair (finding 8).
- **5 (labels, captions, names).** Labels and captions are on. Every new part is labelled with its Cadasio tooltip name or its
  engraved code (Elbow / Shoulder / Claw Motor, 6 / 10 / 16mm Hex Screw, Servo Extension Wire). Honoured.
- **7 (pink servo labels).** All four MG90S motors (three of `MG90S` plus the claw's `MG90S_Cut wires shorter`) carry #ff00ff and
  #ffffff from the atlas (`model.report.json`). The horns are #1a1a1a. Honoured.
- **11 (leads present from the start).** The elbow, shoulder and claw leads are drawn from the step each motor appears (36, 46, 60),
  and their plugs ride on the loose end. Each lead stands straight out (or straight up), is moved into its slot in a step of its
  own (40, 50; 61, 78, 79, 81) and sticks straight out past the slot. No motor is ever on screen without its lead. Honoured.
- **14 (no screws that just appear).** All 23 screws in Steps 24-85 hover 60 mm out on their axis and travel in. Honoured.
- **16 (joystick wires).** Every view of the model from Step 30 on has both joysticks' wires whole. No wire caps show in the
  isolated arm or claw views. Honoured.
- **20 (finish the build and the servo wiring).** Done: three plug steps, plus the claw lead through C3 and A6, the extension, and
  the slot in R4. Not settled: when 6 and 9 are plugged in (finding 5).

## Confirmed OK (one line each)

- Pairs and numbering: Steps 24-85 run without gaps; cards are 59, 73 and 85; 168 views in all.
- Camera: it never moves inside a pair; every view is at 35 degrees elevation on a diagonal; the travel is 52-84 degrees off the view
  axis everywhere except Steps 25 and 28.
- `Step Nc` views carry no lead lines, labels or eyes.
- Lead lines: 1, 2 or 4 on every step (no 3 or 5). Every line is within 0.5 degrees of the first straight leg, except Step 31
  (1.8 degrees). Screws have one axial line; wire steps have none.
- Every `Step N` has a cue, and no step has more than two labels. Destination labels "6", "9" and "10" sit on the exact pin rows
  (z 142.0 / 152.0 / 154.6, as in `cad_pins.json`).
- One rigid part or one sub-assembly per step. Each receiver appears in place (A6, A1, A4, A10, C3). The horns move with their motors.
- Hover directions match the video: A9 along A6's normal; the motors horn first, tilted 20 to 25 degrees; C1 and C2 along the
  claw's 0.6 degree normal; C8 slid in -Z; the claw slid in along +X by 99.6 mm (its own length).
