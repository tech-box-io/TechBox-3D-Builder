# The take-apart API (tools/stepgen.py) for the LSM round-3 plan: D10 slid off, the wires off the matrix, then out of the breadboard

Read-only study, 22 Oct 2026, for Lee's note on the deconstruction's Step 10 ("D10 should be removed at this point and the wires
disconnected from the LED Matrix in a group, but left attached to the breadboard, then the breadboard wires moved. Remember, D10 must
slide off of the LED Matrix"). No model was loaded; numbers are from `tools/stepgen.py` (2440 lines), `player/js/player.js`,
`tools/motioncheck.py`, `LSM Build Instructions/deconstruction.py` (335 lines), `guide.py`, `wire_shapes.py`, `steps.json`,
`steps-deconstruction.json` and `published-takeapart.json`. Line numbers are those files' as they stand (HEAD f9e9da1; the LSM files
are unmodified in the working tree).

## Answer first

1. **`remove(caption, [MATRIX])` with the three sockets riding on it is refused.** The riders go with the matrix (line 1001). Each
   wire then has its socket end leaving and its pin end staying, so line 1166 raises "the lead wire ... would be left on J_..._M with
   nothing at its other end". `wires={w: None}` or `wires={w: route}` gets past that check, but the wire then vanishes the moment Next
   is pressed, with no fade (see 1.3).
