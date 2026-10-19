"""PMG reuse study: is a PMG part the same CAD model, placed the same way inside, as the MRA's / RCC's? (GLB headers only.)

    .venv.nosync/bin/python docs/research/pmg/scripts/reuse_compare.py

For two instances that should hold the same model, one rigid transform T (assembly mm) is taken from one mesh node both have
once (the board), and every mesh node of the first is carried by T onto the second's nodes of the same name: the error is how
far the carried own-frame box corners land from the nearest same-named node's box corners (mm). Prints T as a matrix, as
a rotation (axis, degrees) and as an extra_parts / adjust_mm style pose.
"""
import collections
import sys

import numpy as np

sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from reuse_hdr import Glb  # noqa: E402

ROOT = '/Users/lee-johnson/Desktop/Claude_Cadasio/'
PMG = Glb(ROOT + 'PMG Build Instructions/pmg.glb')
MRA = Glb(ROOT + 'MRA Build Instructions Prototype/mra.glb')
RCC = Glb(ROOT + 'RCC Build Instructions/rcc.glb')
np.set_printoptions(suppress=True, precision=4)


def corners(lo, hi):
    return np.array([[x, y, z, 1.0] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])


def placed(row, T=np.eye(4)):
    _, _, lo, hi, _, W = row
    return (corners(lo, hi) @ (T @ W).T)[:, :3]


def axis_angle(R):
    a = np.degrees(np.arccos(np.clip((np.trace(R) - 1) / 2, -1, 1)))
    if a < 1e-6:
        return [0, 0, 1], 0.0
    if abs(a - 180) < 1e-3:
        w, v = np.linalg.eigh((R + np.eye(3)) / 2)
        ax = v[:, np.argmax(w)]
    else:
        ax = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]])
    ax = ax / np.linalg.norm(ax)
    return [round(float(c), 5) for c in ax], round(float(a), 4)


def mesh_rows(H, inst, skip=()):
    i = H.find(inst)
    assert len(i) == 1, (inst, i)
    rows = H.mesh_nodes(i[0])
    if skip:
        drop = set()
        for k in H.subtree(i[0]):
            if H.nodes[k].get('name') in skip:
                drop.update(H.subtree(k))
        rows = [r for r in rows if r[0] not in drop]
    return rows


def compare(A, a_inst, B, b_inst, anchor, a_skip=(), b_skip=(), quiet=False):
    """Carry A's instance onto B's by the transform that maps A's `anchor` mesh node onto B's. Returns T and the errors."""
    ra, rb = mesh_rows(A, a_inst, a_skip), mesh_rows(B, b_inst, b_skip)
    wa = [r for r in ra if r[1] == anchor]
    wb = [r for r in rb if r[1] == anchor]
    assert len(wa) == 1 and len(wb) == 1, (anchor, len(wa), len(wb))
    T = wb[0][5] @ np.linalg.inv(wa[0][5])
    byname = collections.defaultdict(list)
    for r in rb:
        byname[r[1]].append(r)
    worst, missing, used = 0.0, [], set()
    for r in ra:
        cands = byname.get(r[1], [])
        if not cands:
            missing.append(r[1])
            continue
        P = placed(r, T)
        errs = [np.abs(P - placed(c)).max() for c in cands]
        k = int(np.argmin(errs))
        used.add(cands[k][0])
        worst = max(worst, errs[k])
        if errs[k] > 0.05 and not quiet:
            print(f'     {r[1]}: off by {errs[k]:.3f} mm')
    extra = collections.Counter(r[1] for r in rb if r[0] not in used)
    print(f'  {a_inst} ({len(ra)} meshes) -> {b_inst} ({len(rb)} meshes): worst {worst:.4f} mm; in A only: {collections.Counter(missing)}; in B not matched: {dict(extra)}')
    R = T[:3, :3]
    print('     T rotation', np.round(R, 5).tolist(), 'axis/deg', axis_angle(R), 't', np.round(T[:3, 3], 3).tolist())
    return T, worst


print('== assembly chain of pmg.glb (scene root down to the assembly node)')
r = PMG.doc['scenes'][PMG.doc.get('scene', 0)]['nodes'][0]
a = PMG.assembly()
k = a
while k is not None:
    print('  ', PMG.nodes[k].get('name'), 'local matrix identity:', np.allclose(PMG.world(k), np.eye(4)) if k == r else None,
          {kk: v for kk, v in PMG.nodes[k].items() if kk in ('matrix', 'translation', 'rotation', 'scale')})
    k = PMG.parent.get(k)
print('   world(assembly) =', np.round(PMG.world(a), 6).tolist())

print('\n== I/O module (shield only): MRA NAUO82 without its Nano (NAUO126) onto each PMG copy')
T_mra = {}
for inst in ('NAUO78', 'NAUO1', 'NAUO94'):
    inner = {'NAUO1': ('NAUO387',), 'NAUO78': ('NAUO301',), 'NAUO94': ('NAUO301',)}[inst]
    T_mra[inst], _ = compare(MRA, 'NAUO82', PMG, inst, 'Shield_Arduino NANO', a_skip=('NAUO126',), b_skip=inner)

print('\n== the inner plain Nano: RCC NAUO23 (shield + its Nano NAUO86) onto PMG NAUO78 (shield + NAUO301), all meshes')
compare(RCC, 'NAUO23', PMG, 'NAUO78', 'Shield_Arduino NANO')

