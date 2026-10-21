"""Piano Memory Game (PMG), full build: the electronics wired on the bench (the Nano Board, four push buttons, the 4-digit display, the
dot matrix display, the USB cable), then the wooden case, with the electronics fitted into it as it goes up. The build, in order.

Run from the project root:   python "PMG Build Instructions/guide.py"
It writes steps.json (what the player shows) and parts.json (the parts list).

First draft (19 Oct 2026). The order, the wiring and the cameras' sides follow TechBox's published Cadasio guide 19075
(docs/research/guide_19075-piano_memory_game_pmg-full_build.md, docs/research/pmg/cadasio_map.md); the geometry is the CAD's
(pmg-guide.glb, cut from Lee's STEP by make_source.py: docs/research/pmg/cad_study.md). Where the STEP is an earlier version of the
model than the published guide's (two wires per button, the I/O module upside down on the back panel), this follows the published
guide, which is what students build from (make_source.py; questions for Lee in the README). One part or one action per step.

How the guide is put together. The CAD has a copy of most parts in each place the engineer posed them (on the bench, held over the
case, built); the guide uses one copy of each, where it sits in the finished game, and every other place is a pose of it
(cad-geometry.json, measured by make_source.py). On the bench everything lies away from where it is built, so what moves there
rides on the I/O module (the Nano Board pressed in, the jumper wires' caps plugged on, the USB cable's plug) and moves by changing
how it rides; a part goes to its own seat only in the case. Each jumper wire is its two caps (CAD parts) and the wire the player
draws between them; it changes shape step by step.
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
import trimesh

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
import wires as W  # noqa: E402
import routing as R  # noqa: E402
from stepgen import Guide, _matrix, apply_pose, compose, relative_pose, turn_dir, turned, via  # noqa: E402

GEO = json.load(open(HERE / 'cad-geometry.json'))
CAPS, POSES, USB = GEO['caps'], GEO['poses'], GEO['usb']
LINES = W.load(HERE / 'wire-paths.json')['lines']
ZERO = [0.0, 0.0, 0.0]

# ---------------------------------------------------------------- parts
# CAD instance ids (pmg-guide.glb). The case's front, where the student sits, is -X (H1 and the ends of the keys); up is +Y; the
# student's right is +Z. Every wood part's CAD name is the code engraved on it (the "v2" of H4, H11, H12, H13 is not engraved).
H1, H2, H3, H4, H5, H6, H7, H8 = 'NAUO63', 'NAUO65', 'NAUO66', 'NAUO73', 'NAUO67', 'NAUO60', 'NAUO68', 'NAUO61'
KEYS = ['NAUO72', 'NAUO71', 'NAUO70', 'NAUO69']                     # the four H9 piano keys, over the black, yellow, white and blue buttons
H10, H11, H12, H13, H14 = 'NAUO64', 'NAUO62', 'NAUO77', 'NAUO75', 'NAUO74'
MODULE, NANO = 'NAUO78', 'NANO'                                    # the Nano I/O module (the MRA's); the Nano Board (the MRA's, make_source.py)
BUTTONS = ['NAUO76', 'NAUO83', 'NAUO84', 'NAUO85']                 # push buttons: black (D4), yellow (D5), white (D6), blue (D7), left to right
COLOURS = ['black', 'yellow', 'white', 'blue']
DISPLAY, MATRIX = 'NAUO79', 'NAUO81'                               # the TM1637 4-digit display; the 32 x 8 dot matrix display (MAX7219)
USB_B, USB_A = 'NAUO282', 'NAUO283'                                # the USB cable's right-angle Mini-B end, and its A end
JUMPER_CAPS = sorted(CAPS)                                         # the 42 caps of the 21 jumper wires (each on its pin, built)
WOOD = {H1: 'H1', H2: 'H2', H3: 'H3', H4: 'H4', H5: 'H5', H6: 'H6', H7: 'H7', H8: 'H8', **{k: 'H9' for k in KEYS},
        H10: 'H10', H11: 'H11', H12: 'H12', H13: 'H13', H14: 'H14'}

NAMES = {**WOOD, MODULE: 'Nano I/O Module', NANO: 'Nano Board', **{b: 'Push Button' for b in BUTTONS}, DISPLAY: '4-Digit Display',
         MATRIX: 'Dot Matrix Display', USB_B: 'USB Cable', USB_A: 'USB Cable', **{c: 'Breadboard Wire (F-F)' for c in JUMPER_CAPS}}
# (The names of the published guide's section cards: "Nano I/O Module", "Push Buttons", "4-Digit Display", "Dot Matrix Display", "USB
# Cable"; the jumper wires' is the MRA's.)
HOVER_NAMES = {b: f'{c.title()} Push Button' for b, c in zip(BUTTONS, COLOURS)}
UNLISTED = [USB_A] + JUMPER_CAPS                                   # named on hover only (the USB cable is listed by its Mini-B end)

WOOD_BAND, WOOD_HALO = '#dbe4ef', '#8ea6c4'                        # (the MRA's and RCC's wood bands)
PART_GROUPS = [
    ('Parts List', 'Electronics', 'electronics', '#f9c0c0', '#ec8d8d',
     lambda n, i: n in ('Nano I/O Module', 'Nano Board', 'Push Button', '4-Digit Display', 'Dot Matrix Display', 'Breadboard Wire (F-F)', 'USB Cable')),
    ('Parts List (Cont.)', 'Case', 'wood', WOOD_BAND, WOOD_HALO, lambda n, i: re.fullmatch(r'H\d+', n)),
]


def parts_list(parts):
    """The parts list's pages for the parts this guide shows (see Guide(parts_list=)), one band per kind of part, as the RCC's."""
    natural = lambda p: [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', p['name'])]
    pages, used = {}, set()
    for page, title, icon, colour, halo, wanted in PART_GROUPS:
        items = []
        for p in parts:
            ids = [i for i in p['ids'] if i not in used and wanted(p['name'], i)]
            if ids:
                used.update(ids)
                items.append((p, round(p['qty'] * len(ids) / len(p['ids']))))
        if icon == 'wood':
            items.sort(key=lambda t: natural(t[0]))
        if not items:
            continue
        if icon == 'wood':
            title = f"{title} ({items[0][0]['name']}{' - ' + items[-1][0]['name'] if len(items) > 1 else ''})"
        for shown, _ in items:
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


# The engraved code on each wood part (the way its face looks, the middle of the code, seated: cad_study.md 2.2), so the camera
# prefers a side from which it can be read. H5, H6 and H7's are on their undersides (read with the case turned over).
CODES = {H1: ([-1, 0, 0], [460.37, 895.43, 1348.46]), H2: ([0, 0, 1], [579.17, 902.27, 1360.17]), H3: ([0, 0, -1], [578.95, 902.17, 1220.77]),
         H4: ([1, 0, 0], [590.36, 894.35, 1348.62]), H5: ([0, -1, 0], [565.01, 900.08, 1232.30]), H6: ([0, -1, 0], [470.64, 897.37, 1232.01]),
         H7: ([0, -1, 0], [470.80, 894.37, 1231.97]), H8: ([-1, 0, 0], [539.66, 925.25, 1350.13]),
         KEYS[3]: ([0, 1, 0], [534.35, 916.34, 1348.87]), KEYS[2]: ([0, 1, 0], [534.35, 916.34, 1315.61]),
         KEYS[1]: ([0, 1, 0], [534.35, 916.34, 1282.28]), KEYS[0]: ([0, 1, 0], [534.35, 916.34, 1248.94]),
         H10: ([0, 1, 0], [580.56, 934.08, 1347.10]), H11: ([0, 0, 1], [576.15, 956.09, 1311.46]), H12: ([0, 0, -1], [576.48, 955.66, 1269.52]),
         H13: ([0.643, 0.766, 0], [573.33, 975.94, 1290.22]), H14: ([-0.766, 0.643, 0], [547.55, 971.72, 1262.19])}

# Parts list pictures (Lee's first round): the I/O module and the Nano Board from their component side; H5, H6, H7, H9 and H10 the
# right way up; H13 and H14 face on. (The push buttons are pictured by the yellow one: part_picture below.)
PART_VIEWS = {'Nano I/O Module': {'dir': [0.78, 0.36, 0.51]}, 'Nano Board': {'dir': [0.78, 0.36, 0.51]},
              **{code: {'roll': 180} for code in ('H5', 'H6', 'H7', 'H9', 'H10')},
              'H13': {'dir': [0.45, 0.86, -0.27], 'up': [-0.766, 0.643, 0.0], 'roll': 180}, 'H14': {'dir': [-0.587, 0.763, 0.263], 'up': [0.643, 0.766, 0.0]}}

g = Guide(HERE, title='Piano Memory Game (PMG)', part='Full Build', names=NAMES, unlisted=UNLISTED, hover_names=HOVER_NAMES, part_views=PART_VIEWS,
          source='pmg-guide.glb', codes=CODES, hero_azimuth=315,       # the finished game from the front, on the student's right, above (as published)
          parts_list=parts_list, copyright_line='© TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')


# ---------------------------------------------------------------- geometry helpers
def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def shift(v):
    return [float(x) for x in v]


def cap_end(cap, pose=None):
    """Where a cap's wire end is, and the way the wire leaves it, with the cap at `pose` (None: on its pin, built)."""
    c = CAPS[cap]
    return np.asarray(apply_pose(pose, c['wire_end']), float), unit(turn_dir(pose, c['out']))


def lying(cap, centre, out):
    """The pose that lays a cap with its middle at `centre` and its wire end towards `out` (a cap of a loose wire)."""
    c0, o0, o = np.asarray(CAPS[cap]['centre'], float), unit(CAPS[cap]['out']), unit(out)
    axis = np.cross(o0, o)
    s, c = float(np.linalg.norm(axis)), float(o0 @ o)
    if s < 1e-9:
        axis, angle = (np.array([0.0, 1.0, 0.0]) if abs(o0[1]) < 0.9 else np.array([1.0, 0.0, 0.0])), (0.0 if c > 0 else 180.0)
    else:
        axis, angle = axis / s, float(np.degrees(np.arctan2(s, c)))
    return turned(axis.round(6).tolist(), round(angle, 4), c0.round(3).tolist(), (np.asarray(centre, float) - c0).round(3).tolist())


def along_out(cap, pose, mm):
    """The cap at `pose`, moved `mm` further out along its own axis (held over its pin before it is pushed on)."""
    return compose(shift(turn_dir(pose, CAPS[cap]['out']) * mm), pose, CAPS[cap]['centre'])


def refit(points, start, end):
    """A CAD wire's centre line with its ends moved onto `start` and `end` (the moves blended along its length)."""
    p = np.asarray(points, float)
    if np.linalg.norm(p[0] - start) > np.linalg.norm(p[-1] - start):
        p = p[::-1]
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    s = (s / s[-1])[:, None]
    return p + (1 - s) * (np.asarray(start) - p[0]) + s * (np.asarray(end) - p[-1])


def jumper(a, a_out, b, b_out, controls=(), lead=6.0):
    """A smooth jumper wire from wire end `a` (leaving along a_out) to wire end `b` (going in against b_out), through `controls`."""
    a, b, a_out, b_out = np.asarray(a, float), np.asarray(b, float), unit(a_out), unit(b_out)
    pts = [a, a + a_out * lead, *[np.asarray(c, float) for c in controls], b + b_out * lead, b]
    return W.resample(W.smooth(pts, start_dir=a_out, end_dir=-b_out, spacing=0.5), 1.0)


# ---------------------------------------------------------------- the electronics on the bench
# The bench: the I/O module lies flat, pins up, as on the MRA (its USB end towards the student's right); the push buttons stand in a
# row in front of it, pins down; the display to its left; the dot matrix to its right, its input header towards the module. Every
# place is the CAD's (or the published project's) pose copy. The table is the bench module's underside (bench_y).
MODULE_BENCH = POSES['module_bench']
BENCH_Y = GEO['bench_y']
BUTTON_BENCH = [POSES[f'button{k + 1}_bench'] for k in range(4)]
DISPLAY_BENCH, MATRIX_BENCH = POSES['display_bench'], POSES['matrix_bench']
CAP_ON = {(c['device'], c['pin']): cap for cap, c in CAPS.items()}

# The 21 jumper wires, in the published guide's order (each module wired pin by pin, in the order of its header), with the
# published guide's colours (one per wire, in the ribbon's order: rulebook section 8).
WIRES = [  # (device, its pin, the module pin, colour)
    (BUTTONS[0], 'VCC', 'V4', '#b70101'), (BUTTONS[0], 'OUT', 'S4', '#e4e4e4'), (BUTTONS[0], 'GND', 'G4', '#343232'),
    (BUTTONS[1], 'VCC', 'V5', '#21f17a'), (BUTTONS[1], 'OUT', 'S5', '#7c5a30'), (BUTTONS[1], 'GND', 'G5', '#ffdc00'),
    (BUTTONS[2], 'VCC', 'V6', '#85144b'), (BUTTONS[2], 'OUT', 'S6', '#737980'), (BUTTONS[2], 'GND', 'G6', '#3876ac'),
    (BUTTONS[3], 'VCC', 'V7', '#a75294'), (BUTTONS[3], 'OUT', 'S7', '#ff4136'), (BUTTONS[3], 'GND', 'G7', '#3d9970'),
    (DISPLAY, 'CLK', 'S8', '#ac9400'), (DISPLAY, 'DIO', 'S9', '#000000'), (DISPLAY, 'VCC', 'V9', '#ab53ca'), (DISPLAY, 'GND', 'G9', '#bb3d3d'),
    (MATRIX, 'VCC', 'V11', '#411900'), (MATRIX, 'GND', 'G11', '#339f3f'), (MATRIX, 'DIN', 'S11', '#2a2f62'), (MATRIX, 'CS', 'S12', '#662639'),
    (MATRIX, 'CLK', 'S13', '#377e89')]
