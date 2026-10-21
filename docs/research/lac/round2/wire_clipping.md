# LAC round 2: wires clipping through each other during installation

Lee's notes (21 Oct 2026): Step 13 white through blue and purple; Step 14 dark red through blue and purple; Step 32 the
potentiometer's black lead through its tan lead; Steps 36 - 37 the LCD wire through the green and black jumpers, its path
"crazy and bent terribly / randomly"; Step 38 teal through purple and yellow; Step 39 blue through purple, yellow and teal.

Read-only study (no project file changed, nothing regenerated, nothing committed).

## Summary

| Step | What passes through what | Why | Fix (tested on a patched steps.json, motioncheck with parts, 37 moments) |
|---|---|---|---|
| 13 | white jumper through the blue (0.25 mm) and purple (0.29) at 0.55 - 0.65 of the push; the white's cap held up stands in the blue | the CAD's purple and blue run 25 - 30 mm along row a, right over a12 and a14 (the blue 0.95 mm off a14's axis, 13 mm over the cap); the CAD white leaves a14 under them (1.6 mm from the purple); the caps are lowered 18 mm straight down | the white as a low arch like the dark red's (8 mm, bowed -z 3 mm), both caps slid in 14 mm from the front 5 mm up, then pushed down: **0 problems** |
| 14 | dark red through the blue (0.31) and purple (0.56) at 0.50 | the same: the dark red's arch lies 8 mm under them and is lowered from 18 mm up | a12 cap from the front, (+) red cap along the rail from +z (the white's cap stands in front of it), 5 mm up, then down: **0 problems** |
| 32 | potentiometer black through the tan (0.24 mm at 0.60) | the tan's hump (y 919.5) crosses over the black's run (y 915) 17 mm from its cap; held 18 mm up the black's run rises through it | the black's last stretch lowered under the hump (911.9) and held 5 mm up: **0 problems**, nothing new elsewhere |
| 36, 37 | GND / VCC wires through the green and black jumpers (0.16 - 0.26 mm; the caps 0.3 - 0.9 mm into them) | the CAD's GND / VCC holes (k = -2) lie under the green's and black's legs (1.24 / 0.55 mm from the holes' axes) and their wires thread under the legs; nothing can come down onto them | GND / VCC into the same rails at k = +2 / +4 (z 1290.00 / 1295.08), 14 mm straight up and over into the CAD's run: **no touches with any jumper** |
| 37 - 39 | each LCD wire through the ones put in before it (0.09 - 0.65 mm), in the push | the whole run to F9's edge (60 - 114 mm, `b_from`) rides rigidly on the cap, lifted 18 mm and lowered; the CAD stacks the four with the earliest on top (y 939.7 / 937.3 / 935.1 / 933.8 at F9's edge) | a held shape per wire (`a_at=UP`) and a done copy paired from the join (`tail_from`), so only the cap and the bit by it move: **no touches between LCD wires in the push** |
| 36 - 39 | "crazy, bent randomly" | the lying lane's hairpin and drop: 3 - 4 bends of 17 - 24 deg/mm, 1.5 - 2 x the seated wire's turning; beat 1 blends a 66 mm straight line into the 130 - 181 mm route (half way: 586 degrees of turning in 117 mm) | smoother lanes: 10 - 12 deg/mm, 440 - 532 degrees in all |
| 36 - 39, left | wires through the potentiometer's leads on the way from the table (0.14 - 0.90 mm, beat 1); the teal's / blue's caps brushing the a8 / a9 jumpers (0.36 - 0.90 mm, 3 frames); blue / teal 0.27 mm at the end of beat 1 | the ribbon (Step 35) lies under the potentiometer's leads; the carried run arrives from in front and below | needs Step 35's new place (Lee asked for it) and a beat-1 route over the leads: see "What is left" |

Whole guide, wires only (19 moments, all 96 views with motion): 49 touches now, 26 with every fix here; none new.

## How this was checked

- `tools/motioncheck.py` (19 moments, `--trace`), one run at a time on the committed `steps.json` (1b1bc68): Steps 13c, 14c, 32c,
  36c - 39c. Peak memory 380 MB.
