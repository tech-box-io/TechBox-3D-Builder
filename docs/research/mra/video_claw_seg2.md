# Claw.mov, stretch 2 (2:20 to 4:55): what the builder does

Status: COMPLETE for this stretch. Overview at 2 s spacing over 2:20-4:56 (10 sheets, all read), then every action re-read at 1 s spacing
from native-size frames (1080 x 1920) and enlarged crops. I also looked at 2:16-2:19 and, at 2 s spacing only, at 4:57-5:12, to help the merge.

Source: `/Users/lee-johnson/Desktop/Claude_Cadasio/MRA_Videos/Claw.mov` (7:06 = 425.6 s, portrait phone video, hand held, looking down at a
worktop). All times are the video's own. This file covers video seconds 140 to 295.

Codes in this report are the ones ENGRAVED on the wood, written in quotes where they differ from the CAD mesh name. CAD ids, hole sizes and
coordinates (mm, assembly space, Y up) are taken from `docs/research/mra/cad_arm_claw.md` and `mra_instances.json`; I did not re-measure the CAD.

Words used for directions on the worktop (the same as in `video_claw_seg1.md`): "far" = the C1 side of the claw (+Z in assembly space),
"near" = the C2 side (-Z), "back" = the tongue end of C3 where the lead leaves (-X), "front" = the jaw tips (+X).

## 0. What this stretch contains, in one paragraph

Two things happen. First the claw sub-assembly is finished on the worktop, upside down (jaw side up): the driven jaw is already over the
horn, the cover C9 is pressed onto the clip prongs, the second jaw is slid in sideways under the cover, one M3x10 screw is driven through the
cover and that jaw as its pivot, and the jaws are opened and closed once by hand. Then the robot is pulled into view, the claw is turned the
right way up and screwed to the two strips on ONE side of the arm (engraved "A12" and "A13", the +Z side) with two short screws into
clip C1. The third claw screw (other side, into C2), the lead routing, the coupler / extension, the shield rows and any power-up are all
AFTER this stretch. No wire is plugged in or routed, no servo is powered or centred, and no horn is fitted, removed or turned here.

Engraved codes read in this stretch, with the CAD part each one is (all agree with the "engraved text" column in section 9 of `cad_arm_claw.md`):

| Engraved | Read at | How sure | What it is | CAD id | CAD mesh name |
|---|---|---|---|---|---|
| "C6" | 2:18 | certain | keyhole plate (top of the stack as it lies upside down) | NAUO35 | ARA_C4 |
| "C7" | 2:24 | certain | jaw with the horn-shaped slot (driven jaw) | NAUO39 | ARA_C8 |
| "C8" | 2:26, 2:48 | certain | jaw with the 2.8 mm pivot hole (geared jaw) | NAUO38 | ARA_C7 |
| C9 | 2:41 | certain | cover with the 11.7 mm hole | NAUO40 | ARA_C9 |
| C1 | 2:48, 4:03, 4:54 | certain | clip plate with two small holes, far (+Z) side | NAUO32 | ARA_C1 |
| "C5" | 4:55 | probable (half hidden under C1) | spacer bar on the C1 side | NAUO37 | ARA_C6 |
| "A12" | 3:48, 4:54 | certain | levelling link, triangle cut-out by its elbow hole | NAUO27 | ARA_A9 |
| "A13" | 3:48, 4:54 | certain | forearm strip on the +Z side, square cut-out by its elbow hole | NAUO28 | ARA_A10 |
| "A10" | 4:54 | certain | triangle plate at the elbow | NAUO26 | ARA_A8 |
| "A8" | 4:54 | certain | upper-arm side strip, +Z side | NAUO24 | ARA_A6 |
| "A9" | 4:54 | probable (small, sideways) | T-piece (wooden nut) in the cross plate | NAUO30 or NAUO31 | ARA_A12 |
| "A6" | 3:38 | certain | cross plate of the upper arm (two square holes, two cross-slots) | NAUO29 | ARA_A11 |
| "R6" | 4:54 | certain | turret side plate on the +Z side | NAUO14 | CAD R5 |
| R4 | 3:40 | certain | turret cross wall | NAUO13 | R4v2 |
| B8 | 3:40 | certain | lid of the joystick box (words Shoulder, Elbow, Base, Claw) | NAUO8 | CAD B9 |

