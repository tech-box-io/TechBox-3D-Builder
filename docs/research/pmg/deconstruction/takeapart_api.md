# The take-apart machinery, for the PMG deconstruction

Read on 21 Oct 2026 from `tools/stepgen.py` (2356 lines), `player/js/player.js` (1332), `player/js/runthrough.js`, `tools/motioncheck.py`,
`tools/publish.py`, `guides.json`, the MRA's and RCC's `deconstruction.py`, and the PMG's `guide.py` / `steps.json` (51 steps, 99 views).
Line numbers are those files as they stand at commit af553a6 plus the working tree. Nothing was run but small JSON reads.

## 0. How it fits together

- `take_apart()` (stepgen 828-901) reads the Full Build's steps file, not its guide.py. It records:
  - `came`: for every Full Build `hover` view with `moving` (and no `wiggle`), one record per moving part: its way in (`paths[i]` or
    `path`), `stops`, `camera`, `group`, `offsets`, `stationary`, `wires` (the hover view's routes), `wire_via` (the done view's), and
    `rode` (the part's carry entry in the view before). See 846-866. **A step that moved parts only by `ride=` (the PMG's Steps 1-26, 42,
    44, 46) has `moving == []` and leaves no record.** So the Nano, every jumper cap, the USB cable's ends, and the rides of Steps 42/44/46
    have no `came` record. Only Steps 27-41, 43, 45, 47, 48 are on record (the case parts, the keys, the buttons (32, 33), the module
    (43), the display (45), the matrix (47), H14 (48)).
  - the state as the Full Build ends (867-899): `placed`, `riding` (from the Completed View's `carry`), `resting` (moved offsets not
    carried), `wire_state` (route per lead).
  - one step dict `{'kind': 'begin', visible, rest, riding, wires}` (900), a snapshot.
- `remove()` / `unplug()` / `lift()` all go to `_takeoff()` (949-1188), which appends one dict `{'kind': 'takeoff', how, ids, movers,
  leave, ways, stops, ride_after, wires_after, wire_via, lead_off, units, arrows, eye, labels, camera, view_dir, frame, look_from, flip,
  inset, alone, wires_here, keep_camera, arrow_scale, arrow_style, own_frame?}` (1159-1165) and updates `self.placed / riding / resting /
  parked / wire_state` (1166-1185) for the checks of the steps after.
- **`build()` does not read `g.riding` / `g.resting`.** It replays the steps: `begin` (1692-1700) loads the snapshot into its own
  `visible / parked / riding / wires`, then each `takeoff` dict is replayed (1713-1823) from its `movers`, `ways`, `leave`, `ride_after`,
  `lead_off`, `wires_after`. Any new state change must therefore be written into the step dict and replayed in build(); changing
  `g.riding` from the script fixes only `_takeoff`'s checks (see 2).
- Each takeoff step makes two views: `Step N` (`kind: 'hover'`, 1781-1784: parts where they are, `moving: []`, arrows, eyes, labels,
  inset) and `Step Nc` (`kind: 'done'`, 1805-1810: `moving = movers`, `paths` = the ways, `path_stops`, `carry`, `leaving`,
  `leaving_wires`, `wire_via`, `away: True`). Both get `common` (1779-1780): caption, camera, `isolated` if `alone=`.

## 1. `reappear` on a takeoff step

**Not today.** `_takeoff` has no `reappear` parameter (949-952), and `lift(..., **how)` forwards everything, so `lift(..., reappear=True)`
raises `TypeError: _takeoff() got an unexpected keyword argument 'reappear'`. The view dicts of a takeoff never carry `reappear`.

**The player is already keyed on view kinds that takeoff views have.** player.js 842:

    const rv = forward && from.kind === 'hover' && to.kind === 'done' && to.reappear ? to
             : backward && from.kind === 'done' && to.kind === 'hover' && from.reappear ? from : null;

A takeoff's views are `hover` -> `done`, so a `reappear: true` on its done view is enough. Walking through go() for a lift:
- forward: 770-771 sets `ways` from `to.paths`; `fade` (818-830) stays null because a lift has no `leaving`; then 843-849 collect
  `parts` (every id whose start and end offsets differ: the movers *and their riders*, as carry composes them into `offsets`) and `wires`
  (route number changed, or an end among `parts`), and set `anim.dur = anim.moveDur = 1600`.
