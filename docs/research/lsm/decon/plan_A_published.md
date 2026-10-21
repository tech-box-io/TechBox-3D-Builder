# LSM deconstruction, plan A: TechBox's published take-apart, as closely as the house rules allow

Plan for `LSM Build Instructions/deconstruction.py` (21 Oct 2026). The angle: keep TechBox's own published LSM take-apart (24 steps:
`docs/research/guide_19075-laser_stem_matrix_lsm_-_deconstruction.md`) for its order, its groups, its sub-assemblies taken apart on
their own and its cameras, and change it only where our Full Build differs or Lee's conventions require it. Lee's request, word for
word: "Alright, now take this LSM Full Build guide and create a Deconstruction Guide based on it. Same principles as you used for the
MRA. Remembering some things can be removed in groups (like the 3 breadboard wires, etc.)"

Read for this plan: the four study reports in this folder; `LSM Build Instructions/guide.py` (all 826 lines), `steps.json` (the views
named below, read with light Python), `assembly-report.json` (every part's box), `README.txt`; `docs/research/lsm/lee_notes_*.md`;
`docs/cadasio-patterns.md` section 11; `tools/stepgen.py` 828-1235 (take_apart, remove, unplug, lift, _takeoff, put_away), 1388-1424
(arrows), 1790-1806 (a take-off step's close-up); the MRA's, RCC's and PMG's `deconstruction.py`. Nothing was run, built or changed
(this Mac had about 850 MB of swap free); only this file was written. Every number below is from those files; nothing here has been
seen in the player, so the close-ups' targets and the hand-placed arrows are starting values to check.

## 1. The plan in one paragraph

25 steps (0.63 take-apart steps per build step; the rulebook's range for 40 build steps is 18 - 33; the published guide has 24). The
published order is kept, except for three changes our build forces and two the house rules require (section 2). It runs: the 64
stems; D8; D7; D5; the D11 posts at the D4 end, then those at the D5 end; D6; the LED matrix lifted out of the box with D10, still
wired; D10 off the matrix; the matrix laid outside D4; both D9; the matrix carried back over the box to lie beside the open D5 end;
D4; D3; D2 with the button lifted out, still wired; the button's two pins unplugged; on their own, the nut, then the button out of
D2; the USB cable; the three breadboard wires, both ends at once (Lee's group); the matrix away; the 330 Ohm resistor, the capacitor,
the 12 kOhm resistor, the Nano Board. It ends, as the published guide does, on the breadboard stuck to D1, followed by the Full
Build's parts list (as the MRA's and the PMG's). Every lead moves only through shapes the Full Build already has, played backwards;
no new wire shape has to be drawn.

## 2. Where it leaves the published order, and why

What our build forces:

1. **D4 comes off after the matrix (published Step 5; ours Step 13), and the matrix is carried twice (ours Steps 10 and 12).**
   - The published guide lays the matrix beside the box once, with D4 already off.
   - Our build's only place to lay the matrix aside while the D9s are still in is outside D4 (P_OUTSIDE, guide.py:222). There its
     wires run up beside D4 and over D4's top edge (`over_d4`, guide.py:662-676; routes 53-55).
   - With D4 off, those wires would arch over empty air. With D4 on, D4 cannot be lifted through them.
   - The other aside place is P_BESIDE, beside the base past D5 (routes 33-35). Those wires cross D9_B's place: the white wire passes
     x 652 to 690 at y 895 to 868, and D9_B is at x 655.8-658.8, y 882.2-900.7. So P_BESIDE can only be used once the D9s are out.
   - So the order has to be: matrix outside D4 → D9s → matrix carried back to beside the base (the build's Step 26, reversed) → D4.
2. **D10 comes off before the matrix is laid aside, in the main view (published Step 14, on its own; ours Step 9).**
   - Our build hooked D10 on while the matrix was held over the box (guide.py:750-760), so undoing that step there is exact.
   - Laid outside D4 with D10 still under it, D10 would lie across the wires. At P_OUTSIDE, D10 spans x 503-592, y 889-907,
     z 1228-1231. The OUTSIDE wires run under the board at z 1222-1230, about 1.2 mm below the sockets (guide.py:671-675).
3. **The three breadboard wires come off after the USB cable (published Steps 11-13; ours Step 20).**
   - The purple pin in b19 is under the USB plug's leg (README question 2). Their boxes overlap by 6.3 mm in height: J_PURPLE_M
     reaches y 879.92, and USB_B spans y 873.62-881.12 over the same x and z. So the pin cannot be pulled up while the plug is in.
   - The plug's own way out (+Z 25, the build's Step 23 reversed) runs into the back of the seated button after 9.2 mm. USB_B
     reaches z 1224.46 and BUTTON starts at z 1233.65, over the same x and y. So D2 and the button have to be out first, which the
     published guide also does (its USB cable is Step 20).
   - Removed earlier, the pin would pass through the plug, and the generator would log "passes through a part still there" with a
     Review note (stepgen.py:1056-1068).

What the house rules require:

4. **Lee's group: the three wires come off at both ends in one step.** This is how the MRA's eight breadboard wires came off
   (MRA deconstruction.py:236-239). The published guide instead unplugs three pins at the breadboard, one per step, and later pulls
   a single connector off the header in the hand. Our model has three separate sockets, and unplugging only the pins would need
   loose-wire shapes that the build never drew.
5. **D2: lifted out still wired, then unplugged, in two steps.** The published guide does both in one step (a swap). The rulebook
   says: "Wired modules are lifted off the housing first, still wired, and unplugged later." Both steps land exactly on states the
   Full Build already has (its Steps 24 and 21-22).
6. **The nut and the button keep one camera** (Lee, 18 Oct 2026: two steps on one sub-assembly in the hand keep one camera). The
   published guide turns to D2's outer face for the button.
7. **Cues follow the house rules:**
   - one arrow per unit, 15-40 mm long, never pointing at the camera;
   - eyes only on plugs;
   - a close-up, not an eye, for anything the camera cannot see;
   - no eyes on plates that simply lift (the published guide puts eyes on the stems and on D8 / D7);
   - one red box per close-up (`mark`; stepgen.py:1797-1800 keeps only target, dir, radius, hide, mark, alt, caption, arrows).
8. **The matrix is removed in a step of its own** (ours Step 21). In the published guide it is never removed: it simply does not
   come back after its isolated steps. In-house, a part once disconnected leaves by a step.

Kept from the published guide, where our build would otherwise do it differently:

- **D5 and D3 come off with the box the right way up**, from the published guide's corners. Our build put them on upside down
  (Steps 27-28), so their Full Build cameras are turned over and would turn the box over in the take-apart too (stepgen.py:1152-1159).
- **D3 is a straight pull, as published.** By then D4 and D5 are off, so the build's hinge (D3's tabs in D4's slots, guide.py:708-714)
  is gone.
- **D5 comes off early (published Step 4).** In our model this is free: D5 slides +X off tabs that all run along X, and D6 only
  touches its inner face (D6 x max 679.51 = D5 x min).
- **The order of the pairs, the posts' two-stage pull and the small parts' order are the published ones**, and they are also our
  build reversed:
  - the D11 pair at the D4 end first, then the pair at the D5 end;
  - each post pushed out of D1, then pulled out of D6;
  - R330, then the capacitor, then R12K, then the Nano.
- **Close-ups on the catches, as published.** The published guide has framed close-ups on Steps 2-7, 16 and 17 (eight steps), and
  so does this plan, on the same catches (whether to keep all of them is question 4).

Cameras:
- The published guide reused its own Full Build's camera for the step it undid wherever it could (five poses are bit for bit the
  same). This plan does the same with ours, which Lee approved step by step (many are Lee's own framings).
- New cameras only where the build's will not do:
  - D5 and D3: upright, from the published guide's corners;
  - D4, D10, the matrix's moves and the button's pins: the build's own camera, but given by hand, because the generator would not
    pick it (section 4).

## 3. The script, set-up (the MRA's, RCC's and PMG's pattern)

```python
"""Laser Stem Matrix (LSM), deconstruction ... (header as the MRA's / PMG's: what it is, Lee's request, this order and its reasons)"""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
from stepgen import Guide, apply_pose, compose, turned, via  # noqa: E402

# parts (guide.py:27-40; never `import guide`: guide.py:826 runs g.build() and would rewrite steps.json and parts.json)
D1, D2, D3, D4, D5, D6, D7, D8, D10 = 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D10'
D9_A, D9_B = 'D9_A', 'D9_B'
D11_A, D11_B, D11_C, D11_D = 'D11_A', 'D11_B', 'D11_C', 'D11_D'     # A, B at D5's end; C, D at D4's
BREADBOARD, BACKING, NANO, R12K, R330, CAP, MATRIX = 'BREADBOARD', 'BACKING', 'NANO', 'R12K', 'R330', 'CAP', 'MATRIX'
BUTTON, NUT, RED_PIN, BLACK_PIN = 'BUTTON', 'NUT', 'BTN_RED_PIN', 'BTN_BLACK_PIN'
USB_B, USB_A = 'USB_B', 'USB_A'
PINS = ['J_WHITE_M', 'J_GREY_M', 'J_PURPLE_M']                       # in i2, i3, b19 (the 'white' wire is shown and named yellow)
SOCKETS = ['J_WHITE_F', 'J_GREY_F', 'J_PURPLE_F']                    # on V+, V-, IN (they ride on MATRIX)
JUMPERS = ['wire white', 'wire grey', 'wire purple']
LEADS = ['lead red', 'lead black']
STEMS = [f'STEM_{k:02d}' for k in range(1, 65)]
DIAG = [-0.5792, 0.5736, -0.5792]

FULL = json.loads((HERE / 'steps.json').read_text(encoding='utf-8'))
VIEW = {v['name']: v for v in FULL['views']}
ROUTES = FULL['routes']

def camera_of(step, moved=None):                                     # (MRA deconstruction.py:55-60)
    c = VIEW[step]['camera']
    by = moved or [0.0, 0.0, 0.0]
    return dict(view_dir=c['dir'], frame=([round(a + b, 1) for a, b in zip(c['target'], by)], c['radius']))

routes = lambda step, ws: {w: ROUTES[VIEW[step]['wires'][w]] for w in ws}                      # a Full Build view's shapes
back_through = lambda done, ws: {w: [ROUTES[n] for n in VIEW[done]['wire_via'][w]][::-1] for w in ws}   # its stages, reversed

# the Full Build's poses, read from steps.json (relative to the seat)
D2_OUT = VIEW['Step 24']['path'][0]                                   # [0, 0, 57.1]   (guide.py:559)
P_HELD = VIEW['Step 32']['path'][0]                                   # [-0.2, 56.6, -0.3]   (guide.py:223)
P_LIFT = VIEW['Step 30c']['carry'][MATRIX]['via'][0]                 # [-90.8, 56.6, 25.1]  (guide.py:744)
P_OUTSIDE = VIEW['Step 30']['carry'][MATRIX]['pose']                 # [-90.8, 5.9, 25.1]   (guide.py:222)
OVER_THE_BOX = VIEW['Step 26c']['carry'][MATRIX]['via'][::-1]        # P_UP_OUTSIDE, P_MID, P_UP_BESIDE (guide.py:683-685)
P_BESIDE = VIEW['Step 26']['carry'][MATRIX]['pose']                  # turned 180 deg about the matrix's middle (guide.py:221)
SOCKET_OFF = [0.0, 0.0, 15.0]                                         # a socket 15 mm off its pin, along it (guide.py:224)
D11_SHORT, D11_UP = [0.0, 6.38, 0.0], [0.0, 85.0, 0.0]               # (guide.py:802)
NUT_AT = [638.23, 881.63, 1251.0]                                     # (guide.py:532; steps.json Step 20 'at')

def nut_turns(z0, z1, sign, turns=2):                                 # (copied from guide.py:537-540)
    n = 4 * turns
    return [turned([0, 0, 1], sign * 90.0 * k, NUT_AT, [0.0, 0.0, round(z0 + (z1 - z0) * k / n, 2)]) for k in range(1, n + 1)]

g = Guide(HERE, title='Laser Stem Matrix (LSM)', part='Deconstruction', names=dict(FULL['names']),
          steps_file='steps-deconstruction.json', source='lsm.glb', hero_azimuth=45,
          copyright_line='© TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')
g.take_apart(parts_list_at_end=True)                                 # (the Full Build's parts list after the Completed View, as the MRA's)
g.put_away([BACKING])                                                # (see the risk below)

def where(i):                                                         # (MRA deconstruction.py:108-113)
    if i in g.riding:
        by, rel = g.riding[i]
        return compose(where(by), rel, g._pivot(i))
    return g.resting.get(i)
```

**Notes on the set-up:**

- **`source='lsm.glb'`** is needed because Guide's default is `mra.glb`.
- **`hero_azimuth=45`** matches the Full Build (guide.py:92).
- **`names=dict(FULL['names'])`** carries the Full Build's hover names over (for example "Yellow Breadboard Wire").
- **The title page** is the Full Build's, which hides the USB cable (guide.py:103). It is copied because no `start_view` is given.
- **BACKING (risk)**:
  - `take_apart()` adds every part any Full Build view showed (stepgen.py:874-883).
  - BACKING, put away at Full Build Step 1 (guide.py:286), would come back riding on the breadboard at [0, -40, 0] (Step 1c's carry).
  - That places it 40 mm under the breadboard, below D1 and the table, and it can be seen from the low side cameras (Steps 5-6).
  - `g.put_away([BACKING])` straight after `take_apart()` should clear it, and makes Step 1 open as a cut from the title page.
  - put_away has no guard against being called before the first step, but this order has not been tried (the MRA, RCC and PMG do
    not do it). If build() objects, the fallback is a two-line change in take_apart(): skip a part that a later view puts away and
    never brings back.

## 4. The steps

Each step is given as:
- **(a) Caption.**
- **(b) The call.**
- **(c) The Full Build step(s) it undoes.**
- **(d) Why here, and its published counterpart.**
- **(e) Risk.**

"Default" means the generator's own choice: the Full Build's way reversed, by that step's camera (stepgen.py:1012-1035, 1152-1159).

### Step 1: the stems

- **(a)** "Pull all 64 LED stems straight up out of D8, D7 and D6."
- **(b)** `g.remove(..., STEMS, units=[STEMS])`
  - way: default, up 44;
  - camera: Step 40's (STEM_CAMERA, DIAG);
  - arrow: one, on the stem nearest the middle of the block (stepgen.py:1414-1416).
- **(c)** 40 + 39.
- **(d)** Published Step 1, with one arrow as published. Without `units`, STEM_01 (Step 39) and the 63 (Step 40) would be two units
  with two arrows.
- **(e)** None known. Camera: the published guide starts from near its title corner (az 32). Starting from ours (HERO, az 45) only
  moves the 180-degree swing to Step 2, because D8's code reads from DIAG. So the build's camera is kept.

### Step 2: D8

- **(a)** "Lift D8 up off the four D11 posts, past the latches at their tops."
- **(b)** `g.remove(..., [D8], inset=dict(target=[601.63, 934.0, 1166.2], radius=8.0, mark=3.0, caption='A latch at the top of a D11 post', alt='Close-up of the top of a D11 post: D8 sits just under its latch'))`
  - way: default, up 55;
  - camera: SHELF_CAMERA;
  - close-up: its direction defaults to the camera's. The target is D11_D's top, the post nearest the camera: D8's top is at y 932.36
    and the post's top at 935.76.
- **(c)** 38.
- **(d)** Published Step 2: its close-up of a corner latch.
- **(e)** The close-up target has not been seen.

### Step 3: D7

- **(a)** "Lift D7 off the D11 posts."
- **(b)** `g.remove(..., [D7], inset=dict(target=[601.63, 915.0, 1166.2], radius=8.0, mark=3.0, caption='D7 rests in a notch in each post', alt=...))`
  - way: default, up 65;
  - camera: SHELF_CAMERA.
- **(c)** 37.
- **(d)** Published Step 3: its close-up of a post's notch.
- **(e)** The close-up is optional: D7 has nothing to release (question 4).

### Step 4: D5

- **(a)** "Slide D5 off the end of the box, off the tabs of D1, D2 and D3."
- **(b)** `g.remove(..., [D5], look_from=[1, 1, -1], inset=dict(target=[684.0, 899.5, 1155.2], dir=[0.5792, 0.5736, -0.5792], radius=8.0, mark=3.0, caption="D3's tab comes through D5", alt=...))`
  - way: default, Step 28 reversed, +X 42;
  - camera: the D5 / D3 corner, upright, framed by the generator (published 37 / 139; Lee asked for this corner for D5's code,
    lee_notes_2026-10-19.md Step 27);
  - the close-up target is Lee's own lead-line point on D3's tab at D5 (guide.py:718-719).
- **(c)** 28.
- **(d)** Published Step 4. D5 can come off early: every tab through it runs along X, including D10's end tab in its open-topped slot.
- **(e)**
  - The order check tests D5's +X slide against D6, D9_A, D9_B, D10 and MATRIX, none of which were there at Step 28. If D10's tab
    touches the slot walls in the CAD, the log gives a WARNING and the step a Review note. The fix is a straight pull by hand,
    `direction=[1, 0, 0], hover=42`, which is not order-checked.
  - `look_from` makes the camera a hand-given one, so the turned-over Step 28 camera is not copied (stepgen.py:1152).

### Step 5: the two D11 posts at the D4 end

- **(a)** "Push the tabs of the two D11 posts at the D4 end back up out of the slots in D1, then pull the posts up out of D6."
- **(b)** `g.remove(..., [D11_C, D11_D], paths={i: [D11_SHORT, D11_UP] for i in (D11_C, D11_D)}, **camera_of('Step 35'), inset=dict(target=[601.63, 857.0, 1242.4], dir=[0.4109, -0.8401, 0.3541], radius=6.0, mark=3.0, caption='The tab through D1', alt='Close-up from below of a D11 tab through its slot in D1'))`
  - way: two beats, 6.38 mm then up to 85;
  - arrows: two, one per post (each `paths` part is its own unit), along the long pull;
  - close-up: the Full Build's Step 36c close-up (steps.json), moved to D11_C's slot, with a red box added.
- **(c)** 35, and the last 6.38 mm of 36.
- **(d)** Published Step 6 (this pair first, as published, and as our build reversed). The build's Step 36 (box turned over, D1 seen
  through) has no counterpart: a take-off step has no `ghost` (stepgen.py:953-956). Its content is the close-up, as the published
  guide does it.
- **(e)**
  - The D11s ride on D1 and have no Full Build record. Without `paths` they would be "lifted straight up, unchecked", with a Review
    note (stepgen.py:1040-1044).
  - The close-up is from below. Its eye point (about 17 mm off, under D1) is clear of D4 and D2 by the boxes, but has not been seen.

### Step 6: the two D11 posts at the D5 end

- **(a)** "Then the two D11 posts at the D5 end: push their tabs up out of D1 and pull them up out of D6."
- **(b)** As Step 5:
  - `[D11_A, D11_B]`;
  - `**camera_of('Step 34')`;
  - inset target `[674.83, 857.0, 1242.4]`.
- **(c)** 34, and the last 6.38 mm of 36.
- **(d)** Published Step 7. The camera is Lee's (the side the codes face, lee_notes_2026-10-19.md Step 33).
- **(e)** As Step 5.

### Step 7: D6

- **(a)** "Lift D6 off the tops of the walls."
- **(b)** `g.remove(..., [D6])`
  - way: default, up 64;
  - camera: Step 33's (D6's code readable).
- **(c)** 33.
- **(d)** Published Step 8.
- **(e)** None known. The posts that pass through its corner slots are already out.

### Step 8: the matrix lifted out with D10, still wired

- **(a)** "Lift the LED matrix, with D10 hooked under it, straight up out of the box. Leave its three wires plugged in."
- **(b)** `g.lift(..., [MATRIX], wire_via=back_through('Step 32c', JUMPERS), wires=routes('Step 32', JUMPERS))`
  - way: default, Step 32 reversed: through P_HALF to P_HELD, one beat;
  - camera: Step 32's;
  - wires: route 62-64 (HALF) on the way, then 59-61 (HELD);
  - riders: D10 and the three sockets go along.
- **(c)** 32.
- **(d)** Published Step 9, first half (its "hovering above the supports").
- **(e)** Low risk: it is the Full Build's own blend, played backwards. Without `wires=`, only the last 6 mm of each wire would follow
  the matrix (`b_from`, guide.py:264-265), because lift() never re-routes a lead by itself (stepgen.py:938-951).

### Step 9: D10 off the matrix

- **(a)** "Slide D10 along under the LED matrix towards D2 until its hooks let go of the matrix's edges, then lower it away."
- **(b)** `g.remove(..., [D10], paths={D10: [compose(where(MATRIX), [0.0, 0.0, 40.0], g._pivot(D10)), compose(where(MATRIX), [0.0, -22.0, 40.0], g._pivot(D10))]}, arrow_style={D10: dict(at=apply_pose(where(D10), [[590.0, 892.0, 1204.5]])[0].round(2).tolist())}, **camera_of('Step 31'))`
  - way: two beats, +Z 40 then down 22, i.e. the build's D10_UNDER and the Step 31c via, reversed. Worked out from P_HELD:
    [-0.2, 56.6, 39.7] then [-0.2, 34.6, 39.7];
  - arrow: by hand, just off D10's end at D4, outside the matrix, where Lee wanted the build's arrow (guide.py:754-759). Its
    direction comes from the longer stage, the slide.
- **(c)** 31.
- **(d)** Published Step 14, moved here (section 2, item 2). Camera: Lee's framing of the build's Step 31.
- **(e)**
  - D10 has no Full Build record. Without `paths` it would go straight up, through the matrix, with a Review note.
  - Wires: in the build, the HELD wires lie in D10's slot while it slides, so this is the build's own motion, reversed.

### Step 10: the matrix laid outside D4

- **(a)** "Carry the LED matrix over D4 and lay it down outside the box, LEDs up, its wires over the top edge of D4."
- **(b)** `g.lift(..., [MATRIX], path=[P_LIFT, P_OUTSIDE], wire_via=back_through('Step 30c', JUMPERS), wires=routes('Step 30', JUMPERS), **camera_of('Step 30'))`
  - way: two beats, as the build;
  - wires: LIFT (56-58) on the way, then OUTSIDE (53-55);
  - arrow: default, along the longer, level stage.
- **(c)** 30.
- **(d)** Published Step 9, second half ("lying on the table beside the box, still wired"). Our build's place for it is outside D4
  (README question 11: it is held in the air there, as in the published guide).
- **(e)** Low: the build's Step 30 played backwards, with the same parts present (D10 was not on yet in the build either).

### Step 11: both D9

- **(a)** "Lift both D9 LED supports up out of their slots in D2 and D3."
- **(b)** `g.remove(..., [D9_A, D9_B])`
  - way: default, up 65;
  - camera: HELD_CAMERA;
  - arrows: two, one each (two of a kind, apart; stepgen.py:1139-1143).
- **(c)** 29.
- **(d)** Published Step 10. The wires lie under D9_A's open-bottomed end, as they did when the build put it on.
- **(e)** None known.

### Step 12: the matrix carried back over the box, beside the base

- **(a)** "Lift the LED matrix again and carry it back over the box, turning it round, to lie beside the open end where D5 was."
- **(b)** `g.lift(..., [MATRIX], path=OVER_THE_BOX + [P_BESIDE], wire_via=back_through('Step 26c', JUMPERS), wires=routes('Step 26', JUMPERS), arrows=[dict(tail=[585.0, 862.4, 1133.0], head=[690.0, 862.4, 1133.0], normal=[0, 1, 0], part=D1, width=5.0)], **camera_of('Step 26'))`
  - way: four beats, as the build;
  - wires: routes 46 / 45 / 44 for white (and the same for the others), ending on BESIDE, 33-35;
  - camera: the build's view from above (Lee asked for it, lee_notes_2026-10-19.md Step 25);
  - arrow: the build's arrow on D1 (guide.py:703), turned round.
- **(c)** 26.
- **(d)** No published counterpart (section 2, item 1). It is needed so that D4 can come off and the USB cable and the wires can
  come out later.
- **(e)** The highest motion risk in the plan:
  - it is the only walk-back of a part that turns as it moves. The stages are the build's, played backwards, so they should blend as
    they did there (where the README notes two brief wire-to-wire touches);
  - D3 and D2 are present here but were not in the build's Step 26. All the wire shapes keep to z ≥ 1170 and the matrix stays above
    y 918, so they do not come near D3 or D2;
  - check with motioncheck.py.

### Step 13: D4

- **(a)** "Slide D4 outward off the tabs of D1, D2 and D3, then lift it up off the USB cable."
- **(b)** `g.remove(..., [D4], path=[[-8.0, 0.0, 0.0], [-8.0, 65.0, 0.0]], arrow_style={D4: dict(stage=0)}, **camera_of('Step 25'), inset=dict(target=[592.5, 901.4, 1253.4], dir=DIAG, radius=8.0, mark=3.0, caption="D2's tab comes through D4", alt=...))`
  - way: Step 25 reversed: off the tabs, then up, leaving the cable through the open notch;
  - arrow: on the outward slide, as published;
  - camera: BASE_CAMERA;
  - close-up target: on Step 25's lead line (guide.py:635).
- **(c)** 25.
- **(d)** Published Step 5, moved here (section 2, item 1).
- **(e)**
  - By default `remove(D4)` would use Step 31's stand-still way: no motion, no arrow, and the D10 camera (stepgen.py:1012-1016;
    steps.json Steps 26, 30, 31 move D4 by `[ZERO] * n`). So the way has to be given by hand.
  - -8 mm takes D4's inner face to 589.4, clear of the D2 / D3 tab ends at 590.58.

### Step 14: D3

- **(a)** "Pull D3 straight off the tabs at the end of D1."
- **(b)** `g.remove(..., [D3], direction=[0, 0, -1], hover=40.0, look_from=[-1, 1, -1], inset=dict(target=[638.2, 861.0, 1152.5], dir=DIAG, radius=10.0, mark=3.0, caption="D1's tab through D3", alt=...))`
  - way: straight -Z;
  - camera: the DIAG corner, upright;
  - close-up target: D1's middle tab, which goes through D3 (D1 reaches z 1150.0; D3's outer face is at 1153.68).
- **(c)** 27.
- **(d)** Published Step 16 (its straight pull, its close-up of the bottom tab; corner 31 / -124). With D4 and D5 off, the build's
  swing about D4 no longer applies.
- **(e)** Lee's new D3 has spring-cut latches (README); where they catch has not been checked. If they matter, the close-up should be
  on them.

### Step 15: D2 lifted out with the button, still wired

- **(a)** "Slide D2, with the push button, off the tabs at the other end of D1 and stand it beside the base. Leave the button's wires plugged in."
- **(b)** `g.lift(..., [D2], wires=routes('Step 24', LEADS), inset=dict(target=[638.2, 861.0, 1256.8], dir=[0.3, 0.45, 0.84], radius=10.0, mark=3.0, caption="D1's tab through D2", alt=...))`
  - way: default, Step 24 reversed, +Z 57.1 to D2_OUT;
  - camera: BASE_CAMERA;
  - riders: BUTTON and NUT go along;
  - leads: 42/43 change to 38/39;
  - close-up: from D2's outer side, which this camera cannot see (as the published guide's large close-up of D2's outer face).
- **(c)** 24.
- **(d)** Published Step 17, first half.
- **(e)** Low. The scene is the build's Step 24 exactly (matrix beside, BESIDE wires; no D3, D4, D5, D9 or D10).

### Step 16: the button's two pins unplugged

- **(a)** "Unplug the button's red wire from j5 and its black wire from j16."
- **(b)** `g.unplug(..., [RED_PIN, BLACK_PIN], **camera_of('Step 21'))`
  - way: default, Steps 21 and 22 reversed;
  - leads: route 36 / 37;
  - riders: each pin then rides on BUTTON;
  - cues: two eyes (the unplug default);
  - camera: Step 21's, which frames both j5 and j16 (Step 22's, the generator's default, may leave j5 at its edge).
- **(c)** 22 + 21.
- **(d)** Published Step 17, second half (its two eyes). Lee's grouping rule: the build did one wire per step.
- **(e)** Low. The pins' unplugged poses are drawn with D2 at D2_OUT, which is where Step 15 leaves it.

### Step 17: the nut, on its own

- **(a)** "Turn the nut off the back of the push button, inside D2, and slide it off the ends of the wires."
- **(b)**
  ```python
  turns = [compose(where(D2), q, g._pivot(NUT)) for q in nut_turns(0.0, -95.0, -1)]
  g.remove(..., [NUT], path=[via(q) if k not in (3, 7) else q for k, q in enumerate(turns)], alone=[D2, BUTTON, NUT, RED_PIN, BLACK_PIN],
           arrow_style={NUT: dict(at=apply_pose(where(NUT), [[649.24, 882.63, 1250.3]])[0].round(2).tolist())},
           **camera_of('Step 20', moved=D2_OUT))
  ```
  - motion: two turns, unscrewing (clockwise seen from the head; Lee, 19 Oct 2026), over two beats, one turn each;
  - it ends at -95, past the pins' ends (Step 18's NUT_OFF);
  - arrow: from the nut's rear face, 1 mm above the black lead, as Lee had the build's Step 18 (guide.py:546-547);
  - camera: the build's Step 20, from inside D2, moved with D2.
