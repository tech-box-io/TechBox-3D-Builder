"""Put the LSM back together: lsm.glb, the kit's CAD export, from Lee's part files placed where TechBox's Cadasio guide has them.

    .venv.nosync/bin/python "LSM Build Instructions/assemble.py"

Lee's STEP files for the kit do not hold a working assembly (19 Oct 2026): LSM_WoodSteps.STEP and LSM_Electronics.STEP have each
part once, laid out loose; "LSM Lab - Full Build.STEP" has parts in place but lacks the Nano, D4 - D10 and the stems, and six of its
sub-assemblies point at files that are missing. TechBox's published Cadasio guide for the kit (instructions.online,
19075-laser_stem_matrix_lsm_-_full_build) holds the whole assembly, and its parts are the same SolidWorks parts in the same
coordinates (each part's own box agrees with Cadasio's to 0.01 mm). So every part is taken from Lee's files in its own frame and put
where Cadasio's assembly has it (docs/research/lsm/cadasio/raw/...json), or, for the parts that go into the breadboard, into the
exact holes the guide names. Converted once with tools/step_to_glb.py (kept out of git, see .gitignore here):
    lsm-wood.glb          <- LSM_WoodSteps.STEP          (the eleven kinds of wood part, D1 - D11)
    lsm-electronics.glb   <- LSM_Electronics.STEP        (LED matrix, breadboard, resistors, capacitor, jumper caps)
    lsm-fullbuild-raw.glb <- LSM Lab - Full Build.STEP   (the push button with its nut, the right-angle Mini-B plug, the backing sheet)
From the MRA (Lee, 19 Oct 2026: use the MRA's or RCC's version of a part where they have it): the Nano Board (mra.glb NAUO126, as the
RCC's Nanos) and the USB cable's A end (usb-a-end.glb; the LSM's "USB Cable end" is the same model). The jumper caps are the MRA's
model already ("Wire Cap"). The LED stems are not in any of the files: each is drawn as the 3.175 x 66.675 x 3.175 mm rod Cadasio's
box gives (a stand-in until the stem's own CAD comes).

Writes lsm.glb (one assembly node, one child per part, named by the ids guide.py uses) and assembly-report.json (where each part
came from, its placement, and how far its box is from Cadasio's).
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

KIT = Path(__file__).resolve().parent
ROOT = KIT.parent
sys.path.insert(0, str(ROOT / 'tools'))
from glbio import GlbWriter, accessor, node_matrix, read_glb  # noqa: E402

PAYLOAD = ROOT / 'docs/research/lsm/cadasio/raw/19075-laser_stem_matrix_lsm_-_full_build.json'
MRA = ROOT / 'MRA Build Instructions Prototype'

# ---------------------------------------------------------------- the breadboard's holes (assembly mm)
# Read from the breadboard's mesh (its hole pockets) placed where Cadasio has it: rows a - j across x, columns 1 - 30 along z.
# The rows and columns match the hole names in the published guide (b19, j5, j16 fall on its caps to 0.03 mm).
ROW_X = dict(zip('abcdefghij', [624.50, 627.04, 629.58, 632.12, 634.66, 642.46, 645.00, 647.54, 650.08, 652.62]))
COL1_Z, PITCH, BOARD_TOP = 1167.91, 2.54, 871.92


def hole(name):
    """The middle of a hole's mouth, e.g. hole('h16')."""
    return np.array([ROW_X[name[0]], BOARD_TOP, COL1_Z + (int(name[1:]) - 1) * PITCH])


