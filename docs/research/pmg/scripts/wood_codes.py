"""Find each wood part's engraving pocket (faces 0.254 mm below one face, parallel to it) and render the pocket floor as seen from
outside that face, so the code can be read. Writes codes_raw.json and one PNG per part into the scratch folder."""
import sys, json, numpy as np
from PIL import Image, ImageDraw
SP = sys.argv[1]
d = np.load(SP + '/wood.npz')
P = json.load(open(SP + '/wood_planes.json'))
AX = {'X': np.array([1., 0, 0]), 'Y': np.array([0, 1., 0]), 'Z': np.array([0, 0, 1.])}
res = {}
for i, p in P.items():
    V, F = d[i + '__V'], d[i + '__F']
    n = np.array(p['normal']); n /= np.linalg.norm(n)
    tri = V[F]
    cr = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]); area = np.linalg.norm(cr, axis=1) / 2
    fn = cr / np.maximum(2 * area[:, None], 1e-12)
    h = tri @ n                                  # (nf, 3)
    top, bot = h.max(), h.min()
    par = np.abs(fn @ n) > 0.999
    flat = np.ptp(h, axis=1) < 0.02
    lv = h.mean(1)
    up_pocket = par & flat & (np.abs(lv - (top - 0.254)) < 0.03)
    dn_pocket = par & flat & (np.abs(lv - (bot + 0.254)) < 0.03)
    if up_pocket.sum() >= dn_pocket.sum():
        sel, out_n, face_level = up_pocket, n, top
    else:
        sel, out_n, face_level = dn_pocket, -n, bot
    # all faces belonging to the engraving (floor + walls): engraved region = between face level and floor level, not spanning through
    lo_t, hi_t = h.min(1), h.max(1)
    if out_n @ n > 0:
        walls = (~par) & (lo_t >= top - 0.26) & (hi_t <= top + 0.001) & (np.ptp(h, axis=1) > 0.1)
    else:
        walls = (~par) & (hi_t <= bot + 0.26) & (lo_t >= bot - 0.001) & (np.ptp(h, axis=1) > 0.1)
    fl = tri[sel].reshape(-1, 3)
    lo, hi = fl.min(0), fl.max(0)
    centre_floor = (lo + hi) / 2
    centre_face = centre_floor + out_n * 0.254       # middle of the code on the face itself
    # image frame: up = world Y if in plane, else world -X / +X ... choose the in-plane world axis most perpendicular to n
    cands = [AX['Y'], AX['X'], AX['Z']]
    upv = min(cands, key=lambda a: abs(a @ n))
    upv = upv - (upv @ n) * n; upv /= np.linalg.norm(upv)
    right = np.cross(upv, out_n)
    # raster
    pts2 = np.stack([fl @ right, fl @ upv], 1)
    c2 = (pts2.min(0) + pts2.max(0)) / 2
    S = 40.0
    W = int((np.ptp(pts2[:, 0]) + 4) * S); H = int((np.ptp(pts2[:, 1]) + 4) * S)
    img = Image.new('L', (W, H), 255); dr = ImageDraw.Draw(img)
    for t in tri[sel]:
        q = np.stack([t @ right, t @ upv], 1) - c2
        dr.polygon([(W / 2 + x * S, H / 2 - y * S) for x, y in q], fill=0)
    img.save(f'{SP}/code_{i}.png')
    res[i] = dict(name=p['name'], engraved_face_normal=out_n.round(4).tolist(), n_floor_faces=int(sel.sum()), n_wall_faces=int(walls.sum()),
                  floor_lo=lo.round(2).tolist(), floor_hi=hi.round(2).tolist(), code_centre_on_face=centre_face.round(2).tolist(),
                  image_up=upv.round(4).tolist(), image_right=right.round(4).tolist(), code_size_in_image=[round(float(np.ptp(pts2[:, 0])), 2), round(float(np.ptp(pts2[:, 1])), 2)],
                  face_level=round(float(face_level), 3))
    print(i, p['name'], 'face', out_n.round(3), 'floor faces', int(sel.sum()), 'centre', centre_face.round(2), 'size', res[i]['code_size_in_image'], 'up', upv.round(3), 'right', right.round(3))
json.dump(res, open(SP + '/codes_raw.json', 'w'), indent=1)
