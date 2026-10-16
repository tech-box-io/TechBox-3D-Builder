# Arm.mov (12:00): the arm, merged report

Status: COMPLETE (13 Oct 2026). All four segment reports merged; the points they disagreed on were checked against the video.

Video: `/Users/lee-johnson/Desktop/Claude_Cadasio/MRA_Videos/Arm.mov` (719.2 s, 1080 x 1920 portrait, phone looking down at a granite worktop).
Merged from `video_arm_seg1.md` (0:00-3:15), `video_arm_seg2.md` (3:00-6:15), `video_arm_seg3.md` (6:00-9:15) and `video_arm_seg4.md`
(9:00-12:00), all read in full. Where the segments disagreed or were unsure I looked at the video again (1 s frames at native size);
those points are marked "merge check". CAD numbers are from `cad_arm_claw.md`, `cad_pins.md`, `cad_wire_paths.md` and
`mra_instances.json`; the CAD was not re-measured for this report.

## Names and directions

Codes are the ones ENGRAVED on the wood, as read in the video. For most arm parts the CAD mesh name is a different code.

| engraved (video) | CAD id | CAD mesh name | what it is |
|---|---|---|---|
| A1 | NAUO18 | ARA_A1 | lever, inner layer (next to A7): end hole, middle hole, one 5.7 mm round hole |
| A2 | NAUO19 | ARA_A2 | lever, middle layer: end hole, middle hole, keyhole-shaped slot (horn pocket) |
| A3 | NAUO20 | ARA_A2_Supplement | lever, outer layer (faces R5): as A2 but the end hole is 5.6 mm (takes a screw head). This is the CAD's "A2 supplement" |
| A4 | NAUO21 | ARA_A3 | thin link 90 x 10 mm, two holes 80 mm apart, code next to one end |
| A5 | NAUO22 | ARA_A4 | forearm bar on the -Z side, 125 x 10 mm, three holes (0 / 35 / 115 mm), code between the first two |
| A6 | NAUO29 | ARA_A11 | cross plate of the upper arm: two tabs on each long edge, two cross-shaped slots, two square holes |
| A7 | NAUO23 | ARA_A5 | upper-arm bar on the -Z side: hole at each end, two slots, centre hole |
| A8 | NAUO24 | ARA_A6 | upper-arm bar on the +Z side: as A7 but a horn-shaped loop slot at the shoulder end |
| A9 (two) | NAUO30, NAUO31 | ARA_A12 (twice) | T-shaped wooden nuts, one hole each. The CAD's two "A12". They are nuts for the 16 mm screws, not spacers |
| A10 | NAUO26 | ARA_A8 | triangle plate, three holes, a cut-through triangle mark beside one of them |
| A11 | NAUO25 | ARA_A7 | link 90 x 10 mm from the triangle down to the turret; code at one end, no mark |
| A12 | NAUO27 | ARA_A9 | link 90 x 10 mm with a cut-through triangle mark at its coded end |
| A13 | NAUO28 | ARA_A10 | forearm strip on the +Z side, 90 x 10 mm, with a cut-through square mark at its coded end |
| R2 | NAUO11 | ARA_R2 | middle wall of the turret; its ear carries the shoulder pivot |
| R5 | NAUO15 | ARA_R6 | turret side plate on the -Z side (z 109-112) |
| R6 | NAUO14 | ARA_R5 | turret side plate on the +Z side (z 169.2-172.2), the taller one with a lobe on its top edge |
| R8 | NAUO17 | ARA_R8 | servo clamp plate on the -Z side |
| R7 | NAUO16 | ARA_R7 | servo clamp plate on the +Z side |
| Elbow Motor | NAUO58 | MG90S | side servo on the -Z side; horn NAUO59 (single arm), lead NAUO88, plug NAUO84 (row 6); black flag, white underlined "6" |
| Shoulder Motor | NAUO66 | MG90S | side servo on the +Z side; horn NAUO67 (single arm), lead NAUO89, plug NAUO86 (row 9); white flag "9" |

"Elbow Motor" and "Shoulder Motor" are the names in TechBox's own Cadasio project (`cadasio_mra_project.md`, section 3) and they fit the
mechanism seen on video: the -Z servo turns the lever that moves the forearm, the +Z servo turns the upper arm directly.

Screws used in this video (15): M3x16 NAUO53, NAUO54; M3x6 NAUO55, NAUO57, NAUO63, NAUO64, NAUO65, NAUO70; M3x10 NAUO56, NAUO60, NAUO61,
NAUO62, NAUO68, NAUO69, NAUO71. All socket-head, driven with a black T-handle hex driver (handle printed "3.0"). Lengths are the CAD's;
on video they can only be told apart as short / medium / long (section 5, item 9). There are no nuts: every screw cuts its own thread in wood.

Directions (assembly space, mm, Y up): the controller is at -X and the arm reaches out towards +X; -Z is the student's left when sitting at
the joysticks (R5, R8, Elbow Motor), +Z the student's right (R6, R7, Shoulder Motor). "Outside" means away from the middle of the turret.

## Short answers

