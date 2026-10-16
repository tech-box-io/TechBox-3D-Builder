"""Remote Controlled Car (RCC), full build: the controller, the car's electronics tried on the bench with the controller, then
the car. The build, in order.

Run from the project root:   python "RCC Build Instructions/guide.py"
It writes steps.json (what the player shows) and parts.json (the parts list).

First draft (15 Oct 2026). The order and the wiring follow TechBox's published Cadasio guide 19075 (docs/research/rcc/
cadasio_study.md), put right where that guide goes wrong (the car's Nano Board disappears and looks reversed, the battery is
never plugged in, the joysticks glide in through the guard, the test is half there); the geometry is the CAD's (docs/research/
rcc/cad_study.md). Lee's open decisions are yellow Review notes on their steps. One part or one action per step.
"""
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
import wires as W  # noqa: E402
from stepgen import Guide, apply_pose, turned, via  # noqa: E402

# ---------------------------------------------------------------- parts
# CAD instance ids (RCC_Assembly_v1). Every wood part's CAD name is the code engraved on it. The car's front is +X (the flat end
# of L1, where the wheels are), so the car's left is -Z and its right +Z; the controller lies beside the car, on its left.
L1, L2, L3, L4, L5, L6, L7 = ['NAUO%d' % i for i in range(1, 8)]
WHEEL_R, WHEEL_L = 'NAUO8', 'NAUO9'
CAR_RADIO, CONTROLLER_RADIO = 'NAUO10', 'NAUO11'
JOY_LEFT, JOY_RIGHT = 'NAUO12', 'NAUO13'
BATTERY, CLIP = 'NAUO14', 'NAUO15'                                  # the 9V battery; the battery clip ("DC_Adaptor") on its top
USB_B, USB_A = 'NAUO16', 'USB_A'                                    # the USB cable's Mini-B end (in the CAD), its A end (materials.json "extra_parts")
MOTOR_R, MOTOR_L = 'NAUO17', 'NAUO18'                               # FS90R wheel motors: right (+Z), left (-Z)
PLUG_R, PLUG_L = 'NAUO19', 'NAUO20'                                 # the plug of each motor's lead, as the CAD has it on U2 (RWh) / U1 (LWh)
MODULE = 'NAUO23'                                                   # the Nano I/O module (the MRA's I/O module)
CAR_NANO = 'NANO_CAR'                                               # the car's Nano Board: the controller's Nano model in the car's seat (materials.json "extra_parts")
GUARD_LEFT, GUARD_RIGHT = 'NAUO24', 'NAUO25'
ADAPTER = 'NAUO26'                                                  # TechBox's L-shaped adapter board: U1 (LWh), U2 (RWh), U3 (radio)
CONTROLLER_NANO = 'NAUO27'
BARREL = 'NAUO29'                                                   # the barrel plug on the battery clip's lead, as the CAD has it in the power socket
BOARD = 'NAUO30'                                                    # the controller board
# (Not used: the CAD poses each lead twice. NAUO21 / 22 are the same plugs lying loose, NAUO28 the barrel plug out of its
# socket, NAUO31 - 42 the leads' bodies, drawn as wires here; NAUO86 is the car's Nano as the CAD has it, a plainer model.)

NAMES = {L1: 'L1', L2: 'L2', L3: 'L3', L4: 'L4', L5: 'L5', L6: 'L6', L7: 'L7',
         WHEEL_R: 'Wheel', WHEEL_L: 'Wheel', CAR_RADIO: 'Radio Module', CONTROLLER_RADIO: 'Radio Module',
         JOY_LEFT: 'Joystick', JOY_RIGHT: 'Joystick', BATTERY: '9V Battery', CLIP: 'Battery Clip', USB_B: 'USB Cable', USB_A: 'USB Cable',
         MOTOR_R: 'Wheel Motor', MOTOR_L: 'Wheel Motor', PLUG_R: 'Wheel Motor', PLUG_L: 'Wheel Motor',
         MODULE: 'Nano I/O Module', CAR_NANO: 'Nano Board', CONTROLLER_NANO: 'Nano Board', ADAPTER: 'Adapter Board',
         GUARD_LEFT: 'Left Controller Guard', GUARD_RIGHT: 'Right Controller Guard', BOARD: 'Controller Board'}
PART_OF = {BARREL: CLIP}                                            # the barrel plug comes on the battery clip's lead: one part
UNLISTED = [PLUG_R, PLUG_L, USB_A]                                  # named on hover only (a motor's plug; the USB cable is listed by its Mini-B end)
# How the parts list pictures a part, where the generator's own view does not suit: L1's FRONT / L1 and the controller board's
# print came out upside down; the guards and the adapter board are seen from above, so that their print and rims show.
PART_VIEWS = {'L1': {'roll': 180}, 'Controller Board': {'roll': 180}, 'Adapter Board': {'dir': [0.45, 0.85, 0.25]},
              'Left Controller Guard': {'dir': [-0.45, 0.85, 0.25]}, 'Right Controller Guard': {'dir': [-0.45, 0.85, -0.25]}}

