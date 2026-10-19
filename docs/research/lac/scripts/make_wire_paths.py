"""Write the LAC kit's wire-paths.json from the CAD (lac.glb): the breadboard's hole grid, every Dupont cap, every wire body's
centre line (lac_wires.json, from wires3.py), and the poses between the CAD's posed copies (poses.json, from poses.py)."""
from lacload import *
import json
W = json.load(open('lac_wires.json'))
P = json.load(open('poses.json'))
# Cadasio's colour for each wire body (TechBox's published project: docs/research/lac/cadasio)
COLOUR = {'Part1': 'black', 'Part2': 'green', 'Part3': 'blue', 'Part4': 'purple', 'Part6': 'white', 'Part7': 'dark_red', 'Part26': 'orange', 'Part27': 'yellow',
          'Part31': 'red?', 'Part32': 'black?', 'Part37': 'black', 'Part38': 'red', 'Part40': 'purple', 'Part41': 'yellow', 'Part42': 'teal', 'Part43': 'blue',
          'Part44': 'purple', 'Part45': 'yellow', 'Part47': 'blue', 'Part48': 'teal', 'Part49': 'purple', 'Part50': 'yellow', 'Part51': 'teal', 'Part52': 'blue',
          'Part67': 'usb', 'Part75': 'black', 'Part76': 'tan', 'Part77': 'red', 'Part78': 'orange', 'Part79': 'yellow', 'Part80': 'black', 'Part81': 'tan',
          'Part82': 'red', 'Part83': 'red', 'Part84': 'tan', 'Part85': 'black', 'Part86': 'red', 'Part87': 'tan', 'Part88': 'black',
          'Part15': '6-way ribbon', 'Part16': '6-way ribbon', 'Part17': '6-way ribbon', 'Part18': '6-way ribbon', 'Part19': '6-way ribbon', 'Part20': '6-way ribbon'}
COPY_COLOUR = {'Part15': 'purple', 'Part16': 'yellow', 'Part17': 'blue', 'Part18': 'teal'}   # the 4-way male-female ribbon
caps = {}
for c, ci in W['caps'].items():
    lo, hi = np.array(ci['lo']), np.array(ci['hi'])
    mid = (lo + hi) / 2
    e = dict(kind=ci['kind'], box=[lo.round(3).tolist(), hi.round(3).tolist()], axis=ci['axis'])
    if ci['kind'] == 'male' and ci['axis'] == 'y':
        e.update(top=[round(mid[0], 3), round(hi[1], 3), round(mid[2], 3)], wire_at=[round(mid[0], 3), round(hi[1] - 4.0, 3), round(mid[2], 3)],
                 tip=[round(mid[0], 3), round(lo[1], 3), round(mid[2], 3)])
    caps[c] = e
rows = dict(a=689.25, b=686.71, c=684.17, d=681.63, e=679.09, f=671.31, g=668.77, h=666.23, i=663.69, j=661.15)
holes = {}
def col_z(n): return round(1344.66 - 2.54 * n, 2)
TOP = 897.11
for r, x in rows.items():
    for n in range(1, 31):
        holes[f'{r}{n}'] = [x, TOP, col_z(n)]
out = dict(
    _about="LAC (LCD Alarm Clock): where the wires run in the CAD and how the breadboard is laid out, measured from lac.glb (converted from "
           "LAC Full Build.STEP) on 19 Oct 2026 by docs/research/lac/scripts (wires3.py, poses.py, make_wire_paths.py). Millimetres in assembly "
           "space, Y up, as assembled. 'lines': the centre line of every wire body the CAD has (they are left out of the model: the player draws "
           "the wires), with the Dupont cap nearest each end ('cap_a' / 'cap_b', distance in mm: 0 = the line ends inside that cap) and its colour in "
           "TechBox's published LAC Cadasio project. 'caps': every Dupont cap (male 'Wire Cap V2': a 1.75 mm square housing 8 mm long over an 8 mm "
           "pin, 4 mm of it below the housing; female 'Wire Cap', the MRA's part); for a male cap standing in the breadboard, 'top' (the housing's "
           "top, where the wire leaves it), 'wire_at' (where the CAD's wire ends, inside the housing) and 'tip'. 'holes': every terminal hole's top "
           "(a1 ... j30; rows a - e and f - j, columns 1 - 30 along -z), fitted to the caps the CAD has in them; the power rails are 'rails'. "
           "'poses': the CAD's posed copies of a part relative to its seated copy (stepgen poses: [x, y, z] or {t, r, at}).",
    breadboard=dict(top_y=TOP, rows=rows, column_z='1344.66 - 2.54 * column', rails={'+ red': 696.68, '- blue': 699.2},
                    rail_note='rail holes lie at z = 1284.92 + 2.54 k (in groups of five), half a pitch from the terminal columns: a lead from a rail to a terminal hole does not run square to the board',
                    unused_rails='the two rails on the j side, about x 651.0 and 653.5'),
    holes=holes, caps=caps,
    lines={k.split('/')[-1] if '/' in k else k: dict(mesh=v['mesh'], colour=(COPY_COLOUR if v['mesh'].startswith('Copy of') else COLOUR).get(v['mesh'].split('^')[0].replace('Copy of ', ''), '?'),
                                                     length_mm=v['length'], cap_a=v['cap_a'], cap_b=v['cap_b'], pts=v['pts']) for k, v in W['wires'].items()},
    poses=P)
json.dump(out, open('/Users/lee-johnson/Desktop/Claude_Cadasio/LAC Build Instructions/wire-paths.json', 'w'), separators=(',', ':'))
print(len(out['lines']), 'lines', len(caps), 'caps')
print({k: (v['colour'], v['length_mm']) for k, v in out['lines'].items()})
