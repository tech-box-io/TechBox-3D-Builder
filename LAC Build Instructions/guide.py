"""LCD Alarm Clock (LAC), full build: the electronics on the breadboard, wired one wire at a time, then the laser-cut box closed
round them. The build, in order.

Run from the project root:   python "LAC Build Instructions/guide.py"
It writes steps.json (what the player shows) and parts.json (the parts list).

First draft (19 Oct 2026). The order, the wiring (which hole each wire goes in) and the motions follow TechBox's published Cadasio
guide (instructions.online/?id=19075-lac_full_build: docs/research/guide_19075-lac_full_build.md, and the digest and step pictures in
docs/research/lac/cadasio); the geometry is the engineer's STEP (LAC Full Build.STEP -> lac.glb, cut down by trim_source.py to the
parts the guide uses), measured in docs/research/lac (wire-paths.json: the breadboard's holes, the Dupont caps, every wire's centre
line, and the poses the CAD has each sub-assembly in). The Nano Board and the USB cable's A end are the MRA's models (Lee, 19 Oct
2026: "replacing each item in the LAC file with the version you used on either the MRA or RCC if it's present").
One part or one action per step; one wire per step, both ends of a loose wire in one step (docs/cadasio-patterns.md).
F5, F2 and F6 (the two end panels and the back) came as STEPs of their own (Lee, 19 Oct 2026), placed as TechBox's Cadasio project has them.

How things move. A part that has to lie somewhere, or be moved about, before it is finally seated (a jumper wire lying beside the
board, F4 with its switch lying beside the base, F1 with the potentiometer, the buzzer, the LCD, the F7s spread apart) rides on a
part that stays put (carry(): the breadboard or F3), and a step moves it by giving it a new riding pose (ride=); the step that
finally seats it moves it home from where it rides. A wire is drawn by the player along a route tied to the parts at its ends, so
it follows them; a step gives it a new route where it is plugged in or where its part comes to rest.
"""
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
import wires as W  # noqa: E402
from stepgen import Guide, apply_pose, compose, relative_pose, turned, unapply_pose, via  # noqa: E402

# ---------------------------------------------------------------- parts
# CAD instance ids (LAC Full Build). The box's front is +X (F1, with the LCD's window and the knob), its back -X; the buzzer's end
# -Z, the breadboard's end +Z. The breadboard's rows a - e lie towards the front, f - j towards the back; its columns 1 - 30 run
# from +Z to -Z; the (+) red and (-) blue rails used are along its front edge (the j side's rails are not used).
BREADBOARD, F3, RTC, COIN, RES1, RES2 = 'NAUO1', 'NAUO2', 'NAUO3', 'NAUO4', 'NAUO6', 'NAUO7'
F1, POT, NUT, KNOB, WASHER = 'NAUO10', 'NAUO11', 'NAUO12', 'NAUO13', 'NAUO146'
F7A, F7B, F8, F9 = 'NAUO42', 'NAUO43', 'NAUO44', 'NAUO45'          # F7A at the back (-X), F7B in front
F4 = 'F4'                                                           # the top panel, seated (materials.json "extra_parts": the CAD has it only lying beside the base)
F5, F2, F6 = 'F5', 'F2', 'F6'                                       # the end panel at the breadboard's end, the back, the end panel at the buzzer's end
                                                                    # (Lee's STEPs of their own, placed as TechBox's Cadasio project has them: materials.json)
SWITCH, BUZZER, LCD, USB_B, PAPER = 'NAUO46', 'NAUO62', 'NAUO94', 'NAUO122', 'NAUO141'
NANO, USB_A = 'NANO', 'USB_A'                                       # the MRA's Nano Board and USB A end (materials.json "extra_parts")

# The wires. Loose jumpers (male-male), in the order they go in, as published: colour, (cap, its hole's label) at each end, and the
# CAD body whose centre line is the wire's route plugged in (None: the CAD's is wrong, see below). The first end listed is the one
# the published step labels first.
JUMPERS_6 = [  # from the six-wire ribbon (Steps 9 - 14 in the published guide)
    ('black', ('NAUO16', 'i23'), ('NAUO17', '(+) red'), 'NAUO18'),
    ('green', ('NAUO20', '(-) blue'), ('NAUO19', 'i24'), 'NAUO23'),
    ('purple', ('NAUO25', 'a8'), ('NAUO26', 'i22'), 'NAUO27'),
    ('blue', ('NAUO22', 'a9'), ('NAUO21', 'i21'), 'NAUO24'),
    ('white', ('NAUO28', 'a14'), ('NAUO15', '(-) blue'), 'NAUO29'),
    ('dark_red', ('NAUO30', 'a12'), ('NAUO31', '(+) red'), None),   # (the CAD's dark red jumper, NAUO32, ends in a14 beside the white one: the published guide has a12)
]
JUMPERS_2 = [  # from the two-wire ribbon (published Steps 20, 21)
    ('orange', ('NAUO53', 'j1'), ('NAUO52', 'i27'), 'NAUO54'),
    ('yellow', ('NAUO56', 'j3'), ('NAUO55', 'i29'), 'NAUO57'),
]
# Leads that come on a part, in the order they go in (red, tan, black, as published): colour, cap, hole label, the lead's exit on its
# part (seated, measured from the CAD's straight leads), and for the buzzer the CAD bodies of the lead plugged in (lying, clamped).
SWITCH_LEADS = [('red', 'NAUO47', 'j27', [672.52, 929.76, 1258.37]), ('tan', 'NAUO49', '(+) red', [679.52, 929.76, 1258.37]),
                ('black', 'NAUO48', 'j29', [686.52, 929.76, 1258.37])]
POT_LEADS = [('red', 'NAUO34', '(+) red', [718.72, 906.79, 1229.65], 'NAUO157'), ('tan', 'NAUO33', 'a5', [718.72, 906.68, 1235.0], 'NAUO158'),
             ('black', 'NAUO14', '(-) blue', [718.72, 906.57, 1240.35], 'NAUO159')]
BUZZER_LEADS = [('red', 'NAUO58', 'j4', [674.5, 894.24, 1233.12], 'NAUO60', 'NAUO65'), ('black', 'NAUO59', '(-) blue', [676.02, 894.24, 1233.12], 'NAUO63', 'NAUO64')]
# The LCD's four wires (male-female): colour, male cap (breadboard), its hole's label, female cap (LCD header), the pin, and the CAD
# bodies of the wire with the LCD lying face down beside the base, standing just short of F9's notches, and seated.
LCD_WIRES = [('purple', 'NAUO82', '(-) blue', 'NAUO97', 'GND', 'NAUO83', 'NAUO117', 'NAUO101'),
             ('yellow', 'NAUO84', '(+) red', 'NAUO98', 'VCC', 'NAUO85', 'NAUO118', 'NAUO102'),
             ('teal', 'NAUO86', 'b8', 'NAUO99', 'SDA', 'NAUO87', 'NAUO119', 'NAUO103'),
             ('blue', 'NAUO93', 'b9', 'NAUO100', 'SCL', 'NAUO92', 'NAUO120', 'NAUO104')]
JUMPER_CAPS = [c for _, a, b, _ in JUMPERS_6 + JUMPERS_2 for c in (a[0], b[0])]
LEAD_CAPS = [w[1] for w in SWITCH_LEADS + POT_LEADS + BUZZER_LEADS]
LCD_MALE, LCD_FEMALE = [w[1] for w in LCD_WIRES], [w[3] for w in LCD_WIRES]

NAMES = {BREADBOARD: 'Breadboard', F3: 'F3', RTC: 'Real Time Clock', COIN: 'Real Time Clock', RES1: 'Resistor', RES2: 'Resistor',
         F1: 'F1', POT: 'Potentiometer', NUT: 'Potentiometer', KNOB: 'Potentiometer', WASHER: 'Potentiometer', F7A: 'F7', F7B: 'F7', F8: 'F8',
         F9: 'F9', F4: 'F4', F5: 'F5', F2: 'F2', F6: 'F6', SWITCH: 'Rocker Switch', BUZZER: 'Alarm Buzzer', LCD: 'LCD Screen', USB_B: 'USB Cable', USB_A: 'USB Cable',
         PAPER: 'Breadboard', NANO: 'Nano Board', **{c: 'Breadboard Wire (M-M)' for c in JUMPER_CAPS},
         **{c: 'Breadboard Wire (M-F)' for c in LCD_MALE + LCD_FEMALE}, **{w[1]: 'Rocker Switch' for w in SWITCH_LEADS},
         **{w[1]: 'Potentiometer' for w in POT_LEADS}, **{w[1]: 'Alarm Buzzer' for w in BUZZER_LEADS}}
