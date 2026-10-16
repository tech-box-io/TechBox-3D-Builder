"""The I/O module's silkscreen (its printed pin names), written to decals.json for the part NAUO82 (materials.json "decals" names it).

    python "MRA Build Instructions Prototype/silkscreen.py"      then   python tools/build_model.py "MRA Build Instructions Prototype"

Lee asked for it on 14 Oct 2026 so that the pins can be told apart, with three photos of the real board
(docs/research/mra/lee_images_2026-10-14b/11.jpg - 13.jpg). Every label is placed from the CAD: the pin and hole positions
measured in docs/research/mra/cad_pins.md (and from the board's mesh for the edge holes, the LED, the reset button, the
capacitor and the regulator). The player draws the decals in the browser (js/core.js), so the model file holds no picture.

A decal is a flat picture laid on a face: `origin` is its top-left corner, `u` the way its "right" runs, `v` the way its
"down" runs (all seated mm), seen from the side v x u faces. Items are in picture mm: text (size = font size), rect, fill, circle.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INK = '#f2f2f2'                                         # white silkscreen

# The board (cad_pins.md, section 1): x 43.36 to 96.70, z 115.96 to 173.16, top face y = 106.43, underside 104.78.
X0, X1, Z0, Z1, TOP, UNDER = 43.36, 96.70, 115.96, 173.16, 106.43, 104.78

# ---- the top, read as in the photo: the digital rows along the top edge (low x), the USB end on the left (high z)
top_at = lambda x, z: [round(Z1 - z, 3), round(x - X0, 3)]


def text(s, x, z, size=1.25, rot=0, align='center', at=top_at):
    return dict(text=s, at=at(x, z), size=size, **({'rot': rot} if rot else {}), **({'align': align} if align != 'center' else {}))


items = []
# digital side: columns G V S at x 50.085 / 52.574 / 55.064; four blocks of four rows; row names between the headers and the Nano
G, V, S = 50.085, 52.574, 55.064
DIGITAL = [('AREF', 169.64), ('GND', 167.10), ('13', 164.56), ('12', 162.02), ('11', 157.09), ('10', 154.55), ('9', 152.01), ('8', 149.47),
           ('7', 144.54), ('6', 142.00), ('5', 139.46), ('4', 136.92), ('3', 131.99), ('2', 129.45), ('1', 126.91), ('0', 124.37)]
for name, z in DIGITAL:
    if len(name) > 2:                                   # AREF and GND run up the board, as printed
        items.append(text(name, 58.15, z, size=0.98, rot=-90))   # (the real board's AREF runs under the socket; kept clear of it here)
    else:
        items.append(text(name, 58.3, z, size=1.35))
items += [text('TX', 59.9, 126.91, size=1.05), text('RX', 59.9, 124.37, size=1.05)]
for z in (171.9, 159.55, 147.0, 134.46):               # G V S beside each block, on its USB side
    items += [text('G', G, z), text('V', V, z), text('S', S, z)]

# analogue side: columns G V S at x 83.126 / 85.615 / 88.105, rows A0 (z 141.48) to A7 (z 123.70); names outside the S column
AG, AV, AS = 83.126, 85.615, 88.105
items += [text('G', AG, 144.0), text('V', AV, 144.0), text('S', AS, 144.0)]
for k in range(8):
    items.append(text(f'A{k}', 90.65, 141.48 - 2.54 * k, size=1.2))

# the two 4-pin headers and the 2 x 3 block at the far end (not used by the kit)
for name, z in zip(('RX', 'TX', '5V', 'GND'), (126.45, 123.91, 121.37, 118.83)):
    items.append(text(name, 67.05, z, size=1.0))
for name, z in zip(('SCL', 'SDA', '5V', 'GND'), (126.41, 123.87, 121.33, 118.79)):
    items.append(text(name, 71.68, z, size=0.95))
items += [text('3V3', 73.83, 119.2, size=1.05, align='left'), text('GND', 76.33, 119.2, size=1.05, align='left')]

# the power LED and the reset button
items += [text('POWER', 85.65, 119.26, size=1.05), text('RESET', 90.95, 159.58, size=1.05)]

# outlines round the rows of plain holes along the two long edges (holes found in the board's mesh)
EDGE_DIGITAL, EDGE_ANALOG = 45.8, 94.0
digital_holes = [121.0, 123.5, 126.0, 128.75, 131.25, 133.75, 136.25, 138.75, 143.0, 145.5, 148.0, 150.5, 153.0, 155.5, 158.0, 160.75, 163.25, 165.75]
analog_holes = [121.0, 123.5, 126.13, 128.75, 131.25, 133.75, 138.75, 141.38, 144.0, 146.5, 149.0, 151.5, 154.0, 156.63]


def outline(x, z_first, z_last):
    (u0, v0), (u1, v1) = top_at(x - 1.35, z_last + 1.35), top_at(x + 1.35, z_first - 1.35)
    return dict(rect=[u0, v0, round(u1 - u0, 3), round(v1 - v0, 3)], line=0.15)


items += [outline(EDGE_DIGITAL, 121.0, 138.75), outline(EDGE_DIGITAL, 143.0, 165.75), outline(EDGE_ANALOG, 121.0, 133.75), outline(EDGE_ANALOG, 138.75, 156.63)]

top = dict(name='silkscreen top', origin=[X0, TOP + 0.02, Z1], u=[0, 0, -1], v=[1, 0, 0], size=[round(Z1 - Z0, 3), round(X1 - X0, 3)],
           px_per_mm=24, colour=INK, items=items)

# ---- the underside, read as in the photo of it (seen from below: x runs the other way)
under_at = lambda x, z: [round(X1 - x, 3), round(z - Z0, 3)]
under = []
pins = [133.72 + 2.54 * k for k in range(15)]            # the Nano's two 15-way sockets, x 77.08 and 61.78
for name, z in zip('VIN GND RST 5V A7 A6 A5 A4 A3 A2 A1 A0 AREF 3V3 D13'.split(), pins):
    under.append(text(name, 77.08 - 1.6, z, size=1.15, align='left', at=under_at))
for name, z in zip('TX RX RST GND D2 D3 D4 D5 D6 D7 D8 D9 D10 D11 D12'.split(), pins):
    under.append(text(name, 61.78 + 1.6, z, size=1.15, align='right', at=under_at))
for name, z in zip('A5 A4 A3 A2 A1 A0 VIN GND GND 5V NC RST'.split(), analog_holes[:12]):
    under.append(text(name, EDGE_ANALOG - 1.5, z, size=1.05, align='left', at=under_at))
for name, z in zip('RX TX 2 3 4 5 6 7 8 9 10 11 12 13 GND AREF'.split(), digital_holes[:16]):
    under.append(text(name, EDGE_DIGITAL + 1.5, z, size=1.05, align='right', at=under_at))
bottom = dict(name='silkscreen underside', origin=[X1, UNDER - 0.02, Z0], u=[-1, 0, 0], v=[0, 0, 1], size=[round(X1 - X0, 3), round(Z1 - Z0, 3)],
              px_per_mm=20, colour=INK, items=under)

# ---- the print on two parts on the board: the 47 uF capacitor (top at y 112.25) and the AMS1117 regulator (top at y 108.03)
cap_c, cap_r = (86.915, 151.945), 2.62
cap_at = lambda x, z: [round(cap_c[1] + 2.9 - z, 3), round(x - (cap_c[0] - 2.9), 3)]
capacitor = dict(name='capacitor print', origin=[cap_c[0] - 2.9, 112.27, cap_c[1] + 2.9], u=[0, 0, -1], v=[1, 0, 0], size=[5.8, 5.8], px_per_mm=40, colour=INK,
                 items=[dict(circle=[2.9, 2.9, cap_r], colour='#1b1b1b'), dict(circle=[2.9, 2.9, cap_r - 0.15], line=0.22, colour='#9a9a9a'),
                        *[text(s, cap_c[0], z, size=1.05, rot=-90, at=cap_at) for s, z in (('CS', 153.15), ('47', 151.95), ('35V', 150.75))]])
reg_at = lambda x, z: [round(154.63 - z, 3), round(x - 68.06, 3)]
regulator = dict(name='regulator print', origin=[68.06, 108.05, 154.63], u=[0, 0, -1], v=[1, 0, 0], size=[6.5, 3.5], px_per_mm=40, colour='#d0d0d0',
                 items=[dict(fill=[0, 0, 6.5, 3.5], colour='#1e1e1e'), text('AMS1117', 69.3, 151.38, size=0.95, at=reg_at), text('33  D309', 70.5, 151.38, size=0.75, at=reg_at)])

out = {'_about': 'Printing on parts, drawn by the player (js/core.js); materials.json "decals" names this file. Written by silkscreen.py: edit that, not this.',
       'NAUO82': [top, bottom, capacitor, regulator]}
with open(HERE / 'decals.json', 'w') as f:                # (one item a line)
    f.write('{\n "_about": ' + json.dumps(out['_about']) + ',\n "NAUO82": [\n')
    for k, d in enumerate(out['NAUO82']):
        head = {key: val for key, val in d.items() if key != 'items'}
        f.write('  ' + json.dumps(head)[:-1] + ', "items": [\n' + ',\n'.join('   ' + json.dumps(it) for it in d['items']) + ']}' + (',' if k < len(out['NAUO82']) - 1 else '') + '\n')
    f.write(' ]\n}\n')
json.load(open(HERE / 'decals.json'))                     # (it must read back)
print(f"decals.json: NAUO82 ({len(items)} items on top, {len(under)} underneath, the capacitor and the regulator)")