# The parts list after the title page: one band per kind of part (as in the MRA guide).
PART_GROUPS = [
    ('Parts List', 'Controller', 'electronics', '#f9c0c0', '#ec8d8d', lambda n: n in ('Controller Board', 'Left Controller Guard', 'Right Controller Guard', 'Joystick')),
    ('Parts List', 'Electronics', 'electronics', '#f9c0c0', '#ec8d8d', lambda n: n in ('Nano Board', 'Nano I/O Module', 'Adapter Board', 'Radio Module', 'USB Cable', '9V Battery', 'Battery Clip')),
    ('Parts List', 'Motors and wheels', 'motors', '#d8edc6', '#a3cf84', lambda n: n in ('Wheel Motor', 'Wheel')),
    ('Parts List (Cont.)', 'Chassis', 'wood', '#fddcbc', '#f3b583', lambda n: re.fullmatch(r'L\d+', n)),
]


def parts_list(parts):
    """The parts list's pages for the parts this guide shows (see Guide(parts_list=))."""
    natural = lambda p: [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', p['name'])]
    pages, used = {}, set()
    for page, title, icon, colour, halo, wanted in PART_GROUPS:
        items = [p for p in parts if wanted(p['name']) and p['name'] not in used]
        if icon == 'wood':
            items.sort(key=natural)
        if not items:
            continue
        used.update(p['name'] for p in items)
        if icon == 'wood':
            title = f"{title} ({items[0]['name']}{' - ' + items[-1]['name'] if len(items) > 1 else ''})"
        for p in items:
            p['group'] = title
        pages.setdefault(page, []).append(dict(title=title, icon=icon, colour=colour, halo=halo,
                                               items=[dict(name=p['name'], qty=p['qty'], picture=p['picture']) for p in items]))
    left = [p for p in parts if p['name'] not in used]
    if left:
        other = dict(title='Other parts', icon='wood', colour='#e8e8e8', halo='#bdbdbd', items=[dict(name=p['name'], qty=p['qty'], picture=p['picture']) for p in left])
        pages.setdefault(list(pages)[-1] if pages else 'Parts List', []).append(other)
    names = ['Parts List'] + [f"Parts List (Cont.{'' if k == 1 else f' {k}'})" for k in range(1, len(pages))]
    return [dict(name=name, groups=groups) for name, groups in zip(names, pages.values())]


# The engraved code on each wood part (the way its face looks, the middle of the code, seated: cad_study.md 2.4), so the camera
# prefers a side from which it can be read.
CODES = {L1: ([0, 1, 0], [766.26, 908.97, 1394.03]), L2: ([0, 0, -1], [677.40, 899.44, 1336.98]), L3: ([1, 0, 0], [643.17, 886.35, 1348.16]),
         L4: ([1, 0, 0], [716.12, 896.98, 1361.41]), L5: ([1, 0, 0], [742.47, 896.94, 1361.42]), L6: ([0, 0, 1], [766.74, 902.04, 1355.48]),
         L7: ([0, 0, -1], [767.15, 902.08, 1321.48])}

g = Guide(HERE, title='Remote Controlled Car (RCC)',   # ("Remote": Lee, 16 Oct 2026)
          part='Full Build', names=NAMES, part_views=PART_VIEWS, part_of=PART_OF, unlisted=UNLISTED, source='rcc.glb',
          codes=CODES, hero_azimuth=135,                            # the finished car from the front, on its left (the controller's) side, above
          parts_list=parts_list,
          copyright_line='© TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')

# ---------------------------------------------------------------- wires
# The CAD's lead bodies are left out of the model (materials.json "omit"); the leads are drawn from wire-paths.json. A wheel
# motor's lead is three wires (brown on G, red on V, yellow on S) ending in a plug, which rides on the loose end of the lead until
# a step plugs it in. The battery clip's lead is two wires (red, black) ending in the barrel plug.
paths = W.load(HERE / 'wire-paths.json')
LEAD_COLOURS = ['lead_brown', 'lead_red', 'lead_yellow']            # G, V, S (yellow, as the CAD and the published guide have it: see Step 13's note)
ZERO = [0.0, 0.0, 0.0]


def lead_wires(name, motor_name):
    ids = [f'{name} {c}' for c in ('brown', 'red', 'yellow')]
    for wire_id, colour in zip(ids, LEAD_COLOURS):
        g.wire(wire_id, colour, 0.5, name=motor_name)
    return ids


def routes(ids, lines, **ends):
    """One route per wire of a lead."""
    return {wire_id: W.route(line, **ends) for wire_id, line in zip(ids, lines)}


def lifted(pose, mm):
    """The same pose, raised by mm."""
    return [pose[0], pose[1] + mm, pose[2]] if isinstance(pose, list) else {**pose, 't': [pose['t'][0], pose['t'][1] + mm, pose['t'][2]]}


def to_length(corners, length, radius=6.0):
    """A line through `corners`, rounded, cut or carried on along its last leg to `length` mm."""
    line = W.rounded([np.asarray(c, float) for c in corners], radius=radius)
    extra = length - W.length(line)
    if extra <= 0:
        return W.along(line, 0, length)
    return W.join(line, W.straight(line[-1], line[-1] - line[-2], extra))


# The table: on the bench the I/O module lies on its underside; the motors stand on their wheels beside it and the battery on its
# end behind it, each where it goes in the car but lifted onto the table (the chassis is not there yet).
TABLE_Y = float(g.model.inst[MODULE].bounds[0][1])
MOTOR_ON_BENCH = [0.0, round(TABLE_Y - float(g.model.inst[WHEEL_R].bounds[0][1]), 2), 0.0]
BATTERY_ON_BENCH = [0.0, round(TABLE_Y - float(g.model.inst[BATTERY].bounds[0][1]), 2), 0.0]
LEAD_MM = 115.0                                                     # one length for both motors' leads (the CAD's differ: see Step 13's note)


def fitted(make, length, lo=-20.0, hi=60.0):
    """make(s): a line that grows longer with s. Returns the one whose length is `length` (s found by halving between lo and hi)."""
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if W.length(make(mid)) < length else (lo, mid)
    return make((lo + hi) / 2)


def lying_flat(line, across, plug, flat):
    """A lead along `line` with its plug loose on the end, the lead turning (evenly along its length) to lie flat, wide along
    `flat`, so that the plug lies flat. Returns (the three wires, the plug's pose)."""
    lines = W.ribbon(line, across, pitch=1.02, n=3, end_pitch=plug['pitch'], fan_mm=10.0, end_across=flat)
    return lines, W.plug_pose(plug, lines[1][-1], lines[1][-1] - lines[1][-2], lines[2][-1] - lines[0][-1])


FLAT = 1.4                                                          # mm from a surface to the middle of a plug lying flat on it (2.6 mm thick)


def cut_lead(lines, plug, height, fan_mm=12.0):
    """A plugged lead cut short where it comes straight down to its header `height` mm above it, the plug on the end in line with
    it (the same wires, so that from there it only has to go on down). Returns (lines, the plug's pose)."""
    lines = [np.asarray(l, float) for l in lines]
    mid = lines[1]
    y = plug['tops'][1][1] + height
    k = max(i for i in range(1, len(mid)) if mid[i - 1][1] >= y >= mid[i][1])
    f = (mid[k - 1][1] - y) / (mid[k - 1][1] - mid[k][1])
    cut = [np.vstack([l[:k], l[k - 1] + (l[k] - l[k - 1]) * f]) for l in lines]
    d = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(cut[1], axis=0), axis=1))])
    u = np.clip((d - (d[-1] - fan_mm)) / fan_mm, 0.0, 1.0)
    side = (cut[2] - cut[0]) / 2
    grow = 1 + (plug['pitch'] / np.linalg.norm(side, axis=1)[:, None] - 1) * (u * u * (3 - 2 * u))[:, None]
    cut = [cut[1] - side * grow, cut[1], cut[1] + side * grow]
    return cut, W.plug_pose(plug, cut[1][-1], cut[1][-1] - cut[1][-2], cut[2][-1] - cut[0][-1])


