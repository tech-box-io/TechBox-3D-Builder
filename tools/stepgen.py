"""Build-guide generator: turns a short, readable guide script into the steps file the player shows.

A kit folder holds a `guide.py` that lists the build in order (which part goes on next, the caption,
and any hand-set motion). This module works out everything that can be derived from the CAD:

  * the direction each part can be inserted from (it must not pass through anything already built);
  * where its joints are (tab into slot, pin into socket, screw into hole) so the red lead lines can
    run from the feature on the moving part to the feature that receives it;
  * a label anchor on each new part;
  * a camera that keeps the whole exploded arrangement in frame and looks across the motion.

House rules it applies (from TechBox's published Cadasio guides, see docs/cadasio-patterns.md):
one part or one action per step; every step is a pair "Step N" (part hovering, lead lines and labels
on) and "Step Nc" (part seated, annotations off); the camera never moves inside a pair.

All coordinates written to steps.json are millimetres in assembly space, Y up.

Poses. Wherever a part's position in a view is given it is a pose, relative to where the part sits when
built: [x, y, z] (moved), or {"t": [x, y, z], "r": [ax, ay, az, degrees], "at": [px, py, pz]} (turned about
an axis through the point `at`, then moved). `turned()` writes the second form.

Wires. Flexible leads are not CAD parts: each is a centre line (a "route") that the player draws as a tube.
A route is tied to the part at each of its ends, so the wire follows them when they move, and a wire can
change route from one step to the next (the player bends it across). See tools/wires.py for making routes.

Riding parts. A plug on the loose end of a lead, or the cap on a jumper wire, is a CAD part that has no
place of its own until it is plugged in: `carry()` makes it ride with another part (the servo, the joystick)
from when that part appears until a step moves it to its seat.

More than one guide per kit. The Full Build writes steps.json (and parts.json). `chapter()` marks where each Part begins: the
same run also writes each Part as a guide of its own (steps-<slug>.json, its steps the Full Build's) and chapters.json, the map
between them; `in_part()` and `note(only_in=)` give a Part what it has of its own. A guide that is not a cut of the Full Build is
a script of its own in the kit folder with Guide(steps_file='steps-<name>.json'): a deconstruction starts with `take_apart()`
(the Full Build as it ends) and takes it apart with `remove()`, `unplug()` and `lift()` (Step N: the parts where they are, with
their cue; Step Nc: they have gone, or lie where they were put, the view carrying `leaving` and their ways for the player). Every
guide of a kit uses the kit's one model.glb, which holds the parts all of them show (publish.py sends each guide only its own).
"""
import copy
import hashlib
import json
import re
from pathlib import Path

import numpy as np
import trimesh
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation

AXES = [np.array(v, float) for v in ([0, 1, 0], [1, 0, 0], [-1, 0, 0], [0, 0, 1], [0, 0, -1], [0, -1, 0])]  # preference order: from above first

# Defaults measured from TechBox's published guides (docs/cadasio-patterns.md gives the numbers behind each).
DEFAULTS = dict(
    hover_face_on=65.0,    # mm: a flat panel pushed along its own normal onto tabs
    hover_min=40.0,        # mm: a part sliding lengthwise hovers 1.0 x its own length, kept within these limits
    hover_max=140.0,
    hover_other=80.0,      # mm: any other part (e.g. a panel going in edge-first); small parts hover about their own size instead
    hover_fastener=60.0,   # mm: screw, nut, washer or knob along its axis
    contact_tolerance=0.2, # mm inset used when testing whether a slide is blocked
    snug_fit=1.2,          # mm; overlaps shallower than this are press fits, not obstructions (boards are 3 mm)
    max_lead_lines=4,      # the published guides show 1, 2 or 4 lead lines per step (never 3; more than 4 on two frames in a thousand)
    view_elevation=35.0,   # degrees above the horizon for the standard three-quarter view
    fov=45.0,              # camera field of view in degrees (the player reads it from steps.json)
    frame_padding=1.08,    # how loosely the camera frames the fit sphere
)


# ---------------------------------------------------------------- poses
def _rot(pose):
    """The 3x3 turn of a pose, or None if it only moves."""
    if isinstance(pose, dict) and pose.get('r') and pose['r'][3]:
        ax = np.asarray(pose['r'][:3], float)
        ax = ax / np.linalg.norm(ax)
        a = np.radians(pose['r'][3])
        K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
        return np.eye(3) + np.sin(a) * K + (1 - np.cos(a)) * K @ K
    return None


def _shift(pose):
    if pose is None:
        return np.zeros(3)
    return np.asarray(pose.get('t', [0, 0, 0]) if isinstance(pose, dict) else pose, float)


def model_stamp(path):
    """A model's version, as steps files name it (model.glb?v=...): from its content, so that it holds on any computer and
    after any git checkout (a file's date does not)."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:12]


def step_text_file(steps_file):
    """The step-text file of a guide's steps file: step-text.json for the Full Build (and so its Parts), step-text-<name>.json for
    a guide of its own (steps-<name>.json)."""
    return 'step-text.json' if steps_file == 'steps.json' else 'step-text-' + steps_file[len('steps-'):-len('.json')] + '.json'


def apply_pose(pose, pts):
    """Where seated points are when their part is at `pose`."""
    pts, R = np.asarray(pts, float), _rot(pose)
    if R is None:
        return pts + _shift(pose)
    at = np.asarray(pose.get('at', [0, 0, 0]), float)
    return (pts - at) @ R.T + at + _shift(pose)


def unapply_pose(pose, pts):
    pts, R = np.asarray(pts, float), _rot(pose)
    if R is None:
        return pts - _shift(pose)
    at = np.asarray(pose.get('at', [0, 0, 0]), float)
    return (pts - at - _shift(pose)) @ R + at


def turn_dir(pose, v, back=False):
    R = _rot(pose)
    v = np.asarray(v, float)
    return v if R is None else (v @ R if back else v @ R.T)


def turned(axis, degrees, at, t=(0, 0, 0)):
    """A pose: turned by `degrees` about `axis` through the point `at` (seated mm), then moved by `t`."""
    return dict(t=[float(x) for x in t], r=[float(x) for x in axis] + [float(degrees)], at=[float(x) for x in at])


def _matrix(pose):
    M, R = np.eye(4), _rot(pose)
    if R is None:
        M[:3, 3] = _shift(pose)
    else:
        at = np.asarray(pose.get('at', [0, 0, 0]), float)
        M[:3, :3], M[:3, 3] = R, at - R @ at + _shift(pose)
    return M


def compose(outer, inner, pivot=(0, 0, 0)):
    """The pose of a part that is at `inner` and is then carried along by `outer`, written as a turn about `pivot`
    (give the part's own middle, so that it glides sensibly when a later step moves it)."""
    if _rot(outer) is None and not np.any(_shift(outer)):
        return inner if inner is not None else [0.0, 0.0, 0.0]
    return _pose_of(_matrix(outer) @ _matrix(inner), pivot)


def relative_pose(outer, pose, pivot=(0, 0, 0)):
    """compose() undone: the pose `inner` for which compose(outer, inner, pivot) is `pose` (where a part that is at `pose` rides
    on a carrier that is at `outer`)."""
    return _pose_of(np.linalg.inv(_matrix(outer)) @ _matrix(pose), pivot)


def _moved(pose):
    """True if a pose is not the seat."""
    return pose is not None and (_rot(pose) is not None or bool(np.any(np.abs(_shift(pose)) > 1e-6)))


def _shifted(pose, by):
    """A pose moved on by `by` mm (assembly space)."""
    by = np.asarray(by, float)
    if isinstance(pose, dict):
        return dict(pose, t=(_shift(pose) + by).round(3).tolist())
    return (_shift(pose) + by).round(3).tolist()


def _pose_of(M, pivot):
    """A 4x4 placement as a pose, written as a turn about `pivot`."""
    c = np.asarray(pivot, float)
    t = M[:3, :3] @ c + M[:3, 3] - c
    turn = Rotation.from_matrix(M[:3, :3]).as_rotvec()
    angle = float(np.linalg.norm(turn))
    if angle < 1e-7:
        return t.tolist()
    return dict(t=t.tolist(), r=(turn / angle).tolist() + [float(np.degrees(angle))], at=c.tolist())


class via(dict):
    """In a hand-set path: a pose the part passes through without pausing. Poses not wrapped in via() are stops,
    and the player gives each stretch between two stops one beat (800 ms)."""
    def __init__(self, pose):
        super().__init__(pose if isinstance(pose, dict) else dict(t=[float(x) for x in pose]))


def text_key(caption, occurrence=0):
    """The key a step's wording is edited under outside the guide (tools/step_text.py): a short code from the guide's own
    wording of the step and which step with that wording it is (0 for the first), so that neither two steps worded alike nor a
    word replaced all through a spreadsheet can send an edit to the wrong step."""
    return 'T' + hashlib.sha1(f'{caption}\n{occurrence}'.encode('utf-8')).hexdigest()[:8].upper()


def pose_out(pose):
    """A pose as it is written to steps.json (a plain [x, y, z] when there is no turn)."""
    if _rot(pose) is None:
        return np.round(_shift(pose), 1).tolist()
    return dict(t=np.round(_shift(pose), 2).tolist(), r=np.round(pose['r'], 6).tolist(), at=np.round(pose.get('at', [0, 0, 0]), 2).tolist())   # (a turn needs the extra digits)


# ---------------------------------------------------------------- CAD access
class Model:
    """The full-detail CAD export, one welded mesh per top-level instance, in mm.

    adjust: {id: pose} for parts the CAD has slightly out of place or the wrong way round (materials.json "adjust_mm":
    [x, y, z] to move it, or a pose {"t", "r", "at"} to turn it). own_parts: names of CAD nodes inside a part that are
    parts of their own in the guide (the Nano, which the CAD has inside the I/O module's assembly)."""

    def __init__(self, glb_path, scale_to_mm=1000.0, adjust=None, own_parts=(), extra_parts=None):
        scene = trimesh.load(glb_path)
        graph = scene.graph
        parents = graph.transforms.parents
        # Parts are the children of the assembly node; exports wrap everything in one such node under the scene base.
        under_base = [n for n in graph.nodes if parents.get(n) == graph.base_frame]
        root = under_base[0] if len(under_base) == 1 and under_base[0] not in graph.nodes_geometry else graph.base_frame
        own = set(own_parts)

        def top_of(node):
            while parents.get(node) not in (root, None) and node not in own:
                node = parents[node]
            return node

        grouped = {}
        for node in graph.nodes_geometry:
            transform, geom = graph[node]
            mesh = scene.geometry[geom].copy()
            mesh.apply_transform(transform)
            mesh.apply_scale(scale_to_mm)
            grouped.setdefault(top_of(node), []).append(mesh)
        for part_id, (path, pose) in (extra_parts or {}).items():   # parts that come as files of their own (materials.json "extra_parts")
            extra = trimesh.load(path)
            pieces = [extra.geometry[g].copy().apply_transform(extra.graph[n][0]) for n in extra.graph.nodes_geometry for g in [extra.graph[n][1]]] \
                if isinstance(extra, trimesh.Scene) else [extra.copy()]
            mesh = trimesh.util.concatenate(pieces)
            mesh.apply_scale(scale_to_mm)
            mesh.apply_transform(_matrix(pose))
            grouped[part_id] = [mesh]
        self.inst = {k: trimesh.util.concatenate(v) for k, v in grouped.items()}
        missing = own - set(self.inst)
        if missing:
            raise SystemExit(f'own_parts names nodes that are not in {Path(glb_path).name}: {sorted(missing)}')
        for name, mesh in self.inst.items():
            mesh.merge_vertices()
            if adjust and name in adjust:             # a part the CAD has slightly out of place (materials.json "adjust_mm")
                mesh.apply_transform(_matrix(adjust[name]))
        self._union_cache = {}

    def union(self, ids):
        key = tuple(ids)
        if key not in self._union_cache:
            self._union_cache[key] = trimesh.util.concatenate([self.inst[i] for i in ids]) if ids else None
        return self._union_cache[key]

    def bounds(self, ids, offsets=None):
        lo, hi = np.full(3, np.inf), np.full(3, -np.inf)
        for i in ids:
            b, pose = self.inst[i].bounds, (offsets or {}).get(i)
            if _rot(pose) is None:
                b = b + _shift(pose)
            else:                                     # a turned part: the box around its turned box (a little generous)
                corners = apply_pose(pose, [[b[x][0], b[y][1], b[z][2]] for x in (0, 1) for y in (0, 1) for z in (0, 1)])
                b = np.array([corners.min(0), corners.max(0)])
            lo, hi = np.minimum(lo, b[0]), np.maximum(hi, b[1])
        return lo, hi


# ---------------------------------------------------------------- insertion direction
def _sample(points, n=5000, seed=0):
    if len(points) <= n:
        return points
    return points[np.random.default_rng(seed).choice(len(points), n, replace=False)]


def blocked(mov, sta, d, reach, cfg):
    """True if sliding `mov` along d by `reach` mm would pass through `sta`."""
    eps = 0.05
    for src, dst, direction in ((mov, sta, d), (sta, mov, -d)):
        pts = src.vertices - src.vertex_normals * cfg['contact_tolerance']
        if src is sta:  # only stationary points inside the swept region matter
            lo, hi = mov.bounds
            lo = np.minimum(lo, lo + d * reach) - 1
            hi = np.maximum(hi, hi + d * reach) + 1
            pts = pts[np.all((pts >= lo) & (pts <= hi), axis=1)]
            if not len(pts):
                continue
        pts = _sample(pts)
        origins = pts + direction * eps
        locs, idx, tri = dst.ray.intersects_location(origins, np.repeat([direction], len(origins), 0), multiple_hits=False)
        if len(idx):
            dist = np.einsum('ij,j->i', locs - origins[idx], direction)
            hit = (dist > cfg['snug_fit']) & (dist < reach)
            # A first hit on the far side of a face means the ray began inside the other part. If it began only
            # skin-deep (a board edge resting in a slot), it is a press fit and does not block the slide.
            leaving = hit & (dst.face_normals[tri] @ direction > 0)
            if leaving.any():
                depth = trimesh.proximity.closest_point(dst, origins[idx][leaving])[1]
                hit[np.flatnonzero(leaving)[depth <= 0.4]] = False
            if hit.any():
                return True
    return False


def hover_distance(model, moving, direction, cfg):
    """How far off its seat a part is shown before it goes in.

    A flat panel pushed face-on (along its own normal) hovers a fixed distance. A part that slides
    lengthwise hovers its own length, so it clears what it slides past. Anything else hovers about
    80 mm, or about its own size if it is smaller than that, so the gap reads clearly on screen.
    """
    extents = model.union(moving).extents
    d = np.abs(np.asarray(direction, float) / np.linalg.norm(direction))
    thin = int(np.argmin(extents))
    if extents[thin] < 0.25 * np.sort(extents)[1] and d[thin] > 0.9:
        return cfg['hover_face_on']
    along = float(extents @ d)
    if along >= 0.8 * extents.max():
        return float(np.clip(along, cfg['hover_min'], cfg['hover_max']))
    return float(np.clip(max(along, 0.9 * extents.max()), cfg['hover_min'], cfg['hover_other']))


def free_directions(model, moving, stationary, cfg):
    """Axis directions the moving parts can be pulled away along without passing through anything."""
    mov, sta = model.union(moving), model.union(stationary)
    if sta is None:
        return [AXES[0]]
    reach = max(25.0, 0.8 * float(np.linalg.norm(mov.extents))) + 5
    return [d for d in AXES if not blocked(mov, sta, d, reach, cfg)]


# ---------------------------------------------------------------- joints (where lead lines attach)
def _side_contacts(a, b, d, spacing=0.8, back=0.3, gap=0.6, seed=0):
    """Points on a's side faces (facing across the insertion axis d) that touch b, with their normals."""
    normals = a.face_normals
    faces = np.flatnonzero(np.abs(normals @ d) < 0.35)
    if not len(faces):
        return np.zeros((0, 3)), np.zeros((0, 3))
    count = np.clip(np.ceil(a.area_faces[faces] / spacing ** 2).astype(int), 1, 400)
    f = np.repeat(faces, count)
    r = np.random.default_rng(seed).random((len(f), 2))
    s = np.sqrt(r[:, 0])
    bary = np.c_[1 - s, s * (1 - r[:, 1]), s * r[:, 1]]
    p = np.einsum('ij,ijk->ik', bary, a.triangles[f])
    n = normals[f]
    lo, hi = b.bounds
    keep = np.all((p >= lo - 1) & (p <= hi + 1), axis=1)
    p, n = p[keep], n[keep]
    if not len(p):
        return p, n
    origins = p - n * back
    locs, ray, _ = b.ray.intersects_location(origins, n, multiple_hits=False)
    if not len(ray):
        return np.zeros((0, 3)), np.zeros((0, 3))
    dist = np.einsum('ij,ij->i', locs - origins[ray], n[ray])
    ok = dist <= back + gap
    return p[ray][ok], n[ray][ok]


def _clusters(points, link):
    pairs = cKDTree(points).query_pairs(link, output_type='ndarray')
    n, labels = connected_components(coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(len(points), len(points))), directed=False)
    return [np.flatnonzero(labels == k) for k in range(n)]


