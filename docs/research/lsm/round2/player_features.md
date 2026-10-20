# LSM round 2: what the player and the generator can already do

Read-only study (19 Oct 2026) for Lee's notes of 19 Oct (`docs/research/lsm/lee_notes_2026-10-19.md`, pictures in
`lee_images_2026-10-19/`). Files read: `player/player.html`, `player/js/core.js`, `player/js/player.js`, `player/js/runthrough.js`,
`tools/stepgen.py`, `tools/wires.py`, `tools/publish.py`, `tools/bundle.py`, `LSM Build Instructions/guide.py` and its generated
`steps.json` (the committed first draft; note that `guide.py` already has uncommitted edits in the working copy: Step 1's arrow, and
Step 39 changed from `rest()` to `place(move=STEMS[1:])`). Numbers were measured with throwaway scripts in
`/private/tmp/claude-501/lsm_pf/` that load only `steps.json` and `tools/wires.py`. Assembly mm, Y up. Line numbers are those of
the files at commit f5d9422 (the working copy's `guide.py` line numbers are given where cited).

Summary:

| Lee's request | Possible with what exists? | Smallest change if not |
|---|---|---|
| D1 translucent from below, fading back to opaque during Step Nc (Step 33) | No. The machinery exists (`stage.setFade`), no view field drives it | Player: a `ghost: {id: alpha}` view field (about 6 lines in `stepAnimation`); generator: `place(ghost=)` (about 6 lines) |
| Breakout box on the hover view, top-down, D6 hidden (Step 32) | The player: yes. The generator: puts `place(inset=)` on Step Nc only | Generator only: also write the inset on the hover view (`single=True` steps drop it today) |
| Several red squares in a breakout (Step 32, picture 6) | No: `mark` is one square round `target` | Player: a `marks` list (a loop in `buildInset`) plus a pass-through key in stepgen |
| Smooth resistor-leg bends (Steps 4, 7) | Not cleanly: the player resamples every wire to about 1.5 mm per ring | Player: one line, a per-route `spacing`; a no-player-change hack exists (below) |
| Nut spinning 1 - 2 turns (Steps 17, 19) | Yes: `via()` / `turned()` poses (or `ride=` lists), each under 180 degrees apart | none needed; watch the speed (aliasing) |
| All 63 stems moving in at once (Step 39) | Yes: `place(move=STEMS[1:])` | none |
| Image "popout" like Cadasio's Capacitor card (Step 6) | No image field anywhere; the 3D inset is the same visual element | Player: `inset.image` (a few lines in `buildInset`) plus `publish.py` / `bundle.py` shipping the file |

---

## 1. Translucency (Step 33: D1 see-through from below, then opaque again)

**What exists.**

- The toon material has an `opacity` uniform but is created opaque: `toonMaterial()` sets `transparent: true` only for a fading wire
  (`player/js/core.js:18-33`, `opacity: {value: 1}` at :20, `transparent` only with `fade` at :31). A glTF material's own alpha is
  ignored, because every mesh gets `toonMaterial(o.material.color.clone())` (`core.js:85-88`). So `materials.json` cannot make a
  part see-through.
- `stage.setFade(id, a)` (`core.js:122-146`) draws a part with see-through copies of its materials (meshes, edge lines and hulls:
  it traverses `isMesh || isLineSegments`, :135), sets `copy.transparent = true` and `opacity = a`, and puts the part's own materials
  back when `a >= 1`. The copies still write depth ("nearest surface only", comment at :122-123). `stage.clearFades()` (:146) clears
  them all.
- The only caller is the deconstruction fade: `anim.fade`, set in `go()` from `awayTiming()` for a view with `leaving`
  (`player.js:646-661`, `524-543`), driven per frame in `stepAnimation()` (`player.js:703-707`). Fades are cleared at the start of
  every `go()` (`player.js:592`) and at the end of a fading animation (`player.js:725`).
- No steps.json view field holds a part translucent at rest. The only other "fade" field is a route's `fade: [from_mm, to_mm]`
  (`tools/wires.py:28-30`, drawn in `core.js:357-368`), which fades a wire along its length; wires only.
- `stepgen.place()` has no option for it (`tools/stepgen.py:1198-1201`), and `publish.py` would pass a new view key through
  unchanged (it strips only `AUTHORING_KEYS = ('review', 'text_key')`, `tools/publish.py:61`, applied at :340).

So Lee's Step 33 sequence (posts held at the top of D1's slots, D1 translucent from below, then the posts go in as D1 fades back
to opaque) cannot be authored today.

