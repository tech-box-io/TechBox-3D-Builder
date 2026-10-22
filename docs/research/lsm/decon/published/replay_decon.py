"""TechBox's published LSM take-apart (Cadasio 19075-laser_stem_matrix_lsm_-_deconstruction), replayed step by step, in OUR terms.

    .venv.nosync/bin/python -I docs/research/lsm/decon/published/replay_decon.py      (about 2 s, under 100 MB)

Reads (never writes them):
    docs/research/lsm/cadasio/raw/19075-laser_stem_matrix_lsm_-_deconstruction.json   (the getProjectViewer payload)
    LSM Build Instructions/assembly-report.json                                       (our ids <- Cadasio instance names)
    docs/research/lsm/decon/arrows/published_arrows.json                              (cross-check of the arrows)
Writes docs/research/lsm/decon/published/published_steps.json.

How the payload is read (docs/research/guide_19075-...deconstruction.md, "Data caveat", and tools/cadasio/*.py):
  * Every step's `properties` change the state left by the step before, in `orderedSteps` order, hidden steps included.
  * Visibility is per leaf solid: its start value is "no node of its chain has hidden: true in the tree"; from then on only the
    leaf's own `visible` counts (steps never set it on a node with children).
  * `position` / `rotation` (quaternion) replace a node's local translation / turn in its parent's frame (three.js object.position /
    quaternion). World placement = the chain's local matrices multiplied out. Scene units / SF = our assembly mm (SF =
    assemblyStructure.scaleFactor = 0.47846); Cadasio's frame IS our assembly frame (assemble.py placed our parts at its placements).
  * A part's pose = its world matrix now x inverse(world matrix of the copy OUR part was placed at, at home), written as stepgen's
    turned() (t, axis + degrees, about `at` = our part's seated box centre), so it can go straight into a guide.py pose. Our parts
    were nudged up to ~1 mm off Cadasio's seat by assemble.py; the pose keeps our nudge.
  * The steps also name 578 ids that are not in the tree (stale copies from an earlier CAD import): no geometry, ignored, except the
    Step 19 eye, whose leader is tied to one (a "Black Push Button" solid): placed with Push button-2's frame (approximate).
  * Camera: cameraProperties.default_camera, changed by each step's `default_camera`; fov 45 (no step changes it). Our view:
    view_dir = unit(position - target), radius = distance * sin(fov / 2) / 1.08 (player/js/core.js cameraPose, padding 1.08).
  * Eyes / close-ups: toolbox images; the eye is the one PNG used 40 times; any other image (but the two on Start) is a close-up.
    Each has one link: targetId (a leaf) and data.target (a point in that leaf's own frame, scene units) = the ring of its leader.
    A close-up's `height` is its picture's height / width.
"""
import collections, json, math, re, sys
from pathlib import Path
import numpy as np
from scipy.spatial.transform import Rotation

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / 'docs/research/lsm/cadasio/raw/19075-laser_stem_matrix_lsm_-_deconstruction.json'
REPORT = ROOT / 'LSM Build Instructions/assembly-report.json'
ARROWS = ROOT / 'docs/research/lsm/decon/arrows/published_arrows.json'
OUT = Path(__file__).resolve().parent / 'published_steps.json'

j = json.load(open(SRC))
steps, order, A, tcp = j['steps'], j['orderedSteps'], j['assemblyStructure'], j['toolboxComponentsProperties']
SF = A['scaleFactor']; MM = 1.0 / SF
rv = A['rootVersions']
EYE_SRC = 'ASS3e405c2c-ac76-88fc-a2d0-31bb66a7ae52.png'

# ------------------------------------------------------------------ the tree
refs = {}


def walk(n, parent):
    r = n['rootReference']
    t = [float(x) for x in r['transform'].split(',')] if r.get('transform') else None
    m = np.array(t).reshape(4, 4).T if t and len(t) == 16 else np.eye(4)
    refs[r['id']] = dict(name=r['name'], parent=parent, hidden=bool(r.get('hidden')), ver=r.get('childVersionId'),
                         kids=[c['rootReference']['id'] for c in n.get('children') or []], R=m[:3, :3].copy(), t=m[:3, 3].copy())
    for c in n.get('children') or []:
        walk(c, r['id'])


walk(A, None)
ROOTID = A['rootReference']['id']


def chain(k):
    out = []
    while k is not None:
        out.append(k); k = refs[k]['parent']
    return out                        # leaf first, root last


leaves = [k for k, v in refs.items() if not v['kids']]
CH = {k: chain(k) for k in refs}
TOP = {k: (CH[k][-2] if len(CH[k]) >= 2 else k) for k in refs}
TOPS = refs[ROOTID]['kids']
top_leaves = collections.defaultdict(list)
for k in leaves:
    top_leaves[TOP[k]].append(k)
NAME = {k: refs[k]['name'] for k in refs}
BY_NAME = {NAME[t]: t for t in TOPS}


