"""Which of check_caps.py's Step 42c problems a camera sees: a ray from the Step 42 camera (1440x628) to each problem's point, at that
moment of the motion, blocked by any part on screen (but those named in the problem) more than 2 mm before the point."""
import sys, json, re
import numpy as np
import trimesh
from scipy.spatial.transform import Rotation, Slerp
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/tools')
import stepgen
from stepgen import _matrix
KIT = '/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions'
steps_file, report = sys.argv[1], sys.argv[2]
S = json.load(open(steps_file))
spec = json.load(open(KIT + '/materials.json'))
model = stepgen.Model(KIT + '/' + spec['source'], adjust=spec.get('adjust_mm') or {}, own_parts=spec.get('own_parts', {}),
                      extra_parts={i: (KIT + '/' + e['glb'], e['pose']) for i, e in spec.get('extra_parts', {}).items()})
names = [v['name'] for v in S['views']]
i = names.index('Step 42c'); v, before = S['views'][i], S['views'][i - 1]
carry, prior = v['carry'], before.get('carry') or {}
beats = max(len(c.get('via', [])) + 1 for c in carry.values())
ease = lambda k: 4 * k ** 3 if k < 0.5 else 1 - (-2 * k + 2) ** 3 / 2
centre = {}


def mix(a, b, k, part):
    A, B = _matrix(a), _matrix(b)
    c = centre.setdefault(part, model.inst[part].bounds.mean(0))
    R = Slerp([0, 1], Rotation.from_matrix([A[:3, :3], B[:3, :3]]))([k]).as_matrix()[0]
    M = np.eye(4); M[:3, :3] = R
    M[:3, 3] = (A[:3, :3] @ c + A[:3, 3]) * (1 - k) + (B[:3, :3] @ c + B[:3, 3]) * k - R @ c
    return M


def state(km):
    b = min(beats - 1, int(km * beats)); kk = (b + ease(km * beats - b)) / beats
    M = {}
    def placed(pid, d=0):
        if pid in M: return M[pid]
        c = carry.get(pid)
        if c is None or d > 8:
            M[pid] = _matrix((v.get('offsets') or {}).get(pid)); return M[pid]
        was = prior.get(pid, {}).get('pose') if prior.get(pid, {}).get('by') == c['by'] else None
        via = c.get('via', [])
        if was is None or was == c['pose']:
            here = _matrix(c['pose'])
        else:
            poses = [was, *via, c['pose']]; n = len(poses) - 1; s = min(n - 1, int(kk * n))
            here = mix(poses[s], poses[s + 1], kk * n - s, pid)
        M[pid] = placed(c['by'], d + 1) @ here
        return M[pid]
    for pid in v['visible']:
        placed(pid)
    return M


cam = v['camera']; d = np.asarray(cam['dir'], float); d /= np.linalg.norm(d)
w, h = 1440, 628; half = np.radians(22.5)
dist = max(cam['radius'] / np.sin(half), cam['radius'] / np.sin(np.arctan(np.tan(half) * w / h))) * 1.08
eye = np.asarray(cam['target'], float) + d * dist
rows = []
for line in open(report):
    if not line.startswith('Step 42c') or 'near [' not in line:
        continue
    km = float(re.search(r'at ([0-9.]+)', line).group(1))
    pt = np.array(json.loads(re.search(r'near (\[[^\]]*\])', line).group(1)))
    involved = set(re.findall(r'(NAUO\d+|NANO|CAP_\w+)', line))
    rows.append((km, pt, involved, line.strip()))
cache = {}
seen = []
for km, pt, involved, line in rows:
    key = round(km, 2)
    if key not in cache:
        M = state(km)
        cache[key] = {pid: (model.inst[pid], M[pid]) for pid in v['visible'] if pid in model.inst and not pid.startswith('STEM_')}
    parts = cache[key]
    meshes = []
    for pid, (m, X) in parts.items():
        if pid in involved:
            continue
        mm = m.copy(); mm.apply_transform(X); meshes.append(mm)
    big = trimesh.util.concatenate(meshes)
    ray = pt - eye; L = np.linalg.norm(ray); ray /= L
    locs, _, _ = big.ray.intersects_location([eye], [ray])
    hidden = len(locs) and (((locs - eye) @ ray) < L - 2.0).any()
    seen.append(not hidden)
n = len(rows); s = sum(seen)
by_beat = {}
for (km, _, _, _), ok in zip(rows, seen):
    b = min(beats, int(km * beats) + 1)
    t = by_beat.setdefault(b, [0, 0]); t[0] += 1; t[1] += ok
print(f'{n} problems with a place, {s} in sight; by beat (all, in sight):', {b: tuple(x) for b, x in sorted(by_beat.items())})
