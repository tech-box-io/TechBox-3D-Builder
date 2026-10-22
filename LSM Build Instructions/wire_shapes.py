"""(Since Lee's second note of 22 Oct 2026 the deconstruction keeps the matrix held over the box while D10 and the wires come off it,
with the Full Build's own wire shapes (held()), then lays the wires, still in the breadboard, out of the box onto the table (draped(),
draped_socket(): DRAPED, below), and uses MALE, FEMALE and JUMPERS from here; the laid and loose shapes are kept as measured, for the
record. DRAPED is measured at rest by docs/research/lsm/decon/round3/drape_check.py; this file's own check below covers LAID and LOOSE.)

The LSM deconstruction's new wire shapes, for the order of TechBox's published take-apart (instructions.online, 19075-laser_stem_
matrix_lsm_-_deconstruction): the LED matrix, D10 still hooked under it, laid on the table beside the open box (D4 and D5 off) with
its three wires still in the breadboard; the wires unplugged (a fade, as the published guide swaps models); and, in the view of the
matrix on its own, the three connectors pulled off its pins.

    laid(pose)          LAID: each wire from its pin (i2 / i3 / b19) out of the box through the open D4 side, under the matrix's edge,
                        through the notch in D10 to its socket on the matrix's header (the matrix at `pose`).
    loose(pose, off)    LOOSE: each wire from its socket, through the notch in D10, under the matrix and out past its edge to its pin
                        lying on the table; the pins ride on the matrix. off = mm the connectors are pulled off the pins (the view of
                        the matrix on its own): the same shape, moved with the six caps.
    loose_one(w, ...)   one wire's LOOSE route (the published guide unplugs them one per step: yellow, purple, gray).
    pin_pose(w, pose, off), pin_ride(w, off), socket_pose(w, pose, off), socket_ride(off): where the caps are (absolute) and their
                        poses riding on the matrix (for g.carry(..., by='MATRIX', pose=...) or unplug(..., ride_on='MATRIX')).
    LAID_POSE           where the published guide lays the matrix (turned half round about Y, its header at the box's D2 end), on
                        the table: lowered 32.7 mm from the published height (it floats there) so that D10's feet stand on the
                        table, and 2.5 mm further toward D2 so that D10's end clears the USB cable's A end.

Everything is in assembly mm, Y up, as guide.py. The routes are W.route() dicts, as guide.py's jumper() writes them: a = the pin (J_*_M),
b = the socket (J_*_F), a_at / b_at = where those were when the points were drawn, so that the player keeps each end on its part.

Run it on its own to build the shapes and measure them (no generator run; 9 s and 0.57 GB with a cache of the meshes, measured 21 Oct
2026; from lsm.glb the model's loading adds its own peak, about 0.4 GB):

    .venv.nosync/bin/python -I "LSM Build Instructions/wire_shapes.py" [--cache parts.npz] [--write-cache parts.npz]

It prints each wire's clearance (centre line every 0.2 mm, distance to each part's mesh minus the tube's radius 0.62; negative = into
the part) against every part present in each scene, the D9s swept up 54.4 mm (they come out after LAID), the other wires (USB cable,
the button's leads, the resistors' legs) and each other, and writes docs/research/lsm/decon/published/wire_shapes.json.

deconstruction.py (beside it) imports it (`import wire_shapes as WS`) and shows the calls: the matrix set down at LAID_POSE by a fade
with wires=laid(); the three pins unplugged by a fade to pin_pose(), riding on the matrix, with wires=loose(); on its own, D10 slid off
its hooks and down (it must go before the pull: with D10 on, the gray wire's curve into its socket meets D10's notch wall), then the
connectors pulled off with socket_pose(..., off=30) and pin_pose(..., off=30): both ends of each wire move by the same shift, so the
player carries the LOOSE shape along whole. Written for the take-apart's rebuild on TechBox's published guide (21 Oct 2026); its
research and the published data it follows are in docs/research/lsm/decon/published/.
"""
import json
import sys
from pathlib import Path

import numpy as np


def _root():
    """The project folder (the one with tools/stepgen.py), from wherever this file is (docs/research/... or the kit folder)."""
    for p in Path(__file__).resolve().parents:
        if (p / 'tools' / 'stepgen.py').exists():
            return p
    raise SystemExit('wire_shapes.py: cannot find tools/stepgen.py above ' + str(Path(__file__).resolve()))


ROOT = _root()
KIT = ROOT / 'LSM Build Instructions'
if str(ROOT / 'tools') not in sys.path:
    sys.path.insert(0, str(ROOT / 'tools'))
import wires as W  # noqa: E402
from stepgen import apply_pose, compose, relative_pose, turn_dir, turned, unapply_pose  # noqa: E402

ZERO = [0.0, 0.0, 0.0]
JUMPERS = ['white', 'grey', 'purple']                 # (as guide.py: 'white' is drawn and named yellow, 'grey' named gray)
MALE = {w: f'J_{w.upper()}_M' for w in JUMPERS}       # the pins (in i2, i3, b19)
FEMALE = {w: f'J_{w.upper()}_F' for w in JUMPERS}     # the sockets (on the matrix's V+, V- and IN pins)
WIRE = {w: f'wire {w}' for w in JUMPERS}
JUMPER_R = 0.62
TABLE_Y = 856.23

