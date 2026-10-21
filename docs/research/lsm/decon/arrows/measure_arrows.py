"""Every red arrow a published Cadasio guide shows, frame by frame, in millimetres.

    python -I measure_arrows.py <payload.json> <out.txt> [title] [--json <out.json>]

<payload.json> is what the public viewer endpoint returns for a guide (tools/cadasio/digest.py's header):
    https://api.cadasio.com/api/getProjectViewer?id=<guide id>&withSteps=true&hostname=instructions.online

How Cadasio stores an arrow (read from the PMG and LSM take-aparts, 21 Oct 2026):
  * toolboxComponentsProperties[<id>] with type 'arrow', sub_type 'straight': `points` (2 points, scene units, world space; the tail
    first, the tip of the head last), `body_width`, `head_width`, `head_length` (in the arrow's own units, typically 5 : 20 : 17),
    `scale` (a per-arrow factor on those three), `arrow_quaternion` (a roll about the arrow's own axis: the way its flat face looks),
    `object_ids` (the solid under the cursor when it was placed, then a non-CAD id) and `object_local_positions`, `visible` (false:
    the project's default).
  * A step's `properties[<arrow id>]` holds changes on top of the step before in `orderedSteps` (hidden steps included), as for parts:
    `visible` true / false (null: unchanged), and sometimes `points` (moved).
  * mm = scene units / assemblyStructure.scaleFactor. So:
        length       L = |points[-1] - points[0]| / SF            (tail to tip, the head included)
        shaft width  w = body_width * scale / SF
        head         head_width * scale / SF  x  head_length * scale / SF
  * The part named is the top-level component (child of the assembly root) holding object_ids[0]; Cadasio does not tie the arrow
    to it in any other way (the LSM's stems arrow sits on a lens plate's solid).
Frames are numbered as the viewer shows them: hidden steps skipped, Start = 0 (as docs/research/pmg/deconstruction/published_arrows.txt).
Direction words: an axis is named where it carries more than 0.35 of the unit direction (tools/cadasio/digest.py's axis_word).
"""
import json, sys, math

args = sys.argv[1:]
js_out = None
if '--json' in args:
    k = args.index('--json'); js_out = args[k + 1]; del args[k:k + 2]
src, out = args[0], args[1]
title = args[2] if len(args) > 2 else 'Published take-apart'
j = json.load(open(src))
steps, order, tcp, A = j['steps'], j['orderedSteps'], j['toolboxComponentsProperties'], j['assemblyStructure']
SF = A.get('scaleFactor') or 1.0

refs = {}
def walk(n, parent):
    r = n['rootReference']
    refs[r['id']] = dict(name=r['name'], parent=parent)
    for c in n.get('children') or []:
        walk(c, r['id'])
walk(A, None)
root = A['rootReference']['id']
def top_name(k):
    if k not in refs: return '?'
    while refs[k]['parent'] not in (None, root):
        k = refs[k]['parent']
    return refs[k]['name'].split('/')[-1]

def v3(p): return [float(p.get('x', 0)), float(p.get('y', 0)), float(p.get('z', 0))]
def axis_word(v):
    n = math.sqrt(sum(c * c for c in v))
    if n < 1e-9: return 'none'
    names = [('+X', '-X'), ('+Y (up)', '-Y (down)'), ('+Z', '-Z')]
    return ' & '.join(names[i][0 if v[i] > 0 else 1] for i in range(3) if abs(v[i]) / n > 0.35)
def num(x):                                   # (2 decimals, trailing zeros dropped to one: 8.0, 6.9, 5.22)
    return str(round(x, 2))

tb = {k: dict(v) for k, v in tcp.items()}
for t in tb.values(): t.setdefault('visible', False)
lines = [f'{title}: every arrow shown, frame by frame (length, shaft width, head width, head length, mm)']
rows = []
frame = -1
for idx, sid in enumerate(order):
    s = steps[sid]
    for k, p in (s.get('properties') or {}).items():
        if k in tb and isinstance(p, dict):
            for a, b in p.items():
                if a == 'visible' and b is None: continue
                tb[k][a] = b
    if s.get('behaviour') == 'hidden':
        continue
    frame += 1
    shown = [(k, t) for k, t in tb.items() if t.get('type') == 'arrow' and t.get('visible')]
    if not shown:
        continue
    items = []
    for k, t in sorted(shown, key=lambda kt: kt[1].get('name') or ''):
        p0, p1 = v3(t['points'][0]), v3(t['points'][-1])
        d = [b - a for a, b in zip(p0, p1)]
        L = math.sqrt(sum(c * c for c in d)) / SF
        sc = float(t.get('scale') or 1.0)
        w, hw, hl = (float(t.get(f)) * sc / SF for f in ('body_width', 'head_width', 'head_length'))
        oid = t.get('object_ids') or []
        oid = list(oid.values()) if isinstance(oid, dict) else list(oid)
        part = top_name(oid[0]) if oid else '?'
        items.append(f'L {L:.1f} w {num(w)} head {hw:.1f}x{hl:.1f} {axis_word(d)} on {part}')
        rows.append(dict(frame=frame, order_index=idx, step=s['name'], arrow=t.get('name'), id=k, part=part, length_mm=round(L, 2),
                         shaft_mm=round(w, 3), head_w_mm=round(hw, 2), head_l_mm=round(hl, 2), dir=[round(c / (L * SF), 4) for c in d],
                         tail_mm=[round(c / SF, 2) for c in p0], tip_mm=[round(c / SF, 2) for c in p1],
                         body=t.get('body_width'), head=[t.get('head_width'), t.get('head_length')], scale=sc,
                         words=axis_word(d), duration=s.get('animationDuration'), behaviour=s.get('behaviour')))
    lines.append(f'[{frame:03d}] {s["name"]:<12s} ' + ' | '.join(items))
open(out, 'w').write('\n'.join(lines) + '\n')
if js_out:
    json.dump(dict(source=src.split('/')[-1], scale_factor=SF, arrows=rows), open(js_out, 'w'), indent=1)
print(f'{len(rows)} arrow showings in {len(lines) - 1} frames -> {out}')
