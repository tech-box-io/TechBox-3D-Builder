"""PMG: print the markdown tables of cadasio_map.md from cadasio_map.json (sections 4-8).

    .venv.nosync/bin/python docs/research/pmg/scripts/report_tables.py > docs/research/pmg/scripts/work/cadasio_map/tables.md
"""
import json, collections, re
ROOT = '/Users/lee-johnson/Desktop/Claude_Cadasio'
D = json.load(open(ROOT + '/docs/research/pmg/cadasio_map.json'))
W = ROOT + '/docs/research/pmg/scripts/work/cadasio_map'
WI = json.load(open(W + '/wires.json'))
V = D['viewer_steps']
G = D['glb_instances']


def short(n): return (n or '').replace('^PMG Full 3D Cadasio Build', '')


def nlist(ks):
    """NAUO24, NAUO25, ... -> 'NAUO24-25' style runs."""
    nums = sorted(int(k[4:]) for k in ks)
    out = []; s = p = None
    for n in nums:
        if s is None: s = p = n
        elif n == p + 1: p = n
        else: out.append((s, p)); s = p = n
    if s is not None: out.append((s, p))
    return ', '.join(f'NAUO{a}' if a == b else f'NAUO{a}-{b}' for a, b in out)


P = print
# ---------------------------------------------------------------- rigid parts
P('### 4.1 Rigid parts (electronics)\n')
P('| GLB | Cadasio component | Relation | Role | Cadasio shows it |')
P('|---|---|---|---|---|')
order = ['NAUO1', 'NAUO94', 'NAUO78', 'NAUO2', 'NAUO3', 'NAUO7', 'NAUO6', 'NAUO5', 'NAUO4', 'NAUO76', 'NAUO83', 'NAUO84', 'NAUO85',
         'NAUO80', 'NAUO129', 'NAUO79', 'NAUO44', 'NAUO82', 'NAUO267', 'NAUO81', 'NAUO278', 'NAUO279', 'NAUO277', 'NAUO280', 'NAUO281', 'NAUO284',
         'NAUO282', 'NAUO283', 'NAUO285']
for k in order:
    r = G[k]
    P(f"| {k} | {short(r['cadasio']) or '-'} | {r['relation']} | {r['role']} | {r['cadasio_steps']} |")
P()
P('### 4.2 Wood\n')
P('| GLB | Cadasio component | Role | Cadasio shows it (built pose; earlier it is hovering) |')
P('|---|---|---|---|')
for k in ['NAUO63', 'NAUO65', 'NAUO66', 'NAUO73', 'NAUO67', 'NAUO60', 'NAUO68', 'NAUO61', 'NAUO72', 'NAUO71', 'NAUO70', 'NAUO69', 'NAUO64', 'NAUO62', 'NAUO77', 'NAUO75', 'NAUO74']:
    r = G[k]
    P(f"| {k} | {short(r['cadasio'])} | {r['role']} | {r['cadasio_steps']} |")
P()

# ---------------------------------------------------------------- wire bodies by pose
P('### 4.3 Routed wire bodies, by pose\n')
P('Each cell: the GLB body (and its Cadasio twin when the GLB has one). "=" identical, "~" same body within 2.5 mm, "name" same name but another route, '
  '"old" the old VCC wire (button VCC pin to G instead of V), "mirr" module end on the mirrored matrix pin. Rows are the published wires; '
  'a dash means the GLB has no body for that wire in that pose.\n')
poses = ['bench', 'in case, module on bench', 'held above H4', 'mounted, display/matrix on bench', 'BUILT']
P('| Step | Wire | ' + ' | '.join(poses) + ' |')
P('|---|---|' + '---|' * len(poses))
for w in D['wires']:
    cells = []
    for pz in poses:
        ps = [p for p in w['poses'] if p['pose'] == pz]
        if not ps:
            cells.append(''); continue
        p = ps[0]; cw = short((p.get('cadasio') or {}).get('wire'))
        g = p.get('glb') or []
        if not g:
            cells.append(f'- (Cadasio {cw})'); continue
        x = g[0]
        tag = '=' if x['relation'] == 'identical' else '~' if x['relation'].startswith('same body') else 'name' if x['relation'].startswith('same name') else ''
        if 'old wiring' in x['note']: tag = 'old'
        if 'mirrored' in x['note'] or 'turned end for end' in x['note']: tag = (tag + ' mirr').strip()
        cells.append(f"{x['nauo']} {x['body']} [{tag}] (Cadasio {cw})")
    P(f"| {w['step']} | {w['module']} {w['module_pin']} -> {w['shield_pin']} | " + ' | '.join(cells) + ' |')
P()
P('Poses only Cadasio has (no GLB body for any wire): display held above the brackets [104]-[105] (Part190-193) and half-way [106] '
  '(Part194-197); matrix held [109]-[110] (Part166, one body of 5 sweeps) and half-way [111] (Part203-207).\n')
P('GLB-only wire bodies (never shown in Cadasio):\n')
only = collections.defaultdict(list)
for w in D['wires']:
    for p in w['poses']:
        if p['pose'].startswith('GLB only'):
            for x in p['glb']:
                only[p['pose'][10:]].append(f"{x['nauo']} {x['body']} ({x['pins'][0]}->{x['pins'][1]}{'; ' + x['note'] if x['note'] else ''})")
for k, v in only.items():
    P(f'- {k}: ' + ', '.join(v))
P()

