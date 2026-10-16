# Arm.mov, stretch 3 (6:00 to 9:15): linkage on the left side, second side servo, clamp plate R7

Video: `/Users/lee-johnson/Desktop/Claude_Cadasio/MRA_Videos/Arm.mov` (12:00 long, 1080 x 1920, phone looking straight down at the worktop).
This report covers seconds 360 to 555. Status: complete.

How it was read: every frame at 2 s spacing as contact sheets (whole stretch), then every frame at 1 s spacing as contact sheets (whole
stretch), then native-size stills (1080 x 1920) at 1 s spacing for 6:05-7:11, 7:17-8:55 and 8:56-9:22, enlarged crops of every code, screw and
joint, and quarter-second frames around the three cuts. Engraved codes below were read at native size unless marked otherwise.

Naming. Codes are the ones ENGRAVED on the wood. CAD ids follow `cad_codes_base.md`:

| engraved | CAD id | CAD mesh name | what it is |
|---|---|---|---|
| A1, A2, A3 | NAUO18, NAUO19, NAUO20 | ARA_A1, ARA_A2, ARA_A2_Supplement | the three-layer lever on the left side servo (A3 is the outer layer) |
| A4 | NAUO21 | ARA_A3 | link, 90 x 10 mm, 80 mm between holes |
| A5 | NAUO22 | ARA_A4 | forearm bar, 125 x 10 mm, three holes |
| A7 / A8 | NAUO23 / NAUO24 | ARA_A5 / ARA_A6 | the two bars of the upper arm (A7 on -Z, A8 on +Z) |
| A6, A9 x 2 | NAUO29, NAUO30, NAUO31 | ARA_A11, ARA_A12 x 2 | cross plate and the two T-shaped wooden nuts of the upper arm |
| A10 | NAUO26 | ARA_A8 | triangle |
| A11, A12, A13 | NAUO25, NAUO27, NAUO28 | ARA_A7, ARA_A9, ARA_A10 | 90 x 10 mm links |
| R5 / R6 | NAUO15 / NAUO14 | ARA_R6 / ARA_R5 | turret side plates (R5 on -Z, R6 on +Z) |
| R8 / R7 | NAUO17 / NAUO16 | ARA_R8 / ARA_R7 | servo clamp plates (R8 on -Z, R7 on +Z) |

Directions. Assembly space: +X is the arm end of the base, -X the joystick end, +Y up, +Z the student's right when sitting behind the joysticks.
In the frame: while the joysticks are at the TOP of the picture, +X is down and -Z is on the RIGHT; while the joysticks are at the BOTTOM, +X is up
and +Z is on the RIGHT.

## 0. The video is not in the order things were done (important for the merge)

There are two hard cuts inside this stretch and one just after it. Quarter-second frames show them:

| cut at | frame before | frame after |
|---|---|---|
| 7:10.4 (between 7:10.25 and 7:10.50) | joysticks at top, sun patch, triangle A10 and bar A13 lying loose on the left, driver lying top right | same view, but A10 has gone from the left, the driver has moved and turned, and a hand at the bottom right is holding the finished triangle sub-assembly |
| 8:52.4 (between 8:52.25 and 8:52.50) | joysticks at bottom, both side servos fitted, hands off | joysticks at top, sun patch, second side servo lying loose again at the top left, hands holding bar A11 and triangle A10 (A13 still loose on the left) |
| 10:16.6 (between 10:16.50 and 10:16.75, outside this stretch) | joysticks at top, sun patch, hand with the triangle sub-assembly at bottom right, driver top right | joysticks at bottom, both side servos fitted: exactly the layout of 8:52.25 |

The frame at 8:52.50 continues the frame at 7:10.25, the frame at 7:10.50 continues 10:16.50, and 10:16.75 continues 8:52.25. The builder's watch
reads 7:35 at 8:47, 7:35 at 10:28 and 7:36 at 10:56. So the order in which the work was really done is:

    6:00 - 7:10.4   (linkage A4 / A5 on the left side)
    8:52.4 - 10:16.6 (triangle sub-assembly A10 + A11 + A12 built in the hands, off the kit)   <- shown later in the video than it happened
    7:10.4 - 8:52.4 (kit turned round, second side servo, clamp plate R7, two screws)
    10:16.6 - end   (triangle sub-assembly fitted to the kit)

