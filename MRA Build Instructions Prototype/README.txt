MRA Build Instructions Prototype (Full Build: electronics test, base, controller, arm, claw, T1 / T2 block)

Build instructions generated from the SolidWorks model (STEP export), the MRA build notes and the four build videos, as a possible Cadasio replacement. Not for distribution.

HOW TO OPEN (Mac)
1. Double-click "Open Prototype.command". A Terminal window opens and the prototype opens in your browser.
   If macOS says it cannot be opened: open System Settings > Privacy & Security, scroll down, and click "Open Anyway" next to "Open Prototype.command". (On older macOS: right-click the file and choose Open.)
   If macOS asks to install command line developer tools, click Install, then double-click the file again.
2. When you are done, close the Terminal window.
No internet connection is needed: the viewer (with its 3D library) is the one copy in ../player/, shared by every kit;
"Open Prototype.command" serves it with this kit's files.

HOW TO USE
- After the title page, the Parts List pages show every part of the kit, grouped by kind, with how many of each. Click a part (or Tab to it and press Enter) to see its picture large; Escape or the cross closes it.
- Arrow buttons (or the left and right arrow keys; Home and End for the first and last view) step through. "Step N" shows the new part hovering, with red lead lines from its joints to the slots or holes they go into. "Step Nc" shows it in place.
- Drag to rotate, scroll to zoom. Labels stay where they are while you rotate; only their pointer follows the part. The next step always opens on its own view again.
- The instructions are in a box at the top left. The round speaker button reads them aloud (the browser's own voice: nothing is downloaded); press it again to stop. An orange Caution box under them marks a step where it is easy to go wrong.
- Everything works from the keyboard: Tab moves between the buttons, Enter or Space presses one. A screen reader is told each step as it opens (its name, the instructions, any caution and the labels).
- Rest the pointer on a part (or a wire) to see its name. Click it to pick it out: it turns orange and its name stays up until the next click or step.
- The grid button (or "View all steps" in the step list) shows a picture of every step. Click one to jump to it.
- Review notes (yellow) are switched off for this guide now that it is past review (guide.py, review_notes=False); add ?review=1 to the address to see any that are left.
- Hold Option (Alt) and click a spot on a part to note where it is: the step, the part and the spot's position are listed at the bottom right and copied to the clipboard. Paste that into a message to say exactly where a lead line should start or end. (Only when the player is opened directly, not when it is embedded in another page.)
- The round-arrow button at the top right, beside full screen, puts the camera back to the step's own view after turning or zooming it (Lee, 16 Oct 2026).
- Pointing at or clicking a joystick names it Left Joystick or Right Joystick, as its labels do (the parts list counts them as 2 Joysticks).
- In the step list, each Parts List page is pictured as the page itself, small (on trial, Lee 16 Oct 2026). The wood parts' bands in the parts list are blue-grey, so the wood stands out (they were orange).
- The wording of every step can be edited in a spreadsheet: tools/step_text.py exports it (share/MRA step text 2026-10-16/) and imports an edited copy into step-text.json, which guide.py applies.
- Address options: ?labels=0 hides part-name labels, ?captions=0 hides the caption line, ?review=0 hides review notes, ?quality=low for a very slow computer, ?step=12 opens at a given view.

PART IMAGES (for the parts list in the LMS)
- The parts folder holds one picture per part (500 x 500 px PNG, transparent background) plus parts.csv and parts.json listing name, quantity and image file. A motor is pictured with the horn it arrives with. A wire that comes as a part of the kit is pictured whole: the breadboard wire (F-F) straight, with a cap at each end in line with it (Lee, 15 Oct 2026); the servo extension wire with its coupler and its plug. T2 is pictured with its engraved code the right way up.
- To see them or download them as one zip, open parts.html the same way as the player (replace player.html with parts.html in the address). Add ?size=1200 for larger pictures or ?bg=white for a white background.

WHAT TO LOOK AT
- Final positions come straight from the CAD. Insertion directions are calculated from the geometry: a direction is used only if the part can slide that way without passing through anything already built.
- Lead lines are placed automatically: the CAD is searched for places where the moving part and the parts it joins grip each other (a tab in a slot, a board edge in a groove, a screw in a hole), and a line is drawn from the feature on the moving part to the one that receives it. At most four per step, as in the published guides. Where a step's lines are not the ones wanted, they are set by hand in guide.py (lines_at=[...], using points picked with Option-click).
- Each step adds one part or does one thing. Sub-assemblies built in the hand (each joystick between its two walls; the upper arm, the lever and the claw) are shown on their own, then brought to the model.
- The base motor's horn does not fit straight through R1. Step 19c shows what the hands do: the motor is turned a quarter turn so the horn runs along the cut-out, one arm of the horn dips under the rim at a slight angle, the motor levels out, turns back a quarter turn about its shaft and is set down. The path was searched for against the CAD so that nothing passes through R1.
- A set of identical screws: the first is shown close up going in; the next step pulls back, the others appear above their holes and go in together (decided 13 Oct 2026).
- Steps 1 - 18 are an electronics test on the bench before anything is built: the Nano Board onto the I/O module, each joystick wired to the module one wire at a time, the four motors plugged into their rows (the claw motor straight onto row 10), the USB cable (the kit's only power), TechBox's Testing Checklist (its last line: unplug the USB cable), then all four motors unplugged in one step, with a caution to set them and the module aside. The module and joysticks lie as they will in the robot (the CAD's own jumper routes); the motors stand in a row beside the module. Everything is then put aside until the build needs it.
- Wires are drawn by the player along routes taken from the CAD, so they can move: a motor's lead stands clear with its plug on the end until its slot is built, moves into the slot, and is plugged into its row at the end of its section. The joysticks arrive wired to the I/O module: while a joystick is in the hand its four wires fade out a little way from it (they carry on to the module, which is not shown); once it is on the base the module lies beside the base with the wires whole, and they follow the module as it slides into place.
- Work done with the kit upside down is shown with the model turned over: B2 and B1 on the base, and the whole claw (built upside down, as on the video). The model turns over, and back, as the step opens.
- The camera prefers the side from which the engraved code of each wood part going on can be read.
- Wiring as built here (read from the board's printed legends on video, and the same as in TechBox's Cadasio project): left joystick GND - A2 G, 5V - A2 V, X - A2 S, Y - A3 S; right joystick the same on A0 and A1; base motor on row 5, elbow motor on 6, shoulder motor on 9, claw motor on 10 through the servo extension wire; brown to G, red to V, orange to S.
- CAD names do not match the engraved codes on 26 of the 44 wood parts (CAD B10 = B3, B8 = B7, B9 = B8, R5 / R6 swapped, and most of the arm and claw: the engraved arm set is A1 to A13 with A9 twice). Labels and captions follow the engravings. Matching names in the CAD would remove this manual step. The table is in docs/research/mra/cad_codes_base.md.
- Colours follow TechBox's own Cadasio project for the MRA, solid by solid (colour-atlas-mra.json), with TechBox's decisions over the top in materials.json: pins, solder mounds and the mini-USB shell are one silver; servo labels are pink with white lettering; horns are black; every pin-header base on the I/O module is yellow; the I/O module's board is the Nano's navy (Lee, 14 Oct 2026). Outline edges are drawn where two faces meet at more than 40 degrees, the same value as Cadasio's Toon setting, plus the rounded rims of screw heads.
- Two corrections to the CAD (materials.json, "adjust_mm"): the base motor's horn is drawn 1.8 mm lower than the CAD has it, where its arms sit inside B2 (on the real kit they lie in B1's cut-out and B2 slides over them); and R8 is turned end for end, so that its notch is over the elbow motor's lead, as on R7, with its engraved code moved into the band above the notch and turned the right way up ("move_engraving").
- Kit additions to the CAD (materials.json): the Nano Board is a part of its own (in the CAD it is inside the I/O module), and the Elbow, Shoulder and Claw Motors carry a round sticker, 7 mm, on both wide faces, in the middle of the part of the face that shows (clear of R7 / R8): black, white and blue.
- The T1 / T2 block is built last, in the hand, before the finished model.
- The USB cable comes from Lee's two STEP files (cad_extra/), converted into usb-mini-b.glb and usb-a-end.glb and placed by materials.json "extra_parts": the Mini-B end plugs into the Nano Board (in the electronics test and again at the end), the A end lies on the table, and the cable between them is drawn by the player. The STEP files carry no colours: black with silver metal, as noted in materials.json.
- The title page uses the camera of Lee's screenshot of 14 Oct 2026, and the Completed View the same, centred; on windows narrower than they suit, both fall back to the front view on the R5 side. A clicked part turns orange.
- The I/O module carries its silkscreen (pin names, G V S, A0 - A7, POWER, RESET, the capacitor's and the regulator's print), taken from photos of the real board and placed on the CAD's pins (silkscreen.py writes decals.json, build_model.py puts it in the model as data and the player draws it, so the model file grows by a few kB, not by a picture).
- Cameras Lee sent as screenshots on 14 Oct 2026 (Steps 39, 52, 56, 57; Steps 66 and 67 are the same two on the other side) were reproduced by matching renders to the pictures.
- The arm check (Step 76) is one view: A13 and A12, whose far ends are free until the claw goes on, jiggle a little about their screws as it opens. The claw step that slides C8 in (Step 88c) has a close-up of the two gears as if C9 were not there.
- The USB cable stays in the Completed View, its A end lying on the table off the far corner of the base, where that view can see it.
- The I/O module's board is the Nano's navy. In Step 97 the servo extension wire goes over the top edge of R4 and, as the join goes down behind R4, down the narrow stem of R4's L-shaped slot turned on edge (it is wider than the stem is), then across into the pocket. From then until Step 100 it keeps the length it has as Step 97 opens (Lee, 15 Oct 2026): it goes down onto B2 and rightwards along it past R6's front edge, its plug lying flat at the foot of R6 under the shoulder motor's lead. In Step 100 the plug lifts from there, turns upright under the shoulder motor's wire beside the module, goes across above the joysticks' wires and down onto row 10, the wire following stage by stage. Steps 98 and 99 take the elbow and shoulder plugs to rows 6 and 9 the same way, in three beats (Lee, 15 Oct 2026): off the hook (the elbow plug drawn up to the top of the arch that the base motor's lead makes, the way its own lead lies; the shoulder plug with a quarter turn, since it hangs on its hook the other way round), upright over the row where the lead comes straight down to it (the elbow plug over that arch), and down onto the row. The elbow motor's lead goes over the base motor's lead to row 6, as on the real build (Lee, 15 Oct 2026); the CAD has it passing under that lead. Checked frame by frame, forwards and backwards: the wire passes through no part and no other wire. Going back from either step plays it backwards (straight back, the wire would cut through what it was laid round).
- Not modelled yet: moving joints (the arm is always shown in the CAD's pose; the jiggle is a cue, not the linkage moving).

FILES
What the browser loads:
  ../player/                    the viewer (player.html, js/, vendor/), shared by every kit
  steps.json                    the steps (generated)
  model.glb                     the 3D model for the web (generated: a few MB instead of 42 MB; only the parts this guide shows)
  logo.webp                     the title-page logo
  parts.html, parts/            part images
What they are generated from:
  mra.glb                       the 3D model converted from the STEP export (full detail)
  guide.py                      the build, in order: which part goes on next, the caption, any hand-set motion, the wires
  materials.json                colours and how much detail to keep, per part
  colour-atlas-mra.json         the colour of every solid in TechBox's Cadasio project for this kit
  wire-paths.json               the centre line of every wire in the CAD, the plugs and the leads
  engraved-codes.json           the code engraved on each wood part: which way it faces and where it is
  silkscreen.py, decals.json    the I/O module's printing (silkscreen.py writes decals.json; build_model puts it in the model)
Regenerating (from the project folder, one level up; see CLAUDE.md there):
  python "MRA Build Instructions Prototype/guide.py"                 after changing guide.py
  python tools/build_model.py "MRA Build Instructions Prototype"     after changing materials.json or mra.glb
_v1 holds the first version of the prototype's files for reference.
