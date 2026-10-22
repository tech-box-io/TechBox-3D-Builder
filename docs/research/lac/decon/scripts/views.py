"""Summarise LAC steps.json views: name, kind, moving, path/paths/ride, camera, caption. Read-only."""
import json, sys
s = json.load(open(sys.argv[1]))
names = s['names']
for i, v in enumerate(s['views']):
    cam = v.get('camera') or {}
    mv = v.get('moving') or []
    extra = []
    for k in ('path', 'paths', 'ride', 'appear', 'flip', 'reappear', 'wiggle', 'single', 'arrows', 'inset', 'ghost', 'labels_done'):
        if v.get(k):
            val = v[k]
            if k in ('paths', 'ride') and isinstance(val, dict):
                val = {a: (b if len(json.dumps(b)) < 160 else json.dumps(b)[:160]) for a, b in val.items()}
            extra.append(f"{k}={json.dumps(val)[:300]}")
    print(f"[{i}] {v['name']} kind={v.get('kind')} moving={mv} cam=dir{cam.get('dir')} tgt{cam.get('target')} r{cam.get('radius')}")
    if extra: print('     ', ' | '.join(extra))
    if v.get('caption'): print('      cap:', v['caption'][:200])