The timeline in section 2 is in video order with the video's own timestamps; the "true order" column gives the real sequence.

## 1. State at the start (6:00)

Still: `docs/research/mra/stills/arm/t06m00s.jpg`. Joysticks at the top of the frame.

- Base and controller complete. The base servo's lead (white flag "5") is plugged into the shield and comes up out of the turret; the two joystick
  ribbons are in place.
- Upper arm (A7 | A6 with its two A9 nuts and two M3x16 screws | A8) is on the turret, straddling the ear of R2, lying forward (+X), about level. On the -Z side it is held by the shoulder pivot screw (CAD NAUO55): its tip is visible poking through R2's ear at 6:31. On the +Z side
  the A8 bar's shoulder end is free: nothing holds it yet.
- Left (-Z) side servo NAUO58 is already in the side plate engraved R5 (NAUO15) with clamp plate R8 (NAUO17) over its back. R8's upper clamp
  screw is visible (6:31, 6:47); the lower one is hidden by the servo body in every view of this stretch. The servo's lead leaves the +X end of
  the case at its outer end, carries a black flag with a white underlined "6", and lies on the worktop in front of the kit. Not plugged in.
- The three-layer lever A1 + A2 + A3 (NAUO18 / 19 / 20) is already on that servo's horn, standing roughly straight up, clamped by one screw whose
  cap head stands on A3's outer face (CAD NAUO56). The servo's black horn hub is visible between the lever and R5 (6:31).
- Link A4 (NAUO21) is already screwed to the rear-end hole of the forearm bar A5 (NAUO22): screw head on A5 (CAD NAUO57). The builder is holding
  this pair by A4.
- Loose on the worktop: bar A13 and triangle A10 on the left; the second side servo (single-ended horn already on, held by its small cross-head
  screw) at the far top left (in frame from 7:06). Clamp plate R7 and the T-handle hex driver are out of frame at 6:00.

## 2. Timeline

