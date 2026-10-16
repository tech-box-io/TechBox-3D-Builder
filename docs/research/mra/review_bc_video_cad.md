# Review: the rewritten base and controller steps against the build videos and the CAD reports

Written 13 Oct 2026. Status: COMPLETE.

Scope: the 24 steps of `MRA Build Instructions Prototype/guide.py` as generated into `steps.json` (views `Step 1` .. `Step 24`,
48 views with Start and Completed View). Compared with `video_base_seg1.md`, `video_base_seg2.md`, `video_controller_seg1.md`,
`video_controller_seg2.md`, `cad_codes_base.md`, `cad_pins.md`, `cad_wire_paths.md`, `cadasio_mra_project.md` (section 3) and
`lee_notes_2026-10-13.md`.

How: from the documents and `steps.json` only. The CAD was not loaded, nothing was regenerated, no browser was used, nothing in the
project was changed. Poses, lead lines, wire routes and the player's own blending rules (`mixPose`, `skinned` in `js/player.js`) were
replayed with a small pure-Python script on the numbers in `steps.json` (scratch: session scratchpad `review_bc/video_cad/`).
Coordinates are mm in assembly space, Y up. "must fix / should fix / ask Lee" is marked on every finding.

## Lee's question (message 2): does the horn move make sense, and does the guide do it?

Yes. It is what the video shows (Base.mov 0:18 - 0:22) and what the CAD allows (`cad_codes_base.md` 3(a), sequence B), and `Step 2c`
plays it in that order. Read off `Step 2`'s `path` (pivot = the middle of the horn on the shaft, 163.7, 89.4, 140.9; the horn is drawn
1.8 mm lower than the CAD, see `materials.json` `adjust_mm`):

| Beat | Poses | What happens | Lee's words |
|---|---|---|---|
| 1 | path[0] -> [1] | Motor a quarter turn round so the horn lies along R1's cut-out, tilted 12 degrees, straight down 42.1 mm. The leading horn tip ends inside R1's thickness (y 101.5) 0.6 mm from the cut-out's -Z end (z 124.69 against 124.09) | "move it at a slight angle" |
| 2 | [1] -> [6] via [2..5] | Tilt 16 -> 12 -> 8 -> 0 degrees while coming down 7.4 mm and sliding 7.5 mm towards -Z: the leading arm dips under the rim, the hub follows, the trailing tip drops through the notch (z 153.14 against the notch end 153.19). Then 6 mm back towards +Z, level, horn 1.05 mm under R1, gear case 1.1 mm above it | "rotate the Base Motor and its servo horn into the slot" |
| 3 | [6] -> [7] | Quarter turn about the vertical shaft axis (0, 1, 0) at 8.5 mm of lift | "spinning it 90 degrees with respect to the z axis" |
| 4 | [7] -> [8] | Straight down 8.4 mm, ears onto R1 | "setting it in the slot of R1" |