def short(k):
    return NAME[k].split('/')[-1]


def kd_hex(mtl):
    m = re.search(r'Kd\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)', mtl or '')
    return '#%02x%02x%02x' % tuple(max(0, min(255, round(float(x) * 255))) for x in m.groups()) if m else None


BASE_COL = {k: kd_hex((rv.get(refs[k]['ver']) or {}).get('versionMtlData')) for k in leaves}


def leaf_box(k):
    v = rv.get(refs[k]['ver']) or {}
    if v.get('versionMinX') is None:
        return None
    return np.array([v['versionMin' + a] for a in 'XYZ']) * MM, np.array([v['versionMax' + a] for a in 'XYZ']) * MM


BOX = {k: leaf_box(k) for k in leaves}

# ------------------------------------------------------------------ our ids
rep = json.load(open(REPORT))
OURS = {}                                   # Cadasio top-level name -> our id (the seated copy our part was placed at)
for pid, v in rep.items():
    c = v.get('cadasio')
    if c and pid != 'NUT':
        OURS.setdefault(c, pid)
OUR_BOX = {pid: (np.array(v['lo']), np.array(v['hi'])) for pid, v in rep.items() if v.get('lo')}
NUT_LEAF = 'Push button-Boss-Extrude6'      # the nut solid of 'Push button' (Step 18's eye is on it; box 21 x 18 x 1.5 mm)

# Copies of our parts elsewhere in the tree, and the twin each pose is measured against.
TWIN_OF_KIND = {'8x8 LED': '8x8 LED-4', 'LSM_MatrixSupportSmall_r2': 'LSM_MatrixSupportSmall_r2-1', 'LSM_Side3_r2': 'LSM_Side3_r2-1',
                'Push button': 'Push button-1', 'LSM_Lens_Bottom': 'LSM_Lens_Bottom-3', 'USB Cable end': 'USB Cable end-2'}
# The wire bodies and jumper caps, read from colour and place (published_steps.md, "Wires"): our wire ids are guide.py's.
C2 = '^LSM Lab - Chapter 2-1'
EXTRA = {
    'Part25' + C2: ('wire white', 'seated route (Start - Step 9)'), 'Part26' + C2: ('wire grey', 'seated route'),
    'Part27' + C2: ('wire purple', 'seated route'),
    'Part28' + C2: ('wire white', 'with the matrix hovering (Step 9 Transition)'), 'Part29' + C2: ('wire grey', 'hovering'),
    'Part30' + C2: ('wire purple', 'hovering'),
    'Part31' + C2: ('wire white', 'matrix laid aside, still in the breadboard (Step 9c - 11)'),
    'Part32' + C2: ('wire grey', 'laid aside, plugged (9c - 13)'), 'Part33' + C2: ('wire purple', 'laid aside, plugged (9c - 12)'),
    'Copy of Part39' + C2: ('wire white', 'loose, unplugged (11c - 15)'), 'Copy of Part40' + C2: ('wire purple', 'loose (12c - 15)'),
    'Copy of Part41' + C2: ('wire grey', 'loose (13c - 15)'),
    'Part10' + C2: ('lead red', 'seated route to j5 (Start - 17)'), 'Part9' + C2: ('lead black', 'seated route to j16 (Start - 17)'),
    'Part40' + C2: ('lead red', 'straight, unplugged (17c - 19)'), 'Part39' + C2: ('lead black', 'straight, unplugged (17c - 19)'),
    'Part23' + C2: ('usb cable', 'seated (Start - 20)'),
    'Wire Cap V2-4': ('J_WHITE_M', 'in i2'), 'Wire Cap V2-7': ('J_GREY_M', 'in i3'), 'Wire Cap V2-1': ('J_PURPLE_M', 'in b19'),
    'Wire Cap V2-3': ('BTN_RED_PIN', 'in j5'), 'Wire Cap V2-9': ('BTN_BLACK_PIN', 'in j16'),
    'Wire Cap V2-28': ('J_WHITE_M copy', 'white plug, unplugged'), 'Wire Cap V2-31': ('J_PURPLE_M copy', 'purple plug, unplugged'),
    'Wire Cap V2-32': ('J_GREY_M copy', 'grey plug, unplugged'),
    'Wire Cap V2-10': ('BTN_RED_PIN copy', 'red plug, unplugged'), 'Wire Cap V2-11': ('BTN_BLACK_PIN copy', 'black plug, unplugged'),
    'Wire Cap-21': ('J_WHITE_F copy', 'on the matrix hovering / isolated (and a duplicate at the laid-aside matrix, 11c - 13c)'),
    'Wire Cap-22': ('J_PURPLE_F copy', 'hovering / isolated'), 'Wire Cap-23': ('J_GREY_F copy', 'hovering / isolated'),
    'Wire Cap-17': ('J_WHITE_F copy', 'on the matrix laid aside'), 'Wire Cap-19': ('J_PURPLE_F copy', 'laid aside'),
    'Wire Cap-18': ('J_GREY_F copy', 'laid aside'),
}
FEMALE_SEATED = {'J_WHITE_F': 'Wire Cap-14', 'J_PURPLE_F': 'Wire Cap-15', 'J_GREY_F': 'Wire Cap-16'}


