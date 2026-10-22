"""Can our LSM model be taken apart in the order of TechBox's published Cadasio take-apart (19075)? Each published move, swept in our
model (the exact CAD the generator's collision tests use: "LSM Build Instructions/lsm.glb", via tools/stepgen.Model) against every part
still there at that point and the wires drawn as tubes from steps.json's routes.

    .venv.nosync/bin/python -I docs/research/lsm/decon/published/feasibility.py [out.json]

Reads only lsm.glb and steps.json; writes only feasibility.json beside this file (and prints the log). No generator run. Peak memory
about 0.7 GB.

The sweep (rays, as tools/stepgen.blocked does, with numbers instead of a yes / no): points on the moving part (vertices and surface
samples, set `tol` mm in from its surface) are cast along the move into each obstacle, and points of the obstacle in the swept region,
set in the same way, are cast back into the moving part. A ray that meets a face turned towards it is a contact after `t` mm of
travel; a second ray finds where it leaves the obstacle, so `depth` = how far the part would be inside it by the end of the move
(min(reach - t, thickness)). A contact counts when it goes deeper than 0.4 mm (the generator's own press-fit allowance).

The model's joints are drawn tight: many tabs are 0.1 - 0.5 mm wider than their slots (`at rest` below: how far a part already lies
inside the other), and sliding such a tab along its slot reads as contact. So each contact is measured again with the points set
further in (tol 0.2 ... 4 mm): `catch` = the largest tol at which it still collides, about how far the obstacle reaches across the
part's way (an overlap at rest of i mm reads as a catch of up to about 1.7 i; a hook or lip that stands proud by h reads as about h).

Each move gets one verdict:
  FREE      no contact with a catch of 0.6 mm or more.
  LATCH     every such contact begins within the first 1.2 mm of the move: the part is held where it is by a hook, barb, detent or
            latch and comes free once that is released (in the kit: squeezed or flexed by hand). tools/stepgen.blocked() ignores a first
            contact this close (its snug_fit), so the generator lets the move through, as the Full Build's own checks did.
  BLOCKED   a contact with a catch of 0.6 mm or more begins later along the way: the part runs into something.
`generator` = what tools/stepgen.blocked() (the check behind remove()'s warning) says of the same move against the parts (not wires).

Caveat (21 Oct 2026 run): the catch overstates at box-like corners, where vertex normals point diagonally: the 64 stand-in stems (in
fact at most 0.2 mm off their 3.30 mm square holes) and D10's end in D4 (in fact 0.03 mm) read as catches. The joint section at the end
(intervals along lines through each joint, from the meshes' own surface crossings) is the measure to trust: it is what
docs/research/lsm/decon/published/feasibility_verdicts.json quotes."""
import gc
import json
import sys
from pathlib import Path

import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[5]
KIT = ROOT / 'LSM Build Instructions'
sys.path.insert(0, str(ROOT / 'tools'))
from stepgen import DEFAULTS, Model, _matrix, blocked, compose  # noqa: E402

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
OUT = Path(ARGS[0]) if ARGS else Path(__file__).with_name('feasibility.json')
EPS, PRESS, SNUG, REAL = 0.02, 0.4, 1.2, 0.6
TOLS = (0.2, 0.4, 0.6, 0.8, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0)
X, Y, Z = np.eye(3)
AXES = dict(zip(['+X', '-X', '+Y', '-Y', '+Z', '-Z'], (X, -X, Y, -Y, Z, -Z)))

print('loading lsm.glb ...', flush=True)
M = Model(KIT / 'lsm.glb')
S = json.loads((KIT / 'steps.json').read_text(encoding='utf-8'))
ROUTES, WDEF = S['routes'], S['wires']
V = {v['name']: v for v in S['views']}
STEMS = [f'STEM_{k:02d}' for k in range(1, 65)]
D11S = ['D11_A', 'D11_B', 'D11_C', 'D11_D']
PINS = ['J_WHITE_M', 'J_GREY_M', 'J_PURPLE_M']
SOCKETS = ['J_WHITE_F', 'J_GREY_F', 'J_PURPLE_F']
ALL = [i for i in M.inst if i != 'BACKING']          # (the backing is peeled off in Full Build Step 1)


# ---------------------------------------------------------------- meshes
_posed = {}


def mesh(i, pose=None):
    """Part i at a pose (None: seated, the model's own mesh)."""
    if pose is None or pose == [0.0, 0.0, 0.0]:
        return M.inst[i]
    key = (i, json.dumps(pose, sort_keys=True))
    if key not in _posed:
        if len(_posed) > 40:
            _posed.clear()
        m = M.inst[i].copy()
        m.apply_transform(_matrix(pose))
        _posed[key] = m
    return _posed[key]


