import sys
SP = __import__('os').path.dirname(__import__('os').path.abspath(__file__))
sys.path.insert(0, SP)
exec(open(SP + '/way42b.py').read().split("cands = {")[0])
from proj import project, SIZES
# where the held module's top (the plug) is on screen, to tell whether the A end shows above it
plug_top = np.array([[611.0, 1077.0, 1284.0]])
for k, (w, h, b) in SIZES.items():
    print(k, 'plug top on screen', project(plug_top, CAM, w, h).round(0).tolist())
def screen_extent(way, names, n=15):
    for s in range(len(way) - 1):
        ys = []
        for kk in np.linspace(0, 1, n):
            M = mix(way[s], way[s + 1], kk); P = VA @ M[:3, :3].T + M[:3, 3]
            q = project(P, CAM, 1000, 548); ys.append((q[:, 1].max(), q[:, 0].min(), q[:, 0].max()))
        print(f'   {names[s]:>10s}->{names[s + 1]:<10s} A end lowest screen y over the beat (1000): {min(y[0] for y in ys):.0f}..{max(y[0] for y in ys):.0f}')
c = {
 'N1': ([bench, at(RB, [597, 1000, 1399]), at(RB, [680, 1000, 1399]), at(RH, [680, 975, 1225]), at(RH, [646, 975, 1225]), at(RH, [646, 933, 1225]), [0, 0, 0]],
        ['bench', 'lifted', 'back', 'over', 'forward', 'lowered', 'seat']),
 'N2': ([bench, at(RB, [680, 1000, 1399]), at(RB, [680, 1000, 1300]), at(RH, [680, 975, 1225]), at(RH, [646, 975, 1225]), at(RH, [646, 933, 1225]), [0, 0, 0]],
        ['bench', 'up+back', 'across', 'over', 'forward', 'lowered', 'seat']),
 'N3': ([bench, at(RB, [597, 1000, 1399]), at(RB, [680, 1000, 1399]), at(RH, [680, 975, 1225]), at(RH, [646, 946, 1225]), [0, 0, 0]],
        ['bench', 'lifted', 'back', 'over', 'fwd+down', 'seat']),
}
for k, (way, names) in c.items():
    print('==', k); evaluate(way, names); screen_extent(way, names)
