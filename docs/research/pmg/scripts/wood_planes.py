"""Wood parts: exact plate normal (area-weighted over the big faces), the two face planes, flatness, tilt from the nearest axis."""
import sys, json, numpy as np
SP = sys.argv[1]
d = np.load(SP + '/wood.npz')
B = json.load(open(SP + '/wood_basic.json'))
out = {}
for i, b in B.items():
    V, F = d[i + '__V'], d[i + '__F']
    tri = V[F]
    cr = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    area = np.linalg.norm(cr, axis=1) / 2
    n = cr / np.maximum(2 * area[:, None], 1e-12)
    n0 = np.array(b['plate_normal'])
    s = n @ n0
    big = np.abs(s) > 0.99
    # area weighted mean normal (sign aligned)
    nm = (n[big] * np.sign(s[big])[:, None] * area[big][:, None]).sum(0)
    nm /= np.linalg.norm(nm)
    lev = (tri[big] @ nm).mean(1)
    up = s[big] > 0
    hi_lev, lo_lev = lev[up], lev[~up]
    a_up, a_dn = area[big][up], area[big][~up]
    # flatness: spread of vertex heights over each face set (vertices of big faces)
    def spread(sel):
        p = tri[big][sel].reshape(-1, 3) @ nm
        return float(p.min()), float(p.max())
    ax = np.argmax(np.abs(nm)); tilt = float(np.degrees(np.arccos(min(1, abs(nm[ax])))))
    out[i] = dict(name=b['name'], normal=nm.round(5).tolist(), tilt_from_axis_deg=round(tilt, 3), axis='XYZ'[ax],
                  up_face=[round(x, 3) for x in spread(up)], down_face=[round(x, 3) for x in spread(~up)])
    print(i, b['name'], 'n', nm.round(4), 'tilt', round(tilt, 3), 'upface', out[i]['up_face'], 'downface', out[i]['down_face'])
json.dump(out, open(SP + '/wood_planes.json', 'w'), indent=1)
