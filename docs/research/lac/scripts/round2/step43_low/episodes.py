"""Moment ranges where each lead touches each other wire / part (gap below a limit), at fine sampling."""
import numpy as np
from scipy.spatial import cKDTree
from blend import frames, lookup, WN, END


def episodes(path, stops, routes, moments=399, limit=-0.125):
    hits = {}
    for km, lines, M in frames(path, stops, routes, moments):
        for c, p in lines.items():
            s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
            inner = p[(s > END) & (s < s[-1] - END)]
            dp, dw, wi = lookup(inner)
            for w in np.unique(wi[dw - 0.625 < limit]):
                hits.setdefault((c, WN[int(w)]), []).append(km)
            if (dp - 0.625 < -0.19).any():
                hits.setdefault((c, 'parts'), []).append(km)
        a, b = lines['red'][3:-3], lines['black'][3:-3]
        if cKDTree(a).query(b)[0].min() - 1.25 < limit:
            hits.setdefault(('red', 'black'), []).append(km)
    step = 1.0 / (moments + 1)
    out = {}
    for k, kms in hits.items():
        runs, start, prev = [], kms[0], kms[0]
        for x in kms[1:]:
            if x - prev > step * 1.5:
                runs.append((round(start, 3), round(prev, 3)))
                start = x
            prev = x
        runs.append((round(start, 3), round(prev, 3)))
        out[k] = runs
    return out
