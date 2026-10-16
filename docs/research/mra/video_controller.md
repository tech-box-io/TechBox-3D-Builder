# Controller.mov (4:26): merged report

Status: COMPLETE (13 Oct 2026). Merges `video_controller_seg1.md` (0:00 - 2:20, read on to 2:35) and
`video_controller_seg2.md` (2:05 - 4:26). The two segments overlap at 2:05 - 2:20 (the right joystick group being
pressed down, hands off, the module being picked up); those actions are listed once below. Every second of the video
is covered by one segment or the other. Times are the video's own (1080 x 1920, 265.6 s).

Directions: CAD assembly space, mm, Y up. Controller end = -X, turret = +X. The builder sits at the controller end, so
builder's left = -Z (B5, NAUO4, Z 105.1 - 108.1) and builder's right = +Z (B7, NAUO7, Z 173.6 - 176.6). The base is
picked up and turned several times after 2:47, so "left / right" always means the builder's.

Parts in this video: B1 NAUO1, B2 NAUO2, B3 NAUO9, B4 NAUO3, B5 NAUO4, B6 (left) NAUO5, B6 (right) NAUO6, B7 NAUO7,
B8 NAUO8; turret R1 NAUO10, R2 NAUO11, R3 NAUO12, R4 NAUO13, R5 (engraved) NAUO15, R6 (engraved) NAUO14; base servo
NAUO45 and its plug NAUO83; left joystick NAUO80, right joystick NAUO81; I/O module NAUO82; jumper caps NAUO95 - NAUO110;
ribbons NAUO111 (right joystick) and NAUO112 (left joystick).

### What I looked at again for the merge

The segments do not contradict each other anywhere. These points were marked unsure, or were described a little
differently by the two, so I went back to the frames (native 1080 x 1920, crops up to 13x):

| Point | Result |
| --- | --- |
| How the module is held at 2:20 - 2:44 (seg 1: "USB end toward the turret"; seg 2: "by its power-jack edge") | Same thing. Left hand holds the analogue edge, which has the power jack at its far corner; the mini-USB points at the turret (+X). Stills `t02m22s.jpg`, `t02m31s.jpg`. |
| Which row the servo plug is on (seg 2: "row 5, fairly sure") | Re-measured on the native 4:24 frame with my own overlay (`video_controller_row5_check.jpg`): **row 5**. Details in section 2, action 32. |
| Which of the G and V rows the black, brown, yellow and green jumpers are in (seg 1: not read) | At 3:47 and 4:24 the three plugs on A2 stand in the order blue (board edge, S), green (middle, V), yellow (next to the Nano, G), with purple beside blue on the S row. At 4:24 a black wire goes to the row next to the Nano at the capacitor end. So GND is on G and +5V on V, as Lee's list says. Fairly sure (plug tops lean, so this is the order of the tops, not of the pins). Still `c_t03m47s_analogue_plugs.jpg`. |
| B7's engraving (video: outward; CAD: inward) | Confirmed outward. At 2:01 the group is tipped so B7 lies on top of the joystick and "B7" is on the upper face, the one away from the joystick; the code also shows on the fitted wall at 2:51, when the base is tilted toward its right-hand side (`c_t02m51s_B7_engraving_outward.jpg`). |
| Whether B4's end post beside the USB is on the real part (seg 2: "fairly sure") | Yes. A burnt wood end stands just beyond the board edge beside the mini-USB socket at 3:47 (`c_t03m47s_usb_end_B4_post.jpg`). |
| Direction and order of the module slide | Confirmed from 1 s native frames 2:45 - 3:08: carried over the base to the builder's right, slid toward the builder's left (-Z), USB and jack to the right. |
| B8, the lead under R6's lug, the plugging-in | Confirmed from 1 s and 2 s frames 3:08 - 4:24. |

I did not load the CAD. CAD numbers below are the ones the segment reports measured from `mra.glb`, checked against the
bounding boxes in `mra_instances.json`.

## Short answers to the questions asked

- **Where the I/O module lies while the joysticks are fitted.** Flat on the worktop OUTSIDE the base, on the builder's
  LEFT (-Z side), component side up, 10 - 80 mm from the plate edge and about level with B4 and the gap between B4 and
  the turret, hanging on its two ribbons. Its mini-USB end points away from the builder (toward +X), a quarter turn
  from how it finally sits. It is there from 0:29 to 2:19 and is dragged a little each time a ribbon is pulled.
- **How and when it goes in.** 2:45 - 3:07, AFTER both joystick groups are on the base and BEFORE B8. The right hand
  carries it over the base to the builder's RIGHT and turns it a quarter turn clockwise (seen from above) to its final
  orientation: USB and power jack to the right (+Z), analogue header with the eight jumper plugs toward the turret
  (+X), digital header toward the joysticks (-X). It is then slid sideways toward the left (-Z), plain end first, in
  the pair of facing slots in the long arm of each B6 (first NAUO6, then NAUO5), passing above B4. A last push and a
  press down on the power-jack / USB end at 3:05 - 3:07 seats it.
- **Servo leads plugged in during this video: one.** The base servo's lead (white paper flag, "5") is pushed onto the
  digital row printed "5" at 4:14 - 4:19: orange toward the Nano (S), red in the middle (V), brown at the board edge
  (G). The other three servos lie loose at the back-left of the worktop the whole time; no flag can be seen on their
  leads in this video.
- **The lead is never put into R4's L-shaped slot**, and not into the hook slot of R6's lug either.
- **USB side.** Once fitted, the Nano's mini-USB and the module's power jack are at the builder's right (+Z).
- No screws, no servo horn, no centring or motion test, no power cable anywhere in the video.
- **Order on video:** B3, B4, left joystick into B5, B6, seat; right joystick into B6, B7, seat; module; B8; base lead
  to row 5. `guide.py` has B8 before the module; otherwise the same.
- The stage-by-stage table of where the module, the ribbons and the servo lead are is Appendix A; every legend read
  off the boards, and which jumper is on which pin, is Appendix B.

## 1. What is already built or laid out at 0:00

Still `stills/controller/t00m00s.jpg`.

- **B1 + B2 (NAUO1 + NAUO2) screwed together**: six screw heads visible, four corners and two mid-edge (NAUO47 -
  NAUO52). "B2" engraving up, at the controller end, builder's near-left corner (CAD: X -14.9 to -5.4, Z 96.8 - 103.2).
