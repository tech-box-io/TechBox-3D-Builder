"""Print published_geometry.json compactly (for reading)."""
import json, sys
from pathlib import Path
d = json.load(open(Path(__file__).resolve().parents[1] / 'published_geometry.json'))
want = set(sys.argv[1:])
for r in d['frames']:
    if want and r['name'] not in want and str(r['frame']) not in want:
        continue
    c = r['camera']
    print(f"[{r['frame']:03d}] {r['name']} ({r['kind']}, {r['duration_ms']} ms)" + (
        f"  CAM dir {c['view_dir']} target {c['target']} dist {c['distance']} -> radius {c['radius']} (el {c['elevation']} az {c['azimuth']}) up_axis {c['up_axis']} roll {c.get('roll_deg_from_world_up')} camup {c.get('camera_up')}" if r['camera_moves'] else ''))
    for a in r['arrows']:
        print(f"   ARROW {a['name']}: tail {a['tail']} tip {a['tip']} L {a['length']} w {a['shaft_w']} head {a['head']} dir {a['dir']} on {a['placed_on']} anchors {a.get('points_vs_anchors_mm')}")
    for e in r['eyes']:
        print(f"   EYE {e['name']}: ring {e['ring']} on {e['on']} screen {e['screen_pct']} ring@ {e['ring_screen_pct']}")
    for e in r['insets']:
        print(f"   INSET {e['name']} {e['src']}: target {e['ring']} on {e['on']} screen {e['screen_pct']} w {e['width_pct']} h/w {e['height_over_width']}")
    for e in r['labels']:
        print(f"   LABEL '{e['text']}': ring {e['ring']} on {e['on']} screen {e['screen_pct']} ring@ {e['ring_screen_pct']}")
    for e in r['lead_lines']:
        print(f"   LINE {e['name']}: {e['tail']} -> {e['tip']} L {e['length']} anchors {e.get('points_vs_anchors_mm')} {e.get('tail_by_anchor','')} {e.get('tip_by_anchor','')}")
    for m in r['moved']:
        print(f"   MOVED {m['part']} [{m['ours']}]: step {m['step_move']} ({m['step_move_len']}) turn {m['step_turn_deg']} | pose {m['pose']} screw {m.get('screw')} step_screw {m.get('step_screw')} rel {m.get('rel_to')}")
    for m in r['appear']:
        print(f"   APPEAR {m['part']} [{m['ours']}] {m.get('solids')} pose {m.get('pose')} screw {m.get('screw')} rel {m.get('rel_to')}")
    if r['disappear']:
        print(f"   GONE {[m['part'] for m in r['disappear']]}")
    if r.get('parts_with_solids_apart'):
        print(f"   SPLIT {r['parts_with_solids_apart']}")
