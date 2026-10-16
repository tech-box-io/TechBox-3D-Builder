# Arm.mov, stretch 1 (0:00 to 3:15): H-frame built, hung on the turret, lever stack started

Status: COMPLETE for this stretch.

Video: `/Users/lee-johnson/Desktop/Claude_Cadasio/MRA_Videos/Arm.mov` (12:00 long, 1080 x 1920 portrait). This report covers seconds 0 to 195,
read at 2 s spacing (overview) and then every second at native resolution, with zoomed crops where a code or a screw had to be read.
Timestamps are the video's own. Nothing in the CAD was re-measured for this report; CAD numbers quoted here come from
`cad_arm_claw.md`, `cad_codes_base.md` and `mra_instances.json`.

## Names used

Codes are the ones ENGRAVED on the wood, as read in the video. They do not match the CAD mesh names:

| engraved (video) | CAD id | CAD mesh name | what it is |
|---|---|---|---|
| A6 | NAUO29 | ARA_A11 | cross plate of the upper arm (two square holes, two cross-shaped slots, two tabs on each long edge) |
| A7 | NAUO23 | ARA_A5 | side bar of the upper arm, -Z side (hole at each end, two rectangular slots, centre hole) |
| A8 | NAUO24 | ARA_A6 | side bar of the upper arm, +Z side (as A7, but a teardrop-shaped loop slot in place of one end hole: the servo-horn pocket) |
| A9 (two) | NAUO30, NAUO31 | ARA_A12 | T-shaped wooden nuts, one hole each |
| A1 | NAUO18 | ARA_A1 | lever layer with one large round hole |
| A2 | NAUO19 | ARA_A2 | lever layer with a keyhole slot |
| A3 | NAUO20 | ARA_A2_Supplement | lever layer with a keyhole slot and a larger end hole |
| R2 | NAUO11 | ARA_R2 | middle wall of the turret, with the ear the arm pivots on |
| R5 | NAUO15 | ARA_R6 | tall side wall at -Z (z = 110.5) |
| R6 | NAUO14 | ARA_R5 | tall side wall at +Z (z = 170.7); code not read in this stretch, named by elimination |
| R8 (+ one more frame plate) | NAUO17 (, NAUO16) | ARA_R8 (, ARA_R7) | servo clamp plates; loose throughout this stretch |

Read directly in the video: A1, A2, A3, A6, A7, A8, A9, A10, A11, A12, A13, R1, R2, R5, R8, B8 (all sure). Not seen at all in this stretch: A4, A5.

Directions: the controller is at -X, the arm reaches out towards +X; wall R5 is -Z, wall R6 is +Z (checked against the video: "R5" is on the wall the driver passes
through, and the screw goes from that side into R2, which is what the CAD has for NAUO55).

## 1. State at the start (0:00)

- Base and controller are finished and stand at the top left, mostly out of frame (only the joystick panel end shows; labels "Base", "Claw", "Elbow" readable). Seen whole from
  1:44: base plate with its M3 screws, turret box with floor R1 ("R1" readable on the floor at 1:46-1:53), middle wall R2 with its ear (one hole near the top of the ear),
  tall side walls R5 and R6 each with an EMPTY rectangular servo opening, both end walls, the base servo in the turret floor (dark body, red label).
- The base servo's lead (brown / red / orange, white flag printed "5") is already plugged into the shield; it comes up out of the turret on the R6 side of R2 and passes over the
  top of the controller-side end wall next to its hook-shaped notch. Nano on the shield, both joystick ribbons plugged in, joystick panel B8 fitted.
- Nothing of the arm is on the turret: no side servos, no clamp plates, no arm parts.
- Loose on the worktop, left side: two rectangular frame plates (one reads "R8"; the other is half out of frame), one "A9" T piece (the second is out of frame), cross plate
  "A6", bars "A8" and "A7", links "A13" (has a small square hole near one end), "A11", "A12" (triangle mark by one end hole), triangular plate "A10" (triangle mark by one corner).
- T-handle hex driver at the top right (handle marked "3.0" in white, read at 3:12 and 3:17). Screws are kept out of frame to the right; the builder reaches for each one.

## 2. Timeline

Sub-assembly A: the H-frame of the upper arm, built in the hand (0:02 - 1:38)

