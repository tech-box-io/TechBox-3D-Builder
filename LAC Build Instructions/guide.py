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
    ('white', ('NAUO28', 'a14'), ('NAUO15', '(-) blue'), None),       # (a low arch, under the purple and blue: JUMPER_ARCH)
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

NAMES = {BREADBOARD: 'Breadboard', F3: 'F3', RTC: 'Real Time Clock', COIN: 'Real Time Clock', RES1: '12 kΩ Resistor', RES2: '12 kΩ Resistor',
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
     lambda n: n in ('Breadboard', 'Nano Board', '12 kΩ Resistor', 'Real Time Clock', 'Rocker Switch', 'Potentiometer', 'Alarm Buzzer', 'LCD Screen', 'USB Cable')),
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


PART_VIEWS = {'LCD Screen': {'dir': [0.8, 0.45, 0.4]},              # (the parts list pictures the LCD from the front, its screen showing,
              'Potentiometer': {'dir': [0.5417, 0.6428, -0.5417]}}  # and the potentiometer from its knob's side: Lee, 20 Oct 2026)
g = Guide(HERE, title='LCD Alarm Clock (LAC)', part='Full Build', names=NAMES, part_of=PART_OF, unlisted=UNLISTED, hover_names=HOVER_NAMES, part_views=PART_VIEWS,
          source='lac-guide.glb', codes=CODES, hero_azimuth=135,     # the finished clock from the front (F1: the screen and the knob), the knob's end
          parts_list=parts_list, copyright_line='© TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')

paths = W.load(HERE / 'wire-paths.json')
HOLES, CAPS, LINES = paths['holes'], paths['caps'], paths['lines']
# The LCD's GND and VCC wires go into the rails at k = +2 and +4 (z 1290.00, 1295.08), not where the CAD has them (k = -2, z 1279.84):
# there the black and green jumpers lean right over the holes (the green 1.24 mm from the GND hole's axis at y 925, the black 0.55 mm
# from the VCC hole's), and neither wire could go in without passing through them (Lee, 21 Oct 2026, Steps 36 - 37: "clips through the
# existing green and black breadboard wires"; docs/research/lac/round2/wire_clipping.md). Any hole of a rail is the same connection.
# materials.json adjust_mm moves the caps the same.
LCD_RAIL_SHIFT = {'NAUO82': 10.16, 'NAUO84': 15.23}
for _cap, _dz in LCD_RAIL_SHIFT.items():
    for _k in ('top', 'wire_at', 'tip'):
        if _k in CAPS[_cap]:
            CAPS[_cap][_k] = np.add(CAPS[_cap][_k], [0.0, 0.0, _dz]).tolist()
    CAPS[_cap]['box'] = np.add(CAPS[_cap]['box'], [0.0, 0.0, _dz]).tolist()
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


def screen_x(p, view_dir):
    """How far right a point is in a view from view_dir (world up)."""
    right = unit(np.cross(-unit(view_dir), [0.0, 1.0, 0.0]))
    return float(np.dot(np.asarray(p, float), right))


NEAR_REACH = 0.05     # how far a label sits from its own spot, as a share of the window's width (player.js layoutCallouts NEAR):
                      # 100 px in Lee's 2000 px window, 50 px in the LMS's 1000 px frame


def near(side, reach=NEAR_REACH):
    """A label's (or an eye's) place beside its own spot: 'near-left' / 'near-right' level with it, 'up-left' ... 'down-right' diagonally,
    'near-above' / 'near-below' straight over or under it; `reach` a share of the window's width. Not a side of the model ('left',
    'right', 'top'): the player puts those outside the box round every part and wire on screen, which in this kit's close frames (F3, the
    breadboard and the long leads reach past the window) is the window's edge (Lee's second round, 21 Oct 2026: "flung to the edges of
    the screen"). The player does not keep near labels apart: each step's are chosen clear of each other (round2/labels.md)."""
    return dict(side=side, reach=reach)


def sides(labels, view_dir, places=None):
    """Labels on spots side by side: the left one beside its spot to the left, the right one beside its spot to the right, level with
    them, so that neither sits on the parts between them nor do their leaders cross (Lee, 20 and 21 Oct 2026); or at `places`
    ([(side, reach), ...] in the labels' order) where a step needs others."""
    out = [dict(l) for l in labels]
    if places:
        return [dict(l, **near(*p)) for l, p in zip(out, places)]
    order = sorted(range(len(out)), key=lambda k: screen_x(out[k]['anchor'], view_dir))
    out[order[0]].update(near('near-left'))
    out[order[-1]].update(near('near-right'))
    return out


def away_from(label, part_point, view_dir):
    """A label beside its spot, on the side away from a part (the switch, the potentiometer) that its wire comes from."""
    return dict(label, **near('near-right' if screen_x(label['anchor'], view_dir) > screen_x(part_point, view_dir) else 'near-left'))


def wire_at(cap):
    """Where a male cap standing in the breadboard holds its wire (the top of its pin, inside the housing; seated)."""
    return np.asarray(CAPS[cap]['wire_at'], float)


def cap_mid(cap):
    """The middle of a Dupont cap's housing (seated). A pose of the cap is written about it: the player turns a part about its pose's
    `at` between two poses (player.js mixPose), and compose() writes the origin, 1.7 m away, unless it is given a pivot (Lee, 20 Oct
    2026: the buzzer's caps swung off the screen in Steps 33 - 34)."""
    return np.asarray(CAPS[cap]['box'], float).mean(0).round(2)


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
BENCH_DIAG = [0.5792, 0.5736, -0.5792]                              # (the three-quarter view BENCH_LOOK gives, for a frame of our own)
_tail = [float(_phi[0]) - 4.0, float(_plo[1]) - 1.0, float(_plo[2]) + 4.0]   # (the arrow at the backing's front corner, out from under the breadboard)
g.place('Begin with the breadboard. Peel the protective backing off its underside.', appear=[BREADBOARD], ride={PAPER: [0.0, -50.0, 0.0]}, lines=False,
        arrows=[dict(tail=_tail, head=[_tail[0], _tail[1] - 26.0, _tail[2]], normal=[0.71, 0.0, -0.71], part=PAPER)],
        labels=[dict(id=BREADBOARD, text='Breadboard', anchor=[663.9, 897.1, 1302.6], **near('near-right'))],   # (beside it, clear of the arrow)
        view_dir=BENCH_DIAG, frame=([674.5, 914.3, 1305.8], 58.4))   # (Step 1's camera and the label's spot as they were before the
                                                                     # breadboard's tabs moved: Lee, 21 Oct 2026)
g.put_away([PAPER])
# (the breadboard's body without its joining tabs, which are on the a side and the column 30 end as on the real board: Lee, 21 Oct
# 2026; the corner lines 2 mm in from the body's own corners)
_lo, _hi = np.array([647.80, 887.61, 1264.41]), np.array([702.55, 897.13, 1346.09])
BB_CORNERS = [[x, float(_lo[1]), z] for x in (float(_lo[0]) + 2.0, float(_hi[0]) - 2.0) for z in (float(_lo[2]) + 2.0, float(_hi[2]) - 2.0)]
g.place('Stick the breadboard down onto F3, its red and blue rails along the same edge of F3 as its engraved code.', move=[BREADBOARD], show=[F3],
        path=[[0.0, BB_HOVER, 0.0], ZERO], lines_at=BB_CORNERS, labels=[dict(id=F3, text='F3', **near('down-left', 0.035))], look_from=BENCH_LOOK)
g.place('Press the Nano Board into the breadboard: its pins go in rows c and g, columns 1 to 15, with its USB socket at column 1.', move=[NANO],
        direction=[0, 1, 0], hover=40,
        labels=[dict(id=NANO, text='Nano Board', **near('down-left')), dict(text='c15', anchor=HOLES['c15'], id=BREADBOARD, **near('near-right')),
                dict(text='g1', anchor=HOLES['g1'], id=BREADBOARD, **near('near-left'))],   # (each hole's label to its own side, its leader across its lead line)
        lines_at=[[[HOLES[h][0], 891.6, HOLES[h][2]], HOLES[h]] for h in ('c15', 'g1')],   # (each corner pin's tip, to its hole)
        view_dir=BENCH_DIAG, frame=([676.5, 916.0, 1324.3], 50.0))   # (close on the Nano and its two corner holes, as the LSM's Step 3)

# The resistors: their legs bent down first (Step 4: shown straight, as bought, then bent, as the LSM's: Lee, 20 Oct 2026), then each
# pressed in from the (-) blue rail to row h. The legs are wires (the CAD's own legs, straight and bent, leave the model:
# materials.json), so that they can bend. Measured from the CAD: the body x 677.03 - 688.03 on an axis at y 901.15 (RES2: 901.27,
# 5.15 mm further to -z); each bent leg runs on from the body's end to over its hole and turns 8.0 mm straight down, its tip 3.96 mm
# under the holes' tops (docs/research/lac/round1/lsm_techniques.md, section 1).
RES_HOVER = 37.0
LEG_R, LEG_RINGS, LEG_DROP = 0.315, 0.25, 8.0
RES_LEG_ENDS = {   # per leg: where it leaves the body (0.4 mm inside its end), and the point over its hole where it turns down
    RES1: [([687.63, 901.15, 1277.13], [699.20, 901.15, 1277.36]),     # to the (-) blue rail
           ([677.43, 901.15, 1276.38], [666.18, 901.15, 1276.20])],    # to h27
    RES2: [([687.63, 901.27, 1271.98], [699.20, 901.27, 1272.21]),
           ([677.44, 901.27, 1271.23], [666.18, 901.27, 1271.05])]}    # to h29


def legs(body, name):
    """Each leg of a resistor as a wire tied to its body: straight out, as bought, or bent through 30, 60 and 90 degrees at the point
    over its hole; every shape as long as the bent leg, so that the tip swings round rather than shrinking (as the LSM's)."""
    straight_, bent = {}, {}
    for k, (start, corner) in enumerate(RES_LEG_ENDS[body], 1):
        wid = f'{name} leg {k}'
        g.wire(wid, 'pin', LEG_R, name=NAMES[body])
        start, corner = np.array(start), np.array(corner)
        line = W.rounded([start, corner, corner - [0.0, LEG_DROP, 0.0]], radius=1.2, spacing=0.25)
        n, run = W.length(line), float(np.linalg.norm(corner - start))
        out = (corner - start) / run
        shapes = [W.route(W.rounded([start, corner, corner + (out * np.cos(t) + [0.0, -np.sin(t), 0.0]) * (n - run)], radius=1.2, spacing=0.25),
                          a=body, spacing=LEG_RINGS) for t in np.radians([30.0, 60.0])]
        bent[wid] = [*shapes, W.route(line, a=body, spacing=LEG_RINGS)]
        straight_[wid] = W.route(W.straight(start, out, n), a=body, spacing=LEG_RINGS)
    return straight_, bent


R1_STRAIGHT, R1_BENT = legs(RES1, 'res1')
R2_STRAIGHT, R2_BENT = legs(RES2, 'res2')
g.part_picture(NAMES[RES1], wires=[dict(colour='pin', radius=LEG_R, pts=r['pts']) for r in R1_STRAIGHT.values()])   # (pictured as bought)
g.rest_at([RES1], [0.0, RES_HOVER, 0.0])
RES_MID = np.array([682.53, 901.15, 1276.77])                       # (the body's middle)
g.in_hand = [RES1]                                                  # (shown on its own, as published: a view of the resistor alone)
g.place('Bend the legs of both 12 kΩ resistors (brown, red, black, red, brown) down at right angles, like this, so that they fit the breadboard.',
        appear=[RES1], lines=False, staged=True, wires=R1_STRAIGHT, wires_done=R1_BENT,
        labels=[dict(id=RES1, text='2x - 12 kΩ Resistor', anchor=[682.5, 903.5, 1276.8], side='up-left')],   # (on the body's top: the CAD's legs are not
        eye=[dict(id=RES1, anchor=[682.5, 901.2, 1274.3], side='down-right')],                               # drawn; label and eye clear of the legs)
        frame=((RES_MID + [0.0, RES_HOVER, 0.0]).round(1).tolist(), 24.0), look_from=BENCH_LOOK)   # (the straight legs span x 658.7 - 706.7)
g.in_hand = []

RES_LEGS = {RES1: [[699.2, 893.1, 1277.5], [666.0, 893.1, 1276.3]], RES2: [[699.1, 893.3, 1272.2], [666.0, 893.3, 1271.0]]}   # (each leg's tip: Lee, 20 Oct 2026)
for res, h in ((RES1, 'h27'), (RES2, 'h29')):
    g.place(f"Press {'a' if res == RES1 else 'the other'} 12 kΩ resistor into the breadboard, from the (-) blue rail to {h}.", move=[res],
            **(dict(path=[[0.0, RES_HOVER, 0.0], ZERO]) if res == RES1 else dict(direction=[0, 1, 0], hover=RES_HOVER)),
            labels=[dict(text='(-) blue', anchor=[paths['breadboard']['rails']['- blue'], BB_TOP, HOLES[h][2] + 1.1], id=BREADBOARD, **near('near-left')),
                    dict(text=h, anchor=HOLES[h], id=BREADBOARD, **near('up-right'))],   # (each to its own side, clear of the resistor)
            lines_at=RES_LEGS[res], wires={k: v[-1] for k, v in R2_BENT.items()} if res == RES2 else None,
            view_dir=BENCH_DIAG, frame=([682.7, 918.0, HOLES[h][2] + 0.6], 32.0))   # (close on the two holes and the resistor over them)

