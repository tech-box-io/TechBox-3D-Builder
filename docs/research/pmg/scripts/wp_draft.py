"""Pass 6: group the measured wire bodies into the 21 wires of the build and their poses, and write
docs/research/pmg/wire-paths-draft.json (format as the MRA's / RCC's wire-paths.json where it fits). Prints the tables the
report quotes.

Inputs (scratchpad, made by the other wp_ scripts): wires_raw.json (wp_extract), caps_pins.json (wp_caps_pins),
links.json (wp_links), cadasio_wires.json (wp_cadasio_replay), cadasio_match.json (wp_cadasio_match).
"""
import json, collections
import numpy as np

SP = '/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/bc7f208e-dd24-481f-9696-6a220688eb27/scratchpad/'
OUT = '/Users/lee-johnson/Desktop/Claude_Cadasio/docs/research/pmg/wire-paths-draft.json'
raw = json.load(open(SP + 'wires_raw.json'))
cp = json.load(open(SP + 'caps_pins.json'))
links = json.load(open(SP + 'links.json'))
cw = json.load(open(SP + 'cadasio_wires.json'))
cm = json.load(open(SP + 'cadasio_match.json'))
VIEWER = cw['viewer']

# ---------------------------------------------------------------- devices and their pins
BUTTONS_BENCH = {1: 'NAUO7', 2: 'NAUO6', 3: 'NAUO5', 4: 'NAUO4'}          # button n is wired to row n + 3 (Cadasio Steps 3 - 14)
BUTTONS_CASE = {1: 'NAUO76', 2: 'NAUO83', 3: 'NAUO84', 4: 'NAUO85'}       # (from the CAD's own wiring: G4 -> NAUO76 and so on)
DISPLAYS = {'NAUO80': 'bench', 'NAUO129': 'held 80 mm to the side of its seat (+Z), above the brackets', 'NAUO79': 'seated on the brackets'}
MATRICES = {'NAUO44': 'bench', 'NAUO82': 'held 143 mm in front of its seat (-Z)', 'NAUO267': 'held 86 mm above its seat', 'NAUO81': 'seated on the brackets'}
MODULES = {'NAUO1': 'bench (flat, pins up)', 'NAUO94': 'held 104.7 mm above its place on H4', 'NAUO78': 'on H4 (seated)'}

# Pin names by physical pin (index k = the order wp_caps_pins.py found them in on the reference pose, carried to every pose of
# the same part, so k is the same physical pin in every pose). Names as the PUBLISHED guide has them (its pin labels, carried
# through Cadasio's own transforms to every pose; see cad_wire_paths.md section 3):
#   button (reference NAUO7, -z to +z): 0 VCC, 1 OUT, 2 GND   (the STEP wires its G-row wires to pin 0)
#   display (NAUO80, low y to high y): 0 GND, 1 VCC, 2 DIO, 3 CLK   (the STEP agrees in every pose)
#   matrix (NAUO44, low y to high y): 0 VCC, 1 GND, 2 DIN, 3 CS, 4 CLK   (the STEP agrees in the case; its bench matrix is wired the reverse way)
BUTTON_PIN = {0: 'VCC', 1: 'OUT', 2: 'GND'}
DISPLAY_PIN = {0: 'GND', 1: 'VCC', 2: 'DIO', 3: 'CLK'}
MATRIX_PIN = {0: 'VCC', 1: 'GND', 2: 'DIN', 3: 'CS', 4: 'CLK'}

WIRES = []                                     # the 21 wires, in the published guide's order
for n in (1, 2, 3, 4):
    row = n + 3
    for pin, col in (('VCC', 'V'), ('OUT', 'S'), ('GND', 'G')):
        WIRES.append(dict(id=f'button{n} {pin}', device=f'button {n}', device_pin=pin, module_pin=f'{col}{row}'))
for pin, mp in (('CLK', 'S8'), ('DIO', 'S9'), ('VCC', 'V9'), ('GND', 'G9')):
    WIRES.append(dict(id=f'display {pin}', device='display', device_pin=pin, module_pin=mp))
for pin, mp in (('VCC', 'V11'), ('GND', 'G11'), ('DIN', 'S11'), ('CS', 'S12'), ('CLK', 'S13')):
    WIRES.append(dict(id=f'matrix {pin}', device='matrix', device_pin=pin, module_pin=mp))
BY_MODULE_PIN = {w['module_pin']: w for w in WIRES}