- A scratch copy of motioncheck (`scratchpad/clip/mc.py`: the same code, plus `--noparts` (wires only, no model), `--moments N`,
  `--dump` of every wire's centre line at each moment). The fixes below were tried by patching a copy of steps.json the way the
  proposed guide.py change would write it (routes built with the guide's own `arch` / `into_hole` / `W.smooth`, copied into
  `scratchpad/clip/common.py`) and running motioncheck on it, with parts, 37 moments; and the whole guide wires-only (all 96 views
  with motion) before and after, to see what else a shape change touches.
- Bends: turn of the tangent over a 3 mm window, per mm (deg/mm), on the routes resampled every 0.5 mm. For scale: a CAD jumper's
  arch peaks at 10 - 13 deg/mm; 20 deg/mm is a bend of 2.9 mm radius in a 1.25 mm wire.
- Steps are named as the player lists them (Step 13 = views 27/28 of steps.json).
- Line numbers are guide.py as committed in 1b1bc68. While this was written the working copy was being changed elsewhere (the cameras of
  Steps 16 - 18 and 30 - 32: `SWITCH_CAMERA`, `POT_CAMERA`), which shifts lines after 470 by 2 - 4; none of the code proposed here
  touches those lines, and the Step 32 fix does not depend on the camera.

## Steps 13 and 14: the white and dark red jumpers through the purple and blue

**What passes through what.** motioncheck 13c: white and blue centre lines 0.25 mm apart at 0.55 of the move, near
[690.3, 918.1, 1308.7]; white and purple 0.29 mm at 0.65, near [692.5, 919.8, 1308.1]; and at the start (0.05) the blue wire runs
0.59 mm into the white's a14 cap held at UP. 14c: dark red and blue 0.31 mm at 0.50 near [689.9, 917.2, 1314.5]; dark red and purple
0.56 mm at 0.50 near [691.5, 918.4, 1315.2]; the blue 0.67 mm into the a12 cap at 0.05.

**Why.** The CAD's purple (NAUO27, a8 -> i22) and blue (NAUO24, a9 -> i21) do not cross straight over the Nano: they rise out of
a8 / a9 and run 25 - 30 mm along -z right over row a (x 689.4 - 692.2, y 913 - 920), only turning over the Nano at z ~1296. So they
pass directly over a12 and a14, the holes of the next two wires: over a14 the blue is at (690.2, 918.2), 0.95 mm off the hole's axis,
13 mm over the cap's top (905.11); the purple at (692.1, 919.6). Each jumper step holds both caps 18 mm straight over their holes
(`UP`, guide.py:403-406) and pushes them down; the jumper's route is tied to its caps (`stretch`), so the whole wire is lowered 18 mm:
- held at UP, the a14 / a12 cap (y 911 - 923, x 688.4 - 690.1) already stands in the blue (whose tube spans x 689.6 - 690.8 at y 918);
- the CAD's white arch (NAUO29) leaves a14 leaning +x *under* the blue and purple (seated, 2.72 mm from the blue, 1.6 mm from the
  purple), so any upward offset closes that gap: held 1 mm up it is 1.14 mm from the purple, 2 mm up 0.68, 4 mm up 0.15. The cap's pin
  goes 4 mm into the board, so no way in that ends with a straight 4 mm push can miss the purple with this shape;
- the dark red (the guide's own low arch, top 909.2) lies 8 mm under the blue/purple; lowered from 18 mm up it passes through them.
(No motion of the dark red through the white: their nearest approach during the 18 mm descent is 2.07 mm, because the CAD white bows
-z to z 1308.2 over the (+) rail.)

**Fix (tested).** Draw the white as a low arch like the dark red's, bowed away from the dark red's (+) rail hole, and bring both wires
in low from the front, under the purple and blue, then push them 5 mm down:

```python
# JUMPERS_6 (guide.py:54): the white's CAD body is no longer used
    ('white', ('NAUO28', 'a14'), ('NAUO15', '(-) blue'), None),     # (a low arch, under the purple and blue: JUMPER_ARCH)

# guide.py:354-358, jumper_done: per-wire arches
JUMPER_ARCH = {'dark_red': (8.0, (0.0, 0.0, 3.0)),                  # (over the (+) rail by the clock module, bowed to +z)
               'white': (8.0, (0.0, 0.0, -3.0))}                     # (under the purple and blue over row a, bowed to -z, clear of
                                                                     # the dark red's (+) red hole: Lee, 21 Oct 2026)
def jumper_done(colour, ca, cb, key):
    """A jumper's route plugged in: the CAD's, or a low arch (JUMPER_ARCH) for a wire that has to go in under others."""
    if colour in JUMPER_ARCH:
        height, shift = JUMPER_ARCH[colour]
        line = arch(wire_at(ca), wire_at(cb), height, shift=shift)
    else:
        line = cad_line(key, ca)
    return W.route(line, a=ca, b=cb, stretch=True)

# Each cap's way in for a wire that goes in under wires already in (the CAD's purple and blue run over row a, over a12 and a14):
# slid in 14 mm from the front 5 mm up, then pushed down. The dark red's (+) red cap comes along the rail from +z instead: the white's
# (-) blue cap stands right in front of it (z 1310.35 / 1310.36).
FRONT_LOW, LOW = [14.0, 5.0, 0.0], [0.0, 5.0, 0.0]
JUMPER_WAYS = {'white': {'NAUO28': [FRONT_LOW, LOW, ZERO], 'NAUO15': [FRONT_LOW, LOW, ZERO]},
               'dark_red': {'NAUO30': [FRONT_LOW, LOW, ZERO], 'NAUO31': [[0.0, 5.0, 14.0], LOW, ZERO]}}

# jumper_run (guide.py:401-406):
    for k, (colour, (ca, la), (cb, lb), key) in enumerate(jumpers):
        done = jumper_done(colour, ca, cb, key)
        ways = JUMPER_WAYS.get(colour, {ca: [UP, ZERO], cb: [UP, ZERO]})
        for c in (ca, cb):
            g.rest_at([c], ways[c][0])
        g.place(..., paths=ways, ...)       # (the rest as now)
```

Measured on a steps.json patched this way (routes as `arch()` writes them; paths as above):
- motioncheck with parts, 37 moments: Steps 13c and 14c, **0 problems**.
- The white's apex 909.13 at (695.5, 1307.1) (the dark red's: 909.21). Held 5 mm up it is 4.48 mm from the blue and 5.82 mm from the
  purple (centre lines); seated 2.35 mm from the dark red.
