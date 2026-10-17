"""Turn a raw CAD export (GLB from STEP) into the small, coloured model the player loads.

    python tools/build_model.py <kit folder>

Reads  <kit>/source.glb (or the `source` named in materials.json) and <kit>/materials.json.
Writes <kit>/model.glb and <kit>/model.report.json.
If <kit>/steps.json exists, only the parts that guide shows are kept (the rest of the CAD is never
drawn, so there is no reason to download it), and the guide is pointed at the new model.

What it does, per mesh:
  * colours it from materials.json — one colour, or several by splitting the mesh into its
    disconnected solids (a Nano board is one mesh in the STEP export but ~270 solids);
  * simplifies the triangles to a tolerance in millimetres (purchased parts such as screws, servos
    and cables carry far more detail than a student can see);
  * roughens laser-cut plates ("roughen_mm"): their edges shifted a fraction of a millimetre in the
    plate's plane, so that a cutting file traced from the published model comes out slightly wrong
    (a deterrent, not a guarantee: at 0.1 mm most joints would still fit);
  * extracts the outline (crease) edges once, here, so the player never has to compute them;
  * quantizes and meshopt-compresses the result.
Identical meshes (the CAD export repeats a screw's geometry for every screw) are processed and stored once.
Node names and hierarchy are preserved, so step files keep addressing parts by the same ids.
Units in the output are millimetres.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
from scipy.special import ndtr

import ctypes

import meshoptimizer as mo
from meshoptimizer._loader import lib as _molib

# The Python wrapper ships without a signature for this call, so declare it (meshoptimizer.h).
_molib.meshopt_simplifyWithAttributes.argtypes = [
    ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.c_size_t, ctypes.POINTER(ctypes.c_float), ctypes.c_size_t, ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_float), ctypes.c_size_t, ctypes.POINTER(ctypes.c_float), ctypes.c_size_t, ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_size_t, ctypes.c_float, ctypes.c_uint, ctypes.POINTER(ctypes.c_float)]
_molib.meshopt_simplifyWithAttributes.restype = ctypes.c_size_t

sys.path.insert(0, str(Path(__file__).parent))
from glbio import GlbWriter, accessor, node_matrix, read_glb  # noqa: E402


# ---------------------------------------------------------------- geometry helpers
def weld_positions(V, tol=1e-3):
    """Merge vertices that share a position (to `tol` mm). Returns (unique positions, remap)."""
    q = np.round(V / tol).astype(np.int64)
    _, first, inv = np.unique(q, axis=0, return_index=True, return_inverse=True)
    return V[first], inv.reshape(-1)


def split_components(n_vertices, F):
    e = np.vstack([F[:, [0, 1]], F[:, [1, 2]]])
    graph = coo_matrix((np.ones(len(e), dtype=np.int8), (e[:, 0], e[:, 1])), shape=(n_vertices, n_vertices))
    return connected_components(graph, directed=False)


def face_normals(V, F):
    n = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    length = np.linalg.norm(n, axis=1)
    ok = length > 1e-12
    n[ok] /= length[ok, None]
    return n, ok


def feature_edges(V, F, angle_deg):
    """Outline edges of a position-welded mesh: creases sharper than angle_deg, plus open borders."""
    fn, ok = face_normals(V, F)
    F, fn = F[ok], fn[ok]
    if not len(F):
        return np.zeros((0, 2), dtype=np.int64)
    e = np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]])
    face = np.tile(np.arange(len(F)), 3)
    e = np.sort(e, axis=1)
    order = np.lexsort((e[:, 1], e[:, 0]))
    e, face = e[order], face[order]
    new = np.ones(len(e), dtype=bool)
    new[1:] = np.any(e[1:] != e[:-1], axis=1)
    start = np.flatnonzero(new)
    count = np.diff(np.append(start, len(e)))
    # An edge is drawn if it is an open border, or if any face on it turns away from the first by more than the
    # crease angle. (CAD exports sometimes stack several coplanar faces on one edge; those are not outlines.)
    cos = np.einsum('ij,ij->i', fn[face], np.repeat(fn[face[start]], count, axis=0))
    keep = (count == 1) | (np.minimum.reduceat(cos, start) < np.cos(np.radians(angle_deg)))
    return e[start[keep]]


def fillet_edges(V, F, corner_normals, angle_deg, max_radius_mm):
    """Outline edges for corners that are rounded off rather than sharp (the rim of a screw head, say).

    A rounded corner is a narrow band of faces across which the surface turns quickly; no single edge in it
    reaches the crease angle, so feature_edges() draws nothing there and the two surfaces seem to run into
    each other. Here a band whose bend radius is under max_radius_mm, lying between two surfaces that differ
    by more than the crease angle, gets one line: along the band's border with the larger of the two surfaces.

    corner_normals: (faces, 3, 3) the CAD's own shading normal at each corner of each face, which is what
    tells a rounded band from a flat or gently curved face. (A faceted export has none, and gets no lines.)
    """
    fn, ok = face_normals(V, F)
    F, fn, corner_normals = F[ok], fn[ok], corner_normals[ok]
    if len(F) < 4:
        return np.zeros((0, 2), dtype=np.int64)
    tight = np.zeros(len(F), dtype=bool)
    for i, j in ((0, 1), (1, 2), (2, 0)):                 # the normal swings more than the bend radius allows along this side
        swing = np.linalg.norm(corner_normals[:, i] - corner_normals[:, j], axis=1)
        tight |= (swing > 0.05) & (swing * max_radius_mm > np.linalg.norm(V[F[:, i]] - V[F[:, j]], axis=1))
    if not tight.any() or tight.all():
        return np.zeros((0, 2), dtype=np.int64)
    e = np.sort(np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), axis=1)
    face = np.tile(np.arange(len(F)), 3)
    order = np.lexsort((e[:, 1], e[:, 0]))
    e, face = e[order], face[order]
    new = np.ones(len(e), dtype=bool)
    new[1:] = np.any(e[1:] != e[:-1], axis=1)
    start = np.flatnonzero(new)
    two = start[np.diff(np.append(start, len(e))) == 2]   # edges with exactly two faces
    ev, fa, fb = e[two], face[two], face[two + 1]
    crease = np.cos(np.radians(angle_deg))
    gentle = np.einsum('ij,ij->i', fn[fa], fn[fb]) > crease
    # the surfaces either side: patches of the remaining faces, joined across edges gentler than the crease angle
    calm = ~tight[fa] & ~tight[fb] & gentle
    n_patch, patch = connected_components(coo_matrix((np.ones(calm.sum(), dtype=np.int8), (fa[calm], fb[calm])), shape=(len(F), len(F))), directed=False)
    area = np.linalg.norm(np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]), axis=1) / 2
    patch_area = np.bincount(patch, weights=area, minlength=n_patch)
    neighbours = [[] for _ in range(len(F))]              # across any two-face edge that is not itself a crease
    for x, y in zip(fa[gentle], fb[gentle]):
        neighbours[x].append(y)
        neighbours[y].append(x)
    centre = V[F].mean(1)
    out = []
    for k in np.flatnonzero((tight[fa] != tight[fb]) & gentle):
        t, p = (fa[k], fb[k]) if tight[fa[k]] else (fb[k], fa[k])
        seen, queue, far = {t}, [t], None
        while queue and far is None:                      # walk across the band to the surface on its other side
            nxt = []
            for f in queue:
                for g in neighbours[f]:
                    if g in seen:
                        continue
                    seen.add(g)
                    if tight[g]:
                        if np.linalg.norm(centre[g] - centre[t]) < 4 * max_radius_mm:
                            nxt.append(g)
                    elif patch[g] != patch[p] and (far is None or np.linalg.norm(centre[g] - centre[t]) < np.linalg.norm(centre[far] - centre[t])):
                        far = g
            queue = nxt
        if far is None or fn[p] @ fn[far] > crease:
            continue
        if (patch_area[patch[p]], patch[p]) > (patch_area[patch[far]], patch[far]):
            out.append(ev[k])
    return np.array(out, dtype=np.int64).reshape(-1, 2)


def thin_out_edges(V, E, min_spacing_mm):
    """Leave out crease lines packed closer together than min_spacing_mm (a modelled screw thread, knurling).

    At the size a guide is viewed such lines merge into a black patch. A run of lines joined end to end is kept
    or dropped whole, judged by the median distance from its segments to the nearest line running alongside.
    """
    if min_spacing_mm <= 0 or len(E) < 2:
        return E
    a, b = V[E[:, 0]], V[E[:, 1]]
    mid, d = (a + b) / 2, b - a
    length = np.linalg.norm(d, axis=1)
    d = d / np.maximum(length, 1e-9)[:, None]
    pairs = cKDTree(mid).query_pairs(min_spacing_mm + float(length.max()), output_type='ndarray')
    spacing = np.full(len(E), np.inf)
    if len(pairs):
        i, j = pairs[:, 0], pairs[:, 1]
        joined = (E[i][:, :, None] == E[j][:, None, :]).any(axis=(1, 2))        # the next piece of the same line
        r = mid[j] - mid[i]
        along = np.einsum('ij,ij->i', r, d[i])
        side = np.sqrt(np.maximum(np.einsum('ij,ij->i', r, r) - along ** 2, 0.0))
        beside = ~joined & (np.abs(np.einsum('ij,ij->i', d[i], d[j])) > 0.9) & (np.abs(along) < (length[i] + length[j]) / 2)
        np.minimum.at(spacing, i[beside], side[beside])
        np.minimum.at(spacing, j[beside], side[beside])
    graph = coo_matrix((np.ones(len(E), dtype=np.int8), (E[:, 0], E[:, 1])), shape=(len(V), len(V)))
    run = connected_components(graph, directed=False)[1][E[:, 0]]
    keep = np.ones(len(E), dtype=bool)
    for r_id in np.unique(run):
        sel = run == r_id
        keep[sel] = np.median(spacing[sel]) >= min_spacing_mm
    return E[keep]


def simplify(V, N, F, error_mm, normal_weight=0.4):
    """Error-bounded simplification that keeps a subset of the original vertices (so normals stay valid)."""
    if error_mm <= 0 or len(F) < 64:
        return F
    idx = np.ascontiguousarray(F.reshape(-1).astype(np.uint32))
    out = np.zeros_like(idx)
    weights = np.full(3, normal_weight, dtype=np.float32)
    n = mo.simplify_with_attributes(out, idx, np.ascontiguousarray(V, dtype=np.float32), np.ascontiguousarray(N, dtype=np.float32), weights,
                                    target_index_count=12, target_error=float(error_mm), options=mo.SIMPLIFY_ERROR_ABSOLUTE)
    return out[:n].reshape(-1, 3).astype(np.int64)


def drop_degenerate(F):
    return F[(F[:, 0] != F[:, 1]) & (F[:, 1] != F[:, 2]) & (F[:, 0] != F[:, 2])]


def cut_faces(V, N, F, axis, value, tol=1e-6):
    """Split every triangle that crosses the plane (mesh frame) where coordinate `axis` equals `value`, so that a colour region
    can end exactly on that plane (a band round a battery whose sides are a few long triangles). Positions and normals of the
    new corners are interpolated; winding is kept. Returns (V, N, F)."""
    d = V[F, axis] - value                                    # (faces, 3) signed distance of each corner
    s = np.where(np.abs(d) < tol, 0, np.sign(d)).astype(int)
    crossing = (s.max(1) > 0) & (s.min(1) < 0)
    if not crossing.any():
        return V, N, F
    V, N, keep, new = list(V), list(N), F[~crossing].tolist(), []

    def point(a, b):                                          # where edge a-b meets the plane: a new vertex
        t = (value - V[a][axis]) / (V[b][axis] - V[a][axis])
        V.append(V[a] + (V[b] - V[a]) * t)
        n = N[a] + (N[b] - N[a]) * t
        N.append(n / (np.linalg.norm(n) or 1.0))
        return len(V) - 1

    for f, sf in zip(F[crossing], s[crossing]):
        for r in range(3):                                    # turn the corners so that the odd one out comes first
            a, b, c = f[r], f[(r + 1) % 3], f[(r + 2) % 3]
            sa, sb, sc = sf[r], sf[(r + 1) % 3], sf[(r + 2) % 3]
            if sa == 0 and sb * sc < 0:                       # a corner on the plane, the other two either side
                m = point(b, c)
                new += [[a, b, m], [a, m, c]]
                break
            if sa != 0 and sb != 0 and sc != 0 and sb == sc and sa != sb:   # one corner alone on its side
                p, q = point(a, b), point(a, c)
                new += [[a, p, q], [p, b, c], [p, c, q]]
                break
        else:
            keep.append(list(f))                              # (a corner on the plane and the others on one side: nothing to cut)
    return np.array(V), np.array(N), np.array(keep + new, dtype=np.int64)


def smooth_normals(V, F):
    """Area-weighted vertex normals (for tubes and other parts with no hard edges)."""
    fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    n = np.zeros_like(V)
    for k in range(3):
        np.add.at(n, F[:, k], fn)
    length = np.linalg.norm(n, axis=1)
    n[length < 1e-12] = (0.0, 0.0, 1.0)             # sliver faces that cancel out: any unit vector beats a zero one
    length[length < 1e-12] = 1.0
    return n / length[:, None]


def simplify_to_budget(V, N, F, error_mm, max_tris=None, normal_weight=0.4, keep_below_mm=1.5):
    """Simplify to error_mm; if a triangle budget (per colour of a mesh) is given and missed, relax the tolerance, up to 8x.

    Solids smaller than keep_below_mm (solder pads, chip legs) only ever get the base tolerance:
    relaxing it for them makes them vanish altogether.
    Returns (faces, tolerance actually used).
    """
    if error_mm <= 0 or len(F) < 64:
        return F, 0.0
    vp, remap = weld_positions(V)
    n_comp, labels = split_components(len(vp), remap[F])
    span = np.zeros(n_comp)
    lo = np.full((n_comp, 3), np.inf)
    hi = np.full((n_comp, 3), -np.inf)
    np.minimum.at(lo, labels, vp)
    np.maximum.at(hi, labels, vp)
    span = (hi - lo).max(1)
    small = span[labels[remap[F[:, 0]]]] < keep_below_mm
    big, kept = F[~small], simplify(V, N, F[small], error_mm, normal_weight)
    out, err = simplify(V, N, big, error_mm, normal_weight), error_mm
    while max_tris and len(out) + len(kept) > max_tris and err < error_mm * 8:
        err = min(err * 1.6, error_mm * 8)
        out = simplify(V, N, big, err, normal_weight)
    return np.vstack([out, kept]), err


def engraved_faces(V, F, eps=0.02):
    """Faces of a flat panel that belong to a shallow engraving (e.g. the part code lasered into plywood).

    A panel has two outer planes across its thinnest axis. Through-cuts span both planes and the outer
    faces lie in one of them; anything else is a pocket cut part-way in, i.e. an engraving.
    """
    axis = int(np.argmin(np.ptp(V, axis=0)))
    t = V[:, axis][F]
    lo, hi = t.min(1), t.max(1)
    t0, t1 = V[:, axis].min(), V[:, axis].max()
    spans_through = (lo <= t0 + eps) & (hi >= t1 - eps)
    on_outer_plane = (lo >= t1 - eps) | (hi <= t0 + eps)
    return ~spans_through & ~on_outer_plane


def move_engraving(V, N, F, Vp, Fp, face_colour, delta, turn, ink, lift_mm=0.05):
    """Move a panel's engraved code by `delta` (mm, the mesh's own frame), turned by `turn` degrees (0 or 180) about its
    own middle on the face: the pocket is filled in flush with the face, and the pocket's floor is laid on the face at the
    new place, `lift_mm` proud, as a decal in the colour `ink`. Returns V, N, F, face_colour with the decal's faces added."""
    eng = engraved_faces(Vp, Fp)
    if not eng.any():
        return V, N, F, face_colour
    axis = int(np.argmin(np.ptp(Vp, axis=0)))           # across the panel
    t0, t1 = Vp[:, axis].min(), Vp[:, axis].max()
    cut_from_high = Vp[np.unique(Fp[eng]), axis].mean() > (t0 + t1) / 2
    surface, out = (t1, 1.0) if cut_from_high else (t0, -1.0)
    floor = eng & np.all(np.abs(V[F][:, :, axis] - surface) > 0.02, axis=1)
    decal_v = V[F[floor]].reshape(-1, 3).copy()
    if round(turn) % 360 == 180:                        # half round on the face: about the code's own middle, in the face's plane
        middle = (decal_v.min(0) + decal_v.max(0)) / 2
        across = [k for k in range(3) if k != axis]
        decal_v[:, across] = 2 * middle[across] - decal_v[:, across]
    elif round(turn) % 360:
        raise SystemExit('move_engraving: "turn" may be 0 or 180')
    decal_v[:, axis] = surface + out * lift_mm
    decal_v += np.asarray(delta, float)
    decal_n = np.zeros_like(decal_v)
    decal_n[:, axis] = out
    V = V.copy()
    V[np.unique(F[eng]), axis] = surface               # the pocket flush: its floor on the face, its walls flat to nothing
    N[np.unique(F[floor])] = decal_n[0]
    face_colour = face_colour.copy()
    first = len(V)
    V, N = np.vstack([V, decal_v]), np.vstack([N, decal_n])
    F = np.vstack([F, first + np.arange(len(decal_v)).reshape(-1, 3)])
    return V, N, F, np.concatenate([face_colour, np.array([ink] * int(floor.sum()), dtype=object)])