# The real-time clock module (with its coin cell), its six pins along row j, j19 to j24.
g.place('Press the real time clock module into row j, its pins from j19 to j24, with its coin cell facing the back.', move=[RTC, COIN], direction=[0, 1, 0], hover=34,
        labels=[dict(id=RTC, text='Real Time Clock', **near('near-left')), dict(text='j24', anchor=HOLES['j24'], id=BREADBOARD, **near('near-right')),
                dict(text='j19', anchor=HOLES['j19'], id=BREADBOARD, **near('near-left'))],
        lines_at=[[[HOLES[h][0], 893.69, HOLES[h][2]], HOLES[h]] for h in ('j24', 'j19')],
        view_dir=BENCH_DIAG, frame=([660.0, 934.0, 1290.0], 52.0))   # (close on row j and the module over it)
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


# The jumpers drawn as a low arch instead of the CAD's shape: the dark red (it clears the jumpers and the leads by the clock module) and
# the white, which goes in under the purple and blue where they run along row a over a12 and a14 (Lee, 21 Oct 2026: the white and the
# dark red went in through them; docs/research/lac/round2/wire_clipping.md): (height over the higher end, its top moved).
JUMPER_ARCH = {'dark_red': (8.0, (0.0, 0.0, 3.0)),                  # (over the (+) rail by the clock module, bowed to +z)
               'white': (8.0, (0.0, 0.0, -3.0))}                     # (under the purple and blue, bowed to -z, clear of the dark red's hole)


def jumper_done(colour, ca, cb, key):
    """A jumper's route plugged in: the CAD's, or a low arch (JUMPER_ARCH) for a wire that has to go in under others."""
    if colour in JUMPER_ARCH:
        height, shift = JUMPER_ARCH[colour]
        line = arch(wire_at(ca), wire_at(cb), height, shift=shift)
    else:
        line = cad_line(key, ca)
    return W.route(line, a=ca, b=cb, stretch=True)


# Each cap's way in for a wire that goes in under wires already in (the CAD's purple and blue run along row a, over a12 and a14): slid in
# 14 mm from the front, 5 mm up, then pushed down. The dark red's (+) red cap comes along the rail from +z instead: the white's (-) blue
# cap stands right in front of it. (Held 18 mm straight over their holes, they went down through the purple and blue.)
FRONT_LOW, LOW = [14.0, 5.0, 0.0], [0.0, 5.0, 0.0]
JUMPER_WAYS = {'white': {'NAUO28': [FRONT_LOW, LOW, ZERO], 'NAUO15': [FRONT_LOW, LOW, ZERO]},
               'dark_red': {'NAUO30': [FRONT_LOW, LOW, ZERO], 'NAUO31': [[0.0, 5.0, 14.0], LOW, ZERO]}}


def frame_on(points, view_dir, margin=8.0, least=26.0):
    """A camera from view_dir framing these points (assembly mm) closely: the middle of their box, the radius to the farthest plus a margin."""
    pts = np.asarray(points, float)
    mid = (pts.min(0) + pts.max(0)) / 2
    return dict(view_dir=view_dir, frame=(mid.round(1).tolist(), round(max(least, float(np.linalg.norm(pts - mid, axis=1).max()) + margin), 1)))


def held_over(caps):
    """Where the holes of these caps are, and the caps held over them (for framing)."""
    p = np.array([[wire_at(c)[0], BB_TOP, wire_at(c)[2]] for c in caps])
    return np.vstack([p, p + [0.0, HOVER_MM + 12.0, 0.0]])


def corners(part, pose=None):
    """The corners of a part's box, where it is at `pose` (relative to its seat)."""
    lo, hi = g.model.inst[part].bounds
    return posed_line(pose, np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]))


def hole_camera(caps, view_dir, margin=8.0, least=26.0):
    """A camera close on the holes a step's caps go into and on the caps held over them (as the LSM framed its breadboard steps: Lee,
    20 Oct 2026, "zoom in so that we can better see the target slots")."""
    return frame_on(held_over(caps), view_dir, margin, least)


def jumper_run(jumpers, z_mid, ribbon_caption, wire_caption, view_dirs):
    """The ribbon peeled apart, then each of its wires plugged in: the peeled wires are taken off the screen, and each step opens on its
    wire held over its two holes (so that the step's camera can be close on them), then pushes it in. (As the LSM's: picked up off the
    table, out of the close frame, each wire swept in from below it: the review of Lee's first round, 20 Oct 2026.)"""
    joined, apart = ribbon(jumpers, z_mid, RIBBON_PITCH), ribbon(jumpers, z_mid, SPLIT_PITCH)
    caps = [c for _, a, b, _ in jumpers for c in (a[0], b[0])]
    for colour, (ca, _), (cb, _), _ in jumpers:
        g.carry([ca], by=BREADBOARD, pose=joined[colour][0], appear=False)
        g.carry([cb], by=BREADBOARD, pose=joined[colour][1], appear=False)
    mid = np.array([FRONT_X + (len(jumpers) - 1) * RIBBON_PITCH / 2, TABLE_Y + 1.0, z_mid])
    g.place(ribbon_caption, appear=caps, lines=False, labels=[], eye=[dict(anchor=mid.round(2).tolist(), **near('up-right'))],
            wires={f'jumper {c}': joined[c][2] for c, *_ in jumpers}, wires_done={f'jumper {c}': apart[c][2] for c, *_ in jumpers},
            ride={c: apart[col][k] for col, (ca, _), (cb, _), _ in jumpers for k, c in ((0, ca), (1, cb))},
            frame=((mid + [8.0, 0.0, 0.0]).round(1).tolist(), 42.0), view_dir=[0.45, 0.8, -0.4])
    g.put_away(caps)
    for k, (colour, (ca, la), (cb, lb), key) in enumerate(jumpers):
        done = jumper_done(colour, ca, cb, key)
        ways = JUMPER_WAYS.get(colour, {ca: [UP, ZERO], cb: [UP, ZERO]})
        for c in (ca, cb):
            g.rest_at([c], ways[c][0])
        g.place(wire_caption.format(colour=colour.replace('_', ' '), a=la, b=lb), move=[ca, cb], appear=[ca, cb],
                paths=ways, lines=False, labels=sides([hole_label(la, ca), hole_label(lb, cb)], view_dirs[colour], JUMPER_PLACES.get(colour)),
                wires={f'jumper {colour}': done}, wires_done={f'jumper {colour}': done}, **hole_camera([ca, cb], view_dirs[colour]))


# The jumper wires are kit parts, but in the CAD only their caps are parts (the wire is drawn): listed by hand, pictured straight with
# a cap at each end (as the MRA's breadboard wires).
_pic = ribbon(JUMPERS_6[:1], 1305.0, RIBBON_PITCH)['black']
_pa, _pb = np.asarray(_pic[2]['pts'][0], float), np.asarray(_pic[2]['pts'][-1], float)
g.list_part('Breadboard Wire (M-M)', ['NAUO16', 'NAUO17'], 8, after='Real Time Clock')
g.part_picture('Breadboard Wire (M-M)', poses={'NAUO16': _pic[0], 'NAUO17': _pic[1]},
               wires=[dict(colour='jumper_black', radius=WIRE_R, pts=np.linspace(_pa, _pb, 40))])
# The jumpers' camera: from the front at the buzzer's end, 55 degrees up, looking down into the holes past the wires already in. A
# wire whose holes a cap or a wire hides from there has its own, the nearest from which both its holes show whole: sight lines from the
# player's own eye (core.js cameraPose, in windows from 16:9 to portrait) to 9 points over each hole, against every part and wire as
# the player draws them (the review of Lee's first round, 20 Oct 2026: the dark red wire's (+) red hole half behind the white wire's
# cap, i27 and i29 behind the green jumper and the switch's tan lead).
JUMPER_DIR = [0.497, 0.819, -0.287]
JUMPER_DIRS = {c: JUMPER_DIR for c, *_ in JUMPERS_6 + JUMPERS_2}
JUMPER_DIRS.update({'dark_red': [0.369, 0.819, -0.439], 'orange': [0.299, 0.906, -0.299], 'yellow': [0.433, 0.866, -0.25]})
# Each wire's two hole labels beside their holes, in the order the wire's ends are listed (Lee's second round, 21 Oct 2026: close to the
# holes, not at the window's edges): level and outwards where that is clear, else below or above (clear of the wires already in).
JUMPER_PLACES = {'black': [('near-right', 0.05), ('near-left', 0.05)],      # Step 9: i23, (+) red
                 'green': [('near-left', 0.05), ('near-right', 0.05)],      # Step 10: (-) blue, i24
                 'purple': [('near-left', 0.05), ('down-left', 0.05)],      # Step 11: a8, i22 (under it: to its right are the black and green wires)
                 'blue': [('near-left', 0.05), ('down-left', 0.05)],        # Step 12: a9, i21 (the same)
                 'white': [('down-right', 0.035), ('near-left', 0.05)],     # Step 13: a14, (-) blue
                 'dark_red': [('down-right', 0.045), ('down-left', 0.05)],  # Step 14: a12, (+) red (below: the a12 cap starts 14 mm in
                                                                            #   front, to their left on screen)
                 'orange': [('up-left', 0.05), ('down-right', 0.035)],      # Step 20: j1, i27
                 'yellow': [('up-left', 0.05), ('near-right', 0.05)]}       # Step 21: j3, i29
jumper_run(JUMPERS_6, 1305.0, 'Peel six wires off the ribbon of jumper wires, one of each colour, and lay them side by side.',
           'Connect the {colour} jumper wire from {a} to {b}.', JUMPER_DIRS)
# ================================================================ JUMPER WIRES (end)

# ================================================================ THE ROCKER SWITCH (begin)
# The switch is pushed into the square hole in F4 with F4 lying beside the base (the camera close on F4: published, F4 alone), then
# its three leads are plugged in one at a time: red to j27, tan to the (+) red rail, black to j29. F4 lies at the CAD's place for it
# (behind the base, raised, the leads hanging under it).
# F4 (and the switch in it) lying behind the base, relative to their seats: the CAD's pose, 35 mm nearer the base, so that the switch's
# leads can be seen close with the switch (Lee, 20 Oct 2026).
FLAT_F4 = tidy(np.add(POSES['switch_flat_F4'], [35.0, 0.0, 0.0]))
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
        labels=[dict(id=F4, text='F4', **near('down-left', 0.035)), dict(id=SWITCH, text='Rocker Switch', **near('near-left'))], wires={f'switch {c}': switch_lead(c, cap, e, FLAT_F4) for c, cap, _, e in SWITCH_LEADS},
        frame=F4_FLAT_FRAME, view_dir=[0.45, 0.75, -0.48])
SWITCH_DIRS = {c: [0.4007, 0.615, -0.6792] for c in ('red', 'tan', 'black')}   # (Lee's camera, below: from the front at the far end)
# The camera for the switch's leads, Steps 16 - 18 (Lee, 21 Oct 2026: his screenshot, solved: docs/research/lac/round2/cameras.md).
SWITCH_CAMERA = dict(view_dir=[0.4007, 0.615, -0.6792], frame=([643.67, 917.68, 1281.09], 45.24))
# Each lead's way to its hole: down from the switch, across over F3's back edge in a lane of its own (keeping to the buzzer's side of
# the clock module and clear of the other two), and down into its hole (a path search through every view the leads lie in, Steps 18 - 46).
SWITCH_WAY = {'red': [[594.9, 937.4, 1261.6], [597.6, 935.6, 1263.4], [600.9, 934.1, 1264.9], [604.8, 933.3, 1265.7], [609.1, 932.8, 1266.0], [613.0, 932.5, 1266.0], [616.8, 932.3, 1266.0], [620.8, 932.1, 1266.0], [624.6, 931.9, 1266.1], [628.8, 931.4, 1266.6], [632.4, 930.2, 1267.8], [635.5, 928.2, 1269.8], [638.0, 926.3, 1271.7], [641.1, 924.1, 1273.5], [644.5, 922.4, 1274.6], [648.2, 920.7, 1274.9], [651.6, 919.3, 1275.0], [655.4, 917.6, 1275.1]],
              'tan': [[602.0, 937.6, 1261.4], [605.7, 936.5, 1262.5], [609.8, 936.1, 1262.9], [613.8, 936.0, 1263.0], [617.8, 936.0, 1263.0], [621.7, 936.0, 1263.0], [625.7, 936.0, 1263.0], [629.7, 936.0, 1263.0], [633.7, 936.0, 1263.0], [637.6, 935.9, 1263.1], [641.8, 935.4, 1263.6], [645.4, 934.3, 1264.7], [648.2, 932.7, 1266.3], [651.4, 930.9, 1268.1], [654.9, 929.6, 1269.4], [659.0, 929.1, 1269.9], [662.8, 928.7, 1270.0], [667.0, 928.0, 1270.0], [670.5, 926.8, 1270.0], [674.4, 925.3, 1270.0], [678.1, 923.6, 1270.0], [681.5, 922.1, 1270.0], [685.3, 920.3, 1270.0], [689.0, 918.6, 1270.0], [692.8, 916.9, 1270.0]],
              'black': [[610.7, 939.0, 1258.0], [614.4, 938.3, 1258.0], [618.8, 938.0, 1258.0], [622.7, 938.0, 1258.0], [626.7, 937.9, 1258.0], [630.5, 937.4, 1258.1], [634.3, 936.2, 1258.5], [637.6, 934.1, 1259.6], [640.5, 931.5, 1261.3], [642.9, 929.1, 1262.9], [645.4, 926.6, 1264.4], [648.3, 923.9, 1266.1], [650.9, 921.7, 1267.5], [654.1, 919.5, 1268.9], [657.3, 917.3, 1270.0]]}
