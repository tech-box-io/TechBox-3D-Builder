"""Mini Robot Arm (MRA), full build: an electronics test on the bench, then base, controller, arm, claw. The build, in order.

Run from the project root:   python "MRA Build Instructions Prototype/guide.py"
It writes steps.json (what the player shows) and parts.json (the parts list).

Order and wording follow the MRA Build Notes and Lee's step notes of 13 and 14 Oct 2026; the arm and claw
follow the build videos (docs/research/mra/). One part or one action per step.
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
from scipy.spatial.transform import Rotation

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
import wires as W  # noqa: E402
from stepgen import Guide, apply_pose, compose, turn_dir, turned, via  # noqa: E402

# ---------------------------------------------------------------- parts
# CAD instance ids. The CAD file names do not match the codes engraved on the wood for 26 of the 44
# wood parts (docs/research/mra/cad_codes_base.md has the table); everything below follows the engravings.
B1, B2, B4, B5, B6_LEFT, B6_RIGHT, B7, B8, B3 = 'NAUO1 NAUO2 NAUO3 NAUO4 NAUO5 NAUO6 NAUO7 NAUO8 NAUO9'.split()
R1, R2, R3, R4, R6, R5, R7, R8 = 'NAUO10 NAUO11 NAUO12 NAUO13 NAUO14 NAUO15 NAUO16 NAUO17'.split()
BASE_MOTOR, BASE_HORN = 'NAUO45', 'NAUO46'
BASE_SCREWS = ['NAUO47', 'NAUO48', 'NAUO49', 'NAUO50', 'NAUO51', 'NAUO52']
JOY_LEFT, JOY_RIGHT, MODULE = 'NAUO80', 'NAUO81', 'NAUO82'
NANO = 'NAUO126'                                                    # the Nano Board: inside the module's assembly in the CAD, a part of its own here (materials.json "own_parts")
BASE_PLUG = 'NAUO83'
# The arm. Engraved codes A1 - A13, with A9 twice; only A1 and A2 are also the CAD's names (CAD A2_Supplement = A3, A3 = A4,
# A4 = A5, A5 = A7, A6 = A8, A7 = A11, A8 = A10, A9 = A12, A10 = A13, A11 = A6, A12 = A9).
A1, A2, A3, A4, A5, A7, A8, A11, A10, A12, A13, A6 = ['NAUO%d' % i for i in range(18, 30)]
A9_NEAR_A7, A9_NEAR_A8 = 'NAUO30', 'NAUO31'
ELBOW_MOTOR, ELBOW_HORN, ELBOW_PLUG = 'NAUO58', 'NAUO59', 'NAUO84'          # in R5, under R8; its lead goes to row 6
SHOULDER_MOTOR, SHOULDER_HORN, SHOULDER_PLUG = 'NAUO66', 'NAUO67', 'NAUO86'  # in R6, under R7; its lead goes to row 9
A7_SCREW, A8_SCREW = 'NAUO53', 'NAUO54'                             # 16mm: the two bars of the upper arm into the A9 pieces
PIVOT_SCREW = 'NAUO55'                                              # 6mm: A7 on R2 (the shoulder pivot)
LEVER_SCREW, LEVER_A4_SCREW = 'NAUO56', 'NAUO62'                    # 10mm: A1 + A2 + A3; the top of the lever to A4
A5_A4_SCREW, A5_A7_SCREW = 'NAUO57', 'NAUO63'                       # 6mm: A5 to A4; A5 to the end of A7 (the elbow)
R8_SCREWS, R7_SCREWS = ['NAUO60', 'NAUO61'], ['NAUO68', 'NAUO69']   # 10mm: the clamp plates, above and below each motor
A11_SCREW, A12_SCREW, R6_A11_SCREW = 'NAUO64', 'NAUO65', 'NAUO70'   # 6mm: A11 and A12 on A10; R6's lobe to A11
A13_SCREW = 'NAUO71'                                                # 10mm: A13 and A10 to the end of A8 (the elbow)
# The claw. Engraved codes C1 - C9; five differ from the CAD's names (CAD C4 = C6, C5 = C4, C6 = C5, C7 = C8, C8 = C7).
C1, C2, C3, C6, C4, C5, C8, C7, C9 = ['NAUO%d' % i for i in range(32, 41)]
CLAW_MOTOR, CLAW_HORN, CLAW_PLUG = 'NAUO72', 'NAUO73', 'NAUO90'     # between C3 and C6; its short lead ends in a plug of its own
C6_SCREWS, C8_SCREW = ['NAUO74', 'NAUO75'], 'NAUO76'                # 16mm: C6 to C3 either side of the motor; 10mm: the pivot of jaw C8
A12_C1_SCREW, A13_C1_SCREW, A5_C2_SCREW = 'NAUO77', 'NAUO78', 'NAUO79'   # 6mm: the claw to the arm
# The servo extension wire: a coupler that takes the claw motor's plug, a plug of its own inside the coupler, three wires and
# a plug for row 10 of the I/O module.
COUPLER, EXTENSION_PLUG, ROW10_PLUG = 'NAUO91', 'NAUO92', 'NAUO85'
# The T1 / T2 block: two square plates (T1) and two strips (T2) that cross in a half-lap. NAUO42 has its slot open at the top,
# so its solid end is the bottom one; NAUO43 is the same strip upside down.
T1_LOWER, T2_SOLID_DOWN, T2_SLOT_DOWN, T1_UPPER = 'NAUO41', 'NAUO42', 'NAUO43', 'NAUO44'
# The USB cable: its two ends come as STEP files of their own (materials.json "extra_parts"); the cable between them is drawn.
USB_B, USB_A = 'USB_B', 'USB_A'                                     # the Mini-B end (into the Nano Board), the A end (to the computer)

NAMES = {R1: 'R1', R2: 'R2', R3: 'R3', R4: 'R4', R5: 'R5', R6: 'R6', R7: 'R7', R8: 'R8',
         B1: 'B1', B2: 'B2', B3: 'B3', B4: 'B4', B5: 'B5', B6_LEFT: 'B6', B6_RIGHT: 'B6', B7: 'B7', B8: 'B8',
         BASE_MOTOR: 'Base Motor', JOY_LEFT: 'Joystick', JOY_RIGHT: 'Joystick', MODULE: 'Nano I/O Module', NANO: 'Nano Board',
         T1_LOWER: 'T1', T1_UPPER: 'T1', T2_SOLID_DOWN: 'T2', T2_SLOT_DOWN: 'T2',
         **{s: '6mm Hex Screw' for s in BASE_SCREWS}}
NAMES.update({A1: 'A1', A2: 'A2', A3: 'A3', A4: 'A4', A5: 'A5', A6: 'A6', A7: 'A7', A8: 'A8', A9_NEAR_A7: 'A9', A9_NEAR_A8: 'A9',
              A10: 'A10', A11: 'A11', A12: 'A12', A13: 'A13', ELBOW_MOTOR: 'Elbow Motor', SHOULDER_MOTOR: 'Shoulder Motor',
              **{s: '6mm Hex Screw' for s in (PIVOT_SCREW, A5_A4_SCREW, A5_A7_SCREW, A11_SCREW, A12_SCREW, R6_A11_SCREW)},
              **{s: '10mm Hex Screw' for s in (LEVER_SCREW, LEVER_A4_SCREW, A13_SCREW, *R8_SCREWS, *R7_SCREWS)},
              **{s: '16mm Hex Screw' for s in (A7_SCREW, A8_SCREW)}})
NAMES.update({C1: 'C1', C2: 'C2', C3: 'C3', C4: 'C4', C5: 'C5', C6: 'C6', C7: 'C7', C8: 'C8', C9: 'C9', CLAW_MOTOR: 'Claw Motor',
              COUPLER: 'Servo Extension Wire', **{s: '16mm Hex Screw' for s in C6_SCREWS}, C8_SCREW: '10mm Hex Screw',
              **{s: '6mm Hex Screw' for s in (A12_C1_SCREW, A13_C1_SCREW, A5_C2_SCREW)}})
# Parts that come fitted to another: same name on hover, one line in the parts list, pictured together.
PART_OF = {BASE_HORN: BASE_MOTOR, ELBOW_HORN: ELBOW_MOTOR, SHOULDER_HORN: SHOULDER_MOTOR, CLAW_HORN: CLAW_MOTOR, EXTENSION_PLUG: COUPLER}
# Named on hover only (no label, no line in the parts list): the plug on a motor's lead, the caps of the jumper wires.
JUMPER_CAPS = ['NAUO%d' % i for i in range(95, 111)]
NAMES.update({BASE_PLUG: 'Base Motor', ELBOW_PLUG: 'Elbow Motor', SHOULDER_PLUG: 'Shoulder Motor', CLAW_PLUG: 'Claw Motor',
              ROW10_PLUG: 'Servo Extension Wire', **{cap: 'Breadboard Wire (F-F)' for cap in JUMPER_CAPS}, USB_B: 'USB Cable', USB_A: 'USB Cable'})
UNLISTED = [BASE_PLUG, ELBOW_PLUG, SHOULDER_PLUG, CLAW_PLUG, ROW10_PLUG, USB_A] + JUMPER_CAPS   # (the USB cable has one line in the parts list, pictured by its Mini-B end)

# Part pictures that came out with the engraved code upside down are turned round here.
PART_VIEWS = {'R1': {'roll': 180}, 'B1': {'roll': 180}, 'B2': {'roll': 180}, 'B8': {'roll': 180}, 'T2': {'roll': 180},   # (T2: its code read upside down, Lee 15 Oct 2026)
              'Base Motor': {'dir': [0.62, 0.42, -0.66], 'roll': 180},             # motors from the side that carries the label
              'Elbow Motor': {'dir': [0.4, -0.8, -0.45]}, 'Shoulder Motor': {'dir': [0.4, 0.8, 0.45]}, 'Claw Motor': {'dir': [-0.8, 0.45, -0.4], 'roll': 180}}

# The coloured dot on three of the servos tells them apart (TechBox's Testing Checklist); a motor's label says which (Lee, 14 Oct 2026).
DOT = {'Elbow Motor': 'Black Dot', 'Shoulder Motor': 'White Dot', 'Claw Motor': 'Blue Dot'}
dotted = lambda name: f'{name} ({DOT[name]})' if name in DOT else name

# The parts list after the title page, as the published guides lay it out (Lee, 14 Oct 2026): one band per kind of part, with
# the quantity, the name (and its size or dot as a tag) and the picture, grouped by kind, each kind in a colour of its own.
# page, heading, icon, band colour, halo colour round the picture, which part names
WOOD_BAND, WOOD_HALO = '#dbe4ef', '#8ea6c4'   # the wood parts' bands: blue-grey, so the wood stands out (the orange was too close to it: Lee, 16 Oct 2026)
PART_GROUPS = [
    ('Parts List', 'Electronics', 'electronics', '#f9c0c0', '#ec8d8d', lambda n: n in ('Nano I/O Module', 'Nano Board', 'Joystick', 'Breadboard Wire (F-F)', 'USB Cable', 'Servo Extension Wire')),
    ('Parts List', 'Motors', 'motors', '#d8edc6', '#a3cf84', lambda n: n.endswith('Motor')),
    ('Parts List', 'Screws', 'screws', '#c4e8e5', '#88cfc8', lambda n: n.endswith('Hex Screw')),
    ('Parts List (Cont.)', 'Rotating base', 'wood', WOOD_BAND, WOOD_HALO, lambda n: re.fullmatch(r'R\d+', n)),
    ('Parts List (Cont.)', 'Base and controller', 'wood', WOOD_BAND, WOOD_HALO, lambda n: re.fullmatch(r'B\d+', n)),
    ('Parts List (Cont.)', 'T1 / T2 block', 'wood', WOOD_BAND, WOOD_HALO, lambda n: re.fullmatch(r'T\d+', n)),
    ('Parts List (Cont. 2)', 'Arm', 'wood', WOOD_BAND, WOOD_HALO, lambda n: re.fullmatch(r'A\d+', n)),
    ('Parts List (Cont. 2)', 'Claw', 'wood', WOOD_BAND, WOOD_HALO, lambda n: re.fullmatch(r'C\d+', n)),
]


def parts_list(parts):
    """The parts list's pages for the parts this guide shows (see Guide(parts_list=)); empty groups and pages are left out."""
    natural = lambda p: [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', p['name'])]
    pages, used = {}, set()
    for page, title, icon, colour, halo, wanted in PART_GROUPS:
        items = [p for p in parts if wanted(p['name']) and p['name'] not in used]          # (in the order the build uses them...)
        if icon in ('wood', 'screws'):                              # (... but codes and sizes in order: A1, A2 ... A13; 6, 10, 16 mm)
            items.sort(key=natural)
        if not items:
            continue
        used.update(p['name'] for p in items)
        if icon == 'wood':                                          # "Arm (A1 - A13)"
            title = f"{title} ({items[0]['name']}{' - ' + items[-1]['name'] if len(items) > 1 else ''})"
        rows = []
        for p in items:
            name, tag = p['name'], DOT.get(p['name'])
            if name.endswith('Hex Screw'):                          # "6mm" as the tag, "Hex Screw" as the name
                tag, name = name.split(' ', 1)
            rows.append(dict(name=name, qty=p['qty'], picture=p['picture'], **({'tag': tag} if tag else {})))
            p['group'] = title
        pages.setdefault(page, []).append(dict(title=title, icon=icon, colour=colour, halo=halo, items=rows))
    left = [p for p in parts if p['name'] not in used]
    if left:                                                        # (a part no group names still gets listed, on the last page)
        other = dict(title='Other parts', icon='wood', colour='#e8e8e8', halo='#bdbdbd', items=[dict(name=p['name'], qty=p['qty'], picture=p['picture']) for p in left])
        if pages:
            pages[list(pages)[-1]].append(other)
        else:
            pages['Parts List'] = [other]
    # (named in order, whichever pages this guide has: a guide for the claw alone gets "Parts List", "Parts List (Cont.)")
    names = ['Parts List'] + [f"Parts List (Cont.{'' if k == 1 else f' {k}'})" for k in range(1, len(pages))]
    return [dict(name=name, groups=groups) for name, groups in zip(names, pages.values())]


# The engraved code on each wood part (which way it faces, where it is): the camera prefers a side from which it can be read.
CODES = {i: (c['normal'], c['centre']) for i, c in json.load(open(HERE / 'engraved-codes.json')).items() if not i.startswith('_')}

g = Guide(HERE, title='Mini Robot Arm (MRA)', part='Full Build', names=NAMES, part_views=PART_VIEWS, part_of=PART_OF, unlisted=UNLISTED,
          hover_names={JOY_LEFT: 'Left Joystick', JOY_RIGHT: 'Right Joystick'},   # (as their labels say; both 'Joystick' in the parts list: Lee, 16 Oct 2026)
          codes=CODES, hero_azimuth=135,                            # the finished model: from the front, on the R5 side, above
          # the title page: the camera of Lee's screenshot of 14 Oct 2026 (solved from where nine engraved codes are in it; within 6 px)
          # (it suits frames at least 1.7 times as wide as tall; on narrower ones the finished model's view is used; the USB
          # cable's ends are left off it: with the cable hidden behind the base, its A end looked like a stray plug)
          start_view=dict(dir=[0.518, 0.3056, -0.7989], target=[278.5, 167.7, 189.6], radius=133.2, shift=0, min_aspect=1.7, hide=['USB_B', 'USB_A']),
          # the Completed View from the same camera (Lee, 14 Oct 2026): from where it stands, turned to face the model, which then
          # sits in the middle (there is no title beside it)
          end_view=dict(dir=[0.6374, 0.337, -0.6929], target=[219.7, 148.5, 164.9], radius=140.9, shift=0, min_aspect=1.2),   # (with the USB cable: Lee, 14 Oct 2026)
          parts_list=parts_list,
          review_notes=False,                                       # (past review: Lee, 14 Oct 2026; the notes and their switch are hidden)
          copyright_line='\u00a9 TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')

# ---------------------------------------------------------------- wires
# Every wire's centre line in the CAD is in wire-paths.json. A servo lead is three wires (brown on G, red on V,
# orange on S) ending in a plug; the plug rides on the loose end of the lead until a step plugs it in.
paths = W.load(HERE / 'wire-paths.json')
LEAD_COLOURS = ['lead_brown', 'lead_red', 'lead_orange']          # G, V, S
JUMPER_COLOURS = dict(GND='wire_yellow', V='wire_green', X='wire_blue', Y='wire_purple')


def lead_wires(name, motor_name):
    ids = [f'{name} {c}' for c in ('brown', 'red', 'orange')]
    for wire_id, colour in zip(ids, LEAD_COLOURS):
        g.wire(wire_id, colour, 0.5, name=motor_name)
    return ids


def routes(ids, lines, **ends):
    """One route per wire of a lead."""
    return {wire_id: W.route(line, **ends) for wire_id, line in zip(ids, lines)}


# --- the base motor's lead: straight up at first, then in the L-shaped slot in R4, then plugged into row 5
base_chain = paths['chains'][BASE_MOTOR]
base_plug = W.plug(paths['plugs'][BASE_PLUG], g_towards=[1, 0, 0])
BASE_LEAD = lead_wires('base', 'Base Motor')
exit_ = np.array(base_chain['leaves_servo_at'])
up_line = W.join(W.straight(exit_, [0, 0, 1], 3.0), W.rounded([exit_ + [0, 0, 3], exit_ + [0, 0, 8], exit_ + [0, 52, 8]], radius=5)[1:])
base_up, BASE_PLUG_UP = W.loose_lead(up_line, base_chain['across'], base_plug)
in_slot = W.along(base_chain['middle'], 0, 55.5)                   # as far as the pocket of the L-shaped slot
out = in_slot[-1]
slot_line = W.join(in_slot, W.rounded([out, out + [-2.4, 1.6, -1.8], out + [-8, 2.2, -2.5], out + [-22, 2.2, -2.5]], radius=4)[1:])
base_slot, BASE_PLUG_SLOT = W.loose_lead(slot_line, base_chain['across'], base_plug)
# on its way into the slot the lead lies over R4's top edge, above the slot's mouth
over_line = W.join(W.straight(exit_, [0, 0, 1], 3.0), W.rounded([exit_ + [0, 0, 3], exit_ + [0, 0, 9], [160.0, 150.0, 154.0], [137.0, 151.0, 141.7], [111.4, 151.0, 141.7]], radius=6)[1:])
base_over, BASE_PLUG_OVER = W.loose_lead(over_line, base_chain['across'], base_plug)
# ... then at the foot of the slot's stem, before it moves across into the pocket (so it never cuts the corner of the L)
along_slot = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(slot_line, axis=0), axis=1))])
rise = np.clip((along_slot - 30.0) / 20.0, 0.0, 1.0)
stem_line = slot_line + (rise * rise * (3 - 2 * rise))[:, None] * np.array([0.0, 6.3, -1.76])
base_stem, BASE_PLUG_STEM = W.loose_lead(stem_line, base_chain['across'], base_plug)
IN_SLOT = 57.0                                                     # mm along the lead to where R4's slot holds it
base_plugged = W.plugged_lead(base_chain['middle'], base_chain['across'], base_plug)


