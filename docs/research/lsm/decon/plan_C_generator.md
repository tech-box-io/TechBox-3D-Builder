# LSM Deconstruction: plan C, designed around what the generator does well

Planner's report, 21 Oct 2026, for `LSM Build Instructions/deconstruction.py` (not written yet). Lee's request, word for word:
"Alright, now take this LSM Full Build guide and create a Deconstruction Guide based on it. Same principles as you used for the MRA.
Remembering some things can be removed in groups (like the 3 breadboard wires, etc.)"

How this plan was made: only reading. I read the four study reports in this folder; `tools/stepgen.py` (take_apart, remove, unplug,
lift, _takeoff, put_away, and build()'s takeoff branch); the player's wire code (`player/js/player.js` 104-150: how a lead follows its
end parts); `LSM Build Instructions/guide.py`, `steps.json`, `assembly-report.json` and `README.txt`; the MRA's, the RCC's and the PMG's
`deconstruction.py`; and rulebook section 11. The only thing I ran was light Python reading JSON. Nothing in the repository was changed
except this file.

**Status: plan complete (written in stages; this is the final version).**

---

## 0. The approach in one paragraph

The plan is a **strict reverse of the Full Build**. Because of that, every state the deconstruction passes through (where each part
is, and the shape of every wire) is one the Full Build already showed and Lee already checked. Every move is a Full Build move played
backwards: either the generator's own default (the Full Build's way reversed, with that step's camera), or the Full Build's recorded
poses and wire routes read from `steps.json` and handed back in reverse order. **No new wire shape is drawn anywhere.**

The only moves the Full Build never played are:
- the four D11 posts pulled straight up (no wire near them);
- the USB cable and the three breadboard wires, each removed with both ends at once, carried rigidly by those ends;
- the LED matrix pulled 15 mm off the sockets of its own wires.

Steps that "would not move" or that the generator would mark with a Review note are all given their way by hand, using poses read
from `steps.json`. Everything else is left to the defaults.

The plan has **24 steps for the Full Build's 40** (0.60, inside the rulebook's 0.45-0.82). It ends on D1 with the breadboard stuck to
it, then shows the Full Build's parts list pages.

