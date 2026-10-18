"""Mini Robot Arm (MRA), deconstruction: the finished arm taken apart, down to R1. A guide of its own
(steps-deconstruction.json), made from the Full Build as guide.py last wrote it (run that first, and this again after any change to
it). First draft (Lee, 18 Oct 2026): the Full Build in reverse (rulebook section 11), with two exceptions of Lee's:
  - the eight breadboard wires come off the joysticks and the I/O module all at once;
  - no electronics test: each motor is unplugged and taken out once, where the build put it in (the bench test's plugging in and
    unplugging, and its USB cable, have no counterpart).
It opens on the Full Build's title page and ends on what is left, R1 (Lee's first round, 18 Oct 2026: the electronics come out of
the controller before the joysticks' walls, so the base is the last to go). Where Lee asked, a screw and the part it held go in one
step, one after the other: the screw out and gone, then the part (in_turn=: A12, A13, A11, A5, the lever); elsewhere, as the build.

Sub-assemblies the Full Build put together in the hand (the T1 / T2 block, the claw, the arm's links, the joysticks in their walls)
are lifted off the way they went on and taken apart on their own (alone=). Steps of the Full Build that moved only a plug on its lead
(into a slot, a hook or a hole) are walked back from the Full Build's own record of them: its poses and its lead's stages.
With B8 off, the breadboard wires come off the joysticks and the I/O module where they are, then the module slides out of the
controller and the Nano Board out of it (in the hand), then the joysticks come out with their walls and out of them (in the hand)."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
from stepgen import Guide, compose, via  # noqa: E402

# ---------------------------------------------------------------- parts (as guide.py names them; the CAD's instance ids)
B1, B2, B4, B5, B6_LEFT, B6_RIGHT, B7, B8, B3 = 'NAUO1 NAUO2 NAUO3 NAUO4 NAUO5 NAUO6 NAUO7 NAUO8 NAUO9'.split()
R1, R2, R3, R4, R6, R5, R7, R8 = 'NAUO10 NAUO11 NAUO12 NAUO13 NAUO14 NAUO15 NAUO16 NAUO17'.split()
BASE_MOTOR, BASE_HORN, BASE_PLUG = 'NAUO45', 'NAUO46', 'NAUO83'
BASE_SCREWS = ['NAUO47', 'NAUO48', 'NAUO49', 'NAUO50', 'NAUO51', 'NAUO52']
JOY_LEFT, JOY_RIGHT, MODULE, NANO = 'NAUO80', 'NAUO81', 'NAUO82', 'NAUO126'
A1, A2, A3, A4, A5, A7, A8, A11, A10, A12, A13, A6 = ['NAUO%d' % i for i in range(18, 30)]
A9_NEAR_A7, A9_NEAR_A8 = 'NAUO30', 'NAUO31'
ELBOW_MOTOR, ELBOW_HORN, ELBOW_PLUG = 'NAUO58', 'NAUO59', 'NAUO84'
SHOULDER_MOTOR, SHOULDER_HORN, SHOULDER_PLUG = 'NAUO66', 'NAUO67', 'NAUO86'
A7_SCREW, A8_SCREW, PIVOT_SCREW = 'NAUO53', 'NAUO54', 'NAUO55'
LEVER_SCREW, LEVER_A4_SCREW = 'NAUO56', 'NAUO62'
A5_A4_SCREW, A5_A7_SCREW = 'NAUO57', 'NAUO63'
R8_SCREWS, R7_SCREWS = ['NAUO60', 'NAUO61'], ['NAUO68', 'NAUO69']
A11_SCREW, A12_SCREW, R6_A11_SCREW, A13_SCREW = 'NAUO64', 'NAUO65', 'NAUO70', 'NAUO71'
C1, C2, C3, C6, C4, C5, C8, C7, C9 = ['NAUO%d' % i for i in range(32, 41)]
CLAW_MOTOR, CLAW_HORN, CLAW_PLUG = 'NAUO72', 'NAUO73', 'NAUO90'
C6_SCREWS, C8_SCREW = ['NAUO74', 'NAUO75'], 'NAUO76'
A12_C1_SCREW, A13_C1_SCREW, A5_C2_SCREW = 'NAUO77', 'NAUO78', 'NAUO79'
COUPLER, EXTENSION_PLUG, ROW10_PLUG = 'NAUO91', 'NAUO92', 'NAUO85'
T1_LOWER, T2_SOLID_DOWN, T2_SLOT_DOWN, T1_UPPER = 'NAUO41', 'NAUO42', 'NAUO43', 'NAUO44'
USB_B, USB_A = 'USB_B', 'USB_A'
JUMPER_CAPS = ['NAUO%d' % i for i in range(95, 111)]
BASE_SCREWS_HIDDEN = ['NAUO47']                                     # (the base screw R1 - R6 hide from the screws step's camera: a close-up of it)

# ---------------------------------------------------------------- the Full Build, as guide.py last wrote it
FULL = json.loads((HERE / 'steps.json').read_text(encoding='utf-8'))
VIEW = {v['name']: v for v in FULL['views']}
ROUTES = FULL['routes']


def camera_of(step, moved=None):
    """The camera of a Full Build step, for a step of ours that undoes it by hand (the generator reuses it by itself otherwise);
    moved: where the sub-assembly it showed in the hand is now, if it has slid since (a pose that only moves)."""
    c = VIEW[step]['camera']
    by = (moved.get('t') if isinstance(moved, dict) else moved) or [0.0, 0.0, 0.0]
    return dict(view_dir=c['dir'], frame=([round(a + b, 1) for a, b in zip(c['target'], by)], c['radius']))


def leads(step, prefix):
    """The routes of a lead's wires in a Full Build view: {wire: route}."""
    return {w: ROUTES[n] for w, n in VIEW[step]['wires'].items() if w.startswith(prefix + ' ')}