1. **0:02-0:06** Cross plate A6 picked up in the left hand, engraved face up.
2. **0:06-0:14** Bar A7 picked up in the right hand and pressed sideways onto the two tabs on the long edge of A6 that is nearest the "A6" code; the tabs enter A7's two
   rectangular slots. A7 stands at right angles to A6, engraved face OUTWARDS (away from A6). The "A" of "A7" is at the same end as the "A6" code (seen at 0:12 and 0:52).
3. **0:15-0:19** First T piece A9 picked up (code read at 0:17) and pushed, stem first, down into the cross-shaped slot nearest A7, from the ENGRAVED side of A6. It stands
   square to A6, long edge parallel to A7, about 10 mm in from A7. Its code faces A7 (seen at 0:22 and 0:52; fairly sure).
4. **0:21-0:50** One long socket-head screw (M3x16: NAUO53) pushed by hand through the hole in the middle of A7 from the outside face, along the arm of the cross slot that
   runs out to that edge, into the hole in the A9 piece (0:22-0:26). Driven with the T-handle hex driver from 0:27 to 0:49 until the head is down on A7. Fixed joint, fully tight.
5. **0:52-1:01** Assembly turned round in the hand. Bar A8 picked up (code read at 0:56-0:57) and pressed onto the two tabs on the other long edge of A6, engraved face
   OUTWARDS. Its loop-slot end is at the end of the frame AWAY from the "A6" code (seen at 0:58-1:01 and 1:10).
6. **1:02-1:06** Second T piece A9 picked up and pushed, stem first, into the second cross slot (the one nearer A8), again from the engraved side of A6.
7. **1:10-1:38** Second M3x16 screw (NAUO54) through the centre hole of A8 from the outside, along the slot, into the second A9: by hand 1:10-1:16, hex driver about
   1:18-1:37. Fixed joint, fully tight. At 1:38 the H-frame is complete: the two screws enter from the two outer faces, one from each side; the two A9 pieces stand on the
   engraved face of A6, staggered along the frame (the one screwed from A7 is nearer the loop-slot end); each screw tip shows 1-2 mm past its T piece.

Fitting the H-frame to the turret (1:39 - 2:39)

8. **1:39-1:53** Driver put down, H-frame laid on the worktop, base + controller assembly pulled into frame and turned (controller to the right, turret to the left).
9. **1:54-2:10** H-frame picked up and turned end for end (1:55-1:57) so that the loop-slot end of A8 leads and the engraved face of A6 is up. Base turned so the turret end
   points at the builder's left hand (2:01-2:02). Frame angled in from the front, over the end wall that faces away from the controller, leading end going down into the open
   top of the turret (2:02-2:04): A7's end goes down flat against the engraved face of R2's ear (the face towards wall R5); A8's loop-slot end goes down on the other side of
   R2, close to the inside of wall R6. The frame straddles R2 and the base servo's lead comes up between the two bars. 2:05-2:10: left hand holds the frame, right-hand
   fingers line A7's end hole up with the hole in R2's ear.
10. **2:11-2:21** One short socket-head screw (M3x6: NAUO55) fetched (2:11-2:13), brought to the outside of wall R5 at its servo opening (2:14) and started with the fingers
    through A7's end hole into the hole in R2's ear (2:15-2:20; the hand hides exactly how the fingers reach it). At 2:21-2:22 the screw is seen standing in the hole,
    head towards R5.
11. **2:22-2:36** Screw driven with the hex driver. The driver's shaft passes THROUGH THE EMPTY SERVO OPENING in wall R5 (clear at 2:23-2:34); the left hand holds the frame.
    The head ends up on A7's outer face (seen at 2:44).
12. **2:37-2:39** Hands off. The H-frame stays on the turret held only by that screw and lies forwards and slightly down, resting on the top of the front end wall, engraved
    face of A6 up, "A6" code at the free end. It was free to swing down there, so the joint turns: this screw is the shoulder pivot on the R5 side. The builder does not test
    the motion on purpose and nothing is seen being backed off. Assembly pushed away to the top left.

Sub-assembly B: the three-layer lever (2:40 onwards, unfinished at 3:15)

13. **2:40-2:48** Bars A1, A2, A3 put down in a row, codes up, and left on show. A1: small hole at the top end, small hole just below the code, ONE LARGE ROUND HOLE further
    down, a small notch in one long edge beside the code. A2: the same two small holes and notch, but a KEYHOLE-SHAPED SLOT (round end towards the code) where A1 has the
    large hole. A3: as A2, but its top-end hole is LARGER. From 2:47, after the camera is nudged, a loose servo is in view lying beside the turret (dark see-through body,
    pink label with a blank white patch, no horn on its shaft). It is not touched in this stretch.
