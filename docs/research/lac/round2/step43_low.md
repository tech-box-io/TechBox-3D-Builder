# LAC round 2: Step 43's carry beat, design "low, round the holes" (21 Oct 2026)

Lee (21 Oct 2026, his second time on Step 43): "Pass the red and black wires over the black/green/purple/blue wires instead of
clipping through and under them." The seated shapes already pass over those jumpers and the lowering beat is clean. The carry beat
(0.45 - 0.58 of the motion) still sweeps both leads through the wire field: motioncheck at 39 moments gives 14 problems.

The approach I was given: keep each lead's run near its hole low, and swing that low run round its hole through free space (red round
j4 through the back strip of the board, x < 661). That swing changes the +z-going run (lying, lifted) into the -z-going run (seated).
Keep the free run to the buzzer above everything, and share runs between consecutive shapes.

Nothing in the kit was changed or regenerated. Working scripts: `docs/research/lac/scripts/round2/step43_low/` (copied from the
session scratch). `guide_patch.py` holds the paste-ready code, which is executed against copies of guide.py's helpers. The checked
steps copy is `.../scratchpad/s43_low/steps_low.json`. The plan view of the motion is `step43_low_plan.png`, beside this file
(gitignored).

## Result in one paragraph

Step 43 cannot reach 0 problems while the lying and seated shapes keep their topology. The red lead must pass through the switch's
lying tan lead once, and the black lead must pass through each of the four LCD wires once (section 1, a linking-number proof). The
current seated red adds two more forced crossings, through the orange and yellow jumpers.

My design has four beats. It changes the red's seated way only near j4: it now goes in to j4 from the back strip, over the orange and
yellow jumpers. That removes the orange and yellow crossings. Step 43c then has exactly the five forced crossings and nothing else:

* 2 problems at motioncheck's 39 moments; 5 problems at 199 moments, all of them forced.
* Each forced crossing is very brief. Black passes through the four LCD wires in 0.143 - 0.162 of the motion, about 60 ms of the
  3.2 s step. Red passes through the tan lead in 0.62 - 0.63, about 30 ms.
* Everything else stays ≥ 0.25 mm clear: parts, every other wire, and red against black. The smallest gaps are red/black 0.25 at the
  stubs (the stubs are only 1.52 mm apart) and the unchanged seated run over the green jumper's row-i end, 0.32.
* Steps 44c - 56c in motion, and every view at rest (wirecheck), give exactly the same problem lists as the current steps.json, none
  of them a buzzer lead.

## 1. What cannot be made clean in Step 43 (a topological limit)

Close each buzzer lead into a loop: the lying lead (Steps 33c - 42c), then the path of its stub through Step 43, then the seated lead
back to the hole. Close every other wire under the table, from both ends straight down. Wherever the Gauss linking number of the two
loops is not 0, no motion of the lead, however it is drawn, can get from the lying shape to the seated shape without passing through
that wire. (The stub stays above everything.) There is one exception: an end of that wire would have to swing round, and none does in
Step 43. The switch's tan lead has a free end, the switch on F4, but that end hangs in the air 60 - 100 mm behind the board, so
reaching round it is out of the question. `linking.py` computes the numbers.

| lead | wires it is linked with: current steps.json | with this design |
|---|---|---|
| red | switch tan (-1), jumper orange (+1), jumper yellow (+1) | switch tan (-1) only |
| black | lcd purple, yellow, teal, blue (-1 each) | the same four |

Every other wire scores 0.00 in both cases.

Why each of these holds:

* **Red and the tan lead.** The tan lead lies across the board at z 1270, from the (+) red rail to the switch on F4 behind the board.
  * The seated red has to pass under it. Over it, the switch's leads would cut the red lead in Steps 47 - 48: the earlier study's
    candidate 1, and the same parity argument in reverse.
  * The lying red never meets it.
  * The buzzer passes over it in the carry. A crossing made at the moving end is therefore "red over", while "red under" is needed.
  * So the red lead and the tan lead must pass through each other once, in Step 43 or else in Steps 47 - 48.
