"""published_steps.json as a plain listing, frame by frame (like ../arrows/published_arrows.txt).

    .venv.nosync/bin/python -I docs/research/lsm/decon/published/make_table.py     (after replay_decon.py)
Writes docs/research/lsm/decon/published/published_steps.txt.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
d = json.load(open(HERE / 'published_steps.json'))


def p3(v, n=1):
    return '(' + ', '.join(f'{x:.{n}f}' for x in v) + ')'


def pose(p):
    if p is None:
        return ''
    if isinstance(p, dict):
        return f"turned({p3(p['r'][:3], 3)}, {p['r'][3]:.1f}, at={p3(p['at'])}, t={p3(p['t'])})"
    return p3(p) if isinstance(p, list) else str(p)


def part(e):
    s = e.get('ours') or e.get('cadasio')
    if e.get('cadasio') and e.get('ours') and ('copy' in e['ours'] or e['ours'].startswith(('wire', 'lead', 'usb', 'J_', 'BTN'))):
        s += f" [{e['cadasio'].replace('^LSM Lab - Chapter 2-1', '')}]"
    return s


L = ['Published LSM take-apart (Cadasio 19075), replayed in our terms: our ids, our assembly mm (Y up).',
     'camera: view_dir (target -> camera), target, radius = distance * sin(22.5 deg) / 1.08 (our cameraPose); "same" = as the step before.',
     'pose = from our seated part (stepgen turned(): axis, degrees, at, t); move = box-centre displacement since the step before.',
     'Wire bodies and jumper caps have no seated twin: their boxes are given. See published_steps.json for every number.', '']
for r in d['steps']:
    c = r['camera']
    cam = (f"view_dir {p3(c['view_dir'], 4)}  target {p3(c['target'])}  radius {c['radius']:.1f}  (distance {c['distance']:.0f}, "
           f"elevation {c['elevation']:.0f}, azimuth {c['azimuth']:.0f})") if r['camera_moves'] else 'same'
    L.append(f"[{r['frame']:02d}] {r['name']:<14s} {r['kind']:<10s} camera {cam}")
    for a in r['arrows']:
        L.append(f"      arrow   tail {p3(a['tail_mm'])} -> tip {p3(a['tip_mm'])}  L {a['length_mm']:.1f}  w {a['shaft_mm']:.2f}")
    for e in r['eyes']:
        L.append(f"      eye     on {e['on']['ours']} ({e['on']['solid'][-30:]}) at {p3(e['ring_mm'])}; icon at {e['screen_pos_pct']['x']:.0f} %, "
                 f"{e['screen_pos_pct']['y']:.0f} % of the view" + (' (boxed)' if e['framed'] == 'rectangle' else ''))
    for e in r['insets']:
        L.append(f"      close-up ring on {e['on']['ours']} at {p3(e['ring_mm'])}; picture {e['src']} ({e['width_pct']} % wide, h/w "
                 f"{e['aspect_h_over_w']}) at {e['screen_pos_pct']['x']:.0f} %, {e['screen_pos_pct']['y']:.0f} %")
    for e in r.get('title_images', []):
        L.append(f"      title image {e['src']} ({e['width_pct']} % wide, h/w {e['aspect_h_over_w']}) at {e['screen_pos_pct']}")
    for e in r['appear']:
        extra = f"  pose {pose(e.get('pose_from_built'))}" if e.get('pose_from_built') not in (None, [0.0, 0.0, 0.0]) else ''
        box = f"  box {p3(e['box_mm'][0])} - {p3(e['box_mm'][1])}" if (e.get('box_mm') and e.get('pose_from_built') is None) else ''
        pin = f"  pin tip {p3(e['pin_tip_mm'])} pointing {p3(e['pin_dir'])}" if e.get('pin_tip_mm') else ''
        L.append(f"      +  {part(e)}{extra}{box}{pin}" + (f"  ({e['what']})" if e.get('what') else ''))
    for e in r['disappear']:
        f = e.get('faded_at')
        L.append(f"      -  {part(e)}" + (f"  (moved as it fades: pose {pose(f.get('pose_from_built'))})" if f else ''))
    for e in r['partial_visibility_change']:
        L.append(f"      ~  {e['ours'] or e['cadasio']}: {e['solids_before']} -> {e['solids_now']} of {e['of']} solids shown")
    for e in r['moved']:
        L.append(f"      >  {part(e)} moves {p3(e['step_move_mm']) if isinstance(e['step_move_mm'], list) else e['step_move_mm']} "
                 f"({e['step_move_dist']} mm" + (f", turn {e['step_turn_deg']} deg" if isinstance(e.get('step_turn_deg'), float) and e['step_turn_deg'] > 0.1 else '')
                 + ')' + (f"  now {pose(e.get('pose_from_built'))}" if e.get('pose_from_built') not in (None, [0.0, 0.0, 0.0]) else ''))
    sh = r['shown']
    L.append(f"      shown: {', '.join(sh['ours'])}" + (f"; {sh['stems']} stems" if sh['stems'] else ''))
L += ['', 'Glitches of the published guide (not to be copied):'] + [f'  - {g}' for g in d['meta']['glitches']]
L += ['', 'Checks: ' + d['meta']['checks']['arrows']]
(HERE / 'published_steps.txt').write_text('\n'.join(L) + '\n')
print(len(L), 'lines ->', HERE / 'published_steps.txt')
