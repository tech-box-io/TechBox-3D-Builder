# ---- paste-ready for guide.py (the buzzer section). Replaces BUZZER_LIFT_WAY, BUZZER_LIFT and BUZZER_SEAT_WAY['red'], adds the rest.
PATCH = r'''
# Step 43 (Lee, 21 Oct 2026: "pass the red and black wires over the black/green/purple/blue wires instead of clipping through and under
# them"), in four beats: the buzzer is lifted and stood upright as it goes up (BUZZER_LIFT: upright, its middle 70 mm over where it lay,
# so that the carry over the board is a straight move with no turn); carried over its seat, each lead held up over its seated way
# (BUZZER_HELD_WAY); held there while the leads are laid onto their ways; and lowered. The red lead's seated way goes in to j4 from the
# back strip of the board, as the lying lead does, over the orange and yellow jumpers (not under them), so that its run by j4 only
# swings round its hole, low in the back strip. What still passes through (it cannot be avoided: the lying leads are linked with them,
# docs/research/lac/round2/step43_low.md): the black lead through the four LCD wires as the buzzer is lifted (they were laid over it,
# Steps 36 - 39), and the red lead through the switch's lying tan lead as it is laid in under it.
BUZZER_LIFT = tidy((apply_pose(BUZZER_LYING, np.array([BUZZER_LYING['at']]))[0] + [0.0, 70.0, 0.0] - np.asarray(BUZZER_LYING['at'])).tolist())
BUZZER_UP = [0.0, 45.0, 0.0]
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
    L, j = seated_from_buzzer(colour, cap, exit_)
    over = buzzer_over_seat(colour, cap, exit_)
    line = buzzer_on(colour, exit_, BUZZER_UP, run_to(over['pts'], BUZZER_HELD_FROM[colour]), BUZZER_HELD_WAY[colour])
    return W.route(line, a=cap, b=BUZZER, b_at=BUZZER_UP, b_from=over['tail_from'], tail_from=over['tail_from'])
'''
SEAT_RED = r'''
BUZZER_SEAT_WAY['red'] = BUZZER_SEAT_WAY['red'][:14] + [[664.9, 924.6, 1292.6], [664.4, 924.0, 1297.4], [662.0, 922.6, 1302.8], [658.6, 917.0, 1307.4],
                                                     [656.2, 911.0, 1312.4], [655.6, 907.4, 1318.2], [656.0, 906.4, 1324.0], [657.4, 906.2, 1328.8]]
'''