# ---------------------------------------------------------------- seated geometry (lsm.glb, as guide.py measures it)
ROW_X = dict(zip('abcdefghij', [624.50, 627.04, 629.58, 632.12, 634.66, 642.46, 645.00, 647.54, 650.08, 652.62]))
COL1_Z, PITCH = 1167.91, 2.54
HOLE = dict(white='i2', grey='i3', purple='b19')
MC = [638.82, 895.58, 1203.99]                        # guide.py's MC: mid(MATRIX).round(2), the pivot of its poses
M_MID = {w: [ROW_X[HOLE[w][0]], 873.92, COL1_Z + (int(HOLE[w][1:]) - 1) * PITCH] for w in JUMPERS}   # (each pin's middle)
M_EXIT = {w: np.array([M_MID[w][0], 879.92, M_MID[w][2]]) for w in JUMPERS}                       # guide.py's M_EXIT (wire end, +Y)
F_MID = dict(white=[608.24, 894.334, 1187.26], purple=[610.78, 894.334, 1187.26], grey=[613.32, 894.334, 1187.26])
F_EXIT = {w: np.array([F_MID[w][0], F_MID[w][1], 1191.26]) for w in JUMPERS}                      # guide.py's F_EXIT (wire end, +Z)
PULL = [0.0, 0.0, 1.0]                                # a socket comes off its pin along +Z in the matrix's own frame (guide.py's SOCKET_OFF)

# ---------------------------------------------------------------- where the matrix lies
# The published guide's Step 9c: turned((0, 1, 0), 180, at=MC, t=(-90.95, 5.89, 25.28)) (published_steps.json; our P_OUTSIDE has the
# same box but no turn, so its header lies at the far edge). Here: on the table (D10's feet, y 883.12 seated, at 856.28) and 2.5 mm
# further toward D2 (D10's far end tab then clears the USB cable's A end by 2.8 mm instead of 0.35).
LAID_T = [-90.95, TABLE_Y + 0.05 - 883.124, 25.28 + 2.5]
LAID_POSE = turned([0, 1, 0], 180.0, MC, [round(v, 3) for v in LAID_T])


def _laid_world(p):
    """Points drawn in assembly mm with the matrix at LAID_POSE, as the matrix's own (seated) coordinates."""
    return unapply_pose(LAID_POSE, np.asarray(p, float))


# ---------------------------------------------------------------- lines
def smooth(start, start_dir, end, end_dir, mids=(), lead=3.0, lead_b=None, spacing=0.5):
    """guide.py's smooth(): a short straight run out of each end (a wire leaves a pin or a housing straight), a spline between."""
    start, end = np.asarray(start, float), np.asarray(end, float)
    sd, ed = W._unit(start_dir), W._unit(end_dir)
    lb = lead if lead_b is None else lead_b
    a, b = start + sd * lead, end - ed * lb
    body = W.smooth([a, *[np.asarray(m, float) for m in mids], b], start_dir=sd, end_dir=ed, spacing=spacing)
    return W.resample(W.join(W.straight(start, sd, lead), body, W.straight(b, ed, lb)), 0.75)


def _clean(pose):
    """A pose with its rounding noise taken off (an axis of [1, 2.5e-17, 0] written [1, 0, 0])."""
    if isinstance(pose, dict):
        return dict(t=[round(float(v), 3) for v in pose['t']], r=[round(float(v), 6) for v in pose['r']], at=[round(float(v), 3) for v in pose['at']])
    return [round(float(v), 3) for v in pose]


def socket_pose(w, pose=LAID_POSE, off=0.0):
    """Where socket w is, the matrix at `pose` and the socket `off` mm off its pin (absolute: as a view's poses)."""
    return _clean(compose(pose, [v * off for v in PULL], F_MID[w]))


def socket_ride(off=0.0):
    """The socket's pose riding on the matrix (g.carry(..., by='MATRIX', pose=...)): ZERO on its pin, or `off` mm off it."""
    return [v * off for v in PULL]


def _f_end(w, pose, off=0.0):
    p = socket_pose(w, pose, off)
    return apply_pose(p, [F_EXIT[w]])[0], turn_dir(p, [0, 0, 1])


def _m_end(w, pose):
    return apply_pose(pose, [M_EXIT[w]])[0], turn_dir(pose, [0, 1, 0])


def _route(w, pts, m_pose, f_pose_):
    return W.route(pts, a=MALE[w], b=FEMALE[w], a_at=None if m_pose == ZERO else m_pose, b_at=None if f_pose_ == ZERO else f_pose_)