# Each step's hole label and the eye on the cap held over the hole, beside them (Lee's second round, 21 Oct 2026). In Lee's camera the
# holes are on the right of the board, the switch and its leads up to the right: both to the right, in the white space beside the board
# (the tan wire's (+) red on the board's left: its eye up and to the right, clear of the jumper wires there).
SWITCH_PLACES = {'red': (('near-right', 0.05), ('near-right', 0.05)),       # Step 16: j27
                 'tan': (('near-right', 0.05), ('up-right', 0.035)),        # Step 17: (+) red
                 'black': (('near-right', 0.05), ('up-right', 0.05))}       # Step 18: j29 (the cap held only 5 mm up: its eye clear of the label)
# (Step 18: the black cap held 5 mm over j29, not 18: the tan's lane passes 28 mm over j29, and the black lead, held up, went through it:
# the review of Lee's second round)
SWITCH_HOLD = {'black': [0.0, 5.0, 0.0]}
for colour, cap, label, exit_ in SWITCH_LEADS:
    done = switch_lead(colour, cap, exit_, FLAT_F4, SWITCH_WAY[colour])
    # (as each step opens the cap is taken from where it hangs and held over its hole, so that the camera can be close on the switch
    # and the hole: Lee, 20 Oct 2026)
    g.place(f"Connect the switch's {colour} wire to {label}.", move=[cap], path=[SWITCH_HOLD.get(colour, UP), ZERO], lines=False,
            labels=[dict(hole_label(label, cap), **near(*SWITCH_PLACES[colour][0]))], eye=[dict(id=cap, **near(*SWITCH_PLACES[colour][1]))],
            wires={f'switch {colour}': done}, wires_done={f'switch {colour}': done},
            **SWITCH_CAMERA)
# ================================================================ THE ROCKER SWITCH (end)

# ================================================================ JUMPER WIRES, 2 (begin)
jumper_run(JUMPERS_2, 1305.0, 'Peel two wires off the ribbon of jumper wires, an orange and a yellow, and lay them side by side.',
           'Connect the {colour} jumper wire from {a} to {b}.', JUMPER_DIRS)
# ================================================================ JUMPER WIRES, 2 (end)

# ================================================================ THE POTENTIOMETER AND F1 (begin)
# The potentiometer comes with its knob, nut and washer on: they come off one at a time (as published), the potentiometer goes through
# the round hole in F1 from the back, and they go back on in the opposite order. This is done with F1 standing upright well in front of
# the base (BUILD), the camera close on it. Then F1 is laid face down beside the base for its leads to be plugged in.
# F1 held upright 100 mm in front of its seat and 100 mm along, 35 mm up (its leads hang below it), just behind where it is laid face down
# in Step 29.
BUILD = [100.0, 35.0, 100.0]
FRONT_OUT = POSES['F1_hover_front']                                 # F1 upright in front of the box, before it goes on (the CAD's)
PULLED = [-79.0, 0.0, 0.0]                                          # the potentiometer behind F1, before it goes through (published: 79 mm)
OFF_MM = 38.0                                                       # how far the knob, nut and washer slide off the shaft (published: 37.6 - 37.9 mm)
ON_MM = 60.0                                                        # how far out each goes back on from (published: 56 - 61 mm)
DELIVERED = {KNOB: [4.611, 0.0, 0.0], NUT: [-3.0, 0.0, 0.0], WASHER: [-3.0, 0.0, 0.0]}   # (on the potentiometer as it comes: the knob as the CAD's "assembled" one; nut and washer against its body)
g.part_picture('Potentiometer', poses=DELIVERED)                    # (the parts list pictures it as it comes)
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


# Each potentiometer lead is drawn from its cap to its pin, in every shape (Lee, 20 Oct 2026: as F1 was pushed on, a lead drawn from its
# pin dipped into F8; drawn from the hole, the run in the case is held still: pot_plugged).
def pot_hanging(colour, cap, exit_, f1_pose, pot_rel=ZERO):
    """A potentiometer lead hanging straight down from its pin, with F1 at f1_pose and the potentiometer at pot_rel on it."""
    pose = compose(f1_pose, pot_rel)
    e = np.asarray(exit_, float)
    line = posed_line(pose, W.resample(np.linspace(e - [0.0, PLEN, 0.0], e, 14), 1.0))
    return W.route(line, a=cap, b=POT, a_at=compose(pose, pot_cap_rel(cap, exit_)), b_at=pose)   # (not stretched: carried whole as F1 turns)


_pot = g.model.inst[POT].bounds
SHAFT = [float(_pot[1][0]), 919.53, 1235.26]                        # the shaft's tip on the axis (seated)
BUILD_SIDE = [0.35, 0.45, -0.82]                                     # (across the shaft, from the buzzer's end)
POT_ALONE = dict(view_dir=BUILD_SIDE, frame=(posed_line(np.add(BUILD, PULLED).tolist(), [[735.0, 916.0, 1235.0]])[0].round(1).tolist(), 42.0))
BUILD_LOOK = dict(view_dir=BUILD_SIDE, frame=(posed_line(BUILD, [[722.0, 925.0, 1275.0]])[0].round(1).tolist(), 98.0))
# The nut is spun off and on, as the LSM's (Lee, 20 Oct 2026): two turns, a quarter turn per pose (the player turns the shorter way between
# two poses), its move along the shaft shared out evenly, over two beats (the breadboard, seated, keeps still for them: STAY). Seen from the
# shaft's tip, positive degrees about +x are counter-clockwise (coming off), negative clockwise (going on).
NUT_AT = [725.13, 919.53, 1235.26]                                  # the nut's middle, seated, on the shaft's axis (which runs along +x)
STAY = dict(move=[BREADBOARD], paths={BREADBOARD: [ZERO] * 3})      # (two beats, 1.6 s)


def nut_turns(x0, x1, sign, turns=2):
    """The nut's poses from x0 to x1 mm along the shaft (relative to its seat), `turns` whole turns, a quarter turn each."""
    n = 4 * turns
    return [turned([1, 0, 0], sign * 90.0 * k, NUT_AT, [round(x0 + (x1 - x0) * k / n, 2), 0.0, 0.0]) for k in range(1, n + 1)]


# Each arrow along the shaft, from just past its tip (Steps 23, 24: Lee) or the knob's face (Step 22): seated mm on the potentiometer.
TIP_ARROW = dict(tail=np.add(SHAFT, [1.0, 0.0, 0.0]).round(2).tolist(), head=np.add(SHAFT, [31.0, 0.0, 0.0]).round(2).tolist(), normal=[0.0, 0.48, -0.88], part=POT)
KNOB_ARROW = dict(TIP_ARROW, tail=[746.67, 919.53, 1235.26], head=[776.67, 919.53, 1235.26])
for part, name, verb in ((KNOB, 'knob', 'Pull the knob off'), (NUT, 'nut', 'Unscrew the nut and take it off'), (WASHER, 'washer', 'Take the washer off')):
    first = part == KNOB
    off = np.add(DELIVERED[part], [OFF_MM, 0.0, 0.0]).tolist()
    g.place(f"{'Begin the front panel with the potentiometer. ' if first else ''}{verb} the potentiometer's shaft.", appear=[POT] if first else [],
            **(dict(STAY, ride={NUT: nut_turns(DELIVERED[NUT][0], off[0], +1)}) if part == NUT else dict(ride={part: off})), lines=False,
            arrows=[KNOB_ARROW if first else TIP_ARROW],
            labels=[dict(id=POT, text='Potentiometer', **near('down-right', 0.035))] if first else [],   # (below the body: off the knob and its arrow)
            **({'wires': {f'pot {c_}': pot_hanging(c_, cap, e, BUILD, PULLED) for c_, cap, _, e, _ in POT_LEADS}} if first else {}),
            **POT_ALONE)
    g.put_away([part])
TAB_SLOT = [722.6, 919.7, 1243.1]                                  # F1's small cutout beside the round hole, the potentiometer's tab in it (seated)
g.place("Push the potentiometer's shaft through the round hole in F1 from the back, its little tab in the slot beside the hole.", appear=[F1],
        inset=dict(target=posed_line(BUILD, [TAB_SLOT])[0].round(2).tolist(), dir=[0.95, 0.25, 0.18], radius=9.0, mark=2.0,
                   alt="Close-up of the front of F1: the potentiometer's little tab in the small slot beside the round hole"),   # (as published, Step 25c: Lee)
        ride={POT: BUILD}, lines_at=[[posed_line(np.add(BUILD, PULLED).tolist(), [SHAFT])[0].round(2).tolist(), posed_line(BUILD, [[723.83, 919.53, 1235.26]])[0].round(2).tolist()]],
        labels=[dict(id=F1, text='F1', **near('near-left'))], wires_done={f'pot {c_}': pot_hanging(c_, cap, e, BUILD) for c_, cap, _, e, _ in POT_LEADS}, **BUILD_LOOK)
for part, name in ((WASHER, 'washer'), (NUT, 'nut'), (KNOB, 'knob')):
    g.carry([part], by=POT, pose=[ON_MM, 0.0, 0.0], appear=False)
    c = g.model.inst[part].bounds.mean(0)
    g.place(f"Put the {name} back on the shaft{', and tighten it against F1' if part == NUT else (', pushing it all the way on' if part == KNOB else ' against F1')}.",
            appear=[part], **(dict(STAY, ride={NUT: nut_turns(ON_MM, 0.0, -1)[:-1] + [ZERO]}) if part == NUT else dict(ride={part: ZERO})),
            lines_at=[[posed_line(np.add(BUILD, [ON_MM, 0.0, 0.0]).tolist(), [c - [float(g.model.inst[part].bounds[1][0] - g.model.inst[part].bounds[0][0]) / 2, 0.0, 0.0]])[0].round(2).tolist(),
                                                        posed_line(BUILD, [SHAFT])[0].round(2).tolist()]],
            labels=[], **BUILD_LOOK)
# F1 is laid face down in front of the breadboard's end, tipped forward from where it stood (Lee, 20 Oct 2026: closer, smoother, no stop
# part-way), so that its potentiometer's leads lie towards their holes, about 90 mm away. (The CAD and the published guide lay it face
# down past the breadboard's end, the potentiometer some 240 mm from its holes.) Its leads keep their straight shape and turn with it.
F1_MIDDLE = [722.33, 919.53, 1289.87]                               # F1's middle, seated
F1_DOWN = tidy(turned([0, 0, 1], -90.0, F1_MIDDLE, [78.97, -10.43, 99.63]))   # face down, x 763 - 839, z 1307 - 1472, the pins at x 788.6 pointing -x


def pot_flat_lead(colour, cap, exit_):
    """A potentiometer lead with F1 face down: straight out from its pin (the shape it hangs in, turned with F1)."""
    return pot_hanging(colour, cap, exit_, F1_DOWN)


g.place('Lay F1 face down in front of the end of the breadboard, as shown, the potentiometer\'s wires towards the breadboard.',
        ride={F1: F1_DOWN, POT: F1_DOWN}, **STAY, lines=False, eye=[dict(id=F1, **near('down-right', 0.065))],
        wires_done={f'pot {c}': pot_flat_lead(c, cap, e) for c, cap, _, e, _ in POT_LEADS},
        **frame_on(np.vstack([corners(F1, BUILD), corners(F1, F1_DOWN)]), [0.55, 0.62, 0.56], margin=4.0))
# Each lead's way to its hole: on from its pin over F3's front edge and down into its hole, clear of the other leads and wires (a path
# search through every view the leads lie in: docs/research/lac/scripts/routing/).
POT_WAY = {'red': [[776.8, 914.8, 1329.0], [772.9, 915.0, 1329.0], [768.9, 915.0, 1329.0], [764.5, 915.0, 1329.0], [760.5, 915.0, 1329.0], [756.5, 915.0, 1329.0], [752.5, 915.0, 1329.0], [748.5, 915.0, 1329.0], [744.5, 915.0, 1329.0], [740.5, 915.0, 1329.0], [736.5, 915.0, 1329.0], [732.5, 915.0, 1329.0], [728.5, 915.0, 1329.0], [724.5, 915.0, 1329.0], [720.5, 915.0, 1329.0], [716.5, 915.0, 1329.0], [712.6, 915.0, 1328.9], [708.8, 915.0, 1328.5], [704.6, 915.0, 1327.8], [700.9, 915.0, 1327.5], [697.1, 915.0, 1328.8]],
           'tan': [[775.9, 914.8, 1335.0], [771.5, 915.0, 1335.0], [767.5, 915.0, 1335.0], [763.5, 915.0, 1335.0], [759.5, 915.0, 1335.0], [755.6, 915.0, 1335.0], [751.6, 915.0, 1335.0], [747.6, 915.0, 1335.0], [743.6, 915.0, 1335.0], [739.6, 915.0, 1335.0], [735.7, 915.0, 1335.0], [731.7, 915.1, 1334.9], [727.9, 915.3, 1334.7], [723.7, 915.7, 1334.4], [720.0, 916.2, 1334.2], [716.0, 917.2, 1334.0], [712.0, 918.3, 1334.0], [708.3, 919.1, 1334.0], [704.2, 919.5, 1334.0], [700.1, 919.2, 1334.0], [696.6, 918.2, 1333.7], [692.9, 916.7, 1333.2]],
           'black': [[775.8, 914.8, 1340.0], [771.9, 915.0, 1340.0], [767.5, 915.0, 1340.0], [763.5, 915.0, 1340.0], [759.5, 915.0, 1340.0], [755.5, 915.0, 1340.0], [751.5, 915.0, 1340.0], [747.6, 915.0, 1340.0], [743.6, 915.0, 1340.0], [739.6, 915.0, 1340.0], [735.6, 915.0, 1340.0], [731.6, 915.0, 1340.0], [727.6, 915.0, 1340.0], [723.7, 915.0, 1339.8], [719.9, 915.0, 1339.4], [715.9, 915.0, 1338.3], [712.0, 913.8, 1336.9], [708.6, 912.6, 1335.4], [705.2, 911.9, 1333.8]]}
