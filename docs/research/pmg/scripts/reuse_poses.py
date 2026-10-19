"""PMG reuse study: the pose copies the engineer modelled, as poses of ONE copy (the built one), before a trimmed source drops
them. GLB headers only. Writes docs/research/pmg/reuse_poses.json.

    .venv.nosync/bin/python docs/research/pmg/scripts/reuse_poses.py

For each group: the built instance, and for each copy the 4x4 placement M (copy = M . built, assembly mm) taken from one anchor
mesh node, checked on every mesh node of the part (worst corner error, mm), and written as a stepgen pose: turned(axis,
degrees, at, t) about the built part's middle (`at`), i.e. p' = R (p - at) + at + t. A pose with no turn is [x, y, z].
"""
import json
import sys

import numpy as np

sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts')
from reuse_hdr import Glb  # noqa: E402
from reuse_compare import PMG, MRA, compare, mesh_rows, corners, axis_angle  # noqa: E402

OUT = '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/reuse_poses.json'


def box_mid(rows):
    P = np.vstack([(corners(lo, hi) @ W.T)[:, :3] for (_, _, lo, hi, _, W) in rows])
    return (P.min(0) + P.max(0)) / 2, P.min(0), P.max(0)


def as_pose(M, at):
    R = M[:3, :3]
    t = R @ at + M[:3, 3] - at
    ax, deg = axis_angle(R)
    if deg < 1e-4:
        return [round(float(c), 3) for c in M[:3, 3]]
    return dict(t=[round(float(c), 3) for c in t], r=ax + [deg], at=[round(float(c), 3) for c in at])


def anchor_matrix(inst, anchor, skip=()):
    rows = mesh_rows(PMG, inst, skip)
    w = [r for r in rows if r[1] == anchor]
    assert len(w) >= 1, (inst, anchor)
    return w[0][5], rows


def check(M, built_rows, copy_rows):
    """Worst corner distance between the built part's meshes carried by M and the copy's same-named meshes."""
    worst = 0.0
    for r in built_rows:
        P = (corners(r[2], r[3]) @ (M @ r[5]).T)[:, :3]
        cands = [c for c in copy_rows if c[1] == r[1]]
        if not cands:
            continue
        worst = max(worst, min(np.abs(P - (corners(c[2], c[3]) @ c[5].T)[:, :3]).max() for c in cands))
    return round(float(worst), 4)


groups = [
    ('I/O module (shield; its inner plain Nano left out)', 'NAUO78', [('NAUO1', 'on the bench, flat'), ('NAUO94', 'held 104.7 mm above its place on H4')],
     'Shield_Arduino NANO', {'NAUO78': ('NAUO301',), 'NAUO94': ('NAUO301',), 'NAUO1': ('NAUO387',)}),
    ('Button, black cap (D4)', 'NAUO76', [('NAUO7', 'on the bench, behind the module')], 'Board^Big Button Module_По умолчанию', {}),
    ('Button, yellow cap (D5)', 'NAUO83', [('NAUO6', 'on the bench')], 'Board^Big Button Module_По умолчанию', {}),
    ('Button, white cap (D6)', 'NAUO84', [('NAUO5', 'on the bench')], 'Board^Big Button Module_По умолчанию', {}),
    ('Button, blue cap (D7)', 'NAUO85', [('NAUO4', 'on the bench')], 'Board^Big Button Module_По умолчанию', {}),
    ('4-digit display', 'NAUO79', [('NAUO80', 'on the bench'), ('NAUO129', 'beside its place (80 mm along +z)')], 'Display TM1637_По умолчанию', {}),
    ('LED matrix', 'NAUO81', [('NAUO44', 'on the bench'), ('NAUO82', 'in front of its place (143.3 mm along -z)'), ('NAUO267', 'above its place')], 'PCB', {}),
    ('USB Mini-B end (right angle)', 'NAUO282', [('NAUO279', 'on the bench'), ('NAUO281', 'with the module held above H4')], 'USB Right Angle', {}),
    ('USB A end', 'NAUO278', [('NAUO280', 'upright, beside the module'), ('NAUO283', 'on the bench')], 'USB Cable end', {}),
]
out = dict(_about='Pose copies in pmg.glb as poses of one built copy (stepgen poses, assembly mm). Written by '
                  'docs/research/pmg/scripts/reuse_poses.py from the GLB header; "worst_mm" is how far the built copy carried by the '
                  'pose lands from the copy, over every mesh of the part.', groups=[])