# Parts that come on another (one line in the parts list): the coin cell in the clock module, the backing on the breadboard, and the
# potentiometer's knob, nut and washer (it comes with them on, as the published guide shows: Steps 22 - 24 take them off).
PART_OF = {COIN: RTC, PAPER: BREADBOARD, KNOB: POT, NUT: POT, WASHER: POT}
HOVER_NAMES = {KNOB: 'Knob', NUT: 'Nut', WASHER: 'Washer'}
# Named on hover only: the A end of the USB cable (listed by its Mini-B end), and the caps of the wires (the wires are listed by hand
# below; a lead's cap is named as its part).
UNLISTED = [USB_A] + JUMPER_CAPS + LEAD_CAPS + LCD_MALE + LCD_FEMALE

# The engraved code on each wood part (the way its face looks, the middle of the code, seated: measured from the CAD's engraving
# pockets), so the camera prefers a side from which it can be read.
CODES = {F3: ([0, 1, 0], [714.19, 887.48, 1234.4]), F1: ([1, 0, 0], [723.7, 895.78, 1221.91]),
         F7A: ([-1, 0, 0], [657.45, 940.02, 1233.35]), F7B: ([1, 0, 0], [693.05, 940.02, 1233.02]),
         F8: ([0, 0, -1], [707.73, 946.58, 1264.59]), F9: ([0, 0, 1], [698.74, 916.95, 1357.15]), F4: ([0, 1, 0], [714.0, 954.33, 1234.5]),
         F5: ([0, 0, 1], [652.46, 895.62, 1368.94]), F2: ([-1, 0, 0], [641.75, 895.78, 1358.52]), F6: ([0, 0, -1], [712.82, 895.74, 1210.8])}

# The parts list after the title page (as the MRA's and RCC's): electronics, the wires, the wood.
WOOD_BAND, WOOD_HALO = '#dbe4ef', '#8ea6c4'
PART_GROUPS = [
    ('Parts List', 'Electronics', 'electronics', '#f9c0c0', '#ec8d8d',
     lambda n: n in ('Breadboard', 'Nano Board', 'Resistor', 'Real Time Clock', 'Rocker Switch', 'Potentiometer', 'Alarm Buzzer', 'LCD Screen', 'USB Cable')),
    ('Parts List', 'Wires', 'electronics', '#fde3b8', '#f2bb63', lambda n: n.startswith('Breadboard Wire')),
    ('Parts List (Cont.)', 'Case', 'wood', WOOD_BAND, WOOD_HALO, lambda n: re.fullmatch(r'F\d+', n)),
]


def parts_list(parts):
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


PART_VIEWS = {'LCD Screen': {'dir': [0.8, 0.45, 0.4]}}              # (the parts list pictures the LCD from the front, its screen showing)
g = Guide(HERE, title='LCD Alarm Clock (LAC)', part='Full Build', names=NAMES, part_of=PART_OF, unlisted=UNLISTED, hover_names=HOVER_NAMES, part_views=PART_VIEWS,
          source='lac-guide.glb', codes=CODES, hero_azimuth=135,     # the finished clock from the front (F1: the screen and the knob), the knob's end
          parts_list=parts_list, copyright_line='© TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')

paths = W.load(HERE / 'wire-paths.json')
HOLES, CAPS, LINES = paths['holes'], paths['caps'], paths['lines']
BB_TOP = paths['breadboard']['top_y']
TABLE_Y = float(g.model.inst[F3].bounds[0][1])                      # the table: F3's underside
ZERO = [0.0, 0.0, 0.0]
COLOURS = {'black': 'jumper_black', 'green': 'jumper_green', 'purple': 'jumper_purple', 'blue': 'jumper_blue', 'white': 'jumper_white',
           'dark_red': 'jumper_dark_red', 'orange': 'jumper_orange', 'yellow': 'jumper_yellow', 'teal': 'jumper_teal'}
LEAD_COLOURS = {'red': 'lead_red', 'tan': 'lead_tan', 'black': 'lead_black'}
WIRE_R = 0.625                                                      # a jumper's or lead's radius (the CAD's: 1.25 mm across)
HOVER_MM = 18.0                                                     # how high a cap is held over its hole before it is pushed in
UP = [0.0, HOVER_MM, 0.0]


def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def tidy(pose):
    """A pose rounded as steps.json writes poses (a move to 0.1 mm; a turn's move and centre to 0.01 mm), so that what the generator
    composes from it and what the player composes from the rounded numbers agree (the run-through check allows 0.05 mm)."""
    if isinstance(pose, dict):
        return dict(pose, t=np.round(np.asarray(pose['t'], float), 2).tolist(), at=np.round(np.asarray(pose.get('at', [0, 0, 0]), float), 2).tolist(),
                    r=[*np.round(np.asarray(pose['r'][:3], float), 6).tolist(), round(float(pose['r'][3]), 6)])
    return np.round(np.asarray(pose, float), 1).tolist()


POSES = {k: tidy(v) for k, v in paths['poses'].items()}            # (the CAD's posed copies, relative to the seated ones)


def hole_label(text, cap):
    """A destination label on the hole a cap goes into."""
    x, _, z = CAPS[cap]['top']
    return dict(text=text, anchor=[x, BB_TOP, z], id=BREADBOARD)


def wire_at(cap):
    """Where a male cap standing in the breadboard holds its wire (the top of its pin, inside the housing; seated)."""
    return np.asarray(CAPS[cap]['wire_at'], float)


def cad_line(key, start_cap=None):
    """The centre line of a CAD wire body, starting at the end nearest start_cap's wire point."""
    line = np.asarray(LINES[key]['pts'], float)
    if start_cap is not None and np.linalg.norm(line[-1] - wire_at(start_cap)) < np.linalg.norm(line[0] - wire_at(start_cap)):
        line = line[::-1]
    return line


def lying(cap, point, outward):
    """The pose that lays a male cap (standing in the breadboard, seated) down, its wire point at `point` and its pin pointing along
    `outward` (horizontal)."""
    w = wire_at(cap)
    return tidy(turned(unit(np.cross([0, -1, 0], unit(outward))).tolist(), 90.0, w.round(2).tolist(), (np.asarray(point, float) - w).round(2).tolist()))


def arch(start, end, height, lift=6.0, shift=(0.0, 0.0, 0.0)):
    """A smooth wire up out of one hole and down into another, rising `height` mm over the higher end (its top moved by `shift`)."""
    s, e = np.asarray(start, float), np.asarray(end, float)
    p1, p2 = s + [0.0, lift, 0.0], e + [0.0, lift, 0.0]
    mid = (p1 + p2) / 2 + np.asarray(shift, float)
    body = W.smooth([p1, [mid[0], max(s[1], e[1]) + height, mid[2]], p2], start_dir=[0, 1, 0], end_dir=[0, -1, 0], spacing=0.5)
    return W.resample(W.join(W.straight(s, [0, 1, 0], lift), body, W.straight(p2, [0, -1, 0], lift)), 1.0)


def into_hole(cap, start, start_dir, controls, lift=6.0, above=10.0):
    """A lead from `start` (leaving along start_dir) through `controls` and straight down into a cap's housing in the breadboard."""
    top = wire_at(cap) + [0.0, 4.0 + above, 0.0]
    first = np.asarray(start, float) + unit(start_dir) * lift
    body = W.smooth([first, *[np.asarray(c, float) for c in controls], top], start_dir=unit(start_dir), end_dir=[0, -1, 0], spacing=0.5)
    return W.resample(W.join(W.straight(start, start_dir, lift), body, W.straight(top, [0, -1, 0], above + 4.0)), 1.0)


def posed_line(pose, pts):
    return apply_pose(pose, np.asarray(pts, float))


# ================================================================ THE BREADBOARD AND THE NANO BOARD (begin)
# The breadboard comes with a sticky backing on its underside: peeled off (it slides away below the breadboard), then the breadboard
# is stuck down onto F3, the base. (As published: Steps 1 and 2.)
BB_HOVER = 47.0                                                     # (published: 46.9 mm)
g.rest_at([BREADBOARD], [0.0, BB_HOVER, 0.0])
g.carry([PAPER], by=BREADBOARD)
_plo, _phi = g.model.inst[PAPER].bounds
BENCH_LOOK = [1, 1, -1]                                             # from the front, at the buzzer's end
_tail = [float(_phi[0]) - 4.0, float(_plo[1]) - 1.0, float(_plo[2]) + 4.0]   # (the arrow at the backing's front corner, out from under the breadboard)
g.place('Begin with the breadboard. Peel the protective backing off its underside.', appear=[BREADBOARD], ride={PAPER: [0.0, -50.0, 0.0]}, lines=False,
        arrows=[dict(tail=_tail, head=[_tail[0], _tail[1] - 26.0, _tail[2]], normal=[0.71, 0.0, -0.71], part=PAPER)],
        labels={BREADBOARD: 'Breadboard'}, look_from=BENCH_LOOK)
