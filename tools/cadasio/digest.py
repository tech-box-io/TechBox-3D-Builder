"""Reduce a published Cadasio guide to a readable per-step digest.

    python tools/cadasio/digest.py <payload.json> <output folder>

<payload.json> is what the public viewer endpoint returns for a guide:
    https://api.cadasio.com/api/getProjectViewer?id=<guide id>&withSteps=true&hostname=instructions.online
Writes <guide id>.md (one block per step the student sees) and <guide id>.json (the same, as data).

How the payload is read (see docs/cadasio-patterns.md, Appendix A):
  * Step `properties` are changes on top of the previous step in `orderedSteps`, hidden steps included.
  * Visibility is per solid: a solid starts hidden if it or any ancestor carries the CAD "hidden" flag
    and is then switched only by its own entries.
  * A part's `position` replaces the translation of its CAD transform, so its offset from the assembled
    pose is position minus that translation. mm = scene units / assemblyStructure.scaleFactor.
"""
import json, sys, os, re, math, collections

src, out_dir = sys.argv[1], sys.argv[2]
gid = os.path.basename(src)[:-5]
j = json.load(open(src))
steps, order, tcp, A = j['steps'], j['orderedSteps'], j['toolboxComponentsProperties'], j['assemblyStructure']
SF = A.get('scaleFactor') or 1.0
MM = 1.0 / SF
rv = A['rootVersions']

# ---------- assembly tree ----------
refs = {}
def walk(n, parent, depth):
    r = n['rootReference']
    t = [float(x) for x in (r.get('transform') or '').split(',')] if r.get('transform') else []
    refs[r['id']] = dict(name=r['name'], parent=parent, depth=depth, ver=r['childVersionId'], hidden=bool(r.get('hidden')), kids=[c['rootReference']['id'] for c in n.get('children') or []],
                         home=tuple(t[12:15]) if len(t) == 16 else (0.0, 0.0, 0.0))
    for c in n.get('children') or []:
        walk(c, r['id'], depth + 1)
walk(A, None, 0)
root_id = A['rootReference']['id']
leaves = [k for k, v in refs.items() if not v['kids']]
def chain(k):
    out = []
    while k is not None:
        out.append(k); k = refs[k]['parent']
    return out
CHAIN = {k: chain(k) for k in leaves}
def top(k):  # depth-1 ancestor = what a student would call a part
    c = CHAIN[k] if k in CHAIN else chain(k)
    return c[-2] if len(c) >= 2 else c[-1]
TOP = {k: top(k) for k in leaves}
top_leaves = collections.defaultdict(list)
for k in leaves: top_leaves[TOP[k]].append(k)
def short(name):
    return name.split('/')[-1]

# ---------- colours ----------
def kd_hex(mtl):
    m = re.search(r'Kd\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)', mtl or '')
    if not m: return None
    return '#%02x%02x%02x' % tuple(max(0, min(255, round(float(x) * 255))) for x in m.groups())
PALETTE = {'black': (20, 20, 20), 'dark grey': (70, 70, 70), 'grey': (140, 140, 140), 'light grey': (205, 205, 205), 'white': (250, 250, 250),
           'red': (215, 30, 30), 'orange': (240, 140, 30), 'yellow': (240, 220, 40), 'green': (50, 160, 60), 'dark green': (20, 90, 40), 'blue': (30, 80, 200),
           'light blue': (120, 200, 250), 'navy': (15, 30, 100), 'purple': (130, 60, 170), 'pink': (240, 120, 180), 'brown': (110, 65, 30), 'tan/wood': (225, 190, 140),
           'gold': (200, 160, 50), 'silver': (185, 190, 195)}
def cname(hx):
    if not hx or not re.match(r'^#[0-9a-fA-F]{6}$', hx): return str(hx)
    r, g, b = int(hx[1:3], 16), int(hx[3:5], 16), int(hx[5:7], 16)
    return min(PALETTE, key=lambda n: sum((a - c) ** 2 for a, c in zip(PALETTE[n], (r, g, b))))
base_col = {k: kd_hex((rv.get(refs[k]['ver']) or {}).get('versionMtlData')) for k in leaves}

# ---------- cumulative state ----------
vis = {k: not any(refs[a]['hidden'] for a in chain(k)) for k in refs}      # hidden is inherited once, at the start
pos = {}; rot = {}; col = {}; style = {}
tb = {k: dict(v) for k, v in tcp.items()}
for t in tb.values(): t.setdefault('visible', False)
cam = dict((j.get('cameraProperties') or {}).get('default_camera') or {})
scene = {}
for sc in (j.get('scenes') or {}).values(): scene.update(sc)
scene_ids = set((j.get('scenes') or {}).keys())