**Smallest player change (not made).** A view field `ghost: {part id: alpha}` (alpha 0..1, a part not listed is opaque):

1. `player.js`, in `stepAnimation()` just after the fade block (after line 707):
   `const g0 = (anim.from && anim.from.ghost) || {}, g1 = anim.to.ghost || {};`
   `for (const id of new Set([...Object.keys(g0), ...Object.keys(g1)])) stage.setFade(id, (g0[id] ?? 1) + ((g1[id] ?? 1) - (g0[id] ?? 1)) * e);`
   This runs before the frame is drawn (`frame = now => stage.frame(now, stepAnimation(now) || ...)`, `player.js:1082`), so the
   `clearFades()` at the start of `go()` (:592) causes no flash. A jump has `anim.from = null` and `e = 1`, which gives the target
   view's alphas at once. Going back from Step Nc to Step N fades D1 out again to 0.5.
2. `player.js:725` (`if (faded) stage.clearFades();`): after this line, apply `view.ghost` again, so that a deconstruction fade in the
   same step does not wipe the ghost.
3. Optional: `applyState()` / `renderThumb()` (`player.js:189-193`, `812-840`) should apply `view.ghost` so that the step list's
   pictures show it. `hitUnder()` / `thingUnder()` (`player.js:879-907`) could skip ghosted parts, so that a click picks the post
   behind D1 rather than D1.
4. `runthrough.js` checks opacity only for deconstruction fades (`runthrough.js:55-86`). A check that each part's opacity equals
   `view.ghost[id]` at rest would be worth adding.

Generator side: `place(..., ghost={D1: 0.5})` stored by `_record()` and written on the hover view in `build()` (next to
`stepgen.py:1847-1849`), with an optional `ghost_done=` for the done view. A Step N with `ghost` followed by its own Step Nc
without one then gives exactly "the D11s go in as D1 fades back to opaque": the alpha is blended with the motion's eased progress `e`
over the beat (800 ms).

What the existing `setFade` copies look like: opaque parts are drawn first and transparent ones after (three.js), so the D11 tabs
behind a 50% D1 show through it. D1's edge lines fade with it (`copy.opacity = a`), and its hull outline goes as `a^3`
(`core.js:49`). Two ghosted parts one behind the other hide each other (the copies write depth). D1's own far faces can show
unevenly through its near faces. Cadasio's Step 34 (picture 7) has every wood part translucent, not only D1: the field takes
any set of ids.

**Without a player change**, the nearest is the real view through the slots: from below (`flip=True`), D1's slots are
through-holes, so with D1 opaque the tips of D11 posts held at the top of the slots show inside the slot openings. An inset from
below (`dir=[0, -1, 0]`, see section 2) gives a close-up of one slot. There is no way to hide D1 for one step only, short of
`put_away([D1])`, which is wrong here: the next view starts afresh with nothing gliding (`stepgen.py:1179-1196`, `cut`).

---

## 2. Insets (framed close-ups)

**Generator (`place(inset=...)`, documented at `stepgen.py:1252-1255`).** It is written in `build()` at `stepgen.py:1856-1860`:

    inset = dict(target=[round(x, 2) ...], dir=_unit(I.get('dir', camera['dir'])), radius=float(I.get('radius', 20.0)),
                 hide=list(I.get('hide', [])), **{k: I[k] for k in ('mark', 'alt', 'caption') if k in I})

| option | meaning | default |
|---|---|---|
| `target` [x, y, z] | the spot the close-up centres on and the blue leader points to; assembly mm, not moved with any pose (`player.js:374, 395, 406`) | required |
| `dir` [x, y, z] | the direction from the spot towards the inset's camera, in assembly space; on a turned-over view it turns with the model (`player.js:374`) | the step's camera `dir` |
| `radius` mm | half the framed size: camera distance = radius / sin(fov/2) x 1.05 (`player.js:378`), so 2.74 x radius at fov 45 | 20 |
| `hide` [ids] | parts left out of the close-up (wires are not hidden: `setVisible` touches parts only, `core.js:236`) | [] |
| `mark` mm | one red square of half-width `mark` mm, centred on `target`, 2 px line, rounded corners (`player.js:382-389`) | none |
| `alt` | what a screen reader says for the picture (`player.js:391`) | '' |
| `caption` | a line of text under the picture (`player.js:392`, `#insetcap`) | '' |
| `arrows` (deconstruction only) | which parts' red arrows the close-up shows (`stepgen.py:1722`, `player.js:373`) | none |

