# Review: the base and controller guide against Lee's notes of 13 Oct 2026

Written 13 Oct 2026. Checked: `MRA Build Instructions Prototype/guide.py` (21:48), `steps.json` (21:49, 24 steps, 48 views),
`materials.json`, `model.glb` / `model.report.json` (21:37), `colour-atlas-mra.json`, `parts.json`, `parts/`, `js/player.js`,
`js/core.js`, `js/parts.js`, `tools/stepgen.py`, `tools/wires.py`, `tools/build_model.py`, the rulebook, `README.txt` (both as
rewritten at 21:59) and the research in this folder.
Requests are quoted from `lee_notes_2026-10-13.md`; "old Step N" is Lee's numbering, "Step N" is the name in `steps.json` today.

How it was checked. Nothing in the project was changed, no generator was run and no browser was opened. Colours and outline
edges were read out of the shipped `model.glb` (decoded, not rendered). Wire ends, lengths and slot crossings were measured from
the routes in `steps.json`. The horn path of Step 2c and every wire in every view were replayed with the player's own
interpolation against the CAD meshes. Four part pictures in `parts/` were looked at. So anything below that says "looks" is
from data or from those pictures; the step animations themselves have not been seen by this review.

## Verdict per request

| Request | Verdict |
|---|---|
| Opening: more detail, still Chromebook-light | Partly: Nano, screws, servo, thumb caps got more; the I/O module's own parts are unchanged (finding 1). Not tried on a Chromebook |
| Opening: edge at the top of the screw head | Done |
| Opening: wire outlines as thin as other edges | Done in code (0.9 px silhouette against 1 px edges); not seen on screen |
| 1 regulator pins silver | Done |
| 2 solder mounds on the Nano silver | Done |
| 3 mini-USB same silver as the pins | Done (shell and core; the five contacts inside stay lighter) |
| 4 one screw, zoom out, five appear, go in | Done |
| 5 labels and captions on; better part names | Done; three small naming gaps (finding 9) |
| 6 Step 2 = R1 + motor with black horn, 2c = horn angled in; R2 in Step 3 | Done |
| 7 servo label pink with white text | Done in the model; the part picture `parts/Base-Motor.png` still shows the plain side (finding 6) |
| 8 logo | Done (as `logo.webp`) |
| 9, 10 R3 / R4 tab points | Done |
| 11 base motor's wires shown, up, then into R4's slot and straight out | Done |
| 12 B2 slides in over the horn; horn into B1; first screw close up, then five | Done; three points to settle (findings 2, 3, 4) |
| 13 Step 10 begins with B1 below B2 | Done, by making B1 the part that moves (finding 3) |
| 14 the five screws hover, then go in | Done |
| 15 joystick pins silver | Done |
| 16 joystick wires: cut short with a break mark, whole once the module is shown; pin list | Done |
| 17 old Step 23: lead goes from horizontal to row 5 | Done (Step 23) |
| 18 old Step 24 dropped | Done (the move into the slot is Step 8) |
| 19 USB cable later | Left as a text card (Step 24) |
| 20 arm and claw | Still to come |
| 21 jumper colours only need to differ | Done |
| Message 2: how the horn goes through R1 | Done, and it holds up when replayed (0.59 mm worst graze) |

Nothing Lee asked for has been ignored outright. The one request with no change behind it is the grain on the I/O module's own
parts (finding 1); the one that could not be checked at all is loading on a Chromebook.

## Findings

