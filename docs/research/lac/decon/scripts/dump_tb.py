"""Dump every toolbox item shown per viewer frame (raw fields), for reading."""
from lacpub import *
S = State()
frame = -1
prev = set()
for idx, sid in enumerate(order):
    s = steps[sid]
    S.apply(s)
    if s.get('behaviour') == 'hidden':
        continue
    frame += 1
    on = {k for k, t in S.tb.items() if t.get('visible')}
    new = on - prev
    for k in sorted(new, key=lambda k: S.tb[k].get('name') or ''):
        t = S.tb[k]
        ty = t.get('type')
        d = dict(type=ty, name=t.get('name'))
        for f in ('position', 'target_position', 'width', 'height', 'links', 'points', 'object_ids', 'object_local_positions', 'scale', 'body_width', 'head_width', 'head_length', 'leader_start_position'):
            if f in t: d[f] = t[f]
        if ty == 'image': d['src'] = ((t.get('content') or {}).get('src') or '').split('/')[-1].split('?')[0]
        if ty == 'editor': d['text'] = re.sub(r'<[^>]+>', '', t.get('editor_contents') or '')[:40]
        print(f"[{frame:03d}] {s['name']}: " + json.dumps(d)[:900])
    prev = on