- **Turret R1 - R6 with the base servo inside** (NAUO10 - NAUO15, NAUO45), on the plate at the far end, turned about
  20 - 30 degrees off square on its servo. Read during the video: "R4" on the outer face of the low wall facing the
  controller (NAUO13), "R5" on the outer face of the side plate on the builder's left (NAUO15), "R6" on the side plate
  on the builder's right (NAUO14), "R1" on the turret floor, "R2" on the partition.
- **Base servo lead** (brown / red / orange, black 3-way socket, white paper flag printed "5" about 25 mm from the
  socket) comes up out of the turret and lies across the plate, unplugged.
- **Controller area of B2 empty**: the row of slots for B3, the long cross slot for B4, the two small slots near the
  turret for the hooked ends of the B6 arms, and the wall-tab slots are all open.
- **Loose, right of the plate:** B4, B3, B5 and the two B6 (all four codes read in the first ten seconds). B7 is out
  of frame to the right until 1:56. Further back, B8 (two round holes, eight small slots, one centre slot, engraved
  "B8" plus four words with arrows; read later, see Appendix B).
- **Loose, back-left:** two small rectangular frames with two holes each (one reads "R8"; so R7 and R8, NAUO16 /
  NAUO17), three servos with their leads (not touched in this video), and **the two joysticks lying side by side,
  already wired to the I/O module by two 4-way ribbon jumpers** (one black / brown / red / orange, one yellow / green /
  blue / purple). Nothing else is plugged into the module.

## 2. Timeline

One list for the whole video. "Sure" means the code or detail was read directly in a frame. Actions 16 - 18 are the
overlap of the two segments.

1. **0:02 - 0:07 Turret squared up.** Left hand steadies the plate, right hand takes the turret by its walls and turns
   it until it is square to the plate (the base servo is back-driven by hand, about 20 - 30 degrees). No part added.
   Fairly sure it is the turret that turns: the angle between its walls and the plate edge changes.
2. **0:07 - 0:10 Base servo lead moved aside, first time.** Left hand lays the lead off the LEFT edge (-Z); plug and
   flag "5" end up on the worktop left of the plate. The lead leaves the turret over the top edge of R4, right of
   centre; it is not in any slot.
3. **0:10 - 0:18 B3 fitted (NAUO9).** Picked up from the right; "B3" read at 0:11 - 0:13, sure (`t00m12s.jpg`). A long
   strip with a tall three-pronged centre, two low sections and an upright at each end. Held prongs up and lowered
   straight down (-Y) into the row of slots across B2 nearest the controller end (X 1.2 - 4.2), then pressed down at
   both ends with a finger of each hand (0:16 - 0:18). Engraved face toward the builder (-X), as in the CAD (engraving
   on the -X face at Z 135.9 - 145.5). B3 reaches Y 87.1 in the CAD, so its feet go through B2 into B1. No fastener.
4. **0:19 - 0:23 B4 fitted (NAUO3).** Picked up from the right; "B4" read at 0:20 - 0:21, sure. A low strip about
   75 mm long with notches in its top edge and a short post at each end. Held notches up, "B4" at the builder's left
   end and facing the builder, pressed straight down (-Y) into the long cross slot in B2 (X 68.5 - 71.5), one hand at
   each end. CAD has the engraving on the same face (-X, Z 117.3 - 126.9). Stands about 16 mm above B2. Still after
   both: `t00m24s.jpg`.
5. **0:25 - 0:33 Joysticks and module brought in.** Right hand nudges the pile of B5 / B6 / B7 further right (0:25);
   both hands lift the joystick-and-module bundle from the back-left, carry it across in front of the turret and put
   it down on the worktop to the LEFT of the plate (0:27 - 0:29). The joysticks are separated and laid out, module
   flat, components up (0:30 - 0:33). Nothing is plugged or unplugged. Still `t00m32s.jpg`.
6. **0:34 - 0:44 Module shown to the camera.** Left hand holds the module, right hand holds the ribbons up so the
   plugs can be seen. No change to the wiring. Most of the legends in Appendix B were read here (`t00m39s.jpg`).
7. **0:45 - 0:47 Parts parked.** Module put down flat left of the plate, about level with B4, USB end pointing away
   from the builder. The joystick on the black..orange ribbon (the right joystick, NAUO81) is parked on the worktop at
   the far left, beside the turret corner of the plate. The joystick on the yellow..purple ribbon (the left joystick,
   NAUO80) stays in the left hand.
8. **0:48 - 0:55 Left joystick into B5 (NAUO80 into NAUO4), in the hand.** B5 picked up from the right; "B5" read at
   0:50 - 0:55, sure. B5 is held upright in the left hand (tabs down), engraved face toward the builder, long low arm
   to the builder's left. The joystick is brought up BEHIND it (the face away from the engraving), board level, thumb
   cap up, header pins pointing along B5's arm, and pushed through so that the side edge of its board goes through the
   two short horizontal slots in B5's two uprights and its body sits in the U-shaped cut-out between them. In
   assembly axes: the joystick moves along -Z into the wall, square to the wall face, not down from above. The board
   edge ends just proud of the engraved face (CAD: board edge Z 105.0, B5's outer face Z 105.1). Still `t00m52s.jpg`.
9. **0:56 - 1:03 First B6 onto the joystick's other edge (NAUO5).** "B6" read at 0:57, sure (`t00m57s.jpg`). Same tall
   block as B5 but with a longer arm that ends in an upright post with a hook-shaped relief cut. Brought to the free
   side edge of the joystick board, arm parallel to B5's arm, and pressed on toward the builder (B6 moves along -Z
   onto the board edge) with thumb and two fingers along its top. The joystick is now held by its two side edges
   between B5 and B6.
10. **1:04 - 1:06 Left group carried to the base.** The module stays flat on the worktop left of the plate and is
    dragged a little by the ribbon.
11. **1:07 Base servo lead moved aside, second time.** Right hand flicks the lead from the left of the plate over to
    the RIGHT (+Z). From here until 3:38 it leaves the turret over the corner where R4 meets R6, and the plug and
    flag "5" lie on the worktop right of the plate.