* **Black and the LCD wires.** The four LCD wires were laid over the lying black lead in Steps 36 - 39, between the board's +z end and
  the LCD lying beside it. The seated black runs along the front, outside them. Black has to come out from under them, and their ends
  are on the board and on the LCD.
* **Red, orange and yellow.** This crossing comes from the current seated red, which runs from j4 under the orange and yellow arches
  beside the Nano Board. The lying red leaves j4 to the back and never passes under them. The new seated way (section 3) comes into
  j4 from the back as the lying one does, and crosses over the orange and yellow further along. The linking goes to 0 and the
  orange and yellow crossings disappear (motioncheck confirms this).

To get Step 43 to 0 problems, one of these would have to change:

* Steps 34 - 39: lay the LCD wires under the black lead, or route the lying black elsewhere. Every option I found was absurd.
* The order of the build: the buzzer's leads plugged in after the buzzer is seated.
* Step 43 shown with `reappear=True`, the fade-out/fade-in used for the PMG's Step 42. Nothing then moves through anything.

Moving the red/tan crossing into Steps 47 - 48 instead does not reduce the total.

## 2. The design: four beats

Path: `[BUZZER_LYING, BUZZER_LIFT, BUZZER_UP, BUZZER_UP, ZERO]`. Each beat is 800 ms; the step was three beats and is now four.

| beat | buzzer | leads |
|---|---|---|
| 1 lift | from lying on its side to **upright**, its middle 70 mm above where it lay (`BUZZER_LIFT`, a pure move [-0.4, 57.2, 176.1]) | Red's run along the back strip stays where it lay; only its last ~30 mm rises to the stubs. Black rises from under the LCD wires up and over them (the four forced crossings, 0.143 - 0.162). |
| 2 carry | straight across to 45 mm above its seat, with no turn | Each lead goes from its lifted shape to a **held** shape. The held shape lies over the lead's seated way, held up above it: red low in the back strip by j4, then up 15 - 30 mm over orange/yellow, the jumpers' ends and the tan lead; black up out of (-) blue and along the front at y 934 - 943. Red's low run swings round j4 through the back strip from +z to -z. |
| 3 settle | stays still over its seat | Each lead is lowered onto its way (the over-seat shape of now). Red goes in under the switch's tan lead (the forced crossing, 0.62 - 0.63). |
| 4 lower | into its seat | As now: the run from the hole to the junction stays put. |

Why the design takes this form, from the variants I tried (design1 - design11 in the scratch):

* **Standing the buzzer upright in the lift** makes the carry a straight move. With the turn spread over the carry, the ends of the
  leads by the stubs either turned with the buzzer (full skinning: folds, and red crossing black by the stubs) or did not (stretch:
  they could not untwist). Red crosses over black by the stubs when lying. A pure move of the lift keeps that crossing, and the turn
  then undoes it with nothing passing through.
* **The lifted shapes are stretch leads.** That pairs them by share of length with the lying shapes (the lift) and with the held
  shapes (the carry). Tail_from pairing needed shapes of equal length on both sides; otherwise it bunched the new length at one point,
  and runs grew out of a point or folded. During the straight carry, "carried by the ends' moves only" is exact.
* **The held stop exists because of a pocket.** Red's seated way threads a pocket: under the tan lead, beside the green jumper's
  arch, behind the black and green arches and in front of the purple and blue. No straight blend from a lead that is still at +z can
  reach it without clipping the arches. A 3-beat version (lifted straight to over-seat) gives 15 contact episodes. The pocket can
  only be entered from above, on its -z side. The held shape puts the lead there (and over everything else) first, and the settle
  beat lowers it. The held, over-seat and clamped shapes are all paired at the junction (tail_from 94.7 red, 101.4 black), so in the
  settle and the lowering the run before the junction stays still or drops in place.
