"""Laser Stem Matrix (LSM), full build: the electronics on the open base, the housing closed round them, the LED matrix hung inside
on its supports, the three shelves on their posts, and the 64 LED stems. The build, in order.

Run from the project root:   python "LSM Build Instructions/guide.py"
It writes steps.json (what the player shows) and parts.json (the parts list).

First draft (19 Oct 2026). The order, the wiring and the moves follow TechBox's published Cadasio guide for the kit
(instructions.online, 19075-laser_stem_matrix_lsm_-_full_build: docs/research/lsm/cadasio_study.md), 38 numbered steps, put right
where the house rules say otherwise (one wire per step: the button's two leads are two steps; a check step where the published
guide leaves the posts short). The model is lsm.glb, put back together by assemble.py from Lee's part files and the published
guide's assembly (Lee's assembly STEP is broken); the part ids are the names assemble.py gives (D1 ... D11 as engraved).
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
import wires as W  # noqa: E402
from stepgen import Guide, apply_pose, compose, relative_pose, turn_dir, turned, via  # noqa: E402

ZERO = [0.0, 0.0, 0.0]

# ---------------------------------------------------------------- parts (ids: assemble.py)
D1, D2, D3, D4, D5, D6, D7, D8, D10 = 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D10'
D9_A, D9_B = 'D9_A', 'D9_B'                                         # the wide LED supports: D9_A nearer D4, D9_B nearer D5
D11_A, D11_B, D11_C, D11_D = 'D11_A', 'D11_B', 'D11_C', 'D11_D'      # shelf posts: A, B at D5's side (D2's end, D3's end), C, D at D4's
BREADBOARD, BACKING, NANO = 'BREADBOARD', 'BACKING', 'NANO'
R12K, R330, CAP, MATRIX = 'R12K', 'R330', 'CAP', 'MATRIX'
BUTTON, NUT, RED_PIN, BLACK_PIN = 'BUTTON', 'NUT', 'BTN_RED_PIN', 'BTN_BLACK_PIN'   # the push button, its nut, the pins on its two leads
USB_B, USB_A = 'USB_B', 'USB_A'                                     # the USB cable's right-angle Mini-B plug and its A end
JUMPERS = ['white', 'grey', 'purple']                               # the three-wire jumper ribbon, in ribbon order
MALE = {w: f'J_{w.upper()}_M' for w in JUMPERS}                     # each wire's pin (into the breadboard) ...
FEMALE = {w: f'J_{w.upper()}_F' for w in JUMPERS}                   # ... and socket (onto the LED matrix's pins)
STEMS = [f'STEM_{k:02d}' for k in range(1, 65)]
WALLS = [D2, D3, D4, D5]

# The engraved codes are the student's names for the wood. The housing's sides, after the published guide's tooltips: D2 left (the
# button's), D3 right, D4 rear (the USB cable's), D5 front. In assembly space D2 is at +Z, D3 at -Z, D4 at -X, D5 at +X.
NAMES = {D1: 'D1', D2: 'D2', D3: 'D3', D4: 'D4', D5: 'D5', D6: 'D6', D7: 'D7', D8: 'D8', D9_A: 'D9', D9_B: 'D9', D10: 'D10',
         D11_A: 'D11', D11_B: 'D11', D11_C: 'D11', D11_D: 'D11',
         BREADBOARD: 'Breadboard', NANO: 'Nano Board', R12K: '12 kΩ Resistor', R330: '330 Ω Resistor', CAP: 'Capacitor', MATRIX: 'LED Matrix',
         BUTTON: 'Push Button', USB_B: 'USB Cable', USB_A: 'USB Cable', **{s: 'LED Stem' for s in STEMS},
         **{MALE[w]: 'Breadboard Wire (M-F)' for w in JUMPERS}, **{FEMALE[w]: 'Breadboard Wire (M-F)' for w in JUMPERS}}
PART_OF = {BACKING: BREADBOARD, NUT: BUTTON, RED_PIN: BUTTON, BLACK_PIN: BUTTON}   # (the backing comes on the breadboard; the nut and the leads on the button)
UNLISTED = [USB_A] + list(MALE.values()) + list(FEMALE.values())    # named on hover only (the USB cable is listed by its Mini-B plug; the jumper's caps by hand)
HOVER_NAMES = {MALE['white']: 'White Breadboard Wire', FEMALE['white']: 'White Breadboard Wire', MALE['grey']: 'Grey Breadboard Wire',
               FEMALE['grey']: 'Grey Breadboard Wire', MALE['purple']: 'Purple Breadboard Wire', FEMALE['purple']: 'Purple Breadboard Wire'}

# The parts list after the title page (as the MRA's and RCC's): one band per kind of part; the wood's bands blue-grey.
WOOD_BAND, WOOD_HALO = '#dbe4ef', '#8ea6c4'
PART_GROUPS = [
    ('Parts List', 'Electronics', 'electronics', '#f9c0c0', '#ec8d8d',
     lambda n: n in ('Breadboard', 'Nano Board', '12 kΩ Resistor', '330 Ω Resistor', 'Capacitor', 'Breadboard Wire (M-F)', 'LED Matrix', 'Push Button', 'USB Cable')),
    ('Parts List (Cont.)', 'Housing', 'wood', WOOD_BAND, WOOD_HALO, lambda n: n in ('D1', 'D2', 'D3', 'D4', 'D5')),
    ('Parts List (Cont.)', 'Supports and Shelves', 'wood', WOOD_BAND, WOOD_HALO, lambda n: n in ('D6', 'D7', 'D8', 'D9', 'D10', 'D11')),
    ('Parts List (Cont.)', 'Stems', 'wood', WOOD_BAND, WOOD_HALO, lambda n: n == 'LED Stem'),
]


def parts_list(parts):
    natural = lambda p: [int(t) if t.isdigit() else t for t in __import__('re').split(r'(\d+)', p['name'])]
    pages, used = {}, set()
    for page, title, icon, colour, halo, wanted in PART_GROUPS:
        items = [p for p in parts if p['name'] not in used and wanted(p['name'])]
        if not items:
            continue
        used.update(p['name'] for p in items)
        if icon == 'wood':
            items.sort(key=natural)
        for p in items:
            p['group'] = title
        pages.setdefault(page, []).append(dict(title=title, icon=icon, colour=colour, halo=halo,
                                               items=[dict(name=p['name'], qty=p['qty'], picture=p['picture']) for p in items]))
    left = [p for p in parts if p['name'] not in used]
    if left:
        pages.setdefault(list(pages)[-1] if pages else 'Parts List', []).append(
            dict(title='Other parts', icon='wood', colour='#e8e8e8', halo='#bdbdbd', items=[dict(name=p['name'], qty=p['qty'], picture=p['picture']) for p in left]))
    names = ['Parts List'] + [f"Parts List (Cont.{'' if k == 1 else f' {k}'})" for k in range(1, len(pages))]
    return [dict(name=name, groups=groups) for name, groups in zip(names, pages.values())]


# How the parts list pictures a part, where the generator's own view does not suit: the shelves' codes came out upside down.
PART_VIEWS = {'D6': {'roll': 180}, 'D7': {'roll': 180}, 'D8': {'roll': 180}}

g = Guide(HERE, title='Laser Stem Matrix (LSM)', part='Full Build', names=NAMES, part_of=PART_OF, unlisted=UNLISTED, hover_names=HOVER_NAMES, part_views=PART_VIEWS,
          source='lsm.glb', hero_azimuth=45, parts_list=parts_list,      # (the finished model from D5 and D2's corner, the button and the USB cable in view)
          copyright_line='© TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')
M = g.model.inst
box = lambda i: M[i].bounds
mid = lambda i: M[i].bounds.mean(0)
# The title page: the finished kit from D5 and D2's corner, framed on the box, closer and higher in the frame than the finished model's
# own camera (Lee, 19 Oct 2026: "a little low and could be zoomed in a bit more"), without the USB cable (as the MRA's title page).
# The Completed View keeps the first draft's camera, with the USB cable.
HERO_DIR = [0.5997, 0.5299, 0.5997]
g.start_view = dict(dir=HERO_DIR, target=[638.5, 898.5, 1204.5], radius=84.0, hide=[USB_A, USB_B])
g.end_view = dict(dir=HERO_DIR, target=[602.9, 912.5, 1204.3], radius=114.1)

# ---------------------------------------------------------------- the breadboard's holes (assembly mm; as assemble.py)
ROW_X = dict(zip('abcdefghij', [624.50, 627.04, 629.58, 632.12, 634.66, 642.46, 645.00, 647.54, 650.08, 652.62]))
COL1_Z, PITCH, BOARD_TOP, TABLE_Y = 1167.91, 2.54, 871.92, 856.23   # (the box stands on its walls' feet: the table is at y 856.23)


def hole(name, y=BOARD_TOP):
    return [ROW_X[name[0]], y, COL1_Z + (int(name[1:]) - 1) * PITCH]


def r1_camera(d, target, radius):
    """A step's camera as the first draft had it, where a change elsewhere (the USB cable's A end moved out, a new camera on the step
    before) would otherwise move it unasked."""
    return dict(view_dir=d, frame=(target, radius))


DIAG = [-0.5792, 0.5736, -0.5792]                                    # (the first draft's usual corner: D4 and D3's)


def hole_label(name, part=BREADBOARD):
    return dict(id=part, text=name, anchor=hole(name))


# ---------------------------------------------------------------- wires
def smooth(start, start_dir, end, end_dir, mids=(), lead=3.0, spacing=0.5):
    """A smooth line from `start` (leaving along start_dir) through `mids` into `end` (arriving along end_dir), with a short straight
    run at each end (a wire leaves a pin or a housing straight)."""
    start, end = np.asarray(start, float), np.asarray(end, float)
    sd, ed = W._unit(start_dir), W._unit(end_dir)
    a, b = start + sd * lead, end - ed * lead
    body = W.smooth([a, *[np.asarray(m, float) for m in mids], b], start_dir=sd, end_dir=ed, spacing=spacing)
    return W.resample(W.join(W.straight(start, sd, lead), body, W.straight(b, ed, lead)), 0.75)


CLEAR_OF = [i for i in M if not i.startswith('STEM_')]


def check(route_pts, radius, near_ends=(), skip=(), name=''):
    """Log where a wire passes into a part (its middle within its radius of a part's surface, away from its own ends)."""
    pts = np.asarray(route_pts, float)
    L = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    inner = pts[(L > 4.0) & (L < L[-1] - 4.0)]
    if not len(inner):
        return
    for i in CLEAR_OF:
        if i in skip:
            continue
        lo, hi = box(i)
        sel = inner[np.all((inner > lo - radius) & (inner < hi + radius), axis=1)]
        if not len(sel):
            continue
        d = M[i].nearest.on_surface(sel)[1]
        if (d < radius * 0.8).any():
            g.log.append(f'  WIRE {name}: within {d.min():.2f} mm of {i} at {sel[d.argmin()].round(1).tolist()}')


# --- resistor legs: drawn as wires so that they can be bent (Steps 4 and 7). Each leg leaves the body's end along its axis; bent,
# it runs on to above its hole and turns straight down, its tip 2.8 mm below the board's top (as the published model has it).
# Drawn with a ring every 0.25 mm (the player's default, one every 1.5 mm, made the bends look pinched: Lee, 19 Oct 2026), and bent
# through 30 and 60 degrees on the way, each shape as long as the straight leg, so that the leg swings round rather than shrinking.
LEG_R, LEG_RINGS = 0.31, 0.25


def legs(body, holes, name):
    lo, hi = box(body)
    c = mid(body)
    ids = [f'{name} leg {k}' for k in (1, 2)]
    straight_, bent = {}, {}
    for wid, end_z, h, sign in ((ids[0], lo[2] + 0.4, holes[0], -1), (ids[1], hi[2] - 0.4, holes[1], 1)):
        g.wire(wid, 'pin', LEG_R, name=NAMES[body])
        start = np.array([c[0], c[1], end_z])
        tip = np.array([c[0], BOARD_TOP - 2.8, hole(h)[2]])
        corner = np.array([c[0], c[1], tip[2]])
        line = W.rounded([start, corner, tip], radius=1.2, spacing=0.25)
        n = W.length(line)
        shapes = []
        for deg in (30.0, 60.0):                                     # (the same length: the far end swings down on a circle)
            a = np.radians(deg)
            down = np.array([0.0, -np.sin(a), sign * np.cos(a)])
            run = abs(corner[2] - start[2])
            part = W.rounded([start, corner, corner + down * (n - run)], radius=1.2, spacing=0.25)
            shapes.append(W.route(part, a=body, spacing=LEG_RINGS))
        bent[wid] = [*shapes, W.route(line, a=body, spacing=LEG_RINGS)]
        straight_[wid] = W.route(W.straight(start, [0, 0, sign], n), a=body, spacing=LEG_RINGS)
        check(line, LEG_R, skip=(body,), name=wid)
    return straight_, bent


R12K_STRAIGHT, R12K_BENT = legs(R12K, ('h3', 'h16'), '12k')
R330_STRAIGHT, R330_BENT = legs(R330, ('a11', 'a19'), '330')
for _body, _legs in ((R12K, R12K_STRAIGHT), (R330, R330_STRAIGHT)):     # (pictured with their legs straight, as they come)
    g.part_picture(NAMES[_body], wires=[dict(colour='pin', radius=LEG_R, pts=r['pts']) for r in _legs.values()])

# --- the jumper ribbon: three wires, each a pin (into the breadboard) and a socket (onto the LED matrix). A pin stands in its hole,
# its wire leaving the top of its housing (y 879.92) straight up; a socket lies on its pin under the LED matrix's corner, its wire
# leaving its far end along +Z (as built), towards the middle of the matrix.
JUMPER_R = 0.62
JUMPER_HOLES = dict(white='i2', grey='i3', purple='b19')            # V+ (to VIN), V- (to GND), IN (from D7 through the 330 Ω resistor)
MATRIX_PINS = dict(white='V+', purple='IN', grey='V-')              # (the published guide's badges: V+, "V-In", V-)
for w in JUMPERS:
    g.wire(f'wire {w}', f'wire_{w}', JUMPER_R, name='Breadboard Wire (M-F)')
M_EXIT = {w: np.array([hole(JUMPER_HOLES[w])[0], 879.92, hole(JUMPER_HOLES[w])[2]]) for w in JUMPERS}
F_EXIT = {w: np.array([mid(FEMALE[w])[0], mid(FEMALE[w])[1], box(FEMALE[w])[1][2]]) for w in JUMPERS}
F_TIP = {w: np.array([mid(FEMALE[w])[0], mid(FEMALE[w])[1], box(FEMALE[w])[0][2]]) for w in JUMPERS}   # (its open end, on the pin)

# The LED matrix's places, as the published guide has them (each relative to its seat, about its middle): over the breadboard for
# its wires (Steps 13 - 15, turned half round); lying beside the base (Steps 19 - 24); outside D4 while the box is closed round the
# breadboard (24c - 28); held over the box (28c - 30); in the box.
MC = mid(MATRIX).round(2).tolist()
P_OVER = turned([0, 1, 0], 180.0, MC, [0.49, 21.76, 14.14])
P_BESIDE = turned([0, 1, 0], 180.0, MC, [91.01, -21.66, 11.37])
P_OUTSIDE = turned([0, 1, 0], 180.0, MC, [-90.76, 5.89, 25.09])
P_HELD = [-0.2, 56.64, -0.32]
SOCKET_OFF = [0.0, 0.0, 15.0]                                       # a socket held 15 mm off its pin, in line with it (Steps 10 - 15)


def f_pose(w, matrix_pose, off=ZERO):
    """Where socket w is when the LED matrix is at matrix_pose (and the socket `off` from its pin)."""
    return compose(matrix_pose, off, mid(FEMALE[w]).tolist()) if (matrix_pose != ZERO or off != ZERO) else ZERO


def f_end(w, pose):
    """The socket's wire end and the way its wire leaves it, with the socket at `pose`."""
    return apply_pose(pose, [F_EXIT[w]])[0], turn_dir(pose, [0, 0, 1])


PIN_HOVER = [0.0, 30.0, 0.0]                                        # a pin held 30 mm over its hole (Steps 10 - 12)


def m_end(w, pose):
    return apply_pose(pose, [M_EXIT[w]])[0], turn_dir(pose, [0, 1, 0])


def jumper(w, m_pose, f_pose_, mids=(), skip=(), lead=3.0):
    a, ad = m_end(w, m_pose)
    b, bd = f_end(w, f_pose_)
    line = smooth(a, ad, b, -bd, mids, lead=lead)
    check(line, JUMPER_R, skip=(MALE[w], FEMALE[w], *skip), name=f'wire {w}')
    return {f'wire {w}': W.route(line, a=MALE[w], b=FEMALE[w], a_at=m_pose if m_pose != ZERO else None,
                                 b_at=f_pose_ if f_pose_ != ZERO else None, stretch=True)}


# ---------------------------------------------------------------- the build
# ================================================================ PART 1: THE BREADBOARD (begin)
# The breadboard first, on its own, held 49 mm up (where it waits for D1, as in the published guide); its protective backing
# peeled off and set aside.
BOARD_UP = [0.0, 49.0, 0.0]
g.rest_at([BREADBOARD], BOARD_UP)
g.carry([BACKING], by=BREADBOARD)
_bb = box(BREADBOARD)
g.place('Peel the protective backing off the bottom of the breadboard.', appear=[BREADBOARD], ride={BACKING: [0.0, -40.0, 0.0]}, lines=False,
        labels={BREADBOARD: 'Breadboard'},
        # (Longer, at the corner nearest the camera, so that it shows under the breadboard: Lee, 19 Oct 2026.)
        arrows=[dict(tail=[_bb[0][0] + 4.0, _bb[0][1] - 1.0, _bb[0][2] + 4.0], head=[_bb[0][0] + 4.0, _bb[0][1] - 46.0, _bb[0][2] + 4.0],
                     normal=[-0.7071, 0, -0.7071], part=BACKING, width=4.0)])
g.put_away([BACKING])
# D1 appears in place; the breadboard (sticky side down) is pressed onto it, between its corner marks.
CORNERS = [[x, 862.4, z] for x in (_bb[0][0] + 1.0, _bb[1][0] - 1.0) for z in (_bb[0][2] + 1.0, _bb[1][2] - 1.0)]
g.place('Press the breadboard, sticky side down, onto D1 between its corner marks.', move=[BREADBOARD], show=[D1], path=[BOARD_UP, ZERO],
        labels={D1: 'D1'}, lines_at=CORNERS)
# The Nano Board straddles the middle of the breadboard: its pins in rows c and g, from column 2 to column 16, its USB socket at
# column 16 (pin D12 in c16, as Part 1 of the published guide has it).
NANO_PINS = [[ROW_X[r], 865.9, COL1_Z + (c - 1) * PITCH] for r in 'cg' for c in (2, 16)]
g.place('Press the Nano Board into the breadboard: its pins in rows c and g, from column 2 to column 16, with its USB socket at column 16.',
        move=[NANO], direction=[0, 1, 0], hover=35, labels=[hole_label('c16'), hole_label('g2')],
        lines_at=[[p, [p[0], BOARD_TOP, p[2]]] for p in NANO_PINS],
        view_dir=[-0.5792, 0.5736, -0.5792], frame=([638.6, 888.0, 1192.0], 50.0))   # (closer, for the holes: Lee, 19 Oct 2026)
# The resistors: each one's legs bent on its own first, then into its holes.
g.place('Bend both legs of the 12 kΩ resistor (brown, red, black, red, brown) straight down.', show=[R12K], staged=True, lines=False, frame=(mid(R12K).tolist(), 24.0),
        labels={R12K: '12 kΩ Resistor'}, eye=[R12K], wires=R12K_STRAIGHT, wires_done=R12K_BENT)
# (From the corner on the other side of the Nano Board, which hid the holes, and closer: Lee, 19 Oct 2026.)
g.seat('Push the 12 kΩ resistor into h3 and h16.', [R12K], direction=[0, 1, 0], hover=32,
       labels=[hole_label('h3'), hole_label('h16')], lines_at=[hole('h3'), hole('h16')],
       view_dir=[0.5792, 0.5736, -0.5792], frame=([647.5, 886.0, 1189.5], 30.0))
# The capacitor's polarity first, on its own, with a close-up of its grey stripe (Lee, 19 Oct 2026, after the published guide's
# Capacitor card): the stripe runs down the side over the negative leg, which goes to GND. Then it goes in, seen from further round
# so that the stripe and j3 show.
STRIPE = [653.57, 878.67, 1174.02]                                  # the middle of the grey stripe (it faces +Z, towards j3)
CAP_LEG = dict(gnd=[652.62, 868.0, 1172.97], plus=[652.62, 868.0, 1170.47])   # its legs, low down: into j3 and j2
CAP_VIEW = [0.346, 0.574, 0.742]                                   # (25 degrees round from j3's side: the stripe and j3 both show)
g.place('The capacitor has a negative (-) leg and a positive (+) leg. The grey stripe down its side marks the negative leg, which goes to GND.',
        show=[CAP], staged=True, single=True, lines=False, view_dir=[-0.646, 0.259, 0.718], frame=([653.6, 874.0, 1172.0], 13.0),   # (the stripe and both legs)
        labels=[dict(id=CAP, text='GND (-)', anchor=CAP_LEG['gnd']), dict(id=CAP, text='+', anchor=CAP_LEG['plus'])], eye=[dict(id=CAP, anchor=STRIPE)],
        inset=dict(target=STRIPE, dir=[-0.21, 0.15, 0.966], radius=4.5, mark=2.0, caption='Grey stripe: the negative (-) leg, to GND',
                   alt='Close-up of the grey stripe down the side of the capacitor'))
g.seat('Push the capacitor into j2 and j3, its grey stripe in j3.', [CAP], direction=[0, 1, 0], hover=29,
       labels=[hole_label('j3'), hole_label('j2')], lines_at=[hole('j2'), hole('j3')], eye=[dict(id=CAP, anchor=STRIPE)],
       caution="The capacitor's grey stripe marks its negative (-) leg, which goes in j3 (the Nano Board's GND).",
       view_dir=CAP_VIEW, frame=([652.6, 885.0, 1172.0], 28.0))
g.place('Bend both legs of the 330 Ω resistor (orange, orange, black, black, brown) straight down.', show=[R330], staged=True, lines=False, frame=(mid(R330).tolist(), 18.0), view_dir=DIAG,
        labels={R330: '330 Ω Resistor'}, eye=[R330], wires=R330_STRAIGHT, wires_done=R330_BENT)
g.seat('Push the 330 Ω resistor into a11 and a19.', [R330], direction=[0, 1, 0], hover=30,
       labels=[hole_label('a11'), hole_label('a19')], lines_at=[hole('a11'), hole('a19')],
       view_dir=[-0.5792, 0.5736, -0.5792], frame=([624.5, 886.0, 1203.5], 30.0))   # (closer, for the holes: Lee, 19 Oct 2026)
# ================================================================ PART 1 (end)

# ================================================================ PART 2: THE LED MATRIX'S WIRES (begin)
# The jumper ribbon on its own: three wires side by side, white, grey, purple; their ends pulled apart. (The white wire's pin is the
# one the others are laid out from: they ride on it here.)
RIB_X, RIB_Y, RIB_Z, RIB_LEN = 700.0, 925.0, 1100.0, 80.0           # the ribbon on its own: lying along X, pins at +X
RIB_PITCH, RIB_SPREAD = 1.9, 6.0


def lying_pin(w, z):
    """A pin lying along X, its pin pointing +X and its wire leaving at x = RIB_X."""
    return turned([0, 0, 1], 90.0, M_EXIT[w].tolist(), (np.array([RIB_X, RIB_Y, z]) - M_EXIT[w]).round(3).tolist())


def lying_socket(w, z):
    """A socket lying along X at the ribbon's far end, its open end pointing -X."""
    return turned([0, 1, 0], 90.0, F_EXIT[w].tolist(), (np.array([RIB_X - RIB_LEN, RIB_Y, z]) - F_EXIT[w]).round(3).tolist())


joined_z = {w: RIB_Z + k * RIB_PITCH for k, w in enumerate(JUMPERS)}
split_z = {w: RIB_Z + k * RIB_SPREAD for k, w in enumerate(JUMPERS)}   # (the white pin, which the others ride on, stays where it is)
RIBBON = {w: dict(m=lying_pin(w, joined_z[w]), f=lying_socket(w, joined_z[w]), ms=lying_pin(w, split_z[w]), fs=lying_socket(w, split_z[w])) for w in JUMPERS}


def ribbon_wire(w, split):
    a, ad = m_end(w, RIBBON[w]['ms' if split else 'm'])
    b, bd = f_end(w, RIBBON[w]['fs' if split else 'f'])
    if split:                                                        # (joined in the middle, the ends spread over 15 mm)
        za, zb, zj = a[2], b[2], joined_z[w]
        mids = [[a[0] - 30.0, a[1], zj], [b[0] + 30.0, b[1], zj]]
    else:
        mids = []
    return {f'wire {w}': W.route(smooth(a, ad, b, -bd, mids), a=MALE[w], b=FEMALE[w], a_at=RIBBON[w]['ms' if split else 'm'],
                                 b_at=RIBBON[w]['fs' if split else 'f'], stretch=True)}


# The ribbon in the parts list: one wire of the three, its pin and socket lying as in Step 9 with the wire straight between them.
_wm, _wf = m_end('white', RIBBON['white']['m'])[0], f_end('white', RIBBON['white']['f'])[0]
g.list_part('Breadboard Wire (M-F)', [MALE['white'], FEMALE['white']], 3, after='Capacitor')
g.part_picture('Breadboard Wire (M-F)', poses={MALE['white']: RIBBON['white']['m'], FEMALE['white']: RIBBON['white']['f']},
               wires=[dict(colour='wire_purple', radius=JUMPER_R, pts=np.linspace(_wm, _wf, 40))])
carrier = MALE['white']
g.rest_at([carrier], RIBBON['white']['m'])
_cpose = RIBBON['white']['m']
for w in JUMPERS:
    if MALE[w] != carrier:
        g.carry([MALE[w]], by=carrier, pose=relative_pose(_cpose, RIBBON[w]['m'], mid(MALE[w]).tolist()))
    g.carry([FEMALE[w]], by=carrier, pose=relative_pose(_cpose, RIBBON[w]['f'], mid(FEMALE[w]).tolist()))
split_ride = {MALE[w]: relative_pose(_cpose, RIBBON[w]['ms'], mid(MALE[w]).tolist()) for w in JUMPERS if MALE[w] != carrier}
split_ride.update({FEMALE[w]: relative_pose(_cpose, RIBBON[w]['fs'], mid(FEMALE[w]).tolist()) for w in JUMPERS})
g.place('Pull apart both ends of the three-wire jumper ribbon, so that each wire can reach its own place.', show=[carrier], appear=[carrier], staged=True,
        lines=False, eye=[FEMALE['grey']], ride=split_ride,
        wires={k: v for w in JUMPERS for k, v in ribbon_wire(w, False).items()}, wires_done={k: v for w in JUMPERS for k, v in ribbon_wire(w, True).items()})
g.put_away(list(MALE.values()) + list(FEMALE.values()))

# Back to the breadboard: the pins held over their holes, the sockets held where the LED matrix's pins will be (Steps 13 - 15).
# One wire per step: its pin straight down into its hole.
for w in JUMPERS:
    g.rest_at([MALE[w]], PIN_HOVER)
    g.rest_at([FEMALE[w]], f_pose(w, P_OVER, SOCKET_OFF))
# The wires from the pins to the sockets held off the LED matrix's pins (and, ON_MIDS, on them): white and grey side by side, the
# purple wire passing under the grey one to its socket between the other two. With the pins still held up, the wires leave them
# higher, the white one over the grey one's pin.
LOOSE_MIDS = dict(white=[[659.0, 901.0, 1192.0], [667.5, 907.5, 1199.0], [669.8, 913.5, 1205.5]],
                  grey=[[655.0, 901.0, 1195.5], [662.0, 906.5, 1201.5], [664.7, 913.0, 1206.5]],
                  purple=[[640.0, 900.0, 1214.0], [660.0, 902.0, 1210.0], [666.8, 905.5, 1207.0], [667.2, 913.5, 1208.5]])
HOVER_MIDS = dict(white=[[651.0, 925.0, 1176.0], [662.0, 922.0, 1192.0], [667.5, 918.0, 1199.0], [669.8, 915.5, 1205.5]],
                  grey=[[651.0, 918.5, 1180.0], [657.0, 917.0, 1193.0], [662.0, 915.0, 1201.5], [664.7, 914.5, 1206.5]],
                  purple=[[634.0, 916.5, 1213.6], [652.0, 912.0, 1211.0], [664.0, 909.0, 1208.5], [667.0, 911.0, 1208.0]])
ON_MIDS = dict(white=[[659.0, 901.0, 1192.0], [669.5, 906.5, 1203.0], [671.0, 911.0, 1214.0], [670.4, 914.5, 1222.0]],   # (wide of the purple socket)
               grey=[[655.0, 901.0, 1195.5], [662.0, 906.5, 1209.0], [664.7, 913.0, 1220.0]],
               purple=[[640.0, 900.0, 1214.0], [660.0, 902.0, 1215.0], [666.8, 905.5, 1219.0], [667.2, 913.5, 1222.0]])


def loose(w, plugged):
    return jumper(w, ZERO if plugged else PIN_HOVER, f_pose(w, P_OVER, SOCKET_OFF), LOOSE_MIDS[w] if plugged else HOVER_MIDS[w])


wires_now = {k: v for w in JUMPERS for k, v in loose(w, False).items()}
# (Each from a corner where the hole is not hidden: i2 and i3 from beyond row j, b19 from beyond row a and the 330 Ω resistor's far
# end: Lee, 19 Oct 2026.)
PIN_CAMERA = dict(white=dict(view_dir=[0.5792, 0.5736, -0.5792], frame=([650.1, 892.0, 1172.0], 34.0)),
                  grey=dict(view_dir=[0.5792, 0.5736, -0.5792], frame=([650.1, 892.0, 1172.0], 34.0)),
                  purple=dict(view_dir=[-0.5792, 0.5736, 0.5792], frame=([627.0, 892.0, 1213.6], 34.0)))
plugged = []
for k, w in enumerate(JUMPERS):
    h = JUMPER_HOLES[w]
    g.place(f'Push the {w} wire\'s pin into {h}.', move=[MALE[w]], appear=list(MALE.values()) + list(FEMALE.values()) if k == 0 else (),
            path=[PIN_HOVER, ZERO], lines=False, labels=[hole_label(h)], eye=[MALE[w]],
            wires=wires_now if k == 0 else None, wires_done=loose(w, True), **PIN_CAMERA[w])
    plugged.append(w)

# The LED matrix comes in over the breadboard, turned half round, its three pins towards the sockets; each socket goes onto its pin.
# (The card gives the pins their names; the sockets ride on the matrix from here on.)
g.put_away(list(FEMALE.values()))
# The LED matrix itself, turned over (Lee, 19 Oct 2026: "an actual visual of the LED Matrix", in place of the first draft's note card):
# its three pins, in a right-angle header lying flat at one corner of its back, and the label stuck beside them, V- IN V+. Seen from the
# side that reads the label upright.
PIN_X = dict(white=608.24, purple=610.78, grey=613.32)               # V+, IN, V- (assemble.py), 1.27 mm under the back face
PIN_Y, PIN_TIP_Z = 894.333, 1190.06
g.place('Find the three pins on the back of the LED matrix, at one corner: V+, IN and V-, named on the label beside them. '
        'The white wire goes on V+, the purple wire on IN and the grey wire on V-.',
        show=[MATRIX], staged=True, single=True, lines=False, flip=True, view_dir=[-0.18, -0.8, 0.57], frame=([628.0, 895.0, 1199.0], 36.0),
        labels=[dict(id=MATRIX, text=MATRIX_PINS[w], anchor=[PIN_X[w], PIN_Y, PIN_TIP_Z - 1.0]) for w in ('white', 'purple', 'grey')],
        eye=[dict(id=MATRIX, anchor=[610.78, 894.2, 1181.0])],
        inset=dict(target=[612.5, 894.5, 1191.0], radius=10.0, caption='V+, IN and V-, as the label names them', alt='Close-up of the three pins and the label'))
g.put_away([MATRIX])
g.rest_at([MATRIX], P_OVER)
for w in JUMPERS:
    g.carry([FEMALE[w]], by=MATRIX, pose=SOCKET_OFF, appear=False)
ON_PIN = {w: jumper(w, ZERO, f_pose(w, P_OVER), ON_MIDS[w]) for w in JUMPERS}
# (From the corner to the right of the first draft's, a little below the matrix and looking up at its pins: Lee, 19 Oct 2026. One
# camera for the three.)
_pins_over = apply_pose(P_OVER, [[PIN_X['purple'], PIN_Y, 1186.0]])[0]
PIN_VIEW = dict(view_dir=[0.757, -0.154, -0.635], frame=(_pins_over.round(1).tolist(), 30.0))
OFF_PIN = {k: v for w in JUMPERS for k, v in loose(w, True).items()}   # (the wires as Step 12 left them: put_away took them off with the sockets)
for k, w in enumerate(['white', 'purple', 'grey']):                # (in the order of the pins along the matrix's edge)
    g.place(f'Push the {w} wire\'s socket onto the {MATRIX_PINS[w]} pin of the LED matrix.', appear=[MATRIX] + list(FEMALE.values()) if k == 0 else (),
            ride={FEMALE[w]: ZERO}, lines=False,
            labels=[dict(id=MATRIX, text=MATRIX_PINS[w], anchor=F_TIP[w].round(2).tolist())], eye=[FEMALE[w]],   # (anchors are on the part, as built)
            wires=OFF_PIN if k == 0 else None, wires_done=ON_PIN[w], **PIN_VIEW)
g.put_away([MATRIX] + list(FEMALE.values()))
# ================================================================ PART 2 (end)

# ================================================================ PART 3: THE BUTTON AND THE USB CABLE (begin)
# The push button on its own: its nut off, through the hole in D2 from the brown side, the nut back on from the inside.
_btn = box(BUTTON)
AXIS = [float(mid(BUTTON)[0]), 881.63]                              # the button's axis (x, y); it points along Z, its head at +Z
STUB = dict(red=np.array([634.54, 881.61, 1233.65]), black=np.array([641.93, 881.65, 1233.65]))   # where each lead leaves the back of the button
LEAD_R, HAND_LEAD = 0.62, 50.0                                      # the leads laid out straight back from the button, 50 mm (in the hand)
for c in ('red', 'black'):
    g.wire(f'lead {c}', 'wire_red' if c == 'red' else 'wire_black', LEAD_R, name='Push Button')
PIN_OF = dict(red=RED_PIN, black=BLACK_PIN)
PIN_HOLE = dict(red='j5', black='j16')                              # red on 5V (g5), black on D13 (g16): the 12 kΩ resistor pulls D13 down
PIN_EXIT = {c: np.array([hole(PIN_HOLE[c])[0], 879.92, hole(PIN_HOLE[c])[2]]) for c in ('red', 'black')}


def hand_pin(c):
    """A lead's pin at the end of its lead laid out straight back from the button (the button in its seat), pin pointing -Z."""
    end = STUB[c] + [0.0, 0.0, -HAND_LEAD]
    return turned([1, 0, 0], 90.0, PIN_EXIT[c].tolist(), (end - PIN_EXIT[c]).round(3).tolist())


def pin_pose(c, button_pose=ZERO):
    """Where a lead's pin is, laid out straight back from the button, with the button at button_pose."""
    return compose(button_pose, hand_pin(c), mid(PIN_OF[c]).tolist()) if button_pose != ZERO else hand_pin(c)


def hand_lead(c, button_pose=ZERO):
    start = apply_pose(button_pose, [STUB[c]])[0]
    end = apply_pose(pin_pose(c, button_pose), [PIN_EXIT[c]])[0]
    return {f'lead {c}': W.route(W.resample(np.linspace(start, end, 40), 0.75), a=BUTTON, b=PIN_OF[c],
                                 a_at=button_pose if button_pose != ZERO else None, b_at=pin_pose(c, button_pose), stretch=True)}


g.carry([NUT], by=BUTTON, pose=[0.0, 0.0, 3.12])                    # (screwed up to the button's head, as it comes)
g.part_picture('Push Button', add=[NUT, RED_PIN, BLACK_PIN], poses={NUT: [0.0, 0.0, 3.12], RED_PIN: hand_pin('red'), BLACK_PIN: hand_pin('black')},
               wires=[dict(colour='wire_red' if c == 'red' else 'wire_black', radius=LEAD_R, pts=hand_lead(c)[f'lead {c}']['pts']) for c in ('red', 'black')])
for c in ('red', 'black'):
    g.carry([PIN_OF[c]], by=BUTTON, pose=hand_pin(c))
# The nut turns as it comes off and as it goes back on (Lee, 19 Oct 2026: "the idea of rotation", one or two turns): two turns, a
# quarter turn a pose (the player takes the shorter way between two poses), over two beats so that the hexagon does not seem to turn
# backwards. (The button is given a way that stays where it is, of three stops, which makes the step two beats long.) Unscrewed, the
# nut turns clockwise seen from the button's head; screwed on, the other way.
NUT_AT = [AXIS[0], AXIS[1], 1251.0]                                 # (on the button's axis, which runs along Z)
NUT_OFF = [0.0, 0.0, -95.0]
TWO_BEATS = [ZERO, ZERO, ZERO]


def nut_turns(z0, z1, sign, turns=2):
    """The nut's poses from z0 to z1 mm along the axis, `turns` whole turns, a quarter turn each (sign -1: unscrewing)."""
    n = 4 * turns
    return [turned([0, 0, 1], sign * 90.0 * k, NUT_AT, [0.0, 0.0, round(z0 + (z1 - z0) * k / n, 2)]) for k in range(1, n + 1)]


g.place('Unscrew the nut from the push button and slide it off over the wires.', move=[BUTTON], path=TWO_BEATS, staged=True,
        ride={NUT: nut_turns(3.12, NUT_OFF[2], -1)}, lines=False,
        labels={BUTTON: 'Push Button'}, wires={**hand_lead('red'), **hand_lead('black')},
        arrows=[dict(tail=[AXIS[0] + 11.0, AXIS[1], 1255.0 - 3.0], head=[AXIS[0] + 11.0, AXIS[1], 1255.0 - 60.0], normal=[0, 1, 0], part=NUT)],
        **r1_camera([0.6213, 0.2806, 0.7316], [638.2, 881.6, 1207.0], 53.4))
g.put_away([NUT])
g.place('Push the button, wires first, through the round hole in D2 from the side with D2 engraved on it.', move=[BUTTON], show=[D2], against=[D2], staged=True,
        direction=[0, 0, 1], hover=100, labels={D2: 'D2'}, lines_at=[[AXIS[0] + 7.4, AXIS[1], 1253.5]])
NUT_ON = [[0.0, 0.0, -60.0]] + [via(p) for p in nut_turns(-60.0, 0.0, 1)[:-1]] + [ZERO]
g.place('Screw the nut back onto the button from the other side of D2, until it is tight against D2.', move=[NUT, BUTTON], against=[D2, BUTTON], staged=True,
        path=NUT_ON, paths={NUT: NUT_ON, BUTTON: TWO_BEATS}, lines_at=[[AXIS[0] + 7.4, AXIS[1], 1251.2]], look_from=[1, 1, -1])
g.put_away([D2, BUTTON, NUT, RED_PIN, BLACK_PIN])

# Back on the base: D2, with its button, stands beside D1 (57 mm out from its place, as in the published guide), and the LED matrix
# lies beside the base; each of the button's leads goes into its hole, one per step.
D2_OUT = [0.0, 0.0, 57.11]
g.rest_at([D2], D2_OUT)
g.carry([BUTTON, NUT], by=D2)
for c in ('red', 'black'):
    g.carry([PIN_OF[c]], by=BUTTON, pose=hand_pin(c))
g.carry([MATRIX], by=BREADBOARD, pose=P_BESIDE)
for w in JUMPERS:
    g.carry([FEMALE[w]], by=MATRIX)
BESIDE_MIDS = dict(white=[[652.0, 895.0, 1176.0], [690.0, 868.0, 1194.5], [731.2, 865.0, 1207.8]],   # (side by side as their sockets are, the
                   grey=[[652.0, 894.0, 1179.0], [690.0, 868.0, 1199.5], [728.8, 865.0, 1212.2]],    # purple wire over the grey one to its place
                   purple=[[630.0, 900.0, 1216.0], [672.0, 899.5, 1207.0], [696.0, 875.0, 1197.5], [730.0, 865.0, 1210.0]])   # between the two)
BESIDE = {k: v for w in JUMPERS for k, v in jumper(w, ZERO, f_pose(w, P_BESIDE), BESIDE_MIDS[w]).items()}


def plugged_lead(c, d2_pose=ZERO, mids=(), into=3.0):
    a = apply_pose(d2_pose, [STUB[c]])[0]
    line = smooth(a, [0, 0, -1], PIN_EXIT[c], [0, -1, 0], mids, lead=min(3.0, into))
    check(line, LEAD_R, skip=(BUTTON, PIN_OF[c], D2, NUT), name=f'lead {c}')
    return {f'lead {c}': W.route(line, a=BUTTON, b=PIN_OF[c], a_at=d2_pose if d2_pose != ZERO else None, stretch=True)}


LEAD_MIDS = dict(red=[[636.0, 893.0, 1250.0], [651.0, 895.0, 1192.0]], black=[[642.0, 893.0, 1250.0], [652.0, 894.0, 1222.0]])
for k, c in enumerate(('red', 'black')):
    g.place(f'Push the pin on the button\'s {c} wire into {PIN_HOLE[c]}.', move=[PIN_OF[c]], path=[pin_pose(c, D2_OUT), ZERO], lines=False,
            appear=[D2, MATRIX, RED_PIN, BLACK_PIN] if k == 0 else (),
            labels=[hole_label(PIN_HOLE[c])], eye=[PIN_OF[c]],
            wires={**BESIDE, **hand_lead('red', D2_OUT), **hand_lead('black', D2_OUT)} if k == 0 else None,
            wires_done=plugged_lead(c, D2_OUT, LEAD_MIDS[c]),
            view_dir=[0.5792, 0.5736, -0.5792], frame=([645.0, 884.0, 1209.0], 40.0))   # (closer, from beyond row j: Lee, 19 Oct 2026)

# The USB cable: its right-angle Mini-B plug into the Nano Board's socket, its cable leaving towards D4 and out through the notch in
# D4's foot to the A end lying on the table.
USB_EXIT = np.array([619.29, 877.37, 1221.36])                      # the cable's end of the plug (the cable leaves along -X)
_a = box(USB_A)
A_EXIT = np.array([_a[1][0], (_a[0][1] + _a[1][1]) / 2, (_a[0][2] + _a[1][2]) / 2])   # the A end's cable end (+X), lying on the table
NOTCH = np.array([595.9, 859.1, 1219.0])                            # the cable in the notch in D4's foot (y 856.2 - 862.7, z 1216 - 1222)
g.wire('usb cable', 'cable_black', 1.75, name='USB Cable')
USB_OUT = [0.0, 0.0, 25.0]


# Down beside the breadboard, over the edge of D1 and out through the notch in D4's foot (z 1216 - 1221, up to y 869) resting on D1, as
# the published guide has it, then down to the A end on the table.
USB_MIDS = [[612.0, 876.1, 1223.6], [606.0, 870.9, 1222.0], [602.0, 866.7, 1219.8], [598.0, 864.4, 1219.2], [594.0, 864.2, 1219.3], [586.0, 862.5, 1219.5], [576.0, 860.8, 1219.2]]
USB_OUT_MIDS = [[610.0, 875.0, 1240.0], [603.0, 868.0, 1228.0], [598.0, 864.4, 1219.5], [594.0, 864.2, 1219.3], [586.0, 862.5, 1219.5], [576.0, 860.8, 1219.2]]


def usb_cable(out=ZERO):
    a = apply_pose(out, [USB_EXIT])[0]
    line = smooth(a, [-1, 0, 0], A_EXIT, [-1, 0, 0], USB_MIDS if out == ZERO else USB_OUT_MIDS, lead=2.0)
    check(line, 1.75, skip=(USB_B, USB_A), name='usb cable')
    return {'usb cable': W.route(line, a=USB_B, b=USB_A, a_at=out if out != ZERO else None, stretch=True)}


g.place("Plug the USB cable's Mini-B plug into the Nano Board's USB socket, its cable towards the D4 end of the base.", move=[USB_B], show=[USB_A],
        path=[USB_OUT, ZERO], lines_at=[[637.29, 877.37, 1211.63]], labels={USB_B: 'USB Cable'}, wires=usb_cable(USB_OUT), wires_done=usb_cable(),
        **r1_camera(DIAG, [640.9, 881.6, 1232.8], 148.7))

# D2 stands on D1, its tabs into the slots along D1's edge; the button's leads follow.
# (Round the USB plug on its far side, between the 12 kΩ resistor's leg and the black wire's pin, under D10.)
SEATED_LEAD_MIDS = dict(red=[[640.0, 882.5, 1229.0], [647.5, 881.5, 1222.0], [650.0, 879.6, 1210.0], [650.3, 880.0, 1200.0], [651.5, 883.0, 1188.0]],
                        black=[[645.5, 882.0, 1228.0], [651.0, 881.4, 1218.0], [652.62, 881.0, 1210.0]])
g.place('Stand D2, with the button, on D1: its tabs go into the slots along the edge of D1.', move=[D2], path=[D2_OUT, ZERO],
        wires_done={**plugged_lead('red', ZERO, SEATED_LEAD_MIDS['red']), **plugged_lead('black', ZERO, SEATED_LEAD_MIDS['black'], into=1.2)},   # (j16 is under D10)
        **r1_camera(DIAG, [640.9, 881.6, 1232.8], 148.7))
# ================================================================ PART 3 (end)

# ================================================================ PART 4: THE HOUSING (begin)
# (The USB cable's A end lies out of D4's way, 60 mm further out than in the first draft (assemble.py), so that D4, held out before it
# goes on, has the cable in its notch: Lee, 19 Oct 2026. The cable itself passes through the notch in D4's foot.)
g.place('Push D4 onto the end of D1 and D2, the USB cable in the notch at its foot.', move=[D4], labels={D4: 'D4'}, direction=[-1, 0, 0], hover=65,
        against=[i for i in g.placed if i not in g.parked and i != USB_A], **r1_camera(DIAG, [640.9, 881.6, 1232.8], 148.7))

# ---- The LED matrix's three wires from here on (Lee, 19 Oct 2026: they went through D4, the D9s and D10). Inside the box each runs
# from its pin under the end of D9 nearest D3 (the white and grey wires over the Nano Board's ICSP pins, which leave 1.8 mm under the
# engraved end of the D9; the purple wire under the D9's lower edge), along the floor beside D4, inside the D11 posts, under where
# D10's lower edge will be. From there: up and over the top edge of D4 to the matrix laid outside; with the matrix held over the box,
# on along the floor, up behind D2 and back along under the matrix (as the published guide has them, so that D10 is hooked on over
# them); the matrix in place, up into the slot in D10 and back under the matrix to its pins. (White V+ nearest D4, then grey; the
# purple wire's pin, b19, is under the USB plug's leg: it passes 0.3 mm into the plug, as the CAD places the two.)
IN_BOX = dict(white=[[646.0, 885.4, 1170.45], [622.0, 885.4, 1170.45], [609.0, 884.8, 1170.6], [605.0, 883.0, 1174.5], [605.0, 882.0, 1186.0], [605.0, 882.0, 1199.0]],
              grey=[[646.0, 885.4, 1172.99], [622.0, 885.4, 1172.99], [611.0, 884.8, 1173.1], [607.4, 883.0, 1177.0], [607.4, 882.0, 1188.0], [607.4, 882.0, 1199.0]],
              purple=[[623.5, 881.45, 1213.6], [614.0, 881.45, 1213.6]])
PIN_LEAD = dict(white=3.0, grey=3.0, purple=1.5)                    # (the purple wire turns under the D9 as soon as it leaves its pin)
# Where each crosses the top edge of D4 (y 907.04), 2.5 mm apart, in the order their sockets lie outside (white nearest D4): so the
# grey wire rises first and passes over the white one, which runs on along the floor and rises behind it.
OVER_Z = dict(grey=1211.0, purple=1213.5, white=1216.0)
RISE = dict(white=[[605.0, 882.0, 1209.0], [604.6, 882.6, 1213.5], [603.8, 887.5, 1215.6], [602.0, 898.0, 1216.0]],   # (from the floor to D4's top, inside)
            grey=[[607.4, 882.0, 1203.0], [607.6, 884.5, 1206.0], [607.0, 890.5, 1208.6], [604.6, 899.5, 1210.6]],
            purple=[[610.0, 883.0, 1213.5], [607.0, 887.0, 1213.5], [603.6, 893.0, 1213.5], [600.4, 900.0, 1213.5]])


def over_d4(w, lift):
    """The wire from its pin, over the top of D4, to its socket on the LED matrix laid outside, `lift` mm up (the published guide's
    pose: 5.89)."""
    pose = turned([0, 1, 0], 180.0, MC, [-90.76, lift, 25.09])
    sx = f_end(w, pose)[0]
    top = 908.4 + (lift - 5.89) * 0.25                              # (over the edge, higher while the matrix is held higher)
    z = OVER_Z[w]
    ys = sx[1]
    out = [[599.3, top - 2.6, z], [596.0, top, z], [592.5, top - 1.6, z + 0.6]]
    # Outside, the three go on as a flat ribbon about the purple wire's line, turning from going out across D4's edge (side by side
    # along z) to going along the sockets (side by side along x), each kept 2.5 mm from the middle one square to the way they run;
    # down under the matrix's edge before they reach it.
    k = dict(white=1, purple=0, grey=-1)[w]
    px = f_end('purple', pose)[0]
    c0, c1 = np.array([592.5, OVER_Z['purple'] + 0.6]), np.array([px[0], px[2] - 3.0])
    for f in (0.25, 0.5, 0.75):
        t = (1 - f) * np.array([-1.0, 0.0]) + f * np.array([0.0, 1.0])
        t /= np.linalg.norm(t)
        x, zz = (1 - f) * c0 + f * c1 + 2.5 * k * np.array([t[1], -t[0]])
        out.append([round(float(x), 2), round(top - 1.6 - (top - 1.6 - ys - 0.3) * min(1.0, f / 0.55), 2), round(float(zz), 2)])
    return pose, jumper(w, ZERO, f_pose(w, pose), IN_BOX[w] + RISE[w] + out, lead=PIN_LEAD[w])


# The LED matrix is lifted over D4 and laid outside it, its wires over the top edge of D4 (Lee, 19 Oct 2026: from above, with one
# arrow, as the published guide's Step 23): lifted straight up, carried across over the walls, lowered outside. Three beats (D4 is
# given a way that stays where it is, which makes the step three beats long), the wires keeping pace.
P_UP_BESIDE = turned([0, 1, 0], 180.0, MC, [91.01, 25.0, 11.37])
UP_BESIDE_MIDS = dict(white=[[652.0, 902.0, 1176.0], [690.0, 912.0, 1194.5], [731.2, 915.5, 1207.8]],   # (BESIDE's, lifted)
                      grey=[[652.0, 901.0, 1179.0], [690.0, 911.5, 1199.5], [728.8, 915.5, 1212.2]],
                      purple=[[630.0, 905.0, 1216.0], [672.0, 917.0, 1207.0], [696.0, 914.5, 1197.5], [730.0, 915.5, 1210.0]])
UP_BESIDE = {k: v for w in JUMPERS for k, v in jumper(w, ZERO, f_pose(w, P_UP_BESIDE), UP_BESIDE_MIDS[w]).items()}
P_UP_OUTSIDE, UP_OUTSIDE = None, {}
for w in JUMPERS:
    P_UP_OUTSIDE, r = over_d4(w, 25.0)
    UP_OUTSIDE.update(r)
OUTSIDE = {}
for w in JUMPERS:
    P_OUT, r = over_d4(w, 5.89)
    OUTSIDE.update(r)
assert P_OUT == P_OUTSIDE
_bb = box(BREADBOARD)
g.place('Lift the LED matrix over D4 and lay it down outside, its wires over the top edge of D4.', move=[D4], paths={D4: [ZERO, ZERO, ZERO, ZERO]},
        ride={MATRIX: [P_UP_BESIDE, P_UP_OUTSIDE, P_OUTSIDE]}, lines=False, eye=[MATRIX],
        wires_done={k: [UP_BESIDE[k], UP_OUTSIDE[k], OUTSIDE[k]] for k in OUTSIDE},
        arrows=[dict(tail=[690.0, 862.4, 1133.0], head=[585.0, 862.4, 1133.0], normal=[0, 1, 0], part=D1, width=5.0)],
        view_dir=[0.0, 0.996, 0.088], frame=([638.5, 880.0, 1205.0], 82.0))
# D3 and D5 go on with the box turned over (as in the published guide): D3 is hooked into D4 tilted, then swung shut; D5 closes the box.
# The hinge: D3's end tabs in D4's slots, a vertical line at D4's inner face and D3's inner face. Tilted, D3's far end is 22 degrees
# out from the box; it comes in along its own tilted length, then swings shut so that D1's tabs go into its slots.
HINGE = [float(box(D4)[1][0]), float(mid(D3)[1]), float(box(D3)[1][2])]
TILT = 22.0
_in = 40.0 * np.array([np.cos(np.radians(TILT)), 0.0, -np.sin(np.radians(TILT))])
g.place('Turn the box over. Hook the tabs at the end of D3 into the slots in D4, then swing D3 shut onto D1.', move=[D3], labels={D3: 'D3'},
        path=[turned([0, 1, 0], TILT, HINGE, _in.round(2).tolist()), turned([0, 1, 0], TILT, HINGE), ZERO], flip=True,
        lines_at=[[[590.9, y, 1155.1], [597.4, y, 1155.1]] for y in (862.0, 902.0)],   # (D3's end tabs into D4's slots)
        **r1_camera([-0.5792, -0.5736, -0.5792], [617.4, 881.6, 1189.6], 135.7))
# (From the corner on D5's side, near its engraved code: Lee, 19 Oct 2026. The box is upside down, so the code is too.)
g.place('Push D5 onto the open end, over the tabs of D3 and D2.', move=[D5], labels={D5: 'D5'}, direction=[1, 0, 0], hover=42, flip=True,
        **r1_camera([0.5792, -0.5736, -0.5792], [617.4, 881.6, 1189.6], 135.7))
# ================================================================ PART 4 (end)

# ================================================================ PART 5: THE LED MATRIX, THE SHELVES AND THE STEMS (begin)
# (The wires already lie under the D9 that is nearer D4, at its engraved end: Lee, 19 Oct 2026.)
HELD_CAMERA = r1_camera(DIAG, [601.0, 910.9, 1204.6], 114.8)
g.place('Turn the box the right way up. Push the two D9 LED supports down into their slots in D2 and D3.', move=[D9_A, D9_B], labels={D9_A: 'D9'},
        direction=[0, 1, 0], hover=65, **HELD_CAMERA)
# Held over the box (Lee, 19 Oct 2026, as the published guide): each wire on along the floor beside D4, up behind D2, over and back
# along under the matrix's edge to its socket, through where D10's slot will be (x 605.2 - 612.8): D10 then comes up behind the matrix
# with the wires in its slot, and slides along under them.
HELD_TAIL = dict(white=[[605.0, 882.0, 1238.0], [605.2, 884.0, 1244.8], [605.6, 893.0, 1248.0], [605.9, 925.0, 1248.3], [606.2, 940.5, 1251.3],
                        [606.4, 945.0, 1255.0], [606.6, 949.3, 1253.0], [606.6, 950.4, 1247.5], [606.6, 950.4, 1205.0]],
                 grey=[[607.4, 882.0, 1236.5], [607.6, 884.0, 1243.5], [608.5, 893.0, 1246.6], [609.5, 925.0, 1246.9], [610.2, 940.0, 1249.8],
                       [610.8, 944.6, 1253.8], [611.2, 948.8, 1252.0], [611.2, 950.4, 1246.5], [611.2, 950.4, 1205.0]],
                 purple=[[611.0, 882.0, 1219.0], [610.8, 882.0, 1238.5], [610.4, 884.0, 1246.0], [609.6, 893.0, 1249.4], [609.0, 925.0, 1249.7], [608.9, 941.0, 1252.4],
                         [608.9, 945.4, 1256.2], [608.9, 949.6, 1254.0], [608.9, 950.4, 1248.5], [608.9, 950.4, 1205.0]])
HELD = {k: v for w in JUMPERS for k, v in jumper(w, ZERO, f_pose(w, P_HELD), IN_BOX[w] + HELD_TAIL[w], lead=PIN_LEAD[w]).items()}
P_TURN = turned([0, 1, 0], 90.0, MC, [-50.0, 45.0, 12.0])          # (half way round, in the air: each turn between two poses under 180 degrees)
g.place('Pick up the LED matrix and hold it over the box, LEDs up.', ride={MATRIX: [P_TURN, P_HELD]}, lines=False, eye=[MATRIX], wires_done=HELD, **HELD_CAMERA)
# D10 hooks under the LED matrix: up under it, then slid along so that its hooks hold the matrix's edges (it rides on the matrix).
D10_UNDER = [0.0, -22.0, 40.0]
g.carry([D10], by=MATRIX, pose=D10_UNDER, appear=False)
_d10 = box(D10)
g.place('Hook D10 under the LED matrix: hold it under the matrix, then slide it along until its hooks hold both edges.', appear=[D10],
        ride={D10: [[0.0, 0.0, 40.0], ZERO]}, lines=False, labels={D10: 'D10'},
        arrows=[dict(tail=[float(mid(D10)[0]), float(_d10[1][1]) + 1.0, float(_d10[1][2]) + 1.0], head=[float(mid(D10)[0]), float(_d10[1][1]) + 1.0, float(_d10[1][2]) - 28.0],
                     normal=[1, 0, 0], part=D10)], **HELD_CAMERA)
# In the box: from the floor beside D4 up into the slot in D10 and back along under the matrix to its socket (as the published guide).
SEATED_TAIL = dict(white=[[605.2, 882.0, 1205.0], [605.6, 885.0, 1208.6], [606.2, 890.0, 1209.2], [606.6, 893.2, 1207.3], [606.6, 893.6, 1203.5], [606.8, 893.7, 1197.0]],
                   grey=[[607.6, 882.0, 1205.0], [608.6, 884.6, 1208.8], [610.4, 890.0, 1209.6], [611.2, 893.2, 1207.6], [611.2, 893.6, 1203.5], [611.6, 893.7, 1197.0]],
                   purple=[[610.8, 883.0, 1213.2], [609.8, 886.5, 1212.2], [609.2, 889.5, 1211.0], [608.9, 892.8, 1208.8], [608.9, 893.6, 1203.5], [609.3, 893.7, 1197.0]])
SEATED = {k: v for w in JUMPERS for k, v in jumper(w, ZERO, ZERO, IN_BOX[w] + SEATED_TAIL[w], lead=PIN_LEAD[w]).items()}
# (The lead lines end at the bottoms of the slots in D4 and D5, where D10's end tabs stop: Lee, 19 Oct 2026. A close-up, the matrix
# left out, of the wires going down through the slot in D10 to the breadboard.)
D10_TABS = [[596.0, 891.15, 1204.47], [681.0, 891.15, 1204.47]]
g.place('Lower the LED matrix, with D10, into the box: the ends of D10 go into the slots in D4 and D5.', move=[MATRIX], path=[P_HELD, ZERO],
        lines_at=D10_TABS, lines_to=WALLS + [D10], wires_done=SEATED, **HELD_CAMERA,
        inset=dict(target=[608.5, 889.0, 1203.0], dir=[-0.45, 0.85, 0.27], radius=15.0, hide=[MATRIX],
                   caption='The wires go down through the slot in D10', alt='Close-up, without the LED matrix, of the wires in the slot in D10'))
# (Centred and closer, from the same corner as the step before, so that D6's code reads; a close-up from above, D6 left out, of the four
# slots in D1 that the D11 posts go into: Lee, 19 Oct 2026, as the published guide.)
D1_SLOTS = [[x, 862.4, z] for x in (601.63, 674.83) for z in (1166.2, 1242.4)]
g.place('Lay D6 on top of the walls, its slots over their tabs.', move=[D6], labels={D6: 'D6'}, direction=[0, 1, 0], hover=64,
        view_dir=[-0.5792, 0.5736, -0.5792], frame=([638.5, 913.0, 1204.5], 84.0),
        inset=dict(target=[638.2, 862.4, 1204.3], dir=[0.0, 1.0, 0.0001], radius=58.0, hide=[D6], marks=[(p, 6.5) for p in D1_SLOTS],
                   caption='The four slots in D1 for the D11 posts', alt='The box from above, without D6: four red boxes round the slots in D1'))
# The four D11 posts (Lee, 19 Oct 2026, as the published guide): two and two, each pair seen from the side its engraved codes face,
# down through D6's corner slots only until their tabs reach the top of the slots in D1; then, the box turned over and D1 and D5
# see-through, all four pushed home together. Until then they ride on D1.
D11S = [D11_A, D11_B, D11_C, D11_D]
D11_SHORT, D11_UP = [0.0, 6.38, 0.0], [0.0, 85.0, 0.0]               # (short: the tab's foot at D1's top, y 862.4)
g.carry(D11S, by=D1, pose=D11_UP, appear=False)
foot = lambda i, up: [float(mid(i)[0]), float(box(i)[0][1]) + up, float(mid(i)[2])]
g.place('Push two D11 shelf posts down through the corner slots of D6 at the D5 end, until their tabs reach the slots in D1.', appear=[D11_A, D11_B],
        ride={D11_A: D11_SHORT, D11_B: D11_SHORT}, labels={D11_A: 'D11'}, lines_at=[[foot(i, D11_UP[1]), foot(i, D11_SHORT[1])] for i in (D11_A, D11_B)],
        view_dir=[0.5469, 0.359, 0.7563], frame=([638.5, 935.0, 1204.5], 100.0))
g.place('Push the other two D11 posts down through the corner slots at the D4 end, until their tabs reach the slots in D1.', appear=[D11_C, D11_D],
        ride={D11_C: D11_SHORT, D11_D: D11_SHORT}, lines_at=[[foot(i, D11_UP[1]), foot(i, D11_SHORT[1])] for i in (D11_C, D11_D)],
        view_dir=[-0.7476, 0.3966, 0.5328], frame=([638.5, 935.0, 1204.5], 100.0))
g.place('Turn the box over. Push all four D11 posts down until their tabs come through the slots in D1.', ride={i: ZERO for i in D11S},
        flip=True, view_dir=[0.4109, -0.8401, 0.3541], frame=([638.5, 870.0, 1204.5], 72.0), ghost={D1: 0.5, D5: 0.5},
        eye=[dict(id=D11_B, anchor=foot(D11_B, 0.0))], lines_at=[[[float(mid(i)[0]), 874.75, float(mid(i)[2])], [float(mid(i)[0]), 857.98, float(mid(i)[2])]] for i in D11S],
        inset=dict(target=[674.83, 857.0, 1166.2], radius=6.0, caption='The tab through D1', alt='Close-up from below of a D11 tab through its slot in D1'))
g.place('Turn the box the right way up. Lay D7 onto the D11 posts.', move=[D7], labels={D7: 'D7'}, direction=[0, 1, 0], hover=65, lines_to=D11S,
        **r1_camera(DIAG, [602.9, 918.8, 1204.3], 117.3))
g.place('Lay D8 onto the D11 posts.', move=[D8], labels={D8: 'D8'}, direction=[0, 1, 0], hover=55, lines_to=D11S, **r1_camera(DIAG, [602.9, 918.8, 1204.3], 117.3))
g.place('Push one LED stem down through a corner hole of D8, D7 and D6 until it stands over its LED.', move=[STEMS[0]], direction=[0, 1, 0], hover=44,
        labels={STEMS[0]: 'LED Stem'}, axial=True, **r1_camera(DIAG, [602.9, 934.5, 1204.3], 126.4))
# (All 63 come in and go down together, rather than appearing in place: Lee, 19 Oct 2026.)
g.place('Push in the other 63 LED stems the same way, one through each hole.', move=STEMS[1:], direction=[0, 1, 0], hover=44, lines=False,
        eye=[STEMS[0]], **r1_camera(DIAG, [602.9, 934.5, 1204.3], 126.4))
# ================================================================ PART 5 (end)

g.build()
