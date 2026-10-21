"""Step 42 (Lee's fourth round, second note: "from behind the model instead of up and above it"): cameras from behind screened against
the round-4 motion as steps.json has it. For each direction (azimuth from straight behind, +x, towards -z positive; elevation), the
smallest frame (target moved along the view's up, radius) that keeps the module, its Nano Board and plug, the USB A end and the cable on
screen and clear of the caption box at four window sizes through every beat; then, from there, how much of the module and of the A end the
case and the displays hide (rays, embree), beat by beat."""
import sys, os, json
import numpy as np
from scipy.spatial.transform import Rotation as Ro, Slerp
import trimesh
sys.path.insert(0, 'tools'); sys.path.insert(0, 'docs/research/pmg/round3/scripts')
import stepgen
from stepgen import _matrix
from proj import project, SIZES
KIT = 'PMG Build Instructions'
S = json.load(open(KIT + '/steps.json'))
V = {v['name']: v for v in S['views']}
v42, v42c = V['Step 42'], V['Step 42c']
spec = json.load(open(KIT + '/materials.json'))
model = stepgen.Model(KIT + '/' + spec['source'], adjust=spec.get('adjust_mm') or {}, own_parts=spec.get('own_parts', {}),
                      extra_parts={i: (KIT + '/' + e['glb'], e['pose']) for i, e in spec.get('extra_parts', {}).items()})
MOD, NANO, PLUG, A = 'NAUO78', 'NANO', 'NAUO282', 'NAUO283'


def placed(v):
    carry, offs = v.get('carry') or {}, v.get('offsets') or {}
    out = {}
    def pl(pid, d=0):
        if pid in out: return out[pid]
        c = carry.get(pid)
        out[pid] = _matrix(offs.get(pid)) if c is None or d > 8 else pl(c['by'], d + 1) @ _matrix(c['pose'])
        return out[pid]
    for p in v['visible']: pl(p)
    return out


P0 = placed(v42)                 # (bench)
riders = {MOD, NANO, PLUG}
STATIC = [p for p in v42['visible'] if p in model.inst and p not in riders and p != A]
by = lambda p: P0[v42c['carry'][p]['by']]
stops = lambda p: [_matrix(v42['carry'][p]['pose'])] + [_matrix(x) for x in v42c['carry'][p]['via']] + [_matrix(v42c['carry'][p]['pose'])]
MS, AS = stops(MOD), stops(A)
cM, cA = model.inst[MOD].bounds.mean(0), model.inst[A].bounds.mean(0)


def mix(Ma, Mb, k, c):
    k = k * k * (3 - 2 * k)
    R = Slerp([0, 1], Ro.from_matrix([Ma[:3, :3], Mb[:3, :3]]))([k]).as_matrix()[0]
    M = np.eye(4); M[:3, :3] = R
    M[:3, 3] = (Ma[:3, :3] @ c + Ma[:3, 3]) * (1 - k) + (Mb[:3, :3] @ c + Mb[:3, 3]) * k - R @ c
    return M


