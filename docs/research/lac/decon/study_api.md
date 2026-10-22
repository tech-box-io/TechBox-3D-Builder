# LAC deconstruction: the take-apart API, and how the four existing deconstructions use it

Study for the LAC's deconstruction guide (Lee, 21 Oct 2026: "we need to make a deconstruction guide for this LAC as well. Here is the
published version ... https://instructions.online/?id=19075-lac_deconstruction"). Read-only: nothing was run but light JSON reads
(`docs/research/lac/decon/scripts/takeapart_state.py`, a mirror of `take_apart()` on the LAC's steps.json, and the LSM session's
`measure_arrows.py` on the published payload, output kept in the scratchpad and copied into section 3.1). No generator, no CAD, no
browser. Complete, 21 Oct 2026.

Sources: `tools/stepgen.py` (2435 lines as it stands: take_apart 828-912, remove 914-945, unplug 947-952, lift 954-967, _takeoff
969-1246, put_away 1258-1275, _arrow_dims 1429-1433, _arrow_out 1435-1513, build(): `begin` 1750-1758, takeoff views 1771-1902, title
and Completed View 2033-2104, turned-over runs 2108-2152, parts pages 2219-2220, _sync_model 2421-2435); the four deconstruction.py
scripts (MRA 281 lines, RCC 138, PMG 242, LSM 237); the earlier studies `docs/research/pmg/deconstruction/takeapart_api.md` and
`docs/research/lsm/decon/study_generator.md` (both now partly out of date: `let_go=`, `reappear=`, `arrow_style dims= / then=`, and
`inset` `marks= / ghost= / side=` on take-off steps have been added since; see 1.3); `player/js/player.js` (awayTiming), `runthrough.js`,
`tools/motioncheck.py`, `tools/publish.py`; `LAC Build Instructions/guide.py` and `steps.json` (118 views, 126 routes, 25 wires);
`docs/research/guide_19075-lac_deconstruction.md`; rulebook section 11.

---------------------------------------------------------------------------------------------------------------------------------

## 0. In one page

- A deconstruction is a script of its own, `LAC Build Instructions/deconstruction.py`: `Guide(..., part='Deconstruction',
  steps_file='steps-deconstruction.json', source='lac-guide.glb')`, then `g.take_apart(...)`, then `remove()` / `unplug()` / `lift()` /
  `note()` / `put_away()`, then `g.build()`. It reads the Full Build **only from steps.json** (`FULL`, `VIEW`, `ROUTES`), never by
  importing guide.py (the LAC's guide.py calls `g.build()` at module level, line 1375: importing it would load the CAD and rewrite
  steps.json and parts.json).