# ---------------------------------------------------------------- the run under the matrix (both shapes)
# Each socket's wire leaves its far end along the matrix's +Z (laid: -Z, toward D10 across the matrix's middle), 1.3 mm under the
# matrix's back. The only way past D10 under the matrix is the notch in its top edge that the wires lie in when built (seated x 605.18 -
# 612.79, y 889.10 up, D10's thickness z 1202.97 - 1205.97). In it the three share out the room evenly (0.43 mm between wire and
# wire, and between the outer wires and the notch's wall or the line of D10's hook lip, which the yellow one keeps clear of so that D10,
# taken off downward in the view of the matrix on its own, passes it): the gray one moved 1.6 mm in from its socket (which is 0.5 mm
# outside the notch). Then on under the matrix, over the USB cable (laid on the table under the matrix's middle).
NOTCH_X = dict(white=608.40, purple=610.07, grey=611.74)      # seated x in the notch (laid: 578.29, 576.62, 574.95)
RUN_Y = 893.35                                                # seated y of the run (laid 866.48): 1.6 mm under the matrix's back, 4.1 over the notch's bottom


def _socket_run(w, laid_zs):
    """The level run through the notch to just short of the socket, in the matrix's own frame (seated): from the laid z values `laid_zs`
    (with the matrix at LAID_POSE; ascending, toward the socket) on through D10 (seated z 1206.6, 1202.4: 0.6 mm either side of it) and
    an S into line with the socket."""
    x = NOTCH_X[w]
    zs = [float(_laid_world([[0.0, 0.0, z]])[0][2]) for z in laid_zs]
    return [[x, RUN_Y, z] for z in zs] + [[x, RUN_Y, 1206.6], [x, RUN_Y, 1202.4],
                                          [(x + F_EXIT[w][0]) / 2, (RUN_Y + F_EXIT[w][1]) / 2, 1197.6]]


# ---------------------------------------------------------------- LAID
# Pin -> socket. Inside the box every wire stays under the D9s' lower edges, so that the D9s, lifted straight out next, pass clear: the
# yellow and gray wires leave their pins toward D4, over the Nano Board beyond its ICSP pins (z > 1172) and under the end of D9_A (lower
# edge y 886.3 there); the purple one leaves b19 under D9_A (lower edge 882.2) beside the USB plug. Out of the box over D1's edge (D4
# is off) at the D2 end of the box, beside the USB cable (z 1219: 5 mm away), they turn under the matrix's edge into the run above.
# The order the wires lie in is not the same at the two ends (along the run the sockets give gray, purple, yellow across; the pins give
# yellow, gray, purple), so the yellow wire crosses over the other two, once each, where the box is open above them: it runs along
# D4's side of the box (x 605.4, about 16 mm over D1) toward D2, and the gray and purple wires, low on their way out, pass under it
# square on (see the report). No arrangement with fewer than two crossings exists: a wire's left-right place among the others is kept by
# any bend that stays level; coming off the pins toward D4 the yellow wire is on the right of the gray one (and the purple to the left
# of both), arriving at the sockets it must be on the left of both (gray, purple, yellow from the right). Only a crossing, a half twist
# or a run up and back over (as the built wires go up into D10 and back) changes that, and the yellow wire must pass two others.
BOX_MIDS = dict(   # assembly mm (fixed: the box does not move)
    white=[[646.0, 883.8, 1171.9], [636.0, 884.0, 1173.9], [626.0, 884.3, 1175.4], [618.6, 884.6, 1176.4], [613.0, 884.0, 1177.6],
           [608.6, 882.2, 1180.0], [605.9, 880.6, 1184.5], [605.4, 879.6, 1192.0], [605.4, 879.0, 1200.0], [605.3, 878.5, 1206.5],
           [603.6, 877.4, 1211.6], [600.0, 875.2, 1213.9], [595.5, 872.2, 1214.0]],
    grey=[[646.0, 881.2, 1174.2], [636.0, 880.6, 1176.0], [626.0, 880.4, 1177.4], [618.6, 880.3, 1178.4], [614.6, 879.3, 1180.8],
          [612.9, 877.9, 1186.0], [612.3, 876.2, 1194.0], [609.6, 873.8, 1202.4], [604.0, 870.6, 1207.6], [597.5, 868.4, 1209.2]],
    purple=[[624.0, 881.7, 1213.4], [618.6, 881.0, 1213.0], [613.0, 878.4, 1212.6], [608.0, 874.4, 1212.0], [603.0, 871.4, 1211.7],
            [597.5, 869.4, 1211.6]])
# Outside the box, drawn with the matrix at LAID_POSE and riding with it (laid world mm; turned into the matrix's frame below): down
# to the run's height and into the turn under the matrix's +X edge (x 579.8), each wire turning inside the one before (yellow first).
OUT_MIDS = dict(
    white=[[589.0, 869.0, 1214.0], [584.0, 867.2, 1214.0], [580.6, 866.6, 1214.9], [578.7, 866.5, 1216.9]],
    purple=[[589.0, 867.9, 1211.6], [584.0, 866.9, 1211.6], [579.4, 866.5, 1212.5], [577.0, 866.5, 1214.9]],
    grey=[[589.0, 867.3, 1209.2], [584.0, 866.7, 1209.2], [578.2, 866.5, 1210.0], [575.35, 866.5, 1212.7]])
