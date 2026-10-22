"""TechBox's published LAC take-apart (Cadasio 19075-lac_deconstruction), every viewer frame, in OUR assembly frame (mm, Y up):
cameras as view_dir + frame(target, radius), arrows (tail, tip, dims), eyes, labels, close-ups, lead lines, and every part's pose
relative to its seat. Read-only study for the LAC deconstruction (21 Oct 2026).

    .venv.nosync/bin/python docs/research/lac/decon/scripts/published_geometry.py      (about 3 s, under 150 MB; JSON only, no CAD)

Reads docs/research/lac/decon/published/raw/19075-lac_deconstruction.json (getProjectViewer payload) and
LAC Build Instructions/wire-paths.json (to name the wire bodies and caps by our CAD ids). Writes
docs/research/lac/decon/published_geometry.json. The reading rules are in lacpub.py.

Poses. For a copy X of a part whose seated copy is S (F1-2 of F1-1, the LCD's V1-2 of V1-1 ...): world move D = M_X(now) x
inverse(M_S(home)), written (a) as stepgen's pose about the seated part's box centre (`pose`: [dx, dy, dz] or {t, r: axis + deg,
at}) and (b) as a screw (`screw`: unit axis, degrees, a point on the axis, slide along it), which names a hinge where there is one.
For parts riding on another (knob, nut, washer on the potentiometer; switch on F4; the LCD's wires ...) `rel_to` gives the pose
relative to the carrier's own move (= a ride pose on the carrier, as guide.py writes them).
Camera: view_dir = unit(eye - target), radius = distance x sin(22.5 deg) / 1.08 (player/js/core.js cameraPose, frame_padding 1.08):
`view_dir=..., frame=(target, radius)` puts our eye where Cadasio's was in a landscape window (vertical fov 45 in both).
Arrows: mm = scene / SF; shaft w = body_width x scale / SF, head = head_width x scale / SF by head_length x scale / SF (the LSM's
measure_arrows.py, calibrated on the PMG); our player draws the head 4 w wide and min(0.6 L, 3.4 w) long, so dims=(L, w).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lacpub import *  # noqa: E402,F401,F403

OUT = Path(__file__).resolve().parents[1] / 'published_geometry.json'
EYE_SRC = 'ASS3e405c2c-ac76-88fc-a2d0-31bb66a7ae52.png'
FOV = float(((j.get('cameraProperties') or {}).get('default_camera') or {}).get('fov') or 45.0)

# ------------------------------------------------------------------ names: Cadasio top-level part -> our id
# Rigid parts (docs/research/lac/round1/published_motions.md section 0; docs/research/lac/cad_study.md). "copy" = another posed copy
# of the same part (a pose the published guide cross-fades to); its pose is measured against the seated copy (SEAT).
OURS = {
    'F1-1': 'NAUO10', 'F1-2': 'NAUO10 copy (pulled forward; CAD NAUO35)', 'F1-3': 'NAUO10 copy (face down beside the +z end; CAD NAUO125)',
    'F1-4': 'NAUO10 copy (face up beyond the -z end; CAD NAUO154)',
    'F2-1': 'F2', 'F2-2': 'F2 (the copy this guide moves)', 'F3-1': 'NAUO2', 'F4-1': 'F4', 'F4-2': 'F4 copy (flat beside the base; CAD NAUO50)',
    'F4-3': 'F4 copy (over the frame)', 'F5-1': 'F5', 'F6-1': 'F6', 'F7-1': 'NAUO42', 'F7-2': 'NAUO43', 'F8-1': 'NAUO44', 'F9-1': 'NAUO45',
    'Breadboard-1': 'NAUO1', 'Paper-1': 'NAUO141', 'nano-1': 'NANO', 'HW-84 v7-1': 'NAUO3', 'CR2025-50003LC-1': 'NAUO4 / NAUO5 (coin cell)',
    'CR2025-50003LC-2': 'NAUO4 / NAUO5 (coin cell)', 'LAC Resistor 1.SLDPRT-1': 'NAUO6', 'LAC Resistor 1.SLDPRT-2': 'NAUO7',
    'LAC Potentiometer-1': 'NAUO11', 'LAC Nut-2': 'NAUO12', 'LAC Knob-1': 'NAUO13', 'Washer-2': 'NAUO146',
    'LAC Potentiometer-2': 'NAUO11 copy (with F1-2)', 'LAC Knob-2': 'NAUO13 copy (with F1-2)', 'LAC Nut-3': 'NAUO12 copy (with F1-2)',
    'Washer-1': 'NAUO146 copy (with F1-2)',
    'LAC Potentiometer-3': 'NAUO11 copy (with F1-3)', 'LAC Knob-3': 'NAUO13 copy (with F1-3)', 'LAC Nut-4': 'NAUO12 copy (loose)',
    'Washer-3': 'NAUO146 copy (loose)',
    'LAC Potentiometer-4': 'NAUO11 copy (with F1-4)', 'LAC Knob-4': 'NAUO13 copy (with F1-4)',
    'LAC Potentiometer Assembled-1': 'potentiometer as supplied (never shown)',
    'Rocker Switch-1': 'NAUO46', 'Rocker Switch-2': 'NAUO46 copy (in F4-2; CAD NAUO51)', 'Rocker Switch-3': 'NAUO46 copy (in F4-3; CAD NAUO144)',
    'Piezo Buzzer-2': 'NAUO62', 'Piezo Buzzer-1': 'NAUO62 copy (lying; CAD NAUO61)',
    'LCD V1-1': 'NAUO94', 'LCD V1-2': 'NAUO94 copy (lying face down; CAD NAUO95)', 'LCD V1-3': 'NAUO94 copy (angled, F8 end in F8; no CAD copy)',
    'LCD V1-5': 'NAUO94 copy (standing 14.9 mm short of F9; CAD NAUO96)',
    'USB Right Angle-1': 'NAUO122', 'USB Cable end-1': 'USB_A', 'USB Cable 2-1': 'USB cable as supplied (never shown)',
}
SEAT = {'F1': 'F1-1', 'F2': 'F2-1', 'F4': 'F4-1', 'LAC Potentiometer': 'LAC Potentiometer-1', 'LAC Knob': 'LAC Knob-1', 'LAC Nut': 'LAC Nut-2',
        'Washer': 'Washer-2', 'Rocker Switch': 'Rocker Switch-1', 'Piezo Buzzer': 'Piezo Buzzer-2', 'LCD V1': 'LCD V1-1'}
CARRIER = {'LAC Knob': 'LAC Potentiometer', 'LAC Nut': 'LAC Potentiometer', 'Washer': 'LAC Potentiometer', 'LAC Potentiometer': 'F1',
           'Rocker Switch': 'F4'}


def kind(name):
    return re.sub(r'-\d+$', '', name)


def seat_of(t):
    n = NAME[t]
    s = SEAT.get(kind(n))
    if s and s in BY_NAME:
        return BY_NAME[s]
    return t


wp = json.load(open(WIRES))
LINE_OF_MESH = {v['mesh']: (k, v.get('colour')) for k, v in wp['lines'].items()}
CAP_CENTRES = {k: (np.array(v['box'][0]) + np.array(v['box'][1])) / 2 for k, v in wp['caps'].items()}
CAP_KIND = {k: v['kind'] for k, v in wp['caps'].items()}


def our_id(t):
    n = NAME[t]
    if n in OURS:
        return OURS[n]
    base = kind(n)
    if base in LINE_OF_MESH:
        k, c = LINE_OF_MESH[base]
        return f'wire body {k} ({c})'
    if base.startswith('Part') or base.startswith('Copy of Part'):
        return 'wire body (not in wire-paths.json)'
    if base.startswith('Wire Cap'):
        b = HOME.world_box(top_leaves[t], home=True)
        if b is not None:
            c = (b[0] + b[1]) / 2
            best = min(CAP_CENTRES, key=lambda k: float(np.linalg.norm(CAP_CENTRES[k] - c)))
            d = float(np.linalg.norm(CAP_CENTRES[best] - c))
            if d < 0.6:
                return f'cap {best} ({CAP_KIND[best]})'
            return f'cap (no CAD twin within 0.6 mm; nearest {best} at {d:.1f})'
    return None


OUR = {t: our_id(t) for t in TOPS}


def seat_box_centre(t):
    s = seat_of(t)
    b = HOME.world_box(top_leaves[s], home=True)
    return (b[0] + b[1]) / 2 if b else None


def describe_pose(S_, t, M):
    """The pose of top-level part t (placed at world matrix M now) relative to its seat; and to its carrier's move."""
    s = seat_of(t)
    D = M @ np.linalg.inv(home_top(s))
    c = seat_box_centre(t)
    u, deg, p, slide = screw(D)
    out = dict(pose=pose_about(D, c), seat=NAME[s])
    if u is not None and deg > 0.05:
        # (the point on the axis nearest the part's middle)
        q = p + ((c - p) @ u) * u
        out['screw'] = dict(axis=r2(u, 4), deg=round(deg, 3), through=r2(q), slide=round(slide, 2))
        out['pose_hinge'] = dict(t=r2(slide * u), r=r2(u, 5) + [round(deg, 3)], at=r2(q))
    t_now = D[:3, 3] + D[:3, :3] @ c - c
    out['centre_moved_mm'] = round(float(np.linalg.norm(t_now)), 2)
    return out