print('\n== the three PMG module copies against each other (all meshes, inner Nano included)')
T_1_78, _ = compare(PMG, 'NAUO1', PMG, 'NAUO78', 'Shield_Arduino NANO', quiet=True)
T_78_94, _ = compare(PMG, 'NAUO78', PMG, 'NAUO94', 'Shield_Arduino NANO', quiet=True)

print('\n== the Nano: MRA NAUO126 (nano_Varsayilan) against PMG NAUO2 / NAUO3')
mra_nano = MRA.mesh_nodes(MRA.find('NAUO126')[0])
for inst in ('NAUO2', 'NAUO3'):
    rows = PMG.mesh_nodes(PMG.find(inst)[0])
    (_, n, lo, hi, cnt, W), = rows
    (_, n0, lo0, hi0, cnt0, W0), = mra_nano
    top = PMG.world(PMG.find(inst)[0]).copy(); top[:3, 3] *= 1000
    top0 = MRA.world(MRA.find('NAUO126')[0]).copy(); top0[:3, 3] *= 1000
    print(f'  {inst}: mesh {n!r} {cnt} verts, own box {np.round(lo, 3).tolist()} .. {np.round(hi, 3).tolist()}')
    print(f'     MRA: mesh {n0!r} {cnt0} verts, own box {np.round(lo0, 3).tolist()} .. {np.round(hi0, 3).tolist()}')
    print('     mesh node inside its part, PMG vs MRA (same?):', np.allclose(np.linalg.inv(top) @ W, np.linalg.inv(top0) @ W0, atol=1e-6),
          'world centre', np.round(placed(rows[0]).mean(0), 2).tolist())
# where NAUO3 (seated on NAUO1) sits relative to NAUO1's shield, and the same seat on NAUO78
(_, _, lo3, hi3, _, W3), = PMG.mesh_nodes(PMG.find('NAUO3')[0])
seat78 = T_1_78 @ W3
print('  the Nano seat on NAUO78 = T(NAUO1 -> NAUO78) . W(NAUO3): box', np.round(placed((0, 0, lo3, hi3, 0, seat78)).min(0), 2).tolist(),
      '..', np.round(placed((0, 0, lo3, hi3, 0, seat78)).max(0), 2).tolist())
print('     as a pose for extra_parts (moves the cut part from NAUO3\'s place to there): rotation axis/deg', axis_angle(T_1_78[:3, :3]),
      't', np.round(T_1_78[:3, 3], 3).tolist())
# the MRA's Nano in its module, carried by T_mra: does it land where NAUO3 does relative to its module (NAUO1)?
(_, _, loM, hiM, _, WM), = mra_nano
pred = T_mra['NAUO1'] @ WM
print('  MRA Nano carried onto PMG NAUO1 by the shield transform vs PMG NAUO3: worst corner',
      round(float(np.abs(placed((0, 0, loM, hiM, 0, pred)) - placed((0, 0, lo3, hi3, 0, W3))).max()), 3), 'mm')
pred78 = T_mra['NAUO78'] @ WM
print('  MRA Nano carried onto PMG NAUO78: box', np.round(placed((0, 0, loM, hiM, 0, pred78)).min(0), 2).tolist(), '..',
      np.round(placed((0, 0, loM, hiM, 0, pred78)).max(0), 2).tolist())
# the inner plain Nano's board under NAUO78: where it is
inner = [r for r in mesh_rows(PMG, 'NAUO78') if r[1] in ('nano-board', 'MINIUSBSHELL', 'atmega328')]
for r in inner:
    P = placed(r)
    print(f'  NAUO78 inner {r[1]}: box {np.round(P.min(0), 2).tolist()} .. {np.round(P.max(0), 2).tolist()}')

print('\n== USB ends: own-frame boxes')
UA = Glb(ROOT + 'MRA Build Instructions Prototype/usb-a-end.glb')
UB = Glb(ROOT + 'MRA Build Instructions Prototype/usb-mini-b.glb')
for H, label in ((UA, 'MRA usb-a-end.glb'), (UB, 'MRA usb-mini-b.glb')):
    for k, n in enumerate(H.nodes):
        if 'mesh' in n:
            (_, name, lo, hi, cnt, W), = H.mesh_nodes(k)
            print(f'  {label}: {name!r} {cnt} verts own box {np.round(lo, 3).tolist()} .. {np.round(hi, 3).tolist()}')
for inst in ('NAUO278', 'NAUO280', 'NAUO283', 'NAUO279', 'NAUO281', 'NAUO282', 'NAUO277', 'NAUO284', 'NAUO285'):
    for (k, name, lo, hi, cnt, W) in PMG.mesh_nodes(PMG.find(inst)[0]):
        P = placed((k, name, lo, hi, cnt, W))
        print(f'  PMG {inst}: {name!r} {cnt} verts own box {np.round(lo, 3).tolist()} .. {np.round(hi, 3).tolist()}; '
              f'world {np.round(P.min(0), 2).tolist()} .. {np.round(P.max(0), 2).tolist()}; R {np.round(W[:3, :3], 4).tolist()} t {np.round(W[:3, 3], 3).tolist()}')

print('\n== Wire caps: own boxes')
for H, inst in ((MRA, 'NAUO95'), (PMG, 'NAUO8'), (PMG, 'NAUO130'), (PMG, 'NAUO203')):
    (_, name, lo, hi, cnt, W), = H.mesh_nodes(H.find(inst)[0])
    print(f'  {"MRA" if H is MRA else "PMG"} {inst}: {name!r} {cnt} verts own box {np.round(lo, 3).tolist()} .. {np.round(hi, 3).tolist()}')
