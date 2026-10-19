"""PMG: assemble docs/research/pmg/cadasio_map.json from the working files of cadasio_tree.py, match.py, replay.py and wires.py,
and print the tables used in cadasio_map.md.

    .venv.nosync/bin/python docs/research/pmg/scripts/build_map.py
"""
import json, re, collections
import numpy as np
ROOT = '/Users/lee-johnson/Desktop/Claude_Cadasio'
W = ROOT + '/docs/research/pmg/scripts/work/cadasio_map'
TREE = json.load(open(W + '/cadasio_tree.json'))
T = {t['id']: t for t in TREE['tops']}; TN = {t['name']: t for t in T.values()}
G = json.load(open(W + '/glb_boxes.json'))
R = json.load(open(W + '/replay.json')); V = R['viewer']
M = {m['cad_id']: m for m in json.load(open(W + '/match.json'))}
WI = json.load(open(W + '/wires.json'))
VN = {v['name']: v['v'] for v in V}


def short(n): return n.replace('^PMG Full 3D Cadasio Build', '')


def ranges(vs):
    out = []; s = None
    for x in vs:
        if s is None: s = p = x
        elif x == p + 1: p = x
        else: out.append([s, p]); s = p = x
    if s is not None: out.append([s, p])
    return out


def rtxt(vs):
    rr = ranges(vs)
    if not rr: return 'never shown'
    return ', '.join(f'[{a:03d}] {V[a]["name"]}' if a == b else f'[{a:03d}]-[{b:03d}] {V[a]["name"]} to {V[b]["name"]}' for a, b in rr)


def centre(b): return ((np.array(b['min']) + np.array(b['max'])) / 2)


def gkind(k):
    ms = G[k]['meshes']
    for m in ms:
        if m['name'].startswith('Socket_Blok'): return 'Big Button Module'
        if m['name'].startswith('8x female'): return 'LED Matrix 32x8 (MAX7219)'
        if m['name'].startswith('smt_resistor'): return 'Ensamblaje_Shield_NANO'
    return ms[0]['name'].split('^')[0].replace('_По умолчанию', '').replace('_Varsayılan', '')


