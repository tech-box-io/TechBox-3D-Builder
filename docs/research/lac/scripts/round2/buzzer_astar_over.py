import json, sys
import numpy as np
import astar as A
import design as D
# the ways round the board closed: behind row j and in front of the rails, between the board's end and the Nano Board
X, Z = A.G[..., 0], A.G[..., 2]
band = (Z > 1262.0) & (Z < 1326.0)
A.UNDER = A.UNDER | (band & ((X < 663.5) | (X > 698.5)))
every = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0
need = float(sys.argv[2]) if len(sys.argv) > 2 else 0.35
out = {}
start = {c: np.add(D.EXIT[c], [0.0, -D.SEAT_OUT, 0.0]) for c in ('red', 'black')}
goal = {c: D.wire_at(D.CAP[c]) + [0.0, 4.0 + D.ABOVE[c], 0.0] for c in ('red', 'black')}
clear = A.CLEAR
for c in sys.argv[3].split(',') if len(sys.argv) > 3 else ('red', 'black'):
    p = A.search(start[c], goal[c], clear, need=need)
    if p is None:
        print(c, 'NO PATH', flush=True); continue
    ctl = A.controls(p, every=every)
    out[c] = ctl
    line = D.seated_line(c, ctl)
    np.save(f'path_{c}.npy', p)
    print(c, 'path pts', len(p), 'controls', len(ctl), 'line len %.1f' % np.linalg.norm(np.diff(line, axis=0), axis=1).sum(),
          'max y %.1f' % line[:, 1].max(), 'min y %.1f' % line[:, 1].min(), flush=True)
    print('  raw path every ~4 mm:', [q.round(1).tolist() for q in p[::5]], flush=True)
    clear = A.wire_clear(line)
json.dump(out, open('astar_over_ctrl.json', 'w'))
print(json.dumps(out))