- stepAnimation 861-863: `km = e = 0` for the first 800 ms, `1` after, so `alongPath(way, 0|1)` gives the way's two ends (in-between
  stops and `via`s are not played), riders follow (872-882; `paced()` also returns 0 or 1), and `wire_via` stages are skipped; 894-897
  fade the parts and wires out, then in. 919-922 clear the fades.
- backward from the done view: 772-787 (the `away` branch) builds reversed ways and `wireVia`; rv (from.reappear) then overrides the
  timing the same way. Fine.
- motioncheck.py 148 skips `done` views with `reappear` (it would otherwise check a motion that is not played). runthrough.js has no
  `reappear` logic and needs none (its mid-motion checks are only for `leaving`). publish.py strips only `review` / `text_key` (61), so
  `reappear` is published.

**Code needed** (none in player.js for it to work):

1. stepgen.py `_takeoff` signature (949-952): add `reappear=False`.
2. Refuse it where it does not mean anything (after 959):
   `if reappear and how == 'remove': raise ValueError(f'remove({caption[:30]!r}): reappear= is for lift() / unplug(): parts taken off fade out anyway')`
   (with `leaving`, `anim.fade` and rv would both drive the same parts: they would fade out, fade back in at the end of their way, and then
   vanish at k = 1, 920-921). Optionally also refuse `reappear` with `in_turn` (its waits are not played).
3. The step dict (1159-1165): `**({'reappear': True} if reappear else {})`.
4. build(), takeoff branch, `common` (1779-1780): `**({'reappear': True} if s.get('reappear') else {})`, so both views carry it, as
   place()'s do (1895-1896; the player reads it on the done view only).
5. lift()'s docstring (936-946) and remove()'s option list (903-926), and CLAUDE.md's takeoff paragraph.

One optional player fix, only reachable with a takeoff: a takeoff's done view has `away: true`, so go() treats Next/Prev half-way through
it as a turn-around (718-719) and starts the reverse from `dur - elapsed`, but `dur` there is still the pre-rv value (`STEP_MS * legs`,
821), while rv then sets `anim.dur = 1600`. Mid-fade reversal therefore pops (the part jumps to full opacity). Fix inside the rv block
(after 848): `if (turnAround) anim.t0 = performance.now() - Math.max(0, anim.dur - elapsed);`. (The Full Build's Step 42 never turns
around: its views have no `away`.)

A **pure fade-out removal** (no slide) already works without reappear: `remove(caption, ids, paths={i: [current pose of i]})` (ZERO for a
part in its seat). The way has zero length, so `awayTiming` (684-703) puts `restAt = 0` and the fade at 0: the parts fade where they are
over 800 ms. `_arrow_out` returns None for a reach under 1 mm (1404-1405), so give `eye=`.

## 2. Pulling a device off the caps of its jumper wires

PMG facts (steps.json, Completed View): every jumper lead's route has `a` = the cap on the device's pin, riding on the device
(`NAUO76/83/84/85`, `NAUO79` display, `NAUO81` matrix), and `b` = the cap on the module's pin, riding on the module (`NAUO78`); the 23
things riding on the module are its 21 caps, the Nano (`NANO`) and the USB Mini-B end (`NAUO282`); the USB A end (`NAUO283`) rides on H1
(`NAUO63`) at pose ZERO. Every carry pose is ZERO at the end.

**Today `remove(MATRIX)` is refused**: `leave = ids + riders(ids)` (971) takes the matrix's five caps along, then the lead check
(1100-1112) finds each matrix lead with its `a` end leaving and its `b` end (a module cap) staying:
`ValueError: remove('...'): the lead dot matrix display VCC would be left on NAUO116 with nothing at its other end: unplug it first,
take both its ends off together, or say wires={'dot matrix display VCC': None}`.
`wires={w: None}` only makes the leads vanish at once (no fade: they are not in `leaving_wires`) and leaves the module's caps bare: not
what the published guide shows. There is no option that keeps a rider behind.

Workarounds with today's API, both poor:
- an extra step first, `lift('...', caps_on_matrix, paths={c: [where(c)] for c in caps})`: the caps stop riding on the matrix (the first
  rests, the others ride on it, 1148-1152), then `remove(MATRIX)` leaves only the matrix and the leads stay. Costs a Step N / Nc pair in
  which nothing moves.
