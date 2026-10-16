# Claw and final wiring section: authoring log

Status: COMPLETE (13 Oct 2026). 25 steps added (guide Steps 60 to 84: 24 part / wire steps and one note card); the existing
power-cable card is now Step 85. The sandbox generates with 0 warnings; `_runthrough()` reports 168 views, 0 problems; no console
errors. The base and arm steps generate exactly as before (their generator lines are identical).

Sandbox: `/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/06aa2268-0605-4ce1-8b0c-854218069941/scratchpad/kit_full/guide.py`,
between the markers "CLAW AND FINAL WIRING (begin)" and "(end)"; new ids and names beside the existing ones at the top (the claw
horn and the extension's own plug added to `PART_OF`, the two plugs to the hover-only names); the claw lead (`CLAW`, `claw_lead`,
`by_way_of`), the extension (`EXTENSION_LEAD`, `spread`) and the side leads' plugged routes (`lead['plugged']`) in the wires section
after `SHOULDER_LEAD`. The arm section was not changed.
Check scripts: `.../scratchpad/claw_scripts/` (explore*.py = measurements; wirecheck.py = every wire and riding plug against every
part and wire on screen; sweep.py = every moving part and riding plug along its glide; holefit*.py = the plug passing the holes;
final_generate.log, wirecheck_final.log, sweep_final.log; guide_before_claw.py / guide_after_claw.py).

## Ids (engraved code = CAD id)

C1 NAUO32 (+Z clip), C2 NAUO33 (-Z clip), C3 NAUO34 (servo plate), C4 NAUO36 (bar by C2), C5 NAUO37 (bar by C1), C6 NAUO35 (keyhole
plate), C7 NAUO39 (jaw on the horn), C8 NAUO38 (geared jaw), C9 NAUO40 (cover). Claw Motor NAUO72 + horn NAUO73 (arrives fitted: video 0:00).
16mm NAUO74, 75 (C6 to C3); 10mm NAUO76 (pivot of C8); 6mm NAUO77 (A12 to C1), NAUO78 (A13 to C1), NAUO79 (A5 to C2).
Claw lead's plug NAUO90. Servo Extension Wire: coupler NAUO91 (in the parts list), its plug in the coupler NAUO92 (part of it),
plug for row 10 NAUO85 (hover-only).

## Steps as written

| Step | what | how |
|---|---|---|
| 60 | Claw Motor (+ horn) up through C3 (C3 shown), lead standing straight up through the notch of the cut-out | in hand, auto (from below), hover 55 by hand, REVIEW (shown the CAD way up) |
| 61 | lead back through the hole in C3's tongue | wire step in hand, eye on the hole; plug follows the lead through the hole |
| 62, 63 | C1, C2 through C3 from the plain side | in hand, direction by hand (the claw's own normal, 0.6 degrees off vertical) |
| 64, 65 | bars C4, C5 from the engraved side | in hand, auto |
| 66 | C6 | in hand, auto |
| 67, 68 | 16mm NAUO74, NAUO75 | in hand, hand |
| 69 | C7 over the horn | in hand, auto (horn left out of the motion test, line to the horn) |
| 70 | C9 | in hand, auto |
| 71 | C8 slid in from the C1 side | in hand, auto |
| 72 | 10mm NAUO76 | in hand, hand |
| 73 | card: check that the two jaws open and close together | card, REVIEW |
| 74 | claw into the fork | seat, auto (+X, 99.6 mm) |
| 75, 76, 77 | 6mm NAUO77, NAUO78, NAUO79 | hand, close-up |
| 78 | lead through the top hole of A6, from the plain side | wire step, eye on the hole, plug follows the lead |
| 79 | lead back through the bottom hole, plug held above R4 | wire step, eye on the hole, plug follows the lead, then forward |
| 80 | extension appears 25 mm off and is pushed onto the plug | wire step (riders), eye on the coupler, REVIEW |
| 81 | join back over R4 and down to its CAD place, extension into the L-shaped slot | wire step, eye on the slot |
| 82, 83, 84 | plugs onto rows 6, 9, 10 | as the base motor's step, but over the row then straight down; REVIEW on 82 (order) and 84 (colours) |

## Decisions and why

- Order = the video's (video_claw.md sections 2 and 4), which differs from the CAD-derived order (clips early, C9 before C8). Every
  step re-tested here with `free_directions`: free. C1 / C2 need the claw's own normal (0.011, 1, 0); C7 is blocked only by the
  horn (0.35 mm CAD overlap), so the horn is left out of that one motion test.
- Upside down: on video the claw is built engraved faces up and turned over at 3:42. A sub-assembly can only be shown in its CAD
  orientation, so C3 is on top and nine parts arrive from underneath (as B1 under B2). Captions use "engraved side / plain side /
  code facing ..." and never up or down. Review note on Step 60.
- Claw onto the arm: the CAD's tested slide into the fork (+X, auto, 99.6 mm = the claw's length, the house rule for a lengthwise
  slide). On video the claw is held against A12 / A13 alone, swung on the first screw and A5 swung down to it afterwards; the guide
  cannot show the forearm strips swung, so the screws follow in the video's order (A12, A13, A5) with the claw already in the fork.
