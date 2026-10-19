"""PROPOSAL (not yet in the kit): cut the PMG's CAD export down to the parts the guide uses, a "trimmed source" that
materials.json "source" and guide.py's Guide(source=...) then name instead of pmg.glb.

    .venv.nosync/bin/python "PMG Build Instructions/trim_source.py"              reads trim.json beside it, writes its "out"
    .venv.nosync/bin/python "PMG Build Instructions/trim_source.py" --check      says what it would keep and how big, writes nothing
    (here, for review: .venv.nosync/bin/python docs/research/pmg/scripts/trim_source.py --config <trim.json> [--out <file>])

Why. pmg.glb (167 MB, 6.5 million vertices, 10.7 million triangles) holds the engineer's pose copies of most parts (three I/O
modules, two Nanos, eight buttons, three displays, four LED matrices, three of each USB end) and every jumper wire and the USB
cable as solids (114 sweep bodies, 60 % of the vertices). tools/stepgen.py loads the whole source with trimesh on every
guide.py run and copies every mesh (about 570 MB per copy of the file's geometry, two to three copies at once), and
tools/build_model.py holds the whole file in memory (twice while it adds extra_parts). On this 16 GB Mac, with swap nearly full,
that is the kind of job that took the machine down on 13 Oct 2026. The guide needs one copy of each part, where it sits built
(every other position is a pose of that copy); the wires are drawn by the player from wire-paths.json, which must be measured
from the full pmg.glb BEFORE it is trimmed.

What it writes. A GLB with the same assembly node and, under it, only the kept top-level instances, each with its own name,
matrix and sub-tree as in the source (so part ids such as NAUO78 are unchanged and guide.py works with either file), and only
those meshes' bytes (each accessor's own bytes, as tools/cut_part.py copies them: the source keeps all geometry in three
buffer views). Identical accessors are stored once (the 34 jumper caps, the four buttons' parts, the LED matrix's eight
headers). The source is read through a memory map: the script's memory is the output's size plus the JSON header.

trim.json:
  "source": "pmg.glb", "out": "pmg-guide.glb",
  "keep":   ["NAUO78", ...]                       top-level instances kept as they are
  "drop":   {"NAUO78": ["NAUO301"]}               nodes left out inside a kept instance, by node name (the I/O module's own plain
                                                  Nano: the guide fits the MRA's Nano model instead)
  "rename": {"NAUO76": {"Push_Button_Cap.step_По умолчанию": "Push_Button_Cap black"}}
                                                  one instance's mesh under a name of its own, so that a materials.json rule can
                                                  colour it alone (the four button caps are the same mesh in the CAD)
  "graft":  {"NANO": {"glb": "../MRA Build Instructions Prototype/mra.glb", "node": "NAUO126", "pose": {"t", "r", "at"}}}
                                                  optional: a part from another export, as a top-level instance of its own, its
                                                  node's world placement in that file moved by `pose` (assembly mm, as
                                                  materials.json extra_parts poses). Instead of extra_parts + cut_part.py.
The GLB's asset.extras records the source's size and SHA-256 and the config, so a stale trimmed file can be told apart.
"""
import argparse
import hashlib
import json
import mmap
import struct
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1] if (Path(__file__).resolve().parents[1] / 'tools').exists() else Path('/Users/lee-johnson/Desktop/Claude_Cadasio')
sys.path.insert(0, str(ROOT / 'tools'))
from glbio import node_matrix  # noqa: E402

COMPONENT = {5120: 1, 5121: 1, 5122: 2, 5123: 2, 5125: 4, 5126: 4}
PER_TYPE = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT2': 4, 'MAT3': 9, 'MAT4': 16}


class Source:
    """A GLB read as its JSON header plus a memory map of the file (no copy of the binary chunk)."""

    def __init__(self, path):
        self.path = Path(path)
        self.f = open(path, 'rb')
        magic, version, _ = struct.unpack('<III', self.f.read(12))
        if magic != 0x46546C67 or version != 2:
            raise SystemExit(f'{path} is not a GLB v2 file')
        clen, _ = struct.unpack('<II', self.f.read(8))
        self.doc = json.loads(self.f.read(clen))
        self.bin = 12 + 8 + clen + 8
        self.mm = mmap.mmap(self.f.fileno(), 0, access=mmap.ACCESS_READ)
        self.nodes = self.doc['nodes']
        self.parent = {c: i for i, n in enumerate(self.nodes) for c in n.get('children', [])}

    def accessor_bytes(self, index):
        a = self.doc['accessors'][index]
        view = self.doc['bufferViews'][a['bufferView']]
        size = COMPONENT[a['componentType']] * PER_TYPE[a['type']]
        stride = view.get('byteStride', size)
        start = self.bin + view.get('byteOffset', 0) + a.get('byteOffset', 0)
        if stride == size:
            return bytes(self.mm[start:start + size * a['count']]), view
        rows = np.lib.stride_tricks.as_strided(np.frombuffer(self.mm, np.uint8, count=stride * (a['count'] - 1) + size, offset=start),
                                               shape=(a['count'], size), strides=(stride, 1))
        return rows.tobytes(), view                         # (de-interleaved: written tightly packed)

    def world(self, i):
        m = np.eye(4)
        while i is not None:
            m = node_matrix(self.nodes[i]) @ m
            i = self.parent.get(i)
        return m

    def assembly(self):
        r = self.doc['scenes'][self.doc.get('scene', 0)]['nodes'][0]
        while len(self.nodes[r].get('children', [])) == 1 and 'mesh' not in self.nodes[r]:
            r = self.nodes[r]['children'][0]
        return r


