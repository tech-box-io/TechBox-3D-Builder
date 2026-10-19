"""Pass 2: the centre line of every wire body in pmg.glb (each body is one round tube: one jumper wire, or a piece of the USB cable).

Method (as the RCC/MRA studies, adapted): every vertex moved in by the radius along its own normal lands on the centre line;
those points are put in order by distance over the mesh from one end, binned every 0.5 mm and averaged, then re-projected onto the
line and binned again (three rounds). Side vertices only (normal across the tube); the two flat end faces give the end points.
radius = mean distance of the side vertices from the final line; check = their spread.
Writes scratchpad wires_raw.json: {instance: {mesh, radius_mm, length_mm, end_a, end_b, dir_a, dir_b, points (1 mm), check}}.
"""
import sys, json
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
from scipy.spatial import cKDTree
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from wp_glb import Glb
from wp_components import wire_instances, GLB
import importlib.util as _iu
_spec = _iu.spec_from_file_location('tool_wires', '/Users/lee-johnson/Desktop/Claude_Cadasio/tools/wires.py')
W = _iu.module_from_spec(_spec); _spec.loader.exec_module(W)          # tools/wires.py (this folder has another wires.py)

OUT = sys.argv[1] if len(sys.argv) > 1 else '/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/bc7f208e-dd24-481f-9696-6a220688eb27/scratchpad/wires_raw.json'


USB_BODIES = ('Copy of Part23', 'Part152', 'Part153')        # the USB cable (4.6 mm across); every other body is a 1.25 mm jumper wire


def mesh_with_normals(G, node):
    V, N, F, base = [], [], [], 0
    for name, Wm, prims, ni in G.meshes_of(node):
        for p in prims:
            v = G.acc(p['attributes']['POSITION']).astype(np.float64)
            n = G.acc(p['attributes']['NORMAL']).astype(np.float64)
            V.append((np.c_[v, np.ones(len(v))] @ Wm.T)[:, :3] * 1000.0)
            R = Wm[:3, :3]
            n = n @ np.linalg.inv(R).T.T if False else n @ R.T
            N.append(n / np.linalg.norm(n, axis=1)[:, None])
            f = G.acc(p['indices']).reshape(-1, 3).astype(np.int64)
            F.append(f + base); base += len(v)
    return np.vstack(V), np.vstack(N), np.vstack(F)


def dense(line, step=0.05):
    p = W.resample(line, step)
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    return p, s


def windowed_nearest(P, step, Q, s_prev, half_mm=6.0, chunk=4000):
    """For each point of Q, the arc position on the dense line P (spacing `step`) nearest to it, searched only within
    half_mm of its previous estimate s_prev (so a wire that doubles back near itself is not confused)."""
    h = int(round(half_mm / step))
    out = np.empty(len(Q))
    dist = np.empty(len(Q))
    for i in range(0, len(Q), chunk):
        q, sp = Q[i:i + chunk], s_prev[i:i + chunk]
        i0 = np.clip(np.round(sp / step).astype(int), 0, len(P) - 1)
        idx = np.clip(i0[:, None] + np.arange(-h, h + 1)[None, :], 0, len(P) - 1)
        d = np.linalg.norm(P[idx] - q[:, None, :], axis=2)
        j = np.argmin(d, axis=1)
        out[i:i + chunk] = idx[np.arange(len(q)), j] * step
        dist[i:i + chunk] = d[np.arange(len(q)), j]
    return out, dist


def binned(svals, pts, width=0.5, min_count=2):
    b = np.floor(svals / width).astype(int)
    order = np.argsort(b, kind='stable')
    b, pts, sv = b[order], pts[order], svals[order]
    ub, start = np.unique(b, return_index=True)
    sums = np.add.reduceat(pts, start, axis=0)
    cnt = np.diff(np.r_[start, len(b)])
    keep = cnt >= min_count
    return (sums / cnt[:, None])[keep], ((ub + 0.5) * width)[keep]