### Why not TechBox's published order (D5 and D4 off first, the matrix laid aside early)
In our model, the purple wire's pin in b19 sits under the leg of the USB plug (README Q2: the plug's leg is exactly where the pin
goes). So the purple pin cannot come out before the USB plug. The plug in turn cannot come out while the push button sits behind it:
its way out (+Z 25) hits the back of the button after 9.2 mm. Moving the button means moving D2 out, and D2 cannot move until D4
and D5 are off (D2's end tabs go through closed slots in both).

So the matrix stays wired to the breadboard until nearly the end, and while the walls come off it has to lie somewhere. The Full
Build has wire shapes for only three such places:
- **HELD**, over the box: this blocks the D9s on their way up.
- **OUTSIDE**, outside D4: the wires lie over D4's top edge, so this blocks D4.
- **BESIDE**, past D5's end: the wires run through D5's place and through D9_B's seat, so D5 and the D9s must already be off.

The reverse order visits these three exactly as the Full Build did. Any other order means drawing new wire shapes and checking them
against Lee's rule that wires never pass through parts.

---

## 1. The script skeleton (as the MRA's, RCC's and PMG's)

```python
"""Laser Stem Matrix (LSM), deconstruction: ... down to D1 with the breadboard on it (header as the MRA's: Lee's request, the order,
the exceptions)."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
from stepgen import Guide, apply_pose, compose, via          # noqa: E402

# parts: the ids guide.py gives (copied here: NEVER `import guide` - guide.py:826 calls g.build() at import and rewrites steps.json)
D1, D2, D3, D4, D5, D6, D7, D8, D10 = 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D10'
D9_A, D9_B = 'D9_A', 'D9_B'
D11S = ['D11_A', 'D11_B', 'D11_C', 'D11_D']
BREADBOARD, BACKING, NANO, R12K, R330, CAP, MATRIX = 'BREADBOARD', 'BACKING', 'NANO', 'R12K', 'R330', 'CAP', 'MATRIX'
BUTTON, NUT, RED_PIN, BLACK_PIN = 'BUTTON', 'NUT', 'BTN_RED_PIN', 'BTN_BLACK_PIN'
USB_B, USB_A = 'USB_B', 'USB_A'
PINS = ['J_WHITE_M', 'J_GREY_M', 'J_PURPLE_M']                 # the three breadboard wires' pins (i2, i3, b19); 'white' is drawn yellow
SOCKETS = ['J_WHITE_F', 'J_GREY_F', 'J_PURPLE_F']              # their sockets, on the matrix's V+, V- and IN pins
STEMS = [f'STEM_{k:02d}' for k in range(1, 65)]

FULL = json.loads((HERE / 'steps.json').read_text(encoding='utf-8'))
VIEW = {v['name']: v for v in FULL['views']}
ROUTES = FULL['routes']

def camera_of(step, moved=None): ...      # the MRA's (deconstruction.py:55-60), verbatim
def leads(step, prefix): ...              # the MRA's (63-65), verbatim
def full_way_back(step, part, then=()): ...   # the MRA's (92-99), verbatim

def slid(pose, by):
    """A Full Build pose moved on by a pure shift `by` (D2 and all on it, slid out to where the Full Build stood it): a turn about
    its own `at` and then t, so only t changes; a via() stays a via()."""
    if isinstance(pose, dict):
        return type(pose)(dict(pose, t=[round(a + b, 3) for a, b in zip(pose.get('t', [0.0, 0.0, 0.0]), by)]))
    return [round(a + b, 3) for a, b in zip(pose, by)]

def carried_back(step, part, prefix):
    """A Full Build step that moved `part` only by riding (the matrix on the breadboard, Steps 26 and 30: D4 was given a way that
    stays put to pace it), walked back for lift(): its stops reversed, each a stop (a beat a stretch, as the Full Build), its leads
    through the routes they came through, reversed, to the routes they had before it. As the PMG's carried_back()."""
    done = VIEW[step + 'c']
    c = done['carry'][part]
    stops = [VIEW[step]['carry'][part]['pose'], *(c.get('via') or []), c['pose']]
    stages = {w: [ROUTES[n] for n in nos[::-1]] for w, nos in done['wire_via'].items() if w.startswith(prefix + ' ')}
    assert all(len(r) + 1 == len(stops) - 1 for r in stages.values()), (step, len(stops), {w: len(r) for w, r in stages.items()})
    return dict(path=stops[::-1][1:], wire_via=stages, wires=leads(step, prefix))

def ridden_back(step, part, on):
    """A part brought in only riding on `on` (D10 hooked under the held matrix, Step 31): its stops on `on`, reversed, made absolute
    with where `on` is now."""
    stops = [VIEW[step]['carry'][part]['pose'], *(VIEW[step + 'c']['carry'][part].get('via') or [])]
    return [compose(where(on), p, g._pivot(part)) for p in reversed(stops)]

g = Guide(HERE, title='Laser Stem Matrix (LSM)', part='Deconstruction', names=dict(FULL['names']),
          steps_file='steps-deconstruction.json', source='lsm.glb', hero_azimuth=45,
          copyright_line='© TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')
g.take_apart(parts_list_at_end=True)        # (the Full Build's parts list after the Completed View: the MRA's and the PMG's)
g.put_away([BACKING])                       # (see below)

def where(i): ...                           # the MRA's (108-113), verbatim
```

Notes on the skeleton:
- `source='lsm.glb'`: the Guide's default is mra.glb (`stepgen.py` Guide signature). `hero_azimuth=45` as in guide.py:92. It matters
  only for views with no camera of their own, and for a Completed View after a turned-over last step (not the case here).
- `names=dict(FULL['names'])` already holds the hover names: "Yellow / Grey / Purple Breadboard Wire", "Push Button" for the nut and
  the pins, "D9" and "D11" for each copy. So `hover_names=` is not needed.
- **`g.put_away([BACKING])` straight after `take_apart()` is required.** `take_apart()` adds every part any Full Build view showed
  (stepgen.py:874, the `for v in reversed(states)` loop in take_apart; line numbers here are the current working tree's). BACKING was last shown in Step 1c (steps.json view [4]), riding
  BREADBOARD at pose `[0, -40, 0]`. So the deconstruction would start with the backing paper hanging 40 mm under the breadboard, through
  D1 and below the table (I checked steps.json: BACKING's carry in Step 1c is `{'by': 'BREADBOARD', 'pose': [0.0, -40.0, 0.0]}`). It would
  also count in the Completed View's framing.
  - The cost: Step 1 opens as a "cut", so there is no glide from the title page into Step 1 (player.js:713).
  - The cut-free alternative is to edit the generator's internals from the script (`g.placed.remove(BACKING)`, pop it from
    `g.riding`, and remove it from `g.steps[-1]['visible']` and `['riding']`). I do not recommend it.
- The title page is the Full Build's (no `start_view`): the USB cable is left off it there.

---

## 2. The steps

Some terms used in the tables:
- **Default**: the generator chooses the way out (the Full Build's way reversed) and the camera (that Full Build step's).
- **Hover routes**: the wire routes of a Full Build step's first view (Step N).
- **Done view**: a step's second view (Step Nc).

Step numbers are the deconstruction's. "FB" means a Full Build step.

### Part A: the stems, shelves and posts (FB 40 - 33)

**Step 1. Stems**

| | |
|---|---|
| **(a) Caption** | "Pull all 64 LED stems straight up out of D8, D7 and D6." |
| **(b) Call** | `g.remove(caption, STEMS, units=[STEMS])`. Optional `caution='Unplug the USB cable from the computer before you start.'` (see question 3). |
| **(c) Undoes** | FB 40 and 39 |
| **(d) Why here** | The stems pass through D8, D7 and D6 and stand over the LEDs, so they come off first. The Full Build's "one, then the rest" (FB 39 + 40) is merged into one group (rulebook section 11). |
| **(e) Risk** | None. Default ways (up 44) and FB 40's camera (STEM_CAMERA). Without `units=` there would be two arrows, one per Full Build step. With it there is one arrow, starting on the stem nearest the block's middle. |

**Step 2. D8**

| | |
|---|---|
| **(a) Caption** | "Lift D8 off the D11 posts." |
| **(b) Call** | `g.remove(caption, [D8])` |
| **(c) Undoes** | FB 38 |
| **(d) Why here** | D8 sits on the posts, above D7. |
| **(e) Risk** | None. Default: up 55, SHELF_CAMERA. |

**Step 3. D7**

| | |
|---|---|
| **(a) Caption** | "Lift D7 off the D11 posts." |
| **(b) Call** | `g.remove(caption, [D7])` |
| **(c) Undoes** | FB 37 |
| **(d) Why here** | As D8. |
| **(e) Risk** | None. Default: up 65, SHELF_CAMERA. |

**Step 4. The four D11 posts**

| | |
|---|---|
| **(a) Caption** | "Push the tabs of the four D11 posts up out of D1 from underneath, then pull the posts up out of D6." |
| **(b) Call** | See the code below. |
| **(c) Undoes** | FB 36, 35 and 34 |
| **(d) Why here** | The posts run down through D6's corner slots, so they come off before D6. All four in one step: Lee's groups. |

```python
POST_WAY = [VIEW['Step 36']['carry']['D11_A']['pose'], VIEW['Step 34']['carry']['D11_A']['pose']]   # [0, 6.4, 0], [0, 85, 0]
g.remove(caption, D11S, path=POST_WAY, units=[[i] for i in D11S], keep_camera=True,
         inset=dict(target=[674.83, 857.0, 1166.2], dir=[0.4109, -0.8401, 0.3541], radius=6.0, mark=2.5,
                    caption='Push the tab up out of D1', alt='Close-up from below of a D11 tab through its slot in D1'))
```

More on Step 4:
- **The way:** two beats, as the Full Build had them. The tab comes out of D1 first, then the post rises up out of D6.
- **The camera:** `keep_camera=True` keeps D7's SHELF_CAMERA, so one camera serves the whole shelf run.
- **The close-up:** it is FB 36c's own close-up, reused, now looking from below with one red box.
- **Why the way is given by hand:** the posts ride D1 and the Full Build has no record of them moving (they only rode in), so by
  default they would be lifted "straight up, unchecked" with a WARNING and a yellow Review note (stepgen.py:1038 on, the `computed` branch of
  `_takeoff`).
- **Arrows:** `units=` gives one arrow per post, as the MRA's six base screws. Expect the log NOTE "4 arrows".
- **(e) Risk:** low. With nothing on top of them, the posts slide up through D6's slots, the way the Full Build brought them in.
  Check that all four arrows can be seen from DIAG: D11_A is the farthest away, but all four stand 32 mm above D6. The close-up is a
  catch close-up, which is Lee's call (question 5); drop `inset=` if Lee does not want it.

**Step 5. D6**

| | |
|---|---|
| **(a) Caption** | "Lift D6 off the tops of the walls." |
| **(b) Call** | `g.remove(caption, [D6])` |
| **(c) Undoes** | FB 33 |
| **(d) Why here** | D6 lies over the matrix and D10 (0.3 mm above them) and on the walls' tabs. |
| **(e) Risk** | None. Default: up 64, FB 33's camera. FB 33's close-up of D1's four slots (`marks=`) cannot be carried over: a takeoff close-up keeps only one red box. It is not needed here. |

### Part B: the LED matrix out of the box, still wired (FB 32 - 29)

**Step 6. The matrix lifted out with D10**

| | |
|---|---|
| **(a) Caption** | "Lift the LED matrix, with D10 hooked under it, straight up out of the box. Keep its three wires plugged in." |
| **(b) Call** | See the code below. |
| **(c) Undoes** | FB 32 |
| **(d) Why here** | The matrix has to come off the D9s (it rests on them), and D10's end tabs lift out of the open-topped slots in D4 and D5. Rulebook: "Wired modules are lifted off the housing first, still wired". |

```python
g.lift(caption, [MATRIX],
       wire_via={w: [ROUTES[n] for n in nos[::-1]] for w, nos in VIEW['Step 32c']['wire_via'].items()},   # HALF: routes 62 / 63 / 64
       wires=leads('Step 32', 'wire'))                                                                     # HELD: routes 59 / 60 / 61
```

More on Step 6:
- **The way and camera are the defaults:** FB 32's record reversed is seat → via P_HALF → P_HELD `[-0.2, 56.6, -0.3]`, in one beat
  (its stops are [0, 2]), by FB 32's camera. D10 and the three sockets ride along.
- **(e) Risk:** low. This is FB 32's blend (HELD → HALF → SEATED) played backwards, which is what the Full Build's Prev button shows.
  The wires must be given: `lift()` never re-routes leads by itself. Without `wires=`, only the last 6 mm of each wire would follow the
  socket (`b_from` = length − 6, player.js:126-131), and the wire would break.

**Step 7. D10 off the held matrix**

| | |
|---|---|
| **(a) Caption** | "Slide D10 along under the LED matrix towards D2 until its hooks let go, then lower it away." |
| **(b) Call** | See the code below. |
| **(c) Undoes** | FB 31 |
| **(d) Why here** | In the Full Build, D10 went on while the matrix was held, and the matrix only went outside D4 without it. The OUTSIDE and BESIDE wire shapes were drawn with no D10, and near the header they run where D10 would be. |

```python
g.remove(caption, [D10], path=ridden_back('Step 31', D10, MATRIX),     # [-0.2, 56.6, 39.7] then [-0.2, 34.6, 39.7]: slide +Z 40, then down 22
         arrow_style={D10: dict(at=[round(float(x), 2) for x in apply_pose(where(D10), [[599.5, 880.0, 1207.0]])[0]])},
         **camera_of('Step 31'))                                       # (Lee's framing of FB 31)
```

More on Step 7:
- **The arrow:** two beats; it follows the 40 mm slide. Its tail is placed by hand at the D4 end of D10, below its lower edge, the
  mirror image of FB 31's own hand arrow (guide.py:759, which Lee approved). Left to the default, the arrow would start under the
  matrix and be moved on until it could be seen, ending up 30 mm past the matrix's edge, away from D10 (lee_notes_2026-10-19b: "no
  arrow hidden under the matrix").
- **Why the way is given by hand:** D10 only ever rode, so it has no record. By default it would be lifted straight up through the
  matrix, with a WARNING and a Review note.
- **(e) Risk:** low. This is FB 31's own sweep reversed: the HELD wires were drawn clear of D10 coming up (guide.py:652, "clear of
  D10 as it comes up (z 1242.7 - 1245.7)"). Check the arrow by eye.

**Step 8. The matrix out over D4**

| | |
|---|---|
| **(a) Caption** | "Carry the LED matrix out over D4 and lay it down outside the box, LEDs up, its wires over the top edge of D4." |
| **(b) Call** | `g.lift(caption, [MATRIX], **carried_back('Step 30', MATRIX, 'wire'), **camera_of('Step 30'))` |
| **(c) Undoes** | FB 30 |
| **(d) Why here** | While the matrix is held over the box, it is in the way of the D9s going up (65 mm up reaches 965.7; the matrix's bottom is at about 949.7). The Full Build put the D9s in with the matrix outside D4. |

More on Step 8:
- **What `carried_back` gives:** path `[P_LIFT, P_OUTSIDE]` (two beats); wire_via LIFT (routes 56-58); wires OUTSIDE (routes 53-55).
- **The camera:** HELD_CAMERA, the same camera as Step 9 (FB 29), so there is no camera jump.
- **The arrow:** the default follows the longer stage, the 94 mm move across over D4, starting at the matrix's D4 edge. FB 30 had an
  eye on the matrix instead; arrows=[] with eye=[MATRIX] is the fallback.
- **(e) Risk:** medium-low. These are the Full Build's routes in reverse, but here the matrix is a moving part where the Full Build had
  it riding, paced by D4's still way. The pacing should match: two stops and two route stages ("keeps pace stop by stop", CLAUDE.md).
  Run motioncheck on this step.

**Step 9. The two D9s**

| | |
|---|---|
| **(a) Caption** | "Pull both D9 LED supports up out of their slots in D2 and D3." |
| **(b) Call** | `g.remove(caption, [D9_A, D9_B])` |
| **(c) Undoes** | FB 29 |
| **(d) Why here** | The D9s' ends go through D3 (and D2), so they come off before D3. D9_B stands over the capacitor. The wires lie under D9_A's engraved end, which is open at the bottom, so D9_A lifts off over them as the Full Build lowered it. |
| **(e) Risk** | None. Default: up 65, HELD_CAMERA. Two of a kind that do not touch get an arrow each (2 arrows). The matrix lying outside is within the frame (59 mm from the target, against 1.1 × 114.8), so there is no NOTE. |

### Part C: the walls round the base, the matrix moved round to the D5 end (FB 28 - 25)

**Step 10. D5, box turned over**

| | |
|---|---|
| **(a) Caption** | "Turn the box over. Slide D5 off the end of the box." |
| **(b) Call** | `g.remove(caption, [D5])` |
| **(c) Undoes** | FB 28 |
| **(d) Why here** | D5 goes over the tabs of D1, D2 and D3, all of which run along X. With D10 gone, nothing else holds it. |
| **(e) Risk** | None. Default: +X 42, FB 28's camera, which is turned over (the box upside down, as in the Full Build; the RCC's "Turn the car over. Slide L6 out." is the precedent). |

More on Step 10:
- The turned-over run starts here, so its turning axis comes from this view, not from FB 27's as in the Full Build (stepgen.py:2052 on, the
  flip-run block in build()).
- That does not change the picture: a half turn about any level axis turns the model the same way relative to a camera given in the
  model's own frame.
- The matrix lying outside D4 turns with the model, as it did in FB 27-28.

**Step 11. D3, still turned over**

| | |
|---|---|
| **(a) Caption** | "Swing the free end of D3 out from the box, then slide D3 away from D4 to unhook its tabs." |
| **(b) Call** | `g.remove(caption, [D3])` |
| **(c) Undoes** | FB 27 |
| **(d) Why here** | D3's end tabs are hooked into D4's slots (and D5's are now free), so D3 comes off before D4. Rulebook: "A two-stage joint is undone inside one step"; the generator does it from FB 27's way. |
| **(e) Risk** | Low. Default: swing 22° about HINGE, then 40 mm along the tilt; two beats; FB 27's camera, turned over. The arrow follows the slide (the longest stage). If Lee wants the arrow on the swing, add `arrow_style={D3: dict(stage=0)}`. The order check skips ways that turn. FB 27 brought D3 in with the matrix outside D4, the same state as here. |

**Step 12. The matrix back over D4 to the D5 end**

| | |
|---|---|
| **(a) Caption** | "Turn the box the right way up. Lift the LED matrix back over D4, turning it round, and lay it beside the base at the open D5 end." |
| **(b) Call** | `g.lift(caption, [MATRIX], **carried_back('Step 26', MATRIX, 'wire'), **camera_of('Step 26'))` |
| **(c) Undoes** | FB 26 |
| **(d) Why here** | The OUTSIDE wires lie over D4's top edge, so D4 cannot lift off until they are moved. BESIDE runs through D5's place and D9_B's seat, both now empty. Both orders the Full Build used. |

More on Step 12:
- **What `carried_back` gives:** path `[P_UP_OUTSIDE, P_MID, P_UP_BESIDE, P_BESIDE]`, four beats, with a quarter turn on each of the
  middle two stages. wire_via is routes 46, 45, 44 (white), 49, 48, 47 (grey), 52, 51, 50 (purple). wires BESIDE is 33 / 34 / 35.
- **The camera:** FB 26's, from straight above.
- **The arrow:** by default it follows the longest stage (P_MID → P_UP_BESIDE, 117 mm along +X). Seen from above, it points across
  the box. FB 26 had an eye on the matrix; that is the fallback.
- **(e) Risk:** medium. This is the one walk-back with turns, and the riskiest step in the guide. The routes and poses are FB 26's in
  reverse, but the turned poses are now played as a moving part's path where the Full Build had riding stops. Check it with
  motioncheck.py, and by eye at Step 12c half way.
- If it misbehaves, the fallback is `reappear=True` (in the working tree's stepgen.py, uncommitted: the matrix fades out where it is
  and back in at the D5 end). Lee has approved that fade for the PMG's Step 42 only, so it would need Lee's word here.

**Step 13. D4**

| | |
|---|---|
| **(a) Caption** | "Slide D4 off the tabs of D1 and D2, then lift it up off the base; the USB cable comes out of the notch in its foot." |
| **(b) Call** | `g.remove(caption, [D4], path=full_way_back('Step 25', D4), **camera_of('Step 25'))` |
| **(c) Undoes** | FB 25 |
| **(d) Why here** | D4 goes over D2's tabs through closed slots, so it comes off before D2 can move. The matrix is now beside the base, as it was in FB 25. |

More on Step 13:
- **The way:** `[[-8, 0, 0], [-8, 65, 0]]`, two beats: off the tabs, then up. The notch is open underneath and the cable runs along X
  through it, so D4 comes away cleanly.
- **The camera:** BASE_CAMERA.
- **Why by hand:** D4's latest Full Build "move" is FB 31's still way, `[ZERO]*3` (D4 was used to pace the matrix's rides in FB 26,
  30 and 31). The generator takes the latest record whose group is leaving, so by default D4 would not move, would have no arrow, and
  would get FB 31's D10 close-up camera.
- **(e) Risk:** none beyond the hand way, which is FB 25's own.

**Step 14. D2 slid out, still wired**

| | |
|---|---|
| **(a) Caption** | "Slide D2, with the push button in it, straight out off the tabs of D1. Keep the button's two wires plugged in." |
| **(b) Call** | `g.lift(caption, [D2], wires=leads('Step 24', 'lead'), arrow_style={D2: dict(at=[638.2, 912.0, 1256.0])})` |
| **(c) Undoes** | FB 24 |
| **(d) Why here** | With D2 at D2_OUT, the USB plug can come out (+Z 25), and the button's pins come out exactly as FB 21-22 put them in: their poses and routes were drawn with D2 there. "Wired modules are lifted off still wired". |

More on Step 14:
- **The way:** default, FB 24 reversed: +Z 57.1 to D2_OUT, by BASE_CAMERA. BUTTON and NUT ride along.
- **The leads:** `wires=` gives FB 24's hover routes, 38 and 39, so the leads blend from 42/43 back to 38/39 as the Full Build blended
  them forwards.
- **The arrow:** the tail is placed on D2's top edge at its outer face, 5 mm above it. D2's outer face is turned away from DIAG, so a
  default arrow would be pushed on about 35 mm past D2 before it could be seen, and would float where D2 ends up.
- **(e) Risk:** low. This is FB 24's blend reversed. Check the arrow by eye.

### Part D: power, the push button and its leads (FB 23 - 19)

**Step 15. The USB cable**

| | |
|---|---|
| **(a) Caption** | "Unplug the USB cable from the Nano Board and lift its other end off the table." |
| **(b) Call** | `g.remove(caption, [USB_B, USB_A], units=[[USB_B]], arrow_scale=2.5, paths={USB_A: [[0.0, 25.0, 0.0]]})` |
| **(c) Undoes** | FB 23 |
| **(d) Why here** | The plug's way out is now clear of the button. The plug has to come out before the purple pin in b19, which is under its leg. |

More on Step 15:
- **The plug:** USB_B uses its default way (+Z 25) and FB 23's camera (BASE_CAMERA).
- **The A end:** it is lifted 25 mm with the plug, as on the RCC and the MRA. It has no record of its own (it was only shown in FB 23).
- **The arrow:** one arrow, on the plug that is pulled (RCC rule). It is scaled 2.5 times because at radius 125 the default 15 mm
  arrow is only 0.12 of the view (the MRA used ×2, the RCC ×4).
- **(e) Risk, how the cable moves:** the cable leaves with both ends, so it is carried by their moves (a `stretch` route, blended by
  share of its length) rather than blended through route 40, as FB 23 did.
  - The A end and the run along the table rise up to 25 mm, with nothing above them now that D4 is off.
  - The run near the plug shifts +Z with the plug, sideways along -X, away from the button's leads (x 635-655) and away from the
    purple wire (which leaves b19 towards +X).
  - Check it with motioncheck.
- **(e) Risk, the purple pin:** the purple pin overlaps the plug by 0.3 mm at rest (the CAD's own clash, README Q2). The order check
  will not warn, because FB 23's own stationary parts had the same overlap.

**Step 16. Both button pins**

| | |
|---|---|
| **(a) Caption** | "Unplug the push button's red and black wires from j5 and j16." |
| **(b) Call** | `g.unplug(caption, [RED_PIN, BLACK_PIN], caution='Pull each wire out by its pin, not by the wire.', **camera_of('Step 21'))` |
| **(c) Undoes** | FB 22 and 21 |
| **(d) Why here** | Lee's groups: wires that went in one at a time come out together. The leads are unplugged before the button sub-assembly is taken apart. |

More on Step 16:
- **The defaults do the rest:** each pin goes back to its FB 21 / FB 22 pose (laid straight back from the button at D2_OUT). The leads
  blend from 38/39 to 36/37. Each pin then rides BUTTON (its `rode` from FB 20c). Two eyes, no arrows.
- **The camera:** FB 21's (radius 40, D5/D3 corner), given by hand. The default would be FB 22's (radius 35.5), which frames j16 and
  can cut off j5's way out.
- **(e) Risk:** none if Step 14 really ended at D2_OUT, which it does (FB 24's path, reversed). In the Full Build these leads were
  plugged in with the USB plug not yet in, the same as now that Step 15 has taken it out.

**Step 17. The nut, in the hand**

| | |
|---|---|
| **(a) Caption** | "Unscrew the nut from the push button on the inside of D2, and slide it off over the wires." |
| **(b) Call** | See the code below. |
| **(c) Undoes** | FB 20 |
| **(d) Why here** | The button sub-assembly is taken apart on its own (alone=, as the RCC's controller and module and the MRA's claw), the nut first, as the button cannot leave through D2 with the nut on it. |

```python
HAND = [D2, BUTTON, NUT, RED_PIN, BLACK_PIN]
D2_AT = where(D2)                                                  # [0, 0, 57.1] (FB 24's path, reversed)
assert isinstance(D2_AT, list)                                     # (a pure shift: slid() is exact)
nut_way = [slid(p, D2_AT) for p in full_way_back('Step 20', NUT)]  # FB 20's NUT_ON reversed: two turns, unscrewing, -60 mm
nut_way[3] = dict(nut_way[3])                                      # (after one turn: a stop, so the two turns take two beats, as FB 20)
g.remove(caption, [NUT], path=nut_way, alone=HAND,
         arrow_style={NUT: dict(at=[round(float(x), 2) for x in apply_pose(where(NUT), [[649.24, 882.63, 1250.3]])[0]])},   # (FB 18's tail: the rear face, 1 mm over the black lead)
         **camera_of('Step 20', moved=D2_AT))                      # (from inside D2, where the nut is)
```

More on Step 17:
- **Why the way is given by hand:** the nut's only record (FB 20) has the group NUT + BUTTON, so a remove of the nut alone does not
  match it, and the nut would be lifted straight up with a Review note.
- **The turns:** `full_way_back` keeps FB 20's quarter-turn poses (unscrewing, the reverse of Lee's screwing-on direction). Passing
  the poses through `slid()` keeps the Full Build's angles exactly.
- **The beats:** the Full Build's stops are [0, 8], which would give one beat for two turns. Making the pose after one turn a stop
  gives two beats, as FB 20 had. In FB 20 the length came from BUTTON's still way, which cannot be used in a remove.
- **The arrow tail** is FB 18's (guide.py:547), moved with D2.
- **(e) Risk:** low. Check by eye that there is no visible pause at the half-way stop. If there is, keep all the middle poses as
  via() and accept one beat.

**Step 18. The button, in the hand**

| | |
|---|---|
| **(a) Caption** | "Pull the push button out of D2 from the engraved side, drawing its wires back through the hole." |
| **(b) Call** | `g.remove(caption, [BUTTON], path=[slid(p, D2_AT) for p in full_way_back('Step 19', BUTTON)], alone=[D2, BUTTON, RED_PIN, BLACK_PIN], **camera_of('Step 19', moved=D2_AT))` |
| **(c) Undoes** | FB 19 |
| **(d) Why here** | After the nut. |

Then: `g.put_away([D2])`. That is what is left of the sub-assembly; the next view starts afresh, back on the base.

More on Step 18:
- **The way:** `[[0, 0, 157.1]]`, FB 19's +Z 100 moved with D2. The pins ride the button, so they leave with it, and both leads go
  with them (both ends leave).
- **Why by hand:** BUTTON's latest record is FB 20's still way `[ZERO]*3` (it was given only to make FB 20 two beats long), so by
  default the button would not move.
- **(e) Risk, convention:** this breaks Lee's rule that "two steps on one sub-assembly in the hand keep one camera". FB 20's camera
  (inside D2) sees the nut; FB 19's (outside) sees the button come out head first. With one camera, one of the two cues would be
  behind D2. The Full Build and TechBox's published take-apart (its Steps 18 and 19) both use two sides. See question 4 for the
  one-camera version.

### Part E: the LED matrix off its wires, the three wires, the parts in the breadboard (FB 17 - 3)

**Step 19. The matrix off its wires' sockets**

| | |
|---|---|
| **(a) Caption** | "Pull the LED matrix off the sockets of its three wires and lift it away." |
| **(b) Call** | See the code below. |
| **(c) Undoes** | FB 17, 16 and 15 |
| **(d) Why here** | The matrix is a module pulled off the ends of its wires before the wires are unplugged at the other end. This is the PMG's draft of today ("each device pulled off the ends of its wires ... then all 21 breadboard wires off the I/O module at once") and TechBox's published take-apart (cable off the header). |

```python
OFF_PINS = compose(where(MATRIX), [0.0, 0.0, -15.0], g._pivot(MATRIX))       # (back 15 mm along its pins: guide.py:224 SOCKET_OFF, the other way)
g.remove(caption, [MATRIX], let_go=SOCKETS,
         path=[OFF_PINS, compose([0.0, 30.0, 0.0], OFF_PINS, g._pivot(MATRIX))],
         arrow_style={MATRIX: dict(stage=0)},                                 # (the arrow along the pull off the pins, as the RCC's joysticks)
         look_from=[1, 1, -1])                                                # (D5 / D3's corner: the matrix in front, the wires back to i2, i3, b19)
```

More on Step 19:
- **What happens:** the matrix slides 15 mm off its header pins, which is +Z in assembly space (it is turned 180° at P_BESIDE), and
  then lifts 30 mm. The sockets stay where they lie, resting, with their wires still in the breadboard.
- **(e) Risk, the generator:** `let_go=` is in the working tree's `tools/stepgen.py`. It was added today by the PMG session and is
  **uncommitted**. If it is not there when this script is run, use the fallback below.
- **(e) Risk, the motion:** check that the matrix sliding over the wires lying under it, at y 865-872 below its bottom at 871.4, does
  not touch them. The header pins slide out of the sockets.

Fallback without `let_go=` (one step instead of Steps 19-20: the wires leave on the matrix's pins):

```python
g.remove('Unplug the yellow, grey and purple wires from i2, i3 and b19, and lift the LED matrix away with them.', [MATRIX] + PINS,
         paths={MATRIX: [compose([0.0, 30.0, 0.0], where(MATRIX), g._pivot(MATRIX))]}, units=[[MATRIX]], eye=['J_GREY_M', 'J_PURPLE_M'],
         caution='Pull each wire out by its pin, not by the wire.', look_from=[1, 1, -1])
```

**Step 20. The three breadboard wires together (Lee's group)**

| | |
|---|---|
| **(a) Caption** | "Unplug the yellow, grey and purple wires from i2, i3 and b19." |
| **(b) Call** | See the code below. |
| **(c) Undoes** | FB 13, 12 and 11 |
| **(d) Why here** | Lee's group. The purple pin (b19) is free now that the USB plug is out. |

```python
g.remove(caption, PINS + SOCKETS,
         paths={s: [compose([0.0, 30.0, 0.0], where(s), g._pivot(s))] for s in SOCKETS},   # (the loose ends up with the pins)
         arrows=[], eye=['J_GREY_M', 'J_PURPLE_M'],                                       # (an eye on i2 / i3, side by side, and on b19)
         caution='Pull each wire out by its pin, not by the wire.', keep_camera=True)
```

More on Step 20:
- **The ways:** the pins use their defaults (FB 11-13 reversed, up 30). The sockets get the same lift, by hand.
- **Why the wires stay in shape:** every point of a jumper wire up to 6 mm from its socket moves wholly with its pin (`b_from` =
  length − 6, player.js:126-131), and the last 6 mm move with the socket. With all six ends rising 30 mm, each wire rises as one piece
  in its BESIDE shape and fades with its ends. No routes are needed.
- **(e) Risk:** none known. This is the only clean way to take a wire off with both ends. If a socket were pulled off along its pin
  while the pin rose, the wire would tear at the 6 mm mark. For the same reason I do **not** use `unplug()` on the pins: it would put
  each lead back on FB 11-13's route, which was drawn for the matrix held upright over the breadboard.
- **(e) Risk, camera:** `keep_camera=True` is needed. Otherwise the generator takes FB 13's close b19 camera, which leaves the sockets
  out and logs a NOTE.

**Step 21. The 330 Ω resistor**

| | |
|---|---|
| **(a) Caption** | "Pull the 330 Ω resistor out of a11 and a19." |
| **(b) Call** | `g.remove(caption, [R330])` |
| **(c) Undoes** | FB 9 |
| **(d) Why here** | Reverse order. Its box overlaps the USB plug's, and the plug is now out. |
| **(e) Risk** | None. Default: up 30, FB 9's camera. Its bent legs (leads `330 leg 1/2`, b = None) go with it. |

**Step 22. The capacitor**

| | |
|---|---|
| **(a) Caption** | "Pull the capacitor out of j2 and j3." |
| **(b) Call** | `g.remove(caption, [CAP])` |
| **(c) Undoes** | FB 7 |
| **(d) Why here** | Reverse order. D9_B, which stood over it, is long gone. |
| **(e) Risk** | None. Default: up 29, FB 7's camera. |

**Step 23. The 12 kΩ resistor**

| | |
|---|---|
| **(a) Caption** | "Pull the 12 kΩ resistor out of h3 and h16." |
| **(b) Call** | `g.remove(caption, [R12K])` |
| **(c) Undoes** | FB 5 |
| **(d) Why here** | Before the Nano: their boxes overlap by 1.2 mm. |
| **(e) Risk** | None. Default: up 32. Its legs go with it. |

**Step 24. The Nano Board**

| | |
|---|---|
| **(a) Caption** | "Lift the Nano Board out of the breadboard." |
| **(b) Call** | `g.remove(caption, [NANO])` |
| **(c) Undoes** | FB 3 |
| **(d) Why here** | The last plug-in part. |
| **(e) Risk** | None. Default: up 35, FB 3's camera (DIAG). |

`g.build()`

### The end, the parts list, the website entry
- **Completed View:** D1 with the breadboard on it, nothing else. It is framed close on what is left, from the last step's direction
  (FB 3's DIAG, which is not turned over). This is where TechBox's published LSM take-apart ends too.
  - The breadboard is stuck on D1 by its backing.
  - FB 1 (backing peeled off) and FB 2 (breadboard pressed onto D1) have no counterpart.
  - So do the preparation and look steps: FB 4 and 8 (legs bent), 6 (capacitor card), 10 (ribbon split), 14 (matrix pins) and 18 (nut
    off a new button).
- **Parts list:** the Full Build's two pages, "Parts List" and "Parts List (Cont.)", after the Completed View
  (`take_apart(parts_list_at_end=True)`). These are "the MRA's principles": the curriculum director, 19 Oct 2026, and the PMG's draft
  today.
- **Title page and card:** the Full Build's. `_dev.card()` on `player.html?steps=steps-deconstruction.json` copies `cards/steps.webp`.
  The model is unchanged: the deconstruction shows no new part, so model.glb is not rebuilt.
- **guides.json**, after the `laser-stem-matrix-full-build` line:
  `"laser-stem-matrix-deconstruction": {"kit": "laser-stem-matrix", "steps": "steps-deconstruction.json", "label": "Deconstruction", "script": "deconstruction.py"},`
  then run `python3 tools/site_pages.py`, which writes the guide's framing rules into render.yaml (check_site.py refuses the guide
  without them).

---

## 3. Summary: what is by hand, and why

| What | Steps | Why the default will not do |
|---|---|---|
| `put_away([BACKING])` | before 1 | take_apart() brings BACKING back 40 mm under the breadboard (Step 1c's carry) |
| D11 posts' way (from steps.json: FB 36 / 34 carry poses) | 4 | they only rode: no record, so "lifted straight up, unchecked" with a Review note |
| Matrix leads (`wires=` / `wire_via=` from FB 32 / 32c) | 6 | lift() never re-routes leads |
| D10's way (FB 31 carry poses), arrow tail | 7 | it only rode: no record. The default arrow would end up under or past the matrix |
| Matrix walk-backs (`carried_back`, FB 30 and FB 26) | 8, 12 | the matrix only rode in FB 26 and FB 30: no record |
| D4's way (FB 25 path) | 13 | its latest record is FB 31's still way: it would not move |
| D2's leads (FB 24 hover routes), arrow tail | 14 | lift() never re-routes; D2's outer face is hidden from DIAG |
| USB A end lifted, one unit, ×2.5 | 15 | the A end has no record; the RCC / MRA convention |
| Button pins' camera (FB 21) | 16 | FB 22's camera is tight on j16 |
| Nut's and button's ways (FB 20 / 19, moved by D2_OUT), nut stop, arrow tail | 17, 18 | a group mismatch (nut); a still way (button) |
| Matrix off its pins, `let_go=` | 19 | a move the Full Build never made (the sockets went on with the matrix upright) |
| Sockets lifted with the pins | 20 | they rest (let go): no record |

Defaults used unchanged: stems (with `units=`), D8, D7, D6, the matrix's lift out of the box, the D9s, D5 and D3 (turned over), D2's
way, the USB plug's way, both button pins (unplug), the jumper pins' ways, R330, CAP, R12K, NANO.

**Expected log:**
- `take_apart(): from steps.json as it ends (98 parts, 10 leads)`. BACKING is counted here, then put away.
- One NOTE: Step 4, "4 arrows".
- No WARNING and no Review note. If any WARNING appears ("passes through a part still there", "not in its seat", "plug left behind"),
  stop and look.

---

## 4. Checks after it is run (one heavy job at a time; swap was at 849 MB free when this study began)

1. Before running, copy `steps.json` to the scratchpad. Afterwards confirm it is byte for byte unchanged: the script never writes it,
   and guide.py is never imported.
2. Read the log for the lines in section 3.
3. Run `motioncheck.py "LSM Build Instructions" --steps steps-deconstruction.json`, looking hardest at:
   - Step 12, the four-beat walk back with turns;
   - Step 8;
   - Step 15, the cable carried by its ends;
   - Step 19, the matrix sliding over its wires.
4. Run `wirecheck.py "LSM Build Instructions" steps-deconstruction.json`.
5. In the player on 8805, open `?steps=steps-deconstruction.json` and run `_runthrough()`. By eye, check:
   - the arrows of Steps 7, 14 and 17;
   - the four D11 arrows;
   - Step 12c and Step 19c half way through (`_dev.show('Step 12c', 0.5)`);
   - the two cameras of Steps 17 and 18.
6. Run `_runthrough()` on the Full Build as well (82 views, unchanged).
7. Make the card with `_dev.card()`, then publish only to the test site, as the memory note says
   (`--to "share/Test guides preview"`, Lee on 8799).
8. Records:
   - a DECONSTRUCTION section in the LSM README;
   - a paragraph in CLAUDE.md's "A deconstruction guide", and the address in its list;
   - a note in rulebook section 11 for any convention Lee states.
9. Commit only this guide's files. Other sessions have uncommitted work in `tools/stepgen.py`, `tools/motioncheck.py`, `CLAUDE.md` and
   the LAC and PMG folders.

Note on line numbers: `tools/stepgen.py` is being edited in the working tree by another session (the PMG's deconstruction: `let_go=`,
`reappear=`). The study reports' stepgen line numbers (take_apart 828-901, _takeoff 949-1188) are about 4-10 lines low against the
current file. The code they describe is unchanged apart from the two new options.

---

## 5. Questions for Lee (only real ones)

1. **The matrix's route.** The draft walks the Full Build back, so the LED matrix is carried out over D4 (Step 8) and later back round
   to the D5 end (Step 12), as the Full Build moved it. TechBox's published take-apart takes D5 and D4 off early and lays the matrix
   aside instead; in our model that needs new wire shapes, and the purple pin would come up through the USB plug. Keep the reverse?
2. **The three wires.** The draft first pulls the matrix off their sockets (Step 19), then unplugs all three from i2, i3 and b19 in one
   step (Step 20). The alternative is one step: the wires come out of the breadboard and leave still on the matrix. Which?
3. **Power.** The USB plug cannot be reached until the box is open and D2 is out (Step 15; the published take-apart also removes it
   late). Add a caution on Step 1: "Unplug the USB cable from the computer before you start."?
4. **The push button in the hand.** The nut is seen from inside D2 (Step 17) and the button from outside (Step 18), as in the Full
   Build. Or one camera for both (your rule), with the button's arrow in a close-up of D2's outer face?
5. **Catch close-ups.** The draft has one: the D11 tab through D1 (Step 4, the Full Build's own close-up). Add the published guide's
   latch close-ups on D8 and D7 as well, or none at all?
6. **More groups.** Lift D8 and D7 in one step (one after the other)? Pull the two resistors and the capacitor out in one step? The
   draft keeps each as its own step, as both the Full Build and the published take-apart do.