- **Which servo goes where.** Elbow Motor (NAUO58, lead flag "6") in side plate R5 on the -Z side (student's left), held by clamp plate R8.
  Shoulder Motor (NAUO66, lead flag "9") in side plate R6 on the +Z side (student's right), held by R7. Both go in from OUTSIDE the turret,
  shaft pointing INWARDS, the shaft at the end of the case away from the controller (+X), the lead leaving that same end on the outside.
  Each clamp plate is threaded over the plug and lead first and is held by two 10 mm screws that pass beside the servo, not through its ears.
- **Horns.** Both servos arrive with a single-arm horn already pressed on and held by its own small screw. No horn is screwed to wood. Each
  is fed through the side plate ahead of the servo (servo tilted, horn first, then levelled) and drops into a horn-shaped pocket: the Elbow
  Motor's into the keyhole slot of lever layers A2 + A3 (A1 closes the back), the Shoulder Motor's into the loop slot at the shoulder end of A8.
- **Pivots** (must stay free to turn): the 6 mm screw through A7 into R2 (shoulder); the lever on the head of that screw (no fastener of its
  own); lever top to A4 (10 mm); A4 to A5 (6 mm); A5 to A7 (6 mm, elbow); R6 to A11 (6 mm); A11 to A10 (6 mm); A12 to A10 (6 mm); A13 + A10
  to A8 (10 mm, elbow). **Fixed** (done up tight): the two 16 mm screws of the upper arm, the 10 mm screw through the lever, the four 10 mm clamp screws.
- **Layers, -Z side, outside in:** R8, the motor's ears, R5, (gap), A3, A2, A1, then A7 and A4 side by side in one layer, then R2's ear. A5 is in
  A1's layer, on the outside of A4 and A7. **+Z side, from the arm outwards:** A8, A10, then A11 / A12 / A13 in one layer, R6 (outside A11's
  lower end only), the motor's ears, R7.
- **"Spacers".** There are none. The CAD's two "A12" are the T-shaped nuts engraved A9 that the 16 mm screws thread into. The CAD's
  "A2 supplement" is the lever's outer layer, engraved A3; it is screwed into the lever and carries half of the horn pocket.
- **Leads.** Neither side servo's lead is routed or plugged in during this video; both lie loose on the worktop to the end. They are already
  plugged in when Claw.mov starts.
- **Order.** Upper arm (in the hand), onto R2, shoulder pivot screw through R5's empty servo opening, lever (in the hand), link pair A4 + A5
  (in the hand), lever into the turret, Elbow Motor, R8, lever-top screw into A4, elbow screw, triangle group (in the hand), Shoulder Motor,
  R7, triangle group onto R6, A13 and the last elbow screw. The video shows the last three blocks in a different order from the one they were done in (section 0).

## 0. The video is not in the order the work was done

Merge check, confirmed on 1 s frames (7:08-7:13, 8:50-8:55, 10:14-10:19; stills `merge_cut_*.jpg`). There are three hard cuts:

| cut at | just before | just after |
|---|---|---|
| 7:10.4 | joysticks at the top of the frame, arm lying forward, A10 and A13 loose on the left | same view, but a hand at the bottom right already holds the finished A10 + A11 + A12 group; the kit is then turned round |
| 8:52.4 | joysticks at the bottom, BOTH side servos fitted, hands off | joysticks at the top, NO servo in R6, a loose servo at the top left, hands picking up A11 and A10 |
| 10:16.6 | joysticks at the top, no servo in R6, the finished A10 + A11 + A12 group in the hand | joysticks at the bottom, both side servos fitted: the layout of 8:52 |

The frames either side of each cut match up: on segment 3's quarter-second frames 8:52.50 carries on from 7:10.25, 7:10.50 from 10:16.50
and 10:16.75 from 8:52.25, and the builder's watch reads 7:35 at 8:47, 7:35 at 10:28 and 7:36 at 10:56. So it is one continuous recording
with two blocks swapped when it was put together. Why is not known. The real order was:

    0:00 - 7:10     upper arm, shoulder pivot, lever, Elbow Motor, R8, linkage A4 / A5
    8:52 - 10:16    triangle group A10 + A11 + A12 built in the hand      (shown LATER in the video than it happened)
    7:10 - 8:52     kit turned round, Shoulder Motor, R7
    10:17 - 11:59   triangle group fitted, A13, elbow screw

Segment 3 found this. Segment 4 did not: its start state ("both side servos fitted at 9:00") is right only from 10:17, and the "fourth servo,
presumably the claw's" that it saw lying loose from 9:00 to 10:16 is the Shoulder Motor before it was fitted. Nothing forces either order:
the triangle group is built off the kit, so it can be built before or after the Shoulder Motor goes in.

The timeline below is numbered in the REAL order, with the video's own timestamps.

## 1. What is already built or laid out at 0:00

- Base and controller finished: base plates with their six screws, turret R1 to R6 with the base motor in its floor, shield with the Nano,
  both joysticks under plate B8, both joystick ribbons plugged in. It stands at the top left, partly out of frame, and is pulled into frame at 1:44.
- The base motor's lead (brown / red / orange, white flag "5") is plugged into the shield. It comes up out of the turret on the R6 side of R2
  and goes over the top of the controller-side end wall next to that wall's slot (as segment 1 read it; not re-checked).
- Nothing of the arm is on the turret. R5 and R6 each have an EMPTY rectangular servo opening. R2's ear has one hole near its top.
- Loose on the worktop, codes up: clamp plate R8 and a second frame plate half out of frame (R7, by elimination), one A9 (the second out of
  frame), A6, A8, A7, A13, A11, A12, A10.
  A1 to A5 and both side servos are out of frame. The driver is at the top right. Screws are kept out of frame; the builder reaches for each one.
- Both side servos arrive with a black single-arm horn already on the shaft, held by a small cross-head screw in the hub (merge check: seen at
  4:28 on the Elbow Motor and at 7:22 on the Shoulder Motor; stills `merge_horn_screw_*.jpg`). No horn is fitted, removed or screwed to wood
  anywhere in this video. One of them (the Shoulder Motor) lies at the left edge of the frame from 2:47, and is still there through 8:53-10:16, until it is picked up at 7:19.
  Segment 1 took it to have no horn; at native size a black hub is on its shaft at 2:48 and the arm cannot be seen either way
  (`merge_loose_servo_02m48s-10m13s.jpg`). It has its horn two seconds after it is picked up, so I take the horn to be on throughout.

## 2. Timeline (real order; video timestamps)

Every joint is called FIXED (clamped tight) or PIVOT (a part has to turn on the screw). "Pivot" is from what the parts do afterwards on video
and from the CAD's hole sizes (2.8 mm free, 2.3 mm thread); how tight each pivot screw was left cannot be seen (section 5, item 7).

### A. Upper arm (H-frame), built in the hand: 0:02 - 1:38

1. **0:02-0:14 A7 onto A6.** Cross plate A6 (NAUO29) is held in the left hand, engraved face up. Bar A7 (NAUO23) is pressed sideways onto the
   two tabs on the long edge of A6 nearest the "A6" code; the tabs enter A7's two slots. A7 stands square to A6, engraved face OUTWARDS, with
   the "A" of "A7" at the same end as the "A6" code. In CAD terms A7 moves +Z onto tabs at [195.4, 184.1, 126.4] and [214.2, 204.9, 126.4].
2. **0:15-0:19 first A9 into its slot.** T piece A9 (NAUO30; code read at 0:17) is pushed, stem first, into the cross-shaped slot nearest A7,
   from the ENGRAVED side of A6 (CAD: along [0.74, -0.67, 0], window at [200.7, 190.0, 138.0]). Its bar stops on A6's face, long edge
   parallel to A7. Its code faces A7 (fairly sure; the CAD has it facing the other way; the piece is symmetric, so only the picture differs).
   It is loose until the screw bites; A6 is kept level meanwhile.
3. **0:21-0:50 first 16 mm screw (NAUO53).** Pushed by hand through the centre hole of A7 from its outer face, along the slot in A6, into the
   hole in the A9 (0:22-0:26), then driven with the hex driver (0:27-0:49) until the head is down on A7. FIXED. CAD: head at
   [200.7, 190.0, 123.5], pointing +Z; free through A7, thread in the A9.
4. **0:52-1:01 A8 onto A6.** Assembly turned round in the hand. Bar A8 (NAUO24; code read 0:56) is pressed onto the two tabs on the other long
   edge, engraved face OUTWARDS, its loop-slot (horn pocket) end at the end of the frame AWAY from the "A6" code. CAD: A8 moves -Z onto tabs
   at [195.4, 184.1, 162.6] and [214.0, 204.8, 162.6].
5. **1:02-1:06 second A9 (NAUO31)** pushed stem first into the other cross slot, again from the engraved side of A6 (window [208.7, 198.9, 151.0]).
6. **1:10-1:38 second 16 mm screw (NAUO54).** Through the centre hole of A8 from outside into the second A9: by hand 1:10-1:16, driver
   1:18-1:37. FIXED. CAD: head at [208.7, 198.9, 165.5], pointing -Z. At 1:38 the H-frame is complete: one screw in from each outer face, the
   two A9 standing on the engraved face of A6 and staggered 12 mm along the frame (the one on the A7 side nearer the shoulder), each screw
   tip showing 1-2 mm past its A9. Each screw took 20 s or more of turning.

### B. Upper arm onto the turret: 1:39 - 2:39

7. **1:39-2:10 H-frame lowered over R2.** Driver down, base + controller pulled into frame (1:44) and turned. The H-frame is turned end for
   end so the loop-slot end of A8 leads and A6's engraved face is up, then angled in from the front, over the end wall away from the
   controller, down into the open top of the turret (2:02-2:04). A7's end goes flat against the engraved face of R2's ear (the face towards
   R5); A8's loop end goes down on the other side of R2, close inside R6. The frame straddles R2. The base motor's lead comes up between the
   two bars, on the shoulder side of A6. 2:05-2:10: fingers line A7's end hole up with the hole in R2's ear. CAD: A7 on the -Z face of the ear
   at [175.3, 161.9, 129.55]; the frame can be lowered straight down (-Y).
8. **2:11-2:36 shoulder pivot screw, 6 mm (NAUO55).** Fetched 2:11, brought to the outside of R5 at its servo opening and started with the
   fingers through A7's end hole into R2's ear (2:15-2:20; the hand hides how the fingers reach it). At 2:21 it stands in the hole, head
   towards R5. Driven 2:22-2:36 with the driver's shaft passing THROUGH THE EMPTY SERVO OPENING IN R5 (clear 2:23-2:34). The head ends on
   A7's outer face. CAD: head top [175.35, 161.84, 123.52], pointing +Z; free through A7, thread in R2. It has to go in before the Elbow Motor,
   which later sits on the same axis and blocks the driver.
9. **2:37-2:39 hands off.** The frame, held only by that screw, swings forwards and comes to rest on the top of the front end wall, engraved
   face of A6 up, "A6" code at the free end. So the joint turns: PIVOT (the shoulder bearing on the -Z side). Nothing is seen being backed off.
   The +Z bar A8 is not held by anything yet. Assembly pushed away to the top left.

### C. Lever A1 + A2 + A3, built in the hand: 2:40 - 3:26

10. **2:40-3:00 three layers stacked.** A1, A2, A3 are laid in a row, codes up (2:40-2:48), showing their differences: each has a hole at the
    far end, a hole just below the code and a small notch in one long edge; A1 has ONE LARGE ROUND HOLE where A2 and A3 have a KEYHOLE SLOT
    (round end towards the code); A3's far-end hole is LARGER. A1 is picked up, A2 laid flat on it (2:49-2:55; A1's large hole shows through
    the round end of A2's keyhole), then A3 on A2 (2:56-3:00). All three codes face the same way and the three notches line up. Order in the
    stack: A1 / A2 / A3. CAD: A2 (NAUO19) and A3 (NAUO20) each go +Z onto A1 (NAUO18); z layers A3 117.55-120.55, A2 -123.55, A1 -126.55.
11. **3:01-3:26 lever screw, 10 mm (NAUO56).** Pushed by hand into the MIDDLE hole (the hole just below the "A3" code) from the A3 face
    (3:03-3:05); it drops about 6 mm and stands about 4 mm proud. Driven 3:06-3:22 through A3 and A2 into A1, fully tight. FIXED: the three
    layers are now one part. Head proud on A3's engraved face. Shown at 3:24 and put down, A3 up: from the coded end, large hole, "A3", screw
    head, round end of the keyhole, slot. The keyhole pocket (two layers deep, A1 its floor) is empty. CAD: head top [158.64, 169.43, 114.54],
    pointing +Z; free through A3 and A2, thread in A1; tip 1.0 mm proud of A1's inner face.

### D. Link pair A4 + A5, built in the hand: 3:27 - 4:01

12. **3:27-3:45 A5 laid on A4.** Both taken from the pile at the lower left and laid side by side, codes up (A5 the longer, three holes; A4 two
    holes). A5's end hole NEXT TO ITS CODE is laid over A4's PLAIN end hole (the end far from "A4"), both engraved faces the same way, A5 on
    top. CAD: A5 (NAUO22) lies on the -Z face of A4 (NAUO21) at [197.05, 235.70].
13. **3:43-4:01 link screw, 6 mm (NAUO57).** Put in by hand through A5 (3:43-3:45), driven 3:46-3:58 with the bars held on edge. Head on A5's
    engraved face. At 3:59 the pair is opened to an L and swings freely: PIVOT. CAD: head top [196.99, 235.71, 120.52], pointing +Z; free
    through A5, thread in A4.

### E. Elbow Motor side of the turret: 4:02 - 5:49

14. **4:02-4:12 kit laid on its +Z side** so R5 faces up at the camera (base plate on edge, arm hanging at the lower left). Handling only.
    It stays like this until 5:40, apart from a moment upright at 4:24.
15. **4:13-4:27 lever into the gap between R5 and A7.** Lever held with the A3 face towards the camera (so A3 will face R5), keyhole end
    lowest (4:13-4:14), turned edge-on and slid in from the open top of the turret, KEYHOLE END FIRST, between R5's inner face and bar A7
    (4:15-4:16). Seen through R5's servo opening at 4:17-4:21: the head of the lever's own screw in the corner of the opening nearest the turret
    top and the controller, and a set of concentric rings (round end of the keyhole, A1's round hole, a screw head inside it) at the end away
    from the controller. That is A1's 5.7 mm hole sitting over the HEAD of the shoulder pivot screw NAUO55. The coded end of the lever sticks
    out past R5's top edge. 4:24-4:27: kit stood up, a fingertip presses the lever down in the gap (guess: seating it on the screw head), kit
    laid back. Nothing fastens the lever: it is a PIVOT riding on the screw head, trapped between A7 and R5. CAD: the gap is 14.6 mm (R5 inner
    face z 112.0 to A7 z 126.55); the lever is 9 mm plus its 3 mm screw head; it has to hop 3 mm sideways over the pivot screw's head.
16. **4:28-4:43 Elbow Motor (NAUO58) into R5 from outside, horn (NAUO59) already on.** Merge check at native size: at 4:28 both hands hold
    the servo over the kit, horn and its hub screw visible (whether the horn is being turned by hand here, as it is on the other servo at
    7:22, cannot be told); 4:30-4:32 it is carried out to the right and back; 4:33-4:36 it is turned so the
    shaft points down at R5, long axis of the case along the long axis of the opening, shaft at the end AWAY from the controller, horn lying
    along the case and pointing outboard past the shaft end. 4:37 tilted, horn end lowest, and the horn fed through the opening first; 4:38-4:40
    levelled; 4:41-4:43 pressed down until the mounting ears sit on R5's outer face. The left forefinger holds the lever's sticking-out end
    still, so the horn drops into the lever's keyhole pocket; this happens blind, behind R5. Case outside the turret, shaft inwards (+Z). The
    lead leaves the case at the end away from the controller, outside R5, and carries a black flag with a white underlined "6". The horn is not
    screwed to any wood; it is captive in the pocket in A2 + A3 with A1 behind it. CAD: shaft tip [175.66, 162.28, 120.35] pointing +Z, ears
    z 106.48-108.98 on R5's outer face z 109.0, lead leaves at [181.51, 162.28, 92.85] heading +X, horn pointing [0.91, -0.41, 0].
17. **4:44-5:00 clamp plate R8 (NAUO17) over the lead and onto the servo.** Lead lifted, R8 picked up (4:44-4:46). The servo's PLUG is passed
    through R8's window (4:47-4:51; flag "6" read here) and R8 is slid down the lead and lowered over the back of the servo (4:52-4:57),
    engraved face out, "R8" on the long side nearest the turret top, at its controller end. The servo's back end and lead stick out through
    R8. CAD: R8 at z 103.46-106.46, window x 157.7-181.9, y 156.1-168.4; it moves +Z onto the ears.
18. **5:01-5:21 first clamp screw, 10 mm (NAUO60).** Set by hand in R8's hole on the turret-top side of the servo, next to the "R8" code
    (5:03-5:07), driven 5:08-5:20 through R8 into R5. It passes BESIDE the servo case, not through the servo's ear holes; the ears are trapped
    between R8 and R5. CAD: [170.31, 171.58], head top z 100.45, pointing +Z.
19. **5:22-5:40 second clamp screw, 10 mm (NAUO61).** Lead swept out of the way (5:24-5:26); screw set in R8's other hole, on the base-plate
    side of the servo (5:27-5:30; both heads visible 5:29-5:30); driven 5:31-5:40. CAD: [170.31, 152.93].
20. **5:41-5:49 kit stood upright; a clamp screw finished** with the driver level from the R5 side, its shaft passing over the top of the
    servo, so it is the upper one, NAUO60 (fairly sure). Both clamp screws end tight: FIXED.

### F. Elbow linkage on the -Z side: 5:50 - 7:10

21. **5:50-5:59 lever swung upright by hand.** The right hand takes the lever by its free (coded) end and turns it about the shoulder axis from
    leaning towards the controller to nearly upright; the left hand holds the arm. This turns the servo by hand through its horn. Not a
    powered test. Purpose (inferred): to lift the lever's end hole clear above R5's top edge so a screw and driver can reach it (CAD: in the
    drawn pose the hole axis is at y 176.3 and R5's top edge at y 175.4).
22. **6:00-6:11 screw through the top of the lever, A4 hung on its tip.** The A4 + A5 pair is picked up by A4, A5 hanging from its far end
    ("A4" shown at 6:02). Merge check (`merge_a4_on_lever_06m06s-06m09s.jpg`): at 6:06-6:07 A4 is held flat beside the lever, code up, while
    the right hand pushes a screw in BY HAND from the R5 side through the lever's top hole (A3's large hole, then A2, then A1); at 6:08-6:09
    A4 is turned on edge and its CODED end hole is put onto the screw's tip, against the INNER face of the lever (against A1). So the screw
    is started first and the link second, as segment 3 has it (segment 2 has them the other way; the difference is two seconds). A4's
    engraved face ends up against the lever, looking towards -Z ("A4" read from the -Z side at 6:47).
23. **6:12-6:38 lever-top screw driven, 10 mm (NAUO62).** Driver level from the -Z side, passing just above the servo; left hand pinches A4 to
    the lever (6:12-6:29). The head ends SUNK in the large hole of A3 (its neighbour NAUO56 stands proud); the tip stands 1-2 mm proud of
    A4's inner face. A4 + A5 swing freely on it afterwards (6:30-6:38): PIVOT. CAD: head top [143.47, 176.30, 117.54], pointing +Z; head in
    A3's 5.6 mm hole, free through A2 and A1, thread in A4.
24. **6:39-6:49 forearm folded up to the elbow.** The left hand lifts the upper arm by its free end; the right hand swings A5 up and lays it
    flat on the OUTER (-Z) face of A7 at A7's free end, A5's second hole (35 mm from the A4 joint) over A7's end hole. 6:46-6:49: kit tipped
    onto its +Z side for 2 s to show the -Z side (best single view: "R5", "R8", "A3", "A4", "A7", one "A9" readable).
25. **6:50-7:06 elbow screw on the -Z side, 6 mm (NAUO63).** Set by hand through A5's second hole into A7's end hole from the outside
    (6:52-6:56), driven level from the -Z side (6:57-7:06). Head on A5. PIVOT. CAD: head top [228.88, 221.29, 120.52], pointing +Z; free
    through A5, thread in A7.
26. **7:07-7:10 motion check.** Driver down; the left hand lowers the upper arm forwards and lets go. Lever, A4 and A5 follow freely; the arm
    stays lying forward with A5 sticking out forward and down from the elbow.

    *Cut at 7:10.4. The work carries on at 8:52.5 in the video.*

### G. Triangle group A10 + A11 + A12, built in the hand: 8:52 - 10:16 (shown later in the video than it happened)

27. **8:52-9:19 A11 laid on A10.** Triangle A10 (NAUO26) in the left hand, engraved face up. Link A11 (NAUO25) is laid on TOP of A10's engraved
    face, also engraved face up, the hole at A11's CODED end over the hole in A10's ACUTE corner (the corner 40 and 46 mm from the other
    two holes, which are 20 mm apart). A10's triangle mark is beside another hole, not this one. 9:01-9:17 nothing moves (the right hand is
    away fetching a screw). CAD: A11 on the +Z face of A10 at [193.1, 239.1].
28. **9:20-9:35 6 mm screw (NAUO64), A11 to A10.** Pair turned on edge, screw pressed in by hand from the A11 side (9:20-9:22; head stands about
    3 mm off A11 before driving), driven about 10 s (9:23-9:32). Head on A11's engraved face. PIVOT. CAD: head top [193.07, 239.08, 172.23],
    pointing -Z; free through A11, thread in A10.
29. **9:36-9:47 A12 laid on A10.** A12 (NAUO27) fetched from the left. Its marked end (hole, cut-through triangle, then the code) is laid on
    A10's engraved face over the hole that has A10's triangle mark beside it; the two triangle marks end up next to each other. Engraved
    face up. CAD: at [239.1, 238.7].
30. **9:48-10:16 6 mm screw (NAUO65), A12 to A10.** Set by hand from the A12 side (9:48-9:51), driven about 14 s (9:52-10:06). 10:08-10:16:
    A12 is swung about 60 degrees on its screw with a finger and back (turns freely: PIVOT), then the group is held flat to the camera: A10
    in the middle, A12 at the triangle-marked corner, A11 at the acute corner, both heads up, A10's third (plain) hole still empty. CAD: head
    top [239.08, 238.63, 172.23], pointing -Z.

    *Cut at 10:16.6. The work carries on at 7:10.5 in the video.*

### H. Shoulder Motor side of the turret: 7:10 - 8:52

31. **7:10-7:18 kit turned round.** One hand holds the finished triangle group; the other picks the kit up and puts it down turned 180
    degrees, joysticks now at the bottom of the frame. The upper arm is now raised (somewhere between 30 and 60 degrees above level; a top view
    does not give the angle). The triangle group is laid on the worktop on the +Z side of the kit.
32. **7:18-7:27 Shoulder Motor (NAUO66) fetched; its horn (NAUO67) turned by hand.** Carried over from the far left, lead trailing. Horn
    already on with its hub screw (7:22). At 7:22-7:23 the left fingers turn the horn (the servo is not powered). From 7:24 the right hand
    holds the servo label side up, shaft pointing towards the turret (-Z), horn pointing forward (+X) as seen from above, lead leaving the +X
    end. The white flag near its plug reads "9" (merge check at 7:50-7:51, `merge_flag9_07m50s-07m52s.jpg`: a 9 with a line under it; fairly sure).
33. **7:28-7:37 Shoulder Motor into R6 from outside.** Left hand steadies the turret and the raised upper arm. The servo comes in at an angle,
    HORN LEADING: 7:32.5 horn tip at the cut-out; 7:33 horn through the cut-out and inside the plate while the case is still outside and
    tilted; 7:34-7:37 case squared up and pushed straight in (-Z) until the ears stop on R6's outer face. Label up (+Y), shaft at the +X end of
    the case and pointing inwards, lead out of the +X end, outside R6. The horn goes into the horn-shaped pocket at the shoulder end of bar
    A8; nothing screws it to the wood. From now on A8, and so the whole upper arm, is carried by this servo. CAD: shaft tip
    [175.66, 162.28, 160.85] pointing -Z, ears z 172.23-174.73 on R6's outer face z 172.2, lead leaves at [181.51, 162.28, 188.35] heading
    +X, horn pointing [0.67, 0.74, 0] along the upper arm.
34. **7:38-7:58 clamp plate R7 (NAUO16).** Kit picked up and held tilted, thumb on the servo. R7 picked up and "R7" shown (7:48). The servo's
    plug is passed through R7's window and the plate run along the lead, flag and all (7:50-7:54), slid down onto the back of the servo and
    pressed against the ears (7:55-7:58). Engraved face out (+Z), "R7" in the top front corner (upper edge, arm end), one screw hole above
    and one below the servo. CAD: z 174.74-177.74; moves -Z.
35. **7:59-8:26 first clamp screw, 10 mm (NAUO68), upper hole.** Set by hand (8:06-8:07), seen standing in the hole (8:08-8:09), driven
    8:10-8:21 with the driver level from the +Z side, kit still held tilted. 8:21-8:26: kit laid on its -Z side (R6 / R7 face up) and the screw
    given a few more turns from above. CAD: [170.27, 171.57], head top z 180.75, pointing -Z.
36. **8:27-8:46 second clamp screw, 10 mm (NAUO69), lower hole** (the one nearer the base). Set by hand 8:28-8:30 (both screws visible 8:31,
    one each side of the servo), driven from above 8:32-8:46. CAD: [170.31, 152.98].
37. **8:46-8:52 kit stood upright**, upper screw given a last tighten from the +Z side (8:47-8:49), driver down, hands off. Both FIXED. Seen
    from inside the turret at 8:52: the horn's hub and screw sit in the pocket at the shoulder end of A8.

    *Cut at 8:52.4. The work carries on at 10:16.75 in the video.*

### I. Triangle group fitted on the +Z side: 10:17 - 11:59

38. **10:17-10:23 A11's free end tucked inside R6.** (10:17-10:18 hands off: a clean top view.) The right hand carries the group by the
    triangle with A11 hanging down, plates parallel to R6, engraved faces outwards (+Z). The free (PLAIN) end of A11 is brought DOWN from above
    and tucked behind the lobe on R6's top edge (the lobe on the controller side), flat against R6's INNER face. A11 is therefore inside R6,
    between R6 and bar A8. The left hand lines its hole up with the hole in the lobe. CAD: at [139.4, 179.8], A11 at z 166.2-169.2.
39. **10:24-10:55 turret screw, 6 mm (NAUO70).** Pushed in by hand from OUTSIDE R6 through the hole in the lobe into A11 behind it
    (10:25-10:28), driven about 15 s level from the +Z side (10:31-10:46). PIVOT: when let go at 10:48 the group falls outwards and down
    under its own weight. 10:52-10:53: kit tipped to show A11 coming out from behind R6, head on R6's lobe. CAD: head top
    [139.38, 179.78, 175.23], pointing -Z; free through R6, thread in A11 (the screw turns with A11 inside R6's hole).
40. **10:56-11:15 triangle lined up at the elbow; kit laid on its -Z side.** The right hand lifts A10 to the top end of A8. A13 is picked
    up and moved to the right of the kit (11:00-11:02; not fitted yet). 11:03-11:08: A10's free (plain) corner is pinched against the OUTER
    face of A8's top end while the left hand moves the upper arm to bring the holes into line. 11:09-11:15: kit tipped onto its -Z side so
    R6, R7 and the Shoulder Motor face up; hands swap; A10 held on A8 with the holes in line.
41. **11:16-11:18 A13 laid on.** A13 (NAUO28) is laid with its marked end (hole, cut-through SQUARE, then the code) on top of A10 over the
    elbow hole, engraved face out. Stack at the elbow from the arm outwards: A8, A10, A13.
42. **11:19-11:52 elbow screw on the +Z side, 10 mm (NAUO71).** Dropped through A13 and A10 by hand (11:22-11:25; head on A13 next to the
    square mark), driven straight down (-Z in assembly terms) for about 25 s, much longer than the three short screws (11:27-11:52). A13
    swings on the screw while it is driven; the left hand keeps A10 pinched to A8. PIVOT for both A13 and A10. CAD: head top
    [228.97, 221.31, 172.21], pointing -Z; free through A13 and A10, thread in A8.
43. **11:53-11:59 shown.** Kit stood up, laid over once more with A12 and A13 lifted on one finger (clearest view of the finished linkage,
    every code readable), stood up again; final top view, hands away. End of the video.

### Things that do NOT happen in this video

- No servo lead is routed or plugged in. Lead "6" (Elbow Motor) and lead "9" (Shoulder Motor) are left lying on the worktop from the moment
  each servo is fitted until the end. Neither is in the hook-shaped slot of its side plate.
- No servo is powered, centred or tested. The only horn work is by hand: the lever is swung up (action 21) and the Shoulder Motor's horn is
  turned to suit the raised arm (action 32).
- No horn is fitted to a shaft, taken off, or screwed to wood. No part of the claw is touched.

## 3. State at the end (11:59)

- **Upper arm:** A7 (-Z) and A8 (+Z) on the tabs of A6, each pulled in by a 16 mm screw into an A9. On the -Z side A7 turns on the 6 mm
  pivot screw in R2's ear; on the +Z side A8 sits on the Shoulder Motor's horn. It stands nearly upright and is moved by hand; nothing holds it at
  the CAD's 47.9 degrees.
- **-Z side, outside in:** R8 (two 10 mm screws) over the back of the Elbow Motor; the motor's ears; R5; a gap with the motor's gear housing and
  the horn; lever A3 / A2 / A1 on the horn and on the head of the pivot screw; then A7 with A4 in the same layer; A5 in A1's layer on the
  outside of A4 and A7. Chain: horn -> lever -> (10 mm pivot) -> A4 -> (6 mm pivot) -> A5 -> (6 mm pivot, elbow) -> A7. A5's far hole is empty.
  Every screw head on this side faces -Z.
- **+Z side, from the arm outwards:** A8; A10 (0.76 mm clear of A8 in the CAD, pressed against it on video); A11, A12 and A13 all in the next
  layer; R6 outside A11's lower end; the Shoulder Motor's ears on R6; R7 with two 10 mm screws. Pivots: R6 lobe to A11 (6 mm), A11 to A10
  (6 mm), A12 to A10 (6 mm), A13 + A10 to A8 (10 mm, elbow). The far holes of A12 and A13 are empty. Every screw head on this side faces +Z.
- **Free ends waiting for the claw:** A5 (-Z), A13 and A12 (+Z). CAD: screws NAUO79, NAUO78, NAUO77.
- **Leads:** base motor "5" plugged in as at the start. Elbow Motor "6" and Shoulder Motor "9" loose on the worktop, plugs free. (At the start
  of Claw.mov three servo leads are already in the shield, so these two were plugged in off camera between the two videos; see section 5.)
- **Left over:** nothing of the arm. Driver on the worktop. No claw parts in view.

## 4. Proposed guide steps for the arm section (house style)

How to read this list.

- Numbers are local to the section ("Arm 1"); in the Full Build they carry on from the last controller step. Each is a `Step N` (part
  hovering, lead lines, label) and a `Step Nc` (in place), camera fixed inside the pair.
- **Bench groups.** Four groups are built in the hand on video: the upper arm, the lever, the link pair A4 + A5 and the triangle group. They
  are proposed the way `guide.py` already does the joystick groups: built on their own (`staged=True`), then seated as one (`g.seat`).
  Each group is built immediately before it is fitted (rulebook section 3: preparation comes immediately before first use). That moves two
  blocks compared with the real order on video: the link pair is built after R8 instead of before the lever goes in, and the triangle group
  after the Shoulder Motor instead of before it (which is also where the cut video shows it). Nothing depends on either choice; to follow the
  real order exactly, move steps 17-18 to before step 12 and steps 26-29 to before step 22.
- **Screws.** No joint in this section has three or more identical screws, so "one shown, then the rest" never applies. The two clamp screws on
  each plate use the base screws' wording ("... with two 10mm screws." / "Add the second ..."). Screw travel is set by hand (`direction=`,
  `axial=True`) as for the base screws. Captions use "6mm / 10mm / 16mm screw"; hover names are "6mm / 10mm / 16mm Hex Screw".
- **Motion** is the travel from hover to seat, in assembly space. "free" = tested for this report with `stepgen.blocked` on the CAD meshes
  against everything fitted by then (same settings as the generator); "hand" = no straight path exists, set a path by hand with a Review note.
- All coordinates are the CAD's one pose (upper arm 47.9 degrees above level, lever 24 degrees above level pointing back). See section 5,
  items 13-15, for where that pose disagrees with what the builder does.

| # | caption (draft) | appears / moves | motion and notes |
|---|---|---|---|
| 1 | Begin the arm with A6. Press A7 onto the two tabs on the edge of A6 nearest its code, engraving facing out. | appears NAUO29 (A6); moves NAUO23 (A7) | Bench. +Z [0, 0, 1], face-on; free. 2 lead lines, tab tips [195.4, 184.1, 126.4] and [214.2, 204.9, 126.4] into A7's slots. Right way round: the "A" of "A7" at the same end as the "A6" code (A7's two end holes differ: 2.8 mm at the shoulder, 2.3 mm at the elbow). |
| 2 | Push an A9 into the cross-shaped slot next to A7, from the engraved side of A6. | moves NAUO30 (A9) | Bench. [0.74, -0.67, 0] (along A6's normal, stem first); free with A7 already on. 1 line, stem to the window at [200.7, 190.0, 138.0]. |
| 3 | Screw A7 to the A9 with a 16mm screw. | moves NAUO53 | Bench. +Z, along the slot in A6; head ends at [200.72, 189.99, 123.54]. Fixed. Label "16mm Hex Screw". |
| 4 | Press A8 onto the other two tabs of A6, engraving facing out, with its long slot at the end away from the A6 code. | moves NAUO24 (A8) | Bench. -Z [0, 0, -1]; free. 2 lines, tabs [195.4, 184.1, 162.6] and [214.0, 204.8, 162.6]. |
| 5 | Push the second A9 into the other cross-shaped slot. | moves NAUO31 (A9) | Bench. [0.74, -0.67, 0]; free. Window at [208.7, 198.9, 151.0]. |
| 6 | Screw A8 to the second A9 with a 16mm screw. | moves NAUO54 | Bench. -Z; head ends at [208.73, 198.86, 165.45]. Fixed. |
| 7 | Lower the arm over R2, with A7 against the engraved side of R2 and A8 on the other side. | moves NAUO23, 24, 29, 30, 31, 53, 54 as one | -Y [0, -1, 0]; free (also free along +X and along the arm). R2's ear (top y 167.9, z 129.55-132.55) goes between A7 and A8. On video the frame is angled in from the front and then lies forward on the end wall; here it would arrive, and stay, at 47.9 degrees (section 5, item 13). |
| 8 | Screw A7 to R2 with a 6mm screw, through the opening in R5. Stop when the head touches A7: the arm must still swing. | moves NAUO55 | +Z, starting OUTSIDE R5 and passing through its servo opening (x 158.9-182.7, y 156.1-168.4); axis [175.35, 161.84], head ends at z 123.52. Camera from the -Z side. Pivot. Must come before the Elbow Motor. |
| 9 | Stack A2 on A1, codes facing the same way and notches together... | appears NAUO18 (A1); moves NAUO19 (A2) | Bench. +Z, face-on; free. The keyhole of A2 goes over the large hole of A1. |
| 10 | ...then A3 on A2. | moves NAUO20 (A3) | Bench. +Z, face-on. A3 is the layer with the larger end hole; it ends up facing R5. |
| 11 | Screw A1 - A3 together with a 10mm screw in the middle hole. | moves NAUO56 | Bench. +Z from the A3 face; head ends at [158.64, 169.43, 114.54], proud of A3. Fixed. |
| 12 | Slide A1 - A3 down between R5 and A7, with A3 facing R5, until the large hole in A1 sits over the screw in A7. | moves NAUO18, 19, 20, 56 as one | **hand.** Blocked in every straight direction in the CAD pose. A path that works in the CAD (`cad_arm_claw.md` 7.4, M3a / M3b): lever turned 66 degrees up about the shoulder axis [175.66, 162.28] so its long end points straight up, 3.2 mm to the -Z side of its seat, lowered -Y; pushed 3 mm +Z so A1's 5.7 mm hole goes over the head of NAUO55; swung back down. On video it is slid in from the top, keyhole end first. Nothing fastens it. Review note. |
| 13 | Angle the elbow motor's servo horn through the opening in R5 and into the slot in A2 and A3, then push the motor in. | moves NAUO58 + NAUO59 as one, lead NAUO88 and plug NAUO84 riding loose | **hand.** Straight -Z pull-out is blocked with the horn on (free without it): the horn tip ends at x 192.4, 9.7 mm past the end of the opening. Real motion: servo tilted, horn through first at the end away from the controller, levelled, pushed +Z until the ears (z 106.48-108.98) are on R5 (z 109.0). Same kind of path as the base motor's horn through R1. Shaft inwards, lead end towards +X, outside R5. Label "Elbow Motor". |
| 14 | Pass the elbow motor's wire through R8, then slide R8 over the back of the motor. | moves NAUO17 (R8) | +Z onto the ears (R8 ends at z 103.46-106.46), engraved face out, "R8" at the top, controller end. With the full servo mesh the slide tests as blocked (probably the rigid lead stubs and the label plate; `cad_arm_claw.md` found it free against case and shaft only), so set the direction by hand. The loose lead must be posed through R8's window (section 5, item 16). |
| 15 | Screw R8 onto R5 with two 10mm screws. | moves NAUO60 | +Z; upper hole [170.31, 171.58], head ends at z 100.45. Beside the motor, not through its ears. Fixed. Close up, as for the first base screw. |
| 16 | Add the second 10mm screw. | moves NAUO61 | +Z; lower hole [170.31, 152.93]. Fixed. |
| 17 | Place the coded end of A5 on the plain end of A4. | appears NAUO21 (A4); moves NAUO22 (A5) | Bench. +Z, face-on (A5 lies on the -Z, engraved, face of A4) at [197.05, 235.70]. Both engravings face the same way. |
| 18 | Screw A5 to A4 with a 6mm screw. Stop when the head touches A5: it must still swing. | moves NAUO57 | Bench. +Z; head ends at [196.99, 235.71, 120.52]. Pivot. |
| 19 | Fit A4 and A5: the coded end of A4 goes against the inside of A1, and the middle hole of A5 over the end of A7. | moves NAUO21, 22, 57 as one | -Y; free (also free along [-0.74, 0.67, 0] and along the arm; blocked along Z both ways, because A4 is behind the lever and A5 in front of A7). A4's hole to the lever's top hole [143.44, 176.32]; A5's middle hole to A7's end hole [228.94, 221.29]. On video A4 is hung on the screw first with the lever upright, and A5 swung up afterwards (actions 21-24). |
| 20 | Screw A1 - A3 to A4 with a 10mm screw through the large hole in A3. It must still swing. | moves NAUO62 | +Z from the -Z side; head ends SUNK in A3 at [143.47, 176.30, 117.54]. Pivot. In the CAD pose the head (y 173.57-179.07) overlaps R5's top edge (y 175.38) by 1.8 mm as it travels in from outside R5; on video the lever is swung upright first (section 5, item 14). |
| 21 | Screw A5 to the end of A7 with a 6mm screw. It must still swing. | moves NAUO63 | +Z; head ends at [228.88, 221.29, 120.52], on A5. Pivot (the elbow, -Z side). |
| 22 | Angle the shoulder motor's servo horn through the opening in R6 and into the slot in A8, then push the motor in. | moves NAUO66 + NAUO67 as one, lead NAUO89 and plug NAUO86 riding loose | **hand.** Blocked straight with the horn on (free without it): the horn points along the upper arm and overhangs the opening by about 7 mm. Real motion: tilted, horn first, squared up, pushed -Z until the ears (z 172.23-174.73) are on R6 (z 172.2). Label up, shaft inwards, lead end towards +X, outside R6. Camera from the +Z side. Label "Shoulder Motor". |
| 23 | Pass the shoulder motor's wire through R7, then slide R7 over the back of the motor. | moves NAUO16 (R7) | -Z onto the ears (R7 ends at z 174.74-177.74), engraved face out, "R7" at the top, arm end. Same note as step 14. |
| 24 | Screw R7 onto R6 with two 10mm screws. | moves NAUO68 | -Z; upper hole [170.27, 171.57], head ends at z 180.75. Fixed. |
| 25 | Add the second 10mm screw. | moves NAUO69 | -Z; lower hole [170.31, 152.98]. Fixed. |
| 26 | Place the coded end of A11 on the pointed corner of A10. | appears NAUO26 (A10); moves NAUO25 (A11) | Bench. -Z, face-on, onto A10's engraved face at [193.1, 239.1]; free. Not the corner with the triangle mark. A11's coded end has the 2.8 mm hole; reversed it does not work. |
| 27 | Screw A11 to A10 with a 6mm screw. It must still swing. | moves NAUO64 | Bench. -Z; head ends at [193.07, 239.08, 172.23]. Pivot. |
| 28 | Place A12 on A10 so that the two triangle marks meet. | moves NAUO27 (A12) | Bench. -Z, face-on, at [239.1, 238.7]; free. |
| 29 | Screw A12 to A10 with a 6mm screw. It must still swing. | moves NAUO65 | Bench. -Z; head ends at [239.08, 238.63, 172.23]. Pivot. |
| 30 | Lower the plain end of A11 inside R6, behind the hole in its raised corner, with A10 on the outside of A8. | moves NAUO25, 26, 27, 64, 65 as one | -Y; free (also free along -X and along the arm; blocked +Z). A11's end goes between R6 (inner face z 169.2) and A8, its hole behind R6's lobe hole [139.4, 179.8]; A10's plain corner lies on A8's elbow end [228.94, 221.29]. The hole in A11 is hidden behind R6: the lead line has to end on R6's hole. |
| 31 | Screw R6 to A11 with a 6mm screw, from the outside of R6. It must still swing. | moves NAUO70 | -Z; head ends at [139.38, 179.78, 175.23], on R6's lobe. Pivot (free through R6, thread in A11). |
| 32 | Place the end of A13 with the square mark on A10, over the hole at the top of A8. | moves NAUO28 (A13) | -Z, face-on; free. Stack at the elbow from the arm outwards: A8, A10, A13. |
| 33 | Screw A13 and A10 to A8 with a 10mm screw. Both must still swing. | moves NAUO71 | -Z; head ends at [228.97, 221.31, 172.21], on A13. Pivot (the elbow, +Z side). |
| 34 | Move the elbow motor's wire into the hook-shaped slot in R5. | lead NAUO88 | NOT ON VIDEO. Slot mouth on the front edge of R5's lug (x 117.66, y 166.25-168.54); the lead sits in the drop at [123.54, 163.40, 110.50]. Eye on the slot, as for the base motor's wire in R4. |
| 35 | Reconnect the elbow motor to 6. Remember brown to G, red to V, and orange to S. | plug NAUO84, lead NAUO88 | NOT ON VIDEO. Row 6 of the digital header (z 142.0; G / V / S at x 50.09 / 52.57 / 55.06, pin tops y 113.8). Label "6". |
| 36 | Move the shoulder motor's wire into the hook-shaped slot in R6. | lead NAUO89 | NOT ON VIDEO. Same slot outline in R6; the lead sits at [123.53, 163.42, 170.70]. |
| 37 | Reconnect the shoulder motor to 9. | plug NAUO86, lead NAUO89 | NOT ON VIDEO. Row 9 (z 152.01). Label "9". |

Counts: 33 steps from the video (18 wood or motor placements, 15 screws) and 4 wire steps from the CAD and the house rule for servos
(lead loose while parts go on, into its slot in its own step, plugged in at the end of the section).

Steps the video has and this list leaves out, on purpose: laying the kit on its side or turning it round (a camera change in the guide);
swinging the lever upright before step 20 (only needed if the lever is to be shown out of the CAD pose; section 5, item 14); the builder's
motion checks (7:07, 10:08, 10:48). A single "check that the arm, the lever and the links all swing freely" note card after step 33 would
stand in for the checks.

## 5. Uncertain, contradictory, or where the CAD may not match

Disagreements between the segment reports, and how each was settled:

1. **Order of work (segments 3 and 4).** Settled by the merge: the video is cut out of order (section 0). Segment 4's start state is wrong
   for 9:00-10:16 and its "fourth servo" is the Shoulder Motor.
2. **Does the loose servo seen from 2:47 have a horn? (segments 1 and 3).** Segment 1: no horn. Segment 3: horn on when picked up. Merge
   check: a black hub is on the shaft at 2:48; the horn arm cannot be seen either way at that size; the horn and its screw are plainly on at
   7:21-7:22, two seconds after pick-up. Taken as "on throughout", not proven for 2:47.
3. **A4 or the screw first at the top of the lever (segments 2 and 3).** Merge check: the screw is started through the lever at 6:06-6:07
   while A4 is still held flat beside it; A4 goes onto the tip at 6:08-6:09. Both agree on the result: A4's CODED end on the INNER face of A1,
   engraved face against the lever, screw from the R5 side.
4. **Horn screw on the Elbow Motor (segment 2 could not see one).** Merge check: a small screw head is in the horn hub at 4:28
   (`merge_horn_screw_elbow_04m28s.jpg`). Both side servos have one.
5. **Flag on the Shoulder Motor's lead (segments 3 and 4: "9, not certain").** Merge check at 7:50-7:51: one digit with a line under it,
   loop at the top with the line below, so 9. Fairly sure, not certain. The CAD puts this servo on row 9 and the 6 is on the other lead.

Not shown in this video (so not known from it):

6. **Fitting the horns and centring the servos.** All four servos in the four videos arrive with a horn pressed on and screwed. Nothing in
   Arm.mov says at what servo angle each horn should sit. On video the builder simply turns each servo by hand to suit the wood (actions 21
   and 32). If the horn angle matters for the arm's range of travel, that instruction has to come from an earlier chapter or from Lee.
7. **How loose a pivot screw is left.** Eight of the fifteen screws are pivots (NAUO55, 57, 62, 63, 64, 65, 70, 71), and the lever also turns
   on the head of NAUO55 with no screw of its own; the seven fixed ones are NAUO53, 54, 56, 60, 61, 68, 69. Each pivot screw is driven until it
   stops turning easily; none is seen being backed off; every joint swings freely straight afterwards. "Tighten, then check it still swings"
   is the most the video supports. The captions in section 4 say so in words; Lee should confirm the wording.
8. **How the shoulder pivot screw NAUO55 is started** (2:15-2:20): fingers hide it. Either passed in through R5's servo opening or dropped in
   from above between R5 and A7 (the gap is 14.6 mm, the screw 9 mm long). It is driven through the opening for certain.
9. **Screw lengths.** Not measurable on video. What can be seen: two long ones in the upper arm; the lever screw stands about 4 mm proud after
   dropping 6 mm; the clamp screws' shanks are about twice the head diameter; the last elbow screw takes about twice as long to drive as the
   three before it. All of that fits the CAD's 16 / 10 / 6 mm, which is what this report uses.
10. **Routing and plugging of leads "6" and "9".** Never done in Arm.mov. At the start of Claw.mov three servo leads are already in the shield
    (`video_claw_seg1.md`), so it happened off camera. The routes in section 4, steps 34-37, are the CAD's (`cad_wire_paths.md` 3.3, 3.4).
    The only video hint is in Claw.mov at 6:56, where fingers pinch the +Z servo's lead at R6's front lug (`video_claw_seg3.md`, a guess there).
11. **The first clamp screw finished at 5:41-5:49** is taken to be the upper one (NAUO60) because the driver passes over the servo; fairly sure.
    R8's lower screw is hidden in every later view, but both heads are seen at 5:29-5:30.
12. **Which way the first A9's code faces** (towards A7, fairly sure). The CAD has both A9 codes facing +Z. The piece is symmetric.

Where the video and the CAD (one pose, rigid parts) do not match, or the CAD cannot show what is done:

13. **Upper-arm pose.** After the pivot screw the real arm lies forward on the front end wall until the Shoulder Motor is fitted, 14 steps
    later in section 4; then it is raised by hand (30 to 60 degrees) to meet the horn. The CAD has it at 47.9 degrees throughout, so from
    step 8 to step 22 the guide's arm would stand in mid-air on one screw. Options: accept it; rest the arm forward until step 22 (a second
    pose); or fit the Shoulder Motor and R7 straight after step 8 (nothing on the +Z side waits for the -Z side; the video does it later).