* **The lift is 70 mm**, so that black's lead under the stub clears the tops of the LCD wires (y 940) in the carry. At 60 mm black
  crosses the LCD purple a second time in the carry; 64 and 66 are also clean (see the caveats).

## 3. Paste-ready code for guide.py

(a) **Replace** the line `BUZZER_LIFT = tidy(compose([0.0, 60.0, 0.0], BUZZER_LYING, BUZZER_LYING['at']))` (about line 751) with:

```python
BUZZER_LIFT = tidy((apply_pose(BUZZER_LYING, np.array([BUZZER_LYING['at']]))[0] + [0.0, 70.0, 0.0] - np.asarray(BUZZER_LYING['at'])).tolist())
                                                                    # (Step 43: stood upright as it is lifted, its middle 70 mm over where
                                                                    # it lay, so that the carry over the board is a straight move)
```

**Delete** `BUZZER_LIFT_WAY` (no longer used). `BUZZER_UP` stays `[0.0, 45.0, 0.0]`. `buzzer_plugged`'s `stretch` argument is then
unused and can go. In the comment above `BUZZER_WAY`, "and lifted 60 mm over where it lies (Step 43)" no longer applies.

(b) **Replace** `BUZZER_SEAT_WAY['red']`. The first 14 points are unchanged; from [664.9, 924.6, 1292.6] on, the way goes over the
orange and yellow jumpers into the back strip and in to j4 from the back:

```python
BUZZER_SEAT_WAY = {'red': [[674.5, 891.3, 1235.6], [674.5, 892.9, 1239.5], [674.5, 895.4, 1246.8], [674.5, 898.2, 1250.6], [674.5, 902.0, 1254.5], [674.5, 905.5, 1258.0], [674.5, 909.0, 1261.5], [674.1, 912.5, 1265.0], [672.9, 915.7, 1268.2], [670.4, 919.1, 1271.6], [667.9, 921.9, 1274.5], [665.7, 924.4, 1278.3], [664.8, 925.6, 1283.0], [664.8, 925.4, 1287.8], [664.9, 924.6, 1292.6], [664.4, 924.0, 1297.4], [662.0, 922.6, 1302.8], [658.6, 917.0, 1307.4], [656.2, 911.0, 1312.4], [655.6, 907.4, 1318.2], [656.0, 906.4, 1324.0], [657.4, 906.2, 1328.8]],
                   'black': ...unchanged...}
```

The comment above it should then read: "... over the jumpers (red over their ends in row i, then over the orange and yellow jumpers
and down into the back strip of the board, in to j4 from the back as the lying lead goes in: linked under them, it had to pass
through them in Step 43; docs/research/lac/round2/step43_low.md), ...". `seated_from_buzzer`, `buzzer_over_seat` and `buzzer_clamped`
are unchanged.

(c) **Add** these after `buzzer_clamped`:

```python
# Step 43 (Lee, 21 Oct 2026: "pass the red and black wires over the black/green/purple/blue wires instead of clipping through and under
# them"), in four beats: lifted and stood upright (BUZZER_LIFT); carried over its seat, each lead held up over its seated way
# (BUZZER_HELD_WAY); held there while the leads are laid onto their ways; lowered. What still passes through cannot be avoided (the
# lying leads are linked with it: docs/research/lac/round2/step43_low.md): the black lead through the four LCD wires as the buzzer is
# lifted (they were laid over it, Steps 36 - 39), and the red lead through the switch's lying tan lead as it is laid in under it.
BUZZER_LIFTED_FROM = {'red': 55.0, 'black': 9.0}                       # (mm from the hole of the lying lead kept as it lay)
BUZZER_LIFTED_WAY = {'red': [[648.5, 914.0, 1386.0], [652.0, 930.0, 1395.0], [659.0, 940.0, 1403.0], [667.0, 943.0, 1408.0], [672.0, 944.5, 1409.2]],
                     'black': [[699.0, 928.0, 1342.0], [697.0, 943.0, 1346.0], [690.0, 950.0, 1355.0], [683.0, 951.5, 1368.0], [678.5, 950.5, 1385.0],
                               [676.3, 947.5, 1399.0], [675.7, 945.5, 1405.0]]}   # (black up over the LCD wires)
BUZZER_HELD_FROM = {'red': 18.0, 'black': 14.0}                       # (mm from the hole of the seated way already laid)
BUZZER_HELD_WAY = {'red': [[656.5, 913.0, 1313.5], [659.5, 927.0, 1308.0], [663.2, 935.5, 1302.5], [665.0, 938.0, 1296.0], [665.0, 938.5, 1288.0],
                           [665.8, 938.5, 1280.5], [668.5, 938.0, 1274.0], [671.0, 937.5, 1267.0], [673.2, 936.5, 1259.0], [674.3, 935.0, 1250.0],
                           [674.5, 934.0, 1242.0], [674.5, 934.5, 1237.0]],
                   'black': [[698.6, 922.0, 1335.0], [698.5, 934.0, 1327.0], [698.5, 940.0, 1312.0], [698.5, 942.5, 1295.0], [698.3, 943.0, 1281.0],
                             [696.5, 941.0, 1270.5], [693.5, 938.0, 1262.5], [689.5, 936.0, 1255.0], [684.5, 935.5, 1247.0], [679.5, 936.0, 1239.5]]}


def run_to(line, mm):
    """A line from its first point up to `mm` mm along it, ending exactly there."""
    line = np.asarray(line, float)
    s = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))]
    end = np.array([np.interp(mm, s, line[:, k]) for k in range(3)])
    return np.vstack([line[s < mm - 1e-6], end])


def buzzer_on(colour, exit_, pose, head, way):
    """A buzzer lead drawn from the hole: `head` as it is, then smoothly through `way` to its stub (the buzzer at `pose`), leaving the
    stub straight for BUZZER_OUT mm."""
    q = posed_line(pose, [exit_, np.add(exit_, [0.0, -1.0, 0.0])])
    e, d = q[0], unit(q[1] - q[0])
    first = e + d * BUZZER_OUT
    body = W.smooth([head[-1], *[np.asarray(c, float) for c in way], first], start_dir=unit(head[-1] - head[-3]), end_dir=-d, spacing=0.5)
    return W.resample(W.join(head, body, W.straight(first, -d, BUZZER_OUT)), 1.0)


def buzzer_lifted(colour, cap, exit_):
    """Lifted and stood upright (Step 43's first stop): the lying lead as it lay up to BUZZER_LIFTED_FROM, then BUZZER_LIFTED_WAY up to the
    stub. A stretch lead: paired with the lying lead and with the held one by share of length (the carry is a straight move, so being
    carried by its ends' moves only is exact)."""
    lying = buzzer_line(colour, cap, exit_, BUZZER_LYING, BUZZER_WAY[colour])[::-1]
    line = buzzer_on(colour, exit_, BUZZER_LIFT, run_to(lying, BUZZER_LIFTED_FROM[colour]), BUZZER_LIFTED_WAY[colour])
    return W.route(line, a=cap, b=BUZZER, b_at=BUZZER_LIFT, b_from=BUZZER_LIFTED_FROM[colour], stretch=True)


def buzzer_held(colour, cap, exit_):
    """Held up over the seat (Step 43's second stop): the seated way from the hole up to BUZZER_HELD_FROM, then BUZZER_HELD_WAY, over the
    rest of the way, to the stub. Paired with the next shape (buzzer_over_seat) as that one is paired with the clamped one."""
    over = buzzer_over_seat(colour, cap, exit_)
    line = buzzer_on(colour, exit_, BUZZER_UP, run_to(over['pts'], BUZZER_HELD_FROM[colour]), BUZZER_HELD_WAY[colour])
    return W.route(line, a=cap, b=BUZZER, b_at=BUZZER_UP, b_from=over['tail_from'], tail_from=over['tail_from'])
```

(d) **Step 43's call** (about line 1163):