C2, C3 and the spacer "C4" are in the claw but their codes are not readable anywhere in this stretch.

## 1. State at the start (2:20; described from 2:17-2:18, just before the first action)

Still: `docs/research/mra/stills/claw/t02m18s.jpg`.

- The claw body lies on the worktop UPSIDE DOWN compared with the CAD pose: the servo case and the bodies of the clips are underneath, the
  plate engraved "C6" (NAUO35) is on top with its engraving up. The back (tongue of C3) is to the left of the frame, the front to the right,
  the far (C1, +Z) side at the top of the frame.
- Already assembled (segment 1's work): C3 (NAUO34) at the bottom of the stack with the claw servo (NAUO72) through it; the two spacer bars;
  plate "C6" on them; both clips. The clip prongs stand up through "C6" in pairs with a slit between them, each pair with a small hook: one
  pair at the far back corner (C1, NAUO32) and one at the near back corner (C2, NAUO33). Just inside the C1 prongs a second slot shows the
  flush tab of the far spacer bar; at the near side the bar's tab shares the slot with the C2 prongs. This matches the CAD (C1 prongs at
  z 164.7 and the bar tab at z 157.2 in separate slots; C2 prongs at z 128.05 and the bar tab at z 131.05 in one double slot).
- Two silver socket-head cap screws are already down in "C6", both on the centre line: one behind the horn hub near the "C6" engraving and
  one in the lug at the front edge (the M3x16 pair, NAUO74 at [322.93, 176.84, 147.11] and NAUO75 at [347.24, 176.58, 147.03]).
- The small pivot hole of "C6" (2.3 mm, at [335.39, y, 156.09]) is empty, at the far front of the plate.
- The black single-arm servo horn (NAUO73, six small holes along the arm) is already on the shaft with a silver cross-head screw in its hub.
  It stands in the keyhole of "C6", above the plate, arm pointing to the front, parallel to the long axis of the claw to within about 15
  degrees. The hub is off-centre towards the near side (CAD: shaft at z 138.76, plate centre line z 147).
- The legs of C1 and C2 stick out at the back left, one hole visible in each. The servo lead (brown / red / orange) comes up through the
  rectangular hole in the tongue of C3 and trails off to the top of the frame; black 3-pin socket on its end, nothing joined to it.
- Loose: jaw "C7" (about to be picked up), jaw "C8" and cover C9 out of frame to the right, the dark grey T-handle hex driver at the top
  edge (the builder puts it down there at 2:16, after the second M3x16 screw, and lets go of the claw).

## 2. Timeline

Directions are given as seen and, in brackets, in assembly space for the CAD pose. Because the claw is upside down on the worktop,
"lowered onto the stack" is +Y in assembly space.

1. **2:18-2:23 - jaw engraved "C7" (NAUO39) onto the horn.** (Overlaps segment 1, which has it as its step 12.) Right hand brings the jaw
   from the right, engraved face up. It is held tilted, gear end low, and the round end of its horn-shaped slot is put over the horn hub
   (2:19-2:20); then it is levelled and pressed flat with the left forefinger on the gear end (2:21-2:22). Seated at 2:23: the horn arm lies
   in the slot, flush, all six horn holes visible; nothing is screwed through the horn into the wood. The jaw takes the horn's angle and
   points to the front. Engraved face up = away from "C6" (assembly space: engraving faces -Y, jaw moves +Y; horn at
   [342.02, 178.14, 137.91]). Still `t02m24s.jpg`.
2. **2:24-2:28 - jaw engraved "C8" (NAUO38) tried in place, then taken off again.** Right hand lays the second jaw on "C6", engraved face
   up, its 2.8 mm hole over the pivot hole of "C6", gear teeth meshed with the teeth of "C7", both jaws closed so the two half-round bites
   make one round hole (2:26). One second later it is lifted off and put down at the top of the frame (2:27-2:28). No screw. Certain about
   what happens; the reason is a guess (nothing holds this jaw until the cover and screw are on). Still `t02m26s.jpg` - the clearest view
   of how the two gears mesh, because the cover is not yet on.