def find_joints(model, moving, stationary, d):
    """Joints between the moving and stationary parts for an insertion along -d.

    A joint is a patch where the two touch on faces that run along the insertion axis: a tab's sides
    against a slot's walls, a pin in a socket, a screw in a hole. `locking` is True when the patch is
    gripped from opposite sides (a real tab-in-slot), False for a one-sided rub.
    Each joint: centre (mm), depth (extent along d), width (extent across d), locking.
    """
    d = np.asarray(d, float) / np.linalg.norm(d)
    mov, sta = model.union(moving), model.union(stationary)
    if mov is None or sta is None:
        return []
    p1, n1 = _side_contacts(mov, sta, d)
    p2, n2 = _side_contacts(sta, mov, d)
    p, n = np.vstack([p1, p2]), np.vstack([n1, -n2])
    joints = []
    if len(p) >= 4:
        for idx in _clusters(p, 3.6):
            if len(idx) < 4:
                continue
            q, m = p[idx], n[idx]
            along = q @ d
            across = q - np.outer(along, d)
            span = np.ptp(across, axis=0)
            joints.append(dict(centre=(q.max(0) + q.min(0)) / 2, depth=float(np.ptp(along)), width=float(np.linalg.norm(span)),
                               axis=span / (np.linalg.norm(span) + 1e-9), locking=bool(np.linalg.norm(m.mean(0)) < 0.75), n=len(idx), points=q))
    if joints:
        return joints
    # Nothing rubs sideways: fall back to where the surfaces simply meet (a part resting on another).
    pts = np.vstack([mov.vertices, mov.triangles_center])
    lo, hi = sta.bounds
    pts = pts[np.all((pts >= lo - 0.5) & (pts <= hi + 0.5), axis=1)]
    if len(pts) > 20000:
        pts = _sample(pts, 20000)
    if not len(pts):
        return []
    near = pts[np.abs(trimesh.proximity.signed_distance(sta, pts)) < 0.35]
    if len(near) < 3:
        return []
    for idx in _clusters(near, 4.0):
        if len(idx) < 3:
            continue
        q = near[idx]
        along = q @ d
        span = np.ptp(q - np.outer(along, d), axis=0)
        joints.append(dict(centre=(q.max(0) + q.min(0)) / 2, depth=float(np.ptp(along)), width=float(np.linalg.norm(span)),
                           axis=span / (np.linalg.norm(span) + 1e-9), locking=False, n=len(idx), points=q))
    return joints


def lead_points(joints, d, max_lines):
    """Lead-line anchors, one per joint: (tip on the moving part, mouth on the receiving part), seated coordinates.

    Long joints (a whole edge in a groove) get a line at each end. The published guides draw 1, 2 or 4
    lines, never 3 and almost never more: with more joints than that, the farthest-apart ones are kept
    so the lines still frame the part.
    """
    d = np.asarray(d, float) / np.linalg.norm(d)
    pool = [j for j in joints if j['locking']] or joints
    anchors = []

    def line_through(j, centre):
        # Take the line's two ends from the contact points that lie on it (within 2 mm, measured across the
        # insertion axis). A patch can merge two neighbouring joints of different depth; the box would overshoot.
        rel = j['points'] - centre
        along = rel @ d
        near = np.linalg.norm(rel - np.outer(along, d), axis=1) < 2.0
        lo, hi = (along[near].min(), along[near].max()) if near.any() else (-j['depth'] / 2, j['depth'] / 2)
        return centre + d * lo, centre + d * hi

    for j in pool:
        if j['width'] > 30:
            for sign in (-0.4, 0.4):
                anchors.append(line_through(j, j['centre'] + j['axis'] * j['width'] * sign))
        else:
            anchors.append(line_through(j, j['centre']))
    keep = max_lines if len(anchors) >= max_lines else 2 if len(anchors) == 3 else len(anchors)   # 1, 2 or 4: never 3
    if len(anchors) > keep:
        max_lines = keep
        pts = np.array([a[1] for a in anchors])
        chosen = [int(np.argmax(np.linalg.norm(pts - pts.mean(0), axis=1)))]
        while len(chosen) < max_lines:
            dist = np.min(np.linalg.norm(pts[:, None] - pts[chosen][None], axis=2), axis=1)
            chosen.append(int(np.argmax(dist)))
        anchors = [anchors[i] for i in sorted(chosen)]
    return anchors


def hand_lines(points):
    """Lead lines set by hand, as (tip, mouth) pairs like lead_points gives.

    Each entry is one point [x, y, z] that the line should run through (a spot on the tab, or on the slot
    it enters, as copied from the player with Option-click), or a pair [[tip], [mouth]] to set both ends.
    Seated coordinates in mm. A single point works for either part: the line is drawn from where that
    spot is while the part hovers to where it is once the part is seated.
    """
    anchors = []
    for p in points:
        a = np.asarray(p, float)
        if a.shape == (3,):
            anchors.append((a, a.copy()))
        elif a.shape == (2, 3):
            anchors.append((a[0], a[1]))
        else:
            raise ValueError(f'lines_at entries are [x, y, z] or [[x, y, z], [x, y, z]], not {p!r}')
    return anchors


def camera_eye(camera, cfg):
    """Where the player puts the camera for a view (landscape frame): far enough to fit the view's sphere."""
    dist = camera['radius'] / np.sin(np.radians(cfg['fov'] / 2)) * cfg['frame_padding']
    return np.asarray(camera['target'], float) + np.asarray(camera['dir'], float) * dist


def _hidden(model, point, eye, visible, offsets):
    """True if something stands between a point (already at its on-screen position) and the camera."""
    sight = eye - point
    sight = sight / np.linalg.norm(sight)
    for other in visible:
        pose = offsets.get(other)
        locs, _, _ = model.inst[other].ray.intersects_location([unapply_pose(pose, point + sight * 0.3)], [turn_dir(pose, sight, back=True)], multiple_hits=False)
        if len(locs):
            return True
    return False


