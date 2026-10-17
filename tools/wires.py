"""Routes for flexible wires.

A wire in a guide is not a CAD part: it is a centre line (a "route") that the player draws as a round
tube. This module makes routes: from a few corner points, from a CAD cable's centre line, as the
side-by-side conductors of a flat lead, or cut short with a break mark.

    route(points, a='NAUO45', b='NAUO82')    a route tied to the part at each end (see route())

All points are millimetres in assembly space, in seated coordinates: where things are when built.
"""
import json

import numpy as np


def route(points, a=None, b=None, mark=None, a_at=None, b_at=None, b_from=None, fade=None, stretch=False):
    """A route as steps.json stores it.

    a, b: the part ids at the first and last point. The wire moves with them: the first part of its
    length follows `a` and the last part follows `b`, blending between, so it stretches and swings as
    either end is lifted or tilted. With only `a`, the whole wire rides with that part.
    a_at, b_at: the pose that end's part was at when these points were drawn, if not its seat. A lead whose
    loose plug rides with the servo (see Guide.carry) is drawn with the plug at its riding pose: give that
    pose as b_at, and the end of the wire stays in the plug as the plug is carried about and then plugged in.
    b_from: millimetres from the first point up to which the wire does not follow `b` at all. For a lead that is
    held in a slot part of the way along: the run from the servo to the slot then stays put while the plug is moved.
    mark: a polyline drawn in black with the wire (a break mark across a cut end); it rides with `a`.
    fade: (from_mm, to_mm) along the wire from its first point: the wire fades out between the two, for a wire that
    runs on but is left out of the picture (the joysticks' wires while a joystick is in the hand). Draw the route a
    little past to_mm.
    stretch: when the wire changes to or from this route, each bit of it keeps its share of the wire's length, not its
    distance from the first end: a representative lead that is longer or shorter in its next shape then stretches evenly
    instead of growing out of its tip (or bunching at it). For a lead whose length does not matter (the RCC's motor leads).
    """
    out = dict(pts=np.round(np.asarray(points, float), 2).tolist(), a=a, b=b)
    if b_from:
        out['b_from'] = float(b_from)
    for key, pose in (('a_ref', a_at), ('b_ref', b_at)):
        if pose is not None:
            out[key] = pose if isinstance(pose, dict) else [float(x) for x in pose]
    if mark is not None:
        out['mark'] = np.round(np.asarray(mark, float), 2).tolist()
    if fade is not None:
        out['fade'] = [float(fade[0]), float(fade[1])]
    if stretch:
        out['stretch'] = True
    return out


def length(points):
    p = np.asarray(points, float)
    return float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum())


def resample(points, spacing=1.5):
    """The same line as points about `spacing` mm apart."""
    p = np.asarray(points, float)
    d = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))])
    keep = np.concatenate([[True], np.diff(d) > 1e-9])
    p, d = p[keep], d[keep]
    n = max(2, int(np.ceil(d[-1] / spacing)) + 1)
    at = np.linspace(0.0, d[-1], n)
    return np.stack([np.interp(at, d, p[:, k]) for k in range(3)], axis=1)


def smoothed(points, window_mm=20.0, spacing=0.5):
    """The same line with its small wiggles taken out (a cable the CAD models twisted, whose centre line winds round
    a helix): each point moves to the average of the line within window_mm / 2 of it on either side, the window
    shrinking towards the two ends so that they stay where they are."""
    p = resample(points, spacing)
    n, half = len(p), max(1, int(round(window_mm / 2 / spacing)))
    out = p.copy()
    for _ in range(2):                                    # twice: a box average of a box average is smooth
        total = np.cumsum(np.vstack([np.zeros(3), out]), axis=0)
        nxt = out.copy()
        for i in range(n):
            h = min(half, i, n - 1 - i)
            if h:
                nxt[i] = (total[i + h + 1] - total[i - h]) / (2 * h + 1)
        out = nxt
    return out


def along(points, start_mm=0.0, end_mm=None):
    """The stretch of a line between two distances from its first point."""
    p = resample(points, 0.5)
    d = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))])
    end_mm = d[-1] if end_mm is None else min(end_mm, d[-1])
    return p[(d >= start_mm - 1e-9) & (d <= end_mm + 1e-9)]


