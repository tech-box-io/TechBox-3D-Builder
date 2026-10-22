"""TechBox's published LAC take-apart (Cadasio 19075-lac_deconstruction): the payload's tree, a replay of its steps, and world
placements in OUR assembly frame (mm, Y up). A library for published_geometry.py (light: JSON only, no CAD; ~1 s, < 150 MB).

How the payload is read (docs/research/guide_19075-lac_deconstruction.md section 1 "Data caveat", and the LSM's
docs/research/lsm/decon/published/replay_decon.py, which this follows):
  * Every step's `properties` change the state left by the step before, in `orderedSteps` order, hidden steps included.
  * Visibility is per leaf solid: its start value is "no node of its chain has hidden: true in the tree"; from then on only the leaf's
    own `visible` counts. (Checked here too: the steps set `visible` on leaves only, except where noted by `nonleaf_visible`.)
  * `position` / `rotation` (quaternion x, y, z, w) replace a node's local translation / turn in its parent's frame (three.js
    object.position / quaternion). The tree's `transform` is a three.js Matrix4 array (column-major): the home placement.
    World placement = the chain's local matrices multiplied out (the root's is the identity).
  * mm = scene units / assemblyStructure.scaleFactor (0.6054634). The published scene is our assembly frame scaled by that factor
    (docs/research/lac/cad_study.md section 7: fitted on F1, F3, F7 x2, F8, F9 to 0.0006 mm), so scene / SF = our assembly mm, no turn.
"""
import collections
import json
import math
import re
from pathlib import Path

import numpy as np
from scipy.spatial.transform import Rotation

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / 'docs/research/lac/decon/published/raw/19075-lac_deconstruction.json'
WIRES = ROOT / 'LAC Build Instructions/wire-paths.json'

j = json.load(open(SRC))
steps, order, A, tcp = j['steps'], j['orderedSteps'], j['assemblyStructure'], j['toolboxComponentsProperties']
SF = A['scaleFactor']
MM = 1.0 / SF
rv = A['rootVersions']

refs = {}


def _walk(n, parent):
    r = n['rootReference']
    t = [float(x) for x in r['transform'].split(',')] if r.get('transform') else None
    m = np.array(t).reshape(4, 4).T if t and len(t) == 16 else np.eye(4)
    refs[r['id']] = dict(name=r['name'], parent=parent, hidden=bool(r.get('hidden')), ver=r.get('childVersionId'),
                         kids=[c['rootReference']['id'] for c in n.get('children') or []], R=m[:3, :3].copy(), t=m[:3, 3].copy())
    for c in n.get('children') or []:
        _walk(c, r['id'])


_walk(A, None)
ROOTID = A['rootReference']['id']


def chain(k):
    out = []
    while k is not None:
        out.append(k)
        k = refs[k]['parent']
    return out


CH = {k: chain(k) for k in refs}
TOP = {k: (CH[k][-2] if len(CH[k]) >= 2 else k) for k in refs}
TOPS = refs[ROOTID]['kids']
leaves = [k for k, v in refs.items() if not v['kids']]
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


def _leaf_box(k):
    v = rv.get(refs[k]['ver']) or {}
    if v.get('versionMinX') is None:
        return None
    return np.array([v['versionMin' + a] for a in 'XYZ']) * MM, np.array([v['versionMax' + a] for a in 'XYZ']) * MM


BOX = {k: _leaf_box(k) for k in leaves}


def v3(d):
    return np.array([float(d.get('x', 0)), float(d.get('y', 0)), float(d.get('z', 0))])


def r2(v, n=2):
    return [round(float(x), n) for x in v]


