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

Lee's first round (20 Oct 2026; docs/research/lac/round1/):
  planner.py         (updated) Field(..., poses={id: pose}) places parts where a step does not have them (F1 aside, the LCD seated)
  plan_r1.py         the switch's leads lying (F4 35 mm nearer: SWITCH_WAY) and the potentiometer's with F1 face down in front (POT_WAY):
                     python plan_r1.py sw|pot [F1 pose as JSON] <clearance> <control point spacing>
  plan_buzz.py       the buzzer's leads lying (BUZZER_WAY) and at Step 43's stops (BUZZER_LIFT_WAY, BUZZER_UP_WAY):
                     python plan_buzz.py '<stop poses JSON>' '<view>' <clearance> <spacing> <grid mm> '<views to clear, comma-separated>'
  plan_aside.py      the potentiometer's leads with F1 moved aside (Step 46: ASIDE_WAY), through the case as it is once the LCD is in,
                     F8's way in kept clear: python plan_aside.py '<F1 pose JSON>' '<LCD pose JSON>' <clearance> <spacing>
  plan_buzz_up.py    the buzzer's leads held over its seat (Step 43: BUZZER_UP_WAY), from the buzzer to the CAD's clamped lead 36 mm along
  sight.py           sight lines from the player's eye to the holes a step's caps go into, against the caps and wires at rest, in four
                     window shapes; `search` / `relaxed` look for nearby camera directions that show them (the cameras of Steps 14, 20,
                     21 and 38). Caps are taken as their boxes: confirm a direction in the player, against its meshes.
