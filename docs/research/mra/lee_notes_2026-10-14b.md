# Lee's feedback of 14 Oct 2026 (second round: "the first comprehensive review"), and what was done

Lee's images for this round are in `lee_images_2026-10-14b/`: 7 - 10 are cameras wanted (Steps 40, 53, 57 and 58 in the old
numbering), 11 - 13 photos of the real I/O module (angled, underside, top), 14 - 16 parts-list pages from TechBox's
published Cadasio guides.

## Step numbers: old (Lee's) to new

Two cards were removed (old Step 18, the USB card; old Step 91, the jaw-check card) and old Step 19 became a 3D step.

| Old | New |
|---|---|
| 1 - 17 | 1 - 17 (unchanged) |
| 18 (card "Disconnect the Mini-USB cable") | removed |
| 19 (card "disconnect all servos") | 18, now a 3D step: the four plugs lift off their rows |
| 20 - 90 | 19 - 89 (one less) |
| 91 (card "Check that the two jaws ...") | removed |
| 92 - 106 | 90 - 104 (two less) |

Parts List pages come before Step 1 (they are not numbered steps).

## The requests, one by one (old numbers in brackets)

| Request | Done |
|---|---|
| Speaker icon to read the instructions | A round speaker button in the caption box (and on note cards) reads the caption and caution with the browser's own speech (`speechSynthesis`): nothing to download, so loading is unchanged. Shorthand is spelled out for the voice ("R1 to R6", "I O module", "6 millimetre"). Pressing it again stops; a new step stops it. Hidden in a browser without speech. |
| Buttons work from the keyboard | They were real buttons already; now with a visible focus ring, titles naming the keys, Home / End for the first / last view, the step list's dialog keeps Tab inside it while open, and focus moves to the other button when the one in use turns off at either end. |
| On-screen text readable by a screen reader | Each step is announced as it opens (name, number, caption, caution, labels); the 3D view has a text description; labels drawn in SVG are hidden from the reader (they are in the announcement instead); the parts list is a real list; the close-up has alt text. |
| Remove Step 18 | Done. The checklist's last line already says to unplug the USB cable; the cable is simply not on the bench after the checklist. |
| Step 19: show the servo wires coming off the I/O module; no "before you start the build" | New Step 18: "Unplug all four servo motor wires from the I/O module." The four plugs lift straight up off their rows (one step for four plugs, as asked), with an eye on the plugs. |
| Step 19: caution to set the servos and module aside | "Set the servos and the I/O module aside for now. You will use them again in a bit." |
| Parts list at the start, styled like the examples | Three pages after the title page: Electronics / Motors / Screws; R, B and T wood; A and C wood. The 8 breadboard wires are listed too (pictured as one wire with its two caps; the LMS list in parts/ has them now as well). One band per kind of part: quantity, a tag over the name (screw size, motor dot), the part picture at the end of the band with a halo in the band's colour, an icon and colour per kind. Built from the parts the guide shows, so a guide for one part of the build gets its own list. |
| Caption ~15% bigger, in an enclosing box | 16 to 18.4 px (17.2 px on a phone, where the box would otherwise fill half the screen), in a box with a blue border (was a blue bar beside it). |
| Step 27 (26): arrow instead of lead lines, in the half-moon cut-out | A fat red arrow from the round end of B2's slot out through its mouth, the way B2 slides. |
| Step 28 (27): caution about the horn and B1 | "If the servo horn is not lined up, you may need to adjust it so that it fits in the B1 slot." |
| Step 33 (32) and 36 (35): the joystick's wires stay connected; name its pins | Caution: "The joystick's breadboard wires stay connected to the I/O module: just place the joystick for now. The left joystick is the one wired to A2 G, A2 V, A2 S and A3 S." (the right one: A0 G, A0 V, A0 S and A1 S). |
| Step 38 (37): B6 must not clip the left joystick's wires | The wires did pass through B6's low middle bar about half-way down (checked by ray tests). Now the step reads "Hold the left joystick's wires up out of the way, then place B6 and B7 onto B3": the wires are held up in an arch as the step opens and laid back down as the group seats. Checked: no contact at any point of the move. |
| Each step resets to its own camera | The player always moves the camera to the step's own view (swinging there when stepping, at once when jumping), even when two steps share a camera and the viewer had turned it. No camera was changed by this. |
| Step 40 (39): module up a little to clear B4's tab; camera of image 7 | B4's end lip stands 3.1 mm above the board's underside and the module's 3 degree tilt was about its leading edge, so that edge went through the lip. Now the module comes in lifted 3.4 mm, tips about its leading edge as it reaches the slots in the B6 so its far end stays over the lip, and levels out at the end: the lip is cleared all the way (checked at 21 points of the move). In the CAD the slots in the B6 fit the board exactly, so the tipped board grazes their tops by up to 2.2 mm; clearing both is not possible with the CAD's exact fit. Camera of image 7: solved by matching renders to the screenshot. |
| Step 41 (40): caution, brown to G | "Very important: the brown wire goes on G, the pin nearest the edge of the board." |
| Elbow Motor's black dot a little more grey | #1a1a1a to #5a5a5a (`sticker_grey`); still called the Black Dot. |
| "(Colour Dot)" on the motors' labels | Elbow Motor (Black Dot), Shoulder Motor (White Dot), Claw Motor (Blue Dot) on every label of those motors (bench test, the motors going in, the final wiring); the parts list shows the dot as the motor's tag. |
| Step 53 (52), 57 (56), 58 (57): cameras of images 8, 9, 10 | Solved by matching renders to each screenshot. Step 56 looks up from below, so the lower R8 screw is seen going into its hole. |
| Steps 67 and 68 (66, 67): the same as 57 and 58 | The same two cameras mirrored onto the R6 side (z = 140.6 is half-way between R5 and R6; the second R7 screw is the lower one, as on R8). |
| Step 74 (73): lower the shoulder motor's wire | The CAD's lead arcs up over R6's lobe, about 13 mm above the screw's path, so on screen the screw ran through it. The lead now hangs down between the back of the motor and the hook-shaped slot, 28 mm below the screw's path where it passes it, clear of every part (ray-tested in every view that shows it). The same lead is used from Step 67c to the end. |
| Step 77 (76): copy 76c and jiggle A11 and A12 | A 3D step with Step 75c's camera and an eye on A12: A11 rocks 1.5 degrees about the R6 - A11 screw (taking its screw on A10 with it; A11 lies over that joint, so it does not come apart) and A12 6 degrees about its screw on A10, twice, whenever the step opens (stepping, going back or jumping) and again on Next. The caption is the old card's text. (A cue only: the arm's linkage is not modelled, and with it A11 cannot really move on its own.) |
| Step 87 (86): caution about the horn and C7 | "If the servo horn is not lined up, you may need to adjust it so that it fits in the C7 slot." |
| Step 89c (88c): x-ray close-up of the gears | A framed close-up beside the model (the house style for a picture with a lead line to it, rather than a cloud shape), drawn as the view opens, with C9 left out, seen square-on to the gears: a blue leader and ring to where the teeth meet, a thin red box round it, "Seen without C9" under it. |
| Remove Step 91 | Done. |
| Step 98 (96): caution about wire colours; no eye | "Check that the wire colours match across the join: brown to brown, red to red and orange to orange." The eye is gone. |
| Steps 100 - 102c (98 - 100): labels unreadable over the module | Every label now sits on a white box: unseen in white space, so it shows only where a label has to lie over the model (these steps, and a few close-ups such as Step 40's Row 5), where it makes the text readable. |
| USB cable in the Completed View | Shown. Straight back from the module it was hidden behind the base, so its A end now lies on the table off the far corner of the base, along the arm, where that view sees it (the USB step's camera, Step 101, kept as it was). |
| The I/O module's silkscreen | From the three photos, placed on the CAD's pins: G / V / S beside each block of rows, the digital row numbers 13 - 0 with TX / RX (AREF and GND upright), A0 - A7 with G / V / S, the small headers (RX TX 5V GND, SCL SDA 5V GND, 3V3 / GND), POWER, RESET, outlines round the edge holes, "CS 47 35V" on the capacitor and "AMS1117" on the regulator; the underside's pin names too. `silkscreen.py` writes `decals.json`; `build_model.py` puts it into `model.glb` as data and the player draws it, so the model file grows only by that text (a few kB), not by a picture. |

## Checks

- Every view's camera compared with steps.json from before the round: only the steps Lee named changed (and the two new
  3D steps, which were cards).
- `_runthrough()`: 212 views forwards, backwards and by jumping, 0 problems (now also checking arrows, close-ups,
  cautions and the parts list).
