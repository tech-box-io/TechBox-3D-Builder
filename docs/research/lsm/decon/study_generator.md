# How tools/stepgen.py makes a deconstruction, and what that means for the LSM

Study for the LSM deconstruction (Lee, 21 Oct 2026). Read-only: nothing was run but light JSON reading. Line numbers are
tools/stepgen.py unless another file is named. Complete (21 Oct 2026).

## 0. Sources read
- tools/stepgen.py: take_apart 828-901, remove 903-927, unplug 929-934, lift 936-947, _takeoff 949-1188, put_away 1200-1217,
  _arrow_dims 1370-1375, _arrow_out 1377-1455, build() 1632-2164 (takeoff branch 1713-1823, title / end cameras 2017-2025,
  flip runs 2029-2073, parts pages 2140-2141), _sync_model 2342-2356.
- MRA Build Instructions Prototype/deconstruction.py (281 lines), RCC Build Instructions/deconstruction.py (138 lines).
- LSM Build Instructions/guide.py (826 lines), steps.json.

## 1. What take_apart() starts from (stepgen.py 828-901)

- Only in a guide of its own (`Guide(steps_file='steps-deconstruction.json')`, 837-838), as the first call (839-840).
- Reads the Full Build's steps.json as last written (841): never imports guide.py. **The LSM's guide.py calls `g.build()` at module
  level (guide.py:826): importing it from the deconstruction script would rewrite steps.json and parts.json.** Every pose and route
  the LSM deconstruction needs must come from steps.json (VIEW / ROUTES, as the MRA's and RCC's scripts do) or be copied as numbers.
- `came` (846-864): for every Full Build hover view with `moving` (and no wiggle), one record per moving part: the view index, name,
  the whole moving group, its way (its own `paths` entry, else the step's `path`), stops (`path_stops`/`stops`), camera, `isolated`,
  `stationary` (visible parts not moving, not carried, not offset), offsets, the step's hover wires (routes), the next done view's
  `wire_via`, and `rode` = the carry entry of that part in the view before (where it rode just before it was moved).
  **Parts brought in only by `ride=` (a carried part moved by a ride, not listed in `moving`) get no record.** `fits[-1]` (the latest
  record whose group is wholly leaving) is the one used, so a later "still" move of a part (a way of all-zero poses used to pace a
  ride) wins over its real way in.
- The state (867-893): every part of the Completed View (or, if it has none / is a cut, of the last view that showed it); `riding` =
  the Completed View's `carry`; `resting` = any part offset from its seat (none, for the LSM: every offset in its Completed View is
  zero); `wire_state` = the Completed View's leads, plus older leads whose ends are both still there (881-883).
- Title page: the Full Build's Start view, camera and all (1959-1962, 2017-2019) unless the deconstruction's Guide gets its own
  `start_view`.
- `parts_list_at_end=True` copies the Full Build's Parts List cards after the Completed View (887-889, 2140-2141).
- Logs `take_apart(): from steps.json as it ends (N parts, M leads)` (901); NOTE if there is no plain Completed View (884-885).

## 2. API cheat sheet