def device_kind(inst):
    if inst in BUTTONS_BENCH.values() or inst in BUTTONS_CASE.values():
        return 'button'
    if inst in DISPLAYS:
        return 'display'
    if inst in MATRICES:
        return 'matrix'
    if inst in MODULES:
        return 'module'
    return None


def device_pin_name(inst, pin):
    k = int(pin[3:])
    return {'button': BUTTON_PIN, 'display': DISPLAY_PIN, 'matrix': MATRIX_PIN}[device_kind(inst)][k]


def button_number(inst):
    for n, i in list(BUTTONS_BENCH.items()) + list(BUTTONS_CASE.items()):
        if i == inst:
            return n


# ---------------------------------------------------------------- Cadasio: colour of each wire, use of each body
cad_by_ours = collections.defaultdict(list)
for r in cm['rows']:
    if r.get('ours'):
        cad_by_ours[r['ours']].append(r)
# each of the 21 wires has its own colour in the published guide (the routed wire of its Step Nc)
GUIDE_STEPS = {'button1 VCC': 3, 'button1 OUT': 4, 'button1 GND': 5, 'button2 VCC': 6, 'button2 OUT': 7, 'button2 GND': 8,
               'button3 VCC': 9, 'button3 OUT': 10, 'button3 GND': 11, 'button4 VCC': 12, 'button4 OUT': 13, 'button4 GND': 14,
               'display CLK': 16, 'display DIO': 17, 'display VCC': 18, 'display GND': 19,
               'matrix VCC': 20, 'matrix GND': 21, 'matrix DIN': 22, 'matrix CS': 23, 'matrix CLK': 24}
comp_by_name = {c['name']: c for c in cw['comps']}
wire_comps = [c for c in cw['comps'] if (c['base'] or '').split('^')[0].replace(' [Default]', '').startswith(('Part', 'Copy', 'G11', 'S1 ', 'S12', 'S13', 'V11'))]
for w in WIRES:
    sn = GUIDE_STEPS[w['id']]
    vi_c = VIEWER.index(f'Step {sn}c')
    vi_n = VIEWER.index(f'Step {sn}')
    # the routed wire = a wire component that first shows at Step Nc; the token = one shown at Step N and gone at Nc
    routed = [c for c in wire_comps if c['steps'] and c['steps'][0] == vi_c and vi_n not in c['steps']]
    token = [c for c in wire_comps if vi_n in c['steps'] and vi_c not in c['steps']]
    w['published_step'] = f'Step {sn}'
    w['colour'] = list(routed[0]['colours'])[0] if routed else None
    w['cadasio_routed_on_bench'] = routed[0]['name'] if routed else None
    w['cadasio_token'] = token[0]['name'] if token else None
    w['cadasio_token_colour'] = list(token[0]['colours'])[0] if token else None

# ---------------------------------------------------------------- the jumper-wire bodies, oriented device -> module
jumpers = []
taken = collections.Counter()                  # (module, device, module pin) -> how many bodies of that pose end on it
for lk in links.values():
    devs = [lk[e]['device'] for e in 'ab']
    if any(d in MODULES for d in devs) and all(devs):
        m_end = 'a' if lk['a']['device'] in MODULES else 'b'
        d_end = 'b' if m_end == 'a' else 'a'
        taken[(lk[m_end]['device'], lk[d_end]['device'], lk[m_end]['pin'])] += 1
