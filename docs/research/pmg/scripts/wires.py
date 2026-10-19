"""PMG: the 21 jumper wires of the published guide, pose by pose, in the Cadasio project and in pmg.glb.

    .venv.nosync/bin/python docs/research/pmg/scripts/wires.py

1. Cadasio: for each wire step (Step N / Step Nc) the components that appear and disappear (token wire + 2 caps at Step N;
   routed wire + 2 caps at Step Nc), the two pin labels of Step N, and each wire's displayed colour. Every later pose of the
   same wire is found by its colour (each of the 21 wires has its own colour), every later pose of a cap by the pin it is on.
2. Pins: a cap is named by the pin it sits on: the I/O module's G/V/S columns and D0-D13 rows from the header meshes of
   NAUO1 (suffix _N = G, _R = V, _B = S: docs/research/mra/cad_pins.md), the push button's VCC/OUT/GND from its sockets,
   and the display's and matrix's pins from the caps that appear in Steps 16c-24c.
3. GLB: every wire body's attached caps (a cap whose box is within 0.6 mm of a wire vertex), read through a memory map.
Writes work/cadasio_map/wires.json.
"""
import json, mmap, struct, sys, collections, math
import numpy as np
ROOT = '/Users/lee-johnson/Desktop/Claude_Cadasio'
sys.path.insert(0, ROOT + '/tools')
from glbio import node_matrix, COMPONENT, NCOMP
W = ROOT + '/docs/research/pmg/scripts/work/cadasio_map'
T = {t['id']: t for t in json.load(open(W + '/cadasio_tree.json'))['tops']}
TN = {t['name']: t for t in T.values()}
R = json.load(open(W + '/replay.json'))
G = json.load(open(W + '/glb_boxes.json'))
D = json.load(open(ROOT + '/docs/research/pmg/cadasio/19075-piano_memory_game_pmg-full_build.json'))['steps']
V = R['viewer']; VN = {v['name']: v['v'] for v in V}
visible = [set() for _ in V]
for cid, r in R['tops'].items():
    for v in r['vis']: visible[v].add(cid)


def centre(b): return (np.array(b['min']) + np.array(b['max'])) / 2


def name(cid): return T[cid]['name']


def colour(cid):
    c = R['tops'][cid]['colours']
    return c[0][0] if c else None


def is_cap(n): return n.startswith('Wire Cap')


# ---------- pins ----------
def inv(M):
    M = np.array(M); Ri = M[:3, :3].T
    out = np.eye(4); out[:3, :3] = Ri; out[:3, 3] = -Ri @ M[:3, 3]
    return out


def to_local(M, p): return (inv(M) @ np.append(p, 1))[:3]


def to_world(M, p): return (np.array(M) @ np.append(p, 1))[:3]


# shield pins, per copy, in world mm, from that copy's own header boxes (suffix _N = G, _R = V, _B = S) and its power jack
# (the jack is at the USB end, where the rows are AREF, GND, 13, 12; RX0 is at the far end)
ORDER = ['AREF', 'GND', '13', '12', '11', '10', '9', '8', '7', '6', '5', '4', '3', '2', 'TX1', 'RX0']
COLS = {'_N': 'G', '_R': 'V', '_B': 'S'}


def pins_from_boxes(headers, board, jack):
    """headers: [(suffix, lo, hi)] of the four-pin headers; board: (lo, hi) of the PCB; jack: centre of the power jack."""
    blo, bhi = map(np.array, board); axis = int(np.argmin(bhi - blo))              # the pin axis is the board's normal
    bc = (blo + bhi) / 2
    pts = []
    for suf, lo, hi in headers:
        lo = np.array(lo); hi = np.array(hi); d = hi - lo
        others = [i for i in range(3) if i != axis]
        row = max(others, key=lambda i: d[i]); colax = min(others, key=lambda i: d[i])
        top = hi[axis] if abs(hi[axis] - bc[axis]) > abs(lo[axis] - bc[axis]) else lo[axis]
        for k in range(4):
            q = (lo + hi) / 2; q[axis] = top; q[row] = lo[row] + 1.27 + 2.54 * k
            pts.append((COLS[suf], q, row))
    row = pts[0][2]
    allc = np.mean([q[row] for _, q, _ in pts]); sgn = 1 if jack[row] > allc else -1
    out = {}
    for c in 'GVS':
        qs = sorted([q for cc, q, _ in pts if cc == c], key=lambda q: -sgn * q[row])
        for nm, q in zip(ORDER, qs):
            out[c + nm if nm[0].isdigit() else c + '-' + nm] = (q, axis)
    return out


