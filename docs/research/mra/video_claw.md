# Claw.mov (7:06): merged report - the claw, the claw on the arm, the claw motor's wiring

STATUS: COMPLETE (merge of the three segment reports, plus the merge's own look at the video and one CAD test of the video's order).

Source: `/Users/lee-johnson/Desktop/Claude_Cadasio/MRA_Videos/Claw.mov` (7:06 = 425.6 s, portrait phone video 1080 x 1920, hand held, looking
down at a worktop). Segment reports merged here: `video_claw_seg1.md` (0:00-2:35), `video_claw_seg2.md` (2:20-4:55), `video_claw_seg3.md`
(4:40-7:06). Every action in the two overlaps (2:20-2:35 and 4:40-4:55) is listed once. All times are the video's own.

**Names.** Codes are the ones ENGRAVED on the wood. Five claw parts and all four arm parts used here are engraved differently from their
CAD file name, so every part is given with its CAD id:

| Engraved | CAD id | CAD file name | What it is | Read on video at |
|---|---|---|---|---|
| C1 | NAUO32 | ARA_C1 | clip plate, two small holes (body and leg), +Z side | 0:27, 2:48, 4:03, 4:54 |
| C2 | NAUO33 | ARA_C2 | clip plate, one small hole (leg), -Z side | 0:33, 0:35-0:38, 5:34 |
| C3 | NAUO34 | ARA_C3 | servo plate with the tongue and the cable hole | 0:00, 0:17, 1:17 |
| **C4** | NAUO36 | ARA_C5 | spacer bar on the C2 side (-Z), narrow tabs (7.6 mm) | 0:00, 0:52-0:54 |
| **C5** | NAUO37 | ARA_C6 | spacer bar on the C1 side (+Z), wide tabs (10 mm) | 1:06-1:07 |
| **C6** | NAUO35 | ARA_C4 | keyhole plate | 0:00, 1:19, 2:18 |
| **C7** | NAUO39 | ARA_C8 | jaw with the horn-shaped slot: the DRIVEN jaw | 0:00, 2:24 |
| **C8** | NAUO38 | ARA_C7 | jaw with the small pivot hole: the GEARED jaw | 2:26, 2:48 |
| C9 | NAUO40 | ARA_C9 | cover plate with the 11.7 mm hole | 0:00, 2:41 |
| **A5** | NAUO22 | ARA_A4 | long forearm strip, -Z side, three holes | 5:34 (fairly sure) |
| **A6** | NAUO29 | ARA_A11 | cross plate of the upper arm, two 8 x 8 mm square holes | 3:38 and many later frames |
| **A12** | NAUO27 | ARA_A9 | upper (levelling) strip, +Z side, triangle mark | 3:48, 4:54 |
| **A13** | NAUO28 | ARA_A10 | lower (forearm) strip, +Z side, square mark | 3:48, 4:54 |
| R4 | NAUO13 | ARA_R4v2 | turret wall facing the controller, with the L-shaped slot | 3:40, 6:43-7:05 |

Other ids: claw motor NAUO72 (CAD mesh `MG90S_Cut wires shorter`), its single-arm horn NAUO73, its lead NAUO94 with plug NAUO90;
coupler NAUO91 (`JR-3 Bridge`); extension lead NAUO93 with plugs NAUO92 (coupler end) and NAUO85 (shield end); screws NAUO74, NAUO75
(M3x16), NAUO76 (M3x10), NAUO77, NAUO78, NAUO79 (M3x6); I/O module NAUO82. This table agrees with `cad_arm_claw.md` section 9 and
`cad_codes_base.md`.

**Axes and words.** mm, assembly space, Y up. "+Z side" is the student's right when sitting at the joysticks, "-Z side" the student's
left. For the claw on the worktop: "near" = the C2 side (-Z), "far" = the C1 side (+Z), "back" = the tongue end of C3 (-X), "front" = the
jaw tips (+X). The claw's plates are tilted 0.6 degrees in the CAD: their normal is n = [0.011, 1, 0].

## 0. The ten things that matter most

1. **The claw is built upside down**, engraved faces up, on the worktop and in the hand, and only turned the right way up at 3:42 to go
   on the arm. In the CAD pose C3 is the top plate (y 193-196) and C9 the bottom (y 174-177): nine of the thirteen claw steps go on from
   underneath there. The engraved faces of C3, C6, C7, C8 and C9 all look down (-Y) in the CAD pose, so a view from above shows blank wood.
2. **Order on video:** claw motor through C3 (lead first), lead out through C3's tongue hole, clip C1, clip C2, bar C4, bar C5, keyhole
   plate C6, two 16 mm screws, jaw C7 on the horn, cover C9, jaw C8 slid in under the cover, one 10 mm pivot screw, jaws tried by hand.
   This is NOT the CAD-derived order of `cad_arm_claw.md` 7.5 (clips last, both jaws before C9). The merge tested the video's order against
   the CAD with the generator's own collision test: every step is free (section 4.3).
3. **The claw motor is not screwed down.** Its two mounting tabs are trapped between C3 and a step in the edge of each spacer bar; the two
   16 mm screws clamp C6 to C3 through the bars' height.
4. **The horn is already on the motor at 0:00**, with its small cross-head screw in the hub, pointing straight to the front of the claw
   (along +X; CAD horn direction [1, 0, -0.03]). It is never taken off, turned or centred on camera. Nothing fastens the horn to the wood:
   jaw C7 is pressed over it and C6 above and C9 below keep it there.
5. **Jaws:** C7 (NAUO39) is driven by the horn about the motor shaft ([335.13, y, 138.76]); C8 (NAUO38) turns on the 10 mm screw NAUO76
   ([335.45, y, 156.07]); their gear teeth mesh half-way between (axes 17.3 mm apart), so they open and close equal and opposite.
6. **Screws.** Clamps: NAUO74, NAUO75 (16 mm, C6 to C3). Pivots: NAUO76 (10 mm, jaw C8), NAUO77 (6 mm, A12 into the body of C1), NAUO78
   (6 mm, A13 into the leg of C1), NAUO79 (6 mm, A5 into the leg of C2). Every one is driven until its head is down; the pivoting parts
   still swing afterwards. Lengths are judged by eye and agree with the CAD.
7. **Claw to arm:** the claw, right way up, goes against the INNER faces of A12 and A13 on the +Z side first (A12 screw, swing the claw
   on it, A13 screw), then the robot is turned round and A5 is screwed to C2 on the -Z side. All three strips lie outside the clips; the
   engraved faces of C1 and C2 look outwards; all three screw heads are outside.
8. **Lead route:** out of the motor at its -Z end, back over the top of C3, down through the hole in C3's tongue (done during claw
   assembly), back under the claw along the forearm, through the elbow-end square hole of A6 from the back face to the engraved face, down
   the engraved face, through the shoulder-end square hole to the back, down into the turret. Only then is its plug pushed into the
   coupler, which arrives already fitted on one end of the twisted extension lead (blue flag "10").
9. **Shield rows at the end:** four servo plugs on the digital side. Two side by side in the block printed 4 5 6 7 with row 4 left bare
   (rows 5 and 6); two side by side in the block printed 8 9 10 11 (rows 9 and 10); the extension goes in next to the plug that was already
   in that block. Flags read: white hand-written "5", black printed underlined "6", blue printed "10". The row 9 lead's flag is not
   established. Rows agree with the CAD (base 5, NAUO58 6, NAUO66 9, claw 10) and with Lee's note (base on 5).
