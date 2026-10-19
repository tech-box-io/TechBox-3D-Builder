"""Write lac-guide.glb: the LAC CAD export (lac.glb) cut down to the parts the guide uses.

Run from the project root:   python "LAC Build Instructions/trim_source.py"

The engineer's export (LAC Full Build.STEP -> lac.glb, 159 top-level instances) carries most parts several times, once for each
pose the SolidWorks model was set up in (four F1 / potentiometer sets, three LCDs, three switches, two buzzers, every wire in two
or three poses), and the wires as solid bodies. The guide shows each part once and moves it itself, and draws the wires (their
centre lines are in wire-paths.json), so the generator and the model builder only need the instances listed in KEEP: about a
third of the triangles, which keeps each run light on this computer's memory (CLAUDE.md, "This computer").
Instance names stay the CAD's (NAUO1 ...), so guide.py, materials.json and wire-paths.json refer to the same ids either way.
Re-run after replacing lac.glb.
"""
import json
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
from glbio import read_glb  # noqa: E402

# Every instance the guide may show, seated (where the CAD has a part in several poses, the seated one: the guide moves it).
KEEP = [
    'NAUO1',                                            # breadboard
    'NAUO2',                                            # F3, the base
    'NAUO3', 'NAUO4',                                   # the real-time clock module and its coin cell, in its holder (NAUO5 is a second copy, half out of it)
    'NAUO6', 'NAUO7',                                   # the two resistors (legs both straight and bent: the straight ones are omitted)
    'NAUO10', 'NAUO11', 'NAUO12', 'NAUO13', 'NAUO146',  # F1 seated, with the potentiometer, its nut, knob and washer
    'NAUO42', 'NAUO43', 'NAUO44', 'NAUO45',             # F7 x2, F8, F9
    'NAUO46',                                           # the rocker switch, seated (F4 itself is extra part F4)
    'NAUO62',                                           # the buzzer, between the two F7s
    'NAUO94',                                           # the LCD, seated in F9's notches behind F1's window
    'NAUO122',                                          # the USB cable's right-angle Mini-B end, in the Nano Board
    'NAUO141',                                          # the breadboard's protective backing
    # the male Dupont caps in the breadboard: 8 loose jumpers (2 each), the switch's, potentiometer's and buzzer's leads (one
    # each), the LCD's four wires (their male ends)
    'NAUO14', 'NAUO15', 'NAUO16', 'NAUO17', 'NAUO19', 'NAUO20', 'NAUO21', 'NAUO22', 'NAUO25', 'NAUO26', 'NAUO28', 'NAUO30',
    'NAUO31', 'NAUO33', 'NAUO34', 'NAUO47', 'NAUO48', 'NAUO49', 'NAUO52', 'NAUO53', 'NAUO55', 'NAUO56', 'NAUO58', 'NAUO59',
    'NAUO82', 'NAUO84', 'NAUO86', 'NAUO93',
    'NAUO97', 'NAUO98', 'NAUO99', 'NAUO100',            # the LCD wires' female caps on the seated LCD's header
]
COMPONENT = {5120: 1, 5121: 1, 5122: 2, 5123: 2, 5125: 4, 5126: 4}
PER_TYPE = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT2': 4, 'MAT3': 9, 'MAT4': 16}


def main(src=HERE / 'lac.glb', out=HERE / 'lac-guide.glb'):
    doc, blob = read_glb(src)
    nodes = doc['nodes']
    root = doc['scenes'][0]['nodes'][0]
    by_name = {nodes[c].get('name'): c for c in nodes[root]['children']}
    missing = [k for k in KEEP if k not in by_name]
    if missing:
        raise SystemExit(f'not in {src.name}: {missing}')
    keep, todo = [root], [by_name[k] for k in KEEP]
    while todo:
        i = todo.pop(0)
        keep.append(i)
        todo += nodes[i].get('children', [])
    new_node = {old: k for k, old in enumerate(keep)}
    meshes = sorted({nodes[i]['mesh'] for i in keep if 'mesh' in nodes[i]})
    new_mesh = {old: k for k, old in enumerate(meshes)}
    res = dict(asset=dict(version='2.0', generator='TechBox LAC trim_source.py'), scene=0, scenes=[dict(nodes=[0])], nodes=[], meshes=[],
               accessors=[], bufferViews=[], materials=[])
    data, accessors, materials = bytearray(), {}, {}

    def copy_accessor(index):
        if index not in accessors:
            acc = doc['accessors'][index]
            view = doc['bufferViews'][acc['bufferView']]
            size = COMPONENT[acc['componentType']] * PER_TYPE[acc['type']]
            stride = view.get('byteStride', size)
            start = view.get('byteOffset', 0) + acc.get('byteOffset', 0)
            length = stride * (acc['count'] - 1) + size if acc['count'] else 0
            while len(data) % 4:
                data.append(0)
            res['bufferViews'].append({**{k: v for k, v in view.items() if k not in ('buffer', 'byteOffset', 'byteLength')},
                                       'buffer': 0, 'byteOffset': len(data), 'byteLength': length})
            data.extend(blob[start:start + length])
            res['accessors'].append({**{k: v for k, v in acc.items() if k != 'byteOffset'}, 'bufferView': len(res['bufferViews']) - 1})
            accessors[index] = len(res['accessors']) - 1
        return accessors[index]

    for old in meshes:
        m = doc['meshes'][old]
        prims = []
        for p in m['primitives']:
            q = dict(p, attributes={k: copy_accessor(v) for k, v in p['attributes'].items()})
            if 'indices' in p:
                q['indices'] = copy_accessor(p['indices'])
            if 'material' in p:
                if p['material'] not in materials:
                    res['materials'].append(doc['materials'][p['material']])
                    materials[p['material']] = len(res['materials']) - 1
                q['material'] = materials[p['material']]
            prims.append(q)
        res['meshes'].append(dict(m, primitives=prims))
    for old in keep:
        n = {k: v for k, v in nodes[old].items() if k not in ('children', 'mesh')}
        if 'mesh' in nodes[old]:
            n['mesh'] = new_mesh[nodes[old]['mesh']]
        kids = [new_node[c] for c in nodes[old].get('children', []) if c in new_node]
        if kids:
            n['children'] = kids
        res['nodes'].append(n)
    if not res['materials']:
        del res['materials']
    while len(data) % 4:
        data.append(0)
    res['buffers'] = [dict(byteLength=len(data))]
    js = json.dumps(res, separators=(',', ':')).encode()
    js += b' ' * ((-len(js)) % 4)
    with open(out, 'wb') as f:
        f.write(struct.pack('<III', 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(data)))
        f.write(struct.pack('<II', len(js), 0x4E4F534A) + js)
        f.write(struct.pack('<II', len(data), 0x004E4942) + bytes(data))
    print(f'{out.name}: {len(KEEP)} of {len(nodes[root]["children"])} instances from {src.name}, {len(meshes)} meshes, {len(data) / 1e6:.1f} MB')


if __name__ == '__main__':
    main()