def roughen(V, F, amount_mm, name, wavelength_mm=12.0, n_waves=16):
    """Shift a laser-cut plate's edges by about amount_mm in its own plane, so that a cutting file traced from the model comes
    out slightly wrong while the part looks just the same. A deterrent, not a guarantee: at 0.1 mm a slot's width changes by
    0.04 - 0.14 mm (median, 95th percentile), within laser and plywood tolerances, so most traced joints would still fit.

    The plate's thickness runs along one axis of the mesh's own frame (as engraved_faces assumes), and nothing moves along it.
    Vertices that share a place in the plate's plane (its two faces, the top and bottom of every wall) move together, so the
    faces stay flat and parallel and the walls square to them. Each place moves between half and all of amount_mm, in a
    direction that wanders over the plate: two sums of random waves about wavelength_mm long, seeded by the mesh's name, so
    every build gives the same model. The two sides of a slot or a tab move independently (its width comes out up to about
    2 x amount_mm wrong), while neighbouring points along a curve move nearly alike, so holes stay smooth, the walls turn by
    half a degree on average (they keep their normals) and hardly any crease line comes or goes. (Moving each vertex its own
    random way turns sliver triangles over and draws stray lines across the faces.)
    Returns V, how many corners had to be eased (below) and how many faces are still turned over (should be none).
    """
    axis = int(np.argmin(np.ptp(V, axis=0)))           # across the plate
    across = [k for k in range(3) if k != axis]
    fn, ok = face_normals(V, F)
    area = np.linalg.norm(np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]), axis=1)
    flat = ok & (np.abs(fn[:, axis]) > 0.999)           # faces across the thickness: the plate's two faces, engraving floors
    if area[flat].sum() < 0.5 * area.sum():
        raise SystemExit(f'{name}: "roughen_mm" is for a flat plate whose thickness runs along an axis of its own frame')
    # the places in the plate's plane (vertices within a micron of each other are one place, and end up at one position)
    P = V[:, across]
    pairs = cKDTree(P).query_pairs(1e-3, output_type='ndarray').reshape(-1, 2)
    n, place = connected_components(coo_matrix((np.ones(len(pairs), dtype=np.int8), (pairs[:, 0], pairs[:, 1])), shape=(len(P), len(P))), directed=False)
    centre = np.zeros((n, 2))
    np.add.at(centre, place, P)
    centre /= np.bincount(place, minlength=n)[:, None]

    def waves(salt):
        """A smooth random field over the plate, its values spread like a standard normal's."""
        h = np.array([np.frombuffer(hashlib.sha256(f'{name}/{salt}/{k}'.encode()).digest()[:12], dtype='<u4') for k in range(n_waves)]) / 2.0 ** 32
        heading = 2 * np.pi * h[:, 0]
        k = (2 * np.pi / wavelength_mm) * (0.6 + 0.8 * h[:, 1])
        wave = k[:, None] * np.stack([np.cos(heading), np.sin(heading)], axis=1)
        return np.sqrt(2.0 / n_waves) * np.cos(centre @ wave.T + 2 * np.pi * h[:, 2]).sum(axis=1)
    heading = 2 * np.pi * ndtr(waves('heading'))         # ndtr (the normal distribution function) spreads both evenly over their range
    move = amount_mm * (0.5 + 0.5 * ndtr(waves('distance')))[:, None] * np.stack([np.cos(heading), np.sin(heading)], axis=1)

    # A sliver on a face can still turn over, its middle corner carried across its long side (a few per kit): that corner then
    # moves as the long side does beside it, which keeps the sliver the right way up.
    sound = (place[F[:, 0]] != place[F[:, 1]]) & (place[F[:, 1]] != place[F[:, 2]]) & (place[F[:, 0]] != place[F[:, 2]])
    side = np.stack([np.linalg.norm(centre[place[F[:, (j + 1) % 3]]] - centre[place[F[:, (j + 2) % 3]]], axis=1) for j in range(3)], axis=1)
    middle = np.argmax(side, axis=1)                     # the corner opposite the longest side
    eased = set()
    for _ in range(100):
        out = V.copy()
        out[:, across] = (centre + move)[place]
        fn_out, ok_out = face_normals(out, F)
        over = np.flatnonzero(flat & sound & (~ok_out | (fn_out[:, axis] * fn[:, axis] <= 0)))
        if not len(over):
            break
        for f in over:
            c, a, b = (place[F[f, (middle[f] + j) % 3]] for j in range(3))
            ab = centre[b] - centre[a]
            t = np.clip((centre[c] - centre[a]) @ ab / (ab @ ab), 0.0, 1.0)
            move[c] = (1 - t) * move[a] + t * move[b]
            eased.add(int(c))
    return out, len(eased), len(over)


