import time
from planner import *
from eval_in import IN
VIEW = 'Step 52c'
FO = PATHS['poses']['F1_hover_front']
BOX = ([690.0, 886.0, 1215.0], [802.0, 951.0, 1275.0])
done, ctl_up = {}, {}
t0 = time.time()
for c in ('black', 'red', 'tan'):
    cap, e, d = start(c, FO)
    k = next(j for j, p in enumerate(IN[c]) if p[0] < 706.0)      # where the seated lead is inside the corridor
    entry = np.asarray(IN[c][k], float)
    a = e + d * 6.0
    extra = [(done[o], 0.625) for o in done]
    F = Field(VIEW, BOX, skip=(cap,), extra=extra)
    path = astar(F, a, entry, free_near=(a,))
    if path is None:
        print(c, 'NO PATH'); continue
    front = controls_from(path, every=10.0)
    ctl_up[c] = front + IN[c][k:]
    done[c] = into_hole(cap, e, d, ctl_up[c])
    print(c, 'entry', IN[c][k], 'front', front, round(time.time() - t0, 1), 's', flush=True)
    for v in ('Step 52c', 'Step 53'):
        print('   ', v, check(v, done[c], 0.625, ends=('NAUO11', cap), wire=POTW), clearance(v, done[c], 0.625, ends=('NAUO11', cap), wire=POTW))
print('mutual', mutual(done))
print('UP =', {c: [[round(x, 1) for x in p] for p in w] for c, w in ctl_up.items()})
