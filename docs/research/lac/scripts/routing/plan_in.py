import time, json, sys
from planner import *
VIEW = 'Step 56c'
BOX = ([655.0, 886.0, 1222.0], [725.0, 951.0, 1342.0])
order = sys.argv[1].split(',') if len(sys.argv) > 1 else ['black', 'red', 'tan']
drops = {c: np.array([wire_at(POTL[c][0]) + [0, 14.0, 0], wire_at(POTL[c][0]) + [0, 2.0, 0]]) for c in POTL}
done = {}
t0 = time.time()
for c in order:
    cap, e, d = start(c, None) if False else (POTL[c][0], np.asarray(POTL[c][1], float), np.array([0.0, -1.0, 0.0]))
    a = e + d * 6.0; b = drops[c][0]
    extra = [(drops[o], 0.625) for o in POTL if o != c and o not in done] + [(done[o], 0.625) for o in done]
    F = Field(VIEW, BOX, skip=(cap,), extra=extra)
    print(c, 'field', round(time.time() - t0, 1), 's; clear at start', round(float(F.clear[F.idx(a)]), 2), 'at goal', round(float(F.clear[F.idx(b)]), 2), flush=True)
    path = astar(F, a, b, free_near=(a, b))
    if path is None:
        print(c, 'NO PATH'); continue
    ctl = controls_from(path)
    line = into_hole(cap, e, d, ctl)
    done[c] = line
    print(c, 'path', len(path), 'controls', ctl, round(time.time() - t0, 1), 's', flush=True)
    for v in ('Step 53c', 'Step 56c'):
        print('   ', v, clearance(v, line, 0.625, ends=('NAUO11', cap), wire=POTW))
print('mutual', mutual(done))
json.dump({c: controls_from(np.zeros((0, 3))) if False else None for c in []}, open('/dev/null', 'w'))