```python
# (lifted and stood upright, carried over its seat with its leads held up over their ways, held while they are laid onto them, and
# lowered: a stop each, its leads keeping pace stop by stop, then clamped as the CAD has them)
g.place('Lower the buzzer in between the two F7s, its ears into their slots.', move=[BUZZER], path=[BUZZER_LYING, BUZZER_LIFT, BUZZER_UP, BUZZER_UP, ZERO],
        lines=False, eye=[dict(id=BUZZER, **near('near-above'))],         # (above the buzzer: Lee, 21 Oct 2026)
        wires_done={f'buzzer {c}': [buzzer_lifted(c, cap, e), buzzer_held(c, cap, e), buzzer_over_seat(c, cap, e), buzzer_clamped(c, cap, e)]
                    for c, cap, _, e, _, _ in BUZZER_LEADS}, **CASE_CAMERA)
```

The lying routes (Steps 33c - 42c) are not changed at all. The paste-ready code was run on copies of guide.py's helpers
(`build_final.py`). It reproduces the checked routes to 0.01 mm. The route summaries (length, b_from, tail_from, stretch):

| | lifted | held | over the seat | clamped |
|---|---|---|---|---|
| red | 126.5, 55, -, stretch | 131.7, 94.7, 94.7 | 150.6, 94.7, 94.7 | 132.9, 94.9, 94.9 |
| black | 118.6, 9, -, stretch | 142.9, 101.4, 101.4 | 157.1, 101.4, 101.4 | 150.6, 101.8, 101.8 |

## 4. Checks

**motioncheck**, on a steps copy built as stepgen writes it: Step 43c's path and its stops replaced, with `wire_via` holding the
lifted, held and over-seat shapes and the new clamped red in every view from Step 43c on.

```
$ motioncheck.py "LAC Build Instructions" --steps steps_low.json --moments 39 "Step 43c"
Step 43c  buzzer red    and switch tan    centre lines 0.19 mm apart at 0.62, near [671.2, 926.5, 1270.0]
Step 43c  buzzer black  and lcd teal      centre lines 0.86 mm apart at 0.15, near [684.9, 934.3, 1358.6]
checked 1 views in motion; 2 problems
$ ... --moments 199 "Step 43c"
Step 43c  buzzer red    and switch tan    centre lines 0.19 mm apart at 0.62, near [671.2, 926.5, 1270.0]
Step 43c  buzzer black  and lcd purple    centre lines 0.25 mm apart at 0.16, near [684.9, 939.4, 1358.9]
Step 43c  buzzer black  and lcd blue      centre lines 0.85 mm apart at 0.14, near [684.8, 931.9, 1357.8]
Step 43c  buzzer black  and lcd yellow    centre lines 0.85 mm apart at 0.15, near [685.0, 936.5, 1358.8]
Step 43c  buzzer black  and lcd teal      centre lines 0.86 mm apart at 0.15, near [684.9, 934.3, 1358.6]
checked 1 views in motion; 5 problems
```

For comparison, the current steps.json at 39 moments has 14 problems: red through yellow, orange, green, black, purple and blue;
black through purple, the LCD blue, yellow and teal, green, the tan lead and the black jumper.