def compact(F, *attrs):
    """Drop unused vertices; return (reindexed faces, attrs...)."""
    used, inv = np.unique(F.reshape(-1), return_inverse=True)
    return (inv.reshape(F.shape),) + tuple(a[used] for a in attrs)


def weld_attributes(V, N, F):
    """Merge vertices that share position and normal."""
    key = np.hstack([np.round(V / 1e-3), np.round(N * 512)]).astype(np.int64)
    _, first, inv = np.unique(key, axis=0, return_index=True, return_inverse=True)
    return V[first], N[first], inv.reshape(-1)[F]


def srgb_to_linear(hexcode):
    c = np.array([int(hexcode[i:i + 2], 16) / 255 for i in (1, 3, 5)])
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4).tolist()


# ---------------------------------------------------------------- colour rules
class Materials:
    def __init__(self, spec, kit_dir):
        self.palette = spec['palette']
        self.defaults = spec.get('defaults', {})
        self.rules = [(re.compile(r['match']), r) for r in spec['rules']]
        self.kit_dir = kit_dir
        self._atlases = {}
        # "atlas": a file of colours per mesh name, taken from TechBox's own Cadasio project for the kit. A mesh whose
        # rule names no colour of its own takes its colours from there.
        self.atlas_file = spec.get('atlas')
        self.atlas_data = json.load(open(kit_dir / self.atlas_file)) if self.atlas_file else {}

    def rule_for(self, mesh_name):
        own = next((rule for rx, rule in self.rules if rx.search(mesh_name)), {})
        rule = {**self.defaults, **own}
        if not any(k in own for k in ('color', 'components', 'atlas')):
            if isinstance(self.atlas_data.get(mesh_name), dict) and not mesh_name.startswith('_'):
                rule['atlas'] = f'{self.atlas_file}#{mesh_name}'
            elif mesh_name in self.atlas_data.get('_single_colour', {}):
                rule['color'] = self.atlas_data['_single_colour'][mesh_name]
        return rule

    def atlas(self, ref):
        """A colour atlas is a list of solids {min, max, colour} taken from a published Cadasio model of the same part."""
        if ref not in self._atlases:
            path, key = ref.split('#')
            self._atlases[ref] = json.load(open(self.kit_dir / path))[key]
        return self._atlases[ref]


AXIS_MAPS = [(p, s) for p in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0))
             for s in ((1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1), (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1))]


def colour_from_atlas(boxes, atlas):
    """Match each component box to the atlas solid with the closest box, trying every axis mapping.

    boxes: (n, 2, 3) component min/max in mm. Returns (list of hex colours, fraction closely matched, which are skins).
    Atlas entries with "solid": null are marks printed on a solid, not solids: see flat_marks().
    """
    solids = [s for s in atlas['solids'] if s.get('solid', 0) is not None]
    amin = np.array([s['min'] for s in solids])
    amax = np.array([s['max'] for s in solids])
    acol = [s['colour'] for s in solids]
    askin = np.array([bool(s.get('skin')) for s in solids])
    alo, ahi = np.array(atlas['bbox_min']), np.array(atlas['bbox_max'])
    lo, hi = boxes[:, 0].min(0), boxes[:, 1].max(0)
    best = None
    for perm, sign in AXIS_MAPS:
        perm, sign = list(perm), np.array(sign)
        size = (hi - lo)[perm]
        if np.any(np.abs(size - (ahi - alo)) > 0.02 * (ahi - alo).max() + 0.3):
            continue
        # map our coordinates into the atlas frame: permute axes, flip, align box corners
        def to_atlas(p):
            q = (p - lo)[:, perm]
            return np.where(sign > 0, q, size - q) + alo
        a, b = to_atlas(boxes[:, 0]), to_atlas(boxes[:, 1])
        bmin, bmax = np.minimum(a, b), np.maximum(a, b)
        d = np.abs(bmin[:, None] - amin[None]).sum(2) + np.abs(bmax[:, None] - amax[None]).sum(2)
        nearest = d.argmin(1)
        err = d[np.arange(len(boxes)), nearest]
        score = (err < 0.6).mean()
        if best is None or score > best[0]:
            best = (score, [acol[i] for i in nearest], askin[nearest] & (err < 0.6))
    if best is None:
        return None, 0.0, np.zeros(len(boxes), dtype=bool)
    return best[1], float(best[0]), best[2]