# ---------------------------------------------------------------- Cadasio's assembly
def cadasio_placements():
    j = json.load(open(PAYLOAD))
    A = j['assemblyStructure']
    mm = 1.0 / A['scaleFactor']
    refs = {}

    def walk(n, parent):
        r = n['rootReference']
        refs[r['id']] = dict(name=r['name'], parent=parent, t=r['transform'], ver=r['childVersionId'])
        for c in n.get('children') or []:
            walk(c, r['id'])
    walk(A, None)

    def local(k):
        t = refs[k]['t']
        if not t:
            return np.eye(4)
        m = np.array([float(x) for x in t.split(',')]).reshape(4, 4).T
        m[:3, 3] *= mm
        return m

    def world(k):
        m = np.eye(4)
        while k is not None:
            m = local(k) @ m
            k = refs[k]['parent']
        return m
    root = A['rootReference']['id']
    top = {refs[k]['name']: k for k, v in refs.items() if v['parent'] == root}
    boxes = {}
    for name, k in top.items():
        v = A['rootVersions'].get(refs[k]['ver']) or {}
        boxes[name] = world(k)
    return boxes


CAD = cadasio_placements()


def at(name, nudge=(0, 0, 0)):
    """Cadasio's placement of a top-level part (4x4, mm), moved by `nudge` mm (one of the guide's own corrections)."""
    m = CAD[name].copy()
    m[:3, 3] += nudge
    return m


def placement(R, t):
    m = np.eye(4)
    m[:3, :3], m[:3, 3] = R, t
    return m


# The Nano, its plug and the jumper caps take one turn: their own x along the assembly's +z, their own z along -x, y up.
NANO_TURN = np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]], float)
# A male jumper cap standing in a hole: its own z (housing up from the pin) along +y, its own y along -z.
CAP_UP = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], float)

# ---------------------------------------------------------------- sources
SOURCES = {}


def source(path):
    if path not in SOURCES:
        SOURCES[path] = read_glb(path)
    return SOURCES[path]


def mesh_data(path, mesh_name):
    """(positions mm, normals, indices) of the first mesh called mesh_name, in the mesh's own frame."""
    doc, blob = source(path)
    m = next(m for m in doc['meshes'] if m['name'] == mesh_name)
    p = m['primitives'][0]
    return (accessor(doc, blob, p['attributes']['POSITION']).astype(np.float64) * 1000.0,
            accessor(doc, blob, p['attributes']['NORMAL']).astype(np.float64),
            accessor(doc, blob, p['indices']).reshape(-1).astype(np.int64))


def children_of(path, node_name):
    """The meshes under a sub-assembly node, each with its matrix inside the sub-assembly (mm): [(mesh name, 4x4)]."""
    doc, _ = source(path)
    nodes = doc['nodes']
    i = next(k for k, n in enumerate(nodes) if n.get('name') == node_name)
    out = []
    for c in nodes[i].get('children', []):
        m = node_matrix(nodes[c])
        m[:3, 3] *= 1000.0
        if 'mesh' in nodes[c]:
            out.append((doc['meshes'][nodes[c]['mesh']]['name'], m))
    return out


def split(V, N, F):
    """A mesh's solids: [(vertex ids, face rows)] by connected component (welded to 1 micron)."""
    q = np.round(V / 1e-3).astype(np.int64)
    _, first, inv = np.unique(q, axis=0, return_index=True, return_inverse=True)
    inv = inv.reshape(-1)
    T = F.reshape(-1, 3)
    W = inv[T]
    n = len(first)
    e = np.vstack([W[:, [0, 1]], W[:, [1, 2]]])
    k, lab = connected_components(coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(n, n)), directed=False)
    face_lab = lab[W[:, 0]]
    return [np.where(face_lab == c)[0] for c in range(k)]


def sub_mesh(V, N, F, faces):
    T = F.reshape(-1, 3)[faces]
    used, remap = np.unique(T, return_inverse=True)
    return V[used], N[used], remap.reshape(-1)