14. **The lever-top screw NAUO62 and R5's top edge.** In the CAD pose the screw's head overlaps R5's top edge by 1.8 mm on its way in
    (head y 173.57-179.07, edge y 175.38), which is why the builder swings the lever upright first. Raising the lever by 3 to 4 degrees
    clears it. Options: accept the graze (no tool is drawn); show the lever a few degrees higher; or add a hand-action step "Swing A1 - A3
    upright" before step 19 and show A4 + A5 hanging, as on video (then the linkage has to return to the CAD pose later).
15. **The lever cannot reach its seat by a straight move** (step 12), and in the CAD pose it has 2.55 mm of sideways room where it needs 3.0;
    it only goes on when swung 40 to 90 degrees up. On video it goes in from the top with the kit on its side; the lever's exact angle then
    cannot be read. The CAD shows concentric hole, screw head and horn, which is what is seen through R5's opening at 4:17-4:21.
16. **Clamp plates over the lead.** R8 and R7 are threaded over the plug and slid down the lead. In the CAD each servo has three rigid 3 mm
    lead stubs that leave the +X end face 10.6 mm outside the clamp plate's outer face and reach x 184.58, past the window edge at x 181.9,
    so a rigid plate cuts through them; `blocked` reports the slide as blocked with the full servo mesh. The loose lead in the guide has to be
    posed through the window (for example straight out along -Z for the Elbow Motor, +Z for the Shoulder Motor).
