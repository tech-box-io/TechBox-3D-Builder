"""The PMG's I/O module against the MRA's (NAUO82 in mra.glb) and the RCC's (NAUO23 in rcc.glb): rigid transforms fitted on
meshes that are the same in both files (same name and vertex count, names unique in the module), checked on all the shared
meshes by nearest distance. Also the MRA's single-mesh Nano (NAUO126) against the PMG's loose Nano NAUO3."""
import sys, json, numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from pmglib import Glb, kabsch, pose_from
SP = sys.argv[1]
ROOT = '/Users/lee-johnson/Desktop/Claude_Cadasio/'
P = Glb(ROOT + 'PMG Build Instructions/pmg.glb')
C = json.load(open(SP + '/copies.json'))
def meshes(g, t):
    out = []
    for i, name, mi, W in g.mesh_nodes(t):
        v, _ = g.mesh_geometry(mi, W, faces=False)
        out.append((g.meshes[mi].get('name') or name, name, v))
    return out
def Tm(pose):
    from scipy.spatial.transform import Rotation
    if isinstance(pose, list):
        T = np.eye(4); T[:3, 3] = pose; return T
    ax = np.array(pose['r'][:3]); R = Rotation.from_rotvec(ax / np.linalg.norm(ax) * np.radians(pose['r'][3])).as_matrix()
    at = np.array(pose['at']); T = np.eye(4); T[:3, :3] = R; T[:3, 3] = at - R @ at + np.array(pose['t']); return T
pm = meshes(P, 'NAUO78')
pmid = (np.concatenate([m[2] for m in pm]).min(0) + np.concatenate([m[2] for m in pm]).max(0)) / 2
out = {}
for label, path, t in [('MRA NAUO82', 'MRA Build Instructions Prototype/mra.glb', 'NAUO82'), ('RCC NAUO23', 'RCC Build Instructions/rcc.glb', 'NAUO23')]:
    G = Glb(ROOT + path)
    om = meshes(G, t)
    from collections import Counter
    co = Counter((m[0], len(m[2])) for m in om); cp = Counter((m[0], len(m[2])) for m in pm)
    unique = [k for k in co if co[k] == 1 and cp.get(k) == 1]
    A = np.concatenate([next(m[2] for m in om if (m[0], len(m[2])) == k) for k in unique])
    B = np.concatenate([next(m[2] for m in pm if (m[0], len(m[2])) == k) for k in unique])
    R, tt, rms, mx = kabsch(A, B)
    omid = (np.concatenate([m[2] for m in om]).min(0) + np.concatenate([m[2] for m in om]).max(0)) / 2
    pose = pose_from(R, tt, omid)
    # check: every mesh of the other module, moved, against the PMG module's points of the same name
    checks = {}
    for name in sorted(set(m[0] for m in om)):
        src = np.concatenate([m[2] for m in om if m[0] == name]) @ R.T + tt
        dst = [m[2] for m in pm if m[0] == name]
        if not dst:
            checks[name] = 'not in the PMG module'; continue
        d, _ = cKDTree(np.concatenate(dst)).query(src[::max(1, len(src) // 3000)])
        checks[name] = dict(median=round(float(np.median(d)), 3), p95=round(float(np.percentile(d, 95)), 3))
    print(label, '-> PMG NAUO78 (built): fitted on', unique, 'rms', round(rms, 4), 'max', round(mx, 4))
    print('   pose', pose)
    for k, v in checks.items():
        print('   ', k, v)
    # to the bench copy NAUO1: compose with NAUO78 -> NAUO1
    T1 = Tm(C['io_module']['NAUO1']['pose']); T94 = Tm(C['io_module']['NAUO94']['pose'])
    S = np.eye(4); S[:3, :3] = R; S[:3, 3] = tt
    pose1 = pose_from((T1 @ S)[:3, :3], (T1 @ S)[:3, 3], omid)
    pose94 = pose_from((T94 @ S)[:3, :3], (T94 @ S)[:3, 3], omid)
    print('   -> PMG NAUO1 (bench):', pose1); print('   -> PMG NAUO94 (held above):', pose94)
    out[label] = dict(fitted_on=[f'{a} ({b} verts)' for a, b in unique], rms_mm=round(rms, 4), max_err_mm=round(mx, 4), other_module_middle=omid.round(2).tolist(),
                      to_PMG_NAUO78_built=pose, to_PMG_NAUO1_bench=pose1, to_PMG_NAUO94_held_above=pose94, mesh_checks=checks)
    if label.startswith('MRA'):
        # the MRA's single-mesh Nano NAUO126 -> PMG loose Nano NAUO3 and the built Nano seat
        nano = next(m[2] for m in om if m[1] == 'NAUO126')
        moved = nano @ R.T + tt
        n3, _, _ = P.instance_geometry('NAUO3', faces=False)
        # NAUO3 is the bench seat + 15.24 Y; carry NAUO3 back to the built pose: inverse of (NAUO78->NAUO1) after removing the lift
        T1i = np.linalg.inv(T1)
        n3_seat_built = (n3 - [0.01, 15.24, 0.01]) @ T1i[:3, :3].T + T1i[:3, 3]
        d, _ = cKDTree(n3_seat_built).query(moved[::50])
        print('   MRA Nano NAUO126 (carried with the module) vs PMG Nano (NAUO3 brought to the built seat): median', np.median(d).round(3), 'p95', np.percentile(d, 95).round(3))
        out[label]['MRA_nano_NAUO126_vs_PMG_built_seat'] = dict(median=round(float(np.median(d)), 3), p95=round(float(np.percentile(d, 95)), 3))
json.dump(out, open(SP + '/module_compare.json', 'w'), indent=1)
