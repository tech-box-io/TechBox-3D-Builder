"""Project assembly points into a step's camera as the player does (fov 45, padding 1.08, up = world y)."""
import numpy as np
SIZES = {'760x634': (760, 634, (16, 14, 540, 136)), '1000x548': (1000, 548, (16, 14, 576, 112)),
         '1440x628': (1440, 628, (16, 14, 576, 112)), '1920x914': (1920, 914, (16, 14, 576, 112))}


def project(pts, cam, w, h, fov=45.0, pad=1.08):
    d = np.asarray(cam['dir'], float); d /= np.linalg.norm(d)
    t = np.asarray(cam['target'], float)
    half = np.radians(fov / 2); aspect = w / h
    fitV = cam['radius'] / np.sin(half); fitH = cam['radius'] / np.sin(np.arctan(np.tan(half) * aspect))
    pos = t + d * max(fitV, fitH) * pad
    f = -d; r = np.cross(f, [0, 1, 0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    q = np.asarray(pts, float) - pos
    z = q @ f; x = q @ r; y = q @ u
    th = np.tan(half)
    nx = x / (z * th * aspect); ny = y / (z * th)
    return np.c_[(nx + 1) / 2 * w, (1 - ny) / 2 * h]


def report(pts, cam, label=''):
    out = []
    for k, (w, h, box) in SIZES.items():
        p = project(pts, cam, w, h)
        under = ((p[:, 0] > box[0]) & (p[:, 0] < box[2]) & (p[:, 1] > box[1]) & (p[:, 1] < box[3])).mean()
        off = ((p[:, 0] < 0) | (p[:, 0] > w) | (p[:, 1] < 0) | (p[:, 1] > h)).mean()
        out.append(f'{k}: top y {p[:, 1].min():.0f} x {p[:, 0].min():.0f}-{p[:, 0].max():.0f} under box {under:.0%} off {off:.0%}')
    print(label, ' | '.join(out))