10. **Nothing happens at the very end:** after the extension is plugged in, the join is pushed down inside the turret behind R4 with the
    extension's wires dropped into R4's slot, and the robot is lifted and shown. No USB, no power, no test, no servo centring.

## 1. What is already built or laid out when the video starts (0:00)

Stills: `stills/claw/t00m00s.jpg`, `stills/claw/merge_t00m00s_flag5_x5.jpg`, `stills/claw/t03m40s.jpg` (the robot, first seen whole at 3:38).

**The robot (base, controller, turret, arm), finished in the earlier videos.** Only its controller end is in frame until 3:37.

- Joystick box with its lid B8 (engraved Shoulder and Base by the left joystick, Elbow and Claw by the right, each with arrows), B5 on
  the wall facing the camera, both joystick caps. Behind it the Nano on the blue I/O module with the rainbow jumper ribbon.
- **Three servo leads are already plugged into the I/O module** (seen at 0:00; rows read at 5:42 and 6:43: two in the block printed
  4 5 6 7, one in the block printed 8 9 10 11). One carries a white paper flag with a hand-written **5** (clear at 0:00 at native size:
  merge's own look), one a black flag with a white printed, underlined **6** (3:38-3:43 and later). Arm.mov ended with both side-motor
  leads loose and unplugged, so **the two side motors were plugged in off camera, between Arm.mov and Claw.mov**.
- Seen from 3:38: turret with cross wall R4, a side motor on each side under its clamp plate, both leads running down to the shield (the
  -Z motor's lead loops out to the student's left and round to the shield; the +Z motor's lead runs forward past the front lug of the +Z
  side plate and in from the student's right). Upper arm standing at about 60 degrees: two side strips joined by the cross plate A6 with
  its two square holes (both empty) and two cross-slots, each with a T-piece and a long screw. The three-layer lever on the -Z side. At
  the elbow on the +Z side the triangle plate A10 with A12 and A13 screwed to it at their elbow ends, hanging down along the upper arm,
  claw ends free. On the -Z side the long strip A5 with its claw-end hole empty.
- The mini-USB socket of the Nano is empty. A white USB power block with a black cable lies at the top right of the worktop for the whole
  video and is never touched.

**Loose on the worktop at 0:00**, every wooden part lying engraved face up except one spacer bar:

- The claw motor NAUO72 (MG90S, blue and red label) **with the black single-arm horn NAUO73 already pressed on its shaft and a silver
  cross-head screw already in the hub** (six small holes along the arm). Its lead (brown / red / orange flat ribbon, black 3-pin socket)
  trails off to the left; nothing is joined to it.
- C6 (keyhole plate), C9 (half out of frame), the two jaws stacked (C7 on top, C8 underneath), C1, C3, C2, bar C4 (code up) and bar C5
  (code down, read later at 1:06).
- With their engraved faces up, C1 and C2 are mirror images. C1 has a hole in its leg and a second in its body; C2 only the one in its leg.
- No screws in view (they are fetched one at a time from off-frame). A dark grey T-handle hex driver (handle marked "3.0") at the right edge.
- The twisted extension lead is not in the working area. A lead with a black connector lies at the top left corner of the worktop from
  3:40 to 5:34 (`t03m40s.jpg`, `t05m34s.jpg`); that is probably it (guess).

## 2. Timeline: every assembly action, in order

Directions are given as seen (claw upside down until action 21) and, in brackets, in assembly space for the CAD pose. "Certain",
"fairly sure" and "guess" are the segment reports' own grades unless "merge" is written.

### A. Claw sub-assembly, built upside down (0:00-3:36)

1. **0:01-0:10 - claw motor's lead threaded through C3.** Right hand lifts the motor, left hand lifts C3 (NAUO34), engraved face
   towards the camera. The plug on the end of the lead is fed through C3's rectangular servo cut-out **from the engraved face** (first
   try 0:04-0:07, C3 slips 0:08-0:09, plug through at 0:10). Certain.
2. **0:11-0:16 - claw motor pushed through C3.** C3 held on edge; the motor follows its lead through the cut-out, **case bottom first,
   from the engraved face**, until both mounting tabs stop flat on the engraved face (0:15). Seated, the gear housing, shaft and horn
   stand proud of the engraved face and the case hangs out of the other face. The shaft is at the **near (-Z) end** of the cut-out, the
   end with the single big square slot beside it. The horn points **straight to the front**, away from the tongue. The horn is not
   touched. No screws go through the motor's tabs, here or later. (Assembly space: motor moves +Y up through C3, tabs end under C3;
   cut-out centre [335.27, 194.72, 143.81]; shaft tip [335.11, 179.37, 138.76] pointing -Y.) Stills `t00m12s.jpg`, `t00m17s.jpg`. Certain.
3. **0:16-0:24 - lead taken out through the tongue hole.** The lead is now on the case side of C3. It is pulled straight (0:17-0:18),
   the plug is pushed through the small rectangular hole in C3's tongue **from the case side out to the engraved side** (0:19-0:20) and
   the whole lead is pulled through after it (0:21-0:24). Result: the lead leaves the motor on the case side, runs along C3's plain face
   to the tongue and comes out of the tongue hole on the engraved side. (Assembly space: over the top of C3, down through the
   6.3 x 10 mm hole centred [300.78, 195.09, 147.06], out underneath: as the CAD lead NAUO94 is modelled.) Still `t00m24s.jpg`. Certain.
4. **0:26-0:31 - clip C1 (NAUO32).** Right hand picks it up (code read 0:27), carries it round behind C3 and pushes its two sprung
   prongs through the **outer of the two parallel slots on the far side** of C3, **from the case side towards the engraved side**, in one
   push. The prongs now stand out of the engraved face; the leg with the hole stands beside the tongue on the far side. Engraved face
   outwards (+Z): in shadow here, confirmed at 4:54 where "C1" is readable on the outside. (Assembly space: prongs go down, -Y, through
   C3 at [317.12, 194.92, 164.7]; body on top of C3.) Still `t00m27s.jpg`. Certain (with 4:54).
5. **0:32-0:38 - clip C2 (NAUO33).** Left hand picks it up (code read 0:33); prongs pushed through the **outer half of the single
   square slot on the near side** of C3, again from the case side. Engraved face outwards (-Z): code readable on the outer face at
   0:35-0:38 and at 5:34. Leg beside the tongue on the near side. Both clips also have a small tooth at the front that sits in the two
   open notches in C3's front edge (0:42, 1:17). (Assembly space: -Y through C3 at [317.12, 194.92, 128.05].) Still `t00m38s.jpg`. Certain.
6. **0:39-0:48 - put down.** Lead lifted clear and laid to the upper left; sub-assembly set on the worktop **engraved C3 face up**,
   resting on the motor case and the clip bodies, tongue to the left (0:41). The far clip's prongs are pinched once (0:42-0:43). Camera
   moves in close at 0:47 and stays close.
7. **0:50-1:02 - spacer bar C4 (NAUO36).** Right hand (code read 0:52-0:54) stands it on edge and pushes its tab straight down into the
   **inner half of the near-side square slot** of C3, directly inboard of C2's prongs (0:55-0:58), then presses it home (0:59-1:02).
   **Engraved face outwards** (towards C2; code made out at 0:57 and 1:04). The bar runs front to back along the near edge and its
   stepped edge passes over the motor's tab at the shaft end, trapping that tab between C3 and the bar. (Assembly space: tab into C3 at
   [315, 194.9, 131.05], bar moves +Y; shoulder 0.10 mm under the tab.) Still `t00m57s.jpg`. Certain.