def tube(pts, r, sides=10):
    """A wire's tube along its centre line (open at both ends), faces turned outward."""
    p = np.asarray(pts, float)
    p = p[np.r_[True, np.linalg.norm(np.diff(p, axis=0), axis=1) > 1e-6]]
    t = np.gradient(p, axis=0)
    t /= np.linalg.norm(t, axis=1)[:, None]
    n = np.cross(t[0], [0, 1, 0] if abs(t[0][1]) < 0.9 else [1, 0, 0])
    rings = []
    for k in range(len(p)):                          # (parallel transport)
        n = n - t[k] * (n @ t[k])
        n /= np.linalg.norm(n)
        b = np.cross(t[k], n)
        a = np.linspace(0, 2 * np.pi, sides, endpoint=False)
        rings.append(p[k] + r * (np.cos(a)[:, None] * n + np.sin(a)[:, None] * b))
    verts = np.vstack(rings)
    faces = []
    for k in range(len(p) - 1):
        for s in range(sides):
            a0, a1 = k * sides + s, k * sides + (s + 1) % sides
            faces += [[a0, a1, a1 + sides], [a0, a1 + sides, a0 + sides]]
    f = np.array(faces)
    m = trimesh.Trimesh(verts, f, process=False)
    flip = np.einsum('ij,ij->i', m.face_normals, m.triangles_center - np.repeat(p, sides, axis=0)[f[:, 0]]) < 0
    f[flip] = f[flip][:, ::-1]
    return trimesh.Trimesh(verts, f, process=False)


def wire_mesh(name, route_no):
    return tube(ROUTES[route_no]['pts'], WDEF[name]['radius'])


def union(meshes):
    meshes = [m for m in meshes if m is not None]
    return meshes[0] if len(meshes) == 1 else trimesh.util.concatenate(meshes)


def shifted(pose, by):
    by = np.asarray(by, float)
    if pose is None:
        return by.round(3).tolist()
    if isinstance(pose, dict):
        return dict(pose, t=(np.asarray(pose.get('t', [0, 0, 0]), float) + by).round(3).tolist())
    return (np.asarray(pose, float) + by).round(3).tolist()


# ---------------------------------------------------------------- the sweep
_pts = {}


def _points(m, tol, n=12000, seed=1):
    """Points `tol` mm inside a mesh's surface: its vertices and area samples (cached for the model's own meshes)."""
    key = (id(m), tol, n)
    if key in _pts:
        return _pts[key]
    v = m.vertices - m.vertex_normals * tol
    s, fi = trimesh.sample.sample_surface(m, n, seed=seed)
    pts = np.vstack([v, s - m.face_normals[fi] * tol])
    if len(pts) > 40000:
        pts = pts[np.random.default_rng(seed).choice(len(pts), 40000, replace=False)]
    if any(m is M.inst[i] for i in M.inst):
        _pts[key] = pts
    return pts


def _cast(src, dst, d, reach, spot_on_dst):
    """Rays from src along d into dst: rows (t, depth, inside at rest, x, y, z); x, y, z: the spot on the obstacle, at rest."""
    if not len(src):
        return np.zeros((0, 6))
    o = src + d * EPS
    tri, ray, loc = dst.ray.intersects_id(o, np.repeat([d], len(o), 0), multiple_hits=False, return_locations=True)
    if not len(ray):
        return np.zeros((0, 6))
    t = np.einsum('ij,j->i', loc - o[ray], d)
    facing = dst.face_normals[tri] @ d
    out = []
    ent = (facing < 0) & (t < reach)
    if ent.any():
        e_loc, e_t = loc[ent], t[ent]
        o2 = e_loc + d * EPS
        _, ray2, loc2 = dst.ray.intersects_id(o2, np.repeat([d], len(o2), 0), multiple_hits=False, return_locations=True)
        thick = np.full(len(o2), np.inf)
        if len(ray2):
            thick[ray2] = np.einsum('ij,j->i', loc2 - o2[ray2], d)
        out.append(np.c_[e_t, np.minimum(reach - e_t, thick), np.zeros(len(e_t)), e_loc if spot_on_dst else o[ray][ent]])
    lv = facing > 0
    if lv.any():
        q = o[ray[lv]]
        if len(q) > 3000:
            q = q[np.random.default_rng(0).choice(len(q), 3000, replace=False)]
        _, dist, _ = trimesh.proximity.closest_point(dst, q)
        out.append(np.c_[np.zeros(len(q)), dist, np.ones(len(q)), q])
    return np.vstack(out) if out else np.zeros((0, 6))