DEVICE_NAME = {**{b: f'{c} push button' for b, c in zip(BUTTONS, COLOURS)}, DISPLAY: '4-digit display', MATRIX: 'dot matrix display'}
WIRE_ID = {}
for device, pin, row, colour in WIRES:
    wire_id = f"{DEVICE_NAME[device].replace(' push button', '')} {pin}"
    WIRE_ID[(device, pin)] = wire_id
    g.wire(wire_id, colour, 0.625, name='Breadboard Wire (F-F)')
DEV_CAP = {w: CAP_ON[(d, p)] for (d, p), w in WIRE_ID.items()}                 # wire -> the cap on the device's pin
MOD_CAP = {WIRE_ID[(d, p)]: CAP_ON[(MODULE, row)] for d, p, row, _ in WIRES}   # wire -> the cap on the module's pin
ALL_WIRES = [WIRE_ID[(d, p)] for d, p, _, _ in WIRES]

# Where each pin is (for its label): on the device and on the module, seated, where the cap will go.
pin_tip = lambda cap: CAPS[cap]['pin_tip']

# --- the jumper caps ride on the I/O module while it lies on the bench (it never moves there): a cap of a loose wire lies on the
# bench, and plugging it on is a change in how it rides (to its pin, on its device's bench place).
HUB = lambda cap, world: relative_pose(MODULE_BENCH, world, CAPS[cap]['centre'])
DEVICE_BENCH = {**dict(zip(BUTTONS, BUTTON_BENCH)), DISPLAY: DISPLAY_BENCH, MATRIX: MATRIX_BENCH}
on_bench = lambda wire, end: DEVICE_BENCH[WIRE_DEVICE[wire]] if end == 'a' else MODULE_BENCH   # where a wire's cap is once plugged on
WIRE_DEVICE = {WIRE_ID[(d, p)]: d for d, p, _, _ in WIRES}
WIRE_ROW = {WIRE_ID[(d, p)]: row for d, p, row, _ in WIRES}
WIRE_PIN = {WIRE_ID[(d, p)]: p for d, p, _, _ in WIRES}

# The loose wires lie side by side on the bench in front of the module, along z (the cap for the device at the left end, the cap
# for the module at the right), first in their ribbon (the wires touching), then split apart: each step picks one up.
LOOSE_LENGTH = 56.0                                                # between the wire ends (the published loose wires are 58 mm)
LOOSE_Y = BENCH_Y + 0.875                                          # a cap's middle, lying on the bench
LOOSE_Z = 1290.0


def loose_poses(wire, x, z=LOOSE_Z, along='z'):
    """The world poses of a loose wire's two caps lying on the bench, its middle at (x, z), along z (the device's cap at the -z end) or
    along x (the device's cap at the -x end), and its straight centre line."""
    k = 2 if along == 'z' else 0
    mid, half = np.array([x, LOOSE_Y, z]), LOOSE_LENGTH / 2
    axis = np.eye(3)[k]
    a, b = DEV_CAP[wire], MOD_CAP[wire]
    pa, pb = lying(a, mid - axis * (half + 4.0), axis), lying(b, mid + axis * (half + 4.0), -axis)
    line = np.linspace(mid - axis * half, mid + axis * half, 57)
    return pa, pb, line


# The 21 jumper wires are a kit part, but in the CAD only their caps are parts (the wire is drawn): listed by hand, pictured straight
# with its two caps in line, as the MRA's breadboard wires (Lee, 15 Oct 2026).
_pa, _pb, _line = loose_poses(ALL_WIRES[0], 0.0)
# The push buttons are pictured by the yellow one (Lee's first round: the black one's cap is lost against its board): the black
# button gets a picture of its own (not shown in the list), so that the main picture is of the next, the yellow.
g.part_picture('Push Button', piece=BUTTONS[0], file='Push Button black')
g.list_part('Breadboard Wire (F-F)', [DEV_CAP[ALL_WIRES[0]], MOD_CAP[ALL_WIRES[0]]], len(ALL_WIRES), after='Dot Matrix Display')
g.part_picture('Breadboard Wire (F-F)', poses={DEV_CAP[ALL_WIRES[0]]: _pa, MOD_CAP[ALL_WIRES[0]]: _pb},
               wires=[dict(colour=WIRES[0][3], radius=0.625, pts=_line)])


def loose(wire, x, z=LOOSE_Z, along='z'):
    """The wire lying loose at (x, z): {cap: riding pose} and {wire: route}."""
    pa, pb, line = loose_poses(wire, x, z, along)
    a, b = DEV_CAP[wire], MOD_CAP[wire]
    return {a: HUB(a, pa), b: HUB(b, pb)}, {wire: W.route(line, a=a, b=b, a_at=pa, b_at=pb, stretch=True)}


# --- where the jumper wires run. Each set of wires the guide shows together is a "layout": each device's wires laid side by side as a
# ribbon (turned on the way so that none crosses another of its bundle), then settled clear of one another and of every part on screen
# (routing.py; Lee's first round, 19 Oct 2026: wires running through each other and into parts). Wires a step does not move are held
# where they were. The printed numbers are the settling's report: what is left of the worst overlap and the worst depth in a part (mm).
DEVICE_WIRES = {d: [w for w in ALL_WIRES if WIRE_DEVICE[w] == d] for d in BUTTONS + [DISPLAY, MATRIX]}
SURFACES = R.Surfaces(g.model)
LAYOUTS = {}


def bundle_lines(device, dev_pose, mod_pose, controls, lead=6.0, **how):
    """A device's wires side by side, from its pins (the device at dev_pose) to the module's (at mod_pose), through `controls`
    (R.ribbon: `twist=` where the bundle turns)."""
    ws = DEVICE_WIRES[device]
    lines = R.ribbon([cap_end(DEV_CAP[w], dev_pose) for w in ws], [cap_end(MOD_CAP[w], mod_pose) for w in ws], controls, lead=lead, **how)
    return dict(zip(ws, lines))


def middle_ends(device, dev_pose, mod_pose):
    """The middle of a device's wire ends at the device and at the module (where its ribbon starts and ends)."""
    ws = DEVICE_WIRES[device]
    return (np.mean([cap_end(DEV_CAP[w], dev_pose)[0] for w in ws], axis=0), np.mean([cap_end(MOD_CAP[w], mod_pose)[0] for w in ws], axis=0))


def on_screen(module, devices, case=(), extra=()):
    """(part, pose) for everything the wires must keep clear of: the module with the Nano Board and the USB plug on it, the devices,
    every plugged cap, the case, and `extra`."""
    items = [(MODULE, module), (NANO, module), (USB_B, module), *devices.items()]
    for w in ALL_WIRES:
        if WIRE_DEVICE[w] in devices:
            items += [(DEV_CAP[w], devices[WIRE_DEVICE[w]]), (MOD_CAP[w], module)]
    return items + [(p, None) for p in case] + list(extra)


def settled(name, lines, scene, held=None, cable=None):
    """The layout `name`: `lines` ({wire: drawn centre line}) settled among `held` ({wire: line}, wires that stay as they are), the
    USB cable (its centre line, 3.5 mm across) and the parts of `scene`."""
    if name not in LAYOUTS:
        fixed = dict(held or {})
        radii = {}
        if cable is not None:
            fixed['usb cable'], radii['usb cable'] = cable, 1.75
        report = []
        LAYOUTS[name] = R.settle(lines, fixed=fixed, parts=SURFACES.placed(scene), skip={w: {DEV_CAP[w], MOD_CAP[w]} for w in lines},
                                 radii=radii, report=report)
        print(f"  wires, {name}: {len(lines)} settled among {len(fixed)} held, {report[0]}")
    return LAYOUTS[name]


# On the bench the module lies flat, pins up. A button's wires drop out of its pins and come down into its row from above; the
# display's run behind the buttons' (over the Nano Board) into rows 8 and 9; the matrix's come in over the USB plug into rows 11 - 13.
BENCH_DISPLAY_WAY = [[664.0, 917.0, 1258.0], [667.0, 911.0, 1284.0], [663.0, 905.0, 1301.0]]
BENCH_MATRIX_WAY = [[651.0, 924.0, 1346.0], [656.0, 924.0, 1326.0]]   # (level at the matrix pins' height, then straight down into the header:
#                                                                       a cap held over its pin later sits under the bends of those already in)


def bench_layout():
    lines = {}
    for k, b in enumerate(BUTTONS):
        a, e = middle_ends(b, BUTTON_BENCH[k], MODULE_BENCH)
        over = [(a[0] + e[0]) / 2, (a[1] + e[1]) / 2 + 4.0, a[2] + 0.6 * (e[2] - a[2])]
        lines.update(bundle_lines(b, BUTTON_BENCH[k], MODULE_BENCH, [over, e + [0.0, 12.0, 0.0]]))
    lines.update(bundle_lines(DISPLAY, DISPLAY_BENCH, MODULE_BENCH, BENCH_DISPLAY_WAY))
    lines.update(bundle_lines(MATRIX, MATRIX_BENCH, MODULE_BENCH, BENCH_MATRIX_WAY, lead=(6.0, 24.0)))
    scene = on_screen(MODULE_BENCH, DEVICE_BENCH, extra=[(USB_A, USB_A_BENCH), (USB_B, usb_plug_bench)])
    return settled('bench', lines, scene, cable=usb_cable(MODULE_BENCH, USB_A_BENCH)['usb cable']['pts'])


def plugged_on_bench(wire):
    a, b = DEV_CAP[wire], MOD_CAP[wire]
    return {wire: W.route(bench_layout()[wire], a=a, b=b, a_at=on_bench(wire, 'a'), b_at=MODULE_BENCH, stretch=True)}


HELD_MM = 12.0                                                     # a cap held over its pin before it is pushed on


def refit_ends(points, start, end, reach=30.0):
    """A centre line with its ends moved onto `start` and `end`, each move fading out over `reach` mm along the line, so that the
    rest stays where it was (a wire held just off its pins keeps its place in its bundle)."""
    p = np.asarray(points, float)
    if np.linalg.norm(p[0] - start) > np.linalg.norm(p[-1] - start):
        p = p[::-1]
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    fade = lambda d: 1 - (lambda x: x * x * (3 - 2 * x))(np.clip(d / reach, 0, 1))
    return p + fade(s)[:, None] * (np.asarray(start) - p[0]) + fade(s[-1] - s)[:, None] * (np.asarray(end) - p[-1])


def plug_on(wire, park):
    """The step's motion for one wire: both caps from the bench, held over their pins, pushed on (ride=), the wire with them. Held, the
    wire keeps its plugged shape with its ends lifted off the pins, settled among the wires already plugged in (Lee's first round:
    no wire through another, even while it moves). With park['gap'] (the matrix's, Lee's second round: the loose wire lies in the
    gap between the module and the matrix, across it), a beat each: the matrix's cap rises straight up to its place 5 mm off its pin
    (each wire's place is under those already in) while the module's comes over through the gap, upright, just above the pins'
    height; then the module's slides along its column to over its pin; then both are pushed on. So neither cap passes through the
    module or the Nano Board, and the wire comes into its bundle from below. With park['over'] and park['lift_a'] (heights: the 4-digit
    display's), a beat each: both caps lifted straight up off the bench (the module's to `over`, the display's to `lift_a`); carried
    over, the display's to 30 mm out along its pin, in its own lane above the wires already in, the module's over the Nano Board and
    the bundle to above its pin; the display's slid along its lane to where it is held while the module's is lowered over its pin;
    both pushed on."""
    a, b = DEV_CAP[wire], MOD_CAP[wire]
    pa, pb = on_bench(wire, 'a'), MODULE_BENCH
    ha, hb = along_out(a, pa, HELD_MM), along_out(b, pb, HELD_MM)
    if park.get('gap') is not None:
        ha, hb = along_out(a, pa, 5.0), along_out(b, pb, 13.0 if WIRE_ROW[wire].startswith('S') else 10.5)   # (the module's cap