- changing `g.riding` in the script: `_takeoff`'s checks pass, but build() still has the caps riding on the matrix (from `begin`), so in
  Step Nc they ride out with it and stay visible where its way ends, then jump back to their seats in the next step. Do not.

**Smallest addition, proposed: `let_go=[ids]` on remove() and lift()** ("these riders stay where they are"):

stepgen `_takeoff` (signature 949-952: `let_go=()`), before `leave` is computed (970-971):

    let_go = list(dict.fromkeys(let_go or ()))
    bad = [i for i in let_go if i not in riders(ids)]
    if bad:
        raise ValueError(f'{how}({caption[:30]!r}): let_go= names parts that do not ride on what moves: {bad}')
    kept = set(let_go) | set(riders(let_go))                  # (what rides on them stays with them)
    leave = [i for i in ids + riders(ids) if i not in kept] if how == 'remove' else []
    held = {i: now(i) for i in let_go}                        # (after now() is defined, 977; before any state changes)

`staying` (982) then includes them (it is computed from `leave`). Step dict (1159): `let_go=let_go`. State (after 1171):

    for i in let_go:
        self.riding.pop(i, None); self.resting[i] = held[i]; self.parked.add(i)

build(), at the top of the takeoff branch (before 1714), so that **both** views show them resting (no `carry` entry on either view):

    if s.get('let_go'):
        held, _ = with_riders({i: p for i, p in parked.items() if i in visible}, visible)
        for i in s['let_go']:
            riding.pop(i, None)
            parked[i] = held.get(i)

No player change: a part with no carry entry and the same offsets in both views stays put (stepAnimation 866, `mixPose(start, end)`
with start == end), forwards and backwards. (If build() popped the riding only between the two views instead, Prev would blend the cap
from its resting pose to the returning matrix, 880, and it would visibly swing.) The leads keep their routes; their ends are the caps, which
do not move. The same `let_go` on lift() lets a device be lifted off its caps' pins while they stay.

An alternative of the same size: `g.rest_here(ids)`, a step-less declaration like `put_away()` (kind `'rest_here'`, handled in build()
next to `put_away` at 1681, before `n += 1` at 1703, with the same three lines as above). `let_go=` reads better in the script and keeps
the change in the step it belongs to.

Things to know when the device has gone: its caps rest where they were, in the air at its pins' places (as Cadasio shows rigid wires);
the later `remove()` of those caps with the module's caps takes the leads with them (`lead_off`, faded). Those caps have no `came` record
and are off their seats, so they are "computed" (see 8: WARNING "not in its seat") unless `path=` / `paths=` / `direction=` + `hover=`
is given.

## 3. Hiding a group for a run of steps: `alone=`

- `alone=[ids]` is per step (972-975): it must include every part the step moves (ValueError), and `_takeoff` adds what rides on its
  parts at that moment (`riders(alone)`, transitively). build() shows only `shown = [i in visible if i in alone]` (1714) on both views.
- Leads: both views draw `wires_in(..., shown)` (1648-1655, 1782, 1805): a lead is drawn only if each of its non-None ends is shown. So a
  lead to a hidden part is hidden; a lead whose two caps are both shown (riders of shown parts) is drawn. `wires_here={id: route}` draws
  leads differently on that step only (they are merged over `wires` for its two views and dropped after).
- Both views get `isolated: true` (1780). Hidden parts keep their state in build() (`visible`, `parked`, `riding` untouched), so the next
  step without `alone=` shows them **where they were**. The player: `if (from.isolated && !to.isolated) for (id of to.visible)
  start[id] = end[id]` (803) and `anim.from = null` (835): the parts are simply there (a cut, no glide, no wire blending), while the camera
  swings (836) and a turned-over model turns (834). Into an isolated view, parts glide as usual and the hidden ones just disappear
  (`stage.setVisible(to.visible)`, 757).
