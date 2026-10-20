from design_common import *
a, b = wire_at('NAUO30'), wire_at('NAUO31')     # a12, (+) red
def arch(s, e, height, mid_shift=(0, 0, 0), lift=6.0):
    p1, p2 = s + [0, lift, 0], e + [0, lift, 0]
    mid = (p1 + p2) / 2 + np.asarray(mid_shift, float)
    body = W.smooth([p1, [mid[0], max(s[1], e[1]) + height, mid[2]], p2], start_dir=[0, 1, 0], end_dir=[0, -1, 0], spacing=0.5)
    return W.resample(W.join(W.straight(s, [0, 1, 0], lift), body, W.straight(p2, [0, -1, 0], lift)), 1.0)
best = []
for h in (8, 10, 12, 14, 16, 20, 24, 28):
    for dz in (-6, -3, 0, 3):
        line = arch(a, b, h, (0, 0, dz))
        worst = min(clearance(v, line, 0.625, ends=('NAUO30', 'NAUO31'), wire='jumper dark_red')[0] for v in ('Step 14c', 'Step 39c', 'Step 56c'))
        best.append((worst, h, dz))
best.sort(reverse=True)
print(best[:6])