# --- the elbow and shoulder motors' leads. Each stands straight out of the back of its motor at first: folded back over the
# end of the motor, so that the clamp plate can be passed over the plug and slid down the lead. Once the clamp plate is screwed
# on, the lead is moved into the hook-shaped slot in the ear of the side plate and its plug hangs just past the slot. The two
# plugs go onto rows 6 and 9 in the final wiring: W.plugged_lead(lead['chain']['middle'], lead['chain']['across'], lead['plug']).
def sagging(chain, from_mm, to_mm, sag, upto_mm=None):
    """The CAD's centre line of a lead with the stretch between `from_mm` and `to_mm` along it hanging down: its height runs
    straight from one end of the stretch to the other, less `sag` mm in the middle (the way a lead hangs between the back of
    its motor and the slot that holds it). The run in plan is the CAD's. Returns the chain and, if `upto_mm` is given, how far
    along the new line the point is that was `upto_mm` along the old one."""
    P = np.array(chain['middle'], float)
    lengths = lambda X: np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(X, axis=0), axis=1))])
    s = lengths(P)
    y0, y1 = np.interp(from_mm, s, P[:, 1]), np.interp(to_mm, s, P[:, 1])
    u = np.clip((s - from_mm) / (to_mm - from_mm), 0.0, 1.0)
    hang = y0 + (y1 - y0) * u - sag * np.sin(np.pi * u)
    ease = lambda t: np.clip(t, 0.0, 1.0) ** 2 * (3 - 2 * np.clip(t, 0.0, 1.0))
    w = ease((s - from_mm) / 18.0) * ease((to_mm - s) / 18.0)        # (eased in and out over 18 mm, so the lead has no corner)
    Q = P.copy()
    Q[:, 1] = P[:, 1] + w * (hang - P[:, 1])
    new = dict(chain, middle=Q.round(3).tolist())
    if upto_mm is None:
        return new
    return new, float(np.interp(upto_mm, s, lengths(Q)))


def side_lead(name, motor, plug_id, outwards, through_slot_mm, past_slot, chain=None):
    """outwards: -1 or 1, the z direction out of the turret on the motor's side. through_slot_mm: how far along the CAD's
    lead the hook-shaped slot has been passed. past_slot: corner points of the loose end beyond that, relative to it.
    chain: the lead's centre line, if not the CAD's."""
    chain, plug, ids = chain or paths['chains'][motor], W.plug(paths['plugs'][plug_id], g_towards=[1, 0, 0]), lead_wires(name, NAMES[motor])
    exit_, out = np.array(chain['leaves_servo_at']), np.array([0.0, 0.0, outwards])
    behind = exit_ + out * 8.4                                     # 3.6 mm clear of the back of the motor
    line = W.join(W.straight(exit_, [1, 0, 0], 3.0),
                  W.rounded([exit_ + [3, 0, 0], exit_ + [6, 0, 0], behind + [6, 0, 0], behind + [-9.6, 0, 0], behind + [-9.6, 0, 0] + out * 42], radius=3)[1:])
    loose, plug_loose = W.loose_lead(line, chain['across'], plug)
    in_slot = W.along(chain['middle'], 0, through_slot_mm)
    hooked_line = W.join(in_slot, W.rounded([in_slot[-1]] + [in_slot[-1] + np.array(p, float) for p in past_slot], radius=4)[1:])
    hooked, plug_hooked = W.loose_lead(hooked_line, chain['across'], plug)
    ends, held = dict(a=motor, b=plug_id), through_slot_mm + 2.5        # (past the hook the lead is held: it does not follow the plug)
    return dict(chain=chain, plug=plug, wires=ids, motor=motor, plug_id=plug_id, loose=routes(ids, loose, b_at=plug_loose, **ends), plug_loose=plug_loose,
                hooked=routes(ids, hooked, b_at=plug_hooked, b_from=held, **ends), plug_hooked=plug_hooked, held=held)


def over_the_base_lead(chain, plug_top):
    """The elbow motor's lead as the CAD has it as far as just past the hook-shaped slot in R5, then up over the arch that the
    base motor's lead makes over to row 5 (about 8 mm above it, middle wire to middle wire) and straight down into row 6, beside it.
    (The CAD takes it under that arch; on the real build it goes over it: Lee, 15 Oct 2026.)"""
    keep = W.along(chain['middle'], 0, 125.0)
    turn = W.along(chain['middle'], 0, 132.0)[-1]
    top = np.asarray(plug_top, float)
    over = [[101.0, 178.0, 130.5], [89.0, 188.0, 136.0], [76.0, 191.5, 140.5], [64.0, 190.0, top[2]], [56.0, 183.0, top[2]], [top[0], 172.0, top[2]]]
    middle = W.join(keep, W.rounded([keep[-1], turn, *over, top], radius=12)[1:])   # (wide bends, as a lead lies)
    return dict(chain, middle=np.asarray(middle, float).tolist())   # (unrounded: as far as the hook it is the CAD's, to the last digit)


ELBOW_LEAD = side_lead('elbow', ELBOW_MOTOR, ELBOW_PLUG, -1, 113.5, [[-1.0, 0.0, 2.0], [-5.0, 0.3, 4.0], [-22.0, 0.3, 4.0]])
ELBOW_LEAD['chain'] = over_the_base_lead(ELBOW_LEAD['chain'], ELBOW_LEAD['plug']['tops'][1])   # (for the final wiring; loose and hooked as before)
# The shoulder motor's lead arcs up high in the CAD, over the lobe of R6 where the R6 - A11 screw goes in, so the screw seemed to
# pass through it (Lee, 14 Oct 2026). It hangs down instead, between the back of the motor and the hook-shaped slot: 15 mm or
# more below the screw's axis all the way, at its lowest about 150 mm high, beyond the back of the motor (clear of it). Where it
# leaves the motor and where it goes through the hook is as the CAD has it.
SHOULDER_CHAIN, SHOULDER_THROUGH = sagging(paths['chains'][SHOULDER_MOTOR], 8.0, 139.0, 14.0, upto_mm=139.5)
SHOULDER_LEAD = side_lead('shoulder', SHOULDER_MOTOR, SHOULDER_PLUG, 1, SHOULDER_THROUGH, [[-1.0, -1.0, -1.5], [-5.0, -1.5, -3.0], [-22.0, -1.5, -3.0]], chain=SHOULDER_CHAIN)
for lead, motor, plug_id in ((ELBOW_LEAD, ELBOW_MOTOR, ELBOW_PLUG), (SHOULDER_LEAD, SHOULDER_MOTOR, SHOULDER_PLUG)):     # plugged in: along its chain (the CAD's, or as above)
    lead['plugged'] = routes(lead['wires'], W.plugged_lead(lead['chain']['middle'], lead['chain']['across'], lead['plug']), a=motor, b=plug_id, b_from=lead['held'])


# On to its row in the final wiring (Steps 98 and 99), in three beats with the lead in step (Lee, 15 Oct 2026: in one move the
# elbow motor's lead swept through the base motor's, and the shoulder motor's plug turned right over with a kink in its lead):
# off the hook, then upright over its row where its plugged lead comes straight down to it, then down onto the row.
def lead_stage(lead, upto_mm, corners=(), end_across=None, fan_mm=10.0):
    """A side lead on its way from the hook to its row: the CAD's centre line as far as `upto_mm` along it, then through
    `corners`, its plug loose on the end (end_across: the way the flat lead and the plug are wide there). (routes, plug pose)."""
    line = W.along(lead['chain']['middle'], 0, upto_mm - (5.0 if len(corners) else 0.0))
    if len(corners):                                   # (the point `upto_mm` along is a corner too, rounded like the rest)
        at = W.along(lead['chain']['middle'], 0, upto_mm)[-1]
        line = W.join(line, W.rounded([line[-1], at, *[np.asarray(c, float) for c in corners]], radius=5)[1:])
    lines = W.ribbon(line, lead['chain']['across'], pitch=1.02, n=3, end_pitch=lead['plug']['pitch'], fan_mm=fan_mm, end_across=end_across)
    pose = W.plug_pose(lead['plug'], lines[1][-1], lines[1][-1] - lines[1][-2], lines[2][-1] - lines[0][-1])
    return routes(lead['wires'], lines, a=lead['motor'], b=lead['plug_id'], b_at=pose, b_from=lead['held']), pose