g.put_away([PAPER])
_lo, _hi = g.model.inst[BREADBOARD].bounds
BB_CORNERS = [[x, float(_lo[1]), z] for x in (float(_lo[0]) + 2.0, float(_hi[0]) - 2.0) for z in (float(_lo[2]) + 2.0, float(_hi[2]) - 2.0)]
g.place('Stick the breadboard down onto F3, its red and blue rails along the same edge of F3 as its engraved code.', move=[BREADBOARD], show=[F3],
        path=[[0.0, BB_HOVER, 0.0], ZERO], lines_at=BB_CORNERS, labels={F3: 'F3'}, look_from=BENCH_LOOK)
g.place('Press the Nano Board into the breadboard: its pins go in rows c and g, columns 1 to 15, with its USB socket at column 1.', move=[NANO],
        direction=[0, 1, 0], hover=40,
        labels=[dict(id=NANO, text='Nano Board'), dict(text='c15', anchor=HOLES['c15'], id=BREADBOARD), dict(text='g1', anchor=HOLES['g1'], id=BREADBOARD)],
        lines_at=[[[HOLES[h][0], 891.6, HOLES[h][2]], HOLES[h]] for h in ('c15', 'g1')], look_from=BENCH_LOOK)   # (each corner pin's tip, to its hole)

# The resistors: their legs bent down first (one view: the published guide swaps a straight-legged model for a bent one, which the
# player cannot; the CAD carries both, and the straight legs are left out of the model), then each pressed in from the (-) blue
# rail to row h.
RES_HOVER = 37.0
g.rest_at([RES1], [0.0, RES_HOVER, 0.0])
_res = g.model.inst[RES1].bounds.mean(0)
g.in_hand = [RES1]                                                  # (shown on its own, as published: a view of the resistor alone)
g.place('Bend the legs of both resistors down at right angles, like this, so that they fit the breadboard.', appear=[RES1], single=True, lines=False, staged=True,
        labels={RES1: '2x Resistor'}, frame=((_res + [0.0, RES_HOVER, 0.0]).round(1).tolist(), 24.0), look_from=BENCH_LOOK,
        review='The published guide shows the legs straight, then bent; this view shows them bent only (the player cannot swap a part '
               'for another of a new shape). Enough?')
g.in_hand = []


def resistor_lines(res):
    """Each leg's tip, straight down into its hole."""
    legs = [b for b in g.model.inst[res].split(only_watertight=False) if b.bounds[1][1] - b.bounds[0][1] > 6.0]
    tips = sorted([[float(b.bounds.mean(0)[0]), float(b.bounds[0][1]), float(b.bounds.mean(0)[2])] for b in legs])
    return [[t, [t[0], BB_TOP, t[2]]] for t in (tips[0], tips[-1])]


for res, h in ((RES1, 'h27'), (RES2, 'h29')):
    g.place(f"Press {'a' if res == RES1 else 'the other'} resistor into the breadboard, from the (-) blue rail to {h}.", move=[res],
            **(dict(path=[[0.0, RES_HOVER, 0.0], ZERO]) if res == RES1 else dict(direction=[0, 1, 0], hover=RES_HOVER)),
            labels=[dict(text='(-) blue', anchor=[paths['breadboard']['rails']['- blue'], BB_TOP, HOLES[h][2] + 1.1], id=BREADBOARD), dict(text=h, anchor=HOLES[h], id=BREADBOARD)],
            lines_at=resistor_lines(res), look_from=BENCH_LOOK)

# The real-time clock module (with its coin cell), its six pins along row j, j19 to j24.
g.place('Press the real time clock module into row j, its pins from j19 to j24, with its coin cell facing the back.', move=[RTC, COIN], direction=[0, 1, 0], hover=34,
        labels=[dict(id=RTC, text='Real Time Clock'), dict(text='j24', anchor=HOLES['j24'], id=BREADBOARD), dict(text='j19', anchor=HOLES['j19'], id=BREADBOARD)],
        lines_at=[[[HOLES[h][0], 893.69, HOLES[h][2]], HOLES[h]] for h in ('j24', 'j19')], look_from=BENCH_LOOK)
# ================================================================ THE BREADBOARD AND THE NANO BOARD (end)

# ================================================================ JUMPER WIRES (begin)
# A ribbon of jumper wires is laid out in front of the board and peeled into single wires (its own step, as published, the camera
# close on the ribbon); the wires then lie side by side in front of the board, and each step picks one up and plugs both its ends
# in: each cap is lifted, turned upright and held over its hole, then pushed in, the wire arching between them as the CAD routes it.
RIBBON_PITCH, SPLIT_PITCH = 1.75, 7.0                              # wire to wire, joined and peeled apart
RIBBON_MM = 66.0                                                    # a jumper's length between the tops of its two pins (the CAD's ribbon)
FRONT_X = 745.0                                                     # the nearest loose wire, 18 mm in front of F3
for colour, *_ in JUMPERS_6 + JUMPERS_2:
    g.wire(f'jumper {colour}', COLOURS[colour], WIRE_R, name='Breadboard Wire (M-M)')


def ribbon(jumpers, z_mid, pitch):
    """Where each jumper of a ribbon lies on the table in front of the board, along z, side by side in x: {colour: (pose of its first
    cap, pose of its second cap, the straight route between them)}. The first cap's pin points towards +z."""
    out = {}
    for k, (colour, (ca, _), (cb, _), _) in enumerate(jumpers):
        x = FRONT_X + k * pitch
        pa = np.array([x, TABLE_Y + 0.875, z_mid + RIBBON_MM / 2])
        pb = np.array([x, TABLE_Y + 0.875, z_mid - RIBBON_MM / 2])
        a, b = lying(ca, pa, [0, 0, 1]), lying(cb, pb, [0, 0, -1])
        out[colour] = (a, b, W.route(W.resample(np.linspace(pa, pb, 12), 1.0), a=ca, b=cb, a_at=a, b_at=b, stretch=True))
    return out


def jumper_done(ca, cb, key):
    """A jumper's route plugged in: the CAD's, or for the dark red one a low arch of the same kind (it clears the jumpers and the
    leads by the clock module)."""
    line = cad_line(key, ca) if key else arch(wire_at(ca), wire_at(cb), 8.0, shift=(0.0, 0.0, 3.0))
    return W.route(line, a=ca, b=cb, stretch=True)


def jumper_run(jumpers, z_mid, ribbon_caption, wire_caption, camera):
    """The ribbon peeled apart, then each of its wires plugged in."""
    joined, apart = ribbon(jumpers, z_mid, RIBBON_PITCH), ribbon(jumpers, z_mid, SPLIT_PITCH)
    caps = [c for _, a, b, _ in jumpers for c in (a[0], b[0])]
    for colour, (ca, _), (cb, _), _ in jumpers:
        g.carry([ca], by=BREADBOARD, pose=joined[colour][0], appear=False)
        g.carry([cb], by=BREADBOARD, pose=joined[colour][1], appear=False)
    mid = np.array([FRONT_X + (len(jumpers) - 1) * RIBBON_PITCH / 2, TABLE_Y + 1.0, z_mid])
    g.place(ribbon_caption, appear=caps, lines=False, labels=[], eye=[dict(anchor=mid.round(2).tolist())],
            wires={f'jumper {c}': joined[c][2] for c, *_ in jumpers}, wires_done={f'jumper {c}': apart[c][2] for c, *_ in jumpers},
            ride={c: apart[col][k] for col, (ca, _), (cb, _), _ in jumpers for k, c in ((0, ca), (1, cb))},
            frame=((mid + [8.0, 0.0, 0.0]).round(1).tolist(), 42.0), view_dir=[0.45, 0.8, -0.4])
    for k, (colour, (ca, la), (cb, lb), key) in enumerate(jumpers):
        a, b, _ = apart[colour]
        done = jumper_done(ca, cb, key)
        g.place(wire_caption.format(colour=colour.replace('_', ' '), a=la, b=lb), move=[ca, cb],
                paths={ca: [a, UP, ZERO], cb: [b, UP, ZERO]}, lines=False,
                labels=[hole_label(la, ca), hole_label(lb, cb)], eye=[dict(anchor=[FRONT_X + k * SPLIT_PITCH, TABLE_Y + 1.0, z_mid])],
                wires_done={f'jumper {colour}': [done, done]}, **camera)


# The jumper wires are kit parts, but in the CAD only their caps are parts (the wire is drawn): listed by hand, pictured straight with
# a cap at each end (as the MRA's breadboard wires).
_pic = ribbon(JUMPERS_6[:1], 1305.0, RIBBON_PITCH)['black']
_pa, _pb = np.asarray(_pic[2]['pts'][0], float), np.asarray(_pic[2]['pts'][-1], float)
g.list_part('Breadboard Wire (M-M)', ['NAUO16', 'NAUO17'], 8, after='Real Time Clock')
g.part_picture('Breadboard Wire (M-M)', poses={'NAUO16': _pic[0], 'NAUO17': _pic[1]},
               wires=[dict(colour='jumper_black', radius=WIRE_R, pts=np.linspace(_pa, _pb, 40))])
