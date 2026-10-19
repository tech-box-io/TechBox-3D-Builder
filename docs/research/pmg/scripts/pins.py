"""The pins the PMG's wires go on, in every pose copy (assembly mm), and which way each points.
- I/O module: the MRA's measured pin tops (docs/research/mra/cad_pins.json) carried by the exact MRA -> PMG transforms.
- Buttons: the tip of each right-angle pin (Socket_Blok meshes), named by TechBox's Cadasio labels (Socket-2 VCC, Socket-1 OUT,
  Socket-3 GND: low z to high z on the bench copies).
- Display: the 4 right-angle pins of the one display mesh (CLK, DIO, VCC, GND from the Cadasio labels' anchor points).
- Matrix: the 5 right-angle pins of '90 5xHeader Pins' (VCC, GND, DIN, CS, CLK from -Y to +Y on NAUO44: the Cadasio labels' points on its copy
  'MAX7219-1', which is NAUO44 turned 180 deg about X, fall within 0.2 mm of these pins).
Measured on the bench copies (axis-aligned) and carried to the built and other copies by the exact copy transforms."""
import sys, json, numpy as np
from scipy.spatial.transform import Rotation
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from pmglib import Glb
SP = sys.argv[1]
ROOT = '/Users/lee-johnson/Desktop/Claude_Cadasio/'
g = Glb(ROOT + 'PMG Build Instructions/pmg.glb')
C = json.load(open(SP + '/copies.json')); MC = json.load(open(SP + '/module_compare.json'))
MRA = json.load(open(ROOT + 'docs/research/mra/cad_pins.json'))
def T(pose):
    M = np.eye(4)
    if isinstance(pose, list):
        M[:3, 3] = pose; return M
    ax = np.array(pose['r'][:3]); R = Rotation.from_rotvec(ax / np.linalg.norm(ax) * np.radians(pose['r'][3])).as_matrix()
    at = np.array(pose['at']); M[:3, :3] = R; M[:3, 3] = at - R @ at + np.array(pose['t']); return M
def ap(M, p): return (M[:3, :3] @ np.asarray(p, float) + M[:3, 3]).round(2).tolist()
def ad(M, d):
    v = M[:3, :3] @ np.asarray(d, float); return v.round(3).tolist()
out = {}
# ---- I/O module
Mb = T(MC['MRA NAUO82']['to_PMG_NAUO78_built']); M1 = T(MC['MRA NAUO82']['to_PMG_NAUO1_bench']); M94 = T(MC['MRA NAUO82']['to_PMG_NAUO94_held_above'])
rows = ['D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13']
mod = dict(source='MRA cad_pins.json pin tops (top of each male pin), carried by the exact MRA NAUO82 -> PMG transforms', rows={})
for copy, M in (('NAUO78 built', Mb), ('NAUO1 bench', M1), ('NAUO94 held above', M94)):
    mod.setdefault('pin_direction', {})[copy] = ad(M, [0, 1, 0])
    for r in rows:
        for c in 'GVS':
            mod['rows'].setdefault(r[1:], {}).setdefault(c, {})[copy] = ap(M, MRA['shield']['pins'][r][c])
# USB socket of the Nano, power jack, board plane
mod['board_normal_up_side'] = {k: ad(M, [0, 1, 0]) for k, M in (('NAUO78 built', Mb), ('NAUO1 bench', M1))}
mod['nano_usb_end'] = {k: ad(M, [0, 0, 1]) for k, M in (('NAUO78 built', Mb), ('NAUO1 bench', M1))}
mod['digital_rows_edge'] = {k: ad(M, [-1, 0, 0]) for k, M in (('NAUO78 built', Mb), ('NAUO1 bench', M1))}
mod['row_order_D0_to_D13'] = {k: ad(M, [0, 0, 1]) for k, M in (('NAUO78 built', Mb), ('NAUO1 bench', M1))}
out['io_module'] = mod
for r in ['4', '8', '11', '13']:
    print('module row', r, {c: mod['rows'][r][c] for c in 'GVS'})
print('module pin direction', mod['pin_direction'])
# ---- helpers to read pieces
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
def pieces(inst, meshname):
    res = []
    for i, name, mi, W in g.mesh_nodes(inst):
        if meshname not in (g.meshes[mi].get('name') or ''):
            continue
        V, F = g.mesh_geometry(mi, W)
        key = np.round(V / 1e-3).astype(np.int64)
        _, inv = np.unique(key, axis=0, return_inverse=True); inv = inv.reshape(-1); Fw = inv[F]; n = inv.max() + 1
        r_ = np.concatenate([Fw[:, 0], Fw[:, 1], Fw[:, 2]]); c_ = np.concatenate([Fw[:, 1], Fw[:, 2], Fw[:, 0]])
        nc, lab = connected_components(coo_matrix((np.ones(len(r_)), (r_, c_)), shape=(n, n)), directed=False)
        Vw = np.zeros((n, 3)); Vw[inv] = V
        res.append((name, [Vw[lab == k] for k in range(nc)]))
    return res
