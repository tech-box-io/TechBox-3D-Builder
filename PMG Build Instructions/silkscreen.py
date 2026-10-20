"""The PMG's printing, written to decals.json (materials.json "decals" names it).

    .venv.nosync/bin/python "PMG Build Instructions/silkscreen.py"      then   .venv.nosync/bin/python tools/build_model.py "PMG Build Instructions"

- NAUO78, the Nano I/O module on the back panel H4: the MRA's module print (its decals.json, written by its silkscreen.py), carried
  over unchanged, as the RCC's: the board is the same CAD model with every part in the same place, so the one rigid move that takes
  the MRA's module onto the PMG's (cad-geometry.json "mra_module_to_pmg", written by make_source.py: measured on the board mesh both
  files share, with the module turned the published way up) takes its print there too. Only each picture's corner and directions
  change; white on navy, as on the MRA and the RCC. (This assumes the PMG kit's module is the board in Lee's MRA photos, as the
  RCC's was confirmed to be, 16 Oct 2026.)

Lee's first round on the PMG (19 Oct 2026, photos in docs/research/pmg/lee_images_2026-10-19/; measurements in
docs/research/pmg/silkscreen.md):
- NAUO76, NAUO83, NAUO84, NAUO85, the push buttons (black, yellow, white, blue): VCC, OUT and GND by the 3-pin header on the cap side
  and the outline round the header (photo 2, TechBox's Cadasio card), white on navy. The four are one CAD part placed four ways
  (tilted about 7 degrees in the case): the print is laid out once in the board's own frame and placed by each button's board node.
- NAUO79, the TM1637 4-digit display: the front (U1, J1 and the outline round the header, "4-Digit Display  V1.2"; photo 4) and the
  back (HW-069, CLK DIO VCC GND by the pins, C1 C2 R1 R2 C3 C4 U2 with their outlines, the display's twelve solder joints with
  "12" and "1"; photo 5), white on blue, with the plated rims of the four corner holes and the small parts drawn flat (the CAD has
  neither). Measured on the photos, calibrated on the corner holes (16.2 px/mm), against the CAD board (42 x 24 mm).
- NAUO81, the dot matrix display: the board's rear (photo 7): each of the four 8 x 8 modules' VCC GND DIN CS CLK at its input end
  and VCC GND DOUT CS CLK at its output end, "<- OUT" and "IN <-" along the lower edge, MH on the input module, the pins' plated
  rims and the links between the modules. And the faces of its four LED blocks (1088AS): black, with 64 round white dots in an
  8 x 8 grid, measured on the CAD's dot solids (3.0 mm across, 3.98 mm apart); materials.json's ^1088AS$ rule colours the whole
  face black underneath (the CAD's dots are coarse polygons once the model is simplified: Lee's "FAR from circles").
Every part is placed by its own node in pmg-guide.glb (the kit's source, read here for its node matrices only), so the print
follows the CAD if make_source.py places a part anew. The player draws text in Arial; the boards' silkscreen font is narrower,
so a label is given its photo's capital height and squeezed to its photo's length (`width`).

A decal is a flat picture laid on a face: `origin` is its top-left corner, `u` the way its "right" runs, `v` the way its "down"
runs (seated assembly mm), seen from the side v x u faces. Items are in picture mm (see js/core.js, addDecal).
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
from glbio import read_glb, node_matrix  # noqa: E402

MRA_DECALS = HERE.parent / 'MRA Build Instructions Prototype' / 'decals.json'
SPEC = json.load(open(HERE / 'materials.json'))
TO_MM = float(SPEC.get('source_scale_to_mm', 1.0))
M = np.array(json.load(open(HERE / 'cad-geometry.json'))['mra_module_to_pmg'], float)
R, T = M[:3, :3], M[:3, 3]
r3 = lambda a: round(float(a), 3)

INK = '#f2f2f2'            # white silkscreen (as the MRA's module)
PAD = '#a6a9aa'            # tinned copper: plated hole rims, solder joints, the small parts' ends (the palette's steel)
CAP = 0.716                # Arial's capital height as a share of the font size: a text item's `size` is the font size

module = []
for d in json.load(open(MRA_DECALS))['NAUO82']:
    d = dict(d)
    d['origin'] = [r3(c) for c in R @ np.array(d['origin'], float) + T]
    d['u'] = [int(round(c)) for c in R @ np.array(d['u'], float)]
    d['v'] = [int(round(c)) for c in R @ np.array(d['v'], float)]
    module.append(d)


# ---------------------------------------------------------------- the parts' own frames, from the source's nodes

def part_nodes():
    """{instance name: [(mesh name, world matrix in mm, local box min, max in mm), ...]} for the top-level parts in the source."""
    doc, _ = read_glb(HERE / SPEC['source'])
    nodes, out = doc['nodes'], {}

    def walk(i, W, inst):
        n = nodes[i]
        W = W @ node_matrix(n)
        if inst is None and n.get('name', '').startswith('NAUO'):
            inst = n['name']
            out.setdefault(inst, [])
        if inst is not None and 'mesh' in n:
            mesh = doc['meshes'][n['mesh']]
            a = doc['accessors'][mesh['primitives'][0]['attributes']['POSITION']]
            Wmm = W.copy()
            Wmm[:3, 3] *= TO_MM
            out[inst].append((mesh.get('name', ''), Wmm, np.array(a['min']) * TO_MM, np.array(a['max']) * TO_MM))
        for c in n.get('children', []):
            walk(c, W, inst)
    for r in doc['scenes'][doc.get('scene', 0)]['nodes']:
        walk(r, np.eye(4), None)
    return out


NODES = part_nodes()


def frame_of(inst, mesh_prefix, box=None):
    """The world matrices (mm) of the meshes of `inst` whose name starts with mesh_prefix, checked against their expected own box."""
    found = [(W, lo, hi) for name, W, lo, hi in NODES.get(inst, []) if name.startswith(mesh_prefix)]
    if not found:
        raise SystemExit(f'silkscreen.py: no mesh "{mesh_prefix}..." in {inst} ({SPEC["source"]})')
    for W, lo, hi in found:
        if box is not None and (np.abs(lo - box[0]).max() > 0.02 or np.abs(hi - box[1]).max() > 0.02):
            raise SystemExit(f'silkscreen.py: {inst} {mesh_prefix}: own box {lo.round(3)} - {hi.round(3)}, expected {box}: the CAD has changed, measure again')
    return [W for W, _, _ in found]


def vec(a):
    """A direction for decals.json: whole numbers when it lies along an axis."""
    a = np.asarray(a, float)
    a = a / np.linalg.norm(a)
    return [int(round(c)) if abs(c - round(c)) < 5e-6 else round(float(c), 5) for c in a]


def decal(name, W, origin, u, v, size, px_per_mm, colour, items):
    """A decal laid out in a part's own frame (origin, u, v in the mesh's own mm), placed in the assembly by its node W."""
    Rw, tw = W[:3, :3], W[:3, 3]
    o = Rw @ np.asarray(origin, float) + tw
    return dict(name=name, origin=[r3(c) for c in o], u=vec(Rw @ np.asarray(u, float)), v=vec(Rw @ np.asarray(v, float)),
                size=[r3(size[0]), r3(size[1])], px_per_mm=px_per_mm, colour=colour, items=items)


def text(s, at, h, rot=0, align='center', weight=700, width=None):
    """h = the capitals' height (mm); width = the photo's length of the label: Arial is squeezed to it where it is longer."""
    it = dict(text=s, at=at, size=r3(h / CAP))
    if rot:
        it['rot'] = rot
    if align != 'center':
        it['align'] = align
    it['weight'] = weight
    if width:
        it['width'] = r3(width)
    return it


def outline(at, a0, a1, b0, b1, line=0.15, margin=0.0):
    """A rectangle round the box a0..a1, b0..b1 (the face's own two axes, mm), its line's middle `margin` outside it."""
    (p, q), (r, s) = at(a0 - margin, b0 - margin), at(a1 + margin, b1 + margin)
    return dict(rect=[r3(min(p, r)), r3(min(q, s)), r3(abs(r - p)), r3(abs(s - q))], line=line)


def ring(at, a, b, r_in, r_out, square=False, colour=PAD):
    """A plated rim round a hole (or a pad): the band r_in..r_out; square = the first pin's square pad."""
    u, v = at(a, b)
    if square:
        h = (r_in + r_out) / 2
        return dict(rect=[r3(u - h), r3(v - h), r3(2 * h), r3(2 * h)], line=r3(r_out - r_in), colour=colour)
    return dict(circle=[u, v, r3((r_in + r_out) / 2)], line=r3(r_out - r_in), colour=colour)


# ---------------------------------------------------------------- NAUO76, NAUO83, NAUO84, NAUO85: the push buttons
# The board's own frame (mm): x across (-6.5 .. 6.5), z along (-11 .. 11, the header's end +z), y up from the cap side (the face,
# y 0; the board -1.2 .. 0). The header's three pins at x -2.5 (VCC), 0 (OUT), +2.5 (GND); their black spacer z 7.5 .. 10, the
# switch's body ends at z 4.0 (its legs 4.7), the cap at 4.54. Seen as in the photo, cap side up, header at the bottom: right = +x,
# down = +z, so VCC is on the left. Photo 2 (38 px/mm across the pins): OUT 1.05 - 1.1 mm high, 0.3 mm above the spacer; VCC and
# GND reading up the board (tops to the left), 1.3 mm high, 3.3 mm long, from about 1 mm above the spacer to its lower end,
# centred between the board's edge and the spacer; a thin outline round the header's footprint.
BUTTONS = [('NAUO76', 'black'), ('NAUO83', 'yellow'), ('NAUO84', 'white'), ('NAUO85', 'blue')]
BOARD_BOX = ([-6.5, -1.2, -11.0], [6.5, 0.0, 11.0])
B_X0, B_Z0 = -6.5, 4.8                                    # the picture's corner: the band of the board below the switch
b_at = lambda x, z: [r3(x - B_X0), r3(z - B_Z0)]
button_items = [
    text('OUT', b_at(0.0, 6.65), 1.1, width=3.4),
    text('VCC', b_at(-5.15, 8.3), 1.3, rot=-90, width=3.3),
    text('GND', b_at(5.15, 8.3), 1.3, rot=-90, width=3.3),
    outline(b_at, -3.75, 3.75, 7.5, 10.0, line=0.13, margin=0.15),
]
buttons = {}
for inst, colour in BUTTONS:
    W, = frame_of(inst, 'Board^Big Button Module', BOARD_BOX)
    buttons[inst] = [decal('silkscreen', W, [B_X0, 0.02, B_Z0], [1, 0, 0], [0, 0, 1], (13.0, 11.0 - B_Z0), 40, INK, button_items)]


# ---------------------------------------------------------------- NAUO79: the TM1637 4-digit display
# Its own frame (mm): x along the board (-21 .. 21; the pins at x 18.8, bent out to +x), y across (-12 .. 12), z out of the front
# (the board 0 .. 1.3; the digit block on the front, x -14 .. 16, y -7 .. 7; the TM1637 on the back, x -16.7 .. -8.7,
# y -6.5 .. 6.5). Corner holes r 1.1 at (+-19, +-10). Pins: CLK y 3.5, DIO 1.1, VCC -1.3, GND -3.7 (cad-geometry.json caps).
# Photos 4 (front) and 5 (back), 16.2 and 16.3 px/mm on the corner holes, which match the CAD's (38 x 20 mm apart). Seen from the
# front, the pins on the right: right = +x, down = -y; from the back, the pins on the left: right = -x, down = -y.
DISPLAY_BOX = ([-21.0, -12.0, -2.6], [26.5, 12.0, 8.6])
W_DISPLAY, = frame_of('NAUO79', 'Display TM1637', DISPLAY_BOX)
HOLES = [(-19.0, -10.0), (-19.0, 10.0), (19.0, -10.0), (19.0, 10.0)]
PINS = [('CLK', 3.5, 3.13), ('DIO', 1.1, 2.9), ('VCC', -1.3, 3.07), ('GND', -3.7, 3.07)]     # name, y, the label's length on photo 5
PIN_X = 18.8

f_at = lambda x, y: [r3(x + 21.0), r3(12.0 - y)]
front_items = [ring(f_at, x, y, 1.1, 1.6) for x, y in HOLES] + [
    text('U1', f_at(1.42, 8.56), 1.18, width=1.7),                               # above the digit block
    text('J1', f_at(18.55, 6.45), 1.06, width=1.5),                              # above the header
    outline(f_at, PIN_X - 1.35, PIN_X + 1.35, -3.7 - 1.35, 3.5 + 1.35, line=0.15),   # round the header's footprint
    text('4-Digit Display  V1.2', f_at(2.2, -9.67), 1.55, weight=400, width=17.06),  # under the digit block
]
display = [decal('silkscreen front', W_DISPLAY, [-21.0, 12.0, 1.32], [1, 0, 0], [0, -1, 0], (42.0, 24.0), 32, INK, front_items)]

k_at = lambda x, y: [r3(21.0 - x), r3(12.0 - y)]
DY = -0.28            # the parts between the digit block's two rows of joints: placed from the joints (the block's middle, y 0),
#                       which sit 0.28 mm off the corner holes' middle on the real board (photo 5)
back_items = [ring(k_at, x, y, 1.1, 1.6) for x, y in HOLES]
back_items += [ring(k_at, PIN_X, y, 0.5, 1.0, square=(name == 'GND')) for name, y, _ in PINS]          # the header's pins
back_items += [text(name, k_at(PIN_X - 1.67, y), 1.24, align='left', width=w) for name, y, w in PINS]
back_items += [text('HW-069', k_at(16.59, 10.25), 1.2, align='left', width=5.9)]
# the digit block's 12 pins, soldered on the back (not in the CAD): two rows 10.16 apart, 2.54 pitch, about its middle (x 1);
# pin 1 (square) at the chip's end of the lower row, pin 12 above it
for k in range(6):
    x = 1.0 + (k - 2.5) * 2.54
    for y in (-5.08, 5.08):
        u, v = k_at(x, y)
        back_items.append(dict(fill=[r3(u - 0.72), r3(v - 0.72), 1.44, 1.44], colour=PAD) if (k == 0 and y < 0) else dict(circle=[u, v, 0.72], colour=PAD))
back_items += [text('12', k_at(-5.16, 3.61 + DY), 0.9, width=1.41), text('1', k_at(-5.07, -2.96 + DY), 1.0)]


def smd(at, a0, a1, b0, b1, body, marking=None, rot=0):
    """A small two-ended part lying in its outline: tinned ends, its body between (a0..a1 along it, b0..b1 across)."""
    end = 0.45
    (p, q), (r, s) = at(a0, b0), at(a1, b1)
    u0, u1, v0, v1 = min(p, r), max(p, r), min(q, s), max(q, s)
    out = [dict(fill=[r3(u0), r3(v0), r3(u1 - u0), r3(v1 - v0)], colour=PAD),
           dict(fill=[r3(u0 + end), r3(v0), r3(u1 - u0 - 2 * end), r3(v1 - v0)], colour=body)]
    if marking:
        out.append(dict(text=marking, at=[r3((u0 + u1) / 2), r3((v0 + v1) / 2)], size=r3(0.6 / CAP), weight=400, colour=INK, **({'rot': rot} if rot else {})))
    return out


RES, CERAMIC = '#1b1b1b', '#c39a6b'                       # a resistor's black body, a capacitor's tan (photo 5)
for name, (x0, x1, y0, y1), (lx, ly, lw), body, mark in (
        ('R2', (1.48, 4.70, 0.23, 1.95), (5.72, 1.21, 1.96), RES, ('103', 0)),
        ('C4', (1.48, 4.70, -1.73, -0.05), (5.72, -1.27, 2.27), CERAMIC, None),
        ('R1', (-3.11, 0.14, 0.23, 1.95), (-4.06, 1.49, 1.65), RES, ('103', 180)),
        ('C3', (-3.11, 0.14, -1.73, -0.05), (-4.12, -1.02, 2.14), CERAMIC, None)):
    y0, y1, ly = y0 + DY, y1 + DY, ly + DY
    back_items.append(outline(k_at, x0, x1, y0, y1, line=0.15))
    back_items += smd(k_at, x0 + 0.35, x1 - 0.35, y0 + 0.33, y1 - 0.33, body, *(mark or (None,)))
    back_items.append(text(name, k_at(lx, ly), 1.25, rot=-90, width=lw))       # reading up the board, as printed
UP = 0.3              # C1 and C2 (photo 5) lifted 0.3 mm clear of the CAD's chip, which is 0.3 mm longer than the real one
for name, (x0, x1, y0, y1), (lx, ly) in (('C1', (-17.26, -14.04, 8.27, 9.71), (-12.79, 8.76)),
                                         ('C2', (-17.26, -14.04, 6.34, 7.78), (-12.82, 6.98))):
    back_items.append(outline(k_at, x0, x1, y0 + UP, y1 + UP, line=0.15))
    back_items += smd(k_at, x0 + 0.35, x1 - 0.35, y0 + UP + 0.25, y1 + UP - 0.25, CERAMIC)
    back_items.append(text(name, k_at(lx, ly + UP), 1.13, width=1.5))
back_items += [text('U2', k_at(-13.03, -7.86), 1.07, width=1.7),                   # under the chip
               dict(circle=[*k_at(-9.0, 6.95), 0.3], line=0.13)]                     # its pin-1 mark, by the corner
display.append(decal('silkscreen back', W_DISPLAY, [21.0, 12.0, -0.02], [-1, 0, 0], [0, -1, 0], (42.0, 24.0), 32, INK, back_items))


# ---------------------------------------------------------------- NAUO81: the dot matrix display
# The LED blocks' own frame (mm): the face at y 0 (x 0 .. 31.8, z -31.8 .. 0; the black mask y -0.1 .. 0). The CAD's dots are
# discs 3.0 across at x 1.9875 + 3.98 i, z -(1.9875 + 3.98 j) (56 measured; the eighth column, x 1.9875, is welded into the body
# in this export and follows the same grid).
LED_BOX = ([0.0, -10.5, -31.8], [31.81, 0.0, 0.0])
FACE, DOT = '#1e1616', '#ffffff'                          # the palette's led_face and led_white
led_items = [dict(fill=[0, 0, 31.8, 31.8], colour=FACE)]
led_items += [dict(circle=[r3(1.9875 + 3.98 * i), r3(31.8 - (1.9875 + 3.98 * j)), 1.5], colour=DOT) for j in range(8) for i in range(8)]
matrix = [decal('LED face', W, [0.0, 0.02, -31.8], [1, 0, 0], [0, 0, 1], (31.8, 31.8), 24, DOT, led_items)
          for W in frame_of('NAUO81', '1088AS', LED_BOX)]

# The board's own frame (mm): x along it (-16.1875 .. 113.3125; the input header at the low end), y across (-16 .. 16), z out of
# the back (the board 0 .. 1.5, the LED blocks in front of it, z < 0). Four modules, 32.375 long, centres x 32.375 k; on each,
# holes 1.0 across: the LED block's pins at x -9.188 + 2.54 i, y +-12 (pin 1, square, at x 8.593, y -12); the input pins
# (VCC GND DIN CS CLK) at x -14.2875, y -5.76 -3.22 -0.68 1.86 4.4; the output pins (VCC GND DOUT CS CLK) at x 14.6875,
# y -5.56 -3.02 -0.48 2.06 4.6. Seen as in photo 7 (8.2 px/mm), the back up, the input header on the right: right = -x, down = +y.
PCB_BOX = ([-16.1875, -16.0, 0.0], [113.3125, 16.0, 1.5])
W_PCB, = frame_of('NAUO81', 'PCB', PCB_BOX)
X_HI = 113.3125
m_at = lambda x, y: [r3(X_HI - x), r3(y + 16.0)]
IN_X, OUT_X = -14.2875, 14.6875
IN_Y, OUT_Y = [-5.76, -3.22, -0.68, 1.86, 4.4], [-5.56, -3.02, -0.48, 2.06, 4.6]
IN_NAMES = [('VCC', 2.42), ('GND', 2.33), ('DIN', 2.27), ('CS', 1.5), ('CLK', 2.36)]       # the label's length on photo 7
OUT_NAMES = [('VCC', 2.42), ('GND', 2.33), ('DOUT', 3.12), ('CS', 1.5), ('CLK', 2.36)]
GAP = 1.5             # from a pin's middle to its label's near end


def arrow(at, tail, tip, y, shaft=0.32, head=1.2, half=0.68):
    """A printed arrow along the board (x from tail to tip, at y): a shaft and a filled head."""
    s = 1 if tip > tail else -1
    neck = tip - s * head
    return [dict(poly=[at(tail, y - shaft / 2), at(neck, y - shaft / 2), at(neck, y + shaft / 2), at(tail, y + shaft / 2)]),
            dict(poly=[at(tip, y), at(neck, y - half), at(neck, y + half)])]


rear = []
for k in range(4):
    c = 32.375 * k
    rear += [ring(m_at, c - 9.188 + 2.54 * i, y, 0.5, 0.9, square=(i == 7 and y < 0)) for i in range(8) for y in (-12.0, 12.0)]
    rear += [ring(m_at, c + IN_X, y, 0.5, 0.9) for y in IN_Y] + [ring(m_at, c + OUT_X, y, 0.5, 0.9) for y in OUT_Y]
    rear += [text(s, m_at(c + IN_X + GAP, y), 1.06, align='right', width=w) for (s, w), y in zip(IN_NAMES, IN_Y)]
    rear += [text(s, m_at(c + OUT_X - GAP, y), 1.06, align='left', width=w) for (s, w), y in zip(OUT_NAMES, OUT_Y)]
    rear += [text('OUT', m_at(c + 8.7, 14.42), 1.52, width=4.0), text('IN', m_at(c - 7.55, 14.42), 1.52, width=2.43)]
    rear += arrow(m_at, c + 11.3, c + 15.55, 14.42) + arrow(m_at, c - 13.5, c - 9.24, 14.42)
    if k < 3:                                             # the links from this module's output to the next one's input
        rear += [dict(poly=[m_at(c + OUT_X, a), m_at(c + 32.375 + IN_X, b)], line=0.45, open=True, colour=PAD) for a, b in zip(OUT_Y, IN_Y)]
rear.append(text('MH', m_at(-0.44, -14.5), 1.52, width=3.8))                          # on the input module only
matrix.append(decal('silkscreen back', W_PCB, [X_HI, -16.0, 1.52], [-1, 0, 0], [0, 1, 0], (129.5, 32.0), 24, INK, rear))


# ---------------------------------------------------------------- write
out = {'_about': 'Printing on parts, drawn by the player (js/core.js); materials.json "decals" names this file. Written by silkscreen.py: edit that, not this.',
       'NAUO78': module, **buttons, 'NAUO79': display, 'NAUO81': matrix}
with open(HERE / 'decals.json', 'w') as f:                # (one item a line, as the MRA's and RCC's)
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
for key in keys:
    for d in back[key]:
        print(f"{key} {d['name']}: origin {d['origin']} u {d['u']} v {d['v']} size {d['size']} ({len(d['items'])} items)")