8. **1:03-1:16 - spacer bar C5 (NAUO37).** Picked up from the right (code read 1:06-1:07), stood on edge and pushed down into the
   **inner of the two far-side slots** of C3, inboard of C1's prongs (1:08-1:11). Its inner face is blank, so **engraved face outwards**
   (towards C1). It passes over the motor's other tab. (Assembly space: [318.29, 194.9, 157.22], +Y.) Then the whole thing is lifted a
   little and each bar squeezed down hard between finger and thumb (1:12-1:16). Still `t01m17s.jpg`. Certain.
9. **1:17-1:40 - keyhole plate C6 (NAUO35).** Brought over **engraved face up** (code read 1:19-1:20). Its big cut-out is a round hole
   open to the front edge. The plate comes in tilted, back edge high, and is lowered so the horn hub stands in the round part and the
   horn arm lies across the open gap (1:20-1:21): it goes on **with the horn already on the motor**, and the horn ends up above the plate
   (assembly space: below it, in the jaw layer). The tabs of the two bars enter its slots and the prongs of C1 and C2 come up through it
   (C1: outer far slot; bar C5: inner far slot; C2 and bar C4 share the near square slot). Pressed and squeezed down for about twenty
   seconds, corner by corner (1:22-1:40): a tight fit. Three small holes in it: one beside the code (back screw), one in the lug at the
   front edge beside the keyhole opening (front screw), and the smallest, on the far side of the shaft (jaw pivot, 2.3 mm, at
   [335.39, y, 156.09]). (Assembly space: plate moves +Y onto the bars' lower tabs at [315, 181.4, 131.05] and [318.15, 181.4, 157.22].)
   Still `t01m20s.jpg`. Certain.
10. **1:41-1:55 - first 16 mm screw (NAUO74).** A long silver socket-cap screw (shank about three head-widths long in a blurred frame
    at 1:41.5; a 10 mm screw could not span the 3 + 10.5 + 3 mm stack) is dropped into the **back hole of C6, beside the code**
    (1:42-1:44) and driven **from the engraved side** with the T-handle hex driver until the head is down on C6 (1:46-1:54). Tightened
    fully: a clamp. (Assembly space: head end y 176.84, at [322.93, 176.84, 147.11], pointing +Y; free through C6, threads into C3.) Certain.
11. **1:56-2:16 - second 16 mm screw (NAUO75).** Same kind of screw, stood in the **hole in the lug at the front edge of C6**, close
    to the tip of the horn (1:58-2:03; fiddly, the fingers work round the horn), driven home (2:05-2:13), driver put down (2:14-2:16).
    Tightened fully. (Assembly space: [347.24, 176.58, 147.03], +Y.) Stills `t02m17s.jpg`, `t02m18s.jpg`: both cap heads on C6, pivot hole
    empty, horn lying above the plate, hub off-centre towards the near side (shaft z 138.76 against the plate's centre line z 147). Certain.
12. **2:17-2:23 - jaw C7 (NAUO39) onto the horn.** Right hand brings the jaw, **engraved face up**, tilted with the gear end low; the
    round end of its horn-shaped through-slot goes over the horn hub (2:19-2:20), then the jaw is levelled and pressed flat with the left
    forefinger (2:21-2:22). Seated at 2:23: the horn arm lies in the slot, flush, all six horn holes showing. The horn is not unscrewed or
    turned; the jaw takes the horn's angle and points straight forward, its hooked tip curling towards the far side. Nothing screws the
    horn to the wood. (Assembly space: jaw moves +Y; engraving faces -Y; horn at [342.02, 178.14, 137.91]; the CAD has up to 0.35 mm of
    overlap between horn and slot, i.e. a push fit.) Stills `t02m23s.jpg`, `t02m24s.jpg`. Certain.
13. **2:24-2:28 - jaw C8 (NAUO38) tried in place, then taken off again.** Right hand lays it on C6, engraved face up, its 2.8 mm hole
    over C6's pivot hole, gear teeth meshed with C7's, both jaws closed so the two half-round bites make one round hole (2:26). One
    second later it is lifted off and laid at the top of the frame (2:27-2:28). No screw. Certain about what happens; why is a guess
    (nothing would hold this jaw while C9 is squeezed on). Still `t02m26s.jpg`: the clearest view of how the two gears mesh.
14. **2:29-2:41 - cover C9 (NAUO40) pressed onto the clip prongs, with only jaw C7 underneath.** Brought **engraved face up**
    (2:30-2:31) and lowered flat: its two short slots over the two pairs of prongs (C1 far, C2 near), its 11.7 mm hole over the horn hub
    (the horn screw shows through it), its small hole over the pivot hole, its code at the back edge reading the same way as C6's. Both
    hands squeeze it down at the back corners from 2:33 to 2:40. At 2:41 the prong tips with their hooks stand 2 to 3 mm through the slots
    (CAD 3.3 mm) and the cover sits level on jaw C7 and the two cap heads; the front cap head stays visible beyond its front edge. The
    snap of the barbs cannot be seen; the prongs standing through is the evidence. (Assembly space: C9 moves +Y to y 173.6-176.6;
    slots at [316.8, 175.41, 164.7] and [316.8, 175.41, 128.05]; engraving faces -Y.) Stills `t02m33s.jpg`, `t02m41s.jpg`. Certain.
15. **2:42-2:53 - jaw C8 (NAUO38) slid in under the cover.** Right hand picks it up again (2:42-2:45); left hand lifts the claw, still
    jaw side up (2:46). The jaw is held flat, engraved face up, and its GEAR END is pushed into the 3 mm gap between C9 and C6 at the far
    front corner (2:46-2:48: gear half under the cover), then slid further in (2:49-2:51) until its teeth mesh with C7's and its hole
    shows through the small hole of C9 (2:52-2:54). Both jaws end closed, tips together. (Assembly space: the jaw moves in its own plane,
    y 176.6-179.6, from the +Z front corner, mostly -Z with some -X.) Still `t02m48s.jpg`. Certain.
16. **2:54-3:03 - pause.** Claw held still in the left hand and shown; tilted once at 3:02. No change.
17. **3:04-3:28 - jaw pivot screw (NAUO76).** One silver socket-cap screw fetched from off-frame (3:04-3:05) and dropped thread first
    into the small hole of C9 (3:06). At 3:07-3:11 it stands upright with about 4 mm of shank showing under the head: what an M3x10 does
    here (3 mm of C9 and 3 mm of jaw are clearance, then the thread meets the 2.3 mm hole in C6). Driver in at 3:13, turned 3:14-3:27 with
    the claw held flat on the worktop, lifted away 3:28; head down on C9. (Assembly space: [335.39, 170.7, 156.09], pointing +Y; free
    through C9 and jaw C8, threads into C6.) Still `t03m07s.jpg`. Length fairly sure; how tight it was left cannot be seen.
18. **3:29-3:32 - jaws tried by hand.** Right finger and thumb pull the tip of C8 outwards to the far side while the left hand pulls the
    tip of C7 to the near side: both jaws swing open together, roughly 30 to 40 degrees each, turning the unpowered motor through the jaw
    and horn. Pushed closed again at 3:32. The only motion test in the whole video. Still `t03m30s.jpg`. Certain.
19. **3:33-3:36 - claw and driver put down.** Finished claw lies jaw side up (C9, C8, C7 readable, lead trailing); pushed aside at 3:36.

### B. Claw onto the arm (3:37-5:35)

20. **3:37-3:41 - robot pulled into frame** by the joystick box (state in section 1). The claw is picked up (3:40), its lead held near
    the plug for a moment and let go (3:41). Still `t03m40s.jpg`.
21. **3:42-3:53 - claw turned the right way up and offered to A12 and A13.** The claw is now motor case and clip bodies up, jaws and C9
    underneath, jaw tips pointing away from the arm, tongue of C3 towards the arm, lead hanging from the back. The left hand swings the
    two +Z strips up and outwards (3:44) and pinches their free ends together (3:45 on). The right hand brings the claw to the strips'
    free ends from beyond them so that the OUTER, engraved face of clip C1 lies against the INNER face of both strips (3:45-3:46) and
    shuffles it until the hole in the BODY of C1 is behind the end hole of A12 (3:47-3:53). Only the hands hold it. The -Z strip is not
    involved. (Assembly space: C1's outer face z 166.2 against the strips' inner face; the claw comes back along the forearm, about
    [-0.91, 0.41, 0], and up against the strips in +Z.) Still `t03m46s.jpg`. Certain.
22. **3:54-4:16 - first claw-to-arm screw (NAUO77): A12 into the body of C1.** A short silver socket-cap screw fetched (3:54-3:59),
    started by hand from the OUTSIDE (+Z) through the end hole of the UPPER strip A12 (NAUO27) into clip C1 (4:00-4:03), then driven with
    the T-handle driver from the same side (4:05-4:15). Left hand holds strips and claw together throughout. Shank about as long as the
    head is wide: 6 mm. (Assembly space: [311.98, 205.67, 172.23], pointing -Z; 2.8 mm clearance hole in A12, 2.3 mm thread in C1.)
    Still `t04m00s.jpg`. Certain.
23. **4:17-4:27 - pause, then the claw is swung on that screw.** Nothing moves 4:17-4:23. At 4:24-4:27 the right hand takes the claw
    by the jaw end and turns it about the first screw until the hole in the LEG of C1 is behind the end hole of the lower strip. So the
    first screw is left free enough to turn on.
24. **4:28-4:52 - second claw-to-arm screw (NAUO78): A13 into the leg of C1.** Another short cap screw fetched (4:28-4:30), started by
    hand from the same side through the end hole of the LOWER strip A13 (NAUO28) into the leg of C1 (4:31-4:35; both heads visible one
    above the other at 4:32 and 4:35), driven 4:37-4:51 with the driver level, coming in from the builder's right. (Assembly space:
    [301.81, 188.27, 172.23], pointing -Z: the wrist axis.) Still `t04m30s.jpg`. Certain (segment 2 saw which hole; segment 3 confirms
    the side and the end).
25. **4:52-4:56 - that side shown to the camera.** Readable at 4:54: A12 (upper strip), A13 (lower strip), A10 (triangle), A8, R6, and
    C1 on the clip, engraved face outwards. A silver socket head at each end of A12 and A13. Both strips lie on the OUTSIDE of C1. The
    lead leaves the top of the motor at its -Z end, crosses C3 to the back, goes DOWN through the tongue hole and hangs loose below the
    claw, its plug on the worktop. Still `t04m54s.jpg`.
26. **4:57-5:09 - robot turned end for end; A5 brought to the claw.** Half a turn flat on the worktop (4:57-4:58): controller now at the
    top of the frame, the builder's right is now the -Z side. Right hand takes the free end of the long strip A5 (NAUO22) and swings it
    down to the claw (4:59-5:06, partly below the frame edge); the strip goes on the OUTSIDE of clip C2, its end hole over the hole in
    C2's leg (confirmed by the result at 5:10 and 5:34). Robot dragged towards the camera (5:07-5:09).
27. **5:10-5:29 - third claw-to-arm screw (NAUO79): A5 into the leg of C2.** A short silver socket-cap screw is started by hand from the
    -Z side through the end hole of A5 into C2 (5:10-5:14), then driven with the T-handle driver from that side, about 14 s of turning,
    head down on A5 (5:15-5:29). No backing-off seen. (Assembly space: [301.86, 188.36, 120.52], pointing +Z: the same wrist axis as
    NAUO78.) Still `t05m10s.jpg`. Certain.
28. **5:30-5:35 - driver put down; claw seen from above, then the -Z side shown.** From above (5:31-5:33): motor case in C3's cut-out,
    the silver tip of one 16 mm screw showing in C3 between the motor and the tongue, the lead leaving the motor at its -Z end, curving
    back and going down through the tongue hole; behind it A6 with both square holes still empty. At 5:34: "C2" on the clip, engraved face
    outwards; "A5" on the long strip (fairly sure); silver head at the claw end of A5 on C2's leg. The claw now hangs on three screws and
    still tilts freely when the arm is moved. Stills `t05m33s.jpg`, `t05m34s.jpg`.

### C. Claw motor's lead, coupler, extension, shield (5:36-7:05)

29. **5:36-5:42 - robot turned back; arm stood upright by hand.** Controller at the bottom of the frame again. Upper arm vertical, A6's
    engraved face towards the controller and the camera, forearm folded so the claw sits above and beyond the top of A6. The arm stays
    like this until 6:58. The claw lead hangs down the +Z side, plug free. Shield: three plugs in, flag "6" standing up
    (`merge_t05m42s_arm_upright_three_plugs.jpg`).
30. **5:43-5:48 - extension lead fetched and shown.** The builder reaches off the top of the frame (5:43) and comes back with it
    (5:44): three wires TWISTED together, yellow / red / brown (not the flat orange / red / brown ribbon of the motor leads), roughly
    150 mm long (CAD NAUO93: 149 mm), a black connector on each end, and a BLUE flag with a white printed "10" wrapped round it about
    20 mm from one end. Held up, then laid down at the right.
31. **5:49-6:04 - claw lead through the elbow-end hole of A6.** Right hand takes the lead's plug, carries it round the +Z side to the
    BACK of the upright arm (the face of A6 away from the controller) and pushes the plug, narrow end first, through the UPPER square
    hole of A6 (elbow end; 8 x 8 mm, centre [222.76, 214.43, 144.49]) **from the back face to the engraved face** (5:49-5:59; 5:57 shows
    the plug filling the hole). Left hand receives it; the plug and about 60 mm of lead are drawn out on the engraved side and down the
    face of A6 (6:00-6:04). Still `t05m57s.jpg`. Certain.
32. **6:05-6:13 - claw lead through the shoulder-end hole of A6; slack pulled flat.** The plug is pushed through the LOWER square hole
    (shoulder end; 8 x 8 mm, centre [186.70, 174.50, 144.49]) **from the engraved face to the back** and caught below (6:05-6:10). At
    6:09 the lead lies on the engraved face from the upper hole to the lower, flat side against the wood, down the middle of the plate
    between the two T-pieces. Right hand goes to the claw end while the left holds the plug below, and the loop standing off A6 is pulled
    flat (6:10-6:13); which way the slack goes cannot be told. Still `t06m09s.jpg`. Certain.
33. **6:13-6:21 - plug drawn down into the turret.** The lead comes out of the lower hole on the back of A6, under A6's bottom edge, and
    the plug is fished down and forwards inside the turret, between the two side plates, with the fingers of both hands. At 6:20-6:21 it
    is held up over the turret end-on: an ordinary small 3-way servo socket (three square holes). Still `t06m21s.jpg`.
34. **6:21-6:39 - claw lead's plug pushed into the coupler on the extension lead.** The extension is picked up (6:21). Its end WITHOUT
    the flag already carries the coupler: a hollow black sleeve, clearly wider and thicker than a servo plug and open at the end (6:22.5 to
    6:26.5; broad face at 6:23, `merge_t06m23s_coupler_and_plug.jpg`). Nobody fits the sleeve to the extension in this video. The join is
    made in the air just above the turret: right hand holds the claw lead's plug between the side plates, left hand brings the sleeve to
    it; first offer about 6:26, apart again 6:27-6:29 (plug turned over or re-aimed), together from 6:30, squeezed home until 6:39. Signal
    wire meets signal wire: at 6:43 brown is on the same edge of the join on both leads, and orange (motor) meets yellow (extension) on
    the other edge. Still `t06m24s.jpg`. Certain about the join; "re-aimed" is a guess.
35. **6:40-6:43 - join let go.** It hangs over the top edge of R4: the motor's plug uppermost with its ribbon coming straight down from
    A6, the coupler in the middle, the extension's plug lowest and outside R4, its twisted wires falling in front of R4 towards the shield.
    At 6:42-6:43 the flag "10" is turned to the camera (`t06m42s.jpg`, `merge_t06m43s_join_over_R4_flag10.jpg`). The left hand rests on
    the right joystick for a moment at 6:40 (nothing is powered; not a test).
36. **6:44-6:50 - extension plugged into the shield.** Right hand takes the free end (flag "10" just behind the plug), loops the twisted
    lead round to the +Z side of the shield and pushes the plug straight DOWN onto the pins of the digital header (the edge nearest the
    joysticks), in the block printed 8 9 10 11, next to the plug already there. Left forefinger steadies the board. The hand hides the
    pins at the moment of plugging; row 10 is by the evidence in section 3. Still `t06m49s.jpg`.
37. **6:51-6:57 - join tucked into the turret; extension's wires into R4's slot.** Right hand reaches over from the +Z side and pushes
    the join down inside the turret, left hand at R4 (hidden by the hands 6:53-6:55). At 6:56 the join stands upright INSIDE the turret
    close behind R4, between R4 and the base motor, and the extension's three wires go DOWN INTO THE SLOT in R4's top edge and come out
    on the controller side below it (clear at 6:58, 6:59, 7:04). At 6:56-6:57 the right fingertips pinch the +Z motor's lead where it
    passes the front lug of the +Z side plate (guess: pressing that lead back into its slot).
38. **6:58-7:05 - finished robot shown.** Left hand lifts the controller end, right hand holds the +Z side of the turret, the robot is
    tilted towards the camera (7:00-7:03); the arm swings freely on its pivots and the claw is seen from above. Put down 7:04, hands
    away 7:05. Video ends at 7:05.6. Stills `t06m58s.jpg`, `t07m01s.jpg`, `merge_t07m05s_end.jpg`.

No horn is fitted, removed or turned anywhere in the video; no motor is centred or powered; no USB or power cable is connected.

## 3. State at the end (7:05)

- **Claw, complete:** C3 with the claw motor through it; clips C1 (+Z) and C2 (-Z), engraved faces outwards; bars C4 (-Z) and C5 (+Z)
  trapping the motor's tabs; C6 held by two 16 mm screws into C3; horn with its screw; jaw C7 on the horn; cover C9 snapped over the
  prong tips of C1 and C2; jaw C8 between C6 and C9 on its 10 mm pivot screw. Jaws closed. Right way up: motor case and clip bodies on
  top, C9 underneath, jaws pointing away from the arm.
- **Claw on the arm by three screws, all pivots, all heads outside:** A12 into the body of C1 and A13 into the leg of C1 from the +Z
  side (NAUO77, NAUO78), A5 into the leg of C2 from the -Z side (NAUO79). All three strips lie outside the clips. The claw tilts freely.
- **Claw motor's lead, in order:** leaves the motor at its -Z end; bends back over the top of C3; down through the hole in C3's tongue;
  back under the claw and along the forearm between the strips, loose, no clip or tie; through the elbow-end square hole of A6 from the
  back; down A6's engraved face, flat against it, visible from the controller side; through the shoulder-end square hole to the back;
  under A6's bottom edge; down and forwards inside the turret; its plug, pointing down, in the top of the coupler.
- **Coupler and extension:** plug, sleeve, plug make about 30 mm of black in a straight line, standing roughly upright just inside R4,
  lower end about level with R4's top edge. The extension's wires drop into the slot in R4's top edge (CAD: mouth 2.12 mm wide,
  z 140.60-142.72, on the top edge y = 146.59, leading to a pocket z 140.60-148.72, y 127.25-135.75, in the plate x 131.94-134.94),
  come out on the controller side, run in a loose loop round the +Z side of the shield and down into the plug. This is the same slot the
  base motor's lead uses.