def kind(name):
    return re.sub(r'-\d+$', '', name)


def our_id(t, leaf=None):
    """Our id for a top-level Cadasio part (or one of its solids: the nut)."""
    n = NAME[t]
    nut = leaf is not None and short(leaf) == NUT_LEAF and kind(n) == 'Push button'
    if n in OURS:
        return 'NUT' if nut else OURS[n]
    if n in EXTRA:
        return EXTRA[n][0]
    tw = TWIN_OF_KIND.get(kind(n))
    if tw and tw in OURS:
        return ('NUT' if nut else OURS[tw]) + ' copy'
    return None


def twin(t):
    n = NAME[t]
    if n in OURS:
        return t
    tw = TWIN_OF_KIND.get(kind(n))
    return BY_NAME.get(tw) if tw else None


def is_stem(t):
    return NAME[t].startswith('LSM_Stem-')


# ------------------------------------------------------------------ state and geometry
vis = {k: not any(refs[a]['hidden'] for a in CH[k]) for k in refs}
pos, rot, col = {}, {}, {}
tb = {k: dict(v) for k, v in tcp.items()}
for t in tb.values():
    t.setdefault('visible', False)
cam = dict((j.get('cameraProperties') or {}).get('default_camera') or {})
FOV = float(cam.get('fov') or 45.0)


def v3(d):
    return np.array([float(d.get('x', 0)), float(d.get('y', 0)), float(d.get('z', 0))])


def local(k, home=False):
    m = np.eye(4)
    r = refs[k]
    if not home and k in rot:
        q = rot[k]; m[:3, :3] = Rotation.from_quat([q.get('x', 0), q.get('y', 0), q.get('z', 0), q.get('w', 1)]).as_matrix()
    else:
        m[:3, :3] = r['R']
    m[:3, 3] = (pos[k] if (not home and k in pos) else r['t']) * MM
    return m


def world(k, home=False):
    m = np.eye(4)
    for a in reversed(CH[k][:-1]):          # (the root's transform is the identity)
        m = m @ local(a, home)
    return m


def below_top(k):
    m = np.eye(4)
    c = CH[k]
    for a in reversed(c[:c.index(TOP[k])]):
        m = m @ local(a, True)
    return m


HOME_TOP = {}


def home_top(t):
    if t not in HOME_TOP:
        HOME_TOP[t] = world(t, home=True)
    return HOME_TOP[t]


def leaf_top(k):
    """The top-level part's world matrix implied by one leaf's placement now."""
    return world(k) @ np.linalg.inv(below_top(k))