def box_mesh(size):
    """A rod: an axis-aligned box from the origin to `size` (mm), flat-shaded."""
    sx, sy, sz = size
    V, N, F = [], [], []
    for axis in range(3):
        for side in (0, 1):
            n = np.zeros(3)
            n[axis] = 1 if side else -1
            u, v = [a for a in range(3) if a != axis]
            quad = []
            for du, dv in ((0, 0), (1, 0), (1, 1), (0, 1)):
                p = np.zeros(3)
                p[axis] = size[axis] * side
                p[u], p[v] = size[u] * du, size[v] * dv
                quad.append(p)
            b = len(V)
            V += quad
            N += [n] * 4
            tri = [(0, 1, 2), (0, 2, 3)]
            if np.dot(np.cross(quad[1] - quad[0], quad[2] - quad[0]), n) < 0:
                tri = [(0, 2, 1), (0, 3, 2)]
            F += [b + i for t in tri for i in t]
    return np.array(V), np.array(N), np.array(F)


# ---------------------------------------------------------------- the parts
WOOD, EL, FB = KIT / 'lsm-wood.glb', KIT / 'lsm-electronics.glb', KIT / 'lsm-fullbuild-raw.glb'
parts = {}          # id -> dict(meshes=[(mesh name, V, N, F, 4x4 inside the part)], place=4x4, came=..., cadasio=name)


def add(part_id, meshes, place, came, cadasio=None):
    parts[part_id] = dict(meshes=meshes, place=place, came=came, cadasio=cadasio)


def from_mesh(path, mesh_name, rename=None, main_solid=False):
    V, N, F = mesh_data(path, mesh_name)
    if main_solid:                       # (a wood part: its plate only, without the flat black sheets Cadasio lays in its engraving)
        solids = split(V, N, F)
        V, N, F = sub_mesh(V, N, F, max(solids, key=len))
    return [(rename or mesh_name, V, N, F, np.eye(4))]


def from_sub(path, node_name, only=None, rename=None):
    out = []
    for name, m in children_of(path, node_name):
        if only and name not in only:
            continue
        V, N, F = mesh_data(path, name)
        out.append(((rename or {}).get(name, name), V, N, F, m))
    return out


# wood: D-codes as engraved (Cadasio's tooltips: "Housing Base - Part D1" ...)
for part_id, mesh, inst in [('D1', 'LSM_Bottom_r1', 'LSM_Bottom_r1-1'), ('D2', 'LSM_Side3_r2', 'LSM_Side3_r2-1'),
                            ('D3', 'LSM_Side1_r8', 'LSM_Side1_r8-1'), ('D4', 'LSM_Side2_r2', 'LSM_Side2_r2-1'),
                            ('D5', 'LSM_Side4_r2', 'LSM_Side4_r2-1'), ('D6', 'LSM_Lens_Bottom', 'LSM_Lens_Bottom-3'),
                            ('D7', 'LSM_Lens_Middle', 'LSM_Lens_Middle-2'), ('D8', 'LSM_Lens_Top', 'LSM_Lens_Top-1'),
                            ('D9_A', 'LSM_MatrixSupportLong_r3', 'LSM_MatrixSupportLong_r3-2'),
                            ('D9_B', 'LSM_MatrixSupportLong_r3', 'LSM_MatrixSupportLong_r3-3'),
                            ('D10', 'LSM_MatrixSupportSmall_r2', 'LSM_MatrixSupportSmall_r2-1'),
                            ('D11_A', 'LSM_LensSupport_r2', 'LSM_LensSupport_r2-2'), ('D11_B', 'LSM_LensSupport_r2', 'LSM_LensSupport_r2-3'),
                            ('D11_C', 'LSM_LensSupport_r2', 'LSM_LensSupport_r2-1'), ('D11_D', 'LSM_LensSupport_r2', 'LSM_LensSupport_r2-4')]:
    add(part_id, from_mesh(WOOD, mesh, main_solid=True), at(inst), f'lsm-wood.glb {mesh} (its plate)', inst)
