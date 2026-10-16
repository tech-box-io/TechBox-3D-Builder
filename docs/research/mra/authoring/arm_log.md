# Arm section: authoring log

Status: COMPLETE (13 Oct 2026). 36 steps added (guide Steps 24 to 59: 35 part / wire steps and one note card).
The sandbox generates with 0 warnings; `_runthrough()` reports 119 views, 0 problems; no console errors.

Sandbox: `/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/06aa2268-0605-4ce1-8b0c-854218069941/scratchpad/kit_full/guide.py`,
between the markers "ARM (begin)" and "ARM (end)"; new ids and names next to the existing ones at the top; the two leads
(`side_lead`, `ELBOW_LEAD`, `SHOULDER_LEAD`) in the wires section after the base motor's lead.
Check scripts: `.../scratchpad/arm_scripts/` (common.py, lever.py, servo_plan.py, servo_check.py, wirecheck.py, sweepcheck.py,
misc1.py, camscore.py, tipcross.py, a9cam.py; generator output of the last run in final_generate.log).

## Ids (engraved code = CAD id)

A1 NAUO18, A2 NAUO19, A3 NAUO20, A4 NAUO21, A5 NAUO22, A6 NAUO29, A7 NAUO23, A8 NAUO24, A9 NAUO30 + NAUO31, A10 NAUO26,
A11 NAUO25, A12 NAUO27, A13 NAUO28, R7 NAUO16 (+Z), R8 NAUO17 (-Z).
Elbow Motor NAUO58 (horn NAUO59, plug NAUO84, row 6, -Z side, in R5). Shoulder Motor NAUO66 (horn NAUO67, plug NAUO86, row 9, +Z side, in R6).
Screws: 16mm NAUO53, 54; 6mm NAUO55, 57, 63, 64, 65, 70; 10mm NAUO56, 60, 61, 62, 68, 69, 71.

## Steps as written