### 2.1 Guide(...) for a deconstruction
As the MRA's (deconstruction.py:102-105) and RCC's (54-58): `Guide(HERE, title=..., part='Deconstruction', names=dict(FULL['names']),
steps_file='steps-deconstruction.json', source=..., copyright_line=...)`.
- `source=` **must be 'lsm.glb'** for the LSM (Guide's default is 'mra.glb', 625; the RCC passes 'rcc.glb'). lsm.glb is 19 MB.
- `FULL['names']` are the Full Build's hover names (build() writes `names` with hover_names applied, 2147): for the LSM 'Yellow / Grey /
  Purple Breadboard Wire' for each wire's two caps, 'D9' (x2), 'D11' (x4), 'Push Button' (BUTTON, NUT, both pins), 'USB Cable' (both
  ends). The names drive default label text, the log and the "two of a kind" arrow rule (1129).
- `hero_azimuth=` defaults to 225; the LSM's Full Build uses 45 (guide.py:92). It matters only if the deconstruction's last step is
  turned over or has no camera: the Completed View then looks from `hero['dir']` (2025). Pass `hero_azimuth=45`.
- `review_notes=False` hides Review notes; the generator adds a Review note itself in some cases (2.6).
- No `parts_list=`, `part_of=`, `codes=` needed (the MRA passes none). build() still makes a parts list internally; it is not written
  for a deconstruction (parts.json only for steps.json, 2155-2157).

### 2.2 take_apart(full='steps.json', parts_list_at_end=False)  (828)
See section 1. The LSM has 2 Parts List cards ('Parts List', 'Parts List (Cont.)'), so `parts_list_at_end=True` works.

### 2.3 remove(caption, ids, **how) (903) / unplug(caption, ids, ride_on=None, **how) (929) / lift(caption, ids, to=None, ride_on=None, **how) (936)
All three go through `_takeoff` (949). Arguments (signature 949-952):

| argument | default | what it does |
|---|---|---|
| `ids` | - | parts that move. Must all be on screen (957-959). Duplicates dropped (956). |
| `path=[pose, ...]` | None | the way out by hand for every mover without its own `paths` entry: **absolute poses relative to the seat, after where it is now** (991). `via()` poses are passed through (1057-1059). |
| `paths={id: [pose, ...]}` | None | the same, per part (988). |
| `direction=[x,y,z]`, `hover=mm` | None | a straight pull for the movers with no hand way; `hover` default = `hover_distance` of those movers (994-997). |
| `to=` (lift only) | None | the end pose, or {id: pose}: a one-stage way (992-993). |
| `ride_on=` | None | unplug: an id or {plug: id}: what each plug rides on afterwards (1081). lift: **one id only** (1149; a dict silently falls to "ride on the first mover"). |
| `wires={id: route or None}` | None | lead routes as the step completes (Step Nc); None removes the lead (1792-1795). A lead listed here is exempt from the "one end left" refusal (1102). |
| `wire_via={id: [route, ...]}` | None | routes the lead passes through, one per stage; its last route must be in `wires=` (1086-1089). Written only for leads still on screen (1809). |
| `wires_here={id: route}` | None | how leads are drawn on this step's two views only (1782, 1805); not kept. A lead is drawn only if both its end parts are shown (wires_in, 1648-1655). |
| `arrows=` | None | None: one per unit (computed); `[]`: none; a list of dict(tail, head, normal, part, width?) in seated mm on `part`, drawn where that part is now (1770-1773). Any non-None value skips the computed units (1119). |
| `units=[[ids], ...]` | None | the arrows by hand: one per group; every id must be a mover (1114-1118). Works for unplug too (unplug computes no units of its own; this or hand `arrows=` gives it an arrow). |
| `eye=` | unplug: every mover; else [] (1136-1137) | ids or dict(id=, anchor=, side=...). Anchors found by `label_anchor` where missing (1767-1769). |
| `labels=` | () | ids (text = name) or dicts (id, text, anchor, side) (1139). Shown on Step N only. |
| `caution=`, `review=` | None | as place(). |
| `inset=dict(...)` | None | a close-up on **Step N**. Only `target` (required: KeyError without it), `dir` (default the camera's), `radius` (20), `hide`, and `mark`, `alt`, `caption`, `arrows` are passed (1774-1778). **`image`, `ghost`, `marks`, `side` are dropped.** `arrows=[ids]` puts those units' arrows in the close-up (MRA 265). |
| `view_dir=`, `frame=(target, radius)`, `look_from=`, `new_camera=True` | - | any of them: a camera chosen for this step (choose_view) instead of the Full Build's (1141, 1723-1725). |
| `keep_camera=True` | False | the previous takeoff step's camera exactly (1723). |
| `flip=True` | False | shown turned over. If the Full Build's camera is not turned over, its direction becomes `look_from` (1146-1147). **If the Full Build's camera is turned over, the step is shown turned over whatever `flip` says** (the camera is copied with `flip`), unless a camera is given by hand. |
| `own_frame=True` | False | only matters in a run of turned-over steps: this step keeps its own framing (2049-2058). |
| `alone=[ids]` | None | only these (and what rides on them) are shown; must include the movers (972-975); the views are `isolated` (1780). |
| `in_turn=[[ids], ...]` | None | groups leave one after another (padding each way with waits, 1060-1074). Must list every mover exactly once (1063-1064). **Refused when any lead changes route or has wire_via** (1097-1099). |
| `arrow_scale=k` | 1.0 | all arrows of the step x k (1758). |
| `arrow_style={id: dict(...)}` | None | for the unit containing id (1757): `scale`, `like=id2` (as big as id2's own arrow: its stage in this step, or its own Full Build way, 1745-1754), `at=[x,y,z]` (tail, assembly mm), `shift=[dx,dy,dz]`, `face=[x,y,z]`, `keep=True` (an arrow even end-on), `stage=k` (along stage k of its way, 0 first, 1737-1744). `at`/`shift`/`face` = placed by hand: not moved on to be seen (1415). |

### 2.4 How the way out is chosen (987-1041)
For each mover (a listed id that does not ride on another listed id, 970), in order:
1. `paths[id]` or `path` by hand (988-991);
2. lift with `to=` (992-993);
3. `direction=` (994-997);
4. otherwise the Full Build's record: `fits` = its records whose whole group is leaving now (1000; for unplug the last record even if
   not). Used if the part is in its seat and not riding, **or** rides at its seat (relative pose zero) on a part that is not moving
   (`in_seat_on`, 1001-1003). The way is the record's way reversed (1007), composed with the carrier's current pose if it rides
   (so a sub-assembly lifted off and taken apart in the hand keeps its parts' Full Build ways, MRA claw / RCC module). Stops are
   reversed (1019-1021). The camera is the record's; if the carrier has slid since, the camera is slid with it; if it has turned,
   no camera (choose_view) (1008-1018).
5. else, unplug: **ValueError** "the Full Build never plugged X in" (1022-1023);
6. else `computed`: pulled straight out together the first free axis (AXES order: up first, 51) found by the collision test against
   the seated parts that stay (1026-1041), `hover_distance` far. **A computed part that is riding or not in its seat is not tested:
   it goes straight up, the log says `WARNING: ... not in its seat: lifted straight up, unchecked`, and the step gets a yellow
   Review note** "Not in its seat, it is lifted straight up: the way out needs a check." (1029-1032). No free axis: WARNING + Review (1033-1036).

Order check (1043-1056): for each Full Build record used, if its way has no turn and starts at the seat, the generator tests whether
the reversed way is blocked by what stays (seated, non-riding parts, plus in_turn groups still to go) but was not blocked by the Full
Build's own `stationary`: then WARNING "the way out of Step N passes through a part still there" and a Review note. **Riding parts are
never in this test** (983), and nor are ways with a turn.

### 2.5 Riders, leads, units, eyes, camera
- **Riders go with their part**: `leave = ids + riders(ids)` for remove (961-971): everything riding on a leaving part, transitively.
  For unplug and lift nothing leaves; riders are carried along in the views by `with_riders` (1715, 1720).
- **Leads that go**: a lead with an end on a leaving part goes too if its other end also leaves or is None (resistor legs: `b=None`)
  (1100-1109). **A lead with one end leaving and the other staying is refused** (ValueError, 1110-1112) unless it is in `wires=`.
- **unplug's leads**: each lead ending on the plug takes the route it had on the Full Build's hover view of that step, and its
  `wire_via` reversed (1090-1096). The plug ends where the Full Build's way started and rides from then on on `ride_on`, or on what it
  rode on just before that Full Build step (`rode`), if that part is still there and not moving (1079-1085).
- **lift**: they stay on screen; movers after the first ride on the first, or all on `ride_on` (1148-1152). No automatic lead
  routes (give `wires=`/`wire_via=`). WARNING if a seated part that the Full Build plugged (a record with `rode`) overlaps a lifted
  part's box within 1 mm (1153-1158): "looks plugged into a part that is lifted, and stays behind".
- **Units / arrows** (1113-1135, only if `arrows is None` and not unplug): movers keyed by the Full Build record (same step = one
  unit), all computed ones together, each `paths` part alone, the rest (direction/path) together. A unit of exactly two parts with
  the same name, not the two ends of one lead, and whose boxes do not touch (0.5 mm) is split into two arrows (1129-1131). More than
  2 units: NOTE in the log (1134-1135).
- **The arrow** (_arrow_out 1377-1455, called at 1761): along the longest stage of the way (by pivot travel; `stage=` picks one) from
  the unit's pivot mean; a unit of parts all apart (1 mm) with none containing the mean starts on the one nearest the middle (1397-1402);
  no arrow if the travel < 1 mm (1404-1405); **end-on (|d . camera dir| > 0.8) becomes an eye on the unit's first part** unless `keep`
  (1407-1408, 1762-1763); length 15-40 mm = 0.25 x reach + 0.2 x size, thickness 1.6-3.2 = 0.1 x length (1371-1375); tail 2 mm outside
  the parts along d, then moved on 4 mm at a time (up to 12) until not hidden (1416-1449); face towards the camera.
- **Camera** (1140-1147, 1723-1726): the Full Build's camera of the latest record used, when every mover has one and no camera is given;
  else choose_view. NOTE if that record was in a sub-assembly view and `alone` is not given (1144-1145); NOTE if that camera leaves out
  a part lying aside (more than 1.1 radius from target) (1727-1734).
- **Views** (1781-1810): Step N = hover view, parts where they are, `moving: []`, arrows / eyes / labels / inset, `cut` after a
  put_away; Step Nc = done view, `moving` = movers, `paths` = their ways (rounded by pose_out: 0.1 mm), `path_stops` where some poses are
  via, `leaving` (ids that go), `leaving_wires` (routes of leads that go), `wire_via`, `away: true`; riding entries carry `via` for a plug
  that rides on the same part before and after with at most 2 stops (1799-1804).

### 2.6 put_away(ids) (1200-1217) and note()
- put_away: off the screen without a step, riders too, leads ending on them cleared; the next view is a cut (1690). Used after a
  sub-assembly is taken apart in the hand (MRA 121, 173, 185, 203, 219, 230, 242, 249, 254; RCC 87, 96, 112, 132).
- note(): a card as in a build (793). place(), rest() and seat() refuse in a deconstruction (1308-1309, 1546-1547, 1563-1564).

### 2.7 The end (2017-2025)
The Completed View shows what is left (SystemExit if nothing is, 2020-2021), framed on it, from the last step's camera direction unless
that step was turned over (then `hero['dir']`). For the LSM: pass hero_azimuth=45 (2.1).

### 2.8 Errors and log lines, all in one place
ValueError: take_apart in steps.json (838) or not first (839); X not on screen (957-959); alone without the movers (972-973); unplug
of a part never plugged (1022-1023); in_turn not listing the movers (1063-1064); wire_via without its last route in wires (1087-1089);
in_turn with a lead changing (1097-1099); a lead left with one end (1110-1112); units naming non-movers (1115-1117); place/rest/seat.
SystemExit: no model steps (844-845); no parts list pages (888-889); nothing left at the end (2020-2021). KeyError: an inset without
`target` (1777).
Log: per step "caption  how  N part(s), the Full Build's way, reversed | by hand | pulled out along [..] | mixed, k arrow(s), m lead(s)
with them" (1186-1188); WARNINGs: not in its seat (1031), no straight way (1035), way passes through a part still there (1056), plug left
behind on lift (1158); NOTEs: >2 arrows (1135), Full Build sub-assembly camera (1145), camera leaves out a part lying aside (1733),
no plain Completed View (885). Then step-text warnings (1621-1629) and the model sync: the deconstruction shows no new parts, so
`_sync_model` (2342-2356) does not rebuild model.glb.

## 3. Patterns the MRA and RCC scripts use (worked examples)

- Read the Full Build once: `FULL = json.loads(steps.json)`, `VIEW = {name: view}`, `ROUTES = FULL['routes']` (MRA 50-52, RCC 36-38).
- `camera_of(step, moved=None)` (MRA 55-60): a Full Build step's camera as `view_dir=` + `frame=(target, radius)`, its target slid by a
  sub-assembly's current shift. Used wherever a way is given by hand (the generator reuses the Full Build's camera by itself only
  when it uses the Full Build's way). RCC's `turned_camera` (42-46) does the same for a turned controller.
- `leads(step, prefix)` (MRA 63-65, RCC 49-51): the routes of a lead in a Full Build view, for `wires=` / `wire_via=`.
- `walked_back(step, plug, prefix, carrier_pose, pivot)` (MRA 68-81): a Full Build step that moved a plug only by a ride, walked back
  as `lift(..., path=[via..., last], ride_on=carrier, wire_via=..., wires=...)`. Its assert (76) needs one route per pose.
  `riding_back` (84-89), `full_way_back` (92-99) are the same for other cases.
- `where(i)` (MRA 108-113, RCC 61-66): where a part is now (composed through what it rides on); with `compose(pose, where(i), pivot)`
  a hand way is written relative to where the part is (RCC 73, 95, 131). **Hand ways are absolute poses (relative to the seat),
  not offsets from the current place.**
- A sub-assembly: `lift(...)` it the Full Build's way reversed (its parts then ride on the first id), take it apart with
  `remove(..., alone=[...])` (each part's Full Build way, composed with the lifted carrier), `keep_camera=True` for the run, then
  `put_away([what is left])` (MRA 153-173, 245-254; RCC 105-112, 117-132).
- Several of a set at once: `remove(caps, arrows=[], eye=[one per end])` (MRA 238-239: the eight breadboard wires, both caps of each,
  so every lead goes with them). A cable: `remove([plug, far_end], units=[[plug]], paths={far_end: [lifted a little]}, arrow_scale=2)`
  (MRA 125-126, RCC 71-77). Labels instead of eyes on unplugs (MRA 129-132). A screw then its part: `in_turn=` + `arrow_style={screw:
  dict(like=part)}` (MRA 176-184). Hidden parts: `inset=dict(target, dir, radius, arrows=[ids], alt)` + `arrow_style face=` (MRA 262-266).

## 4. The LSM: what take_apart() would inherit

State at the start (steps.json Completed View, checked 21 Oct 2026, 82 views, 68 routes):
- 97 parts on screen (33 + 64 stems); no part offset from its seat (so `resting` is empty).
- Riding (carry), all at their seats (pose zero): BUTTON and NUT on D2; J_WHITE_F, J_GREY_F, J_PURPLE_F and D10 on MATRIX; D11_A - D on D1.
  MATRIX itself does not ride (Step 32 moved it); BTN_RED_PIN / BTN_BLACK_PIN do not ride (Steps 21-22 moved them).
- 10 leads: '12k leg 1/2' and '330 leg 1/2' (a = the resistor, b = None: they go with it), 'wire white/grey/purple' (route nos 65-67,
  SEATED: a = J_*_M, b = J_*_F, b_from = length - 6, tail_from set), 'lead red/black' (42/43: BUTTON to its pin), 'usb cable' (41: USB_B
  to USB_A).
- Title page: the Full Build's (dir [0.5997, 0.5299, 0.5997], USB_A / USB_B hidden). Two parts list cards for parts_list_at_end.

What each part would do by default (a mirror of take_apart's `came` and `fits[-1]`, read from steps.json; the way is the Full
Build's reversed, by that step's camera):

| part | record used | default way out | verdict |
|---|---|---|---|
| STEM_01 | Step 39 | up 44 | fine |
| STEM_02 - 64 | Step 40 (group of 63) | up 44 | fine; all 64 in one step = 2 units, 2 arrows (one on STEM_01, one on the stem nearest the 63's middle): `units=[STEMS]` for one |
| D8 / D7 | Steps 38 / 37 | up 55 / 65 | fine |
| D11_A - D | none (ride= only, guide.py:803-814) | computed: straight up ~80 mm (posts 80 mm tall), **unchecked: WARNING + Review note** | give `direction=[0,1,0], hover=` or `path=` |
| D6 | Step 33 | up 64 | fine once the D11 posts are out (they go through its corner slots) |
| MATRIX | Step 32 | [seat, via P_HALF, P_HELD (-0.2, 56.6, -0.3)], one beat, Step 32's camera | fine as a lift; its riders (D10, the three sockets) go with it; **leads not re-routed** (give wires/wire_via); remove() refused while the pins are in the breadboard |
| D10 | none (rode in on the matrix, Step 31) | computed: straight up, **WARNING + Review**; up through the matrix if it is in the box | paths by hand |
| D9_A, D9_B | Step 29 (both) | up 65, 2 arrows (35 mm apart, same name) | fine once the matrix is off them |
| D5 | Step 28 | +X 42, **turned over** (Step 28's camera has flip) | fine; caption must say the box is turned over |
| D3 | Step 27 | swing 22 deg about the hinge, then 40 mm out along its tilt, turned over | fine; arrow along the slide (longest stage) unless `arrow_style={D3: dict(stage=0)}` |
| D4 | **Step 31** (records: 25, 26, 30, 31; 26, 30 and 31 are the still ways [ZERO]*5 / *3 that pace the matrix's rides) | **no motion, no arrow (travel < 1 mm, stepgen 1404), Step 31's camera** (the D10 framing) | `path=[[-8,0,0],[-8,65,0]]` (Step 25 reversed) and Step 25's camera by hand |
| D2 | Step 24 | +Z 57.1 (to D2_OUT) | fine as a lift (riders BUTTON, NUT go along); remove refused while the pins are plugged |
| BTN_RED_PIN / BTN_BLACK_PIN | Steps 21 / 22 (rode on BUTTON) | out to the pose laid back from the button **with D2 at D2_OUT**, then ride on BUTTON; leads -> routes 36 / 37 (drawn with D2 at D2_OUT) | right only after D2 is lifted out to D2_OUT; then unplug(both) works with no hand work (2 eyes) |
| USB_B | Step 23 | +Z 25 | fine; take USB_A with it (the lead) |
| USB_A | none (show=) | computed: free axis (likely up), ~45 mm | fine, but 2 arrows: `units=[[USB_B]]`, `paths={USB_A: [[0, 25, 0]]}` as MRA/RCC |
| NUT | Step 20 (group NUT + BUTTON, isolated) | used only if BUTTON leaves in the same step; else computed straight up, **WARNING + Review** | path by hand (Step 20's NUT poses reversed, shifted by D2_OUT) |
| BUTTON | **Step 20** (way [ZERO]*3, the still way that made Step 20 two beats) | **no motion** | path by hand: Step 19 reversed, +Z 100, shifted by D2_OUT |
| J_*_M | Steps 11 / 12 / 13 | up 30 | the way is right; **unplug's lead routes are Step 11-13's** (21, 25, 23: sockets held 15 mm off the matrix held upright at P_UP) - wrong anywhere later; remove refused unless the sockets go too |
| J_*_F | none (rode on via ride=, Steps 15-17) | **unplug: ValueError** (1022-1023); remove: computed straight up + WARNING + Review | by hand: their way off is along +Z off the pins (SOCKET_OFF [0,0,15] relative to the matrix, guide.py:224) |
| R330 / CAP / R12K / NANO | Steps 9 / 7 / 5 / 3 | up 30 / 29 / 32 / 35, legs go with the resistors | fine |
| BREADBOARD | Step 2 | up 49 | only if the guide ends on D1 alone (the published one ends on the breadboard on D1) |

## 5. LSM features the take-apart code may not handle, or handles oddly

1. **D4's still ways** (guide.py:700, 748, 756: `move=[D4], paths={D4: [ZERO] * 5 / * 3}` to pace the matrix's rides in Steps 26, 30,
   31). take_apart records them as D4's ways in (stepgen 848-858) and `fits[-1]` takes the latest, Step 31 (1000-1004): `remove([D4])`
   would not move D4 at all, draw no arrow (1404-1405) and use Step 31's camera (the D10 close framing, dir [-0.6875, 0.4904, -0.5355]).
   By hand: `path=[[-8.0, 0.0, 0.0], [-8.0, 65.0, 0.0]]` (Step 25's way reversed: off the tabs of D1 and D2, then up; the USB cable leaves
   the notch in its foot as it slides) and Step 25's camera (`view_dir=[-0.5792, 0.5736, -0.5792], frame=([630.0, 880.0, 1228.0], 125.0)`).
   The same three steps also mean the matrix has **no record** of Steps 26 and 30 (it moved there as a rider): walking those back is
   `lift([MATRIX], path=...)` by hand, poses from the carry entries (below).
2. **The matrix carried and turned (Steps 26 - 32).** Only Step 32 is the matrix's own move. Every pose and route needed to walk the
   rest back is in steps.json (0.1 mm rounding of plain poses in carry entries does not matter):
   - Step 32 reversed (into the box -> held over it): `lift([MATRIX])` with no path uses Step 32's way reversed (seat, via P_HALF,
     P_HELD [-0.2, 56.6, -0.3]; one beat) and camera; give `wire_via={w: [ROUTES[62/63/64]]}` (HALF) and `wires={w: ROUTES[59/60/61]}`
     (HELD), from `VIEW['Step 32c']['wire_via']` and `VIEW['Step 32']['wires']`. D10 and the three sockets ride along (with_riders).
   - Step 31 reversed (D10 off the held matrix): D10 has no record; `remove([D10], paths={D10: [compose(P_HELD, [0,0,40], pivot),
     compose(P_HELD, [0,-22,40], pivot)]})`: slide along +Z 40, then down 22 (`VIEW['Step 31']['carry']['D10']`, Step 31c `via`), with
     Step 31's camera by hand. Without a path: straight up through the matrix, WARNING + Review note (1026-1032).
   - Step 30 reversed (held -> outside D4): `lift([MATRIX], path=[[-90.8, 56.6, 25.1], [-90.8, 5.9, 25.1]], wire_via={w: [ROUTES[56/57/58]]}
     (LIFT), wires={w: ROUTES[53/54/55]} (OUTSIDE))`, Step 30's camera (`view_dir=DIAG, frame=([601.0, 910.9, 1204.6], 114.8)`). The
     OUTSIDE / LIFT shapes run over D4's top edge: only right while D4 is on.
   - Step 26 reversed (outside D4 -> beside the base, 4 beats, turned twice): `lift([MATRIX], path=[P_UP_OUTSIDE, P_MID, P_UP_BESIDE,
     P_BESIDE], wire_via={w: [UP_OUTSIDE, MID, UP_BESIDE]} (routes 46,45,44 / 49,48,47 / 52,51,50), wires={w: BESIDE} (33/34/35))`; poses from
     `VIEW['Step 26c']['carry']['MATRIX']['via']` reversed and `VIEW['Step 26']['carry']['MATRIX']['pose']` (P_BESIDE, a turn of 180 deg about
     MC [638.82, 895.58, 1203.99]); Step 26's camera (from straight above: a horizontal arrow is fine there, a vertical one would be end-on).
     Four stops and three wire_via routes + the last: the wires keep pace stop by stop, as in the Full Build (there the pacing came from
     D4's still way and the matrix was a rider with `via`; here the matrix is the mover - the interpolation of its turned poses should be
     the same, but this is the one walk-back with turns to check with motioncheck.py). BESIDE runs along the floor past D5's place: only
     after D5 (and D3) are off, which the reverse order gives.
   Reversing a Full Build route sequence replays the Full Build's own blends backwards (what its Prev button shows), so `tail_from` /
   `stretch` / `b_from` matching behaves as it did there. A change between two routes the Full Build never blended (e.g. SEATED straight
   to BESIDE) is untested ground.
3. **jumper() routes with follow / tail_from / stretch** (guide.py:244-268): the in-box shapes have `b_from` = length - 6 mm (follow=6),
   so with no new route only the last 6 mm move with the socket (wires.py:26-27): a matrix lifted without `wires=` drags a 6 mm stub
   across the screen from a wire left lying in the box. **lift() never re-routes leads by itself** (only unplug does, 1090-1096): every
   matrix move needs `wires=` (+ `wire_via=` for several stages).
4. **The sockets (J_*_F) and D10 ride on the matrix; the D11 posts ride on D1** (carry at guide.py:478 / 566, 752, 803). None has a
   Full Build record, so: `unplug()` of a socket is a ValueError (1022-1023); `remove()` of any of them pulls it straight up unchecked,
   with a WARNING and a yellow Review note (1026-1032). Their real ways: sockets off along the pin, +Z in the matrix's frame
   (`compose(matrix_pose, [0, 0, 15], pivot)`, guide.py:224, 227-229); D10 as item 2; D11 posts straight up (`direction=[0, 1, 0]`,
   hover about 80 is what the generator would pick: hover_distance 298-313 on 80 mm posts) - giving `direction=` removes the warning.
   Riding parts are also never obstacles in the order check (983, 1048), so taking D6 off before the posts would not be warned about.
5. **The three breadboard wires as a group** (Lee: "the 3 breadboard wires"). Each wire is two caps and a lead: J_WHITE_M / J_WHITE_F
   etc. (`wire white` a = pin, b = socket). Options in the code:
   - `remove([3 pins + 3 sockets], ...)`: both ends of every lead leave, so the leads go with them (1107-1108), no routes needed (as the
     MRA's eight wires, MRA 238-239). Pins: Steps 11-13 reversed (up 30). Sockets: `paths=` by hand (else straight up + Review). Default
     units would be 3 + 1 (+ NOTE, 1134-1135): give `arrows=[]` and an eye per end, or `units=` by hand. Camera by hand: the default
     would be Step 13's close view of b19 (the max record), which leaves out a matrix lying beside the base (NOTE, 1727-1734).
   - `unplug([3 pins])` alone: the way is right but each lead takes Step 11 / 12 / 13's hover route (21, 25, 23: drawn with the matrix
     upright at P_UP and the sockets 15 mm off its pins), which is wrong anywhere else; give `wires=` (no Full Build route has the pins
     out with the matrix beside the base or in the box: they would have to be drawn).
   - `remove([3 pins])` alone: refused (lead left on its socket, 1110-1112) unless `wires={w: None}` (the wires vanish).
   Order: the purple pin (b19) is under the 330 Ω resistor's leg / the USB plug: the wires before R330 and the USB plug's area is the
   reverse order anyway.
6. **The button and its nut (Steps 18 - 20, 24, 21 - 22).**
   - D2 to D2_OUT: `lift([D2])` uses Step 24 reversed (+Z 57.1) and its camera; BUTTON and NUT ride along; give
     `wires={'lead red': ROUTES[38], 'lead black': ROUTES[39]}` (Step 24's hover routes, drawn with D2 at D2_OUT) or the leads stretch
     from the seated shape. Only once D4, D5, D3 and the D9s (in slots in D2 and D3) are off (the order check would warn otherwise).
   - The pins: `unplug([BTN_RED_PIN, BTN_BLACK_PIN])` then needs nothing by hand: Steps 21/22 reversed, leads -> routes 36/37, each pin
     then rides on BUTTON (its `rode`), two eyes (as the published Step 17). **Done with D2 in its seat it is wrong**: those poses and
     routes are drawn with D2 at D2_OUT (route 36/37 `a_ref` [0, 0, 57.11]).
   - NUT: its record (Step 20) has the group NUT + BUTTON, so alone it is "computed" (straight up + Review); BUTTON's latest record
     is Step 20's still way [ZERO]*3 (the TWO_BEATS trick, guide.py:534, 553-554), so it would not move. Both by hand: the nut's
     Step 20 poses reversed (`full_way_back('Step 20', NUT)` as MRA 92-99, which restores the via() lost in JSON), each shifted by
     D2_OUT; the button `path=[[0, 0, 157.1]]` (Step 19's +Z 100, plus D2_OUT); `alone=[D2, BUTTON, NUT, pins]`; camera from Step 20 /
     19 slid by D2_OUT (`camera_of(step, moved=[0,0,57.1])`). Note: the nut's reversed poses have stops [0, 8] (one beat for two turns);
     in the Full Build the button's still way stretched it to two beats: make one middle pose a stop for two beats.
   - Taking the button out takes its pins (riding on it after the unplug) and both leads with it (1107-1108); removing D2 while the pins
     are still in j5 / j16 is refused (lead left on the pin).
7. **D3's two-stage tilt** (guide.py:708-714): Step 27 reversed is a swing of 22 deg about the hinge then a 40 mm slide along the tilt
   (two beats), by Step 27's turned-over camera. The order check is skipped for ways with turns (1049). The arrow follows the longest
   stage, the slide (D3's middle moves only ~16 mm in the swing): `arrow_style={D3: dict(stage=0)}` for the swing (the published Step 16
   is a pull outward from the bottom tab, with a framed close-up).
8. **Turned-over steps (flip).** D5 and D3 come off turned over by default (Steps 28 / 27 cameras carry `flip`; `flip=` is not needed and
   `flip=False` does not undo it: give a camera to show them upright, 1146-1147). The run code re-derives the pivot and axis from the
   deconstruction's first turned view (2029-2044); their framings are not merged (different directions). If the D11 posts are taken out
   from below as Steps 34-36 put them in (Step 36's camera, dir [0.4109, -0.8401, 0.3541]), a vertical arrow is end-on (|d . dir| = 0.84 >
   0.8) and becomes an eye (1407-1408, 1762-1763) unless `keep=True`.
9. **ghost= on Step N** (Steps 32's inset ghost, 36's D1 / D5 see-through): takeoff steps have no `ghost` (not in _takeoff's signature,
   949-952; no ghost written, 1781-1810), and an inset's `ghost` is dropped (1777-1778). Show a hidden catch with a 3D close-up
   (`inset=dict(target, dir, radius, hide=[...], mark=half_width)`) instead.
10. **inset image=** (the capacitor card, Step 6) and `marks=` (Step 33's four slots) and `side=`: dropped by the takeoff branch
    (1777-1778: only target, dir, radius, hide, mark, alt, caption, arrows). One red box per close-up (`mark`), at its target.
11. **labels_done** (not used by the LSM's Full Build): takeoff steps have labels on Step N only (1781).
12. **The 64 stems** (Steps 39 + 40): fine; together they are 2 units (two records), so `units=[STEMS]` for the published single arrow
    (it starts on the stem nearest the middle of the block, 1397-1402) and `eye=[a middle stem]`. The camera defaults to Step 40's
    (STEM_CAMERA). 64 parts in the order check's union is light.
13. **The USB cable and its A end**: USB_A has no record (`show=` in Step 23) and is pulled out the first free axis (~45 mm, likely up),
    giving 2 arrows; as the MRA and RCC: `units=[[USB_B]], paths={USB_A: [[0.0, 25.0, 0.0]]}` (A lies at its seat on the table, x 460 -
    510). The lead goes with the two ends (1107-1108). Step 23's camera frames both ends.
14. **rest_at parts** (BREADBOARD 276, ribbon 379, pins / sockets 397-398, MATRIX 476, D2 560): none carries over (the build leaves
    everything seated). Every "set aside" pose the deconstruction uses (P_HELD, P_OUTSIDE, P_BESIDE, D2_OUT, D10_UNDER, D11_UP ...) must
    be read from steps.json (Step 24 path, Step 26 / 26c / 30 / 30c / 31 / 31c / 34 carry) or copied as numbers; guide.py cannot be imported
    (its g.build() at line 826 runs on import and rewrites steps.json and parts.json).
15. **Resistor legs** (routes with a = resistor, b = None): go with their resistor (1107). The leg bending (Steps 4, 8), the capacitor
    card (6), the ribbon pulled apart (10), the matrix turned over to read its pins (14) and the backing (1) are preparation steps: no
    counterpart (rulebook section 11, "coarser than the build").
16. **lift()'s "plug left behind" warning** (1153-1158) looks for seated parts whose Full Build record has `rode` (the button pins, and
    MATRIX, which rode on BREADBOARD before Step 32) within 1 mm of a lifted part's box: possible spurious warnings if the matrix is still
    in the box when something next to it is lifted (not in a reverse order).
17. **The end and the title page**: the Completed View must keep something (2020-2021): D1 + the breadboard (as the published guide),
    or D1 alone if the breadboard comes off too (Step 2 reversed: up 49). It is framed on what is left from the last step's camera
    direction, or from `hero` (azimuth 225 by default, not the LSM's 45) if the last step was turned over (2025).

## 6. Checklist for whoever writes LSM Build Instructions/deconstruction.py

- `Guide(HERE, title='Laser Stem Matrix (LSM)', part='Deconstruction', names=dict(FULL['names']), steps_file='steps-deconstruction.json',
  source='lsm.glb', hero_azimuth=45, copyright_line=...)`; `g.take_apart(parts_list_at_end=True)`; never `import guide`.
- By hand, always: D4's way (item 1); every matrix move after the first lift, with its routes (item 2); D10's way; the sockets' way
  (or the whole wires removed with them); the D11 posts' `direction=`; the nut's and the button's ways (item 6); a camera wherever a
  way is by hand (camera_of as the MRA's); `units=` / `arrows=[]` where the default gives more than 2 arrows (stems, USB, wires).
- Works by default: stems, D8, D7, D6, D9s, D5, D3 (turned over), D2 (lift; give its lead routes), the button pins (unplug, once D2
  is at D2_OUT), USB_B, R330, CAP, R12K, NANO, BREADBOARD, the first matrix lift (give its routes).
- A strict reverse of the Full Build stays on routes the Full Build already has: stems -> D8 -> D7 -> D11s -> D6 -> matrix lifted
  (32) -> D10 (31) -> matrix out over D4 (30) -> D9s (29) -> D5 (28, turned) -> D3 (27, turned) -> matrix back beside the base (26) ->
  D4 (25) -> D2 out (24) -> USB (23) -> button pins (22 + 21) -> nut, button, D2 in the hand (20, 19) -> the three wires (17 - 11, both
  ends at once) -> matrix -> R330 -> CAP -> R12K -> NANO, ending on the breadboard on D1. Any other order (the published one takes D5 and
  D4 off before D11 and D6, and lays the matrix with D10 on the table while the walls are on) needs wire shapes the Full Build does not
  have, drawn anew (guide.py's helpers would have to be copied, not imported).
- After running it (one heavy job at a time): read the log for WARNING / NOTE lines; run `tools/motioncheck.py` on
  steps-deconstruction.json for the matrix walk-backs; the browser runthrough with `?steps=steps-deconstruction.json`; a guides.json
  entry with "script": "deconstruction.py" before any publish (CLAUDE.md).

## 7. Not checked here
Nothing was run (no generator, no player). The pacing of a moving part's turned poses against wire_via (item 2, Step 26 walked back)
and the look of the unplug / lift blends are inferred from the code and from the Full Build doing the same blends forwards.