SHIELD_PINS = {}
for k in ('NAUO1', 'NAUO78', 'NAUO94'):
    ms = G[k]['meshes']
    hd = [(m['name'][-2:], m['min'], m['max']) for m in ms if m['name'].startswith('Samtec-TLW-104-01-F-S') and m['name'][-2:] in COLS]
    bd = [(m['min'], m['max']) for m in ms if m['name'] == 'Shield_Arduino NANO'][0]
    jk = [centre(m) for m in ms if m['name'] == 'User Library-PJ-002AH_Body'][0]
    SHIELD_PINS[k] = pins_from_boxes(hd, bd, jk)
for n in ('Ensamblaje_Shield_NANO-1', 'Ensamblaje_Shield_NANO-2', 'Ensamblaje_Shield_NANO-3'):
    subs = collections.defaultdict(list)
    for x in TN[n]['solids']: subs[x['sub']].append(x)
    def ub(v): return [min(x['min'][i] for x in v) for i in range(3)], [max(x['max'][i] for x in v) for i in range(3)]
    hd = []
    for sb, v in subs.items():
        if sb and sb.startswith('Samtec-TLW-104-01-F-S') and sb.rsplit('-', 1)[0][-2:] in COLS:
            lo, hi = ub(v); hd.append((sb.rsplit('-', 1)[0][-2:], lo, hi))
    brd = [x for x in TN[n]['solids'] if x['sub'] is None and x['name'].startswith('Shield_Arduino')]
    bd = ub(brd) if brd else None
    if bd is None:   # the board solid: the thinnest big solid at depth 1
        cand = [x for x in TN[n]['solids'] if x['sub'] is None]
        x = max(cand, key=lambda x: (np.array(x['max']) - np.array(x['min'])).prod() / max(1e-6, min(np.array(x['max']) - np.array(x['min']))))
        bd = (x['min'], x['max'])
    lo, hi = ub(subs['User Library-PJ-002AH-1']); jk = (np.array(lo) + np.array(hi)) / 2
    SHIELD_PINS[n] = pins_from_boxes(hd, bd, jk)


def shield_pin(part, c, tol=1.3):
    best = None
    for nm, (q, ax) in SHIELD_PINS[part].items():
        d = c - q; along = d[ax]; d2 = d.copy(); d2[ax] = 0
        if abs(along) < 14 and np.linalg.norm(d2) < tol and (best is None or np.linalg.norm(d2) < best[0]): best = (np.linalg.norm(d2), nm)
    return best[1] if best else None


MOD_PINS = {}      # kind -> {pin: local point}, filled from the published caps of Steps 3c-24c


def kind_of(part, cadasio):
    if cadasio: return part.rsplit('-', 1)[0]
    nm = G[part]['meshes'][0]['name']
    for m in G[part]['meshes']:
        if m['name'].startswith('Socket_Blok'): return 'Big Button Module'
        if m['name'].startswith('Display TM1637'): return 'Display TM1637'
        if m['name'].startswith('8x female'): return 'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219'
    return nm


def box_dist(c, b, pad=0.0):
    lo = np.array(b['min']) - pad; hi = np.array(b['max']) + pad
    return float(np.linalg.norm(np.maximum(0, np.maximum(lo - c, c - hi))))


def rigid(n): return not (n.startswith(('Part', 'Copy', 'Wire Cap')) or ' to ' in n)


