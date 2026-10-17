"""The RCC's printing, written to decals.json (materials.json "decals" names it): the silkscreen of its three boards, the
radio modules' antenna and the FRONT engraved on L1.

    .venv.nosync/bin/python "RCC Build Instructions/silkscreen.py"      then   .venv.nosync/bin/python tools/build_model.py "RCC Build Instructions"

- NAUO23, the Nano I/O module: the MRA's module print (its decals.json, written by its silkscreen.py), carried over unchanged:
  the board is the same CAD model with every part in the same place, turned a quarter round about Y (docs/research/rcc/
  reuse_and_colours.md 1.3, cad_study.md 3.1). Only the four pictures' corners and directions change; white on navy, as there.
- NAUO26, the L adapter board, and NAUO30, the controller board: white boards with black print, from Lee's photos of the real
  boards (docs/research/rcc/lee_images_2026-10-15/). The controller's print is placed where TechBox's own Cadasio project has
  its silkscreen solids (TopSilkscreen~j5tP-*, docs/research/rcc/cadasio/raw/), with the letter sizes of the photo (the real
  board's lettering is about 1.4 x the CAD's); the adapter's, which no CAD has, is measured on its photo (calibrated on its
  headers, about 16.5 px/mm). The TechBox logo on both is traced from the kit's logo.webp (the same artwork, white on blue):
  icon and wordmark fitted to the Cadasio solids' boxes on the controller, to the photo on the adapter.
- NAUO10 / NAUO11, the radio modules: the gold antenna trace, which the CAD has as a plain black sheet (Lee, 16 Oct 2026,
  with a photo of the module).
- NAUO1, L1: "FRONT" at the front-left corner of its top face, as Lee drew it (L1_etching.png), in the palette's ink. The CAD
  has no pocket for it, so it is drawn here, in the stroke weight and letter height of the CAD's own engraved "L1" (which
  materials.json "move_engraving" turns the right way up: {"NAUO1": {"by": [-0.74, 0, -0.95], "turn": 180}}).

A decal is a flat picture laid on a face: `origin` is its top-left corner, `u` the way its "right" runs, `v` the way its "down"
runs (seated assembly mm), seen from the side v x u faces. Items are in picture mm: text (size = font size), rect, fill, circle,
poly (filled outlines, even-odd: a ring inside another is a hole; or `line` for an outline, `open` for a polyline) and arc (see
js/core.js, addDecal). The player draws them in the browser, so the model file holds no picture.
"""
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
MRA_DECALS = HERE.parent / 'MRA Build Instructions Prototype' / 'decals.json'
PRINT = '#000000'          # black print on the white boards (as the rulebook's breadboard legends)
INK = '#1e1616'            # the palette's "ink": engraved codes
BAND = '#1e1616'           # the dark band on a capacitor's top
PAD = '#a6a9aa'            # metal: the solder pads of the adapter's underside sockets
CAP = 0.716                # Arial's capital height as a share of the font size: a text item's `size` is the font size
r3 = lambda a: round(float(a), 3)


def frame(origin, u, v):
    """Assembly (x, z) on a level face -> picture (right, down) mm, for a decal with this corner and these directions."""
    ox, oz, (ux, _, uz), (vx, _, vz) = origin[0], origin[2], u, v
    return lambda x, z: [r3((x - ox) * ux + (z - oz) * uz), r3((x - ox) * vx + (z - oz) * vz)]


def text(s, at, h, rot=0, align='center', weight=400, width=None):
    """h = the height of the capitals (mm); width = squeezed to at most that long (the real boards' face is narrower than Arial)."""
    it = dict(text=s, at=at, size=r3(h / CAP))
    if rot:
        it['rot'] = rot
    if align != 'center':
        it['align'] = align
    it['weight'] = weight                                 # (always written: the format's default is bold)
    if width:
        it['width'] = width
    return it


def outline(at, x0, x1, z0, z1, line=0.2, margin=0.0):
    """A rectangle drawn round an assembly box (x0..x1, z0..z1), its line's middle `margin` outside the box."""
    (a, b), (c, d) = at(x0 - margin, z0 - margin), at(x1 + margin, z1 + margin)
    return dict(rect=[r3(min(a, c)), r3(min(b, d)), r3(abs(c - a)), r3(abs(d - b))], line=line)


