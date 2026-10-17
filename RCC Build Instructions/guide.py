"""Remote Controlled Car (RCC), full build: the controller, the car's electronics tried on the bench with the controller, then
the car. The build, in order.

Run from the project root:   python "RCC Build Instructions/guide.py"
It writes steps.json (what the player shows) and parts.json (the parts list).

First draft (15 Oct 2026). The order and the wiring follow TechBox's published Cadasio guide 19075 (docs/research/rcc/
cadasio_study.md), put right where that guide goes wrong (the car's Nano Board disappears and looks reversed, the battery is
never plugged in, the joysticks glide in through the guard, the test is half there); the geometry is the CAD's (docs/research/
rcc/cad_study.md). Lee's open decisions were yellow Review notes on their steps (all answered by 16 Oct 2026). One part or one action per step.

Lee's first round (16 Oct 2026): the controller guards come fitted to the controller board and the wheels to the wheel motors (no
steps for them; one part each, "Controller Board" and "Wheel Motor"); "9V Adapter" for the battery clip; brown, red and orange
leads; the 9V adapter and battery taken off as one before the motors are unplugged; the leads lie straight back along L1; the
cameras of Steps 6, 7, 16, 23, 25 - 28 as he gave them (the step numbers here are the new ones: Steps 1 and 2, the guards, and
Steps 10 and 11, the wheels, are gone, and a step is added before the motors are unplugged).

Lee's second and third rounds (16, 17 Oct 2026): see the kit's README.txt (the leads smooth and their lengths representative, the
adapter board's old holes filled, Step 24's camera Step 23's mirrored, the controller turned round from Step 29, the title page and
the Completed View closer in).
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
CONTROLLER_NANO = 'NANO_CONTROLLER'                                 # the controller's Nano Board: the MRA's export of the CAD's NAUO27 (materials.json "extra_parts")
BARREL = 'NAUO29'                                                   # the barrel plug on the battery clip's lead, as the CAD has it in the power socket
BOARD = 'NAUO30'                                                    # the controller board
# (Not used: the CAD poses each lead twice. NAUO21 / 22 are the same plugs lying loose, NAUO28 the barrel plug out of its
# socket, NAUO31 - 42 the leads' bodies, drawn as wires here; NAUO86 is the car's Nano as the CAD has it, a plainer model, and
# NAUO27 the controller's, whose export has sliver triangles across the board.)

NAMES = {L1: 'L1', L2: 'L2', L3: 'L3', L4: 'L4', L5: 'L5', L6: 'L6', L7: 'L7',
         CAR_RADIO: 'Radio Module', CONTROLLER_RADIO: 'Radio Module',
         JOY_LEFT: 'Joystick', JOY_RIGHT: 'Joystick', BATTERY: '9V Battery', CLIP: '9V Adapter', USB_B: 'USB Cable', USB_A: 'USB Cable',   # ("9V Adapter": Lee, 16 Oct 2026)
         MOTOR_R: 'Wheel Motor', MOTOR_L: 'Wheel Motor', PLUG_R: 'Wheel Motor', PLUG_L: 'Wheel Motor',
         MODULE: 'Nano I/O Module', CAR_NANO: 'Nano Board', CONTROLLER_NANO: 'Nano Board', ADAPTER: 'Adapter Board', BOARD: 'Controller Board'}
# The barrel plug comes on the 9V adapter's lead; the guards come fitted to the controller board, and the wheels to the wheel
# motors (Lee, 16 Oct 2026): one part each, no step to fit them.
PART_OF = {BARREL: CLIP, GUARD_LEFT: BOARD, GUARD_RIGHT: BOARD, WHEEL_R: MOTOR_R, WHEEL_L: MOTOR_L}
# The pointer names the two of each more exactly than the parts list does (as each is labelled when it comes in).
HOVER_NAMES = {JOY_LEFT: 'Left Joystick', JOY_RIGHT: 'Right Joystick', MOTOR_L: 'Left Wheel Motor', MOTOR_R: 'Right Wheel Motor',
               PLUG_L: 'Left Wheel Motor', PLUG_R: 'Right Wheel Motor'}
UNLISTED = [PLUG_R, PLUG_L, USB_A]                                  # named on hover only (a motor's plug; the USB cable is listed by its Mini-B end)
# How the parts list pictures a part, where the generator's own view does not suit: L1's FRONT / L1 and the controller board's
# print came out upside down; the adapter board is seen from above, so that its print shows; the wheel motor from its inner
# side, so that the motor shows and not only its wheel.
PART_VIEWS = {'L1': {'roll': 180}, 'Controller Board': {'roll': 180}, 'Adapter Board': {'dir': [0.45, 0.85, 0.25]},
              'Wheel Motor': {'dir': [-0.45, 0.55, 0.7]}}

# The parts list after the title page: one band per kind of part (as in the MRA guide). The controller's band holds the parts
# that go on the controller board (one Nano Board and one radio module of the two: Lee, 16 Oct 2026), so a band takes parts by
# their ids. The wood's bands are blue-grey, as the MRA's (Lee, 16 Oct 2026).
WOOD_BAND, WOOD_HALO = '#dbe4ef', '#8ea6c4'
ON_CONTROLLER = {BOARD, CONTROLLER_NANO, CONTROLLER_RADIO, JOY_LEFT, JOY_RIGHT}
PART_GROUPS = [
    ('Parts List', 'Controller', 'electronics', '#f9c0c0', '#ec8d8d', lambda n, i: i in ON_CONTROLLER),
    ('Parts List', 'Electronics', 'electronics', '#f9c0c0', '#ec8d8d', lambda n, i: n in ('Nano Board', 'Nano I/O Module', 'Adapter Board', 'Radio Module', 'USB Cable', '9V Battery', '9V Adapter')),
    ('Parts List', 'Motors', 'motors', '#d8edc6', '#a3cf84', lambda n, i: n == 'Wheel Motor'),
    ('Parts List (Cont.)', 'Chassis', 'wood', WOOD_BAND, WOOD_HALO, lambda n, i: re.fullmatch(r'L\d+', n)),
]


def parts_list(parts):
    """The parts list's pages for the parts this guide shows (see Guide(parts_list=)): a part whose pieces belong to two bands
    (a Nano Board on the controller and one in the car) is listed in each, with the number that band takes, and with the
    picture of the pieces that band takes where they have one of their own (the car's Nano Board, with its blue dot)."""
    natural = lambda p: [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', p['name'])]
    pages, used = {}, set()
    for page, title, icon, colour, halo, wanted in PART_GROUPS:
        items = []
        for p in parts:
            ids = [i for i in p['ids'] if i not in used and wanted(p['name'], i)]
            if ids:
                used.update(ids)
                own = next((a['picture'] for a in p.get('also', []) if set(ids) <= set(a['ids'])), p['picture'])
                items.append((dict(p, picture=own), round(p['qty'] * len(ids) / len(p['ids']))))
        if icon == 'wood':
            items.sort(key=lambda t: natural(t[0]))
        if not items:
            continue
        if icon == 'wood':
            title = f"{title} ({items[0][0]['name']}{' - ' + items[-1][0]['name'] if len(items) > 1 else ''})"
        for shown, _ in items:                                       # (the parts list entry itself, which parts.json keeps)
            p = next(q for q in parts if q['name'] == shown['name'])
            p['group'] = f"{p['group']} / {title}" if p.get('group') else title
        pages.setdefault(page, []).append(dict(title=title, icon=icon, colour=colour, halo=halo,
                                               items=[dict(name=p['name'], qty=qty, picture=p['picture']) for p, qty in items]))
    left = [p for p in parts if any(i not in used for i in p['ids'])]
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
          part='Full Build', names=NAMES, part_views=PART_VIEWS, part_of=PART_OF, unlisted=UNLISTED, hover_names=HOVER_NAMES, source='rcc.glb',
          codes=CODES, hero_azimuth=135,                            # the finished car from the front, on its left (the controller's) side, above
          parts_list=parts_list,
          copyright_line='© TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')
# The two Nano Boards look alike but for the dot on the processor (white on the controller's, blue on the car's: materials.json
# "stickers"), so the car's has a picture of its own where the parts list shows it (Lee, 16 Oct 2026).
g.part_picture('Nano Board', piece=CAR_NANO, file='Nano Board car')

# ---------------------------------------------------------------- wires
# The CAD's lead bodies are left out of the model (materials.json "omit"); the leads are drawn from wire-paths.json. A wheel
# motor's lead is three wires (brown on G, red on V, orange on S) ending in a plug, which rides on the loose end of the lead until
# a step plugs it in. The 9V adapter's lead is two wires (red, black) ending in the barrel plug.
paths = W.load(HERE / 'wire-paths.json')
LEAD_COLOURS = ['lead_brown', 'lead_red', 'lead_orange']            # G, V, S (orange, as the MRA's servos: Lee, 16 Oct 2026)
ZERO = [0.0, 0.0, 0.0]


def lead_wires(name, motor_name):
    ids = [f'{name} {c}' for c in ('brown', 'red', 'orange')]
    for wire_id, colour in zip(ids, LEAD_COLOURS):
        g.wire(wire_id, colour, 0.5, name=motor_name)
    return ids


def routes(ids, lines, **ends):
    """One route per wire of a lead."""
    return {wire_id: W.route(line, **ends) for wire_id, line in zip(ids, lines)}


def lifted(pose, mm, forward=0.0):
    """The same pose, raised by mm (and moved `forward` mm along +x)."""
    return [pose[0] + forward, pose[1] + mm, pose[2]] if isinstance(pose, list) else {**pose, 't': [pose['t'][0] + forward, pose['t'][1] + mm, pose['t'][2]]}


def to_length(corners, length, radius=6.0):
    """A line through `corners`, rounded, cut or carried on along its last leg to `length` mm."""
    line = W.rounded([np.asarray(c, float) for c in corners], radius=radius)
    extra = length - W.length(line)
    if extra <= 0:
        return W.along(line, 0, length)
    return W.join(line, W.straight(line[-1], line[-1] - line[-2], extra))


# The table: on the bench the I/O module lies on its underside; the motors stand on their wheels beside it and the battery on its
# end behind it, each where it goes in the car but lifted onto the table (the chassis is not there yet). The battery stands 18 mm
# further back than in the car, so that the barrel plug can be held in line with the power socket, 20 mm out, and pushed
# straight in (Lee, 16 Oct 2026).
TABLE_Y = float(g.model.inst[MODULE].bounds[0][1])
MOTOR_ON_BENCH = [0.0, round(TABLE_Y - float(g.model.inst[WHEEL_R].bounds[0][1]), 2), 0.0]
BATTERY_ON_BENCH = [-18.0, round(TABLE_Y - float(g.model.inst[BATTERY].bounds[0][1]), 2), 0.0]
LEAD_MM = 115.0                                                     # a motor's lead laid out straight: in the hand, and back over L1 and past it
BENCH_MM = 55.0                                                     # ... and laid out straight behind the motor on the bench (Steps 8, 9: see motor_lead)
HELD_MM = 15.0                                                      # how high a plug is held over its header before it is pushed down (Steps 8, 9, 25, 26)
DROP_MM = 12.0                                                      # the straight run of a plugged lead down into its plug
OUT_X = 714.0                                                       # in the car a lead runs straight back out of its motor to here (inside L4's hole, 0.9 mm short of its rear face), then turns up
Y_DECK = 909.23 + 0.5 + 1.0                                         # the middle of a lead running flat back over L1 (its top at y 909.23), 1 mm clear of it


def plug_at_end(plug, lines):
    """The pose of a lead's plug on the end of its three wires."""
    return W.plug_pose(plug, lines[1][-1], lines[1][-1] - lines[1][-2], lines[2][-1] - lines[0][-1])


def deck_line(exit_, side, length=LEAD_MM, rise_x=(715.5, 702.0), jog=0.8):
    """Straight back from the motor through L4's hole, up out of L1's notch (moving `jog` mm towards the notch's middle, so that
    the lead can lie flat in it), then on straight back just over L1 and past its rear edge into space: `length` mm in all."""
    x0, y0, z0 = exit_
    xs = np.arange(x0, rise_x[1] - 1e-9, -0.25)
    e = W.smootherstep((rise_x[0] - xs) / (rise_x[0] - rise_x[1]))
    line = W.resample(np.c_[xs, y0 + e * (Y_DECK - y0), z0 + side * jog * e], 0.5)
    return W.resample(W.join(line, W.straight(line[-1], [-1, 0, 0], length - W.length(line))), 1.0)


def rise(start, radius, degrees):
    """A bend of `radius` mm from heading -x up towards +y, `degrees` round (out of a notch, or up off the bench)."""
    a = np.asarray(start, float)
    th = np.radians(np.linspace(0.0, degrees, max(3, int(np.ceil(radius * np.radians(degrees) / 0.25)))))
    return np.c_[a[0] - radius * np.sin(th), a[1] + radius - radius * np.cos(th), np.full_like(th, a[2])]


def plugged_line(exit_, top, controls, out_x, bend=(10.0, 70.0), held=0.0, raise_controls=()):
    """A plugged lead's middle: out of the motor straight back to x = out_x, a bend up, then a smooth curve through `controls` to
    DROP_MM over the plug's middle top and straight down into it. held: the plug held that many mm over its header instead, each
    control point raised by raise_controls so that the lead stays smooth."""
    a = np.asarray(exit_, float)
    arc = rise([out_x, a[1], a[2]], *bend)
    end = np.asarray(top, float) + [0.0, held + DROP_MM, 0.0]
    cs = [np.asarray(c, float) + [0.0, raise_controls[i] if i < len(raise_controls) else 0.0, 0.0] for i, c in enumerate(controls)]
    mid = W.smooth([arc[-1], *cs, end], start_dir=arc[-1] - arc[-2], end_dir=[0, -1, 0], spacing=0.5)
    return W.resample(W.join(W.straight(a, [-1, 0, 0], a[0] - out_x), arc, mid, W.straight(end, [0, -1, 0], DROP_MM)), 1.0)


def flat_lead(line, across, plug, twist=(3.0, 15.0)):
    """A lead's three wires along `line`: leaving the motor on edge, turned flat (wide along its plug's G-to-S line, +Z) `twist` mm
    out (3 - 15 mm for a lead that lies back over L1; 8 - 22 mm, once it is up out of L1's narrow notch, for one that rises
    there), and into its plug (the RCC's motor leads in every shape of a plug's way in, so that no two such shapes are twisted the
    opposite way: blended by the player from one to the next, such shapes cross their wires over; in the hand they stay on edge)."""
    return W.ribbon(line, across, pitch=1.02, n=3, end_pitch=plug['pitch'], fan_mm=10.0, end_across=plug['across'], twist=twist)


def lead_into(head, top, heading, controls=(), run=6.0):
    """A lead's middle: `head` (its first part, as it leaves the motor), then a smooth curve (through `controls`) into its plug's
    top at `top`, coming into it along `heading` (the last `run` mm straight): the plug held with its tip along `heading`."""
    head, top, heading = np.asarray(head, float), np.asarray(top, float), W._unit(heading)
    mid = W.smooth([head[-1], *controls, top - heading * run], start_dir=head[-1] - head[-2], end_dir=heading, spacing=0.5)
    return W.resample(W.join(head, mid, W.straight(top - heading * run, heading, run)), 1.0)


def motor_lead(name, motor, plug_id, side, car, car_held, bench, bench_held):
    """Everything about one motor's lead. side: +1 for the right motor (+Z), -1 for the left. car / bench: the points its middle
    wire passes through on its way up and over to its header, in the car / on the bench (it leaves the motor backwards, -X);
    car_held / bench_held: how far each is raised while the plug is held HELD_MM over its header.
    A plug is brought to its header in four beats, its tip turning no more than a quarter turn in each (Lee, 17 Oct 2026: Steps 8,
    9, 25, 26 "less angular and more smooth"): lying back along its lead; picked up, tip up; carried over, tip forward; held over
    its header, tip down; pushed in. Each stop has a smooth shape of its own, all lying flat the same way, so that from stop to stop
    the lead changes between two like shapes (the player blends them bit by bit along their length: very unlike shapes fold).
    The lengths are representative (Lee, 16 and 17 Oct 2026: "I am not worried about the wires exact length ... you can lengthen
    them as needed to create a smooth path"): each shape is drawn as it looks best, smooth, without corners, and clear of every
    part, and the routes say `stretch`, so that from one shape to the next the lead stretches evenly (W.route)."""
    chain = paths['chains'][motor]
    plug = W.plug(paths['plugs'][plug_id], g_towards=[0, 0, 1])     # (S at +Z, G at -Z on U1 and U2, as printed "S V G")
    exit_, across, ids = np.asarray(chain['leaves_servo_at'], float), np.asarray(chain['across'], float), lead_wires(name, f'{name.title()} Wheel Motor')
    top = plug['tops'][1]
    z_out, z_in = exit_[2], top[2]
    ends = dict(a=motor, b=plug_id, stretch=True)
    lead = dict(chain=chain, plug=plug, wires=ids, exit=exit_)

    def stop(key, line, a_at=None, twist=(3.0, 15.0)):
        lines = flat_lead(line, across, plug, twist)
        lead[key + '_pose'] = plug_at_end(plug, lines)
        lead[key] = routes(ids, lines, a_at=a_at, b_at=lead[key + '_pose'], **ends)
        lead[key + '_mm'] = W.length(lines[1])

    def rising(start, out_x, bend):                                  # straight back out of the motor, then a bend up
        return W.join(W.straight(start, [-1, 0, 0], start[0] - out_x), rise([out_x, start[1], start[2]], *bend))
    # On the bench (Steps 8, 9): first laid out straight behind the motor (Lee, 17 Oct 2026: "start with their wires extended
    # straight to the rear"), BENCH_MM long so that its plug starts in Steps 8 and 9's close frames (at 115 mm it would start off
    # the screen); then picked up, carried over, held over its header and in, as above.
    up = exit_ + MOTOR_ON_BENCH
    stop('bench_straight', to_length([up, up + [-BENCH_MM, 0, 0]], BENCH_MM), a_at=MOTOR_ON_BENCH)
    stop('bench_lift', lead_into([up, up + [-12.0, 0, 0]], [up[0] - 33.0, up[1] + 17.0, z_out], [0, 1, 0]), a_at=MOTOR_ON_BENCH)
    stop('bench_over', lead_into(rising(up, up[0] - 1.5, (14.0, 80.0)), [up[0] + 3.0, up[1] + 37.0, z_out + 0.45 * (z_in - z_out)], [1, 0, 0]), a_at=MOTOR_ON_BENCH)
    stop('bench_held', plugged_line(up, top, bench, up[0] - 1.5, bend=(14.0, 80.0), held=HELD_MM, raise_controls=bench_held), a_at=MOTOR_ON_BENCH)
    plugged = flat_lead(plugged_line(up, top, bench, up[0] - 1.5, bend=(14.0, 80.0)), across, plug)
    lead['bench_plugged'], lead['bench_mm'] = routes(ids, plugged, a_at=MOTOR_ON_BENCH, **ends), W.length(plugged[1])
    lead['bench_lengths'] = [lead[k + '_mm'] for k in ('bench_straight', 'bench_lift', 'bench_over', 'bench_held')] + [lead['bench_mm']]
    # In the hand (Steps 18 - 20, the motor into L5, L4 slid along the leads): straight back from the motor, LEAD_MM long.
    hand, lead['hand_pose'] = W.loose_lead(to_length([exit_, exit_ + [-LEAD_MM, 0, 0]], LEAD_MM), across, plug)
    lead['hand'] = routes(ids, hand, b_at=lead['hand_pose'], **ends)
    # On L1 (Steps 21c - 24): out through the hole in L4, up out of L1's notch and straight back along its original path over L1
    # and on past L1's rear edge into space, its plug flat, LEAD_MM long (Lee, 17 Oct 2026: "their original length ... they can
    # just extend back beyond the rear of L1 as long as they don't clip / interfere with L1's body"). It turns flat as it comes
    # up out of the notch.
    middle = deck_line(exit_, side)
    stop('deck', middle)
    # Plugged in, in the car (Steps 25c, 26c on): out through L4, a bend up behind it, then a smooth curve over the module, clear of
    # L1 (Lee, 17 Oct 2026: it went into L1 by the notch), and straight down into its header; before that (Steps 25, 26) picked up
    # off L1, carried over and held HELD_MM over its header.
    stop('lift', lead_into(middle[middle[:, 0] >= 692.0], [668.0, 952.0, middle[-1][2]], [0, 1, 0]))
    stop('over', lead_into(rising(exit_, OUT_X, (10.0, 70.0)), [724.0, 988.0, z_out + 0.45 * (z_in - z_out)], [1, 0, 0]), twist=(8.0, 22.0))   # (forward of where it rises: no doubling back)
    stop('held', plugged_line(exit_, top, car, OUT_X, held=HELD_MM, raise_controls=car_held), twist=(8.0, 22.0))
    plugged = flat_lead(plugged_line(exit_, top, car, OUT_X), across, plug, (8.0, 22.0))
    lead['plugged'], lead['plugged_mm'] = routes(ids, plugged, **ends), W.length(plugged[1])
    lead['car_lengths'] = [lead[k + '_mm'] for k in ('deck', 'lift', 'over', 'held')] + [lead['plugged_mm']]
    return lead


# (The points each lead passes through: chosen for even bends, of about 6 mm radius or more, and for clearance from every part.)
RIGHT_LEAD = motor_lead('right', MOTOR_R, PLUG_R, 1,
                        car=[[705.7, 928.7, 1378.7], [719.0, 963.2, 1350.4], [727.5, 970.1, 1330.1]], car_held=[5.6, 10.1, 14.0],
                        bench=[[701.5, 966.8, 1381.9], [709.3, 980.3, 1362.3], [718.8, 982.2, 1342.6], [724.6, 978.4, 1331.0]], bench_held=[3.7, 7.3, 13.2, 15.0])
LEFT_LEAD = motor_lead('left', MOTOR_L, PLUG_L, -1,
                       car=[[699.9, 937.5, 1291.2], [699.0, 952.2, 1291.5], [712.7, 970.2, 1312.9]], car_held=[2.8, 10.3, 12.2],
                       bench=[[700.5, 971.8, 1292.8], [701.0, 979.7, 1299.5], [708.0, 980.0, 1314.4]], bench_held=[2.5, 10.3, 14.8])
for _lead in (RIGHT_LEAD, LEFT_LEAD):
    g.log.append(f"  lead {_lead['wires'][0].split()[0]}: {LEAD_MM:.0f} mm in the hand; in Steps 25 / 26 (on L1, lifted, carried over, held, in) "
                 f"{' / '.join(f'{x:.0f}' for x in _lead['car_lengths'])} mm; in Steps 8 / 9 (laid out, lifted, carried over, held, in) "
                 f"{' / '.join(f'{x:.0f}' for x in _lead['bench_lengths'])} mm")

# --- the 9V adapter's lead: two wires from the clip on the battery to the barrel plug. The CAD has it out of the socket and in.
# The clip and the plug each have a stub of each wire (6 mm and 3 mm long); the CAD's conductors start at the inner end of the
# clip's stubs and end at the plug's grip, so each wire is drawn from the end of its stub on the clip to the end of its stub on
# the plug, carrying on along both (Lee, 16 Oct 2026: they looked like stubs with other wires leaving beside them).
BATTERY_LEAD = ['battery red', 'battery black']
for _wire, _colour in zip(BATTERY_LEAD, ('wire_red', 'cable_black')):   # (the colours of the stubs on the clip and the plug)
    g.wire(_wire, _colour, 0.68, name='9V Adapter')
OUT_OF_SOCKET = [-8.95, 0.0, 0.0]                                   # the barrel plug out of the power socket, as the CAD has it (NAUO28)
CLIP_STUB, PLUG_STUB = 6.0, 3.0
battery = paths['battery']


def stub_ends(c):
    """Where conductor c leaves the end of its stub on the clip and where it meets the end of its stub on the plug (seated), and the
    way each stub points (clip: away from the clip; plug: into the plug)."""
    line = np.asarray(battery['plugged'][c], float)
    out, into = W._unit(line[1] - line[0]), W._unit(line[-1] - line[-2])
    return line[0] + out * CLIP_STUB, out, line[-1] - into * PLUG_STUB, into


def cad_lead(pose):
    """The CAD's own lead, in its pose 'plugged' or 'out', from stub end to stub end."""
    return {w: W.route(W.along(battery[pose][c], CLIP_STUB, W.length(battery[pose][c]) - PLUG_STUB), a=CLIP, b=BARREL,
                       b_at=OUT_OF_SOCKET if pose == 'out' else None) for w, c in zip(BATTERY_LEAD, ('red', 'black'))}


battery_in, battery_out = cad_lead('plugged'), cad_lead('out')
PICTURED_PLUG = [-30.0, -14.0, 22.0]                               # (in the parts list: the clip with its barrel plug laid out beside it on its lead)
g.part_picture('9V Adapter', poses={BARREL: PICTURED_PLUG},
               wires=[dict(colour=colour, radius=0.68, pts=W.curve(a, out, apply_pose(PICTURED_PLUG, b), into, pull=14.0))
                      for colour, (a, out, b, into) in (('wire_red', stub_ends('red')), ('cable_black', stub_ends('black')))])


def battery_lead(plug_pose, battery_pose=ZERO):
    """The 9V adapter's lead from the clip (on the battery at `battery_pose`) to the barrel plug at `plug_pose` (both moves):
    on the bench the battery stands on the table, and the lead is a little longer than the CAD's so that it reaches."""
    out = {}
    for w, c in zip(BATTERY_LEAD, ('red', 'black')):
        a, leaves, b, into = stub_ends(c)
        out[w] = W.route(W.curve(np.add(a, battery_pose), leaves, apply_pose(plug_pose, b), into, pull=14.0), a=CLIP, b=BARREL,
                         a_at=battery_pose if battery_pose != ZERO else None, b_at=plug_pose if plug_pose != ZERO else None)
    return out


bench_battery_lead = lambda plug_pose: battery_lead(plug_pose, BATTERY_ON_BENCH)


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
# From Step 29 the controller, with its USB cable, is turned round in place (180 degrees about the vertical through the controller
# board's middle), so that it faces the other way beside the car, and the build leaves it so: the title page and the Completed View
# show it that way (Lee, 16 Oct 2026: "facing the wrong way"; 17 Oct 2026: "Step 29 - the Controller should already be flipped
# around for the USB installation"). Steps 1 - 4 and the test (Step 12) show it as the CAD has it.
_lo, _hi = g.model.bounds([BOARD, GUARD_LEFT, GUARD_RIGHT])
CONTROLLER_POSE = turned([0, 1, 0], 180.0, ((_lo + _hi) / 2).round(2).tolist())
# The title page and the Completed View, much closer in (Lee, 17 Oct 2026: "WAY too zoomed out", with a picture of the title page
# as wanted, solved by matching renders to it). The title page's camera is the picture's; the Completed View has no title, so it is
# the same camera with the car and controller centred, and Step 29c glides into it. Where a window cannot show that (the title,
# a fixed size on the page, would cover the car in a small window such as the LMS's frame, or a narrow frame would cut the
# controller off), the player takes the first of CLOSER (moved aside just enough to clear the title) that fits, and in the end
# the whole finished model as before.
START_DIR = [0.5552, 0.7053, -0.4409]
CENTRED = [713.8, 911.6, 1199.7]                                    # (the car and controller centred in the frame, as in the picture)
CLOSER = [dict(dir=START_DIR, target=CENTRED, radius=r) for r in (125.0, 145.0, 170.0, 195.0)]
g.start_view = dict(dir=START_DIR, target=[742.4, 911.6, 1235.8], radius=110.0, shift=0, min_aspect=1.0, clear_title=True, otherwise=CLOSER)
g.end_view = dict(dir=START_DIR, target=CENTRED, radius=110.0, min_aspect=1.0, otherwise=CLOSER)

# ================================================================ THE CONTROLLER (begin)
# The guards come fitted to the controller board (Lee, 16 Oct 2026). The Nano Board and the radio module go straight down into
# their sockets (the CAD's sockets are solid blocks, so the generator cannot find the way in: set by hand, with the lead lines on
# the corner pins).
H_PIN_TOP = 927.04
g.place('Begin the controller with the controller board. Press a Nano Board into H1 and H2, its USB socket at the end of the board marked USB.',
        move=[CONTROLLER_NANO], show=[BOARD, GUARD_LEFT, GUARD_RIGHT], direction=[0, 1, 0], hover=35, look_from=[-1, 1, -1],
        labels={BOARD: 'Controller Board', CONTROLLER_NANO: 'Nano Board'},     # (no H1 / H2 labels: Lee, 16 Oct 2026)
        lines_at=[[[x, 921.04, z], [x, H_PIN_TOP, z]] for x in (695.04, 730.60) for z in (1105.3, 1120.5)])
g.place('Press a radio module into the socket marked NRF24L01, so that the module lies over the board, away from the USB end.', move=[CONTROLLER_RADIO],
        direction=[0, 1, 0], hover=35, labels={CONTROLLER_RADIO: 'Radio Module'},                 # (no NRF24L01 label: Lee)
        lines_at=[[[710.70, 921.74, 1126.75], [710.70, 927.24, 1126.75]], [[713.20, 921.74, 1134.25], [713.20, 927.24, 1134.25]]])

# Each joystick is set down into its pocket a few millimetres short of its socket, then pushed towards it until its pins are in
# (the published guide had it glide in sideways through the guard). L-JS / R-JS are right-angle sockets that open towards the
# pocket; the joystick's pins go 6 mm in, into the socket's top row (as the CAD has them; Lee, 16 Oct 2026: "the assembly model
# you made is perfect as it is, but we should add a caution for the joystick's pins to go into the top row").
for joystick, side, socket, at, near in ((JOY_LEFT, 'left', 'L-JS', [725.75, 921.86, 1084.84], [1, 1, -1]), (JOY_RIGHT, 'right', 'R-JS', [725.62, 921.86, 1157.61], [1, 1, 1])):
    g.place(f'Set the {side} joystick into its pocket, then push it towards {socket} until its pins are all the way into the socket.', move=[joystick],
            path=[[-7.0, 35.0, 0.0], [-7.0, 0.0, 0.0], ZERO], look_from=near,
            lines_at=[[[731.75, 921.86, z], [at[0], at[1], z]] for z in (at[2] - 4.92, at[2] + 5.08)],   # (the two end pins into the socket's mouth)
            labels={joystick: f'{side.title()} Joystick'},                                         # (no L-JS / R-JS label: Lee)
            caution=f"Make sure the joystick's pins go into the top row of {socket}, not the bottom row.")
# The controller is put aside while the car's electronics are put together; it comes back for the test.
g.put_away(CONTROLLER)
# ================================================================ THE CONTROLLER (end)

# ================================================================ ELECTRONICS TEST (begin)
# As on the MRA: the car's electronics are put together on the bench and tried before anything is built. The I/O module lies
# where the CAD has it (the chassis is not there yet); the motors stand on their wheels beside it and the battery behind it.
g.place("Begin the car's electronics with the I/O module. Press the other Nano Board into it, its USB socket at the same end as the power socket.",
        move=[CAR_NANO], show=[MODULE], direction=[0, 1, 0], hover=35, labels={CAR_NANO: 'Nano Board', MODULE: 'Nano I/O Module'}, look_from=[-1, 1, 1])
# (Its USB socket at the power socket's end, as the CAD and the MRA have it: the published guide has it the wrong way round. Lee, 16 Oct 2026.)
# (Steps 6 and 7 from the corner opposite Step 5's, above: Lee, 16 Oct 2026.)
g.place('Press the adapter board onto the I/O module, its sockets over the pins along the side, with U3 at the end away from the power socket.', move=[ADAPTER],
        direction=[0, 1, 0], hover=35, labels={ADAPTER: 'Adapter Board'}, look_from=[1, 1, -1],
        lines_at=[[[694.64, 920.08, 1318.43], [694.64, 925.91, 1318.43]], [[740.36, 920.08, 1323.51], [740.36, 925.91, 1323.51]],
                  [[739.2, 920.2, 1344.5], [739.2, 925.91, 1344.5]]])   # (the third, the 2-pin socket onto 3V3 / GND: Lee's point, 16 Oct 2026)
g.place('Press the other radio module into U3, so that it sticks out past the end of the I/O module.', move=[CAR_RADIO], direction=[0, 1, 0], hover=35,
        labels={CAR_RADIO: 'Radio Module'}, look_from=[1, 1, -1],                                  # (no U3 label: Lee)
        lines_at=[[[745.06, 933.38, 1317.28], [745.06, 938.88, 1317.28]], [[747.56, 933.38, 1324.78], [747.56, 938.88, 1324.78]]])

# The motors plugged in for the test (each comes with its wheel fitted: Lee, 16 Oct 2026): a motor stands beside the module, its
# lead laid out straight behind it; its plug is picked up, carried over, held over its header and pushed straight down, four beats,
# the lead keeping pace (see motor_lead) (Lee, 17 Oct 2026: "start with their wires extended straight to the rear instead of already bent
# and so near the target header ... the wire paths are very angular instead of smooth").
BROWN_TO_G = 'Very important: the brown wire goes on G, the pin on the same side as the left wheel.'   # (G is at the car's left on U1 and U2)
# Steps 8 - 10 keep their corner, closer in on what each one does: the motor, its plug and the adapter board; the battery, the 9V
# adapter and its barrel plug (Lee, 16 Oct 2026: "too far zoomed out ... even more zoomed in than Step 11").
BENCH_DIR = [-0.5792, 0.5736, 0.5792]
for motor, wheel, plug_id, lead, side, printed, frame in ((MOTOR_L, WHEEL_L, PLUG_L, LEFT_LEAD, 'left', 'LWh', ([722.6, 945.0, 1306.1], 66.1)),
                                                          (MOTOR_R, WHEEL_R, PLUG_R, RIGHT_LEAD, 'right', 'RWh', ([722.6, 945.0, 1363.9], 71.6))):
    g.rest_at([motor], MOTOR_ON_BENCH)
    g.carry([wheel], by=motor)
    g.place(f'Plug the {side} wheel motor into {printed} for the test. Remember brown to G, red to V, and orange to S.',
            move=[plug_id], appear=[motor, plug_id],                                                # (the plug on screen at the end of its lead as the step opens)
            path=[lead['bench_straight_pose'], lead['bench_lift_pose'], lead['bench_over_pose'], lead['bench_held_pose'], ZERO],
            lines=False, wires=lead['bench_straight'], wires_done={w: [lead[k][w] for k in ('bench_lift', 'bench_over', 'bench_held', 'bench_plugged')] for w in lead['wires']},
            view_dir=BENCH_DIR, frame=frame,                                                        # (their cameras as before: Lee, 16 Oct 2026)
            labels={motor: f'{side.title()} Wheel Motor'},                                          # (no LWh / RWh label: Lee)
            caution=BROWN_TO_G if side == 'left' else None)

# Power: the battery stands on the table behind the module; the 9V adapter snaps onto it, and its barrel plug, held in line with
# the power socket, goes straight in.
g.rest_at([BATTERY], BATTERY_ON_BENCH)
g.carry([CLIP], by=BATTERY, pose=[0.0, 30.0, 0.0], appear=False)
BENCH_PLUG_OUT = [-20.0, 0.0, 0.0]                                  # the barrel plug held in line with the power socket, 20 mm out
g.rest_at([BARREL], BENCH_PLUG_OUT)
# (The 9V battery powers the car and USB the controller for the test; the 9V adapter's lead is representative: Lee, 16 Oct 2026.)
_clip = g.model.inst[CLIP].bounds.mean(0)
CLIP_TOP = [641.67, 945.54, 1333.0]                                 # on the clip's top face, so the label's leader clears the arrow (Lee)
g.place('Snap the 9V adapter onto the 9V battery.', appear=[BATTERY, CLIP, BARREL], ride={CLIP: ZERO}, lines=False,
        # (the arrow's face turned to the camera, which looks from the -x, +z side: Lee, 16 Oct 2026, it was seen edge on)
        arrows=[dict(tail=(_clip + [0.0, 2.0, 0.0]).tolist(), head=(_clip - [0.0, 24.0, 0.0]).tolist(), normal=[-0.71, 0, 0.71], part=CLIP)],
        labels=[dict(id=BATTERY, text='9V Battery'), dict(id=CLIP, text='9V Adapter', anchor=CLIP_TOP)], wires=bench_battery_lead(BENCH_PLUG_OUT),
        view_dir=BENCH_DIR, focus=[BATTERY, CLIP, BARREL], focus_pad=1.25)
g.place("Plug the 9V adapter's barrel plug into the power socket on the I/O module.", move=[BARREL], path=[BENCH_PLUG_OUT, ZERO],
        lines_at=[[696.29, 925.05, 1354.06]], labels={BARREL: '9V Adapter'},   # (from the side the plug lies on; its camera as before Lee's first round)
        view_dir=[-0.5792, 0.5736, 0.5792], frame=([702.8, 945.0, 1338.4], 106.6), wires_done=bench_battery_lead(ZERO))
# The controller comes back, and its USB cable goes in (a computer or a power bank at the other end).
g.place("Connect the USB cable to the controller's Nano Board.", move=[USB_B], show=CONTROLLER + [USB_A], direction=[-1, 0, 0], hover=USB_OUT,
        lines_at=[[[694.92, 933.05, 1112.91], [689.42, 933.05, 1112.91]]], labels={USB_B: 'USB Cable'},
        wires=usb_cable(USB_OUT), wires_done=usb_cable(), focus=CONTROLLER + [USB_B, USB_A], focus_pad=1.1)
# (The Completed View shows the controller with its USB cable in, as the last step leaves it: Lee, 16 Oct 2026.)
g.put_away(CONTROLLER + [USB_B, USB_A, BATTERY, CLIP, BARREL])
g.note('Testing Checklist\nGo through the following checklist to make sure you have tested each part of your RCC:\n'
       '•  The controller was powered on by connecting a Mini-USB cable to its Nano.\n'
       '•  The car was powered on by plugging in the 9V battery.\n'
       '•  Pushing the left joystick forward made the left wheel turn.\n'
       '•  Pushing the right joystick forward made the right wheel turn.\n'
       '•  Each wheel stopped when its joystick was released.\n'
       '•  The battery was unplugged and the Mini-USB cable disconnected after testing.')
# (A placeholder: the test itself is handled in the curriculum, and Lee will work through this card's wording later, 16 Oct 2026.)
# After the checklist the battery is unplugged (Lee, 16 Oct 2026): the 9V adapter stays on it, and the two are set aside as one,
# the barrel plug pulled straight out of the socket. (They come back as they were, riding together, so that they can move off.)
SET_ASIDE = [-40.0, 0.0, 0.0]
g.carry([BATTERY], by=MODULE, pose=BATTERY_ON_BENCH, appear=False)
g.carry([CLIP], by=BATTERY, appear=False)
g.carry([BARREL], by=BATTERY, pose=[-c for c in BATTERY_ON_BENCH], appear=False)   # (plugged in while the battery stands on the bench)
g.place('Unplug the 9V adapter from the power socket, and set the battery aside with the 9V adapter still on it.',
        appear=[BATTERY, CLIP, BARREL], ride={BATTERY: np.add(BATTERY_ON_BENCH, SET_ASIDE).tolist()}, lines=False, labels=[], eye=[BARREL],
        wires=bench_battery_lead(ZERO))
g.put_away([BATTERY, CLIP, BARREL, PLUG_L, PLUG_R])
g.carry([PLUG_L, PLUG_R], by=MODULE, appear=False)                  # (plugged in by Steps 8 and 9; riding the module, they are lifted off together)
g.place('Unplug both wheel motors from the adapter board.', appear=[PLUG_L, PLUG_R], ride={PLUG_L: lifted(ZERO, 40.0), PLUG_R: lifted(ZERO, 40.0)}, lines=False, eye=[PLUG_L],
        wires={**LEFT_LEAD['bench_plugged'], **RIGHT_LEAD['bench_plugged']},
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
g.carry([BARREL], by=BATTERY, pose=OUT_OF_SOCKET)                   # in line with the power socket, so that it goes straight in (Lee)

# ================================================================ THE CHASSIS (begin)
# L2 and L3 go on with the car upside down. L2 cannot go straight in: its front end is a barbed hook that goes through the notch
# at the flat end of L1 and back over L1's top. So it comes in tilted (its rear end away from L1), its hook is slid over the end of
# the notch, and it is swung down onto L1 so that its two tabs go into the slots (a collision search against the CAD: cad_study.md 2.3).
HOOK = [765.0, 911.5, 1338.5]
hooked = lambda t: turned([0, 0, 1], 25.0, HOOK, t)
g.place('Begin the car with L1, engraved side down. Hook the end of L2 over the notch at the flat end of L1, then swing L2 down so its tabs go into the slots in L1.',
        move=[L2], show=[L1], path=[hooked([6.0, -40.0, 0.0]), via(hooked([6.0, 0.0, 0.0])), hooked(ZERO), ZERO], flip=True,
        view_dir=[-0.306, -0.2011, -0.9306], one_off_camera=True,           # (lower, from Lee's picture, 16 Oct 2026: solved by matching renders to it)
        labels=[dict(id=L1, text='L1', anchor=[618.0, 906.23, 1312.0]), dict(id=L2, text='L2')],   # (L1's on its round end, clear of L2 and its etching: Lee)
        lines_at=[[617.5, 909.2, 1338.5], [675.7, 909.2, 1338.5], [772.1, 914.3, 1339.0]])   # (the third, the hook into the notch: Lee, 16 Oct 2026)
# (One step with the hook-and-swing, and L1's FRONT / L1 etching as drawn: Lee, 16 Oct 2026, "perfect, no changes needed".)
g.place('Push L3 onto L2 so its two tabs go into the short slots in L1.', move=[L3], flip=True)

# (The hand work starts afresh: from the turned-over L1 and L2 the view would otherwise turn L5 and the motor over as they appear.)
g.put_away([])
# The wheel motors, L5 and L4 are put together in the hand. Each motor's lead stands straight back from it; L4 is slid along the
# two leads, each plug passing through the hole at its end of L4.
g.place('Push the right wheel motor into one end of L5, its mounting tab through the slot, its wheel outwards and its wire pointing away from L5.',
        move=[MOTOR_R], show=[L5], against=[L5], staged=True, wires=RIGHT_LEAD['hand'],
        labels={MOTOR_R: 'Right Wheel Motor', L5: 'L5'},
        view_dir=[0.5792, 0.5736, 0.5792], frame=([651.1, 906.9, 1343.3], 126.9))       # (its camera as before)
g.place('Push the left wheel motor into the other end of L5 the same way.', move=[MOTOR_L], against=[L5, MOTOR_R], staged=True, wires=LEFT_LEAD['hand'],
        labels={MOTOR_L: 'Left Wheel Motor'},
        view_dir=[0.5792, 0.5736, -0.5792], frame=([651.1, 906.9, 1338.4], 129.7))      # (its camera as before)
L4_HOLES = [[714.62, 906.86, 1385.68], [714.62, 906.86, 1291.28]]   # the holes for the leads at the ends of L4
g.place("Pass each motor's plug through the hole at its end of L4, then slide L4 along the wires onto the motors.", move=[L4], against=[L5, MOTOR_R, MOTOR_L],
        staged=True, direction=[-1, 0, 0], hover=LEAD_MM + 20.0, lines_at=L4_HOLES,    # (one step, as it is: Lee, 16 Oct 2026)
        view_dir=[0.5792, 0.5736, -0.5792], frame=([651.1, 906.9, 1338.4], 129.7))      # (its camera as before)
g.seat("Turn the car the right way up. Lower L4 and L5, with the motors, onto L1: their tabs go into the slots in L1 and over L2, and each motor's wire into the notch behind it.",
       [L5, MOTOR_R, MOTOR_L, L4], direction=[0, 1, 0],
       lines_at=[[740.7, 891.3, 1314.7], [713.8, 891.3, 1316.3], [713.7, 891.3, 1360.5], [740.6, 891.3, 1358.6]],   # (Lee's points, 16 Oct 2026)
       view_dir=[0.5792, 0.5736, -0.5792], frame=([682.0, 946.9, 1338.4], 138.0),     # (its camera as before)
       wires_done={**RIGHT_LEAD['deck'], **LEFT_LEAD['deck']}, ride={PLUG_R: RIGHT_LEAD['deck_pose'], PLUG_L: LEFT_LEAD['deck_pose']})

# The I/O module, with everything on it, slides in from the front along the grooves in L5 and L4 until it stops against L2's fin;
# then L7 and L6 slide in from the front and lock it (their heads stop it coming forward).
g.place('Slide the I/O module, with everything on it, into the grooves in L5 and L4 from the front of the car, until it stops against L2.',
        move=[MODULE], direction=[1, 0, 0], hover=60, labels={MODULE: 'Nano I/O Module'},
        view_dir=[0.5792, 0.5736, -0.5792], frame=([717.5, 911.5, 1338.4], 141.5),        # (as before: the leads lying on L1 moved, the camera does not)
        lines_at=[[[691.1, 917.7, z], [713.1, 917.7, z]] for z in (1312.6, 1364.4)])   # (the board's back corners, to the back of L4's grooves)
# (L7 and L6 go on after the I/O module, as in the published guide: their heads hold it in. They slide in under L1, so the car is
# shown turned over for them; their codes, under L1, show only from below. Lee, 16 Oct 2026: "perfect, no changes needed".)
L2_MID_Z = 1338.48                                                  # L2's mid-plane (NAUO2 runs from z 1336.98 to 1339.98): the car is symmetric about it
STEP23_CAMERA = dict(view_dir=[0.6103, -0.515, -0.6019], frame=([734.8, 938.1, 1330.3], 118.2))   # (Lee's picture, 16 Oct 2026)


def mirrored(cam):
    """The same camera from the other side of L2."""
    (x, y, z), r = cam['frame']
    return dict(view_dir=[cam['view_dir'][0], cam['view_dir'][1], -cam['view_dir'][2]], frame=([x, y, round(2 * L2_MID_Z - z, 1)], r))


g.place("Turn the car over. Slide L7 in from the front, through the slots in L5 and L4, on the left wheel's side of L2.", move=[L7], labels={L7: 'L7'},
        flip=True, one_off_camera=True, **STEP23_CAMERA)
g.place("Slide L6 in the same way, on the right wheel's side of L2.", move=[L6], labels={L6: 'L6'}, flip=True,
        **mirrored(STEP23_CAMERA))                                  # (Step 23's camera, from the other side: Lee, 17 Oct 2026)
# ================================================================ THE CHASSIS (end)

# ================================================================ WIRING AND POWER (begin)
# One plug per step: picked up off the end of its lead (which runs back past L1) and turned upright, carried over the module high
# enough to clear the plug already in and its lead (U1 and U2 are side by side: the right plug passed through the left one on its
# way, Lee, 16 Oct 2026), lowered over its header and pushed straight down; closer in than the steps around them, so that the wires
# show (Lee). Four beats, the lead keeping pace with the plug stop by stop, a smooth shape of its own at each stop (lifted, carried
# over, held, in: motor_lead), so that the move is not rushed (Lee, 16 Oct 2026: "a little rapid / doesn't look smooth") and the
# lead is smooth throughout (Lee, 17 Oct 2026: "less angular and more smooth").
for plug_id, lead, side, printed in ((PLUG_L, LEFT_LEAD, 'left', 'LWh'), (PLUG_R, RIGHT_LEAD, 'right', 'RWh')):
    g.place(f"{'Turn the car the right way up. ' if side == 'left' else ''}Reconnect the {side} wheel motor to {printed}. Remember brown to G, red to V, and orange to S.",
            move=[plug_id],
            path=[lead['deck_pose'], lead['lift_pose'], lead['over_pose'], lead['held_pose'], ZERO], lines=False,
            # (up and forward, as the lead behind it is straight; then across high, over the other plug and its lead, down over its header, in)
            labels={plug_id: f'{side.title()} Wheel Motor'},                                        # (no LWh / RWh label: Lee)
            view_dir=[-0.5792, 0.5736, -0.5792], frame=([675.8, 928.0, 1338.5], 93.3),     # (their closer cameras as before)
            wires_done={w: [lead[k][w] for k in ('lift', 'over', 'held', 'plugged')] for w in lead['wires']}, caution=BROWN_TO_G if side == 'left' else None)
# (Steps 27 and 28: Lee's picture, 16 Oct 2026, solved by matching renders to it; the model then let down 4% of the frame, so that
# the battery clears the caption and its label has room above it: the picture was cut off just under the caption.)
BATTERY_VIEW = dict(view_dir=[-0.6337, 0.5821, 0.5095], frame=([690.1, 926.7, 1346.5], 76.4))
g.place('Push the 9V battery, clip at the top, down through the square hole in L1 into L3.', move=[BATTERY], direction=[0, 1, 0],
        labels=[dict(id=BATTERY, text='9V Battery', anchor=[633.1, 932.0, 1340.0])], wires=battery_out, **BATTERY_VIEW)   # (on the face towards the camera, high up)
g.place("Plug the 9V adapter's barrel plug into the power socket on the I/O module.", move=[BARREL], path=[OUT_OF_SOCKET, ZERO],
        lines_at=[[696.29, 925.05, 1354.06]], labels={BARREL: '9V Adapter'}, wires_done=battery_in, **BATTERY_VIEW)
# (Plugged in at the end, as the CAD has it: Lee, 16 Oct 2026, "fine for now".)
# The controller comes back turned round (CONTROLLER_POSE), everything on it riding with the board, the USB cable's Mini-B end held
# USB_OUT out of its socket; it slides straight in. (A moving part ends at its seat, so the plug rides instead: ride= ZERO.)
USB_TIP, USB_MOUTH = [694.92, 933.05, 1112.91], [689.42, 933.05, 1112.91]   # (the plug's tip, as built; the socket's mouth)
g.rest_at([BOARD], CONTROLLER_POSE)
g.carry([GUARD_LEFT, GUARD_RIGHT, CONTROLLER_NANO, CONTROLLER_RADIO, JOY_LEFT, JOY_RIGHT, USB_A], by=BOARD)
g.carry([USB_B], by=BOARD, pose=[-USB_OUT, 0.0, 0.0])
g.place("Connect the USB cable to the controller's Nano Board.", appear=[BOARD], ride={USB_B: ZERO},
        lines_at=[[apply_pose(CONTROLLER_POSE, np.add(USB_TIP, [-USB_OUT, 0.0, 0.0])).round(2).tolist(), apply_pose(CONTROLLER_POSE, USB_MOUTH).round(2).tolist()]],
        lines_to=CONTROLLER + [USB_B],                                     # (so that the points are checked against the turned controller and plug)
        labels={USB_B: 'USB Cable'}, wires=usb_cable(USB_OUT), wires_done=usb_cable(), focus=CONTROLLER + [USB_B, USB_A], focus_pad=1.1, look_from=[1, 1, -1])
# ================================================================ WIRING AND POWER (end)

g.build()