12. **1:08 - 1:40 Left group seated on the base (NAUO4 + NAUO80 + NAUO5).** Lowered onto the left half of B2, arms
    toward the turret, joystick end first: the slot in the bottom edge of each wall drops over B3 (X 1.2 - 4.2) and
    the two arms drop over B4 where its top edge is notched. Pressed down (-Y) with both hands at the joystick end, in
    several goes (1:10 - 1:28). At 1:29 - 1:30 and again 1:37 - 1:40 the right hand presses the hooked post at the far
    end of B6's arm down into its small slot in B2 just short of the turret (X 94.9 - 107.6, Z 128.6 - 131.6) while the
    left index finger holds the joystick end down. At 1:35 the joystick itself is pressed down. Result
    (`t01m24s.jpg`): B5 on the outer left edge with its arm ending just past B4 (X 83.3); B6 inboard with its arm
    running on to the post near the turret; joystick header toward the turret. No fastener.
13. **1:41 - 1:46 Base lifted and put back.** Left hand lifts the yellow..purple ribbon clear, right hand takes the
    plate by its right edge near the turret, lifts and turns it a few degrees and sets it down. Guess: checking that
    the tabs are home. Nothing added.
14. **1:48 - 1:55 Right joystick into the second B6 (NAUO81 into NAUO6), in the hand.** Second B6 picked up from the
    right; "B6" read at 1:49 - 1:53, sure. Right hand fetches the parked joystick on the black..orange ribbon from the
    far left (1:50). B6 is held upright in the left hand, engraved face toward the builder, arm to the builder's left;
    the joystick is pushed in from BEHIND exactly as in action 8 (joystick moves along -Z into the wall; cap up;
    header toward the arm). Still `t01m51s.jpg`. The black..orange ribbon now crosses over the yellow..purple one and
    pulls the module round on the worktop.
15. **1:56 - 2:02 B7 onto the joystick's other edge (NAUO7).** "B7" read at 1:56 - 2:02, sure. The tall block only
    (two uprights and the U cut-out), no arm. Pressed onto the free side edge of the joystick board (B7 moves along
    -Z) with its ENGRAVED face outward, away from the joystick (`t01m59s.jpg`, taken at 1:59.5). At 2:01 - 2:02 the
    group is tipped over in the hands so B7 is uppermost and B6 and B7 are squeezed together.
16. **2:03 - 2:18 Right group seated on the base (NAUO6 + NAUO81 + NAUO7).** Carried to the right half of B2; the
    ribbon arches up from the module and over the left walls. The plate is slid a little on the worktop at 2:06 -
    2:07. The group is lowered joystick end first over B3 and B4 and pressed straight down (-Y) with both hands
    (2:07 - 2:18); at 2:12 - 2:13 the right hand presses the hooked post of this B6 into the second small slot near
    the turret (X 94.9 - 107.6, Z 150.0 - 153.0). B7 stands on the outer right edge, at the joystick end only.
17. **2:19 Hands off** (`t02m19s.jpg`). Across the controller end, left to right: B5 | left joystick | B6 | open
    centre bay | B6 | right joystick | B7.
18. **2:20 - 2:44 Module picked up and shown.** Nothing is assembled. The left hand lifts the module off the worktop by
    its analogue edge (power jack at the far corner) and holds it, tilted, just left of the plate above the gap
    between B4 and the turret for about 22 s: mini-USB toward the turret (+X), digital edge toward the plate. Stills
    `t02m22s.jpg`, `t02m31s.jpg`.
19. **2:45 - 2:46 Module carried to the right and turned.** The right hand takes the module, carries it OVER the base
    to the builder's right and turns it flat, component side up, a quarter turn clockwise seen from above: USB socket
    and power jack to the right (+Z), analogue header with the eight jumper plugs toward the turret (+X), digital
    header toward the joysticks (-X). This is how NAUO82 sits in the CAD. The two ribbons now stand up from the
    joystick headers and arch to the right. Still `t02m46s.jpg` (also the clearest view of B4, the two B6 arms and
    their hooked ends before the module covers them).
20. **2:47 - 2:51 Base lifted.** The left hand lifts the whole base off the worktop (held under the controller end,
    tilted to the camera). The right hand holds the module level beside the right-hand edge of the base, in line with
    the gap between B4 and the turret.
21. **2:52 - 2:57 Module slid in (NAUO82).** Slid SIDEWAYS toward the builder's left (-Z), plain end (the end away
    from the USB) leading. At 2:52 the plain end is entering the right-hand B6 arm (NAUO6) and the USB end overhangs
    the plate edge by 20 mm or more (`t02m52s.jpg`); at 2:56 the plain end has reached the left-hand B6 arm (NAUO5)
    and the USB end is inside the plate edge (`t02m56s.jpg`). Right index finger on top of the power jack, thumb under
    the corner beside the USB socket: the pushing, and any lifting, is done at the USB end. The board passes above
    B4. Each B6 arm grips the two long edges of the board (analogue edge and digital edge) in a pair of facing slots.
    Travel about 72 mm (plain end from outside the plate, Z > 188.3, to Z 115.96). The base servo lead lies on the
    plate in the gap between the module and R4 while this is done.
22. **2:58 - 3:04 Base turned in the hands** so the camera sees it from the builder's left and from behind the turret.
    Module in, level; both hooked arm ends stand up just beyond its turret-side edge. "B2", "B5", "R4", "R5" read.
23. **3:05 - 3:07 Final push and press.** Base back on the worktop. Right index finger on the power jack, thumb on
    the corner beside the USB: the module is pushed the last few mm to the left and pressed DOWN at that end
    (`t03m05s.jpg`). Guess: this is the USB end dropping behind B4's right-hand end post (section 5, item 1).
24. **3:08 - 3:09 Lead lifted clear.** The right hand lifts the base servo lead off to the right, flag "5" up.
25. **3:10 - 3:12 B8 lowered (NAUO8).** Picked up from the far right of the worktop ("B8" read in the hand and after
    fitting) and lowered flat, straight down (-Y), engraved face UP, over the two thumb caps (`t03m11s.jpg`). "B8" is
    in the middle of the turret-side edge and reads the right way up from the builder's seat.
26. **3:12 - 3:27 B8 pressed down.** Pressed in stages with the fingers of both hands, working round the plate, for
    about 15 s. The tabs on the tops of B5, B6, B6 and B7 come up through the eight small slots (two rows of four,
    one row each side of the thumb caps) and the centre prong of B3 comes up through the cross-wise slot between the
    two round holes. Hands off at 3:27: seated, level, thumb caps standing through the round holes (`t03m27s.jpg`).
    No screws.
