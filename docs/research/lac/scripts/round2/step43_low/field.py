"""A clearance field for Step 43's motion: signed distance to every part on screen in Step 43c except the buzzer (posed as there), and
distance to every other wire's surface (static in Step 43), on a grid. Saved to field43.npz."""
import sys, time
import numpy as np
import trimesh
from scipy.spatial import cKDTree
from evalkit import *

LO, HI, PITCH = np.array([636.0, 884.0, 1222.0]), np.array([716.0, 968.0, 1408.0]), 0.5


def build(view='Step 43c', out='field43.npz'):
    t0 = time.time()
    M = model()
    S = load_steps()
    v = {x['name']: x for x in S['views']}[view]
    shape = tuple((np.ceil((HI - LO) / PITCH)).astype(int) + 1)
    axes = [LO[k] + np.arange(shape[k]) * PITCH for k in range(3)]
    dpart = np.full(shape, 10.0, np.float32)
    for i in v['visible']:
        if i in ('NAUO62', 'NAUO58', 'NAUO59'):
            continue
        m = M.inst[i]
        off = v.get('offsets', {}).get(i)
        V = apply_pose(off, np.asarray(m.vertices)) if off is not None else np.asarray(m.vertices)
        lo, hi = V.min(0), V.max(0)
        if np.any(hi < LO - 3) or np.any(lo > HI + 3):
            continue
        mm = trimesh.Trimesh(V, m.faces, process=False)
        n = int(mm.area / 0.3 ** 2) + 200
        sp, f = trimesh.sample.sample_surface(mm, n, seed=1)
        sn = mm.face_normals[f]
        t = cKDTree(sp)
        a0, a1 = [np.clip(np.floor((lo - 10 - LO) / PITCH).astype(int), 0, np.array(shape) - 1), np.clip(np.ceil((hi + 10 - LO) / PITCH).astype(int), 0, np.array(shape) - 1)]
        for a in range(a0[0], a1[0] + 1):
            g = np.stack(np.meshgrid([axes[0][a]], axes[1][a0[1]:a1[1] + 1], axes[2][a0[2]:a1[2] + 1], indexing='ij'), -1).reshape(-1, 3)
            d, k = t.query(g, distance_upper_bound=10.0)
            ok = k < len(sp)
            d = np.where(ok, d, 10.0)
            inbox = np.all((g > lo) & (g < hi), axis=1)
            inside = np.zeros(len(g), bool)
            sel = ok & inbox
            inside[sel] = np.einsum('ij,ij->i', g[sel] - sp[k[sel]], sn[k[sel]]) < -0.3 * d[sel]
            sd = np.where(inside, -d, d).reshape(a1[1] - a0[1] + 1, a1[2] - a0[2] + 1).astype(np.float32)
            blk = dpart[a, a0[1]:a1[1] + 1, a0[2]:a1[2] + 1]
            dpart[a, a0[1]:a1[1] + 1, a0[2]:a1[2] + 1] = np.minimum(blk, sd)
        print(i, len(sp), round(time.time() - t0, 1), flush=True)
    print('parts done', round(time.time() - t0, 1), flush=True)
    W_, R_ = [], []
    for w, ri in v['wires'].items():
        if w.startswith('buzzer'):
            continue
        q = np.asarray(S['routes'][ri]['pts'], float)
        s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(q, axis=0), axis=1))]
        at = np.arange(0, s[-1], 0.2)
        W_.append(np.stack([np.interp(at, s, q[:, k]) for k in range(3)], 1)); R_.append(np.full(len(at), S['wires'][w]['radius']))
        names = None
    wp, wr = np.vstack(W_), np.concatenate(R_)
    widx = np.concatenate([np.full(len(x), i) for i, x in enumerate(W_)])
    wnames = [w for w in v['wires'] if not w.startswith('buzzer')]
    t2 = cKDTree(wp)
    axes = [LO[k] + np.arange(shape[k]) * PITCH for k in range(3)]
    dwire = np.empty(shape, np.float32)
    which = np.empty(shape, np.int16)
    for a in range(shape[0]):
        g = np.stack(np.meshgrid([axes[0][a]], axes[1], axes[2], indexing='ij'), -1).reshape(-1, 3)
        d, k = t2.query(g, distance_upper_bound=10.0)
        ok = k < len(wp)
        dwire[a] = np.where(ok, d - wr[np.minimum(k, len(wp) - 1)], 10.0).reshape(shape[1], shape[2])
        which[a] = np.where(ok, widx[np.minimum(k, len(wp) - 1)], -1).reshape(shape[1], shape[2])
    print('wires done', round(time.time() - t0, 1), flush=True)
    np.savez_compressed(SCR / out, dpart=dpart, dwire=dwire, which=which, lo=LO, pitch=PITCH, wnames=np.array(wnames))


if __name__ == '__main__':
    build()