- **Shield, digital side: four servo plugs.** Block 4 5 6 7: row 4 bare, two plugs side by side (rows 5 and 6). Block 8 9 10 11: two
  plugs side by side. At 6:43, before the extension went in, bare pins showed at the "10 11" end of that block and one plug sat beside
  them; at 7:05 the blue flag covers that spot and the block printed 12 13 GND AREF is still bare
  (`merge_t06m43s_shield_before_extension_x4.jpg`, `merge_t07m05s_shield_end_x4.jpg`). So: claw on 10, the plug beside it on 9. Agrees
  with the CAD (plug NAUO85 on row 10: z = 154.55; G x = 50.085, V x = 52.574, S x = 55.064, pin tops y = 113.80).
- **Flags:** black, white printed underlined "6" (the -Z side motor NAUO58, row 6); white paper, hand-written "5" (base motor, row 5);
  blue, white printed "10" (on the extension, about 20 mm from the plug that goes on the shield). The lead on row 9 (the +Z side motor
  NAUO66): flag not established (section 5, point 12).
- **Not connected:** USB, power jack. Driver on the worktop at the right. No spare parts in view.

## 4. Proposed guide steps for this section

House style: one part or one wire per step; each row below is a `Step N` (the part hovering, or the wire as it was) and a `Step Nc`
(in place). Captions use the engraved codes and TechBox's part names (Claw Motor, 16mm / 10mm / 6mm Hex Screw, Servo Extension Wire,
Nano I/O Module). "Travels" is the way the part moves to its seat, in assembly space for the CAD pose; `direction=` in `guide.py` is the
opposite (the side it hovers on). n = [0.011, 1, 0] is the claw's plate normal.