- Three LAC-specific must-dos: `source='lac-guide.glb'` (Guide's default is 'mra.glb'); `take_apart(leave_out=[PAPER])` (the
  breadboard's backing, NAUO141, put away in the Full Build's Step 1, would otherwise come back 50 mm under the breadboard: section 8);
  `hero_azimuth=135` (the Full Build's: used for the Completed View if the last step is turned over).
- What works by the Full Build's own record ("the Full Build's way, reversed", its camera too): F6, F5, F8, F2 (3 stages), F1 with the
  potentiometer (Step 54, both listed), F4 off the frame (Step 49), the LCD out of its notches (Step 52), the buzzer out from between the
  F7s (Step 43), the USB plug (40), every jumper pair (9 - 14, 20, 21), every lead cap (16 - 18, 30 - 32, 33, 34, LCD male caps 36 - 39),
  the RTC with its coin cell (7), both resistors (5, 6) and the Nano (3).
- What has **no record** (it came in by `ride=` / `appear=` only) and so needs a way by hand (else a straight pull up, a WARNING and a
  yellow Review note): F9, both F7s, the rocker switch, the knob, nut and washer, the four LCD female caps, the USB A end, and every
  move the Full Build made by riding (F1 laid face down / aside / stood up, F4 laid flat / lifted, the LCD stood up, the potentiometer
  through F1). All their poses are in steps.json (`carry` entries), section 4.
- `lift()` and `remove()` never re-route a lead; `unplug()` does (to the route its Full Build step opened with). Every tethered move
  needs `wires=` (and `wire_via=` for several stages), taken from the Full Build's own views: a strict reverse of the Full Build stays on
  routes it already has; any other order needs routes drawn anew (section 4.4).
- Cannot be done with the API: putting anything back on (the published Steps 16 - 18 refit the washer, nut and knob for storage:
  `place()` is refused in a take-apart, and Lee's rule is that a part once off is gone); arrows in turn (`then=`) together with a lead
  that changes route stage by stage (`wire_via=`) in one step (F2 with the USB cable, the buzzer, the LCD; a 5-line generator change
  would allow it, 3.4); a close-up that is a picture (`inset=dict(image=)`) on a take-off step; a view with the scene's up axis turned
  sideways (the published F1 and F4 isolations: our player only turns the model upside down, `flip=True`).

---------------------------------------------------------------------------------------------------------------------------------

## 1. The API, exactly

### 1.1 Signatures

    Guide(kit_dir, title, part, names, source='mra.glb', copyright_line='', ..., hero_azimuth=225.0, start_view=None, end_view=None,
          parts_list=None, review_notes=True, hover_names=None, steps_file='steps.json', **overrides)
    g.take_apart(full='steps.json', parts_list_at_end=False, leave_out=())
    g.remove(caption, ids, **how)                         # parts leave and are gone (Step Nc: they slide out, then fade)
    g.unplug(caption, ids, ride_on=None, **how)           # plugs come out the way the Full Build put them in; an eye on each, no arrow
    g.lift(caption, ids, to=None, ride_on=None, **how)    # parts move and stay on screen, still wired
    g.put_away(ids)                                       # off the screen, no step of its own; the next view cuts in
    g.note(caption, review=None, caution=None)            # a text card (only_in= is for a Part of a Full Build: refused here)
    g.build()

    **how (_takeoff, 969-972): path=None, paths=None, direction=None, hover=None, wires=None, arrows=None, eye=None, labels=(),
        caution=None, review=None, view_dir=None, frame=None, look_from=None, new_camera=False, inset=None, alone=None, flip=False,
        wire_via=None, units=None, wires_here=None, in_turn=None, keep_camera=False, arrow_scale=1.0, arrow_style=None,
        own_frame=False, reappear=False, let_go=()

`place()`, `rest()` and `seat()` raise `ValueError: ... a deconstruction guide takes parts off (remove(), unplug(), lift()); it puts
nothing on` (1366, 1604, 1621). `chapter()` / `in_part()` / `note(only_in=)` are for a Full Build's Parts only.

### 1.2 What each argument does (as the code reads, not only as documented)

| argument | what it does | where |
|---|---|---|
| `ids` | the parts that move; each must be on screen. A listed part riding on another listed part goes with it (not a mover). | 976-979, 992 |
| `path=[pose, ...]` | the way by hand for every mover without its own `paths=` entry: **absolute poses (relative to the part's seat), the ones after where it is now** (the current pose is put first). Each pose is a stop (one 800 ms beat); a `via(pose)` is passed through. | 1016-1019, 1085-1087 |
| `paths={id: [pose, ...]}` | the same, per part | 1016 |
| `direction=[x,y,z]`, `hover=mm` | a straight pull for movers with no hand way (`hover` default: `hover_distance`) | 1022-1025 |
| `to=pose` or `{id: pose}` (lift) | a one-stage way | 1020-1021 |
| (none of these) | the Full Build's record: the latest record of the part whose whole group is leaving now, reversed, its stops kept, its camera used. Used if the part is in its seat and not riding, or rides at its seat on a part that stays. Otherwise: unplug -> ValueError; remove / lift -> pulled straight out the first free axis (collision test), or, for a part not in its seat or riding, **straight up, unchecked: WARNING + Review note**. | 1026-1069 |
| `ride_on=` | unplug: an id or `{plug: id}`, what each plug rides on afterwards (default: what it rode on in the Full Build before that step, `rode`). lift: **one id only** (a dict is ignored); default: the movers after the first ride on the first. | 1131-1138, 1201-1205 |
| `wires={w: route or None}` | lead routes as the step ends (Step Nc). `None`: the lead goes at once (not faded). A lead listed here is exempt from the "left with one end" refusal. | 1139, 1154-1165 |
| `wire_via={w: [route, ...]}` | routes a lead passes through, one per stage boundary; its last route must be in `wires=` (ValueError). The lead keeps pace stop by stop only if `len(wire_via[w]) + 1` equals the step's beats (player `paced()`); nothing warns of a mismatch. Prev plays it backwards. | 1139-1142, 1887 |
| `wires_here={w: route}` | how leads are drawn on this step's two views only (not kept) | 1860, 1883 |
| `arrows=` | `None`: one per unit (computed); `[]`: none; or `[dict(tail, head, normal, part, width)]` by hand, in seated mm on `part`, drawn where that part is now. Any non-None value skips the computed units (and so `arrow_style`). | 1166-1188, 1845-1848 |
| `units=[[ids], ...]` | the arrows by hand: one per group (ids must be movers). Also gives an unplug an arrow. | 1167-1171 |
| `eye=` | ids or `dict(id=, anchor=, side=, reach=)`; anchor found where the camera sees the part if not given. Default: every mover for unplug, none otherwise. An arrow that would point at the camera becomes an eye on its part. | 1189-1191, 1825-1826, 1842-1844 |
| `labels=` | ids (text = the part's hover name) or dicts (`id, text, anchor, side, reach`), on Step N only; an anchor is placed where missing | 1192, 1842-1844, 1859 |
| `caution=`, `review=` | as a build's (Step N and Nc) | 1856-1858 |
| `inset=dict(...)` | a close-up on **Step N** (the catch to release): `target` (required), `dir` (default the camera's), `radius` (20), `hide`, `mark`, `marks=[(at, half), ...]`, `ghost={id: alpha}`, `side`, `alt`, `caption`, `arrows=[ids]` (those units' arrows drawn in it). **No `image=`** on a take-off step. | 1849-1855 |
| `view_dir=`, `frame=(target, radius)`, `look_from=`, `new_camera=True` | any of them: a camera chosen for this step (choose_view) instead of the Full Build's | 1193-1200, 1786-1788 |
| `keep_camera=True` | the step before's camera exactly (a run on one sub-assembly) | 1786 |
| `flip=True` | shown turned over; a Full Build camera that is turned over is turned over whatever `flip` says | 1199-1200 |
| `own_frame=True` | in a run of turned-over steps, this one keeps its own framing | 2126-2152 |
| `alone=[ids]` | only these (and what rides on them, added) are on screen; must include the movers; both views `isolated` (the player cuts back to the whole model at the next step without `alone`) | 999-1002, 1777, 1857 |
| `in_turn=[[ids], ...]` | groups leave one after another; must list each mover once; refused with a lead changing route or `wire_via` | 1088-1102, 1150-1152 |
| `arrow_scale=k` | every arrow of the step times k | 1821 |
| `arrow_style={id: dict(...)}` | the arrow of the unit holding `id`: `scale`, `dims=(length, shaft width)` mm, `like=id2`, `at=[x,y,z]` (its tail), `shift=`, `face=`, `keep=True`, `stage=k` (along stage k, 0 the first), `then=[dict(stage=k, dims=, at=, shift=, face=, keep=), ...]` (arrows in turn) | 1104-1128, 1819-1840 |
| `reappear=True` (lift, unplug) | nothing moves: what changes place, its riders and leads fade out and in, a beat each; refused on remove() and with `in_turn` | 980-981, 1858 |
| `let_go=[ids]` | riders of what leaves that stay where they are, resting from then on | 993-997, 1226-1229, 1772-1776 |

Two views per step (1859-1889): `Step N` (kind `hover`: parts where they are, arrows, eyes, labels, inset, `moving: []`) and `Step Nc`
(kind `done`: `moving` = the movers, `paths` = their ways, `path_stops`, `leaving` = parts that go, `leaving_wires` = their leads,
`wire_via`, `staged_arrows`, `away: true`). The player plays the slide on Next, then fades what leaves over 800 ms starting 200 ms before
it rests (awayTiming, player.js 690-711); Prev plays it all backwards. There are no "Transition" frames: the published guide's
auto-advancing transitions are our Step Nc's motion.

### 1.3 Changed since the PMG's and LSM's API studies (read those with this in mind)

- `let_go=` exists (the PMG study proposed it; the PMG and LSM use it).
- `reappear=True` exists on lift() and unplug() (the PMG's Step 8).
- `arrow_style` takes `dims=` and `then=` (with a rest beat before each later stage, added by the generator: 1118-1128).
- A take-off `inset=` now passes `marks=`, `ghost=` and `side=` (the LSM study said they were dropped); `image=` is still not passed.
- The LSM study's "a lift() `ride_on=` dict silently falls back" still holds.

### 1.4 How the four scripts are laid out (the pattern to copy)

    import json, sys
    from pathlib import Path
    import numpy as np
    HERE = Path(__file__).resolve().parent
    sys.path.insert(0, str(HERE.parent / 'tools'))
    from stepgen import Guide, _shifted, apply_pose, compose, relative_pose, via  # noqa: E402

    # ids copied from guide.py (never import it)
    FULL = json.loads((HERE / 'steps.json').read_text(encoding='utf-8'))
    VIEW = {v['name']: v for v in FULL['views']}
    ROUTES = FULL['routes']
    # helpers: camera_of, leads, walked_back / carried_back / lifted_back / full_way_back, where()
    g = Guide(HERE, title=..., part='Deconstruction', names=dict(FULL['names']), steps_file='steps-deconstruction.json', source=...,
              copyright_line='© TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')
    g.take_apart(parts_list_at_end=True)
    ... steps, grouped under '# ====' headings in the order they play, each with a comment saying why ...
    g.build()

Features each one uses:

| | MRA | RCC | PMG | LSM |
|---|---|---|---|---|
| take_apart | parts_list_at_end | (none) | parts_list_at_end | parts_list_at_end, leave_out=[BACKING] |
| Full Build's way by default | most panels, screws, motors | most | case plates, keys | stems, D8, D7, D6, D9s, D5, D3, R330 ... |
| hand ways | USB A end, join, claw plug walks | USB A end, adapter, plugs, motors | USB, devices off their caps, wires up 25 | D11 posts, D10, D4, nut, button, matrix |
| lift + wire_via / wires | claw / elbow / shoulder plugs (`walked_back`), join (`riding_back`) | L4 / L5 block (`wires=` Step 21) | displays (`lifted_back`, `carried_back`), module, buttons | matrix (Step 32 reversed, `carried_back` 30 and 26), D2 |
| unplug | servo rows (labels instead of eyes), base plug | barrel plug, motors (`ride_on=L1`) | - | button pins (caution) |
| alone= + put_away | T block, claw, links, forearm, lever, upper arm, module, joysticks | controller, battery, module, L4/L5 | electronics | button on D2 |
| arrows | in-house sizes, `scale`, `like`, `at`, `face`, `keep`, inset arrows | `scale`, `at`, `stage=0` | published `dims`, `then=`, `at` (`in_front`) | published `dims`, `then=`, hand `arrows=` |
| let_go / reappear | - | - | both | let_go |
| Step 1 caution | - | - | - | "Disconnect the USB Cable from the computer ..." |

### 1.5 The LAC's ids, for the fragments below (copied from guide.py 37-73; never import it)

    BREADBOARD, F3, RTC, COIN, RES1, RES2 = 'NAUO1', 'NAUO2', 'NAUO3', 'NAUO4', 'NAUO6', 'NAUO7'
    F1, POT, NUT, KNOB, WASHER = 'NAUO10', 'NAUO11', 'NAUO12', 'NAUO13', 'NAUO146'
    F7A, F7B, F8, F9 = 'NAUO42', 'NAUO43', 'NAUO44', 'NAUO45'           # F7A at the back (-x), F7B in front
    F4, F5, F2, F6 = 'F4', 'F5', 'F2', 'F6'                             # (materials.json extra_parts)
    SWITCH, BUZZER, LCD, USB_B, PAPER = 'NAUO46', 'NAUO62', 'NAUO94', 'NAUO122', 'NAUO141'
    NANO, USB_A = 'NANO', 'USB_A'
    ZERO = [0.0, 0.0, 0.0]
    JUMPERS = {'black': ('NAUO16', 'NAUO17'), 'green': ('NAUO20', 'NAUO19'), 'purple': ('NAUO25', 'NAUO26'),   # (the end the published
               'blue': ('NAUO22', 'NAUO21'), 'white': ('NAUO28', 'NAUO15'), 'dark_red': ('NAUO30', 'NAUO31'),  #  build labels first, first)
               'orange': ('NAUO53', 'NAUO52'), 'yellow': ('NAUO56', 'NAUO55')}
    SWITCH_CAPS = {'red': 'NAUO47', 'tan': 'NAUO49', 'black': 'NAUO48'}             # (leads 'switch <colour>': a = SWITCH, b = the cap)
    POT_CAPS = {'red': 'NAUO34', 'tan': 'NAUO33', 'black': 'NAUO14'}                # ('pot <colour>': a = the cap, b = POT)
    BUZZER_CAPS = {'red': 'NAUO58', 'black': 'NAUO59'}                              # ('buzzer <colour>': a = the cap, b = BUZZER)
    LCD_WIRES = {'purple': ('NAUO82', 'NAUO97', 'GND'), 'yellow': ('NAUO84', 'NAUO98', 'VCC'),   # ('lcd <colour>': a = male cap in the
                 'teal': ('NAUO86', 'NAUO99', 'SDA'), 'blue': ('NAUO93', 'NAUO100', 'SCL')}       #  breadboard, b = female cap on the LCD)
    LCD_MALE, LCD_FEMALE = [m for m, _, _ in LCD_WIRES.values()], [f for _, f, _ in LCD_WIRES.values()]
    POWER = 'Disconnect the USB cable from the computer or power supply before you begin.'

---------------------------------------------------------------------------------------------------------------------------------

## 2. What `take_apart()` starts from, for the LAC

Mirrored from steps.json by `docs/research/lac/decon/scripts/takeapart_state.py` (run it again after any guide.py change):

- 58 parts, 25 leads; with `leave_out=[PAPER]`, 57 parts. `resting` (off its seat, not riding): only USB_A, on the table behind the
  case (`A_ON_TABLE`).
- Riding at the end, all at their seats (pose ZERO): the rocker switch on F4; washer, nut, knob on the potentiometer; the four LCD
  female caps (NAUO97 - 100) on the LCD; both F7s and F9 on F3. F1, the potentiometer, F4, the LCD and the buzzer do **not** ride (a
  Full Build step moved each of them home with `move=`).
- Leads: resistor legs (a = resistor, b = None: they go with it); eight jumpers (a, b = the two caps, `stretch`); switch red / tan /
  black (a = SWITCH, b = the cap, `stretch`); pot red / tan / black (a = the cap, b = POT, `tail_from`); buzzer red / black (a = cap,
  b = BUZZER); lcd purple / yellow / teal / blue (a = male cap, b = female cap); usb cable (a = USB_B, b = USB_A, `tail_from`).
- Records (`came`; `*` = the one used when the part is taken off on its own or with its whole group):

| part (id) | record | way | notes |
|---|---|---|---|
| F6, F5, F8 | 57, 55, 50 | -z 67.5, +z 56, +x 94 | one stage each |
| F2 | 56 | 3 stages, reversed: swung out about its hinge, 14 mm along itself out of F5's slots, 40 mm out along -x | 56c also changes the USB cable (`wire_via` [74, 124] -> 125) |
| F1 + POT (NAUO10, NAUO11) | 54, **group of two** | +x 76.7 (FRONT_OUT) | list both, or neither has a fit (a straight pull instead) |
| F4 | 49 | up 49.8 (HOVER_F4) | its lying beside the base (48) was a ride: no record |
| LCD (NAUO94) | 52 | ZERO -> STANDING -> via x3 -> ANGLED, stops [0, 1, 5] reversed: 2 beats | 51 (stood up, carried in) was a ride |
| buzzer (NAUO62) | 43 | ZERO -> HIGH -> LIFT -> LYING, 3 beats | 43c `wire_via` 2 routes per lead |
| USB_B (NAUO122) | 40 | +z 18 | USB_A: no record |
| switch caps NAUO47 / 49 / 48 | 16 / 17 / 18, rode = SWITCH | up 18 / 18 / 5 | hover route = plugged route (30 / 31 / 32): see 5.1 |
| pot caps NAUO34 / 33 / 14 | 30 / 31 / 32, rode = POT | up 18 / 18 / 5 | hover route = plugged route (47 / 48 / 49) |
| buzzer caps NAUO58 / 59 | 33 (5 poses, stops [0, 3, 4]) / 34 (3 poses), rode None / BUZZER | back to where they lay on the buzzer | 33c / 34c `wire_via` 1 route each |
| LCD male caps NAUO82 / 84 / 86 / 93 | 36 / 37 / 38 / 39 | up 18 | female caps: no record |
| jumper pairs | 9 - 12, 20, 21 (up 18); 13, 14 (up 5, then +x 14) | group of two each | one unit (the two ends of one lead) |
| RTC + COIN (NAUO3, NAUO4) | 7, **group of two** | up 34 | list both |
| RES1, RES2 | 5, 6 | up 37 | legs go with them |
| NANO | 3 | up 40 | |
| BREADBOARD (NAUO1) | 2, then **still ways** 23, 27, 29, 47 (all ZERO: pacing rides) | the latest is a still way: a default remove would not move | never taken off (the published ends on it) |
| no record | F3, F9, F7A, F7B, SWITCH, KNOB, NUT, WASHER, LCD female caps, USB_A, PAPER | - | hand ways only |

---------------------------------------------------------------------------------------------------------------------------------

## 3. (a) Panels slid out; arrows of a given size; two-stage moves with an arrow per stage

### 3.1 The published arrows, measured (length / shaft width, mm)

`python3 -I docs/research/lsm/decon/arrows/measure_arrows.py docs/research/lac/decon/published/raw/19075-lac_deconstruction.json <out>`
(the LSM session's script, calibrated on the PMG's; the LAC payload's axes are ours: F6 -Z, F2 -X, F5 +Z, F1 and F8 +X, as our build
moves them). Our player draws the head 4w wide and min(0.6 L, 3.4 w) long, so `dims=(L, w)` gives the published 5 : 20 : 17 arrow.

    PUBLISHED = dict(f6=(56.1, 4.87), f2=(79.8, 5.51), f5=(64.6, 6.19), f1=(79.0, 5.78), f8=(83.9, 4.51), f4=(73.2, 3.35),
                     knob=(41.2, 2.93), nut=(56.5, 3.72), washer=(70.6, 2.89), pot=(52.7, 4.21), f9=(33.8, 3.3), usb=(63.5, 5.78),
                     f7_spread_a=(36.9, 3.75), f7_spread_b=(40.5, 3.8), buzzer=(58.3, 6.15), f7_a=(37.3, 3.96), f7_b=(34.2, 3.96),
                     switch=(63.6, 4.95), rtc=(29.8, 3.55), res1=(39.4, 3.47), res2=(46.8, 3.96), nano=(64.2, 3.72))
    size = lambda key, **more: dict(dims=PUBLISHED[key], **more)          # (as the PMG's and LSM's scripts)

(Published Steps 5, 6, 9 - 11, 19 - 23, 29 - 34, 36 - 43 have an eye and no arrow; 26 and 28 have two arrows, one per F7.)
Whether the LAC takes the published sizes (Lee's PMG ruling, applied by analogy in the LSM) or the in-house 15 - 40 mm (the MRA's
default, `_arrow_dims`) is Lee's call; the LSM precedent is the published sizes.

### 3.2 One panel, one arrow, the Full Build's way reversed

    g.remove('Remove F6 from the end of the case.', [F6], arrow_style={F6: size('f6')}, caution=POWER)   # Step 57 reversed: -z 67.5,
    g.remove('Remove F5 from the other end of the case.', [F5], arrow_style={F5: size('f5')})          # by Step 57's / 55's camera
    g.remove('Slide F8 out of the slots in F4 and F3, towards the front.', [F8], arrow_style={F8: size('f8')})   # Step 50: +x 94

The arrow runs along the way, from just outside the part's middle (`_arrow_out`: tail = the part's centre moved 2 mm past its far side
along the way, then moved on 4 mm at a time until the camera sees it). `at=[x, y, z]` puts the tail by hand (the published F6 arrow's
tail is on F6's lower corner), `shift=` moves it, `face=` turns its flat face, `keep=True` keeps one that points at the camera (else it
becomes an eye). Order: the generator warns ("the way out of Step N passes through a part still there") if a straight Full Build way is
blocked by a part the order leaves on (F1 before F5 / F6, for instance).

### 3.3 Two or more stages, an arrow per stage in turn (`stage=`, `then=`)

`arrow_style={id: dict(dims=..., stage=0, then=[dict(stage=1, dims=...), ...])}`: Step N shows stage 0's arrow; as the step plays, each
part rests a beat before each later stage while that stage's arrow fades in, and the arrow goes as its own stage plays (Lee's PMG
rulings, 21 Oct 2026). Stage numbers count the way's stages as given (the rest beats are added and renumbered by the generator). Rules
(ValueError otherwise, 1104-1117, 1828-1829): the first arrow needs `stage=`; later stages in order, after it, within the way; every
part the step moves has the same number of stages; no `in_turn=`; **no `wire_via=`**. A still (step list, 2D PDF) draws all of them.
`stage=k` alone (no `then=`) puts the one arrow along stage k (the RCC's joysticks, `stage=0`).

**F9** (published Step 24: tilt about its foot to unhook, then up 33 mm still tilted; one 33.8 mm arrow up; a close-up of the foot
hooked under F3). F9 has no record (it came in by `ride=`): walk Steps 46 and 45 back by hand. Its poses, relative to its seat with F3 in
its seat (so absolute): Step 46's carry pose (HOOKED, tipped 25.79 degrees about its front edge) and Step 45c's `via[0]` (TIPPED, the same
tilt 33 mm higher). Stopping there matches the published two stages (Step 45's first pose, F9 upright 35 mm over its slots, is not
needed):

    HOOKED = VIEW['Step 46']['carry'][F9]['pose']                        # (the swing back: its back foot up out of its slot)
    TIPPED = VIEW['Step 45c']['carry'][F9]['via'][0]                    # (then up 33 mm, still tipped: its front foot out from under F3)
    FOOT = VIEW['Step 45c']['inset']                                    # (the Full Build's close-up: the front foot's barb under F3, F3 faint)
    g.remove('Tip F9 towards the front to free its back foot, then lift it up out of its front slot.', [F9], path=[HOOKED, TIPPED],
             arrow_style={F9: size('f9', stage=0, then=[size('f9', stage=1)])},
             inset=dict(target=FOOT['target'], dir=FOOT['dir'], radius=FOOT['radius'], mark=FOOT['mark'], ghost=FOOT['ghost'],
                        alt=FOOT['alt']),
             **camera_of('Step 46'))                                    # (a hand way: the generator would choose a camera itself)

**F7 pair** (published 26: spread apart, two opposed arrows, they stay; 27: the buzzer out; 28: both straightened and lifted 44 mm,
two up arrows). Neither F7 has a record (rides on F3). Spread = Step 44 reversed, a lift that keeps them riding on F3 (without
`ride_on=F3` the second would ride on the first from then on, 1205):

    TILT = {i: VIEW['Step 42c']['carry'][i]['pose'] for i in (F7A, F7B)}   # (15 degrees each way about its foot)
    g.lift('Spread the tops of the two F7s apart.', [F7A, F7B], paths={i: [TILT[i]] for i in (F7A, F7B)}, ride_on=F3,
           arrows=[dict(a, part=F3, width=3.8) for a in VIEW['Step 42']['arrows']],   # (the Full Build's own spread arrows; absolute,
           **camera_of('Step 44'))                                      #  so on F3, which is in its seat)
    ...                                                                 # (the buzzer out: section 4.3)
    UP80 = VIEW['Step 41']['carry'][F7A]['pose']                         # ([0, 80, 0]: where the Full Build held them)
    g.remove('Let the two F7s close, then lift them up out of their slots in F3.', [F7A, F7B],
             paths={i: [[0.0, 0.0, 0.0], UP80] for i in (F7A, F7B)},    # (two stages: straightened, then up)
             arrow_style={F7A: size('f7_a', stage=1), F7B: size('f7_b', stage=1)},   # (as published: only the lift's arrows; or
             **camera_of('Step 41'))                                    #  stage=0 + then=[stage 1] for an arrow per stage)

With `paths=` per part each F7 is a unit of its own, so each gets its arrow (`('own', i)` units, 1175).

**F2** (published Step 2: tilt about 21 degrees about an edge, then slide 78 mm; one 80 mm -X arrow; an eye on the USB cable at F2's
slit). Our Full Build brought it in 3 stages (in along x, 14 mm along itself into F5's slots, swung shut), the USB cable following the
slit (56c `wire_via`). Reversed by default, with the cable walked back too:

    g.remove('Swing the free end of F2 out, slide its tabs out of F5, then pull it away from the back of the case.', [F2],
             wires={'usb cable': ROUTES[VIEW['Step 56']['wires']['usb cable']]},                # (74: the line the slit came in along)
             wire_via={'usb cable': [ROUTES[n] for n in VIEW['Step 56c']['wire_via']['usb cable'][::-1]]},   # (124, 74: a stage each)
             arrow_style={F2: size('f2', stage=2)},                     # (one arrow, on the pull away: then= is refused with wire_via)
             eye=[dict(e) for e in VIEW['Step 56']['eye']])             # (the Full Build's eye on the cable in the slit)

3 stages, `wire_via` 2 + the final route = 3 legs: the cable keeps pace. Arrows in turn are not possible in the same step (see 3.4).
Without the `wire_via` (then= allowed), the slit moves about 13 mm across the cable during the 14 mm slide and F2's wood passes through
the cable. A two-stage way like the published (`path=[swung, swung(F2_OFF)]`, skipping the 14 mm) drags F2's hooks diagonally through
F5's slots (F5 is already off by then in the published order, but not in a strict reverse: F5 comes off after F2).

### 3.4 Where `then=` cannot go, and the smallest change that would let it

`_takeoff` refuses `then=` with `wire_via=` (1116-1117) because the rest beats it inserts (1118-1124) would put the lead's stages out of
step. Padding each lead's stages the same way would keep them in step: for each inserted rest before stage k, repeat the route at the
end of stage k-1. In `_takeoff`, after `ways[i], stops[i] = w, st` (1124), instead of the ValueError:

    if wire_via:                                  # (a lead rests while its part rests: its route at the end of the stage before, again)
        for w, rs in wire_via.items():
            rs = list(rs)
            for k in reversed(holds):             # (k >= 1: then= stages come after the first arrow's)
                rs.insert(k - 1, rs[k - 1])
            wire_via[w] = rs

(and drop 1116-1117). Untested; it touches every kit's generator, so it is Lee's call. Without it, the LAC has three steps where Lee's
"an arrow per stage" and a lead's stage-by-stage shapes conflict: F2 (USB cable), the buzzer out from between the F7s, the LCD unclipped.

---------------------------------------------------------------------------------------------------------------------------------

## 4. (b) Tethered parts moved but kept on screen, still wired

### 4.1 The mechanics

- `lift()` moves the parts and leaves them on screen: one mover rests at its last pose; several: the others ride on the first; with
  `ride_on=X`, each rides on X (one id). Riders of the movers (the switch on F4, the knob / nut / washer and later the hanging caps on
  the potentiometer, the female caps on the LCD) are carried by `with_riders` (1721-1735). Nothing leaves, so the "lead left with one
  end" check does not apply.
- **No lead is re-routed by lift() or remove()** (1139: `after = wires or {}`). A route is drawn for its end parts at given poses
  (`a_ref` / `b_ref`, wires.py 48; player.js 114 `endMove`): the player moves it with its ends from those poses, blending along its
  length. So a Full Build route is exactly right when its end parts are where they were in the Full Build view it comes from, and
  bends (sometimes through parts) anywhere else. Hence: **walk the Full Build back, and give each tethered move the routes of the Full
  Build view whose state it ends in**: `wires=` = the hover view of the Full Build step being undone (the state before it), and
  `wire_via=` = that step's done view `wire_via`, reversed (its in-between shapes).
- `unplug()` re-routes by itself: each lead with an end on the plug takes the route of the Full Build step's hover view, and that step's
  `wire_via` reversed (1143-1149). For the LAC's caps the hover route is the plugged one (5.1).
- `wires_here={w: route}` changes how leads are drawn on this step's two views only (the MRA's joystick wires fading in the hand).

### 4.2 How the scripts get the Full Build's poses and routes (all from steps.json)

- Routes: `ROUTES[VIEW[step]['wires'][w]]` (the route a lead had in that view); `VIEW[step + 'c']['wire_via'][w]` (route numbers of its
  in-between shapes). MRA / LSM: `leads(step, prefix)` = `{w: ROUTES[n] for w, n in VIEW[step]['wires'].items() if w.startswith(prefix + ' ')}`.
- Poses of a mover: `VIEW[step]['path']` or `['paths'][id]`, stops in `['stops']` / `['path_stops'][id]` (JSON loses `via()`:
  `full_way_back()` re-wraps the non-stops, MRA 92-99, LSM 73-80).
- Poses of a ride (`ride=` in guide.py): `VIEW[step]['carry'][id]['pose']` is where it rode as the step opened, `VIEW[step + 'c']['carry']
  [id]` = `{by, pose, via}` where it ends and the poses between. Relative to the carrier's seat: absolute when the carrier (F3 here) is
  in its seat; `compose(where(carrier), rel, g._pivot(id))` otherwise.
- Helpers to copy: MRA `camera_of`, `leads`, `walked_back(step, plug, prefix, carrier_pose, pivot)` (a plug's ride walked back with its
  lead's stages, for `lift(..., ride_on=)`), `riding_back(step, part)`, `full_way_back`; PMG `lifted_back(step, part)` (wire_via and
  wires for a mover step the generator walks back itself) and `carried_back(step, part)` (a ride on H1 walked back: path, wire_via,
  wires); LSM `carried_back(step, part, prefix)` (with an assert that the part is where that step left it), `slid`, `at_now`,
  `shift_of`; RCC `turned_camera`; all: `where(i)`.
- Numbers copied as numbers where steps.json does not hold them (RCC's `L2_MID_Z`, arrow tails). Never `import guide`.

For the LAC (paste-ready):

    def camera_of(step):
        """A Full Build step's camera, for a step of ours whose way is by hand (the generator reuses it by itself otherwise)."""
        c = VIEW[step]['camera']
        return dict(view_dir=c['dir'], frame=(c['target'], c['radius']))

    def leads(step, prefix):
        """The routes a set of leads had in a Full Build view: {wire: route}."""
        return {w: ROUTES[n] for w, n in VIEW[step]['wires'].items() if w.startswith(prefix + ' ')}

    def stages_back(step, prefix):
        """A Full Build step's in-between lead shapes (its done view's wire_via), walked back: {wire: [route, ...]}."""
        return {w: [ROUTES[n] for n in nos[::-1]] for w, nos in (VIEW[step + 'c'].get('wire_via') or {}).items() if w.startswith(prefix + ' ')}

    def ride_back(step, part, carrier_now=None):
        """A Full Build ride of `part` (ride=), walked back: its in-between poses and where it rode as the step opened, a stop each,
        made absolute with where its carrier is now (None: in its seat)."""
        c = VIEW[step + 'c']['carry'][part]
        rel = [*(c.get('via') or [])[::-1], VIEW[step]['carry'][part]['pose']]
        return [compose(carrier_now, p, g._pivot(part)) if carrier_now is not None else p for p in rel]

    def where(i):
        """Where a part is now (through what it rides on)."""
        if i in g.riding:
            by, rel = g.riding[i]
            return compose(where(by), rel, g._pivot(i))
        return g.resting.get(i)

### 4.3 The LAC's tethered moves, each the Full Build's own, reversed

**F1 pulled forward, then laid aside** (published 4, 5). Step 54 reversed (a record, both listed), then Step 53's ride reversed:

    g.lift('Pull F1 forward off the tabs of F4 and F3. Leave its potentiometer wires connected.', [F1, POT],
           wires=leads('Step 54', 'pot'), arrow_style={F1: size('f1')})   # (Step 54 reversed, by its camera; POT rides on F1 from now on)
    g.lift('Lay F1 face down in front of the case, out of the way.', [F1], path=[VIEW['Step 53']['carry'][F1]['pose']],   # (F1_ASIDE)
           wires=leads('Step 53', 'pot'), arrows=[], eye=[F1], **camera_of('Step 53'))   # (published: an eye, no arrow)

**F4 lifted off the frame, still wired** (published 8: up, then "held above"). Step 49 reversed (record), then, to unplug the switch's
leads with the Full Build's own shapes (5.1), Step 48's ride reversed, back to lying beside the base (both by the Full Build's
CASE_CAMERA, which Steps 48 and 49 share); or both in one lift of two beats:

    FLAT_F4 = VIEW['Step 48']['carry'][F4]['pose']                       # ([-82.7, 17.3, -0.1]: lying beside the base, where the switch
    g.lift('Lift F4, with the rocker switch, up off the tabs of the F7s and F9, and lay it beside the case. Leave the switch wires '   # was wired
           'connected.', [F4], path=[VIEW['Step 49']['path'][0], FLAT_F4],   # (HOVER_F4, then down beside the base: a beat each)
           wire_via={w: [ROUTES[VIEW['Step 49']['wires'][w]]] for w in leads('Step 49', 'switch')},   # (84 - 86: over the frame)
           wires=leads('Step 48', 'switch'),                            # (30 - 32: as they lay before Step 48)
           arrow_style={F4: size('f4', stage=0)}, **camera_of('Step 49'))

**LCD unclipped from F9 and F8 and laid face down, still wired** (published 6, one step, an eye and a close-up with two red boxes).
Step 52 (record: way reversed, 2 beats) then Step 51's ride (4 beats) reversed. As two steps:

    NOTCHES = VIEW['Step 52c']['inset']
    g.lift('Slide the LCD screen out of the notches in F9 and straighten it out through the slots in F8. Leave its wires connected.',
           [LCD], wires=leads('Step 52', 'lcd'), wire_via=stages_back('Step 52', 'lcd'),   # (106 - 109 angled; via 110 - 113 standing)
           arrows=[], eye=[LCD],
           inset=dict(target=NOTCHES['target'], dir=NOTCHES['dir'], radius=NOTCHES['radius'], alt=NOTCHES['alt'],
                      marks=[(m['at'], m['half']) for m in NOTCHES['marks']]))   # (steps.json writes marks as {at, half}: give tuples)
    g.lift('Lift the LCD screen out of the case and lay it face down beside it.', [LCD], path=ride_back('Step 51', LCD),   # (4 stops)
           wire_via=stages_back('Step 51', 'lcd'), wires=leads('Step 51', 'lcd'),   # (3 shapes + the lying ones: a beat each)
           arrows=[], eye=[LCD], **camera_of('Step 51'))

As one step (as published): `path=[*full_way_back('Step 52', LCD), *ride_back('Step 51', LCD)]`, `wire_via` = Step 52's (standing),
the angled routes (`leads('Step 52', 'lcd')` as a list), then Step 51's three; `wires` = Step 51's: 6 stops, 5 + 1 routes. One camera
must then frame both moves (Step 51's is the wider).

**The buzzer out from between the F7s, laid on the table, still wired** (published 27). Step 43 reversed (record, 3 beats), as the PMG's
`lifted_back()`:

    g.lift('Lift the buzzer up out from between the two F7s and lay it beside the base. Leave its wires connected.', [BUZZER],
           wires=leads('Step 43', 'buzzer'), wire_via=stages_back('Step 43', 'buzzer'),   # (52 / 53; via 76, 75 / 78, 77)
           arrow_style={BUZZER: size('buzzer', stage=0)}, eye=[BUZZER])   # (the arrow on the lift out; published: an arrow and an eye)

Afterwards the buzzer rests (one mover, no `ride_on`) at BUZZER_LYING.

**F1 walked back further** (to unplug the potentiometer's leads with the Full Build's own shapes, 5.1; and, if the strip-down is done
with F1 upright as the Full Build did it, 6.2):

    g.lift('...', [F1], path=[VIEW['Step 47']['carry'][F1]['pose']], wires=leads('Step 47', 'pot'), **camera_of('Step 47'))   # (F1_DOWN)
    g.lift('Stand F1 up again, the knob towards you.', [F1], path=[VIEW['Step 29']['carry'][F1]['pose']],   # (BUILD, [100, 35, 100])
           wires=leads('Step 29', 'pot'), **camera_of('Step 29'))       # (41 - 43: the leads hanging, as before Step 29)

### 4.4 Order: a strict reverse stays on existing routes; the published order does not everywhere

Each route above is right only in the state of the Full Build view it comes from (4.1). The published order differs from a strict
reverse of our Full Build in places (it lays F1 aside before the LCD comes out, as our Full Build's Steps 47 - 54 did; but it unplugs the
potentiometer's leads before the LCD's, which our Full Build plugged in the other order; it takes F9 and the USB plug before the F7s,
which our Full Build put in before them). Where a lead must change shape in a state the Full Build never had, its route has to be drawn
in the script with `tools/wires.py` (`import wires as W`, as guide.py does) and the guide's own helpers (`pot_plugged`, `lcd_lead`,
`usb_cable` ... live in guide.py and would have to be copied, or moved into a module both scripts import: a guide.py change, Lee's
call). Two leads that each keep their own Full Build route but are now unplugged in another order can cross; motioncheck.py and
wirecheck.py tell (section 9).

---------------------------------------------------------------------------------------------------------------------------------

## 5. (c) Unplugging; two-ended wires; labels

### 5.1 A lead whose other end stays on its part: `unplug()`

`g.unplug(caption, [cap])`: the cap comes out its Full Build way reversed, its lead takes that step's hover route (and `wire_via`
reversed), it then rides on what it rode on before that step (`rode`) or `ride_on=`; an eye on each plug, no arrow (1131-1149, 1190).
Refused if the Full Build never plugged it in (no record) or it is not in its seat (1050-1051).

For the LAC (records: 2):
- switch caps (16 - 18, rode = SWITCH), pot caps (30 - 32, rode = POT), buzzer black (34, rode = BUZZER): `unplug()` works with nothing by
  hand and the cap rides on its part afterwards.
- buzzer red (33): `rode` is None (the buzzer appeared in that very step), so give `ride_on=BUZZER`, or the cap stays where it lands and
  a later `remove([BUZZER])` is refused ("the lead buzzer red would be left on NAUO58 ...").
- **The LAC's switch and pot hover routes are the plugged routes** (Step 16's 'switch red' is 30 in both views; Step 32's 'pot black' 49
  in both): the generator's unplug lifts the cap 18 mm (5 for the switch's and the pot's black) and leaves it there, riding on its part, its lead in its
  plugged shape. The Full Build had them hanging from the part before (Step 15c: switch caps; Step 29c: pot caps; routes 27 - 29 and 44 -
  46). The published guide shows them hanging ("Swap: black wire hangs straight below F4"). The exact walk-back is a two-stage unplug by
  hand (as the MRA's `walked_back()`): out, then down to where it hung, its lead through the Full Build's two shapes:

        def unplug_to_hanging(caption, cap, wire, plugged_step, hanging_view, part, **more):
            """A Full Build step that plugged `cap` in (from held over its hole), walked back on to where the cap hung from `part` in the
            Full Build view before it (`hanging_view`), its lead through the plugged shape to the hanging one: a beat each."""
            held = VIEW[plugged_step]['path'][0]                                   # ([0, 18, 0], or [0, 5, 0] for the two black ones)
            hang = compose(where(part), VIEW[hanging_view]['carry'][cap]['pose'], g._pivot(cap))
            g.unplug(caption, [cap], path=[held, hang], ride_on=part,
                     wire_via={wire: [ROUTES[VIEW[plugged_step]['wires'][wire]]]},
                     wires={wire: ROUTES[VIEW[hanging_view]['wires'][wire]]}, **camera_of(plugged_step), **more)

        unplug_to_hanging("Unplug the rocker switch's black wire from j29.", SWITCH_CAPS['black'], 'switch black', 'Step 18', 'Step 15c', SWITCH)
        unplug_to_hanging("Unplug the rocker switch's tan wire from the (+) red rail.", SWITCH_CAPS['tan'], 'switch tan', 'Step 17', 'Step 15c', SWITCH)
        unplug_to_hanging("Unplug the rocker switch's red wire from j27.", SWITCH_CAPS['red'], 'switch red', 'Step 16', 'Step 15c', SWITCH)
        unplug_to_hanging("Unplug the potentiometer's black wire from the (-) blue rail.", POT_CAPS['black'], 'pot black', 'Step 32', 'Step 29c', POT)
        ...                                                                         # (tan: Step 31, red: Step 30)

  With a hand way, the camera, the routes and `ride_on` are not taken from the record (1050-1053, 1131-1149), hence the arguments. Each
  is exact only in the Full Build's state of that step: F4 lying flat beside the base (FLAT_F4) for the switch, F1 face down at F1_DOWN
  for the potentiometer (4.3), and the other leads of the set as they were (unplugged in the reverse order: black, tan, red, which is
  also the published order).
- buzzer leads: `g.unplug("Unplug the buzzer's black wire from the (-) blue rail.", [BUZZER_CAPS['black']])` and
  `g.unplug("Unplug the buzzer's red wire from j4.", [BUZZER_CAPS['red']], ride_on=BUZZER)`: Steps 34 / 33 reversed by the generator,
  the routes their own (53 -> 53 -> 51; 52 -> 52 -> 50, a beat each), back to where each lay on the buzzer. Exact once the buzzer is back
  at BUZZER_LYING (4.3). The published order is red then black (the build's order); the reverse is black then red.

### 5.2 A two-ended loose wire taken off both ends: `remove([cap_a, cap_b])`

Both ends leave, so the lead goes with them and fades (`lead_off`, 1153-1165). Its route is not changed; it is carried by its two
moving ends.
- **Jumpers** (records, one unit each: the two ends of one lead are never split into two arrows, 1177-1186): by default up 18 (Steps 13 /
  14: up 5, then +x 14), both ends together, so the wire rises whole; by the Full Build step's camera, which is very close (radius 26 -
  44). As published (an eye on one plug, no arrow) and with one camera for the run (published: all eight jumpers, the RTC, the resistors
  and the Nano from one view):

        BOARD_CAMERA = dict(view_dir=[0.5792, 0.5736, -0.5792], frame=([676.5, 916.0, 1310.0], 60.0))   # (to be chosen in the player)
        for k, (colour, (a, b)) in enumerate(JUMPERS.items()):
            g.remove(f'Unplug the {colour.replace("_", " ")} breadboard wire from both its holes.', [a, b], arrows=[], eye=[a],
                     **(BOARD_CAMERA if k == 0 else dict(keep_camera=True)))

  (The Full Build's jumper cameras look down steeply, dir . up = 0.82: an arrow straight up there would turn into an eye, 1465.)
  Or several at once (Lee's PMG / LSM ruling, "the breadboard wires" as a group): `remove(all_caps, arrows=[], eye=[one cap per
  bundle])` (MRA 238-239) or an arrow per bundle with `units=` (PMG 224-227).
- **LCD wires** (male cap in the breadboard, a record; female cap on the LCD's header, riding, no record). Three ways:
  1. one wire per step, as published, both ends off: `remove([male, fem], paths={fem: [compose(where(LCD), VIEW[step]['carry']
     [fem]['pose'], g._pivot(fem))]})`, `step` the wire's own Full Build step, 36 - 39 (the female 15 mm back off its pin, [0, 0, 15] on
     the LCD, where the Full Build held it; the male up 18 by its record),
     `arrows=[]`, `eye=[male]`, the pin's label (below). The camera is Step 36's by itself (only the male has a record, 1194).
  2. a pure fade, as the published "routed wire cross-fades to a loose wire, then fades": every way of zero length, `paths={male:
     [ZERO], fem: [where(fem)]}`: no slide, the wire and both caps fade where they are (awayTiming: restAt 0, fade at 0); `_arrow_out`
     returns None for a way under 1 mm, so give `eye=`.
  3. as the LSM's and PMG's: the LCD pulled off its four female caps (`remove([LCD], let_go=LCD_FEMALE, path=...)`), then the wires out
     of the breadboard together (`remove(LCD_MALE + LCD_FEMALE, paths={c: [_shifted(where(c), [0, 25, 0])] ...}, arrows=[], eye=...)`).
  Then "take the LCD away" (published 23, an eye, no motion): `g.remove('...', [LCD], paths={LCD: [where(LCD)]}, arrows=[], eye=[LCD])`.
- **USB cable**, as all four kits: one arrow on the plug pulled, none on the far end, which is lifted with it:

        g.remove("Unplug the USB cable from the Nano Board.", [USB_B, USB_A], units=[[USB_B]], arrow_style={USB_B: size('usb')},
                 paths={USB_A: [_shifted(where(USB_A), [0.0, 25.0, 0.0])]})   # (USB_B: Step 40 reversed, +z 18, by its close camera:
                                                                                #  give view_dir= / frame= for a wider one, as the RCC's)

### 5.3 Labels on a take-off step

`labels=[...]` (Step N only): an id (text = its hover name) or a dict with `id`, `text`, and optionally `anchor` (seated mm on `id`;
placed where the camera sees it if left out), `side`, `reach`. The published GND / VCC / SDA / SCL labels are on the LCD's header pins:
the Full Build's Steps 36 - 39 carry exactly those labels (anchor on the LCD, seated, `side='near-right'`), as the MRA copied its Row
labels (MRA 129-132):

    PIN_LABEL = {fem: next(dict(l) for l in VIEW[step]['labels'] if l['id'] == LCD)
                 for (male, fem, pin), step in zip(LCD_WIRES.values(), ('Step 36', 'Step 37', 'Step 38', 'Step 39'))}
    g.remove('Unplug the purple LCD wire from GND on the LCD screen and from the (-) blue rail.', [male, fem], arrows=[], eye=[male],
             labels=[PIN_LABEL[fem]], paths=...)                         # (as 5.2)

The anchor is right wherever the LCD lies (it is on the LCD, seated). The published has no hole labels on these steps (the Full Build's
second label, on the breadboard, is left out). Rulebook section 11 says "no text labels" in a take-apart, with Lee's MRA exception for
row labels on unplugs; the published LAC's four pin labels are the same kind of exception.

---------------------------------------------------------------------------------------------------------------------------------

## 6. (d) Isolation: a sub-assembly taken apart on its own

### 6.1 Mechanics

- `alone=[ids]` on each step of the run: only those and what rides on them are shown (riders added, 1001-1002), leads whose both ends are
  shown are drawn, both views are `isolated`. The parts hidden keep their state; the first step without `alone=` shows them where they
  were (the player cuts, no glide). There is no `hide=` for a run: repeat `alone=` (the MRA's `without()` helper).
- `keep_camera=True` for the steps after the first (Lee: "two steps on one sub-assembly in the hand keep one camera").
- At the end of the run, `put_away([what is left])`: off the screen for good, its riders and leads with it; the next view cuts in.
  (The published hides F1 and F4 after their runs: the same thing.)
- A takeoff step's way for a part riding on a moved carrier must be made absolute: `compose(where(carrier), rel, g._pivot(part))`.
- `flip=True`: the model shown turned over (camera below); the player turns only upside down. The published LAC turns the scene's up axis
  to -X for these runs (so F1, lying flat, stands upright on screen): **not available**. Either move the sub-assembly into an upright pose
  with a real step (the Full Build's own), or look at it as it lies (a view by hand, `flip=True` to see its underside).

### 6.2 F1 with the potentiometer (published 12 - 15: knob, nut, washer off along the shaft, then the pot pushed out of F1's back)

In the Full Build the strip-down and refit (Steps 22 - 28) were done with F1 upright at BUILD ([100, 35, 100]), the potentiometer
riding on F3 behind it, all by one camera (Steps 25 - 28: dir [0.3505, 0.4506, -0.8211], target [822, 960, 1375], radius 98). The exact
reverse: stand F1 back up (Step 29 reversed, 4.3), then Steps 28, 27, 26, 25 reversed, alone, by that camera. Knob, nut and washer have
no record (they rode on the potentiometer): their ways come from the carry entries (relative to the potentiometer):

    F1_SET = [F1, POT]                                                   # (+ what rides on it: knob, nut, washer, the three hanging caps)
    g.remove('Pull the knob off the potentiometer.', [KNOB], alone=F1_SET, arrow_style={KNOB: size('knob')},
             paths={KNOB: ride_back('Step 28', KNOB, where(POT))},      # ([60, 0, 0] along the shaft, from where the pot is now)
             **camera_of('Step 28'))
    NUT_WAY = ride_back('Step 27', NUT, where(POT))                     # (seven quarter turns back, then off: 8 stops = 8 beats; make all
    NUT_WAY = [via(p) if k not in (3, len(NUT_WAY) - 1) else p for k, p in enumerate(NUT_WAY)]   # but two via(): 2 beats, as the build's)
    g.remove('Unscrew the nut and take it off the shaft.', [NUT], alone=F1_SET, path=NUT_WAY, arrow_style={NUT: size('nut')}, keep_camera=True)
    g.remove('Take the washer off the shaft.', [WASHER], alone=F1_SET, paths={WASHER: ride_back('Step 26', WASHER, where(POT))},
             arrow_style={WASHER: size('washer')}, keep_camera=True)
    POT_OUT = relative_pose(VIEW['Step 25']['carry'][F1]['pose'], VIEW['Step 25']['carry'][POT]['pose'], g._pivot(POT))   # ([-79, 0, 0] on F1)
    g.remove("Push the potentiometer out through the back of F1.", [POT], alone=F1_SET, arrow_style={POT: size('pot')},
             paths={POT: [compose(where(F1), POT_OUT, g._pivot(POT))]}, keep_camera=True)   # (its hanging caps and leads go with it)
    g.put_away([F1])

(The nut's `via` poses are dicts with a turn of up to 720 degrees about the shaft's axis point; `compose()` keeps them as turns about the
nut's pivot. The Full Build paced the nut's ride with the breadboard's still way: our nut is a mover, so its stops pace it.) Lee's rule
("a part, once disconnected, disappears: it is removed, never reconnected, so nothing is refitted for storage, as LAC does") and the API
(`place()` refused) both leave out the published re-assembly (Steps 16 - 18); a `g.note('Put the washer, nut and knob back on the
potentiometer to store it.')` card is the only way to say it.

Without standing F1 up (it lies face down at F1_DOWN or F1_ASIDE, knob down): the same four steps with views by hand; the knob, nut and
washer then come off downward, the potentiometer upward out of F1's back. `flip=True` on the first three shows them coming off upward on
screen; the fourth is seen from above. The published Step 15 also changes camera for the pot (from below / behind). A fade instead of the
walk to BUILD: `lift('...', [F1], path=[BUILD], wires=leads('Step 29', 'pot'), reappear=True, alone=F1_SET)` (as the published pose swaps).

### 6.3 F4 with the switch (published 35: the switch pushed up out of F4, isolated; then the base restored)

With F4 lying flat beside the base and the switch's leads hanging (5.1): Step 15 reversed, the switch rode on F4 50 mm over it:

    g.remove('Push the rocker switch up out of the square hole in F4.', [SWITCH], alone=[F4, SWITCH], arrow_style={SWITCH: size('switch')},
             paths={SWITCH: [compose(where(F4), VIEW['Step 15']['carry'][SWITCH]['pose'], g._pivot(SWITCH))]},   # ([0, 50, 0] on F4)
             **camera_of('Step 15'))                                    # (the Full Build's: F4 is where it was then)
    g.put_away([F4])

The switch's caps ride on it after the unplugs, so they go with it and the leads fade with them.

### 6.4 Cameras for runs

- The Full Build's camera of the step being undone: by itself when the way is the record's (1193-1198); `**camera_of(step)` when the way
  is by hand; `camera_of(step, moved=shift)` (LSM 60-65) slides it with a sub-assembly that has slid since (a turned one needs its own,
  as the RCC's `turned_camera`).
- `keep_camera=True` for the rest of a run; `new_camera=True` / `look_from=` let the generator choose (one of the four diagonals);
  `view_dir=` + `frame=(target, radius)` set it exactly (a screenshot solved with camsolve.js).
- The generator logs `NOTE: ... the Full Build's camera leaves out <parts>, lying aside` where a borrowed camera misses a part off its
  seat (1790-1797): expected on the LAC for the USB A end on the table, F1 aside, the LCD and buzzer lying, F4 flat.

---------------------------------------------------------------------------------------------------------------------------------

## 7. (e) Close-ups on Step N (a catch to release)

On a take-off step `inset=` is drawn on Step N (1849-1855). Both published LAC close-ups exist in our Full Build already:

- **LCD in F9's notches** (published Step 6; two red boxes): `VIEW['Step 52c']['inset']`: target [713.1, 919.5, 1356.5], dir [0.5963,
  0.2981, 0.7454], radius 34, `marks` at [712.1, 947.3, 1356.5] and [712.1, 892.6, 1356.5], half 3.0. Pass `marks` as tuples
  (`[(m['at'], m['half']) for m in ins['marks']]`): `_takeoff` unpacks `for at, half in I['marks']` (1854), and the dicts steps.json holds
  would unpack as their two keys. Code in 4.3.
- **F9's foot hooked under F3** (published Step 24; one red box): `VIEW['Step 45c']['inset']`: target [716.0, 885.5, 1355.8], dir
  [0.1497, 0.1997, 0.9684], radius 10, `mark` 3.0, `ghost` {F3: 0.25}. Code in 3.3. Its `ghost` key is the CAD id 'NAUO2' already.
- Also available: Step 56c's (the USB cable in F2's slit), Step 25c's (the potentiometer's tab in F1's slot).
- Options as a build's: `caption=`, `alt=`, `side='left'` (tried first), `hide=[ids]`, `arrows=[ids]` (an arrow in the close-up for a
  part the camera cannot see, with `arrow_style={id: dict(face=dir_of_the_inset)}`, MRA 262-266). `image=` (a picture made outside) is
  not supported on take-off steps (no `_inset_image` call in that branch; the build's branch has it, 2004).

---------------------------------------------------------------------------------------------------------------------------------

## 8. (f) The frame of the guide

- **Guide(...)**:

        g = Guide(HERE, title='LCD Alarm Clock (LAC)', part='Deconstruction', names=dict(FULL['names']), steps_file='steps-deconstruction.json',
                  source='lac-guide.glb', hero_azimuth=135,             # (the Full Build's; Guide's defaults are 'mra.glb' and 225)
                  copyright_line='© TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')
        g.take_apart(parts_list_at_end=True, leave_out=[PAPER])          # (the Full Build's parts list after the Completed View; the backing,
                                                                         #  put away in the Full Build's Step 1, left out from the start)

  `FULL['names']` are the Full Build's hover names (Knob, Nut, Washer; caps named as their part or 'Breadboard Wire (M-M)' / '(M-F)'):
  they give default label text and decide "two of a kind" arrows. `review_notes=False` once past review.
- **leave_out=[PAPER]**: `take_apart()` takes every part any Full Build view showed, the ones its Completed View does not show from the
  last view that did (877-886). The backing (NAUO141) was put away at Step 1 with the breadboard holding it at [0, -50, 0], so it would
  come back 50 mm under the breadboard on every step. `leave_out` refuses a part the Completed View shows or that was never shown.
  The title page is the Full Build's Start (with the backing in its seat, unseen under the breadboard), so Step 1 glides from it.
- **Step 1 caution**: the USB plug is inside the closed case (F2's slit, F5 beside it), so the cable cannot come out first as the MRA's,
  RCC's and PMG's do. As the LSM's: `POWER = 'Disconnect the USB cable from the computer or power supply before you begin.'` on Step 1.
- **Title page**: the Full Build's (same camera, visible parts, wires) unless `start_view=` is given (2038-2041, 2096-2098); its
  subtitle is `part`. **Completed View**: what is left (F3 with the breadboard, as published), framed on it, from the last step's camera
  direction, or the hero's (azimuth 135) if the last step is turned over (2099-2104); `end_view=` overrides. Nothing left: SystemExit.
- **Card**: `_dev.card()` on `player.html?steps=steps-deconstruction.json` copies the Full Build's `cards/steps.webp` (runthrough.js
  130-143); the LAC has no `cards/` folder yet: make the Full Build's card first.
- **Model**: the deconstruction shows no part the Full Build does not, so `_sync_model` (2421-2435) does not rebuild model.glb.
- **guides.json** (do not add yet; for reference): the LAC has no kit entry and no Full Build entry. A deconstruction needs all three:

        "kits":   "lcd-alarm-clock": {"name": "LCD Alarm Clock", "code": "LAC", "folder": "LAC Build Instructions"}
        "guides": "lcd-alarm-clock-full-build":     {"kit": "lcd-alarm-clock", "steps": "steps.json", "label": "Full Build"},
                  "lcd-alarm-clock-deconstruction": {"kit": "lcd-alarm-clock", "steps": "steps-deconstruction.json", "label": "Deconstruction",
                                                     "script": "deconstruction.py"}

  (the addresses by analogy with Lee's; an LMS address must never change, so Lee names them.) publish.py then warns when the
  deconstruction is older than its script or than the Full Build it was taken from (`taken_from`, 361-370), and when its card is missing
  or stale (486-491).
- **Step text**: `step-text-deconstruction.json`; `python3 tools/step_text.py export "LAC Build Instructions" "share/<folder>/LAC
  deconstruction step text.csv" steps-deconstruction.json`. Every step has wording of its own (Lee's rule), in TechBox's take-apart style.
- **2D PDF**: `player.html?steps=steps-deconstruction.json`, `_pages()`, then `tools/make_pdf.py "LAC Build Instructions" "<pdf>"
  steps-deconstruction.json`.
- **Write-ups, as the others**: the script's docstring (the request quoted, the order and its reasons, what is not mirrored); the kit's
  README a "THE DECONSTRUCTION" section (PMG README 323-367 is the model: one line per run of steps, choices Lee may want otherwise,
  what was checked); CLAUDE.md, "A kit's guides": a "The LAC's (deconstruction.py, N steps, ...)" paragraph after the LSM's, the
  deconstruction's first-draft list ("the MRA's and the RCC's ...; the PMG's and the LSM's ...") and the Commands block
  (`.venv.nosync/bin/python "LAC Build Instructions/deconstruction.py"   # (the LAC's, likewise, after its guide.py)`); rulebook section
  11 any ruling Lee makes; the kit's README questions for Lee (the LSM's are numbered 20 - 25).

---------------------------------------------------------------------------------------------------------------------------------

## 9. (g) Running and checking it (as the others were)

Order (one heavy job at a time: `df -h /System/Volumes/Data`, `sysctl vm.swapusage` first; deconstruction.py loads lac-guide.glb, 7 MB):

1. `.venv.nosync/bin/python "LAC Build Instructions/guide.py"` first, whenever the Full Build changed (take_apart reads steps.json as
   last written); then `.venv.nosync/bin/python "LAC Build Instructions/deconstruction.py"`. Expected log: `take_apart(): from
   steps.json as it ends (57 parts, 25 leads)`, then one line per step (caption, remove / unplug / lift, parts, "the Full Build's way,
   reversed" / "by hand" / "pulled out along [..]" / "mixed", arrows, leads with them), then `N steps -> M views, ... wrote
   steps-deconstruction.json`.
2. Read the log's WARNING and NOTE lines:
   - `WARNING: <caption>: <parts> not in its seat: lifted straight up, unchecked` (+ Review note): a part with no record or riding,
     taken off with no way given. On the LAC: anything in the "no record" row of section 2. Give `path=` / `paths=` / `direction=`.
   - `WARNING: no straight way out was found in the CAD` (+ Review): no free axis for a computed pull.
   - `WARNING: <caption>: the way out of <Full Build step> passes through a part still there` (+ Review): a straight Full Build way
     blocked by a part the order leaves on (only ways from the seat with no turn; riders never count as obstacles). On the LAC likely
     where the order differs from the reverse (the USB plug's +z 18 before the F7s / buzzer, for instance).
   - `WARNING: <caption>: <name> looks plugged into a part that is lifted, and stays behind: list it with them` (lift only): a seated
     part with a Full Build record that rode in (`rode`), whose box touches a lifted part's within 1 mm. Possible on `lift([F1, POT])`
     (the pot caps near the potentiometer's body) and `lift([LCD])`: a false alarm if the cap is really in the breadboard.
   - `NOTE: <caption>: N arrows (the published take-aparts show 2 at most)`; `NOTE: ... the Full Build put this on in a sub-assembly
     view`; `NOTE: ... the Full Build's camera leaves out <parts>, lying aside (new_camera=True, or alone=)` (expected, 6.4);
     `NOTE: ... the arrow of stage k would point at the camera: left out (keep=True)`.
   - Errors stop the run (ValueError): not on screen; `alone=` without the movers; unplug of a part never plugged in; `in_turn=` not
     listing the movers or with a lead changing; `wire_via` without its last route in `wires=`; a lead left with one end
     (`unplug it first, take both its ends off together, or say wires={w: None}`); `units=` naming a non-mover; `then=` rules (3.3);
     `let_go=` naming a non-rider; `reappear=` on remove(). SystemExit: nothing left at the end; no parts list for parts_list_at_end.
3. Serve the kit (`/usr/bin/python3 tools/serve.py "LAC Build Instructions" 8793`, in the background from the shell) and open
   `http://localhost:8793/player.html?steps=steps-deconstruction.json`. Look at each step as it opens, half-way (`_dev.show('Step 12c',
   0.5)`) and at its end, at 1440 x 900 and in a narrow LMS-size window (760 x 720), with each later arrow while it is due.
4. The run-through: `(0, eval)(await fetch('js/runthrough.js').then(r => r.text())); _dev.freeze(); _runthrough()` on that page. For a
   take-apart it also checks that a part in `leaving` was on screen before, is gone after and never comes back, slides solid and fades
   on time forwards and backwards, and that `staged_arrows` show in turn (runthrough.js 41-115). Run the Full Build's again too if the
   player changed.
5. The wires: `.venv.nosync/bin/python tools/motioncheck.py "LAC Build Instructions" --steps steps-deconstruction.json` (every view whose
   wires change or whose wired parts move; `--moments 39` for steps of several beats; loads the CAD: heavy) and
   `.venv.nosync/bin/python tools/wirecheck.py "LAC Build Instructions" steps-deconstruction.json` (at rest). A walk-back replays the
   Full Build's own blends backwards, so a clash it shows that the Full Build's own step also has (mirrored in time) is not new (the
   PMG's README records exactly that); a leaving lead is not in the done view's wires and is not checked. `reappear` views are skipped.
6. In later rounds: keep a copy of steps-deconstruction.json before an edit and diff every view's camera after (memory: keep step
   cameras).
7. Publish for Lee only to the test preview (`python3 tools/publish.py lcd-alarm-clock-deconstruction --to "share/Test guides preview"`,
   served on 8799), once guides.json has the entries; never live without Lee.

---------------------------------------------------------------------------------------------------------------------------------

## 10. What the API cannot do, and what the others did instead

| the published LAC does | our API | what to do (precedent) |
|---|---|---|
| refits washer, nut, knob for storage (16 - 18) | `place()` refused in a take-apart; Lee: nothing refitted | leave out; a `note()` card if wanted |
| cross-fades a panel or module between posed copies (4c, 5c, 6c, 8c, 27c) | moves are slides; `lift(..., reappear=True)` fades out and in instead | slide (MRA, LSM); fade where a slide cannot be clean (PMG Step 8) |
| a routed wire cross-fades to a loose wire beside the base, then fades (12 wires) | no loose-wire swap; a leaving lead fades with its ends | both ends pulled up together (PMG, LSM); or a zero-length way: a fade in place |
| turns the scene's up axis to -X for F1's and F4's runs | `flip=True` only (upside down) | the Full Build's upright pose as a real step (F1 at BUILD), or a view by hand |
| an arrow per stage while a lead changes shape stage by stage | `then=` refused with `wire_via=` | one arrow (`stage=`), or the generator change in 3.4 |
| the build's own inset pictures | take-off `inset=` has no `image=` | a 3D close-up (target / dir / radius / mark(s) / ghost) |
| re-uses ride-only moves (F9, F7s, switch, knob ...) | no record: no default way | hand ways from steps.json carry entries (sections 3 - 6) |
| a camera per published step | the Full Build's camera of the step undone, or by hand | `camera_of()`; published cameras converted to ours: `docs/research/lsm/decon/study_published.md` |

Nothing here was run: the code fragments follow the four working scripts and the generator as read, and each needs its run, its log and
the browser checks of section 9.