LAID_RUN = [1219.0, 1223.0, 1226.5]   # laid z of the level run's first points (then _socket_run's own)
PIN_LEAD = dict(white=3.0, grey=3.0, purple=2.0)   # (the purple wire bends toward D9_A sooner: the USB plug's corner is 0.4 mm beside it)


def laid(pose=LAID_POSE):
    """LAID: {wire id: route}, the matrix at `pose` (LAID_POSE, or a pose near it: the part outside the box rides with the matrix)."""
    out = {}
    for w in JUMPERS:
        a, ad = _m_end(w, ZERO)
        b, bd = _f_end(w, pose)
        outside = apply_pose(pose, _laid_world(OUT_MIDS[w]))
        run = apply_pose(pose, _socket_run(w, LAID_RUN))
        line = smooth(a, ad, b, -bd, [*BOX_MIDS[w], *outside, *run], lead=PIN_LEAD[w])
        out[WIRE[w]] = _route(w, line, ZERO, socket_pose(w, pose))
    return out


# ---------------------------------------------------------------- LOOSE
# Socket -> run through D10's notch -> on under the matrix, coming down over the USB cable (y 864.6 over it) and under where the wires
# still plugged in turn toward the box (3 - 5 mm under them: the published guide unplugs one wire at a time, so a loose wire lies beside
# plugged ones) -> out past the matrix's edge (D3's end of it, laid z 1201.6) -> its pin lying on the table, pointing away from the
# matrix, 2.8 mm apart. Drawn with the matrix at LAID_POSE (laid world mm) and riding with it.
PIN_X = dict(grey=573.9, purple=576.7, white=579.5)          # the pins lying on the table (laid world x) ...
PIN_END_Z = 1189.0                                            # ... their wire ends at this z, their tips 12 mm further on (-Z)
PIN_AXIS_Y = TABLE_Y + 0.875                                  # (the housing is 1.75 mm square)
LOOSE_MIDS = dict(   # laid world mm, pin -> run
    white=[[579.3, 857.9, 1196.0], [578.8, 860.2, 1204.0], [578.35, 862.8, 1212.0], [578.29, 864.6, 1219.0], [578.29, 865.9, 1224.5]],
    purple=[[576.7, 857.9, 1196.0], [576.65, 860.2, 1204.0], [576.62, 862.8, 1212.0], [576.62, 864.6, 1219.0], [576.62, 865.9, 1224.5]],
    grey=[[574.05, 857.9, 1196.0], [574.6, 860.2, 1204.0], [574.9, 862.8, 1212.0], [574.95, 864.6, 1219.0], [574.95, 865.9, 1224.5]])
LOOSE_RUN = [1227.6]          # laid z where the level run toward the notch begins


def _pin_laid(w):
    """The pin lying on the table, the matrix at LAID_POSE: its wire end toward the matrix (+Z), its tip away (-Z)."""
    end = np.array([PIN_X[w], PIN_AXIS_Y, PIN_END_Z])
    return turned([1, 0, 0], 90.0, M_EXIT[w].tolist(), (end - M_EXIT[w]).round(3).tolist())


def pin_ride(w, off=0.0):
    """The pin's pose riding on the matrix (g.carry([...], by='MATRIX', pose=...) / unplug(ride_on='MATRIX')), `off` mm pulled."""
    rel = relative_pose(LAID_POSE, _pin_laid(w), M_MID[w])
    return _clean(compose([v * off for v in PULL], rel, M_MID[w]) if off else rel)


def pin_pose(w, pose=LAID_POSE, off=0.0):
    """Where pin w lies (absolute), the matrix at `pose` and the connectors pulled `off` mm."""
    return _clean(compose(pose, pin_ride(w, off), M_MID[w]))


def loose_one(w, pose=LAID_POSE, off=0.0):
    """One wire's LOOSE route: {wire id: route}. off: mm the connectors are pulled off the pins (the six caps and the wires move as one)."""
    shift = np.array([v * off for v in PULL])
    pp, fp = pin_pose(w, pose, off), socket_pose(w, pose, off)
    a, ad = _m_end(w, pp)
    b, bd = _f_end(w, pose, off)
    mids = apply_pose(pose, _laid_world(LOOSE_MIDS[w]) + shift)
    run = apply_pose(pose, np.asarray(_socket_run(w, LOOSE_RUN), float) + shift)
    line = smooth(a, ad, b, -bd, [*mids, *run])
    return {WIRE[w]: _route(w, line, pp, fp)}


def loose(pose=LAID_POSE, off=0.0):
    """LOOSE: {wire id: route} for the three."""
    return {k: v for w in JUMPERS for k, v in loose_one(w, pose, off).items()}