def flat_marks(V, F, atlas, tol=0.05):
    """Faces that carry print (the lettering on a servo's label): {colour: face mask}.

    The CAD draws print as flat patches lying on a solid's face; the atlas lists each as an entry with
    "solid": null, "flat": true, "shown": true and its box. A patch is found as a group of faces joined
    through shared vertices (in the mesh as exported, before any welding) whose box is that box.
    """
    marks = [s for s in atlas['solids'] if s.get('solid', 0) is None and s.get('flat') and s.get('shown')]
    if not marks:
        return {}
    n_island, island = split_components(len(V), F)
    lo = np.full((n_island, 3), np.inf)
    hi = np.full((n_island, 3), -np.inf)
    np.minimum.at(lo, island, V)
    np.maximum.at(hi, island, V)
    out = {}
    for s in marks:
        match = np.all(np.abs(lo - np.array(s['min'])) < tol, axis=1) & np.all(np.abs(hi - np.array(s['max'])) < tol, axis=1)
        if match.any():
            out[s['colour']] = out.get(s['colour'], np.zeros(len(F), dtype=bool)) | match[island[F[:, 0]]]
    return out


def order_leads(V, labels, ids):
    """Order a cable's leads as they sit side by side where the cable ends.

    The cable's tip is its point farthest from its middle; each lead's end is its vertex nearest that
    tip; the leads are sorted along the line through those ends. Which side counts as "first" is fixed
    by a rule (the sorting axis points along its largest component), so the same CAD always gives the
    same order. Bundled, non-flat cables work too, which ordering by overall position would not.
    """
    if len(ids) < 2:
        return ids
    pts = [V[labels == c] for c in ids]
    everything = np.vstack(pts)
    tip = everything[np.argmax(np.linalg.norm(everything - everything.mean(0), axis=1))]
    ends = np.array([p[np.argmin(np.linalg.norm(p - tip, axis=1))] for p in pts])
    spread = ends - ends.mean(0)
    axis = np.linalg.svd(spread, full_matrices=False)[2][0]
    if axis[np.argmax(np.abs(axis))] < 0:
        axis = -axis
    return ids[np.argsort(spread @ axis)]


def colour_components(rule, mats, V, F, labels, n_comp):
    """Return a palette-name-or-hex per component, a note for the report, and which components are skins."""
    face_label = labels[F[:, 0]]
    boxes = np.zeros((n_comp, 2, 3))
    for c in range(n_comp):
        pts = V[labels == c]
        boxes[c] = pts.min(0), pts.max(0)
    size = boxes[:, 1] - boxes[:, 0]
    dims = np.sort(size, axis=1)                      # per component: [thin, mid, long]
    volume_rank = np.argsort(-np.prod(np.maximum(size, 1e-3), axis=1))
    out = [rule.get('color')] * n_comp
    note = ''
    skin = np.zeros(n_comp, dtype=bool)
    if 'atlas' in rule:
        cols, score, atlas_skin = colour_from_atlas(boxes, mats.atlas(rule['atlas']))
        note = f'atlas match {score:.0%}'
        if cols is not None and score >= rule.get('atlas_min_match', 0.6):
            swap = rule.get('atlas_colours', {})          # e.g. {"#cccccc": "pin"}: this kit's choice for one of the atlas's colours
            return [swap.get(c, c) for c in cols], note, atlas_skin
        note += ' (too low, fell back to rules)'
    for comp in rule.get('components', []):
        if 'rank' in comp:                            # 0 = biggest solid
            sel = np.zeros(n_comp, dtype=bool)
            ranks = comp['rank'] if isinstance(comp['rank'], list) else [comp['rank']]
            sel[[volume_rank[r] for r in ranks if r < n_comp]] = True
        else:
            sel = np.ones(n_comp, dtype=bool)
        for key, col in (('thin', 0), ('mid', 1), ('long', 2)):
            if key in comp:
                lo, hi = comp[key]
                sel &= (dims[:, col] >= lo) & (dims[:, col] <= hi)
        if 'across' in comp:                          # e.g. the three leads of a servo cable, in order across its connector
            ids = order_leads(V, labels, np.flatnonzero(sel))
            for i, c in enumerate(ids):
                out[c] = comp['across'][min(i, len(comp['across']) - 1)]
        else:
            for c in np.flatnonzero(sel):
                out[c] = comp['color']
        if comp.get('skin'):
            skin |= sel
    return out, note, skin


def faces_under_skin(V, F, face_comp, skin, reach_mm=0.05, never=None):
    """Faces of other solids that lie directly under a skin solid (all three corners and the middle within reach_mm of it).
    `never` marks solids that are left alone (other skins).

    Some CAD parts are a coloured shell a hundredth of a millimetre outside a full copy of the body. Drawn in two
    colours, the two surfaces flicker against each other on screens with a coarse depth buffer; given the skin's
    colour, the body underneath cannot show.
    """
    is_skin = skin[face_comp]
    under = np.zeros(len(F), dtype=bool)
    if not is_skin.any() or is_skin.all():
        return under
    import trimesh
    shell = trimesh.Trimesh(V, F[is_skin], process=False)
    rest = np.flatnonzero(~is_skin if never is None else ~is_skin & ~never[face_comp])
    tri = V[F[rest]]
    # A skin is a copy of the faces it covers, so a covered face has each corner right beside a corner of the skin and
    # its middle right beside the middle of one of the skin's faces: that settles nearly all of them. Faces that are
    # merely near (or that only share their corners with skins, like a board's top face between its pads) are
    # measured against the skin's surface.
    middle = tri.mean(1)
    corner = cKDTree(V[np.unique(F[is_skin])]).query(tri.reshape(-1, 3), distance_upper_bound=1.0)[0].reshape(-1, 3)
    near = (corner < 1.0).all(axis=1)
    sure = (corner <= reach_mm).all(axis=1) & (cKDTree(shell.triangles_center).query(middle, distance_upper_bound=reach_mm + 0.02)[0] < np.inf)
    maybe = np.flatnonzero(near & ~sure)
    for start in range(0, len(maybe), 5000):          # in batches: the exact measure is heavy on memory
        part = maybe[start:start + 5000]
        samples = np.concatenate([tri[part], middle[part][:, None]], axis=1).reshape(-1, 3)
        sure[part] = (shell.nearest.on_surface(samples)[1].reshape(-1, 4) <= reach_mm).all(axis=1)
    under[rest] = sure
    return under


# ---------------------------------------------------------------- changes to the CAD's own arrangement
def pose_matrix(pose):
    """materials.json "adjust_mm": [x, y, z] (mm) moves a part; {"t": [x, y, z], "r": [ax, ay, az, degrees], "at": [x, y, z]}
    turns it about an axis through `at`, then moves it (the same poses as steps.json)."""
    m = np.eye(4)
    if isinstance(pose, dict):
        t, r, at = np.asarray(pose.get('t', [0, 0, 0]), float), pose.get('r'), np.asarray(pose.get('at', [0, 0, 0]), float)
        if r and r[3]:
            ax = np.asarray(r[:3], float) / np.linalg.norm(r[:3])
            a = np.radians(r[3])
            K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
            m[:3, :3] = np.eye(3) + np.sin(a) * K + (1 - np.cos(a)) * K @ K
            m[:3, 3] = at - m[:3, :3] @ at
        m[:3, 3] += t
    else:
        m[:3, 3] = np.asarray(pose, float)
    return m


