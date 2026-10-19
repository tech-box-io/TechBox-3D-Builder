"""The PMG's CAD cut down to what the guide shows (pmg-guide.glb), and the measurements guide.py needs (cad-geometry.json).

    .venv.nosync/bin/python "PMG Build Instructions/make_source.py"            after the STEP or this script changes
    .venv.nosync/bin/python "PMG Build Instructions/make_source.py" --check    says what it would write, writes nothing

Why a cut-down source. pmg.glb (167 MB: 6.5 million vertices, from "PMG Full 3D Cadasio Build.STEP" by tools/step_to_glb.py) holds
TechBox's engineer's pose copies of most parts (three I/O modules, two Nanos, eight buttons, three displays, four LED matrices,
three of each USB end), 139 jumper caps and 114 wire and cable bodies. stepgen.Model trimesh-loads the whole source on every
guide.py run (2 - 4 GB for this file), which this Mac cannot afford, and the file is over GitHub's 100 MB limit. The guide needs one
copy of each part, where it sits when the game is built; every other place is a pose of that copy, and the wires are drawn by the
player. pmg-guide.glb holds those parts only (about 17 MB) and is what materials.json and guide.py name. pmg.glb stays on this Mac
(outside git, its checksum in cad-sources.sha256, as the STEP's).

The published guide, not the STEP, where they differ (19 Oct 2026; docs/research/pmg/critic.md, cadasio_map.md section 2). The STEP
is an earlier save of the assembly than the one TechBox's published Cadasio guide (19075-piano_memory_game_pmg-full_build, CAD
version 7) was made from. Where they differ this follows the published guide, which is what students build from today:
  * the I/O module goes on the back panel H4 with the Nano's USB end at the TOP (the STEP has it at the bottom): NAUO78, the caps on
    its pins, the USB plug in its Nano and the Nano are placed as the published project places its module (cadasio-placements.json),
    1.90 mm higher, so that the board's lower edge rests on H5's rear tongue instead of sinking into it (the published project has it
    1.9 mm into the tongue);
  * each push button has three wires (VCC to V, OUT to S, GND to G): the STEP has no cap on V4 - V7 or on a button's GND pin, so four
    caps are copied onto V4 - V7 (from the G caps, moved by the V - G step measured on V9 / G9) and four onto the buttons' GND pins
    (from the OUT caps, moved by the pin step), as new parts CAP_V4 ... CAP_V7 and CAP_GND1 ... CAP_GND4.
Questions for Lee (the README's): whether the STEP is the latest; which way up the module goes; two or three wires per button.

Reused from the MRA (Lee, 19 Oct 2026: "replace each item in the PMG file with the version you used on either the MRA or RCC"):
  * the Nano Board is the MRA's export of the Nano model (mra.glb NAUO126, as the RCC's both Nanos), carried by the transform that
    takes the MRA's I/O module onto the PMG's (measured on the board mesh both files share), as the part NANO; the module's own
    plain Nano (node NAUO301 inside NAUO78) is left out;
  * the I/O module is the MRA's module model already (every mesh the same): its colours, atlas and silkscreen carry over;
  * the USB A end is the MRA's usb-a-end.glb model already (the same vertices); the jumper caps are the MRA's Wire Cap;
  * the USB cable's Mini-B end stays the PMG's own right-angle one: the MRA's is straight, and a part that differs stays the kit's own
    (Lee, 19 Oct 2026, rulebook section 13).
The four button caps are one mesh in the CAD: each is renamed after its colour so that materials.json can colour them apart.
"""
import argparse
import hashlib
import json
import mmap
import struct
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'tools'))
from glbio import node_matrix  # noqa: E402

