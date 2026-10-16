# Base.mov, 0:00 - 4:40 (seconds 0 - 280): what the builder does

Status: COMPLETE for this stretch (studied to 4:42).
Source: `/Users/lee-johnson/Desktop/Claude_Cadasio/MRA_Videos/Base.mov` (8:54 long, portrait phone video, 1080 x 1920, camera looking down
at a granite worktop; the builder's hands come in from the bottom of the frame).

How it was studied: every 2 s over the whole stretch (contact sheets), then every 1 s at 1600 px for every action, then 3 to 6
frames a second at full resolution for the three fast actions (horn through R1 at 0:18-0:22, lead handling at 3:20-3:24 and
3:36-3:42, turret into B2 at 4:08-4:26). All times are the video's own. Nothing was tested by ear: the sound track was not used.

Directions are given two ways: relative to the parts, and in CAD assembly space (mm, Y up). The link between the two was fixed by
matching the engraved faces seen on video to the engraved (0.25 mm recessed) faces in the CAD, part by part; every part's side and
facing on video agrees with its place in the CAD.

| Engraved code (read on video) | CAD id | CAD mesh name | Where it is in the CAD (mm) | Engraved face |
|---|---|---|---|---|
| R1 | NAUO10 | ARA_R1 | flat plate, X 127.6-200.3, Y 100.0-103.0, Z 105.6-175.6 | top (+Y); text at X 136-143, Z 138-147 |
| R2 | NAUO11 | ARA_R2 | upright, Z 129.6-132.6, X 127.6-200.3, Y 96.6-167.9 | -Z |
| R3 | NAUO12 | ARA_R3v2 | upright, X 192.7-195.7, Y 96.6-146.6 | +X (outwards) |
| R4 | NAUO13 | ARA_R4v2 | upright, X 131.9-134.9, Y 96.6-146.6 | -X (outwards) |
| R5 | NAUO15 | ARA_R6 (CAD name is swapped) | upright, Z 109.0-112.0, Y 93.5-175.4 | -Z (outwards) |
| R6 | NAUO14 | ARA_R5 (CAD name is swapped) | upright, Z 169.2-172.2, Y 93.5-185.0 | +Z (outwards) |
| B2 | NAUO2 | ARA_B2 | flat plate, Y 90.5-93.5, X -27.2-215.5, Z 93.3-188.3 | top (+Y); text at X -15 to -5, Z 97-103 |
| B1 (not used in this stretch) | NAUO1 | ARA_B1 | flat plate, Y 87.5-90.5 | top (+Y) |
| base servo | NAUO45 | MG90S | X 157.6-169.9, Y 91.6-123.9, Z 119.4-151.6; shaft points down (-Y) at X 163.7, Z 140.9 | - |
| horn, double-ended | NAUO46 | 2PartShoulder_Mirrored | X 145.5-181.8 (36.3 long), Z 137.5-144.2, arms Y 90.2-92.2, hub up to Y 94.4 | - |

The video confirms the R5 / R6 swap already recorded in `guide.py` (engraved R5 = NAUO15, engraved R6 = NAUO14).

---

## 1. State at the start (0:00)

Still: `docs/research/mra/stills/base/t00m00s.jpg`.

- Nothing of the base is built. On the worktop, upper left: an Arduino Nano on its blue I/O expansion shield (yellow 3-pin header
  rows), and above it two joystick modules (black thumb caps), each wired to the shield by a 5-way rainbow ribbon of jumper wires.
  These stay untouched for the whole stretch.
- Far left: one MG90S servo lying on its side (pink "TowerPro MG90S Micro servo" label). **A black double-ended horn is already on
  its shaft.** Its lead (brown / red / orange) runs in a loop across the worktop and is plugged into the shield, at a 3-pin position
  on the header block at the corner of the shield furthest from the power jack. The pin label on the shield cannot be read. The lead
  carries a white paper flag marked "5" a few centimetres from the plug.
- Top right: B1 and B2 lying stacked, codes readable. B1 stays there for the whole stretch.
- R1 is not in frame at 0:00; it is on the worktop by 0:12.

## 2. Timeline of every action

Certainty about codes: R1, R2, R3, R4, R5, R6 and B2 were each read directly from the engraving in a close-up (sure). No fastener of
any kind is used in this stretch. No servo is powered, centred or tested for motion. The horn is never removed, turned on its shaft or
screwed to wood.

1. **0:02 - 0:08. Unplug the servo.** Right hand steadies the shield; left hand pulls the plug of the lead flagged "5" straight up
   out of the shield. The servo is now loose, horn still fitted.

2. **0:09 - 0:17. Show the servo, pick up R1.** Servo held upright with the horn on top and shown to the camera. R1 is taken in the
   left hand with its engraved face towards the camera. The horn lies **across** the servo body, at right angles to the body's long
   axis (checked at full resolution at 0:17, again from below at 1:13, and at 4:22). That is the same as in the CAD (horn along X,
   body along Z). Still: `stills/base/t00m17s.jpg`.

3. **0:18 - 0:22. Horn through R1's cut-out, then the servo is seated.** The servo comes at R1 from the **engraved side**, horn
   first. In order (6 frames a second):
   - 0:18.0 - 0:18.5 the servo is laid over, one end of the horn leading;
   - 0:18.5 - 0:19.2 one tip of the horn is dipped into the rectangular cut-out (still: `stills/base/t00m19s.jpg`);
   - 0:19.2 - 0:20.7 the servo is swung towards upright so that the hub and then the other tip follow through (the black tip of the
     trailing arm is at the edge of the hole 0:20.3 - 0:20.7). During this the servo body is a quarter-turn away from where it
     ends up: the horn is in line with the long axis of the cut-out, so the body is across it;
   - 0:20.7 - 0:21.2 the whole servo is twisted a quarter-turn about its shaft, so the body lines up with the cut-out and the horn
     ends up across it;
   - 0:21.2 - 0:22 the body is pressed down into the cut-out until its two mounting ears rest on R1's engraved face.
   Result: servo body on the engraved (top) side of R1, horn on the plain (under) side. In CAD terms the servo goes down (-Y) through
   R1; its ears sit at Y 103 on R1's top face. Nothing fastens the servo to R1.
   Lead at this stage: it leaves the servo case at the end nearer the output shaft (+Z end) and at the face furthest from R1 (the top,
   about Y 120-124), and trails away across the worktop to the right.

4. **0:22 - 0:49. Grip adjusted (0:24 - 0:26), then held still for the camera.** R1 tilted away, servo label towards the camera.

5. **0:50 - 0:57. R1 turned flat, engraved face up.** The view straight down matches the CAD top view of NAUO10: "R1" beside the
   edge where R4 will go, the comb of three slits at the opposite end.

6. **0:58 - 1:02. R2 on.** R2 (house shape with a hole at the apex) is brought over R1 with its engraved face up and leaning back,
   its open-bottomed notch over the servo body; it is stood upright and **pushed straight down** (towards R1, -Y) with the left
   thumb, so that the notch straddles the servo body between the ears and R2's feet enter R1's slots. R2's engraved face points
   towards the short end of the servo (-Z); the servo's shaft end, its label, its lead and R1's engraving are all on R2's plain side
   (+Z). R2 now traps the servo: in the CAD the top of R2's notch (Y 123.3) sits on the top of the servo case (Y 123.9).
   Still: `stills/base/t01m03s.jpg` (from R2's engraved side; the short end of the servo shows through the notch).

7. **1:03 - 1:31. Shown from both sides and from below.** 1:03 - 1:04 engraved side; 1:05 - 1:12 plain side; 1:12.3 - 1:14.3 flipped
   over to show the underside: the horn is below R1 and lies across the cut-out, R2's feet show through R1's slots, the lead with
   flag 5 trails to the left (still: `stills/base/t01m13s.jpg`); 1:14.7 - 1:31 held.

8. **1:32 - 1:47. Lead re-draped, assembly turned.** Right hand lifts the lead and lays it back over R1's +Z edge (the edge on
   R2's plain side). Then both sides are shown again.

9. **1:48 - 1:55. R3 on.** R3 is held up flat, code readable (1:48 - 1:50), turned on edge with its engraved face pointing away
   from the servo, and **lowered straight down** at the end of R1 that has the comb of three slits, i.e. the end furthest from
   the "R1" engraving (+X; CAD X 192.7-195.7). Its two feet go into R1's two slots and its bottom-opening slot passes down over R2's
   side tab (this last point is how it looks; the tab itself is hidden by fingers). Pressed home with the right fingers 1:54 - 1:55.
   Engraved face outwards (+X). Lead not touched. Still: `stills/base/t01m52s.jpg`.

10. **1:56 - 2:11. Held, then turned round** so R2's engraved side faces the camera.

11. **2:12 - 2:16. R4 on.** R4 held up, code readable (2:12 - 2:13). R4 has an L-shaped cut in its top edge: a narrow slit down from
    the edge with a square opening at its foot. R4 is **lowered straight down** at the other end of R2 from R3, beside the "R1"
    engraving (-X; CAD X 131.9-134.9), feet into R1's slots, slot over R2's tab, pressed home with the right fingers. Engraved face
    outwards (-X). The lead is held up out of the way while R4 goes on.

12. **2:17 - 2:45. Held and turned.** R4's face is shown (still: `stills/base/t02m23s.jpg`): the servo case is visible through the
    square opening of the L-slot. The lead comes up out of the open top and hangs over R4's top edge near its +Z corner. It is not in
    the L-slot. 2:36 - 2:45: turned to show the open side that R2's engraved face looks at.

13. **2:46 - 2:58. R5 on.** R5 picked up, code readable (rectangular window with two small holes, a hook at one top corner). It is
    laid over the open side that R2's engraved face looks at (-Z), engraved face outwards, and **pressed on square to its own face**
    (towards R2, +Z): the side tabs of R3 and R4 come through R5's four small slots and R1's edge tab through the slot near R5's
    bottom edge. The builder presses with both thumbs at several points for about 10 s. The lead is on the other side of R2 and
    is not involved.

14. **3:00 - 3:19. Held,** R5's face to the camera.

15. **3:20 - 3:24. Turned over; lead cleared.** The box is turned so the remaining open side (+Z, R2's plain side, the side with the
    servo label and the lead) faces the camera. The right hand takes the lead, which was hanging out through that open side, and
    lifts it up and out through the open top of the box (3:21 - 3:22); the left hand then holds it there. If this were not done,
    R6 would trap the lead.

16. **3:25 - 3:36. R6 on.** R6 (the mirror image of R5, taller, hook at the other top corner) is laid over the +Z open side,
    engraved face outwards, and pressed on square to its own face (towards R2, -Z) with both thumbs. Code readable from 3:33.
    Still: `stills/base/t03m34s.jpg`.

17. **3:37 - 3:58. Shown; where the lead is.** At 3:37.0 and 3:42.0 R4's outer face is square to the camera with R6 fitted. The lead
    comes up out of the open top, **over the top edge of R4** about 10 mm to the R6 side of the L-slot's slit, and hangs down R4's
    outer face in front of the square opening (still: `stills/base/t03m42s.jpg`). **It is not in the L-slot, and the builder does
    nothing to put it there.** 3:43 - 3:58: R6's face, then a three-quarter view held still (R5 far, R6 near, R2 between them).

18. **3:59 - 4:07. B2 fetched.** Right hand takes B2 from the pile at the top right, shows it (code readable at 4:05, engraved face
    up) and lays it flat on the worktop, engraved face up. B2 has a round hole joined to one long edge by a straight slot (a keyhole).

19. **4:08 - 4:13. Turret shown over B2, then its underside.** 4:08 - 4:10 the turret is held upright above the keyhole end of B2,
    seen from above (the inside is visible: servo, R2, the lead leaving over R4). 4:10.5 - 4:13.5 the turret is tipped onto its side
    in the left hand to show the horn underneath, while the right hand picks B2 up again by its far end.

20. **4:14 - 4:17. Turret into B2's slot.** Done in the air, turret in the left hand, B2 in the right, both tilted towards the camera.
    The turret is offered to the **open end of B2's slot** with the horn on B2's plain (under) side and the bottom edges of R5 and R6
    on B2's engraved (top) side, and slid along the slot until the servo's round boss is in the round hole (4:14.75 start;
    4:15.25 - 4:15.75 the round hole is still visible beyond the turret, still: `stills/base/t04m15s.jpg`; 4:16.0 the hole is
    covered; 4:16.5 seated). R5 faces the open end of the slot, R6 is at the far side. In CAD terms the turret moves +Z relative to
    B2, about 47 mm (shaft from the plate edge at Z 93.3 to the hole centre at Z 140.8). B2's slot is 12.7 mm wide, the servo body
    12.3 mm.

21. **4:17 - 4:21. Set down; lead moved aside.** The pair is put on the worktop. 4:18 - 4:19 the right hand picks the free end of
    the lead off B2 and lays it out to the right, clear of the plate. It still leaves the box over R4's top edge.

22. **4:21.75 - 4:23.5. Underside shown.** Lifted and turned over: the horn is below B2 and lies **across** the slot at the round
    hole, with a silver screw in its centre (the horn is screwed to the servo shaft; that was done before the video). R5's code is
    readable above. Still: `stills/base/t04m22s.jpg`.

23. **4:23.75 - 4:29. Set down again and pushed home.** 4:25 - 4:26 the right thumb pushes on R5's face, towards the round hole,
    while the left hand holds B2. 4:27 B2's code is shown. 4:28 - 4:29 put down.

24. **4:30 - 4:42. Held still.** Left hand resting on the worktop. Nothing else happens before the end of this stretch.

## 3. State at the end (4:40)

Still: `docs/research/mra/stills/base/t04m32s.jpg`.

- Built: R1 + base servo (horn fitted) + R2 + R3 + R4 + R5 + R6, standing on the keyhole end of B2. B2 lies flat on the worktop,
  engraved face up, its long end running towards the lower right of the frame with the code "B2" at the corner nearest the builder.
  R5 faces the builder, with the open end of B2's slot showing in front of it; R6 is at the back. The horn is under B2.
- The servo lead comes up out of the open top of the turret, over R4's top edge near the R6 corner, and arcs out to the right; its
  plug and the "5" flag lie on the worktop to the right of the turret. It is not plugged in and not in R4's L-slot.
- Not yet done: B1 (still on the pile at the top right), any screws, R7 / R8, plugging the servo back in.
- Nano, shield and joysticks are where they were at 0:00 (now mostly out of frame, top left).

## 4. Lee's points, checked against this stretch

| Lee's statement | What the video shows |
|---|---|
| The base servo arrives with its double-ended horn already fitted | Yes. The horn is on the servo at 0:00 and is never fitted, removed or turned on its shaft. A screw is in its centre (4:22). |
| The horn is angled through a slot in R1 | Yes, 0:18 - 0:22, from R1's engraved side, one tip first; the servo is a quarter-turn round while the horn passes and is then twisted a quarter-turn and pressed down. |
| R2 then slides over the servo with its tabs entering R1's slots | Yes, 0:58 - 1:02, straight down, engraved face towards the short end of the servo. |
| After R6 the servo lead is moved into the L-shaped slot in R4 | **Not seen in 0:00 - 4:42.** The lead is lifted out of the way before R6 (3:20 - 3:24); after R6, and still after B2, it lies over R4's top edge beside the slot. If it is put in the slot, that is after 4:42. |
| B2's slot slides in above the servo horn and below R5 / R6 into B2's round cut-out | Yes, 4:14 - 4:17, with both parts held in the hands, then pushed home by thumb at 4:25. |
| Then the horn fits into the horn-shaped cut-out in B1; then six 6 mm screws | After this stretch. |

Order actually used: unplug servo, servo into R1, R2, R3, R4, R5, R6, turret onto B2.

## 5. Hard to show in a 3D guide, or where video and CAD may differ

1. **The servo cannot go into R1 in a straight line.** R1's cut-out is 12.3 mm wide (X 157.6-169.9) and 29.1 mm long counting the
   narrow notch at its +Z end (Z 124.1-146.8, notch 5.7 mm wide on to Z 153.2); the horn is 36.3 mm long. The move is: horn in line
   with the cut-out, tilt, one tip through, level, quarter-turn about the shaft, press down. The collision test in `stepgen.py` will
   find no free straight direction for servo + horn as one group; this needs a hand-set path with a tilt and a turn.
2. **`guide.py` has the servo going into R2 first, then R2 + servo onto R1.** On video the servo goes into R1 first and R2 comes
   down over it afterwards.
3. **`guide.py` brings the horn (NAUO46) in with B2** (`show=[B2, BASE_HORN]`). On video the horn is part of the servo from the start.
4. **In the CAD the horn overlaps B2.** Horn arms: Y 90.16-92.21. B2: Y 90.5-93.5. A point in the middle of either horn arm
   (X 150 or 178, Y 91.5, Z 140.8) tests as inside B2's solid. The clearance modelled between the servo case face (Y 94.6) and the
   top of the horn arms (Y 92.2) is 2.4 mm, less than B2's 3.0 mm. On video B2 passes between the horn and R5 / R6 by hand with
   no visible force. So a slide of B2 along its slot cannot be collision-free in the CAD as it stands; the horn would have to sit
   about 1.7 mm lower, wholly in B1's layer (Y 87.5-90.5), where B1's horn-shaped cut-out (X 144.8-182.5, Z 136.9-144.8) waits for it.
5. **The turret-to-B2 join is done in the air with both parts tilted.** A guide would more naturally show B2 flat and the turret
   sliding in level along +Z, R5 trailing.
6. **The lead is a flexible part with a different position at almost every step** (trailing; over R1's edge; held up for R4; lifted
   out of the top before R6; over R4's top edge). The one handling move that matters for the build is 3:20 - 3:24: get the lead out
   of the +Z opening before R6 goes on.
7. **R5 and R6 engage several tabs at once** (four side tabs from R3 / R4 plus R1's edge tab) and take about 10 s of pressing at
   different points. A single straight push in the guide is right in direction but hides that effort.
8. **R3 and R4 look alike.** On video the difference that is easy to see is the L-shaped cut in R4's top edge; R4 goes at the end of
   R1 nearest the "R1" engraving, R3 at the end with the comb of three slits.
9. **Which way round the servo sits** depends on R1's cut-out: the shaft end is the end with the narrow notch (+Z), on R2's plain
   side. The lead leaves the case at that same end.
10. **The start is a disassembly step.** The servo begins plugged into the shield with a "5" flag on its lead; the first action is
    to unplug it. The shield's pin label is not readable on video.

## 6. Reference stills (1280 px, in `docs/research/mra/stills/base/`)

- `docs/research/mra/stills/base/t00m00s.jpg` - start: shield with two joysticks, servo with horn fitted and flagged lead plugged in, B1 / B2 pile.
- `docs/research/mra/stills/base/t00m17s.jpg` - R1 (engraved face) in the left hand, servo in the right with the horn across its body.
- `docs/research/mra/stills/base/t00m19s.jpg` - first tip of the horn entering R1's cut-out from the engraved side, servo tilted.
- `docs/research/mra/stills/base/t01m03s.jpg` - R2 seated on R1, seen from R2's engraved side; short end of the servo through R2's notch.
- `docs/research/mra/stills/base/t01m13s.jpg` - underside of R1: horn below the plate, across the cut-out; lead with flag 5.
- `docs/research/mra/stills/base/t01m52s.jpg` - R3 on edge being lowered at the comb end of R1; servo label and lead on R2's plain side.
- `docs/research/mra/stills/base/t02m23s.jpg` - R4 fitted, outer face: L-shaped slot in the top edge, lead over the top edge, flag 5.
- `docs/research/mra/stills/base/t03m34s.jpg` - R6 being pressed on, code readable.
- `docs/research/mra/stills/base/t03m42s.jpg` - after R6: lead over R4's top edge beside the L-slot, not in it.
- `docs/research/mra/stills/base/t04m15s.jpg` - turret entering the open end of B2's slot; B2's round hole still visible beyond it.
- `docs/research/mra/stills/base/t04m22s.jpg` - underside of B2: horn below the plate, across the slot, screw in its centre.
- `docs/research/mra/stills/base/t04m32s.jpg` - end of stretch: turret on B2, lead out over R4 to the right, no B1, no screws.