def rounded(corners, radius=4.0, spacing=1.5):
    """A line through corner points with each corner rounded off (how a wire actually bends)."""
    c = np.asarray(corners, float)
    out = [c[0]]
    for i in range(1, len(c) - 1):
        u, v = c[i] - c[i - 1], c[i + 1] - c[i]
        lu, lv = np.linalg.norm(u), np.linalg.norm(v)
        u, v = u / lu, v / lv
        turn = np.arccos(np.clip(u @ v, -1.0, 1.0))
        if turn < 1e-3 or np.pi - turn < 1e-3:
            out.append(c[i])
            continue
        cut = min(radius * np.tan(turn / 2), 0.45 * lu, 0.45 * lv)     # how far from the corner the bend starts
        r = cut / np.tan(turn / 2)
        start, centre = c[i] - u * cut, c[i] + (v - u) / np.linalg.norm(v - u) * (r / np.cos(turn / 2))
        x, y = start - centre, np.cross(np.cross(u, v) / np.linalg.norm(np.cross(u, v)), start - centre)
        for t in np.linspace(0.0, turn, max(3, int(np.ceil(r * turn / spacing)) + 1)):
            out.append(centre + x * np.cos(t) + y * np.sin(t))
    out.append(c[-1])
    return resample(np.array(out), spacing)


def _unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def _about(axis, angle):
    """Rotation matrix: `angle` radians about the unit vector `axis`."""
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * K @ K


def smootherstep(t):
    t = np.clip(np.asarray(t, float), 0.0, 1.0)
    return t * t * t * (t * (6 * t - 15) + 10)


def smooth(points, start_dir=None, end_dir=None, spacing=1.0):
    """A smooth line through a few control points: a C2 cubic spline parameterised by chord length, its first and last
    tangents along start_dir / end_dir when given (a natural end otherwise), resampled every `spacing` mm. No corners, so a
    lead drawn this way bends evenly (rounded() joins straight runs with tight bends)."""
    from scipy.interpolate import make_interp_spline
    P = np.asarray(points, float)
    u = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
    left = [(1, _unit(start_dir))] if start_dir is not None else [(2, np.zeros(3))]
    right = [(1, _unit(end_dir))] if end_dir is not None else [(2, np.zeros(3))]
    dense = make_interp_spline(u, P, k=3, bc_type=(left, right))(np.linspace(0.0, u[-1], max(200, int(u[-1] / 0.1))))
    return resample(dense, spacing)


def ribbon(points, across, pitch=1.27, n=3, end_pitch=None, fan_mm=0.0, end_across=None, twist=None):
    """The n side-by-side conductors of a flat lead whose middle follows `points`.

    across: which way the lead is wide at its first point. Returns n lines; the first is the one furthest along
    -across. The lead is carried along without twisting, unless end_across says which way it must be wide at its
    last point (to meet a plug): the twist needed is then spread evenly along its length, or done between twist =
    (from_mm, to_mm) along it, easing in and out (a lead that turns flat as it comes up out of a notch, then runs on flat).
    end_pitch, fan_mm: the conductors spread to end_pitch over the last fan_mm (into a plug's contacts).
    """
    p = resample(points, 1.0)
    t = np.gradient(p, axis=0)
    t /= np.linalg.norm(t, axis=1)[:, None]
    d = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))])
    side = np.asarray(across, float)
    sides = []
    for k in range(len(p)):                              # carried along without twisting
        side = side - t[k] * (side @ t[k])
        side = side / np.linalg.norm(side)
        sides.append(side)
    sides = np.array(sides)
    if end_across is not None:
        want = np.asarray(end_across, float)
        want = _unit(want - t[-1] * (want @ t[-1]))
        roll = np.arctan2(np.cross(sides[-1], want) @ t[-1], sides[-1] @ want)
        frac = d / d[-1] if twist is None else smootherstep((d - twist[0]) / (twist[1] - twist[0]))
        sides = np.array([_about(t[k], roll * frac[k]) @ sides[k] for k in range(len(p))])
    gap = np.full(len(p), float(pitch))
    if end_pitch is not None and fan_mm > 0:
        u = np.clip((d - (d[-1] - fan_mm)) / fan_mm, 0.0, 1.0)
        gap = pitch + (end_pitch - pitch) * u * u * (3 - 2 * u)
    return [p + sides * (gap * (k - (n - 1) / 2))[:, None] for k in range(n)]