Contact episodes at 399 moments (gap under motioncheck's limit), from `episodes.py` over a precomputed clearance field. This checker
matches motioncheck to within about 0.05 mm on the current steps.

* black / lcd blue 0.143 - 0.145; teal 0.148 - 0.150; yellow 0.152 - 0.155; purple 0.158 - 0.162 (lift beat)
* red / switch tan 0.620 - 0.630 (settle beat)
* nothing else: no part, no other wire, red against black and no fold of either lead anywhere in the motion

**Steps 44c - 56c in motion** (every view where a wire moves, 39 moments) give the same 16 problems with the design as with the
current steps.json: the potentiometer's leads in Steps 46c and 52c. None of them involves a buzzer lead.

**wirecheck** (every view at rest): the same single problem with and without the design, `Step 12 jumper purple / NAUO22 0.04 mm`
(not this work).

**At rest**: surface gaps in mm, with the parts posed as they are at each stop. The lead's own cap and the buzzer are skipped, as
wirecheck does.

| shape | red | black |
|---|---|---|
| lifted (stop 1) | yellow cap at j3 0.94, yellow jumper 0.84 (both at the drop into j4, as in the lying shape), USB cable 2.42, orange 5.0 | pot tan 6.0, pot black 7.9, LCD purple 10.1 (over it) |
| held (stop 2) | yellow cap 1.63, yellow 1.65, RTC 4.6, orange 5.8, tan lead 8.9, green 9.7 | pot tan 1.39, pot red 6.6, LCD yellow 7.3 |
| over the seat (stop 3) | green 0.32 (the existing run over its row-i end), yellow 1.64, black jumper 2.31, orange 2.32, RTC 2.87 | pot tan 0.41, green 0.70, LCD yellow 1.47 (all as now) |
| clamped (Steps 43c - Completed View, every view) | green 0.32, buzzer black 0.57 by the stubs, yellow cap 1.63 (1.03 within 3 mm of the hole), orange 2.32, RTC 2.87; the USB cable, F2 and every other part > 4 | unchanged |

For comparison, the current clamped red has green 0.33 and yellow cap 1.66. The new part of the seated way has nothing closer than
the orange jumper at 2.32 mm.

## 5. What it looks like

* **Lift (0 - 0.25).** The buzzer rises from where it lies past the breadboard's end and turns upright as it rises. The red lead stays
  where it lay along the back strip of the board. Only its end lifts off and rises to the stub, a lead hanging from the buzzer. The
  black lead lifts off the board's end and comes up over the LCD wires, passing through them in a flicker (about 60 ms in all).
* **Carry (0.25 - 0.5).** The upright buzzer glides straight over the board to above its slot. The red lead's short run by j4 swings
  round the hole, low in the back strip, from pointing towards the buzzer's old place to pointing along the board. The rest of the red
  lead lifts and lays itself out about 15 mm above its way: over the orange and yellow jumpers, over the row-i ends, over the tan lead
  and down behind the buzzer. The black lead swings round (-) blue, above the potentiometer's leads, and lays itself along the front
  edge above its way. Both stay above every jumper.
* **Settle (0.5 - 0.75).** The buzzer waits above its slot while both leads drop onto their ways. Red goes in under the tan lead (a
  flicker through it, about 30 ms) and black lies over the jumpers' rail ends and the tan lead's end.
* **Lower (0.75 - 1).** As now: the buzzer goes down between the F7s, and only the run behind it moves.

## 6. Caveats and options

* **The settle beat has the buzzer standing still** for 800 ms. A variant where it sinks 5 mm during the settle is just as clean
  (5 forced episodes, nothing else): the third stop `[0, 50, 0]`, the held shapes drawn at it, and the last three points of each
  `BUZZER_HELD_WAY` raised 5 mm.
* **Framing.** CASE_CAMERA's frame (radius 110 about [690, 915, 1270]) did not contain the lifted buzzer before either. On screen,
  "up" reached 124 mm above the frame's middle before; upright and 70 mm up, the buzzer's top reaches 137. Look at Step 43 in Lee's
  window. If the top is cut off, a 64 or 66 mm lift (with `BUZZER_LIFTED_WAY`'s heights scaled down by the same amount over y > 905)
  is also clean. 60 mm is not.
* **The forced crossings are Lee's call.** They cannot be removed in Step 43 alone (section 1). They are now five crossings of a few
  frames each, against 14 slow sweeps. To remove them entirely needs one of section 1's options: `reappear=True` for Step 43, or a
  change to Steps 34 - 39 or to the build order.
* **Not checked in the browser** (no player run). The checks are motioncheck and wirecheck on the steps copy, and the blending is
  replicated from player.js. After applying: run guide.py, then motioncheck "Step 43c" at 39 and 199 moments, then run-through and
  look at Steps 43 - 44 in the player.
