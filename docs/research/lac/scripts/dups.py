from lacload import *
from scipy.spatial.transform import Rotation
groups = {
 'F1': ['NAUO10', 'NAUO35', 'NAUO125', 'NAUO154'],
 'pot': ['NAUO11', 'NAUO36', 'NAUO126', 'NAUO155'],
 'knob': ['NAUO13', 'NAUO37', 'NAUO156'],
 'nut': ['NAUO12', 'NAUO38', 'NAUO127'],
 'washer': ['NAUO146', 'NAUO145', 'NAUO153'],
 'switch': ['NAUO46', 'NAUO51', 'NAUO144'],
 'buzzer': ['NAUO62', 'NAUO61'],
 'coin': ['NAUO4', 'NAUO5'],
 'F7': ['NAUO42', 'NAUO43'],
 'resistor': ['NAUO6', 'NAUO7'],
}
for g, names in groups.items():
    A = mesh(names[0])[0]
    for n in names[1:]:
        B = mesh(n)[0]
        if len(A) != len(B):
            print(g, names[0], '->', n, 'vertex counts differ', len(A), len(B)); continue
        R, t = kabsch(A, B)
        err = np.abs(A @ R.T + t - B).max()
        rv = Rotation.from_matrix(R).as_rotvec(); ang = np.degrees(np.linalg.norm(rv))
        ax = rv / np.linalg.norm(rv) if ang > 1e-6 else np.zeros(3)
        c = A.mean(0)
        print(f"{g}: {names[0]} -> {n}: turn {ang:.2f} deg about {ax.round(4)}, centre moves {(c @ R.T + t - c).round(2)}, err {err:.4f}")