def curve(start, start_dir, end, end_dir, pull=None, spacing=1.5):
    """A smooth run from `start` (leaving along start_dir) to `end` (arriving along end_dir): a cubic Bezier whose
    handles are `pull` mm long (default a third of the distance). For a loose cable between two plugs."""
    a, b = np.asarray(start, float), np.asarray(end, float)
    pull = np.linalg.norm(b - a) / 3 if pull is None else pull
    c1, c2 = a + _unit(start_dir) * pull, b - _unit(end_dir) * pull
    t = np.linspace(0.0, 1.0, 200)[:, None]
    pts = (1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * c1 + 3 * (1 - t) * t ** 2 * c2 + t ** 3 * b
    return resample(pts, spacing)


def straight(start, direction, length):
    """A straight run from `start`."""
    start, direction = np.asarray(start, float), _unit(direction)
    return np.array([start, start + direction * length])


def join(*pieces):
    """Lines placed end to end as one (a point shared by two pieces is kept once)."""
    out = [np.asarray(pieces[0], float)]
    for piece in pieces[1:]:
        piece = np.asarray(piece, float)
        out.append(piece[1:] if np.linalg.norm(piece[0] - out[-1][-1]) < 1e-6 else piece)
    return np.vstack(out)


def plug(info, g_towards):
    """What a route needs to know about a plug, from its CAD measurements (one entry of "plugs" in wire-paths.json).

    g_towards: a direction; the contact furthest along -g_towards is G (brown), the one furthest along it S (orange).
    Returns tops (where the three wires end, G V S, seated), cable (unit vector from the plug towards its cable)
    and across (unit vector from the G contact to the S contact).
    """
    cable = -_unit(info['mating_direction'])
    face = np.asarray(info['cable_end_face_centre'], float)
    centres = sorted((np.asarray(c['centre'], float) for c in info['contacts']), key=lambda c: c @ np.asarray(g_towards, float))
    tops = [c + cable * ((face - c) @ cable - 1.0) for c in centres]          # the contacts stop 1 mm inside the cable-end face
    return dict(tops=np.array(tops), cable=cable, across=_unit(tops[2] - tops[0]), pitch=float(np.linalg.norm(tops[1] - tops[0])))


def plug_pose(plug_info, point, heading, across):
    """The pose that puts a loose plug on the end of a lead: its middle contact at `point`, the lead running into it
    along `heading`, wide along `across` (from the G conductor to the S conductor)."""
    c0, a0 = plug_info['cable'], plug_info['across']
    c1 = -_unit(heading)
    a1 = np.asarray(across, float)
    a1 = _unit(a1 - c1 * (a1 @ c1))
    R = np.column_stack([a1, c1, np.cross(a1, c1)]) @ np.column_stack([a0, c0, np.cross(a0, c0)]).T
    at = plug_info['tops'][1]
    w, V = np.linalg.eig(R)
    cos = np.clip((np.trace(R) - 1) / 2, -1.0, 1.0)
    t = [float(x) for x in np.asarray(point, float) - at]
    if cos > 1 - 1e-9:
        return t
    axis = np.real(V[:, np.argmin(np.abs(w - 1))])
    angle = np.degrees(np.arccos(cos))
    if np.linalg.norm(_about(_unit(axis), np.radians(angle)) - R) > 1e-6:      # the other way round the same axis
        angle = -angle
    return dict(t=t, r=[float(x) for x in _unit(axis)] + [float(angle)], at=[float(x) for x in at])


def loose_lead(centre, across, plug_info, pitch=1.02, fan_mm=10.0):
    """A lead lying loose along `centre` with its plug on the end.

    Returns (the three conductors G, V, S, the plug's pose). `across` is the direction from G to S at the start.
    """
    lines = ribbon(centre, across, pitch=pitch, n=3, end_pitch=plug_info['pitch'], fan_mm=fan_mm)
    return lines, plug_pose(plug_info, lines[1][-1], lines[1][-1] - lines[1][-2], lines[2][-1] - lines[0][-1])


def plugged_lead(centre, across, plug_info, pitch=1.02, fan_mm=30.0):
    """A lead along `centre` (its middle wire, ending on the plug's middle contact) into its plug, seated."""
    return ribbon(centre, across, pitch=pitch, n=3, end_pitch=plug_info['pitch'], fan_mm=fan_mm, end_across=plug_info['across'])


def cut_mark(ends, direction, size=2.2, overhang=2.0, edge_on=False):
    """A zigzag across the cut ends of one or more wires, to show that they carry on off the picture.

    ends: the end point of each wire, in order across the bundle. direction: which way the wires were heading.
    edge_on=True gives the same zigzag turned a quarter turn about the wires, through the middle of the bundle:
    drawn together (give one to each of two wires' routes) the pair reads as a break from any side.
    """
    ends = np.asarray(ends, float).reshape(-1, 3)
    d = _unit(direction)
    if len(ends) > 1 and np.linalg.norm(ends[-1] - ends[0]) > 1e-6:
        e = ends[-1] - ends[0]
    else:
        e = np.cross(d, [0.0, 1.0, 0.0]) if abs(d[1]) < 0.9 else np.cross(d, [1.0, 0.0, 0.0])
    span = np.linalg.norm(e) if len(ends) > 1 else 0.0
    e = _unit(e - d * (e @ d))
    middle = ends.mean(0)
    if edge_on:
        e = np.cross(d, e)
    half = span / 2 + overhang
    a, b = middle - e * half, middle + e * half
    teeth = max(4, int(round(2 * half / size)) * 2)
    return [a + (b - a) * (k / teeth) + d * (size / 2 if k % 2 else -size / 2) for k in range(teeth + 1)]


def load(path):
    """A kit's wire-paths.json: the centre line of every wire in the CAD, the plugs, and each servo's lead as a chain."""
    return json.load(open(path))
