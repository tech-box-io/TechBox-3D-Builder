# LAC round 1 (Lee, 20 Oct 2026): how the LSM does what Lee asks for "as on the LSM"

Written 20 Oct 2026 for Lee's first round of notes on the LAC Full Build. Read: `LSM Build Instructions/guide.py` (as of commit 68e430a,
20:52, which put Step 3's c16 label back on its hole and turned Steps 6 - 7), its `README.txt`, `LSM Build Instructions/assemble.py`,
`docs/research/lsm/` (Lee's notes and `round2/player_features.md`), `tools/stepgen.py`, `tools/wires.py`, `player/js/player.js`,
`player/js/core.js`. LAC numbers are measured from `LAC Build Instructions/lac-guide.glb` (7.4 MB; read piece by piece with
`tools/glbio.py`, one process: NAUO6 / NAUO7 resistors, NAUO10 F1, NAUO11 potentiometer, NAUO12 nut, NAUO13 knob, NAUO146 washer) and
`wire-paths.json`. Nothing was run, regenerated or changed in the project; no server, no build.

LAC `guide.py` line numbers are those of the working copy as read: it has uncommitted edits for this round in progress (names,
Step 1 / 15 / 22 labels, RES_LEGS, F4 / F1 / F5 lead lines, the F7s' spread), so they may shift.

## 0. Found while reading: the working copy drops Step 22's potentiometer leads

`LAC Build Instructions/guide.py:447` (the in-progress edit that added `side='top'`) put the `wires=` argument inside the comment:

    labels=[dict(id=POT, text='Potentiometer', side='top')] if first else [],   # (above: its leader clear of the knob) **({'wires': {...}} if first else {}),

so Steps 22 - 24 show the three caps with no leads (they appear only with Step 25's `wires_done`). Put it back on a line of its own:

```python
            labels=[dict(id=POT, text='Potentiometer', side='top')] if first else [],   # (above: its leader clear of the knob)
            **({'wires': {f'pot {c_}': pot_hanging(c_, cap, e, BUILD, PULLED) for c_, cap, _, e, _ in POT_LEADS}} if first else {}),
```

---

## 1. A resistor's legs straight, then bent (LAC Step 4)

### What the LSM does

- **The CAD part is the body only.** `assemble.py:350-373` (`fit_into(..., keep={'Resistor body 12k'}, leg_meshes={'Resistor stem 3'})`)
  keeps only the body mesh in R12K / R330; the CAD's legs are used only to place the body so that their feet land in the holes. There
  is no second CAD body and no `put_away` / `appear` swap: **the legs exist only as wires**, which the player can bend.
- **Two wires per resistor**, `LSM guide.py:159-188`: `g.wire(f'{name} leg {k}', 'pin', LEG_R, name=NAMES[body])` (`:172`; hovering a
  leg names the resistor), `LEG_R = 0.31`, rings every `LEG_RINGS = 0.25` mm (`:163`; `W.route(spacing=)`, `tools/wires.py:34-35`, read
  by `player.js:99-101`). At the default 1.5 mm the 90-degree bend drew as a pinched chamfer (Lee, `lee_notes_2026-10-19.md:15`;
  analysis `round2/player_features.md:135-174`). Each route is tied to the body only (`W.route(..., a=body)`, no `b`), drawn with the body
  at its seat, so the legs ride with the body wherever it is.
- **The shapes** (`:173-186`): bent = `W.rounded([start, corner, tip], radius=1.2, spacing=0.25)`, from 0.4 mm inside the body's end along
  its axis to `corner` (over its hole), then straight down to the tip (2.8 mm under the board's top). Straight = `W.straight(start, axis,
  n)`, **as long as the bent leg** (`n = W.length(line)`). Two in-between shapes bent through 30 and 60 degrees at the same corner, each
  also `n` long, so that the far end swings round on a circle instead of shrinking: the player blends two routes point by point by
  distance from the first end, and routes of different lengths fold at the tip (`player_features.md:189-206`, `player.js:152-180`).
- **One step, two views** (`:298-299`): `g.place('Bend both legs of the 12 kΩ resistor (brown, red, black, red, brown) straight down.',
  show=[R12K], staged=True, lines=False, frame=(mid(R12K).tolist(), 24.0), labels={R12K: '12 kΩ Resistor'}, eye=[R12K],
  wires=R12K_STRAIGHT, wires_done=R12K_BENT)`. Step 4: straight legs, label and eye, the resistor alone (`staged`). Step 4c: the legs
  bend in one beat (no part moves), through the 30- and 60-degree shapes (written as the view's `wire_via`, `stepgen.py:1893`; played
  one after another, `player.js:159-160`). Prev plays it backwards. Camera: `frame=` on the body, radius 24 (the 330 Ω's 18, with
  `view_dir=DIAG`, `:327`).
- **Then** `g.seat('Push the 12 kΩ resistor into h3 and h16.', [R12K], direction=[0, 1, 0], hover=32, labels=[hole_label('h3'),
  hole_label('h16')], lines_at=[hole('h3'), hole('h16')], view_dir=[0.5792, 0.5736, -0.5792], frame=([647.5, 886.0, 1189.5], 30.0))`
  (`:301-303`); the legs keep their bent routes (the wire state carries on from step to step).
- **Parts list**: pictured with its legs straight, as bought: `g.part_picture(NAMES[_body], wires=[dict(colour='pin', radius=LEG_R,
  pts=r['pts']) for r in _legs.values()])` (`:193-194`).
- The LSM's two resistors are different values, so each has its own bend step (Steps 4 and 8).

### What the LAC's CAD has (measured, assembly mm)

| | RES1 (NAUO6) | RES2 (NAUO7) |
|---|---|---|
| body `LAC Resistor 1` | x 677.03 - 688.03, y 898.69 - 903.60 (axis y 901.15), z 1274.20 - 1279.33 | the same, +0.12 y, -5.15 z |
| bent legs `Resistor stem 3` (0.63 mm across) | rail leg: along +x to x 699.20, then 8.0 mm down to y 893.15 (z 1277.36); h leg: to x 666.18, down (z 1276.20) | rail leg z 1272.21, h leg z 1271.05, tips y 893.27 |
| straight legs `Part6^LAC Resistor 1.SLDPRT` (omitted already) | x 663.73 - 678.74 (z 1276.38) and 685.22 - 700.23 (z 1277.13) | z 1271.23 / 1271.98 |
| holes | (-) blue rail x 699.2, z 1277.30; h27 (666.23, 1276.08); hole tops y 897.11 | rail z 1272.22; h29 (666.23, 1271.00) |

The body is 11 mm long; each bent leg is about 19 mm (11.2 - 11.6 mm along, 8.0 mm down), so 76 - 77 rings at 0.25 mm (the player's cap
is 160). The bands are brown, red, black, red, brown on a blue body (`colour-atlas-lac.json`, "LAC Resistor 1", solids in order along
it): the same code as the LSM's 12 kΩ caption. The palette already has `"pin": "#a6a9aa"` (`LAC materials.json:11`), the colour the
LSM's legs use.

### For the LAC

1. **materials.json**: leave the CAD's bent legs out too (the first rule that matches wins, `tools/build_model.py:470-472`; the omit rule
   at `:41-45` comes before the colour rule at `:118-123`):

```json
    {
      "match": "^(Part6\\^LAC Resistor 1\\.SLDPRT|Resistor stem 3)$",
      "omit": true,
      "_about": "each resistor's legs, straight and bent: guide.py draws them as wires, straight as bought and bent in Step 4, as the LSM's"
    },
```

   and the colour rule's match becomes `"^LAC Resistor 1$"`. Then `build_model.py` once (guide.py rebuilds the model only when the set
   of parts changes), then `guide.py`, then `parts.html` for the picture. The generator's own model (lac-guide.glb) keeps the legs, so a
   label or eye placed on RES1 without an anchor may land on a leg that is no longer drawn: give anchors by hand (below). wirecheck skips
   a wire's own part (`tools/wirecheck.py:49-50`) and 5 mm at each end (`:20`), so the legs (tied to RES1, tips 3.96 mm under the hole
   tops) should not be reported.

2. **guide.py**, after `g.rest_at([RES1], ...)` (`LAC guide.py:240-241`):

```python
# The resistors' legs, drawn as wires so that they can be bent (Step 4), as the LSM's (LSM guide.py:159-194); the CAD's own legs leave
# the model (materials.json). Measured from lac-guide.glb: the body x 677.03 - 688.03 on an axis at y 901.15 (NAUO7: 901.27, 5.15 mm
# further to -z); each bent leg runs on from the body's end to over its hole and turns 8.0 mm straight down, its tip at y 893.15
# (3.96 mm under the holes' tops).
LEG_R, LEG_RINGS, LEG_DROP = 0.315, 0.25, 8.0
RES_LEG_ENDS = {   # per leg: where it leaves the body (0.4 mm inside its end), and the point over its hole where it turns down
    RES1: [([687.63, 901.15, 1277.13], [699.20, 901.15, 1277.36]),    # to the (-) blue rail
           ([677.43, 901.15, 1276.38], [666.18, 901.15, 1276.20])],   # to h27
    RES2: [([687.63, 901.27, 1271.98], [699.20, 901.27, 1272.21]),
           ([677.44, 901.27, 1271.23], [666.18, 901.27, 1271.05])],   # to h29
}


def legs(body, name):
    """Each leg of a resistor as a wire tied to its body: straight out, as bought, or bent through 30, 60 and 90 degrees at the point
    over its hole; every shape as long as the bent leg, so that the far end swings round rather than shrinking (LSM guide.py:166-188)."""
    straight_, bent = {}, {}
    for k, (start, corner) in enumerate(RES_LEG_ENDS[body], 1):
        wid = f'{name} leg {k}'
        g.wire(wid, 'pin', LEG_R, name=NAMES[body])
        start, corner = np.array(start), np.array(corner)
        line = W.rounded([start, corner, corner - [0.0, LEG_DROP, 0.0]], radius=1.2, spacing=0.25)
        n, run = W.length(line), float(np.linalg.norm(corner - start))
        out = (corner - start) / run
        shapes = [W.route(W.rounded([start, corner, corner + (out * np.cos(a) + [0.0, -np.sin(a), 0.0]) * (n - run)], radius=1.2, spacing=0.25),
                          a=body, spacing=LEG_RINGS) for a in np.radians([30.0, 60.0])]
        bent[wid] = [*shapes, W.route(line, a=body, spacing=LEG_RINGS)]
        straight_[wid] = W.route(W.straight(start, out, n), a=body, spacing=LEG_RINGS)
    return straight_, bent


R1_STRAIGHT, R1_BENT = legs(RES1, 'res1')
R2_STRAIGHT, R2_BENT = legs(RES2, 'res2')
g.part_picture(NAMES[RES1], wires=[dict(colour='pin', radius=LEG_R, pts=r['pts']) for r in R1_STRAIGHT.values()])   # (as bought: LSM :193-194)
```

   Step 4 becomes a pair (drop `single=True` and the `review=`; keep the `g.in_hand` lines round it, `LAC guide.py:243, 248`):

```python
g.place('Bend the legs of both 12 kΩ resistors (brown, red, black, red, brown) down at right angles, like this, so that they fit the breadboard.',
        appear=[RES1], lines=False, staged=True, wires=R1_STRAIGHT, wires_done=R1_BENT,
        labels=[dict(id=RES1, text='2x - 12 kΩ Resistor', anchor=[682.5, 903.5, 1276.8])],   # (on the body's top: the CAD's legs are not drawn)
        eye=[dict(id=RES1, anchor=[682.5, 901.2, 1274.3])],                               # (the body's -z side, towards the camera)
        frame=((_res + [0.0, RES_HOVER, 0.0]).round(1).tolist(), 28.0), look_from=BENCH_LOOK)   # (28: the straight legs span x 658.7 - 706.7)
```

   (Anchors are seated mm on the part; the player puts them where RES1 rests, `player.js:262`.) Step 6, where RES2 first appears, gets
   its legs already bent: add `wires={k: v[-1] for k, v in R2_BENT.items()} if res == RES2 else None` to the `g.place` in
   `LAC guide.py:259-264`. RES1's legs carry on from Step 4. Lee's lead-line points (`RES_LEGS`, `LAC guide.py:258`) are the legs' tips
   at y 893.1, where the drawn legs end.

---

## 2. A nut spun off and on a threaded shaft (LAC Steps 23 and 27)

### What the LSM does (`LSM guide.py:523-549`)

```python
NUT_AT = [AXIS[0], AXIS[1], 1251.0]          # a point on the button's axis (it runs along Z)
NUT_OFF = [0.0, 0.0, -95.0]
TWO_BEATS = [ZERO, ZERO, ZERO]

def nut_turns(z0, z1, sign, turns=2):
    n = 4 * turns
    return [turned([0, 0, 1], sign * 90.0 * k, NUT_AT, [0.0, 0.0, round(z0 + (z1 - z0) * k / n, 2)]) for k in range(1, n + 1)]

# off (Step 18): the nut rides on the button; its ride is a list of poses
g.place('Unscrew the nut ...', move=[BUTTON], path=TWO_BEATS, staged=True, ride={NUT: nut_turns(3.12, NUT_OFF[2], -1)}, lines=False, ...)
# on (Step 20): the nut was put away, so it comes back as a moving part with via() poses
NUT_ON = [[0.0, 0.0, -60.0]] + [via(p) for p in nut_turns(-60.0, 0.0, 1)[:-1]] + [ZERO]
g.place('Screw the nut back onto the button ...', move=[NUT, BUTTON], against=[D2, BUTTON], staged=True,
        path=NUT_ON, paths={NUT: NUT_ON, BUTTON: TWO_BEATS}, lines_at=[[AXIS[0] + 7.4, AXIS[1], 1251.2]], look_from=[1, 1, -1])
```

- **A quarter turn per pose**, the move along the axis shared out evenly (2 turns = 8 poses). The player slerps between consecutive
  poses and always takes the shorter way (`player.js:57`, `mixPose`), so each stretch must be under 180 degrees; 180 exactly can go
  either way (`round2/player_features.md:208-219`). Each pose is turned into an absolute orientation, so 0, 90 ... 720 works. The last
  pose on the way on is written as `ZERO` (720 degrees is 0): the step from 630 to 0 is 90 degrees the right way.
- **Two beats, without a pause**: a part that stays put is given a way of three stops (`TWO_BEATS`), which makes the step 1.6 s
  (`player.js:719, 725`: a step lasts as many beats as its longest way has stretches). The nut's own list is spread over the whole step:
  a riding part's in-between places play by `throughPoses()` (`player.js:82, 769`), an equal share of time each, eased over the whole
  step, unless their number equals the number of beats (`paced`, `player.js:762`). Two turns in one beat peak at 45 degrees a frame at
  60 fps and the hexagon seems to turn backwards; over two beats they peak at 22.5 (`player_features.md:244-252`). Do **not** use
  `ride_beats=True` for this: it gives every one of the 8 stretches a beat of its own (`player.js:718`).
- **Off**: the nut keeps riding (`ride=` a list, `stepgen.py:1260-1262`, written as the carry's `via`, `:1833-1835`). **On**: in the LSM
  the nut had been put away (`LSM guide.py:544`) and comes back new, so it is a moving part (`paths=`, its in-between poses `via()`,
  `stepgen.py:175-179`).
- **Which way** (`player_features.md:239-243`): a positive angle is clockwise seen looking along the axis, counter-clockwise seen from
  its tip end. The LSM's "clockwise unscrewing" (`lee_notes_2026-10-19.md:60`) is seen from the button's head, the end away from the nut:
  the same turn as counter-clockwise seen from the nut's own side.
- The arrow starts at the nut's rear face, 11 mm off the axis and 1 mm up, clear of the leads (`LSM guide.py:541-542`; Lee,
  `lee_notes_2026-10-19b.md:20, 65`).

### For the LAC

The shaft runs along +x, out through F1's front. Measured: the nut (NAUO12) x 724.23 - 726.03 (1.8 mm thick), 10.3 mm across the flats,
its middle on the axis at **[725.13, 919.53, 1235.26]** (the axis y 919.53, z 1235.26, as `SHAFT`, `LAC guide.py:436`); the thread
(radius 3.5) from x 720.5 to 728.5, then the plain shaft (radius 2.95) to its tip at x 737.83. Seen from the shaft's tip (from the
front), **counter-clockwise = positive degrees about [1, 0, 0]** (unscrewing, the nut moving +x towards the viewer), clockwise = negative
(screwing on, moving -x towards F1). That is a right-hand thread either way.

Two differences from the LSM decide the code:

- **Both steps keep the nut riding on the potentiometer** (`ride=` lists), unlike the LSM's Step 20. A moving part is taken off its carrier
  for good (`stepgen.py:1820-1821`) and ends the step at its own seat (`:1827-1828`); the LAC's nut has to end on the potentiometer, which
  is held at `BUILD`, and has to stay with it when F1 and the potentiometer are moved (Steps 29 and 46 move them with `ride=`).
- **For the two beats**, the potentiometer, F1, the washer and the knob cannot be the part that stays put: they ride too, and the
  `ride=` of later steps would no longer reach them (`stepgen.py:1829-1831`: a ride counts only for a part still riding). The
  breadboard can: it is seated and on screen, nothing rides on it by Step 22 (every jumper cap is plugged in; the LCD wires' caps
  have not appeared), and it is out of these steps' frame. This is the LSM's D4 trick (`LSM guide.py:692, 740, 749`).

```python
NUT_AT = [725.13, 919.53, 1235.26]                                  # the nut's middle, seated, on the shaft's axis (which runs along +x)
STAY = dict(move=[BREADBOARD], paths={BREADBOARD: [ZERO] * 3})      # (two beats, 1.6 s: the breadboard, seated, keeps still; LSM guide.py:529, 692)


def nut_turns(x0, x1, sign, turns=2):
    """The nut's riding poses from x0 to x1 mm along the shaft (relative to its seat), `turns` whole turns, a quarter turn each (the
    player takes the shorter way between two poses). sign +1: counter-clockwise seen from the shaft's tip (coming off); -1: clockwise
    (going on). As the LSM's (LSM guide.py:532-535), about +x."""
    n = 4 * turns
    return [turned([1, 0, 0], sign * 90.0 * k, NUT_AT, [round(x0 + (x1 - x0) * k / n, 2), 0.0, 0.0]) for k in range(1, n + 1)]


# Step 23 (in the loop at LAC guide.py:440-449, for part == NUT):
#     ride={NUT: nut_turns(DELIVERED[NUT][0], DELIVERED[NUT][0] + OFF_MM, +1)}, **STAY
#   (from x -3 to +35: 8 poses, 4.75 mm and a quarter turn each; it ends turned 720 degrees, which differs textually from where it
#   started, as player.js:769 needs; then g.put_away([NUT]) as now)
# Step 27 (in the loop at LAC guide.py:453-459, for part == NUT; the carry at ON_MM and appear=[NUT] as now):
#     ride={NUT: nut_turns(ON_MM, 0.0, -1)[:-1] + [ZERO]}, **STAY
#   (from x 60 to its seat; the last pose ZERO rather than -720 degrees, as the LSM's NUT_ON; -630 to 0 is 90 degrees clockwise)
```

The loop's other parts (knob, washer) keep `ride={part: ...}` as they are; build `ride` and `STAY` per part, e.g.
`**(dict(STAY, ride={NUT: ...}) if part == NUT else dict(ride={part: ...}))`. `lines_at` on Step 27 stays as it is: with the breadboard's
path `[ZERO] * 3` the player still draws the line from the hover pose (`player.js:195-198`). The log shows the step as `hand`, as the
LSM's are. (Spinning the nut only along the 8 mm of thread and sliding it the rest of the way would be more literal, but Lee asked for
the LSM's look, which spreads two turns over the whole move.)

---

## 3. Arrows from a chosen point (LAC Steps 23 and 24: "from the shaft's tip")

- `arrows=[dict(tail=[x, y, z], head=[x, y, z], normal=[x, y, z], part=id, width=mm)]` (`stepgen.py:1265-1268`): the points are seated mm
  on `part` (default: the first moving part), drawn where that part is in Step N (`stepgen.py:1879-1882`: `apply_pose(hover[part],
  tail)`; riding parts included, `:1826`). `normal` is the way the flat arrow faces: square to the arrow and towards the camera. Default
  width 4 mm, head 8 mm each side, head length min(0.6 L, 3.4 x width) (`core.js:303-317`). Step N only; a step with arrows has no lead
  lines (`stepgen.py:1350`).
- The LSM always starts the tail on a surface it names, not inside the part: the nut's rear face (`LSM guide.py:541-542`, z 1250.3 against
  the face at 1250.43); D10's front face below its lower edge, outside the matrix (`:750-751`); the backing's corner nearest the camera,
  45 mm long, `width=4.0` (`:279-281`).

For the LAC (`LAC guide.py:446` today starts at the part's middle + 4 mm, which is inside the shaft or the nut): give the points on the
potentiometer, so that they are drawn wherever it is held:

```python
# (from 1 mm past the shaft's tip, 30 mm along it; seated mm on the potentiometer, drawn where it is held; the face towards BUILD_SIDE)
TIP_ARROW = dict(tail=np.add(SHAFT, [1.0, 0.0, 0.0]).round(2).tolist(), head=np.add(SHAFT, [31.0, 0.0, 0.0]).round(2).tolist(),
                 normal=[0.0, 0.48, -0.88], part=POT)
#   Steps 23 (nut) and 24 (washer): arrows=[TIP_ARROW]
#   (tail [738.83, 919.53, 1235.26] seated; with the potentiometer at BUILD + PULLED it is drawn at [809.83, 954.53, 1236.36])
```

The normal is `BUILD_SIDE` (`LAC guide.py:437`) with its x part removed: [0, 0.481, -0.877]. In Step 22 the knob covers the tip (knob x
724.05 - 741.06, delivered 4.61 mm further out), so an arrow from its outer face would be `tail=[746.67, 919.53, 1235.26]`, same part and
normal (not asked for).

---

## 4. Close-ups of a small detail (LAC Step 25: the potentiometer's tab in F1's small cutout)

`inset=dict(target=, dir=, radius=, mark= | marks=[(point, half)], hide=[ids], ghost={id: alpha}, caption=, alt=, image=)`
(`stepgen.py:1269-1272, 1279-1282`; written at `:1895-1901`). Drawn once on Step Nc (or on the one view of a `single` step,
`:1904-1907`), from `dir` (assembly space), the camera `radius / sin(fov/2) x 1.05` from the target, the picture's up following the main
view's (`player.js:402-410`); the picture's half-height at the detail is radius x 1.05 / cos 22.5 = 1.14 x radius (`:418`). The red
box(es): `mark` half-width round the target, or `marks` (`player.js:414-422`). **The target and marks are in the view's assembly space,
not on a part** (`stage.toWorld`, `player.js:405, 417`: only the model's own turn is applied), so a part held away from its seat needs the
point where it is in that view. (The LSM's close-ups are all of seated parts; the LSM's Step 6 picture card has its target moved off
the stripe "to the side of the can it is on" only to steer its leader, `LSM guide.py:320`.)

How the LSM chose `dir` and `radius`:

| LSM step | inset | why |
|---|---|---|
| 14, the matrix's pins (`:467`) | `target=[613.0, 895.6, 1196.0], radius=11.0`, no `dir` (the step's camera) | the header and the label; the ring on the label, so that it is not taken for a fourth pin (`:466`) |
| 32, D10's slot (`:781-782`) | `dir=[0.15, 0.5, -0.85], radius=15.0, ghost={MATRIX: 0.12, D4: 0.25}` | along the slot, from beside it, so that the wires show lying in it and "D10" reads whole; the parts in front drawn faint (Lee, `lee_notes_2026-10-19b.md:43`; done `:76`) |
| 33, D1's four slots (`:788-789`) | `dir=[0.0, 1.0, 0.0001], radius=58.0, hide=[D6], marks=[(p, 6.5) ...]` | straight down (the 0.0001 keeps the picture's up defined), D6 left out to show what is under it, a box per slot |
| 36, a D11 tab through D1 (`:806`) | `target=[674.83, 857.0, 1166.2], radius=6.0`, no `dir` | one 3 mm tab, from the turned-over step's own side |
| LAC 55, the cable in F2's slit (`LAC guide.py:736`) | `dir=[-0.9, 0.35, -0.25], radius=14.0, mark=4.0` | |

So: `dir` looks into the feature (along a slot, face-on into a cutout), with what is in front left out (`hide`) or faint (`ghost`);
`radius` 1.5 - 3 x the feature, enough to show what it sits beside; `mark` the feature's half-size plus about 0.5 mm.

**The LAC's tab and cutout (measured):** F1's small cutout is an arc slot beside the round hole (radius 3.6), through F1 (x 720.83 - 723.83),
y 918.14 - 920.93, z 1242.23 - 1243.89 (7.0 - 8.6 mm from the shaft's axis, on its +z side). The potentiometer's tab sits in it, its end
at x 722.43 (1.4 mm under F1's front face), y 918.18 - 920.88, z 1242.61 - 1243.71. In Step 25c F1 and the potentiometer are at `BUILD`
([150, 35, 1.1]).

```python
TAB_SLOT = [723.1, 919.53, 1243.1]                                  # F1's small slot beside the hole, with the potentiometer's tab in it (seated)
# Step 25 (LAC guide.py:450-452), added:
        inset=dict(target=posed_line(BUILD, [TAB_SLOT])[0].round(2).tolist(),   # [873.1, 954.53, 1244.2]: where it is held in this step
                   dir=[0.9, 0.3, 0.3], radius=9.0, mark=2.0,
                   caption='The tab in the small slot beside the hole',
                   alt="Close-up of the front of F1: the potentiometer's little tab sits in the small slot beside the round hole"),
```

`dir` is nearly face-on (26 degrees off F1's normal): the tab's end is 1.4 mm down a 1.66 x 2.8 mm slot, so a slanting view loses it
behind the slot's wall (at 18 degrees each way about 1.2 x 2.35 mm of it shows). From the +z side the shaft is behind the slot, not in
front of it. `radius` 9 frames the slot and the threaded bush beside it (7.9 mm away). A `ghost={F1: 0.4}` would show the tab's whole
length through F1, but the potentiometer's front plate behind F1 is the same colour as the tab, so it is likely to read worse: try it
in the player only if face-on does not read.

---

## 5. Label and eye placement

The player lays out each label and eye once per view (`player.js:289-330`): by default on the side of the model with the most room nearest
its spot, a little above it so that the leader slopes (`:309-312`), or "float" near the part when there is no room (`:313`); labels on
one side are stacked in the order of their spots so that leaders do not cross (`:319-329`); never under the caption box (`:316-318`). A
label is `dict(id=, text=, anchor=[x, y, z])` (anchor seated mm on `id`; without it the generator picks a spot this camera can see,
`stepgen.py:1849-1850`, `label_anchor` `:485`), plus:

- `side=`: `'left' | 'right' | 'top' | 'bottom'` (a side of the model's box on screen) or `'up-right' | 'up-left' | 'down-right' |
  'down-left' | 'near-left' | 'near-right' | 'near-above' | 'near-below'` (beside its own spot), with `reach=` the distance as a share of the
  view's width (default 0.07) (`player.js:287-308`). Eyes take the same keys (they go through the same layout, `:292-293`).
- `ring=False`: no dashed ring at the anchor (`player.js:350`).

What the LSM does with them:

- **A hole label beside its own red lead line** (Step 3): the label's leader ends on the hole, where c16's red lead line ends, with its
  dashed ring, and the label is put to one side so that its leader comes in nearly level, **across** the (upright) red line rather than
  along it: `labels=[dict(hole_label('c16'), side='right'), hole_label('g2')]` (`LSM guide.py:294`; Lee's follow-up of 20 Oct,
  `lee_notes_2026-10-20.md:56`, done `:62`). The earlier fix, the anchor moved 1.5 mm aside with `ring=False`, was undone at Lee's
  request: he wants the ring on the hole and the two lines only not running parallel.
- **Labels under their legs** (Step 6, as Lee's capacitor picture): `side='down-left'` and `side='down-right'` (`:317`); **an eye beside
  its spot** so that its leader does not cross the part (Step 7): `eye=[dict(id=CAP, anchor=STRIPE, side='near-left')]` (`:324`).
- **Several labels on a small part without crossing leaders** (Step 14): each pin named at a different place along it (`ALONG_PIN`,
  `:461`), so the three leaders run side by side (`:465`); no eye.
- **Hole labels** anchored on the hole's top (`hole_label`, `:122-123`); in Steps 15 - 17 the label of the wire's other end is on the part
  it is in (`:480-481`).
- The PMG uses the `near-*` / `reach` forms for labels close to their spots (`PMG guide.py:528, 555, 566-567, 946`).

**For the LAC.** With the bench camera (`look_from=BENCH_LOOK`, the diagonal [0.5792, 0.5736, -0.5792]) screen-right is world
(-1, 0, -1)/√2: the front (+x: the rails, rows a - e) and column 1 (+z) are on the left of the picture, the back rows and the buzzer's
end on the right. So:

- Step 3, as the LSM's Step 3 now: both corner-hole labels on their holes with their rings, each to its own side, so that each leader
  comes in across its upright red lead line (`LAC guide.py:235` draws them straight down from the pin tips):
  `dict(text='c15', anchor=HOLES['c15'], id=BREADBOARD, side='right')`, `dict(text='g1', anchor=HOLES['g1'], id=BREADBOARD, side='left')`
  (g1 is the left of the two on screen). The LSM's Step 3 has no "Nano Board" label; if it stays, `side='top'`.
- Steps 5 and 6: `side='left'` on '(-) blue' (the rail is on the left), `side='right'` on 'h27' / 'h29': each leader then runs away from the
  resistor between them.
- Step 7: 'Real Time Clock' `side='top'`; j19 (+z of j24, so left of it) `side='left'`, j24 `side='right'`.
- Step 22, "above the knob": `side='top'` puts the label at the top of the whole model's box on screen (`player.js:311`), which with the
  base in view can be far above; `side='near-above', reach=0.1` puts it just above its own spot (`:305-308`). Give the anchor where the
  leader should end (seated mm on the potentiometer, e.g. its body's top [714.0, 928.6, 1235.3]).
- Steps 1 and 15: `side='top'` / `side='left'` (already in the working copy).

Check each in the player at 1280, 1000 and 768 px wide, as the LSM's rounds of 20 Oct did (`lee_notes_2026-10-20.md:43-44, 62`).

---

## 6. Framing the breadboard wiring steps so that the holes are easy to see

The LSM's (its breadboard is the same half breadboard, rows 2.54 mm apart; board top y 871.92, `LSM guide.py:106`):

| LSM step | camera | target over the board | radius |
|---|---|---|---|
| 3, Nano (`:296`) | `view_dir=[-0.5792, 0.5736, -0.5792]`, `frame=([638.6, 888.0, 1192.0], 50.0)` | 16 | 50 |
| 5, 12 kΩ into h3, h16 (`:303`) | `[0.5792, 0.5736, -0.5792]`, `([647.5, 886.0, 1189.5], 30.0)`: the other corner, the Nano hid the holes (Lee, `lee_notes_2026-10-19.md:16`) | 14 | 30 |
| 7, capacitor j2, j3 (`:312, 326`) | `CAP_VIEW = [0.4698, 0.5736, 0.671]` (35 degrees round from j3's side, as Lee's capacitor picture), `([652.6, 885.0, 1172.0], 28.0)` | 13 | 28 |
| 9, 330 Ω a11, a19 (`:331`) | `[-0.5792, 0.5736, -0.5792]`, `([624.5, 886.0, 1203.5], 30.0)` | 14 | 30 |
| 11 - 12, pins i2, i3 (`:441-443`) | `[-0.3282, 0.6298, -0.704]`, `([644.3, 895.7, 1180.6], 38.3)`: solved from Lee's screenshot | 24 | 38.3 |
| 13, pin b19 (`:443`) | `[-0.5792, 0.5736, 0.5792]`, `([627.0, 892.0, 1213.6], 34.0)`: the opposite corner, beyond row a | 20 | 34 |
| 15 - 17, sockets on the matrix, holes labelled (`:475`) | `[-0.36, 0.45, -0.82]`, `([643.0, 906.0, 1203.0], 48.0)`, one camera for the three | 34 | 48 |
| 21 - 22, button leads j5, j16 (`:578-579`) | red `[0.5792, 0.5736, -0.5792]`, `([645.0, 884.0, 1209.0], 40.0)`; black from Lee's screenshot `[0.6491, 0.6967, -0.3055]`, `([653.7, 892.4, 1204.6], 35.5)` | 12 - 20 | 35.5 - 40 |

How: radius 28 - 50 mm (the LAC's wiring steps are 72 - 110 today: `LAC guide.py:330, 375, 461, 521, 583`), the target 12 - 24 mm over
the board, between the holes and where the part starts; **a camera per wire** (`PIN_CAMERA[w]`, `LEAD_CAMERA[c]`, passed with `**`) from
whichever corner leaves the hole clear (b19 from the other corner, `:439-443`). And, what lets the frame be tight, **each part starts close
to its hole**: the jumper pins are held 30 mm over their holes (`PIN_HOVER`, `:235`; `rest_at` `:391-393`; all appearing in the first pin
step, `:447`), the sockets 15 mm off their pins (`SOCKET_OFF`, `:222`), the button's leads laid straight back 50 mm (`:492`); the ribbon
has its own step and is put away before the wire steps (`:382-385`).

There is no automatic framing helper in the LSM: `r1_camera()` (`:113-116`) only writes `view_dir` + `frame`; cameras came from Lee's notes
("closer", "the other corner") and from his screenshots, solved with `player/js/camsolve.js` (`_cam.target`, `_cam.solveDir`,
`_cam.solveFrame`, usage at `camsolve.js:4-8`), checked with `_dev.show(...)` / `_dev.look(part, dir)`. The generator's own close-up is
`focus=[ids]` (+ `focus_pad`, default 1.6; `stepgen.py:1245-1246, 554-557`): it frames those parts where they hover and where they seat.
`one_off_camera=True` (`:1283-1285`) keeps a pinned camera from changing the next steps' choice.

**For the LAC.** A helper that frames as the LSM did:

```python
def hole_camera(points, view_dir, up=12.0, margin=10.0, least=25.0):
    """A camera close on the holes a step's parts go into, as the LSM framed its breadboard steps (target 12 - 24 mm over the board,
    radius 28 - 50 mm): the middle of the holes raised `up` mm, the radius to the farthest hole plus `margin`."""
    p = np.asarray(points, float)
    c = (p.min(0) + p.max(0)) / 2 + [0.0, up, 0.0]
    return dict(view_dir=view_dir, frame=(c.round(1).tolist(), round(max(least, float(np.linalg.norm(p - c, axis=1).max()) + margin), 1)))
# holes: [CAPS[cap]['top'][0], BB_TOP, CAPS[cap]['top'][2]] for the step's caps
```

| LAC step | holes | frame from `hole_camera` |
|---|---|---|
| 3, Nano | as the LSM's Step 3 (the same Nano: columns 1 - 15, USB at +z; the LSM's camera mirrored to the a side) | `view_dir=[0.5792, 0.5736, -0.5792], frame=([676.5, 913.1, 1324.3], 50.0)` |
| 5, RES1 | rail (699.2, 1277.30), h27 | `([682.7, 909.1, 1276.7], 30.4)` |
| 6, RES2 | rail (699.2, 1272.22), h29 | `([682.7, 909.1, 1271.6], 30.4)` |
| 9, black | i23, (+) | `([680.2, 909.1, 1285.6], 30.4)` |
| 10, green | (-), i24 | `([681.4, 909.1, 1284.3], 31.4)` |
| 11, purple | a8, i22 | `([676.5, 909.1, 1306.5], 35.0)` |
| 12, blue | a9, i21 | `([676.5, 909.1, 1306.5], 33.2)` |
| 13, white | a14, (-) | `([694.2, 909.1, 1309.7], 25.0)` |
| 14, dark red | a12, (+) | `([692.9, 909.1, 1312.3], 25.0)` |

The catch: the LAC's jumper caps start lying on the table in front of the board (`FRONT_X = 745`, `LAC guide.py:277`), 45 - 85 mm from their
holes, so a frame that keeps their start in view needs a radius of 61 - 69 (computed for Steps 9 - 14), barely closer than today's 74
(the switch's, potentiometer's and buzzer's caps start further out still: "30 - 34 wires fly off screen"). Getting the LSM's 25 - 35 means
opening each wire step with that wire's caps already held over their holes, as the LSM's pins (after the ribbon step, `g.put_away(caps)`;
then per wire `g.rest_at([ca, cb], UP)`, `appear=[ca, cb]`, `move=[ca, cb]`, `path=[UP, ZERO]`, `wires={f'jumper {colour}': done}`: a route
tied to both caps follows them, so the plugged route is drawn 18 mm up while they are held), or letting the caps glide from the table
into a tight frame as Step N opens. Steps 12 and 14 ("obstructed by other wires") want a camera of their own from the corner where the
earlier wires are behind the holes, as the LSM's b19 (pick it with `_dev.look`).

---

## 7. Part names and label text for resistors

- `NAMES`: `R12K: '12 kΩ Resistor', R330: '330 Ω Resistor'` (`LSM guide.py:47`), the same names in the parts list's group test (`:59`); the
  legs' wires carry the resistor's name for hover (`:172`). Lee wrote "12kOhm" in his LSM notes (`lee_notes_2026-10-19.md:18`) and the
  guide shows "12 kΩ"; only the plain-text README spells it "12 kOhm" (`LSM README.txt:53-54`). The LAC working copy already has
  `'12 kΩ Resistor'` (names, parts-list group, captions).
- Captions name the value and the bands: `'Bend both legs of the 12 kΩ resistor (brown, red, black, red, brown) straight down.'` (`:298`),
  `'Push the 12 kΩ resistor into h3 and h16.'` (`:301`). The LAC's resistor has the same bands (section 1).
- Labels: `labels={R12K: '12 kΩ Resistor'}` (`:299`). The LSM never shows two of one resistor at once, so it has no "2x". Left to itself
  the generator writes one label per name with a count, `"2x 12 kΩ Resistor"`, without a dash (`stepgen.py:1500`); Lee's
  `'2x - 12 kΩ Resistor'` has to be given by hand (`labels=`), as in the working copy. Quantity cues in the rulebook: "Nx"
  (`docs/cadasio-patterns.md:314`).
- Parts list picture: the straight-legged resistor (section 1). Not from the LSM, but nearby: the potentiometer "backwards in the Parts
  List" is a picture direction, set as the LCD's is (`PART_VIEWS`, `LAC guide.py:133`; the LSM turns its shelves with `{'roll': 180}`,
  `LSM guide.py:89`), e.g. `'Potentiometer': {'dir': [0.8, 0.45, 0.4]}` to see it from the shaft's end (to be checked in `parts.html`).

---

## 8. Leads on a part that turns, flips or is carried

What the LSM uses (all with the LED matrix's three wires, which ride on the matrix as it is lifted, turned and lowered):

- **Each shape drawn for where its end parts are**: `W.route(..., a_at=pose, b_at=pose)` (`wires.py:22-24`); the socket's pose composed from
  the matrix's (`f_pose`, `LSM guide.py:225-232`; `jumper`, `:265-266`).
- **A shape per stop, the step as many beats as shapes**: Step 26 (`:692-696`) gives the matrix four places (`ride={MATRIX: [P_UP_BESIDE,
  P_MID, P_UP_OUTSIDE, P_OUTSIDE]}`), the wires four routes (`wires_done={k: [UP_BESIDE[k], MID[k], UP_OUTSIDE[k], OUTSIDE[k]]}`), and D4
  a way of five stops that stays put (`paths={D4: [ZERO] * 5}`): four beats, the matrix and its wires keeping pace stop by stop (`paced`,
  `player.js:758-762, 769, 774-777`). Step 30 does the same over two beats (`:740-741`). `ride_beats=True` does it without the stationary
  part, giving each stretch of the riding parts' longest list a beat (`player.js:714-719`; the PMG's display).
- **A via pose with a route at the same share**: Step 32 (`:775`), `path=[P_HELD, via(P_HALF), ZERO]` with `wires_done=[HALF, SEATED]`;
  P_HALF is half way (28.6 mm, then 28.0), so the wire's two legs (equal shares of the eased progress, `player.js:159-160`) keep pace with
  the matrix's path.
- **`tail_from`** (`wires.py:36-39`; `jumper(tail=...)`, `LSM guide.py:250-253, 264`): changing between two routes that both have it, the
  run up to that point is matched by distance from the first end and the rest by distance from the last (`player.js:167-176`), so the run
  in the box stays put and the run under the moving matrix moves with it (`:565-566, 667-668, 733-734, 757-758, 770-771`).
- **`b_from`** (`follow=6.0`, `fixed=`: `:246-249, 260-263`): only the last 6 mm follow the far part; the middle is left to the change of
  shape, so that a blend of two shapes that each lie clear stays clear.
- **`stretch`**: `False` for shapes that share their start (matched by distance from the pin, `:243-245`); `True` for a lead whose length
  does not matter (stretched evenly, and **carried by its ends' moves only, not turned with them**, `player.js:110-113, 161-163`).
- **Turn the part where its leads have room**: the matrix is turned on its way out over D4 (Step 26), so that Step 30 is only a lift and
  a move (Lee, `lee_notes_2026-10-19b.md:39`; done `:74`).
- **Angled, then moved, then home**: D3 (`:700-706`), `path=[turned([0, 1, 0], TILT, HINGE, _in), turned([0, 1, 0], TILT, HINGE), ZERO]`:
  tilted, slid in along its own tilted length, swung shut. The pattern for the LCD into F9's and F8's notches (LAC Steps 50 - 51), with
  `wires_done` a route per stop.
- **Wires without kinks**: the LSM's `smooth()` (`:127-134`): a spline through a few points (`W.smooth`, no corners) with a short straight
  run at each end, resampled every 0.75 mm; `W.route(spacing=)` for a short lead with a tight bend (the buzzer's red lead's kink may be
  either; a CAD centre line can also be eased with `W.smoothed`, `wires.py:76`).
- Checked with `tools/motioncheck.py <kit> [views]` (19 moments of each move) and `tools/wirecheck.py` (at rest).

**For the LAC's Step 29** (F1 laid face down: "drop the middle of the animation, smoother flip"; `LAC guide.py:469-473`). Today:
`ride={F1: [ASIDE, FLAT_BESIDE], POT: [...]}, ride_beats=True`: two beats with a stop at ASIDE, then the whole 180-degree turn of
`F1_flat_beside` (about (-1, 1, 0)/√2) in one slerp, which may go either way round and, measured, dips F1 31 mm under the table (F3's
underside, y 884.6). Straight from `BUILD` to `FLAT_BESIDE` without the carry past the end is not possible: with F1's middle on a straight
line, F1 passes through the case's corner (x < 720.8, z < 1369.1) for about an eighth of the way (measured, even raised 80 mm). So keep the
way past the end but play it as one movement (no `ride_beats`: no stop), turn in 60-degree stretches, raise F1 40 mm while it turns
(its lowest point then y 889.0, never inside the case), and give it two beats with the breadboard trick:

```python
F1_MIDDLE = [722.33, 919.53, 1289.87]                               # F1's middle, seated (its box x 720.83 - 723.83, y 881.43 - 957.63, z 1207.29 - 1372.45)


def part_way(p0, p1, f, pivot, lift=0.0):
    """A pose a share f of the way from p0 (a move) to p1 (a turn): f of p1's turn about the part's middle, the middle moved in a
    straight line between the two, raised `lift` mm at half way."""
    c0, c1 = apply_pose(p0, [pivot])[0], apply_pose(p1, [pivot])[0]
    c = c0 + (c1 - c0) * f + np.array([0.0, lift * 4.0 * f * (1.0 - f), 0.0])
    return tidy(turned(p1['r'][:3], p1['r'][3] * f, pivot, (c - np.asarray(pivot, float)).tolist()))


# Carried 112 mm, 112 mm (still upright), then turned 60, 120, 180 degrees: five stretches of 84 - 112 mm each, an equal share of the
# time each (player.js:82), so that the pace stays even. The turned poses come out as
#   turned([-0.707107, 0.707107, 0.0], 60.0, F1_MIDDLE, [68.8, 55.41, 222.95]) and (..., 120.0, ..., [-12.41, 40.26, 220.89]).
LAY_DOWN = [np.add(BUILD, [0.0, 0.0, 112.0]).tolist(), ASIDE] + [part_way(ASIDE, FLAT_BESIDE, f, F1_MIDDLE, lift=40.0) for f in (1 / 3, 2 / 3)] + [FLAT_BESIDE]
g.place('Lay F1 face down beside the end of the base, as shown, with the potentiometer at the end nearer the breadboard.',
        ride={F1: LAY_DOWN, POT: LAY_DOWN}, move=[BREADBOARD], paths={BREADBOARD: [ZERO] * 3}, lines=False, eye=[F1],
        wires_done={f'pot {c}': pot_flat_lead(c, cap, e) for c, cap, _, e, _ in POT_LEADS}, view_dir=..., frame=...)
```

and in `pot_hanging` (`LAC guide.py:427-432`) drop `stretch=True`. The hanging lead and the flat one are the same straight 50 mm lead in
the potentiometer's frame; without `stretch` the player carries each route rigidly with the potentiometer and its cap (they move
together), so the leads simply turn with F1 and need no in-between routes. With `stretch` on either route (as now) they are carried by
their ends' moves only, not turned (`player.js:110-113, 161-163`), and bend mid-flip. (The change into the plugged routes, `pot_plugged`,
`stretch=True`, `LAC guide.py:485`, is unaffected: one route with `stretch` is enough for that blend.) F1 sweeps x 590 - 874, z 1208 -
1597 in this step, so a frame holding all of it is about 250 mm in radius; "too zoomed out and off-centre" needs a choice between the
whole way and the landing (the base's end and F1 lying, about [660, 905, 1460], radius 110).

**For Step 46** (F1 carried round to the far end, "pot wires through F9 and F1"; `LAC guide.py:678-679`): it already has `ride_beats=True`
and two stops, but both wire routes are the same (`[POT_OTHER[c], POT_OTHER[c]]`), so between start and end the leads blend straight
through F9 (stood up in Step 45). As the LSM's Step 26: draw the first route for F1 at its middle stop (`compose(FRONT_OUT, F1_MID)`), from
the plugged holes up and over F9's top (its tabs' tops are at y 957.84; the LSM keeps its wires 2.5 mm over D4's top edge, `D4_TOP`,
`LSM guide.py:651`, in `over_d4`, `:654-668`), and give both routes `tail_from=` at the point where they leave the breadboard area, so that
the plugged run stays put while the rest follows F1; then `tools/motioncheck.py "LAC Build Instructions"` on that step.

---

## Arguments used (stepgen.py / wires.py / player.js)

| argument | where | used for |
|---|---|---|
| `turned(axis, degrees, at, t)` | `stepgen.py:122-124` | the nut's quarter turns, F1's flip, D3's tilt |
| `via(pose)` | `stepgen.py:175-179` | a pose passed through without a stop (the LSM's nut on, Step 32) |
| `carry(ids, by, pose, appear)` / `rest_at` | `stepgen.py:715-729` | the nut riding on the potentiometer; caps held over their holes |
| `place(ride={id: [poses]})` | `stepgen.py:1260-1262, 1829-1835`, `player.js:82, 769` | the nut off and on, F1 laid down |
| `paths={id: [ZERO] * n}` (beats) | `stepgen.py:1253-1256, 1299-1300`, `player.js:719, 725` | two beats for the nut and the flip |
| `ride_beats=True` | `stepgen.py:1290-1293`, `player.js:714-719` | a beat per in-between place (not for 8 quarter turns) |
| `wires=`, `wires_done=[via..., final]` | `stepgen.py:1247, 1257-1259, 1893` | straight legs, then the bend through 30 and 60 degrees |
| `W.route(a=, b=, a_at=, b_at=, b_from=, stretch=, spacing=, tail_from=)` | `wires.py:16-57` | legs (`spacing`), leads that turn (`stretch` off), carried runs (`tail_from`, `b_from`) |
| `W.rounded`, `W.straight`, `W.length`, `W.smooth` | `wires.py:60-62, 102-121, 140-150, 197-200` | the legs' shapes |
| `arrows=[dict(tail, head, normal, part, width)]` | `stepgen.py:1265-1268, 1879-1882`, `core.js:303-317` | arrows from the shaft's tip |
| `inset=dict(target, dir, radius, mark, marks, hide, ghost, caption, alt, image)` | `stepgen.py:1269-1272, 1279-1282, 1895-1901`, `player.js:389-422` | the tab in F1's slot |
| labels / eyes `dict(id, text, anchor, side, reach, ring)` | `stepgen.py:1235-1237, 1491-1503`, `player.js:287-330, 350` | labels off parts and lead lines |
| `frame=(target, radius)`, `view_dir=`, `look_from=`, `focus=`, `one_off_camera=` | `stepgen.py:1245-1251, 1283-1285, 543-621`; `camera_eye` `:467-470` | close frames on the holes |
| `staged=True`, `single=True`, `g.part_picture(wires=)` | `stepgen.py:1242, 1275-1276, 742` | the resistor alone; its picture with straight legs |
