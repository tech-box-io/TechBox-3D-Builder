RCC Build Instructions (Remote Controlled Car, Full Build: controller, electronics test, chassis, wiring and power)

FIRST DRAFT 15 Oct 2026, LEE'S FIRST ROUND 16 Oct 2026. Build instructions generated from Lee's STEP (RCC_Assembly_v1.STEP),
TechBox's published Cadasio guide for the kit (instructions.online/?id=19075-rcc_remote_controlled_car) and Lee's photos and L1
drawing, in the same format as the MRA guide. Not for distribution. Questions for Lee are yellow Review notes on their steps
(switched on for this draft).

HOW TO OPEN (Mac)
1. Double-click "Open Prototype.command". A Terminal window opens and the prototype opens in your browser (port 8796, so it can
   run beside the MRA's). If macOS says it cannot be opened: System Settings > Privacy & Security > "Open Anyway".
2. When you are done, close the Terminal window. No internet connection is needed.
The controls are the MRA guide's (see its README.txt): arrows step through, drag to rotate, scroll to zoom, Option-click a spot to
copy where it is, the grid button shows every step, ?review=0 hides the Review notes.

THE BUILD (step numbers as since 16 Oct 2026: the guard and wheel steps are gone, a step was added before the motors come out)
- Steps 1 - 4, the controller (its guards come fitted): the Nano Board into H1 / H2 (USB socket at the end marked USB); the radio
  module into the NRF24L01 socket; each joystick set into its pocket a few millimetres short of its socket and pushed in (L-JS,
  R-JS). The controller is then put aside.
- Steps 5 - 15, the car's electronics tried on the bench, as on the MRA: the second Nano Board into the I/O module (USB socket at
  the power socket's end), the adapter board onto the module's side pins (U3 at the end away from the power socket), the second
  radio module into U3; the left motor (wheel fitted) into LWh (U1) and the right into RWh (U2), brown to G; the 9V adapter onto
  the 9V battery and its barrel plug straight into the power socket; the controller back, and its USB cable in; a Testing
  Checklist card (a placeholder); the battery and its 9V adapter unplugged and set aside as one; both motors unplugged and
  everything set aside.
- Steps 16 - 24, the chassis: L1 engraved side down, L2 hooked over the notch at L1's flat end and swung down, L3 (both with the
  car upside down); in the hand, the two motors into L5 and L4 slid along their leads; the block lowered onto L1 the right way up,
  the leads up out of L1's notches and straight back along it; the I/O module, with everything on it, slid in from the front along
  the grooves in L5 and L4 to L2's fin; L7 and L6 slid in from the front with the car turned over (they go in under L1).
- Steps 25 - 29, wiring and power: each motor plugged in again (LWh, RWh), the battery down into L3, the barrel plug in, and the
  controller's USB cable in. The Completed View shows the car and the controller.
  (Old to new: Steps 3 - 9 are now 1 - 7, 12 - 17 are 8 - 13, 18 - 32 are 15 - 29; Step 14 is new.)

LEE'S FIRST ROUND (16 Oct 2026), done
- Model: the battery in Amazon Basics colours (amber, slate band, dark top; no lettering); the radio modules' antenna trace gold;
  both Nano Boards from the MRA's export of the Nano model (the RCC's had grey sliver triangles beside the processor), with a
  3.5 mm dot sticker on each processor, white on the controller's, blue on the car's; the adapter board's 2-pin socket over the
  module's 3V3 / GND pins moved 0.94 mm to sit on them; the wheel motors' leads brown / red / orange (the MRA's orange) and their
  cases outlined at the rounded corners; the 9V adapter's two wires start and end at the ends of its stubs on the clip and the plug.
- Guide: guards fitted to the controller board and wheels to the wheel motors (no steps; one part each in the parts list); the
  controller's band of the parts list holds 1 Nano Board, 1 radio module, 2 joysticks (the car's Nano Board, in the Electronics
  band, has its own picture with its blue dot: parts/Nano-Board-car.png); wood bands blue-grey as the MRA's; no
  labels on H1 / H2, NRF24L01, L-JS / R-JS, U3, LWh / RWh; hover names Left / Right Joystick and Left / Right Wheel Motor as their
  labels; "9V Adapter" for the battery clip; Step 10's arrow turned to the camera; the battery and barrel plug set down so the plug
  goes straight in (bench and car); the new Step 14 (battery and adapter off as one); the leads up out of L1's notches (they ran
  through L1) and straight back; the right plug carried over the left one on its way to RWh; L1's label on its round end and a
  third red line from L2's hook to the notch (Step 16).
- Cameras: Steps 6 and 7 from the opposite upper corner; Steps 16, 23, 27 and 28 solved from Lee's screenshots (Steps 27 / 28 let
  down 4% so the battery clears the caption and its label fits above it); Steps 25 and 26 closer in. Every other step keeps its
  camera (Steps 8 - 11 included, where the content changed).

PUT RIGHT FROM THE PUBLISHED GUIDE
- The car's Nano Board stays on the module (the published guide loses it at its Step 29) and has its USB socket at the power
  socket's end (the published pictures show it reversed).