def world_box(ks):
    los, his = [], []
    for k in ks:
        b = BOX.get(k)
        if b is None:
            continue
        lo, hi = b
        c = np.array([[x, y, z, 1] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
        w = (world(k) @ c.T).T[:, :3]
        los.append(w.min(0)); his.append(w.max(0))
    if not los:
        return None
    return np.min(los, 0), np.max(his, 0)


def r2(v, n=2):
    return [round(float(x), n) for x in v]


def pose_of(M, pivot):
    """stepgen._pose_of: a 4x4 placement as a pose turned about `pivot`."""
    c = np.asarray(pivot, float)
    t = M[:3, :3] @ c + M[:3, 3] - c
    turn = Rotation.from_matrix(M[:3, :3]).as_rotvec()
    ang = float(np.linalg.norm(turn))
    if ang < 1e-6:
        return r2(t)
    return dict(t=r2(t), r=r2(turn / ang, 4) + [round(math.degrees(ang), 2)], at=r2(c))


def groups_of(t, ks):
    """Leaves of a part split by their (our-id, placement) so that a nut that moves apart is its own group."""
    g = collections.OrderedDict()
    for k in ks:
        M = leaf_top(k)
        key = (our_id(t, k), tuple(np.round(M[:3, 3], 2)), tuple(np.round(M[:3, :3].ravel(), 3)))
        g.setdefault(key, []).append(k)
    return g


def describe(t, ks, M):
    """Where a (group of a) part is: its box, and its pose from OUR seated part (or from its CAD home, for wires and caps)."""
    o = our_id(t, ks[0])
    box = world_box(ks)
    d = dict(ours=o, cadasio=NAME[t], solids=f'{len(ks)}/{len(top_leaves[t])}')
    if box:
        d['box_mm'] = [r2(box[0]), r2(box[1])]
        d['centre_mm'] = r2((box[0] + box[1]) / 2)
    if NAME[t] in EXTRA:
        d['what'] = EXTRA[NAME[t]][1]
    if kind(NAME[t]) in ('Wire Cap V2', 'Wire Cap'):
        d.update(plug_info(t, ks))
    tw = twin(t)
    if tw is not None and o:
        Dl = M @ np.linalg.inv(home_top(tw))
        pid = o.replace(' copy', '')
        pivot = (OUR_BOX[pid][0] + OUR_BOX[pid][1]) / 2 if pid in OUR_BOX else Dl[:3, 3]
        ps = pose_of(Dl, pivot)
        d['pose_from_built'] = ps
        d['dist_from_built_mm'] = round(float(np.linalg.norm(ps['t'] if isinstance(ps, dict) else ps)), 2)
    return d


def cam_view(c):
    p, t = v3(c['position']) * MM, v3(c['orbit_target']) * MM
    d = p - t; dist = float(np.linalg.norm(d)); u = d / dist
    out = dict(position=r2(p), target=r2(t), fov=FOV, distance=round(dist, 2), view_dir=r2(u, 4),
               radius=round(dist * math.sin(math.radians(FOV / 2)) / 1.08, 2),
               elevation=round(math.degrees(math.asin(max(-1, min(1, u[1])))), 1), azimuth=round(math.degrees(math.atan2(u[0], u[2])), 1))
    if c.get('rotation'):
        q = c['rotation']; R = Rotation.from_quat([q['x'], q['y'], q['z'], q['w']]).as_matrix()
        up_cam, fwd = R[:, 1], -R[:, 2]
        yproj = np.array([0, 1.0, 0]) - fwd * fwd[1]; yproj /= np.linalg.norm(yproj)
        out['roll_deg'] = round(math.degrees(math.atan2(np.dot(np.cross(yproj, up_cam), fwd), np.dot(yproj, up_cam))), 2)
    return out


def plug_info(t, ks):
    """A jumper cap: its long axis, which end the pin is at (the silver solid of a male cap), its tip and its back (wire) end."""
    box = world_box(ks)
    if box is None:
        return {}
    size = box[1] - box[0]
    ax = int(np.argmax(size))
    out = dict(axis='xyz'[ax], length_mm=round(float(size[ax]), 2))
    pins = [k for k in ks if (col.get(k) or BASE_COL.get(k) or '').lower() in ('#a6a9aa', '#b1b3b3', '#c0c0c0')]
    if pins and len(pins) < len(ks):
        pb = world_box(pins); c_all = (box[0] + box[1]) / 2; c_pin = (pb[0] + pb[1]) / 2
        sgn = 1.0 if c_pin[ax] > c_all[ax] else -1.0
        tip = c_all.copy(); tip[ax] = box[1][ax] if sgn > 0 else box[0][ax]
        back = c_all.copy(); back[ax] = box[0][ax] if sgn > 0 else box[1][ax]
        d = np.zeros(3); d[ax] = sgn
        out.update(pin_dir=r2(d, 0), pin_tip_mm=r2(tip), wire_end_mm=r2(back))
    return out


def kind_of_step(name, behaviour):
    if name == 'Start':
        return 'start'
    if name == 'Completed View':
        return 'end'
    if behaviour == 'play':
        return 'transition'
    if re.match(r'^Step \d+c$', name):
        return 'Nc'
    if re.match(r'^Step \d+$', name):
        return 'N'
    return behaviour


def collapse_stems(items, key='ours'):
    """64 stems as one entry (they always act together here)."""
    stems = [x for x in items if (x.get(key) or '').startswith('STEM_')]
    rest = [x for x in items if not (x.get(key) or '').startswith('STEM_')]
    if stems:
        e = dict(ours='STEM_01 .. STEM_64', cadasio='LSM_Stem-* (64)', n=len(stems))
        for f in ('step_move_mm', 'step_move_dist', 'step_turn_deg', 'pose_from_built', 'dist_from_built_mm'):
            if f in stems[0]:
                vals = [json.dumps(s.get(f)) for s in stems]
                e[f] = stems[0][f] if len(set(vals)) == 1 else f'{len(set(vals))} different values; first {stems[0][f]}'
        rest.insert(0, e)
    return rest


# ------------------------------------------------------------------ walk
records = []
prev_groups = {}            # (top, our id) -> (leaves, matrix)
prev_vis = {}
frame = -1
SNAP = {}                   # frame -> {(top, our id): matrix, box} (for the checks below)
SPECIFICS = []              # the matrix, D10, wires and plugs, D2 and the button, at the steps asked about
EVER = set()                # top-level parts shown in at least one viewer step
SPEC_STEPS = {'Step 9': 'with_next', 'Step 9c': 1, 'Step 10': 1, 'Step 11c': 1, 'Step 12c': 1, 'Step 13c': 1, 'Step 14': 'with_next', 'Step 14c': 1,
              'Step 15': 'with_next', 'Step 15c': 1, 'Step 17': 1, 'Step 17c': 1, 'Step 18': 'with_next', 'Step 18c': 1, 'Step 19': 'with_next'}
for idx, sid in enumerate(order):
    s = steps[sid]
    for k, p in (s.get('properties') or {}).items():
        if not isinstance(p, dict):
            continue
        if k in refs:
            if p.get('visible') is not None:
                vis[k] = bool(p['visible'])
            if isinstance(p.get('position'), dict):
                pos[k] = v3(p['position'])
            if isinstance(p.get('rotation'), dict):
                rot[k] = p['rotation']
            if p.get('colour_main'):
                col[k] = p['colour_main']
        elif k in tb:
            for a, b in p.items():
                if a == 'visible' and b is None:
                    continue
                tb[k][a] = b
        elif k == 'default_camera':
            cam.update(p)
    if s.get('behaviour') == 'hidden':
        continue
    frame += 1
    cur_vis, cur_groups = {}, {}
    for t in TOPS:
        ks = [k for k in top_leaves[t] if vis[k]]
        if not ks:
            continue
        cur_vis[t] = ks
        for (o, _, _), gks in groups_of(t, ks).items():
            key = (t, o)
            if key in cur_groups:                 # same id, two placements (Cadasio's own loose solids): keep the larger group
                if len(gks) <= len(cur_groups[key][0]):
                    continue
            cur_groups[key] = (gks, leaf_top(gks[0]))
    SNAP[frame] = {key: dict(M=M, box=world_box(gks), n=len(gks)) for key, (gks, M) in cur_groups.items()}
    EVER.update(t for (t, o) in cur_groups)
    if s['name'] in SPEC_STEPS or (s['name'].startswith('Trans') and SPEC_STEPS.get(records[-1]['name'] if records else '') == 'with_next'):
        SPECIFICS.append(dict(frame=frame, name=s['name'], parts=[describe(t, gks, M) for (t, o), (gks, M) in cur_groups.items()
                                                                  if not is_stem(t) and (NAME[t] in EXTRA or twin(t) is not None and NAME[t] not in OURS
                                                                                         or (o or '').startswith(('MATRIX', 'D10', 'D2', 'BUTTON', 'NUT')))]))
    appear = [key for key in cur_groups if key not in prev_groups]
    gone = [key for key in prev_groups if key not in cur_groups]
    moved = []
    for key, (gks, M) in cur_groups.items():
        if key not in prev_groups:
            continue
        a = prev_groups[key][1]
        dR = Rotation.from_matrix(M[:3, :3] @ a[:3, :3].T).magnitude()
        if np.linalg.norm(M[:3, 3] - a[:3, 3]) > 0.05 or dR > 1e-3:
            box = world_box(gks)
            c_now = (box[0] + box[1]) / 2
            c_prev = (a @ np.linalg.inv(M) @ np.append(c_now, 1))[:3]
            moved.append(dict(describe(key[0], gks, M), step_move_mm=r2(c_now - c_prev), step_move_dist=round(float(np.linalg.norm(c_now - c_prev)), 2),
                              step_turn_deg=round(math.degrees(dR), 2)))
    def faded(t, o):
        d = dict(ours=o, cadasio=NAME[t])
        ks = [k for k in top_leaves[t] if our_id(t, k) == o] or top_leaves[t]
        M = leaf_top(ks[0])
        Mp = prev_groups[(t, o)][1]
        if np.linalg.norm(M[:3, 3] - Mp[:3, 3]) > 0.05 or Rotation.from_matrix(M[:3, :3] @ Mp[:3, :3].T).magnitude() > 1e-3:
            dd = describe(t, ks, M)
            d['faded_at'] = {k: dd[k] for k in ('pose_from_built', 'centre_mm', 'box_mm') if k in dd}
            d['note'] = 'moved in the same step that hides it (it fades at the new place)'
        return d

    partial = [dict(ours=our_id(t), cadasio=NAME[t], solids_before=len(prev_vis[t]), solids_now=len(ks), of=len(top_leaves[t]))
               for t, ks in cur_vis.items() if t in prev_vis and len(prev_vis[t]) != len(ks)
               and not any((t, o) in appear or (t, o) in gone for (tt, o) in list(cur_groups) + list(prev_groups) if tt == t)]

    # annotations
    eyes, insets, titles, arrows, labels, lines = [], [], [], [], [], []
    for k, t in tb.items():
        if not t.get('visible'):
            continue
        ty = t.get('type')
        if ty == 'image':
            src = ((t.get('content') or {}).get('src') or '').split('/')[-1].split('?')[0]
            links = [l for l in (t.get('links') or []) if isinstance(l, dict)]
            ring, on = None, None
            if links:
                leaf = links[0].get('targetId')
                p_loc = v3((links[0].get('data') or {}).get('target') or {}) * MM
                if leaf in refs:
                    ring = r2((world(leaf) @ np.append(p_loc, 1))[:3])
                    on = dict(ours=our_id(TOP[leaf], leaf), cadasio=NAME[TOP[leaf]], solid=short(leaf))
                else:                       # (Step 19: a button solid no longer in the tree; Push button-2's frame)
                    pb = BY_NAME['Push button-2']
                    ks = [k for k in top_leaves[pb] if short(k) != NUT_LEAF]
                    ring = r2((leaf_top(ks[0]) @ np.append(p_loc, 1))[:3])
                    on = dict(ours='BUTTON copy', cadasio='Push button-2 (approx.: the solid named is not in the tree)', solid=leaf)
            entry = dict(name=t.get('name'), ring_mm=ring, on=on, screen_pos_pct=t.get('position'), ring_screen_pct=t.get('target_position'),
                         width_pct=t.get('width'), framed=(t.get('container') or {}).get('container_type'))
            if src == EYE_SRC:
                eyes.append(entry)
            elif not links:
                titles.append(dict(name=t.get('name'), src=src, screen_pos_pct=t.get('position'), width_pct=t.get('width'), aspect_h_over_w=t.get('height')))
            else:
                entry.update(src=src, aspect_h_over_w=t.get('height'))
                insets.append(entry)
        elif ty == 'arrow':
            p0, p1 = v3(t['points'][0]) * MM, v3(t['points'][-1]) * MM
            L = float(np.linalg.norm(p1 - p0)); sc = float(t.get('scale') or 1.0)
            oid = t.get('object_ids') or []
            oid = list(oid.values()) if isinstance(oid, dict) else list(oid)
            on = oid[0] if oid else None
            arrows.append(dict(name=t.get('name'), tail_mm=r2(p0), tip_mm=r2(p1), length_mm=round(L, 2), dir=r2((p1 - p0) / L, 4),
                               shaft_mm=round(float(t.get('body_width')) * sc * MM, 3), head_w_mm=round(float(t.get('head_width')) * sc * MM, 2),
                               head_l_mm=round(float(t.get('head_length')) * sc * MM, 2),
                               placed_on=(our_id(TOP[on], on) or NAME[TOP[on]]) if on in refs else None))
        elif ty == 'editor':
            labels.append(dict(name=t.get('name'), text=re.sub(r'<[^>]+>', '', t.get('editor_contents') or '')[:60]))
        elif ty == 'line':
            lines.append(t.get('name'))

    shown = collections.Counter()
    unmapped = []
    n_stems = 0
    for (t, o), (gks, M) in cur_groups.items():
        if is_stem(t):
            n_stems += 1
        elif o:
            shown[o] += 1
        else:
            unmapped.append(f'{NAME[t]} ({len(gks)}/{len(top_leaves[t])})')
    rec = dict(frame=frame, order_index=idx, name=s['name'], kind=kind_of_step(s['name'], s.get('behaviour')), duration_ms=s.get('animationDuration'),
               shown=dict(ours=sorted(shown), stems=n_stems, unmapped_cadasio=sorted(unmapped)),
               appear=collapse_stems([describe(t, *cur_groups[(t, o)]) for (t, o) in appear]),
               disappear=collapse_stems([faded(t, o) for (t, o) in gone]),
               partial_visibility_change=partial,
               moved=collapse_stems(moved),
               camera=cam_view(cam) if cam.get('position') and cam.get('orbit_target') else None,
               eyes=eyes, insets=insets, arrows=arrows)
    if titles:
        rec['title_images'] = titles
    if labels:
        rec['labels'] = labels
    if lines:
        rec['lead_lines'] = lines
    records.append(rec)
    prev_groups, prev_vis = cur_groups, cur_vis

prev = None
for r in records:
    c = r['camera']
    r['camera_moves'] = prev is None or bool(np.max(np.abs(np.subtract(c['position'], prev['position']))) > 0.05
                                             or np.max(np.abs(np.subtract(c['target'], prev['target']))) > 0.05)
    prev = c

# ------------------------------------------------------------------ checks
checks = {}
try:
    pa = json.load(open(ARROWS))['arrows']
    by = collections.defaultdict(list)
    for a in pa:
        by[a['frame']].append(a)
    bad = []
    for r in records:
        mine = sorted((tuple(a['tail_mm']), tuple(a['tip_mm'])) for a in r['arrows'])
        theirs = sorted((tuple(a['tail_mm']), tuple(a['tip_mm'])) for a in by.get(r['frame'], []))
        if len(mine) != len(theirs) or any(np.max(np.abs(np.subtract(m[0], t[0]))) > 0.02 for m, t in zip(mine, theirs)):
            bad.append(r['frame'])
    checks['arrows'] = f'{len(pa)} arrow showings in arrows/published_arrows.json; frames that differ from this replay: {bad or "none"}'
except FileNotFoundError:
    checks['arrows'] = 'arrows/published_arrows.json not found'
# the female caps: carried back by the matrix copy they are shown with (less the trio's common shift, ~1.2 mm in Cadasio's copies),
# each should land on the seated cap (Wire Cap-14 / -15 / -16) of the colour it is mapped to
SEATED_F = {}
for pid, nm in FEMALE_SEATED.items():
    k = top_leaves[BY_NAME[nm]][0]
    SEATED_F[pid] = (world(k, True) @ np.append((BOX[k][0] + BOX[k][1]) / 2, 1))[:3]
fc = []
for f, groups in SNAP.items():
    mats = [(t, g['M']) for (t, o), g in groups.items() if kind(NAME[t]) == '8x8 LED']
    if not mats:
        continue
    t_m, M_m = mats[0]
    D = M_m @ np.linalg.inv(home_top(BY_NAME['8x8 LED-4']))
    caps = {}
    for (t, o), g in groups.items():
        if NAME[t] in EXTRA and kind(NAME[t]) == 'Wire Cap' and o and o.endswith('_F copy'):
            c = (g['box'][0] + g['box'][1]) / 2
            caps[NAME[t]] = (o, (np.linalg.inv(D) @ np.append(c, 1))[:3])
    if not caps:
        continue
    near = {nm: v for nm, v in caps.items() if min(np.linalg.norm(v[1] - q) for q in SEATED_F.values()) < 5}
    shift = (np.mean([v[1] for v in near.values()], 0) - np.mean([SEATED_F[v[0].replace(' copy', '')] for v in near.values()], 0)) if near else np.zeros(3)
    for nm, (o, back) in caps.items():
        best = min(SEATED_F, key=lambda pid: np.linalg.norm(back - shift - SEATED_F[pid]))
        bd = float(np.linalg.norm(back - shift - SEATED_F[best]))
        fc.append(f'[{f:02d}] {nm} (with {NAME[t_m]}; common shift {r2(shift)}) -> {best} at {bd:.2f} mm; mapped {o}'
                  + ('' if o.startswith(best) else '  MISMATCH') + ('' if nm in near else '  (not at a header: a stray copy)'))
checks['female_caps'] = sorted(set(fc))

GLITCHES = [
    "Step name 'Transiton' (frame 38, Step 14's transition).",
    "Step 4: its Transition moves nothing; D5 gets its +54.1 mm X offset in Step 4c, the step that hides it (it fades there; no hover frame).",
    "Step 4c also hides the four D11 posts; they are back at Step 5 and really come off at Steps 6 - 7.",
    "D3 is hidden from Step 1 to Step 9c (its plate is back at Step 10, its engraved sheets at Step 16) although it is on until Step 16; the "
    "Step 4 and Step 5 eyes are tied to D3 and point at an empty corner.",
    "The seated LED matrix (8x8 LED-4) is never shown: no matrix from Start to Step 9; it appears already hovering in Step 9's Transition "
    "(8x8 LED-5, a model swap, not a tween) and is swapped again for one laid aside at 9c (8x8 LED-6).",
    "Step 9 reuses Step 8's arrow unchanged (it starts where D6 was, not on the matrix).",
    "Step 9 Transition: the three male plugs in the breadboard (Wire Cap V2-1/-4/-7) are hidden, though the hovering wires still reach the "
    "breadboard; back at 9c. The hovering wires also loop out to z 1259.7, through D2 (outer face z 1254.9).",
    "Wire Cap-21 (white female cap) is shown a second time on the laid-aside matrix from 11c, on top of Wire Cap-17, which is hidden at 13c "
    "(when the grey wire is unplugged): duplicate solids, no visible effect.",
    "Step 14's isolated view puts the matrix back at its hovering place (8x8 LED-5: 56.6 mm above its seat, not turned), not where it was laid "
    "aside; the D10 copy keeps the laid-aside half turn (D10 is symmetric, so it does not show).",
    "The laid-aside matrix floats at its seated height + 5.9 mm (bottom y 896.5; the base's underside is y 859.4): beside the box only "
    "because there is no floor.",
    "Step 19 pushes the button out (+Z) with its wires and plugs passing through D2's button hole.",
    "Step 20 has an arrow and an eye but no motion: the USB cable (both ends and the cable) just fades at 20c.",
    "The matrix wires are unplugged white (i2), purple (b19), grey (i3): neither the build's order nor its reverse.",
    "Arrow sizes vary for no reason (5 of 24 depart from 5 : 20 : 15-17; per-arrow scale makes Step 15's and Step 18's heavy, Step 22's thin).",
    "Step 4's eye has a light-blue box round it (the other 16 have none); Step 16's close-up frame is clipped at the bottom.",
    "The Nano is 2.08 mm above its CAD seat from Start (the USB plug and the A end with it); some of its solids toggle at Steps 1, 2, 8 "
    "(a 2.3 mm z shift), 20c, 21 and 24. R330 shows 8 of its 10 solids from Step 2, R12K 8 of 10 throughout, the USB plug 2 of 3.",
    "D11_B / C / D are hidden for Step 1 only; the breadboard's backing sheet (BACKING) is on until Step 16c.",
    "The steps name 578 ids not in the tree (stale copies from an earlier CAD import): no geometry; the Step 19 eye is tied to one (a button "
    "solid), so its ring is placed with Push button-2's frame (on the button's front face).",
    "A hidden authoring step 'Step 51' precedes Start; 69 lead lines, 10 labels (hole names i2, i3, b19, j5, j16 ...), 16 arrows and 36 images "
    "of the project are never shown.",
]
mapping = {}
for t in sorted(EVER, key=lambda t: NAME[t]):
    if is_stem(t):
        continue
    o = our_id(t)
    mapping[NAME[t]] = dict(ours=o, why=(EXTRA[NAME[t]][1] if NAME[t] in EXTRA else 'assembly-report.json "cadasio"' if NAME[t] in OURS
                                         else f'a copy of {twin(t) and NAME[twin(t)]}' if twin(t) else None))
    if kind(NAME[t]) == 'Push button':
        mapping[NAME[t]]['nut_solid'] = NUT_LEAF + (' -> NUT' if NAME[t] in OURS else ' -> NUT copy')
mapping['LSM_Stem-* (64)'] = dict(ours='STEM_01 .. STEM_64', why='assembly-report.json "cadasio"')
never = sorted(NAME[t] for t in TOPS if t not in EVER)
meta_extra = dict(mapping=mapping, unmapped_shown=sorted(k for k, v in mapping.items() if not v['ours']), never_shown=never, glitches=GLITCHES)

meta = dict(source=str(SRC.relative_to(ROOT)), scale_factor=SF, fov=FOV, frames=len(records),
            note='mm in our assembly frame (Y up). pose_from_built: stepgen turned() pose relative to OUR seated part (t, axis+degrees, '
                 'at = our part\'s seated box centre). "<id> copy" = another CAD copy of that part (a posed copy), measured against our seated '
                 'part. step_move_mm: box-centre displacement since the viewer step before. camera.radius = distance * sin(fov/2) / 1.08 '
                 '(our cameraPose). Wire bodies and caps are mapped by colour and place (EXTRA in replay_decon.py); their boxes are given, '
                 'not poses (no seated twin).',
            checks=checks, **meta_extra)
# The loose and re-routed wires, end to end, from their boxes and their caps (no wire meshes in the payload: each wire's own shape
# inside its box is not known; a loose one lies in the plane of its thin box side, from its female cap to the top of its male plug).
COLOUR = {'wire white': 'WHITE', 'wire purple': 'PURPLE', 'wire grey': 'GREY', 'lead red': 'RED', 'lead black': 'BLACK'}
wire_runs = []
for sp in SPECIFICS:
    parts = sp['parts']
    for w in parts:
        if not (w.get('ours') or '').startswith(('wire ', 'lead ')) or 'seated' in (w.get('what') or ''):
            continue
        c = COLOUR[w['ours']]
        male = [q for q in parts if (q.get('ours') or '').startswith((f'J_{c}_M', f'BTN_{c}_PIN'))]
        female = [q for q in parts if (q.get('ours') or '').startswith(f'J_{c}_F')]
        lo, hi = np.array(w['box_mm'][0]), np.array(w['box_mm'][1])
        run = dict(frame=sp['frame'], step=sp['name'], wire=w['ours'], cadasio=w['cadasio'], what=w.get('what'), box_mm=w['box_mm'],
                   thin_axis='xyz'[int(np.argmin(hi - lo))], thin_axis_at=round(float(((lo + hi) / 2)[int(np.argmin(hi - lo))]), 2))
        if male:
            m = male[0]
            run['male_plug'] = dict(ours=m['ours'], cadasio=m['cadasio'], pin_tip_mm=m.get('pin_tip_mm'), wire_end_mm=m.get('wire_end_mm'),
                                    pin_dir=m.get('pin_dir'))
        if female:
            f = female[-1]
            fc = np.array(f['centre_mm']); fb = np.array(f['box_mm'])
            ax = int(np.argmax(fb[1] - fb[0]))
            # the wire leaves the cap on the side its box reaches into
            end = fc.copy(); end[ax] = hi[ax] if abs(hi[ax] - fc[ax]) < abs(lo[ax] - fc[ax]) else lo[ax]
            run['female_cap'] = dict(ours=f['ours'], cadasio=f['cadasio'], centre_mm=r2(fc))
            if fb[0][ax] - 0.5 <= end[ax] <= fb[1][ax] + 0.5:       # (only where the wire's box ends inside the cap: not the hovering loops)
                run['female_cap']['wire_starts_mm'] = r2(end)
        wire_runs.append(run)
json.dump(dict(meta=meta, steps=records, specifics=SPECIFICS, wire_runs=wire_runs), open(OUT, 'w'), indent=1)
print(len(records), 'viewer steps ->', OUT)
print(checks['arrows'])
print('\n'.join(checks['female_caps']))
