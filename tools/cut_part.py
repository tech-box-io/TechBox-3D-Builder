"""Cut one part out of a CAD export (GLB from STEP) into a GLB of its own, for materials.json "extra_parts".

    python tools/cut_part.py <source.glb> <node name> <out.glb> [--like <other.glb> <node name>]

The part (the named node and everything under it) is written in assembly space, exactly as it sits in the source's
assembly; with --like, it is put where the named node of another export sits instead: the same CAD part used in another
kit, when one export of it is better than the other (the RCC's two Nano Boards are the MRA's Nano model, whose export is
finer: the RCC's has sliver triangles across the board). The extra part's "pose" in materials.json then moves it from there.
"""
import argparse
import json
import struct
from pathlib import Path

import numpy as np

from glbio import node_matrix, read_glb


COMPONENT = {5120: 1, 5121: 1, 5122: 2, 5123: 2, 5125: 4, 5126: 4}          # glTF component types, bytes each
PER_TYPE = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT2': 4, 'MAT3': 9, 'MAT4': 16}


def world(doc, name):
    """The named node's index and its world matrix (the export's own units)."""
    nodes = doc['nodes']
    parent = {c: i for i, n in enumerate(nodes) for c in n.get('children', [])}
    i = next((k for k, n in enumerate(nodes) if n.get('name') == name), None)
    if i is None:
        raise SystemExit(f'no node called {name}')
    m, k = np.eye(4), i
    while k is not None:
        m = node_matrix(nodes[k]) @ m
        k = parent.get(k)
    return i, m


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('source')
    ap.add_argument('node')
    ap.add_argument('out')
    ap.add_argument('--like', nargs=2, metavar=('OTHER_GLB', 'NODE'))
    a = ap.parse_args()
    doc, blob = read_glb(a.source)
    top, place = world(doc, a.node)
    if a.like:
        place = world(read_glb(a.like[0])[0], a.like[1])[1]
    nodes, keep = doc['nodes'], []
    todo = [top]
    while todo:
        i = todo.pop(0)
        keep.append(i)
        todo += nodes[i].get('children', [])
    new_node = {old: k + 1 for k, old in enumerate(keep)}            # (node 0 is the frame)
    meshes = sorted({nodes[i]['mesh'] for i in keep if 'mesh' in nodes[i]})
    new_mesh = {old: k for k, old in enumerate(meshes)}
    out = dict(asset=dict(version='2.0', generator='TechBox cut_part.py'), scene=0, scenes=[dict(nodes=[0])],
               nodes=[dict(name=f'{a.node}_frame', children=[1])], meshes=[], accessors=[], bufferViews=[], materials=[])
    data, accessors, materials = bytearray(), {}, {}

    def copy_accessor(index):
        """The accessor and only its own bytes (an export may keep every mesh's data in one view: copying the whole view
        would carry the rest of the assembly along)."""
        if index not in accessors:
            acc = doc['accessors'][index]
            view = doc['bufferViews'][acc['bufferView']]
            size = COMPONENT[acc['componentType']] * PER_TYPE[acc['type']]
            stride = view.get('byteStride', size)
            start = view.get('byteOffset', 0) + acc.get('byteOffset', 0)
            length = stride * (acc['count'] - 1) + size if acc['count'] else 0
            while len(data) % 4:
                data.append(0)
            out['bufferViews'].append({**{k: v for k, v in view.items() if k not in ('buffer', 'byteOffset', 'byteLength')},
                                       'buffer': 0, 'byteOffset': len(data), 'byteLength': length})
            data.extend(blob[start:start + length])
            out['accessors'].append({**{k: v for k, v in acc.items() if k != 'byteOffset'}, 'bufferView': len(out['bufferViews']) - 1})
            accessors[index] = len(out['accessors']) - 1
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
                    out['materials'].append(doc['materials'][p['material']])
                    materials[p['material']] = len(out['materials']) - 1
                q['material'] = materials[p['material']]
            prims.append(q)
        out['meshes'].append(dict(m, primitives=prims))
    for old in keep:
        n = {k: v for k, v in nodes[old].items() if k not in ('matrix', 'translation', 'rotation', 'scale', 'children', 'mesh')}
        m = place if old == top else node_matrix(nodes[old])
        if not np.allclose(m, np.eye(4)):
            n['matrix'] = m.T.reshape(-1).tolist()
        if 'mesh' in nodes[old]:
            n['mesh'] = new_mesh[nodes[old]['mesh']]
        if nodes[old].get('children'):
            n['children'] = [new_node[c] for c in nodes[old]['children']]
        out['nodes'].append(n)
    if not out['materials']:
        del out['materials']
    while len(data) % 4:
        data.append(0)
    out['buffers'] = [dict(byteLength=len(data))]
    js = json.dumps(out, separators=(',', ':')).encode()
    js += b' ' * ((-len(js)) % 4)
    with open(a.out, 'wb') as f:
        f.write(struct.pack('<III', 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(data)))
        f.write(struct.pack('<II', len(js), 0x4E4F534A) + js)
        f.write(struct.pack('<II', len(data), 0x004E4942) + bytes(data))
    print(f'{Path(a.out).name}: {a.node} from {Path(a.source).name}, {len(keep)} nodes, {len(meshes)} meshes, {len(data) / 1e6:.1f} MB'
          + (f', placed like {a.like[1]} in {Path(a.like[0]).name}' if a.like else ''))


if __name__ == '__main__':
    main()
