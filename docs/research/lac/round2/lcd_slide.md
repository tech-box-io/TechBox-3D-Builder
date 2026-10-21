# LAC round 2, Step 50: the LCD slides into F8's slots along its length (21 Oct 2026)

Lee: "The LCD Display should really slide into F8's slots along its length. Right now the animation has it clipping through the front of
F8 instead of sliding it. For the rotation portion of the animation, it would be more natural to have the left end of the display rotate
up and over the wire / header end instead of flipping under as it does now. Also, a slightly more zoomed in view."

Read-only study. Nothing in the project was edited or regenerated. Step numbers are the player's: Step 50 is the `g.place('Stand the LCD
screen up ...')` at `LAC Build Instructions/guide.py:1047`, and Step 51 is the straighten at `:1052` (working copy, 21 Oct 2026).

## 1. What is there (measured from lac-guide.glb with tools/glbio.py)

**F8 (NAUO44)** is the plate at z 1264.47 - 1267.47 (3 mm), x 703.84 - 720.35. This is its outline, from a 0.1 mm raster of its +z face:

| y (assembly mm) | solid x |
|---|---|
| 881.2 - 887.6 | 706.8 - 717.2 (the tab into F3) |
| 887.6 - 889.5 | 703.8 - 720.4 |
| **889.5 - 895.9** | 703.8 - 712.2 and **714.0 - 720.4**: the bottom slot, **x 712.2 - 714.0** (1.8 mm), closed at the front |
| 895.9 - 943.1 | 703.8 - 709.7 only: the window, open to the front edge (x 709.7 - 720.4) |
| **943.1 - 949.9** | 703.8 - 712.2 and **714.0 - 720.4**: the top slot, x 712.2 - 714.0, closed at the front |
| 949.9 - 951.5 | 703.8 - 720.4 |
| 951.5 - 957.8 | 706.8 - 717.2 (the tab into F4) |

**The LCD (NAUO94)** is 98 x 60 mm:

- Board: x 712.16 - 713.76 (1.6 mm), y 889.52 - 949.52, z 1262.22 (the F8 end) to 1360.22 (the F9, or header, end).
- Display bezel: x 714.76 - 722.76, y 899.52 - 939.52, z 1262.8 - 1359.6. It fits through F8's window.
- Bezel tabs behind the board: x 709.76 - 712.16, at z 1267 - 1271.
- Backpack and I2C header on the back, near the F9 end: x 703.26 - 712.16. The female caps sit at x 702.73 - 704.48 and z 1349.8 - 1357.8.

Seated, the board's two ends pass through F8's slots by 2.25 mm, and the bezel passes through the window.

**What goes wrong now.** The LCD's ride is `[LCD_LIFTED, LCD_OUT, LCD_ANGLED]`:

- `LCD_OUT` to `LCD_ANGLED` is a 40 mm move along -x, at the depth where the board's end is already inside F8 (z 1264.6 - 1265.0). So the top and bottom strips of the board cut through F8's material in front of the slots (x 714.0 - 720.4): **1.48 mm deep, 82 sample points**. That is the clipping Lee saw.
- `LCD_LIFTED` to `LCD_OUT` is a single 170-degree slerp about the LCD's middle. In it the F8 end, which is the left end on screen, dips down and back while the header end swings up and out. The LCD goes **12.9 mm below the table (1032 points)**. On screen the left end drops from 74 % to 87 % of the frame's height before it comes round. That is the flip "under".
- The board can enter the slots only with its own line passing through them. A 14-degree board in a 1.8 mm slot takes up 2.3 mm across the plate, so it must slide in along its own length, as far as the published angled pose has it (2.5 mm deep). It cannot come in from the front.

## 2. The new motion (Step 50: four beats, 3.2 s; was three, 2.4 s)

| stop | pose | where the LCD is |
|---|---|---|
| (start) | `LCD_LYING` | face down beyond the box's +z end. F8 end at (728, 904, 1479), F9 end at (728, 904, 1381). |
| 1 | `LCD_ON_END` `{'t': [46.22, -8.0, 15.33], 'r': [1, 0, 0, 90.0], 'at': [712.96, 919.52, 1360.22]}` | Stood on its header end, face to the front. F9 end at (759.2, 911.5, 1375.6); F8 end straight up at (759, 1010, 1376). |
| 2 | `LCD_OUT` `{'t': [46.22, 0.0, 11.33], 'r': [0, 1, 0, 14.0], 'at': [712.96, 919.52, 1360.22]}` | Tipped over its header end: upright, F8 end angled in 14 degrees, 20 mm out in front. F8 end at (735, 920, 1276). |
| 3 | `LCD_IN` `{'t': [2.9, 0.0, 11.64], 'r': [0, 1, 0, 14.0], 'at': [723.37, 921.6, 1265.11]}` | Moved 20 mm in along -x. The board's end is 9 mm short of F8's inner face. |
| 4 | `LCD_ANGLED` (unchanged) | Slid 12 mm along its own length, (-0.242, 0, -0.970), until the board's end is in F8's slots. This is the published pose without its lift. |