def walked_back(step, plug, prefix, carrier_pose=None, pivot=None):
    """A Full Build step that moved only a plug on its lead (its poses on the part it rides on, passed through at an even pace with
    the lead's stages), walked back: (path, wire_via, wires) for lift(ride_on=...). The poses are made absolute with the pose of the
    part the plug rides on, if that is not in its seat now."""
    done = VIEW[step + 'c']
    c = done['carry'][plug]
    stops = [VIEW[step]['carry'][plug]['pose'], *(c.get('via') or []), c['pose']]
    lines = {w: [r, *[ROUTES[n] for n in (done.get('wire_via') or {}).get(w, [])], ROUTES[done['wires'][w]]] for w, r in leads(step, prefix).items()}
    assert all(len(r) in (2, len(stops)) for r in lines.values()), (step, len(stops), {w: len(r) for w, r in lines.items()})
    if carrier_pose is not None:
        stops = [compose(carrier_pose, p, pivot) for p in stops]
    stops.reverse()
    path = [via(p) for p in stops[1:-1]] + [stops[-1]]
    return path, {w: r[::-1][1:-1] for w, r in lines.items() if len(r) > 2}, {w: r[0] for w, r in lines.items()}


def riding_back(step, part):
    """The way back through a Full Build step for a part that rode on the claw motor through it (the claw's lead and the servo
    extension wire's join, down behind R4 at Step 97): from where the step left it, through its stops, to where it was."""
    stops = [VIEW[step]['carry'][part]['pose'], *(VIEW[step + 'c']['carry'][part].get('via') or [])]
    stops.reverse()
    return [via(p) for p in stops[:-1]] + [stops[-1]]


def full_way_back(step, part, then=()):
    """A Full Build step's way in for one part, reversed (its stops kept, the poses between passed through), and on to `then`."""
    v = VIEW[step]
    own = (v.get('paths') or {}).get(part)
    way, stops = (own, (v.get('path_stops') or {}).get(part)) if own else (v['path'], v.get('stops'))
    n = len(way) - 1
    keep = {n - k for k in stops} if stops else set(range(n + 1))
    return [p if k in keep else via(p) for k, p in enumerate(way[::-1])][1:] + list(then)