def motor_lead(name, motor, plug_id, side, bench_over, plugged_over):
    """Everything about one motor's lead. side: +1 for the right motor (+Z), -1 for the left. bench_over / plugged_over: the
    corners its middle wire passes over on its way to its header, on the bench / in the car (it leaves the motor backwards, -X)."""
    chain = paths['chains'][motor]
    plug = W.plug(paths['plugs'][plug_id], g_towards=[0, 0, 1])     # (S at +Z, G at -Z on U1 and U2, as printed "S V G")
    exit_, across, ids = np.asarray(chain['leaves_servo_at'], float), np.asarray(chain['across'], float), lead_wires(name, 'Wheel Motor')
    top = plug['tops'][1]
    ends = dict(a=motor, b=plug_id)
    lead = dict(chain=chain, plug=plug, wires=ids, exit=exit_)
    # On the bench: lying on the table straight back from the motor, its plug flat, then up over the module and down onto its
    # header (the corners over the module moved back or forward until the lead is its own length).
    up = exit_ + MOTOR_ON_BENCH
    lying, lead['bench_loose_pose'] = lying_flat(to_length([up, up + [-6, 0, 0], [up[0] - 24, TABLE_Y + FLAT, up[2]], [up[0] - 60, TABLE_Y + FLAT, up[2]]], LEAD_MM, 8.0),
                                                 across, plug, [0.0, 0.0, 1.0])
    lead['bench_loose'] = routes(ids, lying, a_at=MOTOR_ON_BENCH, b_at=lead['bench_loose_pose'], **ends)
    over = lambda corners, s: [np.asarray(c, float) + [-s, 0.0, 0.0] for c in corners]
    bench = W.plugged_lead(fitted(lambda s: W.rounded([up, up + [-6, 0, 0], *over(bench_over, s), [top[0], top[1] + 14, top[2]], top], radius=8), LEAD_MM), across, plug)
    lead['bench_plugged'] = routes(ids, bench, a_at=MOTOR_ON_BENCH, **ends)
    above, lead['bench_above_pose'] = cut_lead(bench, plug, 10.0)  # held upright over its header, the lead coming straight down to it
    lead['bench_above'] = routes(ids, above, a_at=MOTOR_ON_BENCH, b_at=lead['bench_above_pose'], **ends)
    # In the hand (the motor into L5, L4 slid along the leads): straight back from the motor.
    straight, lead['hand_pose'] = W.loose_lead(to_length([exit_, exit_ + [-LEAD_MM, 0, 0]], LEAD_MM), across, plug)
    lead['hand'] = routes(ids, straight, b_at=lead['hand_pose'], **ends)
    # On L1 once the motors are in: out through the hole in L4 and L1's notch behind it, up onto L1 and back along it outside the
    # battery's hole, then round behind it, the plug lying flat on L1 pointing towards the middle of the car (the two plugs' ends
    # some 12 mm apart, either side of L2's tab).
    z, on_l1 = exit_[2], 909.23 + FLAT
    deck = [exit_, [704.0, exit_[1], z], [695.0, on_l1, z], [640.0, on_l1, z], [620.0, on_l1, z - side * 14.0], [620.0, on_l1, z - side * 60.0]]
    lying, lead['deck_pose'] = lying_flat(to_length(deck, LEAD_MM), across, plug, [1.0, 0.0, 0.0])
    lead['deck'] = routes(ids, lying, b_at=lead['deck_pose'], **ends)
    # Plugged in, in the car: out through L4, up behind it and over the module to its header.
    plugged = W.plugged_lead(fitted(lambda s: W.rounded([exit_, [705.0, exit_[1], z], *over(plugged_over, s), [top[0], top[1] + 14, top[2]], top], radius=8), LEAD_MM),
                             across, plug)
    lead['plugged'] = routes(ids, plugged, **ends)
    lead['plugged_mm'], lead['bench_mm'] = W.length(plugged[1]), W.length(bench[1])
    above, lead['above_pose'] = cut_lead(plugged, plug, 10.0)
    lead['above'] = routes(ids, above, b_at=lead['above_pose'], **ends)
    return lead