def sweep(mov, obs, d, reach, tol=0.2):
    """Sliding mov along d by reach past obs (points tol mm in): dict, or None if they never meet."""
    d = np.asarray(d, float) / np.linalg.norm(d)
    lo, hi = mov.bounds
    slo, shi = np.minimum(lo, lo + d * reach) - 1, np.maximum(hi, hi + d * reach) + 1
    olo, ohi = obs.bounds
    if np.any(ohi < slo) or np.any(olo > shi):
        return None
    Q = _points(obs, tol, 8000)
    Q = Q[np.all((Q >= slo) & (Q <= shi), axis=1)]
    hits = np.vstack([_cast(_points(mov, tol), obs, d, reach, True), _cast(Q, mov, -d, reach, False)])
    if not len(hits):
        return None
    rest, move = hits[hits[:, 2] == 1], hits[hits[:, 2] == 0]
    deep = move[move[:, 1] > PRESS]
    r = dict(rest_overlap=round(float(rest[:, 1].max()), 2) if len(rest) else 0.0, hit=bool(len(deep)))
    if len(deep):
        k = int(np.argmin(deep[:, 0]))
        r.update(first=round(float(deep[k, 0]), 2), depth=round(float(deep[:, 1].max()), 2), at=np.round(deep[k, 3:6], 2).tolist())
    return r


_thin = {}


def thin(m):
    """A mesh's thinnest extent (its oriented box's), for the largest tol that still measures something: points set in further than
    about half of it come out on the far side."""
    if id(m) not in _thin:
        _thin[id(m)] = float(min(m.bounding_box_oriented.primitive.extents))
    return _thin[id(m)]


def measure(mov, obs, d, reach, parts=()):
    """One obstacle against one move: the contact at tol 0.2, and its catch (the largest tol at which it still collides, up to 0.4 of
    the thinner part's thinnest extent: 'catch_capped' when it still collides there)."""
    r = sweep(mov, obs, d, reach, 0.2)
    if not r or not r['hit']:
        return r
    cap = 0.4 * min([thin(mesh(i)) for i in parts] + [thin(obs)])
    c, last = 0.2, r
    r['catch_capped'] = False
    for tol in [t for t in TOLS[1:] if t <= cap] + [None]:
        if tol is None:
            r['catch_capped'] = True
            break
        q = sweep(mov, obs, d, reach, tol)
        if not q or not q['hit']:
            break
        c, last = tol, q
    real = REAL if thin(obs) > 2.0 else 0.2                    # (a wire: any contact counts)
    r['catch'] = c
    r['first_real'] = last['first'] if c >= real else None      # (where the deepest-reaching part of it is first met)
    r['at_real'] = last['at'] if c >= real else None
    r['kind'] = ('tight' if c < real else 'latch' if last['first'] < SNUG else 'blocked')
    return r


# ---------------------------------------------------------------- states and moves
class State:
    def __init__(self, parts, poses=None, wires=None):
        self.parts = list(parts)
        self.poses = dict(poses or {})               # id -> pose (not seated)
        self.wires = dict(wires or {})               # wire name -> route no

    def copy(self, **change):
        s = State(self.parts, self.poses, self.wires)
        for k, v in change.items():
            setattr(s, k, v)
        return s

    def obstacles(self, moving, skip=()):
        out = {i: mesh(i, self.poses.get(i)) for i in self.parts if i not in moving and i not in skip}
        for w, n in self.wires.items():
            r = ROUTES[n]
            if r.get('a') in moving or r.get('b') in moving or 'wire:' + w in skip:
                continue                             # (a wire with an end on the moving part bends with it: not tested here)
            out['wire:' + w] = wire_mesh(w, n)
        return out

    def moving_mesh(self, moving, extra=None):
        return union([mesh(i, (extra or {}).get(i, self.poses.get(i))) for i in moving])


RESULTS = []


