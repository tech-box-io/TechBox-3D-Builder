"""Plan (x-z) crossings of each buzzer lead's routes with every other wire in a view, with which is on top."""
import json, sys, numpy as np
S = json.load(open(sys.argv[1] if len(sys.argv) > 1 else '/Users/lee-johnson/Desktop/Claude_Cadasio/LAC Build Instructions/steps.json'))
V = {v['name']: v for v in S['views']}; R = S['routes']
def dense(p, step=0.25):
    p = np.asarray(p, float); s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    t = np.arange(0, s[-1], step); return np.stack([np.interp(t, s, p[:, k]) for k in range(3)], 1)
def seg_cross(A, B):
    """crossings of polylines A, B in x-z: list of (i, j, ta, tb)"""
    out = []
    a0, a1 = A[:-1][:, [0, 2]], A[1:][:, [0, 2]]
    for j in range(len(B) - 1):
        b0, b1 = B[j, [0, 2]], B[j + 1, [0, 2]]
        da, db = a1 - a0, b1 - b0
        den = da[:, 0] * db[1] - da[:, 1] * db[0]
        ok = np.abs(den) > 1e-12
        w = b0 - a0
        ta = np.where(ok, (w[:, 0] * db[1] - w[:, 1] * db[0]) / np.where(ok, den, 1), -1)
        tb = np.where(ok, (w[:, 0] * da[:, 1] - w[:, 1] * da[:, 0]) / np.where(ok, den, 1), -1)
        for i in np.where(ok & (ta >= 0) & (ta < 1) & (tb >= 0) & (tb < 1))[0]:
            out.append((i, j, ta[i], tb[i]))
    return out
def report(view, routes_of=None, only=None):
    v = V[view]
    for bw in ('buzzer red', 'buzzer black'):
        no = (routes_of or {}).get(bw, v['wires'].get(bw))
        if no is None: continue
        A = dense(R[no]['pts'] if isinstance(no, int) else no, 0.5)
        print(f'== {view} {bw} route {no if isinstance(no, int) else "given"}')
        for w, wn in v['wires'].items():
            if w.startswith('buzzer') or (only and w not in only): continue
            B = dense(R[wn]['pts'], 0.5)
            for i, j, ta, tb in seg_cross(A, B):
                pa = A[i] + (A[i + 1] - A[i]) * ta; pb = B[j] + (B[j + 1] - B[j]) * tb
                print(f'   {w:14s} at x {pa[0]:6.1f} z {pa[2]:7.1f}: lead y {pa[1]:6.1f}, wire y {pb[1]:6.1f}  -> {"OVER" if pa[1] > pb[1] else "under"} by {abs(pa[1]-pb[1]):.1f}  (lead s={i*0.5:.0f})')
if __name__ == '__main__':
    for vn in ['Step 42c', 'Step 43c', 'Step 46c', 'Step 47c', 'Step 48c', 'Step 56c']:
        if vn in V: report(vn)
