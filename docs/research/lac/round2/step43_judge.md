# LAC Step 43: judging the two carry designs, "low" and "high" (21 Oct 2026)

Lee (21 Oct 2026, his second time on Step 43): "Pass the red and black wires over the black/green/purple/blue wires instead of
clipping through and under them." Two designers proposed fixes: `step43_low.md` and `step43_high.md`. This note does three things:

* re-runs their checks on their own steps copies;
* pastes each design's code into a copy of the current guide.py;
* plays each steps copy in the real player and judges how it looks.

Nothing in the kit was changed. Two temporary files went into the kit's `thumbs/` and were removed: the steps copies, and the pictures
(kept here as `step43_judge_*.png`, gitignored). Scripts and outputs are in `scripts/round2/step43_judge/`.

## Verdict

(Applied to guide.py the same day, as section 5 gives it: Step 43c then checked at 1 problem at 39 moments and 4 at 199, as below.)

**Take "high".** Neither design is clean, and neither can be: both designers found, by different methods, that the black lead must pass
through the four LCD wires once in Step 43. The LCD wires were laid over the lying black lead in Steps 36 - 39. Removing that crossing
takes a change outside Step 43.

High is the better of the two:

* **Fewest crossings.** It has only those four forced crossings. The red lead touches nothing at any moment.
* **The red / tan crossing is avoidable.** Low keeps one more crossing (red through the switch's tan lead) and calls it forced. It is
  forced only for low's seated red, which runs behind the switch. High's seated red runs in front of the switch, and Steps 44 - 56 stay
  as clean as now.
* **Same pace and framing as now.** It keeps the step's three beats (2.4 s). The buzzer is never higher on screen than it is now.
  Low adds a fourth beat, in which the buzzer hangs still for 0.8 s. Low's buzzer, stood upright at the top of its lift, goes partly
  behind the caption box (section 4).

High has two costs that Lee will see:

* **A different seated red, from Step 43c to the Completed View.** It now goes forward, up in front of the switch beside the black
  lead, back across the board past the clock module, and into j4 from behind.
* **A stiff look while the buzzer is held high.**
  * Black runs as a long, nearly straight line across the model at the buzzer's height.
  * Red stands up as a post behind the j-side caps, and a red loop stands up there as the buzzer is lowered.
  * There is a short crease in the red lead mid-carry. Low has its own sharp V in the red mid-carry, so this does not decide it.

## 1. Their motioncheck claims, re-run on their steps copies

| | the guide now | low (`s43_low/steps_low.json`) | high (`s43_high/steps-final.json`) |
|---|---|---|---|
| Step 43c, 39 moments | 14 | **2**: red / switch tan 0.19 at 0.62; black / LCD teal 0.86 at 0.15 (as claimed) | **1**: black / LCD teal 0.70 at 0.45 (as claimed) |
| Step 43c, 199 moments | 16 | **5**: red / switch tan; black / LCD purple, blue, yellow, teal at 0.14 - 0.16 (as claimed) | **4**: black / LCD yellow, teal, blue, purple at 0.44 - 0.46 (as claimed) |
| Steps 44 - 56c, 39 moments (27 views) | 16 (the potentiometer's leads, 46c and 52c) | the same 16, line for line | the same 16, line for line |
| wirecheck, all 116 views at rest | 1 (Step 12, jumper purple / NAUO22 0.04) | the same 1 | the same 1 |

Neither design touches Lee's black, green, purple or blue jumpers at any moment. Each forced LCD crossing lasts about 0.02 of the
motion:

* low: at 0.14 - 0.16, in the lift (about 60 ms of 3.2 s);
* high: at 0.44 - 0.46, in the carry (about 50 ms of 2.4 s).

Low's red / tan crossing is at 0.62 - 0.63 (about 30 ms), in the middle of the picture.

## 2. Paste-readiness against the current guide.py (unchanged since 13:21)

`paste_check.py` works in four steps:

1. It pastes each design's code into a copy of guide.py, as text, exactly as its report gives it.
2. It checks that the whole file still parses.
3. It runs the patched buzzer section with guide.py's own setup lines (the AST-selected assignments and helpers; no Guide, no model).
4. It compares the result with the designer's steps copy.

Results:

* **low:** Step 43's path and all 8 routes (4 shapes x 2 leads) equal the steps copy exactly: 0.00 mm, the same keys. The lying
  routes (Steps 33c - 42c) equal the current steps.json exactly. The only differences from the current steps.json:
  * Step 43 / 43c's path;
  * 43c's wire_via;
  * the red's seated route in every view from Step 43c on, and in the Start view.

  Loose ends in the text:
  * the comment above BUZZER_WAY ("lifted 60 mm") and the comment above BUZZER_SEAT_WAY ("red in under the orange and yellow") go
    stale;
  * buzzer_plugged's `stretch` argument becomes unused.
* **high:** Step 43's path and all 6 routes (3 x 2) are exact, and the lying routes are identical. The only differences:
  * Step 43 / 43c's path;
  * 43c's wire_via;
  * both seated routes from Step 43c on. Black's points are the same; its b_from / tail_from become 9.0 (the drop) instead of the
    junction's 101.8.

  The patch rewrites its own comments. Nothing else in guide.py uses the names it removes:
  * BUZZER_UP, BUZZER_UP_WAY, BUZZER_J_Z;
  * buzzer_over_seat;
  * seated_from_buzzer's second return value.

  (Its steps copy did not update the Start view's routes; the generator will. That has no effect on any check.)

## 3. How each looks in the player (CASE_CAMERA, 1280 x 800)

Each steps copy was played in the real player and drawn at moments of Step 43c. The pictures are `step43_judge_now.png`,
`_low*.png` and `_high*.png`.

**Low, 4 beats, 3.2 s.**

* **Lift (0 - 0.25).** The buzzer rises at the far end and turns upright. The black lead lifts out from under the LCD wires (the
  flicker). The red lead stays low along the back and rises to the buzzer: tidy.
* **Carry (0.25 - 0.5).**
  * At 0.37 - 0.40 the red lead has a sharp V under the buzzer. The black lead makes a wide loop over the left of the board.
  * At 0.43 the red lead is a boxy loop.
  * By 0.47 both leads lie about 15 mm above their ways.
* **Settle (0.5 - 0.75).** The buzzer hangs still over its slot while both leads drop onto their ways. The red lead passes through the
  switch's tan lead at 0.62. It reads as "lay the leads, then push the buzzer in", but the buzzer stands still in mid-air for 0.8 s.
* **Lower (0.75 - 1).** Clean, as now.

**High, 3 beats, 2.4 s.**

* **Lift (0 - 0.33).** As now: the buzzer rises 60 mm, still lying.
  * The red lead's first 32 mm stay low behind the board's end.
  * The black lead rises from under the LCD wires.
* **Carry (0.33 - 0.67).** The buzzer swings over the board and turns upright, to 75 mm over its slot.
  * The black lead passes through the LCD wires at 0.44 - 0.46.
  * There is a small S-crease in the red lead at 0.48 - 0.52.
  * By 0.55 the leads are held high. The black lead goes straight up out of (-) blue, then runs as a long, nearly straight line over
    the board to the buzzer. The red lead stands up as a post behind the j-side caps, then arches to the buzzer.
* **Lower (0.67 - 1).** The buzzer goes straight down into the F7s. Each lead settles from above onto its seated way. As the red post
  folds down, a red loop stands up by the clock module (0.8 - 0.93) and shrinks away.

**Sharp bends** (`run_bends.py`: motioncheck's blending at 199 moments; turning per mm over 3 mm; the drop into the hole and the
20 mm at the stub left out). Counted as moments over 30 degrees per mm, a crease:

| | red | black |
|---|---|---|
| now | 17 moments (0.47 - 0.55) | none |
| low | 7 moments (0.36 - 0.39; 42 at the V) | 6 moments (0.37 - 0.40; 33) |
| high | 26 moments (0.45 - 0.77): the S-crease (49 at 0.515) and the post folding at the start of the lowering (30) | none |

## 4. Framing: the buzzer against the caption box

`topOf()` in the real player: the buzzer's highest pixel through the motion, and the share of the buzzer behind the caption box
(the box ends 87 px down).

| window | now | low | high |
|---|---|---|---|
| 1280 x 800 | top 102 px, never behind | top 55 px; **up to 27 % behind, t 0.18 - 0.33** | top 99 px, never behind |
| 1100 x 600 (short) | up to 54 % behind (t 0.25 - 0.45) | **up to 84 %** (t 0.15 - 0.35) | up to 54 % (t 0.25 - 0.55) |
| 768 x 1024 | | | clear (top 179 px) |

(In the LMS frame the caption is a pill, so the box does not apply there.)

## 5. What to paste (high)

Two replacements in `LAC Build Instructions/guide.py`. Both were checked by pasting into a copy of the guide.py of 13:21.

**(1)** Replace everything from the comment `# Each lead's way to its hole, the buzzer lying (Steps 33 - 42) and lifted 60 mm` (line 741)
down to the end of `buzzer_clamped` (its `return W.route(line, a=cap, b=BUZZER, b_from=k, tail_from=k)`, line 841) with:

```python
# Each lead's way to its hole, the buzzer lying (Steps 33 - 42) and lifted 60 mm over where it lies (Step 43): short and smooth, clear
# of the parts and the other wires (a path search; Lee, 20 Oct 2026: the CAD's lying leads loop out sideways, and blending the straight
# leads into them threw them off the screen; the red one had a kink by the breadboard). Lifted, red's run behind the board's end stays
# low (under the yellow jumper's arch at j4) up to BUZZER_LIFT_HOLD and only then rises to the buzzer, so that as the buzzer is carried
# the run swings round behind the j-side caps without touching the yellow jumper (docs/research/lac/round2/step43_high.md).
BUZZER_WAY = {'red': [[647.2, 901.2, 1399.0], [647.8, 901.9, 1394.1], [647.8, 902.0, 1389.2], [647.8, 902.0, 1384.2], [647.8, 902.0, 1379.2], [647.9, 902.0, 1374.3], [648.1, 902.3, 1369.0], [648.5, 902.6, 1364.2], [648.8, 903.1, 1359.0], [648.8, 903.7, 1354.3], [649.1, 904.7, 1349.3], [650.1, 905.6, 1344.7], [652.5, 906.0, 1340.3], [655.8, 906.0, 1336.5]],
              'black': [[648.9, 897.0, 1393.1], [652.2, 897.0, 1389.5], [655.7, 897.0, 1386.0], [659.2, 897.1, 1382.5], [662.7, 897.4, 1379.0], [666.5, 897.8, 1375.2], [669.9, 898.0, 1371.8], [673.5, 898.0, 1368.3], [677.0, 898.0, 1364.9], [681.0, 898.3, 1361.5], [684.5, 899.2, 1358.7], [688.0, 901.4, 1355.6], [690.9, 904.1, 1352.7], [693.6, 907.0, 1349.8], [696.0, 910.3, 1346.4]]}
BUZZER_LIFT_WAY = {'red': [[645.7, 951.9, 1397.4], [645.9, 949.6, 1393.0], [646.6, 946.6, 1389.0], [648.0, 943.5, 1385.8], [650.5, 940.5, 1382.3], [653.0, 937.9, 1378.8], [654.6, 934.0, 1375.0], [655.2, 927.0, 1370.5], [655.0, 919.0, 1366.0], [654.3, 912.0, 1361.5], [653.8, 908.0, 1357.0], [653.5, 906.8, 1352.0], [653.6, 906.5, 1347.0], [653.2, 906.5, 1342.5], [653.0, 906.6, 1338.6]],
                   'black': [[648.2, 954.7, 1393.7], [651.0, 952.0, 1390.8], [653.8, 949.1, 1387.9], [656.7, 946.2, 1385.0], [659.6, 943.3, 1382.1], [662.5, 940.5, 1379.2], [665.4, 937.6, 1376.3], [668.3, 934.7, 1373.4], [671.1, 931.8, 1370.6], [674.0, 929.0, 1367.6], [677.3, 926.3, 1364.4], [680.4, 924.4, 1361.3], [683.9, 922.7, 1357.8], [687.1, 921.2, 1354.6], [690.6, 919.5, 1351.1], [693.7, 917.9, 1347.8], [696.7, 916.1, 1344.1]]}
BUZZER_LIFT_HOLD = {'red': 32.0}                                  # (red, lifted: the run up to here, from the hole, does not follow the buzzer)
BUZZER_LIFT = tidy(compose([0.0, 60.0, 0.0], BUZZER_LYING, BUZZER_LYING['at']))   # (about the buzzer's own middle, as BUZZER_LYING is)
BUZZER_HIGH = [0.0, 75.0, 0.0]                                       # (Step 43: carried over the board to 75 mm over its seat, clear of the
                                                                    # spread F7s' tops, then lowered straight in)


BUZZER_ABOVE = {'red': 0.5, 'black': 5.0}                           # (how far each goes straight down into its hole, over the cap's top: red
                                                                    # into j4 under the yellow jumper, whose centre line is 913 over j4)
BUZZER_CREST = {'red': 0.3, 'black': 1.5}                           # (how far over the drop's top each comes in: red low, so that held 5 mm
                                                                    # over j4 (Step 33) it stays under the yellow jumper: review, 21 Oct 2026)
BUZZER_OUT = 3.0                                                    # (straight out of the buzzer before a lead turns)
BUZZER_RISE = {'red': 2.2, 'black': 0.0}                            # (red then rises over the black lead beside it, which it turns across)


def buzzer_line(colour, cap, exit_, pose, way):
    """A buzzer lead from its exit (the buzzer at `pose`): 3 mm straight out, through `way`, over a crest BUZZER_CREST mm above the top of its
    straight drop and 4.5 mm short of it, and down into its hole. The controls within 8 mm of the run out and 7 mm (across) of the drop
    are left out, so that the lead turns over several mm (the review of Lee's first round: the path search's controls there made
    hairpins, and the drop's top a crease)."""
    q = posed_line(pose, [exit_, np.add(exit_, [0.0, -1.0, 0.0])])
    e, d = q[0], unit(q[1] - q[0])
    above = BUZZER_ABOVE[colour]
    first, top = e + d * BUZZER_OUT, wire_at(cap) + [0.0, 4.0 + above, 0.0]
    across = lambda p: float(np.hypot(p[0] - top[0], p[2] - top[2]))
    keep = [np.asarray(p, float) for p in way if np.linalg.norm(np.asarray(p, float) - first) > 8.0 and across(p) > 7.0]
    rise = [first + d * 2.0 + [0.0, BUZZER_RISE[colour], 0.0]] if BUZZER_RISE[colour] else []
    h = top - (keep[-1] if keep else first)
    h[1] = 0.0
    return into_hole(cap, e, d, rise + keep + [top - unit(h) * 4.5 + [0.0, BUZZER_CREST[colour], 0.0]], lift=BUZZER_OUT, above=above)


def shared_to(line, point):
    """How far along `line` (from its first point) its point nearest `point` is."""
    s = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))]
    return round(float(s[int(np.argmin(np.linalg.norm(line - np.asarray(point, float), axis=1)))]), 1)


def buzzer_plugged(colour, cap, exit_, pose, way, stretch=False, hold=None):
    """A buzzer lead plugged in (buzzer_line), drawn from the hole: its straight drop held in the hole (b_from) and shared between
    shapes (tail_from); the rest carried whole with the buzzer (no stretch: it turns with it). With `stretch` (the buzzer lifted, Step
    43): matched to the next shape by share of length instead, so that its run over the seat grows along the lead rather than fanning out
    from the top of the drop (where it dipped into the resistors). `hold`: mm from the hole that do not follow the buzzer (b_from), if
    more than the drop."""
    line = buzzer_line(colour, cap, exit_, pose, way)[::-1]
    k = BUZZER_ABOVE[colour] + 4.0
    return W.route(line, a=cap, b=BUZZER, b_at=pose, b_from=hold or k, **({'stretch': True} if stretch else {'tail_from': k}))


# The seated leads (Lee, 21 Oct 2026: "pass the red and black wires over the black/green/purple/blue wires"; his second note on Step 43,
# the same day: and not through them as the buzzer is carried in). From the stub's end, straight on down 1 mm and round under it. Red comes
# into j4 from behind, as it lies before the step (under the yellow jumper's arch only at the hole): it climbs behind the j-side caps,
# crosses over the yellow and orange jumpers just past the clock module, over the row-i ends of the jumpers and over the black and green
# jumpers' arches, then over the switch's tan lead by the (+) red rail and down in front of the switch to the buzzer. Black runs along the
# front rails over the potentiometer's leads, the LCD's purple wire and the green jumper, over the switch's tan lead, to the buzzer. Both
# pass in front of the switch (on its +x side where it is seated), so that neither is under one of the switch's leads before F4 is lifted
# (Step 47): the buzzer is carried over the board, so its leads can only lie over what they cross, and the switch is then carried over
# them (docs/research/lac/round2/step43_high.md: which crossings each motion allows). Drawn from the stub's end: no gap where the lead
# meets it.
BUZZER_SEAT_WAY = {'red': [[674.5, 891.3, 1235.6], [675.5, 892.6, 1239.0], [678.0, 894.5, 1241.8], [683.5, 899.5, 1246.0], [685.3, 903.5, 1249.5], [686.3, 907.5, 1253.0], [687.4, 911.0, 1256.5], [688.5, 914.5, 1260.0], [689.3, 919.5, 1262.5], [690.0, 923.8, 1265.0], [690.4, 927.8, 1268.2], [690.3, 931.5, 1272.0], [689.3, 934.6, 1275.3], [687.0, 935.6, 1278.3], [682.5, 935.4, 1280.6], [676.5, 934.0, 1282.3], [671.0, 931.0, 1284.0], [667.0, 927.8, 1286.2], [665.2, 926.0, 1289.0], [664.6, 925.6, 1293.5], [663.6, 925.0, 1298.5], [661.6, 923.8, 1303.0], [659.3, 921.6, 1307.0], [657.6, 917.8, 1311.8], [656.9, 913.2, 1317.5], [657.1, 909.3, 1323.5], [657.9, 907.4, 1329.0]],
                   'black': [[676.2, 891.3, 1235.6], [677.6, 893.0, 1238.8], [680.6, 895.6, 1240.6], [686.8, 902.4, 1244.4], [687.8, 905.7, 1247.7], [688.1, 909.5, 1251.5], [688.8, 912.9, 1254.9], [690.4, 916.1, 1258.1], [692.4, 919.5, 1261.5], [693.2, 922.9, 1264.9], [694.1, 926.6, 1268.6], [695.8, 929.6, 1271.8], [697.7, 932.1, 1275.6], [698.4, 933.1, 1280.5], [698.5, 933.1, 1285.3], [698.5, 932.2, 1290.4], [698.5, 930.3, 1295.2], [698.5, 928.6, 1299.9], [698.5, 928.0, 1304.7], [698.5, 927.8, 1309.6], [698.5, 926.5, 1314.5], [698.5, 924.3, 1319.1], [698.5, 922.7, 1324.0], [698.5, 922.1, 1328.7], [698.5, 921.0, 1333.5]]}
BUZZER_SEAT_OUT = 1.0                                               # (straight on out of the stub before the lead turns under it)
BUZZER_KEEP = {'red': [661.6, 923.8, 1303.0], 'black': None}         # (Step 43: the run from the hole to here is the same carried high and
                                                                    # seated, and stays put as the buzzer is lowered; black: its drop)
BUZZER_RISER = {'red': [661.0, 945.0, 1304.2], 'black': [699.2, 945.0, 1340.9]}   # (carried high: the top of each lead's
                                                                    # rise, red's from BUZZER_KEEP behind the j-side caps, black's straight up out of (-) blue)
BUZZER_RED_RISE = [[661.2, 928.0, 1303.8], [661.0, 934.0, 1304.2]]
BUZZER_HIGH_WAY = {'red': [[673.0, 960.0, 1238.0], [676.0, 957.0, 1252.0], [680.0, 954.0, 1268.0], [674.0, 951.0, 1285.0], [665.5, 948.0, 1298.0]],
                   'black': [[679.0, 960.0, 1237.0], [686.0, 959.0, 1250.0], [693.0, 958.0, 1268.0], [698.5, 955.0, 1290.0], [699.0, 950.0, 1322.0]]}


def seated_from_buzzer(colour, cap, exit_):
    """A buzzer lead seated, from the stub's end to the hole, every 1 mm (red in over a crest under the yellow jumper, as buzzer_line)."""
    e, d = np.asarray(exit_, float), np.array([0.0, -1.0, 0.0])
    above = BUZZER_ABOVE[colour]
    top = wire_at(cap) + [0.0, 4.0 + above, 0.0]
    way = [np.asarray(p, float) for p in BUZZER_SEAT_WAY[colour]]
    if colour == 'red':
        h = top - way[-1]
        h[1] = 0.0
        way.append(top - unit(h) * 4.5 + [0.0, BUZZER_CREST[colour], 0.0])
    return into_hole(cap, e, d, way, lift=BUZZER_SEAT_OUT, above=above)


def buzzer_kept(colour, cap, exit_):
    """The seated lead from the hole to BUZZER_KEEP (black: its drop), and its length."""
    line = seated_from_buzzer(colour, cap, exit_)[::-1]
    if BUZZER_KEEP[colour] is None:
        k = BUZZER_ABOVE[colour] + 4.0
    else:
        k = shared_to(line, BUZZER_KEEP[colour])
    s = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))]
    return line[:int(np.argmin(np.abs(s - k))) + 1], k


def buzzer_high(colour, cap, exit_):
    """A buzzer lead with the buzzer carried high over its seat (BUZZER_HIGH, Step 43): the seated lead from the hole to BUZZER_KEEP, up
    to the top of its rise (BUZZER_RISER) and high over the board to the buzzer (BUZZER_HIGH_WAY). Drawn from the hole; the run to the top
    of the rise does not follow the buzzer (b_from), and the run kept is matched by distance from the hole to the seated lead's as the
    buzzer is lowered (tail_from), the rest by distance from the buzzer: it settles straight down onto the seated lead."""
    kept, k = buzzer_kept(colour, cap, exit_)
    top = np.asarray(BUZZER_RISER[colour], float)
    if colour == 'red':
        line = seated_from_buzzer(colour, cap, exit_)
        j = len(line) - len(kept)                                   # (where the kept run ends, on the seated lead drawn from the stub)
        rise = W.resample(W.smooth([kept[-1], *[np.asarray(c, float) for c in BUZZER_RED_RISE], top], start_dir=unit(line[j - 1] - line[j]),
                                   end_dir=[0, 1, 0], spacing=0.5), 1.0)
    else:
        w = wire_at(cap)
        n = int(round(top[1] - w[1]))
        rise = np.array([[w[0], w[1] + i * (top[1] - w[1]) / n, w[2]] for i in range(n + 1)])
        kept = rise[:1]
    head = np.vstack([kept, rise[1:]])
    e, d = np.add(exit_, BUZZER_HIGH), np.array([0.0, -1.0, 0.0])
    body = W.smooth([e + d * BUZZER_OUT, *[np.asarray(c, float) for c in BUZZER_HIGH_WAY[colour]], top], start_dir=d, end_dir=[0, -1, 0],
                    spacing=0.5)
    tail = W.resample(W.join(W.straight(e, d, BUZZER_OUT), body), 1.0)[::-1]
    held = round(float(np.linalg.norm(np.diff(head, axis=0), axis=1).sum()), 1)
    return W.route(np.vstack([head, tail[1:]]), a=cap, b=BUZZER, b_at=BUZZER_HIGH, b_from=held, tail_from=k)


def buzzer_clamped(colour, cap, exit_):
    """A buzzer lead seated (seated_from_buzzer), drawn from the hole; the run from the hole to BUZZER_KEEP held still and kept (as the
    buzzer is lowered onto its seat, the rest follows it down)."""
    line = seated_from_buzzer(colour, cap, exit_)[::-1]
    _, k = buzzer_kept(colour, cap, exit_)
    return W.route(line, a=cap, b=BUZZER, b_from=k, tail_from=k)
```

**(2)** Replace the comment line `# (lifted, carried over and lowered: ...` and the `g.place('Lower the buzzer ...` call (lines 1163 - 1167)
with:

```python
# (lifted, carried high over the board to 75 mm over its seat and lowered in: a stop each, its leads keeping pace stop by stop: carried,
# each lead rises behind what it will lie over and arches high to the buzzer; lowered, it settles straight down onto its seated way)
g.place('Lower the buzzer in between the two F7s, its ears into their slots.', move=[BUZZER], path=[BUZZER_LYING, BUZZER_LIFT, BUZZER_HIGH, ZERO],
        lines=False, eye=[dict(id=BUZZER, **near('near-above'))],         # (above the buzzer: Lee, 21 Oct 2026)
        wires_done={f'buzzer {c}': [buzzer_plugged(c, cap, e, BUZZER_LIFT, BUZZER_LIFT_WAY[c], stretch=True, hold=BUZZER_LIFT_HOLD.get(c)),
                                    buzzer_high(c, cap, e), buzzer_clamped(c, cap, e)] for c, cap, _, e, _, _ in BUZZER_LEADS}, **CASE_CAMERA)
```

(The same text is in `scripts/round2/step43_high/guide_patch.txt` and `guide_patch_step43.txt`.)

## 6. After pasting: what to run and check

1. Save a copy of steps.json, then run `.venv.nosync/bin/python "LAC Build Instructions/guide.py"`. Diff every view's camera against
   the copy. Only routes and Step 43 / 43c's path should change; no camera should.
2. `tools/motioncheck.py "LAC Build Instructions" --moments 39 "Step 43c"` should give 1 problem, and `--moments 199` 4. Both are the
   black lead and the LCD wires only.
3. Run motioncheck on Steps 44 - 56c at 39 moments. It should give the same 16 problems as now: the potentiometer's leads, 46c and 52c.
4. `tools/wirecheck.py "LAC Build Instructions"` should give the same 1 problem as now (Step 12).
5. Run the player's runthrough. Then look at the following:
   * Steps 42c - 44c;
   * Step 47c - 48c (F4 and the switch over the new red);
   * Lee's Step 49 camera;
   * the Completed View.
6. Publish to `share/Test guides preview` for Lee on 8799.

## 7. What Lee will see

* **Step 43, as before.** It still plays in three beats.
* **Lift.** The buzzer lifts off beside the board. The red lead stays low behind the board's end; the black lead rises.
* **Carry.**
  * The buzzer swings over the board, turning upright, to well above its slot.
  * Both leads pass over every jumper. In a frame or two the black lead flickers through the four LCD wires at the far end.
  * For a moment the leads look held up on stiff wires: a long black line across the model and a red post behind the caps.
* **Lower.**
  * The buzzer drops straight into the F7s. The leads settle onto the board from above.
  * A red loop briefly stands up by the clock module and shrinks away.
* **From Step 43c on**, the red lead takes a new way:
  * it leaves the buzzer forward, beside the black lead, and goes up in front of the switch;
  * it crosses back over the board just past the clock module, over the orange and yellow jumpers;
  * it goes into j4 from behind.

## 8. What is left, and the options

* **The black lead through the four LCD wires** (about 50 ms). Three ways to remove it, none of them inside Step 43:
  * re-lay the LCD wires (Steps 35 - 51) so that they run forward of (-) blue instead of looping round it, over the lying black lead.
    High's shapes then need no change.
  * lay the black lead over the LCD wires' loops in Steps 34 - 42. That makes a 45 mm arch in Lee's Step 33 - 34 camera; both
    designers advise against it.
  * play Step 43 with `reappear=True`, as the PMG's Step 42 does: the buzzer and its leads fade out and fade in seated. Nothing then
    passes through anything, but the carry Lee asked about is no longer shown.
* **High's stiff held-high look and the red loop in the lowering** could be softened in a further round. For example:
  * a lower BUZZER_HIGH;
  * black's way bowed rather than straight;
  * red's post leaned.

  None of these was tried or checked here.
