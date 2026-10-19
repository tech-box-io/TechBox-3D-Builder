"""Critic: poses nobody wrote down yet (header only: node matrices and accessor boxes; no vertices are read).

1. The published way up of the I/O module on H4 (Cadasio Ensamblaje_Shield_NANO-2 / -3) as poses of the STEP's NAUO78, exact from the
   two projects' matrices; the MRA -> published transform (the NANO extra part's pose if the published way up is chosen).
2. Where the 8 caps the STEP lacks would sit (V4 - V7 on the built module, both ways up; GND on each built button), from the caps
   the STEP has.
"""
import json, sys
import numpy as np
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from pmglib import Glb
ROOT = '/Users/lee-johnson/Desktop/Claude_Cadasio'
g = Glb(ROOT + '/PMG Build Instructions/pmg.glb')
tree = json.load(open(ROOT + '/docs/research/pmg/scripts/work/cadasio_map/cadasio_tree.json'))['tops']
cad = {c['name']: np.array(c['matrix_mm']) for c in tree}

def top_matrix(name):
    from glbio import node_matrix
    M = g.root_M @ node_matrix(g.nodes[g.top[name]])
    M = M.copy(); M[:3, 3] *= 1000.0
    return M

def axis_angle(R):
    ang = np.degrees(np.arccos(np.clip((np.trace(R) - 1) / 2, -1, 1)))
    if ang < 1e-6:
        return [1.0, 0.0, 0.0], 0.0
    if abs(ang - 180) < 1e-4:
        B = (R + np.eye(3)) / 2; ax = np.sqrt(np.clip(np.diag(B), 0, None))
        i = int(np.argmax(ax)); ax = B[i] / np.sqrt(B[i, i])
    else:
        ax = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]]); ax /= np.linalg.norm(ax)
    return ax.round(6).tolist(), round(float(ang), 4)

def as_pose(M, at):
    """stepgen / materials pose {"t", "r", "at"} for the 4x4 M (mm), turned about `at`."""
    R = M[:3, :3]; ax, ang = axis_angle(R)
    at = np.asarray(at, float)
    t = M[:3, 3] - (at - R @ at)
    return {'t': np.round(t, 3).tolist(), 'r': ax + [ang], 'at': np.round(at, 3).tolist()}

def rot(ax, deg):
    a = np.asarray(ax, float); a /= np.linalg.norm(a); th = np.radians(deg)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(th) * K + (1 - np.cos(th)) * K @ K

def check(pose, M):
    R = rot(pose['r'][:3], pose['r'][3]) if pose['r'][3] else np.eye(3)
    at = np.array(pose['at']); t = np.array(pose['t'])
    return float(np.abs(R - M[:3, :3]).max()), float(np.abs(at - R @ at + t - M[:3, 3]).max())

M78, M94 = top_matrix('NAUO78'), top_matrix('NAUO94')
print('NAUO78', M78.round(4).tolist())
print('Cadasio -2', cad['Ensamblaje_Shield_NANO-2'].tolist())
for label, Mstep, cname in (('built', M78, 'Ensamblaje_Shield_NANO-2'), ('held', M94, 'Ensamblaje_Shield_NANO-3')):
    D = cad[cname] @ np.linalg.inv(Mstep)          # STEP copy -> published copy
    p = as_pose(D, [605.78, 932.5, 1290.47])
    # the line it turns about (180 deg about X): y0 = t_y / 2, z0 = t_z / 2
    print(f'published {label} module from the STEP\'s {label} copy:', p, 'check', check(p, D), ' turn line y0 %.3f z0 %.3f' % (D[1, 3] / 2, D[2, 3] / 2))
    if label == 'built':
        D_built = D
# published held as a pose of the STEP's BUILT copy (what the guide needs: one module part, built = NAUO78 turned)
D_held_from_built = cad['Ensamblaje_Shield_NANO-3'] @ np.linalg.inv(cad['Ensamblaje_Shield_NANO-2'])
print('published held, from the published built:', as_pose(D_held_from_built, [605.78, 930.6, 1290.6]))

# MRA module -> PMG NAUO78 (reuse_plan 2.1) and -> the published way up
R_mra = np.array([[0, 1, 0], [0, 0, -1], [-1, 0, 0]], float); t_mra = np.array([490.546, 1077.982, 1360.501])
A = np.eye(4); A[:3, :3] = R_mra; A[:3, 3] = t_mra
P = D_built @ A
pp = as_pose(P, [0, 0, 0])
print('MRA -> published built (NANO extra_parts pose if turned):', pp, 'check', check(pp, P))
print('  i.e. x\' = %s' % (P[:3, :3].round(6).tolist()), '+', P[:3, 3].round(3).tolist())