def eff_vis(k): return vis[k]                                          # per solid from then on
def eff_pos(k):
    x = y = z = 0.0
    for a in CHAIN[k]:
        p = pos.get(a)
        if p:                                           # offset from the assembled pose = position - CAD translation
            h = refs[a]['home']; x += p[0] - h[0]; y += p[1] - h[1]; z += p[2] - h[2]
    return (x, y, z)
def eff_rot(k):
    return tuple(json.dumps(rot[a], sort_keys=True) for a in CHAIN[k] if a in rot)
def eff_col(k):
    for a in CHAIN[k]:
        if a in col: return col[a]
    return base_col.get(k)

def snap():
    return dict(vis={k: eff_vis(k) for k in leaves}, pos={k: eff_pos(k) for k in leaves}, rot={k: eff_rot(k) for k in leaves},
                tb={k: json.dumps(v, sort_keys=True) for k, v in tb.items()}, tbv={k: bool(v.get('visible')) for k, v in tb.items()}, cam=dict(cam), scene=dict(scene))

def v3(d): return (float(d.get('x', 0)), float(d.get('y', 0)), float(d.get('z', 0)))
def fmt_mm(v): return '(' + ', '.join('%+.0f' % (c * MM) for c in v) + ')'
def norm(v): return math.sqrt(sum(c * c for c in v))
def axis_word(v):
    n = norm(v)
    if n < 1e-9: return 'none'
    names = [('+X', '-X'), ('+Y (up)', '-Y (down)'), ('+Z', '-Z')]
    parts = [names[i][0 if v[i] > 0 else 1] for i in range(3) if abs(v[i]) / n > 0.35]
    return ' & '.join(parts)
def strip_html(s):
    s = re.sub(r'<br\s*/?>|</p>', ' / ', s or '')
    s = re.sub(r'<[^>]+>', '', s).replace('&nbsp;', ' ').replace('​', '')
    return re.sub(r'(\s*/\s*)+$', '', re.sub(r'\s+', ' ', s)).strip()
def ref_label(rid):
    if rid not in refs: return '?' + str(rid)[:8]
    c = chain(rid)
    names = [short(refs[a]['name']) for a in reversed(c)][1:]
    return ' > '.join(names[:3]) if names else refs[rid]['name']

def group_summary(ids):
    """Collapse leaf ids into student-level parts: 'Name (n/N leaves) [colours]'."""
    by = collections.defaultdict(list)
    for k in ids: by[TOP[k]].append(k)
    rows = []
    for t, ks in by.items():
        cols = collections.Counter(cname(eff_col(k)) for k in ks)
        partial = len(ks) < len(top_leaves[t])
        sub = ''
        if partial:
            subs = collections.Counter(short(refs[CHAIN[k][-3]]['name']) if len(CHAIN[k]) >= 3 else short(refs[k]['name']) for k in ks)
            sub = ' sub-parts: ' + ', '.join(f'{n}' + (f'×{c}' if c > 1 else '') for n, c in subs.most_common(5)) + (' …' if len(subs) > 5 else '')
        rows.append(dict(top=t, name=refs[t]['name'], n=len(ks), total=len(top_leaves[t]), partial=partial, sub=sub,
                         colours=', '.join(f'{c}' for c, _ in cols.most_common(3))))
    rows.sort(key=lambda r: r['name'])
    return rows
def base_name(n): return re.sub(r'[-_ ]?\d+$', '', n)
def fmt_groups(rows, limit=14):
    if not rows: return 'none'
    if len(rows) > limit:
        agg = collections.Counter(base_name(r['name']) for r in rows)
        return f'{len(rows)} parts — ' + '; '.join(f'{n} ×{c}' for n, c in agg.most_common(12)) + (' …' if len(agg) > 12 else '')
    return '; '.join(f"{r['name']}" + (f" ({r['n']}/{r['total']} solids){r['sub']}" if r['partial'] else '') + f" [{r['colours']}]" for r in rows)

