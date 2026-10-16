# Claw.mov, stretch 1 (0:00 to 2:35): what the builder does

Status: COMPLETE for this stretch (overview at 2 s over the whole stretch, then every action re-read at 1 s, full size or enlarged crops).

Source: `/Users/lee-johnson/Desktop/Claude_Cadasio/MRA_Videos/Claw.mov` (7:06 long, 1080 x 1920 portrait phone video). This file covers video
seconds 0 to 155. All times are the video's own. Nothing is plugged into the shield, no servo is powered and nothing is joined to the arm in
this stretch: it is the claw sub-assembly, built in the hand and on the worktop, from the servo up to the bottom cover.

What I could not see is said where it applies. CAD ids and coordinates (mm, assembly space) are taken from
`docs/research/mra/cad_arm_claw.md` and `mra_instances.json`; I did not re-measure the CAD.

## 0. Three things the merge needs first

1. **The claw is built upside down compared with the CAD pose.** Every plate is handled with its engraved face up: C3, then the plate
   engraved C6, the jaws and C9 are stacked upwards on the worktop while the servo case and the bodies of the clips C1 / C2 hang underneath.
   In assembly space that stack runs in -Y (C3 at y 193-196 is the top plate of the finished claw; C9 at y 174-177 is the bottom).
2. **The engraved codes differ from the CAD names for five parts**, all read clearly on the video:

   | Engraved on the wood | What it is | CAD id | CAD mesh name |
   |---|---|---|---|
   | C1 | clip plate, two small holes, far side as built (+Z) | NAUO32 | ARA_C1 |
   | C2 | clip plate, one small hole, near side as built (-Z) | NAUO33 | ARA_C2 |
   | C3 | servo plate with the tongue and cable hole | NAUO34 | ARA_C3 |
   | **C4** | spacer bar on the C2 side (-Z) | NAUO36 | ARA_C5 |
   | **C5** | spacer bar on the C1 side (+Z) | NAUO37 | ARA_C6 |
   | **C6** | keyhole plate (the second plate of the stack) | NAUO35 | ARA_C4 |
   | **C7** | jaw with the horn-shaped slot (driven jaw) | NAUO39 | ARA_C8 |
   | **C8** | jaw with the small pivot hole (geared jaw) | NAUO38 | ARA_C7 |
   | C9 | cover plate with the 11.7 mm hole | NAUO40 | ARA_C9 |

   This agrees with the "engraved" column of section 9 of `cad_arm_claw.md`; the video confirms it part by part.
3. **The order is not the CAD-derived order.** On video the clips C1 and C2 go into C3 straight after the servo (second and third wooden
   parts), not last; the horn is already on the servo before anything is assembled; and the cover C9 goes on with only ONE jaw (engraved C7)
   in place. The second jaw (engraved C8) is offered up, taken away again, and is fitted after C9 (just past the end of this stretch).

## 1. State at the start (0:00)

Still: `docs/research/mra/stills/claw/t00m00s.jpg`.

- Top right of the frame: the finished base with the controller. Joystick box with its lid engraved B8 and the words Shoulder, Elbow, Base and
  Claw with arrows; B5 engraved on the box wall facing the camera; two joystick caps. Behind it the Nano on the blue I/O shield with the rainbow
  jumper ribbon and three servo leads (brown / red / orange) already plugged in. One of those leads carries a white tape flag with a
  handwritten **5** (read at native resolution; which row it is in cannot be seen from here). Turret walls engraved R5 and R4 are just in
  frame at the top edge. The arm itself is out of frame for the whole stretch. A dark grey T-handle hex driver lies at the right edge.