def cut_lead(lead, upto_mm=None, height=None, fan_mm=12.0):
    """The lead plugged in, cut short `upto_mm` along it, or where it comes straight down to its row `height` mm above the row's
    pins (the same three wires, so that from there it only has to go on), its wires spreading to the plug's contacts there; the
    plug on the end, in line with the lead."""
    lines = [np.asarray(l, float) for l in W.plugged_lead(lead['chain']['middle'], lead['chain']['across'], lead['plug'])]
    mid = lines[1]
    if height is not None:
        y = lead['plug']['tops'][1][1] + height
        k = max(i for i in range(1, len(mid)) if mid[i - 1][1] >= y >= mid[i][1])      # (on its last way down)
        f = (mid[k - 1][1] - y) / (mid[k - 1][1] - mid[k][1])
    else:
        along = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(mid, axis=0), axis=1))])
        k = int(np.searchsorted(along, upto_mm))
        f = (upto_mm - along[k - 1]) / (along[k] - along[k - 1])
    cut = [np.vstack([l[:k], l[k - 1] + (l[k] - l[k - 1]) * f]) for l in lines]
    d = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(cut[1], axis=0), axis=1))])
    u = np.clip((d - (d[-1] - fan_mm)) / fan_mm, 0.0, 1.0)
    side = (cut[2] - cut[0]) / 2
    width = np.linalg.norm(side, axis=1)[:, None]
    grow = 1 + (lead['plug']['pitch'] / width - 1) * (u * u * (3 - 2 * u))[:, None]
    cut = [cut[1] - side * grow, cut[1], cut[1] + side * grow]
    pose = W.plug_pose(lead['plug'], cut[1][-1], cut[1][-1] - cut[1][-2], cut[2][-1] - cut[0][-1])
    return routes(lead['wires'], cut, a=lead['motor'], b=lead['plug_id'], b_at=pose, b_from=lead['held']), pose


over_row = lambda lead, height: cut_lead(lead, height=height)


def turned_as(pose, t):
    """The plug turned as in `pose`, moved by `t` (its middle contact `t` mm from its seat): for a place it passes through."""
    return via(dict(pose, t=[float(x) for x in t])) if isinstance(pose, dict) else via(t)


# The elbow motor's lead goes over the arch of the base motor's lead to row 6 (the two run side by side down to the rows), so its
# plug is drawn off the hook and up, then over that arch along the way its lead will lie, the plug leading, and let down beside
# the base motor's lead: each stage the plugged lead cut short, so the lead only grows along its own way.
ELBOW_OFF, T_ELBOW_OFF = cut_lead(ELBOW_LEAD, 172.0)                          # (off the hook and up to the top of the arch)
ELBOW_ALONG = {mm: cut_lead(ELBOW_LEAD, mm)[1] for mm in (150.0, 190.0, 205.0)}   # (where the plug passes, on its way over)
ELBOW_UP, T_ELBOW_UP = over_row(ELBOW_LEAD, 41.0)
# The shoulder motor's plug hangs on its hook the other way round from the way it goes onto row 9 (orange on top, its lead coming
# in level): 169 degrees to turn in all. Off the hook its lead dips towards the row, so that the plug is half-way round there
# (85 degrees), and it turns the rest (83) as it goes up over the joysticks' wires and stands up over the row: in one move it
# had turned right over at once, its lead kinking. (It is still turned 23 degrees about its lead over the row, as the plugged
# lead twists into it; it straightens as it goes down.)
SHOULDER_UP, T_SHOULDER_UP = over_row(SHOULDER_LEAD, 41.0)
SHOULDER_OFF, T_SHOULDER_OFF = lead_stage(SHOULDER_LEAD, 132.0, [[112.0, 170.0, 158.0], [104.0, 172.0, 149.0], [98.0, 166.0, 155.5]], end_across=[0.26, 0.6, 0.76])


# --- the claw motor's lead, and the servo extension wire that carries it on to row 10. The motor's own lead is short and ends
# in a plug. It stands straight up out of the motor at first (it goes through C3 ahead of the motor), is fed back through the
# hole in the end of C3 and, once the claw is on the arm, through the two square holes in A6. Its plug is then held above R4,
# where the coupler of the extension is pushed onto it. Last, the join goes down inside the turret behind R4 (where the CAD
# has it) with the extension in R4's L-shaped slot, and the extension's other plug goes onto row 10.
def spread(lines, pitch, over_mm=10.0):
    """The three wires of a lead spread out to `pitch` at their first end, over `over_mm` (into the contacts of a plug there)."""
    low, middle, high = (np.asarray(line, float) for line in lines)
    d = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(middle, axis=0), axis=1))])
    u = np.clip(1 - d / over_mm, 0.0, 1.0)
    side = high - low
    width = np.linalg.norm(side, axis=1)
    more = ((pitch - width / 2) * u * u * (3 - 2 * u) / width)[:, None] * side
    return [low - more, middle, high + more]


claw_chain = paths['chains'][CLAW_MOTOR]                           # (the CAD's centre line runs on through the join to row 10)
claw_plug = W.plug(paths['plugs'][CLAW_PLUG], g_towards=[0, 0, 1])
CLAW_LEAD = lead_wires('claw', 'Claw Motor')
claw_along = lambda from_mm, to_mm: W.along(claw_chain['middle'], from_mm, to_mm)
ABOVE_R4 = np.array([-33.0, 31.0, 2.0])                            # where the join is made, from where the CAD has it: level, above the top edge of R4


def claw_lead(line, tail=None):
    """The claw motor's lead along `line`, loose, with its plug on the end: (a route for each wire, the plug's pose).
    With `tail`, the lead carries on along it into the plug at the tail's end. It is carried along `line` without twisting,
    so that every route looks the same for as far as they share the CAD's centre line, and turned over the length of the
    tail to meet the plug's contacts."""
    if tail is None:
        lines, pose = W.loose_lead(line, claw_chain['across'], claw_plug)
    else:
        first = W.ribbon(line, claw_chain['across'], pitch=1.02)
        last = W.ribbon(tail, first[2][-1] - first[0][-1], pitch=1.02, end_pitch=claw_plug['pitch'], fan_mm=10.0, end_across=claw_plug['across'])
        lines, pose = [W.join(a, b) for a, b in zip(first, last)], (np.asarray(tail[-1]) - claw_plug['tops'][1]).round(3).tolist()
    # once the lead is through a hole it is held there: the part before the hole stays put while the plug is moved on
    length = W.length(lines[1])
    held = next((mm for mm, needs in ((210, 212), (149, 150), (62, 64)) if length >= needs), None)
    return routes(CLAW_LEAD, lines, a=CLAW_MOTOR, b=CLAW_PLUG, b_at=pose, b_from=held), pose


claw_exit = np.array(claw_chain['leaves_servo_at'])
through_a6 = claw_along(0, 210)                                    # as the CAD has it, as far as just through the lower hole in A6
below_a6, held = through_a6[-1], claw_plug['tops'][1] + ABOVE_R4
CLAW = dict(
    # straight up for 55 mm, folded against the end of the motor: there it passes through the notch in the end of C3's cut-out
    up=claw_lead(W.rounded([claw_exit, claw_exit + [0, 0, -0.64], claw_exit + [0, 55, -0.64]], radius=1)),
    # the CAD's centre line as far as 88 mm: over the motor, down through the hole in the end of C3 and back under C3
    in_c3=claw_lead(claw_along(0, 88)),
    # as far as 176 mm: along the forearm, through the upper hole in A6 and down over its engraved face, between the two A9
    in_a6=claw_lead(claw_along(0, 176)),
    # through the lower hole too, then under the bottom edge of A6 and forward to where the plug is held above R4
    above_r4=claw_lead(through_a6, W.rounded([below_a6, below_a6 + [0.8, -3.4, 0], [183.5, 162.5, 145.0], held + [38, 0, 0], held], radius=5)),
    # all of it: down inside the turret in front of R3 and forward into the plug, where the CAD has the join
    home=claw_lead(through_a6, W.join([below_a6], claw_along(210, 265.5), [claw_plug['tops'][1]])))


def by_way_of(*places):
    """A move of the claw motor's lead through in-between places to the last one (each as claw_lead() gives it, or a number: the
    lead as far as that many mm along the CAD's centre line), so that its plug is seen to go through a hole rather than through
    the wood: what place() wants as wires_done= and ride=."""
    places = [claw_lead(claw_along(0, p)) if isinstance(p, (int, float)) else p for p in places]
    return dict(wires_done={wire_id: [place[0][wire_id] for place in places] for wire_id in CLAW_LEAD}, ride={CLAW_PLUG: [place[1] for place in places]})


extension_plug, row10_plug = W.plug(paths['plugs'][EXTENSION_PLUG], g_towards=[0, 0, 1]), W.plug(paths['plugs'][ROW10_PLUG], g_towards=[1, 0, 0])
EXTENSION = [f'extension {c}' for c in ('brown', 'red', 'orange')]  # (the same colours as the servo leads, Lee 14 Oct 2026; drawn as a flat lead)
for wire_id, colour in zip(EXTENSION, LEAD_COLOURS):
    g.wire(wire_id, colour, 0.5, name='Servo Extension Wire')
extension_from = extension_plug['tops'][1]


def extension(lines, at=None, row10_at=None):
    """Routes for the extension's three wires. at, row10_at: where its two plugs were when the lines were drawn, if not at their seats."""
    return routes(EXTENSION, spread(lines, extension_plug['pitch']), a=EXTENSION_PLUG, b=ROW10_PLUG, a_at=at, b_at=row10_at)


# loose: about 100 mm out of the coupler's end, towards the controller, sagging a little (35 mm looked too short: Lee). It runs
# between the two joysticks, above their wires and knobs.
EXT_START = extension_from + ABOVE_R4
ext_loose, ROW10_PLUG_LOOSE = W.loose_lead(W.rounded([EXT_START, EXT_START + [-40, 0, 0], EXT_START + [-75, -6, 0], EXT_START + [-100, -8, 0]], radius=12),
                                           extension_plug['across'], row10_plug)
# (The CAD models the extension twisted, so its centre line winds round a helix: smoothed, the flat lead lies in a clean curve.)
ext_plugged = W.plugged_lead(W.join([extension_from], W.smoothed(claw_along(293.0, 434.5), 24.0), [row10_plug['tops'][1]]), extension_plug['across'], row10_plug)
EXTENSION_LEAD = dict(loose=extension(ext_loose, at=ABOVE_R4.tolist(), row10_at=ROW10_PLUG_LOOSE), plugged=extension(ext_plugged))
# In the slot: as the CAD has it as far as the pocket of the L-shaped slot in R4, then lying on B2 past R6 (REST, below). (Laid
# out across the module, as it once was, it lay against the right joystick's wires and went through them on its way to row 10:
# Lee, 14 Oct 2026; hanging beside the module, as it was next, it looked plugged into B2 and was half its length: Lee, 15 Oct.)
# The plugged extension runs under the shoulder motor's wire and over the jumper wires, so Step 100 takes the plug up under the
# shoulder motor's wire where there is no jumper wire (beside the module), across above the jumper wires beside the shoulder
# motor's wire, and down onto row 10: a route for each stage.
ext_pocket = W.join([extension_from], claw_along(293.0, 301.5))
IN_POCKET = W.length(ext_pocket) + 2.0                               # (held in the slot up to here: it does not follow the plug)
EXT_TOP = np.asarray(row10_plug['tops'][1], float)                   # the top of the row 10 plug's middle contact, seated
P0 = ext_pocket[-1]                                                  # where the extension leaves the slot in R4


# The stem of the L-shaped slot in R4 (z 140.6 - 142.7, R4 being x 131.9 - 134.9) is narrower than the flat lead is wide, so on
# its way down the stem (Step 97) the lead goes through R4 turned on edge, its width up and down, and turns flat again in the pocket.
STEM_Z = 141.66


def edge_on(lines, x_in=135.6, x_out=131.6, turn_in=3.6, turn_out=2.5):
    """The lead turned on edge (wide up and down) from x_in to x_out, turning over turn_in mm before and turn_out mm after."""
    low, mid, high = (np.asarray(line, float) for line in lines)
    t = np.gradient(mid, axis=0)
    t /= np.linalg.norm(t, axis=1)[:, None]
    smooth = lambda u: np.clip(u, 0.0, 1.0) ** 2 * (3 - 2 * np.clip(u, 0.0, 1.0))
    w = smooth((x_in + turn_in - mid[:, 0]) / turn_in) * smooth((mid[:, 0] - (x_out - turn_out)) / turn_out)
    half = (high - low) / 2
    for k in np.nonzero(w > 0)[0]:
        up = np.array([0.0, -1.0, 0.0]) + t[k] * t[k][1]                  # (brown, the wire on the -z side, on top: away from the base motor's lead)
        up /= np.linalg.norm(up)
        roll = np.arctan2(np.cross(half[k], up) @ t[k], half[k] @ up)
        half[k] = W._about(t[k], roll * w[k]) @ half[k]
    return [mid - half, mid, mid + half]


def ext_stage(corners, t):
    """The extension from the pocket in R4 along `corners` into its row 10 plug standing upright `t` mm from its seat (Step 100)."""
    end = EXT_TOP + np.asarray(t, float)
    line = W.join(ext_pocket, W.rounded([P0, *[np.asarray(c, float) for c in corners], end + [0.0, 9.0, 0.0], end], radius=5)[1:])
    lines = spread(W.plugged_lead(line, extension_plug['across'], row10_plug), extension_plug['pitch'])
    return routes(EXTENSION, lines, a=EXTENSION_PLUG, b=ROW10_PLUG, b_at=[float(x) for x in t], b_from=IN_POCKET)


