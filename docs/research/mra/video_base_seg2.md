# Base.mov, second stretch: 4:25 to 8:54 (265 s to 534 s)

Status: COMPLETE. Every 2 s frame of 4:24-8:52 was read, then every 1 s frame of 4:10-4:32 and 4:52-8:53, with
half-second frames for the two plate joins and native-resolution (1080 x 1920) crops wherever a code, a hole or the lead
had to be read.

Source: `/Users/lee-johnson/Desktop/Claude_Cadasio/MRA_Videos/Base.mov` (phone video, portrait, 533.6 s).
Timestamps are the video's own (m:ss). Two people work together: one with rings and a watch on the left hand, who mostly
holds the work, and a second who mostly drives the Allen key. "The builder" below means whoever is acting.

What this stretch contains, in one paragraph: at 4:25 the turret (R1-R6 with the base servo and its horn) is already on
B2. B1 is then fitted underneath so the horn drops into B1's horn-shaped cut-out, the pair is turned over to check, and
six socket-head screws are put in from above in the order NAUO47, 48, 49, 50, 51, 52 and then all six are gone round
again with the Allen key. The servo lead is never put into R4's L-shaped slot and is never plugged in. No servo is
centred and the turret is not turned by hand to test it.

## CAD facts used to name things (measured from mra.glb; mm, assembly space, Y up)