- The whole guide, wires only, before / after: 49 / 42 touches. Gone: the four above, and three later ones the CAD white had with the
  potentiometer's leads (46c white / tan 0.88 mm; 52c white / red 0.46, white / tan 0.55). None new. (A white 9.5 mm high instead
  touches the tan's way in Step 46 - 51 at 0.94 mm; 7.0 or 8.0 are both clean.)
- The caps' starting places stay inside each step's camera (farthest corner 24.3 mm from the target of a 26 mm frame in Step 13,
  19.6 in Step 14).

## Step 32: the potentiometer's black lead through its tan lead

**What passes through what.** motioncheck 32c: black and tan centre lines 0.24 mm apart at 0.60 of the push, near
[705.7, 919.4, 1334.0] (traced: no blend, the black's own route 49 skinned with its cap moving).

**Why.** The path search behind `POT_WAY` (guide.py:599-601) laid the tan (Step 31) over the black's way: the tan rises to a hump of
y 919.5 at x 700 - 708 (z 1334) and the black runs under it at y 915 - 916 (z 1331 - 1334), crossing under it in plan at x ~705.
Seated they are 4.07 mm apart (centre lines, at [701.2, 916.0, 1331.7]). The black is installed after the tan and is held 18 mm over
its hole (`UP`); its route (`stretch`, no `b_from`) carries the lead near the cap almost wholly with the cap (weight 0.98 at the
crossing, 17 mm from the cap), so held up, its run under the tan is lifted 18 mm through the tan and comes back down through it.
The largest lift that clears the tan is 2.8 mm, less than the 4 mm the pin needs to come out of the hole.

**Fix (tested): lower the black's last stretch under the tan and hold it 5 mm up.**

```python
# guide.py:601, POT_WAY['black']: the last three controls lowered under the tan's hump (it was 915.0 throughout)
             ..., [715.9, 915.0, 1338.3], [712.0, 913.8, 1336.9], [708.6, 912.6, 1335.4], [705.2, 911.9, 1333.8]]}
POT_ABOVE = {'black': 6.0}              # (straight down into its hole from 6 mm over the cap's top, not 10: its run stays under the tan)
POT_HOLD = {'black': [0.0, 5.0, 0.0]}   # (held 5 mm over its hole, under the tan's hump: 18 mm up its lead rose through the tan)

# pot_plugged (guide.py:604): an `above` for into_hole
def pot_plugged(colour, cap, exit_, f1_pose, way, shared=None, above=10.0):
    ...
    line = into_hole(cap, e, d, way, above=above)[::-1]

# the loop (guide.py:618-624)
    done = pot_plugged(colour, cap, exit_, F1_DOWN, POT_WAY[colour], above=POT_ABOVE.get(colour, 10.0))
    g.place(..., move=[cap], path=[POT_HOLD.get(colour, UP), ZERO], ...)
```

Measured (patched steps.json): Steps 32 and 32c with parts, 37 moments: **0 problems**. Seated, black to tan 4.75 mm (centre lines);
held 5 mm up, 1.98 mm. The whole guide wires-only: the two black/tan touches of Steps 32 and 32c gone, nothing new (49 -> 47). The
black's riser then turns into its drop at 29 deg/mm (the current one: 32 deg/mm), at the cap's top. The hold can go to about 8 mm if
the black's last stretch is lowered to y 909 instead (`above` 4.0); 18 mm is not possible while the black runs under the tan.

*Alternative, for an 18 mm hold like the other two leads (tested, not recommended yet):* lay the black over the tan instead (tan flat
at y 915.0 from x 731.7 to 696.6, ending [693.2, 915.8, 1333.2]; black rising from [715.9, 916.0, 1338.3] through [712.0, 917.4,
1336.9], [708.6, 918.6, 1335.4], [705.5, 919.3, 1333.8], [703.0, 919.6, 1332.4] into a drop with `above` 14.0). Step 32c is then clean
with `UP`, but in Step 46 (F1 moved aside) the tan's blend to its aside route sweeps across the black's now taller riser (new touch,
0.64 mm at 0.30 near [699.7, 914.5, 1330.4]). Step 46 has six other touches already (pot tan through the black and green jumpers, the
pot red, the LCD purple and yellow, the switch tan: all in the current guide) and wants its own rework; this variant belongs with it.

## Steps 36 - 39: the LCD wires

### What passes through what (motioncheck, parts, the committed steps.json)

Each step has two beats: beat 1 (0 - 0.5 of the move) the male cap goes from the table to 18 mm over its hole (`UP`) while the female
goes 15 mm short of its pin (`F_OFF`), and the wire changes from the straight line on the table to its lying route; beat 2 (0.5 - 1)
both are pushed home (`wires_done=[done, done]`, guide.py:897).

| View | Touch (centre lines, or a wire into a cap) | When | Which beat, what |
|---|---|---|---|
| 36c | green jumper into the purple's cap NAUO82 0.44 mm; green / purple 0.16 mm near [700.4, 924.4, 1280.2] | 0.40 | end of beat 1: the cap and wire arrive over the (-) hole under the green's leg |
| 36c | black / purple 0.22 mm near [697.0, 922.9, 1280.1] | 0.80 | beat 2: the purple pushed down under the black's leg |
| 36c | purple / pot tan 0.59 mm near [706.1, 919.4, 1334.0] | 0.25 | beat 1, half way from the table |
| 37c | yellow's cap NAUO84 hit by the purple (0.92 mm), black (0.78), green (0.30); purple / yellow 0.09, black / yellow 0.26, green / yellow 0.76 | 0.35 - 0.80 | both beats, at the (+) hole under the black's leg |
| 38c | LCD purple / teal 0.11 mm near [688.5, 939.8, 1363.8]; teal / LCD yellow 0.17 near [685.9, 936.7, 1359.4] | 0.55, 0.85 | beat 2: the teal held up and pushed down under the purple and yellow at F9's back edge |
| 38c | purple jumper into the teal's cap 0.21 mm; teal / pot tan 0.75 | 0.40, 0.25 | beat 1 |
| 39c | blue / LCD teal 0.43, blue / LCD purple 0.44 near [680.6, 932.3, 1329.2], blue / LCD yellow 0.65 | 0.70 - 0.85 | beat 2 |
| 39c | blue jumper into the blue's cap 0.32 mm; blue / pot red 0.18, pot black 0.35, pot tan 0.74 | 0.25 - 0.40 | beat 1 |

### Why

1. **The whole run to F9's edge is lifted 18 mm with the cap.** Every LCD route is tied to its male cap with `b_from` = the length of the
   shared run from the breadboard round F9's back edge (`lcd_lead`, guide.py:847-852: purple 113.5 mm, yellow 111.4, teal 61.6,
   blue 59.9): that whole run moves rigidly with the cap (player.js skinned: no weight on the far end before `b_from`). Held at `UP`
   the run is 18 mm up along its whole length (the in-between shapes are 187 - 193 mm long, top at y 957.7, against 181 mm and 939.9 at
   rest), and the push brings it down 18 mm through whatever lies over it.