# ---------------------------------------------------------------- DRAPED (Lee, 22 Oct 2026, after the matrix came off its wires held over
# the box: "Add a step that lays the three wires over the side of the box, still in the breadboard, before the D9s come out")
# Each wire keeps the Full Build's own run in the box (its held shape, HELD: from its pin toward D4, under the D9 nearer D4, along the
# D4 end toward D2), as far as just short of where that shape turns up beside D2; from there it turns out over D1's edge where D4 was
# (19 - 21 mm over it), and down onto the table outside, where it runs straight out, parallel to the USB cable, as long as the wire is
# (at least as long as the same wire HELD: 261, 252 and 184 mm), its connector lying on the table with its wire end toward the box,
# the three side by side. They turn
# out in the order HELD rises toward D2 (gray, purple, yellow: z 1247.3, 1248.7, 1250.0 there), so that changing from HELD no wire
# passes another; along the D4 end the yellow one lies nearest the open end, so the gray and purple ones cross over it (2.1 and 2.5 mm
# from it, centre to centre) as they turn out. The USB cable leaves the box 20 mm nearer D3 (z 1219); D2's tabs past D1's edge are 5 mm further on.
DRAPE = dict(   # where each leaves HELD (z), its run out over D1's edge (z, y), its connector's middle on the table (z)
    grey=dict(turn=1238.5, out=1240.0, y=884.5, lie=1239.5),
    purple=dict(turn=1240.5, out=1242.5, y=884.5, lie=1243.0),
    white=dict(turn=1244.0, out=1245.5, y=None, lie=1246.5))   # (y None: level from where it leaves HELD, 882.6)


def held():
    """HELD: {wire id: route}, the Full Build's own shapes as its Step 32 begins (the matrix held over the box): the deconstruction's
    wires from its Step 9c until they are laid out."""
    S = json.loads((KIT / 'steps.json').read_text(encoding='utf-8'))
    v = next(x for x in S['views'] if x['name'] == 'Step 32')
    return {WIRE[w]: S['routes'][v['wires'][WIRE[w]]] for w in JUMPERS}


def _length(pts):
    return float(np.linalg.norm(np.diff(np.asarray(pts, float), axis=0), axis=1).sum())


def _draped_line(w, lie_x):
    """Wire w's DRAPED points with its connector's middle at x `lie_x` on the table, and where it leaves HELD (mm from its pin)."""
    h, d = held()[WIRE[w]], DRAPE[w]
    p = np.asarray(h['pts'], float)
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    k = int(np.argmax(p[:, 2] >= d['turn']))                       # (the first point of the run along the D4 end past its turn)
    assert k and p[k, 1] < 885.0 and s[k] < (h.get('tail_from') or s[-1]), (w, k, p[k])   # (before HELD turns up)
    keep, here = p[:k], p[k - 1]
    y = here[1] if d['y'] is None else d['y']
    pose = _socket_on_table(w, lie_x)
    b, bd = apply_pose(pose, [F_EXIT[w]])[0], turn_dir(pose, [0, 0, 1])
    on_table = [[x, TABLE_Y + 0.95, d['lie']] for x in np.arange(574.0, b[0] + 6.0, -8.0)]   # (straight out along the table)
    mids = [[here[0] - 1.0, (here[1] + y) / 2, here[2] + 0.7 * (d['out'] - here[2])], [here[0] - 3.5, y, d['out']],
            [598.0, y, d['out']], [591.0, y - 2.5, d['out']], [585.0, 870.0, (d['out'] + d['lie']) / 2], [580.0, 860.5, d['lie']],
            *on_table]
    tail = smooth(here, np.array([0.0, 0.0, 1.0]), b, -bd, mids, lead=0.4)
    return np.vstack([keep[:-1], tail]), float(s[k - 1]), pose


def _socket_on_table(w, lie_x):
    mid = np.array(F_MID[w], float)
    there = np.array([lie_x, TABLE_Y + 0.875, DRAPE[w]['lie']])
    return _clean(turned([0, 1, 0], 90.0, mid.tolist(), (there - mid).round(3).tolist()))


def _lie_x():
    """Where the sockets' middles lie (x): side by side, as far out as the wire that needs it most must lie to be as long as it is HELD
    (the other two a few mm longer: changing shape the player takes that up between the ends; lined up, they keep their order as they
    change). Each wire's own place is found by moving it out by what it lacks, until that is under 0.01 mm."""
    out = []
    for v in JUMPERS:
        want, x = _length(held()[WIRE[v]]['pts']), 567.0
        for _ in range(8):
            short = want - _length(_draped_line(v, x)[0])
            x -= short
            if abs(short) < 0.01:
                break
        else:
            raise SystemExit(f'wire_shapes.py: DRAPED {v}: the length did not settle ({short:.3f} mm short)')
        out.append(x)
    return round(min(out), 2)


def draped_socket(w):
    """Where socket w lies on the table (absolute): a quarter turn about Y on its middle, so that its wire end faces the box (+X)."""
    return _socket_on_table(w, _lie_x())


def draped():
    """DRAPED: {wire id: route}, the three wires out of the box over its open D4 end and onto the table, still in the breadboard, each as
    long as it is HELD. Each keeps HELD's points up to its turn and says so (`tail_from`), so that changing from HELD the run in the box
    stays put and the rest is matched from the connector's end."""
    out, x = {}, _lie_x()
    for w in JUMPERS:
        line, keep_to, pose = _draped_line(w, x)
        L = _length(line)
        assert L >= _length(held()[WIRE[w]]['pts']) - 0.05, (w, L)       # (never shorter than HELD: see above)
        out[WIRE[w]] = W.route(line, a=MALE[w], b=FEMALE[w], b_at=pose, b_from=L - 6.0, tail_from=keep_to)
    return out