RIGHT_LEAD = motor_lead('right', MOTOR_R, PLUG_R, 1, bench_over=[[702.0, 952.0, 1372.0], [712.0, 958.0, 1340.0]],
                        plugged_over=[[699.0, 916.0, 1382.0], [704.0, 945.0, 1360.0], [722.0, 956.0, 1330.0]])
LEFT_LEAD = motor_lead('left', MOTOR_L, PLUG_L, -1, bench_over=[[700.0, 950.0, 1300.0], [706.0, 958.0, 1316.0]],
                       plugged_over=[[690.0, 912.0, 1292.35], [684.0, 935.0, 1296.0], [690.0, 952.0, 1308.0], [708.0, 958.0, 1318.0]])
for _lead in (RIGHT_LEAD, LEFT_LEAD):
    g.log.append(f"  lead {_lead['wires'][0].split()[0]}: plugged in {_lead['plugged_mm']:.1f} mm in the car, {_lead['bench_mm']:.1f} mm on the bench (loose {LEAD_MM:.0f} mm)")

# --- the battery clip's lead: two wires from the clip on the battery to the barrel plug. The CAD has it out of the socket and in.
BATTERY_LEAD = ['battery red', 'battery black']
for _wire, _colour in zip(BATTERY_LEAD, ('wire_red', 'cable_black')):   # (the colours of the stubs on the clip and the plug)
    g.wire(_wire, _colour, 0.68, name='Battery Clip')
OUT_OF_SOCKET = [-8.95, 0.0, 0.0]                                   # the barrel plug out of the power socket, as the CAD has it (NAUO28)
OVER_SOCKET = [-8.95, 14.0, 0.0]                                    # ... and lifted clear of the socket, its back against the battery: how it rides until plugged in
battery = paths['battery']
battery_in = {w: W.route(battery['plugged'][c], a=CLIP, b=BARREL) for w, c in zip(BATTERY_LEAD, ('red', 'black'))}
PICTURED_PLUG = [-30.0, -14.0, 22.0]                               # (in the parts list: the clip with its barrel plug laid out beside it on its lead)
g.part_picture('Battery Clip', poses={BARREL: PICTURED_PLUG},
               wires=[dict(colour=colour, radius=0.68, pts=W.curve(np.asarray(battery['plugged'][c][0]), np.subtract(battery['plugged'][c][1], battery['plugged'][c][0]),
                                                                   apply_pose(PICTURED_PLUG, battery['plugged'][c][-1]), [1.0, 0.0, 0.0], pull=14.0))
                      for colour, c in (('wire_red', 'red'), ('cable_black', 'black'))])


def battery_lead(plug_pose, battery_pose=ZERO):
    """The clip's lead from the clip (on the battery at `battery_pose`) to the barrel plug at `plug_pose`: on the bench the battery
    stands on the table, its clip higher than in the car, and the lead is a little longer than the CAD's so that it reaches."""
    out = {}
    for w, c in zip(BATTERY_LEAD, ('red', 'black')):
        line = np.asarray(battery['plugged'][c], float)
        start, end = line[0] + battery_pose, apply_pose(plug_pose, line[-1])
        out[w] = W.route(W.curve(start, line[1] - line[0], end, line[-1] - line[-2], pull=14.0), a=CLIP, b=BARREL,
                         a_at=battery_pose if battery_pose != ZERO else None, b_at=plug_pose if plug_pose != ZERO else None)
    return out


bench_battery_lead = lambda plug_pose: battery_lead(plug_pose, BATTERY_ON_BENCH)
battery_out = battery_lead(OVER_SOCKET)


# --- the USB cable: the Mini-B end, out of the controller's Nano Board, to the A end lying on the table beyond the grips
g.wire('usb cable', 'cable_black', 1.75, name='USB Cable')
usb_b, usb_a = paths['plugs'][USB_B], paths['plugs'].get(USB_A)
USB_B_EXIT = np.asarray(usb_b['cable_end_face_centre'], float)
if usb_a:
    USB_A_EXIT = np.asarray(usb_a['cable_end_face_centre'], float)
else:                                                               # (the A end lies along X, plug away from the controller: its cable leaves its +X end)
    _lo, _hi = g.model.inst[USB_A].bounds
    USB_A_EXIT = np.array([_hi[0], (_lo[1] + _hi[1]) / 2, (_lo[2] + _hi[2]) / 2])
USB_OUT = 30.0                                                      # the Mini-B end held this far out of its socket, before it goes in