17. **R8's notch.** `cad_arm_claw.md` asks which way round the real R8 goes, because the CAD has its 1 x 8 mm notch at the end away from the
    lead. On video "R8" is on the long side nearest the turret top, at the controller end (segment 2; also visible in `t06m47s.jpg`), and
    "R7" is at the top, arm end. R7 and R8 are the same plate engraved on one face, so that puts R8's notch at the controller end, away from
    the lead, as the CAD has it. The notch itself was not seen on video.
18. **Horn screws are not in the CAD.** Each horn hub has a screw on video. On the -Z side the horn hub ends at z 122.1 and the head of the
    pivot screw NAUO55 starts at z 123.55, both inside the lever: 1.45 mm for the horn screw's head. Nothing looked tight on video.
19. **Order against the CAD-derived order** (`cad_arm_claw.md` 7): on video the A9 nuts go in AFTER each bar is on the tabs (CAD: before);
    the horns stay on the servos (CAD: laid in the wood first); A4 + A5 are joined on the bench and A4 is screwed to the lever on the kit
    (CAD: A4 to the lever on the bench, A5 added on the kit); the turret screw NAUO70 goes in BEFORE A13 and the elbow screw NAUO71 (CAD:
    last). All of the video's choices test as free in the CAD.
20. **Floppy linkage.** After NAUO70 the triangle group hangs down from A11; A12, A13 and A5 hang or swing until the claw is fitted. The CAD
    holds them at one attitude. The CAD also has 0.76 mm of air between A10 and A8 at the elbow; on video A10 is pressed against A8.