#                                                    slides well clear of the pins it passes; the S column, nearest the camera, higher)
        gb = compose(shift([0.0, 0.0, park['gap'] - apply_pose(pb, CAPS[b]['centre'])[2]]), hb, CAPS[b]['centre'])
    ea, _ = cap_end(a, ha)
    eb, _ = cap_end(MOD_CAP[wire], hb)
    name = f'held: {wire}'
    before = ALL_WIRES[:ALL_WIRES.index(wire)]
    plugged = {w: p for w, p in bench_layout().items() if w in before}
    devices = {d: DEVICE_BENCH[d] for d in {WIRE_DEVICE[w] for w in before + [wire]}}
    if name not in LAYOUTS:
        scene = [item for item in on_screen(MODULE_BENCH, devices) if item[0] not in (a, b)] + [(a, ha), (b, hb)]
        if park.get('gap') is not None:                            # (the matrix's: its plugged shape, only its ends moved)
            LAYOUTS[name] = refit_ends(bench_layout()[wire], ea, eb)
        else:
            if WIRE_DEVICE[wire] != DISPLAY:                       # (a button's: its own plugged shape, lifted off the pins)
                line = refit(bench_layout()[wire], ea, eb)
            else:                                                  # (the display's: arched over from where they lie, as before)
                ea_out, eb_out = cap_end(a, ha)[1], cap_end(b, hb)[1]
                line = jumper(ea, ea_out, eb, eb_out, [(ea + eb) / 2 + [0.0, 10.0, 0.0]], lead=8.0)
            LAYOUTS[name] = R.settle({wire: line}, fixed=plugged, parts=SURFACES.placed(scene), skip={wire: {a, b}})[wire]
    held = W.route(LAYOUTS[name], a=a, b=b, a_at=ha, b_at=hb, stretch=True)
    ride = {a: [HUB(a, ha), HUB(a, pa)], b: [HUB(b, hb), ZERO]}
    routes = [held, plugged_on_bench(wire)[wire]]
    if park.get('gap') is not None:                                # (in the gap: the matrix's cap in its place, the module's below it)
        name = f'gathered: {wire}'
        if name not in LAYOUTS:
            (ea, ea_out), (eg, eg_out) = cap_end(a, ha), cap_end(b, gb)
            scene = [item for item in on_screen(MODULE_BENCH, devices) if item[0] not in (a, b)] + [(a, ha), (b, gb)]
            LAYOUTS[name] = R.settle({wire: jumper(ea, ea_out, eg, eg_out, lead=6.0)}, fixed=plugged, parts=SURFACES.placed(scene),
                                     skip={wire: {a, b}})[wire]
        ride = {a: [HUB(a, ha), HUB(a, ha), HUB(a, pa)], b: [HUB(b, gb), HUB(b, hb), ZERO]}
        routes = [W.route(LAYOUTS[name], a=a, b=b, a_at=ha, b_at=gb, stretch=True), *routes]
    if park.get('over') is not None:                               # (the display's: both caps straight up off the bench; the display's
        la, lb, _ = loose_poses(wire, park['x'], park['z'], park['along'])   # over to 30 mm out along its pin, in its own lane above the
        ua = compose(shift([0.0, park['lift_a'] - LOOSE_Y, 0.0]), la, CAPS[a]['centre'])   # wires already in, then along it to where
        oa = along_out(a, pa, 30.0)                                # it is held; the module's over the Nano Board and the bundle, low
        ub = compose(shift([0.0, park['over'] - LOOSE_Y, 0.0]), lb, CAPS[b]['centre'])   # enough to stay clear of the caption box,
        ob = compose(shift([0.0, park['over'] - apply_pose(hb, CAPS[b]['centre'])[1], 0.0]), hb, CAPS[b]['centre'])   # then down
        shapes = []                                                # over its pin: an independent review, 20 Oct 2026)
        for k, (pa_, pb_) in enumerate(((ua, ub), (oa, ob))):
            name = f'{("lifted", "over")[k]}: {wire}'
            if name not in LAYOUTS:
                (ea, ea_out), (eo, eo_out) = cap_end(a, pa_), cap_end(b, pb_)
                scene = [item for item in on_screen(MODULE_BENCH, devices) if item[0] not in (a, b)] + [(a, pa_), (b, pb_)]
                LAYOUTS[name] = R.settle({wire: jumper(ea, ea_out, eo, eo_out, [(ea + eo) / 2 + [0.0, (-7.0, 1.0)[k], 0.0]],   # (lifted:
                                                         lead=(4.0, 2.0)[k])},   # sagging, so it reads as in the air; over: flat, below the caption)
                                         fixed=plugged, parts=SURFACES.placed(scene), skip={wire: {a, b}})[wire]
            shapes.append(W.route(LAYOUTS[name], a=a, b=b, a_at=pa_, b_at=pb_, stretch=True))
        ride = {a: [HUB(a, ua), HUB(a, oa), HUB(a, ha), HUB(a, pa)], b: [HUB(b, ub), HUB(b, ob), HUB(b, hb), ZERO]}
        routes = [*shapes, *routes]
    return ride, {wire: routes}


# --- the USB cable: its right-angle Mini-B end plugs into the Nano Board; its A end lies on the bench. The player draws the cable.
g.wire('usb cable', 'cable_black', 1.75, name='USB Cable')
_lo, _hi = np.asarray(GEO['parts'][USB_A]['lo']), np.asarray(GEO['parts'][USB_A]['hi'])
_corners = np.array([[x, y, z] for x in (_lo[0], _hi[0]) for y in (_lo[1], _hi[1]) for z in (_lo[2], _hi[2])])
USB_A_BENCH = compose([0.0, round(BENCH_Y - float(apply_pose(POSES['usb_a_bench'], _corners)[:, 1].min()), 3), 0.0], POSES['usb_a_bench'], GEO['parts'][USB_A]['middle'])
USB_OUT = 25.0                                                     # the plug held this far out of the Nano's socket before it goes in (built: up)
USB_HOVER = [0.0, USB_OUT, 0.0]                                    # (built, the plug goes in downwards: held up, out of the socket)
usb_plug_bench = compose(MODULE_BENCH, USB_HOVER, GEO['parts'][USB_B]['middle'])


def usb_cable(plug_pose, a_pose, pull=24.0):
    """The cable from the plug (at plug_pose) to the A end (at a_pose)."""
    start, start_dir = np.asarray(apply_pose(plug_pose, USB['plug_exit'])), unit(turn_dir(plug_pose, USB['plug_out']))
    end, end_dir = np.asarray(apply_pose(a_pose, USB['a_exit'])), -unit(turn_dir(a_pose, USB['a_out']))
    return {'usb cable': W.route(W.curve(start, start_dir, end, end_dir, pull=pull), a=USB_B, b=USB_A, a_at=plug_pose, b_at=a_pose, stretch=True)}


# ================================================================ THE ELECTRONICS (begin)
# Step 1: the Nano Board into the I/O module, which lies on the bench (the published guide's section card "Nano I/O Module" is not
# drawn: the module is named by its label). The Nano rides on the module, 35 mm over its sockets, and is pushed down.
g.rest_at([MODULE], MODULE_BENCH)
NANO_UP = relative_pose(MODULE_BENCH, compose([0.0, 35.0, 0.0], MODULE_BENCH), GEO['parts'][NANO]['middle'])
g.carry([NANO], by=MODULE, pose=NANO_UP)
M_MRA = np.asarray(GEO['mra_module_to_pmg'], float)
mra = lambda p: (M_MRA[:3, :3] @ np.asarray(p, float) + M_MRA[:3, 3])
# The Nano's four corner pins into the end holes of the two sockets (the MRA's Step 1 lines, carried over: tip of the pin, mouth of
# the hole), where the step shows them: the Nano 35 mm up.
NANO_LINES = [[apply_pose(MODULE_BENCH, mra(t)) + [0.0, 35.0, 0.0], apply_pose(MODULE_BENCH, mra(m))]
              for t, m in (([61.5, 109.0, 136.9], [61.5, 114.8, 136.9]), ([62.1, 109.1, 166.0], [62.1, 114.9, 166.0]),
                           ([76.8, 109.2, 136.9], [76.8, 114.9, 136.9]), ([77.4, 109.2, 166.0], [77.4, 114.9, 166.0]))]
MODULE_SPOT = [597.0, 906.0, 1290.0]                               # (a bare spot on the module's board, clear of the sockets: its label)
g.place('Begin the electronics with the I/O module. Press the Nano Board into it, its USB socket at the same end as the power socket.',
        appear=[MODULE], ride={NANO: ZERO}, lines_at=[[np.round(t, 2).tolist(), np.round(m, 2).tolist()] for t, m in NANO_LINES],
        labels=[dict(id=NANO, text='Nano Board'), dict(id=MODULE, text='Nano I/O Module', anchor=MODULE_SPOT)])

# Steps 2 - 14: the push buttons. First the twelve wires they need are peeled off a ribbon and separated; then each button is wired pin
# by pin (VCC, OUT, GND: the order of its header), from D4 to D7. A button appears where it stands on the bench with its first wire;
# each wire lies loose at one spot in front of the module for its own step (as published), then its caps are plugged on.
BUTTON_WIRES = ALL_WIRES[:12]
RIBBON_X0, RIBBON_PITCH, SPLIT_X0, SPLIT_PITCH = 611.0, 1.75, 597.0, 4.0
PARK_X = 618.0                                                     # where a loose wire lies on the bench for its step


def ribbon(wires, x0, pitch):
    """The wires in a row: each wire's caps' riding poses and the routes."""
    ride, routes = {}, {}
    for k, w in enumerate(wires):
        r, rt = loose(w, x0 + pitch * k)
        ride.update(r)
        routes.update(rt)
    return ride, routes


def peel(wires, caption, x0, camera=None):
    """A ribbon step: the wires in their ribbon, close up, then separated; then they are put away until each one's step."""
    in_ribbon, ribbon_routes = ribbon(wires, x0, RIBBON_PITCH)
    for cap, pose in in_ribbon.items():
        g.carry([cap], by=MODULE, pose=pose, appear=False)
    split, split_routes = ribbon(wires, x0 - 14.0, SPLIT_PITCH)
    caps = list(in_ribbon)
    g.place(caption, appear=caps, ride=split, wires=ribbon_routes, wires_done=split_routes, lines=False, labels=[],
            eye=[dict(anchor=[x0 + RIBBON_PITCH * (len(wires) - 1) / 2, LOOSE_Y, LOOSE_Z])], **(camera or dict(focus=caps, focus_pad=1.15)))
    g.put_away(caps)


peel(BUTTON_WIRES, 'Peel twelve breadboard wires off the ribbon, keeping them in order. Separate them so that each can be picked up on its own.', RIBBON_X0)

for k, b in enumerate(BUTTONS):
    g.rest_at([b], BUTTON_BENCH[k])

# Step 3: the push buttons introduced, as the published guide's "Push Buttons" card does (Lee's first round: a breakout of the board,
# its printed pin names highlighted): the black push button on its own, close up, its pins' names (VCC, OUT and GND, printed beside
# its header: silkscreen.py) boxed in red in a close-up.
_print = json.load(open(HERE / 'decals.json'))[BUTTONS[0]][0]
_o, _u, _v = (np.asarray(_print[k], float) for k in ('origin', 'u', 'v'))
PRINT_MID = _o + _u * _print['size'][0] / 2 + _v * _print['size'][1] / 2           # (seated)
PRINT_FACE = -unit(np.cross(_u, _v))                                              # (the cap side, seated)
_bench_mid = np.asarray(apply_pose(BUTTON_BENCH[0], PRINT_MID))
_bench_face = unit(turn_dir(BUTTON_BENCH[0], PRINT_FACE))
_lo, _hi = np.asarray(GEO['parts'][BUTTONS[0]]['lo']), np.asarray(GEO['parts'][BUTTONS[0]]['hi'])
_button_box = np.asarray(apply_pose(BUTTON_BENCH[0], [[x, y, z] for x in (_lo[0], _hi[0]) for y in (_lo[1], _hi[1]) for z in (_lo[2], _hi[2])]))
g.place('Find the four push buttons. Each has three pins, named on its board beside them: VCC, OUT and GND.',
        appear=[BUTTONS[0]], single=True, lines=False, labels=[],                    # (the caption names it; a label would sit under the close-up)
        inset=dict(target=_bench_mid.round(2).tolist(), dir=unit(_bench_face + [0.0, 0.25, 0.12]).round(4).tolist(), radius=8.5, mark=6.9,
                   alt='Close-up of the push button\'s pins: VCC, OUT and GND are printed on the board beside them.'),
        view_dir=unit(_bench_face + [0.0, 0.06, 0.25]).round(4).tolist(),       # (level with the button: the module below it stays out of view)
        frame=(_button_box.mean(0).round(1).tolist(), 24.0), one_off_camera=True)


