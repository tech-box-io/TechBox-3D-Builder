"""Step 42 from behind: for each direction (azimuth from straight behind towards -z, elevation), the smallest frame that keeps the moving
module (with its Nano Board and plug), the USB A end and the cable (as steps.json has them now) on screen and clear of the caption box,
at all four window sizes and at the three wider ones; and what the case hides of the module and the A end from there."""
import sys, os, runpy
import numpy as np
argv = sys.argv[1:]
sys.argv = ['x']
ns = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cam42.py'), run_name='lib')
project, SIZES, KEY, MOMENTS, cable, hidden = ns['project'], ns['SIZES'], ns['KEY'], ns['MOMENTS'], ns['cable'], ns['hidden']
KEYs = KEY[::3]


def bad(cam, sizes):
    for key in sizes:
        w, h, box = SIZES[key]
        q = project(KEYs, cam, w, h)
        if (q[:, 0] < 8).any() or (q[:, 0] > w - 8).any() or (q[:, 1] < 8).any() or (q[:, 1] > h - 8).any(): return True
        if ((q[:, 0] > box[0] - 4) & (q[:, 0] < box[2] + 4) & (q[:, 1] > box[1] - 4) & (q[:, 1] < box[3] + 4)).any(): return True
    return False


def fit(d, sizes):
    d = np.asarray(d, float) / np.linalg.norm(d)
    f = -d; r = np.cross(f, [0, 1, 0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    c0 = (KEY.min(0) + KEY.max(0)) / 2
    best = None
    for sh in np.arange(-0.6, 0.31, 0.05):
        for sr in np.arange(-0.5, 0.51, 0.05):
            mk = lambda rad: dict(dir=d.round(4).tolist(), target=(c0 + u * sh * rad + r * sr * rad).round(0).tolist(), radius=float(rad))
            if bad(mk(240.0), sizes): continue
            lo, hi = 70.0, 240.0
            while hi - lo > 1.0:
                mid = (lo + hi) / 2
                (lo, hi) = (mid, hi) if bad(mk(mid), sizes) else (lo, mid)
            if best is None or hi < best[0] - 0.5 or (abs(hi - best[0]) <= 0.5 and abs(sr) + abs(sh) < abs(best[2]) + abs(best[3])):
                best = (hi, mk(np.ceil(hi)), round(float(sh), 2), round(float(sr), 2))
    return best


for a in argv:
    az, el = map(float, a.split(','))
    ar, er = np.radians(az), np.radians(el)
    d = [np.cos(er) * np.cos(ar), np.sin(er), -np.cos(er) * np.sin(ar)]
    for sizes in (list(SIZES), ['1000x548', '1440x628', '1920x914']):
        b = fit(d, sizes)
        if b is None: print(f'az {az:4.0f} el {el:3.0f} sizes {len(sizes)}: none'); continue
        cam = b[1]
        hm = max(hidden(cam, m[::4]) for _, _, m, _ in MOMENTS)
        ha = max(hidden(cam, a_[::2]) for _, _, _, a_ in MOMENTS)
        print(f"az {az:4.0f} el {el:3.0f} sizes {len(sizes)}: radius {cam['radius']:.0f} target {cam['target']} dir {cam['dir']} (up {b[2]}, "
              f"right {b[3]})  most hidden: module {hm:.0%} A end {ha:.0%}", flush=True)
