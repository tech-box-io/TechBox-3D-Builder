Scripts behind Lee's third round (20 - 21 Oct 2026), kept as they were run (paths made relative; pickles go to the system's temporary
folder). Run from the repository's top folder with .venv.nosync/bin/python. Each loads the kit's guide or model: one at a time.

probe.py       guide.py's definitions up to a marker, with a stub Guide holding the real model (for experiments).
proj.py        assembly points projected as the player does (fov 45, padding 1.08), with the caption box at four window sizes.
exp42.py       the wires and parts as they are in Step 42 with the module held over H4 (pickled for way42*.py).
way42.py       a USB A end way (poses) against those wires and parts, and the caption box: wire clearance, depth in parts, how
               much is under the box and how high it reaches on screen, beat by beat.
way42b.py, way42c.py, way42d.py   the ways tried: hanging in front of the display's wires (b), raised and further left (c), set down
               to the display's left and slid in under its end (d: S5 is the one the guide uses).
exp42c.py      the USB cable at each stop of a way, settled as guide.py's usb_held() does, its length, and its height on screen
               through each blend against the caption box.
cam1920.py     Steps 19 - 20: every view direction against the tops of the pins being wired (superseded: a pin's tip can be seen
               while the cap that goes on it cannot).
cam1920c.py    Steps 19c - 20c: every view direction against the new wire's two caps as they sit once plugged in, and the angle
               at which the display's printed back is seen (the camera DISPLAY_PINS_RUN comes from this).
insight42.py   which of check_caps.py's Step 42c problems a ray from the step's camera reaches (in sight) at that moment.
capcmp.py      check_caps.py outputs compared step by step.
camdiff_r3.py  every view's camera compared with a steps.json saved before the round (only the steps Lee named may differ).