27. **3:28 - 3:37 Base picked up; finger on the module.** The left hand picks the whole base up (it stays in the left
    hand until 4:21). Right index finger on the jack / reset button, thumb at the corner beside the USB, held about
    8 s. Guess: checking that the board is home, or pointing while talking; nothing visibly moves.
28. **3:38 - 3:45 Lead tucked under R6's lug.** Right index finger and thumb take the lead where it leaves the turret
    (over R4's top edge, in the corner against R6) and tuck it down and outward UNDER the front lug of R6 (the tab of
    NAUO14 that sticks out toward the controller above R4's height). At 3:45, seen from outside R6 (`t03m45s.jpg`),
    the lug's hook slot is empty and the lead comes out from under the lug toward the controller. This does not last
    (action 32).
29. **3:46 - 3:51 Plug end shown.** Right hand holds the plug up to the camera (`t03m47s.jpg`): black 3-way socket,
    brown / red / orange, white flag "5". The clearest view of the module in place, its legends, the jumper plugs,
    B4's end post beside the USB, and R4's L-shaped slot, which is empty.
30. **3:52 - 4:09 Nothing assembled.** The lead is let go; it loops up and over to the right and its plug rests beside
    the module's USB end. At 4:09 the base is tilted to show the turret from the controller side (`t04m09s.jpg`):
    "R1", "R2", "R5" read; the lead still passes under R6's lug; hook slot and L-slot both empty.
31. **4:10 - 4:13 Lead picked up.** Right hand takes the lead just behind the flag and brings the plug over the
    module from the right, under the right joystick's ribbon.
32. **4:14 - 4:19 Base servo plug onto row 5 (NAUO83).** Pushed straight down (-Y, about 6 mm onto 5.8 mm pins) onto
    one 3-pin row of the digital block printed "7 6 5 4" and pressed home with the index finger at 4:16 - 4:18
    (`t04m17s.jpg`). Orange nearest the Nano (S), red in the middle (V), brown at the board edge (G). From 4:16 the
    lead is no longer under R6's lug: pulling the plug across has drawn it out, and it now crosses R4's top edge
    further along, toward the middle.
    **Which row.** Certain: the block is "7 6 5 4"; row 4 is empty (three pins seen) and row 7 is empty (its V and G
    pins seen), so the plug is on 5 or 6. Seg 2 placed it on row 5 from an overlay of predicted pin positions
    (`video_controller_seg2_row5_overlay.jpg`), and `cad_pins.md` reached row 5 independently. My own check on the
    native 4:24 frame (`video_controller_row5_check.jpg`): I took the block outline and row pitch from the uncovered
    "3 2 1 0" block (pitch 7.9, -5.7 px per row; pins lean 0.7 px per mm straight up the frame) and drew a 14 mm plug on
    row 5 and on row 6. The row-5 box ends where the black plug ends in the frame (its right-hand edge within about
    1 px) and leaves row 7's V and G pins and part of row 6's G end showing, as they do; the row-6 box would cover
    about 7 px of yellow header that is plainly visible. So **row 5**, fairly sure; it also agrees with the flag, with
    Lee and with the CAD (NAUO83 at Z 138.0 - 140.7; row 5 pins at Z 139.46, G X 50.085, V X 52.574, S X 55.064). Not
    certain, because no frame shows the foot of the plug.
33. **4:20 - 4:22 Loop tidied, base put down.** Right hand tidies the loop of lead (flag "5" facing the camera at
    4:20) and the base goes back on the worktop.
34. **4:23 - 4:25 Hands off.** End state (`t04m24s.jpg`, `c_t04m24s_module_end_state.jpg`).

## 3. State at the end (4:25)

- Base flat on the worktop. On it: turret R1 - R6 with the base servo; B3 and B4; B5 | left joystick | B6 | B6 |
  right joystick | B7 (NAUO4 | NAUO80 | NAUO5 | NAUO6 | NAUO81 | NAUO7); B8 on top with both thumb caps through its
  round holes; the I/O module in the slots of the two B6 arms, over B4, USB and power jack to the builder's right.
- Left joystick ribbon (yellow GND, green +5V, blue VRx, purple VRy): from the header (pins pointing at the turret)
  out of the bay under B8, in a wide loop out past the plain end of the module on the builder's LEFT, up and back down
  onto the analogue header at A2 / A3.
- Right joystick ribbon (black GND, brown +5V, red VRx, orange VRy): from its header up and diagonally across the
  top of the Nano, down onto the analogue header at the capacitor end (A0 / A1). It crosses above the other ribbon's
  plugs and above the servo plug.
- Base servo lead: leaves the servo on its +Z side, rises, crosses R4's top edge (Y 146.6) at about Z 147 (plus or
  minus 3; guess from the image scale), which is directly above the pocket of the L-slot but over the edge, not in
  the slot; drops in front of R4 past the "R4" engraving, passes under both ribbons, makes a free loop about 60 mm
  across out past the builder's-right edge of the plate, and comes back to its plug on row 5. Flag "5" lies on the
  "11 10 9 8" block.
- Nothing is tucked or tied: all three cables arch in free air above the module.
- Not done by the end of this video: the lead in R4's L-slot; the power cable; any other servo lead; R7 and R8.

## 4. Proposed guide steps for this section

House style from `docs/cadasio-patterns.md`: one part or one hand action per numbered step; `Step N` shows the part
hovering back along its real path with red lead lines, `Step Nc` shows it in place; bench sub-assemblies on their own;
one wire per step with an eye icon and a destination label. Captions are TechBox's wording as it stands in
`guide.py`. Numbers continue the full build: the controller starts at Step 13 in the present `steps.json`.

The list follows the VIDEO's order, which differs from the present guide in one place (module before B8; see the note
after the table). Hover distances are the rulebook defaults, to be set by `stepgen.py` as usual.

