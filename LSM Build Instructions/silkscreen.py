"""The printing on the LED matrix's back and the label stuck on it, written to decals.json for the part MATRIX (materials.json
"decals" names it).

    python "LSM Build Instructions/silkscreen.py"      then   python "LSM Build Instructions/guide.py" (or tools/build_model.py)

Lee asked for the label on 19 Oct 2026 ("there's also a label on the back of the LED Matrix now"), with photographs of the real board
(docs/research/lsm/lee_images_2026-10-19/3.jpg, 4.jpg). Placed from the photograph fitted on the board's mounting holes
(docs/research/lsm/round2/led_matrix.md, sections 3 and 4). The CAD board is about 5 mm short of the real one along its rows, so
places are mapped through the holes and sizes kept true. The player draws the decals in the browser (js/core.js).

A decal is a flat picture laid on a face: `origin` is its top-left corner, `u` the way its "right" runs, `v` the way its "down" runs
(all seated mm), seen from the side v x u faces. Items are in picture mm: text (size = font size), fill. Everything is worked out in
the matrix's own frame (x along the assembly's x, own y along -z, own z 0 at the back face, which faces down) and placed with the
matrix's placement in lsm.glb, so that a move of the matrix in assemble.py carries its printing.
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
from glbio import node_matrix, read_glb  # noqa: E402

doc, _ = read_glb(HERE / 'lsm.glb')
PLACE = node_matrix(next(n for n in doc['nodes'] if n.get('name') == 'MATRIX'))
PLACE[:3, 3] *= 1000.0
seated = lambda p: (PLACE @ [*p, 1.0])[:3].round(3).tolist()
along = lambda d: (PLACE[:3, :3] @ d).round(6).tolist()

INK, LABEL, LABEL_INK = '#f2f2f2', '#f4f4f2', '#1e1616'
X0, Y0 = -32.75, -31.65                                   # the board's corner at own min x, min y (the far end from the header)

# The board's own print, white, reading along +x with the tops of the letters away from the header (seen from below).
back = dict(name='silkscreen back', origin=seated([X0, Y0, -0.02]), u=along([1, 0, 0]), v=along([0, 1, 0]), size=[63.79, 60.42],
            px_per_mm=24, colour=INK, items=[
                dict(text='WS2812B-64', at=[31.60, 19.95], size=3.59, weight=400, width=20.9),
                dict(text='Better Than Expected', at=[30.62, 27.89], size=2.5, weight=400, width=25.6),
                dict(fill=[24.30, 32.50, 10.8, 5.1]),
                dict(text='BTE', at=[29.53, 35.03], size=5.74, weight='italic 700', width=9.3, colour='#111111'),
                dict(text='Only ONE Pin', at=[14.08, 42.91], size=2.53, weight=400, width=13.9),
                dict(text='24 bit color', at=[29.69, 42.91], size=2.53, weight=400, width=11.2),
                dict(text='64 RGB LEDs', at=[46.09, 42.91], size=2.53, weight=400, width=15.4)])

# The label: a white half-inch square beside the header, past the pins' tips, reading the other way round (its tops towards the
# header), "V- IN V+" in black, V+ over the V+ pin's side. 0.04 mm off the face, so that it is drawn over the board's print.
LX, LY = -19.713, 9.053                                   # its corner at own max x, min y (seated x 619.96, z 1193.50)
label = dict(name='label V- IN V+', origin=seated([LX, LY, -0.04]), u=along([-1, 0, 0]), v=along([0, -1, 0]), size=[12.7, 12.7],
             px_per_mm=40, colour=LABEL_INK, items=[
                 dict(fill=[0, 0, 12.7, 12.7], colour=LABEL),
                 dict(text='V-', at=[1.69, 6.49], size=2.2, weight=400),
                 dict(text='IN', at=[5.51, 6.49], size=2.2, weight=400),
                 dict(text='V+', at=[9.70, 6.49], size=2.2, weight=400)])

about = 'Printing on parts, drawn by the player (js/core.js); materials.json "decals" names this file. Written by silkscreen.py: edit that, not this.'
decals = [back, label]
with open(HERE / 'decals.json', 'w') as f:                # (one item a line)
    f.write('{\n "_about": ' + json.dumps(about) + ',\n "MATRIX": [\n')
    for k, d in enumerate(decals):
        head = {key: val for key, val in d.items() if key != 'items'}
        f.write('  ' + json.dumps(head)[:-1] + ', "items": [\n' + ',\n'.join('   ' + json.dumps(it) for it in d['items']) + ']}' + (',' if k < len(decals) - 1 else '') + '\n')
    f.write(' ]\n}\n')
json.load(open(HERE / 'decals.json'))                     # (it must read back)
print(f"decals.json: MATRIX (the board's print, {len(back['items'])} items; the label)  back face at y {seated([0, 0, 0])[1]}")