g = Guide(HERE, title='Mini Robot Arm (MRA)', part='Deconstruction', names=dict(FULL['names']), steps_file='steps-deconstruction.json',
          hover_names={JOY_LEFT: 'Left Joystick', JOY_RIGHT: 'Right Joystick'},
          copyright_line='© TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')
g.take_apart()


def where(i):
    """Where a part is now (on what it rides, if it rides)."""
    if i in g.riding:
        by, rel = g.riding[i]
        return compose(where(by), rel, g._pivot(i))
    return g.resting.get(i)


# ================================================================ T1 / T2 BLOCK (the build's last, in the hand: first off)
T_BLOCK = [T1_LOWER, T2_SOLID_DOWN, T2_SLOT_DOWN, T1_UPPER]
g.remove('Take the T1 / T2 block apart. Pull the top T1 off the two T2.', [T1_UPPER], alone=T_BLOCK)
g.remove('Slide the upper T2 up and out of the other T2.', [T2_SLOT_DOWN], alone=T_BLOCK[:3])
g.remove('Pull the last T2 out of the plus-shaped slot in the lower T1.', [T2_SOLID_DOWN], alone=T_BLOCK[:2])
g.put_away([T1_LOWER])                                              # (what is left of a sub-assembly taken apart in the hand)

# ================================================================ POWER AND THE MOTORS' PLUGS
A_ON_THE_TABLE = VIEW['Completed View']['offsets'][USB_A]
g.remove('Unplug the power cable from the Nano Board.', [USB_B, USB_A], units=[[USB_B]],
         paths={USB_A: [dict(A_ON_THE_TABLE, t=[A_ON_THE_TABLE['t'][0], A_ON_THE_TABLE['t'][1] + 30.0, A_ON_THE_TABLE['t'][2]])]})   # (its other end lifted off the table with it)
g.unplug('Unplug the servo extension wire from Row 10.', [ROW10_PLUG])
g.unplug('Unplug the shoulder motor from Row 9.', [SHOULDER_PLUG])
g.unplug('Unplug the elbow motor from Row 6.', [ELBOW_PLUG])

# The join of the claw motor's lead and the servo extension wire: up from behind R4 and over its top edge, the extension wire out of
# the L-shaped slot in R4 (the Full Build's Step 97, walked back); then the extension wire pulled off the claw motor's plug (96).
JOIN = [CLAW_PLUG, COUPLER, EXTENSION_PLUG, ROW10_PLUG]
g.lift('Lift the join back up from behind R4, and the servo extension wire up out of the L-shaped slot in R4.', JOIN,
       paths={i: riding_back('Step 97', i) for i in JOIN}, ride_on=CLAW_MOTOR, arrows=[], eye=[COUPLER],
       wire_via={w: [ROUTES[n] for n in nos][::-1] for w, nos in VIEW['Step 97c']['wire_via'].items()},
       wires={**leads('Step 97', 'extension'), **leads('Step 97', 'claw')}, **camera_of('Step 97'))
g.remove("Pull the servo extension wire off the claw motor's plug.", [COUPLER, EXTENSION_PLUG, ROW10_PLUG],
         paths={i: [VIEW['Step 96']['carry'][i]['pose']] for i in (COUPLER, EXTENSION_PLUG, ROW10_PLUG)}, units=[[COUPLER, EXTENSION_PLUG]],
         **camera_of('Step 96'))                                    # (the arrow on the join; the plug at the wire's far end goes with it)
for step, caption in (('Step 95', "Pull the claw motor's plug back out of the bottom hole in A6."),
                      ('Step 94', 'Then pull it back out of the top hole in A6.')):
    path, stages, last = walked_back(step, CLAW_PLUG, 'claw')
    g.lift(caption, [CLAW_PLUG], path=path, ride_on=CLAW_MOTOR, wire_via=stages, wires=last, arrows=[], eye=[CLAW_PLUG], **camera_of(step))   # (an eye on the plug, no arrow, as an unplug: Lee, 18 Oct 2026)