2. **`remove(..., [MATRIX], let_go=SOCKETS, path=[...])` is the one-step form of the plan's Step 11.** The sockets stay exactly where
   they are, resting and no longer riding. Their wires keep their routes, untouched. The matrix slides off the header pins and away,
   then fades. Only the matrix moves (along −Z of its own frame, the reverse of the sockets' +Z pull), so the wires cannot pass into
   anything. `wires=` may still give them new routes in the same step; they would blend over the matrix's motion while the sockets
   stay put.
3. **`unplug(SOCKETS, ...)` needs `paths=`.** The Full Build never "moved" the sockets: it put them on by `ride=` in its Steps 15 - 17
   (`moving: []`). Without `paths=`, line 1054 raises. With `paths=` the sockets move off the pins and end resting, not riding, unless
   `ride_on=` is given. Their wires keep their old routes (bent by the socket's move) unless `wires=` gives new ones. `unplug()` never
   takes anything off the screen (`leave = []` for unplug, line 1001), so the matrix needs a `remove()` of its own after it.
4. **`remove(caption, PINS + SOCKETS)` takes each wire whole.** Both ends leave, so the three leads go with them (`lead_off`, lines
   1156 - 1164) and fade with their ends (player.js 703 - 705, 907).
   - **Pins:** each takes the Full Build's way reversed, `[0, 0, 0] -> [0, 30, 0]`, by default.
   - **Sockets:** they are not in their seats, so by default they are "pulled straight up, unchecked" with a WARNING and a Review
     note. Give `paths=` per part (each its own).
   - **Arrows:** by default up to six (three pin units from three Full Build steps, plus the sockets), with a log NOTE. `units=[...]`
     sets them by hand.
   - **Eyes instead of arrows:** `arrows=[]` with `eye=[...]`, and no `units=`, because `units=` makes arrows whatever `arrows=` says.
5. **D10: `remove([D10], path=[slid, lowered], arrow_style={D10: dict(stage=0, ..., then=[dict(stage=1, ...)])})` is valid.**
   - **Stages:** D10 is the only part moving and has two stages. `stage=0` is required. The `then` stages must be after it, in order
     and below 2.
   - **Timing:** the generator adds a one-beat hold before stage 1, so the step plays in three beats. It renumbers `then`'s stage to 2.
   - **Arrow tail:** a `then` arrow's `at=` is an absolute tail. Give it where D10 is after the slide, not where it starts.
   - **Wire clearance:** the Full Build's Step 31, reversed, has the same matrix pose and identical wire routes as the
     deconstruction's Step 9c (routes 59 / 60 / 61, deconstruction route numbers 10 / 11 / 12). guide.py drew those routes so that D10
     comes up and slides along with the wires lying in its notch (guide.py 653, 729 - 733).
6. **Two pitfalls change the plan.**
   - **The D9s must come out before the wires are pulled from the breadboard.** The wires run under D9_A's engraved end (open at the
     bottom) and under its lower edge. The D9s can come out once the matrix has gone (they are blocked while it is held over the box).
     So the order is: Step 9 lift, 10 D10, 11 matrix off the connectors, 12 both D9, 13 the wires out.
   - **`tools/motioncheck.py` does not check anything a `remove()` takes off.** It tests only the done view's `visible` parts and
     `wires`. A leaving part (D10, the matrix, the D9s) and the leaving leads (`leaving_wires`) are not tested. The motions Lee is
     worried about therefore need another check (section 7).

## 0. The state the plan starts from (after Step 9c, as steps-deconstruction.json has it now)

- `MATRIX` is resting, not riding, at `[-0.2, 56.6, -0.3]`, a pure shift. That is the Full Build's `P_HELD = [-0.2, 56.64, -0.32]`
  (guide.py 224), rounded by `pose_out` (stepgen 189 - 193).
- `D10`, `J_WHITE_F`, `J_GREY_F` and `J_PURPLE_F` ride on `MATRIX` at pose `[0, 0, 0]`. This is the `take_apart()` begin state (lines
  904 - 908). Step 9c's `carry` shows it too.
- The pins `J_WHITE_M`, `J_GREY_M` and `J_PURPLE_M` are seated in i2, i3 and b19. They are neither riding nor moved.
- The leads `wire white`, `wire grey` and `wire purple` have `a` = pin (`J_*_M`) and `b` = socket (`J_*_F`). Their routes are the Full
  Build's `HELD` routes 59 / 60 / 61 (deconstruction route numbers 10 / 11 / 12), with:
  - `b_ref` `[-0.2, 56.64, -0.32]`;
  - `b_from` 255.20 / 245.75 / 178.41 mm;
  - `tail_from` 154.17 / 146.85 / 78.35 mm.

  (Step 9 sets them with `wires=leads('Step 32', 'wire')`, deconstruction.py 247.)
- `self.taken['came']` (the Full Build's moves, stepgen 852 - 870):
  - MATRIX has one record, Full Build Step 32 (path `[[-0.2, 56.6, -0.3], via [-0.1, 28.0, -0.2], [0, 0, 0]]`).
  - The pins have Full Build Steps 11 / 12 / 13 (`[[0, 30, 0], [0, 0, 0]]`).
  - **D10 and the sockets have no record.** The Full Build brought D10 in by `ride={D10: [[0, 0, 40], ZERO]}` from
    `carry(..., pose=[0, -22, 40])` (guide.py 752 - 758; its Step 31 has `moving: ['D4']`). It brought the sockets in by riding from
    `SOCKET_OFF = [0, 0, 15]` (guide.py 225; Full Build Steps 15 - 17 have `moving: []`).
- **Paths are absolute.** A pose in a `path=` or `paths=` is relative to the part's own seat, not to where it is now. For a part riding
  on the held matrix, the current pose is the composed one: `where(i)` in deconstruction.py 96 - 101, or `now(i)` in stepgen 1007 -
  1011, for example `[-0.2, 56.6, -0.3]` for D10 and the sockets.

## 1. `remove(caption, ids, ...)` with ids = [MATRIX] and the sockets riding on it

### 1.1 What goes

- **Riders go with it.** `riders(group)` (986 - 994) is everything riding on the ids, transitively. `leave = ids + riders(ids)`
  minus `kept` (1000 - 1001), where `kept = let_go + riders(let_go)`.
- **Movers.** `movers` (995) is the ids that do not ride on another id. A rider is not a mover: it is carried by its carrier through
  `with_riders` in build() (1724 - 1738), and it leaves and fades with it. In the player, a rider's fade starts with its carrier's
  (player.js 700 - 702).
- **Leads.** For every lead in `wire_state` that touches something in `leave`, unless the lead is named in `wires=` (1157 - 1168):
  - Both ends are in `leave`: the lead goes too (`lead_off`). Step Nc carries it as `leaving_wires`, and the player fades it as its
    later end fades (player.js 703 - 705).
  - One end stays: **ValueError**: `remove('…'): the lead wire white would be left on J_WHITE_M with nothing at its other end: unplug it
    first, take both its ends off together, or say wires={'wire white': None}` (1166 - 1168).
  - So `remove([MATRIX])` without `let_go` is refused for our plan: the pins stay in the breadboard.

### 1.2 `let_go=[ids]`

- **Validation** (996 - 999): each name must ride on something that moves and must not itself be in `ids`. Otherwise:
  `let_go= names parts that do not ride on what moves`.
  - The sockets qualify (they ride on MATRIX).
  - Listing a socket in `ids` and in `let_go` at once is refused.
- **Where they rest.** `held_here = {i: now(i)}` (1012) is where each one is at script time, composed through its carrier. After the
  step (1229 - 1232): `riding.pop(i)`, `resting[i] = held_here[i]`, `parked.add(i)`.
  - In build() this happens before Step N is drawn (1775 - 1779), so both views show them at that pose, not riding.
  - For our sockets that pose is `[-0.2, 56.6, -0.3]`: in mid-air over the box, on the header's line, the matrix gone from above them.
- **Their wires.** Nothing happens to them. `wire_state` is untouched (1233 - 1235 change only `lead_off` and `wires=`). The route
  number is the same on Step N and Step Nc, so the player does not blend (player.js 166, `changing` false). `skinned()` ties each end
  to its part's pose (player.js 105 - 145), and neither end moves, so the wire stands still.
- **`wires=` in the same step is allowed.**
  - A lead named in `wires=` is skipped by the lead check (1158) and gets its new route as the step completes (1872 - 1876).
  - Both its ends are still on screen (`left`, 1878), so `wires_in` (1709 - 1716) draws it on Step Nc. The player blends old to new
    over the step's motion (the matrix's beats).
  - It is legal, but nothing pulls the wires, so a change of shape here would look self-propelled. With `let_go` the wires are best
    left alone.

### 1.3 Why `wires={w: None}` or a new route does not help when the socket leaves with the matrix

- If the socket is in `leave`, the lead is not in `lead_off` (named in `wires=`), so it is not in `leaving_wires`.
- `wires_in(…, left)` drops it from Step Nc because its `b` end is not in `left` (1713).
- The player draws `leads = {...to.wires, ...to.leaving_wires}` (player.js 907), and the lead is in neither. It disappears at the
  first frame of the step: no fade, no motion.

### 1.4 The matrix's own way

- MATRIX is resting at a moved pose, so the Full Build's way (Step 32) does not apply. The test at 1034,
  `(not _moved(start) and i not in self.riding) or in_seat_on`, fails, and MATRIX falls to `computed` (1055 - 1056).
- **Without a path** (1057 - 1072):
  - `seated_now` is empty, so the direction is `AXES[0] = [0, 1, 0]` (line 51), straight up.
  - The log gets "WARNING: … not in its seat: lifted straight up, unchecked (give direction= or path=)".
  - The step gets the Review note "Not in its seat, it is lifted straight up: the way out needs a check."
- **Give `path=`** (absolute poses, section 0). For example, off the pins along −Z, then away:
  `path=[[-0.2, 56.6, -15.3], [-0.2, 96.6, -15.3]]`.
  - The sockets come off along +Z of the matrix's frame (`WS.PULL = [0, 0, 1]`, wire_shapes.py 76; guide.py `SOCKET_OFF`), so the
    matrix leaves along −Z.
  - 15 mm is the Full Build's own "held off its pin" distance.
- **Its arrow.** By default there is one unit, `('hand',)` (1178), so one arrow along the longest stage (1803 - 1810), here the lift.
  `arrow_style={MATRIX: dict(stage=0, ...)}` points it along the pull instead. Eyes are not given by default for `remove()` (1193),
  so give `eye=[...]` on the sockets if Lee wants the unplug cue (rulebook: an eye on each plug).

## 2. `unplug(caption, plugs, ride_on=None, ...)`

### 2.1 How it finds the way out, and "the route it had before" (no `paths=`)

- **The way** (1029 - 1052). `fits` is the Full Build records of the plug whose group (less what is already gone) lies within
  `ids ∪ leave`. For unplug there is a fallback: the last record whatever its group (1031).
  - The plug must be in its seat and not riding, or riding at its seat on a carrier that stays (`in_seat_on`, 1033).
  - The way is then the Full Build's way reversed, composed onto the carrier's current pose if it rides (1038), with its stops
    reversed (1050 - 1052).
  - The camera is the Full Build step's. It is shifted if the carrier has only slid since, and dropped if the carrier has turned
    (1039 - 1049).
- **The route before** (1146 - 1152). For each lead the plug ends, and that is not in `wires=`, the new route is the route that lead had
  in the Full Build step's hover view, i.e. before that step plugged it in (`m['wires']`, from take_apart 863). `wire_via` is the Full
  Build's next done view's `wire_via`, reversed (862).
- **No record: refused.** For a plug with no record, line 1054 raises: `unplug(): the Full Build never plugged J_WHITE_F in (or it is
  not in its socket now): remove() or lift() it, or give path=`. **This is the case for our three sockets** (section 0).

### 2.2 The options

- **`paths={id: [pose, ...]}` / `path=`.** Absolute poses after where the part is now (1019 - 1022). With a path by hand there is no
  `moves` entry, so:
  - no camera is copied (camera None, then `choose_view` or your camera);
  - no automatic route;
  - no automatic `ride_on`;
  - no order check (1075 - 1087 test only the Full Build's ways).
- **`ride_on=`** (1134 - 1141). An id, or `{plug: id}`. The plug rides on that part from the end of the step, as long as it is on
  screen and not itself moving. Without it, a plug that has a Full Build record rides on what it rode before the Full Build plugged
  it (`moves[i]['rode']`). **For the sockets with `paths=` and no `ride_on`, `ride_after` is empty, so they end resting at their last
  pose** (1243 - 1246; build 1903 - 1904).
  - Do not pass `ride_on=MATRIX`: a later `remove([MATRIX])` would then carry the sockets off and refuse their leads (section 1.1).
- **`wires=`.** Without it, each lead keeps its route and is bent by its ends' moves (`skinned`, section 5), so give new routes. Each
  new route's `b_at` must be the socket's final pose (as `wire_shapes._route` does), so that the player does not move the drawn tail
  again by the socket's offset.
- **Eyes and arrows.**
  - `eye` defaults to one per plug (1193): three eyes.
  - There are no arrows unless `units=[[...]]` is given (1170 - 1174; the automatic units are made only for `how != 'unplug'`, 1175),
    or `arrows=[dict(tail, head, normal, part)]` by hand.
- **`reappear=True`.** Nothing moves. Parts whose pose changes, and leads whose route changes or whose end moves, fade out where they
  are (800 ms) and in where they end (800 ms) (player.js 848 - 857, 879). It is refused with `in_turn=` or for `remove()` (983 - 984).
  `motioncheck.py` skips such a view (148 - 149).

### 2.3 Could `unplug()` pull the three sockets off the matrix's pins?

- Yes:
  `g.unplug(caption, SOCKETS, paths={WS.FEMALE[w]: [WS.socket_pose(w, where(MATRIX), off=15.0)] for w in WS.JUMPERS}, wires={...})`.
  - `socket_pose` is `compose(pose, PULL·off, F_MID[w])` (wire_shapes.py 109 - 111). For the held matrix that is `[-0.2, 56.6, 14.7]`.
  - The sockets end resting there. The matrix stays held in the air, and a separate `remove([MATRIX], path=...)` takes it away.
- **The catch: the wires.** Each socket's wire leaves its +Z end and runs straight on along +Z under the matrix, at x 608.4 / 610.2 /
  611.9 and y 950.97, from z 1203 to 1256 (guide.py `HELD_TAIL`, 736 - 741). Pulling the socket 15 mm along +Z drives it along its own
  wire's run, so new routes must shorten or bunch that run.
  - Matched by the default rule (by distance from the pin end), the wire's tip shrinks into the socket.
  - With `tail_from` in both routes, the tail is matched from the socket end, so the run under the matrix slides along itself toward
    the bend over D2 (player.js 177 - 186).
  - Either way it is a new shape to draw and check. `remove(MATRIX, let_go=SOCKETS)` (section 1.2) needs no new shape at all.

## 3. `remove(caption, PINS + SOCKETS)`: three wires whose two ends both go

- **Movers.** All six caps are movers, provided none rides on another id in the list. After either section 1.2 or 2.3 the sockets
  rest. If they still rode on MATRIX, they would not be movers, and MATRIX would have to be in the list.
- **The ways** (1018 - 1056):
  - **Pins:** each has its own Full Build record (Steps 11, 12, 13), is in its seat and not riding, so it takes its record reversed:
    `[[0, 0, 0], [0, 30, 0]]`.
  - **Sockets:** resting at a moved pose, so `computed`. Lines 1058 - 1063 then give
    `dirs = [AXES[0]]` (since `seated_now` is empty), the WARNING "… not in its seat: lifted straight up, unchecked", and the Review
    note.
  - **`paths={id: [...]}` gives each end its own way** (`hand = (paths or {}).get(i, path)`, 1019). `path=` applies to the movers
    not in `paths`.
  - **Giving all six the same shift moves each wire rigidly.** `skinned()` moves each point by `wa·A + wb·B` with `wa + wb = 1`, so
    equal moves of A and B translate the whole wire. For example pins `[[0, 30, 0]]` and sockets `[_shifted(where(s), [0, 30, 0])]`.
    That is what the old Step 14 relied on with `off=30` ("both ends of each wire move by the same shift", wire_shapes.py 31 - 33).
  - **Unequal moves deform the wire.** The held routes have `b_from`, so every point before `b_from` mm (255 of the yellow wire's 350,
    the floor run, the rise and the bend over D2) moves wholly with the pin (`wb = 0`, so `wa = 1`, player.js 131 - 134). Only the run
    after `b_from` blends toward the socket.
- **The leads fade with their ends.** Both ends are in `leave`, so the leads are in `lead_off` (1163 - 1164) and go into Step Nc's
  `leaving_wires` (1868 - 1869, 1889). The player draws them with their unchanged routes, skinned to the live poses of their ends
  (player.js 907), and fades each from `max(fadeAt[a], fadeAt[b])` over `FADE_MS = 800` (player.js 11, 703 - 707).
  - Do **not** name these leads in `wires=` or `wires_here=`. A lead in `wires=` leaves `lead_off` and vanishes at once (section 1.3).
    A lead in `wires_here=` is drawn on Step N with that route, but Step Nc's `leaving_wires` uses the state route (1868), so it would
    blend back as it leaves.
- **Arrows by default** (1175 - 1191). The units are keyed as follows:
  - a Full Build move gets `('build', index)`;
  - a computed move gets `('out',)`;
  - an id in `paths` gets `('own', i)`;
  - otherwise `('hand',)`.

  So, with no `paths=`: three pin units (three different Full Build steps), plus one `('out',)` unit of three sockets, makes four
  arrows. With `paths=` for all six: six arrows. Above two, the log gets "NOTE: … N arrows (the published take-aparts show 2 at most)"
  (1190 - 1191). The "two of a kind" split (1185 - 1187) applies only to a key group of exactly two same-named parts that are not
  joined by one cable and do not touch.
- **Arrows by hand:** `units=[PINS]` (one arrow, as the current Step 14 does with `units=[SOCKETS]`). Add `arrow_style={PINS[0]:
  dict(dims=, at=)}` for its size and tail.
- **Eyes instead of arrows:** `arrows=[]` and `eye=[...]`, with no `units=`. `arrows=[]` stops the automatic units (1175: only
  `arrows is None`). `units=` would still make arrows (1170 - 1174 run first). `eye` items are ids or dicts (`dict(id=, anchor=,
  side=)`). An item with an id and no anchor gets one from `label_anchor` (1845 - 1847). The published Step 11 - 13 eyes, on our pins in
  their holes, work as is: `eye('Step 13')` (J_GREY_M) and `eye('Step 12')` (J_PURPLE_M), as the current Step 12 uses them
  (deconstruction.py 259).
- **An arrow pointing within 37° of the camera** (`|d·dir| > 0.8`) becomes an eye on the part (1468 - 1469, 1828 - 1829), unless
  `keep=True`.
- **The camera when the pins keep their Full Build ways.** With no camera given, the step takes the camera of the latest Full Build
  move among them (1197 - 1199): Step 13's close-up on b19 (`dir [-0.5792, 0.5736, 0.5792]`, target `[627.0, 892.0, 1213.6]`, radius
  34). That close-up would also leave out the sockets lying aside 60+ mm away, and build() would log "NOTE: … the Full Build's camera
  leaves out …" (1793 - 1800). Give `view_dir=` / `frame=` (the current Step 12 uses `cam('Step 11')`: `dir [0.556, 0.758, -0.341]`,
  target `[625.34, 873.23, 1206.5]`, radius 91.3), or `keep_camera=True`.