3. **2:29-2:41 - cover engraved C9 (NAUO40) pressed onto the clip prongs.** Right hand brings C9 from the right, engraved face up
   (2:30), and lowers it flat onto the stack: its two short slots over the two pairs of prongs, its 11.7 mm hole over the horn hub (the horn
   screw shows through it), its small hole over the pivot hole, the code "C9" at the back edge reading the same way as "C6" did (2:31-2:32).
   From 2:33 to 2:40 both hands squeeze it down, thumbs and fingers at the back corners over the prongs. At 2:41 the hands are off: the prong
   tips with their hooks stand 2 to 3 mm through the slots of C9 (CAD: 3.3 mm), and the cover sits level on jaw "C7". The front cap screw head stays
   visible just beyond the front edge of C9. I cannot see or hear the barbs snap; the prongs standing through is the evidence that it is
   home. (Assembly space: C9 moves +Y to y 173.6-176.6; engraving faces -Y.) Still `t02m41s.jpg`.
4. **2:42-2:53 - jaw "C8" (NAUO38) slid in under the cover.** Right hand picks jaw "C8" up again (2:42-2:45). Left hand lifts the claw off
   the worktop, still jaw side up (2:46). The jaw is held flat, engraved face up, and its GEAR END is pushed into the 3 mm gap between C9
   and "C6" at the far front corner (2:46-2:48: the gear is half under the cover), then slid further in towards the middle and back
   (2:49-2:51) until its teeth mesh with "C7" and its hole shows through the small hole of C9 (2:52-2:54). Both jaws end closed, tips
   together. (Assembly space: the jaw moves in its own plane, y 176.6-179.6, from the +Z front corner, i.e. mostly -Z with some -X. The CAD
   report found this jaw free to leave along +Z with C9 on, which is the same path backwards.) Still `t02m48s.jpg`.
5. **2:54-3:03 - pause.** Claw held still in the left hand and shown to the camera; tilted once at 3:02 to look at its side. No change.
6. **3:04-3:09 - pivot screw placed (NAUO76).** Right arm reaches off-frame (3:04) and comes back with one silver socket-head cap screw
   held by the head (3:05). It is dropped, thread first, into the small hole of C9 (3:06). At 3:07-3:11 it stands upright in the hole with
   about 4 mm of shank showing under the head. That is what an M3x10 does here (3 mm of C9 and 3 mm of jaw are clearance, then the thread
   meets the 2.3 mm hole in "C6"), so: M3x10, fairly sure. (Assembly space: [335.39, 170.7, 156.09], pointing +Y.) Still `t03m07s.jpg`.
7. **3:12-3:28 - pivot screw driven.** T-handle hex driver picked up (3:12), put in the head (3:13), turned from 3:14 to 3:27 while the
   left hand holds the claw flat on the worktop; driver lifted away at 3:28. The head ends down on C9. How tight it was left cannot be seen;
   the jaws swing freely straight afterwards (next action), so it is not clamping the jaw.
8. **3:29-3:32 - jaws tested by hand.** With the driver still in the right hand, right finger and thumb pull the tip of jaw "C8" outwards
   to the far side while the left hand pulls the tip of "C7" to the near side (3:29-3:31): both jaws swing open together, roughly 30 to 40
   degrees each, turning the servo horn (the unpowered servo is being turned by hand through the jaw). Pushed closed again at 3:32. This is
   the only motion test in the stretch. Still `t03m30s.jpg`.
9. **3:33-3:36 - claw and driver put down.** Finished claw lies jaw side up (C9, "C8", "C7" readable, lead trailing); at 3:36 the left hand
   pushes it aside.
10. **3:37-3:41 - the robot is pulled into frame.** A hand drags the base in by the joystick box (3:37-3:39). See "State of the robot"
    below. The claw is picked up (3:40), the lead is held near its plug for a moment and let go (3:41), and by 3:42 the right hand has
    the claw. Still `t03m40s.jpg`.
