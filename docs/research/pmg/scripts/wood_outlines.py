"""Draw each wood plate's outline (union of its faces parallel to the plate) in its own plane, 4 px/mm, with a 10 mm grid and
the world coordinates of the image edges written on it. One PNG per part in the scratch folder, and a sheet."""
import sys, json, numpy as np
from PIL import Image, ImageDraw
SP = sys.argv[1]
d = np.load(SP + '/wood.npz')
P = json.load(open(SP + '/wood_planes.json'))
S = 4.0
FR = {  # image right, image up (world) per part: chosen so the part is seen from outside the case / from above / from the front
    'NAUO63': ([0, 0, 1], [0, 1, 0]),    # H1 seen from the front (-X): right=+Z
    'NAUO65': ([1, 0, 0], [0, 1, 0]),    # H2 seen from +Z
    'NAUO66': ([-1, 0, 0], [0, 1, 0]),   # H3 seen from -Z
    'NAUO73': ([0, 0, -1], [0, 1, 0]),   # H4 seen from behind (+X)
    'NAUO67': ([0, 0, 1], [1, 0, 0]),    # H5 seen from above, front at the bottom
    'NAUO60': ([0, 0, 1], [1, 0, 0]),
    'NAUO68': ([0, 0, 1], [1, 0, 0]),
    'NAUO61': ([0, 0, 1], [0, 1, 0]),    # H8 from the front
    'NAUO69': ([0, 0, 1], [1, 0, 0]),
    'NAUO64': ([0, 0, 1], [1, 0, 0]),
    'NAUO62': ([1, 0, 0], [0, 1, 0]),    # H11 from +Z
    'NAUO77': ([1, 0, 0], [0, 1, 0]),    # H12 from +Z too (so the two brackets compare)
    'NAUO75': ([0, 0, 1], [0.766, -0.643, 0]),   # H13 from above-behind, its long edge horizontal
    'NAUO74': ([0, 0, 1], [0.643, 0.766, 0]),    # H14 from the front-above
}
ims = []
for i, (r, u) in FR.items():
    V, F = d[i + '__V'], d[i + '__F']
    n = np.array(P[i]['normal']); r = np.array(r, float); u = np.array(u, float)
    r -= (r @ n) * n; r /= np.linalg.norm(r); u -= (u @ n) * n; u -= (u @ r) * r; u /= np.linalg.norm(u)
    tri = V[F]
    cr = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]); a = np.linalg.norm(cr, axis=1)
    fn = cr / np.maximum(a[:, None], 1e-12)
    par = np.abs(fn @ n) > 0.99
    p2 = np.stack([V @ r, V @ u], 1)
    lo, hi = p2.min(0) - 6, p2.max(0) + 6
    W, H = int((hi[0] - lo[0]) * S), int((hi[1] - lo[1]) * S)
    img = Image.new('RGB', (W, H + 30), 'white'); dr = ImageDraw.Draw(img)
    for gx in np.arange(np.ceil(lo[0] / 10) * 10, hi[0], 10):
        x = (gx - lo[0]) * S; dr.line([(x, 0), (x, H)], fill=(225, 225, 255))
    for gy in np.arange(np.ceil(lo[1] / 10) * 10, hi[1], 10):
        y = H - (gy - lo[1]) * S; dr.line([(0, y), (W, y)], fill=(225, 225, 255))
    for t in F[par]:
        q = p2[t]
        dr.polygon([((x - lo[0]) * S, H - (y - lo[1]) * S) for x, y in q], fill=(200, 160, 100))
    dr.text((4, H + 4), f"{i} {P[i]['name']}  right={np.round(r,2).tolist()} [{lo[0]+6:.1f}..{hi[0]-6:.1f}]  up={np.round(u,2).tolist()} [{lo[1]+6:.1f}..{hi[1]-6:.1f}]", fill='black')
    img.save(f'{SP}/outline_{i}.png'); ims.append(img)
    print(i, P[i]['name'], img.size)
