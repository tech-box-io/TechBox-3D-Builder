"""PMG reuse study: write the DRAFT materials.json and colour atlas for the PMG (into docs/research/pmg/, not the kit), then check
them against pmg.glb: which mesh each rule catches (first match wins, as tools/build_model.py), meshes no rule or atlas entry
colours, and how well the atlas entries copied from the MRA / RCC match the PMG's own meshes (build_model's colour_from_atlas,
on the meshes' welded solids).

    .venv.nosync/bin/python docs/research/pmg/scripts/reuse_drafts.py
"""
import collections
import copy
import json
import re
import sys

import numpy as np

ROOT = '/Users/lee-johnson/Desktop/Claude_Cadasio/'
sys.path.insert(0, ROOT + 'tools')
sys.path.insert(0, ROOT + 'docs/research/pmg/scripts')
from build_model import colour_from_atlas, split_components, weld_positions  # noqa: E402
from reuse_hdr import Glb  # noqa: E402

OUT_MAT = ROOT + 'docs/research/pmg/materials.proposed.json'
OUT_ATLAS = ROOT + 'docs/research/pmg/colour-atlas-pmg.proposed.json'
rcc = json.load(open(ROOT + 'RCC Build Instructions/materials.json'))
rcc_atlas = json.load(open(ROOT + 'RCC Build Instructions/colour-atlas-rcc.json'))
mra_atlas = json.load(open(ROOT + 'MRA Build Instructions Prototype/colour-atlas-mra.json'))
trim = json.load(open(ROOT + 'docs/research/pmg/scripts/trim.example.json'))
poses = json.load(open(ROOT + 'docs/research/pmg/reuse_poses.json'))
nano_pose = next(g for g in poses['groups'] if g['built'].startswith('NANO'))['extra_parts_pose']

# ---------------------------------------------------------------- the draft materials.json
palette = {k: v for k, v in rcc['palette'].items() if k not in (
    'servo_fs90r', 'servo_fs90r_label', 'servo_fs90r_spline', 'tyre', 'battery_grey', 'battery_amber', 'battery_slate', 'battery_top',
    'pcb_white', 'silk_black', 'lead_yellow', 'servo_body', 'servo_label', 'pot_blue', 'header_red', 'header_white')}
palette.update({
    'jumper_cap': '#404040',          # the MRA's jumper caps (its atlas: Wire Cap #404040)
    'cap_black': '#1e1616',           # button caps: black plastic (Cadasio #000000)
    'cap_yellow': '#ffdc00',          # Cadasio #ffdc00 (= the house wire yellow)
    'cap_white': '#f5f5f6',           # Cadasio #ffffff; the house white plastic
    'cap_blue': '#0074d9',            # Cadasio #0074d9
    'led_white': '#ffffff',           # display segments, LED dots and the LED blocks' white sides (Cadasio #ffffff / #e4e4e4)
    'led_face': '#1e1616',            # the LED blocks' black face (Cadasio TOP MASK #1a1a1a) and the display's black window
})

# the 64 dots of a 1088AS block (own frame: face at own y 0, dots 3 mm across at these x / z centres; the column at x 2.0 is
# welded into the body in this export, so every dot is coloured by a box, after the black face box)
DOT_X = [2.0, 6.0, 9.9, 13.9, 17.9, 21.9, 25.8, 29.8]
DOT_Z = [-29.8, -25.9, -21.9, -17.9, -13.9, -9.9, -6.0, -2.0]
H = 1.1                               # half-size of each dot's box (inside the 1.5 radius: no corner of the black face caught)
dot_regions = [dict(box=[[round(x - H, 2), -0.15, round(z - H, 2)], [round(x + H, 2), 0.01, round(z + H, 2)]], color='led_white') for x in DOT_X for z in DOT_Z]