## 4. D10: `remove([D10], path=[...], arrow_style={D10: dict(dims=, at=, stage=0, then=[dict(stage=1, dims=)])})`

### 4.1 The way

- **The Full Build's D10 move, walked back:** slid +40 mm along Z of the matrix's frame (its hooks off both edges), then lowered 22 mm
  (guide.py 752 - 758: `D10_UNDER = [0, -22, 40]`, `ride={D10: [[0, 0, 40], ZERO]}`).
- **With the matrix held** (a pure shift, `[-0.2, 56.6, -0.3]`):
  - `D10_SLID = _shifted(where(D10), [0, 0, 40])` = `[-0.2, 56.6, 39.7]`;
  - `D10_DOWN = _shifted(D10_SLID, [0, -22, 0])` = `[-0.2, 34.6, 39.7]`;
  - `path=[D10_SLID, D10_DOWN]`. `where(D10)` composes through MATRIX because D10 rides; `_shifted` (stepgen 156 - 161) keeps a list
    a list.
- **How the generator treats it.** D10 rides on MATRIX, which is not in `ids`, so D10 is a mover (995). `start = now(D10)` is the
  composed pose (1020). `ways[D10] = [start, D10_SLID, D10_DOWN]` (1022). In build(), `riding.pop(D10)` (1782 - 1783).