def pose_matrix(pose):
    """materials.json / steps.json pose (assembly mm) as a 4x4: [x, y, z], or {"t", "r": [ax, ay, az, degrees], "at"}."""
    m = np.eye(4)
    if isinstance(pose, dict):
        t, r, at = np.asarray(pose.get('t', [0, 0, 0]), float), pose.get('r'), np.asarray(pose.get('at', [0, 0, 0]), float)
        if r and r[3]:
            ax = np.asarray(r[:3], float) / np.linalg.norm(r[:3])
            a = np.radians(r[3])
            K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
            m[:3, :3] = np.eye(3) + np.sin(a) * K + (1 - np.cos(a)) * K @ K
            m[:3, 3] = at - m[:3, :3] @ at
        m[:3, 3] += t
    elif pose is not None:
        m[:3, 3] = np.asarray(pose, float)
    return m


class Writer:
    def __init__(self):
        self.out = dict(asset=dict(version='2.0', generator='TechBox trim_source.py'), scene=0, scenes=[dict(nodes=[0])],
                        nodes=[], meshes=[], accessors=[], bufferViews=[], materials=[])
        self.data = bytearray()
        self.by_content = {}                                # identical accessors are stored once
        self.refs = 0
        self.materials = {}

    def accessor(self, src, index):
        a = src.doc['accessors'][index]
        raw, view = src.accessor_bytes(index)
        key = (a['componentType'], a['type'], a['count'], a.get('normalized', False), hashlib.sha1(raw).hexdigest())
        self.refs += 1
        if key not in self.by_content:
            while len(self.data) % 4:
                self.data.append(0)
            bv = {k: v for k, v in view.items() if k in ('target',)}
            if view.get('byteStride') and a['type'] != 'SCALAR':
                bv['byteStride'] = COMPONENT[a['componentType']] * PER_TYPE[a['type']]
            self.out['bufferViews'].append(dict(bv, buffer=0, byteOffset=len(self.data), byteLength=len(raw)))
            self.data.extend(raw)
            self.out['accessors'].append({**{k: v for k, v in a.items() if k not in ('byteOffset', 'bufferView', 'sparse')},
                                          'bufferView': len(self.out['bufferViews']) - 1})
            self.by_content[key] = len(self.out['accessors']) - 1
        return self.by_content[key]

    def mesh(self, src, index, name=None):
        m = src.doc['meshes'][index]
        prims = []
        for p in m['primitives']:
            q = dict(p, attributes={k: self.accessor(src, v) for k, v in p['attributes'].items()})
            if 'indices' in p:
                q['indices'] = self.accessor(src, p['indices'])
            if 'material' in p:
                mk = (id(src), p['material'])
                if mk not in self.materials:
                    self.out['materials'].append(src.doc['materials'][p['material']])
                    self.materials[mk] = len(self.out['materials']) - 1
                q['material'] = self.materials[mk]
            q.pop('targets', None)
            prims.append(q)
        self.out['meshes'].append(dict({k: v for k, v in m.items() if k != 'primitives'}, name=name or m.get('name'), primitives=prims))
        return len(self.out['meshes']) - 1

    def subtree(self, src, i, drop=(), rename=None, top_matrix=None, top_name=None, report=None):
        """Copy node i and its children (less any named in `drop`); returns the new node's index."""
        n = src.nodes[i]
        new = {k: v for k, v in n.items() if k not in ('children', 'mesh', 'matrix', 'translation', 'rotation', 'scale')}
        if top_name:
            new['name'] = top_name
        if top_matrix is not None:
            if not np.allclose(top_matrix, np.eye(4)):
                new['matrix'] = top_matrix.T.reshape(-1).tolist()
        else:
            new.update({k: n[k] for k in ('matrix', 'translation', 'rotation', 'scale') if k in n})
        k = len(self.out['nodes'])
        self.out['nodes'].append(new)
        if 'mesh' in n:
            name = src.doc['meshes'][n['mesh']].get('name')
            new['mesh'] = self.mesh(src, n['mesh'], (rename or {}).get(name))
            if report is not None:
                report['meshes'] += 1
                report['verts'] += src.doc['accessors'][src.doc['meshes'][n['mesh']]['primitives'][0]['attributes']['POSITION']]['count']
                if rename and name in rename:
                    report['renamed'].append(name)
        kids = []
        for c in n.get('children', []):
            if src.nodes[c].get('name') in drop:
                if report is not None:
                    report['dropped'].append(src.nodes[c].get('name'))
                continue
            kids.append(self.subtree(src, c, drop, rename, report=report))
        if kids:
            new['children'] = kids
        return k

    def write(self, path, extras):
        self.out['asset']['extras'] = extras
        if not self.out['materials']:
            del self.out['materials']
        while len(self.data) % 4:
            self.data.append(0)
        self.out['buffers'] = [dict(byteLength=len(self.data))]
        js = json.dumps(self.out, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
        js += b' ' * ((-len(js)) % 4)
        total = 12 + 8 + len(js) + 8 + len(self.data)
        if path:
            with open(path, 'wb') as f:
                f.write(struct.pack('<III', 0x46546C67, 2, total))
                f.write(struct.pack('<II', len(js), 0x4E4F534A) + js)
                f.write(struct.pack('<II', len(self.data), 0x004E4942) + bytes(self.data))
        return total


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 22), b''):
            h.update(block)
    return h.hexdigest()