def add_extra_parts(doc, blob, kit_dir, extras, assembly, to_mm):
    """Parts that come as files of their own (a purchased part's STEP, converted with tools/step_to_glb.py): materials.json
    "extra_parts": {id: {"glb": file in the kit folder, "pose": [x, y, z] or {"t", "r", "at"}}}. The pose places the
    file's own frame (mm) in the assembly. Each becomes a part called `id`, a child of the assembly node, exactly as
    if the CAD export had had it. Returns the new (doc, blob)."""
    doc = json.loads(json.dumps(doc))
    for part_id, spec in extras.items():
        edoc, eblob = read_glb(kit_dir / spec['glb'])
        pad = (-len(blob)) % 4
        offset = len(blob) + pad
        blob = blob + b'\0' * pad + eblob
        bv0, acc0, mesh0, mat0, node0 = (len(doc.get(k, [])) for k in ('bufferViews', 'accessors', 'meshes', 'materials', 'nodes'))
        doc['bufferViews'] += [dict(bv, buffer=0, byteOffset=bv.get('byteOffset', 0) + offset) for bv in edoc['bufferViews']]
        doc['accessors'] += [dict(a, bufferView=a['bufferView'] + bv0) if 'bufferView' in a else dict(a) for a in edoc['accessors']]
        doc.setdefault('materials', []).extend(edoc.get('materials', []))
        for m in edoc['meshes']:
            prims = [dict(pr, attributes={k: v + acc0 for k, v in pr['attributes'].items()}, **({'indices': pr['indices'] + acc0} if 'indices' in pr else {}),
                          **({'material': pr['material'] + mat0} if 'material' in pr else {})) for pr in m['primitives']]
            doc['meshes'].append(dict(m, primitives=prims))
        for n in edoc['nodes']:
            out = dict(n)
            if 'mesh' in n:
                out['mesh'] = n['mesh'] + mesh0
            if 'children' in n:
                out['children'] = [c + node0 for c in n['children']]
            doc['nodes'].append(out)
        roots = [r + node0 for scene in edoc['scenes'] for r in scene['nodes']]
        A = node_matrix(doc['nodes'][assembly])
        A[:3, 3] *= to_mm                              # the assembly node's own matrix, in mm: the pose is in assembly space, as stepgen has it
        place = np.linalg.inv(A) @ pose_matrix(spec['pose'])
        place[:3, 3] /= to_mm                          # (node translations are in the export's metres)
        doc['nodes'].append(dict(name=part_id, children=roots, matrix=place.T.reshape(-1).tolist()))
        doc['nodes'][assembly] = dict(doc['nodes'][assembly], children=doc['nodes'][assembly].get('children', []) + [len(doc['nodes']) - 1])
    doc['buffers'] = [dict(doc['buffers'][0], byteLength=len(blob))]
    return doc, blob


def promote(doc, names, assembly):
    """The CAD nodes named in materials.json "own_parts" become parts of their own (children of the assembly node), where
    they are: the Nano, which the CAD has inside the I/O module's assembly, so that the guide can fit it onto the module."""
    nodes = [dict(n) for n in doc['nodes']]
    parent = {c: i for i, n in enumerate(nodes) for c in n.get('children', [])}
    for name in names:
        i = next((k for k, n in enumerate(nodes) if n.get('name') == name), None)
        if i is None:
            raise SystemExit(f'materials.json own_parts: no node called {name} in the CAD')
        chain, k = [], i
        while k in parent and k != assembly:
            chain.append(k)
            k = parent[k]
        if k != assembly or parent.get(i) == assembly:
            continue                                   # (already a part)
        m = np.eye(4)
        for j in reversed(chain):
            m = m @ node_matrix(nodes[j])
        moved = {key: v for key, v in nodes[i].items() if key not in ('matrix', 'translation', 'rotation', 'scale')}
        nodes[i] = dict(moved, matrix=m.T.reshape(-1).tolist())
        nodes[parent[i]] = dict(nodes[parent[i]], children=[c for c in nodes[parent[i]]['children'] if c != i])
        nodes[assembly] = dict(nodes[assembly], children=nodes[assembly]['children'] + [i])
    return dict(doc, nodes=nodes)


def stickers(doc, blob, specs, to_mm, world, adjust=None, assembly=None):
    """Round stickers that the kit adds to a purchased part (a coloured dot on each motor, to tell them apart).

    specs: materials.json "stickers": [{"on": instance id, "colour": palette name, "diameter_mm": 7, "faces": "wide"}].
    "wide": one on each of the two widest faces of the part's body (across its thinnest axis), in the middle of the part of
    that face that shows when the part is in place: the face is looked at square on, past the parts round it (R7 and R8
    stand across the motors' faces), and the dot goes to the spot nearest the middle of what shows that leaves a little
    room round it (or as much room as there is). Or "at": [x, y, z] (seated assembly mm) instead of "faces": one dot on the
    part's face under that spot, looking along -"normal" (default [0, 1, 0], straight down): a dot on a chip's top (the RCC's
    Nano Boards). Returns [(instance node index, vertices in assembly mm, faces, rim segments, colour)]."""
    import trimesh
    from scipy.ndimage import distance_transform_edt
    adjust = adjust or {}
    nodes = doc['nodes']
    by_name = {n.get('name'): i for i, n in enumerate(nodes)}

    def instance(top):
        """Every mesh of a top-level instance, in assembly mm, where the guide shows it built (adjust_mm included)."""
        parts, todo = [], [top]
        place = pose_matrix(adjust[nodes[top]['name']]) if nodes[top].get('name') in adjust else np.eye(4)
        while todo:
            i = todo.pop()
            todo += nodes[i].get('children', [])
            if 'mesh' in nodes[i]:
                prim = doc['meshes'][nodes[i]['mesh']]['primitives'][0]
                V = accessor(doc, blob, prim['attributes']['POSITION']).astype(np.float64) * to_mm
                F = accessor(doc, blob, prim['indices']).reshape(-1, 3).astype(np.int64)
                m = place @ world[i]
                parts.append(trimesh.Trimesh(V @ m[:3, :3].T + m[:3, 3], F, process=False))
        return trimesh.util.concatenate(parts) if parts else None

    def box_of(top):
        """The instance's box in assembly mm, from its accessors' min and max (cheap)."""
        lo, hi, todo = np.full(3, np.inf), np.full(3, -np.inf), [top]
        place = pose_matrix(adjust[nodes[top]['name']]) if nodes[top].get('name') in adjust else np.eye(4)
        while todo:
            i = todo.pop()
            todo += nodes[i].get('children', [])
            if 'mesh' in nodes[i]:
                a = doc['accessors'][doc['meshes'][nodes[i]['mesh']]['primitives'][0]['attributes']['POSITION']]
                if 'min' not in a:
                    return None
                m = place @ world[i]
                c = np.array([[a['min'][0] if k & 1 else a['max'][0], a['min'][1] if k & 2 else a['max'][1], a['min'][2] if k & 4 else a['max'][2]] for k in range(8)]) * to_mm
                c = c @ m[:3, :3].T + m[:3, 3]
                lo, hi = np.minimum(lo, c.min(0)), np.maximum(hi, c.max(0))
        return lo, hi

    tops = nodes[assembly].get('children', []) if assembly is not None else []
    out = []
    def dot(base, normal, u, w, radius, k=40):
        """A round sticker 0.12 mm thick lying on a face at `base` (already just proud of it): vertices, faces, rim segments."""
        ring = [base + radius * (np.cos(t) * u + np.sin(t) * w) for t in np.linspace(0, 2 * np.pi, k, endpoint=False)]
        top_ring = [p + normal * 0.12 for p in ring]
        middle = base + normal * 0.12
        if np.dot(np.cross(top_ring[0] - middle, top_ring[1] - middle), normal) < 0:   # (faces outwards whichever way u and w turn)
            top_ring, ring = top_ring[::-1], ring[::-1]
        V = np.array([base + normal * 0.12] + top_ring + ring)
        F = [[0, 1 + j, 1 + (j + 1) % k] for j in range(k)]
        F += [[1 + j, 1 + k + j, 1 + (j + 1) % k] for j in range(k)] + [[1 + (j + 1) % k, 1 + k + j, 1 + k + (j + 1) % k] for j in range(k)]
        rim = np.array([[top_ring[j], top_ring[(j + 1) % k]] for j in range(k)])
        return V, np.array(F), rim

    for spec in specs:
        top = by_name[spec['on']]
        body = instance(top)
        if 'at' in spec:                                  # one dot on the face under a given spot
            normal = np.asarray(spec.get('normal', [0, 1, 0]), float)
            normal /= np.linalg.norm(normal)
            locs, _, _ = body.ray.intersects_location([np.asarray(spec['at'], float) + normal * 30.0], [-normal], multiple_hits=False)
            if not len(locs):
                raise SystemExit(f"stickers: nothing of {spec['on']} under {spec['at']}")
            u = np.cross(normal, [1.0, 0.0, 0.0] if abs(normal[0]) < 0.9 else [0.0, 0.0, 1.0])
            u /= np.linalg.norm(u)
            V, F, rim = dot(locs[0] + normal * 0.06, normal, u, np.cross(normal, u), spec.get('diameter_mm', 7.0) / 2)
            out.append((top, V, F, rim, spec['colour']))
            print(f"  sticker on {spec['on']}: {spec['colour']} at {locs[0].round(2).tolist()}")
            continue
        box = body.bounding_box_oriented
        axes, size, centre = box.primitive.transform[:3, :3], box.primitive.extents, box.primitive.transform[:3, 3]
        lo, hi = body.bounds
        near = [t for t in tops if t != top and (b := box_of(t)) is not None and np.all(b[0] <= hi + 25) and np.all(b[1] >= lo - 25)]
        others = [m for m in (instance(t) for t in near) if m is not None]
        scene = trimesh.util.concatenate([body] + others)
        own = len(body.faces)                            # faces before this index are the part's own
        thin = int(np.argmin(size))
        radius, k, step = spec.get('diameter_mm', 7.0) / 2, 40, 0.4
        across = [a for a in range(3) if a != thin]
        for sign in (1, -1):
            normal = axes[:, thin] * sign
            u, w = axes[:, across[0]], axes[:, across[1]]
            nu, nw = int(size[across[0]] / step) + 1, int(size[across[1]] / step) + 1
            gu = (np.arange(nu) - (nu - 1) / 2) * step
            gw = (np.arange(nw) - (nw - 1) / 2) * step
            grid = centre + normal * (size[thin] / 2 + 40.0) + gu[:, None, None] * u + gw[None, :, None] * w
            origins = grid.reshape(-1, 3)
            locs, ray, tri = scene.ray.intersects_location(origins, np.tile(-normal, (len(origins), 1)), multiple_hits=False)
            depth = np.full(len(origins), -np.inf)
            mine = np.zeros(len(origins), dtype=bool)
            depth[ray] = (locs - centre) @ normal
            mine[ray] = tri < own
            outer = depth[mine].max() if mine.any() else None
            if outer is None:
                raise SystemExit(f"stickers: no face of {spec['on']} found along {normal.round(2).tolist()}")
            shows = (mine & (depth > outer - 0.3)).reshape(nu, nw)      # the face itself, seen square on and not covered
            room = distance_transform_edt(np.pad(shows, 1))[1:-1, 1:-1] * step   # how far each spot is from the face's edge or a cover
            # the spot nearest the middle of what shows that still has room round the dot (a little more than its radius, or the
            # most there is): so the dot is central wherever the face allows it, not at the first spot with the most room
            su, sw = np.nonzero(shows)
            cu, cw = gu[su].mean(), gw[sw].mean()
            ok = np.argwhere(room >= min(room.max(), radius + 1.5) - 1e-9)
            iu, iw = ok[int(np.argmin(np.hypot(gu[ok[:, 0]] - cu, gw[ok[:, 1]] - cw)))]
            if room[iu, iw] < radius:
                print(f"  note: sticker on {spec['on']} has only {room[iu, iw]:.1f} mm of free face round its middle (wants {radius:.1f})")
            base = centre + normal * outer + gu[iu] * u + gw[iw] * w + normal * 0.06   # (just proud of the face, so the two never flicker)
            V, F, rim = dot(base, normal, u, w, radius, k)
            out.append((top, V, F, rim, spec['colour']))
            print(f"  sticker on {spec['on']}: {spec['colour']} at {base.round(1).tolist()} ({room[iu, iw]:.1f} mm of free face round it)")
    return out


