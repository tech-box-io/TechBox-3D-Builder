"""Close-up sections of the joints: in the mid-plane of one plate, a 0.1 mm grid coloured by which parts are there
(tan = the plate cut, blue = the other part(s), red = both). One crop per joint, with world coordinates on the edges."""
import sys, json, numpy as np, trimesh
from PIL import Image, ImageDraw
SP = sys.argv[1]
d = np.load(SP + '/wood.npz'); P = json.load(open(SP + '/wood_planes.json'))
M = {}
for k in d.files:
    if k.endswith('__V'):
        i = k[:-3]; m = trimesh.Trimesh(d[i + '__V'], d[i + '__F'], process=True); m.merge_vertices(); M[i] = m
def midc(i):
    n = np.array(P[i]['normal']); t = d[i + '__V'] @ n; return n, (t.min() + t.max()) / 2
AX = {'X': [1, 0, 0], 'Y': [0, 1, 0], 'Z': [0, 0, 1], 'S': [0.643, 0.766, 0], 'T': [-0.766, 0.643, 0]}
# (label, plate cut, other parts, centre (assembly mm, projected onto the plate's mid-plane), right axis, up axis, half-width, half-height)
J = [
 ('H14 (section in H14; up = up its slope)', 'NAUO74', ['NAUO62', 'NAUO77', 'NAUO75'], [560, 984.2, 1290.5], 'Z', 'S', 40, 32),
 ('H13 (section in H13; up = (0.766,-0.643,0))', 'NAUO75', ['NAUO62', 'NAUO77', 'NAUO73', 'NAUO74'], [581.6, 967, 1290.5], 'Z', 'T', 36, 24),
 ('H11 top, zoom (section in H11)', 'NAUO62', ['NAUO74', 'NAUO75'], [565, 990, 1310], 'X', 'Y', 14, 17),
 ('H2 front tab in H1', 'NAUO65', ['NAUO63'], [462, 898.6, 1358.7], 'X', 'Y', 9, 10),
 ('H3 front tab in H1', 'NAUO66', ['NAUO63'], [462, 898.6, 1222.2], 'X', 'Y', 9, 10),
 ('H2 rear tabs in H4', 'NAUO65', ['NAUO73'], [590, 910, 1358.7], 'X', 'Y', 9, 22),
 ('H2 top tab in H10', 'NAUO65', ['NAUO64'], [535, 932, 1358.7], 'X', 'Y', 10, 8),
 ('H2 windows: H5 H6 H7', 'NAUO65', ['NAUO67', 'NAUO60', 'NAUO68'], [525, 899, 1358.7], 'X', 'Y', 36, 8),
 ('H3 notches: H5 H6 H7', 'NAUO66', ['NAUO67', 'NAUO60', 'NAUO68'], [525, 899, 1222.2], 'X', 'Y', 36, 8),
 ('H5 tongue in H4 (section in H4)', 'NAUO73', ['NAUO67', 'NAUO68', 'NAUO60'], [588.9, 900, 1290.5], 'Z', 'Y', 30, 13),
 ('H10 rear tabs in H4 (section in H10)', 'NAUO64', ['NAUO73'], [592, 932.6, 1290.5], 'Z', 'X', 52, 9),
 ('H4 at H10 tabs (section in H4)', 'NAUO73', ['NAUO64', 'NAUO62', 'NAUO77', 'NAUO75'], [588.9, 945, 1290.5], 'Z', 'Y', 52, 26),
 ('key tab in H4 (section in key)', 'NAUO72', ['NAUO73'], [588, 914.9, 1240.5], 'Z', 'X', 9, 9),
 ('key in H8 (section in key)', 'NAUO72', ['NAUO61'], [541, 914.9, 1240.5], 'Z', 'X', 18, 8),
 ('H8 tabs in H5 (section in H8)', 'NAUO61', ['NAUO67', 'NAUO69', 'NAUO70', 'NAUO71', 'NAUO72', 'NAUO62', 'NAUO77', 'NAUO64'], [541.1, 916, 1290.5], 'Z', 'Y', 70, 18),
 ('H11 in H10, H8, H4, H13, H14 (section in H11)', 'NAUO62', ['NAUO64', 'NAUO61', 'NAUO73', 'NAUO75', 'NAUO74'], [558, 967, 1310], 'X', 'Y', 38, 41),
 ('H12 in H10, H8, H4, H13, H14 (section in H12)', 'NAUO77', ['NAUO64', 'NAUO61', 'NAUO73', 'NAUO75', 'NAUO74'], [558, 967, 1271], 'X', 'Y', 38, 41),
]
S = 10.0
ONLY = [int(x) for x in sys.argv[2:]] if len(sys.argv) > 2 else None
for k, (label, cut, others, c, ra, ua, hw, hh) in enumerate(J):
    if ONLY is not None and k not in ONLY: continue
    n, lev = midc(cut)
    r = np.array(AX[ra], float); u = np.array(AX[ua], float)
    r -= (r @ n) * n; r /= np.linalg.norm(r); u -= (u @ n) * n; u -= (u @ r) * r; u /= np.linalg.norm(u)
    c = np.array(c, float); c = c + (lev - c @ n) * n
    xs = np.arange(-hw, hw, 1 / S); ys = np.arange(-hh, hh, 1 / S)
    X, Y = np.meshgrid(xs, ys)
    pts = c + X.reshape(-1, 1) * r + Y.reshape(-1, 1) * u
    a = M[cut].contains(pts)
    b = np.zeros(len(pts), bool)
    for o in others:
        lo, hi = M[o].bounds
        near = np.all((pts >= lo - 0.1) & (pts <= hi + 0.1), axis=1)
        if near.any():
            bb = np.zeros(len(pts), bool); bb[near] = M[o].contains(pts[near]); b |= bb
    img = np.full((len(ys), len(xs), 3), 255, np.uint8)
    A = a.reshape(X.shape); Bm = b.reshape(X.shape)
    img[A & ~Bm] = (210, 170, 110); img[Bm & ~A] = (90, 140, 220); img[A & Bm] = (230, 30, 30)
    img = img[::-1]
    im = Image.fromarray(img).resize((len(xs) * 2 // 2, len(ys) * 2 // 2))
    canvas = Image.new('RGB', (im.width + 20, im.height + 46), 'white'); canvas.paste(im, (10, 34))
    dr = ImageDraw.Draw(canvas)
    p_lo = c - hw * r - hh * u
    dr.text((10, 2), f'{label}', fill='black')
    dr.text((10, 16), f'right={ra}: {c @ AX[ra] - hw:.1f}..{c @ AX[ra] + hw:.1f}  up={ua}: {c @ AX[ua] - hh:.1f}..{c @ AX[ua] + hh:.1f}  (1 px = 0.1 mm)', fill='black')
    canvas.save(f'{SP}/sec2_{k:02d}.png' if ONLY is not None else f'{SP}/sec_{k:02d}.png')
    print(k, label, canvas.size, 'overlap px', int((A & Bm).sum()))