def ext_lying(corners, start=None, at=None, radius=5.0, end_across=None):
    """The extension along `corners` with its row 10 plug lying loose on the end, in line with it (end_across: the way the flat
    lead and the plug are wide there, e.g. level so the plug lies flat): from the pocket in R4, or from the coupler raised to `at`
    before the join goes down behind R4 (`start`: the points the lead follows from the coupler, close bends; it is turned on edge
    through R4). Returns (the routes, the plug's pose), the pose being the one to give the plug in that view."""
    c = [np.asarray(p, float) for p in corners]
    if start is None:
        line = W.join(ext_pocket, W.rounded([P0, *c], radius=radius)[1:])
    else:
        start = [np.asarray(p, float) for p in start]
        line = W.join(W.rounded(start[:-1], radius=1.5), W.rounded([*start[-2:], *c], radius=radius)[1:])
    lines = W.ribbon(line, extension_plug['across'], pitch=1.02, n=3, end_pitch=row10_plug['pitch'], fan_mm=10.0, end_across=end_across)
    pose = W.plug_pose(row10_plug, lines[1][-1], lines[1][-1] - lines[1][-2], lines[2][-1] - lines[0][-1])
    lines = spread(lines, extension_plug['pitch'])
    if start is not None:
        lines = edge_on(lines)
    return routes(EXTENSION, lines, a=EXTENSION_PLUG, b=ROW10_PLUG, a_at=at, b_at=pose, **({} if start is not None else {'b_from': IN_POCKET})), pose


def through_stem(raised, y_at_r4):
    """From the coupler raised `raised` mm, across to the stem of R4's slot and through R4 on edge, `y_at_r4` mm up (the
    corners after it turn the lead away from the base motor's lead, which comes out of the slot beside it)."""
    c = extension_from + [0.0, raised, 0.0]
    return [c, [138.3, c[1] + (y_at_r4 - c[1]) * 0.15, 144.0], [136.6, c[1] + (y_at_r4 - c[1]) * 0.7, 142.0],
            [135.6, y_at_r4 + 0.2, STEM_Z], [131.6, y_at_r4, STEM_Z], [130.6, y_at_r4, STEM_Z]]


# At rest, from Step 97c until Step 100 (Lee, 15 Oct 2026: it had looked plugged into B2, and it must keep the length it has as
# Step 97 opens): out of the slot, down onto B2 in front of R4 and rightwards along it past R6's front edge, its plug lying flat
# on B2 at the foot of R6, under the shoulder motor's lead where that lead loops round the outside of R6. 99.8 mm, as Step 97
# opens with 100.6.
REST, T_REST = ext_lying([[124.5, 133.0, 147.0], [118.2, 128.3, 151.5], [113.8, 111.5, 154.0], [111.5, 98.0, 155.5], [106.9, 94.5, 159.0],
                          [101.4, 94.5, 165.8], [101.9, 94.5, 173.6], [108.7, 94.75, 179.4], [113.5, 95.12, 183.25], [121.0, 95.12, 183.4]],
                         radius=10.0, end_across=[0.02, 0.0, -0.9998])
# Step 97 takes the plug there in front of R6 (it may not come down through the shoulder motor's lead, which loops round the
# outside of R6 above its rest): held up beside R6's front edge as the join goes over R4, then low over B2 as the join goes down,
# then laid down and slid in under that lead. The wire keeps its length on the way (97 - 100 mm).
OVER_R4, T_HELD_HIGH = ext_lying([[127.0, 166.0, 143.5], [118.0, 169.0, 160.0], [108.0, 173.0, 174.0], [90.0, 180.0, 180.0], [64.0, 186.0, 183.0]],   # (high, over the joysticks' wires, and out beyond the hooked shoulder plug, not over it)
                                 start=through_stem(float(ABOVE_R4[1]), 165.5), at=[0.0, float(ABOVE_R4[1]), 0.0])
IN_STEM, T_HELD_LOW = ext_lying([[128.4, 134.1, 144.3], [122.0, 131.0, 149.0], [116.0, 119.0, 153.0], [112.0, 100.0, 155.5], [106.9, 94.5, 159.0],
                                 [101.4, 94.5, 165.8], [100.5, 99.0, 173.0], [102.5, 106.0, 179.5], [107.0, 110.0, 183.0]],
                                start=through_stem(2.0, 134.4), at=[0.0, 2.0, 0.0])
T_RISEN = [43.5, 52.0, 3.4]                                          # Step 100: upright beside the module, under and beside the shoulder motor's wire
T_ACROSS, T_OVER = [0.0, 52.0, 3.4], [0.0, 52.0, 0.0]                # over row 10, beside the shoulder motor's wire; right over row 10 (the plug's underside 7 mm over the jumper wires)
UNDER_SHOULDER = [[106.0, 137.0, 145.0], [100.0, 146.0, 150.0]]    # (the shoulder motor's wire is at z 150, y 162 - 177 here)
EXTENSION_LEAD.update(
    rest=REST,
    # Step 97: over the top edge of R4 with the join raised, then down the stem of the slot to its foot as the join goes down
    # behind R4 (the lead on edge in the stem), then across into the pocket as the join goes the last 2 mm down
    over_r4=OVER_R4, in_stem=IN_STEM,
    # Step 100: up beside the plug, passing 4 mm to the side of the shoulder motor's wire, and over the plug's top in a wide turn;
    # then across under the shoulder motor's wire to where that wire is high, up there beside it and over row 10
    risen=ext_stage(UNDER_SHOULDER + [[101.5, 156.0, 154.5], [103.0, 172.0, 155.5], [103.0, 185.0, 157.0], [102.0, 190.5, 157.6], [98.0, 191.5, 158.2], [96.0, 187.0, 158.2]], T_RISEN),
    over_row=ext_stage(UNDER_SHOULDER + [[90.0, 158.0, 154.0], [80.0, 165.0, 156.0], [68.0, 190.0, 157.5], [60.0, 192.0, 157.0]], T_OVER))
# The extension appears a little way off the claw motor's plug, in line with it. (Its parts have no place of their own until
# the join goes down behind R4, so until then they are carried: by the claw motor, which by then is fixed on the arm.)
APART = np.array([-25.0, 0.0, 0.0])


g.part_picture('Servo Extension Wire', add=[ROW10_PLUG], poses={COUPLER: ABOVE_R4.tolist(), EXTENSION_PLUG: ABOVE_R4.tolist(), ROW10_PLUG: ROW10_PLUG_LOOSE},
                wires=[dict(colour=colour, radius=0.5, pts=EXTENSION_LEAD['loose'][wire_id]['pts']) for wire_id, colour in zip(EXTENSION, LEAD_COLOURS)])   # (Lee: the whole wire, not one end)


def lifted(pose, mm):
    """The same pose, raised by mm."""
    return [pose[0], pose[1] + mm, pose[2]] if isinstance(pose, list) else {**pose, 't': [pose['t'][0], pose['t'][1] + mm, pose['t'][2]]}


# --- the joysticks' jumper wires: each joystick arrives wired to the I/O module by four wires
JOY_PIN = {'NAUO104': 'GND', 'NAUO105': 'V', 'NAUO106': 'X', 'NAUO107': 'Y', 'NAUO103': 'GND', 'NAUO108': 'V', 'NAUO109': 'X', 'NAUO110': 'Y'}
jumpers = {JOY_LEFT: [], JOY_RIGHT: []}                            # joystick -> [(wire id, full centre line, cap on the joystick, cap on the module)]
for w in paths['joystick_wires']:
    line = np.array(next(c for c in paths[w['bundle']] if c['solid'] == w['solid'])['points'])
    if np.linalg.norm(line[0] - w['joystick_end']) > np.linalg.norm(line[-1] - w['joystick_end']):
        line = line[::-1]
    joystick = JOY_LEFT if w['bundle'] == 'NAUO112' else JOY_RIGHT
    pin = JOY_PIN[w['joystick_cap']]
    wire_id = f"{'left' if joystick == JOY_LEFT else 'right'} {pin}"
    g.wire(wire_id, JUMPER_COLOURS[pin], 0.625, name='Breadboard Wire (F-F)')
    jumpers[joystick].append((wire_id, line, w['joystick_cap'], w['shield_cap']))


def jumper_routes(joystick, fade=None):
    """The four wires of a joystick: whole (tied to the module at the far end), or fading out over fade=(from_mm, to_mm)
    from the joystick, for while it is in the hand and the module is not shown (Lee, 14 Oct 2026: the wires should be seen
    to run on, not look cut)."""
    if fade is None:
        return {wire_id: W.route(line, a=joystick, b=MODULE) for wire_id, line, _, _ in jumpers[joystick]}
    return {wire_id: W.route(W.along(line, 0, fade[1] + 3), a=joystick, fade=fade) for wire_id, line, _, _ in jumpers[joystick]}


RIGHT_MODULE_CAPS = [cap for _, _, _, cap in jumpers[JOY_RIGHT]]
# The eight breadboard wires are a kit part, but in the CAD only their caps are parts (the wire is drawn): listed by hand,
# pictured as one wire with its two caps (below).
_wire_id, _wire_line, _cap_a, _cap_b = next(w for w in jumpers[JOY_LEFT] if JOY_PIN[w[2]] == 'GND')
g.list_part('Breadboard Wire (F-F)', [_cap_a, _cap_b], 8, after='Joystick')
# Pictured straight (Lee, 15 Oct 2026: not kinked as the CAD routes it): the far cap turned to lie in line with the first, the
# wire its full length between them.
_wire_out, _wire_in = np.asarray(_wire_line[0], float), np.asarray(_wire_line[-1], float)   # (it leaves the first cap along +x; it goes down into the far one)
_wire_far = _wire_out + [W.length(_wire_line), 0.0, 0.0]
g.part_picture('Breadboard Wire (F-F)', poses={_cap_b: turned([0, 0, 1], 90.0, _wire_in.tolist(), (_wire_far - _wire_in).tolist())},
               wires=[dict(colour=JUMPER_COLOURS['GND'], radius=0.625, pts=np.linspace(_wire_out, _wire_far, 72))])
MODULE_ASIDE = [10.0, -16.3, 100.0]

# --- the USB cable: from the Mini-B end, plugged into the Nano Board, out and down to the A end lying on the table
g.wire('usb cable', 'cable_black', 1.75, name='USB Cable')
USB_B_EXIT, USB_A_EXIT = np.array([69.46, 120.94, 223.6]), np.array([69.46, 91.81, 280.0])   # where the cable leaves each end, as materials.json places them
USB_IN = [[[69.46, 120.94, 169.6], [69.46, 120.94, 174.86]]]           # the tip of the plug, to the mouth of the socket in the Nano Board
ON_THE_BENCH = 102.9 - 87.53                                        # (the electronics test is on the bench at the I/O module's underside, the build on the table under B1)


def usb_cable(a_lift=0.0, plug=0.0, a_pose=None):
    """The cable's route, with the A end lifted by a_lift mm from where materials.json has it (or at `a_pose`, a pose
    relative to there) and the Mini-B end `plug` mm out of its socket. (The hover view gets a route of its own: bent from the
    seated one, the cable would fold back.)"""
    a_pose = a_pose or ([0.0, a_lift, 0.0] if a_lift else None)
    start, end = USB_B_EXIT + [0.0, 0.0, plug], apply_pose(a_pose, USB_A_EXIT)
    return {'usb cable': W.route(W.curve(start, [0, 0, 1], end, turn_dir(a_pose, [0, 0, 1]), pull=22.0 if not plug else None), a=USB_B, b=USB_A,
                                 a_at=[0.0, 0.0, plug] if plug else None, b_at=a_pose)}


# Once the arm is built, the cable's A end lies on the table off the far corner of the base, along the arm, where the Completed
# View's camera can see it (Lee, 14 Oct 2026: the cable must be there; straight back, it was hidden behind the base).
A_ON_THE_TABLE = turned([0, 1, 0], 90, USB_A_EXIT, np.array([175.0, 91.81, 255.0]) - USB_A_EXIT)


def riding_in_the_build():
    """What rides with what from the base onwards (the electronics test before it puts the same parts together on the bench)."""
    g.carry([BASE_PLUG], by=BASE_MOTOR, pose=BASE_PLUG_UP)
    for lead, motor, plug_id in ((ELBOW_LEAD, ELBOW_MOTOR, ELBOW_PLUG), (SHOULDER_LEAD, SHOULDER_MOTOR, SHOULDER_PLUG)):
        g.carry([plug_id], by=motor, pose=lead['plug_loose'])
    g.carry([CLAW_PLUG], by=CLAW_MOTOR, pose=CLAW['up'][1])
    g.carry([COUPLER, EXTENSION_PLUG], by=CLAW_MOTOR, pose=(ABOVE_R4 + APART).tolist(), appear=False)
    g.carry([ROW10_PLUG], by=CLAW_MOTOR, pose=compose(APART.tolist(), ROW10_PLUG_LOOSE, paths['plugs'][ROW10_PLUG]['centre']), appear=False)
    for joystick in (JOY_LEFT, JOY_RIGHT):
        g.carry([cap for _, _, cap, _ in jumpers[joystick]], by=joystick)
        # the caps on the module's pins appear with their wires: at once for the left joystick, later for the right
        g.carry([cap for _, _, _, cap in jumpers[joystick]], by=MODULE, appear=joystick == JOY_LEFT)
    g.carry([NANO], by=MODULE)
    # Until it is slid into place the I/O module lies on the table beside the base, held only by its wires.
    g.rest_at([MODULE], MODULE_ASIDE)

