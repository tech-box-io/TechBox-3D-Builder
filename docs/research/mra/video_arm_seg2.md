# Arm.mov, stretch 2 (3:00 to 6:15): elbow lever, link pair A4/A5, elbow servo and clamp plate R8

Video: `/Users/lee-johnson/Desktop/Claude_Cadasio/MRA_Videos/Arm.mov` (12:00 long, portrait, camera looking down on a granite worktop).
This report covers seconds 180 to 375. Status: COMPLETE (overview at 2 s over the whole stretch, then every second from 2:20 to 6:44 read at
full size as cropped sheets). Times are the video's own. I also looked at 2:20 to 3:00 and 6:15 to 6:44 to pin down the start and end states;
what I say about those is marked as outside my stretch.

Directions: "controller end" = -X, "away from the controller" = +X, "turret top" = +Y, "R5 side" = -Z, "inward" = toward the middle of the turret.
CAD coordinates are mm in assembly space (Y up). The CAD numbers come from `mra.glb` through `tools/stepgen.py` (sections through each part at mid-thickness).

## What this stretch adds, in one paragraph

Three wooden layers A1 + A2 + A3 are screwed into one lever. Two thin bars A4 and A5 are joined end to end by a pivot screw. The lever is slid
into the gap between turret side plate R5 and the arm, onto the head of the shoulder pivot screw. A servo that already has a single-ended horn on
its shaft (lead flag "6") is pushed through R5 from outside so the horn lands in the lever's keyhole pocket, and is held by clamp plate R8 with
two screws. The lever is swung upright by hand and the free end of A4 is screwed to the top of the lever. Nothing is plugged in.

## Engraved codes read in this stretch (and the CAD part each one is)

All read from full-size stills; sure unless marked. From A3 upward the engraved code is NOT the CAD name.

| engraved | what it is | CAD mesh, id | how tied |
|---|---|---|---|
| A1 | lever layer nearest the arm: small hole at the far end, small hole in the middle, 5.75 mm round hole near the other end, solid beyond it | `ARA_A1` NAUO18 | hole pattern (2.8 / 2.3 / 5.75 mm) |
| A2 | lever middle layer: far-end hole, middle hole, keyhole-shaped slot (horn pocket) | `ARA_A2` NAUO19 | hole pattern |
| A3 | lever outer layer: same as A2 but the far-end hole is larger (5.6 mm, a recess for a screw head) | `ARA_A2_Supplement` NAUO20 | the larger end hole is seen at 2:44 to 2:48 and 3:24 |
| A4 | thin bar, one hole at each end 80 mm apart, engraving next to one end | `ARA_A3` NAUO21 | two 2.3 mm holes 80 mm apart |
| A5 | long thin bar, three holes (0 / 35 / 115 mm), engraving between the first two | `ARA_A4` NAUO22 | three 2.8 mm holes |
| A6 | cross plate of the arm's H-frame (already fitted) | `ARA_A11` NAUO29 | read at 4:04, 5:52 |
| R5 | turret side plate on the -Z side, with a 23.8 x 12.3 mm servo opening | `ARA_R6` NAUO15 | as `guide.py` already has it |
| R8 | rectangular clamp frame over the back of the servo in R5 | `ARA_R8` NAUO17 | on the R5 side; here CAD name = engraving |

Other codes visible on loose parts at the lower left, not used in this stretch: "A10" (triangle), "A11", "A12", "A13" (thin links).
So the wood runs A1 to A13; the CAD has A1 to A12 plus `A2_Supplement`.

Each lever layer also has a small half-round notch in one long edge, level with the middle hole (2:44 to 2:48). The notches line up when the three
layers are stacked the same way round.

## 1. State at the start (3:00)

- Top of frame: the base, controller and turret, complete, lying at an angle. The base servo's lead carries a WHITE flag "5" and is plugged into the
  shield; the rainbow joystick jumpers are plugged in.
- The arm's H-frame (two side bars joined by cross plate "A6", two long screws into the T-shaped wooden nuts) is already on the turret, straddling
  the ear of R2. Outside my stretch, at 2:22 to 2:34, I saw the builder drive one screw horizontally from the R5 side, THROUGH R5's servo opening,
  into the H-frame's side bar: that is the shoulder pivot (NAUO55, head at about [175.35, 161.84, 123.5]). Its head stands 3 mm proud of the side
  bar, facing R5. The lever of this stretch sits on that head.
