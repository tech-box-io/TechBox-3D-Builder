RCC Build Instructions (Radio Controlled Car, Full Build: controller, electronics test, chassis, wiring and power)

FIRST DRAFT, 15 Oct 2026. Build instructions generated from Lee's STEP (RCC_Assembly_v1.STEP), TechBox's published Cadasio guide
for the kit (instructions.online/?id=19075-rcc_remote_controlled_car) and Lee's photos and L1 drawing, in the same format as the
MRA guide. Not for distribution. Questions for Lee are yellow Review notes on their steps (switched on for this draft).

HOW TO OPEN (Mac)
1. Double-click "Open Prototype.command". A Terminal window opens and the prototype opens in your browser (port 8796, so it can
   run beside the MRA's). If macOS says it cannot be opened: System Settings > Privacy & Security > "Open Anyway".
2. When you are done, close the Terminal window. No internet connection is needed.
The controls are the MRA guide's (see its README.txt): arrows step through, drag to rotate, scroll to zoom, Option-click a spot to
copy where it is, the grid button shows every step, ?review=0 hides the Review notes.

THE BUILD, AS DRAFTED
- Steps 1 - 6, the controller: the board laid printed side down and the two guards pressed on; turned over; the Nano Board into
  H1 / H2 (USB socket at the end marked USB); the radio module into the NRF24L01 socket; each joystick set into its pocket a few
  millimetres short of its socket and pushed in (L-JS, R-JS). The controller is then put aside.
- Steps 7 - 18, the car's electronics tried on the bench, as on the MRA: the second Nano Board into the I/O module (USB socket at
  the power socket's end), the adapter board onto the module's side pins (U3 at the end away from the power socket), the second
  radio module into U3; a wheel pressed onto each wheel motor; the left motor into LWh (U1) and the right into RWh (U2), brown to
  G; the battery clip onto the 9V battery and the barrel plug into the power socket; the controller back, and its USB cable in;
  a Testing Checklist card (a placeholder); both motors unplugged and everything set aside.
- Steps 19 - 27, the chassis: L1 engraved side down, L2 hooked over the notch at L1's flat end and swung down, L3 (both with the
  car upside down); in the hand, the two motors into L5 and L4 slid along their leads; the block lowered onto L1 the right way up;
  the I/O module, with everything on it, slid in from the front along the grooves in L5 and L4 to L2's fin; L7 and L6 slid in
  from the front with the car turned over (they go in under L1), which lock it.
- Steps 28 - 32, wiring and power: each motor plugged in again (LWh, RWh), the battery down into L3, the barrel plug in, and the
  controller's USB cable in. The Completed View shows the car and the controller.

PUT RIGHT FROM THE PUBLISHED GUIDE
- The car's Nano Board stays on the module (the published guide loses it at its Step 29) and has its USB socket at the power
  socket's end (the published pictures show it reversed).