def carrier_move(S_, t):
    """The world move of t's carrier copy shown with it now (the potentiometer copy shown with a knob copy...), or None."""
    car = CARRIER.get(kind(NAME[t]))
    if not car:
        return None
    cands = [u for u in TOPS if kind(NAME[u]) == car and S_.visible_leaves(u)]
    if not cands:
        return None
    # the copy nearest t
    ct = S_.world_box(S_.visible_leaves(t))
    best, bd = None, 1e9
    for u in cands:
        b = S_.world_box(S_.visible_leaves(u))
        d = float(np.linalg.norm((b[0] + b[1]) / 2 - (ct[0] + ct[1]) / 2))
        if d < bd:
            best, bd = u, d
    Mu = S_.leaf_top(S_.visible_leaves(best)[0])
    return best, Mu @ np.linalg.inv(home_top(seat_of(best)))


# ------------------------------------------------------------------ annotations
def anchored(S_, oid, loc):
    if oid in refs:
        return (S_.world(oid) @ np.append(v3(loc) * MM, 1))[:3]
    return None


def arrow_info(S_, t):
    pts = [v3(p) * MM for p in t['points']]
    p0, p1 = pts[0], pts[-1]
    L = float(np.linalg.norm(p1 - p0))
    sc = float(t.get('scale') or 1.0)
    w = float(t.get('body_width')) * sc * MM
    hw, hl = float(t.get('head_width')) * sc * MM, float(t.get('head_length')) * sc * MM
    oid = t.get('object_ids') or []
    oid = list(oid.values()) if isinstance(oid, dict) else list(oid)
    olp = t.get('object_local_positions') or {}
    via_obj = []
    for i in range(min(len(oid), 2)):
        a = anchored(S_, oid[i], olp.get(str(i)) or {}) if olp.get(str(i)) is not None else None
        via_obj.append(a)
    d = (p1 - p0) / L if L > 1e-9 else np.zeros(3)
    out = dict(name=t.get('name'), tail=r2(p0), tip=r2(p1), length=round(L, 2), dir=r2(d, 4), shaft_w=round(w, 2),
               head=[round(hw, 2), round(hl, 2)], dims=[round(L, 1), round(w, 2)],
               placed_on=[(OUR.get(TOP[o]) or NAME[TOP[o]]) + ' / ' + NAME[TOP[o]] if o in refs else 'stale id' for o in oid])
    if all(a is not None for a in via_obj) and via_obj:
        dev = max(float(np.linalg.norm(a - b)) for a, b in zip(via_obj, (p0, p1)))
        out['points_vs_anchors_mm'] = round(dev, 2)
        if dev > 0.5:
            out['tail_by_anchor'], out['tip_by_anchor'] = r2(via_obj[0]), r2(via_obj[1])
    return out


