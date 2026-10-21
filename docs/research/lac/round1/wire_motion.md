# LAC round 1 (Lee, 20 Oct 2026): why the wires misbehave mid-move, and the fix for each

Lee's notes: Steps 30 - 32 "the wire animations are crazy and fly off the screen mid-animation"; 33 - 34 "the same; the red breadboard
wire has a visible kink near the breadboard"; 36 - 39 "the breadboard wires do not extend into the wire ends at the LCD Screen (empty
space)"; 43 "the buzzer's wires animate all over the place and partially off the screen, and clip through other wires"; 46 "the
potentiometer's wires glitch through F9 and the front of F1"; 50 - 51 "the LCD's wires must stay behind F9 and wrap round into the LCD's
header".

**Versions.** Lee reviewed the steps.json made from HEAD (`c717aae`, guide.py of 19 Oct 23:43). While this was written, another session
was rewriting the same guide (working copy guide.py and steps.json of 20 Oct 21:58). Line numbers below are given as `HEAD:n` (what Lee
saw) and `wc:n` (the working copy at 21:58). In the working copy Lee's Step 46 (F1 carried round) is gone, so his Steps 50 - 51 are now
**Steps 49 - 50**. (At 22:03 guide.py changed again: the red buzzer lead now drops into j4 only 1 mm, under the yellow jumper's arch,
`BUZZER_ABOVE`; the red cap's own way, `[start, UP, ZERO]`, still passes through that arch: section 4, item 3.)

**How this was measured** (one process at a time, no guide.py run, no lac.glb):
- `tools/motioncheck.py` (with `--trace`) on the steps.json Lee saw (snapshot), on the working copy's (21:40, 21:58), and on copies
  patched with the fixes below.
- `tools/wirecheck.py` (at rest) on the same files.
- A Python copy of the player's motion (player.js `mixPose`, `alongPath`, the riding loop, `skinned`, `sampled`, `drawWires`), written
  for this report, to see where parts and wires are mid-move and how far off the camera's frame they go (motioncheck cannot: see 1.3).
  Scratch scripts (not in the project): `/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/46c40992-e0fc-4f94-b08e-62c20da998a4/scratchpad/emu.py`,
  `.../scratchpad/build_fix.py` (patches a steps.json as the fixes below would), `.../scratchpad/partclash.py` (a moving part's own
  mesh against the parts that stay put).

## 0. Summary

| Lee's step | What goes wrong | Fix | Working copy 21:58 |
|---|---|---|---|
| 30 - 32 | The cap's starting pose is written as a turn about the assembly's origin (1.7 m away); the player turns a part about its pose's `at` between two poses, so the cap (and its lead) swings out on a 1.7 m arc: 1.7 m from its hole, 13 - 15 frame-halves off screen, the lead 1.86 m long | Write the pose about the cap's middle (`compose(..., pivot)`) | Gone: the cap is now taken to its hole as the step opens (`path=[UP, ZERO]`), from its riding pose, which stepgen writes about the cap's middle |
| 33 - 34 | The same origin swing (the cap 0.5 - 0.7 m from its hole). Kink: the CAD's red lead (NAUO60) folds back on itself 8 - 10 mm over j4. The red cap held 18 mm over j4 sits in the yellow jumper's arch | Pivot; redraw the lead's last 12 mm; bring the red cap in under the arch | **Still swings** (`wc:651`); kink gone (new path-searched `BUZZER_WAY`); arch clash still there |
| 36 - 39 | The CAD's lying teal and blue wires stop 1.33 / 1.46 mm short of the CAD's own caps, and the guide's caps sit 0.45 mm further on: a 1.8 / 1.9 mm gap. Purple and yellow measure 4.3 mm inside their caps | Start every LCD wire inside its cap, along its axis | Done (`into_fem`, `wc:725-733`): all four 4.0 mm inside, measured |
| 43 | Origin swing of the buzzer (its in-between pose); the in-between stop had no route of its own (the clamped route twice); `stretch` leads are not turned with the buzzer's 120 degree turn; in Lee's version the buzzer lay under the potentiometer's leads and was lifted through them | Pivot; a route per stop, kept high; no `stretch` (`tail_from` on the drop into the hole) | Routes per stop added; **still swings** (`BUZZER_LIFT`, `wc:639`: 1.8 frame-halves off screen); `stretch` kept |
| 46 | The leads' run round F9's back edge paired with a run inside the case (share-of-length blend) cuts F9; `stretch` leads not turned with F1 cut F1; F1's own way passes through the LCD, breadboard, F3 and F9 | (see 7) | Step removed (F1 stays face down in front) |
| 50 - 51 (now 49 - 50) | The female end is the route's first end and the routes `stretch`: the run behind F9, a third of the way from the header, moves with the LCD by 84 %, so every move of the LCD sweeps it through F9; the in-between stop had no route; the CAD's standing teal/blue wires fold back on themselves | Routes from the breadboard to the header, `b_from` = `tail_from` at the point just round F9's back edge; a drawn shape per stop | New stops and shapes, but still female-first with `stretch`: in 49c three wires 2.0 - 2.1 mm into F9, three up to 2.0 mm into F4 (measured on its steps.json) |

Tested together (the fixes in 1, 4, 6, 8, on Lee's steps.json): no wire passes into any part in 43c, 50c, 51c, and in 33c only where the
two buzzer caps lying side by side overlap (0.5 mm: section 4, item 4); all 116 views clean at rest (wirecheck: 0 problems); every moving part and wire
stays within the frame (at most 0.73 of the half-frame), except the LCD at the stop where it is slid out in front (1.04: that step's
frame needs widening). What is left are sub-millimetre touches between wires for a moment.

## 1. The fly-off: poses turned about the assembly's origin (Steps 30 - 34, 43)

### 1.1 Mechanism

`compose(outer, inner, pivot=(0, 0, 0))` (stepgen.py:137-142) writes the composed pose as a turn about `pivot`, the origin unless one
is given (its docstring: "give the part's own middle, so that it glides sensibly when a later step moves it"). guide.py gives none at:

- `HEAD:488` `start = compose(FLAT_BESIDE, pot_cap_rel(cap, exit_))` (Steps 30 - 32);
- `HEAD:522` / `wc:651` `start = compose(BUZZER_LYING, buzzer_cap_rel(cap, exit_))` (Steps 33 - 34);
- `HEAD:666` `via(compose([0.0, 60.0, 0.0], BUZZER_LYING))` / `wc:639` `BUZZER_LIFT = tidy(compose([0.0, 60.0, 0.0], BUZZER_LYING))` (Step 43).

So Step 30's path starts at `{"t": [1592.54, 1609.41, 2899.58], "r": [-0.707107, 0.707107, 0, 180], "at": [0, 0, 0]}` (the same physical
place as the riding pose, but written about the origin). Between two poses the player turns the part about `b.at`, or `a.at` when `b`
has no turn (player.js:57-65, `const at = (turn(b) ? b.at : a.at) || ZERO`), and moves that point in a straight line. From that pose to
`UP = [0, 18, 0]` (no turn) the cap is turned 180 degrees about the origin, 1.7 m from the parts, while the origin's image slides from
(1592, 1609, 2900) to (0, 18, 0): half way the cap is at (1636, 1856, 321). Its lead follows it (the lead's far end is tied to the cap,
player.js:113-135). It plays both ways: going back from Step 30c the way is reversed (player.js:693-703) and swings again.

### 1.2 Measured (the player's motion, Lee's steps.json; "frame-halves" = how far off the camera's centre, 1 = the frame's edge)

| View | Moving part | Furthest | Lead length (mm) |
|---|---|---|---|
| 30c | cap NAUO34 | (1636, 1856, 321) at 0.25; 13.7 frame-halves | 1866 (route 50 to 288) |
| 31c | cap NAUO33 | 13.4 frame-halves | 1859 |
| 32c | cap NAUO14 | 14.3 frame-halves | 1863 |
| 33c | cap NAUO58 | (1012, 656, 1539) at 0.175; 51 frame-halves | 847 |
| 34c | cap NAUO59 | (1022, 648, 1534); 54 frame-halves | 876 |
| 43c | buzzer NAUO62 | (1223, 661, 1602) at 0.275; 1.77 frame-halves | 830 |
| 43c, working copy | buzzer | (1246, 656, 1616) at 0.475; 1.81 frame-halves | |

With the same poses written about the moving part's middle: 30c 0.63, 33c 0.24, 34c 0.21, 43c 0.64 frame-halves at most.

### 1.3 Why motioncheck did not report it

`tools/motioncheck.py:49-56` mixes two poses about the part's own middle, not about the pose's `at` as the player does, so it plays a
smooth glide and found only 2 sub-millimetre touches in 30c - 32c. Make it mix as the player does (then it reports the swing as the
wire passing through whatever the arc crosses; a frame check would name it outright):

```python
    def mix(a, b, k, part=None):
        """Part of the way from pose a to pose b as the player mixes them (player.js mixPose): the turn spread evenly about b's pivot (a's
        if b has none), that point moved in a straight line. A pose turned about a far point then swings its part round it, as on screen."""
        A, B = _matrix(a), _matrix(b)
        turned = lambda p: isinstance(p, dict) and p.get('r') and p['r'][3]
        c = np.asarray(((b if turned(b) else a).get('at') if (turned(a) or turned(b)) else None) or [0.0, 0.0, 0.0], float)
        R = Slerp([0, 1], Rotation.from_matrix([A[:3, :3], B[:3, :3]]))([k]).as_matrix()[0]
        M = np.eye(4)
        M[:3, :3] = R
        M[:3, 3] = (A[:3, :3] @ c + A[:3, 3]) * (1 - k) + (B[:3, :3] @ c + B[:3, 3]) * k - R @ c
        return M
```

(and, cheaply, after `M` is filled: report any moving or riding part whose middle is more than 1.5 camera radii from `v['camera']['target']`.)

### 1.4 Fix

In guide.py, next to `wire_at` (`wc:195`):

```python
def cap_mid(cap):
    """The middle of a Dupont cap's housing (seated). A pose of the cap is written about it: the player turns a part about its pose's
    `at` between two poses (player.js mixPose), and compose() writes the origin, 1.7 m away, unless it is given a pivot."""
    return np.asarray(CAPS[cap]['box'], float).mean(0).round(2)
```

then `start = compose(BUZZER_LYING, buzzer_cap_rel(cap, exit_), cap_mid(cap))` (`wc:651`; and `HEAD:488` with `FLAT_BESIDE` if that step
comes back), and for the buzzer `compose([0.0, 60.0, 0.0], BUZZER_LYING, BUZZER_LYING['at'])` (`wc:639`; `BUZZER_LYING['at']` =
[675.26, 918.29, 1224.7], the CAD pose's pivot, the buzzer's middle).

A guard in the generator would stop it for every kit: in `Guide.place` (stepgen.py), after `path = [p if isinstance(p, dict) else ...]`
(stepgen.py:1335),

```python
        # A pose turned about a point far from its part (compose() without a pivot: the origin) makes the player swing the part round that
        # point on its way to the next pose (player.js mixPose turns about the pose's `at`): write each turned pose about the part's middle.
        def about_own(p, i):
            if _rot(p) is None or np.linalg.norm(np.asarray(p.get('at', (0, 0, 0)), float) - self._pivot(i)) < 60.0:
                return p
            q = _pose_of(_matrix(p), self._pivot(i))
            return via(q) if isinstance(p, via) else q
        if move:
            path = [about_own(p, move[0]) for p in path]
        paths = {i: [about_own(p, i) for p in way] for i, way in paths.items()}
```

(the same for `ride=` lists, which the player mixes the same way, player.js:769). Riding poses are already written about the part's
middle (Step 29c's offset for NAUO34 has `at` [696.69, 899.11, 1330.61]), which is why the working copy's `path=[UP, ZERO]` steps no
longer swing.

## 2. How the player bends a wire from one shape to the next (what the other faults have in common)

- A route is tied to the part at each end. Every point moves with the far-end part by `ramp(u)` (0 for the first 10 % of the length,
  smoothly to 1 at 90 %) and with the near-end part by the rest (player.js:102, 120-129). `b_from`: up to that many mm from the first end
  a point does not follow the far end at all (player.js:123; wires.py:25-26).
- When a wire changes shape, if either route says `stretch` both are carried by their ends' moves only, **not turned with their parts**
  (player.js:111-117, 163-164), and paired point for point by share of length (player.js:177). Otherwise by distance from the first end;
  with `tail_from` in both, the run up to there by distance from the first end and the rest by distance from the last (player.js:167-176).
- `wires_done=[A, B]` gives a wire one shape per beat (player.js:775-777); `[R, R]` (the final shape as the in-between one) means the
  in-between stop has no shape of its own: the final shape is just dragged there by its end.

## 3. Steps 30 - 32

Cause: section 1 only (the blends themselves are tame: motioncheck 30c - 32c, 2 touches of 0.75 mm between the red and tan leads at
0.10). Working copy: no longer swings (`wc:595-601`, `path=[UP, ZERO]`; measured on its steps.json: the cap at most 0.37 frame-halves out).

## 4. Steps 33 - 34

1. **The swing**: section 1. Still in the working copy (`wc:651`; its steps.json: caps 1.44 - 1.48 frame-halves out, (1164, 780, 1735)).
   Fix: `cap_mid` pivot (1.4).
2. **The kink** (Lee's version, `HEAD:523`: the plugged lead is the CAD's NAUO60). Its centre line, from the cap in j4:
   0.0 mm (661.10, 901.11, 1334.46), 5.8 (660.98, 906.95), 7.9 (660.98, **909.04**), 8.7 (661.10, 908.25), 9.0 (661.06, **907.96**),
   9.7 (660.80, 908.63), 10.7 (660.35, **909.45**): up, back down 1.1 mm, up again, a 175 degree fold over 3 mm, 8 - 10 mm over j4
   (wire-paths.json `lines.NAUO60`). The clamped copy (NAUO65, Step 43 on) has no fold (at most 28 degrees). The working copy draws new
   leads (`BUZZER_WAY`, `wc:633-634`), which removes it. To keep the CAD's shape instead (tested: worst bend 30 degrees over 3 mm, 2.05 mm
   from the yellow jumper):

```python
def cad_into_cap(key, cap, clear=12.0, rise=7.0):
    """A CAD lead from its part into a male cap, its last `clear` mm drawn again: a smooth bend into a straight `rise` mm drop into the
    cap's housing. (The CAD's buzzer red lead, NAUO60, folds back on itself 8 - 10 mm over j4: y 909.04, 907.96, 909.45.)"""
    line = cad_line(key, cap)[::-1]                                 # (from its part to the cap)
    s = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))]
    keep = line[s <= s[-1] - clear]
    top = wire_at(cap) + [0.0, rise, 0.0]
    bend = W.smooth([keep[-1], top], start_dir=unit(keep[-1] - keep[-3]), end_dir=[0, -1, 0], spacing=0.5)
    return W.resample(W.join(keep, bend, W.straight(top, [0, -1, 0], rise)), 1.0)
```

3. **The red cap in the yellow jumper.** The yellow jumper (j3 to i29) rises from j3 and turns over j4 at y 913 (route at (661.0, 913,
   1334.5)); the red cap held `UP` (18 mm) over j4 spans y 911 - 923 (motioncheck 33c: "jumper yellow into NAUO58 0.75 mm at 0.50", in
   Lee's version and the working copy alike). Bring it in from beside j4, 5 mm up, under the arch (tested: that clash is gone):
   `path=[start, via([-14.0, 5.0, 0.0]), [0.0, 5.0, 0.0], ZERO] if colour == 'red' else [start, UP, ZERO]` (`wc:654`).
4. Minor: the two caps lying side by side overlap (their exits are 1.52 mm apart, the caps 1.75 mm across: "buzzer black into NAUO58
   0.5 - 0.66 mm" at 0.10 of 33c; under wirecheck's 5 mm end allowance). A lead in 34c touches the potentiometer's leads for a moment
   (0.21 - 0.64 mm) in Lee's version only.

## 5. Steps 36 - 39: the gap at the LCD's header

Each LCD wire is `lcd_route(key, fem, male, LCD_LYING)` (`HEAD:585-587`): the CAD's lying centre line from the female end. Measured with
the female caps where they ride on the lying LCD (wire end in the cap's own seated frame; the wire leaves the cap through its +z face,
the header pin enters through -z; the pin's tip is 1.15 mm inside the +z face, z 1356.65, where the seated CAD wires end):

| Wire | CAD lying line | Its end vs the cap's wire face | Why |
|---|---|---|---|
| purple | NAUO83 | 4.3 mm inside | |
| yellow | NAUO85 | 4.3 mm inside | |
| teal | NAUO87 | **1.78 mm outside**, 19 degrees off the axis | the CAD's line stops 1.33 mm short of the CAD's lying cap NAUO79 (wire-paths.json `cap_a`), and the guide's cap (NAUO99 posed by `lcd_lying`) sits a further 0.45 mm on from NAUO79 |
| blue | NAUO92 | **1.91 mm outside** | 1.46 mm short of NAUO78, + 0.45 |

During the moves of 36c - 39c the end stays tied to the cap (both shapes' first points are moved by the cap's own move, player.js:116-117),
so the gap is the same at rest and in motion. `F_OFF` ([0, 0, 15] in the LCD's frame, `HEAD:540`) is the right way off the pin (+z).
The working copy's `into_fem` (`wc:716-733`: the line restarted 4 mm inside the cap along its axis) closes it: measured on its steps.json,
all four 4.0 mm inside at Steps 39c, 49c, 50c. If Lee still sees empty space at purple or yellow, it is not the wire's end (4.3 mm inside
before, 4.0 now): a screenshot would show what it is.

The CAD's standing shapes have a fault of their own (they come back in Steps 49 - 50): NAUO119 and NAUO120 (teal, blue) run +z out of
the cap to z 1360.0, back to 1358.4, then on (172 and 175 degree folds, 18 - 20 mm from the cap). `into_fem` only redraws the first
3.5 mm, so it keeps them.

## 6. Step 43: the buzzer lowered between the F7s

Lee's version (`HEAD:666-668`): `path=[BUZZER_LYING, via(compose([0, 60, 0], BUZZER_LYING)), BUZZER_UP, ZERO]`,
`wires_done={...: [clamped] * 2}` with `stretch=True`.

1. The swing (section 1): the via pose is about the origin, so from it to `BUZZER_UP` the buzzer turns 120 degrees about the origin.
2. No shape for the in-between stop: the clamped CAD lead (drawn for the buzzer seated) is dragged up 45 mm at the buzzer's end and blended
   from the lying shape by share of length; motioncheck 43c (which does not see the swing, 1.3): 11 - 14 contacts with the jumpers, the LCD wires and
   the switch's tan lead (0.12 - 1.05 mm).
3. `stretch` on both shapes: the run leaving the buzzer is not turned with its 120 degree turn (player.js:111-117).
4. In Lee's version the potentiometer's leads run 10.8 mm over the lying buzzer (y 921 over its top at 910.2, x 681 - 688): lifting it
   goes through them ("pot red/tan/black into NAUO62 1.56 - 1.67 mm"). In the working copy F1 lies in front, so nothing is over it now.

Working copy (`wc:631-646, 823-826`): a shape per stop (`BUZZER_LIFT_WAY`, `BUZZER_UP_WAY`), good; but `BUZZER_LIFT` is still about the
origin (1.81 frame-halves out, measured on its steps.json) and `buzzer_plugged` still `stretch=True`. Change:

```python
BUZZER_LIFT = tidy(compose([0.0, 60.0, 0.0], BUZZER_LYING, BUZZER_LYING['at']))   # (about the buzzer's own middle)


def buzzer_plugged(colour, cap, exit_, pose, way):
    """A buzzer lead from its exit (the buzzer at `pose`) through `way` and down into its hole; carried whole with the buzzer (no stretch:
    it turns with it), its straight drop into the hole (into_hole: `above` + 4 mm) shared between shapes (tail_from)."""
    q = posed_line(pose, [exit_, np.add(exit_, [0.0, -1.0, 0.0])])
    above = BUZZER_ABOVE[colour]                                    # (as at 22:03; 10.0, into_hole's default, without it)
    line = into_hole(cap, q[0], unit(q[1] - q[0]), way, above=above)
    return W.route(line, a=BUZZER, b=cap, a_at=pose, tail_from=round(W.length(line) - (above + 4.0), 1))
```

and the clamped shape the same way, `line = cad_line(k2, cap)[::-1]`, `W.route(line, a=BUZZER, b=cap, tail_from=round(W.length(line) - 8.0, 1))`
(`wc:826`; the CAD's lead is straight for its last 6 - 8 mm). The lying shapes of Steps 33 - 34 then lose `stretch` too, which changes
nothing there (their blend from the straight leads is still by share of length, since those `stretch`). Tested on Lee's file with shapes of
the same kind (the buzzer lifted 70 mm, then over its seat, each shape kept high, at y 928 - 960): no lead into any part, the buzzer
itself touching only F7B as its ears enter the slots, at most 0.73 frame-halves out; 12 - 15 sub-millimetre touches with the jumpers as
the leads settle. Two details from that test: give the two leads separate control points (with one shared point they meet, 0.02 mm), and
end each shape with a control point straight over its hole, so that the shared drop is entered vertically (with the last one 4 - 8 mm off
the hole's axis the blend made a 90 degree corner at the top of the drop for a moment).

## 7. Step 46 (Lee's numbering): F1 carried round, its leads through F9 and F1

Gone from the working copy (F1 stays face down in front until it is stood up). For the record, measured on Lee's version (`HEAD:675-679`):

- The leads (`POT_WAY`, F1 face down past the breadboard's end) pass F9's plane behind its back edge (x 681 - 688; F9 is x 689 - 720.3,
  with a solid strip x 689 - 701.5 at every height and a window open to the front for y 898 - 941). `POT_OTHER` (F1 at the far end) runs
  inside the case at x 700 - 735. Paired by share of length (`stretch`), straight blends between the two cross F9's solid strip:
  pot red/tan/black 2.0 - 2.1 mm into F9 at 0.30 - 0.35.
- The in-between stop (F1 upright in front) had no shape (`[POT_OTHER] * 2`), and with `stretch` the run leaving the pins is not turned as
  F1 turns 90 degrees onto its face: 2.1 mm into F1 at 0.65 - 0.75 ("the front of F1").
- F1's own way passes through the lying LCD (60 of 4000 sample points), the breadboard, F3, the Nano and F9 at 0.225 - 0.25.

If it comes back: F1 lifted and turned out in front of the case, not over it; a shape per stop without `stretch`, `tail_from` at the 14 mm
drop; and, simplest of all, carry F1 round **before** F9 goes in (published order: F9, then F1), so that the leads never go round F9 (a
question for Lee). A first cut of that (F1 up 100 mm and 150 mm out face down, upright 60 mm up in front, then laid down) had F1 clear of
the case and no lead through F9, but the leads still crossed F1 during its 180 degree turn (2.1 mm) and each other.

## 8. Steps 50 - 51 (now 49 - 50): the LCD's wires behind F9

Geometry (lac-guide.glb, measured): F9 x 689.0 - 720.3, z 1354.28 - 1357.28; its back strip x 689 - 701.5 is solid at every height, and
it has a window open to the front edge for y 898 - 941 (x 701.5 - 720.3), the LCD's board ends in two notches at y 944 - 947 and
890 - 894. The female caps sit on the header pins at x 702.7 - 704.5, z 1349.8 - 1357.8, their wire faces 0.5 mm past F9's far face. Every
CAD shape of these wires (lying, standing, seated) comes out of the header along +z, runs along F9's far face to x 680 - 688 and comes
round F9's back edge into the case (they cross F9's plane at x 677 - 687): that run is what Lee calls "behind F9".

What goes wrong (Lee's version, `HEAD:585-587, 695-701`; motioncheck 50c: the four wires 2.06 - 2.11 mm into F9 at 0.25 - 0.65, and
into the LCD and each other's caps):

1. **The female end is the route's first end, and the routes `stretch`.** The run behind F9 lies about a third of the way from the header
   (u = 0.3: it follows the LCD by 1 - ramp(0.3) = 0.84). When the LCD is 40 mm out in front (the in-between stop), that run is moved
   34 mm towards the front, through F9's solid strip, and it sweeps back through it as the LCD comes in.
2. **No shape for the in-between stop**: `[LCD_STAND_ROUTE[c]] * 2`.
3. The CAD's standing teal and blue fold back on themselves at the notch (section 5).
4. The LCD's own way, lying to standing, passes through F3 and the breadboard (74 and 2 of 4000 sample points at 0.275).

The working copy (`wc:851-899`: stood up through a pose half way round, slid along itself, angled 14 degrees with its F8 end in F8's notch
(the published pose), straightened and pushed 14.9 mm through F8, slid back into F9) gives every stop a shape through the point where the
seated wire rounds F9's back edge, which is right. But the routes are still female-first with `stretch` (`lcd_way`, `lcd_route`), so between
stops the run behind F9 still follows the LCD: on its steps.json (21:58), 49c has three wires 2.03 - 2.11 mm into F9, three up to 2.04 mm
into F4 and two 1.42 mm into the LCD itself; 50c purple 0.54 mm into F9.

**Fix: wires from the breadboard to the header, the run round F9's back edge held still.** With the male end first (`a`, in the
breadboard, which does not move) and the female end last (`b`, on the LCD), `b_from` stops the run up to the back edge following the LCD
at all, and the same distance as `tail_from` keeps it in place when the shape changes (the LSM's jumper wires under its LED matrix, LSM
guide.py:242-266). After `lcd_route` (`wc:736`):

```python
# The LCD's wires run from the breadboard (male end, a) to the header (female end, b). The run from the breadboard round F9's back edge is
# the seated CAD wire's in every shape, up to the point just round it; from there on the wire follows the LCD (b_from) and changes shape
# between stops (tail_from). Female end first and `stretch`, the player moved every point with the LCD by a share growing along the wire
# (player.js:120-128): the run behind F9, a third of the way along, went with the LCD by 84 % and through F9.
def behind_f9(line):
    """The first point of a line from the breadboard that has come round F9's back edge (x < 689) to 3 mm past F9's far face (z > 1360.3)."""
    return next(i for i, p in enumerate(line) if p[2] > 1360.3 and p[0] < 689.0)


def lcd_lead(line, fem, male, lcd_pose, at):
    """An LCD wire along `line` (from the breadboard), the LCD at lcd_pose: the run up to the point nearest `at` stays put."""
    line = W.resample(line, 1.0)
    s = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))]
    k = round(float(s[int(np.argmin(np.linalg.norm(line - np.asarray(at, float), axis=1)))]), 1)
    return W.route(line, a=male, b=fem, b_at=lcd_pose, b_from=k, tail_from=k)


def lcd_tail(head, fem, lcd_pose, controls, reach=3.0):
    """`head` (from the breadboard round F9's back edge), then through `controls` into the female cap with the LCD at lcd_pose, the last
    `reach` mm along the cap's axis and 4 mm into it."""
    end, out = fem_end(fem, lcd_pose)
    body = W.smooth([head[-1], *[np.asarray(c, float) for c in controls], end + out * reach], start_dir=unit(head[-1] - head[-3]),
                    end_dir=-out, spacing=0.5)
    return W.join(head, body, np.array([end + out * reach, end - out * 4.0]))


LCD_LEADS = {}
for colour, male, _, fem, _, lying_key, _, seated_key in LCD_WIRES:
    seated = into_fem(cad_line(seated_key, male)[::-1], fem, None)[::-1]        # (from the breadboard)
    head = seated[:behind_f9(seated) + 1]                                       # (the shared run: on to just round F9's back edge)
    lying = into_fem(cad_line(lying_key, male)[::-1], fem, LCD_LYING)[::-1]
    y = fem_end(fem)[0][1]                                                      # (the wire's height at the header)
    LCD_LEADS[colour] = dict(
        lying=lcd_lead(lying, fem, male, LCD_LYING, lying[behind_f9(lying)]),
        standing=lcd_lead(lcd_tail(head, fem, LCD_STANDING, [[697.0, y, 1362.0], [703.6, y, 1358.5]]), fem, male, LCD_STANDING, head[-1]),
        seated=lcd_lead(seated, fem, male, None, head[-1]))
```

and a shape for each stop before them, the same way: for the published angled pose (header at x 726.3, z 1358.7, just in front of F9's
front edge) `lcd_tail(head, fem, pose, [[700.0, y, 1362.5], [716.0, y, 1366.5]], reach=6.0)`; for it 40 mm out in front
`[[700.0, y, 1362.5], [722.0, y, 1366.0], [748.0, y, 1369.0]], reach=6.0`; the working copy's path-searched shapes (`LCD_HALF_WAY`,
`LCD_SLID_WAY`) turned round: `lcd_lead(lcd_way_line[::-1], fem, male, pose, head[-1])`, where `lcd_way_line` is `lcd_way`'s line
(they pass within 0.2 - 5.6 mm of `head[-1]`, as their comment says). Also:

- the ribbon, the same way round (`wc:693`): `W.route(W.resample(np.linspace(pm, pf, 12), 1.0), a=male, b=fem, a_at=m, b_at=f_world,
  stretch=True)`, and the parts-list picture's female pose then `joined['purple'][2]['b_ref']` (`wc:702`, now `a_ref`);
- Steps 36 - 39: `done = LCD_LEADS[colour]['lying']` (`wc:742`); the steps' blends are by share of length as before (the ribbon has
  `stretch`);
- Steps 49 - 50: `wires_done` one shape per stop, e.g. `[d['lying'], d['out'], d['angled']]` and `[d['standing'], d['seated']]`.
- Draw the angled and standing shapes rather than take the CAD's: NAUO119/120 fold (section 5), and the published report notes the CAD's
  angled wires NAUO109 - 112 end 2.8 - 4.4 mm off the header in this pose (published_motions.md, "Our Steps 50-51").
- Drop the published 2.14 mm lift from the angled pose: with it the LCD's top is at y 951.66, 0.2 mm into F4's underside (951.46), and
  the purple wire grazes the top of F9's window as the LCD straightens (0.5 - 0.6 mm at 0.25 of 50c).

Tested on Lee's file with the LCD's way: lying, slid 60 mm out in front still lying, stood up angled 40 mm out, angled (published, about
the LCD's middle, no lift), straight 14.9 mm short, seated (Step 50: `ride={LCD: [SLID, OUT, ANGLED]}` with `wires_done=[lying, out,
angled]`; Step 51: `path=[ANGLED, LCD_STANDING, ZERO]` with `[standing, seated]`): no wire into any part in either step (was 11 and 0),
6 and 0 sub-millimetre touches between wires; the LCD itself touches only F8 as its board enters F8's notch; wirecheck clean at rest.
With the working copy's stops turned round the same way (rebuilt from its code), F9 is no longer hit in 49c, but F4 still is (1.9 - 2.1 mm)
and the LCD itself (1.1 - 1.4 mm, round the half-way pose): the LCD's own way from the half-way pose to the slid one passes through F4's
front corner by the breadboard's end (21 sample points in F4, 9 in F9 at 0.525), and the wires on its header go with it. That stop needs
moving, not the wires. 50c then keeps 0.2 - 0.6 mm grazes of F9's window with the CAD's angled and standing shapes, which the drawn ones
above do not have. Write the LCD's poses about its middle ([713.01, 919.52, 1311.22]) where it turns a long way between two of them
(`compose(pose, ZERO, LCD_MID)`): turned about the F8-end upright, the player swings its middle round a point 46 mm away.

## 9. Found while checking (not asked)

- In the working copy, F1 lies face down in front of the breadboard's end (`F1_DOWN`, x 763 - 839, z 1307 - 1472) and its leads' new way
  (`POT_WAY`, `wc:583-585`, y 915 from x 777 to the holes at z 1329 - 1340) crosses the LCD's seat: wirecheck on its steps.json (21:40):
  pot red/tan/black **inside the LCD, 0.71 - 0.79 mm, at rest in Steps 49c, 50, 50c, 51**; motioncheck: the LCD goes through them in 49c - 50c
  (1.4 mm), and they pass through F8 (2.1 mm) and the LCD (1.5 mm) as F1 is stood up and pushed on (51c, 52c). F1 there also fills the
  space in front where the LCD is stood up (moving the LCD's slid stop 40 mm out puts 137 of its 4000 sample points in F1).
- jumper wires 13 - 14 at rest: wirecheck "jumper blue route 24: NAUO28 0.03 mm, NAUO30 inside 0.05 mm" (working copy).

## 10. After the change

    .venv.nosync/bin/python "LAC Build Instructions/guide.py"
    .venv.nosync/bin/python tools/motioncheck.py "LAC Build Instructions" "Step 33c" "Step 34c" "Step 43c" "Step 49c" "Step 50c" --trace
    .venv.nosync/bin/python tools/wirecheck.py "LAC Build Instructions"

(motioncheck with the `mix` of 1.3, or it will not see a swing), then the player on each changed step half way through
(`_dev.show('Step 43c', 0.5)`), and the run-through check.