# One camera for each run of wires (as published: set on the first wire of a module and held), from the published guide's side.
BUTTON_RUN = dict(view_dir=[-0.7228, 0.4352, 0.5368], frame=([645.0, 911.0, 1295.0], 58.0))   # (Lee's second round: higher, from their
#                                                                                              screenshot of Step 9, solved: camsolve.js)
DISPLAY_RUN = dict(view_dir=[0.507, 0.766, -0.396], frame=([672.0, 902.0, 1264.0], 58.0))   # (from behind, above: the display's printed back,
#                                                                                            the module's pins: Lee's second round)
DISPLAY_PINS_RUN = dict(view_dir=[0.4589, 0.5, 0.7344], frame=([672.0, 911.0, 1262.0], 74.0))   # (Steps 19 - 20, VCC and GND:
#             lower and further round towards rows 10 - 13 than DISPLAY_RUN, from whose side the display's own wires and caps, on S8 and
#             S9, hid V9 and G9 (Lee's third round, 20 Oct 2026). A ray test of every view direction against the new wire's two caps as
#             they sit once plugged in (docs/research/pmg/round3/scripts/cam1920c.py): about half of each in view at both ends (the
#             camera of round 3's first try: 55 % at the module, 17 % at the display; DISPLAY_RUN 0 - 7 %); the display's back at 63
#             degrees from the line of sight (DISPLAY_RUN 58, the first try 79), but its header's pin stubs lie over the printed names
#             beside DIO, VCC and GND from here: no direction sees both pins and the printing squarely. The labels name the pins.)
MATRIX_RUN = dict(view_dir=[0.474, 0.829, 0.296], frame=([672.0, 898.0, 1338.0], 54.0))     # (higher: Lee's second round, their Step 22 screenshot)   # (from behind: the matrix's printed back, its pin
#                                                                                               names by the header, and the module's pins: Lee's first round)


def wire_step(wire, caption, appear=(), labels_more=(), caution=None, camera=None, review=None, park=None,
              module_label=dict(side='up-right'), device_label=None, close_up=False, close_up_dir=(0.06, 1.0, 0.1)):
    """One wire: it lies loose at the parking spot (an eye on it), then its two caps are lifted, held over their pins and pushed on.
    A label at each pin, at the top of the pin (measured: make_source.py), on the device and on the module (Lee's first round).
    close_up: on Step Nc, a close-up from above of the module's pin with the new cap on it, boxed in red (as the LAC's breadboard holes:
    Lee's fourth round, Steps 17 - 20); or the side of the model to put it on ('left': Steps 19 - 20, where the pin is at the module's
    left end; on the right, the side with most room, its leader ran across the module and the caps just put on: a review, 21 Oct).
    close_up_dir: where the close-up looks from (from above; the dot matrix's from the G side, [-0.4, 0.9, 0.15]: from above, the wire
    just put on V11 rose between the camera and G11 and the close-up of Step 22c showed only that wire: a review, 21 Oct)."""
    device, row = WIRE_DEVICE[wire], WIRE_ROW[wire]
    a, b = DEV_CAP[wire], MOD_CAP[wire]
    park = dict(dict(x=PARK_X, z=LOOSE_Z, along='z', eye=0.0), **(park or {}))   # (where the loose wire lies; eye: mm along it from its middle)
    lying_on_bench, loose_route = loose(wire, park['x'], park['z'], park['along'])
    eye_at = np.array([park['x'], LOOSE_Y, park['z']]) + np.eye(3)[2 if park['along'] == 'z' else 0] * park['eye']
    for cap in (a, b):
        g.carry([cap], by=MODULE, pose=lying_on_bench[cap], appear=False)
    ride, routes = plug_on(wire, park)
    labels = [dict(text=WIRE_PIN[wire], anchor=pin_tip(a), id=device, ring=False, **(device_label or {})),
              dict(text=row, anchor=pin_tip(b), id=MODULE, ring=False, **(module_label or {})), *labels_more]
    inset = None
    if close_up:
        top = np.asarray(apply_pose(MODULE_BENCH, pin_tip(b)), float)
        inset = dict(target=top.round(2).tolist(), dir=list(close_up_dir), radius=13.0, mark=1.6,
                     alt=f"Close-up from above: the {WIRE_PIN[wire]} wire's cap on {row} of the I/O module, among the caps already in",
                     **({'side': close_up} if isinstance(close_up, str) else {}))
    g.place(caption, appear=list(appear) + [a, b], ride=ride, wires=loose_route, wires_done=routes, lines=False, labels=labels,
            eye=[dict(anchor=eye_at.round(2).tolist(), **park.get('eye_place', {}))], caution=caution, review=review,
            ride_beats='gap' in park or 'over' in park, **({'inset': inset} if inset else {}), **(camera or {}))   # (the displays': a beat
#                                                                       for each stretch, see plug_on)


NAME_REACH = dict(zip(BUTTONS, (0.10, 0.16, 0.10, 0.13)))           # (each the least that clears the caption box at LMS sizes)


def name_on_cap(b):
    """A push button's name label, on its round cap (seated: the cap is the top of the button), so that its pins have one pointer."""
    lo, hi = np.asarray(GEO['parts'][b]['lo']), np.asarray(GEO['parts'][b]['hi'])
    return dict(id=b, text=HOVER_NAMES[b], anchor=[round(float(lo[0] + hi[0]) / 2 - 3.0, 2), round(float(hi[1]) - 1.5, 2), round(float(lo[2] + hi[2]) / 2, 2)],
                side='up-right', reach=NAME_REACH[b])              # (up and to the right, as the module's: Lee's second round; far
#                                                                     enough out to clear the caption box at LMS sizes: a review, 20 Oct)


THREE_WIRES = ("Three wires per push button here (VCC to V, OUT to S, GND to G), as in the published guide. Your STEP has two (OUT to S, VCC to "
               "G) and looks like an older save of the model. Which is the kit's wiring?")
ROWS = ' (the V pin of row 4)'                                      # (in Step 4's caption, not a caution box: the box hid the black
#                                                                     button in the LMS's frame: a review, 20 Oct 2026)
for k, b in enumerate(BUTTONS):
    for pin in ('VCC', 'OUT', 'GND'):
        wire = WIRE_ID[(b, pin)]
        first = pin == 'VCC'
        name = f'{COLOURS[k]} push button'
        wire_step(wire, f'Connect {pin} on the {name} to {WIRE_ROW[wire]}{ROWS if (k, pin) == (0, "VCC") else ""} on the I/O module.',
                  appear=[b] if first and k > 0 else [], labels_more=[name_on_cap(b)] if first else [], camera=BUTTON_RUN,
                  review=THREE_WIRES if (k, pin) == (0, 'VCC') else None,
                  device_label=dict(side='right') if k > 0 else None)   # (the pins' labels to the right, clear of the buttons before)

# Steps 15 - 24: the 4-digit display and the dot matrix display: nine more wires off the ribbon, then each display pin by pin.
DISPLAY_WIRES, MATRIX_WIRES = ALL_WIRES[12:16], ALL_WIRES[16:]
peel(DISPLAY_WIRES + MATRIX_WIRES, 'Peel nine more breadboard wires off the ribbon, keeping them in order, and separate them.', RIBBON_X0 + 2.5,
     camera=dict(view_dir=[-0.4962, 0.8124, 0.3062], frame=([640.0, 884.0, 1292.0], 62.0)))   # (from higher up: Lee's first round; the whole module)
g.rest_at([DISPLAY], DISPLAY_BENCH)
g.rest_at([MATRIX], MATRIX_BENCH)
for wire in DISPLAY_WIRES:
    first = wire == DISPLAY_WIRES[0]
    wire_step(wire, f'Connect {WIRE_PIN[wire]} on the 4-digit display to {WIRE_ROW[wire]} on the I/O module.',
              appear=[DISPLAY] if first else [], labels_more=[dict(id=DISPLAY, text='4-Digit Display', side='near-below', reach=0.1)] if first else [],
              camera=DISPLAY_PINS_RUN if WIRE_PIN[wire] in ('VCC', 'GND') else DISPLAY_RUN, park=dict(x=712.0, z=1262.0, over=916.0, lift_a=932.0, eye_place=dict(side='near-below', reach=0.05)),   # (on the camera's
#                                                                             side, between; the module's cap over the Nano Board: see plug_on)
              **(dict(module_label=dict(side='left', reach=0.08), device_label=dict(side='down-right', reach=0.05))   # (from DISPLAY_PINS_RUN: clear
                 if WIRE_PIN[wire] in ('VCC', 'GND') else                                                          #  of the wires, boards and the
                                                                                                                   #  parked wire's cap)
                 dict(module_label=dict(side='up-left', reach=0.08), device_label=dict(side='up-right', reach=0.08))),
              close_up='left' if WIRE_PIN[wire] in ('VCC', 'GND') else True)
# Steps 21 - 25 (Lee's fourth round, 21 Oct 2026): each matrix pin's label to the right of its pin, just under the wire put in the step
# before (VCC, the first, up and to the right); the module's V11, G11, S12 and S13 up and a little to the right of where they were (S11
# too, though Lee did not name it: where it was it met DIN at the LMS's size); the eye to the right of the loose wire, 18 mm down it (clear
# of the module's corner). Checked clear of one another at four window sizes.
MATRIX_LABELS = {'VCC': (dict(side='up-left', reach=0.03), dict(side='up-right', reach=0.03)),     # (VCC: no wire above it yet)
                 'GND': (dict(side='up-left', reach=0.025), dict(side='near-right', reach=0.035)),     # (G11 nearer than the others: at 0.03 it
                 'DIN': (dict(side='up-left', reach=0.03), dict(side='near-right', reach=0.035)),       #  met GND at 1440 wide; above its pin, it
#                                                                                                         sat over the brown wire: a review, 21 Oct;
#                                                                                                         S11, near-left, met DIN at the LMS's size)
                 'CS': (dict(side='up-left', reach=0.03), dict(side='near-right', reach=0.035)),
                 'CLK': (dict(side='up-left', reach=0.025), dict(side='near-right', reach=0.025))}   # (closer: S13 met CLK)
MATRIX_CLOSE_UP = 'right'                                          # (on the left it covered the dot matrix display, in a narrow
#                                                                     window its header too; on the right its leader runs along the module's top edge)
for wire in MATRIX_WIRES:
    first = wire == MATRIX_WIRES[0]
    module_label, device_label = MATRIX_LABELS[WIRE_PIN[wire]]
    wire_step(wire, f'Connect {WIRE_PIN[wire]} on the dot matrix display to {WIRE_ROW[wire]} on the I/O module.',
              appear=[MATRIX] if first else [], labels_more=[dict(id=MATRIX, text='Dot Matrix Display', side='near-below',
                                                                       anchor=[531.1, 941.6, 1251.0], reach=0.12)] if first else [],
              camera=MATRIX_RUN, park=dict(x=680.0, z=1356.0, along='x', gap=1338.0, eye=18.0, eye_place=dict(side='near-right', reach=0.025)),   # (in the
#                                                                                    gap between them, across it: Lee's second round)
              module_label=module_label, device_label=device_label, close_up=MATRIX_CLOSE_UP,   # (as Steps 17 - 20's: Lee, 21 Oct 2026)
              close_up_dir=(-0.4, 0.9, 0.15))

# Step 25: the USB cable, its right-angle plug pushed into the Nano Board's socket (as published: hover and plug, one lead line), its A
# end lying on the bench. Seen from behind the module, as published (the plug goes in along -z, at the module's +z end: side on).
g.carry([USB_B], by=MODULE, pose=USB_HOVER, appear=False)
g.rest_at([USB_A], USB_A_BENCH)
# (The Mini-B end is the PMG's own right-angle plug: a part that differs from the MRA's stays the kit's own, Lee, 19 Oct 2026, rulebook
# section 13. The A end is the MRA's model, which the CAD already has.)
g.place("Connect the USB cable to the Nano Board.", appear=[USB_B, USB_A], ride={USB_B: ZERO},
        lines_at=[[np.round(apply_pose(usb_plug_bench, USB['plug_tip']), 2).tolist(), np.round(apply_pose(MODULE_BENCH, USB['socket_mouth']), 2).tolist()]],
        lines_to=[MODULE, NANO, USB_B],                                # (so that the tip is checked against the plug where it is held)
        labels={USB_B: 'USB Cable'}, wires=usb_cable(usb_plug_bench, USB_A_BENCH), wires_done=usb_cable(MODULE_BENCH, USB_A_BENCH),
        view_dir=[0.922, 0.3871, 0.0054], frame=([668.0, 898.0, 1325.0], 70.0),
        caution='Set the I/O module, with everything plugged into it, aside for now. You will use it again in a bit.')
ELECTRONICS = [MODULE, NANO, USB_B, USB_A, DISPLAY, MATRIX] + BUTTONS + JUMPER_CAPS
g.put_away(ELECTRONICS)
# ================================================================ THE ELECTRONICS (end)

# ================================================================ THE CASE (begin)
# The case is built on its own first (the published guide hides the electronics until the buttons go in). H1 is the datum.
g.place('Begin the case with H1. Push the front tabs of H2 into the slots at the end of H1 until they click.', move=[H2], show=[H1],
        direction=[1, 0, 0], hover=40, labels=[dict(id=H1, text='H1', side='near-above', reach=0.06), dict(id=H2, text='H2')])   # (H1's
#                                                                                                   label above it: Lee's fourth round)
g.place('Push H3 onto the other end of H1 the same way.', move=[H3], direction=[1, 0, 0], hover=43, labels={H3: 'H3'})
g.place('Push H4 onto the back tabs of H2 and H3.', move=[H4], direction=[1, 0, 0], hover=65, labels={H4: 'H4'})

