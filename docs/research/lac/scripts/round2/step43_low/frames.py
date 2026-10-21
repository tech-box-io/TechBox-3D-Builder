"""Plan views of the two leads at chosen moments of Step 43 over the other wires (PNG)."""
import numpy as np
from PIL import Image
from blend import frames, along
from plot import plan, view_lines
from common import *


def strip(path, stops, routes, kms, out, xlim=(640, 715), zlim=(1225, 1410), scale=6):
    S = load_steps()
    base = {w: p for w, p in view_lines(S, 'Step 43c').items() if not w.startswith('buzzer')}
    ims = []
    for km_want in kms:
        best = None
        for km, lines, M in frames(path, stops, routes, moments=399):
            if best is None or abs(km - km_want) < abs(best[0] - km_want):
                best = (km, lines, M)
        km, lines, M = best
        ex = (M[BUZZER] @ np.r_[674.5, 894.24, 1233.12, 1.0])[:3]
        L = dict(base)
        L.update({f'new {c}': p for c, p in lines.items()})
        L['new buzzer_exit'] = np.array([ex, ex + [0.5, 0, 0.5]])
        name = f'_f{int(km * 1000):04d}.png'
        plan(L, name, xlim=xlim, zlim=zlim, scale=scale, label_every=8, title=f'km {km:.3f}  exit y {ex[1]:.0f} z {ex[2]:.0f}')
        ims.append(Image.open(SCR / name))
    w, h = ims[0].size
    cols = min(4, len(ims))
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (w * cols, h * rows), 'white')
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    sheet.save(SCR / out)