def tb_desc(k, t):
    ty = t.get('type')
    if ty == 'editor':
        text = strip_html(t.get('editor_contents') if isinstance(t.get('editor_contents'), str) else '')
        cont = (t.get('container') or {})
        size = re.findall(r'font-size:\s*([\d.]+)em', t.get('editor_contents') or '')
        links = [ref_label(l.get('targetId')) for l in (t.get('links') or []) if isinstance(l, dict)]
        p = t.get('position') or {}
        return dict(kind='label', text=text, container=cont.get('container_type'), border=cont.get('container_colour_border'), fill=cont.get('container_colour_fill'),
                    leader=(t.get('leader') or {}).get('leader_colour_border'), anchor=(t.get('anchor_type') or [''])[0], em=size[0] if size else None,
                    bold='<strong>' in (t.get('editor_contents') or ''), anchored_to=links, screen_xy=(round(p.get('x', 0)), round(p.get('y', 0))), static=t.get('static'))
    if ty == 'image':
        c = t.get('content') or {}
        links = [ref_label(l.get('targetId')) for l in (t.get('links') or []) if isinstance(l, dict)]
        p = t.get('position') or {}
        return dict(kind='image', name=re.sub(r'_\d+$', '', t.get('name') or ''), src=(c.get('src') or '').split('/')[-1].split('?')[0], anchored_to=links,
                    width=t.get('width'), screen_xy=(round(p.get('x', 0)), round(p.get('y', 0))), leader=(t.get('leader') or {}).get('leader_colour_border'), static=t.get('static'))
    if ty in ('line', 'arrow'):
        pts = t.get('points') or []
        L = norm([a - b for a, b in zip(v3(pts[0]), v3(pts[-1]))]) * MM if len(pts) >= 2 else None
        d = axis_word([b - a for a, b in zip(v3(pts[0]), v3(pts[-1]))]) if len(pts) >= 2 else None
        oid = t.get('object_ids') or {}
        oid = list(oid.values()) if isinstance(oid, dict) else list(oid)
        return dict(kind='lead line' if ty == 'line' else 'arrow', sub=t.get('sub_type'), colour=t.get('colour_main'), style=t.get('style'), n_points=len(pts),
                    length_mm=round(L, 1) if L is not None else None, direction=d, anchored_to=[ref_label(o) for o in oid], name=re.sub(r'_\d+$', '', t.get('name') or ''))
    return dict(kind=ty)
def fmt_tb(d):
    k = d['kind']
    if k == 'label':
        return f"LABEL \"{d['text']}\" ({d['container']}, border {d['border']}, leader {d['leader']}, {d['em']}em{' bold' if d['bold'] else ''}, screen {d['screen_xy']}%) → {', '.join(d['anchored_to']) or 'no anchor'}"
    if k == 'image':
        return f"IMAGE {d['name']} [{d['src'][-22:]}] (w={d['width']}, screen {d['screen_xy']}%) → {', '.join(d['anchored_to']) or 'no anchor'}"
    if k in ('lead line', 'arrow'):
        return f"{k.upper()} {d['colour']} {d.get('style') or d.get('sub')} len≈{d['length_mm']}mm dir {d['direction']} :: {' ⇄ '.join(d['anchored_to']) or 'unanchored'}"
    return str(d)

def cam_view(c):
    if not c.get('position') or not c.get('orbit_target'): return None
    p, t = v3(c['position']), v3(c['orbit_target'])
    d = [a - b for a, b in zip(p, t)]; n = norm(d) or 1
    d = [x / n for x in d]
    return dict(dist_mm=n * MM, elev=math.degrees(math.asin(max(-1, min(1, d[1])))), azim=math.degrees(math.atan2(d[0], d[2])), dir=d, target=t)

