# LAC round 2: lead-line labels flung to the edges of the screen (21 Oct 2026)

Lee: "there are a lot of steps where the lead line labels on this kit are flung to the edges of the screen and they should be moved
closer to their target piece" (named: Steps 3, 5, 6, 7, 9 - 18, 20, 21, 30 - 34, 36; Step 43 "move the eyeball above the buzzer";
Step 49 "F8 ... up and to the right of F8"). Read-only study: nothing in the project was changed, nothing regenerated.

## In short

- Every hole label in this kit is given a **side of the model** (`'left'`, `'right'`, or `'top'` for part names; `sides()` and
  `away_from()` in guide.py, and by hand in Steps 3, 5 - 7, 15). The player puts such a label **outside the box round every part and
  wire on screen** and then pushes it back inside the window. In the LAC's close frames (radius 26 - 76 mm) F3 (86 x 159 mm), the
  breadboard and the long switch, potentiometer, buzzer and USB leads reach well past the window, so that box is wider than the window
  and **every `'left'` label lands 8 px from the left edge, every `'right'` one 8 px from the right edge, every `'top'` one at the top
  (y = 64)**. At Lee's window (2000 x 1016 CSS px) the leaders are 500 - 1000 px long (Step 38's b8: 1017 px).
- The fix is the other kind of side the player already has: a place **beside the label's own spot** (`'near-left'`, `'near-right'`,
  `'up-right'`, ... with `reach`, a share of the window's width), as the PMG does. Proposed: a small helper `near()`, `sides()` and
  `away_from()` returning near places (0.05 of the width: 100 px at Lee's 2000 px, 50 px in the LMS's 1000 px frame), and a place
  for each label and eye of every step, chosen at eight window shapes so that none overlaps another label or eye, none goes under the
  caption, none covers the cap or part being placed or its wire, and leaders do not cross. Code below, ready to paste.
- Leaders after the change: 90 - 215 px at Lee's 2000 px (was 100 - 1017), 44 - 123 px at 1000 px.

## Why: how the player places a label (player/js/player.js, current file)

`layoutCallouts()` (player.js:373 - 415), laid out once as each view opens (player.js:429; only the leader follows the part after):

- Size: font `max(15, min(28, 0.027 W))` px, a label's box = text width + 20 by font + 12; an eye `max(44, 0.07 W)` by 0.56 of that
  (player.js:374, 377). W = the window's (stage's) width in CSS px; Lee's screenshots are 2000 x 1016 (the bar is 86 px of 1102).
- `R` = `screenRect()` (player.js:349): the screen box of the 8 corners of every visible part's box, at its pose in the view, and of
  every 4th point of every wire drawn in it.
- A **model side** (player.js:393 - 396): `'right'` puts the box at `R.x1 + gap` (gap `max(14, 0.02 W)`), `ay - h - 1.6 gap` (a
  little above the spot); `'left'` at `R.x0 - gap - w`; `'top'` at `ax + gap`, `R.y0 - gap - h`; `'bottom'` at `R.y1 + gap`. Then
  clamped into `[8, W - w - 8] x [64, H - h - 12]` (player.js:398). With `R` wider than the window the clamp is what places the label:
  at the window's edge.
- **No side**: the side with room (`room >= 0`) nearest the spot (player.js:381 - 388); none with room: `'float'`, 90 px from the spot
  diagonally up and towards the window's middle (player.js:397).