SOURCE, OUT, GEOMETRY = HERE / 'pmg.glb', HERE / 'pmg-guide.glb', HERE / 'cad-geometry.json'
MRA = ROOT / 'MRA Build Instructions Prototype' / 'mra.glb'
PLACEMENTS = json.load(open(HERE / 'cadasio-placements.json'))
TABLE_Y = 887.79                                          # the case's underside (H4's lowest point): the table
TONGUE_TOP = 902.98                                       # the top of H5's rear tongue, where the I/O module's board rests
PIN_STEP = [-0.02, 0.02, -2.50]                           # a built button's GND pin tip from its OUT pin tip (docs/research/pmg/cad_study.md 5.2)

MODULE = 'NAUO78'                                         # the I/O module on H4 (the STEP's, turned the published way up)
BUTTONS = ['NAUO76', 'NAUO83', 'NAUO84', 'NAUO85']        # black, yellow, white, blue (D4 - D7), left to right for the student
BUTTON_COLOURS = ['black', 'yellow', 'white', 'blue']
DISPLAY, MATRIX = 'NAUO79', 'NAUO81'
USB_B, USB_A = 'NAUO282', 'NAUO283'                       # the right-angle Mini-B end in the Nano; the A end on the table
WOOD = ['NAUO60', 'NAUO61', 'NAUO62', 'NAUO63', 'NAUO64', 'NAUO65', 'NAUO66', 'NAUO67', 'NAUO68', 'NAUO69', 'NAUO70', 'NAUO71', 'NAUO72',
        'NAUO73', 'NAUO74', 'NAUO75', 'NAUO77']
# The caps the STEP has on the built parts' pins (docs/research/pmg/cadasio_map.md 4.4), by pin.
MODULE_CAPS = dict(G4='NAUO97', S4='NAUO96', G5='NAUO95', S5='NAUO99', G6='NAUO98', S6='NAUO100', G7='NAUO102', S7='NAUO101',
                   S8='NAUO111', G9='NAUO114', V9='NAUO113', S9='NAUO112', G11='NAUO117', V11='NAUO116', S11='NAUO115', S12='NAUO118', S13='NAUO119')
BUTTON_CAPS = [dict(VCC='NAUO86', OUT='NAUO87'), dict(VCC='NAUO88', OUT='NAUO89'), dict(VCC='NAUO90', OUT='NAUO91'), dict(VCC='NAUO93', OUT='NAUO92')]
DISPLAY_CAPS = dict(CLK='NAUO259', DIO='NAUO260', VCC='NAUO261', GND='NAUO262')
MATRIX_CAPS = dict(VCC='NAUO134', GND='NAUO135', DIN='NAUO136', CS='NAUO137', CLK='NAUO138')
# The pose copies the guide's poses are measured from (never kept).
BENCH_MODULE, HELD_MODULE = 'NAUO1', 'NAUO94'
BENCH_BUTTONS = ['NAUO7', 'NAUO6', 'NAUO5', 'NAUO4']      # black, yellow, white, blue, standing in a row in front of the bench module
BENCH_DISPLAY = 'NAUO80'
BENCH_USB_A = 'NAUO278'

COMPONENT = {5120: 1, 5121: 1, 5122: 2, 5123: 2, 5125: 4, 5126: 4}
PER_TYPE = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT2': 4, 'MAT3': 9, 'MAT4': 16}


