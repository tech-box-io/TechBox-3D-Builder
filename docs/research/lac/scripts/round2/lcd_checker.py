"""The LCD (and its four female caps) against the parts on screen in Steps 50 - 51, sampled along each stretch of a pose list as the
player mixes poses (player.js mixPose = motioncheck.mix)."""
import json, numpy as np
from scipy import ndimage
from poses import mix, M_of, tf, KEY
from plate import face_tris, raster

def lcd_points():
    d = np.load('NAUO94.npz'); P = [d['V']]
    for c in ('NAUO97', 'NAUO98', 'NAUO99', 'NAUO100'):
        P.append(np.load(c + '.npz')['V'])
    P = np.vstack(P)
    P = np.unique(np.round(P, 2), axis=0)
    return P

# LCD solid as boxes (seated), for the reverse test (plate points inside the LCD)
LCD_BOXES = np.array([
    [[712.16, 889.52, 1262.22], [713.76, 949.52, 1360.22]],   # board
    [[713.76, 899.52, 1262.80], [722.76, 939.52, 1359.60]],   # display (bezel)
    [[706.66, 945.25, 1310.85], [718.16, 947.79, 1351.49]],   # 16-pin header strip
    [[705.41, 931.25, 1314.93], [712.16, 944.00, 1357.23]],   # backpack parts
    [[703.26, 932.95, 1337.97], [712.16, 943.11, 1356.65]],   # I2C header, pot
    [[702.73, 933.30, 1349.80], [704.48, 942.70, 1357.80]],   # female caps
    [[709.76, 899.52, 1267.00], [712.16, 939.52, 1271.00]],   # bezel tabs at the F8 end
])

class Plate:
    def __init__(self, pid, axis, step=0.1, pose=None):
        d = np.load(f'obs_{pid}.npz'); V, F = d['V'], d['F']
        self.pid, self.pose = pid, pose
        if pose is not None:   # back to its seated frame
            Minv = np.linalg.inv(M_of(pose)); V = tf(Minv, V)
        self.axis = axis
        lo, hi = V[:, axis].min(), V[:, axis].max()
        self.lo, self.hi = lo, hi
        T1, T2 = face_tris(V, F, axis, lo, 0.05), face_tris(V, F, axis, hi, 0.05)
        T = T1 if len(T1) <= len(T2) else T2
        self.ax2 = [a for a in range(3) if a != axis]
        T2d = T[:, :, self.ax2]
        mn = V[:, self.ax2].min(0) - 0.5; mx = V[:, self.ax2].max(0) + 0.5
        self.xs, self.ys, self.G = raster(T2d, mn, mx, step)
        self.step, self.mn = step, mn
        self.depth2d = ndimage.distance_transform_edt(self.G) * step
    def inside(self, P, tol=0.05):
        """depth of each point inside the plate (<=0 outside)."""
        if self.pose is not None:
            P = tf(np.linalg.inv(M_of(self.pose)), P)
        a = P[:, self.axis]
        dn = np.minimum(a - self.lo, self.hi - a)
        uv = P[:, self.ax2]
        i = np.floor((uv[:, 0] - self.mn[0]) / self.step).astype(int); j = np.floor((uv[:, 1] - self.mn[1]) / self.step).astype(int)
        ok = (i >= 0) & (i < len(self.xs)) & (j >= 0) & (j < len(self.ys)) & (dn > tol)
        dep = np.full(len(P), -1.0)
        dep[ok] = np.minimum(dn[ok], self.depth2d[i[ok], j[ok]])
        return dep
    def samples(self, spacing=0.3, levels=3):
        """points through the plate (assembly mm, posed)."""
        sub = max(1, int(round(spacing / self.step)))
        G = self.G[::sub, ::sub]; xs = self.xs[::sub]; ys = self.ys[::sub]
        X, Y = np.meshgrid(xs, ys, indexing='ij')
        uv = np.stack([X[G], Y[G]], 1)
        out = []
        for t in np.linspace(self.lo + 0.02, self.hi - 0.02, levels):
            P = np.zeros((len(uv), 3)); P[:, self.ax2[0]] = uv[:, 0]; P[:, self.ax2[1]] = uv[:, 1]; P[:, self.axis] = t
            out.append(P)
        P = np.vstack(out)
        if self.pose is not None:
            P = tf(M_of(self.pose), P)
        return P