def where(c, cadasio=True):
    """what a cap centred at c sits on: (part, pin name or None)."""
    items = [(t['name'], t) for t in T.values() if t['min'] and rigid(t['name'])] if cadasio else \
            [(k, b) for k, b in G.items() if rigid(b['meshes'][0]['name'])]
    near = sorted((box_dist(c, b, 0), float(np.prod(np.array(b['max']) - np.array(b['min']))), n) for n, b in items if box_dist(c, b, 6) == 0)
    for _, _, n in near:
        if n in SHIELD_PINS:
            p = shield_pin(n, c)
            if p: return n, p
        k = kind_of(n, cadasio)
        if k in MOD_PINS:
            M = (TN[n] if cadasio else G[n])['matrix_mm']; pl = to_local(M, c)
            d, pn = min((float(np.linalg.norm(pl - q)), pn) for pn, q in MOD_PINS[k].items())
            if d < 1.5: return n, pn
    return (near[0][2] if near else None), None


# ---------- 1. the wire steps ----------
def labels(v):
    return [d['text'] for d in D[v]['tb_on'] if d['kind'] == 'label']


steps = []
for v in V:
    nm = v['name']
    if not nm.startswith('Step ') or nm.endswith('c'): continue
    n = int(nm.split()[1])
    if not (3 <= n <= 14 or 16 <= n <= 24): continue
    h = v['v']; c = VN[nm + 'c']
    app_h = sorted(visible[h] - visible[h - 1], key=name); app_c = sorted(visible[c] - visible[c - 1], key=name)
    gone_c = sorted(visible[c - 1] - visible[c], key=name)
    lab = labels(h)
    routed0 = [x for x in app_c if not is_cap(name(x))]
    token = [x for x in gone_c if not is_cap(name(x)) and T[x]['nsolids'] == 1 and routed0 and colour(x) == colour(routed0[0])]
    routed = [x for x in app_c if not is_cap(name(x))]
    steps.append(dict(step=n, v_hover=h, v_done=c, labels=lab,
                      token=[name(x) for x in token], token_caps=[name(x) for x in gone_c if is_cap(name(x))],
                      routed=[name(x) for x in routed], routed_caps=[name(x) for x in app_c if is_cap(name(x))],
                      gone=[name(x) for x in gone_c],
                      other_appear_hover=[name(x) for x in app_h if x not in token and not is_cap(name(x))],
                      colour_token=[colour(x) for x in token], colour_routed=[colour(x) for x in routed]))

# module pins, named from the module-end cap of each step (the cap that is not on the I/O module)
for s_ in steps:
    for cn in s_['routed_caps']:
        part, pin = where(centre(TN[cn]))
        if part and part.startswith('Ensamblaje'): s_['shield_cap'] = [cn, pin]
        else:
            lab = [l for l in s_['labels'] if not (l[:1] in 'VGSvgs' and l[1:].isdigit())]
            k = kind_of(part, True)
            MOD_PINS.setdefault(k, {})[lab[0].upper()] = to_local(TN[part]['matrix_mm'], centre(TN[cn]))
            s_['module_cap'] = [cn, part, lab[0].upper()]
mod_pin = MOD_PINS

# every later pose: wires by colour, caps by pin
by_colour = collections.defaultdict(list)
for cid, r in R['tops'].items():
    if r['vis'] and not is_cap(name(cid)) and T[cid]['nsolids'] <= 5 and colour(cid) and ('Part' in name(cid) or ' to ' in name(cid)):
        by_colour[colour(cid)].append(cid)


def ranges(vs):
    out = []; s0 = None
    for x in vs:
        if s0 is None: s0 = p = x
        elif x == p + 1: p = x
        else: out.append([s0, p]); s0 = p = x
    if s0 is not None: out.append([s0, p])
    return out




cap_info = {}
for cid, r in R['tops'].items():
    if is_cap(name(cid)):
        part, pin = where(centre(T[cid]))
        cap_info[name(cid)] = dict(on=part, pin=pin, vis=ranges(r['vis']), colours=r['colours'][:2])

for s in steps:
    col_ = s['colour_routed'][0] if s['colour_routed'] else None
    s['all_poses'] = [dict(name=name(x), vis=ranges(R['tops'][x]['vis']), box_c=centre(T[x]).round(1).tolist()) for x in by_colour.get(col_, [])]
    tok = s['colour_token'][0] if s['colour_token'] else None
    s['token_same_colour'] = tok == col_

# ---------- 3. GLB: caps attached to each wire body ----------
GLB = ROOT + '/PMG Build Instructions/pmg.glb'
f = open(GLB, 'rb'); mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
clen, _ = struct.unpack_from('<II', mm, 12); doc = json.loads(bytes(mm[20:20 + clen])); bin_off = 20 + clen + 8
nodes = doc['nodes']


