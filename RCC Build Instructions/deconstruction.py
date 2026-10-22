"""Remote Controlled Car (RCC), deconstruction: the finished car and controller taken apart, down to L1. A guide of its own
(steps-deconstruction.json), made from the Full Build as guide.py last wrote it (run that first, and this again after any change to
it). It opens on the Full Build's title page and ends on what is left, L1, then goes straight to the Full Build's parts list pages (no
Completed View: Lee, 22 Oct 2026); its card on the website is the Full Build's.

First draft (Lee, 18 Oct 2026), the Full Build in reverse (rulebook section 11), in the order Lee gave:
  1. the controller first, on its own (the car hidden): its USB cable unplugged (seen a little wider, so that the cable shows; one
     arrow, on the Mini-B plug, clear of the cable), then the joysticks, the radio module and the Nano Board come off, close in;
  2. the car: the barrel plug unplugged and the battery lifted out with its 9V adapter; the adapter taken off the battery on its
     own; then back to the car;
  3. the wheel motors unplugged before L6, L7 and the I/O module come out;
  4. the I/O module, once out of the car, taken apart on its own (the radio module, the adapter board, the Nano Board); then back
     to the car and motors;
  5. L4 and L5 lifted off L1 with the motors and taken off them in the hand (Lee wrote "R4 and R5"), then L3 and L2 off L1.
No electronics test: each part comes out once, where the build put it in last."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
from stepgen import Guide, _rot, apply_pose, compose  # noqa: E402

# ---------------------------------------------------------------- parts (as guide.py names them; the CAD's instance ids)
L1, L2, L3, L4, L5, L6, L7 = ['NAUO%d' % i for i in range(1, 8)]
WHEEL_R, WHEEL_L = 'NAUO8', 'NAUO9'
CAR_RADIO, CONTROLLER_RADIO = 'NAUO10', 'NAUO11'
JOY_LEFT, JOY_RIGHT = 'NAUO12', 'NAUO13'
BATTERY, CLIP, BARREL = 'NAUO14', 'NAUO15', 'NAUO29'
USB_B, USB_A = 'NAUO16', 'USB_A'
MOTOR_R, MOTOR_L, PLUG_R, PLUG_L = 'NAUO17', 'NAUO18', 'NAUO19', 'NAUO20'
MODULE, CAR_NANO, ADAPTER = 'NAUO23', 'NANO_CAR', 'NAUO26'
BOARD, GUARD_LEFT, GUARD_RIGHT, CONTROLLER_NANO = 'NAUO30', 'NAUO24', 'NAUO25', 'NANO_CONTROLLER'
CONTROLLER = [BOARD, GUARD_LEFT, GUARD_RIGHT, CONTROLLER_NANO, CONTROLLER_RADIO, JOY_LEFT, JOY_RIGHT]

# ---------------------------------------------------------------- the Full Build, as guide.py last wrote it
FULL = json.loads((HERE / 'steps.json').read_text(encoding='utf-8'))
VIEW = {v['name']: v for v in FULL['views']}
ROUTES = FULL['routes']
TURN = VIEW['Completed View']['offsets'][BOARD]                    # (the controller, turned round from Step 29 on)


def turned_camera(step):
    """A Full Build step's camera on the controller, turned round with it (the build put its parts on before it was turned)."""
    c = VIEW[step]['camera']
    return dict(view_dir=[round(float(x), 4) for x in _rot(TURN) @ c['dir']],
                frame=([round(float(x), 1) for x in apply_pose(TURN, c['target'])], c['radius']))


def leads(step, side):
    """The routes of a motor's lead in a Full Build view: {wire: route}."""
    return {w: ROUTES[n] for w, n in VIEW[step]['wires'].items() if w.startswith(side + ' ')}


g = Guide(HERE, title='Remote Controlled Car (RCC)', part='Deconstruction', names=dict(FULL['names']), steps_file='steps-deconstruction.json', source='rcc.glb',
          hover_names={JOY_LEFT: 'Left Joystick', JOY_RIGHT: 'Right Joystick', MOTOR_L: 'Left Wheel Motor', MOTOR_R: 'Right Wheel Motor',
                       PLUG_L: 'Left Wheel Motor', PLUG_R: 'Right Wheel Motor'},
          copyright_line='© TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')