# ================================================================ the check
STEP = 0.2


def _dense(pts, step=STEP):
    pts = np.asarray(pts, float)
    L = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    s = np.arange(0.0, L[-1] + 1e-9, step)
    return np.c_[[np.interp(s, L, pts[:, k]) for k in range(3)]].T, s, L[-1]


class Parts:
    """The part meshes (trimesh, seated), cropped near each query (the Nano has 380 000 triangles)."""

    def __init__(self, meshes):
        self.m = meshes
        self.box = {i: m.bounds for i, m in meshes.items()}
        self._subs = {}

    @classmethod
    def load(cls, cache=None, write_cache=None):
        import trimesh
        if cache and Path(cache).exists():
            z = np.load(cache)
            ids = sorted({k[:-3] for k in z.files})
            return cls({i: trimesh.Trimesh(z[i + '__v'], z[i + '__f'], process=False) for i in ids})
        from stepgen import Model
        spec = json.loads((KIT / 'materials.json').read_text(encoding='utf-8'))
        M = Model(KIT / spec['source'], adjust=spec.get('adjust_mm') or {}, own_parts=spec.get('own_parts', {}),
                  extra_parts={i: (KIT / e['glb'], e['pose']) for i, e in spec.get('extra_parts', {}).items()})
        meshes = {i: m for i, m in M.inst.items() if not i.startswith('STEM_') and i != 'BACKING'}
        if write_cache:
            np.savez_compressed(write_cache, **{f'{i}__{k}': (m.vertices if k == 'v' else m.faces) for i, m in meshes.items() for k in 'vf'})
        return cls(meshes)

    def clearance(self, i, pose, pts, radius, reach=3.0):
        """Each point's distance to part i (at `pose`) minus `radius`, negative inside; None where farther than `reach`."""
        import trimesh
        q = unapply_pose(pose, pts) if pose not in (None, ZERO) else np.asarray(pts, float)
        lo, hi = self.box[i]
        sel = np.all((q > lo - radius - reach) & (q < hi + radius + reach), axis=1)
        out = np.full(len(q), np.nan)
        if not sel.any():
            return out
        qs = q[sel]
        m = self.m[i]
        blo, bhi = qs.min(0) - 8.0, qs.max(0) + 8.0
        tri = m.vertices[m.faces]
        keep = np.all(tri.min(axis=1) < bhi, axis=1) & np.all(tri.max(axis=1) > blo, axis=1)   # (triangles whose box meets the query's)
        if not keep.any():
            return out
        key = (i, keep.tobytes().__hash__())
        if key not in self._subs:
            if len(self._subs) > 64:
                self._subs.clear()
            self._subs[key] = trimesh.Trimesh(m.vertices, m.faces[keep], process=False)
        sub = self._subs[key]
        cp, d, tri = trimesh.proximity.closest_point(sub, qs)
        inside = np.einsum('ij,ij->i', qs - cp, sub.face_normals[tri]) < -0.3 * d
        out[np.flatnonzero(sel)] = np.where(inside, -d, d) - radius
        return out


def other_wires():
    """The wires that stay as the Full Build left them (its last view): the USB cable, the button's leads, the resistors' legs."""
    S = json.loads((KIT / 'steps.json').read_text(encoding='utf-8'))
    last = [v for v in S['views'] if v.get('wires')][-1]
    return {w: dict(pts=S['routes'][n]['pts'], radius=S['wires'][w]['radius']) for w, n in last['wires'].items() if not w.startswith('wire ')}