2. **The CAD's four wires are stacked in the reverse of the order they go in.** Where they come round F9's back edge the head ends are
   one over the other: purple y 939.70, yellow 937.31, teal 935.13, blue 933.75 (x 687.3 - 688.9, z 1360.4 - 1361.6); over the Nano they
   converge the same way (z 1350: purple (677.8, 937.2), yellow (678.3, 934.0), teal (682.1, 930.4), blue (681.6, 927.3)). Each later
   wire's run lies 1.3 - 3.2 mm under an earlier one, so lifting it 18 mm passes it through them (Steps 38, 39).
3. **The CAD's GND and VCC wires thread under the black and green jumpers.** Both go into the rails at k = -2 (z 1279.84 / 1279.85),
   under the legs of the black (i23 -> (+) red) and green ((-) blue -> i24) jumpers, which lean -z over those very holes: the green's leg
   passes 1.24 mm from the GND hole's axis at y 925.3 ([700.4, 925.3, 1279.6]), the black's 0.55 mm from the VCC hole's at y 924.1
   ([696.7, 924.1, 1279.3]). Seated, the purple passes 1.34 mm under the black's leg (18 mm from its cap), the yellow 1.82 mm. In plan
   both holes lie inside the loops of the two jumpers, so no way of putting either wire in from above (or from the side, low) misses
   them: any lift of the first 20 mm reaches the black's leg. (Steps 36, 37: Lee's green and black.)