# D4 and D5 centred on the tabs of D2 and D3 (Cadasio has D4 0.19 mm towards D3 and D5 0.22 mm towards D2, so that D2's 3 mm
# tabs bind on the edges of their 3 mm slots; D3 is 3.17 mm thick in the CAD, in 3 mm slots).
parts['D4']['place'][2, 3] += 0.19
parts['D5']['place'][2, 3] -= 0.215
# D8 in line with D6 and D7 (Cadasio has it 0.81 mm towards D3: D6 and D7 fit between D3 and D2 exactly, and so must D8).
parts['D8']['place'][2, 3] += 0.81
# The four shelf posts at one height (Cadasio has two of them 0.6 and 1.0 mm low: they stand on D1 like the other two).
for part_id in ('D11_C', 'D11_D'):
    parts[part_id]['place'][1, 3] = parts['D11_A']['place'][1, 3]

# the breadboard, its backing sheet and the LED matrix: where Cadasio has them (the matrix 0.2 mm across as Cadasio shows it seated)
add('BREADBOARD', from_mesh(EL, 'Breadboard'), at('Breadboard-1'), 'lsm-electronics.glb Breadboard', 'Breadboard-1')
add('BACKING', from_mesh(FB, 'Paper'), at('Paper-1'), 'lsm-fullbuild-raw.glb Paper', 'Paper-1')
add('MATRIX', from_mesh(EL, '8x8 LED'), at('8x8 LED-4', (0.2, 0.0, -0.2)), 'lsm-electronics.glb 8x8 LED', '8x8 LED-4')

# The Nano: the MRA's model (mra.glb NAUO126: its pins 2.54 mm apart along its own x, the two rows at z 0 and -15.24, tips at
# y -8.52, the header's plastic down to y -2.5, the USB socket at the +x end). In rows c and g, columns 2 - 16, USB socket at
# column 16 (Part 1 of the published guide: "Pin D12 - c16"; then D13 is at g16, 5V at g5, GND at g3 and VIN at g2, which is what
# the resistor, capacitor, button and LED matrix wires go to). The plastic sits on the breadboard.
nano_t = np.array([(ROW_X['c'] + ROW_X['g']) / 2 - 7.62, BOARD_TOP + 2.5, hole('c2')[2]])
add('NANO', from_mesh(MRA / 'mra.glb', 'nano_Varsayılan'), placement(NANO_TURN, nano_t), 'mra.glb nano_Varsayılan (the MRA Nano)', 'Arduino Nano V1-1')

# The USB cable's right-angle Mini-B plug, pushed fully into the Nano's socket (its shell's base at the socket's mouth, Nano x 41.18,
# its middle on the socket's, Nano y 2.95, z -7.62), the cable leaving towards D4. The A end lies where Cadasio has it.
plug_t = nano_t + NANO_TURN @ np.array([41.18 + 8.0, 2.95 - 3.75, -7.62])
add('USB_B', from_mesh(FB, 'USB Right Angle'), placement(NANO_TURN, plug_t), 'lsm-fullbuild-raw.glb USB Right Angle', 'USB Right Angle-1')
# The A end lies on the table outside D4, in line with the notch in D4's foot the cable leaves by (z 1219), plug pointing away
# (its own +x, tip to cable, along +x; its own y across, along z): the box stands on its walls' feet, so the table is at y 856.23.
# (Cadasio has it 24 mm below the table.)
TABLE_Y = 856.23
add('USB_A', from_mesh(MRA / 'usb-a-end.glb', 'USBCableend'), placement(np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], float), [520.0 - 134.3, TABLE_Y + 8.4, 1219.0]),
    'MRA usb-a-end.glb', 'USB Cable end-2')