# ---------- walk the steps ----------
records = []
prev = snap()
colour_overrides = collections.Counter(); style_overrides = collections.Counter(); edge_overrides = collections.Counter()
for idx, sid in enumerate(order):
    s = steps[sid]; P = s.get('properties') or {}
    for k, p in P.items():
        if not isinstance(p, dict): continue
        if k in refs:
            if p.get('visible') is not None: vis[k] = bool(p['visible'])
            if isinstance(p.get('position'), dict): pos[k] = v3(p['position'])
            if p.get('rotation') is not None: rot[k] = p['rotation']
            if p.get('colour_main'): col[k] = p['colour_main']; colour_overrides[(base_name(short(refs[k]['name'])), p['colour_main'])] += 1
            if p.get('style'): style_overrides[p['style']] += 1
            if p.get('style_edges'): edge_overrides[p['style_edges']] += 1
        elif k in tb:
            for a, b in p.items():
                if a == 'visible' and b is None: continue
                tb[k][a] = b
        elif k == 'default_camera': cam.update(p)
        elif k in scene_ids: scene.update(p)
    if s.get('behaviour') == 'hidden':
        continue
    cur = snap()
    appeared = [k for k in leaves if cur['vis'][k] and not prev['vis'][k]]
    gone = [k for k in leaves if prev['vis'][k] and not cur['vis'][k]]
    moved = collections.defaultdict(list)
    for k in leaves:
        if cur['vis'][k] and prev['vis'][k] and cur['pos'][k] != prev['pos'][k]:
            d = tuple(round(a - b, 4) for a, b in zip(cur['pos'][k], prev['pos'][k]))
            if norm(d) > 1e-4: moved[(TOP[k], d, tuple(round(c, 4) for c in cur['pos'][k]))].append(k)
    rotated = collections.Counter(refs[TOP[k]]['name'] for k in leaves if cur['vis'][k] and prev['vis'][k] and cur['rot'][k] != prev['rot'][k])
    # where do newly appeared parts sit relative to assembled?
    app_off = collections.defaultdict(list)
    for k in appeared: app_off[(TOP[k], tuple(round(c, 4) for c in cur['pos'][k]))].append(k)
    tb_on = [k for k in tb if cur['tbv'][k] and not prev['tbv'][k]]
    tb_off = [k for k in tb if prev['tbv'][k] and not cur['tbv'][k]]
    tb_changed = [k for k in tb if cur['tbv'][k] and prev['tbv'][k] and cur['tb'][k] != prev['tb'][k]]
    tb_visible = [k for k in tb if cur['tbv'][k]]
    cv, pv = cam_view(cur['cam']), cam_view(prev['cam'])
    cam_change = None
    if cv and pv:
        ang = math.degrees(math.acos(max(-1, min(1, sum(a * b for a, b in zip(cv['dir'], pv['dir']))))))
        shift = norm([a - b for a, b in zip(cv['target'], pv['target'])]) * MM
        if ang > 0.5 or shift > 0.5 or abs(cv['dist_mm'] - pv['dist_mm']) > 0.5:
            cam_change = dict(angle_deg=round(ang, 1), target_shift_mm=round(shift), dist_from=round(pv['dist_mm']), dist_to=round(cv['dist_mm']), zoom=round(pv['dist_mm'] / cv['dist_mm'], 2) if cv['dist_mm'] else None)
    displaced = collections.Counter(refs[TOP[k]]['name'] for k in leaves if cur['vis'][k] and norm(cur['pos'][k]) > 1e-4)
    vis_tops = collections.Counter(refs[TOP[k]]['name'] for k in leaves if cur['vis'][k])
    scene_change = {a: b for a, b in cur['scene'].items() if prev['scene'].get(a) != b}
    rec = dict(order_index=idx, name=s['name'], behaviour=s['behaviour'], duration=s.get('animationDuration'), description=strip_html(s.get('description') or ''),
               popup=dict(type=s.get('popupType'), info=strip_html(json.dumps(s.get('popupInfo'))) if s.get('popupInfo') else None, button=s.get('popupButtonText')) if s.get('popupType') not in (None, 'none') else None,
               image=s.get('image'),
               appeared=group_summary(appeared), disappeared=group_summary(gone),
               appeared_offsets=[dict(part=refs[t]['name'], offset_mm=[round(c * MM, 1) for c in off], dist_mm=round(norm(off) * MM, 1), dir=axis_word(off), n=len(ks)) for (t, off), ks in app_off.items()],
               moved=[dict(part=refs[t]['name'], n=len(ks), total=len(top_leaves[t]), delta_mm=[round(c * MM, 1) for c in d], dist_mm=round(norm(d) * MM, 1), dir=axis_word(d),
                           now_offset_mm=[round(c * MM, 1) for c in now], seated=norm(now) < 1e-4) for (t, d, now), ks in moved.items()],
               rotated=dict(rotated),
               tb_on=[tb_desc(k, tb[k]) for k in tb_on], tb_off=[tb_desc(k, tb[k]) for k in tb_off], tb_changed=[tb_desc(k, tb[k]) for k in tb_changed],
               tb_visible_counts=dict(collections.Counter(tb_desc(k, tb[k])['kind'] for k in tb_visible)),
               camera=dict(change=cam_change, dist_mm=round(cv['dist_mm']) if cv else None, elev=round(cv['elev']) if cv else None, azim=round(cv['azim']) if cv else None),
               visible_parts=len(vis_tops), visible_solids=sum(vis_tops.values()), displaced_parts=dict(displaced), scene_change=scene_change)
    records.append(rec)
    prev = cur