4. **Beat 1 blends two unrelated shapes, and the table is under the potentiometer's leads.** The wire changes from the straight 66 mm
   line on the table to the 130 - 181 mm lying route, pairing points by share of length (`stretch` on the table route, player.js
   drawWires), with the far route carried by the cap's move. Half way the purple is a crumpled 117 mm line turning through 586 degrees
   (it starts at 6, ends at 717). The ribbon lies at x 733 - 754, z 1287 - 1353 (Step 35, guide.py:769-805), and the potentiometer's
   three leads run over it at y 915 - 919.5, z 1328 - 1341, from the potentiometer at x ~790 to the rails; the wires' lying routes run
   behind the leads' risers (x < 689), so every wire has to pass through the leads on its way (Lee's Step 35 note asks for the ribbon
   to move anyway: "partially covered by F1 and the potentiometer wires").
5. **The lying shape itself** (`lying_lane`, guide.py:872-877): from the end of the shared run each wire turns to +z over 2 - 3 mm, goes
   up over the top (y 938 - 940) and drops straight down 21 - 27 mm at x ~689, turns +x at the bottom, runs along to its pin and turns +z
   into its cap. Measured (deg/mm over 3 mm, and the whole wire's turning):

   | Lying route | Length | Sharpest bends | Total turn | (seated, for scale) |
   |---|---|---|---|---|
   | purple (61) | 181.2 mm | 19.3 at the join round F9's edge [688.4, 939.8, 1361.4], 17.8 over the top of the drop [689.2, 938.3, 1371.4], 13.5 at its foot [690.5, 914.1, 1371.1], 10.5 into the cap | 752 deg | 494 |
   | yellow (62) | 177.9 | 20.4 [688.9, 937.3, 1361.7], 17.8 [689.9, 935.5, 1368.6], 12.8, 9.0 | 699 | 427 |
   | teal (63) | 130.2 | 16.9 [688.7, 933.4, 1365.5] (join and top of the drop in one), 11.6 at the foot | 590 | 359 |
   | blue (64) | 128.8 | 24.1 [689.8, 933.1, 1361.9], 10.8 | 542 | 341 |

   That is: a kink where the lane leaves the shared run (its first control point is 2 - 3 mm away, `[h0 + 0.8, h1, (h2 + z) / 2]`, while the
   run is heading +x), a hairpin over a vertical drop, and two more tight corners: 3 - 4 bends of 2.4 - 5 mm radius in each wire, and
   1.5 - 2 times the turning of the same wire seated. With the in-between shapes of point 4 (and the 18 mm lift of point 1) this is the
   "crazy, bent randomly" look. (The CAD's seated heads also zigzag by about +-5 deg/mm at 1 mm spacing; that is not visible.)

### Fixes

**(a) GND and VCC into other holes of the same rails** (tested). Any hole of a rail is the same connection; at k = +2 and +4 nothing
leans over them. Move the purple's cap to the (-) blue rail at z 1290.00 and the yellow's to the (+) red rail at z 1295.08 (rail holes
are at z 1284.92 + 2.54 k, in fives: k = 0 - 4 is one group), and redraw their first 20 - 25 mm: 14 mm straight up, then over into the
CAD's own run. (If the published hole matters to Lee, this is his call; the steps' wording, "(-) blue" / "(+) red", does not change.)

```json
"adjust_mm": { ..., "NAUO82": [0, 0, 10.16], "NAUO84": [0, 0, 15.23] }
```
```python
# guide.py, after HOLES, CAPS, LINES = ... (line 140)
# The LCD's GND and VCC wires go into the rails at k = +2 and +4, not where the CAD has them (k = -2, z 1279.84): there the black and
# green jumpers lean right over the holes (the green 1.24 mm from the GND hole's axis at y 925, the black 0.55 mm from the VCC hole's),
# and neither wire can go in without passing through them (Lee, 21 Oct 2026). materials.json adjust_mm moves the caps the same.
LCD_RAIL_SHIFT = {'NAUO82': 10.16, 'NAUO84': 15.23}
for _cap, _dz in LCD_RAIL_SHIFT.items():
    for _k in ('top', 'wire_at', 'tip'):
        if _k in CAPS[_cap]:
            CAPS[_cap][_k] = np.add(CAPS[_cap][_k], [0.0, 0.0, _dz]).tolist()
    CAPS[_cap]['box'] = np.add(CAPS[_cap]['box'], [0.0, 0.0, _dz]).tolist()

# guide.py, beside lcd_line (line 842)
LCD_RISE = {'NAUO82': [[698.6, 921.5, 1290.3], [694.0, 927.0, 1292.0], [688.5, 928.9, 1295.5]],   # (GND: up, over the (+) rail and
            'NAUO84': [[696.5, 921.5, 1296.5]]}                                                     # the jumpers' ends; VCC: up and on)
LCD_RISE_JOIN_Z = {'NAUO82': 1299.76, 'NAUO84': 1304.59}            # (where each meets the CAD's run, going on along it)

def rerouted(male, line):
    """A CAD wire's line from the breadboard, its start redrawn from the moved hole (LCD_RAIL_SHIFT): 14 mm straight up, then smoothly
    through LCD_RISE into the CAD's own run."""
    if male not in LCD_RISE:
        return line
    j = int(np.argmax(line[:, 2] >= LCD_RISE_JOIN_Z[male]))
    w = wire_at(male)
    body = W.smooth([w + [0.0, 14.0, 0.0], *LCD_RISE[male], line[j]], start_dir=[0, 1, 0], end_dir=unit(line[j + 2] - line[j]), spacing=0.5)
    head = W.resample(W.join(W.straight(w, [0, 1, 0], 14.0), body), 1.0)
    head[-1] = line[j]
    return W.join(head, line[j:])

def lcd_line(key, male, fem, lcd_pose):
    """A CAD wire's line from the breadboard (its male end) into its female cap, the LCD at lcd_pose."""
    return rerouted(male, into_fem(cad_line(key, male)[::-1], fem, lcd_pose)[::-1])
```
(LCD_HEAD, the lying, out, angled, standing and seated shapes all come from `lcd_line`, so they all get the new start.)

**(b) Push only the cap: a held shape per wire** (tested). Draw each wire with its cap held at UP as its own route (`a_at=UP`): straight up
out of the cap 4 mm and one smooth bend into the lying route at a point before the wire runs under one put in earlier; and give the
done view a copy of the lying route whose `tail_from` is that point. Both keep `b_from` = the shared run's length, so both heads are
carried by the cap; paired from the far end (the run past the join is the same points in both), their moves cancel exactly:
(1 - k)(P - 18k) + k(P + 18(1 - k)) = P. The run past the join stays put while the cap goes down, and the bit by the cap shrinks from the
held bend into the riser. From the next step until Step 50 the wire takes a third copy of the same points with no `tail_from` at all:
with `tail_from` in both, the player pairs the run up to the larger of the two by distance from the first end (player.js drawWires
`two()`), so swapping straight back to the lying route (`tail_from` = the shared run, which Step 50's blends need) pulled the wire up
to 12.5 mm out of shape as the next step opened (measured); with it missing in one of them the two are paired by distance and nothing
moves (measured: 0.5 mm, the resampling). Step 50's first leg then goes from that copy to the lying route, also unseen.

```python
LCD_JOIN = {'purple': 22.0, 'yellow': 22.0, 'teal': 25.0, 'blue': 23.0}   # (mm along each lying wire where the held wire meets it:
                                                                        # before it runs under a wire put in before it)

def lcd_held(colour, male, fem, lying):
    """An LCD wire's lying route `lying` (from the breadboard) with its male cap held at UP; the same route for the push, paired with it
    from the join on; and the same route with no tail_from, for the steps after (see above). The lying route's own points are used as
    they are, so that every swap is exact."""
    line, k = np.asarray(lying['pts'], float), lying['b_from']       # (k: the shared run's length)
    s = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))]
    i = int(np.searchsorted(s, LCD_JOIN[colour]))
    J, tJ = line[i], unit(line[i + 2] - line[i])
    start = line[0] + UP
    P1 = start + [0.0, 4.0, 0.0]
    body = W.smooth([P1, P1 + (J - P1) * 0.4, J], start_dir=[0, 1, 0], end_dir=tJ, spacing=0.25)
    first = W.resample(W.join(W.straight(start, [0, 1, 0], 4.0), body), 1.0)
    first[-1] = J
    f = round(W.length(first), 1)
    held = W.route(W.join(first, line[i:]), a=male, b=fem, a_at=UP, b_at=LCD_LYING, b_from=round(f + k - float(s[i]), 1), tail_from=f)
    push = W.route(line, a=male, b=fem, b_at=LCD_LYING, b_from=k, tail_from=round(float(s[i]), 1))
    plain = W.route(line, a=male, b=fem, b_at=LCD_LYING, b_from=k)                      # (no tail_from: see above)
    return held, push, plain

# the loop (guide.py:886-901)
LCD_PLAIN = {}
for k, (colour, male, label, fem, pin, lying_key, _, _) in enumerate(LCD_WIRES):
    held, push, LCD_PLAIN[colour] = lcd_held(colour, male, fem, LCD_LYING_LEAD[colour])
    prev = {f'lcd {LCD_WIRES[k - 1][0]}': LCD_PLAIN[LCD_WIRES[k - 1][0]]} if k else {}   # (the wire before: the same line, unseen)
    g.place(..., wires=prev or None, wires_done={f'lcd {colour}': [held, push]}, ...)   # (the rest as now)
# and the USB step (guide.py:950): wires=dict(usb_cable(USB_OUT), **{'lcd blue': LCD_PLAIN['blue']})
```

**(c) Smoother lying lanes** (tested for bends and clearances; a look in the player still wanted):

```python
LCD_LANE_CTRL = (0.3, 0.55, 0.82)                                   # (shares of the way from the run's end to the pin, in x)

def lying_lane(colour, fem, head):
    """The control points of an LCD wire's lane from the end of its shared run to its pin on the lying LCD: across to its lane while
    nearly level, down while moving on towards its pin, along at the pin's height, and in to its cap (Lee, 21 Oct 2026: the hairpin over
    F9's place and the straight drop read as bent at random)."""
    h, z = head[-1], LCD_LANE_Z[colour]
    end, out = fem_end(fem, LCD_LYING)
    x, y = end[0], end[1]
    a, b, c = LCD_LANE_CTRL
    return [[h[0] + a * (x - h[0]), h[1] - 1.0, z - 1.0], [h[0] + b * (x - h[0]), (h[1] + y) / 2, z],
            [h[0] + c * (x - h[0]), y + 1.2, z + 0.5], [x - 0.4, y, z + 6.0]]
```
Bends of the lying routes with (a) and (c): purple 12.3 deg/mm (was 19.3; its sharpest is now in the new rise, 38 - 41 mm from the
hole), yellow 10.8 (20.4), teal 10.0 (16.9), blue 10.0 (24.1); total turning 532 / 473 / 439 / 440 degrees (was 752 / 699 / 590 / 542);
the largest corner between two 1 mm segments 11 - 17 degrees. Lengths 163.4 / 151.0 / 117.3 / 117.6 mm (were 181.2 / 177.9 / 130.2 /
128.8). The four lanes keep their order (GND outermost) and their spacing; the closest pairs at rest are in the shared run (purple /
yellow 2.51 mm, yellow / teal 1.89, as now). Other lane spacings tried (1373/1369/1365/1361, 1374/1370/1366/1362) gave the same.

### Measured with (a) + (b) + (c) together (and the Step 13/14 and Step 32 fixes)

motioncheck with parts, 37 moments, the caps moved as materials.json would (`MC_ADJUST` in the scratch copy):
- **Gone:** every touch with the black, green and white jumpers (36c, 37c), and every touch between the LCD wires in the push (37c purple /
  yellow, 38c purple / teal and teal / yellow, 39c blue with purple, yellow and teal in beat 2).
- Steps 37, 38, 39, 40 (the unseen swaps), 45c, 49c, 51c: 0 problems. Step 50c: three touches between the LCD wires' tails as the LCD
  swings out (0.82 - 1.03 mm at 0.475) - these are in the committed guide too, worse (0.39 - 0.55 mm at 0.475; found only with 37 moments: the
  default 19 sample 0.45 and 0.50, either side of the beat boundary).
- **Left (beat 1 only):** the wires passing through the potentiometer's leads on their way from the table (36c purple / pot black
  0.17 mm at 0.25; 37c yellow / pot red 0.82 at 0.27; 39c blue / pot tan 0.14 at 0.32, blue / pot black 0.89 at 0.27); the teal's and
  blue's caps brushing the purple and blue jumpers' risers at a8 / a9 as they arrive over b8 / b9 (0.74, 0.90, 0.36 mm at 0.37, 3
  frames); and in 39c the blue's run brushing the teal's riser at the end of beat 1 (0.27 mm at 0.37, near [686.9, 918.2, 1325.0]).
- Whole guide, wires only, 19 moments: 49 touches before, 26 after; none new (36c's purple / pot tan becomes purple / pot black).

### What is left, and how to finish it

All of what is left happens in beat 1, because the run to F9's edge is carried by the cap as it comes from the table: it arrives from in
front and below (which is what keeps the later wires under the earlier ones at F9's edge), so the cap's last bit of way is also from in
front and below, past the a8 / a9 risers, and the wire sweeps through anything between the table and its place.
1. **Step 35's ribbon** must not lie under the potentiometer's leads, and from where it lies the way to each wire's place must not cross
   them. The leads span x 689 - 790 at z 1328 - 1341 (y up to 919.5); the wires' places are behind their risers (x < 689) between z 1280
   and 1360 and the lanes beyond. A ribbon in front at z < 1325 still crosses them on the way to the LCD (the female ends must get to
   z 1384); one +z of them (z 1342 - 1381, x 727 - 762: 35 x 39 mm, too short for the 66 mm wires straight) does not fit. Two ways out:
   lay the ribbon on the lying LCD's back (y ~914, x 700 - 766 along x, z ~1395 - 1416: the female ends by the header; the male ends'
   way to the board then needs a `via()` over the leads, y >= 935), or keep the ribbon where Lee wants it and give beat 1 an in-between
   route (`wire_via`) drawn over the leads (y >= 925 across x 697 - 790). Either needs a run in the player.
2. **The a8 / a9 brush**: hold the teal and blue caps higher (`[0, 25, 0]` tried: 0.69 / 0.81 mm left) or come in over b8 / b9 from
   above; the second makes the carried run come down from above at F9's edge, so it needs the run in beat 1 tied to the female cap
   instead (`a_whole` / `b_whole`, the female straight onto its pin in beat 1, and the same invisible swap back afterwards). Tried: it
   removes the brush but its in-between shapes then crossed the yellow; not finished.
3. A smaller held bend: the held shapes above bend over the cap's top at 24 - 39 deg/mm (a 1.5 - 2.5 mm radius) where the wire leaves
   the cap upwards and turns to the join; a higher exit (6 mm instead of 4) or a join a little further on softens it. The ones tried
   with a length-matched loop instead were worse (47 - 60 deg/mm).

## Notes on the checking tools (found on the way)

- `tools/motioncheck.py` spaces a way's in-between poses (`via()`) by the distance between the poses' matrices' translations
  (`along`, motioncheck.py:73-77). For a pose written as a turn (a lying cap: `{t, r, at}`) that translation is about the origin, so a
  `via` next to it gets ~2200 mm of "distance" and the part reaches it only at the very end of the beat. The player spaces them by
  `pose.t` plus half the turn in degrees (player.js `poseGap`, :641). Ways without a `via`, or with only untilted poses, are unaffected.
  The scratch copy uses the player's spacing:
  ```python
        def gap(a, b):                          # (player.js poseGap: the move `t` plus half the turn in degrees)
            sh = lambda p: np.asarray(p if isinstance(p, list) else (p or {}).get('t', [0, 0, 0]), float)
            ra = Rotation.from_matrix(_matrix(a)[:3, :3]); rb = Rotation.from_matrix(_matrix(b)[:3, :3])
            return float(np.linalg.norm(sh(b) - sh(a)) + np.degrees((ra.inv() * rb).magnitude()) * 0.5)
        L = [gap(seg[i], seg[i + 1]) + 1e-6 for i in range(len(seg) - 1)]
  ```
- 19 moments (0.05, 0.10, ... 0.95) skip 0.475: in a step of several beats a touch at a beat boundary can be missed (the committed Step
  50c has three, 0.39 - 0.55 mm at 0.475, that the default run does not report). `--moments 37` in the scratch copy finds them.
- It checks wires against parts and against each other, not a moving part (a cap) against the parts it passes; the caps' brushes above
  are wires running into caps.
- It does not look at shapes. The bend measure used here (turn over 3 mm, per mm) is in `scratchpad/clip/bend.py`.

## Scratch files (not in the project)

`/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/46c40992-e0fc-4f94-b08e-62c20da998a4/scratchpad/clip/`: `mc.py`
(motioncheck with `--noparts`, `--moments`, `--dump`, the player's via spacing, and `MC_ADJUST` for a part moved as adjust_mm would),
`common.py` (the guide's helpers), `fix1314.py`, `fix32b.py` (the tested variant), `fix32.py` (the 18 mm alternative), `fixlcd3.py` +
`held2.py` + `lane.py` (the LCD changes), `final.json` (steps.json with every fix), `base_all2.txt` / `final_all.txt` (whole guide,
wires only, before / after).