# 2. caps
def cap_centre_axis(name):
    M = top_matrix(name)
    mesh = [m for i, nm, m, W in g.mesh_nodes(name)]
    nodes = g.mesh_nodes(name)
    lo, hi = [], []
    for i, nm, m, W in nodes:
        for pr in g.meshes[m]['primitives']:
            a = g.doc['accessors'][pr['attributes']['POSITION']]
            c = np.array([[x, y, z] for x in (a['min'][0], a['max'][0]) for y in (a['min'][1], a['max'][1]) for z in (a['min'][2], a['max'][2])])
            w = (c @ W[:3, :3].T + W[:3, 3]) * 1000.0
            lo.append(w.min(0)); hi.append(w.max(0))
    lo, hi = np.min(lo, 0), np.max(hi, 0)
    return (lo + hi) / 2, hi - lo, M

caps = {}
for n in ['NAUO97', 'NAUO96', 'NAUO95', 'NAUO99', 'NAUO98', 'NAUO100', 'NAUO102', 'NAUO101', 'NAUO113', 'NAUO114',
          'NAUO86', 'NAUO87', 'NAUO88', 'NAUO89', 'NAUO90', 'NAUO91', 'NAUO92', 'NAUO93',
          'NAUO106', 'NAUO109', 'NAUO105', 'NAUO103', 'NAUO130', 'NAUO131', 'NAUO132', 'NAUO133']:
    caps[n] = cap_centre_axis(n)
    c, s, _ = caps[n]
    print(f'  cap {n}: centre {c.round(2).tolist()} size {s.round(2).tolist()}')
# V column = G column + (V - G) (module pins: G z 1310.42, V 1307.93 built: the V9 / G9 caps give it exactly)
dVG = caps['NAUO113'][0] - caps['NAUO114'][0]
print('V9 - G9 caps (the V - G step on the built module):', dVG.round(3).tolist())
for row, gcap in (('4', 'NAUO97'), ('5', 'NAUO95'), ('6', 'NAUO98'), ('7', 'NAUO102')):
    c = caps[gcap][0] + dVG
    cpub = D_built[:3, :3] @ c + D_built[:3, 3]
    print(f'  V{row} cap centre: STEP way up {c.round(2).tolist()} | published way up {cpub.round(2).tolist()}  (from G{row} cap {gcap})')
for b, (vcc, out) in {'black': ('NAUO86', 'NAUO87'), 'yellow': ('NAUO88', 'NAUO89'), 'white': ('NAUO90', 'NAUO91'), 'blue': ('NAUO93', 'NAUO92')}.items():
    step = caps[out][0] - caps[vcc][0]
    print(f'  {b} button GND cap centre (built): {(caps[out][0] + step).round(2).tolist()}  (OUT cap {out} + (OUT - VCC) {step.round(3).tolist()})')
# a spare cap moved onto a new place: the pose that carries it there (same orientation as the cap it copies)
def move_onto(spare, like, shift):
    Ms = caps[spare][2]; Ml = caps[like][2].copy(); Ml[:3, 3] += shift
    D = Ml @ np.linalg.inv(Ms)
    return as_pose(D, caps[spare][0])
print('  e.g. adjust_mm for spare NAUO106 (held G4) onto V4 (STEP way up):', move_onto('NAUO106', 'NAUO97', dVG))
print('  e.g. adjust_mm for spare NAUO130 (display-aside CLK) onto the black button GND:',
      move_onto('NAUO130', 'NAUO87', caps['NAUO87'][0] - caps['NAUO86'][0]))

# 3. If the published way up is chosen: the bench / held poses re-expressed from the TURNED built copies (pose_new = pose_old . D^-1)
rp = {grp['built']: grp for grp in json.load(open(ROOT + '/docs/research/pmg/reuse_poses.json'))['groups']}
def pmat(pose):
    M = np.eye(4)
    if isinstance(pose, dict):
        R = rot(pose['r'][:3], pose['r'][3]) if pose['r'][3] else np.eye(3)
        at = np.array(pose['at']); M[:3, :3] = R; M[:3, 3] = at - R @ at + np.array(pose['t'])
    else:
        M[:3, 3] = pose
    return M
Dinv = np.linalg.inv(D_built)
print('\nIf the module goes on H4 the published way up (built copies turned by D, 180 deg about the X line y 931.545, z 1290.510):')
for built, label in (('NAUO78', 'I/O module'), ('NANO (extra part)', 'Nano'), ('NAUO282', 'USB Mini-B plug')):
    grp = rp[built]
    at_new = (D_built @ np.r_[grp['at'], 1.0])[:3]
    for c in grp['copies']:
        Mn = pmat(c['pose']) @ Dinv
        p = as_pose(Mn, at_new)
        if p['r'][3] == 0:
            p = p['t']
        print(f'  {label}: {c["instance"]} ({c["where"]}) from the turned built copy: {p}')
    if built == 'NANO (extra part)':
        seat = pmat(grp['copies'][0]['pose']); seat[1, 3] -= 44.9          # NAUO2's place less 44.9 mm = the true bench seat
        print('  Nano: bench seat (NAUO2 - 44.9 Y) from the turned built copy:', as_pose(seat @ Dinv, at_new))
print('  module held above H4 (Cadasio -3) from the turned built copy: [0.0, 102.33, 0.159]')