rules = [
    dict(match='\\^PMG Full 3D Cadasio Build$', omit=True,
         _about='the CAD\'s jumper wire and USB cable bodies (PartNN^..., Copy of PartNN^..., 114 sweeps): the player draws them as wires along '
                'wire-paths.json. Only needed if the full pmg.glb is the source (pmg-guide.glb has none).'),
    dict(match='^(nano-board|atmega328|ftdi FT232rl|NANO DIODE|MINIUSB(SHELL|CORE)|MINI USB (CONTACT|SOLDER)|16mhz crystal - measured|1[08][29] RESISTOR PACK|15pin_header__|2pin_header__02)$',
         omit=True, _about='the plain Nano model inside the I/O module\'s CAD (NAUO301 in NAUO78; the RCC car Nano\'s model): the guide fits the MRA\'s Nano '
                           '(NANO). Only needed if the full pmg.glb is the source; it cannot catch the plain Nano\'s LEDs, regulator, reset button, caps and '
                           'resistors, which share names with the module\'s own: trim it out (trim.json "drop") or make it a part of its own (own_parts NAUO301).'),
    dict(match='^USB Right Angle$', color='black_plastic', components=[dict(rank=[1, 2], color='pin')], simplify_mm=0.03, max_tris=3000, outline=True,
         _about='the USB cable\'s right-angle Mini-B end (NAUO282), 3 solids: overmould black, the plug\'s shell and its insert silver (as the MRA\'s straight Mini-B: '
                'plug silver, the rest black). Not in the MRA or RCC: their Mini-B end is straight (docs/research/pmg/reuse_plan.md 2.3).'),
    dict(match='^USB Cable end$', color='black_plastic', components=[dict(rank=1, color='pin'), dict(rank=2, color='white_plastic'), dict(rank=[3, 4], color='pin')],
         simplify_mm=0.03, max_tris=4000, outline=True,
         _about='the USB cable\'s A end (NAUO278): the same mesh as the MRA\'s usb-a-end.glb (vertices identical), the MRA\'s ^USBCableend$ rule renamed: overmould black, shell and contacts silver, tongue white'),
    dict(match='^H([1-9]|1[0-4])(v2)?$', color='wood', simplify_mm=0, roughen_mm=0.1, engraving='ink',
         _about='the laser-cut wood, H1 - H14 (four H9 keys; H4v2, H11v2, H12v2, H13v2): roughened as every kit\'s wood (publish.py requires it)'),
    dict(match='^Wire Cap( V2)?$', color='jumper_cap',
         _about='jumper wire caps: #404040 as the MRA\'s (its atlas; the PMG Cadasio has them #000000, the rulebook\'s Dupont housings #1e1616). "Wire Cap V2" (12 mm) is only on the CAD\'s loose ribbons.'),
    dict(match='^Board\\^Big Button Module', color='pcb_navy', simplify_mm=0.02, _about='the button modules\' boards (rulebook: PMG button boards #000f41)'),
    dict(match='^Socket_Blok$', color='pin', components=[dict(rank=1, color='header_black')],
         _about='a button module\'s header pin (rank 0, the bent pin, silver: Lee\'s pins-silver ruling; Cadasio #c6c1bc) and its black spacer (rank 1; Cadasio #1a1a1a). '
                'The CAD has four per module, two of them the same pin in the same place.'),
    dict(match='^Tactal Switch', color='black_plastic', simplify_mm=0.05, max_tris=3000, edge_min_size_mm=1.5,
         _about='the 12 x 12 mm tactile switch (21 solids: the body and 20 small marks 0.25 mm thick on it), all black (Cadasio #1e1e1e)'),
    dict(match='^Push_Button_Cap black$', color='cap_black', simplify_mm=0.05, max_tris=1500, outline=True, _about='NAUO76 (D4); renamed by trim.json'),
    dict(match='^Push_Button_Cap yellow$', color='cap_yellow', simplify_mm=0.05, max_tris=1500, outline=True, _about='NAUO83 (D5)'),
    dict(match='^Push_Button_Cap white$', color='cap_white', simplify_mm=0.05, max_tris=1500, outline=True, _about='NAUO84 (D6)'),
    dict(match='^Push_Button_Cap blue$', color='cap_blue', simplify_mm=0.05, max_tris=1500, outline=True, _about='NAUO85 (D7)'),
    dict(match='^Push_Button_Cap', color='cap_black', simplify_mm=0.05, max_tris=1500, outline=True,
         _about='a cap not renamed (the full pmg.glb as source): every cap one colour, since the four are one mesh'),
    dict(match='^Display TM1637', color='pin',
         components=[dict(rank=0, color='pcb_blue'), dict(rank=1, color='led_face'), dict(rank=2, color='ic_black'), dict(thin=[0, 0.02], color='led_white')],
         regions=[dict(box=[[-13.7, -6.45, 1.35], [15.7, 6.45, 8.25]], color='led_face'), dict(box=[[-13.7, -6.45, 8.45], [15.7, 6.45, 8.55]], color='led_face')],
         simplify_mm=0.02,
         _about='the TM1637 4-digit display (NAUO79), one mesh of 41 solids, the same solids as TechBox\'s Cadasio model: rank 0 the board, which in this CAD '
                'includes the display block, blue #224bbe (rulebook); rank 1 a black shell 0.1 mm over the block (Cadasio #000000); the two boxes make the block '
                'itself black under it (its sides and top; not the segments\' pockets\' rims, 8.25 - 8.45); rank 2 the TM1637 chip under the board; the 30 flat '
                'segment and colon pieces (0 thick, own z 8.3, in pockets of the block) white; the 4 bent pins and their 4 stubs silver.'),
    dict(match='^PCB$', color='pcb_blue', simplify_mm=0.03, max_tris=6000, edge_min_size_mm=1.0, _about='the LED matrix\'s board (Cadasio #234bbf ~ the house display blue)'),
    dict(match='^8x female rounded header$', color='header_black', simplify_mm=0.05, max_tris=1500, edge_min_size_mm=1.5,
         _about='the eight 8-way sockets between the matrix board and its four LED blocks (11,951 vertices each, all but hidden): kept light'),
    dict(match='^1088AS$', color='pin',
         components=[dict(rank=0, color='led_white'), dict(thin=[0, 0.02], color='ink')],
         regions=[dict(box=[[-0.5, -0.15, -32.3], [32.3, 0.01, 0.5]], color='led_face')] + dot_regions,
         simplify_mm=0.03, max_tris=8000,
         _about='an 8 x 8 LED block (4 per matrix), 79 solids: the body white (Cadasio #ffffff sides), its face (own y -0.1 to 0) black (Cadasio TOP MASK #1a1a1a), '
                'the 64 dots white (each by a box: one column is welded into the body in this export), the 16 legs silver, the "1088AS" print on its side (flat pieces) black'),
    dict(match='^MAX7219', color='ic_black', simplify_mm=0.02, _about='the four MAX7219 driver chips'),
    dict(match='^90 5xHeader Pins$', color='pin', components=[dict(rank=0, color='header_black')], simplify_mm=0.02,
         _about='the matrix\'s 5-way right-angle input header (VCC GND DIN CS CLK): plastic black, pins silver'),
]
# the I/O module's and the Nano's rules, exactly as the MRA / RCC have them
for r in rcc['rules']:
    if re.match(r'\^(nano_|Shield_Arduino|Samtec-TLW-|47uf CAP|cap106C|\(m7 diode|reset shell|led\$)', r['match']):
        rules.append(copy.deepcopy(r))