g.take_apart(parts_list_at_end=True, completed_view=False)          # (from Step 20c straight to the Full Build's parts list, as the others: Lee,
#                                                                     22 Oct 2026; no Completed View)


def where(i):
    """Where a part is now (on what it rides, if it rides)."""
    if i in g.riding:
        by, rel = g.riding[i]
        return compose(where(by), rel, g._pivot(i))
    return g.resting.get(i)

# ================================================================ THE CONTROLLER, on its own (Lee, 18 Oct 2026: the car hidden)
USB = [USB_B, USB_A]
A_END = VIEW['Completed View']['offsets'].get(USB_A) or [0.0, 0.0, 0.0]
g.remove("Unplug the USB cable from the controller's Nano Board.", USB, alone=CONTROLLER + USB,
         units=[[USB_B]],                                           # (one arrow, on the Mini-B plug: none on the A end, lifted with it)
         paths={USB_A: [compose([0.0, 25.0, 0.0], A_END)]},
         arrow_style={USB_B: dict(scale=4.0, at=[711.0, 942.0, 1129.23])},   # (four times the size (Lee, 18 Oct 2026: doubled twice), on the plug's body, just above it, clear of
                                                                    # the cable, which runs on along the plug's way out: Lee)
         view_dir=VIEW['Step 29']['camera']['dir'], frame=([748.0, 928.0, 1126.0], 112.0))   # (Step 29's corner, wider than the controller's
                                                                    # close-ups, so that the whole cable shows: Lee)
# (the joysticks' arrows twice the size and along the pull back out of the socket, the first stage of the way: Lee, 18 Oct 2026)
g.remove('Pull the right joystick back out of R-JS, then lift it out of its pocket.', [JOY_RIGHT], alone=CONTROLLER,
         arrow_style={JOY_RIGHT: dict(scale=4.0, stage=0)}, **turned_camera('Step 4'))
# (one camera for the run on the controller: Lee's rule, two steps on one sub-assembly in the hand keep one camera)
g.remove('Pull the left joystick back out of L-JS, then lift it out of its pocket.', [JOY_LEFT], alone=[i for i in CONTROLLER if i != JOY_RIGHT],
         arrow_style={JOY_LEFT: dict(scale=4.0, stage=0)}, keep_camera=True)
LEFT_ON_BOARD = [BOARD, GUARD_LEFT, GUARD_RIGHT, CONTROLLER_NANO, CONTROLLER_RADIO]
g.remove('Lift the radio module out of its socket.', [CONTROLLER_RADIO], alone=LEFT_ON_BOARD, keep_camera=True, arrow_scale=4.0)
g.remove('Lift the Nano Board out of H1 and H2.', [CONTROLLER_NANO], alone=LEFT_ON_BOARD[:4], keep_camera=True, arrow_scale=4.0)
g.put_away([BOARD])                                                 # (what is left of the controller: the board with its guards)

# ================================================================ POWER
g.unplug("Unplug the 9V adapter's barrel plug from the power socket on the I/O module.", [BARREL])
g.lift('Lift the 9V battery, with its 9V adapter, out of the square hole in L1.', [BATTERY], arrow_scale=2.0)
BATTERY_SET = [BATTERY, CLIP, BARREL]
g.remove('Unsnap the 9V adapter from the top of the battery.', [CLIP, BARREL], alone=BATTERY_SET, units=[[CLIP]], direction=[0, 1, 0], hover=30.0,   # (Lee: on its own)
         arrow_scale=2.0,
         paths={BARREL: [compose([0.0, 30.0, 0.0], where(BARREL), g._pivot(BARREL))]})   # (its barrel plug, dangling, goes up with it)
g.put_away([BATTERY])

# ================================================================ THE WHEEL MOTORS' PLUGS (before L6, L7 and the module: Lee)
g.unplug('Unplug both wheel motors from RWh and LWh.', [PLUG_R, PLUG_L], ride_on=L1)   # (in one step: Lee; each plug back behind L1, lying on it,
                                                                    # as before Steps 25 and 26)