def test(label, state, moving, d, reach, skip=(), note='', record=True, quiet=False, gen_check=True):
    """Sweep the moving parts along d by reach against everything else in `state`; print and record the verdict."""
    d = np.asarray(d, float) / np.linalg.norm(d)
    mov = state.moving_mesh(moving)
    obst = state.obstacles(moving, skip)
    rows = {}
    for k, o in obst.items():
        r = measure(mov, o, d, reach, moving)
        if r and (r['hit'] or r['rest_overlap'] > 0.05):
            rows[k] = r
    real = {k: r for k, r in rows.items() if r.get('kind') in ('latch', 'blocked')}
    verdict = 'BLOCKED' if any(r['kind'] == 'blocked' for r in real.values()) else 'LATCH' if real else 'FREE'
    lo, hi = mov.bounds
    slo, shi = np.minimum(lo, lo + d * reach) - 1, np.maximum(hi, hi + d * reach) + 1
    parts = [o for k, o in obst.items() if not k.startswith('wire:') and not (np.any(o.bounds[1] < slo) or np.any(o.bounds[0] > shi))]
    gen = (bool(parts) and bool(blocked(mov, union(parts), d, reach, DEFAULTS))) if gen_check else None
    if not quiet:
        named = ', '.join(f"{k} {r['kind']}" for k, r in sorted(real.items()))
        print(f'{label}: {np.round(d, 3).tolist()} x {round(reach, 1)} mm: {verdict}' + (f' ({named})' if real else '')
              + ("; generator's check: " + ('flags it' if gen else 'passes') if gen is not None else ''), flush=True)
        for k, r in sorted(rows.items(), key=lambda kr: (kr[1].get('first') is None, kr[1].get('first') or 0)):
            if r['hit'] or r['rest_overlap'] > 0.05:
                print(f"    {k:<16s} at rest {r['rest_overlap']:>5}  contact {r.get('first')} mm (depth {r.get('depth')})  catch "
                      f"{('>=' if r.get('catch_capped') else '') + str(r.get('catch'))}"
                      f"  {r.get('kind', '')}{'  first met after ' + str(r['first_real']) + ' mm at ' + str(r['at_real']) if r.get('at_real') else ''}")
    res = dict(label=label, moving=list(moving), dir=np.round(d, 4).tolist(), reach=reach, verdict=verdict, generator_flags=gen,
               contacts=rows, note=note)
    if record:
        RESULTS.append(res)
    gc.collect()
    return res


def first_stage(label, state, moving, d, reach, ks=(0.5, 1, 1.5, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20), only=None):
    """The smallest shift across the move, made first, after which the move has no BLOCKED or LATCH contact (and the shift none either)."""
    d = np.asarray(d, float) / np.linalg.norm(d)
    found = {}
    for name, e in AXES.items():
        if abs(e @ d) > 0.5 or (only and name not in only):
            continue
        for k in ks:
            s1 = test(f'{label} / first {name} {k}', state, moving, e, k, record=False, quiet=True, gen_check=False)
            if s1['verdict'] != 'FREE':
                continue
            st2 = state.copy(poses={**state.poses, **{i: shifted(state.poses.get(i), e * k) for i in moving}})
            s2 = test(f'{label} / then', st2, moving, d, reach, record=False, quiet=True, gen_check=False)
            if s2['verdict'] == 'FREE':
                found[name] = k
                break
    print(f'    -> first stage that frees it: {found or "none up to 20 mm"}', flush=True)
    return found


def other_ways(label, state, moving, reach, skip=()):
    """Which straight axis directions take the part off outright (FREE, or held only by a latch)."""
    out = {}
    for name, e in AXES.items():
        out[name] = test(f'{label} / try {name}', state, moving, e, reach, skip=skip, record=False, quiet=True, gen_check=False)['verdict']
    print(f'    -> straight directions: {out}', flush=True)
    return out


def staged(label, state, moving, stages, note=''):
    """A move in straight stages [(direction, mm), ...], each swept from where the one before ended."""
    st = state.copy(poses=dict(state.poses))
    out = []
    for k, (d, reach) in enumerate(stages):
        out.append(test(f'{label} / stage {k + 1}', st, moving, d, reach, note=note))
        d = np.asarray(d, float) / np.linalg.norm(d)
        st.poses.update({i: shifted(st.poses.get(i), d * reach) for i in moving})
    return out


def static(label, a_mesh, b_mesh):
    """How far two things at rest lie inside each other (0 if they do not)."""
    r = sweep(a_mesh, b_mesh, Y, 0.05, 0.05)
    q = sweep(b_mesh, a_mesh, Y, 0.05, 0.05)
    depth = max((r or {}).get('rest_overlap', 0.0), (q or {}).get('rest_overlap', 0.0))
    spot = (r or {}).get('at') or (q or {}).get('at')
    print(f'{label}: overlap {depth} mm{" near " + str(spot) if spot else ""}', flush=True)
    RESULTS.append(dict(label=label, static_overlap=depth))
    return depth


# ================================================================ the published order, in our model
WAYS = {}
SEATED_WIRES = dict(V['Completed View']['wires'])
st = State(ALL, wires=SEATED_WIRES)