# (the black's last stretch lowered under the tan's hump, which crosses over it: Lee, 21 Oct 2026, Step 32, the black went up and down
# through the tan as its cap was held 18 mm over its hole; held 5 mm up, it goes in clear: docs/research/lac/round2/wire_clipping.md)
POT_ABOVE = {'black': 6.0}                                          # (straight down into its hole from 6 mm over the cap's top, not 10)
POT_HOLD = {'black': [0.0, 5.0, 0.0]}                               # (held 5 mm over its hole, under the tan's hump)
POT_EYE = {'black': ('up-right', 0.05)}                             # (the cap held only 5 mm up: its eye clear of the hole's label)


def pot_plugged(colour, cap, exit_, f1_pose, way, shared=None, above=10.0):
    """A potentiometer lead from its hole up through `way` (given from the pin) to its pin, F1 at f1_pose. With `shared` (a point on it):
    the run from the hole to there stays put as F1 moves (b_from) and is kept as the lead changes shape (tail_from); else `stretch`."""
    e = posed_line(f1_pose, [exit_])[0]
    d = unit(posed_line(f1_pose, [np.add(exit_, [0.0, -1.0, 0.0])])[0] - e)
    line = into_hole(cap, e, d, way, above=above)[::-1]
    if shared is None:
        return W.route(line, a=cap, b=POT, b_at=f1_pose, stretch=True)
    s = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))]
    k = round(float(s[int(np.argmin(np.linalg.norm(line - np.asarray(shared, float), axis=1)))]), 1)
    return W.route(line, a=cap, b=POT, b_at=f1_pose, b_from=k, tail_from=k)


# The camera for the potentiometer's leads, Steps 30 - 32 (Lee, 21 Oct 2026: his screenshot, solved: docs/research/lac/round2/cameras.md).
POT_DIR = [-0.2332, 0.758, 0.6091]                                  # (from the breadboard's end, high: the potentiometer and the holes)
POT_CAMERA = dict(view_dir=POT_DIR, frame=([697.93, 915.57, 1338.76], 41.69))
for colour, cap, label, exit_, _ in POT_LEADS:
    done = pot_plugged(colour, cap, exit_, F1_DOWN, POT_WAY[colour], above=POT_ABOVE.get(colour, 10.0))
    # (as each step opens the cap is taken from where its lead lies and held over its hole)
    g.place(f"Connect the potentiometer's {colour} wire to {label}.", move=[cap], path=[POT_HOLD.get(colour, UP), ZERO], lines=False,
            labels=[dict(hole_label(label, cap), **near('near-right'))], eye=[dict(id=cap, **near(*POT_EYE.get(colour, ('near-right', 0.05))))],
            wires={f'pot {colour}': done}, wires_done={f'pot {colour}': done},
            **POT_CAMERA)
# ================================================================ THE POTENTIOMETER AND F1 (end)

# ================================================================ THE BUZZER (begin)
# The buzzer lies beside the base (the CAD's place for it, past the breadboard's end, at the back); its red lead goes to j4, its black
# lead to the (-) blue rail.
BUZZER_LYING = POSES['buzzer_lying']
g.carry([BUZZER], by=F3, pose=BUZZER_LYING, appear=False)
BLEN = 39.0                                                         # (the CAD's straight leads: 39 mm to the cap)
for colour, cap, _, exit_, _, _ in BUZZER_LEADS:
    g.wire(f'buzzer {colour}', LEAD_COLOURS[colour], WIRE_R, name='Alarm Buzzer')


BUZZER_FAN = {'NAUO58': [-1.5, 0.0, 0.0], 'NAUO59': [1.5, 0.0, 0.0]}   # (the two caps lying 1.5 mm further apart than their exits, so that
                                                                    # the red's cap, picked up first, clears the black lead: 1.52 mm apart,
                                                                    # it brushed it: the review of Lee's second round)


def buzzer_cap_rel(cap, exit_):
    """The cap on the end of a buzzer lead lying straight out from the buzzer (relative to its seat, the buzzer seated): pin pointing
    away from the buzzer (the lead leaves it straight down when the buzzer is clamped), fanned out a little (BUZZER_FAN)."""
    return tidy(np.asarray(exit_, float) - [0.0, BLEN, 0.0] + BUZZER_FAN[cap] - wire_at(cap))


for colour, cap, _, exit_, _, _ in BUZZER_LEADS:
    g.carry([cap], by=BUZZER, pose=buzzer_cap_rel(cap, exit_))


# Each buzzer lead is drawn from its cap to the buzzer, in every shape (as the potentiometer's): the run held in the breadboard then
# stays put while the buzzer moves (b_from).
def buzzer_straight(colour, cap, exit_):
    e = np.asarray(exit_, float)
    line = posed_line(BUZZER_LYING, W.resample(np.linspace(e - [0.0, BLEN, 0.0] + BUZZER_FAN[cap], e, 12), 1.0))
    return W.route(line, a=cap, b=BUZZER, a_at=compose(BUZZER_LYING, buzzer_cap_rel(cap, exit_)), b_at=BUZZER_LYING, stretch=True)


# Each lead's way to its hole, the buzzer lying (Steps 33 - 42) and lifted 60 mm over where it lies (Step 43): short and smooth, clear
# of the parts and the other wires (a path search; Lee, 20 Oct 2026: the CAD's lying leads loop out sideways, and blending the straight
# leads into them threw them off the screen; the red one had a kink by the breadboard). Lifted, red's run behind the board's end stays
# low (under the yellow jumper's arch at j4) up to BUZZER_LIFT_HOLD and only then rises to the buzzer, so that as the buzzer is carried
# the run swings round behind the j-side caps without touching the yellow jumper (docs/research/lac/round2/step43_high.md).
BUZZER_WAY = {'red': [[647.2, 901.2, 1399.0], [647.8, 901.9, 1394.1], [647.8, 902.0, 1389.2], [647.8, 902.0, 1384.2], [647.8, 902.0, 1379.2], [647.9, 902.0, 1374.3], [648.1, 902.3, 1369.0], [648.5, 902.6, 1364.2], [648.8, 903.1, 1359.0], [648.8, 903.7, 1354.3], [649.1, 904.7, 1349.3], [650.1, 905.6, 1344.7], [652.5, 906.0, 1340.3], [655.8, 906.0, 1336.5]],
              'black': [[648.9, 897.0, 1393.1], [652.2, 897.0, 1389.5], [655.7, 897.0, 1386.0], [659.2, 897.1, 1382.5], [662.7, 897.4, 1379.0], [666.5, 897.8, 1375.2], [669.9, 898.0, 1371.8], [673.5, 898.0, 1368.3], [677.0, 898.0, 1364.9], [681.0, 898.3, 1361.5], [684.5, 899.2, 1358.7], [688.0, 901.4, 1355.6], [690.9, 904.1, 1352.7], [693.6, 907.0, 1349.8], [696.0, 910.3, 1346.4]]}
BUZZER_LIFT_WAY = {'red': [[645.7, 951.9, 1397.4], [645.9, 949.6, 1393.0], [646.6, 946.6, 1389.0], [648.0, 943.5, 1385.8], [650.5, 940.5, 1382.3], [653.0, 937.9, 1378.8], [654.6, 934.0, 1375.0], [655.2, 927.0, 1370.5], [655.0, 919.0, 1366.0], [654.3, 912.0, 1361.5], [653.8, 908.0, 1357.0], [653.5, 906.8, 1352.0], [653.6, 906.5, 1347.0], [653.2, 906.5, 1342.5], [653.0, 906.6, 1338.6]],
                   'black': [[648.2, 954.7, 1393.7], [651.0, 952.0, 1390.8], [653.8, 949.1, 1387.9], [656.7, 946.2, 1385.0], [659.6, 943.3, 1382.1], [662.5, 940.5, 1379.2], [665.4, 937.6, 1376.3], [668.3, 934.7, 1373.4], [671.1, 931.8, 1370.6], [674.0, 929.0, 1367.6], [677.3, 926.3, 1364.4], [680.4, 924.4, 1361.3], [683.9, 922.7, 1357.8], [687.1, 921.2, 1354.6], [690.6, 919.5, 1351.1], [693.7, 917.9, 1347.8], [696.7, 916.1, 1344.1]]}
BUZZER_LIFT_HOLD = {'red': 32.0}                                  # (red, lifted: the run up to here, from the hole, does not follow the buzzer)
BUZZER_LIFT = tidy(compose([0.0, 60.0, 0.0], BUZZER_LYING, BUZZER_LYING['at']))   # (about the buzzer's own middle, as BUZZER_LYING is)
BUZZER_HIGH = [0.0, 75.0, 0.0]                                       # (Step 43: carried over the board to 75 mm over its seat, clear of the
                                                                    # spread F7s' tops, then lowered straight in)


BUZZER_ABOVE = {'red': 0.5, 'black': 5.0}                           # (how far each goes straight down into its hole, over the cap's top: red
                                                                    # into j4 under the yellow jumper, whose centre line is 913 over j4)
BUZZER_CREST = {'red': 0.3, 'black': 1.5}                           # (how far over the drop's top each comes in: red low, so that held 5 mm
                                                                    # over j4 (Step 33) it stays under the yellow jumper: review, 21 Oct 2026)
BUZZER_OUT = 3.0                                                    # (straight out of the buzzer before a lead turns)
BUZZER_RISE = {'red': 2.2, 'black': 0.0}                            # (red then rises over the black lead beside it, which it turns across)


def buzzer_line(colour, cap, exit_, pose, way):
    """A buzzer lead from its exit (the buzzer at `pose`): 3 mm straight out, through `way`, over a crest BUZZER_CREST mm above the top of its
    straight drop and 4.5 mm short of it, and down into its hole. The controls within 8 mm of the run out and 7 mm (across) of the drop
    are left out, so that the lead turns over several mm (the review of Lee's first round: the path search's controls there made
    hairpins, and the drop's top a crease)."""
    q = posed_line(pose, [exit_, np.add(exit_, [0.0, -1.0, 0.0])])
    e, d = q[0], unit(q[1] - q[0])
    above = BUZZER_ABOVE[colour]
    first, top = e + d * BUZZER_OUT, wire_at(cap) + [0.0, 4.0 + above, 0.0]
    across = lambda p: float(np.hypot(p[0] - top[0], p[2] - top[2]))
    keep = [np.asarray(p, float) for p in way if np.linalg.norm(np.asarray(p, float) - first) > 8.0 and across(p) > 7.0]
    rise = [first + d * 2.0 + [0.0, BUZZER_RISE[colour], 0.0]] if BUZZER_RISE[colour] else []
    h = top - (keep[-1] if keep else first)
    h[1] = 0.0
    return into_hole(cap, e, d, rise + keep + [top - unit(h) * 4.5 + [0.0, BUZZER_CREST[colour], 0.0]], lift=BUZZER_OUT, above=above)


def shared_to(line, point):
    """How far along `line` (from its first point) its point nearest `point` is."""
    s = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))]
    return round(float(s[int(np.argmin(np.linalg.norm(line - np.asarray(point, float), axis=1)))]), 1)


def buzzer_plugged(colour, cap, exit_, pose, way, stretch=False, hold=None):
    """A buzzer lead plugged in (buzzer_line), drawn from the hole: its straight drop held in the hole (b_from) and shared between
    shapes (tail_from); the rest carried whole with the buzzer (no stretch: it turns with it). With `stretch` (the buzzer lifted, Step
    43): matched to the next shape by share of length instead, so that its run over the seat grows along the lead rather than fanning out
    from the top of the drop (where it dipped into the resistors). `hold`: mm from the hole that do not follow the buzzer (b_from), if
    more than the drop."""
    line = buzzer_line(colour, cap, exit_, pose, way)[::-1]
    k = BUZZER_ABOVE[colour] + 4.0
    return W.route(line, a=cap, b=BUZZER, b_at=pose, b_from=hold or k, **({'stretch': True} if stretch else {'tail_from': k}))