JUMPER_CAMERA = dict(view_dir=[0.62, 0.62, -0.48], frame=([710.0, 905.0, 1305.0], 74.0))
jumper_run(JUMPERS_6, 1305.0, 'Peel six wires off the ribbon of jumper wires, one of each colour, and lay them side by side.',
           'Connect the {colour} jumper wire from {a} to {b}.', JUMPER_CAMERA)
# ================================================================ JUMPER WIRES (end)

# ================================================================ THE ROCKER SWITCH (begin)
# The switch is pushed into the square hole in F4 with F4 lying beside the base (the camera close on F4: published, F4 alone), then
# its three leads are plugged in one at a time: red to j27, tan to the (+) red rail, black to j29. F4 lies at the CAD's place for it
# (behind the base, raised, the leads hanging under it).
FLAT_F4 = POSES['switch_flat_F4']                                   # F4 (and the switch in it) lying beside the base, relative to their seats
HOVER_F4 = POSES['switch_hover']                                    # F4 held over the frame, before it goes down onto the tabs
SW_HOVER = 50.0                                                     # (published: 81.2 mm; less, so that the switch and its leads stay in the close frame)
g.carry([F4], by=F3, pose=FLAT_F4, appear=False)
g.carry([SWITCH], by=F4, pose=[0.0, SW_HOVER, 0.0], appear=False)
DANGLE_MM = 30.0                                                    # each lead hangs this far below the switch (the CAD's: 30 mm)


def switch_hang(cap, exit_):
    """The cap hanging on its lead, straight under the lead's exit (relative to its seat, with the switch at its seat)."""
    return tidy(np.asarray(exit_, float) - [0.0, DANGLE_MM, 0.0] - wire_at(cap) - [0.0, 4.0, 0.0])


for colour, cap, _, exit_ in SWITCH_LEADS:
    g.wire(f'switch {colour}', LEAD_COLOURS[colour], WIRE_R, name='Rocker Switch')
    # the cap hanging on its lead, straight under the exit (relative to its seat, with the switch at its seat)
    g.carry([cap], by=SWITCH, pose=switch_hang(cap, exit_))


def switch_lead(colour, cap, exit_, pose, controls=None):
    """A switch lead with F4 (and the switch) at `pose`: hanging straight down, or plugged into its hole through `controls`."""
    e = posed_line(pose, [exit_])[0]
    if controls is None:
        line = W.resample(np.linspace(e, e - [0.0, DANGLE_MM + 4.0, 0.0], 12), 1.0)
        return W.route(line, a=SWITCH, b=cap, a_at=pose, b_at=compose(pose, switch_hang(cap, exit_)), stretch=True)
    return W.route(into_hole(cap, e, [0, -1, 0], controls), a=SWITCH, b=cap, a_at=pose, stretch=True)


_sw = g.model.inst[SWITCH].bounds
SW_TIP = [float(_sw.mean(0)[0]), float(_sw[0][1]), float(_sw.mean(0)[2])]     # (the switch body's bottom, seated)
F4_FLAT_FRAME = (posed_line(FLAT_F4, [[_sw.mean(0)[0], 960.0, _sw.mean(0)[2]]])[0].round(1).tolist(), 62.0)
g.place('Push the rocker switch, wires first, down into the square hole in F4 until it clicks in.', appear=[F4, SWITCH], ride={SWITCH: ZERO},
        lines_at=[[posed_line(FLAT_F4, [np.add(SW_TIP, [0.0, SW_HOVER, 0.0])])[0].round(2).tolist(),
                   posed_line(FLAT_F4, [[SW_TIP[0], 954.46, SW_TIP[2]]])[0].round(2).tolist()]],
        labels={F4: 'F4', SWITCH: 'Rocker Switch'}, wires={f'switch {c}': switch_lead(c, cap, e, FLAT_F4) for c, cap, _, e in SWITCH_LEADS},
        frame=F4_FLAT_FRAME, view_dir=[0.45, 0.75, -0.48])
SWITCH_CAMERA = dict(view_dir=[0.8, 0.42, -0.43], frame=([628.0, 928.0, 1272.0], 82.0))   # (from the front, low: the leads hang under F4)
# Each lead's way to its hole: down from the switch, across over F3's back edge in a lane of its own (keeping to the buzzer's side of
# the clock module and clear of the other two), and down into its hole.
SWITCH_WAY = {'red': [[566.0, 932.0, 1262.0], [620.0, 923.0, 1264.0], [654.0, 917.0, 1272.0]],
              'tan': [[570.0, 931.0, 1254.0], [620.0, 924.0, 1256.0], [655.0, 919.0, 1262.0], [688.0, 917.0, 1266.0]],
              'black': [[575.0, 930.0, 1258.5], [620.0, 922.0, 1260.5], [650.0, 916.0, 1265.0]]}
for colour, cap, label, exit_ in SWITCH_LEADS:
    start = compose(FLAT_F4, switch_hang(cap, exit_))
    done = switch_lead(colour, cap, exit_, FLAT_F4, SWITCH_WAY[colour])
    g.place(f"Connect the switch's {colour} wire to {label}.", move=[cap], path=[start, UP, ZERO], lines=False,
            labels=[hole_label(label, cap)], eye=[cap], wires_done={f'switch {colour}': [done, done]}, **SWITCH_CAMERA)
# ================================================================ THE ROCKER SWITCH (end)

# ================================================================ JUMPER WIRES, 2 (begin)
jumper_run(JUMPERS_2, 1305.0, 'Peel two wires off the ribbon of jumper wires, an orange and a yellow, and lay them side by side.',
           'Connect the {colour} jumper wire from {a} to {b}.', JUMPER_CAMERA)
# ================================================================ JUMPER WIRES, 2 (end)

# ================================================================ THE POTENTIOMETER AND F1 (begin)
# The potentiometer comes with its knob, nut and washer on: they come off one at a time (as published), the potentiometer goes through
# the round hole in F1 from the back, and they go back on in the opposite order. This is done with F1 standing upright well in front of
# the base (BUILD), the camera close on it. Then F1 is laid face down beside the base for its leads to be plugged in.
BUILD = [150.0, 35.0, 1.1]                                        # F1 held upright 150 mm in front of its seat, 35 mm up (its leads hang below it)
FRONT_OUT = POSES['F1_hover_front']                                 # F1 upright in front of the box, before it goes on (the CAD's)
FLAT_BESIDE = POSES['F1_flat_beside']                               # F1 face down beside the base, past the breadboard's end (the CAD's)
FLAT_OTHER_END = POSES['F1_flat_other_end']                         # F1 face up beyond the buzzer's end (the CAD's)
PULLED = [-79.0, 0.0, 0.0]                                          # the potentiometer behind F1, before it goes through (published: 79 mm)
OFF_MM = 38.0                                                       # how far the knob, nut and washer slide off the shaft (published: 37.6 - 37.9 mm)
ON_MM = 60.0                                                        # how far out each goes back on from (published: 56 - 61 mm)
DELIVERED = {KNOB: [4.611, 0.0, 0.0], NUT: [-3.0, 0.0, 0.0], WASHER: [-3.0, 0.0, 0.0]}   # (on the potentiometer as it comes: the knob as the CAD's "assembled" one; nut and washer against its body)
# F1 and the potentiometer both ride on F3 and are moved together (the same pose for each): a part riding on one whose own carrier
# is not on screen yet (the potentiometer before F1 appears) is mis-placed by the generator once something rides on it in turn.
g.carry([F1], by=F3, pose=BUILD, appear=False)
g.carry([POT], by=F3, pose=tidy(np.add(BUILD, PULLED)), appear=False)
for part in (KNOB, NUT, WASHER):
    g.carry([part], by=POT, pose=DELIVERED[part])
# Its leads hang straight down from its pins (the CAD has them lying straight out from F1's back with F1 face down beside the base).
for colour, cap, _, exit_, _ in POT_LEADS:
    g.wire(f'pot {colour}', LEAD_COLOURS[colour], WIRE_R, name='Potentiometer')
PLEN = 50.0                                                         # (the CAD's: 50 mm to the cap)


def pot_cap_rel(cap, exit_):
    """The cap on the end of a potentiometer lead hanging straight down from its pin, pin down as in the breadboard (relative to its seat,
    the potentiometer seated)."""
    return tidy(np.asarray(exit_, float) - [0.0, PLEN, 0.0] - wire_at(cap))


for colour, cap, _, exit_, _ in POT_LEADS:
    g.carry([cap], by=POT, pose=pot_cap_rel(cap, exit_))


def pot_hanging(colour, cap, exit_, f1_pose, pot_rel=ZERO):
    """A potentiometer lead hanging straight down from its pin, with F1 at f1_pose and the potentiometer at pot_rel on it."""
    pose = compose(f1_pose, pot_rel)
    e = np.asarray(exit_, float)
    line = posed_line(pose, W.resample(np.linspace(e, e - [0.0, PLEN, 0.0], 14), 1.0))
    return W.route(line, a=POT, b=cap, a_at=pose, b_at=compose(pose, pot_cap_rel(cap, exit_)), stretch=True)