1. **should fix. Opening paragraph, I/O module parts (visible from Step 17 on, close up in Step 23).** Lee named "PCB parts on the
   IO module and Nano board" as grainy. Only the Nano was given more detail. In `materials.json` the rules for the module's own
   parts are the same as in the file Lee was looking at: `^Shield_Arduino` (0.02 mm), `^Samtec-TLW-` (0.02), `^47uf CAP`,
   `^cap106C`, `^(m7 diode|smt_resistor|nano - reg|blm21|reset core)`, `^reset shell`, `^led$`, all at the default 0.04 mm.
   `model.report.json`: resistor 4,056 -> 228 triangles, LED 1,716 -> 224, `blm21` 1,708 -> 262, reset core 1,692 -> 358,
   `cap106C` 6,702 -> 816, regulator 4,092 -> 1,212, 47 uF can 7,719 -> 2,037, and `cap106C`, `led`, `reset shell`, `blm21` carry 0
   outline segments (`edges: false` or `edge_min_size_mm` 3). What did change: Nano budget 6,000 -> 16,000 per colour (26,346 ->
   34,193 triangles, and its pin and mound colour group is no longer relaxed to 0.48 mm), screw 0.04 mm / 1,600 -> 0.03 mm / 3,000
   (2,094 triangles now), servo 0.08 mm / 3,000 -> 0.05 mm / 8,000 per colour (8,965 now), thumb cap budget 1,800 -> 3,500 (2,914
   now). Whole model: 147,909 triangles, 1.35 MB (it was 137,529 and 1.76 MB with the CAD cables in it), so there is room. Fix:
   tighten those rules (for example `simplify_mm` 0.02 and outlines back on for parts over 1 mm), rebuild, and have Lee look at
   Step 23, or ask him which parts still look grainy before spending triangles.

2. **ask Lee. Step 11, the punch-in on the first screw.** It is a 2.0x close-up: camera radius 69.4 mm against 139.1 in Step 12
   and 153.6 in Step 10c (`focus=BASE_SCREWS[:1], focus_pad=2.0`). The frame has to hold the 60 mm hover, so the screw head
   (5.5 mm) is about 3.4% of the view height, roughly 20 to 25 px on a laptop, against 1.7% in Step 12. Lee called the punch-in
   "important" twice. If he wants it tighter: `focus_pad=1.2` gives 5.7%; a shorter hover for this one step (30 mm) with
   `focus_pad=1.6` gives about 7%. The camera also swings a quarter turn for this step (dir z -0.58) and back for Step 12
   (dir z +0.58), which is right for seeing the screw past the turret but is a second movement on top of the zoom.

3. **ask Lee. Step 10 / 10c, which plate moves.** Lee: "Step 10 should begin with B1 distanced below B2." It does: B1 appears
   65 mm below (`offsets NAUO1 [0, -65, 0]`, gliding in from 117 mm below) and the assembly no longer jumps up and back. But it
   is done by lifting B1 up into B2, while the caption says "Place B2 onto B1 so the servo horn fits into the cut-out in B1."
   and the rulebook says a hovering part is "always above or beside its seat, never below it" (section 4) and "the hand-held
   piece is the one that moves" (section 3). `guide.py` only says "B1 comes up from below". Section 14 of the rulebook now
   mentions it ("Where a part goes on from below (B1 under B2) it is shown below the model, seen from above"), but as what the
   player does, not as something Lee decided; section 13 has no entry. Either add it to section 13 as an exception and reword the
   caption ("Bring B1 up under B2 ..."), or ask Lee whether he would rather see the built part come down onto B1.

4. **should fix. Step 9, lead lines.** Lee's description is about the slot and the round cut-out. The four automatic lines are
   at the feet of R5 and R6 instead: tips (143.1, 93.8, 109.5), (184.4, 93.8, 109.1), (136.1, 93.6, 169.3), (191.9, 94.0, 169.3),
   each a 2.5 to 2.8 mm rub patch where a wall stands on B2's top face. Nothing points at the keyhole or the motor. Fix: set them
   by hand, for example one line from the far rim of B2's round cut-out, `lines_at=[[163.6, 92.0, 150.4]]`, alone or with one
   under R5 and one under R6 kept (1, 2 or 4 lines).

5. **should fix. Step 8, no close-up on the slot.** The rulebook (section 13, "Punching in on one small part", decided
   13 Oct) says the camera punches in "where a wire has to be seen going into a slot". Step 23 does (`focus=[MODULE, R4]`, radius
   72.2). Step 8 has no `focus=`: radius 78.8, the whole turret with the lead standing 52 mm above it, so the 2.1 mm stem and
   8.1 x 8.5 mm pocket of the L-slot are about 1% and 4.6% of the view height. Fix: `focus=[R4], focus_pad=1.0` on the Step 8
   `g.place(...)` gives a radius of about 43 (1.8x closer) but crops the top of the upright lead while the step is open;
   keeping the plug in frame as well (`focus=[R4, BASE_PLUG]`) only gets to about 66. `focus` takes whole parts, so a tighter
   frame on the slot itself would need a small addition to `stepgen.py`. Which of the two matters more is Lee's call.