for wid, lk in links.items():
    a, b = lk['a'], lk['b']
    ends = {'a': a, 'b': b}
    mod = [e for e in 'ab' if ends[e]['device'] in MODULES]
    dev = [e for e in 'ab' if ends[e]['device'] and ends[e]['device'] not in MODULES]
    w = raw[wid]
    pts = np.array(w['points'])
    row = dict(body=wid, mesh=w['mesh'], radius_mm=w['radius_mm'], length_mm=w['length_mm'])
    if not mod:                                # a loose straight wire (no pins)
        row.update(kind='loose', cap_a=a['cap'], cap_b=b['cap'])
        jumpers.append(row)
        continue
    me, de = mod[0], dev[0]
    if de == 'b':                              # points from the device end to the module end
        pts = pts[::-1]
    mi, di = ends[me]['device'], ends[de]['device']
    mp = ends[me]['pin']
    dname = device_pin_name(di, ends[de]['pin'])
    kind = device_kind(di)
    prefix = f"button{button_number(di)}" if kind == 'button' else kind
    by_mod = BY_MODULE_PIN.get(mp)
    if by_mod and by_mod['id'].startswith(prefix + ' ') and (taken[(mi, di, mp)] == 1 or by_mod['device_pin'] == dname):
        wire = by_mod['id']
    else:
        wire = f'{prefix} {dname}'                # (a CAD slip: wrong module pin) named by the device pin it is on
    expected = next(x for x in WIRES if x['id'] == wire)
    row.update(kind='routed', wire=wire, device_pin_as_published=(dname == expected['device_pin']), module=mi, module_pin=mp, module_cap=ends[me]['cap'], module_cap_gap_mm=ends[me]['gap_mm'],
               device=di, device_pin=dname, device_pin_index=int(ends[de]['pin'][3:]), device_cap=ends[de]['cap'], device_cap_gap_mm=ends[de]['gap_mm'],
               module_pin_as_expected=(mp == expected['module_pin']), expected_module_pin=expected['module_pin'],
               device_end=np.round(pts[0], 3).tolist(), device_end_direction=np.round((pts[0] - pts[2]) / np.linalg.norm(pts[0] - pts[2]), 4).tolist(),
               module_end=np.round(pts[-1], 3).tolist(), module_end_direction=np.round((pts[-1] - pts[-3]) / np.linalg.norm(pts[-1] - pts[-3]), 4).tolist(),
               in_published_guide=[c['name'] for c in cad_by_ours.get(wid, []) if c['steps']],
               points=np.round(pts, 2).tolist())
    jumpers.append(row)

# poses
POSES = collections.OrderedDict()


def pose_key(j):
    m, d = j['module'], j['device']
    kind = device_kind(d)
    if kind == 'button':
        return f"buttons {'bench' if d in BUTTONS_BENCH.values() else 'in case'} / module {m}"
    if kind == 'display':
        return f'display {d} / module {m}'
    return f'matrix {d} / module {m}'


for j in jumpers:
    if j['kind'] == 'routed':
        POSES.setdefault(pose_key(j), []).append(j)

POSE_NOTES = {
    'buttons bench / module NAUO1': 'Bench: the four buttons float in a row behind the module (Steps 3 - 14 of the published guide). Only GND and OUT are modelled.',
    'buttons in case / module NAUO1': 'Buttons clipped into H6, module still on the bench (published Steps 33 - 45).',
    'buttons in case / module NAUO94': 'Buttons in H6, module held 104.7 mm above its place on H4 (published Step 45c - 46; the published module is turned half a turn there).',
    'buttons in case / module NAUO78': 'Buttons in H6, module on H4 (published Step 46c on; the published module is turned half a turn there).',
    'display NAUO80 / module NAUO1': 'Bench (published Steps 16 - 19).',
    'display NAUO80 / module NAUO94': 'Display on the bench, module held above H4.',
    'display NAUO80 / module NAUO78': 'Display on the bench, module on H4.',
    'display NAUO129 / module NAUO78': 'Display held 80 mm to the side of its seat (+Z), module on H4. Not a pose of the published guide.',
    'display NAUO79 / module NAUO78': 'Display seated on the brackets, module on H4 (the finished game).',
    'matrix NAUO44 / module NAUO1': 'Bench (published Steps 20 - 24; the published bench matrix is turned end for end and 29.4 mm further along +Z).',
    'matrix NAUO44 / module NAUO94': 'Matrix on the bench, module held above H4.',
    'matrix NAUO44 / module NAUO78': 'Matrix on the bench, module on H4.',
    'matrix NAUO82 / module NAUO78': 'Matrix held 143 mm in front of its seat (-Z), module on H4. Its GND wire is on G9 in the CAD.',
    'matrix NAUO81 / module NAUO78': 'Matrix seated on the brackets, module on H4 (the finished game).',
    'matrix NAUO81 / module NAUO1': 'Matrix seated, module still on the bench: not a state of the published build order.',
    'matrix NAUO81 / module NAUO94': 'Matrix seated, module held above H4: not a state of the published build order.',
    'matrix NAUO267 / module NAUO1': 'Matrix held 86 mm above its seat, module on the bench: not a state of the published build order. CS wire missing, GND wire on S11.',
}

