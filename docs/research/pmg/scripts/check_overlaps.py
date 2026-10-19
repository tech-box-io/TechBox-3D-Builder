"""Where two of the PMG guide's drawn wires run through each other: every view's wires, bent with their end parts as the player bends
them, pairs whose centre lines come within 1.2 mm of each other (the wires are 1.25 mm across) for 6 mm or more, away from the caps.

    .venv.nosync/bin/python docs/research/pmg/scripts/check_overlaps.py
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
from stepgen import _matrix  # noqa: E402

s = json.load(open(ROOT / 'PMG Build Instructions' / 'steps.json'))
routes = s['routes']


def ramp(x):
    t = np.clip((x - 0.1) / 0.8, 0, 1)
    return t * t * (3 - 2 * t)


def skin(r, poses):
    p = np.asarray(r['pts'], float)
    L = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    u = L / (L[-1] or 1)

    def mv(part, ref):
        if not part or (poses.get(part) is None and ref is None):
            return None
        M = _matrix(poses.get(part))
        return M @ np.linalg.inv(_matrix(ref)) if ref is not None else M
    A, B = mv(r.get('a'), r.get('a_ref')), mv(r.get('b'), r.get('b_ref'))
    wb = ramp(u)[:, None] if r.get('b') else np.zeros((len(p), 1))
    wa = 1 - wb if r.get('a') else np.zeros((len(p), 1))
    out = p.copy()
    if A is not None:
        out += wa * ((p @ A[:3, :3].T + A[:3, 3]) - p)
    if B is not None:
        out += wb * ((p @ B[:3, :3].T + B[:3, 3]) - p)
    return out, L


bad = {}
for v in s['views']:
    ws = v.get('wires') or {}
    lines = {w: skin(routes[n], v.get('offsets') or {}) for w, n in ws.items() if w != 'usb cable'}
    names = sorted(lines)
    for i, a in enumerate(names):
        tree = cKDTree(lines[a][0])
        for b in names[i + 1:]:
            pb, Lb = lines[b]
            d, _ = tree.query(pb)
            close = (d < 1.2) & (Lb > 12) & (Lb < Lb[-1] - 12)
            if close.sum() >= 6:
                bad.setdefault((a, b), []).append((v['name'], int(close.sum()), round(float(d.min()), 2)))
for k, hits in sorted(bad.items(), key=lambda t: -max(h[1] for h in t[1])):
    print(k, len(hits), 'views, e.g.', hits[0], hits[-1])
print(len(bad), 'pairs')