| # | video time | true order | action |
|---|---|---|---|
| 1 | 6:00 - 6:04 | 1 | **A4 + A5 pair presented.** Left hand holds link A4 with forearm bar A5 hanging from its far end; "A4" is turned to the camera at 6:02. |
| 2 | 6:04 - 6:11 | 2 | **Screw through the lever, then A4 hung on its tip.** 6:04 - 6:07 A4 is held beside the top of the lever. 6:05 - 6:08 the right hand brings one screw and pushes it in BY HAND from the OUTER side (-Z, the servo side), travelling +Z, through the free (top) end of the lever: it slides through all three layers A3, A2, A1 (loose holes) and at 6:08 about 3 mm of its thread shows on the inner side. 6:09 the left hand puts the free end hole of A4 (the end without A5) onto that tip, so A4 lies flat against the INNER (+Z) face of the lever (against A1); four layers are now seen edge-on (6:10 - 6:11) and the screw head has been pushed back out a few mm. A4's engraved face is the face against the lever (it looks towards -Z: confirmed at 6:47, where "A4" is read from the -Z side, behind the lever). Still `t06m06s.jpg`. |
| 3 | 6:12 - 6:29 | 3 | **Lever screw driven into A4** (CAD NAUO62, M3x10) with the T-handle hex driver held level, coming from the -Z side and passing just above the servo; left hand pinches A4 against the lever. When done its head is sunk into the large hole in the outer layer A3 (6:47: head below A3's face, while the lever's other screw stands proud) and its tip stands 1 to 2 mm proud of A4's inner face (6:31). Both observations fit a 10 mm screw: A3 + A2 + A1 + A4 is 12 mm, head recessed 3 mm. |
| 4 | 6:30 - 6:38 | 4 | Hands off. Chain as it stands: servo horn -> lever (upright) -> A4 hanging down and forward on the inner side of the lever -> A5 hanging from A4, its long end on the worktop to the right of the arm. Still `t06m34s.jpg`. |
| 5 | 6:39 - 6:46 | 5 | **Forearm folded up to the elbow.** Left hand lifts the upper arm by its free end; right hand swings A5 up (A4 and A5 make an L at 6:43) and lays A5 flat against the OUTER (-Z) face of bar A7 at A7's free end, A5's second hole (35 mm from the A4 joint) over A7's end hole. |
| 6 | 6:46 - 6:49 | 6 | Kit tipped onto its +Z side for about 2 s so the -Z side faces the camera, then set back. Best single view of this side: "R5", "R8", "A3", "A4", "A7" and one "A9" all readable. Still `t06m47s.jpg`. |
| 7 | 6:50 - 6:56 | 7 | **Elbow screw placed.** Left fingers pinch A5 to A7's end; right hand brings a short screw (6:52) and sets it by hand into A5's second hole from the outer (-Z) side, travelling +Z, into A7's end hole (6:53 - 6:56). It goes in just below the head of the A4 - A5 screw. Still `t06m56s.jpg`. |
| 8 | 6:57 - 7:06 | 8 | **Elbow screw driven** (CAD NAUO63, M3x6): driver level from the -Z side, left hand holding the joint. |
| 9 | 7:07 - 7:10 | 9 | **Motion check.** Driver put down; the left hand lowers the upper arm forward and lets go. The lever, A4 and A5 follow freely; the arm stays where it is left, lying forward with A5 sticking out forward and down from the elbow. |
| - | 7:10.4 | - | CUT. What follows was filmed after the triangle sub-assembly (rows 21 - 22 and the next stretch) had been built. |
| 10 | 7:10.5 - 7:16 | 12 | **Kit turned round.** One hand is holding the finished triangle sub-assembly (A10 with A11 and A12 screwed to it); the other reaches over, picks the whole kit up (7:11.7) and puts it down turned 180 degrees, joysticks now at the bottom of the frame. The upper arm is now raised (somewhere between 30 and 60 degrees above level; a top view does not give the angle; the CAD pose is 48). |
| 11 | 7:16 - 7:18 | 13 | Triangle sub-assembly laid on the worktop to the right (+Z side) of the kit. Not fitted in this stretch. On it, "A12" has an engraved arrowhead next to its screwed end and "A10" has an arrowhead next to the same corner (7:22 crop). |
| 12 | 7:18 - 7:21 | 14 | **Second side servo fetched** from the far left of the worktop (carried across the kit at 7:19), lead trailing. Single-ended horn with six holes already pressed on and held by its own small cross-head screw (7:22). White paper flag on the lead near the plug. |
| 13 | 7:21 - 7:27 | 15 | **Horn set by hand.** Both hands on the servo; at 7:22 - 7:23 the left fingers turn the horn (the servo is not powered and nothing is plugged in). From 7:24 the right hand holds the servo label side up, shaft pointing left (-Z), horn pointing forward (+X) as seen from above (how far it is tilted up cannot be read from a top view; it has to match the raised arm), lead leaving the +X end. Still `t07m26s.jpg`. |
| 14 | 7:28 - 7:37 | 16 | **Servo NAUO66 into the plate engraved R6 (NAUO14), from outside (+Z).** Left hand steadies the turret and the raised upper arm. The servo is brought in at an angle with the horn leading: 7:32.5 horn tip at the cut-out; 7:33.0 - 7:33.5 the horn is through the cut-out and inside the plate while the case is still outside and tilted (still `t07m33s.jpg`); 7:34 - 7:37 the case is squared up and pushed straight in (-Z) until the ears stop on R6's outer face. Label up (+Y), shaft at the +X end of the case, lead out of the +X end face at the outer end. |
| 15 | 7:38 - 7:46 | 17 | Kit picked up in the left hand and held tilted towards the camera (joystick end raised, +Z side turned part-way up), left thumb on the servo to keep it in. |
| 16 | 7:46 - 7:58 | 18 | **Clamp plate R7 (NAUO16).** 7:46 - 7:49 picked up; "R7" shown to the camera at 7:48 (still `t07m48s.jpg`). 7:50 - 7:54 the servo's plug is passed through R7's window and the plate is run along the lead (flag and all). 7:55 - 7:58 the plate is slid down the lead onto the back of the servo and pressed against the ears (still `t07m55s.jpg`). Engraved face outwards (+Z), "R7" in the top front corner (upper edge, towards the arm end; read at 7:59 and 8:26, and the same place as in the CAD: 181.1, 171.4), the two screw holes above and below the servo. |
| 17 | 7:59 - 8:21 | 19 | **First clamp screw: upper hole** (CAD NAUO68, M3x10). 7:59 - 8:05 hand away for a screw; 8:06 - 8:07 set in R7's upper hole by hand; 8:08 - 8:09 seen standing in the hole (shank about twice the head diameter long, so 10 mm, not 6 or 16); 8:10 - 8:21 driven with the driver level from the +Z side, kit still held tilted in the left hand. |
| 18 | 8:21 - 8:26 | 20 | Kit laid on its -Z side on the worktop so the R6 / R7 face is up ("R6" and "R7" both readable). The upper screw gets a few more turns from above (8:22 - 8:25); driver put down. |
| 19 | 8:27 - 8:46 | 21 | **Second clamp screw: lower hole** (CAD NAUO69, M3x10). 8:28 - 8:30 fetched and set by hand in R7's lower hole (the one nearer the base); 8:31 both screws visible, one each side of the servo (still `t08m31s.jpg`); 8:32 - 8:46 driven from above. |
| 20 | 8:46 - 8:50 | 22 | Kit stood upright again; the upper clamp screw is given a last tighten, driver level from the +Z side (8:47 - 8:49). Driver put down at 8:50. |
| - | 8:51 - 8:52.3 | 23 | Hands off: the most advanced state in this stretch (section 3). Still `t08m52s.jpg`. |
| - | 8:52.4 | - | CUT, back in time: the kit is as it was at 7:10 (joysticks at top, second side servo still loose at the top left). |
| 21 | 8:52.5 - 9:01 | 10 | **Triangle sub-assembly started, in the hands.** Right hand holds link A11, left hand holds triangle A10 (both codes readable at 8:54; A10 has an engraved arrowhead beside one corner hole). 8:55 - 8:56 the two are laid together; 8:57 - 9:01 A11's end hole is lined up over the hole in A10's sharp corner (the corner furthest from the other two holes). A11 lies ON TOP of A10's engraved face; both engraved faces look the same way (towards the camera). The arrowhead corner of A10 is NOT the one used here. Still `t09m01s.jpg`. |
| 22 | 9:01 - 9:19 | 11 | The pair is held still in the left hand by the joint while the right hand is out of frame (9:01 - 9:16), then reaches across for a screw (9:18 - 9:19). No change to any part. From 9:20 the screw is put into this joint and driven (next stretch). |