- Loose on the worktop, every wooden part lying engraved face up except one spacer bar:
  - the claw servo (MG90S, blue and red label), NAUO72, **with a black single-arm horn already pressed on its shaft and a silver
    cross-head screw already in the hub** (horn = NAUO73; six small holes along the arm). Its lead (brown / red / orange, black 3-pin socket)
    trails off to the left. There is no coupler or extension on it yet.
  - plate engraved C6 (keyhole plate, NAUO35), engraved C9 (NAUO40, half out of frame at the left), the two jaws stacked one on the other
    (C7 on top, its code readable; the one underneath is C8, read later), clip C1 (NAUO32), plate C3 (NAUO34), clip C2 (NAUO33), the spacer
    bar engraved C4 (code up, NAUO36) and the other spacer bar code down (it is C5, NAUO37, read at 1:06).
  - With their engraved faces up, C1 and C2 are mirror images of each other. C1 has a hole in the end of its leg and a second hole in the
    body; C2 has only the hole in the leg.
- No screws are in view yet; they are brought in from off-frame one at a time.

## 2. Timeline

Directions are given two ways: as seen (the claw upside down, engraved faces up) and, in brackets, in assembly space for the CAD pose.
"Near" is the side towards the builder (the C2 side, -Z); "far" is the C1 side (+Z); "back" is the tongue end of C3 (-X); "front" is the
jaw end (+X).

1. **0:01-0:10 - servo lead threaded through C3.** Right hand lifts the servo, left hand lifts C3 (engraved face towards the camera). The
   plug on the end of the servo lead is fed down through the rectangular servo cut-out of C3 **from the engraved face** (first try 0:04-0:07,
   C3 slips at 0:08-0:09, plug through at 0:10). Certain.
2. **0:11-0:16 - servo pushed through C3.** C3 is held on edge; the servo follows its lead through the cut-out, **case bottom first, from
   the engraved face**, until both mounting ears stop flat on the engraved face (0:15). (Assembly space: servo moves +Y up through C3; ears
   under C3. Cut-out centre [335.27, 194.72, 143.81].) Seated, the gear housing, shaft and horn stand proud of the engraved face; the case
   hangs out of the other face. The shaft is at the **near (-Z) end** of the cut-out, the end with the single big square slot beside it; the
   horn points **straight to the front**, away from the tongue, square to the plate (CAD horn direction [1, 0, -0.03]: the same). The horn is
   not touched, turned or removed. No screws go through the servo ears, here or later. Stills `t00m12s.jpg` (servo about to enter),
   `t00m17s.jpg` (seated). Certain.
3. **0:16-0:24 - lead taken out through the tongue hole.** The lead is now on the case side of C3. The builder pulls it straight
   (0:17-0:18), then pushes the plug through the small rectangular hole in the tongue of C3 **from the case side out to the engraved side**
   (0:19-0:20) and pulls the whole lead through after it (0:21-0:24). At 0:22 the lead can be seen through the near-side square slot,
   running behind C3 from the shaft end of the servo to the tongue. Result: lead leaves the servo on the case side, runs along the
   non-engraved face of C3 to the tongue, and comes out of the tongue hole on the engraved side. (Assembly space: over the top of C3, down
   through the 10 x 6.3 mm tongue hole, out underneath; this is also how the CAD lead is modelled.) Still `t00m24s.jpg`. Certain.
4. **0:26-0:31 - clip C1.** Right hand picks up C1 (code read at 0:27, still `t00m27s.jpg`), carries it round behind C3 and pushes its two
   sprung prongs through the **outer of the two parallel slots on the far side** of C3, **from the case side towards the engraved side**, in
   one push. The prongs now stand up out of the engraved face; the leg with the hole stands up beside the tongue, on the far side of it.
   (Assembly space: prongs go down, -Y, through C3 at [317.12, 194.92, 164.7]; body on top of C3.) Engraved face of C1 outwards (+Z): not
   seen directly (it is in shadow), but with the leg at the tongue end and the prongs through from the case side it can only sit that way.
   Fairly sure.
5. **0:32-0:38 - clip C2.** Left hand picks up C2 (code read at 0:33), and its prongs are pushed up through the **outer half of the single
   square slot on the near side** of C3, again from the case side. Its engraved face is outwards (-Z): the code is readable on the outer
   face at 0:35-0:38. Leg with the hole beside the tongue, on the near side of it. (Assembly space: [317.12, 194.92, 128.05], -Y.) Both
   clips also have a small tooth at the front that shows in the two open notches in the front edge of C3 (seen at 0:42 and 1:17). Still
   `t00m38s.jpg` shows both clips in, both pairs of prongs and both legs standing up from the engraved face, and the lead through the tongue.
   Certain.
