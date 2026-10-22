"""Markdown tables from published_geometry.json (cameras, arrows, eyes, labels, close-ups, lead lines), for published_geometry.md."""
import json, math, re
from pathlib import Path
d = json.load(open(Path(__file__).resolve().parents[1] / 'published_geometry.json'))
F = d['frames']
def step_of(r):
    # the numbered step a frame belongs to (transitions: the Step N before them); fix the two misnamed frames
    return r['name']
fmt = lambda v, n=2: '(' + ', '.join(f'{x:.{n}f}' for x in v) + ')'
print('### Cameras\n')
print('| frame | step (published) | view_dir | target | distance | radius | el / az | up | in the seated frame of the copy shown alone |')
print('|---|---|---|---|---|---|---|---|---|')
for r in F:
    if not r['camera_moves']: continue
    c = r['camera']
    up = 'world +y' if (c['up_axis'] in (None, '+y')) else f"{c['up_axis']} (roll {c['roll_deg_from_world_up']:+.0f} deg)"
    s = c.get('in_seated_frame_of')
    ss = f"{s['seated']}: view_dir {fmt(s['view_dir'], 4)}, target {fmt(s['target'], 1)} (el {s['elevation']}, az {s['azimuth']}, roll {s['roll_deg_from_world_up']:.0f})" if s else ''
    print(f"| {r['frame']:03d} | {r['name']} | {fmt(c['view_dir'], 4)} | {fmt(c['target'], 1)} | {c['distance']:.1f} | **{c['radius']:.1f}** | {c['elevation']} / {c['azimuth']} | {up} | {ss} |")
print('\n### Arrows\n')
print('| frame | step | placed on (solid under the cursor) | dir | tail (mm) | tip (mm) | L | shaft w | head w x l | `dims=` | travel after | L / travel |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|')
for i, r in enumerate(F):
    for a in r['arrows']:
        # the travel that follows: the first move in the next frames before the next instruct frame
        trav = []
        for q in F[i + 1:]:
            if q['kind'] == 'N' or (q['name'].startswith('Step') and q['arrows']): break
            for m in q['moved']:
                if not m['ours'] or m['ours'].startswith(('wire', 'cap')): continue
                trav.append((m['part'], m['step_move_len'], m['step_turn_deg']))
        tv = '; '.join(f"{p} {l:.1f}" + (f" ({t:.1f} deg)" if t > 0.5 else '') for p, l, t in trav[:3]) or 'none (cross-fade)'
        main = max([l for _, l, _ in trav] or [0])
        ratio = f"{a['length'] / main:.2f}" if main > 1 else ''
        dv = a['dir']; ax = max(range(3), key=lambda k: abs(dv[k])); word = ('+' if dv[ax] > 0 else '-') + 'xyz'[ax]
        print(f"| {r['frame']:03d} | {r['name']} | {a['placed_on'][0].split(' / ')[-1]} | {word} {fmt(dv, 3)} | {fmt(a['tail'])} | {fmt(a['tip'])} | {a['length']:.1f} | {a['shaft_w']:.2f} | {a['head'][0]:.1f} x {a['head'][1]:.1f} | ({a['dims'][0]}, {a['dims'][1]}) | {tv} | {ratio} |")
print('\n### Eyes\n')
print('| frame | step | ring (leader end, our mm) | on (our id / Cadasio part) | icon at (x %, y %) | ring on screen |')
print('|---|---|---|---|---|---|')
seen = set()
for r in F:
    for e in r['eyes']:
        key = (e['name'], tuple(e['ring']))
        if key in seen: continue
        seen.add(key)
        on = e['on'].split(' / solid')[0]
        print(f"| {r['frame']:03d} | {r['name']} | {fmt(e['ring'])} | {on} | {fmt(e['screen_pct'], 1)} | {fmt(e['ring_screen_pct'], 1)} |")
print('\n### Labels, close-ups, lead lines\n')
for r in F:
    for e in r['labels']:
        print(f"- [{r['frame']:03d}] {r['name']}: label \"{e['text']}\" at {fmt(e['screen_pct'], 1)} %, leader ring {fmt(e['ring'])} on {e['on'].split(' / solid')[0]}")
    for e in r['insets']:
        print(f"- [{r['frame']:03d}] {r['name']}: close-up picture {e['src']} at {fmt(e['screen_pct'], 1)} %, {e['width_pct']} % wide (h/w {e['height_over_width']}), leader to {fmt(e['ring'])} on {e['on'].split(' / solid')[0]}")
    for e in r['lead_lines']:
        print(f"- [{r['frame']:03d}] {r['name']}: lead line {fmt(e['tail'])} -> {fmt(e['tip'])}, {e['length']:.1f} mm")