6. **should fix. `parts/` is behind `guide.py`.** `parts/Base-Motor.png` (21:47) was drawn before `PART_VIEWS['Base Motor']`
   was added (`guide.py` 21:48, `parts.json` 21:49): it shows the motor from the house view, both visible sides black, no pink
   label. And three pictures with the old names are still in the folder: `6mm-Screw.png`, `Base-Servo.png`,
   `I-O-Extension-Module.png` (18:17). Fix: open `parts.html` once through `tools/serve.py` so the pictures are redrawn, and
   delete the three old files.

7. **should fix (read from the code, not seen). Steps 2, 15 and 18, parts that ride with a new part lag behind it as it
   glides in.** In `player.js` `go()` a new moving part starts 1.8x further out, but a part that rides with it (`carry`) starts
   at its final spot and takes the "it was not riding before: it glides there" branch of `stepAnimation`. Worked through for
   Step 15: the joystick starts at z +72 and its four wire caps at z +40, 32 mm away from the pins they sit on, closing over the
   0.8 s. Step 18 is the same. In Step 2 the plug stays put while the motor comes down 46 mm, so the 59 mm lead between them
   is squashed. Fix: in `go()`, give each rider of a part that is new in the view the same starting pose as its carrier (or
   treat it as already riding).

8. **should fix (small). The papers are now ahead of the guide.** `README.txt` and section 14 of the rulebook were rewritten at
   21:59, during this review, and are up to date on everything above. They also describe what is not there yet: "Full Build:
   base, controller, arm, claw", sub-assemblies "the upper arm, the lever and the claw", "elbow motor on 6, shoulder motor on 9,
   claw motor on 10". So do the title page (`meta.part` "Full Build") and `guide.py`'s first line. The guide ends at the
   controller (24 steps). Right once point 20 lands; if Lee is shown this build first, say so. Also: `materials.json` still
   carries five `Part...^ARA_Pathways` rules for cable meshes that are no longer in the model; section 14 lists punching in
   for "a wire going onto a pin" where section 13 says "into a slot or onto a pin" (finding 5); and the colour library in
   section 8 still gives the I/O module's header pins as `#e3e3e3`, while Lee's "pins are silver" (`_notes.decided`) made them
   `#a6a9aa`, and has no line for the servo label or the horns.

9. **ask Lee. Three naming gaps against TechBox's Cadasio tooltips (point 5).** (a) Resting the pointer on the Nano shows
   "Nano I/O Module"; Cadasio has "Nano" for that part and "Nano I/O Module" for the rest (the player names top-level parts
   only). (b) The wires have no hover name at all: they are drawn by the player with picking switched off (`mesh.raycast`
   emptied in `core.js`), so of a jumper only the black caps answer "Breadboard Wire (F-F)", and of the motor's lead only the
   plug answers "Base Motor"; in Cadasio the wire bundles and the servo cable carry those names. (c) Captions use "the I/O module" and "the nano", labels
   "Nano I/O Module". The research note asked for one name everywhere; Lee has not been asked which.

10. **ask Lee. Step 2c, pace of the key move.** The motion is right (see message 2 below), but the part Lee calls key, the
    angled dip and levelling, is five poses played in one 0.8 s beat, at a tilt of 12 to 16 degrees. If it reads too fast or too
    flat on screen, make the level pose under the floor (`horn_way[5]`) a stop, which adds a beat, or raise the tilt (the
    research found clean routes at 20 and 60 degrees).

11. **ask Lee (small). Two leftovers on the Nano and one on the jack.** The five contact blades inside the mini-USB socket are
    still `#d3d6d3` (seen only looking into its mouth). Fifteen tiny navy rings remain on the tops of the solder mounds of one
    header row (x 77.0 to 77.2, 1.6 mm2 in all, against 712 mm2 of silver). One pad of the power jack is `#c0c0c0`, lighter than
    the pin silver `#a6a9aa` (the Cadasio project has it so).