# The seated leads (Lee, 21 Oct 2026: "pass the red and black wires over the black/green/purple/blue wires"; his second note on Step 43,
# the same day: and not through them as the buzzer is carried in). From the stub's end, straight on down 1 mm and round under it. Red comes
# into j4 from behind, as it lies before the step (under the yellow jumper's arch only at the hole): it climbs behind the j-side caps,
# crosses over the yellow and orange jumpers just past the clock module, over the row-i ends of the jumpers and over the black and green
# jumpers' arches, then over the switch's tan lead by the (+) red rail and down in front of the switch to the buzzer. Black runs along the
# front rails over the potentiometer's leads, the LCD's purple wire and the green jumper, over the switch's tan lead, to the buzzer. Both
# pass in front of the switch (on its +x side where it is seated), so that neither is under one of the switch's leads before F4 is lifted
# (Step 47): the buzzer is carried over the board, so its leads can only lie over what they cross, and the switch is then carried over
# them (docs/research/lac/round2/step43_high.md: which crossings each motion allows). Drawn from the stub's end: no gap where the lead
# meets it.
BUZZER_SEAT_WAY = {'red': [[674.5, 891.3, 1235.6], [675.5, 892.6, 1239.0], [678.0, 894.5, 1241.8], [683.5, 899.5, 1246.0], [685.3, 903.5, 1249.5], [686.3, 907.5, 1253.0], [687.4, 911.0, 1256.5], [688.5, 914.5, 1260.0], [689.3, 919.5, 1262.5], [690.0, 923.8, 1265.0], [690.4, 927.8, 1268.2], [690.3, 931.5, 1272.0], [689.3, 934.6, 1275.3], [687.0, 935.6, 1278.3], [682.5, 935.4, 1280.6], [676.5, 934.0, 1282.3], [671.0, 931.0, 1284.0], [667.0, 927.8, 1286.2], [665.2, 926.0, 1289.0], [664.6, 925.6, 1293.5], [663.6, 925.0, 1298.5], [661.6, 923.8, 1303.0], [659.3, 921.6, 1307.0], [657.6, 917.8, 1311.8], [656.9, 913.2, 1317.5], [657.1, 909.3, 1323.5], [657.9, 907.4, 1329.0]],
                   'black': [[676.2, 891.3, 1235.6], [677.6, 893.0, 1238.8], [680.6, 895.6, 1240.6], [686.8, 902.4, 1244.4], [687.8, 905.7, 1247.7], [688.1, 909.5, 1251.5], [688.8, 912.9, 1254.9], [690.4, 916.1, 1258.1], [692.4, 919.5, 1261.5], [693.2, 922.9, 1264.9], [694.1, 926.6, 1268.6], [695.8, 929.6, 1271.8], [697.7, 932.1, 1275.6], [698.4, 933.1, 1280.5], [698.5, 933.1, 1285.3], [698.5, 932.2, 1290.4], [698.5, 930.3, 1295.2], [698.5, 928.6, 1299.9], [698.5, 928.0, 1304.7], [698.5, 927.8, 1309.6], [698.5, 926.5, 1314.5], [698.5, 924.3, 1319.1], [698.5, 922.7, 1324.0], [698.5, 922.1, 1328.7], [698.5, 921.0, 1333.5]]}
BUZZER_SEAT_OUT = 1.0                                               # (straight on out of the stub before the lead turns under it)
BUZZER_KEEP = {'red': [661.6, 923.8, 1303.0], 'black': None}         # (Step 43: the run from the hole to here is the same carried high and
                                                                    # seated, and stays put as the buzzer is lowered; black: its drop)
BUZZER_RISER = {'red': [661.0, 945.0, 1304.2], 'black': [699.2, 945.0, 1340.9]}   # (carried high: the top of each lead's
                                                                    # rise, red's from BUZZER_KEEP behind the j-side caps, black's straight up out of (-) blue)
BUZZER_RED_RISE = [[661.2, 928.0, 1303.8], [661.0, 934.0, 1304.2]]
BUZZER_HIGH_WAY = {'red': [[673.0, 960.0, 1238.0], [676.0, 957.0, 1252.0], [680.0, 954.0, 1268.0], [674.0, 951.0, 1285.0], [665.5, 948.0, 1298.0]],
                   'black': [[679.0, 960.0, 1237.0], [686.0, 959.0, 1250.0], [693.0, 958.0, 1268.0], [698.5, 955.0, 1290.0], [699.0, 950.0, 1322.0]]}


def seated_from_buzzer(colour, cap, exit_):
    """A buzzer lead seated, from the stub's end to the hole, every 1 mm (red in over a crest under the yellow jumper, as buzzer_line)."""
    e, d = np.asarray(exit_, float), np.array([0.0, -1.0, 0.0])
    above = BUZZER_ABOVE[colour]
    top = wire_at(cap) + [0.0, 4.0 + above, 0.0]
    way = [np.asarray(p, float) for p in BUZZER_SEAT_WAY[colour]]
    if colour == 'red':
        h = top - way[-1]
        h[1] = 0.0
        way.append(top - unit(h) * 4.5 + [0.0, BUZZER_CREST[colour], 0.0])
    return into_hole(cap, e, d, way, lift=BUZZER_SEAT_OUT, above=above)


def buzzer_kept(colour, cap, exit_):
    """The seated lead from the hole to BUZZER_KEEP (black: its drop), and its length."""
    line = seated_from_buzzer(colour, cap, exit_)[::-1]
    if BUZZER_KEEP[colour] is None:
        k = BUZZER_ABOVE[colour] + 4.0
    else:
        k = shared_to(line, BUZZER_KEEP[colour])
    s = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))]
    return line[:int(np.argmin(np.abs(s - k))) + 1], k


def buzzer_high(colour, cap, exit_):
    """A buzzer lead with the buzzer carried high over its seat (BUZZER_HIGH, Step 43): the seated lead from the hole to BUZZER_KEEP, up
    to the top of its rise (BUZZER_RISER) and high over the board to the buzzer (BUZZER_HIGH_WAY). Drawn from the hole; the run to the top
    of the rise does not follow the buzzer (b_from), and the run kept is matched by distance from the hole to the seated lead's as the
    buzzer is lowered (tail_from), the rest by distance from the buzzer: it settles straight down onto the seated lead."""
    kept, k = buzzer_kept(colour, cap, exit_)
    top = np.asarray(BUZZER_RISER[colour], float)
    if colour == 'red':
        line = seated_from_buzzer(colour, cap, exit_)
        j = len(line) - len(kept)                                   # (where the kept run ends, on the seated lead drawn from the stub)
        rise = W.resample(W.smooth([kept[-1], *[np.asarray(c, float) for c in BUZZER_RED_RISE], top], start_dir=unit(line[j - 1] - line[j]),
                                   end_dir=[0, 1, 0], spacing=0.5), 1.0)
    else:
        w = wire_at(cap)
        n = int(round(top[1] - w[1]))
        rise = np.array([[w[0], w[1] + i * (top[1] - w[1]) / n, w[2]] for i in range(n + 1)])
        kept = rise[:1]
    head = np.vstack([kept, rise[1:]])
    e, d = np.add(exit_, BUZZER_HIGH), np.array([0.0, -1.0, 0.0])
    body = W.smooth([e + d * BUZZER_OUT, *[np.asarray(c, float) for c in BUZZER_HIGH_WAY[colour]], top], start_dir=d, end_dir=[0, -1, 0],
                    spacing=0.5)
    tail = W.resample(W.join(W.straight(e, d, BUZZER_OUT), body), 1.0)[::-1]
    held = round(float(np.linalg.norm(np.diff(head, axis=0), axis=1).sum()), 1)
    return W.route(np.vstack([head, tail[1:]]), a=cap, b=BUZZER, b_at=BUZZER_HIGH, b_from=held, tail_from=k)


def buzzer_clamped(colour, cap, exit_):
    """A buzzer lead seated (seated_from_buzzer), drawn from the hole; the run from the hole to BUZZER_KEEP held still and kept (as the
    buzzer is lowered onto its seat, the rest follows it down)."""
    line = seated_from_buzzer(colour, cap, exit_)[::-1]
    _, k = buzzer_kept(colour, cap, exit_)
    return W.route(line, a=cap, b=BUZZER, b_from=k, tail_from=k)


# The camera for the buzzer's leads, Steps 33 - 34 (Lee, 21 Oct 2026: his screenshot, solved: docs/research/lac/round2/cameras.md).
BUZZER_DIR = [-0.3958, 0.7598, 0.5158]                              # (from behind at the breadboard's end, as published, closer)
BUZZER_CAMERA = dict(view_dir=BUZZER_DIR, frame=([656.14, 910.4, 1382.06], 46.98))
BUZZER_PLACES = {'red': (('near-left', 0.05), ('up-left', 0.035)),         # Step 33: j4, and the eye on the lying cap
                 'black': (('near-right', 0.05), ('near-left', 0.05))}      # Step 34: (-) blue (at the board's end: white space to its right)
for k, (colour, cap, label, exit_, lying_key, _) in enumerate(BUZZER_LEADS):
    start = compose(BUZZER_LYING, buzzer_cap_rel(cap, exit_), cap_mid(cap))
    done = buzzer_plugged(colour, cap, exit_, BUZZER_LYING, BUZZER_WAY[colour])
    # (the red cap comes in from beside j4, 5 mm up, under the yellow jumper's arch over j4: held over j4 it stood in the arch)
    g.place(f"{'Lay the alarm buzzer beside the base, past the end of the breadboard. ' if k == 0 else ''}Connect the buzzer's {colour} wire to {label}.",
            move=[cap], path=[start, via(dict(start, t=np.add(start['t'], [0.0, 6.0, 0.0]).round(2).tolist())), via([-14.0, 5.0, 0.0]),
                              [0.0, 5.0, 0.0], ZERO] if colour == 'red' else [start, UP, ZERO], lines=False,   # (red: lifted off the black lead first)
            appear=[BUZZER, cap] if k == 0 else [],                   # (the cap on screen where it lies as the step opens)
            labels=([dict(id=BUZZER, text='Alarm Buzzer', **near('near-left', 0.065))] if k == 0 else []) + [dict(hole_label(label, cap), **near(*BUZZER_PLACES[colour][0]))],
            eye=[dict(id=cap, **near(*BUZZER_PLACES[colour][1]))], wires={f'buzzer {c}': buzzer_straight(c, cp, e) for c, cp, _, e, _, _ in BUZZER_LEADS} if k == 0 else None,
            wires_done={f'buzzer {colour}': [done, done]},
            **BUZZER_CAMERA)
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


LCD_X, LCD_Z = 733.0, 1245.0                                        # the LCD ribbon's near wire and its middle: in front of F3's edge, near the
                                                                    # holes (Lee, 20 Oct 2026: the holes closer), and clear of F1 and the
                                                                    # potentiometer's leads (Lee, 21 Oct 2026, Step 35: it lay under them;
                                                                    # at z 1278 F1, propped 22 mm up, still hid the teal and blue's ends)


def lcd_ribbon(pitch):
    """Each LCD wire lying on the table in front of the base: {colour: (male cap's pose, female cap's pose relative to the lying LCD,
    the straight route)}. The male end towards the breadboard (-z), its pin pointing -z; the female end towards the lying LCD's header
    (+z), its open end +z: turned as the lying LCD is, so that it goes onto its pin without spinning round. (Lee's first round: the
    other way round, each wire's two ends crossed over as it was connected.)"""
    out = {}
    for k, (colour, male, _, fem, *_ ) in enumerate(LCD_WIRES):
        x = LCD_X + k * pitch
        pm = np.array([x, TABLE_Y + 0.875, LCD_Z - RIBBON_MM / 2])
        pf = np.array([x, TABLE_Y + 0.875, LCD_Z + RIBBON_MM / 2])
        m = lying(male, pm, [0, 0, -1])
        f_rel = tidy((unapply_pose(LCD_LYING, pf[None])[0] - fem_centre(fem)).round(3).tolist())
        f_world = compose(LCD_LYING, f_rel, fem_centre(fem).round(2))                  # (where that puts it, as the generator composes it)
        out[colour] = (m, f_rel, W.route(W.resample(np.linspace(pm, pf, 12), 1.0), a=male, b=fem, a_at=m, b_at=f_world, stretch=True))
    return out


joined, apart = lcd_ribbon(RIBBON_PITCH), lcd_ribbon(SPLIT_PITCH)
# (listed by hand, pictured straight with its male cap at one end and its female cap at the other, as it lies before it goes in)
_m, _f = LCD_WIRES[0][1], LCD_WIRES[0][3]
_line = np.asarray(joined['purple'][2]['pts'], float)
g.list_part('Breadboard Wire (M-F)', [_m, _f], 4, after='Breadboard Wire (M-M)')
g.part_picture('Breadboard Wire (M-F)', poses={_m: joined['purple'][0], _f: joined['purple'][2]['b_ref']},
               wires=[dict(colour='jumper_purple', radius=WIRE_R, pts=np.linspace(_line[0], _line[-1], 40))])
for colour, male, _, fem, *_ in LCD_WIRES:
    g.carry([male], by=BREADBOARD, pose=joined[colour][0], appear=False)
    g.carry([fem], by=LCD, pose=joined[colour][1], appear=False)
_mid = np.array([LCD_X + 1.5 * RIBBON_PITCH, TABLE_Y + 1.0, LCD_Z])
g.place('Lay the LCD screen face down beside the base. Then peel four wires off the ribbon of male-female wires and lay them side by side.',
        appear=[LCD] + LCD_MALE + LCD_FEMALE, lines=False, labels=[dict(id=LCD, text='LCD Screen', **near('down-right'))],
        eye=[dict(anchor=_mid.round(2).tolist(), **near('near-left', 0.035))],
        wires={f'lcd {c}': joined[c][2] for c, *_ in LCD_WIRES}, wires_done={f'lcd {c}': apart[c][2] for c, *_ in LCD_WIRES},
        ride={**{m: apart[c][0] for c, m, *_ in LCD_WIRES}, **{f: apart[c][1] for c, _, _, f, *_ in LCD_WIRES}},
        frame=([700.0, 905.0, 1330.0], 125.0), view_dir=[0.62, 0.62, 0.48])   # (the camera Lee saw, a little wider to take in the
                                                                                # ribbon where it now lies: Lee, 21 Oct 2026)
