MRA Build Instructions Prototype (Chapter 2: Base and Controller)

A test of build instructions generated from the SolidWorks model (STEP export) and the MRA build notes, as a possible Cadasio replacement. Not for distribution.

HOW TO OPEN (Mac)
1. Unzip the folder.
2. Double-click "Open Prototype.command". A Terminal window opens and the prototype opens in your browser.
   If macOS says it cannot be opened: open System Settings > Privacy & Security, scroll down, and click "Open Anyway" next to "Open Prototype.command". (On older macOS: right-click the file and choose Open.)
   If macOS asks to install command line developer tools, click Install, then double-click the file again.
3. When you are done, close the Terminal window.
An internet connection is needed (the 3D viewer library loads from the web).

HOW TO USE
- Arrow buttons (or the left and right arrow keys) step through. "Step N" shows the part hovering with red guide lines; "Step Nc" shows it in place.
- Drag to rotate, scroll to zoom. The grid button lists all steps.
- Yellow "Review" notes mark steps where the motion could not be calculated from the CAD and was set by hand. Untick "Review notes" to hide them.

WHAT TO LOOK AT
- Final positions come straight from the CAD. Insertion directions were calculated from the geometry for 13 of 17 piece moves.
- Set by hand: screws (they overlap the wood in the CAD because they thread in), both joysticks (the joystick model overlaps its walls), and the extension module's drop onto B4.
- CAD names do not match the engraved names on the parts: CAD B10 = B3, B8 = B7, B9 = B8, and R5/R6 are swapped. Labels follow the engravings. Matching names in the CAD would remove this manual step.
- The STEP export had no colors; parts were colored by name.

FILES
player.html (the viewer), steps.json (the generated steps), mra.glb (the 3D model converted from the STEP), analyze.py (the script that calculates insertion directions).