| Step | Draft caption | Moves (CAD ids) | Already there / appears | Motion and cues |
| --- | --- | --- | --- | --- |
| 13 / 13c | Insert B3 into B2. | B3 NAUO9 | B1 + B2 with turret | Hover about 80 mm above, straight down (-Y) into the row of slots at X 1.2 - 4.2. Engraved face toward the controller end (-X), prongs up. Feet go through B2 into B1 (to Y 87.1). Lead lines: 2 or 4, foot tips to slots. As now. |
| 14 / 14c | Insert B4 into B2. | B4 NAUO3 | | Straight down (-Y) into the cross slot at X 68.5 - 71.5. Notches up, "B4" at the builder's left end facing the controller end. Lead lines: 2, foot tips to slot. As now. |
| 15 / 15c | Place the left joystick (the joystick connected to A3) into B5... | Left joystick NAUO80 with its four caps NAUO104 - NAUO107 and its wires, shown cut short | B5 NAUO4 appears in place (it is the part held still). Bench view: everything else hidden | Joystick travels along -Z, square to B5's face, from the un-engraved (+Z) side: board edge through the two slots in B5's uprights, body in the U cut-out. Cap up, header pointing along B5's arm (+X). Not from above. Lead lines: 2, the two corners of the board edge to the two slots. As now (`staged=True`). |
| 16 / 16c | ...and B6. | B6 NAUO5 | B5 + joystick | B6 travels along -Z onto the joystick's free board edge, arm parallel to B5's arm. Lead lines: 2, slots to the board-edge corners. As now. |
| 17 / 17c | Then place B5 and B6 onto B3. | Sub-assembly NAUO4 + NAUO80 + NAUO5 as one | Back to the whole model. I/O module NAUO82 appears lying beside the base with the left joystick's wires whole (module caps NAUO99 - NAUO102) | Straight down (-Y): bottom-edge slots over B3, arms over the notches in B4, the hooked post of B6 into its slot in B2 at X 94.9 - 107.6, Z 128.6 - 131.6. Lead lines: 4 (the two wall slots over B3, the hooked post to its slot, B5's arm to B4). **Step 17c could carry an eye icon on the hooked post**: on video it needs its own firm press, twice. |
| 18 / 18c | Place the right joystick into B6... | Right joystick NAUO81 with caps NAUO103, NAUO108 - NAUO110, wires cut short | B6 NAUO6 appears in place. Bench view | As Step 15: joystick along -Z into B6 from its +Z side. |
| 19 / 19c | ...and B7. | B7 NAUO7 | B6 + joystick | B7 along -Z onto the free board edge. On video its engraving faces OUT (+Z); the CAD has it facing in. |
| 20 / 20c | Then place B6 and B7 onto B3. | Sub-assembly NAUO6 + NAUO81 + NAUO7 as one | Right joystick's wires whole, module caps NAUO95 - NAUO98 appear | Straight down (-Y), as Step 17; hooked post into the slot at Z 150.0 - 153.0. Same optional eye icon on 20c. |
| (card) | Nano I/O Module | | | Optional, un-numbered. The rulebook gives a section card to any module whose pins appear on labels; row "5" does in Step 23. Module alone, close up, the "7 6 5 4" block marked. Not in the present guide. |
| 21 / 21c (now 22) | Slide the I/O module through the slots in B6 on top of B4. | I/O module NAUO82 with all eight module-side caps NAUO95 - NAUO102; both ribbons follow | | Hover beside the builder's-right edge of the base in its final orientation (USB and power jack to +Z), about 72 mm out so the plain end is clear of the plate (Z > 188.3). Travel along -Z in the facing slots of the two B6 arms (X 43.0 - 45.2 and X 94.7 - 97.0, Y 104.8 - 106.3), over B4, until the plain end meets B4's left end post (Z 115.96). Second motion: press the USB end down so it drops behind B4's right end post. Lead lines: 4, the plain-end corners of the board to the slot mouths in NAUO6, or 2 per arm. Eye icon on 21c at the USB end / B4 post. **Breaks rule 11** (a wired part is slid); see the note below. Keep the yellow Review note: the CAD has no collision-free path. |
| 22 / 22c (now 21) | Attach B8 on top of B5 - B7. | B8 NAUO8 | | Hover about 65 mm above, straight down (-Y), engraved face up, "B8" at the turret-side edge, over the two thumb caps. The eight wall tabs come through the eight slots and B3's centre prong through the centre slot. Lead lines: 4, the corner wall tabs (B5 and B7) to their slots. A snap fit (B3's barb): 22c could carry an eye icon on the centre prong. |
| 23 / 23c | Reconnect the base motor to 5. Remember brown to G, red to V, and orange to S. | Base servo plug NAUO83 and the three conductors of the lead | | Wire step: eye icon on the loose plug, label `5` on row 5 (anchor 52.6, 107.9, 139.5, as now). 23 shows the lead loose, 23c shows it routed and plugged; the plug goes straight down about 6 mm onto the pins. Orange toward the Nano. As now. |
| 24 | Connect the power cable to the nano. | | | Not in this video. Not modelled. As now. |

Notes on the proposal:

1. **Order of B8 and the module.** Video: module (2:45 - 3:07), then B8 (3:10 - 3:27). `guide.py` and the build notes:
   B8, then module. Either works in the CAD (B8 covers X -27.2 to 32.5; the module starts at X 43.4). With B8 on
   first the ribbons come out of two 20.6 mm wide bays and are harder to steer, and the rulebook's own order is
   electronics before the panel that covers them. I have listed the video's order; swapping steps 21 and 22 back is a
   one-line change. Lee to decide.
2. **Rule 11 (anything with wires attached is never slid into place).** The module has eight wires on it when it goes
   in. To keep the rule: one step with an eye icon on the module lying beside the base (pick it up), then the module
   shown in place, both ribbons swapped to their routed shape, no slide. To keep TechBox's caption ("Slide...") and
   show what the student has to know, namely that the board only goes in sideways from the USB side, the slide has to
   be animated and the ribbons cross-faded between two shapes. The present guide animates it. I would break the rule
   here for that reason, and say so in the step's Review note.
3. **The slide's path.** The present hand-set path (start 70 to +Z and 6 up, slide, drop 6) lifts the whole board,
   which the slots do not allow: beyond the slots each B6 arm rises to Y 109.4 on the joystick side and Y 118.5 at the
   hooked end. What the video shows is the USB end held between finger and thumb (thumb underneath) and pressed down
   at the end. Closer to that: slide along -Z with the board tilted a few degrees about X (USB end up, pivot at the
   NAUO6 slot; the CAD needs 3.1 mm of lift 20.5 mm behind the slot to clear the post, about 8.6 degrees), then level
   it. In the rigid CAD the board (1.65 thick) will still clip the 1.53 high slots, so this stays a reviewed step.