def silk_box(at, x0, x1, z0, z1, line=0.2):
    """An outline whose outer edge is a Cadasio silkscreen solid's box."""
    return outline(at, x0, x1, z0, z1, line, margin=-line / 2)


def decal(name, origin, u, v, size, px_per_mm, colour, items):
    return dict(name=name, origin=[r3(c) for c in origin], u=u, v=v, size=[r3(size[0]), r3(size[1])], px_per_mm=px_per_mm, colour=colour, items=items)


# ---------------------------------------------------------------- the TechBox logo, traced from logo.webp

def trace(level, iso=0.5):
    """Closed outlines (marching squares, to a fraction of a pixel) of where `level` > iso: a list of (n, 2) arrays of (x, y) px."""
    f = np.pad(np.asarray(level, float), 1, constant_values=0.0)
    b = f > iso
    code = (b[:-1, :-1] * 1) | (b[:-1, 1:] * 2) | (b[1:, 1:] * 4) | (b[1:, :-1] * 8)      # corners TL, TR, BR, BL of each cell
    # the cell's sides: 0 top, 1 right, 2 bottom, 3 left; each piece of outline is listed in one direction round its shape
    table = {1: [(3, 0)], 2: [(0, 1)], 3: [(3, 1)], 4: [(1, 2)], 6: [(0, 2)], 7: [(3, 2)], 8: [(2, 3)], 9: [(2, 0)],
             11: [(2, 1)], 12: [(1, 3)], 13: [(1, 0)], 14: [(0, 3)]}
    side = lambda i, j, e: ('h', i, j) if e == 0 else ('v', i, j + 1) if e == 1 else ('h', i + 1, j) if e == 2 else ('v', i, j)

    def point(k):
        kind, i, j = k
        if kind == 'h':
            a, c = f[i, j], f[i, j + 1]
            return (j + (iso - a) / (c - a) - 1, i - 1)
        a, c = f[i, j], f[i + 1, j]
        return (j - 1, i + (iso - a) / (c - a) - 1)
    nxt = {}
    for i, j in zip(*np.nonzero((code > 0) & (code < 15))):
        c = int(code[i, j])
        if c in (5, 10):                                  # two opposite corners in: the middle of the cell decides
            joined = f[i:i + 2, j:j + 2].mean() > iso
            pieces = ([(3, 2), (1, 0)] if joined else [(3, 0), (1, 2)]) if c == 5 else ([(0, 3), (2, 1)] if joined else [(0, 1), (2, 3)])
        else:
            pieces = table[c]
        for a, e in pieces:
            nxt[side(i, j, a)] = side(i, j, e)
    loops, seen = [], set()
    for start in nxt:
        if start in seen:
            continue
        loop, k = [], start
        while k not in seen:
            seen.add(k)
            loop.append(point(k))
            k = nxt[k]
        loops.append(np.array(loop))
    return loops


def simplify(P, tol):
    """Douglas-Peucker on a closed outline."""
    def dp(A):
        keep = np.zeros(len(A), bool)
        keep[[0, -1]] = True
        stack = [(0, len(A) - 1)]
        while stack:
            s, e = stack.pop()
            if e <= s + 1:
                continue
            d, seg = A[e] - A[s], A[s + 1:e] - A[s]
            n = math.hypot(*d)
            dist = np.abs(seg[:, 0] * d[1] - seg[:, 1] * d[0]) / n if n > 1e-9 else np.hypot(seg[:, 0], seg[:, 1])
            m = int(np.argmax(dist))
            if dist[m] > tol:
                keep[s + 1 + m] = True
                stack += [(s, s + 1 + m), (s + 1 + m, e)]
        return A[keep]
    far = int(np.argmax(((P - P[0]) ** 2).sum(1)))
    return np.vstack([dp(P[:far + 1])[:-1], dp(np.vstack([P[far:], P[:1]]))[:-1]])


def area(P):
    return 0.5 * float(np.sum(P[:, 0] * np.roll(P[:, 1], -1) - np.roll(P[:, 0], -1) * P[:, 1]))


