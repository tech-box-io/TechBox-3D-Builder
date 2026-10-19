"""Section in a bracket's plane (H11 at z 1310, or H12 at z 1271) showing the wood (filled) and the electronics cut by the same
plane (outlines: display NAUO79 green, matrix NAUO81 purple, I/O module NAUO78 orange), 10 px per mm."""
import sys, json, numpy as np, trimesh
from PIL import Image, ImageDraw
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from pmglib import Glb
SP, zc, x0, x1, y0, y1, out = sys.argv[1], float(sys.argv[2]), *map(float, sys.argv[3:7]), sys.argv[7]
d = np.load(SP + '/wood.npz')
W = {}
for k in d.files:
    if k.endswith('__V'):
        i = k[:-3]; m = trimesh.Trimesh(d[i + '__V'], d[i + '__F'], process=True); m.merge_vertices(); W[i] = m
g = Glb('/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions/pmg.glb')
S = 10.0
xs = np.arange(x0, x1, 1 / S); ys = np.arange(y0, y1, 1 / S)
X, Y = np.meshgrid(xs, ys); pts = np.stack([X.ravel(), Y.ravel(), np.full(X.size, zc)], 1)
img = np.full((len(ys), len(xs), 3), 255, np.uint8)
COL = {'NAUO62': (210, 170, 110), 'NAUO77': (210, 170, 110), 'NAUO74': (150, 110, 60), 'NAUO75': (180, 140, 80), 'NAUO64': (190, 150, 90),
       'NAUO73': (170, 130, 70), 'NAUO61': (200, 160, 100)}
for i, m in W.items():
    lo, hi = m.bounds
    if zc < lo[2] - 0.1 or zc > hi[2] + 0.1: continue
    near = np.all((pts[:, :2] >= lo[:2] - 0.1) & (pts[:, :2] <= hi[:2] + 0.1), axis=1)
    if not near.any(): continue
    ins = np.zeros(len(pts), bool); ins[near] = m.contains(pts[near])
    img.reshape(-1, 3)[ins] = COL.get(i, (200, 200, 200))
im = Image.fromarray(img[::-1]); dr = ImageDraw.Draw(im)
def px(p): return ((p[0] - x0) * S, (y1 - p[1]) * S)
for inst, col in (('NAUO79', (0, 160, 0)), ('NAUO81', (140, 0, 170)), ('NAUO78', (240, 120, 0))):
    V, F, _ = g.instance_geometry(inst)
    m = trimesh.Trimesh(V, F, process=False)
    lines = trimesh.intersections.mesh_plane(m, [0, 0, 1], [0, 0, zc])
    for a, b in lines:
        dr.line([px(a), px(b)], fill=col, width=2)
    del m, V, F
canvas = Image.new('RGB', (im.width, im.height + 30), 'white'); canvas.paste(im, (0, 30))
ImageDraw.Draw(canvas).text((4, 4), f'section z={zc}: x {x0}..{x1} (right), y {y0}..{y1} (up); 10 px/mm; display green, matrix purple, module orange', fill='black')
canvas.save(out); print(out, canvas.size)