def main():
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--config', default=str(here / 'trim.json'))
    ap.add_argument('--out', help='write here instead of the config\'s "out" (beside the config)')
    ap.add_argument('--check', action='store_true', help='say what would be kept, write nothing')
    a = ap.parse_args()
    cfg_path = Path(a.config)
    cfg = json.load(open(cfg_path))
    base = cfg_path.parent if not cfg.get('base') else (cfg_path.parent / cfg['base']).resolve()
    src = Source(base / cfg['source'])
    asm = src.assembly()
    if not np.allclose(src.world(asm), np.eye(4)):
        raise SystemExit('the assembly node is not at the origin: grafts would need its inverse (not handled)')
    tops = {src.nodes[c].get('name'): c for c in src.nodes[asm].get('children', [])}
    keep = cfg['keep']
    missing = [k for k in keep if k not in tops]
    if missing:
        raise SystemExit(f'not top-level instances of {cfg["source"]}: {missing}')
    if len(set(keep)) != len(keep):
        raise SystemExit('trim.json keep lists an instance twice')
    w = Writer()
    root = {k: v for k, v in src.nodes[asm].items() if k != 'children'}
    w.out['nodes'].append(root)
    kids, rows = [], []
    for name in [n for n in tops if n in keep]:                 # (the source's order)
        rep = dict(meshes=0, verts=0, dropped=[], renamed=[])
        kids.append(w.subtree(src, tops[name], drop=set(cfg.get('drop', {}).get(name, [])), rename=cfg.get('rename', {}).get(name), report=rep))
        for d in cfg.get('drop', {}).get(name, []):
            if d not in rep['dropped']:
                raise SystemExit(f'drop {name}/{d}: no such node directly under {name}')
        for r in cfg.get('rename', {}).get(name, {}):
            if r not in rep['renamed']:
                raise SystemExit(f'rename {name}: it has no mesh called {r!r}')
        rows.append((name, rep))
    for gname, g in cfg.get('graft', {}).items():
        if gname in tops:
            raise SystemExit(f'graft {gname}: that name is already a part of {cfg["source"]}')
        other = Source((base / g['glb']).resolve())
        hits = [i for i, n in enumerate(other.nodes) if n.get('name') == g['node']]
        if len(hits) != 1:
            raise SystemExit(f'graft {gname}: {len(hits)} nodes called {g["node"]} in {g["glb"]}')
        P = pose_matrix(g.get('pose'))
        P[:3, 3] /= 1000.0                                      # (poses are in mm, the export in metres)
        rep = dict(meshes=0, verts=0, dropped=[], renamed=[])
        kids.append(w.subtree(other, hits[0], top_matrix=P @ other.world(hits[0]), top_name=gname, report=rep))
        rows.append((gname + f' (from {Path(g["glb"]).name} {g["node"]})', rep))
    root['children'] = kids
    total_v = sum(r['verts'] for _, r in rows)
    for name, r in rows:
        extra = (f"; left out {', '.join(r['dropped'])}" if r['dropped'] else '') + (f"; renamed {', '.join(r['renamed'])}" if r['renamed'] else '')
        print(f'  {name}: {r["meshes"]} meshes, {r["verts"]} vertices{extra}')
    extras = dict(trimmed_from=cfg['source'], source_bytes=src.path.stat().st_size, source_sha256=None if a.check else sha256(src.path),
                  config=cfg_path.name, keep=len(keep), graft=list(cfg.get('graft', {})))
    out = None if a.check else (Path(a.out) if a.out else base / cfg['out'])
    size = w.write(out, extras)
    print(f'{len(rows)} parts, {total_v} vertices, {w.refs} accessors stored as {len(w.out["accessors"])}: '
          f'{size / 1e6:.1f} MB' + ('' if out is None else f' written to {out}') + f' (source {src.path.stat().st_size / 1e6:.0f} MB)')


if __name__ == '__main__':
    main()