sub = lambda p, n: np.asarray(model.inst[p].vertices)[::max(1, len(model.inst[p].vertices) // n)]
VM = {p: sub(p, 400) for p in (MOD, NANO, PLUG)}
VA = sub(A, 200)
rel = {p: np.linalg.inv(P0[MOD]) @ P0[p] for p in (NANO, PLUG)}   # (riders on the module)
MOMENTS = []                          # (beat, k, module points, A end points)
for b in range(len(MS) - 1):
    for k in np.linspace(0, 1, 9):
        M = by(MOD) @ mix(MS[b], MS[b + 1], k, cM)
        Ma = by(A) @ mix(AS[b], AS[b + 1], k, cA)
        mp = np.vstack([VM[MOD] @ M[:3, :3].T + M[:3, 3]] + [VM[p] @ (M @ rel[p])[:3, :3].T + (M @ rel[p])[:3, 3] for p in (NANO, PLUG)])
        MOMENTS.append((b, k, mp, VA @ Ma[:3, :3].T + Ma[:3, 3]))
cable = np.vstack([np.asarray(S['routes'][i]['pts'], float) for i in v42c['wire_via']['usb cable'] + [v42c['wires']['usb cable']]])
KEY = np.vstack([np.vstack([m, a]) for _, _, m, a in MOMENTS] + [cable])
static_mesh = trimesh.util.concatenate([model.inst[p].copy().apply_transform(P0[p]) for p in STATIC])
ray = trimesh.ray.ray_pyembree.RayMeshIntersector(static_mesh) if hasattr(trimesh.ray, 'ray_pyembree') else static_mesh.ray


def fit(d):
    d = np.asarray(d, float) / np.linalg.norm(d)
    f = -d; r = np.cross(f, [0, 1, 0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    c0 = (KEY.min(0) + KEY.max(0)) / 2
    for rad in np.arange(80, 200, 3.0):
        for sh in np.arange(-0.5, 0.31, 0.05):           # (target moved along the view's up by sh * radius: things down, clear of the box)
            for sr in (0.0, -0.1, 0.1):
                cam = dict(dir=d.tolist(), target=(c0 + u * sh * rad + r * sr * rad).tolist(), radius=float(rad))
                ok = True
                for key, (w, h, box) in SIZES.items():
                    q = project(KEY, cam, w, h)
                    if (q[:, 0] < 8).any() or (q[:, 0] > w - 8).any() or (q[:, 1] < 8).any() or (q[:, 1] > h - 8).any():
                        ok = False; break
                    if ((q[:, 0] > box[0] - 4) & (q[:, 0] < box[2] + 4) & (q[:, 1] > box[1] - 4) & (q[:, 1] < box[3] + 4)).any():
                        ok = False; break
                if ok: return cam
    return None


def hidden(cam, pts):
    """Share of pts the static parts hide from the camera (as at the LMS's size)."""
    w, h, _ = SIZES['1000x548']
    d = np.asarray(cam['dir']); half = np.radians(22.5); aspect = w / h
    dist = max(cam['radius'] / np.sin(half), cam['radius'] / np.sin(np.arctan(np.tan(half) * aspect))) * 1.08
    eye = np.asarray(cam['target']) + d * dist
    v = pts - eye; L = np.linalg.norm(v, axis=1); v /= L[:, None]
    loc, idx, _ = ray.intersects_location(np.repeat(eye[None], len(pts), 0), v, multiple_hits=False)
    hit = np.zeros(len(pts), bool)
    if len(idx):
        dd = np.linalg.norm(loc - eye, axis=1)
        hit[idx[dd < L[idx] - 1.0]] = True
    return hit.mean()


if __name__ == '__main__':
    cands = [(az, el) for az in (-45, -30, -15, 0, 15, 30, 45, 60) for el in (20, 28, 35, 42, 50)]
    if len(sys.argv) > 1: cands = [tuple(map(float, a.split(','))) for a in sys.argv[1:]]
    rows = []
    for az, el in cands:
        a, e = np.radians(az), np.radians(el)
        d = [np.cos(e) * np.cos(a), np.sin(e), -np.cos(e) * np.sin(a)]
        cam = fit(d)
        if cam is None: print(f'az {az:4.0f} el {el:3.0f}: no frame'); continue
        hm = [np.mean([hidden(cam, m[::4]) for b, k, m, a_ in MOMENTS if b == bb]) for bb in range(len(MS) - 1)]
        ha = [np.mean([hidden(cam, a_[::2]) for b, k, m, a_ in MOMENTS if b == bb]) for bb in range(len(MS) - 1)]
        rows.append((az, el, cam, hm, ha))
        print(f"az {az:4.0f} el {el:3.0f}: radius {cam['radius']:5.0f} target {np.round(cam['target'], 0).tolist()}  module hidden "
              f"{' '.join(f'{x:4.0%}' for x in hm)}  A end hidden {' '.join(f'{x:4.0%}' for x in ha)}", flush=True)