6. **0:39-0:48 - put down.** The lead is lifted clear and laid away to the upper left (0:39-0:40). The sub-assembly is set on the worktop
   **engraved C3 face up**, resting on the servo case and the clip bodies, tongue to the left (0:41). The builder pinches the far clip's
   prongs once (0:42-0:43), then hands off (0:44-0:47). The camera moves in close at 0:47-0:48 and stays close.
7. **0:50-1:02 - spacer bar engraved C4 (NAUO36).** Right hand picks it up from the lower right (code read 0:52-0:54), stands it on edge
   and pushes its lower tab straight down into the **inner half of the near-side square slot** of C3, directly inboard of C2's prongs
   (0:55-0:58); then presses it home with the fingertips (0:59-1:02). **Engraved face outwards** (towards C2; the code can be made out on the
   near face at 0:57 and 1:04). The bar runs front to back along the near edge and its stepped edge passes over the servo ear at the shaft
   end, so that ear is now held between C3 and the bar. (Assembly space: tab into C3 at [315, 194.9, 131.05], moving +Y; shoulder under the
   ear.) Still `t00m57s.jpg`. Certain.
8. **1:03-1:16 - spacer bar engraved C5 (NAUO37).** Picked up from the right (code read 1:06-1:07), stood on edge and pushed down into the
   **inner of the two far-side slots** of C3, inboard of C1's prongs (1:08-1:11). The face towards the camera (the inner face) is blank, so
   its **engraved face is outwards** (towards C1). It passes over the other servo ear. (Assembly space: [318.29, 194.9, 157.22], +Y.) Then
   the builder lifts the whole thing a little and squeezes each bar down hard between finger and thumb (1:12-1:16). Still `t01m17s.jpg`
   shows the result from above: servo trapped by both bars, both clips, lead through the tongue. Certain.
9. **1:17-1:40 - keyhole plate engraved C6 (NAUO35).** Right hand brings it over **engraved face up** (code read 1:19-1:20, still
   `t01m20s.jpg`). Its big cut-out is a round hole that is **open to the front edge**; the plate comes in tilted, back edge high, and is
   lowered so the horn hub stands in the round part and the horn arm lies across the open gap (1:20-1:21). So the plate goes on **with the
   horn already on the servo**, and the horn ends up above the plate. The upward tabs of the two bars enter its slots and the prongs of C1
   and C2 come up through it (C1: outer far slot; bar C5: inner far slot; C2 and bar C4 share the near square slot). It is then pressed and
   squeezed down for about twenty seconds (1:22-1:40), corner by corner and with the stack lifted and pinched: a tight fit. (Assembly
   space: plate moves +Y onto the lower tabs of the bars.) Certain.
   The plate has three small holes, identified by their spacing from the shaft: one just in front of the code (back screw hole), one in the
   lug at the front edge beside the keyhole opening (front screw hole), and the smallest one on the far side of the shaft (the jaw pivot hole).
10. **1:41-1:55 - first M3x16 screw (NAUO74).** A long silver socket-cap screw is brought in (blurred at 1:41.5: the shank is about three
    head-widths long, so 16 mm; a 10 mm screw would not reach, the stack is 3 + 10.5 + 3 mm) and dropped into the **back hole of C6, the
    one beside the code** (1:42-1:44). Driven **from the engraved side** with the T-handle hex driver (its handle is marked "3.0") until
    the head is down on C6 (1:46-1:54); driver put down (1:55). Tightened fully: it is a clamp, not a pivot. (Assembly space: head end at
    y 176.8, axis +Y, at [322.93, 176.84, 147.11]; free through C6 / CAD C4, threads into C3.)