def label_anchor(model, part_id, eye=None, visible=(), offsets=None):
    """A point on the part's surface for a label's leader to end on (seated coordinates).

    Given the camera position, picks the point nearest the part's middle that the camera can actually
    see (not hidden behind this or another part), so the leader never ends on thin air.
    """
    mesh = model.inst[part_id]
    centres = mesh.triangles_center
    order = np.argsort(np.linalg.norm(centres - mesh.bounds.mean(0), axis=1))
    if eye is None:
        return centres[order[0]]
    offsets = offsets or {}
    own = offsets.get(part_id)
    step = max(1, len(order) // 160)
    for k in order[::step][:160]:
        p = apply_pose(own, centres[k])
        if turn_dir(own, mesh.face_normals[k]) @ (eye - p) < 0.15 * np.linalg.norm(eye - p):      # faces away from the camera
            continue
        if not _hidden(model, p, eye, visible, offsets):
            return centres[k]
    return centres[order[0]]


# ---------------------------------------------------------------- camera
def code_seen(model, codes, ids, eye, visible, offsets):
    """The share of these parts whose engraved code the camera can read: facing it and not hidden. None if none has a code."""
    have = [i for i in ids if i in codes]
    if not have:
        return None
    seen = 0
    for i in have:
        normal, centre = codes[i]
        pose = offsets.get(i)
        p, n = apply_pose(pose, centre), turn_dir(pose, normal)
        sight = eye - p
        if n @ sight > 0.3 * np.linalg.norm(sight) and not _hidden(model, p + n * 0.4, eye, visible, offsets):
            seen += 1
    return seen / len(have)


def _fit(model, ids, offsets_list):
    lo, hi = np.full(3, np.inf), np.full(3, -np.inf)
    for offsets in offsets_list:
        a, b = model.bounds(ids, offsets)
        lo, hi = np.minimum(lo, a), np.maximum(hi, b)
    return (lo + hi) / 2, float(np.linalg.norm(hi - lo) / 2)


def _direction(azimuth_deg, elevation_deg):
    az, el = np.radians(azimuth_deg), np.radians(elevation_deg)
    return np.array([np.cos(el) * np.sin(az), np.sin(el), np.cos(el) * np.cos(az)])


def _unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def choose_view(model, visible, offsets_hover, offsets_done, travel, anchors, moving, previous, cfg, focus=None, focus_pad=1.0, frame=None, look_from=None,
                coded=(), codes=None, flip=False, view_dir=None):
    """Camera for a Step N / Step Nc pair: a unit direction (target -> camera), target and fit radius.

    A good view looks across the motion rather than along it, keeps the lead lines in sight, does not show a
    flat part edge-on and lets the student read the engraved code of the wood parts the step brings in
    (`coded`; `codes` gives each part's code face). Among good views it prefers the house three-quarter view,
    then the view already on screen, so the camera only swings when that genuinely helps.
    flip: a view of the underside: the four diagonals below the model; the player shows it with the model
    turned over, so it reads as an ordinary view of the kit built upside down. view_dir: exactly this direction.
    """
    target, radius = _fit(model, focus or visible, [offsets_hover, offsets_done])
    radius *= focus_pad if focus else 1.0             # a close-up of `focus` still shows a little of what is around it
    if frame is not None:                             # a close-up on a place rather than on parts: (centre, radius)
        target, radius, focus = np.asarray(frame[0], float), float(frame[1]), True
    travel = None if travel is None or np.linalg.norm(travel) < 1e-6 else np.asarray(travel, float) / np.linalg.norm(travel)
    lines = [(apply_pose(hover_pose, a), b) for (a, b), hover_pose in anchors] if anchors else []     # hover tip -> mouth
    thin_axis = None
    if moving:
        extents = model.union(moving).extents
        if extents.min() < 0.25 * np.sort(extents)[1]:
            thin_axis = np.eye(3)[int(np.argmin(extents))]

    def score(direction):
        s = 0.0
        if travel is not None:                         # how much of the motion the student sees: 1 square-on, 0 end-on
            s += 2.0 * np.sqrt(max(0.0, 1 - float(direction @ travel) ** 2))
        if thin_axis is not None:                      # a flat panel should show its face, not its edge
            s += 1.0 * min(1.0, abs(float(direction @ thin_axis)) / 0.35)
        if lines:
            eye = camera_eye(dict(dir=direction, target=target, radius=radius), cfg)
            seen = [not _hidden(model, a + (b - a) * f, eye, visible, offsets_hover) for a, b in lines for f in (0.15, 0.5, 0.85)]
            s += 2.0 * sum(seen) / len(seen)
        return s

    elevation = -cfg['view_elevation'] if flip else cfg['view_elevation']
    fresh = dict(target=target.round(1).tolist(), radius=round(radius, 1), **({'flip': True} if flip else {}))
    if view_dir is not None:                          # the author gives the exact direction
        return dict(dir=_unit(view_dir).round(4).tolist(), **fresh)
    if coded and codes:                               # the engraved codes of the parts coming in should be readable
        plain = score

        def score(direction):
            eye = camera_eye(dict(dir=direction, target=target, radius=radius), cfg)
            seen = code_seen(model, codes, coded, eye, visible, offsets_hover)
            return plain(direction) + (1.5 * seen if seen is not None else 0.0)
    if look_from is not None:                         # the author says which side to look from: the three-quarter view nearest to it
        want = np.asarray(look_from, float)
        views = [_direction(az, elevation) for az in (45, 135, 225, 315)]
        return dict(dir=max(views, key=lambda d: float(d @ want)).round(4).tolist(), **fresh)
    same_side = previous is not None and bool(previous.get('flip')) == flip
    if travel is None and not lines and same_side and not coded:    # nothing travels: no reason to swing the camera
        prev_target, prev_radius = np.array(previous['target']), previous['radius']
        inside = np.linalg.norm(target - prev_target) + radius <= prev_radius * 1.1
        return dict(previous) if inside and not focus else dict(dir=previous['dir'], **fresh)
    if not same_side:
        previous = None
    house = _direction(225, elevation)
    scored = [(score(d), d) for d in (_direction(az, elevation) for az in (45, 135, 225, 315))]   # the four three-quarter views
    best_score = max(t[0] for t in scored)
    good = [d for sc, d in scored if sc >= best_score - 0.34]          # all but about one line-sample in six as visible as the best
    prev_dir = np.array(previous['dir']) if previous is not None else None
    if prev_dir is not None and any(np.allclose(d, prev_dir, atol=1e-3) for d in good):
        chosen = prev_dir                                               # the view on screen is still good: do not swing
    elif any(np.allclose(d, house, atol=1e-3) for d in good):
        chosen = house
    else:                                                               # otherwise the good view that needs the smallest swing
        ref = prev_dir if prev_dir is not None else house
        chosen = max(good, key=lambda d: float(d @ ref))
    chosen = chosen.round(4).tolist()
    if previous is not None and chosen == previous['dir']:
        prev_target, prev_radius = np.array(previous['target']), previous['radius']
        if np.linalg.norm(target - prev_target) + radius <= prev_radius * 1.1 and radius >= prev_radius * 0.6:
            return dict(previous)                     # same angle and still well framed: the camera does not move at all
    return dict(dir=chosen, **fresh)


# ---------------------------------------------------------------- the guide script API
ZERO = [0.0, 0.0, 0.0]


class Guide:
    def __init__(self, kit_dir, title, part, names, source='mra.glb', copyright_line='', part_views=None, part_of=None, unlisted=(), mesh_names=None,
                 codes=None, hero_azimuth=225.0, start_view=None, end_view=None, parts_list=None, review_notes=True, hover_names=None,
                 steps_file='steps.json', **overrides):
        """codes: {id: (normal, centre)}, the engraved code on each wood part (the way its face looks, and the middle of the
        code, seated): the camera then prefers a side from which the codes of the parts coming in can be read.
        hero_azimuth: the side the title page and the finished model are seen from (degrees about the vertical; 0 = from +Z).
        start_view: the title page's camera, when it should differ from the finished model's view: dict(azimuth=,
        elevation=, zoom=) (zoom < 1 is closer), or exactly dict(dir=, target=, radius=, shift=) (shift: how far, in
        radii, the player moves the view sideways to leave room for the title; 0 for a camera taken from a screenshot).
        min_aspect: the narrowest frame (width / height) that camera suits; on narrower ones the player uses the finished
        model's camera instead, or otherwise=dict(dir=, target=, radius=, shift=) if given. otherwise=[camera, ...] (closest
        first) instead: the generator works out where the parts reach on screen with each of them and with the finished
        model's camera after them, and in each window the player takes the first that keeps the parts within the frame's
        left, right and top edges (the bottom may cut a cable off, as Lee's picture of the RCC's title page does; the
        website's card picture needs the bottom too); on the
        title page (its own camera then shift=0) moved aside just enough to clear the logo and title, which are a fixed size on
        the page (clear_title=True: a punched-in camera from a screenshot taken in a large window, seen in a small one such as
        the LMS's frame). The RCC's title page and Completed View.
        hide: parts left off the title page (a cable end that would show without its cable).
        end_view: the same for the Completed View (the finished model's own camera is then the fallback).
        Either may also give poses={id: pose}: parts that view shows turned or moved from where the build leaves them (the RCC's
        controller turned round, until it was turned in the build itself from Step 29 instead). Parts riding on them go with them,
        a camera the generator makes for that view (and a min_aspect fallback) frames them as posed (a camera given as dir= /
        target= / radius= is used as it is), and the Completed View then opens without gliding from the last step.
        parts_list: a function that takes the guide's parts list (one entry per kind of part: name, qty, ids, picture) and
        returns its pages, [dict(name='Parts List', groups=[dict(title, icon, colour, halo, items=[dict(name, tag, qty,
        picture)])])]: shown after the title page, as the published guides do. Only the parts this guide shows are listed,
        so a guide for one part of the build gets the parts of that part.
        review_notes: False once a guide is past review: the player then shows no Review notes and no switch for them
        (they stay in steps.json; ?review=1 shows them).
        hover_names: {id: name} where the pointer (hover or click) should name one part more exactly than the parts list does
        (the MRA's Left Joystick and Right Joystick, both "Joystick" in the parts list).
        The step text can be edited outside the guide: tools/step_text.py exports it to a CSV and brings an edited one back
        into the kit's step-text.json, which build() applies (matched by each step's text_key).
        steps_file: the file this guide is written to. 'steps.json' is the kit's Full Build (it also writes parts.json, from which
        the part pictures are made); a guide of its own in the same kit folder, not cut from the Full Build (a deconstruction
        guide), gets its own, e.g. 'steps-deconstruction.json', and its own step-text file ('step-text-deconstruction.json').
        A kit's guides share its one model.glb, which holds every part any of them shows (see _sync_model): no guide ever
        shrinks it. Part guides are cut from the Full Build itself (see chapter())."""
        self.kit_dir = Path(kit_dir)
        self.steps_file = steps_file
        if not re.fullmatch(r'steps(-[a-z0-9]+(-[a-z0-9]+)*)?\.json', steps_file):
            raise ValueError(f'steps_file: steps.json, or steps-<lower-case words joined by hyphens>.json, not {steps_file!r}')
        made = Path(kit_dir) / 'chapters.json'                     # (a Part's file is the Full Build's to write)
        if steps_file != 'steps.json' and made.exists() and steps_file in [c['file'] for c in json.load(open(made)).get('chapters', [])]:
            raise ValueError(f'steps_file={steps_file!r} is a Part of the Full Build (chapters.json): give this guide another name')
        self.chapters = []                      # Part guides cut from this one (see chapter())
        self.taken = None                       # a deconstruction guide: the Full Build it takes apart (see take_apart())
        self.wire_state = {}                    # (a deconstruction: each lead's route as the guide stands, for remove()'s checks)
        self.cfg = {**DEFAULTS, **overrides}
        self.hero_azimuth = float(hero_azimuth)
        self.start_view = dict(start_view or {})
        self.end_view = dict(end_view or {})
        self.parts_list = parts_list
        self.meta = dict(title=title, part=part, copyright=copyright_line, **({} if review_notes else {'review_notes': False}))
        self.names = dict(names)                # CAD instance id -> student-facing name
        self.part_of = part_of or {}            # id -> the id of the part it comes fitted to (a horn on its motor): same name on
        for child, parent in self.part_of.items():   # hover, one line in the parts list, pictured together
            if parent in self.names:
                self.names[child] = self.names[parent]
        self.mesh_names = mesh_names or {}      # start of a CAD mesh name -> hover name, for a part inside a part (the Nano on its module)
        self.hover_names = dict(hover_names or {})   # id -> the pointer's name for it, where it differs from the parts list's
        self.unlisted = set(unlisted)           # ids named on hover only: no label of their own, no line in the parts list
                                                # (a lead's plug, the caps of a jumper wire: the wire itself is not a CAD part)
        self.part_views = part_views or {}      # part name -> how its picture is framed, e.g. {'roll': 180} if it comes out upside down
        self.placed = []                        # ids already in the build, in order
        self.in_hand = []                       # ids of the sub-assembly currently being built on its own
        self.resting = {}                       # id -> pose a part lies at from when it appears until a step moves it into place
        self.parked = set()                     # ids on screen but not yet in place (so nothing is tested against them)
        self.riding = {}                        # id -> (carrier id, pose): a part that rides with another until a step moves it
        self.late = set()                       # riding parts that appear only when a step asks for them
        self.wire_defs = {}                     # wire id -> {colour, radius}
        self.steps = []
        self.log = []
        self.listed_extra = []                  # kit parts listed by hand (see list_part)
        self.pictured = {}                      # name -> how its picture is laid out (see part_picture)
        self.piece_pictures = {}                # name -> [pictures of one piece of it each, where its pieces look different] (part_picture)
        materials = self.kit_dir / 'materials.json'
        spec = json.load(open(materials)) if materials.exists() else {}
        self.palette = spec.get('palette', {})
        adjust = spec.get('adjust_mm') or {}
        extras = {i: (self.kit_dir / e['glb'], e['pose']) for i, e in spec.get('extra_parts', {}).items()}
        self.model = Model(self.kit_dir / source, adjust=adjust, own_parts=spec.get('own_parts', {}), extra_parts=extras)
        self.codes = {}
        moved = spec.get('move_engraving', {})
        for i, (normal, centre) in (codes or {}).items():   # (a part turned round by adjust_mm takes its code with it; move_engraving moves it on its face)
            by = moved.get(i, [0, 0, 0])
            self.codes[i] = (_unit(turn_dir(adjust.get(i), normal)), apply_pose(adjust.get(i), centre) + np.asarray(by['by'] if isinstance(by, dict) else by, float))

    # -- things declared once
    def rest_at(self, ids, pose):
        """Until a step moves them into place, these parts are shown at `pose` once they appear
        (for example a board lying beside the model, held only by its wires)."""
        for i in ids:
            self.resting[i] = pose

    def carry(self, ids, by, pose=None, appear=True):
        """These parts ride with the part `by`, from when it appears until a step moves them to their own seats
        (the plug on a servo's loose lead; the caps of the jumper wires on a joystick).
        pose: where they sit while riding, relative to their own seats, with `by` in place (default: at their seats).
        appear=False: they do not appear with `by` but when a later step lists them in its `appear=`."""
        for i in ids:
            self.riding[i] = (by, pose if pose is not None else [0.0, 0.0, 0.0])
            if not appear:
                self.late.add(i)

    def _pivot(self, part_id):
        return self.model.inst[part_id].bounds.mean(0)

    def list_part(self, name, ids, qty, wires=(), after=None):
        """A kit part for the parts list whose CAD pieces are named on hover only (unlisted): a breadboard wire, which is two
        caps in the CAD and a wire the player draws. ids: the pieces pictured; wires: [dict(colour, radius, pts)] drawn in
        its picture (pts in seated mm); after: the name of the part it is listed after."""
        wires = [dict(colour=self.palette.get(w['colour'], w['colour']), radius=float(w['radius']), pts=np.round(np.asarray(w['pts'], float), 2).tolist()) for w in wires]
        ids = list(ids)
        self.listed_extra.append(dict(name=name, ids=ids[:1], qty=int(qty), **({'with': ids[1:]} if ids[1:] else {}), **({'wires': wires} if wires else {}), _after=after))

    def part_picture(self, name, add=(), poses=None, wires=(), piece=None, file=None):
        """How the parts list pictures the part called `name`, when its first piece alone is not the whole part: `add` more
        pieces (the far plug of an extension wire), `poses` {id: pose} to lay the pieces out (as in a step), and `wires`
        [dict(colour, radius, pts)] drawn between them (pts in mm, as laid out).
        piece: a second picture, of that piece of the part, for a kind of part whose pieces look different (the RCC's car Nano
        Board, with a blue dot where the controller's has a white one); parts.html saves it as parts/<file>.png (file: a name
        for it, made into a file name as part names are) and the parts.json entry lists it under "also" ({ids, picture}), for
        the guide's parts_list function to show where that piece is listed. The parts list's own rows (and the LMS's) stay one
        per kind of part."""
        wires = [dict(colour=self.palette.get(w['colour'], w['colour']), radius=float(w['radius']), pts=np.round(np.asarray(w['pts'], float), 2).tolist()) for w in wires]
        how = dict(add=list(add), poses={i: pose_out(p) for i, p in (poses or {}).items()}, wires=wires)
        if piece is None:
            self.pictured[name] = how
        else:
            if not re.sub(r'[^A-Za-z0-9]+', '', file or ''):
                raise ValueError(f'part_picture({name!r}, piece={piece!r}) needs a file= name (with letters or digits) for its picture')
            self.piece_pictures.setdefault(name, []).append(dict(how, piece=piece, file=file))

    def wire(self, wire_id, colour, radius=0.6, name=None):
        """Declare a flexible wire. colour is a palette name from materials.json or #rrggbb; radius in mm; name is
        what the pointer reads on it. Steps then give it a route (see `wires=` and `wires_done=` on place(), and tools/wires.py)."""
        self.wire_defs[wire_id] = dict(colour=self.palette.get(colour, colour), radius=float(radius), **({'name': name} if name else {}))

    # -- step kinds
    def chapter(self, slug, part, start_view=None, end_view=None):
        """From here on, until the next chapter() (or the end), the steps are also a Part guide of their own, written by the same
        run to steps-<slug>.json (Lee, 16 Oct 2026: "Part guides"). Its core steps are this Full Build's own, with their wording
        and cameras, numbered from Step 1; it gets its own title page, a Parts List of only the parts new in it (the parts
        earlier Parts brought in are not listed again), and its own Completed View. Its title page and Completed View show the
        model as the Part leaves it. part: how its title page names it under the guide's title (e.g. "Part 1: The Controller").
        start_view / end_view: as Guide's, for this Part (default: the finished model's corner, framing what the Part shows).
        The run also writes chapters.json, the map from each Part's steps to the Full Build's (for "Part 2, Step 5" edits).
        Call it before the first step of the Part, in the Full Build's guide.py only (a guide with steps_file='steps.json')."""
        if self.steps_file != 'steps.json':
            raise ValueError('chapter(): Part guides are cut from the Full Build (steps.json), not from a guide of their own')
        if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', slug):
            raise ValueError(f'chapter({slug!r}): lower-case words joined by hyphens (it names steps-{slug}.json)')
        if any(c['slug'] == slug for c in self.chapters):
            raise ValueError(f'chapter({slug!r}) is there already')
        theirs = self.kit_dir / f'steps-{slug}.json'
        if theirs.exists() and 'chapter' not in json.load(open(theirs)).get('meta', {}):
            raise ValueError(f'chapter({slug!r}): {theirs.name} is a guide of its own (not a Part): give the chapter another name')
        if self.chapters and self.chapters[-1]['at'] == len(self.steps):
            raise ValueError(f'chapter({slug!r}): the chapter before it ({self.chapters[-1]["slug"]}) has no steps')
        self.chapters.append(dict(slug=slug, part=part, at=len(self.steps), start_view=dict(start_view or {}), end_view=dict(end_view or {})))

    def note(self, caption, review=None, caution=None, only_in=None):
        """A text-only card (no 3D), for things the model cannot show. caution: as in place().
        only_in: 'part' for a card only the Part guide this step is in shows (not the Full Build: "Part 1 must be finished
        before you start"), 'full' for one only the Full Build shows. The step numbers of each guide count only its own cards."""
        if only_in not in (None, 'part', 'full'):
            raise ValueError(f"note(only_in={only_in!r}): 'part' or 'full'")
        if only_in and not (self.chapters and self.chapters[-1]['at'] <= len(self.steps)):
            raise ValueError(f'note(only_in={only_in!r}): only inside a chapter() (a Part of the Full Build)')
        self.steps.append(dict(kind='card', caption=caption, review=review, caution=caution, **({'only_in': only_in} if only_in else {})))

    def in_part(self, caption=None, caution=None, view_dir=None, frame=None, look_from=None):
        """The step just added, as its Part guide shows it where that differs from the Full Build (a change "in that Part only",
        Lee 17 Oct 2026); the Full Build keeps the step as written. caption, caution ('' for none): its wording in the Part.
        view_dir= / frame= / look_from=: a camera of its own in the Part, as place()'s and in place of the step's own (both views
        of the step; the steps after it keep theirs). Edited wording in the Part's step-text-<slug>.json (tools/step_text.py)
        comes on top of this. For a note card that only one of the two guides has, see note(only_in=)."""
        if not self.steps or not self.chapters or len(self.steps) - 1 < self.chapters[-1]['at']:
            raise ValueError('in_part(): just after a step inside a chapter() (a Part of the Full Build)')
        s = self.steps[-1]
        if s['kind'] == 'put_away' or s.get('only_in'):
            raise ValueError('in_part(): just after a step both guides show')
        cam = {k: v for k, v in dict(view_dir=view_dir, frame=frame, look_from=look_from).items() if v is not None}
        if cam and s['kind'] != 'place':
            raise ValueError('in_part(): a camera of its own only for a 3D step made by place() or seat()')
        if cam and s.get('flip'):
            raise ValueError('in_part(): no camera of its own for a step shown turned over (not built yet)')
        own = s.setdefault('in_part', {})
        if caption is not None:
            own['caption'] = caption
        if caution is not None:
            own['caution'] = caution or None
        if cam:
            own['camera'] = cam

    # -- a deconstruction guide: the Full Build taken apart (rulebook section 11)
    def take_apart(self, full='steps.json'):
        """Begin a deconstruction guide (a guide of its own: Guide(steps_file='steps-deconstruction.json')) with the Full Build as it
        ends: every part where the Full Build leaves it, parts riding on others still riding, the leads as they are routed. Its
        title page is the Full Build's (the same camera; its subtitle is this guide's `part`). remove(), unplug() and lift() then
        take it apart, as a rule the build in reverse. The Full Build's steps file is read as its guide.py last wrote it: run that
        first, and this script again after any change to it (publish.py warns when the Full Build has changed since)."""
        from check_site import steps_stamp
        if self.steps_file == 'steps.json':
            raise ValueError('take_apart(): in a guide of its own (Guide(steps_file="steps-deconstruction.json")), not in the Full Build')
        if self.steps or self.taken:
            raise ValueError('take_apart(): first, before any step')
        data = json.loads((self.kit_dir / full).read_text(encoding='utf-8'))
        views, routes = data['views'], data['routes']
        states = [v for v in views if v['kind'] in ('hover', 'done')]
        if not states:
            raise SystemExit(f'take_apart(): {full} has no step that shows the model')
        came, before = {}, None                     # id -> [how the Full Build moved it in, each time it did], oldest first
        for k, v in enumerate(views):
            if v['kind'] == 'hover' and v.get('moving') and not v.get('wiggle'):
                for i in v['moving']:
                    own = (v.get('paths') or {}).get(i)
                    came.setdefault(i, []).append(dict(
                        index=k, name=v['name'], group=list(v['moving']), way=own or v['path'], isolated=bool(v.get('isolated')),
                        stops=((v.get('path_stops') or {}).get(i) if own else v.get('stops')), camera=v['camera'],
                        stationary=[j for j in v['visible'] if j not in v['moving'] and j not in (v.get('carry') or {}) and not _moved((v.get('offsets') or {}).get(j))],
                        offsets=dict(v.get('offsets') or {}),
                        wire_via={w: [routes[no] for no in nos] for w, nos in ((views[k + 1].get('wire_via') or {}) if k + 1 < len(views) and views[k + 1]['kind'] == 'done' else {}).items()},
                        wires={w: routes[no] for w, no in (v.get('wires') or {}).items()},
                        rode=((before or {}).get('carry') or {}).get(i)))
            if v['kind'] == 'hover' and not v.get('moving') and k + 1 < len(views) and views[k + 1]['kind'] == 'done':
                like = next((e.get('id') for e in v.get('eye') or [] if re.fullmatch(r'\d+x', next((l['text'] for l in v.get('labels') or []
                                                                                                   if l.get('id') == e.get('id')), ''))), None)
                for i in views[k + 1]['visible']:          # (the rest of a set, put in "like" the one shown in full: rest())
                    if like in came and i not in v['visible'] and i not in came and _rot(came[like][-1]['way'][0]) is None:
                        came[i] = [dict(came[like][-1], group=[i], like=like, index=k)]
            if v['kind'] in ('hover', 'done'):
                before = v
        # As the Full Build leaves the model: its Completed View (its last step may be a sub-assembly in the hand, shown on its own),
        # with any part that view hides, or poses for itself (end_view), as the last step that showed it had it.
        end = views[-1] if views[-1]['kind'] == 'end' else None
        base = end if end is not None and not end.get('cut') else None
        placed = list(base['visible']) if base else []
        offsets, carry = dict(base.get('offsets') or {}) if base else {}, dict(base.get('carry') or {}) if base else {}
        wires_now = {w: routes[no] for w, no in (base.get('wires') or {}).items()} if base else {}
        for v in reversed(states):
            for i in v['visible']:
                if i not in placed:
                    placed.append(i)
                    offsets[i] = (v.get('offsets') or {}).get(i)
                    if i in (v.get('carry') or {}):
                        carry[i] = v['carry'][i]
            for w, no in (v.get('wires') or {}).items():
                if w not in wires_now and all(e is None or e in placed for e in (routes[no].get('a'), routes[no].get('b'))):
                    wires_now[w] = routes[no]
        if end is None or end.get('cut'):
            self.log.append(f'  NOTE: take_apart(): {full} has no plain Completed View; each part is taken as the last step that showed it had it')
        self.taken = dict(file=full, stamp=steps_stamp(data), came=came, start=views[0], routes=routes)
        self.placed = placed
        self.riding = {i: (c['by'], c['pose']) for i, c in carry.items() if i in placed}
        self.resting = {i: p for i, p in offsets.items() if i not in carry and _moved(p)}
        self.parked = set(self.riding) | set(self.resting)
        self.wire_state = wires_now
        self.wire_defs = {**data.get('wires', {}), **self.wire_defs}
        for i, name in (data.get('names') or {}).items():
            self.names.setdefault(i, name)
        self.mesh_names = self.mesh_names or data.get('mesh_names') or {}
        self.meta.update(taken_from=self.taken['stamp'], full_build=full)
        self.steps.append(dict(kind='begin', visible=list(self.placed), rest=dict(self.resting), riding=dict(self.riding), wires=dict(self.wire_state)))
        self.log.append(f'take_apart(): from {full} as it ends ({len(self.placed)} parts, {len(self.wire_state)} leads)')

    def remove(self, caption, ids, **how):
        """Take parts off (after take_apart()): they leave and are gone, never to be put back (Lee, 17 Oct 2026). Step N shows them
        where they are, with a red arrow on each unit that leaves (rulebook section 11: never lead lines); Next plays them out and
        they disappear. Several parts may go at once ("in unison"), each its own way. By default a part leaves the way the Full Build
        brought it in, reversed (to where it hovered there, in its stages), seen by that step's camera; one that the Full Build did not
        move in, or that is not in its seat now, is pulled straight out the first free way (the collision test against what stays).
        Parts riding on them go with them, and so does a lead whose ends both go; a lead with only one end going is refused (unplug it
        first, take both ends off together, or say wires={id: None}). Options (as place()'s where named alike):
          path=[pose, ...], paths={id: [pose, ...]}: the way out by hand, the poses after where the part is now (via() for one it
              passes through); direction=[x, y, z] and hover=mm: a straight pull by hand.
          arrows: None (one per unit), [] (none: an eye instead, say), or [dict(tail, head, normal, part)] by hand (seated mm on `part`,
              drawn where it is now). eye=[ids or dict(anchor=...)], labels=[...] (none by default), caution=, review=, inset= (on Step N:
              the catch to release).
          view_dir= / frame= / look_from=, new_camera=True: a camera chosen for this step instead of the Full Build's; flip=True.
          wires={id: route or None}: leads that change route (or go) as the step completes. wires_here={id: route}: how leads are
              drawn on this step's two views only (a joystick's wires fading out while it is in the hand, the module not shown).
          units=[[ids], ...]: the arrows by hand, one on each group (eight breadboard wires pulled at once: one arrow at each end).
          alone=[ids]: the step shown with only these parts on screen (a sub-assembly taken apart on its own)."""
        return self._takeoff('remove', caption, ids, **how)

    def unplug(self, caption, ids, ride_on=None, **how):
        """Unplug plugs (after take_apart()): each comes out of its socket the way the Full Build plugged it in, reversed, to where it
        was before (its lead back on the route it had then), and stays there, riding on the part it rode on in the Full Build (or on
        `ride_on`: an id, or {plug: id}), until a later step takes it off with its lead and the part at the lead's other end. Step N
        has an eye on each plug (rulebook section 11), no arrow. Other options as remove()'s."""
        return self._takeoff('unplug', caption, ids, ride_on=ride_on, **how)

    def lift(self, caption, ids, to=None, ride_on=None, **how):
        """Move parts off and set them down beside the model, still wired (after take_apart(); a module lifted off the housing, to be
        unplugged later): to = the pose they end at, or {id: pose}; or path= / paths= for the way there; or neither: the way the Full
        Build brought them in, reversed, to where they hovered (a group the Full Build lowered into place, lifted off again to be
        taken apart on its own: alone=). They stay on screen, and go as one: the parts after the first ride on the first from then
        on; or, with ride_on=, each rides on that part again where it ends (plugs moved on their leads, back on their motor: a
        Full Build step that moved only a plug on its lead, walked back; a pose on the way given with via() is passed through at the
        pace the Full Build moved such a plug, stage by stage with its lead). List a plug that is in one of its sockets with them,
        so that it goes along, and a later unplug() takes it out from there; the log warns of a plug left behind. Other options as
        remove()'s, and wire_via={id: [route, ...]}: routes a lead passes through on the way, one per stage of the way (its last
        route is given in wires=)."""
        return self._takeoff('lift', caption, ids, to=to, ride_on=ride_on, **how)

    def _takeoff(self, how, caption, ids, path=None, paths=None, direction=None, hover=None, to=None, ride_on=None, wires=None, arrows=None,
                 eye=None, labels=(), caution=None, review=None, view_dir=None, frame=None, look_from=None, new_camera=False, inset=None,
                 alone=None, flip=False, wire_via=None, units=None, wires_here=None):
        if not self.taken:
            raise ValueError(f'{how}(): only in a deconstruction guide, after take_apart()')
        units_given = units
        ids = list(dict.fromkeys(ids))
        missing = [i for i in ids if i not in self.placed]
        if missing:
            raise ValueError(f'{how}({caption[:30]!r}): {missing} not on screen (taken off already, or never there)')

        def riders(group):                            # what rides on these (and on what rides on them)
            out, todo = [], list(group)
            while todo:
                c = todo.pop()
                for i, (by, _) in self.riding.items():
                    if by == c and i not in group and i not in out:
                        out.append(i)
                        todo.append(i)
            return out
        movers = [i for i in ids if not (i in self.riding and self.riding[i][0] in ids)]   # (one riding on another that moves goes with it)
        leave = ids + riders(ids) if how == 'remove' else []
        if alone is not None and any(i not in alone for i in ids):
            raise ValueError(f'{how}(): alone= must include the parts it moves')

        def now(i, seen=()):
            if i in self.riding and i not in seen:
                by, rel = self.riding[i]
                return compose(now(by, (*seen, i)), rel, self._pivot(i))
            return self.resting.get(i)
        staying = [i for i in self.placed if i not in leave and i not in ids]
        seated = [i for i in staying if not _moved(now(i)) and i not in self.riding]   # (what a straight pull is tested against)
        came = self.taken['came']
        ways, stops, moves, notes = {}, {}, {}, []
        computed = []
        for i in movers:
            hand = (paths or {}).get(i, path)
            start = now(i)
            if hand is not None:
                ways[i] = [start if start is not None else ZERO] + [p if isinstance(p, dict) else list(map(float, p)) for p in hand]
            elif how == 'lift' and to is not None:
                ways[i] = [start if start is not None else ZERO, to.get(i) if isinstance(to, dict) and not ('t' in to or 'r' in to) else to]
            elif direction is not None:
                d = _unit(direction)
                by_hand = [j for j in movers if (paths or {}).get(j, path) is None]
                ways[i] = [start if start is not None else ZERO, _shifted(start or ZERO, d * (float(hover) if hover else hover_distance(self.model, by_hand, d, self.cfg)))]
            else:
                on = set(self.placed)                     # (a part of the Full Build's group that is gone already does not count)
                fits = [m for m in came.get(i, []) if set(m['group']) & on <= set(ids) | set(leave)] or (came.get(i, [])[-1:] if how == 'unplug' else [])
                by, rel = self.riding.get(i, (None, None))
                in_seat_on = by if by is not None and by not in movers and not _moved(rel) else None   # (riding in its seat on a part that stays)
                if fits and ((not _moved(start) and i not in self.riding) or in_seat_on is not None):
                    m = fits[-1]
                    moves[i] = m
                    carrier = now(in_seat_on) if in_seat_on is not None else None
                    ways[i] = [compose(carrier, p, self._pivot(i)) if carrier is not None else p for p in reversed(m['way'])]
                    if in_seat_on is not None and _moved(carrier) and json.dumps(pose_out(carrier) if carrier is not None else None) != json.dumps(m['offsets'].get(in_seat_on)):
                        then = m['offsets'].get(in_seat_on)   # (its carrier has moved since: the Full Build's camera looks elsewhere,
                        level = lambda q: _rot(q) is None or np.allclose(_rot(q), np.eye(3), atol=1e-6)   # or, if it has only slid, there)
                        if m.get('camera') and level(carrier) and level(then):
                            cam = copy.deepcopy(m['camera'])
                            cam['target'] = (np.asarray(cam['target'], float) + _shift(carrier) - _shift(then)).round(1).tolist()
                            moves[i] = dict(m, camera=cam)
                        else:
                            moves[i] = dict(m, camera=None)
                    if m.get('stops'):
                        n = len(m['way']) - 1
                        stops[i] = sorted(n - k for k in m['stops'])
                elif how == 'unplug':
                    raise ValueError(f'unplug(): the Full Build never plugged {i} in (or it is not in its socket now): remove() or lift() it, or give path=')
                else:
                    computed.append(i)
        if computed:                                  # pulled straight out the first way that is free of what stays
            seated_now = [i for i in computed if not _moved(now(i)) and i not in self.riding]
            dirs = free_directions(self.model, seated_now, seated, self.cfg) if seated_now and seated else [AXES[0]]
            if len(seated_now) < len(computed):       # (not in its seat: the collision test, made with seated parts, cannot say)
                review = ((review + ' ') if review else '') + 'Not in its seat, it is lifted straight up: the way out needs a check.'
                self.log.append(f'  WARNING: {caption[:40]}: {", ".join(self.names.get(i, i) for i in computed if i not in seated_now)} not in '
                                f'its seat: lifted straight up, unchecked (give direction= or path=)')
            if not dirs:
                review = ((review + ' ') if review else '') + 'No straight way out was found in the CAD, so this motion needs a check.'
                self.log.append(f'  WARNING: no straight way out was found in the CAD; the motion needs a check ({caption[:40]})')
                dirs = [AXES[0]]
            d = np.asarray(dirs[0], float)
            reach = float(hover) if hover else hover_distance(self.model, computed, d, self.cfg)
            for i in computed:
                ways[i] = [now(i) if now(i) is not None else ZERO, _shifted(now(i) or ZERO, d * reach)]
            notes.append(f'pulled out along {d.astype(int).tolist()}')
        # a way the Full Build gave, now walked the other way: is it still clear of what stays? (the order may not be the exact reverse)
        for key in {m['index'] for m in moves.values()}:
            group = [i for i, m in moves.items() if m['index'] == key]
            way = ways[group[0]]
            if all(_rot(p) is None for p in way) and seated and not _moved(way[0]):   # (tested from the seat: not for a part lifted off with others)
                v = _shift(way[-1]) - _shift(way[0])
                reach = min(float(np.linalg.norm(v)), max(25.0, 0.8 * float(np.linalg.norm(self.model.union(group).extents))) + 5)   # (as free_directions tests)
                then = [j for j in moves[group[0]]['stationary'] if j in self.model.inst]   # (what the Full Build tested it against)
                if (np.linalg.norm(v) > 1e-6 and blocked(self.model.union(group), self.model.union(seated), _unit(v), reach, self.cfg)
                        and not (then and blocked(self.model.union(group), self.model.union(then), _unit(v), reach, self.cfg))):   # (blocked by the order, not by the way)
                    review = ((review + ' ') if review else '') + f'Taken off the way the Full Build put it on ({moves[group[0]]["name"]}), it passes through a part that is still there: check the order, or give a way by hand.'
                    self.log.append(f'  WARNING: {caption[:40]}: the way out of {moves[group[0]]["name"]} passes through a part still there')
        for i, way in ways.items():                   # (a way by hand may pass through poses without pausing: via())
            if i not in stops and any(isinstance(p, via) for p in way):
                stops[i] = sorted({0, len(way) - 1, *[k for k, p in enumerate(way) if not isinstance(p, via)]})
        final = {i: w[-1] for i, w in ways.items()}

        # where the unplugged plugs ride from now on, and what the leads do
        ride_after = {}
        if how == 'unplug':
            for i in movers:
                by = ride_on.get(i) if isinstance(ride_on, dict) else ride_on
                if by is None and moves.get(i, {}).get('rode'):
                    by = moves[i]['rode']['by']
                if by is not None and by in self.placed and by not in movers:
                    ride_after[i] = by
        after, wire_via = dict(wires or {}), {w: list(rs) for w, rs in (wire_via or {}).items()}   # (stages given by hand: a lead moved on its way)
        for w in wire_via:
            if w not in after:
                raise ValueError(f'{how}({caption[:30]!r}): wire_via for {w} needs its last route in wires=')
        if how == 'unplug':
            for i, m in moves.items():
                for w, r in m['wires'].items():
                    if i in (r.get('a'), r.get('b')) and w not in after and w in self.wire_state:
                        after[w] = r
                        if m['wire_via'].get(w):
                            wire_via[w] = list(reversed(m['wire_via'][w]))
        lead_off = []
        for w, r in self.wire_state.items():
            if r is None or w in after:
                continue
            ends = [r.get('a'), r.get('b')]
            if not any(e in leave for e in ends if e):
                continue
            if all(e is None or e in leave for e in ends):
                lead_off.append(w)
            else:
                other = next(e for e in ends if e and e not in leave)
                raise ValueError(f'{how}({caption[:30]!r}): the lead {w} would be left on {other} with nothing at its other end: unplug it '
                                 f'first, take both its ends off together, or say wires={{{w!r}: None}}')
        units = []                                    # one arrow per unit that leaves: parts that came in together the same way
        if units_by_hand := units_given:
            stray = [i for u in units_by_hand for i in u if i not in movers]
            if stray:
                raise ValueError(f'{how}({caption[:30]!r}): units= names parts that do not move: {stray}')
            units = [list(u) for u in units_by_hand]
        elif arrows is None and how != 'unplug':
            keyed = {}                                # (a unit: what the Full Build moved in together, what is pulled out together, one way by hand)
            for i in movers:
                key = ('build', moves[i]['index']) if i in moves else ('out',) if i in computed else ('own', i) if i in (paths or {}) else ('hand',)
                keyed.setdefault(key, []).append(i)
            joined = lambda a, b: any({a, b} <= {r.get('a'), r.get('b')} for r in self.wire_state.values() if r)   # (the two ends of one cable)
            def touching(a, b):                       # (a motor and its servo horn, named alike, are one unit; two screws are two)
                A, B = self.model.inst[a].bounds, self.model.inst[b].bounds
                return bool(np.all(A[0] <= B[1] + 0.5) and np.all(B[0] <= A[1] + 0.5))
            for group in keyed.values():
                if (len(group) == 2 and self.names.get(group[0]) and self.names.get(group[0]) == self.names.get(group[1]) and not joined(*group)
                        and not touching(*group)):
                    units += [[group[0]], [group[1]]]         # (two of a kind: an arrow on each, as the published guides do)
                else:
                    units.append(group)
            if len(units) > 2:
                self.log.append(f'  NOTE: {caption[:40]}: {len(units)} arrows (the published take-aparts show 2 at most: rulebook section 11)')
        if eye is None:
            eye = list(movers) if how == 'unplug' else []
        eye_list = [dict(e) if isinstance(e, dict) else dict(id=e) for e in eye]
        label_list = [dict(i) if isinstance(i, dict) else dict(id=i, text=self.names.get(i, i)) for i in labels]
        camera = None
        if not new_camera and view_dir is None and frame is None and look_from is None and moves and all(m.get('camera') for m in moves.values()):
            m = max(moves.values(), key=lambda m: m['index'])
            camera = copy.deepcopy(m['camera'])
            if m['isolated'] and alone is None:
                self.log.append(f'  NOTE: {caption[:40]}: the Full Build put this on in a sub-assembly view ({m["name"]}); its camera frames that')
            if flip and not camera.get('flip'):          # (turned over here, though not in the Full Build: a turned-over view from its side)
                look_from, camera = camera['dir'], None
        if how == 'lift':                             # (they go as one: the others ride on the first from now on, or all on ride_on)
            if ride_on is not None and ride_on in self.placed and ride_on not in movers:
                ride_after.update({i: ride_on for i in movers})
            else:
                ride_after.update({i: movers[0] for i in movers[1:]})
            plugs = [j for j in staying if j in seated and any(m.get('rode') for m in came.get(j, []))]   # (a plug the Full Build plugged in)
            for j in plugs:                           # (tested in the seat: a mover that is not in its seat now cannot hold a plug in it)
                b = self.model.inst[j].bounds
                if any(np.all(b[0] <= self.model.inst[i].bounds[1] + 1.0) and np.all(self.model.inst[i].bounds[0] <= b[1] + 1.0) for i in movers
                       if i in self.model.inst and not _moved(now(i)) and i not in self.riding):
                    self.log.append(f'  WARNING: {caption[:40]}: {self.names.get(j, j)} looks plugged into a part that is lifted, and stays behind: list it with them')
        self.steps.append(dict(kind='takeoff', how=how, caption=caption, caution=caution, review=review, ids=ids, movers=movers, leave=leave,
                               ways=ways, stops=stops, ride_after=ride_after, wires_after=after, wire_via=wire_via, lead_off=lead_off, units=units,
                               arrows=list(arrows) if arrows else [], eye=eye_list, labels=label_list, camera=camera, view_dir=view_dir,
                               frame=frame, look_from=look_from, flip=bool(flip), inset=dict(inset) if inset else None,
                               alone=list(alone) if alone is not None else None, wires_here=dict(wires_here or {})))
        # the guide's state from here on
        for i in leave:
            self.placed.remove(i)
            self.riding.pop(i, None)
            self.resting.pop(i, None)
            self.parked.discard(i)
        for w in lead_off:
            self.wire_state[w] = None
        self.wire_state.update(after)
        for i in movers:
            if i in leave:
                continue
            if i in ride_after:
                by = ride_after[i]
                self.riding[i] = (by, relative_pose(final.get(by, now(by)), final[i], self._pivot(i)))
                self.resting.pop(i, None)
            else:
                self.riding.pop(i, None)
                self.resting[i] = final[i]
            self.parked.add(i)
        way_note = 'the Full Build\'s way, reversed' if moves and not computed else ('by hand' if not moves and not computed else ', '.join(notes) or 'mixed')
        self.log.append(f"{caption[:58]:58s} {how:6s} {len(leave) if how == 'remove' else len(movers)} part(s), {way_note}"
                        f"{f', {len(units)} arrow(s)' if units else ''}{f', {len(lead_off)} lead(s) with them' if lead_off else ''}")

    def put_away(self, ids):
        """These parts leave the screen (no step of its own): a test set-up on the bench, taken apart before the build.
        Each comes back as a new part when a later step brings it in; give it a new carry() or rest_at() first if it
        should ride with another part or lie somewhere when it does. Parts riding on them go with them. The next view
        starts afresh ("cut"): the player glides nothing over from the view before it, and bends no wire across."""
        ids = list(ids)
        ids += [r for r, (by, _) in self.riding.items() if by in ids and r not in ids]   # (what rides on them goes with them)
        for w, r in self.wire_state.items():          # (a deconstruction: their leads go with them, as build() shows it)
            if r is not None and (r.get('a') in ids or r.get('b') in ids):
                self.wire_state[w] = None
        self.steps.append(dict(kind='put_away', ids=ids))
        self.placed = [i for i in self.placed if i not in ids]
        self.in_hand = [i for i in self.in_hand if i not in ids]
        self.parked -= set(ids)
        for i in ids + [r for r, (by, _) in self.riding.items() if by in ids]:   # (what rode on them goes with them, as build() shows it)
            self.riding.pop(i, None)
            self.resting.pop(i, None)
            self.late.discard(i)

    def place(self, caption, move=(), show=(), against=None, direction=None, hover=None, path=None, labels=None, review=None,
              appear_after=(), appear=(), staged=False, lines=True, lines_to=None, lines_at=None, axial=False, eye=(),
              focus=None, focus_pad=1.6, wires=None, wires_done=None, ride=None, frame=None, look_from=None, flip=False, view_dir=None, paths=None,
              caution=None, arrows=None, inset=None, wiggle=False, one_off_camera=False, single=False):
        """Add one part (or move one sub-assembly) into place. With no `move`, a step where only wires change.

        move:       ids that travel in this step (new parts appear hovering; parts already on screen move as a group).
        show:       new ids that appear already in position (the thing the moving part goes onto).
        appear:     new ids that appear where rest_at() put them: on screen, but neither moving nor yet in place.
                    A part in both `move` and `appear` is on screen where its path starts as the step opens, rather than
                    gliding in from further out as a new moving part does (a plug at the end of a lead laid out on the bench).
        against:    ids to test the motion against (default: everything in place so far that is not moving).
        direction:  hand-set approach axis, e.g. [0, 1, 0] = lowered from above. Default: computed from the CAD.
        hover:      hand-set hover distance in mm (default: see hover_distance).
        path:       hand-set way in: poses from the hover pose (first) to in place (last, [0, 0, 0]). A pose is
                    [x, y, z] in mm from seated, or turned(axis, degrees, at, t) for a part that is tilted on the way.
                    Wrap a pose in via() if the part should pass through it without pausing.
        axial:      True for a part that goes in along its own axis (a screw, a servo through its cut-out):
                    one lead line down the middle, as the published guides draw them. 'each' gives every moving
                    part its own such line (a set of screws going in together).
        labels:     ids to label (default: the new parts that have a name, one label per name). {id: 'text'} overrides;
                    a list may also hold dict(text=..., anchor=[x, y, z], id=part the spot is on) for a label on an exact
                    spot, such as a pin.
        lines_to:   ids the lead lines may attach to, when that differs from `against`
                    (e.g. a servo shaft pressing into its horn overlaps in CAD, so the horn is left out of the motion test).
        lines_at:   hand-set lead lines, for when the automatic ones are not where you want them: a list of points
                    [x, y, z] in mm (Option-click a tab or slot in the player to copy one). See hand_lines.
        staged:     True while a sub-assembly is being built in hand: the rest of the model is hidden until seat().
        appear_after: ids that simply appear once the part is seated.
        eye:        things to mark with the "look here" eye icon: part ids, or dict(anchor=[x, y, z]) for a spot.
        focus:      ids to frame instead of everything on screen: a close-up, for a part too small to see otherwise
                    (focus_pad widens it so some of the surroundings stay in view).
        wires:      {wire id: route, or None to remove it} taking effect as the step opens.
        frame:      ([x, y, z], radius in mm) to frame instead: a close-up on a place (a slot a wire goes into).
        look_from:  [x, y, z], the side to look from (a direction from the model towards the viewer), when the camera the
                    generator picks is on the wrong side: the three-quarter view nearest to it is used.
        view_dir:   [x, y, z], exactly the direction to look from (for a view the four three-quarter views cannot give).
        flip:       True for a view of the underside, shown with the model turned over (work done with the kit upside down).
        paths:      {id: path} for moving parts that each take their own way in (the two ends of a jumper wire: one
                    along a pin lying flat, the other down onto a pin standing up); the others take `path`. Each such
                    path is a list of stops, hover first. (Lead lines are worked out as if every part took
                    `path`: give such a step lines=False, as wire steps have, or set them with lines_at.)
        wires_done: the same, taking effect as the part seats; a wire that changes route is bent across by the player.
                    A list of routes [in-between, ..., final] makes the wire pass through the in-between ones on the way
                    (over the top edge of a wall, then down into its slot).
        ride:       {id: pose} a new riding pose (see carry()) for parts that are riding, taking effect as the step
                    completes: the plug on a loose lead when the lead is moved to a new route. A list of poses
                    [in-between, ..., final] to go with in-between routes.
        caution:    a sentence the student must not miss (brown to G; a horn that may need turning to fit): shown on
                    both views of the step, in a box of its own under the caption. Not a Review note (those are for TechBox).
        arrows:     [dict(tail=[x, y, z], head=[x, y, z], normal=[x, y, z], part=id)]: fat red arrows instead of lead
                    lines, for a move with no mating features (a plate slid along a slot). Points are seated mm on
                    `part` (default: the first moving part) and are drawn where that part hovers; normal is the way
                    the face of the arrow looks. Shown on Step N only, as lead lines are.
        inset:      dict(target=[x, y, z], dir=[x, y, z], radius=mm, hide=[ids], mark=mm, alt=..., caption=...): a framed
                    close-up on Step Nc with a lead line to `target`, seen from `dir` (assembly space) and framing
                    `radius` mm, with `hide` left out (to show what is under them) and a red box of half-width `mark`
                    round the detail. alt is what a screen reader says for it.
        wiggle:     True for a move on the spot that is played as the step opens as well as when it completes (a
                    check that parts move freely: their paths start and end where they are).
        single:     True for a step of one view (no Step Nc): a check where nothing goes on (the arm's jiggle, Lee 2026-10-14).
        one_off_camera: True when this step's camera (view_dir= / frame=) is a one-off: the steps after it choose theirs
                    as if it had the camera the generator would have given it (so pinning one step's camera, from a
                    screenshot, leaves the next steps' cameras as they were).
        """
        if self.taken:
            raise ValueError('place(): a deconstruction guide takes parts off (remove(), unplug(), lift()); it puts nothing on')
        move, show, appear = list(move), list(show), list(appear)
        paths = {i: [list(map(float, p)) if not isinstance(p, dict) else p for p in way] for i, way in (paths or {}).items()}
        if paths and path is None:
            path = next(iter(paths.values()))
        new = list(dict.fromkeys(i for i in show + move + appear if i not in self.placed))
        riders = self._riders(new)
        if staged:
            self.in_hand += [i for i in show + move + list(riders) if i not in self.in_hand]
        stationary = list(against) if against is not None else [p for p in self.placed + show if p not in move and p not in self.parked]
        auto, free = False, []
        if path is None:
            if not move:
                path = [ZERO, ZERO]
            elif all(i in self.parked and i in self.riding for i in move):     # plugging in something that was riding: from where it rides
                path = [self.riding[move[0]][1], ZERO]
            else:
                if stationary and direction is None:
                    dirs = free_directions(self.model, move, stationary, self.cfg)
                    free = [d.astype(int).tolist() for d in dirs]
                    if dirs:
                        direction, auto = dirs[0], True
                    else:
                        review = ((review + ' ') if review else '') + 'No straight-line path was found in the CAD, so this motion was set by hand and needs a check.'
                        self.log.append(f'  WARNING: no straight-line path was found in the CAD; the motion needs a check ({caption[:40]})')   # (in the log too: a guide may hide its Review notes)
                if direction is None:
                    direction = AXES[0]
                direction = np.asarray(direction, float) / np.linalg.norm(direction)
                reach = 0.0                               # the first part has nothing to attach to: it simply appears
                if stationary:
                    reach = float(hover) if hover else hover_distance(self.model, move, direction, self.cfg)
                path = [(direction * reach).round(1).tolist(), ZERO]
        stops = [k for k, p in enumerate(path) if not isinstance(p, via)]
        stops = sorted({0, len(path) - 1, *stops})
        path = [p if isinstance(p, dict) else list(map(float, p)) for p in path]
        straight_in = len(path) > 1 and _rot(path[-2]) is None and _rot(path[-1]) is None
        approach = _shift(path[-2]) - _shift(path[-1]) if straight_in else np.zeros(3)

        anchors = []
        if lines_at is not None:
            on_screen = list(dict.fromkeys(stationary + list(lines_to or ()) + (self.in_hand if staged else self.placed + show)))
            anchors = self._hand_lines(lines_at, move, [i for i in on_screen if i not in move], caption, waiting=set(appear) | set(riders))
        elif lines and move and stationary and np.linalg.norm(approach) > 1e-6:
            targets = list(lines_to) if lines_to is not None else stationary
            if axial == 'each':                       # one line per part, down the middle of where it grips
                for part in move:
                    own = lead_points(find_joints(self.model, [part], targets, approach), approach, self.cfg['max_lead_lines'])
                    if own:
                        anchors.append((np.mean([a for a, _ in own], axis=0), np.mean([b for _, b in own], axis=0)))
            else:
                anchors = lead_points(find_joints(self.model, move, targets, approach), approach, self.cfg['max_lead_lines'])
                if axial and anchors:                 # one line through the middle of the contact, tip to mouth
                    tips, mouths = np.array([a for a, _ in anchors]), np.array([b for _, b in anchors])
                    anchors = [(tips.mean(0), mouths.mean(0))]
        if arrows:                                    # (arrows and lead lines never share a step)
            anchors = []
        self._record(caption, move, show, appear, new, path, anchors, labels, eye, review, staged, appear_after, auto, free, focus, focus_pad,
                     wires, wires_done, lines_at is not None, riders=riders, ride=ride, stops=stops, frame=frame, look_from=look_from, flip=flip, view_dir=view_dir, paths=paths,
                     caution=caution, arrows=arrows, inset=inset, wiggle=wiggle, one_off_camera=one_off_camera, single=single)

    def _arrow_out(self, unit, here, there, camera):
        """A fat red arrow for parts leaving together (a deconstruction step): from just outside them, along the way they go, about as
        long as they travel (20 - 115 mm), its face towards the camera (rulebook section 11, the published take-aparts' sizes)."""
        a = np.mean([apply_pose(here.get(i), self._pivot(i)) for i in unit], axis=0)
        b = np.mean([apply_pose(there.get(i), self._pivot(i)) for i in unit], axis=0)
        reach = float(np.linalg.norm(b - a))
        if reach < 1.0:
            return None
        d = (b - a) / reach
        pts = np.vstack([apply_pose(here.get(i), _sample(np.asarray(self.model.inst[i].vertices), 3000)) for i in unit])
        tail = a + d * (float(((pts - a) @ d).max()) + 2.0)
        head = tail + d * float(np.clip(reach, 20.0, 115.0))
        view = np.asarray(camera['dir'], float)
        face = view - (view @ d) * d
        if np.linalg.norm(face) < 0.2:
            face = np.cross(d, [0.0, 1.0, 0.0]) if abs(d[1]) < 0.9 else np.cross(d, [1.0, 0.0, 0.0])
        return dict(tail=tail.round(2).tolist(), head=head.round(2).tolist(), normal=_unit(face).round(4).tolist())

    def _riders(self, appearing):
        """Parts that ride with one of the parts appearing now, and so appear with it: {id: (carrier, pose)}."""
        out = {i: (by, pose) for i, (by, pose) in self.riding.items() if by in appearing and i not in self.placed and i not in appearing and i not in self.late}
        out.update({i: self.riding[i] for i in appearing if i in self.riding and i not in self.placed})      # asked for by name in appear=
        return out

    def _shown_pose(self, i, waiting=(), seen=()):
        """Where a part waits as a step opens, if not at its seat: at its rest_at() pose, or carried by the part it rides with.
        (Only a part still waiting, or appearing in this step: one a step has seated is at its seat, whatever it rode with or
        rested at before.)"""
        if (i not in self.parked and i not in waiting) or i in seen:
            return None
        if i in self.riding:
            by, rel = self.riding[i]
            return compose(self._shown_pose(by, waiting, (*seen, i)), rel, self._pivot(i))
        return self.resting.get(i)

    def _hand_lines(self, points, move, stationary, caption, waiting=()):
        anchors = hand_lines(points)
        # A point that is on neither the moving part nor what it joins is almost always a typo or a point from another step. (The
        # parts that stay put are taken where the step shows them: a part resting or riding away from its seat, such as the RCC's
        # controller turned round for Step 29.)
        posed = {i: self._shown_pose(i, set(waiting)) for i in stationary}
        posed = {i: q for i, q in posed.items() if q is not None and (_rot(q) is not None or np.any(_shift(q)))}
        meshes = [m for m in (self.model.union(list(move)), self.model.union([i for i in stationary if i not in posed])) if m is not None]

        def gap(p):
            d = min((float(m.nearest.on_surface([p])[1][0]) for m in meshes), default=np.inf)
            for i, q in posed.items():
                d = min(d, float(self.model.inst[i].nearest.on_surface([unapply_pose(q, p)])[1][0]))
            return d
        for tip, mouth in anchors:
            for p in ((tip,) if np.array_equal(tip, mouth) else (tip, mouth)):
                if (meshes or posed) and gap(p) > 3.0:
                    self.log.append(f"  WARNING: lead-line point {p.round(1).tolist()} is not on any part in this step ({caption[:40]})")
        return anchors

    def _record(self, caption, move, show, appear, new, path, anchors, labels, eye, review, staged, appear_after, auto, free, focus, focus_pad,
                wires, wires_done, by_hand, from_hand=False, riders=None, ride=None, stops=None, frame=None, look_from=None, flip=False, view_dir=None, paths=None,
                caution=None, arrows=None, inset=None, wiggle=False, one_off_camera=False, single=False):
        riders = dict(riders or {})
        ride = {i: (list(p) if isinstance(p, list) and p and isinstance(p[0], (list, dict)) else [p]) for i, p in (ride or {}).items()}   # id -> [in-between poses..., final]
        wires_done = {i: (list(r) if isinstance(r, list) else [r]) for i, r in (wires_done or {}).items()}                              # id -> [in-between routes..., final]
        for i, poses in ride.items():                 # from here on it rides at the new pose
            self.riding[i] = (self.riding[i][0], poses[-1])
        guides = [dict(tip=np.round(tip, 1).tolist(), mouth=np.round(mouth, 1).tolist()) for tip, mouth in anchors]
        if labels is None:                            # one label per name: five screws get "5x 6mm Screw", not five labels
            label_list, seen = [], {}
            for i in new:
                name = None if i in self.part_of or i in self.unlisted else self.names.get(i)
                if name and name in seen:
                    seen[name]['count'] += 1
                elif name:
                    seen[name] = dict(id=i, text=name, count=1)
                    label_list.append(seen[name])
            label_list = [dict(id=l['id'], text=l['text'] if l['count'] == 1 else f"{l['count']}x {l['text']}") for l in label_list]
        else:
            label_list = [dict(i) if isinstance(i, dict) else dict(id=i, text=(labels[i] if isinstance(labels, dict) else self.names.get(i, i))) for i in labels]
        eye_list = [dict(e) if isinstance(e, dict) else dict(id=e) for e in eye]
        self.steps.append(dict(kind='place', caption=caption, show=show, move=move, appear=appear, new=new, path=path, staged=staged, riders=riders, ride=ride, stops=stops,
                               hand=list(self.in_hand) if staged else [], from_hand=from_hand, guides=guides, labels=label_list, eye=eye_list,
                               review=review, appear_after=list(appear_after), auto=auto, free=free, focus=list(focus) if focus else None,
                               focus_pad=focus_pad, frame=frame, look_from=look_from, wires=dict(wires or {}), wires_done=wires_done,
                               flip=flip, view_dir=view_dir, paths=dict(paths or {}), rest={i: self.resting[i] for i in appear if i in self.resting},
                               caution=caution, arrows=list(arrows or []), inset=dict(inset) if inset else None, wiggle=bool(wiggle),
                               one_off_camera=bool(one_off_camera), single=bool(single)))
        for i in new + list(riders) + list(appear_after):
            if i not in self.placed:
                self.placed.append(i)
        self.parked |= {i for i in appear if i in self.resting} | set(riders)
        self.parked -= set(move)
        first = pose_out(path[0])
        self.log.append(f"{caption[:58]:58s} {'auto' if auto else 'hand'} hover={first if isinstance(first, list) else 'turned'} lines={len(guides)}"
                        f"{' (set by hand)' if by_hand else ''}{' (sub-assembly)' if from_hand else ''}")

    def rest(self, caption, ids, like, review=None):
        """Add the rest of a set of identical parts once one has been shown in full (the "do the rest" step).

        The step opens with the eye icon and a quantity on the one already fitted (`like`); the others
        then appear in place. This is how the published guides handle three or more of the same part.
        """
        if self.taken:
            raise ValueError('rest(): a deconstruction guide takes parts off (remove(), unplug(), lift()); it puts nothing on')
        self.steps.append(dict(kind='rest', caption=caption, ids=list(ids), like=like, review=review))
        for i in ids:
            if i not in self.placed:
                self.placed.append(i)
        self.log.append(f"{caption[:58]:58s} rest  {len(ids)} more like {self.names.get(like, like)}")

    def seat(self, caption, ids, review=None, labels=(), lines_to=None, lines_at=None, appear=(), eye=(), focus=None, focus_pad=1.6,
             wires=None, wires_done=None, direction=None, hover=None, path=None, lines=True, ride=None, frame=None, look_from=None, flip=False, view_dir=None,
             caution=None, one_off_camera=False):
        """Bring a sub-assembly that was built in hand onto the model.

        The hover view shows it already above its seat (the player glides it across from where it was
        built), so the lead lines run straight from its joints into the model. The other options work as in place():
        `path=` for a sub-assembly that has to be tilted or swung on its way in, `lines=False` for no lead lines.
        """
        if self.taken:
            raise ValueError('seat(): a deconstruction guide takes parts off (remove(), unplug(), lift()); it puts nothing on')
        ids = list(ids)
        stationary = [p for p in self.placed if p not in ids and p not in self.parked]
        targets = list(lines_to) if lines_to is not None else stationary
        auto, free, stops = False, [], None
        if path is None:
            dirs = [np.asarray(direction, float)] if direction is not None else free_directions(self.model, ids, stationary, self.cfg)
            d = dirs[0] if dirs else AXES[0]
            d = d / np.linalg.norm(d)
            reach = float(hover) if hover else hover_distance(self.model, ids, d, self.cfg)
            if not dirs:
                review = ((review + ' ') if review else '') + 'No straight-line path was found in the CAD, so this motion was set by hand and needs a check.'
                self.log.append(f'  WARNING: no straight-line path was found in the CAD; the motion needs a check ({caption[:40]})')   # (in the log too: a guide may hide its Review notes)
            path = [(d * reach).round(1).tolist(), ZERO]
            auto, free = bool(dirs) and direction is None, [x.astype(int).tolist() for x in dirs]
        else:
            stops = sorted({0, len(path) - 1, *[k for k, p in enumerate(path) if not isinstance(p, via)]})
            path = [p if isinstance(p, dict) else list(map(float, p)) for p in path]
        straight_in = _rot(path[-2]) is None and _rot(path[-1]) is None
        approach = _shift(path[-2]) - _shift(path[-1]) if straight_in else np.zeros(3)
        if lines_at is not None:
            anchors = self._hand_lines(lines_at, ids, stationary, caption)
        elif lines and np.linalg.norm(approach) > 1e-6:
            anchors = lead_points(find_joints(self.model, ids, targets, approach), approach, self.cfg['max_lead_lines'])
        else:
            anchors = []
        appear = list(appear)
        new = [i for i in appear if i not in self.placed]
        self._record(caption, ids, [], appear, new, path, anchors, list(labels), eye, review, False, (), auto, free, focus, focus_pad,
                     wires, wires_done, lines_at is not None, from_hand=True, riders=self._riders(new), ride=ride, stops=stops, frame=frame, look_from=look_from,
                     flip=flip, view_dir=view_dir, caution=caution, one_off_camera=one_off_camera)
        self.in_hand = [i for i in self.in_hand if i not in ids and not (i in self.riding and self.riding[i][0] in ids)]   # (its riders leave the hand with it)

    def _apply_step_text(self):
        """Give each step its text key (text_key below), and apply edited wording from the kit's step-text.json (written by
        tools/step_text.py from a CSV): {"steps": [{"key", "step", "caption"?, "caution"?, "was_caution"?}]}, only the fields
        that were edited. A caution edited outside is not used if guide.py's own caution has changed since (was_caution)."""
        seen = {}
        for s in self.steps:
            if s.get('caption'):
                k = seen.get(s['caption'], 0)
                seen[s['caption']] = k + 1
                s['text_key'] = text_key(s['caption'], k)
        path = self.kit_dir / step_text_file(self.steps_file)
        if not path.exists():
            return
        edits = {e['key']: e for e in json.loads(path.read_text(encoding='utf-8')).get('steps', [])}
        done = set()
        for s in self.steps:
            e = edits.get(s.get('text_key'))
            if not e:
                continue
            done.add(e['key'])
            if e.get('caption', '').strip():
                s['caption'] = e['caption']
            if 'caution' in e:
                if (s.get('caution') or '') != e.get('was_caution', s.get('caution') or ''):
                    self.log.append(f'  WARNING: the caution of {e.get("step", e["key"])} has changed in guide.py since it was edited '
                                    f'outside; the edited caution is not used (step-text.json)')
                else:
                    s['caution'] = e['caution'].strip() or None
        for key, e in edits.items():
            if key not in done:
                self.log.append(f'  WARNING: step-text.json has wording for a step the guide no longer has ({e.get("step", "")} {key}: '
                                f'"{e.get("caption", "")[:50]}"); its wording in guide.py has changed or the step is gone')
        self.log.append(f'step-text.json: wording of {len(done)} step(s) applied')

    # -- expansion into the views the player steps through
    def build(self):
        self._apply_step_text()
        used = []
        for s in self.steps:
            for i in s.get('show', []) + s.get('move', []) + s.get('appear', []) + list(s.get('riders', {})) + s.get('appear_after', []) + (s.get('ids', []) if s['kind'] == 'rest' else []) + (s['visible'] if s['kind'] == 'begin' else []):
                if i not in used:
                    used.append(i)
        routes, route_index = [], {}

        def route_no(route):
            key = json.dumps(route, sort_keys=True)
            if key not in route_index:
                route_index[key] = len(routes)
                routes.append(route)
            return route_index[key]

        def wires_in(current, shown):
            """Route numbers of the wires to draw: those whose end parts are both on screen."""
            out = {}
            for wire_id, route in current.items():
                if route is None or any(route.get(end) is not None and route[end] not in shown for end in ('a', 'b')):
                    continue
                out[wire_id] = route_no(route)
            return out

        poses_out = lambda poses: {i: pose_out(p) for i, p in poses.items()}
        views = [dict(name='Start', kind='start', visible=used, offsets={})]
        visible, camera, n, cut = [], None, 0, False
        carry_on = None                                  # the camera the next step's choice carries on from (see one_off_camera)
        parked, wires, riding = {}, {}, {}               # poses of parts lying aside; current route of each wire; parts riding with another

        def with_riders(poses, shown):
            """Add where each riding part is, given where its carrier is; returns (poses, the `carry` entry for the view). A carrier
            that rides on another is placed first (a plug on the claw motor, riding on C3 once the claw is lifted off)."""
            carry = {}

            def place(i, seen=()):
                by, rel = riding[i]
                if by in riding and by in shown and by not in carry and by not in seen:
                    place(by, (*seen, i))
                poses[i] = compose(poses.get(by), rel, self._pivot(i))
                carry[i] = dict(by=by, pose=pose_out(rel))
            for i, (by, rel) in riding.items():
                if i in shown and by in shown and i not in carry:
                    place(i)
            return poses, carry
        first_view = []                                  # the index of each step's first view (for the Part guides, chapter())
        for si, s in enumerate(self.steps):
            first_view.append(len(views))
            if s['kind'] == 'put_away':                                    # off the screen, until a step brings them in again
                gone = set(s['ids'])
                visible[:] = [i for i in visible if i not in gone]
                for i in gone:
                    parked.pop(i, None)
                for i in [i for i, (by, _) in riding.items() if i in gone or by in gone]:
                    riding.pop(i)
                for wire_id in [w for w, r in wires.items() if r is not None and (r.get('a') in gone or r.get('b') in gone)]:
                    wires.pop(wire_id)
                cut = True                                                 # the next view starts afresh (the player glides nothing over)
                continue
            if s['kind'] == 'begin':                                       # a deconstruction: the Full Build as it ends (take_apart())
                visible[:] = list(s['visible'])
                parked.clear()
                parked.update(s['rest'])
                riding.clear()
                riding.update(s['riding'])
                wires.clear()
                wires.update({w: r for w, r in s['wires'].items() if r is not None})
                continue
            only = s.get('only_in')                                        # (a card only the Part shows: not counted in the Full Build)
            if only != 'part':
                n += 1
            if s['kind'] == 'card':
                views.append(dict(name=f'Step {n}' if only != 'part' else f'Step {n}+', kind='card', caption=s['caption'], text_key=s['text_key'], review=s['review'],
                                  visible=list(visible), offsets={}, _step=si, **({'_only': only} if only else {}), **({'_part': dict(s['in_part'])} if s.get('in_part') else {}),
                                  **({'caution': s['caution']} if s.get('caution') else {})))
                if not only:                                               # (a card is a clean break already; but one guide alone has this one)
                    cut = False
                continue
            if s['kind'] == 'takeoff':                                     # a deconstruction step: parts taken off, unplugged or set aside
                shown = [i for i in visible if i in s['alone']] if s['alone'] is not None else list(visible)
                here, carry_here = with_riders({i: p for i, p in parked.items() if i in shown}, shown)
                for i in s['movers']:                                      # (a part that moves on its own is no longer riding)
                    riding.pop(i, None)
                there = {i: p for i, p in here.items() if i not in riding}
                there.update({i: way[-1] for i, way in s['ways'].items()})
                there, carry_there = with_riders(there, shown)
                centre = lambda i: self.model.inst[i].bounds.mean(0)
                travel = np.mean([apply_pose(there.get(i), centre(i)) - apply_pose(here.get(i), centre(i)) for i in s['movers']], axis=0) if s['movers'] else None
                camera = s['camera'] or choose_view(self.model, shown, there, here, travel, [], s['movers'], carry_on, self.cfg, frame=s.get('frame'),
                                                    look_from=s.get('look_from'), flip=s.get('flip', False), view_dir=s.get('view_dir'))
                carry_on = camera
                if s['camera']:                                            # (the Full Build's camera: does it leave out a part lying aside?)
                    aside = [i for i in shown if _moved(here.get(i)) and i not in s['movers']]
                    out_of = [i for i in aside if float(np.linalg.norm(apply_pose(here.get(i), self._pivot(i)) - np.asarray(camera['target'], float)))
                              > 1.1 * float(camera['radius'])]
                    out_of = [i for i in out_of if not (i in riding and riding[i][0] in out_of)]   # (named by what they ride on)
                    if out_of:
                        self.log.append(f"  NOTE: {s['caption'][:40]}: the Full Build's camera leaves out {', '.join(list(dict.fromkeys(self.names.get(i, i) for i in out_of))[:3])}, "
                                        f"lying aside (new_camera=True, or alone=)")
                eye = camera_eye(camera, self.cfg)
                for item in s['labels'] + s['eye']:                        # leaders end on a spot this camera can see
                    if 'id' in item and 'anchor' not in item:
                        item['anchor'] = label_anchor(self.model, item['id'], eye, shown, here).round(1).tolist()
                arrows = [a for a in (self._arrow_out(unit, here, there, camera) for unit in s['units']) if a]
                for a in s['arrows']:                                      # by hand: seated mm on `part`, drawn where it is now
                    pose = here.get(a.get('part', s['movers'][0] if s['movers'] else None))
                    arrows.append(dict(tail=np.round(apply_pose(pose, a['tail']), 2).tolist(), head=np.round(apply_pose(pose, a['head']), 2).tolist(),
                                       normal=_unit(turn_dir(pose, a.get('normal', [0, 1, 0]))).round(4).tolist(), **({'width': a['width']} if 'width' in a else {})))
                inset = None
                if s.get('inset'):                                         # (on Step N here: the catch to release before the part comes off)
                    I = s['inset']
                    inset = dict(target=[round(float(x), 2) for x in I['target']], dir=_unit(I.get('dir', camera['dir'])).round(4).tolist(), radius=float(I.get('radius', 20.0)),
                                 hide=list(I.get('hide', [])), **{k: I[k] for k in ('mark', 'alt', 'caption') if k in I})
                common = dict(caption=s['caption'], text_key=s['text_key'], review=s['review'], camera=camera, _step=si,
                              **({'caution': s['caution']} if s.get('caution') else {}), **({'isolated': True} if s['alone'] is not None else {}))
                views.append(dict(name=f'Step {n}', kind='hover', visible=shown, offsets=poses_out(here), guides=[], labels=s['labels'], eye=s['eye'],
                                  wires=wires_in({**wires, **s['wires_here']}, shown), carry=carry_here, moving=[], path=[ZERO, ZERO], **({'arrows': arrows} if arrows else {}),
                                  **({'inset': inset} if inset else {}), **({'cut': True} if cut else {}), **common))
                cut = False
                going = [i for i in s['leave'] if i in shown]
                with_them = {w: wires[w] for w in s['lead_off'] if wires.get(w) is not None}
                lead_routes = {w: route_no(r) for w, r in with_them.items() if wires_in({w: r}, shown)}
                for w in s['lead_off']:
                    wires.pop(w, None)
                for w, r in s['wires_after'].items():
                    if r is None:
                        wires.pop(w, None)
                    else:
                        wires[w] = r
                visible[:] = [i for i in visible if i not in s['leave']]
                left = [i for i in shown if i not in s['leave']]
                held = {i: k for i, k in s['stops'].items() if len(k) < len(s['ways'][i])}
                for i, by in s['ride_after'].items():             # (a plug moved on its lead, riding on its motor before and after: it rides
                    way = s['ways'][i]                            # through the move, as the Full Build moved it, its stages at an even pace)
                    if by in s['movers'] or by not in shown or (carry_here.get(i) or {}).get('by') != by or len(s['stops'].get(i, range(len(way)))) > 2:
                        continue
                    rel = lambda p: pose_out(relative_pose(there.get(by), p, self._pivot(i)))
                    carry_there[i] = dict(by=by, pose=rel(there[i]), **({'via': [rel(p) for p in way[1:-1]]} if len(way) > 2 else {}))
                views.append(dict(name=f'Step {n}c', kind='done', visible=left, offsets=poses_out(there), wires=wires_in({**wires, **s['wires_here']}, left),
                                  carry={i: c for i, c in carry_there.items() if i in shown}, moving=list(s['movers']), path=[ZERO, ZERO],
                                  paths={i: [pose_out(p) for p in way] for i, way in s['ways'].items()}, **({'path_stops': held} if held else {}),
                                  **({'leaving': going} if going else {}), **({'leaving_wires': lead_routes} if lead_routes else {}),
                                  **({'wire_via': {w: [route_no(r) for r in rs] for w, rs in s['wire_via'].items() if w in wires}} if s.get('wire_via') else {}),
                                  away=True, **common))
                for i in s['leave']:                                       # the state from here on
                    parked.pop(i, None)
                    riding.pop(i, None)
                for i in s['movers']:
                    if i in s['leave']:
                        continue
                    if i in s['ride_after']:
                        by = s['ride_after'][i]
                        riding[i] = (by, relative_pose(there.get(by), there[i], self._pivot(i)))
                        parked.pop(i, None)
                    else:
                        parked[i] = there[i]
                continue
            if s['kind'] == 'rest':
                still, carry = with_riders(dict(parked), visible)
                camera = carry_on = choose_view(self.model, visible + s['ids'], still, still, None, [], [], carry_on, self.cfg)
                anchor = label_anchor(self.model, s['like'], camera_eye(camera, self.cfg), visible, still).round(1).tolist()
                common = dict(caption=s['caption'], text_key=s['text_key'], review=s['review'], moving=[], path=[ZERO, ZERO], camera=camera, carry=carry, _step=si,
                              **({'caution': s['caution']} if s.get('caution') else {}), **({'_part': dict(s['in_part'])} if s.get('in_part') else {}))
                views.append(dict(name=f'Step {n}', kind='hover', visible=list(visible), offsets=poses_out(still), guides=[], wires=wires_in(wires, visible),
                                  labels=[dict(id=s['like'], text=f"{len(s['ids'])}x", anchor=anchor)], eye=[dict(id=s['like'], anchor=anchor)],
                                  **({'cut': True} if cut else {}), **common))
                cut = False
                visible.extend(i for i in s['ids'] if i not in visible)
                views.append(dict(name=f'Step {n}c', kind='done', visible=list(visible), offsets=poses_out(still), wires=wires_in(wires, visible), **common))
                continue
            for i in s['show'] + s['move'] + s['appear'] + list(s['riders']):
                if i not in visible:
                    visible.append(i)
            parked.update(s['rest'])                                       # (where rest_at() had them lie when the step was written)
            riding.update(s['riders'])
            for i in s['move']:                                            # a part that moves on its own is no longer riding
                riding.pop(i, None)
            shown = list(s['hand']) if s['staged'] else list(visible)      # a sub-assembly in hand is shown on its own
            hover = {i: p for i, p in parked.items() if i in shown}
            way = lambda i: s['paths'].get(i, s['path'])
            hover.update({i: way(i)[0] for i in s['move']})
            hover, carry_hover = with_riders(hover, shown)
            for i in s['move']:
                parked.pop(i, None)
            for i, poses in s['ride'].items():
                if i in riding:
                    riding[i] = (riding[i][0], poses[-1])
            done, carry_done = with_riders({i: p for i, p in parked.items() if i in shown}, shown)
            for i, poses in s['ride'].items():             # in-between places on the way to the new riding pose
                if i in carry_done and len(poses) > 1:
                    carry_done[i]['via'] = [pose_out(p) for p in poses[:-1]]
            travel = None
            if s['move']:
                travel = np.mean([apply_pose(way(i)[0], c) - apply_pose(way(i)[-1], c) for i in s['move'] for c in [self.model.inst[i].bounds.mean(0)]], axis=0)
            anchors = [((np.asarray(g['tip']), np.asarray(g['mouth'])), s['path'][0]) for g in s['guides']]
            coded = [i for i in s['move'] + s['show'] + s['new'] if i in self.codes and i in shown]
            choose = lambda look_from=s.get('look_from'), **pinned: choose_view(self.model, shown, hover, done, travel, anchors, s['move'], carry_on, self.cfg, focus=s['focus'],
                                                  focus_pad=s['focus_pad'], look_from=look_from, coded=list(dict.fromkeys(coded)), codes=self.codes, flip=s.get('flip', False), **pinned)
            camera = choose(frame=s.get('frame'), view_dir=s.get('view_dir'))
            part_cam = (s.get('in_part') or {}).get('camera')               # (a camera of its own in its Part guide: in_part())
            part_cam = part_cam and choose(look_from=part_cam.get('look_from'), frame=part_cam.get('frame'), view_dir=part_cam.get('view_dir'))
            carry_on = choose(frame=None, view_dir=None) if s.get('one_off_camera') else camera
            eye = camera_eye(camera, self.cfg)
            placed_here = [item for item in s['labels'] + s['eye'] if 'id' in item and 'anchor' not in item]
            for item in placed_here:                                       # leaders end on a spot this camera can see
                item['anchor'] = label_anchor(self.model, item['id'], eye, shown, hover).round(1).tolist()
            own = None
            if s.get('in_part'):                                           # the step as its Part guide shows it (in_part())
                own = {k: v for k, v in s['in_part'].items() if k != 'camera'}
                if part_cam:
                    part_eye = camera_eye(part_cam, self.cfg)
                    again = lambda items: [dict(item, anchor=label_anchor(self.model, item['id'], part_eye, shown, hover).round(1).tolist())
                                           if any(item is a for a in placed_here) else item for item in items]
                    own.update(camera=part_cam, labels=again(s['labels']), eye=again(s['eye']))
            common = dict(caption=s['caption'], text_key=s['text_key'], review=s['review'], moving=s['move'], path=[pose_out(p) for p in s['path']], camera=camera,
                          _step=si, **({'_part': own} if own else {}))
            if s.get('caution'):
                common['caution'] = s['caution']
            if s['paths']:
                common['paths'] = {i: [pose_out(p) for p in way] for i, way in s['paths'].items()}
                held = {i: sorted({0, len(way) - 1, *[k for k, p in enumerate(way) if not isinstance(p, via)]}) for i, way in s['paths'].items()}
                held = {i: k for i, k in held.items() if len(k) < len(s['paths'][i])}
                if held:                                                   # (a way of its own with poses it passes through without pausing)
                    common['path_stops'] = held
            if s.get('wiggle'):
                common['wiggle'] = True
            if s['stops'] and len(s['stops']) < len(s['path']):
                common['stops'] = s['stops']
            if s['staged']:
                common['isolated'] = True
            wires.update(s['wires'])
            arrows = []
            for a in s.get('arrows') or []:                                # drawn where the part they belong to hovers
                pose = hover.get(a.get('part', s['move'][0] if s['move'] else None))
                arrows.append(dict(tail=np.round(apply_pose(pose, a['tail']), 2).tolist(), head=np.round(apply_pose(pose, a['head']), 2).tolist(),
                                   normal=_unit(turn_dir(pose, a.get('normal', [0, 1, 0]))).round(4).tolist(), **({'width': a['width']} if 'width' in a else {})))
            stay = [i for i in s['move'] if i in s['appear']]               # (on screen where its path starts: see place())
            views.append(dict(name=f'Step {n}', kind='hover', visible=shown, offsets=poses_out(hover), guides=s['guides'], labels=s['labels'], eye=s['eye'],
                              wires=wires_in(wires, shown), carry=carry_hover, **({'arrows': arrows} if arrows else {}), **({'cut': True} if cut else {}),
                              **({'still': stay} if stay else {}), **common))
            cut = False
            after = [i for i in s['appear_after'] if i not in visible]
            visible.extend(after)
            shown_done = shown + [i for i in after if i not in shown]
            wires.update({i: r[-1] for i, r in s['wires_done'].items()})
            wire_via = {i: [route_no(x) for x in r[:-1]] for i, r in s['wires_done'].items() if len(r) > 1}
            inset = None
            if s.get('inset'):
                I = s['inset']
                inset = dict(target=[round(float(x), 2) for x in I['target']], dir=_unit(I.get('dir', camera['dir'])).round(4).tolist(), radius=float(I.get('radius', 20.0)),
                             hide=list(I.get('hide', [])), **{k: I[k] for k in ('mark', 'alt', 'caption') if k in I})
            if own is not None and part_cam and inset and 'dir' not in s['inset']:   # (the close-up from the Part's own side too)
                own['inset'] = dict(inset, dir=_unit(part_cam['dir']).round(4).tolist())
            if s.get('single'):                                            # one view only: the step is its opening view
                continue
            views.append(dict(name=f'Step {n}c', kind='done', visible=shown_done, offsets=poses_out(done), wires=wires_in(wires, shown_done), carry=carry_done,
                              **({'wire_via': wire_via} if wire_via else {}), **({'inset': inset} if inset else {}), **common))
        last, carry_last = with_riders(dict(parked), visible)

        def posed(sv):
            """Where the title page / the Completed View shows each part: as the build leaves it, but for its own poses (and
            the parts riding on those, which go with them)."""
            turns = dict(sv.get('poses') or {})
            for i, c in carry_last.items():
                if c['by'] in turns and i not in turns:
                    turns[i] = turns[c['by']]
            return {**last, **{i: compose(pose, last.get(i), self._pivot(i)) for i, pose in turns.items() if i in used}}
        steps_end = len(views)                           # (where the Completed View goes: the end of the last Part)
        start_last, end_last = posed(self.start_view), posed(self.end_view)
        views.append(dict(name='Completed View', kind='end', visible=list(visible), offsets=poses_out(end_last), wires=wires_in(wires, visible), carry=carry_last,
                          **({'cut': True} if self.end_view.get('poses') else {})))     # (a part turned for the view: no glide from the last step)
        start_shown = [i for i in used if i not in self.start_view.get('hide', ())]
        views[0].update(visible=start_shown, wires=wires_in(wires, start_shown), offsets=poses_out(start_last), carry=carry_last)
        if self.taken and not self.start_view:            # a deconstruction opens on the Full Build's title page (rulebook section 11)
            st = self.taken['start']
            views[0].update(visible=list(st['visible']), offsets=dict(st.get('offsets') or {}), carry=dict(st.get('carry') or {}),
                            wires={w: route_no(self.taken['routes'][no]) for w, no in (st.get('wires') or {}).items()})
        end_shown = [i for i in visible if i not in self.end_view.get('hide', ())]
        views[-1].update(visible=end_shown, wires=wires_in(wires, end_shown))
        hero_target, hero_radius = _fit(self.model, used, [{}])
        hero = dict(dir=_direction(self.hero_azimuth, 32).round(4).tolist(), target=hero_target.round(1).tolist(), radius=round(hero_radius, 1))
        def given(c):
            return dict(dir=_unit(c['dir']).round(4).tolist(), target=[round(float(x), 1) for x in c['target']], radius=round(float(c['radius']), 1),
                        **({'shift': float(c['shift'])} if 'shift' in c else {}))

        def reach(cam, shown, offsets, shifts):
            """Where the parts reach on screen with this camera (landscape frame), moved aside by each of `shifts` radii as the
            player moves a title page's camera for its title: the left and right edges, the top and the bottom, in half frame
            heights from the middle (left and bottom negative). For the player to choose, in each window, the closest of a view's cameras that keeps the
            parts in the frame (and clear of the title)."""
            f, side = -_unit(cam['dir']), _unit(np.cross(cam['dir'], [0.0, 1.0, 0.0]))
            right, up = -side, np.cross(-side, f)
            p = np.vstack([apply_pose(offsets.get(i), self.model.inst[i].vertices) for i in shown])
            p = p[::max(1, len(p) // 150000)]
            t, eye = np.tan(np.radians(self.cfg['fov'] / 2)), camera_eye(cam, self.cfg)
            out = dict(s=[], l=[], r=[], t=[], b=[])
            for k in shifts:
                q = p - (eye + side * k * cam['radius'])
                z = q @ f
                u, v = (q @ right) / (z * t), (q @ up) / (z * t)
                for key, val in (('s', k), ('l', u.min()), ('r', u.max()), ('t', v.max()), ('b', v.min())):
                    out[key].append(round(float(val), 3))
            return out

        def special(sv, shown, offsets, title=False, fit=False):
            """A camera given for the title page or the Completed View (see __init__), or the finished model's (framing the parts
            as that view poses them, if it poses any, or always with fit: a Part guide's)."""
            t, r = _fit(self.model, shown, [offsets]) if sv.get('poses') or fit else (hero_target, hero_radius)
            base = dict(hero, target=t.round(1).tolist(), radius=round(r, 1))
            if 'dir' in sv:
                cam = given(sv)
                if 'min_aspect' in sv:
                    cam['min_aspect'] = float(sv['min_aspect'])
                    if isinstance(sv.get('otherwise'), (list, tuple)):     # several, closest first, then the finished model's:
                        shifts = [round(0.05 * k, 2) for k in range(31)] if title else [0.0]   # the player takes the first that fits
                        if title and float(sv.get('shift', 0.0)) != 0.0:
                            raise ValueError('start_view with a list of `otherwise` cameras: give its own camera shift=0 (the player works the shift out)')
                        cam['otherwise'] = [given(c) for c in sv['otherwise']] + [base]
                        for c in [cam] + cam['otherwise']:
                            c['fit'] = reach(c, shown, offsets, shifts)
                        if sv.get('clear_title'):
                            cam['clear_title'] = True
                    else:
                        cam['otherwise'] = given(sv['otherwise']) if sv.get('otherwise') else base
                elif sv.get('otherwise') or sv.get('clear_title'):
                    raise ValueError('start_view / end_view: `otherwise` and `clear_title` need min_aspect')
                return cam
            return dict(base, dir=_direction(sv.get('azimuth', self.hero_azimuth), sv.get('elevation', 32)).round(4).tolist(),
                        radius=round(r * sv.get('zoom', 1.0), 1)) if (sv.keys() - {'poses', 'hide'}) else base
        views[0]['camera'] = special(self.start_view, start_shown, start_last, title=True)
        views[-1]['camera'] = special(self.end_view, end_shown, end_last)
        if self.taken:                                     # a deconstruction: the Full Build's title page; it ends closer in, on what is left
            if not self.start_view:
                views[0]['camera'] = copy.deepcopy(self.taken['start']['camera'])
            if not end_shown:
                raise SystemExit('a deconstruction ends on what is left assembled (the base it is built on): this one takes everything off')
            if not self.end_view:
                t, r = _fit(self.model, end_shown, [end_last])
                last_cam = next((v['camera'] for v in reversed(views[:-1]) if v['kind'] in ('hover', 'done') and 'camera' in v), None)
                views[-1]['camera'] = dict(dir=last_cam['dir'] if last_cam and not last_cam.get('flip') else hero['dir'], target=t.round(1).tolist(), radius=round(r, 1))
        for v in views:
            if 'camera' not in v:
                v['camera'] = hero
        # Views shown with the model turned over are turned all the same way, about the same point, for as long as they
        # follow one another: the player turns the model about camera['pivot'] (along camera['flip_axis']), so the model
        # itself stays put from step to step and only the camera moves (it turns over again only after a card or a view
        # that is the right way up).
        fb = [v for v in views if v.get('_only') != 'part']   # (the Full Build's own views: a card only a Part has does not break its runs)
        run = None
        for v in fb:
            cam = v['camera']
            if v['kind'] == 'card' or not cam.get('flip'):
                run = None
                continue
            if run is None:
                level = np.array([cam['dir'][0], 0.0, cam['dir'][2]])
                axis = level / np.linalg.norm(level) if np.linalg.norm(level) > 1e-4 else np.array([1.0, 0.0, 0.0])   # (a view straight up or down)
                run = dict(pivot=list(cam['target']), flip_axis=axis.round(4).tolist())
            v['camera'] = dict(cam, **run)
        # ...and a stretch of them seen from the same corner keeps one framing (a sphere round all of theirs), so that the
        # model does not slide about the screen from step to step; the camera moves only when the corner changes (Lee, 14 Oct 2026).
        k = 0
        while k < len(fb):
            cam = fb[k]['camera']
            if fb[k]['kind'] == 'card' or not cam.get('flip'):
                k += 1
                continue
            j = k
            while j + 1 < len(fb) and fb[j + 1]['kind'] != 'card' and fb[j + 1]['camera'].get('flip') and fb[j + 1]['camera']['dir'] == cam['dir']:
                j += 1
            spheres = [(np.array(fb[i]['camera']['target'], float), float(fb[i]['camera']['radius'])) for i in range(k, j + 1)]
            centre, radius = spheres[0]
            for c, r in spheres[1:]:                    # the smallest sphere round two spheres, one at a time
                d = np.linalg.norm(c - centre)
                if d + r <= radius:
                    continue
                if d + radius <= r:
                    centre, radius = c, r
                    continue
                new_r = (d + radius + r) / 2
                centre, radius = centre + (c - centre) * ((new_r - radius) / d), new_r
            for i in range(k, j + 1):
                fb[i]['camera'] = dict(fb[i]['camera'], target=centre.round(1).tolist(), radius=round(radius, 1))
            k = j + 1

        # parts list: identical parts collapse to one entry with a quantity
        parts, seen = [], {}
        for i in used:
            name = self.names.get(i)
            if not name or i in self.part_of or i in self.unlisted:
                continue
            if name in seen:
                seen[name]['ids'].append(i)
                seen[name]['qty'] += 1
            else:
                seen[name] = dict(name=name, ids=[i], qty=1, **({'view': self.part_views[name]} if name in self.part_views else {}))
                fitted = [c for c, parent in self.part_of.items() if parent == i and c in used]
                if fitted:
                    seen[name]['with'] = fitted
                parts.append(seen[name])

        for extra in self.listed_extra:                     # parts listed by hand, after the part they follow
            entry = {k: v for k, v in extra.items() if k != '_after'}
            at = next((k + 1 for k, p in enumerate(parts) if p['name'] == extra['_after']), len(parts))
            parts.insert(at, entry)
        for p in parts:                                     # pictures laid out by hand
            how = self.pictured.get(p['name'])
            if how:
                p['with'] = list(dict.fromkeys(p.get('with', []) + how['add']))
                if how['poses']:
                    p['poses'] = how['poses']
                if how['wires']:
                    p['wires'] = how['wires']
        slug = lambda name: re.sub(r'[^A-Za-z0-9]+', '-', name.strip()).strip('-')     # (the file names parts.html saves the pictures under)
        for p in parts:
            p['picture'] = f"parts/{slug(p['name'])}.png"
            fitted_to = lambda i: [c for c, parent in self.part_of.items() if parent == i and c in used]
            for how in self.piece_pictures.get(p['name'], []):   # a second picture, of one piece that looks different (see part_picture)
                if how['piece'] not in p['ids']:              # (a guide for one part of the build may not show that piece)
                    self.log.append(f"  part_picture({p['name']!r}, piece={how['piece']!r}): that piece is not shown here, so it has no picture of its own")
                    continue
                p.setdefault('also', []).append(dict(ids=[how['piece']], picture=f"parts/{slug(how['file'])}.png",
                                                     **({'with': list(dict.fromkeys(fitted_to(how['piece']) + how['add']))} if fitted_to(how['piece']) or how['add'] else {}),
                                                     **({'poses': how['poses']} if how['poses'] else {}), **({'wires': how['wires']} if how['wires'] else {})))
            covered = {i for a in p.get('also', []) for i in a['ids']}
            if covered and p['ids'][0] in covered:            # the main picture (parts.html draws the first id) must be of a piece with no picture of its own
                main = next((i for i in p['ids'] if i not in covered), None)
                if main is None:
                    raise SystemExit(f"part_picture: every {p['name']} piece has a picture of its own; leave one to the main picture")
                old = p['ids'][0]
                p['ids'] = [main] + [i for i in p['ids'] if i != main]
                if p.get('with'):
                    p['with'] = [c for c in p['with'] if c not in fitted_to(old)]
                p['with'] = list(dict.fromkeys(fitted_to(main) + p.get('with', [])))
                if not p['with']:
                    del p['with']
        for name in set(self.piece_pictures) - {p['name'] for p in parts}:
            self.log.append(f"  part_picture({name!r}, piece=...): no part called {name!r} in this guide's parts list")
        files = [p['picture'] for p in parts] + [a['picture'] for p in parts for a in p.get('also', [])]
        low = [f.lower() for f in files]                     # (the Mac's disk does not tell Nano-Board.png from nano-board.png)
        if len(low) != len(set(low)):
            raise SystemExit(f'two parts list pictures would share a file: {sorted(f for f in files if low.count(f.lower()) > 1)}')
        chapters = self._chapters(views, routes, parts, first_view, steps_end, special, used) if self.chapters else []
        views[:] = [v for v in views if v.get('_only') != 'part']          # (a card only its Part guide shows: note(only_in='part'))
        for v in views:
            for key in ('_step', '_only', '_part'):
                v.pop(key, None)
        if self.parts_list:                                 # the parts list, on pages of its own after the title page
            for k, page in enumerate(self.parts_list(parts)):
                views.insert(1 + k, dict(name=page['name'], kind='card', caption=page['name'], parts=page['groups'], visible=[], offsets={}, camera=hero))

        model_file = self.kit_dir / 'model.glb'
        stamp = f'?v={model_stamp(model_file)}' if model_file.exists() else ''     # so browsers refetch the model only when it changes
        logo = next((f for f in ('logo.svg', 'logo.png', 'logo.webp') if (self.kit_dir / f).exists()), None)
        meta = dict(self.meta, **({'logo': logo} if logo else {}))
        names = {i: self.hover_names.get(i, self.hover_names.get(self.part_of.get(i), self.names[i])) for i in used if i in self.names}   # (a part fitted to another takes its hover name)
        out = dict(meta=meta, model='model.glb' + stamp, fov=self.cfg['fov'], frame_padding=self.cfg['frame_padding'],
                   names=names, mesh_names=self.mesh_names, wires=self.wire_defs, routes=routes, views=views)
        written = [self.steps_file]
        if chapters:                                     # (one run: every Part is cut from this very Full Build, which says so)
            run = hashlib.sha256(json.dumps(out, sort_keys=True).encode('utf-8')).hexdigest()[:12]
            out['meta'] = dict(meta, run=run)
        json.dump(out, open(self.kit_dir / self.steps_file, 'w'), indent=1)
        if self.steps_file == 'steps.json':              # (the Full Build's parts list: the kit's part pictures are made from it)
            json.dump(dict(meta=self.meta, parts=parts), open(self.kit_dir / 'parts.json', 'w'), indent=1)
            written.append('parts.json')
        if self.steps_file == 'steps.json' and (chapters or (self.kit_dir / 'chapters.json').exists()):   # (only the Full Build has Parts)
            written += self._write_chapters(chapters, out, names)
        for line in self.log:
            print(line)
        print(f"{len(self.steps)} steps -> {len(views)} views, {len(parts)} parts, {len(self.wire_defs)} wires; wrote {', '.join(written)}")
        self._sync_model()
        return out

    def _chapters(self, views, routes, parts, first_view, steps_end, special, used):
        """The Part guides (see chapter()): each one's views, cut from the Full Build's (before its parts list pages go in)."""
        marks, out = self.chapters, []
        for k, c in enumerate(marks):
            end_at = marks[k + 1]['at'] if k + 1 < len(marks) else len(self.steps)
            a = first_view[c['at']] if c['at'] < len(first_view) else steps_end
            b = first_view[end_at] if end_at < len(first_view) else steps_end
            for k2 in range(a, b):                       # (a card only the Full Build has, between two turned-over views: the Part turns over twice)
                if views[k2].get('_only') == 'full' and 0 < k2 < len(views) - 1 and views[k2 - 1].get('camera', {}).get('flip') and views[k2 + 1].get('camera', {}).get('flip'):
                    self.log.append(f"  NOTE: chapter {c['slug']!r}: the card {views[k2]['caption'][:30]!r}, left out of the Part, sits between turned-over steps")
            core = [copy.deepcopy(v) for v in views[a:b] if v.get('_only') != 'full']
            state = next((v for v in reversed(core) if v['kind'] in ('hover', 'done')), None)
            if state is None:
                raise SystemExit(f"chapter {c['slug']!r}: it has no step that shows the model")
            order = list(dict.fromkeys(v['_step'] for v in core))         # (numbered from 1, step by step: a card only the Part has counts too)
            renamed = {}
            for v in core:
                new = f"Step {order.index(v['_step']) + 1}" + ('c' if v['kind'] == 'done' and v['name'].endswith('c') else '')
                renamed[new] = None if v.get('_only') == 'part' else v['name']
                v['name'] = new
                own = v.pop('_part', None)                                 # the step as this Part shows it (in_part())
                if own:
                    v.update({key: val for key, val in own.items() if key in ('caption', 'camera')})
                    if 'caution' in own:
                        v.pop('caution', None)
                        if own['caution']:
                            v['caution'] = own['caution']
                    for key in ('labels', 'eye', 'inset'):
                        if key in own and key in v:
                            v[key] = own[key]
            self._part_text(c['slug'], core)
            cited = [v['name'] for v in core if re.search(r'\bSteps? \d', f"{v.get('caption') or ''} {v.get('caution') or ''}")]
            if cited:
                self.log.append(f"  NOTE: chapter {c['slug']!r}: {', '.join(dict.fromkeys(cited))} name a step by number, the Full Build's (the Part's start at 1)")
            # (a boundary that falls inside something that belongs together is allowed, but worth a look)
            if a > 1 and views[a - 1]['kind'] in ('hover', 'done') and views[a - 1]['camera'].get('flip') and core[0].get('camera', {}).get('flip'):
                self.log.append(f"  NOTE: chapter {c['slug']!r} begins in the middle of steps shown turned over ({views[a - 1]['name']} / {renamed.get(core[0]['name'], core[0]['name'])})")
            if core[0].get('isolated'):
                self.log.append(f"  NOTE: chapter {c['slug']!r} begins in the middle of a sub-assembly built in the hand")
            before = [v for v in views[1:a] if v['kind'] in ('hover', 'done', 'card')]
            seen = {i for v in before for i in v.get('visible', [])}
            shown = {i for v in core for i in v.get('visible', [])}
            new_ids = [i for i in used if i in shown and i not in seen]
            ch_parts = []
            for p in parts:                                   # this Part's own parts: the kinds it brings in, as many as it brings
                ids = [i for i in p['ids'] if i in new_ids]
                if not ids:
                    continue
                e = copy.deepcopy(p)
                e['ids'], e['qty'] = ids, (len(ids) if len(p['ids']) == p['qty'] else p['qty'])
                also = [dict(x, ids=[i for i in x['ids'] if i in ids]) for x in e.pop('also', [])]
                also = [x for x in also if x['ids']]
                if also and all(any(i in x['ids'] for x in also) for i in ids) and len(also) == 1:
                    e['picture'] = also[0]['picture']         # (every piece it brings has a picture of its own: that one)
                elif also:
                    e['also'] = also
                e.pop('group', None)
                ch_parts.append(e)
            visible = [i for i in state['visible']]
            sv, ev = c['start_view'], c['end_view']
            def offsets_of(sv_):
                """Where the Part's title page / Completed View shows each part: as the Part leaves it, but for its own poses, and the
                parts riding on a posed part go with it (as posed() does for the Full Build's)."""
                turns = {i: pose for i, pose in (sv_.get('poses') or {}).items() if i in visible}
                out = {**state['offsets'], **{i: pose_out(compose(pose, state['offsets'].get(i), self._pivot(i))) for i, pose in turns.items()}}
                carry, moved = state.get('carry') or {}, set(turns)
                for _ in range(len(carry)):                  # (riders of riders too)
                    more = {i for i, c in carry.items() if c['by'] in moved and i not in moved and i not in turns}
                    for i in more:
                        out[i] = pose_out(compose(out.get(carry[i]['by']), carry[i]['pose'], self._pivot(i)))
                    moved |= more
                    if not more:
                        break
                return out
            start_shown = [i for i in visible if i not in sv.get('hide', ())]
            end_shown = [i for i in visible if i not in ev.get('hide', ())]
            start_off, end_off = offsets_of(sv), offsets_of(ev)
            wires_of = lambda shown_: {w: no for w, no in (state.get('wires') or {}).items() if all(routes[no].get(e) is None or routes[no][e] in shown_ for e in ('a', 'b'))}
            start = dict(name='Start', kind='start', visible=start_shown, offsets=start_off, wires=wires_of(start_shown), carry=state.get('carry', {}),
                         camera=special(sv, start_shown, start_off, title=True, fit=True))
            end = dict(name='Completed View', kind='end', visible=end_shown, offsets=end_off, wires=wires_of(end_shown), carry=state.get('carry', {}),
                       camera=special(ev, end_shown, end_off, fit=True), **({'cut': True} if ev.get('poses') else {}))
            pages = []
            if self.parts_list and ch_parts:
                hero_cam = start['camera'] if 'dir' in start['camera'] else None
                for page in self.parts_list(copy.deepcopy(ch_parts)):
                    pages.append(dict(name=page['name'], kind='card', caption=page['name'], parts=page['groups'], visible=[], offsets={},
                                      camera={key: val for key, val in (hero_cam or {}).items() if key in ('dir', 'target', 'radius')}))
            for v in core:
                v.pop('_step', None)
                v.pop('_only', None)
            in_full = [name for name in renamed.values() if name]
            out.append(dict(chapter=c, views=[start] + pages + core + [end], renamed=renamed, parts=ch_parts,
                            first=in_full[0] if in_full else '', last=in_full[-1] if in_full else ''))
        return out

    def _part_text(self, slug, core):
        """Apply a Part's own edited wording (step-text-<slug>.json, from tools/step_text.py import ... --only-this-part) to its
        views, over the Full Build's wording and in_part()'s: {"steps": [{"key", "step", "caption"?, "caution"?, "was_caution"?}]}."""
        path = self.kit_dir / f'step-text-{slug}.json'
        if not path.exists():
            return
        edits = {e['key']: e for e in json.loads(path.read_text(encoding='utf-8')).get('steps', [])}
        done = set()
        for e in edits.values():
            hit = [v for v in core if v.get('text_key') == e['key']]
            if not hit:
                self.log.append(f'  WARNING: {path.name} has wording for a step Part {slug!r} no longer has ({e.get("step", "")} {e["key"]}: '
                                f'"{e.get("caption", "")[:50]}")')
                continue
            done.add(e['key'])
            stale = 'caution' in e and (hit[0].get('caution') or '') != e.get('was_caution', hit[0].get('caution') or '')
            if stale:
                self.log.append(f'  WARNING: the caution of Part {slug!r} {hit[0]["name"]} has changed since it was edited outside; the edited '
                                f'caution is not used ({path.name})')
            for v in hit:
                if e.get('caption', '').strip():
                    v['caption'] = e['caption']
                if 'caution' in e and not stale:
                    v.pop('caution', None)
                    if e['caution'].strip():
                        v['caution'] = e['caution'].strip()
        self.log.append(f'{path.name}: wording of {len(done)} step(s) applied to Part {slug!r}')

    def _write_chapters(self, chapters, full, names):
        """Write each Part guide (steps-<slug>.json) and chapters.json, the map; take away the files of Parts no longer there."""
        old = self.kit_dir / 'chapters.json'
        before = [c['file'] for c in json.load(open(old)).get('chapters', [])] if old.exists() else []
        written, entries = [], []
        for ch in chapters:
            c, views = ch['chapter'], ch['views']
            used_routes = sorted({no for v in views for no in (v.get('wires') or {}).values()} |
                                 {no for v in views for nos in (v.get('wire_via') or {}).values() for no in nos})
            remap = {old_no: k for k, old_no in enumerate(used_routes)}
            for v in views:
                if v.get('wires'):
                    v['wires'] = {w: remap[no] for w, no in v['wires'].items()}
                if v.get('wire_via'):
                    v['wire_via'] = {w: [remap[no] for no in nos] for w, nos in v['wire_via'].items()}
            wire_ids = {w for v in views for w in (v.get('wires') or {})} | {w for v in views for w in (v.get('wire_via') or {})}
            shown = {i for v in views for i in v.get('visible', [])}
            meta = dict(full['meta'], part=c['part'], chapter=c['slug'])
            file = f"steps-{c['slug']}.json"
            json.dump(dict(full, meta=meta, names={i: n for i, n in names.items() if i in shown},
                           wires={w: d for w, d in full['wires'].items() if w in wire_ids}, routes=[full['routes'][o] for o in used_routes], views=views),
                      open(self.kit_dir / file, 'w'), indent=1)
            written.append(file)
            entries.append(dict(slug=c['slug'], part=c['part'], file=file, first=ch['first'], last=ch['last'],
                                parts=[dict(name=p['name'], qty=p['qty']) for p in ch['parts']], views=ch['renamed']))
        for f in before:                                 # (a Part taken out or renamed: its old file would mislead)
            if f not in written and (self.kit_dir / f).exists():
                (self.kit_dir / f).unlink()
                self.log.append(f'  removed {f}: no chapter() makes it any more')
        if chapters:
            json.dump(dict(_about='The Part guides cut from this kit\'s Full Build (stepgen.py chapter()): for each, its file, its first and '
                                  'last step in the Full Build, the parts it brings in, and its step names -> the Full Build\'s.',
                           full_build=self.steps_file, run=full['meta']['run'], chapters=entries), open(old, 'w'), indent=1)
            written.append('chapters.json')
        elif old.exists():
            old.unlink()
        return written

    def _sync_model(self):
        """model.glb holds the parts the kit's guides show (every steps file in the kit folder: the Full Build, its Parts, a
        guide of its own such as a deconstruction), so rebuild it whenever that set changes: no guide ever shrinks it below
        what another needs."""
        import build_model
        from glbio import read_glb
        model_file = self.kit_dir / 'model.glb'
        needed = build_model.parts_shown(self.kit_dir) or set()
        have = {n.get('name') for n in read_glb(model_file)[0]['nodes']} if model_file.exists() else set()
        report = self.kit_dir / 'model.report.json'
        kept = json.load(open(report))['summary'].get('parts_kept') if report.exists() else None
        if needed <= have and kept == len(needed):
            return
        print('The set of parts the kit\'s guides show has changed: rebuilding model.glb ...')
        build_model.build(self.kit_dir)