def measure(parts, routes, poses, present, others=(), sweep=(), end_skip=0.0):
    """Per wire: its least clearance to every part present (at poses), to the table, to each other wire; the D9s in `sweep` lifted
    0 - 54.4 mm. Returns {wire: {'parts': {id: (clearance, at)}, 'wires': {...}, 'min': (clearance, what, at)}}."""
    res = {}
    dense = {w: _dense(r['pts']) for w, r in routes.items()}
    for w, r in routes.items():
        pts, s, L = dense[w]
        inner = (s >= end_skip) & (s <= L - end_skip)
        own = {r.get('a'), r.get('b')}
        rec = {}
        for i in present:
            if i in own or i not in parts.m:
                continue
            c = parts.clearance(i, poses.get(i, ZERO), pts, JUMPER_R)
            c[~inner] = np.nan
            if np.isfinite(c).any():
                k = int(np.nanargmin(c))
                rec[i] = (round(float(c[k]), 3), pts[k].round(2).tolist())
        for i in sweep:
            best = (np.inf, None)
            for h in np.arange(0.0, 54.41, 0.5):
                c = parts.clearance(i, [0.0, float(h), 0.0], pts, JUMPER_R)
                c[~inner] = np.nan
                if np.isfinite(c).any() and np.nanmin(c) < best[0]:
                    k = int(np.nanargmin(c))
                    best = (float(c[k]), pts[k].round(2).tolist(), float(h))
            if best[1] is not None:
                rec[f'{i} lifted (at {best[2]:.1f} mm)'] = (round(best[0], 3), best[1])
        t = pts[:, 1] - TABLE_Y - JUMPER_R
        k = int(np.argmin(t))
        rec['table'] = (round(float(t[k]), 3), pts[k].round(2).tolist())
        wires = {}
        from scipy.spatial import cKDTree
        for o, (opts, _, _) in dense.items():
            if o != w:
                d, j = cKDTree(opts).query(pts)
                k = int(np.argmin(d))
                wires[o] = (round(float(d[k] - 2 * JUMPER_R), 3), pts[k].round(2).tolist())
        for o, od in dict(others).items():
            opts = _dense(od['pts'])[0]
            d, j = cKDTree(opts).query(pts)
            k = int(np.argmin(d))
            wires[o] = (round(float(d[k] - JUMPER_R - od['radius']), 3), pts[k].round(2).tolist())
        allc = [(v[0], k, v[1]) for k, v in rec.items()] + [(v[0], k, v[1]) for k, v in wires.items()]
        res[w] = dict(parts=rec, wires=wires, min=min(allc), length=round(float(L), 1))
    return res


BASE = ['D1', 'D2', 'D3', 'BREADBOARD', 'NANO', 'R12K', 'R330', 'CAP', 'BUTTON', 'NUT', 'BTN_RED_PIN', 'BTN_BLACK_PIN', 'USB_B', 'USB_A']
CAPS = list(MALE.values()) + list(FEMALE.values())


def scenes():
    """The scenes the shapes must hold in, after the published order: Step 9c - 10 (LAID; the D9s still in, then lifted out), Steps
    11c - 13c (each wire unplugged in turn: every mix of LAID and LOOSE), the matrix on its own (LOOSE; D10 dropped off it, then the
    connectors pulled 0 - 30 mm)."""
    out = []
    matrix = dict(MATRIX=LAID_POSE, D10=LAID_POSE)
    sock = {FEMALE[w]: socket_pose(w) for w in JUMPERS}
    out.append(dict(name='LAID, D9s in (Step 9c), then lifted out (Step 10)', routes=laid(), poses={**matrix, **sock},
                    present=BASE + ['D9_A', 'D9_B', 'MATRIX', 'D10'] + CAPS, sweep=['D9_A', 'D9_B'], others=True))
    from itertools import combinations
    for n in range(1, 4):
        for gone in combinations(['white', 'purple', 'grey'], n):
            r = laid()
            r.update({k: v for w in gone for k, v in loose_one(w).items()})
            pins = {MALE[w]: pin_pose(w) for w in gone}
            out.append(dict(name=f'unplugged: {", ".join(gone)} (D9s out)', routes=r, poses={**matrix, **sock, **pins},
                            present=BASE + ['MATRIX', 'D10'] + CAPS, others=True))
    for off in (0.0, 7.5, 15.0, 22.5, 30.0):
        caps = {**{FEMALE[w]: socket_pose(w, off=off) for w in JUMPERS}, **{MALE[w]: pin_pose(w, off=off) for w in JUMPERS}}
        out.append(dict(name=f'on its own, D10 off, connectors pulled {off:g} mm', routes=loose(off=off), poses={**matrix, **caps},
                        present=['MATRIX'] + CAPS, others=False, table=False))
        out.append(dict(name=f'on its own, D10 still on, connectors pulled {off:g} mm', routes=loose(off=off), poses={**matrix, **caps},
                        present=['MATRIX', 'D10'] + CAPS, others=False, table=False))
    for h in (0.0, 5.0, 10.0, 20.0, 30.0):                    # (D10 dropped off the matrix, the wires as LOOSE)
        caps = {**sock, **{MALE[w]: pin_pose(w) for w in JUMPERS}}
        out.append(dict(name=f'on its own, D10 dropped {h:g} mm', routes=loose(), poses={**matrix, **caps, 'D10': compose([0.0, -h, 0.0], LAID_POSE, MC)},
                        present=['D10'], others=False, table=False))
    return out