_pot = g.model.inst[POT].bounds
SHAFT = [float(_pot[1][0]), 919.53, 1235.26]                        # the shaft's tip on the axis (seated)
BUILD_SIDE = [0.35, 0.45, -0.82]                                     # (across the shaft, from the buzzer's end)
POT_ALONE = dict(view_dir=BUILD_SIDE, frame=(posed_line(np.add(BUILD, PULLED).tolist(), [[735.0, 916.0, 1235.0]])[0].round(1).tolist(), 42.0))
BUILD_LOOK = dict(view_dir=BUILD_SIDE, frame=(posed_line(BUILD, [[722.0, 925.0, 1275.0]])[0].round(1).tolist(), 98.0))
for part, name, verb in ((KNOB, 'knob', 'Pull the knob off'), (NUT, 'nut', 'Unscrew the nut and take it off'), (WASHER, 'washer', 'Take the washer off')):
    c = g.model.inst[part].bounds.mean(0)
    here = posed_line(np.add(np.add(BUILD, PULLED), DELIVERED[part]).tolist(), [c])[0]
    first = part == KNOB
    g.place(f"{'Begin the front panel with the potentiometer. ' if first else ''}{verb} the potentiometer's shaft.", appear=[POT] if first else [],
            ride={part: np.add(DELIVERED[part], [OFF_MM, 0.0, 0.0]).tolist()}, lines=False,
            arrows=[dict(tail=(here + [4.0, 0.0, 0.0]).round(2).tolist(), head=(here + [34.0, 0.0, 0.0]).round(2).tolist(), normal=[0.0, 0.48, -0.88], part=F3)],
            labels={POT: 'Potentiometer'} if first else [], **({'wires': {f'pot {c_}': pot_hanging(c_, cap, e, BUILD, PULLED) for c_, cap, _, e, _ in POT_LEADS}} if first else {}),
            **POT_ALONE)
    g.put_away([part])
g.place("Push the potentiometer's shaft through the round hole in F1 from the back, its little tab in the slot beside the hole.", appear=[F1],
        ride={POT: BUILD}, lines_at=[[posed_line(np.add(BUILD, PULLED).tolist(), [SHAFT])[0].round(2).tolist(), posed_line(BUILD, [[723.83, 919.53, 1235.26]])[0].round(2).tolist()]],
        labels={F1: 'F1'}, wires_done={f'pot {c_}': pot_hanging(c_, cap, e, BUILD) for c_, cap, _, e, _ in POT_LEADS}, **BUILD_LOOK)
for part, name in ((WASHER, 'washer'), (NUT, 'nut'), (KNOB, 'knob')):
    g.carry([part], by=POT, pose=[ON_MM, 0.0, 0.0], appear=False)
    c = g.model.inst[part].bounds.mean(0)
    g.place(f"Put the {name} back on the shaft{', and tighten it against F1' if part == NUT else (', pushing it all the way on' if part == KNOB else ' against F1')}.",
            appear=[part], ride={part: ZERO}, lines_at=[[posed_line(np.add(BUILD, [ON_MM, 0.0, 0.0]).tolist(), [c - [float(g.model.inst[part].bounds[1][0] - g.model.inst[part].bounds[0][0]) / 2, 0.0, 0.0]])[0].round(2).tolist(),
                                                        posed_line(BUILD, [SHAFT])[0].round(2).tolist()]],
            labels=[], **BUILD_LOOK)
# F1 is laid face down beside the base, its potentiometer's leads towards the breadboard (as the CAD has it, and the published guide).
POT_CAMERA = dict(view_dir=[0.55, 0.7, 0.45], frame=([680.0, 905.0, 1440.0], 105.0))


def pot_flat_lead(colour, cap, exit_):
    """A potentiometer lead with F1 face down beside the base: straight out from its pin along F1's back (the CAD's)."""
    return pot_hanging(colour, cap, exit_, FLAT_BESIDE)


ASIDE = [150.0, 35.0, 225.0]                                        # (on the way: carried along, still upright, past the end of the base, then laid down)
g.place('Lay F1 face down beside the end of the base, as shown, with the potentiometer at the end nearer the breadboard.',
        ride={F1: [ASIDE, FLAT_BESIDE], POT: [ASIDE, FLAT_BESIDE]}, ride_beats=True, lines=False, eye=[F1],
        wires_done={f'pot {c}': [pot_hanging(c, cap, e, ASIDE), pot_flat_lead(c, cap, e)] for c, cap, _, e, _ in POT_LEADS},
        view_dir=[0.55, 0.7, 0.45], frame=([745.0, 930.0, 1420.0], 185.0))
# Each lead's way to its hole: out along F1's back, up over the buzzer and the LCD lying beside the base (and their wires), past
# the end of F9 (where F9 will stand: x < 689), and down into its hole. The black lead crosses over the other two (its pin is at the
# other side of them from its hole).
POT_WAY = {'tan': [[668.0, 917.0, 1560.0], [680.5, 920.0, 1530.0], [682.0, 921.0, 1460.0], [681.5, 921.0, 1400.0], [681.5, 921.0, 1365.0], [682.5, 921.0, 1352.0], [686.0, 920.5, 1341.0]],
           'red': [[668.0, 917.0, 1566.0], [684.5, 920.0, 1532.0], [684.5, 921.0, 1460.0], [684.0, 921.0, 1400.0], [684.0, 921.0, 1365.0], [685.0, 921.0, 1352.0], [691.5, 920.5, 1340.0]],
           'black': [[660.0, 916.0, 1556.0], [672.0, 921.0, 1535.0], [682.5, 925.5, 1505.0], [688.5, 923.0, 1465.0], [687.5, 921.5, 1400.0], [686.8, 921.5, 1365.0], [687.5, 921.5, 1352.0], [694.5, 921.0, 1341.0]]}


def pot_plugged(colour, cap, exit_, f1_pose, way):
    e = posed_line(f1_pose, [exit_])[0]
    d = unit(posed_line(f1_pose, [np.add(exit_, [0.0, -1.0, 0.0])])[0] - e)
    return W.route(into_hole(cap, e, d, way), a=POT, b=cap, a_at=f1_pose, stretch=True)


for colour, cap, label, exit_, _ in POT_LEADS:
    start = compose(FLAT_BESIDE, pot_cap_rel(cap, exit_))
    done = pot_plugged(colour, cap, exit_, FLAT_BESIDE, POT_WAY[colour])
    g.place(f"Connect the potentiometer's {colour} wire to {label}.", move=[cap], path=[start, UP, ZERO], lines=False,
            labels=[hole_label(label, cap)], eye=[cap], wires_done={f'pot {colour}': [done, done]}, **POT_CAMERA)
# ================================================================ THE POTENTIOMETER AND F1 (end)

# ================================================================ THE BUZZER (begin)
# The buzzer lies beside the base (the CAD's place for it, past the breadboard's end, at the back); its red lead goes to j4, its black
# lead to the (-) blue rail.
BUZZER_LYING = POSES['buzzer_lying']
g.carry([BUZZER], by=F3, pose=BUZZER_LYING, appear=False)
BLEN = 39.0                                                         # (the CAD's straight leads: 39 mm to the cap)
for colour, cap, _, exit_, _, _ in BUZZER_LEADS:
    g.wire(f'buzzer {colour}', LEAD_COLOURS[colour], WIRE_R, name='Alarm Buzzer')


def buzzer_cap_rel(cap, exit_):
    """The cap on the end of a buzzer lead lying straight out from the buzzer (relative to its seat, the buzzer seated): pin pointing
    away from the buzzer (the lead leaves it straight down when the buzzer is clamped)."""
    return tidy(np.asarray(exit_, float) - [0.0, BLEN, 0.0] - wire_at(cap))


for colour, cap, _, exit_, _, _ in BUZZER_LEADS:
    g.carry([cap], by=BUZZER, pose=buzzer_cap_rel(cap, exit_))


def buzzer_straight(colour, cap, exit_):
    e = np.asarray(exit_, float)
    line = posed_line(BUZZER_LYING, W.resample(np.linspace(e, e - [0.0, BLEN, 0.0], 12), 1.0))
    return W.route(line, a=BUZZER, b=cap, a_at=BUZZER_LYING, b_at=compose(BUZZER_LYING, buzzer_cap_rel(cap, exit_)), stretch=True)