- A Full Build camera taken over for a step made in a sub-assembly view logs a NOTE when `alone` is not given (1144-1145).
- **Nothing like a reversible put_away.** `put_away(ids)` (1200-1217) takes the parts, their riders and every lead touching them off for
  good (stepgen `wire_state` -> None; build() pops them, 1681-1691; the next view gets `cut`), and nothing can bring them back in a
  take-apart guide (place(), seat() and rest() raise `ValueError` when `self.taken`, 1308-1309, 1546-1547, 1563-1564). The only way to
  hide a group for several steps and show it again is to repeat `alone=` on each of those steps (a list in the script, as the MRA's
  `without()` helper). There is no `hide=` on takeoff steps.

## 4. `flip=` in takeoff steps; a turned-over run

- The camera of a takeoff step (1140-1147): if no `new_camera` / `view_dir` / `frame` / `look_from` and every mover has a `came` record
  with a camera, it is a deep copy of the camera of the **latest** Full Build step among them (`max(index)`), as stored in the Full Build's
  steps.json: a turned-over one keeps `flip: true` and its framing. If the step says `flip=True` and that camera is not turned over, it
  becomes `look_from=camera['dir']` and `choose_view(..., flip=True)` picks the nearest lower diagonal (543-617, elevation -35).
  `keep_camera=True` copies the step before's camera, turned over or not (1723).
- Otherwise (`path=` / `paths=` / `direction=` by hand, a computed straight pull, or a part with no record) the camera is chosen by
  `choose_view(..., flip=s['flip'])` (1724-1725) with `flip` as the step gives it (default False). **Inside a turned-over run a step whose
  way is by hand must say `flip=True`**, or the model turns upright for it. (`choose_view` keeps the previous camera only on the same side,
  593-599.)