# ================================================================ L6, L7 AND THE I/O MODULE
g.remove('Turn the car over. Slide L6 out.', [L6], arrow_scale=2.0)
g.remove('Slide L7 out.', [L7], arrow_scale=2.0)
g.lift('Turn the car the right way up. Slide the I/O module forward, out of the grooves in L4 and L5.', [MODULE], arrow_scale=2.0)
MODULE_SET = [MODULE, CAR_NANO, ADAPTER, CAR_RADIO]
g.remove('Lift the radio module out of U3 on the adapter board.', [CAR_RADIO], alone=MODULE_SET, arrow_scale=2.0)   # (Lee: the module on its own)
ON_ADAPTER = [round(float(x), 2) for x in apply_pose(where(ADAPTER), [704.0, 924.0, 1321.0])]   # (on its long arm, clear of the Nano Board: Lee)
g.remove('Lift the adapter board off the pins along the side of the I/O module.', [ADAPTER], alone=MODULE_SET[:3], keep_camera=True,
         arrow_style={ADAPTER: dict(scale=2.0, at=ON_ADAPTER)})
g.remove('Lift the Nano Board out of the I/O module.', [CAR_NANO], alone=MODULE_SET[:2], keep_camera=True, arrow_scale=2.0)
g.put_away([MODULE])

# ================================================================ L4, L5 AND THE MOTORS
# Lifted off L1 the way the Full Build lowered them, the motors' wires straightened back as they were in the hand (Step 20), so
# that L4 can slide off along them, each plug passing back through its hole in L4.
BLOCK = [L5, MOTOR_R, MOTOR_L, L4]
UP = VIEW['Step 21']['path'][0]                                     # (where the Full Build held the block over L1)
IN_HAND = {p: compose(UP, VIEW['Step 21']['carry'][p]['pose'], g._pivot(p)) for p in (PLUG_R, PLUG_L)}
g.lift("Lift L4 and L5, with the wheel motors, off L1, bringing each motor's wire up out of its notch.", BLOCK + [PLUG_R, PLUG_L], paths={p: [pose] for p, pose in IN_HAND.items()},
       units=[[L5, MOTOR_R, MOTOR_L, L4]], wires={**leads('Step 21', 'right'), **leads('Step 21', 'left')}, arrow_scale=2.0)
IN_L5 = BLOCK + [WHEEL_R, WHEEL_L, PLUG_R, PLUG_L]
g.remove("Slide L4 back off along the motors' wires, each plug passing back through its hole in L4.", [L4], alone=IN_L5, arrow_scale=2.0)
# (both motors out of L5 in one step, Lee; each the way the Full Build pushed it in, reversed, its plug, which rides on L5 since the
# lift, going with it; an arrow on each, four times the size; the right one's starting where the left one's does on its wheel, mirrored
# across L2's mid-plane: Lee, 18 Oct 2026)
L2_MID_Z = 1338.48                                                  # (L2's mid-plane: the car is symmetric about it)
g.remove('Pull both wheel motors out of L5.', [MOTOR_L, PLUG_L, MOTOR_R, PLUG_R], alone=[L5, MOTOR_R, MOTOR_L, PLUG_R, PLUG_L],
         units=[[MOTOR_L], [MOTOR_R]], arrow_scale=4.0, keep_camera=True,   # (as the step before's: one camera for the run in the hand)
         arrow_style={MOTOR_R: dict(scale=4.0, at=[689.64, 986.91, round(2 * L2_MID_Z - 1281.61, 2)])},   # (the left one's tail: 689.64, 986.91, 1281.61)
         paths={plug: [compose(VIEW[step]['path'][0], where(plug), g._pivot(plug))] for step, plug in (('Step 19', PLUG_L), ('Step 18', PLUG_R))})
g.put_away([L5])

# ================================================================ L3 AND L2 (L1 is left)
g.remove('Turn L1 over. Pull L3 off L2 and out of the short slots in L1.', [L3], arrow_scale=2.0)
g.remove('Swing L2 up out of its slots in L1, then unhook it from the notch at the flat end of L1.', [L2], arrow_scale=2.0)

g.build()