### 4.1 The claw, built on its own (a staged sub-assembly; steps K1-K14)

| # | Draft caption | Moves | Appears with it / already there | Travels | Notes |
|---|---|---|---|---|---|
| K1 | Begin with C3. Push the claw motor through C3, wire first, until it rests on C3. | NAUO72 + horn NAUO73 (one part; lead NAUO94 and plug NAUO90 ride on it) | C3 NAUO34 appears in place | +Y through the cut-out [335.27, 194.72, 143.81]; `direction=[0, -1, 0]` | Video 0:01-0:16. The motor goes in from C3's engraved side; the horn end stays on that side. One axial lead line. The lead is shown loose from this step on. |
| K2 | Feed the claw motor's wire through the hole in the end of C3. | wire only (NAUO94) | - | lead re-routed over C3's plain face and through the hole [300.78, 195.09, 147.06] | Video 0:16-0:24, straight after the motor is in. Eye on the hole. From here the lead leaves the claw through this hole in every later step. |
| K3 | Insert C1 into C3. | C1 NAUO32 | - | -n (prongs down through C3 at [317.12, 194.92, 164.7]); `direction=[0.011, 1, 0]` | Video 0:26-0:31. The side of C3 with two slots; outer slot; engraved face outwards. Needs the tilted direction (4.3). |
| K4 | Insert C2 into C3. | C2 NAUO33 | - | -n at [317.12, 194.92, 128.05]; `direction=[0.011, 1, 0]` | Video 0:32-0:38. The side with one square slot; outer half; engraved face outwards. |
| K5 | Insert C4 into C3, next to C2. | bar NAUO36 | - | +Y, tab into C3 at [315, 194.9, 131.05]; `direction=[0, -1, 0]` | Video 0:50-1:02. Engraved face towards C2. Its step sits on the motor's tab. |
| K6 | Insert C5 into C3, next to C1. | bar NAUO37 | - | +Y at [318.29, 194.9, 157.22]; `direction=[0, -1, 0]` | Video 1:03-1:16. Engraved face towards C1. |
| K7 | Place C6 onto C4 and C5. | plate NAUO35 | - | +Y onto the bars' tabs ([315, 181.4, 131.05], [318.15, 181.4, 157.22]); `direction=[0, -1, 0]` | Video 1:17-1:40. Engraved face away from C3; the horn stands in the keyhole. Free in a straight move with the horn on. A tight push fit. |
| K8 | Screw C6 onto C3 with two 16mm screws. | NAUO74 | - | +Y, head ends at [322.93, 176.84, 147.11]; `direction=[0, -1, 0]`, `axial=True` | Video 1:41-1:55. Hole beside the code. Clamp. Close-up is reasonable (small part). |
| K9 | Add the other 16mm screw. | NAUO75 | - | +Y, [347.24, 176.58, 147.03]; `direction=[0, -1, 0]` | Video 1:56-2:16. Hole in the front lug. Two screws only, so each has its own ordinary step. |
| K10 | Place C7 over the servo horn. | jaw NAUO39 | - | +Y, horn slot over the horn at [342.02, 178.14, 137.91]; `direction=[0, -1, 0]` | Video 2:17-2:23. Engraved face away from C6. Leave the horn out of the motion test and name it in `lines_to=` (the CAD overlaps 0.35 mm). |
| K11 | Press C9 onto C1 and C2 until the clips come through. | cover NAUO40 | - | +Y, slots at [316.8, 175.41, 164.7] and [316.8, 175.41, 128.05]; `direction=[0, -1, 0]` | Video 2:29-2:41. Engraved face out; the big hole over the horn's screw. Snap fit: needs force. |
| K12 | Slide C8 between C6 and C9 until its teeth meet C7. | jaw NAUO38 | - | -Z, in the jaw layer y 176.6-179.6; `direction=[0, 0, 1]` | Video 2:42-2:53 (there from the +Z front corner; straight -Z is free in the CAD). Engraved face away from C6. Review: see section 5, point 2. |
| K13 | Screw C8 in place with a 10mm screw. | NAUO76 | - | +Y, head ends at [335.39, 170.7, 156.09]; `direction=[0, -1, 0]`, `axial=True` | Video 3:04-3:28. Through C9 and C8 into C6. Pivot. |
| K14 | (note card, optional) Open and close the claw by hand to check that both sides move together. | - | - | - | Video 3:29-3:32. Turns the unpowered motor by hand; ask Lee whether students should (section 5, point 6). |