11. **3:42-3:53 - claw turned the right way up and offered to the two strips on the +Z side.** The claw is now servo case and clip bodies
    up, jaws and C9 underneath, jaw tips pointing away from the arm, tongue of C3 towards the arm, lead hanging from the back. The two
    strips "A12" (upper, NAUO27) and "A13" (lower, NAUO28) hang folded down from the elbow beside the upper arm; the left hand swings them
    up and outwards (3:44) and then pinches their free ends together (3:45 onwards). The right hand brings the claw to the free ends of
    the strips from beyond them, so that the OUTER face of clip C1 (the engraved one) lies against the INNER face of both strips
    (3:45-3:46), and shuffles it until the hole in the body of C1 is behind the end hole of "A12" (3:47-3:53). The claw is held only by
    the hands. The strip on the other (-Z) side of the arm is not involved. (Assembly space: C1 outer face z 166.2 against the strips; the
    claw comes back along the forearm, direction about [-0.91, 0.41, 0], and up against the strips in +Z.) Still `t03m46s.jpg`.
12. **3:54-4:03 - first claw-to-arm screw placed (NAUO77).** Right arm reaches off-frame to the left (3:54-3:56), returns with a short
    silver socket-head cap screw (3:57-3:59) and starts it by hand from the OUTSIDE (+Z: the right-hand side of the robot as seen from the
    controller end, which is where the builder sits) through the end hole
    of the UPPER strip "A12" into clip C1 (4:00-4:03; the right forefinger steadies the top of the servo at 4:02). At 4:03 the head sits
    in the end of "A12" with the code C1 readable on the clip just beyond it. Screw length judged by eye: shank about as long as the head
    is wide, so 6 mm (the CAD has M3x6 here). (Assembly space: [311.98, 205.67, 172.23], pointing -Z; "A12" hole 2.8 mm clearance, C1 hole
    2.3 mm thread.) Still `t04m00s.jpg`.
13. **4:04-4:16 - first screw driven.** T-handle driver from the same (+Z) side, turned 4:05-4:15, taken away at 4:16. Left hand holds
    strips and claw together throughout.
14. **4:17-4:27 - pause, then the claw is swung on that screw.** 4:17-4:23 nothing moves (right hand off-frame). At 4:24-4:27 the right
    hand takes the claw by the jaw end and turns it about the first screw until the hole in the leg of C1 is behind the end hole of the
    lower strip. So the first screw is left free enough to pivot.
15. **4:28-4:35 - second claw-to-arm screw placed (NAUO78).** Right arm reaches off-frame again (4:28-4:29), returns with another short
    cap screw (4:30) and starts it by hand, same side, through the end hole of the LOWER strip "A13" into the leg of C1 (4:31-4:35). At
    4:32 and 4:35 both heads are visible, one above the other. (Assembly space: [301.81, 188.27, 172.23], pointing -Z: the wrist axis.)
    Still `t04m30s.jpg`.
16. **4:36-4:52 - second screw driven.** Driver picked up (4:36), turned 4:37-4:51, put down (4:52).
17. **4:52-4:56 - result shown.** The left hand lets go; the right hand holds the claw by the jaws while the camera drops to look at the
    +Z side square on (4:54-4:55), then goes back to the view from above (4:56). Still `t04m54s.jpg`.
18. **4:57 onwards (outside this stretch; 2 s spacing only).** The robot is turned end for end so its other (-Z) side faces the builder
    (4:57-4:58) and by 5:06-5:12 both hands are at the claw end on that side with a screw: this is where the third claw screw (through the
    -Z forearm strip into C2, NAUO79) goes in. Left for the next segment to confirm.

### State of the robot when it comes into frame (3:38-3:41)

- Base plate with the joystick box nearest the builder. Lid B8, engraved "Shoulder" and "Base" by one joystick and "Elbow" and "Claw" by
  the other, each with a pair of arrows.
- Behind the box the Arduino Nano on the blue I/O shield (gold mini-USB socket EMPTY: no USB cable in), the rainbow jumper ribbon looping
  over to the left, and three servo leads (brown / red / orange) plugged into the shield at the joystick-box end. I cannot see which rows.
- **Wire flag:** one of those servo leads carries a black flag with a white printed, underlined **6** (underline below the digit, so it is
  a 6 and not a 9), clear at 3:38, 3:39, 3:40, 3:41 and 3:43. I cannot tell which servo that lead comes from. A second dark tag and a
  loose black plug end are half hidden behind it; the mark on the tag could be a 7 but that is a guess. (Segment 1 read a white tape flag
  with a handwritten 5 at 0:00; I do not see that one here.)