# The peeled wires leave the table (as the LSM's and the jumpers): each wire step opens on its wire already in place, its female end
# just off its pin on the header and its male end held over its hole, and pushes both in. (Lee, 21 Oct 2026, Steps 36 - 39: picked up
# off the table, each wire passed through the potentiometer's leads and the jumpers on its way, and the cameras had to take in the table.)
g.put_away(LCD_MALE + LCD_FEMALE)
LCD_DIR = [0.62, 0.62, 0.48]                                        # (from the front at the breadboard's end)
# Each wire's step from LCD_DIR, but for SDA's, whose hole b8 shows whole only from 20 degrees further round and higher (sight lines as
# for the jumpers, JUMPER_DIRS); SCL's hole b9 does not show from anywhere in front (the caps in a8 and a9 and the purple jumper stand in
# front of it, the Nano behind it), so its step has a close-up from above on Step 39c, the blue wire's pin in b9.
LCD_DIRS = {'teal': [0.343, 0.766, 0.544]}


def fem_end(fem, lcd_pose=None):
    """The middle of the end of a female cap its wire comes out of (the end away from its pin, +z seated) and the way out of it, with the
    LCD at lcd_pose."""
    box = np.asarray(CAPS[fem]['box'], float)
    end = [box[:, 0].mean(), box[:, 1].mean(), box[1, 2]]
    p = posed_line(lcd_pose, [end, np.add(end, [0.0, 0.0, 1.0])])
    return p[0], unit(p[1] - p[0])


def into_fem(line, fem, lcd_pose):
    """A CAD wire's line from its female end, made to start 4 mm inside the cap and leave it along its axis (the CAD's teal and blue
    wires stop 2 mm short of their caps: Lee, 20 Oct 2026, "empty space")."""
    end, out = fem_end(fem, lcd_pose)
    line = np.asarray(line, float)
    keep = line[np.linalg.norm(line - end, axis=1) > 3.5]
    keep = keep[np.argmin(np.linalg.norm(keep - end, axis=1)):]   # (from the first point clear of the cap's end)
    head = W.smooth([end - out * 4.0, end + out * 1.5, keep[0], keep[min(2, len(keep) - 1)]], start_dir=out, spacing=0.5)
    return W.resample(W.join(head, keep[min(2, len(keep) - 1):]), 1.0)


# The LCD's wires run from the breadboard (male end, a) to the header (female end, b). The run from the breadboard round F9's back edge
# (where the wires go once the LCD is in, between F9 and F5) is held still while the LCD is moved: the wire follows the LCD only from
# there on (b_from), and changes shape between stops from there on (tail_from). (Lee, 20 Oct 2026: drawn from the female end and
# stretched, the run behind F9 followed the LCD by 84 % and went through F9 as the LCD went in.)
def behind_f9(line):
    """The first point of a line from the breadboard that has come round F9's back edge (x < 689) to 3 mm past F9's far face (z > 1360.3)."""
    return next(i for i, p in enumerate(line) if p[2] > 1360.3 and p[0] < 689.0)


LCD_RISE = {'NAUO82': [[698.6, 921.5, 1290.3], [694.0, 927.0, 1292.0], [688.5, 928.9, 1295.5]],   # (GND: up, over the (+) rail and
            'NAUO84': [[696.5, 921.5, 1296.5]]}                                                     # the jumpers' ends; VCC: up and on)
LCD_RISE_JOIN_Z = {'NAUO82': 1299.76, 'NAUO84': 1304.59}            # (where each meets the CAD's run, going on along it)


def rerouted(male, line):
    """A CAD wire's line from the breadboard, its start redrawn from the moved hole (LCD_RAIL_SHIFT): 14 mm straight up, then smoothly
    through LCD_RISE into the CAD's own run."""
    if male not in LCD_RISE:
        return line
    j = int(np.argmax(line[:, 2] >= LCD_RISE_JOIN_Z[male]))
    w = wire_at(male)
    body = W.smooth([w + [0.0, 14.0, 0.0], *LCD_RISE[male], line[j]], start_dir=[0, 1, 0], end_dir=unit(line[j + 2] - line[j]), spacing=0.5)
    head = W.resample(W.join(W.straight(w, [0, 1, 0], 14.0), body), 1.0)
    head[-1] = line[j]
    return W.join(head, line[j:])


def lcd_line(key, male, fem, lcd_pose):
    """A CAD wire's line from the breadboard (its male end) into its female cap, the LCD at lcd_pose."""
    return rerouted(male, into_fem(cad_line(key, male)[::-1], fem, lcd_pose)[::-1])


def lcd_lead(line, fem, male, lcd_pose, at):
    """An LCD wire along `line` (from the breadboard), the LCD at lcd_pose: the run up to the point nearest `at` stays put."""
    line = W.resample(line, 1.0)
    s = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))]
    k = round(float(s[int(np.argmin(np.linalg.norm(line - np.asarray(at, float), axis=1)))]), 1)
    return W.route(line, a=male, b=fem, b_at=lcd_pose, b_from=k, tail_from=k)


def lcd_tail(head, fem, lcd_pose, controls, reach=3.0):
    """`head` (from the breadboard round F9's back edge), then through `controls` into the female cap with the LCD at lcd_pose, the last
    `reach` mm along the cap's axis and 4 mm into it."""
    end, out = fem_end(fem, lcd_pose)
    body = W.smooth([head[-1], *[np.asarray(c, float) for c in controls], end + out * reach], start_dir=unit(head[-1] - head[-3]),
                    end_dir=-out, spacing=0.5)
    return W.join(head, body, np.array([end + out * reach, end - out * 4.0]))


# Every shape of a wire shares the seated CAD wire's run from the breadboard round F9's back edge (LCD_HEAD), lying too: the CAD's
# lying wires run under the jumpers and its seated ones over them, so that changing from one to the other in Step 50 passed the run
# through the jumpers (the review of Lee's first round). Lying, each wire goes on from there in a lane of its own, so that the four do
# not cross: they come round F9's edge one above the other (GND on top) and go onto pins side by side (GND nearest), so each drops at
# its own distance past F9's end (GND the furthest), runs along under the ones above it to its pin, and turns in to its cap.
LCD_LANE_Z = {'purple': 1371.0, 'yellow': 1368.0, 'teal': 1365.0, 'blue': 1362.0}


LCD_LANE_CTRL = (0.3, 0.55, 0.82)                                   # (shares of the way from the run's end to the pin, in x)


def lying_lane(colour, fem, head):
    """The control points of an LCD wire's lane from the end of its shared run to its pin on the lying LCD: across to its lane while
    nearly level, down while moving on towards its pin, along at the pin's height, and in to its cap (Lee, 21 Oct 2026: a hairpin over
    F9's place and a straight drop read as bent at random)."""
    h, z = head[-1], LCD_LANE_Z[colour]
    end, out = fem_end(fem, LCD_LYING)
    x, y = end[0], end[1]
    a, b, c = LCD_LANE_CTRL
    return [[h[0] + a * (x - h[0]), h[1] - 1.0, z - 1.0], [h[0] + b * (x - h[0]), (h[1] + y) / 2, z],
            [h[0] + c * (x - h[0]), y + 1.2, z + 0.5], [x - 0.4, y, z + 6.0]]


LCD_HEAD, LCD_LYING_LEAD = {}, {}
for colour, male, _, fem, _, lying_key, _, seated_key in LCD_WIRES:
    _seated = lcd_line(seated_key, male, fem, None)
    LCD_HEAD[colour] = _seated[:behind_f9(_seated) + 1]
    LCD_LYING_LEAD[colour] = lcd_lead(lcd_tail(LCD_HEAD[colour], fem, LCD_LYING, lying_lane(colour, fem, LCD_HEAD[colour])), fem, male, LCD_LYING,
                                      LCD_HEAD[colour][-1])
# Each step's pin label (on the lying LCD's header) and hole label beside their spots (Lee's second round, 21 Oct 2026): the pin's
# towards the board (between the header and F3: to its left lies the buzzer), the hole's up and to the right or level to the right
# (clear of the wires already in).
LCD_PLACES = {'purple': (('near-right', 0.035), ('up-right', 0.05)),     # Step 36: GND, (-) blue
              'yellow': (('near-right', 0.035), ('up-right', 0.05)),     # Step 37: VCC, (+) red
              'teal': (('near-right', 0.05), ('near-right', 0.065)),     # Step 38: SDA, b8
              'blue': (('near-right', 0.035), ('near-right', 0.065))}    # Step 39: SCL, b9
# Each wire step's camera, as it was (Lee, 20 Oct 2026: close on the holes and the header): with the wires no longer on the table there
# is nothing further out to take in.
LCD_CAMERAS = {'purple': ([716.1, 905.9, 1333.8], 68.4), 'yellow': ([718.3, 905.9, 1333.8], 69.9),
               'teal': ([716.8, 905.9, 1337.3], 70.1), 'blue': ([720.4, 905.9, 1337.3], 71.9)}
# Each wire is pushed in by its cap only (Lee, 21 Oct 2026, Steps 37 - 39: each LCD wire went through the ones put in before it; the
# whole run to F9's edge rode on the cap, lifted 18 mm with it): drawn with its cap held at UP as a shape of its own, straight up out of
# the cap and in one bend into the lying route at LCD_JOIN mm along it, before it runs under a wire put in earlier; then the lying route
# itself, paired with it from the join on (tail_from), so that only the cap and the bit by it move as it is pushed in. From the next step
# on the wire takes the same points without tail_from (LCD_PLAIN), an unseen swap: with tail_from in both, the player pairs the run up to
# the larger of the two by distance from the first end, which pulled the wire out of shape as the next step opened. (docs/research/lac/
# round2/wire_clipping.md)
LCD_JOIN = {'purple': 22.0, 'yellow': 22.0, 'teal': 25.0, 'blue': 23.0}


def lcd_held(colour, male, fem, lying):
    """An LCD wire's lying route `lying` (from the breadboard) with its male cap held at UP; the same route for the push, paired with it
    from the join on; and the same route with no tail_from, for the steps after. The lying route's own points are used as they are, so
    that every swap is exact."""
    line, k = np.asarray(lying['pts'], float), lying['b_from']       # (k: the shared run's length)
    s = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))]
    i = int(np.searchsorted(s, LCD_JOIN[colour]))
    J, tJ = line[i], unit(line[i + 2] - line[i])
    start = line[0] + UP
    P1 = start + [0.0, 4.0, 0.0]
    body = W.smooth([P1, P1 + (J - P1) * 0.4, J], start_dir=[0, 1, 0], end_dir=tJ, spacing=0.25)
    first = W.resample(W.join(W.straight(start, [0, 1, 0], 4.0), body), 1.0)
    first[-1] = J
    f = round(W.length(first), 1)
    held = W.route(W.join(first, line[i:]), a=male, b=fem, a_at=UP, b_at=LCD_LYING, b_from=round(f + k - float(s[i]), 1), tail_from=f)
    push = W.route(line, a=male, b=fem, b_at=LCD_LYING, b_from=k, tail_from=round(float(s[i]), 1))
    plain = W.route(line, a=male, b=fem, b_at=LCD_LYING, b_from=k)                      # (no tail_from: see above)
    return held, push, plain


LCD_PLAIN = {}
for k, (colour, male, label, fem, pin, lying_key, _, _) in enumerate(LCD_WIRES):
    held, push, LCD_PLAIN[colour] = lcd_held(colour, male, fem, LCD_LYING_LEAD[colour])
    prev = {f'lcd {LCD_WIRES[k - 1][0]}': LCD_PLAIN[LCD_WIRES[k - 1][0]]} if k else {}   # (the wire before: the same line, unseen)
    view = LCD_DIRS.get(colour, LCD_DIR)
    top = [round(float(wire_at(male)[0]), 2), BB_TOP, round(float(wire_at(male)[2]), 2)]
    g.carry([fem], by=LCD, pose=F_OFF, appear=False)               # (just off its pin, on the lying LCD)
    g.rest_at([male], UP)                                           # (held over its hole)
    g.place(f"Connect the {colour} wire from {pin} on the LCD screen to {label}.", move=[male], appear=[male, fem], paths={male: [UP, ZERO]},
            ride={fem: ZERO}, lines=False,
            labels=[dict(text=pin, anchor=fem_centre(fem).round(2).tolist(), id=LCD, **near(*LCD_PLACES[colour][0])),
                    dict(hole_label(label, male), **near(*LCD_PLACES[colour][1]))],
            wires=dict(prev, **{f'lcd {colour}': held}), wires_done={f'lcd {colour}': push},
            **({'inset': dict(target=top, dir=[0.08, 1.0, 0.06], radius=14.0, mark=1.0,
                              alt=f"Close-up from above: the {colour} wire's pin in {label}, between the jumper wires and the Nano Board")}
               if colour == 'blue' else {}),
            view_dir=view, frame=LCD_CAMERAS[colour])
# ================================================================ THE LCD SCREEN (end)