# per wire: its body in each pose, length and caps
for w in WIRES:
    w['poses'] = collections.OrderedDict()
    for pk, js in POSES.items():
        hit = [j for j in js if j['wire'] == w['id']]
        if hit:
            j = hit[0]
            w['poses'][pk] = dict(body=j['body'], length_mm=j['length_mm'], device_cap=j['device_cap'], module_cap=j['module_cap'],
                                  module_pin=j['module_pin'], device_pin=j['device_pin'],
                                  **({} if j['module_pin_as_expected'] else {'WRONG_MODULE_PIN_in_STEP': True}),
                                  **({} if j['device_pin_as_published'] else {'WRONG_DEVICE_PIN_in_STEP': True}))
        else:
            dev_kinds = {device_kind(j['device']) for j in js}
            if w['device'].split()[0] in dev_kinds:
                w['poses'][pk] = None                 # the pose exists for this device but the CAD has no body for this wire
    L = [p['length_mm'] for p in w['poses'].values() if p]
    w['length_spread_mm'] = [min(L), max(L)] if L else None

# ---------------------------------------------------------------- loose straight wires (the tokens and the two ribbons)
loose = [j for j in jumpers if j['kind'] == 'loose']
ribbon12 = sorted([j for j in loose if j['mesh'].startswith('Copy')], key=lambda j: raw[j['body']]['end_a'][0])
ribbon9 = sorted([j for j in loose if j['mesh'].startswith('Part')], key=lambda j: -raw[j['body']]['end_a'][0])


def offsets_of(inst):
    for c in cad_by_ours.get(inst, []):
        return {VIEWER[int(k)]: v for k, v in c['offsets'].items()}, [VIEWER[s] for s in c['steps']]
    return {}, []


tok = {}
for j in loose:
    offs, steps = offsets_of(j['body'])
    j['published'] = dict(steps=steps, offsets_mm=offs)
    c = cad_by_ours.get(j['body'])
    j['published_colour'] = list(c[0]['colours'])[0] if c and c[0]['colours'] else None
    j['points'] = raw[j['body']]['points']
    j['end_a'], j['end_b'] = raw[j['body']]['end_a'], raw[j['body']]['end_b']
# the four straight wires the STEP lacks (Cadasio "Copy (2) of Copy of Part17-3 .. -6"): NAUO222 and its caps moved along +X
missing_tokens = []
for c in cw['comps']:
    if c['name'].startswith('Copy (2) of Copy of Part17^PMG Full 3D Cadasio Build-') and not c['name'].endswith('-2'):
        ref = next(x for x in cw['comps'] if x['name'] == 'Copy (2) of Copy of Part17^PMG Full 3D Cadasio Build-2')
        dx = np.round(np.array(c['lo']) - np.array(ref['lo']), 2).tolist()
        missing_tokens.append(dict(cadasio=c['name'], copy_of='NAUO222', shift_mm=dx, caps_copy_of=['NAUO211', 'NAUO215'],
                                   published_steps=[VIEWER[s] for s in c['steps']], colour=list(c['colours'])[0] if c['colours'] else None,
                                   offsets_mm={VIEWER[int(k)]: v for k, v in c['offsets'].items()}))

# ---------------------------------------------------------------- USB cable
usb = {}
for body, plug, aend, module, what in (('NAUO277', 'NAUO279', 'NAUO278', 'NAUO1', 'bench (published Step 25 - 45)'),
                                        ('NAUO284', 'NAUO281', 'NAUO280', 'NAUO94', 'module held above H4'),
                                        ('NAUO285', 'NAUO282', 'NAUO283', 'NAUO78', 'module on H4')):
    w = raw[body]
    pts = np.array(w['points'])
    plug_c = np.array(cp['plugs'][plug]) if 'plugs' in cp else None
    if plug_c is not None and np.linalg.norm(pts[-1] - plug_c) < np.linalg.norm(pts[0] - plug_c):
        pts = pts[::-1]                        # from the Mini-B plug to the A end
    usb[body] = dict(pose=what, module=module, mini_b_plug=plug, a_end=aend, radius_mm=w['radius_mm'], length_mm=w['length_mm'],
                     raw_end_a=w['end_a'], raw_end_b=w['end_b'], check=w['check'], points=np.round(pts, 2).tolist())