- **Which views.** For `place()` (and `seat()`, which takes no `inset=`), only Step Nc: the inset goes on the done view
  (`stepgen.py:1865-1866`). With `single=True` the step has no done view, and the inset is computed, then dropped by the `continue`
  at `stepgen.py:1863-1864` with no warning. A deconstruction's `remove()` puts it on Step N (`stepgen.py:1718-1727`). A Part guide
  re-aims it from the Part's own camera (`stepgen.py:1861-1862`, `2111-2113`).
- **The player draws an inset on any view that has one**, whatever its kind: `if (view.inset) buildInset(view)` when a view finishes
  opening (`player.js:727`; a jump or a resize runs through the same code with a zero-length animation). On a hover view it hides the
  lead lines inside the picture and shows only the arrows `inset.arrows` names (`player.js:373, 380`). So **an inset on Step N, or
  on a one-view (`single=True`) step, needs a generator change only, not a player change**: build the inset dict before the hover
  view is appended (the camera is known by `stepgen.py:1808`), then add it to the hover view at `stepgen.py:1847` when
  `s['single']` or when the inset asks for it (for example `inset=dict(..., on='hover')`), and pass `arrows` through as the
  deconstruction does.
- **Several boxes: no.** `mark` is one number, giving one square centred on `target` (`player.js:382-389`). Picture 6 (Cadasio's
  Step 31: four red squares on D1's corner slots) needs a player change: accept `marks: [[x, y, z, half_mm], ...]` and loop, projecting
  each point with the inset camera `cam` exactly as `target` is projected at :383-385. stepgen would add `'marks'` to the key list at
  :1860 (and :1722).
- **Posed parts: no.** The close-up is a snapshot of the scene as the view stands when it finishes opening: the view's own
  offsets, riding parts and wires (`stage.snapshot(..., {setup})`, `player.js:372-381`; `core.js:450-473`). It can leave parts out
  (`hide`) and look from anywhere (`dir`, `radius`), but it cannot show a part in another pose. "Render from above with D6 hidden"
  is `dir=[0, 1, 0], hide=['D6']`, which works today, on Step 32c. The picture's "up" is the main camera's up projected
  across `dir` (`player.js:375-377`), so a top-down close-up keeps the main view's far side at the top. A view straight down
  falls back to +Z (:376).
- **Not available inside an inset:** labels, eyes (the overlay is SVG on the main view only), lead lines, translucency, an image
  file. Cadasio's pictures 5 and 8 have an eye inside the breakout; ours cannot.
- **Size and placement (no field to set them).** Width w = round(clamp(0.28 x frame width, 200, 400)) CSS px, height 0.72 w
  (`player.js:369`), rendered at up to 2x device pixels (:370). The box (`#inset`, `player.html:74-76`, 4 px #7fdbff border, 12 px
  radius, 6 px padding) is w + 20 wide and h + 12 + (24 with a caption) + 8 tall (:395). It goes on the side of the model with the most
  room (right / left / top / bottom of the model's screen rectangle, `screenRect`, :396-397), in the middle of that free space, level
  with the target for left and right (:398-399). It is clamped 12 px from the frame's sides and 70 px from its top (:400) and moved
  below the caption box if it would cover it (:401-402). A blue leader runs from the box's edge to the target with a dashed 9 px ring
  (:405-409, `placeLeader` :359-364), redrawn as the camera moves (:342).
- **Caveat on a hover view:** the inset keeps clear of the caption box only, not of the labels (`layoutCallouts` places the
  labels first, at :726; the inset follows at :727). A hover inset next to labels can overlap them.

---

## 3. Wires: why the resistor bends look faceted (Steps 4 and 7, picture 1)

**How the player builds a tube.**

- **Samples per wire.** `wireSamples[id] = min(160, max(12, ceil(route.len / 1.5)))`, the largest over every route the wire uses in
  any view (`wires` and `wire_via`) (`player.js:99-101`). Every route of that wire is then drawn with that many points.
- **Resampling.** Each frame the route's centre line, with its ends carried by their parts (`skinned`, `player.js:113-135`), is
  resampled to those n points, evenly spaced along its length, by linear interpolation between the route's own points (`sampled`,
  `player.js:137-146`). **The route's own point density is thrown away**: only its polyline shape is kept, at about 1.5 mm per
  point.
- **Rings.** One ring per sample, `RADIAL = 10` sides (`core.js:321`), each ring perpendicular to the central-difference tangent
  `pts[i+1] - pts[i-1]` (`core.js:382-384`). The frame is carried along by projecting the previous normal onto the new ring plane
  (parallel transport, `core.js:377-393`). Ring vertices sit at exactly `radius` from the centre line (:391), with no mitre
  correction, flat caps (:333-334, :394-398) and two-tone toon shading. The black outline is the same geometry's back faces pushed
  out (`hullMaterial`, `core.js:37-53`).

**Measured on the draft's routes** (`steps.json`; legs made by `guide.py:145-159`: `W.rounded([start, corner, tip], radius=1.2,
spacing=0.25)`, tube radius `LEG_R = 0.31`):

| wire | route length | route's own points | player samples n | player spacing | turns at the player's rings, bent route | narrowest ring, cos(turn/2) |
|---|---|---|---|---|---|---|
| 12k leg 1 | 18.71 mm | 76 (0.249 mm apart) | 13 | 1.559 mm | 11.5, **62.6**, 15.8 degrees | 0.854 |
| 12k leg 2 | 19.03 mm | 78 | 13 | 1.585 mm | 8.1, **61.8**, 20.0 degrees | 0.858 |
| 330 leg 1 | 12.35 mm | 51 | 12 | 1.123 mm | 8.7, **48.3**, 32.0 degrees | 0.913 |
| 330 leg 2 | 12.33 mm | 51 | 12 | 1.121 mm | 9.0, **48.6**, 31.5 degrees | 0.911 |

The 12k leg's 90-degree bend (radius 1.2 mm) is 1.885 mm of arc, from 9.73 to 12.22 mm along the leg, which is barely more than
one player sample interval (1.56 mm). The player draws it as a chamfer: three rings that turn 11 + 63 + 16 degrees. The middle
ring sits perpendicular to the bisector at the full radius, so the tube there is only 85% as thick as it should be across the
bend: a pinched, faceted corner, which is picture 1. The 0.25 mm route points never reach the screen.

**Route properties that avoid it.**

- **Bend radius alone: not workable.** For no more than about 15 degrees per ring, a 90-degree bend needs 6 or more sample intervals,
  so an arc of 9.4 mm or more, so a radius of about 6 mm (12k) or 4.3 mm (330). `W.rounded` caps a bend at 0.45 x the shorter leg
  (`wires.py:104`): with the 7.98 mm drop that is 3.6 mm at most. It would also not look like a resistor lead.
- **Point spacing or count on the route: no effect.** The player resamples to n points regardless (above).
- **What works: about 0.25 - 0.3 mm per player ring along the bend**, which needs n of about 75 for an 18.7 mm leg (cap 160, so
  wires up to about 40 mm can have it). Modelled (`staged_bend.py`): at n = 76 the worst turn at one ring anywhere in the bend, or
  anywhere in the blend from straight to bent, is 12.5 - 13 degrees (cos 6.5 degrees = 0.994: no visible pinch). At n = 13 it is 62.5
  degrees.
- **Smallest player change (one line, not made):** `player.js:101`, `Math.ceil(routes[no].len / (routes[no].spacing || 1.5))`. A
  route then says its own sample spacing. Route dicts reach `steps.json` unchanged (`route_no()` stores the dict as it is,
  `stepgen.py:1587-1592`), so `guide.py` could set `bent[wid]['spacing'] = 0.25` (or `W.route(..., spacing=)` could write it),
  with no stepgen change. Per-frame cost: about 76 rings x 10 vertices per leg, negligible. (A curvature-adaptive `sampled()` would be
  more general but more code.)
- **A no-player-change hack (fragile, not recommended):** n is the largest over every route a wire uses, and `wire_via` routes
  count (`player.js:100-101`), but a `wire_via` route is drawn only while the wire actually changes route (`changing`,
  `player.js:155-158`). A long dummy route (112 mm or more gives n = 75; 240 mm gives 160) in `wires_done=[dummy, same_route]` on a
  step where that leg keeps its route would raise n for every view and never be drawn. Side effects: that view counts as `staged`
  (`player.js:88`), so going back from it plays its moving parts' ways stop by stop (`player.js:624-635`); and it is opaque to
  anyone reading the guide.

**Blending between two routes** (`drawWires`, `player.js:151-180`). From the old route to the new one, through any in-between
routes listed in the step's `wire_via`, one leg after another over the step's eased progress (:157-159). Each leg samples both
routes with the same n points, at the same distances from the wire's first end over span = max(lengths) (:163-165), or by share of
length with `stretch` (:162), and blends them point by point in a straight line (:166). For the resistor legs (straight and bent are
both 18.71 mm, no `stretch`), modelled at f = 0.25, 0.5 and 0.75:

- Straight to bent in one go (the draft): the lead shrinks to 92%, **88%** and 91% of its length (16.5 of 18.7 mm at f = 0.5),
  because the far leg's tip moves on a straight chord (5.46 mm at f = 0.5) instead of swinging round the bend. At n = 13 the corner
  ring turns 13, 30.5 and 48.6 degrees: a corner that sharpens as it bends, but no fold. At n = 160 the corner stays smooth (6 - 9
  degrees per ring) but the shrinking is the same. So mid-blend the lead looks short and slides into shape rather than bends.
- With in-between routes `wires_done=[bent_30, bent_60, bent_90]` (each a `W.rounded` bend at the same radius, made the same length),
  the shortest mid-leg shape is 98.2% of the length (n = 13) or 98.6% (n = 76). With [45, 90] it is 96.6 - 96.9%. The player passes
  through them in order within the one beat (`player.js:157-159`), and Prev plays them backwards (`staged`, `player.js:624-635`).
  Unless the step has as many beats as routes, the wire's progress is the motion's eased `e` (`player.js:697-700`).
- Two routes of **different** lengths without `stretch` fold at the tip mid-blend: the shorter route's samples past its end all sit
  on its end point (`sampled`, :140). `guide.py:155-157` avoids this by making the straight leg exactly as long as the bent one. Keep
  that for any in-between routes.

---

## 4. Rotation (the nut, Steps 17 and 19)

- **Poses.** `turned(axis, degrees, at, t)` (`stepgen.py:122-124`) is written to steps.json as `{t, r: [ax, ay, az, degrees], at}`
  with the degrees as given, for example 720 (`pose_out`, `stepgen.py:189-193`). The player turns it into a quaternion
  (`quat`, `player.js:53`), so 360 and 720 degrees are the same orientation as 0.
- **Between two consecutive poses:** `mixPose(a, b, k)` (`player.js:57-65`). It re-expresses both about b's pivot `at`, moves the
  translation in a straight line, and **slerps** the turn: `qA.slerp(qB, k)` (:62). three.js `slerp` negates the target when the
  dot product is negative (`vendor/three/three.module.min.js`: `if(a<0)...`), so **it always takes the shorter way round.** A step
  between two consecutive poses therefore turns the intended way only if it is **under 180 degrees**. Exactly 180 is
  unreliable: it depends on the sign of a rounding residue (for example 180 to 360 gives a dot product of about -1e-16, so it turns
  backwards). Use 90 degrees per pose (120 at most). Because each pose is turned into an absolute quaternion, a chain 0, 90, 180, ...,
  720 works: every consecutive pair has a dot product of +0.707.
- **Stops and `via()`.** Poses not wrapped in `via()` are stops (`stepgen.py:175-179`, `1296-1297`; written as `stops` /
  `path_stops` only when some pose is a via, :1828-1837). `alongPath()` (`player.js:508-519`) plays one **beat per stretch between
  two stops**, eased in and out (cubic, `ease`, :503, :512). The via poses inside a beat are passed at a steady pace, shared out by
  `poseGap` (mm moved + 0.5 mm per degree turned, :505, :514-518). A beat is **800 ms** (`STEP_MS`, `player.js:8`). A step lasts
  800 ms x the largest number of beats of any moving part (`legs`, :645; `moveDur`, :651). A step where only riding parts or wires
  change is one beat.
- **Two turns over one 800 ms beat: yes.** For the screw-on (Step 19 of the draft, `guide.py:393-394`):
  `path=[[0, 0, -60], via(turned([0, 0, 1], 90, at, [0, 0, -52.5])), via(turned(..., 180, ..., -45)), ..., via(turned(..., 630, ..., -7.5)), ZERO]`
  with `at` on the button's axis (x = AXIS[0], y = 881.63; the axis runs along Z). That is one beat, with the 8 x 90-degree stretches
  sharing it evenly. The last stretch, 630 degrees to ZERO, is 90 degrees the right way (dot +0.707).
  Generator effects: a path whose last-but-one pose is turned gets no automatic lead lines (`straight_in`, `stepgen.py:1299-1300`),
  so use `lines_at`; the player then draws one straight lead line from the hover pose (`leadLines`, `player.js:185`). The log shows
  `hand`.
- **The nut coming off (Step 17)** is a riding part (`ride={NUT: NUT_OFF}`, `guide.py:386-389`). A `ride=` value may be a list of
  poses [in-between..., final] (`stepgen.py:1243-1245`, `1452`, `1798-1800`). The player plays it with `throughPoses()`, each
  stretch an **equal share** of the time (no `poseGap` weighting), eased over the whole step (`player.js:82`, `689-690`). The same
  under-180-degree rule applies to each stretch. Gotcha: `player.js:690` skips the in-between poses altogether when the final riding
  pose is textually identical to the one before the step, so a spin that ends where it began must be written so that it differs
  (it does here: [0, 0, 3.12] to [0, 0, -95]). Going back (Prev) the nut slides straight back without turning (the hover view's carry
  pose is reached by a plain slerp).
- **Which way.** A positive angle about an axis turns clockwise to someone looking along the axis (from behind it). For the
  button (axis +Z, head at +Z), a right-hand nut is screwed on, moving +Z towards D2, with **positive** degrees about [0, 0, 1].
  It is unscrewed, moving -Z off the back, with **negative** degrees, which is counter-clockwise seen from the wire end and clockwise
  seen from the button's head.
- **Speed and aliasing.** Cubic easing peaks at 3x the average speed (`ease'(0.5) = 3`). Two turns in 800 ms average 0.9 degrees/ms
  and peak at 2.7 degrees/ms: **45 degrees per frame at 60 fps**. The nut is 21.04 x 18 x 1.5 mm (`assemble.py:285-290`), which
  reads as a hexagon 18 mm across the flats, so it looks the same every 60 degrees. A 45-degree step reads as 15 degrees backwards, so
  for about 150 ms around mid-beat (k = 0.41 - 0.59) **the nut appears to turn the wrong way**. One turn per 800 ms beat peaks at 22.5
  degrees per frame, which is fine at 60 fps but aliases at 30 fps.
