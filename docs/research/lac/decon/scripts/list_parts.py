"""List the published take-apart's top-level parts: name, solids, home box (our mm), and the viewer frames each is shown in."""
import sys, json
import numpy as np
from lacpub import *
S = State()
shown = collections.defaultdict(list)
frame = -1
for idx, sid in enumerate(order):
    s = steps[sid]
    S.apply(s)
    if s.get('behaviour') == 'hidden':
        continue
    frame += 1
    for t in TOPS:
        if S.visible_leaves(t):
            shown[t].append(frame)
def runs(fs):
    out=[]; 
    for f in fs:
        if out and f==out[-1][1]+1: out[-1][1]=f
        else: out.append([f,f])
    return ','.join(f'{a}-{b}' if a!=b else f'{a}' for a,b in out)
for t in TOPS:
    b = HOME.world_box(top_leaves[t], home=True)
    c = r2((b[0]+b[1])/2,1) if b else None
    sz = r2(b[1]-b[0],1) if b else None
    print(f"{NAME[t][:44]:44s} n={len(top_leaves[t]):3d} hid={int(refs[t]['hidden'])} c={c} size={sz} shown={runs(shown[t]) or '-'}")
print('nonleaf visible sets:', dict(S.nonleaf_visible))
print('stale ids:', len(S.stale))