# ---------------------------------------------------------------- GLB <-> Cadasio, rigid parts by hand (checked in pairs.py)
RIGID = {
    'NAUO1': ('Ensamblaje_Shield_NANO-1', 'identical', 'Nano I/O Module, on the bench (lying flat, pins up, USB end +Z). In Cadasio its own Nano is hidden and nano-3 is shown on it; in the GLB this copy has the Nano\'s chips but not its board or pin rows'),
    'NAUO78': ('Ensamblaje_Shield_NANO-2', 'same role, turned 180 deg about X', 'Nano I/O Module mounted on the back panel H4 (BUILT pose). The GLB copy is upside down compared with the published one: USB end and power jack at the bottom (Y-), digital G/V/S rows on the +Z side; Cadasio\'s has them at the top and on the -Z side'),
    'NAUO94': ('Ensamblaje_Shield_NANO-3', 'same role, turned 180 deg about X', 'Nano I/O Module held above the back panel, 104.7 mm straight above NAUO78 (Cadasio: 102.3 mm above its mounted copy), turned as NAUO78'),
    'NAUO2': ('nano-1', 'identical', 'Nano Board 44.9 mm straight above its seat on the bench module (never shown in Cadasio)'),
    'NAUO3': ('nano-2', 'identical', 'Nano Board 15.2 mm straight above its seat on the bench module (never shown in Cadasio)'),
    'NAUO7': ('Big Button Module-4', 'identical', 'Push button 1, BLACK cap, on the bench behind the module (wired to D4)'),
    'NAUO6': ('Big Button Module-3', 'identical', 'Push button 2, YELLOW cap, on the bench (D5)'),
    'NAUO5': ('Big Button Module-2', 'identical', 'Push button 3, WHITE cap, on the bench (D6)'),
    'NAUO4': ('Big Button Module-1', 'identical', 'Push button 4, BLUE cap, on the bench (D7)'),
    'NAUO76': ('Big Button Module-5', 'identical', 'Push button 1, BLACK, clipped into its slot in H6 (BUILT pose)'),
    'NAUO83': ('Big Button Module-9', 'identical', 'Push button 2, YELLOW, in the case (BUILT pose)'),
    'NAUO84': ('Big Button Module-10', 'identical', 'Push button 3, WHITE, in the case (BUILT pose)'),
    'NAUO85': ('Big Button Module-11', 'identical', 'Push button 4, BLUE, in the case (BUILT pose); the first one clipped in (Step 33c)'),
    'NAUO80': ('Display TM1637-4', 'identical', '4-digit display on the bench'),
    'NAUO79': ('Display TM1637-2', 'identical (0.2 mm)', '4-digit display seated on the brackets H11/H12 (BUILT pose)'),
    'NAUO129': (None, 'no counterpart', '4-digit display held 80.0 mm to +Z of its seat, same turn as seated; wired to the mounted module (Part105-108). Cadasio holds it instead above the brackets, tilted 23.3 deg (Display TM1637-6, Steps 47c-48) and half-way (Display TM1637-7, [106])'),
    'NAUO44': ('LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-1', 'same role, turned 180 deg about X and 29.4 mm nearer', 'Dot matrix on the bench. The GLB copy is 29.4 mm nearer the module (centre z 1405.6 against 1435.0) and turned end for end, so its input header is at the far end and its five wires land on the mirrored pins'),
    'NAUO81': ('LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-4', 'identical', 'Dot matrix seated on the brackets (BUILT pose)'),
    'NAUO82': ('LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-6', 'identical', 'Dot matrix 143.3 mm to -Z of its seat (beside the case), wired to the mounted module (Part85-88, Part163). Never shown in Cadasio'),
    'NAUO267': ('LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-7', 'same role, 1.9 mm along Z', 'Dot matrix 85.9 mm straight above its seat, wired to the BENCH module (Part147-151). Never shown in Cadasio'),
    'NAUO278': ('USB Cable end-1', 'identical', 'USB cable, A end, on the bench'),
    'NAUO279': ('USB Right Angle-1', 'identical', 'USB cable, right-angle Mini-B plug, plugged into the bench Nano (Step 25: 22.9 mm out along +X)'),
    'NAUO277': ('Copy of Part23^PMG Full 3D Cadasio Build-1', 'same body (0.7 mm)', 'USB cable lead between NAUO278 and NAUO279, bench'),
    'NAUO280': ('USB Cable end-2', 'same role, elsewhere', 'USB A end, held pose (with the module held above H4); GLB 45.6 mm lower and 97.7 mm to +Z of Cadasio\'s'),
    'NAUO281': ('USB Right Angle-2', 'same role, turned 180 deg about X', 'USB Mini-B plug in the held module\'s Nano (at its bottom in the GLB, at its top in Cadasio)'),
    'NAUO284': ('Part152^PMG Full 3D Cadasio Build-1', 'same name, other shape', 'USB lead, held pose (joins NAUO280 and NAUO281); 30.8 mm tall in the GLB, 63.5 mm in Cadasio'),
    'NAUO282': ('USB Right Angle-3', 'same role, turned 180 deg about X', 'USB Mini-B plug in the mounted module\'s Nano (BUILT pose; at the bottom of the module in the GLB)'),
    'NAUO283': ('USB Cable end-3', 'same role, elsewhere', 'USB A end lying on the table behind the case (BUILT pose); GLB 11.2 mm to -X and 69.7 mm to +Z of Cadasio\'s'),
    'NAUO285': ('Part153^PMG Full 3D Cadasio Build-1', 'same name, other shape', 'USB lead, BUILT pose (joins NAUO282 and NAUO283)'),
}
WOOD = {'NAUO63': 'H1-1', 'NAUO65': 'H2-1', 'NAUO66': 'H3-1', 'NAUO73': 'H4v2-1', 'NAUO67': 'H5-1', 'NAUO60': 'H6-1', 'NAUO68': 'H7-1',
        'NAUO61': 'H8-1', 'NAUO72': 'PMG_PianoKey_Aug25-4', 'NAUO71': 'PMG_PianoKey_Aug25-3', 'NAUO70': 'PMG_PianoKey_Aug25-2',
        'NAUO69': 'PMG_PianoKey_Aug25-1', 'NAUO64': 'H10-1', 'NAUO62': 'H11v2-1', 'NAUO77': 'H12v2-2', 'NAUO75': 'H13v2-1', 'NAUO74': 'H14-1'}