mat = dict(
    _about='DRAFT for "PMG Build Instructions/materials.json" (docs/research/pmg/reuse_plan.md): colour and detail rules for the PMG\'s 3D model. '
           'Rules are tried top to bottom against each CAD mesh name; the first match wins. A mesh whose rule names no colour takes its colours from the '
           'atlas: the MRA\'s for the parts the kits share (the I/O module, the Nano).',
    source='pmg-guide.glb', source_scale_to_mm=1000, palette=palette, defaults=copy.deepcopy(rcc['defaults']), rules=rules,
    atlas='colour-atlas-pmg.json',
    decals='decals.json',
    _notes=dict(
        reused='The I/O module (NAUO78) is the MRA\'s board (all 36 meshes the same, placed by one rigid turn); the Nano Board is the MRA\'s model '
               '(NANO, grafted by trim.json or extra_parts); the USB A end and the jumper caps are the MRA\'s meshes. Their rules and atlas entries are the MRA\'s.',
        wires='The CAD\'s jumper wire and USB cable bodies are left out of the model (pmg-guide.glb has none): the player draws them along wire-paths.json.',
        unconfirmed=['Button cap colours black / yellow / white / blue as TechBox\'s Cadasio (D4 - D7).',
                     'Jumper caps #404040 as the MRA (Cadasio PMG #000000).',
                     'The right-angle USB Mini-B end coloured as the MRA\'s straight one.',
                     'LED blocks white-sided with a black face, as the Cadasio.']),
)
# the Nano, if not grafted by trim.json: the MRA's export, placed by the module's transform
mat['_extra_parts_instead_of_graft'] = dict(NANO=dict(glb='nano-mra.glb', pose=nano_pose,
    _about='only if trim.json has no "graft": nano-mra.glb cut from the MRA WITHOUT --like: python tools/cut_part.py "MRA Build Instructions Prototype/mra.glb" '
           'NAUO126 "PMG Build Instructions/nano-mra.glb"; the pose is the MRA module -> NAUO78 transform (docs/research/pmg/reuse_poses.json)'))
json.dump(mat, open(OUT_MAT, 'w'), indent=1, ensure_ascii=False)

# ---------------------------------------------------------------- the draft atlas: the RCC's entries for the shared parts
atlas = {k: copy.deepcopy(v) for k, v in rcc_atlas.items() if k in ('_how_to_read', 'nano_Varsayılan', 'cap106C', 'nano - reg', 'led', 'User Library-PJ-002AH_Pad')
         or k.startswith('Samtec-TLW-')}
atlas['_about'] = ('DRAFT for "PMG Build Instructions/colour-atlas-pmg.json": the MRA\'s colour atlas entries (copied through the RCC\'s, unchanged) for the parts '
                   'the PMG shares with the MRA: the I/O module (NAUO78) and the Nano (NANO). The PMG\'s own parts are coloured by rules (materials.json).')