- A **near side** (`NEAR`, player.js:371; placed at player.js:389 - 392): `d = (reach || 0.07) * W`; the box's nearest corner `d`
  across and `d` up or down from the spot (`up-right`, `up-left`, `down-right`, `down-left`), or the box's middle `1.25 d` straight
  across / up / down (`near-left`, `near-right`, `near-above`, `near-below`). The leader runs from the nearer end of the underline
  (or the eye's middle) to the spot: `1.41 d` for a diagonal, about `1.25 d` for a level one. Then the same clamp.
- Rules that matter for near places, in narrow windows most:
  1. `d` scales with the window's **width**, the model with its height (wider than 1:1) or width (narrower): the same `reach` sits a
     little further out, relative to the model, in a wide window; this kit's choices were checked from 2000 x 1016 to 700 x 634.
  2. The clamp: a near label whose place is off the window is pushed back in, possibly onto its own part (Step 49's F8 in windows
     under about 880 px, F8 being near the right edge of Lee's camera).
  3. Under the caption: a label or eye that overlaps the caption box (top left; in windows of 700 px or less the full width at top
     46 px) is moved down to just under it (player.js:400 - 403), far from its spot. None of the proposed places is, at any size tried.
  4. **Near labels are not kept apart**: the stacking that keeps labels on one side from overlapping (player.js:405 - 413) covers
     only `'right'`, `'left'`, `'top'`, `'bottom'` and `'float'`. Two near places must be chosen apart by hand (two labels both
     `near-left` are fine only if their spots are far enough apart on screen: Steps 7, 14, 33 below were checked for it).
  5. Close-ups keep clear of labels and leaders (`buildInset()`, player.js:473 - 567, the keeping clear from 530), but every LAC
     close-up is on a Step Nc, which has no labels.
- The generator passes `side` and `reach` through as given (tools/stepgen.py:1509, 1513) and finds the anchor of a label or eye given
  by `id` alone (tools/stepgen.py:1858 - 1860), so `dict(id=F3, text='F3', side=..., reach=...)` and `dict(id=cap, side=..., reach=...)`
  work as they are.

## How the LSM and the PMG do it

- **The LSM** gives its hole labels no side (`hole_label()`, LSM guide.py:122; Step 3's c16 `'right'`, Lee's), so the player picks the
  side with room. Its labels are not close either: at 2000 x 1016 its Steps 3 - 22 hole labels have leaders of 350 - 690 px (measured
  the same way). They are not at the window's edge only because the LSM's base fits inside its frames, so there is white space between
  the model and the edge. Its capacitor (Step 6) uses `'down-left'` / `'down-right'` and the eye `'near-left'`, default reach 0.07.
- **The PMG** uses near places throughout (PMG guide.py:509 - 577, 1151): module pins `'up-right'`, `'near-left'` 0.08; device pins
  `'near-below'` 0.12 - 0.145, `'down-right'` 0.05; button names `'up-right'` 0.10 - 0.16 (`NAME_REACH`, "the least that clears the
  caption box at LMS sizes"); the parked wire's eye `'near-below'` 0.05 - 0.09. That is the model followed here.

## The proposal, as guide.py code

Line numbers are those of `LAC Build Instructions/guide.py` as it stands now, with the other round-2 agents' changes in it
(`SWITCH_CAMERA`, `POT_CAMERA`, `BUZZER_CAMERA`, Step 49's `side='up-right'` and camera). Every place below was chosen with those
cameras (round2/cameras.md) for Steps 16 - 18, 30 - 34 and 49, and the committed ones elsewhere. Step numbers are the player's.

### 1. The helpers (replace lines 181 - 192, `sides()` and `away_from()`)

```python
NEAR_REACH = 0.05     # how far a label sits from its own spot, as a share of the window's width (player.js layoutCallouts NEAR):
                      # 100 px in Lee's 2000 px window, 50 px in the LMS's 1000 px frame


def near(side, reach=NEAR_REACH):
    """A label's (or an eye's) place beside its own spot: 'near-left' / 'near-right' level with it, 'up-left' ... 'down-right' diagonally,
    'near-above' / 'near-below' straight over or under it; `reach` a share of the window's width. Not a side of the model ('left',
    'right', 'top'): the player puts those outside the box round every part and wire on screen, which in this kit's close frames (F3, the
    breadboard and the long leads reach past the window) is the window's edge (Lee's second round, 21 Oct 2026: "flung to the edges of
    the screen"). The player does not keep near labels apart: each step's are chosen clear of each other (round2/labels.md)."""
    return dict(side=side, reach=reach)


def sides(labels, view_dir, places=None):
    """Labels on spots side by side: the left one beside its spot to the left, the right one beside its spot to the right, level with
    them, so that neither sits on the parts between them nor do their leaders cross (Lee, 20 and 21 Oct 2026); or at `places`
    ([(side, reach), ...] in the labels' order) where a step needs others."""
    out = [dict(l) for l in labels]
    if places:
        return [dict(l, **near(*p)) for l, p in zip(out, places)]
    order = sorted(range(len(out)), key=lambda k: screen_x(out[k]['anchor'], view_dir))
    out[order[0]].update(near('near-left'))
    out[order[-1]].update(near('near-right'))
    return out


def away_from(label, part_point, view_dir):
    """A label beside its spot, on the side away from a part (the switch, the potentiometer) that its wire comes from."""
    return dict(label, **near('near-right' if screen_x(label['anchor'], view_dir) > screen_x(part_point, view_dir) else 'near-left'))
```

(`away_from()` is then used by no step below, each step having its place in a table; keep it or delete it.)

### 2. The breadboard, the Nano Board, the resistors, the clock module

Line 255 (Step 1; the arrow under the board's front corner is 300 px below the label at 2000 px):
```python
        labels=[dict(id=BREADBOARD, text='Breadboard', **near('near-right'))], look_from=BENCH_LOOK)   # (beside it, clear of the arrow)
```
Line 260 (Step 2): `labels={F3: 'F3'}` becomes `labels=[dict(id=F3, text='F3', **near('down-left', 0.035))]`.

Lines 263 - 264 (Step 3):
```python
        labels=[dict(id=NANO, text='Nano Board', **near('down-left')), dict(text='c15', anchor=HOLES['c15'], id=BREADBOARD, **near('near-right')),
                dict(text='g1', anchor=HOLES['g1'], id=BREADBOARD, **near('near-left'))],   # (each hole's label beside it on its own side, its leader across its lead line)
```
Lines 317 - 318 (Steps 5, 6):
```python
            labels=[dict(text='(-) blue', anchor=[paths['breadboard']['rails']['- blue'], BB_TOP, HOLES[h][2] + 1.1], id=BREADBOARD, **near('near-left')),
                    dict(text=h, anchor=HOLES[h], id=BREADBOARD, **near('up-right'))],   # (each beside its hole on its own side, clear of the resistor)
```
Lines 324 - 325 (Step 7):
```python
        labels=[dict(id=RTC, text='Real Time Clock', **near('near-left')), dict(text='j24', anchor=HOLES['j24'], id=BREADBOARD, **near('near-right')),
                dict(text='j19', anchor=HOLES['j19'], id=BREADBOARD, **near('near-left'))],
```

### 3. The jumper wires (Steps 8 - 14, 19 - 21)

After line 423 (`JUMPER_DIRS.update(...)`), add:
```python
# Each wire's two hole labels beside their holes, in the order the wire's ends are listed (Lee's second round, 21 Oct 2026: close to the
# holes, not at the window's edges): level and outwards where that is clear, else below or above (clear of the wires already in).
JUMPER_PLACES = {'black': [('near-right', 0.05), ('near-left', 0.05)],      # Step 9: i23, (+) red
                 'green': [('near-left', 0.05), ('near-right', 0.05)],      # Step 10: (-) blue, i24
                 'purple': [('near-left', 0.05), ('down-left', 0.05)],      # Step 11: a8, i22 (under it: to its right are the black and green wires)
                 'blue': [('near-left', 0.05), ('down-left', 0.05)],        # Step 12: a9, i21 (the same)
                 'white': [('down-right', 0.035), ('near-left', 0.05)],     # Step 13: a14, (-) blue
                 'dark_red': [('near-left', 0.065), ('near-left', 0.05)],   # Step 14: a12, (+) red (both to the left: to a12's right are the
                                                                            #   Nano Board and the purple and blue wires; a12's is the higher)
                 'orange': [('up-left', 0.05), ('down-right', 0.035)],      # Step 20: j1, i27
                 'yellow': [('up-left', 0.05), ('near-right', 0.05)]}       # Step 21: j3, i29
```
Line 396 (Steps 8, 19, the ribbon peeled): `eye=[dict(anchor=mid.round(2).tolist())]` becomes
`eye=[dict(anchor=mid.round(2).tolist(), **near('up-right'))]`.

Line 405: `labels=sides([hole_label(la, ca), hole_label(lb, cb)], view_dirs[colour]),` becomes
```python
                paths={ca: [UP, ZERO], cb: [UP, ZERO]}, lines=False, labels=sides([hole_label(la, ca), hole_label(lb, cb)], view_dirs[colour], JUMPER_PLACES.get(colour)),
```

### 4. The switch (Steps 15 - 18; Lee's camera for 16 - 18, `SWITCH_CAMERA`)

Line 468 (Step 15):
```python
        labels=[dict(id=F4, text='F4', **near('down-left', 0.035)), dict(id=SWITCH, text='Rocker Switch', **near('near-left'))],
        wires={f'switch {c}': switch_lead(c, cap, e, FLAT_F4) for c, cap, _, e in SWITCH_LEADS},
```
Before line 478 (`for colour, cap, label, exit_ in SWITCH_LEADS:`), add:
```python
# Each step's hole label and the eye on the cap held over the hole, beside them (Lee's second round, 21 Oct 2026). In Lee's camera the
# holes are on the right of the board, the switch and its leads up to the right: both to the right, in the white space beside the board
# (the tan wire's (+) red on the board's left: its eye up and to the right, clear of the jumper wires there).
SWITCH_PLACES = {'red': (('near-right', 0.05), ('near-right', 0.05)),       # Step 16: j27
                 'tan': (('near-right', 0.05), ('up-right', 0.035)),        # Step 17: (+) red
                 'black': (('near-right', 0.05), ('near-right', 0.05))}     # Step 18: j29
```
Line 483:
```python
            labels=[dict(hole_label(label, cap), **near(*SWITCH_PLACES[colour][0]))], eye=[dict(id=cap, **near(*SWITCH_PLACES[colour][1]))],
```

### 5. The potentiometer and F1 (Steps 22, 25, 29, 30 - 32; Lee's camera for 30 - 32, `POT_CAMERA`)

Line 565 (Step 22; the arrow along the shaft runs to the left, the label is right of the potentiometer):
```python
            labels=[dict(id=POT, text='Potentiometer', **near('down-right', 0.035))] if first else [],   # (beside it, clear of the knob and the arrow)
```
Line 574 (Step 25): `labels={F1: 'F1'}` becomes `labels=[dict(id=F1, text='F1', **near('near-left'))]`.
Line 596 (Step 29): `eye=[F1]` becomes `eye=[dict(id=F1, **near('down-right', 0.065))]`.
Line 626 (Steps 30 - 32; in Lee's camera to the right of the holes is white space, the leads coming in above it):
```python
            labels=[dict(hole_label(label, cap), **near('near-right'))], eye=[dict(id=cap, **near('near-right'))],
```

### 6. The buzzer (Steps 33, 34; Lee's camera, `BUZZER_CAMERA`)

Before line 746 (`for k, (colour, cap, label, ...) in enumerate(BUZZER_LEADS):`), add:
```python
BUZZER_PLACES = {'red': (('near-left', 0.05), ('up-left', 0.035)),         # Step 33: j4, and the eye on the lying cap
                 'black': (('near-right', 0.05), ('near-left', 0.05))}      # Step 34: (-) blue (at the board's end: white space to its right)
```
Lines 753 - 754:
```python
            labels=([dict(id=BUZZER, text='Alarm Buzzer', **near('near-left', 0.065))] if k == 0 else []) + [dict(hole_label(label, cap), **near(*BUZZER_PLACES[colour][0]))],
            eye=[dict(id=cap, **near(*BUZZER_PLACES[colour][1]))], wires={f'buzzer {c}': buzzer_straight(c, cp, e) for c, cp, _, e, _, _ in BUZZER_LEADS} if k == 0 else None,
```

### 7. The LCD (Steps 35 - 39)

Line 808 (Step 35):
```python
        appear=[LCD] + LCD_MALE + LCD_FEMALE, lines=False, labels=[dict(id=LCD, text='LCD Screen', **near('down-right'))],
        eye=[dict(anchor=_mid.round(2).tolist(), **near('near-left', 0.035))],
```
Before line 892 (`for k, (colour, male, label, fem, pin, ...) in enumerate(LCD_WIRES):`), add:
```python
# Each step's pin label (on the lying LCD's header), hole label and the eye on the loose wire, beside their spots (Lee's second round,
# 21 Oct 2026): the pin's towards the board (between the header and F3: to its left lies the buzzer), the hole's up and to the right or
# level to the right (clear of the wires already in), the eye to the left of the wire it points at.
LCD_PLACES = {'purple': (('near-right', 0.035), ('up-right', 0.05), ('near-left', 0.035)),   # Step 36: GND, (-) blue
              'yellow': (('near-right', 0.035), ('up-right', 0.05), ('near-left', 0.035)),   # Step 37: VCC, (+) red
              'teal': (('near-right', 0.05), ('near-right', 0.065), ('near-left', 0.035)),   # Step 38: SDA, b8
              'blue': (('near-right', 0.035), ('near-right', 0.065), ('near-left', 0.05))}   # Step 39: SCL, b9
```
Line 897 (`hole = away_from(...)`) is no longer needed; lines 902 - 903 become:
```python
            labels=[dict(text=pin, anchor=fem_centre(fem).round(2).tolist(), id=LCD, **near(*LCD_PLACES[colour][0])),
                    dict(hole_label(label, male), **near(*LCD_PLACES[colour][1]))],
            eye=[dict(anchor=[x, TABLE_Y + 1.0, LCD_Z], **near(*LCD_PLACES[colour][2]))], wires_done={f'lcd {colour}': [done, done]},
```

### 8. The case (Steps 41 - 56)

| line | step | now | becomes |
|---|---|---|---|
| 975 | 41 | `labels={F7A: '2x F7'}` | `labels=[dict(id=F7A, text='2x F7', **near('near-right', 0.065))]` |
| 985 | 43 | `eye=[BUZZER]` | `eye=[dict(id=BUZZER, **near('up-left'))]` (above the buzzer, Lee; to the left, off its way: it is lifted straight up and carried right, to the F7s, and the eye stays where it was placed) |
| 988 | 44 | `eye=[F7A, F7B]` | `eye=[dict(id=F7A, **near('near-right')), dict(id=F7B, **near('down-left'))]` |
| 989 | 45 | `labels={F9: 'F9'}` | `labels=[dict(id=F9, text='F9', **near('near-left', 0.035))]` |
| 1004 | 46 | `eye=[F1]` | `eye=[dict(id=F1, **near('up-left'))]` |
| 1009 | 47 | `eye=[F4]` | `eye=[dict(id=F4, **near('down-left'))]` (not above: F4 is lifted into that space) |
| 1021 | 49 | `side='up-right'` (default reach 0.07, already in) | keep (or `**near('up-right', 0.07)`, to say the reach): clear at Lee's window and the LMS's; see the caveat for windows under 880 px |
| 1049 | 50 | `eye=[LCD]` | `eye=[dict(id=LCD, **near('up-left'))]` (check again once Step 50's motion and camera are changed) |
| 1073 | 52 | `eye=[F1]` | `eye=[dict(id=F1, **near('up-right', 0.035))]` |
| 1092 | 55 | `labels={F2: 'F2'}, eye=[dict(anchor=[643.13, 889.0, 1339.4], id=F2)]` | `labels=[dict(id=F2, text='F2', **near('near-right', 0.08))], eye=[dict(anchor=[643.13, 889.0, 1339.4], id=F2, **near('near-below'))]` |
| 1099 | 56 | `labels={F6: 'F6'}` | `labels=[dict(id=F6, text='F6', **near('down-right', 0.065))]` |

Left as they are: Step 4 (already `'up-left'` / `'down-right'` beside the resistor, 198 / 227 px at 2000 px: Lee's first round),
Step 40 (USB Cable: `'float'`, 103 px from its spot), Step 54 (F5: beside F5, 107 px; a near place there lies over the lead lines).

The same edits as a patch against guide.py as it stands now (checked with `git apply --check`; the edited file compiles; not run):
`/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/46c40992-e0fc-4f94-b08e-62c20da998a4/scratchpad/labels/labels.patch`
(scratchpad: re-make it if guide.py has moved on).

## Every labelled view: where each label and eye lands now, and where it would

Lee's 2000 x 1016 window, the committed steps.json (so Steps 16 - 18, 30 - 34 and 49 with their old cameras: with Lee's cameras, now in
guide.py, the hole labels of 16 - 18 still land at x = 24 - 70, those of 30 - 34 at x = 8, leaders 436 - 943 px, the eyes of 16 - 18 and
30 - 32 at the top edge, y = 64). "Leader after" is with Lee's cameras for those steps, at 2000 x 1016 / 1000 x 634 (the LMS's frame) /
700 x 634 (an iPad in the LMS). Bold: steps Lee named. Anchors as in steps.json (a hole label's on the breadboard's top at the hole; a
part's or an eye's found by the generator when only `id` is given; a cap's in its seat, the view's pose moving it).

| Step | label / eye | anchor (assembly mm; part) | side now | lands now, committed camera, 2000 x 1016 (x, y of the box; leader px) | proposed | leader after (2000 / 1000 / 700 px) |
|---|---|---|---|---|---|---|
| Step 1 | Breadboard | [663.9, 897.1, 1302.6] NAUO1 | top | (1119, 84); 167 | `near-right`, 0.05 | 127 / 65 / 46 |
| Step 2 | F3 | [702.1, 887.6, 1268.3] NAUO2 | unset -> left | (559, 582); 406 | `down-left`, 0.035 | 130 / 82 / 61 |
| **Step 3** | Nano Board | [677.7, 901.8, 1323.0] NANO | top | (1041, 74); 200 | `down-left`, 0.05 | 172 / 102 / 75 |
| **Step 3** | c15 | [684.2, 897.1, 1306.6] NAUO1 | right | (1924, 634); 863 **at the window edge** | `near-right`, 0.05 | 127 / 65 / 46 |
| **Step 3** | g1 | [668.8, 897.1, 1342.1] NAUO1 | left | (368, 442); 531 | `near-left`, 0.05 | 127 / 65 / 46 |
| Step 4 | 2x - 12 kΩ Resistor | [682.5, 903.5, 1276.8] NAUO6 | up-left | (584, 293); 198 | unchanged | - |
| Step 4 | eye | [682.5, 901.2, 1274.3] NAUO6 | down-right | (1173, 667); 227 | unchanged | - |
| **Step 5** | (-) blue | [699.2, 897.1, 1277.2] NAUO1 | left | (8, 715); 724 **at the window edge** | `near-left`, 0.05 | 127 / 65 / 46 |
| **Step 5** | h27 | [666.2, 897.1, 1276.1] NAUO1 | right | (1923, 522); 793 **at the window edge** | `up-right`, 0.05 | 141 / 71 / 49 |
| **Step 6** | (-) blue | [699.2, 897.1, 1272.1] NAUO1 | left | (8, 715); 723 **at the window edge** | `near-left`, 0.05 | 127 / 65 / 46 |
| **Step 6** | h29 | [666.2, 897.1, 1271.0] NAUO1 | right | (1923, 521); 793 **at the window edge** | `up-right`, 0.05 | 141 / 71 / 49 |
| **Step 7** | Real Time Clock | [658.4, 917.1, 1290.1] NAUO3 | top | (1049, 64); 276 **at the window edge** | `near-left`, 0.05 | 127 / 65 / 46 |
| **Step 7** | j24 | [661.1, 897.1, 1283.7] NAUO1 | right | (1657, 653); 632 | `near-right`, 0.05 | 127 / 65 / 46 |
| **Step 7** | j19 | [661.1, 897.1, 1296.4] NAUO1 | left | (195, 606); 710 | `near-left`, 0.05 | 127 / 65 / 46 |
| Step 8 | eye | [749.4, 885.6, 1305.0] | unset -> left | (559, 317); 369 | `up-right`, 0.05 | 171 / 86 / 60 |
| **Step 9** | i23 | [663.7, 897.1, 1286.3] NAUO1 | right | (1932, 365); 846 **at the window edge** | `near-right`, 0.05 | 127 / 65 / 46 |
| **Step 9** | (+) red | [696.7, 897.1, 1284.9] NAUO1 | left | (8, 686); 784 **at the window edge** | `near-left`, 0.05 | 127 / 65 / 46 |
| **Step 10** | (-) blue | [699.1, 897.1, 1284.9] NAUO1 | left | (8, 684); 756 **at the window edge** | `near-left`, 0.05 | 127 / 65 / 46 |
| **Step 10** | i24 | [663.6, 897.1, 1283.6] NAUO1 | right | (1932, 362); 828 **at the window edge** | `near-right`, 0.05 | 127 / 65 / 46 |
| **Step 11** | a8 | [689.2, 897.1, 1324.3] NAUO1 | left | (20, 521); 684 | `near-left`, 0.05 | 127 / 65 / 46 |
| **Step 11** | i22 | [663.7, 897.1, 1288.7] NAUO1 | right | (1932, 479); 694 **at the window edge** | `down-left`, 0.05 | 172 / 102 / 75 |
| **Step 12** | a9 | [689.2, 897.1, 1321.7] NAUO1 | left | (8, 540); 710 **at the window edge** | `near-left`, 0.05 | 127 / 65 / 46 |
| **Step 12** | i21 | [663.7, 897.1, 1291.3] NAUO1 | right | (1932, 470); 710 **at the window edge** | `down-left`, 0.05 | 172 / 102 / 75 |
| **Step 13** | a14 | [689.2, 897.1, 1309.1] NAUO1 | right | (1924, 479); 884 **at the window edge** | `down-right`, 0.035 | 130 / 82 / 61 |
| **Step 13** | (-) blue | [699.2, 897.1, 1310.4] NAUO1 | left | (8, 579); 836 **at the window edge** | `near-left`, 0.05 | 127 / 65 / 46 |
| **Step 14** | a12 | [689.2, 897.1, 1314.2] NAUO1 | right | (1924, 481); 904 **at the window edge** | `near-left`, 0.065 | 164 / 84 / 59 |
| **Step 14** | (+) red | [696.6, 897.1, 1310.4] NAUO1 | left | (124, 577); 749 | `near-left`, 0.05 | 127 / 65 / 46 |
| **Step 15** | F4 | [688.2, 954.5, 1285.1] F4 | left | (21, 361); 768 | `down-left`, 0.035 | 130 / 82 / 61 |
| **Step 15** | Rocker Switch | [681.3, 932.2, 1256.6] NAUO46 | unset -> right | (1468, 304); 473 | `near-left`, 0.05 | 127 / 65 / 46 |
| **Step 16** (Lee's camera) | j27 | [661.1, 897.1, 1276.1] NAUO1 | left | (8, 691); 748 **at the window edge** | `near-right`, 0.05 | 127 / 65 / 46 |
| **Step 16** (Lee's camera) | eye | [660.5, 900.4, 1275.8] NAUO47 | top | (840, 64); 623 **at the window edge** | `near-right`, 0.05 | 125 / 62 / 44 |
| **Step 17** (Lee's camera) | (+) red | [696.7, 897.1, 1269.7] NAUO1 | left | (156, 732); 542 | `near-right`, 0.05 | 127 / 65 / 46 |
| **Step 17** (Lee's camera) | eye | [696.1, 900.4, 1269.2] NAUO49 | top | (828, 64); 676 **at the window edge** | `up-right`, 0.035 | 130 / 65 / 45 |
| **Step 18** (Lee's camera) | j29 | [661.1, 897.1, 1271.0] NAUO1 | left | (8, 701); 760 **at the window edge** | `near-right`, 0.05 | 127 / 65 / 46 |
| **Step 18** (Lee's camera) | eye | [660.5, 900.4, 1270.5] NAUO48 | top | (854, 64); 633 **at the window edge** | `near-right`, 0.05 | 125 / 62 / 44 |
| Step 19 | eye | [745.9, 885.6, 1305.0] | unset -> left | (579, 317); 350 | `up-right`, 0.05 | 171 / 86 / 60 |
| **Step 20** | j1 | [661.1, 897.1, 1342.1] NAUO1 | left | (172, 276); 603 | `up-left`, 0.05 | 141 / 71 / 49 |
| **Step 20** | i27 | [663.6, 897.1, 1276.1] NAUO1 | right | (1932, 674); 720 **at the window edge** | `down-right`, 0.035 | 130 / 82 / 61 |
| **Step 21** | j3 | [661.1, 897.1, 1337.0] NAUO1 | left | (104, 339); 622 | `up-left`, 0.05 | 141 / 71 / 49 |
| **Step 21** | i29 | [663.7, 897.1, 1271.0] NAUO1 | right | (1932, 620); 670 **at the window edge** | `near-right`, 0.05 | 127 / 65 / 46 |
| Step 22 | Potentiometer | [723.2, 917.1, 1232.8] NAUO11 | top | (1159, 64); 384 **at the window edge** | `down-right`, 0.035 | 130 / 82 / 61 |
| Step 25 | F1 | [723.8, 919.4, 1256.3] NAUO10 | unset -> left | (763, 465); 220 | `near-left`, 0.05 | 127 / 65 / 46 |
| Step 29 | eye | [723.8, 919.4, 1256.3] NAUO10 | unset -> right | (1340, 331); 205 | `down-right`, 0.065 | 213 / 107 / 75 |
| **Step 30** (Lee's camera) | (+) red | [696.7, 897.1, 1330.6] NAUO1 | left | (8, 305); 726 **at the window edge** | `near-right`, 0.05 | 127 / 65 / 46 |
| **Step 30** (Lee's camera) | eye | [697.0, 899.8, 1331.5] NAUO34 | top | (865, 64); 218 **at the window edge** | `near-right`, 0.05 | 125 / 62 / 44 |
| **Step 31** (Lee's camera) | a5 | [689.3, 897.1, 1332.0] NAUO1 | left | (8, 303); 771 **at the window edge** | `near-right`, 0.05 | 127 / 65 / 46 |
| **Step 31** (Lee's camera) | eye | [689.6, 899.8, 1332.8] NAUO33 | top | (856, 64); 220 **at the window edge** | `near-right`, 0.05 | 125 / 62 / 44 |
| **Step 32** (Lee's camera) | (-) blue | [699.2, 897.1, 1330.6] NAUO1 | left | (8, 307); 721 **at the window edge** | `near-right`, 0.05 | 127 / 65 / 46 |
| **Step 32** (Lee's camera) | eye | [699.5, 899.8, 1331.5] NAUO14 | top | (866, 64); 218 **at the window edge** | `near-right`, 0.05 | 125 / 62 / 44 |
| **Step 33** (Lee's camera) | Alarm Buzzer | [675.0, 912.4, 1220.4] NAUO62 | top | (1211, 64); 439 **at the window edge** | `near-left`, 0.065 | 164 / 84 / 59 |
| **Step 33** (Lee's camera) | j4 | [661.1, 897.1, 1334.5] NAUO1 | left | (8, 291); 845 **at the window edge** | `near-left`, 0.05 | 127 / 65 / 46 |
| **Step 33** (Lee's camera) | eye | [661.0, 898.8, 1333.8] NAUO58 | near-left | (553, 751); 175 | `up-left`, 0.035 | 130 / 65 / 45 |
| **Step 34** (Lee's camera) | (-) blue | [699.2, 897.1, 1340.9] NAUO1 | left | (8, 229); 923 **at the window edge** | `near-right`, 0.05 | 127 / 65 / 46 |
| **Step 34** (Lee's camera) | eye | [699.9, 897.1, 1340.5] NAUO59 | near-left | (501, 745); 175 | `near-left`, 0.05 | 125 / 62 / 44 |
| Step 35 | LCD Screen | [712.2, 919.7, 1314.4] NAUO94 | unset -> left | (157, 656); 372 | `down-right`, 0.05 | 172 / 102 / 75 |
| Step 35 | eye | [735.6, 885.6, 1320.0] | unset -> right | (1589, 482); 481 | `near-left`, 0.035 | 88 / 44 / 31 |
| **Step 36** | GND | [703.6, 941.8, 1353.8] NAUO94 | left | (8, 474); 558 **at the window edge** | `near-right`, 0.035 | 90 / 48 / 34 |
| **Step 36** | (-) blue | [699.2, 897.1, 1279.8] NAUO1 | right | (1879, 290); 713 **at the window edge** | `up-right`, 0.05 | 141 / 71 / 49 |
| **Step 36** | eye | [733.0, 885.6, 1320.0] | unset -> float | (899, 533); 103 | `near-left`, 0.035 | 88 / 44 / 31 |
| Step 37 | VCC | [703.6, 939.2, 1353.8] NAUO94 | left | (8, 473); 571 **at the window edge** | `near-right`, 0.035 | 90 / 48 / 34 |
| Step 37 | (+) red | [696.7, 897.1, 1279.9] NAUO1 | right | (1886, 281); 740 **at the window edge** | `up-right`, 0.05 | 141 / 71 / 49 |
| Step 37 | eye | [740.0, 885.6, 1320.0] | unset -> float | (916, 547); 103 | `near-left`, 0.035 | 88 / 44 / 31 |
| Step 38 | SDA | [703.6, 936.7, 1353.8] NAUO94 | left | (8, 591); 681 **at the window edge** | `near-right`, 0.05 | 127 / 65 / 46 |
| Step 38 | b8 | [686.6, 897.1, 1324.3] NAUO1 | right | (1912, 320); 1017 | `near-right`, 0.065 | 164 / 84 / 59 |
| Step 38 | eye | [747.0, 885.6, 1320.0] | unset -> float | (971, 500); 103 | `near-left`, 0.035 | 88 / 44 / 31 |
| Step 39 | SCL | [703.6, 934.2, 1353.8] NAUO94 | left | (8, 472); 616 **at the window edge** | `near-right`, 0.035 | 90 / 48 / 34 |
| Step 39 | b9 | [686.7, 897.1, 1321.8] NAUO1 | right | (1885, 324); 930 | `near-right`, 0.065 | 164 / 84 / 59 |
| Step 39 | eye | [754.0, 885.6, 1320.0] | unset -> float | (977, 574); 103 | `near-left`, 0.05 | 125 / 62 / 44 |
| Step 40 | USB Cable | [672.1, 905.5, 1346.2] NAUO122 | unset -> float | (840, 496); 103 | unchanged | - |
| Step 41 | 2x F7 | [660.3, 924.5, 1238.3] NAUO42 | unset -> top | (1169, 76); 200 | `near-right`, 0.065 | 164 / 84 / 59 |
| **Step 43** | eye | [673.1, 916.0, 1220.4] NAUO62 | unset -> bottom | (816, 837); 542 | `up-left`, 0.05 | 171 / 86 / 60 |
| Step 44 | eye | [660.3, 924.5, 1238.3] NAUO42 | unset -> bottom | (1260, 837); 407 | `near-right`, 0.05 | 125 / 62 / 44 |
| Step 44 | eye | [691.2, 922.1, 1235.5] NAUO43 | unset -> bottom | (1106, 837); 316 | `down-left`, 0.05 | 171 / 86 / 60 |
| Step 45 | F9 | [704.1, 919.7, 1357.3] NAUO45 | unset -> left | (389, 292); 485 | `near-left`, 0.035 | 90 / 48 / 34 |
| Step 46 | eye | [720.8, 883.6, 1294.1] NAUO10 | unset -> bottom | (902, 820); 313 | `up-left`, 0.05 | 171 / 86 / 60 |
| Step 47 | eye | [688.2, 954.5, 1285.1] F4 | unset -> right | (1579, 64); 395 **at the window edge** | `down-left`, 0.05 | 171 / 86 / 60 |
| **Step 49** (Lee's camera) | F8 | [709.7, 927.3, 1266.5] NAUO44 | unset -> top | (612, 131); 504 | `up-right`, 0.07 | 198 / 99 / 51 (pushed in at 700) |
| Step 50 | eye | [712.2, 919.7, 1314.4] NAUO94 | unset -> left | (420, 424); 271 | `up-left`, 0.05 | 171 / 86 / 60 |
| Step 52 | eye | [720.8, 883.6, 1294.1] NAUO10 | unset -> top | (641, 94); 504 | `up-right`, 0.035 | 130 / 65 / 45 |
| Step 54 | F5 | [655.1, 897.9, 1369.0] F5 | unset -> left | (444, 516); 107 | unchanged | - |
| Step 55 | F2 | [641.6, 930.2, 1298.3] F2 | unset -> right | (1449, 463); 300 | `near-right`, 0.08 | 201 / 102 / 72 |
| Step 55 | eye | [643.1, 889.0, 1339.4] F2 | unset -> right | (1449, 513); 248 | `near-below`, 0.05 | 178 / 89 / 62 |
| Step 56 | F6 | [689.0, 918.8, 1210.7] F6 | unset -> right | (1550, 660); 251 | `down-right`, 0.065 | 214 / 123 / 89 |

## How this was checked (no browser; nothing in the project changed)

- **The player's layout, in Python.** `layoutCallouts()`, `screenRect()` and `skinned()` (player.js) and `cameraPose()` (core.js: fov
  45, padding 1.08 from steps.json) were copied line for line, with Arial Bold for the text widths and the caption box's own wrapping
  (18.4 px, `max-width: min(560px, 70vw)`, full width at top 46 in windows of 700 px or less). Part boxes from model.glb's accessor
  bounds (as three.js `Box3.setFromObject`). Checked against Lee's screenshots: Step 16's j27 at x = 8, its underline at y = 732 (the
  screenshot: 8, about 737); Step 49's F8 at (612, 131) (the screenshot: 612, about 132).
- **Lee's cameras.** First fitted from his screenshots here (residuals 1 - 18 px), then replaced by the camera agent's solved ones
  (round2/cameras.md, now in guide.py); the choices were re-scored with those and did not change.
- **A picture of each view.** model.glb decoded (meshopt) and drawn flat-shaded by depth, with the wires, lead lines, caption box,
  labels, eyes and leaders where the player puts them; every proposed view looked at at 2000 x 1016, 1000 x 634 and 700 x 634.
- **A score at eight window shapes** (2000 x 1017, 1680 x 964, 1440 x 814, 1280 x 634, 1000 x 634, 820 x 528, 768 x 938 portrait,
  700 x 634; Step 49 also 850 and 800 x 634), from a picture of each view in classes (moving part, its wire, other wires, small parts, lead lines, the spots named):
  what each label's box covers, what its leader crosses, its length, clamping, the caption, and every pair of labels and eyes
  overlapping or their leaders crossing. Every combination of 8 places x 5 reaches (0.035 - 0.10) was scored per view; the table's
  choices are the best or within a few points of it, then made regular by hand (each hole's label on its own side where that is
  clear) and looked at. Result for the table above: **no two labels or eyes overlap and no leaders cross at any of the eight
  shapes; none goes under the caption; none is pushed in at the window's edge except Step 49's F8 in windows under about 880 px.**
  Left over: Step 3's "Nano Board" covers 16 - 27 % of the Nano Board (its own part) at 700 and 768 px; in portrait (768 x 938) only,
  the eyes and names of Steps 44, 45, 47, 50, 55 and 56 cover 3 - 22 % of a part that moves in the step (Step 55's F2 label 22 %).
- The arrows of Steps 1 and 22 were projected too: 300 px and more from the labels at every size.

## To look at in the browser once it is in

1. Regenerate and look at Step N of every step in the table at Lee's window and at about 1000 x 634 (the LMS): each label a short
   leader from its hole, none at an edge (the run-through compares labels with steps.json, not where they land).
2. **Step 49 in narrow windows**: F8 is near the right edge of Lee's camera; in windows under about 880 px wide `'up-right'` (0.07,
   as now in guide.py) has no room and the player pushes the label back in, onto F8 (23 % over F8 at 800 px, 65 % at 700 px). Lee
   asked for up and to the right, and at his window and the LMS's 1000 px it is clear. If the LMS frame can be narrower than 880 px,
   `'up-left'` 0.05 is clear at all nine shapes tried; or the player could mirror a near place that would leave the window (a player
   change, for every kit).
3. **Steps whose geometry other round-2 agents change**: Step 35 (Lee: "move the breadboard wires elsewhere for spreading out")
   moves the anchors of the eyes in Steps 35 - 39 (`_mid`, `[x, TABLE_Y + 1.0, LCD_Z]`): their places were chosen for the ribbon where
   it is now; Step 50's new motion and closer camera (the LCD's eye); Step 43's re-routed buzzer leads (the eye is `'up-left'`, off the
   buzzer's way up and across). Re-look at those once their changes are in.
4. The near places are kept apart by choice, not by the player: a later change of camera on any of these steps needs its labels
   looked at again.
5. Step 4 is unchanged (Lee's first round put its label and eye beside the resistor already, reach 0.07).