## Request by request

### Opening paragraph

**Asked:** more detail without losing a Chromebook: "some PCB parts on the IO module and Nano board, breadboard wires, and
screws look a little too grainy"; an edge "at the top surface of the screw"; wire outlines "thicker than those of other edges".

**Now:**
- Model: 1.35 MB, 147,909 triangles, 63,758 outline segments, 43 parts. Per part, see finding 1.
- Breadboard wires and servo leads are no longer CAD meshes: `core.js` draws each as a 10-sided tube with smooth shading along
  a route, one ring every 1.5 mm (12 to 160 rings), so the old 0.1 mm-simplified cable meshes are gone.
- Screw head: the shipped mesh has an outline ring at radius 2.74 mm, y 96.42, 0.11 mm below the flat top (42 segments,
  17.3 mm round), from the new `fillet_edges_mm: 0.4`. Also rings under the head (y 93.7 and 93.5), at the tip, and the hex
  socket. `parts/6mm-Hex-Screw.png` shows the top rim line.
- Wire outline: a back-face hull pushed out 0.9 drawn pixels (`outlineMaterial`, `width: 0.9`), whatever the zoom; crease
  edges are 1 px lines. The same hull is used on screws and thumb caps.

**Satisfied?** Screw edge: yes. Outline weight: yes by the code. Detail: partly (finding 1). Chromebook: nobody has tried it;
the file is smaller than the one Lee had, and wires are rebuilt on the CPU only while a step animates.

### 1. Regulator under the Nano: silvery pins

Now: mesh `nano - reg` is body `#181818` (148 triangles), both pin ends `#a6a9aa` (724 triangles, 103 mm2, x 65.7 to 74.0), six
print marks `#cccecc`. Colours from the atlas; the pin faces of the body take the skin's colour ("2315 faces under a skin
recoloured"). Satisfied. (Hidden under the Nano in most views.)

### 2. Solder mounds on the Nano

Now: in the shipped Nano, within 1.6 mm above the board at the two pin rows there are 712 mm2 of `#a6a9aa` and 1.6 mm2 of
board navy. `parts/Nano-I-O-Module.png` shows grey mounds round every pin. Satisfied (leftover in finding 11).

### 3. Mini-USB the same silver as the pins

Now: `atlas_colours: {"#cccccc": "pin"}` turns the shell into `pin` = `#a6a9aa` (1,648 triangles; shell and core are one solid).
Recorded under `_notes.decided`. Satisfied; the contacts inside are `#d3d6d3` (finding 11).

### 4. One screw, zoom out, the other five appear, then go in

Now: Step 11 moves NAUO47 alone, close up; Step 12 pulls back to the whole base (radius 139.1) with NAUO48 to 52 hovering
60 mm up, one lead line each, label "5x 6mm Hex Screw"; Step 12c seats all five together. The old "rest" step (eye + "5x",
screws appearing in place) is gone. Satisfied.

### 5. Labels and captions on; part names

Now: `player.js` shows labels unless `?labels=0` and the caption unless `?captions=0`; the step pictures follow the same switch.
Recorded in the rulebook (section 13). Names follow the Cadasio tooltips: Base Motor (motor, horn, plug), Joystick (labels
"Left Joystick" / "Right Joystick"), Nano I/O Module, 6mm Hex Screw, Breadboard Wire (F-F); wood by engraved code. The parts
list has 18 lines with those names. Satisfied, with the gaps in finding 9 and the stale pictures in finding 6.

### 6. Step 2 / 2c / 3

Asked: Step 2 shows R1 and the Base Motor with the double horn fitted and black; 2c angles the horn through R1; R2 appears in
Step 3 and slides over the motor, tabs into R1's slots.