# ---------------------------------------------------------------- the build
# ================================================================ ELECTRONICS TEST (begin)
# Before anything is built the electronics are put together on the bench and tried (Lee, 14 Oct 2026): the Nano Board onto
# the I/O module, each joystick wired to the module one wire at a time, the four motors plugged in, then USB and power.
# The module and the joysticks lie where the CAD has them (the base is not there yet, so this is how they lie on the bench,
# the joysticks' pins towards the module, and the jumper wires take the CAD's own routes); the motors stand in a row beside
# the module, each lead arched over the jumper wires to its row. Afterwards the motors are unplugged and everything is put
# aside until the build needs it.
TABLE_Y = 102.9                                                     # the underside of the I/O module
PIN_TOP_Y = 113.8                                                   # the top of every pin on the module (cad_pins.json)
JOY_PRINTED = dict(GND='GND', V='+5V', X='VRx', Y='VRy')
SHIELD_PIN = {JOY_LEFT: dict(GND='A2 G', V='A2 V', X='A2 S', Y='A3 S'), JOY_RIGHT: dict(GND='A0 G', V='A0 V', X='A0 S', Y='A1 S')}   # Lee's pin map
ON_JOYSTICK, ONTO_MODULE = [[14.0, 0.0, 0.0], [0.0, 0.0, 0.0]], [[0.0, 22.0, 0.0], [0.0, 0.0, 0.0]]   # a cap slides along a joystick pin; down onto a module pin


def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def standing(motor, shaft, x, z):
    """The pose that stands a motor on the bench, shaft up and lead towards the module (-X), the middle of its case at x, z."""
    chain, mesh = paths['chains'][motor], g.model.inst[motor]
    c, s = mesh.bounds.mean(0), unit(shaft)
    lead = np.asarray(chain['middle'][3]) - np.asarray(chain['middle'][0])
    lead = unit(lead - s * (lead @ s))
    src = np.column_stack([lead, s, np.cross(lead, s)])
    dst = np.column_stack([[-1.0, 0.0, 0.0], [0.0, 1.0, 0.0], np.cross([-1.0, 0.0, 0.0], [0.0, 1.0, 0.0])])
    R = dst @ src.T
    low = ((mesh.vertices - c) @ R.T + c)[:, 1].min()
    turn = Rotation.from_matrix(R).as_rotvec()
    return turned(unit(turn), np.degrees(np.linalg.norm(turn)), c.round(3), [x - c[0], TABLE_Y - low, z - c[2]])


def bench_lead(ids, motor, pose, plug_info, plug_id, plug_pose=None, height=170.0):
    """A motor's lead on the bench: out of the motor, up over the jumper wires and down into its plug on the module."""
    chain = paths['chains'][motor]
    start = apply_pose(pose, chain['leaves_servo_at'])
    out = turn_dir(pose, unit(np.asarray(chain['middle'][3]) - np.asarray(chain['middle'][0])))
    top = np.asarray(plug_info['tops'][1], float) if plug_pose is None else apply_pose(plug_pose, W.plug(paths['plugs'][plug_id], g_towards=[0, 0, 1])['tops'][1])
    line = W.rounded([start, start + out * 8, [start[0] + out[0] * 8, height, start[2]], [top[0], height, top[2]], top], radius=12)
    lines = W.plugged_lead(line, turn_dir(pose, chain['across']), plug_info)
    return routes(ids, lines, a=motor, b=plug_id, a_at=pose, b_at=plug_pose)


g.place('Begin the electronics with the I/O module. Press the Nano Board into it, its USB socket at the same end as the power socket.',
        move=[NANO], show=[MODULE], labels={NANO: 'Nano Board', MODULE: 'Nano I/O Module'})

for joystick, side, near_side in ((JOY_LEFT, 'left', [1, 1, -1]), (JOY_RIGHT, 'right', [1, 1, 1])):    # (one camera per joystick, from its own side)
    g.place(f'Lay the {side} joystick beside the I/O module, its pins towards the module.', move=[joystick], direction=[0, 1, 0], hover=40,
            labels={joystick: f'{side.title()} Joystick'}, lines=False, focus=[JOY_LEFT, JOY_RIGHT, MODULE], focus_pad=1.0, look_from=near_side)
    for wire_id, line, joy_cap, shield_cap in sorted(jumpers[joystick], key=lambda w: ['GND', 'V', 'X', 'Y'].index(JOY_PIN[w[2]])):
        pin = JOY_PIN[joy_cap]
        tip, top = np.asarray(line[0]) - [2.0, 0.0, 0.0], [float(line[-1][0]), PIN_TOP_Y, float(line[-1][2])]
        g.place(f'Connect {JOY_PRINTED[pin]} on the {side} joystick to {SHIELD_PIN[joystick][pin]} on the I/O module.',
                move=[joy_cap, shield_cap], paths={joy_cap: ON_JOYSTICK, shield_cap: ONTO_MODULE}, lines=False,
                labels=[dict(text=JOY_PRINTED[pin], anchor=tip.round(2).tolist(), id=joystick, ring=False),
                        dict(text=SHIELD_PIN[joystick][pin], anchor=top, id=MODULE, ring=False)],
                wires={wire_id: W.route(line, a=joy_cap, b=shield_cap)}, focus=[JOY_LEFT, JOY_RIGHT, MODULE], focus_pad=1.0, look_from=near_side)

# the four motors, plugged in for the test: each stands beside the module and its plug is pushed onto its row
ROW5_TOP, ROW6_TOP, ROW9_TOP, ROW10_TOP = ([52.574, PIN_TOP_Y, z] for z in (139.464, 142.0, 152.0, 154.6))
claw_on_row10 = W.plug_pose(claw_plug, row10_plug['tops'][1], -row10_plug['cable'], row10_plug['across'])     # (for the test the claw motor goes straight onto row 10)
BENCH = [  # motor, horn, plug, lead, the way its shaft points in the CAD, the plug's pose on its row, name, row, where it stands (z)
    (BASE_MOTOR, BASE_HORN, BASE_PLUG, BASE_LEAD, [0, -1, 0], [0.0, 0.0, 0.0], base_plug, 'Base Motor', '5', ROW5_TOP, 118.0),
    (ELBOW_MOTOR, ELBOW_HORN, ELBOW_PLUG, ELBOW_LEAD['wires'], [0, 0, 1], [0.0, 0.0, 0.0], ELBOW_LEAD['plug'], 'Elbow Motor', '6', ROW6_TOP, 140.0),
    (SHOULDER_MOTOR, SHOULDER_HORN, SHOULDER_PLUG, SHOULDER_LEAD['wires'], [0, 0, -1], [0.0, 0.0, 0.0], SHOULDER_LEAD['plug'], 'Shoulder Motor', '9', ROW9_TOP, 162.0),
    (CLAW_MOTOR, CLAW_HORN, CLAW_PLUG, CLAW_LEAD, [0, -1, 0], claw_on_row10, dict(claw_plug, across=row10_plug['across']), 'Claw Motor', '10', ROW10_TOP, 184.0)]
for motor, horn, plug_id, lead, shaft, on_row, plug_info, name, row, row_top, z in BENCH:
    pose = standing(motor, shaft, 142.0, z)
    g.rest_at([motor, horn], pose)
    g.carry([plug_id], by=MODULE, pose=lifted(on_row, 40.0), appear=False)
    g.place(f'Plug the {name.lower()} into Row {row} for the test. Remember brown to G, red to V, and orange to S.', appear=[motor, horn, plug_id],   # ("Row": Lee, 15 Oct 2026)
            ride={plug_id: on_row}, labels=[dict(id=motor, text=dotted(name)), dict(text=f'Row {row}', anchor=row_top, id=MODULE, ring=False)],
            wires=bench_lead(lead, motor, pose, plug_info, plug_id, plug_pose=None if on_row == [0.0, 0.0, 0.0] else on_row))   # (the claw motor straight onto row 10, no extension: Lee)
g.rest_at([USB_A], [0.0, ON_THE_BENCH, 0.0])
g.place('Connect the USB cable to the Nano Board.', move=[USB_B], appear=[USB_A], direction=[0, 0, 1], hover=30, lines_at=USB_IN,
        labels={USB_B: 'USB Cable'}, wires=usb_cable(ON_THE_BENCH, plug=30), wires_done=usb_cable(ON_THE_BENCH), focus=[MODULE, NANO, USB_B, USB_A], focus_pad=1.15, look_from=[1, 1, 1])
# (USB power only: this version of the kit has no supply for the module's power socket. The checklist is TechBox's, word for word;
# its last line says the cable was unplugged after the test, so the cable is not on the bench from here on: Lee, 14 Oct 2026.)
g.put_away([USB_B, USB_A])
g.note('Testing Checklist\nGo through the following checklist to make sure you have tested each part of your MRA:\n'
       '•  The MRA was powered on by connecting a Mini-USB cable to the nano.\n'
       '•  Moving the left joystick side to side made the Base servo turn.\n'
       '•  Moving the left joystick forward and back made the Shoulder servo (white dot) move.\n'
       '•  Moving the right joystick forward and back made the Elbow servo (black dot) move.\n'
       '•  Moving the right joystick side to side made the Claw servo (blue dot) move.\n'
       '•  Each servo stopped moving when the joystick was released.\n'
       '•  The Mini-USB cable was disconnected from the nano after testing.')   # (the checklist's dot colours are right: Lee, 14 Oct 2026)
# The four plugs come off their rows together, straight up, as they went on (the reverse of four plugging steps; one step,
# as Lee asked, 14 Oct 2026).
g.place('Unplug all four servo motor wires from the I/O module.', ride={b[2]: lifted(b[5], 40.0) for b in BENCH}, lines=False, eye=[ELBOW_PLUG],
        focus=[MODULE, NANO] + [i for b in BENCH for i in b[:3]], focus_pad=1.05,
        caution='Set the servos and the I/O module aside for now. You will use them again in a bit.')
g.put_away([NANO, MODULE, JOY_LEFT, JOY_RIGHT, *JUMPER_CAPS] + [i for b in BENCH for i in b[:3]])
riding_in_the_build()
# ================================================================ ELECTRONICS TEST (end)

# --- rotating base (R1 - R6)
# The horn (36 mm long) does not fit straight through R1's cut-out (12.5 x 22.75 mm): the motor is turned a quarter turn so
# the horn runs along the cut-out, one arm is dipped under the far rim at a slight angle, the motor is levelled, turned back
# a quarter turn about its shaft and set down. Poses found by a collision search against the CAD (worst overlap 0.5 mm).
HORN = [163.67, 89.43, 140.85]                                     # the middle of the horn, on the shaft


def horn_pose(tilt, along, lift, spin=90):
    """The motor and horn spun about the shaft, tilted about the axis across the cut-out, moved along the cut-out and lifted."""
    pose = turned([0, 1, 0], spin, HORN) if spin else [0, 0, 0]
    if tilt:
        pose = compose(turned([1, 0, 0], tilt, HORN), pose, HORN)
    return compose([0, lift, along], pose, HORN)


horn_way = [horn_pose(-28, 1.5, 52), horn_pose(-24, 1.5, 17.45),    # hovering at an angle; down until one tip of the horn is in the cut-out
            via(horn_pose(-12, -4.5, 11.45)), via(horn_pose(-9, -6, 9.95)), via(horn_pose(0, -6, 8.45)),   # under the rim, levelling out
            horn_pose(0, 0, 8.45),                                 # level and centred: R1 is between the horn and the motor's body
            [0, 8.4, 0], [0, 0, 0]]                                # a quarter turn about the shaft, then set down
g.place("Begin with R1. Angle the base motor's servo horn through the slot in R1, then turn the motor and set it into the slot. The wire end of the motor lines up with the notch in the cut-out.",
        move=[BASE_MOTOR, BASE_HORN], show=[R1], path=horn_way, labels={R1: 'R1', BASE_MOTOR: 'Base Motor'},
        lines_at=[[[181.0, 89.4, 140.9], [163.7, 103.0, 124.3]]],
        wires=routes(BASE_LEAD, base_up, a=BASE_MOTOR, b=BASE_PLUG, b_at=BASE_PLUG_UP))
g.place('Slide R2 over the base motor so its tabs enter the slots in R1.', move=[R2])
# Lee's points on the tabs of R3 and R4 (and their mirror images on the other leg); each line ends at the mouth of its slot in R1.
g.place('Add R3.', move=[R3], lines_at=[[[193.6, 96.6, 121.5], [193.6, 102.96, 121.5]], [[193.6, 96.6, 159.7], [193.6, 102.96, 159.7]]])
g.place('Add R4.', move=[R4], lines_at=[[[133.6, 96.6, 121.2], [133.6, 102.96, 121.2]], [[133.6, 96.6, 160.0], [133.6, 102.96, 160.0]]])
g.place('Add R5.', move=[R5])
g.place("Add R6. Keep the base motor's wire up out of the way so it is not trapped.", move=[R6])
# The lead goes into the slot from R4's top edge: over the edge above the slot's mouth first, then down the stem into the pocket.
over, in_stem = (routes(BASE_LEAD, lines, a=BASE_MOTOR, b=BASE_PLUG, b_at=at) for lines, at in ((base_over, BASE_PLUG_OVER), (base_stem, BASE_PLUG_STEM)))
in_pocket = routes(BASE_LEAD, base_slot, a=BASE_MOTOR, b=BASE_PLUG, b_at=BASE_PLUG_SLOT, b_from=IN_SLOT)
g.place("Move the base motor's wire into the L-shaped slot in R4.", eye=[dict(anchor=[133.4, 146.6, 141.7], id=R4)],
        frame=([146.0, 148.0, 147.0], 50.0), look_from=[-1, 1, -1],        # (from the corner nearer R5, where the slot shows: Lee)
        wires_done={wire: [over[wire], in_stem[wire], in_pocket[wire]] for wire in BASE_LEAD},
        ride={BASE_PLUG: [BASE_PLUG_OVER, BASE_PLUG_STEM, BASE_PLUG_SLOT]})