# The floor plates go on with the case turned over. Each hooks its tabs into the windows of H2, then swings up so that its other
# edge clicks into the open notches of H3 (cad_study.md 2.4: an 8 degree hinge about the edge at H2).


def hinged(part, at):
    """A floor plate's way in: tilted 8 degrees about its edge at H2 (`at`), 5 mm short of H2's windows and 60 mm down (the case is
    turned over, so it comes in from above for the student), then into H2's windows, then swung up into H3's notches. A beat for
    each (Lee's first round: slower, to see it slot into H2 and then H3): down to just short of the windows, slowing as it comes,
    into the windows, swung in."""
    tilt = lambda t: turned([1, 0, 0], -8.0, at, t)
    return [tilt([0.0, -60.0, -5.0]), tilt([0.0, -18.0, -5.0]), tilt([0.0, 0.0, -5.0]), tilt(ZERO), ZERO]


FLOOR_CAMERA = dict(view_dir=[-0.8, -0.5657, -0.2], frame=([529.0, 882.0, 1290.0], 118.0))   # (from the front, by H1: Lee's first round)


def spots(part, receivers, most=2, slab_mm=None):
    """Spots on a part's tabs where they pass through a receiving plate (for lead lines), seated: the part's points that lie in the
    plate's thickness and within its outline's box, grouped, the biggest groups first."""
    from scipy.cluster.hierarchy import fcluster, linkage
    out = []
    mover = g.model.inst[part]
    for r in receivers:
        plate = g.model.inst[r]
        V = plate.vertices - plate.vertices.mean(0)
        n = np.linalg.svd(V, full_matrices=False)[2][-1]
        d = plate.vertices @ n
        lo, hi = plate.bounds
        P = trimesh.sample.sample_surface_even(mover, 40000, seed=0)[0]   # (a tab's corners need not lie in the plate it passes through)
        on = P[(P @ n >= d.min() - 0.01) & (P @ n <= d.max() + 0.01) & np.all((P >= lo - 0.1) & (P <= hi + 0.1), axis=1)]
        if len(on) < 4:
            continue
        if len(on) > 1500:                                         # (single linkage is quadratic: a sample is plenty)
            on = on[np.random.default_rng(0).choice(len(on), 1500, replace=False)]
        groups = fcluster(linkage(on, 'single'), 3.0, 'distance')
        sizes = sorted(((np.sum(groups == k), k) for k in set(groups)), reverse=True)
        out += [on[groups == k].mean(0).round(2).tolist() for _, k in sizes[:most]]
    return out


g.place('Turn the case over. Hook the tabs of H5 into the windows in H2, then swing H5 down so that its other tabs click into the notches in H3.',
        move=[H5], path=hinged(H5, [532.3, 903.39, 1357.17]), flip=True, labels={H5: 'H5'}, lines_at=[[502.8, 903.3, 1358.2], [550.3, 903.2, 1358.8], [502.4, 903.3, 1222.2], [547.8, 903.1, 1222.4]],   # (Lee's points)
        one_off_camera=True, **FLOOR_CAMERA)
g.place('Lay H6 on H5 the same way: its tabs into the windows in H2, then into the notches in H3.',
        move=[H6], path=hinged(H6, [518.2, 900.39, 1357.17]), flip=True, labels={H6: 'H6'}, lines_at=[[502.3, 900.3, 1357.8], [549.8, 900.1, 1358.2], [501.8, 900.3, 1222.8], [548.3, 900.1, 1222.6]],   # (Lee's points)
        one_off_camera=True, **FLOOR_CAMERA)

# ---- the push buttons go into H6, with their wires: the electronics come back, lying where they were on the bench beside the case.
# In the case everything that moves rides on H1 (the datum, which never moves) until it goes into its own place.
for k, b in enumerate(BUTTONS):
    g.carry([b], by=H1, pose=BUTTON_BENCH[k])
g.carry([MODULE], by=H1, pose=MODULE_BENCH)
g.carry([DISPLAY], by=H1, pose=DISPLAY_BENCH)
g.carry([MATRIX], by=H1, pose=MATRIX_BENCH)
g.carry([USB_A], by=H1, pose=USB_A_BENCH)
g.carry([NANO, USB_B], by=MODULE)
for w in ALL_WIRES:
    g.carry([DEV_CAP[w]], by=WIRE_DEVICE[w])
    g.carry([MOD_CAP[w]], by=MODULE)
ON_THE_BENCH = {}
for w in ALL_WIRES:
    ON_THE_BENCH.update(plugged_on_bench(w))
ON_THE_BENCH.update(usb_cable(MODULE_BENCH, USB_A_BENCH))


# The push buttons' wires in the case (round1_plan.md). From each button's pins they dip through H5's hole beside the button into the
# gap between H5 and H7 (H6 is cut away there, x 524 - 573: 2.6 mm high, so a button's three wires lie side by side in it), run back
# under the keys, drop under H4's raised bottom edge (z 1243.5 - 1338: the black button's wires move over to clear H4's end, the blue
# button's likewise; Lee's first round: the black wire ran into H4) and come out behind H4, below H5's tongue.
CHANNEL_Y, UNDER_H4_Y = 898.7, 894.5
PASSAGE_Z = [1249.5, None, None, 1330.5]
CASE = [H1, H2, H3, H4, H5, H6, H7]
CASE_ALL = CASE + [H8, H10, H11, H12, H13, H14] + KEYS             # (wires laid in the case keep clear of all it will have)


def in_case_way(k):
    """The middle of button k's three wires, from its pins (seated) to behind H4, where they come out."""
    zk = float(middle_ends(BUTTONS[k], None, MODULE_BENCH)[0][2])
    zp = PASSAGE_Z[k] or zk
    return [[527.5, 905.0, zk], [531.0, 901.8, zk], [535.0, CHANNEL_Y, zk], [552.0, CHANNEL_Y, (zk + zp) / 2], [568.0, CHANNEL_Y, zp],
            [576.5, 896.2, zp], [582.0, UNDER_H4_Y, zp], [596.0, UNDER_H4_Y, zp], [603.0, 895.8, zp]]


def as_routes(lines, module_pose, device_poses=None, held_in_case=False, tail=False, shared=()):
    """{wire: route}: each line tied to its two caps, drawn with the module at module_pose and each device where device_poses has it
    (seated if not named). held_in_case: a push button's wire, once the button is in the case, does not follow the module along the
    run through the case (b_from: up to where it comes out behind H4), so that the run stays put while the module is lifted and
    lowered (the player bends a wire with its end parts in proportion along it: the run swung through H4 and H5). tail: changing
    to another such route, matched by distance from each end (`tail_from`: the run in the case, or the first 7 mm out of a device's
    pin) rather than stretched evenly, and moving wholly with the module from where it first lies over it (`b_whole`: as the module
    turns between two stops the run over its plug and the Nano Board turns with them; by shares of the wire's length it lagged into
    them: the review of 21 Oct) (Step 42). shared: devices whose wires get one b_whole, the least of theirs, so that they bend alike
    (the dot matrix's, in Step 42's bent routes: with one each, its VCC lagged through the other four in the lift: the review of
    21 Oct; for every device, the bundles then touched more often in the last third of the turn)."""
    device_poses = device_poses or {}
    over = over_module(module_pose) if tail else None
    out, how = {}, {}
    for w, p in lines.items():
        p = np.asarray(p, float)
        s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
        b_from = None
        if held_in_case and WIRE_DEVICE[w] in BUTTONS:
            b_from = float(s[int(np.argmax(p[:, 0] > 598.0))])
        how[w] = dict(b_from=b_from)
        if tail:
            inside = over(p)
            how[w].update(tail_from=b_from or 7.0, b_whole=max(float(s[int(np.argmax(inside))]) if inside.any() else float(s[-1]), (b_from or 0.0) + 5.0))
    if tail:
        for d in {WIRE_DEVICE[w] for w in lines} & set(shared):
            ws = [w for w in lines if WIRE_DEVICE[w] == d]
            least = min(how[w]['b_whole'] for w in ws)
            for w in ws:
                how[w]['b_whole'] = round(max(least, (how[w]['b_from'] or 0.0) + 5.0), 2)
    for w, p in lines.items():
        out[w] = W.route(p, a=DEV_CAP[w], b=MOD_CAP[w], a_at=device_poses.get(WIRE_DEVICE[w]), b_at=module_pose, stretch=not tail, **how[w])
    return out


BENCH_CABLE = usb_cable(MODULE_BENCH, USB_A_BENCH)['usb cable']['pts']


def case_bench_layout():
    """The buttons in the case, the module (and the display and matrix) still on the bench: each button's wires come out behind H4
    and across to its row, turning on the way from lying flat (side by side, as in the case) to standing up (one above the other,
    as they go down into the module's G, V and S)."""
    lines = {}
    for k, b in enumerate(BUTTONS):
        way = in_case_way(k)
        e = middle_ends(b, None, MODULE_BENCH)[1]
        lines.update(bundle_lines(b, None, MODULE_BENCH, way + [[618.0, 898.5, (way[-1][2] + e[2]) / 2], [636.0, 900.5, e[2]], [647.0, 901.5, e[2]]],
                            lead=3.0, twist=(way[-1], [636.0, 900.5, e[2]])))
    held = {w: p for w, p in bench_layout().items() if WIRE_DEVICE[w] in (DISPLAY, MATRIX)}
    scene = on_screen(MODULE_BENCH, {**{b: None for b in BUTTONS}, DISPLAY: DISPLAY_BENCH, MATRIX: MATRIX_BENCH}, case=CASE_ALL,
                      extra=[(USB_A, USB_A_BENCH)])
    return settled('case, module on the bench', lines, scene, held=held, cable=BENCH_CABLE)


def first_button_layout():
    """The blue button in the case, the others still on the bench (Step 32c)."""
    b = BUTTONS[FIRST]
    lines = {w: p for w, p in case_bench_layout().items() if WIRE_DEVICE[w] == b}
    held = {w: p for w, p in bench_layout().items() if WIRE_DEVICE[w] != b}
    scene = on_screen(MODULE_BENCH, {**DEVICE_BENCH, b: None}, case=CASE, extra=[(USB_A, USB_A_BENCH)])
    return settled('case, the blue button in', lines, scene, held=held, cable=BENCH_CABLE)


BUTTON_DOWN = 70.0                                                 # a button held over its place in H6 (below it: the case is turned over)


def button_way(k, clear=(-26.0, 0.0, 0.0)):
    """A button from where it stands on the bench: moved clear of the module, lifted (the case is turned over: up on screen is down
    here) above the case, turned and carried over its pocket in H6, then pressed in, a beat each (Lee's second round: in one move it
    passed through H5). Moved 26 mm clear (14 before; the others also 8 mm along the row): the white one, and then its wires, rose
    through the blue one's wires, which run from behind H4 to the module over the others' bench places; 30 mm brought them within
    2 mm of H5's tongue (an independent review, 20 Oct 2026)."""
    mid = GEO['parts'][BUTTONS[k]]['middle']
    cx, cy, cz = clear
    return [BUTTON_BENCH[k], compose([cx, cy, cz], BUTTON_BENCH[k], mid), compose([cx, cy - 110.0, cz], BUTTON_BENCH[k], mid),
            [0.0, -BUTTON_DOWN, 0.0], ZERO]


FIRST = 3                                                          # the blue button goes in first, as published
BUTTONS_IN = dict(view_dir=[0.0175, -0.6364, -0.7712], frame=([582.0, 905.0, 1300.0], 108.0))   # (the published guide's side: Step 33)
g.place('Bring the electronics back beside the case. Press the blue push button into the pocket in H6 farthest from H3, its pins towards H4.',
        move=[BUTTONS[FIRST]], appear=[MODULE, DISPLAY, MATRIX, USB_A] + [b for b in BUTTONS if b != BUTTONS[FIRST]] + JUMPER_CAPS,
        path=button_way(FIRST), lines=False, flip=True, labels={BUTTONS[FIRST]: HOVER_NAMES[BUTTONS[FIRST]]},
        wires=ON_THE_BENCH, wires_done=as_routes(first_button_layout(), MODULE_BENCH), **BUTTONS_IN)
OTHERS = [b for b in BUTTONS if b != BUTTONS[FIRST]]
done_others = as_routes(case_bench_layout(), MODULE_BENCH)      # (the blue button's wires too: they settle again among the others')
# (The case is turned over: on screen and in the student's hands its left and right are the other way round, so the pockets are named
# from the blue button's.)
g.place('Press the other three push buttons into their pockets the same way: white next to the blue one, then yellow, then black nearest H3.',
        move=OTHERS, paths={b: button_way(BUTTONS.index(b), clear=(-26.0, 0.0, -8.0)) for b in OTHERS}, lines=False, flip=True, eye=[OTHERS[0]],
        wires_done=done_others, labels_done=[dict(id=b, text=c.title(), side='left') for b, c in reversed(list(zip(BUTTONS, COLOURS)))],
        **BUTTONS_IN)   # (each named on Step 33c, where only their backs show: Lee's third round; in the caption's order, as a screen reader gets them)