21. **Hidden joints.** A11's lower hole is behind R6 (step 31); A8's elbow hole is under A10 and A13 (step 33; lined up by feel, which took
    from 10:56 to 11:15); the horn meets its pocket blind on both sides (steps 13, 22).
22. **Marks to keep in the model.** The cut-through triangle on A10 (4.0 mm) and A12 (3.3 mm), the square on A13 (2.6 mm) and the edge
    notches on A1, A2, A3 are what the student lines up. `model.glb` must keep them and the camera must be close enough to show them.
23. **The base motor's lead comes up between the two bars of the upper arm** (2:44-2:48); the frame is lowered round it. In the CAD the base
    lead stays low in the turret (y 119 to 134) and the arm's lowest point is y 153, so they do not meet there.
24. **Servo labels.** Both side servos show a pink label on the face turned up (+Y) once fitted (Shoulder Motor: segment 3 and `t11m55s.jpg`,
    with a plain white sticker across it; Elbow Motor: looks the same way in `t06m47s.jpg`, dark centre). Two servos mounted as mirror images
    can only both show a label upwards if both broad faces carry one. Not checked against where the CAD puts the label plate.
25. **Joystick sides.** B8 is engraved "Shoulder" / "Base" at the student's left stick and "Elbow" / "Claw" at the right; the Elbow Motor is on
    the student's left side of the turret and the Shoulder Motor on the right. Not an error, but the motor on a side is not the one named on that side.
