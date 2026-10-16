# RCC first draft: independent review (v1)

15 Oct 2026. What was reviewed: `RCC Build Instructions/guide.py` and the `steps.json` it wrote (23:06), against CLAUDE.md, the
rulebook (`docs/cadasio-patterns.md`), the RCC research (`cadasio_study.md`, `cad_study.md`, `cad_wire_paths.md`, `silkscreen.md`,
`materials_notes.md`), Lee's photos and drawing (`lee_images_2026-10-15/`) and the MRA guide and its `steps.json` for the house
voice. How: reading, plus small read-only scripts on `steps.json`. Part boxes were read from `model.glb`'s JSON header (no geometry
library). Nothing was regenerated, and nothing was looked at in the browser. Points that need a look on screen say so.

Step numbers are the ones the player shows (Step 1 to Step 32; Step 17 is the checklist card).

## Summary

| # | Severity | Step(s) | Finding |
|---|---|---|---|
| M1 | must-fix | 12, 28 | The brown-to-G caution says G is "the pin nearest the left side of the board". As the board's print reads, and as Step 12's camera shows it, G is on the **right**. |
| M2 | must-fix | 31 | The barrel plug "hovers" 9 mm back, with its tip 2 mm short of the socket, and its lead line is 2.0 mm long. The step that fixes published error E3 looks already plugged in. |
| S1 | should-fix | 12c-18c | On the bench a plugged motor lead shrinks from 115 mm to 61 mm (left) or 93.5 mm (right). The MRA's bench leads keep one length. Step 12's Review note says "both are drawn 115 mm here", which is wrong for the bench. |
| S2 | should-fix | 24c-28, 10-12 | Both plugs lie laid aside on their edges. On L1 they sink 1.8 mm into the wood and meet nose to nose on the centre line, so they look plugged into each other. Lee's 15 Oct ruling says a laid-aside plug lies flat. |
| S3 | should-fix | 26, 27 | From above, L7 / L6 slide in under L1. The slots and almost all of the lead line are hidden, and the line ends at L5 (0.56 x the travel). The Review note's premise ("codes cannot be read from above") is wrong for these steps. |
| S4 | should-fix | 5, 6, 10, 11, 14 | Lead lines are missing where the rulebook wants them: the joystick pins into L-JS / R-JS, the wheel onto its shaft, the clip onto the battery's terminals. These steps carry labels only. |
| S5 | should-fix | 5, 6 | Set down 7 mm short, the joystick's board is 11 mm inside the controller board (4.2 mm when seated). The Review note says 4 mm. |
| S6 | should-fix | 21, 22, 28, 29 | Wording: the motor's tab goes through a **slot** in L5, not a "notch". The build's plug-ins should read "Reconnect the ... wheel motor to LWh / RWh", as Lee worded the MRA's. |
| S7 | should-fix | Start | Title "Radio Controlled Car (RCC)". TechBox's published guide is titled "Remote Controlled Car (RCC)". Ask Lee which. |
| S8 | should-fix | (README) | The README says its 16 questions are "also on the steps as Review notes". Several are not: colours (except the signal wire), names, the battery lead's length, section cards, and L1's face. |
| N1-N16 | nice-to-have | various | See the end of this report. |

---

## Must-fix

### M1. Steps 12 and 28: the brown-to-G caution points the wrong way as the student sees the board

`guide.py` line 317: `BROWN_TO_G = 'Very important: the brown wire goes on G, the pin nearest the left side of the board.'`

- **The print.** The adapter prints "S V G" under U1 and U2. The letters stand upright for someone looking from the car's front
  towards its rear. Lee's photo and `silkscreen.md` 1.2 agree: photo up = -X, photo right = -Z. So the print reads S, V, G from left
  to right, and **G is the right-hand pin**. The parts-list picture `parts/Adapter-Board.png` shows the same.