g.place('Lay H7 on H6 the same way, over the push buttons: its tabs into the windows in H2, then into the notches in H3.',
        move=[H7], path=hinged(H7, [518.1, 897.39, 1357.17]), flip=True, labels={H7: 'H7'}, lines_at=[[547.8, 897.1, 1222.3], [501.9, 897.3, 1222.0], [502.1, 897.3, 1357.9], [547.7, 897.1, 1358.0]],   # (Lee's points)
        one_off_camera=True, **FLOOR_CAMERA)

# ---- the top of the case, the right way up again
ON_CASE = dict(focus_pad=1.15)
g.place('Turn the case the right way up. Push H8 down into the slots in H5, between H2 and H3.', move=[H8], direction=[0, 1, 0], hover=94.5,
        labels={H8: 'H8'}, view_dir=[-0.5792, 0.5736, -0.5792], frame=([529.0, 960.0, 1290.5], 108.0))   # (closer: Lee's second round)
KEY_CAMERA = dict(view_dir=[-0.5792, 0.5736, -0.5792], frame=([484.0, 930.0, 1290.5], 130.0))   # (the first key's: the next two steps keep it,
#                                                                                                Lee's first round; closer: their second)
g.place('Slide a piano key, H9, in from the front through H8 until its end clicks into the slot in H4.', move=[KEYS[0]], direction=[-1, 0, 0], hover=108,
        labels={KEYS[0]: 'H9'}, **KEY_CAMERA)
g.place('Slide the other three keys (H9) in the same way.', move=KEYS[1:], direction=[-1, 0, 0], hover=108,
        lines_at=[[[590.2, 914.2, z], [587.4, 914.2, z]] for z in (1273.7, 1307.5, 1341.1)], **KEY_CAMERA)   # (Step 36's line, from the
#   key's end to its slot in H4, at each key: Lee's points' slots, at the height of Step 36's, over the buttons' tops: Lee's third round)


def tipped(at, degrees, axis=(0, 0, 1)):
    return lambda t: turned(list(axis), degrees, at, t)


h10 = tipped([588.86, 931.08, 1290.5], -8.0)                       # (H10's front up 8 degrees about its rear tabs in H4)
g.place('Hook the rear tabs of H10 into the slots in H4, then lower its front onto H2 and H3 so that their top tabs click into it.',
        move=[H10], path=[h10([-124.0, 26.0, 0.0]), via(h10([-14.0, 0.0, 0.0])), h10(ZERO), ZERO], labels={H10: 'H10'}, lines_at=spots(H10, [H4]),
        **KEY_CAMERA)
TOP = CASE + [H8, H10] + KEYS
g.place('Push H11 down into the slot in H10, then slide it back until it clicks into H4.', move=[H11],                 # (punched in, from the
        path=[[-6.7, 53.1, 0.0], [-6.7, 0.0, 0.0], ZERO], labels={H11: 'H11'},                                            # top corner nearest H1's
        view_dir=[-0.5792, 0.5736, 0.5792], frame=([556.0, 982.0, 1302.0], 72.0))                                         # code: Lee's first round)
g.place('Fit H12 in the same way.', move=[H12], path=[[-7.6, 44.5, 0.0], [-7.6, 0.0, 0.0], ZERO], labels={H12: 'H12'},  # (from the other front
        view_dir=[-0.5792, 0.5736, -0.5792], frame=([556.0, 978.0, 1278.0], 72.0))                                         # corner: Lee's first round)
H13_UP = unit([-0.766, 0.643, 0.0])                                # (up its own slope, away from H4)
g.place('Slide H13 down between H11 and H12 until its hooks go into H4.', move=[H13], direction=H13_UP.tolist(), hover=80, labels={H13: 'H13'},
        view_dir=[0.5792, 0.5736, -0.5792], frame=([555.0, 995.0, 1290.0], 102.0))      # (closer: Lee's first round)

# ---- the electronics into the case. The I/O module goes onto the back of H4 (the USB end at the top: the published guide's way up),
# the display between H11 and H12, the dot matrix display on the front edges of H11 and H12. Each is picked up first (an eye), then
# placed (an arrow or lead lines), as published.
MODULE_HELD = POSES['module_held']
DISPLAY_HELD, DISPLAY_HALF = POSES['display_held'], POSES['display_half']
MATRIX_HELD, MATRIX_HALF = POSES['matrix_held'], POSES['matrix_half']
SEATED_CABLE = usb_cable(None, None)['usb cable']['pts']
HELD_CABLE = usb_cable(MODULE_HELD, None)['usb cable']['pts']
SEATED = {b: None for b in BUTTONS}
AT_THE_BACK = [(USB_A, None)]                                      # (the USB cable's A end, on the table behind the case)

# Behind the module (round1_plan.md): rows 4 - 7 (the buttons) at the bottom, their wires coming up from under H4, each button's a
# little further out than the row below's; rows 8 - 9 (the display) out to D_X, then along beside the Nano Board, under the dot
# matrix display's wires, and up beyond the module's end; rows 11 - 13 (the dot matrix) outermost.
NEST_X = [610.5, 614.1, 617.7, 621.3]
UNDER_NANO_Y = 909.0                                               # (the Nano Board stands out to x 618 from y 917 up, z 1281 - 1299)
D_X, M_BRIDGE_X = 624.5, 672.0


def button_lines_to(module_pose):
    """Every button's wires from the case up behind H4 into its row (the module at module_pose), side by side all the way (a row's
    G, V and S lie along z, as the pins in the case do); OUT and VCC change places under H4, one passing under the other."""
    lines = {}
    for k, b in enumerate(BUTTONS):
        way = in_case_way(k)
        e = middle_ends(b, None, module_pose)[1]
        x, zp = NEST_X[k], way[-1][2]
        up = [[x - 1.5, 899.5, zp], [x, 904.0, zp + 0.5 * (e[2] - zp)], [x, UNDER_NANO_Y, e[2]], [x, e[1] - 4.0, e[2]]]
        lines.update(bundle_lines(b, None, module_pose, way + up, lead=(3.0, x - 606.5), twist=(way[-4], way[-1])))
    return lines


def module_held_layout():
    lines = button_lines_to(MODULE_HELD)
    d, m = middle_ends(DISPLAY, DISPLAY_BENCH, MODULE_HELD)[1], middle_ends(MATRIX, MATRIX_BENCH, MODULE_HELD)[1]
    lines.update(bundle_lines(DISPLAY, DISPLAY_BENCH, MODULE_HELD, [[652.0, 940.0, 1262.0], [640.0, 990.0, 1266.0], [628.0, d[1] - 8.0, 1271.0], [D_X, d[1], d[2]]]))
    lines.update(bundle_lines(MATRIX, MATRIX_BENCH, MODULE_HELD, [[656.0, 940.0, 1350.0], [650.0, 990.0, 1320.0], [640.0, m[1] - 10.0, 1290.0], [628.0, m[1], m[2] + 3.0]]))
    scene = on_screen(MODULE_HELD, {**SEATED, DISPLAY: DISPLAY_BENCH, MATRIX: MATRIX_BENCH}, case=CASE_ALL, extra=AT_THE_BACK)
    return settled('the module held over H4', lines, scene, cable=HELD_CABLE)


D_END, M_END = (np.asarray([606.5, 938.4, 1273.7]), np.asarray([606.5, 946.6, 1274.1]))   # (the module ends' middles, seated)
D_BACK = [[D_X, 943.0, 1296.0], [D_X, D_END[1], 1281.0], [D_X, D_END[1], D_END[2]]]           # (up beyond the module's end, then in)
M_BRIDGE = [[656.0, 932.0, 1352.0], [667.0, 946.0, 1336.0], [M_BRIDGE_X, 950.0, 1300.0], [M_BRIDGE_X - 2.0, M_END[1] + 1.0, 1280.0],
            [650.0, M_END[1], M_END[2]]]                                                       # (the matrix on the bench: over the display's way)
M_ROUND_H3 = [[592.0, 953.0, 1225.0], [612.0, 951.0, 1240.0], [628.0, 948.0, 1256.0], [628.0, M_END[1], 1268.0]]   # (well over H4's top corner)


def over_h4(pins_y, lead_end):
    """The display's wires from its pins (out along +z, at height pins_y) round the outside of H11 and over H4 to D_BACK."""
    return [[lead_end[0] + 16.0, pins_y - 2.0, 1330.0], [597.0, max(pins_y - 6.0, 979.0), 1331.0], [614.0, max(pins_y - 18.0, 971.0), 1326.0],
            [623.0, 958.0, 1314.0]] + D_BACK


def mounted_layout():
    """The module on the back of H4; the display and the matrix still on the bench."""
    lines = button_lines_to(None)
    lines.update(bundle_lines(DISPLAY, DISPLAY_BENCH, None, [[650.0, 930.0, 1258.0], [632.0, 936.0, 1268.0], [D_X, D_END[1], D_END[2]]]))
    lines.update(bundle_lines(MATRIX, MATRIX_BENCH, None, M_BRIDGE))
    scene = on_screen(None, {**SEATED, DISPLAY: DISPLAY_BENCH, MATRIX: MATRIX_BENCH}, case=CASE_ALL, extra=AT_THE_BACK)
    return settled('the module on H4', lines, scene, cable=SEATED_CABLE)


def display_layout(name, pose, way):
    """The display's wires with the display at `pose` (its way to the module: `way`), the buttons' and the matrix's held. (H14, the
    last part, is kept clear of only by the wires that stay to the end: the display's in its place.)"""
    held = {w: p for w, p in mounted_layout().items() if WIRE_DEVICE[w] != DISPLAY}
    case = CASE_ALL if pose is None else [p for p in CASE_ALL if p != H14]
    scene = on_screen(None, {**SEATED, DISPLAY: pose, MATRIX: MATRIX_BENCH}, case=case, extra=AT_THE_BACK)
    return settled(name, bundle_lines(DISPLAY, pose, None, way), scene, held=held, cable=SEATED_CABLE)


def matrix_layout(name, pose, way):
    """The matrix's wires with the matrix at `pose`, the buttons' and the display's (in its place) held."""
    held = {**{w: p for w, p in mounted_layout().items() if WIRE_DEVICE[w] in BUTTONS}, **display_seated()}
    case = CASE_ALL if pose is None else [p for p in CASE_ALL if p != H14]
    scene = on_screen(None, {**SEATED, DISPLAY: None, MATRIX: pose}, case=case, extra=AT_THE_BACK)
    return settled(name, bundle_lines(MATRIX, pose, None, way), scene, held=held, cable=SEATED_CABLE)


def pins_at(device, pose):
    """The middle of a device's wire ends at `pose`, and that point `lead` mm out (where its ribbon's way starts)."""
    a = middle_ends(device, pose, None)[0]
    return a, a + unit(np.mean([cap_end(DEV_CAP[w], pose)[1] for w in DEVICE_WIRES[device]], axis=0)) * 6.0


def display_way(pose):
    a, lead_end = pins_at(DISPLAY, pose)
    return over_h4(float(a[1]), lead_end)


display_seated = lambda: display_layout('the display in place', None, display_way(None))


# The display's way up (Lee's first round: it passes under the dot matrix display's wires, then up to its place): slid along behind the
# module, under the matrix's wires (into the space between them and the module), lifted straight up there, over the top of the case,
# and held over its place.
_dmid = GEO['parts'][DISPLAY]['middle']
DISPLAY_UNDER = compose([-17.0, -6.0, 84.0], DISPLAY_BENCH, _dmid)
DISPLAY_UP = compose([-17.0, 104.0, 84.0], DISPLAY_BENCH, _dmid)
DISPLAY_OVER = compose([0.0, 34.0, 0.0], DISPLAY_HELD, _dmid)


def tunnel_way(pose, up):
    """The display's wires while it is behind the module (slid under the matrix's wires, or lifted there): out of its pins, round its
    end and back along beside it to the module."""
    a, lead_end = pins_at(DISPLAY, pose)
    if not up:
        return [[633.0, lead_end[1] + 5.0, 1338.0], [D_X + 1.5, 933.0, 1328.0], [D_X, 938.0, 1305.0]] + D_BACK[1:]
    return [[633.0, lead_end[1] - 2.0, 1338.0], [D_X + 1.5, lead_end[1] - 12.0, 1332.0], [D_X, 990.0, 1318.0]] + D_BACK


# The matrix's way to the front (Lee's first round: without passing through the case): lifted straight up, carried over the top of the
# case, turned to face the front, and held in front of H11 and H12.
_mmid = GEO['parts'][MATRIX]['middle']
MATRIX_UP = compose([0.0, 125.0, 0.0], MATRIX_BENCH, _mmid)
MATRIX_OVER = compose([0.0, 70.0, 0.0], MATRIX_HELD, _mmid)