WOOD_ROLE = {'NAUO63': 'H1, front rail', 'NAUO65': 'H2, side (+Z)', 'NAUO66': 'H3, side (-Z)', 'NAUO73': 'H4, back panel (the module mounts on it)',
             'NAUO67': 'H5, deck with the four button windows', 'NAUO60': 'H6, button carrier under the deck', 'NAUO68': 'H7, bottom cover',
             'NAUO61': 'H8, cross divider', 'NAUO72': 'H9, piano key over button 1 (black); the first key (Step 38)',
             'NAUO71': 'H9, piano key over button 2 (yellow)', 'NAUO70': 'H9, piano key over button 3 (white)', 'NAUO69': 'H9, piano key over button 4 (blue)',
             'NAUO64': 'H10, upper deck', 'NAUO62': 'H11, display bracket (+Z)', 'NAUO77': 'H12, display bracket (-Z)', 'NAUO75': 'H13, rear brace',
             'NAUO74': 'H14, face plate with the display window'}

# ---------------------------------------------------------------- the 21 wires
STEP_WIRE = {}
for s in WI['steps']:
    STEP_WIRE[s['step']] = s
SHIELD_TO_STEP = {}
for s in WI['steps']:
    SHIELD_TO_STEP[s['shield_cap'][1]] = s['step']