- **Step 12** (the first time the caution is shown). The camera is front-right (dir +X +Z). Screen-right runs towards -Z, so G is on
  the right of the header on screen as well.
- **Step 28.** The camera is rear-left, and there G does appear on the left. So the sentence is right for the car's left and for one
  of the two pictures, but wrong for the board's own print and for Step 12.
- **The MRA's wording does not carry over.** "The pin nearest the edge of the board" fails here: on the adapter's narrow leg, G and
  S are about equally far from the two long edges (photo: G 2.7 mm from its edge, S 3.9 mm from its).
- **What is right.** The CAD and the drawn leads are correct. On U1 and U2, brown ends on z 1318.43 (G), red on 1320.97 (V) and
  yellow on 1323.51 (S), on the bench and in the car, and the plugs use `g_towards=[0, 0, 1]`.

**Fix.** Use a cue that holds whichever way the board is seen. The board prints "LWh" / "RWh" right beside G (at z 1316.08), so:
"Very important: the brown wire goes on G, the end pin next to the letters LWh and RWh." Or tie it to the car: "...on G, the pin on
the same side as the left wheel". On the bench the left motor stands on that side too.

### M2. Step 31: the barrel plug hardly moves, and its lead line is 2 mm long

`guide.py` line 417: `path=[OUT_OF_SOCKET, ZERO]` uses the CAD's "out" pose, 8.95 mm back. In that pose the plug's tip is 1.95 mm
short of the jack's mouth.

- In `steps.json` the Step 31 lead line runs from x 687.3 to 689.3, so it is **2.0 mm long for a 9 mm travel** (the rulebook wants
  about 1.0 x the travel).
