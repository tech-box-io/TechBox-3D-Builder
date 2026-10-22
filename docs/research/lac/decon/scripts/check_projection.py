"""Project the extracted rings and arrows with the published camera (fov 45 vertical, 2.071:1, the pictures' 1400 x 676) and compare
the rings with Cadasio's own stored screen position (target_position): checks the camera, the world placements and the anchors."""
import json, math, sys
from pathlib import Path
import numpy as np
from scipy.spatial.transform import Rotation
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lacpub import j, steps, order, State, MM, v3
d = json.load(open(Path(__file__).resolve().parents[1] / 'published_geometry.json'))
ASPECT = 1400 / 676
S = State(); cams = []
for sid in order:
    s = steps[sid]; S.apply(s)
    if s.get('behaviour') == 'hidden': continue
    cams.append(dict(S.cam))
def proj(c, p):
    eye = v3(c['position']) * MM
    q = c['rotation']; R = Rotation.from_quat([q['x'], q['y'], q['z'], q['w']]).as_matrix()
    pc = R.T @ (np.asarray(p) - eye)
    th = math.tan(math.radians(22.5))
    x = pc[0] / -pc[2] / (th * ASPECT); y = pc[1] / -pc[2] / th
    return [round((x + 1) / 2 * 100, 1), round((1 - y) / 2 * 100, 1)]
worst = 0
for r, c in zip(d['frames'], cams):
    for kind in ('eyes', 'labels', 'insets'):
        for e in r[kind]:
            if e.get('ring'):
                p = proj(c, e['ring']); s = e['ring_screen_pct']
                dev = max(abs(p[0] - s[0]), abs(p[1] - s[1])); worst = max(worst, dev)
                print(f"[{r['frame']:03d}] {r['name']:10s} {kind[:-1]:6s} ring proj {p} stored {s} dev {dev:.1f}%")
    for a in r['arrows']:
        print(f"[{r['frame']:03d}] {r['name']:10s} arrow  tail {proj(c, a['tail'])} tip {proj(c, a['tip'])} (px {[round(v*14) for v in proj(c, a['tail'])[:1]]}, ...)")
    for a in r['lead_lines']:
        print(f"[{r['frame']:03d}] {r['name']:10s} line   tail {proj(c, a['tail'])} tip {proj(c, a['tip'])}")
print('worst ring deviation', worst)