- After all views are made, build() redoes the runs over the deconstruction's own views (2029-2073): consecutive turned-over views (no
  card between) share one `pivot` (the first view's target) and `flip_axis` (the level part of its dir); a stretch of them with the same
  `dir` gets one framing (the smallest sphere round theirs), split by `own_frame` (accepted by _takeoff, 952, 1165). The player turns the
  model, not the camera (`stage.worldFor(to.camera)`, 832-838).
- **Turning back upright** happens by itself at the first step whose camera is not turned over: a Full Build camera of an upright step
  (the PMG's H8, Step 35, and H4, Step 29), or `new_camera=True` / `view_dir=` / `look_from=` without `flip`. The player turns the model
  back as the camera moves (834, 864). Say so in the caption ("Turn the case the right way up ...", as the RCC's line 105).
- The PMG Full Build: Steps 30-34 are turned over (H5, H6, blue button, three buttons, H7), all with pivot [529, 882, 1290] and
  flip_axis [-0.9701, 0, -0.2425]; dirs: 30, 31, 34 = [-0.8, -0.5657, -0.2] (radius 118), 32, 33 = [0.0175, -0.6364, -0.7712] (target
  [582, 905, 1300], radius 108). Taken off in reverse (H7 by Step 34's camera, the buttons by Step 33's, H6 by 31's, H5 by 30's), they
  are taken over as they are; Step 35 (H8) and Step 29 (H4) are upright.
- The Completed View is never turned over: it takes the last step's dir unless that one is turned over, then the hero's (2025).

## 5. lift() walking back two Full Build steps at once (the matrix: Steps 47 and 46)

What the Full Build did: Step 46 is a ride (`moving: []`, `ride_beats: true`): the matrix, riding on H1, goes from its bench pose through
two in-between places to `MATRIX_HELD` (46c `carry[NAUO81]` = pose HELD, `via` = [UP, OVER]); its five leads through two in-between
routes (46c `wire_via`, 2 each) to the HELD routes; the USB cable changes once to `usb_outside()` (46c `wires_done`, no stages). Step 47
moves the matrix `path = [HELD, HALF, ZERO]` (three stops: 2 beats), its leads through one in-between route (47c `wire_via`, 1 each).
H1 is in its seat, so the poses of a ride on H1 are absolute poses.

`came` has only Step 47 for the matrix, so a plain `lift(caption, [MATRIX])` walks back Step 47 alone (to HELD, by Step 47's camera)
and **does not change the leads**: for remove() / lift(), `after = wires or {}` (1086); only unplug() fills the routes from the record
(1090-1096). The leads would keep their seated shapes, stretched between the moving caps and the module's.

One step for both (5 beats), from the Full Build's own record (the MRA's `walked_back()` idea):

    M46, M46c, M47, M47c = (VIEW[n] for n in ('Step 46', 'Step 46c', 'Step 47', 'Step 47c'))
    bench = M46['carry'][MATRIX]['pose']; up, over = M46c['carry'][MATRIX]['via']; held = M46c['carry'][MATRIX]['pose']
    half = M47['path'][1]
    MW = [w for w in M47['wires'] if w.startswith('dot matrix display ')]
    g.lift('...', [MATRIX], path=[half, held, over, up, bench],                    # (5 stops after where it is: a beat each)
           wire_via={w: [ROUTES[M47c['wire_via'][w][0]], ROUTES[M47['wires'][w]],
                         *[ROUTES[n] for n in M46c['wire_via'][w][::-1]]] for w in MW},   # (half, held, over, up)
           wires={**{w: ROUTES[M46['wires'][w]] for w in MW},                      # (the bench shapes: the last stage)
                  'usb cable': ROUTES[M46['wires']['usb cable']]},                 # (back inside, as before Step 46)
           eye=[MATRIX], view_dir=M46['camera']['dir'], frame=(M46['camera']['target'], M46['camera']['radius']))

How it plays and what keeps pace:
- `path=` poses are **absolute** (pose of the part relative to its own seat, in assembly space), the poses *after* where it is now: the
  current pose is put first by `_takeoff` (991). A part riding on something that has moved needs `compose(carrier_now, rel, g._pivot(i))`
  (the MRA's `walked_back(carrier_pose=)`). `path=` applies to every mover without its own `paths=` entry (988).
- Each pose not wrapped in `via()` is a stop: one beat (800 ms, `STEP_MS`). `via()` poses are passed through within the beat, split by
  distance (1057-1059 -> `path_stops` on the done view, 1798, 1807; player `alongPath` 670-678). The step lasts `STEP_MS * legs`, legs =
  the most stops - 1 over the movers (814).
- **Riders** (the five caps on the matrix) keep riding: build() leaves them in `riding`, so the done view's `carry` has them (1720) and
  the player composes each onto the carrier's live pose (878: same carrier and pose in both views). Leads are tied to the caps, so their
  `a` ends follow; the `b` ends stay on the module's caps.
- **Leads keep pace stop by stop** only if `max(len(wire_via[w])) + 1 == beats`: player 870-871 `paced(n)` is stepwise only when `n ===
  beats`; otherwise the whole change runs smoothly (`e`) over the whole move. All leads of a view share one `we` (884-886), so a lead
  without stages (the USB cable) blends over the whole step in five eased pulses, as it did in the Full Build's Step 46. Nothing warns of a
  mismatch: count the stages (here 4 + the final = 5 legs = 5 stops).
- `wire_via` needs each lead's last route in `wires=` (ValueError, 1087-1089). Prev plays the stages backwards (787).
- `ride_beats` is not a takeoff option (TypeError). Its takeoff equivalent is simply a mover's stops. The other riding-through-places
  case is a plug walked back on its lead with `ride_on=` its carrier (1799-1804): only when it rides on the same carrier before and
  after, that carrier does not move, and its way has at most 2 stops (in-between poses as `via()`): the poses become the done view's
  `carry[i].via` and the plug moves through them within one beat, its lead's stages evenly with it (the MRA's claw / elbow / shoulder
  plugs).
- After a lift, a single mover rests at its last pose. With several movers, **the others ride on the first from then on** (1148-1152),
  or all on `ride_on=` if that part is on screen and not moving. Consequence: a later `remove()` of the first takes all the others (its
  riders) with it, and their leads to the module are refused. For the PMG, lift the devices one by one, or give `ride_on=MODULE` (it is
  there to the end), never `ride_on=H1` (H1 is taken off before the bench steps).
- Limits: `in_turn=` with any lead changing route or any `wire_via` is refused (1097-1099); a lead's stages are not checked against the
  stops; the hand-path camera is not the Full Build's (give `view_dir=` / `frame=`: the MRA's `camera_of()`); the order check (1042-1056)
  runs only on Full Build ways (not on hand paths) and only on ways without turns.

PMG notes for the lifts:
- The USB A end (`NAUO283`) rides on H1. `remove(H1)` would take it along, and the USB cable's other end (`NAUO282`, on the module) stays:
  ValueError (1111). Lift it with the module (e.g. `lift(..., [MODULE, USB_A], paths={USB_A: [Step 42's carry pose of it]})`: it then
  rides on the module, 1152) before H1 goes.
- The module: `came` = Step 43 only (`[0, 102.3, 0.2]` -> ZERO); Step 42 (a ride with `reappear`) is not on record. Back to the bench:
  `lift([MODULE, USB_A], paths={MODULE: [held, bench], USB_A: [Step 42 hover pose]}, reappear=True, wires=<Step 42's hover routes>)`
  once 1 is implemented, or two steps (Step 43 walked back, then the fade). Step 42's opening routes (`VIEW['Step 42']['wires']`) were
  drawn for exactly the state the reverse order gives: display and matrix on the bench, buttons in the case.
- The buttons: `came` = Steps 32 (blue) and 33 (the other three), whose ways start at their bench poses (`button_way`: bench, clear,
  lifted, under the pocket, in). A plain `lift(BUTTONS)` walks all four back to the bench (4 beats) by Step 33's turned-over camera,
  but needs `wires=` (VIEW['Step 32']['wires'] for the buttons' leads: the bench shapes). They must be lifted, not removed: their leads
  go to the module.
- remove() of a part off its seat with no hand way: WARNING + Review note "not in its seat" (1027-1032). Everything on the bench is off
  its seat (resting or riding on the module), so every bench step needs `path=` / `paths=` / `direction=` + `hover=`. Directions there
  are in assembly space; the module lies turned on the bench (`r` 120 degrees about [1, 1, 1]), so "up off its pins" is its pin axis
  turned by its bench pose (`turn_dir(pose, axis)`). The Nano's way off: `compose(where(MODULE), VIEW['Step 1']['carry'][NANO]['pose'],
  g._pivot(NANO))` (its pose over the module in Step 1, NANO_UP, relative to the module).

## 6. remove() of a group of like parts (four H9, four buttons)

Units (1113-1135): with `arrows=None` (default) and not `unplug`, movers are grouped by how they came: `('build', Full Build view index)`,
`('out',)` for a computed pull, `('own', i)` for a part with its own `paths=` entry, `('hand',)` for the rest. A group of exactly two with
the same name (`self.names`), not the two ends of one lead and whose boxes do not touch, is split into two units (an arrow each). One
arrow per unit; more than 2 -> `NOTE: <caption>: N arrows (the published take-aparts show 2 at most: rulebook section 11)` (1134-1135).
`units=[[ids], ...]` by hand replaces this (ValueError if it names a part that does not move, 1115-1117).

- The four keys: Step 36 brought one (`NAUO72`), Step 37 three -> **2 units, 2 arrows** by default; `units=[KEYS]` for one; `units=[[k]
  for k in KEYS]` for four (NOTE). The four buttons: Steps 32 (blue) + 33 (three) -> 2 units likewise.
- An arrow (`_arrow_out`, 1377-1455): along the longest stage of the part's way (`stage`, 1737-1744; `arrow_style={id: dict(stage=k)}`
  for stage k, 0 the first: for the buttons the press out of the pocket is stage 0, the 110 mm lift is longer), sized by `_arrow_dims`
  (1371-1375: length = clip(0.25 reach + 0.2 size, 15, 40) mm, width = clip(0.1 length, 1.6, 3.2)), times `arrow_scale`. A unit of parts
  spread apart (all pairs more than 1 mm apart) gets its arrow on the part nearest their middle (1397-1402). Moved on along its way, 4 mm
  at a time, until the camera sees it (1416-1449). One pointing within about 37 degrees of the camera axis (|d . dir| > 0.8) becomes an
  eye on `unit[0]` instead (1407-1408, 1762-1763), unless `keep=True`. A way shorter than 1 mm gives no arrow (1404-1405).
- `eye=` is a list of ids or `dict(anchor=[x, y, z])`; each id gets an eye whose anchor is found where this step's camera sees the part
  (`label_anchor`, 1767-1769). Several ids -> several eyes. Default: none for remove() and lift(), one per plug for unplug() (1136-1137).
  `arrows=[]` means no arrows at all (then give `eye=`): the MRA's eight breadboard wires, `arrows=[], eye=[one cap at each end]`.
- Names: the deconstruction scripts pass `names=dict(FULL['names'])`, which are the Full Build's **hover** names (stepgen 2147): the PMG's
  buttons are "Black / Yellow / White / Blue Push Button", so they never count as "two of a kind"; the keys are all "H9".

## 7. Title page, Completed View, card, parts list, publishing

- Title page: the Full Build's first view as it is (visible, offsets, carry, wires, camera) unless the Guide is given `start_view=`
  (1959-1962, 2018-2019). Its subtitle is the guide's `part` ("Deconstruction").
- Completed View (1955-1964, 2017-2025): what is still `visible` after the last step, framed by `_fit(end_shown, end_last)` (the box round
  it), looking from the last step's camera dir, or the hero's (from `hero_azimuth`, elevation 32) if that one is turned over. `SystemExit`
  if nothing is left ("a deconstruction ends on what is left assembled ..."). `Guide(end_view=...)` overrides it. For the PMG pass
  `hero_azimuth=315` as its guide.py does (the default 225 is used only in that fallback). Ending on the bare I/O module, lying turned on
  the bench, frames the module there.
- `take_apart(parts_list_at_end=True)` appends deep copies of the Full Build's parts list cards after the Completed View (2140-2141;
  SystemExit if it has none, 888-889). The PMG's are "Parts List" and "Parts List (Cont.)". `Guide(parts_list=fn)` would put pages after
  the title page instead (published practice: none).
- Constructor: `Guide(HERE, title='Piano Memory Game (PMG)', part='Deconstruction', names=dict(FULL['names']),
  steps_file='steps-deconstruction.json', source='pmg-guide.glb', hover_names=..., copyright_line=...)`. **`source=` is required**: the
  default is `'mra.glb'` (625). `steps_file` must match `steps-<words>.json` and must not be a Part's file in chapters.json (667-671; the
  PMG has no chapters.json). The run writes only `steps-deconstruction.json` (no parts.json, 2155-2157); its wording file is
  `step-text-deconstruction.json` (93-96). `_sync_model` (2342-2356) rebuilds model.glb (heavy, ~2 GB) only if the parts the kit's steps
  files show change: the deconstruction shows no new part, so it should not.
- Card: `_dev.card()` on `player.html?steps=steps-deconstruction.json` copies the Full Build's `cards/steps.webp` (and its `.json`) to
  `cards/steps-deconstruction.webp` (runthrough.js 103-116: it refuses if the Full Build's card is missing or drawn from another model).
  The PMG has `cards/steps.webp`.
- guides.json: add, after `piano-memory-game-full-build`, `"piano-memory-game-deconstruction": {"kit": "piano-memory-game", "steps":
  "steps-deconstruction.json", "label": "Deconstruction", "script": "deconstruction.py"}` (the MRA's and RCC's entries are the model).
- publish.py: `--kit piano-memory-game` publishes each changed guide; warns if the steps file is older than its script (483-485), if the
  card is missing or stale (486-491), if the Full Build changed since the take-apart (`taken_from` stamp, 361-370, also listed for the
  whole kit at 699 / 752), and that Review notes are left out (495-497); refuses steps whose model stamp differs from model.glb (465-467).
  Run deconstruction.py again after every Full Build change. Publishing for review goes to `--to "share/Test guides preview"` (8799);
  never live without Lee.

## 8. Every message the takeoff code can give

Errors (the run stops):
| where | message (abridged) | meaning |
|---|---|---|
| `Guide.__init__` 667-668 | `steps_file: steps.json, or steps-<lower-case words joined by hyphens>.json` | file name pattern |
| 670-671 | `steps_file=... is a Part of the Full Build (chapters.json)` | name taken by a Part |
| take_apart 837-838 | `take_apart(): in a guide of its own (...), not in the Full Build` | called with steps.json |
| 839-840 | `take_apart(): first, before any step` | called twice or late |
| 844-845 SystemExit | `take_apart(): <full> has no step that shows the model` | empty Full Build |
| 888-889 SystemExit | `take_apart(parts_list_at_end=True): <full> has no parts list to show` | |
| place / rest / seat 1308, 1546, 1563 | `...: a deconstruction guide takes parts off ...; it puts nothing on` | no putting on in a take-apart |
| chapter / note(only_in) / in_part 779-826 | Part-only features | not in a take-apart |
| _takeoff 953-954 | `<how>(): only in a deconstruction guide, after take_apart()` | |
| 957-959 | `<how>('...'): [ids] not on screen (taken off already, or never there)` | id gone (or put away) |
| 972-973 | `<how>(): alone= must include the parts it moves` | |
| 1022-1023 | `unplug(): the Full Build never plugged <id> in (or it is not in its socket now): remove() or lift() it, or give path=` | unplug needs a `came` record and the plug in its seat (or riding at its seat) |
| 1063-1064 | `in_turn= must list each part that moves once (...)` | in_turn must partition the movers |
| 1087-1089 | `wire_via for <w> needs its last route in wires=` | |
| 1097-1099 | `in_turn= where a lead changes route: ...` | a lead's stages cannot keep pace with one group |
| 1110-1112 | `the lead <w> would be left on <id> with nothing at its other end: unplug it first, take both its ends off together, or say wires={w: None}` | remove() of one end of a lead (see 2) |
| 1115-1117 | `units= names parts that do not move: [...]` | |
| build 2020-2021 SystemExit | `a deconstruction ends on what is left assembled ...: this one takes everything off` | nothing left for the Completed View |
| _inset_image 1194-1195 SystemExit | `inset image '...' is not in the kit folder` | |
| (not raised, but crashes) | `arrow_style={i: dict(like=j)}` with j neither moving in the step nor ever moved in the Full Build -> KeyError in `dims_of` (1749); `stage=k` beyond the way's stages -> IndexError (1743) | |
| (proposed) | `TypeError ... unexpected keyword argument 'reappear'` / `'ride_beats'` / `'let_go'` today | options takeoff does not take |

WARNINGs (the step is made; most also add a Review note to the step):
| where | message | meaning |
|---|---|---|
| 1029-1032 (+ review) | `<caption>: <names> not in its seat: lifted straight up, unchecked (give direction= or path=)` | a computed pull for a part resting or riding off its seat: the collision test (made seated) cannot say; the way is straight up (+y) in assembly space |
| 1033-1035 (+ review) | `no straight way out was found in the CAD; the motion needs a check (<caption>)` | free_directions found none: pulled up |
| 1053-1056 (+ review) | `<caption>: the way out of <Full Build step> passes through a part still there` | the order differs from the build's reverse (tested only from the seat, ways without turns, and only when the Full Build's own stationary parts did not block it) |
| 1153-1158 (lift only) | `<caption>: <name> looks plugged into a part that is lifted, and stays behind: list it with them` | a seated part the Full Build moved in from riding (a plug) whose box touches (1 mm) a seated mover. In the PMG the electronics' seated boxes do not touch each other (cad-geometry.json), so no false alarms are expected |
| step text 1621, 1627 | caution changed since edited outside; wording for a step that is gone | step-text-deconstruction.json |

NOTEs (log only):
| where | message | meaning |
|---|---|---|
| 884-885 | `take_apart(): <full> has no plain Completed View; each part is taken as the last step that showed it had it` | the Full Build's end view is cut (posed); the PMG's is not |
| 1134-1135 | `<caption>: N arrows (the published take-aparts show 2 at most: rulebook section 11)` | more than 2 units |
| 1144-1145 | `<caption>: the Full Build put this on in a sub-assembly view (<step>); its camera frames that` | an `isolated` Full Build step's camera, used without `alone=` |
| build 1727-1734 | `<caption>: the Full Build's camera leaves out <names>, lying aside (new_camera=True, or alone=)` | a part off its seat lies more than 1.1 radius from the borrowed camera's target. Expect it in the PMG for case steps once the electronics are on the bench |

Log lines: `take_apart(): from steps.json as it ends (N parts, M leads)` (901); one line per step: caption, how, number of parts, the way
("the Full Build's way, reversed" / "by hand" / "pulled out along [x, y, z]" / "mixed"), arrows, leads that go with them (1186-1188).

Player checks (runthrough.js 41-49, 59-87): a part in `leaving` must have been on screen in the view before, be gone in its view, and
never show again; while it slides it must be moving and solid, half-way through its fade about half see-through, then gone; and the same
backwards. motioncheck.py checks the leads during each move (skips `reappear` done views).