# ---------------------------------------------------------------- checks
def world_matrices(doc, to_mm):
    """World matrix (mm) of every node."""
    world = {}

    def visit(i, parent):
        m = node_matrix(doc['nodes'][i])
        m[:3, 3] *= to_mm
        world[i] = parent @ m
        for c in doc['nodes'][i].get('children', []):
            visit(c, world[i])
    for scene in doc['scenes']:
        for root in scene['nodes']:
            visit(root, np.eye(4))
    return world


def wire_breaks(wires):
    """Places where one conductor changes colour between two separately modelled pieces.

    wires: list of (label, colour, world-space vertices). Two pieces that share an end ring (a cable
    continuing a servo's lead stub, say) are the same physical wire and must be the same colour.
    """
    from scipy.spatial import cKDTree
    breaks = []
    trees = [cKDTree(v) for _, _, v in wires]
    for i in range(len(wires)):
        for j in range(i + 1, len(wires)):
            if wires[i][0].split('#')[0] == wires[j][0].split('#')[0]:
                continue                               # two leads of the same cable lie side by side, not end to end
            shared = trees[i].count_neighbors(trees[j], 0.05)
            if shared >= 8 and wires[i][1] != wires[j][1]:
                breaks.append(f"{wires[i][0]} is {wires[i][1]} but continues as {wires[j][0]}, which is {wires[j][1]}")
    return breaks


# ---------------------------------------------------------------- main
def parts_shown(kit_dir):
    """Ids of the parts the kit's guide ever shows, or None if there is no guide yet."""
    steps = kit_dir / 'steps.json'
    if not steps.exists():
        return None
    shown = set()
    for view in json.load(open(steps))['views']:
        shown.update(view.get('visible', []))
    return shown