def inside(p, P):
    x, y = P[:, 0], P[:, 1]
    xn, yn = np.roll(x, -1), np.roll(y, -1)
    cross = (y > p[1]) != (yn > p[1])
    return bool(np.sum(cross & (p[0] < (xn - x) * (p[1] - y) / np.where(yn == y, 1e-12, yn - y) + x)) % 2)


def logo_shapes():
    """The logo's white artwork as shapes, each [outline, hole, ...] in logo pixels, left to right: the icon's (gear, bulb,
    two bars, base) and the seven letters of TECHBOX. Returns (icon shapes, letter shapes)."""
    im = np.asarray(Image.open(HERE / 'logo.webp').convert('RGBA'), float) / 255
    rings = [simplify(L, 0.8) for L in trace(im[:, :, 0] * im[:, :, 3])]     # white = red channel high (the blue has none)
    outer = [R for R in rings if area(R) < 0]             # (outlines run one way round, holes the other)
    holes = [R for R in rings if area(R) > 0]
    shapes = [[R] for R in sorted(outer, key=lambda R: R[:, 0].min())]
    for H in holes:
        home = min((s for s in shapes if inside(H[0], s[0])), key=lambda s: -area(s[0]))
        home.append(H)
    gaps = [(shapes[k + 1][0][:, 0].min() - max(r[:, 0].max() for s in shapes[:k + 1] for r in s), k) for k in range(len(shapes) - 1)]
    split = max(gaps)[1] + 1                              # the widest gap is between the icon and the wordmark
    icon, letters = shapes[:split], shapes[split:]
    if len(letters) != 7:
        raise SystemExit(f'logo.webp: expected the 7 letters of TECHBOX after the icon, found {len(letters)} shapes')
    return icon, letters


def box(shapes):
    P = np.vstack([r for s in shapes for r in s])
    return P.min(0), P.max(0)


def placed(shapes, s, t):
    """Shapes scaled by s and moved by t (picture mm), as poly items' rings."""
    return [[[[round(float(x * s + t[0]), 3), round(float(y * s + t[1]), 3)] for x, y in r] for r in sh] for sh in shapes]


def fit_box(shapes, lo, hi):
    """Scale (uniform, by height) and centre the shapes on the picture box lo..hi."""
    a, b = box(shapes)
    s = (hi[1] - lo[1]) / (b[1] - a[1])
    t = ((lo[0] + hi[0]) / 2 - s * (a[0] + b[0]) / 2, lo[1] - s * a[1])
    return s, t


def fit_letters(letters, targets):
    """One scale and offset that lays the letters on their target boxes (picture mm), least squares on their edges."""
    rows, rhs = [], []
    for sh, (lo, hi) in zip(letters, targets):
        a, b = box([sh])
        for px, pm in ((a[0], lo[0]), (b[0], hi[0])):
            rows.append([px, 1, 0]); rhs.append(pm)
        for py, pm in ((a[1], lo[1]), (b[1], hi[1])):
            rows.append([py, 0, 1]); rhs.append(pm)
    (s, tu, tv), *_ = np.linalg.lstsq(np.array(rows, float), np.array(rhs, float), rcond=None)
    worst = float(np.max(np.abs(np.array(rows) @ [s, tu, tv] - rhs)))
    return s, (tu, tv), worst


ICON, LETTERS = logo_shapes()
logo_note = []


def logo_items(shapes, s, t, colour=None):
    out = []
    for rings in placed(shapes, s, t):
        out.append(dict(poly=rings, **({'colour': colour} if colour else {})))
    return out


# ---------------------------------------------------------------- NAUO23: the I/O module, the MRA's print turned a quarter round
# p_RCC = R p_MRA + t (reuse_and_colours.md 1.3: the same board, checked on its 36 parts to 0.001 mm)
R = np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]], float)
T = np.array([864.282, 812.112, 1268.449])
shield = []
for d in json.load(open(MRA_DECALS))['NAUO82']:
    d = dict(d)
    d['origin'] = [r3(c) for c in R @ np.array(d['origin'], float) + T]
    d['u'] = [int(round(c)) for c in R @ np.array(d['u'], float)]
    d['v'] = [int(round(c)) for c in R @ np.array(d['v'], float)]
    shield.append(d)


