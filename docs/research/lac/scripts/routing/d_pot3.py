from pot_common import *
VIEWS_FLAT = [n for n in VIEWS if any(n == f'Step {k}' or n == f'Step {k}c' for k in range(30, 47))]
def ways(y=921.0, dyb=4.5):
    return {'tan': [[668.0, y - 4, 1560.0], [680.5, y - 1, 1530.0], [682.0, y, 1460.0], [681.5, y, 1400.0], [681.5, y, 1365.0], [682.5, y, 1352.0], [686.0, y - 0.5, 1341.0]],
            'red': [[668.0, y - 4, 1566.0], [684.5, y - 1, 1532.0], [684.5, y, 1460.0], [684.0, y, 1400.0], [684.0, y, 1365.0], [685.0, y, 1352.0], [691.5, y - 0.5, 1340.0]],
            'black': [[660.0, y - 5, 1556.0], [672.0, y, 1535.0], [682.5, y + dyb, 1505.0], [688.5, y + 2, 1465.0], [687.5, y + 0.5, 1400.0], [686.8, y + 0.5, 1365.0],
                      [687.5, y + 0.5, 1352.0], [694.5, y, 1341.0]]}
def report(L, views=VIEWS_FLAT):
    for a, b in (('red', 'black'), ('tan', 'black'), ('tan', 'red')):
        A, sa, _ = dense(L[a], 0.3); B, _, _ = dense(L[b], 0.3)
        d, k = cKDTree(B).query(A[25:-25]); j = int(np.argmin(d))
        print(f'  {a}/{b} gap {d[j] - 1.25:.2f} at {A[25 + j].round(1).tolist()}')
    print('  worst', worst(L, views))
if __name__ == '__main__':
    for y in (920.0, 921.0, 922.0):
        for dyb in (3.5, 4.5):
            print(y, dyb); report({c: plugged(c, w) for c, w in ways(y, dyb).items()})