print('\n# 1 - 3. the stems, D8, D7 (from the top)')
test('P1 the 64 stems up 62.5', st, STEMS, Y, 62.5)
st.parts = [i for i in st.parts if i not in STEMS]
r = test('P2 D8 up 54.1', st, ['D8'], Y, 54.1)
st.parts.remove('D8')
test('P3 D7 up 67.8', st, ['D7'], Y, 67.8)
st.parts.remove('D7')

print('\n# 4. D5 out +X 54.1 (the D11 posts, D6, the matrix with D10, the D9s, D4, D3 and D2 still on)')
r = test('P4 D5 +X 54.1', st, ['D5'], X, 54.1)
WAYS['P4'] = other_ways('P4 D5', st, ['D5'], 54.1)
st.parts.remove('D5')

print('\n# 5. D4 out -X 75.2 (the USB cable stays in its notch)')
r = test('P5 D4 -X 75.2', st, ['D4'], -X, 75.2)
WAYS['P5'] = other_ways('P5 D4', st, ['D4'], 75.2, skip=('wire:usb cable',))
staged('P5 alt: the Full Build\'s Step 25 reversed', st, ['D4'], [(-X, 8.0), (Y, 65.0)])
st.parts.remove('D4')

print('\n# 6 - 7. the D11 posts up, D6 still on (published: 86.5, 88.8; 84.5, 70.5)')
for i, reach in (('D11_C', 86.5), ('D11_D', 88.8), ('D11_A', 84.5), ('D11_B', 70.5)):
    test(f'P6/7 {i} up {reach}', st, [i], Y, reach)
staged('P6/7 alt: all four posts, tabs up out of D1 (6.38), then up 78.62', st, D11S, [(Y, 6.38), (Y, 78.62)])
test('P6/7 alt: D6 up 44.7 with the posts still in', st, ['D6'], Y, 44.7, record=True)
up638 = st.copy(poses={**st.poses, **{i: [0.0, 6.38, 0.0] for i in D11S}})
test('P6/7 alt: the four posts and D6 lifted together, 80 up, once the tabs are out of D1', up638, D11S + ['D6'], Y, 80.0)
WAYS['P6_first_stage'] = first_stage('P6/7 D11_A', st, ['D11_A'], Y, 84.5)
st.parts = [i for i in st.parts if i not in D11S]

print('\n# 8. D6 up 44.7')
test('P8 D6 up 44.7', st, ['D6'], Y, 44.7)
st.parts.remove('D6')

print('\n# 9. the LED matrix with D10 (and the sockets) up to P_HELD, then laid aside at P_OUTSIDE (the published 9c pose)')
MAT = ['MATRIX', 'D10'] + SOCKETS
P_HELD, P_LIFT, P_OUTSIDE = [-0.2, 56.64, -0.32], [-90.76, 56.64, 25.09], [-90.76, 5.89, 25.09]
test('P9 matrix + D10 up 56.64 to P_HELD', st, MAT, Y, 56.64)
held = st.copy(poses={**st.poses, **{i: P_HELD for i in MAT}})
d = np.subtract(P_LIFT, P_HELD)
test('P9 matrix + D10 from P_HELD over to P_LIFT (above where D4 was)', held, MAT, d, float(np.linalg.norm(d)))
test('P9 matrix + D10 down from P_LIFT to P_OUTSIDE', held.copy(poses={**st.poses, **{i: P_LIFT for i in MAT}}), MAT, -Y, 50.75)
d = np.subtract(P_OUTSIDE, P_HELD)
test('P9 alt: matrix + D10 from P_HELD to P_OUTSIDE in a straight line', held, MAT, d, float(np.linalg.norm(d)))
# the wires there: the Full Build's shapes were drawn with D10 off the matrix at LIFT and OUTSIDE (it joined it held, Step 31)
for view, pose, what in (('Step 31c', P_HELD, 'HELD'), ('Step 30', P_LIFT, 'LIFT'), ('Step 26c', P_OUTSIDE, 'OUTSIDE')):
    wires = V[view]['wires'] if what != 'LIFT' else {w: n for w, n in zip(('wire white', 'wire grey', 'wire purple'), (56, 57, 58))}
    for w in ('wire white', 'wire grey', 'wire purple'):
        static(f'P9 static: D10 riding the matrix at P_{what} against {w} (route {wires[w]})', mesh('D10', pose), wire_mesh(w, wires[w]))