- The battery is plugged in (never, in the published guide), and its 9V adapter has a step.
- The joysticks are set down into their pockets and pushed into their sockets (they glided in sideways through the guard).
- The test is complete: power, a checklist, unplug, set aside (the published guide plugged the motors in and stopped).
- One part per step, Step N / Step Nc, a cue on every Step N, captions, the kit never seen from below, a parts list, and the house
  colours (the I/O module's board navy, the wood #deb887).

WHAT CAME FROM WHERE
- Colours: materials.json and colour-atlas-rcc.json (the MRA's atlas for the parts the two kits share, TechBox's RCC Cadasio
  project where its colours suit). Colours waiting for Lee are under _notes.unconfirmed in materials.json.
- Reused from the MRA, as Lee asked: the Nano Board (both RCC Nanos are the MRA's export of the Nano model, nano-mra.glb, cut by
  tools/cut_part.py: the CAD's own car Nano is a plainer model, and the RCC's export of the controller's has sliver triangles), the I/O module with its colours and printed legend, the joysticks, the Mini-B plug and the
  USB cable's A end (usb-a-end.glb), the servo plug colours.
- Printing (silkscreen.py -> decals.json): the I/O module's legend carried over from the MRA; the adapter board's and the
  controller board's print from Lee's photos (the TechBox logo traced from logo.webp); FRONT etched on L1, and the CAD's own "L1"
  turned the right way and moved onto FRONT's line, as in Lee's drawing (materials.json "move_engraving").
- Wires (wire-paths.json, measured from the CAD's lead bodies): the CAD poses each motor's lead twice (loose, and plugged in) at
  different lengths (68, 107 and 162 mm); here each lead is drawn 115 mm long throughout, on the bench and in the car. A plug
  laid aside lies flat (on the table on the bench; on L1 behind the battery's hole in the car). The 9V adapter's lead is the CAD's
  (about 30 mm) in the car, longer on the bench. The USB cable is drawn between the Mini-B end and the A end lying on the table beyond the controller's grips.

QUESTIONS FOR LEE (also on the steps as Review notes; step numbers as now)
 1. Power for the test: the 9V battery for the car and USB for the controller, as drafted? Or USB for both (two cables)?
 2. TechBox's RCC Testing Checklist, word for word (Step 13 has a placeholder). Which joystick drives which wheel? Does the
    FS90R's stop trim need setting in the test?
 3. (Answered 16 Oct 2026: the wheels come fitted to the wheel motors.)
 4. L2 in one step with the hook-and-swing (as drafted) or two?
 5. L4 and the plugs: one step (as drafted) or a step per plug through L4?
 6. The barrel plug at the end: plugged in (as drafted) or left out with a caution?
 7. Colours still open: the FS90R case (blue as published, or black?), the radio boards (black, as drafted, or green), the wheels,
    the plug housings, silver or gold pins, the white boards. And is the RCC's I/O module the same board as the MRA's (its
    printing is carried over on that assumption)? (Answered 16 Oct: the signal wire is orange; the battery is the Amazon Basics.)
 8. (Answered 16 Oct: "Controller Board" with its guards, "9V Adapter", the rest as drafted.)
 9. The car's Nano Board: USB socket at the power socket's end (as drafted; the published pictures show it the other way)?
10. The joysticks: the CAD's joystick board overlaps the controller board by 4 mm, so it clips the board as it is set down. How
    does it really sit, and do its pins go into the top row of L-JS / R-JS?
11. (Answered 16 Oct: the guards come fitted to the controller board.)
12. L1's etching: FRONT at the front-left corner and L1 at the front-right, as in the drawing, on the top face (as drafted)?
13. L6 / L7: their codes are on the parts under L1, so they cannot be read from above. Engrave them on the heads instead?
14. Lead lengths: how long is the FS90R's lead (drawn 115 mm), and the 9V adapter's?
15. Section cards with your two photos (the controller's and the adapter's pin names) before Steps 1 and 6?
16. Should the Completed View show the controller with its USB cable in (as drafted and as published)?
17. (Answered 16 Oct 2026: the title is "Remote Controlled Car (RCC)".)
18. Which way round do L3, L4, L5 (nearly symmetric) and L6 / L7 go? If it matters, the captions can say "code facing the front"
    or "code facing out", as on the MRA. And which face of the real L4 carries its code (the CAD's faces L5)?
19. (Answered 16 Oct: yes, the car's Nano Board has its own picture with the blue dot, in the Electronics band.)

CAD POINTS (docs/research/rcc/cad_study.md section 4)
The joystick overlaps the controller board and sits in the guard's floor; the controller board is modelled 2.6 mm thick; the
sockets are solid blocks (every plug-in direction is set by hand in guide.py); the I/O module's reset button clips L4 / L5 by
0.3 mm as it slides in; the adapter's 2-pin socket sat 0.9 mm off the module's 3V3 / GND pins (moved: materials.json adjust_mm); there is no car USB cable (a Mini-B plug in
the car's Nano would run into the battery).

FILES
  guide.py                      the build, in order (edit here, then run it: see CLAUDE.md "Commands" with this folder's name)
  materials.json, colour-atlas-rcc.json   colours and detail
  wire-paths.json               the leads' centre lines and the plugs, measured from the CAD
  silkscreen.py -> decals.json  the printing on the boards, the radios' gold antenna and FRONT on L1
  rcc.glb                       the CAD (converted from RCC_Assembly_v1.STEP); nano-mra.glb, usb-a-end.glb: extra parts
  logo.webp                     the title-page logo (the viewer is the one copy in ../player/, shared with the MRA)
  steps.json, parts.json, model.glb, model.report.json, parts/   generated; do not edit by hand
Research: docs/research/rcc/ (cadasio_study.md, cad_study.md, reuse_and_colours.md, cad_wire_paths.md, silkscreen.md,
materials_notes.md, review_v1.md).