- Turret with cross wall R4, a servo on each side of it (red and dark labels, clamp plates over them), leads from both running down to the
  shield. Upper arm standing up at about 60 degrees, leaning away from the controller: two side strips joined by the cross plate "A6"
  (NAUO29) with its two square holes and two cross-slots, each with a T-piece and a long screw through it. A three-layer stack (the lever)
  is on the -Z side at the shoulder.
- At the elbow, on the +Z side: the triangle plate and the strips "A12" and "A13", each already screwed at its elbow end, hanging down
  along the upper arm. On the -Z side one strip stands up past the elbow with a screw near its top; at 4:54 a strip with an empty hole in
  its free end hangs down behind the arm on that side. Guess: that is the -Z forearm strip (CAD A4, NAUO22, engraved "A5" per the CAD
  report), not yet joined to anything at its claw end.
- A white USB power block with a black cable lies at the top right corner of the frame, not connected to the robot.

## 3. State at the end (4:55)

Still: `docs/research/mra/stills/claw/t04m54s.jpg`.

- The claw is complete: C3, servo, two spacer bars, "C6", two M3x16, horn with its screw, jaw "C7" on the horn, cover C9 snapped over the
  prongs of C1 and C2, jaw "C8" between C9 and "C6" on its M3x10 pivot screw. Jaws closed.
- The claw hangs on the arm by TWO screws, both on the +Z side, both through a strip into clip C1: "A12" into the body of C1 (upper hole,
  NAUO77) and "A13" into the leg of C1 (lower back corner, NAUO78). Screw heads outwards (+Z). The claw is the right way up: servo case
  and clip bodies on top, C9 underneath, jaws pointing away from the arm. C1 is engraved on its outer face and readable beside "A12".
- The -Z side of the claw (clip C2) is not yet screwed to its strip.
- The claw servo lead leaves the top of the servo case at the end away from the strips (the C2 end, -Z), crosses the top of C3
  diagonally to the back, goes DOWN through the rectangular hole in the tongue of C3 and hangs loose below the claw, behind the end of
  "A13": roughly 10 cm hanging (the whole lead looks 15 to 20 cm long, judged against the 86 mm strip), with its black 3-pin socket
  lying on the worktop. It is not threaded through the cross plate "A6", not joined to a coupler or extension, and not
  plugged in.
- Three other servo leads are in the shield; no USB or power is connected.

## 4. Hard to show in a 3D guide, or different from the CAD

- **The claw is built upside down, then turned over.** Everything up to 3:33 is done with the jaw side up; at 3:40 the claw is turned
  servo side up to go on the arm. The guide needs a view change (or a "turn the claw over" card) between the claw sub-assembly and the step
  that joins it to the arm.
- **Order differs from the CAD-derived order.** `cad_arm_claw.md` section 7.5 has both jaws, then C9, then the pivot screw, then clips C2
  and C1 last. On video the clips are in from the start, C9 is pressed onto their prong tips with only jaw "C7" in place, and jaw "C8" is
  slid in sideways AFTER the cover. The CAD report already found both variants free (clips first with C9 pushed onto the prong tips; the
  pivot jaw free along +Z with C9 on). For a 3D guide the simpler picture is the trial position at 2:26 (jaw "C8" laid on, then C9); the
  builder chose not to do that, and I do not know whether that is TechBox's intended method or a habit.
- **C9 is a snap fit.** It takes about eight seconds of squeezing with both hands (2:33-2:40). A rigid model can only show the cover
  arriving; the caption has to say to press until the prong tips stand through the slots.
- **The horn screw is not in the CAD.** A small silver cross-head screw is in the horn hub from before this stretch. C9's 11.7 mm hole
  leaves it reachable afterwards (visible through the hole at 2:41 and 3:07).
- **The driven jaw is not fixed to the horn.** It is only pressed over it; C9 above and "C6" below keep it there. The CAD shows up to
  0.35 mm of overlap between horn and slot (a push fit), which matches the finger pressure used at 2:21-2:22.
- **Pivot tightness.** Three screws in this stretch are pivots (NAUO76, NAUO77, NAUO78). All are driven until the head is down, and the
  parts still turn afterwards (jaws at 3:29, claw on the first arm screw at 4:24). A guide cannot show "snug but free"; it needs words.