# --- base plates
turret = [R1, R2, R3, R4, R5, R6, BASE_MOTOR, BASE_HORN]
# B2 and B1 go on from underneath: both steps are seen with the base turned over (Lee, 14 Oct 2026), so that B2 is seen sliding
# in between the horn and R5 / R6, and the horn is seen dropping into B1's cut-out.
UNDER_TURRET = dict(flip=True, frame=([163.0, 98.0, 141.0], 82.0))
# (An arrow along the slot in B2 rather than lead lines, Lee, 14 Oct 2026: from the round end of the cut-out, where the motor
# ends up, out through the mouth of the slot towards the motor; just under B2, on the side that is seen.)
g.place('Once R1 - R6 are together, slide B2 in between the servo horn and R5 / R6, until the motor sits in the round cut-out.',   # (Lee's wording, 15 Oct 2026, second note)
        move=[B2], direction=[0, 0, 1], hover=60, labels={B2: 'B2', BASE_HORN: 'Base Motor'}, **UNDER_TURRET,
        arrows=[dict(tail=[163.67, 88.0, 140.85], head=[163.67, 88.0, 92.0], normal=[0, -1, 0])])
# B1 comes up from below: two lines from the ends of its horn-shaped cut-out to the horn, two at the plates' corners.
g.place('Place B2 onto B1 so the servo horn fits into the cut-out in B1.', move=[B1], direction=[0, -1, 0],
        labels={B1: 'B1', BASE_HORN: 'Base Motor'}, flip=True, frame=([150.0, 84.0, 141.0], 112.0),   # (the same side, a little wider: B1 is large)
        lines_at=[[146.2, 88.6, 140.9], [181.2, 88.6, 140.9], [-26.0, 90.5, 94.5], [214.3, 90.5, 187.1]],
        caution='If the servo horn is not lined up, you may need to adjust it so that it fits in the B1 slot.')
# Screws thread into the wood, so the CAD cannot give their direction: set by hand. One is shown close up, then the rest.
g.place('Screw B2 onto B1 with six 6mm screws.', move=BASE_SCREWS[:1], direction=[0, 1, 0], hover=35, axial=True,
        focus=BASE_SCREWS[:1], focus_pad=1.5, labels={BASE_SCREWS[0]: '6mm Hex Screw'})
g.place('Add the other five 6mm screws.', move=BASE_SCREWS[1:], direction=[0, 1, 0], hover=g.cfg['hover_fastener'], axial='each')

# --- controller
g.place('Insert B3 into B2.', move=[B3])
g.place('Insert B4 into B2.', move=[B4])
# Each joystick is built in hand between two walls, then the group goes onto B3. It arrives wired to the I/O module
# (left joystick: GND - A2 G, 5V - A2 V, X - A2 S, Y - A3 S; right joystick: the same on A0 and A1), so while it is
# in hand its wires are shown cut short, and whole again once the group is on the base beside the module.
JOYSTICK_CAUTION = ("The joystick's breadboard wires stay connected to the I/O module: just place the joystick for now. "
                    "The {side} joystick is the one wired to {pins}.")
g.place('Place the left joystick (the joystick connected to A3) into B5...', move=[JOY_LEFT], show=[B5], against=[B5], staged=True,
        labels={JOY_LEFT: 'Left Joystick', B5: 'B5'}, wires=jumper_routes(JOY_LEFT, fade=(30, 62)),
        caution=JOYSTICK_CAUTION.format(side='left', pins='A2 G, A2 V, A2 S and A3 S'))
g.place('...and B6.', move=[B6_LEFT], against=[B5, JOY_LEFT], staged=True)
g.seat('Then place B5 and B6 onto B3.', [B5, B6_LEFT, JOY_LEFT], appear=[MODULE], wires=jumper_routes(JOY_LEFT),
       lines_at=[[-15.6, 90.5, 107.1], [21.1, 90.5, 131.0], [-20.3, 87.1, 131.3], [21.0, 90.5, 107.1], [79.9, 90.5, 107.8], [100.2, 87.1, 130.0]])   # Lee's points on the tabs of B5 and B6 (six, as Lee asked)
g.place('Place the right joystick into B6...', move=[JOY_RIGHT], show=[B6_RIGHT], against=[B6_RIGHT], staged=True,
        labels={JOY_RIGHT: 'Right Joystick', B6_RIGHT: 'B6'}, wires=jumper_routes(JOY_RIGHT, fade=(30, 62)),
        caution=JOYSTICK_CAUTION.format(side='right', pins='A0 G, A0 V, A0 S and A1 S'))
g.place('...and B7.', move=[B7], against=[B6_RIGHT, JOY_RIGHT], staged=True)
# The left joystick's wires run from it to the I/O module lying beside the base, across where B6 comes down (Lee, 14 Oct
# 2026): they are held up in an arch over it while the group goes on, then laid back down over it.
def held_up(joystick, lift=70.0):
    """The joystick's wires lifted in an arch, highest about half-way along (the ends stay on their pins)."""
    out = {}
    for wire_id, line, _, _ in jumpers[joystick]:
        line = np.asarray(line, float)
        s = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))])
        u = np.clip((s / s[-1] - 0.12) / 0.8, 0.0, 1.0)
        out[wire_id] = W.route(line + (lift * np.sin(np.pi * u))[:, None] * np.array([0.0, 1.0, 0.0]), a=joystick, b=MODULE)
    return out


g.seat("Hold the left joystick's wires up out of the way, then place B6 and B7 onto B3.", [B6_RIGHT, B7, JOY_RIGHT], appear=RIGHT_MODULE_CAPS,
       wires={**jumper_routes(JOY_RIGHT), **held_up(JOY_LEFT)}, wires_done=jumper_routes(JOY_LEFT),
       lines_at=[[21.3, 90.5, 151.0], [-15.3, 90.5, 175.0], [-23.5, 87.1, 152.0], [20.4, 90.5, 176.2], [101.0, 87.1, 151.3]])   # Lee's points on the tabs of B6 and B7
# One line per slot in B8 (Lee, 14 Oct 2026): from the middle of the slot on B8's underside straight down to the top of the tab it
# takes. B5, both B6 and B7 have two tabs each (x -20.8 and 26.2); the tabs of B5 and B7 end at y 140.2, those of the B6 at 143.2.
B8_UNDERSIDE = 134.23
B8_SLOTS = [(x, z, top) for z, top in ((106.55, 140.23), (130.13, 143.23), (151.55, 143.23), (175.13, 140.23)) for x in (-20.84, 26.16)]
STEP_38_CAMERA = dict(view_dir=[-0.5792, 0.5736, -0.5792], frame=([94.2, 158.2, 184.2], 167.6))   # the right group's own camera, kept for B8 (Lee; the I/O module's step has its own since 14 Oct 2026)
g.place('Attach B8 on top of B5 - B7.', move=[B8], lines_at=[[[x, B8_UNDERSIDE, z], [x, top, z]] for x, z, top in B8_SLOTS], **STEP_38_CAMERA)

# --- electronics
# Lee (14 Oct 2026): the board goes in angled very slightly, over the end lip of B4 and into the slots of the two B6, and levels
# out at the end. The lip stands 3.1 mm above the board's underside (y 107.89 against 104.78, at z 174 - 179.8), so the board
# comes in lifted 3.4 mm clear of it (Lee, later the same day: it went through the lip), then, as its leading edge reaches the
# slots in the B6, is tipped about that edge so that its far end stays over the lip, and levels out once past it. (The CAD's
# slots fit the board exactly, so the tipped board grazes their tops by a millimetre or two; and the CAD has B7 in the way
# of it; both ignored, as Lee said.)
LEADING_EDGE = [70.0, 104.8, 116.0]
board_tilt = lambda t, degrees=3.0: turned([1, 0, 0], -degrees, LEADING_EDGE, t)
g.place('Slide the I/O module through the slots in B6 on top of B4, angled very slightly over the end of B4, until it lies flat.', move=[MODULE],
        labels={MODULE: 'Nano I/O Module'}, path=[board_tilt([0, 3.4, 70]), via(board_tilt([0, 3.4, 40])), via(board_tilt([0, 0.4, 36], 7.6)),
                                                  via(board_tilt([0, 0, 20], 4.6)), board_tilt([0, 0, 0.6], 3.3), [0, 0, 0]],
        view_dir=[-0.7071, 0.2457, 0.6631], frame=([62.5, 129.6, 161.0], 80.9),   # (the camera of Lee's screenshot of Step 40, 14 Oct 2026, solved by matching it)
        lines_at=[[95.9, 105.6, 131.5], [95.8, 105.6, 153.0], [44.1, 105.6, 131.6], [44.1, 105.6, 152.9]])   # the board's corners, at the slots in the two B6
ROW5 = ROW5_TOP                                                     # (the top of the middle pin of row 5)
BROWN_TO_G = 'Very important: the brown wire goes on G, the pin nearest the edge of the board.'   # (Lee, 14 Oct 2026)
# The plug is lifted clear of the joystick wires, brought upright over row 5 and pushed straight down onto the pins.
g.place('Reconnect the base motor to Row 5. Remember brown to G, red to V, and orange to S.', move=[BASE_PLUG],   # ("Row": Lee, 15 Oct 2026)
        path=[BASE_PLUG_SLOT, via([35, 62, 0]), [0, 45, 0], [0, 0, 0]],
        labels=[dict(text='Row 5', anchor=ROW5, id=MODULE, ring=False), dict(text='Base Motor', id=BASE_PLUG)], lines=False,
        view_dir=[-0.527, 0.7929, -0.306], frame=([84.2, 131.5, 137.4], 69.0),   # (the camera of Lee's screenshot of Step 41c, 14 Oct 2026, solved within 6 px)
        wires_done=routes(BASE_LEAD, base_plugged, a=BASE_MOTOR, b=BASE_PLUG, b_from=IN_SLOT),
        caution=BROWN_TO_G)

# ================================================================ ARM (begin)
# Order and handling follow the build video Arm.mov (docs/research/mra/video_arm*.md); the geometry was checked against the
# CAD (docs/research/mra/cad_arm_claw.md). Three groups are built in the hand and then fitted: the upper arm (A6 - A9), the
# lever (A1 - A3) and the triangle (A10 - A12); A4 + A5 are joined in the hand too.
SCREW = dict(hover=g.cfg['hover_fastener'], axial=True)              # a screw goes in along its own axis: one line down the middle
CLOSE = dict(focus_pad=2.0)                                          # (with focus=[the screw]) a single screw on the model, shown close up
OUT_LEFT, OUT_RIGHT = [0, 0, -1], [0, 0, 1]                          # out of the arm on the R5 side / on the R6 side


def horn_leading(hub, horn, inwards, way):
    """The way in for a motor that has its horn fitted: the horn is fed through the opening ahead of the motor.
    hub: the middle of the horn's hub. horn: the way the horn points. inwards: the way the shaft points.
    way: (degrees the motor is tilted so the horn's end leads, mm moved along the horn, mm short of home), hover first."""
    horn, inwards = np.array(horn, float), np.array(inwards, float)
    axis = np.cross(horn, inwards)
    return [turned(axis, tilt, hub, horn * along - inwards * short) if tilt else (horn * along - inwards * short).tolist() for tilt, along, short in way]


# --- upper arm: A6 with A7 and A8 on its tabs, each held by a 16mm screw into an A9 (a T-shaped wooden nut)
g.in_hand = [i for i in g.in_hand if i not in JUMPER_CAPS]         # (seat() leaves the joysticks' wire caps "in hand", so they would show in every sub-assembly view from here on)
A6_FACE = [-0.742, 0.670, 0.0]                                      # the way the engraved face of A6 looks
upper_arm = [A6, A7, A9_NEAR_A7, A7_SCREW, A8, A9_NEAR_A8, A8_SCREW]
g.place('Press A7 onto the two tabs of A6 nearest the A6 code. The code on A7 faces out, with its A at the same end as the A6 code.',
        move=[A7], show=[A6], against=[A6], staged=True)
# (The line follows the tip of the A9's stem right through A6. With the automatic line, which stops at the face of A6, the camera
# chosen for this step looks along that face and the slot cannot be seen.)
g.place('Push an A9 into the cross-shaped slot next to A7, from the engraved side of A6.', move=[A9_NEAR_A7], against=[A6, A7], direction=A6_FACE, staged=True,
        lines_at=[[203.5, 187.5, 138.0]])
g.place('Screw A7 to the A9 with a 16mm screw through the middle hole of A7.', move=[A7_SCREW], against=upper_arm[:3], direction=OUT_LEFT, staged=True, **SCREW)
g.place('Press A8 onto the other two tabs of A6, code facing out and its horn-shaped slot at the end away from the A6 code.',
        move=[A8], against=upper_arm[:4], staged=True)
g.place('Push the other A9 into the cross-shaped slot next to A8.', move=[A9_NEAR_A8], against=upper_arm[:5], direction=A6_FACE, staged=True,
        lines_at=[[211.5, 196.4, 151.0]])
g.place('Screw A8 to that A9 with a 16mm screw.', move=[A8_SCREW], against=upper_arm[:6], direction=OUT_RIGHT, staged=True, **SCREW)
g.seat('Lower A6 - A9 over R2: A7 goes against the R5 side of R2, A8 beside R6.', upper_arm)
# The shoulder pivot. The driver reaches it through the empty motor opening in R5, so it goes in before the elbow motor.
# (The line is set by hand to end in that opening, just under its top edge. The automatic line, to the hole in A7, can be seen
# as well from the R6 side as from the R5 side, and the camera then stays on the R6 side, where the opening does not show.)
# (Seen through the opening in R5, a little off the screw's axis, so that the screw is seen going into the hole in A7: Lee, 14 Oct 2026.)
g.place('Screw A7 to R2 with a 6mm screw. Reach it through the opening in R5. A7 must still swing.', move=[PIVOT_SCREW], direction=OUT_LEFT, focus=[PIVOT_SCREW], **SCREW, **CLOSE,
        view_dir=[-0.42, 0.34, -0.84])

# --- lever: A1, A2 and A3 stacked, one 10mm screw through the middle hole
lever = [A1, A2, A3, LEVER_SCREW]
g.place('Lay A2 on A1, codes facing the same way and notches together.', move=[A2], show=[A1], against=[A1], direction=OUT_LEFT, staged=True,
        lines_at=[[144.5, 175.4, 124.5], [177.8, 160.5, 123.8]])       # Lee's points: the end of the slot and the middle hole