- **Longer than one beat without a pause.** A middle stop eases to rest, which shows as a pause. Each part's way is spread over
  the step's whole motion with its own stops (`player.js:683`). So a nut path with stops only at its ends lasts as long as the
  step's longest way. A step can be made 2 beats (1.6 s) without moving anything else by giving a part already in place a way of
  three stops that stays at its seat: `move=[NUT, BUTTON], paths={NUT: nut_path, BUTTON: [ZERO, ZERO, ZERO]}`. The nut then gets 1.6 s
  for its turns (peak 22.5 degrees per frame for two turns). A riding part's `ride=` list likewise spans the whole step. This is a
  trick: a cleaner way would be a per-step `beat_ms` (a player change, `STEP_MS` is a constant).

---

## 5. Step 39: `rest()` against `place(move=[63 stems])`

- **`rest(caption, ids, like)`** (`stepgen.py:1486-1498`, views at :1767-1779): Step N shows only what is already built, with an
  eye and the label "63x" on the stem fitted in Step 38 (`like`). In Step Nc the 63 stems simply appear in their holes: the player
  glides nothing that was not on screen before (`was()`, `player.js:594-599`). This is the committed draft.
- **`place(move=STEMS[1:], direction=[0, 1, 0], hover=44, lines=False, eye=[STEMS[0]])`** (the working copy, `guide.py:521-523`)
  works as Lee asks. On Step N the 63 stems glide in from 1.8 x their hover offset (79 mm) to 44 mm above their holes as the step
  opens (`further`, `player.js:83`, `636-637`). On Step Nc all 63 go down together in one 800 ms beat.