def acc(i):
    a = doc['accessors'][i]; view = doc['bufferViews'][a['bufferView']]
    off = bin_off + view.get('byteOffset', 0) + a.get('byteOffset', 0)
    n = NCOMP[a['type']]; dt = np.dtype(COMPONENT[a['componentType']])
    st = view.get('byteStride')
    if st and st != dt.itemsize * n:
        raw = np.frombuffer(mm, dtype=np.uint8, count=st * a['count'], offset=off).reshape(a['count'], st)
        return np.frombuffer(raw[:, :dt.itemsize * n].tobytes(), dtype=dt).reshape(a['count'], n)
    return np.frombuffer(mm, dtype=dt, count=a['count'] * n, offset=off).reshape(a['count'], n)


def world_points(top):
    out = []
    def walk(i, M):
        Wm = M @ node_matrix(nodes[i])
        if 'mesh' in nodes[i]:
            for p in doc['meshes'][nodes[i]['mesh']]['primitives']:
                P = acc(p['attributes']['POSITION']).astype(np.float64)
                out.append((P @ Wm[:3, :3].T + Wm[:3, 3]) * 1000.0)
        for c in nodes[i].get('children', []): walk(c, Wm)
    walk(G[top]['node'], np.eye(4))
    return np.vstack(out)


glb_caps = {k: g for k, g in G.items() if g['meshes'][0]['name'].startswith('Wire Cap')}
glb_wires = {k: g for k, g in G.items() if len(g['meshes']) == 1 and (g['meshes'][0]['name'].startswith(('Part', 'Copy')))
             and not g['meshes'][0]['name'].startswith(('Part152', 'Part153'))}
glb = {}
for k, g in sorted(glb_wires.items(), key=lambda x: int(x[0][4:])):
    P = world_points(k)
    att = []
    for pad in (0.1, 0.6, 1.5):
        cnt = []
        for ck, cb in glb_caps.items():
            lo = np.array(cb['min']) - pad; hi = np.array(cb['max']) + pad
            n_in = int(np.count_nonzero(np.all((P >= lo) & (P <= hi), axis=1)))
            if n_in: cnt.append((n_in, ck))
        cnt.sort(reverse=True)
        keep = []
        for n_in, ck in cnt:      # the best cap at each end: a second cap must be over 20 mm from the first
            cc = centre(glb_caps[ck])
            if all(np.linalg.norm(cc - centre(glb_caps[k2])) > 20 for _, k2 in keep): keep.append((n_in, ck))
            if len(keep) == 2: break
        if len(keep) == 2: break
    for n_in, ck in keep:
        cb = glb_caps[ck]; part, pin = where(centre(cb), cadasio=False)
        att.append(dict(cap=ck, on=part, pin=pin, c=centre(cb).round(1).tolist(), verts_in=n_in, pad=pad))
    glb[k] = dict(mesh=g['meshes'][0]['name'].split('^')[0], verts=len(P), caps=att, box_c=centre(g).round(1).tolist(),
                  length_hint=round(float(np.linalg.norm(np.array(g['max']) - np.array(g['min']))), 1))
    del P
glb_cap_pins = {}
for ck, cb in glb_caps.items():
    part, pin = where(centre(cb), cadasio=False)
    glb_cap_pins[ck] = dict(on=part, pin=pin, c=centre(cb).round(1).tolist())

json.dump(dict(steps=steps, cap_info=cap_info, module_pins={k: {n: q.round(2).tolist() for n, q in v.items()} for k, v in mod_pin.items()},
               shield_pins={k: {n: q.round(2).tolist() for n, (q, ax) in v.items()} for k, v in SHIELD_PINS.items()}, glb_wires=glb, glb_caps=glb_cap_pins),
          open(W + '/wires.json', 'w'), indent=1)
for s in steps:
    print(s['step'], s['labels'], 'token', s['token'], s['colour_token'], '| routed', s['routed'], s['colour_routed'], '| caps', s.get('shield_cap'), s.get('module_cap'))
print('module pins', {k: sorted(v) for k, v in mod_pin.items()})
