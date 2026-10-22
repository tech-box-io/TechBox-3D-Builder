"""The published LAC take-apart's camera on each frame, in our terms (read-only).

    python3 -I docs/research/lac/decon/scripts/published_cameras.py

Reads docs/research/lac/decon/published/raw/19075-lac_deconstruction.json. Cadasio's frame is our assembly frame (mm = scene units /
scaleFactor, as docs/research/lac/round1/published_motions.md found for the Full Build). Camera: cameraProperties.default_camera, then
each step's properties.default_camera (orderedSteps order, hidden steps included). Ours: view_dir = unit(position - orbit_target),
radius = distance x sin 22.5 deg / 1.08 (player/js/core.js, frame_padding 1.08). up = the camera's own up (its quaternion applied to
+Y): where it is not near +Y the published scene was turned (the report's "up-axis flipped")."""
import json, math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
j = json.load(open(ROOT / 'docs/research/lac/decon/published/raw/19075-lac_deconstruction.json'))
SF = j['assemblyStructure']['scaleFactor']
cam = dict(j['cameraProperties']['default_camera'])
v3 = lambda p: [p['x'] / SF, p['y'] / SF, p['z'] / SF]


def qrot(q, v):
    x, y, z, w = q['x'], q['y'], q['z'], q['w']
    ux, uy, uz = v
    tx, ty, tz = 2 * (y * uz - z * uy), 2 * (z * ux - x * uz), 2 * (x * uy - y * ux)
    return [ux + w * tx + (y * tz - z * ty), uy + w * ty + (z * tx - x * tz), uz + w * tz + (x * ty - y * tx)]


frame = -1
for sid in j['orderedSteps']:
    s = j['steps'][sid]
    c = (s.get('properties') or {}).get('default_camera')
    moved = bool(c)
    if c:
        cam.update(c)
    if s.get('hideInStepPicker') and s.get('behaviour') == 'play':
        hidden = True
    else:
        hidden = False
    frame += 1
    if not moved and frame:
        continue
    t, p = v3(cam['orbit_target']), v3(cam['position'])
    d = [a - b for a, b in zip(p, t)]
    n = math.sqrt(sum(x * x for x in d))
    dirv = [round(x / n, 4) for x in d]
    up = [round(x, 2) for x in qrot(cam['rotation'], [0, 1, 0])]
    print(f"[{frame:03d}] {s['name']:12s} target {[round(x, 1) for x in t]} dir {dirv} dist {n:.1f} -> radius {n * math.sin(math.radians(22.5)) / 1.08:.1f}"
          f"  up {up}")