4. **Where the module lies beforehand.** `guide.py` parks it beside the builder's RIGHT edge (`MODULE_ASIDE`
   [10, -16.3, 100]) in its final orientation. On video it lies on the builder's LEFT, a quarter turn round, and is
   carried over the base before it goes in. Parking it on the right is simpler and honest enough (that is where it
   has to be to go in; the ribbons reach either side); I would keep it and not add a "carry it over" step.
5. **The joysticks never appear on their own.** From the first joystick step the module and eight wires are part of
   the picture. The present guide shows the wires cut short in the bench views and whole once a group is on the base,
   as Lee asked. The rulebook's habit for a pre-wired assembly is a numbered "pick it up" step with an eye icon; a
   Step before 15 showing both joysticks, the two ribbons and the module on their own would do that, but there is no
   TechBox caption for it, so it is not in the table.
6. **Not steps:** squaring the turret by hand (action 1), moving the lead out of the way (2, 11, 24), lifting and
   turning the base (13, 22), showing parts to the camera (6, 18, 29), tucking the lead under R6's lug (28).

## 5. Uncertain, contradictory, or where the CAD may not match

1. **The module's slide against B4's end post.** CAD: each B6 arm (NAUO5 at Z 128.6 - 131.6, NAUO6 at Z 150.0 -
   153.0) has two facing slots 1.53 high (Y 104.78 - 106.31), at X 43.04 - 45.20 and X 94.73 - 97.02. The board (X
   43.36 - 96.70, Y 104.78 - 106.43, Z 115.96 - 173.16) rides in them like a drawer, so its only free direction is
   along Z. B4 (X 68.5 - 71.5) runs under the board at Y 102.11 and has a post at each end: at -Z, Z 108.05 - 115.67
   up to Y 109.41 (the stop the plain end meets, 0.29 from the board); at +Z, Z 173.45 - 179.80 up to Y 107.89, which
   is 0.29 beyond the board's USB edge and 1.46 above the board's top face. So in the CAD a level slide from +Z is
   blocked by that post, as `guide.py` notes. On video the board does go in from +Z and is then pressed down at the
   jack end. The post is on the real part (seen at 3:47). Guess: the USB end is carried a few mm high over the post
   and drops behind it once the edge has passed; real laser-cut slots are looser than the CAD's. The video does not
   show the board's edge against the post, so how it clears is not seen directly.
2. **Order differs from `guide.py`** (module before B8 on video). See note 1 in section 4.
3. **B7's engraving faces out on video, in in the CAD.** CAD: NAUO7 is engraved on its -Z face (toward the right
   joystick; `cad_codes_base.md`). Video: "B7" is on the outer (+Z) face. B7 is symmetrical, so it fits either way.
   B3, B4, B5 and both B6 match the CAD (B5 and B6 have the long arm on one end and only go one way).
4. **B8 can go on more than one way.** From the slot coordinates seg 2 measured (tab slots at X -24.0 to -17.7 and
   23.0 to 29.3; Z 105.05, 128.63, 150.05, 173.63; centre slot Z 136.9 - 144.7), the slots are symmetrical about the
   middle of the plate in both directions, so B8 would also fit turned half a turn or face down. That is an inference
   from the numbers, not something tried. On video "B8" is at the turret side and the words read from the builder's
   seat. The CAD's B8 has only "B8"; the four words and arrows are missing, and they are what tells a student which
   way round it goes and which stick does what.
5. **B8 is a snap fit.** CAD: B3's centre prong is 7.94 wide at B8's level and has a barb reaching Z 145.89 just above
   B8's top face (Y 137.23); B8's centre slot is Z 136.87 - 144.68, so B8 has to be pushed past the barb (1.2 mm of
   interference in a rigid test) and then cannot lift off. That is why the builder presses for 15 s. B6's tabs stand
   6 mm proud of B8 (Y 143.2), B5's and B7's 3 mm (Y 140.2).
6. **Seating a joystick group is not one clean drop.** It goes down joystick end first over B3, the arms are levelled
   onto B4, and the hooked post at the far end of each B6 needs its own press into the slot near the turret. B3 and
   both ends of B6 reach Y 87.1, below B2, so these are snap fits through B2 into B1. A straight -Y move is a fair
   simplification.
7. **The base servo lead and the slots.** The build notes' "move the servo wire into the L-shaped slot in R4" is not
   done in this video or in Base.mov (`video_base.md`). The present guide does it at Step 8, before B2, and leaves the
   lead sticking out horizontally toward the controller while the controller is built. On video the lead is loose
   throughout: off the left edge (0:08), off the right edge (1:07), under R6's lug (3:38, not a CAD route; the lug's
   hook slot stays empty), and at the end over R4's top edge at about Z 147, above the L-slot's pocket (CAD: stem
   Z 140.6 - 142.7, pocket Z 140.6 - 148.7, Y 127.3 - 135.8). If the guide keeps the L-slot it has to come from the
   notes or a later video (`stills/pins/Claw_mov_t07m00s_leads_through_R4_R5_R6.jpg` is the place to look).
8. **Row 5 is "fairly sure", not certain.** Three independent readings of the 4:24 frame agree (seg 2, `cad_pins.md`,
   mine), plus the flag and Lee's statement, but the foot of the plug is hidden in every frame. The 4:21 frames are
   motion-blurred and cannot be used.
9. **G and V rows of the black, brown, yellow and green jumpers.** Yellow on the inner row and green in the middle at
   A2 are seen at 3:47 and 4:24 (fairly sure); black on the inner row at A0 is seen at 4:24 (fairly sure); brown is
   inferred. No frame shows the plugs' feet. The four S-row wires are sure.
10. **Jumper colours.** `guide.py` draws both joysticks' wires yellow / green / blue / purple by pin. On video only
    the left ribbon has those colours; the right one is black / brown / red / orange. Lee has said the colours only
    need to differ and need not be true, so this is noted, not a fault.
11. **Cables have no fixed shape.** The CAD has every wire in one final arc (NAUO111, NAUO112 and the lead). On video
    the left ribbon loops out to the left of the module, the right ribbon crosses over the Nano, and the servo lead
    makes a loop off the right-hand edge; all three change each time the base is handled. Only the end points are
    fixed.
12. **Plugging the lead in is done with the base in the hand**, tilted, B8 on and both ribbons in the way; the plug
    is fed in under the right joystick's ribbon. A guide would show it from above with the ribbons out of the way.
    Which way round the plug goes cannot be seen in the geometry (the socket is symmetric), so the caption has to
    say it, as it does.