# ---------------------------------------------------------------- NAUO26: the L adapter board (board top y 930.178)
# Seen as in Lee's photo: right = -z, down = +x (U1 above U2, U3 at the bottom, the short arm on the left).
A_TOP = 930.178 + 0.02
A_U, A_V = [0, 0, -1], [1, 0, 0]

# the long arm: U1 (LWh) and U2 (RWh), the two 3-pin servo headers (pins G V S at z 1318.43 / 1320.97 / 1323.51)
long_o = [692.67, A_TOP, 1327.5]
at = frame(long_o, A_U, A_V)
long_items = []
for name, row, x_label, x_svg, wheel, x_wheel in (('U1', 717.50, 716.32, 719.84, 'LWh', 717.20), ('U2', 730.20, 729.10, 732.63, 'RWh', 729.99)):
    long_items += [outline(at, row - 1.272, row + 1.268, 1317.163, 1324.783, margin=0.15),         # round the header's body
                   text(name, at(x_label, 1325.5), 0.73, weight=700),
                   text(wheel, at(x_wheel, 1316.08), 1.3, rot=-90, width=3.55 if wheel == 'LWh' else 3.7),   # reads up the board
                   *[text(c, at(x_svg, z), 1.67, width=w) for c, z, w in (('S', 1323.51, 1.2), ('V', 1320.97, 1.35), ('G', 1318.43, 1.25))]]


def pads(at, points, square):
    """The solder joints of the underside sockets, whose pins come up through the board (round, the first pin square)."""
    out = []
    for k, (x, z) in enumerate(points):
        u, v = at(x, z)
        out.append(dict(fill=[r3(u - 0.8), r3(v - 0.8), 1.6, 1.6], colour=PAD) if k == square else dict(circle=[u, v, 0.82], colour=PAD))
    return out


G3 = (1318.43, 1320.97, 1323.51)
long_items += pads(at, [(694.64, z) for z in G3], 0)                                   # onto the AREF row
long_items += pads(at, [(699.72, 1323.51), (702.26, 1323.51)], 1)                       # D13, D12
long_items += pads(at, [(x, 1323.51) for x in (707.34, 709.88, 712.42, 714.96)], 3)     # D11 - D8
long_items += pads(at, [(x, z) for x in (722.58, 725.12) for z in G3], 3)               # D6, D5
long_size = (1327.5 - 1314.76, 736.0 - 692.67)

# the short arm: U3 (the radio's socket), C1, the logo, and two more sockets' pads
short_o = [736.0, A_TOP, 1348.56]
at = frame(short_o, A_U, A_V)
short_items = [outline(at, 743.827, 748.827, 1315.693, 1326.263, margin=0.15), text('U3', at(743.09, 1316.19), 0.72, weight=700),
               text('C1', at(747.98, 1329.43), 0.79, weight=700)]
short_items += pads(at, [(740.36, z) for z in G3], 0) + pads(at, [(740.36, 1343.20), (740.36, 1345.74)], 1)
lo, hi = at(739.20, 1341.76), at(748.32, 1335.88)          # the icon on the photo (line art, bulb up the board)
s, t = fit_box(ICON, lo, hi)
short_items += logo_items(ICON, s, t)
logo_note.append(f'adapter icon {box(ICON)[1][0] * s - box(ICON)[0][0] * s:.2f} x {hi[1] - lo[1]:.2f} mm (photo {hi[0] - lo[0]:.2f} wide)')
short_size = (1348.56 - 1314.76, 750.08 - 736.0)


def capacitor(cx, cz, top, u, v, rot, band_angle):
    """The print on a 470 uF can's top (r 2.95 flat): the dark band over its negative side and 470 / 10V / RVT, the block
    moved 0.5 mm along its lines away from the band and 0.2 mm towards the letters' tops (as on both photos)."""
    h = 3.1
    o = [cx - h * (v[0] + u[0]), top + 0.02, cz - h * (v[2] + u[2])]
    at = frame(o, u, v)
    c = at(cx, cz)
    alpha = math.degrees(math.acos(1.45 / 2.95))           # the band's edge 1.45 mm from the middle
    read, up = (1, 0) if rot == 0 else (0, 1), (0, -1) if rot == 0 else (1, 0)     # reading direction and letter tops, picture
    items = [dict(arc=[c[0], c[1], 2.95, r3(band_angle - alpha), r3(band_angle + alpha)], colour=BAND)]
    for k, (s, w) in enumerate((('470', None), ('10V', 2.7), ('RVT', 2.8))):
        off = 0.2 + 1.5 * (1 - k)
        items.append(text(s, [r3(c[0] + 0.5 * read[0] + off * up[0]), r3(c[1] + 0.5 * read[1] + off * up[1])], 1.15, rot=rot, width=w))
    return decal('capacitor print', o, u, v, (6.2, 6.2), 48, PRINT, items)


