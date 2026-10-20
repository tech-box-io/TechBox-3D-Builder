from design_common import *
usb = cad_line('NAUO123'); EXIT = usb[0]; CDIR = unit(usb[3] - usb[0])
NOTCH = np.array([643.13, 899.6, 1339.3]); PRE = np.array([651.5, 900.8, 1343.0]); A_T = np.array([598.0, 884.61 + 4.3, NOTCH[2]])
def route(out, k=(-6.0, -1.0), run=16.0):
    start = EXIT + [0.0, 0.0, out]
    mid = W.smooth([start, PRE + [0, 0, out / 2], NOTCH, NOTCH + [k[0], k[1], 0.0], A_T + [run, 0.0, 0.0]], start_dir=CDIR, end_dir=[-1, 0, 0], spacing=0.5)
    return W.resample(W.join(mid, W.straight(mid[-1], [-1, 0, 0], run)), 1.0)
for k in ((-6.0, -1.0), (-5.0, -0.5), (-8.0, -2.0)):
    for run in (12.0, 16.0):
        r = [clearance(v, route(18.0 if v == 'Step 40' else 0.0, k, run), 1.75, ends=('NAUO122', 'USB_A'), wire='usb cable', end_mm=4.0) for v in ('Step 40', 'Step 40c', 'Step 55c', 'Step 56c')]
        L = route(0.0, k, run); print(k, run, [(round(a, 2), b) for a, b in r], 'end', L[-1].round(2).tolist(), 'A_T', A_T.round(2).tolist())
