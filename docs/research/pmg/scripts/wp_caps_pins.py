"""Pass 3: every Dupont cap (Wire Cap 8 mm, Wire Cap V2 12 mm) with its axis and two end faces, and the pins of every device pose
(I/O module NAUO1/78/94: G V S rows; buttons; display; matrix), all in assembly mm. Writes scratchpad caps_pins.json."""
import sys, json
import numpy as np
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from wp_glb import Glb, node_matrix
from wp_components import GLB

SP = '/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/bc7f208e-dd24-481f-9696-6a220688eb27/scratchpad/'
G = Glb(GLB); d = G.doc; T = G.top()


def world_of(inst):
    return G.rootM @ node_matrix(d['nodes'][T[inst]])


def carry(p_mm, src, dst):
    """A point of instance `src` (assembly mm) where the same point of instance `dst` is (same part, other pose)."""
    M = world_of(dst) @ np.linalg.inv(world_of(src))
    p = np.c_[np.atleast_2d(p_mm) / 1000.0, np.ones(len(np.atleast_2d(p_mm)))] @ M.T
    return p[:, :3] * 1000.0


def verts(inst, mesh_filter=None):
    out = []
    for name, Wm, prims, ni in G.meshes_of(T[inst]):
        if mesh_filter and not mesh_filter(name):
            continue
        for p in prims:
            v = G.acc(p['attributes']['POSITION']).astype(np.float64)
            out.append((name, (np.c_[v, np.ones(len(v))] @ Wm.T)[:, :3] * 1000.0))
    return out


caps = {}
for inst, node in T.items():
    ms = G.meshes_of(node)
    if len(ms) == 1 and ms[0][0].startswith('Wire Cap'):
        V = verts(inst)[0][1]
        c = (V.min(0) + V.max(0)) / 2
        u, s, vt = np.linalg.svd(V - V.mean(0), full_matrices=False)
        ax = vt[0] / np.linalg.norm(vt[0])
        ax = np.round(ax, 4)
        proj = (V - c) @ ax
        cc = c + ax * (proj.max() + proj.min()) / 2           # centre along the axis
        half = (proj.max() - proj.min()) / 2
        # the body's middle across the axis: mean of the extreme cross-section box
        caps[inst] = dict(kind=ms[0][0], centre=np.round(cc, 3).tolist(), axis=ax.tolist(), length_mm=round(2 * half, 2),
                          face_plus=np.round(cc + ax * half, 3).tolist(), face_minus=np.round(cc - ax * half, 3).tolist())

# --- the I/O module's pins (NAUO1, then carried to NAUO78 and NAUO94)
mod_pins = {}
hdr = verts('NAUO1', lambda n: n.startswith('Samtec-TLW-104') or n.startswith('Samtec-TLW-108'))
col = {'_N': 'G', '_R': 'V', '_B': 'S'}
digital = {}
for name, V in hdr:
    suf = name[-2:]
    if suf not in col:
        continue
    lo, hi = V.min(0), V.max(0)
    top = V[V[:, 1] > hi[1] - 0.01]                   # the pin tops (pins point +y)
    zs = np.unique(np.round(top[:, 2], 1))
    # pin tops are small squares: cluster by z
    groups = []
    for z in sorted(top[:, 2]):
        if not groups or z - groups[-1][-1] > 1.0:
            groups.append([z])
        else:
            groups[-1].append(z)
    xs = top[:, 0]
    for g in groups:
        sel = (top[:, 2] >= g[0] - 1e-6) & (top[:, 2] <= g[-1] + 1e-6)
        p = top[sel].mean(0)
        side = 'digital' if name.startswith('Samtec-TLW-104') else 'analogue'
        digital.setdefault((side, col[suf]), []).append(np.round(p, 3))
