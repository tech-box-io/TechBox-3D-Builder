# Base.mov (8:54): the rotating base and the two base plates

Status: COMPLETE. Merged from `video_base_seg1.md` (0:00-4:40) and `video_base_seg2.md` (4:25-8:54); both were read in full.
The overlap (4:10-4:42) is listed once. Where the two disagreed, or a point was marked unsure, the video was looked at again
(0:18-0:22 at four frames a second; 3:19-3:24, 3:36-3:44, 4:10-4:37 and 4:54-5:01 at two frames a second; 3:42 and 8:50 at native
1080 x 1920) and the CAD was measured again (`mra.glb`, mm, assembly space, Y up). What was re-checked, and how each
disagreement was settled, is in section 5.

Video: `/Users/lee-johnson/Desktop/Claude_Cadasio/MRA_Videos/Base.mov`, 533.6 s, portrait phone video looking down on a granite
worktop. Times are the video's own. The sound track was not used.

**Short answer.** The order on video is: unplug the base servo, servo (horn already on) into R1, R2, R3, R4, R5, R6, turret onto
B2, B2 onto B1, six screws, all six tightened again. Every one of Lee's points is confirmed except one: **the servo lead is never
put into R4's L-shaped slot**, in this video or (according to `video_controller_seg2.md`) in Controller.mov. R7 and R8 are not in
this video; they are servo clamp plates fitted in Arm.mov.

## Parts in this video

| Engraved code (read on video) | CAD id | CAD mesh name | Where it is when built (mm) | Engraved face |
|---|---|---|---|---|
| R1, turret floor | NAUO10 | ARA_R1 | flat, Y 99.96-102.96, X 127.6-200.3, Z 105.6-175.6 | top (+Y); text near the R4 end |
| R2, divider with the apex hole | NAUO11 | ARA_R2 | upright, Z 129.55-132.55, Y 96.6-167.9 | -Z (towards R5) |
| R3, end wall | NAUO12 | ARA_R3v2 | upright, X 192.67-195.67, Y 96.6-146.6 | +X (outwards) |
| R4, end wall with the L-shaped slot | NAUO13 | ARA_R4v2 | upright, X 131.94-134.94, Y 96.6-146.6 | -X (outwards, towards the controller end) |
| R5, side wall (the shorter one) | NAUO15 | ARA_R6 (CAD name swapped) | upright, Z 109.0-112.0, Y 93.53-175.4 | -Z (outwards) |
| R6, side wall (the taller one) | NAUO14 | ARA_R5 (CAD name swapped) | upright, Z 169.2-172.2, Y 93.53-185.0 | +Z (outwards) |
| B2, top plate | NAUO2 | ARA_B2 | flat, Y 90.53-93.53, X -27.2-215.5, Z 93.3-188.3 | top; text at the controller end, R5 side |
| B1, bottom plate | NAUO1 | ARA_B1 | flat, Y 87.53-90.53, same outline | top; same corner, so hidden once B2 is on |
| Base servo | NAUO45 | MG90S | X 157.6-169.9, Y 91.6-123.9, Z 119.4-151.6; shaft down, axis X 163.65, Z 140.85 | - |
| Horn, double-ended | NAUO46 | 2PartShoulder_Mirrored | 36.35 long along X (145.46-181.81), 6.65 wide at the hub, 3.2 at the tips | - |
| Screws, six | NAUO47-52 | M3x6mm_91292A111 | heads on B2 (Y 93.5-96.5), thread down to Y 87.5 | - |

The video confirms the R5 / R6 swap that `guide.py` already has. R7 (NAUO16) and R8 (NAUO17) do not appear.

Two people's hands are in the video from about 4:11 (fairly sure): the builder, whose left hand has rings and a watch, and a helper
whose hand comes in from the right (short nails, no rings; clearest at 4:25 and 5:38). The helper holds B2 for the slide and
drives the Allen key. Before 4:11 both hands look like the builder's.

---

## 1. What is built or laid out at the start (0:00)

Still: `stills/base/t00m00s.jpg`.

- Nothing of the base is built.
- Upper left: an Arduino Nano on its blue I/O expansion shield, and above it two joystick modules, each wired to the shield by a
  5-way ribbon of jumper wires. None of this is touched in the video.
- Far left: one MG90S servo lying on its side. **A black double-ended horn is already on its shaft** (a silver cross-head screw in
  its hub is visible later, at 4:22). Its lead (brown / red / orange) is plugged into a 3-pin position on the shield and carries a
  white paper flag marked "5" about 25-30 mm from the plug. The shield's pin label cannot be read in this video.