# ---------------------------------------------------------------- reading and writing GLBs without loading them whole
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
        r = self.doc['scenes'][self.doc.get('scene', 0)]['nodes'][0]
        while len(self.nodes[r].get('children', [])) == 1 and 'mesh' not in self.nodes[r]:
            r = self.nodes[r]['children'][0]
        self.asm = r
        self.top = {self.nodes[c].get('name'): c for c in self.nodes[r].get('children', [])}

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
        return rows.tobytes(), view

    def positions(self, mesh_index):
        out = []
        for p in self.doc['meshes'][mesh_index]['primitives']:
            raw, _ = self.accessor_bytes(p['attributes']['POSITION'])
            out.append(np.frombuffer(raw, np.float32).reshape(-1, 3).astype(np.float64))
        return np.concatenate(out)

    def world(self, i):
        """A node's world matrix in mm."""
        m = np.eye(4)
        while i is not None:
            m = node_matrix(self.nodes[i]) @ m
            i = self.parent.get(i)
        return _mm(m)

    def find(self, name, under=None):
        hits = [i for i, n in enumerate(self.nodes) if n.get('name') == name and (under is None or self._under(i, under))]
        if len(hits) != 1:
            raise SystemExit(f'{self.path.name}: {len(hits)} nodes called {name}' + (f' under {self.nodes[under].get("name")}' if under is not None else ''))
        return hits[0]

    def _under(self, i, top):
        while i is not None:
            if i == top:
                return True
            i = self.parent.get(i)
        return False

    def mesh_nodes(self, i, drop=()):
        """[(node, mesh index, world mm)] of node i and everything under it (less the named nodes)."""
        out = []
        n = self.nodes[i]
        if 'mesh' in n:
            out.append((i, n['mesh'], self.world(i)))
        for c in n.get('children', []):
            if self.nodes[c].get('name') not in drop:
                out += self.mesh_nodes(c, drop)
        return out

    def vertices(self, i, drop=()):
        """Every vertex of node i's sub-tree, world mm."""
        return np.concatenate([self.positions(m) * 1000.0 @ W[:3, :3].T + W[:3, 3] for _, m, W in self.mesh_nodes(i, drop)])


def _mm(m):
    m = np.array(m, float)
    m[:3, 3] *= 1000.0
    return m


def _metres(m):
    m = np.array(m, float)
    m[:3, 3] /= 1000.0
    return m


class Writer:
    def __init__(self):
        self.out = dict(asset=dict(version='2.0', generator='TechBox PMG make_source.py'), scene=0, scenes=[dict(nodes=[0])],
                        nodes=[], meshes=[], accessors=[], bufferViews=[], materials=[])
        self.data = bytearray()
        self.by_content = {}                              # identical accessors are stored once (the caps, the four buttons' parts)
        self.materials = {}

    def accessor(self, src, index):
        a = src.doc['accessors'][index]
        raw, view = src.accessor_bytes(index)
        key = (a['componentType'], a['type'], a['count'], a.get('normalized', False), hashlib.sha1(raw).hexdigest())
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

    def subtree(self, src, i, drop=(), rename=None, matrix=None, name=None):
        """Copy node i and its children (less any named in `drop`) under the assembly node: at `matrix` (its world placement, mm)
        if given, else where it is in the source. Returns the new node's index and the number of vertices copied."""
        n = src.nodes[i]
        new = {k: v for k, v in n.items() if k not in ('children', 'mesh', 'matrix', 'translation', 'rotation', 'scale')}
        if name:
            new['name'] = name
        if matrix is not None:
            new['matrix'] = _metres(matrix).T.reshape(-1).tolist()
        else:
            new.update({k: n[k] for k in ('matrix', 'translation', 'rotation', 'scale') if k in n})
        k = len(self.out['nodes'])
        self.out['nodes'].append(new)
        count = 0
        if 'mesh' in n:
            mesh_name = src.doc['meshes'][n['mesh']].get('name')
            new['mesh'] = self.mesh(src, n['mesh'], (rename or {}).get(mesh_name))
            count += src.doc['accessors'][src.doc['meshes'][n['mesh']]['primitives'][0]['attributes']['POSITION']]['count']
        kids = []
        for c in n.get('children', []):
            if src.nodes[c].get('name') in drop:
                continue
            kid, more = self.subtree(src, c, drop, rename)
            kids.append(kid)
            count += more
        if kids:
            new['children'] = kids
        return k, count

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


# ---------------------------------------------------------------- poses (stepgen's form)
def translation(v):
    m = np.eye(4)
    m[:3, 3] = v
    return m


