LAC wire routes: the scripts that designed the re-routed wires (19 Oct 2026; docs/research/lac/cad_study.md, section 8)

Run from this folder with the project's Python (.venv.nosync/bin/python <script>); each reads the kit's current steps.json, so the other
wires are as last generated. What each found is written into "LAC Build Instructions/guide.py" by hand, as control points.

  harness.py         check(view, points, radius, ...) and clearance(...): a candidate route against the view's parts and other wires,
                     as tools/wirecheck.py judges it
  design_common.py   into_hole() and the CAD's wire lines, as guide.py has them
  planner.py         a path search: the clearance to every part's surface and every other wire on a 1 mm grid, A* over the free cells
                     (preferring 3 mm of room), smoothed into control points
  plan_in.py         the potentiometer's leads seated (F1_IN_WAY), view Step 56c
  plan_up.py         ... with F1 stood up in front of the case (F1_FRONT_WAY), joined to the seated ones inside the case
  plan_sw.py         the switch's leads seated (SW_SEATED_WAY): python plan_sw.py 0.6 4 (clearance asked for, control point spacing)
  pot_common.py, eval_in.py, d_pot3.py   the potentiometer's leads lying beside the base (POT_WAY: hand-set lanes, scored)
  d_switch.py, d_red.py, d_usb3.py       the switch's leads beside the base, the dark red jumper's arch, the USB cable