g.place('Lay A3 on A2 the same way.', move=[A3], against=lever[:2], direction=OUT_LEFT, staged=True, lines_at=[[144.8, 175.4, 120.5], [177.8, 160.3, 123.5]])
g.place('Screw A1 - A3 together with a 10mm screw through the middle hole of A3.', move=[LEVER_SCREW], against=lever[:3], direction=OUT_LEFT, staged=True, **SCREW)
# With the turret built, the lever only goes over the head of the pivot screw while it stands 40 to 90 degrees up from where it
# ends up (the head of its own screw then clears the top of R5): upright, down between R5 and A7, across onto the head, swung down.
SHOULDER = [175.33, 161.90, 122.05]                                 # the shoulder axis, in the middle of the lever
upright = lambda t: turned([0, 0, 1], -66, SHOULDER, t)
g.seat('Slide A1 - A3 down between R5 and A7, slotted end first and A3 facing R5, onto the screw head in A7. Swing it towards the controller.', lever, focus=lever + [R5], focus_pad=1.0,
       view_dir=[-0.6029, 0.675, -0.4254], frame=([156.8, 190.1, 139.8], 77.6),   # (the camera of Lee's screenshot of Step 53, 14 Oct 2026, solved by matching it)
       path=[upright([0, 60, -3.2]), upright([0, 0, -3.2]), upright([0, 0, 0]), [0, 0, 0]], lines_at=[[175.3, 161.9, 123.6]])

# --- elbow motor: horn first through R5 into the lever, then clamp plate R8 over its lead
# The horn (18 mm long) reaches 10 mm past the end of the opening in R5. Poses found by a collision search against the CAD
# (worst overlap 0.5 mm): tilted 20 degrees and drawn back along the horn, the horn goes through; the motor is levelled as it
# follows, and pushed home so the horn drops into the slot in A3 and A2.
ELBOW_HUB, ELBOW_HORN_ALONG = [175.66, 162.28, 120.6], [0.911, -0.412, 0.0]
elbow_way = horn_leading(ELBOW_HUB, ELBOW_HORN_ALONG, [0, 0, 1], [(20, -10, 60), (20, -10, 15), (20, -8, 13), (0, -1, 6), (0, 0, 0)])
elbow_way[2] = via(elbow_way[2])
elbow_tip = np.array(ELBOW_HUB) + 18.0 * np.array(ELBOW_HORN_ALONG)    # the lead line runs from the horn's tip to where the tip passes through R5
g.place('The elbow motor has 6 on its wire. Angle its servo horn through the opening in R5, then push the motor in so the horn sits in the slot in A2 and A3.', move=[ELBOW_MOTOR, ELBOW_HORN], path=elbow_way,
        lines_at=[[elbow_tip, [182.0, 159.4, 110.6]]], wires=ELBOW_LEAD['loose'], focus=[ELBOW_MOTOR, R5], focus_pad=1.1, labels={ELBOW_MOTOR: dotted('Elbow Motor')})
g.place("Pass the elbow motor's plug through R8 and slide R8 down the wire onto the back of the motor, code facing out.", move=[R8],
        direction=OUT_LEFT, hover=45, focus=[R8, ELBOW_MOTOR, R5], focus_pad=1.1,
        lines_at=[[[170.28, 171.6, 106.46], [170.28, 171.6, 109.0]], [[170.28, 152.95, 106.46], [170.28, 152.95, 109.0]]])     # hole to hole
g.place('Screw R8 onto R5 with two 10mm screws.', move=R8_SCREWS[:1], direction=OUT_LEFT, focus=R8_SCREWS[:1], **SCREW, **CLOSE)
# (Seen from low down, looking up, so that the lower screw is seen going into its hole as the upper one was from above; then the
# hook-shaped slot from higher up: Lee's screenshots of Steps 57 and 58, 14 Oct 2026, solved by matching them. The shoulder
# side's two steps have the same cameras, mirrored onto the R6 side. They are one-offs: the steps after them keep the cameras
# they had, as Lee asked.)
SECOND_SCREW_CAMERA = dict(view_dir=[0.7713, -0.1611, -0.6158], frame=([170.2, 151.5, 77.2], 73.6), one_off_camera=True)
HOOK_SLOT_CAMERA = dict(view_dir=[-0.6151, 0.5602, -0.5548], frame=([147.9, 134.0, 119.4], 75.7), one_off_camera=True)
mirrored = lambda cam: dict(view_dir=[cam['view_dir'][0], cam['view_dir'][1], -cam['view_dir'][2]],
                            frame=([cam['frame'][0][0], cam['frame'][0][1], round(2 * 140.6 - cam['frame'][0][2], 1)], cam['frame'][1]), one_off_camera=True)
g.place('Add the second 10mm screw.', move=R8_SCREWS[1:], direction=OUT_LEFT, focus=R8_SCREWS[1:], **SCREW, **CLOSE, **SECOND_SCREW_CAMERA)
g.place("Move the elbow motor's wire into the hook-shaped slot in R5.", eye=[dict(anchor=[119.6, 167.4, 110.5], id=R5)], focus=[R5, R8], focus_pad=1.3, **HOOK_SLOT_CAMERA,
        wires_done=ELBOW_LEAD['hooked'], ride={ELBOW_PLUG: ELBOW_LEAD['plug_hooked']})

# --- A4 and A5: joined in the hand, A4 against the inside of the lever's free end, A5 screwed to the end of A7
g.place('Lay the coded end of A5 over the plain end of A4.', move=[A5], show=[A4], against=[A4], direction=OUT_LEFT, staged=True)
g.place('Screw A5 to A4 with a 6mm screw.', move=[A5_A4_SCREW], against=[A4, A5], direction=OUT_LEFT, staged=True, **SCREW)
g.seat('Swing A1 - A3 up until its free end stands clear above R5, and hold the coded end of A4 against the inner face of A1 there.', [A4, A5, A5_A4_SCREW],
       focus=[A4, A5, A7] + lever, focus_pad=1.0)
g.place('With A1 - A3 still swung up clear of R5, screw A1 - A3 to A4 with a 10mm screw through the large hole in A3.', move=[LEVER_A4_SCREW], direction=OUT_LEFT,
        focus=[LEVER_A4_SCREW], **SCREW, **CLOSE)                     # (shown with A1 - A3 down, where they end up: Lee, 14 Oct 2026, fine as it is)
g.place('Swing A5 up against the outside of A7 and screw them together with a 6mm screw through the second hole of A5.', move=[A5_A7_SCREW], direction=OUT_LEFT,
        focus=[A5_A7_SCREW], **SCREW, **CLOSE)

# --- shoulder motor: horn first through R6 into A8, then clamp plate R7 over its lead
# As the elbow motor: tilted 20 to 25 degrees with the horn leading (collision search against the CAD, worst overlap 0.5 mm).
SHOULDER_HUB, SHOULDER_HORN_ALONG = [175.66, 162.28, 160.6], [0.670, 0.742, 0.0]
shoulder_way = horn_leading(SHOULDER_HUB, SHOULDER_HORN_ALONG, [0, 0, -1], [(20, -9, 60), (20, -9, 21), (25, -9, 16), (25, -5, 13), (0, 0, 6), (0, 0, 0)])
shoulder_way[2], shoulder_way[3] = via(shoulder_way[2]), via(shoulder_way[3])
shoulder_tip = np.array(SHOULDER_HUB) + 18.0 * np.array(SHOULDER_HORN_ALONG)    # (to where it passes through R6: a line ending there is hidden from the R5 side, so the camera comes round to R6)
g.place('The shoulder motor has 9 on its wire. Hold the arm up, angle the servo horn through the opening in R6 and push the motor in so the horn sits in the slot in A8.', move=[SHOULDER_MOTOR, SHOULDER_HORN], path=shoulder_way,
        lines_at=[[shoulder_tip, [180.7, 167.8, 170.7]]], wires=SHOULDER_LEAD['loose'], focus=[SHOULDER_MOTOR, R6], focus_pad=1.1, labels={SHOULDER_MOTOR: dotted('Shoulder Motor')})   # (9: confirmed by Lee)
g.place("Pass the shoulder motor's plug through R7 and slide R7 down the wire onto the back of the motor, code facing out.", move=[R7],
        direction=OUT_RIGHT, hover=45, focus=[R7, SHOULDER_MOTOR, R6], focus_pad=1.1,
        lines_at=[[[170.28, 171.6, 174.74], [170.28, 171.6, 172.2]], [[170.28, 152.95, 174.74], [170.28, 152.95, 172.2]]])
g.place('Screw R7 onto R6 with two 10mm screws.', move=R7_SCREWS[:1], direction=OUT_RIGHT, focus=R7_SCREWS[:1], **SCREW, **CLOSE)
g.place('Add the second 10mm screw.', move=R7_SCREWS[1:], direction=OUT_RIGHT, focus=R7_SCREWS[1:], **SCREW, **CLOSE, **mirrored(SECOND_SCREW_CAMERA))
g.place("Move the shoulder motor's wire into the hook-shaped slot in R6.", eye=[dict(anchor=[119.6, 167.4, 170.7], id=R6)], focus=[R6, R7], focus_pad=1.3, **mirrored(HOOK_SLOT_CAMERA),
        wires_done=SHOULDER_LEAD['hooked'], ride={SHOULDER_PLUG: SHOULDER_LEAD['plug_hooked']})

# --- triangle: A11 and A12 screwed to A10 in the hand, then hung inside R6 and screwed to the end of A8 under A13
triangle = [A10, A11, A11_SCREW, A12, A12_SCREW]
g.place('Lay the coded end of A11 on the sharp corner of A10.', move=[A11], show=[A10], against=[A10], direction=OUT_RIGHT, staged=True)
g.place('Screw A11 to A10 with a 6mm screw.', move=[A11_SCREW], against=triangle[:2], direction=OUT_RIGHT, staged=True, **SCREW)
g.place('Lay A12 on A10 with the two triangle marks together.', move=[A12], against=triangle[:3], direction=OUT_RIGHT, staged=True)
g.place('Screw A12 to A10 with a 6mm screw.', move=[A12_SCREW], against=triangle[:4], direction=OUT_RIGHT, staged=True, **SCREW)
g.seat('Lower the plain end of A11 inside R6, behind the lobe on its top edge. A10 goes against the outside of A8.', triangle,
       focus=triangle + [R6, A8], focus_pad=1.0, lines_at=[[139.4, 179.8, 167.7], [228.9, 221.3, 164.7]])
g.place('Screw R6 to A11 with a 6mm screw, through the hole in the lobe from outside R6.', move=[R6_A11_SCREW], direction=OUT_RIGHT,
        focus=[R6_A11_SCREW], **SCREW, **CLOSE)
g.place('Lay the square-marked end of A13 on A10, over the hole at the end of A8.', move=[A13], direction=OUT_RIGHT, hover=g.cfg['hover_face_on'],
        focus=[A13, A10, A12, A8], focus_pad=1.0)
g.place('Screw A13 and A10 to A8 with a 10mm screw.', move=[A13_SCREW], direction=OUT_RIGHT, focus=[A13_SCREW], **SCREW, **CLOSE)
# (The builder checks by hand at 7:07, 10:08 and 10:48 on the video.) Lee, 14 Oct 2026: Step 76c's view, with A13 and A12, whose
# far ends are still free until the claw goes on, jiggling a little about their screws as the step opens (A11 stays put: Lee
# corrected the parts the same day). One view, one advance: no Step 76c. An eye on A12: what to check.
def jiggle(at, degrees):
    """A path that rocks a part about the screw at `at` (its axis along z) and back: twice, pausing half-way."""
    rock = lambda k: via(turned([0, 0, 1], degrees * k, at))
    return [[0, 0, 0], rock(1), rock(-1), [0.0, 0.0, 0.0], rock(1), rock(-0.6), [0, 0, 0]]


STEP_76C_CAMERA = dict(view_dir=[0.5792, 0.5736, 0.5792], frame=([243.2, 200.0, 196.8], 93.8))   # (Step 76c's own camera, as Lee asked)
pivot = lambda screw: g.model.inst[screw].bounds.mean(0).round(2)   # (the screw's axis runs along z through the middle of it)
g.place('Check that the arm and all its links swing freely.', move=[A13, A12], lines=False, wiggle=True, single=True, **STEP_76C_CAMERA, eye=[A12],
        paths={A13: jiggle(pivot(A13_SCREW), 6.0), A12: jiggle(pivot(A12_SCREW), 6.0)})
# ================================================================ ARM (end)

# ================================================================ CLAW AND FINAL WIRING (begin)
# Order and handling follow the build video Claw.mov (docs/research/mra/video_claw.md); the geometry was checked against the
# CAD (docs/research/mra/cad_arm_claw.md, cad_wire_paths.md). The claw is built in the hand and then fitted to the arm.
# On the video it is built upside down (engraved faces up) and turned over to go on the arm; so it is here (Lee, 14 Oct 2026):
# every step of the claw in the hand is seen with it turned over (flip=True), so that the parts the CAD has arriving from
# underneath are seen going on from above. The captions say which face goes where by the engraved codes.
FROM_BELOW, CLAW_NORMAL = [0, -1, 0], [0.011, 1, 0]                 # (the claw's plates are tilted 0.6 degrees in the CAD)
UPSIDE_DOWN = dict(staged=True, flip=True)                           # a claw step in the hand: seen turned over
claw = [C3, CLAW_MOTOR, CLAW_HORN, C1, C2, C4, C5, C6, *C6_SCREWS, C7, C9, C8, C8_SCREW]
GEAR_MESH = [334.8, 177.9, 147.2]                                    # where the teeth of C7 and C8 meet: half-way between the horn's axis and C8's pivot, in the gears' mid-plane