adapter = [decal('silkscreen long arm', long_o, A_U, A_V, long_size, 30, PRINT, long_items),
           decal('silkscreen short arm', short_o, A_U, A_V, short_size, 40, PRINT, short_items),
           capacitor(743.657, 1331.006, 937.88, A_U, A_V, 90, 270)]          # band toward -x (the photo's top), lines read +x


# ---------------------------------------------------------------- NAUO30: the controller board (top face y 918.536)
# Seen as in Lee's photo: right = +z, down = -x (the joystick sockets at the top, USB at the bottom, TECHBOX on the right grip).
# Boxes are the Cadasio project's TopSilkscreen~j5tP solids (x, z in assembly mm); letter heights and lengths are the photo's.
C_TOP = 918.536 + 0.02
C_U, C_V = [0, 0, 1], [-1, 0, 0]
controller = []

for name, o, outlines, label in (
        ('silkscreen L-JS', [735.2, C_TOP, 1077.5], [(727.56, 734.60, 1078.06, 1091.63), (725.84, 727.54, 1078.06, 1091.63)],
         lambda at: text('L–JS', at(733.755, 1092.1), 1.1, align='left')),
        ('silkscreen R-JS', [735.2, C_TOP, 1145.5], [(727.43, 734.48, 1150.83, 1164.40), (725.71, 727.41, 1150.83, 1164.40)],
         lambda at: text('R–JS', at(733.63, 1146.2), 1.15, align='left'))):
    at = frame(o, C_U, C_V)
    controller.append(decal(name, o, C_U, C_V, (20.0, 10.0), 32, PRINT, [*[silk_box(at, *b) for b in outlines], label(at)]))

o = [734.6, C_TOP, 1103.4]                                # between the joystick holes: the Nano's sockets, the radio's, C1, USB
at = frame(o, C_U, C_V)
centre = [silk_box(at, 693.41, 732.23, 1103.91, 1106.67), silk_box(at, 693.41, 732.23, 1119.15, 1121.91),      # H2, H1
          text('H2', at(733.4, 1105.29), 1.1), text('H1', at(733.4, 1120.53), 1.1),
          text('NANO BOARD', at(722.2, 1114.15), 2.0, rot=90, align='left'),               # reads down the board, tops to +z
          text('CONTROLLER', at(722.2, 1110.85), 2.0, rot=90, align='left', width=18.5),
          silk_box(at, 709.26, 714.60, 1125.10, 1136.03), text('NRF24L01', at(707.55, 1130.57), 1.2, width=7.9),
          text('C1', at(705.55, 1133.2), 1.0, align='left', width=1.6),
          text('USB', at(692.0, 1112.9), 2.0, width=5.3)]
# C1's outline: two brackets round the can's base, open where its leads come out (+-z), the + corners (+z) cut off
for x_open, x_far in ((702.73, 705.38), (701.32, 698.66)):
    c = 1.0 if x_far > x_open else -1.0
    centre.append(dict(poly=[at(x_open, 1126.83), at(x_far, 1126.83), at(x_far, 1133.54 - 1.0), at(x_far - c * 1.0, 1133.54), at(x_open, 1133.54)],
                       line=0.2, open=True))
controller.append(decal('silkscreen centre', o, C_U, C_V, (1137.0 - 1103.4, 734.6 - 689.5), 24, PRINT, centre))