# ---------------------------------------------------------------- caps
P('### 4.4 Wire caps (the black housings), by the part and pin they sit on\n')
P('| Part (pose) | GLB caps: pin = NAUO | Cadasio caps with no GLB cap (shown) |')
P('|---|---|---|')
caps = WI['glb_caps']; byp = collections.defaultdict(dict)
for k, c in caps.items():
    if c['pin']: byp[c['on']][c['pin']] = k
missing = collections.defaultdict(list)
for n, c in D['caps'].items():
    if c['relation'] == 'no counterpart' and c['steps'] != 'never shown' and c['on']:
        missing[c['on']].append(f"{c['pin']} = {n}")
names = {'NAUO1': 'I/O module, bench (NAUO1)', 'NAUO94': 'I/O module, held (NAUO94)', 'NAUO78': 'I/O module, mounted (NAUO78)',
         'NAUO7': 'button 1 black, bench', 'NAUO6': 'button 2 yellow, bench', 'NAUO5': 'button 3 white, bench', 'NAUO4': 'button 4 blue, bench',
         'NAUO76': 'button 1 black, case', 'NAUO83': 'button 2 yellow, case', 'NAUO84': 'button 3 white, case', 'NAUO85': 'button 4 blue, case',
         'NAUO80': 'display, bench', 'NAUO129': 'display, held beside (GLB only)', 'NAUO79': 'display, seated',
         'NAUO44': 'matrix, bench (GLB turned)', 'NAUO82': 'matrix, aside (never shown)', 'NAUO267': 'matrix, raised (never shown)', 'NAUO81': 'matrix, seated'}
CADPART = {'NAUO1': 'Ensamblaje_Shield_NANO-1', 'NAUO94': 'Ensamblaje_Shield_NANO-3', 'NAUO78': 'Ensamblaje_Shield_NANO-2', 'NAUO7': 'Big Button Module-4',
           'NAUO6': 'Big Button Module-3', 'NAUO5': 'Big Button Module-2', 'NAUO4': 'Big Button Module-1', 'NAUO76': 'Big Button Module-5',
           'NAUO83': 'Big Button Module-9', 'NAUO84': 'Big Button Module-10', 'NAUO85': 'Big Button Module-11', 'NAUO80': 'Display TM1637-4',
           'NAUO79': 'Display TM1637-2', 'NAUO44': 'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-1', 'NAUO81': 'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-4'}
pin_order = ['VCC', 'OUT', 'GND', 'CLK', 'DIO', 'DIN', 'CS']
def pkey(p):
    if p in pin_order: return (0, pin_order.index(p), 0)
    m = re.match(r'([GVS])(\d+)', p)
    return (1, int(m.group(2)), 'GVS'.index(m.group(1))) if m else (2, 0, 0)
for k in names:
    pins = byp.get(k, {})
    cell = ', '.join(f'{p}={n}' for p, n in sorted(pins.items(), key=lambda x: pkey(x[0])))
    miss = ', '.join(sorted(missing.get(CADPART.get(k), []), key=lambda s: pkey(s.split(' = ')[0])))
    P(f'| {names[k]} | {cell} | {miss} |')
for cp in ('Display TM1637-6', 'Display TM1637-7', 'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-8', 'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-9'):
    P(f"| {cp} (Cadasio only) | - | {', '.join(sorted(missing.get(cp, []), key=lambda s: pkey(s.split(' = ')[0])))} |")
P()

# ---------------------------------------------------------------- tokens and ribbons
P('### 4.5 Loose straight wires (tokens) and the two ribbons\n')
P('| Step | Token wire: Cadasio = GLB | Its two caps: Cadasio = GLB | Centre at Step N (mm) | Ribbon |')
P('|---|---|---|---|---|')
for w in D['wires']:
    t = [p for p in w['poses'] if p['pose'].startswith('loose')][0]
    c = t['cadasio']; g = t.get('glb') or {}
    capg = g.get('caps') or []
    P(f"| {w['step']} | {short(c['wire'])} = {g.get('wire') or 'not in GLB'} | {', '.join(c['caps'])} = {', '.join(capg) if capg else 'not in GLB'} | {c['centre_mm_at_step']} | {'12-wire (Step 2)' if w['step'] <= 14 else '9-wire (Step 15)'} |")
P()

# ---------------------------------------------------------------- cameras, compact
P('### 8. Cameras (one row per camera; the JSON has every step)\n')
P('Direction = unit vector from the target to the eye, GLB frame. Up = the camera\'s up vector (Y- on the turned-over run).\n')
P('| Viewer steps | Direction | Target (mm) | Distance (mm) | Elev / azim (deg) | Up |')
P('|---|---|---|---|---|---|')
rows = []
for v in V:
    c = v['camera']; key = json.dumps([c['dir'], c['target_mm'], c['dist_mm']])
    if rows and rows[-1][0] == key: rows[-1][2] = v
    else: rows.append([key, v, v])
for key, a, b in rows:
    c = a['camera']
    st = f"[{a['v']:03d}] {a['name']}" if a['v'] == b['v'] else f"[{a['v']:03d}] {a['name']} to [{b['v']:03d}] {b['name']}"
    P(f"| {st} | {[round(x, 3) for x in c['dir']]} | {c['target_mm']} | {c['dist_mm']} | {c['elev_deg']} / {c['azim_deg']} | {[round(x, 2) for x in c['up']]} ({a['up_axis']}) |")