BUZZER_CAMERA = dict(view_dir=[0.7, 0.55, 0.45], frame=([668.0, 905.0, 1362.0], 72.0))
for k, (colour, cap, label, exit_, lying_key, _) in enumerate(BUZZER_LEADS):
    start = compose(BUZZER_LYING, buzzer_cap_rel(cap, exit_))
    done = W.route(cad_line(lying_key, cap)[::-1], a=BUZZER, b=cap, a_at=BUZZER_LYING, stretch=True)
    g.place(f"{'Lay the alarm buzzer beside the base, past the end of the breadboard. ' if k == 0 else ''}Connect the buzzer's {colour} wire to {label}.",
            move=[cap], path=[start, UP, ZERO], lines=False, appear=[BUZZER] if k == 0 else [],
            labels=([dict(id=BUZZER, text='Alarm Buzzer')] if k == 0 else []) + [hole_label(label, cap)], eye=[cap],
            wires={f'buzzer {c}': buzzer_straight(c, cp, e) for c, cp, _, e, _, _ in BUZZER_LEADS} if k == 0 else None,
            wires_done={f'buzzer {colour}': [done, done]}, **BUZZER_CAMERA)
# ================================================================ THE BUZZER (end)

# ================================================================ THE LCD SCREEN (begin)
# The LCD lies face down beside the base (the CAD's place for it). A ribbon of four male-female wires is peeled apart; then each wire
# goes from a pin of the LCD's header (its female end) to the breadboard (its male end): GND to (-) blue, VCC to (+) red, SDA to b8,
# SCL to b9 (in the order of the pins, as published).
LCD_LYING = POSES['lcd_lying']
LCD_STANDING = POSES['lcd_standing_out']                            # upright, 15 mm short of F9's notches (the CAD's)
g.carry([LCD], by=F3, pose=LCD_LYING, appear=False)
for colour, *_ in LCD_WIRES:
    g.wire(f'lcd {colour}', COLOURS[colour], WIRE_R, name='Breadboard Wire (M-F)')
F_OFF = [0.0, 0.0, 15.0]                                            # a female cap held off its pin, before it goes on (the LCD's own frame)


def fem_centre(cap):
    return np.asarray(CAPS[cap]['box'], float).mean(0)


LCD_Z = 1250.0                                                      # the LCD ribbon's middle (in front of the base, at the buzzer's end)


def lcd_ribbon(pitch):
    """Each LCD wire lying on the table in front of the base: {colour: (male cap's pose, female cap's pose relative to the lying LCD,
    the straight route)}. The male end towards +z, its pin pointing +z; the female end towards -z, its open end -z (as on its pin)."""
    out = {}
    for k, (colour, male, _, fem, *_ ) in enumerate(LCD_WIRES):
        x = FRONT_X + k * pitch
        pm = np.array([x, TABLE_Y + 0.875, LCD_Z + RIBBON_MM / 2])
        pf = np.array([x, TABLE_Y + 0.875, LCD_Z - RIBBON_MM / 2])
        m = lying(male, pm, [0, 0, 1])
        f_world = tidy(pf - fem_centre(fem))
        f_rel = tidy(relative_pose(LCD_LYING, f_world, fem_centre(fem).round(2)))
        f_world = compose(LCD_LYING, f_rel, fem_centre(fem).round(2))                  # (where that puts it, as the generator composes it)
        out[colour] = (m, f_rel, W.route(W.resample(np.linspace(pf, pm, 12), 1.0), a=fem, b=male, a_at=f_world, b_at=m, stretch=True))
    return out


joined, apart = lcd_ribbon(RIBBON_PITCH), lcd_ribbon(SPLIT_PITCH)
# (listed by hand, pictured straight with its male cap at one end and its female cap at the other, as it lies before it goes in)
_m, _f = LCD_WIRES[0][1], LCD_WIRES[0][3]
_line = np.asarray(joined['purple'][2]['pts'], float)
g.list_part('Breadboard Wire (M-F)', [_m, _f], 4, after='Breadboard Wire (M-M)')
g.part_picture('Breadboard Wire (M-F)', poses={_m: joined['purple'][0], _f: joined['purple'][2]['a_ref']},
               wires=[dict(colour='jumper_purple', radius=WIRE_R, pts=np.linspace(_line[0], _line[-1], 40))])
for colour, male, _, fem, *_ in LCD_WIRES:
    g.carry([male], by=BREADBOARD, pose=joined[colour][0], appear=False)
    g.carry([fem], by=LCD, pose=joined[colour][1], appear=False)
_mid = np.array([FRONT_X + 1.5 * RIBBON_PITCH, TABLE_Y + 1.0, LCD_Z])
g.place('Lay the LCD screen face down beside the base. Then peel four wires off the ribbon of male-female wires and lay them side by side.',
        appear=[LCD] + LCD_MALE + LCD_FEMALE, lines=False, labels={LCD: 'LCD Screen'}, eye=[dict(anchor=_mid.round(2).tolist())],
        wires={f'lcd {c}': joined[c][2] for c, *_ in LCD_WIRES}, wires_done={f'lcd {c}': apart[c][2] for c, *_ in LCD_WIRES},
        ride={**{m: apart[c][0] for c, m, *_ in LCD_WIRES}, **{f: apart[c][1] for c, _, _, f, *_ in LCD_WIRES}},
        frame=([700.0, 905.0, 1330.0], 110.0), view_dir=[0.62, 0.62, 0.48])
LCD_CAMERA = dict(view_dir=[0.62, 0.62, 0.48], frame=([700.0, 905.0, 1330.0], 110.0))


def lcd_route(key, fem, male, lcd_pose):
    line = cad_line(key, male)[::-1]                                # (from the female end, on the LCD, to the male end)
    return W.route(line, a=fem, b=male, a_at=lcd_pose, stretch=True)


for k, (colour, male, label, fem, pin, lying_key, _, _) in enumerate(LCD_WIRES):
    done = lcd_route(lying_key, fem, male, LCD_LYING)
    x = FRONT_X + k * SPLIT_PITCH
    g.place(f"Connect the {colour} wire from {pin} on the LCD screen to {label}.", move=[male], paths={male: [apart[colour][0], UP, ZERO]},
            ride={fem: [F_OFF, ZERO]}, ride_beats=True, lines=False, labels=[dict(text=pin, anchor=fem_centre(fem).round(2).tolist(), id=LCD), hole_label(label, male)],
            eye=[dict(anchor=[x, TABLE_Y + 1.0, LCD_Z])], wires_done={f'lcd {colour}': [done, done]}, **LCD_CAMERA)
# ================================================================ THE LCD SCREEN (end)

# ================================================================ THE USB CABLE (begin)
# The right-angle Mini-B end goes into the Nano Board's socket (hover and plug, as decided for the MRA: section 13). The cable leaves
# it towards the back and lies straight out behind the case, on the table, along the line on which F2's slit comes in (Step 55: F2 is
# brought in from behind, swung out, its tabs are hooked into F5 and it swings shut, its slit, open at the bottom, sliding along the
# cable); from then on it passes through the slit, and bends round to the A end. (The CAD's cable crosses F2's plane at z 1339.4,
# y 890.8, through F3's edge, and lays the A end along the case, 9 mm under the table; here the cable passes 9 mm higher, in the
# slit's open part, clear of F2, F3 and the breadboard.)
g.wire('usb cable', 'cable_black', 1.75, name='USB Cable')
_usb = cad_line('NAUO123')
USB_EXIT, USB_EXIT_DIR = _usb[0], unit(_usb[3] - _usb[0])
NOTCH = np.array([643.13, 899.6, 1339.4])                           # where the cable passes F2 seated: the middle of its slit (5 mm wide, open to y 901)
USB_PRE = np.array([651.5, 900.8, 1343.0])                          # (on the way: past the breadboard's corner)
SWING = 20.0                                                        # F2 swung out at its far end (published: about 21 degrees)
HINGE = [641.63, 919.5, 1366.07]                                    # F2's outer face where it meets F5's inside: it swings about the upright there
swung = lambda t=(0.0, 0.0, 0.0): turned([0, 1, 0], SWING, HINGE, list(t))
_u = np.array([np.sin(np.radians(SWING)), 0.0, np.cos(np.radians(SWING))])   # F2's length, swung out
F2_HOOK = (-_u * 14.0).round(2).tolist()                            # swung out, 14 mm short of F5: its tabs just out of F5's slots
F2_OFF = np.add(F2_HOOK, [-40.0, 0.0, 0.0]).round(2).tolist()       # ... and 40 mm further out behind the case (it comes in along x)
# (published: F2 comes in about 80 mm, diagonally from behind and from F6's end, the case lying on its front; here the case stays
# upright, seen from behind, as the player turns a model only upside down, and F2 comes in straight along x and then 14 mm along
# itself, so that its slit, open at the bottom, slides along the cable lying straight out behind the case)
SLIT_IN = posed_line(swung(F2_HOOK), [NOTCH])[0]                    # where the slit is as F2 comes in (along x, at this z)
A_CABLE_END = _usb[-1]                                              # the A end's cable end, as the CAD has it (its plug towards +z)
A_TARGET = np.array([575.0, TABLE_Y + 4.3, SLIT_IN[2]])             # ... and where it lies: out behind the case, in line with the slit coming in
A_ON_TABLE = tidy(turned([0, 1, 0], -90.0, A_CABLE_END.round(2).tolist(), (A_TARGET - A_CABLE_END.round(2)).round(2).tolist()))
g.rest_at([USB_A], A_ON_TABLE)
USB_OUT = 18.0                                                      # (the plug's hover, clear of the buzzer lying behind it)