def usb_cable(plug=0.0):
    a_at = [-plug, 0.0, 0.0] if plug else None
    start = USB_B_EXIT + (a_at or ZERO)
    return {'usb cable': W.route(W.curve(start, [-1, 0, 0], USB_A_EXIT, [-1, 0, 0], pull=20.0), a=USB_B, b=USB_A, a_at=a_at)}


# ---------------------------------------------------------------- the build
CONTROLLER = [BOARD, GUARD_LEFT, GUARD_RIGHT, CONTROLLER_NANO, CONTROLLER_RADIO, JOY_LEFT, JOY_RIGHT]

# ================================================================ THE CONTROLLER (begin)
# The guards go on first (the published guide has them on from the start): each is a tray round one half of the board that
# also holds the floor of a joystick pocket, so the board is laid face down and each guard pressed onto it.
GUARD_NOTE = ('How do the guards go on? The CAD has each as a tray under one half of the board (here pressed on with the board face '
              'down); your photo shows four rim pieces. And should they go on first, as here?')
g.place('Begin the controller with the controller board, printed side down. Press the left guard onto the half of the board with the L-JS socket.',
        move=[GUARD_LEFT], show=[BOARD], direction=[0, -1, 0], flip=True, labels={BOARD: 'Controller Board', GUARD_LEFT: 'Left Controller Guard'},
        review=GUARD_NOTE + ' Names to confirm: Controller Board, Left / Right Controller Guard, Nano Board, Radio Module, Joystick, USB Cable, '
                             'Nano I/O Module, Adapter Board, Wheel Motor, Wheel, 9V Battery, Battery Clip.')
g.place('Press the right guard onto the other half.', move=[GUARD_RIGHT], direction=[0, -1, 0], flip=True)

# The Nano Board and the radio module go straight down into their sockets (the CAD's sockets are solid blocks, so the generator
# cannot find the way in: set by hand, with the lead lines on the corner pins).
H_PIN_TOP = 927.04
g.place('Turn the controller over. Press a Nano Board into H1 and H2, its USB socket at the end of the board marked USB.', move=[CONTROLLER_NANO],
        direction=[0, 1, 0], hover=35,
        labels=[dict(id=CONTROLLER_NANO, text='Nano Board'), dict(text='H1', anchor=[733.0, H_PIN_TOP, 1120.53], id=BOARD, ring=False),
                dict(text='H2', anchor=[733.0, H_PIN_TOP, 1105.29], id=BOARD, ring=False)],
        lines_at=[[[x, 921.04, z], [x, H_PIN_TOP, z]] for x in (695.04, 730.60) for z in (1105.3, 1120.5)],
        review='A section card before this step with your photo of the controller board, its pin names boxed in red? (The player has text-only cards so far.)')
g.place('Press a radio module into the socket marked NRF24L01, so that the module lies over the board, away from the USB end.', move=[CONTROLLER_RADIO],
        direction=[0, 1, 0], hover=35,
        labels=[dict(id=CONTROLLER_RADIO, text='Radio Module'), dict(text='NRF24L01', anchor=[711.9, 927.24, 1130.6], id=BOARD, ring=False)],
        lines_at=[[[710.70, 921.74, 1126.75], [710.70, 927.24, 1126.75]], [[713.20, 921.74, 1134.25], [713.20, 927.24, 1134.25]]])

# Each joystick is set down into its pocket a few millimetres short of its socket, then pushed towards it until its pins are in
# (the published guide had it glide in sideways through the guard). L-JS / R-JS are right-angle sockets that open towards the
# pocket; the joystick's pins go 6 mm in.
JOY_NOTE = ('In the CAD the joystick\'s board overlaps the controller board at the end away from its socket (the cut-out is 31.6 mm, '
            'the joystick 34 mm): by 4 mm when it is in, 11 mm while it is set down short of its socket here, and its underside sits 2.8 mm '
            'into the guard\'s floor. How does the joystick really sit? And do its pins go into the '
            'top row of L-JS (as in the CAD)? If so, a caution here would say so.')
for joystick, side, socket, at, near in ((JOY_LEFT, 'left', 'L-JS', [725.75, 921.86, 1084.84], [1, 1, -1]), (JOY_RIGHT, 'right', 'R-JS', [725.62, 921.86, 1157.61], [1, 1, 1])):
    g.place(f'Set the {side} joystick into its pocket, then push it towards {socket} until its pins are all the way into the socket.', move=[joystick],
            path=[[-7.0, 35.0, 0.0], [-7.0, 0.0, 0.0], ZERO], look_from=near,
            lines_at=[[[731.75, 921.86, z], [at[0], at[1], z]] for z in (at[2] - 4.92, at[2] + 5.08)],   # (the two end pins into the socket's mouth)
            labels=[dict(id=joystick, text=f'{side.title()} Joystick'), dict(text=socket, anchor=at, id=BOARD, ring=False)],
            review=JOY_NOTE if side == 'left' else None)
# The controller is put aside while the car's electronics are put together; it comes back for the test.
g.put_away(CONTROLLER)
# ================================================================ THE CONTROLLER (end)