Now: Step 2 shows R1 in place and NAUO45 + NAUO46 hovering 58 mm up, labels "R1" and "Base Motor", one lead line from the
leading horn tip (163.7, 143.8, 125.5) to the far end of the cut-out (163.7, 103.0, 124.3). Horn `#1a1a1a`, moved with the motor
(`PART_OF`). Step 2c plays the path in four beats. Step 3: R2 hovers 71.3 mm up, lines at both legs, caption "Slide R2 over the
base motor so its tabs enter the slots in R1." The old "Insert the base servo into R2" step is gone. Satisfied.

### 7. Servo label pink with white text

Now: on NAUO45 the label plate is `#ff00ff` and the lettering `#ffffff` (40.4 mm2 of white on a 202.5 mm2 plate, no pink and
white face in the same place, so nothing to flicker). It is on the motor's +X face: it faces the camera while the motor
hovers a quarter turn round in Step 2 and through the first beats of 2c; once seated it faces R3, away from the usual camera,
and R2 and R3 soon cover most of it. Satisfied in the model; finding 6 for the part picture.

### 8. Logo

Now: `logo.webp` in the kit folder (the white-on-blue pill, 2000 px wide, 33 KB); `stepgen.py` records it in `meta.logo` and
the title page swaps it for the text badge. Lee attached SVG and PNG; the project holds a WebP copy only. Satisfied.

### 9, 10. R3's and R4's left tab

Now: `lines_at=[[193.6, 96.6, 121.5], [193.6, 96.6, 159.7]]` on R3 and `[[133.6, 96.6, 121.2], [133.6, 96.6, 160.0]]` on R4:
Lee's point plus its mirror on the other leg (CAD tab ranges z 117.7 to 124.0 and 157.2 to 163.5). Satisfied.

### 11. The base motor's wires

Asked: wires present from the start, "maybe sticking straight up", then after R6 moved into R4's slot and "straight out
horizontally past the slot".

Now: three wires (brown `#975100`, red `#bd291f`, orange `#ff9d07`, the colours of the motor's own stubs) from Step 2 on, with
the plug NAUO83 riding on the end. Steps 2 to 8: out of the motor 8 mm, then straight up 52 mm to y 171 (59 mm of lead), clear
of R2 to R6 as they go on. Step 8 ("Move the base motor's wire into the L-shaped slot in R4.", eye on the slot) bends it to
the second route: through the pocket (y 129.2 to 131.4, z 141.2 to 146.5; pocket is y 127.3 to 135.8, z 140.6 to 148.7) and
21 mm straight out past R4's face, heading (-1, 0, 0). No wire's centre line is inside any wood part in any view. Satisfied.
(The videos never show the lead in the slot; this follows Lee.)

### 12. B2, B1 and the screws

- Horn on the motor from Step 2: yes.
- Step 9 / 9c: B2 hovers 80 mm to +Z and slides in at its own height, slot mouth leading, under R6 then R5, horn underneath.
  Caption: "Once R1 - R6 are together, slide B2 in above the servo horn and below R5 and R6, until the motor sits in the round
  cut-out." The horn is drawn 1.8 mm lower than the CAD so that it clears B2 (`adjust_mm`, listed under `_notes.adjusted`).
  Satisfied; lead lines in finding 4.
- Step 10: horn into B1's cut-out, four hand-set lines (two at the horn's tips, two at plate corners). Satisfied; finding 3.
- "The 2 callouts look weird": taken to mean the eye and the "5x" that both pointed at the first screw in the old Step 12
  (the old Step 11 had one lead line and one label). That pair is gone: Step 11 has one lead line and one label, Step 12 five
  lead lines and one label. Satisfied if that is what Lee meant; worth one question, since his sentence is about the first
  screw.
- Punch-in: there, at 2.0x (finding 2).

### 13. Step 9c to Step 10

Now: B1 is the moving part and appears below; nothing else moves in the transition except the camera panning down
(target y 136.5 to 103.8). Satisfied (finding 3 for the caption and the rule).

### 14. The other five screws

Now: Step 12 `offsets` are [0, 60, 0] for NAUO48 to 52 with five lead lines; they go in on 12c. Satisfied.

### 15. Joystick pins

Now: `5x_Ang_Conn_1` is `#a6a9aa` pins (320 triangles) in a `#303030` bar; potentiometer legs and switch legs `#a6a9aa` too.
`parts/Joystick.png` shows silver pins. Satisfied.