for i in ('MATRIX', 'D10'):
    static(f'P9 static: {i} at P_OUTSIDE against the USB cable', mesh(i, P_OUTSIDE), wire_mesh('usb cable', SEATED_WIRES['usb cable']))
    static(f'P9 static: {i} at P_OUTSIDE against the USB A end', mesh(i, P_OUTSIDE), mesh('USB_A'))
st = st.copy(poses={**st.poses, **{i: P_OUTSIDE for i in MAT}}, wires=dict(V['Step 26c']['wires']))

print('\n# 10. both D9 up 54.4 (the matrix aside, its wires in the OUTSIDE shape)')
for i in ('D9_A', 'D9_B'):
    test(f'P10 {i} up 54.4', st, [i], Y, 54.4)
WAYS['P10_first_stage'] = first_stage('P10 D9_A', st, ['D9_A'], Y, 54.4, only=('+X', '-X'))
st.parts = [i for i in st.parts if i not in ('D9_A', 'D9_B')]

print('\n# 11 - 13. the three pins out of i2, b19 and i3 (30 up, the Full Build\'s way reversed), the USB plug still in')
for i in ('J_WHITE_M', 'J_PURPLE_M', 'J_GREY_M'):
    test(f'P11-13 {i} up 30 (USB plug in)', st, [i], Y, 30.0, skip=('wire:wire white', 'wire:wire grey', 'wire:wire purple'))
static('P11-13 static: the purple pin against the USB plug', mesh('J_PURPLE_M'), mesh('USB_B'))
static('P11-13 static: the purple wire (route 67, as seated) against the USB plug', wire_mesh('wire purple', 67), mesh('USB_B'))

print('\n# 14 - 15. on their own: the matrix as held, with D10 and the sockets')
iso = State(MAT, {i: P_HELD for i in MAT})
test('P14 D10 down 48.4 off the matrix (published)', iso, ['D10'], -Y, 48.4)
WAYS['P14'] = other_ways('P14 D10', iso, ['D10'], 48.4)
staged('P14 alt: the Full Build\'s Step 31 reversed (+Z 40 along the matrix, then down 22)', iso, ['D10'], [(Z, 40.0), (-Y, 22.0)])
staged('P14 alt: -Z 40 along the matrix, then down 22', iso, ['D10'], [(-Z, 40.0), (-Y, 22.0)])
iso.parts.remove('D10')
test('P15 the three sockets +Z 30.5 off the pins', iso, SOCKETS, Z, 30.5)

st = st.copy(parts=[i for i in st.parts if i not in MAT + PINS], wires={w: n for w, n in st.wires.items() if not w.startswith('wire ')})

print('\n# 16. D3 out -Z 38.4 (D4 and D5 off)')
test('P16 D3 -Z 38.4', st, ['D3'], -Z, 38.4)
WAYS['P16'] = other_ways('P16 D3', st, ['D3'], 38.4)
st.parts.remove('D3')

print('\n# 17. D2 with the button +Z (the published 17c pose is D2 57.1 out: our D2_OUT); the button\'s pins out of j5 and j16')
D2SET = ['D2', 'BUTTON', 'NUT']
test('P17 D2 + button +Z 57.1 (USB plug in)', st, D2SET, Z, 57.1, skip=('wire:lead red', 'wire:lead black'))
WAYS['P17'] = other_ways('P17 D2', st, D2SET, 57.1, skip=('wire:lead red', 'wire:lead black'))
for i in ('BTN_RED_PIN', 'BTN_BLACK_PIN'):
    test(f'P17 {i} straight up 12 out of its hole', st, [i], Y, 12.0, skip=('wire:lead red', 'wire:lead black'))

print('\n# 18 - 19. on their own: D2 57.1 out, the button, its pins riding behind it as the Full Build\'s Step 19 carries them')
PIN_REL = {i: V['Step 19']['carry'][i]['pose'] for i in ('BTN_RED_PIN', 'BTN_BLACK_PIN')}
iso2 = State(D2SET + list(PIN_REL), {**{i: [0.0, 0.0, 57.1] for i in D2SET},
                                     **{i: compose([0.0, 0.0, 57.1], p) for i, p in PIN_REL.items()}})
test('P18 the nut -Z 85 off the button, over the pins', iso2, ['NUT'], -Z, 85.0)
iso2.parts.remove('NUT')
test('P19 the button, its pins riding, +Z 94.8 out of D2', iso2, ['BUTTON'] + list(PIN_REL), Z, 94.8)

print('\n# 20. the USB plug out (our Full Build: +Z 25; the published arrow 63.3, no motion)')
st = st.copy(parts=[i for i in st.parts if i not in D2SET + ['BTN_RED_PIN', 'BTN_BLACK_PIN']],
             wires={w: n for w, n in st.wires.items() if not w.startswith('lead ')})