CORRECT = {10: ('OUT', 'S6'), 16: ('CLK', 'S8'), 17: ('DIO', 'S9')}   # published slips: Step 10 says S5; Steps 16-17 lower case
MODULE_OF = {}
for s in WI['steps']:
    n = s['step']
    MODULE_OF[n] = ('button %d' % ((n - 3) // 3 + 1)) if n <= 14 else ('display' if n <= 19 else 'matrix')

# poses of the module and of the I/O module, both projects
SHIELD_POSE = {'NAUO1': 'bench', 'Ensamblaje_Shield_NANO-1': 'bench', 'NAUO94': 'held', 'Ensamblaje_Shield_NANO-3': 'held',
               'NAUO78': 'mounted', 'Ensamblaje_Shield_NANO-2': 'mounted'}
MOD_POSE = {}
for k in ('NAUO4', 'NAUO5', 'NAUO6', 'NAUO7', 'NAUO80', 'NAUO44'): MOD_POSE[k] = 'bench'
for k in ('NAUO76', 'NAUO83', 'NAUO84', 'NAUO85'): MOD_POSE[k] = 'in case'
MOD_POSE.update({'NAUO79': 'seated', 'NAUO81': 'seated', 'NAUO129': 'held beside (GLB only)', 'NAUO82': 'aside (-Z)', 'NAUO267': 'raised'})
for n in ('Big Button Module-1', 'Big Button Module-2', 'Big Button Module-3', 'Big Button Module-4', 'Display TM1637-4', 'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-1'):
    MOD_POSE[n] = 'bench'
for n in ('Big Button Module-5', 'Big Button Module-9', 'Big Button Module-10', 'Big Button Module-11'): MOD_POSE[n] = 'in case'
MOD_POSE.update({'Display TM1637-2': 'seated', 'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-4': 'seated', 'Display TM1637-6': 'held above brackets',
                 'Display TM1637-7': 'half-way', 'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-8': 'held', 'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-9': 'half-way',
                 'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-6': 'aside (-Z)', 'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-7': 'raised',
                 'Display TM1637-1': 'raised high', 'Display TM1637-5': 'raised'})

# GLB wires: identity from the shield pin, pose from the two parts
glb_wire_rows = {}
for k, w in WI['glb_wires'].items():
    caps = w['caps']
    if len(caps) < 2 or not any(c['on'] in SHIELD_POSE for c in caps):
        continue
    sc = [c for c in caps if c['on'] in SHIELD_POSE][0]; mc = [c for c in caps if c is not sc][0]
    step = SHIELD_TO_STEP.get(sc['pin'])
    if mc['pin'] == 'VCC' and sc['pin'].startswith('G') and MODULE_OF[step].startswith('button'):
        step = SHIELD_TO_STEP['V' + sc['pin'][1:]]      # the old VCC wire: same module end as the published VCC wire, shield end one column over
    if mc['on'] in ('NAUO81', 'NAUO82', 'NAUO267'):     # matrix copies the right way round: the wire is the one on that module pin
        step = {'VCC': 20, 'GND': 21, 'DIN': 22, 'CS': 23, 'CLK': 24}[mc['pin']]
    pub = STEP_WIRE[step]
    pub_mod_pin = pub['module_cap'][2]
    note = ''
    if MODULE_OF[step].startswith('button') and mc['pin'] == 'VCC' and sc['pin'].startswith('G'):
        note = 'old wiring: from the button\'s VCC pin to %s, not V%s (the GLB has no wire on the button\'s GND pin)' % (sc['pin'], sc['pin'][1:])
    elif mc['pin'] != pub_mod_pin:
        note = 'module end on the %s pin, published wire uses %s (matrix turned end for end)' % (mc['pin'], pub_mod_pin)
    elif sc['pin'] != pub['shield_cap'][1]:
        note = 'ends on %s, the published wire on %s (a slip in this unused CAD pose: %s already has its own wire)' % (sc['pin'], pub['shield_cap'][1], sc['pin'])
    glb_wire_rows[k] = dict(nauo=k, body=w['mesh'], step=step, shield_cap=sc['cap'], shield_pin=sc['pin'], shield_pose=SHIELD_POSE[sc['on']],
                            module=mc['on'], module_cap=mc['cap'], module_pin=mc['pin'], module_pose=MOD_POSE.get(mc['on'], '?'), note=note)

# Cadasio wires: identity from colour, pose from visibility
cad_wire_rows = collections.defaultdict(list)
for s in WI['steps']:
    for p in s['all_poses']:
        cad_wire_rows[s['step']].append(dict(name=p['name'], vis=p['vis']))
# Part54 (OUT -> S4, in the case) is shown in the default grey #e3e3e3, so the colour search misses it; Part166 holds all five matrix wires
cad_wire_rows[4].append(dict(name='Part54^PMG Full 3D Cadasio Build-1', vis=ranges(R['tops'][TN['Part54^PMG Full 3D Cadasio Build-1']['id']]['vis'])))
for n in range(20, 25):
    if not any(r['name'].startswith('Part166') for r in cad_wire_rows[n]):
        cad_wire_rows[n].append(dict(name='Part166^PMG Full 3D Cadasio Build-1 (one of its 5 sweeps)', vis=ranges(R['tops'][TN['Part166^PMG Full 3D Cadasio Build-1']['id']]['vis'])))


def cad_pose(vis):
    a = vis[0][0]; b = vis[-1][1]
    nm = V[a]['name']
    if nm in ('Step 2', 'Step 15'): return 'ribbon'
    return {'Step 3c': 'bench', 'Step 4c': 'bench'}.get(nm, None) or (
        'bench' if a < 73 and V[a]['name'].endswith('c') else
        'in case, module on bench' if nm in ('Step 33c', 'Step 34c') else
        'held above H4' if nm == 'Step 45c' else
        'mounted, display/matrix on bench' if nm == 'Step 46c' else
        'display held' if nm == 'Step 47c' else 'display half-way' if nm == 'Transition' and a == 106 else
        'matrix held' if nm == 'Step 49c' else 'matrix half-way' if nm == 'Transition' and a == 111 else
        'BUILT' if nm == 'Start' else 'token' if not nm.endswith('c') else nm)


def glb_pose(r):
    sp, mp = r['shield_pose'], r['module_pose']
    if sp == 'bench' and mp == 'bench': return 'bench'
    if sp == 'bench' and mp == 'in case': return 'in case, module on bench'
    if sp == 'held' and mp in ('bench', 'in case'): return 'held above H4'
    if sp == 'held': return 'module held above H4, %s %s' % ('matrix' if r['step'] >= 20 else 'display', mp)
    if sp == 'bench': return 'module on the bench, %s %s' % ('matrix' if r['step'] >= 20 else 'display', mp)
    if sp == 'mounted' and mp == 'in case': return 'BUILT'
    if sp == 'mounted' and mp == 'seated': return 'BUILT'
    if sp == 'mounted' and mp == 'bench': return 'mounted, display/matrix on bench'
    if sp == 'mounted': return 'module mounted, %s %s' % ('matrix' if r['step'] >= 20 else 'display', mp)
    return sp + '/' + mp


# a GLB wire and a Cadasio wire are "the same body" when their names agree and their boxes are within 2.5 mm
def same_body(cname, gk):
    t = TN.get(cname.split(' (')[0])
    if not t: return None
    g = G[gk]
    err = float(np.abs(centre(t) - centre(g)).max() + np.abs((np.array(t['max']) - np.array(t['min'])) - (np.array(g['max']) - np.array(g['min']))).max())
    return round(err, 1)


SHIELDS = ['Ensamblaje_Shield_NANO-1', 'Ensamblaje_Shield_NANO-2', 'Ensamblaje_Shield_NANO-3']
MODCOPIES = {'button 1': ['Big Button Module-4', 'Big Button Module-5'], 'button 2': ['Big Button Module-3', 'Big Button Module-9'],
             'button 3': ['Big Button Module-2', 'Big Button Module-10'], 'button 4': ['Big Button Module-1', 'Big Button Module-11'],
             'display': ['Display TM1637-4', 'Display TM1637-2', 'Display TM1637-6', 'Display TM1637-7'],
             'matrix': ['LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-%d' % i for i in (1, 4, 8, 9)]}
wires_out = []
for n in sorted(STEP_WIRE):
    s = STEP_WIRE[n]
    lab = s['labels']; mod_lab, sh_lab = s['module_cap'][2], s['shield_cap'][1]
    printed = [l for l in lab]
    poses = []
    # token + caps
    tok = s['token'][0] if s['token'] else None
    tvis = R['tops'][TN[tok]['id']]['vis'] if tok else []
    hv = s['v_hover']
    off = R['tops'][TN[tok]['id']]['off'].get(str(hv)) if tok else None
    tpos = (centre(TN[tok]) + np.array(off or [0, 0, 0])).round(1).tolist() if tok else None
    gtok = M[TN[tok]['id']] if tok else None
    poses.append(dict(pose='loose token at Step %d (parking spot)' % n, steps=rtxt([v for v in tvis if v >= hv - 1]), cadasio=dict(wire=short(tok) if tok else None, caps=s['token_caps'],
                      centre_mm_at_step=tpos, offset_from_cad_mm=off),
                      glb=dict(wire=gtok['best'] if gtok and gtok['box_err'] < 0.5 else None,
                               caps=[M[TN[c]['id']]['best'] for c in s['token_caps'] if M[TN[c]['id']]['box_err'] < 0.5])))
    # ribbon membership
    ribbon_v = [v for v in tvis if v < hv - 1]
    if ribbon_v:
        poses.append(dict(pose='ribbon (Step %s), then fanned out (Step %sc)' % (V[ribbon_v[0]]['name'].split()[1], V[ribbon_v[0]]['name'].split()[1]),
                          steps=rtxt(ribbon_v), cadasio=dict(wire=short(tok), offsets_mm={V[v]['name']: R['tops'][TN[tok]['id']]['off'].get(str(v)) for v in ribbon_v})))
    # routed poses
    gl = [r for r in glb_wire_rows.values() if r['step'] == n]
    for cw in sorted(cad_wire_rows[n], key=lambda r: r['vis'][0][0]):
        if cw['name'] == tok: continue
        pose = cad_pose(cw['vis'])
        g_same = [r for r in gl if glb_pose(r) == pose]
        g_desc = []
        for r in g_same:
            e = same_body(cw['name'], r['nauo']) if r['body'] == short(cw['name']).rsplit('-', 1)[0].split(' (')[0] else None
            g_desc.append(dict(nauo=r['nauo'], body=r['body'], caps=[r['module_cap'], r['shield_cap']], pins=[r['module_pin'], r['shield_pin']],
                               relation=('identical' if e is not None and e < 0.5 else 'same body (%.1f mm)' % e if e is not None and e < 2.5 else
                                         'same name, other route' if e is not None else 'other body'),
                               note=r['note']))
        wv = {v for a, b in cw['vis'] for v in range(a, b + 1)}
        ccaps = []
        for cn, ci in WI['cap_info'].items():
            if not ci['on'] or ci['on'] not in MODCOPIES[MODULE_OF[n]] + SHIELDS: continue
            want = mod_lab if ci['on'] in MODCOPIES[MODULE_OF[n]] else sh_lab
            if ci['pin'] == want and wv & {v for a, b in ci['vis'] for v in range(a, b + 1)}:
                ccaps.append(cn)
        poses.append(dict(pose=pose, steps=rtxt(sorted(wv)), cadasio=dict(wire=short(cw['name']), caps=sorted(ccaps)), glb=g_desc or None))
    # GLB-only poses of this wire
    used = {d['nauo'] for p in poses for d in (p.get('glb') or []) if isinstance(d, dict) and 'nauo' in d}
    for r in gl:
        if r['nauo'] not in used:
            poses.append(dict(pose='GLB only: ' + glb_pose(r), steps='never shown in Cadasio',
                              glb=[dict(nauo=r['nauo'], body=r['body'], caps=[r['module_cap'], r['shield_cap']], pins=[r['module_pin'], r['shield_pin']], note=r['note'])]))
    col = s['colour_routed'][0]
    wires_out.append(dict(step=n, module=MODULE_OF[n], module_pin=mod_lab, shield_pin=sh_lab, published_labels=printed,
                          slip=('labelled "%s"; the pin is %s' % ('S5', 'S6') if n == 10 else 'labels in lower case ("clk"/"s8")' if n == 16 else 'labels in lower case ("dio"/"s9")' if n == 17 else None),
                          colour=col, viewer=dict(hover=hv, done=s['v_done']),
                          caps_routed_bench=dict(module=s['module_cap'][0], shield=s['shield_cap'][0]), poses=poses))

# caps: Cadasio cap -> GLB cap by (part pose, pin)
POSE_PART = {'Ensamblaje_Shield_NANO-1': 'NAUO1', 'Ensamblaje_Shield_NANO-2': 'NAUO78', 'Ensamblaje_Shield_NANO-3': 'NAUO94',
             'Big Button Module-1': 'NAUO4', 'Big Button Module-2': 'NAUO5', 'Big Button Module-3': 'NAUO6', 'Big Button Module-4': 'NAUO7',
             'Big Button Module-5': 'NAUO76', 'Big Button Module-9': 'NAUO83', 'Big Button Module-10': 'NAUO84', 'Big Button Module-11': 'NAUO85',
             'Display TM1637-4': 'NAUO80', 'Display TM1637-2': 'NAUO79', 'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-1': 'NAUO44',
             'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-4': 'NAUO81', 'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-6': 'NAUO82',
             'LED Matrix 32x8 - 4 Modules 8x8 with MAX7219-7': 'NAUO267'}
glb_cap_by = {(c['on'], c['pin']): k for k, c in WI['glb_caps'].items() if c['pin']}
caps_out = {}
for n, c in WI['cap_info'].items():
    g = None; rel = None
    cid = TN[n]['id']; m = M[cid]
    if m['box_err'] < 0.5: g, rel = m['best'], 'identical'
    elif c['on'] in POSE_PART and c['pin'] and (POSE_PART[c['on']], c['pin']) in glb_cap_by:
        g, rel = glb_cap_by[(POSE_PART[c['on']], c['pin'])], 'same pin of the same part, other place (part turned or moved)'
    caps_out[n] = dict(on=c['on'], pin=c['pin'], steps=rtxt(R['tops'][cid]['vis']), glb=g, relation=rel or 'no counterpart')

# ---------------------------------------------------------------- every GLB instance
glb_out = {}
cad_by_glb = collections.defaultdict(list)
for cid, m in M.items():
    if m['box_err'] < 0.5: cad_by_glb[m['best']].append(T[cid]['name'])
for k in sorted(G, key=lambda x: int(x[4:])):
    kind = gkind(k); row = dict(kind=kind, centre_mm=centre(G[k]).round(1).tolist(), size_mm=(np.array(G[k]['max']) - np.array(G[k]['min'])).round(1).tolist())
    if k in RIGID:
        cn, rel, role = RIGID[k]
        row.update(cadasio=cn, relation=rel, role=role, cadasio_steps=rtxt(R['tops'][TN[cn]['id']]['vis']) if cn else 'n/a')
    elif k in WOOD:
        cn = WOOD[k]; row.update(cadasio=cn, relation='identical', role=WOOD_ROLE[k], cadasio_steps=rtxt(R['tops'][TN[cn]['id']]['vis']))
    elif k in glb_wire_rows:
        r = glb_wire_rows[k]; pub = STEP_WIRE[r['step']]
        cn = cad_by_glb.get(k, [None])[0]
        same = [c for c in [TN.get(r['body'] + '^PMG Full 3D Cadasio Build-1')] if c]
        rel = 'identical' if cn else ('same name, re-routed' if same else 'no counterpart')
        row.update(cadasio=cn or (same[0]['name'] if same else None), relation=rel,
                   role='wire %s -> %s (Step %d, %s), %s pose: %s %s -> I/O module %s%s' % (
                       r['module_pin'], r['shield_pin'], r['step'], pub['colour_routed'][0], glb_pose(r), MODULE_OF[r['step']], r['module_pose'], r['shield_pose'],
                       ('; ' + r['note']) if r['note'] else ''),
                   cadasio_steps=rtxt(R['tops'][(TN.get(cn) or (same[0] if same else {'id': None}))['id']]['vis']) if (cn or same) else 'n/a')
    elif kind.startswith('Wire Cap'):
        c = WI['glb_caps'][k]; cn = cad_by_glb.get(k, [None])[0]
        if c['pin']:
            role = 'cap on %s pin %s (%s)' % (c['on'], c['pin'], (SHIELD_POSE.get(c['on']) and 'I/O module ' + SHIELD_POSE[c['on']]) or (MOD_POSE.get(c['on'], '') + ' ' + gkind(c['on'])))
        else:
            # a loose token's cap: which token wire it belongs to
            tw = [w for w, v in WI['glb_wires'].items() if any(x['cap'] == k for x in v['caps'])]
            role = 'cap of loose token wire %s (%s)' % (tw[0] if tw else '?', WI['glb_wires'][tw[0]]['mesh'] if tw else '?')
        row.update(cadasio=cn, relation='identical' if cn else 'no counterpart (see caps)', role=role, cadasio_steps=rtxt(R['tops'][TN[cn]['id']]['vis']) if cn else 'n/a')
    elif kind.startswith(('Copy', 'Part')):
        cn = cad_by_glb.get(k, [None])[0]
        w = WI['glb_wires'].get(k)
        tok = [s for s in WI['steps'] if s['token'] and cn and s['token'][0] == cn]
        if tok:
            role = 'loose straight wire (token) for Step %d, %s; member of the %s ribbon' % (tok[0]['step'], tok[0]['colour_token'][0], '12-wire' if tok[0]['step'] <= 14 else '9-wire')
        elif cn:
            role = 'loose straight wire of the 9-wire ribbon, spare (never shown)'
        else:
            role = 'wire body, ' + str(w['caps'] if w else '')
        row.update(cadasio=cn, relation='identical' if cn else 'no counterpart', role=role, cadasio_steps=rtxt(R['tops'][TN[cn]['id']]['vis']) if cn else 'n/a')
    else:
        cn = cad_by_glb.get(k, [None])[0]
        row.update(cadasio=cn, relation='identical' if cn else '?', role='?', cadasio_steps=rtxt(R['tops'][TN[cn]['id']]['vis']) if cn else 'n/a')
    glb_out[k] = row

# ---------------------------------------------------------------- every Cadasio component
cad_out = []
glb_of = {}
for k, r in glb_out.items():
    if r.get('cadasio'): glb_of.setdefault(r['cadasio'], []).append((k, r['relation']))
for t in sorted(T.values(), key=lambda t: t['idx']):
    r = R['tops'][t['id']]
    cad_out.append(dict(name=t['name'], idx=t['idx'], solids=t['nsolids'], centre_mm=centre(t).round(1).tolist(),
                        size_mm=(np.array(t['max']) - np.array(t['min'])).round(1).tolist(), steps=rtxt(r['vis']), visible=r['vis'],
                        moves={V[int(v)]['name'] + ' [%03d]' % int(v): o for v, o in r['off'].items()},
                        turned_at=[V[int(v)]['name'] for v in r['rot']], colour=(r['colours'][0][0] if r['colours'] else None),
                        glb=glb_of.get(t['name'], [])))

moves_of = {c['name']: c['moves'] for c in cad_out}
for k, r in glb_out.items():
    if r.get('cadasio') and r['relation'] in ('identical', 'identical (0.2 mm)', 'same body (0.7 mm)') and moves_of.get(r['cadasio']):
        r['cadasio_moves_mm'] = moves_of[r['cadasio']]
out = dict(
    about='PMG: the published Cadasio guide 19075-piano_memory_game_pmg-full_build mapped onto PMG Build Instructions/pmg.glb. mm, assembly frame, Y up. Written by docs/research/pmg/scripts/build_map.py, 19 Oct 2026.',
    frame=dict(mm_per_cadasio_unit=TREE['scale_mm_per_unit'], relation='identity (Cadasio units x 23.6076 = GLB mm; same axes)',
               note='a Cadasio position override is in its parent frame: offsets here are world offsets (turned by the part rotation)'),
    summary=dict(
        step_vs_published='pmg.glb is an earlier state of the CAD the published guide used (Cadasio CAD version 7, 2026-08-04): 159 of 415 Cadasio components identical; see cadasio_map.md section 2',
        built_pose=dict(io_module='NAUO78 (turned 180 deg about X against the published copy)', nano='inside NAUO78', buttons={'black': 'NAUO76', 'yellow': 'NAUO83', 'white': 'NAUO84', 'blue': 'NAUO85'},
                        display='NAUO79', matrix='NAUO81', usb=['NAUO282 plug', 'NAUO285 lead', 'NAUO283 A end'], wood='NAUO60-75, NAUO77'),
        buttons=[dict(colour='black', cap='#000000', pin_row='D4', bench='NAUO7', case='NAUO76', case_z=1241.8, key='NAUO72'),
                 dict(colour='yellow', cap='#ffdc00', pin_row='D5', bench='NAUO6', case='NAUO83', case_z=1274.3, key='NAUO71'),
                 dict(colour='white', cap='#ffffff', pin_row='D6', bench='NAUO5', case='NAUO84', case_z=1306.9, key='NAUO70'),
                 dict(colour='blue', cap='#0074d9', pin_row='D7', bench='NAUO4', case='NAUO85', case_z=1339.4, key='NAUO69')],
        front='-X (H1); student right = +Z'),
    viewer_steps=[dict(v=v['v'], name=v['name'], behaviour=v['behaviour'], up_axis=v['up_axis'], camera=v['camera']) for v in V],
    wires=wires_out, caps=caps_out, glb_instances=glb_out, cadasio_components=cad_out,
    module_pins_local=WI['module_pins'], shield_pins_world=WI['shield_pins'])
json.dump(out, open(ROOT + '/docs/research/pmg/cadasio_map.json', 'w'), indent=1, ensure_ascii=False)
print('wrote', len(glb_out), 'GLB rows,', len(cad_out), 'Cadasio rows,', len(wires_out), 'wires')
unknown = [k for k, r in glb_out.items() if r['role'] == '?' or r['role'].startswith('wire body')]
print('unclassified', unknown)