- **Limits.**
  - Labels: by default one label per name, so the one label "63x LED Stem" goes on the first new stem (STEM_02)
    (`stepgen.py:1457-1466`). It hides with `?labels=0` (only bare quantities `/^\d+x$/` always show, `player.js:312`). For the bare
    quantity as `rest()` gives it, write `labels=[dict(id=STEMS[1], text='63x')]` (its anchor is worked out, `stepgen.py:1813-1815`).
  - Lead lines: automatic ones are capped at 4 (`max_lead_lines`, `stepgen.py:62`, `lead_points` :409-444). `axial=True` would draw
    one line through the mean of all 63 (meaningless), `axial='each'` 63 lines. `lines=False` (as written) or `lines_at=` a few holes.
    The log then shows `lines=0`, which is expected here.
  - Collision test: none, since `direction` and `hover` are given (`stepgen.py:1281-1295`). Without them, `free_directions` would
    test the union of the 63 meshes against everything (ray tests on up to 5000 sampled points per direction, `blocked`, :269-295):
    slower but workable.
  - Camera: `choose_view` frames the hovering and the seated stems together (`_fit`, `stepgen.py:554`), so the view is a little
    wider than Step 38's. The label anchor's visibility test casts a ray at each of the 97 visible parts per candidate point (up to
    160 candidates, `label_anchor` :485-505, `_hidden` :473-482). It usually stops at the first candidate; the worst case is seconds.
  - Player performance: 63 `alongPath` + `setPose` calls per frame during one beat, negligible next to drawing the same 97 parts the
    Completed View draws. Nothing is added per frame at rest.