- **Without `path=`.** D10 has no Full Build record, so it is `computed`, lifted **up** (`AXES[0]`) into the matrix, with a WARNING
  and a Review note. Always give the path.
- **Leads.** None has D10 as an end, so no lead check applies and no lead leaves. The three wires keep routes 10 / 11 / 12 on both
  views; the matrix does not move, so they stand still.
- **This is the Full Build's Step 31 played backwards in identical wire shapes.**
  - Step 9c's routes are the Full Build's `HELD` routes 59 / 60 / 61, with the same `b_from`, `b_ref` and `tail_from`. The matrix pose
    is the same.
  - guide.py drew them so that "D10 comes up between the matrix's end and the wires' bend, the wires in its slot, and slides along
    under them" (729 - 733): dead straight at x 608.4 / 610.2 / 611.9 and y 950.97 from z 1203.0 to 1256.2.
  - D10's notch, seated, is x 605.18 - 612.79 from y 889.10 up (wire_shapes.py 133 - 137). Held, that is x 604.98 - 612.59.
  - The rise beside D2 is "clear of D10 as it comes up (z 1242.7 - 1245.7)" (guide.py 653). That is exactly D10's z range after the
    +40 slide (seated 1202.97 - 1205.97, −0.3 held, +40).
- **Margins.** The grey wire's surface is 0.07 mm from the notch's +X wall (611.9 + 0.62 = 612.52 against 612.59). The grey rise at
  `[610.0, 913.0, 1247.3]` is about 1 mm from D10's dropped face. Both are tight but clear by the Full Build's design. The sibling
  report `fullbuild_d10_wires.md` measures them.