Fasteners used in this stretch:

| screw (CAD id) | size | joins | from | pivot or fixed |
|---|---|---|---|---|
| NAUO62 at (143.5, 176.3) | M3x10 | lever A3 + A2 + A1 to link A4 | outside (-Z), travelling +Z; head sunk in A3 | PIVOT: in the CAD the three lever layers are clearance holes and the thread is in A4 |
| NAUO63 at (229.0, 221.3) | M3x6 | forearm A5 to upper-arm bar A7 (elbow) | outside (-Z), travelling +Z; head on A5 | PIVOT: clearance in A5, thread in A7 |
| NAUO68 at (170.3, 171.6) | M3x10 | clamp plate R7 to side plate R6 (upper) | outside (+Z), travelling -Z | fixed |
| NAUO69 at (170.3, 153.0) | M3x10 | clamp plate R7 to side plate R6 (lower) | outside (+Z), travelling -Z | fixed |

Both pivot screws were driven until they stopped turning easily; I did not see either one backed off afterwards. The arm was moved by hand
straight after (row 9) and everything swung freely, so they were not done up hard. How loose to leave them cannot be read from the picture.

Servos and wires in this stretch: no servo is powered, centred or plugged in. The only thing done to a horn is turning the second side servo's
horn by hand (row 13) so that it points the way the raised upper arm points. Neither horn is screwed to wood: each sits in a horn-shaped pocket
(left: in the lever layers A2 and A3; right: in the shoulder end of bar A8).