# ---------- part / colour inventory ----------
inventory = []
for t, ks in top_leaves.items():
    cols = collections.Counter(eff_col(k) for k in ks)
    inventory.append(dict(name=refs[t]['name'], solids=len(ks), colours=[(c, cname(c), n) for c, n in cols.most_common(6)],
                          ever_visible=any(True for _ in [0])))
inventory.sort(key=lambda r: r['name'])
toolbox_inv = collections.Counter(); label_styles = collections.Counter(); line_styles = collections.Counter(); label_texts = collections.Counter(); images = collections.Counter()
for k, t in tb.items():
    d = tb_desc(k, t); toolbox_inv[d['kind']] += 1
    if d['kind'] == 'label': label_styles[(d['container'], d['border'], d['leader'], d['em'], d['bold'], d['anchor'])] += 1; label_texts[d['text']] += 1
    if d['kind'] in ('lead line', 'arrow'): line_styles[(d['kind'], d['colour'], d.get('style') or d.get('sub'))] += 1
    if d['kind'] == 'image': images[(d['name'], d['src'])] += 1

meta = dict(id=gid, url='https://instructions.online/?id=' + gid, name=j.get('name'), type=j.get('type'), mm_per_unit=round(MM, 3),
            ordered_steps=len(order), viewer_steps=len(records), behaviours=dict(collections.Counter(steps[s]['behaviour'] for s in order)),
            scene={k: scene.get(k) for k in ('colour_main', 'colour_type', 'scene_render_style', 'scene_edge_style', 'scene_edge_colour', 'scene_edge_width', 'scene_edge_angle', 'scene_silhouette_style', 'scene_camera_fov',
                                              'scene_light_intensity_ambient', 'scene_light_intensity_directional', 'scene_light_colour_ambient', 'scene_light_colour_directional', 'scene_light_follow_camera', 'show_viewcube', 'up_axis')},
            part_style_overrides=dict(style_overrides), part_edge_overrides=dict(edge_overrides),
            camera_fov=cam.get('fov'), camera_type=cam.get('type'),
            project_flags={k: j.get(k) for k in ('autoStart', 'animateStepsViewer', 'animatePreviousStep', 'edgesVisibleOnAnimate', 'baseFontSize', 'defaultFont', 'defaultFontColour', 'stepPrefix', 'tooltips', 'viewerNavigationOverlay', 'interactionPrompt', 'transparentBackground', 'forceLandscape', 'speakStepDescriptionViewer', 'chain', 'repeatCount', 'embedSize')},
            animation=dict(duration=dict(collections.Counter(str(steps[s].get('animationDuration')) for s in order)),
                           cad=dict(collections.Counter(json.dumps({k: v for k, v in (steps[s].get('animationOptionsCad') or {}).items()}, sort_keys=True) for s in order)),
                           camera=dict(collections.Counter(json.dumps(steps[s].get('animationOptionsCamera'), sort_keys=True) for s in order))),
            toolbox=dict(toolbox_inv), label_styles=[dict(style=list(k), n=n) for k, n in label_styles.most_common(8)], line_styles=[dict(style=list(k), n=n) for k, n in line_styles.most_common(8)],
            label_texts=label_texts.most_common(80), images=[dict(name=k[0], src=k[1], n=n) for k, n in images.most_common(30)],
            colour_overrides=[dict(part=k[0], colour=k[1], name=cname(k[1]), n=n) for k, n in colour_overrides.most_common(60)])
json.dump(dict(meta=meta, inventory=inventory, steps=records), open(os.path.join(out_dir, gid + '.json'), 'w'), indent=1)

# ---------- markdown ----------
L = []
L.append(f"# {meta['name']}\n")
L.append(f"- id: `{gid}`  ·  url: {meta['url']}")
L.append(f"- steps: {meta['ordered_steps']} authored, **{meta['viewer_steps']} shown in the viewer** (hidden authoring steps are folded into the next shown step). behaviours: {meta['behaviours']} (pause = waits for the student, play = auto-advances)")
L.append(f"- units: offsets/lengths below are in mm (1 scene unit = {meta['mm_per_unit']} mm)")
L.append(f"- scene: {meta['scene']}")
L.append(f"- part render style overrides seen: {meta['part_style_overrides']}; edge style: {meta['part_edge_overrides']}; camera fov {meta['camera_fov']} ({meta['camera_type']})")
L.append(f"- project flags: {meta['project_flags']}")
L.append(f"- animation: {meta['animation']}")
L.append(f"- annotations inventory: {meta['toolbox']}")
L.append(f"- label styles (container, border, leader, em, bold, anchor): {meta['label_styles']}")
L.append(f"- line/arrow styles: {meta['line_styles']}")
L.append(f"- label texts used: {meta['label_texts']}")
L.append(f"- images used: {meta['images']}")
L.append(f"- step-level colour overrides (part base name, colour): {meta['colour_overrides'][:40]}")
L.append('\n## Parts inventory (top-level components; colours are effective at end of guide)\n')
agg = collections.defaultdict(lambda: dict(n=0, solids=0, cols=collections.Counter()))
for r in inventory:
    a = agg[base_name(r['name'])]; a['n'] += 1; a['solids'] += r['solids']
    for hx, nm, n in r['colours']: a['cols'][f'{nm} {hx}'] += n