26. **Driver size.** The handle is printed "3.0"; M3 socket-head screws normally take a 2.5 mm key. Not resolved; no tool is drawn in the guide.

## 6. Reference stills

All in `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/arm/`. Timestamps are the video's own. Numbers 1 to 48 are the
segment studies' stills (720 x 1280).

1. `t00m00s.jpg` - start: loose arm parts with codes R8, A9, A6, A8, A7, A13, A11, A12, A10; controller end of the base at the top left.
2. `t00m17s.jpg` - A7 on A6's tabs; an A9 (code readable) about to go into the cross slot.
3. `t00m23s.jpg` - first 16 mm screw pushed by hand through A7, along the slot, into the A9.
4. `t00m52s.jpg` - outside of A7: code, screw head by the "7", the A9's code facing A7, "A6" at the "A" end.
5. `t00m59s.jpg` - A8 pressed onto the other pair of tabs, loop-slot end visible.
6. `t01m38s.jpg` - finished H-frame from the engraved side: two screws, two staggered A9.
7. `t01m53s.jpg` - turret before the arm: R1 floor, R2's ear, R5's empty servo opening, base motor lead leaving over the end wall.
8. `t02m04s.jpg` - H-frame just lowered into the turret, loop end inside, "A6" at the free end.
9. `t02m26s.jpg` - shoulder pivot screw being driven, driver shaft through R5's servo opening.
10. `t02m44s.jpg` - pivot screw head on A7 at R2's ear ("R2", "R5" readable); A1, A2, A3 laid out with their holes.
11. `t03m04s.jpg` - A1 / A2 / A3 stacked, screw standing in the middle hole on the A3 face; A3's larger end hole.
12. `t03m05s.jpg` - the same a second later (segment 2's copy): screw in the middle hole of A3, three layers.
13. `t03m15s.jpg` - three layers edge-on, empty keyhole pocket, screw nearly home; H-frame on the turret and the loose servo at the top left.
14. `t03m24s.jpg` - finished lever: large end hole, "A3", screw head, keyhole pocket; A10 to A13 loose at the left.
15. `t03m32s.jpg` - A5 (three holes) and A4 (two holes) side by side, codes readable.
16. `t04m00s.jpg` - A4 and A5 joined as an L, screw head on the coded end of A5, A5 on top.
17. `t04m13s.jpg` - kit on its side, R5 up; lever held with A3 towards R5 before it goes in.
18. `t04m18s.jpg` - lever in place seen through R5's servo opening: its screw head and the rings of the pivot.
19. `t04m36s.jpg` - Elbow Motor with the single-arm horn on its shaft, about to go into R5.
20. `t04m43s.jpg` - Elbow Motor seated in R5, lead leaving the end away from the controller, lever end "A3" sticking out past R5.
21. `t04m50s.jpg` - clamp plate R8 threaded on the lead; black flag "6".
22. `t05m30s.jpg` - R8 on the servo with both clamp screws in, one each side of the case; "R5", "R8" readable.
23. `t05m59s.jpg` - kit upright; lever being swung upright by hand; lead "6" loose at the lower left.
24. `t06m00s.jpg` - lever on the Elbow Motor, A4 + A5 pair in the hand, A13 and A10 loose, flag "6".
25. `t06m06s.jpg` - A4 beside the top of the lever, screw about to go in from the servo side.
26. `t06m07s.jpg` - a second later: A4's coded end at the lever top, screw pushed in from the R5 side.
27. `t06m34s.jpg` - hands off after the lever-top screw: lever, A4 and A5 hanging; screw tip through A4.
28. `t06m47s.jpg` - the -Z side face-on: R5, R8 (code at the top, controller end), A3 with a sunk and a proud screw head, A4, A7, an A9, lead "6".
29. `t06m56s.jpg` - elbow: 6 mm screw standing in A5's second hole over the end of A7, before driving.
30. `t07m26s.jpg` - kit turned round; Shoulder Motor with its horn in the hand; triangle group (A10, A11, A12) beside the kit.
31. `t07m33s.jpg` - horn already through the cut-out in R6 while the servo case is still outside and tilted.
32. `t07m48s.jpg` - clamp plate with "R7" readable, Shoulder Motor seated in R6, white flag on its lead.
33. `t07m55s.jpg` - R7 threaded on the lead and being slid down onto the back of the servo.
34. `t08m31s.jpg` - kit on its side: "R6", "R7", both clamp screws, one each side of the servo.
35. `t08m52s.jpg` - both side servos fitted, horn in A8's pocket seen from inside, both leads loose (the frame before the cut back in time).
36. `t09m00s.jpg` - (earlier in real time) A10 with A11 on its acute corner; kit with NO servo in R6; A13 and flag "6" on the worktop.
37. `t09m01s.jpg` - a second later: A11 on A10's sharp corner, triangle mark at another corner.
38. `t09m10s.jpg` - A10 close up: three holes, the triangle mark, A11 on the engraved face.
39. `t09m23s.jpg` - 6 mm screw going in from the A11 side, head 3 mm proud; also the -Z side stack (lever layers, R5, servo).
40. `t09m41s.jpg` - A12's triangle-marked end being brought to A10's triangle-marked hole.
41. `t10m12s.jpg` - triangle group flat: A10, A11, A12, two screw heads, third hole empty.
42. `t10m17s.jpg` - first frame after the cut forward: kit turned round, hands off, both side servos fitted, loose leads.
43. `t10m28s.jpg` - 6 mm screw pushed in from outside R6; A11 inside R6.
44. `t10m53s.jpg` - kit tipped to show the +Z side: A11 behind R6, screw head on R6's lobe, codes A11 / A10 / A12 / A6 / R6, flag "6".
45. `t11m10s.jpg` - kit on its -Z side: A10 held over the top of A8, elbow hole still empty; R7, R6, the Shoulder Motor and its lead.
46. `t11m26s.jpg` - A13 on the elbow with the screw set in; square mark on A13, triangle marks on A12 and A10.
47. `t11m55s.jpg` - finished linkage from the +Z side, every code readable (A8, A10, A11, A12, A13, R6, R7 at the top arm end, A9 inside).
48. `t11m58s.jpg` - end of the video, top view: both sides of the arm, leads still loose.

Added by the merge (contact sheets and enlarged crops from native frames):

49. `merge_cut_07m08s-07m13s.jpg` - the cut at 7:10: at 7:11 a hand already holds the finished triangle group; kit turned round at 7:12-7:13.
50. `merge_cut_08m50s-08m55s.jpg` - the cut at 8:52: both servos fitted at 8:52, no servo in R6 and a loose servo at 8:53.
51. `merge_cut_10m14s-10m19s.jpg` - the cut at 10:16: early state with the triangle group in the hand, then the state of 8:52 again.
52. `merge_a4_on_lever_06m06s-06m09s.jpg` - screw started through the lever top while A4 is still held flat, then A4 on its tip.
53. `merge_horn_screw_elbow_04m28s.jpg` - Elbow Motor's horn with the small screw in its hub.
54. `merge_elbow_motor_horn_04m33s-04m37s.jpg` - Elbow Motor turned over R5: horn along the case, pointing past the shaft end.
55. `merge_horn_screw_shoulder_07m21s-07m25s.jpg` - Shoulder Motor's horn and hub screw; the horn being turned by hand.
56. `merge_flag9_07m50s-07m52s.jpg` - the white flag on the Shoulder Motor's lead, read as an underlined 9.
57. `merge_loose_servo_02m48s-10m13s.jpg` - the loose Shoulder Motor at five times between 2:48 and 10:13: a black hub on its shaft.

## Method

Segment reports read in full; overlaps (3:00-3:15, 6:00-6:15, 9:00-9:15) merged so each action appears once. Own frames, 1 s apart at
native 1080 x 1920: 2:45-3:15, 4:22-4:37, 6:03-6:12, 7:06-7:27, 7:50-7:54, 8:48-8:56, 10:12-10:20, 11:57-11:58. Slide tests for section 4
used `stepgen.blocked` with the generator's defaults on the arm meshes that the segment 2 study had saved from `mra.glb`; R5's top edge and
R6's lobe were measured by ray casts on the same meshes. Nothing in the project was changed apart from this file and the nine
`merge_*.jpg` stills.