def line_info(S_, t):
    a = arrow_info(S_, dict(t, body_width=0, head_width=0, head_length=0))
    return {k: a[k] for k in ('name', 'tail', 'tip', 'length', 'dir', 'placed_on', 'points_vs_anchors_mm', 'tail_by_anchor', 'tip_by_anchor') if k in a}


def link_ring(S_, t):
    links = [l for l in (t.get('links') or []) if isinstance(l, dict)]
    if not links:
        return None, None
    leaf = links[0].get('targetId')
    tgt = (links[0].get('data') or {}).get('target') or {}
    if leaf not in refs:
        return None, 'stale id ' + str(leaf)
    p = (S_.world(leaf) @ np.append(v3(tgt) * MM, 1))[:3]
    return r2(p), f'{OUR.get(TOP[leaf]) or "?"} / {NAME[TOP[leaf]]} / solid {short(leaf)}'


def kind_of_step(name, behaviour):
    if name == 'Start':
        return 'start'
    if name == 'Completed View':
        return 'end'
    if behaviour == 'play':
        return 'transition (auto)'
    if 'Trans' in name:
        return 'transition (pause)'
    if re.match(r'^Step \d+c$', name):
        return 'Nc'
    if re.match(r'^Step \d+$', name):
        return 'N'
    return behaviour