# ================================================================ THE USB CABLE (begin)
# The right-angle Mini-B end goes into the Nano Board's socket (hover and plug, as decided for the MRA: section 13). The cable leaves
# it towards the back and lies straight out behind the case, on the table, along the line on which F2's slit comes in (Step 55: F2 is
# brought in from behind, swung out, its tabs are hooked into F5 and it swings shut, its slit, open at the bottom, sliding along the
# cable); from then on it passes through the slit, and bends round to the A end. (The CAD's cable crosses F2's plane at z 1339.4,
# y 890.8, through F3's edge, and lays the A end along the case, 9 mm under the table; here the cable passes 9 mm higher, in the
# slit's open part, clear of F2, F3 and the breadboard.)
g.wire('usb cable', 'cable_black', 1.75, name='USB Cable')
# Where the cable leaves each plug, measured from the plugs' meshes (docs/research/lac/round2/usb_ends.md; Lee, 21 Oct 2026, Step 40:
# the cable met both plugs off-centre): the middle of the end of the Mini-B plug's cable stub (4.5 mm across, along -x from x 666.34),
# and of the A end's strain relief (8 mm across, facing -z as the CAD has the A end). The CAD's own cable body (NAUO123) ends on both;
# the centre line wire-paths.json has for it starts 1.74 mm and ends 2.37 mm off them, and leaves the Mini-B end 25 degrees off its axis.
USB_EXIT, USB_EXIT_DIR = np.array([658.34, 903.33, 1354.39]), np.array([-1.0, 0.0, 0.0])
USB_TUCK = 1.0                                                      # (the tube runs on 1 mm into each plug, so its flat end does not show)
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
A_CABLE_END = np.array([599.97, 876.35, 1389.92])                   # the middle of the A end's strain relief, as the CAD has it (its plug towards +z)
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
    line = W.resample(W.join(W.straight(start - USB_EXIT_DIR * USB_TUCK, USB_EXIT_DIR, USB_TUCK), inside, outside,
                             W.straight(outside[-1], [-1, 0, 0], 12.0 + USB_TUCK)), 1.0)   # (down to the table, and straight into the A end's middle)
    to_slit = float(np.linalg.norm(np.diff(line[:int(np.argmin(np.linalg.norm(line - slit, axis=1))) + 1], axis=0), axis=1).sum())
    return {'usb cable': W.route(line, a=USB_B, b=USB_A, a_at=a_at, b_at=A_ON_TABLE, tail_from=round(to_slit, 1))}   # (the bit in the slit stays in it as the cable changes shape)


g.place("Plug the USB cable's small end into the Nano Board's USB socket, the cable towards the back.", move=[USB_B], appear=[USB_A], path=[[0.0, 0.0, USB_OUT], ZERO],
        lines_at=[[[676.34, 903.89, 1337.64], [676.34, 903.89, 1345.07]]], labels={USB_B: 'USB Cable'},
        wires=dict(usb_cable(USB_OUT), **{'lcd blue': LCD_PLAIN['blue']}), wires_done=usb_cable(),   # (the blue LCD wire: an unseen swap)
        view_dir=[-0.45, 0.45, 0.77], frame=([672.0, 906.0, 1352.0], 32.0))   # (close, into the socket: Lee)
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
        lines_at=[[np.add(t, [0.0, F7_HOVER, 0.0]).tolist(), [t[0], 887.61, t[2]]] for t in F7_TAB.values()], labels=[dict(id=F7A, text='2x F7', **near('near-right', 0.065))],
        view_dir=CASE_CAMERA['view_dir'], frame=([678.0, 948.0, 1262.0], 110.0))   # (as the case's camera, the model lower: the F7s and where they hover centred)
SPREAD = 15.0                                                       # (published: about 15 degrees)
TILT_A = turned([0, 0, 1], SPREAD, [657.33, 887.61, 1233.2])
TILT_B = turned([0, 0, 1], -SPREAD, [693.18, 887.61, 1233.2])
g.place('Spread the tops of the two F7s apart.', ride={F7A: TILT_A, F7B: TILT_B}, lines=False,
        arrows=[dict(tail=[655.0, 945.0, 1233.2], head=[628.0, 945.0, 1233.2], normal=[0, 1, 0], part=F3),
                dict(tail=[695.5, 945.0, 1233.2], head=[722.5, 945.0, 1233.2], normal=[0, 1, 0], part=F3)], **CASE_CAMERA)
# (lifted, carried high over the board to 75 mm over its seat and lowered in: a stop each, its leads keeping pace stop by stop: carried,
# each lead rises behind what it will lie over and arches high to the buzzer; lowered, it settles straight down onto its seated way)
g.place('Lower the buzzer in between the two F7s, its ears into their slots.', move=[BUZZER], path=[BUZZER_LYING, BUZZER_LIFT, BUZZER_HIGH, ZERO],
        lines=False, eye=[dict(id=BUZZER, **near('near-above'))],         # (above the buzzer: Lee, 21 Oct 2026)
        wires_done={f'buzzer {c}': [buzzer_plugged(c, cap, e, BUZZER_LIFT, BUZZER_LIFT_WAY[c], stretch=True, hold=BUZZER_LIFT_HOLD.get(c)),
                                    buzzer_high(c, cap, e), buzzer_clamped(c, cap, e)] for c, cap, _, e, _, _ in BUZZER_LEADS}, **CASE_CAMERA)
g.place('Let go of the two F7s, so that they close on the buzzer.', ride={F7A: ZERO, F7B: ZERO}, lines=False, eye=[dict(id=F7A, **near('near-right')), dict(id=F7B, **near('down-left'))], **CASE_CAMERA)
g.place('Push F9 down into the slots in F3 beside the end of the breadboard, its engraved side towards that end.', move=[F9], labels=[dict(id=F9, text='F9', **near('near-left', 0.035))],
        review='The published guide hooks F9 in tilted and then stands it up (Steps 45, 46); in the CAD it goes straight down into its '
               'slots, so it does here. Does the real part need the hook-and-swing?',
        view_dir=[0.53, 0.66, 0.53], frame=([700.0, 945.0, 1330.0], 110.0))   # (from the side its code faces, as published; the model lower, F9 over it in frame)

# F1 is moved out of the way, as published (Step 46: to the far end), still face down: further out in front and along towards the F7s'
# end, so that the potentiometer's leads run in between F7 and where F8 goes, behind F8 and the LCD (lying where it was, they crossed the
# LCD's seat). Each lead's way: a path search through the case as it is once the LCD is in, F8's way in kept clear
# (docs/research/lac/scripts/routing/).
F1_ASIDE = tidy(turned([0, 0, 1], -90.0, F1_MIDDLE, [135.97, -10.43, 14.63]))
ASIDE_WAY = {'red': [[832.9, 914.9, 1244.0], [827.9, 915.0, 1244.0], [822.9, 915.0, 1244.0], [817.9, 915.0, 1244.0], [812.9, 915.0, 1244.0], [807.9, 915.0, 1244.0], [802.9, 915.0, 1244.0], [797.9, 915.0, 1244.0], [792.5, 915.1, 1243.9], [787.7, 915.3, 1243.7], [783.0, 915.7, 1243.3], [777.7, 915.9, 1243.1], [772.7, 916.0, 1243.0], [767.7, 916.0, 1243.0], [762.7, 916.0, 1243.0], [757.7, 916.0, 1243.0], [752.7, 916.0, 1243.0], [747.7, 916.0, 1243.0], [742.7, 916.0, 1243.0], [737.7, 916.0, 1243.0], [732.9, 916.3, 1243.0], [727.8, 917.3, 1243.0], [722.8, 918.6, 1243.0], [718.3, 919.5, 1243.1], [713.4, 919.9, 1244.0], [709.4, 920.0, 1247.2], [707.4, 920.1, 1251.6], [705.2, 920.6, 1256.0], [702.4, 921.8, 1259.9], [700.1, 923.2, 1264.5], [699.9, 923.9, 1269.1], [701.4, 924.0, 1273.8], [703.5, 924.0, 1278.4], [704.7, 924.0, 1283.4], [705.0, 924.0, 1288.3], [705.0, 924.0, 1293.3], [705.0, 924.0, 1298.3], [705.0, 924.0, 1303.3], [704.7, 923.7, 1308.6], [703.8, 922.9, 1313.0], [702.0, 921.4, 1317.8], [700.0, 920.0, 1321.9], [697.7, 918.5, 1326.3]],
              'tan': [[831.9, 914.9, 1250.0], [826.9, 915.0, 1250.0], [821.9, 915.0, 1250.0], [816.9, 915.0, 1250.0], [811.9, 915.0, 1250.0], [806.9, 915.0, 1250.0], [801.9, 915.0, 1250.0], [796.5, 914.9, 1249.9], [791.9, 914.4, 1249.4], [787.1, 912.8, 1247.8], [782.8, 911.1, 1246.1], [778.0, 910.2, 1245.2], [773.1, 910.0, 1245.0], [768.1, 910.0, 1245.0], [763.1, 910.0, 1245.0], [758.2, 910.0, 1245.0], [753.2, 910.0, 1245.0], [748.2, 910.0, 1245.0], [743.2, 910.0, 1245.0], [738.2, 910.0, 1245.0], [733.2, 910.0, 1245.0], [728.3, 910.0, 1244.7], [723.1, 910.0, 1244.1], [718.4, 910.0, 1243.5], [713.1, 910.0, 1244.1], [709.3, 910.0, 1247.1], [706.9, 910.0, 1251.3], [704.0, 910.0, 1255.6], [700.8, 910.0, 1259.2], [697.3, 910.0, 1262.8], [694.3, 910.0, 1267.0], [692.5, 910.0, 1271.8], [692.0, 910.0, 1276.6], [692.0, 910.0, 1281.6], [692.0, 910.0, 1286.6], [692.0, 910.0, 1291.6], [692.1, 910.0, 1296.5], [692.7, 910.4, 1301.6], [693.8, 911.4, 1306.3], [694.7, 912.7, 1311.0], [694.9, 913.7, 1315.9], [694.5, 914.0, 1320.6], [692.9, 914.1, 1325.4]],
              'black': [[831.9, 914.9, 1255.0], [826.9, 915.0, 1255.0], [822.0, 915.0, 1255.0], [816.5, 915.0, 1255.0], [811.5, 915.0, 1255.0], [806.5, 915.0, 1255.0], [801.5, 915.0, 1255.0], [796.5, 915.0, 1255.0], [791.5, 915.0, 1255.0], [786.5, 915.0, 1255.0], [781.5, 915.0, 1255.0], [776.5, 915.0, 1255.0], [771.5, 915.0, 1255.0], [766.6, 915.0, 1255.0], [761.6, 915.0, 1255.0], [756.6, 915.0, 1255.0], [751.6, 915.0, 1255.0], [746.6, 915.0, 1255.0], [741.7, 915.0, 1254.8], [736.6, 915.0, 1253.9], [732.5, 915.0, 1251.8], [728.3, 915.0, 1248.5], [724.4, 915.0, 1245.9], [719.6, 915.0, 1244.2], [714.7, 915.0, 1244.0], [710.2, 915.0, 1246.2], [707.8, 915.0, 1250.5], [705.7, 915.3, 1255.1], [703.0, 916.2, 1259.1], [700.5, 917.7, 1263.1], [699.4, 918.7, 1267.7], [700.0, 918.8, 1273.1], [701.8, 918.3, 1277.6], [703.7, 917.5, 1282.1], [704.8, 917.1, 1287.0], [705.0, 917.0, 1291.9], [705.0, 917.0, 1296.9], [705.0, 917.0, 1301.9], [705.0, 917.0, 1306.8], [704.9, 917.0, 1311.8], [704.5, 917.0, 1316.6], [703.5, 916.7, 1321.6], [701.9, 915.9, 1326.6]]}
POT_ASIDE = {c: pot_plugged(c, cap, e, F1_ASIDE, ASIDE_WAY[c]) for c, cap, _, e, _ in POT_LEADS}
g.place('Move F1, still face down, further out in front of the case and along towards its other end, out of the way of the LCD screen.',
        ride={F1: F1_ASIDE, POT: F1_ASIDE}, **STAY, lines=False, eye=[dict(id=F1, **near('up-left'))], wires_done={f'pot {c}': POT_ASIDE[c] for c in POT_ASIDE},
        **frame_on(np.vstack([corners(F1, F1_DOWN), corners(F1, F1_ASIDE), corners(F9)]), [0.55, 0.62, 0.56], margin=4.0))

# F4: lifted over the frame (the switch's leads re-routed, the CAD's), then lowered onto the tabs of the F7s and F9.
SW_OVER = {c: W.route(cad_line(k, cap)[::-1], a=SWITCH, b=cap, a_at=HOVER_F4, stretch=True) for (c, cap, _, _), k in zip(SWITCH_LEADS, ('NAUO149', 'NAUO148', 'NAUO147'))}
g.place('Lift F4, with the switch, over the frame.', ride={F4: HOVER_F4}, lines=False, eye=[dict(id=F4, **near('down-left'))],
        wires_done={f'switch {c}': [SW_OVER[c], SW_OVER[c]] for c, *_ in SWITCH_LEADS}, **CASE_CAMERA)
F4_LINES = [[659.0, 957.8, 1233.3], [692.0, 957.8, 1232.9], [697.5, 957.8, 1355.4], [712.2, 954.7, 1356.1]]   # (the tops of the F7s' and F9's tabs: Lee, 20 Oct 2026)
# Each lead's way from the seated switch down to its hole, clear of the others and of the jumpers (found by a path search through
# the closed case, kept as control points).
SW_SEATED_WAY = {'red': [[669.0, 921.7, 1263.0], [666.9, 920.0, 1266.0], [665.1, 918.5, 1269.2], [663.2, 917.3, 1272.8]],
                'tan': [[685.0, 921.7, 1262.1], [687.9, 919.6, 1264.4], [690.5, 917.8, 1266.2], [693.7, 916.1, 1268.1]],
                'black': [[682.1, 919.2, 1257.5], [679.2, 917.0, 1259.1], [676.3, 915.7, 1261.5], [673.4, 915.1, 1263.6], [669.8, 914.8, 1265.6], [666.3, 914.5, 1267.3]]}
