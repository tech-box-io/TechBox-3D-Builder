"""A path search for the buzzer's seated leads through every state the case passes through from Step 43c to the end (parts
as posed in each view, the switch on its way down, every other wire at rest and at 41 moments of every motion), forced over
the black, green, purple and blue jumpers (the columns under them are closed)."""
import json, sys, heapq, itertools
import numpy as np
from scipy.spatial import cKDTree
from field import *
import design as D
PITCH = float(sys.argv[1]) if len(sys.argv) > 1 else 0.75
NEED, PREF, K = 0.35, 1.6, 4.0
LO, HI = np.array([655.0, 886.0, 1228.0]), np.array([705.0, 945.0, 1345.0])
shape = tuple((np.ceil((HI - LO) / PITCH)).astype(int) + 1)
G = np.stack(np.meshgrid(*[LO[k] + np.arange(shape[k]) * PITCH for k in range(3)], indexing='ij'), -1).reshape(-1, 3)
# ---- parts, every pose they take from Step 43c on (and the switch and F4 on their way down, Step 48)
seen = {}
i0 = ORDER.index('Step 43c')
for view in ORDER[i0:]:
    for pid, off in near_parts(view):
        seen[(pid, json.dumps(off))] = (pid, off)
for dy in (10.0, 20.0, 30.0, 40.0):
    for pid in ('NAUO46',):
        seen[(pid, str(dy))] = (pid, [0.0, dy, 0.0])
seen[('NAUO62', 'null')] = ('NAUO62', None)
dpart = np.full(len(G), 12.0)
for (pid, _), (_, off) in seen.items():
    sp, sn = part_samples(pid)
    if not len(sp): continue
    if off is not None:
        sp = apply_pose(off, sp); sn = apply_pose(off, sn) - apply_pose(off, np.zeros((1, 3)))
    lo, hi = np.array(B[pid][0]), np.array(B[pid][1])
    c = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
    if off is not None: c = apply_pose(off, c)
    t = cKDTree(sp)
    dk, kk = t.query(G, k=5, distance_upper_bound=12.0)
    d = np.where(np.isfinite(dk[:, 0]), dk[:, 0], 12.0)
    inbox = np.all((G > c.min(0)) & (G < c.max(0)), axis=1)
    votes = np.zeros(len(G))
    for m in range(5):
        ok = np.isfinite(dk[:, m])
        votes[ok] += np.where(np.einsum('ij,ij->i', G[ok] - sp[kk[ok, m]], sn[kk[ok, m]]) < 0, 1, -1)
    inside = inbox & (votes >= 3)
    dpart = np.minimum(dpart, np.where(inside, -d, d))
    del t, dk, kk
print('parts', len(seen), flush=True)
# ---- wires: every other wire at rest in every view from 43c, and at 41 moments of each motion after it
M = np.load('moving.npz')
wp, wr = [M['p'].astype(float)], [M['r'].astype(float)]
for view in ORDER[i0:]:
    for w, ri in VIEWS[view]['wires'].items():
        if 'buzzer' in w: continue
        q, _, _ = dense(S['routes'][ri]['pts'], 0.3)
        wp.append(q); wr.append(np.full(len(q), RAD[w]))
wp, wr = np.vstack(wp), np.concatenate(wr)
sel = np.all((wp > LO - 4) & (wp < HI + 4), axis=1)
wp, wr = wp[sel], wr[sel]
wp, idx = np.unique(np.round(wp, 1), axis=0, return_index=True); wr = wr[idx]
t2 = cKDTree(wp); d2, k2 = t2.query(G, distance_upper_bound=12.0)
dwire = np.where(np.isfinite(d2), d2 - wr[np.minimum(k2, len(wr) - 1)], 12.0)
print('wire points', len(wp), flush=True)
clear = (np.minimum(dpart, dwire) - 0.625).reshape(shape)
# ---- the columns under the four jumpers closed
Z = []
for w in ('jumper black', 'jumper green', 'jumper purple', 'jumper blue'):
    q, _, _ = dense(S['routes'][VIEWS['Step 43c']['wires'][w]]['pts'], 0.3)
    q = q[q[:, 1] > 903.0]                                     # (not their straight drops into the holes)
    Z.append(q)
Z = np.vstack(Z)
t3 = cKDTree(Z[:, [0, 2]])
cols = G.reshape(shape + (3,))[:, 0, :, :][:, :, [0, 2]].reshape(-1, 2)
nb = t3.query_ball_point(cols, r=2.2)
ymax = np.array([Z[n, 1].max() if n else -1e9 for n in nb]).reshape(shape[0], shape[2])
under = G.reshape(shape + (3,))[..., 1] < ymax[:, None, :]
np.save('field_clear.npy', clear.astype(np.float32)); np.save('field_under.npy', under)
json.dump(dict(lo=LO.tolist(), hi=HI.tolist(), pitch=PITCH, shape=[int(s) for s in shape]), open('field_meta.json', 'w'))
print('saved', shape, flush=True)