for title, built, copies, anchor, skips in groups:
    Wb, rows_b = anchor_matrix(built, anchor, skips.get(built, ()))
    mid, lo, hi = box_mid(rows_b)
    g = dict(part=title, built=built, built_box=[np.round(lo, 2).tolist(), np.round(hi, 2).tolist()], at=np.round(mid, 3).tolist(), copies=[])
    print(f'== {title}: built {built}, box {np.round(lo, 1).tolist()} .. {np.round(hi, 1).tolist()}')
    for inst, note in copies:
        Wc, rows_c = anchor_matrix(inst, anchor, skips.get(inst, ()))
        M = Wc @ np.linalg.inv(Wb)
        pose = as_pose(M, mid)
        worst = check(M, rows_b, rows_c)
        g['copies'].append(dict(instance=inst, where=note, pose=pose, worst_mm=worst, matrix=np.round(M, 6).tolist()))
        print(f'   {inst} ({note}): pose {pose}  worst {worst} mm')
    out['groups'].append(g)

# the Nano: its seat is the MRA's Nano carried with the MRA's module onto NAUO78 (the PMG's own nano copies are not seated)
Tm = {}
for inst in ('NAUO78', 'NAUO1', 'NAUO94'):
    inner = {'NAUO1': ('NAUO387',)}.get(inst, ('NAUO301',))
    ra, rb = mesh_rows(MRA, 'NAUO82', ('NAUO126',)), mesh_rows(PMG, inst, inner)
    wa = [r for r in ra if r[1] == 'Shield_Arduino NANO'][0][5]
    wb = [r for r in rb if r[1] == 'Shield_Arduino NANO'][0][5]
    Tm[inst] = wb @ np.linalg.inv(wa)
(_, _, loN, hiN, _, WN), = MRA.mesh_nodes(MRA.find('NAUO126')[0])
seat = Tm['NAUO78'] @ WN
P = (corners(loN, hiN) @ seat.T)[:, :3]
mid = (P.min(0) + P.max(0)) / 2
g = dict(part='Nano Board (the MRA model, nano-mra.glb): its seat on NAUO78', built='NANO (extra part)',
         built_box=[np.round(P.min(0), 2).tolist(), np.round(P.max(0), 2).tolist()], at=np.round(mid, 3).tolist(), copies=[],
         extra_parts_pose=dict(t=np.round(Tm['NAUO78'][:3, 3], 3).tolist(), r=axis_angle(Tm['NAUO78'][:3, :3])[0] + [axis_angle(Tm['NAUO78'][:3, :3])[1]], at=[0, 0, 0]),
         note='extra_parts pose for nano-mra.glb cut from mra.glb NAUO126 WITHOUT --like (the file then holds the Nano where the MRA has '
              'it): the MRA module -> PMG NAUO78 transform, exact on all 36 shield meshes. Its board lands on the CAD inner plain Nano\'s board (NAUO301) to 0.01 mm.')
print(f'== Nano seat on NAUO78: box {np.round(P.min(0), 2).tolist()} .. {np.round(P.max(0), 2).tolist()}; extra_parts pose {g["extra_parts_pose"]}')
for inst, note in (('NAUO2', 'hovering over the bench module NAUO1'), ('NAUO3', 'over the bench module NAUO1, not seated')):
    (_, _, lo, hi, _, W), = PMG.mesh_nodes(PMG.find(inst)[0])
    M = W @ np.linalg.inv(seat)
    seat1 = Tm['NAUO1'] @ WN
    off = W[:3, 3] - seat1[:3, 3]
    g['copies'].append(dict(instance=inst, where=note, pose=as_pose(M, mid), worst_mm=0.0, matrix=np.round(M, 6).tolist(),
                            above_true_seat_on_NAUO1_mm=np.round(off, 3).tolist()))
    print(f'   {inst}: pose {as_pose(M, mid)}; offset from the true seat on NAUO1 {np.round(off, 3).tolist()} mm')
out['groups'].insert(1, g)

# do the USB plug copies ride with the module copies exactly?
Wp, rows_p = anchor_matrix('NAUO282', 'USB Right Angle')
for mod, plug in (('NAUO1', 'NAUO279'), ('NAUO94', 'NAUO281')):
    M = Tm[mod] @ np.linalg.inv(Tm['NAUO78'])
    _, rows_c = anchor_matrix(plug, 'USB Right Angle')
    print(f'   plug {plug} vs NAUO282 carried with the module NAUO78 -> {mod}: worst {check(M, rows_p, rows_c)} mm')
json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
print('written', OUT)