### 16. Joystick wires

- Step 15 and 16 (left joystick, on its own): four wires 42 mm long of 106 to 113, ending in mid air with a zigzag drawn twice
  (across the bundle and edge-on). Step 18 and 19 the same for the right joystick (42 of 111 to 117 mm). Lee said "say half";
  it is 36 to 39%.
- Step 17: the module appears lying beside the base (`MODULE_ASIDE` [10, -16.3, 100]) with the left joystick's four wires
  whole, no zigzag, tied to both ends: drawn 192 to 197 mm long while the joystick group hovers, 171 to 177 once seated. Step 20:
  the same for the right joystick (142 to 173 mm). Step 22: all eight follow the module in. No wire passes through wood in any
  resting view.
- Pins, measured at the route ends: left GND (83.13, 136.48) A2 G; 5V (85.62, 136.48) A2 V; X (88.10, 136.48) A2 S;
  Y (88.10, 133.94) A3 S; right GND (83.13, 141.48) A0 G; 5V (85.62, 141.48) A0 V; X (88.10, 141.48) A0 S; Y (88.10, 138.94)
  A1 S. All eight as Lee listed.

Satisfied. Done differently in one respect Lee did not specify: the module is parked on the +Z side (the side it later slides
in from); on video it lies on the other side and is carried across.

### 17. Old Step 23

Now: Step 23, "Reconnect the base motor to 5. Remember brown to G, red to V, and orange to S.", close up on module and R4,
label "5" on the row. The plug swings from the horizontal pose to its seat and the lead changes to the CAD route. Ends:
brown x 49.98 (G, board edge), red 52.52 (V), orange 55.06 (S, Nano side), z 139.36 = row 5. Satisfied.

### 18. Old Step 24

Now: removed. Lee's first option was taken (lead into the slot after R6, new Step 8), not the alternative (keep it up until
plugging in). 25 steps became 24. Satisfied.

### 19. USB cable

Now: Step 24 is a text card, "Connect the power cable to the nano.", with the review note "The power cable is not modelled
yet." As asked.

### 20. Arm and claw

Still to come. Not reviewed.

### 21. Jumper colours

Now: yellow, green, blue, purple on each joystick (GND, 5V, X, Y), the same four colours as before, both joysticks alike.
Satisfied.

### Message 2. The horn through R1

Asked: "move it at a slight angle and rotate the Base Motor and its servo horn into the slot before spinning it 90 degrees
with respect to the z axis and setting it in the slot of R1."

Now (Step 2 / 2c, `horn_way`, stops 0, 1, 6, 7, 8 = four beats of 0.8 s):
1. Hover: motor and horn 58 mm up, already a quarter turn round so the horn runs along the cut-out, tilted 12 degrees, one
   tip 7 mm lower than the other.
2. Straight down 42 mm at that tilt.
3. The low tip dips under the far rim (tilt 16, then 12, 8, 0 degrees while sliding 7.5 mm along the cut-out and coming down
   to 8.5 mm), the motor levels and slides back 6 mm onto the shaft axis.
4. A quarter turn about the shaft (the vertical axis through (163.7, 140.9)), 8.5 mm above its seat.
5. Set down 8.4 mm.

Replayed against the CAD with the player's interpolation: no overlap in the descent, the turn or the set-down; 0.59 mm at
worst during the dip (the trailing horn tip at the end of the notch, (163.64, 102.35, 153.78)), which is the "0.6 mm" the
comment in `guide.py` claims. Recorded in the rulebook (section 13). It matches the build video too (0:18 to 0:22 of Base.mov).
Satisfied; see finding 10 for the pace.

## Seen on the way (not in Lee's notes)

- Step 22 still carries its yellow Review note; the video suggests a tilt at the USB end rather than lifting the whole board
  6 mm (`video_controller_seg2.md`, section 4 item 1).
- Step 23 has a label but no eye icon; the rulebook's wire-step cue is an eye on the wire plus the destination label.
- On video the module goes in before B8; the guide keeps Lee's old order (B8 at Step 21, module at Step 22).