def as_pose(M, at):
    """The 4x4 move M (world to world, mm) as a stepgen pose about the point `at`: [x, y, z] when it only moves."""
    R, at = M[:3, :3], np.asarray(at, float)
    t = M[:3, 3] - (at - R @ at)
    angle = float(np.degrees(np.arccos(np.clip((np.trace(R) - 1) / 2, -1, 1))))
    if angle < 1e-6:
        return np.round(M[:3, 3], 3).tolist()
    if abs(angle - 180) < 1e-4:
        B = (R + np.eye(3)) / 2
        j = int(np.argmax(np.diag(B)))
        axis = B[j] / np.sqrt(B[j, j])
    else:
        axis = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]])
    axis = axis / np.linalg.norm(axis)
    return dict(t=np.round(t, 3).tolist(), r=np.round(axis, 6).tolist() + [round(angle, 4)], at=np.round(at, 3).tolist())


def published(name):
    return np.array(PLACEMENTS[name]['matrix_mm'], float)


def box(V):
    return V.min(0), V.max(0)


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 22), b''):
            h.update(block)
    return h.hexdigest()


# ---------------------------------------------------------------- the PMG
def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--check', action='store_true', help='say what would be written, write nothing')
    args = ap.parse_args()
    src, mra = Source(SOURCE), Source(MRA)
    top = src.top
    W = {name: src.world(top[name]) for name in top}

    # The published way up of the module: the STEP's NAUO78 placed as the published project places its module, then lifted so that
    # the board rests on H5's rear tongue (y 902.98) instead of 1.9 mm into it.
    D = published('Ensamblaje_Shield_NANO-2') @ np.linalg.inv(W[MODULE])
    plain_nano = src.find('NAUO301', under=top[MODULE])
    board = src.vertices(top[MODULE], drop={'NAUO301'}) @ D[:3, :3].T + D[:3, 3]
    tongue = board[(board[:, 0] > 595.0) & (board[:, 0] < 601.2) & (board[:, 2] > 1270.1) & (board[:, 2] < 1320.4)]
    lift = TONGUE_TOP - float(tongue[:, 1].min())
    D = translation([0.0, lift, 0.0]) @ D
    print(f'I/O module: turned the published way up (USB end at the top), lifted {lift:.2f} mm onto H5\'s tongue')

    # The MRA's Nano, carried by the move that takes the MRA's I/O module onto this one (measured on the board mesh both share).
    mra_board = mra.find('NAUO122')                       # 'Shield_Arduino NANO' in mra.glb's NAUO82
    pmg_board = next(i for i, m, _ in src.mesh_nodes(top[MODULE]) if src.doc['meshes'][m].get('name') == 'Shield_Arduino NANO')
    T = src.world(pmg_board) @ np.linalg.inv(mra.world(mra_board))
    a = src.positions(src.nodes[pmg_board]['mesh']) * 1000.0 @ src.world(pmg_board)[:3, :3].T + src.world(pmg_board)[:3, 3]
    b = mra.positions(mra.nodes[mra_board]['mesh']) * 1000.0 @ (T @ mra.world(mra_board))[:3, :3].T + (T @ mra.world(mra_board))[:3, 3]
    if len(a) != len(b) or np.abs(a - b).max() > 0.01:
        raise SystemExit('the MRA module and the PMG module do not share their board mesh: the Nano cannot be placed by it')
    nano_node = mra.find('NAUO126')
    NANO_M = D @ T @ mra.world(nano_node)
    nano_v = mra.positions(mra.nodes[nano_node]['mesh']) * 1000.0 @ NANO_M[:3, :3].T + NANO_M[:3, 3]
    plain_v = src.vertices(plain_nano) @ D[:3, :3].T + D[:3, 3]
    print(f'Nano: the MRA\'s, at {np.round(nano_v.min(0), 2).tolist()} .. {np.round(nano_v.max(0), 2).tolist()} '
          f'(the CAD\'s own plain Nano there: {np.round(plain_v.min(0), 2).tolist()} .. {np.round(plain_v.max(0), 2).tolist()})')

    # The A end lies on the table behind the case, as the published project has it (but on the table, not 3 mm into it).
    a_end = published('USB Cable end-3')
    move = a_end @ np.linalg.inv(W[USB_A])
    a_v = src.vertices(top[USB_A]) @ move[:3, :3].T + move[:3, 3]
    a_end = translation([0.0, TABLE_Y - float(a_v[:, 1].min()), 0.0]) @ a_end

    # What goes into pmg-guide.glb: {name: (source node, world placement or None to keep, mesh renames, nodes left out)}.
    parts = {}
    for name in WOOD + [DISPLAY, MATRIX] + list(DISPLAY_CAPS.values()) + list(MATRIX_CAPS.values()):
        parts[name] = (top[name], None, None, ())
    for k, name in enumerate(BUTTONS):
        parts[name] = (top[name], None, {'Push_Button_Cap.step_По умолчанию': f'Push_Button_Cap {BUTTON_COLOURS[k]}'}, ())
    for caps in BUTTON_CAPS:
        for name in caps.values():
            parts[name] = (top[name], None, None, ())
    parts[MODULE] = (top[MODULE], D @ W[MODULE], None, ('NAUO301',))
    for name in MODULE_CAPS.values():
        parts[name] = (top[name], D @ W[name], None, ())
    parts[USB_B] = (top[USB_B], D @ W[USB_B], None, ())
    parts[USB_A] = (top[USB_A], a_end, None, ())
    # The caps the STEP lacks: V4 - V7 from the G caps moved by the V - G step (V9 cap less G9 cap), GND from the OUT caps moved by
    # the pin step (OUT to GND is 2.5 mm along the button's pin row, -z when built).
    v_step = W[MODULE_CAPS['V9']][:3, 3] - W[MODULE_CAPS['G9']][:3, 3]
    new_caps = {}
    for row in '4567':
        g_cap = MODULE_CAPS[f'G{row}']
        new_caps[f'CAP_V{row}'] = (g_cap, D @ translation(v_step) @ W[g_cap])
    for k, caps in enumerate(BUTTON_CAPS):                  # (by the pins' step, measured on their tips: the caps are seated 0.2 mm apart)
        new_caps[f'CAP_GND{k + 1}'] = (caps['OUT'], translation(PIN_STEP) @ W[caps['OUT']])
    for name, (like, M) in new_caps.items():
        parts[name] = (top[like], M, None, ())
    print(f'V - G step {np.round(v_step, 3).tolist()}; OUT - GND pin step {PIN_STEP}')

    # ---- write the GLB (the source's order, then the new parts)
    w = Writer()
    root = {k: v for k, v in src.nodes[src.asm].items() if k != 'children'}
    w.out['nodes'].append(root)
    kids, total = [], 0
    order = [n for n in top if n in parts] + [n for n in parts if n not in top]
    for name in order:
        node, M, rename, drop = parts[name]
        kid, count = w.subtree(src, node, drop=set(drop), rename=rename, matrix=M, name=name)
        kids.append(kid)
        total += count
    kid, count = w.subtree(mra, nano_node, matrix=NANO_M, name='NANO')
    kids.append(kid)
    total += count
    root['children'] = kids
    extras = dict(made_by='make_source.py', source=SOURCE.name, source_bytes=SOURCE.stat().st_size,
                  source_sha256=None if args.check else sha256(SOURCE), parts=len(kids))
    size = w.write(None if args.check else OUT, extras)
    print(f'{len(kids)} parts, {total} vertices, {len(w.out["accessors"])} accessors: {size / 1e6:.1f} MB'
          + ('' if args.check else f' -> {OUT.name}'))

    # ---- the measurements guide.py needs (cad-geometry.json): every place seated (as built), mm
    seat = {name: (M if M is not None else W[name]) for name, (_, M, _, _) in parts.items()}
    seat['NANO'] = NANO_M

    def middle(name):
        node, M, _, drop = parts[name]
        V = src.vertices(node, set(drop))
        V = V @ (M @ np.linalg.inv(W[name]))[:3, :3].T + (M @ np.linalg.inv(W[name]))[:3, 3] if M is not None else V
        lo, hi = box(V)
        return (lo + hi) / 2, lo, hi

    mids = {}
    for name in [MODULE, DISPLAY, MATRIX, USB_B, USB_A] + BUTTONS:
        c, lo, hi = middle(name)
        mids[name] = dict(middle=np.round(c, 3).tolist(), lo=np.round(lo, 3).tolist(), hi=np.round(hi, 3).tolist())
    mids['NANO'] = dict(middle=np.round((nano_v.min(0) + nano_v.max(0)) / 2, 3).tolist(), lo=np.round(nano_v.min(0), 3).tolist(), hi=np.round(nano_v.max(0), 3).tolist())

    def pose_of(copy_M, built):
        """Where the pose copy is, as a pose of the built part (about its middle)."""
        return as_pose(copy_M @ np.linalg.inv(seat[built]), mids[built]['middle'])

    poses = {
        'module_bench': pose_of(W[BENCH_MODULE], MODULE),
        'module_held': pose_of(translation([0.0, lift, 0.0]) @ published('Ensamblaje_Shield_NANO-3'), MODULE),
        'display_bench': pose_of(W[BENCH_DISPLAY], DISPLAY),
        'display_held': pose_of(published('Display TM1637-6') @ np.linalg.inv(published('Display TM1637-2')) @ seat[DISPLAY], DISPLAY),
        'display_half': pose_of(published('Display TM1637-7') @ np.linalg.inv(published('Display TM1637-2')) @ seat[DISPLAY], DISPLAY),
        'matrix_bench': pose_of(published('LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-1') @ np.linalg.inv(published('LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-4')) @ seat[MATRIX], MATRIX),
        'matrix_held': pose_of(published('LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-8') @ np.linalg.inv(published('LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-4')) @ seat[MATRIX], MATRIX),
        'matrix_half': pose_of(published('LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-9') @ np.linalg.inv(published('LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-4')) @ seat[MATRIX], MATRIX),
        'usb_a_bench': pose_of(W[BENCH_USB_A], USB_A),
    }
    for k, name in enumerate(BUTTONS):
        poses[f'button{k + 1}_bench'] = pose_of(W[BENCH_BUTTONS[k]], name)
    # the bench is the bench module's underside (its lowest point): the bench copies stand on different levels in the CAD
    bench_v = src.vertices(top[BENCH_MODULE])
    bench_y = float(bench_v[:, 1].min())

    # every cap: its device and pin, its middle, the way out of it (from the pin's end to the wire's), its wire end
    caps = {}
    groups = [(MODULE, {**MODULE_CAPS, **{f'V{r}': f'CAP_V{r}' for r in '4567'}})]
    for k, b in enumerate(BUTTONS):
        groups.append((b, {**BUTTON_CAPS[k], 'GND': f'CAP_GND{k + 1}'}))
    groups += [(DISPLAY, DISPLAY_CAPS), (MATRIX, MATRIX_CAPS)]
    for device, pins in groups:
        dev_mid = np.asarray(mids[device]['middle'])
        for pin, cap in pins.items():
            like = new_caps[cap][0] if cap in new_caps else cap
            Ms = seat[cap]
            local = src.positions(src.nodes[top[like]]['mesh']) * 1000.0 if 'mesh' in src.nodes[top[like]] else None
            if local is None:                             # (a cap's mesh may sit one level down)
                (_, m, Wn), = src.mesh_nodes(top[like])
                local = src.positions(m) * 1000.0
                Wl = np.linalg.inv(W[like]) @ Wn
            else:
                Wl = np.eye(4)
            V = local @ (Ms @ Wl)[:3, :3].T + (Ms @ Wl)[:3, 3]
            lo, hi = box(V)
            centre = (lo + hi) / 2
            # its long axis: the principal direction of its vertices
            u, s, vt = np.linalg.svd(V - V.mean(0), full_matrices=False)
            axis = vt[0] / np.linalg.norm(vt[0])
            ends = [centre + axis * 4.0, centre - axis * 4.0]
            out = axis if np.linalg.norm(ends[0] - dev_mid) > np.linalg.norm(ends[1] - dev_mid) else -axis
            proj = (V - centre) @ out
            caps[cap] = dict(device=device, pin=pin, centre=np.round(centre, 3).tolist(), out=np.round(out, 5).tolist(),
                             wire_end=np.round(centre + out * float(proj.max()), 3).tolist(), length=round(float(proj.max() - proj.min()), 3),
                             pin_tip=np.round(centre + out * (float(proj.max()) - 2.2), 3).tolist())
    # the USB cable: where it leaves each end, and the plug's tip and the Nano socket's mouth, built. Measured on the STEP's own
    # copies: the bench set (plug NAUO279, lead NAUO277, A end NAUO278) for where the lead meets each end, the built plug NAUO282 for
    # the plug's metal (fully in the socket: 903.1 - 910.1 mm up, pushed in along +y in the STEP, the module the other way up).
    lead = dict(plug=[655.043, 894.864, 1338.537], plug_in=[0.9999, 0.0001, -0.0146], a=[597.829, 875.376, 1374.07], a_in=[0.0, 0.0, 1.0])   # (along the A end's length: the CAD's lead dips into the table there)
    def carried(M_from, M_to, p, d=None):              # a point (and a direction) on one copy, on another
        X = M_to @ np.linalg.inv(M_from)
        return (X[:3, :3] @ np.asarray(p, float) + X[:3, 3]) if d is None else X[:3, :3] @ np.asarray(d, float)
    V282 = src.vertices(top[USB_B])
    metal = V282[V282[:, 1] > 903.3]
    tip, mouth = [metal[:, 0].mean(), metal[:, 1].max(), metal[:, 2].mean()], [metal[:, 0].mean(), 903.1, metal[:, 2].mean()]
    usb = dict(plug_exit=carried(W['NAUO279'], seat[USB_B], lead['plug']), plug_out=-carried(W['NAUO279'], seat[USB_B], None, lead['plug_in']),
               a_exit=carried(W[BENCH_USB_A], seat[USB_A], lead['a']), a_out=-carried(W[BENCH_USB_A], seat[USB_A], None, lead['a_in']),
               plug_tip=D[:3, :3] @ tip + D[:3, 3], socket_mouth=D[:3, :3] @ mouth + D[:3, 3], plug_in=D[:3, :3] @ [0.0, 1.0, 0.0])
    usb = {k: np.round(v, 4 if k.endswith(('_out', '_in')) else 3).tolist() for k, v in usb.items()}
    geometry = {
        '_about': 'Measured by make_source.py from pmg.glb and cadasio-placements.json; read by guide.py. Assembly mm (Y up, front -X, the '
                  "student's right +Z), every part where it sits when the game is built (pmg-guide.glb). poses: where the pose copies the "
                  "engineer modelled (and the published project's held and half-way copies) are, as stepgen poses of the built part about its "
                  'middle. caps: each jumper cap on its pin, built: its device and pin, middle, out (unit, from the pin end to the wire end), '
                  'wire_end (the middle of the face the wire leaves from), pin_tip (2.2 mm inside the wire end: where a label points).',
        'table_y': TABLE_Y, 'bench_y': round(bench_y, 3), 'module_lift_mm': round(lift, 3),
        'mra_module_to_pmg': np.round(D @ T, 6).tolist(),   # (the MRA's I/O module onto this one: for silkscreen.py)
        'parts': mids, 'poses': poses, 'caps': caps, 'usb': usb,
    }
    if not args.check:
        with open(GEOMETRY, 'w') as f:
            json.dump(geometry, f, indent=1, ensure_ascii=False)
    print(f'cad-geometry.json: {len(poses)} poses, {len(caps)} caps; bench at y {bench_y:.2f}' + (' (not written)' if args.check else ''))


if __name__ == '__main__':
    main()