- The camera frames the whole car (radius 119). Step 31 therefore looks the same as Step 31c, and published error E3 ("the battery is
  never connected") is fixed in data but hardly on screen.

**Fix.**
- Give the plug a hover that clearly shows it out: for example `path=[lifted(OUT_OF_SOCKET, 30.0), OUT_OF_SOCKET, ZERO]` (up beside
  the battery, down onto the socket's axis, in). And/or punch in on the socket with `focus=[BARREL, MODULE]`, which rulebook 13
  allows for a plug going onto a pin.
- End the line where the tip finishes, not at the mouth. A single point `lines_at=[[696.29, 925.05, 1354.06]]` (the tip, seated)
  draws the whole travel, as a breadboard line ends on the floor of the hole.
- The same mouth-ending makes Step 15's last leg 5 mm.
- The CAD's 30-39 mm battery lead is what boxes the plug in (`cad_wire_paths.md` 6.2); see N10.

---

## Should-fix

### S1. Steps 12c-18c: on the bench the motor leads shrink when plugged in

Middle-wire lengths, computed from `steps.json` routes:

| | Left lead | Right lead |
|---|---|---|
| Loose on the table (Steps 10-12) | 115.0 mm | 115.0 mm |
| Held over its header (in-between route, Step 12c / 13c) | 51.0 mm | 83.4 mm |
| Plugged (Steps 12c-18c) | **61.0 mm** | **93.5 mm** |
| In the car (Steps 28c / 29c) | 115.6 mm | 118.9 mm |

In Step 12c the left lead visibly loses almost half its length as it is plugged in. It stays that short through the unplugging in
Step 18c, then is 115 mm again in the hand at Step 21. The MRA's bench leads keep one length (base 180.7 mm throughout Steps 12-18c).
Lee objected to a lead "shrunk to half" on 15 Oct (rulebook 14).

**Fix.** Either stand the motors further out from the module on the bench (`MOTOR_ON_BENCH` with an outward z offset), so that 115 mm
reaches naturally, or give `bench_over` / `bench` a slack loop lying on the table, so that `W.length(bench[1])` is about 115 mm. Then
correct the Step 12 Review note (line 324), which says both leads are drawn 115 mm "here".

### S2. Steps 24c-28 (and 10-12): the laid-aside plugs stand on edge, sink into L1 and meet nose to nose

- **On edge, and sunk into L1.** The deck route (line 185) runs the lead at y 911.2 and ends the plug with its contacts stacked
  vertically: the wire ends are at y 908.66 / 911.2 / 913.74. The 7.6 mm wide housing therefore stands on its 2.6 mm edge, centred at
  y 911.2, with its bottom about 1.8 mm below L1's top face (909.23). The lowest conductor also dips about 1.1 mm into the wood.
  (The CAD's own loose plug is on edge too, but sits on L1 with its centre at y 913.04.)
- **Nose to nose.** The right plug's mating face ends at z 1338.55 and the left plug's at z 1338.41, both at x 627, y 911.2. The two
  housings touch face to face on the car's centre line behind the battery hole, so they read as the two leads plugged into each other.
- **On the bench (line 173)** the loose plugs also stand on edge on the table (centred at TABLE_Y + 3.8).
- Lee's ruling of 15 Oct (rulebook 14) says a lead laid aside "lies on a surface with its plug flat".

**Fix.**
- Lay each plug on its broad face (G-to-S across horizontal at the plug, its centre about 1.3 mm above the surface). That needs the
  ribbon to twist about 90 degrees along the lead.
- Stop each lead on its own side of the centre line, with a clear gap between the plugs: for example, shorten the last leg
  (`z - side * 60` to about `z - side * 35`) and spend the length on a gentle curve.
- Or, at the least, raise the deck route to y >= 913.05 so that nothing is inside L1.

### S3. Steps 26 and 27 (L7, L6): the slide happens out of sight, and the Review note's premise is wrong

- **The motion is hidden.** The camera is a normal diagonal from above (elevation 35 degrees). L7's body slides under L1, through the
  slots in L5 and L4. Of the lead line, which runs at y 902.6 under L1, only about 8 mm of 36 mm is in view. Its far end (L5's slot)
  and L4's slot are under L1. In Step 26c only the head shows. This is why the published guide went below the horizon.
- **The line is short.** It ends at L5's front face, 36.3 mm for a 64.7 mm travel (0.56 x). The snap tab finishes in L4's slot.
- **The codes can be read here.** `L67_NOTE` says the codes "cannot be read from above". While L7 / L6 hover in front of the car
  (x 774-839), their outer faces, which carry the codes, face the camera: L7's -Z face from the front-left camera, L6's +Z face from
  the front-right one. So the codes can be read on Step 26 / 27 itself. They are hidden only in the finished car. The README's
  question 13 has the same premise.

**Fix.**
- Show both steps with the car turned over (`flip=True`, caption "Turn the car over. Slide L7 in..."), so that the bodies, the slots
  and the line face the camera. That makes a second flip block, which the geometry forces (L7 / L6 must follow the module). Then
  "Turn the car the right way up." on Step 28.
- Or keep the view and add an `inset=` on Step 26c / 27c showing the clip from below.
- End the line in L4's slot, with a single point at the tab tip seated (about [716.1, 902.6, 1323.0] / [716.1, 902.6, 1354.0]).
- Reword the note: the codes face out and can be read while each part hovers, but are hidden under L1 once it is in. Does TechBox
  still want them on the heads?

### S4. Steps 5, 6, 10, 11 and 14: rigid parts going onto mating features have no lead lines

The rulebook (sections 5 and 9) gives a rigid part travelling onto mating features red lead lines: 1 for an axial part, 2 for a
two-tab or two-lead part. These steps pass `lines=False`, so their only cue is the part-name and destination labels.
`cadasio_study.md` section 5 proposed the wheel's line ("one lead line down the shaft"). CLAUDE.md's checklist flags a `lines=0`
step that is not a wire or a card.

- **Steps 5 / 6 (joystick into L-JS / R-JS):** two lines at the end pins, as single points at the seated pin tips (6 mm inside the
  socket). Left: `[731.75, 921.86, 1079.92]` and `[731.75, 921.86, 1089.92]`; right: z + 72.77. The player bends each line through
  the waypoint, so it shows "down, then in".
- **Steps 10 / 11 (wheel onto its shaft):** one line down the axle, from the hub to the spline. It is a rider now (`ride=`), so either
  make the wheel the moving part or give `lines_at` in the bench frame (the motor sits at `MOTOR_ON_BENCH`).
- **Step 14 (clip onto the battery):** two lines, from the clip's snaps to the battery's terminals (also in the bench frame).

### S5. Steps 5 and 6: the joystick goes through the controller board

| Pose | Joystick board (x) | Cut-out (x) | Overlap with the controller board |
|---|---|---|---|
| Set down 7 mm short (`[-7, 0, 0]`) | 684.7 - 718.7 | 695.9 - 727.5 | 11.2 mm |
| Seated (the CAD's own problem, `cad_study.md` 4.1) | 691.7 - 725.7 | 695.9 - 727.5 | 4.2 mm |

So the "set it into its pocket" stage puts the joystick board deep into the white board, and it then slides 7 mm still inside it.
The hand-set paths are not collision-tested (stepgen only tests when `direction` is left out). `JOY_NOTE` describes only the 4 mm
seated overlap. Also worth a look in the browser: possible flicker where the joystick board and the controller board overlap,
since the CAD has them nearly in one plane (tipped 3 degrees).

**Fix.** Keep the Review note, but say that the set-down pose overlaps by 11 mm. Ask whether the joystick really sits lower, in the
guard's pocket, with its far end under the board. That would also answer the "which row of L-JS" question. Until Lee answers, an
`adjust_mm` on the joysticks, or a path that enters pins-first at a tilt, would stop the pass-through.

### S6. Wording against the CAD and Lee's MRA phrasing

- **Steps 21 and 22** (lines 384, 387): "Push the ... wheel motor into the notch at one end of L5." The motor's front tab (ear)
  goes through a closed 12.1 x 2.55 mm slot near the end of L5 (`cad_study.md` 2.1 / 2.2). Suggested: "Push the tab on the front of
  the right wheel motor through the slot near one end of L5, its wheel outwards and its wire pointing away from L5."
- **Steps 28 and 29** (line 411): "Plug the left wheel motor into LWh." Lee's MRA wording for the second plug-in of a motor that was
  tested is "Reconnect the base motor to Row 5" (rulebook 13, 15 Oct). So: "Reconnect the left wheel motor to LWh. Remember brown to
  G, red to V, and yellow to S."

### S7. Start: the kit's name

`Guide(title='Radio Controlled Car (RCC)')` (line 97). TechBox's published guide 19075 is titled **"Remote Controlled Car (RCC)"**
(`cadasio_study.md` 2.1, and the guide's own id `rcc_remote_controlled_car`). CLAUDE.md and the README say "Radio". The title block
is the kit's name, so one line to Lee settles which.

### S8. Open decisions that appear only in the README, not as Review notes

The README's question list says "(also on the steps as Review notes)". These are not on any step, so Lee will not meet them in the
player:

- Q7, colours, apart from the signal wire: FS90R body, radio boards, wheels, plug housings, pins, white boards, and whether the I/O
  module is the MRA's board.
- Q8, names.
- Q12, the top-face part: Step 19's note states the etching but does not ask whether the drawing shows the top or the underside.
- Q14, the battery lead's length.
- Q15, section cards with Lee's two photos.

**Fix.** Add short notes where each first matters:

| Note | Step |
|---|---|
| Names | Step 1 |
| Radio colour | Step 4 |
| I/O module board, and whether it is the MRA's | Step 7 |
| Section card for the adapter | Step 8 |
| Section card for the controller | Step 3 |
| Motor body and wheel colours | Step 10 |
| Battery lead length (and whether the battery is in the kit) | Step 14 |
| Top face or underside | Step 19 |

Or change the README's line to say which questions are notes.

---

## Point by point

### 1. Rulebook compliance

| Rule | Status |
|---|---|
| One kit item per step | Holds. Step 18 unplugs two plugs at once, as Lee chose for the MRA. Step 24 (the L4 / L5 / motor block) and Step 25 (the module with its riders) are sub-assemblies. |
| Step N / Step Nc pairs | Holds. The checklist is a numbered card, as on the MRA. |
| Camera held inside every pair | Checked on all 30 pairs. |
| Travel at least 40 degrees off the view axis | 54-69 degrees on every leg. |
| Never from below | Holds. The four flipped steps (1, 2, 19, 20) turn the model, and a flip run shares one pivot. |
| Lead lines 1, 2 or 4 | Holds wherever drawn. Lengths are discussed under S3, M2 and N5. |
| Destination labels on plug-in steps | H1 / H2, NRF24L01, L-JS / R-JS, U3, LWh / RWh, with no dotted ring on the pin labels, as on the MRA. No destination label on the barrel plug, but there is no print at the jack (the module's "POWER" is at the far end, x 745). |
| Engraved codes, Lee 14 Oct | Each wood step is seen from the side its code faces: L2 (-Z, Step 19), L3 (+X, Step 20), L5 (+X, Step 21), L4 (+X, Step 23, readable over L5 at 135 mm), L7 (-Z, Step 26), L6 (+Z, Step 27). |
| Hover distances | Plug-in parts 35 mm. Guards 65 (a face-on panel). Module 60 and L7 / L6 64.7 (1.0 x their length). Battery 47.9. L4 135 (it must clear the plugs). Exceptions: Step 31 (M2), and the wheel at 40 against the rulebook's 60 (N8). |
| Cautions | On both views of each step. M1 covers the wording. Step 12 adds the brown-to-G caution to the test's first plug; the MRA had it only on the build's first plug. That is reasonable here, since it is the student's first plug, but it is one more departure for Lee to confirm. |
| Every Step N carries a cue | True if labels count. Lead lines are missing where the rulebook expects them (S4). |
| Captions in the house voice | They follow the MRA closely ("Begin the car's electronics with the I/O module...", "...for the test. Remember brown to G, red to V, and yellow to S.", "Set the ... aside for now. You will use them again in a bit."). Exceptions: S6, N9 and N11. |

### 2. Correctness against the CAD and the wiring

| Point | Verdict |
|---|---|
| Left motor to LWh = U1 (x 717.5); right to RWh = U2 (x 730.2) | Correct. PLUG_L / NAUO20 on U1, PLUG_R / NAUO19 on U2, labels LWh / RWh. |
| S / V / G | Correct in the data: brown on G, z 1318.43, on both plugs, bench and car. Lead order at the motor matches the CAD (right: brown on top; left: brown at the bottom). The caution's wording is wrong (M1). |
| Car Nano | NANO_CAR is the controller's Nano moved +225 mm in z only. Its USB shell is at x 689.4, the same end as the jack (689.3-703.7), and its rows match the module's (D12 row z 1330.3, D13 row 1345.5). Correct, and it fixes E2. |
| The module slides in before L6 / L7 | Correct (Step 25, then Steps 26-27), from the front along the grooves to L2's fin, as `cad_study.md` 2.3 requires. Both lead lines stop in free space at the seated corners, 0.6 mm short of L2's fin (N6). |
| Battery and barrel plug | The battery goes down through L1 into L3 with its clip on, then the plug goes in. Correct, apart from M2. |
| USB | One cable, the controller's, with the A end on the table. Correct, and the car is powered by the battery. Review notes cover the open questions. |
| Joysticks | Left = NAUO12 into L-JS at low z, the student's left with the grips towards them, matching Lee's photo; right = NAUO13 into R-JS. Correct. |
| Guards | Left NAUO24 is on the L-JS half. Correct. |
| Motors, wheels, L6 / L7 | All named correctly: right motor +Z, left -Z; L7 at z 1321.5-1324.5, left of L2; L6 right of it. |
| L1's etching | `move_engraving` turns L1 and FRONT is drawn as a decal, as Lee decided on 15 Oct. |

### 3. The published guide's errors (`cadasio_study.md` section 4)

| # | Fixed? |
|---|---|
| E1, the car's Nano disappears | **Yes.** It rides with the module and is on screen from Step 25 to the Completed View. |
| E2, the car's Nano reversed | **Yes**, with a Review note (Step 7). N13 suggests a camera that shows the USB end. |
| E3, the battery never plugged in | **In data only.** Step 31 shows almost no motion (M2). |
| E4, the joysticks glide in through the guard | **Partly.** The new path passes through the board instead (S5). Flagged to Lee. |
| E5, the test is half there | **Yes:** power, checklist placeholder, unplug, set aside. The controller and battery leave unannounced (N12). |
| E6, the electronics come in diagonally | **Yes.** A 60 mm slide along the grooves with two lines, as the CAD requires (not "straight down", which the study proposed). |
| E7, the guards never fitted | **Yes**, Steps 1-2, with a Review note. |
| E8, the wheels never fitted | **Yes**, Steps 10-11, but without the lead line (S4). |
| E9, the clip never fitted | **Yes**, Step 14, without lead lines (S4). |
| E10, the plugs-through-L4 cue | **Yes.** The caption says it. The lines run from L4's holes along the leads. |
| C1 (navy module), C4 (Mini-B), C5 (wood) | Fixed in `materials.json`. |
| C2, C3, C6 | Asked: C6 as a Review note, C2 / C3 in the README only (S8). |
| R1, R5, R7, R8 | Fixed. |
| R2 | Mostly fixed (S4). |
| R3 | Fixed. |
| R4 | Fixed, but the motion is now hidden (S3). |
| R6, section cards | Not done (the player has no photo cards yet). It is in the README only (S8). |

### 4. Review notes

**Coverage of `cadasio_study.md` section 6.**

| # | Decision | Where |
|---|---|---|
| 1 | Power | Steps 14 and 16 |
| 2 | Checklist | Step 17 |
| 3 | Wheels | Step 10 |
| 4 | Order; L2 in one step or two | Steps 26 and 19 |
| 5 | L4 | Step 23 |
| 6 | Barrel plug | Step 31 |
| 9 | Car Nano | Step 7 |
| 10 | Joystick row | Step 5 |
| 11 | Guards | Step 1 |
| 12 | L1 | Step 19, which asks only about the drawing, not the face (S8) |
| 7 | Colours | Signal wire on Step 12 only; the rest in the README (S8) |
| 8 | Names | README only (S8) |
| 13 | Section cards | README only (S8) |

**Notes that are wrong or unclear.**
- Step 12: "both are drawn 115 mm here" is wrong on the bench (S1).
- Step 26 (`L67_NOTE`): the premise about reading the codes is wrong for Steps 26-27 (S3).
- Step 5 (`JOY_NOTE`): it understates the overlap at the set-down pose (S5).
- The others read clearly.

### 5. Consistency of `steps.json`

**Checks that passed:**
- Every wire shown in a view has both end parts visible in it.
- No rider is visible without its carrier.
- Every label and eye anchor lies on its own part's box (0.0 mm away, all 40).
- Every lead-line tip lies on the moving part.
- Every mouth lies on a stationary part, except Step 25's two (N6). Step 23's two land on the motors, which is where L4's holes end up.
- Parts appear and vanish only at the intended places: the controller put away after Step 6 and back at Steps 16 and 32; the bench
  set-up put away after Step 18; the chassis hidden for the bench work of Steps 21-23; the module back at Step 25; the battery at
  Step 30.

**Points to look at:**
- **The lead lengths across steps** (S1). Also the battery lead: 52-57 mm on the bench, 33-39 mm in the car (N10).
- **The flip back at Step 21.** The last flipped view is Step 20c. Step 21 is unflipped and changes the content at the same moment
  (the chassis is hidden, and L5 and the motor appear). Check in the browser that the turn back does not swing L5 and the motor round
  through 180 degrees as they appear. If it does, end the flip run on a view where nothing new appears, or start Step 21 afresh.

---

## Nice-to-have

| # | Step(s) | Point and suggestion |
|---|---|---|
| N1 | 3 | **Three labels** (Nano Board, H1, H2); the MRA never shows more than two. Drop "Nano Board", which the caption names. |
| N2 | 3, 7 | **The two Nano Boards get different line counts:** the controller's gets 2 lines at diagonal corner pins, the car's gets 4. The rulebook wants 4 at the corner pins for a pin-header board. Make Step 3 match Step 7. |
| N3 | 5 / 6 | **The camera swings** from front-left to front-right between the two joysticks. `cadasio_study.md` 5 suggests one camera if one view shows both pockets. |
| N4 | 10, 11 | **The motor floats.** Before its wheel is on, each motor hangs about 24 mm above the table (it is lifted to its height standing on its wheel). Acceptable as "in the hand", but it looks odd beside the module lying on the table. |
| N5 | 3, 4, 7, 8, 9, 30 | **Lead lines end at the socket mouth or hole mouth,** so they are 0.83-0.84 x the travel (Step 30: 0.65). Ending them where the pin tip finishes gives 1.0 x, as the rulebook's breadboard lines do. |
| N6 | 25 | **The module's two lines end in free space** at the seated back corners (x 691.1), on no part. End them at the rear of L4's grooves (x 713.1), the last female feature. |
| N7 | 18 | **The caution says only "the wheel motors and the I/O module".** The controller, the battery and the USB cable also leave the screen there (put away before the card). Suggested: "Set the controller, the battery, the wheel motors and the I/O module aside for now. You will use them again in a bit." |
| N8 | 10, 11 | **Wheel hover 40 mm;** the rulebook's default for a part onto a shaft is 60. |
| N9 | 15, 31 | **Label and caption names.** The plug's label reads "Battery Clip" (its part's name, the MRA's motor-on-plug convention) while the caption says "barrel plug". Suggested caption: "Plug the battery clip's barrel plug into the power socket on the I/O module." |
| N10 | 14, 30 | **Battery lead length.** The bench lead is drawn 52-57 mm and the car's 33-39 mm (the CAD's). Ask Lee for the real length (S8) and draw one length. It would also free Step 31's hover (M2). |
| N11 | 20, 23, 21, 26, 27 | **Code direction in captions.** The CAD's L3, L4 and L5 are nearly symmetric, so the code is the only cue to which way round they go. If TechBox wants them the CAD's way, say "code facing the front" (L3, L4, L5) and "code facing out" (L6, L7), as the MRA's captions do where it matters. Also ask Lee which face the real L4 is engraved on (`cad_study.md` 2.6). |
| N12 | 24 | **The leads and L1's notches.** As the block drops, each lead has to fall into the small notch in L1 behind its motor. A clause in the caption would help, in the MRA's manner ("Keep the base motor's wire up out of the way so it is not trapped."). |
| N13 | 7 (and 3) | **Camera and the orientation cue.** The camera is from the front (+X), so the Nano's USB socket and the power socket, which are the orientation cue, are at the far end. Since E2 was a picture error that students copy, consider `look_from` the rear for Step 7 (and the USB end for Step 3). |
| N14 | Start, Completed View | **Check the composition.** From the front-left camera, the controller (at the car's left) is about 130 mm nearer the camera than the car and overlaps the car's rear-left on screen by roughly 50 mm. Check the title page and Completed View in the browser. |
| N15 | 4 | **Radio orientation caution.** `cadasio_study.md` suggested a caution on the controller radio's orientation "if TechBox wants one". It is not asked anywhere. |
| N16 | 5 | **JOY_NOTE leaves out the guard floor.** It could also mention that the joystick's underside sits 2.8 mm into the guard's pocket floor (`cad_study.md` 4.2). |

## Files

- Reviewed: `RCC Build Instructions/guide.py`, `RCC Build Instructions/steps.json`, `RCC Build Instructions/materials.json`,
  `RCC Build Instructions/decals.json`, `RCC Build Instructions/README.txt`, `RCC Build Instructions/parts.json`.
- Compared with: `MRA Build Instructions Prototype/guide.py` and `MRA Build Instructions Prototype/steps.json`.
- Part boxes for the anchor checks were read from `RCC Build Instructions/model.glb` (its JSON header only), with a scratch script
  kept in the session scratchpad.

## What was done (15 Oct 2026)

| Item | Done |
|---|---|
| M1 | The caution now reads "Very important: the brown wire goes on G, the pin on the same side as the left wheel." (G is at the car's left on U1 and U2; true from any camera, on the bench and in the car.) |
| M2 | In the car the barrel plug rides lifted 14 mm clear of the socket, its back against the battery; Step 31 takes it down onto the socket's axis, then in (two beats), with the camera closer (focus on the plug, battery and module) and one lead line from the tip's hover to where it finishes. Step 15 likewise ends its line where the tip finishes, and looks from the side the plug lies on. |
| S1 | The bench and the plugged routes are fitted to the lead's length: 114.9 mm loose, on the bench and plugged in, for both motors. |
| S2 | Every laid-aside plug lies flat (the lead turning flat along its length): on the table on the bench; on L1 behind the battery's hole, resting on the wood (0.03 mm above it), the two ends 12.3 mm apart either side of L2's tab. |
| S3 | L7 and L6 are shown with the car turned over ("Turn the car over. Slide L7 in ..., on the left wheel's side of L2."); Step 28 opens "Turn the car the right way up." The Review note's wrong premise is gone. |
| S4 | Steps 5 and 6: two lead lines, the end pins to the socket's mouth. Steps 10, 11 and 14: a red arrow (the wheel along its axle, the clip down onto the battery), because the part rides on another that stands off its seat, where the generator cannot draw a lead line. |
| S5 | The joystick note gives 4 mm seated, 11 mm while set down, and the 2.8 mm into the guard's floor (N16). |
| S6 | "Push the right wheel motor into one end of L5, its mounting tab through the slot, ..."; Steps 28 - 29 "Reconnect the ... wheel motor to LWh / RWh." |
| S7 | Kept "Radio Controlled Car (RCC)": Lee's own words for the kit (15 Oct 2026). The published title differs; listed for Lee. |
| S8 | Review notes added: names (Step 1), section cards (Steps 3 and 8), colours and the I/O module board (Step 7), the battery lead's length (Step 14), L1's etching on the top face (Step 19). |
| Flip at Step 21 | Step 21 starts afresh (`put_away([])`, a cut), so L5 and the motor do not turn over as they appear. |
| N2 | Step 3 has four lead lines at the corner pins, as Step 7. |
| N6 | The module's lines run from its back corners to the back of L4's grooves. |
| N7 | The caution reads "Set the controller, the battery, the wheel motors and the I/O module aside for now. ..." |
| N9 | "Plug the battery clip's barrel plug into the power socket on the I/O module." (Steps 15 and 31) |
| N12 | Step 24: "... and each motor's wire into the notch behind it." |
| N13 | Step 7 looks from the rear, so the Nano's USB socket and the power socket are near. |
| Not done | N1, N3, N4, N5, N8, N10 (waits on Lee's lead length), N11 (in the questions for Lee), N14 (the controller sits in front of the car's left rear on the title page; left for Lee's camera), N15. |

After the changes: `_runthrough()` 67 views, 0 problems; the MRA's 211 views, 0 problems (its core.js gained the new decal shapes).