The lift of 8.5 mm for the quarter turn is inside the free window (7.40 mm = gear case clear of R1's top; 9.55 mm = horn arms touch
R1's underside with the horn drawn 1.8 mm lower; 7.75 mm in the unadjusted CAD). The one lead line runs from the leading horn tip
(163.7, 143.8, 125.5 while hovering) to the -Z end of the cut-out (163.7, 103.0, 124.3). Notes, not findings: the tilt is 12 - 16 degrees
with a stated worst overlap of 0.6 mm; `cad_codes_base.md` has a tested overlap-free sequence at 20 degrees and the video's builder lays
the motor over much further. Lee asked for "slight", so this is right as it stands.

## Verdict

Parts, engraved codes, CAD ids, order and insertion directions are right on all 24 steps, and all nine wires are on the right pins.
One thing is plainly wrong on screen (the plug's glide in `Step 23c`). The rest are places where the video's builder does something
with a wire or a snap fit that the guide does not say, and one hand-set path (`Step 22`) that the video can now correct.

## Findings

### F1. `Step 23` / `Step 23c`: the plug glides through the joystick wires and the Nano, and arrives sideways. MUST FIX

- What: the plug (NAUO83) has a two-pose path: from where it rides in the L-slot (`{"t": [58.04, 12.19, 0.67], "r": [-0.618, -0.618, -0.487, 128.1]}`)
  straight to its seat. The player blends that as one straight glide with an even turn.
- Evidence (replayed in 2% steps): between 18% and 52% of the way the plug's body passes through all four right-joystick wires where they
  stand up from A0 / A1 (they occupy x 80.3 - 88.2, y 116 - 149.4 in the plug's lane z 134.5 - 144.5), and through "left GND" / "left V" at
  40 - 46%. From 44% to 92% its lower end is inside the Nano's footprint (x 60.5 - 78.5) at y 118.4 falling to 108.8; the Nano's sockets top
  out at y 114.94 and its board is at about y 117.4 - 119.0. At 90% the mating face is at (56.8, 109.4, 141.1): already 4.4 mm below the pin
  tops (y 113.80) and still 4.3 mm to the side, so it slides onto row 5 from the Nano side through the S pins instead of coming down over
  three pins.
- Video and CAD: Controller.mov 4:10 - 4:19, "carries it over the shield from the right ... pushed straight down onto a 3-pin row";
  `cad_wire_paths.md` 2.1, plug_direction (0, -1, 0).
- Fix: give the step a hand path with a last stop upright and straight above row 5, e.g. `path=[BASE_PLUG_SLOT, via(<lifted clear>), [0, 35, 0], [0, 0, 0]]`
  (35 mm is the rulebook's hover for a plug-in part). The stretch before that stop has to clear y 150 where it crosses x 80 - 88, or go
  round the USB end as the real lead does. Then check it in the player as CLAUDE.md asks.

### F2. `Step 7` (also `Step 5`): nothing tells the student to keep the wire out of R6's way. SHOULD FIX

- What: caption is "Add R6." The picture has the lead standing straight up inside the turret (routes 0 - 2: x 161.1 - 166.2, z 146.8 - 154.8,
  top y 171.1, plug above it to y 184.1), 12.9 mm clear of R6's inner face (z 169.2), so on screen nothing can go wrong.
- Evidence: the real lead does not stand up. It leaves the motor from its +Z end face, heading +Z (`cad_wire_paths.md` 3.1: exit
  (163.64, 119.11, 146.77), direction (0, 0, 1)), i.e. straight out of the open side that R6 closes. Base.mov 3:20 - 3:24: the builder turns
  the box, lifts the lead "up and out through the open top", holds it there, then fits R6; the report adds "If this were not done, R6 would
  trap the lead." At 2:12 - 2:16 the lead is also held up while R4 goes on.
- Fix: `Step 7` caption, e.g. "Add R6. Keep the base motor's wire up through the top so it is not trapped." (wording for Lee). No change to
  the motion.

### F3. `Step 22`: the hand-set path is not what the video shows; the video settles the direction. ASK LEE (the step already carries a Review note)

- What: path `[0, 6, 70] -> [0, 6, 0] -> [0, 0, 0]`: in from +Z, 6 mm high, then a 6 mm drop.
- Right: the side and the way round. Controller.mov 2:46 - 2:57: the shield is carried to the right-hand side (+Z), USB / jack end to the
  right, analogue header towards the turret (the CAD's orientation) and "slid in sideways from the builder's right toward the left (-Z),
  plain end leading: through the right-hand B6 arm first, then on to the left-hand B6 arm".
- Not right: the lift and drop. From `cad_pins.md` section 5: the board's long edges (x 43.36 and 96.70) sit in notches only 1.53 mm tall
  (y 104.78 - 106.31) in each B6 wall, with wood above them (to y 109.4 - 110.2 on the joystick side, to y 118.5 in the tower x 94.86 - 107.6 on
  the turret side). At +6 mm the board (y 110.78 - 112.43) clears the joystick-side wall by 0.6 - 1.4 mm but its +X edge, x 94.86 - 96.70, cuts
  through both towers as it passes them (z 150 - 153, then z 128.6 - 131.6), and the drop takes both edges through the wood above the
  notches. On video there is no lift: 3:05 - 3:07 "pushed the last few mm to the left and pressed down".
- What is still unknown: how the real board passes B4's end post (z 173.45 - 179.80, top y 107.89, 3.11 mm above the board's underside;
  the tails of the 4-pin header at x 69.5 need 4.09 mm). As a rigid part held in the notches it cannot. The video does not show what gives.
- Fix to try: slide at seated height through the notches with only the trailing (USB) end raised about 3 mm (a tilt of about 4 degrees
  about X), levelling over the last few mm. Ask Lee, with the kit in hand, whether the board is tilted or B4 gives. Keep the Review note
  until then.

### F4. `Step 9`: the four lead lines mark where B2 rests under R5 / R6, not the keyhole. SHOULD FIX

- What: guides run from B2's top face to under the bottom edges of R5 and R6: (143.1, 93.8, 109.5 -> 112.0), (184.4, 93.8, 109.1 -> 111.9),
  (136.1, 93.6, 169.3 -> 172.1), (191.9, 94.0, 169.3 -> 172.1).
- Evidence: `cad_codes_base.md` 3(c): "the turret rides on B2 and nothing of the turret is tabbed into B2"; the joint is the keyhole: slot
  x 157.29 - 169.99 from the -Z edge (z 93.34) to the round cut-out centred (163.64, 140.84). The automatic search found the resting contact
  because that is the only contact there is.
- Fix: one hand-set line along the slot, e.g. `lines_at=[[163.6, 92.0, 140.8]]` (the round cut-out's centre: drawn from where it hovers to
  the shaft), or two along the slot's edges at x 157.3 and x 170.0. Direction and distance are right as they are (B2 from +Z by 80 mm; the
  CAD needs 51 mm or more, moving -Z).

### F5. `Step 17` .. `Step 21`: with the I/O module parked on the right, the left joystick's wires cross the bay the right-hand group drops into. ASK LEE

- What: `MODULE_ASIDE = [10.0, -16.3, 100.0]` (on the table beside the +Z long edge; the solder tails rest on the table plane y 87.5). The
  four left wires are drawn stretched from 106 - 113 mm to 171 - 177 mm and cross the right-hand B6's plane (z 150 - 153) at x 63 - 66,
  y 134 - 139.
- Evidence: in `Step 20c` the right-hand B6 arm (wall top y 102.1 at that x, hovering 80 mm up) comes down through those four wires. On
  the bench it means the student has to hold the left ribbon up and lay it over the right-hand group; otherwise B6 or B7 pins it.
  Controller.mov avoids this: the shield lies on the LEFT of the plate from 0:29 to 2:44 (the left group's ribbon goes straight off the
  left edge; the right group's ribbon is draped over walls that are already seated) and is carried over to the right only at 2:45 - 2:46,
  just before it is slid in.
- Is the guide's version safe: yes, nobody gets stuck. The real ribbon is about 200 mm (video estimate), longer than the 177 mm drawn; the
  end result (left wires lying over the right-hand B6 arm) is correct, and the module is already on the side it is slid in from.
- Options for Lee: (a) leave it and add a few words to `Step 20` ("keep the left joystick's wires on top"); (b) park the module on the left
  as the video does and bring it round in `Step 22`.

### F6. `Step 17` and `Step 20`: the hooked ends of the B6 arms get a lead line but no words. ASK LEE

- What: both seats have a line at the hooked post: (102.9, 87.7 -> 93.5, 130.1) and (102.9, 87.5 -> 93.4, 151.5). Captions are the old ones,
  "Then place B5 and B6 onto B3." / "Then place B6 and B7 onto B3."
- Evidence: Controller.mov 1:29 - 1:30, 1:37 - 1:40 and 2:12 - 2:13: each hooked post gets its own firm press into the small slot near the
  turret, separately from pressing the joystick end down. The post reaches y 87.1 (through B2 into B1): a snap fit.
- Fix: a few words on both captions ("... and press the hooked end of B6 into its slot"), or an eye icon on the post in the `c` view.

### F7. `Step 8` / `Step 8c`: the guide does not show or say that the wire goes in from the top edge, on edge. SHOULD FIX (low)

- Right: the eye is on the slot's mouth, (133.4, 146.6, 141.7) against the CAD mouth x 133.44, y 146.59, z 140.59 - 142.73. In `Step 8c`
  all three wires pass R4 inside the pocket (red crosses the mid-plane at (133.44, 130.26, 143.47), the CAD's own point).
- What is missing: the lead is 3.1 x 1.0 mm and the slit is 2.12 mm wide, so it only goes down the slit on edge
  (`cad_pins.md`: "goes into the 2.1 mm entry of R4's slot ... edge-on, then lies in the wider pocket"). Between `Step 8` and `Step 8c`
  the wire is blended from "straight up" to "in the slot". Replayed with the player's own blending: from 57% of the way to the end, the
  stretch 53 - 68 mm from the motor passes through R4's wood beside the slit (y 131.9 - 146.6, z 139.5 - 146.5) instead of coming over the
  top edge and down the slit. The plug itself goes over the top edge without touching R4.
- Fix: an in-between route (lead lying over R4's top edge in the slit's mouth) as the route for `Step 8`, or the words "from the top, on its
  edge" in the caption. Rulebook section 10 allows showing a cable in a notch by its result, so this is a nicety.

### F8. `Step 8` to `Step 22`: once in the slot, the loose lead points at the place where the controller is built. ASK LEE

- What: from `Step 8c` the lead sticks out of R4 towards the controller (drawn in mid-air to x 110.6, plug x 97.6 - 111.6, y 130.8 - 135.3,
  z 136.0 - 144.3; it clears everything that is seated later, checked against both B6 towers, the module and the jumper wires).
- Evidence: a real lead hangs down onto B2 exactly where B4 (x 68.5 - 71.5), the two hook slots (x 97 - 107) and the module (x 43 - 97) go.
  The builder moves it out of the way four times: Base.mov 4:18 - 4:19, Controller.mov 0:07 - 0:10, 1:07, 3:08 - 3:09.
- Options: a few words on `Step 13` or `Step 17` ("keep the base motor's wire clear"), or Lee's own alternative (note 18): leave the wire
  standing up until the module is in and put the slot step just before `Step 23`. Either way nobody gets stuck.

### F9. `Step 2`: nothing says which way round the motor ends up, and by the CAD report's numbers it fits both ways. ASK LEE

- Evidence: R1's cut-out is 22.75 mm long and the motor body 22.55 mm, the ears are symmetrical (z 119.37 and 151.57 about a body from
  124.19 to 146.74) and R2's notch crosses the body either way (`cad_codes_base.md` 3(a), 3(b); the reversed fit itself was not tested in
  the CAD). The shaft is 5.90 mm from one end and 16.65 mm from the other, so a motor turned the other way in beat 3 seats with its shaft
  10.75 mm off the turret's axis and its wire towards R5. `video_base_seg1.md` 5.9: "the shaft end is the end with the narrow notch (+Z)
  ... The lead leaves the case at that same end."
- The animation ends the right way round; a student who copies it is fine. A student who twists the other way finds out only when the
  turret sits off-centre on B2.
- Fix: an eye icon on R1's notch in `Step 2c`, or a clause such as "the wire end sits at the notched end of the slot".

### F10. `Step 19`: B7's engraving faces in (CAD, and so the guide) but out on the video. ASK LEE

- Evidence: `cad_codes_base.md`: NAUO7 engraved on -Z (towards the joystick). Controller.mov 1:59: "B7" on the outer face. B7 is symmetrical
  and fits both ways. If TechBox wants the code readable on the finished controller the CAD has to be turned; the guide follows the CAD.

### F11. `Step 10`: the horn has to line up with B1's cut-out to about 1 degree. ASK LEE

- Evidence: `cad_codes_base.md` 3(d): fits at 0.5 degrees, touches at 1.0, overlaps 0.3 mm at 2. Controller.mov 0:02 - 0:07 shows the turret
  20 - 30 degrees off square and being turned by hand; Base.mov 5:02 - 5:10 turns the pair over to check the horn sits in the cut-out.
  The caption ("... so the servo horn fits into the cut-out in B1") implies it; the two lines from the cut-out's ends are right
  ((146.2, 88.6, 140.9) and (181.2, 88.6, 140.9); cut-out x 144.81 - 182.45).
- Fix, if wanted: "turn R1 - R6 until the horn lines up", or an eye icon on the horn in a view from below.

### F12. Names on hover: two gaps against the Cadasio tooltips. SHOULD FIX (low)

- The Nano answers "Nano I/O Module" (names are per top-level instance, NAUO82); TechBox's project calls it "Nano", and `Step 24`'s
  caption talks about "the nano".
- The drawn wires have no hover name (the player only names CAD parts). In TechBox's project the motor's cable is "Base Motor" and the
  jumper wires are "Breadboard Wire (F-F)"; here only the plug and the sixteen caps answer.

## The three known differences from the video: are they safe?

| Difference | Safe? | Why |
|---|---|---|
| B8 (`Step 21`) before the I/O module (`Step 22`); the video does module 2:53 - 3:07, then B8 3:10 - 3:27 | Yes | B8 lies over x -27 .. 32.5 at y 134.2 and up; the module travels at x 43.4 - 96.7, so the two never overlap in plan. The wires leave the bays at x 32.5, y 124, 10 mm under B8. Nothing of B8 is in the module's way, and with B8 on the B6 walls are braced while the board is pushed through them. |
| Base motor's wire in R4's L-shaped slot (`Step 8`) | Yes | It is what Lee, the build notes and the CAD have (lead through the pocket with 1.3 mm to spare; mouth never covered). It also keeps R6's hook free for the Shoulder Motor's lead (row 9), which the CAD routes there. Two cautions: F7 and F8. Correction to the brief: the video's builder did not use R6's hook either. `video_controller_seg2.md` retracts that: the lead was worked round the tip of R6's ear at 3:38 - 3:44, had "come free" by 4:16 and ends over R4's top edge near the middle; "both slots empty in every frame". |
| I/O module parked on the right from `Step 17` (the video keeps it on the left until 2:45) | Yes, with care | See F5. |

## What the video shows that the guide leaves out

Needed by a student:

1. Free the wire before R6 (Base.mov 3:20 - 3:24). F2.
2. Press each B6 hooked end into its slot (Controller.mov 1:29, 1:37, 2:12). F6.
3. Keep the loose wire off the plate while the controller is built (four times on video). F8.
4. The ribbon that crosses the other bay has to end up on top (F5).
5. The motor's wire end goes to the notched end of R1's cut-out (F9); the horn has to be parallel to the plates before B1 (F11).

Worth a word, not needed:

6. R5 and R6 are pressed at several points for about 10 s each (four or five snap tabs at once); the guide's one push is right in direction.
7. The screws are driven with an Allen key and all six are gone round a second time (7:40 - 8:40). The rulebook draws no tools.
8. The kit's servo leads carry a numbered paper flag near the plug ("5" on this one). It is the student's check for `Step 23` and will
   matter more with four motors.
9. The lead goes into B2's keyhole with turret and plate both tilted in the hands; the guide's level slide is the clean equivalent.

## Step by step

"OK" = engraved code and CAD id, order, direction of the hover offset (`path[0]`) and caption all agree with the video, the CAD report,
Lee's notes and the old captions.

| Step | Part (id) | Hover `path[0]` | Video / CAD | Result |
|---|---|---|---|---|
| 1 | card | - | Base.mov 0:02 - 0:08 unplugs the lead flagged 5. Old caption with "I/O module" for "I/O extension module" | OK |
| 2 | R1 (NAUO10) shown; Base Motor + horn (NAUO45, 46) | [0, 58, 1.5], turned and tilted | See the table at the top. From R1's engraved side, horn first, as 0:18 - 0:22 | OK; F9 |
| 3 | R2 (NAUO11) | [0, 71.3, 0] | Straight down, 0:58 - 1:02; CAD needs 20.9 mm. Lines at the two slot mouths (135.1 and 192.7; CAD 134.99 and 192.74) | OK |
| 4 | R3 (NAUO12) | [0, 63, 0] | Straight down at +X, 1:48 - 1:55; CAD needs 24.75. Lines at Lee's point (193.6, 96.6, 121.5) and its twin | OK |
| 5 | R4 (NAUO13) | [0, 63, 0] | Straight down at -X, 2:12 - 2:16. Lines at Lee's point (133.6, 96.6, 121.2) and its twin | OK; F2 |
| 6 | R5 (NAUO15, CAD name R6) | [0, 0, -65] | Pushed +Z, 2:46 - 2:58; CAD: +Z. Four lines at R1's two tabs and the arms of R3 / R4 | OK |
| 7 | R6 (NAUO14, CAD name R5) | [0, 0, 65] | Pushed -Z, 3:25 - 3:36; CAD: -Z | OK; F2 |
| 8 | wire into R4's slot | no part moves | Not on video (never done there); Lee note 11, CAD 3.2 | OK; F7, F8 |
| 9 | B2 (NAUO2) | [0, 0, 80] | B2 moves -Z relative to the turret (CAD 3(c); video 4:14 - 4:17, R6 side leading). Caption is Lee's note 12 | OK; F4 |
| 10 | B1 (NAUO1) | [0, -65, 0] | Straight along Y, 4:59 - 5:01; from below as Lee's note 13 asks | OK; F11 |
| 11 | 6mm Hex Screw (NAUO47) | [0, 60, 0] | The video's first screw is the NAUO47 position. One line (209.2, 87.5 -> 93.5, 99.7) = CAD | OK |
| 12 | five screws (NAUO48 - 52) | [0, 60, 0] each | All five axes match the CAD table; label "5x 6mm Hex Screw" | OK |
| 13 | B3 (NAUO9, CAD name B10) | [0, 80, 0] | Straight down, Controller.mov 0:10 - 0:18 | OK |
| 14 | B4 (NAUO3) | [0, 67.3, 0] | Straight down, 0:19 - 0:23 | OK |
| 15 | Left Joystick (NAUO80) into B5 (NAUO4) | [0, 0, 40] | Joystick moves -Z into the wall from its plain side, 0:48 - 0:55. Wires cut at 42 mm with the break mark | OK |
| 16 | B6 (NAUO5) | [0, 0, 65] | B6 moves -Z onto the board's edge, 0:56 - 1:03 | OK |
| 17 | group onto the base; module appears aside | [0, 80, 0] | Straight down, 1:08 - 1:40 | OK; F5, F6 |
| 18 | Right Joystick (NAUO81) into B6 (NAUO6) | [0, 0, 40] | As step 15, 1:48 - 1:55 | OK |
| 19 | B7 (NAUO7, CAD name B8) | [0, 0, 65] | Moves -Z onto the free edge, 1:56 - 2:02 | OK; F10 |
| 20 | group onto the base | [0, 80, 0] | Straight down, 2:03 - 2:18 | OK; F5, F6 |
| 21 | B8 (NAUO8, CAD name B9) | [0, 65, 0] | Straight down, engraved face up, 3:10 - 3:27 (after the module on video) | OK |
| 22 | Nano I/O Module (NAUO82) | [0, 6, 70] | From +Z, plain end first, 2:53 - 2:57 | Side OK; path F3 |
| 23 | plug (NAUO83) to row 5 | from the slot pose | 4:14 - 4:19, straight down onto the row | Pins OK; path F1 |
| 24 | card | - | Old caption; cable not modelled (Review note) | OK |

Names: "Base Motor" on NAUO45, 46 and 83, "6mm Hex Screw", "Joystick", "Nano I/O Module" and "Breadboard Wire (F-F)" on the caps are
the Cadasio tooltips word for word; wood parts carry their engraved codes (all 15 checked against `cad_codes_base.md` section 1, including
B3 / B7 / B8 and the R5 / R6 swap). Gaps: F12.

## Wiring

| Check | Result | Evidence (route ends in `steps.json`) |
|---|---|---|
| Left joystick = NAUO80, on A2 / A3 | Right | "left GND" (27.46, 124.23, 123.34) -> (83.13, 115.97, 136.48) = A2 G; "left V" z 120.84 -> (85.62, .., 136.48) = A2 V; "left X" z 118.34 -> (88.10, .., 136.48) = A2 S; "left Y" z 115.84 -> (88.10, .., 133.94) = A3 S |
| Right joystick = NAUO81, on A0 / A1 | Right | "right GND" z 168.34 -> (83.13, .., 141.48) = A0 G; "right V" z 165.84 -> (85.62, .., 141.48) = A0 V; "right X" z 163.34 -> (88.10, .., 141.48) = A0 S; "right Y" z 160.84 -> (88.10, .., 138.94) = A1 S |
| Caps | Right | Left: NAUO104 - 107 on the joystick (from `Step 15`), NAUO99 - 102 on the module from `Step 17`. Right: NAUO103, 108 - 110 on the joystick (from `Step 18`), NAUO95 - 98 on the module from `Step 20` |
| Base lead colours | Right | "base brown" (162.62, 119.11, 146.76) -> (49.98, 120.97, 139.36) = G contact; "base red" 163.64 -> 52.52 = V; "base orange" 164.66 -> 55.06 = S. Same order on the loose lead (plug contacts at x 161.09 / 163.63 / 166.17 in `Step 2c`; 110.56 with z 137.68 / 140.15 / 142.62 in `Step 8c`) |
| Row 5 | Right | Plug seat z 139.36; row 5 is z 139.46 (row 4 136.92, row 6 142.00) |
| Label "5" | Right | Anchor (52.6, 107.9, 139.5): the foot of row 5's V pin (52.574, .., 139.46) on top of the header strip (y 107.97) |
| Caption | Right | "brown to G, red to V, and orange to S": G is the column at the board edge (x 50.09), S nearest the Nano (x 55.06) |

Jumper colours are yellow / green / blue / purple for GND / 5V / X / Y on both joysticks: the real colours for the left ribbon, placeholders
for the right one, as Lee accepted in note 21.

## Open points in the evidence itself

- `cad_pins.md` (section 5, "What the real leads do") says the base lead leaves the turret "through R4's L-shaped slot" in the final frame
  of Controller.mov; `video_controller_seg2.md` says the slot is empty at 3:47, 4:06 and 4:24 and the lead lies over R4's top edge near
  the middle. One of them misread the same frame. It does not change the guide (Lee and the CAD decide), but `cad_pins.md` should not be
  quoted as video evidence for the slot until it is re-checked.
- `video_controller_seg2.md` is marked IN PROGRESS and `video_base.md` DRAFT 1.
- Not confirmed from the documents: whether B4 fits its slot both ways round. Its end posts differ (z 108.05 - 115.67 and 173.45 - 179.80),
  and turned round the +Z post would stand where the board's USB end goes. The video's builder puts "B4" at the left end, facing the
  joysticks, which is how the guide draws it.

## Not checked

- Anything on screen: label and eye placement, whether row 5 is in view in `Step 23`, how the wire blends look. No browser in this review.
- Clearances that need the meshes (the 0.6 mm overlap stated for `Step 2`, the model's own stub colours on the motor).
- Noticed in passing: the kit's `README.txt` still describes the old 25-step guide (motor into R2 from below, wiring as text cards).