def usb_cable(out=0.0, f2=None):
    """The cable from the Nano Board's socket (its plug `out` mm short of it) through F2's slit with F2 at pose f2 (relative to its seat),
    or, for f2 None, along the line on which the slit comes in, and on to the A end on the table."""
    a_at = [0.0, 0.0, out] if out else None
    start = USB_EXIT + [0.0, 0.0, out]
    if f2 is None:
        slit, across = SLIT_IN, np.array([-1.0, 0.0, 0.0])
    else:
        slit = posed_line(f2, [NOTCH])[0]
        across = unit(posed_line(f2, [NOTCH + [-1.0, 0.0, 0.0]])[0] - slit)     # (straight through F2)
    inside = W.smooth([start, USB_PRE + [0.0, 0.0, out / 2], slit - across * 6.0, slit], start_dir=USB_EXIT_DIR, end_dir=across, spacing=0.5)
    outside = W.smooth([slit, slit + across * 6.0, A_TARGET + [12.0, 0.0, 0.0]], start_dir=across, end_dir=[-1, 0, 0], spacing=0.5)
    line = W.resample(W.join(inside, outside, W.straight(outside[-1], [-1, 0, 0], 12.0)), 1.0)   # (down to the table, and straight into the A end)
    to_slit = float(np.linalg.norm(np.diff(line[:int(np.argmin(np.linalg.norm(line - slit, axis=1))) + 1], axis=0), axis=1).sum())
    return {'usb cable': W.route(line, a=USB_B, b=USB_A, a_at=a_at, b_at=A_ON_TABLE, tail_from=round(to_slit, 1))}   # (the bit in the slit stays in it as the cable changes shape)


g.place("Plug the USB cable's small end into the Nano Board's USB socket, the cable towards the back.", move=[USB_B], appear=[USB_A], path=[[0.0, 0.0, USB_OUT], ZERO],
        lines_at=[[[676.34, 903.89, 1337.64], [676.34, 903.89, 1345.07]]], labels={USB_B: 'USB Cable'},
        wires=usb_cable(USB_OUT), wires_done=usb_cable(), view_dir=[-0.62, 0.6, 0.5], frame=([628.0, 900.0, 1350.0], 70.0))   # (from behind: the LCD lies in front; the A end in frame)
# ================================================================ THE USB CABLE (end)

# ================================================================ THE CASE (begin)
# The two F7s go into F3 by the buzzer; they are spread apart, the buzzer goes in between them (its ears into their slots), and they
# are let go. Then F9 (which holds the LCD's end), F1 is carried round to the other end, F4 goes on top, F8, the LCD into F9's notches,
# and F1 on the front. (The F7s ride on F3, so that they can be spread and let go.)
F7_HOVER = 80.0                                                     # (published: 80.3 mm)
g.carry([F7A, F7B], by=F3, pose=[0.0, F7_HOVER, 0.0], appear=False)
F7_TAB = {F7A: [658.83, 881.23, 1228.4], F7B: [691.68, 881.23, 1238.0]}
CASE_CAMERA = dict(view_dir=[0.55, 0.55, -0.63], frame=([690.0, 915.0, 1270.0], 110.0))
g.place('Push the two F7s down into the slots in F3 by the end of the breadboard, their engraved sides facing out.', appear=[F7A, F7B], ride={F7A: ZERO, F7B: ZERO},
        lines_at=[[np.add(t, [0.0, F7_HOVER, 0.0]).tolist(), [t[0], 887.61, t[2]]] for t in F7_TAB.values()], labels={F7A: '2x F7'}, **CASE_CAMERA)
SPREAD = 15.0                                                       # (published: about 15 degrees)
TILT_A = turned([0, 0, 1], SPREAD, [657.33, 887.61, 1233.2], [0.0, 2.6, 0.0])
TILT_B = turned([0, 0, 1], -SPREAD, [693.18, 887.61, 1233.2], [0.0, 2.6, 0.0])
g.place('Spread the tops of the two F7s apart.', ride={F7A: TILT_A, F7B: TILT_B}, lines=False,
        arrows=[dict(tail=[655.0, 945.0, 1233.2], head=[628.0, 945.0, 1233.2], normal=[0, 1, 0], part=F3),
                dict(tail=[695.5, 945.0, 1233.2], head=[722.5, 945.0, 1233.2], normal=[0, 1, 0], part=F3)], **CASE_CAMERA)
BUZZER_UP = [0.0, 45.0, 0.0]
g.place('Lower the buzzer in between the two F7s, its ears into their slots.', move=[BUZZER], path=[BUZZER_LYING, via(compose([0.0, 60.0, 0.0], BUZZER_LYING)), BUZZER_UP, ZERO],
        lines=False, eye=[BUZZER],
        wires_done={f'buzzer {c}': [W.route(cad_line(k2, cap)[::-1], a=BUZZER, b=cap, stretch=True)] * 2 for c, cap, _, _, _, k2 in BUZZER_LEADS}, **CASE_CAMERA)
g.place('Let go of the two F7s, so that they close on the buzzer.', ride={F7A: ZERO, F7B: ZERO}, lines=False, eye=[F7A, F7B], **CASE_CAMERA)
g.place('Push F9 down into the slots in F3 beside the end of the breadboard, its engraved side towards that end.', move=[F9], labels={F9: 'F9'},
        review='The published guide hooks F9 in tilted and then stands it up (Steps 45, 46); in the CAD it goes straight down into its '
               'slots, so it does here. Does the real part need the hook-and-swing?', **CASE_CAMERA)

# F1 is carried round to the far end (the buzzer's) and laid face up there, its potentiometer's leads re-routed (the CAD's).
F1_MID = [70.0, 40.0, -100.0]                                      # (on the way round: upright, in front of the box)
POT_OTHER = {c: W.route(cad_line(k, cap)[::-1], a=POT, b=cap, a_at=FLAT_OTHER_END, stretch=True) for c, cap, _, _, k in POT_LEADS}
g.place('Move F1 round to the other end of the base and lay it face up there.', ride={F1: [compose(FRONT_OUT, F1_MID), FLAT_OTHER_END], POT: [compose(FRONT_OUT, F1_MID), FLAT_OTHER_END]}, ride_beats=True, lines=False, eye=[F1],
        wires_done={f'pot {c}': [POT_OTHER[c], POT_OTHER[c]] for c, *_ in POT_LEADS}, view_dir=[0.62, 0.62, 0.48], frame=([700.0, 915.0, 1300.0], 200.0))

# F4: lifted over the frame (the switch's leads re-routed, the CAD's), then lowered onto the tabs of the F7s and F9.
SW_OVER = {c: W.route(cad_line(k, cap)[::-1], a=SWITCH, b=cap, a_at=HOVER_F4, stretch=True) for (c, cap, _, _), k in zip(SWITCH_LEADS, ('NAUO149', 'NAUO148', 'NAUO147'))}
g.place('Lift F4, with the switch, over the frame.', ride={F4: HOVER_F4}, lines=False, eye=[F4],
        wires_done={f'switch {c}': [SW_OVER[c], SW_OVER[c]] for c, *_ in SWITCH_LEADS}, **CASE_CAMERA)
F4_SLOTS = [[693.64, 1355.78], [697.62, 1355.78], [658.83, 1238.01], [691.68, 1228.36]]   # (over the tabs of F9 (x2) and the F7s, as published)
# Each lead's way from the seated switch down to its hole, clear of the others and of the jumpers (found by a path search through
# the closed case, kept as control points).
SW_SEATED_WAY = {'red': [[669.0, 921.7, 1263.0], [666.9, 920.0, 1266.0], [665.1, 918.5, 1269.2], [663.2, 917.3, 1272.8]],
                'tan': [[685.0, 921.7, 1262.1], [687.9, 919.6, 1264.4], [690.5, 917.8, 1266.2], [693.7, 916.1, 1268.1]],
                'black': [[682.1, 919.2, 1257.5], [679.2, 917.0, 1259.1], [676.3, 915.7, 1261.5], [673.4, 915.1, 1263.6], [669.8, 914.8, 1265.6], [666.3, 914.5, 1267.3]]}
SW_SEATED = {c: W.route(into_hole(cap, exit_, [0, -1, 0], SW_SEATED_WAY[c]), a=SWITCH, b=cap, stretch=True) for c, cap, _, exit_ in SWITCH_LEADS}
g.place('Lower F4 onto the tabs of the F7s and F9.', move=[F4], path=[HOVER_F4, ZERO], lines_at=[[[x, 951.46, z], [x, 957.84, z]] for x, z in F4_SLOTS],
        wires_done={f'switch {c}': SW_SEATED[c] for c in SW_SEATED}, **CASE_CAMERA)