# The resistors and the capacitor: Cadasio's turn, moved so that their legs stand in the holes the guide names. A resistor's legs
# are drawn as wires (they are bent in Steps 4 and 7), so only its body is a part.
def fit_into(part_id, path, node, cad_name, holes, keep, leg_meshes, rename=None):
    meshes = from_sub(path, node, rename=rename)
    place = at(cad_name)
    tips = []
    for name, V, N, F, m in meshes:
        if name in leg_meshes:
            W = (place @ m @ np.c_[V, np.ones(len(V))].T).T[:, :3]
            lo = W[:, 1].min()
            foot = W[W[:, 1] < lo + 0.05]
            tips.append(foot.mean(0))
    tips = sorted(tips, key=lambda p: p[2])
    want = sorted([hole(h) for h in holes], key=lambda p: p[2])
    shift = np.mean(want, 0) - np.mean(tips, 0)
    shift[1] = 0.0                                            # (the height is Cadasio's)
    place = place.copy()
    place[:3, 3] += shift
    add(part_id, [x for x in meshes if x[0] in keep], place, f'{path.name} {node}', cad_name)
    parts[part_id]['legs'] = [((t + shift).round(2).tolist(), h) for t, h in zip(tips, sorted(holes, key=lambda h: hole(h)[2]))]


fit_into('R12K', EL, 'NAUO4', 'Resistor 1-1', ['h3', 'h16'], {'Resistor body 12k'}, {'Resistor stem 3'}, rename={'Resistor body': 'Resistor body 12k'})
fit_into('R330', EL, 'NAUO5', 'Resistor 2-1', ['a11', 'a19'], {'Resistor body 330'}, {'Resistor stem 2'}, rename={'Resistor body': 'Resistor body 330'})
fit_into('CAP', EL, 'NAUO8', 'Capacitor V3-1', ['j2', 'j3'], {'Capacitor body', 'Capacitor leg'}, {'Capacitor leg'})

# The push button and its nut (one mesh in the CAD: its eight solids split, the nut being the 21 x 18 x 1.5 mm one). Where
# Cadasio has it seated on D2, 1 mm out as Cadasio shows it.
V, N, F = mesh_data(FB, 'Push button')
solids = split(V, N, F)
sizes = [np.ptp(V[np.unique(F.reshape(-1, 3)[f])], axis=0) for f in solids]
nut = next(k for k, s in enumerate(sizes) if abs(s[0] - 21.04) < 0.1 and abs(s[2] - 1.5) < 0.05)
button_faces = np.concatenate([f for k, f in enumerate(solids) if k != nut])
# Its flange (radius 8.43 mm, its own z -3.5) against D2's outer face, z 1255.05; the nut (its own z -9.33 to -7.83) screwed up
# against D2's inner face, z 1251.93. (Cadasio's seat leaves the flange 0.46 mm off the face and the nut 0.75 mm off.)
button_place = at('Push button-1', (0.0, 0.0, -0.46))
add('BUTTON', [('Push button', *sub_mesh(V, N, F, button_faces), np.eye(4))], button_place, 'lsm-fullbuild-raw.glb Push button (less its nut)', 'Push button-1')
add('NUT', [('Push button nut', *sub_mesh(V, N, F, solids[nut]), np.eye(4))], at('Push button-1', (0.0, 0.0, 0.75)), 'lsm-fullbuild-raw.glb Push button (its nut)', 'Push button-1')

# Jumper caps. Male ends (a pin under a housing) stand straight up in their holes, pin fully in; the female ends on the LED
# matrix's pins are where Cadasio has them (white V+, purple DIN, grey GND, as Steps 13 - 15 plug them).
VM, NM, FM = mesh_data(EL, 'Wire Cap V2')
mid = np.array([(-1.43 + 0.32) / 2, (-1.66 + 0.09) / 2])           # the cap's middle across (its own x, y)
for part_id, h in [('J_WHITE_M', 'i2'), ('J_GREY_M', 'i3'), ('J_PURPLE_M', 'b19'), ('BTN_RED_PIN', 'j5'), ('BTN_BLACK_PIN', 'j16')]:
    p = hole(h)
    t = np.array([p[0] - mid[0], BOARD_TOP, p[2] + mid[1]])
    add(part_id, [('Wire Cap V2', VM, NM, FM, np.eye(4))], placement(CAP_UP, t), f'lsm-electronics.glb Wire Cap V2, in {h}')
    parts[part_id]['hole'] = h
