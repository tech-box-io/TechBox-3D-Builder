Scripts behind Lee's fourth round (21 Oct 2026), Step 42, kept as they were run (paths made relative). Run from the repository's top
folder with .venv.nosync/bin/python. Each loads the kit's model: one at a time. They read Step 42's bench and held poses from the
kit's steps.json as it was before the round (the module's pose on the bench and over H4 have not changed since).

path42.py    the module's way from the bench to over H4, tried several ways (a straight turn; Rx first; flat a quarter turn, then
             stood up: the one used), with the wires bent with it as the player bends Step 42's opening routes: crossings of wire
             with wire, wires into the module, the Nano Board and the plug, sampled along the way; and how far the bent shapes end
             from the shapes over H4 (the re-dress still to come).
eval42n.py   a whole plan (the module's stops and the USB A end's, beat by beat) screened before it went into guide.py: the module
             against the case, the A end against the moving module, the wires and the parts, and how much of it is under the
             caption box at four window sizes (proj.py from round3/scripts).

The plan itself is in guide.py (WAY_42); docs/research/pmg/scripts/check_caps.py checks it as played (201 moments per beat), and
round3/scripts/insight42.py says which of its problems the camera can see.

Lee's second note of the round ("from behind the model instead of up and above it"):
cam42.py      Step 42 as steps.json has it, seen from behind: per direction, the smallest frame keeping the moving parts and the
              cable on screen and clear of the caption box at four window sizes, and what the case hides (rays, embree).
fit42.py      the same frame fit, faster (bisection on the radius, the target moved along the view's up and right); the camera in
              guide.py is its fit straight behind at 33 degrees up.
eval42top.py  the A end over the module's top in the stand-up beat, screened as eval42n.py screens a plan.
eval42top2.py the same, the stop on the module's display side, and how much of the A end the camera sees drawn over the wires.
shapes42.py   the wires as the player draws them while Step 42 plays (check_caps.py's blend, without the model): each wire's sharpest
              bend, how much longer than either shape it blends between, how high above both, beat by beat. A fold or a tent shows
              as a bend of over 100 degrees in 3 mm.