- **Order.** D10 must go while the wires still have these shapes: in the step straight after Step 9, with no `wires=`. The laid and
  loose shapes leave the notch's line within the slide, which is what Lee saw (22 Oct).

### 4.2 `then=` rules (1107 - 1131, and build 1822 - 1843)

- **Same number of stages for every mover, no `in_turn`, no `wire_via`.**
  `legs = {i: len(stops.get(i, range(len(ways[i])))) - 1 for i in movers}` must have one value, and there must be no `in_turn=`
  (1110 - 1112). `wire_via=` is refused with `then=` (1119 - 1120). D10 alone: `legs = {D10: 2}`.
- **Stage numbers** (1115 - 1118, 1831 - 1832). The first arrow's `stage=` is required: `0 <= stage < n`. `then` stages must be
  ascending, unique and strictly between `stage` and `n`. For D10, `stage=0` with `then=[dict(stage=1, ...)]` is the only shape.
- **Holds** (1121 - 1131). Before each `then` stage a duplicate pose is inserted, a one-beat rest during which that stage's arrow fades
  in. Every stage number is renumbered by `new(k) = k + #holds <= k`. D10's way becomes `[start, SLID, SLID, DOWN]` with stops
  `[0, 1, 2, 3]`: three beats. The `then` arrow, written as stage 1, is stored as stage 2.
- **Where each arrow is drawn.**
  - Step N's arrow: `dims` = `(length, width)` in mm. Otherwise the size comes from `_arrow_dims` (1432 - 1436: length
    `clip(0.25·reach + 0.2·size, 15, 40)`, width `clip(0.1·length, 1.6, 3.2)`). `at=` is the tail in absolute assembly mm, and
    `shift=` and `face=` adjust it. An arrow placed by hand (`at`, `shift` or `face`) is not moved on to be seen (1476 - 1477).
  - A `then` arrow is drawn "where the part is as that stage begins": `at_k = ways[i][stops[k]]` (1836). That holds only for a
    computed tail. **An `at=` given by hand is used as is** (1474). D10's drop arrow's `at` must therefore be where D10 is after the
    slide (the published Step 14 tail `[604.07, 945.65, 1204.58]` + 40 in z, roughly), not its starting place.
  - The published Step 14 arrow (D10 straight down) is length 50.76, width 4.43 (published-takeapart.json).
- **Arrows pointing at the camera.** A `then` arrow that would point at the camera is left out with a log NOTE unless `keep=True`
  (1840 - 1841). Step N's arrow becomes an eye instead (1828 - 1829).
- **How the player shows them** (player.js 861 - 865, 888 - 891). Forward, Step N's arrow stays until its stage plays. Each `then`
  arrow fades in during the hold before its stage and fades out as its stage plays. Backward: none. Stills (the step list and the 2D
  PDF) draw all stages' arrows at once (player.js 1033 - 1034).
- **`via()` poses.** A `via` pose in a hand path is passed through without a stop: stops are the indices of non-`via` poses plus the
  first and last (1088 - 1090; `via` class 175 - 179). Stages count stops, not poses, so a `via` inside a stage does not add a stage or
  a hold. Each stage takes one beat (STEP_MS 800, player.js 8).