13. **Turret turned by hand at 0:02 - 0:07.** Back-driving the base servo is housekeeping before the build, not
    something the guide should teach.
14. **The thin J-shaped cuts** near the hooked end of each B6 arm (X 101.3 - 104.2, Y 97.5 - 112.2) and in R4 are
    spring cuts for the snap tabs, about 1 mm wide. No wire goes through them.
15. **Other servos.** Three loose servos are in frame throughout and are not touched. No flags can be read on their
    leads here; `cad_pins.md` has the flag "6" from Arm.mov.
16. **Guesses kept from the segments:** ribbon length about 20 cm; where exactly the lead crosses R4 at the end
    (Z 147 plus or minus 3); what the builder is doing at 1:41 - 1:46 and 3:28 - 3:37 (checking the fit, or pointing
    while talking; the video was studied without sound).

## 6. Reference stills

All under `docs/research/mra/stills/controller/`. The `t..` files are whole frames at 720 x 1280; the `c_..` files
are crops from native frames, added for this merge.

1. `t00m00s.jpg` - start: B1 + B2 with the turret, lead with flag "5", loose parts laid out, joysticks wired to the module.
2. `t00m12s.jpg` - B3 in the hands, "B3" readable, shape of its top edge.
3. `t00m24s.jpg` - B3 and B4 seated, empty slots in B2, "R4" on the turret, lead off to the left.
4. `t00m32s.jpg` - module from above with both joysticks: digital legends, ribbon colours, HW-504 boards.
5. `t00m39s.jpg` - module in the hand (0:39.5): "G V S", "A0..A7", which row each wire colour is in.
6. `t00m52s.jpg` - left joystick seated in B5: board edge through the wall slots, header legend, "B5".
7. `t00m57s.jpg` - B6 held up: "B6", long arm, hooked end post.
8. `t01m24s.jpg` - left group seated on B2; ribbon route; module on the worktop to the left.
9. `t01m51s.jpg` - right joystick being pushed into the second B6 from behind.
10. `t01m59s.jpg` - B7 on the right joystick, engraving outward (1:59.5).
11. `t02m19s.jpg` - both groups seated; both ribbons; flag "5" on the right.
12. `t02m22s.jpg` - module lifted in the left hand over the left edge, USB toward the turret.
13. `t02m31s.jpg` - the same, held up to the camera; lead flag "5" off to the right.
14. `t02m46s.jpg` - module carried to the right in its final orientation; B4, both B6 arms and their hooked ends, R4.
15. `t02m52s.jpg` - slide in progress: plain end entering the right-hand B6 arm; plain-end header legends.
16. `t02m56s.jpg` - plain end reaching the left-hand B6 arm; all digital legends and S V G letters.
17. `t03m05s.jpg` - final push and press on the power-jack end.
18. `t03m11s.jpg` - B8 just lowered over the thumb caps, engraved face up, all five engravings.
19. `t03m27s.jpg` - B8 seated, hands off; module in place; lead still unplugged.
20. `t03m45s.jpg` - from outside R6: "R6" engraving, empty hook slot in the lug, lead coming out from under the lug.
21. `t03m47s.jpg` - plug end held up, flag "5"; module legends; empty L-slot in R4.
22. `t04m09s.jpg` - turret from the controller side: "R1", "R2", "R5"; lead under R6's lug.
23. `t04m17s.jpg` - plug being pressed onto the digital header.
24. `t04m24s.jpg` - end state: plug on row 5, both ribbons, lead over R4's top edge beside the empty L-slot.
25. `c_t02m51s_B7_engraving_outward.jpg` - 2:51, base tilted: "B7" on the outer face of the fitted wall; right joystick header and ribbon.
26. `c_t02m56s_module_legends.jpg` - 2:56 at twice native size: every digital legend, the three plain-end headers, "S V G" by the capacitor, red on the outer row and yellow on the inner row of the analogue header.
27. `c_t03m47s_analogue_plugs.jpg` - 3:47: the eight jumper plugs on A0 - A3 (purple and blue on the edge row, green, then yellow nearest the Nano), bare A4 - A7, "POWER" LED, hooked end of a B6 arm.
28. `c_t03m47s_usb_end_B4_post.jpg` - 3:47: mini-USB end of the module with the end of B4 standing just beyond the board edge; "13 12", "11 10" legends.
29. `c_t04m24s_module_end_state.jpg` - 4:24: the whole module in place, both ribbons, servo plug and flag, B8's "B8" and "Elbow".

Beside this report: `video_controller_seg2_row5_overlay.jpg` (seg 2's 26x crop of 4:24 with predicted pin positions)
and `video_controller_row5_check.jpg` (my check: the same frame plain, with a 14 mm plug drawn on row 5, and with one
drawn on row 6).

## Appendix A. Where the module lies and how the wires run, stage by stage

| Time | I/O module | Joystick ribbons | Base servo lead |
| --- | --- | --- | --- |
| 0:00 - 0:26 | Back-left of the worktop with the joysticks, not in play | Bunched between joysticks and module | Across the plate, then (0:08) off the left edge |
| 0:29 - 0:33 | Flat, left of the plate, level with B4, USB end away from the builder | Fanned out toward the builder, one joystick at each end | Off the left edge |
| 0:34 - 0:44 | In the hands, shown to the camera | Held up | same |
| 0:45 - 1:06 | Flat, left of the plate, 30 - 80 mm from its edge, USB end away from the builder | Black..orange to the right joystick parked far-left beside the turret; yellow..purple to the left joystick in the hand | same |
| 1:07 - 1:47 | Same place | Yellow..purple leaves the left joystick's header toward the turret, bends left across B5's arm about where B4 crosses, and goes off the left edge to the module. Black..orange still to the parked joystick | From 1:07 over the R4 / R6 corner and off the RIGHT edge |
| 1:48 - 2:02 | Same place, pulled round so the USB end points away-right | Black..orange now crosses over yellow..purple | same |
| 2:03 - 2:19 | Against the left edge of the plate beside the turret, 10 - 40 mm out, power jack away-left | Both arch from the two headers up over the left walls and B4 to the analogue header | same |
| 2:20 - 2:44 | In the left hand above the left edge of the plate, USB toward the turret | Both arch from the module over to the right | same |
| 2:45 - 2:57 | Carried over the base to the right, turned, slid in toward the left | Both stand up from the joystick headers and arch to the right, then follow the module in | Lying on the plate in the gap between the module and R4, off to the right |
| 2:58 - 3:37 | In place | Left ribbon loops out past the plain end on the builder's left (over B5's low arm at 3:05); right ribbon crosses the top of the Nano | Lifted clear to the right at 3:08 |
| 3:38 - 4:13 | In place | same | Tucked under R6's lug (3:38 - 4:13), plug resting beside the USB end |
| 4:14 - 4:25 | In place | same | Over R4's top edge near Z 147, free loop to the right, plug on row 5 |