# ================================================================ CLAW
g.remove('Unscrew the two 6mm screws that hold A12 and A13 to C1.', [A12_C1_SCREW, A13_C1_SCREW])
g.remove('Unscrew the 6mm screw that holds A5 to C2.', [A5_C2_SCREW])
CLAW_PARTS = list(VIEW['Step 90']['moving'])                          # (C3 first: the rest ride on it once it is lifted off)
g.lift('Slide the claw out from between A5 and A12 / A13.', CLAW_PARTS)
CLAW = CLAW_PARTS + [CLAW_PLUG]
without = lambda *gone: [i for i in CLAW if i not in gone]
g.remove('Take the claw apart. Unscrew the 10mm screw from C9.', [C8_SCREW], alone=CLAW)
g.remove('Slide C8 out from between C6 and C9.', [C8], alone=without(C8_SCREW))
g.remove('Pull C9 off the ends of C1 and C2.', [C9], alone=without(C8_SCREW, C8))
g.remove('Pull C7 off the servo horn.', [C7], alone=without(C8_SCREW, C8, C9))
g.remove('Unscrew the two 16mm screws that hold C6 to C3.', C6_SCREWS, alone=without(C8_SCREW, C8, C9, C7))
g.remove('Lift C6 off C4 and C5.', [C6], alone=without(C8_SCREW, C8, C9, C7, *C6_SCREWS))
g.remove('Pull C4 and C5 out of their slots in C3.', [C4, C5], alone=without(C8_SCREW, C8, C9, C7, *C6_SCREWS, C6))
IN_C3 = [C3, CLAW_MOTOR, CLAW_HORN, CLAW_PLUG]
g.remove('Pull C1 and C2 out of their slots in C3.', [C1, C2], alone=IN_C3 + [C1, C2])
assert VIEW['Step 78c']['carry'][CLAW_PLUG]['pose'] == VIEW['Step 94']['carry'][CLAW_PLUG]['pose']   # (the plug is where Step 78 left it)
path, stages, last = walked_back('Step 78', CLAW_PLUG, 'claw', carrier_pose=where(CLAW_MOTOR), pivot=g._pivot(CLAW_PLUG))
g.lift("Pull the claw motor's wire back out of the hole in the end of C3.", [CLAW_PLUG], path=path, ride_on=CLAW_MOTOR,
       wire_via=stages, wires=last, alone=IN_C3, view_dir=[-0.5792, 0.5736, -0.5792],   # (from above C3: Lee, 18 Oct 2026)
       arrows=[], eye=[CLAW_PLUG])
g.remove('Push the claw motor back out of C3.', [CLAW_MOTOR, CLAW_HORN], alone=IN_C3)
g.put_away([C3])

# ================================================================ ARM: the forearm links (A10 - A13)
g.remove('Unscrew the 6mm screw that holds A12 to A10, then lift A12 off.', [A12_SCREW, A12], in_turn=[[A12_SCREW], [A12]],
         **camera_of('Step 75'))
g.remove('Unscrew the 10mm screw that holds A13 and A10 to A8, then lift A13 off.', [A13_SCREW, A13], in_turn=[[A13_SCREW], [A13]])
g.remove('Unscrew the 6mm screw in the lobe of R6, from outside R6.', [R6_A11_SCREW])
LINKS = [A10, A11, A11_SCREW]
g.lift('Lift A10 and A11 out from behind the lobe of R6.', LINKS)
g.remove('Unscrew the 6mm screw that holds A11 to A10, then lift A11 off.', [A11_SCREW, A11], in_turn=[[A11_SCREW], [A11]], alone=LINKS)
g.put_away([A10])

# ================================================================ SHOULDER MOTOR
path, stages, last = walked_back('Step 67', SHOULDER_PLUG, 'shoulder')
g.lift("Take the shoulder motor's wire out of the hook-shaped slot in R6.", [SHOULDER_PLUG], path=path, ride_on=SHOULDER_MOTOR,
       wire_via=stages, wires=last, arrows=[], eye=[SHOULDER_PLUG], **camera_of('Step 67'))