o = [689.2, C_TOP, 1154.5]                                # the logo on the right grip: icon and wordmark where the Cadasio has them
at = frame(o, C_U, C_V)
lo, hi = at(688.66, 1155.04), at(681.45, 1159.83)         # the icon's solids (gear 144, bulb 145, bars 146-148)
s, t = fit_box(ICON, lo, hi)
logo = logo_items(ICON, s, t)
logo_note.append(f'controller icon {(box(ICON)[1][0] - box(ICON)[0][0]) * s:.2f} x {hi[1] - lo[1]:.2f} mm (Cadasio {hi[0] - lo[0]:.2f} wide)')
CAD_LETTERS = [(1161.05, 1164.45, 681.86, 687.80), (1164.92, 1167.90, 681.86, 687.80), (1168.41, 1172.09, 681.73, 687.92),
               (1172.63, 1176.21, 681.86, 687.80), (1176.99, 1180.60, 681.86, 687.80), (1181.12, 1184.70, 681.73, 687.92),
               (1184.97, 1188.70, 681.86, 687.80)]                 # T E C H B O X (solids 149-155)
s, t, worst = fit_letters(LETTERS, [(at(x1, z0), at(x0, z1)) for z0, z1, x0, x1 in CAD_LETTERS])
logo += logo_items(LETTERS, s, t)
logo_note.append(f'TECHBOX laid on the Cadasio letters to {worst:.2f} mm')
controller.append(decal('logo', o, C_U, C_V, (1189.5 - 1154.5, 689.2 - 681.0), 40, PRINT, logo))
controller.append(capacitor(702.023, 1130.18, 926.237, C_U, C_V, 0, 180))   # band toward -z (the photo's left), lines read +z


# ---------------------------------------------------------------- NAUO1: L1's FRONT (top face y 909.227; flat front end x 774.466)
# Lee's drawing (L1_etching.png, 4.58 px/mm): FRONT 5.1 mm in from the left (-z) edge, on the line of the L1 at the right, letters
# up towards the front (+x). Drawn in the CAD "L1"'s weight: capitals 6.32 high, upright strokes 0.85, cross strokes 0.75.

def front(left, top, H=6.32, stem=0.85, bar=0.75):
    """FRONT as filled strokes (picture mm, y down from the capitals' top): the letter shapes and spacing of Lee's drawing, at
    the CAD code's height. Each stroke is an item of its own (strokes overlap, and even-odd would cut the overlaps out)."""
    out = []
    quad = lambda *p: out.append(dict(poly=[[r3(left + x), r3(top + y)] for x, y in p]))
    bar_ = lambda x0, y0, x1, y1: quad((x0, y0), (x1, y0), (x1, y1), (x0, y1))

    def slant(x0, y0, x1, y1, w):                          # a stroke w wide, cut level at both ends: top-left corner (x0, y0), bottom-right (x1, y1)
        dx = w
        for _ in range(4):
            dx = w / math.cos(math.atan2(x1 - x0 - dx, y1 - y0))
        quad((x0, y0), (x0 + dx, y0), (x1, y1), (x1 - dx, y1))

    def ring(cx, cy, rx, ry, w, h, a0=0, a1=360, n=72):    # an elliptic band, outer radii rx, ry; w thick at the sides, h at top and bottom
        angles = np.radians(np.linspace(a0, a1, n + 1))
        o = [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in angles]
        i = [(cx + (rx - w) * math.cos(a), cy + (ry - h) * math.sin(a)) for a in angles]
        if a1 - a0 >= 360:
            out.append(dict(poly=[[[r3(left + x), r3(top + y)] for x, y in o[:-1]], [[r3(left + x), r3(top + y)] for x, y in i[:-1]]]))
        else:
            quad(*o, *reversed(i))
    # F (3.78 wide)
    bar_(0, 0, stem, H); bar_(0, 0, 3.78, bar); bar_(0, 0.516 * H - bar / 2, 3.36, 0.516 * H + bar / 2)
    # R (4.63 wide): stem, bowl (bars to x 2.2, a half round to x 3.94), leg from the bowl's foot to the corner
    x, yb, xb = 5.02, 3.45, 2.2
    bar_(x, 0, x + stem, H); bar_(x, 0, x + xb + 0.02, bar); bar_(x, yb - bar, x + xb + 0.02, yb)
    ring(x + xb, yb / 2, yb / 2, yb / 2, 0.82, bar, -90, 90, 36)
    slant(x + 1.75, yb - bar, x + 4.63, H, 0.85)
    # O (6.29 wide, overshooting the line by 0.14 above and below)
    ring(10.25 + 3.145, H / 2, 3.145, H / 2 + 0.14, stem, bar + 0.04)
    # N (5.04 wide)
    x, w = 17.78, 5.04
    bar_(x, 0, x + stem, H); bar_(x + w - stem, 0, x + w, H); slant(x, 0, x + w, H, 0.9)
    # T (5.04 wide)
    x = 23.63
    bar_(x, 0, x + w, bar); bar_(x + (w - stem) / 2, 0, x + (w + stem) / 2, H)
    return out