# ================================================================ ELECTRONICS TEST (begin)
# As on the MRA: the car's electronics are put together on the bench and tried before anything is built. The I/O module lies
# where the CAD has it (the chassis is not there yet); the motors stand on their wheels beside it and the battery behind it.
g.carry([PLUG_R], by=MODULE, pose=RIGHT_LEAD['bench_loose_pose'], appear=False)
g.carry([PLUG_L], by=MODULE, pose=LEFT_LEAD['bench_loose_pose'], appear=False)
g.place("Begin the car's electronics with the I/O module. Press the other Nano Board into it, its USB socket at the same end as the power socket.",
        move=[CAR_NANO], show=[MODULE], direction=[0, 1, 0], hover=35, labels={CAR_NANO: 'Nano Board', MODULE: 'Nano I/O Module'}, look_from=[-1, 1, 1],
        review="The published guide shows this Nano Board the other way round (USB socket towards the front); the CAD and the MRA have it at "
               "the power socket's end, as here. And the CAD's Nano Board here is a plainer model, so the controller's Nano Board is shown instead. "
               "Colours to confirm (materials.json _notes.unconfirmed): the wheel motors' blue (as published, or black?), the radio boards black or green, "
               "the wheels, the plug housings, silver or gold pins, the white boards; and is this I/O module the MRA's board (its printing is carried over)?")
g.place('Press the adapter board onto the I/O module, its sockets over the pins along the side, with U3 at the end away from the power socket.', move=[ADAPTER],
        direction=[0, 1, 0], hover=35, labels={ADAPTER: 'Adapter Board'},
        review='A section card before this step with your photo of the adapter board (U1 / LWh, U2 / RWh, U3, S V G)?',
        lines_at=[[[694.64, 920.08, 1318.43], [694.64, 925.91, 1318.43]], [[740.36, 920.08, 1323.51], [740.36, 925.91, 1323.51]]])
g.place('Press the other radio module into U3, so that it sticks out past the end of the I/O module.', move=[CAR_RADIO], direction=[0, 1, 0], hover=35,
        labels=[dict(id=CAR_RADIO, text='Radio Module'), dict(text='U3', anchor=[746.33, 938.88, 1320.97], id=ADAPTER, ring=False)],
        lines_at=[[[745.06, 933.38, 1317.28], [745.06, 938.88, 1317.28]], [[747.56, 933.38, 1324.78], [747.56, 938.88, 1324.78]]])

# The wheels: each motor appears standing beside the module, its lead loose on the table, and a wheel is pressed onto its shaft.
for motor, wheel, plug_id, lead, side, outwards in ((MOTOR_L, WHEEL_L, PLUG_L, LEFT_LEAD, 'left', -1), (MOTOR_R, WHEEL_R, PLUG_R, RIGHT_LEAD, 'right', 1)):
    g.rest_at([motor], MOTOR_ON_BENCH)
    g.carry([wheel], by=motor, pose=[0.0, 0.0, outwards * 40.0], appear=False)
    hub = g.model.inst[wheel].bounds.mean(0)
    g.place(f'Press a wheel onto the shaft of the {side} wheel motor.' if side == 'left' else 'Press the other wheel onto the right wheel motor.',
            appear=[motor, wheel, plug_id], ride={wheel: ZERO}, wires=lead['bench_loose'], lines=False,
            # (the wheel rides with a motor standing off its seat, so the generator cannot draw a lead line: an arrow along the axle)
            arrows=[dict(tail=(hub + [0.0, 0.0, outwards * 14.0]).tolist(), head=(hub - [0.0, 0.0, outwards * 26.0]).tolist(), normal=[0, 1, 0], part=wheel)],
            labels=[dict(id=wheel, text='Wheel'), dict(id=motor, text=f'{side.title()} Wheel Motor')],
            review=('Wheels on for the test, as in the published guide (the student sees them turn), or pressed on at the end of the build?'
                    if side == 'left' else None))

# The motors plugged in for the test: each plug is brought up over its header and pushed straight down.
BROWN_TO_G = 'Very important: the brown wire goes on G, the pin on the same side as the left wheel.'   # (G is at the car's left on U1 and U2)
for motor, plug_id, lead, side, header, printed in ((MOTOR_L, PLUG_L, LEFT_LEAD, 'left', 717.5, 'LWh'), (MOTOR_R, PLUG_R, RIGHT_LEAD, 'right', 730.2, 'RWh')):
    g.place(f'Plug the {side} wheel motor into {printed} for the test. Remember brown to G, red to V, and yellow to S.',
            ride={plug_id: [lead['bench_above_pose'], ZERO]}, lines=False, wires_done={w: [lead['bench_above'][w], lead['bench_plugged'][w]] for w in lead['wires']},
            labels=[dict(text=printed, anchor=[header, 938.68, 1320.97], id=ADAPTER, ring=False), dict(id=plug_id, text=f'{side.title()} Wheel Motor')],
            caution=BROWN_TO_G if side == 'left' else None,
            review=("The CAD and the published guide draw the signal wire yellow (the MRA's captions say orange): which is it on the kit's FS90R? "
                    "And how long is the lead? The CAD's two poses of each lead differ (71 mm loose, 110 / 165 mm plugged); both are drawn 115 mm here."
                    if side == 'left' else None))

# Power: the battery stands on the table behind the module; its clip goes on and its barrel plug into the power socket.
g.rest_at([BATTERY], BATTERY_ON_BENCH)
g.carry([CLIP], by=BATTERY, pose=[0.0, 30.0, 0.0], appear=False)
BENCH_PLUG_OUT = [-20.0, round(TABLE_Y + 4.3 - 925.05, 2), 12.0]    # the barrel plug lying loose on the table beside the battery, before it is plugged in
g.rest_at([BARREL], BENCH_PLUG_OUT)
POWER_NOTE = ('Power for the test: the 9V battery for the car, as here, and USB for the controller? Or USB for both (two cables)? The '
              'Testing Checklist below assumes the battery. And how long is the battery clip\'s lead? The CAD\'s is about 30 mm (drawn longer here on the bench).')