## 3. State at the end

Most advanced build state (8:52.0, still `t08m52s.jpg`; this is also what the kit looks like when the next stretch resumes at 10:16.6):

- Joysticks at the bottom of the frame. Upper arm raised (30 to 60 degrees, see row 10); forearm bar A5 hanging from the elbow.
- Left (-Z) side: servo NAUO58 in R5 under R8; lever A1 + A2 + A3 on its horn; A4 from the lever's free end to A5's rear end; A5's second
  hole screwed to A7's free end.
- Right (+Z) side: servo NAUO66 in the plate engraved R6 (NAUO14), body outside, shaft inwards (-Z), clamp plate R7 over its back with both
  M3x10 screws. Seen from inside the turret at 8:52: the horn's hub and its cross-head screw sit in the pocket at the shoulder end of bar A8, and
  the horn's splined boss fills the gap between A8 and R6. So A8 is now carried by this servo.
- Leads: base servo (flag "5") plugged into the shield. Left side servo (black flag "6"): makes a small loop beside the servo and runs on the
  worktop to the front left of the kit; its plug lies free there. Right side servo (white flag): leaves the +X end of the servo and lies on the worktop
  to the right; its plug lies free. The white flag has one printed digit with a line under it; it reads as "9" (it is not clear enough to be
  certain, but the "6" is on the other servo and `cad_pins.md` puts this servo on row 9). Nothing is routed through any slot.
- Loose: triangle sub-assembly (A10 + A11 + A12) to the right of the kit; bar A13 on the left; driver.

What is on screen at the end of the stretch (9:15) is earlier in real time: the kit as at 7:10 (joysticks at top, second side servo loose), with
the left hand holding A10 and A11, hole over hole, waiting for a screw.

## 4. Hard to show in a 3D guide, or different from the CAD

1. **The video is cut out of order** (section 0). A step order taken straight from the timestamps would fit the second side servo before the
   triangle sub-assembly is built; in reality the builder built the triangle first. Neither order is forced by the parts: the triangle is built off
   the kit.
2. **A side servo with its horn on cannot go straight through the side plate.** Measured on the CAD: the cut-out in each side plate is
   23.75 x 12.30 mm (x 158.91 - 182.66, y 156.13 - 168.43); the shaft axis is at x = 175.35, y = 162.3; the horn reaches 18.6 mm from the axis.
   From the axis the cut-out's edges are only 7.3 mm (+X), 16.4 mm (-X), 6.1 mm (+Y) and 6.2 mm (-Y) away, so the horn overhangs the plate whichever way
   it points (by 2.2 mm at best, by about 7 mm in the built position). On video the builder hooks the horn through first with the servo tilted, then
   squares the servo up and pushes it home (row 14). A straight slide along Z will be reported as blocked by the collision test; this step needs a
   hand-set motion (tilt in, then level) or the horn has to be allowed to pass through the plate.
3. **The horn has to meet the pocket in A8 as the servo goes in.** The pocket is horn-shaped, so the horn must point along the upper arm. On video
   the builder turns the horn by hand to suit the arm (row 13) and holds the arm while pushing. The servo is not centred electrically at any point in
   this stretch, so the video does not show how the horn angle is supposed to relate to the servo's mid position; if that matters it was done before
   6:00 or is not done at all.
4. **Clamp plate R7 goes over the plug and lead first.** Its window (24.2 x 12.3 mm) is threaded over the servo plug, flag and lead, and slid down
   the lead onto the servo. The lead is not a CAD part, so the guide has to say this in the caption or show the lead passing through the window.