# ---- buttons (bench copies are axis-aligned: pins' free legs point -Y, tips at the lowest y)
BTN = {'black': ('NAUO76', 'NAUO7'), 'yellow': ('NAUO83', 'NAUO6'), 'white': ('NAUO84', 'NAUO5'), 'blue': ('NAUO85', 'NAUO4')}
SHIELD_ROW = {'black': '4', 'yellow': '5', 'white': '6', 'blue': '7'}
btn = {}
for colour, (built, bench) in BTN.items():
    tips = []
    for name, ps in pieces(bench, 'Socket_Blok'):
        pin = max(ps, key=lambda P: np.ptp(P[:, 1]))     # the L-shaped pin (9.4 mm tall), not the plastic block
        low = pin[pin[:, 1] < pin[:, 1].min() + 0.05]
        tips.append(low.mean(0))
    tips = np.unique(np.round(tips, 2), axis=0)          # two of the four Socket_Blok meshes coincide
    tips = tips[np.argsort(tips[:, 2])]
    names = ['VCC', 'OUT', 'GND']
    Minv = np.linalg.inv(T(C['button_' + colour][bench]['pose']))   # bench -> built
    e = dict(built=built, bench=bench, shield_row='D' + SHIELD_ROW[colour], pitch_mm=round(float(np.diff(tips[:, 2]).mean()), 2),
             pin_direction={'bench': [0.0, -1.0, 0.0], 'built': ad(Minv, [0, -1, 0])}, pins={})
    for nm, p in zip(names, tips):
        e['pins'][nm] = {'bench': p.round(2).tolist(), 'built': ap(Minv, p)}
    btn[colour] = e
    print('button', colour, e['pins'], e['pin_direction'])
out['buttons'] = btn
# ---- display (bench copy NAUO80)
ps = pieces('NAUO80', 'Display')[0][1]
pins = [P for P in ps if len(P) == 56]                  # the four L-shaped pins
tips = []
for P in pins:
    hi = P[P[:, 2] > P[:, 2].max() - 0.05]; tips.append(hi.mean(0))
tips = np.array(tips); tips = tips[np.argsort(-tips[:, 1])]
names = ['CLK', 'DIO', 'VCC', 'GND']
disp = dict(bench='NAUO80', built='NAUO79', held='NAUO129', shield_rows={'CLK': 'S8', 'DIO': 'S9', 'VCC': 'V9', 'GND': 'G9'}, pins={})
Mi = np.linalg.inv(T(C['display']['NAUO80']['pose'])); M129 = T(C['display']['NAUO129']['pose']) @ Mi
disp['pin_direction'] = {'bench NAUO80': [0, 0, 1], 'built NAUO79': ad(Mi, [0, 0, 1]), 'NAUO129': ad(M129, [0, 0, 1])}
for nm, p in zip(names, tips):
    disp['pins'][nm] = {'bench NAUO80': p.round(2).tolist(), 'built NAUO79': ap(Mi, p), 'NAUO129': ap(M129, p)}
disp['pitch_mm'] = round(float(-np.diff(tips[:, 1]).mean()), 2)
print('display', disp['pins'], disp['pin_direction'])
out['display'] = disp
# ---- matrix (bench copy NAUO44): the mating legs are the pieces 1.83 x 0.66 x 4.61 along Z
ps = pieces('NAUO44', '90 5xHeader')[0][1]
legs = [P for P in ps if 4.4 < np.ptp(P[:, 2]) < 4.8 and np.ptp(P[:, 0]) < 2.5]
tips = np.array([P[P[:, 2] > P[:, 2].max() - 0.05].mean(0) for P in legs]); tips = tips[np.argsort(-tips[:, 1])]
names = ['CLK', 'CS', 'DIN', 'GND', 'VCC']   # top to bottom on NAUO44 (checked against the Cadasio label points on its copy -1, NAUO44 turned 180 deg about X)
mx = dict(bench='NAUO44', built='NAUO81', others=['NAUO82', 'NAUO267'], shield_rows={'VCC': 'V11', 'GND': 'G11', 'DIN': 'S11', 'CS': 'S12', 'CLK': 'S13'}, pins={})
Mi = np.linalg.inv(T(C['matrix']['NAUO44']['pose']))
Mo = {o: T(C['matrix'][o]['pose']) @ Mi for o in ['NAUO82', 'NAUO267']}
mx['pin_direction'] = {'bench NAUO44': [0, 0, 1], 'built NAUO81': ad(Mi, [0, 0, 1])}
for nm, p in zip(names, tips):
    mx['pins'][nm] = {'bench NAUO44': p.round(2).tolist(), 'built NAUO81': ap(Mi, p), **{o: ap(M, p) for o, M in Mo.items()}}
mx['pitch_mm'] = round(float(-np.diff(tips[:, 1]).mean()), 2)
print('matrix', mx['pins'], mx['pin_direction'])
out['matrix'] = mx
json.dump(out, open(SP + '/pins.json', 'w'), indent=1)