g.remove('Unscrew the two 10mm screws that hold R7 to R6.', R7_SCREWS)
g.remove("Slide R7 back up the shoulder motor's wire and off over its plug.", [R7])
g.remove('Take the shoulder motor out of R6, angling its servo horn back out through the opening.', [SHOULDER_MOTOR, SHOULDER_HORN])

# ================================================================ ARM: A4 and A5
g.remove('Unscrew the 6mm screw that holds A5 to A7, and the 10mm screw that holds A1 - A3 to A4.', [A5_A7_SCREW, LEVER_A4_SCREW])
FOREARM = [A4, A5, A5_A4_SCREW]
g.lift('Lift A4 and A5 off together.', FOREARM)
g.remove('Unscrew the 6mm screw that holds A5 to A4, then lift A5 off.', [A5_A4_SCREW, A5], in_turn=[[A5_A4_SCREW], [A5]], alone=FOREARM)
g.put_away([A4])

# ================================================================ ELBOW MOTOR
path, stages, last = walked_back('Step 57', ELBOW_PLUG, 'elbow')
g.lift("Take the elbow motor's wire out of the hook-shaped slot in R5.", [ELBOW_PLUG], path=path, ride_on=ELBOW_MOTOR,
       wire_via=stages, wires=last, arrows=[], eye=[ELBOW_PLUG], **camera_of('Step 57'))
g.remove('Unscrew the two 10mm screws that hold R8 to R5.', R8_SCREWS)
g.remove("Slide R8 back up the elbow motor's wire and off over its plug.", [R8])
g.remove('Take the elbow motor out of R5, angling its servo horn back out through the opening.', [ELBOW_MOTOR, ELBOW_HORN])

# ================================================================ ARM: the lever (A1 - A3) and the upper arm (A6 - A9)
LEVER = [A1, A2, A3, LEVER_SCREW]
g.lift('Slide A1 - A3 back up from between R5 and A7.', LEVER)
g.remove('Unscrew the 10mm screw from A1 - A3, then lift A3 off, then A2, leaving A1.', [LEVER_SCREW, A3, A2],
         in_turn=[[LEVER_SCREW], [A3], [A2]], units=[[LEVER_SCREW, A3, A2]], alone=LEVER)   # (all three go the same way: one arrow)
g.put_away([A1])
g.remove('Unscrew the 6mm screw that holds A7 to R2. Reach it through the opening in R5.', [PIVOT_SCREW])
UPPER = [A6, A7, A9_NEAR_A7, A7_SCREW, A8, A9_NEAR_A8, A8_SCREW]
g.lift('Lift A6 - A9 up off R2.', UPPER)
g.remove('Unscrew the 16mm screw that holds A8 to the A9 beside it.', [A8_SCREW], alone=UPPER)
g.remove('Pull that A9 out of its cross-shaped slot in A6.', [A9_NEAR_A8], alone=[A6, A7, A9_NEAR_A7, A7_SCREW, A8, A9_NEAR_A8])
g.remove('Pull A8 off its two tabs on A6.', [A8], alone=[A6, A7, A9_NEAR_A7, A7_SCREW, A8])
g.remove('Unscrew the 16mm screw that holds A7 to the other A9.', [A7_SCREW], alone=[A6, A7, A9_NEAR_A7, A7_SCREW])
g.remove('Pull that A9 out of its slot too.', [A9_NEAR_A7], alone=[A6, A7, A9_NEAR_A7])
g.remove('Pull A7 off the last two tabs on A6.', [A7], alone=[A6, A7])
g.put_away([A6])