def matrix_way(pose, high=False):
    a, lead_end = pins_at(MATRIX, pose)
    if high and pose is MATRIX_UP:
        return [[655.0, lead_end[1] - 9.0, 1345.0], [660.0, 1000.0, 1320.0], [650.0, 960.0, 1290.0], [630.0, M_END[1], 1276.0]]
    if high:
        return [[548.0, lead_end[1] + 1.0, 1210.0], [580.0, lead_end[1] - 9.0, 1222.0], [605.0, 1010.0, 1240.0], [622.0, 970.0, 1260.0],
                [628.0, 950.0, 1271.0]]
    return [[lead_end[0] + 16.0, lead_end[1] - 3.0, 1209.0], [570.0, lead_end[1] - 6.0, 1213.0]] + M_ROUND_H3


def usb_outside():
    """The USB cable from Step 47 on (Lee's second round): out of the plug, over the dot matrix display's wires and down outside them
    to its A end on the table (before, it came down between them and the case), settled among the wires as they are at the end."""
    name = 'usb cable outside'
    if name not in LAYOUTS:
        start, a_exit = np.asarray(USB['plug_exit'], float), np.asarray(USB['a_exit'], float)
        way = [start, start + unit(USB['plug_out']) * 8.0, [632.0, 975.0, 1256.0], [646.0, 962.0, 1252.0], [648.0, 932.0, 1250.0],
               [638.0, 904.0, 1248.0], a_exit + unit(USB['a_out']) * 8.0, a_exit]
        line = W.resample(W.smooth(way, start_dir=unit(USB['plug_out']), end_dir=-unit(USB['a_out']), spacing=0.5), 1.0)
        held = {**{w: p for w, p in mounted_layout().items() if WIRE_DEVICE[w] in BUTTONS}, **display_seated(),
                **matrix_layout('the matrix in place', None, matrix_way(None))}
        scene = on_screen(None, {**SEATED, DISPLAY: None, MATRIX: None}, case=CASE_ALL, extra=AT_THE_BACK)
        report = []
        LAYOUTS[name] = R.settle({'usb cable': line}, fixed=held, parts=SURFACES.placed(scene), skip={'usb cable': {USB_B, USB_A}},
                                 radii={'usb cable': 1.75}, report=report)['usb cable']
        print(f'  wires, {name}: settled among {len(held)} held, {report[0]}')
    return {'usb cable': W.route(LAYOUTS[name], a=USB_B, b=USB_A, stretch=True)}


# Each from the published guide's side (its Steps 45 - 51), framed on the action; the display, the dot matrix display and H14 from in
# front, where their faces are.
# Step 42 (Lee's third and fourth rounds, 20 - 21 Oct 2026). The fourth: "still a mess and the animation is way too slow and weird
# now. How about you try moving the IO module through the gap between the Dot matrix display wires and the Blue Push Button's wires
# (moving the USB cable in unison up and letting it settle between the Black Push button's wires and the 4-digit display's wires."
# On the bench the buttons' bundles come to the module from the case (-x), side by side (the black one at -z, the blue at +z), the
# display's from -z and the matrix's from +z; the USB cable runs from the plug, at the module's +z end, out through the corner between
# the blue button's bundle and the matrix's to its A end beside the case. Five beats (4 s; round 3's took ten): the module lifted and
# spun flat a quarter turn, its USB end swinging through that corner towards the case, while the A end is lifted straight up out of
# it and turned the right way up; the module stood up onto H4 (its USB end rising, its face turning to the back) while the A end goes
# up with it, over the module's top to its display side; then the A end straight down there, beside the 4-digit display, set down
# and slid in under the display's end, the cable coming out of the plug towards the display's side and down between the black
# button's wires and the display's. Seen from behind (Lee, the same round: "from behind the model instead of up and above it"), as
# Steps 41 and 43 are: from there the A end, carried across below the module's top (as it was for the view from the front), passed
# between the wires and H4, and from over the middle of the top, down across the display's wires; over the top to the display side
# and straight down it crosses nothing. Of the ways compared (round4/scripts/path42.py), spinning first and
# standing up second crossed the button bundles about half as often as the shortest turn or standing up first; the A end's way was
# screened against the moving module, the wires and the parts, and drawn over the wires from the camera (round4/scripts/eval42n.py,
# eval42top.py, eval42top2.py); the camera's frame fitted to keep it all clear of the caption box at four window sizes (fit42.py). While the module spins every wire keeps the shape it had on the bench and is bent
# with the module (wholly from where it first lies over it, `b_whole`, less and less towards its far end); as it stands up the wires
# take their shapes over H4, matched from each end (`tail_from`).
_MODULE_SEATED = np.vstack([np.asarray(g.model.inst[p].vertices) for p in (MODULE, NANO, USB_B)])


def over_module(pose, margin=3.0, above=25.0):
    """A test for points lying over the module, its Nano Board or the USB plug at `pose`: within their box in the module's own frame,
    from just under the board to `above` mm off its component side (+x where it sits on H4), whichever way it is turned."""
    Xi = np.linalg.inv(_matrix(pose if pose is not None else ZERO))
    lo, hi = _MODULE_SEATED.min(0) - margin, _MODULE_SEATED.max(0) + [above, margin, margin]

    def over(p):
        q = np.asarray(p, float) @ Xi[:3, :3].T + Xi[:3, 3]
        return np.all((q > lo) & (q < hi), axis=1)
    return over


def turned_by(R, centre, middle):
    """A pose: turned by the rotation matrix R from where the part sits, about the point `centre` (its middle), that point moved to `middle`."""
    from scipy.spatial.transform import Rotation
    rv = Rotation.from_matrix(R).as_rotvec()
    angle = float(np.linalg.norm(rv))
    centre = np.asarray(centre, float)
    if angle < 1e-9:
        return (np.asarray(middle, float) - centre).round(3).tolist()
    return turned((rv / angle).round(6).tolist(), round(float(np.degrees(angle)), 4), centre.round(3).tolist(),
                  (np.asarray(middle, float) - centre).round(3).tolist())


def upright(deg):
    """A turn of `deg` about the vertical."""
    from scipy.spatial.transform import Rotation
    return Rotation.from_rotvec(np.radians(deg) * np.array([0.0, 1.0, 0.0])).as_matrix()


_on_bench = {DISPLAY: DISPLAY_BENCH, MATRIX: MATRIX_BENCH}
_mid_module = np.asarray(GEO['parts'][MODULE]['middle'], float)
_mid_a = np.asarray(GEO['parts'][USB_A]['middle'], float)
_mid_bench, _mid_held = np.asarray(apply_pose(MODULE_BENCH, _mid_module)), np.asarray(apply_pose(MODULE_HELD, _mid_module))
MODULE_SPUN = turned_by(upright(-90.0) @ _matrix(MODULE_BENCH)[:3, :3], _mid_module, (_mid_bench + _mid_held) / 2 + [0.0, 40.0, 0.0])
#   (spun flat a quarter turn on its way up, half way there and 40 mm higher: its USB end, at +z on the bench, towards the case)
_held_lines = module_held_layout()


def bent(route, pose):
    """A route's centre line as the player draws it with the module at `pose` (bent by its b_whole / b_from weights, or its default
    ramp), for settling the USB cable among the wires as they are part of the way."""
    p = np.asarray(route['pts'], float)
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    if route.get('a_whole') is not None or route.get('b_whole') is not None:
        lo, hi = max(route.get('a_whole') or 0.0, route.get('b_from') or 0.0), route.get('b_whole', s[-1])
        t = np.clip((s - lo) / max(1e-6, hi - lo), 0.0, 1.0)
    else:
        u = (s - route['b_from']) / max(1e-6, s[-1] - route['b_from']) if route.get('b_from') else s / s[-1]
        t = np.clip((u - 0.1) / 0.8, 0.0, 1.0)
    B = _matrix(pose) @ np.linalg.inv(_matrix(route['b_ref']))
    return p + (t * t * (3 - 2 * t))[:, None] * ((p @ B[:3, :3].T + B[:3, 3]) - p)


CABLE_NEAR = 40.0   # (mm of the USB cable out of its plug that turn with the plug while the module turns: stretched, carried by its ends'
#                     moves only, it folded flat there: the review of 21 Oct)


def usb_at(name, mod_pose, a_pose, via_pts, fixed, near=False):
    """The USB cable with the module at mod_pose and its A end at a_pose, drawn through `via_pts`, settled among the wires `fixed` and
    the parts on screen. near: matched from each end, its first CABLE_NEAR mm turning with the plug (a shape the module turns into or
    out of), not stretched."""
    if name not in LAYOUTS:
        start, sdir = np.asarray(apply_pose(mod_pose, USB['plug_exit'])), unit(turn_dir(mod_pose, USB['plug_out']))
        end, edir = np.asarray(apply_pose(a_pose, USB['a_exit'])), unit(turn_dir(a_pose, USB['a_out']))
        line = W.resample(W.smooth([start, start + sdir * 8.0, *map(np.asarray, via_pts), end + edir * 8.0, end], start_dir=sdir, end_dir=-edir,
                                   spacing=0.5), 1.0)
        scene = on_screen(mod_pose, {**SEATED, DISPLAY: DISPLAY_BENCH, MATRIX: MATRIX_BENCH}, case=CASE_ALL, extra=[(USB_A, a_pose)])
        report = []
        LAYOUTS[name] = R.settle({'usb cable': line}, fixed=dict(fixed), parts=SURFACES.placed(scene), skip={'usb cable': {USB_B, USB_A}},
                                 radii={'usb cable': 1.75}, report=report)['usb cable']
        print(f'  wires, {name}: settled among {len(fixed)} wires, {report[0]}')
    return W.route(LAYOUTS[name], a=USB_B, b=USB_A, a_at=mod_pose, b_at=a_pose, stretch=not near,
                   **(dict(tail_from=CABLE_NEAR, a_whole=CABLE_NEAR) if near else {}))


_bench_wires = as_routes({**case_bench_layout(), **{w: p for w, p in bench_layout().items() if WIRE_DEVICE[w] in (DISPLAY, MATRIX)}}, MODULE_BENCH,
                         _on_bench, held_in_case=True, tail=True, shared=[MATRIX])
_near = dict(tail_from=CABLE_NEAR, a_whole=CABLE_NEAR)
_bench_cable = W.route(BENCH_CABLE, a=USB_B, b=USB_A, a_at=MODULE_BENCH, b_at=USB_A_BENCH, **_near)
_held_wires = as_routes(_held_lines, MODULE_HELD, _on_bench, held_in_case=True, tail=True)
A_UP = turned_by(upright(-90.0), _mid_a, [670.0, 1025.0, 1399.0])   # (lifted straight up out of the corner, the right way up, its cable end towards the module)


def spun_matrix_layout(others):
    """The dot matrix's wires with the module spun flat (Step 42's first stop), settled among `others`: straight up out of their pins,
    then over and down to the matrix on the bench. (On the bench they come in over the USB plug; bent with the module, that drape stood
    up with the module's USB end and folded into a tent above it, seen from behind: Lee's fourth round. Straight up, they turn out of
    the module's face as it stands up, as they come out of it over H4. Laid along the board away from the plug instead, they folded
    halfway through the first beat. The change from the bench shape, less than half as long, is matched by head_first, below.)"""
    lines = bundle_lines(MATRIX, MATRIX_BENCH, MODULE_SPUN, [[651.0, 955.0, 1345.0], [646.0, 1010.0, 1322.0], [634.0, 1034.0, 1296.0],
                                                             [624.0, 1030.0, 1281.0]])   # (from the matrix)
    scene = on_screen(MODULE_SPUN, {**SEATED, DISPLAY: DISPLAY_BENCH, MATRIX: MATRIX_BENCH}, case=CASE_ALL, extra=[(USB_A, A_UP)])
    return settled('the dot matrix wires, the module spun', lines, scene, held=others)


_spun_lines = {w: bent(r, MODULE_SPUN) for w, r in _bench_wires.items() if WIRE_DEVICE[w] != MATRIX}
_spun_lines.update(spun_matrix_layout(_spun_lines))
_spun_matrix = as_routes({w: p for w, p in _spun_lines.items() if WIRE_DEVICE[w] == MATRIX}, MODULE_SPUN, _on_bench, tail=True, shared=[MATRIX])

# The A end's way (and the module's stops), a beat each, the cable at each stop.
A_TOP = turned_by(np.eye(3), _mid_a, [650.0, 1110.0, 1215.0])     # (over the module's top as it stands up, to its display side, turned as it
#                                                                      will lie, its cable end towards the plug: from there it goes straight
#                                                                      down, clear of the display's wires)
WAY_42 = [(MODULE_SPUN, A_UP, usb_at('usb cable, the module spun', MODULE_SPUN, A_UP,
                                      [[598.0, 1030.0, 1258.0], [601.0, 1054.0, 1264.0], [630.0, 1046.0, 1316.0]], _spun_lines, near=True)),
#   (over the module's USB end, not across its face, where it hid the board as it spun, nor round it on the case's side, where the
#   change from its shape on the bench took it through the case's back corner: a check of 21 Oct (it still dips into the top of the case
#   for a moment in the first beat, up to 2.4 mm: README); up out of the plug, then to the A end: turned back on itself, in the run
#   that turns with the plug or beyond, it folded into a hook as the A end crossed over)
          (MODULE_HELD, A_TOP, usb_at('usb cable, the module held, the A end over its top', MODULE_HELD, A_TOP,
                                      [[611.0, 1082.0, 1252.0], [607.0, 1100.0, 1228.0]], _held_lines, near=True)),
#   (out of the plug towards the display's side and up into the A end, which faces it)
          (MODULE_HELD, turned_by(np.eye(3), _mid_a, [684.0, 992.0, 1180.0]), None),
          (MODULE_HELD, turned_by(np.eye(3), _mid_a, [667.048, 892.065, 1180.0]), None),
          (MODULE_HELD, ZERO, None)]