14. **2:49-2:55** A1 picked up in the left hand, code towards the camera. A2 laid flat on it, code towards the camera, outlines and notches lined up. A1's large hole shows
    through the round end of A2's keyhole slot (2:52-2:55).
15. **2:56-3:00** A3 laid flat on A2, code towards the camera. Stack from back to front: A1 / A2 / A3, all three codes facing the same way, all three notches together.
16. **3:01-3:17+** One screw (M3x10 by CAD: NAUO56; by eye it is between the pivot screw and the frame screws in length) fetched and pushed into the hole just below the "A3"
    code, i.e. the MIDDLE hole, from the A3 face (3:03-3:04). Hex driver picked up at 3:05, screw driven from 3:06; at 3:17 the head is about 1 mm from A3's face and the
    driver is still turning, so this action finishes in the next stretch. The keyhole pocket (two layers deep, A1 as its floor) is empty: no servo horn is in it yet.

Not done anywhere in 0:00-3:15: no servo fitted, no horn fitted, removed, turned or screwed to wood, no clamp plate (R7 / R8) fitted, no lead routed or plugged in, no servo
centred, no deliberate motion test, no part of the claw.

## 3. State at the end (3:15)

- On the turret: H-frame (A6 + A7 + A8 + two A9 + two M3x16) hanging on ONE M3x6 pivot screw through A7's end hole into R2's ear, head on the R5 side. The frame lies forwards
  over the front end wall. A8's loop-slot end is inside the turret beside wall R6 with nothing in the loop yet. Both servo openings (R5, R6) still empty.
- In the builder's hands: A1 / A2 / A3 stacked, one screw nearly home in the middle hole, entered from the A3 face. Top-end holes and the keyhole pocket empty.
- On the worktop: one loose servo beside the turret (no horn), links A11, A12, A13 and triangle A10 at the lower left. The clamp plates and anything else are out of frame.
- Wiring unchanged from the start: only the base servo's lead (flag "5") and the joystick ribbons are plugged in.

## 4. What the CAD says about the same joints, and what would be hard to show

Agreement with the CAD (all checked against `cad_arm_claw.md`):

- H-frame: screws NAUO53 (head at [200.7, 190.0, 123.5], pointing +Z, through A7 into the A9 at z = 138.0) and NAUO54 (head at [208.7, 198.9, 165.5], pointing -Z, through
  A8 into the A9 at z = 151.0). The A9 on the A7 side is 12 mm nearer the shoulder, as on video. Clearance hole in the bar, thread in the T piece: fully tight, not pivots.
- A6's code is nearer A7 and in the elbow half of the plate; A8's loop slot is at the shoulder end; A7 reads from the elbow end towards the shoulder. All as on video.
- Pivot: NAUO55 (M3x6), head top at [175.35, 161.84, 123.52], pointing +Z: clearance through A7, thread in R2. This axis runs through the middle of R5's servo opening
  (servo NAUO58 sits there later, shaft on the same axis), which is why the driver goes through that opening and why this screw has to go in before that servo.
- Lever: NAUO56 (M3x10), head on the A3 side at [158.64, 169.43, 114.54], pointing +Z: clearance through A3 and A2, thread in A1. Layer order A3 (z = 119.1, nearest wall R5) /
  A2 (122.1) / A1 (125.1, against A7). A1's large hole (5.7 mm) is the one that later sits over the HEAD of pivot screw NAUO55; A3's larger end hole is the recess for the
  head of NAUO62; the keyhole pocket in A2 + A3 takes the horn NAUO59 of the R5-side servo.

Differences and things a 3D guide has to handle:

1. **Two sub-assemblies are built in the hand, away from the model**: the H-frame (5 wood parts + 2 screws) and the lever (3 wood parts + 1 screw, plus whatever the next
   stretch adds). The guide needs steps that show a sub-assembly on its own and then a step that moves the whole sub-assembly onto the turret.
2. **Pose.** On video the H-frame goes in angled from the front and is then left lying forwards on the front end wall. In the CAD the upper arm stands about 48 degrees above
   horizontal. The step that fits the frame cannot use the CAD pose for its start, and a frame "floating" at 48 degrees on one screw would look wrong.