- No servo in R5 or in the opposite side plate yet. One servo (pink label) lies at the left edge of the frame and stays there all through my stretch;
  the servo fitted in this stretch comes in from off-frame right.
- Lower left: loose links "A11", "A13", "A12", triangle "A10", a long bar lying blank side up; A4 and A5 are in that pile.
- T-handle hex driver (handle marked "3.0") at the right.
- In the builder's hands: the three lever layers, already stacked. Outside my stretch (2:44 to 2:59) they were laid out left to right A1, A2, A3,
  engraved faces up and the same way round, then A2 put on A1 and A3 on A2. At 2:53 A1's large round hole shows through the round end of A2's keyhole.

## 2. Timeline

1. **3:00-3:23 Lever screwed together (A1 + A2 + A3).** Stack held in the left hand, A3 on top, engraved faces all up, all three the same way round
   (engraved ends together, keyhole ends together). 3:03-3:05: one screw pushed by hand into the MIDDLE hole of A3, the hole just below the "A3"
   engraving. It drops about 6 mm and stands about 4 mm proud, which fits an M3x10 through two clearance layers (sure of "longer than 6, shorter
   than 16"; 10 by proportion and by the CAD). 3:06-3:22: driven with the hex driver, straight down through A3 and A2 into A1, fully tight. This is a
   fixed joint; it makes the three layers one part. Head ends up proud on the engraved face of A3 (3:24). CAD: NAUO56, M3x10, at [158.6, 169.5],
   head on NAUO20, clearance through NAUO20 and NAUO19, thread in NAUO18.
2. **3:24-3:26** Finished lever shown to the camera and put down at the upper left, A3 face up. From the engraved end: large hole, "A3", screw head,
   round end of the keyhole, slot running to the other end.
3. **3:27-3:37 A5 and A4 taken from the pile** at the lower left and laid side by side, engraved faces up, engraved ends away from the builder.
   A5 is the longer one with three holes; A4 has two.
4. **3:38-3:58 A4 and A5 joined (pivot).** A5 picked up in the left hand, A4 in the right. A5's end hole next to its engraving is laid over A4's
   PLAIN end hole (the end far from "A4"), both engraved faces the same way, A5 on top. 3:43-3:45: a short screw put in by hand through A5.
   3:46-3:58: bars held on edge and the screw driven horizontally from the right, through A5 into A4. Short screw, M3x6 (about 3 mm of shank shows
   before driving; guess by proportion, agrees with the CAD). CAD: NAUO57, M3x6, at [197.1, 235.7], clearance in NAUO22, thread in NAUO21.
5. **3:59-4:01** The pair is opened to an L and laid down, both engravings up, screw head on the engraved face of A5. It swings freely straight after
   driving, so this joint is a pivot (how far the screw was backed off, if at all, cannot be seen).
6. **4:02-4:12 Assembly re-oriented.** Base assembly pulled to the middle; the lever is picked up and put down a couple of times; at 4:08 the whole
   assembly is laid on its side with plate R5 facing up at the camera (base plate on edge at the right of the frame, controller toward the top, the
   arm's H-frame hanging at the lower left). No assembly action.
7. **4:13-4:23 Lever fitted between R5 and the arm.** Lever held with the A3 face toward the camera (so A3 will face R5, outward), keyhole end
   toward the bottom of the frame, large-hole end toward the top (4:13-4:14). Turned edge-on and slid in from the open top of the turret, keyhole end
   first, into the gap between the inner face of R5 and the arm's side bar (4:15-4:16). 4:17-4:21: looking through R5's servo opening, the head of
   the lever's middle screw is in the corner of the opening nearest the turret top and the controller, and a set of concentric rings (round end of
   the keyhole, A1's round hole, a screw head inside it) is at the end of the opening away from the controller. That is the lever sitting with A1's
   5.75 mm hole over the head of the shoulder pivot screw. 4:22-4:23: lever nudged round; its engraved end with the large hole sticks out past the
   top edge of R5. Nothing fastens the lever: it is a loose pivot on the screw head, trapped between the arm and R5.
8. **4:24-4:27** Assembly stood upright for a moment; a fingertip pushes down into the gap on the lever (guess: seating it on the screw head; the hole
   itself cannot be seen); laid back on its side, R5 up. From here to 4:43 the left forefinger rests on the lever's sticking-out end.
9. **4:28-4:43 Servo pushed into R5 from outside, horn already on.** The servo comes from off-frame right. A black single-ended horn is ALREADY on
   its shaft at 4:28; I did not see it being fitted in my stretch, and I could not see whether a horn screw is in the shaft. The horn lies along
   the long axis of the case and points past the shaft end (outboard), as in the CAD. 4:33-4:36: servo turned so the shaft points down at R5, long
   axis of the case along the long axis of the opening, shaft at the end AWAY from the controller. 4:37: tilted, horn end lowest, and the horn fed
   through the opening first, toward the end away from the controller; 4:38-4:40: levelled; 4:41-4:43: pressed down until the mounting ears sit on
   R5's outer face. The left forefinger holds the lever still meanwhile, so the horn drops into the lever's keyhole pocket (blind: hidden behind R5).
   The lead leaves the servo at the end away from the controller, on the outside of R5. CAD: servo NAUO58 (case x 159.0..181.6, y 156.2..168.3, ears
   x 154.2..186.4 at z 106.5..109.0, on R5's outer face z 109.0), shaft toward +Z on the shoulder axis [175.35, 161.84], horn NAUO59 in the pocket
   through NAUO20 and NAUO19. The horn is not screwed to any wood; it is captive in the pocket.
10. **4:44-5:00 Clamp plate R8 threaded over the lead and laid on the servo.** 4:44-4:46: lead lifted, R8 picked up (a rectangular frame with a
   window and one small hole in the middle of each long side). 4:47-4:51: the servo plug is passed through R8's window; the lead carries a BLACK flag
   with a white underlined "6" (sure it is 6 and not 9: the underline is under the digit at 4:51, 5:52 to 5:57 and 6:12 onward). 4:52-4:57: R8 slid
   down the lead and lowered over the back of the servo, engraved face out; "R8" sits on the long side nearest the turret top, at its controller end.
   The servo's back end and the lead stick out through and beyond R8. CAD: NAUO17, window x 157.7..181.9, y 156.1..168.4, outer face z 103.5.
11. **5:01-5:21 First clamp screw.** 5:03-5:07: screw put by hand into R8's hole on the turret-top side of the servo (the hole next to the "R8"
   engraving). 5:08-5:20: driven straight down with the hex driver, through R8 into R5. Medium length, M3x10 (the shank is about twice the head
   diameter in the fingers at 5:03). The screw passes BESIDE the servo case at mid-length, not through the servo's ear holes; the ears are trapped
   between R8 and R5. CAD: NAUO60 at [170.3, 171.6], 2.8 mm clearance hole in NAUO17, 2.3 mm hole in NAUO15.
12. **5:22-5:40 Second clamp screw.** 5:24-5:26: the lead, which had been lying up along the base plate, is swept down toward the bottom of the frame.
   5:27-5:30: second screw put into R8's other hole (base-plate side of the servo); both heads visible at 5:29-5:30. 5:31-5:40: driven. CAD: NAUO61 at
   [170.3, 153.0], M3x10.
13. **5:41-5:49** Assembly stood upright again (controller at the top of the frame, R5 side at the right). The driver is used horizontally from the R5
   side on a clamp screw while the left hand steadies the arm; the driver's shaft passes over the top of the servo, so it is the upper screw (NAUO60)
   being finished (fairly sure). Both clamp screws end fully tight: fixed joints.
14. **5:50-5:59 Lever swung up by hand.** Driver put down (5:50). The right hand takes the lever by its free end and turns it about the shoulder axis
   from leaning toward the controller to nearly upright (5:51-5:59), while the left hand holds the arm. This back-drives the servo, because the horn
   is in the lever's pocket. No powered test and no centring. Purpose (inferred, see section 4): to lift the lever's end hole clear above R5's top edge.
15. **6:00-6:11 A4 offered to the top of the lever, screw started by hand.** 6:00-6:02: the A4/A5 pair picked up from the lower left by A4, A5 hanging
   below. 6:04-6:07: A4's ENGRAVED end (hole next to "A4") brought to the lever's free end, on the INNER face of the lever (against A1, the side toward
   the arm). 6:05: screw picked up with the right hand. 6:06-6:11: screw pushed in by hand from the R5 side into the large end hole of A3, through A2
   and A1 toward A4; from 6:08 the four layers are seen edge-on with the screw head at the R5 side. A4's engraved face ends up against the lever
   (facing the R5 side); shown by 6:32 to 6:42, outside my stretch: A5 sits on the R5 side of A4 with its screw head facing the R5 side, and the faces
   turned inward are blank.
16. **6:12-6:15 (goes on to 6:29, outside my stretch) Screw driven.** Hex driver horizontal, from the R5 side, into the lever's top hole; left hand
   pinches the stack. CAD: NAUO62, M3x10, at [143.4, 176.3] in the CAD pose, head in the 5.6 mm recess of NAUO20, clearance through NAUO19 and NAUO18,
   thread in NAUO21. On video the tip shows through the inner face of A4 at 6:32 to 6:36, which fits M3x10 with the head sunk in A3. Afterwards the
   links swing freely on it (6:30-6:40), so it is a pivot.

## 3. State at the end (6:15)

- Lever (A1 + A2 + A3, one screw) on the shoulder axis between R5 and the arm's R5-side bar, A3 facing R5, standing nearly upright.
- Servo "6" in R5, shaft inward on the shoulder axis, horn in the lever's pocket, held by R8 and two M3x10 screws into R5. Shaft end and lead
  exit both at the end away from the controller.
- A4's engraved end on the inner face of the lever's free end, the screw through the lever into A4 started and being driven from the R5 side.
- A5 hangs from A4's other end on the R5 side of A4 (pivot screw, head toward the R5 side). A5's middle and far holes are still free.
  (At 6:40 to 6:44, outside my stretch, the builder starts a screw through A5's middle hole into the far end of the arm's R5-side bar.)
- Lead "6" is NOT plugged in and NOT routed: it leaves the servo's end away from the controller and lies loose on the worktop round the front
  of the base, flag and plug at the lower left of the frame. Base servo lead "5" is unchanged.
- The opposite side plate has no servo yet; the second side servo still lies at the upper left. "A10" to "A13" still loose.
- Every screw head fitted on this side faces the R5 side (outward): NAUO56, NAUO57, NAUO60, NAUO61, NAUO62 (and the pivot NAUO55 from before).

## Joints: fixed or pivot

| joint | screw | on video |
|---|---|---|
| A3 + A2 + A1 (lever) | NAUO56 M3x10, middle hole | fixed, driven fully tight |
| A5 to A4 | NAUO57 M3x6 | pivot: swings freely straight after driving (3:59) |
| lever on the shoulder axis | none: A1's 5.75 mm hole rides on the 5.5 mm head of the shoulder pivot screw NAUO55 | pivot, turned by the servo horn |
| R8 to R5 | NAUO60, NAUO61 M3x10 | fixed, tight; servo ears clamped between the two plates |
| lever free end to A4 | NAUO62 M3x10 | pivot: links swing on it after 6:29 |

Order of layers on the R5 side, from outside in (CAD z): R8 103.5..106.5, gap with the servo ears, R5 109..112, 5.6 mm gap, A3 117.6..120.6,
A2 120.6..123.6, A1 123.6..126.6, then A4 and the arm's side bar in the same layer 126.6..129.6, then R2's ear 129.6..132.6. A5 is in A1's
layer (123.6..126.6), on the R5 side of A4.

## 4. Hard to show in a 3D guide, or possibly different from the CAD

1. **The lever goes onto a screw HEAD inside a closed gap.** With R5 in place the lever cannot move in along Z at all, and sliding it down the gap
   (along -Y) it has to hop 3 mm sideways over the pivot screw's head. In the CAD the gap is 14.6 mm (R5 inner face z 112.0 to the side bar z 126.6)
   and the lever plus the proud head of its own screw NAUO56 is 12 mm, so the hop only works where that head is not behind R5: over the servo opening
   or above R5's top edge. On video the head is seen inside the servo opening at 4:17 to 4:21, which is how it fits (inference from what is seen plus
   the CAD numbers). `stepgen`'s collision test will not find a straight path; this step needs a hand-set motion and a Review note.
2. **The servo cannot go straight in with its horn on.** R5's opening is x 158.9..182.7, y 156.1..168.4. In the CAD the horn tip is at x 192.4, 18.3 mm
   from the shaft axis, 9.7 mm past the end of the opening. The builder tilts the servo and feeds the horn through first, then levels it. A straight
   axial move collides in the CAD.
3. **Blind mating.** The horn has to find the keyhole pocket behind R5 while a finger holds the lever at the right angle. In the CAD pose the horn
   points 22.7 degrees below +X and the lever's long arm 155.6 degrees from +X (24 degrees above level, toward the controller). The video does not
   show the lever angle when the servo goes in, nor any centring of the servo first.
4. **The horn is already on the servo at 4:28.** Fitting it (and whether it gets a horn screw) is not in my stretch. The guide needs that step
   somewhere before this one; check the other stretches and videos.
5. **R8 must be threaded over the plug and slid down the lead** before it can sit on the servo. A rigid CAD wire cannot show that; it needs a note.
6. **The lever is turned by hand before the A4 screw goes in.** In the CAD pose the axis of NAUO62 is at y 176.3 and R5's top edge is at y 175.4, so
   the screw is only 0.9 mm above the plate edge and a driver from the R5 side fouls R5. The builder swings the lever upright first. Either the guide
   shows the lever rotated for that step, or the camera hides the problem.
7. **Pivot tightness** cannot be seen. Only the result: A5 on A4 and A4 on the lever swing freely; the lever and clamp screws are tight.
8. **The kit is laid on its side** (R5 up) from 4:08 to 5:40 for the lever, servo, R8 and both clamp screws, and is upright for everything else.
   A guide would keep it upright and look from the R5 side.
9. **Engraved codes against CAD names** as in the table: A3 = CAD `A2_Supplement`, A4 = CAD `A3`, A5 = CAD `A4`, A6 = CAD `A11`, R5 = CAD `R6`.
10. **Lead "6"** is left loose; routing and plugging happen later. The clamp screws go beside the servo, not through its ears, which is easy to
   draw wrongly.

## 5. Reference stills (1280 px, in `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/arm/`)

- `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/arm/t03m05s.jpg` screw standing in the middle hole of A3, three layers stacked.
- `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/arm/t03m24s.jpg` finished lever: large end hole, "A3", screw head, keyhole pocket; loose "A10" to "A13" at the left.
- `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/arm/t03m32s.jpg` A5 (three holes) and A4 (two holes) side by side, engravings readable.
- `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/arm/t04m00s.jpg` A4 and A5 joined as an L, screw head on the engraved end of A5, A5 on top of A4.
- `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/arm/t04m13s.jpg` assembly on its side, R5 up; lever held A3 toward R5 before it goes in.
- `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/arm/t04m18s.jpg` lever in place seen through R5's servo opening: its screw head and the rings of the pivot.
- `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/arm/t04m36s.jpg` servo with the single-ended horn on its shaft, about to go into R5.
- `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/arm/t04m43s.jpg` servo seated in R5, lead leaving the end away from the controller, lever end "A3" sticking out past R5.
- `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/arm/t04m50s.jpg` clamp frame R8 threaded on the lead; black flag "6".
- `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/arm/t05m30s.jpg` R8 on the servo with both clamp screws in, one each side of the case; "R5" and "R8" readable.
- `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/arm/t05m59s.jpg` kit upright; lever being swung upright by hand; lead "6" loose at the lower left.
- `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/arm/t06m07s.jpg` A4's engraved end held to the inner face of the lever top, screw pushed in from the R5 side.

Not copied but worth the merge's attention (in the next stretch): 6:32 to 6:36 shows the layer order lever / A4 / A5 from above, and 6:42 shows the
blank inward faces of A4 and A5.
