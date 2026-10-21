import sys
sys.argv = ['x', 'Step 45']
exec(open('/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/lac/scripts/round2/f9/f9check.py').read().split("ways = {")[0])
f3m = posed[F3]
def pen(M, mesh=f3m):
    pts = samples @ M[:3, :3].T + M[:3, 3]
    b = mesh.bounds
    sel = np.all((pts >= b[0] - 0.01) & (pts <= b[1] + 0.01), axis=1)
    if not sel.any(): return 0.0, None
    d = trimesh.proximity.signed_distance(mesh, pts[sel])
    j = int(np.argmax(d))
    return float(d[j]), pts[sel][j]
for k in (0.6, 0.8):
    d, p = pen(mix(HOOKED, ZERO, k)); print('published swing at', k, round(d, 2), None if p is None else p.round(2))
print('F3 watertight', f3m.is_watertight, 'F9 watertight', model.inst[F9].is_watertight)
R = Rotation.from_rotvec(np.radians(25.79) * np.array([0, 0, -1.0])).as_matrix()
best = []
for dx in np.arange(-4.0, 1.01, 0.5):
    for dy in np.arange(-4.0, 1.01, 0.5):
        Q = np.array(P) + [dx, dy, 0.0]
        t = (np.eye(3) - R) @ (np.array(P) - Q)
        HQ = turned([0, 0, -1], 25.79, Q.tolist(), t=t.tolist())
        worst = max(pen(mix(HQ, ZERO, k))[0] for k in np.linspace(0.05, 0.95, 10))
        best.append((round(worst, 2), round(dx, 2), round(dy, 2)))
best.sort()
print('best pivots (penetration, dx, dy):', best[:12])
