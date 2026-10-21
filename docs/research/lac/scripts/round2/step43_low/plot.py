import sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from common import *

BOX = {'board': ([647.8, 1263.1], [703.9, 1346.1]), 'Nano': ([667.6, 1300.1], [685.6, 1345.1]), 'RTC': ([647.0, 1279.3], [661.4, 1301.1]),
       'USBplug': ([658.3, 1337.6], [682.3, 1357.5]), 'buzzer': ([651.5, 1220.0], [699.0, 1235.5]), 'F7A': ([639.1, 1223.1], [661.9, 1243.2]),
       'F7B': ([688.6, 1223.1], [711.4, 1243.2]), 'res': ([663.7, 1269.0], [700.2, 1279.3]), 'LCD': ([698.0, 1381.3], [758.0, 1479.3])}
COL = {'black': (0, 0, 0), 'green': (0, 150, 0), 'purple': (150, 0, 180), 'blue': (0, 0, 230), 'white': (170, 170, 170), 'dark_red': (120, 30, 30),
       'orange': (255, 140, 0), 'yellow': (200, 170, 0), 'teal': (0, 160, 160), 'red': (230, 0, 0), 'tan': (190, 150, 90), 'cable': (110, 110, 110)}


def plan(lines, out, xlim=(640, 715), zlim=(1225, 1410), scale=10, label_every=6, axes=(0, 2), boxes=True, title=''):
    W_, H_ = int((xlim[1] - xlim[0]) * scale), int((zlim[1] - zlim[0]) * scale)
    im = Image.new('RGB', (W_ + 60, H_ + 40), 'white')
    d = ImageDraw.Draw(im)
    f = ImageFont.load_default()
    X = lambda x: 50 + (x - xlim[0]) * scale
    Z = lambda z: 20 + (zlim[1] - z) * scale
    for g in range(int(xlim[0]) // 5 * 5, int(xlim[1]) + 1, 5):
        d.line([(X(g), Z(zlim[0])), (X(g), Z(zlim[1]))], fill=(235, 235, 235)); d.text((X(g) - 8, H_ + 24), str(g), fill=(120, 120, 120), font=f)
    for g in range(int(zlim[0]) // 5 * 5, int(zlim[1]) + 1, 5):
        d.line([(X(xlim[0]), Z(g)), (X(xlim[1]), Z(g))], fill=(235, 235, 235)); d.text((2, Z(g) - 5), str(g), fill=(120, 120, 120), font=f)
    if boxes:
        for n, (lo, hi) in BOX.items():
            d.rectangle([X(lo[0]), Z(hi[1]), X(hi[0]), Z(lo[1])], outline=(150, 150, 150))
            d.text((X(lo[0]) + 2, Z(lo[1]) - 12), n, fill=(150, 150, 150), font=f)
    for w, p in lines.items():
        p = np.asarray(p, float)
        c = COL.get(w.split()[-1].split('_')[0] if not w.endswith('dark_red') else 'dark_red', (0, 0, 0))
        wd = 4 if w.startswith('buzzer') or w.startswith('new') else 1
        pts = [(X(q[axes[0]]), Z(q[axes[1]])) for q in p]
        if w.startswith('lcd'):
            for a, b in zip(pts[:-1:2], pts[1::2]):
                d.line([a, b], fill=c, width=wd)
        else:
            d.line(pts, fill=c, width=wd)
        s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
        for t in np.arange(0, s[-1], label_every):
            i = int(np.argmin(abs(s - t)))
            if xlim[0] < p[i, axes[0]] < xlim[1] and zlim[0] < p[i, axes[1]] < zlim[1]:
                d.text((X(p[i, axes[0]]) + 2, Z(p[i, axes[1]]) - 4), f'{p[i, 1]:.0f}', fill=c, font=f)
    d.text((60, 4), title, fill=(0, 0, 0), font=f)
    im.save(SCR / out)


def view_lines(steps, view):
    R = steps['routes']; v = {x['name']: x for x in steps['views']}[view]
    return {w: R[ri]['pts'] for w, ri in v['wires'].items()}


if __name__ == '__main__':
    S = load_steps()
    plan(view_lines(S, sys.argv[1]), sys.argv[2], title=sys.argv[1] + ' plan: x right, z up; numbers = y')