- Top right: B1 and B2 lying stacked, codes readable. R1 comes into frame by 0:12. R2-R6 are brought in from outside the frame.

## 2. Timeline

Codes R1, R2, R3, R4, R5, R6, B1 and B2 were each read from the engraving in a close-up (sure). No servo is powered, centred or
tested for motion at any point. The horn is never fitted, removed, turned on its shaft or screwed to wood. Directions are given
relative to the parts and in CAD axes.

| # | Time | Action |
|---|---|---|
| 1 | 0:02-0:08 | **Servo unplugged.** One hand steadies the shield, the other pulls the plug of the lead flagged "5" straight up out of the shield. The servo is now loose, horn on. |
| 2 | 0:09-0:17 | Servo held upright and shown, horn on top. R1 taken in the left hand, engraved face to the camera. The horn lies **across** the servo body (at right angles to the body's long axis), as in the CAD (horn along X, body along Z). Still `t00m17s.jpg`. |
| 3 | 0:18-0:22 | **Servo, horn first, through R1's cut-out, from R1's engraved side.** Four phases (still sequence `seq_00m18s_to_00m22s_servo_into_R1.jpg`): (a) 0:18.0-0:18.5 the servo is laid over at an angle, one tip of the horn leading; (b) 0:18.5-0:19.2 that tip is dipped into the cut-out (`t00m19s.jpg`); (c) 0:19.2-0:20.7 the servo is swung towards upright so the hub and then the other tip follow through; all this time the servo is a quarter-turn away from where it ends up, so the horn runs along the length of the cut-out and the body lies across it; (d) 0:20.7-0:21.2 the whole servo is spun a quarter-turn about its shaft, so the body lines up with the cut-out and the horn ends up across it underneath; 0:21.2-0:22.0 the body is pressed down until its two mounting ears rest on R1's engraved face. Result: body above R1, horn below R1. In CAD terms the last move is -Y; the ears' underside is at Y 102.96, R1's top face. Nothing fastens the servo to R1. |
| 4 | 0:22-0:57 | Grip adjusted, held for the camera; 0:50-0:57 R1 turned flat, engraved face up. |
| 5 | 0:58-1:02 | **R2 on.** R2 is brought over R1 leaning back, its open-bottomed notch over the servo body, stood upright and **pushed straight down** (-Y) with a thumb. The notch straddles the servo between the ears; R2's two feet go into R1's two slots (X 129.49-140.49 and X 187.24-198.24, Z 129.55-132.55). R2's engraved face points to -Z: the short end of the servo shows through the notch on that side (`t01m03s.jpg`); the shaft end, the label, the lead and R1's engraving are on R2's plain side (+Z). |
| 6 | 1:03-1:31 | Shown from both sides, then (1:12-1:14) turned over: horn below R1 and across the cut-out, R2's feet showing through R1's slots (`t01m13s.jpg`). |
| 7 | 1:32-1:47 | Lead lifted and laid back over R1's +Z edge; both sides shown again. |
| 8 | 1:48-1:55 | **R3 on.** Held up flat, code readable, turned on edge with the engraved face away from the servo and **lowered straight down** (-Y) at the +X end of R1 (the end away from the "R1" engraving). Its two feet go into R1's slots (X 192.67-195.67; Z 114.03-125.03 and 156.17-167.17) and its bottom-opening slot goes down over the end of R2. Pressed home with the fingers. Engraved face outwards (+X). Lead not touched. Still `t01m52s.jpg`. |
| 9 | 1:56-2:11 | Held, then turned so R2's engraved side faces the camera. |
| 10 | 2:12-2:16 | **R4 on.** Held up, code readable. **Lowered straight down** (-Y) at the other end, beside the "R1" engraving (-X): feet into R1's slots (X 131.94-134.94, same Z as R3's), slot over the other end of R2, pressed home. Engraved face outwards (-X). The lead is held up out of the way while R4 goes on. |
| 11 | 2:17-2:45 | Shown. R4's face (`t02m23s.jpg`): the L-shaped slot in its top edge, the servo case visible through the slot's pocket. The lead comes up out of the open top and hangs over R4's top edge near its +Z corner; it is not in the slot. |
| 12 | 2:46-2:58 | **R5 on.** Code readable. Laid over the open -Z side (the side R2's engraved face looks at), engraved face outwards, and **pressed on square to its own face** (+Z). The side tabs of R3 and R4 and R1's edge tabs come through R5's slots. Pressed with both thumbs at several points for about 10 s. The lead is on the other side of R2 and is not involved. |
| 13 | 3:00-3:19 | Held, R5's face to the camera. |
| 14 | 3:20-3:24 | **Lead cleared.** The box is turned so the remaining open side (+Z) faces the camera. The right hand takes the lead, which was hanging out through that open side, and lifts it up and out through the open top (3:21-3:22); the left hand then holds it there. Without this, R6 would trap the lead. |
| 15 | 3:25-3:36 | **R6 on.** Laid over the +Z side, engraved face outwards, **pressed on square to its own face** (-Z) with both thumbs. Code readable from 3:33 (`t03m34s.jpg`). |
| 16 | 3:37-3:58 | Shown. At 3:41-3:42 R4's outer face is square to the camera (`t03m42s.jpg`, native crop `crop_03m42s_R4_L-slot_and_lead.jpg`): the lead comes up out of the open top, **over R4's top edge 5-10 mm to the R6 side of the slot's stem**, and hangs down R4's face in front of the slot's pocket. **It is not in the L-slot and nothing is done to put it there.** |
| 17 | 3:59-4:07 | B2 fetched from the pile, shown (code readable at 4:05) and laid flat, engraved face up. It has a round cut-out joined to one long edge by a straight slot (a keyhole). |
| 18 | 4:08-4:14 | Turret held upright over the keyhole end of B2 (4:08-4:10), then tipped over in the left hand to show the horn underneath (4:10-4:14). B2 is picked up again and held from the right, engraved face up, slot mouth towards the turret (`t04m14s.jpg`). |
| 19 | 4:14.5-4:17.5 | **Turret into B2's slot**, both parts in the air and tilted (still sequence `seq_04m10s_to_04m21s_turret_into_B2.jpg`). The turret is offered to the **open end of the slot** with the horn on B2's plain (under) side and the bottom edges of R5 and R6 on B2's engraved (top) side; B2's edge passes between them. The turret is run along the slot, R6 side leading and R5 last, until the servo is in the round cut-out (4:15.25-4:15.75 the round cut-out is still visible beyond the turret, `t04m15s.jpg`; covered at 4:16.0; level and seated by 4:17). In CAD terms the turret moves +Z relative to B2. |
| 20 | 4:17-4:21 | Set down. The free end of the lead, lying across the controller part of B2, is picked off the plate and laid on the worktop on the R6 side (`t04m21s.jpg`). |
| 21 | 4:21.75-4:23.5 | Lifted and tipped back to show the underside (`t04m22s.jpg`, `t04m23s.jpg`): the horn lies flat under B2, across the round cut-out, long axis along the length of the plate (X), at right angles to the slot. The black end of the servo shows in the round cut-out and the inner end of the slot; R1's underside shows through the rest of the slot. |
| 22 | 4:24-4:29 | Set down again. 4:25-4:26 a hand grips the turret from above, thumb on R5's face, and pushes it home towards the round cut-out while the other hand holds B2. 4:27 the "B2" code is shown. 4:29 the free end of the lead is straightened (`t04m28s.jpg`). |
| 23 | 4:30-4:53 | Nothing moves (`t04m32s.jpg`). Turret on B2 on the worktop: R4 towards the controller end, R3 towards the far end, R5 at the slot-mouth edge, R6 on the other side. B1 still at the top right. |
| 24 | 4:54.5-4:59.5 | **B1 fetched and shown.** B1 is brought under the camera engraved face up; B2 with the turret is tipped back so the horn under it faces the camera, and B1 is held beside it: code "B1" up, horn-shaped cut-out visible, the same way round as B2 (`t04m59s.jpg`). |
| 25 | 4:59.5-5:01 | **B2 (with the turret) closed onto B1**, in the hands (still sequence `seq_04m54s_to_05m01s_B2_onto_B1.jpg`): B2's plain underside onto B1's engraved top face, outlines lined up, and the horn drops into B1's horn-shaped cut-out (`t05m00s.jpg`). Relative motion straight along Y. B1 meets B2 at a slight angle and is then pressed flat. The horn already lay along the length of the plates, so nothing was turned to make it fit. |
| 26 | 5:01-5:11 | **Checked from below.** Tipped until B1's underside faces the camera (5:02, 5:06, 5:08, 5:10): the horn sits in B1's cut-out, hub screw visible, about flush with B1's underside (`t05m08s.jpg`). 5:08-5:11 a second hand squeezes the plates together. |
| 27 | 5:12-5:23 | Turned upright and set down, turret up. Hands off. No screws yet. |
| 28 | 5:24-5:25 | A screw is held up to the camera (`t05m25s.jpg`): silver socket-head cap screw, head about 5.5 across and 3 tall, thread about as long as the head is wide. |
| 29 | 5:26-5:52 | **Screw 1, NAUO47 position** (turret-end corner, R5 side; X 209.2, Z 99.7). Dropped into the hole by hand (5:27), then driven with an L-shaped Allen key while the other person holds the plate (`t05m38s.jpg`). From above, through B2 into B1, until the head sits on B2. |
| 30 | 5:56-6:21 | **Screw 2, NAUO48 position** (middle of the R5-side long edge; X 104.1, Z 99.7). Carried to the hole on the tip of the key. |
| 31 | 6:22-6:24 | Plate turned on the worktop so the controller end is nearest the camera (`t06m24s.jpg`: two screws in, four holes empty). |
| 32 | 6:25-6:39 | **Screw 3, NAUO49 position** (controller-end corner beside the "B2" code; X -20.8, Z 99.7). |
| 33 | 6:42-7:03 | **Screw 4, NAUO50 position** (the other controller-end corner; X -20.8, Z 182.0). 7:03 plate turned. |
| 34 | 7:04-7:22 | **Screw 5, NAUO51 position** (middle of the R6-side long edge; X 104.1, Z 182.0). |
| 35 | 7:23-7:26 | Plate spun half a turn (`t07m25s.jpg`: five in, the turret-end corner on the R6 side still empty). |
| 36 | 7:27-7:38 | **Screw 6, NAUO52 position** (turret-end corner, R6 side; X 209.2, Z 182.0). All six in at 7:39. |
| 37 | 7:40-8:40 | **All six tightened again** with the Allen key, plate turned between them: NAUO47 7:40-7:57, NAUO52 8:00-8:15, NAUO51 8:20-8:23, NAUO48 8:24-8:33, NAUO49 8:35-8:38, NAUO50 8:39-8:40. The heads already sat on B2 after the first round, so this is a final tightening. None is left loose. |
| 38 | 8:41-8:53 | Plate set straight, turret at the top of the frame; hands off (`t08m50s.jpg`). |

Screw positions: the order (going round the outline, which is CAD-id order 47 to 52) is certain. The first, second and sixth
positions were checked on native-resolution crops; the third, fourth and fifth rest on 1 s frames and on counting screws against
empty holes in the hands-off frames. Start and end seconds of each are good to about 2 s.

### What the servo lead does, stage by stage

The lead is the usual three-wire ribbon (brown, red, orange) with a black 3-way socket and a white flag "5". It leaves the servo
case at the shaft end (+Z) and at the face away from R1 (CAD: 163.64, 119.11, 146.77, heading +Z), so it is always in the
compartment between R2 and R6.

| Time | Lead |
|---|---|
| 0:00 | Plugged into the shield. |
| 0:02-0:08 | Unplugged. Never plugged in again in this video. |
| 0:18-0:57 servo into R1 | Trails away across the worktop. |
| 0:58-1:31 R2 | On R2's plain side (+Z), untouched. |
| 1:32-1:47 | Lifted and laid back over R1's +Z edge. |
| 1:48-1:55 R3 | Not touched. |
| 2:12-2:16 R4 | Held up out of the way; afterwards up out of the open top and over R4's top edge near its +Z corner. |
| 2:46-2:58 R5 | Not involved (other side of R2). |
| 3:20-3:24 | Had dropped out through the open +Z side; lifted up and out through the open top and held there. |
| 3:25-3:36 R6 | Held clear above the box. |
| 3:37-4:10 | Out of the top, over R4's top edge 5-10 mm to the R6 side of the L-slot's stem, down R4's outer face. Not in the slot. |
| 4:14-4:17 B2 | Hangs free, then lies across B2. |
| 4:18-4:21 | Picked off B2, laid on the worktop on the R6 side. |
| 4:54-5:18 B1 | Dangles free below the work. |
| 5:19-8:40 screws | Lies on the worktop; swings round each time the plate is turned. |
| 8:43-8:53 | Over R4's top edge hard against R6 (20-25 mm from the slot), down the outside of the R4 / R6 corner under R6's hook, onto the worktop. L-slot empty (`crop_08m50s_turret_and_lead.jpg`). |

## 3. State at the end (8:53)

Still: `stills/base/t08m50s.jpg`.

- B1 (NAUO1) under B2 (NAUO2), outlines lined up, held by six socket-head screws (NAUO47-52) driven from above through B2 into
  B1, all tight, heads standing about 3 mm above B2.
- Turret R1-R6 (NAUO10-15) standing on B2 at the end away from the "B2" code, square to the plate: R4 towards the controller end,
  R3 at the far end, R5 at the slot-mouth edge, R6 on the other side. The base servo (NAUO45) is inside, shaft down through B2's
  keyhole. No screw holds it: its ears rest on R1 and R2's notch sits over it. The horn (NAUO46) is below B2, in B1's cut-out.
  B1 holds the horn still, so when the servo is driven the turret turns on B2, riding on the bottom edges of R5 and R6 (they reach
  6.4 mm below R1, down to B2's top face). The horn is wider than the 19 mm round cut-out, so it also stops the turret lifting off.
- Servo lead loose and unplugged, flag "5", on the worktop on the R6 side. R4's L-shaped slot is empty.
- Not fitted: B3-B8, joysticks, I/O module, R7, R8, any arm or claw part. The shield, Nano and joysticks are where they were at 0:00.

## 4. Proposed guide steps for this section

House style from `docs/cadasio-patterns.md`, with Lee's notes of 13 October (`lee_notes_2026-10-13.md`, items 6, 11-14, 17, 18 and
message 2) applied where they settle something. Numbers start at 1 here and will shift in the full build. "Travel" is the move
from the hover pose to the seat. Free directions were tested with `stepgen.free_directions` on `mra.glb`.

| Step | Draft caption | CAD ids | Motion and cues |
|---|---|---|---|
| card | Before you start, disconnect all servos from the I/O extension module. | - | As now. On video this is one plug, flag "5" (0:02-0:08). |
| 1 / 1c | Begin with R1. Angle the horn of the base servo through the slot in R1, then turn the servo a quarter turn and set it down. | appears: NAUO10. Moves as one part: NAUO45 + NAUO46 (and the lead with its plug riding) | R1 appears in place, engraved face up. Step 1: servo above R1 on the engraved side, a quarter-turn round about its shaft (horn along Z, in line with the cut-out) and tilted, one horn tip down. Auto-advancing middle: tip through, level, with R1 lying between the horn and the servo case. Step 1c: spun a quarter-turn about the shaft axis (vertical through X 163.65, Z 140.85) and lowered until the ears rest on R1 (ears' underside Y 102.96). No straight path exists (`free_directions` returns none for NAUO45 + NAUO46 against NAUO10), so the path is set by hand. Level pose: 7.3 to 9.5 mm above the seat with the horn where `materials.json` puts it (7.3 to 7.7 with the raw CAD). The servo ends with its shaft end, and the lead, at +Z. |
| 2 / 2c | Slide R2 over the base servo and into the slots in R1. | NAUO11 | Hover above, travel -Y (the only free direction). Engraved face to -Z. Two lead lines: R2's two feet to R1's slots at X 129.49-140.49 and X 187.24-198.24, Z 129.55-132.55. |
| 3 / 3c | Add R3. | NAUO12 | Hover above, travel -Y. At the +X end, engraved face outwards. Two lead lines: feet to R1's slots at X 192.67-195.67, Z 114.03-125.03 and Z 156.17-167.17. |
| 4 / 4c | Add R4. | NAUO13 | Hover above, travel -Y. At the -X end (beside the "R1" engraving), engraved face outwards, L-shaped slot at the top. Two lead lines: feet to R1's slots at X 131.94-134.94, same Z. |
| 5 / 5c | Add R5. | NAUO15 | Face-on: hover on the -Z side, travel +Z, engraved face outwards. Four lead lines: R4's and R3's side tabs to R5's upright slots (X 131.94-134.94 and X 192.67-195.67, Y 133.56-144.56) and R1's two edge tabs to R5's flat slots (X 148.39-156.19 and X 180.09-192.79, Y 99.96-102.96). |
| 6 / 6c | Add R6. | NAUO14 | Face-on: hover on the +Z side, travel -Z, engraved face outwards. Four lead lines: the same two upright slots, and R1's edge tabs to R6's flat slots (X 134.83-143.72 and X 176.94-184.75). The lead must already be out of the top (see below). |
| 7 / 7c | Move the servo wire into the L-shaped slot in R4. | lead of NAUO45 | Wire step: eye icon on the slot; Step 7 lead straight up out of the top, Step 7c lead down the slot's stem into the pocket (CAD route passes 133.44, 130.25, 143.46) and straight out past R4. **Not on video.** Lee's item 11 puts it here; his item 18 offers the alternative of leaving the lead straight up until it is plugged in, which is closer to what the builder does. |
| 8 / 8c | Once R1 - R6 are together, slide B2 in between the servo horn and R5 / R6 until the servo sits in the round cut-out in B2. | appears: NAUO2. Moves: NAUO10-15, NAUO45, NAUO46 | B2 appears flat in place. Turret hovers level at its seated height, displaced -Z, and travels +Z along the slot, R5 trailing: the only free direction once the horn is lowered (raw CAD: none). 47.5 mm takes the shaft from the plate edge to the centre of the round cut-out; 51 mm starts with the horn outside the plate edge; 82 mm starts with the whole turret outside it (suggested hover). One lead line along the slot, from the shaft to the centre of the round cut-out (163.6, 140.85). |
| 9 / 9c | Place B2 onto B1 so that the servo horn fits into the horn-shaped cut-out in B1. | appears: NAUO1. Moves: NAUO2 and everything on it | B1 appears below with a clear gap (Lee's item 13); B2 with the turret travels -Y onto it. Two lead lines from the horn's tips to the ends of B1's cut-out (X 144.81-182.45, Z 136.86-144.82), or four at the plate corners. The joint is hidden once closed: a framed close-up of the underside on 9c would match what the builder checks at 5:02-5:10. |
| 10 / 10c | Screw B2 onto B1 with six 6mm screws. | NAUO47 | One screw, close in (Lee's item 12): hover 60 mm above the turret-end corner on the R5 side, travel -Y, one lead line down its axis into the hole at X 209.2, Z 99.7. This is also the first screw on video. |
| 11 / 11c | Add the other five 6mm screws. | NAUO48-52 | Camera pulls back; the five appear above their holes and go down together (Lee's items 12 and 14). Video order: 48, 49, 50, 51, 52. A caption could add "Tighten all six." |

Notes on the list:

- **Step 1 is Lee's item 6 and message 2 as he described them, and it is what the video shows**: slight angle, horn in through the
  cut-out, spin 90 degrees about the vertical, set down. If one pair reads as too busy it splits cleanly in two: "Angle the horn of
  the base servo through the slot in R1." (ends level, horn under R1) and "Turn the servo a quarter turn and push it down into R1."
- **The lead before step 7.** Lee's item 11 has it sticking straight up from the start. On video it is lifted out through the top
  just before R6 (3:20-3:24); if the guide draws it straight up from step 1 that hand action needs no step of its own. If it were
  drawn as it really lies (out through the open +Z side), a numbered step "Lift the servo wire out through the top." would be
  needed between steps 5 and 6.
- The plug is not reconnected in this section. `video_controller_seg2.md` has it going onto the "7 6 5 4" block at Controller.mov
  4:14-4:19.
- "Base servo" follows the captions in `guide.py`; Lee's notes say "Base Motor".

## 5. Uncertain, contradictory, or where the CAD may not match

**Lee's points against the video**

| Lee's statement | Video |
|---|---|
| The base servo arrives with its double-ended horn already fitted | Yes. On at 0:00, never fitted, removed or turned; a screw is in its hub (4:22). |
| The horn is angled through a slot in R1 (message 2: slight angle, rotate in, spin 90 degrees, set down) | Yes, 0:18-0:22, from the engraved side, in exactly those four phases. |
| R2 then slides over the servo, tabs into R1's slots | Yes, 0:58-1:02, straight down. |
| After R6 the lead is moved into the L-shaped slot in R4 | **Not done.** Before R6 the lead is lifted out of the top; after R6 it lies over R4's top edge beside the slot; the slot is empty in the last frame. |
| B2's slot slides in above the horn and below R5 / R6, into the round cut-out | Yes, 4:14.5-4:17.5, both parts in the hands, then pushed home at 4:25. |
| Then the horn fits into the horn-shaped cut-out in B1 | Yes, 4:59.5-5:01, checked from below 5:02-5:10. |
| Then six 6 mm screws | Yes, six, 5:26-7:38, from above, then all tightened again. Length cannot be measured on video; they look like the CAD's M3 x 6. |

**Open points**

1. **The L-shaped slot is never used on video.** The slot is open at R4's top edge, so the lead can be dropped in at any time after
   R4 is on. Its stem is only 2.1 mm wide (Z 140.6-142.7, from Y 146.59 down to Y 135.75), so the ribbon goes in edge-on; the
   pocket is Y 127.25-135.75, Z 140.6-148.72. When to show it (after R6, or when the plug is connected) is Lee's choice between his
   items 11 and 18.
2. **Horn height.** In the raw CAD the horn's arms are at Y 90.16-92.21, inside B2 (Y 90.53-93.53) by 1.68 mm and only 0.37 mm
   into B1's layer. `materials.json` already lowers NAUO46 by 1.8 mm (`adjust_mm`), which puts the arms at Y 88.36-90.41: clear of
   B2 by 0.12 mm and inside B1's thickness. On video the horn looks about flush with B1's underside (5:08), which would be 2.3 to
   2.6 mm lower than the raw CAD, not 1.8. Guess at the cause: the CAD servo is short between its ears and its shaft tip (11.35 mm
   in the CAD; from memory the TowerPro drawing gives about 14 mm, not checked), so on the real kit everything below R1 hangs about
   2 mm lower. Worth one caliper measurement on a real servo: ear face to shaft tip.
3. **Servo end and B2's keyhole.** In the CAD the servo's gear end stops at Y 95.67, 2.1 mm above B2's top face, and only the
   4.9 mm shaft passes through B2. But B2's slot is 12.7 mm wide (the servo is 11.8-12.3) and the round cut-out is 19.0 mm, just
   over the 17.7 mm circle the gear end sweeps when it turns. That sizing, and the view at 4:23, suggest the real gear end reaches
   into B2's thickness. Not confirmed; same measurement as point 2.
4. **Which horn tip goes through R1 first, and which way the quarter-turn goes, cannot be read from the video** (fingers cover the
   cut-out). Either turn direction works; the servo must end with its shaft end at the notch end of the cut-out (+Z). R1's cut-out
   is 12.5 x 22.75 mm (X 157.39-169.89, Z 124.09-146.84) with a 5.7 mm wide notch on to Z 153.19; the horn is 36.35 mm long. The
   pose drawings in `stills/cad_base/servo_into_R1_servo_turned.png` (made by a parallel task; not checked here) follow the same
   sequence as the video.
5. **`guide.py` as it stands differs from the video in two places**: it puts the servo into R2 and then lowers R2 + servo onto R1
   (on video the servo goes into R1 first, R2 comes down over it), and it brings the horn in with B2 (`show=[B2, BASE_HORN]`; on
   video the horn is on the servo from the start, which is why the turret cannot be lowered straight onto B2).
6. **R3 and R4 are the same outline apart from the L-slot** (CAD), and their feet and R1's slots are symmetrical, so a student can
   fit them at the wrong ends. The only cues are the engraved code and the slot. R5 and R6 cannot be swapped: R1's edge tabs are at
   different places on the two sides.
7. **Snap fits.** R2's, R3's and R4's feet have 1 mm barbs that catch under R1, and the side tabs of R3 and R4 have barbs beyond
   R5 and R6. That is why R5 and R6 each take about 10 s of pressing. A straight push in the guide is right in direction but hides
   the effort.
8. **The B2 join is done in the air, tilted, by two people's hands.** The clean equivalent is a level slide along +Z with B2 flat.
9. **Horn direction is not adjustable at the B1 step.** The horn has to lie along the length of the plates to drop into B1. Here
   it did. No centring is shown, and `video_controller_seg1.md` reports the turret being squared up by hand (20-30 degrees) at the
   start of Controller.mov. If a kit's horn sat at another angle the turret would end up skewed.
10. **B1's code is hidden after step 9** (it is on B1's top face, under B2).
11. **Screws**: socket-head cap screws, Allen key, self-threading into B1 (holes 2.8 mm in B2, 2.3 mm in B1). Everything is
    tightened twice; the second round is a caption at most. The plate is turned on the worktop about nine times; none of that
    needs showing.
12. **The shield pin the lead comes out of at 0:02 cannot be read in this video.** The flag says "5".
13. **Two people from about 4:11** is a reading of the hands, not certain.

**How the segment reports' disagreements were settled**

| Point | Segment 1 | Segment 2 | Settled as |
|---|---|---|---|
| Travel of the turret along B2's slot | about 47 mm | about 55 mm | Both are right for different reference points: 47.5 mm shaft to cut-out centre, 53.4 mm for the gear end to start outside the plate edge. Whole turret outside the edge: 82 mm. |
| Width of B2's slot | 12.7 mm | 13.0 mm | 12.7 mm (X 157.29-169.99), measured again. Round cut-out 19.0 mm, centre 163.6, 140.85. |
| How much lower the horn has to be | about 1.7 mm | 2.3-2.6 mm | 1.68 mm is the least that clears B2; 2.3-2.6 mm is what "flush with B1's underside" on video would need. `materials.json` uses 1.8. |
| Where the lead crosses R4's top edge | about 10 mm from the slot (3:42) | 20-25 mm from it, against R6 (8:50) | Both right at their times: the loose lead moved. Native crops of both saved. |
| Who holds what at 4:14 | one builder, left and right hand | a second person holds B2 | Second person, fairly sure (see top of report). |
| 4:25-4:26 | thumb pushes R5's face towards the cut-out | "set down" | A hand grips the turret from above with the thumb on R5 and pushes it home. |
| R4's slot stem | "narrow slit" | about 3 mm wide | 2.1 mm (Z 140.6-142.7), as `cad_wire_paths.md` has it. |
| R5's slots | four small slots for R3 / R4 tabs plus one for R1's tab | - | CAD: four in all, two upright for one tab each of R4 and R3, two flat for R1's two edge tabs. |
| R3's slot over R2 | "how it looks; hidden by fingers" | - | CAD confirms: R3 and R4 each have a bottom-opening slot (Z 129.6-132.6, Y 103.0-127.7) that goes down over the end of R2. |
| R1's cut-out width | 12.3 mm | - | 12.5 mm (12.3 is the servo). |

## 6. Reference stills

All in `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/base/` (1280 px on the long side unless noted).

- `t00m00s.jpg` - start: shield with two joysticks, servo with horn fitted and flagged lead plugged in, B1 / B2 pile.
- `t00m17s.jpg` - R1 (engraved face) in the left hand, servo in the right with the horn across its body.
- `t00m19s.jpg` - first tip of the horn entering R1's cut-out from the engraved side, servo tilted.
- `seq_00m18s_to_00m22s_servo_into_R1.jpg` - 20 frames, four a second: tip in, swing upright, quarter-turn, pressed down.
- `t01m03s.jpg` - R2 seated on R1, seen from R2's engraved side; short end of the servo through R2's notch.
- `t01m13s.jpg` - underside of R1: horn below the plate and across the cut-out; lead with flag 5.
- `t01m52s.jpg` - R3 on edge being lowered at the far end of R1; servo label and lead on R2's plain side.
- `t02m23s.jpg` - R4 fitted, outer face: L-shaped slot in the top edge, lead over the top edge, flag 5.
- `t03m34s.jpg` - R6 being pressed on, code readable.
- `t03m42s.jpg` - after R6: lead over R4's top edge beside the L-slot, not in it.
- `crop_03m42s_R4_L-slot_and_lead.jpg` - the same moment at native resolution: stem and pocket of the slot, lead passing in front.
- `t04m14s.jpg` - B2 held up, keyhole slot and round cut-out clear; turret underside with horn at lower left.
- `t04m15s.jpg` - turret entering the open end of B2's slot; round cut-out still visible beyond it.
- `seq_04m10s_to_04m21s_turret_into_B2.jpg` - 24 frames, two a second: turret shown, B2 held up, slide, set down, lead moved.
- `t04m21s.jpg` - turret upright on B2, "R5" at the slot-mouth edge; lead being laid aside on the R6 side.
- `t04m22s.jpg` - underside of B2: horn below the plate, across the slot, screw in its hub; "R5" readable above.
- `t04m23s.jpg` - underside of B2, clearer: horn across the round cut-out, servo end in the slot.
- `t04m28s.jpg` - set down on the worktop after the slide; B1 apart at the top right.
- `t04m32s.jpg` - the hold at 4:30-4:53: turret on B2, lead out over R4 to the right, no B1, no screws.
- `seq_04m54s_to_05m01s_B2_onto_B1.jpg` - 16 frames, two a second: B1 fetched, horn shown, plates closed together.
- `t04m59s.jpg` - just before joining: horn under B2 in one hand, B1 code-up with its cut-out in the other.
- `t05m00s.jpg` - the two plates closed together in the hands, "R5" readable.
- `t05m08s.jpg` - underside of B1: horn sitting in the horn-shaped cut-out, about flush.
- `t05m25s.jpg` - the screw held up to the camera: short socket-head cap screw.
- `t05m38s.jpg` - first screw (NAUO47 position) being driven with the Allen key; two people's hands; "R1" on the floor.
- `t06m24s.jpg` - two screws in (NAUO47, NAUO48), "B2" readable, Allen key in the hand at the right.
- `t07m25s.jpg` - five screws in, the turret-end corner on the R6 side still an empty hole; lead and flag "5".
- `t08m50s.jpg` - final state: six screws, lead over the R4 / R6 corner, L-slot in R4 empty.
- `crop_08m50s_turret_and_lead.jpg` - the turret in the final frame at native resolution: servo, lead, empty L-slot, two screw heads.

CAD drawings made for this report, in `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/`:

- `video_base_cad_R1_top.png` - R1 from above with the servo's ears and body and the horn as built: cut-out, notch, slots.
- `video_base_cad_B2_keyhole.png` - turret end of B2 and B1 from above: slot, round cut-out, B1's horn-shaped cut-out, horn, servo end.
- `video_base_cad_section_X163.png` - section through the shaft (raw CAD): R1, servo, horn inside B2's layer, B1, R5, R6.