_cables = [WAY_42[0][2], WAY_42[1][2],
           usb_at('usb cable, the A end over', MODULE_HELD, WAY_42[2][1], [[606.0, 1080.0, 1250.0], [614.0, 1050.0, 1210.0], [628.0, 1000.0, 1186.0]], _held_lines),
           usb_at('usb cable, the A end set down', MODULE_HELD, WAY_42[3][1],
                  [[606.0, 1080.0, 1250.0], [612.0, 1050.0, 1215.0], [620.0, 990.0, 1190.0], [628.0, 930.0, 1183.0]], _held_lines),
           usb_cable(MODULE_HELD, None)['usb cable']]
_ride = {MODULE: [m for m, _, _ in WAY_42], USB_A: [a for _, a, _ in WAY_42]}


def head_first(route, tail=3.0):
    """`route` matched, between two such routes, by distance from its first end along all but its last `tail` mm. The dot matrix's
    wires and the USB cable change in Step 42's first beat between shapes 70 - 80 mm and 190 - 220 mm long; matched by distance from
    the far end beyond the first few mm (tail_from 7, or the cable's 40), the shorter one's points bunched where the two runs met and a
    small copy of the longer one's shape hung there, a zigzag by the matrix's header and a hairpin above the plug in the open; bunched
    at the far end instead, it is among the module's pins (the A end, at the start, lies behind the dot matrix display). (Only the
    bench cable: matched so, the cable lifted with the module and its next shape, 197 and 103 mm, bunched at the A end in view.)"""
    L = float(np.linalg.norm(np.diff(np.asarray(route['pts'], float), axis=0), axis=1).sum())
    return {**route, 'tail_from': round(L - tail, 2)}


_firsts = [w for w in ALL_WIRES if WIRE_DEVICE[w] == MATRIX]
_bench_wires.update({w: head_first(_bench_wires[w]) for w in _firsts})
_spun_matrix = {w: head_first(r) for w, r in _spun_matrix.items()}
_held_wires.update({w: head_first(_held_wires[w]) for w in _firsts})
_bench_cable = head_first(_bench_cable)
_wires_42 = {**{w: [_spun_matrix.get(w, _bench_wires[w])] + [_held_wires[w]] * (len(WAY_42) - 1) for w in ALL_WIRES}, 'usb cable': _cables}
assert all(len(x) == len(WAY_42) for x in [*_ride.values(), *_wires_42.values()])
# Lee, 21 Oct 2026, after round 4: "For Step 42, let's make an exception for this step only ... let's do a fade and reappear in final
# position transition, since the wiring is such a mess, and see how that looks." The module, all it carries, the USB cable's A end and
# every wire fade out where they lie on the bench and fade in where Step 42 leaves them (`reappear`). Lee, having seen it: "Let's keep
# the fade on 42." False would play round 4's way again (WAY_42, above: its shapes are still the ones the fade ends on).
STEP42_REAPPEAR = True
if STEP42_REAPPEAR:
    _ride = {MODULE: MODULE_HELD, USB_A: ZERO}
    _wires_42 = {**{w: _held_wires[w] for w in ALL_WIRES}, 'usb cable': _cables[-1]}
g.place("Pick up the I/O module, with everything plugged into it, and hold it over the back of H4, its USB end at the top. Lay the USB "
        "cable's other end on the table behind the case.",
        ride=_ride, ride_beats=not STEP42_REAPPEAR, reappear=STEP42_REAPPEAR,   # (a beat each: see WAY_42; or fade and reappear)
        lines=False, labels=[], eye=[MODULE],
        wires={**_bench_wires, 'usb cable': _bench_cable},            # (the same shapes as Step 41c's, drawn to be bent: see above)
        review=("The module goes on H4 USB end up, as in the published guide. Your STEP has it USB end down, its power socket on H5's tongue. "
                "Which way up is right?"),
        wires_done=_wires_42,
        view_dir=[0.8387, 0.5446, 0.0], frame=([638.0, 1012.0, 1323.0], 126.0))   # (from behind: Lee's fourth round; round 3's view was
#   from the front of the case, high, which hid the buttons' wires behind H4. Straight behind, between Step 41's corner and Step 43's,
#   with the module's face square on)
_c = np.asarray(GEO['parts'][MODULE]['middle'])
SIDE = [0.0, 0.0, 35.5]                                            # (beside the module's +z edge, clear of its face and wires)
g.place('Lower the I/O module onto the back of H4, its edges into the notches in the tabs of H10.', move=[MODULE], path=[MODULE_HELD, ZERO],
        arrows=[dict(tail=(_c + SIDE).round(2).tolist(), head=(_c + SIDE - [0.0, 100.0, 0.0]).round(2).tolist(), normal=[0.7071, 0, 0.7071], part=MODULE)],
        labels=[dict(id=MODULE, text='Nano I/O Module', side='near-left', reach=0.11)],   # (to its left: Lee's second round)
        wires_done={**as_routes(mounted_layout(), None, {DISPLAY: DISPLAY_BENCH, MATRIX: MATRIX_BENCH}, held_in_case=True), **usb_cable(None, None)},
        view_dir=[0.6161, 0.4908, 0.6161], frame=([600.0, 985.0, 1290.0], 100.0))

d_routes = lambda name, pose, way: as_routes(display_layout(name, pose, way), None, {DISPLAY: pose})
# One step (Lee's second round: the two of the first round combined): under the dot matrix display's wires, a pause, then up behind
# the case, over the top and held over its place, a beat each (ride_beats), its wires keeping pace.
_under = d_routes('the display under the matrix wires', DISPLAY_UNDER, tunnel_way(DISPLAY_UNDER, up=False))
_up = d_routes('the display lifted behind the module', DISPLAY_UP, tunnel_way(DISPLAY_UP, up=True))
_over = d_routes('the display over the case', DISPLAY_OVER, display_way(DISPLAY_OVER))
_held = d_routes('the display held over its place', DISPLAY_HELD, display_way(DISPLAY_HELD))
g.place("Pick up the 4-digit display and pass it under the dot matrix display's wires, then lift it up behind the case and over the top. "
        "Hold it over the gap between H11 and H12, its digits towards the front.",
        ride={DISPLAY: [DISPLAY_UNDER, DISPLAY_UP, DISPLAY_OVER, DISPLAY_HELD]}, ride_beats=True, lines=False, labels=[], eye=[DISPLAY],
        wires_done={w: [_under[w], _up[w], _over[w], _held[w]] for w in DISPLAY_WIRES},
        view_dir=[0.7586, 0.6514, 0.0144], frame=([618.0, 962.0, 1278.0], 102.0))
_half = d_routes('the display half way down', DISPLAY_HALF, display_way(DISPLAY_HALF))
_in = as_routes(display_seated(), None)
g.place('Lower the 4-digit display into the notches in H11 and H12, then let it lean back against H13.', move=[DISPLAY],
        path=[DISPLAY_HELD, DISPLAY_HALF, ZERO], lines_at=spots(DISPLAY, [H11, H12], most=1), labels={DISPLAY: '4-Digit Display'},
        wires_done={w: [_half[w], _in[w]] for w in DISPLAY_WIRES}, view_dir=[-0.3466, 0.5631, 0.7502], frame=([560.0, 972.0, 1290.0], 70.0))

m_routes = lambda name, pose, way: as_routes(matrix_layout(name, pose, way), None, {MATRIX: pose})
_up = m_routes('the matrix lifted', MATRIX_UP, matrix_way(MATRIX_UP, high=True))
_over = m_routes('the matrix over the case', MATRIX_OVER, matrix_way(MATRIX_OVER, high=True))
_held = m_routes('the matrix held in front', MATRIX_HELD, matrix_way(MATRIX_HELD))
g.place('Pick up the dot matrix display, lift it over the case and hold it in front of H11 and H12, its LEDs towards the front.',
        ride={MATRIX: [MATRIX_UP, MATRIX_OVER, MATRIX_HELD]}, ride_beats=True, lines=False, labels=[], eye=[MATRIX],   # (a beat each: Lee)
        wires_done={**{w: [_up[w], _over[w], _held[w]] for w in MATRIX_WIRES}, **usb_outside()},     # (the USB cable out over the matrix's
        #                                                                                              wires as it goes: Lee's second round)
        view_dir=[-0.7334, 0.6108, 0.2983], frame=([575.0, 970.0, 1320.0], 115.0))
_half = m_routes('the matrix half way', MATRIX_HALF, matrix_way(MATRIX_HALF))
_in = m_routes('the matrix in place', None, matrix_way(None))
g.place('Hang the dot matrix display on the hooks at the front of H11 and H12, then let it lean back against them.', move=[MATRIX],
        path=[MATRIX_HELD, MATRIX_HALF, ZERO], lines_at=spots(MATRIX, [H11, H12], most=1), labels={MATRIX: 'Dot Matrix Display'},
        wires_done={w: [_half[w], _in[w]] for w in MATRIX_WIRES}, view_dir=[-0.62, 0.5, -0.6], frame=([540.0, 955.0, 1285.0], 85.0))

h14 = tipped([548.0, 968.0, 1290.5], 10.0)                         # (H14's top out 10 degrees about its bottom edge)
SLOPE, OUTWARD = unit([0.643, 0.766, 0.0]), unit([-0.766, 0.643, 0.0])
_h14 = g.model.inst[H14].vertices
_feet = _h14[_h14[:, 1] < _h14[:, 1].min() + 1.0]
H14_TABS = [_feet[_feet[:, 2] < 1290.5].mean(0).round(2).tolist(), _feet[_feet[:, 2] > 1290.5].mean(0).round(2).tolist()]   # (its two tabs' feet)
g.place('Fit H14 over the 4-digit display: set its two bottom tabs down onto the top edge of the dot matrix display, then swing its top in '
        'until its two slots go over the tops of H11 and H12.', move=[H14],
        path=[h14((SLOPE * 10.0 + OUTWARD * 50.0).round(2).tolist()), h14((SLOPE * 10.0 + OUTWARD * 6.0).round(2).tolist()),
              h14((SLOPE * 10.0).round(2).tolist()), h14(ZERO), ZERO],                                     # (a beat each: Lee's first round, slower)
        labels=[dict(id=H14, text='H14', anchor=CODES[H14][1])], lines_at=[[568.8, 1001.8, 1270.9], [569.0, 1002.5, 1310.1]] + H14_TABS,   # (the upper two: Lee's points)
        inset=dict(target=H14_TABS[0], dir=[0.15, 0.97, -0.2], radius=15.0, mark=6.0,       # (from above: the tab is behind the LEDs' top edge)
                   alt="Close-up of H14's tab resting in the top edge of the dot matrix display."),
        view_dir=[-0.65, 0.6, -0.46], frame=([552.0, 975.0, 1290.0], 78.0))
# The title page: the camera solved from Lee's screenshot of it (21 Oct 2026: "On the starting view / completed view, let's go for
# this camera position / zoom for the PMG"; the Completed View then centred, below), the finished game from the front, on the
# student's right, seen a little lower than before. shift=0: the player moves it aside only where that lets the model be bigger (windows near
# square or upright: 1 degree round at 900 x 880, 8 on a phone held upright); in wider windows it is seen from exactly there.
# The Completed View has no logo or title beside the model, and centres it (Lee, the same day: "Centre the model on the Completed
# View; keep the title page as it is"): seen from the same place as the title page (the eye 3.4 mm from it in windows 1.2 times as
# wide as the picture is tall or more, every landscape size measured), turned to look at the model's middle, at the same distance
# (radius). The same faces show; the picture is turned about 4 degrees more level than the title page's, and the model is 75% of
# the frame's height (the title page's, off to the side, is stretched a little by the perspective to 78%). Only moving the camera
# sideways would have shown the model 8 degrees round from Lee's view. The player hardly moves it aside in any window (6 mm, 0.6
# degrees from Lee's view, on a phone held upright, where the title page is the one moved aside).
# Were: title page dir=[-0.3999, 0.546, 0.7362], target=[574.4, 947.3, 1290.5], radius=150.5, shift=0.7 (Lee's fifth round, moved
# right); Completed View dir=[-0.7157, 0.5739, 0.398], target=[532.0, 935.0, 1292.0], radius=112.0.
g.start_view = dict(dir=[-0.7723, 0.4726, 0.4246], target=[522.7, 912.3, 1235.3], radius=113.6, shift=0)
g.end_view = dict(dir=[-0.8363, 0.459, 0.2999], target=[546.0, 915.1, 1274.2], radius=113.6)
# ================================================================ THE CASE (end)

g.build()