SW_SEATED = {c: W.route(into_hole(cap, exit_, [0, -1, 0], SW_SEATED_WAY[c]), a=SWITCH, b=cap, stretch=True) for c, cap, _, exit_ in SWITCH_LEADS}
g.place('Lower F4 onto the tabs of the F7s and F9.', move=[F4], path=[HOVER_F4, ZERO], lines_at=F4_LINES,
        wires_done={f'switch {c}': SW_SEATED[c] for c in SW_SEATED}, **CASE_CAMERA)
g.place('Slide F8 into the slots in F4 and F3 from the front.', move=[F8], direction=[1, 0, 0], hover=94,   # (published: 94.2 mm)
        labels=[dict(id=F8, text='F8', side='up-right')],
        view_dir=[0.4502, 0.5391, 0.7119], frame=([703.91, 927.27, 1307.02], 97.1))   # (Lee's screenshot, solved: round2/cameras.md)

# The LCD into the case (Steps 51, 52 published; Lee, 20 Oct 2026: "the subtleties of how the LCD Display moves into the slots on F9
# and F8"; Lee, 21 Oct 2026, Step 50: "slide into F8's slots along its length", "the left end of the display rotate up and over the
# wire / header end instead of flipping under", "a slightly more zoomed in view"). Step 50, a beat each: stood on its header (F9) end,
# face to the front, its other end raised; tipped over that end, so that it stands upright, its F8 end angled in 14 degrees, 20 mm out
# in front of the case; moved in, its board 9 mm short of F8; slid 12 mm along its own length until the board's end is in F8's notches
# (the published angled pose, without its 2.14 mm lift, which put the LCD's top into F4's underside). Step 51: straightened, pushed
# 14.9 mm further through F8's notches, and slid back 14.9 mm into F9's notches. The first two poses are written about the board's F9
# end, so that the player turns the LCD about that end (it turns a part about the pose's `at`: player.js mixPose): the header end stays
# by its wires while the other end goes up and over it. Moved in sideways (the last version), the board's ends went through the front
# of F8 above and below its window. Its wires stay behind F9: the run from the breadboard round F9's back edge is the seated CAD wire's
# in every shape, and from there each wire runs along F9's far face to the header, turning in to its cap on a 6 mm radius.
LCD_ANGLE_AT = [723.37, 921.6, 1265.11]                             # the upright the LCD is turned about: 3 mm in front of F8, at its notch
LCD_ANGLED = turned([0, 1, 0], 14.0, LCD_ANGLE_AT)                  # (published: 14.0 degrees)
LCD_F9_END = [712.96, 919.52, 1360.22]                              # the middle of the end of the LCD's board by its header, seated
LCD_ALONG = np.array([np.sin(np.radians(14.0)), 0.0, np.cos(np.radians(14.0))])   # the angled LCD's length, from its F8 end to its F9 end
LCD_IN = tidy(turned([0, 1, 0], 14.0, LCD_ANGLE_AT, (LCD_ALONG * 12.0).round(3).tolist()))   # angled, in the case, 12 mm back along its
                                                                    # length: the board's end 9 mm short of F8 (its ends clear of F8 as it comes in)
LCD_OUT = tidy(compose([20.0, 0.0, 0.0], LCD_IN, LCD_F9_END))       # ... 20 mm out in front of the case (clear of F4's front edge as it tips over)
LCD_ON_END = tidy(turned([1, 0, 0], 90.0, LCD_F9_END, (posed_line(LCD_OUT, [LCD_F9_END])[0] + [0.0, -8.0, 4.0] - LCD_F9_END).round(3).tolist()))
                                                                    # stood on its F9 end, face to the front, 8 mm lower and 4 mm further out


def lcd_hook(colour, fem, pose, radius=6.0, reach=6.0):
    """The last two control points of an LCD wire coming in to its female cap with the LCD at `pose`: a quarter turn of `radius` mm onto
    the cap's axis, `reach` mm out from the cap (lcd_tail goes on from there into it), so that the wire does not kink as it turns in."""
    end, out = fem_end(fem, pose)
    b = end + out * reach
    h = b - LCD_HEAD[colour][-1]
    h = unit(h - out * (h @ out))                                   # (the way the wire comes in, square to the cap)
    return [b - radius * h + radius * out, b - radius * h + radius * (out + h) / np.sqrt(2)]


LCD_LEADS = {}
for colour, male, _, fem, _, _, standing_key, seated_key in LCD_WIRES:
    seated = lcd_line(seated_key, male, fem, None)
    head = LCD_HEAD[colour]                                         # (the shared run: on to just round F9's back edge)
    y = fem_end(fem)[0][1]                                          # (the wire's height at the header)
    tail = lambda pose, *controls, reach=6.0: lcd_lead(lcd_tail(head, fem, pose, [[700.0, y, 1364.0], *controls, *lcd_hook(colour, fem, pose)],
                                                                reach=reach), fem, male, pose, head[-1])
    LCD_LEADS[colour] = dict(
        on_end=tail(LCD_ON_END, [722.0, y - 12.0, fem_end(fem, LCD_ON_END)[0][2] - 10.0]),   # (down under the header end and up into the caps)
        out=tail(LCD_OUT, [722.0, y, 1376.0]),
        inside=tail(LCD_IN, [714.0, y, 1374.0]),
        angled=tail(LCD_ANGLED, [712.0, y, 1368.5]),
        standing=lcd_lead(lcd_tail(head, fem, LCD_STANDING, [[697.0, y, 1362.0], [703.6, y, 1358.5]]), fem, male, LCD_STANDING, head[-1]),
        seated=lcd_lead(seated, fem, male, None, head[-1]))
LCD_IN_DIR = [0.62, 0.62, 0.48]                                     # (from the front at the breadboard's end, as before)
g.place('Stand the LCD screen up in front of the case, face to the front. Then move it in and slide it along until the end of its board '
        'goes into the slots in F8, its other end angled out in front of F9.', ride={LCD: [LCD_ON_END, LCD_OUT, LCD_IN, LCD_ANGLED]},
        ride_beats=True, lines=False, eye=[dict(id=LCD, **near('up-left'))],
        wires={f'lcd {c}': LCD_LYING_LEAD[c] for c, *_ in LCD_WIRES},   # (from LCD_PLAIN: the same points, an unseen swap)
        wires_done={f'lcd {c}': [LCD_LEADS[c][k] for k in ('on_end', 'out', 'inside', 'angled')] for c, *_ in LCD_WIRES},
        view_dir=LCD_IN_DIR, frame=([736.7, 938.8, 1396.5], 100.0))   # (the whole move, closer: Lee, 21 Oct 2026; was radius 130.6)
F9_NOTCHES = [[712.1, 947.3, 1359.5], [712.1, 892.6, 1359.5]]       # the end of the LCD's board, where it goes into F9's two notches (seated)
# (Step 51: straightened as it is pushed on through F8's notches, the board kept in the middle of them: through three poses between
# the angled one and the straight one, the board's line crossing F8's middle plane, z 1265.97, at x 713.02; straight from one to the
# other, turned about LCD_ANGLE_AT, the board's front face went 0.75 mm into the notches' front wall half way.)
LCD_STRAIGHTENING = [tidy(compose(turned([0, 1, 0], 14.0 * (1 - k), [712.96, 919.52, 1263.4 + 17.47 * k], [0.06, 0.4 * k, 2.57 - 17.47 * k]),
                                  [0.0, 0.0, 0.0], LCD_ANGLE_AT)) for k in (0.25, 0.5, 0.75)]
g.place("Straighten the LCD screen, pushing it on through the slots in F8, then slide it back until its board goes into the notches in F9.",
        move=[LCD], path=[LCD_ANGLED, *[via(p) for p in LCD_STRAIGHTENING], LCD_STANDING, ZERO], lines_at=F9_NOTCHES,
        wires_done={f'lcd {c}': [LCD_LEADS[c]['standing'], LCD_LEADS[c]['seated']] for c in LCD_LEADS},
        inset=dict(target=[713.1, 919.5, 1356.5], dir=[0.6, 0.3, 0.75], radius=34.0, marks=[([712.1, 947.3, 1356.5], 3.0), ([712.1, 892.6, 1356.5], 3.0)],
                   alt="Close-up of F9: the ends of the LCD screen's board in its two notches"),   # (as published, Step 52)
        view_dir=LCD_IN_DIR, frame=([705.0, 915.0, 1320.0], 110.0))

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
F1_SHARED = {c: F1_IN_WAY[c][1 if c == 'tan' else 2] for c in F1_IN_WAY}   # (where the two ways meet: on from there to the hole they are one)
POT_UP = {c: pot_plugged(c, cap, e, FRONT_OUT, F1_UP_WAY[c], F1_SHARED[c]) for c, cap, _, e, _ in POT_LEADS}
POT_IN = {c: pot_plugged(c, cap, e, None, F1_IN_WAY[c], F1_SHARED[c]) for c, cap, _, e, _ in POT_LEADS}
g.place('Stand F1 up in front of the case, the knob on the outside.', ride={F1: FRONT_OUT, POT: FRONT_OUT}, lines=False, eye=[dict(id=F1, **near('up-right', 0.035))],
        wires_done={f'pot {c}': [POT_UP[c]] * 1 for c in POT_UP}, view_dir=[0.62, 0.55, -0.56], frame=([720.0, 915.0, 1270.0], 120.0))
F1_LINES = [[[721.0, 886.1, 1321.6], [723.8, 886.1, 1321.6]], [[720.8, 886.1, 1258.1], [723.8, 886.1, 1258.1]],   # (F3's tabs, F4's at the
            [[720.9, 953.0, 1258.1], [723.8, 953.0, 1258.1]], [[721.0, 952.6, 1321.2], [727.2, 952.6, 1321.2]]]   # buzzer's end, F4's front tab:
                                                                    # Lee; from F1's back, as the others: 21 Oct 2026)
g.place('Push F1 onto the tabs of F4 and F3.', move=[F1, POT], path=[FRONT_OUT, ZERO], wires_done={f'pot {c}': POT_IN[c] for c in POT_IN}, lines_at=F1_LINES,
        view_dir=[0.62, 0.55, -0.56], frame=([720.0, 915.0, 1270.0], 120.0))

# The ends and the back, as published (Steps 55 - 57): F5 onto the end by the breadboard; F2's hooks into F5's slots with F2 swung out,
# then F2 swung shut over the tabs of F3 and F4, its slit sliding along the USB cable; F6 onto the other end, which locks them all.
# Lead lines from each slot (on the moving panel) to the tab that goes into it.
END_CAMERA = dict(view_dir=[0.82, 0.4, 0.42], frame=([683.0, 919.0, 1320.0], 115.0))   # (low, from the front, as published: from further round F5 hides its lines)
F5_TABS = [[722.33, 949.8, 1372.45], [722.33, 888.4, 1372.45], [663.68, 886.11, 1369.24], [701.78, 886.11, 1369.24]]   # F1's two hooks, F3's two tabs
g.place("Push F5 onto the end of the case by the breadboard: the tabs of F1, F3 and F4 go into its slots. Its engraved side faces out.", move=[F5],
        direction=[0, 0, 1], hover=56, lines_at=[[[x, y, 1366.07], [x, y, z]] for x, y, z in F5_TABS] + [[702.5, 952.7, 1369.2], [663.5, 952.5, 1369.2]],   # (+ F4's: Lee)
        labels={F5: 'F5'}, **END_CAMERA)   # (published: 56.0 mm)
F2_HOOKS = [[643.13, 949.8, 1372.45], [643.13, 888.4, 1372.45]]    # the hooks at F2's end by F5
g.place("Turn the case so its back faces you. Hook the tabs at the slit end of F2 into the slots in F5, its engraved side facing out and "
        "its other end swung out, then swing F2 shut onto the tabs of F3 and F4.", move=[F2], path=[swung(F2_OFF), swung(F2_HOOK), swung(), ZERO],
        lines_at=[[h, [h[0], h[1], 1366.07]] for h in F2_HOOKS], labels=[dict(id=F2, text='F2', **near('near-right', 0.08))], eye=[dict(anchor=[643.13, 889.0, 1339.4], id=F2, **near('near-below'))],   # (the cable in the slit)
        inset=dict(target=NOTCH.round(2).tolist(), dir=[-0.9, 0.35, -0.25], radius=14.0, mark=4.0, alt='The USB cable in the slit at the bottom of F2'),
        caution='The USB cable must sit in the slit at the bottom of F2.', wires_done={'usb cable': [usb_cable()['usb cable'], usb_cable(f2=swung())['usb cable'],
                                                                                        usb_cable(f2=ZERO)['usb cable']]},   # (the cable follows the slit)
        view_dir=[-0.7, 0.5, -0.5], frame=([640.0, 915.0, 1290.0], 125.0))   # (F2 swung out, whole, in frame)
F6_TABS = [[722.33, 949.8, 1207.29], [722.33, 888.4, 1207.29], [643.13, 949.8, 1207.29], [643.13, 888.4, 1207.29]]   # F1's and F2's hooks
g.place("Push F6 onto the other end of the case: the tabs of F1, F2, F3 and F4 go into its slots. Its engraved side faces out.", move=[F6],
        direction=[0, 0, -1], hover=67.5, lines_at=[[[x, y, 1213.67], [x, y, z]] for x, y, z in F6_TABS], labels=[dict(id=F6, text='F6', **near('down-right', 0.065))],
        view_dir=[0.5, 0.55, -0.67], frame=([683.0, 919.0, 1250.0], 110.0))   # (published: 67.5 mm)
# ================================================================ THE CASE (end)

g.build()