def centre_line(V, N, F, r0=0.62, step=0.05):
    key = np.round(V, 3)
    U, inv = np.unique(key, axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    e = inv[np.r_[F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]]
    e = e[e[:, 0] != e[:, 1]]
    w = np.linalg.norm(U[e[:, 0]] - U[e[:, 1]], axis=1)
    A = coo_matrix((w, (e[:, 0], e[:, 1])), shape=(len(U), len(U))).tocsr()
    d0 = dijkstra(A, directed=False, indices=0)
    a = int(np.argmax(np.where(np.isfinite(d0), d0, -1)))
    s_geo = dijkstra(A, directed=False, indices=a)[inv]
    r = r0
    C = V - r * N
    # first line: bins of the over-the-mesh distance; map that distance to arc length along the first line
    width = 0.5
    b = np.floor(s_geo / width).astype(int)
    ub, start = np.unique(np.sort(b), return_index=True)
    order = np.argsort(b, kind='stable')
    sums = np.add.reduceat(C[order], start, axis=0); cnt = np.diff(np.r_[start, len(b)])
    line = sums / cnt[:, None]
    seg = np.r_[0, np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))]
    s_prev = np.interp(s_geo, (ub + 0.5) * width, seg)
    side = np.ones(len(V), bool)
    for it in range(5):
        P = W.resample(line, step)
        s_new, dist = windowed_nearest(P, step, C, s_prev)
        k = np.clip(np.round(s_new / step).astype(int), 0, len(P) - 1)
        t = np.gradient(P, axis=0); t /= np.linalg.norm(t, axis=1)[:, None]
        side = np.abs(np.einsum('ij,ij->i', N, t[k])) < 0.35
        if it >= 1:
            sv, dv = windowed_nearest(P, step, V[side], s_new[side])
            r = float(np.median(dv))
            C = V - r * N
            s_new, dist = windowed_nearest(P, step, C, s_new)
        line, centres = binned(s_new[side], C[side], 0.5)
        seg = np.r_[0, np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))]
        s_prev = np.interp(s_new, centres, seg)             # the same places, measured along the new line
    P = W.resample(line, step)
    S = np.arange(len(P)) * step
    s_v, _ = windowed_nearest(P, step, V, s_prev)
    k = np.clip(np.round(s_v / step).astype(int), 0, len(P) - 1)
    t = np.gradient(P, axis=0); t /= np.linalg.norm(t, axis=1)[:, None]
    axial = np.abs(np.einsum('ij,ij->i', N, t[k])) > 0.9
    L = S[-1]
    ends = []
    for at in (0, -1):
        sel = axial & ((s_v < 2.0) if at == 0 else (s_v > L - 2.0))
        tt = t[0] if at == 0 else t[-1]
        if sel.sum() >= 3:
            proj = V[sel] @ tt
            ext = proj.min() if at == 0 else proj.max()
            face = V[sel][np.abs(proj - ext) < 0.05]
            ends.append(np.unique(np.round(face, 4), axis=0).mean(0))
        else:
            ends.append(P[at] - tt * 0.0)
    ea, eb = ends
    # the line between the end faces: drop line points behind either face, then add the two face centres
    ta, tb = W._unit(P[min(int(2 / step), len(P) - 1)] - P[0]), W._unit(P[-1] - P[max(-int(2 / step), -len(P))])
    near_a, near_b = S < 3.0, S > L - 3.0                     # (only near each end: a wire may curve back past its own end plane)
    keep = (~near_a | ((P - ea) @ ta > 0.3)) & (~near_b | ((eb - P) @ tb > 0.3))
    mid = P[keep]
    full = np.vstack([ea, mid, eb]) if len(mid) else np.vstack([ea, eb])
    pts = W.resample(full, 1.0)
    Pd = W.resample(full, step)
    s_side, dist = windowed_nearest(Pd, step, V[side], np.clip(s_v[side], 0, (len(Pd) - 1) * step))
    chk = dict(side_vertices=int(side.sum()), min=float(dist.min()), p01=float(np.percentile(dist, 1)), mean=float(dist.mean()),
               p99=float(np.percentile(dist, 99)), max=float(dist.max()))
    dir_a = W._unit(pts[0] - pts[min(3, len(pts) - 1)])           # pointing out of the wire at end a
    dir_b = W._unit(pts[-1] - pts[max(-4, -len(pts))])
    return dict(radius_mm=round(r, 3), length_mm=round(W.length(pts), 2), end_a=np.round(ea, 3).tolist(), end_b=np.round(eb, 3).tolist(),
                dir_a=np.round(dir_a, 4).tolist(), dir_b=np.round(dir_b, 4).tolist(), n_points=len(pts),
                points=np.round(pts, 2).tolist(), check={k_: round(v_, 3) if isinstance(v_, float) else v_ for k_, v_ in chk.items()})


if __name__ == '__main__':
    G = Glb(GLB)
    only = sys.argv[2].split(',') if len(sys.argv) > 2 else None
    res = {}
    for inst, mesh in wire_instances(G):
        if only and inst not in only:
            continue
        V, N, F = mesh_with_normals(G, G.top()[inst])
        usb = mesh in USB_BODIES
        out = centre_line(V, N, F, r0=2.25 if usb else 0.62)
        out = dict(mesh=mesh, **out)
        res[inst] = out
        c = out['check']
        print(inst, mesh, 'r', out['radius_mm'], 'L', out['length_mm'], 'a', np.round(out['end_a'], 1).tolist(), 'b', np.round(out['end_b'], 1).tolist(),
              'chk', c['p01'], c['mean'], c['p99'], c['max'], flush=True)
    json.dump(res, open(OUT, 'w'))