### 4.2 Claw onto the arm, and the wiring (steps K15-K23)

| # | Draft caption | Moves | Travels | Notes |
|---|---|---|---|---|
| K15 | Turn the claw over and place it between A5 and A13, with C1 against A12 and A13. | the whole claw (NAUO32-40, 72-76, with the lead) | back along the forearm, [-0.91, 0.41, 0]; `direction=[1, 0, 0]` or `[0.91, -0.41, 0]` (both free) | Video 3:42-3:53 (there against the +Z strips only, A5 added later). `seat()` of the sub-assembly. Body 39.65 mm wide between z 126.55 and z 166.2, no gap either side. |
| K16 | Screw A12 to C1 with a 6mm screw. | NAUO77 | -Z, head ends at [311.98, 205.67, 172.23]; `direction=[0, 0, 1]`, `axial=True` | Video 3:54-4:16. Into the BODY hole of C1. Pivot. First of the three: close-up. |
| K17 | Screw A13 to C1 with a 6mm screw. | NAUO78 | -Z, [301.81, 188.27, 172.23]; `direction=[0, 0, 1]` | Video 4:28-4:52. Into the LEG of C1 (the wrist). Pivot. |
| K18 | Screw A5 to C2 with a 6mm screw. | NAUO79 | +Z, [301.86, 188.36, 120.52]; `direction=[0, 0, -1]` | Video 5:10-5:29. Into the leg of C2, from the other side. Pivot. Needs a camera from the -Z side. |
| K19 | Feed the claw motor's wire through the top hole in A6. | wire only (NAUO94) | lead re-routed under the claw, along the forearm and through [222.76, 214.43, 144.49], back face to engraved face | Video 5:49-6:04. Eye on the hole. |
| K20 | Then feed it through the bottom hole in A6. | wire only (NAUO94) | on down A6's engraved face and through [186.70, 174.50, 144.49], engraved face to back; plug ends inside the turret | Video 6:05-6:21. |
| K21 | Connect the claw motor's wire to the servo extension wire. | plug NAUO90 into coupler NAUO91 (the extension NAUO93 with NAUO91, NAUO92 and NAUO85 appears) | along the join's axis: in the CAD pose the motor's plug mates towards -X at y 133.6, z 140.7-148.6 | Video 6:21-6:39 (made in the air above the turret). Brown to brown. The coupler arrives on the extension. |
| K22 | Connect the servo extension wire to 10. Remember brown to G, red to V, and yellow to S. | plug NAUO85 | -Y onto row 10: plug body [48.57-56.47, 107.97-121.97, 153.28-156.03] | Video 6:44-6:50. Destination label "10" on the pin row. "Yellow" is the video's signal colour; see section 5, point 10. |
| K23 | Move the servo extension wire into the L-shaped slot in R4. | wire only (NAUO93; the join NAUO90-92 rides) | wires down into the slot mouth at R4's top edge (z 140.60-142.72, y 146.59); join inside the turret behind R4 | Video 6:51-6:57. Eye on the slot. On video this comes AFTER K22; the base motor in the present guide does slot first, plug second. Either order works. |

After K23 the present guide's last card stands as it is ("Connect the power cable to the nano."): this video shows no power step.

Three 6 mm screws go into three different joints from two sides, and the video does them one at a time with the robot turned round for
the third, so they are proposed as three steps (K16 with the close-up) rather than "one, then the rest".