def build(kit_dir, keep='guide'):
    """keep: 'guide' = only parts shown by the kit's steps.json (all parts if there is none); None = everything; or a set of ids."""
    kit_dir = Path(kit_dir)
    spec = json.load(open(kit_dir / 'materials.json'))
    mats = Materials(spec, kit_dir)
    src = kit_dir / spec.get('source', 'source.glb')
    to_mm = spec.get('source_scale_to_mm', 1000.0)
    doc, blob = read_glb(src)
    if keep == 'guide':
        keep = parts_shown(kit_dir)

    # which nodes survive: a "part" is a child of the assembly node; dropping one drops its whole subtree
    roots = [r for scene in doc['scenes'] for r in scene['nodes']]
    assembly = roots[0] if len(roots) == 1 and 'mesh' not in doc['nodes'][roots[0]] else None
    if (spec.get('extra_parts') or spec.get('own_parts')) and assembly is None:
        raise SystemExit(f'materials.json extra_parts / own_parts need a CAD export with one assembly node; {src.name} has {len(roots)} scene roots')
    if spec.get('extra_parts') and assembly is not None:
        doc, blob = add_extra_parts(doc, blob, kit_dir, spec['extra_parts'], assembly, to_mm)
    if spec.get('own_parts') and assembly is not None:
        doc = promote(doc, spec['own_parts'], assembly)
    nodes = doc['nodes']
    dropped = set()
    if keep is not None and assembly is not None:
        def drop(i):
            dropped.add(i)
            for c in nodes[i].get('children', []):
                drop(c)
        for child in nodes[assembly].get('children', []):
            if nodes[child].get('name') not in keep:
                drop(child)
        missing = set(keep) - {nodes[c].get('name') for c in nodes[assembly].get('children', [])}
        if missing:
            raise SystemExit(f'steps.json shows parts that are not in {src.name}: {sorted(missing)}')
    kept_nodes = [i for i in range(len(nodes)) if i not in dropped]
    used_meshes = sorted({nodes[i]['mesh'] for i in kept_nodes if 'mesh' in nodes[i]})

    writer = GlbWriter(compress=True)
    material_index, materials_json = {}, []

    def material(name):
        if name not in material_index:
            hexcode = mats.palette.get(name, name)
            if not re.fullmatch(r'#[0-9a-fA-F]{6}', hexcode or ''):
                raise SystemExit(f'materials.json: "{name}" is neither a palette entry nor a #rrggbb colour')
            material_index[name] = len(materials_json)
            materials_json.append(dict(name=name, pbrMetallicRoughness=dict(baseColorFactor=srgb_to_linear(hexcode) + [1.0], metallicFactor=0.0, roughnessFactor=1.0)))
        return material_index[name]

    edge_material = material('edge')
    adjust = spec.get('adjust_mm', {})               # parts the CAD has out of place: instance id -> [x, y, z] to move it by, or a pose to turn it
    meshes_json, dequant, report, new_mesh_index, lead_solids = [], {}, [], {}, {}
    first_like, same_as, omitted = {}, {}, set()      # identical geometry under the same name is built once and shared
    # "move_engraving": {instance id: {"by": [x, y, z] mm in assembly space, "turn": 180}}: the engraved code of that part goes
    # elsewhere on its face (the real part is engraved there), turned half round on the face if "turn" says so. Turned into
    # the mesh's own frame, which is where the faces are worked on.
    moves, world0 = {}, world_matrices(doc, to_mm)
    by_name = {n.get('name'): i for i, n in enumerate(nodes)}
    for inst, how in spec.get('move_engraving', {}).items():
        how = how if isinstance(how, dict) else {'by': how}
        i = by_name[inst]
        R = pose_matrix(adjust[inst])[:3, :3] @ world0[i][:3, :3] if inst in adjust else world0[i][:3, :3]
        moves[nodes[i]['mesh']] = (R.T @ np.asarray(how['by'], float), float(how.get('turn', 0)))
    for mi in used_meshes:
        mesh = doc['meshes'][mi]
        if len(mesh['primitives']) != 1 or mesh['primitives'][0].get('mode', 4) != 4:
            raise SystemExit(f"{mesh['name']}: expected one triangle primitive per mesh, found {len(mesh['primitives'])}")
        prim = mesh['primitives'][0]
        rule = mats.rule_for(mesh['name'])
        if rule.get('omit'):                          # e.g. a CAD cable that the guide draws as a live wire instead
            omitted.add(mi)
            continue
        raw = [accessor(doc, blob, prim['attributes']['POSITION']), accessor(doc, blob, prim['attributes']['NORMAL']), accessor(doc, blob, prim['indices'])]
        key = (mesh['name'], hashlib.md5(b''.join(np.ascontiguousarray(a).tobytes() for a in raw)).hexdigest(), mi if mi in moves else None)
        if key in first_like:
            same_as[mi] = first_like[key]
            report[new_mesh_index[first_like[key]]]['used_by'] += 1
            continue
        first_like[key] = same_as[mi] = mi
        V = raw[0].astype(np.float64) * to_mm
        N = raw[1].astype(np.float64).copy()
        F = raw[2].reshape(-1, 3).astype(np.int64)
        for region in rule.get('regions', []):        # a region with "cut": its box's faces cut the triangles that cross them first
            if region.get('cut'):
                for axis in range(3):
                    for value in np.asarray(region['box'], float)[:, axis]:
                        if V[:, axis].min() < value < V[:, axis].max():
                            V, N, F = cut_faces(V, N, F, axis, value)

        Vp, remap = weld_positions(V)
        Fp = remap[F]
        n_comp, labels = split_components(len(Vp), Fp)
        if 'components' in rule or 'atlas' in rule:
            comp_colour, note, skin = colour_components(rule, mats, Vp, Fp, labels, n_comp)
        else:
            comp_colour, note, skin = [rule.get('color')] * n_comp, '', np.zeros(n_comp, dtype=bool)
        if any('across' in c for c in rule.get('components', [])):   # remember each lead for the continuity check
            lead_solids[mi] = [(c, comp_colour[c], Vp[labels == c]) for c in range(n_comp) if str(comp_colour[c]).startswith('wire_')]
        face_comp = labels[Fp[:, 0]]
        face_colour = np.array([comp_colour[c] for c in face_comp], dtype=object)
        if skin.any():                                # the body under a skin takes the skin's colour (see faces_under_skin)
            recoloured = 0
            for colour in sorted({str(comp_colour[c]) for c in np.flatnonzero(skin)}):
                group = skin & np.array([str(c) == colour for c in comp_colour])
                under = faces_under_skin(Vp, Fp, face_comp, group, never=skin)
                face_colour[under] = colour
                recoloured += int(under.sum())
            if recoloured:
                note = (note + '; ' if note else '') + f'{recoloured} faces under a skin recoloured'
        for region in rule.get('regions', []):        # faces whose middle lies in a box (mm, the mesh's own frame): one solid in two colours (see cut_faces for "cut")
            lo, hi = np.asarray(region['box'], float)
            middle = Vp[Fp].mean(axis=1)
            face_colour[np.all((middle >= lo) & (middle <= hi), axis=1)] = region['color']
        if rule.get('engraving') and mi in moves:      # the code moved: its pocket filled in flush, the code drawn as a decal elsewhere
            V, N, F, face_colour = move_engraving(V, N, F, Vp, Fp, face_colour, *moves[mi], rule['engraving'])
        elif rule.get('engraving'):
            face_colour[engraved_faces(Vp, Fp)] = rule['engraving']
        if 'atlas' in rule:                           # print on a face (a servo's label)
            for colour, faces in flat_marks(V, F, mats.atlas(rule['atlas'])).items():
                face_colour[faces] = rule.get('atlas_colours', {}).get(colour, colour)
        # "roughen_mm": a laser-cut plate's edges, slots, holes and engraving shifted by about that much in its plane (see
        # roughen), so that a cutting file traced from the published model comes out slightly wrong. After the engraving is moved and before the
        # crease lines are drawn, so the lines follow the moved faces.
        if rule.get('roughen_mm'):
            V, eased, left = roughen(V, F, rule['roughen_mm'], mesh['name'])
            note = (note + '; ' if note else '') + f"edges roughened by up to {rule['roughen_mm']} mm" + (f' ({eased} sliver corners eased)' if eased else '')
            if left:
                print(f"  WARNING {mesh['name']}: {left} faces turned over by roughen_mm")

        # quantization grid for this mesh (shared by its triangles and edges)
        lo = V.min(0)
        step = max((V.max(0) - lo).max() / 65535.0, 1e-6)
        quant = lambda P: np.round((P - lo) / step).astype(np.uint16)

        prims, tris_out, edge_chunks, worst_tolerance = [], 0, [], 0.0
        for name in sorted(set(face_colour), key=str):
            sel = face_colour == name
            f, v, n = compact(F[sel], V, N)
            if rule.get('smooth'):                    # tubes and cables: weld by position, rebuild smooth normals
                v, remap = weld_positions(v, rule.get('weld_mm', 0.02))
                f = drop_degenerate(remap[f])
                if not len(f):
                    continue
                f, v = compact(f, v)
                n = smooth_normals(v, f)
            else:
                v, n, f = weld_attributes(v, n, f)
                f = drop_degenerate(f)
            f_full = f
            f, used_tolerance = simplify_to_budget(v, n, f, rule.get('simplify_mm', 0.0), rule.get('max_tris'), rule.get('normal_weight', 0.4))
            worst_tolerance = max(worst_tolerance, used_tolerance)
            if not len(f):
                continue
            # Crease edges normally come from the simplified surface, so the lines sit exactly on it. "edges_from": "source"
            # takes them from the full-detail surface instead, for small parts whose creases the simplifier rounds off
            # ("edge_min_spacing_mm" then leaves out a modelled thread: see thin_out_edges).
            edge_v, edge_n, edge_f = (v, n, f_full) if rule.get('edges_from') == 'source' else (None, None, None)
            f, v, n = compact(f, v, n)
            if edge_v is None:
                edge_v, edge_n, edge_f = v, n, f

            if rule.get('edges', True) and name != rule.get('engraving'):
                vp, remap = weld_positions(edge_v)
                fp = remap[edge_f]
                sound = (fp[:, 0] != fp[:, 1]) & (fp[:, 1] != fp[:, 2]) & (fp[:, 0] != fp[:, 2])
                fp, corner_normals = fp[sound], edge_n[edge_f[sound]]
                if len(fp):
                    min_size = rule.get('edge_min_size_mm', 0.0)
                    if min_size > 0:
                        nc, lab = split_components(len(vp), fp)
                        span = np.zeros(nc)
                        for c in range(nc):
                            span[c] = np.ptp(vp[lab == c], axis=0).max()
                        big = span[lab[fp[:, 0]]] >= min_size
                        fp, corner_normals = fp[big], corner_normals[big]
                    e = feature_edges(vp, fp, rule.get('edge_angle', 30))
                    if rule.get('fillet_edges_mm', 0.0) > 0:      # rounded corners get a line too (see fillet_edges)
                        e = np.vstack([e, fillet_edges(vp, fp, corner_normals, rule.get('edge_angle', 30), rule['fillet_edges_mm'])])
                    e = thin_out_edges(vp, e, rule.get('edge_min_spacing_mm', 0.0))
                    if len(e):
                        edge_chunks.append(vp[e])     # (m, 2, 3) segment endpoints in mm

            order = np.zeros(f.size, dtype=np.uint32)
            mo.optimize_vertex_cache(order, np.ascontiguousarray(f.reshape(-1).astype(np.uint32)), f.size, len(v))
            f = order.reshape(-1, 3)
            pos = np.zeros((len(v), 4), dtype=np.uint16)
            pos[:, :3] = quant(v)
            nrm = np.zeros((len(n), 4), dtype=np.int8)
            nrm[:, :3] = np.clip(np.round(n * 127), -127, 127)
            prims.append(dict(attributes=dict(POSITION=writer.add_vertices(pos, 'VEC3', with_bounds=True), NORMAL=writer.add_vertices(nrm, 'VEC3', normalized=True)),
                              indices=writer.add_indices(f), material=material(name), mode=4))
            tris_out += len(f)

        edges = np.zeros((0, 2), dtype=np.int64)
        if edge_chunks:
            seg = np.concatenate(edge_chunks)
            ev, remap = weld_positions(seg.reshape(-1, 3))
            edges = remap.reshape(-1, 2)
            edges = edges[edges[:, 0] != edges[:, 1]]
            pos = np.zeros((len(ev), 4), dtype=np.uint16)
            pos[:, :3] = quant(ev)
            prims.append(dict(attributes=dict(POSITION=writer.add_vertices(pos, 'VEC3', with_bounds=True)), indices=writer.add_indices(edges, triangles=False), material=edge_material, mode=1))

        entry = dict(name=mesh['name'], primitives=prims)
        if rule.get('outline'):
            entry['extras'] = dict(outline=True)     # smooth part with no crease edges: the player draws a silhouette instead
        new_mesh_index[mi] = len(meshes_json)
        meshes_json.append(entry)
        dequant[mi] = (lo, step)
        row = dict(mesh=mesh['name'], used_by=1, solids=int(n_comp), tris_in=int(len(F)), tris_out=int(tris_out), edge_segments=int(len(edges)),
                   colours=sorted({str(c) for c in face_colour}), note=note)
        if worst_tolerance > rule.get('simplify_mm', 0.0) + 1e-9:
            row['tolerance_relaxed_to_mm'] = round(worst_tolerance, 3)
        if mi in lead_solids:
            row['lead_order'] = [str(comp_colour[c]) for c in order_leads(Vp, labels, np.array([c for c, _, _ in lead_solids[mi]]))]
        report.append(row)

    # "decals": printing laid on a part (a circuit board's silkscreen), as data for the player to draw: {instance id: [decal,
    # ...]} or the name of a JSON file in the kit that holds that (see js/core.js, addDecal). Seated assembly mm.
    decals = spec.get('decals') or {}
    if isinstance(decals, str):
        decals = json.load(open(kit_dir / decals))
    # nodes: same names and hierarchy; mesh nodes get the de-quantization baked into their matrix
    new_node_index = {old: new for new, old in enumerate(kept_nodes)}
    parent_of = {c: k for k, n in enumerate(nodes) for c in n.get('children', [])}
    nodes_json = []
    for i in kept_nodes:
        node = nodes[i]
        out = {'name': node['name']} if 'name' in node else {}
        if node.get('name') in decals and not node['name'].startswith('_'):
            out['extras'] = dict(decals=decals[node['name']])
        children = [new_node_index[c] for c in node.get('children', []) if c in new_node_index]
        if children:
            out['children'] = children
        m = node_matrix(node)
        m[:3, 3] *= to_mm
        if node.get('name') in adjust:
            move = pose_matrix(adjust[node['name']])
            up = parent_of.get(i)
            if up is not None and up != assembly:    # a piece inside a part (a socket on a board): the move is in assembly mm all the same
                move = np.linalg.inv(world0[up]) @ move @ world0[up]
            m = move @ m
        if 'mesh' in node and node['mesh'] not in omitted:
            out['mesh'] = new_mesh_index[same_as[node['mesh']]]
            lo, step = dequant[same_as[node['mesh']]]
            q = np.eye(4)
            q[:3, :3] *= step
            q[:3, 3] = lo
            m = m @ q
        if not np.allclose(m, np.eye(4)):
            out['matrix'] = m.T.reshape(-1).tolist()
        nodes_json.append(out)
    # stickers the kit adds: each a small mesh of its own, hung under its part's node (so it moves with the part)
    world = world_matrices(doc, to_mm)
    for top, V, F, rim, colour in stickers(doc, blob, spec.get('stickers', []), to_mm, world, adjust, assembly):
        if top not in new_node_index:
            continue
        inverse = np.linalg.inv(world[top])                          # (in the part's own frame, before any adjust_mm)
        V = V @ inverse[:3, :3].T + inverse[:3, 3]
        rim = rim.reshape(-1, 3) @ inverse[:3, :3].T + inverse[:3, 3]
        lo, step = V.min(0), max(np.ptp(V, axis=0).max() / 65535.0, 1e-6)
        quant = lambda P: np.round((P - lo) / step).astype(np.uint16)
        pos, ring = np.zeros((len(V), 4), dtype=np.uint16), np.zeros((len(rim), 4), dtype=np.uint16)
        pos[:, :3], ring[:, :3] = quant(V), quant(rim)
        n = np.zeros((len(V), 4), dtype=np.int8)
        n[:, :3] = np.clip(np.round(np.cross(V[F[0][1]] - V[F[0][0]], V[F[0][2]] - V[F[0][0]]) / np.linalg.norm(np.cross(V[F[0][1]] - V[F[0][0]], V[F[0][2]] - V[F[0][0]])) * 127), -127, 127)
        prims = [dict(attributes=dict(POSITION=writer.add_vertices(pos, 'VEC3', with_bounds=True), NORMAL=writer.add_vertices(n, 'VEC3', normalized=True)),
                      indices=writer.add_indices(F.astype(np.uint32)), material=material(colour), mode=4),
                 dict(attributes=dict(POSITION=writer.add_vertices(ring, 'VEC3', with_bounds=True)), indices=writer.add_indices(np.arange(len(rim), dtype=np.uint32).reshape(-1, 2), triangles=False),
                      material=edge_material, mode=1)]
        meshes_json.append(dict(name=f"sticker {colour}", primitives=prims))
        q = np.eye(4)
        q[:3, :3] *= step
        q[:3, 3] = lo
        if 'mesh' in nodes[top] and nodes[top]['mesh'] not in omitted:   # the part's node has its own mesh's de-quantization in its matrix
            p_lo, p_step = dequant[same_as[nodes[top]['mesh']]]
            pq = np.eye(4)
            pq[:3, :3] *= p_step
            pq[:3, 3] = p_lo
            q = np.linalg.inv(pq) @ q
        nodes_json.append(dict(name=f"{nodes[top].get('name')} sticker", mesh=len(meshes_json) - 1, matrix=q.T.reshape(-1).tolist()))
        nodes_json[new_node_index[top]].setdefault('children', []).append(len(nodes_json) - 1)
        report.append(dict(mesh=f"sticker {colour} on {nodes[top].get('name')}", used_by=1, solids=1, tris_in=0, tris_out=len(F), edge_segments=len(rim) // 2, colours=[colour], note='added by the kit'))
    scenes_json = [dict(scene, nodes=[new_node_index[r] for r in scene['nodes'] if r in new_node_index]) for scene in doc['scenes']]

    out_doc = dict(asset=dict(version='2.0', generator='TechBox build_model.py'), scene=doc.get('scene', 0), scenes=scenes_json,
                   nodes=nodes_json, meshes=meshes_json, materials=materials_json)
    size = writer.write(kit_dir / 'model.glb', out_doc)

    # one conductor, one colour: a cable must match the lead stub or pigtail it continues
    wires = []
    for i in kept_nodes:
        mi = same_as.get(nodes[i].get('mesh'))
        for c, colour, pts in lead_solids.get(mi, []):
            wires.append((f"{nodes[i].get('name')}#{c} ({doc['meshes'][mi]['name']})", colour, pts @ world[i][:3, :3].T + world[i][:3, 3]))
    breaks = wire_breaks(wires)

    drawn = [report[new_mesh_index[same_as[nodes[i]['mesh']]]] for i in kept_nodes if nodes[i].get('mesh') in same_as]
    inst_in = sum(r['tris_in'] for r in drawn)
    inst_out = sum(r['tris_out'] for r in drawn)
    all_parts = len(nodes[assembly].get('children', [])) if assembly is not None else None
    summary = dict(source=src.name, source_bytes=src.stat().st_size, model_bytes=size, triangles_in=inst_in, triangles_out=inst_out,
                   edge_segments=sum(r['edge_segments'] for r in drawn), meshes=len(report), parts_kept=None if keep is None else len(keep), parts_in_source=all_parts,
                   materials=[m['name'] for m in materials_json], wire_colour_breaks=breaks)
    json.dump(dict(summary=summary, meshes=report), open(kit_dir / 'model.report.json', 'w'), indent=1)

    # point the guide at the new file, so browsers that cached the old model fetch this one
    steps = kit_dir / 'steps.json'
    if steps.exists():
        data = json.load(open(steps))
        data['model'] = f"model.glb?v={int((kit_dir / 'model.glb').stat().st_mtime)}"
        json.dump(data, open(steps, 'w'), indent=1)

    scope = f"{len(keep)} of {all_parts} parts (those the guide shows)" if keep is not None else 'all parts'
    print(f"{src.name}: {summary['source_bytes'] / 1e6:.1f} MB  ->  model.glb: {size / 1e6:.2f} MB, {inst_out:,} triangles ({inst_in:,} in the source for the same parts), {scope}")
    for r in sorted(report, key=lambda r: -r['tris_out'] * r['used_by'])[:12]:
        relaxed = f"  (detail relaxed to {r['tolerance_relaxed_to_mm']} mm to meet max_tris)" if 'tolerance_relaxed_to_mm' in r else ''
        print(f"  {r['mesh'][:40]:40s} x{r['used_by']:<2} {r['tris_in']:>8,} -> {r['tris_out']:>7,} tris  {r['solids']:>4} solids  {', '.join(r['colours'])[:60]}  {r['note']}{relaxed}")
    for b in breaks:
        print('  WARNING wire colour changes along one conductor:', b)
    return summary


if __name__ == '__main__':
    if len(sys.argv) not in (2, 3) or (len(sys.argv) == 3 and sys.argv[2] != '--all'):
        raise SystemExit(__doc__ + '\nAdd --all to keep every part of the CAD, not just the ones the guide shows.')
    build(sys.argv[1], keep=None if len(sys.argv) == 3 else 'guide')