atlas['_source'] = dict(from_file='RCC Build Instructions/colour-atlas-rcc.json', which_has='the MRA atlas entries for these meshes, unchanged')
atlas['_single_colour'] = {k: v for k, v in rcc_atlas['_single_colour'].items() if k in (
    '47uf CAP Dcase', 'blm21', 'm7 diode', 'reset core', 'reset shell', 'Samtec-SSW-115-01-F-S', 'Shield_Arduino NANO', 'smt_resistor222_a', 'User Library-PJ-002AH_Body')}
atlas['_single_colour']['Wire Cap'] = mra_atlas['_single_colour']['Wire Cap']
for k, v in atlas.items():
    if isinstance(v, dict) and 'instances' in v:
        v['rcc_instances'] = v.pop('instances')
        v['instances'] = ['NANO'] if k == 'nano_Varsayılan' else ['NAUO78']
json.dump(atlas, open(OUT_ATLAS, 'w'), indent=1, ensure_ascii=False)
print('written', OUT_MAT, 'and', OUT_ATLAS)

# ---------------------------------------------------------------- checks against pmg.glb
P = Glb(ROOT + 'PMG Build Instructions/pmg.glb')
M = Glb(ROOT + 'MRA Build Instructions Prototype/mra.glb')
compiled = [(re.compile(r['match']), r) for r in rules]
renames = trim.get('rename', {})
drop = trim.get('drop', {})


def mesh_names(H, inst, skip=()):
    out = []
    i = H.find(inst)[0]
    dropped = set()
    for k in H.subtree(i):
        if H.nodes[k].get('name') in skip:
            dropped.update(H.subtree(k))
    for k in H.subtree(i):
        if k in dropped or 'mesh' not in H.nodes[k]:
            continue
        name = H.doc['meshes'][H.nodes[k]['mesh']].get('name')
        out.append((renames.get(inst, {}).get(name, name), H.nodes[k]['mesh']))
    return out


print('\n== the guide set (trim.example.json) against the draft rules: rule -> meshes caught')
caught, uncoloured = collections.defaultdict(collections.Counter), collections.Counter()
for inst in trim['keep']:
    for name, _ in mesh_names(P, inst, set(drop.get(inst, []))):
        rule = next((r for rx, r in compiled if rx.search(name)), None)
        if rule is None:
            how = 'atlas' if isinstance(atlas.get(name), dict) else 'atlas single colour' if name in atlas['_single_colour'] else None
            if how:
                caught['(no rule: ' + how + ')'][name] += 1
            else:
                uncoloured[name] += 1
        else:
            caught[rule['match']][name] += 1
caught[next(r['match'] for r in rules if r['match'] == '^nano_')]['nano_Varsayılan (grafted NANO)'] += 1
for m, names in caught.items():
    print(f'  {m}: ' + ', '.join(f'{n} x{c}' for n, c in names.items()))
print('  meshes nothing colours (would be the default grey):', dict(uncoloured) or 'none')
unused = [r['match'] for r in rules if r['match'] not in caught and not r.get('omit')]
print('  rules that catch nothing in the guide set:', unused)

print('\n== every mesh name in the full pmg.glb against the draft rules (what the omit rules catch, and anything left uncoloured)')
allnames = collections.Counter(P.doc['meshes'][P.nodes[k]['mesh']].get('name') for k in range(len(P.nodes)) if 'mesh' in P.nodes[k])
om, left = collections.Counter(), collections.Counter()
for name, c in allnames.items():
    rule = next((r for rx, r in compiled if rx.search(name)), None)
    if rule and rule.get('omit'):
        om[rule['match'][:30]] += c
    elif rule is None and not isinstance(atlas.get(name), dict) and name not in atlas['_single_colour']:
        left[name] += c
print('  omitted meshes by rule:', dict(om))
print('  names with no rule and no atlas entry:', dict(left) or 'none')

print('\n== atlas entries copied from the MRA, matched on the PMG\'s own meshes of NAUO78 (build_model.colour_from_atlas, needs >= 60 %)')
seen = set()
for name, mi in mesh_names(P, 'NAUO78', {'NAUO301'}):
    if not isinstance(atlas.get(name), dict) or name in seen:
        continue
    seen.add(name)
    (V, I), = P.triangles(mi)
    V = V.astype(np.float64) * 1000
    Vp, remap = weld_positions(V)
    Fp = remap[I.reshape(-1, 3).astype(np.int64)]
    n, labels = split_components(len(Vp), Fp)
    boxes = np.array([[Vp[labels == c].min(0), Vp[labels == c].max(0)] for c in range(n)])
    cols, score, _ = colour_from_atlas(boxes, atlas[name])
    print(f'  {name}: {n} solids, match {score:.0%}' + (f', colours {dict(collections.Counter(cols))}' if cols else ''))