USB = ['USB_B', 'USB_A']
test('P20 the USB plug +Z 25 (the matrix\'s pins already out)', st, USB, Z, 25.0, skip=('wire:usb cable',))
test('P20 alt: the USB plug +Z 25 with the purple pin still in b19 (our draft\'s order)',
     st.copy(parts=st.parts + ['J_PURPLE_M']), USB, Z, 25.0, skip=('wire:usb cable',))
st.parts = [i for i in st.parts if i not in USB]

print('\n# 21 - 24. the 330 ohm resistor, the capacitor, the 12 kOhm resistor, the Nano Board, each up')
for i, reach in (('R330', 30.3), ('CAP', 29.1), ('R12K', 31.3), ('NANO', 31.0)):
    test(f'P21-24 {i} up {reach}', st, [i], Y, reach)
    st.parts.remove(i)
test('check: the Nano up 31 with the 12 kOhm resistor still in', State(['D1', 'BREADBOARD', 'NANO', 'R12K']), ['NANO'], Y, 31.0)
test('check: the 330 ohm resistor up 30.3 with the USB plug still in', State(['D1', 'BREADBOARD', 'NANO', 'R330', 'USB_B']), ['R330'], Y, 30.3)

print('\n# the wires against the walls\' moves')
test('wires: D5 +X 54.1 against the matrix wires as seated (routes 65 - 67)',
     State(['D5'], wires={w: n for w, n in SEATED_WIRES.items() if w.startswith('wire ')}), ['D5'], X, 54.1)
test('wires: D4 -X 75.2 against the matrix wires as seated', State(['D4'], wires={w: n for w, n in SEATED_WIRES.items() if w.startswith('wire ')}),
     ['D4'], -X, 75.2)
test('wires: D4 -X 75.2 along the USB cable (route 41)', State(['D4'], wires={'usb cable': SEATED_WIRES['usb cable']}), ['D4'], -X, 75.2)
test('wires: D4 up 65 off the USB cable, after -X 8', State(['D4'], {'D4': [-8.0, 0.0, 0.0]}, {'usb cable': SEATED_WIRES['usb cable']}), ['D4'], Y, 65.0)
test('wires: D4 up 65 off the USB cable, after -X 75.2', State(['D4'], {'D4': [-75.2, 0.0, 0.0]}, {'usb cable': SEATED_WIRES['usb cable']}),
     ['D4'], Y, 65.0)

# ================================================================ the joints that hold, measured along lines through them
# intervals(part, line): where a line (through `at`, along `axis`) is inside the part, from its surface crossings.
def intervals(part, at, axis, pose=None, span=150.0):
    m = mesh(part, pose)
    e = np.zeros(3)
    e[axis] = 1.0
    o = np.asarray(at, float).copy()
    o[axis] -= span
    loc, _, _ = m.ray.intersects_location([o], [e], multiple_hits=True)
    if not len(loc):
        return []
    c = np.unique(np.round(np.sort(loc[:, axis]), 3))
    return [(round(float(a), 2), round(float(b), 2)) for a, b in zip(c[0::2], c[1::2])]


def gaps(iv, lo, hi):
    """The free stretches between `lo` and `hi` along a line, given a part's intervals on it."""
    out, x = [], lo
    for a, b in iv:
        if b <= lo or a >= hi:
            continue
        if a > x:
            out.append((round(x, 2), round(a, 2)))
        x = max(x, b)
    if x < hi:
        out.append((round(x, 2), round(hi, 2)))
    return out


JOINTS = []


def joint(label, holder, hole_at, tab, tab_ats, axis, window):
    """A tab of `tab` through a hole in `holder`: the hole along the line through hole_at (axis), and the tab's extent along lines
    through each of tab_ats (where it is beyond the holder, i.e. what the holder must pass over). Overhang = how far the tab there
    reaches past the hole's edges."""
    hole = gaps(intervals(holder, hole_at, axis), *window)
    hole = [h for h in hole if h[1] - h[0] > 0.3]
    rows = []
    for at in tab_ats:
        iv = [t for t in intervals(tab, at, axis) if t[1] > window[0] and t[0] < window[1]]
        over = []
        for a, b in iv:
            near = min(hole, key=lambda h: abs((h[0] + h[1]) / 2 - (a + b) / 2)) if hole else None
            if near:
                over.append(round(max(0.0, near[0] - a, b - near[1]), 2))
        rows.append(dict(at=at, tab=iv, overhang=over))
    print(f'{label}: the hole in {holder} along {"XYZ"[axis]} through {hole_at}: {hole}')
    for r in rows:
        print(f'    {tab} through {r["at"]}: {r["tab"]}  reaches past the hole by {r["overhang"]} mm')
    JOINTS.append(dict(label=label, holder=holder, tab=tab, hole=hole, rows=rows))