5. **The linkage is fitted in poses the CAD does not have, and the lever screw goes in before the link.** The screw is pushed through the
   lever first and A4 is hung on its tip (row 2), because the lever holes are loose and A4's hole is the one the thread bites into; a guide that
   seats A4 first and then brings the screw in shows the same result. A4 is screwed on while the lever stands upright and A4 + A5 hang down
   (rows 2 - 4); A5 is then swung up about 180 degrees to reach the elbow (row 5). In the CAD everything is in one pose (lever 24 degrees above level
   pointing back, upper arm 48 degrees up). Showing A4 + A5 arriving as a rigid pair in their final CAD positions is the simple option; it then needs
   two screws in a row (NAUO62, NAUO63) with nothing swinging.
6. **A4 and A5 arrive already joined** (screw NAUO57 was fitted before 6:00): the moving thing in row 2 is a two-part sub-assembly, not one part.
7. **Layer order on the left side** (useful for the camera and for lead lines): from outside in, A3 / A2 / A1, then A4 and A7 share the next
   layer (z 126.6 - 129.6), and A5 shares A1's layer (z 123.6 - 126.6). A4 goes on the INNER face of the lever, A5 on the OUTER face of A7. The video
   agrees with the CAD on all of this.
8. **Sunk screw head.** The lever screw NAUO62 ends up with its head inside the large hole in A3; the screw next to it (NAUO56) stands proud.
   In a 3D view the sunk head is nearly invisible once seated.
9. **The kit is handled constantly**: tipped on its side to look (6:46), turned 180 degrees (7:11), held tilted in one hand for the first clamp
   screw, laid on its side for the second (8:21 - 8:46). All four screws in this stretch are horizontal (along Z) when the kit stands upright, and
   the builder drives three of them that way; a guide can keep the kit still and bring the screws in from the side.
10. **Engraved arrowheads.** A10 has an arrowhead beside one corner hole and A12 has one beside one end hole; those two holes are the ones screwed
    together (seen at 7:22). A13 also has a small mark near one end hole (8:53). If the CAD pockets do not include these marks the guide loses a cue
    the student has on the wood. Not checked against the CAD here.
11. **Lower R8 screw not seen.** Only R8's upper clamp screw is visible in this stretch; the lower one should be confirmed from the previous
    stretch.
12. **Flags.** Left side servo: black flag, white "6" underlined. Right side servo: white flag, reads as "9" with moderate confidence. Both leads
    are simply left lying on the worktop; where they are finally routed is not in this stretch.

## 5. Reference stills

All in `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/arm/` (1280 px high).

1. `docs/research/mra/stills/arm/t06m00s.jpg` - start: lever stack on the left side servo, A4 + A5 pair in the hand, A13 and A10 loose, flag "6".
2. `docs/research/mra/stills/arm/t06m06s.jpg` - A4 against the inner face of the lever, screw about to go in from the servo side.
3. `docs/research/mra/stills/arm/t06m34s.jpg` - hands off after the lever screw: lever, A4 and A5 hanging; screw tip through A4.
4. `docs/research/mra/stills/arm/t06m47s.jpg` - the -Z side face-on: R5, R8, A3 (sunk screw head and proud screw head), A4, A7, A9, servo lead exit.
5. `docs/research/mra/stills/arm/t06m56s.jpg` - elbow: short screw standing in A5's second hole over the end of A7, before driving.
6. `docs/research/mra/stills/arm/t07m26s.jpg` - kit turned round; second side servo with single-ended horn in the hand; triangle sub-assembly (A10, A11, A12) beside the kit.
7. `docs/research/mra/stills/arm/t07m33s.jpg` - horn already through the cut-out in R6 while the servo case is still outside and tilted.
8. `docs/research/mra/stills/arm/t07m48s.jpg` - clamp plate with "R7" readable, servo seated in R6, white flag on the lead.
9. `docs/research/mra/stills/arm/t07m55s.jpg` - R7 threaded onto the lead and being slid down onto the back of the servo.
10. `docs/research/mra/stills/arm/t08m31s.jpg` - kit on its side: "R6", "R7", both clamp screws, one each side of the servo.
11. `docs/research/mra/stills/arm/t08m52s.jpg` - end state: both side servos fitted, horn in A8's pocket seen from inside, both leads loose.
12. `docs/research/mra/stills/arm/t09m01s.jpg` - (earlier in real time) A11 laid on A10's sharp corner, arrowhead visible at another corner of A10.