### 4.3 The video's order tested against the CAD

One run of `stepgen.blocked` / `free_directions` with the generator's defaults, each part against everything the video has in place at
that moment (script and log in the merge's scratch folder, `order_check.py`, `order_diag.py`):

| Step | Result |
|---|---|
| Motor + horn into C3 | free, pulled away along -Y (so it goes in +Y). |
| C1, C2 into C3 (before the bars) | along exact +Y the test says blocked: two sample points on the prong's barb ([311.83, 177.13, 163.3-166.1] on C1, [311.88, 177.11, 126.7-129.4] on C2) meet C3 16.3 mm up, because the claw is tilted 0.6 degrees. Along the claw normal [0.011, 1, 0] both are free. Give `direction=[0.011, 1, 0]`. |
| Bars C4, C5 (clips already in) | free along -Y. |
| C6 with the horn on the motor | free along -Y, with or without the horn in the test. |
| Jaw C7 | free along -Y with the horn left out; blocked with the horn in (the known 0.35 mm CAD overlap). |
| C9 with only jaw C7 under it | free along -Y. |
| Jaw C8 after C9 (video) | free along +Z only (so it slides in -Z). Diagonal directions towards the front corner are blocked in the test. |
| Jaw C8 before C9 (CAD order) | along exact -Y blocked by one tooth point on jaw C7 (the tilt again); free along [-0.011, -1, 0] and along +Z. |
| Whole claw into the fork (A5, A12, A13 and their neighbours in place) | free along +X and along the forearm [0.91, -0.41, 0]. |

So the video's order can be shown with straight moves throughout.

## 5. Uncertain, contradictory, or where the CAD may not match

1. **Upside-down build against the CAD pose.** On video every claw part goes on from above with its engraved face up. In the CAD pose
   the motor, both bars, C6, both 16 mm screws, C7, C9 and the pivot screw go on from underneath, and the codes of C3, C6, C7, C8 and C9
   face down. The rulebook wants a hovering part above or beside its seat and the kit shown turned over for underside work; the player
   cannot turn a sub-assembly over yet (rulebook section 14). Either the claw is shown in the CAD pose with parts arriving from below
   (as B1 under B2 is now), or the generator gains a way to show a staged sub-assembly turned over. Decision for Lee; the second matches
   the video and shows the codes.
2. **Jaw C8 after the cover.** The builder lays C8 in place at 2:26, takes it off, presses C9 on with only C7 underneath, and slides
   C8 in afterwards. Both segments agree on what happens. Whether that is TechBox's intended method or this builder's habit is not known.
   The CAD allows both. K11-K12 follow the video.
3. **Clips first.** The CAD-derived order puts C1 and C2 on last; the video puts them on second and third. Both pass the collision
   test. The video's order changes what the clips do: C6 and C9 are lowered over prongs that are already standing.
4. **The horn.** Fitted and screwed before 0:00; never centred on camera; the CAD has no horn screw. With the jaws closed the horn
   points straight forward (segment 1) or within about 15 degrees of it before the jaw is on (segment 2): the same thing. At what motor
   angle the horn was fitted (so which end of the joystick's travel is "closed") is not shown in any of the four videos. A "claw motor
   arrives with its horn fitted" start matches the video and the base motor's treatment; a centring step would have to come from the
   build notes.
5. **Screw lengths are judged by eye:** 16 mm for NAUO74 / 75 (blurred frame plus the stack height), 10 mm for NAUO76 (4 mm proud
   before driving), 6 mm for NAUO77 / 78 / 79 (short shank). All agree with the CAD; none measured.
6. **Pivot tightness and the hand test.** NAUO76, 77, 78, 79 are driven until the head is down with no backing-off seen, and the parts
   still swing (jaws at 3:29, claw on the first arm screw at 4:24, claw tilting at 5:34 and 7:00). "Tighten, then check it still moves"
   is the most the video supports. The jaw test at 3:29 turns an unpowered motor by hand.
7. **Arm pose.** On video the strips hang folded and are lifted to the claw; the claw goes onto the +Z strips alone, one screw at a
   time, and the arm is laid flat, turned end for end and stood upright as needed. The CAD has one pose (forearm 24 degrees below
   level, claw level), and the player does not move joints. K15 uses the CAD report's tested slide into the fork instead.
8. **The claw motor's lead length.** Segment 1 guessed about 200 mm, segment 2 150 to 200 mm; the CAD lead NAUO94 is 268 mm from motor
   to plug. The lead reaches from the claw through both holes of A6 to the top of R4, which needs roughly 240 mm, so the eye estimates
   are probably low (merge's reckoning, not a measurement). It looks like an ordinary motor lead with an ordinary 3-way socket; nothing on
   video shows it shortened. The CAD mesh name `MG90S_Cut wires shorter` refers to the 0.5 mm modelled stubs.
9. **The coupler.** It is already on the extension's plain end when the lead is picked up; no step shows it being fitted, and whether
   it has pins inside could not be seen. If the kit ships coupler and extension separately, one more step is needed that no video covers.
   The sleeve is 10 mm wide and cannot pass A6's 8 mm holes, so threading must come before the join (K19, K20 before K21).
10. **Extension colours and conductor order.** Twisted yellow / red / brown on video (yellow = signal, meeting the motor lead's orange);
    the guide's lead colours are brown / red / orange. `cad_wire_paths.md` section 5 notes that the CAD's claw chain swaps the outer
    conductors once too often. Which way round the plug went on row 10 (brown to G) was hidden by the hand.
11. **Where the join sits.** CAD: plug NAUO90, coupler NAUO91, plug NAUO92 in a straight HORIZONTAL line along -X at y 133.6
    (x 167.88 down to 138.88), the claw lead dropping just in front of R3 and the extension leaving through the POCKET of R4's slot.
    Video: the join stands roughly UPRIGHT just behind R4, the claw lead comes to it in one slack line from A6's lower hole, and the
    extension's thin wires sit in the slot. The coupler itself could not pass the slot (mouth 2.12 mm, pocket 8.1 x 8.5 mm).
12. **Flags and rows.** "5" (white, hand-written) is certain at 0:00 (merge's look at native size); "6" (black, printed, underlined)
    and "10" (blue, printed) are certain. Row 10 for the extension and row 9 for the plug beside it rest on the before-and-after views
    of the 8 9 10 11 block plus the flag and the CAD; no frame shows the plug's foot on the pins. The flag on the row 9 lead is not
    established: at 7:02 a white flag shows a closed loop with a straight stroke beside it (`merge_t07m02s_white_flag_x7.jpg`), which
    could be an underlined 9 or the "5" seen at an angle; a second small white tag stands behind the "5" flag at 0:00. The Arm.mov merge
    also has that flag as "read as 9, not certain".
13. **Segment 2's "second tag, perhaps a 7" at 3:40.** Looked at by the merge at 3:39-3:42, enlarged: the mark is wood-coloured and
    appears on two uprights; it is the slot cut in the top of each B6 wall, not a wire flag
    (`merge_t03m39s_to_42s_B6_slot_not_a_flag_x5.jpg`). The "loose black plug end" beside it is most likely the black housings of the
    joystick jumpers on the analogue header (guess).
14. **Side-motor leads.** Rows 6 and 9 were plugged in between Arm.mov and Claw.mov; no video shows it, or how those two leads were
    routed. The pinch at 6:56-6:57 on the +Z motor's lead by the front lug of the +Z side plate is a guess at re-seating it in a slot.
15. **Order of the last two wiring actions.** Video: plug onto row 10, then wires into R4's slot and join pushed down. Lee's rule for
    motor leads (and the base motor in the present guide): into the slot first, plugged in last. Either works mechanically.
16. **Slack.** How much lead is left at the wrist for the claw to tilt, and which way the slack was pulled at 6:10-6:13, cannot be told.
    Nothing ties or clips the lead along the forearm.
17. **Hidden by hands:** the plug passing each hole of A6 on the far side, the plug going onto the shield pins (6:47-6:50), and the join
    being pushed down behind R4 (6:53-6:55).
18. **Near-twins a student can swap.** C1 and C2 share an outline; bars C4 and C5 look alike (tab width 7.6 against 10 mm). The builder
    goes by the codes: C2 and C4 on the side of C3 with the single square slot (the shaft side), C1 and C5 on the side with two parallel
    slots, all four engraved faces outwards. A12 and A13 differ only by their mark (triangle, square).
19. **Press fits a rigid model cannot show:** the bars into C3, C6 onto the bars (about twenty seconds of pressing), C9 over the barbed
    prongs (about eight seconds, two hands), jaw C7 over the horn.
20. **Where the extension lead came from.** Segment 3 has it picked up from the right of the frame; at 5:43 the builder's arm reaches
    off the top of the frame, and a lead with a black connector lay at the top left from 3:40. Not important for the guide.
21. **Small timing difference between segments:** segment 1 stops at 2:35 with C9 still being pressed; segment 2 has it pressed until
    2:40 and the hands off at 2:41. The second is the full action.

## 6. Reference stills

All in `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/claw/` (720 x 1280 unless a crop).

- `t00m00s.jpg` - start: every claw part laid out engraved face up, motor with horn already on, controller at the top right.
- `t00m12s.jpg` - C3 on edge, lead already through the cut-out, motor about to follow, case first, from the engraved face.
- `t00m17s.jpg` - motor seated in C3: tabs on the engraved face, shaft at the near end, horn pointing forward.
- `t00m24s.jpg` - lead brought out through the tongue hole to the engraved side.
- `t00m27s.jpg` - clip C1 in the hand: code, two holes, two prongs, leg.
- `t00m38s.jpg` - both clips in: prongs and legs standing up from C3's engraved face; code C2 on the outer face of the near clip.
- `t00m57s.jpg` - bar C4 going into the near slot, inboard of C2's prongs.
- `t01m17s.jpg` - both bars in, stepped edges over the motor's tabs; blank inner face of bar C5; clip teeth in the front notches.
- `t01m20s.jpg` - plate C6 tilted in over the horn; its three small holes and open keyhole.
- `t02m17s.jpg` - C6 down, both 16 mm cap heads in, pivot hole empty, horn lying above the plate.
- `t02m18s.jpg` - the same a second later, with the whole lead and its plug in view.
- `t02m23s.jpg` - jaw C7 pressed over the horn.
- `t02m24s.jpg` - jaw C7 seated, engraved face up, all six horn holes showing.
- `t02m26s.jpg` - jaw C8 tried in place: gear mesh and pivot hole visible with no cover on.
- `t02m33s.jpg` - cover C9 lowered over the prongs with only jaw C7 underneath; jaw C8 lying loose at the top.
- `t02m41s.jpg` - C9 pressed on: prong tips through its slots, horn screw in the big hole, pivot hole still empty.
- `t02m48s.jpg` - jaw C8 being slid, gear end first, into the gap between C9 and C6; clip C1 with its two holes at the top.
- `t03m07s.jpg` - 10 mm pivot screw standing in the small hole of C9 before it is driven; both jaws in and closed.
- `t03m30s.jpg` - jaws pulled open by hand after the pivot screw is in.
- `t03m40s.jpg` - the robot before the claw goes on: arm standing, cross plate A6, shield with the flag "6", lid B8.
- `t03m46s.jpg` - claw, right way up, held against the inside of strips A12 and A13.
- `t04m00s.jpg` - first 6 mm screw started by hand through the end of A12 into C1.
- `t04m30s.jpg` - first screw in, second in the fingers; lead crossing C3 and going down through the tongue hole.
- `t04m54s.jpg` - +Z side after two screws: A12 (triangle mark) and A13 (square mark) screwed to C1; A10, A8, R6 readable; lead hanging.
- `t05m10s.jpg` - robot turned end for end; third screw in the fingertips about to go through A5 into C2 from the -Z side.
- `t05m33s.jpg` - claw from above: motor in C3, lead leaving at the -Z end and going down through the tongue hole; A6 with both holes empty.
- `t05m34s.jpg` - -Z side: C2 outwards, long strip A5 screwed to it, -Z side motor and clamp plate.
- `t05m57s.jpg` - arm upright; plug being pushed through the elbow-end hole of A6 from behind.
- `t06m09s.jpg` - lead lying on A6's engraved face; plug entering the shoulder-end hole.
- `t06m21s.jpg` - lead through both holes and pulled flat; plug held over the turret.
- `t06m24s.jpg` - the two ends before joining: the claw lead's plug end-on (left hand); the coupler sleeve on the extension, edge-on (right hand).
- `t06m42s.jpg` - join made and hanging over R4; blue flag "10" held to the camera; three plugs on the shield.
- `t06m49s.jpg` - extension plug being pushed onto the shield's digital pins, left forefinger steadying the board.
- `t06m58s.jpg` - end state from the controller side: join upright behind R4, extension wires in R4's slot, lead on A6, four plugs in.
- `t07m01s.jpg` - finished robot tilted to the camera: join, slot, twisted extension looping to the shield, flag "6".
- `merge_t00m00s_flag5_x5.jpg` - crop x5 of 0:00 and 0:02: the white hand-written "5" flag on a plugged-in lead, a second white tag behind it.
- `merge_t03m38s_to_43s_flag6_shield.jpg` - six crops of the shield, 3:38-3:43: the black underlined "6" flag from several angles.
- `merge_t03m39s_to_42s_B6_slot_not_a_flag_x5.jpg` - crop x5: the mark segment 2 took for a possible "7" is a slot in a B6 wall.
- `merge_t05m42s_arm_upright_three_plugs.jpg` - arm stood upright, A6's two holes empty, claw lead hanging on the +Z side, three plugs in.
- `merge_t06m23s_coupler_and_plug.jpg` - the coupler sleeve seen broad face on (right hand) and the claw lead's plug (left hand).
- `merge_t06m43s_join_over_R4_flag10.jpg` - the join hanging over R4, flag "10" readable, lead on A6's face.
- `merge_t06m43s_shield_before_extension_x4.jpg` - crop x4: rows before the extension goes in (row 4 bare; "10 11" end of the third block bare).
- `merge_t07m02s_white_flag_x7.jpg` - crop x7: the white flag whose mark could be an underlined 9 or the 5 at an angle.
- `merge_t07m05s_end.jpg` - the last frame with the hands away.
- `merge_t07m05s_shield_end_x4.jpg` - crop x4: rows at the end (blue flag over the third block; block 12 13 GND AREF bare).

Working frames, sheets and the CAD test scripts (not part of the project):
`/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/06aa2268-0605-4ce1-8b0c-854218069941/scratchpad/research_r2/video_claw_merge/`.