# ---------------------------------------------------------------- write
doc = collections.OrderedDict()
doc['_about'] = dict(
    what='DRAFT. Centre lines of every flexible thing in pmg.glb (Piano Memory Game), measured from the CAD: 109 jumper-wire bodies, '
         '3 USB-cable bodies. Written by the PMG wire-path study, 19 Oct 2026; see docs/research/pmg/cad_wire_paths.md. '
         'Not yet in the kit folder: copy to "PMG Build Instructions/wire-paths.json" when the guide author takes it.',
    units='millimetres, assembly space of pmg.glb (Y up), the pose each body is modelled in',
    conductors='Top-level keys NAUOn: the round tube(s) of that instance, as the MRA/RCC files: solid (always 0: every body is one wire), '
               'radius_mm, length_mm, end_a / end_b = centres of the two flat end faces, dir_a / dir_b = the way the wire points out of '
               'each end, points = centre line from end_a to end_b every 1 mm (end faces exact), check = distance of the tube\'s side '
               'vertices from the line (equals the radius).',
    jumper_wires='One entry per routed jumper-wire body, oriented from the device (button / display / matrix) to the I/O module: '
                 'device + device_pin + device_cap, module + module_pin + module_cap, the two end points and directions, points. '
                 'module_pin_as_expected = false marks a CAD slip (the wire is on the wrong module pin).',
    wires='The 21 wires of the build in the published order: device pin, module pin, published step, colour in the published guide, '
          'and the body that draws it in each pose of the CAD (null = the pose exists but the CAD has no body for this wire).',
    caps='Every Dupont cap: kind (Wire Cap 8 mm, Wire Cap V2 12 mm), centre, axis (unit, along its length), face_plus / face_minus '
         '= centres of its two end faces, the pin it sits on (device, pin) and the wire bodies that end in it.',
    pins='Pin tips (assembly mm) of every device pose, and each pose\'s pin direction (the way the pin points, i.e. the way a cap '
         'is pushed off it). Module pins named "D4 G" etc. (row, column), as docs/research/mra/cad_pins.json.',
    loose_wires='The straight 58 mm wires lying beside the bench (the published guide\'s "tokens", Steps 2 / 15 and every Step N of '
                'a wire), with the offsets the published guide gives them (Cadasio position minus CAD place, mm, by viewer step).',
    usb='The USB cable in its three poses, from the right-angle Mini-B plug to the A end. radius 2.3 mm.',
    colours='pmg.glb has a single default material: no wire has a colour of its own. Colours here are the published Cadasio '
            'guide\'s (hex), one per wire.',
)
for wid in sorted(raw, key=lambda s: int(s[4:])):
    w = raw[wid]
    doc[wid] = [dict(solid=0, mesh=w['mesh'], colour=None, radius_mm=w['radius_mm'], length_mm=w['length_mm'], end_a=w['end_a'], end_b=w['end_b'],
                     dir_a=w['dir_a'], dir_b=w['dir_b'], n_points=w['n_points'], points=w['points'], check=w['check'])]
doc['wires'] = WIRES
doc['poses'] = {pk: dict(note=POSE_NOTES.get(pk, ''), bodies=[j['body'] for j in js]) for pk, js in POSES.items()}
doc['jumper_wires'] = [j for j in jumpers if j['kind'] == 'routed']
# caps with the wires that end in them
ends_in = collections.defaultdict(list)
for wid, lk in links.items():
    for e in 'ab':
        ends_in[lk[e]['cap']].append(dict(body=wid, wire_face=lk[e]['wire_face'], gap_mm=lk[e]['gap_mm']))
caps = {}
for cid, c in sorted(cp['caps'].items(), key=lambda kv: int(kv[0][4:])):
    on = None
    for wid, lk in links.items():
        for e in 'ab':
            if lk[e]['cap'] == cid and lk[e]['device']:
                on = dict(device=lk[e]['device'], pin=lk[e]['pin'] if lk[e]['device'] in MODULES else device_pin_name(lk[e]['device'], lk[e]['pin']),
                          pin_index=None if lk[e]['device'] in MODULES else int(lk[e]['pin'][3:]), pin_off_axis_mm=lk[e]['pin_off_axis_mm'])
    if on is None:                             # a cap no wire ends in: find its pin directly
        ctr, ax, half = np.array(c['centre']), np.array(c['axis']), c['length_mm'] / 2
        for kind, table, names in (('matrices', cp['devices']['matrices'], MATRIX_PIN), ('displays', cp['devices']['displays'], DISPLAY_PIN),
                                   ('buttons', cp['devices']['buttons'], BUTTON_PIN)):
            for dv, tips in table.items():
                for k, tip in enumerate(tips):
                    v = np.array(tip) - ctr
                    if abs(v @ ax) <= half + 0.5 and np.linalg.norm(v - ax * (v @ ax)) < 1.0:
                        on = dict(device=dv, pin=names[k], pin_index=k, pin_off_axis_mm=round(float(np.linalg.norm(v - ax * (v @ ax))), 2))
    caps[cid] = dict(c, sits_on=on, wires=ends_in.get(cid, []))