def in_boxes(Q, boxes=LCD_BOXES, tol=0.05):
    d = np.full(len(Q), -1.0)
    for lo, hi in boxes:
        dd = np.minimum(Q - lo, hi - Q).min(1)
        d = np.maximum(d, dd)
    return np.where(d > tol, d, -1.0)

def make_scene():
    s = json.load(open('/Users/lee-johnson/Desktop/Claude_Cadasio/LAC Build Instructions/steps.json'))
    v = [v for v in s['views'] if v['name'] == 'Step 50c'][0]
    F1_ASIDE = v['offsets']['NAUO10']
    plates = [Plate('NAUO44', 2), Plate('NAUO45', 2), Plate('NAUO2', 1), Plate('F4', 1), Plate('NAUO42', 0), Plate('NAUO43', 0),
              Plate('NAUO10', 0, pose=F1_ASIDE)]
    bounds = json.load(open('obs_bounds.json'))
    others = {k: np.array(b[:2]) for k, b in bounds.items() if k not in [p.pid for p in plates]}
    return plates, others

TABLE_Y = 884.61

def check(name, a, b, P, plates, others, n=41, samples=None, verbose=True):
    worst = {}
    for k in np.linspace(0, 1, n):
        M = mix(a, b, k)
        Q = tf(M, P)
        lo, hi = Q.min(0), Q.max(0)
        for pl in plates:
            d = pl.inside(Q)
            if (d > 0).any():
                j = int(np.argmax(d)); key = (pl.pid, 'lcd in')
                if d[j] > worst.get(key, (0,))[0]:
                    worst[key] = (round(float(d[j]), 2), round(float(k), 3), Q[j].round(1).tolist(), int((d > 0.3).sum()))
            # reverse: plate points inside the LCD
            S = samples[pl.pid]
            near = np.all((S > lo - 1) & (S < hi + 1), axis=1)
            if near.any():
                Sl = tf(np.linalg.inv(M), S[near])
                d2 = in_boxes(Sl)
                if (d2 > 0).any():
                    j = int(np.argmax(d2)); key = (pl.pid, 'in lcd')
                    if d2[j] > worst.get(key, (0,))[0]:
                        worst[key] = (round(float(d2[j]), 2), round(float(k), 3), S[near][j].round(1).tolist(), int((d2 > 0.3).sum()))
        for pid, (blo, bhi) in others.items():
            inb = np.all((Q > blo + 0.05) & (Q < bhi - 0.05), axis=1)
            if inb.any():
                key = (pid, 'lcd in box')
                c = int(inb.sum())
                if c > worst.get(key, (0, 0, 0, 0))[3]:
                    worst[key] = (0.0, round(float(k), 3), Q[inb][0].round(1).tolist(), c)
        if lo[1] < TABLE_Y - 0.05:
            key = ('table', 'below')
            dd = TABLE_Y - lo[1]
            if dd > worst.get(key, (0,))[0]:
                worst[key] = (round(float(dd), 2), round(float(k), 3), Q[np.argmin(Q[:, 1])].round(1).tolist(), int((Q[:, 1] < TABLE_Y).sum()))
    if verbose:
        if not worst: print(f'{name}: clear')
        for key, val in sorted(worst.items(), key=lambda kv: -kv[1][0]):
            print(f'{name}: {key[0]:7s} {key[1]:10s} depth {val[0]:5.2f} mm at k {val[1]:.3f} near {val[2]} ({val[3]} pts)')
    return worst