### 4.3 The camera for this step

- A path by hand means no Full Build camera (`camera` None, 1197). The camera is then `keep_camera`, `view_dir` / `frame`, or
  `choose_view` (1789 - 1791). `choose_view` keeps Step 9's direction if it is still among the good ones (604 - 617).
- Natural choices:
  - **The Full Build's Step 31 camera**, framed by Lee for this very motion: `view_dir=[-0.6875, 0.4904, -0.5355],
    frame=([631.8, 932.6, 1218.0], 63.4)`.
  - **The published Step 14 camera**, `cam('Step 14')`: `dir [-0.519, 0.591, -0.618]`, target `[645.61, 909.86, 1212.47]`, radius
    78.24. The published guide showed D10 coming off the matrix hovering at `HOVER = [0, 56.64, -0.52]` (deconstruction.py 140),
    0.28 mm from our held pose, so it applies without `to_laid`.

## 5. `wires=`, `wires_here=`, `wire_via=` on remove / lift / unplug, and how the player blends

### 5.1 `wires={id: route or None}`

- The routes apply as the step completes, on Step Nc (1142, 1215 - 1216, build 1872 - 1876), and stay from then on (`wire_state`,
  1235).
- A lead named here is exempt from the one-end-left check (1158).
- `None` removes the lead at once, with no fade.
- On `unplug()`, a plug's Full Build route is added automatically for leads not named here (1146 - 1150).

### 5.2 `wire_via={id: [route, ...]}`

- These are in-between routes, one per stage boundary. The last route must be in `wires=`: "wire_via for … needs its last route in
  wires=" (1143 - 1145).
- They are written to Step Nc only for leads still drawn (1890: `if w in wires`).
- Refused with `then=` (1119 - 1120), and with `in_turn=` of more than one group where any lead changes route (1153 - 1155).
- Going back, they play reversed (player.js 793).

### 5.3 `wires_here={id: route}`

- The route is used on this step's two views only: `wires_in({**wires, **s['wires_here']}, …)` (1863, 1886). It is not saved into the
  state.
- On the next step the lead's state route comes back, and the player blends to it as that view opens.
- It is not used for `leaving_wires`, which take the state route (1868).

### 5.4 The player's blend (player.js 158 - 202; motioncheck.py 181 - 208 mirrors it)

- **When a lead changes route.** Between `from.wires[id]` and `to.wires[id]`, through any `wire_via` routes, the route at each frame
  is a per-sample mix. Both routes are `skinned()` with the parts' live poses: each end carries its run by `a_ref` / `b_ref`, with
  `b_from` (nothing before it moves with `b`) or `a_whole` / `b_whole`, and a smooth ramp in between (113 - 145). Samples are matched:
  - **Default:** by distance from the first end (`a` = the pin), over the longer length. The shared run stays put, and a longer route
    grows out of the tip at the `b` end (187).
  - **`stretch` on either route:** by share of length, each route carried by its ends' moves only (`endsOnly`, 135 - 137, 171 - 174).
  - **`tail_from` on both routes:** the head by distance from `a` up to `tail_from`, the tail by distance from `b`, each along the
    route as drawn (177 - 186). The held routes have `tail_from`; LAID and LOOSE (wire_shapes.py) do not.
- **Pace.** `we = paced(vias + 1)` (player.js 904 - 906, 886 - 887). If the number of in-between routes plus one equals the step's
  beats, the lead keeps pace stop by stop. Otherwise it blends eased over the whole motion.
- **When a lead does not change route.** It is redrawn each frame skinned to its ends' live poses, so it bends with its moving ends.
  For the held routes, everything before `b_from` follows the pin rigidly.

## 6. `alone=`, `keep_camera=`, `view_dir=` / `frame=` / `look_from=`, `new_camera=`

### 6.1 `alone=[ids]`

- It must include every id the step moves: "alone= must include the parts it moves" (1002 - 1003). Riders of the listed parts are
  added (1004 - 1005).
- Only those parts are drawn (`shown`, 1780). Both views get `isolated: True` (1860), and `choose_view` frames only them.
- Leaving an isolated view for a normal one does not glide: the model "is simply there" (player.js 809).
- **A lead is drawn only if both its ends are shown** (`wires_in`, 1713). This is why the current Steps 13 and 14 list
  `*PINS, *SOCKETS` in `alone`. In the new plan the pins are in the breadboard, so `alone=[MATRIX, D10, *SOCKETS]` would hide the
  wires, and adding the pins would show them floating without the breadboard.
- For Steps 10 and 11 of the plan, show the whole model: Lee's point is D10 against the wires in place.

### 6.2 `keep_camera=True`

- It copies the step before's camera (`carry_on`, 1789) and takes precedence over the Full Build camera, `view_dir`, `frame` and
  `look_from`.
- `carry_on` is set by every take-off step (1792). A `put_away()` does not change it.

### 6.3 `view_dir=` / `frame=` / `look_from=`

- They are passed to `choose_view` (1790 - 1791) and stop the Full Build camera from being copied (1197).
- `view_dir` is the exact direction (580 - 581).
- `frame=(centre, radius)` sets the target and radius (556 - 557).
- `look_from` picks the three-quarter diagonal nearest to it (589 - 592).
- `flip=True` is a view from below, the model turned. If the Full Build camera was not flipped, it becomes `look_from` (1202 - 1203).

### 6.4 `new_camera=True`

- It only stops the Full Build camera from being copied (1197). With a hand path there is no Full Build camera anyway, so it changes
  nothing for D10, the matrix or the sockets.
- The generator then chooses with `choose_view`, preferring the previous direction (604 - 617). With no travel and no lines it keeps
  the previous camera outright (594 - 597).

## 7. What refuses, what warns, and what nothing checks

### 7.1 Refusals (ValueError) that the plan could hit

| Call | Line | When |
|---|---|---|
| any | 980 - 982 | an id not on screen (taken off already, or put away) |
| lift / unplug | 983 - 984 | `reappear=` on `remove()`, or with `in_turn=` |
| any | 997 - 999 | `let_go=` naming something that does not ride on what moves, or that is in `ids` |
| any | 1002 - 1003 | `alone=` without the moved ids |
| any | 1094 - 1095 | `in_turn=` not listing each mover exactly once |
| any | 1110 - 1120 | `then=`: movers with different stage counts, `in_turn`, a bad stage number, or `wire_via` |
| build() | 1831 - 1832 | `then=` without the first arrow's `stage=` |
| any | 1143 - 1145 | `wire_via` without its last route in `wires=` |
| any | 1153 - 1155 | `in_turn=` (more than one group) where a lead changes route |
| unplug | 1053 - 1054 | a plug with no Full Build record and no path: **the sockets** |
| remove | 1166 - 1168 | a lead left with one end on screen: **`remove([MATRIX])` without `let_go=SOCKETS`** |
| any | 1171 - 1173 | `units=` naming a part that does not move |

### 7.2 Warnings and notes (the guide still builds)

- **Not in its seat, lifted straight up** (1060 - 1063): WARNING plus a Review note. It fires for a computed way of a part that is not
  in its seat (D10 riding, MATRIX held, sockets resting) when no path is given.
- **No straight way out found** (1064 - 1066).
- **Order check** (1075 - 1087). It runs only for the Full Build's ways, when the way is all shifts, starts from the seat, and the
  part is blocked by what is still there but was not blocked in the Full Build: WARNING "the way out of … passes through a part still
  there", plus a Review note. It tests the CAD parts only, never wires.
- **More than two arrows** (1190 - 1191): NOTE.
- **A `then` arrow towards the camera** is left out (1840 - 1841): NOTE.
- **The Full Build's camera leaves out a part lying aside** (1793 - 1800): NOTE.
- **A sub-assembly view's camera** (1200 - 1201): NOTE.
- **A plug left behind** (lift only, 1209 - 1214): WARNING.

### 7.3 What nothing checks

- **Hand paths.** No collision test is made against parts.
- **Wires, in stepgen.** stepgen never tests wires against anything.
- **`tools/motioncheck.py` and `remove()` steps.** It tests, for a done view, only `v['visible']` (217) against `v['wires']` (184).
  A `remove()` step's leaving parts are not in Step Nc's `visible` (`left`, stepgen 1878), and its leaving leads are under
  `leaving_wires`, not `wires`. So it does **not** see:
  - D10 sliding past the wires (plan Step 10);
  - the matrix leaving the connectors (Step 11);
  - the D9s lifting past the floating connectors and tails (Step 12);
  - the three wires leaving (Step 13).

  `reappear` views are skipped outright (148 - 149). Ways to check those motions:
  - **(a)** `motioncheck.py "LSM Build Instructions" "Step 31c"` on `steps.json`. This is the Full Build's identical relative motion
    for D10, with identical routes, as a proxy for plan Step 10.
  - **(b)** Make the step a `lift()` for a check run only. The parts then stay on screen at the end of their way: `lift()` with no
    `ride_on` makes later movers ride on the first, which is harmless for a check. Run motioncheck on that steps file, then put
    `remove()` back.
  - **(c)** Extend motioncheck to add `v.get('leaving')` to the parts tested and `v.get('leaving_wires')` to the wires (a tools
    change for every kit: say so if it is made).

  motioncheck loads the model. On this Mac, run it as the only heavy job (CLAUDE.md: one heavy job at a time) and check
  `sysctl vm.swapusage` first.

## 8. Pitfalls in deconstruction.py as it stands, for this change

1. **The order: the D9s before the wires come out, not after.**
   - The wires run "under the end of D9 nearest D3 … the purple wire under the D9's lower edge" (guide.py 639 - 641, 725). D9_A's
     engraved end is "open at the bottom: the build lowered it over them, so D9_A lifts off over them"
     (docs/research/lsm/decon/study_published.md 63).
   - Pulling the wires up with D9_A in place moves the whole in-box run (before `b_from`) up through D9_A, and neither stepgen nor
     motioncheck (section 7.3) would say so.
   - The D9s cannot come out while the matrix is held. The matrix's bottom is at about y 949.7; a D9's top, 900.7 + 65 = 965.7 at the
     end of its Full Build way `[0, 65, 0]` (same study, line 63). So the D9s come out after the matrix has gone.
   - Order: 9 lift (as now), 10 D10 slid off, 11 the matrix off the connectors (or the connectors unplugged, then the matrix removed),
     12 both D9 (today's lines 251 - 253, camera reconsidered: its `frame` held the laid matrix), 13 the three wires out of i2, i3 and
     b19.
   - If Step 11 leaves the sockets floating (`let_go`), D9_A's lift passes beside them. D9_A is at x 617 - 620 (study_build_map.md 18);
     the grey socket's centre is at x 613.32, so its 2.54 mm housing reaches about 614.6. The tails are at x 612.5 or less. That is
     about 2.4 mm of clearance, an estimate to verify (section 7.3).
2. **Remove the laid-matrix machinery from the new steps.**
   - Today's Step 10 (lines 248 - 250, `to=WS.LAID_POSE, reappear=True, wires=WS.laid()`), Step 12 (257 - 259, `WS.loose()`, pins
     riding on MATRIX), Step 13 (264 - 267) and Step 14 (268 - 275), with `LAID_VIEW` / `laid_cam` / `to_laid`, all assume the laid
     matrix.
   - The published Steps 14 and 15 cameras and arrows were taken with the matrix hovering over the box at `HOVER [0, 56.64, -0.52]`
     (deconstruction.py 138 - 141). With the matrix held at `[-0.2, 56.6, -0.3]` they apply directly: `cam('Step 14')`,
     `arrow('Step 14')`, `cam('Step 15')`, `arrow('Step 15')`, 0.3 mm off, with no `to_laid`.
3. **`g.put_away([MATRIX])` (line 276) must go once the matrix is removed in Step 11.**
   - `put_away()` does not check its ids (1261 - 1278). It would still record a put-away step, so the next view (D3) would open with
     `cut` (no glide: build 1751, player.js 719).
   - `LAID = where(MATRIX)` (line 268) would then be `None`.
4. **The published eyes of Steps 14 and 15 name the published model's copies**, `'D10 copy'` and `'J_PURPLE_F copy'`, not our ids.
   `eye('Step 14')` would give `id='D10 copy'`. Use `eye=[D10]`, or `dict(id=D10, anchor=...)`, as today's line 267 does. The Steps 11
   - 13 eyes name our pins and are fine.
5. **`cam()`, `arrow()` and `eye()` take the published guide's step numbers** (the keys of `PUB`), not ours. Renumbering our steps does
   not change which published step a call should name.
6. **Paths are absolute.** For D10 and the sockets, which ride on the held matrix, build the poses from `where(...)` (as today's line
   265 does with `_shifted(where(D10), …)`). Do this before the step that changes their riding: `where()` reads `g.riding` /
   `g.resting` at that moment.
7. **Step 9 must keep `wires=leads('Step 32', 'wire')`** (routes 59 / 60 / 61), and the D10 step must not change them. The slide is
   clear only in these shapes (section 4.1).
8. **The button and nut steps (lines 295 - 319) show the patterns that work.**
   - `lift(..., path=[via(...), …])`: one beat for eight quarter-turns, since `via` poses are not stops.
   - `lift(..., ride_on=BUTTON)`: the nut ends riding on the button, by `relative_pose(final[by], final[i])`, 1239 - 1242.
   - `arrow_style={NUT: arrow('Step 18', at=False, stage=0)}`: `stage=` alone picks the stage the arrow points along; `then=` is not
     needed for that.
   - `put_away(ON_SET)` after a sub-assembly taken apart on its own.
   - For the new Step 11, `remove(MATRIX, let_go=SOCKETS)` is the analogue of the PMG's devices pulled off their wires' caps
     (`let_go`, stepgen 946 - 947).
9. **No `step-text-deconstruction.json` exists for the LSM.** New captions (new `text_key`s, stepgen 182 - 186) lose no outside edits.

## 9. The calls, sketched (not run)

```python
HELD = where(MATRIX)                                                  # [-0.2, 56.6, -0.3] after Step 9
D10_SLID = _shifted(where(D10), [0.0, 0.0, 40.0])                     # the Full Build's Step 31, walked back: along first ...
D10_DOWN = _shifted(D10_SLID, [0.0, -22.0, 0.0])                      # ... then down, clear of the wires in its notch
g.remove('Slide D10 along under the LED Matrix until its hooks let go of both edges, then lower it away.', [D10],
         path=[D10_SLID, D10_DOWN],
         arrow_style={D10: dict(dims=(..., ...), at=[...], stage=0,                    # the slide (+Z)
                                then=[dict(stage=1, dims=(50.8, 4.4), at=[...])])},   # the drop: at = a tail where D10 is after the slide
         eye=[D10], view_dir=[-0.6875, 0.4904, -0.5355], frame=([631.8, 932.6, 1218.0], 63.4))   # (or cam('Step 14'))
g.remove('Pull the LED Matrix off the three wire connectors ...', [MATRIX], let_go=SOCKETS,
         path=[_shifted(HELD, [0.0, 0.0, -15.0]), _shifted(HELD, [0.0, 40.0, -15.0])],  # off the pins (-Z), then away
         arrow_style={MATRIX: dict(stage=0)}, eye=[...], caution=PULL, **cam('Step 15'))
g.remove('Remove both D9 pieces ...', [D9_A, D9_B], ...)                                 # today's lines 251 - 253, moved here
g.remove('Pull the three wires out of i2, i3, and b19.', PINS + SOCKETS,
         paths={**{p: [[0.0, 30.0, 0.0]] for p in PINS}, **{s: [_shifted(where(s), [0.0, 30.0, 0.0])] for s in SOCKETS}},  # rigid
         arrows=[], eye=[eye('Step 13'), eye('Step 12')], caution=PULL, **cam('Step 11'))  # (or units=[PINS] + arrow_style)
```

Check each with the browser run-through. Check the D10 slide with `motioncheck.py … "Step 31c"` on `steps.json`, and Steps 11 - 13 by
a `lift()` check run or an extended motioncheck (section 7.3).