for n, a in sorted(agg.items()):
    L.append(f"- {n} ×{a['n']} ({a['solids']} solids): " + ', '.join(f'{c} ({k})' for c, k in a['cols'].most_common(5)))
L.append('\n## Steps as the student sees them\n')
for i, r in enumerate(records):
    L.append(f"### [{i:03d}] {r['name']}  —  {r['behaviour']}, {r['duration']}ms  ·  thumb: thumbs/{gid}/{i:03d}.jpg")
    if r['description']: L.append(f"- description: {r['description']}")
    if r['popup']: L.append(f"- popup: {r['popup']}")
    c = r['camera']
    L.append(f"- camera: " + (f"MOVES — view rotates {c['change']['angle_deg']}°, target shifts {c['change']['target_shift_mm']}mm, distance {c['change']['dist_from']}→{c['change']['dist_to']}mm (zoom ×{c['change']['zoom']})" if c['change'] else 'unchanged') + f"  [now dist {c['dist_mm']}mm, elevation {c['elev']}°, azimuth {c['azim']}°]")
    if r['appeared']:
        L.append(f"- APPEAR ({len(r['appeared'])} parts): {fmt_groups(r['appeared'])}")
        offs = [o for o in r['appeared_offsets'] if o['dist_mm'] > 0.05]
        if offs:
            oc = collections.Counter((tuple(o['offset_mm']), o['dir']) for o in offs)
            L.append('  - appear displaced from seated pose by: ' + '; '.join(f"{list(k[0])}mm ({k[1]}) ×{n}" for k, n in oc.most_common(6)))
        else: L.append('  - appear already in seated (assembled) pose')
    if r['disappeared']: L.append(f"- DISAPPEAR ({len(r['disappeared'])} parts): {fmt_groups(r['disappeared'])}")
    if r['moved']:
        mv = collections.defaultdict(list)
        for m in r['moved']: mv[(tuple(m['delta_mm']), m['dir'], m['seated'])].append(m)
        for (d, dr, seated), ms in sorted(mv.items(), key=lambda kv: -len(kv[1]))[:10]:
            names = collections.Counter(base_name(m['part']) if len(ms) > 6 else m['part'] for m in ms)
            L.append(f"- MOVE {list(d)}mm ({norm(d):.0f}mm, {dr}) → {'SEATED' if seated else 'still displaced ' + str(ms[0]['now_offset_mm'])}: " + '; '.join(f'{n}' + (f' ×{c}' if c > 1 else '') for n, c in names.most_common(10)))
    if r['rotated']: L.append(f"- ROTATE: {r['rotated']}")
    for d in r['tb_on']: L.append(f"- + {fmt_tb(d)}")
    if r['tb_off']:
        oc = collections.Counter(d['kind'] for d in r['tb_off']); L.append('- − annotations removed: ' + ', '.join(f'{k} ×{n}' for k, n in oc.items()))
    if r['tb_changed']:
        oc = collections.Counter(d['kind'] for d in r['tb_changed']); L.append('- ~ annotations repositioned/edited: ' + ', '.join(f'{k} ×{n}' for k, n in oc.items()))
    L.append(f"- on screen now: {r['visible_parts']} parts ({r['visible_solids']} solids); annotations {r['tb_visible_counts'] or '{}'}; parts still displaced: {dict(collections.Counter(base_name(n) for n in r['displaced_parts'])) or 'none'}")
    if r['scene_change']: L.append(f"- scene change: {r['scene_change']}")
    L.append('')
open(os.path.join(out_dir, gid + '.md'), 'w').write('\n'.join(L))
print(gid, 'viewer steps', len(records), 'md chars', sum(len(x) for x in L))
