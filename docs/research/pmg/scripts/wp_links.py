"""Pass 4: each wire's two ends -> the caps they enter -> the pins those caps sit on. Prints a table, writes scratchpad links.json."""
import json, sys
import numpy as np
SP = '/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/bc7f208e-dd24-481f-9696-6a220688eb27/scratchpad/'
wires = json.load(open(SP + 'wires_raw.json'))
cp = json.load(open(SP + 'caps_pins.json'))
caps = cp['caps']

# every pin of every device pose: (device instance, pin name, tip)
pins = []
for inst, pp in cp['module_pins'].items():
    for name, p in pp.items():
        row, col = name.split()
        pins.append((inst, f'{col}{row[1:]}' if row.startswith('D') else f'{col} {row}', np.array(p)))
for inst, pp in cp['devices']['buttons'].items():
    for k, p in enumerate(pp):
        pins.append((inst, f'pin{k}', np.array(p)))       # named later from the wiring
for inst, pp in cp['devices']['displays'].items():
    for k, p in enumerate(pp):
        pins.append((inst, f'pin{k}', np.array(p)))
for inst, pp in cp['devices']['matrices'].items():
    for k, p in enumerate(pp):
        pins.append((inst, f'pin{k}', np.array(p)))


def cap_for(e):
    best = None
    for cid, c in caps.items():
        for face in ('face_plus', 'face_minus'):
            dd = np.linalg.norm(np.array(c[face]) - e)
            if best is None or dd < best[0]:
                best = (dd, cid, face)
    return best


def pin_for(cid):
    c = caps[cid]
    ctr, ax, half = np.array(c['centre']), np.array(c['axis']), c['length_mm'] / 2
    best = None
    for inst, name, p in pins:
        v = p - ctr
        along = v @ ax
        perp = np.linalg.norm(v - ax * along)
        if abs(along) <= half + 0.5 and perp < 1.0:
            if best is None or perp < best[0]:
                best = (perp, inst, name, along)
    return best


links = {}
for wid, w in wires.items():
    if w['radius_mm'] > 1.0:
        continue
    row = dict(mesh=w['mesh'], length_mm=w['length_mm'])
    for end in ('a', 'b'):
        e = np.array(w['end_' + end])
        dd, cid, face = cap_for(e)
        c = caps[cid]
        pin = pin_for(cid)
        row[end] = dict(cap=cid, cap_kind=c['kind'], gap_mm=round(float(dd), 2), wire_face=face,
                        device=pin[1] if pin else None, pin=pin[2] if pin else None,
                        pin_off_axis_mm=round(float(pin[0]), 2) if pin else None,
                        pin_tip_depth_mm=round(float(abs(np.array(c[face]) - (np.array(c['centre']) + np.array(c['axis']) * pin[3])) @ np.array(c['axis'])), 2) if pin else None)
    links[wid] = row
    print(f"{wid:8s} {w['mesh'][-22:]:22s} {w['length_mm']:7.1f}  a: {row['a']['cap']:8s} gap {row['a']['gap_mm']:4.2f} {str(row['a']['device']):7s} {str(row['a']['pin']):8s} | "
          f"b: {row['b']['cap']:8s} gap {row['b']['gap_mm']:4.2f} {str(row['b']['device']):7s} {str(row['b']['pin']):8s}")
json.dump(links, open(SP + 'links.json', 'w'), indent=0)
used = {}
for wid, r in links.items():
    for end in 'ab':
        used.setdefault(r[end]['cap'], []).append(wid)
print('caps used twice:', {k: v for k, v in used.items() if len(v) > 1})
print('caps not used by any wire:', sorted(set(caps) - set(used), key=lambda s: int(s[4:])))