# ------------------------------------------------------------------ walk
S = State()
records = []
prev = {}
frame = -1
for idx, sid in enumerate(order):
    s = steps[sid]
    S.apply(s)
    if s.get('behaviour') == 'hidden':
        continue
    frame += 1
    cur = {}
    for t in TOPS:
        gs = S.groups(t)
        if not gs:
            continue
        gs.sort(key=len, reverse=True)
        cur[t] = (gs[0], S.leaf_top(gs[0][0]), len(gs))
    appear = [t for t in cur if t not in prev]
    gone = [t for t in prev if t not in cur]
    moved = []
    for t, (ks, M, ng) in cur.items():
        if t not in prev:
            continue
        Mp = prev[t][1]
        dR = Rotation.from_matrix(M[:3, :3] @ Mp[:3, :3].T).magnitude()
        if np.linalg.norm(M[:3, 3] - Mp[:3, 3]) > 0.05 or dR > 1e-3:
            box = S.world_box(ks)
            c_now = (box[0] + box[1]) / 2
            c_prev = (Mp @ np.linalg.inv(M) @ np.append(c_now, 1))[:3]
            e = dict(part=NAME[t], ours=OUR[t], step_move=r2(c_now - c_prev), step_move_len=round(float(np.linalg.norm(c_now - c_prev)), 2),
                     step_turn_deg=round(math.degrees(dR), 2), **describe_pose(S, t, M))
            if dR > 1e-3:
                u, deg, p, slide = screw(M @ np.linalg.inv(Mp))
                q = p + ((c_prev - p) @ u) * u
                e['step_screw'] = dict(axis=r2(u, 4), deg=round(deg, 3), through=r2(q), slide=round(slide, 2))
            cm = carrier_move(S, t)
            if cm:
                car, Dc = cm
                Dx = M @ np.linalg.inv(home_top(seat_of(t)))
                e['rel_to'] = dict(carrier=NAME[car], pose=pose_about(np.linalg.inv(Dc) @ Dx, seat_box_centre(t)))
            moved.append(e)

    def placed(t):
        ks, M, ng = cur[t]
        d = dict(part=NAME[t], ours=OUR[t], solids=f'{len(ks)}/{len(top_leaves[t])}')
        b = S.world_box(ks)
        if b:
            d['box'] = [r2(b[0], 1), r2(b[1], 1)]
        if NAME[t] == 'LAC Wire Cables-1':                    # (the six-way ribbon's solids, used one wire at a time as a loose jumper)
            d['leaves'] = []
            for k in S.visible_leaves(t):
                Dk = S.world(k) @ np.linalg.inv(HOME.world(k, home=True))
                bk = S.world_box([k])
                hb = HOME.world_box([k], home=True)
                d['leaves'].append(dict(solid=short(k), our_line=LINE_OF_MESH.get(kind(short(k)), (None,))[0],
                                        box=[r2(bk[0], 1), r2(bk[1], 1)], from_cad=pose_about(Dk, (hb[0] + hb[1]) / 2)))
            return d
        if OUR[t] and (OUR[t].startswith('wire body') or OUR[t].startswith('cap')):
            D = M @ np.linalg.inv(home_top(t))
            hb = HOME.world_box(top_leaves[t], home=True)
            if np.abs(D - np.eye(4)).max() > 1e-4:
                d['from_cad'] = pose_about(D, (hb[0] + hb[1]) / 2)
            return d
        if seat_of(t) != t or kind(NAME[t]) in SEAT or NAME[t] in OURS:
            d.update(describe_pose(S, t, M))
            cm = carrier_move(S, t)
            if cm and cm[0] != t:
                car, Dc = cm
                d['rel_to'] = dict(carrier=NAME[car], pose=pose_about(np.linalg.inv(Dc) @ (M @ np.linalg.inv(home_top(seat_of(t)))), seat_box_centre(t)))
        return d

    eyes, insets, titles, arrows, labels, lines = [], [], [], [], [], []
    for k, t in S.tb.items():
        if not t.get('visible'):
            continue
        ty = t.get('type')
        if ty == 'image':
            src = ((t.get('content') or {}).get('src') or '').split('/')[-1].split('?')[0]
            ring, on = link_ring(S, t)
            e = dict(name=t.get('name'), ring=ring, on=on, screen_pct=r2(v3(t.get('position') or {})[:2], 1),
                     ring_screen_pct=r2(v3(t.get('target_position') or {})[:2], 1), width_pct=t.get('width'))
            if src == EYE_SRC:
                eyes.append(e)
            elif ring is None:
                titles.append(dict(name=t.get('name'), src=src, screen_pct=e['screen_pct'], width_pct=t.get('width')))
            else:
                e.update(src=src, height_over_width=t.get('height'))
                insets.append(e)
        elif ty == 'arrow':
            arrows.append(arrow_info(S, t))
        elif ty == 'line':
            lines.append(line_info(S, t))
        elif ty == 'editor':
            ring, on = link_ring(S, t)
            labels.append(dict(name=t.get('name'), text=re.sub(r'<[^>]+>', '', t.get('editor_contents') or '').strip(), ring=ring, on=on,
                               screen_pct=r2(v3(t.get('position') or {})[:2], 1), ring_screen_pct=r2(v3(t.get('target_position') or {})[:2], 1)))
    cam = cam_view(S.cam, FOV)
    cam['up_axis'] = S.scene.get('up_axis')
    # Isolated sub-assemblies shown in a posed copy (F1-4 face up beyond the -z end, F4-2 flat beside): the same camera in the
    # seated frame of that copy's part, i.e. for our parts seated (or carried by a pure translation of it, alone=).
    for host in ('F1-4', 'LAC Potentiometer-4', 'F4-2'):
        h = BY_NAME[host]
        if 'in_seated_frame_of' not in cam and h in cur and not any(NAME[t] == 'F3-1' for t in cur):
            Dh = cur[h][1] @ np.linalg.inv(home_top(seat_of(h)))
            inv = np.linalg.inv(Dh)
            eye_s = (inv @ np.append(cam['eye'], 1))[:3]
            tgt_s = (inv @ np.append(cam['target'], 1))[:3]
            u = (eye_s - tgt_s) / np.linalg.norm(eye_s - tgt_s)
            up_s = inv[:3, :3] @ np.array(cam['camera_up'])
            yproj = np.array([0, 1.0, 0]) - (-u) * (-u)[1]
            yproj /= np.linalg.norm(yproj)
            roll = math.degrees(math.atan2(np.dot(np.cross(yproj, up_s), -u), np.dot(yproj, up_s)))
            cam['in_seated_frame_of'] = dict(copy=host, seated=NAME[seat_of(h)], view_dir=r2(u, 4), target=r2(tgt_s), eye=r2(eye_s),
                                             radius=cam['radius'], camera_up=r2(up_s, 4), roll_deg_from_world_up=round(roll, 2),
                                             elevation=round(math.degrees(math.asin(max(-1, min(1, u[1])))), 1),
                                             azimuth=round(math.degrees(math.atan2(u[0], u[2])), 1))
            for a in arrows + lines:                  # (the arrows and lead lines in that seated frame too)
                a['seated_frame'] = dict(of=NAME[seat_of(h)], tail=r2((inv @ np.append(a['tail'], 1))[:3]), tip=r2((inv @ np.append(a['tip'], 1))[:3]),
                                         dir=r2(inv[:3, :3] @ np.array(a['dir']), 4))
            for e in eyes + labels + insets:
                if e.get('ring'):
                    e['ring_seated_frame'] = r2((inv @ np.append(e['ring'], 1))[:3])
    rec = dict(frame=frame, order_index=idx, name=s['name'], kind=kind_of_step(s['name'], s.get('behaviour')), behaviour=s.get('behaviour'),
               duration_ms=s.get('animationDuration'), camera=cam,
               arrows=arrows, eyes=eyes, insets=insets, labels=labels, lead_lines=lines,
               appear=[placed(t) for t in appear], disappear=[dict(part=NAME[t], ours=OUR[t]) for t in gone], moved=moved,
               shown=sorted(NAME[t] for t in cur))
    if titles:
        rec['title_images'] = titles
    split = [NAME[t] for t, v in cur.items() if v[2] > 1]
    if split:
        rec['parts_with_solids_apart'] = split
    records.append(rec)
    prev = cur