11. **1:56-2:16 - second M3x16 screw (NAUO75).** Same kind of screw (shank seen spinning at 1:57.5), stood in the **hole in the lug at the
    front edge of C6**, close to the tip of the horn (1:58-2:03; fiddly, the fingers have to work round the horn), driven home the same way
    (2:05-2:13), driver put down (2:14-2:16). Tightened fully. (Assembly space: [347.24, 176.58, 147.03], +Y.) Still `t02m17s.jpg`: both
    cap heads on C6, the third hole (pivot) still empty. Certain.
12. **2:17-2:23 - jaw engraved C7 (NAUO39) onto the horn.** Right hand brings the jaw, **engraved face up**. The jaw has a through-slot the
    shape of the horn (round at the gear end, long and narrow towards the tip). It is lowered over the horn, round end over the hub
    (2:19-2:20), and pressed down with the left forefinger until it lies flat on C6 with the horn sunk in the slot (2:21-2:22). The horn is
    not unscrewed or turned: the jaw simply takes up the horn's angle, so it points straight forward, its hooked tip curling towards the
    far side. Nothing screws the horn to the wood. (Assembly space: jaw moves +Y onto the horn; horn at [342.02, 178.14, 137.91].) Still
    `t02m23s.jpg`. Certain.
13. **2:24-2:28 - jaw engraved C8 (NAUO38) offered up, then put aside.** Right hand picks up the second jaw (code read 2:26), holds it
    **engraved face up** flat on C6 with its small centre hole over the pivot hole of C6 and its teeth meshed with the teeth of C7, tip
    pointing forward, its hook curling towards C7 so the two half-round bites in the jaws face each other (2:26). It is **not left there**:
    by 2:27-2:28 it has been laid down again at the top of the frame, beyond the lead. No screw is fitted. Certain about what happens; why
    is a guess (showing the camera where it goes).
14. **2:29-2:35 (still going at the end of the stretch) - cover engraved C9 (NAUO40).** Right hand brings C9, **engraved face up**
    (2:30-2:31), and lowers it onto the stack: its two short slots go over the tips of the prongs of C1 (far) and C2 (near), its 11.7 mm
    round hole sits over the horn hub (the horn screw shows through it) and its small hole lines up over the pivot hole. It rests on jaw C7
    and on the two cap heads; the front cap head stays just visible beyond its front edge. From 2:32 both hands are pressing it down over
    the prongs. At 2:35 it is seated on the prong tips but I cannot say the barbs have snapped through yet. (Assembly space: C9 moves +Y;
    slots at [316.8, 175.41, 164.7] and [316.8, 175.41, 128.05].) Still `t02m33s.jpg`. Certain.

No wire is plugged in, no servo is centred or tested, and no horn is fitted, removed or turned anywhere in this stretch.

## 3. State at the end (2:35)

On the worktop, upside down, from the bottom up: clip bodies of C1 and C2 and the servo case; C3 (engraved face up); spacer bars engraved
C4 (near) and C5 (far) with the servo ears trapped under them; plate engraved C6 held down by two M3x16 cap screws; jaw engraved C7 pressed
over the horn, pointing straight forward; cover C9 lying on top, being pressed down over the prongs of the clips. The servo lead comes out
of the tongue hole of C3 on the engraved side and lies loose on the worktop to the upper left, its plug free. Jaw engraved C8 lies loose at
the top of the frame. Not yet fitted: jaw C8, the M3x10 jaw pivot screw (NAUO76), the three M3x6 screws to the arm, the coupler and the
extension lead.

Looking ten seconds past my end, only to line up with the next report (which covers it properly): C9 is pressed until about 2:40; at
2:42-2:51 the builder picks up jaw C8 again and **slides it in from the front, gear end first, between plate C6 and cover C9**.

## 4. Hard to show in a 3D guide, or different from the CAD

- **Upside-down build.** The natural camera for these steps looks at the underside of the claw (assembly -Y towards the viewer), with the
  tongue at the left. In the CAD pose every one of these parts would be going on from underneath.
- **Step order against the CAD order (section 7.5 of `cad_arm_claw.md`).** Video: servo, lead through tongue, C1, C2, bar C4, bar C5,
  plate C6, screw, screw, jaw C7, cover C9, then jaw C8. CAD order: servo, bars, plate, screws, horn, both jaws, C9, pivot screw, C2, C1.
  The clips going in early changes what they do: the plate C6 and the cover C9 are lowered over prongs that are already standing there.