g.place('Slide F8 into the slots in F4 and F3 from the front.', move=[F8], direction=[1, 0, 0], hover=94, labels={F8: 'F8'}, **CASE_CAMERA)   # (published: 94.2 mm)

# The LCD: stood up in front of the box and brought in, 15 mm short of F9 (the CAD's), then slid into F9's notches.
LCD_STAND_ROUTE = {c: lcd_route(k, f, m, LCD_STANDING) for c, m, _, f, _, _, k, _ in LCD_WIRES}
LCD_SEAT_ROUTE = {c: lcd_route(k, f, m, None) for c, m, _, f, _, _, _, k in LCD_WIRES}
g.place('Stand the LCD screen up, face to the front, and bring it into the front of the case.', ride={LCD: [np.add(LCD_STANDING, [40.0, 0.0, 0.0]).tolist(), LCD_STANDING]}, ride_beats=True,
        lines=False, eye=[LCD], wires_done={f'lcd {c}': [LCD_STAND_ROUTE[c]] * 2 for c in LCD_STAND_ROUTE}, view_dir=[0.62, 0.62, 0.48], frame=([705.0, 915.0, 1320.0], 110.0))
g.place("Slide the LCD screen along until its board goes into the notches in F9 and F8.", move=[LCD], path=[LCD_STANDING, ZERO], wires_done={f'lcd {c}': LCD_SEAT_ROUTE[c] for c in LCD_SEAT_ROUTE},
        view_dir=[0.62, 0.62, 0.48], frame=([705.0, 915.0, 1320.0], 110.0))

# F1: stood up in front of the box (the CAD's), then pushed onto the tabs of F4 and F3.
# Each lead's way through the closed case to its hole, seated (found by a path search, kept as control points): from the pins down
# under the potentiometer, between the buzzer and F8, then along the rails (black behind the LCD's board, red over the (+) rail, tan
# over the Nano Board) and down into its hole. Stood up in front of the case, each lead runs in from the front to the same way.
F1_IN_WAY = {'black': [[712.9, 903.1, 1249.3], [708.7, 907.3, 1254.3], [704.2, 911.8, 1258.9], [700.8, 916.0, 1265.0], [701.3, 917.4, 1272.8], [703.6, 916.2, 1280.2], [704.8, 916.0, 1288.1], [705.0, 916.0, 1296.0], [705.0, 916.0, 1304.0], [704.9, 916.0, 1312.0], [703.7, 916.0, 1319.9], [701.3, 915.4, 1327.6]],
             'red': [[713.2, 900.7, 1240.1], [709.3, 902.4, 1246.8], [704.7, 903.2, 1253.7], [699.6, 905.1, 1259.4], [695.1, 908.9, 1264.4], [692.4, 911.6, 1271.4], [692.0, 912.0, 1279.6], [692.0, 912.0, 1287.6], [692.1, 912.0, 1295.5], [693.3, 912.1, 1303.5], [694.7, 913.1, 1311.0], [695.0, 914.0, 1319.0], [695.3, 914.5, 1326.9]],
             'tan': [[710.7, 905.9, 1242.4], [705.3, 906.9, 1247.7], [699.4, 907.4, 1253.6], [694.2, 907.9, 1259.2], [690.4, 908.0, 1266.1], [689.2, 908.0, 1274.0], [689.0, 908.0, 1281.9], [689.0, 908.0, 1290.4], [688.6, 908.0, 1298.2], [686.5, 908.0, 1305.8], [683.7, 908.0, 1313.1], [682.6, 908.7, 1321.2], [685.0, 911.7, 1328.2]]}
F1_FRONT_WAY = {'black': [[781.2, 900.0, 1240.0], [771.3, 900.0, 1240.0], [761.5, 900.3, 1240.3], [753.2, 904.0, 1244.0], [746.5, 909.2, 1249.2], [736.8, 911.0, 1251.0], [726.9, 911.0, 1251.2], [717.3, 911.0, 1253.2], [708.0, 911.2, 1257.1]],
                'red': [[781.7, 900.0, 1233.0], [771.7, 900.0, 1233.0], [761.7, 900.0, 1233.0], [751.5, 900.2, 1233.6], [742.5, 902.1, 1236.7], [733.6, 903.0, 1241.0], [724.3, 903.0, 1245.2], [715.1, 903.0, 1249.4]],
                'tan': [[781.6, 903.1, 1237.0], [771.5, 904.0, 1237.0], [761.5, 904.0, 1237.0], [751.8, 904.6, 1237.1], [741.9, 906.5, 1237.7], [731.8, 907.0, 1238.2], [722.2, 907.0, 1240.3], [713.0, 907.0, 1244.4]]}
F1_UP_WAY = {c: F1_FRONT_WAY[c] + F1_IN_WAY[c][1 if c == 'tan' else 2:] for c in F1_IN_WAY}
POT_UP = {c: pot_plugged(c, cap, e, FRONT_OUT, F1_UP_WAY[c]) for c, cap, _, e, _ in POT_LEADS}
POT_IN = {c: pot_plugged(c, cap, e, None, F1_IN_WAY[c]) for c, cap, _, e, _ in POT_LEADS}
g.place('Stand F1 up in front of the case, the knob on the outside.', ride={F1: FRONT_OUT, POT: FRONT_OUT}, lines=False, eye=[F1],
        wires_done={f'pot {c}': [POT_UP[c]] * 1 for c in POT_UP}, view_dir=[0.62, 0.55, -0.56], frame=([720.0, 915.0, 1270.0], 120.0))
g.place('Push F1 onto the tabs of F4 and F3.', move=[F1, POT], path=[FRONT_OUT, ZERO], wires_done={f'pot {c}': POT_IN[c] for c in POT_IN},
        view_dir=[0.62, 0.55, -0.56], frame=([720.0, 915.0, 1270.0], 120.0))

# The ends and the back, as published (Steps 55 - 57): F5 onto the end by the breadboard; F2's hooks into F5's slots with F2 swung out,
# then F2 swung shut over the tabs of F3 and F4, its slit sliding along the USB cable; F6 onto the other end, which locks them all.
# Lead lines from each slot (on the moving panel) to the tab that goes into it.
END_CAMERA = dict(view_dir=[0.82, 0.4, 0.42], frame=([683.0, 919.0, 1320.0], 115.0))   # (low, from the front, as published: from further round F5 hides its lines)
F5_TABS = [[722.33, 949.8, 1372.45], [722.33, 888.4, 1372.45], [663.68, 886.11, 1369.24], [701.78, 886.11, 1369.24]]   # F1's two hooks, F3's two tabs
g.place("Push F5 onto the end of the case by the breadboard: the tabs of F1, F3 and F4 go into its slots. Its engraved side faces out.", move=[F5],
        direction=[0, 0, 1], hover=56, lines_at=[[[x, y, 1366.07], [x, y, z]] for x, y, z in F5_TABS], labels={F5: 'F5'}, **END_CAMERA)   # (published: 56.0 mm)
F2_HOOKS = [[643.13, 949.8, 1372.45], [643.13, 888.4, 1372.45]]    # the hooks at F2's end by F5
g.place("Turn the case so its back faces you. Hook the tabs at the slit end of F2 into the slots in F5, its engraved side facing out and "
        "its other end swung out, then swing F2 shut onto the tabs of F3 and F4.", move=[F2], path=[swung(F2_OFF), swung(F2_HOOK), swung(), ZERO],
        lines_at=[[h, [h[0], h[1], 1366.07]] for h in F2_HOOKS], labels={F2: 'F2'}, eye=[dict(anchor=[643.13, 889.0, 1339.4], id=F2)],   # (the cable in the slit)
        inset=dict(target=NOTCH.round(2).tolist(), dir=[-0.9, 0.35, -0.25], radius=14.0, mark=4.0, alt='The USB cable in the slit at the bottom of F2'),
        caution='The USB cable must sit in the slit at the bottom of F2.', wires_done={'usb cable': [usb_cable()['usb cable'], usb_cable(f2=swung())['usb cable'],
                                                                                        usb_cable(f2=ZERO)['usb cable']]},   # (the cable follows the slit)
        view_dir=[-0.7, 0.5, -0.5], frame=([640.0, 915.0, 1290.0], 125.0))   # (F2 swung out, whole, in frame)
F6_TABS = [[722.33, 949.8, 1207.29], [722.33, 888.4, 1207.29], [643.13, 949.8, 1207.29], [643.13, 888.4, 1207.29]]   # F1's and F2's hooks
g.place("Push F6 onto the other end of the case: the tabs of F1, F2, F3 and F4 go into its slots. Its engraved side faces out.", move=[F6],
        direction=[0, 0, -1], hover=67.5, lines_at=[[[x, y, 1213.67], [x, y, z]] for x, y, z in F6_TABS], labels={F6: 'F6'},
        view_dir=[0.5, 0.55, -0.67], frame=([683.0, 919.0, 1250.0], 110.0))   # (published: 67.5 mm)
# ================================================================ THE CASE (end)

g.build()