class State:
    """The replay state: per node visibility, position and rotation overrides; toolbox state; camera; scene up axis."""

    def __init__(self):
        self.vis = {k: not any(refs[a]['hidden'] for a in CH[k]) for k in refs}
        self.pos, self.rot, self.col = {}, {}, {}
        self.tb = {k: dict(v) for k, v in tcp.items()}
        for t in self.tb.values():
            t.setdefault('visible', False)
        self.cam = dict((j.get('cameraProperties') or {}).get('default_camera') or {})
        self.scene = {}
        for sc in (j.get('scenes') or {}).values():
            self.scene.update(sc)
        self.nonleaf_visible = collections.Counter()
        self.stale = set()

    def apply(self, s):
        scene_ids = set((j.get('scenes') or {}).keys())
        for k, p in (s.get('properties') or {}).items():
            if not isinstance(p, dict):
                continue
            if k in refs:
                if p.get('visible') is not None:
                    self.vis[k] = bool(p['visible'])
                    if refs[k]['kids']:
                        self.nonleaf_visible[NAME[k]] += 1
                if isinstance(p.get('position'), dict):
                    self.pos[k] = v3(p['position'])
                if isinstance(p.get('rotation'), dict):
                    self.rot[k] = p['rotation']
                if p.get('colour_main'):
                    self.col[k] = p['colour_main']
            elif k in self.tb:
                for a, b in p.items():
                    if a == 'visible' and b is None:
                        continue
                    self.tb[k][a] = b
            elif k == 'default_camera':
                self.cam.update(p)
            elif k in scene_ids:
                self.scene.update(p)
            else:
                self.stale.add(k)

    # ------------------------------------------------------------ geometry
    def local(self, k, home=False):
        m = np.eye(4)
        r = refs[k]
        if not home and k in self.rot:
            q = self.rot[k]
            m[:3, :3] = Rotation.from_quat([q.get('x', 0), q.get('y', 0), q.get('z', 0), q.get('w', 1)]).as_matrix()
        else:
            m[:3, :3] = r['R']
        m[:3, 3] = (self.pos[k] if (not home and k in self.pos) else r['t']) * MM
        return m

    def world(self, k, home=False):
        m = np.eye(4)
        for a in reversed(CH[k][:-1]):
            m = m @ self.local(a, home)
        return m

    def below_top(self, k):
        m = np.eye(4)
        c = CH[k]
        for a in reversed(c[:c.index(TOP[k])]):
            m = m @ self.local(a, True)
        return m

    def leaf_top(self, k):
        """The top-level part's world matrix implied by one leaf's placement now (a leaf moved inside its part shows as its own group)."""
        return self.world(k) @ np.linalg.inv(self.below_top(k))

    def world_box(self, ks, home=False):
        los, his = [], []
        for k in ks:
            b = BOX.get(k)
            if b is None:
                continue
            lo, hi = b
            c = np.array([[x, y, z, 1] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
            w = (self.world(k, home) @ c.T).T[:, :3]
            los.append(w.min(0))
            his.append(w.max(0))
        if not los:
            return None
        return np.min(los, 0), np.max(his, 0)

    def visible_leaves(self, t):
        return [k for k in top_leaves[t] if self.vis[k]]

    def groups(self, t):
        """A part's visible leaves split by placement (a knob or nut moved apart from its potentiometer is its own group)."""
        g = collections.OrderedDict()
        for k in self.visible_leaves(t):
            M = self.leaf_top(k)
            key = (tuple(np.round(M[:3, 3], 2)), tuple(np.round(M[:3, :3].ravel(), 3)))
            g.setdefault(key, []).append(k)
        return list(g.values())


HOME = State()          # never advanced: home placements


def home_top(t):
    return HOME.world(t, home=True)


def screw(M):
    """A rigid move (4x4) as a screw: unit axis, angle (deg), the point on the axis nearest the origin's image... returned as
    (axis, deg, point_on_axis, slide_along_axis). For a pure translation axis=None."""
    R, t = M[:3, :3], M[:3, 3]
    rv_ = Rotation.from_matrix(R).as_rotvec()
    ang = float(np.linalg.norm(rv_))
    if ang < 1e-6:
        return None, 0.0, None, t
    u = rv_ / ang
    slide = float(t @ u)
    tp = t - slide * u                     # the part of t across the axis: (I - R) p = tp for p on the axis
    A_ = np.eye(3) - R
    p, *_ = np.linalg.lstsq(A_, tp, rcond=None)
    p = p - (p @ u) * u                    # (the point of the axis nearest the origin)
    return u, math.degrees(ang), p, slide


def pose_about(M, pivot):
    """stepgen's turned()/pose form of a world move M (4x4) about `pivot` (our assembly mm): [dx, dy, dz] or
    {t, r: axis + degrees, at}: apply_pose(pose, x) = R (x - at) + at + t."""
    c = np.asarray(pivot, float)
    t = M[:3, :3] @ c + M[:3, 3] - c
    turn = Rotation.from_matrix(M[:3, :3]).as_rotvec()
    ang = float(np.linalg.norm(turn))
    if ang < 1e-5:
        return r2(t)
    return dict(t=r2(t), r=r2(turn / ang, 5) + [round(math.degrees(ang), 3)], at=r2(c))


def cam_view(c, fov=45.0):
    p, t = v3(c['position']) * MM, v3(c['orbit_target']) * MM
    d = p - t
    dist = float(np.linalg.norm(d))
    u = d / dist
    out = dict(eye=r2(p), target=r2(t), distance=round(dist, 2), view_dir=r2(u, 4),
               radius=round(dist * math.sin(math.radians(fov / 2)) / 1.08, 2),
               elevation=round(math.degrees(math.asin(max(-1, min(1, u[1])))), 1),
               azimuth=round(math.degrees(math.atan2(u[0], u[2])), 1))
    if c.get('rotation'):
        q = c['rotation']
        R = Rotation.from_quat([q['x'], q['y'], q['z'], q['w']]).as_matrix()
        up_cam, fwd = R[:, 1], -R[:, 2]
        out['camera_up'] = r2(up_cam, 4)
        out['looks_along'] = r2(fwd, 4)
        yproj = np.array([0, 1.0, 0]) - fwd * fwd[1]
        yproj /= np.linalg.norm(yproj)
        out['roll_deg_from_world_up'] = round(math.degrees(math.atan2(np.dot(np.cross(yproj, up_cam), fwd), np.dot(yproj, up_cam))), 2)
        out['eye_on_view_dir_deg'] = round(math.degrees(math.acos(max(-1, min(1, float(-fwd @ u))))), 3)
    return out
