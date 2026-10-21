"""Gauss linking numbers: each buzzer lead's loop (lying shape + the stub's path + the seated shape reversed) against every other wire
in Step 43c, closed under the table (both ends straight down to y 850, joined there)."""
import json, sys
import numpy as np
sys.path.insert(0, '/Users/lee-johnson/Desktop/Claude_Cadasio/tools')
from stepgen import apply_pose, _matrix

KIT = '/Users/lee-johnson/Desktop/Claude_Cadasio/LAC Build Instructions'


def lk(P, Q):
    """Gauss linking number of two closed polylines (exact per segment pair: the solid-angle formula, Klenin & Langowski 2000)."""
    P = np.asarray(P, float); Q = np.asarray(Q, float)
    a0, a1 = P[:-1], P[1:]
    b0, b1 = Q[:-1], Q[1:]
    tot = 0.0
    for i in range(len(a0)):
        r1, r2 = a0[i], a1[i]
        r3, r4 = b0, b1
        r13, r14, r23, r24 = r3 - r1, r4 - r1, r3 - r2, r4 - r2
        def nrm(u, v):
            c = np.cross(u, v); n = np.linalg.norm(c, axis=1, keepdims=True)
            return c / np.where(n < 1e-12, 1, n)
        n1, n2, n3, n4 = nrm(r13, r14), nrm(r14, r24), nrm(r24, r23), nrm(r23, r13)
        s = lambda u, v: np.arcsin(np.clip(np.einsum('ij,ij->i', u, v), -1, 1))
        om = s(n1, n2) + s(n2, n3) + s(n3, n4) + s(n4, n1)
        sign = np.sign(np.einsum('ij,ij->i', np.cross(r4 - r3, np.broadcast_to(r2 - r1, r13.shape)), r13))
        tot += float((om * sign).sum())
    return tot / (4 * np.pi)


def closed_under(pts, floor=850.0):
    p = np.asarray(pts, float)
    a, b = p[0].copy(), p[-1].copy()
    a[1] = floor; b[1] = floor
    return np.vstack([p, b, a, p[:1]])


def exit_path(poses, exit_, n=40):
    """The stub's exit point through the buzzer's stops (straight between stop positions: high over everything during the carry)."""
    pts = [apply_pose(p, np.asarray([exit_], float))[0] if p is not None else np.asarray(exit_, float) for p in poses]
    out = []
    for a, b in zip(pts[:-1], pts[1:]):
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(a + (b - a) * t)
    out.append(pts[-1])
    return np.array(out)


def lead_loop(lying, seated, poses, exit_):
    """lying: from the hole to the lying exit; seated: from the hole to the seated exit."""
    path = exit_path(poses, exit_)
    return np.vstack([lying, path[1:], seated[::-1][1:]])


if __name__ == '__main__':
    steps = json.load(open(sys.argv[1] if len(sys.argv) > 1 else f'{KIT}/steps.json'))
    R = steps['routes']
    V = {v['name']: v for v in steps['views']}
    v43 = V['Step 43c']
    path = v43['path']
    leads = {'red': (v43.get('wire_via', {}).get('buzzer red'), [674.5, 894.24, 1233.12]), 'black': (None, [676.02, 894.24, 1233.12])}
    lying = {'buzzer red': V['Step 42c']['wires']['buzzer red'], 'buzzer black': V['Step 42c']['wires']['buzzer black']}
    seated = {'buzzer red': v43['wires']['buzzer red'], 'buzzer black': v43['wires']['buzzer black']}
    ex = {'buzzer red': [674.5, 894.24, 1233.12], 'buzzer black': [676.02, 894.24, 1233.12]}
    for w in ('buzzer red', 'buzzer black'):
        Ly = np.asarray(R[lying[w]]['pts']); Se = np.asarray(R[seated[w]]['pts'])
        L = lead_loop(Ly, Se, path, ex[w])
        print(w, 'loop gap check', np.linalg.norm(L[len(Ly) - 1] - Ly[-1]).round(3))
        out = []
        for o, ri in v43['wires'].items():
            if o.startswith('buzzer'):
                continue
            O = closed_under(R[ri]['pts'])
            out.append((round(lk(L, O), 2), o))
        print('  ', ', '.join(f'{o} {x:+.2f}' for x, o in out))