Stops 1 and 2 are written about the board's F9 end, not the LCD's middle. The player turns a part about the pose's `at` and moves that point in a straight line (player.js mixPose). So the header end stays by its wires while the other end goes up and over it.

**On screen** (the new camera, at the screenshots' 1.96:1):

- The left (F8) end rises from (34 %, 74 %) to (58 %, 23 %), above the header end. It crosses over and comes down to its right at (66 %, 39 %).
- The header end only drifts, from (51 %, 57 %) to (57 %, 57 %).
- The old motion took the left end down to (37 %, 87 %) first.

**Beat 1** turns the LCD 120 degrees about (-1, 1, 1)/sqrt 3. **Beat 2** turns it 90 degrees about x, plus the 14-degree yaw: a cartwheel in the plane of its face. Each stretch is under 180 degrees, so the slerp cannot pick the other way round.

**Clearances** (41 samples per beat, the LCD's 54 k vertices):

| beat | lowest point | nearest parts |
|---|---|---|
| 1 | y 892.5 (table 884.61) | F3 14.5 mm, F9 24.5 mm |
| 2 | y 889.1 | F4 14.3 mm, F3 14.9 mm, F8 17.4 mm. Highest point y 1015.6. |
| 3 | y 889.5 | F4 2.0 mm, F3 3.0 mm, F9 4.8 mm, F8 9.2 mm |
| 4 | y 889.5 | F4 2.0 mm, F3 3.0 mm, F9 4.1 mm. Within F8 the board stays on the line of the slots. |

The 2 mm to F4 and the 3 mm to F3 are the seated LCD's own gaps (board top 949.52 against F4's underside at 951.46).

## 3. Collision results

**The LCD against the parts**, as the player mixes poses:

| beat | result |
|---|---|
| Lying -> on end | clear |
| On end -> out | clear (table, F1 and the potentiometer aside, the box) |
| Out -> in | clear |
| In -> angled | **0.51 mm, 6 sample points**, at the very end: the board's back-bottom corner against the bottom slot's back wall, (711.8, 889.5, 1265.0). This is the published 14-degree pose itself (it was 0.51 mm before too), hidden inside the slot. |
| Step 51 as now | F8's slot front wall 0.75 mm into the board half way (164 points), then 0.22 mm into F9 and 0.10 mm into F8 as it seats. Hidden inside the slot; optional fix in section 6. |

**The LCD's wires** were checked with tools/motioncheck.py itself on a scratch steps file (Steps 49c - 51c with these poses and routes), at its 19 moments and again at 99. Steps 50c and 51c show **0 problems**: no wire into the LCD, F8, F9, F3, F4, the breadboard, F1, the potentiometer or the caps, and no two wires closer than 0.9 of their radii. This includes the LCD sweeping past the USB cable, the pot leads and the jumpers.

## 4. Paste into guide.py

The block replaces `guide.py:1024 - 1057`, from the comment "# The LCD into the case" to the end of the Step 51 `g.place`. `LCD_MID` and `LCD_LIFTED` are no longer needed; nothing else uses them, nor the old `LCD_OUT`. Everything it calls is already in guide.py: `turned`, `compose`, `tidy`, `posed_line`, `unit`, `fem_end`, `LCD_HEAD`, `lcd_tail`, `lcd_lead`, `lcd_line` and `via`.

The block was run with copies of those helpers and a recording `g`. It reproduces the checked poses and routes exactly. The copies themselves reproduce steps.json's present 'out' and 'angled' routes to 0.0 mm.

```python
# The LCD into the case (Steps 51, 52 published; Lee, 20 Oct 2026: "the subtleties of how the LCD Display moves into the slots on F9
# and F8"; Lee, 21 Oct 2026, Step 50: "slide into F8's slots along its length", "the left end of the display rotate up and over the
# wire / header end instead of flipping under", "a slightly more zoomed in view"). Step 50, a beat each: stood on its header (F9) end,
# face to the front, its other end raised; tipped over that end, so that it stands upright, its F8 end angled in 14 degrees, 20 mm out
# in front of the case; moved in, its board 9 mm short of F8; slid 12 mm along its own length until the board's end is in F8's notches
# (the published angled pose, without its 2.14 mm lift, which put the LCD's top into F4's underside). Step 51: straightened, pushed
# 14.9 mm further through F8's notches, and slid back 14.9 mm into F9's notches. The first two poses are written about the board's F9
# end, so that the player turns the LCD about that end (it turns a part about the pose's `at`: player.js mixPose): the header end stays
# by its wires while the other end goes up and over it. Moved in sideways (the last version), the board's ends went through the front
# of F8 above and below its window. Its wires stay behind F9: the run from the breadboard round F9's back edge is the seated CAD wire's
# in every shape, and from there each wire runs along F9's far face to the header, turning in to its cap on a 6 mm radius.
LCD_ANGLE_AT = [723.37, 921.6, 1265.11]                             # the upright the LCD is turned about: 3 mm in front of F8, at its notch
LCD_ANGLED = turned([0, 1, 0], 14.0, LCD_ANGLE_AT)                  # (published: 14.0 degrees)
LCD_F9_END = [712.96, 919.52, 1360.22]                              # the middle of the end of the LCD's board by its header, seated
LCD_ALONG = np.array([np.sin(np.radians(14.0)), 0.0, np.cos(np.radians(14.0))])   # the angled LCD's length, from its F8 end to its F9 end
LCD_IN = tidy(turned([0, 1, 0], 14.0, LCD_ANGLE_AT, (LCD_ALONG * 12.0).round(3).tolist()))   # angled, in the case, 12 mm back along its
                                                                    # length: the board's end 9 mm short of F8 (its ends clear of F8 as it comes in)
LCD_OUT = tidy(compose([20.0, 0.0, 0.0], LCD_IN, LCD_F9_END))       # ... 20 mm out in front of the case (clear of F4's front edge as it tips over)
LCD_ON_END = tidy(turned([1, 0, 0], 90.0, LCD_F9_END, (posed_line(LCD_OUT, [LCD_F9_END])[0] + [0.0, -8.0, 4.0] - LCD_F9_END).round(3).tolist()))
                                                                    # stood on its F9 end, face to the front, 8 mm lower and 4 mm further out


def lcd_hook(colour, fem, pose, radius=6.0, reach=6.0):
    """The last two control points of an LCD wire coming in to its female cap with the LCD at `pose`: a quarter turn of `radius` mm onto
    the cap's axis, `reach` mm out from the cap (lcd_tail goes on from there into it), so that the wire does not kink as it turns in."""
    end, out = fem_end(fem, pose)
    b = end + out * reach
    h = b - LCD_HEAD[colour][-1]
    h = unit(h - out * (h @ out))                                   # (the way the wire comes in, square to the cap)
    return [b - radius * h + radius * out, b - radius * h + radius * (out + h) / np.sqrt(2)]


LCD_LEADS = {}
for colour, male, _, fem, _, _, standing_key, seated_key in LCD_WIRES:
    seated = lcd_line(seated_key, male, fem, None)
    head = LCD_HEAD[colour]                                         # (the shared run: on to just round F9's back edge)
    y = fem_end(fem)[0][1]                                          # (the wire's height at the header)
    tail = lambda pose, *controls, reach=6.0: lcd_lead(lcd_tail(head, fem, pose, [[700.0, y, 1364.0], *controls, *lcd_hook(colour, fem, pose)],
                                                                reach=reach), fem, male, pose, head[-1])
    LCD_LEADS[colour] = dict(
        on_end=tail(LCD_ON_END, [722.0, y - 12.0, fem_end(fem, LCD_ON_END)[0][2] - 10.0]),   # (down under the header end and up into the caps)
        out=tail(LCD_OUT, [722.0, y, 1376.0]),
        inside=tail(LCD_IN, [714.0, y, 1374.0]),
        angled=tail(LCD_ANGLED, [712.0, y, 1368.5]),
        standing=lcd_lead(lcd_tail(head, fem, LCD_STANDING, [[697.0, y, 1362.0], [703.6, y, 1358.5]]), fem, male, LCD_STANDING, head[-1]),
        seated=lcd_lead(seated, fem, male, None, head[-1]))
LCD_IN_DIR = [0.62, 0.62, 0.48]                                     # (from the front at the breadboard's end, as before)
g.place('Stand the LCD screen up in front of the case, face to the front. Then move it in and slide it along until the end of its board '
        'goes into the slots in F8, its other end angled out in front of F9.', ride={LCD: [LCD_ON_END, LCD_OUT, LCD_IN, LCD_ANGLED]},
        ride_beats=True, lines=False, eye=[LCD],
        wires_done={f'lcd {c}': [LCD_LEADS[c][k] for k in ('on_end', 'out', 'inside', 'angled')] for c, *_ in LCD_WIRES},
        view_dir=LCD_IN_DIR, frame=([736.7, 938.8, 1396.5], 100.0))   # (the whole move, closer: Lee, 21 Oct 2026; was radius 130.6)
F9_NOTCHES = [[712.1, 947.3, 1359.5], [712.1, 892.6, 1359.5]]       # the end of the LCD's board, where it goes into F9's two notches (seated)
# (Step 51: straightened as it is pushed on through F8's notches, the board kept in the middle of them: through three poses between
# the angled one and the straight one, the board's line crossing F8's middle plane, z 1265.97, at x 713.02; straight from one to the
# other, turned about LCD_ANGLE_AT, the board's front face went 0.75 mm into the notches' front wall half way.)
LCD_STRAIGHTENING = [tidy(compose(turned([0, 1, 0], 14.0 * (1 - k), [712.96, 919.52, 1263.4 + 17.47 * k], [0.06, 0.4 * k, 2.57 - 17.47 * k]),
                                  [0.0, 0.0, 0.0], LCD_ANGLE_AT)) for k in (0.25, 0.5, 0.75)]
g.place("Straighten the LCD screen, pushing it on through the notch in F8, then slide it back until its board goes into the notches in F9.",
        move=[LCD], path=[LCD_ANGLED, *[via(p) for p in LCD_STRAIGHTENING], LCD_STANDING, ZERO], lines_at=F9_NOTCHES,
        wires_done={f'lcd {c}': [LCD_LEADS[c]['standing'], LCD_LEADS[c]['seated']] for c in LCD_LEADS},
        inset=dict(target=[713.1, 919.5, 1356.5], dir=[0.6, 0.3, 0.75], radius=34.0, marks=[([712.1, 947.3, 1356.5], 3.0), ([712.1, 892.6, 1356.5], 3.0)],
                   alt="Close-up of F9: the ends of the LCD screen's board in its two notches"),   # (as published, Step 52)
        view_dir=LCD_IN_DIR, frame=([705.0, 915.0, 1320.0], 110.0))
```

The resulting numbers are given so that a diff of steps.json can be checked against them. `LCD_STRAIGHTENING` is
`{'t': [-0.6, 0.1, -3.65], 'r': [0, 1, 0, 10.5]}`, `{'t': [-0.87, 0.2, -7.38], 'r': [0, 1, 0, 7.0]}` and
`{'t': [-0.65, 0.3, -11.15], 'r': [0, 1, 0, 3.5]}`, all about `[723.37, 921.6, 1265.11]`. For the other poses see the table in section 2.

The caption is a proposal; the old one said "move it in until the end of its board by F8 goes into the notch in F8". "Slots" is Lee's word for them; Step 51's caption still says "notch".

## 5. What the LCD's wires (LCD_LEADS) need

- **One shape per ride stop: four, not three.** `wires_done` is now `[on_end, out, inside, angled]` (was `[LCD_LYING_LEAD, out, angled]`). Step 50 starts from `LCD_LYING_LEAD` as before.
- **`out` must be redrawn.** The new `LCD_OUT` has the F9 end at (759.2, 919.5, 1371.6), against (776.3, 919.5, 1359.9) before. The old controls (`[748, y, 1369]` ...) were for caps 17 mm further out.
- **`on_end` and `inside` are new.**
  - In `on_end` the caps are at the bottom of the upright LCD, (749.8, 913.9, 1390.2 - 1397.9), their pins pointing down. Each wire goes from the end of its shared run, under the header end and up into its cap.
  - In `inside` the caps are at (729.5, 934 - 942, 1371.5), pointing along the LCD's length.
- **`angled` can stay as it is.** Its pose has not changed. The block above redraws it with the same 6 mm turn into the cap, and that version is the one checked. The current one turns in on a 2.0 mm radius; every new shape's turn is 5.4 - 5.7 mm.
- **`standing` and `seated` are unchanged.**

Bend radii of the new shapes (0.5 mm sampling):

| part of the wire | radius |
|---|---|
| where the tail leaves the shared CAD run | at least 7.0 mm (blue) and 10 - 23 mm (the rest), as now |
| the run | at least 4.8 mm |
| the turn into the cap | 5.4 - 5.7 mm |

Seen in rough projections from the Step 50 camera, front and top, at the stops and at nine moments of the motion, the wires hang from the header and turn in without loops.

## 6. Step 51 (optional, included in the block)

Lee asked for Step 51 as it is. The block keeps its stops, wires, inset and camera, and adds three `via` poses. With them the board stays in the middle of F8's slots while it is straightened:

| | as now | with the via poses |
|---|---|---|
| F8 inside the board while straightening | 0.75 mm, 164 points | 0.33 mm, 41 points, in the first quarter |
| at the start | 0.51 mm (the angled pose itself) | 0.51 mm (unchanged) |
| F9 | | grazed 0.05 mm |
| wire problems (motioncheck) | 0 | 0 |

The stops stay ANGLED, STANDING and ZERO, so the two wire shapes still keep pace. To leave Step 51 exactly as it is, drop `LCD_STRAIGHTENING` and use `path=[LCD_ANGLED, LCD_STANDING, ZERO]`. Section 3's checks hold either way.

## 7. Camera (Step 50)

`view_dir=LCD_IN_DIR` (unchanged, so that Steps 50 and 51 are seen from the same side), `frame=([736.7, 938.8, 1396.5], 100.0)`. Before it was `([755.5, 919.5, 1375.9], 130.6)`, so things now look 1.31x bigger.

The target is the middle of the whole new motion on screen; that is the board's sampled vertices at every moment, plus F8's slots and F9's front edge. At 1.96:1, Lee's screenshots, the motion fills 17 % - 83 % of the height and 31 % - 69 % of the width. The tightest frame that keeps it within 90 % of the frame is radius 75.6. In the old camera the old motion filled only the middle half.

| point | screen position (x, y from top) |
|---|---|
| lying LCD | (43 %, 65 %) |
| top of the on-end pose | (58 %, 23 %) |
| F8's bottom slot | (64 %, 42 %) |
| seated LCD | (59 %, 40 %) |

The top slot is behind F4 from this side, as it was. For "slightly" in the gentler sense, radius 110 at the same target fills 21 % - 79 %.

## 8. How it was checked

All scripts and files are in the session scratchpad (`/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/46c40992-e0fc-4f94-b08e-62c20da998a4/scratchpad/lcd/`). Python stayed under about 500 MB.

1. **Parts.** Each part was read piece by piece with tools/glbio.py from `lac-guide.glb` and the extra-part GLBs, at the Step 50c poses from steps.json.
2. **Part collisions (`checker.py`).** For each stretch the LCD's 54 k unique vertices and its four female caps were sampled at 41 points, mixed as `tools/motioncheck.py` `mix()` / player.js `mixPose` does.
   - Each point was tested exactly against F8, F9, F3, F4, both F7s and F1 (at its aside pose). Each plate is a prism: a 0.1 mm raster of its face times its thickness.
   - The reverse was tested too: plate points (0.3 mm grid, 3 layers) inside the LCD's seven component boxes.
   - The other parts were tested by box, and the table plane was checked.
   - On the current motion the checker finds the 1.48 mm clip through F8's front and the LCD 12.9 mm under the table, which is what Lee saw.
3. **Wires.** tools/motioncheck.py was run itself, unchanged, with `--steps` pointing at a scratch steps file. That file is Steps 49c - 51c from steps.json with the new ride, routes and Step 51 path. Its `Model` was replaced by one holding only the 19 parts near the LCD, read with glbio, so the 7 MB CAD was never loaded whole. It was run at the default 19 moments and at 99.
   - A deliberately bad shape (through F9 and the LCD) gave 11 problems, so the setup does detect them.
4. **Copied code.** guide.py's LCD-wire helpers (`fem_end`, `into_fem`, `lcd_line`, `behind_f9`, `lcd_lead`, `lcd_tail`, `LCD_HEAD`) were copied, and they rebuild steps.json's current 'out' and 'angled' routes to 0.0 mm. The block in section 4 was then executed with them and a recording `g`, and it reproduces every checked pose and route exactly.
5. **Camera.** The camera was fitted with the player's own framing: `core.js cameraPose`, fov 45, padding 1.08.

**Not done (read-only):** regenerating, the browser run-through (`_runthrough()` on `player.html`), and looking at Steps 49 - 52. After pasting, run guide.py, then:

- `tools/motioncheck.py "LAC Build Instructions" "Step 50c" "Step 51c"` (expect 0 problems);
- in the player, `_dev.show('Step 50c', 0.3)` and `_dev.show('Step 50c', 0.45)` for the turn over the header end, and `_dev.show('Step 50c', 0.9)` for the slide into F8's slots;
- a camera diff of every other view against steps.json saved before the change. Only Step 50 / 50c should differ.
