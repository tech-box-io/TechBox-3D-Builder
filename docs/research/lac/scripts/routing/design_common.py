from harness import *
def unit(v):
    v = np.asarray(v, float); return v / np.linalg.norm(v)
def cad_line(key):
    return np.asarray(PATHS['lines'][key]['pts'], float)
CAPS = PATHS['caps']
def wire_at(cap): return np.asarray(CAPS[cap]['wire_at'], float)
def into_hole(cap, start, start_dir, controls, lift=6.0, above=10.0):
    top = wire_at(cap) + [0.0, 4.0 + above, 0.0]
    first = np.asarray(start, float) + unit(start_dir) * lift
    body = W.smooth([first, *[np.asarray(c, float) for c in controls], top], start_dir=unit(start_dir), end_dir=[0, -1, 0], spacing=0.5)
    return W.resample(W.join(W.straight(start, start_dir, lift), body, W.straight(top, [0, -1, 0], above + 4.0)), 1.0)