prevc = None
for r in records:
    c = r['camera']
    r['camera_moves'] = prevc is None or max(abs(a - b) for a, b in zip(c['eye'] + c['target'], prevc['eye'] + prevc['target'])) > 0.05 \
        or c.get('up_axis') != prevc.get('up_axis')
    prevc = c

meta = dict(source=str(SRC.relative_to(ROOT)), scale_factor=SF, mm_per_scene_unit=round(MM, 5), fov=FOV, frames=len(records),
            stale_ids_in_steps=len(S.stale), nonleaf_visible_sets=dict(S.nonleaf_visible),
            mapping={NAME[t]: OUR[t] for t in TOPS if OUR[t]},
            note='mm in our assembly frame (Y up). Frames as the viewer shows them (hidden steps skipped, Start = 0), as in '
                 'docs/research/guide_19075-lac_deconstruction.md. See published_geometry.md.')
# ------------------------------------------------------------------ by published step (1 - 47)
# The instruct frame of each numbered step (docs/research/guide_19075-lac_deconstruction.md section 3; [104] is Step 40's instruct frame
# though named 'Step 41', [105] a duplicate of it, [120] Step 45's though named 'Step 45c').
INSTRUCT = [1, 4, 8, 11, 13, 15, 19, 22, 25, 27, 29, 31, 35, 38, 41, 43, 45, 47, 49, 52, 55, 58, 61, 63, 67, 70, 72, 74, 78, 80, 82, 84,
            86, 88, 90, 92, 95, 98, 101, 104, 108, 111, 114, 117, 120, 123, 126]