- A cascade (not asked for) is possible with `paths={id: [...]}` and leading repeated poses: a way that begins by waiting waits there
  (`fromHere`, `player.js:602`).

---

## 6. A picture card / "popout image highlight" (Step 6, the Capacitor card in picture 2)

- Cadasio's Capacitor card (picture 2) is the 3D capacitor with a blue-framed box holding a **raster image** (a photo-like capacitor
  with "GND Strip" and GND / VCC badges), joined by a blue leader to a dashed ring on the part.
- The player has **no image field** for a step or a card. A note card (`kind: 'card'`) shows text and a caution only
  (`player.js:567-573`, `player.html:112-114`). Images appear only in the Parts List pages (bands with `parts/*.png` pictures,
  `player.js:454-481`) and in its large-picture overlay (`#partzoom`, `player.js:486-499`). Those pages are inserted only after the
  title page (`stepgen.py:2057-2059`).
- **The `#inset` element is Cadasio's popout already**: same blue frame (`#7fdbff`, 4 px, 12 px radius, `player.html:74`), blue leader
  and dashed ring (`player.js:405-409`). But its picture is always a 3D snapshot (`$('insetimg').src = canvas.toDataURL(...)`,
  `player.js:390`).
- **With what exists:** a step whose Step Nc has a 3D inset on the stripe (`target` on the grey stripe, `dir` facing it, `radius`
  of about 6 - 8 mm, `mark` of about 2.5 mm for a red square, `caption` such as "Grey stripe: GND (-) leg, into j3"), and on Step N
  labels on the legs (`labels=[dict(id=CAP, text='GND (-)', anchor=[...]), dict(id=CAP, text='+', anchor=[...])]`) with an eye on
  the stripe. A one-view step cannot carry the inset until the generator change of section 2.
- **Smallest change for a real image popout (not made):**
  - player: in `buildInset()`, when `I.image` is set, use it as `$('insetimg').src` and skip the snapshot; keep the caption, the
    placement and the leader to `I.target`. Placement assumes an aspect of 0.72 (`player.js:369`, `395`), so take `h` from the
    image's natural size.
  - stepgen: add `'image'` to the key list at `stepgen.py:1860`.
  - `publish.py`: list the file in `_own_files` (`tools/publish.py:345-353`; `check_site.py` already allows .png / .webp / .jpg).
  - `bundle.py`: inline it as a data URL, as it does for part pictures (`tools/bundle.py:67-77`).
  - The picture itself (badges, arrow, "GND Strip" label) would be made outside and dropped into the kit folder.