print('\n# the joints')
joint("D2's end tab in D5 (beyond D5's outer face, x 682.51)", 'D5', [681.0, 0, 1253.43], 'D2',
      [[x, 0, 1253.43] for x in (682.0, 682.7, 683.5, 685.0)], 1, (855.0, 909.0))
joint("D3's end tab in D5", 'D5', [681.0, 0, 1155.18], 'D3', [[x, 0, 1155.18] for x in (682.0, 682.7, 683.5, 685.0)], 1, (855.0, 909.0))
joint("D2's end tab in D4 (beyond D4's outer face, x 594.41)", 'D4', [595.9, 0, 1253.43], 'D2',
      [[x, 0, 1253.43] for x in (595.0, 594.2, 593.5, 591.5)], 1, (855.0, 909.0))
joint("D3's end tab in D4", 'D4', [595.9, 0, 1155.18], 'D3', [[x, 0, 1155.18] for x in (595.0, 594.2, 593.5, 591.5)], 1, (855.0, 909.0))
joint("D10's end in D4", 'D4', [595.9, 0, 1204.47], 'D10', [[x, 0, 1204.47] for x in (595.0, 594.2)], 1, (855.0, 909.0))
joint("D10's end in D5", 'D5', [681.0, 0, 1204.47], 'D10', [[x, 0, 1204.47] for x in (682.0, 682.7)], 1, (855.0, 909.0))
joint("D1's tab in D2 (beyond D2's outer face, z 1254.93)", 'D2', [631.54, 0, 1253.43], 'D1',
      [[631.54, 0, z] for z in (1254.0, 1255.2, 1256.5, 1258.0)], 1, (850.0, 870.0))
joint("D1's tab in D3 (beyond D3's outer face, z 1153.68)", 'D3', [644.81, 0, 1155.18], 'D1',
      [[644.81, 0, z] for z in (1155.0, 1153.4, 1152.0, 1150.5)], 1, (850.0, 870.0))
joint("D1's tab in D4", 'D4', [595.9, 0, 1197.34], 'D1', [[x, 0, 1197.34] for x in (595.9, 594.2, 593.9)], 1, (850.0, 870.0))
joint("D9_A's end in its notch in D2 (along X)", 'D2', [0, 901.5, 1253.43], 'D9_A', [[0, y, 1253.43] for y in (899.0, 895.0)], 0, (612.0, 626.0))
joint("D9_A's end in its notch in D2, at the notch's narrowest", 'D2', [0, 901.8, 1253.43], 'D9_A', [[0, 899.0, 1253.43]], 0, (612.0, 626.0))
for y in (931.0, 932.5, 933.5, 934.5, 935.5):
    joint(f'D11_A in D8\'s slot (along Z): D8 at y 930.8, the post at y {y}', 'D8', [674.83, 930.8, 0], 'D11_A', [[674.83, y, 0]], 2, (1225.0, 1260.0))
for y in (856.5, 858.0, 859.0):
    joint(f"D11_A's tab in D1's slot: D1 at y 860.9, the tab at y {y}", 'D1', [674.83, 860.9, 0], 'D11_A', [[674.83, y, 0]], 2, (1225.0, 1260.0))
    joint(f"D11_A's tab against D6's corner slot: D6 at y 902.5, the tab at y {y}", 'D6', [674.83, 902.5, 0], 'D11_A', [[674.83, y, 0]], 2,
          (1225.0, 1260.0))
for y in (902.5, 905.0, 910.0, 913.0, 915.0):
    joint(f'D11_A in D6\'s corner slot (along Z): the post at y {y}', 'D6', [674.83, 902.5, 0], 'D11_A', [[674.83, y, 0]], 2, (1225.0, 1260.0))
joint("D10's hooks over the matrix's edges (along X): the matrix at y 895", 'MATRIX', [0, 895.0, 1204.47], 'D10',
      [[0, y, 1204.47] for y in (899.0, 898.5, 897.9, 895.0, 892.0)], 0, (590.0, 690.0))

json.dump(dict(method=__doc__, results=RESULTS, other_ways=WAYS, joints=JOINTS), open(OUT, 'w'), indent=1,
          default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
print('->', OUT)