| Step | what | how |
|---|---|---|
| 24 | A7 onto A6 (A6 shown) | in hand, auto |
| 25 | A9 (NAUO30) into the slot next to A7 | in hand, direction by hand (A6's normal), line by hand |
| 26 | 16mm NAUO53 | in hand, hand |
| 27 | A8 onto A6 | in hand, auto |
| 28 | A9 (NAUO31) | in hand, as 25 |
| 29 | 16mm NAUO54 | in hand, hand |
| 30 | upper arm onto R2 | seat, auto (from above) |
| 31 | 6mm pivot NAUO55 through R5's opening | hand, close-up, line by hand |
| 32, 33 | A2 on A1 (A1 shown); A3 on A2 | in hand, direction by hand |
| 34 | 10mm NAUO56 | in hand, hand |
| 35 | lever onto the head of NAUO55 | seat, turned path, close framing |
| 36 | Elbow Motor + horn, lead loose | turned path (collision search), close framing |
| 37 | R8 over the lead | hand (hover 45) |
| 38, 39 | 10mm NAUO60, NAUO61 | hand, close-up |
| 40 | elbow lead into R5's hook | wire step, eye on the slot |
| 41 | A5 on A4 (A4 shown) | in hand, hand |
| 42 | 6mm NAUO57 | in hand, hand |
| 43 | A4 + A5 onto lever and A7 | seat, auto (from above) |
| 44 | 10mm NAUO62 | hand, close-up, REVIEW |
| 45 | 6mm NAUO63 | hand, close-up |
| 46 | Shoulder Motor + horn, lead loose | turned path (collision search), REVIEW (flag 9) |
| 47 | R7 over the lead | hand (hover 45) |
| 48, 49 | 10mm NAUO68, NAUO69 | hand, close-up |
| 50 | shoulder lead into R6's hook | wire step, eye on the slot |
| 51 | A11 on A10 (A10 shown) | in hand, hand |
| 52 | 6mm NAUO64 | in hand, hand |
| 53 | A12 on A10 | in hand, hand |
| 54 | 6mm NAUO65 | in hand, hand |
| 55 | triangle group inside R6 / onto A8 | seat, auto (from above), lines by hand |
| 56 | 6mm NAUO70 from outside R6 | hand, close-up |
| 57 | A13 | hand (face-on) |
| 58 | 10mm NAUO71 | hand, close-up |
| 59 | note: check that the arm and its links swing freely | card |

## Decisions and why

- Order follows the video's real order (video_arm.md section 0), with two moves forced by "one sub-assembly in the hand at a
  time": A4 + A5 are joined after R8 (video: before the lever goes in), and the triangle group is built after the Shoulder Motor
  (video: before). Same as the merged report's own proposal. Nothing depends on either.
- A4 is seated before the lever-top screw NAUO62 (video: screw pushed through the lever first, A4 hung on its tip two seconds later).
  Same result.
- Horns: both side motors arrive with the horn fitted (video 4:28 and 7:22, each held by its own small screw): horn in PART_OF,
  motor and horn move as one.
- Lever path: upright (turned -66 degrees about the shoulder axis [175.33, 161.90]), 60 mm above and 3.2 mm towards R5; down; across
  onto the head of NAUO55; swung down. Checked leg by leg, as the player interpolates, against turret, upper arm and NAUO55: clear
  (0.12 mm numerical touch on the screw head). -50 to -75 degrees also clear; -90 hits A7.
- Motors with horn fitted cannot go straight in (a level slide puts the horn 1.5 mm into the side plate). Planar search (tilt about the
  axis square to shaft and horn, slide along the horn, in / out): elbow way in (tilt, mm along horn, mm out) = (20, -10, 60) (20, -10, 15)
  via (20, -8, 13) (0, -1, 6) (0, 0, 0), worst overlap 0.48 mm with R5; shoulder = (20, -9, 60) (20, -9, 21) via (25, -9, 16)
  via (25, -5, 13) (0, 0, 6) (0, 0, 0), worst 0.51 mm with R6. Matches the video (horn end leading, levelled, pushed home).
- Leads: loose = out of the end of the motor, folded back over its back, straight out for 42 mm (68 mm in all), through the window of
  the hovering clamp plate (hover 45 mm), plug beyond the plate. Hooked = the CAD's own centre line as far as just through the hook
  slot (113.5 / 139.5 mm) plus 22 mm level towards the controller, plug on the end. Every route checked against every part on screen
  with it to the end of the section: clear by more than the wire's radius. Every moving part's sweep checked against the wires on
  screen: only R8 / R7 touch a lead (1.4 mm into the fold at the motor's end, for a moment, as the plate goes over it; the motor's
  own rigid 3 mm lead stubs are in the way there too). Plugs left riding (`ride=`), not plugged in. Tested in a throwaway copy that
  `move=[plug]` with `W.plugged_lead(lead['chain']['middle'], lead['chain']['across'], lead['plug'])` generates from this end state.
- Hook steps come straight after each clamp plate's second screw (the video never routes these leads).
- R8 / R7 by hand along the motor's axis: the collision test is blocked by the motor's rigid lead stubs.
- Single screws on the model are shown close up (focus on the screw); screws inside a sub-assembly view are not.
- Close framing (focus) also on the lever, both motors, both clamp plates, both hook steps, A4 + A5, the triangle and A13: at whole-model
  scale none of these could be made out.
- No tightening advice in the captions: the video shows every pivot screw driven until it stops and the joint swinging afterwards,
  never a screw backed off. One note card at the end stands in for the builder's three checks by hand.
- Captions name groups by their codes ("A6 - A9", "A1 - A3"), as the existing "R1 - R6"; "the lever" only in comments.
- NAUO62: in the CAD pose the screw's head passes 1.8 mm through R5's top edge (checked: 1.5 mm deep, nothing else touched). On video
  the lever is swung upright first. A fitted part cannot be shown in a second pose, so the step carries a Review note.
- Every other screw's straight path from 60 mm out was checked against what is in place when it goes in: clear.

## Camera (the generator picks one of four views; three steps needed steering)

- A9 steps: with the automatic lead line the first one was seen along the face of A6 (slot invisible). A line that follows the stem
  tip through A6 (`lines_at` single point) makes the engraved-face view score within reach, and it is chosen.
- Pivot screw: the automatic line (to the hole in A7) scores the same from the R6 side as from the R5 side, and the camera stayed
  on the R6 side. Line set by hand from the top of the screw's head to just under the top edge of R5's opening (1.7 degrees off the
  axis; a point exactly on the axis in the opening is 5.7 mm from any part and raises the generator's "not on any part" warning).
- Shoulder Motor: line ends where the horn tip passes through R6; a line ending short of R6 is as visible from the R5 side and the
  camera stayed there.
- Result: Steps 24-30 from -X +Z, 31-45 from the R5 side (-Z), 46-58 from the R6 side (+Z). `camscore.py` reproduces the scoring.

## Generator / player gaps met

1. `Guide.seat()` leaves a sub-assembly's riders in `in_hand`: the joysticks' eight wire caps showed in every later isolated view.
   Worked round inside the arm section (`g.in_hand` cleared of JUMPER_CAPS). Existing Steps 18 / 19 (right joystick) still show the
   left joystick's four caps.
2. No per-step camera: side and direction can only be nudged through which lead-line samples are visible.
3. A fitted part cannot be shown in a second pose (lever swung upright for NAUO62; upper arm lying forward until the Shoulder Motor
   is in; links hanging).
4. Only one sub-assembly in the hand at a time.
5. A plate cannot be threaded along a flexible lead: R8 / R7 pass through the lead's fold and the rigid stubs for a moment.
6. `lines_at` warns for a point more than 3 mm from any part, so a line cannot end in the middle of an opening.