# --- claw: the motor through C3, the two clips, the two bars, C6 screwed on, then the jaws and the cover
# The motor arrives with its horn fitted (video 0:00). Nothing screws it down: its tabs are trapped between C3 and the bars.
g.place('Begin the claw with C3. Push the claw motor through C3 from the engraved side, wire first, with the wire at the notched end of the cut-out.',
        move=[CLAW_MOTOR, CLAW_HORN], show=[C3], against=claw[:1], hover=55, **UPSIDE_DOWN, wires=CLAW['up'][0], labels={C3: 'C3', CLAW_MOTOR: dotted('Claw Motor')},
        lines_at=[[[329.14, 196.6, 132.86], [329.14, 193.0, 132.86]], [[341.29, 196.6, 155.41], [341.29, 193.0, 155.41]]])   # case corners to cut-out corners
g.place("Feed the claw motor's wire back through the hole in the end of C3.", **UPSIDE_DOWN, eye=[dict(anchor=[300.8, 196.5, 147.1], id=C3)],
        **by_way_of(43, 50, 57, 66, 76, CLAW['in_c3']))     # (the plug follows the lead through the hole, 55 - 59 mm along)
# (C1 and C2 go in along the claw's own normal: straight down, the test finds the 0.6 degree tilt in the way.)
g.place('Insert C1 into the outer of the two slots on one side of C3, from the plain side, code facing out.', move=[C1], against=claw[:3],
        direction=CLAW_NORMAL, **UPSIDE_DOWN)
g.place('Insert C2 into the outer half of the square slot on the other side, code facing out.', move=[C2], against=claw[:4],
        direction=CLAW_NORMAL, **UPSIDE_DOWN)
g.place('Insert C4 into the same square slot from the engraved side of C3, next to C2, code facing C2.', move=[C4], against=claw[:5], **UPSIDE_DOWN)
g.place('Insert C5 into the slot next to C1, code facing C1.', move=[C5], against=claw[:6], **UPSIDE_DOWN)
g.place('Press C6 onto C4 and C5, code facing away from C3. The servo horn sits in its round cut-out.', move=[C6], against=claw[:7], **UPSIDE_DOWN)
g.place('Screw C6 onto C3 with two 16mm screws.', move=C6_SCREWS[:1], against=claw[:8], direction=FROM_BELOW, **UPSIDE_DOWN, **SCREW,
        lines_at=[[[322.95, 195.85, 147.08], [322.95, 179.53, 147.08]]])
g.place('Add the second 16mm screw.', move=C6_SCREWS[1:], against=claw[:9], direction=FROM_BELOW, **UPSIDE_DOWN, **SCREW,
        lines_at=[[[347.25, 195.59, 147.06], [347.25, 179.53, 147.06]]])
# (The CAD has the horn 0.35 mm into the sides of C7's slot, a push fit, so the horn is left out of the motion test.)
g.place('Press C7 over the servo horn, code facing away from C6.', move=[C7], against=[i for i in claw[:10] if i != CLAW_HORN], lines_to=[CLAW_HORN], **UPSIDE_DOWN,
        caution='If the servo horn is not lined up, you may need to adjust it so that it fits in the C7 slot.')
# The cover goes on before the second jaw, as on the video (2:29 - 2:53): C8 is then slid in under it.
g.place('Press C9 onto the ends of C1 and C2 until they click through, code facing out.', move=[C9], against=claw[:11], **UPSIDE_DOWN)
# Step 88c: a close-up of the two gears as if C9 were not there, with a lead line to where they mesh (Lee, 14 Oct 2026), seen
# square-on to the gears from the C9 side.
g.place('Slide C8 in between C6 and C9, code facing C9, with both jaws closed, until its teeth mesh with C7.', move=[C8], against=claw[:12], **UPSIDE_DOWN,
        inset=dict(target=GEAR_MESH, dir=[0.0, -1.0, 0.0], radius=21.0, hide=[C9], mark=4.5, caption='Seen without C9',
                   alt='Close-up of the claw with C9 left out: the teeth of C7 and C8 mesh together.'))
g.place('Screw C8 in place with a 10mm screw through C9.', move=[C8_SCREW], against=claw[:13], direction=FROM_BELOW, **UPSIDE_DOWN, **SCREW)

# --- claw onto the arm: slid back between the forearm strips, then one 6mm screw through each strip
g.seat('Slide the claw in between A5 and A12 / A13, with the motor on top and C1 against A12 and A13.', claw,
       focus=[C1, C2, C3, CLAW_MOTOR, A5, A12, A13], focus_pad=0.9,   # (sliding it in: Lee, 14 Oct 2026)
       lines_at=[[[298.2, 206.1, 166.2], [316.8, 206.1, 166.2]], [[298.1, 189.2, 126.6], [305.8, 189.2, 126.6]],
                 [[300.7, 187.6, 166.2], [306.0, 187.6, 169.2]]])     # the two the generator found, and Lee's from C1 to A13
g.in_hand = [i for i in g.in_hand if i != CLAW_PLUG]                # (seat() leaves the lead's plug "in hand": see the note in the arm section)
g.place('Screw A12 to C1 with a 6mm screw.', move=[A12_C1_SCREW], direction=OUT_RIGHT, focus=[A12_C1_SCREW], **SCREW, **CLOSE)
g.place('Screw A13 to C1 with a 6mm screw.', move=[A13_C1_SCREW], direction=OUT_RIGHT, focus=[A13_C1_SCREW], **SCREW, **CLOSE)
g.place('Screw A5 to C2 with a 6mm screw.', move=[A5_C2_SCREW], direction=OUT_LEFT, focus=[A5_C2_SCREW], **SCREW, **CLOSE)

# --- the claw motor's wire: through A6 twice, joined to the servo extension wire above R4, then down behind R4
# (Both seen nearly square to the engraved face of A6, between the arm's side strips, so that the whole run of the lead shows: Lee, 14 Oct 2026.)
ALONG_A6 = [-0.7, 0.62, -0.35]
g.place("Feed the claw motor's wire through the top hole in A6, from the plain side.", eye=[dict(anchor=[221.6, 215.4, 144.5], id=A6)],
        frame=([224.2, 207.6, 155.7], 63.3), view_dir=[-0.6864, 0.6928, -0.2208],   # (the camera of Lee's screenshot of Step 96, solved within 11 px)
        **by_way_of(129, 136, 143, 152, 162, CLAW['in_a6']))     # (the hole is 142 - 146 mm along)
g.place('Then feed it back through the bottom hole in A6 and bring the plug forward over R4.', eye=[dict(anchor=[185.6, 175.5, 144.5], id=A6)],
        frame=([165.0, 180.0, 145.0], 62.0), view_dir=ALONG_A6,      # (through the hole, 203 - 207 mm along, then hanging behind A6)
        **by_way_of(190, 197, 204, 216, CLAW['above_r4']))
# (The coupler arrives on the extension: on the video nobody fits it. The extension is the piece in the hand, so it moves.)
g.place("Push the coupler of the servo extension wire onto the claw motor's plug, brown wire to brown wire.",
        appear=[COUPLER, EXTENSION_PLUG, ROW10_PLUG], frame=([60.0, 160.0, 146.0], 80.0), wires=EXTENSION_LEAD['loose'],   # (wide enough for the loose end)
        caution='Check that the wire colours match across the join: brown to brown, red to red and orange to orange.',   # (instead of the eye: Lee, 14 Oct 2026)
        view_dir=[-0.45, 0.85, -0.3],                                 # (from high up, above the joysticks' wires: Lee, 14 Oct 2026)
        ride={COUPLER: ABOVE_R4.tolist(), EXTENSION_PLUG: ABOVE_R4.tolist(), ROW10_PLUG: ROW10_PLUG_LOOSE})
behind_r4 = [[0.0, float(ABOVE_R4[1]), 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 0.0]]   # back over the top edge of R4, then down (the extension down the slot's stem to its foot, then into the pocket)
g.place('Push the join down behind R4 and move the servo extension wire into the L-shaped slot in R4.',
        eye=[dict(anchor=[133.4, 146.6, 141.7], id=R4)], frame=([128.0, 142.0, 143.0], 55.0),
        wires_done={**CLAW['home'][0], **{w: [EXTENSION_LEAD['over_r4'][w], EXTENSION_LEAD['in_stem'][w], EXTENSION_LEAD['rest'][w]] for w in EXTENSION}},
        ride={CLAW_PLUG: behind_r4, COUPLER: behind_r4, EXTENSION_PLUG: behind_r4, ROW10_PLUG: [T_HELD_HIGH, T_HELD_LOW, T_REST]})

# --- final wiring: one plug per step, in the order of the rows. Each plug is brought over its row and pushed straight down.
ROW6, ROW9, ROW10 = ROW6_TOP, ROW9_TOP, ROW10_TOP                    # the tops of the middle pins of the rows (cad_pins.json)
row_label = lambda row, at, plug, name: [dict(text=f'Row {row}', anchor=at, id=MODULE, ring=False), dict(text=dotted(name), id=plug)]
PLUG_IN = dict(lines=False, view_dir=[-0.3614, 0.8788, 0.3116], frame=([85.9, 131.8, 144.2], 64.3))   # one camera for the wiring run: Lee's screenshot of Step 102c (solved within 9 px)
g.place('Reconnect the elbow motor to Row 6. Remember brown to G, red to V, and orange to S.', move=[ELBOW_PLUG],
        path=[ELBOW_LEAD['plug_hooked'], via(ELBOW_ALONG[150.0]), T_ELBOW_OFF, via(ELBOW_ALONG[190.0]), via(ELBOW_ALONG[205.0]), T_ELBOW_UP, [0.0, 0.0, 0.0]],   # (up, over the base motor's lead, then down beside it)
        labels=row_label(6, ROW6, ELBOW_PLUG, 'Elbow Motor'), wires_done={w: [ELBOW_OFF[w], ELBOW_UP[w], ELBOW_LEAD['plugged'][w]] for w in ELBOW_LEAD['wires']}, **PLUG_IN)
g.place('Reconnect the shoulder motor to Row 9. Remember brown to G, red to V, and orange to S.', move=[SHOULDER_PLUG],
        path=[SHOULDER_LEAD['plug_hooked'], T_SHOULDER_OFF, turned_as(T_SHOULDER_UP, [20.0, 52.0, 0.0]), turned_as(T_SHOULDER_UP, [0.0, 52.0, 0.0]), T_SHOULDER_UP, [0.0, 0.0, 0.0]],   # (upright over the joysticks' wires, then over the row)
        labels=row_label(9, ROW9, SHOULDER_PLUG, 'Shoulder Motor'), wires_done={w: [SHOULDER_OFF[w], SHOULDER_UP[w], SHOULDER_LEAD['plugged'][w]] for w in SHOULDER_LEAD['wires']}, **PLUG_IN)
g.place('Connect the servo extension wire to Row 10. Remember brown to G, red to V, and orange to S.', move=[ROW10_PLUG],
        # from its rest: straight up, still flat, under the shoulder motor's lead; across in front of R6's ear and turning upright,
        # under that lead where it runs down to row 9; then up beside it, over row 10 and down (clear of the jumper wires: Lee)
        path=[T_REST, via(lifted(T_REST, 35.0)), via([50.0, 21.0, 10.0]), T_RISEN, via(T_ACROSS), T_OVER, [0.0, 0.0, 0.0]],
        labels=row_label(10, ROW10, ROW10_PLUG, 'Claw Motor'), **PLUG_IN,
        wires_done={w: [EXTENSION_LEAD['risen'][w], EXTENSION_LEAD['over_row'][w], EXTENSION_LEAD['plugged'][w]] for w in EXTENSION})
# ================================================================ CLAW AND FINAL WIRING (end)

g.rest_at([USB_A], A_ON_THE_TABLE)
g.place('Connect the power cable to the Nano Board.', move=[USB_B], appear=[USB_A], direction=[0, 0, 1], hover=30, lines_at=USB_IN,
        labels={USB_B: 'USB Cable'}, wires=usb_cable(plug=30, a_pose=A_ON_THE_TABLE), wires_done=usb_cable(a_pose=A_ON_THE_TABLE),
        view_dir=[0.5792, 0.5736, 0.5792], frame=([70.0, 106.2, 222.8], 128.5))   # (the USB cable is the power cable: Lee) (the step's camera as it was, kept)

# ================================================================ T1 / T2 BLOCK (begin)
# The four-piece block that stands beside the base (docs/research/mra/cad_codes_base.md, section 2), built last, in the hand
# (Lee, 14 Oct 2026): the solid end of one T2 into an arm of the plus-shaped slot in the lower T1, the other T2 down over it,
# slot into slot, until it latches into the T1 too, then the upper T1 onto the two.
T_BLOCK = [T1_LOWER, T2_SOLID_DOWN, T2_SLOT_DOWN, T1_UPPER]
T_CAMERA = dict(look_from=[1, 1, 1], frame=([195.2, 143.0, 58.5], 63.0))   # one camera for all three, from the side the first T2's code faces (Lee)
g.place('Build the T1 / T2 block. Push the solid end of a T2 into one arm of the plus-shaped slot in a T1.', move=[T2_SOLID_DOWN], show=[T1_LOWER],
        against=T_BLOCK[:1], direction=[0, 1, 0], staged=True, labels={T1_LOWER: 'T1', T2_SOLID_DOWN: 'T2'}, **T_CAMERA)
g.place('Slide the other T2 down over it, slot into slot, until it clicks into the T1 as well.', move=[T2_SLOT_DOWN], against=T_BLOCK[:2],
        direction=[0, 1, 0], hover=65, staged=True, **T_CAMERA)       # (hover set: the automatic one left a lead line 0.1 mm long)
g.place('Press the other T1 onto the tops of the two T2 until it clicks.', move=[T1_UPPER], against=T_BLOCK[:3], direction=[0, 1, 0], staged=True, **T_CAMERA)
# ================================================================ T1 / T2 BLOCK (end)

g.build()