- The battery is plugged in (never, in the published guide), its clip has a step, and so do the guards and the wheels.
- The joysticks are set down into their pockets and pushed into their sockets (they glided in sideways through the guard).
- The test is complete: power, a checklist, unplug, set aside (the published guide plugged the motors in and stopped).
- One part per step, Step N / Step Nc, a cue on every Step N, captions, labels on every header (H1, H2, NRF24L01, L-JS, R-JS, U3,
  LWh, RWh), the kit never seen from below, a parts list, and the house colours (the I/O module's board navy, the wood #deb887).

WHAT CAME FROM WHERE
- Colours: materials.json and colour-atlas-rcc.json (the MRA's atlas for the parts the two kits share, TechBox's RCC Cadasio
  project where its colours suit). Colours waiting for Lee are under _notes.unconfirmed in materials.json.
- Reused from the MRA, as Lee asked: the Nano Board (the car's Nano is the controller's Nano model, nano-car.glb, because the CAD's
  own car Nano is a plainer model), the I/O module with its colours and printed legend, the joysticks, the Mini-B plug and the
  USB cable's A end (usb-a-end.glb), the servo plug colours.
- Printing (silkscreen.py -> decals.json): the I/O module's legend carried over from the MRA; the adapter board's and the
  controller board's print from Lee's photos (the TechBox logo traced from logo.webp); FRONT etched on L1, and the CAD's own "L1"
  turned the right way and moved onto FRONT's line, as in Lee's drawing (materials.json "move_engraving").
- Wires (wire-paths.json, measured from the CAD's lead bodies): the CAD poses each motor's lead twice (loose, and plugged in) at
  different lengths (68, 107 and 162 mm); here each lead is drawn 115 mm long throughout, on the bench and in the car. A plug
  laid aside lies flat (on the table on the bench; on L1 behind the battery's hole in the car). The battery clip's lead is the CAD's
  (about 30 mm). The USB cable is drawn between the Mini-B end and the A end lying on the table beyond the controller's grips.

QUESTIONS FOR LEE (also on the steps as Review notes)
 1. Power for the test: the 9V battery for the car and USB for the controller, as drafted? Or USB for both (two cables)?
 2. TechBox's RCC Testing Checklist, word for word (Step 17 has a placeholder). Which joystick drives which wheel? Does the
    FS90R's stop trim need setting in the test?
 3. Wheels on for the test (as drafted, and as published), or pressed on at the end of the build?
 4. L2 in one step with the hook-and-swing (as drafted) or two?
 5. L4 and the plugs: one step (as drafted) or a step per plug through L4?
 6. The barrel plug at the end: plugged in (as drafted) or left out with a caution?
 7. Colours: the FS90R case (blue as published, or black?), the signal wire (yellow, as the CAD and the published guide; the
    MRA's captions say orange), the radio boards (black or green), the wheels, the plug housings, silver or gold pins, the white
    boards. And is the RCC's I/O module the same board as the MRA's (its printing is carried over on that assumption)?
 8. Names (Controller Board, Left / Right Controller Guard, Nano Board, Radio Module, Joystick, USB Cable, Nano I/O Module,
    Adapter Board, Wheel Motor, Wheel, 9V Battery, Battery Clip, L1 - L7).
 9. The car's Nano Board: USB socket at the power socket's end (as drafted; the published pictures show it the other way)?
10. The joysticks: the CAD's joystick board overlaps the controller board by 4 mm, so it clips the board as it is set down. How
    does it really sit, and do its pins go into the top row of L-JS / R-JS?
11. The guards: the CAD has two trays pressed on under the board; the photo shows four rim pieces. How do they go on, and first?
12. L1's etching: FRONT at the front-left corner and L1 at the front-right, as in the drawing, on the top face (as drafted)?
13. L6 / L7: their codes are on the parts under L1, so they cannot be read from above. Engrave them on the heads instead?
14. Lead lengths: how long is the FS90R's lead, and the battery clip's lead?
15. Section cards with your two photos (the controller's and the adapter's pin names) before Steps 3 and 8?
16. Should the Completed View show the controller with its USB cable in (as drafted and as published)?
17. The kit's name: "Radio Controlled Car (RCC)" as you wrote it (as drafted), or "Remote Controlled Car (RCC)" as the published guide has it?
18. Which way round do L3, L4, L5 (nearly symmetric) and L6 / L7 go? If it matters, the captions can say "code facing the front"
    or "code facing out", as on the MRA. And which face of the real L4 carries its code (the CAD's faces L5)?

CAD POINTS (docs/research/rcc/cad_study.md section 4)
The joystick overlaps the controller board and sits in the guard's floor; the controller board is modelled 2.6 mm thick; the
sockets are solid blocks (every plug-in direction is set by hand in guide.py); the I/O module's reset button clips L4 / L5 by
0.3 mm as it slides in; the adapter's sockets sit up to 0.9 mm off the module's pins; there is no car USB cable (a Mini-B plug in
the car's Nano would run into the battery).

FILES
  guide.py                      the build, in order (edit here, then run it: see CLAUDE.md "Commands" with this folder's name)
  materials.json, colour-atlas-rcc.json   colours and detail
  wire-paths.json               the leads' centre lines and the plugs, measured from the CAD
  silkscreen.py -> decals.json  the printing on the boards and FRONT on L1
  rcc.glb                       the CAD (converted from RCC_Assembly_v1.STEP); nano-car.glb, usb-a-end.glb: extra parts
  player.html, js/, vendor/, logo.webp, parts.html   the viewer (the same as the MRA's)
  steps.json, parts.json, model.glb, model.report.json, parts/   generated; do not edit by hand
Research: docs/research/rcc/ (cadasio_study.md, cad_study.md, reuse_and_colours.md, cad_wire_paths.md, silkscreen.md,
materials_notes.md, review_v1.md).
