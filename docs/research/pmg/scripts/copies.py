"""Rigid transform from the BUILT copy of a part to each of its pose copies, by matching vertices mesh by mesh (same mesh name
and vertex count, in node order: the copies are the same CAD part, so their vertices come in the same order). Writes
copies.json into the scratch folder (merged with what is there)."""
import sys, json, os, numpy as np
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from pmglib import Glb, kabsch, pose_from
SP = sys.argv[1]
g = Glb('/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions/pmg.glb')
KINDS = {
    'io_module': ('NAUO78', ['NAUO1', 'NAUO94']),
    'button_black': ('NAUO76', ['NAUO7']), 'button_yellow': ('NAUO83', ['NAUO6']),
    'button_white': ('NAUO84', ['NAUO5']), 'button_blue': ('NAUO85', ['NAUO4']),
    'display': ('NAUO79', ['NAUO80', 'NAUO129']),
    'matrix': ('NAUO81', ['NAUO44', 'NAUO82', 'NAUO267']),
    'usb_right_angle': ('NAUO282', ['NAUO279', 'NAUO281']),
    'usb_a_end': ('NAUO283', ['NAUO278', 'NAUO280']),
    'nano_loose': ('NAUO3', ['NAUO2']),
    'buttons_built_to_built': ('NAUO76', ['NAUO83', 'NAUO84', 'NAUO85']),
    'buttons_bench_to_bench': ('NAUO7', ['NAUO6', 'NAUO5', 'NAUO4']),
}
which = sys.argv[2:] or list(KINDS)
path = SP + '/copies.json'
res = json.load(open(path)) if os.path.exists(path) else {}
def meshes(t):
    out = []
    for i, name, mi, W in g.mesh_nodes(t):
        v, _ = g.mesh_geometry(mi, W, faces=False)
        out.append((g.meshes[mi].get('name') or name, name, v))
    return out
for k in which:
    built, others = KINDS[k]
    A = meshes(built)
    allA = np.concatenate([m[2] for m in A])
    lo, hi = allA.min(0), allA.max(0); mid = (lo + hi) / 2
    res.setdefault(k, {})['built'] = built
    res[k]['built_box'] = dict(lo=lo.round(2).tolist(), hi=hi.round(2).tolist(), mid=mid.round(2).tolist())
    for o in others:
        Bm = meshes(o)
        # pair meshes: same (mesh name, count) in order of appearance
        pool = {}
        for j, (mn, nn, v) in enumerate(Bm):
            pool.setdefault((mn, len(v)), []).append(j)
        pa, pb, missing = [], [], []
        for mn, nn, v in A:
            key = (mn, len(v))
            if pool.get(key):
                j = pool[key].pop(0); pa.append(v); pb.append(Bm[j][2])
            else:
                missing.append(mn)
        extra = [Bm[j][0] for js in pool.values() for j in js]
        PA, PB = np.concatenate(pa), np.concatenate(pb)
        R, t, rms, mx = kabsch(PA, PB)
        pose = pose_from(R, t, mid)
        bl, bh = np.concatenate([m[2] for m in Bm]).min(0), np.concatenate([m[2] for m in Bm]).max(0)
        res[k][o] = dict(pose=pose, rms_mm=round(rms, 4), max_err_mm=round(mx, 4), n_points=len(PA), meshes_only_in_built=missing,
                         meshes_only_in_copy=extra, copy_box=dict(lo=bl.round(2).tolist(), hi=bh.round(2).tolist(), mid=((bl + bh) / 2).round(2).tolist()))
        print(k, built, '->', o, 'pose', pose, 'rms', round(rms, 4), 'max', round(mx, 4), 'n', len(PA), 'missing', missing, 'extra', extra)
    json.dump(res, open(path, 'w'), indent=1)