assert len(INSTRUCT) == 47
by_step = []
cam_now = None
for n, f0 in enumerate(INSTRUCT, start=1):
    f1 = INSTRUCT[n] if n < len(INSTRUCT) else len(records) - 1           # (the Completed View, frame 129, is not part of Step 47)
    r0 = records[f0]
    c = r0['camera']
    cam = dict(view_dir=c['view_dir'], frame=[c['target'], c['radius']], distance=c['distance'], elevation=c['elevation'], azimuth=c['azimuth'],
               up_axis=c['up_axis'], new=r0['camera_moves'] or any(records[k]['camera_moves'] for k in range(f0, f1)))
    if c.get('in_seated_frame_of'):
        s_ = c['in_seated_frame_of']
        cam['seated_frame'] = dict(of=s_['seated'], view_dir=s_['view_dir'], frame=[s_['target'], s_['radius']])
    motion = []
    for k in range(f0 + 1, f1):
        r = records[k]
        rigid = lambda m: m.get('ours') and not m['ours'].startswith(('wire', 'cap'))
        mv = [dict(part=m['part'], ours=m['ours'], step_move=m['step_move'], turn_deg=m['step_turn_deg'], pose=m['pose'],
                   **({'pose_hinge': m['pose_hinge']} if 'pose_hinge' in m else {}), **({'rel_to': m['rel_to']} if 'rel_to' in m else {}))
              for m in r['moved'] if rigid(m)]
        ap = [dict(part=m['part'], ours=m['ours'], pose=m.get('pose'), **({'pose_hinge': m['pose_hinge']} if 'pose_hinge' in m else {}),
                   **({'rel_to': m['rel_to']} if 'rel_to' in m else {})) for m in r['appear'] if rigid(m)]
        wires_in = [dict(part=m['part'], ours=m['ours'], box=m.get('box'), **({'from_cad': m['from_cad']} if 'from_cad' in m else {}),
                         **({'leaves': m['leaves']} if 'leaves' in m else {}))
                    for m in r['appear'] if not rigid(m)]
        wires_moved = [dict(part=m['part'], ours=m['ours'], step_move=m['step_move'], from_cad=m['pose']) for m in r['moved'] if not rigid(m)]
        motion.append(dict(frame=k, name=r['name'], kind=r['kind'], duration_ms=r['duration_ms'], moved=mv, cross_faded_in=ap,
                           faded_out=[m['part'] for m in r['disappear']], wires_shown=wires_in, wires_moved=wires_moved))
    by_step.append(dict(step=n, instruct_frame=f0, frames=list(range(f0, f1)), camera=cam, arrows=r0['arrows'], eyes=r0['eyes'],
                        labels=r0['labels'], insets=r0['insets'], lead_lines=r0['lead_lines'], motion=motion))
end = records[-1]['camera']
json.dump(dict(meta=meta, by_step=by_step, completed_view=dict(view_dir=end['view_dir'], frame=[end['target'], end['radius']], distance=end['distance']),
               start=dict(view_dir=records[0]['camera']['view_dir'], frame=[records[0]['camera']['target'], records[0]['camera']['radius']],
                          distance=records[0]['camera']['distance'], title_images=records[0].get('title_images')),
               frames=records), open(OUT, 'w'), indent=1)
print(len(records), 'frames ->', OUT)
