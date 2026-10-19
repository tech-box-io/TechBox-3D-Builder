from lacload import *
from scipy.spatial.transform import Rotation
import json
def fit(a, b, sub=None):
    if sub:
        A = np.vstack([V for mn, V, F in pieces(a) if mn == sub][:1]); B = np.vstack([V for mn, V, F in pieces(b) if mn == sub][:1])
    else:
        A = mesh(a)[0]; B = mesh(b)[0]
    R, t = kabsch(A, B)
    err = float(np.abs(A @ R.T + t - B).max())
    return R, t, err, A.mean(0)
def pose_of(R, t, c):
    rv = Rotation.from_matrix(R).as_rotvec(); ang = float(np.degrees(np.linalg.norm(rv)))
    newc = c @ R.T + t
    if ang < 1e-4:
        return [round(float(x), 3) for x in (newc - c)]
    ax = rv / np.linalg.norm(rv)
    return dict(t=[round(float(x), 3) for x in newc - c], r=[round(float(x), 6) for x in ax] + [round(ang, 4)], at=[round(float(x), 3) for x in c])
out = {}
for name, a, b, sub in [('F1_flat_beside', 'NAUO10', 'NAUO125', None), ('F1_flat_other_end', 'NAUO10', 'NAUO154', None), ('F1_hover_front', 'NAUO10', 'NAUO35', None),
                        ('pot_flat_beside', 'NAUO11', 'NAUO126', None), ('pot_flat_other_end', 'NAUO11', 'NAUO155', None),
                        ('knob_flat_other_end', 'NAUO13', 'NAUO156', None), ('nut_flat_beside', 'NAUO12', 'NAUO127', None), ('washer_flat_beside', 'NAUO146', 'NAUO153', None),
                        ('switch_flat_F4', 'NAUO46', 'NAUO51', None), ('switch_hover', 'NAUO46', 'NAUO144', None),
                        ('buzzer_lying', 'NAUO62', 'NAUO61', None),
                        ('lcd_standing_out', 'NAUO94', 'NAUO96', 'Kol_kov_ li_ta p__m_ kr_tk_ - 2,54mm_16.STEP'),
                        ('lcd_lying', 'NAUO94', 'NAUO95', 'Kol_kov_ li_ta p__m_ kr_tk_ - 2,54mm_16.STEP'),
                        ('pot_assembled_knob', 'NAUO13', 'NAUO9', 'LAC Knob')]:
    R, t, err, c = fit(a, b, sub)
    out[name] = pose_of(R, t, c)
    print(name, out[name], 'err', round(err, 4))
json.dump(out, open('poses.json', 'w'), indent=1)