- Three 6mm screws into three different joints from two sides: each its own close-up step (as the arm section does single screws).
- Claw lead: Step 60 straight up 55 mm, folded against the end of the motor (z 132.2: it passes through the 1 x 8 mm notch of C3's
  cut-out as the motor rises). After that every route is a piece of the CAD's own centre line: to 88 mm (through the tongue
  hole), to 176 mm (through the top hole of A6, plug over A6's face between the two A9), to 210 mm (through the bottom hole)
  plus my own tail under A6 and forward to a point above R4, and the whole CAD route (265.5 mm into the plug). The ribbon is
  carried without twist along the shared part and turned only over the tail. In the hole steps the plug is moved along the lead
  through in-between places (wires_done / ride lists), so it goes through the hole rather than through the wood.
- Brown side: the CAD's `across` for the claw chain is kept (brown meets brown in the coupler and lands on G), which puts brown on
  the label side of the claw motor, unlike the other three motors (cad_wire_paths.md section 5 recommends this).
- Where the join is made: the CAD has it inside the turret (not visible). Video: made in the air above the turret, left hanging
  over R4, pushed down behind R4 last. So the plug is held level 31 mm above its CAD place and 33 mm forward (above R4's top edge,
  z + 2 mm to clear the base motor's lead), the extension appears in line 25 mm off, and the join then goes back over R4 and down
  to the CAD place (lying level, not upright as on video). y 164.5 because a join at y 149 crossed the joystick jumper wires.
- Extension: separate item; coupler listed in the parts list as "Servo Extension Wire"; NAUO85 and NAUO90 hover-only. Wires brown /
  red / yellow (the real one on video; the Cadasio project has brown / red / orange). Drawn as a flat lead (allowed by the task),
  fanned into the contacts at both plugs (`spread` for the coupler end). Loose 35 mm, in the slot 22 mm past R4, as the base lead.
- Final wiring at the end, rows in order 6, 9, 10, one camera for the run, slot before plug (as the base motor; the video plugs
  the extension first, then tucks the join and drops the wires into the slot). On the video 6 and 9 are already in when the claw
  video starts (done off camera). Kept at the end: plugged-in side leads arc over the shield right where the join is made, and the
  task asks for the plug steps as the final wiring. Each plug is brought over its row and pushed straight down (`via([0, 30, 0])`):
  a straight glide from the hook clipped the module's headers on the way.
- T1 / T2 (NAUO41 to 44): not in any video report (no mention in video_*.md). Left out.
- Nothing happens at the very end of the video (no power, no test, no centring), so no extra card before the power-cable card.
- Jaw check: one card (the only motion test on the video, 3:29), with a review note asking whether students should turn the
  unpowered motor by hand.

## Checks

- wirecheck.py (final): every claw / extension / side lead route clear of every part on screen with it, in every view from
  Step 60, and no two wires closer than 1.0 mm (centres); nearest.py shows the check is live (smallest gaps: C2 0.52 / 0.83, R3
  0.98 / 1.24, A6 1.76, R4 pocket 1.68 mm). Only report: the row-10 plug seated on its pins (1.3 mm, as the CAD).
- sweep.py (final): staged parts touch at most 0.3 mm on the way in (press fits); the claw slide, the join's moves and the three plug
  moves are clear except for the last 1.3 mm onto the header pins. The plug passing the holes: holefit2.py, corners up to 1 to 2
  mm into the wood beside A6's 8 mm holes (a 7.9 mm plug at 23 degrees), up to 3 mm at C3's 6.3 mm tongue hole (the plug would
  have to be turned on edge), for a fraction of a second.
- Looked at in the player: hover and seated views of Steps 60, 61, 62, 64, 66, 67, 69, 71, 72, 74, 75, 77, 78, 79, 80, 81, 82, 84,
  the Completed View, and two half-way frames (79c, 83c).

## Gaps met (generator / player)

1. A sub-assembly cannot be shown turned over: the claw is built the CAD way up, parts from below, codes on hidden faces.
2. No per-step camera: the wire steps inherit the house view (from -X, -Z); the top hole of A6 is behind A5 from there, the lead's
   run between the forearm strips and down behind A6 is mostly hidden. `frame=` only sets the target and distance.
3. Labels and eye icons are placed by the player: in close-ups they float 90 px from the target and can sit on an engraved code
   ("10" over "R4" in Step 84 at an 800 px pane) or under the caption.
4. A fitted part cannot be shown in a second pose (the forearm strips swung out to meet the claw, as on video).
5. Parts with no seat of their own until late (coupler, extension plugs) have to be "carried" by some part: the claw motor.
6. A riding plug glides in straight lines between the poses it is given; following a lead through a hole needs in-between routes
   and poses, and the plug's turn is tied to the lead's twist, so it cannot be turned on edge to pass a narrow hole.
7. parts.html / PART_VIEWS were not looked at for the new parts.