_clip = g.model.inst[CLIP].bounds.mean(0)
g.place('Snap the battery clip onto the 9V battery.', appear=[BATTERY, CLIP, BARREL], ride={CLIP: ZERO}, lines=False,
        arrows=[dict(tail=(_clip + [0.0, 2.0, 0.0]).tolist(), head=(_clip - [0.0, 24.0, 0.0]).tolist(), normal=[0.71, 0, 0.71], part=CLIP)],
        labels={BATTERY: '9V Battery', CLIP: 'Battery Clip'}, wires=bench_battery_lead(BENCH_PLUG_OUT), review=POWER_NOTE)
g.place("Plug the battery clip's barrel plug into the power socket on the I/O module.", move=[BARREL], path=[BENCH_PLUG_OUT, [-12.0, 0.0, 0.0], ZERO],
        lines_at=[[696.29, 925.05, 1354.06]], labels=[dict(id=BARREL, text='Battery Clip')], look_from=[-1, 1, 1],   # (from the side the plug lies on)
        wires_done=bench_battery_lead(ZERO))
# The controller comes back, and its USB cable goes in (a computer or a power bank at the other end).
g.place("Connect the USB cable to the controller's Nano Board.", move=[USB_B], show=CONTROLLER + [USB_A], direction=[-1, 0, 0], hover=USB_OUT,
        lines_at=[[[694.92, 933.05, 1112.91], [689.42, 933.05, 1112.91]]], labels={USB_B: 'USB Cable'},
        wires=usb_cable(USB_OUT), wires_done=usb_cable(), focus=CONTROLLER + [USB_B, USB_A], focus_pad=1.1,
        review='Should the Completed View show the controller with its USB cable in, as the published guide does (and as the last step here does)?')
# (The checklist's last line has the battery and the USB cable unplugged after the test, so they leave the bench with it.)
g.put_away(CONTROLLER + [USB_B, USB_A, BATTERY, CLIP, BARREL])
g.note('Testing Checklist\nGo through the following checklist to make sure you have tested each part of your RCC:\n'
       '•  The controller was powered on by connecting a Mini-USB cable to its Nano.\n'
       '•  The car was powered on by plugging in the 9V battery.\n'
       '•  Pushing the left joystick forward made the left wheel turn.\n'
       '•  Pushing the right joystick forward made the right wheel turn.\n'
       '•  Each wheel stopped when its joystick was released.\n'
       '•  The battery was unplugged and the Mini-USB cable disconnected after testing.',
       review="A placeholder: TechBox's RCC Testing Checklist is needed word for word, as for the MRA. Which joystick drives which wheel? "
              "Does the FS90R's stop trim need setting during the test?")
g.place('Unplug both wheel motors from the adapter board.', ride={PLUG_L: lifted(ZERO, 40.0), PLUG_R: lifted(ZERO, 40.0)}, lines=False, eye=[PLUG_L],
        caution='Set the controller, the battery, the wheel motors and the I/O module aside for now. You will use them again in a bit.')
g.put_away([MODULE, CAR_NANO, ADAPTER, CAR_RADIO, MOTOR_L, MOTOR_R, WHEEL_L, WHEEL_R, PLUG_L, PLUG_R])
# ================================================================ ELECTRONICS TEST (end)

# What rides with what from here on.
g.carry([WHEEL_R], by=MOTOR_R)
g.carry([WHEEL_L], by=MOTOR_L)
g.carry([PLUG_R], by=MOTOR_R, pose=RIGHT_LEAD['hand_pose'])
g.carry([PLUG_L], by=MOTOR_L, pose=LEFT_LEAD['hand_pose'])
g.carry([CAR_NANO, ADAPTER, CAR_RADIO], by=MODULE)
g.carry([CLIP], by=BATTERY)
g.carry([BARREL], by=BATTERY, pose=OVER_SOCKET)

# ================================================================ THE CHASSIS (begin)
# L2 and L3 go on with the car upside down. L2 cannot go straight in: its front end is a barbed hook that goes through the notch
# at the flat end of L1 and back over L1's top. So it comes in tilted (its rear end away from L1), its hook is slid over the end of
# the notch, and it is swung down onto L1 so that its two tabs go into the slots (a collision search against the CAD: cad_study.md 2.3).
HOOK = [765.0, 911.5, 1338.5]
hooked = lambda t: turned([0, 0, 1], 25.0, HOOK, t)
g.place('Begin the car with L1, engraved side down. Hook the end of L2 over the notch at the flat end of L1, then swing L2 down so its tabs go into the slots in L1.',
        move=[L2], show=[L1], path=[hooked([6.0, -40.0, 0.0]), via(hooked([6.0, 0.0, 0.0])), hooked(ZERO), ZERO], flip=True,
        labels={L1: 'L1', L2: 'L2'}, lines_at=[[617.5, 909.2, 1338.5], [675.7, 909.2, 1338.5]],
        review='One step with the hook-and-swing (as here), or two (hook it on, then swing it down)? And L1: FRONT and L1 are etched as in your '
               'drawing, on the top face (the CAD\'s L1 read upside down; FRONT is new).')
g.place('Push L3 onto L2 so its two tabs go into the short slots in L1.', move=[L3], flip=True)

