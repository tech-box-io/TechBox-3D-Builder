"""Compute insertion directions for each build step from the MRA CAD.

Order and wording come from MRA Build Notes (source of truth). For each step, the
moving parts are tested against the parts already in place: a direction is free if
the moving parts can slide that way without passing through anything.
"""
import json, sys
import numpy as np
import trimesh

GLB = sys.argv[1]
OUT = sys.argv[2]

scene = trimesh.load(GLB)
g = scene.graph
parents = g.transforms.parents
ROOT = 'ARA_Pathways'

def top_of(node):
    while parents.get(node) not in (ROOT, None):
        node = parents[node]
    return node

inst_meshes = {}
for node in g.nodes_geometry:
    T, geom = g[node]
    m = scene.geometry[geom].copy()
    m.apply_transform(T)
    m.apply_scale(1000.0)  # mm
    inst_meshes.setdefault(top_of(node), []).append(m)
inst = {k: trimesh.util.concatenate(v) for k, v in inst_meshes.items()}
for m in inst.values():
    m.merge_vertices()
INSET = 0.2  # mm, contact tolerance
MIN_BLOCK = 1.2  # mm; overlaps shallower than this are snug fits, not obstructions (boards are 3mm)

def inset_pts(m):
    return m.vertices - m.vertex_normals * INSET

# CAD instance ids (top-level node names) used in the build
B1, B2, B4, B5, B6a, B6b, B8, B9, B10 = 'NAUO1 NAUO2 NAUO3 NAUO4 NAUO5 NAUO6 NAUO7 NAUO8 NAUO9'.split()
# CAD file names ARA_R5 / ARA_R6 are swapped relative to the engraving on the wood; these follow the engraving.
R1, R2, R3, R4, R6, R5 = 'NAUO10 NAUO11 NAUO12 NAUO13 NAUO14 NAUO15'.split()
BASE_SERVO, BASE_HORN = 'NAUO45', 'NAUO46'
SCREWS = ['NAUO47', 'NAUO48', 'NAUO49', 'NAUO50', 'NAUO51', 'NAUO52']
JOY_L, JOY_R, MODULE = 'NAUO80', 'NAUO81', 'NAUO82'
JOY_WIRES = ['NAUO111', 'NAUO112'] + ['NAUO%d' % i for i in range(95, 111)]

# Student-facing names follow the build notes, not the CAD file names.
LABEL = {R1: 'R1', R2: 'R2', R3: 'R3', R4: 'R4', R5: 'R5', R6: 'R6', B1: 'B1', B2: 'B2',
         B10: 'B3', B4: 'B4', B5: 'B5', B6a: 'B6', B6b: 'B6', B8: 'B7', B9: 'B8',
         BASE_SERVO: 'Base Servo', JOY_L: 'Left Joystick', JOY_R: 'Right Joystick',
         MODULE: 'I/O Extension Module'}

def union(ids):
    return trimesh.util.concatenate([inst[i] for i in ids]) if ids else None

AXES = [np.array(v, float) for v in ([0, 1, 0], [1, 0, 0], [-1, 0, 0], [0, 0, 1], [0, 0, -1], [0, -1, 0])]

def sample(pts, n=5000, seed=0):
    if len(pts) <= n:
        return pts
    return pts[np.random.default_rng(seed).choice(len(pts), n, replace=False)]

def blocked(mov, sta, d, reach):
    """True if sliding `mov` along d by `reach` mm would pass through `sta`."""
    eps = 0.05
    for src, dst, dirn in ((mov, sta, d), (sta, mov, -d)):
        pts = inset_pts(src)
        if src is sta:  # only stationary points in the swept region matter
            lo, hi = mov.bounds
            lo = np.minimum(lo, lo + d * reach) - 1
            hi = np.maximum(hi, hi + d * reach) + 1
            pts = pts[np.all((pts >= lo) & (pts <= hi), axis=1)]
            if not len(pts):
                continue
        pts = sample(pts)
        o = pts + dirn * eps
        locs, idx, _ = dst.ray.intersects_location(o, np.repeat([dirn], len(o), 0), multiple_hits=False)
        if len(idx):
            dist = np.einsum('ij,j->i', locs - o[idx], dirn)
            if np.any((dist > MIN_BLOCK) & (dist < reach)):
                return True
    return False

def free_dirs(moving, stationary):
    mov = union(moving)
    sta = union(stationary)
    size = float(np.linalg.norm(mov.extents))
    reach = max(25.0, 0.8 * size)
    if sta is None:
        return [AXES[0]], reach
    return [d for d in AXES if not blocked(mov, sta, d, reach + 5)], reach

def pick(dirs):
    return dirs[0] if dirs else None  # AXES order = preference (from above first)

# Steps follow MRA Build Notes, Chapter 2 (Base and Controller).
steps = []
placed = []

def card(caption, flag=None):
    steps.append({'kind': 'card', 'caption': caption, 'flag': flag})