# ================================================================ THE CONTROLLER'S ELECTRONICS (Lee, 18 Oct 2026: they come out before the walls)
g.unplug('Unplug the base motor from Row 5.', [BASE_PLUG])
BENCH_ROUTES = {w: r for side in ('left', 'right') for w, r in leads('Step 11c', side).items()}   # (the wires' own shapes, tied to their caps
g.remove('Lift B8 off B5 - B7.', [B8], wires=BENCH_ROUTES)                                        # as on the bench, so that they go with them)
ENDS_ON = lambda part: [cap for cap in JUMPER_CAPS if g.riding[cap][0] == part]
middle = lambda caps: sorted(caps, key=lambda c: tuple(g._pivot(c).round(1)))[len(caps) // 2]
g.remove('Unplug the eight breadboard wires from the joysticks and the I/O module.', JUMPER_CAPS, arrows=[],
         eye=[middle(ENDS_ON(JOY_LEFT)), middle(ENDS_ON(JOY_RIGHT)), middle(ENDS_ON(MODULE))])   # (an eye on each end, no arrows: Lee)
g.lift('Slide the I/O module back out of the slots in B6.', [MODULE])   # (the way it went in, reversed, by the Full Build's camera for it)
g.remove('Lift the Nano Board out of the I/O module.', [NANO], alone=[MODULE, NANO], view_dir=VIEW['Step 1']['camera']['dir'])
g.put_away([MODULE])                                                # (what is left of a sub-assembly taken apart in the hand)

# ================================================================ THE JOYSTICKS AND THEIR WALLS
RIGHT = [B6_RIGHT, B7, JOY_RIGHT]                                     # (B6 first, as the Full Build: the others ride on it once lifted off)
g.lift('Lift B6 and B7 off B3 with the right joystick between them.', RIGHT, units=[[JOY_RIGHT]])   # (the arrow on the joystick: Lee)
g.remove('Pull B7 off the right joystick.', [B7], alone=RIGHT)
g.remove('Pull the right joystick out of B6.', [JOY_RIGHT], alone=[B6_RIGHT, JOY_RIGHT], keep_camera=True)   # (as the step before: Lee)
g.put_away([B6_RIGHT])
LEFT = [B5, B6_LEFT, JOY_LEFT]
g.lift('Lift B5 and B6 off B3 with the left joystick between them.', LEFT, units=[[JOY_LEFT]])
g.remove('Pull B6 off the left joystick.', [B6_LEFT], alone=LEFT)
g.remove('Pull the left joystick out of B5.', [JOY_LEFT], alone=[B5, JOY_LEFT], keep_camera=True)
g.put_away([B5])
g.remove('Pull B4 out of B2.', [B4])
g.remove('Pull B3 out of B2.', [B3])

# ================================================================ BASE (R1 is left)
HIDDEN_HEAD = [round(float(x), 1) for x in (g.model.inst[BASE_SCREWS_HIDDEN[0]].bounds.mean(0) * [1, 0, 1]
                                            + [0, g.model.inst[BASE_SCREWS_HIDDEN[0]].bounds[1][1] - 1.0, 0])]   # (its head)
g.remove('Unscrew the six 6mm screws that hold B2 to B1.', BASE_SCREWS, keep_camera=True,   # (B3's camera, kept: Lee)
         inset=dict(target=HIDDEN_HEAD, dir=[0.5792, 0.5736, -0.5792], radius=14.0, mark=4.5,   # (the sixth screw, seen from the other side)
                    alt='The sixth screw, at the far corner, behind R1 - R6'))
g.remove('Lift R1 - R6 and B2 off B1.', [B1])
g.remove('Slide B2 out from between the servo horn and R5 / R6.', [B2])
path, stages, last = walked_back('Step 25', BASE_PLUG, 'base')
g.lift("Take the base motor's wire out of the L-shaped slot in R4.", [BASE_PLUG], path=path, ride_on=BASE_MOTOR,
       wire_via=stages, wires=last, arrows=[], eye=[BASE_PLUG], **camera_of('Step 25'))
g.remove("Take R6 off. Keep the base motor's wire clear of it.", [R6])
g.remove('Take R5 off the other side.', [R5])
g.remove('Lift R4 off R1.', [R4])
g.remove('Lift R3 off R1.', [R3])
g.remove('Slide R2 up off the base motor.', [R2])
g.remove('Turn the base motor and angle its servo horn back out through the slot in R1.', [BASE_MOTOR, BASE_HORN])

g.build()