- **(c)** 20.
- **(d)** Published Step 18 (also seen from inside D2).
- **(e)**
  - Without `path`, the nut would be lifted straight up with a Review note: its Full Build record is shared with BUTTON
    (stepgen.py:1012).
  - The poses are composed through D2_OUT, so `turned()` angles over 180 degrees come out as shorter turns the other way. The player
    takes the shorter way between neighbouring quarter-turn poses, so the sense is kept; check it in the player.

### Step 18: the button, on its own

- **(a)** "Pull the push button out of D2 from its engraved side; its wires follow it through the hole."
- **(b)** `g.remove(..., [BUTTON], path=[compose(D2_OUT, [0.0, 0.0, 100.0])], alone=[D2, BUTTON, RED_PIN, BLACK_PIN], keep_camera=True)`, then `g.put_away([D2])`.
  - way: Step 19 reversed, +Z 100 from D2_OUT;
  - riders: the pins (riding the button since Step 16) and both leads go with it.
- **(c)** 19.
- **(d)** Published Step 19. One camera for both in-hand steps (house rule). The published guide turned to D2's outer face.
- **(e)**
  - BUTTON's last record is Step 20's stand-still way, so without `path` it would not move.
  - From inside D2, the generator's arrow starts just past the button's head, behind D2, and is moved along until it can be seen,
    which may put it far off. If so, give `arrow_style={BUTTON: dict(at=<beside the button's back end, inside D2>, scale=0.5)}`, short
    enough to stop at D2's inner face (z 1251.93 + 57.1).