# (The hand work starts afresh: from the turned-over L1 and L2 the view would otherwise turn L5 and the motor over as they appear.)
g.put_away([])
# The wheel motors, L5 and L4 are put together in the hand. Each motor's lead stands straight back from it; L4 is slid along the
# two leads, each plug passing through the hole at its end of L4.
g.place('Push the right wheel motor into one end of L5, its mounting tab through the slot, its wheel outwards and its wire pointing away from L5.',
        move=[MOTOR_R], show=[L5], against=[L5], staged=True, wires=RIGHT_LEAD['hand'],
        labels=[dict(id=MOTOR_R, text='Right Wheel Motor'), dict(id=L5, text='L5')])
g.place('Push the left wheel motor into the other end of L5 the same way.', move=[MOTOR_L], against=[L5, MOTOR_R], staged=True, wires=LEFT_LEAD['hand'],
        labels=[dict(id=MOTOR_L, text='Left Wheel Motor')])
L4_HOLES = [[714.62, 906.86, 1385.68], [714.62, 906.86, 1291.28]]   # the holes for the leads at the ends of L4
g.place("Pass each motor's plug through the hole at its end of L4, then slide L4 along the wires onto the motors.", move=[L4], against=[L5, MOTOR_R, MOTOR_L],
        staged=True, direction=[-1, 0, 0], hover=LEAD_MM + 20.0, lines_at=L4_HOLES,
        review='One step (as here, the published guide\'s plug-to-hole cue in words), or a step for each plug through L4 and then L4?')
g.seat("Turn the car the right way up. Lower L4 and L5, with the motors, onto L1: their tabs go into the slots in L1 and over L2, and each motor's wire into the notch behind it.",
       [L5, MOTOR_R, MOTOR_L, L4], direction=[0, 1, 0],
       wires_done={**RIGHT_LEAD['deck'], **LEFT_LEAD['deck']}, ride={PLUG_R: RIGHT_LEAD['deck_pose'], PLUG_L: LEFT_LEAD['deck_pose']})

# The I/O module, with everything on it, slides in from the front along the grooves in L5 and L4 until it stops against L2's fin;
# then L7 and L6 slide in from the front and lock it (their heads stop it coming forward).
g.place('Slide the I/O module, with everything on it, into the grooves in L5 and L4 from the front of the car, until it stops against L2.',
        move=[MODULE], direction=[1, 0, 0], hover=60, labels={MODULE: 'Nano I/O Module'},
        lines_at=[[[691.1, 917.7, z], [713.1, 917.7, z]] for z in (1312.6, 1364.4)])   # (the board's back corners, to the back of L4's grooves)
L67_NOTE = ("L7 and L6 go on after the I/O module, as in the published guide: their heads hold it in. They slide in under L1, so the car is "
            "shown turned over for them. Their codes are on the parts under L1: in the finished car they show only from below.")
g.place("Turn the car over. Slide L7 in from the front, through the slots in L5 and L4, on the left wheel's side of L2.", move=[L7], labels={L7: 'L7'},
        flip=True, review=L67_NOTE)
g.place("Slide L6 in the same way, on the right wheel's side of L2.", move=[L6], labels={L6: 'L6'}, flip=True)
# ================================================================ THE CHASSIS (end)

# ================================================================ WIRING AND POWER (begin)
# One plug per step: lifted off L1, brought upright over its header and pushed straight down.
for plug_id, lead, side, header, printed in ((PLUG_L, LEFT_LEAD, 'left', 717.5, 'LWh'), (PLUG_R, RIGHT_LEAD, 'right', 730.2, 'RWh')):
    g.place(f"{'Turn the car the right way up. ' if side == 'left' else ''}Reconnect the {side} wheel motor to {printed}. Remember brown to G, red to V, and yellow to S.",
            move=[plug_id],
            path=[lead['deck_pose'], via(lifted(lead['deck_pose'], 40.0)), lead['above_pose'], ZERO], lines=False,
            labels=[dict(text=printed, anchor=[header, 938.68, 1320.97], id=ADAPTER, ring=False), dict(id=plug_id, text=f'{side.title()} Wheel Motor')],
            wires_done={w: [lead['above'][w], lead['plugged'][w]] for w in lead['wires']}, caution=BROWN_TO_G if side == 'left' else None)
g.place('Push the 9V battery, clip at the top, down through the square hole in L1 into L3.', move=[BATTERY], direction=[0, 1, 0],
        labels={BATTERY: '9V Battery'}, wires=battery_out)
g.place("Plug the battery clip's barrel plug into the power socket on the I/O module.", move=[BARREL], path=[OVER_SOCKET, OUT_OF_SOCKET, ZERO],
        lines_at=[[696.29, 925.05, 1354.06]], labels=[dict(id=BARREL, text='Battery Clip')], wires_done=battery_in, focus=[BARREL, BATTERY, MODULE], focus_pad=1.3,
        review='Plugged in at the end, as here (the CAD has it in), or left out with a caution ("plug it in to drive, unplug it when you stop")?')
g.place("Connect the USB cable to the controller's Nano Board.", move=[USB_B], show=CONTROLLER + [USB_A], direction=[-1, 0, 0], hover=USB_OUT,
        lines_at=[[[694.92, 933.05, 1112.91], [689.42, 933.05, 1112.91]]], labels={USB_B: 'USB Cable'},
        wires=usb_cable(USB_OUT), wires_done=usb_cable(), focus=CONTROLLER + [USB_B, USB_A], focus_pad=1.1)
# ================================================================ WIRING AND POWER (end)

g.build()