def place(caption, add, move=None, labels=None, against=None, stage_of=None, flag=None, appear=None, path=None):
    move = move or add
    sta = against if against is not None else [p for p in placed + add if p not in move]
    if path is not None:  # motion set by a person (two-part moves, threaded screws)
        dirs, auto = [], False
    else:
        dirs, reach = free_dirs(move, sta)
        d = pick(dirs)
        auto = True
        if d is None:
            flag = (flag + ' ' if flag else '') + 'No straight-line path found in the CAD: motion set by hand, needs review.'
            path = [[0, 40, 0], [0, 0, 0]]
            auto = False
        else:
            path = [(d * reach).round(1).tolist(), [0, 0, 0]]
    st = {'kind': 'place', 'caption': caption, 'add': add, 'move': move, 'path': path, 'auto': auto,
          'free': [x.astype(int).tolist() for x in dirs], 'labels': labels or [], 'flag': flag,
          'stage_of': stage_of, 'appear': appear or []}
    steps.append(st)
    placed.extend([a for a in add if a not in placed] + [a for a in (appear or []) if a not in placed])
    print(f"{caption[:55]:55s} auto={auto} path={path} free={st['free']}")
    return st

card('Before you start, disconnect all servos from the I/O extension module.')
place('Begin with R1.', [R1], labels=[{'id': R1, 'text': 'R1'}])
place('Insert the base servo into R2, then add R2.', [R2, BASE_SERVO], labels=[{'id': R2, 'text': 'R2'}, {'id': BASE_SERVO, 'text': 'Base Servo'}],
      flag='The build notes do not say when the base servo goes in. This placement comes from the video and CAD.')
for r in (R3, R4, R5, R6):
    place(f'Add {LABEL[r]}.', [r], labels=[{'id': r, 'text': LABEL[r]}])
turret = [R1, R2, R3, R4, R5, R6, BASE_SERVO]
place('Once R1 - R6 are together, attach R1 - R6 to B2.', [B2, BASE_HORN], move=turret, against=[B2],
      labels=[{'id': B2, 'text': 'B2'}])
base = turret + [B2, BASE_HORN]
place('Then screw B2 onto B1 with 6mm screws.', [B1], move=base, against=[B1], labels=[{'id': B1, 'text': 'B1'}])
place('Screw B2 onto B1 with six 6mm screws.', SCREWS, path=[[0, 25, 0], [0, 0, 0]], labels=[{'id': SCREWS[0], 'text': '6mm Screw x6'}])
place('Insert B3 into B2.', [B10], labels=[{'id': B10, 'text': 'B3'}])
place('Insert B4 into B2.', [B4], labels=[{'id': B4, 'text': 'B4'}])
STAGE = [-170, 80, 0]  # where subassemblies are built 'in hand', beside the model (mm)
# Subassemblies built in hand: joystick into its two walls, then the group onto B3.
place('Place the left joystick (the joystick connected to A3) into B5 and B6.', [B5, B6a, JOY_L], move=[JOY_L],
      against=[B5, B6a], stage_of=[B5, B6a, JOY_L],
      labels=[{'id': JOY_L, 'text': 'Left Joystick'}, {'id': B5, 'text': 'B5'}, {'id': B6a, 'text': 'B6'}],
      flag='The joystick model overlaps B5 and B6 in the CAD, so no clear path could be calculated.')
steps[-1]['stage'] = STAGE
st = place('Then place B5 and B6 onto B3.', [], move=[B5, B6a, JOY_L])
st['path'] = [STAGE, [0, 80, 0], [0, 0, 0]]
place('Place the right joystick into B6 and B7.', [B6b, B8, JOY_R], move=[JOY_R], against=[B6b, B8],
      stage_of=[B6b, B8, JOY_R],
      labels=[{'id': JOY_R, 'text': 'Right Joystick'}, {'id': B6b, 'text': 'B6'}, {'id': B8, 'text': 'B7'}],
      flag='The joystick model overlaps B6 and B7 in the CAD, so no clear path could be calculated.')
steps[-1]['stage'] = STAGE
st = place('Then place B6 and B7 onto B3.', [], move=[B6b, B8, JOY_R])
st['path'] = [STAGE, [0, 80, 0], [0, 0, 0]]
place('Attach B8 on top of B5 - B7.', [B9], labels=[{'id': B9, 'text': 'B8'}])
place('Slide the extension module through the slots in B6 on top of B4.', [MODULE], appear=JOY_WIRES,
      path=[[0, 6, 70], [0, 6, 0], [0, 0, 0]],
      flag='Two-part move (slide through the B6 slots, then drop onto B4). The slide was found from the CAD; the drop was set by hand.',
      labels=[{'id': MODULE, 'text': 'I/O Extension Module'}])
card('Reconnect the servo to 5. Remember brown to G, red to V, and orange to S.', flag='Wiring is not animated in this test.')
card('Move the servo wire into the L-shaped slot in R4.', flag='Wiring is not animated in this test.')
card('Connect the power cable to the nano.', flag='Wiring is not animated in this test.')

json.dump({'labels': LABEL, 'steps': steps}, open(OUT, 'w'), indent=1)
print('steps:', len(steps))