# (Cadasio has the three 1.38 mm to one side of the matrix's pins and 0.56 mm low: each is put on its pin, the pin's end 2.9 mm in.)
for part_id, inst in [('J_WHITE_F', 'Wire Cap-14'), ('J_PURPLE_F', 'Wire Cap-15'), ('J_GREY_F', 'Wire Cap-16')]:
    add(part_id, from_mesh(EL, 'Wire Cap'), at(inst, (1.385, 0.555, 0.0)), 'lsm-electronics.glb Wire Cap (the MRA jumper cap), on its pin', inst)

# The 64 LED stems, where Cadasio has them (in its order: LSM_Stem-1, then -96 to -158).
STEM = box_mesh((3.175, 66.675, 3.175))
stem_names = sorted([n for n in CAD if n.startswith('LSM_Stem-')], key=lambda n: (CAD[n][2, 3], CAD[n][0, 3]))
for k, inst in enumerate(stem_names, 1):
    # (Cadasio's stems are 0.19 mm across and 0.77 mm along from the middle of D6's and D7's holes; D8's holes are 0.13 mm
    # from theirs once D8 is in line: each stem goes in the middle of the two, which the 3.3 mm holes take with 0.06 mm to spare.)
    add(f'STEM_{k:02d}', [('LSM_Stem', *STEM, np.eye(4))], at(inst, (-0.19, 0.0, 0.835)), 'drawn: Cadasio box of LSM_Stem', inst)


# ---------------------------------------------------------------- write lsm.glb
def main():
    writer = GlbWriter(compress=False)
    nodes = [dict(name='LSM_Assembly', children=[])]
    meshes, mesh_index = [], {}
    report = {}
    for part_id, p in parts.items():
        kids = []
        for name, V, N, F, m in p['meshes']:
            key = (name, V.shape, float(V.sum()))
            if key not in mesh_index:
                pos = writer.add_vertices((V / 1000.0).astype(np.float32), 'VEC3', with_bounds=True)
                nor = writer.add_vertices(N.astype(np.float32), 'VEC3')
                ind = writer.add_indices(F.astype(np.uint32))
                meshes.append(dict(name=name, primitives=[dict(attributes=dict(POSITION=pos, NORMAL=nor), indices=ind)]))
                mesh_index[key] = len(meshes) - 1
            node = dict(name=f'{part_id}:{name}', mesh=mesh_index[key])
            if not np.allclose(m, np.eye(4)):
                mm = m.copy()
                mm[:3, 3] /= 1000.0
                node['matrix'] = mm.T.reshape(-1).tolist()
            nodes.append(node)
            kids.append(len(nodes) - 1)
        place = p['place'].copy()
        place[:3, 3] /= 1000.0
        nodes.append(dict(name=part_id, children=kids, matrix=place.T.reshape(-1).tolist()))
        nodes[0]['children'].append(len(nodes) - 1)
        lo, hi = np.full(3, np.inf), np.full(3, -np.inf)
        for name, V, N, F, m in p['meshes']:
            W = (p['place'] @ m @ np.c_[V, np.ones(len(V))].T).T[:, :3]
            lo, hi = np.minimum(lo, W.min(0)), np.maximum(hi, W.max(0))
        report[part_id] = dict(came=p['came'], cadasio=p.get('cadasio'), lo=lo.round(2).tolist(), hi=hi.round(2).tolist(),
                               **{k: p[k] for k in ('legs', 'hole') if k in p})
    doc = dict(asset=dict(version='2.0', generator='LSM Build Instructions/assemble.py'), scene=0, scenes=[dict(nodes=[0])], nodes=nodes, meshes=meshes)
    size = writer.write(KIT / 'lsm.glb', doc)
    json.dump(report, open(KIT / 'assembly-report.json', 'w'), indent=1)
    print(f'lsm.glb: {len(parts)} parts, {len(meshes)} meshes, {size / 1e6:.1f} MB')


if __name__ == '__main__':
    main()