L1_TOP, L1_FRONT, L1_LEFT = 909.227, 774.466, 1273.481
code_top = 769.434 - 0.74                                 # the CAD's L1, turned and moved by move_engraving: x 762.34 - 768.69
o = [code_top + 0.4, L1_TOP + 0.02, L1_LEFT + 5.1 - 0.4]
l1 = [decal('engraving FRONT', o, [0, 0, 1], [-1, 0, 0], (29.5, 7.2), 40, INK, front(0.4, 0.4))]


# ---------------------------------------------------------------- NAUO10 / NAUO11, the radio modules: the gold antenna trace
# The CAD has the antenna as a plain 0.1 mm black sheet on the board's top (own y 1.2 - 1.3, at the end away from the header).
# The trace is measured on Lee's photo of the module (lee_images 2026-10-16, about 16.4 px/mm): picture x runs along the board
# from its antenna end (own z -14.5), picture y across it from the crystal's edge (own x 7.65). Both modules lie face up,
# turned the same way: own (x, y, z) -> assembly (t_x - z, t_y + y, t_z + x).
GOLD = '#c8a25c'           # the trace's gold, read off the photo
TRACE = 0.5                # mm wide
xl, xr = 0.75, 4.65
rows = [4.48, 5.70, 6.85, 8.0, 9.15, 10.3]
meander = [[xl, 0.45]]
for k, y in enumerate(rows):                              # down the left edge, then back and forth, the turns alternating right / left
    a, b = (xl, xr) if k % 2 == 0 else (xr, xl)
    meander += [[a, y], [b, y]]
meander += [[xl, 11.5], [8.6, 11.5]]                      # ... and along the bottom to the matching parts
antenna_items = [dict(poly=meander, line=TRACE, open=True), dict(poly=[[6.6, 4.15], [6.6, 11.5]], line=TRACE, open=True)]
radios = {}
for rid, (tx, ty, tz) in (('NAUO10', (758.057, 941.378, 1323.433)), ('NAUO11', (723.699, 929.736, 1132.903))):
    radios[rid] = [decal('antenna', [tx + 14.5, ty + 1.3 + 0.02, tz + 7.65], [-1, 0, 0], [0, 0, -1], (9.5, 12.0), 40, GOLD, antenna_items)]


# ---------------------------------------------------------------- write
out = {'_about': 'Printing on parts, drawn by the player (js/core.js); materials.json "decals" names this file. Written by silkscreen.py: edit that, not this.',
       'NAUO1': l1, 'NAUO23': shield, 'NAUO26': adapter, 'NAUO30': controller, **radios}
with open(HERE / 'decals.json', 'w') as f:                # (one item a line)
    keys = [k for k in out if k != '_about']
    f.write('{\n "_about": ' + json.dumps(out['_about']) + ',\n')
    for n, key in enumerate(keys):
        f.write(f' "{key}": [\n')
        for k, d in enumerate(out[key]):
            head = {kk: vv for kk, vv in d.items() if kk != 'items'}
            f.write('  ' + json.dumps(head)[:-1] + ', "items": [\n' + ',\n'.join('   ' + json.dumps(it) for it in d['items']) + ']}' + (',' if k < len(out[key]) - 1 else '') + '\n')
        f.write(' ]' + (',' if n < len(keys) - 1 else '') + '\n')
    f.write('}\n')
back = json.load(open(HERE / 'decals.json'))              # (it must read back)
print('decals.json: ' + '; '.join(f'{k} ({", ".join(d["name"] + " " + str(len(d["items"])) for d in back[k])})' for k in keys))
print('logo: ' + '; '.join(logo_note))