doc['caps'] = caps
# which cap sits on which pin, per device pose (the cap is the same physical cap in every wire that uses that pin in that pose)
on_pins = collections.defaultdict(dict)
for cid, c in caps.items():
    if c['sits_on']:
        on_pins[c['sits_on']['device']][c['sits_on']['pin']] = cid
doc['caps_on_pins'] = dict(sorted(on_pins.items(), key=lambda kv: int(kv[0][4:])))
for w in WIRES:                               # the caps each of the 21 wires would use, pose by pose, by the pins it belongs on
    w['module_cap_by_module_pose'] = {m: on_pins[m].get(w['module_pin']) for m in MODULES}
    devs = ([BUTTONS_BENCH[int(w['device'][-1])], BUTTONS_CASE[int(w['device'][-1])]] if w['device'].startswith('button')
            else list(DISPLAYS) if w['device'] == 'display' else list(MATRICES))
    w['device_cap_by_device_pose'] = {dv: on_pins[dv].get(w['device_pin']) for dv in devs}
pins = dict(module=cp['module_pins'], module_pin_direction=cp['module_pin_dir'], pin_direction=cp['devices']['pin_dirs'],
            buttons={k: dict(tips=v, names=[BUTTON_PIN[i] for i in range(3)]) for k, v in cp['devices']['buttons'].items()},
            displays={k: dict(tips=v, names=[DISPLAY_PIN[i] for i in range(4)]) for k, v in cp['devices']['displays'].items()},
            matrices={k: dict(tips=v, names=[MATRIX_PIN[i] for i in range(5)]) for k, v in cp['devices']['matrices'].items()},
            note='Device pins are listed in the same physical order in every pose of a device (index k is the same pin). Buttons: '
                 'k = 0, 1, 2 from -z to +z on the bench button NAUO7. Display: k = 0..3 from low y to high y on NAUO80. Matrix: k = 0..4 '
                 'from low y to high y on NAUO44.')
doc['pins'] = pins
doc['loose_wires'] = dict(ribbon_12=[dict({k: v for k, v in j.items() if k not in ('kind',)}) for j in ribbon12],
                          ribbon_9=[dict({k: v for k, v in j.items() if k not in ('kind',)}) for j in ribbon9],
                          missing_from_STEP=missing_tokens)
doc['usb'] = usb
json.dump(doc, open(OUT, 'w'), separators=(',', ':'))     # one line, as the MRA's and RCC's files

# ---------------------------------------------------------------- tables for the report
print('POSES')
for pk, js in POSES.items():
    print(f'  {pk}: ' + ', '.join(f"{j['body']} {j['wire']} {j['length_mm']:.1f}{'' if j['module_pin_as_expected'] else ' WRONG MODULE PIN ' + j['module_pin']}{'' if j['device_pin_as_published'] else ' (on ' + j['device_pin'] + ')'}" for j in js))
print('WIRES')
for w in WIRES:
    ps = ' | '.join(f"{('-' if p is None else p['body'] + ' ' + format(p['length_mm'], '.1f'))}" for pk, p in w['poses'].items())
    print(f"  {w['id']:13s} {w['module_pin']:4s} {w['published_step']:8s} {str(w['colour']):8s} spread {w['length_spread_mm']}  {ps}")
print('LOOSE ribbon12', [(j['body'], j['published_colour'], j['published']['steps'][-1:] if j['published']['steps'] else None) for j in ribbon12])
print('LOOSE ribbon9', [(j['body'], j['published_colour'], j['published']['steps'][-1:] if j['published']['steps'] else None) for j in ribbon9])
print('MISSING tokens', [(m['cadasio'][-2:], m['shift_mm'], m['colour'], m['published_steps']) for m in missing_tokens])
print('USB', {k: (v['length_mm'], v['radius_mm'], v['check']['p01'], v['check']['p99']) for k, v in usb.items()})