3. **The driver path.** The pivot screw is reached only through R5's servo opening (about 23 x 12 mm). The camera has to look from the -Z side and the lead line / screw path
   has to pass through that opening. This fixes the order: H-frame and pivot screw first, R5-side servo and clamp plate R8 afterwards.
4. **The pivot is not visibly "left loose".** The screw is driven for about 13 s and the frame then swings freely. In the CAD the head bears on A7, so a fully tightened
   screw would pinch A7 against R2. Whether students should back it off a touch is not answered by this stretch; the guide needs a note either way.
5. **T pieces are loose until the screw bites.** A9 only drops into its slot; the builder keeps A6 level until the screw has caught. Direction matters: stem first, from the
   engraved side of A6. The first A9 went in with its code facing A7; the CAD has both codes facing +Z. The part is symmetric, so this changes nothing but the picture.
6. **Self-tapping into wood.** Each frame screw takes 20 s or more of turning. A caption should say the screw cuts its own thread and feels stiff.
7. **A7 can be put on the wrong way round.** A7 has a hole at each end and looks symmetric, but the CAD has a 2.8 mm clearance hole at the shoulder end and a 2.3 mm thread
   hole at the elbow end. On video the rule that works is: engraved face out, and the "A" of "A7" at the same end as the "A6" code. Worth a label in the guide.
8. **A1 / A2 / A3 look alike.** They differ only in large hole vs keyhole slot and in the size of the end hole. The stacking rule seen on video: A1 at the back, then A2, then A3,
   codes all facing the same way, notches together, screw from the A3 face into the middle hole.
9. **The base servo's lead comes up between the two bars of the H-frame**, on the shoulder side of cross plate A6 (seen at 2:44-2:48). The frame is lowered around it.
   If the CAD routes that lead elsewhere, the fitted frame and the wire will not agree.
10. **Fingers hide the start of the pivot screw** (2:15-2:20). Whether it is passed through the servo opening or dropped in from above between R5 and A7 cannot be seen; both
    are possible (the gap between R5 and A7 is about 14.6 mm in the CAD and the screw is 9 mm long with its head).
11. The hex driver's handle is marked "3.0"; M3 socket-head screws normally take a 2.5 mm key, so the mark may belong to a different tip of the same tool. Not resolved here.

## 5. Reference stills

All in `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/arm/` (720 x 1280).

1. `docs/research/mra/stills/arm/t00m00s.jpg` - loose arm parts with their codes: R8, A9, A6, A8, A7, A13, A11, A12, A10; controller end of the base at top left.
2. `docs/research/mra/stills/arm/t00m17s.jpg` - A7 already on A6's tabs; T piece A9 (code readable) about to go into the cross slot.
3. `docs/research/mra/stills/arm/t00m23s.jpg` - first M3x16 screw pushed by hand through A7 and along the slot into A9.
4. `docs/research/mra/stills/arm/t00m52s.jpg` - outside of A7: code, screw head by the "7", A9's code facing A7, "A6" code at the "A" end.
5. `docs/research/mra/stills/arm/t00m59s.jpg` - A8 pressed onto the other pair of tabs, loop-slot end visible.
6. `docs/research/mra/stills/arm/t01m38s.jpg` - finished H-frame from the engraved side: two screws, two staggered T pieces.
7. `docs/research/mra/stills/arm/t01m53s.jpg` - turret before the arm: R1 on the floor, R2's ear, R5 with its empty servo opening, base servo lead leaving over the end wall.
8. `docs/research/mra/stills/arm/t02m04s.jpg` - H-frame just dropped into the turret, loop end inside, "A6" code at the free end.
9. `docs/research/mra/stills/arm/t02m26s.jpg` - pivot screw being driven, driver shaft through R5's servo opening.
10. `docs/research/mra/stills/arm/t02m44s.jpg` - pivot screw head on A7 at R2's ear ("R2" and "R5" readable); A1, A2, A3 laid out with their codes and holes.
11. `docs/research/mra/stills/arm/t03m04s.jpg` - A1 / A2 / A3 stacked, screw standing in the middle hole on the A3 face; A3's larger end hole visible.
12. `docs/research/mra/stills/arm/t03m15s.jpg` - end of the stretch: three layers seen edge-on, empty keyhole pocket, screw nearly home; H-frame on the turret and the loose servo
    at the top left.
