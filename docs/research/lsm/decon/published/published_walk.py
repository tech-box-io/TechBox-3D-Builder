"""The published LSM take-apart (Cadasio 19075), replayed: for each viewer step, which top-level components show and how far each has
moved from where the CAD has it, in our assembly mm (the published coordinates are in our frame: docs/research/lsm/decon/arrows/report.md).

    python -I published_walk.py <payload.json> <out.json>

Visibility is set on leaf solids (the assembly's `hidden` is only the initial value); `position` is a node's local position in its
parent's frame, so a leaf's world move = R(parent chain) @ (position - rest translation) / SF (the corrected walk described at the top of
docs/research/guide_19075-laser_stem_matrix_lsm_-_deconstruction.md). Transforms are 16 numbers, column-major (three.js)."""
import json
import sys

import numpy as np

src, out = sys.argv[1], sys.argv[2]
j = json.load(open(src))
steps, order, A = j['steps'], j['orderedSteps'], j['assemblyStructure']
SF = A['scaleFactor']

OURS = {'LSM_Bottom_r1-1': 'D1', 'LSM_Side3_r2-1': 'D2', 'LSM_Side2_r2-1': 'D4', 'LSM_Side4_r2-1': 'D5', 'LSM_Lens_Bottom-3': 'D6',
        'LSM_Lens_Middle-2': 'D7', 'LSM_Lens_Top-1': 'D8', 'LSM_MatrixSupportLong_r3-2': 'D9_A', 'LSM_MatrixSupportLong_r3-3': 'D9_B',
        'LSM_MatrixSupportSmall_r2-1': 'D10', 'LSM_LensSupport_r2-2': 'D11_A', 'LSM_LensSupport_r2-3': 'D11_B',
        'LSM_LensSupport_r2-1': 'D11_C', 'LSM_LensSupport_r2-4': 'D11_D', 'LSM_Side1_r8-1': 'D3', 'Breadboard-1': 'BREADBOARD',
        'Paper-1': 'BACKING', '8x8 LED-4': 'MATRIX', 'Arduino Nano V1-1': 'NANO', 'USB Right Angle-1': 'USB_B', 'USB Cable end-2': 'USB_A',
        'Resistor 1-1': 'R12K', 'Resistor 2-1': 'R330', 'Capacitor V3-1': 'CAP', 'Push button-1': 'BUTTON+NUT',
        'Wire Cap-14': 'J_WHITE_F', 'Wire Cap-15': 'J_PURPLE_F', 'Wire Cap-16': 'J_GREY_F'}

nodes = {}


def mat(s):
    return np.array([float(x) for x in s.split(',')]).reshape(4, 4).T     # column-major -> row-major


def walk(n, parent, top):
    r = n['rootReference']
    M = mat(r['transform'])
    kids = n.get('children') or []
    nodes[r['id']] = dict(name=r['name'], parent=parent, top=top, M=M, rest_t=M[:3, 3].copy(), leaf=not kids,
                          visible=not r.get('hidden', False), pos=M[:3, 3].copy())
    for c in kids:
        walk(c, r['id'], top if top else r['id'])


root = A['rootReference']['id']
nodes[root] = dict(name='root', parent=None, top=None, M=np.eye(4), rest_t=np.zeros(3), leaf=False, visible=True, pos=np.zeros(3))
for c in A['children']:
    walk(c, root, None)
for k, nd in nodes.items():                      # (a top-level node is its own top)
    if nd['parent'] == root:
        nd['top'] = k


def chain_R(k):
    """The world rotation of node k's parent frame."""
    R = np.eye(3)
    p = nodes[k]['parent']
    while p is not None and p != root:
        R = nodes[p]['M'][:3, :3] @ R
        p = nodes[p]['parent']
    return R


# hidden flags of ancestors: the study says only leaves carry visibility; a top-level 'hidden' is the leaves' initial value
for k, nd in nodes.items():
    if nd['leaf'] and nd['top'] and k != nd['top']:
        nd['visible'] = not (not nodes[nd['top']]['visible']) and nd['visible']
Rc = {k: chain_R(k) for k, nd in nodes.items() if nd['leaf']}

frames = []
frame = -1
for idx, sid in enumerate(order):
    s = steps[sid]
    for k, p in (s.get('properties') or {}).items():
        if k in nodes and isinstance(p, dict):
            if p.get('visible') is not None:
                nodes[k]['visible'] = bool(p['visible'])
            if isinstance(p.get('position'), dict):
                q = p['position']
                nodes[k]['pos'] = np.array([float(q.get('x', 0)), float(q.get('y', 0)), float(q.get('z', 0))])
    if s.get('behaviour') == 'hidden':
        continue
    frame += 1
    tops = {}
    for k, nd in nodes.items():
        if not nd['leaf'] or not nd['top'] or not nd['visible']:
            continue
        d = Rc[k] @ (nd['pos'] - nd['rest_t']) / SF
        tops.setdefault(nd['top'], []).append(d)
    shown = {}
    for t, ds in tops.items():
        name = nodes[t]['name']
        ds = np.array(ds)
        shown[OURS.get(name, name)] = dict(n=len(ds), move=np.round(np.median(ds, 0), 1).tolist(),
                                           spread=round(float(np.ptp(np.linalg.norm(ds, axis=1))), 1))
    frames.append(dict(frame=frame, step=s['name'], behaviour=s.get('behaviour'), shown=shown))

json.dump(dict(scale_factor=SF, frames=frames), open(out, 'w'), indent=0)
# a compact listing: what changes from frame to frame
prev = {}
for f in frames:
    cur = f['shown']
    gone = sorted(set(prev) - set(cur))
    came = sorted(set(cur) - set(prev))
    moved = sorted((k, cur[k]['move']) for k in cur if k in prev and np.linalg.norm(np.subtract(cur[k]['move'], prev[k]['move'])) > 0.5)
    print(f"[{f['frame']:03d}] {f['step']:<14s} gone {gone[:12]}{'...' if len(gone) > 12 else ''} came {came[:12]}"
          f"{'...' if len(came) > 12 else ''} moved {moved[:8]}")
    prev = cur