| Thing | CAD id | Where |
|---|---|---|
| B1, bottom plate | NAUO1 | Y 87.53-90.53; outline X -27.2..215.5, Z 93.3..188.3 (242.7 x 95.0) |
| B2, top plate | NAUO2 | Y 90.53-93.53; same outline |
| R1 turret floor | NAUO10 | Y 99.96-102.96 (6.4 above B2's top face) |
| R2 divider holding the servo | NAUO11 | Z 129.55-132.55 |
| R3 | NAUO12 | X 192.7-195.7 (wall at the far end, away from the controller) |
| R4 | NAUO13 | X 131.9-134.9 (wall facing the controller end) |
| R5 (engraved; CAD file "R6") | NAUO15 | Z 109-112, 81.8 tall, feet on B2's top face (Y 93.5) |
| R6 (engraved; CAD file "R5") | NAUO14 | Z 169.2-172.2, 91.5 tall, feet on B2's top face |
| Base servo | NAUO45 | shaft down, axis at X 163.65, Z 140.85; gear-case face Y 93.6; shaft tip Y 91.6 |
| Horn (double-ended) | NAUO46 | 36.3 long along X, 6.7 wide; arms Y 90.16-92.21; hub Y 89.86-94.41 |
| Screws, M3 x 6 socket head | NAUO47-52 | heads on top of B2 (Y 93.5-96.5), threads down to Y 87.5 |

- B2's keyhole: a slot 13.0 wide (X 157.0-170.0) cut in from the long edge at Z 93.3 (the R5 side) to a round cut-out
  19.0 in diameter centred X 163.6, Z 140.85.
- B1's horn-shaped cut-out: X 144.8-182.5, Z 136.9-144.8 (37.6 x 8.0), long axis along X, centred under B2's round
  cut-out. The horn (36.3 x 6.7) fits it with about 0.65 clearance all round.
- Screw holes are 2.8 in B2 (clearance) and 2.3 in B1 (the screw cuts its own thread in the wood). Centres (X, Z):
  NAUO47 (209.2, 99.7), NAUO48 (104.1, 99.7), NAUO49 (-20.8, 99.7), NAUO50 (-20.8, 182.0), NAUO51 (104.1, 182.0),
  NAUO52 (209.2, 182.0). Z 99.7 is the R5 side, Z 182.0 the R6 side; X 209 is the turret end, X -21 the controller end.
- Engraved "B2" is on B2's top face at X -14.9..-5.4, Z 96.8..103.2 (controller end, R5 side, next to NAUO49).
  Engraved "B1" is on B1's top face at the same corner (X -12.1..-3.8), so it is covered by B2 once the plates are joined.
- R4's L-shaped slot: a channel about 3 wide cut down from R4's top edge (Y 146.6) at Z 140.5-143.5 to Y 136, opening
  sideways into a pocket Y 127.5-136, Z 140.5-148.5. It is at the middle of R4's top edge.

## 1. State at the start of the stretch (4:25)

The 15 s before 4:25 belong mainly to the first stretch. They are described here from half-second stills so the merge
can line the two reports up, and because Lee's point about B2 is settled by them.

- 4:11-4:14 B2 is held up by the second person, engraved face up, keyhole slot towards the turret
  (`stills/base/t04m14s.jpg`). The turret is in the other person's hands, underside showing: black double-ended horn
  on the servo shaft below R1.
- 4:14.5-4:17.5 **B2 goes on.** Both parts are in the air and tilted. The turret is offered to the slot-mouth edge of
  B2 lying over on its R5 side (codes "R6" and "R4" readable at 4:14.5 and 4:15). B2's edge goes in between the horn
  (which stays underneath B2) and the turret (R1's underside and the feet of R5 and R6, which stay on top of B2). The
  servo's neck runs along the slot to the round cut-out, R6 side leading and R5 side last, and the two are levelled.
  By 4:17 the turret stands on B2 with R5 at the slot-mouth edge, code "R5" facing outwards. In CAD terms the turret
  travels +Z relative to B2 (B2 travels -Z relative to the turret) by about 55 mm, the distance needed for the servo's
  gear-case end to get from outside the plate edge (Z 93.3) to the cut-out centre (Z 140.85).
- 4:18-4:21 The lead, which was trailing across the controller part of B2, is lifted aside by the second hand and laid
  on the worktop on the R6 side (`stills/base/t04m21s.jpg`).
- 4:22-4:23 The assembly is tipped back to show B2's underside (`stills/base/t04m23s.jpg`): the horn lies flat against
  the underside of B2, across the round cut-out, long axis along the length of the plate (CAD X), at right angles to
  the slot. A silver cross-head screw is in the horn's hub, so the horn is screwed to the servo shaft. The servo's black
  gear-case end fills the round cut-out and the inner end of the slot and looks nearly level with B2's underside;
  R1's underside shows through the rest of the slot.
- 4:24-4:29 Set down on the worktop, turret up (`stills/base/t04m28s.jpg`). Turret orientation on B2: R4 faces the
  controller end, R3 the far end, R5 is on the slot-mouth side, R6 on the other side.
- B1 lies apart at the top right of the frame, engraved face up. The servo lead is not plugged in to anything; it
  comes up out of the open top of the turret, over R4's top edge at its R6 end, and lies on the worktop with a white
  paper flag marked "5" near the plug.

## 2. Timeline of actions

Codes read on the wood in this stretch, all at native resolution and all certain: "B2" (4:27, 6:24, 8:24-8:53), "B1"
(4:59), "R5" (4:21, 4:22, 5:00, 5:04, 5:12), "R4" (4:15, 8:50), "R6" (4:14.5), "R3" (5:04, 5:06), "R1" on the turret
floor seen from above (5:35-5:55).

1. **4:29-4:54 Nothing is assembled.** At 4:29 a hand straightens the free end of the lead; from 4:31 to 4:53 nothing
   moves (presumably talking). Turret on B2 on the worktop, B1 still at the top right.
2. **4:54.5-4:56 B1 picked up** (NAUO1) from the top right, engraved face up, and brought under the camera in one
   hand while the other hand lifts B2 with the turret on it.
3. **4:56-4:59.5 Shown before joining.** B2 with the turret is tipped back so the horn under B2 faces the camera, and
   B1 is held beside it, code "B1" up, horn-shaped cut-out visible (`stills/base/t04m59s.jpg`). B1 is the same way round
   as B2: codes at the same corner, cut-out at the turret end.
4. **4:59.5-5:01 B2 (with the turret) is put onto B1**, in the hands, not on the worktop. The two plates are closed
   together face to face: B2's plain underside onto B1's engraved top face, outlines lined up, and the horn drops into
   B1's horn-shaped cut-out (`stills/base/t05m00s.jpg`). Relative motion is straight along Y: B2 and turret down onto
   B1 (equally, B1 up onto B2). B1 goes on at a slight angle and is then pressed flat. The horn was already lying
   along the length of the plates, so nothing was turned to make it fit. Nothing is done to the horn itself.
5. **5:01-5:11 Turned over and checked from below.** The pair is tipped until B1's underside faces the camera (5:02,
   5:06, 5:08, 5:10). The horn sits inside B1's cut-out with its hub screw visible, about flush with B1's underside
   (`stills/base/t05m08s.jpg`). At 5:08-5:11 a second hand squeezes the two plates together. Between views it is tipped
   the other way to show the turret side (5:04: "R3" and "R5" readable).
6. **5:12-5:18 Turned upright and set down** on the worktop, turret up. The lead hangs free while the assembly is in
   the air (flag "5" visible at 4:59) and is left on the worktop on the R6 side. 5:19-5:23 hands off; no screws in
   (both turret-end holes are empty at 5:26).
7. **5:24-5:25 A screw is held up to the camera** (`stills/base/t05m25s.jpg`): silver socket-head cap screw, head
   about 5.5 across and 3 tall, thread about as long as the head is wide. That fits M3 x 6; the length cannot be
   measured from the video (guess, agreeing with the CAD's M3 x 6).
8. **5:26-5:52 Screw 1, NAUO47 position** (turret-end corner, R5 side). Dropped into the hole by hand at 5:27, standing
   in the hole at 5:28-5:32, plate turned a little at 5:33-5:34, then driven with an L-shaped Allen key by the second
   person while the other holds the plate down (5:35-5:52, key visible at 5:38 and 5:41, `stills/base/t05m38s.jpg`).
   From above, through B2, into B1. Driven until the head sits on B2. Hands off at 5:53-5:55.
9. **5:56-6:21 Screw 2, NAUO48 position** (middle hole of the R5-side long edge, beside the turret). Key picked up and
   passed across at 5:56-5:58; at 6:02-6:06 the screw appears to be put on the tip of the key in the fingers and
   carried to the hole; driven until 6:21.
10. **6:22-6:24 Plate turned** on the worktop so the controller end is nearest the camera; "B2" readable; two screws
    in, four holes empty (`stills/base/t06m24s.jpg`).
11. **6:25-6:39 Screw 3, NAUO49 position** (controller-end corner beside the "B2" code).
12. **6:42-7:02 Screw 4, NAUO50 position** (the other controller-end corner). 7:03 plate turned.
13. **7:04-7:22 Screw 5, NAUO51 position** (middle hole of the R6-side long edge, next to where the lead lies).
    Screw in the fingers at 7:04; key in use at 7:19-7:22.
14. **7:23-7:26 Plate spun half a turn.** Five screws in; the turret-end corner on the R6 side is still an empty
    hole (`stills/base/t07m25s.jpg`).
15. **7:27-7:38 Screw 6, NAUO52 position** (turret-end corner, R6 side). Offered on the key at 7:27, driven by 7:38.
    All six are in at 7:39.
16. **7:40-8:40 All six gone round again with the Allen key**, the plate being turned between them:
    NAUO47 7:40-7:57; plate turned 7:58-7:59; NAUO52 8:00-8:15; plate turned 8:16-8:19; NAUO51 8:20-8:23;
    NAUO48 8:24-8:33 (fingers on the head first, then the key); NAUO49 8:35-8:38; NAUO50 8:39-8:40. This is a final
    tightening, not late fitting: the heads already sat on B2 after the first round (compare the NAUO48 screw at 6:24
    and at 8:27). All six are tightened fully; none is left loose as a pivot.
17. **8:41-8:43 Plate spun and set straight**, turret at the top of the frame, controller end towards the camera.
18. **8:43-8:53 Final hold**, hands off (`stills/base/t08m50s.jpg`).

Screws were therefore put in going round the outline of the plate, which happens to be CAD-id order: 47, 48, 49, 50,
51, 52. The first screw in the video is the same one the present guide shows first (`SCREWS[0]` = NAUO47).

How sure the screw positions are: each was fixed two ways, by where the hands work relative to the "B2" code and the
side the lead leaves the turret (the R6 side), and by counting screws against empty holes in the hands-off frames at
5:26, 5:53, 6:24, 6:41, 7:04, 7:25 and 7:39. The first, second and sixth were also checked on native-resolution crops.
The third, fourth and fifth rest on 1 s frames at 1280 px; the order is certain, the exact start and end seconds of
each are good to about 2 s.

What the servo lead does at each stage:

| Time | Lead |
|---|---|
| 4:14-4:17 B2 slid on | Trails out of the open top of the turret over R4's top edge at its R6 end; hangs free, then lies across B2 |
| 4:18-4:21 | Lifted off B2 by hand and laid on the worktop on the R6 side |
| 4:54-5:18 B1 fitted and checked | Dangles free below the work; flag "5" visible; not held or routed |
| 5:19-8:40 screws | Lies on the worktop; swings round each time the plate is turned; a hand rests on it at 8:00-8:15 |
| 8:43-8:53 end | Unchanged: over R4's top edge at the R6 end, down the outside of the R4 / R6 corner under R6's ear, onto the worktop |

The lead is the standard three-wire servo ribbon (brown, red, orange) with a black three-way socket. The flag is a
white paper tab marked "5", centred about 25-30 mm from the plug end (scaled from the 95 mm plate width in the same
frame). It is not plugged into anything at any point in this stretch.

## 3. State at the end of the stretch (8:53)

- B1 (NAUO1) under B2 (NAUO2), outlines lined up, held by six M3 socket-head screws (NAUO47-52) driven from above
  through B2 into B1, all tight, heads standing about 3 mm above B2.
- Turret R1-R6 (NAUO10-15) standing on B2 at the end away from the "B2" code, square to the plate: R4 towards the
  controller end, R5 on the slot-mouth side, R6 on the other. Base servo (NAUO45) inside, shaft down through B2's
  keyhole; horn (NAUO46) below B2, sitting in B1's cut-out. Because B1 is now fixed to B2, the horn cannot turn, so
  when the servo is driven the turret will turn on B2. The horn is wider than B2's 19 mm cut-out, so it is also what
  stops the turret lifting off.
- Servo lead loose, unplugged, flag "5", lying on the worktop on the R6 side. **R4's L-shaped slot is empty**
  (native-resolution crop of 8:50): the lead crosses R4's top edge about 20-25 mm away from the slot, hard against R6.
- Nothing else is fitted: B3-B8, the joysticks and the I/O module are not on the base. The shield with jumper wires
  and the two joysticks sit unused at the top left of the frame.

## 4. Lee's points checked against the video

| Lee's statement | Seen in this stretch |
|---|---|
| B2's slot slides in above the servo horn and below R5 / R6, into B2's round cut-out | Yes, 4:14.5-4:17.5. Done in the air with both parts tilted, R6 side first, R5 ends at the slot-mouth edge |
| Then the horn fits into the horn-shaped cut-out in B1 | Yes, 4:59.5-5:01, checked from below at 5:02-5:10. B2 with the turret goes down onto B1's engraved face |
| Then six 6 mm screws | Yes, six, 5:26-7:38, from above, order NAUO47, 48, 49, 50, 51, 52, then all re-tightened 7:40-8:40. Length not measurable; they look like M3 x 6 |
| After R6 the servo lead is moved into the L-shaped slot in R4 | **Not seen.** Not done anywhere from 4:10 to the end of the video; the slot is empty in the last frame. The first-stretch report says the same for 0:00-4:42. If it is done, it is in another video |
| The servo arrives with its double-ended horn already fitted | Consistent: the horn is on the shaft, with a screw in its hub, before B2 goes on, and nothing is done to it afterwards |

## 5. Hard to show in a 3D guide, or where the video and the CAD disagree

1. **The horn is too high in the CAD.** In mra.glb the horn's arms are at Y 90.16-92.21, inside B2's layer
   (Y 90.53-93.53), and beyond the 19 mm round cut-out (X below 154.1 and above 173.1) they pass through solid B2.
   Only 0.4 mm of the arms is in B1's layer, so in the CAD the horn does not sit in B1's cut-out at all. On video the
   horn is wholly below B2 and sits in B1's cut-out about flush with B1's underside (5:08). To match, the horn has to
   be about 2.3-2.6 mm lower than the CAD has it (arms at roughly Y 87.8-89.9). Guess at the cause: partly the horn is
   modelled too high on the shaft (its hub top, Y 94.41, is 0.8 mm inside the servo's gear case, face at Y 93.6), and
   partly the servo sits lower in the real kit. Supporting the second part: the gear-case end is 11.8 x 14.7 in plan,
   18.9 across the diagonal, and B2's round cut-out is 19.0, as if that end is meant to turn inside B2's thickness;
   and at 4:23 the black gear-case end looks nearly level with B2's underside. Effect on the generator: a collision
   test will find no free direction for B2 against the turret, or for B1 against B2 and the horn, until this is
   corrected or the motion is set by hand.
2. **The present guide shows the horn arriving with B2** (`show=[B2, BASE_HORN]` in "attach R1 - R6 to B2", with the
   turret moved onto it). On video the horn is part of the servo from the start, and B2 is fed in sideways between
   horn and turret. A straight vertical placement of the turret onto B2 is impossible in the real kit: the horn is
   36 mm long and the cut-out is 19 mm.
3. **The B2 slide is a hand manoeuvre**, done tilted and in the air in about two seconds. The clean equivalent is a
   level slide of about 55 mm along Z with B2 passing through the 3 mm gap between the horn and the feet of R5 / R6.
4. **The horn-to-B1 fit can only be seen from below.** The builder turns the whole assembly over to check it
   (5:02-5:10). A camera from above shows nothing of this joint.
5. **Horn direction is not adjustable at this point.** The horn has to lie along the length of the plates to drop into
   B1. Here it already did. If a servo were not at the same angle, the turret would have to be turned on B2 until the
   horn lined up, and the turret would then sit at an angle to the base. No centring is shown in this stretch and the
   servo is unplugged throughout.
6. **B1's engraved code ends up hidden** between the plates (the CAD has "B1" on B1's top face; at 4:59 B1 is held
   code-up just before B2 goes on top). After this step B1 can only be told apart by shape.
7. **The screws are socket-head cap screws driven with an Allen key**, self-threading into B1's 2.3 mm holes. The head
   stays about 3 mm proud of B2 when tight, which is what the CAD shows (head Y 93.5-96.5).
8. **Everything is tightened twice.** The second round (7:40-8:40) has no CAD equivalent; it is a caption, not a step.
9. **The plate is turned on the worktop nine times** during the screws so that each hole faces the person with the
   key. None of this needs showing.
10. **The loose lead** has no fixed shape. On video it leaves over R4's top edge at the R6 end, not through the
    L-slot, and it is unplugged, so whatever the CAD shows for the lead at this stage is a choice, not a record.

## 6. Reference stills

All in `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/base/` (1280 px on the long side).

- `stills/base/t04m14s.jpg` - B2 held up, keyhole slot and round cut-out clear; turret underside with horn at lower left.
- `stills/base/t04m21s.jpg` - turret upright on B2, "R5" at the slot-mouth edge; lead being laid aside on the R6 side.
- `stills/base/t04m23s.jpg` - underside of B2: horn across the round cut-out with its hub screw, servo end in the slot.
- `stills/base/t04m28s.jpg` - state at the start of this stretch, set down on the worktop; B1 apart at the top right.
- `stills/base/t04m59s.jpg` - just before joining: horn under B2 in one hand, B1 code-up with its cut-out in the other.
- `stills/base/t05m00s.jpg` - the two plates closed together in the hands, "R5" readable.
- `stills/base/t05m08s.jpg` - underside of B1: horn sitting in the horn-shaped cut-out, flush.
- `stills/base/t05m25s.jpg` - the screw held up to the camera: short socket-head cap screw.
- `stills/base/t05m38s.jpg` - first screw (NAUO47 position) being driven with the Allen key; "R1" visible on the floor.
- `stills/base/t06m24s.jpg` - two screws in (NAUO47, NAUO48), "B2" readable, Allen key in the hand at the right.
- `stills/base/t07m25s.jpg` - five screws in, the turret-end corner on the R6 side still an empty hole; lead and flag "5".
- `stills/base/t08m50s.jpg` - final state: six screws, lead over the R4 / R6 corner, L-slot in R4 empty.