- **The horn is pre-fitted.** It is on the shaft, screwed, before the video starts, and it already points straight forward. Nothing in
  this stretch shows the servo being centred, so either it was done earlier or it is still to come; a guide step for it has to come from
  somewhere else. The CAD has no horn screw. The keyhole plate only goes on with the horn in place because its cut-out is open to the front
  edge and the plate is tilted in; a straight drop along the plate normal would also work in the CAD only if the horn is treated as part of
  the servo.
- **The lead.** Two flexible moves (plug down through the servo cut-out ahead of the servo; plug out through the tongue hole afterwards)
  that a rigid model cannot animate. The second one matters for the finished look: the lead leaves the claw through the tongue hole.
- **Servo held without screws.** The ears are clamped between C3 and the stepped edges of the two bars. Easy to miss in a guide because
  nothing visibly fastens the servo.
- **Press fits.** The bars, plate C6 and cover C9 all need real force (C6 about twenty seconds of pressing). The clip prongs are sprung and
  barbed; the snap of C9 over the barbs is not visible as such. The jaw C7 is a push fit on the horn (the CAD shows 0.35 mm of overlap there).
- **Near-twins a student can swap.** C1 and C2 share an outline and would each fit the other side back to front; the two bars look alike
  but differ in tab width (CAD: 7.6 mm for engraved C4, 10 mm for engraved C5). The builder gets them right by code: C2 and C4 on the side
  with the single square slot (the shaft side), C1 and C5 on the side with two parallel slots, all four with engraved faces outwards.
- **Second jaw after the cover.** If the guide follows the video, jaw C8 slides in sideways between two plates that are already fixed,
  which the CAD-derived order never does.
- **Screws.** Socket-cap heads driven with a T-handle hex driver, both from the engraved side of plate C6. Their length (16 mm) is judged
  from blurred frames and from the stack height, not measured.

Open points for the merge: where and when the claw servo was centred and its horn fitted; whether jaw C8 going in after C9 is the intended
method or just how this builder did it; the claw servo lead here looks like an ordinary attached lead (very roughly 200 mm, three C3-lengths
visible on the worktop plus the run behind C3), whereas the CAD names the servo "MG90S_Cut wires shorter" with the lead as a separate part.

## 5. Reference stills

All in `/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/mra/stills/claw/` (720 x 1280).

- `t00m00s.jpg` - start: every claw part laid out engraved face up, servo with horn already on, controller and flag "5" at the top right.
- `t00m12s.jpg` - C3 on edge, lead already through the cut-out, servo about to follow, case first, from the engraved face.
- `t00m17s.jpg` - servo seated in C3: ears on the engraved face, shaft at the near end, horn pointing forward.
- `t00m24s.jpg` - lead brought out through the tongue hole to the engraved side.
- `t00m27s.jpg` - clip C1 in the hand: code, two holes, two prongs, leg.
- `t00m38s.jpg` - both clips in: prongs and legs standing up from the engraved face of C3; code C2 on the outer face of the near clip.
- `t00m57s.jpg` - bar engraved C4 going into the near slot, inboard of C2's prongs.
- `t01m17s.jpg` - both bars in, stepped edges over the servo ears; blank inner face of bar C5; teeth of the clips in the front notches.
- `t01m20s.jpg` - plate engraved C6 tilted in over the horn; its three small holes and open keyhole.
- `t02m17s.jpg` - plate C6 down, both M3x16 cap heads in, pivot hole empty, horn lying above the plate.
- `t02m23s.jpg` - jaw engraved C7 pressed over the horn.
- `t02m33s.jpg` - cover C9 lowered over the prongs with only jaw C7 underneath; jaw C8 lying loose at the top.

Working frames and contact sheets (not kept in the project):
`/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/06aa2268-0605-4ce1-8b0c-854218069941/scratchpad/research_r2/video_claw_seg1/`.