### Step 19: the USB cable

- **(a)** "Unplug the USB cable's Mini-B plug from the Nano Board and lift the cable away."
- **(b)** `g.remove(..., [USB_B, USB_A], units=[[USB_B]], paths={USB_A: [[0.0, 25.0, 0.0]]}, arrow_scale=2.5)`
  - way: default for the plug, Step 23 reversed, +Z 25;
  - the A end is lifted with it;
  - camera: Step 23's BASE_CAMERA;
  - arrow: one, on the plug, as the MRA (×2) and the RCC (×4) do;
  - arrow size: the default 15 mm is only 0.12 of this camera's radius of 125.
- **(c)** 23.
- **(d)** Published Step 20 (same place in the order).
- **(e)** Low. The cable passes D4's old notch, and D4 is off. Lee may want the arrow bigger.

### Step 20: the three breadboard wires, both ends at once (Lee's group)

- **(a)** "Unplug the yellow, grey and purple wires from i2, i3 and b19, and pull their other ends off the pins of the LED matrix."
- **(b)**
  ```python
  g.remove(..., PINS + SOCKETS, paths={s: [compose(where(MATRIX), SOCKET_OFF, g._pivot(s))] for s in SOCKETS}, arrows=[],
           eye=[dict(id='J_WHITE_M', anchor=[650.08, 880.0, 1171.72]), dict(id='J_PURPLE_M', anchor=[627.04, 880.0, 1213.63])],
           inset=dict(target=[757.9, 872.7, 1228.0], dir=[0.3, -0.8, 0.52], radius=12.0, mark=5.0,
                      caption='The three sockets under the LED matrix', alt='Close-up from below of the sockets on the matrix pins'),
           keep_camera=True)
  ```
  - pins: default, Steps 11-13 reversed, up 30;
  - sockets: 15 mm off their pins along them, which is -Z in assembly space, since the matrix is turned round;
  - the three leads go with their ends (stepgen.py:1116-1124);
  - eyes: one on the i2 / i3 pair and one on b19 (the MRA's one eye per group of ends);
  - the sockets are under the board, so they get a close-up from below instead of an eye;
  - camera: kept from Step 19, BASE_CAMERA. With D3 off, i2 and i3 can be seen from DIAG.
- **(c)** 17, 16, 15 and 13, 12, 11.
- **(d)** Published Steps 11-13 and 15, merged as Lee asked, and moved after the USB cable (section 2, item 3).
- **(e)**
  - The inset target is worked out from P_BESIDE: the purple socket's middle is at about [757.9, 872.7, 1232.1].
  - BASE_CAMERA covers x 505-755, so the sockets sit at its edge. If the matrix is cut off, use `look_from=[1, 1, -1]` (the
    published guide's side, az 122), framed by the generator.
  - Each wire's two ends move different ways (pins up, sockets along). Only the last 6 mm follow the socket (`b_from`), so a wire
    stretches a little before it fades. Check it with motioncheck.

### Step 21: the matrix away

- **(a)** "Lift the LED matrix away."
- **(b)** `g.remove(..., [MATRIX], direction=[0, 1, 0], hover=40.0, keep_camera=True)`
- **(c)** None: the matrix came in at Steps 15 and 21.
- **(d)** In-house rule: a part once disconnected leaves by a step. The published guide never removes it.
- **(e)** Without `direction`, the matrix (not in its seat) would be "lifted straight up, unchecked" with a Review note.

### Step 22: the 330 Ohm resistor

- **(a)** "Pull the 330 Ω resistor out of a11 and a19."
- **(b)** `g.remove(..., [R330])`
  - way: default, up 30;
  - camera: Step 9's;
  - its legs go with it.
- **(c)** 9.
- **(d)** Published Step 21. It comes after the USB plug (USB_B's box overlaps R330's).
- **(e)** None known.

### Step 23: the capacitor

- **(a)** "Pull the capacitor out of j2 and j3."
- **(b)** `g.remove(..., [CAP])`
  - way: default, up 29;
  - camera: Step 7's.
- **(c)** 7.
- **(d)** Published Step 22. It comes after D9_B (their boxes overlap 1.7 mm).
- **(e)** None known.

### Step 24: the 12 kOhm resistor

- **(a)** "Pull the 12 kΩ resistor out of h3 and h16."
- **(b)** `g.remove(..., [R12K])`
  - way: default, up 32;
  - camera: Step 5's;
  - its legs go with it.
- **(c)** 5.
- **(d)** Published Step 23. It comes before the Nano (their boxes overlap 1.2 mm).
- **(e)** None known.

### Step 25: the Nano Board

- **(a)** "Pull the Nano Board up out of the breadboard."
- **(b)** `g.remove(..., [NANO])`
  - way: default, up 35;
  - camera: Step 3's.
- **(c)** 3.
- **(d)** Published Step 24.
- **(e)** None known.

Then `g.build()`.

## 5. The end, the parts list, the website entry

- **Completed View.** What is left is D1 with the breadboard stuck on it, as the published guide ends. It is seen from the last step's
  direction (DIAG) and framed close on what is left (stepgen.py:2040-2048).
- **Parts list.** The Full Build's two parts list pages ("Parts List", "Parts List (Cont.)") follow the Completed View, through
  `take_apart(parts_list_at_end=True)`, as the MRA's and the PMG's do.
- **No counterpart** in this guide for these Full Build steps:
  - 1 (backing);
  - 2 (breadboard onto D1; it stays);
  - 4 and 8 (bending the resistor legs);
  - 6 and 14 (the capacitor and matrix look-steps);
  - 10 (the ribbon split);
  - 18 (the nut off a new button).
- **guides.json entry**, after `laser-stem-matrix-full-build`:
  `"laser-stem-matrix-deconstruction": {"kit": "laser-stem-matrix", "steps": "steps-deconstruction.json", "label": "Deconstruction", "script": "deconstruction.py"}`.
  Then run `python3 tools/site_pages.py`, which writes the guide's framing rules into render.yaml.
- **Card.** The website card is the Full Build's: `_dev.card()` on `player.html?steps=steps-deconstruction.json` copies it.

## 6. Ours against the published guide

| ours | published | build step undone | note |
|---|---|---|---|
| 1 stems | 1 | 40 + 39 | |
| 2 D8 | 2 | 38 | close-up kept |
| 3 D7 | 3 | 37 | close-up kept (optional) |
| 4 D5 | 4 | 28 | upright, published corner |
| 5 D11 C, D | 6 | 35 (+36) | close-up of the tab through D1 |
| 6 D11 A, B | 7 | 34 (+36) | |
| 7 D6 | 8 | 33 | |
| 8 matrix + D10 lifted, still wired | 9 (first swap) | 32 | |
| 9 D10 off | 14 (on its own) | 31 | earlier: forced |
| 10 matrix laid outside D4 | 9 (second swap) | 30 | |
| 11 D9 x2 | 10 | 29 | |
| 12 matrix back over the box, beside the base | none | 26 | forced |
| 13 D4 | 5 | 25 | later: forced |
| 14 D3 | 16 | 27 | straight pull, as published |
| 15 D2 lifted, still wired | 17 (part) | 24 | house rule: lifted, then unplugged |
| 16 both button pins | 17 (part) | 22 + 21 | |
| 17 nut (on its own) | 18 | 20 | |
| 18 button (on its own) | 19 | 19 | one camera (house rule) |
| 19 USB cable | 20 | 23 | |
| 20 three wires, both ends | 11-13 + 15 | 17-15, 13-11 | later: forced; merged: Lee |
| 21 matrix away | none (never removed) | none | house rule |
| 22 - 25 R330, CAP, R12K, Nano | 21 - 24 | 9, 7, 5, 3 | |

## 7. The closer variant not taken

Taking D4 off at the published Step 5, and laying the matrix aside only once, is possible, but only with wire shapes our build does
not have:
- an "aside" shape for each jumper: in the box as now (IN_BOX, guide.py:645-647), then out through the open D4 end at about y 882,
  under D10 at P_OUTSIDE, up through D10's slot, and on to the socket (SEATED_TAIL, moved with the matrix);
- either a fade to it (`lift(..., reappear=True)`, as the PMG's Step 42, which Lee approved for that step only), or new in-between
  shapes, checked with motioncheck. Blending HELD straight into such a shape is untested and could fold the wires.

Even then, the three wires would still have to come off after the USB cable (section 2, item 3), so they could not go at the
published Steps 11-13. The gain would be two steps (Steps 10 and 12 become one) and D4 in its published place. The cost is three new
wire shapes in a kit where Lee has checked every wire (lee_notes_2026-10-19b.md). This is offered to Lee as question 1, not planned.

## 8. Checks for whoever writes and runs it (one heavy job at a time)

1. Copy steps.json first. Afterwards check that steps.json is unchanged and that no Full Build camera has moved (memory: keep step
   cameras).
2. Read the log for:
   - WARNING lines (way through a part still there; not in its seat);
   - NOTE lines (more than two arrows; Full Build sub-assembly camera; camera leaves out a part lying aside);
   - the effect of the BACKING put_away.
3. Run `motioncheck.py "LSM Build Instructions" --steps steps-deconstruction.json`. Pay most attention to Steps 12, 8, 10, 15, 16
   and 20.
4. Run `wirecheck.py "LSM Build Instructions" steps-deconstruction.json`.
5. Run `_runthrough()` on `player.html?steps=steps-deconstruction.json`, and on the Full Build (82 views).
6. Look at every close-up and at the hand-placed arrows (Steps 9, 17, 18) at 1280, 1000 and 768 px.
7. Publish only to the test site (`share/Test guides preview`), never to `site/` or `live` without Lee's word. Commit only this
   guide's files: other sessions have uncommitted LAC, CLAUDE.md and motioncheck.py changes.

## 9. Questions for Lee

1. **D4.** Our build lays the LED matrix outside D4 with its wires over D4's top edge. Keeping to shapes Lee has already checked means
   D4 comes off after the matrix (ours Step 13, published Step 5), and the matrix is carried out over D4 and back again (Steps 10 and
   12). The alternative is to draw new wire shapes, so that D4 can come off where the published guide has it and the matrix is laid
   aside only once (section 7). Which?
2. **The three breadboard wires.**
   - The purple wire's pin sits under the USB plug, so all three come off together after the USB cable (Step 20), at both ends at
     once, as the MRA's eight did.
   - The cues would be eyes on i2 / i3 and on b19, plus a close-up of the sockets under the matrix, with no hole labels (as published).
   - The matrix then goes in a step of its own.
   - Is that right?
3. **The D11 posts:** in pairs, as published and as the build (Steps 5-6), or all four in one step?
4. **Close-ups:** all eight the published guide has (including D7's, which holds nothing), or only real catches (D8's latches, the
   posts' tabs through D1, the walls' tabs)?
5. **Power first.** The MRA, RCC and PMG take-aparts unplug the power first, but the LSM's Mini-B plug cannot come out until D2 and
   the button are off (Step 19). Should Step 1 have a caution to unplug the USB cable from the computer first?