rows_d = ['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'GND_row', 'AREF_row']
rows_a = ['A7', 'A6', 'A5', 'A4', 'A3', 'A2', 'A1', 'A0']       # (A0 at the USB end, +z, as on the MRA)
for (side, c), pts in digital.items():
    pts = sorted(pts, key=lambda p: p[2])                       # -z (far from USB) to +z (USB end)
    names = rows_d if side == 'digital' else rows_a
    assert len(pts) == len(names), (side, c, len(pts))
    for nm, p in zip(names, pts):
        mod_pins[f'{nm} {c}'] = p
pins = {'NAUO1': {k: v.tolist() for k, v in mod_pins.items()}}
for other in ('NAUO78', 'NAUO94'):
    pins[other] = {k: np.round(carry(v, 'NAUO1', other)[0], 3).tolist() for k, v in mod_pins.items()}
pin_dir = {'NAUO1': [0, 1, 0]}
for other in ('NAUO78', 'NAUO94'):
    R = (world_of(other) @ np.linalg.inv(world_of('NAUO1')))[:3, :3]
    pin_dir[other] = np.round(R @ [0, 1, 0], 4).tolist()

# --- buttons: the three right-angle pins (Socket_Blok), tips at the far end of the leg that the cap goes on
btn = {}
for inst in ['NAUO4', 'NAUO5', 'NAUO6', 'NAUO7']:
    sb = [V for n, V in verts(inst, lambda n: n == 'Socket_Blok')]
    tips = []
    for V in sb:
        lo = V.min(0)
        tip = V[V[:, 1] < lo[1] + 0.01].mean(0)               # bench pose: the leg points -y
        tips.append(np.round(tip, 3))
    tips = np.unique(np.round(np.array(tips), 2), axis=0)    # (one Socket_Blok mesh is duplicated in the CAD)
    btn[inst] = sorted(tips.tolist(), key=lambda p: p[2])    # -z to +z
ref_btn = np.array(btn['NAUO7'])
for case_btn in ('NAUO76', 'NAUO83', 'NAUO84', 'NAUO85'):
    btn[case_btn] = np.round(carry(ref_btn, 'NAUO7', case_btn), 3).tolist()
# --- display pins (single mesh): the pin tips at the +z end in the bench pose NAUO80
V = verts('NAUO80')[0][1]
hi = V.max(0)
top = V[V[:, 2] > hi[2] - 0.01]
groups = []
for y in sorted(top[:, 1]):
    if not groups or y - groups[-1][-1] > 1.3:
        groups.append([y])
    else:
        groups[-1].append(y)
disp = [np.round(top[(top[:, 1] >= g[0] - 1e-6) & (top[:, 1] <= g[-1] + 1e-6)].mean(0), 3).tolist() for g in groups]
# --- matrix header pins (NAUO44, mesh '90 5xHeader Pins'): tips at max z
V = [v for n, v in verts('NAUO44', lambda n: n.startswith('90 5xHeader'))][0]
hi = V.max(0)
top = V[V[:, 2] > hi[2] - 0.01]
groups = []
for y in sorted(top[:, 1]):
    if not groups or y - groups[-1][-1] > 1.3:
        groups.append([y])
    else:
        groups[-1].append(y)
mat = [np.round(top[(top[:, 1] >= g[0] - 1e-6) & (top[:, 1] <= g[-1] + 1e-6)].mean(0), 3).tolist() for g in groups]

disp_all = {'NAUO80': disp}
for o in ('NAUO79', 'NAUO129'):
    disp_all[o] = np.round(carry(np.array(disp), 'NAUO80', o), 3).tolist()
mat_all = {'NAUO44': mat}
for o in ('NAUO81', 'NAUO82', 'NAUO267'):
    mat_all[o] = np.round(carry(np.array(mat), 'NAUO44', o), 3).tolist()
dirs = {}
for ref, others, v in (('NAUO7', ('NAUO4', 'NAUO5', 'NAUO6', 'NAUO76', 'NAUO83', 'NAUO84', 'NAUO85'), [0, -1, 0]),
                       ('NAUO80', ('NAUO79', 'NAUO129'), [0, 0, 1]), ('NAUO44', ('NAUO81', 'NAUO82', 'NAUO267'), [0, 0, 1])):
    dirs[ref] = v
    for o in others:
        dirs[o] = np.round((world_of(o) @ np.linalg.inv(world_of(ref)))[:3, :3] @ v, 4).tolist()
plugs = {}
for inst in ('NAUO278', 'NAUO279', 'NAUO280', 'NAUO281', 'NAUO282', 'NAUO283'):
    V = verts(inst)[0][1]
    plugs[inst] = np.round((V.min(0) + V.max(0)) / 2, 3).tolist()
devices = dict(buttons=btn, displays=disp_all, matrices=mat_all, pin_dirs=dirs)
print('module pin dir', pin_dir)
print('D4 G/V/S', pins['NAUO1']['D4 G'], pins['NAUO1']['D4 V'], pins['NAUO1']['D4 S'], '78:', pins['NAUO78']['D4 G'], '94:', pins['NAUO94']['D4 G'])
print('buttons', btn); print('dirs', dirs)
print('display', disp_all)
print('matrix', mat_all)
json.dump(dict(plugs=plugs, caps=caps, module_pins=pins, module_pin_dir=pin_dir, devices=devices), open(SP + 'caps_pins.json', 'w'), indent=0)
print(len(caps), 'caps')
