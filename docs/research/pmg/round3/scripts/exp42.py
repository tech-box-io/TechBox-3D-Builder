"""Step 42: try ways for the USB A end (after the module is held over H4) against the wires and parts there, and the caption box."""
import sys, json, pickle, time
import numpy as np
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import probe
from proj import project, SIZES
t0 = time.time()
ns = probe.load(marker='g.place("Pick up the I/O module')
print('loaded', round(time.time() - t0), 's')
G = ns['GEO']; USB_A = ns['USB_A']; MODULE_HELD = ns['MODULE_HELD']
model = ns['g'].model
held = {w: np.asarray(p, float) for w, p in ns['_held_lines'].items()}
scene = ns['on_screen'](MODULE_HELD, {**ns['SEATED'], ns['DISPLAY']: ns['DISPLAY_BENCH'], ns['MATRIX']: ns['MATRIX_BENCH']}, case=ns['CASE_ALL'])
out = dict(held=held, scene=[(p, pose) for p, pose in scene], table_y=G.get('table_y'), bench_y=G.get('bench_y'),
           usb=G['usb'], mid_a=G['parts'][USB_A]['middle'], USB_A_BENCH=ns['USB_A_BENCH'], MODULE_HELD=MODULE_HELD,
           final_cable=np.asarray(ns['usb_cable'](MODULE_HELD, None)['usb cable']['pts'], float),
           bench_cable=np.asarray(ns['_held_cable_bench']['pts'], float))
pickle.dump(out, open(__import__('tempfile').gettempdir() + '/held42.pkl', 'wb'))
print('table', G.get('table_y'), 'bench', G.get('bench_y'), 'A bench', ns['USB_A_BENCH'])
print('scene', [p for p, _ in scene])