- **The jaw test back-drives the servo by hand.** At 3:29-3:32 the jaws are pulled open and pushed shut with the servo unpowered. Whether
  TechBox wants students to do that is a question for Lee.
- **The arm is not in the CAD pose.** In the CAD the forearm sticks out at 24 degrees below horizontal with the claw level. On video the
  strips hang folded against the upper arm and are lifted by hand to meet the claw; the claw goes onto the +Z strips alone, one screw at a
  time, and is swung about the first screw to find the second hole. The CAD report's step W1 (finished claw slid into the fork between
  both sides, then NAUO79, NAUO78, NAUO77) is a different order: video order is NAUO77 ("A12"), NAUO78 ("A13"), and only then the -Z side.
- **Flexible lead.** The lead just hangs during all of this. Its path over C3 and down through the tongue hole agrees with what the CAD
  report says is modelled, but the loose length below the claw has no CAD equivalent at this stage.
- **Hands hold everything.** From 3:45 to 4:52 the left hand is the clamp for two strips and the claw. In 3D the claw will simply appear
  in place against the strips.
- **Screw lengths are judged by eye.** M3x10 for the jaw pivot (4 mm proud before driving) and 6 mm for the two arm screws (short shank
  at 3:59 and 4:30) both agree with the CAD; I could not measure them.

## 5. Reference stills

All in `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/claw/` (720 x 1280).

- `docs/research/mra/stills/claw/t02m18s.jpg` - start of the stretch: claw upside down, plate "C6", horn with its screw, two M3x16 heads, clip prongs, lead through the tongue.
- `docs/research/mra/stills/claw/t02m24s.jpg` - jaw "C7" seated over the horn, engraved face up.
- `docs/research/mra/stills/claw/t02m26s.jpg` - jaw "C8" tried in place: gear mesh and pivot hole visible with no cover on.
- `docs/research/mra/stills/claw/t02m41s.jpg` - cover C9 pressed on: prong tips through its slots, horn screw in the big hole, pivot hole still empty.
- `docs/research/mra/stills/claw/t02m48s.jpg` - jaw "C8" being slid, gear end first, into the gap between C9 and "C6"; clip C1 with its two holes at the top.
- `docs/research/mra/stills/claw/t03m07s.jpg` - M3x10 pivot screw standing in the small hole of C9 before it is driven; both jaws in and closed.
- `docs/research/mra/stills/claw/t03m30s.jpg` - jaws pulled open by hand after the pivot screw is in.
- `docs/research/mra/stills/claw/t03m40s.jpg` - the robot before the claw goes on: arm standing, cross plate "A6", shield with the flag "6", lid B8.
- `docs/research/mra/stills/claw/t03m46s.jpg` - claw, right way up, held against the inside of strips "A12" and "A13".
- `docs/research/mra/stills/claw/t04m00s.jpg` - first short screw started by hand through the end of "A12" into C1.
- `docs/research/mra/stills/claw/t04m30s.jpg` - first screw in, second screw in the fingers; lead crossing C3 and going down through the tongue hole.
- `docs/research/mra/stills/claw/t04m54s.jpg` - side view at the end: "A12" (triangle mark) and "A13" (square mark) screwed to C1, "A10", "A8", "R6" readable, lead hanging.

Working frames (not part of the project): `/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/06aa2268-0605-4ce1-8b0c-854218069941/scratchpad/research_r2/video_claw_seg2/`
(`ov/` 2 s overview, `d1/` and `d2/` native-size frames at 1 s for 2:16-3:33 and 3:33-4:58, `p/` the crop sheets).

## 6. Open points for the merge

- Is jaw "C8" meant to go in after the cover (as on video), or with the cover lifted on over both jaws (as at 2:26)?
- Where and when is the claw servo centred? Not in this video up to 4:55; the horn was already on at 0:00 (segment 1).
- Which servo lead carries the flag "6", and what are the half-hidden tag and plug behind it (3:40)?
- The third claw screw (NAUO79, -Z strip into C2) and everything about the lead, coupler, extension and shield rows is after 4:57.
- How loose are the three pivot screws left? Not visible.