def main():
    args = sys.argv[1:]
    cache = args[args.index('--cache') + 1] if '--cache' in args else None
    write_cache = args[args.index('--write-cache') + 1] if '--write-cache' in args else None
    parts = Parts.load(cache, write_cache)
    # (the constants above against the model)
    for w in JUMPERS:
        assert np.allclose(parts.m[FEMALE[w]].bounds.mean(0), F_MID[w], atol=0.01), (w, parts.m[FEMALE[w]].bounds.mean(0))
        assert np.allclose(parts.m[MALE[w]].bounds.mean(0), M_MID[w], atol=0.01), (w, parts.m[MALE[w]].bounds.mean(0))
        assert abs(parts.m[FEMALE[w]].bounds[1][2] - 1191.26) < 0.01
        for off in (0.0, 30.0):                     # (each route's ends are on its caps, and the caps ride on the matrix as stated)
            r = loose_one(w, off=off)[WIRE[w]]
            assert np.allclose(r['pts'][0], apply_pose(pin_pose(w, off=off), [M_EXIT[w]])[0], atol=0.02)
            assert np.allclose(r['pts'][-1], apply_pose(socket_pose(w, off=off), [F_EXIT[w]])[0], atol=0.02)
            assert np.allclose(apply_pose(pin_pose(w, off=off), [M_MID[w]]), apply_pose(compose(LAID_POSE, pin_ride(w, off), M_MID[w]), [M_MID[w]]))
        r = laid()[WIRE[w]]
        assert np.allclose(r['pts'][0], M_EXIT[w], atol=0.02) and np.allclose(r['pts'][-1], apply_pose(socket_pose(w), [F_EXIT[w]])[0], atol=0.02)
    others = other_wires()
    report, worst = [], {}
    # (the parts the shapes put somewhere new, against what is there: the matrix and D10 laid on the table, the pins lying on it)
    print('== parts placed: least clearance to the parts and the USB cable around them (vertices, mm; negative = into it)')
    cable = _dense(others['usb cable']['pts'])[0]
    from scipy.spatial import cKDTree
    placed = [('MATRIX', LAID_POSE), ('D10', LAID_POSE)] + [(MALE[w], pin_pose(w)) for w in JUMPERS]
    for i, pose in placed:
        v = parts.m[i].vertices
        v = apply_pose(pose, v[np.random.default_rng(0).choice(len(v), min(len(v), 6000), replace=False)])
        near = []
        for o in BASE + ['MATRIX', 'D10'] + CAPS:
            if o in (i, 'MATRIX' if i == 'D10' else None, 'D10' if i == 'MATRIX' else None) or (i in MALE.values() and o == i):
                continue
            opose = dict(placed).get(o, socket_pose(o.split('_')[1].lower()) if o in FEMALE.values() else ZERO)
            c = parts.clearance(o, opose, v, 0.0, reach=5.0)
            if np.isfinite(c).any():
                near.append((round(float(np.nanmin(c)), 2), o))
        dc = float(cKDTree(cable).query(v)[0].min() - others['usb cable']['radius'])
        near.append((round(dc, 2), 'usb cable'))
        near.append((round(float(v[:, 1].min() - TABLE_Y), 2), 'table'))
        print(f'  {i:12s} ' + ', '.join(f'{k} {c:+.2f}' for c, k in sorted(near)[:5]))
    for sc in scenes():
        res = measure(parts, sc['routes'], sc['poses'], sc['present'], others=others if sc.get('others') else (), sweep=sc.get('sweep', ()))
        if sc.get('table') is False:
            for w in res:
                res[w]['parts'].pop('table', None)
                allc = [(v[0], k, v[1]) for k, v in res[w]['parts'].items()] + [(v[0], k, v[1]) for k, v in res[w]['wires'].items()]
                res[w]['min'] = min(allc) if allc else (np.inf, '-', None)
        report.append(dict(scene=sc['name'], wires={w: dict(min=r['min'], length=r['length'], parts=r['parts'], wires=r['wires']) for w, r in res.items()
                                                    if w.startswith('wire ')}))
        print(f'\n== {sc["name"]}')
        for w, r in res.items():
            m = r['min']
            print(f'  {w:12s} {r["length"]:6.1f} mm  least {m[0]:+.2f} mm ({m[1]} at {m[2]})')
            close = sorted([(v[0], k) for k, v in {**r['parts'], **r['wires']}.items()])[:4]
            print('      nearest: ' + ', '.join(f'{k} {c:+.2f}' for c, k in close))
            if 'D10 still on' not in sc['name']:
                worst[w] = min(worst.get(w, (np.inf,)), (m[0], sc['name'], m[1]))
    print('\n== least clearance per wire over all scenes (but the pull with D10 still on, which shows D10 must come off first)')
    for w, m in worst.items():
        print(f'  {w:12s} {m[0]:+.2f} mm  ({m[2]}; {m[1]})')
    out = dict(
        _about='LSM deconstruction wire shapes (docs/research/lsm/decon/published/wire_shapes.py): routes as W.route dicts, poses as stepgen '
               'poses, clearances in mm (centre line every 0.2 mm, distance to the mesh minus the 0.62 mm tube radius; negative = into it).',
        LAID_POSE=LAID_POSE, laid=laid(), loose=loose(), loose_pulled_30=loose(off=30.0),
        pin_pose={MALE[w]: pin_pose(w) for w in JUMPERS}, pin_ride={MALE[w]: pin_ride(w) for w in JUMPERS},
        socket_pose={FEMALE[w]: socket_pose(w) for w in JUMPERS},
        clearances=report, least=worst)
    path = ROOT / 'docs/research/lsm/decon/published/wire_shapes.json'
    path.write_text(json.dumps(out, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else float(o)), encoding='utf-8')
    print('\nwrote', path)


if __name__ == '__main__':
    main()