Ribbon length is about 20 cm (guess from the frame), female plugs at both ends, the four wires of each ribbon still
joined as a flat strip. There is enough slack for the module to lie on the worktop beside the plate, on either side,
while both joysticks are seated.

## Appendix B. Legends read on the boards

**Joysticks** (black board; read at 0:32, 0:52, 2:46, 3:06): "HW-504" printed on the board. Five-pin right-angle
header, pins marked in order `GND`, `+5V`, `VRx`, `VRy`, `SW`. Four wires on GND, +5V, VRx, VRy; SW is left bare. As
fitted, GND is the pin at the builder's right (+Z) end of each header and SW at the left, which is the CAD's pin order
(left joystick caps NAUO104 GND at Z 123.4, NAUO105 at 120.9, NAUO106 at 118.4, NAUO107 at 115.9; right joystick
NAUO103 GND at Z 168.4, NAUO108, NAUO109, NAUO110).

- Left joystick (NAUO80): yellow = GND, green = +5V, blue = VRx, purple = VRy. Sure (read against the legend at 0:52).
- Right joystick (NAUO81): black = GND, brown = +5V, red = VRx, orange = VRy. Sure of the order of colours along the
  header; which end is GND is taken from the same sense as the other board and from 2:46 (fairly sure).

**I/O module** (blue board, yellow 3-pin headers, Nano on sockets; best frames 0:32, 0:39.5, 1:24, 2:52, 2:56, 3:47,
4:24; stills `t00m32s.jpg`, `t00m39s.jpg`, `c_t02m56s_module_legends.jpg`):

- **USB end.** Mini-USB socket on the Nano; black DC power jack on the module at the same end, on the analogue side;
  beside the jack a red reset button, a diode and an electrolytic capacitor (can printed `CS 47 35V`). "NANO" printed
  on the Nano; its LEDs marked `L`, `POW` (or `PWR`), `TX`, `RX`; its own 2 x 3 black header at its plain end.
- **Digital side** (the long edge that ends up facing the joysticks, -X). Four yellow blocks of four rows, a gap
  between blocks. One legend per row on the Nano side of the header, from the USB end to the plain end:
  `AREF`, `GND`, `13`, `12` | `11`, `10`, `9`, `8` | `7`, `6`, `5`, `4` | `3`, `2`, `1`, `0`, with `TX` beside 1 and
  `RX` beside 0. All sixteen read at 2:56. Beside each block three letters name the columns: `S` nearest the Nano,
  `V`, `G` at the board edge. So row 5 is the third row of the third block from the USB end.
- **Analogue side** (the long edge that ends up facing the turret, +X). One yellow block three pins wide and eight
  long. `S`, `V`, `G` printed beside the capacitor, with S at the board edge and G nearest the Nano. `A0 A1 A2 A3 A4
  A5 A6 A7` printed along its outer side, A0 nearest the capacitor / USB end (read at 0:39.5). Both blocks therefore
  read G, V, S in the same direction across the board (digital: G at its edge, S inward; analogue: G inward, S at its
  edge).
- **Plain end.** Three small yellow headers: a 2 x 3 block with one row marked `GND` and one `3V3`; a 4-pin header
  marked `SCL SDA 5V GND`; a 4-pin header marked `RX TX 5V GND` (in both 4-pin headers GND is the pin at the plain-end
  edge). A small LED at the plain-end corner on the analogue side marked `POWER`. None is used by the kit.
- Unpopulated rows of solder pads along both long edges; a mounting hole in each corner.

**Jumper plugs on the module.** All eight are at the A0 - A3 end of the analogue block; A4 - A7 stand bare.

| Joystick pin | Wire | Module pin | How it was read |
| --- | --- | --- | --- |
| Right GND | black | A0 G | black goes to the row next to the Nano at the capacitor end (4:24); otherwise from Lee's list |
| Right +5V | brown | A0 V | from Lee's list and the ribbon order |
| Right VRx | red | A0 S | outer row at the A0 legend, read at 0:39.5, 1:24, 2:56. Sure |
| Right VRy | orange | A1 S | outer row at the A1 legend, 0:39.5, 1:24. Sure |
| Left GND | yellow | A2 G | innermost of the three plugs across the board at A2 (2:56, 3:47, 4:24). Fairly sure |
| Left +5V | green | A2 V | middle of the three (3:47, 4:24). Fairly sure |
| Left VRx | blue | A2 S | outer row at the A2 legend, 0:39.5, 1:24. Sure |
| Left VRy | purple | A3 S | outer row at the A3 legend, 0:39.5, 1:24. Sure |

This is Lee's list exactly. In the CAD the same eight are caps NAUO97 (A0 G), NAUO96 (A0 V), NAUO95 (A0 S), NAUO98
(A1 S), NAUO99 (A2 G), NAUO100 (A2 V), NAUO101 (A2 S), NAUO102 (A3 S); rows at Z 141.5 (A0), 139.0 (A1), 136.5 (A2),
134.0 (A3); G row X 83.2, V 85.6, S 88.1.

**Servo plug.** Flag "5" on the base servo's lead; plugged on digital row `5`; orange on S (Nano side), red on V,
brown on G (board edge). CAD: digital S row X 55.06, V 52.57, G 50.09; block "7 6 5 4" at Z 135.6 - 145.8. The CAD's
other three servo plugs (NAUO84 on row 6, NAUO86 on row 9, NAUO85 on row 10) are not fitted in this video.

**B8** (real part, read at 3:11 and 4:24, from the builder's seat): `Shoulder` with up / down arrows (far left), `B8`
(far centre), `Elbow` with up / down arrows (far right), `Base` with a left / right arrow (near left), `Claw` with a
left / right arrow (near right). So the left stick is Shoulder (push / pull) and Base (left / right), the right stick
Elbow and Claw. The CAD's B8 carries only "B8" (X 22.9 - 29.3, Z 136.4 - 146.0).
