"""PMG: compare the top-level transforms of chosen Cadasio components and GLB instances (rotation angle, axis, translation).

    .venv.nosync/bin/python docs/research/pmg/scripts/pairs.py "Cadasio name=NAUOn" ...
"""
import json, sys, math
import numpy as np
W = '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/scripts/work/cadasio_map'
T = {t['name']: t for t in json.load(open(W + '/cadasio_tree.json'))['tops']}
G = json.load(open(W + '/glb_boxes.json'))


def rel(a, b):
    """pose taking a (4x4, mm) to b: rotation angle (deg), axis, and where a's origin goes."""
    A = np.array(a); B = np.array(b)
    Rr = B[:3, :3] @ A[:3, :3].T
    ang = math.degrees(math.acos(max(-1, min(1, (np.trace(Rr) - 1) / 2))))
    ax = np.array([Rr[2, 1] - Rr[1, 2], Rr[0, 2] - Rr[2, 0], Rr[1, 0] - Rr[0, 1]])
    n = np.linalg.norm(ax)
    if ang > 179: ax = np.sqrt(np.maximum(np.diag(Rr) + 1, 0) / 2)
    elif n > 1e-9: ax = ax / n
    return round(ang, 2), np.round(ax, 3).tolist(), np.round(B[:3, 3] - A[:3, 3], 2).tolist()


for arg in sys.argv[1:]:
    a, b = arg.split('=')
    A = T[a]['matrix_mm'] if a in T else G[a]['matrix_mm']
    B = G[b]['matrix_mm'] if b in G else T[b]['matrix_mm']
    print(arg, '-> turn deg, axis, origin shift mm:', rel(A, B))
